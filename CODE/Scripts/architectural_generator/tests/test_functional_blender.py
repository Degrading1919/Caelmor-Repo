"""Actual-mesh functional circulation, aperture and export-proxy checks."""
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from caelmor_architecture.blender_backend import build,TAG
from caelmor_architecture.model import Settings
from test_world_blender import object_bvh

FUNCTIONS=('SMITHY','MARKET_HALL','STABLE','GATEHOUSE')
REGIONS=('LOWMARK','THORNFELL','MIRE','EMBERHOLT')


class FunctionalMeshTests(unittest.TestCase):
    def test_actual_routes_glass_and_collision_passages(self):
        selected=os.environ.get('CAELM_FUNCTIONS','').split(',')
        unused=set()
        if selected!=[''] and not set(selected).intersection(('SMITHY','MARKET_HALL')):unused.add('function_work.py')
        if selected!=[''] and not set(selected).intersection(('STABLE','GATEHOUSE')):unused.add('function_yard.py')
        source={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (ROOT/'caelmor_architecture').glob('*.py') if p.name not in unused}
        cases=[(f,r) for f in FUNCTIONS for r in REGIONS]
        if selected!=['']:cases=[c for c in cases if c[0] in selected]
        if os.environ.get('CAELM_FUNCTION_PILOT'):
            cases=list(zip(FUNCTIONS,REGIONS))
        reports=[]
        for function,region in cases:
            with self.subTest(function=function,region=region):
                bpy.ops.wm.read_factory_settings(use_empty=True)
                settings=Settings(function=function,region=region,seed=91,detail='MEDIUM',
                                  geometry_mode='EFFICIENT',use_grammar=True,world_aware=True)
                collection,_=build(settings)
                bpy.context.view_layer.update()
                program=json.loads(collection['caelm_functional_program'])
                floor=min(r['base'] for r in program['rooms'])
                dep=bpy.context.evaluated_depsgraph_get()
                trees=[(o,object_bvh(o,dep)) for o in collection.objects if o.get(TAG)]
                visuals=[(o,t) for o,t in trees if not o.get('caelm_collider')]
                glass=[(o,t) for o,t in visuals if o.get('caelm_material')=='glass']
                structure=[(o,t) for o,t in visuals if o.get('caelm_layer')=='structure']
                overlap=[(g.name,s.name) for g,gt in glass for s,st in structure if gt.overlap(st)]
                self.assertFalse(overlap,overlap[:4])
                # Operable door leaves/straps may close service entrances. Their
                # surrounding wall/frame and every integral fixture still count.
                probes=[(o,t) for o,t in trees if not any(str(o.get('caelm_buffer_id','')).endswith(n)
                        for n in ('.facade_doors','.facade_iron'))]
                rays=0
                process_rays=0
                ventilation=program.get('ventilation',{})
                for label in ('hood_inlet','duct','stack'):
                    if label not in ventilation:continue
                    start,end=map(Vector,ventilation[label])
                    direction=end-start;distance=direction.length;direction.normalize()
                    lateral=Vector((0,1,0))
                    second=Vector((1,0,0)) if abs(direction.z)>.9 else Vector((0,0,1))
                    for offset in (Vector((0,0,0)),lateral*.075,-lateral*.075,second*.075,-second*.075):
                        hits=[]
                        for obj,tree in visuals:
                            location,_,_,hit=tree.ray_cast(start+offset,direction,distance)
                            if location is not None:hits.append((obj.name,round(hit,4)))
                        self.assertFalse(hits,(function,region,'exhaust',label,offset,hits[:4]))
                        process_rays+=1
                stair_probes=0
                for station in program['stations']:
                    if '.tread.' not in station['key']:continue
                    b=station['bounds']
                    origin=Vector(((b[0]+b[3])*.5,(b[1]+b[4])*.5,b[5]+.05))
                    hits=[]
                    for obj,tree in visuals:
                        location,_,_,hit=tree.ray_cast(origin,Vector((0,0,1)),1.95)
                        if location is not None:hits.append((obj.name,round(hit,3)))
                    self.assertFalse(hits,(function,region,'stair headroom',station['key'],hits[:5]))
                    stair_probes+=1
                for route in program['routes']:
                    if route['kind'] not in ('human','animal','public','service','material'):continue
                    bounds=route['bounds'];axis=0 if bounds[3]-bounds[0]>=bounds[4]-bounds[1] else 1
                    other=1-axis
                    for lateral in (.2,.5,.8):
                        for rise in (.45,1.2,2.0):
                            z=max(floor,bounds[2])+rise
                            if z>=bounds[5]-.02:continue
                            point=[0.,0.,z]
                            point[axis]=bounds[axis]+.025
                            point[other]=bounds[other]+(bounds[other+3]-bounds[other])*lateral
                            direction=Vector((1,0,0) if axis==0 else (0,1,0))
                            distance=bounds[axis+3]-bounds[axis]-.05
                            hits=[]
                            for obj,tree in probes:
                                location,_,_,hit=tree.ray_cast(Vector(point),direction,distance)
                                if location is not None:hits.append((obj.name,round(hit,3)))
                            self.assertFalse(hits,(function,region,route['key'],point,hits[:5]))
                            rays+=1
                reports.append({'function':function,'region':region,'clearance_rays':rays,
                                'stair_headroom_rays':stair_probes,
                                'exhaust_path_rays':process_rays,
                                'glass_structure_overlaps':len(overlap),
                                'source_geometry_hash':collection['caelm_geometry_hash']})
        current={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (ROOT/'caelmor_architecture').glob('*.py') if p.name not in unused}
        self.assertEqual(current,source,'Source changed during native checks')
        out=ROOT/'evidence'/'function_v06';out.mkdir(parents=True,exist_ok=True)
        name='pilot_mesh_checks.json' if os.environ.get('CAELM_FUNCTION_PILOT') else 'mesh_checks.json'
        if selected!=['']:name='mesh_checks_'+'_'.join(f.lower() for f in selected)+'.json'
        (out/name).write_text(json.dumps({'blender':bpy.app.version_string,'source_sha256':source,
            'cases':reports,'scope':'Actual BVH clearance rays include exported wall/floor proxies. Closed service door leaves are omitted; this is not runtime traversal or exhaustive solid intersection.'},indent=2)+'\n')


if __name__=='__main__':
    sys.argv=[sys.argv[0]]
    unittest.main(verbosity=2)
