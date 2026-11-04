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


def _station_fixture(builder, key, material, zone, role, bounds):
    """Create detailed geometry while retaining the station's stable AABB."""
    buf = builder.ctx.buffer(key, material, "details", zone=zone)
    buf.functional_role = role
    builder.program["stations"].append({
        "key": buf.name, "role": role, "bounds": bounds,
        "zone": getattr(zone,"key",None) if zone else None,
    })
    return buf


def _open_bin(builder, key, bounds, material, zone, role, *, slatted=False):
    """A hollow, open-top working bin with the original station bounds."""
    x0,y0,z0,x1,y1,z1=bounds
    buf=_station_fixture(builder,key,material,zone,role,bounds)
    wall=min(.09,(x1-x0)*.14,(y1-y0)*.14)
    floor=min(.09,(z1-z0)*.18)
    buf.box(((x0+x1)*.5,(y0+y1)*.5,z0+floor*.5),(x1-x0-2*wall,y1-y0-2*wall,floor))
    # Side walls leave a real open top. Coal bins use spaced boards so the
    # contents remain visible; the quench trough is continuous and fireproof.
    for side in (0,1):
        x=x0+wall*.5 if side==0 else x1-wall*.5
        if slatted:
            count=3
            for i in range(count):
                z=z0+floor+.10+(z1-z0-floor-.16)*(i+.5)/count
                buf.box((x,(y0+y1)*.5,z),(wall,y1-y0,.075))
        else:
            buf.box((x,(y0+y1)*.5,(z0+floor+z1)*.5),(wall,y1-y0,z1-z0-floor))
    for side in (0,1):
        y=y0+wall*.5 if side==0 else y1-wall*.5
        if slatted:
            count=3
            for i in range(count):
                z=z0+floor+.10+(z1-z0-floor-.16)*(i+.5)/count
                buf.box(((x0+x1)*.5,y,z),(x1-x0,wall,.075))
        else:
            buf.box(((x0+x1)*.5,y,(z0+floor+z1)*.5),(x1-x0-2*wall,wall,z1-z0-floor))
    return buf


def _market_counter(builder, key, bounds, material, zone):
    """Legged counter with a lower shelf and a shallow, divided display top."""
    x0,y0,z0,x1,y1,z1=bounds
    buf=_station_fixture(builder,key,material,zone,"market_counter",bounds)
    leg=min(.10,(x1-x0)*.16,(y1-y0)*.14)
    top_z=z1-.12
    for x in (x0+leg*.75,x1-leg*.75):
        for y in (y0+leg*.75,y1-leg*.75):
            buf.box((x,y,(z0+top_z)*.5),(leg,leg,top_z-z0))
    buf.box(((x0+x1)*.5,(y0+y1)*.5,top_z+.06),(x1-x0,y1-y0,.12))
    shelf_z=z0+(top_z-z0)*.43
    buf.box(((x0+x1)*.5,(y0+y1)*.5,shelf_z),(x1-x0-2*leg,y1-y0-2*leg,.07))
    # Low dividers keep produce or small goods in the stall's footprint and
    # give the counter a clear working/display face in clay renders.
    rail=min(.055,(y1-y0)*.12)
    for y in (y0+rail*.5,y1-rail*.5):
        buf.box(((x0+x1)*.5,y,top_z+.12+rail*.5),(x1-x0,rail,rail))
    for x in (x0+rail*.5,x1-rail*.5):
        buf.box((x,(y0+y1)*.5,top_z+.12+rail*.5),(rail,y1-y0-2*rail,rail))
    return buf


def _market_back_shelf(builder, key, bounds, material, zone):
    """Open two-tier stock shelf paired with a customer-side counter."""
    x0,y0,z0,x1,y1,z1=bounds
    buf=_station_fixture(builder,key,material,zone,"market_stock_shelf",bounds)
    post=min(.07,(x1-x0)*.18,(y1-y0)*.12)
    for x in (x0+post*.7,x1-post*.7):
        for y in (y0+post*.7,y1-post*.7):
            buf.box((x,y,(z0+z1)*.5),(post,post,z1-z0))
    for z in (z0+.12,z0+(z1-z0)*.56):
        buf.box(((x0+x1)*.5,(y0+y1)*.5,z),(x1-x0-2*post,y1-y0-2*post,.075))
    # A back rail prevents stock from slipping while leaving the front open.
    buf.box(((x0+x1)*.5,y1-post*.5,(z0+z1)*.5),(x1-x0,post,z1-z0))
    return buf


