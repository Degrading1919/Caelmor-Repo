"""Dependency-free world grammar coverage and semantic geometry checks.

Run with ordinary Python or Blender's bundled interpreter:
  blender --background --python tests/test_world.py
"""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from caelmor_architecture.engine import generate, validate, geometry_hash
from caelmor_architecture.model import Settings
from caelmor_architecture.profiles import TYPE_SPECS

REGIONS = ("LOWMARK", "THORNFELL", "MIRE", "EMBERHOLT")
FUNCTIONS = tuple(TYPE_SPECS)
WEALTH_LEVELS = ("MODEST", "ESTABLISHED", "AFFLUENT")


def _dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _ray_hits(origin, direction, distance, buffers):
    hits=[]
    for buffer in buffers:
        for face in buffer.faces:
            a=buffer.vertices[face[0]]
            for i in range(1,len(face)-1):
                b,c=buffer.vertices[face[i]],buffer.vertices[face[i+1]]
                e1,e2=_sub(b,a),_sub(c,a)
                p=_cross(direction,e2); det=_dot(e1,p)
                if abs(det)<1e-10: continue
                inv=1/det; tvec=_sub(origin,a); u=_dot(tvec,p)*inv
                if u < -1e-8 or u > 1+1e-8: continue
                q=_cross(tvec,e1); v=_dot(direction,q)*inv
                if v < -1e-8 or u+v > 1+1e-8: continue
                t=_dot(e2,q)*inv
                if 1e-6 < t < distance-1e-6: hits.append((t,buffer))
    return sorted(hits,key=lambda row:row[0])


