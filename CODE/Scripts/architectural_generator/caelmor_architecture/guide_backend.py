"""Keep editable Blender faces separate from their generated wall assemblies."""
from dataclasses import dataclass
import math
import uuid

import bpy
from mathutils import Matrix, Vector

from .openings import Opening, wall_edges


HOST = 'caelm_guide_host'
GUIDE = 'caelm_guide'
SCHEDULE = 'caelm_opening_schedule'


@dataclass(frozen=True)
class Binding:
    id: str
    side: str
    kind: str
    leaf: bool


def anchor_of(collection):
    return next(obj for obj in collection.objects if obj.get('caelm_anchor'))


def _vertices(source, anchor):
    if (source.type != 'MESH' or source.library or source.get('caelm_generated') or source.modifiers
            or source.mode != 'OBJECT' or len(source.data.polygons) != 1):
        raise ValueError(f'{source.name}: choose an unmodified mesh with one face in Object Mode')
    if source.parent and source.parent != anchor:
        raise ValueError(f'{source.name}: the guide needs to be free-standing or attached to this building root')
    polygon = source.data.polygons[0]
    if len(polygon.vertices) != len(source.data.vertices):
        raise ValueError(f'{source.name}: remove unused vertices from the guide')
    matrix = anchor.matrix_world.inverted() @ source.matrix_world
    vertices = [matrix @ source.data.vertices[i].co for i in polygon.vertices]
    if not all(math.isfinite(value) for vertex in vertices for value in vertex):
        raise ValueError(f'{source.name}: invalid guide coordinates')
    return vertices


def _project(points, edge):
    a, b = edge
    length = math.dist(a, b)
    tx, ty = ((b[i]-a[i])/length for i in range(2))
    offsets = [(v.x-a[0])*ty-(v.y-a[1])*tx for v in points]
    if max(map(abs, offsets)) > .22 or max(offsets)-min(offsets) > .012:
        return None
    return [((v.x-a[0])*tx+(v.y-a[1])*ty, v.z) for v in points]


def propose(collection, source, settings, kind, leaf):
    if not settings.fit_blockout:
        raise ValueError('Choose a box-fitted Lowmark Cottage as the guide target')
    if source.get(HOST) and source.get(HOST) != collection:
        raise ValueError('Remove this guide from its original building before attaching it here')
    points = _vertices(source, anchor_of(collection))
    hits = [side for side, edge in wall_edges(settings.width, settings.depth).items()
            if _project(points, edge) is not None]
    if len(hits) != 1:
        raise ValueError(f'{source.name}: place the face upright and parallel to one wall, within 0.22 m of its exterior')
    previous = source.get(GUIDE) or {}
    identifier = previous.get('id')
    if not identifier or any(o != source and o.get(HOST) == collection and
                             (o.get(GUIDE) or {}).get('id') == identifier for o in bpy.context.scene.objects):
        identifier = uuid.uuid4().hex
    return Binding(identifier, hits[0], kind, leaf)


def _profile(source, binding, points):
    if points is None:
        raise ValueError(f'{source.name}: guide left the {binding.side} wall; move it back or use Apply Guide to attach again')
    s0, s1 = min(s for s,z in points), max(s for s,z in points)
    z0, z1 = min(z for s,z in points), max(z for s,z in points)
    tol = .008
    turns = set()
    for i, (s,z) in enumerate(points):
        a, b = points[i-1], points[(i+1)%len(points)]
        turn = (s-a[0])*(b[1]-z)-(z-a[1])*(b[0]-s)
        if abs(turn) > 1e-6:
            turns.add(turn > 0)
    if len(turns) != 1 or s1-s0 < .1 or z1-z0 < .1:
        raise ValueError(f'{source.name}: use a convex, non-degenerate outline')
    is_box = len(points) == 4 and all(min(math.dist((s,z), corner) for s,z in points) < tol
                                      for corner in ((s0,z0),(s1,z0),(s1,z1),(s0,z1)))
    rise = 0.
    if binding.kind == 'ROUND_DOOR':
        if is_box:
            rise = min(.39*(s1-s0), .44, .21*(z1-z0))
        else:
            left = [z for s,z in points if abs(s-s0) < tol]
            right = [z for s,z in points if abs(s-s1) < tol]
            if any(len(side) < 2 or min(side) > z0+tol for side in (left, right)) or abs(max(left)-max(right)) > .025:
                raise ValueError(f'{source.name}: rounded heads need a level threshold and paired vertical jambs')
            spring = (max(left)+max(right))*.5
            rise = z1-spring
            center = (s1+s0)*.5
            crown = [(s,z) for s,z in points if s0+tol < s < s1-tol]
            if len(crown) < 3 or any(abs(z - spring - rise*math.sqrt(max(0.,1-((s-center)/((s1-s0)*.5))**2))) > .045
                                   for s,z in crown):
                raise ValueError(f'{source.name}: use a symmetric rounded head, or use a rectangle for the default head')
    elif not is_box:
        raise ValueError(f'{source.name}: rectangular doors and windows need a rectangular face')
    return Opening(binding.id, binding.side, 'window' if binding.kind == 'WINDOW' else 'door',
                   *(round(v,5) for v in (s0,s1,z0,z1,rise)), leaf=binding.leaf)


def collect(collection, settings, old, edit=None):
    """Read live guides against their saved wall datums and compute refit offsets."""
    if not collection or not old.get('fit_blockout'):
        return (), ()
    targets = [(o, Binding(**dict(o[GUIDE]))) for o in bpy.context.scene.objects
               if o.get(HOST) == collection and o.get(GUIDE) and (not edit or edit[0] != o)]
    if edit and edit[1]:
        targets.append(edit)
    if not targets:
        return (), ()
    bpy.context.view_layer.update()
    anchor = anchor_of(collection)
    old_edges = wall_edges(old['width'], old['depth'])
    new_edges = wall_edges(settings.width, settings.depth)
    guides, shifts = [], []
    for source, binding in targets:
        if (not edit or source != edit[0]) and source.parent != anchor:
            raise ValueError(f'{source.name}: restore its building-root parent or use Apply Guide to bind it again')
        current = old_edges[binding.side]
        guides.append(_profile(source, binding, _project(_vertices(source, anchor), current)))
        start, _ = new_edges[binding.side]
        delta = Vector((start[0]-current[0][0], start[1]-current[0][1], 0))
        if delta.length > 1e-6:
            shifts.append((source, delta))
    return tuple(sorted(guides, key=lambda item: item.id)), shifts


def apply_binding(collection, source, binding):
    world = source.matrix_world.copy()
    if binding:
        anchor = anchor_of(collection)
        if source.parent != anchor or not source.get(GUIDE):
            source.parent = anchor
            source.matrix_parent_inverse = Matrix.Identity(4)
            source.matrix_basis = anchor.matrix_world.inverted() @ world
        source[HOST] = collection
        source[GUIDE] = dict(id=binding.id, side=binding.side, kind=binding.kind, leaf=binding.leaf)
        if 'caelm_guide_display' not in source:
            source['caelm_guide_display'] = dict(display=source.display_type, hide_render=source.hide_render)
        source.display_type = 'WIRE'
        source.hide_render = True
    else:
        source.parent = None
        source.matrix_world = world
        for key in (HOST, GUIDE):
            del source[key]
        display = source.get('caelm_guide_display')
        if display:
            source.display_type = display['display']
            source.hide_render = display['hide_render']
            del source['caelm_guide_display']
