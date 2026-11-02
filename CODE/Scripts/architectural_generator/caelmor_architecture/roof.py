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
    tiles=MeshBuffer('Split oak shingle courses','roof','roof')
    repair=MeshBuffer('Replacement shingle cohort','roof_patch','roof')
    ridge=MeshBuffer('Overlapping ridge caps','roof','roof')
    trim=MeshBuffer('Ridge caps and valley flashing','iron','roof')
    fascia=MeshBuffer('Roof edge fascia','timber_light','roof')
    rafters=MeshBuffer('Supported roof rafters','timber','roof')
    rng=plan.rng('roof.repair')
    repair_center=(rng.uniform(.15,.85)*plan.settings.width,rng.uniform(.1,.35)*plan.settings.depth)
    detail=plan.settings.detail
    step=.29 if detail=='HIGH' else .45 if detail=='MEDIUM' else .9
    width=.23 if detail=='HIGH' else .36 if detail=='MEDIUM' else .7
    for pi,patch in enumerate(patches):
        # Rows perpendicular to downhill direction, laid on the roof plane.
        axis=1 if abs(patch.plane[1])>1e-8 else 0
        across=1-axis
        lo,hi=min(p[axis] for p in patch.poly),max(p[axis] for p in patch.poly)
        amin,amax=min(p[across] for p in patch.poly),max(p[across] for p in patch.poly)
        for row in range(math.floor(lo/step),math.ceil(hi/step)):
            v0,v1=row*step,(row+1)*step-.009
            for col in range(math.floor(amin/width)-1,math.ceil(amax/width)+1):
                u0=col*width+(row%2)*width*.5
                u1=u0+width-.008
                if axis==1:
                    poly=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
                else:
                    poly=[(v0,u0),(v1,u0),(v1,u1),(v0,u1)]
                for a,b,c in inequalities(patch.poly):
                    poly=clip(poly,a,b,c)
                    if not poly:
                        break
                if not poly or area(poly)<.0004:
                    continue
                cx,cy=sum(p[0] for p in poly)/len(poly),sum(p[1] for p in poly)/len(poly)
                replacement=((cx-repair_center[0])**2/2.0+(cy-repair_center[1])**2/.7<1)
                out=repair if replacement else tiles
                # A small consistent raised butt gives courses real relief.
                sign=1 if patch.plane[axis]>0 else -1
                top=[(x,y,patch.height(x,y)+.052+.018*((((x,y)[axis]-v0)/step) if sign<0 else (v1-(x,y)[axis])/step)) for x,y in poly]
                out.extrude(top,(0,0,-.028))
        # Structural rafters follow each visible slope and stop at resolved valleys.
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
        if len(users)==1:
            fascia.beam((a[0],a[1],a[2]-.09),(b[0],b[1],b[2]-.09),.13,.22)
        elif len(users)==2:
            p,q=(patches[u[0]] for u in users)
            if sum(abs(x-y) for x,y in zip(p.plane,q.plane))<1e-6:
                continue
            # Convex slope joins get rounded ridge tiles; concave joins metal valleys.
            slope_sum=0
            for patch,(_,ea,eb) in zip((p,q),users):
                va,vb=points[ea],points[eb]
                dx,dy=vb[0]-va[0],vb[1]-va[1]
                l=math.hypot(dx,dy)
                slope_sum+=(-dy*patch.plane[0]+dx*patch.plane[1])/l
            aa,bb=(a[0],a[1],a[2]+.085),(b[0],b[1],b[2]+.085)
            if slope_sum<0:
                pieces=max(1,math.ceil(length/.38))
                for i in range(pieces):
                    ridge.cylinder(lerp(aa,bb,i/pieces),lerp(aa,bb,(i+1)/pieces),.105,8)
            else:
                trim.beam(aa,bb,.19,.028)
    return [b for b in (deck,tiles,repair,ridge,trim,fascia,rafters) if b.faces]
