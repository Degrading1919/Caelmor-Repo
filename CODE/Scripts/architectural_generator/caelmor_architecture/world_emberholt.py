"""Parametric Emberholt massing grammar.

This is a reversible art-direction interpretation: substantial angular stone
volumes, terraces, vents, and iron service walks. It creates original geometry
from the shared construction context and never assembles preset meshes.
"""


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


def _buttresses(ctx, mass, detail, count_limit=4):
    """Put battered stone ribs on solid side-wall stations, clear of openings."""
    spacing = 3.1 if detail == "HIGH" else 4.4
    for edge in (1, 3):
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


def build(ctx):
    """Build an angular Emberholt structure from the shared geometry context."""
    s = ctx.settings
    function = _tag(_value(s, "function", "COTTAGE"))
    context = _tag(_value(s, "context", "EMBERHOLD"))
    wealth = _tag(_value(s, "wealth", "ESTABLISHED"))
    detail = _tag(_value(s, "detail", "MEDIUM"))
    age = float(_value(s, "age", 35.0))
    floor_h = max(2.8, min(3.35, float(_value(s, "floor_height", 3.0))))

    industrial = function in {"SMITHY", "WORKSHOP"} or (
        context == "EMBERFORGES" and function not in
        {"GATEHOUSE","WATCHTOWER","BARRACKS","ASSEMBLY_HALL"})
    civic = function in {"ASSEMBLY_HALL", "GATEHOUSE", "WATCHTOWER", "BARRACKS"}
    defensive = function in {"GATEHOUSE", "WATCHTOWER", "BARRACKS"} or context == "EMBERGATE"
    affluent = wealth == "AFFLUENT" or context == "ASHSPIRE"
    # The gatehouse's authored through-passage uses the north/south openings;
    # an east-side court would introduce an unrelated entrance.
    entry_court = (affluent or civic or industrial) and function != "GATEHOUSE"

    # Even dwellings occupy a deep, stone city bay. Wealth adds useful volume
    # and a court-like approach before it adds a signal tower.
    width = max(12.0, float(_value(s, "width", 10.5)))
    depth = max(10.0, float(_value(s, "depth", 8.0)))
    floors = max(2, min(3, int(_value(s, "floors", 2))))
    if wealth == "MODEST":
        width, depth, floors = min(width, 13.2), max(depth, 10.8), 2
    elif wealth == "ESTABLISHED":
        width, depth, floors = min(max(width, 15.0), 16.4), max(depth, 11.5), 2
    else:
        width, depth, floors = min(max(width, 16.5), 18.0), max(depth, 12.6), 3

    if context == "CINDERWEAVE":
        width = min(16.0, max(width, 15.0))
        depth = max(depth, 12.0)
    elif context == "EMBERFORGES":
        width, depth, floors = min(18.0, max(width, 16.0)), max(depth, 13.0), 2
    elif context == "ASHSPIRE":
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
    tower_needed = affluent or civic or defensive or industrial
    link_needed = tower_needed and function not in {"WATCHTOWER", "GATEHOUSE"}
    primary = _mass(
        ctx, "emberholt_main_block", x=0, y=0, width=width, depth=depth,
        floors=floors, floor_height=floor_h, roof="TERRACE", pitch=0.0,
        overhang=.08, entrance_edge=0 if function == "GATEHOUSE" else (1 if floors > 1 else 0),
        blocked_edges=(2,) if industrial else (),
        steps=not entry_court,
        function=function, gallery_edges=(1,) if link_needed else (),
        foundation="PLINTH",
    )

    _buttresses(ctx, primary, detail, count_limit=2 if detail == "LOW" else 4)

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
    if industrial or context in {"EMBERFORGES", "EMBERHOLD", "CINDERWEAVE",
                                 "ASHSPIRE", "EMBERGATE"} or affluent:
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
