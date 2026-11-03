"""Shared functional invariants plus preservation of the other 16 programs."""
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from caelmor_architecture.engine import generate,validate,geometry_hash
from caelmor_architecture.functional import Builder,FUNCTIONS
from caelmor_architecture.model import Settings,resolve_settings
from caelmor_architecture.world import Context,WorldPlan


class FunctionalIntegrationTests(unittest.TestCase):
    def settings(self,function,region):
        return Settings(function=function,region=region,seed=91,detail='MEDIUM',
                        geometry_mode='EFFICIENT',world_aware=True,use_grammar=True)

    def test_programs_validate_across_regions_and_reproduce(self):
        for function in FUNCTIONS:
            for region in ('LOWMARK','THORNFELL','MIRE','EMBERHOLT'):
                with self.subTest(function=function,region=region):
                    settings=self.settings(function,region)
                    p,b=generate(settings);report=validate(p,b)
                    self.assertTrue(report['valid'],report['errors'][:8])
                    self.assertEqual(p.functional_program['function'],function)
                    self.assertTrue(p.functional_program['routes'])
                    self.assertEqual(geometry_hash(b),geometry_hash(generate(settings)[1]))

    def test_declared_public_route_rejects_actual_counter_blockage(self):
        s=resolve_settings(self.settings('MARKET_HALL','THORNFELL'))
        ctx=Context(s);b=Builder(ctx,'MARKET_HALL')
        m=b.mass('hall',width=8,depth=6,floor_height=3.5,open_edges=(0,2))
        b.route('public_aisle',(3,0,.4,5,6,2.5),kind='public')
        b.box('bad_counter',(3.5,2,.5,4.5,3,1.4),'stone',m)
        report=validate(WorldPlan(ctx,s),ctx.buffers)
        self.assertFalse(report['valid'])
        self.assertTrue(any('Functional clearance blocked' in e for e in report['errors']))

    def test_other_sixteen_functions_match_recorded_v05_geometry(self):
        checked=0
        for path in (ROOT/'evidence'/'archetypes_v05'/'manifests').glob('*.json'):
            old=json.loads(path.read_text())
            for row in old['records']:
                if row['function'] in FUNCTIONS:continue
                with self.subTest(function=row['function'],region=row['region']):
                    plan,buffers=generate(Settings(**row['settings']))
                    self.assertIsNone(plan.functional_program)
                    self.assertEqual(geometry_hash(buffers),row['geometry_hash'])
                checked+=1
        self.assertEqual(checked,64)

    def test_stone_structure_cannot_hide_above_weather_roof(self):
        s=resolve_settings(self.settings('MARKET_HALL','THORNFELL'))
        ctx=Context(s);b=Builder(ctx,'MARKET_HALL')
        m=b.mass('hall',width=8,depth=6,floor_height=3.5,open_edges=(0,2))
        bad=ctx.buffer('bad_capital','stone','structure',m)
        bad.box((4,0,m.eave+.10),(.2,.2,.2))
        result=validate(WorldPlan(ctx,s),ctx.buffers)
        self.assertFalse(result['valid'])
        self.assertTrue(any('functional structure crosses weather roof' in e for e in result['errors']))

    def test_forge_exhaust_is_open_from_hood_into_stack(self):
        from test_world import _ray_hits
        import math
        for region in ('LOWMARK','THORNFELL','MIRE','EMBERHOLT'):
            with self.subTest(region=region):
                plan,buffers=generate(self.settings('SMITHY',region))
                for label in ('hood_inlet','duct','stack'):
                    start,end=plan.functional_program['ventilation'][label]
                    distance=math.dist(start,end)
                    direction=tuple((b-a)/distance for a,b in zip(start,end))
                    hits=_ray_hits(start,direction,distance,buffers)
                    self.assertEqual(len(hits),0,(region,label,[(round(t,4),b.name) for t,b in hits[:4]]))
                self.assertTrue(validate(plan,buffers)['valid'])


if __name__=='__main__':unittest.main(verbosity=2)
