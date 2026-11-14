"""Headless native-kit regression and evidence renders for roof autocomplete.

Run from the repository root with Blender 5.x:
  blender --background --disable-autoexec --python CODE/Scripts/architectural_generator/tests/test_roof_autocomplete_blender.py

This uses the authored Lowmark wood_trimmed_plaster wall modules. It keeps the
door, window and original wall meshes in the scene while checking roof-only
generation, repeat cleanup, export, and lighting response.
"""
import hashlib
import json
import math
import os
import struct
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.roof_selection import infer_bearing
from caelmor_architecture.roof_autocomplete import build_roof_collection
from caelmor_architecture.roof import shingle_step
import caelmor_architecture as addon

EVIDENCE = ROOT / "evidence" / "roof_autocomplete"
EVIDENCE.mkdir(parents=True, exist_ok=True)
KIT = REPO / "MEDIA" / "Materials" / "working" / "lowmark" / "Building_Assets" / "wood_trimmed_plaster"
MATDIR = REPO / "MEDIA" / "Materials" / "procedurally_generated"


def append_module(path, center, angle=0.0, prefix="wall"):
    """Append one authored two metre module and place its complete object set."""
    path = str(KIT / path)
    with bpy.data.libraries.load(path, link=False) as (source, target):
        target.objects = list(source.objects)
    offset = Matrix.Translation(Vector(center))
    rotation = Matrix.Rotation(angle, 4, "Z")
    objects = []
    for index, obj in enumerate(target.objects):
        if obj is None or obj.type != "MESH":
            continue
        bpy.context.scene.collection.objects.link(obj)
        obj.matrix_world = offset @ rotation @ obj.matrix_world
        obj.name = f"KIT_{prefix}_{index:02d}_{obj.name}"
        obj["caelm_native_kit"] = "wood_trimmed_plaster"
        obj["caelm_native_module"] = Path(path).stem
        objects.append(obj)
    return objects


def assemble_test_house():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    walls = []
    # 6 by 4 metres. Authored doorway and window remain in the test footprint.
    front = ["2mW_3mH_trimmed.blend", "2mW_3mH_doorway.blend", "2mW_3mH_trimmed.blend"]
    for x, name in zip((-2.0, 0.0, 2.0), front):
        role = "door" if "doorway" in name else "front"
        walls += append_module(name, (x, -2.0, 0.0), math.pi / 2, role)
    back = "2mW_3mH_trimmed.blend"
    for x in (-2.0, 0.0, 2.0):
        walls += append_module(back, (x, 2.0, 0.0), math.pi / 2, "back")
    walls += append_module("2mW_3mH_trimmed_window.blend", (3.0, -1.0, 0.0), 0, "east_window")
    walls += append_module("2mW_3mH_trimmed.blend", (3.0, 1.0, 0.0), 0, "east")
    walls += append_module("2mW_3mH_trimmed.blend", (-3.0, -1.0, 0.0), 0, "west")
    walls += append_module("2mW_3mH_trimmed.blend", (-3.0, 1.0, 0.0), 0, "west")
    for obj in walls:
        obj["caelm_native_wall"] = True
    return walls


def mesh_fingerprint(objects):
    rows = []
    for obj in sorted(objects, key=lambda item: item.name):
        mesh = obj.data
        coords = tuple(round(value, 6) for vertex in mesh.vertices for value in vertex.co)
        rows.append((len(mesh.vertices), len(mesh.polygons), coords))
    rows.sort()
    return hashlib.sha256(repr(rows).encode("utf-8")).hexdigest()


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def roof_bounds(collection):
    points = [obj.matrix_world @ vertex.co for obj in collection.objects if obj.type == "MESH"
              for vertex in obj.data.vertices]
    return tuple((min(point[i] for point in points), max(point[i] for point in points))
                 for i in range(3))


