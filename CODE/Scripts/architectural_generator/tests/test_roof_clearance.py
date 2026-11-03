"""Blender geometry regression for roof/frame penetration at eaves and gables.

Run with Blender's background Python:
  blender --background --python tests/test_roof_clearance.py

This deliberately samples mesh vertices, edge midpoints, and face centroids. It
checks generated geometry against the independently evaluated roof planes,
including the plane extension below the fascia outside the nominal roof outline.
"""

import math
import sys
import unittest
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.blender_backend import TAG, build
from caelmor_architecture.model import Settings, make_plan


def surface_samples(obj):
    """Return world-space vertices, edge midpoints, and polygon centroids."""
    matrix = obj.matrix_world
    vertices = [matrix @ vertex.co for vertex in obj.data.vertices]
    samples = list(vertices)
    for edge in obj.data.edges:
        a, b = (vertices[index] for index in edge.vertices)
        samples.append((a + b) * 0.5)
    for polygon in obj.data.polygons:
        ids = polygon.vertices
        samples.append(sum((vertices[index] for index in ids), vertices[0] * 0.0) / len(ids))
    return samples


def finite_roof_height(plan, x, y):
    height = plan.roof_height(x, y)
    return height if math.isfinite(height) else None


def extended_roof_height(plan, x, y):
    """Evaluate each supporting roof plane beyond its footprint edge."""
    values = []
    for x0, y0, x1, y1, axis in plan.rects:
        if plan.settings.roof_style == "HIP":
            distance = min(x-x0, x1-x, y-y0, y1-y)
        else:
            distance = min(y - y0, y1 - y) if axis == "X" else min(x - x0, x1 - x)
        values.append(plan.eave + plan.slope * distance)
    return max(values)


def build_cases():
    # Span compact and large masses; all footprint types are crossed with all
    # supported pitch endpoints and the default pitch.
    sizes = {
        "RECT": (8.0, 5.5, 1, 3.5, 4.0),
        "L": (11.0, 7.0, 2, 4.2, 4.5),
        "T": (14.0, 9.0, 2, 4.5, 5.2),
        "U": (15.0, 10.0, 2, 4.5, 6.0),
    }
    for footprint, (width, depth, floors, wing_width, wing_depth) in sizes.items():
        for pitch in (30.0, 48.0, 60.0):
            yield Settings(seed=17 + int(pitch), function="FARMHOUSE", footprint=footprint,
                           width=width, depth=depth, floors=floors, wing_width=wing_width,
                           wing_depth=wing_depth, pitch=pitch, detail="HIGH")
    # One-storey buildings have the tightest eaves. Exercise function-specific
    # headers and signs at minimum floor height and maximum roof pitch.
    for function in ("FARMHOUSE", "BARN", "GRAIN_STORE", "MILLER", "INN"):
        yield Settings(seed=91, function=function, footprint="RECT", width=8.0,
                       depth=5.5, floors=1, floor_height=2.4, pitch=60.0,
                       detail="HIGH")
    # Expanded regional grammar coverage includes HIP profiles, elevated Mire
    # foundations and mixed-use civic framing at their resolved dimensions.
    yield Settings(seed=113, function="WATCHTOWER", region="THORNFELL", context="PASSWATCH",
                   use_grammar=True, detail="HIGH", pitch=60.0)
    yield Settings(seed=114, function="MARKET_HALL", region="EMBERHOLT", context="EMBERHOLD",
                   use_grammar=True, detail="HIGH", pitch=60.0)
    yield Settings(seed=115, function="COTTAGE", region="MIRE", context="SORROWMERE",
                   use_grammar=True, maintenance=.1, age=180, detail="HIGH", pitch=60.0)
    yield Settings(seed=116, function="ASSEMBLY_HALL", region="EMBERHOLT", context="CINDERWEAVE",
                   use_grammar=True, detail="HIGH", pitch=60.0)


class RoofClearance(unittest.TestCase):
    def test_frame_and_fascia_stay_below_roof_planes(self):
        tolerance = 0.002
        wall_contact_tolerance = 0.01
        frame_clearance = 0.12
        failures = []

        for settings in build_cases():
            bpy.ops.wm.read_factory_settings(use_empty=True)
            plan = make_plan(settings)
            collection, _metrics = build(settings)
            objects = [obj for obj in collection.objects
                       if obj.get(TAG) and obj.type == "MESH" and not obj.get("caelm_collider")]

            for obj in objects:
                layer = obj.get("caelm_layer")
                if layer == "roof" and obj.get("caelm_buffer_id") == "Roof edge fascia":
                    for index, point in enumerate(surface_samples(obj)):
                        limit = extended_roof_height(plan, point.x, point.y)
                        excess = point.z - limit
                        if excess > tolerance:
                            failures.append((settings.footprint, settings.pitch, "fascia",
                                             obj.name, index, round(excess, 5),
                                             tuple(round(v, 5) for v in point)))
                elif layer == "walls":
                    # Wall tops may meet the deck underside at the eave.
                    for index, point in enumerate(surface_samples(obj)):
                        roof_z = finite_roof_height(plan, point.x, point.y)
                        if roof_z is None:
                            continue
                        excess = point.z - roof_z
                        if excess > wall_contact_tolerance:
                            failures.append((settings.footprint, settings.pitch, "wall",
                                             obj.name, index, round(excess, 5),
                                             tuple(round(v, 5) for v in point)))
                elif layer == "structure" or (layer == "details" and obj.get("caelm_material") == "timber"):
                    # Structure and timber signs must clear the roof deck's
                    # full 120 mm depth.
                    for index, point in enumerate(surface_samples(obj)):
                        roof_z = finite_roof_height(plan, point.x, point.y)
                        if roof_z is None:
                            continue
                        excess = point.z - (roof_z - frame_clearance)
                        if excess > tolerance:
                            failures.append((settings.footprint, settings.pitch, "structure",
                                             obj.name, index, round(excess, 5),
                                             tuple(round(v, 5) for v in point)))

        self.assertFalse(failures, "Roof clearance violations (case, pitch, class, object, sample, "
                         "excess, xyz):\n" + "\n".join(map(str, failures[:80])))


if __name__ == "__main__":
    # Blender's CLI flags remain in sys.argv when it executes a Python script.
    unittest.main(argv=[sys.argv[0]], verbosity=2)
