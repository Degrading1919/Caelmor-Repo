"""Construction-led visual refinement for the two art benchmark families only.

These are reversible art treatments within existing regional construction,
not new lore, props, occupied masses or functional programs.
"""
from .crafted_geometry import replace_box_components,bevel_open_box_front

PALETTES={
    ('LOWMARK','SMITHY'):{
        'timber':(.105,.060,.030,1.),'timber_light':(.19,.115,.060,1.),
        'stone':(.25,.265,.235,1.),'stone_light':(.34,.35,.31,1.),'mortar':(.16,.17,.145,1.),
        'plaster':(.64,.56,.405,1.),'plaster_patch':(.61,.55,.41,1.),
        'roof':(.205,.145,.084,1.),'roof_dark':(.1845,.1305,.0756,1.),
        'roof_worn':(.20,.15,.095,1.),'roof_patch':(.209,.148,.086,1.),
        'iron':(.045,.052,.055,1.),'stone_sooted':(.17,.165,.14,1.)},
    ('THORNFELL','GATEHOUSE'):{
        'timber':(.105,.067,.038,1.),'timber_light':(.17,.12,.072,1.),
        'stone':(.265,.295,.305,1.),'stone_light':(.39,.405,.395,1.),'mortar':(.155,.18,.19,1.),
        'roof':(.075,.125,.155,1.),'roof_dark':(.0675,.1125,.1395,1.),
        'roof_worn':(.080,.126,.151,1.),'roof_patch':(.076,.127,.158,1.),
        'iron':(.045,.055,.065,1.)}
}


def palette(key,settings):
    if settings is None or not getattr(settings,'world_aware',False):return None
    return PALETTES.get((settings.region,settings.function),{}).get(key)


def surface_base(key,buffer_name,settings,base):
    # Wall field is local coursed stone; quoins, arch and bearing bands receive
    # more carefully dressed stock. Sharing the old stone_light key must not
    # make the entire fortification as pale as its dressed portal.
    if uses_masonry_stock(buffer_name,settings):
        return (.295,.315,.32,1.)
    return base


def uses_masonry_stock(buffer_name, settings):
    return (settings.world_aware and (settings.region,settings.function)==('THORNFELL','GATEHOUSE')
            and '.facade_masonry_skin' in buffer_name)


def uses_hewn_pigment(buffer_name, settings):
    return (settings.world_aware and (settings.region,settings.function)==('LOWMARK','SMITHY')
            and any(part in buffer_name for part in (
                '.smithy.primary_end_bent', '.smithy.tie_knees.', '.smithy.stock_bents',
                '.Roof edge fascia')))


def masonry_stock_tint(centers, seed):
    """One mineral tint per stone, with related stock in adjacent courses."""
    import numpy as np
    from .surface_patterns import _noise

    x,y,z=np.asarray(centers).T
    seed=seed & 0xffff
    # Sample at the connected stone's center so its front and bevel share
    # stock. Two crossed fields avoid straight stripes on orthogonal walls.
    stock=np.clip(1.45*(.72*_noise(x+.64*y,z,.68,.73,seed+271)
                       +.28*_noise(y-.46*x,z,1.05,1.22,seed+389)),-1.,1.)
    # Iron-tinted and cooler stock bracket the regional stone palette. This
    # changes diffuse color with little change in value. The dressed surrounds
    # keep their separate palette and the geometry supplies the joint shadows.
    return 1.+stock[:,None]*np.array([.185,.035,-.155])


def refine(ctx):
    """Work existing visible arrises; preserve all aperture and roof domains."""
    pair=(ctx.settings.region,ctx.settings.function)
    if pair not in PALETTES:return
    for buffer in ctx.buffers:
        name=buffer.name
        if '.facade_masonry_skin' in name and pair[0]=='THORNFELL':
            bevel_open_box_front(buffer,inset=.035,depth=.016)
        elif buffer.material in ('stone','stone_light') and any(part in name for part in (
                'bonded_quoins','portal_jamb','stringcourse','loop_reveals','stack_courses','post_stone_shoes')):
            replace_box_components(buffer,bevel=.010 if 'stack_courses' in name else .025,
                predicate=lambda _b,_c,size:min(size)>.075)
