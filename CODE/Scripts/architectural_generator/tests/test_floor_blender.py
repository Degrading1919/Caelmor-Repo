"""Native floor partition, lifecycle, appearance and GLB round-trip evidence.

blender -b --python tests/test_floor_blender.py [-- --render]
Reuses the established world evidence studio. No enterable interiors invented.
"""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate, validate
from caelmor_architecture.blender_backend import build, export_building, load_settings
from caelmor_architecture.floor_backend import preview
from test_construction_treatments import fixture
from test_condition_export import read_glb
from render_world_evidence import _reset_scene, _aim, _neutral_material

OUT = ROOT/'evidence'/'floor_visibility'
CASES = [(f'lowmark_{n}f', Settings(floors=n, footprint='L' if n == 2 else 'RECT',
             width=9, depth=6, detail='MEDIUM')) for n in (1,2,3)] + [
    ('smithy_wings', fixture()), ('thornfell_gatehouse', fixture('THORNFELL','GATEHOUSE'))]


def visuals(collection):
    return [o for o in collection.objects if o.type == 'MESH' and o.get('caelm_generated') and not o.get('caelm_collider')]


def collision(collection):
    return sorted((o['caelm_world_zone'], tuple(tuple(v.co) for v in o.data.vertices),
                   tuple(tuple(p.vertices) for p in o.data.polygons))
                  for o in collection.objects if o.get('caelm_collider'))


def metrics(collection):
    meshes = visuals(collection)
    for o in meshes: o.data.calc_loop_triangles()
    return dict(meshes=len(meshes), vertices=sum(len(o.data.vertices) for o in meshes),
                triangles=sum(len(o.data.loop_triangles) for o in meshes),
                materials=len({m.name for o in meshes for m in o.data.materials if m}))


def tree(collection):
    vertices, faces = [], []
    for obj in visuals(collection):
        offset = len(vertices)
        vertices.extend(tuple(v.co) for v in obj.data.vertices)
        faces.extend(tuple(offset+i for i in p.vertices) for p in obj.data.polygons)
    return BVHTree.FromPolygons(vertices, faces, all_triangles=False)


def probes(collection):
    points = [Vector(v) for o in visuals(collection) for v in o.bound_box]
    lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    rays = []
    for axis in (0,1,2):
        other = [i for i in range(3) if i != axis]
        for a in range(11):
            for b in range(9):
                for sign in (-1,1):
                    start = (lo+hi)/2
                    start[axis] = lo[axis]-2 if sign == 1 else hi[axis]+2
                    start[other[0]] = lo[other[0]]+(a+.39)/11*(hi[other[0]]-lo[other[0]])
                    start[other[1]] = lo[other[1]]+(b+.27)/9*(hi[other[1]]-lo[other[1]])
                    direction = Vector((0,0,0)); direction[axis] = sign
                    rays.append((start,direction))
    return rays


def camera(collection, scene, camera):
    points = [Vector(v) for o in visuals(collection) for v in o.bound_box]
    lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    target = (lo+hi)/2
    _aim(camera, target+Vector((24,-32,26)), target)
    camera.data.ortho_scale = max(hi.x-lo.x, hi.y-lo.y, hi.z-lo.z)*1.62
    scene.render.resolution_x, scene.render.resolution_y = 800, 600
    scene.eevee.taa_render_samples = 24


