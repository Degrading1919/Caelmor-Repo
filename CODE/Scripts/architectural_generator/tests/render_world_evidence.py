"""Render neutral-clay evidence for the world-aware architectural grammar.

Run with Blender's bundled Python:
  blender --background --python tests/render_world_evidence.py -- --quick
  blender --background --python tests/render_world_evidence.py -- --matrix

Outputs are deliberately kept under evidence/world_*. The quick pass is the
first four-region cottage comparison; matrix mode records generation,
validation, regeneration, and a bounded set of comparison renders.
"""
from __future__ import annotations

import bpy
import hashlib
import json
import math
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path

from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
FRAMES = OUT / "_world_frames"
sys.path.insert(0, str(ROOT))

from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate, validate, geometry_hash
from caelmor_architecture import blender_backend
from caelmor_architecture.blender_backend import build
from caelmor_architecture.profiles import TYPE_SPECS

REGIONS = ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")
FUNCTIONS = tuple(TYPE_SPECS)
WEALTH_LEVELS = ("MODEST", "ESTABLISHED", "AFFLUENT")


def _neutral_material():
    mat = bpy.data.materials.new("Neutral clay - geometry review")
    mat.diffuse_color = (.48, .48, .46, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (.48, .48, .46, 1)
    shader.inputs["Roughness"].default_value = .92
    return mat


def _reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 740
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = .8
    scene.world = bpy.data.worlds.new("World evidence studio")
    scene.world.color = (.2, .2, .2)
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get("Background").inputs["Color"].default_value = (.32, .32, .31, 1)
    scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = .7
    bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, -.08))
    ground = bpy.context.object
    ground.name = "Neutral ground"
    ground.data.materials.append(_neutral_material())
    bpy.ops.object.light_add(type="SUN", location=(-15, -18, 28))
    sun = bpy.context.object
    sun.data.energy = 2.1
    sun.data.angle = .12
    sun.rotation_euler = (.45, -.42, -.45)
    bpy.ops.object.light_add(type="AREA", location=(5, -14, 13))
    fill = bpy.context.object
    fill.data.energy = 1500
    fill.data.shape = "DISK"
    fill.data.size = 13
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.data.type = "ORTHO"
    scene.camera = camera
    return scene, camera


