"""Fit an authored rectangular eave envelope without modifying its source mesh."""
from dataclasses import replace
import math
from itertools import product

from mathutils import Vector

from .model import resolve_settings, style_for


def fit(settings, source):
    if settings.region != 'LOWMARK' or settings.function != 'COTTAGE':
        raise ValueError('Select Lowmark and Cottage to fit a blockout')
    if (source is None or source.type != 'MESH' or source.get('caelm_generated')
            or source.modifiers or source.mode != 'OBJECT'):
        raise ValueError('Select an unmodified box mesh in Object Mode')
    mesh = source.data
    if len(mesh.vertices) != 8 or len(mesh.polygons) != 6 or any(len(p.vertices) != 4 for p in mesh.polygons):
        raise ValueError('The source must be one rectangular box with six quad faces')
    corners = [vertex.co for vertex in mesh.vertices]
    low = Vector([min(v[axis] for v in corners) for axis in range(3)])
    high = Vector([max(v[axis] for v in corners) for axis in range(3)])
    extent = high - low
    if min(extent) <= 0:
        raise ValueError('The box must have positive width, depth and height')
    grid = [tuple(round((v[i] - low[i]) / extent[i], 5) for i in range(3)) for v in corners]
    faces = {(axis, corner) for p in mesh.polygons for axis in range(3) for corner in (0, 1)
             if all(grid[i][axis] == corner for i in p.vertices)}
    if set(grid) != set(product((0, 1), repeat=3)) or len(faces) != 6:
        raise ValueError('The mesh must follow its local X, Y and Z axes. Rotate the object in Object Mode')

    matrix = source.matrix_world
    origin = matrix @ low
    if not all(math.isfinite(value) for value in origin):
        raise ValueError('The box must have a finite world position')
    axes = [column.to_3d() for column in matrix.col[:3]]
    scales = [axis.length for axis in axes]
    if not all(math.isfinite(scale) and scale > 0 for scale in scales):
        raise ValueError('The blockout needs a finite positive scale')
    x, y, z = [axis.normalized() for axis in axes]
    if (abs(x.z) > 1e-5 or abs(y.z) > 1e-5 or z.z < 1 - 1e-6
            or (z - Vector((0, 0, 1))).length > 1e-5
            or abs(x.dot(y)) > 1e-5 or x.cross(y).z < 1 - 1e-6):
        raise ValueError('Use an upright box with Z rotation and no shear or reflection')
    width, depth, height = [extent[i] * scales[i] for i in range(3)]
    if not isinstance(settings.floors, int) or not 1 <= settings.floors <= 3:
        raise ValueError('Choose 1–3 floors before fitting the box')
    floor_height = (height - style_for(settings).foundation_height) / settings.floors
    # A rotation can perturb matrix-column lengths at float precision. Retain
    # the saved dimensions when nothing changed at our 10 μm fit precision.
    dimensions = {field: round(value, 5) for field, value in
                  zip(('width', 'depth', 'floor_height'), (width, depth, floor_height))}
    if settings.fit_blockout:
        for field, value in dimensions.items():
            old = getattr(settings, field)
            if math.isclose(old, value, abs_tol=1.1e-5):
                dimensions[field] = old
    fitted = replace(settings, **dimensions,
                     footprint='RECT', world_aware=True, use_grammar=False, fit_blockout=True)
    resolve_settings(fitted)
    return fitted, (origin, math.atan2(x.y, x.x))
