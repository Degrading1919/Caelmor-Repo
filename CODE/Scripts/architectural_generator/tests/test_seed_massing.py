"""Semantic diversity and v0.11 replay regression for two building functions."""
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from caelmor_architecture.engine import generate, geometry_hash, validate
from caelmor_architecture.model import Settings


def massing_signature(plan):
    return tuple((tuple(round(v, 2) for v in mass.bounds), round(mass.eave, 2),
                  mass.plan.roof_mode, mass.plan.rects[0][-1])
                 for mass in plan.world_zones)


def comparison_settings():
    manifest = ROOT / 'evidence' / 'diversity_v12' / 'before' / 'manifest.json'
    return json.loads(manifest.read_text())['cases']


class SeedMassingTests(unittest.TestCase):
    def test_existing_saved_buildings_replay_without_opt_in(self):
        for row in comparison_settings():
            settings = Settings(**row['settings'])
            with self.subTest(function=settings.function, seed=settings.seed):
                self.assertFalse(settings.seed_massing)
                self.assertEqual(row['geometry_hash'], geometry_hash(generate(settings)[1]))

    def test_seed_changes_massing_and_structure_without_changing_function(self):
        signatures = {'SMITHY': set(), 'GATEHOUSE': set()}
        roof_layouts = {'SMITHY': set(), 'GATEHOUSE': set()}
        for row in comparison_settings():
            settings = replace(Settings(**row['settings']), seed_massing=True)
            with self.subTest(function=settings.function, seed=settings.seed):
                plan, buffers = generate(settings)
                report = validate(plan, buffers)
                self.assertTrue(report['valid'], report['errors'][:6])
                self.assertEqual(geometry_hash(buffers), geometry_hash(generate(settings)[1]))
                signature = massing_signature(plan)
                signatures[settings.function].add(signature)
                roof_layouts[settings.function].add(tuple(zone[2:] for zone in signature))
                program = plan.functional_program
                self.assertEqual(program['function'], settings.function)
                if settings.function == 'SMITHY':
                    self.assertTrue({'hood_inlet', 'duct', 'stack'} <= program['ventilation'].keys())
                    self.assertTrue(any(r['key'] == 'forge_material_lane' for r in program['routes']))
                else:
                    route = next(r for r in program['routes']
                                 if r['key'] == 'gatehouse_open_through_passage')
                    x0, _, z0, x1, _, z1 = route['bounds']
                    self.assertGreaterEqual(x1-x0, 2.7-1e-6)
                    self.assertAlmostEqual(z1-z0, 2.90)
                    self.assertEqual(sum('guardhall_connection' in r['key']
                                         for r in program['routes']), 2)
                    openings = [o for mass in plan.world_zones for record in mass.plan.facade_records
                                for o in record['openings'] if o.get('role') == 'gallery_access']
                    self.assertEqual(len(openings), 4)
                    self.assertTrue(all(o['z1']-o['z0'] >= 2.04 for o in openings))
                    zones = {mass.key: mass for mass in plan.world_zones}
                    quoins = [buffer for buffer in buffers if buffer.name.endswith('_bonded_quoins')]
                    self.assertEqual(len(quoins), 2)
                    for buffer in quoins:
                        owner = zones[buffer.world_zone]
                        for x, y, z in buffer.vertices:
                            self.assertLessEqual(z, owner.roof_height(x,y)-.12+1e-6,
                                                 (buffer.name, x, y, z))
        for function, layouts in signatures.items():
            self.assertEqual(len(layouts), 5, function)
            self.assertGreaterEqual(len(roof_layouts[function]), 2, function)

    def test_straight_solid_and_wealth_extremes(self):
        for row in comparison_settings():
            settings = replace(Settings(**row['settings']), seed_massing=True,
                               crafted_curves=False, detail='LOW', geometry_mode='SOLID',
                               wealth='MODEST' if row['settings']['seed'] % 2 else 'AFFLUENT')
            with self.subTest(function=settings.function, seed=settings.seed):
                plan, buffers = generate(settings)
                report = validate(plan, buffers)
                self.assertTrue(report['valid'], report['errors'][:6])
                self.assertFalse(any(getattr(patch, 'swept', False)
                                     for mass in plan.world_zones
                                     for patch in getattr(mass.plan, 'custom_roof_sources', ())))
