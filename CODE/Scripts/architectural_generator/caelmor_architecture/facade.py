"""Grounded exterior facade construction for Caelmor's procedural buildings."""
from __future__ import annotations

import math
from .geometry import MeshBuffer, area, clip, inequalities, subtract_convex


# Millimetres are intentionally avoided: all dimensions follow the engine's metre scale.
WALL_THICKNESS = 0.30
FOUNDATION_HEIGHT = 0.45  # legacy-plan fallback; built plans use plan.foundation_height


def _foundation(plan):
    return float(getattr(plan, "foundation_height", FOUNDATION_HEIGHT))


def _type_features(plan):
    spec = getattr(plan, "type_spec", None)
    return set(getattr(spec, "features", ()) or ())


def _is_type(plan, *names):
    fn = str(plan.settings.function).upper()
    return fn in names or bool(_type_features(plan).intersection(names))


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    return (dx / length, dy / length), length


def _xy_wall(a, b, normal, start, end, inset=0.0, thickness=WALL_THICKNESS):
    """A thin wall footprint between edge parameters; inset is measured inward."""
    tx, ty = _unit(a, b)[0]
    ox, oy = normal
    p0 = (a[0] + tx * start - ox * inset, a[1] + ty * start - oy * inset)
    p1 = (a[0] + tx * end - ox * inset, a[1] + ty * end - oy * inset)
    q1 = (p1[0] - ox * thickness, p1[1] - oy * thickness)
    q0 = (p0[0] - ox * thickness, p0[1] - oy * thickness)
    poly = [p0, p1, q1, q0]
    if area(poly) < 0:
        poly.reverse()
    return poly


def _wall_solid(buf, a, b, normal, s0, s1, z0, z1, inset=0.0, thickness=WALL_THICKNESS):
    if s1 - s0 > 1e-4 and z1 - z0 > 1e-4:
        buf.prism(_xy_wall(a, b, normal, s0, s1, inset,thickness), z0, z1)


def _stone_relief(poly_a, poly_b, normal, s0, s1):
    """Shallow outer-face stone veneer, distinct from the continuous plinth core."""
    tx, ty = _unit(poly_a, poly_b)[0]
    ox, oy = normal
    p0 = (poly_a[0] + tx*s0 + ox*0.035, poly_a[1] + ty*s0 + oy*0.035)
    p1 = (poly_a[0] + tx*s1 + ox*0.035, poly_a[1] + ty*s1 + oy*0.035)
    q1 = (p1[0] - ox*0.105, p1[1] - oy*0.105)
    q0 = (p0[0] - ox*0.105, p0[1] - oy*0.105)
    poly = [p0, p1, q1, q0]
    return list(reversed(poly)) if area(poly) < 0 else poly


def _edge_frame(plan, edge_index, edge):
    a, b = edge
    (tx, ty), length = _unit(a, b)
    # Outward normal is the contract's (dy,-dx) for CCW footprints.
    return a, b, tx, ty, (ty, -tx), length


