"""Focused construction and aperture checks for Emberholt households."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.engine import generate, validate
from caelmor_architecture.model import Settings


class EmberholtHouseholdTests(unittest.TestCase):
    families = ("COTTAGE", "FARMHOUSE", "TOWNHOUSE", "MERCHANT_HOUSE", "SHOP")
    tiers = ("MODEST", "ESTABLISHED", "AFFLUENT")

    def _build(self, function, wealth, context="EMBERHOLD"):
        settings = Settings(seed=91, function=function, region="EMBERHOLT",
                            context=context, wealth=wealth, detail="HIGH",
                            use_grammar=True, world_aware=True)
        plan, buffers = generate(settings)
        report = validate(plan, buffers)
        self.assertTrue(report["valid"], (function, wealth, report["errors"][:8]))
        return plan, buffers

    @staticmethod
    def _zone(plan, key):
        return next(zone for zone in plan.world_zones if zone.key == key)

    @staticmethod
    def _bounds(zone):
        xs = [point[0] for point in zone.plan.outline]
        ys = [point[1] for point in zone.plan.outline]
        return min(xs), min(ys), max(xs), max(ys)

    def test_domestic_families_have_separate_work_ranges_and_real_doors(self):
        for function in self.families:
            for wealth in self.tiers:
                with self.subTest(function=function, wealth=wealth):
                    plan, _buffers = self._build(function, wealth)
                    main = self._zone(plan, "emberholt_main_block")
                    if function == "COTTAGE" and wealth == "AFFLUENT":
                        rooms = self._zone(plan, "emberholt_private_rooms")
                        self.assertTrue(any(o["kind"] == "door"
                                            for r in rooms.plan.facade_records
                                            for o in r["openings"]))
                        continue
                    if function == "COTTAGE" and wealth == "MODEST":
                        continue
                    work = self._zone(plan, "emberholt_domestic_work_range")
                    self.assertLess(self._bounds(work)[2] - self._bounds(work)[0],
                                    self._bounds(main)[2] - self._bounds(main)[0])
                    records = work.plan.facade_records
                    front = next((r for r in records if r["edge_index"] == 0), None)
                    self.assertIsNotNone(front)
                    self.assertTrue(any(o["kind"] == "door" for o in front["openings"]))
                    # The attached range shares the main body's east wall; both
                    # authored faces stay blind so doors/windows cannot overlap.
                    self.assertFalse(any(r["openings"] for r in main.plan.facade_records
                                         if r["edge_index"] == 1))
                    self.assertFalse(any(r["openings"] for r in records
                                         if r["edge_index"] == 3))

    def test_family_floor_hierarchy_and_context_do_not_override_wealth(self):
        expected = {"COTTAGE": {"MODEST": 1, "ESTABLISHED": 2, "AFFLUENT": 3},
                    "FARMHOUSE": {"MODEST": 2, "ESTABLISHED": 2, "AFFLUENT": 2},
                    "TOWNHOUSE": {"MODEST": 3, "ESTABLISHED": 3, "AFFLUENT": 3},
                    "MERCHANT_HOUSE": {"MODEST": 2, "ESTABLISHED": 2, "AFFLUENT": 2},
                    "SHOP": {"MODEST": 2, "ESTABLISHED": 2, "AFFLUENT": 2}}
        for function in self.families:
            for wealth in self.tiers:
                plan, _buffers = self._build(function, wealth)
                main = self._zone(plan, "emberholt_main_block")
                self.assertEqual(main.plan.settings.floors, expected[function][wealth])
        for context in ("ASHSPIRE", "EMBERFORGES"):
            for wealth in ("MODEST", "AFFLUENT"):
                plan, _buffers = self._build("COTTAGE", wealth, context)
                main = self._zone(plan, "emberholt_main_block")
                self.assertEqual(main.plan.settings.floors,
                                 expected["COTTAGE"][wealth])

    def test_gatehouse_passage_and_smithy_still_validate(self):
        for function, wealth in (("GATEHOUSE", "ESTABLISHED"),
                                 ("GATEHOUSE", "AFFLUENT"),
                                 ("SMITHY", "ESTABLISHED")):
            with self.subTest(function=function, wealth=wealth):
                plan, _buffers = self._build(function, wealth)
                main = plan.world_zones[0]
                self.assertEqual(plan.functional_program['function'],function)
                if function == "GATEHOUSE":
                    front = next(r for r in main.plan.facade_records
                                 if r["edge_index"] == 0)
                    self.assertTrue(any(o.get("role") == "passage_entry"
                                        for o in front["openings"]))
                    self.assertTrue(main.plan.passage_geometry['valid'])
                else:
                    self.assertIn(0,main.plan.open_edges)
                    self.assertTrue(any('hearth' in b.name for b in _buffers))


if __name__ == "__main__":
    unittest.main(verbosity=2)
