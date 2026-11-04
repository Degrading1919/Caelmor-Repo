"""World-aware construction assemblies, authored from load paths and access rules.

Volumes are parameterized wall/roof constructions, never stored meshes. Each has
its own weather envelope; attachment faces reserve apertures before geometry.
"""
from dataclasses import replace
import math
import random

from .geometry import MeshBuffer, area, clip, inequalities, stable_seed
from .model import Plan, Settings, resolve_settings, style_for
from .roof import RoofPatch, build_roof, roof_faces
from .facade import build_facades


class MassPlan(Plan):
    def roof_height(self, x, y):
        if not hasattr(self, 'custom_roof_sources'):
            return super().roof_height(x,y)
        heights=[p.height(x,y) for p in self.custom_roof_sources
                 if all(a*x+b*y+c>=-1e-7 for a,b,c in inequalities(p.poly))]
        return max(heights, default=float('-inf'))


def _profile_sources(plan, mode):
    x0,y0,x1,y1,_=plan.rects[0]
    d=y1-y0; o=plan.settings.overhang
    if mode=='SHED' and (getattr(plan,'shed_reverse',False) or plan.rects[0][4]=='Y'):
        across_x=plan.rects[0][4]=='Y'
        span=x1-x0 if across_x else d
        slope=-plan.slope if getattr(plan,'shed_reverse',False) else plan.slope
        intercept=plan.eave+(span*plan.slope if getattr(plan,'shed_reverse',False) else 0.)
        poly=[(x0-o,y0-o),(x1+o,y0-o),(x1+o,y1+o),(x0-o,y1+o)]
        return [RoofPatch(poly,(slope,0.,intercept-slope*x0) if across_x
                          else (0.,slope,intercept-slope*y0))]
    if mode=='TERRACE':
        return [RoofPatch([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],
                          (0.,.035,plan.eave-.035*y0))]
    if mode=='SHED':
        stations=[(-o,-o*plan.slope),(d+o,(d+o)*plan.slope)]
    else:
        # A crown with broad curved shoulders: six planar spans carry continuous
        # reed bundles. The rise is tied to span, never random vertex noise.
        rise=d*.64
        stations=[(-o,-o*.18),(0.,0.),(.18*d,.62*rise),(.38*d,.96*rise),
                  (.5*d,rise),(.62*d,.96*rise),(.82*d,.62*rise),(d,0.),(d+o,-o*.18)]
    patches=[]
    for (t0,h0),(t1,h1) in zip(stations,stations[1:]):
        slope=(h1-h0)/(t1-t0)
        patches.append(RoofPatch([(x0-o,y0+t0),(x1+o,y0+t0),
                                 (x1+o,y0+t1),(x0-o,y0+t1)],
                                (0.,slope,plan.eave+h0-slope*(y0+t0))))
    return patches


def _terrace_roof(plan):
    """Draining mineral weather slab, protected by grounded perimeter parapets."""
    patch=plan.custom_roof_sources[0]
    deck=MeshBuffer('Draining terrace roof','stone','roof')
    deck.extrude([(x,y,patch.height(x,y)) for x,y in patch.poly],(0,0,-.18))
    parapet=MeshBuffer('Terrace parapet and coping','stone_light','roof')
    x0,y0,x1,y1,_=plan.rects[0]
    # Leave a genuine front scupper instead of enclosing an undrained basin.
    for a,b in [((x0,y0),(x0,y1)),((x1,y0),(x1,y1)),((x0,y1),(x1,y1))]:
        z0,z1=patch.height(*a),patch.height(*b)
        parapet.beam((*a,z0+.32),(*b,z1+.32),.34,.66)
        parapet.beam((*a,z0+.67),(*b,z1+.67),.42,.13)
    for a,b in [((x0,y0),(x0+(x1-x0)*.46,y0)),
                ((x0+(x1-x0)*.54,y0),(x1,y0))]:
        parapet.beam((*a,plan.eave+.32),(*b,plan.eave+.32),.34,.66)
        parapet.beam((*a,plan.eave+.67),(*b,plan.eave+.67),.42,.13)
    drains=MeshBuffer('Scupper apron','iron','roof')
    drains.box(((x0+x1)*.5,y0-.16,plan.eave-.04),((x1-x0)*.08,.40,.10))
    # Subtle slab joints describe construction rather than cottage tile courses.
    seams=MeshBuffer('Terrace slab seams','iron','roof')
    if plan.settings.detail!='LOW':
        for i in range(1,max(2,math.ceil((x1-x0)/2.4))):
            x=x0+(x1-x0)*i/max(2,math.ceil((x1-x0)/2.4))
            seams.beam((x,y0+.2,patch.height(x,y0+.2)+.007),
                       (x,y1-.2,patch.height(x,y1-.2)+.007),.018,.012)
    return [b for b in (deck,parapet,drains,seams) if b.faces]


