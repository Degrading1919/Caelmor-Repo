# Validation record

Recorded for the standalone Blender add-on. These checks validate generated authoring geometry, Blender scene behavior, and interchange data; they do not measure game runtime performance or establish Unity compatibility.

## Current v0.3.0 verification (2026-11-02)

The following results apply to the current v0.3.0 source. The final Python suites passed 37/37 tests: 17 generator/model tests, 3 mesh geometry tests, 8 expansion tests, and 9 facade raycast/assembly tests. The suites cover all 20 type profiles as real, semantically distinct geometry; region/context/type/wealth profile resolution; wealth versus upkeep independence; legacy/manual settings; full window-frame and shutter bounds against plates, posts, braces, and gable members; aperture rays through wall and regional cladding; and closed core solids with explicit `SURFACE` decorative layers in EFFICIENT mode.

The frozen source also passed the 96-case seeded expansion stress run (seed 7447, 96/96 valid, 96.523 seconds). Its cases include the regional type matrix and manual roof/footprint extremes, with repeated deterministic generation, roof coverage and overlap, and assembly-clearance checks. The report is `../evidence/expansion_stress.json`.

Blender 5.0.1 checks passed:

- `test_blender.py`: 1/1 integration test, 19.668 seconds. It covers registration, generation, protected mesh edits, scoped and full regeneration, preservation of manually authored objects, GLB export/reimport, collision proxies, and save/reopen behavior.
- `test_profiles_blender.py`: 2/2 tests, 17.717 seconds. Four regional material banks coexist in one scene; legacy snapshots normalize to manual Lowmark SOLID Gable settings and regenerate.
- `test_glass_timber_bvh.py`: all 4 mixed region/floor/pitch fixtures passed with no actual triangle BVH intersections between glass and structural timber.
- `test_roof_clearance.py`: 21/21 fixtures passed in 135.986 seconds. Mesh vertices, edge midpoints, and face centroids were checked against the roof underside; fascia clearance was checked against its supporting plane. The required structural timber/detail clearance is 120 mm.
- `smoke_surface_export.py`: passed. The generated scene contained 26 visual meshes, 12 materials, and 12 packed maps; decoded GLB color attributes matched Blender tint data, including the resolved regional roof palette.

The Blender visual pass used EEVEE in Blender 5.0.1 with 16 samples. It rendered 29 comparison rows: four regional Cottages, Modest/Established/Affluent Lowmark houses, maintained/neglected condition variants, and all 20 building types. Separate sheets compare the four regions, wealth, maintenance, and a Thornfell Watchtower rendered in SOLID and EFFICIENT modes. Closeups cover a window and beam assembly plus gable and hip roofs. The gallery camera fits projected bounds from the actual mesh objects, including wings. Evidence is in `../evidence/`: `expansion_hero.png`, the labeled comparison sheets, `expanded_type_gallery.png`, the closeups, `solid_efficient_roof_comparison.png`, `expansion_evidence.blend`, and `expansion_evidence_manifest.json`.

The render manifest records exact input and effective settings, per-module source SHA256 hashes and loaded module paths, geometry hashes, validation results, actual Blender material counts/colors, triangle and vertex counts, and per-step timings. All 29 render rows matched pure-buffer material counts and Blender collection geometry hashes. In the high-detail Thornfell Passwatch Watchtower comparison, SOLID had 27,554 vertices and 41,408 triangles; EFFICIENT had 21,919 vertices and 23,697 triangles, a measured reduction of 20.45% in vertices and 42.77% in triangles. Both modes validated; the continuous roof deck and structural core remain SOLID, while selected decorative courses and cladding skins use explicit `SURFACE` topology. Nine paired geometry diagnostics across Lowmark Farmhouse, Thornfell Watchtower, and Emberholt Smithy at LOW/MEDIUM/HIGH detail are recorded in `../evidence/geometry_mode_diagnostics.json`. The reported HIGH-detail triangle reductions are 51.67%, 42.77%, and 61.73% respectively. These are measured authoring-mesh counts, not a fixed budget or runtime benchmark.