def _market_vendor_frames(builder, mass, bays, aisle_left, aisle_right, margin, material,
                          rear_margin=None):
    """Build roof-contained aisle-edge bents aligned to vendor-bay breaks."""
    ctx=builder.ctx
    d=mass.depth
    rear_margin=margin if rear_margin is None else rear_margin
    step=(d-margin-rear_margin)/bays
    stations=[margin+i*step for i in range(bays+1)]
    frame=ctx.buffer("market.vendor_bay_frames",material,"structure",mass)
    frame.structural_role="market_vendor_bay_load_path"
    for side in ("west","east"):
        inner=aisle_left-.30 if side=="west" else aisle_right+.30
        outer=aisle_left-2.85 if side=="west" else aisle_right+2.85
        for y in stations:
            zroof=min(mass.roof_height(x,y) for x in (outer,inner))
            top=zroof-.56
            for x in (outer,inner):
                frame.box((x,y,(mass.base+top)*.5),(.20,.20,top-mass.base))
            frame.beam((outer,y,top-.08),(inner,y,top-.08),.20,.16)
        # Side lintels connect the bay posts into a legible covered arcade.
        for y0,y1 in zip(stations,stations[1:]):
            x=outer if side=="west" else inner
            z0=min(mass.roof_height(x,y0),mass.roof_height(x,y1))-.62
            z1=min(mass.roof_height(x,y0),mass.roof_height(x,y1))-.62
            frame.beam((x,y0,z0),(x,y1,z1),.16,.16)


def _market_open_gables(builder, mass, tie_clearance):
    """Frame the open end gables and carry their ridge into the vendor bays."""
    ctx=builder.ctx
    width,depth=mass.width,mass.depth
    x0,x1=.34,width-.34
    ridge=width*.5
    tie_z=mass.base+tie_clearance+.08
    truss=ctx.buffer("market.open_gable_trusses","timber","structure",mass)
    truss.structural_role="market_open_gable_end_truss"
    ends=(.24,depth-.24)
    for y in ends:
        eave_z=[mass.roof_height(x,y)-.32 for x in (x0,x1)]
        # Bearing posts sit at the ends of the public opening; the tie remains
        # above its clear route, while the central aisle stays unobstructed.
        for x,z in zip((x0,x1),eave_z):
            truss.box((x,y,(mass.base+z)*.5),(.20,.20,z-mass.base))
        truss.beam((x0,y,tie_z),(x1,y,tie_z),.16,.16)
        truss.beam((x0,y,eave_z[0]),(ridge,y,mass.roof_height(ridge,y)-.42),.16,.18)
        truss.beam((ridge,y,mass.roof_height(ridge,y)-.42),(x1,y,eave_z[1]),.16,.18)
        truss.beam((ridge,y,tie_z+.08),(ridge,y,mass.roof_height(ridge,y)-.50),.14,.14)
        for x in (width*.32,width*.68):
            z=mass.roof_height(x,y)-.48
            truss.beam((ridge,y,tie_z+.15),(x,y,z),.12,.12)
    purlin=ctx.buffer("market.ridge_purlin","timber","structure",mass)
    purlin.structural_role="gable_truss_supported_ridge_purlin"
    z=mass.roof_height(ridge,depth*.5)-.50
    purlin.beam((ridge,ends[0],z),(ridge,ends[1],z),.18,.20)


