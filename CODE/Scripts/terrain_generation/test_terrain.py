"""Small deterministic regression fixtures for the offline mathematical core."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

import numpy as np

from terrain import adjacent_jump_report, apply_local_bank_constraints, channel_constraints, connected_stage_screen, d8_receivers, export, generate, path_to_outlet


def controls_fixture():
    return {
        "world": {"width_m": 256, "height_m": 256, "base_elevation_m": 26,
                  "maximum_conditioning_raise_m": 12},
        "landforms": [{"id": "ridge", "xy": [0.8, 0.7], "amplitude_m": 12, "radius_m": 80}],
        "hydrology": {
            "outlet": "outlet",
            "nodes": [{"id": "head", "xy": [0.5, 1], "bed_m": 20},
                      {"id": "junction", "xy": [0.5, 0.5], "bed_m": 10},
                      {"id": "tributary", "xy": [0.0, 0.5], "bed_m": 16},
                      {"id": "outlet", "xy": [0.5, 0], "bed_m": 0},
                      {"id": "anomaly_top", "xy": [0.2, 0.4], "bed_m": 24}],
            "reaches": [
                {"id": "upper", "from": "head", "to": "junction", "points": [[0.5, 1], [0.5, 0.5]], "half_width_m": 8},
                {"id": "lower", "from": "junction", "to": "outlet", "points": [[0.5, 0.5], [0.5, 0]], "half_width_m": 8},
                {"id": "tributary", "from": "tributary", "to": "junction", "points": [[0, 0.5], [0.5, 0.5]], "half_width_m": 8},
                {"id": "unresolved_canal", "from": "junction", "to": "anomaly_top", "points": [[0.5, 0.5], [0.2, 0.4]], "kind": "anomalous_engineered"}
            ]},
        "settlements": [{"id": "town", "xy": [0.75, 0.25], "span_m": [70, 100],
                         "buildings": [2, 4], "footprint_m2": 120, "min_freeboard_m": 1,
                         "max_building_slope_deg": 20, "policy": "village"}]
    }


class TerrainCoreTests(unittest.TestCase):
    def test_continuity_diagnostic_exposes_an_offsite_height_step(self):
        height = np.zeros((12, 12))
        height[:, 6:] = 100
        x = np.arange(12, dtype=float) * 8
        report = adjacent_jump_report(height, x, x, controls_fixture())
        self.assertEqual(report["maximum_eight_neighbor_jump_outside_waterfalls_m"], 100)
        self.assertIsNotNone(report["edge_endpoints_east_north_m"])

    def test_distant_high_river_cannot_impose_a_voronoi_cliff(self):
        config = controls_fixture()
        config["world"].update(width_m=1024, height_m=1024)
        for node in config["hydrology"]["nodes"]:
            if node["id"] == "head": node["bed_m"] = 100
            if node["id"] == "junction": node["bed_m"] = 50
            if node["id"] == "tributary": node["bed_m"] = 90
        x = np.linspace(0, 1024, 129)
        xx, yy = np.meshgrid(x, x)
        original = np.full(xx.shape, 20.0)
        prepared = channel_constraints(config, original, xx, yy, 8)
        fixed, distance = prepared[1], prepared[-2]
        modified = apply_local_bank_constraints(prepared[0], fixed, prepared[4], xx, yy)
        distant = distance > 300
        self.assertTrue(distant.any())
        np.testing.assert_array_equal(modified[distant], original[distant],
                                      err_msg="A distant high reach raised unrelated terrain across its nearest-channel Voronoi region")
        self.assertEqual(modified[-1, 64], 100)
        self.assertEqual(fixed[-1, 64], 100)
        self.assertGreater(modified[-1, 63], modified[-1, 64], "The compact local bank must still contain the retained high channel.")

    def test_reproducibility_and_independent_drainage(self):
        first = generate(controls_fixture(), 8)
        second = generate(controls_fixture(), 8)
        np.testing.assert_array_equal(first.height, second.height)
        np.testing.assert_array_equal(first.receiver, second.receiver)
        self.assertTrue(first.metrics["all_cells_reach_outlet"])
        self.assertEqual(first.metrics["unintended_sinks"], 0)
        self.assertTrue(first.metrics["channel_constraints_exact"])
        self.assertTrue(np.all(first.height >= first.height_raw))
        flat, receiver = first.height.ravel(), first.receiver.ravel()
        selected = receiver >= 0
        self.assertTrue(np.all(flat[selected] > flat[receiver[selected]]))
        for channel in first.channels:
            self.assertTrue(np.all(np.diff(first.height.ravel()[channel["path"]]) < 0))
            self.assertEqual(path_to_outlet(channel["path"][0], first.receiver)[1], -1)

    def test_reject_uphill_natural_profile(self):
        config = controls_fixture()
        config["hydrology"]["nodes"][0]["bed_m"] = 5
        with self.assertRaisesRegex(ValueError, "descend strictly"):
            generate(config, 8)

    def test_anomaly_is_not_fabricated_gravity_flow(self):
        result = generate(controls_fixture(), 8)
        anomaly = result.metrics["engineered_reaches"][0]
        self.assertEqual(anomaly["positive_head_requirement_m"], 14)
        self.assertFalse(anomaly["passive_gravity_feasible"])
        self.assertIn("unknown_energy", anomaly["status"])
        self.assertEqual(len(result.channels), 3)

    def test_real_dem_damage_is_detected(self):
        result = generate(controls_fixture(), 8)
        damaged = result.height.copy()
        damaged[0:3, 14:19] += 50
        rerouted = d8_receivers(damaged, 8, result.metrics["outlet_cell"])
        self.assertTrue(np.any(rerouted == -2))

    def test_settlement_capacity_never_flattens_land(self):
        config = controls_fixture()
        with_settlement = generate(config, 8)
        config["settlements"] = []
        without = generate(config, 8)
        np.testing.assert_array_equal(with_settlement.height, without.height)
        capacity = with_settlement.metrics["settlements"][0]
        self.assertEqual(capacity["grading_m3"], 0)
        self.assertLessEqual(capacity["min_span_screened_roof_capacity"], capacity["screened_roof_capacity"])

    def test_constant_stage_wetland_has_finite_blended_apron(self):
        config = controls_fixture()
        config["wetlands"] = [{"id": "test_fen", "polygon": [[0.2, 0.3], [0.8, 0.3], [0.8, 0.6], [0.2, 0.6]],
                               "water_level_m": 14, "bed_depth_m": 0.6, "shore_apron_m": 8, "outer_transition_m": 40}]
        result = generate(config, 8)
        self.assertTrue(np.isfinite(result.height).all())
        self.assertTrue(result.fen_mask.any())

    def test_candidate_footprints_exclude_actual_open_waterworks(self):
        config = controls_fixture()
        config["hydrology"]["reaches"].append({"id": "trial_cut", "kind": "engineered", "from": "junction", "to": "outlet",
                                                "points": [[0.5, 0.5], [0.75, 0.25], [0.5, 0]], "half_width_m": 8})
        result = generate(config, 8)
        masks = result.settlement_masks["town"]
        self.assertTrue(masks["engineering_exclusion"].any())
        self.assertFalse((masks["candidate"] & masks["engineering_exclusion"]).any())
        self.assertIn("Combined open-design terrain", result.metrics["settlements"][0]["capacity_terrain_state"])

    def test_stage_screen_does_not_flood_disconnected_low_pockets(self):
        height = np.full((9, 9), 3.0)
        height[:, 0] = 0
        height[4, 4] = 0.5
        stage = np.zeros_like(height)
        water = np.full_like(height, np.nan)
        water[:, 0] = 0.25
        exposed = connected_stage_screen(height, stage, water, 1.5)
        self.assertTrue(exposed[:, 0].all())
        self.assertFalse(exposed[4, 4])

    def test_flood_screen_capacity_never_counts_exposed_footprints_safe(self):
        result = generate(controls_fixture(), 8)
        report = result.metrics["settlements"][0]
        masks = result.settlement_masks["town"]
        self.assertLessEqual(report["flood_scenario_safe_capacity"], report["normal_stage_roof_capacity"])
        self.assertFalse((masks["scenario_candidate"] & masks["scenario_exposed"]).any())

    def test_saved_arrays_and_exports_are_deterministic(self):
        result = generate(controls_fixture(), 8)
        scratch = Path(__file__).with_name(".scratch")
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as first, tempfile.TemporaryDirectory(dir=scratch) as second:
            export(result, first)
            export(result, second)
            for name in ["height.npy", "height.png", "terrain.obj", "calibration.json", "terrain_arrays.npz"]:
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())
            saved = np.load(Path(first) / "height.npy", allow_pickle=False)
            np.testing.assert_array_equal(saved, result.height.astype("<f4"))


if __name__ == "__main__":
    unittest.main()
