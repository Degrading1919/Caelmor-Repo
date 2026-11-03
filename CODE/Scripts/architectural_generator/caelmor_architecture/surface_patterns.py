"""Vectorized, metric-scale procedural microtextures for Caelmor materials.

Coordinates are arbitrary metric surface coordinates; the sampler does not tile
or wrap them. Wood's long axis is ``u``. Returned albedo is a linear RGB
multiplier intended to be applied to a regional palette downstream.
"""
from __future__ import annotations

import numpy as np


_REGIONS = ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")


def _hash(ix, iy, seed):
    """Stable 32-bit lattice hash with array inputs."""
    mask = np.int64(0xFFFFFFFF)
    n = (ix.astype(np.int64) * 374761393 + iy.astype(np.int64) * 668265263 + int(seed) * 1442695041) & mask
    n = ((n ^ (n >> 13)) * 1274126177) & mask
    n ^= n >> 16
    return n.astype(np.float64) / 2147483647.5 - 1.0


def _noise(u, v, scale_u, scale_v, seed):
    """Cubic-interpolated value noise; continuous over unbounded coordinates."""
    x, y = u * scale_u, v * scale_v
    ix, iy = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = x - ix, y - iy
    fx, fy = fx * fx * (3.0 - 2.0 * fx), fy * fy * (3.0 - 2.0 * fy)
    a = _hash(ix, iy, seed) * (1-fx) + _hash(ix+1, iy, seed) * fx
    b = _hash(ix, iy+1, seed) * (1-fx) + _hash(ix+1, iy+1, seed) * fx
    return a * (1-fy) + b * fy


def _fbm(u, v, seed):
    return (.55*_noise(u,v,2.3,2.3,seed) + .30*_noise(u,v,6.1,6.1,seed+1)
            + .15*_noise(u,v,16.7,16.7,seed+2))


def _clip(x, low, high):
    return np.clip(x, low, high)


