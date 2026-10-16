# Deployment source and web-resource bundle (Public Beta v0.4)

This repository has two **different** concepts:

- deployment/mightora-dataverse-tools/ — currently a folder containing
  fourteen flat HTML resources, README, licence and a JSON manifest.
- deployment/mightora-dataverse-tools.zip — a ZIP of those files.

**Neither is currently a PAC-unpacked Dataverse unmanaged solution.**
The uploaded archive was inspected and did not contain Other/Solution.xml,
Other/Customizations.xml, a Dataverse app module or root component metadata.
A ZIP of HTML files cannot be imported as a Power Apps solution, even if its
contents were compressed using standard packaging tools.

The web resource content itself is now synchronized with the maintained
source files, including REST, FetchFlow and Solution Explorer from pinned
upstream Mightora repositories. The root-level Microsoft helper path has
been fixed in the original eleven tools.

The declarative app-navigation.json now describes fourteen intended
app pages using flat names such as mgt_rest.html, but it is **not a
deployed app module**.

## How to produce a real unmanaged solution

1. Import these HTML resources one-by-one into an unmanaged development
   solution using Power Apps, or update the existing solution web resources.
2. Add the three new pages to the actual model-driven app navigation and
   test each tool in that environment.
3. Export the genuine unmanaged solution ZIP from Dataverse.
4. Run the Microsoft PAC CLI:
   pac solution unpack --zipfile exported.zip --folder real-unpacked --packagetype Unmanaged
5. Verify Other/Solution.xml and Other/Customizations.xml (or an approved
   native Dataverse YAML solution structure).
6. Future updates can then use:
   pac solution pack --folder real-unpacked --zipfile updated-unmanaged.zip --packagetype Unmanaged

See docs/INSTALL.md and docs/DATAVERSE_CONNECTIONS.md for setup and
read-only API troubleshooting.

The REST and Configuration Migration tools can write records. Gate
environment access through genuine Dataverse security permissions.
No Cloudflare beacon is present in any packaged HTML web resource.
