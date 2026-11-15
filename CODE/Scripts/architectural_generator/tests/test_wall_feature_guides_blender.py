"""Exercise a bearing post and a physically recessed plaster loss in Blender."""
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

from caelmor_architecture.blender_backend import export_building, load_settings
from caelmor_architecture.guide_backend import GUIDE, HOST, SCHEDULE, anchor_of
from render_evidence import point_camera
from test_condition_export import read_glb
from test_opening_guides_blender import assembly, cottage, face, opening, rejected, select, setup_scene


DAMP_OUTLINE = ((1.20,.70),(1.40,.61),(1.66,.68),(1.94,.62),(2.05,.83),
                (1.84,1.03),(1.61,.93),(1.43,1.01),(1.22,.90))


def timber_edge(collection, station):
    world = anchor_of(collection).matrix_world
    width = load_settings(collection)['width']
    points = [world @ Vector((width+.04,station,z)) for z in (.45,3.12)]
    mesh = bpy.data.meshes.new('Post stations')
    mesh.from_pydata(points, [(0,1)], [])
    obj = bpy.data.objects.new('Bearing post guide',mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def wall_hit(collection, station, z):
    world = anchor_of(collection).matrix_world
    width = load_settings(collection)['width']
    origin = world @ Vector((width+.30,station,z))
    direction = world.to_3x3() @ Vector((-1.,0.,0.))
    hits = []
    for obj in collection.objects:
        if obj.get('caelm_layer') != 'walls':
            continue
        vertices = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
        tree = BVHTree.FromPolygons(vertices,[tuple(p.vertices) for p in obj.data.polygons])
        point, _, _, distance = tree.ray_cast(origin,direction,.5)
        if point is not None:
            hits.append((distance,obj.get('caelm_material')))
    return min(hits)


def render(scene, camera, collection, path):
    world = anchor_of(collection).matrix_world
    center = Vector((7.5,3.3,1.62))
    point_camera(camera,world @ (center+Vector((12,-5.,5))),world @ center)
    point_camera(bpy.data.objects['Evidence Sun'],world @ (center+Vector((7.,-3.,6.))),world @ center)
    point_camera(bpy.data.objects['Evidence Fill'],world @ (center+Vector((3.,4.,5.))),world @ center)
    camera.data.ortho_scale = 8.2
    scene.render.resolution_x = 1060
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 93
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def render_loss_detail(scene, camera, collection, path):
    world = anchor_of(collection).matrix_world
    width = load_settings(collection)['width']
    center = Vector((width,1.63,.83))
    point_camera(camera,world @ (center+Vector((4.5,-2.,.75))),world @ center)
    point_camera(bpy.data.objects['Evidence Sun'],world @ (center+Vector((.6,-7.,4.))),world @ center)
    bpy.data.objects['Evidence Sun'].data.angle = .04
    bpy.data.objects['Evidence Fill'].data.energy = 170
    clay = bpy.data.materials.new('Clay section reference')
    clay.use_nodes = True
    clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (.43,.43,.43,1.)
    bpy.context.view_layer.material_override = clay
    camera.data.ortho_scale = 1.42
    scene.render.resolution_x = 800
    scene.render.resolution_y = 530
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 93
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def main(output, evidence):
    scene, camera, *_ = setup_scene()
    props = scene.caelmor_settings
    collection, _ = cottage(props,(5.,-2.,1.675))
    window = face(collection,'Neighboring window','right',[(4.74,1.27),(5.60,1.27),(5.60,2.19),(4.74,2.19)])
    opening(props,collection,window,'WINDOW')
    roof = next(obj for obj in collection.objects if obj.get('caelm_layer') == 'roof')
    base_hash = collection['caelm_source_geometry_hash']
    initial = wall_hit(collection,1.5,.80)
    assert initial[1] == 'plaster'
    if evidence:
        render(scene,camera,collection,output/'wall-before.jpg')

    post = timber_edge(collection,3.70)
    post_id = opening(props,collection,post,'TIMBER_POST')
    member = assembly(collection,post_id,role='frame_member')[0]
    native_world = anchor_of(collection).matrix_world.inverted() @ member.matrix_world
    assert min((native_world @ v.co).z for v in member.data.vertices) < .451
    assert max((native_world @ v.co).z for v in member.data.vertices) > 3.10
    assert member['caelm_treatment'] == 'structural_timber'

    damage = face(collection,'Splash-zone plaster loss','right',DAMP_OUTLINE)
    loss_id = opening(props,collection,damage,'PLASTER_LOSS')
    assert assembly(collection,loss_id,role='wall_infill')[0].get('caelm_material') == 'earthen_daub'
    cut = wall_hit(collection,1.5,.80)
    assert cut[1]=='earthen_daub' and .018 < cut[0]-initial[0] < .04
    assert wall_hit(collection,1.5,1.08)[1] == 'plaster'
    assert roof.name in collection.objects
    assert collection['caelm_source_geometry_hash'] != base_hash

    # Artist finish and hewn-post variant are ordinary component inputs.
    select(member)
    props.caelm_component_joinery = 'hewn_pegged'
    assert bpy.ops.caelmor.stage_joinery() == {'FINISHED'}
    assert bpy.ops.caelmor.regenerate() == {'FINISHED'}
    member = assembly(collection,post_id,role='frame_member')[0]
    assert member.get('caelm_variant') == 'hewn_pegged'
    changed = collection['caelm_source_geometry_hash']
    select(post)
    post.location.y += 1.21
    rejected(bpy.ops.caelmor.opening_guide,'adjoining posts and openings',action='REFRESH')
    assert changed == collection['caelm_source_geometry_hash']
    post.location.y -= 1.21

    select(damage)
    damage.location.y += .40
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    assert damage[GUIDE]['id'] == loss_id
    assert wall_hit(collection,1.5,.80)[1] == 'plaster'
    assert wall_hit(collection,1.9,.80)[1] == 'earthen_daub'
    damage.location.y -= .40
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    scene = bpy.context.scene
    if evidence:
        render(scene,camera,collection,output/'wall-directed.jpg')
    saved_hash = collection['caelm_source_geometry_hash']
    path = output/'wall-features.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
    if evidence:
        render_loss_detail(scene,camera,collection,output/'plaster-reveal-clay.jpg')
    bpy.ops.wm.open_mainfile(filepath=str(path))
    damage = bpy.data.objects['Splash-zone plaster loss']
    collection = damage[HOST]
    assert len(json.loads(collection[SCHEDULE])) == 3
    select(damage)
    assert bpy.ops.caelmor.opening_guide(action='REFRESH') == {'FINISHED'}
    assert collection['caelm_source_geometry_hash'] == saved_hash

    path = output/'wall-features.glb'
    export_building(collection,str(path),construction_metadata=True)
    visual, _ = read_glb(path)
    assert any(f'.guide.{post_id}.member' in n['name'] for n in visual['nodes'])
    assert any(f'.guide.{loss_id}.substrate' in n['name'] for n in visual['nodes'])
    data = json.loads(path.with_suffix('.caelmor.json').read_text(encoding='utf-8'))
    assert data['source_validation']['valid'] and data['collision']['object_count'] == 5
    for name,identifier in ((damage.name,loss_id),('Bearing post guide',post_id)):
        select(bpy.data.objects[name])
        assert bpy.ops.caelmor.opening_guide(action='REMOVE') == {'FINISHED'}
        assert not assembly(collection,identifier)
    assert wall_hit(collection,1.5,.80)[1] == 'plaster'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    assert bpy.ops.import_scene.gltf(filepath=str(path)) == {'FINISHED'}
    assert any(f'.guide.{loss_id}.substrate' in obj.get('caelm_buffer_id','') for obj in bpy.context.scene.objects)
    print('WALL_FEATURE_GUIDES_PASS',data['source_validation']['source_triangles'],data['collision']['object_count'])


if __name__ == '__main__':
    if folder := os.environ.get('CAELMOR_WALL_FEATURE_DIR'):
        output = Path(folder)
        output.mkdir(parents=True,exist_ok=True)
        main(output,bool(os.environ.get('CAELMOR_WALL_FEATURE_RENDER')))
    else:
        with TemporaryDirectory(prefix='wall_features_',dir=ROOT/'dist') as work:
            main(Path(work),False)
