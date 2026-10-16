# Mightora Dataverse Tools

Website: https://dataverse-tools.mightora.io/

Six read-only HTML web resources for Microsoft Dataverse model-driven applications. Download from the site, or install files under webresources/ in an unmanaged solution.

- Plugin Trace Explorer: `mgt_/trace.html` (`webresources/mgt_trace.html`)
- Metadata Explorer: `mgt_/metadata.html` (`webresources/mgt_metadata.html`)
- FetchXML Studio: `mgt_/fetchxml.html` (`webresources/mgt_fetchxml.html`)
- Record Counter: `mgt_/counter.html` (`webresources/mgt_counter.html`)
- Solution Inspector: `mgt_/solutions.html` (`webresources/mgt_solutions.html`)
- Relationship Visualiser: `mgt_/relationships.html` (`webresources/mgt_relationships.html`)

Hosted previews use sample data; live data access requires an authenticated Dataverse session. These are early prototypes, not replacements with full XrmToolBox feature parity.

The original hand-built combined model-driven app solution candidate is not import-verified and is not released as a production installer. See docs/INSTALL.md. Open-source under MIT. No backend, token or client secret required.
