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

## Derive Height and Normal from painted grayscale

Run from the repository root with Python 3, Pillow and NumPy. Use an existing
catalog ID and an opaque square PNG. Procreate RGB or RGBA exports work when
their RGB channels are equal. Both commands preserve pixel dimensions and
require fresh output paths in the existing `working` folder.

```powershell
$id = 'hewn_oak'
$work = 'MEDIA/Materials/working'
$paint = Join-Path $work "${id}.png"
$height = Join-Path $work "${id}_height.png"
$normal = Join-Path $work "${id}_normal.png"
py -3 MEDIA/Materials/derive_height.py --id $id --input $paint --output $height --edge stretch --intensity 1 --smoothing 1
if ($LASTEXITCODE -ne 0) { throw 'Height generation failed' }
py -3 MEDIA/Materials/derive_normal.py --id $id --height $height --output $normal --edge stretch --size-m 4 1 --relief-m 0.006
if ($LASTEXITCODE -ne 0) { throw 'Normal generation failed' }
```

- Choose `--edge repeat` in both commands for an already seamless tile.
  This is the default and samples through the tile boundary.
- Choose `--edge stretch` in both commands for a single application across
  a surface. Height filtering reflects at the border and Normal uses one-sided
  edge slopes. In Blender, use the same normalized UV mapping for the paint
  and derived maps and set the texture extension to **Extend**.
- Height attenuates broad painted washes, blends medium and fine grain bands
  and limits strong strokes around mid-gray. Lower `--intensity` to reduce
  relief (0 gives flat, 1 default, 2 maximum). Increase `--smoothing` to
  soften small marks (0.25–4, default 1). Height uses stored paint values
  as a guide and estimates relief from contrast. A painted shadow may still
  need an explicit Height correction.
- Normal uses the catalog's `scale_m` as its default U/V dimensions.
  For stretched paint, supply the actual coverage in metres with
  `--size-m U V`. The Hewn Oak example uses 4 m along horizontal U grain
  and 1 m across V. `--relief-m` is the height represented by the full
  black-to-white range. The generated image generally uses only part of it.

Load Height and the tangent-space +Y Normal as **Non-Color** data. Route Normal
through a Blender Normal Map node. Keep Base Color available for tinting.
Both outputs are 8-bit PNGs and can be passed as explicit `--import-map height=…`
and `--import-map normal=…` inputs to `return_paint.py` when the package dimensions
match. Move earlier derived maps aside before generating replacements at the
same paths.

The local 512 × 512 Hewn Oak export was processed with the commands above.
Height used values 87–170 of 255 (about 2.0 mm of range at the chosen scale).
95% of decoded normals tilted less than 4.8° from flat. The longitudinal grain
was visible in the technical maps. This check used image inspection and decoded
normal measurements. Run the automated checks with
`py -3 -m unittest discover -s MEDIA/Materials -p test_paint_maps.py -v`.

## Derive relief for a painted UV atlas

Use `derive_atlas.py` with a saved Blender mesh and its original painted sRGB
PNG. The tool uses the evaluated mesh, the named UV map, object scale, and the
scene's metre scale. It preserves the atlas resolution and coordinates. Inputs
can be rectangular. Export paint in sRGB and keep covered texels opaque.

```powershell
$work = 'MEDIA/Materials/working'
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
py -3 MEDIA/Materials/derive_atlas.py --blender $blender --blend "$work/lowmark_stone_wall.blend" --object Plane --uv-map UVMap --albedo "$work/lowmark_stone_wall_color_v1.1.png" --shared-uv --height "$work/lowmark_stone_wall_height.png" --normal "$work/lowmark_stone_wall_normal.png" --relief-m 0.002
```

The Lowmark wall intentionally shares paint across its mirrored sides.
The command generates one 2048 × 2048 map pair for both sides from the
current Blender scene and v1.1 atlas. The tested atlas SHA-256 was
`984b402d800b19baa2030ac3b6a7d472737356ffb79573cbceda5f80ffd05734`.
Two runs produced byte-identical maps across 267 occupied regions. Decoded
normal tilt was 1.59° at the 95th percentile and 14.75° at maximum across the
atlas. Both input file hashes matched before and after generation.

