"""Small, usable plans for the forge and shared market hall.

These are working interpretations of the regional construction cues, not new
canon. Circulation is recorded separately from counters and equipment so game
clearance can be checked without treating the stalls as walkable space.
"""

from .functional import Builder


def _enum(value):
    return str(value or "").upper().replace(" ", "_").replace("-", "_")


def _wealth_capacity(settings):
    return {"MODEST": 2, "ESTABLISHED": 3, "AFFLUENT": 4}.get(
        _enum(settings.wealth), 3)


def _wall_thickness(region):
    return {"LOWMARK":.28,"THORNFELL":.50,"MIRE":.18,"EMBERHOLT":.70}.get(_enum(region),.28)


def _beam(ctx, key, material, start, end, width, height=None, zone=None):
    buf = ctx.buffer(key, material, "details", zone=zone)
    buf.beam(start, end, width, height if height is not None else width)
    return buf


def _smithy_flue(builder, mass, x, y, zbase):
    """Hood and outside stack vent through the open left wall without roof cuts."""
    ctx = builder.ctx
    # A shallow shed roof rises toward the closed rear; the hood is prominent
    # but stays well below the low front eave.
    hood_z = min(mass.eave - .50, zbase + 2.45)
    hood = ctx.buffer("smithy.forge_hood", "iron", "details", zone=mass)
    hood.structural_role = "forge_hood"
    lower_z=hood_z-.50; upper_z=hood_z+.22
    # Four sloped sheet panels form a truncated pyramid with an open underside
    # and a small top throat. The intake remains visibly open above the firebed.
    hood.extrude([(x-.82,y-.48,lower_z),(x+.82,y-.48,lower_z),
                  (x+.34,y-.24,upper_z),(x-.34,y-.24,upper_z)],(0,.065,0))
    hood.extrude([(x-.82,y+.48,lower_z),(x+.82,y+.48,lower_z),
                  (x+.34,y+.24,upper_z),(x-.34,y+.24,upper_z)],(0,-.065,0))
    hood.extrude([(x-.82,y-.48,lower_z),(x-.34,y-.24,upper_z),
                  (x-.34,y+.24,upper_z),(x-.82,y+.48,lower_z)],(.065,0,0))
    hood.extrude([(x+.82,y-.48,lower_z),(x+.34,y-.24,upper_z),
                  (x+.34,y+.24,upper_z),(x+.82,y+.48,lower_z)],(-.065,0,0))
    duct_z = upper_z
    outside_x = -1.05
    half=.34; wall=.09
    throat=ctx.buffer("smithy.flue_throat","iron","details",zone=mass)
    throat.structural_role="hollow_flue_throat"
    throat_end=outside_x+half-.045
    mid_x=(x+throat_end)*.5
    run=x-throat_end
    throat.box((mid_x,y-.12,duct_z),(run,.07,.24))
    throat.box((mid_x,y+.12,duct_z),(run,.07,.24))
    throat.box((mid_x,y,duct_z+.12),(run,.24,.07))
    # Leave the underside open over the hood's throat so rising smoke can turn
    # into the horizontal duct. The remaining bottom plate closes continuously
    # from the hood outlet to the stack interior.
    bottom_end=x+.34
    bottom_run=bottom_end-throat_end
    throat.box(((bottom_end+throat_end)*.5,y,duct_z-.12),
               (bottom_run,.24,.07))
    # Four continuous masonry walls enclose a hollow stack. Its nearest face is
    # beyond both the left roof overhang and the open side wall.
    flue = ctx.buffer("smithy.external_flue", "stone", "details", zone=mass)
    flue.structural_role = "supported_hollow_masonry_flue"
    top=duct_z+(2.6 if _enum(builder.region)=="THORNFELL" else
                1.8 if _enum(builder.region)=="EMBERHOLT" else 1.25)
    zmid=(.04+top)*.5; zheight=top-.04
    stack_x=outside_x
    flue.box((stack_x-half+wall/2,y,zmid),(wall,2*half,zheight))
    flue.box((stack_x+half-wall/2,y,zmid),(wall,2*half,zheight))
    flue.box((stack_x,y-half+wall/2,zmid),(2*half-2*wall,wall,zheight))
    flue.box((stack_x,y+half-wall/2,zmid),(2*half-2*wall,wall,zheight))
    # Open topped coping keeps the smoke channel unobstructed.
    for dx in (-half+wall/2,half-wall/2):
        flue.box((stack_x+dx,y,top+.035),(wall,2*half,.07))
    for dy in (-half+wall/2,half-wall/2):
        flue.box((stack_x,y+dy,top+.035),(2*half-2*wall,wall,.07))


