"""Vertical-slice evidence captured with the existing studio and renderer."""
from dataclasses import replace
import json
from pathlib import Path
import sys

import bpy

sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_construction_treatments as studio
from test_construction_library import PRESETS, overrides


def main():
    studio.OUT=studio.ROOT/'evidence'/'construction_library'
    specs=studio.CASE_SPECS
    settings=studio.settings
    records=[]
    fixture=replace(settings('SMITHY'),crafted_curves=True,seed_massing=True)
    specs['SMITHY']['targets']['close']=(2.8,.24,2.25)
    specs['SMITHY']['scales']['close']=7.4
    specs['SMITHY']['directions']['close']=((.36,-1.2,.47),(-.8,-1.2,.4))
    for name in PRESETS:
        records.append(studio.record('SMITHY',replace(fixture,construction_overrides=overrides(name)),
                                     name,('normal','close')))
    specs['STABLE']=dict(specs['SMITHY'],targets={'normal':(8.7,3.,2.7)},scales={'normal':31.})
    stable=replace(settings('STABLE'),construction_overrides=overrides('render_slate'))
    records.append(studio.record('STABLE',stable,'render_slate',('normal',)))
    gate=replace(settings('GATEHOUSE'),crafted_curves=True,seed_massing=True,
                 construction_overrides={})
    previous=studio.ROOT/'evidence'/'construction_treatments'/'manifest.json'
    control=json.loads(previous.read_text(encoding='utf-8'))
    before=next(c for c in control['cases'] if c['function']=='GATEHOUSE' and c['variant']=='after')
    close=next(frame for frame in before['images'] if frame['distance']=='close')
    specs['GATEHOUSE']['targets']['close_front']=close['camera_target']
    specs['GATEHOUSE']['scales']['close']=close['ortho_scale']
    specs['GATEHOUSE']['scales']['normal']=32.
    revised=studio.record('GATEHOUSE',gate,'bonded_returns',('normal','close'))
    for a,b in zip(before['images'],revised['images'],strict=True):
        assert all(a[field]==b[field] for field in ('camera_location','camera_target','ortho_scale'))
    records.append(revised)
    (studio.OUT/'manifest.json').write_text(json.dumps(dict(blender=bpy.app.version_string,
        base_revision='67cba19',source_sha256=studio.source_hashes(),cases=records),indent=2)+'\n')


if __name__=='__main__':
    main()