- For a pre-rasterized Blender-derived mask, use `--island-mask labels.png`
  instead of the Blender scene, object and UV arguments. Supply an opaque 8-bit
  or 16-bit grayscale PNG of the same dimensions, with zero for empty texels and
  one integer per island. Intentional stacks share the same label. Set
  `--size-m U V` to the metres represented by the full atlas axes (default 1 × 1).
  Mask input supplies no per-triangle metric, shear, or overlap validation.
- Blender input accepts one mesh and one atlas in the 0–1 UV square.
  `--allow-stacked` checks complete matching texel footprints and compatible
  physical UV metrics. Use `--shared-uv` for an atlas intentionally reused by
  surfaces with partial overlaps or different triangulation. At each covered
  texel, the first chart and triangle in stable mesh order supply the filter
  label and physical metric. Every surface sharing the texel samples the same
  maps. The reference metric can only approximate the relief on surfaces
  with different UV scales. Shared mode caps normal tilt at 15° to limit
  spikes on distorted triangles. Blender applies the tangent-frame handedness
  when it samples the shared +Y map. Coverage is tested at texel centres.
- `--intensity` controls inferred relief (0–2, default 1). `--smoothing`
  sets the filter scales (0.25–4, default 1). `--relief-m` gives the
  black-to-white Height span in metres. The default is 0.002. Use gentle
  values for modeled stonework. The tool suppresses broad luminance variation,
  limits fine and medium bands, and attenuates responses at strong local
  chroma changes in CIE Lab. Painted lightness supplies a relief cue. Review
  inferred depth around shadows and seams against the modeled asset.
- `--edge-fade` (default 3 texels) fades inferred detail at island boundaries
  and on narrow strips. Use an optional grayscale `--detail-mask` with black
  over modeled joints or bevels and white over areas eligible for inferred
  detail. `--intensity 0` keeps only explicit overrides. For larger bevels or
  bevels joined to the same UV island, use the mask to control the affected area.
- `--depth` adds signed scalar offsets. Midpoint code 128 in 8-bit or 32768
  in 16-bit is neutral. `--cracks` subtracts up to 20% of the full Height
  range at white. Both apply inside island coverage after the automatic
  filter. Use overrides for authored cracks that fall inside the stone faces.
- `--padding` extends full pixels into empty gutters (default 4 texels).
  Filtering and derivatives sample only matching labels. Padding resolves
  ties deterministically and never overwrites another island. Leave enough UV
  gutter for the intended Blender texture sampling and mip levels. Atlases
  with touching islands or very narrow gutters can still mix at sample time.

Load the RGB Normal as **Non-Color** in Blender and route it through a
tangent-space Normal Map node using the same UV map as the albedo. Keep the
16-bit grayscale Height as linear data for editing and rebaking. Use the
generated Normal alone for this material's additional shading relief. The
existing square 8-bit Procreate return package workflow has its own Height
and Normal commands above.

The original synthetic fixture has four beveled stones with three painted
front regions, a mirrored shared front, one narrow gutter, and 16 narrow
bevel strips. Two executions generated identical Height and Normal PNGs at
384 × 256. All 2,720 bevel texels encoded flat Height and neutral Normal.
At 6 mm per full range, the generated Height span was about 1.43 mm and
front Normal tilt was 0.32° at the 95th percentile and 8.67° maximum
(neutral RGB quantization decodes to about 0.32°). In the Blender 5.0.1
comparison, 6 pixels under high light and 1,513 under raking light changed
by more than two levels in at least one RGB channel. The added response
was most visible around the authored fine cracks under raking light.
[Blender comparison](evidence/stone_atlas_relief.jpg)

```powershell
py -3 -m unittest discover -s MEDIA/Materials -p 'test_*.py' -v
py -3 MEDIA/Materials/verify_atlas.py --blender $blender
```

