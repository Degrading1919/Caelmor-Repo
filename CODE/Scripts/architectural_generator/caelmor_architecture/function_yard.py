"""Function-first farm and fortified access buildings.

These assemblies describe working layouts (stalls, handling lanes, guarded
passages) independently of the general regional massing builders.
"""
import math
from .functional import Builder


def _stable_capacity(builder):
    """Return two to six bays from household investment, with a stable seed."""
    wealth = str(getattr(builder.settings, 'wealth', 'ESTABLISHED')).upper()
    craft = str(getattr(builder.settings, 'craftsmanship', 'STANDARD')).upper()
    seed = int(getattr(builder.settings, 'seed', 0))
    capacity = {'MODEST': 3, 'ESTABLISHED': 4, 'AFFLUENT': 5}.get(wealth, 4)
    capacity += {'ROUGH': -1, 'STANDARD': 0, 'SKILLED': 1,
                 'FINE': 1}.get(craft, 0)
    # A small, reproducible investment variation keeps same-tier holdings from
    # becoming clones while preserving a useful, bounded stable footprint.
    capacity += 1 if seed % 7 == 0 else (-1 if seed % 11 == 0 else 0)
    return max(2, min(6, capacity))


def build_stable(ctx):
    """Build an open-sided, divided stable with a clear handling approach."""
    b = Builder(ctx, 'STABLE')
    region = str(getattr(b.settings, 'region', 'LOWMARK')).upper()
    capacity = _stable_capacity(b)
    stall_width, depth = 2.9, 6.2
    aisle_depth = 2.6
    # Add one covered service bay for hay so all numbered stalls remain clear.
    width = (capacity + 1) * stall_width
    base = b.base
    zone_key = 'stable_shelter'
    service_x0 = capacity * stall_width
    animal_bay = (capacity - 1) // 2
    animal_x = (animal_bay + .5) * stall_width
    service_access_x = service_x0 + 2.0

    # The long side-open shelter keeps stalls and the handling aisle legible.
    # MIRE's raised timber floor is a practical flood adaptation inference;
    # it does not imply a new animal, custom, or fixed flood datum.
    open_access = [
        {'edge_index': 0, 's0': bay * stall_width + (stall_width - 1.4) * .5,
         's1': bay * stall_width + (stall_width + 1.4) * .5, 'height': 2.25}
        for bay in range(capacity)
    ]
    rear_center = width - service_access_x  # edge 2 is oriented from x=width to x=0
    open_access.append({'edge_index': 2, 's0': rear_center - .7,
                        's1': rear_center + .7, 'height': 2.25})
    shelter = b.mass(
        zone_key, x=0.0, y=0.0, width=width, depth=depth, floors=1,
        floor_height=3.4,
        function='STABLE', open_edges=[0, 2], open_access=open_access,
        openings='NONE', foundation='PIERS' if region == 'MIRE' else 'PLINTH',
    )
    zone = shelter

    # Open-edge framing reserves a proper 1.4m service door in the hay bay.
    # Rebuild the other rear-wall spans as solid regional panels so the animal
    # stalls stay weather-sheltered instead of turning the whole rear into an
    # arcade. The hay route runs through the one deliberately clear gap.
    rear_wall_material = 'stone_light' if region in ('THORNFELL', 'EMBERHOLT') else 'timber_light'
    wall_top = base + 3.20
    for bay in range(capacity):
        x0, x1 = bay * stall_width + .10, (bay + 1) * stall_width - .10
        b.box(f'stable.rear_stall_wall.{bay}',
              (x0, depth - .12, base, x1, depth + .06, wall_top),
              rear_wall_material, zone, role='weather_wall')
    b.box('stable.rear_hay_wall.west',
          (service_x0 + .02, depth - .12, base,
           service_access_x - .70, depth + .06, wall_top),
          rear_wall_material, zone, role='weather_wall')
    b.box('stable.rear_hay_wall.east',
          (service_access_x + .70, depth - .12, base,
           width - .02, depth + .06, wall_top),
          rear_wall_material, zone, role='weather_wall')

    # A broad handling apron faces stalls that are about 2.9m wide by 3.6m
    # deep. Low split gates define the stall fronts while leaving a 1.4m lead-in.
    partition_mat = 'stone_light' if region == 'THORNFELL' else 'timber_light'
    for bay in range(capacity):
        x0, x1 = bay * stall_width, (bay + 1) * stall_width
        if bay:
            # A bearing post stands at each stall division on the open frontage;
            # this carries the long roof without interrupting the 1.4m openings.
            post_x = x0
            post_top = shelter.roof_height(post_x, 0.0) - .22
            key=f'stable.front_bearing_post.{bay}'
            is_timber=region not in ('THORNFELL', 'EMBERHOLT')
            post=b.box(key,(post_x-.12,-.10,base,post_x+.12,.10,post_top),
                       'timber' if is_timber else 'stone',zone,role='structure')
            if is_timber:
                spec=ctx.component(post,zone,key,'frame_member','structural_timber')
                if spec and spec.variant:
                    from .construction_geometry import hewn_member
                    from .construction_library import timber_workmanship
                    start,end=(post_x,0.,base),(post_x,0.,post_top)
                    post.vertices.clear()
                    post.faces.clear()
                    if spec.variant=='hewn_pegged' and b.settings.detail!='LOW':
                        hewn_member(post,start,end,.24,.20,timber_workmanship(b.settings),
                                    ctx.rng(key))
                    else:
                        post.chamfered_beam(start,end,.24,.20,.006)
            if is_timber:
                bent = b.fixture(f'stable.front_bent_brace.{bay}', 'timber',
                                 zone, role='structure')
                for side in (-1, 1):
                    bent.beam((post_x, 0.0, post_top - .10),
                              (post_x + side * .48, 0.0, post_top - .82),
                              .10, .10)
            b.box(f'stable.divider.{bay}',
                  (x0 - .09, aisle_depth, base, x0 + .09, depth - .18,
                   base + 1.30), partition_mat, zone, role='partition')
        # Open framed gate leaves read as working joinery while preserving the
        # full animal-width lead-in between the two wings.
        gate_half = (stall_width - 1.4) * .5
        for wing, xa, xb in (('left', x0, x0 + gate_half),
                             ('right', x1 - gate_half, x1)):
            if region == 'THORNFELL':
                # Dense stone knee walls break the exposed ridge wind below
                # the gate leaves while keeping the 1.4m lead-in unobstructed.
                b.box(f'stable.ridge_stone_knee.{bay}.{wing}',
                      (xa + .05, aisle_depth - .10, base,
                       xb - .05, aisle_depth + .10, base + .55),
                      'stone', zone, role='windbreak')
            gate_x0, gate_x1 = xa + .09, xb - .09
            gate_y = aisle_depth
            gate_bottom = base + (.55 if region == 'THORNFELL' else 0.0)
            gate_top = base + 1.08
            # Keep the semantic gate station on its bottom rail; the added
            # members are construction detail and preserve the same opening.
            b.box(f'stable.split_gate.{bay}.{wing}',
                  (gate_x0, gate_y - .05, gate_bottom + .03,
                   gate_x1, gate_y + .05, gate_bottom + .13),
                  'timber_light', zone, role='stall_gate')
            b.box(f'stable.split_gate.rail.{bay}.{wing}',
                  (gate_x0, gate_y - .045, gate_bottom + .45,
                   gate_x1, gate_y + .045, gate_bottom + .54),
                  'timber_light', zone, role='structure')
            b.box(f'stable.split_gate.top.{bay}.{wing}',
                  (gate_x0, gate_y - .05, gate_top - .11,
                   gate_x1, gate_y + .05, gate_top - .01),
                  'timber_light', zone, role='structure')
            for post, post_x in enumerate((gate_x0, gate_x1)):
                b.box(f'stable.split_gate.stile.{bay}.{wing}.{post}',
                      (post_x - .045, gate_y - .05, gate_bottom + .08,
                       post_x + .045, gate_y + .05, gate_top - .06),
                      'timber_light', zone, role='structure')
            gate_brace = b.fixture(f'stable.split_gate.brace.{bay}.{wing}',
                                   'timber_light', zone, role='structure')
            gate_brace.beam((gate_x0 + .04, gate_y, gate_bottom + .12),
                            (gate_x1 - .04, gate_y, gate_top - .10),
                            .065, .065)
        center = (x0 + x1) * .5
        manger_material = ('stone_light' if region in ('THORNFELL', 'EMBERHOLT')
                          else 'timber')
        # Keep the historic station key on the trough floor; separate sides
        # leave the inside open so the feed trough has a readable hollow profile.
        b.box(f'stable.manger.{bay}',
              (center - .68, depth - .74, base + .40,
               center + .68, depth - .32, base + .50),
              manger_material, zone, role='feeding')
        b.box(f'stable.manger.side.front.{bay}',
              (center - .68, depth - .74, base + .48,
               center + .68, depth - .66, base + .78),
              manger_material, zone, role='feeding')
        b.box(f'stable.manger.side.back.{bay}',
              (center - .68, depth - .40, base + .48,
               center + .68, depth - .32, base + .78),
              manger_material, zone, role='feeding')
        for end, x0, x1 in (('west', center - .68, center - .60),
                            ('east', center + .60, center + .68)):
            b.box(f'stable.manger.end.{bay}.{end}',
                  (x0, depth - .66, base + .48,
                   x1, depth - .40, base + .78),
                  manger_material, zone, role='feeding')
        b.box(f'stable.hayrack.rail.{bay}',
              (center - .78, depth - .24, base + .92,
               center + .78, depth - .10, base + 1.04),
              'timber_light', zone, role='feeding')
        rack = b.fixture(f'stable.hayrack.profile.{bay}', 'timber_light',
                         zone, role='feeding')
        for side in (-1, 1):
            rack.beam((center + side * .70, depth - .20, base + .58),
                      (center + side * .70, depth - .12, base + 1.0),
                      .075, .075)
        for slat in range(5):
            sx = center - .64 + slat * .32
            b.box(f'stable.hayrack.slat.{bay}.{slat}',
                  (sx - .035, depth - .22, base + .50,
                   sx + .035, depth - .10, base + 1.02),
                  'timber_light', zone, role='feeding')

    # The service bay stores hay behind a low partition and stays outside the
    # animal route, while sharing the same roofed working volume.
    b.box('stable.hay_store.partition',
          (service_x0, aisle_depth, base, service_x0 + .12, depth - .15,
           base + 1.55), partition_mat, zone, role='storage')
    for shelf, z0 in enumerate((base + .10, base + .78)):
        b.box(f'stable.hay_store.shelf.{shelf}',
              (service_x0 + .20, depth - .80, z0,
               service_x0 + 1.05, depth - .57, z0 + .10),
              'timber', zone, role='storage')
    b.box('stable.hay_store.stack',
          (service_x0 + .20, depth - 1.05, base + .10,
           service_x0 + 1.05, depth - .28, base + 1.30),
          'timber', zone, role='storage')

    # A framed service opening ties the hay bay, rear weather-wall gaps and
    # loading route together as one purposeful construction.
    service_frame_x0 = service_access_x - .78
    service_frame_x1 = service_access_x + .78
    frame_y0, frame_y1 = depth - .14, depth
    frame_top = base + 2.38
    for side, px in (('west', service_frame_x0), ('east', service_frame_x1)):
        b.box(f'stable.hay_service_frame.post.{side}',
              (px - .08, frame_y0, base, px + .08, frame_y1, frame_top),
              'timber' if region not in ('THORNFELL', 'EMBERHOLT') else 'stone',
              zone, role='structure')
    b.box('stable.hay_service_frame.header',
          (service_frame_x0, frame_y0, frame_top,
           service_frame_x1, frame_y1, frame_top + .20),
          'timber' if region not in ('THORNFELL', 'EMBERHOLT') else 'stone_light',
          zone, role='structure')

    # Reserve a continuous clear front apron and the animal-width approach.
    # MIRE's gentle ramp is 1:7 onto the raised bank.
    for bay in range(capacity):
        center = (bay + .5) * stall_width
        b.route(f'stable.stall_entry.{bay}',
                (center - .68, 0.0, base + .05,
                 center + .68, aisle_depth - .12, base + 2.25))
        b.route(f'stable.stall_access.{bay}',
                (center - .68, aisle_depth + .12, base + .05,
                 center + .68, depth - 1.0, base + 2.25), kind='animal')
    b.route('stable.animal_access',
            (animal_x - .68, -8.0, .02, animal_x + .68, aisle_depth - .12,
             base + 2.25), kind='animal')
    ramp_run = max(3.0, base * 7.0)
    b.ramp('stable.front_animal_ramp',
           (animal_x, -ramp_run), (animal_x, 0.0), 2.0, base, zone=zone)
    b.ramp('stable.rear_service_ramp',
           (service_access_x, depth + ramp_run),
           (service_access_x, depth), 2.0, base, zone=zone)
    b.route('stable.hay_service_access',
            (service_access_x - .68, depth, base + .05,
             service_access_x + .68, depth + ramp_run, base + 2.25),
            kind='service')
    if region == 'MIRE' and base > .35:
        # Piles and a narrow raised service walk express the adapted platform.
        b.deck('stable.mire_service_walk',
               [(0.0, 0.0), (width, 0.0), (width, .65), (0.0, .65)],
               z=base, material='timber', zone=zone)
    elif region == 'THORNFELL':
        # A stone working apron suits the ridge setting and supports loading.
        b.deck('stable.ridge_forecourt',
               [(0.0, -.85), (width, -.85), (width, 0.0), (0.0, 0.0)],
               z=base, material='stone', zone=zone)
    else:
        # Lowmark and Emberholt retain a simple firm approach, with a broad
        # turnout to allow carts to meet the animal lane without constriction.
        b.deck('stable.yard_apron',
               [(-1.0, -1.1), (width + 1.0, -1.1),
                (width + 1.0, 0.0), (-1.0, 0.0)],
               z=base, material='stone' if region == 'EMBERHOLT' else 'timber',
               zone=zone)
    if region == 'LOWMARK':
        # A narrow raised hay loft uses the high centre of the gable and opens
        # over the separate service bay; it stays above the clear loading route.
        loft_z = base + 2.18
        b.deck('stable.lowmark_hay_loft',
               [(service_x0 + 1.18, 2.75), (width - .18, 2.75),
                (width - .18, depth - .85), (service_x0 + 1.18, depth - .85)],
               z=loft_z, material='timber', zone=zone)
        for post, (px, py) in enumerate(((service_x0 + 1.42, 2.95),
                                         (width - .22, 2.95),
                                         (service_x0 + 1.42, depth - 1.0),
                                         (width - .22, depth - 1.0))):
            b.box(f'stable.lowmark_loft_post.{post}',
                  (px - .08, py - .08, base + 1.25,
                   px + .08, py + .08, loft_z), 'timber', zone, role='structure')
        b.box('stable.lowmark_loft_hay_stack',
              (service_x0 + 1.48, 3.05, loft_z + .02,
               width - .42, depth - 1.10, loft_z + .68),
              'timber_light', zone, role='storage')
        ladder = b.fixture('stable.lowmark_loft_ladder', 'timber', zone, role='access')
        ladder.beam((width - .64, depth - .16, base + .15),
                    (width - .64, depth - .92, loft_z), .09, .11)
        ladder.beam((width - .24, depth - .16, base + .15),
                    (width - .24, depth - .92, loft_z), .09, .11)
        for rung in range(9):
            z = base + .25 + rung * (loft_z - base - .30) / 8
            ladder.beam((width - .62, depth - .16 - .76 * rung / 8, z),
                        (width - .26, depth - .16 - .76 * rung / 8, z), .065, .065)
    elif region == 'EMBERHOLT':
        # Iron hitch rings and stone posts make this a working yard, not just
        # a larger apron; they sit outside the animal approach lane.
        for side, x in (('west', .48), ('east', width - .48)):
            for index, y in enumerate((-.72, -.32)):
                b.box(f'stable.ember_yard_hitch_post.{side}.{index}',
                      (x - .13, y - .13, base, x + .13, y + .13, base + 1.22),
                      'stone', zone, role='yard_equipment')
                fixture = b.fixture(f'stable.ember_yard_hitch_ring.{side}.{index}',
                                    'iron', zone, role='yard_equipment')
                fixture.beam((x, y - .14, base + .86),
                             (x, y + .14, base + .86), .055, .055)
    return b.finish()


