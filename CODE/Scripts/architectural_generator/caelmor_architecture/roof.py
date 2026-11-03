"""Analytic upper-envelope cross gables; no prefab sections or skeleton dependency.

Every visible patch is a convex polygon on an exact plane. Competitor planes are
subtracted only within their support domain. Tile courses are clipped to these
same patches, including the valleys. The welded deck closes the weather shell.
"""
from dataclasses import dataclass
import math
from collections import defaultdict
from .geometry import MeshBuffer, clip, area, inequalities, subtract_convex, lerp


@dataclass
class RoofPatch:
    poly: list
    plane: tuple
    source: int = 0

    def height(self,x,y):
        a,b,c=self.plane
        return a*x+b*y+c


def roof_sources(plan):
    result=[]
    o=plan.settings.overhang
    s=plan.slope
    for i,(a,b,c,d,axis) in enumerate(plan.rects):
        ymin,ymax=b-o,d+o if i==0 else d
        xmin,xmax=a-o,c+o
        if plan.settings.roof_style=='HIP':
            # A hip is the lower envelope of its four eave-distance planes.
            # Partition each rectangle first; roof_faces may then union those
            # explicitly supported slopes across intersecting building volumes.
            planes=[(s,0,plan.eave-s*a),(-s,0,plan.eave+s*c),
                    (0,s,plan.eave-s*b),(0,-s,plan.eave+s*d)]
            domain=[(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)]
            for plane in planes:
                poly=domain
                for other in planes:
                    if other==plane:
                        continue
                    poly=clip(poly,*(u-v for u,v in zip(other,plane)))
                    if not poly:
                        break
                if poly:
                    result.append(RoofPatch(poly,plane,i))
            continue
        if axis=='X':
            middle=(b+d)*.5
            result.extend([
                RoofPatch([(xmin,ymin),(xmax,ymin),(xmax,middle),(xmin,middle)],(0,s,plan.eave-s*b),i),
                RoofPatch([(xmin,middle),(xmax,middle),(xmax,ymax),(xmin,ymax)],(0,-s,plan.eave+s*d),i)])
        else:
            middle=(a+c)*.5
            result.extend([
                RoofPatch([(xmin,ymin),(middle,ymin),(middle,ymax),(xmin,ymax)],(s,0,plan.eave-s*a),i),
                RoofPatch([(middle,ymin),(xmax,ymin),(xmax,ymax),(middle,ymax)],(-s,0,plan.eave+s*c),i)])
    return result


def roof_faces(plan):
    sources=roof_sources(plan)
    visible=[]
    for i,face in enumerate(sources):
        fragments=[face.poly]
        for j,other in enumerate(sources):
            if i==j:
                continue
            diff=tuple(a-b for a,b in zip(other.plane,face.plane))
            if max(abs(v) for v in diff)<1e-8:
                if j>i:
                    continue
                cutter=inequalities(other.poly)
            elif abs(diff[0])+abs(diff[1])<1e-8:
                if diff[2]<0:
                    continue
                cutter=inequalities(other.poly)
            else:
                cutter=inequalities(other.poly)+[diff]
            fragments=[part for poly in fragments for part in subtract_convex(poly,cutter)]
            if not fragments:
                break
        visible.extend(RoofPatch(poly,face.plane,face.source) for poly in fragments if area(poly)>1e-7)
    return visible


def roof_topology(patches):
    """Split all T junctions, weld exact seams; return top verts/faces/edge users."""
    points={tuple(round(v,8) for v in (x,y,p.height(x,y)))
            for p in patches for x,y in p.poly}
    points=sorted(points)
    index={p:i for i,p in enumerate(points)}
    faces=[]
    for patch in patches:
        face=[]
        poly=[(x,y,patch.height(x,y)) for x,y in patch.poly]
        for a,b in zip(poly,poly[1:]+poly[:1]):
            a=tuple(round(v,8) for v in a)
            b=tuple(round(v,8) for v in b)
            delta=tuple(y-x for x,y in zip(a,b))
            l2=sum(v*v for v in delta)
            if l2<1e-18:
                continue
            candidates=[(0.,index[a])]
            for p in points:
                if p==a or p==b:
                    continue
                t=sum((p[k]-a[k])*delta[k] for k in range(3))/l2
                if 1e-9<t<1-1e-9 and sum((a[k]+t*delta[k]-p[k])**2 for k in range(3))<1e-14:
                    candidates.append((t,index[p]))
            face.extend(i for _,i in sorted(candidates))
        if len(set(face))<3:
            raise ValueError('Collapsed roof face')
        faces.append(tuple(face))
    edges=defaultdict(list)
    for fi,face in enumerate(faces):
        for a,b in zip(face,face[1:]+face[:1]):
            edges[tuple(sorted((a,b)))].append((fi,a,b))
    if any(len(v)>2 for v in edges.values()):
        raise ValueError('Overlapping roof patches')
    return points,faces,edges


