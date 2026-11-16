"""Native assembly, mapped finish and export checks. Set CAELMOR_COMPONENT_VIEWS to render evidence."""
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

from caelmor_architecture import _active_build, _settings_from_json, register
from caelmor_architecture import facade, world
from caelmor_architecture.authoring_ui import _opening_info, _opening_parts
from caelmor_architecture.blender_backend import build, export_building, load_settings
from caelmor_architecture.engine import generate
from test_condition_export import read_glb
from test_opening_guides_blender import face, opening, select
from render_evidence import point_camera


def tree(collection, objects):
    anchor = next(o for o in collection.objects if o.get('caelm_anchor'))
    vertices, faces = [], []
    for obj in objects:
        transform = anchor.matrix_world.inverted() @ obj.matrix_world
        faces.extend(tuple(len(vertices)+i for i in p.vertices) for p in obj.data.polygons)
        vertices.extend(transform @ v.co for v in obj.data.vertices)
    return BVHTree.FromPolygons(vertices,faces)


def ray_misses(tree, info, width=.98, height=.98):
    center = Vector(info['center'])
    tx,ty = info['tangent']
    nx,ny = info['normal']
    misses = 0
    for direction in (-1,1):
        for i in range(-10,11):
            for j in range(-10,11):
                x = info['width']*width*i/20
                z = info['height']*height*j/20
                p = center+Vector((tx*x+nx*direction,ty*x+ny*direction,z))
                misses += tree.ray_cast(p,(-nx*direction,-ny*direction,0.),2.)[0] is None
    return misses


def position(collection, identity, ds, dz=0., rejection=None):
    part = _opening_parts(collection,identity)[0]
    info = _opening_info(part)
    select(part)
    assert bpy.ops.caelmor.move_opening(action='SELECT')=={'FINISHED'}
    assert set(bpy.context.selected_objects)==set(_opening_parts(collection,identity))
    assert bpy.ops.caelmor.move_opening(action='BEGIN')=={'FINISHED'}
    handle = bpy.context.object
    tx,ty = info['tangent']
    handle.location += Vector((ds*tx,ds*ty,dz))
    if rejection:
        try:
            bpy.ops.caelmor.move_opening(action='APPLY')
        except RuntimeError as exc:
            assert rejection in str(exc), str(exc)
        else:
            raise AssertionError('Expected invalid opening position to be rejected')
        assert bpy.ops.caelmor.move_opening(action='CANCEL')=={'FINISHED'}
    else:
        assert bpy.ops.caelmor.move_opening(action='APPLY')=={'FINISHED'}
    return _opening_info(_opening_parts(collection,identity)[0])


def pbr(stem):
    directory = ROOT.parents[2]/'MEDIA'/'Materials'/'procedurally_generated'
    material = bpy.data.materials.new(stem)
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    shader = nodes.get('Principled BSDF')
    for suffix, channel in (('_albedo.png','Base Color'),('_rough.exr','Roughness'),('_normal.png','Normal')):
        node = nodes.new('ShaderNodeTexImage')
        node.image = bpy.data.images.load(str(directory/(stem+suffix)),check_existing=True)
        if channel!='Base Color':
            node.image.colorspace_settings.name='Non-Color'
        if channel=='Normal':
            normal = nodes.new('ShaderNodeNormalMap')
            links.new(node.outputs['Color'],normal.inputs['Color'])
            links.new(normal.outputs['Normal'],shader.inputs[channel])
        else:
            links.new(node.outputs['Color'],shader.inputs[channel])
    return material


def render_setup():
    scene = bpy.context.scene
    scene.render.resolution_x,scene.render.resolution_y = 768,512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.engine='BLENDER_WORKBENCH'
    shade = scene.display.shading
    shade.light='STUDIO'
    shade.color_type='SINGLE'
    shade.single_color=(.67,.65,.59)
    shade.show_cavity=True
    shade.cavity_type='BOTH'
    shade.show_shadows=True
    camera = bpy.data.objects.new('Evidence camera',bpy.data.cameras.new('Evidence camera'))
    scene.collection.objects.link(camera)
    scene.camera=camera
    camera.data.type='ORTHO'
    return scene,camera


