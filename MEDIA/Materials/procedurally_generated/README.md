# Lowmark Brookoak Roof Shingles

An editable Material Maker 1.7 roof-field study for Lowmark. Open `Lowmark_Brookoak_RoofShingles.ptex` and use the Remote Controls node at the left. Revision 76 is the reviewed native MaterialPilot graph.

| Control | Starting value | Effect |
| --- | ---: | --- |
| Course count | 8 | Number of courses in a V repeat |
| Minimum shingle width | 0.115 | Minimum width as a fraction of a U repeat |
| Side / butt edge irregularity | 0.012 / 0.017 | Horizontal joint wander and variation in exposed butt position |
| Riven grain strength | 0.32 | Amount of per-board directional wavelet grain |
| Lap relief | 0.37 | Weight of the down-course height ramp |
| Board color variation | 0.35 | Amount of per-board tone variation before the albedo ramp |
| Weathering scale across / down roof | 12 / 8 | Roughness patch scale and the noise driving the side-edge warp |
| Split strength | 0.28 | Weight of the sparse directional split marks |

Change the main Colorize gradient for regional palettes. The second Colorize gradient controls the roughness range. Keep the course count integral and check U/V repetition after changing controls or seeds.

## Deliverables and checks

- MaterialPilot exported 1024px base color and tangent-space +Y normal as PNG, and linear roughness and height as EXR. The Blender-profile export converts Material Maker depth into physical height, with higher values on raised faces. Actual roughness spans about 0.77–0.92. The normal directions were checked against both height gradients.
- `_iteration.png` shows the early 512px native plane. `_preview.png` is the delivered 1024px native plane. `_repeat.png` is a 2×2 albedo repeat. `_raking_light.png` uses the same four exports on a 2×2 Blender surface with a 3.5 cm height range under angled light.
- The courses and board faces continue across the repeat. The V boundary lies at a course transition, where a stronger lip remains visible under grazing light. The repeat cadence is visible across a large roof field.
- Strict MaterialPilot validation passed with one warning. The bridge catalog omits the native `grad` parameter on Fill to Gradient. That native gradient renders and is present in the source.
- For Unity, use the albedo as sRGB, import the normal via the Normal Map importer, and treat the scalar maps as linear. Smoothness is one minus roughness. The Blender displacement preview is an authoring check. Material binding, displacement support, and the gameplay-distance appearance on a Lowmark roof still need Unity verification.
- The material now has varied butts, wood grain, relief, and splits. Distinct knot whorls, chipped silhouettes, and localized ochre weathering from the reference remain future art work. Creative Director review is pending.

## Reproduction and reference

Use one live graph writer. Inspect the bridge capabilities and current revision, plan the node transaction, apply against the checked revision, and inspect a native 512px preview. Validate all channels, render a 1024px preview, and export only under this directory. MaterialPilot derives its save/export roots from its server working directory. For this pass a directory-scoped session shared the running native bridge while enforcing this directory as the write root.

