"""Blender controls, shared fields, finish and protection transaction checks."""
from dataclasses import replace
import sys
from pathlib import Path

import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
import caelmor_architecture as addon
from caelmor_architecture.blender_backend import build, load_settings
from test_construction_depth import case


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon.register()
    props=bpy.context.scene.caelmor_settings
    base=replace(case('SMITHY'),detail='LOW')
    addon._set_props(props,base)
    bpy.ops.caelmor.generate()
    collection=next(c for c in bpy.data.collections if c.get('caelm_build'))
    source=next(o for o in collection.objects if
                o.get('caelm_buffer_id','').endswith('Split oak shingle courses'))
    source['caelm_protected']=True
    source.data.vertices[0].co.z+=.006
    saved=tuple(source.data.vertices[0].co)
    props.caelm_assembly_roof_depth='HYBRID'
    hybrid=addon._settings_from_props(props)
    try:
        build(hybrid,collection=collection)
    except ValueError as exc:
        assert 'unprotect' in str(exc)
    else:
        raise AssertionError('Protected cover was replaced by a mapped field')
    assert tuple(source.data.vertices[0].co)==saved
    source['caelm_protected']=False
    manual=bpy.data.materials.new('Reviewed manual roof slot')
    source.data.materials[0]=manual
    build(hybrid,collection=collection)
    fields=[o for o in collection.objects if o.get('caelm_field_family')]
    assert len(fields)==2
    assert any(o.data.materials[0]==manual for o in fields)
    assert bpy.ops.caelmor.load_settings()=={'FINISHED'}
    assert props.caelm_assembly_roof_depth=='HYBRID'
    assert load_settings(collection)['construction_overrides']['by_role']['roof_cover']['representation']=='HYBRID'

    standalone,_=build(hybrid)
    fields=[o for o in standalone.objects if o.get('caelm_field_family')]
    assert len(fields)==2 and fields[0].data.materials[0]==fields[1].data.materials[0]
    for obj in fields:
        assert all(name in obj.data.uv_layers for name in ('UV0_Metric','UV1_Lightmap','UV2_Surface'))
    for stock,family in (('slate','slate'),('fired_clay','clay')):
        settings=replace(case('SMITHY','HYBRID',stock),detail='LOW')
        other,_=build(settings)
        mapped=[o for o in other.objects if o.get('caelm_field_family')]
        assert mapped and all(o.data.materials[0].get('caelm_shared_field')==family for o in mapped)
    named=bpy.data.materials.new('Named tile finish')
    opts=hybrid.construction_overrides
    opts['by_role']['roof_cover']['finish']='material:'+named.name
    finished,_=build(hybrid)
    named_fields=[o for o in finished.objects if o.get('caelm_field_family')]
    assert named_fields and all(o.data.materials[0]==named for o in named_fields)
    print('CONSTRUCTION_DEPTH_NATIVE_PASS')


if __name__=='__main__':
    main()
