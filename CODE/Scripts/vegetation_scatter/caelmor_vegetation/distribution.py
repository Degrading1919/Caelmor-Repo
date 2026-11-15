"""Seeded habitat sampling in metres. Geometry and ownership live in the Blender adapter."""

from dataclasses import dataclass
import hashlib
import math

import numpy as np


FAMILY_WEIGHTS = {
    "Short_Sward": .95, "Mixed_Verge": .72, "Dry_Roadside": .55, "Meadow_Seed": .30,
    "Ribbed_Rosette": .26, "Wayside_Yarrow": .045, "Selfheal": .053,
    "Sprouts": .92, "Stubble": 1.26, "Low_Weeds": .52, "Dry_Stems": .54, "Broken_Tuft": .82,
}
MASKS = {"cv_density": 1., "cv_exclude": 0., "cv_moisture": .5, "cv_verge": 0.}


@dataclass(frozen=True)
class Variant:
    family: str
    stage: str
    indices: tuple
    triangles: tuple
    radius: float
    height: float
    moisture: float
    edge: float
    patch_density: float
    filler: bool


@dataclass(frozen=True)
class Surface:
    key: str
    triangles: np.ndarray
    masks: np.ndarray


@dataclass(frozen=True)
class Guide:
    segments: np.ndarray
    half_width: float
    verge: float


@dataclass(frozen=True)
class Settings:
    seed: int = 2077
    density: float = 90.
    filler: float = .91
    density_boost: float = .55
    clustering: float = .76
    patch_size: float = 2.40
    moisture: float = .55
    slope_limit: float = 39.
    align: float = .17
    elevation: tuple | None = None
    wall_gap: float = .06
    wall_verge: float = 1.1
    scale: tuple = (.70, 1.21)
    height: float = 1.
    heading: float = 0.
    rotation: float = math.pi
    lod_origin: tuple | None = None
    lod_distances: tuple = (5.5, 14.)
    tile_size: float = 5.
    max_samples: int = 300000
    max_instances: int = 28000
    max_triangles: int = 750000


@dataclass
class Placement:
    xyz: np.ndarray
    euler: np.ndarray
    scale: np.ndarray
    assets: np.ndarray
    lod: np.ndarray
    cost: np.ndarray
    candidates: int = 0
    habitat_count: int = 0
    requested_samples: int = 0

    @property
    def signature(self):
        hash_value = hashlib.sha256()
        for array in (self.xyz, self.euler, self.scale):
            hash_value.update(np.round(array, 6).astype("<f8").tobytes())
        hash_value.update(self.assets.astype("<i4").tobytes())
        return hash_value.hexdigest()


def smooth(low, high, value):
    t = np.clip((value - low) / (high - low), 0., 1.)
    return t*t*(3.-2.*t)


def noise(xy, period, seed):
    cell = np.floor(xy / period)
    x, y = cell.T
    u, v = smooth(0, 1, xy / period - cell).T

    def lattice(a, b):
        h = np.sin(a * 127.1 + b * 311.7 + seed * 17.193) * 43758.5453
        return h - np.floor(h)

    low = (1-u)*lattice(x, y) + u*lattice(x+1, y)
    high = (1-u)*lattice(x, y+1) + u*lattice(x+1, y+1)
    return (1-v)*low+v*high


def segment_distances(points, segments):
    """XY point-to-segment distances, including the ends of open guides."""
    displacements = points[:, None, :] - segments[None, :, 0, :]
    directions = segments[:, 1] - segments[:, 0]
    denom = np.maximum(np.einsum("ij,ij->i", directions, directions), 1.e-16)
    along = np.clip(np.einsum("nsi,si->ns", displacements, directions) / denom, 0, 1)
    delta = displacements - along[..., None] * directions
    return np.sqrt(np.einsum("nsi,nsi->ns", delta, delta))


def group_tiles(xy, width):
    if not len(xy):
        return
    cells = np.floor(xy / width).astype(np.int64)
    indices = np.lexsort((cells[:, 1], cells[:, 0]))
    ordered = cells[indices]
    breaks = np.flatnonzero(np.any(np.diff(ordered, axis=0), axis=1))+1
    for group in np.split(indices, breaks):
        yield tuple(cells[group[0]]), group


