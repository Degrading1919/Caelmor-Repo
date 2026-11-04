"""Fast, Blender-free tests for reusable periodic material detail."""
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from caelmor_architecture.surface_detail import (
    DETAIL_PERIOD, generate_normal_tile, sample_detail,
)


class SurfaceDetailTests(unittest.TestCase):
    def test_all_families_are_finite_bounded_and_periodic(self):
        u = np.array([-.31, .17, .93, 1.91])
        v = np.array([.21, 1.43, -.88, 1.09])
        families = ("wood", "stone", "plaster", "roof", "iron", "leather", "charcoal")
        for family in families:
            with self.subTest(family=family):
                base = sample_detail(family, u, v, craftsmanship="ROUGH")
                moved = sample_detail(family, u + DETAIL_PERIOD, v - DETAIL_PERIOD,
                                       craftsmanship="ROUGH")
                self.assertEqual(base["albedo"].shape, (4, 3))
                for channel in ("albedo", "height", "roughness", "metallic"):
                    self.assertTrue(np.all(np.isfinite(base[channel])))
                    np.testing.assert_allclose(base[channel], moved[channel], atol=2e-12, rtol=0)
                self.assertTrue(np.all((base["albedo"] >= .45) & (base["albedo"] <= 1.35)))
                self.assertTrue(np.all(np.abs(base["height"]) <= .002))
                self.assertTrue(np.all((base["roughness"] >= 0) & (base["roughness"] <= 1)))
                self.assertTrue(np.all((base["metallic"] >= 0) & (base["metallic"] <= 1)))

    def test_height_derivative_is_continuous_across_period_seam(self):
        epsilon = 1e-5
        for axis in ("u", "v"):
            with self.subTest(axis=axis):
                if axis == "u":
                    left = sample_detail("wood", epsilon, .31)["height"][0]
                    at_seam = sample_detail("wood", 0.0, .31)["height"][0]
                    before = sample_detail("wood", DETAIL_PERIOD - epsilon, .31)["height"][0]
                else:
                    left = sample_detail("wood", .31, epsilon)["height"][0]
                    at_seam = sample_detail("wood", .31, 0.0)["height"][0]
                    before = sample_detail("wood", .31, DETAIL_PERIOD - epsilon)["height"][0]
                right_slope = (left - at_seam) / epsilon
                left_slope = (at_seam - before) / epsilon
                self.assertAlmostEqual(left_slope, right_slope, delta=3e-5)

    def test_wood_relief_runs_longitudinally_with_wider_crossgrain_variation(self):
        u, v = np.meshgrid(np.linspace(0, DETAIL_PERIOD, 192, endpoint=False),
                           np.linspace(0, DETAIL_PERIOD, 192, endpoint=False))
        h = sample_detail("wood", u, v)["height"].reshape(u.shape)
        du = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1))
        dv = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0))
        self.assertGreater(np.std(dv), 2.0 * np.std(du))

    def test_region_and_craftsmanship_change_detail(self):
        u, v = np.meshgrid(np.linspace(0, 1.9, 38), np.linspace(0, 1.9, 38))
        roof = [sample_detail("roof", u, v, region=r)["height"]
                for r in ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")]
        self.assertEqual(len({x.tobytes() for x in roof}), 4)
        rough = sample_detail("wood", u, v, craftsmanship="ROUGH")
        fine = sample_detail("wood", u, v, craftsmanship="FINE")
        self.assertGreater(np.mean(rough["height"] ** 2), np.mean(fine["height"] ** 2))

    def test_normal_tile_is_finite_normalized_and_repeat_safe(self):
        tile = generate_normal_tile("wood", craftsmanship="STANDARD", resolution=96)
        self.assertEqual(tile.shape, (96, 96, 4))
        self.assertEqual(tile.dtype, np.float32)
        self.assertTrue(np.all(np.isfinite(tile)))
        np.testing.assert_array_equal(tile[:, :, 3], np.ones((96, 96), dtype=np.float32))
        rgb = tile[:, :, :3] * 2.0 - 1.0
        np.testing.assert_allclose(np.linalg.norm(rgb, axis=2), 1.0, atol=2e-7, rtol=0)
        # Both edge normals are built from wrapped neighbors, so adjacent
        # texture samples across the tile boundary remain close in slope.
        edge_jump = np.mean(np.linalg.norm(rgb[:, 0] - rgb[:, -1], axis=1))
        inside_jump = np.mean(np.linalg.norm(rgb[:, 1:] - rgb[:, :-1], axis=2))
        self.assertLess(edge_jump, inside_jump * 1.5 + 1e-4)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            sample_detail("brick", [0.], [0.])
        with self.assertRaises(ValueError):
            sample_detail("wood", [np.nan], [0.])
        with self.assertRaises(ValueError):
            generate_normal_tile("wood", resolution=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
