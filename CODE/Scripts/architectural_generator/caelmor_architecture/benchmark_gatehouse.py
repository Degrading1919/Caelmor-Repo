"""Thornfell pass-control benchmark: broad flanks, vaulted gate and guard hall."""
from math import tau
from .functional import Builder
from .benchmark_construction import arch_ring
from .geometry import MeshBuffer
from .curve_profiles import voussoir_stations
from .crafted_geometry import beveled_box


def _battered_courses(b,side,owner):
    """Bonded front plinth, retaining the original battered support envelope."""
    a,y0,c,_=owner.bounds;top=owner.base+1.15
    core=b.fixture('gatehouse.'+side+'_plinth_bedding','mortar',owner,'structure')
    core.extrude([(a-.12,y0+.10,0.),(a-.12,y0-.515,0.),
                  (a-.12,y0-.065,top),(a-.12,y0+.10,top)],(c-a+.24,0,0))
    face=b.fixture('gatehouse.'+side+'_battered_plinth','stone',owner,'structure')
    rng=owner.plan.rng('gatehouse.bonded_batter')
    rows=4;rise=top/rows
    for row in range(rows):
        start=a-.12-(.62 if row%2 else .05)
        while start<c+.12:
            end=start+rng.uniform(.94,1.34)
            lo=max(a-.12,start+.009);hi=min(c+.12,end-.009)
            if hi-lo>.08:
                zlo=row*rise+.006;zhi=(row+1)*rise-.006
                stone=MeshBuffer('plinth_piece')
                beveled_box(stone,(.5,.5,.5),(1.,1.,1.),.026)
                vertices=[]
                for u,v,w in stone.vertices:
                    z=zlo+(zhi-zlo)*w;front=y0-.55+.45*z/top
                    vertices.append((lo+(hi-lo)*u,front+(y0+.10-front)*v,z))
                # Mapping the worked cube to a battered block is mildly
                # bilinear; explicit triangles keep every face planar.
                faces=[(f[0],f[j],f[j+1]) for f in stone.faces for j in range(1,len(f)-1)]
                face.indexed(vertices,faces)
            start=end


