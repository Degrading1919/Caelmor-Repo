# Caelmor material painting library

The first 100 reusable material masters are original grayscale starting
points for hand painting. The ranked list starts with Lowmark and then
covers architectural stock, terrain, vegetation, metal, equipment,
textiles, leather, ceramics and glass. Material use and regional fit
are art-direction interpretations. They confer no new resources, recipes,
trade routes or canon.

- [Ranked downloads](INDEX.md) lists all 100 painting ZIPs and grayscale PNGs.
- [Catalog data](catalog.json) records physical repeat dimensions, stock or construction cues, palette families, research sources and human painting notes.
- [Six Blender painting surfaces](evidence/pilot_3d.jpg) shows the imported pilot packages.
- [Palette previews](evidence/palette_previews.jpg) shows three finishes from each of six value masters.
- [Repeat check](evidence/repeat_previews.jpg) tiles the same value maps across a separate flat 2 × 2 swatch.
- [Priority sheets 001–025](evidence/rank_001_025.jpg), [026–050](evidence/rank_026_050.jpg), [051–075](evidence/rank_051_075.jpg), and [076–100](evidence/rank_076_100.jpg) cover every master. The evidence folder also groups them by material family.

## Paint on the iPad

1. Download a **3D ZIP** from the ranked list and unzip it in Files.
   Keep `material.obj`, `material.mtl` and their linked PNGs in the
   same extracted material-ID folder.
2. With Procreate open to **Gallery**, drag the extracted **folder**
   from Files into Gallery. This carries its material links. Open
   the resulting 3D canvas and tap the surface.
3. Paint live on the 3D surface using an additional layer. Work in
   grayscale to keep the result eligible for palette swapping.
   Select the color, roughness, or metallic channel intentionally.
   Use Lighting Studio to inspect the stroke and rotate the model
   to check how it reads under grazing light.
4. In **Actions → Share → Share Textures → PNG**, export the texture
   set to Files. Name the working copy by the stable material ID and
   keep the Procreate document as the editable iPad session.
5. Return only channels you meant to edit. Procreate uses the linked
   normal for display and exposes color, roughness and metallic for
   painting. Caelmor retains the normal and height from the source
   package unless a separate technical edit is explicitly imported.

See the official [Procreate import handbook](https://help.procreate.com/procreate/handbook/3d-painting/import),
[OBJ channel guidance](https://help.procreate.com/articles/Z0mATv-3d-painting),
and [texture-set export instructions](https://help.procreate.com/procreate/handbook/3d-painting/share).

**Device check pending.** Start with
[Split Oak Shingle](packages/split_oak_shingle.zip). In Procreate, check
that one stroke hits one location, the relief is visible, the material
can be selected, and exported channel names and resolution are clear.
Repeat on [Forged Iron](packages/forged_iron.zip) to check metallic
editing. Report any fallback resolution or unsupported-feature message.
The distributed maps are 512 × 512. If the app exports at a different
resolution or finer paint is needed, generate a fresh 1024 or 2048
package for that ID before the next session. Keep the original higher
resolution paint export if reworking the package.

## Keep the master, palette and technical maps separate

| File | Purpose |
| --- | --- |
| `master.png` | Immutable original grayscale value source. A painter can author a new grayscale master in a revision explicitly. |
| `color.png` | Procreate Base Color. Starts as an RGB copy of the value master. A grayscale return can drive a selectable palette. A chromatic return keeps its authored color. |
| `roughness.png`, `metallic.png` | Separate linear data maps for painting and export. Dielectrics start with a zero metallic map. |
| `height.png`, `normal.png` | Derived relief and tangent-space +Y normal. Height is a technical companion. Normal is linked in the painting package. |
| Optional `overlay.png` | RGBA painted overlay imported explicitly and composited after the palette in Blender. |

All painting models use one continuous, non-overlapping UV chart that
covers one repeat in the texture. The eight open-surface templates omit
hidden back faces. Their profile and physical dimensions aid painting
without the cost of individual blocks or shingles. The colored render
palette and the larger repeated surface are separate from the unique
paint chart. Paint across opposite edges in pairs when a stroke needs
to survive tiling.

## Return selected paint to Blender

Run these from the repository root using Python 3 and Blender 5. Replace
the example paths with the actual files returned by Procreate.

```powershell
python MEDIA/Materials/return_paint.py --package MEDIA/Materials/packages/split_oak_shingle.zip --catalog MEDIA/Materials/catalog.json --output MEDIA/Materials/returns --import-map color=MEDIA/Materials/working/oak_color.png --import-map roughness=MEDIA/Materials/working/oak_roughness.png
```

The command creates `returns/split_oak_shingle_rev001/` and a
`return.json` record. Only explicit mappings change. Source packages
stay intact. Start a later return from the latest revision folder to
carry previous edits forward. Color may remain chromatic. A scalar or
value-map import must be grayscale. Imports must match the package
dimensions, so a size mismatch is reported before writing a revision.
An optional `--import-map overlay=...` loads a separate RGBA overlay
instead of baking it into the grayscale source.

```powershell
blender --background --python MEDIA/Materials/return_paint.py -- --blender-package MEDIA/Materials/returns/split_oak_shingle_rev001 --catalog MEDIA/Materials/catalog.json --palette-option native --save-blend MEDIA/Materials/returns/split_oak_shingle_material.blend
```

Append the resulting Blender material into a working scene. It uses
`UV0_Metric` divided by the catalog's U and V repeat dimensions. Check
that the chosen surface's metric UV axes run along its courses, boards
or grain and are continuous at the desired seams. A texture can be
shared across models with compatible UVs. The painting template's
normalized chart and the generator's per-face or packed atlas UVs
serve different purposes.

In the architectural generator, use an artist material slot or the
existing named artist finish on a compatible role. Keep the original
shader and procedural atlases available for other objects. The Blender
helper creates a new material and requires an explicit slot replacement.
This library does not change the generator or remap every existing roof.
For later GLB export, resolve palette and overlay nodes to an albedo
image before using a standard glTF material. This handoff validates
Blender material construction and assignment.

For a deliberate relief change, save a separate grayscale height map,
then regenerate a technical normal. The example uses a 25 mm full
height range. Import both maps explicitly in the new revision.

```powershell
python MEDIA/Materials/derive_normal.py --id split_oak_shingle --height MEDIA/Materials/working/oak_height.png --output MEDIA/Materials/working/oak_normal.png --relief-m 0.025
```

## Build and verify

Python batch tools use Pillow and NumPy. Existing production files are
deterministic, and the builder requires a fresh output location for a
changed build. Rebuild a single high-resolution painting package without
duplicating the whole library.

```powershell
blender --background --factory-startup --python-exit-code 1 --python MEDIA/Materials/build_templates.py
python MEDIA/Materials/build_library.py --id split_oak_shingle --resolution 2048 --out MEDIA/Materials/working_2k
python MEDIA/Materials/review_library.py
blender --background --factory-startup --python-exit-code 1 --python MEDIA/Materials/verify_blender.py -- --resolution 640 --samples 12
blender --background --factory-startup --python-exit-code 1 --python MEDIA/Materials/verify_roundtrip.py
```

Run `build_library.py` with no selector to build all 100 at 512 px.
The Blender verifier imports the six packaged pilot models by default.
It validates Procreate's MTL directive spellings separately and binds
the PBR nodes explicitly for Blender, whose OBJ importer skips the
three vendor PBR map directives.
