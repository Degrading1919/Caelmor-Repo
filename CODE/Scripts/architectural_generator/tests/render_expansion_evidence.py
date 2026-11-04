"""Render bounded comparison evidence for the expanded exterior grammar.

Run ``blender --background --python tests/render_expansion_evidence.py``.
Use ``--hero-only`` for the initial four-region cottage review. Outputs are
compressed editable Blender scenes, labelled contact sheets, and a JSON record
of exact settings, source hashes, geometry counts and measured timings.
"""

import hashlib
import json
import sys
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import caelmor_architecture
import caelmor_architecture.model as model_module
from caelmor_architecture.blender_backend import TAG, build
from caelmor_architecture.engine import compare_geometry_modes, generate, validate
from caelmor_architecture.model import Settings
from caelmor_architecture.profiles import REGIONS, TYPE_SPECS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
FRAMES = OUT / "_expansion_frames"
WIDTH = HEIGHT = 420


def camera_to(camera, position, target):
    camera.location = position
    camera.rotation_euler = (Vector(target)-camera.location).to_track_quat("-Z", "Y").to_euler()


def initialize():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 16
    scene.render.resolution_x = scene.render.resolution_y = WIDTH
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = .3
    scene.world = bpy.data.worlds.new("Caelmor Expansion Evidence")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (.24,.23,.21,1)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = .55
    bpy.ops.mesh.primitive_plane_add(size=1000, location=(0, 0, -.08))
    ground = bpy.context.object
    ground.name = "Neutral Evidence Ground"
    mat = bpy.data.materials.new("Evidence Ground")
    mat.diffuse_color = (.16,.17,.15,1)
    ground.data.materials.append(mat)
    bpy.ops.object.light_add(type="SUN", location=(0,-18,24))
    sun = bpy.context.object; sun.name = "Evidence Sun"; sun.data.energy = 2.5
    sun.data.angle = .18; sun.rotation_euler = (.44,-.35,-.44)
    bpy.ops.object.light_add(type="AREA", location=(0,-12,10))
    fill = bpy.context.object; fill.name = "Evidence Fill"
    fill.data.energy = 1200; fill.data.shape = "DISK"; fill.data.size = 16
    bpy.ops.object.camera_add()
    camera = bpy.context.object; camera.name = "Evidence Camera"
    camera.data.type = "ORTHO"; scene.camera = camera
    return scene, camera, sun, fill, ground


def configurations(hero_only=False):
    rows = []
    for region, spec in REGIONS.items():
        rows.append((f"Region · {region}", Settings(function="COTTAGE", use_grammar=True,
            region=region, context=spec.default_context, wealth="ESTABLISHED",
            craftsmanship="STANDARD", maintenance=.7, age=35, detail="MEDIUM", seed=17)))
    for wealth in ("MODEST", "ESTABLISHED", "AFFLUENT"):
        rows.append((f"Lowmark · {wealth}", Settings(function="COTTAGE", use_grammar=True,
            region="LOWMARK", context="RURAL", wealth=wealth, age=100,
            maintenance=.7, detail="MEDIUM", seed=41)))
    for label, upkeep in (("Maintained", 1.0), ("Neglected", 0.0)):
        rows.append((f"Wear · {label}", Settings(function="COTTAGE", use_grammar=True,
            region="LOWMARK", context="RURAL", wealth="ESTABLISHED", age=160,
            maintenance=upkeep, detail="MEDIUM", seed=41)))
    if hero_only:
        return rows[:9]
    category_region = {
        "RESIDENTIAL":"LOWMARK", "AGRICULTURAL":"LOWMARK",
        "COMMERCIAL":"EMBERHOLT", "INDUSTRIAL":"EMBERHOLT", "CIVIC":"EMBERHOLT",
        "DEFENSIVE":"THORNFELL", "WATERFRONT":"MIRE",
    }
    for index, (function, spec) in enumerate(TYPE_SPECS.items()):
        region = category_region.get(spec.building_category, "LOWMARK")
        rows.append((f"Type · {function}", Settings(function=function, use_grammar=True,
            region=region, context=REGIONS[region].default_context, wealth="ESTABLISHED",
            detail="LOW", seed=100+index)))
    return rows


