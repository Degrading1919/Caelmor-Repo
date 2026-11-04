# Tripo references and a Thornfell masonry study

The reference inputs were the supplied Tripo exports `Fort_Forinthry_watchtower.glb` and `Havenhythe.glb`. Caelmor's art brief is the road approach to a Thornfell pass gate. At the existing seed 91 benchmark camera, the opening and worked stone surround should read first, then the wall courses. This is a controlled studio view, with the camera used as a gameplay distance proxy.

## Observations

| Property | Watchtower | Havenhythe |
| --- | ---: | ---: |
| Indexed vertices / triangles | 167,206 / 272,390 | 172,131 / 295,116 |
| File / embedded image bytes | 10.64 MB / 2.02 MB | 11.42 MB / 2.37 MB |
| Roughness G, median and 5th to 95th percentile | .60 / .35 to .76 | .87 / .84 to .91 |
| Metallic B, median / 95th percentile | .016 / .043 | .008 / .024 |
| Tangent normal tilt, median / 95th percentile | 0.7 / 6.0 degrees | 1.0 / 9.0 degrees |
| Encoded base-color luminance, 5th / 50th / 95th of 255 | 71 / 131 / 163 | 64 / 91 / 179 |

Both files use one indexed triangle primitive, one material, and one shared UV set for three 2048 × 2048 JPEG maps. The files declare no separate occlusion or emission map. The packed map's red channel is near white, and the material does not bind it as occlusion. Low metallic values are compatible with predominantly dielectric surfaces. The small nonzero values in a JPEG do not establish the presence or location of metal. Roughness is a real shader input, with a wider working range in the watchtower. The normal maps are mostly near flat and reinforce some edges. Texture bytes are roughly 19–21% of the files.

UVs spread over almost the entire unit square. The base-color atlases show many packed fragments with different hues, and sampled UV area per unit of mesh area varies about 5.7× and 4.5× from the 5th to 95th percentile. This supports treating them as asset-specific atlases. The normalized bounds are not a reliable metre scale. A mesh count also does not tell us how much of the triangulation was needed for the silhouette.

- **Watchtower.** Cool slate and cool stone are separated by a warm timber band. Its broad lower masonry, pronounced roof flare and projecting upper stage are visible in neutral projections. Those changes in outline and recess need actual geometry. The warm band and cooler envelope already read when sampling base color with lighting disabled.
- **Havenhythe.** The pale central shaft sits between darker base and crown. A red side roof and concentrated green accents break up the otherwise warm wood and pale wall masses. The offsets and projecting trim are visible in neutral projections. Some dark recesses and light edge strokes are visible in base color alone, suggesting painted lighting or contact effects. These cannot be uniquely separated from stock color, weathering, and reconstruction artifacts from these files.
- **Transfer.** Use distinct value groups for structure and openings, then related colors on neighboring pieces. Favor a few support-led changes in thickness or profile for cues that survive neutral shading. Avoid recovering palette values from the references or reproducing their fixed highlights, motifs, or silhouettes. Keep Caelmor's real recesses, atlas roughness and reusable metric normals responsible for their own effects.

## Controlled test

The candidate applies a restrained warm/cool mineral field to existing wall facing. It is sampled in building metres at the center of each connected stone, so the face and bevel share one tint and adjacent pieces can read as related stock. Dressed stone around the passage, quoins, mortar, roofs and iron retain their established roles. The field carries diffuse color only. Existing light, geometry and condition fields supply shadows, roughness and weathering.

The [matched approach and rear views](comparison.png) use the [v0.12 seed 91 control](../diversity_v12/after/manifest.json). The [existing clay view](../diversity_v12/after/91/gatehouse/normal_clay_0.png) serves both treatments because the geometry hash is identical. The warmer and cooler courses are legible in both views, while the passage retains its focal contrast. The first pass pulled too much attention to cool patches on the rear. The delivered pass uses lower chroma. It adds surface character, with the largest visible change on the broad walls. The silhouette and the way the building occupies the road still depend on geometry.

The [comparison record](comparison.json) captures exact settings, camera transforms, source and image hashes, and the focused Blender 5.0.1 GLB check. Only the three wall-facing mesh bindings gained different base-color bytes. The other mapped meshes, normal and roughness/metallic payloads, and texture UV bindings matched the baseline. The reimport verified the affected material's bound images and sampled pixels. The export grew from 16,314,812 to 16,352,616 bytes (about 0.23%) with the same 24 embedded images. Local sample checks passed for deterministic tint, identical tint at the same stone center, and scope. The stock treatment refreshes the generated wall atlas when a Gatehouse is regenerated.

**Pass** for the bounded technical study. **Evidence needed** for production art acceptance and for the effect on another seed. Review the matched views before extending the finish.

## Reuse

First try the same approach on another stone building by mapping local stock to actual masonry roles and testing one approach shot. Tune field scale to several courses so the effect survives at distance. Keep lightness changes smaller than the contrast at the entrance. If the opening or eave reads poorly in clay, test one geometry correction, such as the thickness of a load-bearing projection, before touching the material. For timber and roofs, choose different physical causes such as board stock, shielding or drainage and validate them at the real piece boundaries.

[Measured reference data](reference_statistics.json) comes from GLB headers and memory-mapped accessors, 8,192 sampled triangles and 220,000 area-weighted samples on those triangles per asset. Texture statistics sample the referenced JPEGs at those UVs, and private two-angle point projections compare base color with neutral normal shading. These previews and the supplied assets stayed local. No full reference mesh render or connected-component reconstruction was needed. The approach follows the Caelmor Art Director Support method and [procedural asset baseline](https://github.com/Degrading1919/lessons-learned/pull/3). The [Thornfell dossier](../../../../../LORE/Regions/Caelmor_Region2_ThornfellMarches.md) grounds the stone pass and watchpost context. Mineral color grouping is a reversible art proposal.
