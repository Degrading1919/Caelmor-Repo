# Crafted Curves 0.11

This pass adds authored curvature to selected world-aware constructions. The **Crafted Curves** control is enabled in new Blender scenes. Loading a building saved before 0.11 restores the option off. Changing the control on an existing building requires full regeneration so the roof, framing, walls, and collision proxies follow the same settings.

## Matched Blender comparisons

| Building | Distant | Gameplay | Close |
| --- | --- | --- | --- |
| Lowmark Smithy | [Distant](comparison/smithy_distant.png) | [Gameplay](comparison/smithy_normal.png) | [Close](comparison/smithy_close.png) |
| Thornfell Gatehouse | [Distant](comparison/gatehouse_distant.png) | [Gameplay](comparison/gatehouse_normal.png) | [Close](comparison/gatehouse_close.png) |

Each sheet pairs v0.10 and v0.11 in clay and material, with two views and two additional material renders from the v0.11 GLB reimport. The old frames come from the [immutable v0.10 capture](../polish_v10/after/manifest.json), revision `ae0ec03`. The [v0.11 manifest](after/manifest.json) records generator revision `f6c2311`, camera transforms, hashes, and complete settings. Both captures used Blender 5.0.1, seed 91, established wealth, standard craftsmanship, age 35, maintenance 0.7, medium detail, and Efficient geometry. [Seed 19](seed_19/manifest.json) repeats the normal front clay and material views on both archetypes with the same studio.

- [Smithy Blender scene](after/smithy.blend), [visual GLB](after/smithy.glb), [collision GLB](after/smithy.collision.glb)
- [Gatehouse Blender scene](after/gatehouse.blend), [visual GLB](after/gatehouse.glb), [collision GLB](after/gatehouse.collision.glb)

## Construction and visual findings

- **Lowmark.** The forge roof sweeps from its existing crown to shallow eaves. The profile holds the crown and wall plates at their established heights, continues the eave slope across the overhang, and stays downhill along each drainage path. Roof skin, deck, gable infill, primary rafters, and bargeboards use the same profile. The stock range keeps its simpler shed roof, so the two construction phases read separately. Tapered cubic knees terminate inside their posts and ties. Seeded differences in roof bow and knee shaping leave the connections fixed.
- **Thornfell.** The elliptical arch rises 0.82 m above its springing, up from 0.60 m. The splayed mouth opens outwards ahead of the wall plane, with shaped springing blocks and a fixed-width throat. One set of seeded voussoir stations defines the aperture, vault and portal courses. The wall and its collision mesh use the same cut. The raised grille clears the taller opening. The straight towers keep their defensive profile.
- **Mire.** Where the existing grammar builds a bowed roof, a chamfered section sweep now joins the established rib stations into individual closed timbers. The reed envelope follows its established profile. The focused tests exercise a Mire Miller in both geometry modes. The comparison gallery concentrates on the two main fixtures.
- **Emberholt.** The option applies no additional curve rules to its angular assemblies. The representative Smithy generates identical geometry with the control on and off.

The first clay and material pilot exposed dark bands at roof breaks that crossed the visible shingle faces. The refined profile places each break under a course butt and uses a single swept bargeboard on each side of each gable. The result reads as a changed silhouette at gameplay distance, and the close view makes the fitted knees legible. A Luna visual review flagged the tan roof area by the stack and the dark mark beside it. The opposite orbit and close GLB show the shingled slope with the chimney casting that shadow. The adjoining shed still has a pronounced edge where it meets the taller roof. The Gatehouse change is strongest at the entrance and subtle in the distant view. Its straight walls and existing projecting wall stubs still dominate the distant read. Production-art acceptance belongs to the Creative Director.

## Measured asset cost

These are matched Blender authoring and exported-file measurements. Embedded image bytes are the sum of the distinct GLB image buffer views.

