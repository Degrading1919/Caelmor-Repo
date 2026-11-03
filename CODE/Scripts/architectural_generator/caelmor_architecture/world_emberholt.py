"""Parametric Emberholt massing grammar.

This is a reversible art-direction interpretation: substantial angular stone
volumes, terraces, vents, and iron service walks. It creates original geometry
from the shared construction context and never assembles preset meshes.
"""
import math


def _value(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _tag(value):
    return str(value or "").strip().upper().replace(" ", "_").replace("-", "_")


def _box_bounds(buffer, x0, y0, z0, x1, y1, z1):
    """Create a box from bounds using MeshBuffer's center/size API."""
    buffer.box(((x0+x1)*.5, (y0+y1)*.5, (z0+z1)*.5),
               (x1-x0, y1-y0, z1-z0))


def _wall_point(mass, edge_index, station):
    a, b = _edges(mass)[edge_index]
    length = max(((b[0]-a[0])**2 + (b[1]-a[1])**2)**.5, 1e-8)
    t = station / length
    return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)


def _mass(ctx, key, **kwargs):
    openings = kwargs.pop("openings", "EMBER")
    steps = kwargs.pop("steps", True)
    return ctx.mass(key, openings=openings, steps=steps, **kwargs)


def _edges(mass):
    plan = _value(mass, "plan")
    edges = _value(mass, "edges") or _value(plan, "edges")
    if edges:
        return edges
    outline = _value(plan, "outline", ())
    return list(zip(outline, list(outline[1:]) + list(outline[:1])))


def _records(mass):
    records = _value(mass, "facade_records")
    if records is None:
        records = _value(_value(mass, "plan"), "facade_records", ())
    return records or ()


def _gallery_access(mass, preferred_edge=None):
    """Return the authored upper-floor door and its world-space wall edge."""
    edges = _edges(mass)
    records = list(_records(mass))
    if preferred_edge is not None:
        records.sort(key=lambda row: row.get("edge_index") != preferred_edge)
    for record in records:
        edge_index = int(record.get("edge_index", -1))
        if not 0 <= edge_index < len(edges):
            continue
        for opening in record.get("openings", ()):
            if opening.get("role") == "gallery_access":
                a, b = edges[edge_index]
                dx, dy = b[0] - a[0], b[1] - a[1]
                length = (dx * dx + dy * dy) ** .5
                if length <= 1e-6:
                    continue
                tx, ty = dx / length, dy / length
                center_s = (opening["s0"] + opening["s1"]) * .5
                center = (a[0] + tx * center_s, a[1] + ty * center_s)
                # Contract footprints are counter-clockwise; (dy, -dx) faces
                # outward from each wall.
                normal = (dy / length, -dx / length)
                return {"edge": edge_index, "opening": opening,
                        "center": center, "normal": normal, "tangent": (tx, ty)}
    return None


def _buttresses(ctx, mass, detail, count_limit=4, excluded_edges=()):
    """Put battered stone ribs on solid side-wall stations, clear of openings."""
    spacing = 3.1 if detail == "HIGH" else 4.4
    for edge in (1, 3):
        if edge in excluded_edges:
            continue
        stations = ctx.solid_stations(mass, edge, spacing=spacing, radius=.52)
        for index, station in enumerate(stations[:count_limit]):
            x, y = _wall_point(mass, edge, station)
            a, b = _edges(mass)[edge]
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = max((dx * dx + dy * dy) ** .5, 1e-6)
            nx, ny = dy / length, -dx / length
            # Battered profile: the foot bears out from the wall and leans back
            # toward it near the parapet. The broad section reads at clay scale.
            buffer = ctx.buffer("emberholt_buttress_%d_%d" % (edge, index),
                                "stone_light", "structure", zone=mass)
            buffer.chamfered_beam(
                (x + nx * .48, y + ny * .48, mass.base + .04),
                (x + nx * .06, y + ny * .06, mass.eave - .30),
                .78, .68, .06,
            )


