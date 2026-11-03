"""Lowmark and Thornfell procedural building grammars.

These are reversible art-direction interpretations of the regional dossiers.
The construction language lives in the roofed masses and their load paths, not
in surface decoration, so LOW detail still retains the regional silhouette.
"""
import math


def _get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _norm(value):
    return str(value or "").strip().upper().replace(" ", "_").replace("-", "_")


def _mass(ctx, key, **kwargs):
    """Keep calls explicit and centralize safe roof/facade defaults."""
    kwargs.setdefault("openings", "DOMESTIC")
    kwargs.setdefault("steps", True)
    return ctx.mass(key, **kwargs)


def _beam(ctx, key, material, layer, start, end, radius, zone=None):
    buf = ctx.buffer(key, material, layer, zone=zone)
    buf.beam(start, end, radius * 2, radius * 2)
    return buf


def _box(buf, x0, y0, z0, x1, y1, z1):
    """MeshBuffer.box takes center and size, while callers use bounds."""
    buf.box(((x0+x1)*.5, (y0+y1)*.5, (z0+z1)*.5),
            (x1-x0, y1-y0, z1-z0))


def _wall_point(mass, edge_index, station):
    a, b = mass.plan.edges[edge_index]
    dx, dy = b[0]-a[0], b[1]-a[1]
    length = (dx*dx + dy*dy) ** .5
    if length <= 1e-8:
        return a[0], a[1]
    return a[0] + dx/length*station, a[1] + dy/length*station


def build_lowmark(ctx):
    """Construct a low, expandable Lowmark household/trade building."""
    s = ctx.settings
    category = _norm(_get(s, "function", _get(s, "category", "FARMHOUSE")))
    context = _norm(_get(s, "context", "RURAL"))
    wealth = _norm(_get(s, "wealth", "ESTABLISHED"))
    age = float(_get(s, "age", 35.0))
    detail = _norm(_get(s, "detail", "MEDIUM"))
    factor = {"MODEST": .84, "ESTABLISHED": 1.0, "AFFLUENT": 1.13}.get(wealth, 1.0)
    width = max(6.0, float(_get(s, "width", 10.5)))
    depth = max(5.0, float(_get(s, "depth", 7.0)))
    floors = max(1, min(2, int(_get(s, "floors", 2))))
    floor_h = float(_get(s, "floor_height", 2.8))
    # Broad agricultural/commercial bodies preserve a low eave and horizontal
    # roofline. Dwellings stay narrower and more closed.
    working = category in {
        "BARN", "GRAIN_STORE", "WAREHOUSE", "MARKET_HALL", "STABLE",
        "WORKSHOP", "SMITHY", "BOATHOUSE", "MILLER", "INN",
    }
    if working:
        width = max(width, 11.0) * factor
        depth = max(depth, 7.2)
        floors = 1 if category in {"BARN", "WAREHOUSE", "MARKET_HALL", "STABLE", "BOATHOUSE"} else min(floors, 2)
        openings = "WORKSHOP" if category in {"WORKSHOP", "SMITHY", "BARN", "WAREHOUSE", "STABLE"} else "DOMESTIC"
    else:
        width *= factor
        depth *= factor
        openings = "DOMESTIC"
    # Context alters the real plan: trade towns receive a longer frontage;
    # rebuilt Ashenstead stays modest and rural plots stay compact.
    if context in {"BROOKHOLLOW", "CRESTBRIDGE"}:
        width *= 1.10
    elif context == "ASHENSTEAD":
        width *= .94

    core = _mass(
        ctx, "lowmark_main_hall", x=0, y=0, width=width, depth=depth,
        floors=floors, floor_height=floor_h, roof="GABLE", pitch=32,
        overhang=.42, openings=openings, entrance_edge=0,
        blocked_edges=(1,3) if category=='MILLER' else (1,), foundation="PLINTH",
    )

    # Attached side range: an open, framed grain/work bay or covered store.
    # Party edges are closed, preserving both structural bearing and openings.
    wing_w = max(2.8, min(depth * .53, 5.2))
    wing_d = max(3.0, min(depth * .72, 5.8))
    wing_x = width
    wing_y = -depth * .12
    wing = _mass(
        ctx, "lowmark_service_wing", x=wing_x, y=wing_y,
        width=wing_w, depth=wing_d, floors=1,
        floor_height=max(2.2, floor_h * .82), base=core.base,
        roof="SHED", pitch=20, overhang=.36,
        openings="NONE",open_edges=(0,1,2),
        function='WORKSHOP' if working else 'COTTAGE',
        entrance_edge=0, blocked_edges=(3,), foundation="PLINTH",
    )
    ctx.deck('lowmark_working_range_floor',wing.plan.outline,wing.base,material='timber',zone=wing)
    # An occupied raised work platform has a real approach; open bents carry
    # the lean-to roof instead of another miniature cottage wall enclosure.
    ctx.stair('lowmark_work_range_steps',top=(wing_x+wing_w*.5,wing_y,wing.base),
              width=min(1.6,wing_w-.4),run=max(.9,wing.base*1.6),direction=(0,-1),
              material='stone')
    # A narrow covered loading bay extends broad trade buildings as useful
    # capacity instead of adding height. Its small gap keeps the core's rear
    # openings and entrance approach clear while it reads as a yard-side range.
    if category in {"BARN", "GRAIN_STORE", "WAREHOUSE", "MARKET_HALL", "STABLE"}:
        aw = min(width * .58, 7.0)
        ad = max(2.5, min(4.0, depth * .42))
        _mass(
            ctx, "lowmark_loading_bay", x=0, y=depth+.24,
            width=aw, depth=ad, floors=1, floor_height=floor_h*.75,
            base=core.base, roof="SHED", pitch=20, overhang=.22,
            openings="WORKSHOP", entrance_edge=2,
            function='WAREHOUSE',
            foundation="PLINTH",
        )

    # The core construction already schedules section-safe posts and joints;
    # adding a second decorative post grid would duplicate loads and hit eaves.
    # Weathered buildings gain a few repaired posts at the service wing; this
    # is load-bearing reinforcement, never arbitrary wall ornament.
    if age>=90 and float(s.maintenance)<.7 and detail == "HIGH":
        layout=wing.plan.facade_records[0]['frame_layout']
        posts=layout['principal_posts']
        for i,station in enumerate(posts[:1]+posts[-1:] if len(posts)>1 else posts):
            station+=.12 if i==0 else -.12
            x, y = _wall_point(wing, 0, station)
            top=layout['roof_safety']['structural_top']
            _beam(ctx,"lowmark_sistered_repair_post_%d"%i,"timber_light","structure",
                  (x,y,wing.base),(x,y,top),.05,wing)


