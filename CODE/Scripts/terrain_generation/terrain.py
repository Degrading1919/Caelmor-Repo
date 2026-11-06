"""Deterministic offline, drainage-constrained terrain; no engine or gameplay code.

Coordinates are metres east/north/up from the map's south-west origin. Authored
map points use normalized east/north coordinates. Elevations are provisional
engineering choices, not measurements recovered from the illustration.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
import hashlib
import heapq
import json
import math
from pathlib import Path
import struct
import time
import zlib

import numpy as np


OFFSETS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


@dataclass
class Result:
    x: np.ndarray
    y: np.ndarray
    height_raw: np.ndarray
    height: np.ndarray
    receiver: np.ndarray
    accumulation: np.ndarray
    channel_mask: np.ndarray
    channel_reach: np.ndarray
    water_level: np.ndarray
    channels: list
    metrics: dict
    settlement_masks: dict
    fen_mask: np.ndarray
    channel_distance: np.ndarray
    reference_stage: np.ndarray
    height_engineered: np.ndarray
    engineered_mask: np.ndarray
    plot_sites: dict
    floodplain_masks: dict


def world_of(controls):
    return controls.get("world", controls.get("map_frame", {}))


def xy_m(point, width, height):
    return np.asarray(point, dtype=np.float64) * np.array([width, height])


def grid(controls, resolution_m):
    world = world_of(controls)
    width, height = float(world["width_m"]), float(world["height_m"])
    nx, ny = round(width / resolution_m), round(height / resolution_m)
    if abs(nx * resolution_m - width) > 1e-7 or abs(ny * resolution_m - height) > 1e-7:
        raise ValueError("Extent must be an integer multiple of the chosen cell size.")
    return np.linspace(0, width, nx + 1), np.linspace(0, height, ny + 1)


def regional_field(controls, xx, yy):
    """Smooth Gaussian radial basis interpolation with an affine trend.

    Absolute controls use an augmented interpolation solve. Amplitude/radius
    controls use a direct radial-basis sum on the authored regional trend.
    No stochastic octave noise stands in for landform design.
    """
    world = world_of(controls)
    anchors = controls.get("landforms", controls.get("elevation_controls", []))
    if anchors and all("amplitude_m" in anchor for anchor in anchors):
        result = (float(world.get("base_elevation_m", 65)) + yy * float(world.get("north_slope", 0.001))
                  + xx * float(world.get("east_slope", 0.0005)))
        for anchor in anchors:
            point = xy_m(anchor["xy"], world["width_m"], world["height_m"])
            radius = float(anchor["radius_m"])
            result += float(anchor["amplitude_m"]) * np.exp(-((xx - point[0]) ** 2 + (yy - point[1]) ** 2) / (2 * radius ** 2))
        return result
    if len(anchors) < 3:
        return np.full_like(xx, float(world.get("base_elevation_m", 80))) + yy * 0.005
    points = np.array([xy_m(a["xy"], world["width_m"], world["height_m"]) for a in anchors])
    elevations = np.array([a["elevation_m"] for a in anchors], dtype=float)
    length = float(world.get("rbf_length_m", 1400))
    delta = points[:, None, :] - points[None, :, :]
    kernel = np.exp(-np.sum(delta * delta, axis=2) / (2 * length * length))
    trend = np.column_stack([np.ones(len(points)), points / length])
    system = np.block([[kernel + np.eye(len(points)) * 1e-10, trend], [trend.T, np.zeros((3, 3))]])
    coefficients = np.linalg.solve(system, np.concatenate([elevations, np.zeros(3)]))
    result = coefficients[-3] + coefficients[-2] * xx / length + coefficients[-1] * yy / length
    for point, coefficient in zip(points, coefficients[:-3]):
        result += coefficient * np.exp(-((xx - point[0]) ** 2 + (yy - point[1]) ** 2) / (2 * length * length))
    return result


def polyline_samples(points, spacing):
    points = np.asarray(points, dtype=float)
    lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
    if len(points) < 2 or np.any(lengths <= 0):
        raise ValueError("A reach needs at least two distinct consecutive control points.")
    station = np.concatenate([[0.0], np.cumsum(lengths)])
    samples = []
    stations = []
    for index, length in enumerate(lengths):
        count = max(1, math.ceil(length / spacing))
        t = np.arange(count, dtype=float) / count
        samples.extend(points[index] + t[:, None] * (points[index + 1] - points[index]))
        stations.extend(station[index] + t * length)
    samples.append(points[-1])
    stations.append(station[-1])
    return np.asarray(samples), np.asarray(stations), station


def reach_profile(reach, nodes, length):
    profile = reach.get("profile")
    if profile:
        fractions = np.array([p.get("fraction", p.get("t")) for p in profile], dtype=float)
        elevations = np.array([p.get("z_m", p.get("bed_m")) for p in profile], dtype=float)
    else:
        fractions = np.array([0.0, 1.0])
        elevations = np.array([nodes[reach["from"]]["bed_m"], nodes[reach["to"]]["bed_m"]], dtype=float)
    if fractions[0] != 0 or fractions[-1] != 1 or np.any(np.diff(fractions) <= 0):
        raise ValueError("Profile fractions must strictly increase from zero to one: " + reach["id"])
    return fractions * length, elevations


def project_polyline(points, xx, yy):
    """Nearest continuous polyline station and distance, with deterministic ties."""
    minimum = np.full(xx.shape, np.inf)
    along = np.zeros(xx.shape)
    offset = 0.0
    for start, end in zip(points[:-1], points[1:]):
        delta = end - start
        length = float(np.linalg.norm(delta))
        t = np.clip(((xx - start[0]) * delta[0] + (yy - start[1]) * delta[1]) / (length * length), 0, 1)
        d2 = (xx - start[0] - t * delta[0]) ** 2 + (yy - start[1] - t * delta[1]) ** 2
        select = d2 < minimum
        minimum[select] = d2[select]
        along[select] = offset + t[select] * length
        offset += length
    return np.sqrt(minimum), along


def raster_path(samples, stations, resolution, shape):
    ny, nx = shape
    sample_stations = stations.copy()
    cells = np.rint(samples / resolution).astype(int)
    cells[:, 0] = np.clip(cells[:, 0], 0, nx - 1)
    cells[:, 1] = np.clip(cells[:, 1], 0, ny - 1)
    flat = cells[:, 1] * nx + cells[:, 0]
    keep = np.concatenate([[True], np.diff(flat) != 0])
    flat, stations = flat[keep], stations[keep]
    path, path_stations, positions = [], [], {}
    alias = {"loop_count": 0, "maximum_station_span_m": 0.0, "maximum_displacement_m": 0.0}
    for cell, station in zip(flat, stations):
        cell = int(cell)
        if cell in positions:
            previous = positions[cell]
            span = float(station - path_stations[previous])
            origin = np.array([cell % nx, cell // nx]) * resolution
            # Quantization-only hairpins fit inside one diagonal cell of the
            # repeated center. Larger loops are unresolved at this resolution.
            removed_samples = samples[(sample_stations >= path_stations[previous]) & (sample_stations <= station)]
            deviation = float(np.linalg.norm(removed_samples - origin, axis=1).max()) if len(removed_samples) else 0.0
            if span > resolution * 3 or deviation > resolution * math.sqrt(2) + 1e-6:
                raise ValueError("A resolved channel loop revisits a raster cell; refine controls or resolution.")
            alias["loop_count"] += 1
            alias["maximum_station_span_m"] = max(alias["maximum_station_span_m"], span)
            alias["maximum_displacement_m"] = max(alias["maximum_displacement_m"], deviation)
            for old in path[previous + 1:]: positions.pop(old)
            del path[previous + 1:]; del path_stations[previous + 1:]
        else:
            positions[cell] = len(path)
            path.append(cell); path_stations.append(float(station))
    flat, stations = np.asarray(path, dtype=np.int64), np.asarray(path_stations)
    delta = np.abs(np.diff(np.column_stack([flat % nx, flat // nx]), axis=0))
    if np.any(delta > 1):
        raise AssertionError("Rasterization disconnected a channel.")
    stations[0], stations[-1] = 0.0, stations[-1]
    return flat, stations, alias


def reconcile_channel_raster(fixed, channels, nodes, world, resolution):
    """Enforce a decreasing cell DAG without moving any authored junction."""
    nx = fixed.shape[1]
    targets = fixed.ravel().copy()
    edges = {int(cell): set() for cell in np.flatnonzero(np.isfinite(targets))}
    indegree = {cell: 0 for cell in edges}
    locks = {}
    for channel in channels:
        for a, b in zip(channel["path"][:-1], channel["path"][1:]):
            a, b = int(a), int(b)
            if b not in edges[a]:
                edges[a].add(b); indegree[b] += 1
        for index, node_id in ((0, channel["from"]), (-1, channel["to"])):
            cell = int(channel["path"][index]); value = float(nodes[node_id]["bed_m"])
            if cell in locks and abs(locks[cell] - value) > 1e-8:
                raise ValueError("Different authored hydraulic nodes collapse to one grid cell.")
            locks[cell] = value; targets[cell] = value
    queue = [cell for cell, degree in indegree.items() if degree == 0]
    heapq.heapify(queue); order = []
    while queue:
        cell = heapq.heappop(queue); order.append(cell)
        for successor in sorted(edges[cell]):
            indegree[successor] -= 1
            if indegree[successor] == 0: heapq.heappush(queue, successor)
    if len(order) != len(edges):
        residual = {cell for cell in edges if indegree[cell] > 0}
        involved = [channel["id"] for channel in channels if any(int(cell) in residual for cell in channel["path"])]
        raise ValueError("Rasterized channel graph contains a cycle at " + str(resolution) + "m; this resolution cannot preserve the authored reach network. Affected downstream reaches: " + ", ".join(involved))
    values = targets.copy()
    for cell in reversed(order):
        if edges[cell]:
            required = max(values[successor] + 0.0001 for successor in edges[cell])
            if cell in locks and required > locks[cell] + 1e-8:
                raise ValueError("Rasterized channel junction cannot preserve its locked elevation.")
            values[cell] = max(values[cell], required)
    maximum = float(np.max(np.abs(values[np.isfinite(targets)] - targets[np.isfinite(targets)])))
    if maximum > resolution * 0.05:
        raise ValueError("Channel raster conditioning exceeds the bounded discretization allowance.")
    fixed.ravel()[np.isfinite(targets)] = values[np.isfinite(targets)]
    return maximum


def polygon_mask(points, xx, yy):
    inside = np.zeros(xx.shape, dtype=bool)
    for first, second in zip(points, np.roll(points, -1, axis=0)):
        if first[1] == second[1]:
            continue
        crossed = ((first[1] > yy) != (second[1] > yy)) & (xx < (second[0] - first[0]) * (yy - first[1]) / (second[1] - first[1]) + first[0])
        inside ^= crossed
    return inside


def apply_wetlands(controls, raw, xx, yy):
    world = world_of(controls)
    mask = np.zeros(raw.shape, dtype=bool)
    stages = np.full(raw.shape, np.nan)
    for wetland in controls.get("wetlands", []):
        points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in wetland["polygon"]])
        selected = polygon_mask(points, xx, yy)
        stage = float(wetland.get("water_level_m", wetland.get("reference_water_level_m", np.mean(wetland.get("water_level_range_m", [63.65, 64.2])))))
        depth = float(wetland.get("bed_depth_m", 0.6))
        # This first pass records the authored domain only. Relief is constructed
        # after channel projection, with a blended fringe and wet/dry mixture.
        mask |= selected
        stages[selected] = stage
    return raw, mask, stages


def apply_lowland_corridors(controls, background, xx, yy):
    """Authored broad natural-background constraints, distinct from excavation."""
    world = world_of(controls)
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    reaches = {reach["id"]: reach for reach in controls["hydrology"]["reaches"]}
    for corridor in controls.get("lowland_corridors", []):
        nearest = np.full(background.shape, np.inf)
        stages = np.zeros(background.shape)
        for reach_id in corridor["reach_ids"]:
            reach = reaches[reach_id]
            points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in reach["points"]])
            distance, along = project_polyline(points, xx, yy)
            length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
            head = float(nodes[reach["from"]]["water_level_m"])
            tail = float(nodes[reach["to"]]["water_level_m"])
            chosen = distance < nearest
            nearest[chosen] = distance[chosen]
            stages[chosen] = head + (tail - head) * along[chosen] / length
        half_width = float(corridor.get("core_half_width_m", 180))
        blend = float(corridor.get("blend_width_m", 400))
        t = np.clip((nearest - half_width) / blend, 0, 1)
        weight = 1 - t * t * (3 - 2 * t)
        target = stages + float(corridor.get("relative_to_water_level_m", 3.5))
        desired = background * (1 - weight) + target * weight
        background = np.minimum(background, desired)
    return background


def apply_floodplains(controls, raw, fixed, xx, yy):
    """Bounded agricultural floodplain controls; berms are technical proposals."""
    world = world_of(controls)
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    masks = {}
    for plain in controls.get("floodplains", []):
        points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in plain["polygon"]])
        inside = polygon_mask(points, xx, yy)
        reference_stage = float(nodes[plain["reference_node"]]["water_level_m"])
        low, high = map(float, plain.get("ground_offset_range_m", [0.5, 1.0]))
        normalized_north = np.clip((yy - points[:, 1].min()) / max(1, np.ptp(points[:, 1])), 0, 1)
        base = reference_stage + low + (high - low) * normalized_north
        angle = math.radians(float(plain.get("berm_angle_degrees", 15)))
        spacing = float(plain.get("berm_spacing_m", 90))
        width = float(plain.get("berm_width_m", 10))
        transverse = xx * math.cos(angle) + yy * math.sin(angle)
        phase = (transverse + spacing / 2) % spacing - spacing / 2
        berm = float(plain.get("berm_height_m", 1.0)) * np.exp(-(phase / width) ** 2)
        target = base + berm
        boundary_distance, _ = project_polyline(np.vstack([points, points[0]]), xx, yy)
        t = np.clip(boundary_distance / float(plain.get("blend_width_m", 180)), 0, 1)
        weight = 1 - t * t * (3 - 2 * t)
        weight[inside] = 1
        change = (weight > 0) & ~np.isfinite(fixed)
        raw[change] = raw[change] * (1 - weight[change]) + target[change] * weight[change]
        if plain.get("drainage_corridor_points"):
            corridor_points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in plain["drainage_corridor_points"]])
            distance, along = project_polyline(corridor_points, xx, yy)
            length = float(np.linalg.norm(np.diff(corridor_points, axis=0), axis=1).sum())
            half_width = float(plain.get("drainage_corridor_half_width_m", 70))
            blend = float(plain.get("drainage_corridor_blend_width_m", plain.get("drainage_corridor_blend_m", 120)))
            t = np.clip((distance - half_width) / blend, 0, 1)
            weight = 1 - t * t * (3 - 2 * t)
            # A broad falling ground apron, not an added river, pipe or channel.
            apron = reference_stage + low * (1 - along / length)
            desired = raw * (1 - weight) + apron * weight
            change = (weight > 0) & ~np.isfinite(fixed)
            raw[change] = np.minimum(raw[change], desired[change])
        masks[plain["id"]] = {"mask": inside, "berm": inside & (berm >= float(plain.get("berm_height_m", 1.0)) * 0.5),
                               "normal_stage_m": reference_stage, "reference_node": plain["reference_node"],
                               "target_base": base, "technical_berm": berm}
    return raw, masks


def channel_constraints(controls, raw, xx, yy, resolution):
    world = world_of(controls)
    hydro = controls["hydrology"]
    nodes = {n["id"]: n for n in hydro["nodes"]}
    fixed = np.full(raw.shape, np.nan)
    water = np.full(raw.shape, np.nan)
    channel_reach = np.full(raw.shape, -1, dtype=np.int16)
    distance_to_channel = np.full(raw.shape, np.inf)
    nearby_bed = np.zeros(raw.shape)
    nearby_depth = np.zeros(raw.shape)
    nearby_width = np.ones(raw.shape)
    channels = []
    envelopes = []
    for reach in hydro["reaches"]:
        if reach.get("kind", "natural") != "natural":
            continue
        points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in reach["points"]])
        for endpoint, node_id in ((points[0], reach["from"]), (points[-1], reach["to"])):
            expected = xy_m(nodes[node_id]["xy"], world["width_m"], world["height_m"])
            if np.linalg.norm(endpoint - expected) > 1e-5:
                raise ValueError("Reach endpoint does not match its declared junction: " + reach["id"])
        samples, stations, breaks = polyline_samples(points, resolution / 4)
        profile_s, profile_z = reach_profile(reach, nodes, breaks[-1])
        if np.any(np.diff(profile_z) >= 0):
            raise ValueError("Natural river profile must descend strictly: " + reach["id"])
        if abs(profile_z[0] - nodes[reach["from"]]["bed_m"]) > 1e-6 or abs(profile_z[-1] - nodes[reach["to"]]["bed_m"]) > 1e-6:
            raise ValueError("Profile elevations disagree at a shared junction: " + reach["id"])
        try:
            cells, stations, alias = raster_path(samples, stations, resolution, raw.shape)
        except ValueError as error:
            raise ValueError(reach["id"] + ": " + str(error)) from error
        stations[-1] = breaks[-1]
        bed = np.interp(stations, profile_s, profile_z)
        depth = float(reach.get("water_depth_m", 1.2))
        for node_id in (reach["from"], reach["to"]):
            node = nodes[node_id]
            if "water_level_m" in node and abs(float(node["water_level_m"]) - float(node["bed_m"]) - depth) > 1e-6:
                raise ValueError("Natural water-level/depth mismatch at shared node: " + node_id)
        half_width = float(reach.get("half_width_m", 14))
        distance, along = project_polyline(points, xx, yy)
        bed_field = np.interp(along, profile_s, profile_z)
        nearest = distance < distance_to_channel
        distance_to_channel[nearest] = distance[nearest]
        nearby_bed[nearest] = bed_field[nearest]
        nearby_depth[nearest] = depth
        nearby_width[nearest] = half_width
        valley_width = float(reach.get("valley_half_width_m", 240))
        bank_rise = float(reach.get("bank_rise_m", 9))
        envelope = bed_field + depth + bank_rise * (distance / valley_width) ** 1.4
        weight = np.clip(1 - distance / valley_width, 0, 1)
        weight = weight * weight * (3 - 2 * weight)
        envelopes.append((envelope, weight))
        bank_core = float(reach.get("bank_constraint_core_m", max(half_width, 2 * resolution)))
        bank_blend = float(reach.get("bank_constraint_blend_m", 80))
        index = len(channels)
        fixed_flat, water_flat, reach_flat = fixed.ravel(), water.ravel(), channel_reach.ravel()
        for cell, z in zip(cells, bed):
            if not np.isnan(fixed_flat[cell]) and abs(fixed_flat[cell] - z) > max(0.15, resolution * 0.03):
                raise ValueError("Incompatible channel elevations share a raster cell near " + reach["id"])
            if np.isnan(fixed_flat[cell]) or z < fixed_flat[cell]:
                fixed_flat[cell], water_flat[cell], reach_flat[cell] = z, z + depth, index
        channels.append({"id": reach["id"], "path": cells, "station_m": stations, "bed_m": bed,
                         "water_m": bed + depth, "kind": "natural", "length_m": float(breaks[-1]),
                         "half_width_m": half_width, "profile_s": profile_s, "profile_z": profile_z,
                         "from": reach["from"], "to": reach["to"],
                         "bank_constraint_core_m": bank_core, "bank_constraint_blend_m": bank_blend,
                         "points_m": points, "water_depth_m": depth})
        channels[-1]["raster_alias"] = alias
    if not channels:
        raise ValueError("At least one authored natural river is required.")
    raster_adjustment = reconcile_channel_raster(fixed, channels, nodes, world, resolution)
    for channel in channels:
        channel["maximum_network_raster_adjustment_m"] = raster_adjustment
    for envelope, weight in envelopes:
        raw = np.minimum(raw, raw * (1 - weight) + envelope * weight)
    raw[np.isfinite(fixed)] = fixed[np.isfinite(fixed)]
    wet = distance_to_channel <= nearby_width
    water[wet] = nearby_bed[wet] + nearby_depth[wet]
    return raw, fixed, water, channel_reach, channels, distance_to_channel, nearby_bed + nearby_depth


def apply_local_bank_constraints(raw, fixed, channels, xx, yy):
    """Compose compact banks after all regional landform shaping, exactly once.

    A global nearest-reach floor creates Voronoi cliffs. Applying the local floor
    before regional lowlands allows those lowlands to erase the final banks and
    lets water shortcut around its authored waterfall. Independent continuous
    reach contributions at the final composition boundary avoid both defects.
    """
    for channel in channels:
        distance, along = project_polyline(channel["points_m"], xx, yy)
        bed = np.interp(along, channel["profile_s"], channel["profile_z"])
        width = channel["half_width_m"]
        cross_section = channel["water_depth_m"] * np.minimum(distance / width, 1) ** 2
        floor = bed + cross_section + np.maximum(distance - width, 0) * 0.002
        t = np.clip((distance - channel["bank_constraint_core_m"]) / channel["bank_constraint_blend_m"], 0, 1)
        weight = 1 - t * t * (3 - 2 * t)
        raw = np.maximum(raw, raw * (1 - weight) + floor * weight)
    raw[np.isfinite(fixed)] = fixed[np.isfinite(fixed)]
    return raw


def priority_flood(raw, fixed, epsilon=0.001):
    """Minimum upward conditioning with immutable authored river-cell elevations.

    Every popped nonchannel cell has a strictly lower already-visited neighbour.
    Actual final receivers are computed separately; the flood's parent tree is
    deliberately not used as evidence of drainage correctness.
    """
    ny, nx = raw.shape
    result = raw.copy()
    visited = np.isfinite(fixed)
    cells = np.flatnonzero(visited)
    queue = [(float(result.ravel()[cell]), int(cell)) for cell in cells]
    heapq.heapify(queue)
    while queue:
        elevation, cell = heapq.heappop(queue)
        row, col = divmod(cell, nx)
        for dr, dc in OFFSETS:
            rr, cc = row + dr, col + dc
            if 0 <= rr < ny and 0 <= cc < nx and not visited[rr, cc]:
                visited[rr, cc] = True
                conditioned = max(float(raw[rr, cc]), elevation + epsilon)
                result[rr, cc] = conditioned
                heapq.heappush(queue, (conditioned, rr * nx + cc))
    return result


def d8_receivers(height, resolution, outlet):
    """Independent steepest-downslope D8 routing on the actual final DEM."""
    ny, nx = height.shape
    best = np.zeros_like(height)
    receivers = np.full(height.shape, -2, dtype=np.int32)
    indices = np.arange(height.size, dtype=np.int32).reshape(height.shape)
    for dr, dc in OFFSETS:
        src_r = slice(max(0, -dr), min(ny, ny - dr))
        src_c = slice(max(0, -dc), min(nx, nx - dc))
        dst_r = slice(max(0, dr), min(ny, ny + dr))
        dst_c = slice(max(0, dc), min(nx, nx + dc))
        slope = (height[src_r, src_c] - height[dst_r, dst_c]) / (resolution * math.hypot(dr, dc))
        select = slope > best[src_r, src_c]
        best[src_r, src_c][select] = slope[select]
        receivers[src_r, src_c][select] = indices[dst_r, dst_c][select]
    receivers.ravel()[outlet] = -1
    return receivers


def routing_accumulation(height, receivers):
    order = np.argsort(height.ravel(), kind="stable")[::-1]
    accumulation = np.ones(height.size, dtype=np.int64)
    flat = receivers.ravel()
    for cell in order:
        target = flat[cell]
        if target >= 0:
            accumulation[target] += accumulation[cell]
    return accumulation.reshape(height.shape)


def path_to_outlet(start, receivers, limit=None):
    flat = receivers.ravel()
    path = []
    cell = int(start)
    for _ in range(limit or flat.size + 1):
        if cell < 0:
            return path, cell
        path.append(cell)
        cell = int(flat[cell])
    return path, -3


def engineered_report(controls, height=None, xx=None, yy=None, resolution=8, natural_fixed=None):
    nodes = {n["id"]: n for n in controls["hydrology"]["nodes"]}
    reports = []
    world = world_of(controls)
    engineered_height = None if height is None else height.copy()
    engineered_mask = None if height is None else np.zeros(height.shape, dtype=bool)
    engineering_fixed = None if height is None else natural_fixed.copy() if natural_fixed is not None else np.full(height.shape, np.nan)
    corridors = []
    classified_masks = None if height is None else {name: np.zeros(height.shape, dtype=bool) for name in ("passive_engineered", "natural_backwater", "anomalous_engineered")}
    for reach in controls["hydrology"]["reaches"]:
        kind = reach.get("kind", "natural")
        if kind == "natural":
            continue
        points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in reach["points"]])
        length = float(np.linalg.norm(np.diff(points, axis=0), axis=1).sum())
        source = float(reach.get("upstream_level_m", nodes[reach["from"]].get("water_level_m", nodes[reach["from"]]["bed_m"])))
        tail = float(reach.get("downstream_level_m", nodes[reach["to"]].get("water_level_m", nodes[reach["to"]]["bed_m"])))
        rise = tail - source
        anomalous = kind == "anomalous_engineered" or (reach.get("passive_flow") is False and kind != "backwater")
        report = {"id": reach["id"], "kind": kind, "length_m": length,
                        "source_level_m": source, "tail_level_m": tail,
                        "signed_drop_m": -rise, "slope": -rise / length,
                        "positive_head_requirement_m": max(0.0, rise),
                        "passive_gravity_feasible": rise < 0 and not anomalous,
                        "status": "canon_anomaly_unknown_energy_excluded_from_natural_flow" if anomalous else "unresolved_backwater_topology" if kind == "backwater" else "provisional_controlled_gravity_edge" if rise < 0 else "unresolved_passive_head_conflict",
                        "operating_states": reach.get("operating_states", []),
                        "not_solved": "No discharge, flood hydrograph, lock-cycle or water-balance simulation."}
        if height is not None:
            distance, along = project_polyline(points, xx, yy)
            ps, pz = reach_profile(reach, nodes, length)
            designed_bed = np.interp(along, ps, pz)
            width = float(reach.get("half_width_m", 4))
            corridor = distance <= max(width, resolution * 0.75)
            depth = float(reach.get("water_depth_m", 1.2))
            channel_design = designed_bed + depth * np.minimum(distance / width, 1) ** 2
            cut = np.maximum(height - channel_design, 0)
            support = np.maximum(designed_bed - height, 0)
            engineered_height[corridor] = np.minimum(engineered_height[corridor], channel_design[corridor])
            engineered_mask |= corridor
            classification = "natural_backwater" if kind == "backwater" else "anomalous_engineered" if anomalous else "passive_engineered"
            classified_masks[classification] |= corridor
            report["terrain_change_classification"] = classification
            samples, sample_stations, _ = polyline_samples(points, resolution / 4)
            cells, sample_stations, alias = raster_path(samples, sample_stations, resolution, height.shape)
            sample_stations[-1] = length
            raster_bed = np.interp(sample_stations, ps, pz)
            for cell, bed_value in zip(cells, raster_bed):
                engineered_height.ravel()[cell] = min(engineered_height.ravel()[cell], bed_value)
                prior = engineering_fixed.ravel()[cell]
                engineering_fixed.ravel()[cell] = bed_value if not np.isfinite(prior) else min(prior, bed_value)
            report["raster_alias"] = alias
            report.update({"half_width_m": width, "raster_represented_half_width_m": max(width, resolution * 0.75),
                           "design_bed_head_m": float(pz[0]), "design_bed_tail_m": float(pz[-1]),
                           "design_bed_gradient_min": float(np.min(-np.diff(pz) / np.diff(ps))),
                           "design_bed_gradient_max": float(np.max(-np.diff(pz) / np.diff(ps))),
                           "corridor_area_m2": int(corridor.sum()) * resolution ** 2,
                           "excavation_volume_m3": float(cut[corridor].sum() * resolution ** 2),
                           "excavation_max_depth_m": float(cut[corridor].max()) if corridor.any() else 0,
                           "unsupported_bed_above_ground_max_m": float(support[corridor].max()) if corridor.any() else 0,
                           "surface_state": "separate_open_or_uncontrolled_corridor_design; not inserted into baseline gated natural-routing DEM",
                           "raster_limitation": "Widths under two cells are analytical corridor controls, not resolved canal cross-sections."})
            corridors.append(corridor)
        reports.append(report)
    if height is None:
        return reports
    unconditioned = engineered_height.copy()
    engineered_height = priority_flood(engineered_height, engineering_fixed)
    for report, corridor in zip(reports, corridors):
        report["open_surface_conditioning_raise_max_m"] = float((engineered_height - unconditioned).max())
        actual_excavation = np.maximum(height - engineered_height, 0)
        report["ideal_cross_section_excavation_max_m"] = report["excavation_max_depth_m"]
        report["excavation_max_depth_m"] = float(actual_excavation[corridor].max()) if corridor.any() else 0
        report["excavation_volume_m3"] = float(actual_excavation[corridor].sum() * resolution ** 2)
        report["earthwork_measurement"] = "Actual sampled open-design minus baseline height; overlapping reach-corridor volumes must not be summed. Narrow works need finer local survey."
    return reports, engineered_height, engineered_mask, classified_masks


def slope_degrees(height, resolution):
    dy, dx = np.gradient(height, resolution)
    return np.degrees(np.arctan(np.hypot(dx, dy)))


def adjacent_jump_report(height, x, y, controls, waterfall_buffer_m=200):
    """Expose abrupt raster seams separately from explicitly authored waterfalls."""
    xx, yy = np.meshgrid(x, y)
    distance = np.full(height.shape, np.inf)
    world = world_of(controls)
    for reach in controls["hydrology"]["reaches"]:
        if reach.get("feature_type") != "waterfall":
            continue
        points = np.array([xy_m(point, world["width_m"], world["height_m"]) for point in reach["points"]])
        candidate, _ = project_polyline(points, xx, yy)
        distance = np.minimum(distance, candidate)
    maximum = 0.0
    endpoint_pair = None
    ny, nx = height.shape
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        rr, cc = slice(0, ny - dr), slice(max(0, -dc), min(nx, nx - dc))
        tr, tc = slice(dr, ny), slice(max(0, dc), min(nx, nx + dc))
        eligible = (distance[rr, cc] > waterfall_buffer_m) & (distance[tr, tc] > waterfall_buffer_m)
        difference = np.where(eligible, np.abs(height[rr, cc] - height[tr, tc]), -1)
        row, col = np.unravel_index(difference.argmax(), difference.shape)
        if difference[row, col] > maximum:
            maximum = float(difference[row, col])
            row0, col0 = int(row), int(col) + max(0, -dc)
            endpoint_pair = [[float(x[col0]), float(y[row0])], [float(x[col0 + dc]), float(y[row0 + dr])]]
    return {"maximum_eight_neighbor_jump_outside_waterfalls_m": maximum,
            "waterfall_exclusion_buffer_m": waterfall_buffer_m, "edge_endpoints_east_north_m": endpoint_pair,
            "interpretation": "Continuity diagnostic; remaining steep upland fringe needs local refinement. No universal natural-slope certification."}


def control_structure_report(controls):
    nodes = {node["id"]: node for node in controls["hydrology"]["nodes"]}
    result = []
    for structure in controls["hydrology"].get("engineered_controls", []):
        head = float(nodes[structure["upstream"]]["water_level_m"])
        tail = float(nodes[structure["downstream"]]["water_level_m"])
        declared = float(structure["head_drop_m"])
        result.append({"id": structure["id"], "type": structure["type"], "upstream_level_m": head,
                       "downstream_level_m": tail, "measured_head_drop_m": head - tail,
                       "declared_head_drop_m": declared, "level_constraint_matches": abs(head - tail - declared) < 1e-8,
                       "status": "Static level/head envelope only; no gate, lock-cycle, wheel power or discharge simulation."})
    return result


def connected_stage_screen(height, stage, water, rise):
    """Conservative stage-rise susceptibility connected to existing wet cells.

    This excludes isolated low pockets from the screen. It remains an uncalibrated
    static topographic scenario, not a simulated flood frequency or hydrograph.
    """
    eligible = height <= stage + rise
    reached = eligible & np.isfinite(water) & (height <= water)
    queue = deque(map(int, np.flatnonzero(reached)))
    ny, nx = height.shape
    while queue:
        cell = queue.popleft(); row, col = divmod(cell, nx)
        for dr, dc in OFFSETS:
            rr, cc = row + dr, col + dc
            if 0 <= rr < ny and 0 <= cc < nx and eligible[rr, cc] and not reached[rr, cc]:
                reached[rr, cc] = True; queue.append(rr * nx + cc)
    return reached


def settlement_capacity(controls, xx, yy, height, water, resolution, stage, channel_distance, engineering_exclusion=None):
    world = world_of(controls)
    slope = slope_degrees(height, resolution)
    masks, metrics, plot_sites = {}, [], {}
    if engineering_exclusion is None:
        engineering_exclusion = np.zeros(height.shape, dtype=bool)
    scenario_rise = float(world.get("flood_scenario_rise_m", 1.5))
    scenario_exposed = connected_stage_screen(height, stage, water, scenario_rise)
    access_corridor = np.zeros(height.shape, dtype=bool)
    for route in controls.get("routes", []):
        points = np.array([xy_m(p, world["width_m"], world["height_m"]) for p in route["points"]])
        distance, _ = project_polyline(points, xx, yy)
        access_corridor |= distance <= float(route.get("width_m", 12)) / 2
    for settlement in controls.get("settlements", []):
        center = xy_m(settlement["xy"], world["width_m"], world["height_m"])
        spans = settlement.get("span_m", settlement.get("built_up_span_m", [300, 500]))
        span = float(spans[-1] if isinstance(spans, list) else spans)
        radial = np.hypot(xx - center[0], yy - center[1])
        axes = settlement.get("envelope_axes_m", [span, span])
        elliptical_distance = np.sqrt(((xx - center[0]) / (float(axes[0]) / 2)) ** 2 + ((yy - center[1]) / (float(axes[1]) / 2)) ** 2)
        envelope = elliptical_distance <= 1
        working_radius = float(settlement.get("working_radius_m", span))
        working = (radial <= working_radius) & ~envelope
        # Flood exposure is a static local channel-stage freeboard screen, not a flood model.
        freeboard = height - stage
        max_slope = float(settlement.get("max_building_slope_deg", 8))
        min_freeboard = float(settlement.get("min_freeboard_m", 3))
        dry = ~np.isfinite(water) | (height > water)
        suitable = envelope & (slope <= max_slope) & (freeboard >= min_freeboard) & dry & ~access_corridor & ~engineering_exclusion
        adapted = envelope & (slope <= max_slope) & ~suitable & ~access_corridor & ~engineering_exclusion
        scenario_suitable = suitable & ~scenario_exposed
        cell_area = resolution * resolution
        developable = int(suitable.sum()) * cell_area
        footprint = float(settlement.get("footprint_m2", 120))
        coverage = float(settlement.get("plot_coverage", 0.35))
        road_fraction = float(settlement.get("road_fraction", 0.25))
        capacity = math.floor(developable * (1 - road_fraction) * coverage / footprint)
        min_scale = float(spans[0]) / float(axes[0]) if isinstance(spans, list) else 1.0
        compact_candidate = suitable & (elliptical_distance <= min(1, min_scale))
        compact_capacity = math.floor(int(compact_candidate.sum()) * cell_area * (1 - road_fraction) * coverage / footprint)
        spacing_cells = max(1, math.ceil(math.sqrt(footprint / (coverage * (1 - road_fraction))) / resolution))
        footprint_radius = max(1, math.ceil(math.sqrt(footprint) / (2 * resolution)))
        candidates = []
        adaptation_candidates = []
        scenario_candidates = []
        eligible = suitable.copy()
        adaptive_policy = settlement.get("policy") in ("fen", "fen_stilts", "wetland") or settlement.get("allow_stilts", False)
        adaptive_eligible = envelope & (slope <= max_slope) & ((stage - height) <= float(settlement.get("max_stilt_depth_m", 1.5))) & ~access_corridor & ~engineering_exclusion
        for rr in range(footprint_radius, height.shape[0] - footprint_radius, spacing_cells):
            for cc in range(footprint_radius, height.shape[1] - footprint_radius, spacing_cells):
                if eligible[rr - footprint_radius:rr + footprint_radius + 1, cc - footprint_radius:cc + footprint_radius + 1].all():
                    candidates.append((float(xx[rr, cc]), float(yy[rr, cc]), float(height[rr, cc])))
                    if scenario_suitable[rr - footprint_radius:rr + footprint_radius + 1, cc - footprint_radius:cc + footprint_radius + 1].all():
                        scenario_candidates.append((float(xx[rr, cc]), float(yy[rr, cc]), float(height[rr, cc])))
                elif adaptive_policy and adaptive_eligible[rr - footprint_radius:rr + footprint_radius + 1, cc - footprint_radius:cc + footprint_radius + 1].all():
                    adaptation_candidates.append((float(xx[rr, cc]), float(yy[rr, cc]), float(height[rr, cc])))
        plot_sites[settlement["id"]] = candidates
        capacity = min(capacity, len(candidates))
        scenario_capacity = min(math.floor(int(scenario_suitable.sum()) * cell_area * (1 - road_fraction) * coverage / footprint), len(scenario_candidates))
        compact_sites = int(sum((((px - center[0]) / (float(axes[0]) / 2)) ** 2 + ((py - center[1]) / (float(axes[1]) / 2)) ** 2) <= min(1, min_scale) ** 2 for px, py, _ in candidates))
        compact_capacity = min(compact_capacity, compact_sites)
        buildings = settlement.get("buildings", settlement.get("roofed_buildings", [0, 0]))
        required = int(buildings[-1])
        masks[settlement["id"]] = {"envelope": envelope, "candidate": suitable, "adaptation": adapted, "working": working,
                                          "slope_deg": slope, "freeboard_m": freeboard, "access": access_corridor & (radial <= working_radius),
                                          "scenario_exposed": scenario_exposed & envelope, "scenario_candidate": scenario_suitable,
                                          "engineering_exclusion": engineering_exclusion & envelope}
        metrics.append({"id": settlement["id"], "proposed_buildings": buildings, "built_up_span_m": span,
                        "envelope_area_m2": int(envelope.sum()) * cell_area,
                        "candidate_buildable_area_m2": developable,
                        "circulation_reserved_fraction": road_fraction, "footprint_m2": footprint,
                        "plot_coverage": coverage, "screened_roof_capacity": capacity,
                        "normal_stage_roof_capacity": capacity,
                        "flood_scenario_rise_m": scenario_rise,
                        "flood_scenario_exposed_area_m2": int((envelope & scenario_exposed).sum()) * cell_area,
                        "flood_scenario_safe_capacity": scenario_capacity,
                        "flood_screen_interpretation": "Static connected-by-elevation susceptibility; outside-screen capacity is not a flood safety certification.",
                        "capacity_terrain_state": "Combined open-design terrain; all engineered/backwater/anomalous water corridors excluded from building footprints.",
                        "excluded_waterworks_area_m2": int((envelope & engineering_exclusion).sum()) * cell_area,
                        "min_span_screened_roof_capacity": compact_capacity, "envelope_axes_m": axes,
                        "spaced_candidate_plot_count": len(candidates), "plot_spacing_m": spacing_cells * resolution,
                        "additional_adaptation_plot_count": len(adaptation_candidates),
                        "screened_total_capacity_with_adaptation": capacity + len(adaptation_candidates),
                        "raster_footprint_width_m": 2 * footprint_radius * resolution,
                        "upper_target_met_on_dry_ground": capacity >= required,
                        "adaptation_candidate_area_m2": int(adapted.sum()) * cell_area,
                        "working_land_low_slope_m2": int((working & (slope <= 6) & (freeboard >= min_freeboard) & dry).sum()) * cell_area,
                        "envelope_slope_p50_deg": float(np.median(slope[envelope])) if envelope.any() else None,
                        "envelope_slope_p95_deg": float(np.percentile(slope[envelope], 95)) if envelope.any() else None,
                        "minimum_freeboard_m": float(freeboard[envelope].min()) if envelope.any() else None,
                        "policy": settlement.get("policy", "unspecified"),
                        "waterfront_working_area_m2": int((envelope & (freeboard < min_freeboard) & (slope <= max_slope)).sum()) * cell_area,
                        "access_corridor_area_m2": int((access_corridor & envelope).sum()) * cell_area,
                        "grading_m3": 0,
                        "limitation": "Conservative terrain-fit center lattice and area-density screen; no buildings, cadastral plan, detailed earthworks or flood-frequency prediction."})
    return masks, metrics, plot_sites


def generate(controls, resolution_m=8.0):
    started = time.perf_counter()
    x, y = grid(controls, resolution_m)
    xx, yy = np.meshgrid(x, y)
    background = regional_field(controls, xx, yy)
    background = apply_lowland_corridors(controls, background, xx, yy)
    background, fen_mask, fen_stage = apply_wetlands(controls, background, xx, yy)
    raw, fixed, water, channel_reach, channels, channel_distance, reference_stage = channel_constraints(controls, background, xx, yy, resolution_m)
    raw, floodplain_masks = apply_floodplains(controls, raw, fixed, xx, yy)
    for wetland in controls.get("wetlands", []):
        points = np.array([xy_m(p, world_of(controls)["width_m"], world_of(controls)["height_m"]) for p in wetland["polygon"]])
        selected = polygon_mask(points, xx, yy)
        if wetland.get("water_level_mode") == "nearest_natural_reach" or "water_level_range_m" in wetland:
            level_range = wetland.get("water_level_range_m", [63.65, 64.2])
            stages = np.clip(reference_stage, min(level_range), max(level_range))
        else:
            constant_stage = float(wetland.get("water_level_m", wetland.get("reference_water_level_m", 64)))
            stages = np.full(raw.shape, constant_stage)
        # Explicit bounded fen microrelief: shallow channel fringes, low dry reed
        # hummocks, and two long wavelength deterministic swales. These are
        # technical landform controls, not unconstrained fractal terrain noise.
        depth = float(wetland.get("bed_depth_m", 0.6))
        wet_scale = float(wetland.get("wet_fringe_width_m", 35))
        dry_rise = float(wetland.get("hummock_height_m", 0.50))
        amplitude = float(wetland.get("microrelief_amplitude_m", 0.18))
        relief = (-depth * np.exp(-(channel_distance / wet_scale) ** 2)
                  + dry_rise * (1 - np.exp(-(channel_distance / 85) ** 2))
                  + amplitude * np.sin(xx / 93) * np.cos(yy / 127))
        boundary_points = np.vstack([points, points[0]])
        edge_distance, _ = project_polyline(boundary_points, xx, yy)
        apron = float(wetland.get("shore_apron_m", 120))
        transition = float(wetland.get("outer_transition_m", 500))
        t = np.clip((edge_distance - apron) / transition, 0, 1)
        weight = 1 - t * t * (3 - 2 * t)
        weight[selected] = 1
        # The exterior apron is a broad natural fen-valley landform, never a
        # settlement pad. Preserve the upstream plateau and waterfall lip.
        upland_guard = np.zeros(raw.shape)
        guard_id = wetland.get("upstream_guard_reach")
        if guard_id:
            reach = next(reach for reach in controls["hydrology"]["reaches"] if reach["id"] == guard_id)
            endpoints = np.array([xy_m(point, world_of(controls)["width_m"], world_of(controls)["height_m"]) for point in (reach["points"][0], reach["points"][-1])])
            direction = endpoints[1] - endpoints[0]
            direction /= np.linalg.norm(direction)
            center = endpoints.mean(axis=0)
            downstream = (xx - center[0]) * direction[0] + (yy - center[1]) * direction[1]
            transition_width = float(wetland.get("upstream_guard_transition_m", 500))
            t = np.clip(downstream / transition_width + 0.5, 0, 1)
            # Continuous authored upstream protection. Nearest-reach identity
            # must never act as a hard terrain-height selector at a Voronoi edge.
            upland_guard = 1 - t * t * (3 - 2 * t)
        # Protection also fades to zero at the fen boundary. Applying a full
        # guard only outside the polygon otherwise makes the polygon itself a
        # discontinuous cliff even when the upstream guard is smooth.
        boundary_fade = float(wetland.get("upstream_guard_boundary_fade_m", 200))
        fade_t = np.clip(edge_distance / boundary_fade, 0, 1)
        guard_strength = fade_t * fade_t * (3 - 2 * fade_t)
        weight[~selected] *= 1 - upland_guard[~selected] * guard_strength[~selected]
        dry_shore = dry_rise + 0.001 * np.minimum(edge_distance, apron) + amplitude * 0.4 * np.sin(xx / 93) * np.cos(yy / 127)
        target = stages + np.where(selected, relief, dry_shore)
        change = (weight > 0) & ~np.isfinite(fixed)
        raw[change] = raw[change] * (1 - weight[change]) + target[change] * weight[change]
        water[selected & ~np.isfinite(fixed)] = stages[selected & ~np.isfinite(fixed)]
    raw = apply_local_bank_constraints(raw, fixed, channels, xx, yy)
    height = priority_flood(raw, fixed, float(world_of(controls).get("drainage_epsilon_m", 0.001)))
    outlet_id = controls["hydrology"]["outlet"]
    nodes = {n["id"]: n for n in controls["hydrology"]["nodes"]}
    world = world_of(controls)
    outlet_xy = xy_m(nodes[outlet_id]["xy"], world["width_m"], world["height_m"])
    col, row = np.rint(outlet_xy / resolution_m).astype(int)
    if row not in (0, len(y) - 1) and col not in (0, len(x) - 1):
        raise ValueError("The declared final natural outlet must lie on the regional boundary.")
    outlet = int(row * len(x) + col)
    receivers = d8_receivers(height, resolution_m, outlet)
    accumulation = routing_accumulation(height, receivers)
    sinks = np.flatnonzero(receivers.ravel() == -2)
    fill = height - raw
    floodplain_reports = []
    for name, data in floodplain_masks.items():
        selected = data["mask"]
        stage = np.full(height.shape, data["normal_stage_m"])
        rise = float(world.get("flood_scenario_rise_m", 1.5))
        normal = connected_stage_screen(height, stage, water, 0)
        scenario = connected_stage_screen(height, stage, water, rise)
        data["normal_water"] = normal & selected
        data["scenario_exposed"] = scenario & selected
        berm_selected = data["berm"]
        floodplain_reports.append({"id": name, "area_m2": int(selected.sum()) * resolution_m ** 2,
                                   "reference_node": data["reference_node"], "normal_stage_m": data["normal_stage_m"],
                                   "ground_range_m": [float(height[selected].min()), float(height[selected].max())],
                                   "normal_connected_water_fraction": float(normal[selected].mean()),
                                   "scenario_rise_m": rise, "scenario_connected_exposed_fraction": float(scenario[selected].mean()),
                                   "berm_area_fraction": float(data["berm"][selected].mean()),
                                   "berm_ground_range_m": [float(height[berm_selected].min()), float(height[berm_selected].max())] if berm_selected.any() else [],
                                   "berm_scenario_noninundated_fraction": float((~scenario[berm_selected]).mean()) if berm_selected.any() else None,
                                   "nonberm_soil_ground_range_m": [float(height[selected & ~berm_selected].min()), float(height[selected & ~berm_selected].max())],
                                   "berm_proposal": "Sparse analytic parallel ridges; no trees, parcels, drains or construction authored.",
                                   "scenario_status": "Connected static elevation-level screen only; not a flood prediction."})
    fen_wet = fen_mask & (height <= water)
    fen_dry = fen_mask & (height > water)
    channel_reports = []
    channel_mask = np.isfinite(fixed)
    for channel in channels:
        actual = height.ravel()[channel["path"]]
        path, terminal = path_to_outlet(channel["path"][0], receivers)
        channel_reports.append({"id": channel["id"], "length_m": channel["length_m"],
                                "head_m": float(actual[0]), "tail_m": float(actual[-1]),
                                "minimum_sample_drop_m": float(np.min(-np.diff(actual))),
                                "sampled_uphill_segments": int(np.sum(np.diff(actual) > 1e-8)),
                                "reaches_declared_outlet": terminal == -1,
                                "routing_path_cells": len(path),
                                "routing_path_channel_fraction": float(channel_mask.ravel()[path].mean()) if path else 0,
                                "raster_alias": channel["raster_alias"],
                                "maximum_network_raster_adjustment_m": channel["maximum_network_raster_adjustment_m"]})
    engineered, height_engineered, engineered_mask, classified_masks = engineered_report(controls, height, xx, yy, resolution_m, fixed)
    masks, settlements, plot_sites = settlement_capacity(controls, xx, yy, height_engineered, water, resolution_m, reference_stage, channel_distance, engineered_mask)
    engineered_receivers = d8_receivers(height_engineered, resolution_m, outlet)
    engineered_sinks = np.flatnonzero(engineered_receivers.ravel() == -2)
    engineered_accumulation = routing_accumulation(height_engineered, engineered_receivers)
    fill_budget = float(world.get("maximum_conditioning_raise_m", 12))
    metrics = {"method": "Gaussian RBF regional field; immutable authored natural-channel skeleton; upward epsilon priority flood; independent steepest D8 validation",
               "resolution_m": resolution_m, "shape": list(height.shape), "cells": int(height.size),
               "width_m": world["width_m"], "height_m": world["height_m"],
               "seed": world.get("seed"), "seed_role": "Provenance only; this prototype has no random terms.",
               "elevation_range_m": [float(height.min()), float(height.max())],
               "outlet_cell": outlet, "outlet_accumulation_cells": int(accumulation.ravel()[outlet]),
               "accumulation_units": "Unweighted grid-sample count; cellsize-squared multiplication is an area proxy, not exact boundary-weighted catchment area.",
               "unintended_sinks": int(len(sinks)), "sink_cells": sinks[:40].tolist(),
               "all_cells_reach_outlet": int(accumulation.ravel()[outlet]) == height.size and len(sinks) == 0,
               "conditioning_raise_max_m": float(fill.max()), "conditioning_raise_p95_m": float(np.percentile(fill, 95)),
               "conditioning_raise_mean_m": float(fill.mean()), "conditioning_raise_volume_m3": float(fill.sum() * resolution_m ** 2),
               "conditioning_cells_fraction": float((fill > 1e-7).mean()),
               "conditioning_budget_m": fill_budget, "conditioning_budget_met": float(fill.max()) <= fill_budget,
               "channel_constraints_exact": bool(np.all(height[channel_mask] == fixed[channel_mask])),
               "fen": {"area_m2": int(fen_mask.sum()) * resolution_m ** 2,
                       "wet_ground_fraction": float(fen_wet.sum() / max(1, fen_mask.sum())),
                       "dry_ground_fraction": float(fen_dry.sum() / max(1, fen_mask.sum())),
                       "stage_range_m": [float(np.nanmin(water[fen_mask])), float(np.nanmax(water[fen_mask]))] if fen_mask.any() else [],
                       "slope_p50_deg": float(np.median(slope_degrees(height, resolution_m)[fen_mask])) if fen_mask.any() else None,
                       "slope_p95_deg": float(np.percentile(slope_degrees(height, resolution_m)[fen_mask], 95)) if fen_mask.any() else None},
               "natural_reaches": channel_reports, "engineered_reaches": engineered,
               "control_structures": control_structure_report(controls),
               "continuity": adjacent_jump_report(height, x, y, controls),
               "floodplains": floodplain_reports,
               "engineered_open_surface": {"sink_count": int(len(engineered_sinks)), "sink_cells": engineered_sinks.tolist(),
                                            "all_sinks_in_engineered_corridors": bool(np.all(engineered_mask.ravel()[engineered_sinks])),
                                            "outlet_accumulation_cells": int(engineered_accumulation.ravel()[outlet]),
                                            "all_cells_reach_outlet": int(engineered_accumulation.ravel()[outlet]) == height.size,
                                            "total_open_bed_design_change_volume_m3": float(np.maximum(height - height_engineered, 0).sum() * resolution_m ** 2),
                                            "terrain_change_by_class_volume_m3": {name: float(np.maximum(height - height_engineered, 0)[mask].sum() * resolution_m ** 2) for name, mask in classified_masks.items()},
                                            "volume_classification_note": "Natural-backwater reconstruction is not anthropogenic excavation. Class masks can overlap at junctions; do not sum their volumes.",
                                            "interpretation": "Open bed geometry drains to the region outlet; this is not a discharge or water-surface hydraulic solution." if len(engineered_sinks) == 0 else "Open bed contains sinks requiring explicit review; no unintended storage may be silently accepted."},
               "settlements": settlements,
               "height_sha256": hashlib.sha256(height.astype("<f8").tobytes()).hexdigest(),
               "raw_height_sha256": hashlib.sha256(raw.astype("<f8").tobytes()).hexdigest(),
               "receiver_sha256": hashlib.sha256(receivers.astype("<i4").tobytes()).hexdigest(),
               "seconds": time.perf_counter() - started,
               "limitations": ["Static elevation/routing prototype; no rainfall-runoff or calibrated hydraulic simulation.",
                               "Engineered and canon-anomalous waterways are separate level/head graphs, not fabricated natural D8 flow.",
                               "Raster resolution does not resolve individual locks, buildings, foundations, culverts or fen microtopography."]}
    return Result(x, y, raw, height, receivers, accumulation, channel_mask, channel_reach, water, channels, metrics, masks, fen_mask, channel_distance, reference_stage, height_engineered, engineered_mask, plot_sites, floodplain_masks)


def png16(path, values):
    """Write a deterministic grayscale 16-bit PNG using only the standard library."""
    height, width = values.shape
    scanlines = b"".join(b"\0" + row.astype(">u2").tobytes() for row in values)
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 16, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(scanlines, 9)) + chunk(b"IEND", b""))


def export(result, output, mesh_step=4):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    np.save(output / "height.npy", result.height.astype("<f4"), allow_pickle=False)
    np.savez_compressed(output / "terrain_arrays.npz", height=result.height, height_raw=result.height_raw,
                        receiver=result.receiver, accumulation=result.accumulation, channel_mask=result.channel_mask,
                        channel_reach=result.channel_reach, water_level=result.water_level, x=result.x, y=result.y,
                        fen_mask=result.fen_mask, height_engineered=result.height_engineered, engineered_mask=result.engineered_mask,
                        **{"floodplain_" + name: data["mask"] for name, data in result.floodplain_masks.items()},
                        **{"floodplain_scenario_" + name: data["scenario_exposed"] for name, data in result.floodplain_masks.items()})
    low, high = float(result.height.min()), float(result.height.max())
    encoded = np.rint((result.height - low) / (high - low) * 65535).astype(np.uint16)
    # Image rows north-to-south; arrays and OBJ retain y=north from south-west.
    png16(output / "height.png", encoded[::-1])
    calibration = {"array_origin": "south_west", "image_origin": "north_west", "axes": "x east, y north, z elevation metres",
                   "height_png_min_m": low, "height_png_max_m": high, "height_png_quantization_m": (high - low) / 65535,
                   "mesh_decimation_stride": mesh_step, "grid_cell_m": float(result.x[1] - result.x[0]),
                   "obj_authority": "Decimated inspection preview only; authoritative validation uses the full-resolution array.",
                   "authoritative_array": "height.npy (float32 metric elevations); terrain_arrays.npz also retains float64 model and routing."}
    (output / "calibration.json").write_text(json.dumps(calibration, indent=2) + "\n", encoding="utf-8")
    (output / "metrics.json").write_text(json.dumps(result.metrics, indent=2) + "\n", encoding="utf-8")
    (output / "candidate_plots.json").write_text(json.dumps({"purpose": "Terrain-capacity candidate centers only; no authored building placements.", "sites": result.plot_sites}, indent=2) + "\n", encoding="utf-8")
    rows = list(range(0, len(result.y), mesh_step))
    cols = list(range(0, len(result.x), mesh_step))
    if rows[-1] != len(result.y) - 1: rows.append(len(result.y) - 1)
    if cols[-1] != len(result.x) - 1: cols.append(len(result.x) - 1)
    with (output / "terrain.obj").open("w", encoding="ascii", newline="\n") as stream:
        stream.write("# Caelmor offline terrain, x east / y north / z up, metres\no Lowmark_terrain_prototype\n")
        for row in rows:
            for col in cols:
                stream.write(f"v {result.x[col]:.4f} {result.y[row]:.4f} {result.height[row,col]:.6f}\n")
        width = len(cols)
        for row in range(len(rows) - 1):
            for col in range(width - 1):
                a = row * width + col + 1
                stream.write(f"f {a} {a+1} {a+width+1}\nf {a} {a+width+1} {a+width}\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--controls", type=Path, default=Path(__file__).with_name("lowmark_controls.json"))
    parser.add_argument("--resolution", type=float, default=8)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--omit-lowland-corridors", action="store_true", help="Reproduce the rejected unconstrained-background engineering-depth comparison.")
    args = parser.parse_args(argv)
    controls = json.loads(args.controls.read_text(encoding="utf-8-sig"))
    if args.omit_lowland_corridors:
        controls["lowland_corridors"] = []
    result = generate(controls, args.resolution)
    result.metrics["controls_sha256"] = hashlib.sha256(args.controls.read_bytes()).hexdigest()
    result.metrics["configuration_overrides"] = ["lowland_corridors omitted for comparison"] if args.omit_lowland_corridors else []
    export(result, args.output, max(1, round(32 / args.resolution)))
    print(json.dumps({key: result.metrics[key] for key in ["resolution_m", "cells", "unintended_sinks", "all_cells_reach_outlet", "conditioning_raise_max_m", "seconds", "height_sha256"]}, indent=2))
    if (not result.metrics["all_cells_reach_outlet"] or not result.metrics["channel_constraints_exact"]
            or not result.metrics["conditioning_budget_met"]
            or any(reach["sampled_uphill_segments"] for reach in result.metrics["natural_reaches"])):
        raise SystemExit("Natural drainage validation failed; inspect metrics before using this terrain.")


if __name__ == "__main__":
    main()
