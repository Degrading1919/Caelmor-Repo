"""Run with Blender in background mode to check adjoining Lowmark references."""
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils import Vector

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from place_blockout_sector import GRIDS, place_sector


def terrain_bounds(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    corners = np.array([tuple(obj.matrix_world @ Vector(corner))
                        for obj in set(bpy.data.objects) - before if obj.type == "MESH"
                        for corner in obj.bound_box])
    return corners[:, :2].min(axis=0), corners[:, :2].max(axis=0)


def xy_bounds(obj):
    width, height = obj.data.size
    offset = obj.empty_image_offset
    size = obj.empty_display_size
    a = obj.matrix_world @ Vector((size * offset[0], size * offset[1], 0))
    b = obj.matrix_world @ Vector((size * (1 + offset[0]), size * (height / width + offset[1]), 0))
    return [a.x, a.y, b.x, b.y]


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
terrain = GRIDS.parents[1] / "Lowmark_Terrain"
regional = terrain_bounds(terrain / "terrain.glb")
local = terrain_bounds(terrain / "Local_Refinement/crestbridge_mill.glb")
np.testing.assert_allclose(regional, [(0, 0), (3456, 3072)], atol=.001, rtol=0)
np.testing.assert_allclose(local, [(1104, 552), (2208, 1440)], atol=.001, rtol=0)
west = place_sector("D03")
east = place_sector("E03", source="svg")
bpy.context.view_layer.update()
assert west.data.size[:] == east.data.size[:] == (384, 384)
assert east.data.packed_file is not None
np.testing.assert_array_equal(xy_bounds(west), [1152, 768, 1536, 1152])
np.testing.assert_array_equal(xy_bounds(east), [1536, 768, 1920, 1152])
for x in (1344, 1536, 1728):
    hit, point, _, _, _, _ = scene.ray_cast(
        bpy.context.evaluated_depsgraph_get(), Vector((x, 960, 300)), Vector((0, 0, -1)))
    assert hit and abs(point.x - x) < .001 and abs(point.y - 960) < .001
    print(f"Terrain probe ({x}, 960) hit elevation {point.z:.3f} m")
print(f"CAELMOR_BLOCKOUT_BLENDER_PASSED Blender={bpy.app.version_string} "
      "regional_and_local_GLBs_aligned D03_PNG E03_SVG common_edge_x=1536")
