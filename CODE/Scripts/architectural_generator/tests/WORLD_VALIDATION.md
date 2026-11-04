# World aware architecture validation (v0.4)

This record covers the world aware geometry and Blender integration in the
architectural generator. It distinguishes automated checks, generated images,
and a small blind visual review; the image review is not a human study and does
not establish production art acceptance.

## Automated checks

- **Legacy Python:** 37 existing tests passed with world awareness disabled or
  using legacy settings. This checks that the original generator path remains
  available.
- **World geometry:** 6 world matrix/geometry tests passed, followed by a focused manual-world-input regression (7 tests total). The low detail matrix covers
  all 4 regions × 20 building functions × 3 wealth levels (**240 settings**).
  The selected high detail SOLID/EFFICIENT profiles cover another **16
  settings**. The suite checks repeatable geometry hashes, occupied volume
  overlap, world access and platform support, openings, party walls, and legacy
  defaults.
- **Context stress:** the final root stress run exercised **80 varied context
  and craft/age/wealth settings** and passed in **36.501 seconds**. The exact
  cases and source hashes are recorded in
  `../evidence/world_context_stress.json`.
- **Blender:** the final combined Blender batch passed **7 test methods across 5 modules** in
  **150.5 seconds** on Blender 5.0.1. The batch included the legacy scene
  fixture, world mesh/BVH checks, roof clearance, glass/timber surface checks,
  and both profile integration fixtures. The roof suite exercised 21 roof
  fixtures; the surface/BVH suite included 4 older representative cases.
  The world Blender checks also covered window glass/frame/opening meshes,
  regeneration protection, and GLB/settings sidecar output.

An additional paired HIGH-detail world geometry measurement compared SOLID
with EFFICIENT output for four ESTABLISHED cottages (same seed and settings
apart from geometry mode). Triangle counts were: Lowmark 31,492 → 16,179
(48.63% fewer), Thornfell 36,768 → 20,670 (43.78%), Mire 57,868 → 20,500
(64.57%), and Emberholt 19,872 → 18,057 (9.13%). These measurements are in
`../evidence/world_geometry_diagnostics.json`; Emberholt starts with compact
terraced geometry, so the reduction is smaller.

## Geometry and source evidence

`../evidence/world_matrix_240.json` records the 240 low detail cases and their
repeat hashes. `../evidence/world_selected_profiles.json` records the selected
high detail profiles. `../evidence/world_source_equivalence.json` regenerates
**388 recorded settings**, including the original 304 matrix, selected-profile
and comparison-frame records plus the feature, context-stress and installed
export records: **388 matched geometry hashes, 0 mismatches**.

Rendered source files changed during the bounded architectural revisions, so
their source byte hashes are not all identical to the final source. The
evidence retains the source hash snapshots for the earlier render batches.
Rather than claiming the old image bytes were rendered by the final source,
the equivalence check establishes that the final source regenerates the same
geometry hashes for those settings. The final editable four cottage scene is
also saved with geometry and validation metadata in
`../evidence/world_four_region_cottages.blend` and its manifest.

## Visual evidence

There are **44 regional clay comparison frames** in the archived world render
batches. The later Lowmark and Thornfell architectural distinction pass
refreshed 24 frames; Mire and Emberholt frames remained from the earlier
render batch. The first four cottage blind and labeled panels, wealth cottage
panel, function matrix panel, and high profile panel are under `../evidence/`.

A blind reviewer classified the four cottage panel as follows:

| Blind ID | Region | Review confidence | Read from the clay view |
|---|---|---|---|
| C | Lowmark | High | Rural work compound with open sided work bay, posts, and entry steps |
| A | Thornfell | Medium-high | Heavy masonry cottage with repeated stepped roof and gable edging |
| D | Mire | Very high | Raised house with exposed supports, deck, and long stair |
| B | Emberholt | Medium-high | Broad layered masonry block with parapet and ordered openings |

The reviewer noted that Emberholt can still read as a generic flat roof
masonry block, and that chimneys, doors, stairs, and repeated rectangular
openings are shared cues. This is a useful structural comparison, not a claim
that the buildings have finished production art or that every regional cue is
fully resolved.

The feature renders add function specific geometry not represented in the
cottage comparison: a Lowmark Miller wheel and raceway, a Mire Boathouse
slipway, and an Emberholt Smithy work range, terraces, vent shafts, and iron
walk. Miller and Boathouse use neutral clay. Emberholt uses the backend
materials and has an editable compressed Blender scene.

- `../evidence/world_lowmark_miller_high.png`
- `../evidence/world_mire_boathouse_high.png`
- `../evidence/world_emberholt_smithy_high_pbr.png`
- `../evidence/world_emberholt_smithy_pbr.blend`
- `../evidence/world_feature_heroes_manifest.json` records exact settings,
  generated geometry hashes, validation and backend metrics, Blender version,
  render/build timings, image and scene hashes, and source module hashes.

## Final package verification

The final 0.4 ZIP installed/enabled in isolated Blender preferences and generated
an EFFICIENT world Emberholt Smithy through the real operators: 74 visual meshes,
18,230 vertices and 15 approximate collision proxies across three construction
zones. Generate and Export passed; GLB, collision GLB and settings sidecar are
retained under `world_installed_smithy.*`. A second isolated install generated the
preserved legacy Lowmark Farmhouse (26 visual meshes, 33,278 vertices). Both runs
tested archive SHA256 `5570d6c42885a69190f640f83dcf0dcb7a95d0f5ea8fdad652d8be57c56a345d`.
All packaged source, manifest, license and bundled guides match the local files.

The extended final replay includes all 304 prior records plus the three feature
heroes, 80 varied-context cases and installed world export: **388/388 geometry
hashes matched**, with no validation failures. The source-equivalence JSON retains
the actual older render-source snapshots and the final source fingerprint.

## Reproduction

From the generator directory, run the Python suites with Python 3.11+, and run
the Blender fixtures with Blender 5.0.1. The feature evidence can be regenerated
with:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/render_world_feature_heroes.py
```

The feature script saves its manifest and outputs under `evidence/`.
