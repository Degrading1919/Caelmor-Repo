"""Pure geometry and program checks for function-first yard assemblies."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.model import Settings, resolve_settings
from caelmor_architecture.world import Context
from caelmor_architecture.function_yard import build_gatehouse, build_stable
from caelmor_architecture.engine import generate, geometry_hash, validate
from tests.test_world import _ray_hits


def _context(function, region='LOWMARK', wealth='ESTABLISHED', seed=91):
    requested = Settings(function=function, region=region, wealth=wealth,
                         seed=seed, world_aware=True)
    return Context(resolve_settings(requested))


class StableProgramTests(unittest.TestCase):
    def test_stalls_feeding_store_and_handling_access_are_present(self):
        ctx = _context('STABLE')
        program = build_stable(ctx)
        roles = [row['role'] for row in program['stations']]
        keys = [row['key'] for row in program['stations']]
        self.assertEqual('STABLE', program['function'])
        self.assertEqual(4, sum('.stable.divider.' in key for key in keys))
        self.assertEqual(10, roles.count('stall_gate'))
        self.assertEqual(10, sum('.split_gate.rail.' in key for key in keys))
        self.assertEqual(10, sum('.split_gate.top.' in key for key in keys))
        self.assertEqual(20, sum('.split_gate.stile.' in key for key in keys))
        self.assertEqual(5, sum('.manger.side.front.' in key for key in keys))
        self.assertEqual(5, sum('.manger.side.back.' in key for key in keys))
        self.assertEqual(10, sum('.manger.end.' in key for key in keys))
        self.assertGreaterEqual(roles.count('feeding'), 20)
        self.assertIn('storage', roles)
        self.assertTrue(any(route['key'] == 'stable.stall_entry.0'
                            for route in program['routes']))
        self.assertTrue(any(route['key'] == 'stable.animal_access'
                            and route['kind'] == 'animal'
                            for route in program['routes']))
        self.assertEqual({0, 2}, ctx.masses[0].plan.open_edges)
        self.assertAlmostEqual(6.2, ctx.masses[0].depth)
        self.assertEqual(6, len(ctx.masses[0].plan.functional_access))

    def test_mire_stable_uses_gentle_raised_approach(self):
        ctx = _context('STABLE', 'MIRE')
        program = build_stable(ctx)
        approach = next(row for row in program['approaches']
                        if row['key'] == 'stable.front_animal_ramp')
        self.assertLessEqual(approach['slope'], 1 / 6)
        self.assertEqual(2.0, approach['width'])
        rear = next(row for row in program['approaches']
                    if row['key'] == 'stable.rear_service_ramp')
        self.assertLessEqual(rear['slope'], 1 / 6)
        self.assertGreater(ctx.masses[0].base, .35)
        self.assertTrue(any('mire_service_walk' in buffer.name
                            for buffer in ctx.buffers))


class GatehouseProgramTests(unittest.TestCase):
    def test_emberholt_gate_has_valid_passage_and_guard_positions(self):
        ctx = _context('GATEHOUSE', 'EMBERHOLT')
        program = build_gatehouse(ctx)
        core = ctx.masses[0]
        passage = core.plan.passage_geometry
        self.assertTrue(passage['valid'])
        self.assertAlmostEqual(2.8, passage['clear_width'])
        self.assertGreaterEqual(passage['clear_height'], 3.2)
        self.assertEqual('GATEHOUSE', core.plan.settings.function)
        self.assertEqual('WATCHTOWER', ctx.masses[1].plan.settings.function)
        self.assertEqual('WATCHTOWER', ctx.masses[2].plan.settings.function)
        station_keys = [row['key'] for row in program['stations']]
        self.assertTrue(any('west_guard_stair.tread' in key for key in station_keys))
        self.assertTrue(any('east_guard_stair.tread' in key for key in station_keys))
        self.assertTrue(any('open_leaf' in key for key in station_keys))
        self.assertTrue(any('portcullis.upright' in key for key in station_keys))
        self.assertTrue(any('portal_jamb.front.west' in key
                            for key in station_keys))
        self.assertTrue(any('portal_jamb.rear.east' in key
                            for key in station_keys))
        self.assertEqual(['WATCHTOWER', 'WATCHTOWER'],
                         [mass.plan.settings.function for mass in ctx.masses[1:]])
        self.assertEqual([3, 3], [mass.plan.settings.floors for mass in ctx.masses[1:]])
        self.assertTrue(any(route['key'] == 'gatehouse_open_through_passage'
                            for route in program['routes']))

    def test_region_changes_gate_approach_and_mire_ramp(self):
        mire = _context('GATEHOUSE', 'MIRE')
        mire_program = build_gatehouse(mire)
        approach = next(row for row in mire_program['approaches']
                        if row['key'] == 'gatehouse.front_threshold_ramp')
        self.assertLessEqual(approach['slope'], 1 / 6)
        rear = next(row for row in mire_program['approaches']
                    if row['key'] == 'gatehouse.rear_threshold_ramp')
        self.assertLessEqual(rear['slope'], 1 / 6)
        self.assertTrue(any('gatehouse.mire_landing' in b.name
                            for b in mire.buffers))
        ember = _context('GATEHOUSE', 'EMBERHOLT')
        ember_program = build_gatehouse(ember)
        self.assertTrue(any('gatehouse.forecourt' in buffer.name
                            for buffer in ember.buffers))


class RegionalFunctionTests(unittest.TestCase):
    regions = ('LOWMARK', 'THORNFELL', 'MIRE', 'EMBERHOLT')

    def test_each_region_builds_valid_deterministic_stable_and_gatehouse(self):
        for region in self.regions:
            for function in ('STABLE', 'GATEHOUSE'):
                with self.subTest(region=region, function=function):
                    settings = Settings(function=function, region=region,
                                        world_aware=True, seed=73)
                    plan, buffers = generate(settings)
                    report = validate(plan, buffers)
                    self.assertTrue(report['valid'], report['errors'])
                    first_hash = geometry_hash(buffers)
                    plan_again, buffers_again = generate(settings)
                    self.assertEqual(first_hash, geometry_hash(buffers_again))

    def test_regional_arrangements_have_distinct_functional_buildings(self):
        low_stable = _context('STABLE', 'LOWMARK')
        build_stable(low_stable)
        thorn_stable = _context('STABLE', 'THORNFELL')
        build_stable(thorn_stable)
        mire_stable = _context('STABLE', 'MIRE')
        build_stable(mire_stable)
        ember_stable = _context('STABLE', 'EMBERHOLT')
        build_stable(ember_stable)
        self.assertTrue(any('lowmark_hay_loft' in b.name for b in low_stable.buffers))
        self.assertTrue(any('ridge_stone_knee' in row['key']
                            for row in thorn_stable.functional_program['stations']))
        self.assertTrue(any('mire_service_walk' in b.name for b in mire_stable.buffers))
        self.assertTrue(any('ember_yard_hitch_post' in row['key']
                            for row in ember_stable.functional_program['stations']))

        low_gate = _context('GATEHOUSE', 'LOWMARK')
        build_gatehouse(low_gate)
        thorn_gate = _context('GATEHOUSE', 'THORNFELL')
        build_gatehouse(thorn_gate)
        mire_gate = _context('GATEHOUSE', 'MIRE')
        build_gatehouse(mire_gate)
        ember_gate = _context('GATEHOUSE', 'EMBERHOLT')
        build_gatehouse(ember_gate)
        self.assertEqual('GABLE', thorn_gate.masses[0].plan.roof_mode)
        self.assertAlmostEqual(-.6, low_gate.masses[1].bounds[1])
        self.assertAlmostEqual(-.6, ember_gate.masses[2].bounds[1])
        self.assertTrue(any('lowmark_stone_portal_cheek' in row['key']
                            for row in low_gate.functional_program['stations']))
        self.assertAlmostEqual(1.2, mire_gate.masses[2].bounds[1])
        self.assertTrue(any('mire_watchbank_bridge' in b.name for b in mire_gate.buffers))
        self.assertEqual('TERRACE', ember_gate.masses[0].plan.roof_mode)

    def test_pilot_front_and_rear_routes_are_clear_in_mesh_rays(self):
        stable_plan, stable_buffers = generate(
            Settings(function='STABLE', region='MIRE', world_aware=True, seed=91))
        stable = stable_plan.world_zones[0]
        capacity = 5  # established seed 91 resolves to five stall bays
        bay_center = ((capacity - 1) // 2 + .5) * 2.9
        for origin, direction, distance, label in (
                ((bay_center, -.5, stable.base + .2), (0, 1, 0), 5.4, 'stable front'),
                ((stable.bounds[2] - .9, stable.bounds[3] + .5, stable.base + .2),
                 (0, -1, 0), 1.5, 'stable rear service')):
            with self.subTest(route=label):
                hits = _ray_hits(origin, direction, distance, stable_buffers)
                self.assertEqual([], [(round(t, 3), b.name) for t, b in hits])

        gate_plan, gate_buffers = generate(
            Settings(function='GATEHOUSE', region='EMBERHOLT', world_aware=True, seed=91))
        gate = gate_plan.world_zones[0]
        center_x = sum(gate.bounds[::2]) * .5
        hits = _ray_hits((center_x, -.5, gate.base + 1.5),
                         (0, 1, 0), gate.depth + 1.0, gate_buffers)
        self.assertEqual([], [(round(t, 3), b.name) for t, b in hits])
        mire_gate_plan, mire_gate_buffers = generate(
            Settings(function='GATEHOUSE', region='MIRE', world_aware=True, seed=91))
        mire_gate = mire_gate_plan.world_zones[0]
        mire_center = sum(mire_gate.bounds[::2]) * .5
        mire_hits = _ray_hits((mire_center, -.5, mire_gate.base + 1.5),
                              (0, 1, 0), mire_gate.depth + 1.0, mire_gate_buffers)
        self.assertEqual([], [(round(t, 3), b.name) for t, b in mire_hits])

        mire_context = _context('GATEHOUSE', 'MIRE', seed=91)
        mire_program = build_gatehouse(mire_context)
        east_edge = next(record for record in mire_context.masses[2].plan.facade_records
                         if record['edge_index'] == 1)
        access_door = next(opening for opening in east_edge['openings']
                           if opening['kind'] == 'door')
        self.assertAlmostEqual(1.05, access_door['s1'] - access_door['s0'])
        door_route = next(route for route in mire_program['routes']
                          if route['key'] == 'gatehouse.mire_watchbank_door_route')
        route_bounds = door_route['bounds']
        door_y = (route_bounds[1] + route_bounds[4]) * .5
        door_start_x = route_bounds[0]
        door_distance = route_bounds[3] - route_bounds[0] + .10
        # The façade door is operable and may be closed in this static build;
        # retain every wall, frame, glazing and proxy buffer in the clearance test.
        door_solid_buffers = [buffer for buffer in mire_gate_buffers
                              if not buffer.name.endswith('.facade_doors')]
        for y_offset in (-.4, 0.0, .4):
            for z_offset in (.45, 1.2, 2.0):
                with self.subTest(mire_access_y=y_offset,
                                  mire_access_z=z_offset):
                    door_hits = _ray_hits(
                        (door_start_x, door_y + y_offset,
                         mire_gate.base + z_offset),
                        (1, 0, 0), door_distance, door_solid_buffers)
                    self.assertEqual([], [(round(t, 3), b.name)
                                          for t, b in door_hits])

    def test_modest_established_affluent_and_detail_profiles(self):
        for wealth, expected_watch_slots, expected_stalls in (
                ('MODEST', 3, 4), ('ESTABLISHED', 4, 5), ('AFFLUENT', 5, 6)):
            with self.subTest(wealth=wealth):
                stable_ctx = _context('STABLE', 'LOWMARK', wealth=wealth, seed=91)
                stable_program = build_stable(stable_ctx)
                self.assertEqual(expected_stalls * 2,
                                 sum(row['role'] == 'stall_gate'
                                     for row in stable_program['stations']))
                gate_ctx = _context('GATEHOUSE', 'EMBERHOLT', wealth=wealth, seed=91)
                gate_program = build_gatehouse(gate_ctx)
                count = sum('merlon' in row['key']
                            for row in gate_program['stations'])
                self.assertEqual(expected_watch_slots * 2, count)
        for detail in ('LOW', 'MEDIUM', 'HIGH'):
            with self.subTest(detail=detail):
                settings = Settings(function='GATEHOUSE', region='THORNFELL',
                                    world_aware=True, seed=29, detail=detail)
                plan, buffers = generate(settings)
                self.assertTrue(validate(plan, buffers)['valid'])


if __name__ == '__main__':
    unittest.main()