## Split Oak Shingle — recolorable roof working test

**Creative Director decision (2026-11-09):** Four tint choices and the Blender
node wiring below passed visual review on the Lowmark farmhouse preview.
These are approved **working palette values and a reproducible shader test**,
not a declaration that the roof, scene, asset export, or generator behavior
is production-final. The local working scene was saved as
`MEDIA/Materials/working/lowmark_house_blue_roof.blend`; its native bytes
are not included merely by documenting it here.

### Approved tint choices

Use the following Blender color-picker HEX values for the tint input:

| Display name | HEX | Visual intent |
| --- | --- | --- |
| Weathered Brown Oak | `#A67B5B` | Natural muted brown, legible wood grain |
| Light Brown Oak | `#D2AD81` | Lighter sun-weathered brown |
| Muted Red Oak | `#A65B53` | Restrained aged reddish-stained timber |
| Weathered Slate Blue | `#718DA5` | Muted blue-gray stained wood |

These are the four reviewed hues; they are **not** new lore, a mandatory
regional distribution, or a runtime customization schema. The earlier
`#765039` dark-brown trial was too dark at full-strength Multiply and is
not one of the approved four choices.

### Blender working shader contract

For the **texture-dominant mapped roof field** tested on the Lowmark
farmhouse, the node links and settings are:

```text
UV Map [UV2_Surface]
    -> Mapping [Type: Point; Location: (0,0,0);
                Rotation: (0,0,0); Scale: (0.400,0.500,1.000)]
       -> Image Texture [split_oak_shingle.png, sRGB]
          -> Mix Color [Blend: Multiply, Factor: 1.000,
                        A: grayscale image, B: chosen palette HEX]
             -> Principled BSDF [Base Color]
       -> Image Texture [split_oak_shingle_roughness.png, Non-Color]
          -> Principled BSDF [Roughness]
       -> Image Texture [split_oak_shingle_normal.png, Non-Color]
          -> Normal Map [Tangent Space, Strength: 1.000]
             -> Principled BSDF [Normal]
Principled BSDF [Metallic: 0.000] -> Material Output
```

All three Image Texture **Vector** inputs share the same Mapping output.
Keep the grayscale detail and seam value structure in the Base Color image.
In this test, changing **only** Mix Color input B selects a palette.
Blend mode **Color** produced an overly light reddish-brown result;
lowering Multiply Factor to 0.650 reintroduced too much grayscale.
Use **Multiply at 1.000** and adjust input B to control lightness and hue.

**UV and scale scope:** `UV2_Surface` is the generator's mapped roof-field
UV layer. The tested `0.400, 0.500, 1.000` Mapping scale is specific to
that preview and should not silently replace this catalog's `scale_m:
[2, 1]` repeat specification. The standard material return helper
continues to target `UV0_Metric` for compatible metric-UV meshes.
Modeled shingles or perimeter detail have different UV/geometry needs
and should not automatically receive the painted multi-course pattern.

**Geometry and export status:** The texture-dominant preview showed
acceptable painted detail without decorative shingle-variation meshes.
The Creative Director chose to remove those decorative meshes from the
working scene; this did **not** modify the architectural generator's
persistent output. The working `.blend` is not an approved permanent
fixture. Before Unity/glTF use, bake or otherwise resolve the Blender
Mix Color tint into an exported albedo texture; do not assume the Blender
shader node mix survives standard glTF export. Normal and roughness maps
remain independent, reusable channels.

## Hewn Oak — shared structural timber working treatment

**Creative Director decisions (2026-11-09):** Approve a single hand-painted
grayscale **Hewn Oak** grain source for recolorable structural timber
rather than authoring separate grain textures for each nominal wood
species. The named tints below are **approved palette choices** for
wood-like appearances; they are not botanical identifications, regional
resource claims, or instructions to change structural geometry.

### Approved structural timber tint palette

Enter these HEX values in Blender's Multiply node input **B**. The
Weathered Oak tone was observed in the Lowmark farmhouse Blender test;
the other three values were expressly approved by the Creative Director
as palette choices, without separate screenshot-based appearance tests.

| Appearance name | HEX | Intended read |
| --- | --- | --- |
| Weathered Oak | `#A67B5B` | Medium warm brown; tested on exposed farmhouse framing |
| Pale Ash / Pine | `#D5B78D` | Light golden-beige wood |
| Dark Walnut | `#795340` | Deep brown wood |
| Reddish Chestnut | `#A66B55` | Muted warm red-brown wood |

