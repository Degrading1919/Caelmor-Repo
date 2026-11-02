"""Semantic massing and deterministic Lowmark design inputs, independent of bpy."""
from dataclasses import dataclass
import math
import random
from .geometry import stable_seed, area

FUNCTIONS = ('FARMHOUSE','BARN','GRAIN_STORE','MILLER','INN')
FOOTPRINTS = ('RECT','L','T','U')


@dataclass
class Settings:
    seed: int = 17
    function: str = 'FARMHOUSE'
    footprint: str = 'L'
    width: float = 11.0
    depth: float = 7.0
    wing_width: float = 4.2
    wing_depth: float = 4.5
    floors: int = 2
    floor_height: float = 2.65
    pitch: float = 48.0
    overhang: float = .45
    detail: str = 'HIGH'
    window_density: float = 1.0

    def check(self):
        for name in ('width','depth','wing_width','wing_depth','floor_height','pitch','overhang','window_density'):
            if not math.isfinite(getattr(self,name)):
                raise ValueError(f'{name} must be finite')
        if self.function not in FUNCTIONS or self.footprint not in FOOTPRINTS or self.detail not in ('LOW','MEDIUM','HIGH'):
            raise ValueError('Unsupported function, footprint or detail')
        if not isinstance(self.seed,int) or not isinstance(self.floors,int) or not 1<=self.floors<=3:
            raise ValueError('Integer seed and 1–3 floors required')
        if not 6<=self.width<=24 or not 4<=self.depth<=16:
            raise ValueError('Width 6–24m and depth 4–16m required')
        if not 2.5<=self.wing_width<=self.width-.5 or not 2.5<=self.wing_depth<=12:
            raise ValueError('Wing must be at least 2.5m and narrower than main body')
        if self.footprint!='RECT' and self.wing_width>self.depth:
            raise ValueError('Wing width must not exceed main depth for continuous joined gables')
        if self.footprint=='U' and self.width-2*self.wing_width<2:
            raise ValueError('U courtyard must have at least 2m clearance; reduce wing width')
        if not 2.4<=self.floor_height<=3.8 or not 30<=self.pitch<=60 or not .2<=self.overhang<=.75:
            raise ValueError('Floor height 2.4–3.8m, roof pitch 30–60°, overhang .2–.75m required')
        if not .4<=self.window_density<=1.5:
            raise ValueError('Window density .4–1.5 required')


def rectangle_union_outline(rects):
    xs = sorted(set(v for r in rects for v in (r[0],r[2])))
    ys = sorted(set(v for r in rects for v in (r[1],r[3])))
    cells=set()
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            x,y=(xs[i]+xs[i+1])*.5,(ys[j]+ys[j+1])*.5
            if any(a<=x<=c and b<=y<=d for a,b,c,d,_ in rects):
                cells.add((i,j))
    edges={}
    for i,j in sorted(cells):
        a,b,c,d=(xs[i],ys[j]),(xs[i+1],ys[j]),(xs[i+1],ys[j+1]),(xs[i],ys[j+1])
        for neighbor,p,q in [((i,j-1),a,b),((i+1,j),b,c),((i,j+1),c,d),((i-1,j),d,a)]:
            if neighbor not in cells:
                edges[p]=q
    start=min(edges)
    outline=[start]
    p=edges[start]
    while p!=start:
        if len(outline)>len(edges):
            raise ValueError('Invalid disconnected footprint')
        outline.append(p)
        p=edges[p]
    result=[]
    for i,p in enumerate(outline):
        before,after=outline[i-1],outline[(i+1)%len(outline)]
        if abs((p[0]-before[0])*(after[1]-p[1])-(p[1]-before[1])*(after[0]-p[0]))>1e-8:
            result.append(p)
    if area(result)<=0:
        raise ValueError('Footprint winding invalid')
    return result


class Plan:
    def __init__(self,settings,rects):
        self.settings=settings
        self.rects=rects
        self.outline=rectangle_union_outline(rects)
        self.edges=list(zip(self.outline,self.outline[1:]+self.outline[:1]))
        self.eave=.45+settings.floors*settings.floor_height
        self.slope=math.tan(math.radians(settings.pitch))

    def rng(self,label):
        return random.Random(stable_seed(self.settings.seed,label))

    def roof_height(self,x,y):
        h=[]
        o=self.settings.overhang+1e-7
        for i,(a,b,c,d,axis) in enumerate(self.rects):
            ymax=d+o if i==0 else d+1e-7
            if a-o<=x<=c+o and b-o<=y<=ymax:
                distance = min(y-b,d-y) if axis=='X' else min(x-a,c-x)
                h.append(self.eave+self.slope*distance)
        return max(h) if h else float('-inf')


def make_plan(settings):
    settings.check()
    w,d,ww,wd=settings.width,settings.depth,settings.wing_width,settings.wing_depth
    rng=random.Random(stable_seed(settings.seed,'massing'))
    rects=[(0.,0.,w,d,'X')]
    if settings.footprint=='L':
        x=0. if rng.random()>.5 else w-ww
        rects.append((x,-wd,x+ww,d*.5,'Y'))
    elif settings.footprint=='T':
        x=(w-ww)*rng.uniform(.35,.65)
        rects.append((x,-wd,x+ww,d*.5,'Y'))
    elif settings.footprint=='U':
        delta=rng.uniform(-.14,.14)
        rects.extend([(0.,-wd*(1+delta),ww,d*.5,'Y'),(w-ww,-wd*(1-delta),w,d*.5,'Y')])
    return Plan(settings,rects)
