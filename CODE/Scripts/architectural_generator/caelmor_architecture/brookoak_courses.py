"""Roof cover registered to the approved Brookoak PBR export."""
import math

from .construction import bind
from .geometry import MeshBuffer, area, clip, stable_seed
from .roof import _valley_clearances


EXPOSURE = .30
REPEAT_U = 1.28
ALBEDO_SHA256 = '8095fab4a47043d0444d858d5ff229ff4e4022c3334192c43553b9b32f18f208'

# Dominant side-joint centres, measured from the 1024px albedo in PNG
# top-down order. V in Blender runs in the opposite direction. The material's
# small painted joint wander remains within the narrow physical transition.
JOINTS = (
    (0, 224, 419, 563, 731),
    (12, 227, 506, 758),
    (55, 188, 344, 487, 773, 892),
    (192, 538, 848, 1012),
    (83, 235, 395, 525, 804),
    (127, 304, 599, 719, 852, 1010),
    (172, 293, 445, 663, 971),
    (235, 457, 688),
)


def _field_frame(plan, patch):
    axis = 0 if abs(patch.plane[0]) > abs(patch.plane[1]) else 1
    direction = 1 if patch.plane[axis] > 0 else -1
    sign = direction if axis == 1 else -direction
    rect = plan.rects[patch.source]
    eave = rect[axis] - plan.settings.overhang if direction > 0 else rect[axis+2]+plan.settings.overhang
    step = EXPOSURE / math.hypot(1, patch.plane[axis])
    return axis, direction, sign, eave, step


def _between(poly, axis, low, high):
    a, b = (1, 0) if axis == 0 else (0, 1)
    return clip(clip(poly, a, b, -low, bounded=True), -a, -b, high, bounded=True)


def _regions(plan, patches, topology):
    points, _, edges = topology
    clearances = _valley_clearances(points, patches, edges)
    for index, patch in enumerate(patches):
        poly = patch.poly
        for plane in clearances[index]:
            poly = clip(poly, *plane, bounded=True)
        if poly and area(poly) > 1e-8:
            yield patch, poly, _field_frame(plan, patch)


def _course_segments(poly, frame):
    axis, direction, sign, eave, step = frame
    across = 1-axis
    t = [direction*(p[axis]-eave)/step for p in poly]
    us = [sign*p[across]/REPEAT_U for p in poly]
    for row in range(math.floor(min(t)+1e-7), math.ceil(max(t)-1e-7)):
        limits = sorted((eave+direction*row*step, eave+direction*(row+1)*step))
        band = _between(poly, axis, *limits)
        joints = JOINTS[-1-row % len(JOINTS)]
        starts = [(repeat + x/1024, repeat, k)
                  for repeat in range(math.floor(min(us))-1, math.ceil(max(us))+1)
                  for k, x in enumerate(joints)]
        spans = [(lo, hi, (row, repeat, k)) for (lo, repeat, k), (hi, _, _) in zip(starts,starts[1:])
                 if hi > min(us) and lo < max(us)]
        yield row, band, spans


