"""Native modifier experiment for the mapped construction fields."""
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
import math

import bpy
from mathutils import Vector
import numpy as np

from caelmor_architecture.geometry import area, clip

FIELD_UV = 'UV2_Surface'
GRID = .10
BORDER = .12
MAX_TRIANGLES = 300_000


def _edges(points):
    return zip(points, points[1:] + points[:1])


def _line(a, b):
    u = (b - a).normalized()
    if u.x < -1e-5 or (abs(u.x) <= 1e-5 and u.y < 0):
        u = -u
    return (round(u.x, 4), round(u.y, 4), round(u.cross(a), 4)), u


def _conform(polygons):
    """Split collinear T junctions before welding a chart's clipped cells."""
    segments = defaultdict(dict)
    for points in polygons:
        for a, b in _edges(points):
            key, _ = _line(a, b)
            for point in (a, b):
                segments[key][tuple(round(c, 5) for c in point)] = point
    ordered = {}
    for key, points in segments.items():
        axis = Vector(key[:2])
        samples = sorted((axis.dot(p), i, p) for i, p in enumerate(points.values()))
        ordered[key] = [r[0] for r in samples], [r[2] for r in samples]
    for points in polygons:
        result = []
        for a, b in _edges(points):
            key, _ = _line(a, b)
            axis = Vector(key[:2])
            start, end = axis.dot(a), axis.dot(b)
            distances, positions = ordered[key]
            cut = positions[bisect_right(distances, min(start, end) + 1e-5):
                            bisect_left(distances, max(start, end) - 1e-5)]
            result.extend([a, *(cut if start < end else reversed(cut))])
        yield result


def _chart_key(mesh, face):
    normal = face.normal
    origin = mesh.vertices[face.vertices[0]].co
    return tuple(round(x, 4) for x in (*normal, normal.dot(origin)))


def _chart_cells(mesh, faces):
    normal = faces[0].normal
    axis = Vector((0, 0, 1)) if abs(normal.z) < .9 else Vector((0, 1, 0))
    u = axis.cross(normal).normalized()
    v = normal.cross(u)
    depth = normal.dot(mesh.vertices[faces[0].vertices[0]].co)
    cells = []
    for face in faces:
        outline = []
        for vertex in face.vertices:
            co = mesh.vertices[vertex].co
            outline.append((u.dot(co), v.dot(co)))
        origin = Vector(outline[0])
        index = max(range(2, len(outline)),
                    key=lambda j: abs((Vector(outline[1]) - origin).cross(Vector(outline[j]) - origin)))
        a, b = Vector(outline[1]) - origin, Vector(outline[index]) - origin
        det = a.cross(b)
        if abs(det) < 1e-8 or not math.isclose(abs(area(outline)), face.area, rel_tol=1e-4, abs_tol=1e-5):
            raise ValueError('Material relief needs nondegenerate planar field faces.')
        coordinates = {}
        for layer in mesh.uv_layers:
            zero, one, other = (layer.data[face.loop_start + j].uv.copy() for j in (0, 1, index))
            coordinates[layer.name] = (zero, one - zero, other - zero)
        for x in range(math.floor(min(p[0] for p in outline) / GRID),
                       math.ceil(max(p[0] for p in outline) / GRID)):
            strip = clip(clip(outline, 1, 0, -x * GRID, bounded=True),
                         -1, 0, (x + 1) * GRID, bounded=True)
            if not strip:
                continue
            for y in range(math.floor(min(p[1] for p in strip) / GRID),
                           math.ceil(max(p[1] for p in strip) / GRID)):
                cell = clip(clip(strip, 0, 1, -y * GRID, bounded=True),
                            0, -1, (y + 1) * GRID, bounded=True)
                if cell:
                    cells.append(([Vector(p) for p in cell], (origin, a, b, det, coordinates)))
    return u, v, normal * depth, cells


def _weights(points, boundary):
    """Exact segment distances in chart metres, with bounded temporary memory."""
    xy = np.asarray(points, dtype=np.float32)
    result = np.ones(len(xy), dtype=np.float32)
    starts, ends = (xy[list(indices)] for indices in zip(*boundary))
    for start, end in zip(starts, ends):
        candidates = np.flatnonzero(((xy >= np.minimum(start, end) - 2 * BORDER) &
                                     (xy <= np.maximum(start, end) + 2 * BORDER)).all(axis=1))
        delta = end - start
        query = xy[candidates] - start
        t = np.clip((query * delta).sum(axis=1) / np.dot(delta, delta), 0., 1.)
        distance = np.linalg.norm(query - t[:, None] * delta, axis=1)
        t = np.clip((distance - BORDER) / BORDER, 0., 1.)
        result[candidates] = np.minimum(result[candidates], t * t * (3 - 2 * t))
    return result