def _line_span(poly,axis,value):
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da,db=a[axis]-value,b[axis]-value
        if abs(da)<1e-8:
            result.append(a[1-axis])
        if da*db<0:
            result.append(lerp(a,b,da/(da-db))[1-axis])
    return (min(result),max(result)) if len(result)>=2 else None


def roof_join_kind(points,patches,users):
    if len(users)!=2:
        return 'edge'
    p,q=(patches[u[0]] for u in users)
    if sum(abs(x-y) for x,y in zip(p.plane,q.plane))<1e-6:
        return 'coplanar'
    slope_sum=0.
    for patch,(_,a,b) in zip((p,q),users):
        dx,dy=points[b][0]-points[a][0],points[b][1]-points[a][1]
        slope_sum+=(-dy*patch.plane[0]+dx*patch.plane[1])/math.hypot(dx,dy)
    return 'ridge' if slope_sum<0 else 'valley'


def _valley_clearances(points,patches,edges):
    clearances=defaultdict(list)
    for users in edges.values():
        if roof_join_kind(points,patches,users)!='valley':
            continue
        for fi,a,b in users:
            p,q=points[a],points[b]
            dx,dy=q[0]-p[0],q[1]-p[1]
            clearances[fi].append((-dy,dx,dy*p[0]-dx*p[1]-.065*math.hypot(dx,dy)))
    return clearances


@dataclass
class Shingle:
    poly: list
    plane: tuple
    source: int
    row: int
    bay: int
    axis: int
    direction: int
    eave_coord: float
    course_start: float
    course_end: float
    u0: float
    u1: float
    material: str
    repair: bool
    butt: float
    tilt: float
    exposed_end: float = 0.

    def height(self,x,y):
        t=self.direction*((x,y)[self.axis]-self.eave_coord)
        lip=1-(t-self.course_start)/(self.course_end-self.course_start)
        u=(x,y)[1-self.axis]
        a,b,c=self.plane
        return a*x+b*y+c+.033+self.butt*lip+self.tilt*(u-(self.u0+self.u1)*.5)


def shingle_layout(plan,patches=None,topology=None):
    """Variable-width, lapped courses on resolved slopes; bounded eave repairs.

    The course stream is keyed to the original roof slope, not its clipped
    fragments, so valleys and coplanar partition edges cannot scramble the rows.
    """
    patches=roof_faces(plan) if patches is None else patches
    points,faces,edges=roof_topology(patches) if topology is None else topology
    clearances=_valley_clearances(points,patches,edges)
    detail=plan.settings.detail
    cover=getattr(getattr(plan,'style',None),'roof_cover','SHINGLE')
    cover_scale={'SHINGLE':1.,'SLATE':1.1,'CLAY':1.15,'REED':1.5}[cover]
    exposure={'HIGH':.30,'MEDIUM':.44,'LOW':.85}[detail]*cover_scale
    width={'HIGH':.205,'MEDIUM':.32,'LOW':.67}[detail]*cover_scale
    step=exposure/math.sqrt(1+plan.slope**2)
    # Shingles need headlap, not separated rectangular plates on a bare deck.
    # Three-course coverage keeps the lower courses behind each open side joint.
    overlap=step*2.2
    output=[]
    for pi,patch in enumerate(patches):
        axis=1 if abs(patch.plane[1])>1e-8 else 0
        across=1-axis
        direction=1 if patch.plane[axis]>0 else -1
        rect=plan.rects[patch.source]
        eave=(rect[axis]-plan.settings.overhang if direction>0 else rect[axis+2]+plan.settings.overhang)
        source_lo=rect[across]-plan.settings.overhang
        source_hi=rect[across+2]+plan.settings.overhang
        max_t=max(direction*(p[axis]-eave) for p in patch.poly)
        min_t=min(direction*(p[axis]-eave) for p in patch.poly)
        cohort=plan.rng(f'roof.eave_repair.{patch.source}.{direction}')
        # A short failed eave board can require replacing nearby shingle butts.
        repaired=cohort.random()<.34
        repair_u=cohort.uniform(source_lo+.2,source_hi-.2)
        row=-2
        t=-2*step
        course_rng=plan.rng(f'roof.courses.{patch.source}.{direction}')
        while t<=max_t+1e-7:
            advance=step*course_rng.uniform(.96,1.04)
            end=t+advance+overlap
            if end>=min_t:
                rng=plan.rng(f'roof.shingles.{patch.source}.{direction}.{row}')
                u=source_lo-width*(.35 if row%2 else .85)-rng.uniform(0,.12)*width
                bay=0
                while u<source_hi:
                    span=width*rng.uniform(.76,1.24)
                    u0,u1=u+.002,u+span-.002
                    upper_taper=min(.012,span*.045) if cover=='SHINGLE' else 0.
                    # Split shingles narrow towards their concealed heads.
                    local=[(u0,t),(u1,t),(u1-upper_taper,end),(u0+upper_taper,end)]
                    poly=[((u,eave+direction*v) if axis==1 else (eave+direction*v,u)) for u,v in local]
                    if area(poly)<0:
                        poly.reverse()
                    for a,b,c in inequalities(patch.poly)+clearances[pi]:
                        poly=clip(poly,a,b,c)
                        if not poly:
                            break
                    repair=repaired and 0<=row<3 and abs((u0+u1)*.5-repair_u)<(.46-row*.10)
                    shade=rng.random()
                    material='roof_patch' if repair else 'roof_dark' if shade<.17 else 'roof_worn' if shade>.86 else 'roof'
                    butt,tilt=rng.uniform(.019,.021),rng.uniform(-.004,.004)
                    if cover=='SLATE': butt*=.45
                    elif cover=='REED': butt*=1.8
                    if poly and area(poly)>.0002:
                        output.append(Shingle(poly,patch.plane,patch.source,row,bay,axis,direction,eave,t,end,u0,u1,material,repair,
                                              butt,tilt,t+advance))
                    u+=span
                    bay+=1
            t+=advance
            row+=1
    return output


