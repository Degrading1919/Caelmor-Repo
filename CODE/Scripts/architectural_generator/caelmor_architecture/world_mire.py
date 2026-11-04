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
        if s.crafted_curves:
            from .curve_sweep import sweep_member
            centers = [(x,y,mass.roof_height(x,y)-.28) for y in stations]
            width = .085 if s.detail == "LOW" else .11
            sweep_member(buf,centers,(1,0,0),[width]*len(centers),[.10]*len(centers))
            continue
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
    door=next((o for o in mass.plan.facade_records[0]['openings'] if o['kind']=='door'),None)
    entrance_x=xmin+(door['s0']+door['s1'])*.5 if door else (left+right)*.5
    # A modest home pays for a usable landing, not a promenade across every
    # window. Working/public buildings keep the goods-handling frontage.
    if s.wealth=='MODEST' and s.function in ('COTTAGE','FARMHOUSE','TOWNHOUSE','MERCHANT_HOUSE'):
        left,right=entrance_x-1.35,entrance_x+1.35
        out_y=ymin-1.45
    ctx.deck(f"{key}_front_deck",
             [(left, out_y), (right, out_y), (right, ymin), (left, ymin)],
             z=z, thickness=.16, material="timber", zone=None)
    span = right - left
    stair_w = min(1.35, max(1.0, span * .20))
    stair_x = entrance_x
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


def _sheltered_work_deck(ctx,mass):
    """A lower reed porch, with a real ledger, front posts and shoulder braces.

    The roof drains away from the dwelling; its ledger tucks below the existing
    bow eave. Its declared plane validates the complete exposed timber sections.
    """
    x0,y0,x1,_=mass.bounds
    front=y0-1.72
    back=y0+.035
    slope=.095
    door=next(o for o in mass.plan.facade_records[0]['openings'] if o['kind']=='door')
    # Upper-storey houses can have taller goods/entry doors than cottages.
    # Derive the veranda from the complete head assembly, not a fixed datum.
    head=door.get('assembly_bounds',door)['z1']
    front_z=max(mass.base+2.30,head+.17)
    if front_z+slope*(back-front)>mass.roof_height((x0+x1)*.5,y0)-.17:
        return False  # no legal weather/door clearance at this low eave
    c=front_z-slope*front
    plane=(0.,slope,c)
    def height(y):return slope*y+c
    roof=ctx.buffer('mire_work_veranda_reed_roof','roof','roof',mass)
    roof.extrude([(x0-.16,front-.12,height(front-.12)),
                  (x1+.16,front-.12,height(front-.12)),
                  (x1+.16,back,height(back)),(x0-.16,back,height(back))],(0,0,-.10))
    frame=ctx.buffer('mire_work_veranda_frame','timber','structure',mass)
    frame.roof_envelope={'plane':plane,'clearance':.12}
    ledger_z=height(back)-.23
    frame.beam((x0+.10,back,ledger_z),(x1-.10,back,ledger_z),.13,.16)
    edge_z=height(front)-.23
    frame.beam((x0+.10,front,edge_z),(x1-.10,front,edge_z),.15,.17)
    # Front posts stand on the deck supports' load line, clear of the entry.
    entry=x0+(door['s0']+door['s1'])*.5
    stations=[x0+.18,x1-.18]
    stations += [x for x in (x0+mass.width/3,x0+mass.width*2/3) if abs(x-entry)>1.15]
    for i,x in enumerate(sorted(stations)):
        frame.chamfered_beam((x,front,mass.base),(x,front,edge_z),.15,.15,
                             .018 if ctx.settings.craftsmanship=='FINE' else .006)
        # Knee meets both post and front plate; no floating decorative brace.
        toward=1 if x<(x0+x1)*.5 else -1
        frame.beam((x,front,edge_z-.52),(x+toward*.46,front,edge_z),.085,.10)
    for i in range(max(3,math.ceil(mass.width/1.45))+1):
        x=x0+.12+(mass.width-.24)*i/max(3,math.ceil(mass.width/1.45))
        frame.beam((x,front,height(front)-.18),(x,back,height(back)-.18),.07,.08)
    # Establishing the porch is an investment in dry work space; it is never
    # conditioned on wear or age and remains visible at LOW detail.


def _private_link_screens(ctx,x0,x1,y0,y1,z):
    """Boarded lower rails give the separate room a genuinely private approach."""
    for side,y in (('south',y0),('north',y1)):
        rail=ctx.rail('mire_private_link_screen_'+side,(x0,y),(x1,y),z+.02)
        y=max(rail.support_surface['bounds'][1]+.06,
              min(rail.support_surface['bounds'][3]-.06,y))
        count=max(4,math.ceil((x1-x0)/.18))
        for i in range(count):
            x=x0+.10+(x1-x0-.20)*(i+.5)/count
            rail.box((x,y,z+.52),(.115,.045,.84))


def _pier_repair(ctx,mass):
    if ctx.settings.age<70 or ctx.settings.maintenance>=.6:return
    x0,y0,_,_=mass.bounds
    repair=ctx.buffer('mire_sistered_pier_repair','timber_light','foundation',mass)
    # New pile adjacent to the existing southwest pile; a real head tie carries
    # the same floor, rather than scattering cosmetic damage over every board.
    repair.box((x0+.32,y0+.18,mass.base*.5),(.14,.16,mass.base))
    repair.beam((x0+.13,y0+.18,mass.base-.12),
                (x0+.42,y0+.18,mass.base-.12),.12,.16)


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
    if s.wealth!='MODEST':
        _sheltered_work_deck(ctx,mass)
    if pavilion is not None:
        _private_link_screens(ctx,width,pxmin,deck_y0,deck_y1,base)
    _pier_repair(ctx,mass)
    return mass
