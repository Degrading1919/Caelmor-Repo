"""Real-mesh aperture rays: glazing must occupy the opening, not a filled wall."""
import unittest

from caelmor_architecture.engine import build_roof, validate
from caelmor_architecture.facade import build_facades
from caelmor_architecture.model import Settings, make_plan
from caelmor_architecture.profiles import REGIONS


def _dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def _sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _ray_hits_mesh(origin, direction, distance, buffer):
    """Möller–Trumbore against the actual triangulated Buffer face geometry."""
    hits=[]
    for face in buffer.faces:
        a=buffer.vertices[face[0]]
        for i in range(1,len(face)-1):
            b,c=buffer.vertices[face[i]],buffer.vertices[face[i+1]]
            e1,e2=_sub(b,a),_sub(c,a)
            p=_cross(direction,e2)
            det=_dot(e1,p)
            if abs(det)<1e-10:
                continue
            inv=1.0/det
            tvec=_sub(origin,a)
            u=_dot(tvec,p)*inv
            if u< -1e-8 or u>1.0+1e-8:
                continue
            q=_cross(tvec,e1)
            v=_dot(direction,q)*inv
            if v< -1e-8 or u+v>1.0+1e-8:
                continue
            t=_dot(e2,q)*inv
            if 1e-6<t<distance-1e-6:
                hits.append(t)
    return sorted(hits)


