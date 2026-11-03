"""Blender integration checks; run with Blender's background Python.

Example:
  blender --background --python tests/test_blender.py
"""

import json
import math
import os
import struct
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import caelmor_architecture as addon
from caelmor_architecture.blender_backend import (
    COLLECTION_TAG, SETTINGS_KEY, TAG, export_building,
)


def mesh_edge_counts(mesh):
    counts = Counter()
    for polygon in mesh.polygons:
        indices = list(polygon.vertices)
        for a, b in zip(indices, indices[1:] + indices[:1]):
            counts[tuple(sorted((a, b)))] += 1
    return counts


def mesh_signed_volume(mesh):
    volume = 0.0
    for polygon in mesh.polygons:
        indices = list(polygon.vertices)
        a = mesh.vertices[indices[0]].co
        for i in range(1, len(indices) - 1):
            b, c = mesh.vertices[indices[i]].co, mesh.vertices[indices[i + 1]].co
            volume += (a.x * (b.y * c.z - b.z * c.y)
                       + a.y * (b.z * c.x - b.x * c.z)
                       + a.z * (b.x * c.y - b.y * c.x)) / 6.0
    return volume


def glb_json(filepath):
    with open(filepath, "rb") as stream:
        data = stream.read()
    if data[:4] != b"glTF":
        raise AssertionError("Export is not a GLB container")
    offset = 12
    while offset + 8 <= len(data):
        length, kind = struct.unpack_from("<I4s", data, offset)
        offset += 8
        payload = data[offset:offset + length]
        offset += length
        if kind == b"JSON":
            return json.loads(payload.decode("utf-8").rstrip(" \t\r\n\x00"))
    raise AssertionError("GLB has no JSON chunk")