def _thornfell_buttresses(ctx, mass, s, count=2):
    """Place stone piers at verified solid stations on exposed elevations."""
    detail = _norm(_get(s, "detail", "MEDIUM"))
    spacing = 2.2 if detail == "HIGH" else 3.0
    for edge in (1, 3):
        stations = ctx.solid_stations(mass, edge, spacing=spacing, radius=.48)
        if not stations:
            continue
        for i, station in enumerate(stations[:count]):
            x, y = _wall_point(mass, edge, station)
            # A ground-bearing tapered-looking stone pier, kept out of all
            # aperture assemblies by solid_stations' complete bounds test.
            b = ctx.buffer("thornfell_buttress_%d_%d" % (edge, i), "stone_light", "structure", zone=mass)
            b.chamfered_beam((x, y, mass.base+.02),
                             (x, y, mass.base+(mass.eave-mass.base)*.78), .40, .26)


def _stepped_stone_gables(ctx,mass):
    """Wind-protecting masonry gables with bearing courses and weather copings."""
    x0,y0,x1,y1=mass.bounds
    count=max(8,round(mass.depth/.55)); step=mass.depth/count
    walls=ctx.buffer('stepped_wind_gables','stone','roof',mass)
    caps=ctx.buffer('stepped_gable_copings','stone_light','roof',mass)
    for x in (x0,x1):
        for i in range(count):
            ya,yb=y0+i*step,y0+(i+1)*step
            za,zb=mass.roof_height(x,ya),mass.roof_height(x,yb)
            bottom=min(za,zb)-.18
            top=mass.eave+math.ceil((max(za,zb)-mass.eave)/.42)*.42+.22
            walls.box((x,(ya+yb)*.5,(bottom+top)*.5),(.34,step,top-bottom))
            caps.box((x,(ya+yb)*.5,top+.055),(.46,step+.025,.11))


