"""Validate the real unmanaged solution source and packed ZIP without tenant access."""
from pathlib import Path
import sys, zipfile, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOLUTION=ROOT/"deployment/mightora-dataverse-tools"
WEB=SOLUTION/"WebResources"
MANIFEST=SOLUTION/"Other/Solution.xml"
SITEMAP=SOLUTION/"AppModuleSiteMaps/mightora_MightoraDataverseTools/AppModuleSiteMap.xml"
APP=SOLUTION/"AppModules/mightora_MightoraDataverseTools/AppModule.xml"
SLUGS=("trace","counter","environment","metadata","relationships","views","webresources",
       "fetchxml","fetchflow","rest","solutions","solution_explorer","migration","security","insights")

assert len(SLUGS)==15
sol=ET.parse(MANIFEST).getroot().find("SolutionManifest")
assert sol.findtext("UniqueName")=="MightoraDataverseTools"
assert sol.findtext("Managed")=="0"
assert sol.findtext("Version")=="1.0.0.4"
roots=sol.find("RootComponents")
names={x.attrib.get("schemaName") for x in roots.findall("RootComponent") if x.attrib.get("type")=="61"}
assert len(names)>=16 # fifteen tools plus existing image logo
assert set("mightora_mgt_"+s for s in SLUGS).issubset(names)
app=ET.parse(APP).getroot()
assert app.findtext("UniqueName")=="mightora_MightoraDataverseTools"
assert len(app.findall("./AppModuleRoleMaps/Role"))>=2
site=ET.parse(SITEMAP).getroot()
groups=site.findall("./SiteMap/Area/Group")
assert len(groups)==5, f"Expected five navigation groups, got {len(groups)}"
links=site.findall(".//SubArea")
assert len(links)==15
assert {x.attrib["Url"] for x in links}=={"$webresource:mightora_mgt_"+x for x in SLUGS}
assert all(x.attrib.get("AvailableOffline")=="false" for x in links)
ids=set()
for slug in SLUGS:
    name="mightora_mgt_"+slug
    xml=ET.parse(WEB/(name+".data.xml")).getroot()
    assert xml.findtext("Name")==name
    assert xml.findtext("WebResourceType")=="1"
    uid=xml.findtext("WebResourceId")
    assert uid not in ids and uid
    ids.add(uid)
    assert xml.findtext("FileName").startswith("/WebResources/"+name)
    assert (WEB/name).read_bytes()==(ROOT/"webresources"/("mgt_"+slug+".html")).read_bytes()
    html=(WEB/name).read_text(encoding="utf-8")
    assert len(html)>4000
    assert "beacon.min.js" not in html and "data-cf-beacon" not in html
    assert "Public Beta" in html
    if slug in ("trace", "metadata", "fetchxml", "counter", "solutions", "relationships"):
        assert "if(!demo&&!clientUrl)throw Error(" in html, slug + " must not silently fall back to mock data"
    if slug not in ("solution_explorer",):
        assert "ClientGlobalContext.js.aspx" in html
assert (WEB/"mightora_logo.data.xml").exists()
print("PASS: real unmanaged source, 15 resources, 5 groups, stable IDs, no telemetry.")

if len(sys.argv)>1:
    package=Path(sys.argv[1])
    with zipfile.ZipFile(package) as archive:
        entries=set(archive.namelist())
        assert "solution.xml" in entries and "customizations.xml" in entries
        manifest=ET.fromstring(archive.read("solution.xml")).find("SolutionManifest")
        assert manifest.findtext("Version")=="1.0.0.4"
        rc={x.attrib.get("schemaName") for x in manifest.findall("./RootComponents/RootComponent") if x.attrib.get("type")=="61"}
        assert {"mightora_mgt_"+s for s in SLUGS}.issubset(rc)
        assert sum(p.startswith("WebResources/mightora_mgt_") for p in entries)>=15
        customizations=archive.read("customizations.xml").decode("utf-8-sig")
        assert "mightora_MightoraDataverseTools" in customizations
        for slug in SLUGS:
            assert ("mightora_mgt_"+slug) in customizations, slug
    print("PASS: Microsoft-packed ZIP has 15 tool references and real solution/app components.")