def assert_field_uv(collection, rise, detail, bearing):
    """Check the UV axes follow ridge/run directions and start on course phase."""
    fields = [obj for obj in collection.objects if obj.type == "MESH" and
              "Mapped roof field" in obj.name]
    check(len(fields) == 1, f"expected one mapped field mesh, found {len(fields)}")
    obj = fields[0]
    uv = obj.data.uv_layers.get("RoofUV")
    check(uv is not None, "continuous field is missing named RoofUV")
    slope = rise / (bearing.depth * .5)
    pitch = math.degrees(math.atan(slope))
    plan = type("UvPlan", (), {"settings": type("UvSettings", (),
        {"detail": "HIGH", "age": 0, "roof_style": "GABLE"})(), "slope": slope,
        "style": type("UvStyle", (), {"roof_cover": "SHINGLE"})()})()
    step = shingle_step(plan)
    expected_courses = 1 if detail < 34 else (2 if detail < 67 else 4)
    vs = []
    for poly in obj.data.polygons:
        coords = [(obj.matrix_world @ obj.data.vertices[obj.data.loops[li].vertex_index].co,
                   uv.data[li].uv) for li in poly.loop_indices]
        for i, (a, auv) in enumerate(coords):
            for b, buv in coords[i+1:]:
                dx, dy, dz = b.x-a.x, b.y-a.y, b.z-a.z
                du, dv = buv.x-auv.x, buv.y-auv.y
                if abs(dz) > 1e-7:
                    check(abs(abs(dy)-abs(dz/slope)) < 2e-5,
                          "roof field fall line does not match the requested pitch")
                if abs(dx) > 1e-5:
                    check(abs(abs(du/dx)-1/1.28) < 2e-5,
                          f"roof field U does not follow ridge/grain direction: dU/dX={du/dx} dX={dx} dY={dy}")
                else:
                    check(abs(du) < 2e-5, "roof field U drifts across the fall line")
                if abs(dz) > 1e-7:
                    check(abs(dv/dz - 1/(slope*step*8)) < 2e-4,
                          "roof field V does not follow the pitched course direction")
                else:
                    check(abs(dv) < 2e-5, "roof field V drifts along the ridge")
        vs.extend(uv.data[li].uv.y for li in poly.loop_indices)
    check(vs and abs(min(vs)-expected_courses/8) < 2e-4,
          f"mapped field begins off its course phase: minV={min(vs) if vs else None}")
    return {"field_min_v": round(min(vs), 6), "expected_course_start": expected_courses/8,
            "repeat_courses": 8, "ridge_axis": "X", "pitch_alignment": True}


