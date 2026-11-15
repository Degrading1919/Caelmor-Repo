"""Native Lowmark Cottage authoring, regeneration and delivery check."""
import json
import math
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

import caelmor_architecture as addon
from caelmor_architecture.blender_backend import build, load_settings
from caelmor_architecture.blockout import fit
from render_evidence import point_camera, setup_scene
from test_condition_export import accessor_values, match_uv_values, read_glb


def select(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def scene_material(name, color, timber=False):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = .72
    if not timber:
        return material
    uv = nodes.new('ShaderNodeUVMap')
    uv.uv_map = 'UV0_Metric'
    normal = nodes.new('ShaderNodeNormalMap')
    normal.uv_map = uv.uv_map
    links.new(normal.outputs['Normal'], shader.inputs['Normal'])
    for channel in ('Base Color', 'Normal'):
        image = bpy.data.images.new(name + ' ' + channel, 32, 32, alpha=False)
        if channel == 'Normal':
            image.colorspace_settings.name = 'Non-Color'
        pixels = []
        for y in range(32):
            for x in range(32):
                grain = math.sin((x + .4 * math.sin(y * math.tau / 32)) * math.tau / 4)
                rgb = tuple(c * (1 + .06 * grain) for c in color) if channel == 'Base Color' else (.5 + .025 * grain, .5, 1.)
                pixels.extend((*rgb, 1.))
        image.pixels.foreach_set(pixels)
        image.pack()
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = image
        links.new(uv.outputs['UV'], texture.inputs['Vector'])
        socket = shader.inputs[channel] if channel == 'Base Color' else normal.inputs['Color']
        links.new(texture.outputs['Color'], socket)
    return material


def by_role(collection, name):
    return [obj for obj in collection.objects if obj.get('caelm_component_role') == name]


def root_of(collection):
    return next(obj for obj in collection.objects if obj.get('caelm_anchor'))


def check_box_rejected(props, source):
    settings = addon._settings_from_props(props)
    source.rotation_euler.x = .08
    bpy.context.view_layer.update()
    try:
        fit(settings, source)
    except ValueError as exc:
        assert 'upright' in str(exc)
    else:
        raise AssertionError('Accepted a tilted proxy')
    source.rotation_euler.x = 0


def render_view(scene, camera, anchor, target, filename):
    scene.render.resolution_x = 920
    scene.render.resolution_y = 680
    scene.render.image_settings.file_format = 'JPEG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.quality = 93
    camera.data.ortho_scale = 14.5
    point_camera(camera, anchor.matrix_world @ (target + Vector((-9, -14, 10))),
                 anchor.matrix_world @ target)
    scene.render.filepath = str(filename)
    bpy.ops.render.render(write_still=True)


def main(directory, evidence=None):
    scene, camera, _, _, ground = setup_scene()
    props = scene.caelmor_settings
    props.caelm_function = 'COTTAGE'
    props.caelm_context = 'BROOKHOLLOW'  # Ordinary contextual width scaling must leave the box alone.
    props.caelm_floors = 1
    props.caelm_detail = 'MEDIUM'
    bpy.ops.mesh.primitive_cube_add(size=2, location=(13, -7, 1.75))
    source = bpy.context.object
    source.name = 'Cottage source box'
    source.rotation_euler.z = .41
    source.scale = (4.155, 3.125, 1.675)
    source.display_type = 'WIRE'
    source.hide_render = True
    original = [tuple(v.co) for v in source.data.vertices]
    check_box_rejected(props, source)
    bpy.context.view_layer.update()
    lower = source.matrix_world @ Vector((-1, -1, -1))
    assert bpy.ops.caelmor.fit_blockout() == {'FINISHED'}
    collection = addon._active_build(bpy.context)
    anchor = root_of(collection)
    assert collection['caelm_blockout_source'] == source
    assert (anchor.location - lower).length < 1e-5
    assert abs(anchor.rotation_euler.z - .41) < 1e-5
    assert list(anchor.scale) == [1., 1., 1.]
    data = load_settings(collection)
    assert data['fit_blockout'] and abs(data['width'] - 8.31) < 2e-6
    assert abs(data['depth'] - 6.25) < 2e-6 and abs(data['floor_height'] + .45 - 3.35) < 2e-6
    volumes = json.loads(collection['caelm_construction_zones'])
    assert len(volumes) == 1 and volumes[0]['key'] == 'lowmark_main_hall', volumes
    assert abs(volumes[0]['eave'] - 3.35) < 2e-6
    assert [tuple(v.co) for v in source.data.vertices] == original
    initial_hash = collection['caelm_source_geometry_hash']
    if evidence:
        ground.location.z = lower.z - .08
        render_view(scene, camera, anchor, Vector((4.15, 3.125, 2.4)), evidence / 'cottage-default.jpg')

    frame = by_role(collection, 'frame_member')[0]
    frame_id = frame['caelm_component_id']
    frame_buffer = frame['caelm_buffer_id']
    initial_uv = [tuple(loop.uv) for loop in frame.data.uv_layers['UV0_Metric'].data]
    support = next(obj for obj in by_role(collection, 'roof_support') if obj['caelm_treatment'] == 'structural_timber')
    support_id = support['caelm_component_id']
    support_hash = support['caelm_component_source_hash']
    keep = next(obj for obj in collection.objects if obj.get('caelm_layer') == 'windows')
    select(keep)
    assert bpy.ops.caelmor.protect_selected() == {'FINISHED'}
    foundation = scene_material('Pilot warm stone', (.23, .20, .16))
    timber = scene_material('Pilot worked oak', (.24, .128, .067), timber=True)
    props.caelm_finish_scope = 'ROLE'
    props.caelm_finish_role = 'plinth'
    props.caelm_finish_material = foundation
    assert bpy.ops.caelmor.stage_finish() == {'FINISHED'}
    select(frame)
    props.caelm_finish_scope = 'COMPONENT'
    props.caelm_finish_material = timber
    props.caelm_finish_rotation = '90'
    assert bpy.ops.caelmor.stage_finish() == {'FINISHED'}
    select(support)
    props.caelm_component_joinery = 'squared_housed' if support.get('caelm_variant') != 'squared_housed' else 'hewn_pegged'
    selected_variant = props.caelm_component_joinery
    assert bpy.ops.caelmor.stage_joinery() == {'FINISHED'}
    assert bpy.ops.caelmor.regenerate() == {'FINISHED'}
    assert keep.name in collection.objects and keep.get('caelm_protected')
    assert collection['caelm_source_geometry_hash'] != initial_hash
    assert all(obj.data.materials[0] == foundation for obj in by_role(collection, 'plinth'))
    fresh_frame = next(obj for obj in collection.objects if obj.get('caelm_buffer_id') == frame_buffer)
    assert fresh_frame.data.materials[0] == timber and fresh_frame['caelm_uv_rotation'] == '90'
    new_uv = [tuple(loop.uv) for loop in fresh_frame.data.uv_layers['UV0_Metric'].data]
    assert new_uv == [(-v, u) for u, v in initial_uv]
    assert not any(obj.data.materials[0] == timber for obj in by_role(collection, 'roof_support'))
    next_support = next(obj for obj in by_role(collection, 'roof_support') if obj['caelm_component_id'] == support_id)
    assert next_support['caelm_variant'] == selected_variant
    assert next_support['caelm_component_source_hash'] != support_hash
    saved = load_settings(collection)
    edited_hash = collection['caelm_source_geometry_hash']
    assert saved['construction_overrides']['by_component'][frame_id]['finish'] == 'material:' + timber.name
    select(fresh_frame)
    assert bpy.ops.caelmor.stage_finish(clear=True) == {'FINISHED'}
    assert frame_id not in addon._settings_from_props(props).construction_overrides['by_component']
    assert bpy.ops.caelmor.load_settings() == {'FINISHED'}
    assert bpy.ops.caelmor.regenerate(scope='ROOF') == {'FINISHED'}
    assert load_settings(collection) == saved
    assert collection['caelm_source_geometry_hash'] == edited_hash
    if evidence:
        render_view(scene, camera, anchor, Vector((4.15, 3.125, 2.4)), evidence / 'cottage-directed.jpg')

    source.location.x += 1.2
    source.rotation_euler.z -= .22
    bpy.context.view_layer.update()
    lower = source.matrix_world @ Vector((-1, -1, -1))
    assert bpy.ops.caelmor.fit_blockout(refit=True) == {'FINISHED'}
    assert (anchor.location - lower).length < 1e-5 and abs(anchor.rotation_euler.z - .19) < 1e-5
    assert load_settings(collection) == saved
    assert [tuple(v.co) for v in source.data.vertices] == original
    assert keep.name in collection.objects and keep.get('caelm_protected')
    source.scale.x += .25
    bpy.context.view_layer.update()
    fitted, placement = fit(addon._settings_from_json(saved), source)
    try:
        build(fitted, collection=collection, placement=placement)
    except ValueError as exc:
        assert 'protected section' in str(exc)
    else:
        raise AssertionError('Resizing should report a conflict with the protected window section')
    assert load_settings(collection) == saved
    assert (anchor.location - lower).length < 1e-5
    select(keep)
    assert bpy.ops.caelmor.protect_selected() == {'FINISHED'}
    assert bpy.ops.caelmor.fit_blockout(refit=True) == {'FINISHED'}
    assert abs(load_settings(collection)['width'] - 8.81) < 2e-6
    path = directory / 'blockout-cottage.glb'
    native = next(obj for obj in collection.objects if obj.get('caelm_buffer_id') == frame_buffer)
    native_world = [native.matrix_world @ v.co for v in native.data.vertices]
    assert bpy.ops.caelmor.export(filepath=str(path), construction_metadata=True) == {'FINISHED'}
    doc, binary = read_glb(path)
    sidecar = json.loads(path.with_suffix('.caelmor.json').read_text(encoding='utf-8'))
    assert 'fit_blockout' not in sidecar['settings'] and sidecar['version'] == 1
    assert 'floor_presentation' in sidecar and sidecar['source_validation']['valid']
    assert all(node['name'] != source.name for node in doc['nodes'])
    node = next(node for node in doc['nodes'] if node.get('extras', {}).get('caelm_buffer_id') == frame_buffer)
    primitive = doc['meshes'][node['mesh']]['primitives'][0]
    exported = doc['materials'][primitive['material']]
    assert exported['name'] == timber.name and 'normalTexture' in exported
    assert 'baseColorTexture' in exported['pbrMetallicRoughness']
    assert exported['normalTexture'].get('texCoord', 0) == 0
    coords = accessor_values(doc, binary, primitive['attributes']['TEXCOORD_0'])
    assert not match_uv_values([(u, 1-v) for u, v in coords], native.data.uv_layers['UV0_Metric'])[0]
    collision, _ = read_glb(path.with_suffix('.collision.glb'))
    assert len(collision['meshes']) == sidecar['collision']['object_count']
    blend = directory / 'blockout-cottage.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.wm.open_mainfile(filepath=str(blend))
    collection = next(c for c in bpy.data.collections if c.get('caelm_build'))
    assert collection['caelm_blockout_source'] == bpy.data.objects['Cottage source box']
    assert bpy.ops.caelmor.load_settings() == {'FINISHED'}
    assert bpy.ops.caelmor.regenerate(scope='ROOF') == {'FINISHED'}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    assert bpy.ops.import_scene.gltf(filepath=str(path)) == {'FINISHED'}
    reimported = next(obj for obj in bpy.context.scene.objects if obj.get('caelm_buffer_id') == frame_buffer)
    reimported_world = [reimported.matrix_world @ v.co for v in reimported.data.vertices]
    for axis in range(3):
        for bound in (min, max):
            assert abs(bound(v[axis] for v in native_world) - bound(v[axis] for v in reimported_world)) < 2e-5
    assert reimported.data.materials[0].name == exported['name']
    print('BLOCKOUT_AUTHORING_PASS', sidecar['source_validation'], 'collision meshes', len(collision['meshes']))


if __name__ == '__main__':
    if out := os.environ.get('CAELMOR_BLOCKOUT_CHECK_DIR'):
        output = Path(out)
        output.mkdir(parents=True, exist_ok=True)
        main(output, output if os.environ.get('CAELMOR_BLOCKOUT_RENDER') else None)
    else:
        with TemporaryDirectory(prefix='blockout_', dir=ROOT / 'dist') as temp:
            main(Path(temp))
