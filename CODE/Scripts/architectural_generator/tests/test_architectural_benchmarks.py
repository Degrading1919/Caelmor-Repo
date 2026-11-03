"""Two-case art-pass invariants, adversarial openings and preservation controls."""
from pathlib import Path
import json
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from caelmor_architecture.engine import generate,validate,geometry_hash
from caelmor_architecture.model import Settings
from test_world import _ray_hits

CASES=(('SMITHY','LOWMARK'),('GATEHOUSE','THORNFELL'))

class ArchitecturalBenchmarks(unittest.TestCase):
    def settings(self,f,r,**kw):
        return Settings(function=f,region=r,seed=kw.pop('seed',91),detail=kw.pop('detail','MEDIUM'),
                        geometry_mode=kw.pop('geometry_mode','EFFICIENT'),
                        world_aware=True,use_grammar=True,**kw)

    def test_two_compositions_are_valid_and_have_distinct_roof_hierarchies(self):
        for f,r in CASES:
            p,b=generate(self.settings(f,r));v=validate(p,b)
            self.assertTrue(v['valid'],v['errors'][:6])
            roofs=[m.plan.roof_mode for m in p.world_zones]
            self.assertEqual(roofs,['GABLE','SHED'] if f=='SMITHY' else ['GABLE','HIP','HIP'])
            self.assertGreater(p.world_zones[0].eave,p.world_zones[1].eave)

    def test_actual_arch_cuts_wall_and_has_solid_spandrels(self):
        p,b=generate(self.settings('GATEHOUSE','THORNFELL'))
        m=p.world_zones[0];cx=(m.bounds[0]+m.bounds[2])*.5
        spring=m.base+2.9
        self.assertTrue(m.plan.facade_records[0]['openings'][0].get('arch'))
        # Inside the curved opening, above the spring: must be real air through
        # the whole passage. Beside it at the same height must remain masonry.
        for x,clear in ((cx,True),(cx-1.30,False)):
            hits=_ray_hits((x,-.55,spring+.35),(0,1,0),m.depth+1.1,b)
            self.assertEqual(not bool(hits),clear,(x,[(t,buf.name) for t,buf in hits[:3]]))
        self.assertAlmostEqual(m.plan.passage_geometry['clear_height'],2.9)

    def test_seed_repeat_and_required_identity_survive_detail_and_geometry_modes(self):
        for f,r in CASES:
            hashes=[]
            for seed in (17,91,408):
                s=self.settings(f,r,seed=seed)
                p,b=generate(s);self.assertTrue(validate(p,b)['valid'])
                h=geometry_hash(b);hashes.append(h)
                self.assertEqual(h,geometry_hash(generate(s)[1]))
            self.assertGreater(len(set(hashes)),1)
            for detail,mode in (('LOW','SOLID'),('HIGH','EFFICIENT')):
                p,b=generate(self.settings(f,r,detail=detail,geometry_mode=mode))
                self.assertTrue(validate(p,b)['valid'])
                self.assertTrue(p.functional_program['routes'])

    def test_defensive_slots_are_real_apertures_not_discarded_labels(self):
        p,b=generate(self.settings('GATEHOUSE','THORNFELL'))
        for tower in p.world_zones[1:]:
            loops=[]
            for record in tower.plan.facade_records:
                a,c=tower.plan.edges[record['edge_index']]
                length=((c[0]-a[0])**2+(c[1]-a[1])**2)**.5
                tx,ty=(c[0]-a[0])/length,(c[1]-a[1])/length
                for o in record['openings']:
                    if o.get('role')!='arrow_loop':continue
                    loops.append(o)
                    s=(o['s0']+o['s1'])*.5
                    start=(a[0]+tx*s+ty*.4,a[1]+ty*s-tx*.4,(o['z0']+o['z1'])*.5)
                    hits=_ray_hits(start,(-ty,tx,0),.85,b)
                    self.assertFalse(hits,[(t,buf.name) for t,buf in hits[:4]])
            self.assertEqual(len(loops),6)

    def test_guard_hall_has_supported_doors_from_both_stair_landings(self):
        p,b=generate(self.settings('GATEHOUSE','THORNFELL'))
        doors=[o for m in p.world_zones for rec in m.plan.facade_records
               for o in rec['openings'] if o.get('role')=='gallery_access']
        self.assertEqual(len(doors),4)
        routes=[r for r in p.functional_program['routes'] if 'guardhall_connection' in r['key']]
        self.assertEqual(len(routes),2)
        structural=[buf for buf in b if not buf.name.endswith(('.facade_doors','.facade_iron'))]
        for route in routes:
            x0,y0,z0,x1,y1,z1=route['bounds']
            for height in (.45,1.2,1.9):
                hits=_ray_hits((x0,(y0+y1)*.5,z0+height),(1,0,0),x1-x0,structural)
                self.assertFalse(hits,[(t,buf.name) for t,buf in hits[:4]])
        self.assertTrue(validate(p,b)['valid'])

    def test_other_78_regional_function_outputs_keep_existing_geometry(self):
        checked=0
        for folder in ('archetypes_v05','function_v07'):
            for path in (ROOT/'evidence'/folder/'manifests').glob('*.json'):
                for row in json.loads(path.read_text())['records']:
                    pair=(row['function'],row['region'])
                    is_functional=row['function'] in ('SMITHY','MARKET_HALL','STABLE','GATEHOUSE')
                    if pair in CASES or (folder=='archetypes_v05' and is_functional):continue
                    p,b=generate(Settings(**row['settings']))
                    self.assertEqual(geometry_hash(b),row['geometry_hash'],pair)
                    checked+=1
        self.assertEqual(checked,78)

if __name__=='__main__':unittest.main(verbosity=2)
