"""Pure-Python contract tests for the Caelmor architectural generator.

Run from this directory with:
    python -m unittest discover -s tests -v
"""

import unittest

from caelmor_architecture.engine import generate, geometry_hash, validate
from caelmor_architecture.facade import _openings_for_edge, build_facades
from caelmor_architecture.geometry import area
from caelmor_architecture.model import Settings, make_plan
from caelmor_architecture.roof import build_roof, roof_faces, roof_topology


class PlanTests(unittest.TestCase):
    def test_supported_footprints_have_valid_bounds_and_area(self):
        for footprint in ("RECT", "L", "T", "U"):
            with self.subTest(footprint=footprint):
                settings = Settings(footprint=footprint)
                plan = make_plan(settings)
                self.assertGreaterEqual(len(plan.outline), 4)
                self.assertEqual(len(plan.outline), len(set(plan.outline)))
                xs, ys = zip(*plan.outline)
                self.assertAlmostEqual(min(xs), 0.0)
                self.assertGreater(max(xs) - min(xs), 0.0)
                self.assertGreater(max(ys) - min(ys), 0.0)
                self.assertGreater(len(plan.rects), 0)
                self.assertGreater(plan.eave, 0.0)
                expected = {
                    "RECT": settings.width * settings.depth,
                    "L": settings.width * settings.depth + settings.wing_width * settings.wing_depth,
                    "T": settings.width * settings.depth + settings.wing_width * settings.wing_depth,
                    "U": settings.width * settings.depth + 2 * settings.wing_width * settings.wing_depth,
                }[footprint]
                self.assertAlmostEqual(area(plan.outline), expected, places=6)

    def test_dimension_guards_reject_nonpositive_or_impossible_inputs(self):
        invalid = (
            {"width": 0.0},
            {"depth": -1.0},
            {"floors": 0},
            {"floor_height": 0.0},
            {"wing_width": 0.0},
            {"wing_depth": 0.0},
            {"width": 5.9},
            {"depth": 3.9},
            {"floor_height": 2.0},
            {"pitch": 61.0},
            {"overhang": 0.1},
            {"window_density": 1.6},
            {"floors": 4},
        )
        for overrides in invalid:
            with self.subTest(overrides=overrides):
                with self.assertRaises((ValueError, TypeError)):
                    make_plan(Settings(**overrides))

    def test_invalid_footprint_is_rejected(self):
        with self.assertRaises((ValueError, TypeError)):
            make_plan(Settings(footprint="OCTAGON"))

    def test_named_random_streams_are_stable_and_independent(self):
        settings = Settings(seed=9821)
        first = make_plan(settings)
        second = make_plan(settings)
        self.assertEqual([first.rng("facade").random() for _ in range(4)],
                         [second.rng("facade").random() for _ in range(4)])
        facade_before = [first.rng("facade").random() for _ in range(4)]
        first.rng("roof").random()
        self.assertEqual(facade_before, [first.rng("facade").random() for _ in range(4)])
        self.assertNotEqual(first.rng("facade").random(), first.rng("roof").random())