def build_thornfell(ctx):
    """Construct a compact, stepped and sheltered Thornfell stone building."""
    s = ctx.settings
    category = _norm(_get(s, "function", _get(s, "category", "LONGHOUSE")))
    context = _norm(_get(s, "context", "RIDGE"))
    wealth = _norm(_get(s, "wealth", "ESTABLISHED"))
    age = float(_get(s, "age", 35.0))
    detail = _norm(_get(s, "detail", "MEDIUM"))
    factor = {"MODEST": .90, "ESTABLISHED": 1.0, "AFFLUENT": 1.08}.get(wealth, 1.0)
    # Keep the body compact and narrow; broad inputs turn into a deeper room
    # sequence rather than a Lowmark-like frontage.
    width = max(6.0, min(float(_get(s, "width", 10.5)), 11.0)) * factor
    depth = max(6.0, float(_get(s, "depth", 7.0))) * 1.10
    floors = max(1, min(2, int(_get(s, "floors", 2))))
    floor_h = float(_get(s, "floor_height", 2.8)) * .94
    civic = category in {"ASSEMBLY_HALL", "INN", "MARKET_HALL", "GATEHOUSE", "BARRACKS"}
    defensive = category in {"WATCHTOWER", "GATEHOUSE", "BARRACKS"} or context == "PASSWATCH"
    if category in {"WATCHTOWER"}:
        width = max(5.2, min(width, 7.2))
        depth = max(5.2, min(depth, 7.0))
        floors = max(2, floors)
    if category == "LONGHOUSE" or context == "HIGHSTEADS":
        width = max(width, 9.0)
        depth = max(depth, 7.2)
        floors = 1
    if civic:
        width *= 1.06
        depth *= 1.05
    if defensive:
        width *= .93
        depth *= .96

    tower_needed = (wealth == "AFFLUENT" or
                    category in {"ASSEMBLY_HALL", "WATCHTOWER", "GATEHOUSE"} or
                    context in {"PASSWATCH", "STONEWAKE"})
    roof = _mass(
        ctx, "thornfell_stone_hall", x=0, y=0, width=width, depth=depth,
        floors=floors, floor_height=floor_h, roof="GABLE", pitch=52,
        overhang=.18, openings="NARROW" if defensive else "DOMESTIC",
        entrance_edge=0, blocked_edges=(1, 3) if tower_needed else (1,),
        foundation="PLINTH",
    )
    _stepped_stone_gables(ctx,roof)

    # A side-set lower room creates a stepped plan/roofline; the shared wall is
    # blind, and its exposed entry faces the sheltered approach.
    annex_w = max(3.0, min(width*.40, 4.4))
    annex_d = max(3.0, min(depth*.52, 4.2))
    annex_x = width
    annex_y = depth*.20
    lower_base = roof.base + .42
    annex = _mass(
        ctx, "thornfell_lower_stone_range", x=annex_x, y=annex_y,
        width=annex_w, depth=annex_d, floors=1, floor_height=floor_h*.78,
        base=lower_base, roof="GABLE", pitch=50, overhang=.14,
        openings="NARROW", entrance_edge=0, blocked_edges=(3,),
        function='COTTAGE',
        foundation="PLINTH",
    )
    _stepped_stone_gables(ctx,annex)

    # Wealth, civic role, or frontier duty can justify a narrow signal tower.
    # It attaches on the side opposite the lower range, keeping both footprints
    # clear of each other and every aperture facing an exposed elevation.
    if tower_needed:
        tw = max(3.1, min(4.2, width*.38))
        td = max(3.0, min(4.0, depth*.42))
        tx = -tw
        ty = depth*.36
        tower_floors = 3 if wealth == "AFFLUENT" or category == "WATCHTOWER" else 2
        tower = _mass(
            ctx, "thornfell_signal_tower", x=tx, y=ty,
            width=tw, depth=td, floors=tower_floors, floor_height=floor_h,
            base=roof.base, roof="GABLE", pitch=55, overhang=.12,
            openings="NARROW", entrance_edge=0, blocked_edges=(1,),
            function='WATCHTOWER',
            foundation="PLINTH",
        )
        _stepped_stone_gables(ctx,tower)
        _thornfell_buttresses(ctx, tower, s, count=1 if detail == "LOW" else 2)

    _thornfell_buttresses(ctx, roof, s, count=1 if detail == "LOW" else 3)

    # Defensive/wealthy entries sit under an actual stone hood supported by
    # jamb piers. Keep the small hood in front of, rather than over, the door.
    if defensive or wealth == "AFFLUENT":
        doors=[o for o in roof.plan.facade_records[0]['openings'] if o['kind']=='door']
        if doors:
            door=doors[0]
            cx=(door['s0']+door['s1'])*.5
            hood_w=door['s1']-door['s0']+.76
            hood_y=roof.bounds[1]+.04
            hood_z=door['z1']+.16
            _box(ctx.buffer("thornfell_entry_lintel", "stone", "structure", zone=roof),
                 cx-hood_w*.5,hood_y-.11,hood_z,cx+hood_w*.5,hood_y+.11,hood_z+.18)
            for i,x in enumerate((cx-hood_w*.5+.12,cx+hood_w*.5-.12)):
                _box(ctx.buffer("thornfell_entry_jamb_%d" % i,"stone_light","structure",zone=roof),
                     x-.14,hood_y-.11,roof.base,x+.14,hood_y+.11,hood_z)

    # Exposed age is expressed through buttress repairs; low-detail mode still
    # keeps all primary stepped volumes, steep roofs, and narrow proportions.
    if age>=90 and float(s.maintenance)<.7 and detail == "HIGH":
        _thornfell_buttresses(ctx, annex, s, count=2)
