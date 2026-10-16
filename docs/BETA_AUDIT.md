# v0.2 Public Beta — audit and known limitations

Date: 16 October 2026. These findings describe **source-level validation**, not certification of live Dataverse behaviour.

## Checks performed
- Verified the ten standalone HTML files are committed to the public repository.
- Syntax-checked every inline JavaScript block for all ten resources.
- Ensured every tool clearly displays a **Public Beta** warning.
- Ensured no Cloudflare analytics beacon or external tracking code is included in any Dataverse web resource.
- Confirmed the public website contains ten tool cards and the Cloudflare beacon is conditional on `dataverse-tools.mightora.io`.
- Confirmed the GitHub Pages build script and ZIP manifest include ten tools.
- Confirmed the verified Cloudflare Web Analytics site registration and the unproxied CNAME record to GitHub Pages.

## Fixes made
- Added spreadsheet formula-injection protection to the shared CSV serialization in the original six tools.
- Avoided loading the Dataverse client context library on public sample previews.
- Made sample-data modes and read-only beta notices more explicit.
- Added visible caps to the Metadata Explorer and Relationship Visualiser.
- Made the Web Resource Browser, View Query Inspector, Role Catalogue and Environment Diagnostics available as separate, read-only HTML resources.
- Added an automated check that validates script syntax and blocks accidental Cloudflare telemetry in downloadable resources.

## Open limitations and follow-up tests
| Tool | What to verify in a disposable development tenant |
| --- | --- |
| Plugin Trace Explorer | Trace logging enabled/disabled, privileges, throttling, paging and exception details |
| Metadata Explorer | Paging beyond 1,000 columns, label fallbacks and virtual tables |
| FetchXML Studio | Joined-table aliases, paging beyond first result page, malformed XML and CSV formula sanitization |
| Record Counter | Count cap around 5,000/500 for elastic tables; never imply an approximate result is exact |
| Solution Inspector | Solution component paging and privileges for large installed solutions |
| Relationship Visualiser | Many-to-many relationships, diagram 12-table cap and schema paging caps |
| Web Resource Browser | Unicode and binary web resources, very large base64 values, permissions |
| View Query Inspector | System views only; personal views not implemented, layout XML download not included |
| Security Role Catalogue | Lists roles; no effective privileges, BU inheritance or user/team role resolution |
| Environment Diagnostics | Restricted organization metadata, no access to some user fields and API errors |

## Deployment and solution
- **Website:** GitHub Pages deployment must complete before live operation is considered verified.
- **Cloudflare:** Cloudflare Web Analytics site exists and the manually installed beacon only loads on the public hostname. Pageviews do not guarantee download counts.
- **Dataverse:** No direct tenant integration or permissions testing has been performed.
- **Solution ZIP:** The combined managed/unmanaged model-driven app solution is **not yet import-verified**. A real environment import, publish, test and export remains required.
- **Security:** CodeQL workflow is configured, but a workflow badge is not a guarantee that every risk has been reviewed. No external security certification is claimed.

## Next priorities
1. Live Dataverse test matrix: app navigation, 401/403, paging, export, and differing roles.
2. Read-only compatibility improvements and accessibility testing on mobile.
3. Safe bulk operations behind explicit environment checks, dry-run and audit logging.
4. Validated solution packaging from a real Power Platform development environment.

Report reproducible issues at https://github.com/mightora/dataverse-toolkit.mightora.io/issues.
