"""Headless native-kit regression and evidence renders for roof autocomplete.

Run from the repository root with Blender 5.x:
  blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python CODE/Scripts/architectural_generator/tests/test_roof_autocomplete_blender.py

This uses the authored Lowmark wood_trimmed_plaster wall modules. It keeps the
door, window and original wall meshes in the scene while checking roof-only
generation, repeat cleanup, export, and lighting response.
"""
import hashlib
import json
import math
import struct
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.roof_selection import infer_bearing
from caelmor_architecture.roof_autocomplete import build_roof_collection, _roof_buffers
from caelmor_architecture.roof import roof_faces, roof_topology, roof_join_kind
from caelmor_architecture.geometry import area
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
        rows.append((len(mesh.vertices), len(mesh.polygons), coords, tuple(tuple(row) for row in obj.matrix_world)))
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
    slope = rise / (bearing.depth * .5)
    step = .30 / math.sqrt(1+slope*slope)
    covers = [o for o in collection.objects if o.data.uv_layers.get("RoofUV")]
    assert len(covers) == (1 if detail in (0,100) else 2)
    projected = 0.
    for obj in covers:
        uv = obj.data.uv_layers['RoofUV']
        projected += sum(area([tuple(obj.data.vertices[i].co[:2]) for i in face.vertices])
                         for face in obj.data.polygons)
        for loop in obj.data.loops:
            x,y,_ = obj.data.vertices[loop.vertex_index].co
            u,v = uv.data[loop.index].uv
            # Exposed vertical faces intentionally use a tiny inward inset.
            direction = 1 if y < -1e-6 else -1
            if abs(y)<1e-6 and abs(u-x/1.28)<.0031:
                direction = 1
            assert abs(u-direction*x/1.28) < .0031
            assert abs(v-(2.35-abs(y))/(step*8)) < .0031
    assert abs(projected-(6+.7)*(4+.7)) < .0005, (detail,projected)
    return {"repeat_courses":8,"pitch_alignment":True,"projected_m2":round(projected,5)}


