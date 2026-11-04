"""Small crafted architectural primitives built on :mod:`geometry`'s MeshBuffer."""
from itertools import product
import math

from .geometry import EPS, cross, dot, sub, unit


def beveled_box(buffer, center, size, bevel=.035):
    """Append a closed, planar edge-chamfered box, wholly inside its bounds.

    The bevel is the perpendicular distance from the original edges. It is
    clamped to 20% of the thinnest dimension to keep the central faces intact.
    """
    if len(center) != 3 or len(size) != 3 or min(size) <= 0:
        raise ValueError('Center and positive three-dimensional size are required')
    x, y, z = map(float, center)
    hx, hy, hz = (float(s) * .5 for s in size)
    b = min(max(0., float(bevel)), min(hx, hy, hz) * .4)
    if b <= EPS:
        buffer.box((x, y, z), (2*hx, 2*hy, 2*hz))
        return buffer

    halves = (hx, hy, hz)
    corner_vertices = {}
    vertices = []
    signs_set = tuple(product((-1., 1.), repeat=3))
    inset = b * math.sqrt(2)
    for signs in signs_set:
        for primary in range(3):
            local = [signs[a] * (halves[a] if a == primary else halves[a] - inset)
                     for a in range(3)]
            corner_vertices[(signs, primary)] = len(vertices)
            vertices.append((local[0]+x, local[1]+y, local[2]+z))

    def add_face(indices):
        points = [vertices[i] for i in indices]
        centroid = tuple(sum(p[a] for p in points) / len(points) for a in range(3))
        outward = sub(centroid, (x, y, z))
        normal = unit(outward)
        ref = (1., 0., 0.) if abs(normal[0]) < .8 else (0., 1., 0.)
        u = unit(cross(ref, normal))
        v = cross(normal, u)
        indices.sort(key=lambda i: math.atan2(dot(sub(vertices[i], centroid), v),
                                              dot(sub(vertices[i], centroid), u)))
        p0, p1, p2 = (vertices[indices[i]] for i in range(3))
        if dot(cross(sub(p1, p0), sub(p2, p0)), outward) < 0:
            indices.reverse()
        faces.append(tuple(indices))

    faces = []
    # Six original planes remain as central quads.
    for axis in range(3):
        for side in (-1., 1.):
            face = [corner_vertices[(signs, axis)] for signs in signs_set if signs[axis] == side]
            add_face(face)
    # Each original edge becomes a planar quad, with one inset coordinate.
    for primary_a in range(3):
        for primary_b in range(primary_a + 1, 3):
            third = 3 - primary_a - primary_b
            for sa, sb in product((-1., 1.), repeat=2):
                low = [0., 0., 0.]
                low[primary_a], low[primary_b], low[third] = sa, sb, -1.
                high = list(low)
                high[third] = 1.
                low, high = tuple(low), tuple(high)
                add_face([corner_vertices[(low, primary_a)], corner_vertices[(low, primary_b)],
                          corner_vertices[(high, primary_b)], corner_vertices[(high, primary_a)]])
    # Three bevel planes meet at each original corner to form its small triangle.
    for signs in signs_set:
        add_face([corner_vertices[(signs, axis)] for axis in range(3)])

    # Every face is wound against its outward centroid direction; retain a
    # volume check as a final guard against accidental winding changes.
    volume6 = 0.
    for face in faces:
        p0 = vertices[face[0]]
        for i in range(1, len(face)-1):
            volume6 += dot(p0, cross(vertices[face[i]], vertices[face[i+1]]))
    if volume6 < 0:
        faces = [tuple(reversed(face)) for face in faces]
    buffer.indexed(vertices, faces)
    return buffer


def _components(buffer):
    by_vertex = {}
    for fi, face in enumerate(buffer.faces):
        for vi in face:
            by_vertex.setdefault(vi, set()).add(fi)
    unseen = set(by_vertex)
    while unseen:
        seed = unseen.pop()
        verts, faces, stack = {seed}, set(), [seed]
        while stack:
            vi = stack.pop()
            for fi in by_vertex[vi]:
                if fi in faces:
                    continue
                faces.add(fi)
                for other in buffer.faces[fi]:
                    if other not in verts:
                        verts.add(other)
                        unseen.discard(other)
                        stack.append(other)
        yield verts, faces


