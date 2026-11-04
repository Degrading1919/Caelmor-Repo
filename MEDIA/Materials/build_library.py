"""Build deterministic original PNG masters and Procreate OBJ packages."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image
import numpy as np

from texture_design import generate

ROOT=Path(__file__).resolve().parent
PILOT=('split_oak_shingle','coursed_fieldstone','split_slate','hewn_oak','forged_iron','plain_linen')
CHANNELS={'map_Kd':'color.png','map_roughness':'roughness.png',
          'map_metallic':'metallic.png','map_tangentSpaceNormal':'normal.png'}


def catalog():
    data=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['materials']
    ids=[row['id'] for row in data]
    if len(data)!=100 or len(set(ids))!=100 or [r['rank'] for r in data]!=list(range(1,101)):
        raise ValueError('Expected 100 uniquely ranked material masters')
    if tuple(ids[:6])!=PILOT or any(not re.fullmatch('[a-z][a-z0-9_]+',value) for value in ids):
        raise ValueError('Invalid material ID or pilot ranking')
    return data


def write_bytes(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_bytes()!=value:
        raise FileExistsError(f'{path}: choose a fresh output folder for a changed build')
    path.write_bytes(value)


def png(array):
    with BytesIO() as buffer:
        Image.fromarray(array).save(buffer,format='PNG',compress_level=5)
        return buffer.getvalue()


def model(record, template):
    # Template source is Blender Z-up. Publish Y-up OBJ. Scale local U/V
    # separately, preserving metric repeat metadata and the same paint chart.
    vertices=[tuple(map(float,line[2:].split())) for line in template.splitlines() if line.startswith('v ')]
    extent=[max(p[i] for p in vertices)-min(p[i] for p in vertices) for i in (0,1)]
    u,v=record['scale_m']
    factor=(u/extent[0],v/extent[1],min(u/extent[0],v/extent[1]))
    result=[]
    index=0
    for line in template.splitlines():
        if line.startswith('v '):
            x,y,z=(v*s for v,s in zip(vertices[index],factor))
            line=f'v {x:.9f} {z:.9f} {-y:.9f}'
            index+=1
        elif line.startswith('o '):
            line='o '+record['id']
        elif line=='usemtl CaelmorMaterial':
            line='usemtl '+record['id']
        result.append(line)
    return ('\n'.join(result)+'\n').encode('ascii')


def materials_file(identity):
    return ('\n'.join([f'newmtl {identity}','Kd 1.0 1.0 1.0','d 1.0',
                      *[f'{key} {filename}' for key,filename in CHANNELS.items()]])+'\n').encode('ascii')


def archive(identity, files):
    with BytesIO() as buffer:
        with ZipFile(buffer,'w') as out:
            for filename,value in sorted(files.items()):
                info=ZipInfo(f'{identity}/{filename}',(2026,11,4,0,0,0))
                info.compress_type=ZIP_DEFLATED
                info.external_attr=0o644<<16
                out.writestr(info,value,compresslevel=4)
        return buffer.getvalue()


def build(records, out, templates, resolution):
    for record in records:
        identity=record['id']
        maps=generate(record,resolution)
        files={channel+'.png':png(array) for channel,array in maps.items()}
        material_metadata={**record,'resolution':resolution,'color_space':'sRGB grayscale baseline',
                           'normal_space':'tangent +Y','paint_uv':'one non-overlapping repeat',
                           'map_files':{channel:channel+'.png' for channel in maps}}
        files['metadata.json']=(json.dumps(material_metadata,indent=2,ensure_ascii=True)+'\n').encode()
        template=(templates/(record['template']+'.obj')).read_text(encoding='ascii')
        files['material.obj']=model(record,template)
        files['material.mtl']=materials_file(identity)
        data=archive(identity,files)
        write_bytes(out/'masters'/(identity+'.png'),files['master.png'])
        write_bytes(out/'packages'/(identity+'.zip'),data)
        print(f"{record['rank']:03} {identity} {len(data):,} bytes",flush=True)


def apply_palette(values, stops):
    """Match Blender's linear ColorRamp with sRGB-encoded source and stops."""
    decode=lambda x:np.where(x<=.04045,x/12.92,((x+.055)/1.055)**2.4)
    stops=decode(np.array([[int(color[i:i+2],16) for i in (1,3,5)] for color in stops])/255.)
    factor=decode(values/255.)
    levels=np.linspace(0,1,4)
    color=np.stack([np.interp(factor,levels,stops[:,i]) for i in range(3)],axis=-1)
    encoded=np.where(color<=.0031308,12.92*color,1.055*color**(1./2.4)-.055)
    return np.round(encoded*255).astype(np.uint8)


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--id',action='append',default=[],help='Build only these catalog IDs')
    parser.add_argument('--out',type=Path,default=ROOT)
    parser.add_argument('--templates',type=Path,default=ROOT/'templates')
    parser.add_argument('--resolution',type=int,choices=(512,1024,2048),default=512)
    args=parser.parse_args()
    if args.pilot and args.id:
        parser.error('Choose --pilot or one or more --id options')
    if args.pilot and args.out.resolve()==ROOT:
        parser.error('--pilot needs a separate disposable --out folder')
    data=catalog()
    if args.id:
        unknown=set(args.id)-{r['id'] for r in data}
        if unknown:
            parser.error('Unknown material IDs: '+', '.join(sorted(unknown)))
        data=[r for r in data if r['id'] in args.id]
    elif args.pilot:
        data=data[:len(PILOT)]
    build(data,args.out,args.templates,args.resolution)


if __name__=='__main__':
    main()
