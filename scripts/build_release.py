#!/usr/bin/env python3
"""Build GitHub Pages distribution for Mightora Dataverse Tools."""
from pathlib import Path
import shutil
import zipfile

root = Path(__file__).resolve().parents[1]
dist = root / "dist"
downloads = dist / "downloads"
previews = dist / "webresources"
for folder in (dist, downloads, previews):
    folder.mkdir(parents=True, exist_ok=True)
for filename in ("index.html", "CNAME", "robots.txt", "sitemap.xml"):
    shutil.copy2(root / filename, dist / filename)
(dist / ".nojekyll").touch()

tools = ("trace", "metadata", "fetchxml", "counter", "solutions", "relationships", "webresources", "views", "security", "environment", "migration", "rest", "fetchflow", "solution_explorer")
for slug in tools:
    source = root / "webresources" / f"mgt_{slug}.html"
    content = source.read_text(encoding="utf-8")
    if "ClientGlobalContext.js.aspx" not in content or len(content) < 2000:
        raise ValueError(f"Missing/invalid standalone Dataverse tool: {slug}")
    shutil.copy2(source, downloads / source.name)
    shutil.copy2(source, previews / source.name)

with zipfile.ZipFile(downloads / "mightora-dataverse-tools.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for slug in tools:
        source = root / "webresources" / f"mgt_{slug}.html"
        archive.write(source, source.name)
    archive.write(root / "README.md", "README.md")
    archive.write(root / "LICENSE", "LICENSE")
print(f"Built site with {len(tools)} HTML resources and toolkit ZIP.")
