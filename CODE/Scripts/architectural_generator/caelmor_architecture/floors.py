"""Additive floor-presentation contract. Z is building-local metres, not world Y.

Bands describe visual ownership, never occupancy, traversal or collision. The
last band is unoccupied gable/attic geometry. Runtime occupancy must be authored.
"""
import math

VERSION = 1


def schedule(plan):
    masses = getattr(plan, 'world_zones', None)
    hosts = [(m.key, m.plan) for m in masses] if masses else [('main', plan)]
    result = []
    for key, host in hosts:
        base = host.foundation_height
        height = host.settings.floor_height
        count = host.settings.floors
        result.append(dict(volume=key, base=base, height=height, count=count,
                           boundaries=[base+i*height for i in range(1, count+1)]))
    return result


def behavior(layer, structural_role='', functional_role='', *, component_role='', envelope=None):
    # Hollow flues must retain their void and continuity. They intentionally
    # remain visible, rather than acquiring a horizontal plug at every storey.
    if functional_role == 'chimney' or 'flue' in structural_role or structural_role == 'chimney':
        return 'ALWAYS'
    if (layer == 'roof' or component_role in ('roof_cover', 'roof_deck', 'roof_support')
            or envelope and 'plane' in envelope and envelope.get('clearance') == 0):
        return 'COVERING'
    return 'FLOOR'


def visible(behavior, lower, upper, cutoff):
    if cutoff is None or behavior == 'ALWAYS':
        return True
    if behavior == 'COVERING':
        # Preserve roofs below the occupied level on stepped wings.
        return upper <= cutoff-1e-5
    return lower < cutoff-1e-5


def ceiling(volumes, volume, floor):
    host = next((v for v in volumes if v['volume'] == volume), None)
    if host is None or not isinstance(floor, int) or not 0 <= floor < host['count']:
        raise ValueError('Select an existing volume and occupied floor (ground = 0)')
    value = host['base']+(floor+1)*host['height']
    if not math.isfinite(value):
        raise ValueError('Invalid floor elevation')
    return value