These are palette names for visually distinct timber finishes, not proof
of the modeled wood's species. Apply one tint per material instance;
share the grayscale and normal images across instances. Board, shingle,
bark, and other visibly different **construction patterns** may still
need their own painted source.

### Lowmark farmhouse Blender shader test

The artist's working material was named `hewn_oak_test`. The initial
test used the following Blender nodes and links:

```text
UV Map [UV0_Metric]
    -> Mapping [Type: Point; Location (0,0,0); Rotation (0,0,0);
                Scale (0.250,1.000,1.000)]
       -> Image Texture [hewn_oak.png, sRGB]
          -> Mix Color [Multiply, Factor 1.000;
                        A: grayscale image, B: selected palette HEX]
             -> Principled BSDF [Base Color]
       -> Image Texture [hewn_oak_normal.png, Non-Color]
          -> Normal Map [Tangent Space, UV Map UV0_Metric,
                         Strength 1.000]
             -> Principled BSDF [Normal]
Principled BSDF [Metallic 0.000, Roughness 0.850]
    -> Material Output [Surface]
```

Both Image Texture Vector inputs share the Mapping output. Height is
used to **derive** the normal and is not additionally wired to Bump.
The roughness is intentionally a **constant 0.850**, with no separate
roughness image required for this working treatment. Preserve the
grayscale Base Color source and control color via Multiply input B
at Factor 1.000.

**Grain and UV behavior:** The current generator's `UV0_Metric` aligns
grain with the longest edge of each timber face, and the 0.250 U
scale gave an acceptable working view across vertical posts, horizontal
members, and diagonal braces. This is a **metric-mapped test**, not
verified one-image-span-per-beam UV mapping; it does not supersede the
catalog's 1 × 4 m material metadata. Slight rectangular UV discontinuities
on some small-building vertical timbers were observed close-up and
**accepted/deferred as low-priority cosmetic** at intended game-view
distance. Do not spend generator development time fixing these without
new player-distance evidence.

**Normal generation:** The initial hand-painted 512 × 512 Height and
Normal companions were derived by the tools in this directory with
`--edge stretch`. Sol's example normal pass used
`--size-m 4 1 --relief-m 0.006`; this covers horizontal U grain over
4 m for that sample and is **not** the same orientation as the
catalog's default `scale_m`. Keep source artwork and derived maps
separate; do not silently rewrite the catalog or the approved painting.

**Approval scope:** The grayscale timber appearance, tested Weathered
Oak tint, shader wiring, and current UV tolerance passed Blender
art-direction review. All four tint values are Creative Director
approved. Production asset packaging and Unity/gameplay-lighting
verification remain pending. This README does not include the local
PNG or Blender project files, and no runtime or procedural generator
behavior was changed.

## Fine Floated Lime Plaster — Lowmark working treatment

**Creative Director approval (2026-11-09):** The hand-painted Fine
Floated Lime Plaster finish and warm limewash appearance are approved
for the **Lowmark farmhouse wall infill** at the reviewed Blender
building-level view. It is deliberately quiet and low-contrast, supporting
the timber framing and shingle roof rather than competing with them.
The wider household ensemble was reviewed in Blender; this is an
art-direction acceptance, not a Unity export or in-game validation.

### Approved tint choices

The neutral grayscale artwork is recolored by a **Mix Color → Multiply**
node at **Factor 1.000**. Blender color-picker values:

