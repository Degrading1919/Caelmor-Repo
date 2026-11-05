"""Use the established contact-sheet helper, preserving individual PNGs."""
from pathlib import Path
from PIL import Image, ImageChops
import json
import compose_construction_library as layout

ROOT=Path(__file__).resolve().parents[1]/'evidence'/'floor_visibility'


def main():
    layout.ROOT=ROOT
    records=json.loads((ROOT/'metrics.json').read_text())['cases']
    errors=[]
    for mode in ('clay','material'):
        frames=[]
        for case in records:
            name=case['case']
            states=('exterior','floor0','restored')
            frames.append((name,[ROOT/f'{name}_{mode}_{s}.png' for s in states]))
            baseline=Image.open(ROOT/f'{name}_{mode}_legacy.png').convert('RGB')
            full=Image.open(ROOT/f'{name}_{mode}_exterior.png').convert('RGB')
            restored=Image.open(ROOT/f'{name}_{mode}_restored.png').convert('RGB')
            import numpy as np
            restore_delta=abs(np.asarray(full).astype(float)-np.asarray(restored).astype(float))
            # EEVEE/GPU output can differ by one 8-bit quantization step.
            assert restore_delta.max() <= 1, (name,mode,'restore differs')
            delta=abs(np.asarray(full).astype(float)-np.asarray(baseline).astype(float))
            assert delta.mean() < .01 and (delta.max(axis=2)>8).mean() < .001, (name,mode,'assembled appearance changed')
            errors.append(dict(case=name,mode=mode,mean_channel_delta=float(delta.mean()),
                               restore_max_channel_delta=float(restore_delta.max()),
                               fraction_pixels_over_8=float((delta.max(axis=2)>8).mean())))
        layout.sheet(f'floor_{mode}.jpg',('Full exterior','Interior floor 0 preview','Exterior restored'),frames,width=640)
    layout.sheet('three_storey_progression.jpg',('Full exterior','Ground floor 0','Floor 1','Floor 2'),[
        (mode,[ROOT/f'lowmark_3f_{mode}_{s}.png' for s in ('exterior','floor0','floor1','floor2')])
        for mode in ('clay','material')],width=560)
    (ROOT/'pixel_comparison.json').write_text(json.dumps(errors,indent=2)+'\n')
    print(json.dumps(errors,indent=2))


if __name__=='__main__': main()
