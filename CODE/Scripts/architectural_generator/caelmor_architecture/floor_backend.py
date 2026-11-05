"""Partition finished native meshes, retaining all original material/UV layers."""
import json
import uuid
import bpy
import bmesh
from . import floors

EPS = 1e-5


def _clip(mesh, low=None, high=None, solid=False):
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        for height, normal in ((low, (0, 0, 1)), (high, (0, 0, -1))):
            if height is None:
                continue
            result = bmesh.ops.bisect_plane(bm, geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                dist=EPS, plane_co=(0, 0, height), plane_no=normal,
                clear_inner=True, clear_outer=False)
            if solid:
                edges = [e for e in result['geom_cut'] if isinstance(e, bmesh.types.BMEdge) and e.is_boundary]
                if edges:
                    caps = bmesh.ops.holes_fill(bm, edges=edges, sides=0)['faces']
                    for face in caps:
                        # Use the adjacent construction material and sampled
                        # paint at the joint, never allocate a new material.
                        neighbor = next((f for e in face.edges for f in e.link_faces if f != face), None)
                        if neighbor:
                            face.material_index = neighbor.material_index
                            for uv in bm.loops.layers.uv.values():
                                for loop in face.loops:
                                    sample = next((l for f in loop.vert.link_faces if f != face
                                                   for l in f.loops if l.vert == loop.vert), None)
                                    if sample: loop[uv].uv = sample[uv].uv
                            for colors in (bm.loops.layers.float_color, bm.loops.layers.color):
                                for color in colors.values():
                                    for loop in face.loops:
                                        sample = next((l for f in loop.vert.link_faces if f != face
                                                       for l in f.loops if l.vert == loop.vert), None)
                                        if sample: loop[color] = sample[color]
                        face.normal_update()
                        # Discarded half lies opposite the clipping normal.
                        if face.normal.z*normal[2] > 0: face.normal_flip()
        bm.to_mesh(mesh)
        mesh.update()
    finally:
        bm.free()


def partition(stage, plan):
    """Run once AFTER atlas binding, BEFORE generated-collection transaction."""
    volumes = floors.schedule(plan)
    hosts = {v['volume']: v for v in volumes}
    for source in list(stage.objects):
        if source.type != 'MESH' or source.get('caelm_collider'): continue
        zone = source.get('caelm_world_zone')
        # Existing exterior access assemblies may intentionally span volumes
        # and have no host zone (e.g. Mire decks). Never fabricate a storey for
        # them or infer occupancy: retain them as shared always-visible access.
        shared = not zone and hasattr(plan, 'world_zones')
        volume = 'shared' if shared else (zone or 'main')
        if shared and volume not in hosts:
            host = dict(volume='shared', base=0., height=0., count=0,
                        boundaries=[], occupiable=False)
            volumes.append(host); hosts[volume] = host
        if volume not in hosts:
            raise ValueError(f'{source.name}: no floor schedule for construction volume {volume}')
        host = hosts[volume]
        source_id = source['caelm_buffer_id']
        mode = floors.behavior(source.get('caelm_layer'), source.get('caelm_structural_role', ''),
                               source.get('caelm_functional_role', ''),
                               component_role=source.get('caelm_component_role',''),
                               envelope=json.loads(source.get('caelm_roof_envelope','null')))
        if shared: mode = 'ALWAYS'
        lo = min(v.co.z for v in source.data.vertices)
        hi = max(v.co.z for v in source.data.vertices)
        bands = [(None, None, -1)] if mode != 'FLOOR' else [
            (None if i == 0 else host['boundaries'][i-1],
             host['boundaries'][i] if i < host['count'] else None, i)
            for i in range(host['count']+1)]
        parts = []
        for low, high, index in bands:
            if mode == 'FLOOR' and hi-lo < EPS:
                owner = sum(lo >= boundary-EPS for boundary in host['boundaries'])
                if index != owner: continue
            elif (low is not None and hi <= low+EPS) or (high is not None and lo >= high-EPS): continue
            part = source.copy()
            part.data = source.data.copy()
            if (low is not None and lo < low-EPS) or (high is not None and hi > high+EPS):
                _clip(part.data, low, high, source.get('caelm_topology') == 'SOLID')
            if not part.data.polygons:
                unused = part.data
                bpy.data.objects.remove(part, do_unlink=True)
                if unused.users == 0: bpy.data.meshes.remove(unused)
                continue
            stage.objects.link(part)
            key = f'{source_id}::floor:{volume}:{index}' if mode == 'FLOOR' else f'{source_id}::{mode.lower()}'
            part.name = key
            part['caelm_buffer_id'] = key
            part['caelm_source_buffer_id'] = source_id
            part['caelm_floor_volume'] = volume
            part['caelm_floor_index'] = index
            part['caelm_visibility'] = mode
            part['caelm_floor_min'] = min(v.co.z for v in part.data.vertices)
            part['caelm_floor_max'] = max(v.co.z for v in part.data.vertices)
            part['caelm_floor_contract'] = floors.VERSION
            if low is not None or high is not None:
                # Cut caps need fresh lightmap charts. Surface/material UVs
                # (including shared atlas UV2 and detail UV3) stay untouched.
                from .blender_backend import _lightmap_uv
                old = part.data.uv_layers.get('UV1_Lightmap')
                _lightmap_uv(part.data, old)
            parts.append(part)
        mesh = source.data
        bpy.data.objects.remove(source, do_unlink=True)
        if mesh.users == 0: bpy.data.meshes.remove(mesh)
    return volumes


