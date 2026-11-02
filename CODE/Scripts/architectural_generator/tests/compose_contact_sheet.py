"""Compose existing evidence frames into the ten-row, four-view contact sheet."""

import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence"
FRAMES = OUT / "_frames"
VIEWS = ("front-left", "front-right", "rear-right", "rear-left")
FUNCTIONS = ("FARMHOUSE", "BARN", "GRAIN_STORE", "MILLER", "INN")
DIMENSIONS = {
    "FARMHOUSE": ((11.0, 7.0), (13.5, 8.5)),
    "BARN": ((16.0, 10.0), (16.5, 10.3)),
    "GRAIN_STORE": ((8.5, 5.5), (9.0, 5.8)),
    "MILLER": ((12.0, 8.0), (12.5, 8.3)),
    "INN": ((15.0, 10.0), (15.5, 10.3)),
}


def _open_when_ready(path):
    last_error = None
    for _ in range(12):
        try:
            return Image.open(path).convert("RGB")
        except Exception as exc:
            last_error = exc
            time.sleep(.1)
    raise last_error


def compose():
    thumb_w, thumb_h, label_w = 360, 250, 190
    sheet = Image.new("RGB", (label_w + len(VIEWS) * thumb_w, 10 * thumb_h), (35, 39, 43))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        small = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        font = small = ImageFont.load_default()
    for column, view in enumerate(VIEWS):
        draw.text((label_w + column * thumb_w + 12, 8), view.replace("-", " ").title(),
                  fill=(235, 235, 230), font=font)
    for i in range(10):
        function = FUNCTIONS[i // 2]
        seed = 17 if i % 2 == 0 else 43
        footprint = ("U" if function == "FARMHOUSE" and seed == 43 else
                     "RECT" if function in ("BARN", "GRAIN_STORE") else
                     "T" if function == "MILLER" else "U" if function == "INN" else "L")
        width, depth = DIMENSIONS[function][0 if seed == 17 else 1]
        dims = f"{width:g}×{depth:g} m"
        label = f"{function}\nseed {seed}\n{footprint} · {dims}"
        draw.multiline_text((10, i * thumb_h + 75), label, fill=(235, 235, 230), font=small, spacing=5)
        for j, view in enumerate(VIEWS):
            frame = _open_when_ready(FRAMES / f"building_{i:02d}_{view}.png")
            frame.thumbnail((thumb_w, thumb_h - 36), Image.Resampling.LANCZOS)
            x = label_w + j * thumb_w + (thumb_w - frame.width) // 2
            y = i * thumb_h + 35 + (thumb_h - 36 - frame.height) // 2
            sheet.paste(frame, (x, y))
    sheet.save(OUT / "ten_buildings_four_views.png", optimize=True)
    return OUT / "ten_buildings_four_views.png"


if __name__ == "__main__":
    print(compose())
