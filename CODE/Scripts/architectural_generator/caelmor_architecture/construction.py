"""Semantic component selection, independent of mesh names and palette slots."""
from dataclasses import dataclass, field
from .construction_library import VARIANTS

TREATMENTS = {
    'stone_masonry': ('wall_body', 'plinth', 'arch_ring', 'vault'),
    'dressed_stone': ('wall_body', 'plinth', 'arch_ring', 'vault', 'opening_trim'),
    'structural_timber': ('frame_member', 'roof_support'),
    'wooden_boarding': ('wall_infill', 'boarding', 'roof_deck'),
    'wooden_shingles': ('roof_cover',),
    'slate_tile_roofing': ('roof_cover',),
    'plaster_limewash': ('wall_infill', 'wall_surface'),
}
STONE = ('fieldstone', 'ridge_stone', 'volcanic_stone')
STOCK = {
    'stone_masonry': STONE, 'dressed_stone': STONE,
    'structural_timber': ('structural_wood',), 'wooden_boarding': ('sawn_wood',),
    'wooden_shingles': ('split_wood',), 'slate_tile_roofing': ('slate', 'fired_clay'),
    'plaster_limewash': ('lime_render', 'earthen_render', 'limewash'),
}
ROLES = frozenset(role for roles in TREATMENTS.values() for role in roles)
COVERS = {'SHINGLE': ('wooden_shingles', 'split_wood'),
          'SLATE': ('slate_tile_roofing', 'slate'),
          'CLAY': ('slate_tile_roofing', 'fired_clay')}
COVER_FROM_STOCK = {stock: cover for cover, (_, stock) in COVERS.items()}
PROVENANCE = ('component_id', 'component_role', 'treatment', 'substrate', 'surface_family',
              'finish', 'host_component', 'variant', 'representation')


def _choice(component, field, value, allowed):
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f"{component}: {field} {value!r}; allowed: {', '.join(sorted(allowed))}")
    return value


@dataclass(frozen=True)
class Construction:
    component_id: str
    component_role: str
    treatment: str
    substrate: str
    surface_family: str
    finish: str = 'procedural'
    host_component: str | None = None
    variant: str | None = None
    representation: str | None = None


@dataclass
class Resolver:
    overrides: dict
    region: str
    finish_names: tuple = ()
    components: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.overrides, dict) or self.overrides.keys() - {'by_component', 'by_role'}:
            raise ValueError('construction_overrides requires an object with by_component and/or by_role')
        finishes = ('procedural', *(f'material:{name}' for name in self.finish_names))
        registered = {
            'treatment': TREATMENTS, 'substrate': set().union(*STOCK.values()),
            'surface_family': ('stone', 'wood', 'roof', 'plaster'), 'finish': finishes,
            'variant': {variant for options in VARIANTS.values() for variant in options},
            'representation': ('MODELED','HYBRID','TEXTURE'),
        }
        for scope in ('by_role', 'by_component'):
            entries = self.overrides.get(scope, {})
            if not isinstance(entries, dict):
                raise ValueError(f'construction_overrides.{scope} requires an object')
            for key, fields in entries.items():
                if scope == 'by_role':
                    _choice(scope, 'role', key, ROLES)
                if not isinstance(key, str) or not key or not isinstance(fields, dict):
                    raise ValueError(f'{scope}: each component key needs an object of registered fields')
                for field_name, value in fields.items():
                    _choice(key, 'field', field_name, registered)
                    _choice(key, field_name, value, registered[field_name])

    def requested(self, key, role):
        return (key in self.overrides.get('by_component', {}) or
                role in self.overrides.get('by_role', {}))

    def resolve(self, key, role, default, *, stock=None, treatments=None, host=None,
                mapped=True):
        if key in self.components:
            raise ValueError(f'{key}: duplicate construction component')
        specific = self.overrides.get('by_component', {}).get(key, {})
        fields = {**self.overrides.get('by_role', {}).get(role, {}), **specific}
        if not mapped:
            if specific.get('representation') in ('HYBRID','TEXTURE'):
                raise ValueError(f'{key}: this structural assembly requires modeled geometry')
            fields.pop('representation',None)
        allowed = treatments or tuple(t for t, roles in TREATMENTS.items() if role in roles)
        treatment = _choice(key, 'treatment', fields.get('treatment', default), allowed)
        stocks = STOCK[treatment]
        if role == 'wall_infill' and treatment == 'plaster_limewash':
            stocks = ('lime_render', 'earthen_render')
        if role == 'wall_surface' and host not in self.components:
            raise ValueError(f'{key}: wall_surface requires a resolved host')
        if stock not in stocks:
            stone = dict(LOWMARK='fieldstone', THORNFELL='ridge_stone',
                         MIRE='fieldstone', EMBERHOLT='volcanic_stone')[self.region]
            stock = stone if stocks == STONE else stocks[0]
        substrate = _choice(key, 'substrate', fields.get('substrate', stock), stocks)
        family = ('stone' if substrate in STONE else 'roof' if role == 'roof_cover'
                  else 'plaster' if treatment == 'plaster_limewash' else 'wood')
        surface = _choice(key, 'surface_family', fields.get('surface_family', family), (family,))
        variant = fields.get('variant')
        if variant is not None:
            allowed_variants = tuple(name for name, roles in VARIANTS.get(treatment, {}).items()
                                     if role in roles)
            _choice(key, 'variant', variant, allowed_variants)
        representation = fields.get('representation')
        if representation and role not in ('wall_body','roof_cover'):
            _choice(key,'representation',representation,())
        result = Construction(key, role, treatment, substrate, surface,
                              fields.get('finish', 'procedural'), host, variant, representation)
        self.components[key] = result
        return result

    def finish(self):
        for scope, allowed in (('by_component', self.components),
                               ('by_role', {c.component_role for c in self.components.values()})):
            for key in self.overrides.get(scope, {}):
                _choice(scope, 'component' if scope == 'by_component' else 'role', key, allowed)


def component(plan, slot, role, treatment, **constraints):
    resolver = getattr(plan, 'construction_resolver', None)
    if resolver is None:
        return None
    spec = resolver.resolve(f'{plan.construction_zone}/{slot}', role, treatment, **constraints)
    if spec.representation in ('HYBRID','TEXTURE') and plan.settings.geometry_mode!='EFFICIENT':
        raise ValueError(f'{spec.component_id}: {spec.representation} representation requires Efficient geometry')
    return spec


def bind(spec, *buffers):
    for buffer in buffers:
        buffer.construction = spec
    return spec
