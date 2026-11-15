"""Exercise the artist-facing Blender operators and contextual action routing."""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import bpy

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]

from caelmor_architecture import _active_build, register
from caelmor_architecture.authoring_ui import draw
from caelmor_architecture.blender_backend import export_building, load_settings
from test_blockout_authoring_blender import select, scene_material
from test_condition_export import read_glb
from test_opening_guides_blender import face


class Actions:
    """Record UI requests while Blender supplies the real scene and selection."""
    def __init__(self):
        self.actions = []
        self.controls = []

    def row(self, **_):
        return self

    def operator(self, name, **_):
        self.actions.append(name)
        return SimpleNamespace()

    def prop(self, props, name, **_):
        self.controls.append(name)

    def label(self, **_):
        pass

    def separator(self):
        pass


def actions():
    layout = Actions()
    draw(layout,bpy.context)
    return set(layout.actions)


def volumes(collection):
    return json.loads(collection['caelm_editable_volumes'])


def role(collection,name):
    return next(o for o in collection.objects if o.get('caelm_component_role')==name)


def object_of(collection, identity):
    return next(o for o in collection.objects if o.get('caelm_buffer_id')==identity)


def exported(collection, folder):
    folder.mkdir()
    path = folder/'cottage.glb'
    export_building(collection,str(path))
    visual,_ = read_glb(path)
    return ({n['name'] for n in visual['nodes']},path.with_suffix('.collision.glb').read_bytes(),
            json.loads(path.with_suffix('.caelmor.json').read_text())['floor_presentation'])


def rejected(**kwargs):
    try:
        assert bpy.ops.caelmor.edit_building(**kwargs)=={'CANCELLED'}
    except RuntimeError as exc:
        return str(exc)
    return ''


