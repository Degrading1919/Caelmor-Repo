"""Bounded deterministic local refinement of the persisted regional terrain.

This is a prolongation/local-edit layer of terrain.py, not a second world
generator. Global coordinates, regional boundary samples, water stages and the
original drainage graph remain explicit constraints.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np

import terrain


@dataclass
class LocalPatch:
    id: str
    x: np.ndarray
    y: np.ndarray
    base_height: np.ndarray
    height: np.ndarray
    water_level: np.ndarray
    river_mask: np.ndarray
    road_mask: np.ndarray
    pad_mask: np.ndarray
    receiver: np.ndarray
    accumulation: np.ndarray
    metrics: dict
    plots: list
    stage_deltas: dict
    halo_x: np.ndarray
    halo_y: np.ndarray
    halo_height: np.ndarray
    halo_receiver: np.ndarray
    owned_slice: tuple


@dataclass
class LocalResult:
    patches: list
    composite_height: np.ndarray
    regional_delta: np.ndarray
    metrics: dict


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def adaptive_diagonals(height, receiver):
    """Select triangulation that contains every original diagonal drainage edge."""
    ny, nx = height.shape
    index = np.arange(height.size).reshape(height.shape)
    a, b, c, d = index[:-1, :-1], index[:-1, 1:], index[1:, :-1], index[1:, 1:]
    rec = receiver.ravel()
    sw_ne = (rec[a] == d) | (rec[d] == a)
    nw_se = (rec[b] == c) | (rec[c] == b)
    if np.any(sw_ne & nw_se):
        raise ValueError("Crossing diagonal parent drainage constraints cannot share one heightfield cell.")
    return nw_se


def sample_triangles(height, diagonals, x, y, cell=8.0, meshgrid=True):
    """Exact parent vertices; piecewise planar drainage-aware subcell sampling."""
    xx, yy = np.meshgrid(x, y) if meshgrid else (np.asarray(x), np.asarray(y))
    fx, fy = xx / cell, yy / cell
    col = np.clip(np.floor(fx).astype(int), 0, height.shape[1] - 2)
    row = np.clip(np.floor(fy).astype(int), 0, height.shape[0] - 2)
    u, v = fx - col, fy - row
    a, b, c, d = height[row, col], height[row, col + 1], height[row + 1, col], height[row + 1, col + 1]
    first = np.where(v <= u, a + (b - a) * u + (d - b) * v,
                     a + (d - c) * u + (c - a) * v)
    second = np.where(u + v <= 1, a + (b - a) * u + (c - a) * v,
                      d + (d - c) * (u - 1) + (d - b) * (v - 1))
    return np.where(diagonals[row, col], second, first)


def project_drainage(source, desired, receiver, lower, upper):
    """Bounded projection onto strict inequalities of a previously valid DAG.

    Original field is a feasible witness; immutable cells have lower==upper.
    Actual final receivers are independently recomputed after this projection.
    No arbitrary flood-fill or invented receiver can conceal a pit.
    """
    shape = source.shape
    z, target, rec = source.ravel(), desired.ravel(), receiver.ravel()
    lo, hi = lower.ravel().copy(), upper.ravel().copy()
    if np.any(lo > z + 1e-7) or np.any(hi < z - 1e-7):
        raise ValueError("Drainage source must be a feasible witness within every grading interval.")
    order = np.argsort(z, kind="stable")
    epsilon = np.zeros(z.size)
    active = rec >= 0
    epsilon[active] = np.minimum((z[active] - z[rec[active]]) * 0.5, 0.00001)
    if np.any(epsilon[active] <= 0):
        raise ValueError("Source drainage graph contains a flat/uphill edge.")
    for cell in order:
        dest = rec[cell]
        if dest >= 0:
            lo[cell] = max(lo[cell], lo[dest] + epsilon[cell])
    for cell in order[::-1]:
        dest = rec[cell]
        if dest >= 0:
            hi[dest] = min(hi[dest], hi[cell] - epsilon[cell])
    if np.any(lo > hi + 1e-7):
        raise ValueError("Local grading intervals conflict with immutable downstream drainage.")
    result = np.clip(target, lo, hi)
    for cell in order:
        dest = rec[cell]
        if dest >= 0:
            result[cell] = max(result[cell], result[dest] + epsilon[cell])
    if np.any(result > hi + 1e-7):
        raise AssertionError("Bounded drainage projection exceeded its admissible interval.")
    locked = lower.ravel() == upper.ravel()
    result[locked] = lower.ravel()[locked]
    return result.reshape(shape)


def stage_geometry(controls, xx, yy, height):
    """Actual natural/engineered wet corridors at existing source water levels."""
    world = controls["world"]
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    stage = np.full(height.shape, np.nan)
    nearest = np.full(height.shape, np.inf)
    reference = np.zeros(height.shape)
    exclusion = np.zeros(height.shape, dtype=bool)
    for reach in controls["hydrology"]["reaches"]:
        points = np.asarray(reach["points"]) * [world["width_m"], world["height_m"]]
        distance, along = terrain.project_polyline(points, xx, yy)
        length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
        ps, pz = terrain.reach_profile(reach, nodes, length)
        water = np.interp(along, ps, pz) + float(reach.get("water_depth_m", 1.2))
        width = float(reach.get("half_width_m", 4))
        near = distance < nearest
        nearest[near], reference[near] = distance[near], water[near]
        wet = (distance <= width + 1) & (height <= water + 1e-7)
        stage[wet] = np.fmax(stage[wet], water[wet])
        exclusion |= distance <= width + 8
    for wetland in controls.get("wetlands", []):
        points = np.asarray(wetland["polygon"]) * [world["width_m"], world["height_m"]]
        inside = terrain.polygon_mask(points, xx, yy)
        levels = wetland.get("water_level_range_m", [63.65, 64.2])
        water = np.clip(reference, min(levels), max(levels))
        wet = inside & (height <= water + 1e-7)
        stage[wet] = np.fmax(stage[wet], water[wet])
    exclusion |= np.isfinite(stage)
    return stage, reference, exclusion


def grade_profile(elevations, stations, maximum_grade, smoothing_m):
    spacing = float(np.median(np.diff(stations)))
    count = max(1, round(smoothing_m / spacing))
    if count % 2 == 0: count += 1
    smoothed = np.convolve(np.pad(elevations, count // 2, mode="edge"), np.ones(count) / count, mode="valid")
    lower, upper = smoothed.copy(), smoothed.copy()
    for index in range(1, len(lower)):
        distance = maximum_grade * (stations[index] - stations[index - 1])
        lower[index] = max(lower[index], lower[index - 1] - distance)
        upper[index] = min(upper[index], upper[index - 1] + distance)
    for index in range(len(lower) - 2, -1, -1):
        distance = maximum_grade * (stations[index + 1] - stations[index])
        lower[index] = max(lower[index], lower[index + 1] - distance)
        upper[index] = min(upper[index], upper[index + 1] + distance)
    return (lower + upper) / 2


def road_proposals(parent, diagonals, controls, local, patch, xx, yy, base, feather, exclusion):
    numerator, denominator = np.zeros(base.shape), np.zeros(base.shape)
    reports = []
    settings = local["roads"]
    routes = {route["id"]: route for route in controls.get("routes", [])}
    world = controls["world"]
    for route_id in patch.get("route_ids", []):
        route = routes[route_id]
        points = np.asarray(route["points"]) * [world["width_m"], world["height_m"]]
        samples, stations, _ = terrain.polyline_samples(points, 2)
        original = sample_triangles(parent, diagonals, samples[:, 0], samples[:, 1], meshgrid=False)
        valid = np.ones(len(samples), dtype=bool)
        xmin, ymin, xmax, ymax = patch["bounds_m"]
        valid &= (samples[:, 0] >= xmin) & (samples[:, 0] <= xmax) & (samples[:, 1] >= ymin) & (samples[:, 1] <= ymax)
        crossings = []
        for reach in controls["hydrology"]["reaches"]:
            water_points = np.asarray(reach["points"]) * [world["width_m"], world["height_m"]]
            distance, _ = terrain.project_polyline(water_points, samples[:, 0], samples[:, 1])
            blocked = distance <= float(reach.get("half_width_m", 4)) + settings["water_crossing_exclusion_m"]
            if np.any(blocked): crossings.append(reach["id"])
            valid &= ~blocked
        proposed = original.copy()
        feasible_mask = np.zeros(len(samples))
        failed = []
        intervals = np.flatnonzero(np.diff(np.r_[False, valid, False])).reshape(-1, 2)
        for start, end in intervals:
            if end - start < 4: continue
            target = grade_profile(original[start:end], stations[start:end], settings["max_grade"], settings["profile_smoothing_m"])
            required = float(np.max(np.abs(target - original[start:end])))
            if required > settings["max_cut_fill_m"]:
                failed.append({"station_start_m": float(stations[start]), "station_end_m": float(stations[end - 1]),
                               "required_cut_fill_m": required, "status": "Grade budget infeasible; ground retained, access unresolved."})
                continue
            proposed[start:end], feasible_mask[start:end] = target, 1
        distance, along = terrain.project_polyline(points, xx, yy)
        width, blend = settings["half_width_m"], settings["blend_m"]
        weight = (1 - smoothstep((distance - width) / blend)) * feather
        weight *= np.interp(along, stations, feasible_mask) > 0.99
        weight[exclusion] = 0
        crown = 0.08 * np.maximum(1 - (distance / width) ** 2, 0)
        target = np.interp(along, stations, proposed) + crown
        delta = np.clip(target - base, -settings["max_cut_fill_m"], settings["max_cut_fill_m"])
        numerator += weight * delta; denominator += weight
        reports.append({"id": route_id, "crossed_watercourses": crossings, "water_contact_gap_reaches": crossings,
                        "crossing_list_interpretation": "Watercourses near the route triggering terrain exclusion; proximity is not proof of a geometric centerline crossing.",
                        "infeasible_segments": failed,
                        "maximum_road_stage_cut_fill_m": float(np.max(np.abs(weight * delta))),
                        "crown_height_m": 0.08, "crossing_policy": "Water-contact gaps retained; no bridge or submerged road generated."})
    return numerator / np.maximum(denominator, 1), denominator > 0.01, reports


def bank_proposals(controls, local, patch, xx, yy, base, feather):
    numerator, denominator = np.zeros(base.shape), np.zeros(base.shape)
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    for reach in controls["hydrology"]["reaches"]:
        if reach["id"] not in patch.get("bank_reach_ids", []): continue
        points = np.asarray(reach["points"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        distance, along = terrain.project_polyline(points, xx, yy)
        length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
        ps, pz = terrain.reach_profile(reach, nodes, length)
        width, depth = float(reach.get("half_width_m", 4)), float(reach.get("water_depth_m", 1.2))
        target = np.interp(along, ps, pz) + depth * np.minimum(distance / width, 1) ** 2 + np.maximum(distance - width, 0) * 0.02
        weight = (1 - smoothstep((distance - width) / local["banks"]["blend_m"])) * feather
        budget = local["banks"]["max_cut_fill_m"]
        numerator += weight * np.clip(target - base, -budget, budget); denominator += weight
    return numerator / np.maximum(denominator, 1), denominator > 0.01


def bed_proposals(controls, local, patch, xx, yy, base, bank_delta, feather):
    settings = local.get("beds", {})
    delta, mask = np.zeros(base.shape), np.zeros(base.shape, dtype=bool)
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    for reach in controls["hydrology"]["reaches"]:
        if reach["id"] not in settings.get("reach_ids", []) or reach["id"] not in patch.get("bank_reach_ids", []): continue
        points = np.asarray(reach["points"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        distance, along = terrain.project_polyline(points, xx, yy)
        length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
        ps, pz = terrain.reach_profile(reach, nodes, length)
        width, depth = float(reach.get("half_width_m", 4)), float(reach.get("water_depth_m", 1.2))
        target = np.interp(along, ps, pz) + depth * np.minimum(distance / width, 1) ** 2
        budget = float(settings["max_cut_fill_m"])
        bounded_target = np.clip(target, base - budget, base + budget)
        weight = (1 - smoothstep((distance - width * 0.75) / (width * 0.25))) * feather
        correction = np.minimum(bounded_target - base - bank_delta, 0) * weight
        delta = np.minimum(delta, np.maximum(correction, -budget)); mask |= weight > 0.001
    return delta, mask


def candidate_foundations(controls, local, patch, xx, yy, height, reference, exclusion, road_mask, feather):
    delta, pad_mask, plots = np.zeros(height.shape), np.zeros(height.shape, dtype=bool), []
    resolution = local["resolution_m"]
    settings = local["foundations"]
    settlements = {site["id"]: site for site in controls["settlements"]}
    for site_id in patch["settlement_ids"]:
        site = settlements[site_id]
        center = np.asarray(site["xy"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        axes = site["envelope_axes_m"]
        inside = ((xx - center[0]) / (axes[0] / 2)) ** 2 + ((yy - center[1]) / (axes[1] / 2)) ** 2 <= 1
        size = math.sqrt(site["footprint_m2"])
        radius = max(1, math.ceil(size / (2 * resolution)))
        spacing = max(2 * radius + 3, math.ceil(math.sqrt(site["footprint_m2"] / (site["plot_coverage"] * (1 - site["road_fraction"]))) / resolution))
        applied = 0
        for row in range(radius + 3, height.shape[0] - radius - 3, spacing):
            for col in range(radius + 3, height.shape[1] - radius - 3, spacing):
                rr, cc = slice(row - radius, row + radius + 1), slice(col - radius, col + radius + 1)
                if not inside[rr, cc].all() or exclusion[rr, cc].any() or road_mask[rr, cc].any() or feather[rr, cc].min() < 0.99: continue
                values = height[rr, cc]
                coords = np.column_stack([(xx[rr, cc] - xx[row, col]).ravel(), (yy[rr, cc] - yy[row, col]).ravel(), np.ones(values.size)])
                plane = np.linalg.lstsq(coords, values.ravel(), rcond=None)[0]
                gradient = float(np.hypot(plane[0], plane[1]))
                if gradient > settings["max_plane_grade"]: plane[:2] *= settings["max_plane_grade"] / gradient
                target = (coords @ plane).reshape(values.shape)
                required = float(np.max(np.abs(target - values)))
                stage = float(reference[rr, cc].max())
                minimum = float(values.min())
                stilts = patch.get("policy") == "stilts_only"
                scenario = float(controls["world"].get("flood_scenario_rise_m", 1.5))
                clearance = float(site["min_freeboard_m"])
                floor = max(float(target.max()) + 0.3, stage + scenario + clearance) if stilts else float(target.max()) + 0.3
                freeboard = minimum - stage
                status = "conditional_stilts" if stilts else "terrain_candidate" if freeboard >= site["min_freeboard_m"] and required <= settings["max_cut_fill_m"] else "requires_review"
                plot = {"settlement": site_id, "xy_m": [float(xx[row, col]), float(yy[row, col])],
                        "width_m": radius * 2 * resolution, "length_m": radius * 2 * resolution,
                        "design_roof_area_m2": float(site["footprint_m2"]),
                        "terrain_screen_area_m2": (radius * 2 * resolution) ** 2,
                        "footprint_interpretation": "Conservative raster-aligned terrain support screen encloses the assumed roof area; it is not a final building or parcel design.",
                        "floor_z_m": floor, "status": status, "normal_ground_freeboard_m": freeboard,
                        "scenario_floor_freeboard_m": floor - stage - scenario, "normal_stage_m": stage,
                        "declared_floor_clearance_m": clearance, "scenario_rise_m": scenario,
                        "required_cut_fill_m": required, "plane_grade": float(np.hypot(plane[0], plane[1])),
                        "actual_max_local_relief_m": float(np.ptp(values)), "foundation_applied": False}
                if (not stilts and patch.get("foundation_grading", True) and status == "terrain_candidate"
                        and applied < settings["max_pad_count"]):
                    br = math.ceil(settings["blend_m"] / resolution)
                    br0, br1, bc0, bc1 = row - radius - br, row + radius + br + 1, col - radius - br, col + radius + br + 1
                    if br0 < 0 or bc0 < 0 or br1 > height.shape[0] or bc1 > height.shape[1]: continue
                    support = np.s_[br0:br1, bc0:bc1]
                    dx, dy = xx[support] - xx[row, col], yy[support] - yy[row, col]
                    distance = np.maximum(np.abs(dx) - radius * resolution, np.abs(dy) - radius * resolution)
                    weight = 1 - smoothstep(distance / settings["blend_m"])
                    proposed = plane[0] * dx + plane[1] * dy + plane[2] - height[support]
                    edit = np.clip(proposed, -settings["max_cut_fill_m"], settings["max_cut_fill_m"]) * weight * feather[support]
                    if not exclusion[support].any() and not road_mask[support].any() and not pad_mask[support].any():
                        delta[support] = edit; pad_mask[support] |= weight > 0.001
                        plot["foundation_applied"] = True; applied += 1
                plots.append(plot)
    return delta, pad_mask, plots


def rescreen_plots(plots, controls, local, xx, yy, final, reference, water):
    sites = {site["id"]: site for site in controls["settlements"]}
    scenario = float(controls["world"].get("flood_scenario_rise_m", 1.5))
    summaries = {}
    for plot in plots:
        site = sites[plot["settlement"]]
        px, py = plot["xy_m"]
        selected = (np.abs(xx - px) <= plot["width_m"] / 2 + 1e-8) & (np.abs(yy - py) <= plot["length_m"] / 2 + 1e-8)
        values = final[selected]
        coords = np.column_stack([xx[selected] - px, yy[selected] - py, np.ones(len(values))])
        actual_plane = np.linalg.lstsq(coords, values, rcond=None)[0]
        proposed = actual_plane.copy()
        gradient = float(np.hypot(proposed[0], proposed[1]))
        if gradient > local["foundations"]["max_plane_grade"]:
            proposed[:2] *= local["foundations"]["max_plane_grade"] / gradient
        required = float(np.max(np.abs(coords @ proposed - values)))
        normal_stage = float(reference[selected].max())
        ground_freeboard = float(np.min(values - reference[selected]))
        stilts = plot["status"] == "conditional_stilts"
        clearance = float(site["min_freeboard_m"])
        floor = max(float(values.max()) + 0.3, normal_stage + scenario + clearance) if stilts else float(values.max()) + 0.3
        residual = float(np.max(np.abs(coords @ actual_plane - values)))
        if stilts: normal_status = "conditional_stilts"
        elif np.isfinite(water[selected]).any() or ground_freeboard < clearance: normal_status = "flood_exposure_review"
        elif required > local["foundations"]["max_cut_fill_m"]: normal_status = "earthwork_budget_review"
        elif plot["foundation_applied"] and residual <= 0.15 and gradient <= local["foundations"]["max_plane_grade"] + 1e-8: normal_status = "graded_foundation_test"
        else: normal_status = "bounded_foundation_candidate"
        floor_clearance = float(local["foundations"].get("scenario_floor_clearance_m", 0.3))
        floor_screen = floor - normal_stage - scenario >= floor_clearance - 1e-8
        status = "flood_adaptation_required" if normal_status in ("graded_foundation_test", "bounded_foundation_candidate") and not floor_screen else normal_status
        plot.update(status=status, floor_z_m=floor, normal_stage_m=normal_stage,
                    normal_stage_status=normal_status, scenario_floor_status="outside_static_stage_screen" if floor_screen else "flood_adaptation_required",
                    required_scenario_floor_clearance_m=floor_clearance,
                    normal_ground_freeboard_m=ground_freeboard, scenario_ground_freeboard_m=ground_freeboard - scenario,
                    scenario_floor_freeboard_m=floor - normal_stage - scenario, required_cut_fill_m=required,
                    actual_plane_grade=gradient, actual_plane_residual_max_m=residual,
                    actual_max_local_relief_m=float(np.ptp(values)), postprojection_screen=True,
                    footprint_samples=int(len(values)), maximum_support_height_m=floor - float(values.min()),
                    minimum_floor_ground_clearance_m=floor - float(values.max()))
        summary = summaries.setdefault(site["id"], {"site": site["id"], "normal_candidates": 0, "scenario_ground_candidates": 0,
                                                    "scenario_floor_candidates": 0, "flood_adaptation_required": 0,
                                                    "conditional_stilts": 0, "graded_foundation_tests": 0, "requires_review": 0})
        if normal_status in ("graded_foundation_test", "bounded_foundation_candidate"):
            summary["normal_candidates"] += 1
            summary["scenario_ground_candidates"] += bool(ground_freeboard >= scenario)
            summary["scenario_floor_candidates"] += bool(floor_screen)
            summary["flood_adaptation_required"] += not floor_screen
        elif stilts: summary["conditional_stilts"] += 1
        else: summary["requires_review"] += 1
        summary["graded_foundation_tests"] += normal_status == "graded_foundation_test"
    return summaries


def sample_local(field, hx, hy, points):
    fx = np.clip((points[:, 0] - hx[0]) / (hx[1] - hx[0]), 0, len(hx) - 1)
    fy = np.clip((points[:, 1] - hy[0]) / (hy[1] - hy[0]), 0, len(hy) - 1)
    c0, r0 = np.floor(fx).astype(int), np.floor(fy).astype(int)
    c1, r1 = np.minimum(c0 + 1, len(hx) - 1), np.minimum(r0 + 1, len(hy) - 1)
    u, v = fx - c0, fy - r0
    a, b, c, d = field[r0, c0], field[r0, c1], field[r1, c0], field[r1, c1]
    return np.where(v <= u, a + (b - a) * u + (d - b) * v,
                    a + (d - c) * u + (c - a) * v)


def rescreen_roads(reports, controls, local, specification, hx, hy, final):
    routes = {route["id"]: route for route in controls.get("routes", [])}
    xmin, ymin, xmax, ymax = specification["bounds_m"]
    for report in reports:
        points = np.asarray(routes[report["id"]]["points"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        samples, station, _ = terrain.polyline_samples(points, 2)
        inside = (samples[:, 0] > xmin + 2) & (samples[:, 0] < xmax - 2) & (samples[:, 1] > ymin + 2) & (samples[:, 1] < ymax - 2)
        away = inside.copy()
        for reach in controls["hydrology"]["reaches"]:
            course = np.asarray(reach["points"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
            distance, _ = terrain.project_polyline(course, samples[:, 0], samples[:, 1])
            away &= distance > reach.get("half_width_m", 4) + local["roads"]["water_crossing_exclusion_m"]
        z = sample_local(final, hx, hy, samples)
        grade = np.abs(np.diff(z)) / np.diff(station)
        valid = away[:-1] & away[1:]
        maximum = float(grade[valid].max()) if valid.any() else None
        report.update(actual_postprojection_grade_max=maximum,
                      actual_postprojection_grade_p95=float(np.percentile(grade[valid], 95)) if valid.any() else None,
                      actual_fraction_over_budget=float((grade[valid] > local["roads"]["max_grade"] + 1e-8).mean()) if valid.any() else None,
                      actual_grade_status="unresolved_grade_exceeds_budget" if maximum is not None and maximum > local["roads"]["max_grade"] + 1e-8 else "within_grade_budget_away_from_water_gaps",
                      grade_scope="Actual final two-metre surface; excludes declared water-contact gaps, not a continuous crossing/bridge certification.")


def watercourse_depth_reports(controls, specification, hx, hy, final):
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    xmin, ymin, xmax, ymax = specification["bounds_m"]
    reports = []
    for reach in controls["hydrology"]["reaches"]:
        if reach["id"] not in specification.get("bank_reach_ids", []): continue
        points = np.asarray(reach["points"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        samples, station, breaks = terrain.polyline_samples(points, 1)
        inside = (samples[:, 0] > xmin + 2) & (samples[:, 0] < xmax - 2) & (samples[:, 1] > ymin + 2) & (samples[:, 1] < ymax - 2)
        if not inside.any(): continue
        ps, pz = terrain.reach_profile(reach, nodes, breaks[-1])
        stage = np.interp(station[inside], ps, pz) + float(reach.get("water_depth_m", 1.2))
        ground = sample_local(final, hx, hy, samples[inside])
        depth = stage - ground
        reports.append({"id": reach["id"], "sample_spacing_m": 1, "sample_count": int(inside.sum()),
                        "minimum_static_centerline_depth_m": float(depth.min()), "mean_static_centerline_depth_m": float(depth.mean()),
                        "dry_centerline_samples": int((depth < -1e-7).sum()),
                        "normal_stage_range_m": [float(stage.min()), float(stage.max())],
                        "surface": "Actual published two-metre SWNE triangles, not bilinear or interpolated metadata.",
                        "interpretation": "Static wet-course continuity screen; no discharge, navigable draft or gate operation certification."})
    return reports


def exit_certificates(receiver, halo_receiver, owned_slice, hx, hy, composite, diagonals, regional_receiver, outlet):
    r0, r1, c0, c1 = owned_slice
    labels = np.full(composite.size, -1, dtype=np.int32)
    labels[outlet] = outlet
    rec = regional_receiver.ravel()
    for cell in np.argsort(composite.ravel(), kind="stable"):
        if rec[cell] >= 0: labels[cell] = labels[rec[cell]]
    certificates = []
    for cell in np.flatnonzero(receiver.ravel() == -1):
        row, col = divmod(int(cell), receiver.shape[1])
        target = int(halo_receiver[row + r0, col + c0])
        tr, tc = divmod(target, halo_receiver.shape[1])
        x, y = float(hx[tc]), float(hy[tr])
        cr = min(int(y // 8), composite.shape[0] - 2); cc = min(int(x // 8), composite.shape[1] - 2)
        u, v = x / 8 - cc, y / 8 - cr
        a, b, c, d = cr * composite.shape[1] + cc, cr * composite.shape[1] + cc + 1, (cr + 1) * composite.shape[1] + cc, (cr + 1) * composite.shape[1] + cc + 1
        vertices = (a, b, c) if diagonals[cr, cc] and u + v <= 1 else (b, c, d) if diagonals[cr, cc] else (a, b, d) if v <= u else (a, c, d)
        anchor = min(vertices, key=lambda index: (composite.ravel()[index], index))
        certificates.append({"local_cell": int(cell), "actual_downstream_xy_m": [x, y],
                             "containing_triangle_lower_vertex": int(anchor), "regional_terminal": int(labels[anchor]),
                             "reaches_approved_outlet": bool(labels[anchor] == outlet),
                             "certificate": "Actual downhill halo exit; containing parent triangle has a lower/equal vertex on the independently validated composite regional D8 graph. Not a forced fine-grid receiver."})
    return certificates


def core_receivers(halo_height, owned_slice, spacing):
    halo_receiver = terrain.d8_receivers(halo_height, spacing)
    r0, r1, c0, c1 = owned_slice
    ny, nx = r1 - r0, c1 - c0
    targets = halo_receiver[r0:r1, c0:c1]
    rr, cc = targets // halo_height.shape[1], targets % halo_height.shape[1]
    inside = (targets >= 0) & (rr >= r0) & (rr < r1) & (cc >= c0) & (cc < c1)
    receiver = np.full((ny, nx), -1, dtype=np.int32)
    receiver[inside] = (rr[inside] - r0) * nx + cc[inside] - c0
    receiver[targets == -2] = -2
    return receiver, halo_receiver


def refine_all(regional_npz, regional_controls, local_controls):
    started = time.perf_counter()
    source_file_hash = hashlib.sha256(Path(regional_npz).read_bytes()).hexdigest()
    with np.load(regional_npz, allow_pickle=False) as saved:
        parent = saved["height_engineered"].copy()
    controls, local = regional_controls, local_controls
    spacing = float(local["resolution_m"])
    if spacing not in (1, 2): raise ValueError("Local refinement supports one or two metre spacing.")
    node = next(node for node in controls["hydrology"]["nodes"] if node["id"] == controls["hydrology"]["outlet"])
    outlet_xy = np.asarray(node["xy"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
    oc, orow = np.rint(outlet_xy / 8).astype(int)
    outlet = int(orow * parent.shape[1] + oc)
    parent_receiver = terrain.d8_receivers(parent, 8, outlet)
    if not np.isfinite(parent).all() or np.any(parent_receiver == -2): raise ValueError("Persisted regional input must already pass actual drainage validation at the declared outlet.")
    diagonals = adaptive_diagonals(parent, parent_receiver)
    specifications = local["patches"]
    for index, first in enumerate(specifications):
        bounds = first["bounds_m"]
        if any(value % 8 for value in bounds): raise ValueError("Patch boundaries must align to parent eight-metre vertices.")
        for second in specifications[index + 1:]:
            a, b = bounds, second["bounds_m"]
            if max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3]):
                raise ValueError("Overlapping independent patch ownership is forbidden; use one joint patch.")
    work = []
    proposed_parent, parent_budget = parent.copy(), np.zeros(parent.shape)
    for specification in specifications:
        xmin, ymin, xmax, ymax = map(float, specification["bounds_m"])
        hx = np.arange(max(0, xmin - 16), min(controls["world"]["width_m"], xmax + 16) + spacing, spacing)
        hy = np.arange(max(0, ymin - 16), min(controls["world"]["height_m"], ymax + 16) + spacing, spacing)
        xx, yy = np.meshgrid(hx, hy)
        base = sample_triangles(parent, diagonals, hx, hy)
        edge_distance = np.minimum.reduce([xx - xmin, xmax - xx, yy - ymin, ymax - yy])
        feather = smoothstep(edge_distance / local["boundary_feather_m"])
        boundary = edge_distance <= 0
        water, reference, exclusion = stage_geometry(controls, xx, yy, base)
        if specification.get("policy") == "stilts_only":
            clearance = min(site["min_freeboard_m"] for site in controls["settlements"] if site["id"] in specification["settlement_ids"])
            exclusion |= base < reference + clearance
        bank_delta, bank_mask = bank_proposals(controls, local, specification, xx, yy, base, feather)
        bed_delta, bed_mask = bed_proposals(controls, local, specification, xx, yy, base, bank_delta, feather)
        road_delta, road_mask, road_reports = road_proposals(parent, diagonals, controls, local, specification, xx, yy, base + bank_delta + bed_delta, feather, exclusion)
        pad_delta, pad_mask, plots = candidate_foundations(controls, local, specification, xx, yy, base + bank_delta + bed_delta + road_delta,
                                                         reference, exclusion, road_mask, feather)
        proposed = base + bank_delta + bed_delta + road_delta + pad_delta
        budget = np.maximum.reduce([bank_mask * local["banks"]["max_cut_fill_m"], bed_mask * local.get("beds", {}).get("max_cut_fill_m", 0),
                                    road_mask * local["roads"]["max_cut_fill_m"], pad_mask * local["foundations"]["max_cut_fill_m"]])
        desired = proposed.copy()
        desired = np.clip(desired, base - budget, base + budget)
        budget_clip = desired - proposed
        desired[boundary] = base[boundary]
        coarse = (np.remainder(xx, 8) == 0) & (np.remainder(yy, 8) == 0)
        rows, cols = (yy[coarse] / 8).astype(int), (xx[coarse] / 8).astype(int)
        proposed_parent[rows, cols] = desired[coarse]
        parent_budget[rows, cols] = budget[coarse]
        work.append(dict(specification=specification, hx=hx, hy=hy, xx=xx, yy=yy, base=base, desired=desired,
                         budget=budget, boundary=boundary, coarse=coarse, bank=bank_delta, bed=bed_delta, road=road_delta, pad=pad_delta,
                         budget_clip=budget_clip, road_mask=road_mask, pad_mask=pad_mask, road_reports=road_reports, plots=plots))
    for node in controls["hydrology"]["nodes"]:
        point = np.asarray(node["xy"]) * [controls["world"]["width_m"], controls["world"]["height_m"]]
        cc, rr = np.rint(point / 8).astype(int)
        parent_budget[rr, cc] = 0
    composite = project_drainage(parent, proposed_parent, parent_receiver, parent - parent_budget, parent + parent_budget)
    composite_receiver = terrain.d8_receivers(composite, 8, outlet)
    composite_accumulation = terrain.routing_accumulation(composite, composite_receiver)
    patches = []
    for item in work:
        specification, hx, hy = item["specification"], item["hx"], item["hy"]
        xx, yy, base = item["xx"], item["yy"], item["base"]
        new_base = sample_triangles(composite, diagonals, hx, hy)
        old_coarse_proposal = sample_triangles(proposed_parent, diagonals, hx, hy)
        residual = item["desired"] - old_coarse_proposal
        target = new_base + residual
        row = np.clip(np.floor(yy / 8).astype(int), 0, parent.shape[0] - 2)
        col = np.clip(np.floor(xx / 8).astype(int), 0, parent.shape[1] - 2)
        budget = np.maximum.reduce([parent_budget[row, col], parent_budget[row + 1, col], parent_budget[row, col + 1], parent_budget[row + 1, col + 1], item["budget"]])
        lower, upper = base - budget, base + budget
        locked = item["boundary"] | item["coarse"]
        lower[locked], upper[locked] = new_base[locked], new_base[locked]
        source_receiver = terrain.d8_receivers(new_base, spacing)
        source_sinks = (source_receiver == -2) & ~item["boundary"]
        if source_sinks.any(): raise ValueError("Parent-triangle prolongation created an interior sink before edits.")
        final = project_drainage(new_base, target, source_receiver, lower, upper)
        xmin, ymin, xmax, ymax = specification["bounds_m"]
        r0, r1 = int(round((ymin - hy[0]) / spacing)), int(round((ymax - hy[0]) / spacing)) + 1
        c0, c1 = int(round((xmin - hx[0]) / spacing)), int(round((xmax - hx[0]) / spacing)) + 1
        owned_slice = (r0, r1, c0, c1)
        own = np.s_[r0:r1, c0:c1]
        receiver, halo_receiver = core_receivers(final, owned_slice, spacing)
        accumulation = terrain.routing_accumulation(final[own], receiver)
        water, reference, _ = stage_geometry(controls, xx, yy, final)
        plot_summary = rescreen_plots(item["plots"], controls, local, xx, yy, final, reference, water)
        rescreen_roads(item["road_reports"], controls, local, specification, hx, hy, final)
        watercourses = watercourse_depth_reports(controls, specification, hx, hy, final)
        exits = np.flatnonzero(receiver.ravel() == -1)
        certificates = exit_certificates(receiver, halo_receiver, owned_slice, hx, hy, composite, diagonals, composite_receiver, outlet)
        coarse_projection = new_base - old_coarse_proposal
        fine_projection = final - target
        reference_sw_ne = sample_triangles(parent, np.zeros_like(diagonals), hx, hy)
        stage_deltas = {"bank": item["bank"][own], "road": item["road"][own], "pad": item["pad"][own],
                        "bed": item["bed"][own],
                        "budget_clip": item["budget_clip"][own],
                        "coarse_projection": coarse_projection[own], "fine_projection": fine_projection[own]}
        metric = {"id": specification["id"], "bounds_m": specification["bounds_m"], "resolution_m": spacing,
                  "shape": list(final[own].shape), "cells": int(final[own].size),
                  "boundary_max_error_m": float(np.abs(final - base)[item["boundary"]].max()),
                  "interior_sink_count": int((receiver == -2).sum()), "actual_outward_exit_count": len(exits),
                  "all_owned_samples_reach_outward_exits": int(accumulation.ravel()[exits].sum()) == final[own].size,
                  "maximum_total_cut_fill_m": float(np.abs(final[own] - base[own]).max()),
                  "maximum_bank_delta_m": float(np.abs(item["bank"]).max()),
                  "maximum_bed_delta_m": float(np.abs(item["bed"]).max()),
                  "maximum_road_delta_m": float(np.abs(item["road"]).max()),
                  "maximum_pad_delta_m": float(np.abs(item["pad"]).max()),
                  "maximum_fine_drainage_projection_m": float(np.abs(fine_projection).max()),
                  "height_sha256": hashlib.sha256(final[own].astype("<f8").tobytes()).hexdigest(),
                  "adaptive_base_vs_reference_parent_swne_max_m": float(np.abs(base[own] - reference_sw_ne[own]).max()),
                  "actual_subcell_edit_residual_max_m": float(np.abs(final[own] - new_base[own]).max()),
                  "parent_vertex_adaptation_error_m": float(np.abs(base[item["coarse"]] - parent[(yy[item["coarse"]] / 8).astype(int), (xx[item["coarse"]] / 8).astype(int)]).max()),
                  "roads": item["road_reports"], "approved_exits": certificates, "plot_summary": plot_summary,
                  "watercourse_depths": watercourses,
                  "all_exits_have_regional_continuation": all(item["reaches_approved_outlet"] for item in certificates),
                  "waterbed_refinement_policy": "Intermediate generated bed samples may change within bounded bank corridors; source water levels, hydraulic node anchor cells and world XY stay fixed.",
                  "halo_interpretation": "Drainage-aware parent raster prolongation, not an assertion that the old regional SWNE GLB already represented this subcell routing.",
                  "source_vertex_policy": "Boundary unchanged; bounded interior regional samples changed through explicit local corridors, composite independently validated."}
        patch = LocalPatch(specification["id"], hx[c0:c1], hy[r0:r1], base[own], final[own], water[own], np.isfinite(water[own]),
                           item["road_mask"][own], item["pad_mask"][own], receiver, accumulation, metric, item["plots"], stage_deltas,
                           hx, hy, final, halo_receiver, owned_slice)
        patches.append(patch)
    metrics = {"method": "Drainage-aware parent triangle prolongation; bounded local corridor edits; inequality projection on original parent and fine drainage DAGs; independent actual final D8.",
               "regional_source_sha256": source_file_hash,
               "regional_source_array_sha256": hashlib.sha256(parent.astype("<f8").tobytes()).hexdigest(),
               "composite_sha256": hashlib.sha256(composite.astype("<f8").tobytes()).hexdigest(),
               "composite_sink_count": int((composite_receiver == -2).sum()),
               "composite_outlet_accumulation_cells": int(composite_accumulation.ravel()[outlet]),
               "regional_outlet_cell": outlet, "regional_samples": int(parent.size),
               "maximum_regional_vertex_delta_m": float(np.abs(composite - parent).max()),
               "coordinates": "Global metres east X / north Y / elevation Z, unchanged from regional source; saved arrays rows north/columns east.",
               "surface_contract": "Adaptive parent-raster triangulation is a disclosed subcell refinement; published local two-metre mesh is explicit SWNE triangles. Bounds align to regional edges exactly.",
               "patches": [patch.metrics for patch in patches], "seconds": time.perf_counter() - started,
               "limitations": ["No discharge or flood-frequency simulation.", "Crossings are declared structure gaps; no bridge or architectural generator is invoked.",
                               "Foundation pads are sparse reversible technical tests, not approved production parcels or buildings."]}
    if hashlib.sha256(Path(regional_npz).read_bytes()).hexdigest() != source_file_hash:
        raise RuntimeError("Regional source changed during local refinement; discard this run and retry from one verified source.")
    if (metrics["composite_sink_count"] or metrics["composite_outlet_accumulation_cells"] != parent.size
            or any(patch.metrics["interior_sink_count"] or not patch.metrics["all_owned_samples_reach_outward_exits"]
                   or not patch.metrics["all_exits_have_regional_continuation"] or patch.metrics["boundary_max_error_m"] > 1e-9 for patch in patches)):
        raise RuntimeError("Local/composite drainage or seam verification failed; no local assets may be published.")
    return LocalResult(patches, composite, composite - parent, metrics)


def export_local(result, output):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    for patch in result.patches:
        boundary = np.zeros(patch.height.shape, dtype=bool)
        boundary[[0, -1], :] = True; boundary[:, [0, -1]] = True
        np.savez_compressed(output / (patch.id + ".npz"), x=patch.x, y=patch.y, height=patch.height,
                            base_height=patch.base_height, water_level=patch.water_level, river_mask=patch.river_mask,
                            road_mask=patch.road_mask, pad_mask=patch.pad_mask, receiver=patch.receiver, accumulation=patch.accumulation,
                            delta=patch.height - patch.base_height, boundary_mask=boundary,
                            halo_x=patch.halo_x, halo_y=patch.halo_y, halo_height=patch.halo_height, halo_receiver=patch.halo_receiver,
                            owned_slice=np.asarray(patch.owned_slice), **{name + "_delta": value for name, value in patch.stage_deltas.items()})
        np.save(output / (patch.id + "_height.npy"), patch.height.astype("<f8"), allow_pickle=False)
    np.save(output / "composite_regional_height.npy", result.composite_height, allow_pickle=False)
    np.save(output / "regional_delta.npy", result.regional_delta, allow_pickle=False)
    (output / "local_metrics.json").write_text(json.dumps(result.metrics, indent=2) + "\n", encoding="utf-8")
    (output / "candidate_plots.json").write_text(json.dumps({patch.id: patch.plots for patch in result.patches}, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regional", type=Path, required=True)
    parser.add_argument("--controls", type=Path, default=Path(__file__).with_name("lowmark_controls.json"))
    parser.add_argument("--local-controls", type=Path, default=Path(__file__).with_name("local_controls.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = refine_all(args.regional, json.loads(args.controls.read_text(encoding="utf-8-sig")), json.loads(args.local_controls.read_text(encoding="utf-8-sig")))
    export_local(result, args.output)
    print(json.dumps({"seconds": result.metrics["seconds"], "composite_sinks": result.metrics["composite_sink_count"],
                      "patches": [{key: patch.metrics[key] for key in ("id", "cells", "interior_sink_count", "maximum_total_cut_fill_m")} for patch in result.patches]}, indent=2))


if __name__ == "__main__":
    main()
