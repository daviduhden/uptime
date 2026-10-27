---
name: upptime-template-upgrades
description: Plan and review official Upptime template or monitor upgrades, identify installed versions and generated/custom files, assess conflicts and compatibility, and prepare rollback and validation steps.
---

# Upptime template upgrades

## Use when

The user asks to upgrade Upptime, review template synchronization, compare upstream changes, or resolve an upgrade conflict.

## Inputs and outcome

Need intended target/revision if known and whether update should be planned or applied. Return installed version evidence, upstream changes relevant to this instance, generated/custom conflict map, staged plan, rollback, and validation. Do not execute upgrade without explicit authorization.

## Procedure

1. Identify installed revision from workflow headers/action pins, repository metadata, and `.templaterc.json`; distinguish template version from monitor action version. Here headers currently show Upptime v1.44.0, monitor action v1.44.1, and updates action v1.0.1.
2. Inspect template scope (`.templaterc.json` currently `.github/**/*`), source configuration, local customizations, and worktree state. This repository has a custom PR gate at `.github/workflows/agent-knowledge.yml`; verify actual synchronization behavior for custom paths rather than assuming how the glob treats files absent upstream. Preserve uncommitted work.
3. Consult official release/template notes or compare against the official upstream for the requested target. Use primary official sources; do not assume all upstream files exist locally.
4. Classify changes: generated workflow/template files, maintained source config, custom assets/docs, runtime-generated history/API/graphs/README status. Identify overwritten files and semantic changes to options, token flow, permissions, schedules, runtime, or Pages.
5. Prepare a minimal update plan with pre-update commit/revision, file-by-file conflict handling, safe static validation, post-update observability, and rollback via reverting the update commit. Keep generated data untouched unless the upgrade procedure explicitly regenerates it.
6. Apply only when explicitly authorized. Never run the update workflow or sync remote template as an implicit test.
7. Revalidate installed instructions/skills and their claims against the resulting version; remove stale version-specific statements or document verified behavior.

## Validation and completion

Versions are evidenced, upstream claims are linked or clearly scoped, generated/custom conflicts are listed, rollback is practical, and no remote update was triggered without authorization.

## Common errors and security

- Template sync scope can overwrite workflows or custom files; `.templaterc.json` is consequential.
- A changed action pin may change behavior independently of template version.
- Workflow updates can change write permissions, Issues behavior, schedules, or secret forwarding; review each as operationally significant.
- Never reveal credentials from workflow config/logs or assume an update preserves secrets/settings.

## Example

Before accepting a workflow update, compare its version header and pinned action SHA with the target official template, inspect changes to `permissions` and token fallback, confirm `.upptimerc.yml` remains compatible, then run static validation. Do not invoke `Updates CI` to validate a draft.

## Maintenance & Continuous Learning

After using this skill to change template-managed files or upgrade procedures, review its version and ownership claims against the resulting repository. Update source/generated-file boundaries, sync scope, conflict handling, rollback, tools, examples, and validation when they change. Incorporate reusable compatibility findings, correct stale guidance, and leave out one-off upgrade details. Validate references, frontmatter, and the repository knowledge gate; report synchronization status.
