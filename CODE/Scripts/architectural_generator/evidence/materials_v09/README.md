# Material and condition review — v0.9.0

PR #85 review package, source **`094eb8c`**. Procedural building geometry and
functional layouts remain unchanged from v0.8. This adds reusable original PBR
surfaces and independent condition behavior. **Technical verification passed;
artistic acceptance remains with the Creative Director.** Workmanship at normal
distance remains weaker than maintenance as a visible cue.

## Controlled visual evidence

| Fixture | Before/after, normal + close | Condition pairs, normal | Condition pairs, close |
|---|---|---|---|
| Lowmark Smithy | [Sheet](comparison/smithy_before_after.png) | [Sheet](comparison/smithy_conditions_normal.png) | [Sheet](comparison/smithy_conditions_close.png) |
| Thornfell Gatehouse | [Sheet](comparison/gatehouse_before_after.png) | [Sheet](comparison/gatehouse_conditions_normal.png) | [Sheet](comparison/gatehouse_conditions_close.png) |

Before/after sheets are 2248 × 1522; condition sheets 2248 × 3736. Each control
pair changes only its named input. The last row deliberately contrasts modest
resources with high upkeep against affluent resources with neglect.

[44 individual captures](final/manifest.json), grouped under [Smithy](final/smithy/)
and [Gatehouse](final/gatehouse/), retain exact geometry/finish settings, cameras,
source byte hashes, image hashes and atlas diagnostics. Camera location and
scale match the historical v08 captures. Targets differ only in JSON float32
serialization (maximum metadata difference 0.000000191 m). Studio, lighting,
resolution 1024 × 704 and 32 Eevee samples are retained. Historical images are
referenced directly and have not been overwritten.

The sweeps hold the established/standard **generated geometry** fixed to isolate
surface controls. They are not a claim that normal production ignores wealth
or craftsmanship's existing massing, joinery and masonry rules. Geometry inputs:
seed91, LOWMARK/SMITHY or THORNFELL/GATEHOUSE, established/standard, age35,
maintenance0.7, MEDIUM/EFFICIENT, world/grammar enabled, AUTO context. Finish
states: reference; ages5/120 at upkeep0.7; upkeep0.15/0.95 at age120;
modest/affluent at age35/upkeep0.7; rough/fine at age35/upkeep0.7; and the two
resources-versus-care cases at age120. All other inputs stay fixed.

Editable reference scenes: [Smithy](final/smithy.blend),
[Gatehouse](final/gatehouse.blend). Actual verified exports:
[Smithy GLB](smithy.glb), [Gatehouse GLB](gatehouse.glb), with neighboring settings
and collision sidecars. Texture maps are embedded in these GLBs and packed in
the native scenes. [Four GLB reimport renders](roundtrip/manifest.json) expose the
same normal/close views after actual export/import, not regeneration.
Installable [extension ZIP](../../dist/caelmor_architecture.zip).

## What changed

Previously, shared 128-pixel material-family textures and small grayscale vertex
tints carried most surface variation. Large faces could only interpolate that
condition between their corners. The new pipeline bakes continuous metric
fields into padded face atlases, retaining existing metric and lightmap UVs and
adding `UV2_Surface`. Vertices, faces, openings, roof systems and equipment are
unchanged. Albedo, tangent normal, roughness and metallic properties survive as
standard texture bindings rather than renderer-only shader nodes.

- **Material investment:** stable variation per connected stock piece, with
  wealth-dependent sorting and timber knot/outlier selection. Wealth never
  enters the dirt or corrosion drivers.
- **Preparation:** longitudinal grain, shallow adze/plane relief, dressed versus
  rough mineral surfaces and burnished/oiled timber finish. This is workmanship,
  not age, resources or cleanliness.
- **History:** timber silvering, mineral maturation, moisture exposure, lower
  roof-butt wetting, accumulated corrosion and wear. Old maintained surfaces
  retain patina instead of reverting to new.
- **Care:** reduced deterioration, selective stressed-shingle replacements,
  existing-joint repointing and local limewash over splash/runoff damage.
- **Context:** each real host volume supplies eaves, foundation height and
  apertures. Sill drips and low contact shape wetting; actual generated firebed
  and chimney roles place heat/soot. Protected and out-of-scope sources remain
  available when regenerating selected layers.

The regional pattern bank distinguishes timber, mineral, plaster, iron, leather,
charcoal and roof coverings. Four-region numeric coverage is not four-region
art approval; this visual review remains focused on the two requested buildings.
One prevailing-rain direction and empirical aging curves are artistic inference,
not a climate, thermal or conservation simulation. Approved regional dossiers
remain authority; no lore, catalog or game code changes were made.

## Verification actually executed

- **12 sampler/causal tests** passed with Blender's bundled Python. They check
  deterministic output, metric continuity, regional roof patterns, independent
  stock/preparation controls, extreme age/upkeep ranges, local ground contact,
  sill/normal/cross-distance runoff and localized heat/corrosion behavior.
- **Six architectural regressions** passed (18.242 s for that run), including
  the unaffected 78 geometry fixtures and selected seeds/detail modes. Both
  native benchmark hashes also match their v08 controls. No extra geometry was
  introduced for the new surfaces.