class WorldGrammarTests(unittest.TestCase):
    def test_manual_world_envelope_ignores_unused_legacy_wings(self):
        for region in REGIONS:
            requested=Settings(region=region,world_aware=True,use_grammar=False,
                               width=6.,depth=4.,footprint='U',wing_width=5.,wing_depth=99.,detail='LOW')
            plan,buffers=generate(requested)
            self.assertTrue(validate(plan,buffers)['valid'])
            self.assertIs(plan.requested_settings,requested)
        with self.assertRaises(ValueError):
            generate(Settings(world_aware=False,width=6.,depth=4.,footprint='U',wing_width=5.,wing_depth=99.))
        with self.assertRaises(ValueError):
            generate(Settings(world_aware=True,use_grammar=False,width=5.,depth=4.))

    @staticmethod
    def _point_in_polygon(point, polygon):
        x,y=point
        inside=False
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            if ((a[1]>y)!=(b[1]>y)) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
                inside=not inside
        return inside

    @classmethod
    def _assert_gallery_doors_have_mesh_decks(cls,plan,buffers):
        """A scheduled upper door must land on a generated, outside platform top."""
        decks=[b for b in buffers if b.layer=="foundation" and
               any(term in b.name.lower() for term in ("deck","walk","platform","court"))]
        for mass in plan.world_zones:
            for record in mass.plan.facade_records:
                edge=mass.plan.edges[record["edge_index"]]
                length=math.dist(*edge)
                tx,ty=(edge[1][0]-edge[0][0])/length,(edge[1][1]-edge[0][1])/length
                for opening in record["openings"]:
                    if opening.get("role")!="gallery_access":continue
                    station=(opening["s0"]+opening["s1"])*.5
                    x=edge[0][0]+tx*station+ty*.10
                    y=edge[0][1]+ty*station-tx*.10
                    supported=False
                    for deck in decks:
                        for face in deck.faces:
                            vertices=[deck.vertices[i] for i in face]
                            if not all(abs(v[2]-opening["z0"])<.025 for v in vertices):continue
                            if cls._point_in_polygon((x,y),[(v[0],v[1]) for v in vertices]):
                                supported=True
                                break
                        if supported:break
                    if not supported:
                        raise AssertionError(f"{plan.settings.region}/{plan.settings.function}/"
                            f"{mass.key}: gallery door has no mesh deck outside threshold")

    @staticmethod
    def _assert_disjoint_occupied_masses(plan):
        """Independent swept-prism check, allowing only numerical/abutment epsilon."""
        zones=plan.world_zones
        for i,left in enumerate(zones):
            for right in zones[i+1:]:
                z_overlap=min(left.eave,right.eave)-max(left.base,right.base)
                if z_overlap<=.025:
                    continue
                for a0,b0,a1,b1,_axis in left.plan.rects:
                    for c0,d0,c1,d1,_other in right.plan.rects:
                        dx=min(a1,c1)-max(a0,c0)
                        dy=min(b1,d1)-max(b0,d0)
                        if dx>.025 and dy>.025:
                            raise AssertionError(
                                f"occupied masses {left.key}/{right.key} overlap "
                                f"{dx:.3f} x {dy:.3f} x {z_overlap:.3f}m")

    def test_low_detail_region_function_seed_matrix(self):
        checked=0
        for region in REGIONS:
            for function in FUNCTIONS:
                for wealth in WEALTH_LEVELS:
                    settings=Settings(seed=91,function=function,region=region,
                        wealth=wealth,craftsmanship="STANDARD",detail="LOW",
                        use_grammar=True,world_aware=True)
                    with self.subTest(region=region,function=function,wealth=wealth):
                        plan,buffers=generate(settings)
                        report=validate(plan,buffers)
                        self.assertTrue(report["valid"], report["errors"][:8])
                        self.assertEqual(report["architecture"],"WORLD")
                        self.assertTrue(plan.world_zones)
                        self.assertTrue(all(row["valid"] for row in report["construction_zones"]))
                        self.assertEqual(len(buffers),len({buffer.name for buffer in buffers}),
                                         "World buffer names must be unique per construction zone")
                        self._assert_disjoint_occupied_masses(plan)
                        self._assert_gallery_doors_have_mesh_decks(plan,buffers)
                    checked+=1
        self.assertEqual(checked,len(REGIONS)*len(FUNCTIONS)*len(WEALTH_LEVELS))

    def test_selected_wealth_detail_geometry_modes_validate(self):
        for region in REGIONS:
            for wealth in ("ESTABLISHED","AFFLUENT"):
                for mode in ("SOLID","EFFICIENT"):
                    with self.subTest(region=region,wealth=wealth,mode=mode):
                        s=Settings(seed=91,function="COTTAGE",region=region,wealth=wealth,
                            detail="HIGH",geometry_mode=mode,use_grammar=True,world_aware=True)
                        plan,buffers=generate(s)
                        result=validate(plan,buffers)
                        self.assertTrue(result["valid"],result["errors"][:8])
                        self.assertEqual(result["architecture"],"WORLD")

    def test_world_generation_is_deterministic_and_legacy_path_remains_available(self):
        world=Settings(seed=91,function="COTTAGE",region="MIRE",use_grammar=True,world_aware=True)
        p1,b1=generate(world); p2,b2=generate(world)
        self.assertEqual(geometry_hash(b1),geometry_hash(b2))
        self.assertTrue(validate(p1,b1)["valid"])
        for settings in (Settings(),Settings(seed=91,function="COTTAGE",use_grammar=True)):
            plan,buffers=generate(settings)
            self.assertFalse(hasattr(plan,"world_zones"))
            self.assertTrue(validate(plan,buffers)["valid"])

    def test_world_window_ray_passes_the_real_opening_and_hits_glass(self):
        for region in REGIONS:
            with self.subTest(region=region):
                plan,buffers=generate(Settings(seed=73,function="FARMHOUSE",region=region,
                    detail="LOW",use_grammar=True,world_aware=True))
                walls=[b for b in buffers if b.layer in ("walls","cladding")]
                glass=[b for b in buffers if b.material=="glass"]
                windows=0
                for record in plan.facade_records:
                    a,b=plan.edges[record["edge_index"]]
                    dx,dy=b[0]-a[0],b[1]-a[1]
                    length=(dx*dx+dy*dy)**.5
                    tx,ty=dx/length,dy/length
                    nx,ny=ty,-tx
                    for opening in record["openings"]:
                        if opening["kind"]!="window": continue
                        s=(opening["s0"]+opening["s1"])*.5
                        z=(opening["z0"]+opening["z1"])*.5
                        x,y=a[0]+tx*s,a[1]+ty*s
                        origin=(x-nx*.45,y-ny*.45,z)
                        wall_hits=_ray_hits(origin,(nx,ny,0),.80,walls)
                        self.assertFalse(wall_hits,
                            f"{region}/{record['construction_zone']}: wall closes scheduled window")
                        glass_hits=_ray_hits(origin,(nx,ny,0),.80,glass)
                        self.assertTrue(glass_hits,
                            f"{region}/{record['construction_zone']}: no glazing at scheduled window")
                        windows+=1
                self.assertGreater(windows,0)

    def test_shared_party_edges_are_blind(self):
        for region in REGIONS:
            plan,buffers=generate(Settings(seed=29,function="COTTAGE",region=region,
                detail="LOW",use_grammar=True,world_aware=True))
            def same_edge(left,right):
                return ((all(abs(x-y)<1e-6 for x,y in zip(left[0],right[1])) and
                         all(abs(x-y)<1e-6 for x,y in zip(left[1],right[0]))) or
                        (all(abs(x-y)<1e-6 for x,y in zip(left[0],right[0])) and
                         all(abs(x-y)<1e-6 for x,y in zip(left[1],right[1]))))
            for i,first in enumerate(plan.world_zones):
                for second in plan.world_zones[i+1:]:
                    for edge_index,edge in enumerate(first.plan.edges):
                        if not any(same_edge(edge,other) for other in second.plan.edges): continue
                        rec=next(r for r in plan.facade_records
                                 if r["construction_zone"]==first.key and r["edge_index"]==
                                 sum(len(m.plan.edges) for m in plan.world_zones[:i])+edge_index)
                        self.assertFalse(rec["openings"],(region,first.key,second.key,edge_index))

    def test_access_surfaces_have_explicit_support_and_stairs_reach_the_platform(self):
        for region in ("MIRE","THORNFELL","EMBERHOLT"):
            plan,buffers=generate(Settings(seed=41,function="INN",region=region,
                detail="LOW",use_grammar=True,world_aware=True))
            access=[b for b in buffers if b.structural_role=="exterior_access"]
            for b in access:
                self.assertIsNotNone(b.support_surface,b.name)
                x0,y0,x1,y1=b.support_surface["bounds"]
                a,c,d=b.support_surface["plane"]
                for x,y,z in b.vertices:
                    self.assertGreaterEqual(x,x0-1e-4,b.name)
                    self.assertLessEqual(x,x1+1e-4,b.name)
                    self.assertGreaterEqual(y,y0-1e-4,b.name)
                    self.assertLessEqual(y,y1+1e-4,b.name)
                    self.assertGreaterEqual(z,a*x+c*y+d-.10-1e-5,b.name)
                    self.assertLessEqual(z,a*x+c*y+d+1.10001,b.name)
            stairs=[b for b in buffers if "stair" in b.name.lower()]
            if region=="MIRE":
                self.assertTrue(stairs,"raised Mire inn must provide stairs")
                self.assertTrue(any(min(v[2] for v in b.vertices)<=.05 for b in stairs))


if __name__ == "__main__":
    sys.argv=[sys.argv[0]]
    unittest.main(verbosity=2)