class Mass:
    def __init__(self,key,plan,buffers):
        self.key,self.plan,self.buffers=key,plan,buffers
        x0,y0,x1,y1,_=plan.rects[0]
        self.bounds=(x0,y0,x1,y1)
        self.width,self.depth=x1-x0,y1-y0
        self.eave,self.base=plan.eave,plan.foundation_height

    def roof_height(self,x,y):
        return self.plan.roof_height(x,y)


class Context:
    def __init__(self,settings, resolver=None):
        self.settings=settings
        self.construction_resolver=resolver
        self.masses=[]; self.buffers=[]; self.decks=[]

    def rng(self,label):
        return random.Random(stable_seed(self.settings.seed,'world.'+label))

    def _tag(self,buffer,key,zone):
        if isinstance(zone,Mass) and not key.startswith(zone.key+'.'):
            key=zone.key+'.'+key
        buffer.name=f'world_{self.settings.region.lower()}.{key}'
        if buffer.field_source is not None and isinstance(zone,Mass):
            prefix=f'world_{self.settings.region.lower()}.{zone.key}.'
            buffer.field_source=prefix+buffer.field_source
            buffer.field_peers=tuple(prefix+peer for peer in buffer.field_peers)
        if any(b.name==buffer.name for b in self.buffers):
            raise ValueError('Duplicate semantic buffer identity: '+buffer.name)
        buffer.world_zone=zone.key if isinstance(zone,Mass) else zone
        self.buffers.append(buffer)
        return buffer

    def buffer(self,key,material,layer,zone=None):
        return self._tag(MeshBuffer(key,material,layer),key,zone)

    def component(self, buffer, zone, slot, role, treatment, **constraints):
        from .construction import bind, component
        return bind(component(zone.plan, slot, role, treatment, **constraints), buffer)

    def mass(self,key,*,x=0.,y=0.,width,depth,floors=1,floor_height=None,
             base=None,roof='GABLE',pitch=None,overhang=None,openings='DOMESTIC',
             entrance_edge=0,blocked_edges=(),steps=True,foundation='PLINTH',access_edges=(),
             function=None,gallery_edges=(),open_edges=(),open_access=(),wall_infill_roof_clearance=None,
             roof_axis='X',shed_reverse=False,passage_arch=None,aperture_schedule=None,frame_visibility=None,
             construction=None,swept_eaves=0.):
        if any(m.key==key for m in self.masses):
            raise ValueError('Duplicate construction zone: '+key)
        if not all(math.isfinite(v) for v in (x,y,width,depth)) or min(width,depth)<1.4:
            raise ValueError('Invalid construction volume dimensions')
        if roof not in ('GABLE','HIP','SHED','BOW','TERRACE'):
            raise ValueError('Unsupported construction roof')
        if roof_axis not in ('X','Y'):
            raise ValueError('Unsupported construction ridge axis')
        s=replace(self.settings,world_aware=False,use_grammar=False,footprint='RECT',
                  function=function or self.settings.function,
                  width=width,depth=depth,floors=int(floors),
                  floor_height=floor_height or self.settings.floor_height,
                  pitch=pitch if pitch is not None else self.settings.pitch,
                  overhang=overhang if overhang is not None else self.settings.overhang,
                  roof_style='HIP' if roof=='HIP' else 'GABLE')
        # Zone dimensions are constrained by builders, not public manual UI bounds:
        # a supported service wing can be narrower than the 6m main-body control.
        plan=MassPlan(s,[(x,y,x+width,y+depth,roof_axis)],self.settings)
        # Tile cohorts describe a limited stock/material range. Broad contrasting
        # rectangles on every slope read as arbitrary repairs in material views.
        # Geometry and the bounded eave-repair construction remain unchanged.
        palette=dict(plan.style.palette)
        roof_color=palette.get('roof')
        if roof_color is not None:
            for label,factor in (('roof_dark',.94),('roof_worn',.985),('roof_patch',1.025)):
                palette[label]=tuple(min(1.,c*factor) if i<3 else c for i,c in enumerate(roof_color))
            plan.style=replace(plan.style,palette=palette)
        plan.style=replace(plan.style,foundation_height=base if base is not None else plan.foundation_height,
                           foundation_mode=foundation)
        if self.settings.region in ('THORNFELL','EMBERHOLT'):
            stone_construction=('ASHLAR' if (self.settings.region=='EMBERHOLT' and s.craftsmanship!='ROUGH')
                                or (self.settings.region=='THORNFELL' and s.craftsmanship=='FINE') else 'RUBBLE')
            plan.style=replace(plan.style,construction=stone_construction,
                               wall_material='stone',frame_visibility=0.)
        if self.settings.region=='EMBERHOLT':
            palette=dict(plan.style.palette)
            palette.update(stone=(.17,.18,.185,1),stone_light=(.205,.205,.195,1),
                           mortar=(.115,.12,.12,1),metal=(.075,.085,.09,1))
            plan.style=replace(plan.style,palette=palette,
                               roof_cover='IRON' if roof!='TERRACE' else plan.style.roof_cover)
        if self.settings.region=='MIRE':
            plan.style=replace(plan.style,construction='BOARD',wall_material='timber_light',
                               roof_cover='REED',frame_visibility=1.)
        if open_edges and self.settings.region=='LOWMARK':
            plan.style=replace(plan.style,construction='TIMBER_INFILL',wall_material='plaster',frame_visibility=1.)
        plan.foundation_height=plan.style.foundation_height
        plan.eave=plan.foundation_height+int(floors)*s.floor_height
        plan.slope=math.tan(math.radians(s.pitch)) if roof!='TERRACE' else .035
        plan.opening_style=openings
        plan.entrance_edge_override=entrance_edge
        plan.secondary_entrance_edges=tuple(access_edges)
        plan.gallery_edges=tuple(gallery_edges)
        plan.open_edges=set(open_edges)
        plan.functional_access=tuple(dict(r) for r in open_access)
        plan.wall_infill_roof_clearance=wall_infill_roof_clearance
        plan.shed_reverse=shed_reverse
        plan.passage_arch=passage_arch
        plan.aperture_schedule=aperture_schedule
        plan.blocked_edges=set(blocked_edges)
        plan.entry_steps=steps
        plan.world_mass=True
        plan.roof_mode=roof
        plan.wall_thickness={'LOWMARK':.28,'THORNFELL':.50,'MIRE':.18,'EMBERHOLT':.70}[s.region]
        plan.glazing_recess=.22 if s.region in ('THORNFELL','EMBERHOLT') else 0.
        plan.door_thickness=.12 if s.region=='EMBERHOLT' else .065
        plan.disable_gable_frame=roof=='BOW'
        plan.suppress_function_details=True
        if frame_visibility is not None:
            plan.style=replace(plan.style,frame_visibility=float(frame_visibility))
        if construction is not None:
            if construction not in ('BOARD','TIMBER_INFILL','RUBBLE','ASHLAR'):
                raise ValueError('Unsupported construction override')
            plan.style=replace(plan.style,construction=construction,
                wall_material='timber_light' if construction=='BOARD' else
                'plaster' if construction=='TIMBER_INFILL' else 'stone')
        plan.suppress_chimney=self.settings.region in ('MIRE','EMBERHOLT') or openings=='NONE'
        if swept_eaves:
            if roof != 'GABLE':
                raise ValueError('Swept eaves require a gable')
            from .curve_profiles import swept_gable_sources
            plan.custom_roof_sources=swept_gable_sources(plan,swept_eaves)
        if roof in ('BOW','SHED','TERRACE'):
            plan.custom_roof_sources=_profile_sources(plan,roof)
        plan.construction_zone=key
        plan.construction_resolver=self.construction_resolver
        buffers=build_facades(plan)+(_terrace_roof(plan) if roof=='TERRACE' else build_roof(plan))
        mass=Mass(key,plan,buffers)
        self.masses.append(mass)
        for buffer in buffers:
            # Stone jambs and lintels belong to load-bearing stone walls. Iron
            # doors/straps belong to the industrial tradition, not wooden shutters.
            if self.settings.region in ('THORNFELL','EMBERHOLT') and buffer.name=='facade_timber':
                buffer.material='stone_light'
            if self.settings.region=='EMBERHOLT':
                if buffer.material.startswith('timber'): buffer.material='iron'
                if buffer.name=='facade_shutters': continue
            elif self.settings.region=='THORNFELL' and buffer.name=='facade_shutters':
                continue
            self._tag(buffer,key+'.'+buffer.name,mass)
        return mass

    def solid_stations(self,mass,edge_index,spacing=3.,radius=.25):
        a,b=mass.plan.edges[edge_index]
        length=math.dist(a,b)
        openings=mass.plan.facade_records[edge_index]['openings']
        count=max(1,math.ceil(length/spacing))
        candidates=[radius+.08]+[length*i/count for i in range(1,count)]+[length-radius-.08]
        return [s for s in candidates if radius<s<length-radius and
                all(s+radius<o['assembly_bounds']['s0']-.05 or
                    s-radius>o['assembly_bounds']['s1']+.05 for o in openings)]

    def deck(self,key,polygon_xy,z,thickness=.16,material='timber',zone=None):
        polygon=list(polygon_xy)
        if area(polygon)<0: polygon.reverse()
        deck=self.buffer(key,material,'foundation',zone)
        if (material == 'timber' and zone is not None and
                self.component(deck, zone, key, 'boarding', 'wooden_boarding')):
            from .construction_geometry import board_strips
            board_strips(deck, polygon, 0, lambda x,y: z, thickness)
        else:
            deck.prism(polygon,z-thickness,z)
        bounds=(min(x for x,y in polygon),min(y for x,y in polygon),
                max(x for x,y in polygon),max(y for x,y in polygon))
        self.decks.append((bounds,z))
        # Every elevated external platform gets ground-bearing supports.
        if z>.35:
            supports=self.buffer(key+'.supports','iron' if material=='iron' else 'timber','foundation',zone)
            x0,y0,x1,y1=bounds
            nx=max(1,math.ceil((x1-x0)/3.0)); ny=max(1,math.ceil((y1-y0)/3.0))
            for ix in range(nx+1):
                for iy in range(ny+1):
                    x=x0+.12+(x1-x0-.24)*ix/nx
                    y=y0+.12+(y1-y0-.24)*iy/ny
                    if all(a*x+b*y+c>=0 for a,b,c in inequalities(polygon)):
                        supports.box((x,y,(z-thickness)*.5),(.18,.18,z-thickness))
        return deck

    def stair(self,key,*,top,width,run,direction=(0,-1),material='timber',zone=None):
        tx,ty,tz=top
        if tz<=.05:return None
        length=math.hypot(*direction); dx,dy=(v/length for v in direction)
        ux,uy=-dy,dx
        steps=max(1,math.ceil(tz/.19)); step_run=run/steps
        buffer=self.buffer(key,material,'foundation',zone)
        for i in range(steps):
            z=tz*(1-i/steps)
            p=(tx+dx*step_run*(i+.5),ty+dy*step_run*(i+.5))
            # Individual closed treads carried by two continuous stringers.
            poly=[(p[0]+ux*u+dx*v,p[1]+uy*u+dy*v)
                  for u,v in [(-width/2,-step_run/2),(width/2,-step_run/2),
                              (width/2,step_run/2),(-width/2,step_run/2)]]
            if area(poly)<0:poly.reverse()
            buffer.prism(poly,z-.09,z)
        for side in (-1,1):
            buffer.beam((tx+ux*width*.40*side,ty+uy*width*.40*side,tz-.18),
                        (tx+dx*run+ux*width*.40*side,ty+dy*run+uy*width*.40*side,.04),.14,.21)
        return buffer

    def rail(self,key,a,b,z,material='timber',zone=None):
        supports=[bounds for bounds,height in self.decks if abs(height-z)<.06 and
                  all(bounds[0]-.1<=p[0]<=bounds[2]+.1 and bounds[1]-.1<=p[1]<=bounds[3]+.1 for p in (a,b))]
        if not supports:raise ValueError('Rail has no actual supporting deck: '+key)
        bounds=min(supports,key=lambda q:(q[2]-q[0])*(q[3]-q[1]))
        def inset(p):
            return (max(bounds[0]+.055,min(bounds[2]-.055,p[0])),
                    max(bounds[1]+.055,min(bounds[3]-.055,p[1])))
        a,b=inset(a),inset(b)
        rail=self.buffer(key,material,'details',zone)
        rail.structural_role='exterior_access'
        rail.support_surface={'plane':(0.,0.,z),'bounds':bounds,'max_height':1.1}
        n=max(1,math.ceil(math.dist(a,b)/1.8))
        for i in range(n+1):
            x,y=(a[k]+(b[k]-a[k])*i/n for k in range(2))
            rail.beam((x,y,z),(x,y,z+1.),.075,.075)
        for height in (.47,.97):rail.beam((*a,z+height),(*b,z+height),.07,.075)
        return rail


