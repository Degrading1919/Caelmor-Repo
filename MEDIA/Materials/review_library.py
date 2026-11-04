"""Verify packages, generate a machine-readable inventory and review sheets."""
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from build_library import CHANNELS, PILOT, ROOT, apply_palette, catalog


def check_model(raw, identity):
    lines=raw.decode('ascii').splitlines()
    assert 'mtllib material.mtl' in lines and f'usemtl {identity}' in lines
    vertices=[tuple(map(float,line[2:].split())) for line in lines if line.startswith('v ')]
    coords=[tuple(map(float,line[3:].split())) for line in lines if line.startswith('vt ')]
    faces=[line[2:].split() for line in lines if line.startswith('f ')]
    side=round(len(coords)**.5)
    assert side*side==len(vertices)==len(coords) and side>=2
    assert np.all(np.isfinite(vertices))
    for index,(u,v) in enumerate(coords):
        assert abs(u-(index%side)/(side-1))<1e-8 and abs(v-(index//side)/(side-1))<1e-8
    actual=[]
    for face in faces:
        refs=[tuple(map(int,ref.split('/'))) for ref in face]
        assert len(refs)==4 and all(a==b for a,b in refs)
        actual.append(tuple(a for a,_ in refs))
    expected={(a,a+1,a+side+1,a+side)
              for j in range(side-1) for i in range(side-1) for a in (j*side+i+1,)}
    assert len(actual)==len(expected) and set(actual)==expected
    verts=np.asarray(vertices)
    for face in actual:
        a,b,c,d=verts[np.array(face)-1]
        assert np.linalg.norm(np.cross(b-a,d-a))>1e-10
    return len(vertices), len(faces)


def verify(record,out):
    identity=record['id']
    master=out/'masters'/(identity+'.png')
    path=out/'packages'/(identity+'.zip')
    with ZipFile(path) as z:
        prefix=identity+'/'
        assert len(z.namelist())==len(set(z.namelist()))==9
        assert all(name.startswith(prefix) and '/' not in name[len(prefix):] for name in z.namelist())
        read=lambda name:z.read(prefix+name)
        metadata=json.loads(read('metadata.json'))
        assert all(metadata[k]==value for k,value in record.items())
        size=metadata['resolution']
        maps={}
        for map_type,filename in metadata['map_files'].items():
            with Image.open(BytesIO(read(filename))) as image:
                assert image.size==(size,size), (identity,filename,image.size)
                assert image.mode==('RGB' if map_type in ('color','normal') else 'L')
                maps[map_type]=np.asarray(image)
        assert set(maps)=={'color','master','height','roughness','metallic','normal'}
        assert np.ptp(maps['master'])>=14 and np.std(maps['master'])>=3
        assert np.ptp(maps['height'])>=10 and np.ptp(maps['normal'])>=15
        assert np.array_equal(maps['color'],np.repeat(maps['master'][...,None],3,axis=-1))
        assert master.read_bytes()==read('master.png')
        mtl=read('material.mtl').decode('ascii').splitlines()
        assert f'newmtl {identity}' in mtl
        assert dict(line.split(maxsplit=1) for line in mtl if line.startswith('map_'))==CHANNELS
        vertices,quads=check_model(read('material.obj'),identity)
        gray=maps['master'].astype(float)
        jumps=(np.mean(abs(gray[0]-gray[-1])),np.mean(abs(gray[:,0]-gray[:,-1])))
        # A regular course may cross the repeat. Compare the border against
        # real interior rows or columns, not a flat-image absolute limit.
        inside=(np.mean(abs(np.diff(gray,axis=0)),axis=1),
                np.mean(abs(np.diff(gray,axis=1)),axis=0))
        assert all(edge<=max(13,np.max(interior)*1.15+2) for edge,interior in zip(jumps,inside)), (
            identity,jumps,[float(np.max(row)) for row in inside])
        edge_jump=max(jumps)
    return dict(id=identity,rank=record['rank'],family=record['family'],resolution=size,
                vertices=vertices,quads=quads,edge_jump=round(float(edge_jump),3),
                master_sha256=sha256(master.read_bytes()).hexdigest(),master_bytes=master.stat().st_size,
                zip_sha256=sha256(path.read_bytes()).hexdigest(),zip_bytes=path.stat().st_size)


def fonts():
    return tuple(ImageFont.load_default(size=value) for value in (25,17,13))


def sheet(path, title, cells, cols=5, thumb=186):
    width,height=thumb+16,thumb+47
    rows=(len(cells)+cols-1)//cols
    paper=Image.new('RGB',(cols*width+12,rows*height+56),'#22252a')
    draw=ImageDraw.Draw(paper)
    large,medium,small=fonts()
    draw.text((12,12),title,fill='#f4f1ea',font=large)
    for index,(image,label,subtitle) in enumerate(cells):
        col,row=index%cols,index//cols
        x,y=12+col*width,49+row*height
        paper.paste(image.convert('RGB').resize((thumb,thumb),Image.Resampling.LANCZOS),(x,y))
        for text,font,offset,color in ((label,medium,4,'#f0eee8'),(subtitle,small,26,'#aeb7bd')):
            if draw.textlength(text,font=font)>thumb:
                while draw.textlength(text+'...',font=font)>thumb:
                    text=text[:-1]
                text+='...'
            draw.text((x,y+thumb+offset),text,fill=color,font=font)
    path.parent.mkdir(parents=True,exist_ok=True)
    paper.save(path,quality=91,optimize=True)


def master_image(out,record):
    with Image.open(out/'masters'/(record['id']+'.png')) as image:
        return image.copy()


def render_sheets(out,records,pilot):
    assets=out/'evidence'
    if pilot:
        sheet(assets/'pilot_values.jpg','Pilot | original grayscale baselines',[
            (master_image(out,r),f"{r['rank']:03} {r['name']}",r['motif'].replace('_',' '))
            for r in records],cols=3,thumb=260)
        return
    by_family=defaultdict(list)
    for record in records:
        by_family[record['family']].append(record)
    for family,rows in by_family.items():
        sheet(assets/f'family_{family}.jpg',f"{family.title()} | {len(rows)} masters",[
            (master_image(out,r),f"{r['rank']:03} {r['name']}",r['motif'].replace('_',' '))
            for r in rows],cols=4,thumb=224)
    for start in range(0,100,25):
        rows=records[start:start+25]
        sheet(assets/f'rank_{start+1:03}_{start+25:03}.jpg',f'Painting priority | {start+1:03}-{start+25:03}',[
            (master_image(out,r),f"{r['rank']:03} {r['name']}",r['family'])
            for r in rows],cols=5,thumb=195)
    palette=json.loads((ROOT/'palettes.json').read_text(encoding='utf-8'))
    cells=[]
    for record in records[:6]:
        image=master_image(out,record)
        cells.append((image,record['name'],'Grayscale source'))
        for name,stops in palette[record['palette']].items():
            tinted=apply_palette(np.asarray(image),stops)
            cells.append((Image.fromarray(tinted),record['name'],name.title()))
    sheet(assets/'palette_previews.jpg','One value master | three replaceable palettes',cells,cols=4,thumb=232)
    repeated=[]
    for record in records[:6]:
        image=master_image(out,record)
        tile=Image.new('L',(image.width*2,image.height*2))
        for x,y in ((0,0),(1,0),(0,1),(1,1)):
            tile.paste(image,(x*image.width,y*image.height))
        repeated.append((tile,record['name'],'2 x 2 repeat check'))
    sheet(assets/'repeat_previews.jpg','Seam check | four copies of one master',repeated,cols=3,thumb=275)



def write_index(out,records):
    lines=['# Ranked material masters','',
           'Each ZIP contains one 3D painting folder. The JSON catalog records sources, uses, region fit, and painting notes.','',
           '| Rank | Master | Family | Physical U by V repeat | Palette | Files |',
           '| ---: | --- | --- | --- | --- | --- |']
    for r in records:
        u,v=r['scale_m']
        identity=r['id']
        lines.append(f"| {r['rank']:03d} | {r['name']} | {r['family']} | {u:g} x {v:g} m | {r['palette']} | [3D ZIP](packages/{identity}.zip) / [Grayscale PNG](masters/{identity}.png) |")
    (out/'INDEX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def native_sheet(out,records):
    assets=out/'evidence'
    cells=[]
    for record in records[:len(PILOT)]:
        path=assets/(record['id']+'.png')
        if not path.exists():
            return
        with Image.open(path) as im:
            cells.append((im.copy(),record['name'],'Blender OBJ and PBR preview'))
    sheet(assets/'pilot_3d.jpg','Native Blender pilot | one chart per paint surface',
          cells,cols=3,thumb=286)


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT)
    parser.add_argument('--pilot',action='store_true')
    args=parser.parse_args()
    records=catalog()
    if args.pilot:
        records=records[:len(PILOT)]
    reports=[verify(r,args.out) for r in records]
    if len({r['master_sha256'] for r in reports})!=len(reports):
        raise ValueError('Duplicate grayscale masters')
    if not args.pilot:
        assert len(list((args.out/'masters').glob('*.png')))==100
        assert len(list((args.out/'packages').glob('*.zip')))==100
    render_sheets(args.out,records,args.pilot)
    if not args.pilot:
        write_index(args.out,records)
        native_sheet(args.out,records)
    report={'checked_masters':len(reports),'mapped_png_count':len(reports)*6,
            'master_bytes':sum(row['master_bytes'] for row in reports),
            'package_bytes':sum(row['zip_bytes'] for row in reports),
            'model_vertices':sorted({row['vertices'] for row in reports}),
            'model_quads':sorted({row['quads'] for row in reports}),
            'ipad_import_tested':False,'packages':reports}
    (args.out/'evidence'/'inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"Verified {len(reports)} packages and grayscale masters, {report['package_bytes']:,} ZIP bytes")


if __name__=='__main__':
    main()
