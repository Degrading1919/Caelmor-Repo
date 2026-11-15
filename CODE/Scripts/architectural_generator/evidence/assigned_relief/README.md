# Assigned material relief

## Source and material decisions

The source was the Creative Director's private `MEDIA/Materials/working/lowmark/Building_Assets/test_scene.blend`, SHA-256 `911c3d83e5f3ca3a3633619bfa0f3fe2dd7a78407c72926abc082ef0db0f5154`. Blender 5.0.1 inspected it with auto-execution disabled. The three Substance materials use Principled BSDF, a repeating UV-to-Mapping path, and 1024 × 1024 base color, normal, roughness and metallic images. None had a height image, saved Displacement connection, or saved Substance preset values. The original scene and image caches were read-only.

| Scene material | Scene mapping | SBSAR physical-size metadata | Prototype depth span / neutral | Peak displacement |
| --- | --- | --- | --- | ---: |
| Medieval Wood Shingle Roof | 1 UV repeat/m on the generated slope | Unspecified | 35 mm / 0.45 | 15.30 mm |
| Worn Wood Planks | 0.46 UV repeat/m on the enclosure | 173.80 × 173.50 × 1.88 cm | 18.77 mm / 0.80 | 2.77 mm |
| Aged Birch Wood | 1 UV repeat/m on the enclosure | 80 × 80 cm, depth unspecified | 35 mm / 0.50 | 3.63 mm |

The physical repeat follows the shader as authored in Blender. The vertical depth and neutral positions are prototype authoring choices where the source lacks an explicit connected scale. Adobe Substance Integration Tools 3.1.0 baked base color, roughness, metallic, normal and 16-bit height from the corresponding SBSARs at the same 1K resolution and package-default parameter state. The rebaked visible maps differ from the scene's cached images. Using the matched channel set avoids asserting that a height image from one parameter state matches a normal or color image from another. The original cached appearance is included as a separate flat reference in the local review images.

| Local SBSAR | SHA-256 |
| --- | --- |
| `medieval_wood_shingle_roof.sbsar` | `a2a9f5f75cbffeec5c13b6740eba710f40b78df5cad5507d3d7dbe7742d18e1a` |
| `worn_wood_planks.sbsar` | `7952e1340a152df8d03be8147b2b297e6155f7acedfeadf63f7453a60621e13` |
| `aged_birch_wood.sbsar` | `b9056a3c0225995a821141af3d49c516acf19663b7ab9ce304a189ee390f0624` |

Local review files under the source scene's existing `Building_Assets` folder include `material_relief_review.blend`, three *Material Relief* sheets and three *Material Source* sheets. The preview contains the packed test materials and height images, with only the generated review Cottage. The three materials can also be appended individually. Private scene content, SBSARs, rendered texture channels, GLBs, and visual review files are excluded from distribution.

## What ran

- Fixed 8 × 5.8 m Lowmark Cottage, one storey, seed 17. Modeled frame, openings, roof structure, edge geometry, and material assignments were held for matched flat/height pairs. The original cached shader references test the flat fallback through the same generator. All three height tests run from the same mapping as the corresponding albedo, tangent-space normal and roughness.
- Blender 5.0.1 exercised the saved Scene Material finish control, automatic companion detection, relief, remapping to Birch, and save/reopen/regenerate with packed material image references. The measured replay position delta was under 1 µm. The tested boundary vertices stayed within 2 µm and the height UV matched the shading transform within 2 millionths of a UV unit. Native displacement stayed inside the actual image-derived relief bounds.
- Export and GLB reimport kept all four UV layers on displaced sections, 27 visual renderers, and five colliders. Collision GLB bytes matched in all three exports. The 5 cm test went from 8,464 to 130,838 triangles, and the visual GLB from 12.62 to 17.69 MB. This is an authoring validation at one resolution. The roof has shallow, softened geometry at this sampling density, and the near-flat wood grain is primarily visible in close light. [Measurements](measurements.json)
- Eight pure construction-depth/treatment tests and the native construction-depth regression passed. Blender validated the extension archive. Unity 6000.5.5f1 Editor passed 859 same-key update checks, including artist-owned material overrides, scene and prefab references, persistent mesh IDs, incompatible update rejection, fixed collision and repeat import. The existing guided feature suite passed 2,186 checks.

## Reproduce

Bake the 1K matched visible channels and scalar `*_height.png` alongside them. Use a single preset per material. Then run the proof in the designated checkout.

```powershell
$scene = (Resolve-Path 'MEDIA/Materials/working/lowmark/Building_Assets/test_scene.blend').Path
Set-Location CODE/Scripts/architectural_generator
$blender = 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe'
& $blender -b --factory-startup --disable-autoexec --python-exit-code 1 --python tests/test_assigned_relief_blender.py -- $scene dist/assigned_relief/substance_full --render
py tests/compose_assigned_relief.py (Split-Path -Parent $scene)
```

The authored graph subset is one material per mapped semantic section, one UV coordinate basis with an optional constant planar transform, and a supported image extension. The system reports a flat reason for unsupported graphs. Existing sections with mixed slots require a semantic material split before applying relief. Enabling the mode on a previously modeled section can alter the section layout and requires explicit Unity reconciliation. Subdivision density and LOD remain separate work. Validation was in the Unity Editor.