def _box_component(buffer, verts, face_ids):
    if len(verts) != 8 or len(face_ids) != 6 or any(len(buffer.faces[i]) != 4 for i in face_ids):
        return None
    points = [buffer.vertices[i] for i in verts]
    lo = tuple(min(p[a] for p in points) for a in range(3))
    hi = tuple(max(p[a] for p in points) for a in range(3))
    if any(hi[a] - lo[a] <= EPS for a in range(3)):
        return None
    corners = {(lo[0] if sx < 0 else hi[0], lo[1] if sy < 0 else hi[1], lo[2] if sz < 0 else hi[2])
               for sx, sy, sz in product((-1, 1), repeat=3)}
    if len({tuple(round(v, 8) for v in p) for p in points}) != 8 or any(
            min(sum((p[a]-q[a])**2 for a in range(3)) for q in corners) > 1e-12 for p in points):
        return None
    # Require each face to be one of the six axis-aligned sides and the closed
    # box's usual two faces per axis.
    sides = set()
    for fi in face_ids:
        face = buffer.faces[fi]
        axis = next((a for a in range(3) if all(abs(buffer.vertices[i][a]-lo[a]) < 1e-7 or
                                                 abs(buffer.vertices[i][a]-hi[a]) < 1e-7 for i in face)
                     and len({round(buffer.vertices[i][a], 7) for i in face}) == 1), None)
        if axis is None:
            return None
        sides.add((axis, round(buffer.vertices[face[0]][axis], 7)))
    if len(sides) != 6:
        return None
    center = tuple((lo[a]+hi[a])*.5 for a in range(3))
    size = tuple(hi[a]-lo[a] for a in range(3))
    return center, size


def replace_box_components(buffer, bevel=.035, predicate=None):
    """Replace disconnected axis-aligned box components in-place.

    ``predicate(buffer, center, size)`` optionally selects boxes. Other mesh
    components, metadata, and face ordering are retained. Triangle surface
    skins are never considered boxes.
    """
    replacements = []
    for verts, face_ids in _components(buffer):
        box = _box_component(buffer, verts, face_ids)
        if box and (predicate is None or predicate(buffer, *box)):
            replacements.append((verts, face_ids, *box))
    if not replacements:
        return 0
    old_vertices, old_faces = buffer.vertices, buffer.faces
    new_vertices, new_faces = [], []
    replacement_map = {frozenset(verts): (center, size) for verts, _, center, size in replacements}
    # Components are disjoint by index, so process each original component and
    # preserve its local face topology unless it is a selected box.
    components = list(_components(buffer))
    for verts, face_ids in components:
        key = frozenset(verts)
        if key in replacement_map:
            temp = type(buffer)(name=buffer.name, material=buffer.material, layer=buffer.layer)
            beveled_box(temp, *replacement_map[key], bevel=bevel)
            offset = len(new_vertices)
            new_vertices.extend(temp.vertices)
            new_faces.extend(tuple(offset+i for i in f) for f in temp.faces)
        else:
            mapping = {}
            for vi in sorted(verts):
                mapping[vi] = len(new_vertices)
                new_vertices.append(old_vertices[vi])
            for fi in sorted(face_ids):
                new_faces.append(tuple(mapping[i] for i in old_faces[fi]))
    buffer.vertices, buffer.faces = new_vertices, new_faces
    return len(replacements)


def _open_box_component(buffer, verts, face_ids):
    """Return bounds and the capped axis/side for an axis-aligned open box."""
    if len(verts) != 8 or len(face_ids) != 5 or any(len(buffer.faces[i]) != 4 for i in face_ids):
        return None
    points = [buffer.vertices[i] for i in verts]
    lo = tuple(min(p[a] for p in points) for a in range(3))
    hi = tuple(max(p[a] for p in points) for a in range(3))
    if any(hi[a] - lo[a] <= EPS for a in range(3)):
        return None
    corners = {(lo[0] if sx < 0 else hi[0], lo[1] if sy < 0 else hi[1], lo[2] if sz < 0 else hi[2])
               for sx, sy, sz in product((-1, 1), repeat=3)}
    if len({tuple(round(v, 8) for v in p) for p in points}) != 8 or any(
            min(sum((p[a]-q[a])**2 for a in range(3)) for q in corners) > 1e-12 for p in points):
        return None
    sides = set()
    for fi in face_ids:
        face = buffer.faces[fi]
        side = next(((axis, round(buffer.vertices[face[0]][axis], 7)) for axis in range(3)
                     if len({round(buffer.vertices[i][axis], 7) for i in face}) == 1 and
                     all(abs(buffer.vertices[i][axis]-lo[axis]) < 1e-7 or
                         abs(buffer.vertices[i][axis]-hi[axis]) < 1e-7 for i in face)), None)
        if side is None:
            return None
        sides.add(side)
    if len(sides) != 5:
        return None
    counts = [sum(axis == a for axis, _ in sides) for a in range(3)]
    if sorted(counts) != [1, 2, 2]:
        return None
    front_axis = counts.index(1)
    front_side = next(side for axis, side in sides if axis == front_axis)
    front_coord = lo[front_axis] if abs(front_side-lo[front_axis]) < 1e-7 else hi[front_axis]
    return lo, hi, front_axis, front_coord


