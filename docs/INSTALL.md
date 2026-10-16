# Install Mightora Dataverse Tools in a model-driven app — Public Beta v0.4

The source package provides **14 individual HTML web resources**, not a solution-import ZIP.
The packed deployment/mightora-dataverse-tools.zip is a web-resource bundle,
not a Dataverse unmanaged solution (it has no Solution.xml or app module).

## Recommended flat names

| Tool | Dataverse web-resource name | Access |
|---|---|---|
| Plugin Trace Explorer | mgt_trace.html | Read-only |
| Metadata Explorer | mgt_metadata.html | Read-only |
| FetchXML Studio | mgt_fetchxml.html | Read-only |
| Record Counter | mgt_counter.html | Read-only |
| Solution Inspector | mgt_solutions.html | Read-only |
| Relationship Visualiser | mgt_relationships.html | Read-only |
| Web Resource Browser | mgt_webresources.html | Read-only |
| View Query Inspector | mgt_views.html | Read-only |
| Security Role Catalogue | mgt_security.html | Read-only |
| Environment Diagnostics | mgt_environment.html | Read-only |
| Configuration Migration Studio | mgt_migration.html | **Writes when explicitly authorised** |
| REST Studio | mgt_rest.html | **Can write — confirmation required** |
| FetchFlow Visual Query Builder | mgt_fetchflow.html | Read-only |
| Solution Explorer | mgt_solution_explorer.html | Read-only / solution export |

Original 11 HTML resources also support a virtual-folder name such as
mgt_/trace.html. The three upstream versions are generated for flat
publisher-prefixed names and should retain that naming unless rebuilt.

## Install and test

1. Open Power Apps > Solutions in a development environment.
2. Create or edit your existing **unmanaged solution**.
3. Create or update 14 Webpage (HTML) web resources, using the correct names
   (publisher prefix may be prepended by Power Apps; record the final name).
4. Publish all web resources. Clear cached content or use published version URLs.
5. Edit the model-driven app. Add 14 web resource pages in the appropriate
   navigation groups (refer to deployment/app-navigation.json).
6. Save and publish the model-driven app. Apply role-based access,
   particularly around Configuration Migration and REST Studio.
7. Test the connection using the read-only WhoAmI() request in
   docs/DATAVERSE_CONNECTIONS.md, then test actual table metadata.
8. Export **that solution from Dataverse**. Use pac solution unpack to obtain
   a genuine XML/YAML unpacked solution source. Commit it under a new folder.
9. Use pac solution pack on the genuine unpacked folder. Do not call the
   current generic file bundle an importable unmanaged solution.

### PAC CLI (only after genuine solution export/unpack)

    pac solution unpack --zipfile ./genuine-unmanaged-export.zip --folder ./deployment/real-solution --packagetype Unmanaged
    pac solution pack --zipfile ./deployment/MightoraDataverseTools_unmanaged.zip --folder ./deployment/real-solution --packagetype Unmanaged

The packer's XML format needs Other/Solution.xml and Other/Customizations.xml.
For native Dataverse Git YAML format see Microsoft CLI documentation.

## Privacy and limitations

These HTML web resources run inside the signed-in Dataverse security context.
No Cloudflare analytics scripts are shipped in them. The public download
website separately uses Cloudflare Web Analytics. Data import and REST
request modifications must be authorised and tested in a development tenant.
Source code tests do not prove tenant permissions or production behaviour.

Source: https://github.com/mightora/dataverse-toolkit.mightora.io
