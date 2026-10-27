# Upptime repository guidance

This repository is an Upptime **instance**, not the Upptime engine. It monitors `uhden.dev` and `handbook.uhden.dev`; its installed workflows identify the template as Upptime v1.44.0 and the monitor action as v1.44.1. Treat `.upptimerc.yml` as the primary configuration source.

## Source and generated files

- Editable source: `.upptimerc.yml`, `.templaterc.json`, `.github/ISSUE_TEMPLATE/`, `assets/`, and documentation/instructions added for maintainers.
- Template-generated: existing Upptime runtime workflows under `.github/workflows/`; their headers say updates overwrite changes, so prefer `.upptimerc.yml`. `.github/workflows/agent-knowledge.yml` is a repository-owned PR gate, not an Upptime runtime workflow. `.templaterc.json` includes `.github/**/*`, so review this custom workflow's survival when evaluating template synchronization; do not assume the glob's deletion/overwrite semantics.
- Runtime-generated: `history/`, `api/`, `graphs/`, and the generated status table in `README.md`. Do not hand-edit these; change the source configuration or use a documented, reproducible Upptime procedure.
- `.templaterc.json` currently scopes template synchronization to `.github/**/*`; confirm the effect before changing it.

## Operating rules

- Make small, reversible changes and preserve existing naming, formatting, and repository conventions.
- Check the installed Upptime version/workflows and current official configuration docs before relying on an option. Do not assume this repository contains the upstream source or local build/test commands.
- Never invent commands, configuration keys, validation results, or monitoring capabilities. Clearly distinguish static review from live availability checks.
- Never print secret values, expose private URLs, or access secret values for validation. Do not create real incidents or alter production state as a test.
- Do not close, edit, or publish real incident Issues automatically. Do not publish, change sensitive remote settings, alter production monitoring cadence/permissions, or perform destructive operations without explicit authorization.
- Explain operational risk for changes that affect endpoints, alerting, permissions, schedules, or publication. Verify changes with safe tools available in the repository and report limitations.

## Skill routing

Use the smallest relevant skill set under `.agents/skills/`; combine skills where a change crosses responsibilities. Examples: endpoint change → `upptime-monitoring-config` + `upptime-validation`; false alert → `upptime-incident-triage`; Actions failure → `upptime-github-actions`; page branding → `upptime-status-page`; credentials → `upptime-secrets-security`; upgrade → `upptime-template-upgrades`. Read the selected `SKILL.md` before acting. See [docs/agent-usage.md](docs/agent-usage.md).

## Continuous Agent & Skills Maintenance

### Mandatory review

**Agent instructions and skills are living repository artifacts.**

**Every repository modification MUST include an agent/skills synchronization step.** This applies after code, configuration, dependencies, features, bug fixes, refactors, tests, workflows, documentation, architecture, and instruction changes. Perform one complete synchronization review at the end of the task; repeat validation only if correcting a finding.

**Before completing any task, inspect the applicable AGENTS.md and SKILL.md files, update the affected instructions, and validate their consistency with the implementation.**

**A code change without the corresponding agent knowledge maintenance is considered incomplete.**

**Never claim completion when the synchronization step has been skipped or has failed.**

### Executable procedure

1. Inspect every applicable `AGENTS.md` from repository root through the changed directories. Inventory specialized agents (`.github/agents/*.agent.md`) and skills (`.agents/skills/**/SKILL.md`, `.github/skills/**/SKILL.md`, `.claude/skills/**/SKILL.md`), plus any tool-specific instruction files that exist (such as `CLAUDE.md`, `.cursor/rules/`, or Copilot instructions).
2. Map each changed area and new reusable finding to the existing agent and skills by responsibility. Read the affected files; do not update unrelated skills just to satisfy the policy.
3. Update at least one relevant instruction/agent/skill file with meaningful, reusable knowledge whenever repository files change. Update an existing skill when its scope covers the behavior or its procedure, tools, assumptions, examples, routes, or validation have changed. Create a skill only when a repeatable responsibility has no suitable home; keep it focused and add routing to the relevant agent.
4. Keep the specialized agent's responsibilities and skill routing synchronized with actual skills. Remove stale or duplicate guidance. Do not add timestamps, empty edits, run-specific details, or cosmetic changes as substitutes for operational knowledge.
5. Validate frontmatter and syntax, skill names against directories, required maintenance headings, relative links and skill references, and the final diff. Run the repository gate with `python3 scripts/check-agent-knowledge.py --base <base-ref> --head <head-ref>` for committed comparisons. The PR workflow runs this check automatically. Do not claim that an unavailable check passed.
6. If an applicable instruction cannot be updated, record the reason and mark the task incomplete; do not silently waive the requirement.

### Maintenance headings and self-maintenance

Every specialized agent must have a **Post-Change Knowledge Synchronization** section. Every skill must have a **Maintenance & Continuous Learning** section. These sections require review after the task, relevant knowledge updates, validation, and a final report. When editing this policy, agent, or skills, validate the complete instruction/skill inventory and enforcement mechanism once at the end; no recursive edit loop is required.

### Mandatory Definition of Done

- [ ] Repository changes implemented.
- [ ] Relevant agent instructions reviewed.
- [ ] Relevant skills reviewed.
- [ ] Affected AGENTS.md / SKILL.md files updated.
- [ ] Obsolete knowledge removed.
- [ ] New reusable knowledge incorporated.
- [ ] Agent and skill references validated.
- [ ] Automated maintenance checks passed.
- [ ] Final synchronization status reported.

If any applicable item fails, correct it or explicitly report the limitation and leave the task incomplete. Automated checks verify structural conditions, not semantic relevance; reviewers must confirm that the knowledge change actually helps future work.

### Required final report

Every task summary must include **Agent & Skills Synchronization** with: agents reviewed; skills reviewed; instruction files updated; reusable knowledge added or corrected; validations actually run; and final status **PASS** or **FAIL**. Never report PASS if a required review or check failed or was skipped.
