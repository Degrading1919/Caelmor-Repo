"""Render a bounded ten-building / four-view Blender evidence set.

Run from this directory with:
  blender --background --python tests/render_evidence.py

Outputs go to evidence/. The saved scene contains all ten buildings. Forty
individual frames are combined into one contact sheet and removed afterward.
"""

import sys
import json
import subprocess
import time
import hashlib
from dataclasses import asdict
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import caelmor_architecture as addon
from caelmor_architecture.model import Settings, make_plan
from caelmor_architecture.blender_backend import COLLECTION_TAG, SETTINGS_KEY, TAG, build
from caelmor_architecture.engine import generate, validate


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
FRAMES = OUT / "_frames"
FUNCTIONS = ("FARMHOUSE", "BARN", "GRAIN_STORE", "MILLER", "INN")
VIEWS = ("front-left", "front-right", "rear-right", "rear-left")
WIDTH = HEIGHT = 360


def point_camera(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 16
    scene.render.resolution_x = WIDTH
    scene.render.resolution_y = HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 1.0
    scene.world = bpy.data.worlds.new("Caelmor Evidence World")
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.24, 0.23, 0.21, 1.0)
    background.inputs["Strength"].default_value = 0.55

    bpy.ops.mesh.primitive_plane_add(size=1000, location=(65, 14, -0.08))
    ground = bpy.context.object
    ground.name = "Neutral Evidence Ground"
    material = bpy.data.materials.new("Neutral Ground")
    material.diffuse_color = (0.16, 0.17, 0.15, 1.0)
    material.use_nodes = True
    material.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.16, 0.17, 0.15, 1.0)
    ground.data.materials.append(material)

    bpy.ops.object.light_add(type="SUN", location=(0, -18, 24))
    sun = bpy.context.object
    sun.name = "Evidence Sun"
    sun.data.energy = 2.5
    sun.data.angle = 0.18
    sun.rotation_euler = (0.44, -0.35, -0.44)
    bpy.ops.object.light_add(type="AREA", location=(0, -12, 10))
    light = bpy.context.object
    light.name = "Evidence Fill"
    light.data.energy = 1200
    light.data.shape = "DISK"
    light.data.size = 16
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "Evidence Camera"
    scene.camera = camera
    camera.data.type = "ORTHO"
    addon.register()
    return scene, camera, sun, light, ground


