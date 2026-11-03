"""Actual-mesh checks for new household projections, across wealth tiers."""
import json
import os
import hashlib
from pathlib import Path
import sys
import unittest
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_world_blender import object_bvh
from caelmor_architecture.model import Settings
from caelmor_architecture.blender_backend import build,TAG


class HouseholdMeshTests(unittest.TestCase):
    def test_new_projections_leave_glass_and_doorways_clear(self):
        cases=[(r,w,'COTTAGE') for r in ('LOWMARK','THORNFELL','MIRE','EMBERHOLT')
               for w in ('MODEST','ESTABLISHED','AFFLUENT')]
        cases.extend([('MIRE','ESTABLISHED','FARMHOUSE'),('EMBERHOLT','AFFLUENT','SHOP')])
        selected=os.environ.get('CAELM_TEST_REGIONS','').split(',')
        if selected!=['']:cases=[c for c in cases if c[0] in selected]
        records=[]
        for region,wealth,function in cases:
            with self.subTest(region=region,wealth=wealth,function=function):
                bpy.ops.wm.read_factory_settings(use_empty=True)
                settings=Settings(seed=91,region=region,wealth=wealth,function=function,
                                  detail='MEDIUM',geometry_mode='EFFICIENT',world_aware=True,use_grammar=True)
                collection,_=build(settings)
                bpy.context.view_layer.update()
                from caelmor_architecture.engine import generate
                plan,_=generate(settings)
                dep=bpy.context.evaluated_depsgraph_get()
                objects=[o for o in collection.objects if o.get(TAG) and not o.get('caelm_collider')]
                trees=[(o,object_bvh(o,dep)) for o in objects]
                glass=[(o,t) for o,t in trees if o.get('caelm_material')=='glass']
                structure=[(o,t) for o,t in trees if o.get('caelm_layer')=='structure']
                intersections=[(g.name,f.name) for g,gt in glass for f,ft in structure if gt.overlap(ft)]
                self.assertFalse(intersections,intersections[:4])
                rays=0;doors=0
                for record in plan.facade_records:
                    a,b=plan.edges[record['edge_index']]
                    tangent=(Vector((b[0]-a[0],b[1]-a[1],0))).normalized()
                    normal=Vector((tangent.y,-tangent.x,0))
                    for opening in record['openings']:
                        is_window=opening['kind']=='window'
                        if opening.get('role') in ('passage_entry','passage_exit'):continue
                        for horizontal,vertical in ((.5,.5),(.2,.75),(.8,.75)):
                            station=opening['s0']+(opening['s1']-opening['s0'])*horizontal
                            point=Vector((a[0],a[1],opening['z0']+(opening['z1']-opening['z0'])*vertical))+tangent*station
                            origin=point-normal*.50 if is_window else point+normal*.85
                            direction=normal if is_window else -normal
                            hits=[]
                            for obj,tree in trees:
                                location,_,_,distance=tree.ray_cast(origin,direction,1.30)
                                if location is not None:hits.append((distance,obj))
                            self.assertTrue(hits,(region,wealth,opening))
                            obj=min(hits,key=lambda h:h[0])[1]
                            if is_window:
                                self.assertEqual(obj.get('caelm_material'),'glass',
                                                 (region,wealth,record['construction_zone'],obj.name))
                            else:
                                self.assertTrue(any(name in obj.get('caelm_buffer_id','')
                                                    for name in ('facade_doors','facade_iron')),
                                                (region,wealth,record['construction_zone'],obj.name))
                                doors+=1
                            rays+=1
                records.append({'region':region,'wealth':wealth,'function':function,
                                'aperture_rays':rays,'door_rays':doors,'glass_structure_intersections':len(intersections)})
        name=('v05_targeted_mesh_checks_'+ '_'.join(s.lower() for s in selected)+'.json'
              if selected!=[''] else 'v05_household_mesh_checks.json')
        result={'cases':records,'blender':bpy.app.version_string,
                'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (ROOT/'caelmor_architecture').glob('*.py')}}
        (ROOT/'evidence'/name).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    sys.argv=[sys.argv[0]]
    unittest.main(verbosity=2)
