from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
dist = root / "dist"
assert (dist / "index.html").exists()
assert (dist / "CNAME").read_text().strip() == "dataverse-tools.mightora.io"
index = (dist / "index.html").read_text()
for required in ("<mightora-header", "<mightora-author", "<mightora-footer", "https://dataverse-tools.mightora.io"):
    assert required in index, required
with zipfile.ZipFile(dist / "downloads" / "mightora-dataverse-tools.zip") as archive:
    for slug in ("trace", "metadata", "fetchxml", "counter", "solutions", "relationships", "webresources", "views", "security", "environment"):
        name = f"mgt_{slug}.html"
        assert name in archive.namelist()
        assert (dist / "downloads" / name).read_bytes() == archive.read(name)
        assert (dist / "webresources" / name).exists()
        assert name in index

# Branding and trust requirements: genuine evidence links and correct section order.
assert index.index("<mightora-author>") < index.index('class="quality-badges"') < index.index("<mightora-footer>")
assert index.count("<mightora-footer>") == 1
assert index.count("badge.svg?branch=main") == 2
for required in (
    "class=\"footer-bottom\"",
    "class=\"author-avatar\"",
    "class=\"author-blog-logo\"",
    "class=\"quality-badge-list\"",
    "footer.yaml",
    "raw.replace",
    "actions/workflows/pages.yml",
    "actions/workflows/codeql.yml",
    "blob/main/LICENSE",
    "img.shields.io/badge/source-GitHub",
):
    assert required in index, f"Missing footer or badge requirement: {required}"
assert index.index("js-yaml") < index.index("components.js"), "YAML parser must load first"
assert index.index("Mightora shared-footer compatibility") < index.index("components.js"), "Footer YAML normalisation must initialise before shared components"

assert "Public Beta" in index
assert "static.cloudflareinsights.com/beacon.min.js" in index
print("Build verification passed: ten HTML resources, ZIP, domain, and brand components.")
