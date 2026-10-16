"""Static security and behaviour guards for Configuration Migration Studio."""
from pathlib import Path
html=(Path(__file__).resolve().parents[1]/"dist"/"webresources"/"mgt_migration.html").read_text()
for required in ("PUBLIC BETA", "parsePackage", "validateImport", "performImport", "confirm-host", "confirm-backup", "confirm-impact", "confirm-lookup", "sourceHost", "clientUrl", "entitySetName", "api/data/v9.2/", "PATCH", "odata.maxpagesize=200", "@odata.nextLink", "Public Beta"):
    assert required in html, required
assert "static.cloudflareinsights.com" not in html
assert "beacon.min.js" not in html
assert "DisablePlugin" not in html
assert "Microsoft Configuration Migration ZIP" in html
assert "same-origin" in html
print("Configuration Migration Studio static safety and beta checks passed.")
