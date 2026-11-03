# Construction-quality comparison — 0.7

Generated from source **c9bc152** in PR #85 with Blender **5.0.1**. All 16
function/region configurations are supported and rendered; none were substituted.
The Creative Director's artistic acceptance is pending.

| Function | Four-region clay/material comparison |
|---|---|
| Smithy | [Contact sheet](contact_sheets/smithy.png) · [individual images](individual/smithy) |
| Market Hall | [Contact sheet](contact_sheets/market_hall.png) · [individual images](individual/market_hall) |
| Stable | [Contact sheet](contact_sheets/stable.png) · [individual images](individual/stable) |
| Gatehouse | [Contact sheet](contact_sheets/gatehouse.png) · [individual images](individual/gatehouse) |

Each 4316 × 3080 sheet compares Lowmark, Thornfell, Mire and Emberholt in columns;
rows are clay front, clay rear, material front and material rear. The 64 individual
PNGs are 1024 × 704. Seed 91, ESTABLISHED wealth, STANDARD craftsmanship, age 35,
maintenance .7, MEDIUM detail, EFFICIENT geometry, world/grammar enabled and AUTO
context are fixed. Two opposing camera directions and the original studio are
retained. Orthographic scale is fitted across all four regions of each function,
so changed bounds may change scale relative to 0.6; different functions are not
rendered at a common metric scale. Clay/material pairs share the same native mesh,
camera and framing. Exact settings, cameras, geometry/source/image hashes and
generation/validation records are in [manifests](manifests).

## Diagnosis and changes

The [controlled two-case study](../function_v07_diagnosis/comparison.png) holds
geometry constant while changing light or camera elevation separately. It showed
that presentation revealed relief but did not resolve primitive forms. It does
not isolate individual shader effects. Production materials and the final studio
remain unchanged, so the new comparison exposes the geometry changes.

- Smithies have shaped anvils and wedge bellows/nozzles, open quench/fuel bins,
  and construction around the hot working bay. Existing hood/duct/stack air paths
  are preserved. Sloping rear-wall infill is now mitred over its complete
  thickness; the former approximately 9cm roof penetration is covered by a
  negative regression using a real wall corner.
- Markets allocate customer-facing counters, seller pockets and stock shelves
  alongside the public aisle. Lowmark/Thornfell ridge axes now follow the aisle,
  with open kingpost end trusses, diagonal struts and a ridge purlin. Mire keeps
  its crowned raised roof and reserves a usable 1.35m quay cross-aisle before
  placing stalls. Emberholt retains a heavy mineral-roofed arcade.
- Stables have rail/stile/braced gates, hollow mangers, profiled feeding racks,
  braced bearing bents in the timber regions and a framed hay-service opening.
  Capacity, animal-width entries and supported approaches are retained.
- Gatehouses have near-square flanking towers around a narrower core, deep
  two-face supported portals, radial masonry voussoirs, gate guides/hinges and
  battered stone buttresses in Thornfell/Emberholt. Emberholt has a supported
  corbel crown. Mire retains its offset piled watchbank and now has a real side
  door, supported landing and matching rail opening. This is not a new general
  interior or complete defense simulation.

Earlier [0.6 comparison sheets](../function_v06/README.md) and small intermediate
pilots are retained separately. No historical 80-building gallery was regenerated.
Geometry and new code remain original under GPL-3.0-or-later; existing notices
and reference/inference boundaries are preserved.

## Executed verification

- **28 Python methods passed:** 12 work-program, 8 yard-program and 8 shared
  integration methods. Coverage includes deterministic replay, actual geometry,
  public width/fixture clearance, doorway semantics, full portal-head sections,
  wall/structure roof envelopes and unchanged hashes for the other 64 historical
  configurations (16 functions × 4 regions).
- **16 native Blender configurations passed:** 1,056 circulation rays including
  near-ceiling samples, 128 stair-headroom rays, 60 exhaust-path rays, and zero
  glazing intersections with structural or integral functional fixtures.
  Collision wall/floor proxies count. Operable door leaves are omitted from
  circulation probes; this is not a claim that closed doors are traversable.
- The existing Blender backend test passed operator generation, protection and
  scoped/full regeneration, export/import, and saved-file reopening.
- The final ZIP was installed/enabled in isolated Blender profiles. User-facing
  Generate/Export passed for Emberholt Smithy in EFFICIENT/world mode; legacy
  Farmhouse generation also passed. Archive SHA-256:
  `9572f2d159c4de13bddf47b88a1370183c7b040f30cfa18858da204c0ddefef1`.
- Gallery verification passed all 64 image hashes/dimensions, four composed
  sheets, settings/cameras, current source fingerprints, matching native geometry
  gate records and all 25 archive members. The old 320-image/20-sheet baseline
  also matches its retained hashes.

See [verification.json](verification.json), [verification_tests.json](verification_tests.json),
the two `mesh_checks_*.json` files and installation reports. The latter test
record preserves actual command/results and log digests; timings are individual
test durations, not a performance benchmark or a model-cost measurement.

## Geometry cost and remaining art limitations

Matched authoring triangle counts, **summed over four regions**:

| Function | 0.6 triangles | 0.7 triangles |
|---|---:|---:|
| Smithy | 31,184 | 32,324 |
| Market Hall | 55,198 | 57,541 |
| Stable | 48,175 | 52,351 |
| Gatehouse | 158,718 | 147,158 |

[Geometry diagnostics](geometry_diagnostics.json) include per-configuration
vertices, triangles and objects. Finer semantic components increase object count,
especially for stable joinery; lower total triangle count does not imply better
runtime performance. No target-engine benchmark or arbitrary polygon limit was
introduced.

Root and an independent Luna High image reviewer inspected all four sheets. No
definite blocking penetration or obstructed entrance was identified. The reviewer
found the workfronts, selling bays, stalls and defended threshold clearer, but
the market's central aisle is still inferred from the exterior corner views.
This is bounded image evidence, not final art approval or a recognition study.

Broad roof planes and rear walls remain restrained; Mire roof repetition and
Emberholt's austere slab surfaces are still visible. Small equipment and joinery
are difficult to judge at sheet scale. The forge is unlit, stalls and shelves
are unstocked, and materials remain relatively uniform. These examples cover one
investment/condition setting; this pass does not establish broad socioeconomic
or seed-range artistic acceptance. Existing protected edits survive but may
require artist reconciliation with changed construction layouts. Runtime use,
structural/thermal engineering and terrain fit are outside this verification.

The useful workflow lesson is that a center ray can pass through a window and
that a narrow empty strip can pass collision checks. Require semantic doorway
and usable-width constraints before expensive final evidence. Bounded Luna High
implementation was useful with root integration and native/visual review; no
measured token, allowance or API-dollar saving, or universal model advantage,
is established. Final production-art decisions remain with the Creative Director.
