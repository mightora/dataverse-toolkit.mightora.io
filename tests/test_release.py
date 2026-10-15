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
    for slug in ("trace", "metadata", "fetchxml", "counter", "solutions", "relationships"):
        name = f"mgt_{slug}.html"
        assert name in archive.namelist()
        assert (dist / "downloads" / name).read_bytes() == archive.read(name)
        assert (dist / "webresources" / name).exists()
        assert name in index
print("Build verification passed: six HTML resources, ZIP, domain, and brand components.")