def source_hashes():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((ROOT / "caelmor_architecture").glob("*.py"))}


def loaded_modules():
    return {module.__name__:{"file":str(Path(module.__file__).resolve()),
            "sha256":hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()}
            for module in (caelmor_architecture,model_module)}


def build_rows(rows):
    output = []
    region_index=0
    for label, settings in rows:
        started = time.perf_counter()
        collection, metrics = build(settings)
        blender_seconds = time.perf_counter()-started
        pure_started = time.perf_counter()
        plan, buffers = generate(settings)
        validation = validate(plan, buffers)
        pure_seconds = time.perf_counter()-pure_started
        if not validation["valid"]:
            raise RuntimeError(f"{label} failed validation: {validation['errors']}")
        if collection.get("caelm_geometry_hash") != validation["geometry_hash"]:
            raise RuntimeError(f"{label} Blender build hash does not match independent pure geometry")
        offset=Vector((0.0,0.0,0.0))
        if label.startswith("Region · "):
            offset=Vector(((region_index%2)*30.0,(region_index//2)*25.0,0.0))
            anchor=next(obj for obj in collection.objects if obj.get("caelm_anchor"))
            anchor.location+=offset
            region_index+=1
        elif label.startswith("Lowmark · "):
            wealth_index=sum(1 for row in output if row["label"].startswith("Lowmark · "))
            offset=Vector((wealth_index*15.0,52.0,0.0))
            next(obj for obj in collection.objects if obj.get("caelm_anchor")).location+=offset
        elif label.startswith("Wear · "):
            wear_index=sum(1 for row in output if row["label"].startswith("Wear · "))
            offset=Vector((wear_index*15.0,73.0,0.0))
            next(obj for obj in collection.objects if obj.get("caelm_anchor")).location+=offset
        elif label.startswith("Type · "):
            type_index=sum(1 for row in output if row["label"].startswith("Type · "))
            offset=Vector(((type_index%5)*24.0,105.0+(type_index//5)*24.0,0.0))
            next(obj for obj in collection.objects if obj.get("caelm_anchor")).location+=offset
        objects = [o for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")]
        expected_materials=Counter(buffer.material for buffer in buffers)
        actual_materials=Counter(str(obj.get("caelm_material")) for obj in objects)
        if expected_materials!=actual_materials:
            raise RuntimeError(f"{label} Blender/pure material counts differ: "
                               f"expected={expected_materials}, actual={actual_materials}")
        materials_by_key={}
        for obj in objects:
            material=obj.data.materials[0] if obj.data.materials else None
            if material is not None:
                materials_by_key[str(obj.get("caelm_material"))]=tuple(
                    round(float(v),5) for v in material.diffuse_color)
        triangles = sum(len(poly.vertices)-2 for o in objects for poly in o.data.polygons)
        output.append({"label":label, "settings":settings, "plan":plan,
            "collection":collection, "metrics":metrics, "objects":objects,
            "offset":tuple(offset),
            "expected_material_counts":dict(sorted(expected_materials.items())),
            "actual_material_counts":dict(sorted(actual_materials.items())),
            "geometry_hash_matches_pure_validation":True,
            "materials_by_key":materials_by_key,
            "validation":validation, "triangles":triangles,
            "build_seconds":round(blender_seconds,4), "pure_seconds":round(pure_seconds,4)})
    return output


def build_mode_rows(base_settings):
    output=[]
    for index,mode in enumerate(("SOLID","EFFICIENT")):
        settings=Settings(**{**asdict(base_settings),"geometry_mode":mode})
        started=time.perf_counter()
        collection,metrics=build(settings)
        build_seconds=time.perf_counter()-started
        pure_started=time.perf_counter()
        plan,buffers=generate(settings)
        validation=validate(plan,buffers)
        pure_seconds=time.perf_counter()-pure_started
        if not validation["valid"]:
            raise RuntimeError(f"{mode} mode render fixture failed: {validation['errors']}")
        if collection.get("caelm_geometry_hash") != validation["geometry_hash"]:
            raise RuntimeError(f"{mode} mode Blender build hash does not match independent pure geometry")
        offset=Vector((index*24.0,170.0,0.0))
        next(obj for obj in collection.objects if obj.get("caelm_anchor")).location+=offset
        objects=[obj for obj in collection.objects if obj.get(TAG) and not obj.get("caelm_collider")]
        expected=Counter(buffer.material for buffer in buffers)
        actual=Counter(str(obj.get("caelm_material")) for obj in objects)
        if expected!=actual:
            raise RuntimeError(f"{mode} mode Blender/pure material counts differ: "
                               f"expected={expected}, actual={actual}")
        output.append({"label":f"Geometry mode · {mode}","mode":mode,"settings":settings,
            "plan":plan,"collection":collection,"metrics":metrics,"objects":objects,
            "offset":tuple(offset),"validation":validation,
            "expected_material_counts":dict(sorted(expected.items())),
            "actual_material_counts":dict(sorted(actual.items())),
            "triangles":sum(len(poly.vertices)-2 for obj in objects for poly in obj.data.polygons),
            "build_seconds":round(build_seconds,4),"pure_seconds":round(pure_seconds,4)})
    return output


def frame_for(scene, camera, sun, fill, ground, row, path, resolution=WIDTH, scale_factor=1.55):
    for obj in row["objects"]:
        obj.hide_render = False
    corners=[obj.matrix_world @ Vector(corner) for obj in row["objects"] for corner in obj.bound_box]
    lo=Vector(tuple(min(point[axis] for point in corners) for axis in range(3)))
    hi=Vector(tuple(max(point[axis] for point in corners) for axis in range(3)))
    center=(lo+hi)*.5
    direction=Vector((-1,-1,.58)).normalized()
    distance=max((hi-lo).length*1.5,8.0)
    camera_to(camera, center+direction*distance, center)
    rotation=camera.matrix_world.to_3x3()
    right=rotation @ Vector((1,0,0)); up=rotation @ Vector((0,1,0))
    projected_right=[(point-center).dot(right) for point in corners]
    projected_up=[(point-center).dot(up) for point in corners]
    projected_span=max(max(projected_right)-min(projected_right),
                       max(projected_up)-min(projected_up))
    camera.data.ortho_scale=projected_span*scale_factor+2
    ground.location=(center.x,center.y,-.08)
    sun.location=center+Vector((-distance*.8,-distance*.6,distance*1.2))
    fill.location=center+Vector((-distance*.55,-distance*.7,distance*.9))
    fill.rotation_euler=(center-fill.location).to_track_quat("-Z","Y").to_euler()
    fill.data.energy=1200; fill.data.size=max(row["metrics"]["width"],row["metrics"]["depth"])*1.4
    scene.render.resolution_x=scene.render.resolution_y=resolution
    scene.render.filepath=str(path)
    start=time.perf_counter(); bpy.ops.render.render(write_still=True)
    return round(time.perf_counter()-start,3)


def render_group(scene,camera,sun,fill,ground,all_rows,group_rows,center,path,
                 ortho,resolution=(1600,1100)):
    for row in all_rows:
        visible=any(row is candidate for candidate in group_rows)
        for obj in row["objects"]: obj.hide_render=not visible
    center=Vector(center)
    camera_to(camera,center+Vector((15,-57,43)),center)
    camera.data.ortho_scale=ortho
    ground.location=(center.x,center.y,-.08)
    sun.location=center+Vector((-35,-42,62))
    fill.location=center+Vector((-25,-38,48))
    fill.rotation_euler=(center-fill.location).to_track_quat("-Z","Y").to_euler()
    fill.data.energy=1200; fill.data.size=28
    scene.render.resolution_x,scene.render.resolution_y=resolution
    scene.render.filepath=str(path)
    started=time.perf_counter(); bpy.ops.render.render(write_still=True)
    return round(time.perf_counter()-started,3)


def main():
    OUT.mkdir(exist_ok=True)
    hero_only="--hero-only" in sys.argv
    scene,camera,sun,fill,ground=initialize()
    rows=build_rows(configurations(hero_only))
    mode_settings=Settings(function="WATCHTOWER",region="THORNFELL",context="PASSWATCH",
                           use_grammar=True,detail="HIGH",seed=23)
    mode_rows=[] if hero_only else build_mode_rows(mode_settings)
    render_rows=rows+mode_rows
    report={"blender_version":bpy.app.version_string,"renderer":"BLENDER_EEVEE",
        "source_sha256":source_hashes(), "loaded_modules":loaded_modules(), "rows":[{
            "label":r["label"], "settings":asdict(r["settings"]),
            "effective_settings":asdict(r["plan"].settings),
            "collection_origin_m":list(r["offset"]),
            "validation":r["validation"], "mesh_objects":r["metrics"]["objects"],
            "style":{"wall_material":r["plan"].style.wall_material,
                "construction":r["plan"].style.construction,
                "roof_cover":r["plan"].style.roof_cover,
                "foundation_mode":r["plan"].style.foundation_mode},
            "expected_material_counts":r["expected_material_counts"],
            "actual_blender_material_counts":r["actual_material_counts"],
            "material_counts_match":r["expected_material_counts"]==r["actual_material_counts"],
            "blender_material_rgba":r["materials_by_key"],
            "vertices":r["metrics"]["vertices"], "triangles":r["triangles"],
            "bounds_m":[r["metrics"]["width"],r["metrics"]["depth"],r["metrics"]["height"]],
            "geometry_hash":r["collection"].get("caelm_geometry_hash"),
            "blender_build_seconds":r["build_seconds"],
            "pure_generation_validation_seconds":r["pure_seconds"]} for r in rows],
        "scope":"Blender authoring geometry and visual comparison; not Unity runtime or structural certification."}
    report["solid_efficient_geometry_comparison"]={"settings":asdict(mode_settings),
        "results":compare_geometry_modes(mode_settings),
        "actual_render_fixtures":[{
            "label":r["label"],"mode":r["mode"],"settings":asdict(r["settings"]),
            "validation":r["validation"],"mesh_objects":r["metrics"]["objects"],
            "vertices":r["metrics"]["vertices"],"triangles":r["triangles"],
            "expected_material_counts":r["expected_material_counts"],
            "actual_blender_material_counts":r["actual_material_counts"],
            "material_counts_match":r["expected_material_counts"]==r["actual_material_counts"],
            "bounds_m":[r["metrics"]["width"],r["metrics"]["depth"],r["metrics"]["height"]],
            "geometry_hash":r["collection"].get("caelm_geometry_hash"),
            "blender_build_seconds":r["build_seconds"],
            "pure_generation_validation_seconds":r["pure_seconds"]} for r in mode_rows]}
    report["renders"]={}
    report_path=OUT/"expansion_evidence_manifest.json"
    report_path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"expansion_evidence.blend"),compress=True)

    hero=rows[0]
    for other in render_rows:
        for obj in other["objects"]: obj.hide_render=(other is not hero)
    hero_seconds=frame_for(scene,camera,sun,fill,ground,hero,OUT/"expansion_hero.png",1200,1.35)
    region_seconds=render_group(scene,camera,sun,fill,ground,render_rows,rows[:4],
        (15.0,12.5,2.5),OUT/"four_regions_comparison.png",60.0)
    wealth_seconds=render_group(scene,camera,sun,fill,ground,render_rows,rows[4:7],
        (20.0,56.0,2.5),OUT/"lowmark_wealth_comparison.png",52.0)
    maintenance_seconds=render_group(scene,camera,sun,fill,ground,render_rows,rows[7:9],
        (7.5,77.0,2.5),OUT/"lowmark_maintenance_comparison.png",42.0)
    # Closeups are chosen from actual plan elevations; whole-window framing shows
    # casing and shutters, and the roof sample includes an explicitly hip-roof type.
    closeup_records=[]
    for filename, target, look, ortho, index in (
        ("closeup_window_beam.png", Vector((hero["metrics"]["width"]*.5,0,hero["plan"].eave*.52)),
         Vector((hero["metrics"]["width"]*.5,-7,hero["plan"].eave*.52)), 5.2, 0),
        ("closeup_gable_roof.png", Vector((hero["metrics"]["width"]*.55,hero["metrics"]["depth"]*.45,
                                           hero["plan"].eave+.5)),
         Vector((hero["metrics"]["width"]*.55,-7,hero["plan"].eave+1)), 6.5, 0),
    ):
        for other in rows:
            for obj in other["objects"]: obj.hide_render=(other is not rows[index])
        camera_to(camera,look+Vector((4,-9,2.5)),target)
        camera.data.ortho_scale=ortho
        scene.render.resolution_x=scene.render.resolution_y=900
        scene.render.filepath=str(OUT/filename)
        closeup_started=time.perf_counter()
        bpy.ops.render.render(write_still=True)
        closeup_records.append({"file":filename,"resolution":[900,900],
                                "seconds":round(time.perf_counter()-closeup_started,3)})
    hip=next((row for row in rows if row["settings"].function in ("MARKET_HALL","WATCHTOWER","GATEHOUSE")),None)
    if hip:
        for other in render_rows:
            for obj in other["objects"]: obj.hide_render=(other is not hip)
        c=Vector((hip["offset"][0]+hip["metrics"]["width"]*.5,
                  hip["offset"][1]+hip["metrics"]["depth"]*.5,
                  hip["plan"].eave+.45))
        camera_to(camera,c+Vector((1,-1,.62)).normalized()*9,c)
        camera.data.ortho_scale=6.5
        scene.render.filepath=str(OUT/"closeup_hip_roof.png")
        closeup_started=time.perf_counter()
        bpy.ops.render.render(write_still=True)
        closeup_records.append({"file":"closeup_hip_roof.png","resolution":[900,900],
                                "seconds":round(time.perf_counter()-closeup_started,3)})
    if mode_rows:
        mode_seconds=render_group(scene,camera,sun,fill,ground,render_rows,mode_rows,
            (15.5,173.5,5.0),OUT/"solid_efficient_roof_comparison.png",42.0)
        report["renders"]["solid_efficient_roof_comparison"]={
            "file":"solid_efficient_roof_comparison.png","resolution":[1600,1100],
            "seconds":mode_seconds}
    report["renders"].update({"hero":{"file":"expansion_hero.png","seconds":hero_seconds},
        "four_region_comparison":{"file":"four_regions_comparison.png",
            "resolution":[1600,1100],"seconds":region_seconds},
        "lowmark_wealth_comparison":{"file":"lowmark_wealth_comparison.png",
            "resolution":[1600,1100],"seconds":wealth_seconds},
        "lowmark_maintenance_comparison":{"file":"lowmark_maintenance_comparison.png",
            "resolution":[1600,1100],"seconds":maintenance_seconds},
        "labeled_comparisons":["four_regions_comparison_labeled.png",
            "lowmark_wealth_comparison_labeled.png",
            "lowmark_maintenance_comparison_labeled.png"],
            "closeups":closeup_records})
    if not hero_only:
        FRAMES.mkdir(exist_ok=True)
        timings=[]
        for i,row in enumerate(rows):
            for other in render_rows:
                for obj in other["objects"]: obj.hide_render=(other is not row)
            timings.append(frame_for(scene,camera,sun,fill,ground,row,
                                    FRAMES/f"item_{i:02d}.png",WIDTH,1.55))
        report["renders"]["gallery"]={"items":len(rows),"frame_resolution":[WIDTH,HEIGHT],
                                        "seconds":round(sum(timings),3)}
        for row in render_rows:
            for obj in row["objects"]: obj.hide_render=False
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"expansion_evidence.blend"),compress=True)
        report_path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    else:
        report_path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(f"EXPANSION_HERO_READY={OUT/'expansion_hero.png'}",flush=True)


if __name__=="__main__":
    main()