| Appearance | HEX (RGB) | Status and intent |
| --- | --- | --- |
| Warm Limewash | `#FFF8D6` | **Preferred default** for Lowmark farmhouse; approved from the earlier building preview |
| Weathered Limestone | `#EDE3D2` | Approved optional muted gray-beige variation; reviewed in a subsequent farmhouse preview |

The Creative Director's initial Blender color input was
`#FFF8D6FF`; `FF` is the fully opaque alpha component and the RGB
value is `#FFF8D6`. The two names describe **finish appearance**, not
new regional resources or literal plaster composition. These values
apply to the neutral grayscale source, so the resulting shaded surface
will be darker than a flat HEX swatch.

### Working source and derived maps

The artist's original painted image was retained at
`MEDIA/Materials/working/fine_floated_lime_plaster.png`.
It appeared grayscale but contained unequal RGB channels, so the
strict grayscale-only map tools rejected it. An opaque grayscale
conversion was made **without replacing the original**:

```powershell
cd "C:\Users\CK\Documents\Caelmor-Repo"
$id = 'fine_floated_lime_plaster'
$work = 'MEDIA/Materials/working'
py -3 -c "from PIL import Image; Image.open(r'$work/$id.png').convert('L').save(r'$work/${id}_grayscale.png')"
py -3 MEDIA/Materials/derive_height.py --id $id --input "$work/${id}_grayscale.png" --output "$work/${id}_height.png" --edge stretch --intensity 0.65 --smoothing 1
py -3 MEDIA/Materials/derive_normal.py --id $id --height "$work/${id}_height.png" --output "$work/${id}_normal.png" --edge stretch --size-m 2 2 --relief-m 0.002
```

The Creative Director confirmed the Height and Normal commands completed
successfully. Derived Height is an intermediate source for Normal; it
is not independently connected to a Bump node. Generated map output
paths are in the existing local `working` directory. The derive scripts
protect existing output files from overwrites; move/rename older derived
outputs before regeneration.

### Reviewed Blender material setup

```text
UV Map [UV0_Metric]
    -> Mapping [Type: Point; Scale (0.500,0.500,1.000)]
       -> Image Texture [fine_floated_lime_plaster_grayscale.png, sRGB;
                         Extension: Extend]
          -> Mix Color [Multiply; Factor 1.000;
                        A: grayscale image; B: selected HEX]
             -> Principled BSDF [Base Color]
       -> Image Texture [fine_floated_lime_plaster_normal.png, Non-Color;
                         Extension: Extend]
          -> Normal Map [Tangent Space; UV Map UV0_Metric;
                         Strength 1.000]
             -> Principled BSDF [Normal]
Principled BSDF [Metallic 0.000; Roughness 0.900]
    -> Material Output [Surface]
```

Both Image Texture Vector inputs share the Mapping output. A separate
roughness texture is **not** required; the approved working material
uses a constant Roughness of 0.900. The Normal is restrained through
the derivation parameters above, with no additional mandatory strength
reduction. The 0.500 X/Y mapping scale is the **reviewed working value**,
not a universal plaster UV contract.

**Scaling choice:** The Creative Director compared a 512 × 512 master,
a 2× scaled view, and a 3-wide × 2-high tiled preview. The scaled view
was preferred: tiling exposed a visible repetition grid. For the
approved farmhouse presentation, use a single extended application
rather than visible repetition. `Extend` clamps sampled UVs outside
the image; it does **not** automatically fit the image to arbitrary
geometry. Confirm the mapping when this material is assigned to
different wall sizes, and do not silently change the catalog scale.

**Handoff and scope:** The approved material was judged on a Lowmark
household ensemble in Blender alongside warm structural timber and
painted roof shingles. Minor apparent variation at the upper gable
could be lighting or UV mapping; no corrective work was authorized
without stronger evidence. Preserve the source, derived maps, and
current material choices. Before standard glTF/Unity export, bake or
otherwise resolve the Blender Multiply tint into an exported albedo
texture; test export lighting and normals separately. Neither the
native .blend nor local working PNG files are committed by documenting
this decision; no architectural generator or runtime changes are made.

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
