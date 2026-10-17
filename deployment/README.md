# Mightora Dataverse Tools — Real unmanaged app solution v1.0.0.3

The user exported the authentic **MightoraDataverseTools** unmanaged solution,
version 1.0.0.2, and unpacked it into this repository on 16 October 2026.

## Correct importable artifact

**[MightoraDataverseTools_1_0_0_3_unmanaged.zip](MightoraDataverseTools_1_0_0_3_unmanaged.zip)**

This ZIP is now packed from the genuine Microsoft-exported source using the
Microsoft Power Platform CLI. It includes solution.xml, customizations.xml,
the Mightora model-driven app, SiteMap, logo and 14 web resources.

**It has passed package structure checks, not a real-tenant import test.**
Do not import to production until the development environment confirms all
pages and user roles.

## Unpacked source

`mightora-dataverse-tools/` is now the authentic XML-based PAC-unpacked
solution source, *not* merely a folder of flat HTML files. The maintained
web resource sources live under `../webresources/` and the synchronization
script `../scripts/sync_unmanaged_solution.py` copies them into the exported
solution, preserving original ten web resource IDs.

Five groups are written to the SiteMap:

1. Diagnostics — Plugin Trace Explorer, Record Counter, Environment Diagnostics
2. Tables and data model — Metadata Explorer, Relationship Visualiser,
   View Query Inspector, Web Resource Browser
3. Queries and APIs — FetchXML Studio, FetchFlow, REST Studio
4. Solutions and migration — Solution Inspector, Solution Explorer,
   Configuration Migration Studio
5. Security — Security Role Catalogue

## Files NOT to import as Dataverse solutions

- `mightora-dataverse-tools.zip` and
  `mightora-dataverse-tools-webresources.zip` are separate HTML web-resource
  bundles retained for people manually importing individual tools.
- `MightoraDataverseTools_1_0_0_2.zip` is the original user-exported
  unmanaged solution retained as an immutable reference.

## Repack

The GitHub Action
[pack-unmanaged-solution.yml](../.github/workflows/pack-unmanaged-solution.yml)
runs the Microsoft PAC solution pack operation and validates the result. To
rebuild after changes to maintained HTML files, use that workflow or run:

    python scripts/sync_unmanaged_solution.py
    python tests/test_unmanaged_solution.py
    pac solution pack --folder deployment/mightora-dataverse-tools --zipfile deployment/MightoraDataverseTools_1_0_0_3_unmanaged.zip --packagetype Unmanaged
    python tests/test_unmanaged_solution.py deployment/MightoraDataverseTools_1_0_0_3_unmanaged.zip

## Actual integration testing

Import in a disposable **development** environment. Test the app navigation,
WhoAmI, metadata, FetchXML, solution export, and user permissions. REST Studio
and Configuration Migration Studio can modify real data: use disposable
records only and review plugins/flows. No environment login or token is
packaged. Cloudflare analytics runs on the public GitHub Pages catalogue
only, not inside any Dataverse web resource.

Documentation: ../docs/INSTALL.md.
