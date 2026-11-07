"""Regression fixtures for parent-derived bounded local terrain refinement."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

import terrain
from test_terrain import controls_fixture
from local_refinement import adaptive_diagonals, export_local, grade_profile, project_drainage, refine_all, sample_triangles


def local_fixture():
    return {"resolution_m": 2, "boundary_feather_m": 16,
            "patches": [{"id": "test_town", "bounds_m": [96, 16, 240, 144],
                         "settlement_ids": ["town"], "route_ids": [], "bank_reach_ids": ["lower"]}],
            "roads": {"half_width_m": 4, "blend_m": 10, "max_cut_fill_m": 2, "max_grade": 0.1,
                      "profile_smoothing_m": 12, "water_crossing_exclusion_m": 24},
            "banks": {"max_cut_fill_m": 1, "blend_m": 8},
            "foundations": {"max_cut_fill_m": 1, "max_plane_grade": 0.05, "blend_m": 3, "max_pad_count": 2,
                            "scenario_floor_clearance_m": 0.3}}


class LocalRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = Path(__file__).with_name(".scratch")
        cls.scratch.mkdir(exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(dir=cls.scratch)
        cls.parent_path = Path(cls.temporary.name) / "parent.npz"
        cls.controls = controls_fixture()
        cls.controls["settlements"][0].update(envelope_axes_m=[100, 80], plot_coverage=0.35, road_fraction=0.25)
        cls.parent = terrain.generate(cls.controls, 8).height_engineered
        np.savez_compressed(cls.parent_path, height_engineered=cls.parent)
        cls.source_hash = hashlib.sha256(cls.parent_path.read_bytes()).hexdigest()
        cls.local = local_fixture()
        cls.result = refine_all(cls.parent_path, cls.controls, cls.local)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_diagonal_parent_route_is_not_broken_by_bilinear_sampling(self):
        height = np.array([[10.0, 0], [-1, 10]])
        receiver = terrain.d8_receivers(height, 8)
        diagonals = adaptive_diagonals(height, receiver)
        fine = sample_triangles(height, diagonals, np.arange(0, 9, 2), np.arange(0, 9, 2))
        np.testing.assert_array_equal(fine[::4, ::4], height)
        self.assertGreaterEqual(terrain.d8_receivers(fine, 2)[0, -1], 0)
        old_mesh = sample_triangles(height, np.zeros_like(diagonals), np.arange(0, 9, 2), np.arange(0, 9, 2))
        self.assertEqual(terrain.d8_receivers(old_mesh, 2)[0, -1], -2)

    def test_bounded_projection_preserves_immutable_cells_and_actual_descent(self):
        source = np.add.outer(np.arange(6, 0, -1), np.arange(6, 0, -1)).astype(float)
        rec = terrain.d8_receivers(source, 2)
        budget = np.zeros(source.shape); budget[1:-1, 1:-1] = 1
        target = source.copy(); target[2, 2] -= 8
        projected = project_drainage(source, target, rec, source - budget, source + budget)
        self.assertLessEqual(float(np.max(np.abs(projected - source))), 1)
        np.testing.assert_array_equal(projected[budget == 0], source[budget == 0])
        active = rec.ravel() >= 0
        self.assertTrue((projected.ravel()[active] > projected.ravel()[rec.ravel()[active]]).all())

    def test_parent_source_and_patch_seams_are_exactly_preserved(self):
        self.assertEqual(hashlib.sha256(self.parent_path.read_bytes()).hexdigest(), self.source_hash)
        patch = self.result.patches[0]
        boundary = np.zeros(patch.height.shape, dtype=bool)
        boundary[[0, -1]] = True; boundary[:, [0, -1]] = True
        np.testing.assert_array_equal(patch.height[boundary], patch.base_height[boundary])
        self.assertEqual(patch.x[0] % 8, 0)
        self.assertEqual(patch.y[0] % 8, 0)
        self.assertTrue(np.all(np.diff(patch.x) == 2))

    def test_actual_owned_drainage_has_real_outward_exits(self):
        patch = self.result.patches[0]
        self.assertFalse((patch.receiver == -2).any())
        self.assertTrue(patch.metrics["all_owned_samples_reach_outward_exits"])
        self.assertTrue(patch.metrics["all_exits_have_regional_continuation"])
        self.assertLess(patch.metrics["actual_outward_exit_count"], 2 * sum(patch.height.shape) - 4)
        active = patch.receiver.ravel() >= 0
        self.assertTrue((patch.height.ravel()[active] > patch.height.ravel()[patch.receiver.ravel()[active]]).all())

    def test_stage_deltas_reconstruct_the_saved_final_surface(self):
        patch = self.result.patches[0]
        reconstructed = patch.base_height + sum(patch.stage_deltas.values())
        np.testing.assert_allclose(reconstructed, patch.height, rtol=0, atol=1e-10)
        self.assertLessEqual(float(np.abs(patch.stage_deltas["bank"]).max()), self.local["banks"]["max_cut_fill_m"])
        self.assertLessEqual(float(np.abs(patch.stage_deltas["road"]).max()), self.local["roads"]["max_cut_fill_m"])
        self.assertLessEqual(float(np.abs(patch.stage_deltas["pad"]).max()), self.local["foundations"]["max_cut_fill_m"])

    def test_overlap_ownership_conflict_is_rejected(self):
        config = copy.deepcopy(self.local)
        config["patches"].append(dict(config["patches"][0], id="conflicting_copy"))
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            refine_all(self.parent_path, self.controls, config)

    def test_actual_profile_projection_respects_declared_grade(self):
        stations = np.arange(12, dtype=float) * 2
        elevations = np.array([0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0], dtype=float)
        graded = grade_profile(elevations, stations, 0.10, 6)
        self.assertLessEqual(float(np.max(np.abs(np.diff(graded)) / np.diff(stations))), 0.1000000001)

    def test_repeat_generation_and_saved_arrays_match(self):
        repeated = refine_all(self.parent_path, self.controls, self.local)
        np.testing.assert_array_equal(repeated.composite_height, self.result.composite_height)
        np.testing.assert_array_equal(repeated.patches[0].height, self.result.patches[0].height)
        with tempfile.TemporaryDirectory(dir=self.scratch) as output:
            export_local(self.result, output)
            with np.load(Path(output) / "test_town.npz", allow_pickle=False) as saved:
                np.testing.assert_array_equal(saved["height"], self.result.patches[0].height)
                np.testing.assert_array_equal(saved["halo_height"], self.result.patches[0].halo_height)


if __name__ == "__main__":
    unittest.main()
