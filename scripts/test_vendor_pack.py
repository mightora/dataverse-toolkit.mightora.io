"""Regression tests for the 14-file Dataverse web-resource distribution bundle."""
from pathlib import Path
import json, zipfile, re

ROOT=Path(__file__).resolve().parents[1]
DEPLOY=ROOT/"deployment"/"mightora-dataverse-tools"
slugs=("trace","metadata","fetchxml","counter","solutions","relationships",
       "webresources","views","security","environment","migration",
       "rest","fetchflow","solution_explorer")
assert len(slugs)==14
for slug in slugs:
    name=f"mgt_{slug}.html"
    deployed=DEPLOY/name
    upstream=ROOT/"webresources"/name
    assert deployed.is_file() and upstream.is_file(), name
    assert deployed.read_bytes()==upstream.read_bytes(), "Source/deployment drift: "+name
    html=deployed.read_text(encoding="utf-8")
    assert "<html" in html.lower()
    assert "beacon.min.js" not in html and "data-cf-beacon" not in html
    assert "ClientGlobalContext.js.aspx" in html or slug=="solution_explorer", name

metadata=json.loads((DEPLOY/"manifest.json").read_text(encoding="utf-8"))
assert len(metadata["tools"])==14
assert metadata["dataverse_solution_importable"] is False

for archive in (ROOT/"deployment/mightora-dataverse-tools.zip",
                ROOT/"deployment/mightora-dataverse-tools-webresources.zip"):
    with zipfile.ZipFile(archive) as bundle:
        members=set(bundle.namelist())
        assert all(f"mgt_{slug}.html" in members for slug in slugs)
        assert "README.md" in members and "manifest.json" in members
        assert "Other/Solution.xml" not in members, "Not a Dataverse solution"
        for slug in slugs:
            filename=f"mgt_{slug}.html"
            assert bundle.read(filename)==(DEPLOY/filename).read_bytes()
print("14 synced web resources, original upstream editions, no tracking, and bundle integrity passed.")
