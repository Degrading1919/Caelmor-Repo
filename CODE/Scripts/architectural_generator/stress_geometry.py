"""Independent seeded parameter sweep, roof coverage and overlap release gate."""
import math
import random
import time
from caelmor_architecture.engine import generate, validate
from caelmor_architecture.model import Settings
from caelmor_architecture.roof import roof_faces, roof_sources
from caelmor_architecture.geometry import area, clip, inequalities
from caelmor_architecture.facade import frame_layout


def structural_gate(plan):
    """Independent semantic sweep in addition to closed-mesh validation."""
    post_width=.22 if plan.settings.function in ('BARN','GRAIN_STORE') else .19
    for index,edge in enumerate(plan.edges):
        schedule=frame_layout(plan,index,edge)
        posts=schedule['principal_posts']
        if any(b-a<.65-1e-6 for a,b in zip(posts,posts[1:])):
            raise AssertionError(('principal post spacing',index,posts))
        for post in posts:
            if any(post+post_width*.5>o['s0']+1e-6 and post-post_width*.5<o['s1']-1e-6
                   for o in schedule['openings']):
                raise AssertionError(('post cuts opening',index,post))
        for brace in schedule['braces']:
            # Independent interval/slab clipping of the full brace body in (s,z).
            for opening in schedule['openings']:
                half=brace['width']*.5
                lower,upper=0.,1.
                for a,b,lo,hi in [
                    (brace['s0'],brace['s1'],opening['s0']-half,opening['s1']+half),
                    (brace['z0'],brace['z1'],opening['z0']-half,opening['z1']+half)]:
                    delta=b-a
                    if abs(delta)<1e-10:
                        if not lo<=a<=hi:
                            lower,upper=1.,0.
                            break
                    else:
                        ts=sorted(((lo-a)/delta,(hi-a)/delta))
                        lower,upper=max(lower,ts[0]),min(upper,ts[1])
                if lower<=upper:
                    raise AssertionError(('brace cuts opening',index,brace,opening))


def run(count=80):
    rng=random.Random(7447)
    start=time.monotonic()
    for n in range(count):
        footprint=('RECT','L','T','U')[n%4]
        width,depth=rng.uniform(10,24),rng.uniform(4,16)
        ww=rng.uniform(2.5,min(depth,(width-2)/2))
        settings=Settings(seed=n,footprint=footprint,width=width,depth=depth,wing_width=ww,
            wing_depth=rng.uniform(2.5,12),floors=1+n%3,pitch=rng.uniform(30,60),
            overhang=rng.uniform(.2,.75),detail='LOW',window_density=rng.uniform(.4,1.5),
            function=('FARMHOUSE','BARN','GRAIN_STORE','MILLER','INN')[n%5])
        plan,buffers=generate(settings)
        report=validate(plan,buffers)
        if not report['valid']:
            raise AssertionError((n,settings,report['errors']))
        structural_gate(plan)
        patches=roof_faces(plan)
        # Independent rectangle-union projected area, separate from patch clipping.
        sources=roof_sources(plan)
        xs=sorted(set(x for q in sources for x,y in q.poly))
        ys=sorted(set(y for q in sources for x,y in q.poly))
        expected=0.
        for x0,x1 in zip(xs,xs[1:]):
            for y0,y1 in zip(ys,ys[1:]):
                x,y=(x0+x1)/2,(y0+y1)/2
                if math.isfinite(plan.roof_height(x,y)):
                    expected+=(x1-x0)*(y1-y0)
        actual=sum(area(p.poly) for p in patches)
        if abs(actual-expected)>1e-5:
            raise AssertionError((n,'roof coverage',actual,expected))
        for i,patch in enumerate(patches):
            for other in patches[i+1:]:
                overlap=patch.poly
                for a,b,c in inequalities(other.poly):
                    overlap=clip(overlap,a,b,c)
                if overlap and area(overlap)>1e-6:
                    raise AssertionError((n,'overlapping visible roof patches'))
    return {'cases':count,'seed':7447,'seconds':round(time.monotonic()-start,2),'valid':True}


if __name__=='__main__':
    print(run())