def make_camera_and_lights(scene, variation):
    bpy.ops.object.camera_add(location=(9.5, -11.5, 8.2))
    camera = bpy.context.object
    camera.name = "EvidenceCamera"
    camera.rotation_euler = (Vector((0, 0, 1.8)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 12.5
    scene.camera = camera
    bpy.ops.object.light_add(type="AREA", location=(1.5, -5.0, 10.0))
    key = bpy.context.object
    key.name = "EvidenceKey"
    key.data.energy = 1550 if variation == 0 else 1100
    key.data.shape = "DISK"
    key.data.size = 8.0
    key.rotation_euler = (Vector((0, 0, 1.5)) - key.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="AREA", location=(-5.0, 4.5, 6.0))
    fill = bpy.context.object
    fill.name = "EvidenceFill"
    fill.data.energy = 950 if variation == 0 else 1700
    fill.data.color = (1.0, 0.76, 0.53) if variation == 0 else (0.56, 0.72, 1.0)
    fill.data.size = 7.0
    fill.rotation_euler = (Vector((0, 0, 1.5)) - fill.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.render.resolution_x = 960
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    if scene.world is None:
        scene.world = bpy.data.worlds.new("RoofEvidenceWorld")
    scene.world.color = (0.045, 0.045, 0.045)
    scene.render.image_settings.file_format = "PNG"


def render_pair(collection):
    scene = bpy.context.scene
    # Hide previous collection if caller has left it in the scene.
    make_camera_and_lights(scene, 0)
    scene.render.filepath = str(EVIDENCE / "roof_warm_key.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(bpy.data.objects["EvidenceKey"], do_unlink=True)
    bpy.data.objects.remove(bpy.data.objects["EvidenceFill"], do_unlink=True)
    # Recreate lights for the cooler opposing-key study.
    bpy.ops.object.light_add(type="AREA", location=(-5.0, 2.0, 9.0))
    key = bpy.context.object
    key.name = "EvidenceKey"
    key.data.energy = 1450
    key.data.color = (0.62, 0.77, 1.0)
    key.data.size = 7.5
    key.rotation_euler = (Vector((0, 0, 1.6)) - key.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.light_add(type="AREA", location=(7.0, -1.5, 6.0))
    fill = bpy.context.object
    fill.name = "EvidenceFill"
    fill.data.energy = 1000
    fill.data.color = (1.0, 0.63, 0.39)
    fill.data.size = 6.0
    fill.rotation_euler = (Vector((0, 0, 1.4)) - fill.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = str(EVIDENCE / "roof_cool_key.png")
    bpy.ops.render.render(write_still=True)


def main():
    source_walls = assemble_test_house()
    module_kinds = {obj.get("caelm_native_module") for obj in source_walls}
    check({"2mW_3mH_doorway", "2mW_3mH_trimmed_window", "2mW_3mH_trimmed"} <= module_kinds,
          f"native fixture lacks door/window/trim modules: {module_kinds}")
    source_fingerprint = mesh_fingerprint(source_walls)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bearing = infer_bearing(source_walls, depsgraph=depsgraph)
    base = {"center": tuple(round(v, 5) for v in bearing.center),
            "width": round(bearing.width, 5), "depth": round(bearing.depth, 5),
            "angle": round(bearing.angle, 5)}
    check(abs(bearing.width - 6.0) < 0.03 and abs(bearing.depth - 4.0) < 0.03,
          f"bearing outline failed: {base}")

    # Exercise the same preview/generate operators exposed in the Blender panel.
    addon.register()
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj in source_walls:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = source_walls[0]
    props = bpy.context.scene.caelm_roof_settings
    props.material_directory = str(MATDIR)
    props.rise, props.detail, props.seed = 2.4, 50, 17
    # An incomplete selection must invalidate any stale preview and refuse generation.
    for obj in source_walls:
        obj.select_set(obj.get("caelm_native_module") != "2mW_3mH_trimmed")
    bpy.context.view_layer.objects.active = source_walls[0]
    try:
        missing_result = bpy.ops.caelmor.roof_preview(infer=True)
    except RuntimeError as error:
        check("all four sides" in str(error), f"unexpected incomplete-selection failure: {error}")
        missing_result = {"CANCELLED"}
    check(missing_result == {"CANCELLED"}, "roof preview accepted an incomplete wall selection")
    check(not props.ready, "failed preview kept a stale valid bearing")
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj in source_walls:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = source_walls[0]
    check(bpy.ops.caelmor.roof_preview(infer=True) == {"FINISHED"},
          "roof preview operator failed on selected native wall kit")
    check(props.ready and abs(props.width-6.0) < .03 and abs(props.depth-4.0) < .03,
          "roof preview operator did not publish the expected bearing")
    check(bpy.ops.caelmor.roof_generate() == {"FINISHED"},
          "roof generate operator failed")
    operator_collection = props.target
    check(operator_collection and operator_collection.get("caelm_roof_triangles", 0) > 0,
          "roof operator did not create a tagged collection")

    rows = []
    collections = []
    for rise in (1.8, 3.0):
        for detail in (0, 50, 100):
            collection = build_roof_collection(bpy.context.scene, bearing, rise=rise,
                detail=detail, material_directory=str(MATDIR), seed=17)
            collections.append(collection)
            check(mesh_fingerprint(source_walls) == source_fingerprint,
                  "roof generation changed source wall mesh data")
            check(collection.get("caelm_roof_triangles", 0) > 0, "missing roof triangle count")
            roofs = [obj for obj in collection.objects if obj.type == "MESH"]
            check(roofs, "roof collection has no mesh parts")
            field_uv = assert_field_uv(collection, rise, detail, bearing)
            uv_summaries = []
            for obj in roofs:
                check(len(obj.data.uv_layers) > 0, f"{obj.name}: no roof UV layer")
                layer = obj.data.uv_layers.get("RoofUV") or obj.data.uv_layers.active
                check(layer is not None, f"{obj.name}: no active roof UV map")
                uv_summaries.append((obj.name, layer.name, len(layer.data)))
                check(all(math.isfinite(value) for loop in layer.data for value in loop.uv),
                      f"{obj.name}: non-finite UV coordinate")
                # Every rendered face must occupy UV area, and UV loop count
                # must align exactly with Blender's mesh loop order.
                check(len(layer.data) == len(obj.data.loops), f"{obj.name}: UV loops are misaligned")
                for poly in obj.data.polygons:
                    coords = [layer.data[li].uv for li in poly.loop_indices]
                    signed_area = sum(a.x*b.y-b.x*a.y
                        for a, b in zip(coords, coords[1:]+coords[:1])) * 0.5
                    check(abs(signed_area) > 1e-10, f"{obj.name}: degenerate mapped face {poly.index}")
            rows.append({"rise": rise, "detail": detail,
                "triangles": int(collection["caelm_roof_triangles"]),
                "mesh_parts": len(roofs), "uv_layers": uv_summaries,
                "field_uv_alignment": field_uv,
                "native_walls_unchanged": True, "bearing": base})

    # Increasing detail has strictly increasing physical eave-course geometry.
    for rise in (1.8, 3.0):
        counts = [row["triangles"] for row in rows if row["rise"] == rise]
        check(counts[0] < counts[1] < counts[2], f"detail geometry counts did not rise: {rise} {counts}")
        case_collections = [collections[index] for index, row in enumerate(rows) if row["rise"] == rise]
        standard_bounds = roof_bounds(case_collections[0])
        for collection in case_collections[1:]:
            bounds = roof_bounds(collection)
            check(all(abs(bounds[axis][edge]-standard_bounds[axis][edge]) < .002
                      for axis in range(3) for edge in range(2)),
                  f"detail changed roof outer bounds at rise {rise}: {standard_bounds} vs {bounds}")

    # Repeat build into an owned collection and confirm deterministic cleanup.
    target = collections[0]
    initial = mesh_fingerprint([o for o in target.objects if o.type == "MESH"])
    again = build_roof_collection(bpy.context.scene, bearing, rise=1.8, detail=0,
        material_directory=str(MATDIR), seed=17, collection=target)
    regenerated = [o for o in again.objects if o.type == "MESH"]
    check(mesh_fingerprint(regenerated) == initial, "repeat generation is not deterministic")
    check(len(regenerated) == len({o.name for o in regenerated}), "duplicate roof objects after cleanup")

    # Export the most detailed tall roof, reimport, and check mesh topology, normals,
    # UVs and material slots survived the glTF round trip.
    export_collection = collections[-1]
    glb = EVIDENCE / "native_wallkit_roof.glb"
    bpy.ops.object.select_all(action="DESELECT")
    for obj in export_collection.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = next(o for o in export_collection.objects if o.type == "MESH")
    props.target = export_collection
    check(bpy.ops.caelmor.roof_export(filepath=str(glb)) == {"FINISHED"},
          "roof export operator failed")
    binary = glb.read_bytes()
    json_length = struct.unpack_from("<I", binary, 12)[0]
    gltf = json.loads(binary[20:20+json_length].decode("utf-8").rstrip(" \t\r\n\0"))
    field_materials = [m for m in gltf.get("materials", []) if m.get("name") == "Brookoak Roof Field"]
    check(field_materials, "GLB has no Brookoak Roof Field material")
    field_pbr = field_materials[0].get("pbrMetallicRoughness", {})
    check(field_pbr.get("baseColorTexture") and field_materials[0].get("normalTexture") and
          field_pbr.get("metallicRoughnessTexture"), "GLB lost Brookoak base color/normal/roughness maps")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    imported = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    check(imported, "GLB import has no mesh geometry")
    check(all(len(o.data.polygons) for o in imported), "GLB import lost mesh polygons")
    check(all(len(o.data.uv_layers) for o in imported), "GLB import lost UV maps")
    check(all(len(o.data.materials) for o in imported), "GLB import lost material maps")
    check(all(all(math.isfinite(n) for p in o.data.polygons for n in p.normal) for o in imported),
          "GLB import has invalid normals")
    primitive_attributes = [primitive.get("attributes", {}) for mesh in gltf.get("meshes", [])
                            for primitive in mesh.get("primitives", [])]
    check(primitive_attributes and all("NORMAL" in attributes for attributes in primitive_attributes),
          "GLB primitives are missing exported normals")
    check(all(any(key.startswith("TEXCOORD_") for key in attributes) for attributes in primitive_attributes),
          "GLB primitives are missing exported UV attributes")
    exported = {"mesh_count": len(imported), "faces": sum(len(o.data.polygons) for o in imported),
        "uv_maps": sum(len(o.data.uv_layers) for o in imported),
        "material_slots": sum(len(o.data.materials) for o in imported),
        "field_maps": ["baseColorTexture", "normalTexture", "metallicRoughnessTexture"],
        "normals_exported": True,
        "sha256": hashlib.sha256(glb.read_bytes()).hexdigest()}

    # Rebuild scene for two lighting renders after round-trip checks.
    source_walls = assemble_test_house()
    bearing = infer_bearing(source_walls, depsgraph=bpy.context.evaluated_depsgraph_get())
    showcase = build_roof_collection(bpy.context.scene, bearing, rise=2.4, detail=50,
        material_directory=str(MATDIR), seed=17)
    render_pair(showcase)

    report = {"blender": bpy.app.version_string, "fixture": "6x4m authored Lowmark kit",
        "wall_modules": "wood_trimmed_plaster 2m; front door; east trimmed window",
        "cases": rows, "operator_preview_generate": True,
        "repeat_cleanup_deterministic": True, "glb_roundtrip": exported,
        "renders": ["roof_warm_key.png", "roof_cool_key.png"]}
    (EVIDENCE / "roof_autocomplete_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("ROOF_AUTOCOMPLETE_BLENDER_PASS", json.dumps({"cases": len(rows), "glb": exported}))


if __name__ == "__main__":
    main()