The scene and renders show the implemented geometry for each type profile; profile names and feature hints do not imply that every named feature is modeled. Some hints such as a wheel, lean-to, or arcade do not currently produce dedicated geometry. Collision proxies remain approximate static wall/footprint shapes and have not been tested for traversal or in Unity. Lightmap packing is simple, and weathering is heuristic material variation rather than measured simulation. The checks are Blender authoring and export validation, not structural certification, a game runtime check, or a player-experience test.

The final ZIP was installed and enabled using isolated Blender preference and extension directories, then the actual UI operators generated and exported an EFFICIENT Thornfell Watchtower: 22 visual meshes, 21,836 vertices and 5 collision proxies. `verify_install.py --region THORNFELL --function WATCHTOWER --geometry-mode EFFICIENT --export evidence/installed_thornfell_watchtower.glb --report evidence/installed_extension_verification.json` passed. The earlier v0.3 default SOLID Lowmark farmhouse install/export also passed (26 visual meshes, 33,278 vertices and 8 proxies). Both installed exports' exact saved settings reproduce their source geometry hashes in current pure Python. All nine packaged source modules and bundled documentation match the local files; render and geometry-diagnostics hashes match the source. The final tested archive SHA256 is `e5b9f0b1fc86223b7c592be70686590494c6a8fbdc8f9e80b400df3e9deab05e`.

## Historical v0.2 baseline (not current v0.3 validation)

The sections below preserve the earlier v0.2 validation record for context. Their five-function tests, 17-fixture roof matrix, 10-building render set, counts, timings, and package-verification results describe that prior source and must not be read as v0.3.0 results.

## Pure Python suites

Executed with Python 3.13:

```powershell
py -3.13 -m unittest discover -s tests -p test_generator.py -v
py -3.13 -m unittest discover -s tests -p test_geometry.py -v
```

Both commands passed: 17 generator/model/facade/roof tests and 3 geometry tests (20 total). Coverage includes deterministic seeds and named random streams, all five functions, RECT/L/T/U footprint bounds and area, settings guards, legal nonoverlapping openings (default fixtures retain a 2.0 m door clear height; the minimum-height, steep-pitch Inn fixture permits about 1.904 m), facade parameter isolation from roof generation, principal-post clearance, full brace-body clearance and ascending/descending brace cases, gable rake/kingpost/collar support, analytic roof-envelope and deck clipping, roof seam topology, variable-width course consistency and bounded eave repairs, LOW/MEDIUM/HIGH geometry growth, the near-equal-width/depth regression case, and closed outward-wound generated and primitive solids including chamfered beams. A targeted regression inserts a valid closed legacy-style eave post above the roof underside and confirms `validate` rejects the buffer with the timber-clearance error.

The repository lead ran the final `stress_geometry.py` roof/frame gate on 80 randomized supported inputs (seed 7447); all 80 passed in 34.63 seconds. That independent sweep includes full solid validation, projected roof coverage, pairwise visible-patch overlap checks, and structure/brace clearance from the roof underside.

The frame layout reports one 4.4143 m unsupported span in a Grain Store U footprint. Overlapping door and vent clearance regions leave no legal full-height principal-post station in that interval. The span remains explicit in the layout diagnostic; the full building validates and brace clearance remains intact.

## Roof clearance regression

Executed with Blender 5.0.1:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_roof_clearance.py
```

All 17 generated builds passed in 85.153 seconds. The matrix covers L/T/U/RECT footprints at 30°, 48°, and 60° pitch with varied dimensions, plus one-storey minimum-floor-height (2.4 m), 60° RECT cases for all five functions. It samples mesh vertices, edge midpoints, and face centroids. Structural timber and timber details remain at least 120 mm below the roof's analytic upper surface; fascia remains below its extended supporting plane. Walls can meet the roof deck at eaves; the largest sampled wall contact residual was 6.8 mm under the covering. The original reported fault was a facade timber post extending 139 mm above the roof plane at the outer eave. The frame datums and fascia section were corrected, and `engine.validate` now rejects timber structure/detail buffers that cross the deck underside.

## Blender integration

Executed with Blender 5.0.1:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_blender.py
```

