#!/usr/bin/env python3
"""Vendor original Mightora Dataverse editions, fail closed on incomplete upstream builds."""
from pathlib import Path
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / "deployment" / "mightora-dataverse-tools"
RESOURCES = ROOT / "webresources"
SOURCES = {
    "rest": ROOT / "upstream/rest/dist/dataverse/rest.html",
    "fetchflow": ROOT / "upstream/fetchflow/dist/dataverse/mightora_fetchflow_builder.html",
    "solution_explorer": ROOT / "upstream/solution-explorer/dist/dataverse/solution-explorer.html",
}
PINNED = {
    "rest": "66d0b5cd45ef494dfadee24454fb4bb373569149",
    "fetchflow": "000bb5868f7bf8c5731af09eb01e1bcf1f54e1e4",
    "solution_explorer": "7157e2d37445ae35e93a36d6d5a8f2b4393276fc",
}
EXISTING = ("trace", "metadata", "fetchxml", "counter", "solutions",
            "relationships", "webresources", "views", "security", "environment", "migration")
ALL = EXISTING + tuple(SOURCES)
DEPLOY.mkdir(parents=True, exist_ok=True)
RESOURCES.mkdir(parents=True, exist_ok=True)

for slug, source in SOURCES.items():
    if not source.is_file():
        raise SystemExit(f"Upstream build missing {source}")
    content = source.read_text(encoding="utf-8")
    if len(content) < 15000 or "<html" not in content.lower() or "api/data/v9.2/" not in content.lower():
        raise SystemExit(f"Incomplete Dataverse web resource: {slug}")
    if "beacon.min.js" in content or "data-cf-beacon" in content:
        raise SystemExit(f"Unexpected telemetry in Dataverse resource: {slug}")
    if slug in ("rest", "fetchflow") and "ClientGlobalContext.js.aspx" not in content:
        raise SystemExit(f"Missing global context helper: {slug}")
    for path in (RESOURCES / f"mgt_{slug}.html", DEPLOY / f"mgt_{slug}.html"):
        path.write_text(content, encoding="utf-8")
    print(f"Vendored {slug} - {len(content)} characters")

for slug in EXISTING:
    source = RESOURCES / f"mgt_{slug}.html"
    if not source.exists():
        raise SystemExit(f"Missing source resource {source}")
    shutil.copyfile(source, DEPLOY / source.name)

readme = """# Mightora Dataverse Tools - Web Resource Distribution Bundle

THIS ZIP IS NOT A DATAVERSE SOLUTION ZIP.

This directory has fourteen flat HTML web resources. To create a true
Dataverse solution with pac solution pack, start with a Dataverse-exported
unmanaged solution containing a solution manifest, app definition, and the
proper root components. Do not import this ZIP in the Solutions importer.

Create HTML web resources in a development solution using names like
mgt_trace.html, mgt_rest.html, mgt_fetchflow.html,
mgt_solution_explorer.html. Publish and add the web resources as
model-driven app pages, then export and unpack that actual solution.

REST Studio and Configuration Migration Studio can modify Dataverse data.
Restrict their access to authorized users. All tools are public beta.

Source: https://github.com/mightora/dataverse-toolkit.mightora.io
"""
(DEPLOY / "README.md").write_text(readme, encoding="utf-8")
if not (DEPLOY / "LICENSE").exists():
    shutil.copy2(ROOT / "LICENSE", DEPLOY / "LICENSE")
metadata = {
    "kind": "web-resource-bundle-not-Dataverse-solution",
    "version": "0.4-beta",
    "tools": [f"mgt_{slug}.html" for slug in ALL],
    "upstream_commits": PINNED,
    "dataverse_solution_importable": False,
}
(DEPLOY / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
parts = [DEPLOY / f"mgt_{slug}.html" for slug in ALL]
parts += [DEPLOY / "README.md", DEPLOY / "LICENSE", DEPLOY / "manifest.json"]
for dest in (ROOT / "deployment/mightora-dataverse-tools.zip",
             ROOT / "deployment/mightora-dataverse-tools-webresources.zip"):
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=7) as archive:
        for file in parts:
            archive.write(file, file.name)
    print(f"Packaged {dest.relative_to(ROOT)} ({dest.stat().st_size:,} bytes)")
print(f"Synced and packaged {len(ALL)} HTML web resources.")
