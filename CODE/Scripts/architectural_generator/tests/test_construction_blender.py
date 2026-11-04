"""Native lifecycle, aperture, UV, and export gates for the construction opt-in."""
from dataclasses import replace
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT),str(Path(__file__).resolve().parent)]
import caelmor_architecture as addon
from caelmor_architecture.blender_backend import TAG, build, export_building, load_settings
from caelmor_architecture.engine import generate
from test_condition_export import assert_glb_materials, read_glb
from test_construction_treatments import fixture


def generated(collection):
    return {o['caelm_buffer_id']:o for o in collection.objects
            if o.get(TAG) and not o.get('caelm_collider')}


def signature(collection):
    return sorted((o.get('caelm_world_zone'), [tuple(v.co) for v in o.data.vertices],
                                   [tuple(p.vertices) for p in o.data.polygons])
            for o in collection.objects if o.get('caelm_collider'))


def passage(collection, plan):
    mass = plan.world_zones[0]
    x0,y0,x1,y1 = mass.bounds
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in generated(collection).values():
        if obj.get('caelm_world_zone') != mass.key:
            continue
        tree = BVHTree.FromObject(obj,depsgraph)
        for height in (.30, 1.4, 2.86, 3.25):
            for lateral in (-.45,0.,.45) if height < 3. else (0.,):
                start = Vector(((x0+x1)/2+lateral,y0-.5,mass.base+height))
                start = obj.matrix_world.inverted() @ start
                assert tree.ray_cast(start,Vector((0,1,0)),y1-y0+1)[0] is None, (obj.name,height,lateral)


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon.register()
    s = fixture('THORNFELL','GATEHOUSE', detail='LOW')
    old = replace(s,construction_overrides=None)
    collection, _ = build(old)
    assert 'construction_overrides' not in load_settings(collection)
    props = bpy.context.scene.caelmor_settings
    addon._set_props(props,addon._settings_from_json(load_settings(collection)))
    assert addon._settings_from_props(props).construction_overrides is None
    legacy = generated(collection)
    old_proxy = signature(collection)
    wall = next(o for key,o in legacy.items() if key.endswith('curtain_return.east'))
    wall['caelm_protected'] = True
    wall.data.vertices[0].co.z += .02
    edit = tuple(wall.data.vertices[0].co)
    roof = next(o for key,o in legacy.items() if key.endswith('Split oak shingle courses'))
    custom = bpy.data.materials.new('Reviewed artist override')
    roof.data.materials[0] = custom
    finish = bpy.data.materials.new('Painted stone fixture')
    gate = next(key for key in legacy if key.endswith('curtain_return.west'))
    baseline_plan, _ = generate(s)
    west = next(c.component_id for c in baseline_plan.construction_components.values()
                if c.component_id.endswith('/curtain_return') and 'west' in c.component_id)
    s = replace(s, construction_overrides={'by_component': {west:{'finish':'material:'+finish.name}}})
    addon._set_props(props,s)
    assert addon._settings_from_props(props).construction_overrides == s.construction_overrides
    invalid = replace(s,construction_overrides={'by_role':{'roof_cover':{'substrate':'structural_wood'}}})
    for settings, scope in ((invalid, None),(s,'ROOF')):
        try:
            build(settings,collection=collection,layers=scope)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid or partial plan change was accepted')
        assert generated(collection) == legacy

    build(s,collection=collection)
    live = generated(collection)
    assert live[wall['caelm_buffer_id']] == wall
    assert tuple(wall.data.vertices[0].co) == edit
    assert json.loads(collection['caelm_construction_conflicts']) == [wall['caelm_buffer_id']]
    assert live[gate].data.materials[0] == finish
    assert live[next(k for k,o in legacy.items() if k.endswith('Split oak shingle courses'))].data.materials[0] == custom
    assert signature(collection) == old_proxy
    assert load_settings(collection)['construction_overrides'] == s.construction_overrides
    for obj in live.values():
        if obj.get('caelm_component_role'):
            assert 'UV0_Metric' in obj.data.uv_layers and 'UV1_Lightmap' in obj.data.uv_layers
            if obj.data.materials[0].get('caelm_atlas_revision'):
                assert 'UV2_Surface' in obj.data.uv_layers
    passage(collection,baseline_plan)
    del legacy

    # A finish supplied by construction settings must be replaceable as a
    # finish. The separately replaced artist slot must survive scoped refresh.
    build(s,collection=collection,layers='ROOF')
    assert any(o.data.materials[0]==custom for o in generated(collection).values())
    with TemporaryDirectory(prefix='construction_test_',dir=ROOT/'dist') as tmp:
        target = Path(tmp)/'treatments.glb'
        sidecar = export_building(collection,str(target),construction_metadata=True)
        metadata = json.loads(Path(sidecar).read_text(encoding='utf-8'))
        assert metadata['version']==1 and metadata['settings']['construction_overrides']==s.construction_overrides
        assert any(row.get('component_role')=='wall_body' and row.get('finish')=='material:'+finish.name
                   for row in metadata['objects'])
        assert any(row['protected'] and 'treatment' not in row for row in metadata['objects'])
        doc,binary = read_glb(target)
        report = assert_glb_materials(doc,binary)
        assert target.with_suffix('.collision.glb').is_file()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(target))
        imported = [o for o in bpy.context.scene.objects if o.type=='MESH']
        assert imported and any(len(o.data.uv_layers)>=3 for o in imported)
        print('CONSTRUCTION_NATIVE_PASS',len(imported),report)


if __name__ == '__main__':
    main()