def _aim(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


def _materials(collection, mat):
    for obj in collection.objects:
        if obj.type != "MESH":
            continue
        obj.data.materials.clear()
        obj.data.materials.append(mat)


def _bounds(collection):
    points = [obj.matrix_world @ Vector(corner) for obj in collection.objects
              if obj.type == "MESH" and not obj.hide_render and not obj.get("caelm_collider")
              for corner in obj.bound_box]
    if not points:
        raise RuntimeError("Generated collection has no renderable mesh bounds")
    return tuple((min(p[i] for p in points), max(p[i] for p in points)) for i in range(3))


def _render_one(scene, camera, settings, output, label=None):
    started = time.perf_counter()
    plan, buffers = generate(settings)
    metrics = validate(plan, buffers)
    build_started = time.perf_counter()
    collection, backend_metrics = build(settings)
    build_seconds = time.perf_counter() - build_started
    collection.name = "world_" + settings.region.lower() + "_" + settings.function.lower()
    clay = bpy.data.materials.get("Neutral clay - geometry review") or _neutral_material()
    _materials(collection, clay)
    bounds = _bounds(collection)
    center = tuple((lo + hi) / 2 for lo, hi in bounds)
    span = tuple(hi - lo for lo, hi in bounds)
    distance = max(span[0], span[1])
    target = (center[0], center[1], center[2] * .91)
    _aim(camera, (center[0] + distance * .9, center[1] - distance * 1.35,
                  center[2] + max(span[2] * 1.1, distance * .75)), target)
    camera.data.ortho_scale = max(span[0] * 1.75, span[1] * 1.65, span[2] * 1.5, 11)
    # Wider landscape framing can otherwise crop the depth dimension.
    camera.data.ortho_scale = max(camera.data.ortho_scale, camera.data.ortho_scale * 1100 / 740)
    overlay=None
    if label:
        bpy.ops.object.text_add()
        overlay=bpy.context.object
        overlay.name="World evidence frame label"
        overlay.data.body=label
        overlay.data.size=max(.25,camera.data.ortho_scale*.045)
        overlay.data.extrude=0
        overlay.parent=camera
        overlay.location=(-camera.data.ortho_scale*.46,-camera.data.ortho_scale*.45,-1.0)
        overlay.rotation_euler=(0,0,0)
    scene.render.filepath = str(output)
    bpy.ops.render.render(write_still=True)
    if overlay:
        bpy.data.objects.remove(overlay,do_unlink=True)
    row = {"settings": asdict(settings), "geometry_hash": geometry_hash(buffers),
           "metrics": metrics, "backend_metrics": backend_metrics,
           "build_seconds": round(build_seconds, 4),
           "elapsed_seconds": round(time.perf_counter() - started, 4),
           "bounds": bounds, "image": output.name,"label":label,
           "blender_version":bpy.app.version_string,
           "source_hashes":_source_hashes()}
    return row


def _source_hashes():
    import caelmor_architecture.engine as engine_module
    import caelmor_architecture.model as model_module
    import caelmor_architecture.facade as facade_module
    import caelmor_architecture.roof as roof_module
    import caelmor_architecture.world as world_module
    from caelmor_architecture import world_lowmark_thornfell, world_mire, world_emberholt
    paths=(engine_module.__file__,model_module.__file__,facade_module.__file__,
           roof_module.__file__,world_module.__file__,world_lowmark_thornfell.__file__,
           world_mire.__file__,world_emberholt.__file__,blender_backend.__file__,__file__)
    return {Path(path).name:hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in paths}


def _gallery(scene, camera, settings_list, stem, blind=False):
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    random.seed(1204)
    order = list(settings_list)
    ids = ["A", "B", "C", "D"] if len(order) == 4 else [f"{i+1:03}" for i in range(len(order))]
    if blind and len(order) == 4:
        random.shuffle(ids)
        if ids == ["A", "B", "C", "D"]:
            ids = ["C", "A", "D", "B"]
    records = []
    for i, (settings, ident) in enumerate(zip(order, ids)):
        for obj in list(bpy.data.objects):
            if obj.type == "MESH" and obj.name != "Neutral ground":
                bpy.data.objects.remove(obj, do_unlink=True)
            elif obj.type=="FONT":
                bpy.data.objects.remove(obj,do_unlink=True)
        for collection in list(bpy.data.collections):
            if collection.get("caelm_build"):
                bpy.data.collections.remove(collection, do_unlink=True)
        target = FRAMES / f"{stem}_{ident}.png"
        label=ident if blind else f"{settings.region} · {settings.function} · {settings.wealth}"
        row = _render_one(scene, camera, settings, target,label)
        row["blind_id"] = ident
        records.append(row)
    (OUT / f"world_{stem}_manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    mapping = {row["blind_id"]: row["settings"] for row in records}
    if blind:
        (OUT / f"world_{stem}_blind_key.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    return records


def _compose(stem, names, out_path, title):
    # Compose labelled and blind panels with Blender's own image API.
    images = [bpy.data.images.load(str(FRAMES / name), check_existing=False) for name in names]
    width = max(img.size[0] for img in images)
    height = max(img.size[1] for img in images)
    canvas = bpy.data.images.new("World evidence contact sheet", width=width*2, height=height*2+70, alpha=True)
    # Pixel copying avoids additional image package dependencies.
    pixels = [0.08, 0.08, 0.08, 1.0] * (canvas.size[0] * canvas.size[1])
    for idx, img in enumerate(images):
        ox = (idx % 2) * width
        oy = 70 + (1 - idx // 2) * height
        src = list(img.pixels[:])
        for y in range(height):
            si = y * width * 4
            di = ((oy + y) * canvas.size[0] + ox) * 4
            pixels[di:di+width*4] = src[si:si+width*4]
    canvas.pixels[:] = pixels
    canvas.filepath_raw = str(out_path)
    canvas.file_format = "PNG"
    canvas.save()
    for img in images:
        bpy.data.images.remove(img)
    bpy.data.images.remove(canvas)


def _render_batch(settings_list, stem, manifest_name):
    rows=[]
    for i,settings in enumerate(settings_list):
        scene,camera=_reset_scene()
        label=f"{settings.region} · {settings.function} · {settings.wealth} · {settings.geometry_mode}"
        rows.append(_render_one(scene,camera,settings,
            FRAMES/f"{stem}_{i:02}.png",label))
    (OUT/manifest_name).write_text(json.dumps(rows,indent=2),encoding="utf-8")
    return rows


def _save_editable_cottage_scene(settings_list):
    scene,camera=_reset_scene()
    next_x=0.0
    records=[]
    for settings in settings_list:
        plan,buffers=generate(settings)
        expected_hash=geometry_hash(buffers)
        validation=validate(plan,buffers)
        if not validation["valid"]:
            raise RuntimeError("Editable clay scene contains invalid world geometry: "+repr(validation["errors"][:6]))
        collection,metrics=build(settings,origin=(next_x,0,0))
        if collection.get("caelm_geometry_hash")!=expected_hash:
            raise RuntimeError("Blender collection source hash differs from engine geometry hash")
        clay=bpy.data.materials.get("Neutral clay - geometry review") or _neutral_material()
        _materials(collection,clay)
        bounds=_bounds(collection)
        records.append({"settings":asdict(settings),"collection":collection.name,
                        "bounds":bounds,"backend_metrics":metrics,
                        "geometry_hash":expected_hash,"validation":validation})
        next_x=bounds[0][1]+2.2
    target=(next_x*.5,2.2,3.0)
    _aim(camera,(next_x*.5,-max(next_x*.95,18),max(11,target[2]+8)),target)
    camera.data.ortho_scale=max(next_x*1.25,24)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"world_four_region_cottages.blend"))
    blend_path=OUT/"world_four_region_cottages.blend"
    manifest={"blender_version":bpy.app.version_string,
              "blend_sha256":hashlib.sha256(blend_path.read_bytes()).hexdigest(),
              "source_hashes":_source_hashes(),"buildings":records,
              "scene":"Four editable, neutral-clay cottages; each collection has world settings metadata."}
    (OUT/"world_four_region_cottages_manifest.json").write_text(
        json.dumps(manifest,indent=2),encoding="utf-8")


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    quick = "--matrix" not in args
    scene, camera = _reset_scene()
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    if quick:
        settings = [Settings(seed=91, function="COTTAGE", region=r, wealth="MODEST",
                             craftsmanship="STANDARD", detail="LOW", use_grammar=True,
                             world_aware=True) for r in REGIONS]
        rows = _gallery(scene, camera, settings, "first_four_clay", blind=True)
        _compose("first_four_clay", [f"first_four_clay_{r['blind_id']}.png" for r in rows],
                 OUT / "world_first_four_clay_blind.png", "Blind regional cottage comparison")
        _save_editable_cottage_scene(settings)
        print("FIRST FOUR WORLD COTTAGES", json.dumps(rows, indent=2))
        return

    # Full core matrix: 4 regions x 20 functions x 3 wealth levels, all at low
    # detail. Each case regenerates in memory to record an independent hash.
    matrix = []
    for region in REGIONS:
        for function in FUNCTIONS:
            for wealth in WEALTH_LEVELS:
                settings = Settings(seed=91, function=function, region=region,
                                    wealth=wealth, craftsmanship="STANDARD",
                                    detail="LOW", use_grammar=True, world_aware=True)
                start = time.perf_counter()
                plan, buffers = generate(settings)
                metrics = validate(plan, buffers)
                repeat_plan, repeat_buffers = generate(settings)
                repeat_hash = geometry_hash(repeat_buffers)
                row = {"region":region, "function":function, "wealth":wealth,"seed":91,
                       "geometry_hash":geometry_hash(buffers),
                       "repeat_hash":repeat_hash, "deterministic":geometry_hash(buffers)==repeat_hash,
                       "metrics":metrics, "generation_validation_seconds":round(time.perf_counter()-start,4)}
                matrix.append(row)
    (OUT / "world_matrix_240.json").write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    # Selected high and efficient profiles; same seed and function per region.
    selected = []
    for region in REGIONS:
        for wealth in ("ESTABLISHED", "AFFLUENT"):
            for mode in ("SOLID", "EFFICIENT"):
                s = Settings(seed=91, function="COTTAGE", region=region, wealth=wealth,
                             detail="HIGH", geometry_mode=mode, use_grammar=True, world_aware=True)
                plan, buffers = generate(s)
                selected.append({"settings":asdict(s), "metrics":validate(plan,buffers),
                                 "hash":geometry_hash(buffers)})
    (OUT / "world_selected_profiles.json").write_text(json.dumps(selected, indent=2), encoding="utf-8")
    cottage_wealth=[Settings(seed=91,function="COTTAGE",region=region,wealth=wealth,
        detail="LOW",use_grammar=True,world_aware=True)
        for region in REGIONS for wealth in WEALTH_LEVELS]
    wealth_rows=_render_batch(cottage_wealth,"wealth_cottage",
                              "world_wealth_cottages_render_manifest.json")
    _save_editable_cottage_scene([Settings(seed=91,function="COTTAGE",region=r,
        wealth="MODEST",detail="LOW",use_grammar=True,world_aware=True) for r in REGIONS])

    function_settings=[Settings(seed=91,function=fn,region=region,wealth="MODEST",
        detail="LOW",use_grammar=True,world_aware=True)
        for region in REGIONS for fn in ("COTTAGE","FARMHOUSE","SMITHY","ASSEMBLY_HALL")]
    function_rows=_render_batch(function_settings,"function_matrix",
                               "world_matrix_render_manifest.json")
    high_settings=[Settings(seed=91,function="COTTAGE",region=region,wealth=wealth,
        detail="HIGH",geometry_mode=mode,use_grammar=True,world_aware=True)
        for region in REGIONS for wealth in ("ESTABLISHED","AFFLUENT")
        for mode in ("SOLID","EFFICIENT")]
    high_rows=_render_batch(high_settings,"high_profiles",
                            "world_high_profiles_render_manifest.json")
    print(f"WORLD MATRIX: {len(matrix)} configs; valid={sum(r['metrics']['valid'] for r in matrix)}; deterministic={sum(r['deterministic'] for r in matrix)}; rendered={len(wealth_rows)+len(function_rows)+len(high_rows)}")


if __name__ == "__main__":
    main()
