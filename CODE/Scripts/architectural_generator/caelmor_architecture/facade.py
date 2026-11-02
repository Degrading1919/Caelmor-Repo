"""Grounded exterior facade construction for Caelmor's procedural buildings."""
from __future__ import annotations

import math
from collections import defaultdict

from .geometry import MeshBuffer, area


# Millimetres are intentionally avoided: all dimensions follow the engine's metre scale.
WALL_THICKNESS = 0.30
FOUNDATION_HEIGHT = 0.45


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    return (dx / length, dy / length), length


def _xy_wall(a, b, normal, start, end, inset=0.0):
    """A thin wall footprint between edge parameters; inset is measured inward."""
    tx, ty = _unit(a, b)[0]
    ox, oy = normal
    p0 = (a[0] + tx * start - ox * inset, a[1] + ty * start - oy * inset)
    p1 = (a[0] + tx * end - ox * inset, a[1] + ty * end - oy * inset)
    q1 = (p1[0] - ox * WALL_THICKNESS, p1[1] - oy * WALL_THICKNESS)
    q0 = (p0[0] - ox * WALL_THICKNESS, p0[1] - oy * WALL_THICKNESS)
    poly = [p0, p1, q1, q0]
    if area(poly) < 0:
        poly.reverse()
    return poly


