"""Infer a rectangular roof bearing from selected wall-core meshes.

Coordinates and dimensions are in Blender world units (the add-on uses metres).
Only evaluated geometry is read; the input objects are never changed.
"""
from dataclasses import dataclass
import math
import statistics


@dataclass(frozen=True)
class Bearing:
    center: tuple
    width: float
    depth: float
    angle: float


def _hull(points):
    points = sorted(set(points))
    if len(points) < 3:
        return points
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _rectangle(points):
    hull = _hull([(p[0], p[1]) for p in points])
    if len(hull) < 3:
        return None
    best = None
    for i, p in enumerate(hull):
        q = hull[(i+1) % len(hull)]
        angle = math.atan2(q[1]-p[1], q[0]-p[0])
        c, s = math.cos(angle), math.sin(angle)
        xs = [x*c+y*s for x, y in hull]
        ys = [-x*s+y*c for x, y in hull]
        a, b = max(xs)-min(xs), max(ys)-min(ys)
        area = a*b
        if best is None or area < best[0]:
            best = (area, a, b, angle)
    _, a, b, angle = best
    if b > a:
        a, b, angle = b, a, angle+math.pi/2
    return a, b, angle


def infer_bearing(objects, depsgraph=None):
    """Return a rectangular Bearing or raise ValueError for ambiguous selection.

    Wall cores must form four contiguous, level, perpendicular sides. Thin trim
    and glazing are ignored using their evaluated dimensions, not object names.
    This intentionally rejects partitions, wings, gaps, and stepped wall tops.
    """
    if depsgraph is None:
        import bpy
        depsgraph = bpy.context.evaluated_depsgraph_get()
    cores = []
    for obj in objects:
        if obj.type != 'MESH':
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        if mesh is None:
            continue
        try:
            matrix = evaluated.matrix_world
            points = [tuple(matrix @ vertex.co) for vertex in mesh.vertices]
        finally:
            evaluated.to_mesh_clear()
        if len(points) < 4 or not all(math.isfinite(v) for p in points for v in p):
            continue
        rect = _rectangle(points)
        if rect is None:
            continue
        length, thickness, angle = rect
        bottom, top = min(p[2] for p in points), max(p[2] for p in points)
        height = top-bottom
        if height >= 1.0 and length >= 0.4 and length >= 2.3*max(thickness, 0.001) and height >= 2*thickness:
            cores.append((points, length, thickness, angle, bottom, top))
    if len(cores) < 4:
        raise ValueError('Select wall-core meshes on all four sides of a rectangular building.')
    # Fourfold circular average treats perpendicular sides as the same orientation.
    cx = sum(length*math.cos(4*angle) for _, length, _, angle, _, _ in cores)
    cy = sum(length*math.sin(4*angle) for _, length, _, angle, _, _ in cores)
    if math.hypot(cx, cy) < 0.8*sum(core[1] for core in cores):
        raise ValueError('Selected wall cores are not aligned to two perpendicular directions.')
    angle = math.atan2(cy, cx)/4
    c, s = math.cos(angle), math.sin(angle)
    tops = [core[5] for core in cores]
    bottoms = [core[4] for core in cores]
    tolerance_z = 0.12
    if max(tops)-min(tops) > tolerance_z or max(bottoms)-min(bottoms) > tolerance_z:
        raise ValueError('Selected wall cores have mismatched top or bottom heights.')
    segments = []
    for points, length, thickness, a, _, _ in cores:
        error = abs((a-angle+math.pi/4) % (math.pi/2)-math.pi/4)
        if error > math.radians(4):
            raise ValueError('Selected wall cores are not aligned to two perpendicular directions.')
        xs = [p[0]*c+p[1]*s for p in points]
        ys = [-p[0]*s+p[1]*c for p in points]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x1-x0 > y1-y0:
            segments.append(('x', (y0+y1)/2, x0, x1, thickness))
        else:
            segments.append(('y', (x0+x1)/2, y0, y1, thickness))
    xwalls = [v for v in segments if v[0] == 'x']
    ywalls = [v for v in segments if v[0] == 'y']
    if len(xwalls) < 2 or len(ywalls) < 2:
        raise ValueError('Select wall cores on all four sides of the building.')
    xmin, xmax = min(v[1] for v in ywalls), max(v[1] for v in ywalls)
    ymin, ymax = min(v[1] for v in xwalls), max(v[1] for v in xwalls)
    width, depth = xmax-xmin, ymax-ymin
    if min(width, depth) < 0.5:
        raise ValueError('The selected wall footprint is too small or incomplete.')
    side_tolerance = max(0.08, min(0.2, statistics.median(v[4] for v in segments)*0.75))
    sides = [[], [], [], []]
    for axis, position, start, end, thick in segments:
        ends = (ymin, ymax) if axis == 'x' else (xmin, xmax)
        index = (0 if axis == 'x' else 2) + (0 if abs(position-ends[0]) <= abs(position-ends[1]) else 1)
        if abs(position-ends[index % 2]) > side_tolerance:
            raise ValueError('Selected walls include a misaligned side or internal partition.')
        sides[index].append((start, end, thick))
    for index, side in enumerate(sides):
        if not side:
            raise ValueError('The selected walls do not enclose all four sides.')
        lo, hi = (xmin, xmax) if index < 2 else (ymin, ymax)
        side.sort()
        gap_tolerance = max(0.08, min(0.25, max(v[2] for v in side)*1.5))
        if side[0][0] > lo+gap_tolerance or max(v[1] for v in side) < hi-gap_tolerance:
            raise ValueError('The selected walls leave an open corner.')
        end = side[0][1]
        for start, stop, _ in side[1:]:
            if start > end+gap_tolerance:
                raise ValueError('The selected walls contain a gap along a side.')
            end = max(end, stop)
        if side[0][0] < lo-gap_tolerance or end > hi+gap_tolerance:
            raise ValueError('The selected walls extend beyond the rectangular footprint.')
    x, y = (xmin+xmax)/2, (ymin+ymax)/2
    return Bearing((x*c-y*s, x*s+y*c, statistics.median(tops)), width, depth, angle)
