"""Pure contract tests for the function-first smithy and market plans."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TESTS = ROOT / "tests"
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from caelmor_architecture import function_work
from caelmor_architecture.engine import generate, validate
from caelmor_architecture.model import Settings
from test_world import _ray_hits


class FakeBuilder:
    def __init__(self, ctx, program_id):
        self.ctx = ctx
        self.settings = ctx.settings
        self.region = ctx.settings.region
        self.base = 1.15 if self.region == "MIRE" else .32
        self.roof = "GABLE"
        self.pitch = 42 if self.region == "THORNFELL" else 32
        self.material = "stone" if self.region in ("THORNFELL", "EMBERHOLT") else "timber"
        self.program = {"function": program_id, "routes": [], "stations": []}
        ctx.program = self.program

    def mass(self, key, **kwargs):
        kwargs.setdefault("roof",self.roof)
        kwargs.setdefault("pitch",self.pitch)
        width, depth = kwargs["width"], kwargs["depth"]
        eave = self.base+2.8
        mass = SimpleNamespace(width=width, depth=depth, base=self.base,
                               eave=eave, roof_height=lambda x, y: eave-.1,
                               bounds=(0, 0, width, depth),
                               plan=SimpleNamespace(open_edges=set(kwargs.get("open_edges", [])),
                                                    wall_thickness=function_work._wall_thickness(self.region)))
        self.ctx.masses.append((key, kwargs, mass))
        return mass

    def box(self, key, bounds, material, zone, role="equipment"):
        self.ctx.boxes.append((key, bounds, material, zone, role))
        return SimpleNamespace(box=lambda *args: None)

    def fixture(self, key, material, zone, role="equipment"):
        self.ctx.fixtures.append((key, material, zone, role))
        return SimpleNamespace(box=lambda *args: None)

    def route(self, key, bounds, kind="human"):
        self.program["routes"].append((key, bounds, kind))

    def deck(self, key, poly, z=None, material=None, zone=None):
        self.ctx.decks.append((key, poly, z, material, zone))

    def ramp(self, key, start_xy, end_xy, width, z, zone=None, material=None):
        self.ctx.ramps.append((key, start_xy, end_xy, width, z, zone, material))

    def finish(self):
        return self.program


class FakeBuffer:
    def __init__(self, key):
        self.key = key
    def beam(self, *args): pass
    def extrude(self, *args): pass
    def box(self, *args): pass


class FakeContext:
    def __init__(self, region, wealth="ESTABLISHED", width=11, depth=8):
        self.settings = SimpleNamespace(region=region, wealth=wealth, width=width, depth=depth)
        self.masses, self.boxes, self.fixtures, self.buffers = [], [], [], []
        self.decks,self.ramps=[],[]
    def buffer(self, key, material, layer, zone=None):
        self.buffers.append((key, material, layer, zone))
        return FakeBuffer(key)


class FunctionWorkTests(unittest.TestCase):
    def test_lowmark_smithy_has_open_front_workbays_and_clear_routes(self):
        ctx = FakeContext("LOWMARK")
        with patch.object(function_work, "Builder", FakeBuilder):
            function_work.build_smithy(ctx)
        _, kwargs, mass = ctx.masses[0]
        self.assertEqual(kwargs["open_edges"], [0, 1, 3])
        self.assertEqual([(a["s0"],a["s1"]) for a in kwargs["open_access"]],
                         [(.55,4.3),(5.3,8.9)])
        self.assertEqual({row[0] for row in ctx.program["routes"]},
                         {"forge_material_lane", "smithy.operator_workpad", "smithy.apron_clearance"})
        self.assertEqual(kwargs["roof"], "SHED")
        self.assertEqual(kwargs["pitch"], 18)
        self.assertEqual((kwargs["width"],kwargs["depth"],kwargs["floor_height"]),(9.6,4.6,3.5))
        self.assertEqual(ctx.decks[0][0], "smithy.work_apron")
        self.assertEqual(ctx.ramps[0][0], "smithy.material_ramp")
        self.assertTrue(any(row[0] == "hearth_stone_plinth" for row in ctx.boxes))
        self.assertTrue(any(row[0] == "smithy.external_flue" for row in ctx.buffers))
        self.assertGreater(mass.depth, 0)

    def test_thornfell_smithy_reserves_high_rear_wall_vent(self):
        ctx = FakeContext("THORNFELL")
        with patch.object(function_work, "Builder", FakeBuilder):
            function_work.build_smithy(ctx)
        _, kwargs, _ = ctx.masses[0]
        aperture = kwargs["open_access"][0]
        self.assertEqual(aperture["edge_index"], 0)
        self.assertEqual(aperture["height"], 2.8)
        self.assertEqual(kwargs["open_edges"], [0,3])


class ActualFunctionGenerationTests(unittest.TestCase):
    def _generate_and_validate(self, function, region):
        settings = Settings(function=function, region=region, world_aware=True,
                            use_grammar=True, detail="LOW", seed=91)
        plan, buffers = generate(settings)
        report = validate(plan, buffers)
        self.assertTrue(report["valid"], report.get("errors"))
        self.assertIsNotNone(plan.functional_program)
        self.assertTrue(plan.functional_program["routes"])
        return plan, buffers

    def _wall_hits(self, origin, direction, distance, buffers):
        return [(t,b) for t,b in _ray_hits(origin,direction,distance,buffers)
                if b.layer=="walls" or "facade_walls" in b.name]

    def test_lowmark_smithy_generates_and_validates_real_geometry(self):
        plan, buffers = self._generate_and_validate("SMITHY", "LOWMARK")
        self.assertEqual(plan.functional_program["function"], "SMITHY")
        self.assertTrue(any("external_flue" in buffer.name for buffer in buffers))
        mass=plan.world_zones[0]
        self.assertEqual(mass.plan.roof_mode,"SHED")
        self.assertEqual(mass.plan.settings.pitch,18)
        self.assertEqual(mass.plan.open_edges,{0,1,3})
        stack=next(buffer for buffer in buffers if "external_flue" in buffer.name)
        xs=[p[0] for p in stack.vertices]
        self.assertLess(max(xs),-.38,"Exterior stack overlaps the left roof overhang")
        self.assertEqual(stack.structural_role,"supported_hollow_masonry_flue")

    def test_thornfell_market_generates_and_validates_real_geometry(self):
        plan, buffers = self._generate_and_validate("MARKET_HALL", "THORNFELL")
        self.assertEqual(plan.functional_program["function"], "MARKET_HALL")
        self.assertEqual(len([row for row in plan.functional_program["stations"]
                              if "counter" in row["key"]]), 12)

    def test_lowmark_smithy_front_rays_reach_open_hearth(self):
        plan, buffers = self._generate_and_validate("SMITHY", "LOWMARK")
        mass=plan.world_zones[0]
        x=1.5
        hits=_ray_hits((x,-.1,mass.base+1),(0,1,0),mass.depth+.2,buffers)
        self.assertFalse(any(buffer.layer=="walls" and distance<.5
                             for distance,buffer in hits),
                         "Smithy front ray is blocked by a sealed front wall")
        hits=_ray_hits((x,-.1,mass.base+.46),(0,1,0),mass.depth+.2,buffers)
        self.assertTrue(any("hearth_firebed" in buffer.name
                            for _,buffer in hits),
                        "Open front does not reveal the forge hearth")

    def test_thornfell_market_aisle_rays_enter_and_cross_both_open_ends(self):
        plan, buffers = self._generate_and_validate("MARKET_HALL", "THORNFELL")
        mass=plan.world_zones[0]
        center=mass.width*.5
        for z in (mass.base+1,mass.base+2,mass.base+3):
            for x in (center-.8,center,center+.8):
                with self.subTest(z=z,x=x):
                    hits=_ray_hits((x,-.1,z),(0,1,0),mass.depth+.2,buffers)
                    self.assertEqual(hits,[],"Through-aisle clearance is obstructed")

    def test_all_regional_functional_pilots_generate_validate_and_admit_access_rays(self):
        for region in ("LOWMARK","THORNFELL","MIRE","EMBERHOLT"):
            with self.subTest(region=region,function="SMITHY"):
                smithy,buffers=self._generate_and_validate("SMITHY",region)
                mass=smithy.world_zones[0]
                hx={"LOWMARK":1.5,"THORNFELL":mass.width*.29,
                    "MIRE":mass.width*.25,"EMBERHOLT":mass.width*.25}[region]
                hits=_ray_hits((hx,-.1,mass.base+1),(0,1,0),mass.depth+.2,buffers)
                self.assertFalse(any(buf.layer=="walls" and t<.5 for t,buf in hits),
                                 "front workbay is blocked by a sealed facade")
                route=next(r for r in smithy.functional_program["routes"]
                           if r["key"]=="forge_material_lane")
                x0,y0,z0,x1,y1,z1=route["bounds"]
                origin=((x0+x1)*.5,y0+.025,mass.base+.45)
                wall_hits=self._wall_hits(origin,(0,1,0),mass.depth+1,buffers)
                self.assertTrue(wall_hits,"rear boundary probe did not reach a wall")
                rear_gap=wall_hits[0][0]-(y1-origin[1])
                self.assertGreaterEqual(rear_gap,.149,
                                        "material lane reaches into the closed rear wall")
                if region in ("THORNFELL","MIRE"):
                    side_origin=(x1-.025,(y0+y1)*.5,mass.base+.45)
                    side_hits=self._wall_hits(side_origin,(1,0,0),2,buffers)
                    self.assertTrue(side_hits,"right-side boundary probe did not reach a wall")
                    side_gap=side_hits[0][0]-(x1-side_origin[0])
                    self.assertGreaterEqual(side_gap,.149,
                                            "material lane reaches into the closed side wall")
            with self.subTest(region=region,function="MARKET_HALL"):
                market,buffers=self._generate_and_validate("MARKET_HALL",region)
                mass=market.world_zones[0]
                center=mass.width*.5
                aisle=2.35 if region=="THORNFELL" else 2.6
                for x in (center-.75,center,center+.75):
                    for height in (1,2):
                        hits=_ray_hits((x,-.1,mass.base+height),(0,1,0),mass.depth+.2,buffers)
                        self.assertEqual([(round(t,3),b.name) for t,b in hits],[],
                                         "public through-aisle ray is obstructed")
                if region=="MIRE":
                    self.assertTrue(any("linear_quay_boardwalk" in b.name for b in buffers))
                if region=="EMBERHOLT":
                    counters=[b for b in buffers if "counter" in b.name]
                    self.assertTrue(counters and all(b.material=="iron" for b in counters))
                if region in ("THORNFELL","EMBERHOLT","LOWMARK"):
                    wall=mass.plan.wall_thickness
                    for side,direction in (("west",(-1,0,0)),("east",(1,0,0))):
                        bay_number=1 if side=="west" else 3
                        route=next(r for r in market.functional_program["routes"]
                                   if r["key"]==f"{side}_bay_{bay_number}_front_seller_space")
                        x0,y0,_,x1,y1,_=route["bounds"]
                        x=x0+.025 if side=="west" else x1-.025
                        origin=(x,y0+.144,mass.base+.45)
                        hits=self._wall_hits(origin,direction,2,buffers)
                        self.assertTrue(hits,f"{side} vendor stand has no sidewall boundary")
                        clearance=hits[0][0]-.025
                        self.assertGreaterEqual(clearance,.149,
                                                f"{side} vendor stand enters the wall thickness")

    def test_market_hall_allocates_two_to_four_bays_without_aisle_stalls(self):
        for wealth, expected in (("MODEST", 2), ("ESTABLISHED", 3), ("AFFLUENT", 4)):
            with self.subTest(wealth=wealth):
                ctx = FakeContext("THORNFELL", wealth=wealth)
                with patch.object(function_work, "Builder", FakeBuilder):
                    function_work.build_market(ctx)
                self.assertEqual(len([row for row in ctx.boxes if "_counter" in row[0]]), expected*4)
                aisle = next(row for row in ctx.program["routes"] if row[0] == "public_through_aisle")
                self.assertLess(aisle[1][0], aisle[1][3])
                _, kwargs, _ = ctx.masses[0]
                self.assertEqual(kwargs["open_access"][0]["edge_index"], 0)
                self.assertEqual(kwargs["open_access"][1]["edge_index"], 2)

    def test_lowmark_market_is_a_through_hall(self):
        ctx = FakeContext("LOWMARK")
        with patch.object(function_work, "Builder", FakeBuilder):
            function_work.build_market(ctx)
        self.assertEqual(ctx.masses[0][1]["open_edges"], [0, 2])
        self.assertEqual([row["edge_index"] for row in ctx.masses[0][1]["open_access"]],[0,2])


if __name__ == "__main__":
    unittest.main()