def _smithy_flue(builder, mass, x, y, zbase):
    """Hood and outside stack vent through the open left wall without roof cuts."""
    ctx = builder.ctx
    # A shallow shed roof rises toward the closed rear; the hood is prominent
    # but stays well below the low front eave.
    hood_z = min(mass.eave - .50, zbase + 2.45)
    if builder.region=='THORNFELL':hood_z-=.08
    hood = ctx.buffer("smithy.forge_hood", "iron", "details", zone=mass)
    hood.structural_role = "forge_hood"
    prominent = builder.region=='LOWMARK' and ctx.construction_resolver is not None
    lower_z=hood_z-(.28 if prominent else .50)
    upper_z=hood_z+.22
    front=y-(.34 if prominent else .48)
    half_width=1.02 if prominent else .82
    # Four sloped sheet panels form a truncated pyramid with an open underside
    # and a small top throat. The intake remains visibly open above the firebed.
    hood.extrude([(x-half_width,front,lower_z),(x+half_width,front,lower_z),
                  (x+.34,y-.24,upper_z),(x-.34,y-.24,upper_z)],(0,.065,0))
    hood.extrude([(x-half_width,y+.48,lower_z),(x+half_width,y+.48,lower_z),
                  (x+.34,y+.24,upper_z),(x-.34,y+.24,upper_z)],(0,-.065,0))
    hood.extrude([(x-half_width,front,lower_z),(x-.34,y-.24,upper_z),
                  (x-.34,y+.24,upper_z),(x-half_width,y+.48,lower_z)],(.065,0,0))
    hood.extrude([(x+half_width,front,lower_z),(x+.34,y-.24,upper_z),
                  (x+.34,y+.24,upper_z),(x+half_width,y+.48,lower_z)],(-.065,0,0))
    if prominent:
        hood.chamfered_beam((x-half_width,front,lower_z),(x+half_width,front,lower_z),
                            .086,.091,.012)
    # Rise above the tapered hood before turning sideways; a horizontal run at
    # its rim would cut through the hood's own sloping side panel.
    duct_z = upper_z+(.36 if builder.region=='MIRE' else .18)
    outside_x = -1.05
    half=.34; wall=.09
    throat=ctx.buffer("smithy.flue_throat","iron","details",zone=mass)
    throat.structural_role="hollow_flue_throat"
    for side in (-1,1):
        neck_top=duct_z-.155 if side<0 else duct_z+.12
        throat.box((x+side*.12,y,(upper_z+neck_top)*.5),(.07,.24,neck_top-upper_z))
        throat.box((x,y+side*.12,(upper_z+duct_z+.12)*.5),(.24,.07,duct_z+.12-upper_z))
    throat.box((x+.0775,y,duct_z+.12),(.155,.24,.07))
    # Reducer flange joins the broad open hood mouth to the hollow vertical neck.
    for side in (-1,1):
        throat.box((x+side*(.34+.085)*.5,y,upper_z),(.34-.085,.48,.03))
        throat.box((x,y+side*(.24+.085)*.5,upper_z),(.17,.24-.085,.03))
    throat_end=outside_x+half-wall-.03
    mid_x=(x+throat_end)*.5
    run=x-throat_end
    throat.box((mid_x,y-.12,duct_z),(run,.07,.24))
    throat.box((mid_x,y+.12,duct_z),(run,.07,.24))
    throat.box((mid_x,y,duct_z+.12),(run,.24,.07))
    # Leave the underside open over the hood's throat so rising smoke can turn
    # into the horizontal duct. The remaining bottom plate closes continuously
    # from the hood outlet to the stack interior.
    bottom_end=x-.12
    bottom_run=bottom_end-throat_end
    throat.box(((bottom_end+throat_end)*.5,y,duct_z-.12),
               (bottom_run,.24,.07))
    # Four continuous masonry walls enclose a hollow stack. Its nearest face is
    # beyond both the left roof overhang and the open side wall.
    flue = ctx.buffer("smithy.external_flue", "stone", "details", zone=mass)
    flue.structural_role = "supported_hollow_masonry_flue"
    top=duct_z+(2.6 if _enum(builder.region)=="THORNFELL" else
                1.8 if _enum(builder.region)=="EMBERHOLT" else 1.25)
    if builder.region=='LOWMARK':
        top=max(top,mass.roof_height(mass.width*.5,mass.depth*.5)+.65)
    zmid=(.04+top)*.5; zheight=top-.04
    stack_x=outside_x
    flue.box((stack_x-half+wall/2,y,zmid),(wall,2*half,zheight))
    # The duct enters the right wall through a genuine aperture. A hollow
    # shaft with an uncut inlet wall would still be a sealed exhaust path.
    wall_x=stack_x+half-wall/2
    inlet_low,inlet_high=duct_z-.20,duct_z+.20
    flue.box((wall_x,y,(.04+inlet_low)*.5),(wall,2*half,inlet_low-.04))
    flue.box((wall_x,y,(inlet_high+top)*.5),(wall,2*half,top-inlet_high))
    for side in (-1,1):
        flue.box((wall_x,y+side*(half+.20)*.5,duct_z),(wall,half-.20,.40))
    flue.box((stack_x,y-half+wall/2,zmid),(2*half-2*wall,wall,zheight))
    flue.box((stack_x,y+half-wall/2,zmid),(2*half-2*wall,wall,zheight))
    # Open topped coping keeps the smoke channel unobstructed.
    for dx in (-half+wall/2,half-wall/2):
        flue.box((stack_x+dx,y,top+.035),(wall,2*half,.07))
    for dy in (-half+wall/2,half-wall/2):
        flue.box((stack_x,y+dy,top+.035),(2*half-2*wall,wall,.07))
    builder.program['ventilation']={
        'hood_inlet':[(x,y,zbase+.65),(x,y,duct_z+.04)],
        'duct':[(x,y,duct_z),(outside_x,y,duct_z)],
        'stack':[(outside_x,y,duct_z),(outside_x,y,top+.18)],
        'scope':'Open geometric air path, not a draft or thermal simulation'}