The attached roof screenshot informed the lap, butt offsets, fiber direction, and weathering. User-supplied visual reference SHA-256 `97fa5c1f652a9e169672f69063a98246e4ac0f482f105b2eab5b31f6cb241929`. Distribution rights for the screenshot are unverified, so it is omitted from the repo and supplies no pixels to the asset. The graph and exports are original Caelmor procedural work. The [Split Oak Shingle working palette](../README.md#split-oak-shingle--recolorable-roof-working-test) is the repo reference for muted oak tones.

## Timber Study review candidate

Open [the editable Timber Study](Lowmark_Brookoak_RoofShingles_TimberStudy.ptex) in Material Maker 1.7. The graph at live revision 101 supersedes the previous candidate at Git commit `430ef65`. The registered roof material above remains available for Roof AutoComplete.

| Diagnosis of previous study | Construction and evidence |
| --- | --- |
| The straight lap gradient and warped perimeter produced smooth broad faces with occasional double ledges. | A stepped board-local growth field now creates broader riven face relief before the finer fibers. The lap ramp is sampled through the same warp parameters as the perimeter. Some doubled borders still show under grazing light. |
| Remapped wavelet fibers looked combed and the knot branch produced isolated pits. | Two native height trials compared a slope-warped knot field and masked directional warp. Both kept artificial closed contours. The rejected branch was removed. Continuous fine fibers now deform with the existing growth field and sample in each board’s local UV. Convincing knot whorls remain open. |
| Shallow scratches were hard to distinguish from grain. | A graded lap mask localizes grain-aligned checks toward exposed ends. Shared height drives normals, and the surface changes also feed albedo and roughness. Narrow checks are visible in close-ups. Open fractures and larger chips remain weak. |

The Remote Controls node exposes riven face relief, growth curvature, end checks, butt chips, board color variation, pale exposed wood, relief-driven roughness, lap relief and normal intensity. The timber and pale wood gradients are editable in Colorize nodes. The board-local cleavage and fiber branches can serve as a wood surface for individual modeled shingles once given local UVs and outputs that omit roof joints and laps. Preserve the eight courses, generator seeds and warp settings for the mapped roof.

- [Matched comparison](Lowmark_Brookoak_RoofShingles_TimberStudy_comparison.jpg) contains the registered material, previous study and this refinement under matched cameras, lighting, physical UV scale and 33 mm displacement range. Views include a neutral sphere, adjacent boards, grazing light and a 6.4 × 3.55 m roof slope.
- [Four channels](Lowmark_Brookoak_RoofShingles_TimberStudy_channels.jpg), [native sphere](Lowmark_Brookoak_RoofShingles_TimberStudy_native.png), [2×2 albedo repeat](Lowmark_Brookoak_RoofShingles_TimberStudy_repeat.jpg) and [knot construction trials](Lowmark_Brookoak_RoofShingles_TimberStudy_construction.jpg). The V boundary falls on a course transition and remains stronger than any individual interior row. U continuity looks good, and board-tone cadence is recognizable over the full roof.
- Native Blender-profile exports are 2048 × 2048. Albedo is sRGB, the tangent normal is +Y, and roughness and height are linear EXRs. Re-export after save matched all four SHA-256 digests. Exported albedo downsampled against its native 1024 preview had a mean absolute RGB error of 0.28/255. Signed normal-to-height-gradient correlations were 0.83 across and 0.95 down the tile. Roughness ranged from about 0.70 to 0.95. Strict graph validation passed with two catalog warnings about gradient parameters present in the native graph.
- Roof AutoComplete still uses 1.28 m U, eight 0.30 m courses per V, the same joints and the exact registered albedo hash. Source comparison confirmed the unchanged registration-node parameters and seeds. In 38 side-joint neighborhoods the measured peak moved by a median of zero and at most two 1024-equivalent pixels. A future approved swap requires the new registered hash and a mixed 50% detail test in Blender, with 0% and 100% controls. The generator and registered maps were preserved.
- Independent critique by Astra High recommended retaining the new fibers because they follow the broader relief without restoring deep combing. The close-up is more fibrous than the previous study. The roof-scale pattern is largely the same. Broad relief can still look rounded, the butts are too clean, and long dark course borders remain. The reference’s splintering, open knots, and tool damage are beyond the current candidate. Full missing corners, lifted splinters, and undercut lips require geometry for a true silhouette. Fine vessels, shallow checks and patina belong in the procedural material. Creative Director visual acceptance and installed add-on or Unity checks with this candidate are pending.

### Method references

The screenshot supplied by the Director, SHA-256 `b24cc8eedfb9bfb535176beec9bcbbf71131b4b2faa13e0643e747e4994673b03`, is a visual benchmark. The sources below informed technique and evaluation. Their artwork and code are excluded from the delivery.

- [Pierre Fleau’s Wood Temples](https://pfleau.artstation.com/projects/6KW0W), [Polycount’s height-first discussion](https://polycount.com/discussion/comment/2779282), and [Dannie Carlone’s sculpting and texturing interview](https://80.lv/articles/combining-zbrush-and-substance-designer-for-games/) informed the separation of primary construction, secondary fracture and fine surface relief.
- [The herringbone artist’s grain breakdown](https://www.reddit.com/r/Substance3D/comments/1xk2aev/material_herringbone_parquet_substance_designer/) and [grain-direction critique](https://www.reddit.com/r/Substance3D/comments/1j6ku3a) informed the common grain field and longitudinal placement. The [3D Wood Material skill](https://github.com/MengTo/Skills/blob/main/agent-skills/3d/3d-wood-material/SKILL.md) and [Three.js procedural materials skill](https://github.com/linegel/threejs-complete-set-of-skill/blob/main/skills/threejs-procedural-materials/SKILL.md) informed the added vessels, shared deformation and board-local coordinates. Those ideas were implemented with native Material Maker nodes.
- [MaterialPilot documentation](https://github.com/SS-360/materialpilot/blob/main/docs/user/installation.md) and [Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) informed revision-checked transactions and bounded independent review. Installed MaterialPilot source was checked at `e3721eadd042e077f3aa7d472ad83c5594c7ea5b`.


## Riven bake review candidate

The [Blender build source](build_brookoak.py) creates a tile from overlapping modeled timber surfaces. Each shingle's taper, cup, twist, beveled shoulders, sidewalls and cut end are generated before baking. The outlines include selective corner breaks. The same board-local growth coordinates drive longitudinal relief, redirected grain around selected knots, tapered checks, smaller fissures, and the shader's fine fibers. Exposure and damage alter reflectance and roughness as well as relief. The bake projects material signals without direct light, cast shadows, or AO in the albedo.

Run from the checkout with Blender 5.0.1:

```powershell
blender --background --factory-startup --python-exit-code 1 --python MEDIA/Materials/procedurally_generated/build_brookoak.py -- --verify-repeat
```

The default is a 2048 × 2048 bake. `--size 768 --mesh-detail 72` is a fast draft. `--bake-only` skips the review images. `--sphere-only` renders the reference-style sphere with actual overlapping shingles. The maps are regenerated directly from the source. The Material Maker Timber Study stays available as the previous editable approach.

- [Modeled timber sphere](Lowmark_Brookoak_RoofShingles_RivenBake_sphere_modeled.png), [displaced baked sphere](Lowmark_Brookoak_RoofShingles_RivenBake_sphere.png), and [paired review](Lowmark_Brookoak_RoofShingles_RivenBake_review.jpg). The review includes a matched close-up of the modeled timber and the flat bake, clay views with opposing side lights, and a 6.4 m roof slope.
- [Albedo](Lowmark_Brookoak_RoofShingles_RivenBake_albedo.png), [tangent-space +Y normal](Lowmark_Brookoak_RoofShingles_RivenBake_normal.png), [linear roughness](Lowmark_Brookoak_RoofShingles_RivenBake_rough.exr), [linear height](Lowmark_Brookoak_RoofShingles_RivenBake_displace.exr), and [2×2 albedo repeat](Lowmark_Brookoak_RoofShingles_RivenBake_repeat.jpg). Height is normalized by 50 mm. Cycles Selected to Active projects onto a plane with `RoofUV`, retaining the 1.28 m × 2.40 m repeat and the registered side-joint centers. Each map matched its repeat bake pixel-for-pixel.
- [Roof AutoComplete comparison](Lowmark_Brookoak_RoofShingles_RivenBake_integration.jpg) shows the same 6 × 4 m test house at 50% modeled detail. Blender generated roofs and bound all three input maps at 0%, 50%, and 100% in an isolated test with the candidate texture stem and hash supplied in memory. The installed registration still rejects the candidate hash. The generator and registered production maps remain intact.
- At close range the modeled ends, knot flow, and irregular checks are more legible than in the Timber Study. The bake approximates the relief when projected onto the flat field. Eave silhouettes and undercut lips require geometry, and modeled boards would benefit from a separate wood-only material to avoid repeating the baked lap shading. The flat texture also exposes periodic board tones across a large roof. This source is a bake fixture without solid underside meshes for use as standalone props. Reference parity and Creative Director acceptance remain open.

Visual benchmark is the user-supplied timber sphere (previously recorded above). No reference pixels are used by the bake. [Fleau’s original project](https://pfleau.artstation.com/projects/6KW0W) and [Blender’s Cycles baking reference](https://docs.blender.org/manual/sl/5.0/render/cycles/baking.html) informed the separation of structure, surface detail and bake.
