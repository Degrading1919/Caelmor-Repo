"""Bounded tests for the original vectorized Caelmor microtexture sampler."""
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from caelmor_architecture.surface_patterns import sample_pattern


class SurfacePatternTests(unittest.TestCase):
    def setUp(self):
        self.u, self.v = np.meshgrid(np.linspace(-1.3, 2.1, 57), np.linspace(-.8, .9, 43))

    def test_families_are_deterministic_finite_and_bounded(self):
        for family in ("wood", "stone", "plaster", "roof", "iron", "leather", "charcoal"):
            with self.subTest(family=family):
                a = sample_pattern(family, self.u, self.v, seed=219)
                b = sample_pattern(family, self.u, self.v, seed=219)
                for channel in ("albedo", "height", "roughness", "metallic"):
                    np.testing.assert_array_equal(a[channel], b[channel])
                    self.assertTrue(np.all(np.isfinite(a[channel])))
                self.assertEqual(a["albedo"].shape, (self.u.size, 3))
                self.assertEqual(a["height"].shape, (self.u.size,))
                self.assertTrue(np.all((a["albedo"] >= .45) & (a["albedo"] <= 1.35)))
                self.assertTrue(np.all(np.abs(a["height"]) <= .002))
                self.assertTrue(np.all((a["roughness"] >= 0) & (a["roughness"] <= 1)))
                self.assertTrue(np.all((a["metallic"] >= 0) & (a["metallic"] <= 1)))

    def test_roof_coverings_have_distinct_regional_height_signatures(self):
        outputs = [sample_pattern("roof", self.u, self.v, region=r, seed=14)["height"]
                   for r in ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")]
        self.assertTrue(all(np.std(x) > 1e-5 for x in outputs))
        self.assertEqual(len({x.tobytes() for x in outputs}), 4)
        self.assertGreater(np.std(outputs[2]), np.std(outputs[1]))

    def test_craftsmanship_and_wealth_are_independent_controls(self):
        baseline = sample_pattern("stone", self.u, self.v)
        rough = sample_pattern("stone", self.u, self.v, craftsmanship="ROUGH")
        fine = sample_pattern("stone", self.u, self.v, craftsmanship="FINE")
        modest = sample_pattern("stone", self.u, self.v, wealth="MODEST")
        affluent = sample_pattern("stone", self.u, self.v, wealth="AFFLUENT")
        self.assertGreater(np.mean(rough["roughness"]), np.mean(baseline["roughness"]))
        self.assertGreater(np.mean(fine["roughness"]), 0)
        self.assertLess(np.mean(fine["height"]**2), np.mean(rough["height"]**2))
        self.assertFalse(np.array_equal(modest["albedo"], affluent["albedo"]))
        # Changing wealth does not change preparation; changing craft does not
        # rewrite the sorting/grade variation carried by albedo.
        np.testing.assert_array_equal(modest["height"], affluent["height"])
        np.testing.assert_array_equal(modest["roughness"], affluent["roughness"])
        np.testing.assert_array_equal(rough["albedo"], fine["albedo"])

    def test_coordinates_are_continuous_across_small_steps(self):
        a = sample_pattern("wood", np.array([.123]), np.array([.234]), seed=5)
        b = sample_pattern("wood", np.array([.123001]), np.array([.234001]), seed=5)
        self.assertLess(abs(a["height"][0] - b["height"][0]), 1e-7)
        self.assertLess(abs(a["albedo"][0, 0] - b["albedo"][0, 0]), 1e-4)

    def test_wood_preparation_and_stock_sorting_change_surface_detail(self):
        rough = sample_pattern("wood", self.u, self.v, craftsmanship="ROUGH", seed=71)
        fine = sample_pattern("wood", self.u, self.v, craftsmanship="FINE", seed=71)
        modest = sample_pattern("wood", self.u, self.v, wealth="MODEST", seed=71)
        affluent = sample_pattern("wood", self.u, self.v, wealth="AFFLUENT", seed=71)
        self.assertGreater(np.ptp(rough["height"]), .0005)
        self.assertGreater(np.mean(rough["height"]**2), np.mean(fine["height"]**2))
        self.assertFalse(np.array_equal(modest["height"], affluent["height"]))
        self.assertGreater(np.std(modest["albedo"]), np.std(affluent["albedo"]))
        # The relief stays in the shallow, millimetric range instead of forming
        # oversized grooves or stylized striping.
        self.assertLess(np.max(np.abs(rough["height"])), .002)

    def test_inputs_broadcast_and_invalid_families_are_rejected(self):
        result = sample_pattern("iron", np.array([0., 1.]), 0.)
        self.assertEqual(result["height"].shape, (2,))
        with self.assertRaises(ValueError):
            sample_pattern("brick_wall", [0.], [0.])


if __name__ == "__main__":
    unittest.main(verbosity=2)
