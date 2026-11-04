"""Compose depth comparisons using the library study contact-sheet layout."""
from compose_construction_library import sheet
import compose_construction_library as layout

ROOT=layout.EVIDENCE/'construction_depth'
LABELS=('Modeled','Hybrid','Texture dominant')
MODES=('modeled','hybrid','texture')
FRAMES=(('Normal clay','normal_clay_0.png'),
        ('Normal material','normal_material_0.png'),
        ('Close clay','close_clay_0.png'),
        ('Close material','close_material_0.png'))


def main():
    layout.ROOT=ROOT
    for name in ('smithy','gatehouse'):
        sheet(name+'_depth.jpg',LABELS,[
            (caption,[ROOT/mode/name/frame for mode in MODES]) for caption,frame in FRAMES])
        sheet(name+'_glb.jpg',('Native hybrid','GLB reimport'),[
            ('Normal material',[ROOT/folder/name/'normal_material_0.png'
                                for folder in ('hybrid','glb')])],width=710)


if __name__=='__main__':
    main()
