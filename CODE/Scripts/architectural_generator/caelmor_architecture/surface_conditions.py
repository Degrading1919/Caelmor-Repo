"""Causal surface history in building-local metres; no geometry or Blender imports.

Regional exposure constants are reversible art interpretations, not new lore.
The four controls have separate causes: grade, preparation, elapsed exposure,
and removal/repair of deterioration. Wealth never enters the dirt calculation.
"""
import numpy as np
from .surface_patterns import _noise


def smooth(a, b, x):
    t = np.clip((x-a)/max(b-a, 1e-8), 0., 1.)
    return t*t*(3.-2.*t)


def environment(plan):
    """Compact immutable context from real host apertures, hearths and ground."""
    openings=[]
    for record in getattr(plan, 'facade_records', ()):
        edge=int(record['edge_index']); a,b=plan.edges[edge]
        length=np.hypot(b[0]-a[0], b[1]-a[1])
        if length < 1e-7: continue
        tx,ty=(b[0]-a[0])/length,(b[1]-a[1])/length
        for o in record['openings']:
            if o['kind'] not in ('window','vent'): continue
            openings.append((a[0],a[1],tx,ty,o['s0'],o['s1'],o['z0']))
    return {'base':float(getattr(plan,'foundation_height',0.)),
            'eave':float(getattr(plan,'eave',3.)), 'openings':openings,
            'soot':list(getattr(plan,'soot_sources',()))}


