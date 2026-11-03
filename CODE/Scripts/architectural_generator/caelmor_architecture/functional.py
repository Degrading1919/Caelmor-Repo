"""Function-first spatial contracts and regional construction primitives.

Programs allocate working/animal/public/defensive space before choosing the
regional weather shell. These are reversible art interpretations, not new lore.
"""
import math

from .facade import frame_layout


FUNCTIONS=('SMITHY','MARKET_HALL','STABLE','GATEHOUSE')


class Builder:
    def __init__(self,ctx,program_id):
        self.ctx=ctx;self.settings=ctx.settings;self.region=self.settings.region
        self.base=1.15 if self.region=='MIRE' else .32
        self.roof={'MIRE':'BOW','EMBERHOLT':'TERRACE'}.get(self.region,'GABLE')
        self.pitch=42 if self.region=='THORNFELL' else 32
        self.material='stone' if self.region in ('THORNFELL','EMBERHOLT') else 'timber'
        self.program={'function':program_id,'region':self.region,
                      'context':self.settings.context,'rooms':[],'stations':[],
                      'routes':[],'adaptations':[]}
        ctx.functional_program=self.program

    def mass(self,key,**kwargs):
        kwargs.setdefault('base',self.base)
        kwargs.setdefault('foundation','PIERS' if self.region=='MIRE' else 'PLINTH')
        kwargs.setdefault('roof',self.roof);kwargs.setdefault('pitch',self.pitch)
        kwargs.setdefault('overhang',.38 if self.region in ('LOWMARK','MIRE') else .25)
        kwargs.setdefault('openings','NONE');kwargs.setdefault('steps',False)
        # Cut sloping infill across its complete thickness at the roof soffit.
        # Legacy/non-program builders retain their existing output contract.
        kwargs.setdefault('wall_infill_roof_clearance',.12)
        mass=self.ctx.mass(key,**kwargs)
        self.program['rooms'].append({'key':key,'bounds':mass.bounds,'base':mass.base,
                                     'eave':mass.eave,'open_edges':sorted(mass.plan.open_edges),
                                     'roof':mass.plan.roof_mode})
        # Open masonry arcades need actual bearing piers, rather than converting
        # a closed cottage wall to an unsupported roof. Stations obey the same
        # entrance reservation used by the timber bents.
        if self.region in ('THORNFELL','EMBERHOLT'):
            for edge_index in sorted(mass.plan.open_edges):
                edge=mass.plan.edges[edge_index]
                layout=frame_layout(mass.plan,edge_index,edge)
                a,b=edge;length=math.dist(a,b)
                top=layout['roof_safety']['structural_top']
                piers=self.ctx.buffer(key+f'.arcade_piers_{edge_index}','stone','structure',mass)
                for station in layout['principal_posts']:
                    x=a[0]+(b[0]-a[0])*station/length
                    y=a[1]+(b[1]-a[1])*station/length
                    weather=[mass.roof_height(x+dx,y+dy) for dx in (-.28,.28) for dy in (-.28,.28)]
                    weather=[z for z in weather if math.isfinite(z)]
                    bearing_top=min(top,min(weather)-.045) if weather else top
                    piers.box((x,y,(mass.base+bearing_top)*.5),(.42,.42,bearing_top-mass.base))
                    piers.box((x,y,bearing_top-.04),(.56,.56,.16))
        return mass

    def fixture(self,key,material,zone,role='equipment'):
        buffer=self.ctx.buffer(key,material,'details',zone)
        buffer.functional_role=role
        return buffer

    def box(self,key,bounds,material,zone,role='equipment'):
        x0,y0,z0,x1,y1,z1=bounds
        if min(x1-x0,y1-y0,z1-z0)<=0:raise ValueError('Invalid functional fixture: '+key)
        buffer=self.fixture(key,material,zone,role)
        buffer.box(((x0+x1)*.5,(y0+y1)*.5,(z0+z1)*.5),(x1-x0,y1-y0,z1-z0))
        self.program['stations'].append({'key':buffer.name,'role':role,'bounds':bounds,
                                         'zone':zone.key if zone else None})
        return buffer

    def route(self,key,bounds,kind='human'):
        if any(bounds[i+3]<=bounds[i] for i in range(3)):
            raise ValueError('Invalid functional clearance: '+key)
        self.program['routes'].append({'key':key,'kind':kind,'bounds':bounds})

    def deck(self,key,poly,z=None,material=None,zone=None):
        return self.ctx.deck(key,poly,self.base if z is None else z,
                             material=material or self.material,zone=zone)

    def ramp(self,key,start_xy,end_xy,width,z,zone=None,material=None):
        """Ground-to-floor supported ramp; start is grade, end is raised floor."""
        sx,sy=start_xy;ex,ey=end_xy
        length=math.dist(start_xy,end_xy)
        if length<.1 or width<=0 or z<=0:raise ValueError('Invalid functional ramp')
        dx,dy=(ex-sx)/length,(ey-sy)/length
        px,py=-dy*width*.5,dx*width*.5
        top=[(sx-px,sy-py,.03),(sx+px,sy+py,.03),
             (ex+px,ey+py,z),(ex-px,ey-py,z)]
        ramp=self.ctx.buffer(key,material or self.material,'foundation',zone)
        ramp.extrude(top,(0,0,-.16))
        supports=self.ctx.buffer(key+'.supports',material or self.material,'foundation',zone)
        for i in range(1,max(2,math.ceil(length/1.8))+1):
            t=i/max(2,math.ceil(length/1.8));height=max(.04,.03+(z-.03)*t-.16)
            for side in (-.8,.8):
                x=sx+(ex-sx)*t+px*side;y=sy+(ey-sy)*t+py*side
                supports.box((x,y,height*.5),(.16,.16,height))
        self.program.setdefault('approaches',[]).append({'key':key,'start':start_xy,'end':end_xy,
             'width':width,'rise':z,'run':length,'slope':z/length})
        return ramp

    def finish(self):
        return self.program


def build(ctx):
    if ctx.settings.function not in FUNCTIONS:return False
    if ctx.settings.function in ('SMITHY','MARKET_HALL'):
        from .function_work import build_smithy,build_market
        {'SMITHY':build_smithy,'MARKET_HALL':build_market}[ctx.settings.function](ctx)
    else:
        from .function_yard import build_stable,build_gatehouse
        {'STABLE':build_stable,'GATEHOUSE':build_gatehouse}[ctx.settings.function](ctx)
    return True
