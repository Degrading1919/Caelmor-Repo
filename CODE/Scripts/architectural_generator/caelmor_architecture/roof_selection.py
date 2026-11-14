"""Infer a rectangular or two-volume roof bearing from wall-core meshes.

Coordinates and dimensions are in Blender world units (the add-on uses metres).
Only evaluated geometry is read; the input objects are never changed.
"""
from dataclasses import dataclass
import math
import statistics

from .model import rectangle_union_outline


@dataclass(frozen=True)
class Bearing:
    center: tuple
    width: float
    depth: float
    angle: float
    rects: tuple = ()


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


def _compound(segments, tolerance):
    """Match observed wall spans to the exterior of two connected rectangles."""
    def levels(axis):
        clusters = []
        for pos in sorted(s[1] for s in segments if s[0] == axis):
            if not clusters or pos-clusters[-1][0] > tolerance:
                clusters.append([])
            clusters[-1].append(pos)
        return [statistics.median(c) for c in clusters]

    xs, ys = levels('y'), levels('x')
    if not (2 <= len(xs) <= 4 and 2 <= len(ys) <= 4):
        return None
    from itertools import combinations
    choices = [(x0,y0,x1,y1) for x0,x1 in combinations(xs,2) for y0,y1 in combinations(ys,2)
               if min(x1-x0,y1-y0)>=1]

    def matches(outline):
        assigned = set()
        for a,b in zip(outline,outline[1:]+outline[:1]):
            axis = 0 if abs(a[1]-b[1])<1e-7 else 1
            lo,hi = sorted((a[axis],b[axis]))
            limit = min(.25, max(tolerance, .12))
            spans = sorted((start,end,i) for i,(kind,pos,start,end,_) in enumerate(segments)
                           if kind==('x' if axis==0 else 'y') and abs(pos-a[1-axis])<=tolerance
                           and start>=lo-limit and end<=hi+limit)
            covered = lo
            for start,end,i in spans:
                if start>covered+limit:
                    return False
                covered=max(covered,end)
                assigned.add(i)
            if not spans or covered<hi-limit:
                return False
        return len(assigned)==len(segments)

    good = []
    for a,b in combinations(choices,2):
        dx=min(a[2],b[2])-max(a[0],b[0])
        dy=min(a[3],b[3])-max(a[1],b[1])
        if min(dx,dy)<-1e-7 or max(dx,dy)<=tolerance:
            continue
        main,wing=sorted((a,b),key=lambda r:(-(r[2]-r[0])*(r[3]-r[1]),r))
        # The shared backend needs overlapping support domains. When the
        # observed rectangles touch, extend the wing inward to the main ridge.
        width,depth=main[2]-main[0],main[3]-main[1]
        axis='X' if width>=depth else 'Y'
        rects=[(*main,axis),(*wing,'Y' if axis=='X' else 'X')]
        outline=rectangle_union_outline(rects)
        if len(outline) not in (6,8) or not matches(outline):
            continue
        wing=list(wing)
        if axis=='X':
            center=(main[1]+main[3])/2
            if wing[1]<main[1] and wing[3]<=main[3]:
                wing[3]=max(wing[3],center)
            elif wing[3]>main[3] and wing[1]>=main[1]:
                wing[1]=min(wing[1],center)
            else:
                continue
            if wing[0]<main[0] or wing[2]>main[2] or wing[2]-wing[0]>depth+1e-7:
                continue
        else:
            center=(main[0]+main[2])/2
            if wing[0]<main[0] and wing[2]<=main[2]:
                wing[2]=max(wing[2],center)
            elif wing[2]>main[2] and wing[0]>=main[0]:
                wing[0]=min(wing[0],center)
            else:
                continue
            if wing[1]<main[1] or wing[3]>main[3] or wing[3]-wing[1]>width+1e-7:
                continue
        good.append([rects[0],(*wing,rects[1][4])])
    if good:
        return min(good,key=lambda r:(-(r[0][2]-r[0][0])*(r[0][3]-r[0][1]),r))
    return None


def infer_bearing(objects, depsgraph=None):
    """Return a rectangular Bearing or raise ValueError for ambiguous selection.

    Thin trim and glazing are filtered by evaluated dimensions. The selected
    cores must enclose one level rectangle or a supported orthogonal wing.
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
            cores.append((points, length, thickness, angle, bottom, top, obj.name))
    if len(cores) < 4:
        raise ValueError('Select wall-core meshes on all four sides of a rectangular building.')
    def offset(a,b):
        return (a-b+math.pi/4) % (math.pi/2)-math.pi/4

    angle=max((core[3] for core in cores),key=lambda a:sum(
        c[1] for c in cores if abs(offset(c[3],a)) <= math.radians(4)))
    outliers=sorted((c[6], math.degrees(abs(offset(c[3],angle)))) for c in cores
                    if abs(offset(c[3],angle)) > math.radians(4))
    if outliers:
        names=', '.join(f'{name} ({deviation:.0f}°)' for name,deviation in outliers[:6])
        raise ValueError(f'Non-orthogonal wall cores: {names}. Deselect non-wall geometry; diagonal walls need a different roof workflow.')
    angle=(angle+math.pi/4)%(math.pi/2)-math.pi/4
    angle+=sum(c[1]*offset(c[3],angle) for c in cores)/sum(c[1] for c in cores)
    c, s = math.cos(angle), math.sin(angle)
    tops = [core[5] for core in cores]
    bottoms = [core[4] for core in cores]
    tolerance_z = 0.12
    if max(tops)-min(tops) > tolerance_z or max(bottoms)-min(bottoms) > tolerance_z:
        names=', '.join(sorted(c[6] for c in cores if abs(c[5]-statistics.median(tops)) > tolerance_z/2
                               or abs(c[4]-statistics.median(bottoms)) > tolerance_z/2)[:6])
        raise ValueError(f'Uneven wall bearing: {names}. Select wall cores at one elevation.')
    segments = []
    for points, length, thickness, a, _, _, name in cores:
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
    if any(min(abs(pos-axis_min),abs(pos-axis_max))>side_tolerance
           for axis,pos, *_ in segments
           for axis_min,axis_max in [(ymin,ymax) if axis=='x' else (xmin,xmax)]):
        compound = _compound(segments, side_tolerance)
        if compound is None:
            raise ValueError('Orthogonal footprint could not resolve to a main rectangle and one perpendicular wing. Check interior walls and gaps.')
        x,y=(xmin+xmax)/2,(ymin+ymax)/2
        rects=tuple((a-x,b-y,d-x,e-y,axis) for a,b,d,e,axis in compound)
        return Bearing((x*c-y*s,x*s+y*c,statistics.median(tops)),width,depth,angle,rects)
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