def capture(collection, name, state):
    mats = {o:tuple(o.data.materials) for o in visuals(collection)}
    clay = _neutral_material()
    for mode in ('material','clay'):
        if mode == 'clay':
            for obj in mats:
                obj.data.materials.clear(); obj.data.materials.append(clay)
        bpy.context.scene.render.filepath = str(OUT/f'{name}_{mode}_{state}.png')
        bpy.ops.render.render(write_still=True)
    for obj, slots in mats.items():
        obj.data.materials.clear()
        for mat in slots: obj.data.materials.append(mat)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    render = '--render' in sys.argv
    results = []
    for name, settings in CASES:
        print('FLOOR CASE', name, flush=True)
        scene, cam = _reset_scene()
        base, _ = build(replace(settings, floor_separation=False))
        colliders = collision(base)
        before = metrics(base)
        mats = {o['caelm_buffer_id']: tuple(m.name for m in o.data.materials) for o in visuals(base)}
        source_tree = tree(base)
        rays = probes(base)
        expected = [source_tree.ray_cast(*ray) for ray in rays]
        camera(base, scene, cam)
        if render: capture(base, name, 'legacy')
        with TemporaryDirectory(dir=ROOT/'dist') as temp:
            path = Path(temp)/'building.glb'
            export_building(base, str(path))
            before['glb_bytes'] = path.stat().st_size
            doc, _ = read_glb(path)
            before['primitives'] = sum(len(m['primitives']) for m in doc.get('meshes',[]))
            building, _ = build(replace(settings, floor_separation=True), collection=base)
            assert collision(building) == colliders
            assert building['caelm_floor_contract'] == 1
            after = metrics(building)
            split_tree = tree(building)
            for ray, original in zip(rays, expected):
                hit = split_tree.ray_cast(*ray)
                assert (hit[0] is None) == (original[0] is None), (name,ray,hit,original)
                if hit[0] is not None:
                    assert (hit[0]-original[0]).length < 2e-4, (name,ray,hit,original)
                    assert hit[1].dot(original[1]) > .999, (name,ray,'normal changed')
            ids = [o['caelm_buffer_id'] for o in visuals(building)]
            assert len(ids) == len(set(ids))
            hosts = {v['volume']:v for v in json.loads(building['caelm_floor_schedule'])}
            for o in visuals(building):
                assert tuple(m.name for m in o.data.materials) == mats[o['caelm_source_buffer_id']]
                assert [l.name for l in o.data.uv_layers][:2] == ['UV0_Metric', 'UV1_Lightmap']
                for layer in o.data.uv_layers:
                    assert all(abs(c) < 1e7 for uv in layer.data for c in uv.uv)
                assert o.parent['caelm_floor_group']
                assert o['caelm_building_id'] == building['caelm_building_id']
                if o['caelm_visibility']=='FLOOR':
                    host = hosts[o['caelm_floor_volume']]
                    index = o['caelm_floor_index']
                    if index: assert o['caelm_floor_min'] >= host['boundaries'][index-1]-2e-5
                    if index < host['count']: assert o['caelm_floor_max'] <= host['boundaries'][index]+2e-5
            volumes = json.loads(building['caelm_floor_schedule'])
            host = max(volumes, key=lambda v:v['count'])
            if render: capture(building, name, 'exterior')
            prior = {o:(o.hide_get(),o.hide_render) for o in visuals(building)}
            preview(building,0,host['volume'])
            hidden = [o for o in visuals(building) if o.hide_render and not prior[o][1]]
            assert hidden, name
            assert collision(building) == colliders
            assert all(o.hide_render for o in visuals(building) if o['caelm_visibility']=='COVERING'
                       and o['caelm_floor_max'] > host['base']+host['height'])
            if render: capture(building,name,'floor0')
            for level in range(1,host['count']):
                preview(building, level, host['volume'])
                if render: capture(building,name,f'floor{level}')
            # Export while hidden: still exports complete exterior, restores preview.
            preview(building,0,host['volume'])
            visibility = {o:(o.hide_get(),o.hide_render) for o in visuals(building)}
            group = visuals(building)[0].parent
            group.hide_set(True); group.hide_render = True
            sidecar = export_building(building,str(path))
            assert visibility == {o:(o.hide_get(),o.hide_render) for o in visuals(building)}
            assert group.hide_get() and group.hide_render, 'export changed artist-hidden parent'
            group.hide_set(False); group.hide_render = False
            doc, _ = read_glb(path)
            exported = {n['extras']['caelm_buffer_id']:n['extras'] for n in doc['nodes']
                        if n.get('extras',{}).get('caelm_buffer_id')}
            assert set(exported) == set(ids)
            assert all(e['caelm_floor_contract']==1 for e in exported.values())
            metadata = json.loads(Path(sidecar).read_text())
            assert metadata['floor_presentation']['occupancy_areas'] == []
            assert metadata['floor_presentation']['volumes'] == volumes
            after['glb_bytes'] = path.stat().st_size
            after['primitives'] = sum(len(m['primitives']) for m in doc.get('meshes',[]))
            # Roundtrip into an independent collection; preserve source.
            original_objects = set(bpy.data.objects)
            bpy.ops.import_scene.gltf(filepath=str(path))
            imported = [o for o in bpy.data.objects if o not in original_objects]
            sections = [o for o in imported if o.get('caelm_buffer_id')]
            assert {o['caelm_buffer_id'] for o in sections} == set(ids)
            assert all(o.parent.get('caelm_floor_group') for o in sections)
            for o in imported: bpy.data.objects.remove(o,do_unlink=True)
            preview(building,-1)
            assert prior == {o:(o.hide_get(),o.hide_render) for o in visuals(building)}
            if render: capture(building,name,'restored')
            # Rebuild: section-level edits, materials, stable IDs and collision preserved.
            chosen = next(o for o in visuals(building) if o['caelm_visibility']=='FLOOR')
            chosen['caelm_protected'] = True
            chosen.data.vertices[0].co.x += .013
            edited = chosen.data.vertices[0].co.copy()
            custom = bpy.data.materials.new('Floor artist override '+name)
            chosen.data.materials[0] = custom
            key = chosen['caelm_buffer_id']
            build(replace(settings,floor_separation=True),collection=building)
            retained = next(o for o in visuals(building) if o['caelm_buffer_id']==key)
            assert retained == chosen and retained.data.vertices[0].co == edited
            assert retained.data.materials[0] == custom
            assert {o['caelm_buffer_id'] for o in visuals(building)} == set(ids)
            assert collision(building) == colliders
            # Scoped regeneration must neither duplicate untouched sections nor
            # change their geometry/materials; preserve section-level overrides.
            unaffected = {o['caelm_buffer_id']:(o,tuple(m.name for m in o.data.materials))
                          for o in visuals(building) if o['caelm_layer'] != 'roof'}
            roof = next(o for o in visuals(building) if o['caelm_layer']=='roof')
            roof_key = roof['caelm_buffer_id']
            roof_custom = bpy.data.materials.new('Unprotected roof override '+name)
            roof.data.materials[0] = roof_custom
            build(replace(settings,floor_separation=True),collection=building,layers='ROOF')
            assert all(o in visuals(building) and tuple(m.name for m in o.data.materials)==slots
                       for o,slots in unaffected.values())
            assert next(o for o in visuals(building) if o['caelm_buffer_id']==roof_key).data.materials[0] == roof_custom
            hidden_artist = next(o for o in visuals(building) if o['caelm_visibility']=='FLOOR' and not o.get('caelm_protected'))
            hidden_artist.hide_set(True); hidden_artist.hide_render = True
            preview(building,0,host['volume']); preview(building,-1)
            assert hidden_artist.hide_get() and hidden_artist.hide_render
            try:
                build(replace(settings,floor_separation=False),collection=building)
            except ValueError as exc: assert 'Unprotect' in str(exc)
            else: raise AssertionError('Protected migration must be rejected')
        results.append(dict(case=name,settings=load_settings(building),volumes=volumes,
                            before=before,after=after,exterior_ray_checks=len(rays),
                            hidden_ground_meshes=len(hidden)))
    import caelmor_architecture as addon
    addon.register()
    assert bpy.context.scene.caelmor_settings.caelm_floor_separation
    assert not addon._settings_from_json({'seed':17}).floor_separation
    props=bpy.context.scene.caelmor_settings
    props.caelm_preview_floor=0
    assert bpy.ops.caelmor.floor_preview()=={'FINISHED'}
    props.caelm_preview_floor=-1
    assert bpy.ops.caelmor.floor_preview()=={'FINISHED'}
    expected_ids={o['caelm_buffer_id'] for o in visuals(building)}
    with TemporaryDirectory(dir=ROOT/'dist') as temp:
        path=str(Path(temp)/'floors.blend')
        collection_name=building.name
        bpy.ops.wm.save_as_mainfile(filepath=path)
        bpy.ops.wm.open_mainfile(filepath=path)
        reopened=bpy.data.collections[collection_name]
        assert {o['caelm_buffer_id'] for o in visuals(reopened)}==expected_ids
        preview(reopened,0);preview(reopened,-1)
    addon.unregister()
    (OUT/'metrics.json').write_text(json.dumps(dict(blender=bpy.app.version_string,cases=results,
        source_files={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ROOT/'caelmor_architecture').glob('*.py')}),indent=2)+'\n')
    print('FLOOR VISIBILITY: all native checks passed',flush=True)


if __name__ == '__main__': main()
