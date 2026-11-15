# Material height relief pilot

**Decision:** Keep this as a Blender authoring experiment. Do not expose whole-field displacement in the production Geometry panel. The close clay views prove the meshes have real depth. Under the elevated material camera, the existing normal maps communicate most of that depth at much lower mesh cost.

## Comparison

Generator baseline `62ccecf`. Fixture settings and camera transforms are in [measurements](measurements.json).

- Lowmark Cottage, 8 × 5.8 m manual blockout dimensions, one storey, seed 91. Displaced both roof slopes within the existing mapped covering section.
- Thornfell Gatehouse, existing construction-depth fixture. Displaced the mapped masonry section on floor 0 of the east watchtower. Quoins, window reveals, stringcourses, plinth, portal and other sections use the existing construction.
- Baseline is the existing texture-dominant representation with critical geometry retained. Keep camera, lighting, material nodes, PBR images and scale fixed between baseline and displaced frames. The modeled and hybrid rows provide context and retain the materials assigned by those existing representations.

| Fixture | Same-finish comparison | Existing representations | Sampling pitch in clay |
| --- | --- | --- | --- |
| Cottage | [Roof study](roof.jpg) | [Four roof representations](roof_alternatives.jpg) | [10 cm vs 5 cm](roof_sampling.jpg) |
| Gatehouse | [Masonry study](masonry.jpg) | [Four wall representations](masonry_alternatives.jpg) | [10 cm vs 5 cm](masonry_sampling.jpg) |

The denser roof shows course shadows and shallow lifts up close. The field still reads as a continuous sheet in clay. It cannot reproduce an exposed shingle butt or undercut. At 10 cm, the roof samples miss some joints and the masonry beds become soft and uneven. At 5 cm, the masonry beds become recognizable in clay and the textured stone faces become rounder. The normal map already describes those same joints, which can make the combined finish look inflated up close. The silhouette, aperture outlines and visible construction boundaries stayed stable in the matched views. These observations apply to the two captures and the existing finishes.

## Implementation and cost

Caelmor's existing construction materials derive tangent-space normals from an original height field in metres. The pilot reads that same height and preserves albedo, normal and ORM generation. It uses a shared scalar image and the same affine surface UVs for the mapped field. Blender Simple subdivision refines a flat editable cage, then a native Displace modifier pushes its interior outward. The perimeter and the first 12 cm of each planar chart are held flat, with another 12 cm of feathering. Roof edges, openings, structure and collision are handled by the existing generator.

The relief strength and subdivision settings live on separate modifiers. The controlled run used 40 mm for unit image white, approximately 23 mm of actual peak roof lift and 26 mm in stone. A separate input test loaded Caelmor's Brookoak displacement EXR and measured 34 mm. External height must be a scalar image interpreted as Non-Color, using the same UV layer, repeat policy and scale as the surface textures. A different UV layer can be chosen explicitly in the pilot. Automatic transfer of arbitrary material-node transforms and direct live Substance graph binding remain outside this proof.

| Fixture | Modeled tris | Hybrid tris | Mapped baseline tris | 10 cm tris | 5 cm tris | Visual GLB, baseline → 5 cm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cottage | 11,416 | 9,819 | 9,419 | 23,815 | 67,015 | 3.22 → 5.32 MB |
| Gatehouse | 76,972 | 54,595 | 41,151 | 64,997 | 136,829 | 12.68 → 16.23 MB |

The roof field alone went from 4 to 57,600 triangles. The selected masonry section went from 38 to 95,716. Building-wide visual mesh nodes and GLB primitives stayed at 31 for the Cottage and 188 for the Gatehouse. Images stayed at 30 and 25 respectively. The Gatehouse GLB has a duplicate entry for the same stone shader and image bindings, taking its material table from 11 to 12. Unity shared-material counts were 13 and 11. Image, primitive and renderer counts describe exported assets, not measured draw submissions or frame time. [Full measurements](measurements.json)

## Verification

- Blender 5.0.1 played back both native stacks. The 5 cm run checked 1,040 roof and 2,160 masonry boundary vertices at less than 2 µm position delta. Maximum measured surface UV drift during displacement was below \(5 \times 10^{-7}\) UV units. GLB exports retained node identities, hierarchy, and byte-identical separate collision payloads. Reimport checked evaluated triangle counts and all three UV layers on each modified section.
- The Cottage retained its packed height image, original flat mesh datablock, modifier settings and evaluated geometry through Blender save/reopen. The experiment leaves production regeneration and artist overrides on the existing route. The pilot stack will need explicit semantic replay if it is promoted into the generator.
- The three pure construction-depth regressions and the existing native Blender construction-depth regression passed.
- Unity 6000.5.5f1 Editor imported fresh evaluated assets with 67,015 / 136,829 visual triangles and 5 / 15 colliders. Switching the same Cottage key from baseline to relief was rejected by the existing compatibility guard. The previous import record and its placement GUID survived. The Blender GLB exporter stopped sharing the original field's index accessor and shifted later accessor numbers, which the current static signature includes. No importer or runtime changes were made. Unity player behavior and performance were outside this experiment.
- Adobe Substance Integration Tools 3.1.0 rendered the `height` output of the locally supplied `medieval_wood_shingle_roof.sbsar` at 256 × 256. Blender read the resulting scalar BMP, produced 29.87 mm of peak lift and retained zero measured UV drift with all 1,040 boundary vertices pinned. This tested channel compatibility with the pilot, separate from the same-finish render experiment. The archive and extracted channel remain private local inputs. Source SHA-256 `a2a9f5f75cbffeec5c13b6740eba710f40b78df5cad5507d3d7dbe7742d18e1a`. Rendered height SHA-256 `247c6255d3bfc5c7b8319719fde1a55a7e7e4daac6d5775627790cad277e0c82`.

## Reproduce in the existing checkout

```powershell
Set-Location CODE/Scripts/architectural_generator
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
& $blender -b --factory-startup --python-exit-code 1 --python tests/render_material_relief.py
py tests/compose_material_relief.py
```

The script saves a Cottage preview scene in `dist/material_relief_pilot/roof/relief.blend`. Select the mapped roof field and use **Caelmor Relief Sampling** and **Caelmor Material Height** in Blender's modifier panel. Neither modifier needs to be applied to export the evaluated GLB. Add `-- --metrics-only` to the first command to run the Blender checks and exports without rendering. Original project materials are opened read-only.

Keep eaves, ridges, roof intersections, stone corners, openings and pronounced joints as explicit construction. Use mapped relief across broad fields. The next useful proof is a bounded, close-view surface with a height map authored specifically for low-frequency shape, with the corresponding low-frequency normal contribution reduced. Establish a visible advantage over hybrid geometry at comparable asset cost and a safe same-key update before exposing the option across production buildings.