def create_buildings():
    presets = {
        "FARMHOUSE": {"footprint": "L", "width": 11.0, "depth": 7.0, "floors": 2},
        "BARN": {"footprint": "RECT", "width": 16.0, "depth": 10.0, "floors": 1, "pitch": 42.0},
        "GRAIN_STORE": {"footprint": "RECT", "width": 8.5, "depth": 5.5, "floors": 1},
        "MILLER": {"footprint": "T", "width": 12.0, "depth": 8.0, "floors": 2},
        "INN": {"footprint": "U", "width": 15.0, "depth": 10.0,
                "floors": 2, "wing_width": 4.5, "wing_depth": 6.0},
    }
    configurations = []
    for function in FUNCTIONS:
        for variant, seed in enumerate((17, 43)):
            values = dict(presets[function], function=function, seed=seed)
            if variant == 1:
                values["width"] += 0.5
                values["depth"] += 0.3
                values["window_density"] = 1.2
            if function == "FARMHOUSE" and variant == 1:
                # Deliberately edited footprint, dimensions, and floor count.
                values.update(footprint="U", width=13.5, depth=8.5, wing_width=4.0,
                              wing_depth=5.2, floors=1)
            configurations.append(Settings(**values))

    records = []
    for index, settings in enumerate(configurations):
        build_started = time.perf_counter()
        collection, metrics = build(settings)
        blender_build_seconds = time.perf_counter() - build_started
        validation_started = time.perf_counter()
        plan, buffers = generate(settings)
        validation = validate(plan, buffers)
        pure_generation_seconds = time.perf_counter() - validation_started
        if not validation["valid"]:
            raise ValueError(f"Evidence geometry failed validation: {validation['errors']}")
        col, row = index % 5, index // 5
        offset = Vector((col * 30.0, row * 27.0, 0.0))
        anchor = next(obj for obj in collection.objects if obj.get("caelm_anchor"))
        anchor.location += offset
        objects = [obj for obj in collection.objects
                   if obj.get(TAG) and not obj.get("caelm_collider")]
        center_y = settings.depth * 0.5 if settings.footprint == "RECT" else (settings.depth - settings.wing_depth) * 0.5
        center = offset + Vector((metrics["width"] * 0.5, center_y,
                                  metrics["height"] * 0.47))
        records.append({"settings": settings, "collection": collection, "objects": objects,
                        "anchor": anchor, "offset": offset, "center": center,
                        "metrics": metrics, "validation": validation, "plan": plan,
                        "blender_build_seconds": blender_build_seconds,
                        "pure_generation_validation_seconds": pure_generation_seconds})
    source_hashes = {}
    for source in sorted((ROOT / "caelmor_architecture").glob("*.py")):
        source_hashes[source.name] = hashlib.sha256(source.read_bytes()).hexdigest()
    report = {
        "blender_version": bpy.app.version_string,
        "renderer": "BLENDER_EEVEE",
        "contact_sheet_views_per_building": len(VIEWS),
        "source_sha256": source_hashes,
        "timing_note": "Per-building Blender object construction and independent pure generation/validation wall times measured with time.perf_counter; rendering times recorded by render entry below.",
        "buildings": [
            {"function": r["settings"].function, "seed": r["settings"].seed,
             "footprint": r["settings"].footprint, "width": r["settings"].width,
             "depth": r["settings"].depth, "floors": r["settings"].floors,
             "settings": asdict(r["settings"]), "validation": r["validation"],
             "blender_build_seconds": round(r["blender_build_seconds"], 4),
             "pure_generation_validation_seconds": round(r["pure_generation_validation_seconds"], 4),
             "mesh_objects": r["metrics"]["objects"], "vertices": r["metrics"]["vertices"],
             "bounds_m": [r["metrics"]["width"], r["metrics"]["depth"], r["metrics"]["height"]],
             "geometry_hash": r["collection"].get("caelm_geometry_hash")}
            for r in records
        ],
    }
    (OUT / "evidence_manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return records


def _set_light(sun, light, center, distance, energy, size):
    sun.location = center + Vector((-distance * 0.8, -distance * 0.6, distance * 1.2))
    sun.rotation_euler = (0.44, -0.35, -0.44)
    light.location = center + Vector((-distance * 0.55, -distance * 0.7, distance * 0.9))
    light.rotation_euler = (center - light.location).to_track_quat("-Z", "Y").to_euler()
    light.data.energy = energy
    light.data.size = size


def render_contact_sheet(scene, camera, sun, light, ground, records):
    # Render the hero first so visual review is available before the longer contact pass.
    hero = records[0]
    for record in records:
        for obj in record["objects"]:
            obj.hide_render = record is not hero
    c = hero["center"]
    ground.location = (c.x, c.y, -0.08)
    point_camera(camera, c + Vector((-17, -23, 21)), c)
    camera.data.ortho_scale = max(hero["metrics"]["width"], hero["metrics"]["depth"],
                                  hero["metrics"]["height"]) * 1.35 + 2.5
    _set_light(sun, light, c, 30, 1500, 20)
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 1200
    scene.render.filepath = str(OUT / "hero.png")
    hero_started = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    hero_seconds = round(time.perf_counter() - hero_started, 3)
    closeup_times = render_closeups(scene, camera, sun, light, ground, hero)
    print(f"HERO_READY={OUT / 'hero.png'} seconds={hero_seconds}", flush=True)

    contact_started = time.perf_counter()
    FRAMES.mkdir(parents=True, exist_ok=True)
    scene.render.resolution_x = WIDTH
    scene.render.resolution_y = HEIGHT
    for record_index, record in enumerate(records):
        for other in records:
            for obj in other["objects"]:
                obj.hide_render = other is not record
        c = record["center"]
        width, depth = record["metrics"]["width"], record["metrics"]["depth"]
        distance = max(width, depth) * 1.65 + 5.0
        camera.data.ortho_scale = max(width, depth, record["metrics"]["height"]) * 1.55 + 3.5
        ground.location = (c.x, c.y, -0.08)
        directions = (Vector((-1, -1, .48)), Vector((1, -1, .48)),
                      Vector((1, 1, .48)), Vector((-1, 1, .48)))
        for view, direction in zip(VIEWS, directions):
            direction.normalize()
            point_camera(camera, c + direction * distance, c)
            _set_light(sun, light, c, distance, 1200, max(width, depth) * 1.4)
            scene.render.filepath = str(FRAMES / f"building_{record_index:02d}_{view}.png")
            bpy.ops.render.render(write_still=True)
    contact_seconds = round(time.perf_counter() - contact_started, 3)

    # Render a settlement overview of the complete, editable set.
    for record in records:
        for obj in record["objects"]:
            obj.hide_render = False

    for record in records:
        for obj in record["objects"]:
            obj.hide_render = False
    overall = Vector((65.0, 14.0, 0.0))
    ground.location = (overall.x, overall.y, -0.08)
    point_camera(camera, overall + Vector((8, -90, 66)), overall)
    camera.data.ortho_scale = 165.0
    _set_light(sun, light, overall, 80, 1800, 48)
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 1100
    scene.render.filepath = str(OUT / "overview.png")
    overview_started = time.perf_counter()
    manifest_path = OUT / "evidence_manifest.json"
    report = json.loads(manifest_path.read_text(encoding="utf-8"))
    report["renders"] = {
        "hero": {"file": "hero.png", "resolution": [1200, 1200], "seconds": hero_seconds},
        "closeups": closeup_times,
        "contact_sheet": {"views": len(records) * len(VIEWS), "resolution_per_view": [WIDTH, HEIGHT],
                          "seconds": contact_seconds},
        "overview": {"file": "overview.png", "resolution": [1800, 1100]},
    }
    bpy.ops.render.render(write_still=True)
    report["renders"]["overview"]["seconds"] = round(time.perf_counter() - overview_started, 3)
    manifest_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "ten_buildings.blend"), compress=True)
    print(f"BLEND_READY={OUT / 'ten_buildings.blend'}", flush=True)

    # Pillow fails to read a freshly written render in the same Blender process
    # on some Windows builds; compose in a clean sequential Blender process.
    composer = Path(__file__).resolve().parent / "compose_contact_sheet.py"
    subprocess.run([bpy.app.binary_path, "--background", "--python", str(composer)], check=True)
    for frame in FRAMES.glob("*.png"):
        frame.unlink()
    FRAMES.rmdir()
    # Store the overview framing as the initial view of the complete editable scene.
    scene.render.filepath = str(OUT / "overview.png")


