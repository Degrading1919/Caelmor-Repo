# ChatGPT Image — Reusable Prompt Template for “Flat 2D Reference” (Blender Templates)
Copy one item from your template-asset list into **ASSET_INPUT**, pick a **MODE**, fill optional fields, then paste the full prompt into ChatGPT Image.

---

## MASTER PROMPT (copy/paste + fill)

Create a **flat, technical 2D reference** intended for **3D modeling in Blender**.

ASSET_INPUT: **{PASTE ONE ITEM FROM LIST}**
MODE: **{CHARACTER_BASE | HEAD | HAIR | CLOTHING_MODULE | PROP | MATERIAL_SWATCH | DECAL_OVERLAY}**

WORLD / STYLE (must follow):
- grounded mythic-medieval, lived-in, practical
- **technical model sheet** / orthographic reference
- plain neutral background
- **orthographic (no perspective)**, centered, clean edges
- minimal shadowing, no dramatic lighting, no VFX
- clarity > beauty

OUTPUT (choose ONE):
A) **Single sheet** with multiple labeled views (preferred)
B) **One view only** (use if multi-view consistency fails)

REQUIRED VIEWS (based on MODE):
- CHARACTER_BASE: front + side + back (neutral stance)
- HEAD: front + side + 3/4 + back (include neck seam line)
- HAIR: front + side + back + top (show hairline + attachment breaks)
- CLOTHING_MODULE: on-body front + on-body back + optional flat-lay inset
- PROP: front + side + top (+ back if asymmetric) + attachment/grip inset
- MATERIAL_SWATCH: seamless tile swatch + “clean vs worn” inset
- DECAL_OVERLAY: 8–12 simple mask-style overlays on one sheet

DETAIL RULES:
- show seams, closures, and layer boundaries clearly
- show material zones with simple value separation (not noisy texture)
- include a simple scale reference (ruler line or silhouette height bar)
- keep proportions realistic and consistent

OPTIONAL MATERIAL NOTES (fill if you want):
Primary materials: {e.g., coarse wool, linen, leather, dull iron, brass, heat-blued steel}
Palette (3–5): {e.g., ash gray, soot black, worn brown, deep red, brass accent}
Wear/grime: {e.g., soot at cuffs/hem, mud line at boots, frayed edges, patch repairs}

WHAT TO EMPHASIZE (pick 3):
{silhouette | seams | fasteners | attachment points | layer thickness | stitching | wear/repairs | modular splits}

NEGATIVE CONSTRAINTS (must follow):
- no text blocks, no logos, no watermarks
- no cinematic lighting, fog, sparks, glow, runes
- no dynamic action poses
- no anime/chibi proportions
- do not resemble recognizable third-party IP

Generate the image exactly to spec.

---

## MODE ADD-ONS (paste ONE under the prompt if needed)

### CHARACTER_BASE add-on
- neutral stance, relaxed; feet shoulder-width; hands relaxed
- show basic anatomy landmarks lightly (elbows/knees/clavicle) for modeling
- keep surface detail minimal (this is a base mesh reference)

### CLOTHING_MODULE add-on
- show layer thickness at collar/hem with a small cutaway inset
- show closure clearly (toggle/lace/pin/belt) with a zoom inset
- include inside lining inset if relevant

### PROP add-on
- show how it attaches/carries (hand grip / strap loop / belt hook / back mount)
- include a small exploded inset if modular (e.g., staff head socket)

### MATERIAL_SWATCH add-on
- create a seamless tile swatch
- include two insets: “clean” and “worn”
- keep pattern scale realistic (not too fine)

### DECAL_OVERLAY add-on
- provide 8–12 overlay shapes on one sheet (mud line, soot smear, patch seams, water stains)
- high contrast, simple shapes intended as masks

---

## FALLBACK (if multi-view sheets come out inconsistent)
Run ChatGPT Image 3 times using this single-view prompt:

Create a flat orthographic technical reference of:
ASSET_INPUT: {…}
VIEW: {FRONT / SIDE / BACK}
Same proportions, same design, same materials. Plain background, studio-flat lighting, minimal shadow.
No perspective. Clean edges. Show seams/closures/material zones clearly. No text, no watermark.

---

## QUICK EXAMPLES (copy/paste)

### Example: “Cloak (short + long)”
ASSET_INPUT: **Cloak (short + long)**
MODE: **CLOTHING_MODULE**
Primary materials: coarse wool, leather strap, dull iron clasp
Palette: ash gray, soot black, worn brown
Wear/grime: frayed hem, soot at collar, repaired seam patch
Emphasize: silhouette, seams, fasteners

### Example: “Lantern (2 variants)”
ASSET_INPUT: **Lantern (2 variants)**
MODE: **PROP**
Primary materials: dull iron, brass accents, soot-darkened glass
Palette: dull iron gray, warm brass, smoke black
Wear/grime: soot around vents, polished grip from handling
Emphasize: attachment points, material boundaries, construction