def _finish_piece(buffer,shingle,poly,bend_a=0.,bend_c=0.,efficient=False):
    top=[(x,y,shingle.height(x,y)+bend_a*(x,y)[1-shingle.axis]+bend_c) for x,y in poly]
    if not efficient:
        buffer.extrude(top,(0,0,-.023))
        return
    # The weather deck is closed; this is explicitly open render-detail skin.
    # Hidden headlap, bottoms and buried side walls are not exported as solids.
    vertices=list(top)
    faces=[tuple(range(len(top)))]
    for i,p in enumerate(poly):
        j=(i+1)%len(poly)
        q=poly[j]
        t0=shingle.direction*(p[shingle.axis]-shingle.eave_coord)
        t1=shingle.direction*(q[shingle.axis]-shingle.eave_coord)
        if abs(t0-shingle.course_start)<1e-6 and abs(t1-shingle.course_start)<1e-6:
            n=len(vertices)
            vertices.extend([(top[i][0],top[i][1],top[i][2]-.023),
                             (top[j][0],top[j][1],top[j][2]-.023)])
            faces.append((i,n,n+1,j))
    buffer.indexed(vertices,faces)


def _build_cover_piece(buffer,shingle,cover,efficient,detail):
    poly=shingle.poly
    if efficient:
        # Keep only the exposed course; a continuous bedding skin represents
        # the concealed overlapping heads seen through millimetre side joints.
        axis=shingle.axis
        a,b=(shingle.direction,0) if axis==0 else (0,shingle.direction)
        c=-shingle.direction*shingle.eave_coord-shingle.exposed_end
        poly=clip(poly,-a,-b,-c)
        if not poly or area(poly)<.0002:
            return
    if cover in ('SHINGLE','SLATE') or detail=='LOW':
        _finish_piece(buffer,shingle,poly,efficient=efficient)
        return
    # Original lofted clay pans / reed bundles, evaluated on the exact slope.
    # Three bounded planar strips approximate the curved cross-section and are
    # clipped at valleys using the same footprint as all other roof details.
    across=1-shingle.axis
    span=shingle.u1-shingle.u0
    amplitude=.022 if cover=='CLAY' else .035
    values=[0.,amplitude,amplitude,0.]
    for k in range(3):
        lo=shingle.u0+span*k/3
        hi=shingle.u0+span*(k+1)/3
        aa,bb=(1,0) if across==0 else (0,1)
        section=clip(clip(poly,aa,bb,-lo),-aa,-bb,hi)
        if not section:
            continue
        slope=(values[k+1]-values[k])/(hi-lo)
        _finish_piece(buffer,shingle,section,slope,values[k]-slope*lo,efficient)


