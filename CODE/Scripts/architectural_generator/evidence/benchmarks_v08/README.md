# Two procedural architectural benchmarks — 0.8.0

Creative Director review package for PR #85. These are generated Lowmark Smithy
and Thornfell Gatehouse outputs, with no manual mesh edits in the captured assets.
Technical gates passed; **artistic acceptance remains pending**. The changes have
not been extended to the other 78 region/function combinations.

## Controlled comparisons

Each sheet is 4276 × 1490 pixels. Columns are before front, after front, before
opposed view, after opposed view; rows are clay and materials. Close views use
two useful workfront/entrance angles and intentionally crop the whole building.

| Building | Normal view | Distant silhouette | Close inspection |
|---|---|---|---|
| Lowmark Smithy | [Comparison](comparison/smithy_normal.png) | [Comparison](comparison/smithy_distant.png) | [Comparison](comparison/smithy_close.png) |
| Thornfell Gatehouse | [Comparison](comparison/gatehouse_normal.png) | [Comparison](comparison/gatehouse_distant.png) | [Comparison](comparison/gatehouse_close.png) |

The [before individuals](before/individual/) and [after individuals](after/individual/)
retain all 48 matched PNGs. Editable final material scenes:
[Smithy](after/smithy.blend), [Gatehouse](after/gatehouse.blend).
Lifecycle-verified exports: [Smithy GLB](smithy.glb),
[Gatehouse GLB](gatehouse.glb), with adjacent collision GLBs and settings sidecars.
The [installable archive](../../dist/caelmor_architecture.zip) contains version 0.8.0.

Before source is `39f2e6c`; final source is `e5070b4`. Inputs are seed 91,
ESTABLISHED wealth, STANDARD craftsmanship, age 35, maintenance 0.7,
MEDIUM detail, EFFICIENT geometry, world generation enabled, AUTO local context
and grammar. Exact source byte hashes, settings, cameras, geometry hashes and
image hashes are in [before](before/manifest.json), [after](after/manifest.json)
and [composition](comparison/manifest.json) manifests. Each before/after camera,
target and orthographic scale matches. Normal/distant views contain the generated
bounds. Lighting and studio helper are unchanged. One native collection per case
is reused across cameras and finishes; clay/material images share geometry.

## Architectural changes and visual assessment

The smithy's former single shed envelope is replaced by a taller gabled forge
hall and lower boarded stock range. Exposed pegged timber bents, stone post shoes,
purlins and the main-to-lean-to junction establish a hierarchy visible in clay.
The open frontage retains the existing functional forge arrangement. A coursed,
open stack, fire screen, usable stock lane, workbench, repair wheel, tool storage,
threshold paving and cut-log anvil support describe agricultural repair work.
Charcoal, leather bellows skin and localized soot distinguish heat/work surfaces;
they do not substitute for the changed roof and frame composition.

The gatehouse replaces slender house-like towers with broad, projecting hipped
flanks, battered stone feet, bonded corners and story bands around a central
guard hall. The entrance is a real elliptical arch cut through walls, veneer and
collision geometry, with voussoirs and a segmented barrel vault. Gate leaves
stand in side pockets, leaving the declared route open; the grille has a real
raised opening. Defensive slots penetrate the actual walls. Both tower stairs
connect through four upper doors and supported thresholds to the guard hall.
Courtyard doors and short curtain returns establish a front/rear relationship.
The returns are site interfaces, not a complete fortress generator.

Root inspected all six final sheets, including opposed views. The changes alter
silhouette and construction at normal distance, not only close-up object counts.
The smithy's quieter rear and the gatehouse's austere walls remain deliberate
but may need stronger artistic treatment. Surfaces still look comparatively
clean and uniform, and several tools/mechanisms remain simplified. This is a
higher benchmark offered for review, not a claim of approved production art.

## Geometry cost

Counts describe authoring output for these fixed MEDIUM/EFFICIENT fixtures,
not runtime performance. No Unity tests or new performance benchmarks were run.

| Building | Vertices before → after | Triangles before → after | Objects before → after |
|---|---:|---:|---:|
| Smithy | 5,428 → 8,136 | 6,086 → 9,352 | 37 → 65 |
| Gatehouse | 36,904 → 34,996 | 44,118 → 42,006 | 154 → 149 |

