"""Construction rules for the two 0.8 art benchmarks; no stored mesh assets."""
import math
from .curve_profiles import cubic_centers
from .curve_sweep import sweep_member


def arch_polygon(opening, outer=0.):
    """Convex s/z aperture, with a segmented elliptical intrados."""
    s0,s1=opening['s0']-outer,opening['s1']+outer
    spec=opening['arch'];center=(s0+s1)*.5;radius=(s1-s0)*.5
    spring=spec['spring'];rise=spec['rise']+outer
    points=[(s0,opening['z0']-outer),(s1,opening['z0']-outer)]
    segments=spec.get('segments',16)
    stations=spec.get('stations') or (math.pi*i/segments for i in range(segments+1))
    for t in stations:
        points.append((center+radius*math.cos(t),spring+rise*math.sin(t)))
    return points


def arch_ring(buffer,center,y0,y1,spring,radius,rise,thickness=.30,segments=16,stations=None,sections=None):
    """Bonded radial voussoirs with actual open intrados and normal depth."""
    if stations is not None:
        def point(y, flare, t, offset):
            return (center+(radius+offset+flare)*math.cos(t),y,spring+(rise+offset)*math.sin(t))

        def between(p,q,t):
            return tuple(x+(y-x)*t for x,y in zip(p,q))

        sections=sections or ((y0,0.),(y1,0.))
        for a,b in zip(stations,stations[1:]):
            vertices=[]
            for y,flare in sections:
                inner_a,inner_b=point(y,flare,a,0.),point(y,flare,b,0.)
                outer_a,outer_b=point(y,flare,a,thickness),point(y,flare,b,thickness)
                vertices.extend((between(inner_a,inner_b,.008),between(inner_a,inner_b,.992),
                                 between(outer_a,outer_b,.992),between(outer_a,outer_b,.008)))
            last=len(vertices)-4
            faces=[(3,2,1,0),(last,last+1,last+2,last+3)]
            for start in range(0,last,4):
                for i in range(4):
                    a0,a1=start+i,start+(i+1)%4
                    faces.extend(((a0,a1,a1+4),(a0,a1+4,a0+4)))
            buffer.indexed(vertices,faces)
        return
    for i in range(segments):
        t0=math.pi*(i+.008)/segments;t1=math.pi*(i+.992)/segments
        points=[(center+r*math.cos(t),y0,spring+h*math.sin(t))
                for r,h,t in ((radius,rise,t0),(radius,rise,t1),
                              (radius+thickness,rise+thickness,t1),
                              (radius+thickness,rise+thickness,t0))]
        buffer.extrude(points,(0,y1-y0,0))


