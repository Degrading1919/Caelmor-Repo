"""Native guide lifecycle, timber/masonry shape, and collision export checks."""
import json
import math
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

import caelmor_architecture as addon
from caelmor_architecture.blender_backend import load_settings
from caelmor_architecture.guide_backend import GUIDE, HOST, SCHEDULE, anchor_of
from render_evidence import point_camera, setup_scene
from test_blockout_authoring_blender import select
from test_condition_export import read_glb


def cottage(props, location, wealth='ESTABLISHED'):
    props.caelm_function = 'COTTAGE'
    props.caelm_floors = 1
    props.caelm_wealth = wealth
    props.caelm_detail = 'MEDIUM'
    bpy.ops.mesh.primitive_cube_add(location=location)
    proxy = bpy.context.object
    proxy.scale = (4.2, 3.125, 1.675)
    proxy.rotation_euler.z = .31
    proxy.hide_render = True
    proxy.display_type = 'WIRE'
    assert bpy.ops.caelmor.fit_blockout() == {'FINISHED'}
    return addon._active_build(bpy.context), proxy


def face(collection, name, side, profile):
    anchor = anchor_of(collection)
    bpy.context.view_layer.update()
    data = load_settings(collection)
    if side == 'rear':
        points = [(data['width']-s, data['depth']+.045, z) for s,z in profile]
    else:
        points = [(data['width']+.045, s, z) for s,z in profile]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([anchor.matrix_world @ Vector(p) for p in points], [], [tuple(range(len(points)))])
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    select(obj)
    return obj


def opening(props, collection, source, kind, leaf=True):
    props.caelm_guide_target = collection
    props.caelm_guide_kind = kind
    props.caelm_guide_leaf = leaf
    select(source)
    assert bpy.ops.caelmor.opening_guide(action='APPLY') == {'FINISHED'}
    assert source.get(HOST) == collection and source.parent == anchor_of(collection)
    assert source.hide_render and source.display_type == 'WIRE'
    return source[GUIDE]['id']


def rejected(operator, message, **kwargs):
    try:
        operator(**kwargs)
    except RuntimeError as exc:
        assert message in str(exc), str(exc)
    else:
        raise AssertionError(f'Expected failure: {message}')


def assembly(collection, identifier, *, layer=None, role=None):
    return [o for o in collection.objects if f'.guide.{identifier}.' in o.get('caelm_buffer_id','')
            and (layer is None or o.get('caelm_layer') == layer)
            and (role is None or o.get('caelm_component_role') == role)]


def hits(objects, collection, start, direction, distance=.68):
    world = anchor_of(collection).matrix_world
    start = world @ Vector(start)
    direction = world.to_3x3() @ Vector(direction)
    for obj in objects:
        vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
        tree = BVHTree.FromPolygons(vertices, [tuple(p.vertices) for p in obj.data.polygons])
        if tree.ray_cast(start, direction, distance)[0] is not None:
            return True
    return False


def render(scene, camera, collection, filename):
    world = anchor_of(collection).matrix_world
    center = Vector((4.2,3.125,2.0))
    point_camera(camera, world @ (center + Vector((11,17,7))), world @ center)
    point_camera(bpy.data.objects['Evidence Sun'], world @ (center + Vector((1,10,12))), world @ center)
    point_camera(bpy.data.objects['Evidence Fill'], world @ (center + Vector((7,10,4))), world @ center)
    camera.data.ortho_scale = 14.2
    scene.render.resolution_x = 960
    scene.render.resolution_y = 725
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 93
    scene.render.filepath = str(filename)
    bpy.ops.render.render(write_still=True)