| Asset | Vertices, v0.10 to v0.11 | Triangles, v0.10 to v0.11 | Objects | Visual GLB bytes, v0.10 to v0.11 | Embedded image bytes, v0.10 to v0.11 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Smithy | 9,320 to 10,824 | 11,704 to 14,236 | 67 | 3,781,076 to 4,238,652 | 1,951,642 to 2,049,074 |
| Gatehouse | 46,432 to 46,116 | 64,562 to 63,980 | 151 | 16,016,336 to 16,046,112 | 6,336,672 to 6,422,353 |

The Smithy adds roughly 22% triangles, concentrated in the swept roof cover, framing, and fascia. The Gatehouse changes the masonry around the opening and retains its object count. Material and atlas generation use the existing pipeline.

## Verification

- Four sweep unit tests check bounds, tapered section centers, manifold outward topology, repeatability, and invalid inputs. Four construction tests exercise seeds 7 and 19 in Solid and Efficient modes, roof drainage and shared seams, timber clearance, actual arch aperture rays, Mire rib stations, and the representative Emberholt control. Six existing architectural tests passed, including exact geometry hashes for all 78 historical control fixtures.
- [Native Blender mesh checks](benchmark_mesh_checks.json) passed on both seed 91 fixtures with zero glazing and structural intersections. The run covered 51 route rays, 32 stair headroom rays, 15 forge exhaust rays, and four gate aperture probes across visual meshes and collision proxies.
- [Native GLB checks](export_validation/export_checks.json) passed for both fixtures, including reimported material pixels and atlas UVs. The Smithy lifecycle fixture also verified save and reopen, scoped regeneration, a retained material override, a protected manual geometry edit, and deterministic atlas maps.
- [Isolated Blender installation](install_check.json) installed the extension archive and generated the Lowmark Smithy using the UI defaults. The gallery was composed only after checking image hashes and matching before/after camera transforms.

## References and workflow

The approved Caelmor regional dossiers govern the setting. The roof and portal forms here are art interpretations of Lowmark's working vernacular and Thornfell's stone pass defenses. The Fort Forinthry reference set informed how a roof edge can carry silhouette and how a deeply framed opening can organize the facade. It included supplied photos 1, 2, 3 and 5, as well as the production and environment portfolios. [Neil Richards' Fort Forinthry production sheets](https://zephusees.artstation.com/projects/PXaxR1), [Anouk Debruyne's Fort Forinthry environment art](https://anoukdebruyne.artstation.com/projects/Xg3P93), [Fort Forinthry building context](https://runescape.wiki/w/Fort_Forinthry)

The timber helper uses a bounded planar cross-section sweep, akin to the profile-and-path model documented by Blender. The roof uses a monotone quadratic sampled at its construction joints, the knees use endpoint-constrained cubic samples, and the arch uses an elliptical intrados and correlated joint spacing. These were chosen so the same positions can be tested and built into editable meshes. The reviewed projects provided comparisons for separating layout from construction, parametric arch components, and editable fortification profiles. This pass uses original generator code and geometry, with no imported assets or third-party code. [Blender procedural curves](https://code.blender.org/2021/09/procedural-curves-in-3-0-and-beyond/), [Blender Curve to Mesh](https://docs.blender.org/manual/en/5.4/modeling/geometry_nodes/curve/operations/curve_to_mesh.html), [BlenderLevelArchitect](https://github.com/dottyboy/BlenderLevelArchitect), [Parametric Arch Generator](https://github.com/Aniruddhyagoswami/arch_generator), [Procedural fortification model](https://github.com/FilipOndre/3D-parametric-model-fortifcation-)

The adaptive checks followed the procedural asset baseline. Cheap geometry checks and four first-pass renders identified the roof-course defect before export validation and the full comparison capture. Luna High supplied the bounded sweep helper, focused regression tests, and independent visual review. Integration checked the returned mesh topology and re-ran the regressions against the final profile. [Procedural asset case and baseline](https://github.com/Degrading1919/lessons-learned/pull/3)
