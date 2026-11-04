"""Compose the matched library study frames and historical Gatehouse control."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EVIDENCE=Path(__file__).resolve().parents[1]/'evidence'
ROOT=EVIDENCE/'construction_library'
PREVIOUS=EVIDENCE/'construction_treatments'/'after'


def sheet(name, labels, frames, width=560):
    height=round(width*704/1024)
    heading=33
    image=Image.new('RGB',(len(labels)*width,len(frames)*(height+heading)),(32,36,40))
    draw=ImageDraw.Draw(image)
    font=ImageFont.load_default(size=17)
    for row,(caption,paths) in enumerate(frames):
        for column,path in enumerate(paths):
            x,y=column*width,row*(height+heading)
            draw.text((x+10,y+6),labels[column]+' | '+caption,fill='white',font=font)
            with Image.open(path) as source:
                image.paste(source.convert('RGB').resize((width,height),Image.Resampling.LANCZOS),
                            (x,y+heading))
    image.save(ROOT/name,quality=92,optimize=True)


def main():
    labels=('Hewn frame and shingles','Housed frame and slate','Hewn frame and clay')
    choices=('timber_shingle','render_slate','earth_clay')
    sheet('smithy_library.jpg',labels,[
        (caption,[ROOT/choice/'smithy'/frame for choice in choices])
        for caption,frame in [('Normal clay','normal_clay_0.png'),
                              ('Normal material','normal_material_0.png'),
                              ('Forge detail clay','close_clay_0.png'),
                              ('Forge detail material','close_material_0.png')]])
    sheet('smithy_workfront.jpg',('67cba19','Raised firebed'),[
        (caption,[PREVIOUS/'smithy'/frame,ROOT/'timber_shingle'/'smithy'/frame])
        for caption,frame in [('Normal clay','normal_clay_0.png'),
                              ('Normal material','normal_material_0.png')]],width=710)
    sheet('gatehouse_bonding.jpg',('67cba19','Bonded returns'),[
        (caption,[PREVIOUS/'gatehouse'/frame,ROOT/'bonded_returns'/'gatehouse'/frame])
        for caption,frame in [('Normal clay','normal_clay_0.png'),
                              ('Detail clay','close_clay_0.png'),
                              ('Detail material','close_material_0.png')]],width=710)


if __name__=='__main__':
    main()
