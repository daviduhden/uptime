# Upptime agent usage

## Agent

**Upptime Maintainer** is the repository specialist for endpoint configuration, incidents, GitHub Actions, secrets, the public status page, validation, and template upgrades. General repository rules live in [`AGENTS.md`](../AGENTS.md); the GitHub Copilot profile is [`upptime-maintainer.agent.md`](../.github/agents/upptime-maintainer.agent.md).

## Skills

| Skill | Use for |
| --- | --- |
| `upptime-monitoring-config` | Endpoints, HTTP/TCP checks, response rules, secret references |
| `upptime-incident-triage` | Outage evidence, false positives, incident drafts and postmortems |
| `upptime-github-actions` | Workflow failures, schedules, permissions, generated data and deployment jobs |
| `upptime-status-page` | Branding, themes, CSS, URLs, CNAME/baseUrl and Pages diagnosis |
| `upptime-secrets-security` | Secret allowlists, tokens, permissions, exposure and rotation plans |
| `upptime-validation` | Static config and instruction validation after changes |
| `upptime-template-upgrades` | Version review, template conflicts, upgrade and rollback plans |

Skills are under `.agents/skills/<skill-name>/SKILL.md`. Select the narrowest relevant skill and combine where needed. For example, endpoint edits also use validation; secret edits use security and validation; upgrades use upgrade planning and validation.

## Example requests

- “Añade un endpoint HTTPS para `/health`; devuelve 204. Revisa duplicados y valida el cambio.”
- “`uhden.dev` aparece caído, pero funciona en mi navegador. Analiza las evidencias disponibles y prepara un borrador de incidente; no cambies Issues.”
- “Falla `Uptime CI` en el último paso. Diagnostica el log y dime si el workflow es generado.”
- “Quiero cambiar el tema de la página y comprobar rutas para `status.uhden.dev`.”
- “Audita las referencias a secretos y permisos sin leer ni mostrar valores.”
- “Prepara un plan para actualizar la plantilla de Upptime con rollback; no ejecutes la actualización.”

## Validation procedure

After edits, inspect `git diff --check`, parse YAML/frontmatter with validators already available, check duplicate endpoint names/slugs and secret references by name, verify relative links, and review the final diff for generated files. This repository does not define a build/test command. Static validation does not establish endpoint availability, successful deployment, or schema acceptance by the remote Upptime runner. Do not dispatch production workflows or publish as a test.

Every repository change must also include a meaningful update to relevant agent/skill knowledge. The `Agent Knowledge Gate` PR workflow runs `scripts/check-agent-knowledge.py` against the pull request base and head SHAs. Run it locally for committed comparisons with `python3 scripts/check-agent-knowledge.py --base <base-ref> --head <head-ref>`. The script uses Python's standard library and Ruby/Psych (available on GitHub's Ubuntu runner) to check the change gate, instruction frontmatter, required maintenance headings, names, relative links, skill references, and changed YAML. It detects obvious empty/cosmetic updates structurally, but reviewers still need to assess semantic relevance. The gate is repository-owned; `.templaterc.json` includes `.github/**/*`, so verify its behavior during future Upptime template updates.

## Repository boundaries and safety

`.upptimerc.yml` is the central configuration. The checked-in workflows identify themselves as template-generated; prefer config changes and treat direct workflow edits as customizations with overwrite risk. `history/`, `api/`, `graphs/`, and the README status table are generated data. Never expose secret values or private URLs, trigger production effects as tests, or modify real Issues automatically. Changes to monitoring, permissions, schedules, secrets, or publication should include evidence and operational risk.
