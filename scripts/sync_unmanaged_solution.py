#!/usr/bin/env python3
"""Synchronise all 14 maintained HTML files into the user's actual PAC-unpacked solution.

The source tree was exported by Power Apps on 2026-10-16. Preserve original
component IDs and publisher, app identity, app roles, and unrelated metadata.
Do not create a fake ZIP of web resources; use pac solution pack afterward.
"""
from pathlib import Path
from copy import deepcopy
import uuid
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/"deployment"/"mightora-dataverse-tools"
WEB=FOLDER/"WebResources"
SITEMAP=FOLDER/"AppModuleSiteMaps"/"mightora_MightoraDataverseTools"/"AppModuleSiteMap.xml"
SOLUTION=FOLDER/"Other"/"Solution.xml"
APP=FOLDER/"AppModules"/"mightora_MightoraDataverseTools"/"AppModule.xml"

GROUPS=[
    ("Diagnostics",("trace","counter","environment")),
    ("Tables and data model",("metadata","relationships","views","webresources")),
    ("Queries and APIs",("fetchxml","fetchflow","rest")),
    ("Solutions and migration",("solutions","solution_explorer","migration")),
    ("Security",("security",))
]
NAMES={
    "trace":"Plugin Trace Explorer",
    "counter":"Record Counter",
    "environment":"Environment Diagnostics",
    "metadata":"Metadata Explorer",
    "relationships":"Relationship Visualiser",
    "views":"View Query Inspector",
    "webresources":"Web Resource Browser",
    "fetchxml":"FetchXML Studio",
    "fetchflow":"FetchFlow Visual Query Builder",
    "rest":"REST Studio — Confirm Writes",
    "solutions":"Solution Inspector",
    "solution_explorer":"Solution Explorer",
    "migration":"Configuration Migration Studio — Writes Data",
    "security":"Security Role Catalogue"
}
SLUGS=tuple(s for _,slugs in GROUPS for s in slugs)
assert len(SLUGS)==14 and len(set(SLUGS))==14
assert all(p.exists() for p in (WEB,SITEMAP,SOLUTION,APP)), "Not a Power Apps unpacked solution"
ET.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")
# Match the Microsoft-managed resource IDs (never regenerate those).
original_metadata=WEB/"mightora_mgt_trace.data.xml"
template=ET.parse(original_metadata).getroot()
new_resources=[]
existing_names=set()
for slug in SLUGS:
    resource=f"mightora_mgt_{slug}"
    source=ROOT/"webresources"/f"mgt_{slug}.html"
    if not source.is_file():
        raise RuntimeError(f"Source HTML missing: {source}")
    html=source.read_text(encoding="utf-8")
    if not html.lstrip().lower().startswith("<!doctype html") or len(html)<4000:
        raise RuntimeError(f"Invalid HTML web resource: {source}")
    if "beacon.min.js" in html or "data-cf-beacon" in html:
        raise RuntimeError(f"External analytics are forbidden inside tenant resource {slug}")
    if slug!="solution_explorer" and "ClientGlobalContext.js.aspx" not in html:
        raise RuntimeError(f"Platform global context missing in {slug}")
    # Keep unchanged GUIDs for the 10 resources in the original export.
    target=WEB/resource
    target.write_text(html,encoding="utf-8")
    metadata=WEB/(resource+".data.xml")
    if metadata.exists():
        parsed=ET.parse(metadata).getroot()
        if parsed.findtext("Name")!=resource:
            raise RuntimeError(f"Unexpected existing resource name {metadata}")
        existing_names.add(slug)
    else:
        # IDs are stable across rebuilds, not generated anew on each CI run.
        component=deepcopy(template)
        guid=uuid.uuid5(uuid.NAMESPACE_URL,"https://dataverse-tools.mightora.io/"+resource)
        component.find("WebResourceId").text="{"+str(guid)+"}"
        component.find("Name").text=resource
        component.find("DisplayName").text=NAMES[slug]
        component.find("WebResourceType").text="1"
        component.find("FileName").text="/WebResources/"+resource+str(guid).upper()
        component.find("IntroducedVersion").text="1.0.0.3"
        ET.ElementTree(component).write(metadata,encoding="utf-8",xml_declaration=True)
        new_resources.append((slug,str(guid)))
    if not metadata.is_file():
        raise RuntimeError("Metadata not generated for "+resource)

