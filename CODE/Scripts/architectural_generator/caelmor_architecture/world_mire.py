"""Raised, linked Mire buildings for the world generator.

This is procedural art direction only: flood-ready occupied floors, pier frames,
longhouse proportions and bow roofs. It adds no lore or fixed resource claims.
"""
from __future__ import annotations

import math


def _base_height(settings):
    context = str(getattr(settings, "context", "SORROWMERE")).upper()
    wealth = str(getattr(settings, "wealth", "ESTABLISHED")).upper()
    # The ridge and surviving-root contexts stand on higher ground; the dense
    # settlement and forest edge need visibly greater flood clearance.
    clearance = {
        "SORROWMERE": 1.82,
        "MARSHFALL": 1.95,
        "GRIEFWATCH": 1.08,
        "ROOTREST": 1.30,
    }.get(context, 1.72)
    return clearance + {"MODEST": 0.0, "ESTABLISHED": 0.12,
                        "AFFLUENT": 0.30}.get(wealth, 0.12)


def _add_bow_ribs(ctx, mass, key, spacing=2.7):
    """Add restrained curved rafters just beneath the generated roof skin."""
    s = ctx.settings
    xmin, ymin, xmax, ymax = mass.bounds
    if str(getattr(s, "detail", "MEDIUM")).upper() == "LOW":
        count = 3
    elif str(getattr(s, "detail", "MEDIUM")).upper() == "HIGH":
        count = max(4, int(math.ceil(mass.width / spacing)) + 1)
    else:
        count = max(3, int(math.ceil(mass.width / spacing)) + 1)
    buf = ctx.buffer(key, "timber", "structure", zone=mass)
    ymin_in, ymax_in = ymin + .10, ymax - .10
    # Use the generated bow's actual transverse patch boundaries. A uniform
    # chord can cut across a concave shoulder and rise through the roof skin.
    cuts = {ymin_in, ymax_in}
    for patch in getattr(mass.plan, "custom_roof_sources", ()) or ():
        cuts.update(y for _, y in patch.poly if ymin_in + 1e-7 < y < ymax_in - 1e-7)
    stations = sorted(cuts)
    if len(stations) < 2:
        segments = 8 if str(getattr(s, "detail", "MEDIUM")).upper() != "LOW" else 4
        stations = [ymin_in + (ymax_in - ymin_in) * i / segments
                    for i in range(segments + 1)]
    for j in range(count):
        x = xmin + (xmax - xmin) * (j + .5) / count
        prev = None
        for y in stations:
            # Sample the mass's own roof envelope so every rafter follows the
            # actual piecewise bow. Drop the centreline by .28m so the complete
            # rectangular beam section clears the weather face by >.12m.
            z = mass.roof_height(x, y) - .28
            point = (x, y, z)
            if prev is not None:
                buf.beam(prev, point, width=.085 if s.detail == "LOW" else .11,
                         depth=.10)
            prev = point


def _add_underfloor_bracing(ctx, mass, key):
    """Tie the exposed pier frame below the occupied floor, within its plan."""
    s = ctx.settings
    buf = ctx.buffer(key, "timber", "structure", zone=mass)
    xmin, ymin, xmax, ymax = mass.bounds
    z = mass.base
    width, depth = xmax - xmin, ymax - ymin
    # Longitudinal ties and paired diagonal knees make the raised frame legible
    # as a load path rather than a decorative timber overlay on the wall skin.
    for y in (ymin + .35, ymax - .35):
        buf.beam((xmin + .18, y, z - .12), (xmax - .18, y, z - .12), .13, .14)
    brace_top = z - .14
    brace_low = max(.18, min(.55, z * .30))
    for x in (xmin + .22, (xmin + xmax) * .5, xmax - .22):
        buf.beam((x, ymin + .26, brace_low), (x, ymin + .92, brace_top), .09, .10)
        buf.beam((x, ymax - .26, brace_low), (x, ymax - .92, brace_top), .09, .10)
    # Wide public/community buildings gain a mid-span tie; narrow huts retain
    # a clear, open undercroft for water and flood debris.
    if width > 8.5:
        buf.beam((xmin + .24, (ymin + ymax) * .5, brace_top),
                 (xmax - .24, (ymin + ymax) * .5, brace_top), .10, .12)