def build_smithy(ctx):
    """Build one serviceable forge with separated hot work and handling lanes."""
    b = Builder(ctx, "SMITHY")
    if b.region == "LOWMARK":
        w,d,floor_height=9.6,4.6,3.5
    elif b.region == "THORNFELL":
        w,d,floor_height=8.8,4.8,3.5
    elif b.region == "MIRE":
        w,d,floor_height=max(10.5,b.settings.width),max(8.2,b.settings.depth),3.0
    elif b.region == "EMBERHOLT":
        w,d,floor_height=max(13.5,b.settings.width),max(9.0,b.settings.depth),3.6
    else:
        w,d,floor_height=max(8.4,b.settings.width),max(7.2,b.settings.depth),2.8
    region = _enum(b.region)
    # Lowmark's front and sides open to the hot work apron; the rear wall closes
    # against weather. Other regions retain their wind-sheltered rear vent.
    if region == "LOWMARK":
        rear_open = [0,1,3]
        open_access = [
            {"edge_index":0,"s0":.55,"s1":4.3,"height":3.0},
            {"edge_index":0,"s0":5.3,"s1":8.9,"height":3.0},
        ]
    elif region == "THORNFELL":
        rear_open=[0,3]
        vent_station=d*.42+.15
        wall_clear=_wall_thickness(region)+.15
        lane_x1=w-wall_clear
        open_access=[{"edge_index":0,"s0":.55,"s1":4.3,"height":3.0},
                     {"edge_index":0,"s0":lane_x1-1.4,"s1":lane_x1,"height":3.0},
                     {"edge_index":3,"s0":d-vent_station-.65,"s1":d-vent_station+.65,"height":2.7}]
    elif region == "MIRE":
        rear_open=[0,3]
        vent_station=d*.42+.15
        wall_clear=_wall_thickness(region)+.15
        lane_x1=w-wall_clear
        open_access=[{"edge_index":0,"s0":.55,"s1":w*.43,"height":2.7},
                     {"edge_index":0,"s0":lane_x1-1.4,"s1":lane_x1,"height":2.7},
                     {"edge_index":3,"s0":d-vent_station-.7,"s1":d-vent_station+.7,"height":2.7}]
    elif region == "EMBERHOLT":
        rear_open=[0,1,3]
        vent_station=d*.42+.15
        wall_clear=_wall_thickness(region)+.15
        lane_x1=w-wall_clear
        open_access=[{"edge_index":0,"s0":.55,"s1":w*.43,"height":3.1},
                     {"edge_index":0,"s0":lane_x1-1.4,"s1":lane_x1,"height":3.1},
                     {"edge_index":3,"s0":d-vent_station-.7,"s1":d-vent_station+.7,"height":3.1}]
    else:
        rear_open = []
        open_access = [{"edge_index": 2, "s0": w*.45, "s1": w*.55,
                        "height": 2.95}]
    mass = b.mass("forge_hall", x=0, y=0, width=w, depth=d,
                   floors=1, floor_height=floor_height, openings="NONE", entrance_edge=0,
                   roof="SHED" if region=="LOWMARK" else b.roof,
                   pitch=18 if region=="LOWMARK" else b.pitch,
                   open_edges=rear_open, open_access=open_access,
                   overhang=.42 if region == "LOWMARK" else .28)
    # Public/work access along the front; the main through lane is kept clear.
    if region == "LOWMARK":
        b.deck("smithy.work_apron",[(.2,-1.35),(4.9,-1.35),(4.9,0),(.2,0)],
               z=.04,material="stone",zone=mass)
        b.route("smithy.apron_clearance",(.2,-1.35,0,4.9,0,mass.base+.1),kind="human")
        b.ramp("smithy.material_ramp",(7.1,-2.0),(7.1,0),2.4,mass.base,
               zone=mass,material="stone")
        b.route("forge_material_lane", (5.35,.15,mass.base,8.85,d-mass.plan.wall_thickness-.15,mass.base+2.05), kind="material")
    elif region == "THORNFELL":
        wall_clear=mass.plan.wall_thickness+.15
        lane_x1=w-wall_clear
        lane_x0=lane_x1-1.4
        b.ramp("smithy.material_ramp",((lane_x0+lane_x1)*.5,-2.0),
               ((lane_x0+lane_x1)*.5,.15),1.4,mass.base,zone=mass,material="stone")
        b.route("smithy.material_ramp_clearance",(lane_x0,-2.0,0,lane_x1,.15,mass.base+.1),kind="material")
        b.route("forge_material_lane",(lane_x0,.15,mass.base,lane_x1,d-wall_clear,mass.base+2.05),kind="material")
    elif region == "MIRE":
        ramp_x=w*.75
        b.ramp("smithy.gentle_raised_approach",(ramp_x,-11.5),(ramp_x,-.05),2.2,mass.base,
               zone=mass,material="timber")
        b.route("smithy.ramp_clearance",(ramp_x-1.15,-11.5,mass.base-.05,
                                         ramp_x+1.15,-.05,mass.base+2.1),kind="human")
        b.route("forge_work_lane",(.55,.25,mass.base,w*.56,2.0,mass.base+2.1),kind="human")
        wall_clear=mass.plan.wall_thickness+.15
        lane_x1=w-wall_clear
        b.route("forge_material_lane",(lane_x1-1.4,1.9,mass.base,lane_x1,d-wall_clear,mass.base+2.05),kind="material")
    elif region == "EMBERHOLT":
        b.route("forge_work_lane",(.55,.25,mass.base,w*.58,2.0,mass.base+2.1),kind="human")
        wall_clear=mass.plan.wall_thickness+.15
        lane_x1=w-wall_clear
        b.ramp("smithy.material_ramp",(lane_x1-.7,-2.0),(lane_x1-.7,.2),1.4,mass.base,
               zone=mass,material="stone")
        b.route("smithy.material_ramp_clearance",(lane_x1-1.4,-2,0,lane_x1,.2,mass.base+.1),kind="material")
        b.route("forge_material_lane",(lane_x1-1.4,.2,mass.base,lane_x1,d-wall_clear,mass.base+2.05),kind="material")
    else:
        b.route("forge_work_lane", (.65,.25,mass.base,w-.65,2.0,mass.base+2.1), kind="human")
        wall_clear=mass.plan.wall_thickness+.15
        lane_x1=w-wall_clear
        b.route("forge_material_lane", (lane_x1-1.4,1.9,mass.base,lane_x1,d-wall_clear,mass.base+2.05), kind="material")
    # The Lowmark forge occupies the front-left bay, immediately legible from
    # the public approach; a right-side lane keeps stock and visitors clear.
    if region=="LOWMARK":
        hx,hy=1.5,1.2
    elif region=="THORNFELL":
        hx,hy=1.8,1.2
    elif region=="MIRE":
        hx,hy=w*.25,d*.42
    elif region=="EMBERHOLT":
        hx,hy=w*.25,d*.42
    else:
        hx,hy=w*.5,d*.58
    if region=="MIRE":
        b.deck("smithy.raised_fireproof_bank",
               [(max(.15,hx-2.2),hy-1.35),(hx+2.35,hy-1.35),
                (hx+2.35,hy+1.2),(max(.15,hx-2.2),hy+1.2)],
               z=mass.base,material="stone",zone=mass)
    b.box("hearth_stone_plinth", (hx-.95,hy-.85,mass.base+.04,hx+.95,hy+.85,mass.base+.45), "stone", mass, role="forge")
    # Open-front masonry hearth: the iron firebed is exposed above three low
    # curbs, facing the public workfront so the hot process reads from outside.
    b.box("hearth_firebed", (hx-.66,hy-.58,mass.base+.45,hx+.66,hy+.42,mass.base+.55), "iron", mass, role="forge_fire")
    b.box("hearth_left_curb", (hx-.76,hy-.65,mass.base+.45,hx-.60,hy+.53,mass.base+1.15), "stone", mass, role="forge")
    b.box("hearth_right_curb", (hx+.60,hy-.65,mass.base+.45,hx+.76,hy+.53,mass.base+1.15), "stone", mass, role="forge")
    b.box("hearth_rear_curb", (hx-.76,hy+.48,mass.base+.45,hx+.76,hy+.65,mass.base+1.15), "stone", mass, role="forge")
    ax=(w*.42 if region=="LOWMARK" else
        hx+1.1 if region in ("THORNFELL","MIRE") else w*.48)
    ay=hy
    b.box("anvil", (ax-.48,ay-.28,mass.base+.78,ax+.48,ay+.28,mass.base+1.12), "iron", mass, role="forge")
    horn=ctx.buffer("smithy.anvil_horn","iron","details",zone=mass)
    horn.structural_role="anvil_working_surface"
    horn.extrude([(ax-.12,ay-.24,mass.base+1.07),
                  (ax+.30,ay-.24,mass.base+1.07),
                  (ax+.03,ay-.24,mass.base+1.15)],(0,-.44,0))
    b.box("anvil_stump", (ax-.28,ay-.31,mass.base+.04,ax+.28,ay+.31,mass.base+.76), "timber", mass, role="forge")
    b.box("bellows", (hx-.98,hy+.70,mass.base+1.05,
                       hx-.10,hy+1.25,mass.base+1.77), "timber", mass, role="forge")
    if region in ("LOWMARK","THORNFELL","MIRE"):
        operator_x0=ax+.1 if region=="THORNFELL" else ax-.42
        operator_x1=ax+.85 if region=="THORNFELL" else ax+.52
        b.route("smithy.operator_workpad",(operator_x0,.12,mass.base,operator_x1,.62,mass.base+2.0),kind="human")
        if region=="LOWMARK":
            b.box("quench_trough", (4.75,1.8,mass.base+.04,5.25,2.5,mass.base+.42), "timber", mass, role="quench")
            b.box("coal_bin", (.35,3.05,mass.base+.04,1.25,3.75,mass.base+.88), "timber", mass, role="fuel")
        else:
            b.box("quench_trough", (hx+2.2,hy+.2,mass.base+.04,hx+3.0,hy+.9,mass.base+.42), "stone" if region=="MIRE" else "iron", mass, role="quench")
            b.box("coal_bin", (.35,d*.68,mass.base+.04,1.25,d*.68+.7,mass.base+.88), "timber", mass, role="fuel")
    else:
        b.box("quench_trough", (w*.74,d*.55,mass.base+.04,w*.74+1.05,d*.55+.65,mass.base+.42), "timber", mass, role="quench")
        b.box("coal_bin", (.4,d*.58,mass.base+.04,1.45,d*.58+.82,mass.base+.88), "timber", mass, role="fuel")
    if region=="EMBERHOLT":
        b.box("forge_slag_catch",(w*.64,hy+.55,mass.base+.04,w*.76,hy+1.2,mass.base+.52),"iron",mass,role="slag_bay")
        b.box("ingot_work_bench",(w*.62,hy+1.45,mass.base+.04,w*.77,hy+2.1,mass.base+.98),"iron",mass,role="material_bay")
    _smithy_flue(b, mass, hx, hy+.15, mass.base)
    # Structural rhythm carries the roof and reinforces the open face; these
    # posts are at the perimeter and outside all recorded circulation.
    if region!="MIRE":
        for i,x in enumerate((.3,w-.3)):
            post_top=mass.roof_height(x,d-.12)-.24
            _beam(ctx,f"smithy.bay_post_{i}","timber" if region=="LOWMARK" else "stone",
                  (x,d-.12,mass.base),(x,d-.12,post_top),.20,.20,mass)
    b.finish()


