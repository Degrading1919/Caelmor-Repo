"""Focused construction/tier regressions for Lowmark and Thornfell households."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.engine import generate, geometry_hash, validate
from caelmor_architecture.geometry import clip, inequalities, area
from caelmor_architecture.model import Settings
from caelmor_architecture.profiles import TYPE_SPECS
from caelmor_architecture.roof import roof_faces


def _masses(plan):
    return {mass.key: mass for mass in plan.world_zones}


def _has_buffer(buffers, suffix):
    return any(buffer.name.endswith(suffix) for buffer in buffers)


def _crossing_roofs(masses):
    for i, first in enumerate(masses):
        for second in masses[i+1:]:
            for left in roof_faces(first.plan):
                for right in roof_faces(second.plan):
                    overlap = left.poly
                    for plane in inequalities(right.poly):
                        overlap = clip(overlap, *plane)
                        if not overlap:
                            break
                    if len(overlap) < 3 or abs(area(overlap)) < 1e-5:
                        continue
                    difference = [left.height(x,y)-right.height(x,y) for x,y in overlap]
                    if min(difference) < -.015 and max(difference) > .015:
                        return first.key, second.key, min(difference), max(difference)
    return None


class RuralHouseholdConstructionTests(unittest.TestCase):
    def test_lowmark_wealth_changes_household_program(self):
        for function in ("COTTAGE", "FARMHOUSE", "TOWNHOUSE", "MERCHANT_HOUSE"):
            hashes = set()
            expected_floors = TYPE_SPECS[function].floors
            for wealth in ("MODEST", "ESTABLISHED", "AFFLUENT"):
                settings = Settings(seed=91, function=function, region="LOWMARK",
                    context="RURAL", wealth=wealth, age=35, maintenance=.7,
                    craftsmanship="STANDARD", detail="MEDIUM", geometry_mode="EFFICIENT",
                    use_grammar=True, world_aware=True)
                plan, buffers = generate(settings)
                self.assertTrue(validate(plan, buffers)["valid"])
                masses = _masses(plan)
                self.assertIsNone(_crossing_roofs(plan.world_zones), function)
                self.assertIn("lowmark_main_hall", masses)
                self.assertIn("lowmark_service_wing", masses)
                self.assertEqual(masses["lowmark_main_hall"].plan.settings.floors, expected_floors)
                if wealth == "MODEST":
                    self.assertNotIn("lowmark_household_store", masses)
                    self.assertNotIn("lowmark_private_solar", masses)
                    self.assertTrue(masses["lowmark_service_wing"].plan.open_edges)
                else:
                    self.assertIn("lowmark_household_store", masses)
                    self.assertTrue(any(o["kind"] == "door"
                        for record in masses["lowmark_household_store"].plan.facade_records
                        for o in record["openings"]))
                if wealth == "AFFLUENT":
                    self.assertIn("lowmark_private_solar", masses)
                    self.assertTrue(_has_buffer(buffers, "lowmark_sheltered_workyard_boundary"))
                    self.assertTrue(_has_buffer(buffers, "lowmark_private_solar_approach"))
                else:
                    self.assertNotIn("lowmark_private_solar", masses)
                hashes.add(geometry_hash(buffers))
                repeat_plan, repeat_buffers = generate(settings)
                self.assertEqual(geometry_hash(buffers), geometry_hash(repeat_buffers))
                self.assertTrue(validate(repeat_plan, repeat_buffers)["valid"])
            self.assertEqual(len(hashes), 3)

    def test_thornfell_homes_use_calm_roofs_and_wealth_does_not_buy_towers(self):
        for function in ("COTTAGE", "FARMHOUSE", "TOWNHOUSE", "MERCHANT_HOUSE"):
            expected_floors = TYPE_SPECS[function].floors
            for wealth in ("MODEST", "ESTABLISHED", "AFFLUENT"):
                settings = Settings(seed=91, function=function, region="THORNFELL",
                    context="RIDGE", wealth=wealth, age=35, maintenance=.7,
                    craftsmanship="STANDARD", detail="MEDIUM", geometry_mode="EFFICIENT",
                    use_grammar=True, world_aware=True)
                plan, buffers = generate(settings)
                self.assertTrue(validate(plan, buffers)["valid"])
                masses = _masses(plan)
                self.assertIsNone(_crossing_roofs(plan.world_zones), function)
                self.assertIn("thornfell_stone_hall", masses)
                self.assertEqual(masses["thornfell_stone_hall"].plan.settings.pitch, 42)
                self.assertEqual(masses["thornfell_stone_hall"].plan.settings.floors, expected_floors)
                self.assertNotIn("thornfell_signal_tower", masses)
                self.assertFalse(_has_buffer(buffers, "stepped_wind_gables"))
                if wealth == "MODEST":
                    self.assertNotIn("thornfell_lower_stone_range", masses)
                    self.assertNotIn("thornfell_private_room_range", masses)
                else:
                    self.assertIn("thornfell_lower_stone_range", masses)
                if wealth == "AFFLUENT":
                    self.assertIn("thornfell_private_room_range", masses)
                    self.assertTrue(_has_buffer(buffers, "thornfell_private_court_approach"))
                else:
                    self.assertNotIn("thornfell_private_room_range", masses)
                again, again_buffers = generate(settings)
                self.assertEqual(geometry_hash(buffers), geometry_hash(again_buffers))
                self.assertTrue(validate(again, again_buffers)["valid"])

    def test_civic_and_defensive_towers_remain_functional_not_wealth_driven(self):
        for function in ("GATEHOUSE", "WATCHTOWER"):
            settings = Settings(seed=91, function=function, region="THORNFELL",
                context="RIDGE", wealth="MODEST", detail="LOW", use_grammar=True,
                world_aware=True)
            plan, buffers = generate(settings)
            self.assertTrue(validate(plan, buffers)["valid"])
            if function=='GATEHOUSE':
                self.assertEqual(plan.functional_program['function'],'GATEHOUSE')
                self.assertEqual(sum(m.plan.settings.function=='WATCHTOWER' for m in plan.world_zones),2)
                self.assertTrue(plan.world_zones[0].plan.passage_geometry['valid'])
            else:
                self.assertIn("thornfell_signal_tower", _masses(plan))

    def test_ordinary_homes_do_not_gain_towers_from_public_context_alone(self):
        for context in ("PASSWATCH", "STONEWAKE"):
            plan, buffers = generate(Settings(seed=91, function="COTTAGE",
                region="THORNFELL", context=context, wealth="AFFLUENT",
                detail="LOW", use_grammar=True, world_aware=True))
            self.assertTrue(validate(plan, buffers)["valid"])
            self.assertNotIn("thornfell_signal_tower", _masses(plan))

    def test_thornfell_inns_and_workshops_keep_calm_roofs(self):
        for function in ("INN", "WORKSHOP"):
            plan, buffers = generate(Settings(seed=91, function=function,
                region="THORNFELL", context="RIDGE", wealth="ESTABLISHED",
                detail="LOW", use_grammar=True, world_aware=True))
            self.assertTrue(validate(plan, buffers)["valid"])
            self.assertEqual(_masses(plan)["thornfell_stone_hall"].plan.settings.pitch, 42)
            self.assertFalse(_has_buffer(buffers, "stepped_wind_gables"))

    def test_lowmark_miller_keeps_wheel_and_blind_working_faces(self):
        settings = Settings(seed=91, function="MILLER", region="LOWMARK",
            context="RURAL", wealth="ESTABLISHED", detail="LOW", use_grammar=True,
            world_aware=True)
        plan, buffers = generate(settings)
        self.assertTrue(validate(plan, buffers)["valid"])
        self.assertTrue(_has_buffer(buffers, "mill_wheel_rims_spokes_paddles"))
        main = _masses(plan)["lowmark_main_hall"]
        for edge_index in (1, 3):
            self.assertFalse(main.plan.facade_records[edge_index]["openings"],
                f"Miller wheel interface edge {edge_index} must remain blind")

    def test_selected_type_contracts_remain_valid(self):
        for region, function in (("LOWMARK", "GATEHOUSE"),
                                 ("THORNFELL", "GATEHOUSE"),
                                 ("THORNFELL", "WATCHTOWER")):
            with self.subTest(region=region, function=function):
                context = "RURAL" if region == "LOWMARK" else "RIDGE"
                plan, buffers = generate(Settings(seed=27, function=function,
                    region=region, context=context, wealth="AFFLUENT", detail="LOW",
                    use_grammar=True, world_aware=True))
                self.assertTrue(validate(plan, buffers)["valid"])
                self.assertTrue(_masses(plan))


if __name__ == "__main__":
    unittest.main(verbosity=2)