def main(scratch):
    register()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    assert actions()=={'caelmor.create_building'}
    p = bpy.context.scene.caelmor_settings
    p.caelm_authoring_tool = 'ROOF'
    assert 'caelmor.roof_preview' in actions()
    p.caelm_authoring_tool = 'AUTO'

    # Recommended creation and a manual envelope can coexist in separate
    # buildings. Rebuild always reads the selected building, never the draft.
    assert bpy.ops.caelmor.create_building(function='COTTAGE',region='LOWMARK')=={'FINISHED'}
    other = _active_build(bpy.context)
    assert load_settings(other)['use_grammar']
    assert not load_settings(other).get('manual_shape')
    before = other['caelm_settings']
    assert bpy.ops.caelmor.create_building(function='COTTAGE',region='THORNFELL',method='MANUAL',
                                          width=12.2,depth=8.,floors=2,floor_height=2.9)=={'FINISHED'}
    stone = _active_build(bpy.context)
    assert abs(volumes(stone)['thornfell_stone_hall']['width']-12.2)<1e-5
    assert load_settings(stone)['use_grammar'] and load_settings(stone)['world_aware']
    assert bpy.ops.caelmor.edit_building(action='SHAPE',width=12.6,depth=8.5,floors=2,
                                        floor_height=2.9)=={'FINISHED'}
    assert abs(volumes(stone)['thornfell_stone_hall']['width']-12.6)<1e-5
    assert other['caelm_settings']==before

    # Fitting also uses raised regional floor datums, independent of style.
    bpy.ops.mesh.primitive_cube_add(size=2.,location=(25.,0.,2.4))
    mire_box = bpy.context.object
    mire_box.scale = (4.5,3.75,2.4)
    assert bpy.ops.caelmor.create_building(function='COTTAGE',region='MIRE',method='BOX',floors=1)=={'FINISHED'}
    mire = _active_build(bpy.context)
    raised = volumes(mire)['mire_longhouse']
    assert mire['caelm_blockout_source']==mire_box
    assert abs(raised['width']-9.)<1e-5 and abs(raised['depth']-7.5)<1e-5
    zone = json.loads(mire['caelm_construction_zones'])[0]
    assert zone['base']>1.0 and abs(zone['eave']-4.8)<1e-5

    bpy.ops.mesh.primitive_cube_add(size=2.,location=(8.,-4.,1.55))
    proxy = bpy.context.object
    proxy.scale = (4.,3.,1.55)
    proxy.rotation_euler.z = .37
    original = [tuple(v.co) for v in proxy.data.vertices]
    assert bpy.ops.caelmor.create_building(function='COTTAGE',region='LOWMARK',method='BOX',floors=1)=={'FINISHED'}
    cottage = _active_build(bpy.context)
    assert cottage['caelm_blockout_source']==proxy
    assert [tuple(v.co) for v in proxy.data.vertices]==original
    anchor = next(o for o in cottage.objects if o.get('caelm_anchor'))
    selected = role(cottage,'roof_cover')
    select(selected)
    assert bpy.ops.caelmor.edit_building(action='ROOF',style='HIP',custom_pitch=True,pitch=42.,
                                        custom_overhang=True,overhang=.35)=={'FINISHED'}
    skeleton = volumes(cottage)
    assert skeleton['lowmark_main_hall']['style']=='HIP'
    assert skeleton['lowmark_main_hall']['pitch']==42.
    assert load_settings(cottage)['world_aware'] and load_settings(cottage)['region']=='LOWMARK'
    assert bpy.ops.caelmor.edit_building(action='CONSTRUCTION',cover='slate')=={'FINISHED'}
    assert role(cottage,'roof_cover')['caelm_substrate']=='slate'

    # The legacy/native material slot route also supports parts without a
    # construction role, including window meshes across storeys.
    windows = next(o for o in cottage.objects if o.get('caelm_layer')=='windows')
    window_key = windows['caelm_buffer_id']
    glass = scene_material('Artist window finish',(.19,.29,.39))
    select(windows)
    assert 'caelmor.edit_building' in actions()
    assert bpy.ops.caelmor.edit_building(action='MATERIAL',material=glass.name)=={'FINISHED'}
    assert object_of(cottage,window_key).data.materials[0]==glass
    wall = next(o for o in cottage.objects if 'facade_foundation_core' in o.get('caelm_buffer_id',''))
    wall_key = wall['caelm_buffer_id']
    select(wall)
    assert bpy.ops.caelmor.protect_selected()=={'FINISHED'}
    wall.data.vertices[0].co.x += .011
    changed = wall.data.vertices[0].co.copy()
    tiled = scene_material('Artist roof finish',(.28,.18,.12))
    select(role(cottage,'roof_cover'))
    first = exported(cottage,scratch/'baseline')
    assert bpy.ops.caelmor.edit_building(action='MATERIAL',material=tiled.name,match_group=True,
                                        group='roof_cover')=={'FINISHED'}
    assert all(o.data.materials[0]==tiled for o in cottage.objects if o.get('caelm_component_role')=='roof_cover')
    assert exported(cottage,scratch/'material')==first
    assert object_of(cottage,wall_key)==wall and wall.data.vertices[0].co==changed

    # A selected source face exposes the guide command. Generated parts can
    # select their source again and guide operations use the saved hip roof.
    guide = face(cottage,'Artist rear window','rear',[(1.25,1.1),(2.15,1.1),(2.15,1.95),(1.25,1.95)])
    select(guide)
    assert 'caelmor.edit_feature' in actions()
    p.caelm_guide_target,p.caelm_guide_kind = cottage,'WINDOW'
    assert bpy.ops.caelmor.edit_feature()=={'FINISHED'}
    identifier = guide['caelm_guide']['id']
    generated = next(o for o in cottage.objects if f'.guide.{identifier}.' in o.get('caelm_buffer_id',''))
    select(generated)
    assert 'caelmor.select_feature_guide' in actions()
    assert bpy.ops.caelmor.select_feature_guide()=={'FINISHED'}
    assert bpy.context.view_layer.objects.active==guide
    guide.location.x -= .12
    assert bpy.ops.caelmor.opening_guide(action='REFRESH')=={'FINISHED'}
    assert guide['caelm_guide']['id']==identifier
    assert volumes(cottage)['lowmark_main_hall']['style']=='HIP'
    assert bpy.ops.caelmor.opening_guide(action='REMOVE')=={'FINISHED'}
    assert 'caelm_guide' not in guide

    select(anchor)
    assert bpy.ops.caelmor.load_settings()=={'FINISHED'}
    assert bpy.ops.caelmor.edit_building(action='CONDITION',age=45,maintenance=.55,
                                        craftsmanship='STANDARD')=={'FINISHED'}
    assert 'building changed' in rejected(action='REBUILD',target=stone.name,snapshot=before)
    assert load_settings(cottage)['age']==45 and other['caelm_settings']==before
    try:
        bpy.ops.caelmor.regenerate(require_draft=True)
    except RuntimeError as exc:
        assert 'advanced draft' in str(exc)
    else:
        raise AssertionError('The advanced draft overwrote a newer condition edit.')

    state = cottage['caelm_settings']
    name = cottage.name
    path = scratch/'artist_workflow.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    bpy.ops.wm.open_mainfile(filepath=str(path))
    cottage = bpy.data.collections[name]
    select(next(o for o in cottage.objects if o.get('caelm_anchor')))
    assert bpy.ops.caelmor.edit_building(action='REBUILD')=={'FINISHED'}
    assert cottage['caelm_settings']==state
    assert object_of(cottage,wall_key).get('caelm_protected')
    assert object_of(cottage,window_key).data.materials[0].name=='Artist window finish'
    assert role(cottage,'roof_cover').data.materials[0].name=='Artist roof finish'
    select(role(cottage,'roof_cover'))
    assert bpy.ops.caelmor.edit_building(action='MATERIAL',match_group=True,group='roof_cover',
                                        clear_material=True)=={'FINISHED'}
    assert role(cottage,'roof_cover').data.materials[0].name!='Artist roof finish'
    print('CAELMOR_ARTIST_WORKFLOW_PASS')


if __name__=='__main__':
    with TemporaryDirectory(prefix='artist_workflow_',dir=ROOT/'dist') as temporary:
        main(Path(temporary))
