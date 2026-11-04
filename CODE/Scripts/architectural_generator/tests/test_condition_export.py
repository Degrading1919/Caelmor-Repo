"""Native Blender integration check for the v10 surface/condition GLB contract.

Run with Blender's Python, for example:
  blender --background --python tests/test_condition_export.py

This intentionally validates material bindings, image payloads, atlas/detail UVs and
reimported node links independently of the geometry hash.
"""
import hashlib
import json
import math
import os
import struct
import sys
import tempfile
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.blender_backend import TAG, COLLECTION_TAG, SETTINGS_KEY, build, export_building
from caelmor_architecture.engine import generate, geometry_hash
from caelmor_architecture.model import Settings
from caelmor_architecture.surface_atlas import ATLAS_REVISION

OUT = ROOT / "evidence" / os.environ.get("CAELM_CONDITION_OUTPUT", "polish_v10")


def read_glb(path):
    data = Path(path).read_bytes()
    assert data[:4] == b"glTF", f"Not a GLB: {path}"
    doc, binary = None, b""
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
    assert doc is not None, "GLB JSON chunk missing"
    return doc, binary


def accessor_values(doc, binary, index):
    acc = doc["accessors"][index]
    view = doc["bufferViews"][acc["bufferView"]]
    fmt, size = {5126: ("f", 4), 5123: ("H", 2), 5121: ("B", 1)}[acc["componentType"]]
    width = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[acc["type"]]
    start = view.get("byteOffset", 0) + acc.get("byteOffset", 0)
    stride = view.get("byteStride", width * size)
    scale = 1.0 / (255 if acc["componentType"] == 5121 and acc.get("normalized") else
                   65535 if acc["componentType"] == 5123 and acc.get("normalized") else 1.0)
    return [tuple(v * scale for v in struct.unpack_from("<" + fmt * width, binary, start + i * stride))
            for i in range(acc["count"])]


def match_uv_values(exported, native_layer, tolerance=2e-6):
    """Return unmatched exports and the largest actual native-coordinate delta."""
    buckets = {}
    for loop in native_layer.data:
        uv = (float(loop.uv.x), float(loop.uv.y))
        cell = (math.floor(uv[0] / tolerance), math.floor(uv[1] / tolerance))
        buckets.setdefault(cell, []).append(uv)
    unexpected = []
    max_delta = 0.0
    for u, v in set(exported):
        cell = (math.floor(u / tolerance), math.floor(v / tolerance))
        best = None
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for nu, nv in buckets.get((cell[0] + dx, cell[1] + dy), ()):
                    delta = max(abs(u - nu), abs(v - nv))
                    if best is None or delta < best:
                        best = delta
        if best is None or best > tolerance:
            unexpected.append((u, v))
        elif best > max_delta:
            max_delta = best
    return unexpected, max_delta


def image_payload(doc, binary, image):
    view = doc["bufferViews"][image["bufferView"]]
    start = view.get("byteOffset", 0)
    return binary[start:start + view["byteLength"]]


def texcoord(texture_info):
    # glTF's omitted texCoord means TEXCOORD_0.
    return texture_info.get("texCoord", 0)


