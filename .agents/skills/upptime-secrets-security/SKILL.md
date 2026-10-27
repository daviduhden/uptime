---
name: upptime-secrets-security
description: Audit Upptime secret references, the .upptimerc.yml secrets allowlist, GH_PAT/GitHub App/GITHUB_TOKEN use, Actions permissions, accidental credential exposure, and safe rotation procedures.
---

# Upptime secrets and security

## Use when

Reviewing credentials, GitHub Actions tokens/permissions, secret allowlists, suspected leaks, or credential rotation.

## Inputs and outcome

Need the relevant sanitized config/workflow and intended integrations. Return names/references and exposure paths only, least-privilege findings, prioritized remediation, and rotation steps. Never request or reveal secret values.

## Procedure

1. Inspect secret names and references in `.upptimerc.yml` and generated workflows; inspect `permissions`, token fallback order, checkout, and action pins. Do not query secret values or copy them to output.
2. Confirm installed behavior in actual workflows and official docs. Here workflows prefer a scoped GitHub App token when configured, then `GH_PAT`, then `github.token`; scopes vary by job. `SECRETS_CONTEXT` is generated and comments direct maintainers to configure the allowlist in `.upptimerc.yml`.
3. Check `.upptimerc.yml` `secrets`: when explicit, it is the complete allowlist for contextual secrets. Validate `$NAME` references against names and allowlist, not values. `GH_PAT` is passed separately and should not be in that list.
4. Search tracked source for likely literal credentials using safe pattern/name checks; avoid printing matching lines or values. Treat webhook URLs and embedded credentials as secrets.
5. Assess least privilege: job-level `permissions`, GitHub App permissions, PAT scope/expiry, event context, fork behavior, action pinning, and whether an integration needs write access. Recommend reduction only with evidence that functionality remains supported.
6. If exposure is suspected, recommend immediate revocation/rotation in the relevant GitHub settings and provider, removal from repository history where appropriate, and audit of use. Do not rotate credentials or modify remote settings without explicit authorization.
7. Document a safe rotation sequence: create replacement with minimum scope; store it as a GitHub Actions secret; update references; verify via authorized controlled operation without logging values; revoke old credential; audit.

## Validation and completion

Only names and locations are reported; each reference/allowlist relationship is clear; least-privilege recommendations reflect installed workflows; rotation has an owner/sequence and no values were accessed.

## Common errors and security

- `GITHUB_TOKEN` is constrained by workflow/repository settings; do not assume it can push, deploy, or manage Issues.
- A GitHub App token requires matching repository access and permissions; verify job needs before changing scopes.
- `secrets: []` passes no contextual secret values. Omitted allowlist can enable compatibility auto-detection per installed version; confirm exact behavior.
- Secret masking is not a guarantee against transformed values or URLs in logs. Never echo secrets or enable shell tracing around credentials.

## Example

If a site uses `url: $PRIVATE_API_URL`, verify that the name exists in the explicit `secrets` allowlist and that the relevant generated workflow passes it. Report only the variable name and workflow path, never its value.
