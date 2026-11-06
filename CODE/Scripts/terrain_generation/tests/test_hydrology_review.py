"""Independent terrain checks; the raster, not authored profile claims, is the oracle.

The D8 equations are reproduced here independently of generation/conditioning. These
are topographic routing tests, not discharge, groundwater, or flood-frequency models.
"""
from __future__ import annotations

import math
import json
from collections import deque
from pathlib import Path
import sys
import unittest

import numpy as np

SCRIPT_DIRECTORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIRECTORY))


def independent_d8(height, cell_size_m, outlet):
    """Route an unconditioned inspection field without calling the generator's D8."""
    z = np.asarray(height, dtype=np.float64)
    ny, nx = z.shape
    padded = np.pad(z, 1, constant_values=np.inf)
    padded_ids = np.pad(np.arange(z.size).reshape(z.shape), 1, constant_values=-2)
    best = np.zeros_like(z)
    receiver = np.full(z.shape, -2, dtype=np.int64)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0:
                continue
            values = padded[1+dr:1+dr+ny, 1+dc:1+dc+nx]
            slope = (z-values)/(cell_size_m*math.hypot(dr, dc))
            select = slope > best
            receiver[select] = padded_ids[1+dr:1+dr+ny, 1+dc:1+dc+nx][select]
            best[select] = slope[select]
    receiver.reshape(-1)[outlet] = -1
    accumulation = np.ones(z.size, dtype=np.int64)
    for index in np.argsort(z.reshape(-1), kind="stable")[::-1]:
        target = receiver.reshape(-1)[index]
        if target >= 0:
            accumulation[target] += accumulation[index]
    return receiver, accumulation.reshape(z.shape)


def connected_to_reference(height, water_level_m, reference_cell):
    """Independent fixed-level inundation from one declared river reference.

    Other isolated wet pools are deliberately not new seeds. This is a static
    topographic connectivity screen, not a discharge or flood-frequency model.
    """
    ny, nx = height.shape
    eligible = np.asarray(height) <= water_level_m
    reached = np.zeros(height.shape, dtype=bool)
    row, col = divmod(int(reference_cell), nx)
    if not eligible[row, col]:
        raise AssertionError("Declared river reference lies above the tested water level")
    queue = deque([(row, col)])
    reached[row, col] = True
    while queue:
        row, col = queue.popleft()
        for rr in range(max(0, row-1), min(ny, row+2)):
            for cc in range(max(0, col-1), min(nx, col+2)):
                if eligible[rr, cc] and not reached[rr, cc]:
                    reached[rr, cc] = True
                    queue.append((rr, cc))
    return reached