def _openings_for_edge(plan, edge_index, edge):
    """Return deterministic, function-aware exterior openings in edge metres."""
    if edge_index in getattr(plan,'blocked_edges',()) or edge_index in getattr(plan,'open_edges',()) or getattr(plan,'opening_style','')=='NONE':
        return []
    s = plan.settings
    a, b, tx, ty, normal, length = _edge_frame(plan, edge_index, edge)
    fn = str(s.function).upper()
    openings = []
    rng = plan.rng(f"facade.openings.edge.{edge_index}")
    margin = 0.58
    usable = max(0.0, length - 2 * margin)

    # One recognizable entrance per building, located on the longest suitable wall.
    edges = list(plan.edges)
    # Prefer the south-facing frontage (including a U's courtyard) so a street-side
    # entrance follows the massing instead of landing on the longest rear wall.
    front = [i for i,(p,q) in enumerate(edges) if q[0]-p[0]>2.7 and abs(q[1]-p[1])<1e-7]
    candidates = front or list(range(len(edges)))
    entrance_edge = max(candidates, key=lambda i: math.dist(*edges[i])) if candidates else -1
    passage_edge = -1
    if fn=="GATEHOUSE" and plan.rects:
        # The passage runs from the south edge of the central block through to
        # its north edge, centered on the same world-space axis. U wings flank
        # this route; their short front walls are never mistaken for the entry.
        x0,y0,x1,y1,_axis=plan.rects[0]
        cx=(x0+x1)*.5
        entrances=[i for i,(p,q) in enumerate(edges)
                   if abs(p[1]-y0)<1e-7 and abs(q[1]-y0)<1e-7
                   and min(p[0],q[0])<=cx<=max(p[0],q[0])]
        exits=[i for i,(p,q) in enumerate(edges)
               if abs(p[1]-y1)<1e-7 and abs(q[1]-y1)<1e-7
               and min(p[0],q[0])<=cx<=max(p[0],q[0])]
        if entrances:
            entrance_edge=entrances[0]
        if exits:
            passage_edge=exits[0]
    elif fn in ("GATEHOUSE", "WAREHOUSE") and front:
        yfront=min((p[1]+q[1])*.5 for p,q in (edges[i] for i in front))
        parallel=[i for i,(p,q) in enumerate(edges)
                  if abs(q[0]-p[0])>2.7 and abs(q[1]-p[1])<1e-7 and (p[1]+q[1])*.5>yfront+1.0]
        if parallel:
            passage_edge=max(parallel,key=lambda i:math.dist(*edges[i]))
    entrance_edge=getattr(plan,'entrance_edge_override',entrance_edge)
    fh = _foundation(plan)
    if (edge_index == entrance_edge or edge_index in getattr(plan,'secondary_entrance_edges',())) and length > 2.7:
        door_w = {"BARN":2.55,"GRAIN_STORE":1.45,"INN":1.18,"SHOP":1.35,
                  "WAREHOUSE":2.35,"STABLE":2.35,"SMITHY":1.55,"WORKSHOP":1.45,
                  "ASSEMBLY_HALL":1.8,"GATEHOUSE":2.8,"BOATHOUSE":3.1}.get(fn,1.05)
        if fn in ("WAREHOUSE", "STABLE", "BOATHOUSE"):
            door_w = min(door_w, length - 0.9)
        center = length * (0.46 if fn in ("FARMHOUSE", "MILLER") and edge_index==entrance_edge else 0.50)
        door_head = {"BARN":2.78,"INN":2.68,"WAREHOUSE":3.0,"STABLE":2.7,
                     "GATEHOUSE":3.35,"BOATHOUSE":3.05}.get(fn,2.58)
        if fn=="STABLE":
            stall_width=min(1.12,(length-1.5)*.5)
            for role,stall_center in (("stall_left",length*.38),("stall_right",length*.62)):
                openings.append({"kind":"door","role":role,
                                 "s0":stall_center-stall_width/2,"s1":stall_center+stall_width/2,
                                 "z0":fh-.02,"z1":fh+door_head})
        else:
            openings.append({"kind":"door", "role":"passage_entry" if fn=="GATEHOUSE" and edge_index==entrance_edge else None,
                             "s0":center-door_w/2, "s1":center+door_w/2, "z0":fh-0.02, "z1":fh+door_head})
        if "guard_gallery" in _type_features(plan) and int(s.floors)>1 and not getattr(plan,'suppress_function_details',False):
            deck_z=fh+(int(s.floors)-1)*float(s.floor_height)+.08
            upper_plate=float(plan.eave)-(.24+.145*float(plan.slope))
            access_width=min(1.10,length-.70)
            access_z1=min(deck_z+2.05,upper_plate-.25)
            if access_width>=.90 and access_z1-deck_z>=1.90:
                openings.append({"kind":"door","role":"gallery_access",
                    "s0":length*.5-access_width*.5,"s1":length*.5+access_width*.5,
                    "z0":deck_z,"z1":access_z1})
    elif edge_index == passage_edge and length > 2.7:
        door_w=2.8 if fn=="GATEHOUSE" else 2.35
        center=length*.5
        door_head=3.35 if fn=="GATEHOUSE" else 3.0
        openings.append({"kind":"door", "role":"passage_exit" if fn=="GATEHOUSE" else "loading",
                         "s0":center-door_w/2,"s1":center+door_w/2,
                         "z0":fh-.02,"z1":fh+door_head})

    if usable < 1.0:
        return openings
    # Purpose shapes the rhythm: barns and grain stores use broad high vents; homes use
    # smaller domestic windows; inns favour a more regular public frontage.
    if fn in ("BARN", "GRAIN_STORE") or _type_features(plan).intersection({"loft_vents","vent_slots","hayloft","clerestory_vents","vented_ridge","high_vents"}):
        nominal, ww, wh = (3.25, 0.72, 0.55) if fn == "BARN" else (3.7, 0.64, 0.48)
        count = max(0, min(4, int((usable + 0.4) // nominal)))
        for k in range(count):
            center = margin + usable * (k + 1) / (count + 1)
            openings.append({"kind":"vent", "s0":center-ww/2, "s1":center+ww/2,
                             "z0":fh+float(s.floor_height)-1.02 + rng.uniform(-0.08, 0.10),
                             "z1":fh+float(s.floor_height)-1.02 + wh + rng.uniform(-0.04, 0.05)})
    else:
        nominal = 2.65 if fn in ("INN", "SHOP", "MERCHANT_HOUSE","MARKET_HALL") else (2.85 if fn == "MILLER" else 3.1)
        count = max(0, min(5, int((usable + 0.2) // nominal)))
        if s.floors > 1:
            for level in range(min(int(s.floors), 3)):
                # Ground floor avoids the entry; upper windows repeat at the floor plate.
                plate_z = fh + level * float(s.floor_height)
                next_plate = fh + (level + 1) * float(s.floor_height)
                # Complete casing and open shutters fit in the clear storey band.
                # Leave 100mm below the plate and 160mm below the next plate/roof
                # structure before placing the full assembly, not just the glass.
                band_low = plate_z + (0.40 if level else 0.36)
                band_high = min(next_plate - 0.25, float(plan.eave) - (0.44 + .145*float(plan.slope)))
                zbase = band_low
                zh = min(1.17 if level == 0 else 1.12, band_high - zbase - .22)
                if zh < .64:
                    continue
                for k in range(count):
                    center = margin + usable * (k + 1) / (count + 1)
                    if level == 0 and any(o["kind"] == "door" and abs((o["s0"] + o["s1"])/2-center) < 1.0 for o in openings):
                        continue
                    jitter = rng.uniform(-0.06, 0.06)
                    f=_type_features(plan)
                    w = (0.62 if "narrow_windows" in f else
                         (1.48 if f.intersection({"display_front","long_windows"}) and level==0 else
                         (1.05 if fn == "INN" else 0.9))) * float(s.window_density)
                    openings.append({"kind":"window", "s0":center-w/2+jitter, "s1":center+w/2+jitter,
                                     "z0":zbase, "z1":zbase+zh})
        else:
            for k in range(count):
                center = margin + usable * (k + 1) / (count + 1)
                if any(o["kind"] == "door" and abs((o["s0"]+o["s1"])/2-center) < 0.85 for o in openings):
                    continue
                f=_type_features(plan)
                w = (0.62 if "narrow_windows" in f else
                     (1.5 if f.intersection({"display_front","long_bench_windows","long_windows"}) else
                     (1.08 if fn == "INN" else 0.92))) * float(s.window_density)
                jitter = rng.uniform(-0.08, 0.08)
                z0=fh+.43
                z1=min(z0+(1.20 if fn == "INN" else 1.12), float(plan.eave)-(.46+.145*float(plan.slope)))
                if z1-z0 >= .64:
                    openings.append({"kind":"window", "s0":center-w/2+jitter, "s1":center+w/2+jitter,
                                     "z0":z0, "z1":z1})

    policy=getattr(plan,'opening_style','DOMESTIC')
    if policy in ('EMBER','EMBER_HOME') and int(s.floors)>1 and edge_index in getattr(plan,'gallery_edges',()):
        deck_z=fh+float(s.floor_height)+.08
        openings.append({'kind':'door','role':'gallery_access','s0':length*.5-.58,
                         's1':length*.5+.58,'z0':deck_z,'z1':deck_z+2.12})
    # Construction-specific apertures are dimensioned before the full casing
    # exclusion schedule is built. Material changes never stand in for this.
    for o in openings:
        if o['kind']=='window' and policy=='EMBER_HOME':
            center=(o['s0']+o['s1'])*.5
            cap={'MODEST':.60,'ESTABLISHED':.88,'AFFLUENT':1.02}[s.wealth]
            height={'MODEST':.72,'ESTABLISHED':.91,'AFFLUENT':1.04}[s.wealth]
            # A shop invests in light for its work/display floor; the rooms
            # above retain enclosed domestic proportions and deep reveals.
            if fn=='SHOP' and o['z0']<fh+s.floor_height:
                cap,height=1.45,1.12
            width=min(o['s1']-o['s0'],cap)
            o['s0'],o['s1']=center-width*.5,center+width*.5
            o['z1']=min(o['z1'],o['z0']+height)
        if o['kind']=='window' and policy in ('NARROW','EMBER'):
            center=(o['s0']+o['s1'])*.5
            width=min(o['s1']-o['s0'],.52 if policy=='NARROW' else .64)
            o['s0'],o['s1']=center-width*.5,center+width*.5
            if policy=='EMBER':
                o['z1']=min(o['z0']+1.48,plan.eave-.6)
    # Clamp records to the wall and reject degenerate windows for narrow wings.
    clean = []
    for o in openings:
        o["s0"] = max(0.32, o["s0"])
        o["s1"] = min(length-0.32, o["s1"])
        # A tall door header also projects outside the wall. Its full section
        # must fit below a steep, low eave, not just below the wall datum.
        upper_plate=float(plan.eave)-(.24+.145*float(plan.slope))
        if o.get("role")=="gallery_access":
            head_limit=upper_plate-.25
        elif o["kind"]=="door":
            head_limit=min(plan.eave-(.12+.14*plan.slope+.15+.003),
                           fh+float(s.floor_height)-.27,upper_plate-.25)
        else:
            head_limit=min(plan.eave-(.46+.145*float(plan.slope)),upper_plate-.12)
        o["z1"] = min(o["z1"], head_limit)
        if o["kind"] == "window":
            # Casing, sill, lintel, and both open shutters are all represented in
            # this conservative exterior footprint. Structural schedules use it.
            shutter = min(.18, (o["s1"]-o["s0"])*.21)
            o["assembly_bounds"] = {"s0":o["s0"]-shutter*.92, "s1":o["s1"]+shutter*.92,
                                     "z0":o["z0"]-.10, "z1":o["z1"]+.09}
            o["assembly_members"]=["casing","sill","lintel","shutters","glass"]
        elif o["kind"] == "vent":
            o["assembly_bounds"]={"s0":o["s0"]-.08,"s1":o["s1"]+.08,
                                   "z0":o["z0"]-.07,"z1":o["z1"]+.12}
            o["assembly_members"]=["jambs","lintel","louvres"]
        else:
            o["assembly_bounds"] = {"s0":o["s0"]-.09,"s1":o["s1"]+.09,
                                     "z0":o["z0"]-.08,"z1":o["z1"]+.15}
            o["assembly_members"]=( ["jambs","lintel","open_passage"]
                                     if o.get("role") in ("passage_entry","passage_exit")
                                     else ["jambs","lintel","leaf","threshold"] )
        if o["s1"] - o["s0"] >= 0.38 and o["z1"] - o["z0"] >= 0.35:
            clean.append(o)
    # Resolve accidental overlaps in deterministic order, keeping a margin between cuts.
    # Keep the functional entrance before display/vent openings. Otherwise a
    # centered shop door can be erased by two broad neighbouring windows.
    clean.sort(key=lambda o: (o["kind"]!="door", o["s0"], o["z0"]))
    out = []
    for o in clean:
        bounds=o["assembly_bounds"]
        def overlaps(q):
            other=q["assembly_bounds"]
            return not (bounds["s1"] <= other["s0"]+.08 or bounds["s0"] >= other["s1"]-.08 or
                        bounds["z1"] <= other["z0"]+.08 or bounds["z0"] >= other["z1"]-.08)
        if any(overlaps(q) for q in out):
            continue
        out.append(o)
    return out


def _wall_panels(buf, a, b, normal, length, openings, top, bottom=FOUNDATION_HEIGHT, thickness=WALL_THICKNESS):
    """Tessellate the wall around apertures; no wall surface crosses an opening."""
    xs = {0.0, length}
    zs = {bottom, top}
    for o in openings:
        xs.update((o["s0"], o["s1"]))
        if o["z0"] > bottom:
            zs.add(min(top, o["z0"]))
        zs.add(min(top, o["z1"]))
    xs, zs = sorted(xs), sorted(zs)
    for s0, s1 in zip(xs, xs[1:]):
        if s1-s0 < 0.015:
            continue
        sm = (s0+s1)/2
        for z0, z1 in zip(zs, zs[1:]):
            if z1-z0 < 0.015:
                continue
            zm = (z0+z1)/2
            inside = any(o["s0"]+1e-5 < sm < o["s1"]-1e-5 and o["z0"]+1e-5 < zm < o["z1"]-1e-5 for o in openings)
            if not inside:
                _wall_solid(buf, a, b, normal, s0, s1, z0, z1,thickness=thickness)


def _beam_edge(buf, a, b, s0, s1, z, thickness, depth, material=None, normal=None, normal_offset=0.0, chamfer=0.0):
    tx, ty = _unit(a,b)[0]
    nx,ny=normal or (0.0,0.0)
    p = (a[0]+tx*s0+nx*normal_offset, a[1]+ty*s0+ny*normal_offset, z)
    q = (a[0]+tx*s1+nx*normal_offset, a[1]+ty*s1+ny*normal_offset, z)
    # MeshBuffer.beam uses its width axis normal to a horizontal wall edge and its
    # depth axis vertical. Swap the intuitive (height, wall-depth) arguments here.
    _frame_beam(buf,p,q,depth,thickness,chamfer)


def _frame_beam(buf, a, b, width, depth, chamfer=0.0):
    """Use the engine's bevelled beam primitive when available at the requested tier."""
    beveled = getattr(buf, "chamfered_beam", None)
    if chamfer > 0 and callable(beveled):
        beveled(a, b, width, depth, chamfer=chamfer)
    else:
        buf.beam(a, b, width, depth)


def _xy_opening_slab(a,b,normal,s0,s1,outward,depth):
    """Shallow wall-parallel solid measured from the exterior wall plane."""
    tx,ty=_unit(a,b)[0]
    ox,oy=normal
    p0=(a[0]+tx*s0+ox*outward,a[1]+ty*s0+oy*outward)
    p1=(a[0]+tx*s1+ox*outward,a[1]+ty*s1+oy*outward)
    q1=(p1[0]-ox*depth,p1[1]-oy*depth)
    q0=(p0[0]-ox*depth,p0[1]-oy*depth)
    poly=[p0,p1,q1,q0]
    return list(reversed(poly)) if area(poly)<0 else poly


def _step_prism(buf,a,b,n,s0,s1,depth,z0,z1):
    tx,ty=_unit(a,b)[0]
    ox,oy=n
    p0=(a[0]+tx*s0,a[1]+ty*s0)
    p1=(a[0]+tx*s1,a[1]+ty*s1)
    poly=[p0,p1,(p1[0]+ox*depth,p1[1]+oy*depth),(p0[0]+ox*depth,p0[1]+oy*depth)]
    if area(poly)<0: poly.reverse()
    buf.prism(poly,z0,z1)


def _post(buf, a, b, s, z0, z1, face_width=0.16, depth=0.20, chamfer=0.0):
    tx, ty = _unit(a,b)[0]
    # beam vertical; width/depth are the two horizontal cross-section dimensions.
    x, y = a[0]+tx*s, a[1]+ty*s
    _frame_beam(buf,(x,y,z0),(x,y,z1),face_width,depth,chamfer)


def _segment_hits_opening(brace, opening, clearance):
    """Conservative segment-vs-expanded-opening test in wall (s,z) space."""
    x0, z0, x1, z1 = brace["s0"], brace["z0"], brace["s1"], brace["z1"]
    left, right = opening["s0"] - clearance, opening["s1"] + clearance
    low, high = opening["z0"] - clearance, opening["z1"] + clearance
    # Clip the full centerline against the opening rectangle. Expanding by the
    # brace half-width guarantees that neither its centerline nor its solid body
    # can cross the aperture.
    t0, t1 = 0.0, 1.0
    for p, q, lo, hi in ((x0, x1-x0, left, right), (z0, z1-z0, low, high)):
        if abs(q) < 1e-10:
            if p < lo or p > hi:
                return False
            continue
        a, b = (lo-p)/q, (hi-p)/q
        if a > b:
            a, b = b, a
        t0, t1 = max(t0, a), min(t1, b)
        if t0 > t1:
            return False
    return True


def _gable_profile(plan, edge):
    """Return a compact set of true roof-envelope stations along an exterior edge."""
    a, b = edge
    (tx, ty), length = _unit(a, b)

    def height_at(s):
        h = float(plan.roof_height(a[0] + tx*s, a[1] + ty*s))
        return max(float(plan.eave), h) if math.isfinite(h) else float(plan.eave)

    cuts = {0.0, length}
    if hasattr(plan,'custom_roof_sources'):
        # Exact piecewise roof stations prevent adaptive chords from missing
        # changes in a bow roof's shoulder or a lean-to's supporting slope.
        for patch in plan.custom_roof_sources:
            for p,q in zip(patch.poly,patch.poly[1:]+patch.poly[:1]):
                px,py=p[0]-a[0],p[1]-a[1]
                qx,qy=q[0]-a[0],q[1]-a[1]
                np,nq=px*(-ty)+py*tx,qx*(-ty)+qy*tx
                if abs(np)<1e-7:
                    station=px*tx+py*ty
                    if 0<station<length:cuts.add(station)
                if np*nq<0:
                    t=np/(np-nq)
                    station=(px+t*(qx-px))*tx+(py+t*(qy-py))*ty
                    if 0<station<length:cuts.add(station)
        return [(s,height_at(s)) for s in sorted(cuts)]
    def refine(s0, s1, h0, h1, depth=0):
        sm = (s0+s1)*.5
        hm = height_at(sm)
        if depth < 9 and abs(hm-max(float(plan.eave), (h0+h1)*.5)) > .012:
            cuts.add(sm)
            refine(s0, sm, h0, hm, depth+1)
            refine(sm, s1, hm, h1, depth+1)
    refine(0.0, length, height_at(0.0), height_at(length))
    return [(s, height_at(s)) for s in sorted(cuts)]


def _skin_polygon(buffer, edge, polygon_sz, outward, thickness, efficient=False):
    """Emit a clipped s/z face as a closed veneer or explicit SURFACE detail."""
    if len(polygon_sz)<3 or abs(area(polygon_sz))<.012:
        return
    if area(polygon_sz)<0:
        polygon_sz=list(reversed(polygon_sz))
    a,b=edge
    (tx,ty),_length=_unit(a,b)
    n=(ty,-tx)
    xyz=[(a[0]+tx*s+n[0]*outward,a[1]+ty*s+n[1]*outward,z)
         for s,z in polygon_sz]
    if efficient:
        # EFFICIENT keeps the visible front and every exposed edge reveal so
        # staggered joints retain real depth. Only the concealed back cap goes.
        veneer=MeshBuffer("skin_piece",buffer.material,buffer.layer)
        veneer.extrude(xyz,(-n[0]*thickness,-n[1]*thickness,0.0))
        buffer.indexed(veneer.vertices,[veneer.faces[0],*veneer.faces[2:]])
    else:
        buffer.extrude(xyz,(-n[0]*thickness,-n[1]*thickness,0.0))


def _cladding_tiles(plan, edge_index, edge, openings, construction, buffer):
    """Generate bounded regional wall relief, cut around complete openings."""
    a,b,tx,ty,n,length=_edge_frame(plan,edge_index,edge)
    profile=_gable_profile(plan,edge)
    roof_max=max(z for _s,z in profile)-.12
    bottom=_foundation(plan)
    if roof_max<=bottom+.08:
        return
    detail=str(getattr(plan.settings,"detail","HIGH")).upper()
    efficient=str(getattr(plan.settings,"geometry_mode","SOLID")).upper()=="EFFICIENT"
    # Low-detail faces remain broad and let the material normal carry fine grain.
    if construction=="RUBBLE":
        rng=plan.rng(f"facade.cladding.rubble.edge.{edge_index}")
        base_h=.54 if detail=="LOW" else (.38 if detail=="MEDIUM" else .30)
        base_w=1.25 if detail=="LOW" else (.98 if detail=="MEDIUM" else .78)
        z=bottom
        row=0
        while z<roof_max:
            h=min(roof_max-z,base_h*rng.uniform(.88,1.12))
            stagger=(row%2)*base_w*.42
            s=-stagger
            while s<length:
                span=base_w*rng.uniform(.72,1.32)
                lo,hi=max(0.0,s+.018),min(length,s+span-.018)
                if hi-lo>.16:
                    tile=[(lo,z+.008),(hi,z+.008),(hi,z+h-.008),(lo,z+h-.008)]
                    _emit_clipped_skin_tile(plan,edge_index,edge,profile,openings,buffer,
                                            tile,efficient)
                s+=span
            z+=h
            row+=1
    elif construction=="ASHLAR":
        rng=plan.rng(f"facade.cladding.ashlar.edge.{edge_index}")
        course_h=.52 if detail=="LOW" else (.42 if detail=="MEDIUM" else .36)
        bay_w=1.55 if detail=="LOW" else (1.30 if detail=="MEDIUM" else 1.14)
        z=bottom
        row=0
        while z<roof_max:
            h=min(course_h,roof_max-z)
            stagger=(row%2)*bay_w*.5
            s=-stagger
            while s<length:
                span=bay_w*rng.uniform(.94,1.06)
                lo,hi=max(0.0,s+.022),min(length,s+span-.022)
                if hi-lo>.22:
                    tile=[(lo,z+.012),(hi,z+.012),(hi,z+h-.012),(lo,z+h-.012)]
                    _emit_clipped_skin_tile(plan,edge_index,edge,profile,openings,buffer,
                                            tile,efficient)
                s+=span
            z+=h
            row+=1
    elif construction=="BOARD":
        rng=plan.rng(f"facade.cladding.board.edge.{edge_index}")
        board_w=.42 if detail=="LOW" else (.27 if detail=="MEDIUM" else .21)
        gap=.022 if detail!="LOW" else .03
        s=-.5*board_w
        while s<length:
            width=board_w*rng.uniform(.97,1.03)
            lo,hi=max(0.0,s+gap*.5),min(length,s+width-gap*.5)
            if hi-lo>.07:
                tile=[(lo,bottom),(hi,bottom),(hi,roof_max),(lo,roof_max)]
                _emit_clipped_skin_tile(plan,edge_index,edge,profile,openings,buffer,
                                        tile,efficient)
            # Narrow battens cover board joints and remain subject to the same
            # roof and full-assembly cutters as the siding beneath them.
            batten=.035 if detail=="HIGH" else (.028 if detail=="MEDIUM" else .0)
            if batten and lo>0:
                blo,bhi=max(0.0,s-batten*.5),min(length,s+batten*.5)
                if bhi-blo>.02:
                    tile=[(blo,bottom),(bhi,bottom),(bhi,roof_max),(blo,roof_max)]
                    _emit_clipped_skin_tile(plan,edge_index,edge,profile,openings,buffer,
                                            tile,efficient,outward=.024,thickness=.012)
            s+=width


def _emit_clipped_skin_tile(plan,edge_index,edge,profile,openings,buffer,tile,efficient,
                            outward=.022,thickness=.018):
    """Clip a tile to one roof-profile segment and all assembly exclusion boxes."""
    for (rs0,rh0),(rs1,rh1) in zip(profile,profile[1:]):
        if rs1-rs0<1e-8:
            continue
        piece=clip(tile,1,0,-rs0)
        piece=clip(piece,-1,0,rs1)
        if not piece:
            continue
        slope=(rh1-rh0)/(rs1-rs0)
        roof_intercept=rh0-slope*rs0-.12
        piece=clip(piece,slope,-1,roof_intercept)
        if not piece:
            continue
        fragments=[piece]
        for opening in openings:
            bounds=opening.get("assembly_bounds",opening)
            cutter=[(bounds["s0"],bounds["z0"]),(bounds["s1"],bounds["z0"]),
                    (bounds["s1"],bounds["z1"]),(bounds["s0"],bounds["z1"])]
            planes=inequalities(cutter)
            next_fragments=[]
            for fragment in fragments:
                if (max(p[0] for p in fragment)<=bounds["s0"] or
                    min(p[0] for p in fragment)>=bounds["s1"] or
                    max(p[1] for p in fragment)<=bounds["z0"] or
                    min(p[1] for p in fragment)>=bounds["z1"]):
                    next_fragments.append(fragment)
                else:
                    next_fragments.extend(subtract_convex(fragment,planes))
            fragments=next_fragments
            if not fragments:
                break
        for fragment in fragments:
            _skin_polygon(buffer,edge,fragment,outward,thickness,efficient)


def frame_layout(plan, edge_index, edge):
    """Semantic, deterministic frame schedule for review and clearance checks.

    Distances are measured along the wall from its first endpoint. Brace endpoints
    are post/plate intersections in (s,z), and widths are the full visible face
    width used by the mesh builder.
    """
    a, b, tx, ty, normal, length = _edge_frame(plan, edge_index, edge)
    top = float(plan.eave)
    slope=float(plan.slope)
    structural_top=top-(.14+.145*slope)
    upper_plate=structural_top-.10
    rake_drop=.14+.5*.21*math.sqrt(1+slope*slope)+.5*.19*slope
    kingpost_drop=.14+.5*.19*slope
    openings = [dict(o) for o in _openings_for_edge(plan, edge_index, edge)]
    access_clearances=[{'s0':r['s0'],'s1':r['s1'],'z0':_foundation(plan),
                        'z1':_foundation(plan)+r.get('height',2.4)}
                       for r in getattr(plan,'functional_access',()) if r['edge_index']==edge_index]
    if not access_clearances and edge_index in getattr(plan,'open_edges',()) and edge_index==getattr(plan,'entrance_edge_override',0):
        # A roofed open working bay still has an approach. Reserve the center
        # stairs/handling route without inventing a door leaf or window hole.
        center=length*.5
        access_clearances=[{'s0':center-.90,'s1':center+.90,
                            'z0':_foundation(plan),'z1':_foundation(plan)+2.0}]
    constraints=openings+access_clearances
    fn = str(plan.settings.function).upper()
    spacing = 3.7 if fn in ("BARN", "GRAIN_STORE") else 4.1
    post_width = .22 if fn in ("BARN", "GRAIN_STORE") else .19
    # Principal posts span all storeys, so use the union of every aperture column
    # to keep their full width clear from the lower jamb through the upper floors.
    blocked=[]
    post_clearance=post_width*.5+.11
    for o in constraints:
        bounds=o.get("assembly_bounds",o)
        blocked.append((max(0.0,bounds["s0"]-post_clearance),
                        min(length,bounds["s1"]+post_clearance)))
    merged=[]
    for lo,hi in sorted(blocked):
        if merged and lo<=merged[-1][1]:
            merged[-1]=(merged[-1][0],max(merged[-1][1],hi))
        else:
            merged.append((lo,hi))

    def legal_principal(s):
        return all(s<=lo or s>=hi for lo,hi in merged)

    minimum_post_spacing=.66  # small rounding allowance above the .65m contract
    posts = [s for s in (.10,length-.10) if legal_principal(s)]
    candidate = spacing
    while candidate < length-0.35:
        # Grid stations remain stable across storeys; skip any station in the
        # merged aperture columns because opening casings provide local jambs.
        if (legal_principal(candidate) and
                all(abs(candidate-p)>=minimum_post_spacing for p in posts)):
            posts.append(candidate)
        candidate += spacing
    posts = sorted(set(round(p, 4) for p in posts))
    # Recover a blocked grid bay only where a legal, well-separated post can fit.
    # This caps long unsupported solid wall spans without placing posts against
    # aperture casings or crowding an adjacent principal member.
    max_bay=4.3
    while len(posts)>=2 and any(q-p>max_bay for p,q in zip(posts,posts[1:])):
        inserted=False
        for left,right in zip(posts,posts[1:]):
            if right-left<=max_bay:
                continue
            lo,hi=left+minimum_post_spacing,right-minimum_post_spacing
            regions=[]
            cursor=lo
            for blocked_lo,blocked_hi in merged:
                if blocked_hi<=cursor or blocked_lo>=hi:
                    continue
                if blocked_lo>cursor:
                    regions.append((cursor,min(blocked_lo,hi)))
                cursor=max(cursor,blocked_hi)
            if cursor<hi:
                regions.append((cursor,hi))
            # The .66m exclusion is already applied at both neighboring posts;
            # any remaining legal center interval can host one new station.
            regions=[(r[0]+.001,r[1]-.001) for r in regions
                     if r[1]-r[0]>=.002]
            if not regions:
                continue
            target=(left+right)*.5
            lo2,hi2=min(regions,key=lambda r: 0 if r[0]<=target<=r[1] else min(abs(target-r[0]),abs(target-r[1])))
            station=round(max(lo2,min(hi2,target)),4)
            if (legal_principal(station) and
                    min(abs(station-p) for p in posts)>=minimum_post_spacing):
                posts.append(station)
                posts.sort()
                inserted=True
                break
        if not inserted:
            break
    unsupported_spans=[{"s0":left,"s1":right,"length":right-left}
                       for left,right in zip(posts,posts[1:])
                       if right-left>max_bay+1e-6]
    jambs=[{"opening_index":i,"kind":o["kind"],"s0":o["s0"],"s1":o["s1"],
            "z0":o["z0"],"z1":o["z1"],"assembly_bounds":dict(o["assembly_bounds"]),
            "assembly_members":tuple(o["assembly_members"])} for i,o in enumerate(openings)]

    fh=_foundation(plan)
    plates = [fh+.025, upper_plate]
    plates.extend(fh+level*float(plan.settings.floor_height)
                  for level in range(1, int(plan.settings.floors)))
    plates = sorted(set(round(z, 4) for z in plates))

    braces = []
    upper_plate=plates[-1]
    # A restrained knee brace at each usable exterior corner post ties the post
    # shaft to the continuous top plate. The complete member section is checked
    # against every aperture before it enters the schedule.
    for end_index,post_s in enumerate((.10,length-.10)):
        if not legal_principal(post_s) or not any(abs(post_s-p)<1e-4 for p in posts):
            continue
        if len(posts)<2:
            continue
        neighbor=posts[1] if end_index==0 else posts[-2]
        bay_width=abs(neighbor-post_s)
        if bay_width<1.2:
            continue
        direction=1 if end_index==0 else -1
        inward_s=post_s+direction*.85
        if abs(inward_s-post_s)>.85+1e-8 or not (0<=inward_s<=length):
            continue
        brace={"s0":post_s,"z0":upper_plate-.85,
               "s1":inward_s,"z1":upper_plate,"width":.15,
               "support":"knee","post_s":post_s,"plate_z":upper_plate}
        if not any(_segment_hits_opening(brace,o.get("assembly_bounds",o),brace["width"]*.5+.035) for o in constraints):
            braces.append(brace)

    # Full-bay diagonals remain only at a credible pitch (35-65 degrees).
    # Their entire visible width must clear every opening.
    width = .19  # visible in-wall face width; beam's wall-normal depth is .14m
    for bay, (left, right) in enumerate(zip(posts, posts[1:])):
        if right-left < 1.05:
            continue
        for lower, upper in zip(plates, plates[1:]):
            if upper-lower < .72:
                continue
            # Restrict to a compact knee brace inside the bay. It joins the
            # lower post/plate joint to the adjacent post at the next plate.
            brace = {"s0": left, "s1": right,
                     "z0": upper if bay % 2 else lower,
                     "z1": lower if bay % 2 else upper,
                     "width": width,"support":"bay"}
            if brace["s1"]-brace["s0"] < .55 or abs(brace["z1"]-brace["z0"]) < .40:
                continue
            slope=abs(brace["z1"]-brace["z0"])/(brace["s1"]-brace["s0"])
            if not .70<=slope<=2.15:
                continue
            if any(_segment_hits_opening(brace, o.get("assembly_bounds",o), width*.5+.035) for o in constraints):
                continue
            # One selected brace per bay, in the first storey band with clearance.
            braces.append(brace)
            break

    profile=_gable_profile(plan, edge)
    peak=max(profile,key=lambda p:p[1])
    rakes=[]
    for (s0,z0),(s1,z1) in zip(profile,profile[1:]):
        if max(z0,z1)>top+.10:
            rakes.append({"s0":s0,"z0":z0-rake_drop,
                          "s1":s1,"z1":z1-rake_drop,"width":.19})

    def profile_crossings(height):
        hits=[]
        for (s0,z0),(s1,z1) in zip(profile,profile[1:]):
            if (z0-height)*(z1-height)<=0 and abs(z1-z0)>1e-9:
                t=(height-z0)/(z1-z0)
                if -1e-8<=t<=1+1e-8:
                    hits.append(s0+(s1-s0)*t)
        return sorted(set(round(x,8) for x in hits))

    kingpost=None
    collar=None
    if peak[1]>top+.35:
        kingpost={"s":peak[0],"z0":upper_plate,
                  "z1":peak[1]-kingpost_drop,"width":.15}
        collar_raw=top+(peak[1]-top)*.43
        crossings=profile_crossings(collar_raw)
        if len(crossings)>=2 and crossings[-1]-crossings[0]>.35:
            collar={"s0":crossings[0],"s1":crossings[-1],
                    "z":collar_raw-rake_drop,"width":.15}
    gable={"rakes":rakes,"kingpost":kingpost,"collar":collar}
    if getattr(plan,'disable_gable_frame',False):
        gable={"rakes":[],"kingpost":None,"collar":None}
    return {"edge_index": edge_index, "length": length, "openings": openings,
            "access_clearances":access_clearances,
            "opening_assembly_bounds":[dict(o["assembly_bounds"]) for o in openings],
            "posts": posts, "principal_posts": posts, "jambs": jambs,
            "unsupported_spans": unsupported_spans,
            "plates": plates, "braces": braces,
            "gable_profile": profile,"gable":gable,
            "roof_safety":{"eave":top,"slope":slope,
                           "structural_top":structural_top,
                           "upper_plate":upper_plate,
                           "rake_drop":rake_drop,
                           "kingpost_drop":kingpost_drop}}


def _add_foundation(buffers, plan, edge_index, edge):
    a,b,tx,ty,n,length = _edge_frame(plan, edge_index, edge)
    core = buffers["foundation_core"]
    stone = buffers["stone"]
    fh=_foundation(plan)
    style=getattr(plan,"style",None)
    if str(getattr(style,"foundation_mode","PLINTH")).upper()=="PIERS":
        # Raised timber buildings stand on visible piles and a perimeter deck,
        # leaving air below the floor instead of a closed stone plinth.
        stations=sorted(set([0.10,length-.10]+[round(s,4) for s in _frange(.1,length-.1,2.35)]))
        for ss in stations:
            x,y=a[0]+tx*ss,a[1]+ty*ss
            core.box((x,y,fh*.48),(.23,.23,max(.12,fh*.96)))
        _beam_edge(core,a,b,0,length,fh-.12,.24,.30)
        _beam_edge(core,a,b,0,length,fh-.025,.12,.30)
        return
    _wall_solid(core,a,b,n,0,length,0.0,fh,thickness=getattr(plan,'wall_thickness',WALL_THICKNESS))
    # Shallow, staggered cut-stone courses on the outside face; the core closes gaps.
    rng = plan.rng(f"facade.masonry.edge.{edge_index}")
    course_h = 0.22
    for row, z0 in enumerate((0.04, 0.26)):
        z1 = min(fh-0.015,z0+course_h)
        stagger = 0.0 if row == 0 else 0.36
        s = -stagger
        while s < length:
            span = rng.uniform(0.62,0.92)
            lo,hi = max(0.0,s+0.025),min(length,s+span-0.025)
            if hi-lo > 0.18:
                # A thin relief stone on the exposed face, bedded into the core.
                poly = _stone_relief(a,b,n,lo,hi)
                # Reduce relief depth by choosing a narrow extrusion polygon against the face.
                # Entire block remains closed, with visible recessed mortar between neighbours.
                stone.prism(poly,z0,z1)
            s += span


def _frange(start, stop, step):
    values=[]
    while start < stop:
        values.append(start)
        start += step
    return values


def _declare_flat_envelope(buffer, z, clearance, bounds_source=None):
    """Bind an independent canopy buffer to its generated horizontal roof plane."""
    if not buffer.vertices:
        return
    source=bounds_source if bounds_source is not None and bounds_source.vertices else buffer
    xs=[v[0] for v in source.vertices]
    ys=[v[1] for v in source.vertices]
    buffer.roof_envelope={"plane":(0.0,0.0,float(z)),"clearance":float(clearance),
                          "bounds":(min(xs),min(ys),max(xs),max(ys))}


def _corner_quoin(buf, point, size=0.25):
    buf.box((point[0],point[1],0.245),(size,size,0.40))


def _opening_frame(buffers, a,b,n,o, function, foundation_height=FOUNDATION_HEIGHT, generate_steps=True, glazing_recess=0., door_thickness=WALL_THICKNESS):
    tx,ty = _unit(a,b)[0]
    windows, doors, timbers, details = buffers["windows"],buffers["doors"],buffers["timber"],buffers["details"]
    kind=o["kind"]; s0,s1,z0,z1=o["s0"],o["s1"],o["z0"],o["z1"]
    def point(s, inset=0.0):
        return (a[0]+tx*s-n[0]*inset, a[1]+ty*s-n[1]*inset)
    if kind == "door":
        # Outer timber jambs, lintel, sill threshold, and deeply planked leaf.
        _beam_edge(timbers,a,b,s0-0.07,s0+0.08,(z0+z1)/2, z1-z0+0.14,0.28)
        _beam_edge(timbers,a,b,s1-0.08,s1+0.07,(z0+z1)/2, z1-z0+0.14,0.28)
        _beam_edge(timbers,a,b,s0-0.08,s1+0.08,z1+0.06,0.18,0.28)
        if o.get("role") in ("passage_entry","passage_exit"):
            return
        _beam_edge(timbers,a,b,s0-0.07,s1+0.07,z0+0.03,0.11,0.31)
        if generate_steps and str(function).upper()!="BOATHOUSE" and o.get("role")!="gallery_access":
            steps=max(1,math.ceil(foundation_height/.20))
            for step in range(steps):
                step_z0=foundation_height*step/steps
                step_z1=foundation_height*(step+1)/steps
                extension=.18-step*.045
                _step_prism(buffers["steps"],a,b,n,s0-extension,s1+extension,
                            (steps-step)*.28,step_z0,step_z1)
        # Door leaf as an oriented closed prism.
        poly = _xy_wall(a,b,n,s0+0.035,s1-0.035,inset=-0.018,thickness=door_thickness)
        doors.prism(poly,z0+0.05,z1-0.035)
        # Narrow vertical board seams and three cross rails, overlaid as timber members.
        count=max(3,int((s1-s0)/0.19))
        for j in range(1,count):
            ss=s0+0.035+(s1-s0-0.07)*j/count
            p0,p1=point(ss,-0.042),point(ss,-0.042)
            doors.beam((p0[0],p0[1],z0+0.12),(p1[0],p1[1],z1-0.12),0.018,0.018)
        for zz in (z0+0.36,z0+0.74,z1-0.26):
            _beam_edge(doors,a,b,s0+0.08,s1-0.08,zz,0.08,0.035,normal=n,normal_offset=.05)
        # Black iron strap hinges and a plain hanging ring.
        for zz in (z0+0.38,z1-0.40):
            _beam_edge(buffers["iron"],a,b,s0+0.03,s0+0.42,zz,0.045,0.035,normal=n,normal_offset=0.045)
        _beam_edge(buffers["iron"],a,b,s1-0.18,s1-0.08,z0+0.97,0.12,0.04,normal=n,normal_offset=0.045)
        x,y=point(s1-0.23,-0.055)
        # Eight short iron sections make a visible pull ring in the door plane.
        ring=[]
        tx,ty=_unit(a,b)[0]
        for k in range(8):
            ang=2*math.pi*k/8
            ring.append((x+0.048*math.cos(ang)*tx,y+0.048*math.cos(ang)*ty,z0+0.96+0.048*math.sin(ang)))
        for p,q in zip(ring,ring[1:]+ring[:1]):
            buffers["iron"].beam(p,q,0.016,0.016)
        return
    if kind == "vent":
        # Slatted agricultural ventilation stays weather-protected under a small hood.
        _beam_edge(timbers,a,b,s0-0.07,s0+0.07,(z0+z1)/2,z1-z0+0.13,0.20)
        _beam_edge(timbers,a,b,s1-0.07,s1+0.07,(z0+z1)/2,z1-z0+0.13,0.20)
        _beam_edge(timbers,a,b,s0-0.08,s1+0.08,z1+0.05,0.13,0.22)
        for k in range(4):
            zz=z0+0.10+(z1-z0-0.2)*k/3
            _beam_edge(timbers,a,b,s0+0.05,s1-0.05,zz,0.045,0.16)
        return
    # Deep timber casing and sill around glazing.
    frame=timbers
    _beam_edge(frame,a,b,s0-0.055,s0+0.055,(z0+z1)/2,z1-z0+0.11,0.19)
    _beam_edge(frame,a,b,s1-0.055,s1+0.055,(z0+z1)/2,z1-z0+0.11,0.19)
    _beam_edge(frame,a,b,s0-0.08,s1+0.08,z1+0.035,0.11,0.20)
    _beam_edge(frame,a,b,s0-0.09,s1+0.09,z0-0.025,0.15,0.24)
    # Glass is recessed within the real aperture, split into panes by a lead cross.
    inner0,inner1=s0+0.095,s1-0.095
    innerz0,innerz1=z0+0.10,z1-0.10
    if inner1>inner0 and innerz1>innerz0:
        windows.prism(_xy_opening_slab(a,b,n,inner0,inner1,.065-glazing_recess,.018),innerz0,innerz1)
        mid=(inner0+inner1)/2
        _beam_edge(buffers["iron"],a,b,mid-0.012,mid+0.012, (innerz0+innerz1)/2,innerz1-innerz0,0.025,normal=n,normal_offset=.075-glazing_recess)
        _beam_edge(buffers["iron"],a,b,inner0,inner1,(innerz0+innerz1)/2,0.025,0.025,normal=n,normal_offset=.075-glazing_recess)
    # Hinged exterior shutters: one or two narrow timber leaves, fixed open against jambs.
    leaf=min(0.18,(s1-s0)*0.21)
    for side in (-1,1):
        ss=s0-leaf*0.42 if side<0 else s1+leaf*0.42
        _beam_edge(buffers["shutters"],a,b,ss-leaf/2,ss+leaf/2,(z0+z1)/2,z1-z0-0.05,0.075,normal=n,normal_offset=.06)
        # Three simple horizontal rails indicate board joinery without clutter.
        for frac in (0.25,0.75):
            _beam_edge(buffers["shutters"],a,b,ss-leaf/2,ss+leaf/2,z0+(z1-z0)*frac,0.045,0.085,normal=n,normal_offset=.065)
        # Two short iron straps terminate at the shutter edge and pin into the
        # adjacent casing, making the hanging side legible at normal viewing scale.
        hinge_zs=(z0+(z1-z0)*.24,z0+(z1-z0)*.76)
        for hinge_z in hinge_zs:
            outer=ss-leaf/2 if side<0 else ss+leaf/2
            jamb=s0+.035 if side<0 else s1-.035
            _beam_edge(buffers["iron"],a,b,min(outer,jamb),max(outer,jamb),
                       hinge_z,.035,.028,normal=n,normal_offset=.092)


def _timber_frame(buffers, plan, edge_index, edge, openings, top):
    a,b,tx,ty,n,length=_edge_frame(plan,edge_index,edge)
    timber=buffers["timber"]
    layout = frame_layout(plan, edge_index, edge)
    detail=str(plan.settings.detail).upper()
    chamfer=.012 if detail=="HIGH" else (.008 if detail=="MEDIUM" else 0.0)
    post_width = .22 if str(plan.settings.function).upper() in ("BARN", "GRAIN_STORE") else .19
    structural_top=layout["roof_safety"]["structural_top"]
    visibility=float(getattr(getattr(plan,"style",None),"frame_visibility",1.0))
    if visibility > .16:
        for ss in layout["principal_posts"]:
            _post(timber,a,b,ss,_foundation(plan),structural_top,post_width,.25,chamfer)
    # Storey plates are continuous through ordinary bays and interrupted only
    # where a tall door removes the wall below that level.
    plate_schedule=(layout["plates"] if visibility>.16 and edge_index not in getattr(plan,'open_edges',()) else layout["plates"][-1:])
    for plate_index, z in enumerate(plate_schedule):
        thick = .19 if z==layout["plates"][-1] else .16
        gaps=[(o["s0"]-.04,o["s1"]+.04) for o in openings
              if o["kind"]=="door" and z<o["z1"]+.05]
        cursor=0.0
        for g0,g1 in sorted(gaps):
            if g0>cursor:
                _beam_edge(timber,a,b,cursor,g0,z,thick,.25,chamfer=chamfer)
            cursor=max(cursor,g1)
        if cursor<length:
            _beam_edge(timber,a,b,cursor,length,z,thick,.25,chamfer=chamfer)

    for brace in layout["braces"] if visibility > .16 else ():
        p0=(a[0]+tx*brace["s0"],a[1]+ty*brace["s0"],brace["z0"])
        p1=(a[0]+tx*brace["s1"],a[1]+ty*brace["s1"],brace["z1"])
        _frame_beam(timber,p0,p1,.14,brace["width"],chamfer)
        if brace.get("support")=="knee":
            for ss,zz in ((brace["s0"],brace["z0"]),(brace["s1"],brace["z1"])):
                for tangent_offset in (-.035,.035):
                    x=a[0]+tx*(ss+tangent_offset)
                    y=a[1]+ty*(ss+tangent_offset)
                    buffers["pegs"].cylinder((x+n[0]*.105,y+n[1]*.105,zz),
                                             (x+n[0]*.145,y+n[1]*.145,zz),.016,6)

    # The semantic gable schedule follows every rake segment in the actual roof
    # profile, including a simple two-slope triangle represented by one peak.
    for rake in layout["gable"]["rakes"] if visibility > .16 else ():
        _frame_beam(timber,
            (a[0]+tx*rake["s0"],a[1]+ty*rake["s0"],rake["z0"]),
            (a[0]+tx*rake["s1"],a[1]+ty*rake["s1"],rake["z1"]),
            rake["width"],.21,chamfer)
    kingpost=layout["gable"]["kingpost"]
    if kingpost and visibility > .16:
        _post(timber,a,b,kingpost["s"],kingpost["z0"],kingpost["z1"],
              kingpost["width"],.19,chamfer)
    collar=layout["gable"]["collar"]
    if collar and visibility > .16:
        _beam_edge(timber,a,b,collar["s0"],collar["s1"],collar["z"],
                   collar["width"],.19,chamfer=chamfer)


def _add_quoins(buffers, plan):
    if str(getattr(getattr(plan,"style",None),"foundation_mode","PLINTH")).upper()=="PIERS":
        return
    q=buffers["quoins"]
    for point in plan.outline:
        _corner_quoin(q,point,0.27)


def _add_chimney(buffers, plan):
    """A restrained, hollow brick stack with open flue, cap and weather staining."""
    s=plan.settings; fn=str(s.function).upper()
    # Domestic/inn/miller chimneys are appropriate; barns and grain stores are not heated.
    if fn not in ("FARMHOUSE","MILLER","INN","SMITHY","COTTAGE","LONGHOUSE") and not _type_features(plan).intersection({"forge_stack","chimney","central_hearth"}):
        return
    rect=max(plan.rects,key=lambda r:(r[2]-r[0])*(r[3]-r[1]))
    x0,y0,x1,y1,axis=rect
    x=x0+(x1-x0)*0.78
    y=y0+(y1-y0)*0.76
    bottom=plan.eave-0.18
    height=max(1.25,plan.roof_height(x,y)-bottom+0.7)
    height=min(height,3.8)
    ztop=bottom+height
    size=0.52
    stone=buffers["chimney"]
    # Four wall strips leave an actual continuous open flue through the stack.
    stone.box((x-size/2,y, (bottom+ztop)/2),(0.13,size,height))
    stone.box((x+size/2,y, (bottom+ztop)/2),(0.13,size,height))
    stone.box((x,y-size/2,(bottom+ztop)/2),(size,0.13,height))
    stone.box((x,y+size/2,(bottom+ztop)/2),(size,0.13,height))
    # Recessed horizontal beds and alternating short perp joints read as courses
    # while remaining shallow cuts in the solid flue walls.
    mortar=buffers["mortar"]
    course=.34
    row=1
    z=bottom+course
    while z<ztop-.12:
        for cx,cy,sx,sy in (
                (x,y-size/2-.008,size,.014), (x,y+size/2+.008,size,.014),
                (x-size/2-.008,y,.014,size), (x+size/2+.008,y,.014,size)):
            mortar.box((cx,cy,z),(sx,sy,.018))
        joint_x=x+(-.12 if row%2 else .12)
        joint_y=y+(.12 if row%2 else -.12)
        mortar.box((joint_x,y-size/2-.009,z+course*.48),(.014,.016,.30))
        mortar.box((joint_x,y+size/2+.009,z+course*.48),(.014,.016,.30))
        mortar.box((x-size/2-.009,joint_y,z+course*.48),(.016,.014,.30))
        mortar.box((x+size/2+.009,joint_y,z+course*.48),(.016,.014,.30))
        z+=course
        row+=1
    # Cap ledge and four small corner capstones preserve the flue opening.
    # Four cap stones form an open ring around the flue.
    cap=0.14
    stone.box((x-size/2-cap/2,y,ztop+0.04),(cap,size+0.18,0.12))
    stone.box((x+size/2+cap/2,y,ztop+0.04),(cap,size+0.18,0.12))
    stone.box((x,y-size/2-cap/2,ztop+0.04),(size,cap,0.12))
    stone.box((x,y+size/2+cap/2,ztop+0.04),(size,cap,0.12))
    # Soot tint is localized at the upper flue; patch pieces imply later repair, not ruin.
    details=buffers["details"]
    details.box((x-size*0.30,y-size/2-0.01,ztop-0.38),(0.12,0.025,0.34))
    # Four planar lead aprons sit over the shingle course at the stack penetration.
    # The selected stack lies on one analytic slope; finite differences recover that
    # plane while plan.roof_height keeps the flashing aligned with crossed roofs.
    eps=.015
    cx=(plan.roof_height(x+eps,y)-plan.roof_height(x-eps,y))/(2*eps)
    cy=(plan.roof_height(x,y+eps)-plan.roof_height(x,y-eps))/(2*eps)
    norm=math.sqrt(cx*cx+cy*cy+1.0)
    lift=(-cx/norm*.035,-cy/norm*.035,1.0/norm*.035)
    half=size/2
    apron=.28
    bands=[[(x-half,y-half),(x+half,y-half),(x+half,y-half-apron),(x-half,y-half-apron)],
           [(x-half,y+half),(x+half,y+half),(x+half,y+half+apron),(x-half,y+half+apron)],
           [(x-half,y-half),(x-half,y+half),(x-half-apron,y+half),(x-half-apron,y-half)],
           [(x+half,y-half),(x+half,y+half),(x+half+apron,y+half),(x+half+apron,y-half)]]
    for band in bands:
        poly=[]
        for px,py in band:
            ph=float(plan.roof_height(px,py))
            if not math.isfinite(ph):
                ph=float(plan.roof_height(x,y))
            poly.append((px,py,ph+.062))
        buffers["flashing"].extrude(poly,lift)


def _add_house_details(buffers, plan):
    fn=str(plan.settings.function).upper()
    for i,edge in enumerate(plan.edges):
        a,b,tx,ty,n,length=_edge_frame(plan,i,edge)
        if fn=="MILLER" and i==0:
            # A visible miller's tally board beside the entry reads as practical signage.
            ss=min(length-0.35,0.7)
            if ss>0.15:
                buffers["signage"].prism(_xy_opening_slab(a,b,n,ss-.15,ss+.15,.07,.055),1.59,1.97)
                for zz in (1.68,1.75,1.82):
                    _beam_edge(buffers["iron"],a,b,ss-.08,ss+.08,zz,.018,.018,normal=n,normal_offset=.085)
        if fn=="INN" and i==0:
            ss=length*0.78
            sign_top=min(3.02,plan.eave-(.14+.13*plan.slope+.03))
            sign_bottom=sign_top-.40
            buffers["signage"].prism(_xy_opening_slab(a,b,n,ss-.29,ss+.29,.075,.06),sign_bottom,sign_top)
            for edge_s in (ss-.32,ss+.32):
                _beam_edge(buffers["timber_light"],a,b,edge_s-.025,edge_s+.025,(sign_top+sign_bottom)*.5,.42,.075,normal=n,normal_offset=.09)
            _beam_edge(buffers["timber_light"],a,b,ss-.28,ss+.28,sign_top-.06,.04,.065,normal=n,normal_offset=.09)


def _add_function_details(buffers, plan, edge_openings):
    """Add original purpose-built exterior pieces from scheduled openings."""
    features=_type_features(plan)
    fh=_foundation(plan)
    porch_roof_levels=[]
    gallery_floor_levels=[]
    gallery_clearance_records=[]
    gallery_access_available=any(o.get("role")=="gallery_access"
                                 for edge_opening in edge_openings for o in edge_opening)
    for i,edge in enumerate(plan.edges):
        a,b,tx,ty,n,length=_edge_frame(plan,i,edge)
        openings=edge_openings[i]
        door=next((o for o in openings if o["kind"]=="door"),None)

        if door and features.intersection({"porch","public_porch","civic_porch","market_porch","covered_entry"}):
            s0,s1=door["s0"]-.30,door["s1"]+.30
            ztop=min(door["z1"]+.48,float(plan.eave)-.42)
            if ztop>door["z1"]+.20 and s0>.04 and s1<length-.04:
                buffers["porch_roof"].prism(_xy_opening_slab(a,b,n,s0,s1,.88,.70),ztop-.12,ztop)
                for ss in (s0+.08,s1-.08):
                    x,y=a[0]+tx*ss+n[0]*.56,a[1]+ty*ss+n[1]*.56
                    buffers["porch"].beam((x,y,fh),(x,y,ztop-.14),.14,.14)
                _beam_edge(buffers["porch"],a,b,s0,s1,ztop-.22,.13,.14,normal=n,normal_offset=.26)
                porch_roof_levels.append(ztop)

        # Exterior guard gallery aligns with the upper storey sill datum.
        if (features.intersection({"guard_gallery","passage_arch"})
                and int(plan.settings.floors)>1 and gallery_access_available):
            z=fh+(int(plan.settings.floors)-1)*float(plan.settings.floor_height)+.08
            if z<float(plan.eave)-.75:
                buffers["gallery_deck"].prism(_xy_opening_slab(a,b,n,.12,length-.12,.78,.68),z-.12,z)
                access=next((o for o in openings if o.get("role")=="gallery_access"),None)
                for ss in _frange(.25,length-.10,1.35):
                    if access and access["s0"]-.08<=ss<=access["s1"]+.08:
                        continue
                    x,y=a[0]+tx*ss+n[0]*.57,a[1]+ty*ss+n[1]*.57
                    buffers["gallery_rails"].beam((x,y,z),(x,y,z+1.0),.075,.075)
                rail_spans=[(.12,length-.12)]
                if access:
                    rail_spans=[(lo,hi) for lo,hi in (
                        (.12,access["s0"]-.08),(access["s1"]+.08,length-.12)) if hi-lo>.05]
                for lo,hi in rail_spans:
                    _beam_edge(buffers["gallery_rails"],a,b,lo,hi,z+1.0,.08,.08,
                               normal=n,normal_offset=.61)
                gallery_floor_levels.append(z)
                gallery_clearance_records.append({"edge_index":i,"floor_z":z,
                    "rail_height":1.0,"overhead_clearance":"unroofed",
                    "access_opening":None if access is None else dict(access)})

        # Loading hoist and wall brackets are centered on the actual cargo door.
        loading=next((o for o in openings if o.get("role")=="loading"),None)
        if loading and "hoist_beam" in features:
            z=min(loading["z1"]+.42,float(plan.eave)-.38)
            ss=(loading["s0"]+loading["s1"])*.5
            # The hoist projects beyond the wall; at a roof edge the analytic
            # weather plane drops along that normal. Clamp its full beam section
            # under the actual roof at both ends and the midpoint.
            beam_limits=[]
            for station in (ss-.68,ss,ss+.68):
                for normal_offset in (.15-.11,.15+.11):
                    x=a[0]+tx*station+n[0]*normal_offset
                    y=a[1]+ty*station+n[1]*normal_offset
                    roof_z=float(plan.roof_height(x,y))
                    if math.isfinite(roof_z):
                        beam_limits.append(roof_z-.12-.08-.01)
                    else:
                        beam_limits=[]
                        break
                if not beam_limits:
                    break
            if len(beam_limits)==6:
                z=min(z,min(beam_limits))
            else:
                z=loading["z1"]+.10
            if z>loading["z1"]+.12:
                _beam_edge(buffers["timber"],a,b,ss-.68,ss+.68,z,.16,.22,normal=n,normal_offset=.15)
                for side in (-1,1):
                    _beam_edge(buffers["timber"],a,b,ss+side*.53,ss+side*.61,z-.28,.36,.13,normal=n,normal_offset=.12)
                x,y=a[0]+tx*ss+n[0]*.20,a[1]+ty*ss+n[1]*.20
                buffers["iron"].beam((x,y,z-.04),(x,y,z-.30),.035,.035)
                buffers["iron"].beam((x-.06,y,z-.31),(x+.06,y,z-.31),.10,.035)

        # A projecting hood protects a smithy ventilation opening.
        vent=next((o for o in openings if o["kind"]=="vent"),None)
        if vent and "forge_stack" in features:
            top=min(vent["z1"]+.22,float(plan.eave)-.42)
            _beam_edge(buffers["details"],a,b,vent["s0"]-.12,vent["s1"]+.12,top,.12,.34,normal=n,normal_offset=.15)

        # A stepped exterior slipway meets the raised boathouse door threshold.
        if door and "slipway" in features:
            depth=1.8
            ramp_s0,ramp_s1=door["s0"]-.18,door["s1"]+.18
            ramp_top=[]
            for ss,dd in ((ramp_s0,0.0),(ramp_s1,0.0),(ramp_s1,depth),(ramp_s0,depth)):
                ramp_top.append((a[0]+tx*ss+n[0]*dd,a[1]+ty*ss+n[1]*dd,
                                 fh*(1.0-dd/depth)))
            # Closed sloping slipway plate, from the raised sill to grade.
            if area([(p[0],p[1]) for p in ramp_top])<0:
                ramp_top.reverse()
            ramp=buffers["slipway"]
            ramp.extrude(ramp_top,(0.0,0.0,-.12))
            # Two posts on each side of the platform carry a rail that follows
            # the ramp plane at 0.85m above its surface.
            def ramp_point(ss,dd,lift=0.0):
                floor_z=fh*(1.0-dd/depth)
                return (a[0]+tx*ss+n[0]*dd,a[1]+ty*ss+n[1]*dd,floor_z+lift)
            for ss in (door["s0"]-.08,door["s1"]+.08):
                p0=ramp_point(ss,.18)
                p1=ramp_point(ss,depth-.18)
                for base in (p0,p1):
                    buffers["access_rails"].beam(base,(base[0],base[1],base[2]+.85),.07,.07)
                buffers["access_rails"].beam(ramp_point(ss,.18,.85),
                                              ramp_point(ss,depth-.18,.85),.065,.065)
            if ramp.vertices:
                xs=[v[0] for v in ramp.vertices]; ys=[v[1] for v in ramp.vertices]
                pa=-fh/depth*n[0]; pb=-fh/depth*n[1]
                # Plane passes through the threshold at the wall line.
                pc=fh-pa*(a[0]+tx*ramp_s0)-pb*(a[1]+ty*ramp_s0)
                buffers["access_rails"].structural_role="exterior_access"
                buffers["access_rails"].support_surface={
                    "plane":(pa,pb,pc),
                    "bounds":(min(xs),min(ys),max(xs),max(ys)),
                    "max_height":1.0}

        # Open stone voussoirs frame the real through-opening; no leaf is placed.
        passage=next((o for o in openings if o.get("role") in ("passage_entry","passage_exit")),None)
        if passage and "passage_arch" in features:
            center=(passage["s0"]+passage["s1"])*.5
            radius=(passage["s1"]-passage["s0"])*.5
            spring=passage["z1"]-.42
            for k in range(7):
                t0=math.pi*k/7
                t1=math.pi*(k+1)/7
                p=(a[0]+tx*(center+radius*math.cos(t0)),a[1]+ty*(center+radius*math.cos(t0)),spring+radius*.34*math.sin(t0))
                q=(a[0]+tx*(center+radius*math.cos(t1)),a[1]+ty*(center+radius*math.cos(t1)),spring+radius*.34*math.sin(t1))
                _frame_beam(buffers["stone"],p,q,.24,.26,.012)

    # Each structural buffer is checked against its own actual generated canopy.
    # Roof slabs use zero clearance because the plane is their top weather face;
    # posts, rails and brackets keep the full 120mm underside clearance.
    if porch_roof_levels:
        roof_z=porch_roof_levels[0]
        _declare_flat_envelope(buffers["porch"],roof_z,.12,buffers["porch_roof"])
        _declare_flat_envelope(buffers["porch_roof"],roof_z,0.0)
    if gallery_floor_levels:
        floor_z=gallery_floor_levels[0]
        deck=buffers["gallery_deck"]
        rails=buffers["gallery_rails"]
        xs=[v[0] for v in deck.vertices]; ys=[v[1] for v in deck.vertices]
        rails.structural_role="exterior_access"
        rails.support_surface={"plane":(0.0,0.0,floor_z),
            "bounds":(min(xs),min(ys),max(xs),max(ys)),"max_height":1.15}
        plan.gallery_headroom={"type":"unroofed_guard_gallery",
            "floor_z":floor_z,"rail_height":1.0,"overhead_clearance":"unroofed",
            "clear_vertical_height":None,"edges":gallery_clearance_records}


def _gable_infill(buf, plan, edge):
    """Close each exterior gable up to the analytic roof envelope along that edge."""
    a,b=edge
    (tx,ty),length=_unit(a,b)
    n=(ty,-tx)
    def height_at(s):
        x,y=a[0]+tx*s,a[1]+ty*s
        h=float(plan.roof_height(x,y))
        return max(float(plan.eave),h) if math.isfinite(h) else float(plan.eave)
    # Subdivide at envelope kinks (ridge/valley intersections) so the infill hugs
    # the same analytic roof boundary instead of cutting a coarse chord beneath it.
    cuts={0.0,length}
    def refine(s0,s1,h0,h1,depth=0):
        sm=(s0+s1)*.5; hm=height_at(sm)
        if depth<9 and abs(hm-max(float(plan.eave),(h0+h1)*.5))>.006:
            cuts.add(sm)
            refine(s0,sm,h0,hm,depth+1)
            refine(sm,s1,hm,h1,depth+1)
    refine(0.0,length,height_at(0.0),height_at(length))
    stations=sorted(cuts)
    for s0,s1 in zip(stations,stations[1:]):
        x0,y0=a[0]+tx*s0,a[1]+ty*s0
        x1,y1=a[0]+tx*s1,a[1]+ty*s1
        z0=height_at(s0)
        z1=height_at(s1)
        if max(z0,z1) <= plan.eave+0.025:
            continue
        base=float(plan.eave)
        poly=[(x0,y0,base),(x1,y1,base),(x1,y1,z1),(x0,y0,z0)]
        # Edge tangent crossed with vertical points outward for a CCW footprint.
        thickness=getattr(plan,'wall_thickness',WALL_THICKNESS)
        clearance=getattr(plan,'wall_infill_roof_clearance',None)
        if clearance is None:
            buf.extrude(poly,(-n[0]*thickness,-n[1]*thickness,0.0))
        else:
            # A vertical extrusion copies the outside gable height to the
            # inside face. On a shed high wall the weather plane falls inward,
            # so that copied face used to emerge through the roof covering.
            # Build the actual mitred solid with each top corner at its local
            # soffit; retain the same wall station and editable semantic ID.
            footprint=_xy_wall(a,b,n,s0,s1,thickness=thickness)
            lower=[(x,y,base) for x,y in footprint]
            upper=[]
            for x,y in footprint:
                s=(x-a[0])*tx+(y-a[1])*ty
                h=height_at(s)
                roof=float(plan.roof_height(x,y))
                cap=max(base,roof-clearance) if math.isfinite(roof) else h
                upper.append((x,y,min(h,cap)))
            # At the eave a wedge can taper to zero height. Weld coincident
            # corners and omit collapsed side faces instead of emitting zero-
            # area quads; the remaining triangles still close the solid.
            vertices=[];lookup={};remap=[]
            for point in lower+upper:
                if point not in lookup:
                    lookup[point]=len(vertices);vertices.append(point)
                remap.append(lookup[point])
            faces=[]
            for source in ((3,2,1,0),(4,5,6,7),(0,1,5,4),
                           (1,2,6,5),(2,3,7,6),(3,0,4,7)):
                face=[]
                for i in source:
                    j=remap[i]
                    if not face or j!=face[-1]:face.append(j)
                if len(face)>1 and face[0]==face[-1]:face.pop()
                if len(set(face))>=3:faces.append(tuple(face))
            if len(vertices)>=4 and len(faces)>=4:
                buf.indexed(vertices,faces)


def build_facades(plan):
    """Build exterior wall, frame, openings, plinth and restrained building details."""
    buffers = {}
    def add(key, material, layer):
        buffers[key]=MeshBuffer("facade_"+key, material, layer)
    style=getattr(plan,"style",None)
    fh=_foundation(plan)
    pier_mode=str(getattr(style,"foundation_mode","PLINTH")).upper()=="PIERS"
    construction=str(getattr(style,"construction","TIMBER_INFILL")).upper()
    wall_material=str(getattr(style,"wall_material","plaster"))
    add("foundation_core","timber" if pier_mode else "stone","foundation")
    add("steps","stone_light","foundation")
    add("stone","stone_light","foundation")
    add("mortar","mortar","foundation")
    add("quoins","stone_light","foundation")
    add("walls",wall_material,"walls")
    add("masonry_skin","stone_light" if construction=="RUBBLE" else "stone","walls")
    add("board_skin","timber_light","walls")
    add("patches","plaster_patch","walls")
    add("timber","timber","structure")
    add("timber_light","timber_light","structure")
    add("pegs","timber_light","structure")
    add("windows","glass","windows")
    add("shutters","timber_light","windows")
    add("doors","timber","doors")
    add("iron","iron","details")
    add("details","stone_light","details")
    add("chimney","stone","details")
    add("flashing","iron","details")
    add("signage","timber_light","details")
    add("porch","timber_light" if construction in ("TIMBER_INFILL","BOARD") else "stone","details")
    add("porch_roof","timber_light" if construction in ("TIMBER_INFILL","BOARD") else "stone","details")
    add("gallery_deck","timber_light","foundation")
    add("gallery_rails","timber_light","details")
    add("access_rails","timber","details")
    add("slipway","timber_light","foundation")

    if pier_mode:
        # A continuous closed timber deck sits at the plan foundation datum and
        # joins the raised perimeter beams before the wall assemblies begin.
        buffers["foundation_core"].prism(plan.outline,fh-.15,fh)

    wall_top=float(plan.eave)
    skin_buffer=(buffers["masonry_skin"] if construction in ("RUBBLE","ASHLAR") else
                 buffers["board_skin"] if construction=="BOARD" else None)
    if skin_buffer is not None and str(getattr(plan.settings,"geometry_mode","SOLID")).upper()=="EFFICIENT":
        skin_buffer.topology="SURFACE"
    records=[]
    for i,edge in enumerate(plan.edges):
        a,b,tx,ty,n,length=_edge_frame(plan,i,edge)
        openings=_openings_for_edge(plan,i,edge)
        records.append((edge,openings))
        _add_foundation(buffers,plan,i,edge)
        is_open=i in getattr(plan,'open_edges',())
        if not is_open:_wall_panels(buffers["walls"],a,b,n,length,openings,wall_top,fh,getattr(plan,'wall_thickness',WALL_THICKNESS))
        if skin_buffer is not None and not is_open:
            _cladding_tiles(plan,i,edge,openings,construction,skin_buffer)
        _timber_frame(buffers,plan,i,edge,openings,wall_top)
        # Small exposed pegs indicate the principal post/plate joints. Pegs follow
        # the semantic frame schedule and sit flush to the outward face of timber.
        layout=frame_layout(plan,i,edge)
        peg_positions=(layout["principal_posts"]
                       if float(getattr(style,"frame_visibility",1.0))>.16 else ())
        peg_levels=(layout["plates"][1:-1]
                    if float(getattr(getattr(plan,"style",None),"frame_visibility",1.0))>.16 else [])
        if (float(getattr(getattr(plan,"style",None),"frame_visibility",1.0))>.16
                and not peg_levels and len(layout["plates"])>1):
            peg_levels=[layout["plates"][-1]]
        for ss in peg_positions:
            for z in peg_levels:
                # Paired oak pegs enter the joint across the post face. Their
                # centers stay within the member width and their outer caps only
                # protrude a few millimetres beyond the timber plane.
                for tangent_offset in (-.052,.052):
                    x=a[0]+tx*(ss+tangent_offset)
                    y=a[1]+ty*(ss+tangent_offset)
                    start=(x+n[0]*.105,y+n[1]*.105,z)
                    end=(x+n[0]*.145,y+n[1]*.145,z)
                    buffers["pegs"].cylinder(start,end,.018,6)
        for o in openings:
            _opening_frame(buffers,a,b,n,o,str(plan.settings.function).upper(),_foundation(plan),
                           getattr(plan,'entry_steps',True),getattr(plan,'glazing_recess',0.),
                           getattr(plan,'door_thickness',WALL_THICKNESS))
        # Foundation joints are represented by very shallow mortar reveals between courses.
        # Thin segmented seams remain on the exterior face and never cut the solid core.
        tx,ty=_unit(a,b)[0]
        for z in (0.245,):
            _beam_edge(buffers["mortar"],a,b,0.0,length,z,0.012,0.012)
        if not is_open:_gable_infill(buffers["walls"],plan,edge)
    # Keep semantic opening records next to the generated plan for independent
    # collision review. Records include complete casing/shutter bounds.
    plan.facade_records=[{"edge_index":i,"openings":[dict(o) for o in openings],
                          "frame_layout":frame_layout(plan,i,edge)}
                         for i,(edge,openings) in enumerate(records)]
    if str(plan.settings.function).upper()=="GATEHOUSE":
        passage=[]
        for i,(_edge,openings) in enumerate(records):
            for o in openings:
                if o.get("role") in ("passage_entry","passage_exit"):
                    a,b=plan.edges[i]
                    tx,ty=_unit(a,b)[0]
                    center=(o["s0"]+o["s1"])*.5
                    passage.append({"edge_index":i,"role":o["role"],
                                    "center":(a[0]+tx*center,a[1]+ty*center),
                                    "s0":o["s0"],"s1":o["s1"],"z0":o["z0"],"z1":o["z1"]})
        if len(passage)==2:
            centers_aligned=abs(passage[0]["center"][0]-passage[1]["center"][0])<=1e-6
            same_width=abs((passage[0]["s1"]-passage[0]["s0"])-
                           (passage[1]["s1"]-passage[1]["s0"]))<=1e-6
            plan.passage_geometry={"kind":"open_through_passage",
                "valid":centers_aligned and same_width,"alignment":{"centers_aligned":centers_aligned,
                "same_width":same_width},"openings":passage,
                "clear_width":min(p["s1"]-p["s0"] for p in passage),
                "clear_height":min(p["z1"] for p in passage)-fh,
                "centerline_length":math.dist(passage[0]["center"],passage[1]["center"])}
        else:
            plan.passage_geometry={"kind":"open_through_passage","openings":passage,
                                   "valid":False}
    _add_quoins(buffers,plan)
    if not getattr(plan,'suppress_chimney',False):_add_chimney(buffers,plan)
    if not getattr(plan,'suppress_function_details',False):
        _add_house_details(buffers,plan)
        _add_function_details(buffers,plan,[openings for _,openings in records])

    # Keep the output compact and omit empty semantic buffers.
    return [buffers[key] for key in buffers if buffers[key].faces]
