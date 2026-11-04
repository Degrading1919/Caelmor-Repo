"""Construction profiles shared by render meshes and semantic envelope queries."""

import math
from .roof import RoofPatch, roof_courses


def swept_gable_sources(plan, bow):
    """Form a drained, piecewise planar gable with fixed eaves and crown.

    The overhang continues the first secant, keeping the cover on one plane
    across the wall line. Each strip uses the ordinary roof clipping system.
    """
    (xmin, ymin, xmax, ymax, ridge_axis), = plan.rects
    across, along = ((ymin, ymax), (xmin, xmax)) if ridge_axis == 'X' else ((xmin, xmax), (ymin, ymax))
    half = (across[1] - across[0]) * .5
    rise = half * plan.slope
    if not 0 < bow < rise * .25:
        raise ValueError('Swept gable must drain monotonically to the eaves')
    overhang = plan.settings.overhang
    u0, u1 = along[0] - overhang, along[1] + overhang
    patches = []
    for eave, sign in zip(across, (1, -1)):
        # Place each change of plane beneath a course butt. The exposed tile
        # faces then remain planar and their laps hide the break in pitch.
        cuts=[t-overhang for _,t,_ in roof_courses(plan,0,sign,half+overhang)
              if .12 < t-overhang < half-.10]
        run=[-overhang,*cuts,half]
        ts=[0.,*(u/half for u in cuts),1.]
        heights=[plan.eave+rise*t-4*bow*t*(1-t) for t in ts]
        heights[0]-=overhang*(heights[1]-heights[0])/run[1]
        for a, b, za, zb in zip(run, run[1:], heights, heights[1:]):
            va, vb = eave + sign*a, eave + sign*b
            low, high = sorted((va, vb))
            slope = (zb - za) / (vb - va)
            intercept = za - slope * va
            if ridge_axis == 'X':
                poly = [(u0,low),(u1,low),(u1,high),(u0,high)]
                plane = (0.,slope,intercept)
            else:
                poly = [(low,u0),(high,u0),(high,u1),(low,u1)]
                plane = (slope,0.,intercept)
            patches.append(RoofPatch(poly,plane,swept=True))
    return patches


def cubic_centers(a, b, c, d, sections=6):
    """Sample a cubic in order, including exact endpoints."""
    result = []
    for i in range(sections+1):
        t = i / sections
        u = 1-t
        result.append(tuple(u**3*p + 3*u*u*t*q + 3*u*t*t*r + t**3*s
                            for p,q,r,s in zip(a,b,c,d)))
    return result


def voussoir_stations(segments, phase):
    """Slightly irregular masonry courses with fixed springings and crown."""
    return tuple(math.pi * (t + .20/segments * math.sin(2*math.pi*t + phase)
                            * math.sin(2*math.pi*t)**2)
                 for t in (i/segments for i in range(segments+1)))