def shader(material):
    return next((n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None) if material.use_nodes else None


def linked_image(material, socket_name):
    if not material.use_nodes:
        return None
    target = shader(material)
    if not target:
        return None
    socket = target.inputs.get(socket_name)
    if not socket or not socket.is_linked:
        return None
    pending = [link.from_node for link in socket.links]
    seen = set()
    while pending:
        node = pending.pop(0)
        if node.as_pointer() in seen:
            continue
        seen.add(node.as_pointer())
        if node.type == "TEX_IMAGE":
            return node.image
        pending.extend(link.from_node for input_socket in node.inputs for link in input_socket.links)
    return None


def linked_uv_layer(material, socket_name):
    """Return the UV Map node feeding the image bound to a shader input."""
    if not material.use_nodes:
        return None
    target = shader(material)
    socket = target.inputs.get(socket_name) if target else None
    if not socket or not socket.is_linked:
        return None
    pending = [link.from_node for link in socket.links]
    seen = set()
    image_node = None
    while pending:
        node = pending.pop(0)
        if node.as_pointer() in seen:
            continue
        seen.add(node.as_pointer())
        if node.type == "TEX_IMAGE":
            image_node = node
            break
        pending.extend(link.from_node for input_socket in node.inputs for link in input_socket.links)
    if image_node is None:
        return None
    pending = [link.from_node for link in image_node.inputs["Vector"].links]
    seen.clear()
    while pending:
        node = pending.pop(0)
        if node.as_pointer() in seen:
            continue
        seen.add(node.as_pointer())
        if node.type == "UVMAP":
            return node.uv_map
        pending.extend(link.from_node for input_socket in node.inputs for link in input_socket.links)
    return None


def pixel_signature(image):
    """Stable sampled 8-bit fingerprint, tolerant of PNG float conversion."""
    if not image or not image.size[0] or not image.size[1]:
        return None
    px = [0.0] * len(image.pixels)
    image.pixels.foreach_get(px)
    stride = max(4, (len(px) // 4096 // 4) * 4)
    data = bytearray()
    for i in range(0, len(px), stride):
        data.extend(max(0, min(255, round(px[i + channel] * 255))) for channel in range(min(4, len(px)-i)))
    return hashlib.sha256(struct.pack("<II", *image.size) + data).hexdigest()


def image_variation(image):
    px = [0.0] * len(image.pixels)
    image.pixels.foreach_get(px)
    return max(px[0::4]) - min(px[0::4]) if px else 0.0


def source_fingerprints():
    paths = (ROOT / "caelmor_architecture" / "surface_atlas.py",
             ROOT / "caelmor_architecture" / "surface_detail.py",
             ROOT / "caelmor_architecture" / "blender_backend.py",
             ROOT / "caelmor_architecture" / "surface_patterns.py",
             ROOT / "caelmor_architecture" / "surface_conditions.py")
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def atlas_state(collection):
    state = {}
    signature_cache = {}
    for obj in collection.objects:
        if not obj.get(TAG) or obj.type != "MESH" or obj.get("caelm_collider"):
            continue
        material = next((m for m in obj.data.materials
                         if m and m.get("caelm_atlas_revision") == ATLAS_REVISION), None)
        if not material:
            continue
        maps = {}
        for socket_name in ("Base Color", "Normal", "Roughness"):
            image = linked_image(material, socket_name)
            if image:
                if image.name not in signature_cache:
                    signature_cache[image.name] = pixel_signature(image)
                maps[socket_name] = signature_cache[image.name]
        state[obj.get("caelm_buffer_id")] = (material.get("caelm_surface_fingerprint"), maps)
    return state


def family_fingerprints(collection, layer=None):
    out = set()
    for obj in collection.objects:
        if not obj.get(TAG) or obj.type != "MESH" or obj.get("caelm_collider"):
            continue
        if layer is not None and obj.get("caelm_layer") != layer:
            continue
        for material in obj.data.materials:
            if material and material.get("caelm_atlas_revision") == ATLAS_REVISION:
                out.add((material.get("caelm_material"), material.get("caelm_surface_fingerprint")))
    return out


def sample_image_rgb(image, uv, pixel_cache):
    width, height = image.size
    if image.name not in pixel_cache:
        pixels = [0.0] * len(image.pixels)
        image.pixels.foreach_get(pixels)
        pixel_cache[image.name] = pixels
    pixels = pixel_cache[image.name]
    x = max(0.0, min(width - 1.0, uv[0] * width - .5))
    y = max(0.0, min(height - 1.0, uv[1] * height - .5))
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    x1, y1 = min(width - 1, x0 + 1), min(height - 1, y0 + 1)
    fx, fy = x - x0, y - y0
    values = []
    for channel in range(3):
        def value(px, py):
            return pixels[(py * width + px) * 4 + channel]
        top = value(x0, y0) * (1.0 - fx) + value(x1, y0) * fx
        bottom = value(x0, y1) * (1.0 - fx) + value(x1, y1) * fx
        values.append(top * (1.0 - fy) + bottom * fy)
    return tuple(values)


def roof_surface_samples(collection):
    samples = {}
    pixel_cache = {}
    for obj in collection.objects:
        if (not obj.get(TAG) or obj.type != "MESH" or obj.get("caelm_collider")
                or obj.get("caelm_layer") != "roof"):
            continue
        assert ("UV2_Surface" in obj.data.uv_layers and "UV3_Detail" in obj.data.uv_layers
                and obj.data.materials)
        material = obj.data.materials[0]
        assert material and material.get("caelm_atlas_revision") == ATLAS_REVISION
        images = {role: linked_image(material, socket) for role, socket in
                  (("albedo", "Base Color"), ("normal", "Normal"), ("orm", "Roughness"))}
        assert all(images.values()), f"{obj.name} has incomplete atlas texture links"
        polygons = list(obj.data.polygons)
        chosen = sorted(set((0, len(polygons) // 2, len(polygons) - 1)))
        mesh_samples = []
        for polygon_index in chosen:
            polygon = polygons[polygon_index]
            sampled = {}
            for role, image in images.items():
                socket = {"albedo": "Base Color", "normal": "Normal", "orm": "Roughness"}[role]
                layer_name = linked_uv_layer(material, socket)
                assert layer_name in obj.data.uv_layers, f"{obj.name} missing {layer_name} for {role}"
                layer = obj.data.uv_layers[layer_name]
                uv = tuple(sum(layer.data[loop].uv[axis] for loop in polygon.loop_indices) /
                           len(polygon.loop_indices) for axis in (0, 1))
                sampled[role] = sample_image_rgb(image, uv, pixel_cache)
            mesh_samples.append(sampled)
        samples[obj["caelm_buffer_id"]] = mesh_samples
    return samples


def compare_roof_samples(before, after, tolerance=.04):
    assert before and before.keys() == after.keys(), \
        f"Roof semantic mesh set changed: before={len(before)} after={len(after)}"
    checked, max_error = 0, 0.0
    for buffer_id, samples in before.items():
        assert len(samples) == len(after[buffer_id]), buffer_id
        for left, right in zip(samples, after[buffer_id]):
            for role in ("albedo", "normal", "orm"):
                assert role in left and role in right, f"{buffer_id} missing {role} sample"
                for a, b in zip(left[role], right[role]):
                    error = abs(a - b)
                    max_error = max(max_error, error)
                    assert error <= tolerance, \
                        f"{buffer_id} {role} sample changed by {error:.5f} after roof-only repack"
                    checked += 1
    return checked, max_error


def check_protected_hearth_context(collection, settings):
    hearths = [o for o in collection.objects if o.get(TAG) and o.type == "MESH"
               and "hearth_firebed" in str(o.get("caelm_buffer_id", ""))]
    assert len(hearths) == 1, f"Expected one hearth_firebed buffer, got {len(hearths)}"
    hearth = hearths[0]
    assert hearth.get("caelm_functional_role") == "forge_fire"
    before_full = family_fingerprints(collection)
    roof_stone_before = {entry for entry in before_full
                         if entry[0] in ("roof", "roof_dark", "roof_worn", "roof_patch",
                                         "stone", "stone_light", "stone_sooted")}
    assert roof_stone_before
    hearth["caelm_protected"] = True
    build(settings, collection=collection)
    assert any(o is hearth for o in collection.objects), "Protected hearth was replaced during full regeneration"
    after_full = family_fingerprints(collection)
    roof_stone_after = {entry for entry in after_full
                        if entry[0] in ("roof", "roof_dark", "roof_worn", "roof_patch",
                                        "stone", "stone_light", "stone_sooted")}
    assert roof_stone_after == roof_stone_before, \
        "Retained hearth context changed roof/stone atlases during full regeneration"
    hearth["caelm_protected"] = False
    roof_before_scope = roof_surface_samples(collection)
    build(settings, collection=collection, layers="ROOF")
    assert any(o is hearth and not o.get("caelm_protected") for o in collection.objects), \
        "Roof-only regeneration lost its unprotected heat-context source"
    roof_after_scope = roof_surface_samples(collection)
    sample_count, max_sample_error = compare_roof_samples(roof_before_scope, roof_after_scope)
    roof_objects = [o for o in collection.objects if o.get(TAG) and o.get("caelm_layer") == "roof"
                    and o.type == "MESH" and not o.get("caelm_collider")]
    assert roof_objects and all("UV2_Surface" in o.data.uv_layers and o.data.materials
                                and o.data.materials[0].get("caelm_atlas_revision") == ATLAS_REVISION
                                for o in roof_objects), "Roof-only regeneration left invalid atlas meshes"
    return {"protected_hearth_retained_on_full_regeneration": True,
            "roof_stone_fingerprints_unchanged": True,
            "roof_only_regeneration_retained_heat_context": True,
            "roof_only_atlas_materials_valid": True,
            "roof_only_albedo_normal_orm_samples_checked": sample_count,
            "roof_only_max_sample_error": max_sample_error}


def check_protection_and_regeneration(collection, settings, original_hash, legacy=None, legacy_color=None):
    candidates = [o for o in collection.objects if o.get(TAG) and o.type == "MESH"
                  and not o.get("caelm_collider") and o.data.materials
                  and o.data.materials[0]
                  and o.data.materials[0].get("caelm_atlas_revision") == ATLAS_REVISION]
    assert candidates
    mesh = candidates[0]
    buffer_id = mesh["caelm_buffer_id"]
    original_vertex = tuple(mesh.data.vertices[0].co)
    expected_state = atlas_state(collection)
    cached_material = next(m for m in mesh.data.materials
                           if m and m.get("caelm_atlas_revision") == ATLAS_REVISION)
    cached_fingerprint = cached_material.get("caelm_surface_fingerprint")
    normal_node = next(n for n in cached_material.node_tree.nodes if n.type == "NORMAL_MAP")
    original_strength = float(normal_node.inputs["Strength"].default_value)
    material_pointer = cached_material.as_pointer()
    normal_node.inputs["Strength"].default_value = .73
    override = bpy.data.materials.new("Validation Manual Material Override")
    override_name = override.name
    override.use_nodes = True
    override["caelm_user_override"] = True
    mesh.data.materials[0] = override
    mesh["caelm_protected"] = True
    mesh.data.vertices[0].co.x += .013
    edited = tuple(mesh.data.vertices[0].co)
    build(settings, collection=collection)
    retained = next(o for o in collection.objects if o.get("caelm_buffer_id") == buffer_id)
    assert retained is mesh and tuple(mesh.data.vertices[0].co) == edited
    assert mesh.data.materials[0] is override, "Protected user's material override changed"
    mesh["caelm_protected"] = False
    build(settings, collection=collection)
    rebuilt = next(o for o in collection.objects if o.get("caelm_buffer_id") == buffer_id)
    assert rebuilt is not mesh and tuple(rebuilt.data.vertices[0].co) == original_vertex
    assert rebuilt.data.materials[0] is override, "Regeneration lost explicit material override"
    assert collection.get("caelm_geometry_hash") == original_hash
    reattached = next(m for m in bpy.data.materials
                      if m.get("caelm_surface_fingerprint") == cached_fingerprint)
    reattached_normal = next(n for n in reattached.node_tree.nodes if n.type == "NORMAL_MAP")
    assert reattached.as_pointer() == material_pointer, "Identical regeneration replaced the cached material"
    assert abs(reattached_normal.inputs["Strength"].default_value - .73) < 1e-6, \
        "Identical regeneration lost a cached shader node edit"
    reattached_normal.inputs["Strength"].default_value = original_strength
    after = atlas_state(collection)
    for key, value in expected_state.items():
        if key == buffer_id:
            continue  # This semantic object now has the deliberate user override.
        assert after.get(key) == value, f"Atlas changed on deterministic regeneration for {key}"
    context_report = check_protected_hearth_context(collection, settings)
    if legacy:
        assert all(abs(a-b) < 1e-6 for a, b in zip(shader(legacy).inputs["Base Color"].default_value, legacy_color)), \
            "Legacy manual material changed during atlas rebuild"
    # Save and reopen only a temporary validation scene. This file is not used
    # as an exported product artifact and does not alter production evidence.
    expected_settings = json.loads(collection[SETTINGS_KEY])
    with tempfile.TemporaryDirectory(prefix="caelmor_surface_reopen_") as folder:
        saved = Path(folder) / "surface_validation.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(saved))
        bpy.ops.wm.open_mainfile(filepath=str(saved))
        reopened = next(c for c in bpy.data.collections if c.get(COLLECTION_TAG)
                        and c.get("caelm_geometry_hash") == original_hash)
        assert json.loads(reopened[SETTINGS_KEY]) == expected_settings
        reopened_override = next(o for o in reopened.objects if o.get("caelm_buffer_id") == buffer_id)
        assert reopened_override.data.materials[0].name == override_name
        reopened_meshes = [o for o in reopened.objects if o.get(TAG) and o.type == "MESH"
                           and not o.get("caelm_collider")]
        atlas_meshes = [o for o in reopened_meshes if any(
            m and m.get("caelm_atlas_revision") == ATLAS_REVISION
                                                          for m in o.data.materials)]
        assert atlas_meshes and all("UV0_Metric" in o.data.uv_layers
                                    and "UV1_Lightmap" in o.data.uv_layers
                                    and "UV2_Surface" in o.data.uv_layers
                                    and "UV3_Detail" in o.data.uv_layers for o in atlas_meshes)
        packed_atlas_images = [image for image in bpy.data.images
                               if image.get("caelm_atlas_revision") == ATLAS_REVISION]
        assert packed_atlas_images and all(image.packed_file is not None for image in packed_atlas_images)
        reopened_material = next(m for m in bpy.data.materials
                                 if m.get("caelm_surface_fingerprint") == cached_fingerprint)
        reopened_normal = next(n for n in reopened_material.node_tree.nodes if n.type == "NORMAL_MAP")
        assert abs(reopened_normal.inputs["Strength"].default_value - original_strength) < 1e-6
    return {"protected_geometry_edit_retained": True, "material_override_retained": True,
            "unprotected_geometry_restored": True, "cached_shader_edit_survived_regeneration": True,
            "remaining_atlas_maps_deterministic": True, **context_report,
            "saved_scene_reopened_with_packed_images_and_uvs": True}


def assert_source_surface_uv(objects, glb_doc, binary, atlas_material_names):
    """Check each exported map accessor against its native UV Map node."""
    native_by_name = {o.name + "Mesh": o for o in objects if o.type == "MESH"}
    checked, max_delta = 0, 0.0
    for mesh in glb_doc.get("meshes", []):
        source = native_by_name.get(mesh.get("name"))
        if source is None or "UV2_Surface" not in source.data.uv_layers:
            continue
        for primitive in mesh.get("primitives", []):
            material_index = primitive.get("material")
            if material_index is None or glb_doc["materials"][material_index].get("name") not in atlas_material_names:
                continue  # Includes intentionally untextured glass.
            material = glb_doc["materials"][material_index]
            source_material = bpy.data.materials.get(material.get("name", ""))
            assert source_material, f"Missing native material {material.get('name')}"
            pbr = material.get("pbrMetallicRoughness", {})
            texture_infos = {
                "Base Color": pbr.get("baseColorTexture"),
                "Normal": material.get("normalTexture"),
                "Roughness": pbr.get("metallicRoughnessTexture"),
            }
            for socket_name, info in texture_infos.items():
                if info is None:
                    continue
                layer_name = linked_uv_layer(source_material, socket_name)
                assert layer_name and layer_name in source.data.uv_layers, \
                    f"{material.get('name')} {socket_name} lacks a native UV Map binding"
                uv_set = texcoord(info)
                attr = primitive.get("attributes", {}).get(f"TEXCOORD_{uv_set}")
                assert attr is not None, f"{mesh.get('name')} lacks material-bound TEXCOORD_{uv_set}"
                exported = accessor_values(glb_doc, binary, attr)
                layer = source.data.uv_layers[layer_name]
                native_layer = layer
                # glTF export reverses V. Compare with a tight float tolerance,
                # since float32 serialization can straddle a decimal rounding edge.
                flipped = [(u, 1.0 - v) for u, v in exported]
                unexpected, uv_delta = match_uv_values(flipped, native_layer)
                max_delta = max(max_delta, uv_delta)
                assert not unexpected, \
                    (f"{mesh.get('name')} {socket_name} TEXCOORD_{uv_set} differs from native {layer_name}; "
                     f"unexpected={sorted(unexpected)[:5]}")
                assert all(math.isfinite(c) for uv in exported for c in uv)
                checked += len(exported)
    assert checked, "No material-bound native UV values were compared to exported UVs"
    return checked, max_delta


def assert_glb_materials(doc, binary):
    textures, images = doc.get("textures", []), doc.get("images", [])
    assert images and all("bufferView" in im for im in images), "GLB images must be embedded"
    payloads = [image_payload(doc, binary, im) for im in images]
    assert all(payload.startswith(b"\x89PNG\r\n\x1a\n") for payload in payloads), "Embedded atlas image is not PNG"
    png_hashes = [hashlib.sha256(payload).hexdigest() for payload in payloads]
    mats = doc.get("materials", [])
    assert mats, "No exported materials"
    bound = {"base": 0, "normal": 0, "orm": 0}
    checked = []
    for mat in mats:
        pbr = mat.get("pbrMetallicRoughness", {})
        base = pbr.get("baseColorTexture")
        normal = mat.get("normalTexture")
        orm = pbr.get("metallicRoughnessTexture")
        # Materials with the v10 hybrid contract bind all three surface maps.
        if not (base or normal or orm):
            continue
        assert base and normal and orm, f"{mat.get('name')} is missing a Base/Normal/ORM binding"
        for kind, info in (("base", base), ("normal", normal), ("orm", orm)):
            if kind == "orm":
                assert texcoord(info) == texcoord(base), \
                    f"{mat.get('name')} ORM must share the atlas UV set with albedo"
            ti = info["index"]
            assert 0 <= ti < len(textures)
            ii = textures[ti]["source"]
            assert 0 <= ii < len(images)
            bound[kind] += 1
        checked.append(mat.get("name", ""))
    assert checked, "No materials expose surface atlas maps"
    assert all(bound.values()), f"Missing map categories: {bound}"
    assert len(set(png_hashes)) > 1, "Embedded images are byte-identical; expected map variation"
    return {"materials_with_maps": len(checked), "map_bindings": bound,
            "embedded_image_count": len(images), "embedded_png_sha256": png_hashes}


def check_reimport(path, source_materials):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(path))
    imported = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    assert imported
    materials = {m.name: m for m in bpy.data.materials}
    checks, source_digests = 0, set()
    for name, original in source_materials.items():
        target = materials.get(name)
        if target is None:
            continue
        for socket_name in ("Base Color", "Normal", "Roughness", "Metallic"):
            src_image = original.get(socket_name)
            imported_image = linked_image(target, socket_name)
            if src_image is None:
                continue
            assert imported_image is not None, f"Reimport lost {socket_name} texture on {name}"
            sig = src_image["signature"]
            if sig:
                source_digests.add(sig)
                assert tuple(imported_image.size) == tuple(src_image["size"]), f"Image dimensions changed: {name}/{socket_name}"
                # Compare the actual pixels after decoding the embedded GLB image.
                imported_px = [0.0] * len(imported_image.pixels)
                imported_image.pixels.foreach_get(imported_px)
                assert len(imported_px) == src_image["pixel_count"]
                for i, value in src_image["samples"]:
                    assert abs(value - imported_px[i]) <= (2.1 / 255), \
                        f"Embedded image pixels differ from source: {name}/{socket_name} at {i}"
                checks += 1
    assert checks, "No source/reimported texture pixels could be compared"
    # Exporters reindex or omit unused UV layers. Require the layers actually
    # referenced by each reimported map rather than source layer ordinals.
    uv_meshes = []
    for obj in imported:
        for material in obj.data.materials:
            if not (material and linked_image(material, "Base Color")
                    and linked_image(material, "Normal")
                    and linked_image(material, "Roughness")):
                continue
            for socket_name in ("Base Color", "Normal", "Roughness"):
                layer_name = linked_uv_layer(material, socket_name)
                assert layer_name and layer_name in obj.data.uv_layers, \
                    f"Reimport lost {socket_name} UV binding on {obj.name}: {layer_name}"
            uv_meshes.append(obj)
            break
    assert uv_meshes, "No reimported surface meshes retained bound atlas/detail UV sets"
    return {"imported_meshes": len(imported), "meshes_with_surface_uvs": len(uv_meshes),
            "reimported_pixel_map_checks": checks,
            "distinct_source_pixel_signatures": len(source_digests)}


def run_case(function, region):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    legacy = None
    legacy_color = (.21, .32, .43, 1.0)
    if function == "SMITHY":
        legacy = bpy.data.materials.new("Caelmor | Stone")
        legacy.use_nodes = True
        legacy["caelm_material"] = "stone"
        legacy["caelm_surface_revision"] = 3
        shader(legacy).inputs["Base Color"].default_value = legacy_color
    settings = Settings(function=function, region=region, seed=91, world_aware=True,
                        use_grammar=True, detail="MEDIUM", geometry_mode="EFFICIENT",
                        crafted_curves=os.environ.get("CAELM_CRAFTED_CURVES") == "1",
                        seed_massing=os.environ.get("CAELM_SEED_MASSING") == "1")
    plan, buffers = generate(settings)
    expected = geometry_hash(buffers)
    collection, _ = build(settings)
    if legacy:
        assert all(abs(a-b) < 1e-6 for a, b in zip(shader(legacy).inputs["Base Color"].default_value, legacy_color))
    assert collection.get("caelm_geometry_hash") == expected
    meshes = [o for o in collection.objects if o.get(TAG) and o.type == "MESH" and not o.get("caelm_collider")]
    assert meshes
    atlas_material_names = {slot.material.name for obj in meshes for slot in obj.material_slots
                            if slot.material and slot.material.get("caelm_atlas_revision") == ATLAS_REVISION}
    assert atlas_material_names, "No atlas materials were assigned"
    source_materials = {}
    image_snapshots = {}
    ranges = {}
    for obj in meshes:
        for slot in obj.material_slots:
            material = slot.material
            if not material or material.name in source_materials:
                continue
            images = {}
            for socket_name in ("Base Color", "Normal", "Roughness", "Metallic"):
                image = linked_image(material, socket_name)
                if image:
                    snapshot = image_snapshots.get(image.name)
                    if snapshot is None:
                        pixels = [0.0] * len(image.pixels)
                        image.pixels.foreach_get(pixels)
                        stride = max(4, (len(pixels) // 2048 // 4) * 4)
                        snapshot = {"size": tuple(image.size), "pixel_count": len(pixels),
                                    "signature": pixel_signature(image),
                                    "samples": [(i, pixels[i]) for i in range(0, len(pixels), stride)]}
                        ranges[image.name] = [max(pixels[channel::4]) - min(pixels[channel::4])
                                              for channel in range(3)]
                        image_snapshots[image.name] = snapshot
                    images[socket_name] = snapshot
            source_materials[material.name] = images
    for obj in meshes:
        assert "UV0_Metric" in obj.data.uv_layers and "UV1_Lightmap" in obj.data.uv_layers
        has_atlas = any(slot.material and slot.material.get("caelm_atlas_revision") == ATLAS_REVISION
                        for slot in obj.material_slots)
        if has_atlas:
            assert "UV2_Surface" in obj.data.uv_layers and "UV3_Detail" in obj.data.uv_layers, \
                f"{obj.name} missing atlas/detail UV layers"
        if has_atlas and "CaelmorTint" in obj.data.color_attributes:
            values = [tuple(item.color) for item in obj.data.color_attributes["CaelmorTint"].data]
            assert all(abs(channel - 1.0) < 1e-6 for value in values for channel in value), \
                f"{obj.name} legacy tint was not neutralized for baked atlas maps"

    target = OUT / (function.lower() + ".glb")
    export_building(collection, str(target))
    doc, binary = read_glb(target)
    material_report = assert_glb_materials(doc, binary)
    uv_values, max_uv_delta = assert_source_surface_uv(meshes, doc, binary, atlas_material_names)
    # The old vertex tint is deliberately neutral for atlas materials; exporters
    # may omit the resulting all-white COLOR_0 stream.
    # Keep the actual generated PNG payloads beside the report for inspectable evidence.
    image_folder = OUT / (function.lower() + "_embedded_images")
    image_folder.mkdir(exist_ok=True)
    for i, image in enumerate(doc.get("images", [])):
        payload = image_payload(doc, binary, image)
        (image_folder / f"image_{i:03d}.png").write_bytes(payload)
    regeneration_report = {}
    if function == "SMITHY":
        regeneration_report = check_protection_and_regeneration(
            collection, settings, expected, legacy=legacy, legacy_color=legacy_color)
    color_range = max((max(value) for name, value in ranges.items() if name.endswith(" Color")), default=0.)
    orm_roughness_range = max((value[1] for name, value in ranges.items() if name.endswith(" ORM")), default=0.)
    orm_metallic_range = max((value[2] for name, value in ranges.items() if name.endswith(" ORM")), default=0.)
    assert color_range > .02, "Surface atlas albedo has no meaningful spatial variation"
    assert orm_roughness_range > .005, "Packed ORM roughness channel has no meaningful variation"
    reimport_report = check_reimport(target, source_materials)
    return {"function": function, "region": region, "geometry_hash": expected,
            "uv_bound_values_checked": uv_values, "max_uv_serialization_delta": max_uv_delta,
            "material_export": material_report, "reimport": reimport_report,
            "source_map_variation": {"albedo_rgb_max_range": color_range,
                                     "orm_roughness_g_range": orm_roughness_range,
                                     "orm_metallic_b_range": orm_metallic_range},
            "regeneration_protection_override": regeneration_report,
            "glb_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    initial_sources = source_fingerprints()
    cases = [run_case("SMITHY", "LOWMARK"), run_case("GATEHOUSE", "THORNFELL")]
    final_sources = source_fingerprints()
    assert final_sources == initial_sources, "Production source files changed during the validation run"
    report = {"blender": bpy.app.version_string, "source_sha256": initial_sources,
              "source_unchanged_during_run": True,
              "cases": cases}
    (OUT / "export_checks.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("CONDITION_EXPORT_PASS", json.dumps({
          "cases": len(cases),
          "geometry_hashes": [c["geometry_hash"] for c in cases],
          "fixtures": [{"function": c["function"],
                        "atlas_materials": c["material_export"]["materials_with_maps"],
                        "embedded_pngs": c["material_export"]["embedded_image_count"],
                        "uv_values_checked": c["uv_bound_values_checked"],
                        "reimported_pixel_map_checks": c["reimport"]["reimported_pixel_map_checks"],
                        "lifecycle_checks": c["regeneration_protection_override"]}
                       for c in cases]}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