class WorldPlan:
    def __init__(self,ctx,requested):
        self.world_zones=ctx.masses
        self.access_decks=list(ctx.decks)
        self.settings=ctx.settings; self.requested_settings=requested
        primary=ctx.masses[0].plan
        self.style=primary.style; self.type_spec=primary.type_spec
        self.foundation_height=primary.foundation_height
        self.eave=max(m.eave for m in ctx.masses)
        self.slope=primary.slope
        self.rects=[r for m in ctx.masses for r in m.plan.rects]
        self.outline=primary.outline
        self.edges=[e for m in ctx.masses for e in m.plan.edges]
        self.facade_records=[]
        self.functional_program=getattr(ctx,'functional_program',None)
        offset=0
        for mass in ctx.masses:
            for record in mass.plan.facade_records:
                self.facade_records.append({**record,'edge_index':record['edge_index']+offset,
                                            'construction_zone':mass.key})
            offset+=len(mass.plan.edges)

    def roof_height(self,x,y):
        return max((m.roof_height(x,y) for m in self.world_zones),default=float('-inf'))

    def rng(self,label):
        return random.Random(stable_seed(self.settings.seed,'world.'+label))


def _abutment_flashings(ctx):
    """Folded aprons where a lower roof meets a taller, blind party facade."""
    for i,first in enumerate(ctx.masses):
        for second in ctx.masses[i+1:]:
            a,b=first.bounds,second.bounds
            joint=None
            for axis in (0,1):
                other=1-axis
                lo=max(a[other],b[other]); hi=min(a[other+2],b[other+2])
                if hi-lo<.1:continue
                for ca,cb in ((a[axis+2],b[axis]),(a[axis],b[axis+2])):
                    if abs(ca-cb)<1e-6:joint=(axis,ca,lo,hi)
            if joint is None:continue
            axis,station,lo,hi=joint
            # Stations include actual roof profile changes on both buildings.
            cuts={lo,hi}
            for mass in (first,second):
                from .roof import roof_sources
                for patch in roof_sources(mass.plan):
                    cuts.update(p[1-axis] for p in patch.poly if lo<p[1-axis]<hi)
            for k,(t0,t1) in enumerate(zip(sorted(cuts),sorted(cuts)[1:])):
                if t1-t0<1e-6:continue
                middle=[0.,0.];middle[axis]=station;middle[1-axis]=(t0+t1)*.5
                h0,h1=(m.roof_height(*middle) for m in (first,second))
                if abs(h0-h1)<.08:continue
                lower=first if h0<h1 else second
                bounds=lower.bounds
                inward=1. if abs(bounds[axis]-station)<1e-6 else -1.
                points=[]
                for t,offset in ((t0,0.),(t1,0.),(t1,.16),(t0,.16)):
                    p=[0.,0.];p[axis]=station+inward*offset;p[1-axis]=t
                    points.append((*p,lower.roof_height(*p)+.065))
                buffer=ctx.buffer(f'{first.key}.{second.key}.roof_apron.{k}','iron','roof',lower)
                if lower.plan.roof_mode=='HIP':
                    # A hip break can cross the *width* of this apron even
                    # when its party-line stations are split. Clip to each
                    # actual planar roof face; a warped quad can invert its
                    # thin solid despite a plausible centreline.
                    footprint=[p[:2] for p in points]
                    if area(footprint)<0:footprint.reverse()
                    for patch in roof_faces(lower.plan):
                        piece=footprint
                        for plane in inequalities(patch.poly):piece=clip(piece,*plane)
                        if piece:
                            buffer.extrude([(x,y,patch.height(x,y)+.065) for x,y in piece],(0,0,-.012))
                else:
                    buffer.extrude(points,(0,0,-.012))
                p,q=points[:2]
                buffer.extrude([p,q,(q[0],q[1],q[2]+.17),(p[0],p[1],p[2]+.17)],
                               tuple((.012*inward if j==axis else 0.) for j in range(3)))


