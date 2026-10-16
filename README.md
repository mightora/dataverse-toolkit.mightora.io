# Mightora Dataverse Tools

Website: https://dataverse-tools.mightora.io/

Fourteen browser-based HTML web resources for Microsoft Dataverse model-driven applications. Download from the site, or install files under webresources/ in an unmanaged solution.

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

## v0.4 Public Beta: Dataverse context fix and three additional tools

The tool catalogue now includes fourteen web resources:

- **REST Studio:** source from [mightora/rest.mightora.io](https://github.com/mightora/rest.mightora.io), integrated as mgt_rest.html. Read and deliberately authorised write actions.
- **FetchFlow Visual Query Builder:** source from [mightora/fetchflow.mightora.io](https://github.com/mightora/fetchflow.mightora.io), integrated as mgt_fetchflow.html. Metadata discovery and read-only FetchXML query execution.
- **Solution Explorer:** source from [mightora/solution-explorer.mightora.io](https://github.com/mightora/solution-explorer.mightora.io), integrated as mgt_solution_explorer.html. Inspect solution ZIPs and permitted Dataverse solution metadata/exports.

The upstream editions are built from pinned source revisions in .github/workflows/vendor-dataverse.yml, copied to webresources and deployment/mightora-dataverse-tools, and checked for JavaScript syntax, unwanted telemetry, and package consistency. The separate fetchflow upstream edition was modified to use supported GetGlobalContext plus authenticated same-origin HTTP instead of parent.Xrm, which is unreliable from app-navigation pages.

**Connection fix:** the original browser tools tried to load ../ClientGlobalContext.js.aspx even when the installed web resource name was flat (mgt_trace.html). Now the loader derives the relative helper path from the actual WebResources URL so flat and virtual-folder web-resource names both work. See docs/DATAVERSE_CONNECTIONS.md and automated tests/context-loader.test.cjs.

**Important packaging distinction:** deployment/mightora-dataverse-tools.zip is a **web-resource bundle**, not a Microsoft Dataverse unmanaged solution. Its files contain no actual solution manifest or model-driven app definition. The declarative app-navigation.json describes where the tools should appear but cannot install them. Export an authentic unmanaged solution with all fourteen web resources and the app definition from Power Apps before pac solution pack or import is possible. Do not describe the web-resource bundle as a Dataverse solution ZIP.

All tools remain **Public Beta**. Live tenant connectivity and installation have not been validated here. No Cloudflare beacon runs in Dataverse-hosted web resources; the separate public website uses Cloudflare Web Analytics only.
