# v0.5 final validation and independent visual review

## Machine checks

The lead executed the following checks; the independent reviewer did not rerun them:

- A 59-test Python integration batch passed in 128.070 s: 37 retained legacy tests, 7 world tests, 7 rural household tests, 3 Emberholt household tests and 5 investment/roof tests. The world suite includes 240 region/function/wealth settings and selected detail modes. The batch preceded final metal-sheet subdivision/finish refinement; the 5 affected investment/roof tests were rerun afterward (3.629 s).
- The 80-case varied-context/detail/condition stress pass succeeded in 34.282 s. After source review restored ROUGH Emberholt rubble and FINE Thornfell dressed courses, the new stone-craftsmanship regression passed (0.713 s) and all 14 affected stress settings were revalidated. Other regions/standard-workmanship geometry did not change.
- Seven Blender 5.0.1 regression methods across five retained modules passed in 152.818 s: legacy integration, 21 roof-clearance fixtures, four older glass/timber BVH fixtures, profile migration/material banks and world mesh/protected-regeneration/export checks.
- Fourteen new Blender household fixtures passed actual aperture rays, glass/structure BVH checks and door-clearance probes in 25.707 s. Four affected Emberholt fixtures passed again after the metal-sheet refinement (4.852 s). These native fixtures use STANDARD workmanship; the later workmanship correction has separate Python/geometry checks and rendered views, not a claimed rerun of those native fixtures.
- The packed-material/GLB surface smoke passed with revision 4, 26 visual meshes, 12 materials, 12 packed images, normalized exported colors and retained legacy material datablocks.
- The independent Lowmark roof scan first found six crossings in non-domestic main hall/service range pairs. Moving those ranges to an independent yard position with a 0.85 m gap cleared all six analytic roof crossings; `engine.validate` passed all six. The exact settings and source fingerprints are in [`v05_cross_roof_corrections.json`](../evidence/v05_cross_roof_corrections.json).
- Final Farmhouse render review found a separate access defect: an open working
  range had no opening record, allowing a principal post or diagonal across its
  central steps. Open entrance edges now reserve a 1.8 m wide, 2 m high approach;
  Lowmark working ranges have sufficient headroom. The new triangle-ray regression
  passed eight function/wealth cases (one method, 2.179 s). The seven rural tests
  passed again (15.303 s), as did the five investment/roof tests (3.641 s). Three
  affected Lowmark Blender fixtures passed aperture/BVH/door checks (6.883 s);
  their separate report is `v05_targeted_mesh_checks_lowmark.json`. Only affected
  Lowmark cottage and Farmhouse renders were refreshed afterward.

These checks establish generated geometry and Blender behavior for the listed fixtures. They do not establish target-engine runtime or production art acceptance.

## Native deliverable and compatibility

The final 0.5 ZIP installed/enabled in isolated Blender preferences and generated
an EFFICIENT Emberholt Cottage through the real UI operators: 49 visual meshes,
10,422 vertices. Generate and Export retained visual/collision GLBs and settings
under `v05_installed_emberholt.*`. A second native install generated the preserved
legacy Lowmark Farmhouse. Both reports tested archive SHA256
`93c5688f43e1edf2a033190e64a06b3a01beac556b8c1eb5f0bd54be7fa3d1ce`.
All 21 archive members match the local source/bundled documents.

`verify_household_evidence.py` reproduced all 53 final render records from 23
unique settings (one generation per unique configuration), verified 53 retained
raw-frame hashes, recorded published composite hashes and reproduced the native
export's source geometry hash. The older legacy farmhouse export still reproduces
its original geometry hash. Saved settings remain readable; World construction
intentionally changes with this revision, while the legacy path remains available.

Source snapshots are retained in each manifest. Some clay/material views precede
palette-only or non-STANDARD-workmanship changes; the final source reproduces
their geometry, and only dependent material views were refreshed. This is not a
claim that every image was rendered by byte-identical final source. Geometry
hashes alone do not establish unchanged shading, lighting or pixel identity.

## Controlled comparisons and rejected results

`ARTISTIC_REFINEMENT.md` fixed the early set before substantial implementation:
four regions × three wealth tiers, seed 91, cottage, age 35, maintenance .7,
STANDARD craft and MEDIUM/EFFICIENT detail. Cameras/light are fixed, with common
projected scale across the three tiers within each region. Regions have their own
framing; their images are not a metric comparison of cross-region dimensions.

- Final neutral cottage sheets contain 24 frames (two opposed views per building).
- Final material cottage sheets contain 12 front views of the same settings.
- Four existing function examples add eight material frames: Lowmark Farmhouse,
  Thornfell Inn, Mire Boathouse and Emberholt Smithy. Their individual framing is
  fitted for inspection, not a common-scale function experiment.