tree=ET.parse(SOLUTION)
manifest=tree.getroot().find("SolutionManifest")
assert manifest is not None
assert manifest.findtext("UniqueName")=="MightoraDataverseTools"
assert manifest.findtext("Managed")=="0"
version=manifest.find("Version")
version.text="1.0.0.3"
roots=manifest.find("RootComponents")
assert roots is not None
for slug in SLUGS:
    name="mightora_mgt_"+slug
    if not any(e.attrib.get("type")=="61" and e.attrib.get("schemaName")==name for e in roots.findall("RootComponent")):
        ET.SubElement(roots,"RootComponent",{"type":"61","schemaName":name,"behavior":"0"})
tree.write(SOLUTION,encoding="utf-8",xml_declaration=True)

# Preserve the real exported app and sitemap IDs. Replace only the
# navigational groups so all app subareas reference existing web resources.
tree=ET.parse(SITEMAP)
root=tree.getroot()
area=root.find("./SiteMap/Area")
if area is None:
    raise RuntimeError("Expected exported SiteMap area")
for node in list(area):
    if node.tag=="Group":
        area.remove(node)
for index,(title,slugs) in enumerate(GROUPS,1):
    group=ET.SubElement(area,"Group",{"Id":f"mightora_group_{index}","IsProfile":"false"})
    titles=ET.SubElement(group,"Titles")
    ET.SubElement(titles,"Title",{"LCID":"1033","Title":title})
    for slug in slugs:
        name="mightora_mgt_"+slug
        sub=ET.SubElement(group,"SubArea",{
            "Id":f"mightora_tool_{slug}",
            "Url":"$webresource:"+name,
            "Client":"All,Outlook,OutlookLaptopClient,OutlookWorkstationClient,Web",
            "AvailableOffline":"false","PassParams":"false",
            "Sku":"All,OnPremise,Live,SPLA"
        })
        titles=ET.SubElement(sub,"Titles")
        ET.SubElement(titles,"Title",{"LCID":"1033","Title":NAMES[slug]})
root.find("EnableCollapsibleGroups").text="True"
tree.write(SITEMAP,encoding="utf-8",xml_declaration=True)

app=ET.parse(APP)
root=app.getroot()
assert root.findtext("UniqueName")=="mightora_MightoraDataverseTools"
# Do not replace existing app module ID, roles, logo or app settings.
description=root.find("./Descriptions/Description")
if description is not None:
    description.set("description","Mightora Dataverse Tools — 14 developer utilities, grouped by capability. Public beta: these tools use real Dataverse API permissions and may expose data. REST Studio and Configuration Migration can modify records when authorised. https://dataverse-tools.mightora.io/")
app.write(APP,encoding="utf-8",xml_declaration=True)

# Fail hard on stale references before the official Microsoft packer starts.
site=ET.parse(SITEMAP).getroot()
urls=[e.attrib["Url"] for e in site.findall(".//SubArea")]
expected={"$webresource:mightora_mgt_"+slug for slug in SLUGS}
assert set(urls)==expected and len(urls)==14, (urls,expected)
root=ET.parse(SOLUTION).getroot()
names={e.attrib.get("schemaName") for e in root.findall("./SolutionManifest/RootComponents/RootComponent") if e.attrib.get("type")=="61"}
assert all("mightora_mgt_"+slug in names for slug in SLUGS)
assert all((WEB/("mightora_mgt_"+slug+".data.xml")).exists() for slug in SLUGS)

print(f"Updated true unmanaged solution: 14 real HTML web resources, {len(GROUPS)} grouped sections.")
print("Original ten metadata IDs retained; new resource IDs:",new_resources)
print("Version updated to 1.0.0.3; preserved app identity, publisher and roles.")
