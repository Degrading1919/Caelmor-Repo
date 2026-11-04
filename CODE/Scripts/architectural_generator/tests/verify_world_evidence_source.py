"""Regenerate archived evidence settings and compare geometry to current source.

Run with the Blender-bundled Python after source-only changes that should leave
the existing clay frames unchanged:
  blender-python tests/verify_world_evidence_source.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"
sys.path.insert(0,str(ROOT))

from caelmor_architecture.engine import generate,geometry_hash,validate
from caelmor_architecture.model import Settings
from caelmor_architecture.profiles import TYPE_SPECS


def source_hashes():
    import caelmor_architecture.engine as engine_module
    import caelmor_architecture.model as model_module
    import caelmor_architecture.facade as facade_module
    import caelmor_architecture.roof as roof_module
    import caelmor_architecture.world as world_module
    from caelmor_architecture import world_lowmark_thornfell,world_mire,world_emberholt
    paths=(engine_module.__file__,model_module.__file__,facade_module.__file__,
           roof_module.__file__,world_module.__file__,world_lowmark_thornfell.__file__,
           world_mire.__file__,world_emberholt.__file__,
           ROOT/"caelmor_architecture"/"blender_backend.py",
           ROOT/"tests"/"render_world_evidence.py")
    return {Path(path).name:hashlib.sha256(Path(path).read_bytes()).hexdigest()
            for path in paths}


def check_settings(settings_data,expected_hash,where):
    settings=Settings(**settings_data)
    plan,buffers=generate(settings)
    report=validate(plan,buffers)
    actual=geometry_hash(buffers)
    return {"source":where,"valid":report["valid"],"geometry_hash":actual,
            "matches":actual==expected_hash,"errors":report["errors"][:4]}


def main():
    checks=[]
    frame_manifests=("world_first_four_clay_manifest.json",
                     "world_wealth_cottages_render_manifest.json",
                     "world_matrix_render_manifest.json",
                     "world_high_profiles_render_manifest.json")
    rendered_snapshots=[]
    for filename in frame_manifests:
        rows=json.loads((OUT/filename).read_text(encoding="utf-8"))
        for i,row in enumerate(rows):
            checks.append(check_settings(row["settings"],row["geometry_hash"],
                                         f"{filename}[{i}]"))
            if row.get("source_hashes"):
                rendered_snapshots.append(row["source_hashes"])
    # The 240-case matrix predates the last contextual guard change. Rebuild
    # its exact settings and require both validity and unchanged geometry.
    matrix=json.loads((OUT/"world_matrix_240.json").read_text(encoding="utf-8"))
    for i,row in enumerate(matrix):
        settings=Settings(seed=row["seed"],function=row["function"],region=row["region"],
            wealth=row["wealth"],craftsmanship="STANDARD",detail="LOW",
            use_grammar=True,world_aware=True)
        checks.append(check_settings(settings.__dict__,row["geometry_hash"],
                                     f"world_matrix_240.json[{i}]"))
    selected=json.loads((OUT/"world_selected_profiles.json").read_text(encoding="utf-8"))
    for i,row in enumerate(selected):
        checks.append(check_settings(row["settings"],row["hash"],
                                     f"world_selected_profiles.json[{i}]"))
    heroes=json.loads((OUT/'world_feature_heroes_manifest.json').read_text(encoding='utf-8'))
    for i,row in enumerate(heroes['records']):
        checks.append(check_settings(row['settings'],row['geometry_hash'],f'world_feature_heroes_manifest.json[{i}]'))
    stress=json.loads((OUT/'world_context_stress.json').read_text(encoding='utf-8'))
    for i,row in enumerate(stress['cases']):
        checks.append(check_settings(row['settings'],row['result']['geometry_hash'],f'world_context_stress.json[{i}]'))
    native=OUT/'world_installed_smithy.caelmor.json'
    if native.exists():
        row=json.loads(native.read_text(encoding='utf-8'))
        checks.append(check_settings(row['settings'],row['source_geometry_hash'],native.name))
    unique_render_snapshots=[]
    for snapshot in rendered_snapshots:
        if snapshot not in unique_render_snapshots:
            unique_render_snapshots.append(snapshot)
    final_hashes=source_hashes()
    mismatches=[row for row in checks if not row["valid"] or not row["matches"]]
    report={"verification":"regenerated geometry hashes against current source",
            "checked_settings":len(checks),"passed":len(checks)-len(mismatches),
            "mismatch_count":len(mismatches),"mismatches":mismatches[:12],
            "rendered_source_hash_snapshots":unique_render_snapshots,
            "final_source_hashes":final_hashes,
            "source_byte_hashes_equal":all(snapshot==final_hashes for snapshot in unique_render_snapshots),
            "blend_scene":json.loads((OUT/"world_four_region_cottages_manifest.json").read_text(encoding="utf-8"))}
    report["geometry_equivalent_to_final_source"]=not mismatches
    (OUT/"world_source_equivalence.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({"checked_settings":len(checks),"passed":len(checks)-len(mismatches),
        "mismatch_count":len(mismatches),"byte_hashes_equal":report["source_byte_hashes_equal"],
        "geometry_equivalent_to_final_source":report["geometry_equivalent_to_final_source"],
        "mismatches":mismatches[:8]},indent=2))
    if mismatches:
        raise SystemExit(1)


if __name__=="__main__":
    main()