def _wall_solid(buf, a, b, normal, s0, s1, z0, z1, inset=0.0):
    if s1 - s0 > 1e-4 and z1 - z0 > 1e-4:
        buf.prism(_xy_wall(a, b, normal, s0, s1, inset), z0, z1)


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
    if edge_index == entrance_edge and length > 2.7:
        door_w = {"BARN":2.55,"GRAIN_STORE":1.45,"INN":1.18}.get(fn,1.05)
        center = length * (0.46 if fn in ("FARMHOUSE", "MILLER") else 0.50)
        door_head = {"BARN":2.78,"INN":2.68}.get(fn,2.58)
        openings.append({"kind":"door", "s0":center-door_w/2, "s1":center+door_w/2, "z0":FOUNDATION_HEIGHT-0.02, "z1":door_head})

    if usable < 1.0:
        return openings
    # Purpose shapes the rhythm: barns and grain stores use broad high vents; homes use
    # smaller domestic windows; inns favour a more regular public frontage.
    if fn in ("BARN", "GRAIN_STORE"):
        nominal, ww, wh = (3.25, 0.72, 0.55) if fn == "BARN" else (3.7, 0.64, 0.48)
        count = max(0, min(4, int((usable + 0.4) // nominal)))
        for k in range(count):
            center = margin + usable * (k + 1) / (count + 1)
            openings.append({"kind":"vent", "s0":center-ww/2, "s1":center+ww/2,
                             "z0":2.05 + rng.uniform(-0.08, 0.10), "z1":2.05 + wh + rng.uniform(-0.04, 0.05)})
    else:
        nominal = 2.65 if fn == "INN" else (2.85 if fn == "MILLER" else 3.1)
        count = max(0, min(5, int((usable + 0.2) // nominal)))
        if s.floors > 1:
            for level in range(min(int(s.floors), 3)):
                # Ground floor avoids the entry; upper windows repeat at the floor plate.
                zbase = 0.78 if level == 0 else FOUNDATION_HEIGHT + level * float(s.floor_height) + 0.78
                zh = 1.17 if level == 0 else 1.12
                for k in range(count):
                    center = margin + usable * (k + 1) / (count + 1)
                    if level == 0 and any(o["kind"] == "door" and abs((o["s0"] + o["s1"])/2-center) < 1.0 for o in openings):
                        continue
                    jitter = rng.uniform(-0.06, 0.06)
                    w = (1.05 if fn == "INN" else 0.9) * float(s.window_density)
                    openings.append({"kind":"window", "s0":center-w/2+jitter, "s1":center+w/2+jitter,
                                     "z0":zbase, "z1":zbase+zh})
        else:
            for k in range(count):
                center = margin + usable * (k + 1) / (count + 1)
                if any(o["kind"] == "door" and abs((o["s0"]+o["s1"])/2-center) < 0.85 for o in openings):
                    continue
                w = (1.08 if fn == "INN" else 0.92) * float(s.window_density)
                jitter = rng.uniform(-0.08, 0.08)
                openings.append({"kind":"window", "s0":center-w/2+jitter, "s1":center+w/2+jitter,
                                 "z0":0.86, "z1":2.06 if fn == "INN" else 1.98})

    # Clamp records to the wall and reject degenerate windows for narrow wings.
    clean = []
    for o in openings:
        o["s0"] = max(0.32, o["s0"])
        o["s1"] = min(length-0.32, o["s1"])
        o["z1"] = min(o["z1"], plan.eave - (0.18 if o["kind"]=="door" else 0.48))
        if o["s1"] - o["s0"] >= 0.38 and o["z1"] - o["z0"] >= 0.35:
            clean.append(o)
    # Resolve accidental overlaps in deterministic order, keeping a margin between cuts.
    clean.sort(key=lambda o: (o["s0"], o["z0"]))
    out = []
    for o in clean:
        if any(not (o["s1"] <= q["s0"]+0.08 or o["s0"] >= q["s1"]-0.08 or
                    o["z1"] <= q["z0"]+0.08 or o["z0"] >= q["z1"]-0.08) for q in out):
            continue
        out.append(o)
    return out


def _wall_panels(buf, a, b, normal, length, openings, top):
    """Tessellate the wall around apertures; no wall surface crosses an opening."""
    xs = {0.0, length}
    zs = {FOUNDATION_HEIGHT, top}
    for o in openings:
        xs.update((o["s0"], o["s1"]))
        if o["z0"] > FOUNDATION_HEIGHT:
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
                _wall_solid(buf, a, b, normal, s0, s1, z0, z1)


def _beam_edge(buf, a, b, s0, s1, z, thickness, depth, material=None, normal=None, normal_offset=0.0):
    tx, ty = _unit(a,b)[0]
    nx,ny=normal or (0.0,0.0)
    p = (a[0]+tx*s0+nx*normal_offset, a[1]+ty*s0+ny*normal_offset, z)
    q = (a[0]+tx*s1+nx*normal_offset, a[1]+ty*s1+ny*normal_offset, z)
    # MeshBuffer.beam uses its width axis normal to a horizontal wall edge and its
    # depth axis vertical. Swap the intuitive (height, wall-depth) arguments here.
    buf.beam(p, q, depth, thickness)


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


def _post(buf, a, b, s, z0, z1, face_width=0.16, depth=0.20):
    tx, ty = _unit(a,b)[0]
    # beam vertical; width/depth are the two horizontal cross-section dimensions.
    x, y = a[0]+tx*s, a[1]+ty*s
    buf.beam((x,y,z0), (x,y,z1), face_width, depth)


def _add_foundation(buffers, plan, edge_index, edge):
    a,b,tx,ty,n,length = _edge_frame(plan, edge_index, edge)
    core = buffers["foundation_core"]
    stone = buffers["stone"]
    _wall_solid(core,a,b,n,0,length,0.0,FOUNDATION_HEIGHT)
    # Shallow, staggered cut-stone courses on the outside face; the core closes gaps.
    rng = plan.rng(f"facade.masonry.edge.{edge_index}")
    course_h = 0.22
    for row, z0 in enumerate((0.04, 0.26)):
        z1 = min(FOUNDATION_HEIGHT-0.015,z0+course_h)
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


def _corner_quoin(buf, point, size=0.25):
    buf.box((point[0],point[1],0.245),(size,size,0.40))


def _opening_frame(buffers, a,b,n,o, function):
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
        _beam_edge(timbers,a,b,s0-0.07,s1+0.07,z0+0.03,0.11,0.31)
        _step_prism(buffers["steps"],a,b,n,s0-0.18,s1+0.18,0.92,0.0,0.19)
        _step_prism(buffers["steps"],a,b,n,s0-0.14,s1+0.14,0.57,0.19,0.43)
        # Door leaf as an oriented closed prism.
        poly = _xy_wall(a,b,n,s0+0.035,s1-0.035,inset=-0.018)
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
        windows.prism(_xy_opening_slab(a,b,n,inner0,inner1,.065,.018),innerz0,innerz1)
        mid=(inner0+inner1)/2
        _beam_edge(buffers["iron"],a,b,mid-0.012,mid+0.012, (innerz0+innerz1)/2,innerz1-innerz0,0.025,normal=n,normal_offset=.075)
        _beam_edge(buffers["iron"],a,b,inner0,inner1,(innerz0+innerz1)/2,0.025,0.025,normal=n,normal_offset=.075)
    # Hinged exterior shutters: one or two narrow timber leaves, fixed open against jambs.
    leaf=min(0.18,(s1-s0)*0.21)
    for side in (-1,1):
        ss=s0-leaf*0.42 if side<0 else s1+leaf*0.42
        _beam_edge(buffers["shutters"],a,b,ss-leaf/2,ss+leaf/2,(z0+z1)/2,z1-z0-0.05,0.075,normal=n,normal_offset=.06)
        # Three simple horizontal rails indicate board joinery without clutter.
        for frac in (0.25,0.75):
            _beam_edge(buffers["shutters"],a,b,ss-leaf/2,ss+leaf/2,z0+(z1-z0)*frac,0.045,0.085,normal=n,normal_offset=.065)


def _timber_frame(buffers, plan, edge_index, edge, openings, top):
    a,b,tx,ty,n,length=_edge_frame(plan,edge_index,edge)
    timber=buffers["timber"]
    # Heavy corners and intermediate posts; move a post away from each aperture.
    post_positions=[0.10,length-0.10]
    spacing=2.9 if str(plan.settings.function).upper() in ("BARN","GRAIN_STORE") else 3.3
    candidate=spacing
    while candidate < length-0.35:
        if all(not (o["s0"]-0.12 < candidate < o["s1"]+0.12 and o["z0"] < top-0.1) for o in openings):
            post_positions.append(candidate)
        candidate += spacing
    for o in openings:
        # Window/door jambs are strong posts, with a timber head and sill.
        post_positions.extend((max(0.05,o["s0"]-0.045), min(length-0.05,o["s1"]+0.045)))
    for ss in sorted(set(round(p,4) for p in post_positions)):
        _post(timber,a,b,ss,FOUNDATION_HEIGHT,top,0.19,0.24)
    # Continuous floor plates / wall plates with a small break around large door openings.
    plates=[(FOUNDATION_HEIGHT+0.025,0.16),(top-0.10,0.19)]
    plates.extend((FOUNDATION_HEIGHT+level*float(plan.settings.floor_height),0.15)
                  for level in range(1,int(plan.settings.floors)))
    for z,thick in plates:
        gaps=[(o["s0"]-0.04,o["s1"]+0.04) for o in openings if o["kind"]=="door" and z<o["z1"]+0.05]
        cursor=0.0
        for g0,g1 in sorted(gaps):
            if g0>cursor: _beam_edge(timber,a,b,cursor,g0,z,thick,0.25)
            cursor=max(cursor,g1)
        if cursor<length: _beam_edge(timber,a,b,cursor,length,z,thick,0.25)
    # Short braces run only through solid corner/post spans and stop below opening heads.
    anchors=sorted(set((0.14,length-0.14)+tuple(p for p in post_positions if 0.18<p<length-0.18)))
    for left,right in zip(anchors,anchors[1:]):
        if right-left<0.45 or any(o["s0"]<right-0.08 and o["s1"]>left+0.08 and o["z0"]<FOUNDATION_HEIGHT+1.05 for o in openings):
            continue
        span=min(0.46,(right-left)*0.22)
        for side in (0,1):
            ss0,ss1=(left+0.10,left+0.10+span) if side==0 else (right-0.10-span,right-0.10)
            rise=0.42
            p0=(a[0]+tx*ss0,a[1]+ty*ss0,FOUNDATION_HEIGHT+0.15)
            p1=(a[0]+tx*ss1,a[1]+ty*ss1,FOUNDATION_HEIGHT+0.15+rise)
            timber.beam(p0,p1,0.13,0.19)
    # Rake members and restrained gable studs continue the timber frame above eaves.
    stations=sorted(set([0.0,length]+[length*k/max(1,int(math.ceil(length/.48)))
                                      for k in range(1,int(math.ceil(length/.48)))]))
    heights=[]
    for ss in stations:
        xx,yy=a[0]+tx*ss,a[1]+ty*ss
        hh=max(float(plan.eave),float(plan.roof_height(xx,yy)))
        heights.append(hh)
    for (s0,z0),(s1,z1) in zip(zip(stations,heights),zip(stations[1:],heights[1:])):
        if max(z0,z1)>float(plan.eave)+0.08:
            timber.beam((a[0]+tx*s0,a[1]+ty*s0,z0-0.06),
                        (a[0]+tx*s1,a[1]+ty*s1,z1-0.06),0.16,0.20)
    for ss,hh in zip(stations[1:-1],heights[1:-1]):
        if hh<=float(plan.eave)+0.25:
            continue
        if any(o["s0"]-0.12<ss<o["s1"]+0.12 and o["z1"]>float(plan.eave) for o in openings):
            continue
        _post(timber,a,b,ss,float(plan.eave)+0.06,hh-0.12,0.13,0.18)


def _add_quoins(buffers, plan):
    q=buffers["quoins"]
    for point in plan.outline:
        _corner_quoin(q,point,0.27)


def _add_chimney(buffers, plan):
    """A restrained, hollow brick stack with open flue, cap and weather staining."""
    s=plan.settings; fn=str(s.function).upper()
    # Domestic/inn/miller chimneys are appropriate; barns and grain stores are not heated.
    if fn not in ("FARMHOUSE","MILLER","INN"):
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
    for dx,dz in ((-0.13,0.62),(0.15,1.44),(0.07,2.08)):
        if dz < height-0.22:
            buffers["patches"].box((x+dx,y-size/2-0.025,bottom+dz),(0.13,0.028,0.11))
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
    # Limited repairs and material variation are deterministic and functionally restrained.
    for i,edge in enumerate(plan.edges):
        a,b,tx,ty,n,length=_edge_frame(plan,i,edge)
        rng=plan.rng(f"facade.repair.edge.{i}")
        if fn in ("BARN","GRAIN_STORE"):
            # Occasional vertical weather boards and broad sliding-door strap hints.
            if length>4.0:
                ss=length*0.84
                _beam_edge(buffers["timber_light"],a,b,ss-0.11,ss+0.11,FOUNDATION_HEIGHT+0.9,1.45,0.04)
        if fn=="MILLER" and i==0:
            # A visible miller's tally board beside the entry reads as practical signage.
            ss=min(length-0.35,0.7)
            if ss>0.15:
                buffers["signage"].prism(_xy_opening_slab(a,b,n,ss-.15,ss+.15,.07,.055),1.59,1.97)
                for zz in (1.68,1.75,1.82):
                    _beam_edge(buffers["iron"],a,b,ss-.08,ss+.08,zz,.018,.018,normal=n,normal_offset=.085)
        if fn=="INN" and i==0:
            ss=length*0.78
            buffers["signage"].prism(_xy_opening_slab(a,b,n,ss-.29,ss+.29,.075,.06),2.62,3.02)
            for edge_s in (ss-.32,ss+.32):
                _beam_edge(buffers["timber_light"],a,b,edge_s-.025,edge_s+.025,2.82,.42,.075,normal=n,normal_offset=.09)
            _beam_edge(buffers["timber_light"],a,b,ss-.28,ss+.28,2.96,.04,.065,normal=n,normal_offset=.09)
        # A few settled plaster patches stay comfortably away from openings and frame timbers.
        if fn in ("FARMHOUSE","MILLER","INN") and rng.random()<0.28 and length>3.0:
            ss=rng.uniform(0.9,length-0.9)
            z=rng.uniform(0.68,max(0.8,plan.eave-0.8))
            w=rng.uniform(0.24,0.42); h=rng.uniform(0.13,0.25)
            poly=_xy_opening_slab(a,b,n,ss-w/2,ss+w/2,.025,.025)
            # Avoid the openings by testing the patch centre against stored opening cuts.
            if all(not (o["s0"]<ss<o["s1"] and o["z0"]-h<z<o["z1"]+h) for o in _openings_for_edge(plan,i,edge)):
                buffers["patches"].prism(poly,z-h/2,z+h/2)


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
        poly=[(x0,y0,float(plan.eave)),(x1,y1,float(plan.eave)),(x1,y1,z1),(x0,y0,z0)]
        # Edge tangent crossed with vertical points outward for a CCW footprint.
        buf.extrude(poly,(-n[0]*WALL_THICKNESS,-n[1]*WALL_THICKNESS,0.0))


def build_facades(plan):
    """Build exterior wall, frame, openings, plinth and restrained building details."""
    buffers = {}
    def add(key, material, layer):
        buffers[key]=MeshBuffer("facade_"+key, material, layer)
    add("foundation_core","stone","foundation")
    add("steps","stone_light","foundation")
    add("stone","stone_light","foundation")
    add("mortar","mortar","foundation")
    add("quoins","stone_light","foundation")
    add("walls","plaster","walls")
    add("patches","plaster_patch","walls")
    add("timber","timber","structure")
    add("timber_light","timber_light","structure")
    add("windows","glass","windows")
    add("shutters","timber_light","windows")
    add("doors","timber","doors")
    add("iron","iron","details")
    add("details","stone_light","details")
    add("chimney","stone","details")
    add("flashing","iron","details")
    add("signage","timber_light","details")

    wall_top=float(plan.eave)
    records=[]
    for i,edge in enumerate(plan.edges):
        a,b,tx,ty,n,length=_edge_frame(plan,i,edge)
        openings=_openings_for_edge(plan,i,edge)
        records.append((edge,openings))
        _add_foundation(buffers,plan,i,edge)
        _wall_panels(buffers["walls"],a,b,n,length,openings,wall_top)
        _timber_frame(buffers,plan,i,edge,openings,wall_top)
        for o in openings:
            _opening_frame(buffers,a,b,n,o,str(plan.settings.function).upper())
        # Foundation joints are represented by very shallow mortar reveals between courses.
        # Thin segmented seams remain on the exterior face and never cut the solid core.
        tx,ty=_unit(a,b)[0]
        for z in (0.245,):
            _beam_edge(buffers["mortar"],a,b,0.0,length,z,0.012,0.012)
        _gable_infill(buffers["walls"],plan,edge)
    _add_quoins(buffers,plan)
    _add_chimney(buffers,plan)
    _add_house_details(buffers,plan)

    # Keep the output compact and omit empty semantic buffers.
    return [buffers[key] for key in buffers if buffers[key].faces]