def _pattern(family, u, v, region, wealth, craft, seed):
    n = lambda su, sv, offset=0: _noise(u, v, su, sv, seed + offset)
    fine = n(31.0, 31.0, 1)
    relief_scale = {"ROUGH": 1.7, "STANDARD": 1.0, "FINE": .40}[craft]
    grade = {"MODEST": 1.18, "ESTABLISHED": 1.0, "AFFLUENT": .78}[wealth]

    if family == "wood":
        # Fibres run with u; narrow ridges therefore vary chiefly across v.
        warp = .018*n(1.3, 5.0, 3) + .006*n(3.4, 13.0, 4)
        cross = v + warp
        broad = _noise(u, cross, 1.8, 10.5, seed+5)
        fibre = np.sin(2*np.pi*(cross*23.0 + .65*broad))
        grain = .22*fibre + .34*_noise(u,cross,.9,19.0,seed+6) + .24*broad
        # A few deterministic elongated knots and checks, localized in metric space.
        cell_u = np.floor(u/.9).astype(np.int64)
        cell_v = np.floor(v/.14).astype(np.int64)
        knot_cutoff = {"MODEST": -.50, "ESTABLISHED": -.20, "AFFLUENT": .25}[wealth]
        present = _hash(cell_u,cell_v,seed+10) > knot_cutoff
        du = u - (cell_u*.9 + .1 + (_hash(cell_u,cell_v,seed+11)+1)*.35)
        dv = v - (cell_v*.14 + .07 + .025*_hash(cell_u,cell_v,seed+12))
        radius = np.sqrt((du/.065)**2 + (dv/.018)**2)
        envelope = _clip(1-radius/3.0, 0, 1) * present
        rings = np.cos(2*np.pi*radius*1.12 + .25*n(9,13,13))
        knots = envelope*(.055*rings - .045*np.exp(-radius*radius*1.8))*grade
        check = _clip(1-np.abs(dv - .0015*np.sin(du*95))/.00065, 0, 1)
        knots -= check*envelope*.035*grade*(np.abs(du)<.07)
        # Hand work leaves broad, shallow longitudinal scallops. Their spacing
        # crosses the grain; their depth drifts along u over roughly 10-25 cm.
        tool_drift = .65 + .35*_noise(u,cross,6.2,3.1,seed+14)
        scallops = np.sin(2*np.pi*(cross/.057 + .055*n(2.3,4.7,15))) * tool_drift
        prep_amp = {"ROUGH": .00078, "STANDARD": .00030, "FINE": .000075}[craft]
        prep = prep_amp * scallops
        height = (grain + knots) * .00072 * relief_scale + prep
        color = 1 + .17*grain*grade + .026*fine + grade*envelope*(-.085 + .035*rings)
        # A prepared, burnished/oil-finished face has a deeper heartwood tone;
        # dry split stock remains pale. This is a workmanship finish, not a
        # cleanliness assumption: the separate condition pass still ages it.
        color *= {"ROUGH":1.04,"STANDARD":1.0,"FINE":.78}[craft]
        rough = {"ROUGH":.94,"STANDARD":.82,"FINE":.64}[craft] + .025*n(4,8,12) + .012*np.abs(fine)
        metallic = np.zeros_like(u)
    elif family == "stone":
        granular = .46*_fbm(u,v,seed+20) + .25*n(17,19,21) + .14*n(43,39,22)
        chips = np.maximum(0, n(71,67,23)-.42)
        height = (.0020*granular + .0008*chips) * relief_scale
        color = 1 + .075*granular*grade + .014*fine
        rough = {"ROUGH":.95,"STANDARD":.88,"FINE":.76}[craft] + .04*np.abs(n(8,9,24))
        metallic = np.zeros_like(u)
    elif family == "plaster":
        trowel = _noise(u,v,1.4,1.0,seed+30)*.45 + _noise(u,v,3.5,2.8,seed+31)*.24
        pits = np.maximum(0, n(53,47,32)-.50)
        height = (.00019*trowel + .00012*pits) * relief_scale
        color = 1 + .042*trowel*grade - .020*pits + .009*fine
        rough = .86 + .075*relief_scale + .025*np.abs(n(9,8,33))
        metallic = np.zeros_like(u)
    elif family == "roof":
        # Shared material detail remains subtle; each region has a distinct
        # characteristic scale/form that layers over its palette.
        mineral = _fbm(u,v,seed+40)
        if region == "LOWMARK":  # split boards / overlapping shingles
            seams = np.exp(-np.square((v - .30*np.floor(v/.30))/.006))
            form = .22*np.sin(2*np.pi*v/0.30) - .18*seams + .10*n(3,8,41)
            amp = .00030
        elif region == "THORNFELL":  # fine cleft slate
            form = .16*n(17,2.8,42) + .10*n(25,7,43)
            amp = .00020
        elif region == "MIRE":  # bundled reed ridges
            form = .28*np.sin(2*np.pi*v/.045 + .5*n(2,8,44)) + .10*n(4,20,45)
            amp = .00034
        else:  # EMBERHOLT hammered iron roof plates
            seam_u = np.exp(-np.square((u - .6*np.floor(u/.6))/.004))
            seam_v = np.exp(-np.square((v - .45*np.floor(v/.45))/.004))
            form = .12*np.sin(2*np.pi*u/.6) + .10*np.sin(2*np.pi*v/.45) - .12*(seam_u+seam_v)
            amp = .00027
        height = (amp*(.45*mineral + form) + .00010*n(38,34,47)) * relief_scale
        color = 1 + .055*(.55*mineral + form)*grade + .012*fine
        rough = .84 + .075*relief_scale + .025*np.abs(n(7,8,48))
        metallic = np.full_like(u, .035) if region == "EMBERHOLT" else np.zeros_like(u)
    elif family == "iron":
        hammered = _fbm(u,v,seed+50)*.45 + .22*n(28,26,51)
        corrosion = np.maximum(0, _fbm(u,v,seed+52)-.38)
        height = (.000055*hammered + .000025*corrosion)*relief_scale
        color = 1 - .035*corrosion + .018*hammered
        rough = .43 + .10*relief_scale + .06*corrosion + .025*np.abs(fine)
        metallic = .78 + .035*n(6,7,53)
    elif family == "leather":
        grain = .44*_fbm(u,v,seed+60) + .20*n(24,29,61) + .12*n(51,47,62)
        height = .000045*grain*relief_scale
        color = 1 + .065*grain*grade + .014*fine
        rough = .76 + .09*relief_scale + .025*np.abs(n(9,11,63))
        metallic = np.zeros_like(u)
    elif family == "charcoal":
        ash = _fbm(u,v,seed+70)*.42 + .22*n(30,28,71)
        height = .000025*ash*relief_scale
        color = 1 + .045*ash + .012*fine
        rough = .91 + .055*relief_scale + .02*np.abs(fine)
        metallic = np.zeros_like(u)
    else:
        raise ValueError(f"unknown material family: {family!r}")
    return color, height, rough, metallic


def sample_pattern(family, u, v, *, region="LOWMARK", wealth="ESTABLISHED",
                   craftsmanship="STANDARD", seed=0):
    """Sample one original microtexture at metric ``(u, v)`` coordinates.

    Returns flattened N samples: linear RGB albedo multipliers, height in metres,
    roughness and metallic. Inputs may have any equal shape, including scalar.
    """
    family = str(family).lower()
    region, wealth, craftsmanship = str(region).upper(), str(wealth).upper(), str(craftsmanship).upper()
    if region not in _REGIONS:
        raise ValueError(f"region must be one of {_REGIONS}")
    if wealth not in ("MODEST", "ESTABLISHED", "AFFLUENT"):
        raise ValueError("wealth must be MODEST, ESTABLISHED, or AFFLUENT")
    if craftsmanship not in ("ROUGH", "STANDARD", "FINE"):
        raise ValueError("craftsmanship must be ROUGH, STANDARD, or FINE")
    u, v = np.broadcast_arrays(np.asarray(u,dtype=np.float64), np.asarray(v,dtype=np.float64))
    if not (np.all(np.isfinite(u)) and np.all(np.isfinite(v))):
        raise ValueError("coordinates must be finite")
    color, height, rough, metallic = _pattern(family,u,v,region,wealth,craftsmanship,int(seed))
    return {"albedo": np.repeat(_clip(color,.45,1.35).reshape(-1,1),3,axis=1),
            "height": np.clip(height,-.002,.002).reshape(-1),
            "roughness": _clip(rough,0,1).reshape(-1),
            "metallic": _clip(metallic,0,1).reshape(-1)}