def compound_fixture():
    source = KIT.parent/'test_scene.blend'
    if source.is_file():
        with bpy.data.libraries.load(str(source),link=False) as (available, target):
            names = ('Plane.006','Plane.020','Plane.017','Plane.001','Plane.002','Plane.003',
                     'Plane','Plane.004','Plane.010','Plane.008','Plane.009','Plane.005',
                     'Plane.018','Plane.019','Plane.012','Plane.016','Plane.007')
            target.objects = [n for n in available.objects if n in names]
        for obj in target.objects:
            bpy.context.scene.collection.objects.link(obj)
        try:
            infer_bearing(target.objects)
        except ValueError as error:
            assert 'Plane.010' in str(error) and 'Non-orthogonal' in str(error), str(error)
            diagnostic = str(error)
        else:
            raise AssertionError('Diagonal walls were accepted')
    else:
        diagnostic = 'Local test_scene.blend unavailable'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    walls = []
    points = [(-3,-2),(-1,-2),(-1,-4),(1,-4),(1,-2),(3,-2),(3,2),(-3,2)]
    for i,(a,b) in enumerate(zip(points,points[1:]+points[:1])):
        count = round(math.dist(a,b)/2)
        horizontal = a[1]==b[1]
        for j in range(count):
            f=(j+.5)/count
            center=(*(x+(y-x)*f for x,y in zip(a,b)),0)
            walls += append_module("2mW_3mH_trimmed.blend",center,math.pi/2 if horizontal else 0,f'wing_{i}')
    bearing=infer_bearing(walls)
    assert len(bearing.rects)==2
    roof=build_roof_collection(bpy.context.scene,bearing,rise=1.8,detail=50,material_directory=MATDIR)
    plan,_=_roof_buffers(bearing,1.8,50,.35,'AUTO',17)
    patches=roof_faces(plan)
    points,_,edges=roof_topology(patches)
    valleys=sum(roof_join_kind(points,patches,users)=='valley' for users in edges.values())
    assert valleys>=2
    assert any('valley flashing' in o.name for o in roof.objects)
    # The UI must save and reload both volumes, not just the bounding box.
    bpy.context.view_layer.update()
    for obj in walls:
        obj.select_set(True)
    assert bpy.ops.caelmor.roof_preview() == {'FINISHED'}
    props=bpy.context.scene.caelm_roof_settings
    assert len(json.loads(props.rects))==2
    props.rise=1.8
    props.material_directory=str(MATDIR)
    props.target=roof
    assert bpy.ops.caelmor.roof_load()=={'FINISHED'}
    assert bpy.ops.caelmor.roof_generate()=={'FINISHED'}
    assert len(json.loads(roof['caelm_roof_settings'])['rects'])==2
    scene=bpy.context.scene
    make_camera_and_lights(scene,0)
    camera=scene.camera
    camera.location=(-9.,-12.,9.)
    camera.rotation_euler=(Vector((0,-.5,2.))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.resolution_percentage=65
    scene.cycles.samples=10
    scene.render.filepath=str(EVIDENCE/'compound_wing.png')
    bpy.ops.render.render(write_still=True)
    return {"rectangles":bearing.rects,"valley_segments":valleys,"triangles":roof['caelm_roof_triangles'],
            "saved_test_scene_diagnostic":diagnostic,"render":"compound_wing.png"}


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


def main():
    source_walls = assemble_test_house()
    module_kinds = {obj.get("caelm_native_module") for obj in source_walls}
    check({"2mW_3mH_doorway", "2mW_3mH_trimmed_window", "2mW_3mH_trimmed"} <= module_kinds,
          f"native fixture lacks door/window/trim modules: {module_kinds}")
    bpy.context.view_layer.update()
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
        previous_shingles = set()
        for detail in (0, 25, 50, 75, 100):
            collection = build_roof_collection(bpy.context.scene, bearing, rise=rise,
                detail=detail, material_directory=str(MATDIR), seed=17)
            collections.append(collection)
            check(mesh_fingerprint(source_walls) == source_fingerprint,
                  "roof generation changed source wall mesh data")
            check(collection.get("caelm_roof_triangles", 0) > 0, "missing roof triangle count")
            roofs = [obj for obj in collection.objects if obj.type == "MESH"]
            check(roofs, "roof collection has no mesh parts")
            field_uv = assert_field_uv(collection, rise, detail, bearing)
            dimensional = [o for o in roofs if 'Dimensional Brookoak' in o.name]
            selected = {tuple(tuple(round(c,6) for c in obj.data.vertices[i].co) for i in face.vertices)
                        for obj in dimensional for face in obj.data.polygons if face.normal.z>.1}
            assert previous_shingles <= selected
            previous_shingles=selected
            modeled,total = (collection[key] for key in ('caelm_roof_shingles','caelm_roof_cover_units'))
            assert abs(modeled-total*detail/100)<=1
            assert bool(dimensional)==(detail>0)
            assert any('Mapped roof field' in o.name for o in roofs)==(detail<100)
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
                "mesh_parts": len(roofs), "modeled_shingles": modeled, "total_shingles": total,
                "uv_layers": uv_summaries,
                "field_uv_alignment": field_uv,
                "native_walls_unchanged": True, "bearing": base})

    # Increasing detail has strictly increasing physical eave-course geometry.
    for rise in (1.8, 3.0):
        counts = [row["triangles"] for row in rows if row["rise"] == rise]
        check(all(a<b for a,b in zip(counts,counts[1:])), f"detail geometry counts did not rise: {rise} {counts}")
        case_collections = [collections[index] for index, row in enumerate(rows) if row["rise"] == rise]
        standard_bounds = roof_bounds(case_collections[0])
        for collection in case_collections[1:]:
            bounds = roof_bounds(collection)
            check(all(abs(bounds[axis][edge]-standard_bounds[axis][edge]) < .002
                      for axis,edge in ((0,0),(0,1),(1,0),(1,1),(2,1))),
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
    for obj in imported:
        obj.data.calc_loop_triangles()
    assert sum(len(o.data.loop_triangles) for o in imported)==rows[-1]['triangles']
    exported = {"mesh_count": len(imported), "faces": sum(len(o.data.polygons) for o in imported),
        "uv_maps": sum(len(o.data.uv_layers) for o in imported),
        "material_slots": sum(len(o.data.materials) for o in imported),
        "field_maps": ["baseColorTexture", "normalTexture", "metallicRoughnessTexture"],
        "normals_exported": True,
        "sha256": hashlib.sha256(glb.read_bytes()).hexdigest()}

    compound = compound_fixture()
    source_walls = assemble_test_house()
    bearing = infer_bearing(source_walls, depsgraph=bpy.context.evaluated_depsgraph_get())
    scene=bpy.context.scene
    make_camera_and_lights(scene,0)
    scene.render.resolution_percentage=65
    scene.cycles.samples=10
    lights=[o for o in scene.objects if o.type=='LIGHT']
    showcase=None
    for key in ('warm','grazing'):
        if key=='grazing':
            for light in lights:
                light.location.z=4.5 if light.name=='EvidenceKey' else 5.4
                light.rotation_euler=(Vector((0,0,3.8))-light.location).to_track_quat('-Z','Y').to_euler()
        for percent in (0,50,100):
            showcase=build_roof_collection(scene,bearing,rise=2.4,detail=percent,
                material_directory=MATDIR,seed=17,collection=showcase)
            scene.render.filepath=str(EVIDENCE/f'{key}_{percent}.png')
            bpy.ops.render.render(write_still=True)

    report = {"blender": bpy.app.version_string, "fixture": "6x4m authored Lowmark kit",
        "wall_modules": "wood_trimmed_plaster 2m; front door; east trimmed window",
        "cases": rows, "compound": compound, "operator_preview_generate": True,
        "repeat_cleanup_deterministic": True, "glb_roundtrip": exported,
        "renders": [f"{key}_{n}.png" for key in ("warm","grazing") for n in (0,50,100)]}
    (EVIDENCE / "roof_autocomplete_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("ROOF_AUTOCOMPLETE_BLENDER_PASS", json.dumps({"cases": len(rows), "glb": exported}))


if __name__ == "__main__":
    main()