def guide_fields(xy, guides, reach):
    """Negative clearance is inside tread. Verge strength falls beyond each guide."""
    clearance = np.full(len(xy), np.inf)
    verge = np.zeros(len(xy))
    if not guides or not len(xy):
        return clearance, verge
    segments = np.concatenate([g.segments for g in guides])
    widths = np.repeat([g.half_width for g in guides], [len(g.segments) for g in guides])
    shoulders = np.repeat([g.verge for g in guides], [len(g.segments) for g in guides])
    padding = widths+np.maximum(shoulders, reach)
    lower = segments.min(axis=1) - padding[:, None]
    upper = segments.max(axis=1) + padding[:, None]
    for _, ids in group_tiles(xy, 4.):
        points = xy[ids]
        near = np.all((upper >= points.min(axis=0)) & (lower <= points.max(axis=0)), axis=1)
        if not near.any():
            continue
        dist = segment_distances(points, segments[near]) - widths[near]
        clearance[ids] = dist.min(axis=1)
        width = shoulders[near]
        influence = (1-smooth(0, np.maximum(width, 1.e-6), dist)) * (width > 0)
        verge[ids] = influence.max(axis=1)
    return clearance, verge


def wall_fields(xy, footprints, reach):
    clearance = np.full(len(xy), np.inf)
    for polygon in footprints:
        lower, upper = polygon.min(axis=0)-reach, polygon.max(axis=0)+reach
        ids = np.flatnonzero(np.all((xy >= lower) & (xy <= upper), axis=1))
        if not len(ids):
            continue
        end = np.roll(polygon, -1, axis=0)
        distance = segment_distances(xy[ids], np.stack((polygon, end), axis=1)).min(axis=1)
        diff = xy[ids, None, :] - polygon[None, :, :]
        edges = end-polygon
        cross = edges[:, 0]*diff[:, :, 1] - edges[:, 1]*diff[:, :, 0]
        inside = np.all(cross >= -1.e-10, axis=1)
        clearance[ids] = np.minimum(clearance[ids], np.where(inside, -distance, distance))
    return clearance


def manual_fields(xy, protected, reach):
    clearance = np.full(len(xy), np.inf)
    if not len(protected):
        return clearance
    for _, ids in group_tiles(xy, 4.):
        points = xy[ids]
        padding = reach+protected[:, 2, None]
        near = np.all((protected[:, :2]+padding >= points.min(axis=0)) &
                      (protected[:, :2]-padding <= points.max(axis=0)), axis=1)
        if near.any():
            around = protected[near]
            distance = np.linalg.norm(points[:, None, :] - around[None, :, :2], axis=2)-around[:, 2]
            clearance[ids] = distance.min(axis=1)
    return clearance


def make_candidates(surfaces, settings):
    valid = []
    total_area = 0.
    slope = math.cos(math.radians(settings.slope_limit))
    for surface in sorted(surfaces, key=lambda s: s.key):
        a, b, c = surface.triangles.transpose(1, 0, 2)
        cross = np.cross(b-a, c-a)
        length = np.linalg.norm(cross, axis=1)
        usable = (length > 1.e-9) & (cross[:, 2] >= slope*length)
        if usable.any():
            cumulative = np.cumsum(.5*length[usable])
            valid.append((surface, usable, cumulative, cross[usable]/length[usable, None]))
            total_area += cumulative[-1]
    requested = math.ceil(total_area*settings.density)
    if not requested:
        return np.empty((0, 3)), np.empty((0, 3)), np.empty((0, 4)), np.empty((0, 9)), 0
    density = settings.density*min(1., settings.max_samples/requested)
    samples = []
    planned = 0.
    count_so_far = 0
    for surface, usable, cumulative, normal in valid:
        planned += density*cumulative[-1]
        end = min(settings.max_samples, math.ceil(planned))
        count = end-count_so_far
        count_so_far = end
        seed = int.from_bytes(hashlib.blake2s(surface.key.encode(), digest_size=4).digest(), "little")
        rng = np.random.default_rng(np.random.SeedSequence((settings.seed, seed)))
        roll = rng.random((count, 9))
        face = np.searchsorted(cumulative, roll[:, 0]*cumulative[-1])
        u = np.sqrt(roll[:, 1])
        bary = np.column_stack((1-u, u*(1-roll[:, 2]), u*roll[:, 2]))
        coords = np.einsum("ni,nij->nj", bary, surface.triangles[usable][face])
        paint = np.einsum("ni,nij->nj", bary, surface.masks[usable][face])
        samples.append((coords, normal[face], paint, roll))
    return *tuple(np.concatenate(channel) for channel in zip(*samples)), requested


