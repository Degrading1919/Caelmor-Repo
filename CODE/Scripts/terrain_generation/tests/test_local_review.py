"""Independent local-refinement geometry and drainage acceptance checks."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np

SCRIPT_DIRECTORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIRECTORY))
from tests.test_hydrology_review import independent_d8, review_routing


def regional_triangle_height(height, x, y, sample_x, sample_y):
    """Actual SW--NE regional mesh surface, independently evaluated in metres."""
    sample_x, sample_y = np.broadcast_arrays(sample_x, sample_y)
    if np.any(sample_x < x[0]) or np.any(sample_x > x[-1]) or np.any(sample_y < y[0]) or np.any(sample_y > y[-1]):
        raise AssertionError("Local point lies outside its parent terrain frame")
    col = np.clip(np.searchsorted(x, sample_x, side="right")-1, 0, len(x)-2)
    row = np.clip(np.searchsorted(y, sample_y, side="right")-1, 0, len(y)-2)
    u = (sample_x-x[col])/(x[col+1]-x[col])
    v = (sample_y-y[row])/(y[row+1]-y[row])
    sw, se = height[row, col], height[row, col+1]
    nw, ne = height[row+1, col], height[row+1, col+1]
    return np.where(v <= u, sw+u*(se-sw)+v*(ne-se), sw+u*(ne-nw)+v*(nw-sw))


def review_world_grid(patch, bounds=None):
    x, y, height = np.asarray(patch.x), np.asarray(patch.y), np.asarray(patch.height)
    if height.shape != (len(y), len(x)) or not np.isfinite(height).all():
        raise AssertionError("Local terrain array shape or elevation is invalid")
    for coordinate in (x, y):
        if len(coordinate) < 2 or not np.allclose(np.diff(coordinate), coordinate[1]-coordinate[0], atol=1e-12, rtol=0):
            raise AssertionError("Local grid is not uniform")
        if not 1 <= coordinate[1]-coordinate[0] <= 2:
            raise AssertionError("Local grid must increase east/north at actual 1--2 m spacing")
    if bounds is not None:
        np.testing.assert_array_equal([x[0], y[0], x[-1], y[-1]], bounds,
                                      err_msg="Local coordinates were re-centred or changed datum")


def review_seam(patch, parent_height, parent_x, parent_y):
    review_world_grid(patch)
    xx, yy = np.meshgrid(patch.x, patch.y)
    border = np.zeros(patch.height.shape, dtype=bool)
    border[[0, -1], :] = True
    border[:, [0, -1]] = True
    expected = regional_triangle_height(parent_height, parent_x, parent_y, xx[border], yy[border])
    np.testing.assert_allclose(patch.height[border], expected, rtol=0, atol=1e-9,
                               err_msg="Local border no longer meets the saved regional mesh")


def review_overlap(first, second):
    _, ax, bx = np.intersect1d(first.x, second.x, assume_unique=True, return_indices=True)
    _, ay, by = np.intersect1d(first.y, second.y, assume_unique=True, return_indices=True)
    if len(ax) and len(ay):
        np.testing.assert_allclose(first.height[np.ix_(ay, ax)], second.height[np.ix_(by, bx)],
                                   rtol=0, atol=1e-9, err_msg="Shared local terrain has conflicting heights")


def review_local_drainage(patch):
    """Use actual halo gradients; boundary membership alone never grants an exit."""
    row0, row1, col0, col1 = map(int, patch.owned_slice)
    halo = np.asarray(patch.halo_height)
    ny, nx = patch.height.shape
    hny, hnx = halo.shape
    np.testing.assert_array_equal(halo[row0:row1, col0:col1], patch.height)
    if row0 < 1 or col0 < 1 or row1 >= hny or col1 >= hnx:
        raise AssertionError("Published local grid needs a real external neighbour halo")
    resolution = float(patch.x[1]-patch.x[0])
    core_halo_ids = (np.arange(row0, row1)[:, None]*hnx+np.arange(col0, col1)[None, :]).reshape(-1)
    selected = np.asarray(patch.halo_receiver).reshape(-1)[core_halo_ids]
    if np.any(selected < 0) or np.any(selected >= halo.size):
        raise AssertionError("Owned point terminates before its actual halo neighbour")
    rr = selected//hnx-row0
    cc = selected % hnx-col0
    inside = (rr >= 0) & (rr < ny) & (cc >= 0) & (cc < nx)
    expected_receivers = np.where(inside, rr*nx+cc, -1).reshape(ny, nx)
    np.testing.assert_array_equal(patch.receiver, expected_receivers,
                                  err_msg="A boundary was declared an outlet without actual downstream continuation")
    dr = selected//hnx-core_halo_ids//hnx
    dc = selected % hnx-core_halo_ids % hnx
    if np.any(np.abs(dr) > 1) or np.any(np.abs(dc) > 1) or np.any((dr == 0) & (dc == 0)):
        raise AssertionError("Local halo receiver jumps over terrain")
    drops = halo.reshape(-1)[core_halo_ids]-halo.reshape(-1)[selected]
    if np.any(drops <= 0):
        raise AssertionError("Actual local halo route points flat or uphill")
    maximum = np.full((ny, nx), -np.inf)
    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if row_offset == col_offset == 0:
                continue
            neighbour = halo[row0+row_offset:row1+row_offset, col0+col_offset:col1+col_offset]
            gradient = (patch.height-neighbour)/(resolution*np.hypot(row_offset, col_offset))
            maximum = np.maximum(maximum, gradient)
    np.testing.assert_allclose(drops/(resolution*np.hypot(dr, dc)), maximum.reshape(-1), rtol=1e-10, atol=1e-10,
                               err_msg="Local receiver is not actual steepest D8 descent")
    receiver = np.asarray(patch.receiver).reshape(-1)
    expected_accumulation = np.ones(ny*nx, dtype=np.int64)
    for index in np.argsort(patch.height.reshape(-1), kind="stable")[::-1]:
        target = receiver[index]
        if target >= 0:
            expected_accumulation[target] += expected_accumulation[index]
    np.testing.assert_array_equal(np.asarray(patch.accumulation).reshape(-1), expected_accumulation,
                                  err_msg="Owned-sample local accumulation does not conserve area")
    exits = receiver == -1
    if int(expected_accumulation[exits].sum()) != ny*nx:
        raise AssertionError("Some refined terrain fails to reach a real boundary continuation")
    return {"owned_samples": ny*nx, "exits": int(exits.sum()), "minimum_drop_m": float(drops.min())}


def source_stage_at(controls, x, y):
    """Independent nearest authored water-course reference at footprint points."""
    x, y = np.broadcast_arrays(x, y)
    nearest = np.full(x.shape, np.inf)
    reference = np.zeros(x.shape)
    nodes = {n["id"]: n for n in controls["hydrology"]["nodes"]}
    for reach in controls["hydrology"]["reaches"]:
        points = np.asarray(reach["points"])*[controls["world"]["width_m"], controls["world"]["height_m"]]
        lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
        station = np.r_[0., np.cumsum(lengths)]
        best = np.full(x.shape, np.inf)
        at = np.zeros(x.shape)
        for index, (start, end) in enumerate(zip(points[:-1], points[1:])):
            delta = end-start
            fraction = np.clip(((x-start[0])*delta[0]+(y-start[1])*delta[1])/(lengths[index]**2), 0, 1)
            distance2 = (x-start[0]-fraction*delta[0])**2+(y-start[1]-fraction*delta[1])**2
            selected = distance2 < best
            best[selected] = distance2[selected]
            at[selected] = station[index]+fraction[selected]*lengths[index]
        profile = reach.get("profile")
        if profile:
            positions = np.asarray([p.get("fraction", p.get("t")) for p in profile])*station[-1]
            bed = np.asarray([p.get("z_m", p.get("bed_m")) for p in profile])
        else:
            positions = np.array([0., station[-1]])
            bed = np.array([nodes[reach["from"]]["bed_m"], nodes[reach["to"]]["bed_m"]])
        water = np.interp(at, positions, bed)+float(reach.get("water_depth_m", 1.2))
        chosen = best < nearest
        nearest[chosen], reference[chosen] = best[chosen], water[chosen]
    return reference


def review_footprint_clearance(height, stage, floor, normal_clearance, scenario_rise, floor_clearance, stilts=False):
    if floor < float(np.max(height))-1e-8:
        raise AssertionError("A proposed level floor intersects actual footprint ground")
    if not stilts and float(np.min(height-stage)) < normal_clearance-1e-8:
        raise AssertionError("A supposedly safe footprint has an unsafe corner or edge")
    if floor-float(np.max(stage))-scenario_rise < floor_clearance-1e-8:
        raise AssertionError("A supposedly safe floor lacks scenario freeboard")


def sampled_polyline(points, spacing=2):
    lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
    cumulative = np.r_[0., np.cumsum(lengths)]
    coordinates, stations = [], []
    for index, length in enumerate(lengths):
        fractions = np.arange(max(1, int(np.ceil(length/spacing))))/max(1, int(np.ceil(length/spacing)))
        coordinates.extend(points[index]+fractions[:, None]*(points[index+1]-points[index]))
        stations.extend(cumulative[index]+fractions*length)
    coordinates.append(points[-1]); stations.append(cumulative[-1])
    return np.asarray(coordinates), np.asarray(stations)


def distance_to_polyline(points, x, y):
    squared = np.full(x.shape, np.inf)
    for start, end in zip(points[:-1], points[1:]):
        delta = end-start
        t = np.clip(((x-start[0])*delta[0]+(y-start[1])*delta[1])/(delta @ delta), 0, 1)
        squared = np.minimum(squared, (x-start[0]-t*delta[0])**2+(y-start[1]-t*delta[1])**2)
    return np.sqrt(squared)


def _parent_fixture():
    x = np.array([0., 8., 16.])
    y = np.array([0., 8., 16.])
    height = np.array([[65., 65., 65.], [65., 66., 65.], [65., 65., 65.]])
    fine_x, fine_y = np.arange(0, 17, 2.), np.arange(0, 17, 2.)
    xx, yy = np.meshgrid(fine_x, fine_y)
    fine = regional_triangle_height(height, x, y, xx, yy)
    return height, x, y, SimpleNamespace(x=fine_x, y=fine_y, height=fine)


def _halo_fixture():
    x = np.arange(-2, 7, 2.)
    y = np.arange(-2, 7, 2.)
    xx, yy = np.meshgrid(x, y)
    halo = 100+xx*0.1+yy*0.2
    halo_receiver, _ = independent_d8(halo, 2, 0)
    height = halo[1:4, 1:4].copy()
    receiver = np.full((3, 3), -1, dtype=np.int64)
    for row in range(1, 3):
        for col in range(1, 3):
            receiver[row, col] = (row-1)*3+col-1
    accumulation = np.ones(9, dtype=np.int64)
    for index in np.argsort(height.reshape(-1))[::-1]:
        target = receiver.reshape(-1)[index]
        if target >= 0:
            accumulation[target] += accumulation[index]
    return SimpleNamespace(x=x[1:4], y=y[1:4], height=height, receiver=receiver,
                           accumulation=accumulation.reshape(3, 3), halo_height=halo,
                           halo_receiver=halo_receiver, owned_slice=(1, 4, 1, 4))


class LocalReviewOracleTests(unittest.TestCase):
    def test_mesh_triangle_is_not_bilinear_upsampling(self):
        height, x, y, patch = _parent_fixture()
        # SW and NE carry 65 and 66 m: the saved diagonal midpoint is 65.5 m.
        self.assertEqual(float(regional_triangle_height(height, x, y, 4., 4.)), 65.5)
        self.assertNotEqual(float(regional_triangle_height(height, x, y, 4., 4.)), 65.25)
        review_seam(patch, height, x, y)

    def test_changed_border_vertex_is_detected(self):
        height, x, y, patch = _parent_fixture()
        patch.height[0, 3] += 0.001
        with self.assertRaisesRegex(AssertionError, "border"):
            review_seam(patch, height, x, y)

    def test_reversed_north_axis_is_not_an_export_convention(self):
        _, _, _, patch = _parent_fixture()
        patch.y = patch.y[::-1]
        with self.assertRaisesRegex(AssertionError, "increase east/north"):
            review_world_grid(patch)

    def test_shared_xy_height_conflict_is_detected(self):
        _, _, _, first = _parent_fixture()
        second = SimpleNamespace(x=first.x.copy(), y=first.y.copy(), height=first.height.copy())
        second.height[3, 3] += 0.02
        with self.assertRaisesRegex(AssertionError, "conflicting"):
            review_overlap(first, second)

    def test_real_halo_continuation_and_area_are_verified(self):
        reviewed = review_local_drainage(_halo_fixture())
        self.assertEqual(reviewed["owned_samples"], 9)
        self.assertEqual(reviewed["exits"], 5)

    def test_north_boundary_is_not_automatically_an_outlet(self):
        patch = _halo_fixture()
        patch.receiver[2, 1] = -1
        with self.assertRaisesRegex(AssertionError, "boundary"):
            review_local_drainage(patch)

    def test_safe_centre_does_not_excuse_a_flood_exposed_footprint_corner(self):
        height = np.array([[2., 2.], [2., 0.8]])
        with self.assertRaisesRegex(AssertionError, "unsafe corner"):
            review_footprint_clearance(height, np.zeros_like(height), 3, 1.2, 1.5, 0.3)


class ActualLocalTerrainReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import local_refinement
        cls.module = local_refinement
        cls.regional_controls_path = SCRIPT_DIRECTORY / "lowmark_controls.json"
        cls.local_controls_path = SCRIPT_DIRECTORY / "local_controls.json"
        cls.controls = json.loads(cls.regional_controls_path.read_text(encoding="utf-8-sig"))
        cls.local = json.loads(cls.local_controls_path.read_text(encoding="utf-8-sig"))
        cls.repository = SCRIPT_DIRECTORY.parents[2]
        cls.regional_path = cls.repository / cls.local["regional_source"]
        cls.input_hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest()
                            for path in [cls.regional_path, cls.regional_controls_path, cls.local_controls_path]}
        with np.load(cls.regional_path, allow_pickle=False) as data:
            cls.parent_height = data["height_engineered"].copy()
            cls.parent_x, cls.parent_y = data["x"].copy(), data["y"].copy()
        cls.result = local_refinement.refine_all(cls.regional_path, cls.controls, cls.local)
        cls.specifications = {p["id"]: p for p in cls.local["patches"]}

    def test_all_four_sites_have_disjoint_or_joint_explicit_ownership(self):
        patches = {p.id: p for p in self.result.patches}
        self.assertEqual(set(patches), set(self.specifications))
        covered = {name for p in self.local["patches"] for name in p["settlement_ids"]}
        self.assertEqual(covered, {"crestbridge", "greyharrow", "reedmere", "drowsebank_mill"})
        self.assertIn("drowsebank_mill", self.specifications["crestbridge_mill"]["settlement_ids"])
        self.assertIn("crestbridge", self.specifications["crestbridge_mill"]["settlement_ids"])
        for index, first in enumerate(self.result.patches):
            for second in self.result.patches[index+1:]:
                review_overlap(first, second)
                overlap_x = min(first.x[-1], second.x[-1])-max(first.x[0], second.x[0])
                overlap_y = min(first.y[-1], second.y[-1])-max(first.y[0], second.y[0])
                self.assertFalse(overlap_x > 0 and overlap_y > 0,
                                 "Published independent tiles have duplicate interior ownership")

    def test_true_world_basis_and_exact_parent_mesh_seams(self):
        for patch in self.result.patches:
            with self.subTest(patch=patch.id):
                review_world_grid(patch, self.specifications[patch.id]["bounds_m"])
                review_seam(patch, self.parent_height, self.parent_x, self.parent_y)
                row0, row1, col0, col1 = patch.owned_slice
                np.testing.assert_array_equal(patch.halo_x[col0:col1], patch.x)
                np.testing.assert_array_equal(patch.halo_y[row0:row1], patch.y)

    def test_actual_halo_drainage_and_owned_accumulation(self):
        for patch in self.result.patches:
            with self.subTest(patch=patch.id):
                report = review_local_drainage(patch)
                self.assertGreater(report["exits"], 0)
                self.assertEqual(report["owned_samples"], patch.height.size)

    def test_actual_composite_regional_drainage_and_bounded_ownership(self):
        nodes = {n["id"]: n for n in self.controls["hydrology"]["nodes"]}
        xy = np.asarray(nodes[self.controls["hydrology"]["outlet"]]["xy"])*[
            self.controls["world"]["width_m"], self.controls["world"]["height_m"]]
        outlet = int(round(xy[1]/8))*len(self.parent_x)+int(round(xy[0]/8))
        receiver, accumulation = independent_d8(self.result.composite_height, 8, outlet)
        review_routing(self.result.composite_height, receiver, accumulation, 8, [outlet])
        np.testing.assert_array_equal(self.result.regional_delta, self.result.composite_height-self.parent_height)
        xx, yy = np.meshgrid(self.parent_x, self.parent_y)
        owned = np.zeros(self.parent_height.shape, dtype=bool)
        for specification in self.local["patches"]:
            xmin, ymin, xmax, ymax = specification["bounds_m"]
            owned |= (xx >= xmin) & (xx <= xmax) & (yy >= ymin) & (yy <= ymax)
        np.testing.assert_array_equal(self.result.regional_delta[~owned], 0,
                                      err_msg="Refinement changed unowned regional terrain")
        for path, expected in self.input_hashes.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected,
                             "Refinement overwrote an authoritative input")

    def test_actual_edits_are_bounded_and_water_crossings_are_not_ground_roads(self):
        for patch in self.result.patches:
            with self.subTest(patch=patch.id):
                delta = patch.height-patch.base_height
                self.assertLessEqual(float(np.max(np.abs(delta))), self.local["roads"]["max_cut_fill_m"]+1e-7)
                self.assertLessEqual(float(np.max(np.abs(patch.stage_deltas["bank"]))), self.local["banks"]["max_cut_fill_m"]+1e-9)
                self.assertLessEqual(float(np.max(np.abs(patch.stage_deltas["road"]))), self.local["roads"]["max_cut_fill_m"]+1e-9)
                self.assertLessEqual(float(np.max(np.abs(patch.stage_deltas["pad"]))), self.local["foundations"]["max_cut_fill_m"]+1e-9)
                self.assertTrue(np.all(np.abs(patch.stage_deltas["road"][patch.river_mask]) < 1e-9),
                                "A road grading edit fills existing wet ground instead of declaring a structure gap")
                self.assertTrue(np.all(np.abs(patch.stage_deltas["pad"][patch.river_mask]) < 1e-9),
                                "A foundation pad covers existing wet ground")
                if self.specifications[patch.id].get("foundation_grading") is False:
                    self.assertFalse(patch.pad_mask.any(), "Fen policy silently graded dry foundations")
                    np.testing.assert_array_equal(patch.stage_deltas["pad"], 0)

    def test_stage_deltas_account_for_the_actual_final_surface(self):
        for patch in self.result.patches:
            reconstructed = sum(patch.stage_deltas.values(), np.zeros_like(patch.height))
            np.testing.assert_allclose(reconstructed, patch.height-patch.base_height, rtol=0, atol=1e-10,
                                       err_msg="Stage proposals omit a clipping or projection correction")

    def test_final_full_footprints_and_flood_status_are_rescreened(self):
        sites = {s["id"]: s for s in self.controls["settlements"]}
        scenario = float(self.controls["world"]["flood_scenario_rise_m"])
        safe = {"graded_foundation_test", "bounded_foundation_candidate"}
        for patch in self.result.patches:
            for plot in patch.plots:
                with self.subTest(patch=patch.id, xy=plot["xy_m"]):
                    px, py = plot["xy_m"]
                    columns = np.flatnonzero(np.abs(patch.x-px) <= plot["width_m"]/2+1e-8)
                    rows = np.flatnonzero(np.abs(patch.y-py) <= plot["length_m"]/2+1e-8)
                    self.assertTrue(len(rows) and len(columns))
                    values = patch.height[np.ix_(rows, columns)]
                    xx, yy = np.meshgrid(patch.x[columns], patch.y[rows])
                    stages = source_stage_at(self.controls, xx, yy)
                    self.assertTrue(plot["postprojection_screen"])
                    self.assertEqual(plot["footprint_samples"], values.size)
                    self.assertAlmostEqual(plot["actual_max_local_relief_m"], float(np.ptp(values)), places=8)
                    self.assertAlmostEqual(plot["normal_stage_m"], float(stages.max()), places=8)
                    self.assertAlmostEqual(plot["normal_ground_freeboard_m"], float((values-stages).min()), places=8)
                    self.assertAlmostEqual(plot["scenario_floor_freeboard_m"], plot["floor_z_m"]-float(stages.max())-scenario, places=8)
                    matrix = np.column_stack([(xx-px).reshape(-1), (yy-py).reshape(-1), np.ones(values.size)])
                    plane = np.linalg.lstsq(matrix, values.reshape(-1), rcond=None)[0]
                    grade = float(np.hypot(plane[0], plane[1]))
                    self.assertAlmostEqual(plot["actual_plane_grade"], grade, places=8)
                    if plot["status"] in safe or plot["status"] == "conditional_stilts":
                        site = sites[plot["settlement"]]
                        stilts = plot["status"] == "conditional_stilts"
                        review_footprint_clearance(values, stages, plot["floor_z_m"], site["min_freeboard_m"],
                                                   scenario, site["min_freeboard_m"] if stilts else 0.3, stilts)
                        if not stilts:
                            self.assertFalse(patch.river_mask[np.ix_(rows, columns)].any())
                            self.assertLessEqual(plot["required_cut_fill_m"], self.local["foundations"]["max_cut_fill_m"]+1e-8)
                        else:
                            self.assertFalse(plot["foundation_applied"], "Conditional fen plots received dry-earth foundations")

    def test_postprojection_road_grade_uses_the_actual_triangle_surface(self):
        routes = {r["id"]: r for r in self.controls["routes"]}
        world_scale = [self.controls["world"]["width_m"], self.controls["world"]["height_m"]]
        limit = float(self.local["roads"]["max_grade"])
        for patch in self.result.patches:
            reports = {r["id"]: r for r in patch.metrics["roads"]}
            self.assertEqual(set(reports), set(self.specifications[patch.id]["route_ids"]))
            for name, report in reports.items():
                with self.subTest(patch=patch.id, route=name):
                    points = np.asarray(routes[name]["points"])*world_scale
                    samples, station = sampled_polyline(points)
                    x, y = samples[:, 0], samples[:, 1]
                    inside = (x > patch.x[0]+2) & (x < patch.x[-1]-2) & (y > patch.y[0]+2) & (y < patch.y[-1]-2)
                    valid = inside.copy()
                    for reach in self.controls["hydrology"]["reaches"]:
                        course = np.asarray(reach["points"])*world_scale
                        distance = distance_to_polyline(course, x, y)
                        valid &= distance > reach.get("half_width_m", 4)+self.local["roads"]["water_crossing_exclusion_m"]
                    z = np.zeros(len(samples))
                    z[inside] = regional_triangle_height(patch.height, patch.x, patch.y, x[inside], y[inside])
                    grade = np.abs(np.diff(z))/np.diff(station)
                    edges = valid[:-1] & valid[1:]
                    maximum = float(grade[edges].max()) if edges.any() else None
                    if maximum is None:
                        self.assertIsNone(report["actual_postprojection_grade_max"])
                    else:
                        self.assertAlmostEqual(report["actual_postprojection_grade_max"], maximum, places=8)
                        self.assertAlmostEqual(report["actual_fraction_over_budget"], float((grade[edges] > limit+1e-8).mean()), places=8)
                        expected = "unresolved_grade_exceeds_budget" if maximum > limit+1e-8 else "within_grade_budget_away_from_water_gaps"
                        self.assertEqual(report["actual_grade_status"], expected)

    def test_existing_watercourse_centrelines_are_wet_on_the_actual_final_mesh(self):
        reaches = {r["id"]: r for r in self.controls["hydrology"]["reaches"]}
        nodes = {n["id"]: n for n in self.controls["hydrology"]["nodes"]}
        scale = [self.controls["world"]["width_m"], self.controls["world"]["height_m"]]
        for patch in self.result.patches:
            for name in self.specifications[patch.id]["bank_reach_ids"]:
                with self.subTest(patch=patch.id, reach=name):
                    reach = reaches[name]
                    points = np.asarray(reach["points"])*scale
                    samples, station = sampled_polyline(points)
                    inside = ((samples[:, 0] >= patch.x[0]) & (samples[:, 0] <= patch.x[-1]) &
                              (samples[:, 1] >= patch.y[0]) & (samples[:, 1] <= patch.y[-1]))
                    if not inside.any():
                        continue
                    query = samples[inside]
                    ground = regional_triangle_height(patch.height, patch.x, patch.y, query[:, 0], query[:, 1])
                    length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
                    profile = reach.get("profile")
                    if profile:
                        positions = np.asarray([p.get("fraction", p.get("t")) for p in profile])*length
                        bed = np.asarray([p.get("z_m", p.get("bed_m")) for p in profile])
                    else:
                        positions = np.array([0., length])
                        bed = np.array([nodes[reach["from"]]["bed_m"], nodes[reach["to"]]["bed_m"]])
                    water = np.interp(station[inside], positions, bed)+reach.get("water_depth_m", 1.2)
                    dry = ground > water+1e-5
                    self.assertFalse(dry.any(),
                                     f"Saved {name} mesh has {int(dry.sum())} dry centreline samples; "
                                     f"maximum ground-stage={float((ground-water).max()):.6f} m; "
                                     f"first={query[dry][0].tolist() if dry.any() else None}. A rendered water overlay cannot fix this.")

    def test_inspection_preserves_fixed_anchors_and_has_no_vertical_exaggeration(self):
        inspection = self.local["inspection"]
        self.assertEqual(inspection["vertical_scale"], 1)
        collections = {"settlement": self.controls["settlements"], "hydrology_node": self.controls["hydrology"]["nodes"],
                       "landmark": self.controls["landmark_anchors"]}
        scale = [self.controls["world"]["width_m"], self.controls["world"]["height_m"]]
        for anchor in inspection["anchors"]:
            if anchor["source_type"] == "retained_route_natural_reach_intersection":
                route=next(r for r in self.controls["routes"] if r["id"]==anchor["source_route_id"])
                reach=next(r for r in self.controls["hydrology"]["reaches"] if r["id"]==anchor["source_reach_id"])
                road=np.asarray(route["points"])*scale
                river=np.asarray(reach["points"])*scale
                found=[]
                cross=lambda u,v:u[0]*v[1]-u[1]*v[0]
                for a,b in zip(road[:-1],road[1:]):
                    for c,d in zip(river[:-1],river[1:]):
                        v,u=b-a,d-c
                        denominator=cross(v,u)
                        if abs(denominator)<1e-10: continue
                        t,s=cross(c-a,u)/denominator,cross(c-a,v)/denominator
                        if 0<=t<=1 and 0<=s<=1: found.append(a+t*v)
                self.assertTrue(any(np.linalg.norm(point-anchor["xy_m"])<1e-5 for point in found),
                                "Inspection crossing is not an intersection of the retained road and river")
                continue
            source = next(r for r in collections[anchor["source_type"]] if r["id"] == anchor["source_id"])
            np.testing.assert_allclose(anchor["xy_m"], np.asarray(source["xy"])*scale, rtol=0, atol=1e-5,
                                       err_msg="A narrative anchor was moved to make the inspection work")
        for proxy in inspection["proxies"]:
            if proxy["id"] == "granary_yard_concept":
                self.assertFalse(proxy["include_in_capacity"])
                self.assertFalse(proxy["terrain_grading"])

    def test_final_subcell_geometry_is_more_than_a_denser_parent_array(self):
        for patch in self.result.patches:
            with self.subTest(patch=patch.id):
                delta = patch.height-patch.base_height
                self.assertGreater(float(np.max(np.abs(delta))), 0.02,
                                   "Only resampling or microscopic drainage nudges remain")
                step = int(round(8/(patch.x[1]-patch.x[0])))
                xx, yy = np.meshgrid(patch.x, patch.y)
                coarse_only = regional_triangle_height(delta[::step, ::step], patch.x[::step], patch.y[::step], xx, yy)
                residual = delta-coarse_only
                self.assertGreater(float(np.max(np.abs(residual))), 0.005,
                                   "The claimed two-metre refinement contains no resolved sub-eight-metre feature")

    def test_saved_local_arrays_preserve_every_sample_and_world_coordinate(self):
        scratch = SCRIPT_DIRECTORY / ".scratch"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as output:
            self.module.export_local(self.result, output)
            for patch in self.result.patches:
                with np.load(Path(output)/(patch.id+".npz"), allow_pickle=False) as saved:
                    for name in ["x", "y", "height", "base_height", "receiver", "accumulation", "halo_x", "halo_y", "halo_height", "halo_receiver"]:
                        np.testing.assert_array_equal(saved[name], getattr(patch, name))
                    for name, delta in patch.stage_deltas.items():
                        np.testing.assert_array_equal(saved[name+"_delta"], delta)
                np.testing.assert_array_equal(np.load(Path(output)/(patch.id+"_height.npy"), allow_pickle=False), patch.height)
            np.testing.assert_array_equal(np.load(Path(output)/"composite_regional_height.npy", allow_pickle=False), self.result.composite_height)

    def test_identical_inputs_reproduce_actual_local_geometry(self):
        repeated = self.module.refine_all(self.regional_path, self.controls, self.local)
        np.testing.assert_array_equal(repeated.composite_height, self.result.composite_height)
        for first, second in zip(self.result.patches, repeated.patches):
            self.assertEqual(first.id, second.id)
            for name in ["height", "receiver", "accumulation", "halo_height", "halo_receiver"]:
                np.testing.assert_array_equal(getattr(first, name), getattr(second, name))
            for name in first.stage_deltas:
                np.testing.assert_array_equal(first.stage_deltas[name], second.stage_deltas[name])


if __name__ == "__main__":
    unittest.main()
