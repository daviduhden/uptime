---
name: upptime-status-page
description: Configure or troubleshoot the Upptime public status website, including branding, themes, CSS, visible text/links, CNAME, baseUrl, Pages deployment, and asset routes.
---

# Upptime status page

## Use when

A request changes status page identity/design/links/domain or investigates missing pages, styles, assets, or GitHub Pages deployment.

## Inputs and outcome

Need desired visible change, hosting URL/custom domain, and relevant deployment evidence. Return configuration/assets diff or diagnosis, expected URL/path impact, and safe validation evidence.

## Procedure

1. Inspect `status-website` in `.upptimerc.yml`, `assets/`, `site.yml`, `.templaterc.json`, and installed Upptime version. This instance currently uses `cname: status.uhden.dev`, name `UDENIX Service Status`, and deploys via its generated site workflow.
2. Confirm option support with current official configuration docs and installed version. Prefer documented keys in `status-website`; use `assets/` for custom CSS/theme resources where appropriate.
3. Check domain/DNS and hosting intent before changing CNAME or base URL. With a custom domain at root, do not add a repository path unless hosting requires one. Project Pages needs `baseUrl: /<repo>`.
4. For CSS/assets, verify relative/absolute URL behavior against the configured base path and that the asset is in a directory served by Upptime. Avoid custom executable scripts or unsanitized HTML unless specifically requested and reviewed.
5. Diagnose Pages by separating site generation, deployment workflow, Pages source/settings, CNAME/DNS, and browser asset paths. Use logs or supplied evidence; do not publish to test.
6. Edit configuration and intentional source assets only. Do not edit generated site output or generated workflows directly unless an explicit customization includes a maintenance plan.
7. Validate YAML, paths, relative links, and diff; explain that deployed appearance remains unverified until an authorized publication.

## Validation and completion

Configuration option is supported, domain/base path agree with hosting, referenced assets exist, generated output is untouched, and deployment limitations are explicit.

## Common errors and security

- Missing `baseUrl` on project Pages can break CSS/resource paths.
- Wrong CNAME/DNS or GitHub Pages source can produce 404 even when site generation succeeds.
- External CSS/JS creates availability and supply-chain dependencies; custom HTML can inject active content.
- Public status pages must not reveal private service URLs, tokens, or sensitive incident details.

## Example

To add a theme, place a reviewed stylesheet in `assets/` and point `status-website.themeUrl` at its published URL only after confirming this version's asset routing; verify path behavior for `status.uhden.dev` before publication.

## Maintenance & Continuous Learning

After using this skill to change page configuration, assets, or publication procedures, review it against the resulting setup. Update supported options, domain/base path assumptions, asset routes, tools, examples, and validation when they change. Add reusable findings, correct inaccurate guidance, and omit one-off deployment details. Validate frontmatter, relative references, and the repository knowledge gate; report synchronization status.