class BlenderIntegration(unittest.TestCase):
    def setUp(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        # Factory reset clears custom Scene RNA properties; register the add-on
        # after creating the fresh scene used by this fixture.
        addon.register()
        bpy.context.scene.caelmor_settings.caelm_seed = 73
        bpy.context.scene.caelmor_settings.caelm_function = "FARMHOUSE"
        bpy.context.scene.caelmor_settings.caelm_footprint = "L"
        bpy.context.scene.cursor.location = (2.0, 3.0, 0.0)

    def tearDown(self):
        addon.unregister()

    def _collection(self):
        return next(c for c in bpy.data.collections if c.get(COLLECTION_TAG))

    def test_operator_regeneration_export_roundtrip_and_saved_reopen(self):
        self.assertEqual(bpy.ops.caelmor.generate(), {"FINISHED"})
        collection = self._collection()
        anchor = next(o for o in collection.objects if o.get("caelm_anchor"))
        self.assertEqual(tuple(round(v, 4) for v in anchor.location), (2.0, 3.0, 0.0))
        generated = [o for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")]
        self.assertGreater(len(generated), 0)
        colliders = [o for o in collection.objects if o.get("caelm_collider")]
        self.assertGreater(len(colliders), 0)
        self.assertTrue(all(o.hide_render and o.get("caelm_semantic") == "collider" for o in colliders))
        for collider in colliders:
            self.assertTrue(all(count == 2 for count in mesh_edge_counts(collider.data).values()))
            self.assertGreater(mesh_signed_volume(collider.data), 0.0)
        self.assertTrue(all(o.parent == anchor for o in generated + colliders))

        # Protect and deliberately edit one generated buffer to exercise regen safety.
        protected_obj = next(o for o in generated if o.get("caelm_buffer_id") == "facade_walls")
        protected_id = protected_obj["caelm_buffer_id"]
        protected_obj.data.vertices[0].co.x += 0.17
        protected_obj.data.update()
        edited_vertex = tuple(protected_obj.data.vertices[0].co)
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        protected_obj.select_set(True)
        bpy.context.view_layer.objects.active = protected_obj
        self.assertEqual(bpy.ops.caelmor.protect_selected(), {"FINISHED"})
        self.assertTrue(protected_obj.get("caelm_protected"))

        for obj in generated:
            self.assertIsNotNone(obj.data)
            self.assertTrue(obj.data.materials)
            self.assertTrue(all(material is not None for material in obj.data.materials))
            self.assertIn("UV0_Metric", obj.data.uv_layers)
            self.assertIn("UV1_Lightmap", obj.data.uv_layers)
            self.assertEqual(obj.data.uv_layers.active.name, "UV0_Metric")
            self.assertTrue(obj.data.uv_layers["UV0_Metric"].active_render,
                            f"{obj.name}: UV0 active_render={obj.data.uv_layers['UV0_Metric'].active_render}, "
                            f"active_index={obj.data.uv_layers.active_index}, "
                            f"layers={[(uv.name, uv.active_render) for uv in obj.data.uv_layers]}")
            metric_uv = obj.data.uv_layers["UV0_Metric"]
            lightmap_uv = obj.data.uv_layers["UV1_Lightmap"]
            self.assertTrue(all(all(math.isfinite(coord) for coord in loop.uv) for loop in metric_uv.data))
            self.assertTrue(all(all(-1e-5 <= coord <= 1.00001 for coord in loop.uv)
                                for loop in lightmap_uv.data))
            self.assertTrue(obj.get("caelm_layer"))
            self.assertTrue(obj.get("caelm_semantic"))

        textured_families = set()
        for material in bpy.data.materials:
            if not material.get("caelm_texture_family"):
                continue
            images = [node.image for node in material.node_tree.nodes
                      if node.type == "TEX_IMAGE" and node.image is not None]
            self.assertGreaterEqual(len(images), 2)
            self.assertTrue(all(image.get("caelm_original") for image in images))
            self.assertTrue(all(image.packed_file is not None for image in images))
            textured_families.add(material["caelm_texture_family"])
        self.assertTrue({"wood", "roof", "stone", "plaster"}.issubset(textured_families))

        # A manually authored object inside the generated collection must survive.
        mesh = bpy.data.meshes.new("ManualMesh")
        manual = bpy.data.objects.new("ManualObject", mesh)
        collection.objects.link(manual)

        # Create a second build, then explicitly reactivate the first one before editing.
        bpy.context.scene.caelmor_settings.caelm_seed = 74
        bpy.context.scene.caelmor_settings.caelm_function = "BARN"
        self.assertEqual(bpy.ops.caelmor.generate(), {"FINISHED"})
        second = next(c for c in bpy.data.collections if c.get(COLLECTION_TAG) and c != collection)
        second_objects_before = [o for o in second.objects if o.get(TAG) and not o.get("caelm_collider")]
        self.assertGreater(len(second_objects_before), 0)
        bpy.context.scene.caelmor_settings.caelm_seed = 73
        bpy.context.scene.caelmor_settings.caelm_function = "FARMHOUSE"
        first_visual = next(o for o in collection.objects if o.get(TAG) and not o.get("caelm_collider"))
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        first_visual.select_set(True)
        bpy.context.view_layer.objects.active = first_visual
        anchor.location = (5.0, 6.0, 0.0)
        anchor.scale = (1.15, 1.15, 1.15)
        before_layers = {o.name: o.get("caelm_layer") for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")}
        self.assertEqual(bpy.ops.caelmor.regenerate(scope="ROOF"), {"FINISHED"})
        self.assertIn(manual, collection.objects[:])
        self.assertTrue(all(o.name in bpy.data.objects and o.name in second.objects for o in second_objects_before))
        self.assertEqual(tuple(round(v, 4) for v in anchor.location), (5.0, 6.0, 0.0))
        self.assertEqual(tuple(round(v, 4) for v in anchor.scale), (1.15, 1.15, 1.15))
        after_layers = {o.name: o.get("caelm_layer") for o in collection.objects if o.get(TAG) and not o.get("caelm_collider")}
        self.assertIn("roof", set(after_layers.values()))
        self.assertTrue({layer for layer in before_layers.values() if layer != "roof"}.issubset(set(after_layers.values())))

        # Full regeneration must also retain the edit exactly once.
        self.assertEqual(bpy.ops.caelmor.regenerate(scope="ALL"), {"FINISHED"})
        retained = [o for o in collection.objects
                    if o.get(TAG) and o.get("caelm_buffer_id") == protected_id]
        self.assertEqual(len(retained), 1)
        self.assertIs(retained[0], protected_obj)
        self.assertEqual(tuple(protected_obj.data.vertices[0].co), edited_vertex)

        with tempfile.TemporaryDirectory(prefix="caelmor_arch_") as tmp:
            filepath = os.path.join(tmp, "building.glb")
            sidecar = export_building(collection, filepath)
            self.assertTrue(os.path.isfile(filepath))
            self.assertTrue(os.path.isfile(sidecar))
            collision_path = os.path.join(tmp, "building.collision.glb")
            self.assertTrue(os.path.isfile(collision_path))
            with open(sidecar, encoding="utf-8") as stream:
                manifest = json.load(stream)
            self.assertEqual(manifest["format"], "CaelmorBuildingExport")
            self.assertTrue(manifest["source_geometry_hash"])
            self.assertTrue(manifest["layers"])
            self.assertGreater(manifest["collision"]["object_count"], 0)
            self.assertEqual(manifest["collision"]["file"], os.path.basename(collision_path))
            self.assertGreater(manifest["collision"]["wall_proxy_count"], 0)
            self.assertGreater(manifest["collision"]["floor_proxy_count"], 0)
            self.assertEqual(manifest["protected_buffer_count"], 1)
            self.assertTrue(manifest["has_protected_buffers"])
            self.assertEqual([round(v, 4) for v in manifest["anchor"]["location"]], [5.0, 6.0, 0.0])
            self.assertEqual([round(v, 4) for v in manifest["anchor"]["scale"]], [1.15, 1.15, 1.15])
            self.assertTrue(manifest["objects"])
            self.assertTrue(all(row.get("layer") and row.get("material") for row in manifest["objects"]))
            self.assertTrue(any(row.get("protected") for row in manifest["objects"]))
            gltf_json = glb_json(filepath)
            self.assertTrue(gltf_json.get("images"), "GLB has no embedded material images")
            self.assertTrue(all("bufferView" in image for image in gltf_json["images"]))
            pbr = [m.get("pbrMetallicRoughness", {}) for m in gltf_json.get("materials", [])]
            base_factors = {tuple(p.get("baseColorFactor", ())) for p in pbr}
            self.assertGreaterEqual(len(base_factors), 3, "Palette tint did not vary GLB baseColorFactor across material families")
            normal_textures = [m["normalTexture"] for m in gltf_json.get("materials", [])
                               if m.get("normalTexture")]
            self.assertTrue(normal_textures, "GLB has no exported normal maps")
            self.assertTrue(all(n.get("texCoord", 0) == 0 for n in normal_textures))
            for mesh in gltf_json.get("meshes", []):
                for primitive in mesh.get("primitives", []):
                    attrs = primitive.get("attributes", {})
                    self.assertIn("TEXCOORD_0", attrs)
                    self.assertIn("TEXCOORD_1", attrs)

            # Exercise Blender's glTF importer when available, then check imported UVs.
            importer = getattr(bpy.ops.import_scene, "gltf", None)
            if importer is None:
                self.skipTest("Blender glTF importer is unavailable")
            imported_before = set(bpy.data.objects)
            importer(filepath=filepath)
            imported = [o for o in bpy.data.objects if o not in imported_before and o.type == "MESH"]
            self.assertTrue(imported, "GLB reimport produced no mesh objects")
            for obj in imported:
                self.assertGreaterEqual(len(obj.data.uv_layers), 1)
                self.assertTrue(all(material is not None for material in obj.data.materials))

            saved = os.path.join(tmp, "reopen.blend")
            bpy.ops.wm.save_as_mainfile(filepath=saved)
            bpy.ops.wm.open_mainfile(filepath=saved)
            reopened = next(c for c in bpy.data.collections if c.get(COLLECTION_TAG))
            self.assertTrue(reopened.get(SETTINGS_KEY))
            self.assertTrue(any(o.get(TAG) for o in reopened.objects))
            self.assertTrue(any(o.name == "ManualObject" for o in reopened.objects))
            self.assertEqual(sum(1 for c in bpy.data.collections if c.get(COLLECTION_TAG)), 2)
            reopened_protected = [o for o in reopened.objects
                                  if o.get(TAG) and o.get("caelm_protected")]
            self.assertEqual(len(reopened_protected), 1)
            reopened_obj = reopened_protected[0]
            reopened_id = reopened_obj["caelm_buffer_id"]
            reopened_vertex = tuple(reopened_obj.data.vertices[0].co)
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
            reopened_obj.select_set(True)
            bpy.context.view_layer.objects.active = reopened_obj
            self.assertEqual(bpy.ops.caelmor.protect_selected(), {"FINISHED"})
            self.assertFalse(reopened_obj.get("caelm_protected"))
            self.assertEqual(bpy.ops.caelmor.regenerate(scope="ALL"), {"FINISHED"})
            replacements = [o for o in reopened.objects
                            if o.get(TAG) and o.get("caelm_buffer_id") == reopened_id]
            self.assertEqual(len(replacements), 1)
            self.assertIsNot(replacements[0], reopened_obj)
            self.assertFalse(replacements[0].get("caelm_protected"))
            self.assertNotEqual(tuple(replacements[0].data.vertices[0].co), reopened_vertex)


if __name__ == "__main__":
    sys.argv = [sys.argv[0]]
    unittest.main(verbosity=2)