def smithy_range(b,main):
    """An accreted, lower stock range and legible primary timber bent."""
    ctx=b.ctx;z=main.base;d=main.depth
    stock=b.mass('smithy_stock_range',x=5.6,y=0,width=4.0,depth=d,
                 floor_height=2.55,roof='SHED',roof_axis='Y',shed_reverse=True,
                 pitch=12,overhang=.18,open_edges=[0,3],openings='NONE',
                 frame_visibility=0.,construction='BOARD',
                 open_access=[{'edge_index':0,'s0':.55,'s1':3.2,'height':2.25}])
    frame=ctx.buffer('smithy.primary_end_bent','timber','structure',main)
    frame.structural_role='pegged_primary_bent'
    for y in (.22,d-.24):
        xs=(.24,main.width-.24)
        top=min(main.roof_height(x,y) for x in xs)-.36
        for x in xs:
            frame.chamfered_beam((x,y,z+.28),(x,y,top),.32,.32)
        frame.chamfered_beam((xs[0],y,top-.10),(xs[1],y,top-.10),.30,.32)
        ridge=main.width*.5;peak=main.roof_height(ridge,y)-.42
        frame.beam((ridge,y,top),(ridge,y,peak),.18,.18)
        for x in xs:
            if ctx.settings.crafted_curves:
                cuts={u for patch in main.plan.custom_roof_sources for u,_ in patch.poly
                      if min(x,ridge)<u<max(x,ridge)}
                stations=[x,*sorted(cuts,reverse=x>ridge),ridge]
                centers=[(u,y,main.roof_height(u,y)-.36-.06*(u-x)/(ridge-x))
                         for u in stations]
                sweep_member(frame,centers,(0,1,0),[.26]*len(centers),[.22]*len(centers))
            else:
                frame.chamfered_beam((x,y,top),(ridge,y,peak),.22,.26)
        # Hewn knees join the post shoulders to the tie. The lower end stays
        # above the declared human route, with real bearing at both ends.
        knees=ctx.buffer('smithy.tie_knees.'+('front' if y<d*.5 else 'rear'),'timber','structure',main)
        for x,sign in ((xs[0],1),(xs[1],-1)):
            if ctx.settings.crafted_curves:
                hew=ctx.rng(f'smithy.knee.{y}.{sign}').uniform(-.045,.045)
                centers=cubic_centers((x,y,top-.84),(x+sign*.24,y,top-.58+hew),
                                      (x+sign*.50,y,top-.21+hew),(x+sign*.91,y,top-.14))
                sweep_member(knees,centers,(0,1,0),[.20]*len(centers),
                             [.24,.23,.22,.20,.19,.18,.20])
                continue
            points=[(x,y-.10,top-.88),(x+sign*.14,y-.10,top-.86),
                    (x+sign*.40,y-.10,top-.49),(x+sign*.88,y-.10,top-.20),
                    (x+sign*.88,y-.10,top-.09),(x+sign*.65,y-.10,top-.09),
                    (x+sign*.24,y-.10,top-.34),(x,y-.10,top-.64)]
            knees.extrude(points,(0,.20,0))
        for x in (1.35,main.width-1.35):
            frame.beam((ridge,y,top+.12),(x,y,main.roof_height(x,y)-.42),.15,.17)
    for x in (.24,main.width-.24,main.width*.5):
        h=main.roof_height(x,.22)-.42
        frame.beam((x,.22,h),(x,d-.24,h),.18,.22)
    stock_frame=ctx.buffer('smithy.stock_bents','timber','structure',stock)
    for y in (.22,d-.24):
        for x in (5.82,9.38):
            top=stock.roof_height(x,y)-.30
            stock_frame.chamfered_beam((x,y,z),(x,y,top),.26,.26)
        stock_frame.beam((5.82,y,stock.roof_height(5.82,y)-.30),
                         (9.38,y,stock.roof_height(9.38,y)-.30),.26,.28)
    for x in (5.82,9.38):
        top=stock.roof_height(x,.22)-.30
        stock_frame.beam((x,.22,top),(x,d-.24,top),.18,.22)
    feet=ctx.buffer('smithy.post_stone_shoes','stone','foundation',main)
    for y in (.22,d-.24):
        for x in (.24,main.width-.24):
            feet.box((x,y,z+.14),(.42,.42,.28))
    pegs=b.fixture('smithy.bent_joint_pegs','timber_light',main,'joinery')
    for x in (.24,main.width-.24):
        top=main.roof_height(x,.22)-.46
        for dx in (-.055,.055):
            pegs.cylinder((x+dx,.065,top),(x+dx,.14,top),.023,6)
    # Masonry shields the timber from the hot bay and ties the stack foot to
    # the building. Its top leaves the verified side duct unobstructed.
    shield=b.fixture('smithy.fire_screen','stone',main,'fire_screen')
    shield.box((.08,2.15,z+.90),(.32,2.6,1.80))
    shield.box((-.20,1.35,z+.85),(1.10,.95,1.70))
    for buffer in ctx.buffers:
        if any(part in buffer.name for part in ('hearth_left_curb','hearth_right_curb','hearth_rear_curb')):
            buffer.material='stone_sooted'
        if buffer.name.endswith('.anvil_stump'):
            center=tuple((min(p[i] for p in buffer.vertices)+max(p[i] for p in buffer.vertices))*.5 for i in (0,1))
            bottom=min(p[2] for p in buffer.vertices);upper=max(p[2] for p in buffer.vertices)
            buffer.vertices.clear();buffer.faces.clear()
            buffer.cylinder((*center,bottom),(*center,upper),.28,12)
    coals=b.fixture('smithy.fuel_on_firebed','charcoal',main,'forge_fire')
    for iy in range(3):
        for ix in range(7):
            coals.cylinder((1.02+ix*.16,1.00+iy*.19,z+.55),
                           (1.02+ix*.16,1.00+iy*.19,z+.61),.075,5)
    leather=b.fixture('smithy.bellows_skin','bellows_leather',main,'forge_bellows')
    leather.extrude([(.60,1.96,z+1.34),(1.30,1.96,z+1.34),
                     (1.35,2.25,z+1.34),(.98,2.42,z+1.34),(.58,2.25,z+1.34)],(0,0,.18))
    # A tapered, coursed jacket and an open coping give the masonry stack a
    # constructed profile. The inlet course is actually left open at the duct.
    (sx,sy,duct_z),(_,_,end)=b.program['ventilation']['stack']
    top=end-.18;courses=max(8,round(top/.40))
    stone=b.fixture('smithy.stack_courses','stone_light',main,'chimney')
    for row in range(courses):
        za=.04+row*(top-.04)/courses;zb=.04+(row+1)*(top-.04)/courses
        mid=(za+zb)*.5;r=.36+.16*(1-mid/top)
        stone.box((sx-r+.045,sy,mid),(.09,2*r,zb-za-.012))
        if zb<duct_z-.23 or za>duct_z+.23:
            stone.box((sx+r-.045,sy,mid),(.09,2*r,zb-za-.012))
        for side in (-1,1):
            stone.box((sx,sy+side*(r-.045),mid),(2*r-.18,.09,zb-za-.012))
    for side in (-1,1):
        stone.box((sx+side*.395,sy,top+.07),(.21,1.0,.14))
        stone.box((sx,sy+side*.395,top+.07),(.58,.21,.14))
    bench=b.fixture('smithy.stock_bench','timber',stock,'workbench')
    for x in (6.1,8.4):
        for y in (d-.62,d-.18):bench.box((x,y,z+.43),(.12,.12,.86))
    bench.box((7.25,d-.4,z+.91),(2.65,.70,.12))
    bench.box((7.25,d-.4,z+.25),(2.45,.54,.08))
    stock_iron=b.fixture('smithy.stock_and_tools','iron',stock,'stock')
    for i in range(5):
        x=6.2+i*.42
        stock_iron.beam((x,d-.35,z+.99),(x,d-.35,z+1.45+(i%2)*.12),.035,.035)
        stock_iron.box((x,d-.35,z+1.47+(i%2)*.12),(.23,.09,.08))
    # One wheel being repaired, stored beside the dry work range, conveys
    # agricultural/cart work without a general furnishing catalog.
    wheel=b.fixture('smithy.repair_wheel','timber',stock,'repair_work')
    ring=b.fixture('smithy.repair_wheel_tyre','iron',stock,'repair_work')
    cy,cz=1.55,z+.68
    for i in range(16):
        a=2*math.pi*i/16;c=2*math.pi*(i+1)/16
        p=(9.22,cy+.65*math.cos(a),cz+.65*math.sin(a))
        q=(9.22,cy+.65*math.cos(c),cz+.65*math.sin(c))
        wheel.beam(p,q,.075,.085);ring.beam((9.27,p[1],p[2]),(9.27,q[1],q[2]),.035,.04)
    for i in range(8):
        a=2*math.pi*i/8
        wheel.beam((9.22,cy,cz),(9.22,cy+.62*math.cos(a),cz+.62*math.sin(a)),.045,.055)
    wheel.cylinder((9.10,cy,cz),(9.35,cy,cz),.13,8)
    steps=ctx.buffer('smithy.workfront_threshold','stone','foundation',main)
    steps.box((2.4,-.40,.085),(4.2,.40,.17))
    steps.box((2.4,-.15,.135),(4.2,.30,.27))
    # Weathered masonry has actual joints at the workfront, at usable scale.
    joints=ctx.buffer('smithy.workfront_paving','stone_light','foundation',main)
    for row in range(2):
        for i in range(7):
            joints.box((.52+i*.61,-.92+row*.39,.045),(.59,.37,.035))
    b.program['adaptations'].append('Gabled forge with a lower outward-draining boarded stock range; agricultural wheel/tool repair')
