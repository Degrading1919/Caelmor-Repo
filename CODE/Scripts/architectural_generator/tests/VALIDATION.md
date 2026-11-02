# Validation record

Recorded for the standalone generator source in this repository. The checks below validate generated geometry and Blender interchange behavior; they do not measure game runtime performance or establish Unity compatibility.

## Pure Python suites

Executed with Python 3.13:

```powershell
py -3.13 -m unittest discover -s tests -p test_generator.py -v
py -3.13 -m unittest discover -s tests -p test_geometry.py -v
```

Both commands passed: 11 generator/model/facade/roof tests and 3 geometry tests. Coverage includes deterministic seeds and named random streams, all five functions, RECT/L/T/U footprint bounds and area, settings guards, legal nonoverlapping openings including the 1.9 m minimum door clear height, facade parameter isolation from roof generation, analytic roof-envelope agreement, roof seam topology, the near-equal-width/depth regression case, and closed outward-wound generated and primitive solids.

The repository lead also ran `stress_geometry.py` on 80 randomized supported inputs (seed 7447); all 80 passed in 21.97 seconds. That independent sweep includes full solid validation, projected roof coverage, and pairwise visible-patch overlap checks.

## Blender integration

Executed with Blender 5.0.1:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.0\blender.exe" --background --python tests/test_blender.py
```

The integration test passed. It registers the add-on, generates two selected buildings at a cursor origin, moves/scales a root anchor, protects and vertex-edits a generated buffer, runs scoped and full regeneration, checks that protected and manually authored objects remain intact, unprotects and verifies replacement without duplicates, validates closed collision proxies and UV channels, exports visual and collision GLBs with a JSON manifest, parses GLB JSON for embedded images, palette factors, normal texture UV selection and both UV attributes, reimports the visual GLB, and saves/reopens the Blender file.

The repository lead also ran the packaged extension through an isolated Blender extension repository, installed/enabled it, generated a building, and invoked its Export operator using:

```powershell
py -3 verify_install.py --export evidence/farmhouse.glb
```

That installed-archive run passed with 22 visual mesh objects and 8 collision proxies. It produced `farmhouse.glb`, `farmhouse.collision.glb`, and `farmhouse.caelmor.json` in `evidence/`.

## Visual evidence run

Executed with Blender 5.0.1 using `BLENDER_EEVEE` and 16 render samples:

- Ten buildings: Farmhouse, Barn, Grain Store, Miller, and Inn, each with two seeds.
- Footprints include L, U, RECT, and T. One farmhouse has a deliberate dimension, footprint, and floor-count edit.
- Four oblique camera views per building produced 40 frames at 360 × 360 pixels. The script combined them into a contact sheet and removed the intermediate frames.
- The hero image is 1200 × 1200 pixels; the full-set overview is 1800 × 1100 pixels.
- The editable scene was saved with compression before contact-sheet composition. The evidence manifest records settings, geometry hashes, object counts, bounds, renderer, and Blender version.
- The ten buildings contain 194 generated visual mesh objects and 296,218 vertices in total. These are source geometry counts, not triangles or runtime memory.
- `tests/update_evidence_manifest.py` regenerated and compared all ten geometry hashes, visual mesh counts, and vertex counts against the saved evidence record; all matched.

Evidence files are in `../evidence/`: `hero.png`, `overview.png`, `ten_buildings_four_views.png`, `ten_buildings.blend`, and `evidence_manifest.json`.

## Scope limits

The visual pass is a Blender render, not a player or Unity runtime check. The buildings are exterior-only. The exported collision proxies are approximate static wall and footprint shapes and have not been tested for traversal. Exported material behavior and lighting still need review in any target engine.
