"""Refresh only selected regions in saved world clay evidence manifests.

Example after a narrowly scoped regional art pass:
  blender --background --python tests/rerender_world_regions.py -- --regions LOWMARK THORNFELL
All other regions retain their original image and per-frame source hash.
"""
import json
import sys
import importlib.util
from pathlib import Path

import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from caelmor_architecture.model import Settings
spec=importlib.util.spec_from_file_location("world_evidence_renderer",ROOT/"tests"/"render_world_evidence.py")
render=importlib.util.module_from_spec(spec)
spec.loader.exec_module(render)


def _refresh_manifest(filename,region_set):
    path=render.OUT/filename
    records=json.loads(path.read_text(encoding="utf-8"))
    changed=[]
    for row in records:
        if row["settings"]["region"] not in region_set:
            continue
        settings=Settings(**row["settings"])
        scene,camera=render._reset_scene()
        label=row.get("label") or f"{settings.region} · {settings.function} · {settings.wealth}"
        refreshed=render._render_one(scene,camera,settings,
            render.FRAMES/row["image"],label)
        if row.get("blind_id"):
            refreshed["blind_id"]=row["blind_id"]
        row.clear(); row.update(refreshed)
        changed.append({"manifest":filename,"image":row["image"],
                        "region":settings.region,"function":settings.function,
                        "wealth":settings.wealth,"geometry_hash":row["geometry_hash"]})
    path.write_text(json.dumps(records,indent=2),encoding="utf-8")
    return changed


def main():
    args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    if "--regions" not in args:
        raise SystemExit("Pass --regions followed by one or more region IDs")
    start=args.index("--regions")+1
    regions={v.upper() for v in args[start:] if not v.startswith("--")}
    valid={"LOWMARK","THORNFELL","MIRE","EMBERHOLT"}
    if not regions or not regions<=valid:
        raise SystemExit("Unsupported or empty region selection: "+repr(regions))
    changed=[]
    for filename in ("world_first_four_clay_manifest.json",
                     "world_wealth_cottages_render_manifest.json",
                     "world_matrix_render_manifest.json",
                     "world_high_profiles_render_manifest.json"):
        changed.extend(_refresh_manifest(filename,regions))
    render._save_editable_cottage_scene([
        Settings(seed=91,function="COTTAGE",region=region,wealth="MODEST",
                 detail="LOW",use_grammar=True,world_aware=True)
        for region in ("LOWMARK","THORNFELL","MIRE","EMBERHOLT")])
    result={"refreshed_regions":sorted(regions),"frame_count":len(changed),
            "frames":changed,"blender_version":bpy.app.version_string,
            "source_hashes":render._source_hashes()}
    (render.OUT/"world_selective_rerender_manifest.json").write_text(
        json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"refreshed_regions":sorted(regions),"frame_count":len(changed),
                      "source_hashes":result["source_hashes"]},indent=2))


if __name__=="__main__":
    main()
