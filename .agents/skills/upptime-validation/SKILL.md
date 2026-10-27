---
name: upptime-validation
description: Safely validate Upptime repository changes, including YAML syntax, .upptimerc.yml consistency, duplicate endpoints, secret references by name, agent/skill frontmatter, and changed-file scope.
---

# Upptime validation

## Use when

After changes to Upptime config, agent instructions, skills, status page sources, or workflows; pair with the skill that owns the change.

## Inputs and outcome

Need the working tree/diff and available local tools. Return errors, warnings, checks passed, and unverified live behaviors, clearly separating static validation from real availability checks.

## Procedure

1. Inspect `git status --short` and `git diff --check`; preserve unrelated user changes.
2. Detect available YAML/frontmatter validators (for example, existing `yamllint` only if installed). Do not install dependencies or invent repository commands. Use available offline tools to parse YAML including `.upptimerc.yml` and skill/agent frontmatter.
3. Review site entries for required name/URL or TCP host/port, duplicate names/slugs/normalized endpoints, HTTP/TCP option consistency, and supported option names against official docs for installed version.
4. Collect `$NAME` references and compare names with explicit `secrets` allowlist and generated workflow mappings. Never inspect secret values; distinguish runtime placeholders from repository secrets.
5. Check agent files: Copilot agent has YAML frontmatter with `name` and `description`; each skill directory has a `SKILL.md`, valid YAML frontmatter with `name` and `description`, name matching directory, and focused instructions.
6. Check internal relative links/references, routing names, and generated-file scope. Ensure no unintended edits in `api/`, `graphs/`, `history/`, generated README status content, or generated workflows.
7. Do not perform live network probes, dispatch workflows, open/close Issues, or deploy as validation unless explicitly authorized.
8. Report each check with evidence and limitations. A parse pass does not prove Upptime schema acceptance or endpoint availability.

For committed PR comparisons, run `python3 scripts/check-agent-knowledge.py --base <base-ref> --head <head-ref>`. It validates the changed-file gate, substantive knowledge diff threshold, instruction frontmatter and required headings, skill-directory names, relative Markdown links, agent skill references, and changed YAML using Ruby/Psych. The GitHub Actions PR workflow runs it automatically. This is a structural gate; reviewers still determine whether the knowledge update is semantically relevant.

## Validation and completion

All available static checks pass or findings are recorded; secret values remain inaccessible; result categories distinguish error/warning/pass/unverified; final diff is reviewed.

## Common errors and security

- YAML parsers can interpret GitHub Actions `on` as a boolean under YAML 1.1; use a workflow-aware validator or account for parser version.
- Valid YAML may still use unsupported Upptime keys or invalid combinations.
- Search results can include sensitive lines; report only file/name and redact content.
- Never claim actual uptime based on config validation.

## Example

For an endpoint change, parse `.upptimerc.yml`, confirm a unique site and valid check fields, inspect `$PRIVATE_API_URL` against the allowlist by name, run available lint/whitespace checks, then state “static checks passed; no live availability check performed.”

## Maintenance & Continuous Learning

After using this skill to change validation procedures or repository files, review it against the validators and enforcement workflow that now exist. Update commands, covered file types, references, examples, and the distinction between structural and semantic checks when they change. Add reusable validation findings, correct inaccurate procedures, and avoid task-specific output. Validate frontmatter, references, and the knowledge gate itself; report synchronization status.
