"""Headless authoring API and release-gate geometry diagnostics."""
import hashlib
import json
import math
from collections import Counter
from .model import Settings, make_plan
from .facade import build_facades
from .roof import build_roof, roof_faces, roof_topology
from .geometry import area, cross, sub, dot

TOOL_REVISION='0.2.0'


def generate(settings):
    plan=make_plan(settings)
    buffers=build_facades(plan)+build_roof(plan)
    return plan,buffers


def geometry_hash(buffers):
    digest=hashlib.sha256()
    for b in buffers:
        digest.update(json.dumps((b.name,b.material,b.layer,b.vertices,b.faces),separators=(',',':')).encode())
    return digest.hexdigest()


def validate(plan,buffers):
    errors=[]
    triangles=0
    for b in buffers:
        if not b.vertices or not b.faces:
            errors.append(f'{b.name}: empty mesh')
            continue
        if any(not math.isfinite(c) for p in b.vertices for c in p):
            errors.append(f'{b.name}: nonfinite coordinates')
        edge_counts=Counter()
        edge_direction=Counter()
        roots=list(range(len(b.vertices)))
        def root(v):
            while roots[v]!=v:
                roots[v]=roots[roots[v]]
                v=roots[v]
            return v
        volumes=[]
        for face in b.faces:
            triangles+=len(face)-2
            if len(face)<3 or len(set(face))!=len(face) or any(i<0 or i>=len(b.vertices) for i in face):
                errors.append(f'{b.name}: invalid face indices')
                continue
            normal=(0.,0.,0.)
            for i in range(1,len(face)-1):
                v=cross(sub(b.vertices[face[i]],b.vertices[face[0]]),sub(b.vertices[face[i+1]],b.vertices[face[0]]))
                normal=tuple(x+y for x,y in zip(normal,v))
            if dot(normal,normal)<1e-16:
                errors.append(f'{b.name}: zero area face')
            for v in face[1:]:
                roots[root(v)]=root(face[0])
            volume=0.
            for i in range(1,len(face)-1):
                volume+=dot(b.vertices[face[0]],cross(b.vertices[face[i]],b.vertices[face[i+1]]))/6
            volumes.append((face[0],volume))
            for a,c in zip(face,face[1:]+face[:1]):
                edge_counts[tuple(sorted((a,c)))]+=1
                edge_direction[(a,c)]+=1
        if any(v!=2 for v in edge_counts.values()):
            errors.append(f'{b.name}: nonmanifold solid edges')
        if any(edge_direction[(a,c)]!=edge_direction[(c,a)] for a,c in edge_counts):
            errors.append(f'{b.name}: inconsistent winding')
        component_volumes=Counter()
        for v,volume in volumes:
            component_volumes[root(v)]+=volume
        if any(v<=1e-10 for v in component_volumes.values()):
            errors.append(f'{b.name}: inward or zero-volume solid component')
        # Section-aware construction must remain below the roof underside. A
        # centreline-only eave check missed posts/pegs outside the wall face.
        is_frame=(b.material.startswith('timber') and b.layer in ('structure','details'))
        if is_frame:
            samples=list(b.vertices)
            samples.extend(tuple((x+y)*.5 for x,y in zip(b.vertices[a],b.vertices[c]))
                           for a,c in edge_counts)
            samples.extend(tuple(sum(b.vertices[i][axis] for i in face)/len(face) for axis in range(3))
                           for face in b.faces)
            excess=max((z-(plan.roof_height(x,y)-.12) for x,y,z in samples),default=0.)
            if excess>1e-5:
                errors.append(f'{b.name}: timber crosses roof underside by {excess:.6f}m')
    patches=roof_faces(plan)
    roof_topology(patches)
    # Every convex patch vertex and centroid must lie on the analytic envelope.
    for p in patches:
        sample=p.poly+[(sum(x for x,y in p.poly)/len(p.poly),sum(y for x,y in p.poly)/len(p.poly))]
        if any(abs(p.height(x,y)-plan.roof_height(x,y))>1e-5 for x,y in sample):
            errors.append('Roof patch disagrees with weather envelope')
    return {'valid':not errors,'errors':errors,'objects':len(buffers),
            'vertices':sum(len(b.vertices) for b in buffers),'triangles':triangles,
            'materials':len(set(b.material for b in buffers)),
            'footprint_area':round(area(plan.outline),4),
            'roof_projected_area':round(sum(area(p.poly) for p in patches),4),
            'geometry_hash':geometry_hash(buffers),'tool_revision':TOOL_REVISION}
