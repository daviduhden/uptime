---
name: upptime-github-actions
description: Review and troubleshoot this repository's Upptime GitHub Actions workflows, including scheduled checks, failed runs, permissions, generated data, setup, and Pages-related build jobs.
---

# Upptime GitHub Actions

## Use when

An Upptime workflow fails, schedules behave unexpectedly, generated data is stale, or workflow permissions/dependencies need review.

## Inputs and outcome

Need workflow/run name, run URL or sanitized logs, approximate time, and recent relevant changes. Return the workflow path/job/step, evidence-based cause or ranked hypotheses, safe remediation, and whether files are template-generated.

## Procedure

1. Inspect `.github/workflows/` and `git status`; read workflow headers, version/action pins, triggers, concurrency, permissions, and referenced configuration.
2. This repository's Upptime workflow headers identify v1.44.0. Runtime workflows are template-generated; `.github/workflows/agent-knowledge.yml` is repository-owned PR validation. `.templaterc.json` includes `.github/**/*`; when assessing upgrades, verify how custom workflow files survive template sync rather than assuming glob semantics. Prefer `.upptimerc.yml` for Upptime behavior.
3. Inspect supplied or authorized run logs by step. Check YAML/workflow validation failures, checkout/token permissions, action pin/availability, monitor command failures, commit/push errors, and Pages deploy output separately.
4. Compare workflow purpose: `uptime.yml` checks every five minutes and can manage Issues; `response-time.yml` measures response time; `graphs.yml` generates graphs; `summary.yml` updates README; `site.yml` builds/deploys Pages; `setup.yml` responds to config changes and has broader permissions; `updates.yml` syncs template code.
5. Confirm conclusions against actual triggers and permissions; do not infer schedule execution from cron alone (GitHub scheduling can be delayed/disabled).
6. Recommend the smallest fix. If a workflow edit is necessary, explain overwrite risk and propose how to preserve/document it. Do not change production cadence or permissions without evidence and reviewed justification.
7. Validate statically with available tools; do not dispatch a production workflow as a test without explicit authorization.

## Validation and completion

Failure is tied to a specific log/config fact or marked as a hypothesis; generated/custom ownership is identified; permission changes have a least-privilege rationale; no remote run or setting was changed without authorization.

## Common errors and security

- Setup workflow failures can relate to incorrect `owner`/`repo`, configuration syntax, token scope, or template sync; distinguish evidence.
- Push failures may depend on GitHub App token, `GH_PAT`, or `GITHUB_TOKEN` configuration and repository settings; never reveal credentials.
- Large `SECRETS_CONTEXT` environment lines are generated from configured secret allowlists; do not edit them manually.
- Avoid broadening job permissions to “fix” an unexplained failure. Keep action pins and identify supply-chain changes explicitly.

## Example

For a failed `Graphs CI` run, inspect its “Generate graphs” log and token/checkout errors. The workflow is generated, so prefer an official config correction; only propose direct workflow customization with a reproducible maintenance plan.

For the `Agent Knowledge Gate`, inspect `scripts/validate-agent-knowledge.py` and the PR base/head comparison. It uses Python's standard library and Ruby/Psych for YAML parsing, requires a substantive changed instruction/skill file, checks maintenance headings and relative links, and cannot assess semantic relevance.

## Maintenance & Continuous Learning

After using this skill to change a workflow or its operating procedure, review it against the resulting workflow files and behavior. Update version markers, ownership assumptions, schedule/permission guidance, tools, examples, and validation steps when they change. Add reusable failure evidence, correct inaccurate instructions, and exclude run-specific details. Validate frontmatter, workflow references, and the repository knowledge gate; report synchronization status.