def _add_access(ctx, mass, key, extra_width=0.0):
    """Build one continuous entry deck, stair, and side rails with clear gaps."""
    s = ctx.settings
    xmin, ymin, xmax, _ = mass.bounds
    z = mass.base
    # The mass's edge 0 is its south/front edge. The deck abuts that wall and
    # aligns with its entrance; the bottom landing sits beyond the stair run.
    out_y = ymin - (1.55 if s.wealth == "MODEST" else 1.9)
    left, right = xmin - extra_width, xmax + extra_width
    ctx.deck(f"{key}_front_deck",
             [(left, out_y), (right, out_y), (right, ymin), (left, ymin)],
             z=z, thickness=.16, material="timber", zone=None)
    span = right - left
    stair_w = min(1.35, max(1.0, span * .20))
    stair_x = (left + right) * .5
    boat=str(s.function).upper()=='BOATHOUSE'
    if boat:
        door=next(o for o in mass.plan.facade_records[0]['openings'] if o['kind']=='door')
        stair_x=xmin+(door['s0']+door['s1'])*.5
        stair_w=door['s1']-door['s0']+.30
    # `top` is the outer deck edge; the opening in the deck rail is centered
    # over the stair. Stair direction runs outward from the deck to grade.
    if boat:
        run=max(4.8,z*3.0)
        ramp=ctx.buffer(key+'_boat_slipway','timber','foundation')
        ramp.extrude([(stair_x-stair_w*.5,out_y-run,.08),
                      (stair_x+stair_w*.5,out_y-run,.08),
                      (stair_x+stair_w*.5,out_y,z),
                      (stair_x-stair_w*.5,out_y,z)],(0,0,-.14))
        for side in (-1,1):
            x=stair_x+side*stair_w*.40
            ramp.beam((x,out_y,z-.18),(x,out_y-run,.02),.16,.22)
            for i in range(4):
                t=i/4; height=z*(1-t)+.08*t-.20
                if height>.05:ramp.box((x,out_y-run*t,height*.5),(.18,.18,height))
    else:
        ctx.stair(f"{key}_entry_stair", top=(stair_x, out_y, z),
                  width=stair_w, run=max(2.4, z * 1.6), direction=(0, -1),
                  material="timber", zone=None)
    rail_z = z + .02
    for side_x in (left, right):
        ctx.rail(f"{key}_deck_rail_{'left' if side_x == left else 'right'}",
                 (side_x, ymin), (side_x, out_y), z=rail_z,
                 material="timber", zone=None)
    # Rails on the far edge stop short of the stair landing, preserving a clear
    # route to the stairs and to the front door.
    gap = stair_w * .5 + .12
    if stair_x - gap > left + .1:
        ctx.rail(f"{key}_outer_rail_left", (left, out_y),
                 (stair_x - gap, out_y), z=rail_z, material="timber", zone=None)
    if stair_x + gap < right - .1:
        ctx.rail(f"{key}_outer_rail_right", (stair_x + gap, out_y),
                 (right, out_y), z=rail_z, material="timber", zone=None)


def _should_add_pavilion(settings):
    wealth = str(getattr(settings, "wealth", "ESTABLISHED")).upper()
    function = str(getattr(settings, "function", "FARMHOUSE")).upper()
    context = str(getattr(settings, "context", "SORROWMERE")).upper()
    civic = function in {"INN", "ASSEMBLY_HALL", "MARKET_HALL", "LONGHOUSE",
                         "CHAPEL", "WAREHOUSE", "BARRACKS"}
    return wealth == "AFFLUENT" or (civic and context == "SORROWMERE")