def render_closeups(scene, camera, sun, light, ground, hero):
    """Capture timber joinery, roof/eave, shingle valley, and material crops."""
    c = hero["center"]
    plan = hero.get("plan")
    if plan is None:
        row = json.loads((OUT / "evidence_manifest.json").read_text(encoding="utf-8"))["buildings"][0]
        plan = make_plan(Settings(**row["settings"]))
    width = hero["metrics"]["width"]
    depth = hero["metrics"]["depth"]
    height = hero["metrics"]["height"]
    # The farmhouse is the L-footprint seed-17 hero. Target its front corner,
    # valley junction, and uninterrupted plaster/shingle surfaces separately.
    views = (
        ("closeup_timber.png", c + Vector((2.0, -depth * .34, height * .30)),
         c + Vector((-8.0, -12.0, 8.0)), 7.5),
        ("closeup_valley.png", Vector((3.4, .8, plan.roof_height(3.4, .8)+.15)),
         Vector((8.0, -10.0, 8.0)), 4.5),
        ("closeup_surfaces.png", Vector((9.0, 0.0, 2.2)),
         Vector((5.0, -9.0, 3.5)), 4.3),
        ("closeup_eave.png", Vector((9.0, -.1, plan.eave + .1)),
         Vector((5.0, -7.0, 5.0)), 3.6),
    )
    scene.render.resolution_x = scene.render.resolution_y = 900
    results = []
    for filename, target, offset, scale in views:
        point_camera(camera, target + offset, target)
        camera.data.ortho_scale = scale
        ground.location = (target.x, target.y, -0.08)
        _set_light(sun, light, target, 20, 1200, 11)
        scene.render.filepath = str(OUT / filename)
        started = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        results.append({"file": filename, "resolution": [900, 900],
                        "seconds": round(time.perf_counter() - started, 3)})
    return results


