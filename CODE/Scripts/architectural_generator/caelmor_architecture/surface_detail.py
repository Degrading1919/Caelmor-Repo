"""Reusable periodic metric detail for atlas albedo and tiled normal maps.

Coordinates are in metres and repeat every :data:`DETAIL_PERIOD`. The sampler
has no Blender dependency; callers can share its aligned albedo/height detail
with a repeat-wrapped normal tile using metric UV0 divided by the same period.
"""
from __future__ import annotations

import math

import numpy as np


DETAIL_PERIOD = 2.0
_REGIONS = ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")
_CRAFT = ("ROUGH", "STANDARD", "FINE")
_FAMILIES = ("wood", "stone", "plaster", "roof", "iron", "leather", "charcoal")


def _hash(ix, iy, seed):
    mask = np.int64(0xFFFFFFFF)
    n = (ix.astype(np.int64) * 374761393 + iy.astype(np.int64) * 668265263
         + int(seed) * 1442695041) & mask
    n = ((n ^ (n >> 13)) * 1274126177) & mask
    n ^= n >> 16
    return n.astype(np.float64) / 2147483647.5 - 1.0


def _noise(u, v, cells_u, cells_v, seed):
    """Cubic value noise with integer lattice periods on both axes."""
    x = np.mod(u, DETAIL_PERIOD) * (cells_u / DETAIL_PERIOD)
    y = np.mod(v, DETAIL_PERIOD) * (cells_v / DETAIL_PERIOD)
    ix, iy = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = x - ix, y - iy
    fx, fy = fx * fx * (3.0 - 2.0 * fx), fy * fy * (3.0 - 2.0 * fy)
    x0, x1 = ix % cells_u, (ix + 1) % cells_u
    y0, y1 = iy % cells_v, (iy + 1) % cells_v
    a = _hash(x0, y0, seed) * (1.0 - fx) + _hash(x1, y0, seed) * fx
    b = _hash(x0, y1, seed) * (1.0 - fx) + _hash(x1, y1, seed) * fx
    return a * (1.0 - fy) + b * fy


def _fbm(u, v, seed):
    return (.56 * _noise(u, v, 4, 4, seed)
            + .29 * _noise(u, v, 8, 8, seed + 1)
            + .15 * _noise(u, v, 16, 16, seed + 2))


