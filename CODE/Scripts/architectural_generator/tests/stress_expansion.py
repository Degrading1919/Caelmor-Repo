"""Bounded 96-case expansion stress gate with geometry/source-hash evidence."""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from caelmor_architecture.engine import generate, validate
from caelmor_architecture.facade import frame_layout
from caelmor_architecture.geometry import area, clip, inequalities
from caelmor_architecture.model import Settings, TYPE_SPECS
from caelmor_architecture.roof import roof_faces, roof_sources


def source_sha256():
    digest=hashlib.sha256()
    paths=sorted((ROOT/'caelmor_architecture').glob('*.py'))+[Path(__file__).resolve()]
    for path in paths:
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b'\0')
        digest.update(path.read_bytes())
        digest.update(b'\0')
    return digest.hexdigest()


def _segment_hits_rect(brace,bounds,margin):
    x0,z0,x1,z1=brace['s0'],brace['z0'],brace['s1'],brace['z1']
    t0,t1=0.0,1.0
    for p,q,lo,hi in ((x0,x1-x0,bounds['s0']-margin,bounds['s1']+margin),
                      (z0,z1-z0,bounds['z0']-margin,bounds['z1']+margin)):
        if abs(q)<1e-10:
            if p<lo or p>hi:
                return False
            continue
        ta,tb=sorted(((lo-p)/q,(hi-p)/q))
        t0,t1=max(t0,ta),min(t1,tb)
        if t0>t1:
            return False
    return True


def structural_gate(plan):
    """Independent post/brace/plate checks use full assembly exclusion bounds.

    Raw inter-post spans are diagnostics only: they can include complete
    openings whose jambs carry their local loads. Timber wall support gaps are
    measured only over remaining solid wall; masonry walls carry their own
    course loads and do not rely on exposed post spacing.
    """
    fn=str(plan.settings.function).upper()
    post_width=.22 if fn in ('BARN','GRAIN_STORE') else .19
    raw_spans=[]
    solid_gaps=[]
    for edge_index,edge in enumerate(plan.edges):
        schedule=frame_layout(plan,edge_index,edge)
        openings=schedule['openings']
        raw_spans.extend({'edge_index':edge_index,**span}
                         for span in schedule['unsupported_spans'])
        for post in schedule['principal_posts']:
            for opening in openings:
                bounds=opening['assembly_bounds']
                if post+post_width*.5>bounds['s0']+1e-6 and post-post_width*.5<bounds['s1']-1e-6:
                    raise AssertionError(('principal post overlaps opening assembly',edge_index,post,opening))
        for brace in schedule['braces']:
            for opening in openings:
                if _segment_hits_rect(brace,opening['assembly_bounds'],brace['width']*.5+.035):
                    raise AssertionError(('brace overlaps opening assembly',edge_index,brace,opening))
        for opening in openings:
            bounds=opening['assembly_bounds']
            for index,plate_z in enumerate(schedule['plates']):
                # Plates explicitly stop at door openings when their height
                # enters that opening; do not count the intentional gap as a collision.
                if opening['kind']=='door' and plate_z<=opening['z1']+.05:
                    continue
                half=(.19 if index==len(schedule['plates'])-1 else .16)*.5
                if not (bounds['z1']<=plate_z-half+1e-5 or bounds['z0']>=plate_z+half-1e-5):
                    raise AssertionError(('opening assembly intersects plate',edge_index,opening,
                                          {'z':plate_z,'half_thickness':half,'index':index}))
        if str(plan.style.construction).upper() not in ('RUBBLE','ASHLAR'):
            # Remove the complete opening columns; their framed jambs/headers
            # support the aperture itself. Check the wall material left between.
            blocked=[]
            for opening in openings:
                bounds=opening['assembly_bounds']
                lo=max(0.0,bounds['s0']);hi=min(schedule['length'],bounds['s1'])
                if hi>lo:
                    blocked.append((lo,hi))
            merged=[]
            for lo,hi in sorted(blocked):
                if merged and lo<=merged[-1][1]:
                    merged[-1]=(merged[-1][0],max(merged[-1][1],hi))
                else:
                    merged.append((lo,hi))
            solid=[];cursor=0.0
            for lo,hi in merged:
                if lo>cursor:
                    solid.append((cursor,lo))
                cursor=max(cursor,hi)
            if cursor<schedule['length']:
                solid.append((cursor,schedule['length']))
            for lo,hi in solid:
                supports=[lo]+[p for p in schedule['principal_posts'] if lo+1e-5<p<hi-1e-5]+[hi]
                for left,right in zip(supports,supports[1:]):
                    if right-left>4.301:
                        solid_gaps.append({'edge_index':edge_index,'s0':left,'s1':right,
                                           'length':right-left})
    if solid_gaps:
        raise AssertionError(('unsupported solid wall span',solid_gaps))
    return {'raw_interpost_spans':raw_spans,'solid_wall_support_gaps':solid_gaps}