def review_routing(height, receiver, accumulation, cell_size_m, allowed_outlets=None):
    """Check actual DEM descent, D8 steepest slope, drainage, and contributing area."""
    z = np.asarray(height, dtype=np.float64)
    rec = np.asarray(receiver).reshape(-1)
    accum = np.asarray(accumulation).reshape(-1)
    if z.ndim != 2 or not np.isfinite(z).all() or cell_size_m <= 0:
        raise AssertionError("Finite two-dimensional DEM and positive metric spacing required")
    ny, nx = z.shape
    count = z.size
    if rec.size != count or accum.size != count or rec.dtype.kind not in "iu":
        raise AssertionError("Receiver and accumulation shapes/types must match the DEM")
    if np.any(rec < -1) or np.any(rec >= count):
        raise AssertionError("Receiver outside the DEM")
    outlets = np.flatnonzero(rec == -1)
    if len(outlets) == 0:
        raise AssertionError("No declared drainage outlet")
    if allowed_outlets is not None:
        if not set(map(int, outlets)).issubset(set(map(int, allowed_outlets))):
            raise AssertionError("An undeclared interior/boundary sink was substituted for drainage")
    elif any(0 < i // nx < ny - 1 and 0 < i % nx < nx - 1 for i in outlets):
        raise AssertionError("An interior sink is not a boundary outlet")

    # Independent eight-neighbour gradient, with diagonal distance sqrt(2)*dx.
    padded = np.pad(z, 1, constant_values=np.inf)
    steepest = np.full_like(z, -np.inf)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0:
                continue
            adjacent = padded[1 + dr:1 + dr + ny, 1 + dc:1 + dc + nx]
            slope = (z - adjacent) / (cell_size_m * math.hypot(dr, dc))
            steepest = np.maximum(steepest, slope)

    active = np.flatnonzero(rec >= 0)
    target = rec[active]
    dr = target // nx - active // nx
    dc = target % nx - active % nx
    if np.any(np.abs(dr) > 1) or np.any(np.abs(dc) > 1) or np.any((dr == 0) & (dc == 0)):
        raise AssertionError("Receiver jumps across terrain or points to itself")
    drops = z.reshape(-1)[active] - z.reshape(-1)[target]
    if np.any(drops <= 0):
        raise AssertionError("Actual DEM receiver is flat/uphill; a profile annotation cannot fix it")
    selected = drops / (cell_size_m * np.hypot(dr, dc))
    np.testing.assert_allclose(selected, steepest.reshape(-1)[active], rtol=1e-10, atol=1e-10,
                               err_msg="Actual receiver is not a D8 steepest descent")

    # Strict descent above proves acyclicity. Recompute accumulation independently by
    # sorting actual elevation; a fake receiver tree or reported metric cannot pass.
    expected = np.ones(count, dtype=np.int64)
    for index in np.argsort(z.reshape(-1), kind="stable")[::-1]:
        dest = rec[index]
        if dest >= 0:
            expected[dest] += expected[index]
    np.testing.assert_array_equal(accum, expected, err_msg="Contributing cell counts do not conserve area")
    if int(expected[outlets].sum()) != count:
        raise AssertionError("Some raster area does not reach the declared outlets")
    return {"cells": count, "outlets": len(outlets), "minimum_receiver_drop_m": float(drops.min()),
            "sample_count_area_proxy_m2": count * cell_size_m**2}


def _synthetic_slope():
    n = 6
    z = np.add.outer(np.arange(n, 0, -1), np.arange(n, 0, -1)).astype(float)
    receiver = np.empty(n*n, dtype=np.int64)
    for row in range(n):
        for col in range(n):
            receiver[row*n + col] = (min(row+1, n-1)*n + min(col+1, n-1)
                                    if row != n-1 or col != n-1 else -1)
    accumulation = np.ones(n*n, dtype=np.int64)
    for index in np.argsort(z.reshape(-1))[::-1]:
        if receiver[index] >= 0:
            accumulation[receiver[index]] += accumulation[index]
    return z, receiver, accumulation


class IndependentOracleTests(unittest.TestCase):
    def test_actual_slope_conserves_contributing_area(self):
        z, receiver, accumulation = _synthetic_slope()
        report = review_routing(z, receiver, accumulation, 8, [35])
        self.assertEqual(report["sample_count_area_proxy_m2"], 36*64)

    def test_dammed_dem_rejected_even_if_profile_metadata_still_descends(self):
        z, receiver, accumulation = _synthetic_slope()
        z[1, 1] = z[0, 0] + 2
        with self.assertRaisesRegex(AssertionError, "flat/uphill"):
            review_routing(z, receiver, accumulation, 8, [35])

    def test_fabricated_tree_cannot_jump_across_a_watershed(self):
        z, receiver, accumulation = _synthetic_slope()
        receiver[0] = 35
        with self.assertRaisesRegex(AssertionError, "jumps"):
            review_routing(z, receiver, accumulation, 8, [35])

    def test_interior_terminal_is_not_a_valid_outlet(self):
        z, receiver, accumulation = _synthetic_slope()
        receiver[14] = -1
        with self.assertRaisesRegex(AssertionError, "undeclared"):
            review_routing(z, receiver, accumulation, 8, [35])

    def test_contributing_area_is_not_just_a_positive_number(self):
        z, receiver, accumulation = _synthetic_slope()
        accumulation[35] -= 1
        with self.assertRaisesRegex(AssertionError, "Contributing"):
            review_routing(z, receiver, accumulation, 8, [35])


class LowmarkActualTerrainTests(unittest.TestCase):
    """Read approved-map controls and inspect the actual 8 m Lowmark rasters."""

    @classmethod
    def setUpClass(cls):
        from terrain import generate
        cls.controls = json.loads((SCRIPT_DIRECTORY / "lowmark_controls.json").read_text(encoding="utf-8-sig"))
        cls.result = generate(cls.controls, 8.0)
        cls.nodes = {n["id"]: n for n in cls.controls["hydrology"]["nodes"]}
        cls.outlet = cls.cell_for_node(cls.controls["hydrology"]["outlet"])

    @classmethod
    def cell_for_node(cls, name):
        world = cls.controls["world"]
        x, y = np.asarray(cls.nodes[name]["xy"])*[world["width_m"], world["height_m"]]
        return int(round(y/8))*len(cls.result.x) + int(round(x/8))

    def test_final_natural_dem_not_a_reported_profile_drains_and_conserves(self):
        result = self.result
        reviewed = review_routing(result.height, result.receiver, result.accumulation, 8, [self.outlet])
        self.assertEqual(reviewed["cells"], result.height.size)
        self.assertEqual(reviewed["outlets"], 1)

    def test_natural_channel_sections_remain_connected_and_descend_in_actual_raster(self):
        result = self.result
        field = result.height.reshape(-1)
        receiver = result.receiver.reshape(-1)
        for channel in result.channels:
            with self.subTest(reach=channel["id"]):
                path = np.asarray(channel["path"])
                self.assertTrue(np.all(np.diff(field[path]) < 0), "Actual raster has a channel step-up")
                rows, cols = path//len(result.x), path % len(result.x)
                self.assertTrue(np.all(np.abs(np.diff(rows)) <= 1))
                self.assertTrue(np.all(np.abs(np.diff(cols)) <= 1))
                # A middle-of-reach start avoids pretending one D8 receiver can
                # represent all three simultaneous wetland distributary flows.
                cursor = int(path[len(path)//2])
                for _ in range(result.height.size):
                    if cursor < 0:
                        break
                    self.assertLessEqual(float(result.channel_distance.reshape(-1)[cursor]),
                                         max(c["half_width_m"] for c in result.channels)+8*math.sqrt(2),
                                         "River drainage shortcut leaves every approved channel corridor")
                    cursor = int(receiver[cursor])
                self.assertEqual(cursor, -1, "A natural channel terminates before the region outlet")

    def test_named_junction_water_levels_and_topology_are_continuous(self):
        seen = {}
        for channel in self.result.channels:
            for node_id, index in ((channel["from"], 0), (channel["to"], -1)):
                level = float(channel["water_m"][index])
                self.assertAlmostEqual(level, float(self.nodes[node_id]["water_level_m"]), places=7)
                if node_id in seen:
                    self.assertAlmostEqual(level, seen[node_id], places=7)
                seen[node_id] = level
        natural_pairs = {(c["from"], c["to"]) for c in self.result.channels}
        main = ["head", "falls_lip", "falls_base", "fen_in", "fen_mid1", "fen_mid2", "fen_mid3",
                "fen_out", "crest", "mill_intake", "weir_up", "weir_down", "whisper", "lowerbend",
                "brook_reach", "grey_confluence", "outlet"]
        for pair in zip(main, main[1:]):
            self.assertIn(pair, natural_pairs, "Approved major river relationship lost")
        self.assertIn(("grey_lower", "grey_confluence"), natural_pairs)

    def test_waterfall_drop_is_present_in_actual_grid_and_not_regionally_smoothed(self):
        falls = next(c for c in self.result.channels if c["id"] == "veilwater_falls")
        actual = self.result.height.reshape(-1)[falls["path"]]
        expected_drop = self.nodes["falls_lip"]["bed_m"]-self.nodes["falls_base"]["bed_m"]
        self.assertGreater(expected_drop, 0)
        self.assertAlmostEqual(float(actual[0]-actual[-1]), expected_drop, places=6)
        self.assertLess(falls["length_m"], 64, "Declared short falls transition smeared into a regional ramp")
        self.assertGreater(float(np.max(-np.diff(actual))), expected_drop/len(actual),
                           "No localized steep waterfall drop remains")

    def test_no_pathological_neighbour_cliff_away_from_declared_falls(self):
        reach = next(r for r in self.controls["hydrology"]["reaches"] if r["id"] == "veilwater_falls")
        points = np.asarray(reach["points"])*[self.controls["world"]["width_m"],
                                              self.controls["world"]["height_m"]]
        xx, yy = np.meshgrid(self.result.x, self.result.y)
        distance_squared = np.full(xx.shape, np.inf)
        # Independent metric distance to the authored segment/polyline, not a
        # generator mask which could accidentally conceal the same bad seam.
        for start, end in zip(points[:-1], points[1:]):
            delta = end-start
            length_squared = float(delta @ delta)
            self.assertGreater(length_squared, 0)
            t = np.clip(((xx-start[0])*delta[0]+(yy-start[1])*delta[1])/length_squared, 0, 1)
            dx = xx-start[0]-t*delta[0]
            dy = yy-start[1]-t*delta[1]
            distance_squared = np.minimum(distance_squared, dx*dx+dy*dy)
        outside_falls = distance_squared > 200**2
        ny, nx = xx.shape
        for name, height in (("natural", self.result.height), ("open_engineered", self.result.height_engineered)):
            maximum = -math.inf
            endpoints = None
            # Four undirected orientations cover all eight neighbours, including
            # diagonal edges. This is a seam regression, not a slope safety code.
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                row0, row1 = max(0, -dr), min(ny, ny-dr)
                col0, col1 = max(0, -dc), min(nx, nx-dc)
                first = (slice(row0, row1), slice(col0, col1))
                second = (slice(row0+dr, row1+dr), slice(col0+dc, col1+dc))
                eligible = outside_falls[first] & outside_falls[second]
                difference = np.where(eligible, np.abs(height[first]-height[second]), -math.inf)
                index = int(np.argmax(difference))
                local_row, local_col = np.unravel_index(index, difference.shape)
                candidate = float(difference[local_row, local_col])
                if candidate > maximum:
                    maximum = candidate
                    row, col = local_row+row0, local_col+col0
                    endpoints = [[float(self.result.x[col]), float(self.result.y[row])],
                                 [float(self.result.x[col+dc]), float(self.result.y[row+dr])]]
            print(f"INDEPENDENT_CONTINUITY {name} max_neighbour_jump_m={maximum:.9f} endpoints_m={endpoints}")
            self.assertLess(maximum, 20,
                            f"{name} DEM has a pathological {maximum:.6f} m neighbour cliff away from Falls at {endpoints}")

    def test_fen_keeps_shallow_wet_channels_and_drier_marsh_microrelief(self):
        result = self.result
        fen = np.asarray(result.fen_mask, dtype=bool)
        self.assertTrue(fen.any(), "Approved fen disappeared")
        self.assertTrue(np.isfinite(result.water_level[fen]).all())
        wet = result.height[fen] < result.water_level[fen]
        self.assertGreater(float(wet.mean()), 0, "No fen wet ground or pools remain")
        self.assertLess(float(wet.mean()), 1, "Every fen cell became one excavated lake")
        depth = result.water_level[fen]-result.height[fen]
        self.assertLess(float(np.percentile(depth, 95)), 2,
                        "Technical shallow-fen scenario became deep open water")
        dy, dx = np.gradient(result.height, 8)
        gradient = np.hypot(dx[fen], dy[fen])
        self.assertLess(float(np.median(gradient)), 0.03,
                        "Fen median gradient no longer resembles a low-relief marsh")

    def test_orchard_soil_and_berms_have_actual_seasonal_river_connectivity(self):
        result = self.result
        plain = next(p for p in self.controls["floodplains"] if p["id"] == "floodplain_orchards")
        xx, yy = np.meshgrid(result.x, result.y)
        vertices = np.asarray(plain["polygon"])*[self.controls["world"]["width_m"],
                                               self.controls["world"]["height_m"]]
        inside = np.zeros(result.height.shape, dtype=bool)
        # Independent point-in-polygon parity, not the generator's exported mask.
        for start, end in zip(vertices, np.roll(vertices, -1, axis=0)):
            if start[1] == end[1]:
                continue
            crosses = (start[1] > yy) != (end[1] > yy)
            intersect_x = start[0]+(yy-start[1])*(end[0]-start[0])/(end[1]-start[1])
            inside ^= crosses & (xx < intersect_x)
        self.assertTrue(inside.any(), "Mapped orchard polygon disappeared")
        actual_masks = result.floodplain_masks[plain["id"]]
        np.testing.assert_array_equal(actual_masks["mask"], inside)
        reference = self.cell_for_node(plain["reference_node"])
        stage = float(self.nodes[plain["reference_node"]]["water_level_m"])
        rise = float(self.controls["world"]["flood_scenario_rise_m"])
        self.assertTrue(np.all(result.height[inside] > stage), "Orchard became permanent open water")
        self.assertFalse(np.any(result.channel_mask[inside]), "An unapproved river was added through the orchard")
        normal = connected_to_reference(result.height, stage, reference) & inside
        seasonal = connected_to_reference(result.height, stage+rise, reference) & inside
        self.assertFalse(normal.any())
        self.assertGreater(float(seasonal[inside].mean()), 0, "Low orchard ground is isolated from its river")
        self.assertLess(float(seasonal[inside].mean()), 1, "Scenario drowns every orchard cell")
        np.testing.assert_array_equal(actual_masks["normal_water"], normal)
        np.testing.assert_array_equal(actual_masks["scenario_exposed"], seasonal,
                                      err_msg="Reported flood exposure includes ground disconnected from its reference river")
        angle = math.radians(plain["berm_angle_degrees"])
        along = xx*math.cos(angle)+yy*math.sin(angle)
        spacing = float(plain["berm_spacing_m"])
        phase = (along+spacing/2) % spacing-spacing/2
        berm = inside & (np.abs(phase) <= plain["berm_width_m"]*math.sqrt(math.log(2)))
        np.testing.assert_array_equal(actual_masks["berm"], berm)
        soil = inside & ~berm
        self.assertTrue(berm.any() and soil.any(), "No distinction between planting berms and ordinary soil")
        self.assertGreater(float((~seasonal[berm]).mean()), 0, "Every planting berm is submerged")
        self.assertLess(float((~seasonal[berm]).mean()), 1, "Berms have no actual interaction with seasonal exposure")
        self.assertTrue(np.any(seasonal & soil), "No ordinary orchard soil receives connected seasonal water")
        self.assertTrue(np.any(soil & ~seasonal), "Every ordinary soil cell became permanently exposed in the scenario")

    def test_conditioning_budget_checks_the_actual_height_change(self):
        delta = self.result.height-self.result.height_raw
        self.assertTrue(np.all(delta >= -1e-9), "Upward conditioning silently carved arbitrary extra outlets")
        budget = self.controls["world"].get("maximum_conditioning_raise_m", 12)
        self.assertLessEqual(float(delta.max()), budget, "Concealed large terrain repair exceeds declared budget")

    def test_open_engineered_terrain_has_no_undeclared_sink_or_false_uphill_flow(self):
        receiver, accumulation = independent_d8(self.result.height_engineered, 8, self.outlet)
        sinks = np.flatnonzero(receiver.reshape(-1) == -2)
        self.assertEqual(len(sinks), 0,
                         f"Open engineered ground has {len(sinks)} actual D8 sinks; sample cells={sinks[:12].tolist()}")
        review_routing(self.result.height_engineered, receiver, accumulation, 8, [self.outlet])

    def test_uphill_canal_is_a_measured_exception_and_not_a_natural_receiver_edge(self):
        natural = {c["id"] for c in self.result.channels}
        lift = next(r for r in self.controls["hydrology"]["reaches"] if r["id"] == "uphill_canal_lift")
        self.assertNotIn(lift["id"], natural)
        self.assertEqual(lift["kind"], "anomalous_engineered")
        self.assertFalse(lift["passive_flow"])
        head = self.nodes[lift["to"]]["water_level_m"]-self.nodes[lift["from"]]["water_level_m"]
        self.assertGreater(head, 0)
        self.assertAlmostEqual(head, lift["positive_head_m"], places=7)
        self.assertIn("UNKNOWN", lift["energy_source"])

if __name__ == "__main__":
    unittest.main()