The final-source integration test passed in 15.406 seconds. It registers the add-on, generates two selected buildings at a cursor origin, moves/scales a root anchor, protects and vertex-edits a generated buffer, runs scoped and full regeneration, checks that protected and manually authored objects remain intact, unprotects and verifies replacement without duplicates, validates closed collision proxies and UV channels, exports visual and collision GLBs with a JSON manifest, parses GLB JSON for embedded images, palette factors, normal texture UV selection and both UV attributes, reimports the visual GLB, and saves/reopens the Blender file.

The final-source Blender surface-export smoke passed. It verifies revision-aware reuse without overwriting a legacy material, preservation of manual edits, revision-tagged packed image banks, roof-patch palette color, embedded color/normal/roughness resources, and decoded GLB `COLOR_0` value parity with source Blender tints for plaster and roof meshes. Every decoded color component passed the glTF `[0,1]` bound check required by the [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.pdf). On the seed-17 farmhouse, plaster tint RGB ranged from 0.877374 to 1.0 and roof tint from 0.890000 to 1.0; both source and exported accessors matched within 1e-5. The generated plaster and stone albedo image channels ranged 0.91373–1.0 and 0.88627–1.0 respectively.

The repository lead also ran the packaged extension through an isolated Blender extension repository, installed/enabled it, generated a building, and invoked its Export operator using:

```powershell
py -3 verify_install.py --export evidence/farmhouse.glb
```

The final installed-archive run passed with 24 visual mesh objects (37,362 vertices) and 8 collision proxies. It produced `farmhouse.glb`, `farmhouse.collision.glb`, and `farmhouse.caelmor.json` in `evidence/` from the 0.2.0 packaged extension.

The lead regenerated the installed export's exact saved settings in pure Python
and reproduced its source geometry hash. All eight packaged source modules also
matched the render manifest's source hashes and the final extension ZIP's bytes.

## Visual evidence run

Executed with Blender 5.0.1 using `BLENDER_EEVEE` and 16 render samples:

- Ten buildings: Farmhouse, Barn, Grain Store, Miller, and Inn, each with two seeds.
- Footprints include L, U, RECT, and T. One farmhouse has a deliberate dimension, footprint, and floor-count edit.
- Four oblique camera views per building produced 40 frames at 360 × 360 pixels. The script combined them into a contact sheet and removed the intermediate frames.
- The hero image is 1200 × 1200 pixels; four 900 × 900 closeups cover timber joinery, roof valley, exterior materials, and the south eave; the full-set overview is 1800 × 1100 pixels.
- The editable scene was saved with compression before contact-sheet composition. The evidence manifest records settings, geometry hashes, object counts, bounds, renderer, and Blender version.
- The ten buildings contain 214 generated visual mesh objects and 453,086 vertices in total. These are source geometry counts, not triangles or runtime memory.
- `tests/update_evidence_manifest.py` regenerated and compared all ten geometry hashes, visual mesh counts, and vertex counts against the saved evidence record; all matched.

The current run's manifest records per-building Blender construction time (33.3131 seconds total), independent pure generation/validation time (10.8151 seconds total), hero time (2.362 seconds), closeup times, contact-sheet time (7.148 seconds), and overview time (0.793 seconds). The editable ten-building scene is about 23.7 MB; the evidence directory is about 38.9 MB including a read-only copy of the original hero for visual comparison. Evidence files are in `../evidence/`: `baseline_hero.png`, `hero.png`, `closeup_eave.png`, `closeup_valley.png`, `closeup_surfaces.png`, `closeup_timber.png`, `overview.png`, `ten_buildings_four_views.png`, `ten_buildings.blend`, and `evidence_manifest.json`.

## Scope limits

The visual pass is a Blender render, not a player or Unity runtime check. The buildings are exterior-only. The exported collision proxies are approximate static wall and footprint shapes and have not been tested for traversal. Per-face lightmap packing is intentionally simple and can use atlas space inefficiently. Weathering and material variation are heuristic procedural artwork, not measured simulation. Exported material behavior and lighting still need review in any target engine.
