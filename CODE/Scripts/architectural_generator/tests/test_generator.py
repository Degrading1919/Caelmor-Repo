"""Pure-Python contract tests for the Caelmor architectural generator.

Run from this directory with:
    python -m unittest discover -s tests -v
"""

import unittest

from caelmor_architecture.engine import generate, geometry_hash, validate
from caelmor_architecture.facade import _openings_for_edge, build_facades, frame_layout
from caelmor_architecture.geometry import MeshBuffer, area, inequalities
from caelmor_architecture.model import Settings, make_plan
from caelmor_architecture.roof import build_roof, roof_faces, roof_join_kind, roof_topology, shingle_layout


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
    def test_validator_rejects_legacy_eave_post_above_roof_underside(self):
        settings = Settings(seed=17, function="FARMHOUSE", footprint="RECT",
                            floors=1, floor_height=2.4, pitch=60.0)
        plan, buffers = generate(settings)
        legacy_post = MeshBuffer("Legacy eave post", "timber", "structure")
        legacy_post.box((1.0, -0.10, plan.eave - 0.10), (0.2, 0.1, 0.2))
        report = validate(plan, buffers + [legacy_post])
        self.assertFalse(report["valid"])
        self.assertTrue(any("Legacy eave post: timber crosses roof underside" in error
                            for error in report["errors"]), report["errors"])

    def test_same_seed_is_repeatable_and_seed_changes_result(self):
        settings = Settings(seed=24680)
        _, first = generate(settings)
        _, repeated = generate(settings)
        _, another_seed = generate(Settings(seed=24681))
        self.assertEqual(geometry_hash(first), geometry_hash(repeated))
        self.assertNotEqual(geometry_hash(first), geometry_hash(another_seed))

    def test_detail_tiers_have_ascending_geometry_work(self):
        complexity = []
        for detail in ("LOW", "MEDIUM", "HIGH"):
            _plan, buffers = generate(Settings(seed=17, function="FARMHOUSE",
                                               footprint="L", detail=detail))
            complexity.append((sum(len(buffer.vertices) for buffer in buffers),
                               sum(len(buffer.faces) for buffer in buffers)))
        self.assertLess(complexity[0][0], complexity[1][0])
        self.assertLess(complexity[1][0], complexity[2][0])
        self.assertLess(complexity[0][1], complexity[1][1])
        self.assertLess(complexity[1][1], complexity[2][1])

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
                            self.assertGreaterEqual(opening["z1"] - opening["z0"], 2.0)
                    for i, opening in enumerate(openings):
                        for other in openings[i + 1:]:
                            overlap_s = min(opening["s1"], other["s1"]) - max(opening["s0"], other["s0"])
                            overlap_z = min(opening["z1"], other["z1"]) - max(opening["z0"], other["z0"])
                            self.assertFalse(overlap_s > 0.08 and overlap_z > 0.08)
                self.assertTrue(found_opening)

    def test_frame_layout_braces_land_on_joints_and_clear_full_opening_bounds(self):
        """Braces must connect real post/plate joints without crossing apertures."""
        brace_slopes = set()
        for function in ("FARMHOUSE", "BARN", "GRAIN_STORE", "MILLER", "INN"):
            for footprint in ("RECT", "L", "T", "U"):
                with self.subTest(function=function, footprint=footprint):
                    plan = make_plan(Settings(function=function, footprint=footprint, seed=17))
                    for edge_index, edge in enumerate(plan.edges):
                        layout = frame_layout(plan, edge_index, edge)
                        posts = layout["posts"]
                        plate_levels = layout["plates"]
                        self.assertEqual(layout["principal_posts"], posts)
                        self.assertEqual(layout["edge_index"], edge_index)
                        self.assertGreater(layout["length"], 0.0)
                        post_half_width = .11 if function in ("BARN", "GRAIN_STORE") else .095
                        post_clearance = post_half_width + .11
                        for opening in layout["openings"]:
                            for post in layout["principal_posts"]:
                                self.assertTrue(
                                    post <= opening["s0"] - post_clearance + 1e-3
                                    or post >= opening["s1"] + post_clearance - 1e-3,
                                    f"full-height principal post collides with {opening['kind']} on edge {edge_index}")
                        gaps = [b-a for a, b in zip(posts, posts[1:])]
                        self.assertTrue(all(gap >= .65-1e-7 for gap in gaps))
                        self.assertLessEqual(max(gaps, default=0.0), 6.0+1e-7)
                        for span in layout["unsupported_spans"]:
                            self.assertGreater(span["length"], 4.3)
                            self.assertAlmostEqual(span["s1"]-span["s0"], span["length"], places=6)
                            self.assertFalse(any(span["s0"] < post < span["s1"] for post in posts))
                        for brace in layout["braces"]:
                            brace_slopes.add("ascending" if brace["z1"] > brace["z0"] else "descending")
                            self.assertGreater(brace["width"], 0.0)
                            if brace["support"] == "bay":
                                self.assertTrue(any(abs(brace["s0"] - post) < 1e-7 for post in posts))
                                self.assertTrue(any(abs(brace["s1"] - post) < 1e-7 for post in posts))
                                self.assertTrue(any(abs(brace["z0"] - level) < 1e-7 for level in plate_levels))
                                self.assertTrue(any(abs(brace["z1"] - level) < 1e-7 for level in plate_levels))
                                slope = abs(brace["z1"] - brace["z0"]) / (brace["s1"] - brace["s0"])
                                self.assertGreaterEqual(slope, .70)
                                self.assertLessEqual(slope, 2.15)
                            elif brace["support"] == "knee":
                                self.assertTrue(any(abs(brace["post_s"]-post) < 1e-4 for post in posts))
                                self.assertIn(brace["plate_z"], plate_levels)
                                self.assertAlmostEqual(brace["s0"], brace["post_s"])
                                self.assertAlmostEqual(brace["z0"], brace["plate_z"]-.85)
                                self.assertAlmostEqual(brace["z1"], brace["plate_z"])
                                self.assertAlmostEqual(abs(brace["s1"]-brace["s0"]), .85)
                            else:
                                self.fail(f"unknown brace support kind {brace['support']}")
                            # Liang-Barsky segment-vs-expanded-rectangle test. The
                            # expansion includes the brace's half-width and margin.
                            pad = brace["width"] * 0.5 + 0.035
                            for opening in layout["openings"]:
                                x0, x1 = opening["s0"] - pad, opening["s1"] + pad
                                y0, y1 = opening["z0"] - pad, opening["z1"] + pad
                                dx, dy = brace["s1"] - brace["s0"], brace["z1"] - brace["z0"]
                                lo, hi = 0.0, 1.0
                                for p, q in ((-dx, brace["s0"] - x0), (dx, x1 - brace["s0"]),
                                             (-dy, brace["z0"] - y0), (dy, y1 - brace["z0"])):
                                    if abs(p) < 1e-12:
                                        self.assertGreaterEqual(q, 0.0, "brace parallel to opening edge overlaps")
                                    else:
                                        t = q / p
                                        if p < 0.0:
                                            lo = max(lo, t)
                                        else:
                                            hi = min(hi, t)
                                self.assertFalse(lo <= hi, f"brace crosses {opening['kind']} on edge {edge_index}")
                        for opening in layout["openings"]:
                            if opening["kind"] == "door":
                                self.assertGreaterEqual(opening["z1"] - opening["z0"], 2.0)
        self.assertEqual(brace_slopes, {"ascending", "descending"})

    def test_simple_gables_have_two_rakes_a_kingpost_and_collar(self):
        # Grain Store now defaults to a HIP roof; exercise only profiles whose
        # actual resolved roof style is a simple gable.
        for function in ("FARMHOUSE", "BARN", "MILLER", "INN"):
            with self.subTest(function=function):
                plan = make_plan(Settings(function=function, footprint="RECT", seed=17))
                gables = [frame_layout(plan, i, edge)["gable"]
                          for i, edge in enumerate(plan.edges)]
                simple = [gable for gable in gables if gable["rakes"]]
                self.assertTrue(simple)
                self.assertTrue(any(len(gable["rakes"]) >= 2
                                    and gable["kingpost"] is not None
                                    and gable["collar"] is not None
                                    for gable in simple))

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

    def test_roof_deck_top_vertices_follow_resolved_clipped_envelope(self):
        for footprint in ("RECT", "L", "T", "U"):
            with self.subTest(footprint=footprint):
                plan = make_plan(Settings(seed=31, footprint=footprint, detail="MEDIUM"))
                deck = next(buffer for buffer in build_roof(plan)
                            if buffer.name == "Continuous roof deck")
                self.assertEqual(len(deck.vertices) % 2, 0)
                top_count = len(deck.vertices) // 2
                top = deck.vertices[:top_count]
                bottom = deck.vertices[top_count:]
                self.assertTrue(top)
                for upper, lower in zip(top, bottom):
                    x, y, z = upper
                    self.assertAlmostEqual(z, plan.roof_height(x, y), places=5)
                    self.assertAlmostEqual(lower[0], x, places=6)
                    self.assertAlmostEqual(lower[1], y, places=6)
                    self.assertAlmostEqual(lower[2], z-.12, places=6)

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

    def test_shingle_courses_clip_to_slopes_and_keep_repairs_bounded(self):
        for detail in ("LOW", "MEDIUM", "HIGH"):
            for footprint in ("RECT", "L", "T", "U"):
                with self.subTest(detail=detail, footprint=footprint):
                    plan = make_plan(Settings(seed=17, function="FARMHOUSE", footprint=footprint,
                                              detail=detail))
                    patches = roof_faces(plan)
                    points, _faces, edges = roof_topology(patches)
                    kinds = [roof_join_kind(points, patches, users) for users in edges.values()]
                    self.assertIn("ridge", kinds)
                    shingles = shingle_layout(plan, patches, (points, _faces, edges))
                    self.assertTrue(shingles)
                    keys = {}
                    course_widths = []
                    repaired = []
                    for shingle in shingles:
                        key = (shingle.source, shingle.row, shingle.bay,
                               shingle.axis, shingle.direction)
                        attributes = (shingle.course_start, shingle.course_end,
                                      shingle.u0, shingle.u1, shingle.material, shingle.repair)
                        if key in keys:
                            self.assertEqual(keys[key], attributes,
                                             "split roof patches disagree about a shingle cohort")
                        keys[key] = attributes
                        width = shingle.u1 - shingle.u0
                        course_widths.append(width)
                        self.assertGreater(width, 0.0)
                        # Every emitted tile polygon stays inside a resolved
                        # visible patch with the same analytic slope plane.
                        matching = [patch for patch in patches
                                    if patch.source == shingle.source and patch.plane == shingle.plane]
                        self.assertTrue(any(all(all(a*x + b*y + c >= -1e-6
                                                    for a, b, c in inequalities(patch.poly))
                                                for x, y in shingle.poly)
                                            for patch in matching),
                                        "shingle escaped its clipped roof support")
                        if shingle.repair:
                            repaired.append(shingle)
                            self.assertEqual(shingle.material, "roof_patch")
                            self.assertLess(shingle.row, 3)
                            self.assertLessEqual(width, 1.0)
                        else:
                            self.assertNotEqual(shingle.material, "roof_patch")
                    self.assertGreater(max(course_widths) - min(course_widths), .02)

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