def _vent_shaft(ctx, key, mass, x, y, width, depth, height):
    """A hollow-looking, banded stone vent with a real open top silhouette."""
    z0 = mass.eave - .20
    z1 = z0 + height
    wall = .24
    buf = ctx.buffer(key, "stone", "details", zone=mass)
    # Four separated risers make an actual vent throat rather than a solid fake
    # volume. The iron cap bars are supported across the throat below.
    _box_bounds(buf, x-width/2, y-depth/2, z0, x-width/2+wall, y+depth/2, z1)
    _box_bounds(buf, x+width/2-wall, y-depth/2, z0, x+width/2, y+depth/2, z1)
    _box_bounds(buf, x-width/2+wall, y-depth/2, z0,
                x+width/2-wall, y-depth/2+wall, z1)
    _box_bounds(buf, x-width/2+wall, y+depth/2-wall, z0,
                x+width/2-wall, y+depth/2, z1)
    iron = ctx.buffer(key + "_cap", "iron", "structure", zone=mass)
    # A pair of cap bars leaves the center of the shaft open to view.
    _box_bounds(iron, x-width*.42, y-.055, z1, x+width*.42, y+.055, z1+.16)
    _box_bounds(iron, x-.055, y-depth*.42, z1, x+.055, y+depth*.42, z1+.16)


def _iron_walk(ctx, main, tower, wealth):
    """Connect matching generated gallery doors with a supported iron walk."""
    main_access = _gallery_access(main, preferred_edge=1)
    tower_access = _gallery_access(tower, preferred_edge=3)
    if not main_access or not tower_access:
        return
    # The selected side-wall doors must face each other and share a level.
    n0, n1 = main_access["normal"], tower_access["normal"]
    if n0[0] < .8 or n1[0] > -.8:
        return
    if abs(main_access["center"][1] - tower_access["center"][1]) > .12:
        return
    o0, o1 = main_access["opening"], tower_access["opening"]
    z0, z1 = float(o0["z0"]), float(o1["z0"])
    if abs(z0 - z1) > .12:
        return

    x0 = main_access["center"][0]
    x1 = tower_access["center"][0]
    yc = (main_access["center"][1] + tower_access["center"][1]) * .5
    half = max(.85, min(1.25, (min(o0["s1"] - o0["s0"], o1["s1"] - o1["s0"]) + 1.0) * .5))
    z = (z0 + z1) * .5
    polygon = [(x0, yc-half), (x1, yc-half), (x1, yc+half), (x0, yc+half)]
    ctx.deck("emberholt_iron_walk", polygon, z, thickness=.20, material="iron")

    # Context.deck adds ground-bearing iron posts beneath every raised span.
    # Guardrails stay on that deck and outside both door assemblies.
    ctx.rail("emberholt_walk_rail_north", (x0+.08, yc+half), (x1-.08, yc+half), z+.01, "iron")
    ctx.rail("emberholt_walk_rail_south", (x0+.08, yc-half),
             (x1-.08, yc-half), z+.01, "iron")


def _edge_normal(mass, edge_index):
    a, b = _edges(mass)[edge_index]
    dx, dy = b[0]-a[0], b[1]-a[1]
    length = max(math.hypot(dx, dy), 1e-8)
    return (dy/length, -dx/length)