def _paved_threshold(b,key,start,end,width,base,owner):
    """Ground-bearing architectural causeway with bonded flagstone surfacing."""
    ramp=b.ramp(key,start,end,width,base,zone=owner,material='stone')
    # The generic ramp's slender piers suit decks, not this masonry gate.
    support=next(buf for buf in b.ctx.buffers if buf.name==ramp.name+'.supports')
    support.vertices.clear();support.faces.clear()
    ramp.vertices.clear();ramp.faces.clear()
    sx,sy=start;ex,ey=end;length=((ex-sx)**2+(ey-sy)**2)**.5
    dx,dy=(ex-sx)/length,(ey-sy)/length;px,py=-dy,dx
    def point(u,t,lower=0.):
        return (sx+(ex-sx)*t+px*u,sy+(ey-sy)*t+py*u,.03+(base-.03)*t-lower)
    top=[point(-width*.5,0,.045),point(width*.5,0,.045),point(width*.5,1,.045),point(-width*.5,1,.045)]
    if sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(top,top[1:]+top[:1]))<0:top.reverse()
    bottom=[(x,y,-.08) for x,y,z in top]
    # Keep the original approach top exactly: only its bearing and paving change.
    ramp.indexed(bottom+top,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    paving=b.fixture(key+'.bonded_flags','stone_light',owner,'threshold')
    rows=max(3,round(length/.55))
    for row in range(rows):
        t0=row/rows+.007/length;t1=(row+1)/rows-.007/length
        start_u=-width*.5-(width/6 if row%2 else 0.)
        while start_u<width*.5:
            u0=max(-width*.5,start_u+.006);u1=min(width*.5,start_u+width/3-.006)
            if u1-u0>.06:
                paving.extrude([point(u0,t0),point(u1,t0),point(u1,t1),point(u0,t1)],(0,0,-.055))
            start_u+=width/3
    return ramp


def _tower_openings(width,depth,base,outer_edge):
    schedule={0:[],1:[],2:[],3:[]}
    for level in (0,1):
        z=base+(1.65 if level==0 else 4.80)
        for fraction in (.32,.68):
            s=width*fraction
            schedule[0].append(dict(kind='vent',role='arrow_loop',s0=s-.12,s1=s+.12,z0=z,z1=z+.90))
        s=depth*.52
        schedule[outer_edge].append(dict(kind='vent',role='arrow_loop',s0=s-.12,s1=s+.12,z0=z,z1=z+.90))
    schedule[2]=[dict(kind='door',role='courtyard_access',s0=width*.5-.55,
                      s1=width*.5+.55,z0=base-.02,z1=base+2.45),
                 dict(kind='window',s0=width*.5-.40,s1=width*.5+.40,
                      z0=base+4.80,z1=base+5.75)]
    return schedule


def build(ctx):
    from .function_yard import _stair_to_guard_floor
    b=Builder(ctx,'GATEHOUSE');base=b.base
    upper=base+3.92;link_y=4.05
    wealth=b.settings.wealth
    tower_width={'MODEST':5.4,'ESTABLISHED':5.8,'AFFLUENT':6.2}[wealth]
    core_width=4.8;depth=8.4;tower_depth=6.8;front=-1.8
    cx=tower_width+core_width*.5;total=2*tower_width+core_width
    core_schedule={0:[],1:[],2:[],3:[]}
    for edge in (0,2):
        core_schedule[edge].append(dict(kind='door',role='passage_entry' if edge==0 else 'passage_exit',
            s0=core_width*.5-1.4,s1=core_width*.5+1.4,z0=base-.02,z1=base+3.5))
    core_schedule[0].append(dict(kind='vent',role='portcullis_slot',s0=core_width*.5-.75,
        s1=core_width*.5+.75,z0=base+4.10,z1=base+5.40))
    core_schedule[2].append(dict(kind='window',s0=core_width*.5-.48,
        s1=core_width*.5+.48,z0=base+4.80,z1=base+5.85))
    for edge,station in ((1,link_y),(3,depth-link_y)):
        core_schedule[edge].append(dict(kind='door',role='gallery_access',s0=station-.55,
            s1=station+.55,z0=upper,z1=upper+2.05))
    rise=.82 if b.settings.crafted_curves else .60
    arch_spec={'spring':2.90,'rise':rise}
    if b.settings.crafted_curves:
        arch_spec['stations']=voussoir_stations(16,ctx.rng('gatehouse.voussoir_bond').uniform(0,tau))
    core=b.mass('gatehouse_portal',x=tower_width,width=core_width,depth=depth,
        floors=2,floor_height=3.8,function='GATEHOUSE',roof='GABLE',roof_axis='Y',pitch=32,
        overhang=.25,openings='NARROW',
        passage_arch=arch_spec,aperture_schedule=core_schedule)
    towers=[]
    for side,x,inner,outer in (('west',0.,1,3),('east',tower_width+core_width,3,1)):
        schedule=_tower_openings(tower_width,tower_depth,base,outer)
        station=link_y-front if inner==1 else front+tower_depth-link_y
        schedule[inner]=[dict(kind='door',role='gallery_access',s0=station-.55,
            s1=station+.55,z0=upper,z1=upper+2.05)]
        owner=b.mass('gatehouse_'+side+'_watchtower',x=x,y=front,width=tower_width,
            depth=tower_depth,floors=2,floor_height=3.5,function='WATCHTOWER',
            roof='HIP',pitch=38,overhang=.25,entrance_edge=2,openings='NARROW',
            aperture_schedule=schedule)
        towers.append(owner)
    x0,x1=cx-1.4,cx+1.4;spring=base+2.90
    b.route('gatehouse_open_through_passage',(x0,0,base,x1,depth,spring),kind='human')
    # True side-wall gate pockets keep open leaves outside the clear rectangle.
    for side,a,c,inner in (('west',tower_width,x0,x0),('east',x1,tower_width+core_width,x1)):
        wall=b.fixture('gatehouse.passage_cheek.'+side,'stone',core,'passage_wall')
        for ya,yb in ((0.,.48),(2.2,depth)):
            wall.box(((a+c)*.5,(ya+yb)*.5,(base+spring)*.5),(c-a,yb-ya,spring-base))
        pa,pc=(a,c-.18) if side=='west' else (a+.18,c)
        wall.box(((pa+pc)*.5,1.34,(base+spring)*.5),(pc-pa,1.72,spring-base))
        leaf=b.fixture('gatehouse.open_leaf.'+side,'timber',core,'gate_leaf')
        lx=inner-.10 if side=='west' else inner+.10
        for j in range(8):
            leaf.box((lx,.58+(j+.5)*1.52/8,base+1.33),(.09,1.52/8-.008,2.62))
        straps=b.fixture('gatehouse.leaf_straps.'+side,'iron',core,'gate_leaf')
        for zz in (.42,1.20,2.18):straps.box((lx,1.34,base+zz),(.11,1.52,.055))
    vault=b.fixture('gatehouse.vaulted_passage','stone_light',core,'vault')
    arch_ring(vault,cx,.16,depth-.16,spring,1.4,rise,.26,stations=arch_spec.get('stations'))
    flare=.24 if b.settings.crafted_curves else 0.
    projection=.51 if flare else .34
    for face,wall_y,sign in (('front',0.,-1),('rear',depth,1)):
        sections=sorted(((wall_y+sign*projection,flare),(wall_y,0.),
                         (wall_y-sign*.16,0.)))
        ya,yb=sections[0][0],sections[-1][0]
        arch=b.fixture('gatehouse.portal_arch.'+face,'stone_light',core,'structure')
        arch_ring(arch,cx,ya,yb,spring,1.4,rise,.34 if flare else .30,
                  stations=arch_spec.get('stations'),sections=sections if flare else None)
        for side,xa,xb in (('west',x0-.42,x0),('east',x1,x1+.42)):
            jamb=b.fixture('gatehouse.portal_jamb.'+face+'.'+side,'stone_light',core,'structure')
            rows=8;h=(spring-base)/rows
            for row in range(rows):
                if flare:
                    direction=-1 if side=='west' else 1
                    # A broader springer spreads the ring's bearing into the jamb.
                    left=xa-(.07 if row==rows-1 and direction<0 else 0.)
                    right=xb+(.07 if row==rows-1 and direction>0 else 0.)
                    section=[(left+direction*offset,y) for y,offset in sections]
                    section.extend((right+direction*offset,y) for y,offset in reversed(sections))
                    jamb.prism(section,base+row*h+.006,base+(row+1)*h-.006)
                else:
                    jamb.box(((xa+xb)*.5,(ya+yb)*.5,base+(row+.5)*h),
                             (xb-xa,yb-ya,h-.012))
    # Raised grille and a visible winch aperture, separate from the open arch.
    iron=b.fixture('gatehouse.portcullis','iron',core,'defense')
    bar_bottom=3.56+(rise-.60)
    for j in range(9):
        x=x0+.12+j*2.56/8
        iron.beam((x,.07,base+bar_bottom),(x,.07,base+5.32),.045,.055)
    for z in (3.68+(rise-.60),4.38,5.18):iron.box((cx,.07,base+z),(2.8,.08,.055))
    iron.cylinder((cx-.62,.20,base+4.80),(cx+.62,.20,base+4.80),.13,10)
    for x in (x0-.07,x1+.07):iron.beam((x,.10,base+.12),(x,.10,base+4.65),.065,.065)
    for side,owner in zip(('west','east'),towers):
        a,y0,c,y1=owner.bounds;stair_x=(a+c)*.5;stair_y0=y0+.52;stair_y1=y1-1.32
        for suffix,lo,hi in (('left',a+.22,stair_x-.68),('right',stair_x+.68,c-.22)):
            b.deck('gatehouse.'+side+'_guard_floor.'+suffix,
                   [(lo,y0+.30),(hi,y0+.30),(hi,y1-.30),(lo,y1-.30)],z=upper,material='timber',zone=owner)
        b.deck('gatehouse.'+side+'_guard_landing',[(stair_x-.68,stair_y1),(stair_x+.68,stair_y1),
             (stair_x+.68,y1-.30),(stair_x-.68,y1-.30)],z=upper,material='timber',zone=owner)
        _stair_to_guard_floor(b,'gatehouse.'+side+'_guard_stair',stair_x,stair_y0,stair_y1,base,upper,owner,'timber')
        b.ramp('gatehouse.'+side+'_courtyard_approach',(stair_x,y1+2.0),(stair_x,y1),1.5,base,zone=owner,material='stone')
        # Splayed foot courses, bonded quoins and a stringcourse explain the
        # masonry work; the mass stays squat and unornamented above them.
        _battered_courses(b,side,owner)
        corners=b.fixture('gatehouse.'+side+'_bonded_quoins','stone_light',owner,'structure')
        for row in range(17):
            z=base+(row+.5)*.40
            for x in (a+.20,c-.20):
                for y in (y0+.13,y1-.13):
                    corners.box((x,y,z),(.58 if row%2 else .38,.38 if row%2 else .58,.385))
        band=b.fixture('gatehouse.'+side+'_stringcourse','stone_light',owner,'structure')
        band.box(((a+c)*.5,y0-.04,upper-.14),(c-a+.16,.22,.20))
        band.box(((a+c)*.5,y1+.04,upper-.14),(c-a+.16,.22,.20))
        # Hand-worked, slightly splayed-looking stone reveals flank actual
        # unglazed defensive slots, rather than surface-painted black marks.
        reveals=b.fixture('gatehouse.'+side+'_loop_reveals','stone_light',owner,'defense')
        for record in owner.plan.facade_records:
            ea,eb=owner.plan.edges[record['edge_index']];length=((eb[0]-ea[0])**2+(eb[1]-ea[1])**2)**.5
            tx,ty=(eb[0]-ea[0])/length,(eb[1]-ea[1])/length
            for o in record['openings']:
                if o.get('role')!='arrow_loop':continue
                for s in (o['s0']-.075,o['s1']+.075):
                    x=ea[0]+tx*s+ty*.025;y=ea[1]+ty*s-tx*.025
                    reveals.beam((x,y,o['z0']-.04),(x,y,o['z1']+.04),.14,.14)
                for z in (o['z0']-.08,o['z1']+.08):
                    p=(ea[0]+tx*(o['s0']-.15)+ty*.025,ea[1]+ty*(o['s0']-.15)-tx*.025,z)
                    q=(ea[0]+tx*(o['s1']+.15)+ty*.025,ea[1]+ty*(o['s1']+.15)-tx*.025,z)
                    reveals.beam(p,q,.15,.14)
    floor=ctx.buffer('gatehouse.guard_hall_floor','timber','foundation',core)
    floor.structural_role='floor_borne_by_masonry_vault'
    floor.box((cx,depth*.5,upper-.06),(core_width-.16,depth-.60,.12))
    for side,x in (('west',tower_width),('east',tower_width+core_width)):
        b.deck('gatehouse.guardhall_threshold.'+side,
               [(x-.45,link_y-.70),(x+.45,link_y-.70),
                (x+.45,link_y+.70),(x-.45,link_y+.70)],z=upper,material='stone',zone=core)
        b.route('gatehouse.guardhall_connection.'+side,
                (x-.8,link_y-.45,upper,x+.8,link_y+.45,upper+2.),kind='human')
    _paved_threshold(b,'gatehouse.front_threshold_ramp',(cx,-4.0),(cx,0),2.6,base,core)
    _paved_threshold(b,'gatehouse.rear_threshold_ramp',(cx,depth+3.),(cx,depth),2.6,base,core)
    paving=ctx.buffer('gatehouse.passage_paving','stone_light','foundation',core)
    for row in range(16):
        for col in range(5):
            paving.box((x0+(col+.5)*2.8/5,(row+.5)*depth/16,base+.008),(.54,depth/16-.018,.016))
    # Short cut-off boundary returns make the fortification connection legible;
    # artists extend their plain end interfaces to the selected site wall.
    for side,xa,xb in (('west',-2.4,0.),('east',total,total+2.4)):
        wall=b.fixture('gatehouse.curtain_return.'+side,'stone',towers[0 if side=='west' else 1],'boundary')
        wall.box(((xa+xb)*.5,-.55,(base+3.5)*.5),(xb-xa,.70,base+3.5))
        wall.box(((xa+xb)*.5,-.55,base+3.52),(xb-xa+.06,.82,.18))
    b.program['adaptations'].append('Compact Thornfell ridge gate: hipped flank roofs, vaulted guarded passage and courtyard tower entries')
    return b.finish()