def _stair_to_guard_floor(b, prefix, x, y0, y1, base, upper, zone, material):
    """Build stepped access with visible treads and a continuous handrail."""
    steps = 16
    run = y1 - y0
    for i in range(steps):
        y = y0 + run * (i + .5) / steps
        z = base + (upper - base) * (i + 1) / steps
        b.box(f'{prefix}.tread.{i}',
              (x - .52, y - run / steps * .52, z - .13,
               x + .52, y + run / steps * .52, z),
              material, zone, role='access')
    stair = b.fixture(f'{prefix}.stringers', material, zone, role='access')
    for side in (-1, 1):
        stair.beam((x + side * .49, y0, base + .04),
                   (x + side * .49, y1, upper - .06), .13, .17)
    rail = b.fixture(f'{prefix}.handrails', material, zone, role='access')
    for side in (-1, 1):
        rail.beam((x + side * .55, y0, base + .92),
                  (x + side * .55, y1, upper + .92), .075, .075)
    b.route(prefix + '.clearance',
            (x - .58, y0, base, x + .58, y1, upper + .02), kind='stair')


def build_gatehouse(ctx):
    """Build a defended through-passage with flank towers and guard access."""
    if ctx.settings.region=='THORNFELL':
        from .benchmark_gatehouse import build
        return build(ctx)
    b = Builder(ctx, 'GATEHOUSE')
    region = str(getattr(b.settings, 'region', 'LOWMARK')).upper()
    base = b.base
    tower_width = 4.6 if region == 'THORNFELL' else 5.0
    core_width = 6.0
    depth = 8.4
    tower_depth = 7.0
    total_width = 2 * tower_width + core_width
    height = 3.8
    roof = ('TERRACE' if region == 'EMBERHOLT' else
            'GABLE' if region == 'THORNFELL' else b.roof)
    portal_material = 'iron' if region == 'EMBERHOLT' else 'timber'
    core_x = tower_width
    zone_key = 'gatehouse_portal'

    # The central volume itself owns the validated aligned entry and exit.
    # Side masses are true watchtowers and leave that passage untouched.
    core = b.mass(zone_key, x=core_x, y=0.0, width=core_width, depth=depth,
           floors=2, floor_height=height, function='GATEHOUSE',
           roof=roof, openings='NARROW', blocked_edges=[1, 3])
    tower_roof = roof
    tower_front = -0.6 if region != 'MIRE' else 0.0
    left = b.mass('gatehouse_west_watchtower', x=0.0, y=tower_front,
                  width=tower_width, depth=tower_depth, floors=3,
                  floor_height=height, function='WATCHTOWER',
                  roof=tower_roof, openings='NARROW', blocked_edges=[1])
    right_y = 1.2 if region == 'MIRE' else tower_front
    right_access = ([{'edge_index': 1, 's0': tower_depth * .5 - .7,
                      's1': tower_depth * .5 + .7, 'height': 2.25}]
                    if region == 'MIRE' else [])
    right = b.mass('gatehouse_east_watchtower', x=core_x + core_width, y=right_y,
                   width=tower_width, depth=tower_depth, floors=3,
                   floor_height=height, function='WATCHTOWER',
                   roof=tower_roof, openings='NARROW', blocked_edges=[3],
                   open_access=right_access,
                   access_edges=[1] if region == 'MIRE' else [])
    zone = core

    passage_width = 2.8
    passage_x0 = core_x + (core_width - passage_width) / 2.0
    passage_x1 = passage_x0 + passage_width
    passage = core.plan.passage_geometry
    clear_height = passage['clear_height']
    clear_width = passage['clear_width']
    b.route('gatehouse_open_through_passage',
            (core_x + (core_width - clear_width) * .5, 0.0, base,
             core_x + (core_width + clear_width) * .5, depth, base + clear_height))

    # Each timber/iron gate leaf is parked flat against the portal cheek when
    # open, leaving the tested central route fully clear.
    b.box('gatehouse.open_leaf.west',
          (core_x + .12, .14, base, core_x + 1.52, .30, base + clear_height),
          portal_material, zone, role='gate_leaf')
    b.box('gatehouse.open_leaf.east',
          (core_x + core_width - 1.52, .14, base,
           core_x + core_width - .12, .30, base + clear_height),
          portal_material, zone, role='gate_leaf')
    # The grille is visibly lifted into the front portal head, clear of the
    # measured passage opening. One set of uprights and rails avoids doubled bars.
    grille_low = base + clear_height + .06
    grille_high = base + height - .08
    grille_y0, grille_y1 = .27, .43
    for bar in range(9):
        bx = passage_x0 + .12 + bar * (passage_width - .24) / 8
        b.box(f'gatehouse.portcullis.upright.{bar}',
              (bx - .035, grille_y0, grille_low,
               bx + .035, grille_y1, grille_high), 'iron', zone, role='defense')
    for rail_index, z in enumerate((grille_low + .10, grille_high - .10)):
        b.box(f'gatehouse.portcullis.crossbar.{rail_index}',
              (passage_x0, grille_y0, z - .04,
               passage_x1, grille_y1, z + .04), 'iron', zone, role='defense')

    # Iron guides sit just outside the measured clear width; hinge plates fix
    # the parked leaves to the portal cheeks instead of leaving them as props.
    guides = b.fixture('gatehouse.portcullis.guides', 'iron', zone,
                       role='defense')
    for gx in (passage_x0 - .10, passage_x1 + .10):
        guides.beam((gx, .30, base + .18),
                    (gx, .30, base + height - .12), .09, .09)
    hinges = b.fixture('gatehouse.open_leaf.hinges', 'iron', zone,
                       role='structure')
    for hx in (core_x + .20, core_x + core_width - .20):
        for hz in (base + .35, base + clear_height - .28):
            hinges.beam((hx, .12, hz), (hx, .38, hz), .10, .10)

    # Build the portal as a supported threshold on both faces. Masonry regions
    # use a shallow relieving arch above the unchanged rectangular clear box;
    # timber regions use a deep beam seated on full-height jamb posts.
    portal_mat = {'LOWMARK': 'stone_light', 'THORNFELL': 'stone',
                  'MIRE': 'timber', 'EMBERHOLT': 'stone'}[region]
    for face, face_y0, face_y1 in (
            ('front', -.62, .42), ('rear', depth - .42, depth + .62)):
        for side, px0, px1 in (
                ('west', passage_x0 - .40, passage_x0 - .08),
                ('east', passage_x1 + .08, passage_x1 + .40)):
            key = (f'gatehouse.lowmark_stone_portal_cheek.{side}'
                   if region == 'LOWMARK' and face == 'front' else
                   f'gatehouse.ridge_portal_pier.{side}'
                   if region == 'THORNFELL' and face == 'front' else
                   f'gatehouse.portal_jamb.{face}.{side}')
            if region == 'MIRE':
                jamb = b.fixture(key, portal_mat, zone, role='structure')
                jamb.beam(((px0 + px1) * .5,
                           (face_y0 + face_y1) * .5, base),
                          ((px0 + px1) * .5,
                           (face_y0 + face_y1) * .5,
                          base + clear_height + .12), .34, .34)
            else:
                b.box(key, (px0, face_y0, base, px1, face_y1,
                            base + clear_height + .12), portal_mat, zone,
                      role='structure')
        if region in ('THORNFELL', 'EMBERHOLT'):
            arch = b.fixture(f'gatehouse.portal_arch.{face}', portal_mat,
                             zone, role='structure')
            # Radial wedge stones carry a segmental relieving arch. Construct
            # the full intrados/extrados, rather than rotating rectangular
            # beams whose section can dip into the declared clear opening.
            center=(passage_x0+passage_x1)*.5
            radius=(passage_x1-passage_x0)*.5
            segments = 7
            spring = base + clear_height + .12
            rise = .40
            front_y=-.43 if face=='front' else depth-.12
            for index in range(segments):
                t0=math.pi*(index+.012)/segments
                t1=math.pi*(index+.988)/segments
                points=[(center+r*math.cos(t),front_y,spring+h*math.sin(t))
                        for r,h,t in ((radius,rise,t0),(radius,rise,t1),
                                      (radius+.30,rise+.32,t1),(radius+.30,rise+.32,t0))]
                arch.extrude(points,(0,.55,0))
        else:
            if region == 'MIRE':
                lintel = b.fixture(f'gatehouse.portal_lintel.{face}',
                                   'timber', zone, role='structure')
                lintel.beam((passage_x0 - .08,
                             (face_y0 + face_y1) * .5,
                             base + clear_height + .40),
                            (passage_x1 + .08,
                             (face_y0 + face_y1) * .5,
                             base + clear_height + .40), .22, .66)
            else:
                b.box(f'gatehouse.portal_lintel.{face}',
                      (passage_x0 - .08, face_y0, base + clear_height + .08,
                       passage_x1 + .08, face_y1, base + clear_height + .34),
                      portal_mat, zone, role='structure')

    # Ridge and Emberholt stone towers carry stepped corner feet into the
    # ground; Lowmark relies on its timber frame and Mire on raised piles.
    if region in ('THORNFELL', 'EMBERHOLT'):
        for side, owner in (('west', left), ('east', right)):
            tx0, ty0, tx1, ty1 = owner.bounds
            # Each broad front/rear blade begins .45m out from the wall and
            # slopes back to an engaged upper bearing at 4.8m. The .72m width
            # makes it a true buttress rather than a thin applied strip.
            for face, wall_y, direction in (('front', ty0, -1),
                                             ('rear', ty1, 1)):
                for corner, cx in (('west', tx0 + .36),
                                   ('east', tx1 - .36)):
                    buttress = b.fixture(
                        f'gatehouse.{side}_tower_buttress.{face}.{corner}',
                        'stone' if region == 'THORNFELL' else 'stone_light',
                        owner, role='structure')
                    buttress.extrude([
                        (cx-.36,wall_y-direction*.12,base),
                        (cx-.36,wall_y+direction*.60,base),
                        (cx-.36,wall_y+direction*.14,base+4.8),
                        (cx-.36,wall_y-direction*.12,base+4.8)],(.72,0,0))
    if region == 'EMBERHOLT':
        # A projecting corbel band gives the terrace towers a deliberate heavy
        # crown; it is exterior massing, not a claim of a walkable roof walk.
        for side, owner in (('west', left), ('east', right)):
            tx0, ty0, tx1, ty1 = owner.bounds
            crown_z0 = base + 3 * height - .52
            crown_z1 = base + 3 * height - .24
            b.box(f'gatehouse.{side}_tower_crown.front',
                  (tx0, ty0 - .18, crown_z0, tx1, ty0, crown_z1),
                  'stone_light', owner, role='structure')
            b.box(f'gatehouse.{side}_tower_crown.rear',
                  (tx0, ty1, crown_z0, tx1, ty1 + .18, crown_z1),
                  'stone_light', owner, role='structure')
            b.box(f'gatehouse.{side}_tower_crown.west',
                  (tx0 - .18, ty0, crown_z0, tx0, ty1, crown_z1),
                  'stone_light', owner, role='structure')
            b.box(f'gatehouse.{side}_tower_crown.east',
                  (tx1, ty0, crown_z0, tx1 + .18, ty1, crown_z1),
                  'stone_light', owner, role='structure')

    # A defended upper gallery is split on each side so the passage remains
    # open below. Its staircase is placed inside each tower, clear of traffic.
    upper = base + height + .12
    for side, x0, x1, owner in (('west', .16, tower_width - .16, left),
                                ('east', tower_width + core_width + .16,
                                 total_width - .16, right)):
        tower_y0, tower_y1 = owner.bounds[1], owner.bounds[3]
        stair_x = (tower_width * .5 if side == 'west' else
                   tower_width + core_width + tower_width * .5)
        stair_y0, stair_y1 = tower_y0 + .52, tower_y1 - 1.32
        floor_material = 'stone' if region in ('THORNFELL', 'EMBERHOLT') else 'timber'
        # Split the guard floor around the actual stairwell, then bridge the
        # head with a landing at the upper end of the flight.
        void_half = .68
        if x0 < stair_x - void_half:
            b.deck(f'gatehouse.{side}_guard_floor.left',
                   [(x0, tower_y0 + .30), (stair_x - void_half, tower_y0 + .30),
                    (stair_x - void_half, tower_y1 - .30), (x0, tower_y1 - .30)],
                   z=upper, material=floor_material, zone=owner)
        if stair_x + void_half < x1:
            b.deck(f'gatehouse.{side}_guard_floor.right',
                   [(stair_x + void_half, tower_y0 + .30), (x1, tower_y0 + .30),
                    (x1, tower_y1 - .30), (stair_x + void_half, tower_y1 - .30)],
                   z=upper, material=floor_material, zone=owner)
        b.deck(f'gatehouse.{side}_guard_landing',
               [(stair_x - void_half, stair_y1),
                (stair_x + void_half, stair_y1),
                (stair_x + void_half, tower_y1 - .30),
                (stair_x - void_half, tower_y1 - .30)],
               z=upper, material=floor_material, zone=owner)
        _stair_to_guard_floor(b, f'gatehouse.{side}_guard_stair', stair_x,
                              stair_y0, stair_y1, base, upper,
                              owner,
                              'iron' if region == 'EMBERHOLT' else 'timber')
        # Waist-high merlons protect a standing watch without enclosing the
        # entire platform or inventing a specialized weapon emplacement.
        b.box(f'gatehouse.{side}_parapet.front',
              (x0, tower_y0 + .28, upper, x1, tower_y0 + .48, upper + .95),
              'stone_light' if region in ('THORNFELL', 'EMBERHOLT') else 'timber',
              owner, role='defense')
        wealth = str(getattr(b.settings, 'wealth', 'ESTABLISHED')).upper()
        watch_capacity = {'MODEST': 3, 'ESTABLISHED': 4, 'AFFLUENT': 5}.get(wealth, 4)
        for bay in range(watch_capacity):
            bx = x0 + (x1 - x0) * (bay + .5) / watch_capacity
            b.box(f'gatehouse.{side}_merlon.{bay}',
                  (bx - .20, tower_y0 + .25, upper + .72,
                   bx + .20, tower_y0 + .57, upper + 1.28),
                  'stone_light' if region in ('THORNFELL', 'EMBERHOLT') else 'timber',
                  owner, role='defense')
    # Only the stair clearances are registered as routes; the guarded rooms
    # contain stairs, furniture and defensive fixtures, so they are not empty.

    # Distinct approaches communicate place through construction: Mire banks
    # rise on piles, Emberholt presents a heavy stone portal, and the Marches
    # favor a compact stone forecourt at a guarded ridge pass.
    ramp_run = max(3.0, base * 7.0)
    b.ramp('gatehouse.front_threshold_ramp',
           (core_x + core_width * .5, -ramp_run),
           (core_x + core_width * .5, 0.0), 2.2, base, zone=zone)
    b.ramp('gatehouse.rear_threshold_ramp',
           (core_x + core_width * .5, depth + ramp_run),
           (core_x + core_width * .5, depth), 2.2, base, zone=zone)
    if region == 'MIRE':
        b.deck('gatehouse.mire_landing',
               [(core_x, 0.0), (core_x + core_width, 0.0),
                (core_x + core_width, .55), (core_x, .55)],
               z=base, material='timber', zone=zone)
    elif region == 'THORNFELL':
        b.deck('gatehouse.ridge_approach',
               [(core_x - .8, -.9), (core_x + core_width + .8, -.9),
                (core_x + core_width + .8, 0.0), (core_x - .8, 0.0)],
               z=base, material='stone', zone=zone)
    else:
        b.deck('gatehouse.forecourt',
               [(core_x - 1.0, -1.0), (core_x + core_width + 1.0, -1.0),
                (core_x + core_width + 1.0, 0.0), (core_x - 1.0, 0.0)],
               z=base, material='stone', zone=zone)
    if region == 'MIRE':
        # The shifted east watchbank opens onto a stilted timber walk that
        # skirts the portal and descends back to the banks at both ends.
        bridge_x0, bridge_x1 = total_width + .15, total_width + 2.35
        bridge_y0, bridge_y1 = right.bounds[1] - .20, right.bounds[3] + .20
        bridge_center = (bridge_x0 + bridge_x1) * .5
        access_y = (right.bounds[1] + right.bounds[3]) * .5
        b.deck('gatehouse.mire_watchbank_bridge',
               [(bridge_x0, bridge_y0), (bridge_x1, bridge_y0),
                (bridge_x1, bridge_y1), (bridge_x0, bridge_y1)],
               z=base, material='timber', zone=right)
        b.ctx.rail('gatehouse.mire_bridge_rail.inner',
                   (bridge_x0 + .10, bridge_y0),
                   (bridge_x0 + .10, access_y - .65), base,
                   material='timber', zone=right)
        b.ctx.rail('gatehouse.mire_bridge_rail.inner.rear',
                   (bridge_x0 + .10, access_y + .65),
                   (bridge_x0 + .10, bridge_y1), base,
                   material='timber', zone=right)
        b.ctx.rail('gatehouse.mire_bridge_rail.outer',
                   (bridge_x1 - .10, bridge_y0), (bridge_x1 - .10, bridge_y1),
                   base, material='timber', zone=right)
        bridge_run = max(3.0, base * 7.0)
        b.ramp('gatehouse.mire_watchbank_front_ramp',
               (bridge_center, bridge_y0 - bridge_run),
               (bridge_center, bridge_y0), 2.0, base, zone=right)
        b.ramp('gatehouse.mire_watchbank_rear_ramp',
               (bridge_center, bridge_y1 + bridge_run),
               (bridge_center, bridge_y1), 2.0, base, zone=right)
        b.route('gatehouse.mire_watchbank_bridge_route',
                (bridge_center - .50, bridge_y0, base + .05,
                 bridge_center + .50, bridge_y1, base + 2.15), kind='human')
        b.route('gatehouse.mire_watchbank_door_route',
                (total_width - .50, access_y - .50, base + .05,
                 bridge_x0 + .50, access_y + .50, base + 2.15), kind='human')
        b.deck('gatehouse.mire_watchbank_door_landing',
               [(total_width - .02, access_y - .70),
                (bridge_x0 + .02, access_y - .70),
                (bridge_x0 + .02, access_y + .70),
                (total_width - .02, access_y + .70)],
               z=base, material='timber', zone=right)
    return b.finish()
