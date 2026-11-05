"""Target boundary ownership, capped posts, sparse sections and mapped skins."""
import sys
from pathlib import Path
import bpy
import bmesh
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from caelmor_architecture.model import Settings, make_plan
from caelmor_architecture.geometry import MeshBuffer
from caelmor_architecture.blender_backend import _mesh_object, build
from caelmor_architecture.floor_backend import partition, preview
from test_construction_treatments import fixture


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s=Settings(floors=2,detail='LOW')
    plan=make_plan(s)
    cut=plan.foundation_height+s.floor_height
    stage=bpy.data.collections.new('boundary cases')
    bpy.context.scene.collection.children.link(stage)
    beam=MeshBuffer('continuous post')
    beam.box((0,0,cut),(.3,.3,4))
    plane=MeshBuffer('floor plane',layer='structure',topology='SURFACE')
    plane.indexed([(0,0,cut),(1,0,cut),(1,1,cut),(0,1,cut)],[(0,1,2,3)])
    flue=MeshBuffer('semantic hollow flue',structural_role='supported_hollow_masonry_flue')
    flue.box((2,0,cut),(.4,.4,4))
    for buffer in (beam,plane,flue):stage.objects.link(_mesh_object(buffer,{},'test',plan))
    partition(stage,plan)
    parts=list(stage.objects)
    assert len(parts)==4
    horizontal=next(o for o in parts if o['caelm_source_buffer_id']=='floor plane')
    assert horizontal['caelm_floor_index']==1
    assert next(o for o in parts if o['caelm_source_buffer_id']=='semantic hollow flue')['caelm_visibility']=='ALWAYS'
    for obj in parts:
        if obj['caelm_source_buffer_id']!='continuous post':continue
        bm=bmesh.new();bm.from_mesh(obj.data)
        assert all(e.is_manifold for e in bm.edges),'cut post has an open section'
        caps=[f for f in bm.faces if all(abs(v.co.z-cut)<1e-5 for v in f.verts)]
        assert len(caps)==1
        assert caps[0].normal.z > .99 if obj['caelm_floor_index']==0 else caps[0].normal.z < -.99
        bm.free()
        assert all(tuple(color.color)==(1,1,1,1) for color in obj.data.color_attributes['CaelmorTint'].data)
    # The field's shared materials and UV names must survive final partition.
    settings=fixture(detail='LOW', construction_overrides={'by_role':{
        'roof_cover':{'representation':'HYBRID'}}})
    building,_=build(settings)
    fields=[o for o in building.objects if o.get('caelm_field_family')]
    assert fields
    assert all('UV2_Surface' in o.data.uv_layers and o.get('caelm_floor_contract')==1 for o in fields)
    preview(building,0);preview(building,-1)
    from dataclasses import replace
    field=fields[0]
    custom=bpy.data.materials.new('Migration slot override')
    field.data.materials[0]=custom
    ids={o.get('caelm_buffer_id') for o in building.objects}
    try:build(replace(settings,floor_separation=False),collection=building)
    except ValueError as exc:assert 'material slots' in str(exc)
    else:raise AssertionError('Merging floor-specific finishes silently lost artist overrides')
    assert field.data.materials[0]==custom and ids=={o.get('caelm_buffer_id') for o in building.objects}
    print('FLOOR EDGES: boundary, capped solid, neutral cap colors, semantic continuity and HYBRID UV checks passed')


if __name__=='__main__':main()
