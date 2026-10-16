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

# Validate HTML inline JavaScript before allowing the build bot to commit.
# This catches broken regex literals or incomplete bundling before GitHub Pages.
from html.parser import HTMLParser
import subprocess
import tempfile

class InlineScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.collect = False
        self.blocks = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.collect = not any(key == "src" for key, _ in attrs)
            if self.collect:
                self.blocks.append("")
    def handle_data(self, data):
        if self.collect:
            self.blocks[-1] += data
    def handle_endtag(self, tag):
        if tag == "script":
            self.collect = False

for slug in slugs:
    doc = (DEPLOY / f"mgt_{slug}.html").read_text(encoding="utf-8")
    parser = InlineScripts()
    parser.feed(doc)
    with tempfile.TemporaryDirectory() as folder:
        for ix, code in enumerate(parser.blocks):
            if not code.strip():
                continue
            script_path = Path(folder) / f"inline-{ix}.js"
            script_path.write_text(code, encoding="utf-8")
            result = subprocess.run(["node", "--check", str(script_path)],
                                    capture_output=True, text=True)
            assert result.returncode == 0, f"{slug} inline script {ix}: {result.stderr}"

print("14 synced web resources, original upstream editions, no tracking, and bundle integrity passed.")
