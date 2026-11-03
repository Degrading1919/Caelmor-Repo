"""Functional investment checks; visual readability is a separate human gate."""
from dataclasses import replace
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from caelmor_architecture.engine import generate,validate,geometry_hash
from caelmor_architecture.geometry import clip,inequalities,area
from caelmor_architecture.model import Settings
from caelmor_architecture.roof import roof_faces


def crossing_roofs(masses):
    errors=[]
    for i,a in enumerate(masses):
        for b in masses[i+1:]:
            for pa in roof_faces(a.plan):
                for pb in roof_faces(b.plan):
                    poly=pa.poly
                    for plane in inequalities(pb.poly):
                        poly=clip(poly,*plane)
                        if not poly:break
                    if len(poly)<3 or abs(area(poly))<1e-5:continue
                    difference=[pa.height(x,y)-pb.height(x,y) for x,y in poly]
                    if min(difference)<-.015 and max(difference)>.015:
                        errors.append((a.key,b.key,round(min(difference),3),round(max(difference),3)))
    return errors


class HouseholdInvestmentTests(unittest.TestCase):
    def settings(self,region,wealth):
        return Settings(seed=91,function='COTTAGE',region=region,wealth=wealth,
                        world_aware=True,use_grammar=True,detail='MEDIUM',geometry_mode='EFFICIENT')

    def test_representative_roof_surfaces_do_not_cross_between_volumes(self):
        for region in ('LOWMARK','THORNFELL','MIRE','EMBERHOLT'):
            for wealth in ('MODEST','ESTABLISHED','AFFLUENT'):
                with self.subTest(region=region,wealth=wealth):
                    plan,buffers=generate(self.settings(region,wealth))
                    report=validate(plan,buffers)
                    self.assertTrue(report['valid'],report['errors'][:5])
                    self.assertFalse(crossing_roofs(plan.world_zones))

    def test_validator_rejects_crossed_eaves_without_occupied_overlap(self):
        from caelmor_architecture.world import Context,WorldPlan
        s=self.settings('LOWMARK','ESTABLISHED')
        ctx=Context(s)
        ctx.mass('hall',width=8,depth=6,floors=1,pitch=32,overhang=.42)
        ctx.mass('bad_shed',x=8.2,y=.4,width=3,depth=4,floors=1,
                 floor_height=2.2,roof='SHED',pitch=20,overhang=.36)
        self.assertGreater(ctx.masses[1].bounds[0],ctx.masses[0].bounds[2])
        report=validate(WorldPlan(ctx,s),ctx.buffers)
        self.assertFalse(report['valid'])
        self.assertTrue(any('Weather roofs cross' in e for e in report['errors']),report['errors'])

    def test_ember_work_roof_is_metal_and_solid_mode_is_closed(self):
        s=self.settings('EMBERHOLT','ESTABLISHED')
        for mode in ('SOLID','EFFICIENT'):
            plan,buffers=generate(replace(s,geometry_mode=mode))
            covers=[b for b in buffers if 'Lapped iron roof sheets' in b.name]
            self.assertTrue(covers)
            self.assertTrue(all(b.material=='iron' for b in covers))
            self.assertTrue(all(b.topology==('SOLID' if mode=='SOLID' else 'SURFACE') for b in covers))
            self.assertTrue(validate(plan,buffers)['valid'])

    def test_mire_investment_buys_work_floor_and_private_room(self):
        areas=[]
        for wealth in ('MODEST','ESTABLISHED','AFFLUENT'):
            plan,buffers=generate(self.settings('MIRE',wealth))
            primary=plan.world_zones[0]
            # Measure actual exposed front access floor, normalized by host
            # width: the difference cannot be satisfied by scaling the house.
            decks=[(bounds,z) for bounds,z in plan.access_decks if bounds[1]<0 and bounds[3]<=.01]
            floor_area=sum((b[2]-b[0])*(b[3]-b[1]) for b,z in decks)
            areas.append(floor_area/primary.width)
            if wealth=='AFFLUENT':
                self.assertGreater(len(plan.world_zones),1)
                room=plan.world_zones[1]
                self.assertGreater(room.width*room.depth,12.)
                self.assertTrue(any(o['kind']=='door' for r in room.plan.facade_records for o in r['openings']))
        self.assertGreater(areas[1],areas[0]*2)

    def test_mire_repair_is_a_condition_event_not_a_wealth_stereotype(self):
        s=self.settings('MIRE','MODEST')
        young,by=generate(replace(s,age=15,maintenance=.3))
        old,bo=generate(replace(s,age=110,maintenance=.3))
        kept,bk=generate(replace(s,age=110,maintenance=.9))
        def repair(b):return [v for x in b if 'sistered_pier_repair' in x.name for v in x.vertices]
        self.assertFalse(repair(by));self.assertTrue(repair(bo));self.assertFalse(repair(bk))
        self.assertEqual(old.world_zones[0].bounds,young.world_zones[0].bounds)
        self.assertEqual(min(v[2] for v in repair(bo)),0.)
        self.assertTrue(validate(old,bo)['valid'])
        _,repeat=generate(replace(s,age=110,maintenance=.3))
        self.assertEqual(geometry_hash(bo),geometry_hash(repeat))


if __name__=='__main__':unittest.main(verbosity=2)
