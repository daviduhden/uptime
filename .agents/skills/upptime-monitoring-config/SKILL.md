---
name: upptime-monitoring-config
description: Configure or review monitored sites in this Upptime repository's .upptimerc.yml, including HTTP methods, headers, response rules, TCP checks, endpoint additions/removals, and secret references.
---

# Upptime monitoring configuration

## Use when

The request adds, edits, removes, or audits a monitored endpoint or its HTTP/TCP check. Pair with `upptime-validation` after edits.

## Inputs and outcome

Need the intended service name, endpoint (or secret name), protocol/check type, expected behavior, and any required request data. Return the minimal configuration diff, compatibility evidence, and validation result. Ask only for missing details that change behavior; never guess production endpoints or credentials.

## Procedure

1. Inspect `.upptimerc.yml`, `git status`, current site slugs/names/URLs, workflows, and installed version markers.
2. Confirm syntax and feature support against official Upptime configuration docs for this version. Current docs support HTTP `method`, `headers`, `body`, `expectedStatusCodes`, body status rules, TCP `check: tcp-ping` with `port`, and TCP `check: tcp` body rules. TCP checks do not imply TLS.
3. Check duplicates by URL/name/slug and existing history/API/graph naming implications. Do not rename a service casually: generated history/graph paths are keyed by slug.
4. For HTTP, select a meaningful path and expected status behavior; configure headers/body only as required. Avoid sending mutating requests to production unless explicitly authorized.
5. For TCP, require a host and valid port. Distinguish connection-only `tcp-ping` from application/banner checks using `tcp` and supported body rules.
6. For secret substitutions, use `$SECRET_NAME` and ensure the top-level `secrets` allowlist contains it when explicit allowlisting is configured. Do not access or print secret values. Treat URLs as public unless safely sourced from a secret.
7. Edit only `.upptimerc.yml` for endpoint configuration. Do not hand-edit generated history, API, graphs, or workflows.
8. Run `upptime-validation` and inspect the diff. Report expected monitoring and incident effects; do not trigger a real check as a test.

## Validation and completion

YAML parses; each site has a unique name/slug and appropriate URL or TCP host/port; referenced options are documented for installed version; secret references are named and allowlisted appropriately; generated files are untouched. Clearly report anything that cannot be verified locally.

## Common errors and security

- A `tcp-ping` proves only that a connection opened, not that the application works.
- Body regex syntax is JavaScript regex syntax; invalid patterns can fail a workflow.
- `secrets: []` intentionally passes no contextual secrets; do not add `GH_PAT` to this list.
- Do not put credential literals in YAML, logs, examples, or URLs. Avoid real mutating HTTP checks.

## Example

For a documented health endpoint, add a uniquely named site with its HTTPS URL and an `expectedStatusCodes` list only if defaults are insufficient. For a private endpoint, use `url: $PRIVATE_API_URL`, add `PRIVATE_API_URL` to explicit `secrets`, and never print its value.

## Maintenance & Continuous Learning

After using this skill to change the repository, review it against the resulting configuration and behavior. Update it when supported options, endpoint conventions, secret handling, tools, or validation steps change; add reusable findings and correct inaccurate guidance. Keep examples and procedures current, omit one-off incident details, and validate frontmatter, references, and the repository knowledge gate. Report the review and any update in the final synchronization status.