def _detail(family, u, v, region, craftsmanship):
    n = lambda a, b, seed: _noise(u, v, a, b, seed)
    prep = {"ROUGH": 1.45, "STANDARD": 1.0, "FINE": .45}[craftsmanship]
    if family == "wood":
        warp = .018 * n(2, 5, 11) + .007 * n(4, 13, 12)
        cross = np.mod(v + warp, DETAIL_PERIOD)
        broad = _noise(u, cross, 2, 11, 21)
        fine = _noise(u, cross, 8, 29, 22)
        grain = (.36 * np.sin(math.tau * (19.0 * cross / DETAIL_PERIOD + .7 * broad))
                 + .34 * broad + .18 * fine + .10 * _noise(u, v, 4, 7, 23))

        # Two elongated, safely interior knots per two-metre tile; their rings
        # disrupt longitudinal grain without turning it into narrow striping.
        knots = np.zeros_like(u)
        for ku, kv, seed in ((.55, .46, 31), (1.48, 1.54, 32)):
            du = (u - ku + DETAIL_PERIOD * .5) % DETAIL_PERIOD - DETAIL_PERIOD * .5
            dv = (v - kv + DETAIL_PERIOD * .5) % DETAIL_PERIOD - DETAIL_PERIOD * .5
            radius = np.sqrt((du / .13) ** 2 + (dv / .046) ** 2)
            envelope = np.clip(1.0 - radius / 3.2, 0.0, 1.0)
            rings = np.cos(math.tau * radius * 1.17 + .24 * n(7, 9, seed))
            knots += envelope * (.075 * rings - .05 * np.exp(-radius * radius * 1.8))
        scallop = np.sin(math.tau * (35.0 * cross / DETAIL_PERIOD
                                     + .06 * _noise(u, cross, 3, 7, 35)))
        height = (.00056 * grain + .00027 * knots + .00012 * prep * scallop)
        albedo = (1.0 + .25 * grain + .09 * knots + .012 * fine) * {"ROUGH":1.04,"STANDARD":1.,"FINE":.78}[craftsmanship]
        rough = {"ROUGH":.94,"STANDARD":.82,"FINE":.64}[craftsmanship] + .025 * np.abs(fine)
        metal = np.zeros_like(u)
    elif family == "stone":
        mineral = .54 * _fbm(u, v, 51) + .29 * n(13, 11, 52) + .17 * n(29, 23, 53)
        cleft = n(7, 5, 54)
        chips = np.maximum(0.0, n(41, 37, 55) - .47)
        height = (.0020 * mineral + .0004 * cleft + .0003 * chips) * prep
        albedo = 1.0 + .064 * mineral + .017 * cleft + .009 * chips
        rough = .84 + .08 * (1.0 - prep / 2.0) + .035 * np.abs(n(9, 7, 56))
        metal = np.zeros_like(u)
    elif family == "plaster":
        trowel = .52 * n(3, 2, 61) + .30 * n(7, 5, 62) + .18 * n(15, 11, 63)
        pits = np.maximum(0.0, n(37, 31, 64) - .52)
        height = (.00021 * trowel + .00011 * pits) * prep
        albedo = 1.0 + .045 * trowel - .018 * pits + .008 * n(23, 19, 65)
        rough = .86 + .07 * (1.0 - prep / 2.0) + .025 * np.abs(n(9, 7, 66))
        metal = np.zeros_like(u)
    elif family == "roof":
        mineral = _fbm(u, v, 71)
        if region == "LOWMARK":  # split boards and overlapping shingles
            course = np.sin(math.tau * 7.0 * v / DETAIL_PERIOD)
            seam = np.exp(-np.square(np.sin(math.pi * 7.0 * v / DETAIL_PERIOD) / .11))
            form = .24 * course - .16 * seam + .16 * n(5, 13, 72)
            amplitude = .00052
        elif region == "THORNFELL":  # fine cleft slate
            form = .38 * n(17, 5, 73) + .22 * n(29, 11, 74) + .15 * n(7, 3, 75)
            amplitude = .00037
        elif region == "MIRE":  # close bundled reed ridges
            warp = .34 * n(3, 7, 76)
            form = .32 * np.sin(math.tau * (44.0 * v / DETAIL_PERIOD + warp)) + .17 * n(7, 19, 77)
            amplitude = .00048
        else:  # hammered iron plates and periodic seams
            seam_u = np.exp(-np.square(np.sin(math.pi * 3.0 * u / DETAIL_PERIOD) / .08))
            seam_v = np.exp(-np.square(np.sin(math.pi * 4.0 * v / DETAIL_PERIOD) / .08))
            form = (.12 * np.sin(math.tau * 3.0 * u / DETAIL_PERIOD)
                    + .10 * np.sin(math.tau * 4.0 * v / DETAIL_PERIOD)
                    - .12 * (seam_u + seam_v))
            amplitude = .00043
        height = (amplitude * (.48 * mineral + form) + .00011 * n(31, 27, 78)) * prep
        albedo = 1.0 + .055 * (.55 * mineral + form) + .012 * n(23, 19, 79)
        rough = .82 + .09 * (1.0 - prep / 2.0) + .025 * np.abs(n(7, 9, 80))
        metal = np.full_like(u, .035 if region == "EMBERHOLT" else 0.0)
    elif family == "iron":
        hammer = .62 * _fbm(u, v, 81) + .25 * n(23, 19, 82)
        corrosion = np.maximum(0.0, _fbm(u, v, 83) - .38)
        height = (.00007 * hammer + .000035 * corrosion) * prep
        albedo = 1.0 - .035 * corrosion + .02 * hammer
        rough = .43 + .10 * prep + .055 * corrosion + .02 * np.abs(n(13, 11, 84))
        metal = .78 + .035 * n(7, 5, 85)
    elif family == "leather":
        grain = .62 * _fbm(u, v, 91) + .23 * n(19, 17, 92) + .15 * n(37, 31, 93)
        height = .000055 * grain * prep
        albedo = 1.0 + .055 * grain + .012 * n(23, 19, 94)
        rough = .76 + .09 * prep + .025 * np.abs(n(9, 11, 95))
        metal = np.zeros_like(u)
    else:  # charcoal
        ash = .65 * _fbm(u, v, 101) + .23 * n(25, 21, 102) + .12 * n(43, 37, 103)
        height = .00003 * ash * prep
        albedo = 1.0 + .045 * ash + .012 * n(23, 19, 104)
        rough = .90 + .06 * prep + .02 * np.abs(n(11, 9, 105))
        metal = np.zeros_like(u)

    return (np.clip(albedo, .45, 1.35), np.clip(height, -.002, .002),
            np.clip(rough, 0.0, 1.0), np.clip(metal, 0.0, 1.0))


