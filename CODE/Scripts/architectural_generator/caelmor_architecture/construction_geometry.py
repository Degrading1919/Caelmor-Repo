"""Geometry shared by construction builders. Dimensions are in metres."""
import math
from .geometry import area, clip, cross, lerp, sub, unit
from .curve_sweep import sweep_member


def board_strips(buffer, polygon, axis, height, thickness, width=.26):
    """Closed boards clipped to a support polygon, with tightly fitted seams."""
    low = min(p[axis] for p in polygon)
    high = max(p[axis] for p in polygon)
    count = max(1, math.ceil((high-low)/width))
    spacing = (high-low)/count
    a, b = (1, 0) if axis == 0 else (0, 1)
    for index in range(count):
        start = low + index*spacing
        end = start + spacing
        seam = min(.003, spacing*.08)
        board = clip(clip(polygon, a, b, -start-(seam if index else 0), bounded=True),
                     -a, -b, end-(seam if index+1 < count else 0), bounded=True)
        if abs(area(board)) > 1e-6:
            buffer.extrude([(x, y, height(x, y)) for x, y in board], (0, 0, -thickness))


def stone_face(lo, hi, bottom, top, arris):
    """Ease the corners of a bedded block without disturbing its straight beds."""
    cut = min(arris, (hi-lo)*.18, (top-bottom)*.18)
    return [(lo+cut,bottom),(hi-cut,bottom),(hi,bottom+cut),(hi,top-cut),
            (hi-cut,top),(lo+cut,top),(lo,top-cut),(lo,bottom+cut)]

def hewn_member(buffer, start, end, width, depth, workmanship, rng):
    """Work a long member inside its designed bearing section and envelope."""
    axis = unit(sub(end,start))
    ref = (0,1,0) if abs(axis[2])>.95 else (0,0,1)
    side = unit(cross(axis,ref))
    fraction = rng.uniform(.39,.64)
    cut = workmanship*rng.uniform(.10,.16)
    middle = lerp(start,end,fraction)
    widths = (width, width*(1-cut), width)
    depths = (depth, depth*(1-cut*.65), depth)
    sweep_member(buffer,(start,middle,end),side,widths,depths,
                 chamfer=workmanship*rng.uniform(.09,.16))