def views(collection, info, label, folder, *, across=False, textured=False):
    scene,camera = render_setup()
    center = Vector(info['center'])
    tangent = Vector((*info['tangent'],0.))
    normal = Vector((*info['normal'],0.))
    anchor = next(o for o in collection.objects if o.get('caelm_anchor'))
    rows = [('front',4*normal),('oblique',4*normal+2.5*tangent+Vector((0,0,.7))),
            ('rear',-2*normal)]
    if across:
        rows = [('elevation',4*normal),('gameplay',12*normal+6*tangent+Vector((0,0,8.)))]
    if textured:
        scene.render.engine='BLENDER_EEVEE'
        scene.eevee.taa_render_samples=16
        scene.world=bpy.data.worlds.new('Evidence sky')
        scene.world.use_nodes=True
        scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.55
        sun=bpy.data.objects.new('Evidence sunlight',bpy.data.lights.new('Evidence sunlight','SUN'))
        scene.collection.objects.link(sun)
        sun.rotation_euler=(.5,-.52,2.9)
        sun.data.energy=2.
    for name,origin in rows:
        camera.data.ortho_scale=12.2 if across else 2.3
        point_camera(camera,anchor.matrix_world@(center+origin),anchor.matrix_world@center)
        scene.render.filepath=str(folder/f'{label}_{name}.png')
        bpy.ops.render.render(write_still=True)


def known_baseline(settings, collection, folder, info):
    """Use the actual previous facade module while keeping framing and camera matched."""
    source_path = 'CODE/Scripts/architectural_generator/caelmor_architecture/facade.py'
    revision = 'cc72e49721e5bb94eed0512f5a0e9d81839f2a01'
    old = dict(vars(facade))
    source = subprocess.check_output(['git','show',f'{revision}:{source_path}'],cwd=ROOT)
    exec(compile(source,source_path,'exec'),old)
    current = world.build_facades
    world.build_facades = old['build_facades']
    try:
        baseline,_ = build(replace(settings,production_geometry=False),
                           placement=((0,0,0),0.))
        bpy.context.view_layer.update()
        shapes = [o for o in baseline.objects if o.get('caelm_layer') in ('structure','windows','details')]
        assert ray_misses(tree(baseline,shapes),info)>0
        for obj in collection.objects:
            obj.hide_render=True
        views(baseline,info,'legacy_window',folder)
        wide = dict(info,center=(4.2,6.25,2.35))
        views(baseline,wide,'legacy_cottage',folder,across=True)
        for obj in collection.objects:
            obj.hide_render=bool(obj.get('caelm_collider') or obj.get('caelm_opening_handle'))
        for obj in baseline.objects:
            obj.hide_render=True
    finally:
        world.build_facades=current


def exports(collection, output, revision):
    destination = output/revision
    destination.mkdir(exist_ok=True)
    path = destination/'cottage.glb'
    export_building(collection,str(path))
    glb,_ = read_glb(path)
    source = {n['extras']['caelm_buffer_id'] for n in glb['nodes'] if 'mesh' in n}
    assert all('/opening.' not in key and '.opening.' not in key and '.frame.0.' not in key
               for key in source)
    assert all('caelm_opening_part' not in n.get('extras',{}) for n in glb['nodes'])
    assert len(source)==sum('mesh' in n for n in glb['nodes'])
    assert any('TEXCOORD_0' in p['attributes'] for m in glb['meshes'] for p in m['primitives'])
    return source,sum(len(m['primitives']) for m in glb['meshes'])