def _grounded_household_ties(ctx, mass, detail):
    """Narrow iron straps tie upper masonry back to ground-bearing corners."""
    for edge in (0, 3):
        stations=ctx.solid_stations(mass,edge,spacing=4.8 if detail=="LOW" else 3.8,
                                    radius=.15)
        if not stations:
            continue
        chosen=stations if detail=="HIGH" else [stations[len(stations)//2]]
        a,b=_edges(mass)[edge]
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=max(math.hypot(dx,dy),1e-8)
        tx,ty=dx/length,dy/length
        nx,ny=_edge_normal(mass,edge)
        iron=ctx.buffer("emberholt_grounded_ties_%d"%edge,"iron","structure",zone=mass)
        for index,station in enumerate(chosen):
            x,y=_wall_point(mass,edge,station)
            x+=nx*.37; y+=ny*.37
            z0,z1=.27,mass.eave-.12
            iron.beam((x,y,z0),(x,y,z1),.085,.045)
            # Broad end shoes transfer the strap into the plinth and roof plate.
            iron.beam((x-tx*.14,y-ty*.14,z0+.08),
                      (x+tx*.14,y+ty*.14,z0+.08),.25,.10)
            iron.beam((x-tx*.14,y-ty*.14,z1-.08),
                      (x+tx*.14,y+ty*.14,z1-.08),.25,.10)


def _masonry_corbels_and_anchors(ctx, mass, detail):
    """Seat small parapet corbels and iron anchor plates in clear wall bays."""
    station_spacing=3.8 if detail=="HIGH" else 5.0
    for edge in (0,2):
        stations=ctx.solid_stations(mass,edge,spacing=station_spacing,radius=.56)
        if not stations:
            continue
        if detail!="HIGH":
            stations=stations[::2] or stations[:1]
        nx,ny=_edge_normal(mass,edge)
        stone=ctx.buffer("emberholt_parapet_corbels_%d"%edge,
                         "stone_light","structure",zone=mass)
        iron=ctx.buffer("emberholt_forged_anchor_plates_%d"%edge,
                        "iron","structure",zone=mass)
        for station in stations:
            x,y=_wall_point(mass,edge,station)
            lower=(x+nx*.04,y+ny*.04,mass.eave-.62)
            upper=(x+nx*.38,y+ny*.38,mass.eave-.24)
            stone.beam(lower,upper,.24,.23)
            iron.beam((x+nx*.40,y+ny*.40,mass.eave-.30),
                      (x+nx*.40,y+ny*.40,mass.eave-.12),.27,.08)


def _hearth_flue(ctx, mass, detail, edge=2):
    """A hollow masonry flue rises from the ground along an opening-safe wall bay."""
    candidates=ctx.solid_stations(mass,edge,spacing=3.7,radius=.48)
    if not candidates:
        return None
    length=math.dist(*_edges(mass)[edge])
    station=min(candidates,key=lambda value:abs(value-length*.5))
    x,y=_wall_point(mass,edge,station)
    nx,ny=_edge_normal(mass,edge)
    tx,ty=_edges(mass)[edge][1][0]-_edges(mass)[edge][0][0],\
          _edges(mass)[edge][1][1]-_edges(mass)[edge][0][1]
    edge_len=max(math.hypot(tx,ty),1e-8); tx/=edge_len; ty/=edge_len
    half_t,half_n=.50,.42
    cx,cy=x+nx*(half_n-.025),y+ny*(half_n-.025)
    z0,z1=.04,mass.eave+(1.65 if detail=="LOW" else 1.85)
    wall=.17
    flue=ctx.buffer("emberholt_hearth_flue","stone","structure",zone=mass)
    def strip(t0,n0,t1,n1):
        return [(cx+tx*t0+nx*n0,cy+ty*t0+ny*n0),
                (cx+tx*t1+nx*n0,cy+ty*t1+ny*n0),
                (cx+tx*t1+nx*n1,cy+ty*t1+ny*n1),
                (cx+tx*t0+nx*n1,cy+ty*t0+ny*n1)]
    inner_t,inner_n=half_t-wall,half_n-wall
    for poly in (strip(-half_t,-half_n,half_t,-half_n+wall),
                 strip(-half_t,half_n-wall,half_t,half_n),
                 strip(-half_t,-half_n+wall,-inner_t,half_n-wall),
                 strip(inner_t,-half_n+wall,half_t,half_n-wall)):
        flue.prism(poly,z0,z1)
    # A four-sided weather rim protects the open throat without capping it.
    outer_t,outer_n=half_t+.08,half_n+.06
    rim_t,rim_n=.14,.14
    for poly in (strip(-outer_t,-outer_n,outer_t,-outer_n+rim_n),
                 strip(-outer_t,outer_n-rim_n,outer_t,outer_n),
                 strip(-outer_t,-outer_n+rim_n,-outer_t+rim_t,outer_n-rim_n),
                 strip(outer_t-rim_t,-outer_n+rim_n,outer_t,outer_n-rim_n)):
        flue.prism(poly,z1-.12,z1)
    collar=ctx.buffer("emberholt_flue_iron_collar","iron","structure",zone=mass)
    collar.beam((cx-tx*(half_t+.04)-nx*(half_n+.04),
                 cy-ty*(half_t+.04)-ny*(half_n+.04),mass.eave+.22),
                (cx+tx*(half_t+.04)-nx*(half_n+.04),
                 cy+ty*(half_t+.04)-ny*(half_n+.04),mass.eave+.22),.09,.07)
    mass.plan.soot_sources=[(cx,cy,z1)]
    return flue


def _deep_portal(ctx, mass, edge_index):
    """Stone jambs and a supported lintel frame the actual lower entrance."""
    record=next((r for r in _records(mass)
                 if int(r.get("edge_index",-1))==edge_index),None)
    if not record:
        return None
    door=next((o for o in record.get("openings",())
               if o.get("kind")=="door" and o.get("role")!="gallery_access"),None)
    if not door:
        return None
    bounds=door.get("assembly_bounds",door)
    lo,hi=float(bounds["s0"]),float(bounds["s1"])
    supports=ctx.solid_stations(mass,edge_index,spacing=.8,radius=.18)
    left=[s for s in supports if s<lo-.22]
    right=[s for s in supports if s>hi+.22]
    if not left or not right:
        return None
    stations=(max(left),min(right))
    nx,ny=_edge_normal(mass,edge_index)
    top=float(door["z1"])+.27
    portal=ctx.buffer("emberholt_deep_supported_portal","stone_light","structure",zone=mass)
    for station in stations:
        x,y=_wall_point(mass,edge_index,station)
        inner=(x+nx*.20,y+ny*.20)
        outer=(x+nx*1.02,y+ny*1.02)
        portal.beam((*inner,.27),(*outer,.27),.42,.42)
        portal.beam((*inner,top),(*outer,top),.42,.34)
        portal.beam((*outer,.27),(*outer,top),.34,.34)
        # Forged knee braces visibly transfer the projecting lintel load into
        # the piers; their endpoints stay outside the authored door assembly.
        portal.beam((x+nx*.35,y+ny*.35,top-.58),
                    (x+nx*.96,y+ny*.96,top-.10),.15,.13)
    # The outer lintel bears on both projected jambs, leaving the opening clear.
    p0=_wall_point(mass,edge_index,stations[0]);p1=_wall_point(mass,edge_index,stations[1])
    portal.beam((p0[0]+nx*1.02,p0[1]+ny*1.02,top),
                (p1[0]+nx*1.02,p1[1]+ny*1.02,top),.34,.34)
    return portal


def _private_court(ctx, main, wealth, function):
    """A low stepped room range faces the main household across a supported court."""
    width,depth=main.width,main.depth
    gap=3.45
    room_width=4.5
    room_depth=depth*.66
    room_y=(depth-room_depth)*.5
    room_x=width+gap
    rooms=_mass(ctx,"emberholt_private_rooms",x=room_x,y=room_y,
                width=room_width,depth=room_depth,floors=1,
                floor_height=main.plan.settings.floor_height,base=main.base,
                roof="TERRACE",pitch=0.0,overhang=.05,entrance_edge=3,
                steps=False,function=function,openings="EMBER_HOME",
                foundation="PLINTH")
    _buttresses(ctx,rooms,ctx.settings.detail,count_limit=2)
    half=min(2.25,room_depth*.30)
    cy=depth*.5
    y0,y1=cy-half,cy+half
    x0,x1=width+.05,room_x-.05
    court_z=main.base+.02
    court=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    ctx.deck("emberholt_private_court",court,court_z,thickness=.20,material="stone")
    curb=ctx.buffer("emberholt_private_court_coping","stone_light","foundation")
    curb.beam((x0+.18,y0,court_z+.08),(x1-.18,y0,court_z+.08),.18,.16)
    curb.beam((x0+.18,y1,court_z+.08),(x1-.18,y1,court_z+.08),.18,.16)
    # Grounded treads avoid a hanging stair mesh below the buried court deck.
    steps=ctx.buffer("emberholt_private_court_steps","stone","foundation")
    run=1.35; tread_count=max(2,int(math.ceil((court_z-main.base)/.16)))
    tread_h=(court_z-main.base)/tread_count
    for index in range(tread_count):
        top_z=main.base+(index+1)*tread_h
        y_front=y0-run+(index*run/tread_count)
        y_back=y0-run+((index+1)*run/tread_count)
        steps.prism([((x0+x1)*.5-.55,y_front),((x0+x1)*.5+.55,y_front),
                     ((x0+x1)*.5+.55,y_back),((x0+x1)*.5-.55,y_back)],
                    max(.02,top_z-.13),top_z)
    _deep_portal(ctx,main,1)
    return rooms


def build(ctx):
    """Build an angular Emberholt structure from the shared geometry context."""
    s = ctx.settings
    function = _tag(_value(s, "function", "COTTAGE"))
    context = _tag(_value(s, "context", "EMBERHOLD"))
    wealth = _tag(_value(s, "wealth", "ESTABLISHED"))
    detail = _tag(_value(s, "detail", "MEDIUM"))
    age = float(_value(s, "age", 35.0))
    floor_h = max(2.8, min(3.35, float(_value(s, "floor_height", 3.0))))
    household = function in {"COTTAGE", "FARMHOUSE", "TOWNHOUSE",
                             "MERCHANT_HOUSE", "SHOP"}
    cottage_household=function=="COTTAGE"
    household_affluent = household and wealth == "AFFLUENT"
    household_tier = "AFFLUENT" if household_affluent else wealth

    industrial = function in {"SMITHY", "WORKSHOP"} or (
        context == "EMBERFORGES" and not household and function not in
        {"GATEHOUSE","WATCHTOWER","BARRACKS","ASSEMBLY_HALL"})
    civic = function in {"ASSEMBLY_HALL", "GATEHOUSE", "WATCHTOWER", "BARRACKS"}
    defensive = function in {"GATEHOUSE", "WATCHTOWER", "BARRACKS"} or context == "EMBERGATE"
    affluent = wealth == "AFFLUENT"
    # The gatehouse's authored through-passage uses the north/south openings;
    # an east-side court would introduce an unrelated entrance.
    entry_court = (affluent or civic or industrial) and function != "GATEHOUSE"

    # Even dwellings occupy a deep, stone city bay. Wealth adds useful volume
    # and a court-like approach before it adds a signal tower.
    configured_width=float(_value(s,"width",10.5))
    configured_depth=float(_value(s,"depth",8.0))
    width = max(12.0, configured_width)
    depth = max(10.0, configured_depth)
    floors = max(2, min(3, int(_value(s, "floors", 2))))
    if cottage_household and household_tier == "MODEST":
        width=min(10.0,max(8.8,configured_width*.80))
        depth=min(9.8,max(8.2,configured_depth))
        floors=1
    elif cottage_household and household_tier == "ESTABLISHED":
        width=min(8.0,max(6.8,configured_width*.65))
        depth=min(11.0,max(9.6,configured_depth))
        floors=2
    elif cottage_household:
        width=min(10.0,max(8.2,configured_width*.78))
        depth=min(12.2,max(10.8,configured_depth))
        floors=3
    elif household:
        domestic_profiles={
            "FARMHOUSE":(9.0,11.2,2),
            "TOWNHOUSE":(7.4,10.2,3),
            "MERCHANT_HOUSE":(8.4,10.8,2),
            "SHOP":(7.8,9.8,2),
        }
        base_width,base_depth,base_floors=domestic_profiles[function]
        tier_delta={"MODEST":(-.5,-.4),"ESTABLISHED":(0.,0.),
                    "AFFLUENT":(1.0,1.0)}.get(household_tier,(0.,0.))
        width=min(base_width+1.2,max(base_width-.5,base_width+tier_delta[0]))
        depth=max(8.8,base_depth+tier_delta[1])
        floors=base_floors
    elif wealth == "MODEST":
        width, depth, floors = min(width, 13.2), max(depth, 10.8), 2
    elif wealth == "ESTABLISHED":
        width, depth, floors = min(max(width, 15.0), 16.4), max(depth, 11.5), 2
    else:
        width, depth, floors = min(max(width, 16.5), 18.0), max(depth, 12.6), 3

    if context == "CINDERWEAVE":
        if not household:
            width = min(16.0, max(width, 15.0))
            depth = max(depth, 12.0)
    elif context == "EMBERFORGES":
        if not household:
            width, depth, floors = min(18.0, max(width, 16.0)), max(depth, 13.0), 2
    elif context == "ASHSPIRE":
        if not household:
            width, depth, floors = min(18.0, max(width, 16.5)), max(depth, 13.0), 3
    elif context == "EMBERGATE":
        width, depth = min(width, 17.0), max(depth, 12.0)

    if industrial:
        width, depth, floors = min(18.0, max(width, 16.8)), max(depth, 13.0), 2
    elif function == "WATCHTOWER":
        width, depth, floors = 10.5, 10.0, 4
    elif function == "GATEHOUSE":
        width, depth, floors = min(width, 18.0), max(depth, 13.0), 3
    elif function == "ASSEMBLY_HALL":
        width, depth, floors = min(width, 18.0), max(depth, 13.0), 3
    elif function == "BARRACKS":
        width, depth, floors = min(width, 18.0), max(depth, 12.0), 2

    # Cinderweave's crowded artisan blocks are narrower and deeper; the forge
    # ward's hall is broader. All primary footprints remain below 24m.
    width = min(19.0, width)
    depth = min(16.0, depth)
    tower_needed = (affluent or civic or defensive or industrial) and not household
    link_needed = tower_needed and function not in {"WATCHTOWER", "GATEHOUSE"}
    primary = _mass(
        ctx, "emberholt_main_block", x=0, y=0, width=width, depth=depth,
        floors=floors, floor_height=floor_h, roof="TERRACE", pitch=0.0,
        overhang=.08, entrance_edge=(0 if function=="GATEHOUSE" or household
                                     else (1 if floors>1 else 0)),
        blocked_edges=(2,) if industrial else ((1,) if household else ()),
        steps=not entry_court,
        function=function, gallery_edges=(1,) if link_needed else (),
        openings="EMBER_HOME" if household else "EMBER",
        foundation="PLINTH",
    )

    _buttresses(ctx, primary, detail, count_limit=2 if detail == "LOW" else 4)
    if household:
        _masonry_corbels_and_anchors(ctx,primary,detail)
        _grounded_household_ties(ctx,primary,detail)
        _hearth_flue(ctx,primary,detail)
        include_work_range=(not cottage_household or household_tier=="ESTABLISHED")
        if include_work_range:
            range_width=(3.8 if cottage_household else
                         min(4.5,max(3.3,width*.48)))
            work_depth=min(7.2,depth*.72)
            work=_mass(ctx,"emberholt_domestic_work_range",x=width,y=0,
                       width=range_width,depth=work_depth,floors=1,
                       floor_height=floor_h*.9,base=primary.base,
                       roof="SHED",pitch=24.0,overhang=.04,entrance_edge=0,
                       blocked_edges=(3,),function="WORKSHOP",steps=False,
                       openings="EMBER_HOME",
                       foundation="PLINTH")
            _buttresses(ctx,work,detail,count_limit=2,excluded_edges=(3,))

    if industrial:
        # The annex occupies the rear edge, so the working hearth rises on the
        # exposed west wall and remains clear of loading apertures by station.
        _hearth_flue(ctx,primary,detail,edge=3)

    # Industrial contexts get a lower wide work range, with a blind shared wall
    # and its own terrace parapet. It adds process area instead of cottage wings.
    if industrial:
        bay_w = min(7.2, max(5.4, width*.38))
        bay_d = min(7.4, depth*.56)
        bay = _mass(
            ctx, "emberholt_forge_work_range", x=(width-bay_w)*.5,
            y=depth, width=bay_w, depth=bay_d,
            floors=1, floor_height=floor_h*.90, base=primary.base,
            roof="TERRACE", pitch=0.0, overhang=.06,
            openings="EMBER", entrance_edge=2, blocked_edges=(0,),
            function="WORKSHOP",
            foundation="PLINTH",
        )
        _buttresses(ctx, bay, detail, count_limit=2)

    # A modest residence is a heavy deep bay. Affluent and civic buildings add
    # a compact service tower; the occupied primary mass stays within 24m.
    tower = None
    if tower_needed:
        tower_w = 3.25 if wealth == "MODEST" else 3.7
        tower_d = 4.2 if civic else 3.8
        gap = 3.1 if affluent else 1.35
        tower_x = width + gap
        tower_y = (depth-tower_d)*.5
        tower_floors = floors
        tower = _mass(
            ctx, "emberholt_vent_tower", x=tower_x, y=tower_y,
            width=tower_w, depth=tower_d, floors=tower_floors,
            floor_height=floor_h, base=primary.base,
            roof="TERRACE", pitch=0.0, overhang=.05,
            entrance_edge=3, function="WATCHTOWER",
            gallery_edges=(3,) if link_needed else (), foundation="PLINTH",
        )
        _buttresses(ctx, tower, detail, count_limit=1 if detail == "LOW" else 2)

        # Wealthy homes and civic/industrial masses gain a broad stone terrace
        # against the main entry elevation. The east-wall entry meets it directly.
        if entry_court:
            court_depth = min(2.5 if affluent else 1.8, gap-.15)
            court_half = min(depth*.34, 3.4 if affluent else 2.6)
            court_x0 = width
            court_x1 = court_x0 + court_depth
            court_center_y = depth*.5
            court_y0, court_y1 = court_center_y-court_half, court_center_y+court_half
            court = [(court_x0, court_y0), (court_x1, court_y0),
                     (court_x1, court_y1), (court_x0, court_y1)]
            court_z = primary.base + .02
            ctx.deck("emberholt_terraced_entry_court", court, court_z,
                     thickness=.24, material="stone")
            stair_x = (court_x0+court_x1)*.5
            stair_half = .48
            ctx.rail("emberholt_court_rail_south", (court_x0, court_y0),
                     (court_x1, court_y0), court_z+.02, "iron")
            ctx.rail("emberholt_court_rail_north_a", (court_x0, court_y1),
                     (stair_x-stair_half, court_y1), court_z+.02, "iron")
            ctx.rail("emberholt_court_rail_north_b", (stair_x+stair_half, court_y1),
                     (court_x1, court_y1), court_z+.02, "iron")
            ctx.rail("emberholt_court_rail_outer", (court_x1, court_y0),
                     (court_x1, court_y1), court_z+.02, "iron")
            ctx.stair("emberholt_court_steps", top=(stair_x, court_y1, court_z),
                      width=.85, run=1.7, direction=(0, 1),
                      material="stone")

    # Roofline vents and industrial shafts are open, four-sided stone stacks.
    # They sit within the host roof plan and have separate real geometry buffers.
    if not household and (industrial or context in {"EMBERFORGES", "EMBERHOLD", "CINDERWEAVE",
                                                     "ASHSPIRE", "EMBERGATE"} or affluent):
        shaft_height = 3.0 if industrial else 2.3
        sx = width*.24
        sy = depth*.16
        _vent_shaft(ctx, "emberholt_primary_vent", primary, sx, sy,
                    1.5 if industrial else 1.1, 1.35 if industrial else 1.05,
                    shaft_height)
        if industrial:
            _vent_shaft(ctx, "emberholt_secondary_vent", primary, width*.72,
                        depth*.10, 1.0, 1.0, 2.35)
    if tower is not None:
        _vent_shaft(ctx, "emberholt_tower_vent", tower, tower_x+tower_w*.5,
                    tower_y+tower_d*.5,
                    tower_w*.52, tower_d*.48, 2.1)

    # A real bridge joins authored gallery doors. Its supports, guarded edges,
    # and stair gap follow the geometry contract; no rail crosses either door.
    if tower is not None and link_needed:
        _iron_walk(ctx, primary, tower, wealth)

    if cottage_household and household_affluent:
        _private_court(ctx,primary,wealth,function)

    # The Glassed Hollow's sealed/warped treatment is left to authored landmarks;
    # normal buildings receive only use-driven soot and maintenance cohorts.
    if age >= 90 and detail == "HIGH":
        for edge in (0, 2):
            for index, station in enumerate(ctx.solid_stations(primary, edge,
                                                               spacing=5.0, radius=.40)):
                # Banded iron ties visibly reinforce long civic/industrial walls.
                x, y = _wall_point(primary, edge, station)
                a, b = _edges(primary)[edge]
                dx, dy = b[0]-a[0], b[1]-a[1]
                length = max((dx*dx+dy*dy)**.5, 1e-6)
                tx, ty = dx/length, dy/length
                z = primary.base + floor_h*.52
                ctx.buffer("emberholt_age_tie_%d_%d" % (edge, index),
                           "iron", "details", zone=primary).beam(
                    (x-tx*.22, y-ty*.22, z),
                    (x+tx*.22, y+ty*.22, z), .16, .09)
