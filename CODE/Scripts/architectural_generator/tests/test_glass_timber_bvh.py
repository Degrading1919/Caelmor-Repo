"""Blender BVH regression: glass surfaces must not intersect structural timber.

Run with Blender 5.0.1:
  blender --background --python tests/test_glass_timber_bvh.py
"""

import sys
import unittest
from pathlib import Path

import bpy
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.blender_backend import TAG, build
from caelmor_architecture.model import Settings


CASES = (
    dict(function="FARMHOUSE", region="LOWMARK", context="RURAL", footprint="RECT",
         floors=1, floor_height=2.4, pitch=60.0, window_density=1.5),
    dict(function="TOWNHOUSE", region="THORNFELL", context="STONEWAKE", footprint="RECT",
         floors=3, pitch=44.0, window_density=1.5, use_grammar=True),
    dict(function="BOATHOUSE", region="MIRE", context="SORROWMERE", footprint="RECT",
         floors=1, pitch=38.0, window_density=1.5, use_grammar=True),
    dict(function="INN", region="EMBERHOLT", context="EMBERFORGES", footprint="L",
         floors=2, pitch=42.0, window_density=1.5, use_grammar=True),
)


def object_bvh(obj, depsgraph):
    obj_eval = obj.evaluated_get(depsgraph)
    mesh = obj_eval.to_mesh()
    try:
        mesh.calc_loop_triangles()
        vertices = [obj_eval.matrix_world @ vertex.co for vertex in mesh.vertices]
        triangles = [tuple(tri.vertices) for tri in mesh.loop_triangles]
        return BVHTree.FromPolygons(vertices, triangles, all_triangles=True, epsilon=1e-6)
    finally:
        obj_eval.to_mesh_clear()


class GlassTimberIntersectionTests(unittest.TestCase):
    def test_glass_never_intersects_structural_timber(self):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        findings = []
        for case in CASES:
            collection, _metrics = build(Settings(seed=17, **case))
            glass = [obj for obj in collection.objects
                     if obj.get(TAG) and obj.get("caelm_layer") == "windows"
                     and obj.get("caelm_material") == "glass"]
            timber = [obj for obj in collection.objects
                      if obj.get(TAG) and obj.get("caelm_layer") == "structure"
                      and str(obj.get("caelm_material", "")).startswith("timber")]
            self.assertTrue(glass, (case, "no generated glass objects"))
            self.assertTrue(timber, (case, "no structural timber objects"))
            timber_bvhs = [(obj.name, object_bvh(obj, depsgraph)) for obj in timber]
            for glass_obj in glass:
                glass_bvh = object_bvh(glass_obj, depsgraph)
                for timber_name, timber_bvh in timber_bvhs:
                    intersections = glass_bvh.overlap(timber_bvh)
                    if intersections:
                        findings.append({"case": case, "glass": glass_obj.name,
                                         "timber": timber_name,
                                         "triangle_pairs": intersections[:8],
                                         "pair_count": len(intersections)})
        self.assertFalse(findings, "glass / structural timber BVH overlaps: " + repr(findings[:12]))


if __name__ == "__main__":
    if "--exclude-boathouse" in sys.argv:
        CASES = tuple(case for case in CASES if case["function"] != "BOATHOUSE")
    sys.argv = [sys.argv[0]]
    unittest.main(verbosity=2)