def cage(mesh):
    """Subdivide only the flat field, preserve all affine UVs and pin its perimeter."""
    colors = []
    for attribute in mesh.color_attributes:
        color = tuple(attribute.data[0].color)
        if any(tuple(item.color) != color for item in attribute.data):
            raise ValueError('The relief pilot cannot resample painted vertex colors.')
        colors.append((attribute.name, attribute.data_type, attribute.domain, color))
    groups = defaultdict(list)
    for face in mesh.polygons:
        groups[_chart_key(mesh, face)].append(face)
    vertices, faces, weights = [], [], []
    layers = {layer.name: [] for layer in mesh.uv_layers}
    for group in groups.values():
        u, v, base, cells = _chart_cells(mesh, group)
        if not cells:
            continue
        offset, index, points = len(vertices), {}, []
        users = Counter()
        for poly, (_, data) in zip(_conform([poly for poly, _ in cells]), cells):
            origin, a, b, det, coordinates = data
            ids, kept = [], []
            def vertex(point):
                key = tuple(round(c, 5) for c in point)
                if key not in index:
                    index[key] = len(points)
                    points.append(point)
                    vertices.append(base + u * point.x + v * point.y)
                return index[key]
            for point in poly:
                i = vertex(point)
                if i not in ids:
                    ids.append(i)
                    kept.append(point)
            if len(ids) < 3:
                continue
            # Keep the regular quads. A convex fan makes clipped cells with
            # collinear edge samples safe for Blender's subdivider.
            if len(ids) == 4 and all(abs((q-p).cross(r-q)) > 1e-7
                                     for p, q, r in zip(kept, kept[1:]+kept[:1], kept[2:]+kept[:2])):
                parts = (ids,)
            else:
                middle = vertex(sum(kept, Vector((0., 0.))) / len(kept))
                parts = [(i, j, middle) for i, j in _edges(ids) if
                         abs((points[j] - points[i]).cross(points[middle] - points[i])) > 1e-9]
            for part in parts:
                faces.append(tuple(offset + i for i in part))
                users.update(tuple(sorted(edge)) for edge in _edges(part))
                for i in part:
                    d = points[i] - origin
                    for name, (zero, one, other) in coordinates.items():
                        layers[name].extend(zero + one * (d.cross(b) / det) + other * (a.cross(d) / det))
        if any(count > 2 for count in users.values()):
            raise ValueError('Material relief needs a non-overlapping planar field.')
        weights.extend(_weights(points, [edge for edge, count in users.items() if count == 1]))
    output = bpy.data.meshes.new(mesh.name + ' Relief cage')
    output.from_pydata(vertices, [], faces)
    output.update()
    output.polygons.foreach_set('use_smooth', [True] * len(faces))
    for material in mesh.materials:
        output.materials.append(material)
    for name, values in layers.items():
        layer = output.uv_layers.new(name=name, do_init=False)
        layer.data.foreach_set('uv', values)
    for name, data_type, domain, color in colors:
        layer = output.color_attributes.new(name=name, type=data_type, domain=domain)
        layer.data.foreach_set('color', np.tile(color, len(layer.data)).astype(np.float32))
    output.uv_layers.active_index = mesh.uv_layers.active_index
    output.uv_layers[mesh.uv_layers.active.name].active_render = True
    return output, weights


def height_image(material, craft, weather):
    """Recover the original metres-valued relief behind a Caelmor normal map."""
    from caelmor_architecture.construction_relief import field_maps
    family = material['caelm_shared_field']
    name = f'Caelmor Height {family} {craft} {weather:.2f}'
    if name not in bpy.data.images:
        *_, height = field_maps(family, craft, weather, (.5, .5, .5), include_height=True)
        size = height.shape[0]
        image = bpy.data.images.new(name, size, size, alpha=False, float_buffer=True)
        image.colorspace_settings.name = 'Non-Color'
        rgba = np.ones((size, size, 4), dtype=np.float32)
        rgba[:, :, :3] = height[:, :, None] / .04
        image.pixels.foreach_set(rgba.ravel())
        image.file_format = 'OPEN_EXR'
        image.pack()
    return bpy.data.images[name]


def install(obj, image, *, strength=.025, levels=1, uv=FIELD_UV, repeat=True):
    """Build an editable cage and native modifiers on a generated field only."""
    if obj.type != 'MESH' or not obj.get('caelm_field_family') or obj.get('caelm_collider'):
        raise ValueError('Select a mapped roof or masonry construction field.')
    if obj.get('caelm_protected') or obj.modifiers or obj.vertex_groups:
        raise ValueError('Material relief cannot replace protected geometry, vertex groups or an existing modifier stack.')
    if image.colorspace_settings.name != 'Non-Color' or uv not in obj.data.uv_layers:
        raise ValueError('Use a Non-Color height image and an existing UV layer shared with the material.')
    if not math.isfinite(strength) or not 0 < strength <= .04 or levels not in (0, 1, 2):
        raise ValueError('Choose strength above zero and up to 0.04 m and subdivision level 0–2.')
    source = obj.data
    mesh, weights = cage(source)
    triangles = (sum(len(face.vertices) for face in mesh.polygons) * 2 * 4 ** (levels - 1)
                 if levels else sum(len(face.vertices) - 2 for face in mesh.polygons))
    if triangles > MAX_TRIANGLES:
        bpy.data.meshes.remove(mesh)
        raise ValueError(f'The requested subdivision exceeds {MAX_TRIANGLES:,} triangles on this field. Lower the resolution.')
    obj.data = mesh
    original_name = source.name
    source.name += ' (undisplaced input)'
    source.use_fake_user = True
    mesh.name = original_name
    mask = obj.vertex_groups.new(name='Caelmor Relief Interior')
    for i, weight in enumerate(weights):
        if weight > 0:
            mask.add([i], float(weight), 'REPLACE')
    subdivide = obj.modifiers.new('Caelmor Relief Sampling', 'SUBSURF')
    subdivide.subdivision_type = 'SIMPLE'
    subdivide.levels = subdivide.render_levels = levels
    subdivide.uv_smooth = 'NONE'
    displacement = obj.modifiers.new('Caelmor Material Height', 'DISPLACE')
    texture = bpy.data.textures.new(image.name, type='IMAGE')
    texture.image = image
    texture.extension = 'REPEAT' if repeat else 'EXTEND'
    displacement.texture = texture
    displacement.texture_coords = 'UV'
    displacement.uv_layer = uv
    displacement.direction = 'NORMAL'
    displacement.vertex_group = mask.name
    displacement.mid_level = 0.
    displacement.strength = strength
    return source
