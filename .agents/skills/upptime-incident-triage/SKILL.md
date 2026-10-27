---
name: upptime-incident-triage
description: Investigate Upptime outages, suspected false positives, failed endpoint checks, and incident evidence from history files or GitHub Actions logs; prepare evidence-based incident updates and postmortems.
---

# Upptime incident triage

## Use when

A monitored service is reported down/degraded, a user suspects a false positive, or incident communications/postmortem are needed.

## Inputs and outcome

Use the service/slug, approximate timestamps and timezone, observed symptoms, relevant run logs, and independent evidence if available. Produce a timeline, likely failure layer(s), confidence, next safe checks, and a draft communication/postmortem. Clearly label unknowns.

## Procedure

1. Identify the service in `.upptimerc.yml` and correlate its slug with `history/<slug>.yml`, Issues supplied by the user, and relevant Actions runs/logs supplied or accessible.
2. Build a UTC timeline from `lastUpdated`, status/code/responseTime, workflow start and error timestamps. Do not treat stale history as a live result.
3. Separate monitor failure from service failure. Examine runner/network/DNS errors, HTTP code and redirects, TLS/certificate errors, timeout/connect phase, authentication responses, and application body rules. Compare independent probes only when available and safe.
4. Look for shared versus endpoint-specific patterns, recent configuration/workflow changes, and geographic differences (including Globalping if configured).
5. State hypotheses with supporting and contradicting evidence. Recommend safe read-only checks first; avoid repeated high-impact requests or exposing private targets.
6. Draft a neutral incident update with impact, start time, current confidence/status, and next update expectation. Draft a postmortem with impact, timeline, root cause (or unknown), contributing factors, detection, and actions.
7. Never create, close, edit, or publish real GitHub Issues automatically. Do not run production-impacting probes without explicit authorization.

## Validation and completion

Claims map to evidence, timestamps have timezone, uncertainty is explicit, and recommended actions have owners/evidence where known. No real Issue or production state was changed.

## Common diagnostic clues

- DNS: resolver failure, NXDOMAIN, SERVFAIL, or inconsistent answers.
- TLS: expiration, hostname mismatch, chain or handshake failure; distinguish these from HTTP status.
- HTTP: 401/403 may be auth/WAF policy, 404 may indicate path or expected-status mismatch, 5xx suggests upstream/application but needs corroboration.
- Timeouts: compare connection and total/request timeout evidence; a slow application and a runner network issue are different hypotheses.
- Body-rule failure: HTTP may return success while the configured expected text/regex is absent.

## Security

Redact tokens, authorization headers, private URLs, and user data from copied logs and drafts. Never display secret values or claim an outage is resolved from a single uncorroborated check.

## Example

“The latest recorded check for slug `uhden-dev` reports HTTP 200 at [timestamp]; that supports availability at that time but does not establish current health. The failed run log shows a DNS resolution error, so first compare DNS from an independent resolver and inspect the relevant Actions runner log.”