def render_hero_only(scene, camera, sun, light, ground, records):
    hero = records[0]
    for record in records:
        for obj in record["objects"]:
            obj.hide_render = record is not hero
    c = hero["center"]
    ground.location = (c.x, c.y, -0.08)
    point_camera(camera, c + Vector((-17, -23, 21)), c)
    camera.data.ortho_scale = max(hero["metrics"]["width"], hero["metrics"]["depth"],
                                  hero["metrics"]["height"]) * 1.35 + 2.5
    _set_light(sun, light, c, 30, 1500, 20)
    scene.render.resolution_x = scene.render.resolution_y = 1200
    scene.render.filepath = str(OUT / "hero.png")
    started = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    seconds = round(time.perf_counter() - started, 3)
    closeup_times = render_closeups(scene, camera, sun, light, ground, hero)
    point_camera(camera, c + Vector((-17, -23, 21)), c)
    camera.data.ortho_scale = max(hero["metrics"]["width"], hero["metrics"]["depth"],
                                  hero["metrics"]["height"]) * 1.35 + 2.5
    scene.render.resolution_x = scene.render.resolution_y = 1200
    print(f"HERO_READY={OUT / 'hero.png'} seconds={seconds}", flush=True)
    for record in records:
        for obj in record["objects"]:
            obj.hide_render = False
    scene.render.filepath = str(OUT / "hero.png")
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "ten_buildings.blend"), compress=True)
    manifest_path = OUT / "evidence_manifest.json"
    report = json.loads(manifest_path.read_text(encoding="utf-8"))
    report["renders"] = {
        "hero": {"file": "hero.png", "resolution": [1200, 1200], "seconds": seconds},
        "closeups": closeup_times,
    }
    manifest_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def render_saved_closeups():
    """Reframe detail crops from the hero-only scene without rebuilding geometry."""
    blend = OUT / "ten_buildings.blend"
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    scene = bpy.context.scene
    report_path = OUT / "evidence_manifest.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    row = report["buildings"][0]
    settings = row["settings"]
    bounds = row["bounds_m"]
    center_y = settings["depth"] * .5 if settings["footprint"] == "RECT" else (settings["depth"]-settings["wing_depth"])*.5
    hero = {"center": Vector((bounds[0]*.5, center_y, bounds[2]*.47)),
            "metrics": {"width": bounds[0], "depth": bounds[1], "height": bounds[2]},
            "plan": make_plan(Settings(**settings))}
    collection = next(c for c in bpy.data.collections
                      if c.get(COLLECTION_TAG) and json.loads(c.get(SETTINGS_KEY, "{}" )).get("seed") == settings["seed"]
                      and json.loads(c.get(SETTINGS_KEY, "{}" )).get("function") == settings["function"])
    hero_objects = [obj for obj in collection.objects if obj.get(TAG) and not obj.get("caelm_collider")]
    hero_set = set(hero_objects)
    for obj in bpy.data.objects:
        if obj.get(TAG) and not obj.get("caelm_collider"):
            obj.hide_render = obj not in hero_set
    camera = scene.camera
    sun = bpy.data.objects.get("Evidence Sun")
    light = bpy.data.objects.get("Evidence Fill")
    ground = bpy.data.objects.get("Neutral Evidence Ground")
    closeup_times = render_closeups(scene, camera, sun, light, ground, hero)
    c = hero["center"]
    point_camera(camera, c + Vector((-17, -23, 21)), c)
    camera.data.ortho_scale = max(hero["metrics"]["width"], hero["metrics"]["depth"],
                                  hero["metrics"]["height"]) * 1.35 + 2.5
    scene.render.resolution_x = scene.render.resolution_y = 1200
    scene.render.filepath = str(OUT / "hero.png")
    for obj in hero_objects:
        obj.hide_render = False
    report.setdefault("renders", {})["closeups"] = closeup_times
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    bpy.ops.wm.save_as_mainfile(filepath=str(blend), compress=True)
    print(f"CLOSEUPS_READY={OUT}", flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if "--closeups-only" in sys.argv:
        render_saved_closeups()
        return
    scene, camera, sun, light, ground = setup_scene()
    records = create_buildings()
    if "--hero-only" in sys.argv:
        render_hero_only(scene, camera, sun, light, ground, records)
        return
    render_contact_sheet(scene, camera, sun, light, ground, records)
    print(f"Evidence generated: {OUT}")
    print(f"Buildings: {len(records)}; views per building: {len(VIEWS)}; hero: {OUT / 'hero.png'}")


if __name__ == "__main__":
    main()
