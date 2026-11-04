"""Curated assembly presets for the offline authoring controls."""
from copy import deepcopy

# A variant is a geometry choice within a treatment. The presets below simply
# write registered fields to the same resolver used by headless authoring.
VARIANTS = {
    'stone_masonry': {'broken_course': ('wall_body', 'plinth'),
                      'level_course': ('wall_body', 'plinth')},
    'structural_timber': {'hewn_pegged': ('frame_member', 'roof_support'),
                         'squared_housed': ('frame_member', 'roof_support')},
}

MASONRY = (
    ('broken_course', 'Broken-course stone', 'Staggered unequal stone beds and keyed headers',
     {'treatment':'stone_masonry', 'variant':'broken_course'}),
    ('level_course', 'Level-coursed stone', 'Level beds with regular stagger and alternate headers',
     {'treatment':'stone_masonry', 'variant':'level_course'}),
    ('dressed', 'Dressed stone', 'Fitted, worked units with controlled arrises',
     {'treatment':'dressed_stone'}),
)
TIMBER = (
    ('hewn', 'Hewn and pegged', 'Worked midsections and exposed pegged joints',
     {'treatment':'structural_timber', 'variant':'hewn_pegged'}),
    ('squared', 'Squared and housed', 'Straight sections and flush bearing shoulders',
     {'treatment':'structural_timber', 'variant':'squared_housed'}),
)

# Each control owns only the named construction fields on its role.
ASSEMBLIES = {
    'foundation': ('plinth', 'Foundation', MASONRY),
    'supports': ('frame_member', 'Structural supports', TIMBER),
    'masonry': ('wall_body', 'Masonry wall body', MASONRY),
    'enclosure': ('wall_infill', 'Frame enclosure', (
        ('board', 'Board and batten', 'Individually worked boards under joint battens',
         {'treatment':'wooden_boarding'}),
        ('lime', 'Lime render', 'Lime-rendered infill between supports',
         {'treatment':'plaster_limewash', 'substrate':'lime_render'}),
        ('earth', 'Earthen render', 'Thicker earthen-rendered infill',
         {'treatment':'plaster_limewash', 'substrate':'earthen_render'}),
    )),
    'rafters': ('roof_support', 'Roof structure', TIMBER),
    'cover': ('roof_cover', 'Roof covering', (
        ('wood', 'Split wooden shingles', 'Staggered lapped split wood',
         {'treatment':'wooden_shingles', 'substrate':'split_wood'}),
        ('slate', 'Slate', 'Thin fitted slate in lapped courses',
         {'treatment':'slate_tile_roofing', 'substrate':'slate'}),
        ('clay', 'Fired-clay tile', 'Shaped clay pans in lapped courses',
         {'treatment':'slate_tile_roofing', 'substrate':'fired_clay'}),
    )),
}
FINISH_ROLES = ('wall_body', 'wall_infill', 'roof_cover')


def enum_items(options):
    return [('AUTO','Regional default','Use the local construction assembly'),
            *[(key,label,help_text) for key,label,help_text,_ in options]]


def selected(options, fields):
    for key,_,_,preset in options:
        if all(fields.get(field)==value for field,value in preset.items()):
            return key
    return 'AUTO'


def replace_choice(roles, role, options, key):
    fields = roles.setdefault(role,{})
    for field in {field for _,_,_,preset in options for field in preset}:
        fields.pop(field,None)
    for candidate,_,_,preset in options:
        if candidate==key:
            fields.update(preset)
            break
    if not fields:
        roles.pop(role)


def authored_overrides(props, original):
    """Overlay UI edits while retaining exact legacy and per-component fields."""
    output = deepcopy(original)
    roles = output.get('by_role',{})
    for name,(role,_,options) in ASSEMBLIES.items():
        choice = getattr(props,'caelm_assembly_'+name)
        if choice != selected(options,original.get('by_role',{}).get(role,{})):
            replace_choice(roles,role,options,choice)
    role = props.caelm_finish_role
    if props.caelm_edit_finish:
        fields = roles.setdefault(role,{})
        mat = props.caelm_finish_material
        fields['finish'] = 'material:'+mat.name if mat else 'procedural'
    if roles:
        output['by_role'] = roles
    elif 'by_role' in output and original.get('by_role'):
        output.pop('by_role')
    return output

def timber_workmanship(settings):
    return {'FINE':.68,'STANDARD':1.,'ROUGH':1.20}[settings.craftsmanship]