def main(output):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    register()
    bpy.ops.mesh.primitive_cube_add(location=(4.2,3.125,1.675))
    proxy = bpy.context.object
    proxy.scale=(4.2,3.125,1.675)
    proxy.hide_render=True
    proxy.display_type='WIRE'
    assert bpy.ops.caelmor.create_building(function='COTTAGE',region='LOWMARK',method='BOX')=={'FINISHED'}
    collection = _active_build(bpy.context)
    assert load_settings(collection)['production_geometry']
    # The right wall has room for a distinct artist-authored window.
    guide = face(collection,'Narrow guided window','right',[(2.15,1.21),(2.77,1.21),(2.77,2.13),(2.15,2.13)])
    wid = opening(bpy.context.scene.caelmor_settings,collection,guide,'WINDOW')
    first = 'lowmark_main_hall/opening.2.window.0.1'
    second = 'lowmark_main_hall/opening.2.window.0.2'
    guided = 'lowmark_main_hall/guide.'+wid
    data = {key:_opening_info(_opening_parts(collection,key)[0]) for key in (first,second,guided)}
    for key,info in data.items():
        parts = _opening_parts(collection,key)
        assert {'timber','shutters','iron','windows'} <= {_opening_info(p)['part'] for p in parts}
        glass = next(p for p in parts if _opening_info(p)['part']=='windows')
        assert len(glass.data.vertices)==32
        assert ray_misses(tree(collection,parts),info)==0, key
    assert not any(token in o.get('caelm_buffer_id','') for o in collection.objects
                   for token in ('shingle courses','facade_stone','facade_mortar','facade_board_skin','facade_masonry_skin'))
    assert len([o for o in collection.objects if '.post.' in o.get('caelm_buffer_id','')])>=4
    assert any('Roof edge fascia' in o.get('caelm_buffer_id','') for o in collection.objects)
    assert all(not o.modifiers for o in collection.objects)
    materials = {
        'roof_cover': pbr('Lowmark_Brookoak_RoofShingles_RivenBake'),
        'wall_infill': pbr('Lowmark_Lime_Plaster_Whitewash_Maintained'),
        'frame_member': pbr('Lowmark_Planked_Oak_Joinery_Wood_Maintained'),
        'plinth': pbr('Lowmark_Fieldstone_Masonry'),
    }
    for role,material in materials.items():
        obj = next(o for o in collection.objects if o.get('caelm_component_role')==role)
        select(obj)
        assert bpy.ops.caelmor.edit_building(action='MATERIAL',group=role,
                                              match_group=True, material=material.name)=={'FINISHED'}
        assert any(o.type=='MESH' and material in list(o.data.materials) for o in collection.objects)
    custom = pbr('Lowmark_Planked_Oak_Joinery_Wood_Weathered')
    custom['caelm_material'] = 'timber'
    custom_name = custom.name
    sash = next(o for o in _opening_parts(collection,first) if _opening_info(o)['part']=='sash')
    select(sash)
    assert bpy.ops.caelmor.edit_building(action='MATERIAL',material=custom.name)=={'FINISHED'}
    before = exports(collection,output,'before')
    settings = _settings_from_json(load_settings(collection))
    views_enabled = 'CAELMOR_COMPONENT_VIEWS' in os.environ
    if views_enabled:
        known_baseline(settings,collection,output,data[first])
        views(collection,data[first],'new_unmoved_window',output)
        views(collection,dict(data[first],center=(4.2,6.25,2.35)),'before_move',output,across=True)
    prior_neighbor = {o['caelm_buffer_id']:o.as_pointer() for o in _opening_parts(collection,second)}
    next_info = position(collection,first,-.50)
    assert abs(Vector(next_info['center']).x-Vector(data[first]['center']).x-.50)<1e-4
    assert _opening_info(_opening_parts(collection,second)[0])==data[second]
    assert prior_neighbor=={o['caelm_buffer_id']:o.as_pointer() for o in _opening_parts(collection,second)}
    assert _opening_info(_opening_parts(collection,guided)[0])==data[guided]
    position(collection,first,3.1,rejection='overlaps')
    wall = tree(collection,[o for o in collection.objects if o.get('caelm_layer')=='walls'])
    # At the original leading edge the wall is filled. At the new leading edge it has a clear cut.
    x,y,z = next_info['center']
    assert wall.ray_cast((x-.68,y+.30,z),(0,-1,0),.9)[0] is not None
    assert wall.ray_cast((x+.35,y+.30,z),(0,-1,0),.9)[0] is None
    next_guided = position(collection,guided,.27)
    assert abs(next_guided['center'][1]-data[guided]['center'][1]-.27)<1e-4
    for key,info in ((first,next_info),(guided,next_guided)):
        assert ray_misses(tree(collection,_opening_parts(collection,key)),info)==0
    door = 'lowmark_main_hall/opening.0.door.0.1'
    # Exercise a door on a compatible clear facade in the pure geometry path.
    door_plan,_ = generate(replace(settings,width=12.),
                           finish_names=bpy.data.materials.keys(),opening_placements={door:(.35,0.)})
    assert any(o.get('placement_key')==door and o.get('edited')
               for edge in door_plan.world_zones[0].plan.facade_records for o in edge['openings'])
    after = exports(collection,output,'after')
    assert before==after, (before,after)
    if views_enabled:
        views(collection,next_info,'new_moved_window',output)
        views(collection,next_guided,'guided_window',output)
        wide = dict(next_info,center=(4.2,6.25,2.35))
        views(collection,wide,'after_move',output,across=True)
        views(collection,wide,'mapped_pbr',output,across=True,textured=True)
    saved = output/'openings.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(saved))
    name = collection.name
    bpy.ops.wm.open_mainfile(filepath=str(saved))
    collection=bpy.data.collections[name]
    build(_settings_from_json(load_settings(collection)),collection)
    assert _opening_info(_opening_parts(collection,first)[0])==next_info
    assert _opening_info(_opening_parts(collection,guided)[0])==next_guided
    assert any(o.data.materials[0].name==custom_name for o in _opening_parts(collection,first))
    original_objects=set(bpy.data.objects)
    assert bpy.ops.import_scene.gltf(filepath=str(output/'after'/'cottage.glb'))=={'FINISHED'}
    reimported=[o for o in bpy.data.objects if o not in original_objects and o.type=='MESH']
    assert {o['caelm_buffer_id'] for o in reimported}==after[0]
    assert all(o.data.uv_layers for o in reimported)
    print('CAELMOR_SELECTABLE_OPENINGS_PASS',
          len([o for o in collection.objects if o.get('caelm_generated') and not o.get('caelm_collider')]),
          len(after[0]), after[1])


if __name__=='__main__':
    folder = ROOT/'dist'/'component_verification'
    folder.mkdir(exist_ok=True)
    main(folder)
