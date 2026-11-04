"""Numerical causal checks for building-local surface condition fields.

These checks cover data relationships and bounded values, not art approval.
"""
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from caelmor_architecture.surface_conditions import condition_fields, environment


FAMILIES = ("wood", "stone", "plaster", "roof", "iron", "leather", "charcoal")
REGIONS = ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")


def settings(*, age=0, maintenance=1, wealth="ESTABLISHED", region="LOWMARK"):
    return SimpleNamespace(age=age, maintenance=maintenance, wealth=wealth, region=region)


def sample(family="stone", *, age=0, maintenance=1, wealth="ESTABLISHED",
           region="LOWMARK", position=None, normal=None, context=None, key=None):
    if position is None:
        position = np.array([[.3, -.4, .15], [1.2, .1, 1.0], [2.3, .8, 2.0]])
    position = np.asarray(position, dtype=float)
    if normal is None:
        normal = np.tile([0., -1., 0.], (len(position), 1))
    normal = np.asarray(normal, dtype=float)
    n = len(position)
    return condition_fields(position, normal, np.linspace(0, .5, n), np.linspace(.1, .7, n),
                            key or family, settings(age=age, maintenance=maintenance,
                            wealth=wealth, region=region), context or {'base': 0., 'eave': 3., 'openings': [], 'soot': []},
                            unit=np.linspace(-.7, .7, n), unit_z=np.full(n, 2.), family=family)


class ConditionFieldTests(unittest.TestCase):
    def test_all_region_family_age_and_upkeep_combinations_are_finite_and_bounded(self):
        for family in FAMILIES:
            for region in REGIONS:
                for age in (0, 1, 250):
                    for maintenance in (0, 1):
                        with self.subTest(family=family, region=region, age=age, maintenance=maintenance):
                            result = sample(family, age=age, maintenance=maintenance, region=region)
                            for value in result.values():
                                self.assertTrue(np.all(np.isfinite(value)))
                            self.assertTrue(np.all((result['tint'] >= .15) & (result['tint'] <= 1.3)))
                            self.assertTrue(np.all((result['white'] >= 0) & (result['white'] <= .25)))
                            self.assertTrue(np.all((result['corrosion'] >= 0) & (result['corrosion'] <= .85)))
                            self.assertTrue(np.all((result['moisture'] >= 0) & (result['moisture'] <= 1)))
                            self.assertTrue(np.all((result['soot'] >= 0) & (result['soot'] <= 1)))

    def test_wealth_does_not_change_dirt_drivers_moisture_or_corrosion(self):
        for family in FAMILIES:
            modest = sample(family, age=125, maintenance=.2, wealth='MODEST')
            affluent = sample(family, age=125, maintenance=.2, wealth='AFFLUENT')
            for channel in ('moisture', 'corrosion', 'roughness_delta', 'height', 'white', 'maturity', 'soot'):
                np.testing.assert_array_equal(modest[channel], affluent[channel], err_msg=f'{family}: {channel}')
        # Wealth does affect stock grading on mineral materials, as intended.
        self.assertFalse(np.array_equal(sample('stone', wealth='MODEST')['tint'],
                                        sample('stone', wealth='AFFLUENT')['tint']))

    def test_age_maturity_is_independent_of_upkeep_and_maintained_materials_keep_history(self):
        for family in FAMILIES:
            neglected = sample(family, age=170, maintenance=0)
            kept = sample(family, age=170, maintenance=1)
            fresh = sample(family, age=0, maintenance=1)
            np.testing.assert_array_equal(neglected['maturity'], kept['maturity'], err_msg=family)
            self.assertGreater(float(kept['maturity']), 0.)
        old_iron, fresh_iron = sample('iron', age=170, maintenance=1), sample('iron', age=0, maintenance=1)
        self.assertTrue(np.any(old_iron['tint'] < fresh_iron['tint']))
        old_wood, fresh_wood = sample('wood', age=170, maintenance=1), sample('wood', age=0, maintenance=1)
        self.assertTrue(np.any(old_wood['silver'] > fresh_wood['silver']))

    def test_opening_runoff_uses_sill_jamb_cross_distance_and_outward_normal(self):
        # A real edge/opening record is converted into the same context consumed
        # by the sampler. Edge tangent is +X; exterior normal below the edge is -Y.
        plan = SimpleNamespace(edges=[((0., 0.), (4., 0.))], foundation_height=0., eave=3., soot_sources=[],
            facade_records=[{'edge_index': 0, 'openings': [
                {'kind': 'window', 's0': 1., 's1': 2., 'z0': 1.2},
                {'kind': 'door', 's0': 2.5, 's1': 3.5, 'z0': 0.},
            ]}])
        ctx = environment(plan)
        self.assertEqual(len(ctx['openings']), 1)
        positions = np.array([[1.07, -.05, .85], [1.07, -1.0, .85], [1.07, -.05, 1.3]])
        normals = np.tile([0., -1., 0.], (3, 1))
        result = sample('stone', age=120, maintenance=0, position=positions, normal=normals, context=ctx)
        self.assertGreater(result['moisture'][0], result['moisture'][1])
        self.assertGreater(result['moisture'][0], result['moisture'][2])
        inward = sample('stone', age=120, maintenance=0, position=positions[:1],
                        normal=np.array([[0., 1., 0.]]), context=ctx)
        self.assertGreater(result['moisture'][0], inward['moisture'][0])

    def test_ground_splash_uses_foundation_local_height(self):
        p = np.array([[0., 0., 1.05]])
        n = np.array([[0., -1., 0.]])
        at_grade = sample('stone', age=100, maintenance=0, position=p, normal=n,
                          context={'base': 1., 'eave': 3., 'openings': [], 'soot': []})
        elevated = sample('stone', age=100, maintenance=0, position=p, normal=n,
                          context={'base': 0., 'eave': 3., 'openings': [], 'soot': []})
        self.assertGreater(at_grade['moisture'][0], elevated['moisture'][0])

    def test_iron_corrosion_falls_with_maintenance_and_soot_needs_a_source(self):
        neglected = sample('iron', age=120, maintenance=0)
        maintained = sample('iron', age=120, maintenance=1)
        self.assertTrue(np.all(maintained['corrosion'] <= neglected['corrosion']))
        self.assertTrue(np.any(neglected['corrosion'] > maintained['corrosion']))
        dry = sample('stone', age=120, maintenance=0, key='stone')
        self.assertTrue(np.all(dry['soot'] == 0))
        source_context = {'base': 0., 'eave': 3., 'openings': [], 'soot': [(0., 0., 2.5)]}
        positions = np.array([[0., 0., 2.4], [5., 5., 2.4]])
        sourced = sample('stone', age=120, maintenance=0, position=positions, context=source_context)
        self.assertGreater(sourced['soot'][0], sourced['soot'][1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
