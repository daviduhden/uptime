# Upptime repository guidance

This repository is an Upptime **instance**, not the Upptime engine. It monitors `uhden.dev` and `handbook.uhden.dev`; its installed workflows identify the template as Upptime v1.44.0 and the monitor action as v1.44.1. Treat `.upptimerc.yml` as the primary configuration source.

## Source and generated files

- Editable source: `.upptimerc.yml`, `.templaterc.json`, `.github/ISSUE_TEMPLATE/`, `assets/`, and documentation/instructions added for maintainers.
- Template-generated: `.github/workflows/*.yml`. Their headers say updates overwrite changes; prefer configuration in `.upptimerc.yml`. Change a workflow directly only for an explicit, documented customization with a maintenance plan.
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