def _working_apparatus(ctx):
    """Useful machinery follows industry and reserved building interfaces."""
    main=ctx.masses[0]
    if ctx.settings.region=='LOWMARK' and ctx.settings.function=='MILLER':
        x0,y0,x1,y1=main.bounds
        cy=y0+main.depth*.55; cz=main.base+1.40; radius=1.35
        wood=ctx.buffer('mill_wheel_rims_spokes_paddles','timber','details',main)
        wood.structural_role='mechanical'
        iron=ctx.buffer('mill_wheel_axle_and_bearings','iron','details',main)
        iron.cylinder((x0-1.05,cy,cz),(x0+.24,cy,cz),.16,12)
        n=12 if ctx.settings.detail=='LOW' else 20
        for face_x in (x0-.82,x0-.28):
            for i in range(n):
                a,b=math.tau*i/n,math.tau*(i+1)/n
                wood.beam((face_x,cy+radius*math.cos(a),cz+radius*math.sin(a)),
                          (face_x,cy+radius*math.cos(b),cz+radius*math.sin(b)),.10,.10)
            for i in range(8):
                a=math.tau*i/8
                wood.beam((face_x,cy,cz),(face_x,cy+radius*math.cos(a),cz+radius*math.sin(a)),.08,.10)
        for i in range(n):
            a=math.tau*i/n; ca,sa=math.cos(a),math.sin(a)
            poly=[(xx,cy+radius*ca-t*sa,cz+radius*sa+t*ca)
                  for xx,t in ((x0-.91,-.20),(x0-.19,-.20),(x0-.19,.20),(x0-.91,.20))]
            wood.extrude(poly,(0.,-.07*ca,-.07*sa))
        # The raceway is a ground-supported site interface; water/terrain remains
        # authored outside this building tool, not an invented resource system.
        race=ctx.buffer('mill_raceway_banks','stone','foundation',main)
        for xx in (x0-1.12,x0-.08):
            race.box((xx,cy,.14),(.18,4.0,.28))
    if ctx.settings.function=='WAREHOUSE':
        for record in main.plan.facade_records:
            door=next((o for o in record['openings'] if o.get('role')=='loading'),None)
            if door is None:continue
            a,b=main.plan.edges[record['edge_index']]; length=math.dist(a,b)
            tx,ty=(b[0]-a[0])/length,(b[1]-a[1])/length
            station=(door['s0']+door['s1'])*.5
            x=a[0]+tx*station+ty*.06; y=a[1]+ty*station-tx*.06
            z=min(door['z1']+.30,main.roof_height(x,y)-.32)
            if z<=door['z1']+.13:continue
            buf=ctx.buffer('loading_gantry_and_pulley','iron','details',main)
            buf.beam((x-tx*.74,y-ty*.74,z),(x+tx*.74,y+ty*.74,z),.15,.17)
            for side in (-1,1):
                buf.beam((x+side*tx*.58,y+side*ty*.58,z-.43),
                         (x+side*tx*.58,y+side*ty*.58,z),.12,.14)
            buf.cylinder((x-ty*.04,y+tx*.04,z-.17),(x+ty*.04,y-tx*.04,z-.17),.15,10)