The smithy's additional cost buys a second constructed roof range, primary
joinery and working features. The gatehouse's stronger composition costs fewer
triangles in this fixture. Neither observation establishes a general performance
advantage across seeds or detail settings.

## Executed verification

[Executed checks](executed_checks.json) record results, available durations and
local log digests. [Verification](verification.json) checks correspondence between
the final evidence, source, native meshes, exports and archive.

- Python integration: 33 methods passed before the final guard-hall access
  correction. All six final benchmark methods passed after that correction
  (34 distinct Python methods across these runs, not a single 34-test run).
  Coverage includes deterministic seeds 17/91/408, representative detail/geometry
  modes, roof hierarchy, real arch/slot apertures and supported upper access.
- Golden geometry checks preserve the other 78 region/function outputs. The
  previous shed-wall penetration fixture remains an explicit shed regression
  even though the benchmark smithy's principal roof is now gabled.
- Native Blender integration: [16 cases](mesh_checks.json) passed before the last
  guard-door connection; [the final two fixtures](benchmark_mesh_checks.json)
  passed afterwards. Fingerprints identify the sole intervening production
  module change. These check body routes, structural/opening intersections,
  stairs, roofs and forge exhaust where applicable.
- [Both lifecycle fixtures](lifecycle.json) passed: native aperture probes
  (including 36 defensive-slot/proxy rays and two curved-arch profile rays),
  protected edit preservation during regeneration, restoration after unprotect,
  unique IDs, two UV maps, GLB/settings export and reimport, save/reopen.
- Isolated archive installations generated/exported the [Smithy](installed_smithy.json)
  and [Gatehouse](installed_gatehouse.json); [legacy generation](installed_legacy.json)
  also passed. This does not claim a new exhaustive legacy lifecycle run.
- 48 matched images and six sheets verified; all 27 archive members match their
  workspace sources. Archive SHA-256:
  `9d67c8cfb9a57a8378a2d3a86d276a7d5404870a356bc5493c61d7baa74f7505`.
- 448 historical images still match their retained manifests. Earlier evidence
  is preserved. `pilot1` contains interrupted developmental captures and is not
  a controlled final comparison; `pilot2` predates the final upper-door links.
  Use only `before` and `after` for the controlled claims above.

## Corrections and workflow findings

The arch-volume test caught automatic guard-floor posts occupying the passage;
the final slab is borne by the vault. Architectural review caught the missing
connection between tower landings and the upper hall. Ordinary-window minimum
width logic initially discarded narrow defensive slots: explicit aperture roles
and pure/native air probes now enforce them. Boarded weather faces use the normal
facade builder, including collision proxies. A hip abutment's warped flashing
quad was replaced by clipping against the actual roof planes. These are semantic
construction fixes, rather than hiding meshes or weakening usable clearances.

The existing studio/render, composition and native build infrastructure was
extended instead of replaced. Small selected captures preceded final paired
capture. The broader native check was not repeated after the isolated upper-door
change; targeted final fixtures plus lifecycle checks cover that change.
Luna High captured the immutable baseline, then reported `usage_limit_exceeded`.
Root completed implementation, integration and visual review. No later independent
model art review is claimed. Subscription allowance, token totals, API cost and
total wall time were not recovered, so no numerical model-efficiency claim is made.

## Authority, references and limits

Approved regional dossiers and existing generator contracts govern the regional
interpretations. The [design contract](../../tests/V08_BENCHMARK_CONTRACT.md)
records the observable criteria and reference boundaries.
[Southwater Smithy](https://www.wealddown.co.uk/buildings/smithy-from-southwater/)
is explicitly a circa-1850 vernacular process analogue for economical timber,
local masonry and agricultural repairs, not a medieval design copied into lore.
[Dunstanburgh](https://www.english-heritage.org.uk/visit/places/dunstanburgh-castle/history/description/)
informs guarded passages, courtyard access and accommodation above; its exceptional
scale and exact design were not adopted. New code is original and retains the
add-on's GPL-3.0-or-later license; no reference assets or code were copied.

Final art review covers one matched established/standard seed per building.
Automated seed/detail coverage does not establish artistic quality for every
wealth level or seed. The studio does not demonstrate terrain integration;
functional clearances are not structural or thermal engineering certification.
Guard access is partial functional geometry, not a complete interior system.
Existing protected edits remain protected, but changes to building composition
may require manual reconciliation of older edits. Finish variation, wear and
equipment refinement remain possible next art tasks after Creative Director review.
