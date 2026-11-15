# Caelmor Vegetation Scatter

A Blender 5.0 authoring extension for laying out approved Lowmark vegetation over selected ground meshes. It links the [approved library](../../../MEDIA/Materials/procedurally_generated/Lowmark_Natural_Grass_Wildflowers.blend) with its 93 meshes, shared atlases and placement metadata. Batches contain editable points, with Geometry Nodes instancing the linked specimens. A denser ground layer, fewer tall clumps and sparse blooms let the walking surface read clearly amid patchy growth.

## Install and generate

1. In Blender 5.0.1, open **Edit → Preferences → Get Extensions → Install from Disk** and choose [caelmor_vegetation.zip](dist/caelmor_vegetation.zip).
2. In Object Mode, select the ground meshes. Open the 3D View sidebar with **N** and choose **Caelmor → Vegetation Scatter**. Use terrain modelled with one Blender unit per metre and upward-facing ground normals.
3. Set **Vegetation Library** to the approved `.blend` beside its texture maps. Inside the checked-out project the add-on can discover it from the saved scene path. Keep the source library and maps accessible when reopening a generated scene.
4. Pick a named output layer and a density preset, then click **Generate / Regenerate**. **Candidates per m²** is the sampling rate before habitat, masks and budgets. Species weights of zero disable a family. Shape the mix with **Filler Share**, moisture, clustering and patch size. **Plant Transforms** controls height, scale range, heading, rotation spread and slope alignment.
5. Use unique output layer names for separate planting zones. Regenerate only with each layer's intended ground meshes selected. Set density to zero and generate to clear that layer's generated points. The panel reports generated instances and triangles.

## Habitat and guide inputs

- The sampler uses evaluated world-space terrain. **Maximum Slope** rejects steep faces. **Limit Elevation** bounds the accepted height range. Lower ground and shelter tend to be damper. Each family's moisture preference, path-edge affinity and typical patch density contribute to the mix. Broad patches and smaller gaps vary with the seed and patch size.
- Prepare a paint group on the active ground mesh and use Blender Weight Paint. These names also accept `FLOAT` attributes on the point domain. If a vertex group and a float attribute share a name, the vertex group wins. Weights are interpolated across the triangles.

| Name | Default | Meaning |
| --- | ---: | --- |
| `cv_density` | 1 | Multiplies the local chance of placement |
| `cv_exclude` | 0 | Weight 1 excludes all generated roots from that area |
| `cv_moisture` | 0.5 | Neutral at 0.5, drier below and damper above |
| `cv_verge` | 0 | Adds verge habitat and favors short cover |

- Put unbeveled Blender Curves, edge-only meshes or Grease Pencil strokes in a **Path Guides** collection. The add-on projects their centerlines to world XY and reads the visible drawing at the current frame. Set **Tread Half Width** and **Verge Width** in metres. A guide object can override them with `cv_path_half_width` and `cv_verge_width` float properties. The verge extends outward from the tread edge. The sampler reserves the selected plant's horizontal envelope, including a slope-tilt allowance. This input works with hand-authored guides and gives a future path tool a documented handoff.
- Put simple meshes or curves in **Structure Footprints**. Their oriented bounds projected to XY keep the interior clear. **Wall Clearance** sets the setback, and **Wall Base Width** sets the region available for extra sheltered growth. Use several simple proxies for a concave building or separate wings. A mesh facade with overhangs is a poor footprint proxy for ground-level planting.
- **Verge and Wall Boost** increases the chance of placement along these edges. The painted exclusion, slope and elevation limits take priority.

## Protected edits and budgets

- **Place Protected Plant at Cursor** adds a chosen established specimen at the cursor. **Protect Selected Plants** keeps existing manual meshes editable and reserves space around their roots. Alternatively, assign an existing **Protected Objects** collection. Set `cv_clearance` on an individual object to override its protected radius.
- To keep a generated plant, select its batch in the Outliner, enter Edit Mode, select its point, and use **Pin Selected Points**. This transfers the current transform and LOD to an editable object in the layer's Protected collection. Moving that object keeps its original generated position reserved while the pin exists. Paint `cv_exclude` to suppress generated plants in an area across rebuilds.
- Regeneration replaces the named layer's generated point batches. It retains protected and other hand-added objects. Arbitrary edits to generated points belong in the protected collection if they should persist. Undo is available for the generation and pin operations.
- **LOD Anchor** defaults to the scene camera. With neither, scatter starts at LOD1. At generation, the LOD ranges select an initial mesh. The triangle budget lowers more distant LODs first, then trims generated instances if needed. **Instance Limit** and **Triangle Limit** apply to the generated layer. Protected objects have their own authored costs. Use **Batch Size** to set spatial granularity. These are authoring-time LOD choices, so rebuild after changing the anchor or its ranges.
- **Candidate Limit** bounds the working sample count across large areas. When it is reached the tool spreads its samples across eligible surfaces. Output is deterministic for identical inputs, including terrain names and evaluated topology, seed, masks and LOD anchor. Generate with the same Blender version for exact reproduction.

## Source and verification

The [extension source](caelmor_vegetation) separates habitat sampling from Blender input, instancing and controls. [Native tests](tests/test_scatter.py) cover the actual linked kit, seeds, painted interpolation, slope and elevation, curve and Grease Pencil inputs, rotated footprints, LOD budgets, realized instance selection, and edits across regeneration.

```powershell
blender --background --factory-startup --python-exit-code 1 --python CODE/Scripts/vegetation_scatter/tests/test_scatter.py
blender --background --factory-startup --python-exit-code 1 --python CODE/Scripts/vegetation_scatter/tests/render_review.py -- --optix
blender --factory-startup --command extension build --source-dir CODE/Scripts/vegetation_scatter/caelmor_vegetation --output-filepath CODE/Scripts/vegetation_scatter/dist/caelmor_vegetation.zip
```

The review command uses Blender Cycles. Omit `--optix` for CPU rendering. The Lowmark farmhouse and the 50 × 38 m meadow use matched cameras and lighting across their three densities. Each of the six settings produced the same placement hash on immediate regeneration. The installed ZIP also generated a separate test scene and matched its placement hash after saving and reopening. [Matched density renders](evidence/density_comparison.jpg) · [Farmhouse verge close-up](evidence/farmhouse_verge.jpg) · [Counts and repeat hashes](evidence/counts.csv).

The farmhouse goes from 2,190 to 11,870 instances. Its dense run stays below 820,000 triangles across 19 batches. The meadow goes from 26,679 to 123,744 instances over 72 batches. The dense meadow uses LOD2 throughout under the 2.42 million triangle cap. Each render keeps the tread clear and shows stronger coverage in the sheltered margins and dense patches. The counts describe the triangles represented by the instances. Display performance and Unity runtime remain outside this Blender authoring proof. [Blender extension packaging](https://docs.blender.org/manual/en/5.0/advanced/extensions/getting_started.html)