def generate(settings, *, resolver=None):
    effective=resolve_settings(settings)
    ctx=Context(effective,resolver)
    from .functional import build as build_function
    if build_function(ctx):
        pass
    elif settings.region=='LOWMARK':
        from .world_lowmark_thornfell import build_lowmark
        build_lowmark(ctx)
    elif settings.region=='THORNFELL':
        from .world_lowmark_thornfell import build_thornfell
        build_thornfell(ctx)
    elif settings.region=='MIRE':
        from .world_mire import build
        build(ctx)
    else:
        from .world_emberholt import build
        build(ctx)
    if not ctx.masses:raise ValueError('Architectural language created no occupied volume')
    _abutment_flashings(ctx)
    _working_apparatus(ctx)
    from .benchmark_finish import refine
    refine(ctx)
    buffers=[b for b in ctx.buffers if b.faces]
    return WorldPlan(ctx,settings),buffers


def weather_crossings(masses):
    """Find intersecting visible roof planes across separately built volumes.

    Nonoverlapping occupied footprints alone do not protect projecting eaves.
    Intentional abutments may touch; a sign change within an overlap polygon is
    a genuine surface crossing requiring a junction or sufficient separation.
    """
    errors=[]
    patches=[roof_faces(m.plan) for m in masses]
    for i,a in enumerate(masses):
        for j in range(i+1,len(masses)):
            for pa in patches[i]:
                for pb in patches[j]:
                    poly=pa.poly
                    for plane in inequalities(pb.poly):
                        poly=clip(poly,*plane)
                        if not poly:break
                    if len(poly)<3 or abs(area(poly))<1e-5:continue
                    delta=[pa.height(x,y)-pb.height(x,y) for x,y in poly]
                    if min(delta)<-.015 and max(delta)>.015:
                        errors.append((a.key,masses[j].key,min(delta),max(delta)))
    return errors