def main(directory, evidence=False):
    scene, camera, _, _, _ = setup_scene()
    props = scene.caelmor_settings
    collection, proxy = cottage(props, (5,-2,1.675))
    name = collection.name
    select(next(o for o in collection.objects if o.get('caelm_layer') == 'roof'))
    roof = bpy.context.object
    retained = roof.data.materials[0].copy()
    retained.name = 'Pilot retained roof slot'
    roof.data.materials[0] = retained
    baseline = collection['caelm_source_geometry_hash']
    before = {o.get('caelm_buffer_id'): o for o in collection.objects if o.get('caelm_buffer_id')}
    guide = face(collection,'Rear opening guide','rear',[(1.25,.45),(2.35,.45),(2.35,2.59),(1.25,2.59)])
    source_vertices = [tuple(v.co) for v in guide.data.vertices]
    door = opening(props,collection,guide,'DOOR')
    assert [tuple(v.co) for v in guide.data.vertices] == source_vertices
    assert roof.name in collection.objects and roof.data.materials[0] == retained
    assert assembly(collection, door, role='frame_member') and assembly(collection, door, layer='doors')
    walls = [o for o in collection.objects if o.get('caelm_layer') == 'walls']
    colliders = [o for o in collection.objects if o.get('caelm_collider')]
    assert not hits(walls,collection,(6.6,6.47,1.20),(0,-1,0))
    assert hits(colliders,collection,(6.6,6.47,1.20),(0,-1,0))
    assert collection['caelm_source_geometry_hash'] != baseline

    # A window on the otherwise blocked side gets a real cut and a shuttered
    # assembly, while unrelated roof/door sections keep their Blender identity.
    old_leaf = assembly(collection, door, layer='doors')[0]
    window = face(collection,'Window guide','right',[(2.15,1.25),(3.40,1.25),(3.40,2.20),(2.15,2.20)])
    wid = opening(props,collection,window,'WINDOW')
    assert old_leaf.name in collection.objects and roof.name in collection.objects
    assert len(assembly(collection, wid, layer='windows')) == 2
    assert not hits([o for o in collection.objects if o.get('caelm_layer') == 'walls'],
                    collection,(8.61,2.80,1.65),(-1,0,0))
    assert hits([o for o in collection.objects if o.get('caelm_collider')],
                collection,(8.61,2.80,1.65),(-1,0,0))
    cavity = assembly(collection, wid, role='frame_member')[0]
    finish = bpy.data.materials.new('Pilot window oak')
    finish.diffuse_color = (.20,.085,.039,1.)
    finish.use_nodes = True
    finish.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = finish.diffuse_color
    select(cavity)
    props.caelm_finish_scope = 'COMPONENT'
    props.caelm_finish_material = finish
    assert bpy.ops.caelmor.stage_finish() == {'FINISHED'}
    assert bpy.ops.caelmor.regenerate() == {'FINISHED'}
    roof = next(o for o in collection.objects if o.get('caelm_buffer_id') in before and
                o.get('caelm_layer') == 'roof' and o.data.materials[0] == retained)
    guide_hash = collection['caelm_source_geometry_hash']
    anchor = anchor_of(collection)
    window.location.y += .32
    select(window)
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    assert window[GUIDE]['id'] == wid and collection['caelm_source_geometry_hash'] != guide_hash
    assert assembly(collection, wid, role='frame_member')[0].data.materials[0] == finish
    assert roof.name in collection.objects
    bpy.context.view_layer.update()
    guide_to_local = anchor.matrix_world.inverted() @ window.matrix_world
    stretch = guide_to_local.inverted().to_3x3() @ Vector((0,.16,0))
    for vertex in window.data.vertices:
        if (guide_to_local @ vertex.co).y > 3.1:
            vertex.co += stretch
    window.data.update()
    saved_seed = props.caelm_seed
    props.caelm_seed += 1  # A staged panel change survives guide-only operations.
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    assert props.caelm_seed == saved_seed+1 and load_settings(collection)['seed'] == saved_seed
    props.caelm_seed = saved_seed
    revised = next(g for g in json.loads(collection[SCHEDULE]) if g['id'] == wid)
    assert abs(revised['s1']-revised['s0']-1.41) < 1e-4
    assert assembly(collection, wid, role='frame_member')[0].data.materials[0] == finish

    current_hash = collection['caelm_source_geometry_hash']
    current_schedule = collection[SCHEDULE]
    overlap = face(collection,'Conflicting guide','right',[(2.63,1.26),(3.63,1.26),(3.63,2.17),(2.63,2.17)])
    rejected(bpy.ops.caelmor.opening_guide, 'overlaps', action='APPLY')
    assert not overlap.get(HOST) and collection[SCHEDULE] == current_schedule
    bpy.data.objects.remove(overlap, do_unlink=True)
    window.location.y -= 3.0
    select(window)
    rejected(bpy.ops.caelmor.opening_guide, 'corner', action='REFRESH')
    assert collection['caelm_source_geometry_hash'] == current_hash
    window.location.y += 3.0
    assert bpy.ops.caelmor.opening_guide(action='REMOVE') == {'FINISHED'}
    assert window.get(HOST) is None and window.parent is None and not window.hide_render
    assert not assembly(collection, wid)
    assert not any(wid in key for key in load_settings(collection)['construction_overrides'].get('by_component',{}))
    assert roof.name in collection.objects
    window.hide_render = True

    # Replace an attached rectangle with an editable ellipse profile and keep
    # its identity. Retain the existing timber finish in later refreshes.
    old_world = guide.matrix_world.copy()
    assert guide.parent == anchor
    new_face = face(collection,'Rounded profile source','rear',[(1.25,.45),(2.45,.45)] +
                    [(1.85+.60*math.cos(i*math.pi/8),2.20+.43*math.sin(i*math.pi/8)) for i in range(9)])
    guide.data = new_face.data
    bpy.data.objects.remove(new_face,do_unlink=True)
    props.caelm_guide_kind = 'ROUND_DOOR'
    props.caelm_guide_leaf = False
    select(guide)
    assert bpy.ops.caelmor.opening_guide(action='APPLY') == {'FINISHED'}
    assert guide[GUIDE]['id'] == door
    assert all(abs(a-b) < 2e-6 for left,right in zip(guide.matrix_world,old_world) for a,b in zip(left,right))
    assert not assembly(collection, door, layer='doors')
    assert len(assembly(collection, door, role='frame_member')) == 1
    wall_objects = [o for o in collection.objects if o.get('caelm_layer')=='walls']
    colliders = [o for o in collection.objects if o.get('caelm_collider')]
    assert not hits(wall_objects,collection,(6.55,6.47,2.50),(0,-1,0))
    assert hits(wall_objects,collection,(7.10,6.47,2.55),(0,-1,0))
    assert not hits(colliders,collection,(6.55,6.47,1.25),(0,-1,0))
    assert hits(colliders,collection,(7.10,6.47,2.55),(0,-1,0))
    assert any(o.name.startswith('Collider Approach') for o in colliders)

    protected = assembly(collection, door, role='frame_member')[0]
    select(protected)
    assert bpy.ops.caelmor.protect_selected() == {'FINISHED'}
    guide.location.x += .21
    select(guide)
    current_hash = collection['caelm_source_geometry_hash']
    rejected(bpy.ops.caelmor.opening_guide, 'protected section', action='REFRESH')
    assert protected.name in collection.objects and collection['caelm_source_geometry_hash'] == current_hash
    guide.location.x -= .21
    select(protected)
    assert bpy.ops.caelmor.protect_selected() == {'FINISHED'}

    # Capture the closed fitted timber example for authoring review. The open
    # variant above has already exercised the separate traversable collision.
    props.caelm_guide_leaf = True
    select(guide)
    assert bpy.ops.caelmor.opening_guide(action='APPLY') == {'FINISHED'}
    wid = opening(props,collection,window,'WINDOW')
    select(assembly(collection,wid,role='frame_member')[0])
    props.caelm_finish_material = finish
    assert bpy.ops.caelmor.stage_finish() == {'FINISHED'}
    assert bpy.ops.caelmor.regenerate() == {'FINISHED'}
    if evidence:
        render(scene,camera,collection,directory/'guided-timber.jpg')
    props.caelm_guide_kind = 'ROUND_DOOR'
    props.caelm_guide_leaf = False
    select(guide)
    assert bpy.ops.caelmor.opening_guide(action='APPLY') == {'FINISHED'}
    guide.location.x += .07
    select(guide)
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    current_schedule = json.loads(collection[SCHEDULE])
    proxy.scale.y += .15
    proxy.rotation_euler.z += .17
    proxy.location.x += 1.
    select(next(o for o in collection.objects if o.get('caelm_layer') == 'roof'))
    assert bpy.ops.caelmor.fit_blockout(refit=True) == {'FINISHED'}
    assert json.loads(collection[SCHEDULE]) == current_schedule
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    source_hash = collection['caelm_source_geometry_hash']

    path = directory/'guided-cottage.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    bpy.ops.wm.open_mainfile(filepath=str(path))
    collection = bpy.data.collections[name]
    guide = bpy.data.objects['Rear opening guide']
    select(guide)
    assert guide[HOST] == collection and guide[GUIDE]['id'] == door
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    assert json.loads(collection[SCHEDULE]) == current_schedule
    assert collection['caelm_source_geometry_hash'] == source_hash
    assert assembly(collection,wid,role='frame_member')[0].data.materials[0].name == 'Pilot window oak'
    path = directory/'guided-cottage.glb'
    assert bpy.ops.caelmor.export(filepath=str(path),construction_metadata=True) == {'FINISHED'}
    doc, _ = read_glb(path)
    collision, _ = read_glb(path.with_suffix('.collision.glb'))
    assert all('guide_host' not in node.get('extras',{}) and node['name'] != guide.name for node in doc['nodes'])
    assert any(f'.guide.{door}.' in node.get('extras',{}).get('caelm_buffer_id','') for node in doc['nodes'])
    sidecar = json.loads(path.with_suffix('.caelmor.json').read_text(encoding='utf-8'))
    assert sidecar['version'] == 1 and sidecar['source_validation']['valid']
    assert sidecar['collision']['object_count'] == 6
    assert any(node['name'].startswith('Collider Approach ') for node in collision['nodes'])
    assert not any(key in sidecar for key in ('opening_guides',SCHEDULE))

    # A separately generated affluent cottage exercises the dressed arch
    # without replacing the timber example or its saved artist inputs.
    scene = bpy.context.scene
    camera = scene.camera
    for obj in collection.objects:
        obj.hide_render = True
    masonry, _ = cottage(scene.caelmor_settings, (5,-2,1.675), wealth='AFFLUENT')
    masonry_source = face(masonry,'Masonry arch guide','rear',[(1.15,.45),(2.50,.45),(2.50,2.63),(1.15,2.63)])
    mid = opening(scene.caelmor_settings,masonry,masonry_source,'ROUND_DOOR',leaf=False)
    assert assembly(masonry,mid,role='arch_ring')[0].get('caelm_treatment') == 'dressed_stone'
    if evidence:
        render(scene,camera,masonry,directory/'guided-masonry.jpg')
    bpy.ops.wm.read_factory_settings(use_empty=True)
    assert bpy.ops.import_scene.gltf(filepath=str(path)) == {'FINISHED'}
    assert any(f'.guide.{door}.' in o.get('caelm_buffer_id','') for o in bpy.context.scene.objects)
    print('OPENING_GUIDES_NATIVE_PASS', sidecar['source_validation']['source_triangles'],
          sidecar['collision']['object_count'])


if __name__ == '__main__':
    if output := os.environ.get('CAELMOR_OPENING_CHECK_DIR'):
        path = Path(output)
        path.mkdir(parents=True,exist_ok=True)
        main(path, bool(os.environ.get('CAELMOR_OPENING_RENDER')))
    else:
        with TemporaryDirectory(prefix='guide_test_', dir=ROOT/'dist') as temp:
            main(Path(temp))
