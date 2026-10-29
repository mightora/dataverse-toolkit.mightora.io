"""Ensure all fourteen beta HTML web resources parse and have no third-party tracking."""
from pathlib import Path
from html.parser import HTMLParser
import subprocess, tempfile

root=Path(__file__).resolve().parents[1]
resources=sorted((root/'dist'/'webresources').glob('mgt_*.html'))
assert len(resources)==15, f'Expected 15 resources, got {len(resources)}'
class Inline(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside=False
        self.blocks=[]
    def handle_starttag(self,tag,attrs):
        if tag=='script':
            self.inside=not any(key=='src' for key,_ in attrs)
            if self.inside:self.blocks.append('')
    def handle_data(self,data):
        if self.inside:self.blocks[-1]+=data
    def handle_endtag(self,tag):
        if tag=='script':self.inside=False

for resource in resources:
    html=resource.read_text(encoding='utf-8')
    assert 'Public Beta' in html
    assert 'beacon.min.js' not in html and 'data-cf-beacon' not in html
    assert 'ClientGlobalContext.js.aspx' in html or resource.name == 'mgt_solution_explorer.html'
    parser=Inline()
    parser.feed(html)
    with tempfile.TemporaryDirectory() as d:
        for i,script in enumerate(parser.blocks):
            if not script.strip():continue
            path=Path(d)/f'inline-{i}.js'
            path.write_text(script,encoding='utf-8')
            res=subprocess.run(['node','--check',str(path)],capture_output=True,text=True)
            assert res.returncode==0, f'{resource.name}: {res.stderr}'
print('All 15 beta web resources passed script syntax and telemetry checks.')