def build_market(ctx):
    """Build a public aisle flanked by repeated selling bays."""
    b = Builder(ctx, "MARKET_HALL")
    if b.region == "THORNFELL":
        w,d,floor_height=16.0,6.5,3.6
    elif b.region == "MIRE":
        w,d,floor_height=max(13.0,b.settings.width),max(7.2,b.settings.depth),3.0
    elif b.region == "EMBERHOLT":
        w,d,floor_height=max(14.0,b.settings.width),max(9.0,b.settings.depth),3.8
    else:
        w,d,floor_height=max(11.0,b.settings.width),max(8.0,b.settings.depth),2.8
    region=_enum(b.region)
    bays=_wealth_capacity(b.settings)
    # Thornfell protects the market from ridge wind with stone walls and paired
    # entries. Lowmark's timber hall opens at both ends for a direct public
    # passage. The remaining regions receive distinct covered arcade edges.
    if region == "LOWMARK":
        open_edges=[0,2]
        open_access=[{"edge_index":0,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.4},
                     {"edge_index":2,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.4}]
    elif region == "THORNFELL":
        open_edges=[0,2]
        open_access=[{"edge_index":0,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.8},
                     {"edge_index":2,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.8}]
    elif region == "MIRE":
        open_edges=[0,1,2]
        open_access=[{"edge_index":0,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.4},
                     {"edge_index":2,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.4}]
    elif region == "EMBERHOLT":
        open_edges=[0,2]
        open_access=[{"edge_index":0,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.7},
                     {"edge_index":2,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.7}]
    else:
        open_edges=[0,2]
        open_access=[]
    mass=b.mass("market_hall",x=0,y=0,width=w,depth=d,floors=1,floor_height=floor_height,
                entrance_edge=0,openings="NONE",open_edges=open_edges,
                open_access=open_access,overhang=.38)
    aisle_width=2.35 if region=="THORNFELL" else 2.6
    # A central through aisle spans the full depth. Counters occupy the outer
    # strips, each with a standing/vendor bay on its inner side.
    b.route("public_through_aisle", ((w-aisle_width)*.5,.25,mass.base,
            (w+aisle_width)*.5,d-.25,mass.base+2.25), kind="public")
    if region in ("LOWMARK","THORNFELL"):
        ramp_material="stone" if region=="THORNFELL" else "timber"
        for end,start_xy,floor_xy in (
                ("front",(w*.5,-2.0),(w*.5,.25)),
                ("rear",(w*.5,d+2.0),(w*.5,d-.25))):
            b.ramp(f"market.{end}_approach",start_xy,floor_xy,aisle_width,mass.base,
                   zone=mass,material=ramp_material)
            y0,y1=sorted((start_xy[1],floor_xy[1]))
            b.route(f"market.{end}_approach_clearance",
                    ((w-aisle_width)*.5,y0,0,(w+aisle_width)*.5,y1,mass.base+.1),kind="public")
    wall_clear=mass.plan.wall_thickness+.15
    side_width=(w-2*wall_clear-aisle_width)*.5
    for side, x0 in (("west",wall_clear),("east",wall_clear+side_width+aisle_width)):
        bay_width=(side_width-.55)/bays
        for i in range(bays):
            x=x0+i*bay_width
            cx0=x+.12; cx1=min(x+bay_width-.12,x0+side_width-.12)
            for end,cy0,cy1,seller_y0,seller_y1 in (
                    ("front",.70,1.38,1.48,2.20),
                    ("rear",d-1.38,d-.70,d-2.20,d-1.48)):
                b.box(f"{side}_bay_{i+1}_{end}_counter",
                      (cx0,cy0,mass.base+.04,cx1,cy1,mass.base+.96),
                      "iron" if region=="EMBERHOLT" else
                      "stone" if region=="THORNFELL" else "timber",
                      mass, role=f"stall_{side}_{i+1}_{end}")
                b.route(f"{side}_bay_{i+1}_{end}_seller_space",
                        (cx0,seller_y0,mass.base,cx1,seller_y1,mass.base+2.05),kind="service")
    if region=="MIRE":
        # Sorrowmere's raised trading hall meets a broad boardwalk on the open
        # river-facing side; the long ramp keeps the quay approach gentle.
        b.deck("market.linear_quay_boardwalk",[(w,0),(w+2.8,0),
                                                (w+2.8,d),(w,d)],
               z=mass.base,material="timber",zone=mass)
        qx=w+1.4
        b.ramp("market.quay_ramp",(qx,-11.5),(qx,-.05),2.6,mass.base,
               zone=mass,material="timber")
        b.route("market.quay_approach",(w+.1,-11.5,mass.base-.05,
                                         w+2.7,-.05,mass.base+2.0),kind="public")
        b.route("market.quay_connector",((w+aisle_width)*.5,d*.5-.7,mass.base,
                                          w+2.8,d*.5+.7,mass.base+2.2),kind="public")
    if region=="EMBERHOLT":
        # A broad stone public court precedes the paired iron trade-bay rows.
        center=w*.5
        b.deck("market.public_court_west",[(-2.0,-3.0),(center-1.5,-3.0),
                                            (center-1.5,0.0),(-2.0,0.0)],
               z=.04,material="stone",zone=mass)
        b.deck("market.public_court_east",[(center+1.5,-3.0),(w+2.0,-3.0),
                                            (w+2.0,0.0),(center+1.5,0.0)],
               z=.04,material="stone",zone=mass)
        b.ramp("market.court_ramp",(center,-2.5),(center,-.05),2.5,mass.base,
               zone=mass,material="stone")
        b.route("market.court_approach",(center-1.25,-2.5,0,center+1.25,-.05,mass.base+.1),kind="public")
    b.finish()
