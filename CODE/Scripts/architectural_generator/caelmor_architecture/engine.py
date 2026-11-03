"""Headless authoring API and release-gate geometry diagnostics."""
import hashlib
import json
import math
from collections import Counter
from dataclasses import replace
import time
from .model import Settings, make_plan
from .facade import build_facades
from .roof import build_roof, roof_faces, roof_topology
from .geometry import area, cross, sub, dot

TOOL_REVISION='0.9.0'


def generate(settings):
    if settings.world_aware:
        from .world import generate as generate_world
        return generate_world(settings)
    plan=make_plan(settings)
    buffers=build_facades(plan)+build_roof(plan)
    return plan,buffers


def geometry_hash(buffers):
    digest=hashlib.sha256()
    for b in buffers:
        digest.update(json.dumps((b.name,b.material,b.layer,b.topology,b.roof_envelope,b.structural_role,b.support_surface,b.vertices,b.faces),separators=(',',':')).encode())
    return digest.hexdigest()


def validate(plan,buffers):
    if hasattr(plan,'world_zones'):
        from .world import validate as validate_world
        result=validate_world(plan,buffers,validate)
        result.update(geometry_hash=geometry_hash(buffers),tool_revision=TOOL_REVISION)
        return result
    errors=[]
    triangles=0
    for b in buffers:
        solid=b.topology=='SOLID'
        if b.topology not in ('SOLID','SURFACE'):
            errors.append(f'{b.name}: invalid topology role')
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
        if solid and any(v!=2 for v in edge_counts.values()):
            errors.append(f'{b.name}: nonmanifold solid edges')
        if any(edge_direction[(a,c)]!=edge_direction[(c,a)] for (a,c),count in edge_counts.items() if count==2):
            errors.append(f'{b.name}: inconsistent winding')
        component_volumes=Counter()
        for v,volume in volumes:
            component_volumes[root(v)]+=volume
        if solid and any(v<=1e-10 for v in component_volumes.values()):
            errors.append(f'{b.name}: inward or zero-volume solid component')
        # Section-aware construction must remain below the roof underside. A
        # centreline-only eave check missed posts/pegs outside the wall face.
        is_access=b.structural_role=='exterior_access'
        if is_access:
            support=b.support_surface
            if not support:
                errors.append(f'{b.name}: exterior access has no declared supporting surface')
            else:
                a0,b0,c0=support['plane']
                xmin,ymin,xmax,ymax=support['bounds']
                maximum=support.get('max_height',1.2)
                for x,y,z in b.vertices:
                    floor=a0*x+b0*y+c0
                    if not (xmin-1e-4<=x<=xmax+1e-4 and ymin-1e-4<=y<=ymax+1e-4):
                        errors.append(f'{b.name}: access railing leaves its actual platform')
                        break
                    if not floor-.10<=z<=floor+maximum+1e-4:
                        errors.append(f'{b.name}: access railing has implausible support height')
                        break
        is_frame=(not is_access and b.material.startswith('timber') and b.layer in ('structure','details'))
        if is_frame:
            samples=list(b.vertices)
            samples.extend(tuple((x+y)*.5 for x,y in zip(b.vertices[a],b.vertices[c]))
                           for a,c in edge_counts)
            samples.extend(tuple(sum(b.vertices[i][axis] for i in face)/len(face) for axis in range(3))
                           for face in b.faces)
            if b.roof_envelope is None:
                ceiling=lambda x,y: plan.roof_height(x,y)-.12
                if b.structural_role=='mechanical':
                    # Waterwheels are intentionally weather-exposed. Samples
                    # inside the actual roof domain still obey deck clearance.
                    samples=[p for p in samples if math.isfinite(plan.roof_height(p[0],p[1]))]
            else:
                # A porch/gallery has its own authored, actual roof plane and
                # support footprint; it is not exempt from clearance checks.
                envelope=b.roof_envelope
                pa,pb,pc=envelope['plane']
                clearance=envelope.get('clearance',.12)
                ceiling=lambda x,y: pa*x+pb*y+pc-clearance
                bounds=envelope.get('bounds')
                if bounds and any(not (bounds[0]-1e-5<=x<=bounds[2]+1e-5 and bounds[1]-1e-5<=y<=bounds[3]+1e-5) for x,y,z in samples):
                    errors.append(f'{b.name}: structure leaves its declared canopy support')
            excess=max((z-ceiling(x,y) for x,y,z in samples),default=0.)
            if excess>1e-5:
                errors.append(f'{b.name}: timber crosses roof underside by {excess:.6f}m')
    patches=roof_faces(plan)
    roof_topology(patches)
    # Every convex patch vertex and centroid must lie on the analytic envelope.
    for p in patches:
        sample=p.poly+[(sum(x for x,y in p.poly)/len(p.poly),sum(y for x,y in p.poly)/len(p.poly))]
        if any(abs(p.height(x,y)-plan.roof_height(x,y))>1e-5 for x,y in sample):
            errors.append('Roof patch disagrees with weather envelope')
    layers={}
    for b in buffers:
        row=layers.setdefault(b.layer,{'vertices':0,'triangles':0,'buffers':0})
        row['vertices']+=len(b.vertices)
        row['triangles']+=sum(len(f)-2 for f in b.faces)
        row['buffers']+=1
    return {'valid':not errors,'errors':errors,'objects':len(buffers),
            'vertices':sum(len(b.vertices) for b in buffers),'triangles':triangles,
            'materials':len(set(b.material for b in buffers)),
            'footprint_area':round(area(plan.outline),4),
            'roof_projected_area':round(sum(area(p.poly) for p in patches),4),
            'geometry_hash':geometry_hash(buffers),'tool_revision':TOOL_REVISION,
            'topology':dict(Counter(b.topology for b in buffers)), 'layers':layers,
            'region':plan.settings.region,'context':plan.settings.context,
            'building_type':plan.settings.function,'roof_style':plan.settings.roof_style,
            'geometry_mode':plan.settings.geometry_mode,
            'roof_cover':plan.style.roof_cover,'construction':plan.style.construction}


def compare_geometry_modes(settings):
    """Measure actual authoring vs exposed-detail costs for the same plan."""
    result={}
    for mode in ('SOLID','EFFICIENT'):
        started=time.perf_counter()
        plan,buffers=generate(replace(settings,geometry_mode=mode))
        result[mode]=validate(plan,buffers)
        result[mode]['generation_validation_seconds']=round(time.perf_counter()-started,4)
    for metric in ('vertices','triangles'):
        before=result['SOLID'][metric]
        after=result['EFFICIENT'][metric]
        result[metric+'_reduction_percent']=round(100*(before-after)/before,2) if before else 0.
    return result