def condition_fields(position, normal, u, v, key, settings, context,
                     unit=0., unit_z=0., family='stone'):
    """Return RGB multiplier, whitening, roughness delta, corrosion and relief.

    ``unit`` is one stable value per connected constructed piece, so a stone or
    timber does not change stock colour arbitrarily between adjacent faces.
    Masks use continuous metres, real sill positions, and known heat sources.
    """
    p=np.asarray(position); n=np.asarray(normal)
    x,y,z=p.T; nx,ny,nz=n.T
    unit=np.broadcast_to(np.asarray(unit),z.shape)
    unit_z=np.broadcast_to(np.asarray(unit_z),z.shape)
    age=float(settings.age); upkeep=float(settings.maintenance)
    maturity=1.-np.exp(-age/62.)
    neglect=(1.-upkeep)**1.35
    elapsed=1.-np.exp(-age/16.)
    region=settings.region
    dampness={'LOWMARK':.52,'THORNFELL':.34,'MIRE':.94,'EMBERHOLT':.19}[region]
    rain={'LOWMARK':.62,'THORNFELL':1.,'MIRE':.85,'EMBERHOLT':.42}[region]
    # A declared studio convention for prevailing exposure; no claim of a
    # canon meteorological simulation or terrain/rain shadow solver.
    facing=np.clip(-.60*nx-.80*ny,0.,1.)
    up=np.clip(nz,0.,1.)
    wall=1.-smooth(.35,.85,np.abs(nz))
    height=z-context['base']
    splash=(1.-smooth(.05,.95,height))*wall
    sheltered=smooth(-.05,.05,context['eave']-z)*(1.-smooth(.20,.95,context['eave']-z))*wall
    exposed=np.clip(.20+.58*facing+.55*up-.35*sheltered,0.,1.)*rain
    # Long, downwards streaks are modulated along the wall, never isotropic blobs.
    streak=.62+.38*_noise(x*.60+y*.80,z,6.,.65,83)
    runoff=np.zeros_like(z)
    for ax,ay,tx,ty,s0,s1,sill in context['openings']:
        along=(x-ax)*tx+(y-ay)*ty
        across=(x-ax)*ty-(y-ay)*tx
        outer=np.clip(nx*ty-ny*tx,0.,1.)
        down=sill-z
        drips=np.maximum(np.exp(-((along-(s0+.07))/.11)**2),
                         np.exp(-((along-(s1-.07))/.11)**2))
        runoff=np.maximum(runoff,drips*smooth(-.04,.04,down)*
            (1.-smooth(.25,1.35,down))*np.exp(-(across/.55)**4)*outer)
    moisture=np.clip(dampness*(.82*splash+.45*runoff)+.25*exposed*streak,0.,1.)
    dirt=elapsed*neglect*(.20*exposed+.82*moisture)
    tint=np.ones((len(z),3)); white=np.zeros_like(z)
    rough=np.zeros_like(z); corrosion=np.zeros_like(z); relief=np.zeros_like(z);silver=np.zeros_like(z)
    # Stock grading changes between pieces, not arbitrary per-vertex noise.
    grade={'MODEST':.19,'ESTABLISHED':.115,'AFFLUENT':.055}[settings.wealth]
    stock=1.+grade*np.asarray(unit)
    if family not in ('iron','leather','charcoal'):
        tint*=np.broadcast_to(stock,(len(z),))[:,None]
    if family=='wood' or family=='roof' and region in ('LOWMARK','MIRE'):
        silver=np.clip(maturity*(.18+.95*exposed)*(1.-.45*upkeep),0.,.82)
        # Exposed fibres mature toward a silver-grey mineral colour. Sheltered
        # maintained timber keeps its warmer heartwood; age never resets to new.
        tint*=1.-(.15*maturity+.70*dirt)[:,None]
        # Moisture enters end grain/low post shoes and exposed shingle butts.
        decay=maturity*neglect*(.35*splash+.38*moisture+.20*exposed)
        checks=np.exp(-(np.sin(v*131.+.22*np.sin(u*2.))/ .095)**2)
        tint*=1.-(decay*checks*.43)[:,None]
        relief-=.0018*decay*checks
        rough+=.10*maturity*exposed+.13*decay-.08*upkeep
        if family=='roof':
            # End-grain wets at the drip edge; accumulated exposure darkens
            # its lower courses rather than scattering stains over the slope.
            butt=(1.-smooth(.12,.85,z-context['eave']))*up
            tint*=1.-(.30*maturity*neglect*butt*streak)[:,None]
            # Select a few exposure-stressed whole shingles for replacement;
            # never a rectangular cohort spanning the slope.
            vulnerable=(1.-smooth(.15,1.05,np.asarray(unit_z)-context['eave']))
            repaired=(np.asarray(unit)<(-1.+.22*maturity*upkeep))*vulnerable
            tint=tint*(1.-.45*repaired[:,None])+.45*repaired[:,None]
            silver*=1.-repaired
            white*=1.-repaired*.65
    elif family=='stone' or family=='roof':
        mineral=maturity*exposed*.10
        tint*=1.-(.13*maturity+.80*dirt+mineral)[:,None]
        tint[:,0]*=1.-.16*moisture*elapsed*neglect
        tint[:,2]*=1.-.10*moisture*elapsed*neglect
        rough+=.04*maturity+.10*neglect*moisture
        relief-=.0015*maturity*neglect*moisture
        if key=='mortar':
            # Repointing is tied to stressed existing joints, not fake stones
            # painted over the real mesh. Old maintained joints can be lighter.
            repoint=maturity*upkeep*(.35+.65*moisture)
            white+=.11*repoint
            tint*=1.-.22*elapsed*neglect
            rough+=.045*neglect
    elif family=='plaster':
        tint*=1.-(.11*maturity+.95*dirt)[:,None]
        # Trowelled maintenance limewash follows splash/runoff damage, with a
        # broken brush boundary rather than random rectangular wall stains.
        stress=np.clip(splash+.8*runoff,0.,1.)
        brush=smooth(.10,.55,stress+.12*_noise(x+y,z,3.4,5.1,119))
        white+=.13*maturity*upkeep*brush
        rough+=.075*maturity*(1.-upkeep)-.035*upkeep
        relief-=.0008*maturity*neglect*stress
    elif family=='iron':
        corrosion=np.clip(elapsed*neglect*(.15+.80*moisture+.32*exposed)*
            smooth(-.30,.35,_noise(u,v,7.,8.,97)),0.,.85)
        tint*=1.-(.23*maturity*upkeep)  # dark protective scale/oiling
        rough+=.11*maturity*neglect-.10*upkeep
        relief+=.0006*corrosion
    elif family=='leather':
        tint*=1.-(.12*maturity+.25*dirt)[:,None]
        rough+=.08*maturity*(1.-upkeep)
    soot=np.zeros_like(z)
    for sx,sy,top in context['soot']:
        radial=np.hypot(x-sx,y-sy)
        soot=np.maximum(soot,np.exp(-(radial/.85)**2)*smooth(context['eave']-.8,top,z))
    for sx,sy,fire in context.get('heat',()):
        plume=np.exp(-((x-sx)**2+(y-sy)**2)/.85)*smooth(fire-.12,fire+.85,z)
        plume*=1.-smooth(context['eave'],context['eave']+.5,z)
        soot=np.maximum(soot,plume)
    tint*=1.-(soot*(.35+.38*(1.-upkeep)))[:,None]
    corrosion*=1.-soot
    return {'tint':np.clip(tint,.15,1.3),'white':np.clip(white,0.,.25),'silver':silver,
            'roughness_delta':rough,'corrosion':corrosion,'height':relief,
            'maturity':maturity,'moisture':moisture,'soot':soot}
