"""Semantic massing and deterministic Lowmark design inputs, independent of bpy."""
from dataclasses import dataclass, replace
import math
import random
from .geometry import stable_seed, area
from .profiles import (REGIONS, TYPE_SPECS, CONTEXTS, WEALTH_LEVELS,
                      CRAFTSMANSHIP_LEVELS)

FUNCTIONS = tuple(TYPE_SPECS)
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
    # Additive options. Defaults retain pre-grammar manual Lowmark behavior.
    region: str = 'LOWMARK'
    context: str = 'AUTO'
    wealth: str = 'ESTABLISHED'
    craftsmanship: str = 'STANDARD'
    maintenance: float = .7
    age: float = 35.0
    use_grammar: bool = False
    roof_style: str = 'AUTO'
    geometry_mode: str = 'SOLID'
    world_aware: bool = False
    crafted_curves: bool = False
    seed_massing: bool = False
    construction_overrides: dict | None = None

    def check(self, validate_shape=True):
        for name in ('width','depth','wing_width','wing_depth','floor_height','pitch','overhang','window_density','maintenance','age'):
            if not math.isfinite(getattr(self,name)):
                raise ValueError(f'{name} must be finite')
        if (self.function not in FUNCTIONS or (validate_shape and self.footprint not in FOOTPRINTS)
                or self.detail not in ('LOW','MEDIUM','HIGH')
                or self.region not in REGIONS or self.wealth not in WEALTH_LEVELS
                or self.craftsmanship not in CRAFTSMANSHIP_LEVELS
                or self.roof_style not in ('AUTO','GABLE','HIP')
                or self.geometry_mode not in ('SOLID','EFFICIENT')):
            raise ValueError('Unsupported function, footprint, profile, or detail')
        valid_contexts = ('AUTO', *CONTEXTS[self.region].keys())
        if self.context not in valid_contexts:
            raise ValueError(f'Context {self.context!r} is not compatible with {self.region}')
        if not isinstance(self.use_grammar, bool) or not isinstance(self.world_aware,bool) or not 0<=self.maintenance<=1 or not 0<=self.age<=250:
            raise ValueError('Grammar must be boolean; maintenance 0–1 and age 0–250 years required')
        if not isinstance(self.crafted_curves, bool):
            raise ValueError('Crafted curves must be boolean')
        if not isinstance(self.seed_massing, bool):
            raise ValueError('Seed massing must be boolean')
        if not isinstance(self.seed,int):
            raise ValueError('Integer seed required')
        if validate_shape and (not isinstance(self.floors,int) or not 1<=self.floors<=3):
            raise ValueError('Integer seed and 1–3 floors required')
        if validate_shape:
            if not 6<=self.width<=24 or not 4<=self.depth<=16:
                raise ValueError('Width 6–24m and depth 4–16m required')
            if not 2.5<=self.wing_width<=self.width-.5 or not 2.5<=self.wing_depth<=12:
                raise ValueError('Wing must be at least 2.5m and narrower than main body')
            if self.footprint!='RECT' and self.wing_width>self.depth:
                raise ValueError('Wing width must not exceed main depth for continuous joined gables')
            if self.footprint=='U' and self.width-2*self.wing_width<2:
                raise ValueError('U courtyard must have at least 2m clearance; reduce wing width')
            if not 2.4<=self.floor_height<=3.8 or not 30<=self.pitch<=60:
                raise ValueError('Floor height 2.4–3.8m and roof pitch 30–60° required')
        if not .2<=self.overhang<=.75:
            raise ValueError('Overhang .2–.75m required')
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
    def __init__(self,settings,rects,requested_settings=None):
        self.settings=settings
        self.requested_settings=requested_settings or settings
        self.style=style_for(settings)
        self.type_spec=TYPE_SPECS[settings.function]
        self.foundation_height=self.style.foundation_height
        self.rects=rects
        self.outline=rectangle_union_outline(rects)
        self.edges=list(zip(self.outline,self.outline[1:]+self.outline[:1]))
        self.eave=self.foundation_height+settings.floors*settings.floor_height
        self.slope=math.tan(math.radians(settings.pitch))

    def rng(self,label):
        return random.Random(stable_seed(self.settings.seed,label))

    def roof_height(self,x,y):
        h=[]
        o=self.settings.overhang+1e-7
        for i,(a,b,c,d,axis) in enumerate(self.rects):
            ymax=d+o if i==0 else d+1e-7
            if a-o<=x<=c+o and b-o<=y<=ymax:
                if self.settings.roof_style=='HIP':
                    distance=min(x-a,c-x,y-b,d-y)
                else:
                    distance = min(y-b,d-y) if axis=='X' else min(x-a,c-x)
                h.append(self.eave+self.slope*distance)
        return max(h) if h else float('-inf')


@dataclass(frozen=True)
class Style:
    region: str
    context: str
    foundation_height: float
    foundation_mode: str
    wall_material: str
    construction: str
    roof_cover: str
    frame_visibility: float
    palette: dict
    weather_exposure: float


def _context(settings):
    region=REGIONS[settings.region]
    return region.default_context if settings.context=='AUTO' else settings.context