def roof_gate(plan):
    patches=roof_faces(plan)
    sources=roof_sources(plan)
    xs=sorted(set(x for source in sources for x,y in source.poly))
    ys=sorted(set(y for source in sources for x,y in source.poly))
    expected=0.0
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            if math.isfinite(plan.roof_height((x0+x1)*.5,(y0+y1)*.5)):
                expected+=(x1-x0)*(y1-y0)
    actual=sum(area(p.poly) for p in patches)
    if abs(actual-expected)>1e-5:
        raise AssertionError(('roof coverage mismatch',actual,expected))
    for i,patch in enumerate(patches):
        for other in patches[i+1:]:
            overlap=patch.poly
            for a,b,c in inequalities(other.poly):
                overlap=clip(overlap,a,b,c)
            if overlap and area(overlap)>1e-6:
                raise AssertionError(('overlapping roof patches',i))
    return {'projected_area':actual,'expected_area':expected,'patches':len(patches)}


def _matrix_settings():
    regions=('LOWMARK','THORNFELL','MIRE','EMBERHOLT')
    types=tuple(TYPE_SPECS)
    wealth=('MODEST','ESTABLISHED','AFFLUENT')
    craft=('ROUGH','STANDARD','FINE')
    detail=('LOW','MEDIUM','HIGH')
    modes=('SOLID','EFFICIENT')
    for n in range(80):
        region=regions[n//20]
        function=types[n%20]
        yield Settings(seed=31000+n,function=function,region=region,use_grammar=True,
            wealth=wealth[n%3],craftsmanship=craft[(n//3)%3],
            maintenance=((n%5)/4),age=(n*17)%251,detail=detail[(n//2)%3],
            geometry_mode=modes[(n//5)%2],window_density=.65+(n%6)*.15)


def _manual_settings():
    footprints=('RECT','L','T','U')
    roofs=('GABLE','HIP')
    pitches=(30.0,60.0)
    for n,(footprint,roof,pitch) in enumerate(
            ( (f,r,p) for f in footprints for r in roofs for p in pitches )):
        yield Settings(seed=42000+n,function=('FARMHOUSE','BARN','GATEHOUSE','BOATHOUSE')[n%4],
            region=('LOWMARK','THORNFELL','MIRE','EMBERHOLT')[n%4],
            footprint=footprint,width=14.0,depth=10.0,wing_width=3.0,wing_depth=4.0,
            floors=2,floor_height=2.8,pitch=pitch,overhang=.55,detail='HIGH',
            window_density=1.0,use_grammar=False,roof_style=roof,
            geometry_mode='EFFICIENT' if n%2 else 'SOLID')


def _case(settings,index,phase,determinism=False):
    started=time.perf_counter()
    row={'index':index,'phase':phase,'requested_settings':asdict(settings),'errors':[]}
    try:
        plan,buffers=generate(settings)
        report=validate(plan,buffers)
        if not report['valid']:
            raise AssertionError(('engine validation',report['errors']))
        row['structural_diagnostics']=structural_gate(plan)
        roof=row['roof']=roof_gate(plan)
        row['effective_settings']=asdict(plan.settings)
        row['geometry_hash']=report['geometry_hash']
        row['validation']={'valid':report['valid'],'vertices':report['vertices'],
                           'triangles':report['triangles'],'topology':report['topology']}
        if determinism:
            repeat_plan,repeat_buffers=generate(settings)
            repeat=validate(repeat_plan,repeat_buffers)
            if not repeat['valid'] or repeat['geometry_hash']!=report['geometry_hash']:
                raise AssertionError(('nondeterministic regeneration',report['geometry_hash'],
                                      repeat.get('geometry_hash'),repeat.get('errors')))
            row['determinism']={'repeat_hash':repeat['geometry_hash'],'matched':True}
    except Exception as exc:
        row['errors'].append(repr(exc))
    row['seconds']=round(time.perf_counter()-started,4)
    row['passed']=not row['errors']
    return row


def run(write=True):
    started=time.perf_counter()
    started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    cases=[]
    for i,settings in enumerate(_matrix_settings()):
        cases.append(_case(settings,i,'region_type',determinism=i in (0,39,79)))
    offset=len(cases)
    for j,settings in enumerate(_manual_settings()):
        cases.append(_case(settings,offset+j,'manual_extreme',determinism=j in (0,15)))
    report={'schema':'caelmor.expansion-stress.v1','seed':7447,
            'requested_cases':96,'completed_cases':len(cases),
            'started_utc':started_utc,
            'elapsed_seconds':round(time.perf_counter()-started,3),
            'source_sha256':source_sha256(),'passed':all(c['passed'] for c in cases),
            'failure_count':sum(not c['passed'] for c in cases),
            'cases':cases}
    if write:
        path=ROOT/'evidence'/'expansion_stress.json'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        report['report_path']=str(path)
    return report


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    if not result['passed']:
        sys.exit(1)