def cover_buffers(plan, patches, topology, spec):
    """Replace selected painted cells with registered physical shingles."""
    field = MeshBuffer('Mapped roof field', 'roof', 'roof', topology='SURFACE', field_family='shingle')
    shingles = MeshBuffer('Dimensional Brookoak shingles', 'roof', 'roof', topology='SURFACE', field_family='shingle')
    bind(spec, field, shingles)
    regions = list(_regions(plan, patches, topology))
    keys = {}
    for patch, poly, frame in regions:
        axis, direction, sign, _, _ = frame
        for _, band, spans in _course_segments(poly, frame):
            for lo, hi, key in spans:
                limits = sorted((lo*sign*REPEAT_U, hi*sign*REPEAT_U))
                piece = _between(band, 1-axis, *limits)
                if area(piece) > 1e-8:
                    keys.setdefault((patch.source, axis, direction), set()).add(key)
    selected = {}
    for slope, cells in keys.items():
        # Interleave small spatial groups so even sparse detail reaches the
        # eaves, upper courses and both ends of each slope.
        groups = {}
        for row, repeat, index in cells:
            groups.setdefault((row//2,repeat), []).append((row,repeat,index))
        ranked = []
        for group, members in groups.items():
            members.sort(key=lambda key: (stable_seed(plan.settings.seed, f'{slope}:{key}'), key))
            offset = stable_seed(plan.settings.seed, f'{slope}:{group}') / 2**64
            ranked.extend(((i+offset)/len(members),key) for i,key in enumerate(members))
        selected[slope] = {key for _,key in sorted(ranked)[:round(len(ranked)*plan.cover_percent/100)]}
    plan.cover_units = sum(map(len, keys.values()))
    plan.modeled_units = sum(map(len, selected.values()))

    lips = {}
    for patch, poly, frame in regions:
        axis, direction, sign, eave, step = frame
        chosen = selected.get((patch.source, axis, direction), ())

        def uv(point):
            return sign*point[1-axis]/REPEAT_U, direction*(point[axis]-eave)/(step*len(JOINTS))

        def base(point):
            return (*point, patch.height(*point)+.016)

        def flat(piece):
            if area(piece) > 1e-8:
                field.mapped_face([base(p) for p in piece], [uv(p) for p in piece])

        if not chosen:
            flat(poly)
            continue
        for row, band, spans in _course_segments(poly, frame):
            if not any(key in chosen for _, _, key in spans):
                flat(band)
                continue

            def segment(lo, hi):
                return _between(band, 1-axis, *sorted((lo*sign*REPEAT_U, hi*sign*REPEAT_U)))

            start = spans[0][0]
            for lo, hi, key in spans:
                if key not in chosen:
                    continue
                flat(segment(start, lo))
                start = hi
                piece = segment(lo, hi)
                if area(piece) <= 1e-8:
                    continue
                def top(point):
                    # Raise the butt and taper to the shared plane at the head.
                    v = direction*(point[axis]-eave)/step-row
                    return (*point, base(point)[2]+.027*max(0.,min(1.,1-v)))

                shingles.mapped_face([top(p) for p in piece], [uv(p) for p in piece])
                for a, b in zip(piece,piece[1:]+piece[:1]):
                    if max(top(a)[2]-base(a)[2],top(b)[2]-base(b)[2]) < 1e-7:
                        continue
                    ua,va = uv(a)
                    ub,vb = uv(b)
                    # Short vertical faces sample inside the same painted board.
                    # Give the lip a nonzero UV area without crossing a course.
                    center_u = (lo+hi)/2
                    center_v = (row+.5)/len(JOINTS)
                    if abs(ua-ub) >= abs(va-vb):
                        delta = .003 if (va+vb)/2 < center_v else -.003
                        inset_a, inset_b = (ua,va+delta),(ub,vb+delta)
                    else:
                        delta = .003 if (ua+ub)/2 < center_u else -.003
                        inset_a, inset_b = (ua+delta,va),(ub+delta,vb)
                    ta,tb,ba,bb = top(a),top(b),base(a),base(b)
                    # Adjacent raised boards in the same course have the
                    # same section. Drop their coincident internal faces.
                    edge = tuple(sorted(tuple(round(c,7) for c in p) for p in (ta,tb)))
                    if edge in lips:
                        del lips[edge]
                    elif ta[2]-ba[2] < 1e-7:
                        lips[edge] = ([ta,bb,tb],[(ua,va),inset_b,(ub,vb)])
                    elif tb[2]-bb[2] < 1e-7:
                        lips[edge] = ([ta,ba,tb],[(ua,va),inset_a,(ub,vb)])
                    else:
                        lips[edge] = ([ta,ba,bb,tb],[(ua,va),inset_a,inset_b,(ub,vb)])
            flat(segment(start, spans[-1][1]))
    for vertices, uvs in lips.values():
        shingles.mapped_face(vertices, uvs)
    return field, shingles
