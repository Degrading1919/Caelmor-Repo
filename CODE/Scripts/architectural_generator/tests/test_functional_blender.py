"""Actual-mesh functional circulation, aperture and export-proxy checks."""
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
from contextlib import nullcontext
from unittest.mock import patch

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
        if os.environ.get('CAELM_CASES'):
            requested={tuple(c.split(':')) for c in os.environ['CAELM_CASES'].split(',')}
            cases=[c for c in cases if c in requested]
            self.assertEqual(set(cases),requested,'Unsupported native fixture case')
        if os.environ.get('CAELM_FUNCTION_PILOT'):
            cases=list(zip(FUNCTIONS,REGIONS))
        reports=[]
        geometry_only=os.environ.get('CAELM_GEOMETRY_ONLY')=='1'
        seeds=tuple(int(seed) for seed in os.environ.get('CAELM_SEEDS','91').split(','))
        for function,region,seed in ((f,r,s) for f,r in cases for s in seeds):
            with self.subTest(function=function,region=region,seed=seed):
                bpy.ops.wm.read_factory_settings(use_empty=True)
                settings=Settings(function=function,region=region,seed=seed,detail='MEDIUM',
                                  geometry_mode='EFFICIENT',use_grammar=True,world_aware=True,
                                  crafted_curves=os.environ.get('CAELM_CRAFTED_CURVES')=='1',
                                  seed_massing=os.environ.get('CAELM_SEED_MASSING')=='1')
                atlas = (patch('caelmor_architecture.surface_atlas.apply_surfaces', return_value=[])
                         if geometry_only else nullcontext())
                with atlas:
                    collection,_=build(settings)
                bpy.context.view_layer.update()
                program=json.loads(collection['caelm_functional_program'])
                floor=min(r['base'] for r in program['rooms'])
                dep=bpy.context.evaluated_depsgraph_get()
                trees=[(o,object_bvh(o,dep)) for o in collection.objects if o.get(TAG)]
                visuals=[(o,t) for o,t in trees if not o.get('caelm_collider')]
                glass=[(o,t) for o,t in visuals if o.get('caelm_material')=='glass']
                # New integral fixtures (portal shoulders, stall bents, etc.)
                # must not evade the glazing gate by living in the detail layer.
                structure=[(o,t) for o,t in visuals if o.get('caelm_layer')=='structure'
                           or o.get('caelm_functional_role')]
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
                        rises=sorted({.45,1.2,2.0,round(bounds[5]-max(floor,bounds[2])-.05,6)})
                        for rise in rises:
                            if rise<=0:continue
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
                arch_probes=0
                if settings.crafted_curves and (function,region)==('GATEHOUSE','THORNFELL'):
                    x0,y0,z0,x1,y1,spring=next(r['bounds'] for r in program['routes']
                                               if r['key']=='gatehouse_open_through_passage')
                    x=(x0+x1)*.5
                    for group in (visuals,[(o,t) for o,t in trees if o.get('caelm_collider')]):
                        self.assertTrue(group)
                        for offset,clear in ((.65,True),(.92,False)):
                            start=Vector((x,y0-.6,spring+offset))
                            hits=[obj.name for obj,tree in group
                                  if tree.ray_cast(start,Vector((0,1,0)),y1-y0+1.2)[0] is not None]
                            self.assertEqual(not hits,clear,(offset,hits[:5]))
                            arch_probes+=1
                reports.append({'function':function,'region':region,'seed':seed,'clearance_rays':rays,
                                'stair_headroom_rays':stair_probes,
                                'arch_aperture_rays':arch_probes,
                                'exhaust_path_rays':process_rays,
                                'glass_structure_overlaps':len(overlap),
                                'glazing_opaque_objects_tested':len(structure),
                                'source_geometry_hash':collection['caelm_geometry_hash']})
        current={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (ROOT/'caelmor_architecture').glob('*.py') if p.name not in unused}
        self.assertEqual(current,source,'Source changed during native checks')
        output_name=os.environ.get('CAELM_FUNCTION_OUTPUT','function_v06')
        if output_name in ('.','..') or Path(output_name).name!=output_name or '/' in output_name or '\\' in output_name:
            raise ValueError('Functional output must be a single evidence folder')
        out=ROOT/'evidence'/output_name;out.mkdir(parents=True,exist_ok=True)
        name='pilot_mesh_checks.json' if os.environ.get('CAELM_FUNCTION_PILOT') else 'mesh_checks.json'
        if selected!=['']:name='mesh_checks_'+'_'.join(f.lower() for f in selected)+'.json'
        if os.environ.get('CAELM_CASES'):name='benchmark_mesh_checks.json'
        (out/name).write_text(json.dumps({'blender':bpy.app.version_string,'source_sha256':source,
            'cases':reports,'surface_atlas_baked':not geometry_only,'scope':'Actual BVH clearance rays include exported wall/floor proxies. Glazing intersections include structure and all integral functional fixtures, including detail-layer pieces. Closed service door leaves are omitted from circulation probes; this is not runtime traversal or exhaustive solid intersection.'},indent=2)+'\n')


if __name__=='__main__':
    sys.argv=[sys.argv[0]]
    unittest.main(verbosity=2)
