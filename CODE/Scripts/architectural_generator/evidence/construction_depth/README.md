# Construction depth study

Blender 5.0.1, seed 91, medium detail, Efficient geometry. Each fixture
holds its construction choices, camera, studio lights, and underlying work
program fixed. The Smithy changes roof cover representation only. The
Gatehouse changes exposed masonry wall representation only. The
[manifest](manifest.json) records exact settings, source and image hashes,
layer metrics and every exported texture resolution.

- [Lowmark Smithy roof comparison](smithy_depth.jpg)
- [Thornfell Gatehouse masonry comparison](gatehouse_depth.jpg)
- Native hybrid versus exported and reimported GLB for the [Smithy](smithy_glb.jpg) and [Gatehouse](gatehouse_glb.jpg)
- [Isolated extension install record](install.json)

## Measured cost

Geometry counts are generator vertices and triangulated faces. Roof and
walls are source layers. Foundation, openings, structure and details
contribute to the totals separately.

| Fixture | Mode | Total triangles | Total vertices | Roof triangles / vertices | Wall triangles / vertices |
| --- | --- | ---: | ---: | ---: | ---: |
| Smithy | Modeled | 15,731 | 12,121 | 5,537 / 5,887 | 1,258 / 1,000 |
| Smithy | Hybrid | 13,999 | 9,549 | 3,805 / 3,315 | 1,258 / 1,000 |
| Smithy | Texture dominant | 13,457 | 8,767 | 3,263 / 2,533 | 1,258 / 1,000 |
| Gatehouse | Modeled | 73,870 | 53,042 | 11,926 / 13,026 | 37,456 / 25,676 |
| Gatehouse | Hybrid | 52,025 | 38,481 | 11,926 / 13,026 | 15,611 / 11,115 |
| Gatehouse | Texture dominant | 38,925 | 29,409 | 11,926 / 13,026 | 2,511 / 2,043 |

| Fixture | Mode | Materials | Texture entries / unique images | Mipped RGBA8 estimate | GLB size | Mesh primitives | GLB vertex records |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Smithy | Modeled | 13 | 39 / 32 | 35.51 MiB | 5.06 MiB | 77 | 30,835 |
| Smithy | Hybrid | 14 | 42 / 35 | 37.39 MiB | 4.90 MiB | 77 | 27,413 |
| Smithy | Texture dominant | 14 | 42 / 35 | 37.23 MiB | 4.81 MiB | 77 | 26,351 |
| Gatehouse | Modeled | 11 | 30 / 24 | 81.10 MiB | 17.38 MiB | 155 | 148,436 |
| Gatehouse | Hybrid | 12 | 33 / 27 | 76.48 MiB | 13.84 MiB | 158 | 105,333 |
| Gatehouse | Texture dominant | 11 | 30 / 25 | 72.32 MiB | 11.65 MiB | 155 | 79,911 |

The estimate sums the pixels in each exported image and its full mip chain
at four bytes per pixel. Runtime compression, residency and renderer
allocations will change actual GPU memory. The largest existing atlas by
area was 4096 × 648 on the Smithy and 2048 × 2856 on the Gatehouse in all
three modes. Each repeated construction set uses 512 × 512 albedo and
normal plus 256 × 256 packed ORM. One mipped set is 3 MiB in the estimate.
Compatible zones share the same set, and palettes can reuse normal and ORM.
Separate standalone GLBs each carry their own embedded images.

The primitive counts are glTF submission candidates before runtime
batching, instancing, culling or multipass rendering. Hybrid adds three
Gatehouse primitives and leaves the Smithy count unchanged. No fixture
export used blended primitives. The measurements cover asset structure
and size. Runtime draw calls, frame time and hardware memory were outside
the study.

## Visual findings and recommendation

**Keep individually modeled roofs for the Smithy and other close assets.**
Hybrid saves 31% of Smithy roof-layer triangles and 11% of the whole
building. It adds 1.88 MiB to the estimated texture footprint and changes
GLB size by only 0.16 MiB. The field recovers shingle rhythm at normal
distance. At close range its repeated pattern and border against retained
tile geometry are visible. The texture-dominant mode removes more actual
course shadows for little additional whole-asset savings. Roof caps,
flashings, eaves, verges and distinctive clay silhouettes should remain
geometry. If a far roof representation is needed, it should align mapped
courses to physical boundaries before replacing the existing close roof.

**Hybrid is a useful option for broad Gatehouse wall fields at normal
distance.** It saves 58% of wall-layer triangles, 30% of all triangles,
and 3.54 MiB of exported size. Estimated texture memory also falls by
4.62 MiB. Staggered joints, stock pigmentation and stone-face relief read
in the normal material view. Close inspection reveals the flatter face
and imperfect alignment where modeled headers meet the repeating courses.
Keep modeled depth for close masonry and retain corners, portal rings,
dressed trim, footings, prominent headers and the bonded curtain returns
as physical geometry. Texture dominant is a candidate for distant opaque
wall fields where its flatter appearance is acceptable.

## Verification

- Both fixtures were rendered in clay and material at normal and close
  distances for all three modes. All six configurations exported to GLB.
  Both hybrid GLBs were reimported and rendered at the native camera.
  Export checks confirmed embedded PBR bindings and repeating samplers
  on the mapped fields. Reimport retained the field appearance.
- Three depth tests passed for deterministic geometry, reduced geometry,
  fixed functional programs, passage rays, roof stock selection, finish
  independence and incompatible requests.
- The Blender depth test passed registered controls and saved settings,
  shared roof field materials, all three cover families, named and manual
  artist overrides, UV layers, and rejection of a representation switch
  over a protected edit. The old edit was retained.
- The construction library, treatments and architectural benchmark suites
  passed, including 78 historical modeled hashes. The packaged extension
  installed into isolated Blender preferences and generated the Smithy.

The benchmark uses original Caelmor maps and geometry. Fort Forinthry
informed the question of where geometry earns its cost. Its extracted
assets are absent from this evidence.