- The Mire condition sheet holds wealth constant and varies age/upkeep in three
  front views. Two stone-craft sheets hold household status constant and compare
  ROUGH/STANDARD/FINE in six front views. Labels explicitly describe the varied
  axis; condition/craft slots are not presented as wealth tiers.

The initial Emberholt pass added flues/details to broad slab bodies and was
rejected as still apartment-like. The second pass narrowed domestic bodies,
articulated lower work/private ranges and retained deep supported entrances.
Early Lowmark roof gaps were rejected by actual cross-plane tests; both new
household and six existing non-domestic examples were corrected. Material review
also rejected high-contrast scattered roof rectangles; the retained
`v05_rejected_finish_lowmark.png` records that appearance. Final cohorts have a
restrained stock range while the actual tile geometry remains unchanged.

The v0.4 images/manifests remain the before reference. Early v0.5 and revised
Emberholt sheets are labeled separately and are not substituted for final output.

## Independent render review

Reviewed the fixed neutral Mire cottage tier panel [`v05_final_cottage_clay_mire.png`](../evidence/v05_final_cottage_clay_mire.png) and the Emberholt PBR tier panel [`v05_final_cottage_pbr_emberholt.png`](../evidence/v05_final_cottage_pbr_emberholt.png). The Mire comparison communicates a small raised dwelling, a larger working deck, and a second affluent room volume. The Emberholt comparison communicates heavier vertical mass and a secondary service/private volume as wealth increases. No obvious roof breach or visibly floating geometry appears in these camera views.

The affluent Mire and Emberholt secondary volumes read as separate masses; their circulation and court relationship is not fully legible from these panels alone. This is an art-readability question for the Creative Director, not evidence of a failed door, support, or collision check. The panels are generated comparisons, not a human study or final art sign-off.

**Review result:** no concrete visual blocker was identified in the two inspected sheets. Keep final human art acceptance separate from the machine checks above.

After the open-work access correction, the independent reviewer also inspected
the refreshed Lowmark clay panel and the entrance-clearance source. The modest
and established shelter approaches appeared clear; no concrete blocker was found.
This was read-only review, not an independent rerun of the automated tests.

## Remaining art and technical limits

The lead inspected all four final cottage material panels, both clay perspectives,
the craft/condition panels and the representative function views. Wealth now changes
room/work/storage/access arrangements. Craftsmanship and age remain much subtler
than wealth at this camera distance; the craft comparisons do not establish strong
viewer classification, and the condition repairs need closer art review. Some broad
Emberholt faces remain austere/generic; courts and separate rooms can read as loose
outbuildings. These are material next art-review questions, not hidden completion
claims. No production-art approval or human recognition study is recorded.

Roof-crossing checks cover analytic weather planes of known masses, not arbitrary
CAD intersections of every decorative face. Collision proxies are approximate;
protected manual changes are preserved but outside procedural validation. No
interiors, terrain fitting, target-engine behavior or runtime performance is claimed.
GPL-3.0-or-later source/license remain bundled; geometry and maps are original.

## Efficiency observations worth carrying forward

Two bounded Luna High implementers owned regional files; the lead owned shared
geometry, rendering, Mire and integration. Early small-panel rejection changed the
Emberholt construction before broader evidence. The new between-volume roof gate
found a gap that occupied-volume/topology checks had missed. Material-only changes
refreshed material images; unchanged clay was retained with source/geometry evidence.
The final replay deduplicated 53 records to 23 settings. These are observable workflow
choices, not a measured token/quota/dollar saving or controlled model comparison.

## Reproduction

From this directory's parent, use Blender 5.0.1 and Python 3.11+:

```powershell
py -3 -m unittest discover -s tests -p test_household_investment.py -v
py -3 -m unittest discover -s tests -p test_stone_craft.py -v
py -3 -m unittest discover -s tests -p test_open_work_access.py -v
py -3 tests/stress_world.py --output evidence/v05_context_stress.json
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --factory-startup --background --python-exit-code 1 --python tests/test_household_blender.py
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --factory-startup --background --python-exit-code 1 --python tests/render_household_review.py -- --stage final
./tests/compose_household_review.ps1 -Stage final
py -3 tests/verify_household_evidence.py
```

The verifier does not rerender or benchmark. Raw frames are optional in a fresh
checkout; published composite hashes, settings, geometry hashes and source
snapshots remain available in the report. Isolated install reports and exports
are separate evidence, not synthesized from source presence.
