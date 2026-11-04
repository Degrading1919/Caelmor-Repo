"""Exercise Blender authoring, saved controls, and the exported library provenance."""
from dataclasses import replace
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import caelmor_architecture as addon
from caelmor_architecture.blender_backend import TAG, load_settings
from test_condition_export import assert_glb_materials, read_glb
from test_construction_library import PRESETS, overrides
from test_construction_treatments import fixture


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon.register()
    props=bpy.context.scene.caelmor_settings
    addon._set_props(props,fixture(detail='LOW'))
    assert addon._settings_from_props(props).construction_overrides == {}
    for name, choice in PRESETS['render_slate'].items():
        setattr(props,'caelm_assembly_'+name,choice)
    assert addon._settings_from_props(props).construction_overrides==overrides('render_slate')
    finish=bpy.data.materials.new('Smithy artist render')
    props.caelm_edit_finish=True
    props.caelm_finish_role='wall_infill'
    props.caelm_finish_material=finish
    assert bpy.ops.caelmor.generate()=={'FINISHED'}
    collection=next(c for c in bpy.data.collections if c.get('caelm_build'))
    data=load_settings(collection)
    assert data['construction_overrides']['by_role']['wall_infill']['finish']=='material:'+finish.name
    assert bpy.ops.caelmor.load_settings()=={'FINISHED'}
    assert props.caelm_assembly_cover=='slate'
    assert props.caelm_assembly_supports=='squared'
    assert addon._settings_from_props(props).construction_overrides==data['construction_overrides']
    objs=[o for o in collection.objects if o.get(TAG) and not o.get('caelm_collider')]
    assert any(o.get('caelm_variant')=='level_course' for o in objs)
    assert any(o.get('caelm_variant')=='squared_housed' for o in objs)
    assert all(o.data.materials[0]==finish for o in objs if o.get('caelm_component_role')=='wall_infill')
    with TemporaryDirectory(prefix='library_test_',dir=ROOT/'dist') as directory:
        path=Path(directory)/'smithy.glb'
        assert bpy.ops.caelmor.export(filepath=str(path),construction_metadata=True)=={'FINISHED'}
        report=json.loads(path.with_suffix('.caelmor.json').read_text(encoding='utf-8'))
        assert report['version']==1
        assert any(o.get('variant')=='squared_housed' for o in report['objects'])
        assert any(o.get('substrate')=='slate' for o in report['objects'])
        doc,binary=read_glb(path)
        stats=assert_glb_materials(doc,binary)
        assert path.with_suffix('.collision.glb').exists()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(path))
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
        assert meshes and any(len(o.data.uv_layers)>=3 for o in meshes)
        print('CONSTRUCTION_LIBRARY_NATIVE_PASS',len(meshes),stats['materials_with_maps'])


if __name__=='__main__':
    main()
