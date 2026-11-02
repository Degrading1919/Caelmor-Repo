# Validation record

Recorded for the standalone generator source in this repository. The checks below validate generated geometry and Blender interchange behavior; they do not measure game runtime performance or establish Unity compatibility.

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