def budget_lods(variants, variant, lod, rank, distance, settings):
    cost_table = np.array([entry.triangles for entry in variants], dtype=np.int64)
    take = np.argsort(rank, kind="stable")[:settings.max_instances]
    lod = lod[take].copy()
    desired = variant[take]
    cost = cost_table[desired, lod]
    overflow = cost.sum() - settings.max_triangles
    if overflow > 0:
        priority = np.argsort(-distance[take], kind="stable")
        transitions = np.arange(2)
        by_type = cost_table[desired[priority]]
        savings = by_type[:, :2]-by_type[:, 1:]
        row, step = np.nonzero((transitions >= lod[priority, None]) & (savings > 0))
        length = min(len(row), np.searchsorted(savings[row, step].cumsum(), overflow)+1)
        np.maximum.at(lod, priority[row[:length]], step[:length]+1)
        cost = cost_table[desired, lod]
        overflow = cost.sum()-settings.max_triangles
    if overflow > 0:
        retain = cost.cumsum() <= settings.max_triangles
        take, lod, cost = take[retain], lod[retain], cost[retain]
    return take, lod, cost


def scatter(surfaces, variants, settings, *, guides=(), footprints=(), protected=(), weights=None):
    xyz, normal, paint, roll, requested = make_candidates(surfaces, settings)
    candidates = len(xyz)
    mix = FAMILY_WEIGHTS if weights is None else weights
    enabled = [i for i, item in enumerate(variants) if mix.get(item.family, 0) > 0]
    if not enabled or not candidates:
        return Placement(xyz[:0], xyz[:0], xyz[:0], np.empty(0, int), np.empty(0, int),
                         np.empty(0, int), candidates, 0, requested)
    xy = xyz[:, :2]
    max_tilt = math.radians(settings.slope_limit)*settings.align*math.sqrt(2.)
    spread = max(item.radius+item.height*settings.height*1.14*max_tilt for item in variants)*settings.scale[1]
    tread, verge = guide_fields(xy, guides, spread)
    wall = wall_fields(xy, footprints, spread+settings.wall_gap+settings.wall_verge)
    manual = manual_fields(xy, np.asarray(protected, dtype=float).reshape(-1, 3), spread)
    verge = np.maximum(verge, paint[:, 3])
    shelter = (1-smooth(settings.wall_gap, settings.wall_gap+max(.001, settings.wall_verge), wall))
    broad = noise(xy, settings.patch_size, settings.seed+247)
    medium = noise(xy, settings.patch_size*.38, settings.seed+301)
    detail = noise(xy, settings.patch_size*.15, settings.seed+529)
    patches = .52*broad+.33*medium+.15*detail
    colony = smooth(.34, .69, patches)
    slope = normal[:, 2]
    low, high = np.quantile(xyz[:, 2], (.07, .93))
    relative_z = smooth(low, high+max(.01, (high-low)*.12), xyz[:, 2])
    wet = np.clip(settings.moisture + (paint[:, 2]-.5)*.82 + .35*(medium-.5)
                  + .27*(.5-relative_z) + .11*shelter - .20*(1-slope), 0, 1)
    ruggedness = smooth(.71, 1., slope)
    base = (1-settings.clustering)*.64 + settings.clustering*(.026+1.08*colony)
    boost = settings.density_boost*(verge*.62+shelter*.82)*(.23+.77*smooth(.19,.72,medium))
    chance = np.clip((base+boost)*paint[:, 0]*(1-paint[:, 1])*(.45+.55*ruggedness), 0, 1)
    legal = (roll[:, 3] < chance) & (tread >= 0) & (wall >= settings.wall_gap) & (manual >= 0)
    if settings.elevation is not None:
        legal &= (xyz[:, 2] >= settings.elevation[0]) & (xyz[:, 2] <= settings.elevation[1])
    subset = np.flatnonzero(legal)
    # Reserve most of the margin for short cover. Wetness and each approved
    # asset's habitat metadata select the family within its own layer.
    blend = np.clip(settings.filler + .15*verge + .12*shelter - .24*colony, 0., 1.)
    allowed = np.array([variants[i].filler for i in enabled])
    variant = np.empty(len(subset), dtype=np.int32)
    for rows in np.array_split(np.arange(len(subset)), max(1, math.ceil(len(subset)/8192))):
        selected = subset[rows]
        compatibility = []
        for index in enabled:
            item = variants[index]
            suitability = np.exp(-6*(wet[selected]-item.moisture)**2)
            shoulder = 1.+verge[selected]*(item.edge-.38)
            density = min(1.6, (item.patch_density/(75. if item.filler else 23.))**.32)
            state = (1+.24*(wet[selected]-.5)) if item.stage in {"Young", "Light"} else 1.
            compatibility.append(mix[item.family]*suitability*shoulder*density*state)
        table = np.asarray(compatibility).T
        if allowed.any() and not allowed.all():
            table[:, allowed] *= (blend[selected] / table[:, allowed].sum(axis=1))[:, None]
            table[:, ~allowed] *= ((1-blend[selected]) / table[:, ~allowed].sum(axis=1))[:, None]
        cumulative = table.cumsum(axis=1)
        target = roll[selected, 4]*cumulative[:, -1]
        choice = np.minimum(np.sum(cumulative <= target[:, None], axis=1), len(enabled)-1)
        variant[rows] = np.asarray(enabled)[choice]
    uniform_scale = settings.scale[0]+(settings.scale[1]-settings.scale[0])*roll[subset, 5]
    yaw = settings.heading+(2*roll[subset, 7]-1)*settings.rotation
    n = normal[subset]
    nx = n[:, 0]*np.cos(yaw)+n[:, 1]*np.sin(yaw)
    ny = -n[:, 0]*np.sin(yaw)+n[:, 1]*np.cos(yaw)
    euler = np.column_stack((-settings.align*np.arctan2(ny, n[:, 2]),
                            settings.align*np.arctan2(nx, n[:, 2]), yaw))
    height = uniform_scale*settings.height*(.86+.28*roll[subset, 6])
    radius = np.asarray([item.radius for item in variants])[variant]*uniform_scale
    radius += np.asarray([item.height for item in variants])[variant]*height*np.linalg.norm(euler[:, :2], axis=1)
    room = (tread[subset] >= radius) & (wall[subset] >= settings.wall_gap+radius) & (manual[subset] >= radius)
    subset, variant, uniform_scale = subset[room], variant[room], uniform_scale[room]
    euler, height = euler[room], height[room]
    habitat_count = len(subset)
    if settings.lod_origin is None:
        distance = np.full(len(subset), settings.lod_distances[0])
    else:
        distance = np.linalg.norm(xyz[subset]-settings.lod_origin, axis=1)
    lod = np.sum(distance[:, None] >= settings.lod_distances, axis=1)
    chosen, lod, cost = budget_lods(variants, variant, lod, roll[subset, 8], distance, settings)
    subset, variant, uniform_scale = subset[chosen], variant[chosen], uniform_scale[chosen]
    scale = np.column_stack((uniform_scale, uniform_scale, height[chosen]))
    assets = np.asarray([item.indices for item in variants])[variant, lod]
    return Placement(xyz[subset], euler[chosen], scale, assets, lod, cost, candidates, habitat_count, requested)
