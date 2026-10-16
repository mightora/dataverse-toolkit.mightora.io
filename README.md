# Mightora Dataverse Tools

Website: https://dataverse-tools.mightora.io/

Eleven browser-based HTML web resources for Microsoft Dataverse model-driven applications. Download from the site, or install files under webresources/ in an unmanaged solution.

- Plugin Trace Explorer: `mgt_/trace.html` (`webresources/mgt_trace.html`)
- Metadata Explorer: `mgt_/metadata.html` (`webresources/mgt_metadata.html`)
- FetchXML Studio: `mgt_/fetchxml.html` (`webresources/mgt_fetchxml.html`)
- Record Counter: `mgt_/counter.html` (`webresources/mgt_counter.html`)
- Solution Inspector: `mgt_/solutions.html` (`webresources/mgt_solutions.html`)
- Relationship Visualiser: `mgt_/relationships.html` (`webresources/mgt_relationships.html`)

Hosted previews use sample data; live data access requires an authenticated Dataverse session. These are early prototypes, not replacements with full XrmToolBox feature parity.

The original hand-built combined model-driven app solution candidate is not import-verified and is not released as a production installer. See docs/INSTALL.md. Open-source under MIT. No backend, token or client secret required.

## Public Beta v0.2
These tools are still undergoing tests and are not production-certified. Report bugs at https://github.com/mightora/dataverse-toolkit.mightora.io/issues.

- Web Resource Browser: `mgt_/webresources.html` (`webresources/mgt_webresources.html`)
- View Query Inspector: `mgt_/views.html` (`webresources/mgt_views.html`)
- Security Role Catalogue: `mgt_/security.html` (`webresources/mgt_security.html`)
- Environment Diagnostics: `mgt_/environment.html` (`webresources/mgt_environment.html`)

## Cloudflare Web Analytics
The public site at dataverse-tools.mightora.io uses a verified Cloudflare Web Analytics token. No Cloudflare analytics or tracking are embedded in Dataverse web resources. Pageview stats do not automatically include reliable direct-file download counts.

## Limitations
Some tools return only the first API pages. The Security Role Catalogue does not calculate effective privileges, and View Inspector currently lists system views. The combined Dataverse solution is still experimental and must be imported, tested and exported from an actual Dataverse development environment.

[Beta audit and known limitations](docs/BETA_AUDIT.md)

## Configuration Migration Studio (public beta v0.3)
- Individual HTML web resource: `webresources/mgt_migration.html`; suggested Dataverse name: `mgt_/migration.html`.
- Define editable schema selections for supported scalar fields, export paged configuration records to Mightora JSON, run a target preflight and cautiously upsert records using their existing GUIDs.
- **This tool performs writes when explicitly authorised**; the other ten utilities are read-only.
- It does **not** read Microsoft's Configuration Migration ZIP/XML files, automatically resolve lookups, migrate relationships, disable plugins, remap users, match configurable natural keys or preserve every attribute type.
- See [capability comparison and safe deployment instructions](docs/CONFIGURATION_MIGRATION.md).
- To add it to the combined **model-driven app**, add `mgt_/migration.html` as a new page and include it in the application's solution. A verified managed Dataverse solution ZIP has not yet been produced.
