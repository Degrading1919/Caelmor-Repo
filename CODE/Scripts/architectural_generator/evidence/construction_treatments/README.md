# Construction treatment benchmarks

The v0.13.0 treatment path is compared with the legacy path at seed 91 using
Blender 5.0.1. Both sides of each pair use the same function, region, site
grammar, craftsmanship, condition, geometry mode, camera and lighting. The
legacy geometry comes from the behavior at `abfa9f0`. The
[manifest](manifest.json) records settings, source and image hashes, and camera
values. Side lighting, neutral clay and matched material views separate
physical relief from finish.

- [Lowmark Smithy sheet](smithy_review.jpg)
- [Thornfell Gatehouse sheet](gatehouse_review.jpg)
- Smithy joinery detail in clay, [before](joinery/before/smithy/close_clay_0.png) and [after](joinery/after/smithy/close_clay_0.png)
- Lowmark Stable reuse in [clay](reuse/stable/normal_clay_0.png) and [material](reuse/stable/normal_material_0.png)
- [Installed Blender extension](../../dist/caelmor_architecture.zip) and [isolated install record](install.json)

| Fixture | Legacy triangles | Treated triangles | Difference |
| --- | ---: | ---: | ---: |
| Lowmark Smithy | 12,838 | 14,407 | +1,569 (12.2%) |
| Thornfell Gatehouse | 66,483 | 72,918 | +6,435 (9.7%) |
| Lowmark Stable (reuse) | — | 15,155 | — |

| Treatment | Evidence to inspect |
| --- | --- |
| Stone masonry | Gatehouse return footings, staggered field joints, selected projecting headers and full-depth coping. Smithy and Stable also use stone plinths. |
| Dressed stone | Gatehouse portal rings, vault and jambs. The rings use shaped radial voussoirs and the jamb courses support the spring. |
| Structural timber | Smithy main and stock-range bents, seated pins, housed shoulders, projecting through-tenons, tapered faces and roof clearance. Stable reuses the regional support and frame treatment. |
| Wooden boarding | Smithy stock-range boards with varied widths, seating and bottom edges, overlaid battens, Gatehouse pocketed leaves, timber deck boards. |
| Wooden shingles | Smithy and Stable, using staggered courses with varied unit length and thickness, split corners and physical laps. |
| Slate/tile roofing | Gatehouse, using thinner slate edges on the same course placement system. Fired clay selection was verified in pure geometry. |
| Plaster/limewash | Render on Smithy and Stable infill; the pure checks also generate thick render and zero-relief limewash on stone hosts. |

## Review

The first treatment comparison left the Smithy visually too close to its
control. The Creative Director identified flat roofing, flush boarding and
uniform timber. The revised side-lit clay shows shingle butt shadows and
board edges at normal scale. The exposed posts and ties retain straight
bearing ends with less regular sections in the span. Through-tenons and the
small render losses remain close-view cues. Review of the first side-lit
pass also exposed a gable projection from a shared slope variable. The
corrected pass and a wall-envelope regression separate board tilt from the
roof clipping plane.

The Gatehouse returns now read as bonded masonry at normal scale. Footing,
headers and coping cast distinct shadows in clay. The ends remain flat site
connection faces and the portal and through-route stay open. Slate edges
remain finer than split-wood butts. The rendered trials cover one seed per
building. Other seeds were tested geometrically.

The technical review used separately generated legacy meshes, geometric
ray checks and Blender BVH checks, plus inspection of the exported GLB.
The artistic review used the matched clay and material frames at their
stated studio scales. Production art acceptance and runtime traversal remain
separate gates.

## Verification

- `test_construction_treatments.py` passed five gates covering fixed-seed
  repeatability, all seven treatments, shared construction across functions,
  both geometry modes, incompatible requests, per-field override precedence,
  slate and fired clay, finish invariance, render and limewash, passage
  raycasts, a Smithy skin envelope and cover gauge check, and unchanged
  specialized reed and iron cover meshes.
- `test_architectural_benchmarks.py` passed six gates, including 78 historical
  geometry hashes. A pure seed-91 medium/efficient sweep also validated 80
  opted-in region/function combinations and 12 additional benchmark seed and
  geometry-mode combinations.
- `test_construction_blender.py` passed legacy settings restoration, rejection
  without collection changes, protected geometry, slot replacement, named
  finish, scoped regeneration, UVs, Gatehouse BVH passage and identical
  collision proxies. The Gatehouse GLB reimported 155 meshes and contained
  13 mapped materials and 30 embedded images.
- `verify_install.py --function SMITHY --geometry-mode EFFICIENT` installed
  the tracked extension with isolated preferences and generated a functional
  Smithy with 69 render meshes.

- The targeted native `test_roof_clearance.py` check passed on the steep
  Lowmark L-plan in both legacy and opted-in construction. The full legacy
  native roof matrix was stopped after the scoped replacement was available.

The treatment builders use original Caelmor geometry and textures. Reference
studies informed material reuse and selective depth. No external research
assets are distributed here.
