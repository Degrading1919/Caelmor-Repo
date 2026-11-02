"""Small Blender smoke check for authored surface maps and GLB export."""
import json
import struct
import sys
import tempfile
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.blender_backend import TAG, build, export_building
from caelmor_architecture.materials import PALETTE, SURFACE_REVISION, get_material
from caelmor_architecture.model import Settings


def read_glb_json(path):
    data = Path(path).read_bytes()
    offset = 12
    while offset + 8 <= len(data):
        size, kind = struct.unpack_from("<I4s", data, offset)
        offset += 8
        payload = data[offset:offset + size]
        offset += size
        if kind == b"JSON":
            doc = json.loads(payload.decode("utf-8").rstrip(" \t\r\n\x00"))
        elif kind == b"BIN\x00":
            binary = payload
    return doc, binary


def color_accessor_values(doc, binary, accessor_index):
    accessor = doc["accessors"][accessor_index]
    view = doc["bufferViews"][accessor["bufferView"]]
    comp = accessor["componentType"]
    fmt, unit = {5126: ("f", 4), 5123: ("H", 2), 5121: ("B", 1)}[comp]
    width = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[accessor["type"]]
    start = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    stride = view.get("byteStride", width * unit)
    scale = 1.0 / (255.0 if comp == 5121 and accessor.get("normalized") else 65535.0 if comp == 5123 and accessor.get("normalized") else 1.0)
    return [tuple(x * scale for x in struct.unpack_from("<" + fmt * width, binary, start + i * stride))
            for i in range(accessor["count"])]
    raise AssertionError("GLB JSON chunk missing")


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    legacy = bpy.data.materials.new("Caelmor | Plaster Patch")
    legacy.use_nodes = True
    legacy["caelm_material"] = "plaster_patch"
    legacy_shader = next(node for node in legacy.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    legacy_color = (.21, .32, .43, 1.0)
    legacy_shader.inputs["Base Color"].default_value = legacy_color
    revision_material = get_material("plaster_patch")
    assert revision_material is not legacy
    assert revision_material.name.endswith(f"[Surface{SURFACE_REVISION}]")
    assert all(abs(a-b) < 1e-6 for a, b in zip(legacy_shader.inputs["Base Color"].default_value, legacy_color))
    revised_shader = next(node for node in revision_material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    edited_color = (.31, .41, .51, 1.0)
    revised_shader.inputs["Base Color"].default_value = edited_color
    assert get_material("plaster_patch") is revision_material
    assert all(abs(a-b) < 1e-6 for a, b in zip(revised_shader.inputs["Base Color"].default_value, edited_color))
    revised_shader.inputs["Base Color"].default_value = PALETTE["plaster_patch"][0]
    revision_images = [image for image in bpy.data.images
                       if image.get("caelm_surface_revision") == SURFACE_REVISION]
    assert len(revision_images) == 3
    assert all(f"Surface{SURFACE_REVISION}" in image.name for image in revision_images)
    revised_materials = [material for material in bpy.data.materials
                         if material.get("caelm_material") == "plaster_patch"
                         and material.get("caelm_surface_revision") == SURFACE_REVISION]
    assert revised_materials == [revision_material]

    settings = Settings(seed=17, function="FARMHOUSE", footprint="L", detail="LOW")
    collection, _metrics = build(settings)
    meshes = [obj for obj in collection.objects if obj.get(TAG) and obj.type == "MESH"
              and not obj.get("caelm_collider")]
    assert meshes
    for obj in meshes:
        assert "UV0_Metric" in obj.data.uv_layers, obj.name
        assert "UV1_Lightmap" in obj.data.uv_layers, obj.name
        assert "CaelmorTint" in obj.data.color_attributes, obj.name
    for obj in meshes:
        if obj.get("caelm_material") in ("plaster", "stone", "stone_light", "roof"):
            attr = obj.data.color_attributes["CaelmorTint"].data
            values = [tuple(item.color) for item in attr]
            print(f"BLENDER_TINT {obj.name} material={obj.get('caelm_material')} min={tuple(min(v[i] for v in values) for i in range(4))} max={tuple(max(v[i] for v in values) for i in range(4))}", flush=True)
    for image in bpy.data.images:
        if image.get("caelm_surface_revision") != SURFACE_REVISION or not image.name.endswith(" Color"):
            continue
        family = image.name.replace("Caelmor Original ", "").split(" Surface")[0].lower()
        if family not in ("plaster", "stone"):
            continue
        pixels = [0.0] * (len(image.pixels))
        image.pixels.foreach_get(pixels)
        rgb = pixels[0::4]
        print(f"ALBEDO_RANGE {family} min={min(rgb):.5f} max={max(rgb):.5f}", flush=True)
    roof_patch_materials = [m for m in bpy.data.materials if m.get("caelm_material") == "roof_patch"]
    assert roof_patch_materials, "Roof patch material missing"
    roof_base = tuple(roof_patch_materials[0].node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value)
    assert all(abs(a-b) < 0.015 for a, b in zip(roof_base[:3], (.12, .125, .112))), roof_base
    with tempfile.TemporaryDirectory(prefix="caelmor_surface_smoke_") as tmp:
        glb = Path(tmp) / "smoke.glb"
        export_building(collection, str(glb))
        doc, binary = read_glb_json(glb)
        images = doc.get("images", [])
        assert len(images) >= 12, f"Expected packed color/normal/roughness maps, got {len(images)} images"
        assert all("bufferView" in image for image in images), "An image was not embedded"
        materials = doc.get("materials", [])
        assert any("normalTexture" in material for material in materials), "Normal maps were not exported"
        assert any("metallicRoughnessTexture" in material.get("pbrMetallicRoughness", {}) for material in materials), "Roughness maps were not exported"
        primitives = [p for mesh in doc.get("meshes", []) for p in mesh.get("primitives", [])]
        assert primitives
        assert all("COLOR_0" in p.get("attributes", {}) for p in primitives), "Weathering COLOR_0 missing"
        color_records = []
        for mesh in doc.get("meshes", []):
            for primitive in mesh.get("primitives", []):
                if "COLOR_0" not in primitive.get("attributes", {}):
                    continue
                idx = primitive["attributes"]["COLOR_0"]
                values = color_accessor_values(doc, binary, idx)
                mins = tuple(min(v[i] for v in values) for i in range(3))
                maxs = tuple(max(v[i] for v in values) for i in range(3))
                color_records.append((mesh.get("name"), mins, maxs, values))
        for name, mins, maxs, values in color_records:
            in_bounds = all(-1e-6 <= component <= 1.000001
                            for sample in values for component in sample)
            assert in_bounds, f"{name} COLOR_0 violates glTF normalized [0,1] bounds: {mins}–{maxs}"
        assert any(min(record[1]) < .99 for record in color_records), "COLOR_0 has no visible tint"
        assert any(max(record[2][i] - record[1][i] for i in range(3)) > .025
                   for record in color_records), "COLOR_0 contains no spatial weathering variation"
        for mesh in doc.get("meshes", []):
            for primitive in mesh.get("primitives", []):
                if "COLOR_0" not in primitive.get("attributes", {}):
                    continue
                material = materials[primitive.get("material", 0)].get("name", "")
                if material.endswith("Plaster") or material.endswith("Roof"):
                    record = next(row for row in color_records if row[0] == mesh.get("name"))
                    print(f"GLB_TINT {mesh.get('name')} material={material} min={record[1]} max={record[2]} samples={record[3][:2]}", flush=True)
        source_objects = {obj.name + "Mesh": obj for obj in meshes}
        for mesh_name in ("facade_wallsMesh", "Split oak shingle coursesMesh"):
            source = source_objects[mesh_name]
            raw = [tuple(item.color) for item in source.data.color_attributes["CaelmorTint"].data]
            source_min = tuple(min(v[i] for v in raw) for i in range(3))
            source_max = tuple(max(v[i] for v in raw) for i in range(3))
            exported = next(row for row in color_records if row[0] == mesh_name)
            assert all(-1e-6 <= component <= 1.000001 for value in raw for component in value), \
                f"{mesh_name} Blender tint violates normalized [0,1] bounds"
            for channel in range(3):
                assert abs(source_min[channel] - exported[1][channel]) < 1e-5
                assert abs(source_max[channel] - exported[2][channel]) < 1e-5
        colors = {tuple(round(v, 3) for v in p["pbrMetallicRoughness"].get("baseColorFactor", []))
                  for p in materials}
        assert len(colors) >= 4, f"Material palette has too few visible base color factors: {colors}"
        print(f"SURFACE_SMOKE_OK meshes={len(meshes)} materials={len(materials)} images={len(images)} colors={len(colors)} roof_patch={roof_base[:3]} legacy={legacy.name} revision={revision_material.name}", flush=True)


if __name__ == "__main__":
    main()
