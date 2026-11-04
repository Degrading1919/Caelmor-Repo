"""Compose and clean up the staged frames from render_expansion_evidence.py."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"
FRAMES=OUT/"_expansion_frames"
manifest=json.loads((OUT/"expansion_evidence_manifest.json").read_text(encoding="utf-8"))
rows=manifest["rows"]
try:
    font=ImageFont.truetype("arial.ttf",17)
    label_font=ImageFont.truetype("arial.ttf",24)
except OSError:
    font=label_font=ImageFont.load_default()


def annotate(filename, output, labels):
    image=Image.open(OUT/filename).convert("RGB")
    draw=ImageDraw.Draw(image)
    for (x,y),label in labels:
        bounds=draw.textbbox((0,0),label,font=label_font)
        w,h=bounds[2]-bounds[0],bounds[3]-bounds[1]
        draw.rounded_rectangle((x,y,x+w+20,y+h+14),radius=7,fill=(28,31,34))
        draw.text((x+10,y+7),label,font=label_font,fill=(245,242,232))
    image.save(OUT/output,optimize=True)


annotate("four_regions_comparison.png","four_regions_comparison_labeled.png",[
    ((38,36),"MIRE · upper left"),((1120,36),"EMBERHOLT · upper right"),
    ((38,620),"LOWMARK · lower left"),((1090,620),"THORNFELL · lower right")])
annotate("lowmark_wealth_comparison.png","lowmark_wealth_comparison_labeled.png",[
    ((130,35),"MODEST"),((670,35),"ESTABLISHED"),((1270,35),"AFFLUENT")])
annotate("lowmark_maintenance_comparison.png","lowmark_maintenance_comparison_labeled.png",[
    ((260,35),"MAINTAINED"),((1040,35),"NEGLECTED")])

if FRAMES.exists():
    cols=4; card_w=330; card_h=295; label_h=36
    sheet=Image.new("RGB",(cols*card_w,((len(rows)+cols-1)//cols)*card_h),(35,39,43))
    draw=ImageDraw.Draw(sheet)
    for i,row in enumerate(rows):
        x=(i%cols)*card_w; y=(i//cols)*card_h
        draw.text((x+8,y+5),row["label"],font=font,fill=(240,238,228))
        frame=Image.open(FRAMES/f"item_{i:02d}.png").convert("RGB")
        frame.thumbnail((card_w-12,card_h-label_h-8),Image.Resampling.LANCZOS)
        sheet.paste(frame,(x+(card_w-frame.width)//2,y+label_h))
    path=OUT/"expanded_type_gallery.png"
    sheet.save(path,optimize=True)
    for frame in FRAMES.glob("*.png"):
        frame.unlink()
    FRAMES.rmdir()
    print(path)
