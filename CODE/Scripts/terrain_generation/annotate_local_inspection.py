"""Add inspection captions to actual Blender pixels without changing the terrain."""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
from PIL import Image, ImageDraw, ImageFont


TITLES={
    "crestbridge_broad_elevated":"Crestbridge valley / fixed Hall and Depot anchors",
    "crestbridge_ground_approach":"Approaching the retained Crestbridge crossing / eye level",
    "crestbridge_relationships":"Crestbridge civic relationships / true distances and elevations",
    "greyharrow_local":"Greyharrow / side-branch banks, candidate access and foundations",
    "reedmere_local":"Reedmere / wet ground and conditional raised-floor tests",
    "reedmere_floor_detail":"Reedmere / conditional raised-floor clearance detail",
    "drowsebank_local":"Drowsebank / race, working head and bank space",
}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--metadata",type=Path,required=True)
    p.add_argument("--controls",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    report=json.loads(a.metadata.read_text(encoding="utf-8"))
    controls=json.loads(a.controls.read_text(encoding="utf-8-sig"))
    font_path=Path(matplotlib.get_data_path())/"fonts/ttf/DejaVuSans.ttf"
    font=ImageFont.truetype(str(font_path),21)
    small=ImageFont.truetype(str(font_path),18)
    title_font=ImageFont.truetype(str(font_path),29)
    a.output.mkdir(parents=True,exist_ok=True)
    anchors={i["id"]:i for i in controls["inspection"]["anchors"]}
    distance=lambda p,q:sum((x-y)**2 for x,y in zip(p,q))**.5
    hall=anchors["crest_hall"]["xy_m"]
    depot=anchors["hill_depot"]["xy_m"]
    crossing=anchors["bridge_crossing"]["xy_m"]
    separation=distance(crossing,hall)
    summaries=[]
    for view in report["views"]:
        raw=Path(view["raw_path"])
        if not raw.exists(): raise FileNotFoundError("Missing actual Blender render: "+str(raw))
        pixels=Image.open(raw).convert("RGB")
        w,h=pixels.size
        header,footer=120,210
        out=Image.new("RGB",(w,h+header+footer),"#f3f1e9")
        out.paste(pixels,(0,header))
        draw=ImageDraw.Draw(out)
        draw.text((24,15),TITLES[view["id"]],font=title_font,fill="#222e29")
        draw.text((24,57),"Actual Blender render | vertical scale 1:1 | 2 m local terrain / 8 m surroundings",font=font,fill="#33463d")
        position=view["position_east_north_up_m"]
        draw.text((24,88),f"Camera E {position[0]:.1f} / N {position[1]:.1f} / Z {position[2]:.2f} m | eye offset {view['eye_height_above_sampled_ground_m']:g} m | lens {view['lens_mm']:.1f} mm",font=small,fill="#536056")
        labels=view["labels"] if view["id"].startswith("crestbridge") else []
        occupied=[]
        for index,label in enumerate(labels,1):
            u,v=label["normalized_pixel_xy"]
            x,y=u*w,v*h+header
            lx,ly=x,y
            while any((lx-ox)**2+(ly-oy)**2<42**2 for ox,oy in occupied):
                lx+=35; ly-=20
            occupied.append((lx,ly))
            draw.line((x,y,lx,ly),fill="#192e28",width=2)
            draw.ellipse((lx-14,ly-14,lx+14,ly+14),fill="#faf7e9",outline="#293d32",width=2)
            draw.text((lx-6,ly-12),str(index),font=small,fill="#263d2c")
            suffix=f"; ground {label['ground_m']:.2f} m" if "ground_m" in label else ""
            draw.text((25,header+h+13+(index-1)*26),f"{index}. {label['text']}{suffix}",font=small,fill="#263b30")
        y=header+h+124
        if view["id"].startswith("crestbridge"):
            notes=[f"Inspection crossing to Hall {separation:.1f} m | Hall to Depot {distance(hall,depot):.1f} m | Hall to natural river 640.3 m",
                   "Civic waterfront relationship FAILS at the retained Hall anchor. No canal, annex or tunnel has been invented.",
                   "Bridge/boxes are unapproved scale proxies; brown access ribbons are grading tests. No architectural assets or final town layout."]
        elif view["id"].startswith("reedmere"):
            notes=["Three test floors: normal reference stage + 1.5 m scenario + 0.3 m clearance; ground remains unfilled.",
                   "Decks/piles illustrate a conditional elevation requirement; pile bearing, connected walkways and evacuation remain unresolved.",
                   "Blue is normal reference water, not a flood simulation. No generated hamlet or architectural assets."]
        elif view["id"]=="drowsebank_local":
            notes=["The mill symbol falls in the race: no building mass is placed on the channel. Read bank space and route gaps directly.",
                   "Working head 0.95 m; gravity drainage does not prove barge passage or the separate wartime spur.",
                   "Brown access ribbons and sparse foundation tests are provisional. No wheel, lock, mill building or navigation certification."]
        else:
            notes=["Candidate access and sparse local foundations retain the side-branch town position; no settlement plateau.",
                   "Finer terrain is a feasibility screen. Density, flood exposure and crossing works still constrain the building programme.",
                   "No buildings, fortification assets or NPCs are generated."]
        for line in notes:
            draw.text((24,y),line,font=small,fill="#33483b"); y+=26
        path=a.output/(view["id"]+".png")
        out.save(path)
        summaries.append({"id":view["id"],"file":path.name,"raw_render_sha256":hashlib.sha256(raw.read_bytes()).hexdigest(),
                          "annotated_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                          "pixel_policy":"Raw render pixels preserved at original resolution; captions and projected numbered markers only."})
    (a.output/"image_verification.json").write_text(json.dumps({"images":summaries,"source_metadata":a.metadata.name},indent=2)+"\n",encoding="utf-8")
    print("CAELMOR_LOCAL_RENDER_CAPTIONS "+str(len(summaries)))


if __name__=="__main__": main()
