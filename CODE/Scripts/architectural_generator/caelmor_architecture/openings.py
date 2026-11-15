"""Wall-relative feature inputs for a fitted cottage's construction schedule."""
from dataclasses import asdict, dataclass
import math
import re

from .geometry import area, inequalities


SIDES = ('front', 'right', 'rear', 'left')


def wall_edges(width, depth):
    corners = ((0., 0.), (width, 0.), (width, depth), (0., depth))
    return dict(zip(SIDES, zip(corners, corners[1:] + corners[:1])))


@dataclass(frozen=True)
class Opening:
    id: str
    side: str
    kind: str
    s0: float
    s1: float
    z0: float
    z1: float
    rise: float = 0.
    leaf: bool = True

    def record(self, plan, length):
        width = self.s1 - self.s0
        height = self.z1 - self.z0
        name = f'{self.side.title()} {self.kind} guide {self.id[:8]}'
        if self.kind not in ('door', 'window') or not all(map(math.isfinite, (self.s0, self.s1, self.z0, self.z1, self.rise))):
            raise ValueError(f'{name}: invalid opening profile')
        if self.s0 < .63 or self.s1 > length - .63:
            raise ValueError(f'{name}: leave at least 0.63 m of wall at each corner')
        if self.kind == 'door':
            if not .8 <= width <= 1.65 or not 1.9 <= height <= 2.7:
                raise ValueError(f'{name}: doorway needs 0.8–1.65 m width and 1.9–2.7 m height')
            if abs(self.z0 - plan.foundation_height) > .065:
                raise ValueError(f'{name}: set the threshold on the ground floor at {plan.foundation_height:.2f} m above the box bottom')
            z0 = plan.foundation_height
            if self.rise and not (.18 <= self.rise <= min(.65, width * .52) and self.z1 - self.rise - z0 >= 1.58):
                raise ValueError(f'{name}: use a shallow rounded head with at least 1.58 m under its spring line')
        else:
            z0 = self.z0
            if self.rise or not .42 <= width <= 1.6 or not .45 <= height <= 1.5:
                raise ValueError(f'{name}: use a 0.42–1.6 m by 0.45–1.5 m rectangular window')
            level = math.floor((z0 - plan.foundation_height) / plan.settings.floor_height)
            floor = plan.foundation_height + level * plan.settings.floor_height
            if not 0 <= level < plan.settings.floors or z0 < floor + .42 or self.z1 > floor + plan.settings.floor_height - .30:
                raise ValueError(f'{name}: place the window between its floor sill and upper plate')
        record = dict(kind=self.kind, s0=self.s0, s1=self.s1, z0=z0, z1=self.z1,
                      guide_id=self.id, leaf=self.leaf, guide_name=name)
        if self.rise:
            record['arch'] = dict(spring=self.z1 - self.rise, rise=self.rise, segments=12)
        return record


@dataclass(frozen=True)
class TimberPost:
    id: str
    side: str
    station: float
    bottom: float
    top: float
    kind: str = 'timber_post'


@dataclass(frozen=True)
class PlasterLoss:
    id: str
    side: str
    outline: tuple
    kind: str = 'plaster_loss'

    def triangles(self):
        """Use a single connected, authored outline with a visible chip profile."""
        outline = self.outline
        if not 4 <= len(outline) <= 24 or len(set(outline)) != len(outline):
            raise ValueError('Plaster loss needs 4–24 distinct outline points')
        if area(outline) < 0:
            outline = tuple(reversed(outline))
        center = tuple(sum(v[i] for v in outline)/len(outline) for i in range(2))
        if area(outline) < .035 or any(a*center[0]+b*center[1]+c <= 1e-6 for a,b,c in inequalities(outline)):
            raise ValueError('Use one connected plaster chip with a clear center and no folded or crossing edges')
        # A fan supports irregular, inward-notched profiles with a common
        # visible center. A winding greater than one would double-cut the skin.
        rays = [(s-center[0], z-center[1]) for s,z in outline]
        sweep = sum(math.atan2(a[0]*b[1]-a[1]*b[0], a[0]*b[0]+a[1]*b[1])
                    for a,b in zip(rays, rays[1:]+rays[:1]))
        if abs(sweep-math.tau) > 1e-5:
            raise ValueError('Plaster outline must go around its center once')
        return [(center,a,b) for a,b in zip(outline, outline[1:]+outline[:1])]


def snapshot(guides):
    records = []
    for guide in sorted(guides, key=lambda g: g.id):
        record = asdict(guide)
        if isinstance(guide, PlasterLoss):
            record['outline'] = [list(point) for point in guide.outline]
        records.append(record)
    return records


def guide_walls(guides):
    walls = {}
    ids = set()
    for guide in sorted(guides, key=lambda item: item.id):
        if not re.fullmatch(r'[a-f0-9]{32}', guide.id) or guide.id in ids or guide.side not in SIDES:
            raise ValueError('Wall guides require unique identities and supported wall sides')
        ids.add(guide.id)
        walls.setdefault(SIDES.index(guide.side), []).append(guide)
    return walls
