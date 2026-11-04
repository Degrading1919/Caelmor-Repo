"""Treatment integration gates independent of Blender's material and mesh adapter."""
from dataclasses import replace
import sys
import unittest
from pathlib import Path

sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
from caelmor_architecture.construction import STOCK, TREATMENTS
from caelmor_architecture.engine import Settings, generate, geometry_hash, validate
from caelmor_architecture.roof import shingle_layout
from test_world import _ray_hits


def fixture(region='LOWMARK', function='SMITHY', **kwargs):
    settings = Settings(region=region, function=function, world_aware=True, use_grammar=True,
                        seed=91, detail='MEDIUM', crafted_curves=True, seed_massing=True,
                        geometry_mode='EFFICIENT', construction_overrides={})
    return replace(settings, **kwargs)


class ConstructionTests(unittest.TestCase):
    def test_defaults_are_compatible_deterministic_and_reused(self):
        seen = set()
        by_function = {}
        for region, function in (('LOWMARK','SMITHY'), ('THORNFELL','GATEHOUSE'),
                                 ('LOWMARK','STABLE'), ('MIRE','FARMHOUSE'),
                                 ('EMBERHOLT','FARMHOUSE')):
            settings = fixture(region, function)
            plan, buffers = generate(settings)
            report = validate(plan, buffers)
            self.assertTrue(report['valid'], report['errors'])
            repeated, again = generate(settings)
            self.assertEqual(geometry_hash(buffers), geometry_hash(again))
            self.assertEqual(plan.construction_components, repeated.construction_components)
            specs = [b.construction for b in buffers if b.construction]
            by_function[region, function] = {c.treatment for c in specs}
            for c in specs:
                self.assertIn(c.component_role, TREATMENTS[c.treatment])
                self.assertIn(c.substrate, STOCK[c.treatment])
                seen.add(c.treatment)
            if region in ('MIRE','EMBERHOLT'):
                # Legacy roof assemblies are compared vertex for vertex.
                _, old = generate(replace(settings, construction_overrides=None))
                label = 'Split oak shingle courses' if region=='MIRE' else 'Lapped iron roof sheets'
                covers = [b for b in buffers if b.name.endswith(label)]
                self.assertTrue(covers, (region,function))
                legacy = {b.name:b for b in old}
                for b in covers:
                    self.assertIsNone(b.construction)
                    self.assertEqual(geometry_hash([b]), geometry_hash([legacy[b.name]]))
                self.assertNotIn('slate_tile_roofing', by_function[region, function])
        self.assertEqual(seen, set(TREATMENTS))
        self.assertTrue({'structural_timber','wooden_shingles'} <=
                        by_function['LOWMARK','SMITHY'] & by_function['LOWMARK','STABLE'])

    def test_override_precedence_stock_finish_and_host(self):
        settings = fixture('THORNFELL','GATEHOUSE', seed_massing=False)
        plan, initial = generate(settings)
        cover = next(c for c in plan.construction_components.values() if c.component_role=='roof_cover')
        wall = next(c for c in plan.construction_components.values() if c.component_role=='wall_body')
        opts = {'by_role': {'roof_cover': {'substrate':'fired_clay'}},
                'by_component': {cover.component_id: {'substrate':'slate'},
                                 wall.component_id: {'treatment':'dressed_stone'}}}
        candidate, changed = generate(replace(settings, construction_overrides=opts))
        self.assertEqual(candidate.construction_components[cover.component_id].substrate, 'slate')
        self.assertIn('fired_clay', {c.substrate for c in candidate.construction_components.values()})
        self.assertEqual(candidate.construction_components[wall.component_id].substrate, wall.substrate)
        self.assertNotEqual(geometry_hash(initial), geometry_hash(changed))
        self.assertTrue(validate(candidate, changed)['valid'])
        for substrate in ('limewash','lime_render'):
            coating = wall.component_id.replace('/wall','/wall_surface')
            opts = {'by_component': {coating: {'substrate':substrate}}}
            p, meshes = generate(replace(settings, construction_overrides=opts))
            self.assertTrue(validate(p,meshes)['valid'])
            self.assertEqual(p.construction_components[coating].host_component, wall.component_id)
            tagged = [b for b in meshes if b.construction == p.construction_components[coating]]
            self.assertTrue(tagged)
            if substrate=='limewash':
                for b in tagged:
                    old = next(x for x in initial if x.name==b.name)
                    self.assertEqual((b.vertices,b.faces),(old.vertices,old.faces))
        opts = {'by_component': {cover.component_id: {'finish':'material:Painted slate'}}}
        _, recoated = generate(replace(settings, construction_overrides=opts),
                               finish_names=('Painted slate',))
        self.assertEqual(geometry_hash(initial), geometry_hash(recoated))

    def test_bad_requests_are_rejected(self):
        for scope in (
            {'unknown': {}},
            {'by_role': {'roof_cover': {'treatment':'stone_masonry'}}},
            {'by_role': {'wall_infill': {'substrate':'limewash'}}},
            {'by_role': {'roof_cover': {'surface_family':'wood'}}},
            {'by_role': {'roof_cover': {'finish':'material:missing'}}},
            {'by_component': {'missing/roof_cover': {'treatment':'wooden_shingles'}}},
        ):
            with self.subTest(scope=scope), self.assertRaises(ValueError):
                generate(fixture(construction_overrides=scope))

    def test_smithy_skin_envelope_and_cover_gauge(self):
        settings = fixture()
        plan, buffers = generate(settings)
        shells = {'facade_board_skin', 'facade_render_skin'}
        for zone in plan.world_zones:
            x0, y0, x1, y1 = zone.bounds
            boards = [b for b in buffers if b.world_zone==zone.key and b.name.rsplit('.',1)[-1] in shells]
            for board in boards:
                for x,y,z in board.vertices:
                    # A manufactured face may project by its own gauge. It
                    # cannot acquire metres of relief from a sloping gable.
                    self.assertTrue(x0-.101<=x<=x1+.101 and y0-.101<=y<=y1+.101, (board.name,x,y,z))
                    self.assertLessEqual(z,zone.roof_height(x,y)+.015, (board.name,x,y,z))
        course = [piece for piece in shingle_layout(plan.world_zones[0].plan) if piece.row==2]
        self.assertGreater(len({round(p.thickness,4) for p in course}), 8)
        self.assertGreater(len({round(p.course_end,3) for p in course}), 8)
        self.assertTrue(all(p.course_end-p.exposed_end > p.lap_margin > 0 for p in course))
        self.assertTrue(any(len(p.poly)>4 for p in course))
        stock = next(b for b in buffers if b.name.endswith('facade_board_skin'))
        x_faces = {round(x,3) for x,y,z in stock.vertices if x>plan.world_zones[-1].bounds[2]}
        self.assertGreater(len(x_faces), 10)

    def test_portal_and_curtain_clearances_in_both_modes(self):
        for mode in ('SOLID','EFFICIENT'):
            settings = fixture('THORNFELL','GATEHOUSE', geometry_mode=mode)
            plan, buffers = generate(settings)
            legacy, _ = generate(replace(settings, construction_overrides=None))
            self.assertEqual(plan.functional_program, legacy.functional_program)
            report=validate(plan,buffers)
            self.assertTrue(report['valid'], report['errors'])
            portal=plan.world_zones[0]
            x0,y0,x1,y1=portal.bounds
            cx=(x0+x1)/2
            for z in (.35, 1.6, 2.89, 3.25):
                self.assertFalse(_ray_hits((cx,y0-.5,portal.base+z),(0,1,0),y1-y0+1,buffers))
            returns=[b for b in buffers if b.construction and b.construction.component_id.endswith('/curtain_return')]
            self.assertEqual(len(returns),2)
            for b in returns:
                for route in plan.functional_program['routes']:
                    box=route['bounds']
                    self.assertTrue(any(max(v[i] for v in b.vertices)<=box[i] or
                                        min(v[i] for v in b.vertices)>=box[i+3] for i in range(3)),route['key'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