def validate(plan,buffers,legacy_validator):
    errors=[]; rows=[]
    program=getattr(plan,'functional_program',None)
    if program:
        for route in program['routes']:
            if route['kind'] not in ('human','public','animal','service','material'):continue
            a=route['bounds']
            # A public transit strip is a usable aisle, not a thin empty ray
            # between fixtures. Standing work pads are a separate human role.
            if route['kind']=='public' and min(a[3]-a[0],a[4]-a[1])<1.2-1e-6:
                errors.append('Public circulation narrower than 1.2m: '+route['key'])
            for station in program['stations']:
                b=station['bounds']
                overlap=[min(a[i+3],b[i+3])-max(a[i],b[i]) for i in range(3)]
                if min(overlap)>.005:
                    errors.append('Functional clearance blocked: '+route['key']+' / '+station['key'])
    errors.extend(f'Weather roofs cross: {a} / {b}'
                  for a,b,_,_ in weather_crossings(plan.world_zones))
    zones={m.key:m for m in plan.world_zones}
    for i,mass in enumerate(plan.world_zones):
        for other in plan.world_zones[i+1:]:
            a,b=mass.bounds,other.bounds
            overlap=(min(a[2],b[2])-max(a[0],b[0]),
                     min(a[3],b[3])-max(a[1],b[1]),
                     min(mass.eave,other.eave)-max(mass.base,other.base))
            if min(overlap)>.001:
                errors.append(f'Occupied volumes overlap: {mass.key} / {other.key}')
    for key,mass in zones.items():
        local=[b for b in buffers if getattr(b,'world_zone',None)==key]
        if program:
            for buffer in local:
                if buffer.layer not in ('structure','walls'):continue
                excess=max((z-mass.roof_height(x,y) for x,y,z in buffer.vertices
                            if math.isfinite(mass.roof_height(x,y))),default=0.)
                if excess>1e-5:
                    errors.append(buffer.name+': functional '+('wall' if buffer.layer=='walls' else 'structure')+' crosses weather roof')
        report=legacy_validator(mass.plan,local)
        if mass.plan.settings.function=='GATEHOUSE' and not getattr(mass.plan,'passage_geometry',{}).get('valid'):
            errors.append(f'{key}: gate passage is not aligned through the occupied volume')
        rows.append({'key':key,'bounds':mass.bounds,'base':mass.base,'eave':mass.eave,
                     'valid':report['valid'],'roof':getattr(mass.plan,'roof_mode','GABLE'),
                     'function':mass.plan.settings.function,'wall_thickness':mass.plan.wall_thickness,
                     'vertices':report['vertices'],'triangles':report['triangles']})
        errors.extend(report['errors'])
        for record in mass.plan.facade_records:
            a,b=mass.plan.edges[record['edge_index']]
            length=math.dist(a,b)
            tx,ty=(b[0]-a[0])/length,(b[1]-a[1])/length
            for opening in record['openings']:
                if opening.get('role')!='gallery_access':continue
                station=(opening['s0']+opening['s1'])*.5
                x=a[0]+tx*station+ty*.10; y=a[1]+ty*station-tx*.10
                if not any(abs(z-opening['z0'])<.06 and bounds[0]<=x<=bounds[2] and
                           bounds[1]<=y<=bounds[3] for bounds,z in plan.access_decks):
                    errors.append(f'{mass.key}: upper door has no supporting access platform')
    extra=[b for b in buffers if getattr(b,'world_zone',None) not in zones]
    if extra:
        # Access geometry has explicit support surfaces; unzoned masonry is
        # geometric detail. Structural timber must still belong to a roof zone.
        if any(b.material.startswith('timber') and b.layer=='structure' for b in extra):
            errors.append('Unassigned structural timber construction zone')
        report=legacy_validator(plan.world_zones[0].plan,extra)
        errors.extend(report['errors'])
    return {'valid':not errors,'errors':errors,'objects':len(buffers),
            'vertices':sum(len(b.vertices) for b in buffers),
            'triangles':sum(len(f)-2 for b in buffers for f in b.faces),
            'materials':len({b.material for b in buffers}),
            'region':plan.settings.region,'context':plan.settings.context,
            'building_type':plan.settings.function,'geometry_mode':plan.settings.geometry_mode,
            'architecture':'WORLD','construction_zones':rows}