def style_for(settings):
    """Resolve a restrained regional surface style; regional details remain working grammar."""
    region=REGIONS[settings.region]
    construction=region.construction
    wall=region.wall_material
    cover=region.roof_cover
    mode=region.foundation_mode
    foundation=.68 if mode=='PIERS' else .45
    if settings.region=='MIRE':
        foundation=.9
    if settings.region=='THORNFELL': foundation=.5
    if settings.region=='EMBERHOLT': foundation=.48
    if settings.wealth=='AFFLUENT':
        if construction=='RUBBLE': construction='ASHLAR'
        if wall=='plaster':
            wall='stone'
            construction='ASHLAR'
        if cover=='SHINGLE': cover='SLATE'
        elif cover=='REED': cover='SHINGLE'
    elif settings.wealth=='MODEST':
        if construction=='ASHLAR': construction='RUBBLE'
        if cover in ('SLATE','CLAY'): cover='SHINGLE' if settings.region!='MIRE' else 'REED'
    if settings.craftsmanship=='ROUGH':
        if construction=='ASHLAR': construction='RUBBLE'
        frame=.82
    elif settings.craftsmanship=='FINE': frame=.28
    else: frame=.56
    # Load-bearing stone walls carry their own storeys. Retain roof wall plates
    # and opening casings without drawing a second timber skeleton over them.
    if construction in ('RUBBLE','ASHLAR'):
        frame=.12
    palette=dict(region.base_palette)
    if cover=='SLATE' and settings.region!='THORNFELL':
        # A costlier mineral cover retains its material identity within the
        # local palette rather than inheriting the brown shingle pigment.
        palette['roof']=(.26,.29,.29,1)
        palette['roof_dark']=(.18,.20,.20,1)
    context=_context(settings)
    exposure=region.weather_exposure
    if context in ('RIDGE','PASSWATCH','GRIEFWATCH'):
        exposure=min(1.0,exposure+.08)
    if settings.region=='MIRE' and context in ('MARSHFALL','SORROWMERE'):
        foundation+=.12 if context=='MARSHFALL' else 0.0
    return Style(settings.region,context,foundation,mode,wall,construction,cover,
                 frame,palette,exposure)


def resolve_settings(requested):
    """Return a validated effective grammar realization; manual dimensions are retained."""
    if requested.world_aware and not requested.use_grammar:
        # World builders consume envelope dimensions, not legacy U/L wing or
        # roof controls. Stale hidden controls cannot invalidate a valid input.
        requested.check(validate_shape=False)
        effective=replace(requested,footprint='RECT',wing_width=2.5,wing_depth=2.5,
                          pitch={'LOWMARK':32.,'THORNFELL':52.,'MIRE':38.,'EMBERHOLT':42.}[requested.region])
        effective.check()
        return replace(effective,context=_context(effective),
                       roof_style=TYPE_SPECS[requested.function].roof_style)
    # Grammar replaces the footprint and dimensional controls, so validate
    # those constraints on the effective type plan below. Always validate the
    # active profile, seed, finite values, upkeep, roof control and detail inputs.
    requested.check(validate_shape=not requested.use_grammar)
    if not requested.use_grammar:
        return replace(requested, context=_context(requested),
                       roof_style=(TYPE_SPECS[requested.function].roof_style if requested.roof_style=='AUTO'
                                   else requested.roof_style))
    spec=TYPE_SPECS[requested.function]
    region=REGIONS[requested.region]
    context=_context(requested)
    width,depth,ww,wd=spec.width,spec.depth,spec.wing_width,spec.wing_depth
    floors=spec.floors
    # Local form cues: trade towns and civic districts build broader public fronts;
    # exposed/highland contexts are compact; floodplain MIRE uses stilted narrow plans.
    if context in ('BROOKHOLLOW','CRESTBRIDGE','STONEWAKE','EMBERFORGES','EMBERHOLD'):
        width*=1.08
    if context in ('HIGHSTEADS','PASSWATCH','RIDGE','GRIEFWATCH'):
        width*=.91; depth*=.94
    if requested.region=='MIRE': width*=.94; depth*=.92
    wealth_scale={'MODEST':.88,'ESTABLISHED':1.0,'AFFLUENT':1.12}[requested.wealth]
    width*=wealth_scale; depth*=wealth_scale
    # Keep supported limits and ensure every non-rectangular wing fits its host body.
    width=min(24,max(6,width)); depth=min(16,max(4,depth))
    if spec.footprint=='U':
        ww=min(ww*wealth_scale, (width-2.05)/2, depth-.5)
    else:
        ww=min(ww*wealth_scale,width-.5,depth-.1)
    ww=max(2.5,ww)
    wd=min(12,max(2.5,wd*wealth_scale))
    if requested.region=='MIRE' and spec.category in ('BOATHOUSE','WAREHOUSE','GRAIN_STORE'):
        wd=min(12,wd*1.08)
    pitch={'LOWMARK':43,'THORNFELL':48,'MIRE':38,'EMBERHOLT':42}[requested.region]
    pitch += {'MODEST':-2,'ESTABLISHED':0,'AFFLUENT':2}[requested.wealth]
    craftsmanship_height={'ROUGH':2.65,'STANDARD':2.8,'FINE':3.0}[requested.craftsmanship]
    effective=replace(requested, width=width,depth=depth,wing_width=ww,wing_depth=wd,
                      floors=floors,floor_height=craftsmanship_height,pitch=pitch,
                      footprint=spec.footprint,
                      roof_style=(spec.roof_style if requested.roof_style=='AUTO' else requested.roof_style),
                      context=context)
    effective.check()
    return effective


def make_plan(settings):
    requested=settings
    settings=resolve_settings(settings)
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
    return Plan(settings,rects,requested)