class FacadeRaycastTests(unittest.TestCase):
    def test_window_ray_crosses_open_wall_and_hits_glass(self):
        configurations=[(region,"SOLID") for region in REGIONS]
        configurations.extend((region,"EFFICIENT") for region in ("THORNFELL","MIRE","EMBERHOLT"))
        for region,geometry_mode in configurations:
            with self.subTest(region=region,geometry_mode=geometry_mode):
                plan=make_plan(Settings(seed=73,function="COTTAGE",use_grammar=True,
                    region=region,context=REGIONS[region].default_context,
                    geometry_mode=geometry_mode))
                buffers=build_facades(plan)
                walls=[b for b in buffers if b.layer in ("walls", "cladding")]
                self.assertTrue(any(b.name=="facade_walls" for b in walls))
                glass=next(b for b in buffers if b.material=="glass")
                rays=0
                for record in plan.facade_records:
                    a,b=plan.edges[record["edge_index"]]
                    dx,dy=b[0]-a[0],b[1]-a[1]
                    length=(dx*dx+dy*dy)**.5
                    tx,ty=dx/length,dy/length
                    nx,ny=ty,-tx
                    for opening in record["openings"]:
                        if opening["kind"]!="window":
                            continue
                        s=(opening["s0"]+opening["s1"])*.5
                        z=(opening["z0"]+opening["z1"])*.5
                        x,y=a[0]+tx*s,a[1]+ty*s
                        origin=(x-nx*.45,y-ny*.45,z)
                        direction=(nx,ny,0.0)
                        with self.subTest(edge=record["edge_index"],s=round(s,3),z=round(z,3)):
                            for wall in walls:
                                self.assertFalse(_ray_hits_mesh(origin,direction,.80,wall),
                                    f"{region}/{geometry_mode}: {wall.name} fills a scheduled window")
                            self.assertTrue(_ray_hits_mesh(origin,direction,.80,glass),
                                f"{region}/{geometry_mode}: scheduled window has no glass")
                        rays+=1
                self.assertGreater(rays,0)

    def test_window_rays_clear_regional_cladding_buffers(self):
        for region in ("THORNFELL","MIRE","EMBERHOLT"):
            plan=make_plan(Settings(function="FARMHOUSE",region=region,
                                    use_grammar=True,seed=37))
            buffers=build_facades(plan)
            walls=next(b for b in buffers if b.name=="facade_walls")
            glass=next(b for b in buffers if b.material=="glass")
            skins=[b for b in buffers if b.name in
                   ("facade_masonry_skin","facade_board_skin")]
            self.assertTrue(skins)
            for record in plan.facade_records:
                a,b=plan.edges[record["edge_index"]]
                dx,dy=b[0]-a[0],b[1]-a[1]
                length=(dx*dx+dy*dy)**.5
                tx,ty=dx/length,dy/length
                nx,ny=ty,-tx
                for opening in record["openings"]:
                    if opening["kind"]!="window":
                        continue
                    s=(opening["s0"]+opening["s1"])*.5
                    z=(opening["z0"]+opening["z1"])*.5
                    x,y=a[0]+tx*s,a[1]+ty*s
                    origin=(x-nx*.45,y-ny*.45,z)
                    direction=(nx,ny,0.0)
                    with self.subTest(region=region,edge=record["edge_index"],s=round(s,3)):
                        self.assertFalse(_ray_hits_mesh(origin,direction,.80,walls))
                        self.assertTrue(_ray_hits_mesh(origin,direction,.80,glass))
                        for skin in skins:
                            self.assertFalse(_ray_hits_mesh(origin,direction,.80,skin),
                                f"{skin.name} fills a window assembly in {region}")

    def test_warehouse_hoist_and_market_porch_clear_their_roofs(self):
        for function in ("WAREHOUSE","MARKET_HALL"):
            with self.subTest(function=function):
                plan=make_plan(Settings(function=function,use_grammar=True,region="LOWMARK",
                                        wealth="ESTABLISHED",seed=41))
                facade=build_facades(plan)
                all_buffers=facade+build_roof(plan)
                report=validate(plan,all_buffers)
                self.assertTrue(report["valid"],report["errors"])
                openings=[o for row in plan.facade_records for o in row["openings"]]
                if function=="WAREHOUSE":
                    self.assertTrue(any(o.get("role")=="loading" for o in openings))
                    timber=next(b for b in facade if b.name=="facade_timber")
                    self.assertTrue(timber.faces)
                else:
                    porch=next(b for b in facade if b.name=="facade_porch")
                    roof=next(b for b in facade if b.name=="facade_porch_roof")
                    self.assertEqual(porch.roof_envelope["bounds"],roof.roof_envelope["bounds"])

    def test_efficient_cladding_keeps_solid_fronts_and_joint_reveals(self):
        for region in ("THORNFELL","MIRE","EMBERHOLT"):
            with self.subTest(region=region):
                base=dict(function="FARMHOUSE",region=region,use_grammar=True,
                          detail="MEDIUM",seed=53)
                solid=next(b for b in build_facades(make_plan(Settings(**base,geometry_mode="SOLID")))
                           if "_skin" in b.name)
                efficient=next(b for b in build_facades(make_plan(Settings(**base,geometry_mode="EFFICIENT")))
                               if "_skin" in b.name)
                self.assertEqual(solid.topology,"SOLID")
                self.assertEqual(efficient.topology,"SURFACE")
                self.assertEqual(solid.vertices,efficient.vertices)
                solid_face=efficient_face=vertex_offset=0
                while vertex_offset<len(solid.vertices):
                    n=len(solid.faces[solid_face])
                    self.assertEqual(efficient.faces[efficient_face],solid.faces[solid_face],
                                     "visible course face differs between geometry modes")
                    self.assertEqual(efficient.faces[efficient_face+1:efficient_face+1+n],
                                     solid.faces[solid_face+2:solid_face+2+n],
                                     "efficient mode dropped an exposed course joint reveal")
                    vertex_offset+=2*n
                    solid_face+=n+2
                    efficient_face+=n+1
                self.assertEqual(solid_face,len(solid.faces))
                self.assertEqual(efficient_face,len(efficient.faces))
                self.assertLess(sum(len(f)-2 for f in efficient.faces),
                                sum(len(f)-2 for f in solid.faces))

    def test_joint_pegs_follow_visible_framing_only(self):
        cases=(
            ("THORNFELL","ESTABLISHED",False),
            ("EMBERHOLT","ESTABLISHED",False),
            ("LOWMARK","AFFLUENT",False),
            ("LOWMARK","ESTABLISHED",True),
            ("MIRE","ESTABLISHED",True),
        )
        for region,wealth,has_pegs in cases:
            with self.subTest(region=region,wealth=wealth):
                plan=make_plan(Settings(function="FARMHOUSE",region=region,wealth=wealth,
                                        use_grammar=True,seed=41))
                facade=build_facades(plan)
                peg=next((b for b in facade if b.name=="facade_pegs"),None)
                self.assertEqual(peg is not None,has_pegs)
                if has_pegs:
                    self.assertTrue(peg.faces)
                    self.assertGreater(plan.style.frame_visibility,.16)
                else:
                    self.assertLessEqual(plan.style.frame_visibility,.16)

    def test_gatehouse_passage_aligns_with_usable_open_gallery_access(self):
        plan=make_plan(Settings(function="GATEHOUSE",use_grammar=True,seed=41))
        facade=build_facades(plan)
        passage=plan.passage_geometry
        self.assertTrue(passage["valid"])
        self.assertTrue(passage["alignment"]["centers_aligned"])
        self.assertGreaterEqual(passage["clear_width"],2.0)
        self.assertEqual({o["role"] for o in passage["openings"]},
                         {"passage_entry","passage_exit"})
        headroom=plan.gallery_headroom
        self.assertEqual(headroom["overhead_clearance"],"unroofed")
        access=[edge["access_opening"] for edge in headroom["edges"]
                if edge["access_opening"] is not None]
        self.assertEqual(len(access),1)
        self.assertGreaterEqual(access[0]["z1"]-access[0]["z0"],1.9)
        rails=next(b for b in facade if b.name=="facade_gallery_rails")
        self.assertEqual(rails.structural_role,"exterior_access")
        report=validate(plan,facade+build_roof(plan))
        self.assertTrue(report["valid"],report["errors"])

    def test_too_low_steep_gallery_access_does_not_create_inaccessible_deck(self):
        for function in ("WATCHTOWER","GATEHOUSE"):
            with self.subTest(function=function):
                plan=make_plan(Settings(function=function,footprint="RECT",floors=2,
                    floor_height=2.4,pitch=60.0,roof_style="HIP",use_grammar=False,seed=19))
                facade=build_facades(plan)
                roles=[o.get("role") for row in plan.facade_records
                       for o in row["openings"]]
                self.assertNotIn("gallery_access",roles)
                self.assertFalse(hasattr(plan,"gallery_headroom"))
                self.assertFalse(any(b.name in ("facade_gallery_deck","facade_gallery_rails")
                                     for b in facade))
                report=validate(plan,facade+build_roof(plan))
                self.assertTrue(report["valid"],report["errors"])

    def test_boathouse_slipway_and_rails_use_real_sloping_support(self):
        plan=make_plan(Settings(function="BOATHOUSE",region="MIRE",
                                context="SORROWMERE",use_grammar=True,seed=41))
        facade=build_facades(plan)
        ramp=next(b for b in facade if b.name=="facade_slipway")
        rails=next(b for b in facade if b.name=="facade_access_rails")
        self.assertGreaterEqual(max(v[2] for v in ramp.vertices)-min(v[2] for v in ramp.vertices),.7)
        self.assertEqual(rails.structural_role,"exterior_access")
        self.assertIsNotNone(rails.support_surface)
        report=validate(plan,facade+build_roof(plan))
        self.assertTrue(report["valid"],report["errors"])

    def test_door_leaf_spans_aperture_and_entry_steps_rise_in_supported_order(self):
        plan=make_plan(Settings(function="FARMHOUSE",footprint="RECT",seed=29))
        facade=build_facades(plan)
        door=next(o for r in plan.facade_records for o in r["openings"]
                  if o["kind"]=="door")
        door_mesh=next(b for b in facade if b.name=="facade_doors")
        self.assertLessEqual(min(v[2] for v in door_mesh.vertices),door["z0"]+.051)
        self.assertGreaterEqual(max(v[2] for v in door_mesh.vertices),door["z1"]-.04)

        record=next(r for r in plan.facade_records if door in r["openings"])
        a,b=plan.edges[record["edge_index"]]
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=(dx*dx+dy*dy)**.5
        nx,ny=dy/length,-dx/length
        steps=next(b for b in facade if b.name=="facade_steps")
        spans=[]
        for i in range(0,len(steps.vertices),8):
            verts=steps.vertices[i:i+8]
            if len(verts)!=8:
                continue
            z0,z1=min(v[2] for v in verts),max(v[2] for v in verts)
            depth=max((v[0]-a[0])*nx+(v[1]-a[1])*ny for v in verts)
            spans.append((z0,z1,depth))
        spans.sort()
        self.assertGreaterEqual(len(spans),2)
        self.assertAlmostEqual(spans[0][0],0.0,places=5)
        self.assertAlmostEqual(spans[-1][1],plan.foundation_height,places=5)
        self.assertTrue(all(lo[2]>hi[2] for lo,hi in zip(spans,spans[1:])),
                        "ascending stair treads must become shallower and rest on the lower riser")


if __name__=="__main__":
    unittest.main()