def _smithy_bay_frame(builder, mass, x0, x1, y0, y1, material):
    """A small roof-supported work bay, kept around rather than over the forge."""
    ctx=builder.ctx
    frame=ctx.buffer("smithy.hot_bay_frame",material,"structure",mass)
    frame.structural_role="forge_bay_load_path"
    posts=((x0,y0),(x1,y0),(x0,y1),(x1,y1))
    tops=[]
    for x,y in posts:
        top=mass.roof_height(x,y)-.58
        tops.append(top)
        frame.box((x,y,(mass.base+top)*.5),(.16,.16,top-mass.base))
    # Eaves and ties follow the roof's rise. Each member's top remains below
    # the host weather surface so the forge frame never becomes a roof cut.
    for i,(a,b) in enumerate(((0,1),(2,3),(0,2),(1,3))):
        p0,p1=posts[a],posts[b]
        z0,z1=tops[a],tops[b]
        frame.beam((p0[0],p0[1],z0-.08),(p1[0],p1[1],z1-.08),.16,.16)


def build_smithy(ctx):
    """Build one serviceable forge with separated hot work and handling lanes."""
    b = Builder(ctx, "SMITHY")
    seed_profile = None
    if b.region == "LOWMARK" and getattr(b.settings, "seed_massing", False):
        # Seed the architectural arrangement independently from surface and
        # furnishing variation. Service stations stay anchored in the forge;
        # only the hall shell and the dry stock range change shape.
        capacity = ctx.rng("smithy.stock_capacity").random()
        site_width = ctx.rng("smithy.site_width").random()
        weather = ctx.rng("smithy.weather").random()
        growth = ctx.rng("smithy.growth").random()
        hall_width = round(5.4+site_width*1.2, 2)
        depth = round(4.9+(1.0-growth)*.9, 2)
        # A taller forge bay carries its smoke hood and leaves a useful roof
        # shoulder above the lower stock range at their shared eaves.
        floor_height = round(3.8+site_width*.4, 2)
        pitch = round(30.0+weather*8.0, 1)
        stock_width = round(3.8+capacity, 2)
        stock_setback = round(.18+growth*.87, 2)
        # Larger stock needs a second bent and the independent cross-gable;
        # narrow, accreted ranges retain the outward-draining shed roof.
        extra_stock_bent = stock_width >= 4.30 and depth-stock_setback >= 4.5
        stock_roof = ("GABLE" if capacity > .5 or growth < .25 else "SHED")
        stock_pitch = round(10.0+capacity, 1)
        sweep = (round(.28+weather*.06, 3)
                 if b.settings.crafted_curves and weather < .6 else 0.0)
        seed_profile = {
            "hall_width": hall_width, "depth": depth,
            "floor_height": floor_height, "pitch": pitch,
            "stock_width": stock_width, "stock_setback": stock_setback,
            "stock_roof": stock_roof, "stock_pitch": stock_pitch,
            "stock_floor_height": 2.55,
            "extra_stock_bent": extra_stock_bent,
            "swept_eaves": sweep,
        }

    if b.region == "LOWMARK":
        w,d,floor_height=9.6,5.2,3.6
    elif b.region == "THORNFELL":
        w,d,floor_height=8.8,4.8,3.5
    elif b.region == "MIRE":
        w,d,floor_height=max(10.5,b.settings.width),max(8.2,b.settings.depth),3.0
    elif b.region == "EMBERHOLT":
        w,d,floor_height=max(13.5,b.settings.width),max(9.0,b.settings.depth),3.6
    else:
        w,d,floor_height=max(8.4,b.settings.width),max(7.2,b.settings.depth),2.8
    region = _enum(b.region)
    if seed_profile is not None:
        d = seed_profile["depth"]
        floor_height = seed_profile["floor_height"]
    # Lowmark's front and sides open to the hot work apron; the rear wall closes
    # against weather. Other regions retain their wind-sheltered rear vent.
    if region == "LOWMARK":
        rear_open = [0,1,3]
        if seed_profile is None:
            open_access = [
                {"edge_index":0,"s0":.55,"s1":4.3,"height":3.0},
                {"edge_index":0,"s0":5.3,"s1":8.9,"height":3.0},
            ]
        else:
            # Reserve one broad, in-bounds working frontage for the hot bay.
            open_access = [{"edge_index":0,"s0":.55,
                            "s1":min(4.3,seed_profile["hall_width"]-.30),
                            "height":3.0}]
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
    if seed_profile is None:
        sweep = (b.ctx.rng('smithy.eaves').uniform(.28,.34)
                 if region == 'LOWMARK' and b.settings.crafted_curves else 0.)
        hall_width = 5.6 if region == 'LOWMARK' else w
        mass_pitch = 32 if region == "LOWMARK" else b.pitch
    else:
        sweep = seed_profile["swept_eaves"]
        hall_width = seed_profile["hall_width"]
        mass_pitch = seed_profile["pitch"]
    mass = b.mass("forge_hall", x=0, y=0, width=hall_width if region=='LOWMARK' else w, depth=d,
                   floors=1, floor_height=floor_height, openings="NONE", entrance_edge=0,
                   roof=b.roof,roof_axis='Y' if region=='LOWMARK' else 'X',
                   pitch=mass_pitch,
                   open_edges=rear_open, open_access=open_access,
                   overhang=.42 if region == "LOWMARK" else .28,
                   frame_visibility=0. if region=='LOWMARK' else None,swept_eaves=sweep)
    # Public/work access along the front; the main through lane is kept clear.
    if region == "LOWMARK":
        b.deck("smithy.work_apron",[(.2,-1.35),(4.9,-1.35),(4.9,0),(.2,0)],
               z=.04,material="stone",zone=mass)
        b.route("smithy.apron_clearance",(.2,-1.35,0,4.9,0,mass.base+.1),kind="human")
        if seed_profile is None:
            b.ramp("smithy.material_ramp",(7.1,-2.0),(7.1,0),2.4,mass.base,
                   zone=mass,material="stone")
            b.route("forge_material_lane", (6.2,.15,mass.base,8.2,d-.75,mass.base+2.05), kind="material")
        else:
            stock_x=hall_width
            stock_y=seed_profile["stock_setback"]
            ramp_x=stock_x+1.0
            lane_y1=stock_y+(d-stock_y)-.75
            b.ramp("smithy.material_ramp",(ramp_x,-2.0),(ramp_x,stock_y),1.4,mass.base,
                   zone=mass,material="stone")
            b.route("smithy.material_ramp_clearance",
                    (ramp_x-.7,-2.0,0,ramp_x+.7,stock_y,mass.base+.1),kind="material")
            b.route("forge_material_lane",
                    (stock_x+.30,stock_y+.15,mass.base,stock_x+1.70,lane_y1,mass.base+2.05),
                    kind="material")
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
    prominent = region=="LOWMARK" and ctx.construction_resolver is not None
    firebed_top = mass.base+(.91 if prominent else .55)
    if prominent:
        # The approach sees a supported working-height firebed above an
        # open ash access, with both piers continuing into the slab.
        b.box("hearth_stone_plinth",(hx-1.10,hy-.79,mass.base+.04,
                                    hx+1.10,hy+.80,mass.base+.22),"stone",mass,role="forge")
        for side in (-1,1):
            x=hx+side*.81
            b.box("hearth_bearing_"+str(side),(x-.25,hy-.65,mass.base+.22,
                  x+.25,hy+.67,firebed_top-.22),"stone",mass,role="forge")
        b.box("hearth_backing",(hx-.57,hy+.44,mass.base+.22,hx+.57,hy+.70,
                  firebed_top-.22),"stone",mass,role="forge")
        b.box("hearth_working_slab",(hx-1.08,hy-.72,firebed_top-.22,hx+1.08,hy+.70,
                  firebed_top-.075),"stone_light",mass,role="forge")
        b.box("hearth_firebed",(hx-.81,hy-.60,firebed_top-.075,hx+.81,hy+.51,
                  firebed_top),"iron",mass,role="forge_fire")
        for side in (-1,1):
            x=hx+side*.91
            curb=b.fixture("hearth_"+("left" if side<0 else "right")+"_curb","stone",mass,"forge")
            curb.extrude([(x-.10,hy-.56,firebed_top-.08),(x-.10,hy+.61,firebed_top-.08),
                          (x-.10,hy+.61,firebed_top+.38),(x-.10,hy-.43,firebed_top+.09)],(.20,0,0))
        b.box("hearth_rear_curb",(hx-.81,hy+.45,firebed_top-.08,hx+.81,hy+.65,
                  firebed_top+.42),"stone",mass,role="forge")
    else:
        b.box("hearth_stone_plinth", (hx-.95,hy-.85,mass.base+.04,hx+.95,hy+.85,mass.base+.45), "stone", mass, role="forge")
        b.box("hearth_firebed", (hx-.66,hy-.58,mass.base+.45,hx+.66,hy+.42,mass.base+.55), "iron", mass, role="forge_fire")
        b.box("hearth_left_curb", (hx-.76,hy-.65,mass.base+.45,hx-.60,hy+.53,mass.base+1.15), "stone", mass, role="forge")
        b.box("hearth_right_curb", (hx+.60,hy-.65,mass.base+.45,hx+.76,hy+.53,mass.base+1.15), "stone", mass, role="forge")
        b.box("hearth_rear_curb", (hx-.76,hy+.48,mass.base+.45,hx+.76,hy+.65,mass.base+1.15), "stone", mass, role="forge")
    ax=(w*.42 if region=="LOWMARK" else
        hx+1.1 if region in ("THORNFELL","MIRE") else w*.48)
    ay=hy
    anvil_bounds=(ax-.48,ay-.28,mass.base+.78,ax+.48,ay+.28,mass.base+1.12)
    anvil=_station_fixture(b,"anvil","iron",mass,"forge",anvil_bounds)
    # Forged section: a broad working head narrows through the waist into a
    # flared foot. Keeping the original station AABB preserves clearance data.
    anvil.extrude([(ax-.38,ay-.20,mass.base+.78),
                   (ax+.38,ay-.20,mass.base+.78),
                   (ax+.24,ay-.20,mass.base+.91),
                   (ax+.43,ay-.20,mass.base+1.04),
                   (ax-.43,ay-.20,mass.base+1.04),
                   (ax-.24,ay-.20,mass.base+.91)],(0,.40,0))
    anvil.box((ax,ay,mass.base+1.055),(.94,.52,.09))
    horn=ctx.buffer("smithy.anvil_horn","iron","details",zone=mass)
    horn.structural_role="anvil_working_surface"
    horn.extrude([(ax+.20,ay-.22,mass.base+1.08),
                  (ax+.46,ay-.22,mass.base+1.08),
                  (ax+.46,ay-.22,mass.base+1.15)],(0,.44,0))
    b.box("anvil_stump", (ax-.28,ay-.31,mass.base+.04,ax+.28,ay+.31,mass.base+.76), "timber", mass, role="forge")
    bellows_bounds=(hx-.98,hy+.70,mass.base+1.05,hx-.10,hy+1.25,mass.base+1.77)
    bellows=_station_fixture(b,"bellows","timber",mass,"forge_bellows",bellows_bounds)
    bx0,by0,bz0,bx1,by1,bz1=bellows_bounds
    # Folded wedge cheeks and a top board give the bellows a compressed,
    # directed form instead of a solid crate silhouette.
    for x in (bx0+.08,bx1-.08):
        bellows.extrude([(x,by0+.05,bz0+.08),(x,by1-.04,bz0+.08),
                         (x,by1-.04,bz1-.08)],(.08,0,0))
    bellows.box(((bx0+bx1)*.5,(by0+by1)*.5,bz1-.10),(bx1-bx0,by1-by0,.12))
    bellows.box(((bx0+bx1)*.5,by0+.08,bz0+.10),(bx1-bx0-.12,.12,.12))
    _beam(ctx,"smithy.bellows_nozzle","iron",
          (bx0+.02,by0+.10,bz0+.28),(hx-.05,hy+.26,firebed_top+.33 if prominent else mass.base+.88),.09,.09,mass)
    if region in ("LOWMARK","THORNFELL","MIRE"):
        operator_x0=ax+.1 if region=="THORNFELL" else ax-.42
        operator_x1=ax+.85 if region=="THORNFELL" else ax+.52
        b.route("smithy.operator_workpad",(operator_x0,.12,mass.base,operator_x1,.62,mass.base+2.0),kind="human")
        if region=="LOWMARK":
            _open_bin(b,"quench_trough",(4.75,1.8,mass.base+.04,5.25,2.5,mass.base+.42),"stone",mass,"quench")
            _open_bin(b,"coal_bin",(.35,3.05,mass.base+.04,1.25,3.75,mass.base+.88),"timber",mass,"fuel",slatted=True)
        else:
            _open_bin(b,"quench_trough",(hx+2.2,hy+.2,mass.base+.04,hx+3.0,hy+.9,mass.base+.42),"stone" if region=="MIRE" else "iron",mass,"quench")
            _open_bin(b,"coal_bin",(.35,d*.68,mass.base+.04,1.25,d*.68+.7,mass.base+.88),"timber",mass,"fuel",slatted=True)
    else:
        _open_bin(b,"quench_trough",(w*.74,d*.55,mass.base+.04,w*.74+1.05,d*.55+.65,mass.base+.42),"stone" if region=="EMBERHOLT" else "timber",mass,"quench")
        _open_bin(b,"coal_bin",(.4,d*.58,mass.base+.04,1.45,d*.58+.82,mass.base+.88),"timber",mass,"fuel",slatted=True)
    if region=="EMBERHOLT":
        b.box("forge_slag_catch",(w*.64,hy+.55,mass.base+.04,w*.76,hy+1.2,mass.base+.52),"iron",mass,role="slag_bay")
        b.box("ingot_work_bench",(w*.62,hy+1.45,mass.base+.04,w*.77,hy+2.1,mass.base+.98),"iron",mass,role="material_bay")
    if region=="LOWMARK":
        b.deck("smithy.hot_work_pad",
               [(hx-1.25,hy-.85),(hx+1.35,hy-.85),(hx+1.35,hy+1.8),(hx-1.25,hy+1.8)],
               z=mass.base,material="stone",zone=mass)
    elif region=="THORNFELL":
        # A thick windward breast behind the hearth gives the open forge a
        # sheltered stone working face while leaving the hood inlet and side
        # exhaust route unobstructed.
        wall=ctx.buffer("smithy.stone_hearth_windwall","stone","structure",mass)
        wall.structural_role="hearth_windwall"
        wall.box((hx,hy+.79,mass.base+.86),(1.76,.24,1.08))
    elif region=="EMBERHOLT":
        breast=ctx.buffer("smithy.masonry_hotbay","stone","structure",mass)
        breast.structural_role="masonry_forge_breast"
        breast.box((hx,hy+.88,mass.base+.82),(2.0,.32,.96))
    _smithy_flue(b, mass, hx, hy+.15, mass.base)
    # Structural rhythm carries the roof and reinforces the open face; these
    # posts are at the perimeter and outside all recorded circulation.
    if region!="MIRE":
        for i,x in enumerate((.3,mass.width-.3)):
            post_top=mass.roof_height(x,d-.12)-.24
            _beam(ctx,f"smithy.bay_post_{i}","timber" if region=="LOWMARK" else "stone",
                  (x,d-.12,mass.base),(x,d-.12,post_top),.20,.20,mass)
    if region=='LOWMARK':
        from .benchmark_construction import smithy_range
        smithy_range(b,mass,seed_profile,firebed_top=firebed_top if prominent else None)
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
    front_margin=.62
    rear_margin=1.65 if region=="MIRE" else front_margin
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
                     {"edge_index":2,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.4},
                     {"edge_index":1,"s0":d-1.55,"s1":d-.02,"height":2.4}]
    elif region == "EMBERHOLT":
        open_edges=[0,2]
        open_access=[{"edge_index":0,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.7},
                     {"edge_index":2,"s0":w*.5-1.3,"s1":w*.5+1.3,"height":2.7}]
    else:
        open_edges=[0,2]
        open_access=[]
    mass=b.mass("market_hall",x=0,y=0,width=w,depth=d,floors=1,floor_height=floor_height,
                entrance_edge=0,openings="NONE",open_edges=open_edges,
                open_access=open_access,overhang=.38,
                roof_axis="Y" if region in ("LOWMARK","THORNFELL") else "X",
                roof="GABLE" if region in ("LOWMARK","THORNFELL") else b.roof,
                pitch=30 if region in ("LOWMARK","THORNFELL") else b.pitch)
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
    aisle_left,aisle_right=(w-aisle_width)*.5,(w+aisle_width)*.5
    margin=front_margin
    bay_length=(d-margin-rear_margin)/bays
    trade_material="iron" if region=="EMBERHOLT" else "stone" if region=="THORNFELL" else "timber"
    # Each capacity bay now runs along the public aisle, with a customer
    # counter, a clear seller pocket, and a back stock shelf. Existing front /
    # rear IDs remain stable: they identify the customer face and stock face of
    # each paired stall rather than two isolated end rows.
    for side in ("west","east"):
        for i in range(bays):
            y_start=margin+i*bay_length
            y0=y_start+.14
            y1=y_start+bay_length-.14
            usable_length=y1-y0
            counter_length=min(1.48,usable_length)
            cy=(y0+y1)*.5
            c_y0,c_y1=cy-counter_length*.5,cy+counter_length*.5
            if side=="west":
                counter_x1=aisle_left-.25
                counter_x0=counter_x1-.78
                seller_x1=counter_x0-.12
                seller_x0=seller_x1-1.02
                shelf_x1=seller_x0-.18
                shelf_x0=shelf_x1-.46
            else:
                counter_x0=aisle_right+.25
                counter_x1=counter_x0+.78
                seller_x0=counter_x1+.12
                seller_x1=seller_x0+1.02
                shelf_x0=seller_x1+.18
                shelf_x1=shelf_x0+.46
            bnd=(counter_x0,c_y0,mass.base+.04,counter_x1,c_y1,mass.base+1.00)
            _market_counter(b,f"{side}_bay_{i+1}_front_counter",bnd,
                            trade_material,mass)
            # Seller clearance separates the counter from a rear stock shelf;
            # the public aisle stays entirely outside the trade bay.
            b.route(f"{side}_bay_{i+1}_front_seller_space",
                    (seller_x0,y0,mass.base,seller_x1,y1,mass.base+2.05),kind="service")
            shelf_bounds=(shelf_x0,c_y0,mass.base+.04,shelf_x1,c_y1,mass.base+1.58)
            _market_back_shelf(b,f"{side}_bay_{i+1}_rear_counter",shelf_bounds,
                               trade_material,mass)
    _market_vendor_frames(b,mass,bays,aisle_left,aisle_right,margin,
                          "stone" if region in ("THORNFELL","EMBERHOLT") else "timber",
                          rear_margin=rear_margin)
    if region in ("LOWMARK","THORNFELL"):
        _market_open_gables(b,mass,2.48 if region=="LOWMARK" else 2.90)
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
        # Join the raised linear quay at the clear rear bay break; the central
        # side frontage remains allocated to the vendor stalls.
        b.route("market.quay_connector",((w+aisle_width)*.5,d-1.45,mass.base,
                                          w+2.8,d-.10,mass.base+2.2),kind="public")
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
