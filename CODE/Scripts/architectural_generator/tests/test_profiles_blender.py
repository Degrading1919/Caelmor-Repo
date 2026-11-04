"""Blender integration checks for legacy snapshots and regional material banks."""

import json
import sys
import unittest
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.blender_backend import SETTINGS_KEY, build, _normalize_settings_data
from caelmor_architecture.model import Settings, make_plan


class ExpandedProfileBlenderTests(unittest.TestCase):
    def test_legacy_snapshot_normalizes_to_manual_solid_and_regenerates(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        # Deliberately omit every field introduced by 0.3.0.
        old = {"seed": 73, "function": "GRAIN_STORE", "footprint": "RECT",
               "width": 12.25, "depth": 8.0, "wing_width": 4.0,
               "wing_depth": 5.0, "floors": 2, "floor_height": 2.7,
               "pitch": 46.0, "overhang": .4, "detail": "MEDIUM",
               "window_density": .9}
        migrated = _normalize_settings_data(old)
        self.assertFalse(migrated["use_grammar"])
        self.assertEqual(migrated["geometry_mode"], "SOLID")
        self.assertEqual(migrated["region"], "LOWMARK")
        self.assertEqual(migrated["roof_style"], "GABLE",
                         "legacy manual walls need the old gable roof form")
        self.assertEqual((migrated["width"], migrated["depth"], migrated["floors"]),
                         (12.25, 8.0, 2))
        self.assertEqual(make_plan(Settings(**migrated)).settings.roof_style, "GABLE")
        collection, metrics = build(Settings(**migrated))
        self.assertEqual(json.loads(collection[SETTINGS_KEY])["use_grammar"], False)
        self.assertGreater(metrics["vertices"], 0)

    def test_four_regional_material_banks_coexist_in_one_scene(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        cases = (("LOWMARK", "RURAL"), ("THORNFELL", "STONEWAKE"),
                 ("MIRE", "SORROWMERE"), ("EMBERHOLT", "EMBERFORGES"))
        swatches = {}
        families = {}
        for region, context in cases:
            collection, _metrics = build(Settings(function="COTTAGE", use_grammar=True,
                                                   region=region, context=context,
                                                   wealth="ESTABLISHED", seed=29))
            roof_obj = next(obj for obj in collection.objects
                            if obj.get("caelm_generated") and obj.get("caelm_material") == "roof")
            material = roof_obj.data.materials[0]
            swatches[region] = tuple(round(float(v), 5) for v in material.diffuse_color)
            textures = [node.image for node in material.node_tree.nodes
                        if node.type == "TEX_IMAGE" and node.image is not None]
            self.assertTrue(textures, region)
            families[region] = tuple(image.get("caelm_texture_family") for image in textures)
        self.assertGreaterEqual(len(set(swatches.values())), 3, swatches)
        # Palette variants share the source texture bank instead of minting per-building images.
        self.assertEqual(len(set(families.values())), 1, families)
        roof_palettes = {m.get("caelm_palette_key") for m in bpy.data.materials
                         if m.get("caelm_material") == "roof"}
        self.assertEqual(len(roof_palettes), 4, roof_palettes)


if __name__ == "__main__":
    sys.argv = [sys.argv[0]]
    unittest.main(verbosity=2)