def _validated_inputs(family, u, v, region, craftsmanship):
    family = str(family).lower()
    region, craftsmanship = str(region).upper(), str(craftsmanship).upper()
    if family not in _FAMILIES:
        raise ValueError(f"family must be one of {_FAMILIES}")
    if region not in _REGIONS:
        raise ValueError(f"region must be one of {_REGIONS}")
    if craftsmanship not in _CRAFT:
        raise ValueError(f"craftsmanship must be one of {_CRAFT}")
    u, v = np.broadcast_arrays(np.asarray(u, dtype=np.float64), np.asarray(v, dtype=np.float64))
    if not (np.all(np.isfinite(u)) and np.all(np.isfinite(v))):
        raise ValueError("coordinates must be finite")
    return family, np.mod(u, DETAIL_PERIOD), np.mod(v, DETAIL_PERIOD), region, craftsmanship


def sample_detail(family, u, v, *, region="LOWMARK", craftsmanship="STANDARD"):
    """Sample periodic detail at unbounded metric coordinates in metres.

    Returns flattened linear RGB albedo multipliers, relief in metres,
    roughness, and metallic arrays. ``u`` and ``v`` broadcast like NumPy inputs
    and the result repeats exactly every ``DETAIL_PERIOD`` metres on each axis.
    """
    family, u, v, region, craftsmanship = _validated_inputs(family, u, v, region, craftsmanship)
    albedo, height, roughness, metallic = _detail(family, u, v, region, craftsmanship)
    return {"albedo": np.repeat(albedo.reshape(-1, 1), 3, axis=1),
            "height": height.reshape(-1), "roughness": roughness.reshape(-1),
            "metallic": metallic.reshape(-1)}


def generate_normal_tile(family, region="LOWMARK", craftsmanship="STANDARD", resolution=256):
    """Bake a repeatable tangent-space normal tile from periodic metric height."""
    if isinstance(resolution, bool) or int(resolution) != resolution or resolution < 2:
        raise ValueError("resolution must be an integer of at least 2")
    resolution = int(resolution)
    axis = np.arange(resolution, dtype=np.float64) * (DETAIL_PERIOD / resolution)
    u, v = np.meshgrid(axis, axis)
    result = sample_detail(family, u, v, region=region, craftsmanship=craftsmanship)
    height = result["height"].reshape(resolution, resolution)
    step = DETAIL_PERIOD / resolution
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) / (2.0 * step)
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) / (2.0 * step)
    normal = np.stack((-dx, -dy, np.ones_like(height)), axis=-1)
    normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    tile = np.ones((resolution, resolution, 4), dtype=np.float32)
    tile[:, :, :3] = (normal * .5 + .5).astype(np.float32)
    return tile