class GenerationTests(unittest.TestCase):
    def test_same_seed_is_repeatable_and_seed_changes_result(self):
        settings = Settings(seed=24680)
        _, first = generate(settings)
        _, repeated = generate(settings)
        _, another_seed = generate(Settings(seed=24681))
        self.assertEqual(geometry_hash(first), geometry_hash(repeated))
        self.assertNotEqual(geometry_hash(first), geometry_hash(another_seed))

    def test_all_footprints_pass_engine_validation(self):
        for footprint in ("RECT", "L", "T", "U"):
            with self.subTest(footprint=footprint):
                plan, buffers = generate(Settings(footprint=footprint))
                report = validate(plan, buffers)
                self.assertIsInstance(report, dict)
                self.assertTrue(report["valid"], report["errors"])
                self.assertGreater(report["footprint_area"], 0.0)
                self.assertGreater(report["roof_projected_area"], 0.0)

    def test_all_five_building_functions_generate_valid_exteriors(self):
        for function in ("FARMHOUSE", "BARN", "GRAIN_STORE", "MILLER", "INN"):
            with self.subTest(function=function):
                plan, buffers = generate(Settings(function=function, seed=41, footprint="RECT"))
                report = validate(plan, buffers)
                self.assertTrue(report["valid"], report["errors"])
                self.assertTrue(any(b.layer == "doors" for b in buffers))
                found_opening = False
                for edge_index, edge in enumerate(plan.edges):
                    length = ((edge[1][0] - edge[0][0]) ** 2 + (edge[1][1] - edge[0][1]) ** 2) ** .5
                    openings = _openings_for_edge(plan, edge_index, edge)
                    found_opening |= bool(openings)
                    for opening in openings:
                        self.assertGreaterEqual(opening["s0"], 0.0)
                        self.assertLessEqual(opening["s1"], length)
                        self.assertGreater(opening["s1"], opening["s0"])
                        self.assertGreater(opening["z1"], opening["z0"])
                        if opening["kind"] == "door":
                            self.assertGreaterEqual(opening["z1"] - opening["z0"], 1.9)
                    for i, opening in enumerate(openings):
                        for other in openings[i + 1:]:
                            overlap_s = min(opening["s1"], other["s1"]) - max(opening["s0"], other["s0"])
                            overlap_z = min(opening["z1"], other["z1"]) - max(opening["z0"], other["z0"])
                            self.assertFalse(overlap_s > 0.08 and overlap_z > 0.08)
                self.assertTrue(found_opening)

    def test_facade_parameter_changes_do_not_perturb_roof_generation(self):
        base = Settings(seed=37, window_density=0.8)
        denser = Settings(seed=37, window_density=1.4)
        roof_a, roof_b = build_roof(make_plan(base)), build_roof(make_plan(denser))
        facade_a, facade_b = build_facades(make_plan(base)), build_facades(make_plan(denser))
        self.assertEqual(geometry_hash(roof_a), geometry_hash(roof_b))
        self.assertNotEqual(geometry_hash(facade_a), geometry_hash(facade_b))

    def test_visible_roof_patches_match_upper_envelope_and_have_manifold_seams(self):
        for footprint in ("RECT", "L", "T", "U"):
            with self.subTest(footprint=footprint):
                plan = make_plan(Settings(footprint=footprint))
                patches = roof_faces(plan)
                points, faces, edges = roof_topology(patches)
                self.assertTrue(patches)
                self.assertTrue(faces)
                self.assertTrue(all(len(users) in (1, 2) for users in edges.values()))
                for patch in patches:
                    samples = patch.poly + [(
                        sum(x for x, _ in patch.poly) / len(patch.poly),
                        sum(y for _, y in patch.poly) / len(patch.poly),
                    )]
                    for x, y in samples:
                        self.assertAlmostEqual(patch.height(x, y), plan.roof_height(x, y), places=5)
                self.assertEqual(len(points), len({tuple(round(v, 8) for v in p) for p in points}))

    def test_roof_topology_handles_near_equal_width_and_depth_regression(self):
        settings = Settings(
            seed=13, function="MILLER", footprint="L",
            width=15.825150446193273, depth=4.720957947847847,
            wing_width=4.707569012596809, wing_depth=11.466844779743079,
            floors=2, pitch=40.50679725947052, overhang=0.5335220677100841,
            detail="LOW", window_density=0.7048846527101691,
        )
        plan, buffers = generate(settings)
        result = validate(plan, buffers)
        self.assertTrue(result["valid"], result["errors"])
        points, faces, edges = roof_topology(roof_faces(plan))
        self.assertTrue(points and faces)
        self.assertTrue(all(len(users) in (1, 2) for users in edges.values()))

    def test_buffer_mesh_indices_and_faces_are_valid(self):
        _, buffers = generate(Settings(seed=17))
        self.assertTrue(buffers)
        for buffer in buffers:
            with self.subTest(buffer=buffer.name):
                self.assertGreater(len(buffer.vertices), 0)
                self.assertGreater(len(buffer.faces), 0)
                for face in buffer.faces:
                    self.assertGreaterEqual(len(face), 3)
                    self.assertTrue(all(0 <= i < len(buffer.vertices) for i in face))


if __name__ == "__main__":
    unittest.main()
