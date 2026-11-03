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
        self.name = key
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
        self.assertEqual(aperture["height"], 3.0)
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
        self.assertTrue(any(b.name.endswith("market.vendor_bay_frames")
                            and b.layer=="structure" for b in buffers))
        self.assertEqual(len([row for row in plan.functional_program["stations"]
                              if row["role"]=="market_counter"]), 6)

    def test_thornfell_smithy_is_a_front_visible_shallow_stone_workshop(self):
        plan,buffers=self._generate_and_validate("SMITHY","THORNFELL")
        mass=plan.world_zones[0]
        self.assertEqual(mass.bounds,(0,0,8.8,4.8))
        self.assertEqual(mass.plan.open_edges,{0,3})
        self.assertEqual(mass.plan.settings.floor_height,3.5)
        self.assertEqual(mass.plan.settings.pitch,42)
        self.assertEqual(mass.plan.roof_mode,"GABLE")
        stack=next(buffer for buffer in buffers if "external_flue" in buffer.name)
        self.assertLess(max(p[0] for p in stack.vertices),-.38)
        self.assertGreater(max(p[2] for p in stack.vertices),mass.eave+1.5)
        self.assertTrue(any(a["key"]=="smithy.material_ramp"
                            for a in plan.functional_program["approaches"]))

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
        station=next(s for s in plan.functional_program["stations"]
                     if s["key"].endswith(".anvil"))
        for actual,expected in zip(station["bounds"],(3.552,.92,1.10,4.512,1.48,1.44)):
            self.assertAlmostEqual(actual,expected)
        shaped=next(b for b in buffers if b.name.endswith(".anvil"))
        self.assertGreater(len(shaped.faces),6,"Anvil profile is still a single block")

    def test_thornfell_market_aisle_rays_enter_and_cross_both_open_ends(self):
        plan, buffers = self._generate_and_validate("MARKET_HALL", "THORNFELL")
        mass=plan.world_zones[0]
        center=mass.width*.5
        for z in (mass.base+1,mass.base+2,mass.base+2.75):
            for x in (center-.8,center,center+.8):
                with self.subTest(z=z,x=x):
                    hits=[(t,b) for t,b in _ray_hits((x,-.1,z),(0,1,0),mass.depth+.2,buffers)
                          if b.layer=="walls" or "facade_walls" in b.name]
                    self.assertEqual(hits,[],"Through-aisle clearance is obstructed")

    def test_lowmark_and_thornfell_markets_have_open_gables_and_supported_trusses(self):
        for region in ("LOWMARK","THORNFELL"):
            with self.subTest(region=region):
                plan,buffers=self._generate_and_validate("MARKET_HALL",region)
                mass=plan.world_zones[0]
                self.assertEqual(mass.plan.rects[0][4],"Y")
                self.assertEqual(mass.plan.open_edges,{0,2})
                truss=next(b for b in buffers if b.name.endswith("market.open_gable_trusses"))
                purlin=next(b for b in buffers if b.name.endswith("market.ridge_purlin"))
                self.assertTrue(truss.faces and purlin.faces)
                self.assertTrue(any(abs(x-mass.width*.5)<.1 and y<.5
                                    for x,y,z in truss.vertices),
                                "Front gable has no central kingpost")
                # A high approach ray checks that the end opening is real;
                # the tie/truss is deliberately above the functional clear box.
                hits=[(t,b) for t,b in _ray_hits((mass.width*.5,-.1,mass.base+2.2),
                                                  (0,1,0),.7,buffers)
                      if b.layer=="walls" or "facade_walls" in b.name]
                self.assertEqual(hits,[],"Open gable frontage is filled by a wall")

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
                if region in ("THORNFELL","MIRE","EMBERHOLT"):
                    self.assertGreaterEqual(route["bounds"][3]-route["bounds"][0],1.4)
                if region in ("THORNFELL","EMBERHOLT"):
                    self.assertTrue(any(a["key"]=="smithy.material_ramp"
                                        for a in smithy.functional_program["approaches"]))
                if region=="THORNFELL":
                    hearth_hits=_ray_hits((1.8,-.1,mass.base+.46),(0,1,0),mass.depth+.2,buffers)
                    self.assertTrue(any("hearth_firebed" in b.name for _,b in hearth_hits),
                                    "Thornfell front ray does not reach its forge")
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
                    route=next(r for r in market.functional_program["routes"]
                               if r["key"]=="market.quay_connector")
                    x0,y0,z0,x1,y1,z1=route["bounds"]
                    self.assertGreaterEqual(y1-y0,1.349,"quay connector is too narrow for public passage")
                    opening=next(a for a in mass.plan.functional_access if a["edge_index"]==1)
                    self.assertGreaterEqual(opening["s1"]-opening["s0"],1.5)
                    self.assertEqual(len([s for s in market.functional_program["stations"]
                                          if s["role"]=="market_counter"]),2*3)
                    probe=(x0+.025,(y0+y1)*.5,z0+2.0)
                    hits=_ray_hits(probe,(1,0,0),x1-x0-.05,buffers)
                    self.assertEqual(hits,[],"quay connector ray hits the open-edge facade frame")
                if region=="EMBERHOLT":
                    counters=[b for b in buffers if "counter" in b.name]
                    self.assertTrue(counters and all(b.material=="iron" for b in counters))
                aisle_left=(mass.width-aisle)*.5
                aisle_right=(mass.width+aisle)*.5
                for side in ("west","east"):
                    stands=[s for s in market.functional_program["stations"]
                            if s["role"]=="market_counter" and f"{side}_bay_" in s["key"]]
                    self.assertTrue(stands)
                    ordered=sorted(stands,key=lambda s:s["bounds"][1])
                    self.assertTrue(all(a["bounds"][1]<b["bounds"][1]
                                        for a,b in zip(ordered,ordered[1:])))
                    for stand in stands:
                        x0,y0,_,x1,y1,_=stand["bounds"]
                        self.assertGreater(y1-y0,.55,"vendor counter is too short to use")
                        if side=="west":
                            self.assertLess(x1,aisle_left,"west counter intrudes into the public aisle")
                        else:
                            self.assertGreater(x0,aisle_right,"east counter intrudes into the public aisle")
                        route_key=stand["key"].split(".")[-1].replace("_front_counter","_front_seller_space")
                        route=next(r for r in market.functional_program["routes"] if r["key"]==route_key)
                        a,b=route["bounds"],stand["bounds"]
                        overlap=[min(a[k+3],b[k+3])-max(a[k],b[k]) for k in range(3)]
                        self.assertLessEqual(min(overlap),.005,"seller route overlaps its counter")
                if region in ("LOWMARK","THORNFELL"):
                    approaches={a["key"] for a in market.functional_program["approaches"]}
                    self.assertTrue({"market.front_approach","market.rear_approach"}.issubset(approaches))

    def test_all_eight_function_profiles_repeat_seed_geometry_identically(self):
        for function in ("SMITHY","MARKET_HALL"):
            for region in ("LOWMARK","THORNFELL","MIRE","EMBERHOLT"):
                with self.subTest(function=function,region=region):
                    settings=Settings(function=function,region=region,world_aware=True,
                                      use_grammar=True,detail="LOW",seed=91)
                    _,first=generate(settings)
                    _,second=generate(settings)
                    signature=lambda buffers:[(b.name,b.material,b.layer,
                                               tuple(b.vertices),tuple(b.faces)) for b in buffers]
                    self.assertEqual(signature(first),signature(second))

    def test_market_hall_allocates_two_to_four_bays_without_aisle_stalls(self):
        for wealth, expected in (("MODEST", 2), ("ESTABLISHED", 3), ("AFFLUENT", 4)):
            with self.subTest(wealth=wealth):
                ctx = FakeContext("THORNFELL", wealth=wealth)
                with patch.object(function_work, "Builder", FakeBuilder):
                    function_work.build_market(ctx)
                self.assertEqual(len([row for row in ctx.program["stations"]
                                     if "_counter" in row["key"]]), expected*4)
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
