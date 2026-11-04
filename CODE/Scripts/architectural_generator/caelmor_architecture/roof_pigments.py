"""Diffuse paint in roof-local directions, with accents at real course butts."""
import numpy as np

from .surface_conditions import smooth
from .surface_patterns import _noise


TILE_BUFFERS = ('Split oak shingle courses', 'Seasoned shingle cohorts',
                'Exposed shingle butts', 'Replacement shingle cohort')


def course_start(host, points, normal, cache):
    """Return the laid course and whether its actual butt bounds this face."""
    from .roof import roof_courses

    if normal[2] < .63:
        return None
    axis = 0 if abs(normal[0]) > abs(normal[1]) else 1
    direction = -1 if normal[axis] > 0 else 1
    key = (id(host), axis, direction)
    if key not in cache:
        rect = host.rects[0]
        overhang = host.settings.overhang
        edge = rect[axis]-overhang if direction>0 else rect[axis+2]+overhang
        limit = rect[axis+2]-rect[axis]+2*overhang
        cache[key] = edge, np.array([t for _,t,_ in roof_courses(host,0,direction,limit)])
    eave, starts = cache[key]
    down_edge = direction*(points[:,axis]-eave)
    course = int(np.searchsorted(starts,down_edge.min()+.0002,side='right'))-1
    if course < 0:
        return None
    start = starts[course]
    has_butt = np.count_nonzero(np.abs(down_edge-start)<.0002)>=2
    return axis, direction, eave+direction*start, course, has_butt


def roof_pigment(positions, normals, region, seed):
    """Broad stock and directional pigment without artificial lighting."""
    x,y,z = positions.T
    nx,ny,_ = normals.T
    across = np.where(np.abs(nx)>np.abs(ny),y,x)
    run = np.where(np.abs(nx)>np.abs(ny),x,y)
    seed = seed & 65535
    group = _noise(x+.53*y,z,.61,.79,seed+881)
    if region=='LOWMARK':
        # Split timber reads along the fall, with honey in the prepared stock.
        sweep = _noise(across,run,9.5,1.25,seed+887)
        tint = np.array([1.14,.89,.72])
        pale = np.array([.42,.49,.58])
        dark = np.array([.28,.29,.27])
    else:
        # Broad cleft marks sit across the fall in cooler mineral stock.
        sweep = _noise(across,run,1.6,8.1,seed+887)
        tint = np.array([.87,1.05,1.09])
        pale = np.array([.53,.44,.39])
        dark = np.array([.33,.28,.24])
    signal = .76*group+.24*sweep
    return (tint + smooth(-.18,.64,signal)[:,None]*pale
            - smooth(.10,.68,-signal)[:,None]*dark)


def course_pigment(tile_stock, course_stock, lip, region):
    """Subordinate piece and course variation to broad roof color groups."""
    body = 1.+.105*tile_stock+.065*course_stock
    tint = np.array([.62,.49,.33]) if region=='LOWMARK' else np.array([.45,.49,.46])
    return body[:,None]+lip[:,None]*tint
