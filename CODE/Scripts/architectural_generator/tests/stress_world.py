"""Independent varied-context/condition authoring gate, beyond fixed-seed matrix."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from caelmor_architecture.engine import generate, validate, geometry_hash
from caelmor_architecture.model import Settings
from caelmor_architecture.profiles import REGIONS, TYPE_SPECS


def main():
    started=time.perf_counter(); rng=random.Random(60713); cases=[]
    for ri,(region,spec) in enumerate(REGIONS.items()):
        for fi,function in enumerate(TYPE_SPECS):
            contexts=tuple(spec.contexts)
            requested=Settings(region=region,context=contexts[fi%len(contexts)],function=function,
                seed=rng.randrange(100000),wealth=('MODEST','ESTABLISHED','AFFLUENT')[fi%3],
                craftsmanship=('ROUGH','STANDARD','FINE')[(fi+ri)%3],
                age=(0.,70.,160.,240.)[(fi//2+ri)%4],maintenance=(.15,.5,.9)[(fi+ri)%3],
                window_density=(.4,1.,1.5)[fi%3],detail='HIGH' if fi%4==0 else 'MEDIUM',
                geometry_mode='EFFICIENT' if fi%2 else 'SOLID',use_grammar=True,world_aware=True)
            plan,buffers=generate(requested); result=validate(plan,buffers)
            assert result['valid'],(requested,result['errors'])
            assert len({b.name for b in buffers})==len(buffers)
            if region=='LOWMARK' and requested.age>=90 and requested.maintenance<.7 and requested.detail=='HIGH':
                assert any('sistered_repair_post' in b.name for b in buffers)
            if function in ('GATEHOUSE','MILLER','BOATHOUSE'):
                repeated=geometry_hash(generate(requested)[1])
                assert repeated==result['geometry_hash'],requested
            cases.append({'settings':asdict(requested),'result':result})
    report={'valid':True,'cases':cases,'seed':60713,'seconds':round(time.perf_counter()-started,3),
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted((ROOT/'caelmor_architecture').glob('*.py'))}}
    target=ROOT/'evidence'/'world_context_stress.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(cases),'valid':True,'seconds':report['seconds']}))


if __name__=='__main__':main()