- [Native export and lifecycle checks](export_checks.json) passed in Blender
  5.0.1: Smithy 14 atlas banks/42 embedded PNGs, 18,372 bound UV values and 56
  decoded pixel-map comparisons; Gatehouse 9 banks/27 PNGs, 83,726 UV values and
  36 decoded pixel-map comparisons. Checks follow the actual bound texCoord,
  account for glTF's V flip, and inspect decoded images after reimport.
- Smithy lifecycle checks retained a protected vertex edit, an explicit material
  replacement, an edited Normal Map strength and deterministic cached maps.
  Unprotecting restored source geometry; temporary save/reopen retained settings,
  packed images and UVs. Protected-fire full regeneration retained stone/roof
  fingerprints. Roof-only regeneration repacked the atlas but preserved 432
  sampled albedo/normal/ORM values (maximum error 0.000000593).
- [Legacy farmhouse smoke](legacy_surface_check.json) passed on 26 meshes,
  including legacy shader edits, roof palette, existing UVs, new surface UV
  correspondence, normalized exported data and all 11 PBR atlas banks.
- Isolated extension installation generated/exported the
  [Smithy](install_smithy.json) and [Gatehouse](install_gatehouse.json) from the
  same archive. Profiles were isolated from the user's installed add-ons.
- A [large authoring-range fixture](range_check.json) also generated successfully:
  legacy L-shaped farmhouse, width24/depth16, three floors, HIGH/EFFICIENT,
  seed17; 91,498 native vertices and 10 atlas banks. Its largest atlas is
  4096 × 3644. This is a boundary generation check, not an additional visual
  benchmark, all-parameter guarantee or runtime test.
- [Evidence verification](verification.json) checks all 44 images, six sheets,
  four reimport views, current source bytes, native records and all 30 archive
  members. All 48 historical v08 benchmark image hashes still match. Archive
  SHA-256: `fce644532bb1fa714ecfa515bd680fc44aa09d5d9ca642d588bcc820be0cb919`.
- A [rendered color-space probe](color_space_probe.json) compares direct linear
  color against byte-backed image encodings. Albedo follows
  [glTF's sRGB rule](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#materials);
  normal and ORM stay linear. ORM G is roughness, B metallic, R constant one;
  this does not claim baked ambient occlusion.

## Costs, limitations and review findings

| MEDIUM/EFFICIENT reference | Geometry, unchanged | Atlas texels across banks | GLB | Packed native scene |
|---|---|---:|---:|---:|
| Smithy | 8,136 vertices / 9,352 triangles / 65 objects | 6,293,504 × 3 maps | 11.84 MB | 10.91 MB |
| Gatehouse | 34,996 vertices / 42,006 triangles / 149 objects | 21,919,744 × 3 maps | 50.40 MB | 46.13 MB |

These are authoring/export diagnostics, not runtime memory or performance
measurements. Per-face atlases buy spatial condition without geometry inflation,
but materially increase texture storage; concealed faces and small charts still
consume space. Density follows detail level, with twice the base density for
wood, 256-pixel chart caps and 4096-pixel atlas dimensions. This resolution policy
is not an evidence-based universal runtime budget. No Unity testing was done.

Independent Luna review rejected early samples despite passing numeric tests:
age/upkeep were too alike and grain too regular. Corrections strengthened
silvering, lower-course weathering, grain flow, preparation and maintenance
contrast. Its final read found upkeep side-by-side legible; **age remains subtler,
workmanship is still weak at full-building distance, and timber grain remains
more parallel than the older broad-grain comparator**. Root reviewed the final
before/after and control evidence and reimport views. The default before/after
change is restrained; the larger improvement is controllable history on the same
architecture. A valid map or changed hash does not establish accepted art.

No new geometry damage, chipped silhouettes, furnishing or clutter compensates
for these limitations. Weathering is a local heuristic without true occlusion,
terrain, water level or rain-shadow simulation. Other regions/functions share
the reusable pipeline but have not received this matched artistic review.
Blender 5.0.1 was executed; the declared 4.2 minimum was not newly runtime-tested.
Protected/custom materials intentionally remain under the artist's control and
can retain earlier surface treatment.

## Corrections and efficiency lessons

The first pilot exposed incorrect albedo encoding; the rendered emission probe
replaced guesswork with a permanent inexpensive check. Later inspection found
empty legacy soot metadata in these host zones, so the finish now derives heat
from actual generated roles. Integration review caught protected/scoped source
omission and added a permanent regression. A failed scoped fingerprint comparison
was corrected to compare bound pixel appearance, since repacking is legitimate.

Bounded Luna work supplied the vector sampler, causal tests, native export tests,
legacy test maintenance and independent image critique; root owned context,
atlas integration, corrections and final review. One initial test unnecessarily
rehash-read entire images per mesh because of eager `setdefault` evaluation;
unique-image caching and sampled comparisons removed that repetition while
retaining actual embedded-payload and decoded-image checks. Several local pilots
were needed to expose weak artistic contrast. Future work should use smaller
targeted preparation swatches before repeated building-wide sweeps.

No model-token totals, subscription allowance deltas, API dollars or total task
wall time were recovered. Test/capture durations are not model-cost estimates.
No universal model-efficiency or artistic-success claim is supported by this run.
