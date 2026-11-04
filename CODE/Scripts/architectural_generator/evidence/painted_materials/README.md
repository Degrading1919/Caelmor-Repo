# Production texture study and procedural pigment tests

[Matched approach views](comparison.png) · [Settings, original frames and Blender verification](manifest.json)

The studio views use seed 91 and the established gameplay camera proxy. The Lowmark Smithy's working frontage should read through its timber framing. The Thornfell Gatehouse should keep the passage as its main visual cue and let the wall courses read second. These are material proposals grounded in the existing architecture and the [Lowmark](../../../../../LORE/Regions/Caelmor_Region1_LowmarkVale.md) and [Thornfell](../../../../../LORE/Regions/Caelmor_Region2_ThornfellMarches.md) dossiers.

## What the reference files show

I inspected GLB headers for two Workshop stages, the rear gate and wall, and two Townhall stages. I sampled indexed faces from three files and inspected representative maps from ten material folders. The sampled files declare 7,042 to 24,645 indexed triangles per file across several material primitives. These are individual exported stage files, so the counts are neither a combined scene budget nor a one-to-one comparison with the Tripo meshes. Workshop framing, wall boards, trim, and slate recur as separate material assignments. Townhall also uses plaster, glazing, and distinct wall finishes. In sampled surfaces with vertex color, the sampled colors were white. The painted colors are already visible in the diffuse files.

| Evidence | What to transfer |
| --- | --- |
| The 512 px framing diffuse arranges grain, pale cut faces, and worn sections as distinct regions. The 256 px wall boards use long vertical tonal breaks. Mean adjacent luminance changes about 7.8 times more across the boards than along them in that diffuse image. Indexed UVs for the Workshop boards and slate also run beyond the unit square. | Use direction and scale for each construction role. Separate structural framing, boards and end faces where it serves the read. Leave grain orientation in the UV or member frame. |
| Wall V2, V3, and dirty V2 reuse the exact same packed normal. Clean V2 and V3 also share the compound map while their diffuse differs. Trim has its own profile and a narrow light/dark treatment. Some broad plaster and wall faces span much of a tile in a single triangle. | Separate stock, condition, and physical relief. Use broad pigment and selective edges on actual stone faces. Put large silhouette changes, recesses, and projecting trim in geometry. |
| Slate has grouped cool tones and bright course lips. Plaster is quieter and more diffuse in direction. Door and glass textures localize trim, hardware and pane patterns. Glass in the sampled Townhall binds alpha masking. | Give each assembly a distinct value and stroke scale. Use accents where they explain overlap, handling, or material transitions. Keep infill quiet so the structure reads. |
| Raw sampled normals store varying data in green and alpha, with red and blue zero. In the sampled Workshop export, glTF normal red follows raw green closely, glTF green equals inverted raw alpha, and blue varies with reconstructed relief. Sampled compound green maps to glTF roughness, and raw red maps to metallic blue in the inspected export. Some exported emissive slots point at black maps. | Verify conversion against bindings and pixels. Treat these findings as evidence about the supplied extraction, with no inference that the game uses the same shader or that every compound channel has the same purpose. |

The diffuse maps carry warm/cool pigmentation and painted edge light or recess darkening before a renderer adds light. A single diffuse image cannot establish which marks represent ambient shading, stock, wear, or artistic emphasis. The prior [Tripo study](../masonry_stock/README.md) showed a related division between geometry and color. The production files add stronger evidence for reusable tiled materials, direction, and diffuse variants that share relief.

## Caelmor experiment

Caelmor already bakes metric grain and knots, stone microdetail, roughness and material history into packed textures. It already separates dressed stone from wall facing and groups masonry stock with related colors. The two candidates keep those layers and add only broad diffuse pigment through the existing bake.

- **Smithy timber.** The primary bent, knees, stock bents, and timber verge use broad ribbons aligned to the metric chart's long edge. The prepared wood shifts toward honey tones while a smaller dark band follows the same grain. Narrow longitudinal faces get a bounded arris accent. On the approach, the front tie and verge read more clearly against the darker infill. The effect is small on faces in deep shadow. The roof covering keeps its own material.
- **Gatehouse masonry.** The previous mineral stock field stays in place. Broad directional deposits add variation within the face. A second mask uses the orientation of actual upper bevels to carry a restrained accent. It does not draw a new mortar grid. The contrast is clearest on the side wall and less obvious on the front. The dressed portal stays the focal point.

The change is visible in the matched views, but the overall forms and silhouette still dominate the read. These masks work at the selected benchmark scale. Wide rollout needs another seed and a glance at bevels and grain near the close camera, especially on curved members where each face chart uses a local frame.

## Verification and next step

The comparison reused the v0.12 Smithy and v0.12.1 Gatehouse controls. Blender 5.0.1 captured one new pair of views per building with matching settings, camera, and lighting. Both geometry hashes matched. The GLB checks compared normal and roughness/metallic PNG bytes and texture UV bindings against both baseline files, then sampled reimported material pixels. The Smithy reuses one timber atlas bank, so 19 mesh bindings refer to the updated bank even though the color field is limited to selected charts. The Gatehouse change reached three wall-facing meshes. Image counts stayed at 35 and 24. GLB size changed from 4,156,292 to 4,262,100 bytes for the Smithy and 16,352,616 to 16,508,572 bytes for the Gatehouse. Small local checks verified deterministic pigment and the timber and stone edge responses.

**Pass** for this bounded technical study. **Evidence needed** for art acceptance and use across other buildings. Review the matched views, then try a second seed per family. Carry the method to other regions through their own substrate and construction roles. Reserve more elaborate brush shapes for a cue that still fails at the intended distance.

The work followed the Caelmor Art Director Support method and [procedural asset baseline](https://github.com/Degrading1919/lessons-learned/pull/3). Header reads and sampled arrays supplied the reference evidence. All reference images, meshes, private previews and extracted textures stayed local. The published comparison contains Caelmor output.