def build_roof(plan):
    patches=roof_faces(plan)
    points,faces,edges=roof_topology(patches)
    deck=MeshBuffer('Continuous roof deck','timber','roof')
    n=len(points)
    verts=points+[(x,y,z-.12) for x,y,z in points]
    solids=list(faces)+[tuple(i+n for i in reversed(face)) for face in faces]
    for users in edges.values():
        if len(users)==1:
            _,a,b=users[0]
            solids.append((a,a+n,b+n,b))
    deck.indexed(verts,solids)
    efficient=plan.settings.geometry_mode=='EFFICIENT'
    cover=plan.style.roof_cover
    tiles={key:MeshBuffer(name,key,'roof') for key,name in [
        ('roof','Split oak shingle courses'),('roof_dark','Seasoned shingle cohorts'),
        ('roof_worn','Exposed shingle butts'),('roof_patch','Replacement shingle cohort')]}
    if efficient:
        for buffer in tiles.values(): buffer.topology='SURFACE'
    bedding=MeshBuffer('Concealed roof course bedding','roof_dark','roof',topology='SURFACE')
    if efficient:
        for patch in patches:
            bedding.face([(x,y,patch.height(x,y)+.029) for x,y in patch.poly])
    for shingle in shingle_layout(plan,patches,(points,faces,edges)):
        _build_cover_piece(tiles[shingle.material],shingle,cover,efficient,detail=plan.settings.detail)
    ridge=MeshBuffer('Overlapping ridge caps','roof_dark','roof')
    trim=MeshBuffer('Ridge caps and valley flashing','iron','roof')
    fascia=MeshBuffer('Roof edge fascia','timber','roof')
    rafters=MeshBuffer('Supported roof rafters','timber','roof')
    detail=plan.settings.detail
    for patch in patches:
        axis=1 if abs(patch.plane[1])>1e-8 else 0
        across=1-axis
        amin,amax=min(p[across] for p in patch.poly),max(p[across] for p in patch.poly)
        spacing=.64 if detail=='HIGH' else 1.0
        for col in range(math.ceil(amin/spacing),math.floor(amax/spacing)+1):
            u=col*spacing
            span=_line_span(patch.poly,across,u)
            if not span or span[1]-span[0]<.2:
                continue
            ends=[]
            for value in span:
                x,y=(u,value) if axis==1 else (value,u)
                ends.append((x,y,patch.height(x,y)-.22))
            rafters.beam(*ends,.12,.16)
    for key,users in edges.items():
        a,b=(points[i] for i in key)
        length=math.dist(a,b)
        if length<.05:
            continue
        kind=roof_join_kind(points,patches,users)
        if kind=='edge':
            method=fascia.chamfered_beam if detail!='LOW' else fascia.beam
            # The roof falls across the complete board section, not just its
            # centreline. Keep even the outer top arris below the supporting
            # roof plane; a fixed centre offset let brown timber breach tiles.
            fascia_drop=.02+.11*math.sqrt(1+plan.slope**2)+.065*plan.slope
            method((a[0],a[1],a[2]-fascia_drop),(b[0],b[1],b[2]-fascia_drop),.13,.22)
        elif kind=='ridge':
            dx,dy=b[0]-a[0],b[1]-a[1]
            xy_length=math.hypot(dx,dy)
            across=(-dy/xy_length,dx/xy_length)
            pieces=max(1,math.ceil(length/.39))
            for i in range(pieces):
                start=lerp(a,b,i/pieces)
                finish=lerp(a,b,min(1,(i+1)/pieces+.012/length))
                # Use each adjacent plane, including diagonal hip ridges. A
                # gable-only cross-slope approximation buries caps on hip roofs.
                for fi,ea,eb in users:
                    va,vb=points[ea],points[eb]
                    vx,vy=vb[0]-va[0],vb[1]-va[1]
                    vl=math.hypot(vx,vy)
                    inward=(-vy/vl*.145,vx/vl*.145)
                    xy=[start[:2],finish[:2],(finish[0]+inward[0],finish[1]+inward[1]),
                        (start[0]+inward[0],start[1]+inward[1])]
                    poly=[(x,y,patches[fi].height(x,y)+.083) for x,y in xy]
                    ridge.extrude(poly,(0,0,-.025))
        elif kind=='valley':
            # Folded valley aprons lie beneath cut shingle margins on both slopes.
            for fi,ea,eb in users:
                p,q=points[ea],points[eb]
                dx,dy=q[0]-p[0],q[1]-p[1]
                l=math.hypot(dx,dy)
                inward=(-dy/l*.13,dx/l*.13)
                xy=[p[:2],q[:2],(q[0]+inward[0],q[1]+inward[1]),(p[0]+inward[0],p[1]+inward[1])]
                trim.extrude([(x,y,patches[fi].height(x,y)+.013) for x,y in xy],(0,0,-.007))
    return [b for b in (deck,bedding,*tiles.values(),ridge,trim,fascia,rafters) if b.faces]
