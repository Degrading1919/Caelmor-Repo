"""Refresh stored low-detail matrix/high-profile metrics after a regional art pass."""
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"
sys.path.insert(0,str(ROOT))

from caelmor_architecture.engine import generate,geometry_hash,validate
from caelmor_architecture.model import Settings


def source_hashes():
    import caelmor_architecture.engine as engine_module
    import caelmor_architecture.model as model_module
    import caelmor_architecture.facade as facade_module
    import caelmor_architecture.roof as roof_module
    import caelmor_architecture.world as world_module
    from caelmor_architecture import world_lowmark_thornfell,world_mire,world_emberholt
    paths=(engine_module.__file__,model_module.__file__,facade_module.__file__,roof_module.__file__,
           world_module.__file__,world_lowmark_thornfell.__file__,world_mire.__file__,
           world_emberholt.__file__,ROOT/"caelmor_architecture"/"blender_backend.py")
    return {Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}


def main():
    regions={arg.upper() for arg in sys.argv[1:]}
    valid={"LOWMARK","THORNFELL","MIRE","EMBERHOLT"}
    if not regions or not regions<=valid:
        raise SystemExit("Pass one or more valid region IDs")
    current_sources=source_hashes()
    changed=[]
    path=OUT/"world_matrix_240.json"
    rows=json.loads(path.read_text(encoding="utf-8"))
    for i,row in enumerate(rows):
        if row["region"] not in regions:continue
        settings=Settings(seed=row["seed"],function=row["function"],region=row["region"],
            wealth=row["wealth"],craftsmanship="STANDARD",detail="LOW",
            use_grammar=True,world_aware=True)
        started=time.perf_counter()
        plan,buffers=generate(settings)
        result=validate(plan,buffers)
        digest=geometry_hash(buffers)
        _plan2,buffers2=generate(settings)
        repeat=geometry_hash(buffers2)
        row.update(metrics=result,geometry_hash=digest,repeat_hash=repeat,
                   deterministic=digest==repeat,
                   generation_validation_seconds=round(time.perf_counter()-started,4),
                   source_hashes=current_sources)
        changed.append({"matrix_index":i,"region":row["region"],"function":row["function"],
                        "wealth":row["wealth"],"valid":result["valid"],"hash":digest})
    path.write_text(json.dumps(rows,indent=2),encoding="utf-8")

    selected_path=OUT/"world_selected_profiles.json"
    selected=json.loads(selected_path.read_text(encoding="utf-8"))
    high_changed=[]
    for i,row in enumerate(selected):
        if row["settings"]["region"] not in regions:continue
        settings=Settings(**row["settings"])
        plan,buffers=generate(settings)
        result=validate(plan,buffers)
        digest=geometry_hash(buffers)
        row["metrics"],row["hash"]=result,digest
        row["source_hashes"]=current_sources
        high_changed.append({"profile_index":i,"region":settings.region,
                             "wealth":settings.wealth,"mode":settings.geometry_mode,
                             "valid":result["valid"],"hash":digest})
    selected_path.write_text(json.dumps(selected,indent=2),encoding="utf-8")
    manifest={"regions":sorted(regions),"matrix_rows_updated":len(changed),
              "selected_profiles_updated":len(high_changed),"source_hashes":current_sources,
              "matrix":changed,"selected_profiles":high_changed}
    (OUT/"world_matrix_refresh_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    failed=[row for row in changed+high_changed if not row["valid"]]
    print(json.dumps({"matrix_rows_updated":len(changed),
        "selected_profiles_updated":len(high_changed),"invalid_count":len(failed),
        "source_hashes":current_sources},indent=2))
    if failed:raise SystemExit(1)


if __name__=="__main__":main()