def hierarchy(collection, anchor, volumes):
    """Stable names/extras; all transforms remain building-local identity."""
    building_id = collection.get('caelm_building_id') or uuid.uuid4().hex
    collection['caelm_building_id'] = building_id
    anchor['caelm_building_id'] = building_id
    existing = {o.get('caelm_floor_group'): o for o in collection.objects if o.get('caelm_floor_group')}
    def group(key, parent, **properties):
        obj = existing.get(key)
        if obj is None:
            obj = bpy.data.objects.new('Caelmor '+key, None)
            collection.objects.link(obj)
        obj['caelm_floor_group'] = key
        obj['caelm_building_id'] = building_id
        for name, value in properties.items(): obj['caelm_'+name] = value
        obj.parent = parent
        return obj
    for volume in volumes:
        key = volume['volume']
        root = group('volume:'+key, anchor, floor_volume=key)
        for obj in list(collection.objects):
            if obj.get('caelm_floor_volume') != key or obj.type != 'MESH': continue
            mode, index = obj['caelm_visibility'], obj['caelm_floor_index']
            node = group(f'{key}/{mode}/{index}', root, floor_volume=key,
                         visibility=mode, floor_index=index)
            obj.parent = node
            obj['caelm_building_id'] = building_id
    # Remove obsolete empty groups only; protected sections keep their parents.
    for obj in reversed(list(existing.values())):
        if not obj.children: bpy.data.objects.remove(obj, do_unlink=True)
    collection['caelm_floor_schedule'] = json.dumps(volumes, sort_keys=True)
    collection['caelm_floor_contract'] = floors.VERSION


def preview(collection, floor=-1, volume=None):
    """Non-destructive visual-only preview, independent of collisions/edits."""
    if not collection.get('caelm_floor_contract'):
        raise ValueError('Legacy building: Load Selected Settings, enable Floor Separation, then regenerate All Layers')
    volumes = json.loads(collection['caelm_floor_schedule'])
    volume = volume or volumes[0]['volume']
    cutoff = None if floor == -1 else floors.ceiling(volumes, volume, floor)
    for obj in collection.objects:
        if not obj.get('caelm_visibility') or obj.type != 'MESH' or obj.get('caelm_collider'): continue
        state = obj.get('caelm_preview_original')
        if state is None and cutoff is not None:
            state = json.dumps([obj.hide_get(), obj.hide_render])
            obj['caelm_preview_original'] = state
        if state is None: continue
        hidden, render = json.loads(state)
        show = floors.visible(obj['caelm_visibility'], obj['caelm_floor_min'], obj['caelm_floor_max'], cutoff)
        obj.hide_set(hidden or not show)
        obj.hide_render = render or not show
        if cutoff is None: del obj['caelm_preview_original']
    collection['caelm_preview_floor'] = floor
    collection['caelm_preview_volume'] = volume
