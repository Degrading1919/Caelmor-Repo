# Lowmark settlement showcase

[Editable Blender scene](Lowmark_Settlement.blend) · [Settlement overview](Lowmark_Settlement.png) · [Farmhouse](Lowmark_Farmhouse.png) · [Cottage](Lowmark_Cottage.png) · [Workshop](Lowmark_Workshop.png) · [Cottage material close-up](Lowmark_Materials.png).

The main worn lane leads to the established farmhouse. A narrower branch reaches the cottage, and the broader workshop approach leaves room to carry stock. Low fieldstone walls and scrub break up the pasture. Sheltered firewood, threshold stones, and a workbench with seasoning boards distinguish the plots at close range.

| Building | Generated construction | Surface condition in this scene |
| --- | --- | --- |
| Farmhouse | Two-storey L plan, 10.70 × 6.80 m main range, 40° roof | Maintained lime, weathered oak, maintained iron, clear glass |
| Cottage | One-storey 7.60 × 4.85 m rectangle, 49° roof | Aged lime, heavily aged oak, weathered iron, lightly weathered glass |
| Workshop | One-storey 10.65 × 5.55 m range, 34° roof and wide workdoor | Aged lime, maintained joinery, corroded iron, obscured glass |

## Bindings and reproduction

The generator body remains editable by building and floor, with the generated Roof AutoComplete meshes in separate collections. All three roofs use the native registered board layout. The scene applies the later **Riven Bake** albedo, normal and roughness to those roof UVs after generation. The checkout's registered export and generator hash are the inputs for a new Roof AutoComplete build. The Riven Bake scene binding can be inspected independently on the rendered roof geometry.

The PBR bindings use the existing library's Structural Timber, Fieldstone and Stone Only, Lime Plaster, Planked Oak, Forged Iron, Handcrafted Glass, Packed Earth and Worn Footpath exports. Modeled glazing follows the generated apertures and sits behind their native frames. The terrain uses continuous metric surface UVs and a second UV set for the approved path-transition mask across branches. Vegetation Scatter links the 93-mesh approved kit. The same authored walk centerlines and structure footprints guide its planting exclusions. Field boundaries and props are editable scene meshes using these same approved surfaces.

Open the scene from its tracked path in the repository so the relative library and texture links resolve. The five named cameras share the same terrain, buildings, dressing and daylight. The overview is 3000 × 1710. Each building portrait is 2520 × 1720. The detail is 2350 × 1530. [Reproduction script](build_settlement.py) · [Binding and scatter audit](verification.json) · [Approved material library](../../../../../MEDIA/Materials/procedurally_generated/README.md).

```powershell
blender --background --factory-startup --python-exit-code 1 --python CODE/Scripts/architectural_generator/evidence/lowmark_settlement/build_settlement.py -- --optix
```

The script uses Blender 5.0.1. Omit `--optix` for CPU Cycles. `--draft` writes working previews. Use `--from-scene <path-to-blend>` with `--shots Settlement Farmhouse Cottage Workshop Materials` to render specific cameras from a saved scene.

## Verification and visual assessment

The [Unity standalone performance assessment](PERFORMANCE.md) covers the imported buildings, roof variants, scatter and texture settings.

The saved scene reopened in Blender 5.0.1 with its relative image paths resolved. All three native body validations pass. The roofs contain **3,625 modeled shingles** and the scene fits **27 closed panes**. The placement audit found **217,621 ground-cover instances** across 420 batches, including 192 yarrow and 565 selfheal instances. It found zero roots inside the three walk treads or the thirteen building, stair and boundary-wall clearance proxies. Scrub farther back uses the existing Lowmark leaf cutouts attached to scene-authored branch clusters.

- **Bindings.** No visible mesh has a missing material slot or an unresolved texture path. The three Brookoak image hashes match the Riven Bake files. Ridge caps use the approved longitudinal wood surface. Concealed roof-course bedding retains the generator's solid Brookoak tone. Crossbars and door fittings are native modeled parts with the approved iron shader.
- **Contact and framing.** Early renders exposed unsupported farmhouse porch posts, open cottage eave slots, a distant terrain edge and visible texture stripes across the far hills. The scene seats the posts on stone, adds timber behind the fascia, extends the surrounding land and softens the subpixel ground repeat using the approved albedo's average. The camera audit measures the projected building geometry in the final wide and portrait views. The clear walks remain visible through the individual shots.
- **What still reads procedural.** The same dark and light shingle tones recur across long roof slopes. Plaster panel proportions, straight timbers, stair blocks and some window hardware remain very regular in close view. The buildings have exterior craft cues, with limited readable interior occupation. The larger pasture still needs more mature vegetation and finer-grained variation in ground cover, soil and use patterns to read as a lived-in Lowmark setting at professional environment quality.