def _rear_work_landing(ctx,mass):
    for record in mass.plan.facade_records:
        for door in record['openings']:
            if door.get('role') not in ('passage_exit','loading'):continue
            if record['edge_index']!=2:continue
            a,b=mass.plan.edges[2]
            center=(door['s0']+door['s1'])*.5
            x=a[0]-center; y=a[1]; z=mass.base
            half=(door['s1']-door['s0'])*.5+.28
            ctx.deck('mire_rear_work_landing',[(x-half,y),(x+half,y),(x+half,y+1.35),(x-half,y+1.35)],z)
            for side in (-1,1):
                ctx.rail('mire_rear_work_rail_'+str(side),(x+side*half,y),(x+side*half,y+1.35),z+.01)
            if door.get('role')=='passage_exit':
                ctx.stair('mire_passage_exit_stair',top=(x,y+1.35,z),width=1.35,run=max(2.4,z*1.6),direction=(0,1))


def build(ctx):
    """Create Mire massing and access on an existing world build context."""
    s = ctx.settings
    width, depth = float(s.width), float(s.depth)
    floor_height = float(s.floor_height)
    base = _base_height(s)
    function = str(s.function).upper()
    add_pavilion = _should_add_pavilion(s)
    # Narrow the building plan while preserving its capacity by lengthening it;
    # stores/work halls retain a little more breadth for moving goods.
    narrow = function not in {"WAREHOUSE", "GRAIN_STORE", "MARKET_HALL",
                              "ASSEMBLY_HALL", "BOATHOUSE"}
    if narrow and width > depth * 1.48:
        width = depth * 1.42
    elif function in {"LONGHOUSE", "BARRACKS", "INN", "FARMHOUSE"}:
        width *= 1.05
    width = max(5.0, width)
    depth = max(4.0, depth)
    mass = ctx.mass(
        "mire_longhouse", x=0.0, y=0.0, width=width, depth=depth,
        floors=max(1, int(s.floors)), floor_height=floor_height, base=base,
        roof="BOW", pitch=float(s.pitch), overhang=.68,
        openings="DOMESTIC", entrance_edge=0,
        access_edges=(1,) if add_pavilion else (),
        steps=False, foundation="PIERS")
    _add_bow_ribs(ctx, mass, "mire_bow_roof_ribs")
    _add_underfloor_bracing(ctx, mass, "mire_pier_crossbracing")
    _rear_work_landing(ctx,mass)

    # A prosperous Sorrowmere household or a civic building gains a real second
    # roofed volume. It sits beside, never through, the main walls; a shared
    # deck links the two occupied floors as a raised compound.
    pavilion = None
    if add_pavilion:
        aw = min(5.4, max(3.8, width * .40))
        ad = min(depth * .78, 6.0)
        gap = 1.8
        pavilion = ctx.mass(
            # Mass x/y are the southwest plan origin, not the centre point.
            "mire_linked_pavilion", x=width + gap, y=(depth - ad) * .5,
            width=aw, depth=ad, floors=1, floor_height=floor_height,
            base=base, roof="BOW", pitch=float(s.pitch), overhang=.58,
            openings="DOMESTIC", entrance_edge=3, steps=False,
            function='COTTAGE',
            foundation="PIERS")
        _add_bow_ribs(ctx, pavilion, "mire_pavilion_bow_ribs")
        _add_underfloor_bracing(ctx, pavilion, "mire_pavilion_bracing")
        pxmin, pymin, pxmax, pymax = pavilion.bounds
        # A broad raised connector reaches matching side doors centered on
        # both occupied volumes; the gap leaves room for their roof eaves.
        deck_y0 = max(pymin, depth * .5 - .9)
        deck_y1 = min(pymax, depth * .5 + .9)
        ctx.deck("mire_pavilion_link_deck",
                 [(width, deck_y0), (pxmin, deck_y0),
                  (pxmin, deck_y1), (width, deck_y1)],
                 z=base, thickness=.16, material="timber", zone=None)
        # Rails guard the exposed sides of the connector; the ends stay open
        # into the two building entrances.
        ctx.rail("mire_pavilion_link_rail_south",
                 (width, deck_y0), (pxmin, deck_y0), z=base + .02,
                 material="timber", zone=None)
        ctx.rail("mire_pavilion_link_rail_north",
                 (width, deck_y1), (pxmin, deck_y1), z=base + .02,
                 material="timber", zone=None)
        _add_access(ctx, mass, "mire_access", extra_width=0.0)
    else:
        _add_access(ctx, mass, "mire_access")
    return mass
