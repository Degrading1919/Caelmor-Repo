"""Derive a tileable tangent-space normal from an explicitly edited height PNG."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from PIL import Image

from build_library import catalog


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--id',required=True,help='Catalog material ID')
    parser.add_argument('--height',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--relief-m',type=float,required=True,
                        help='Height in metres represented by the full scalar range')
    args=parser.parse_args()
    record=next((r for r in catalog() if r['id']==args.id),None)
    if record is None or not np.isfinite(args.relief_m) or args.relief_m<=0:
        parser.error('Choose a catalog ID and positive finite relief in metres')
    if args.output.exists():
        parser.error('Choose a fresh output filename')
    with Image.open(args.height) as image:
        if image.mode not in ('L','I;16') or image.width!=image.height:
            parser.error('Height must be a square grayscale PNG')
        height=np.asarray(image,dtype=np.float32)/(255 if image.mode=='L' else 65535)
    width,depth=record['scale_m']
    h,w=height.shape
    dx=(np.roll(height,-1,1)-np.roll(height,1,1))*w*args.relief_m/(2*width)
    dy=(np.roll(height,-1,0)-np.roll(height,1,0))*h*args.relief_m/(2*depth)
    normal=np.stack((-dx,dy,np.ones_like(height)),axis=-1)
    normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
    pixels=np.round((normal*.5+.5)*255).astype(np.uint8)
    Image.fromarray(pixels).save(args.output,format='PNG')


if __name__=='__main__':
    main()
