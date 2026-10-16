# Configuration Migration Studio — Mightora Beta v0.3

**Source:** `webresources/mgt_migration.html`  
**Dataverse web resource name:** `mgt_/migration.html`  
**Website:** https://dataverse-tools.mightora.io/  
**Status:** Public beta; no direct production deployment or cross-environment import tests completed.

## What Microsoft Configuration Migration supports

Microsoft's official tool defines reusable schema XML describing tables, fields and relationships, checks dependencies, configures uniqueness conditions, exports a Microsoft-native ZIP, and imports dependent data in multiple passes. It also provides user mapping, options for disabling plug-ins temporarily and demo-oriented date shifting. It is widely used for configuration or reference data rather than bulk transactional data.

References:
- https://learn.microsoft.com/en-us/power-platform/admin/manage-configuration-data
- https://learn.microsoft.com/en-us/power-platform/admin/create-schema-export-configuration-data
- https://learn.microsoft.com/en-us/power-platform/admin/import-configuration-data

## Current Mightora features

1. Browse Dataverse table metadata using the current model-driven-app sign-in.
2. Add tables, choose supported create/update scalar columns and configure an optional OData filter.
3. Export a JSON schema locally and reuse it in another session.
4. Export paged records and primary GUIDs into a **Mightora JSON package** (maximum 2,000 records per table).
5. Load the package in the target environment and validate target table/field metadata; sample-check five record IDs per table to distinguish existing and missing rows.
6. Explicitly confirm backup, business-impact and lookup/relationship limitations; require typing the exact target hostname.
7. Sequentially upsert using `PATCH /api/data/v9.2/<entityset>(<GUID>)`; preserve source IDs, log success/failure for each row, support stop after the current operation and export activity logs.
8. An interactive GitHub Pages sample preview using fabricated records with all network writes disabled.

## Deliberate beta limitations

| Microsoft feature | Current support |
| --- | --- |
| Schema designer | Yes, supported scalar attributes only |
| Save schema | Yes, custom JSON; **not** Microsoft's XML |
| Relationships and missing dependency checks | Not implemented |
| Microsoft ZIP data package | **Not compatible**; Mightora-specific JSON only |
| Natural or composite uniqueness keys | **Not implemented**; GUID-based upsert only |
| Foundation/dependent multi-pass linking | Not implemented |
| User/team mapping | Not implemented |
| Plug-in suppression during import | Not implemented; normal Dataverse plug-ins may run |
| Date shifting | Not implemented |
| Image, File, Calendar, lookup, currency, state/status columns | Excluded from beta writes |
| Cross-tenant authentication on GitHub Pages | Not supported; source and destination must each host the web resource |

The file may contain sensitive customer configuration data. Files are processed locally by the browser for download or import, but the live operations necessarily call the authenticated Dataverse API. Secure and purge downloaded files according to client policy. No Cloudflare beacon is embedded in this web resource.

**Mightora does not guarantee that a package will contain every record.** A paged export stops with an explicit error if the row cap is exceeded.

## Installation into the model-driven app

1. Import or create the `mgt_/migration.html` HTML web resource in an unmanaged development solution.
2. In the model-driven app designer, add a **Web resource** page named Configuration Migration Studio; position it under a Data Management section, alongside the existing Mightora tools.
3. Deploy to both a source and target development environment using managed ALM. Ensure required tables, fields and privileges exist.
4. Test with small controlled data, environment backup and plug-in execution monitoring before using broader scopes.

The project does not yet contain a validated Dataverse solution ZIP or a working direct-to-target connection from the static website. Microsoft-native schema/ZIP support and general relationship migration require separate implementation and testing.

## Mandatory next integration tests

- Table metadata retrieved with lower-privilege users
- Pagination and 2,000-row cap enforcement
- OData filters and records containing null/option/date/HTML strings
- Upsert created vs updated behaviour, ownership/defaults, custom validations
- Collision of matching natural keys with differing GUIDs
- Handling custom plug-ins and workflows firing on imported records
- Confirming the deployed target app displays the new tool page
- Import from a completely different environment and tenant
- Accessibility, mobile screens and browser file operations

**Important:** Do not use against production until these checks and a real Dataverse import/export test succeed.
