"""Native edit protection, deterministic regeneration, export and reopen."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import bpy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from caelmor_architecture.blender_backend import build,export_building,TAG
from caelmor_architecture.model import Settings
from caelmor_architecture.engine import generate,geometry_hash
from tests.test_world_blender import object_bvh
from mathutils import Vector

out=ROOT/'evidence/benchmarks_v08';out.mkdir(parents=True,exist_ok=True)
reports=[]
for function,region in (('SMITHY','LOWMARK'),('GATEHOUSE','THORNFELL')):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s=Settings(function=function,region=region,seed=91,world_aware=True,use_grammar=True,
               detail='MEDIUM',geometry_mode='EFFICIENT')
    collection,_=build(s)
    original_hash=collection['caelm_geometry_hash']
    aperture_rays=0;arch_rays=0
    if function=='GATEHOUSE':
        plan,buffers=generate(s);assert geometry_hash(buffers)==original_hash
        dep=bpy.context.evaluated_depsgraph_get()
        trees=[(o,object_bvh(o,dep)) for o in collection.objects if o.get(TAG)]
        for tower in plan.world_zones[1:]:
            for record in tower.plan.facade_records:
                a,c=tower.plan.edges[record['edge_index']]
                length=((c[0]-a[0])**2+(c[1]-a[1])**2)**.5
                tx,ty=(c[0]-a[0])/length,(c[1]-a[1])/length
                for opening in record['openings']:
                    if opening.get('role')!='arrow_loop':continue
                    center=(opening['s0']+opening['s1'])*.5
                    for zz in (.2,.5,.8):
                        point=Vector((a[0]+tx*center+ty*.4,a[1]+ty*center-tx*.4,
                            opening['z0']+zz*(opening['z1']-opening['z0'])))
                        hits=[o.name for o,t in trees if t.ray_cast(point,Vector((-ty,tx,0)),.85)[0] is not None]
                        assert not hits,hits
                        aperture_rays+=1
        core=plan.world_zones[0];cx=(core.bounds[0]+core.bounds[2])*.5
        for x,clear in ((cx,True),(cx-1.30,False)):
            point=Vector((x,-.55,core.base+2.90+.35))
            hits=[o.name for o,t in trees if t.ray_cast(point,Vector((0,1,0)),core.depth+1.1)[0] is not None]
            assert (not bool(hits))==clear,hits
            arch_rays+=1
    mesh=next(o for o in collection.objects if o.get(TAG) and o.type=='MESH' and
              not o.get('caelm_collider') and o.get('caelm_layer')=='walls')
    key=mesh['caelm_buffer_id'];original=tuple(mesh.data.vertices[0].co)
    mesh['caelm_protected']=True;mesh.data.vertices[0].co.x+=.013
    edited=tuple(mesh.data.vertices[0].co)
    build(s,collection=collection)
    retained=[o for o in collection.objects if o.get('caelm_buffer_id')==key]
    assert len(retained)==1 and retained[0] is mesh
    assert tuple(mesh.data.vertices[0].co)==edited
    mesh['caelm_protected']=False
    build(s,collection=collection)
    rebuilt=next(o for o in collection.objects if o.get('caelm_buffer_id')==key)
    assert tuple(rebuilt.data.vertices[0].co)==original
    assert collection['caelm_geometry_hash']==original_hash
    ids=[o.get('caelm_buffer_id') for o in collection.objects if o.get(TAG) and not o.get('caelm_collider')]
    assert len(ids)==len(set(ids))
    target=out/(function.lower()+'.glb')
    sidecar=Path(export_building(collection,str(target)))
    data=json.loads(sidecar.read_text())
    assert data['settings']['seed']==91 and data['functional_program']['function']==function
    assert any(o.get('functional_role') for o in data['objects'])
    assert all(len(o.data.uv_layers)==2 for o in collection.objects if o.get(TAG) and not o.get('caelm_collider'))
    with tempfile.TemporaryDirectory(prefix='caelmor_benchmark_') as folder:
        saved=Path(folder)/'reopen.blend'
        bpy.ops.wm.save_as_mainfile(filepath=str(saved))
        bpy.ops.wm.open_mainfile(filepath=str(saved))
        reopened=next(c for c in bpy.data.collections if c.get('caelm_geometry_hash')==original_hash)
        assert json.loads(reopened['caelm_settings'])['seed']==91
        assert any(o.get('caelm_buffer_id')==key for o in reopened.objects)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(target))
    imported=[o for o in bpy.context.scene.objects if o.type=='MESH']
    assert imported and all(o.data.uv_layers for o in imported)
    reports.append({'function':function,'region':region,'geometry_hash':original_hash,
        'protected_edit_retained':True,'unprotected_regeneration_restored':True,
        'unique_semantic_ids':True,'two_native_uv_maps':True,'saved_reopen':True,
        'export_reimport':True,'imported_meshes':len(imported),
        'actual_slot_and_collision_aperture_rays':aperture_rays,
        'actual_arch_profile_rays':arch_rays,
        'glb_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
(out/'lifecycle.json').write_text(json.dumps({'blender':bpy.app.version_string,'cases':reports},indent=2)+'\n')
print('BENCHMARK_LIFECYCLE_PASS',len(reports))
