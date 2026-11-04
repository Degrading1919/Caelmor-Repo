# Construction library vertical slice

The same procedural planners reserve the Smithy workfront and Stable stall
and handling routes before the enclosing and bearing assemblies are built.
The selectors in the Blender panel author the existing role override maps.
The assemblies below were generated in Blender 5.0.1. The
[manifest](manifest.json) records seed, settings, camera, geometry and image
hashes. The historical comparisons use the matched studio views from
`67cba19`. The original evidence remains in its previous location.

- [Smithy workfront before and after](smithy_workfront.jpg)
- [Three Smithy construction combinations in clay and material](smithy_library.jpg)
- Stable reuse in [clay](render_slate/stable/normal_clay_0.png) and [material](render_slate/stable/normal_material_0.png)
- [Thornfell curtain before and after](gatehouse_bonding.jpg)
- [Isolated extension install record](install.json)

| Fixture | Foundation, support, enclosure and cover | Triangles |
| --- | --- | ---: |
| Smithy | Broken-course stone, hewn timber, board and batten, split shingles | 15,731 |
| Smithy | Level-coursed stone, squared timber, lime render, slate | 15,309 |
| Smithy | Dressed stone, hewn timber, earthen render, shaped clay tile | 16,996 |
| Stable | Level-coursed stone, squared timber, lime render, slate | 15,402 |
| Gatehouse | Two-faced curtaining with shallower beds and through headers | 73,870 |

## Visual review

The raised firebed and lower side cheeks expose the charcoal bed from the
approach. The ash opening sits between bearing piers, the hood mouth leaves
a readable gap, and the adjacent anvil and separate stock shelter show the
work sequence. The board seams and shaped clay pans carry the clearest
assembly differences in clay at normal distance. Fine slate edge relief,
plinth beds and timber shoulders read more clearly in the detail frames.
Material review caught a benchmark palette that was overriding the chosen
roof stock. That binding was corrected before the final captures.

The Gatehouse returns have narrower worked arrises, shallower relief in
the field and continuous bearing behind both faces. Full-depth headers
connect both faces at staggered positions. The plain terminal planes remain
site interfaces. The Stable keeps its long frontage, repeated handling
bays and hay route while reusing the frame, infill and slate assembly.

## Verification and boundaries

- `test_construction_library.py` checked deterministic geometry and stable
  route bounds across all three combinations on both functions, sight rays
  from the Smithy approach to the firebed, override precedence and clear
  rejection of unsupported variants.
- `test_construction_treatments.py` and `test_functional_integration.py`
  exercised the treatment roles, two geometry modes, apertures and
  passage, specialized roof meshes, functional layouts and legacy geometry.
  `test_architectural_benchmarks.py` also passed with 78 historical hashes.
- `test_construction_library_blender.py` exercised the registered selectors,
  an artist material, generation and loading operators, and GLB export and
  reimport. The selected Smithy imported 76 meshes with 12 mapped materials.
- `test_construction_blender.py` passed protected edits, manual slot
  overrides, collision equality, aperture BVH, UVs and GLB reimport for
  the Gatehouse. The distributable passed an isolated Blender install and
  Smithy generation.

The slice configures supported construction roles. Specialized pieces such
as Stable stall partitions and regional reed or iron roofing retain their
own builders. Metal framing remains a proposed treatment and is outside
the selectable library. The evidence is an offline architectural review
with one rendered seed per fixture. Production art acceptance remains
with the Creative Director.
