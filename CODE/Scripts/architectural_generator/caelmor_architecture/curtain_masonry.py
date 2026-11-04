"""Dressed facing for a short curtain return, in the wall's local coordinates."""
from .geometry import stable_seed
import random


# Stagger joints through the field. Long headers alternate which end they tie.
_COURSES = (
    ((.0,.24,.49,.74,1.), 'foot'),
    ((.0,.37,.64,1.), 'terminal'),
    ((.0,.24,.50,.82,1.), 'root'),
    ((.0,.35,.65,1.), 'terminal'),
    ((.0,.24,.51,.81,1.), 'root'),
    ((.0,.38,.66,1.), 'seat'),
)


def _facing_stone(buffer, x0, x1, z0, z1, nose, bed, rng, dressed, *, seated=False):
    """Bedded stone with clipped arrises and a broad, mildly tapered face."""
    width, height = x1-x0,z1-z0
    corner=min(width,height)*((.045 if dressed else .068) if seated else (.09 if dressed else .14))
    left_cut=corner*rng.uniform(.65,1.2)
    right_cut=corner*rng.uniform(.70,1.2)
    profile=((x0+left_cut,z0),(x1-right_cut,z0),(x1,z0+right_cut),
             (x1,z1-right_cut),(x1-right_cut,z1),(x0+left_cut,z1),
             (x0,z1-left_cut),(x0,z0+left_cut))
    # The small cut only eases the outer arris. The rear ring remains inside
    # the structural core, and the nose never narrows the course bed.
    inset=min(.045,corner*.6)
    mid_x,mid_z=(x0+x1)*.5,(z0+z1)*.5
    front=[(mid_x+(x-mid_x)*(1.-2*inset/width),nose,
            mid_z+(z-mid_z)*(1.-2*inset/height)) for x,z in profile]
    back=[(x,bed,z) for x,z in profile]
    n=len(profile)
    faces=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]
    faces.extend((i+n,(i+1)%n+n,(i+1)%n,i) for i in range(n))
    buffer.indexed(front+back,faces)


def dressed_curtain_return(buffer, start, end, station, base, seed, *, dressed=False,
                           bonded=False, variant=None):
    """Build road facing and cap around a continuous bearing wall.

    The wall runs from tower joint to site interface in positive X. The
    back face, end plane and top datum agree with the original return.
    """
    width=end-start
    if width<2.0:
        raise ValueError('Dressed curtain return needs at least two metres')
    core_top=base+3.46
    cap_top=base+3.61
    front,back=station-.35,station+.35
    bed=front+.085
    rng=random.Random(stable_seed(seed,'thornfell.curtain.dressing'))
    front_bed=front+(.014 if bonded else .045)
    rear_bed=back-.014 if bonded else back
    buffer.box(((start+end)*.5,(front_bed+rear_bed)*.5,core_top*.5),
               (width,rear_bed-front_bed,core_top))
    levels=(0.,.48,.48+(core_top-.48)*.18,.48+(core_top-.48)*.37,
            .48+(core_top-.48)*.57,.48+(core_top-.48)*.79,core_top)
    if bonded and variant=='level_course':
        levels=(0.,.48,*[.48+(core_top-.48)*index/5 for index in range(1,6)])
    for row, (breaks,role) in enumerate(_COURSES):
        if bonded and variant=='level_course':
            breaks=(0.,.25,.50,.75,1.) if row%2==0 else (0.,.125,.375,.625,.875,1.)
        for i,(a,b) in enumerate(zip(breaks,breaks[1:])):
            last=i==len(breaks)-2
            header=(role=='terminal' and last) or (role=='root' and i==0)
            # Projection belongs to footing, bond headers and cap bearing.
            # The ordinary infill remains comparatively shallow.
            setback=.19 if role=='foot' else .15 if header else .09 if role=='seat' else .045
            if role=='foot' and last:
                setback=.25
            setback+=rng.uniform(-.012,.012)
            if bonded:
                setback={'foot':.086,'seat':.028}.get(role,.018)+(.022 if header else 0.)
                setback+=rng.uniform(-.007,.007)
            x0=start+a*width+(.012 if i else 0.)
            x1=start+b*width-(.012 if not last else 0.)
            z0=levels[row]+(.009 if row else 0.)
            z1=levels[row+1]-.009
            worked=dressed or header or role=='foot'
            if bonded and header:
                # An actual full-depth header ties the faces across the core.
                _facing_stone(buffer,x0,x1,z0,z1,front-setback,back+.021,rng,worked,seated=True)
            else:
                _facing_stone(buffer,x0,x1,z0,z1,front-setback,bed,rng,worked,seated=bonded)
                if bonded:
                    # The rear course shares the bed and keys into alternate
                    # headers. Reverse the extrusion and face winding.
                    rear=type(buffer)('curtain_rear_stone')
                    _facing_stone(rear,x0,x1,z0,z1,-back-setback*.62,-back+.085,rng,worked,seated=True)
                    buffer.indexed([(x,-y,z) for x,y,z in rear.vertices],
                                   [tuple(reversed(face)) for face in rear.faces])
    for i,(a,b) in enumerate(zip((.0,.34,.66),(.34,.66,1.))):
        x0=start+a*width+(.012 if i else 0.)
        x1=start+b*width-(.012 if i<2 else 0.)
        # Full-depth cap stones shed water clear of the face and maintain
        # the original height. Recessed core shoulders carry the cap.
        projection=(.082,.073,.088)[i] if bonded else (.14,.105,.15)[i]
        _facing_stone(buffer,x0,x1,core_top-.05,cap_top,
                      front-projection,back+.06,rng,True,seated=bonded)
