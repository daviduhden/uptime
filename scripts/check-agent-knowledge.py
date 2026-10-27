#!/usr/bin/env python3
"""Enforce structural agent/skill synchronization on a Git comparison."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

ROOT_POLICY = "Continuous Agent & Skills Maintenance"
AGENT_POLICY = "Post-Change Knowledge Synchronization"
SKILL_POLICY = "Maintenance & Continuous Learning"


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def is_knowledge(path: str) -> bool:
    p = PurePosixPath(path)
    return (
        p.name == "AGENTS.md"
        or p.name == "SKILL.md"
        or p.name.endswith(".agent.md")
        or p.name == "CLAUDE.md"
        or p.name == "copilot-instructions.md"
        or (".cursor" in p.parts and p.suffix == ".mdc")
    )


def changed_paths(base: str, head: str) -> list[tuple[str, str]]:
    raw = git("diff", "--name-status", "--find-renames", f"{base}...{head}")
    changes = []
    for line in raw.splitlines():
        fields = line.split("\t")
        status = fields[0]
        # Renames have old and new paths. Validate the destination and count it
        # as a modification, while a deleted knowledge file cannot satisfy the gate.
        if status.startswith("R"):
            changes.append(("D", fields[1]))
            changes.append(("A", fields[2]))
        else:
            changes.append((status[0], fields[1]))
    return changes


def show(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def tree_paths(ref: str) -> list[str]:
    return git("ls-tree", "-r", "--name-only", ref).splitlines()


def substantive_knowledge_diff(base: str, head: str, path: str) -> bool:
    patch = git("diff", "--no-ext-diff", "--unified=0", f"{base}...{head}", "--", path)
    changed_lines = []
    for line in patch.splitlines():
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        content = line[1:].strip()
        if content.startswith(("#", "---", "```")):
            continue
        # Ignore formatting-only edits and count actual prose/config tokens.
        normalized = re.sub(r"[^A-Za-z0-9]+", " ", content).strip()
        if len(normalized.replace(" ", "")) >= 24 and len(normalized.split()) >= 4:
            changed_lines.append(normalized)
    # Heading-only, whitespace-only, and short cosmetic edits are insufficient.
    return (
        sum(len(line.replace(" ", "")) for line in changed_lines) >= 55
        and len(changed_lines) >= 1
    )


def extract_frontmatter(
    text: str, path: str
) -> tuple[dict[str, str] | None, str | None]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return None, f"{path}: missing or malformed YAML frontmatter"
    ruby = r"""require "yaml"; require "json"; value = YAML.safe_load(STDIN.read, permitted_classes: [], permitted_symbols: [], aliases: false); abort "frontmatter must be a YAML mapping" unless value.is_a?(Hash); puts JSON.generate(value)"""
    result = subprocess.run(
        ["ruby", "-e", ruby],
        input=match.group(1),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None, f"{path}: invalid YAML frontmatter ({result.stderr.strip()})"
    fields = json.loads(result.stdout)
    for key in ("name", "description"):
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            return (
                None,
                f"{path}: frontmatter requires non-empty top-level string {key}",
            )
    return fields, None


def required_heading(path: str) -> str | None:
    p = PurePosixPath(path)
    if p.name == "AGENTS.md" and p.parent == PurePosixPath("."):
        return ROOT_POLICY
    if p.name.endswith(".agent.md"):
        return AGENT_POLICY
    if p.name == "SKILL.md":
        return SKILL_POLICY
    return None


def markdown_links(path: str, text: str, paths: set[str]) -> list[str]:
    errors = []
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().split("#", 1)[0]
        if not target or target.startswith(("https://", "http://", "mailto:", "tel:")):
            continue
        resolved = PurePosixPath(path).parent.joinpath(target)
        normalized = []
        for part in resolved.parts:
            if part in ("", "."):
                continue
            if part == "..":
                if normalized:
                    normalized.pop()
            else:
                normalized.append(part)
        candidate = "/".join(normalized)
        if candidate not in paths and not any(
            item.startswith(candidate.rstrip("/") + "/") for item in paths
        ):
            errors.append(f"{path}: broken relative link {target}")
    return errors


def validate(base: str, head: str) -> list[str]:
    errors: list[str] = []
    changes = changed_paths(base, head)
    if not changes:
        return ["No repository changes found in the supplied base/head comparison."]

    knowledge_changes = [
        (status, path) for status, path in changes if is_knowledge(path)
    ]
    project_changes = [
        (status, path) for status, path in changes if not is_knowledge(path)
    ]
    eligible = [
        path
        for status, path in knowledge_changes
        if status != "D" and show(head, path) is not None
    ]
    substantive = [
        path for path in eligible if substantive_knowledge_diff(base, head, path)
    ]
    if not substantive:
        errors.append(
            "No substantive agent/skill knowledge update detected. Every repository change "
            "must include a meaningful AGENTS.md, agent, or SKILL.md update; heading-only, "
            "whitespace-only, and short cosmetic edits do not satisfy the gate."
        )
    all_paths = tree_paths(head)
    path_set = set(all_paths)
    instruction_paths = [path for path in all_paths if is_knowledge(path)]
    skill_names = set()

    for path in instruction_paths:
        text = show(head, path)
        if text is None:
            continue
        heading = required_heading(path)
        if heading and not re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text):
            errors.append(f"{path}: required section heading missing: {heading}")
        if path.endswith("/SKILL.md") or path == "SKILL.md":
            fields, error = extract_frontmatter(text, path)
            if error:
                errors.append(error)
            else:
                folder = PurePosixPath(path).parent.name
                if fields["name"] != folder:
                    errors.append(
                        f"{path}: skill name '{fields['name']}' must match directory '{folder}'"
                    )
                skill_names.add(fields["name"])
        elif path.endswith(".agent.md"):
            _, error = extract_frontmatter(text, path)
            if error:
                errors.append(error)
        errors.extend(markdown_links(path, text, path_set))

    for path in all_paths:
        if path.endswith(".md") and path not in instruction_paths:
            text = show(head, path)
            if text is not None:
                errors.extend(markdown_links(path, text, path_set))

    # Validate changed YAML documents and the YAML frontmatter above using the
    # platform Ruby/Psych parser; no project package installation is needed.
    for status, path in changes:
        if status == "D" or not path.endswith((".yml", ".yaml")):
            continue
        content = show(head, path)
        if content is None:
            continue
        result = subprocess.run(
            ["ruby", "-e", "require 'yaml'; YAML.safe_load(STDIN.read, aliases: true)"],
            input=content,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            errors.append(f"{path}: invalid YAML ({result.stderr.strip()})")

    for path in instruction_paths:
        if path.endswith(".agent.md"):
            text = show(head, path) or ""
            for name in re.findall(r"`(upptime-[a-z0-9-]+)`", text):
                if name not in skill_names:
                    errors.append(f"{path}: references missing skill '{name}'")

    if (
        not any(error.startswith("No repository changes") for error in errors)
        and not errors
    ):
        print(
            f"Changed files: {len(changes)} ({len(project_changes)} project, {len(knowledge_changes)} knowledge)"
        )
        print("Substantive knowledge updates: " + ", ".join(substantive))
        print(f"Validated instruction files: {len(instruction_paths)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base", required=True, help="Base Git ref (usually PR base SHA)"
    )
    parser.add_argument(
        "--head", required=True, help="Head Git ref (usually PR head SHA)"
    )
    args = parser.parse_args()
    try:
        errors = validate(args.base, args.head)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"Agent knowledge validation could not run: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Agent & Skills Maintenance validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(
            "Update relevant agent knowledge, correct structural issues, and rerun this check. "
            "Structural validation cannot determine whether the update is semantically relevant.",
            file=sys.stderr,
        )
        return 1
    print("Agent & Skills Maintenance validation PASSED.")
    print("Reviewers must still assess the semantic relevance of the knowledge update.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