def bevel_open_box_front(buffer, inset=.025, depth=.012, predicate=None):
    """Bevel the capped front of disconnected five-quad open-back boxes.

    The back remains open. ``predicate(buffer, center, size)`` can select
    components; all other geometry and buffer metadata are retained.
    """
    replacements = []
    for verts, face_ids in _components(buffer):
        box = _open_box_component(buffer, verts, face_ids)
        if box is None:
            continue
        lo, hi, front_axis, front_coord = box
        center = tuple((lo[a]+hi[a])*.5 for a in range(3))
        size = tuple(hi[a]-lo[a] for a in range(3))
        if predicate is None or predicate(buffer, center, size):
            replacements.append((verts, face_ids, lo, hi, front_axis, front_coord))
    if not replacements:
        return 0

    old_vertices, old_faces = buffer.vertices, buffer.faces
    components = list(_components(buffer))
    replacement_map = {frozenset(verts): (lo, hi, front_axis, front_coord)
                       for verts, _, lo, hi, front_axis, front_coord in replacements}
    new_vertices, new_faces = [], []
    for verts, face_ids in components:
        key = frozenset(verts)
        if key not in replacement_map:
            mapping = {}
            for vi in sorted(verts):
                mapping[vi] = len(new_vertices)
                new_vertices.append(old_vertices[vi])
            for fi in sorted(face_ids):
                new_faces.append(tuple(mapping[i] for i in old_faces[fi]))
            continue

        lo, hi, front_axis, front_coord = replacement_map[key]
        in_axes = [a for a in range(3) if a != front_axis]
        front_sign = 1. if abs(front_coord-hi[front_axis]) < 1e-7 else -1.
        thickness = hi[front_axis]-lo[front_axis]
        inset_amount = max(0., min(float(inset), (hi[in_axes[0]]-lo[in_axes[0]])*.16,
                                   (hi[in_axes[1]]-lo[in_axes[1]])*.16))
        depth_amount = max(0., min(float(depth), thickness*.45))
        recessed_front = front_coord-front_sign*depth_amount
        base = len(new_vertices)

        # Four central points lie on the original front plane. Four outer
        # points are inset in depth, then four back points preserve the opening.
        for inset_point in (True, False):
            for s0, s1 in product((-1., 1.), repeat=2):
                point = [0., 0., 0.]
                point[front_axis] = front_coord if inset_point else recessed_front
                point[in_axes[0]] = ((lo[in_axes[0]]+hi[in_axes[0]])*.5 +
                                     s0*((hi[in_axes[0]]-lo[in_axes[0]])*.5 - (inset_amount if inset_point else 0.)))
                point[in_axes[1]] = ((lo[in_axes[1]]+hi[in_axes[1]])*.5 +
                                     s1*((hi[in_axes[1]]-lo[in_axes[1]])*.5 - (inset_amount if inset_point else 0.)))
                new_vertices.append(tuple(point))
        for s0, s1 in product((-1., 1.), repeat=2):
            point = [0., 0., 0.]
            point[front_axis] = lo[front_axis] if front_sign > 0 else hi[front_axis]
            point[in_axes[0]] = hi[in_axes[0]] if s0 > 0 else lo[in_axes[0]]
            point[in_axes[1]] = hi[in_axes[1]] if s1 > 0 else lo[in_axes[1]]
            new_vertices.append(tuple(point))

        def emit(ids):
            points = [new_vertices[i] for i in ids]
            centroid = tuple(sum(p[a] for p in points)/len(points) for a in range(3))
            outward = list(centroid[a]-((lo[a]+hi[a])*.5) for a in range(3))
            normal = unit(tuple(outward))
            ref = (1., 0., 0.) if abs(normal[0]) < .8 else (0., 1., 0.)
            u = unit(cross(ref, normal))
            v = cross(normal, u)
            ids = sorted(ids, key=lambda i: math.atan2(dot(sub(new_vertices[i], centroid), v),
                                                        dot(sub(new_vertices[i], centroid), u)))
            p0, p1, p2 = (new_vertices[ids[i]] for i in range(3))
            if dot(cross(sub(p1, p0), sub(p2, p0)), outward) < 0:
                ids.reverse()
            new_faces.append(tuple(ids))

        # Inset front, four sloped bevels, and four short side returns.
        emit([base+i for i in range(4)])
        corner_index = {(s0, s1): i for i, (s0, s1) in enumerate(product((-1., 1.), repeat=2))}
        for varying_axis in range(2):
            for fixed_sign in (-1., 1.):
                start = (-1., fixed_sign) if varying_axis == 0 else (fixed_sign, -1.)
                end = (1., fixed_sign) if varying_axis == 0 else (fixed_sign, 1.)
                i, j = corner_index[start], corner_index[end]
                emit([base+i, base+j, base+4+j, base+4+i])
                emit([base+4+i, base+4+j, base+8+j, base+8+i])
    buffer.vertices, buffer.faces = new_vertices, new_faces
    return len(replacements)
