# v0.6 function-first implementation and verification

Generator sources: `905e97b`, scoped forge/access correction `1286d07`, and
physical exhaust connections/clearance in `8c76e5f`.
Blender 5.0.1; pure tests used Python 3.13. No Unity, C#, runtime benchmark,
gameplay/content/canon changes or merge. Final art acceptance is the Creative
Director's. [Construction contract and precedents](../FUNCTIONAL_PROGRAMS.md).

## Actual capability

World mode routes four purposes through shared spatial primitives before applying
regional shells. Other sixteen functions retain their regional builders; legacy
manual/grammar generation remains available. No settings fields were removed.

- **Smithy:** open hot-work bays, masonry firebed/curbs, sloped open-bottom hood,
  hollow side duct and roof-external masonry flue, horn anvil/stump, bellows,
  quench/fuel areas and separate operator/material routes. Lowmark uses a shallow
  monopitch work shelter; Thornfell a shallow stone/slate wind shelter; Mire a
  raised fireproof workbank/approach; Emberholt an industrial arcade and slag/ingot
  handling area. Material lanes respect finished wall thickness and thresholds.
- **Market Hall:** repeated vendor/counter bays, vendor standing space and a real
  public through-aisle. Lowmark timber through-hall and Thornfell wind-protected
  side walls have public entry/exit ramps; Mire has a supported trading quay and
  long raised approach; Emberholt a stone court and iron trading surfaces.
- **Stable:** approximately 2.9 m stall bays, low divided fronts with 1.4 m entry
  gaps, mangers/hay racks, separate hay storage, handling apron and front/rear
  access. Capacity follows investment/craft/seed. Lowmark adds a hay loft,
  Thornfell stone knee walls/dividers, Mire supported ramps/raised service floor,
  Emberholt a working-yard interface. No animal assets are used as labels.
- **Gatehouse:** validated aligned passage, taller flanking watchtowers, actual
  stair flights/stringers and stairwell openings, guard floors/landings, raised
  grille, parked gate leaves and threshold approaches. Party faces are blind.
  Regional gabled/timber, stone/slate and volcanic terraces remain; Mire offsets
  a watchbank and adds a supported link. This is selected functional space,
  not a complete enterable interior or simulated defense system.

Stable IDs/protection, editable meshes, scoped regeneration, source settings and
GLB/sidecar export remain. Sidecars include the functional program and object
functional roles. New functional collision proxies leave open sides and actual
passage/opening cuts; they remain approximate, not runtime traversal proof.

## Failures that changed the implementation

1. Initial mock-backed worker tests passed while real construction failed:
   fixture calls passed role strings in the Mass argument. Independent actual
   `generate`/`validate` caught the interface error. Real construction tests were
   added; mocks are no longer the only integration evidence.
2. Source review found that access-reservation metadata on a closed edge did not
   cut a wall. Smithy/market fronts were opened in actual geometry, with bearing
   supports placed outside reserved approaches. No validator exemption was added.
3. The first Lowmark clay forge still read as an open barn: the roof/bent framing
   hid its apparatus. A front flue then obscured the hearth. The shallow working
   roof, forward hot bay, open framing reservation and side flue corrected those
   specific visibility failures. Only that pilot was rerendered during revision.
4. First native work-space probes found five wall intrusions: three Smithy
   material lanes entered closed wall thickness; Thornfell/Emberholt market
   seller stands reached into side walls. Layouts now use actual finished-wall
   bounds plus working clearance. Semantic fixture/route bounds alone had not
   detected those wall collisions; Blender BVH probes did.
5. Independent structural inspection found three Thornfell arcade capitals
   exposed about 0.0216 m above steep weather planes. Capitals now use their
   complete section's local weather height. A new stone-structure roof gate and
   deliberately invalid regression preserve this correction alongside timber
   roof safety.
6. Independent final-sheet review rejected the still-hidden Thornfell forge.
   The shallower stone hall, forward hearth/hood and taller exterior flue expose
   its work process. Loading/public ramp and stock-lane corrections accompanied
   the affected profiles. Old Thornfell views remain as rejected evidence.
7. Final source review found that a hollow shaft still had an uncut inlet wall,
   a bottom plate blocked the hood throat, and the original horizontal turn
   crossed the hood's side. The stack now has a real inlet aperture and the
   hood has an open reducer/neck/elbow into the duct. Regional neck heights clear
   the load-bearing wall plates. A permanent firebed-to-neck/duct/stack regression
   and sixty actual Blender air-path probes check the opening at center and
   ±75 mm offsets. These are geometric connections, not a draft/thermal model.

These are session-observed failures/corrections; original failed command stdout
was not retained as a separate immutable log. Initial working-tree pilots retain
their settings/source hashes, not a falsely claimed committed source snapshot.

## Executed checks

| Gate | Executed result and scope |
|---|---|
| Python integration milestone | 71 methods passed in 132.087 s: 37 retained legacy, 7 rural, 3 Emberholt household, 5 investment/roof, 1 open-work access, 1 stone craft, 9 work-program and 8 yard-program tests. This preceded the final scoped forge/access revision. |
| Shared functional regressions | Five methods passed separately: all 16 region/function programs validate/reproduce; an actual counter blocking a declared public route is rejected; stone above a weather roof is rejected; all 64 recorded configurations for the other sixteen functions retain their v0.5 geometry hashes; and all four forge exhausts have open firebed/hood, duct and stack paths. The last method passed after the exhaust correction (0.877 s). |
| Boundary coverage | 32 combinations across the four functions/regions, MODEST/ROUGH/LOW/SOLID and AFFLUENT/FINE/HIGH/EFFICIENT, seed 29, age 110/upkeep .3 passed. The ten affected extreme combinations were checked again after the forge/access revision. Eight Smithy extremes additionally passed validation and all three exhaust segments after the final connection correction. Reports retain source fingerprints. |
| Retained Blender regressions | Seven methods across `test_blender`, `test_roof_clearance`, `test_glass_timber_bvh`, `test_profiles_blender`, `test_world_blender` passed. Includes 21 roof fixtures, actual glass/frame checks, settings migration/material banks, protected regeneration, save/reopen and GLB export. Individual module durations were 21.753, 157.937, 20.168, 13.202 and 17.499 s; these are workload timings, not model speed or runtime benchmarks. |
| New actual Blender geometry | Sixteen configurations covered in two eight-case reports. Final checks total 1,050 circulation/proxy rays, 128 stair-headroom rays and 60 exhaust-path rays, plus glass/structure BVH checks. Yard cases passed in 19.715 s. After the final exhaust correction, the eight work cases passed again in 15.848 s, and ten focused work Python tests passed in 2.800 s. |
| Native package | Final ZIP installed/enabled in isolated Blender preferences; real UI operators generated and exported an EFFICIENT Emberholt Smithy with a functional program. A separate install generated legacy Lowmark Farmhouse. Both reports identify the same archive SHA256 below. |
| Evidence consistency | 16 configurations, 64 individual images and 4 sheets verified; all sixteen native mesh-gate geometry hashes match render records. Source/settings/camera/image/archive checks passed. The old 320 images and 20 sheets match their original manifests and were not rerendered. |

Closed operable service-door leaves/straps are excluded from circulation probes;
walls, frames, integral fixtures and collision proxies are included. Stair routes
are tested with actual upward headroom rays, not treated as empty flat corridors.
BVH/ray probes and analytic weather planes are targeted checks, not exhaustive
solid CAD intersection, thermal engineering, structural load analysis or gameplay.

Yard native checks preceded the shared capital change, which affected only
Thornfell Smithy/Market Hall. Their exact final geometry hashes still match the
tested meshes; the report retains both source snapshots rather than claiming
every native test ran from byte-identical final source.

## Controlled visual evidence

[Four function sheets and individual images](../evidence/function_v06/README.md)
cover four regions × four purposes, fixed seed 91, ESTABLISHED, STANDARD, age 35,
maintenance .7, MEDIUM/EFFICIENT, World/grammar on and AUTO context. Each has
two opposed views in clay/materials, common orthographic scale within a function.
Different functions are independently framed. The initial four representative
pilots and focused rejected Smithy views are separate from the final comparisons.

The forge/access revision refreshed only five configurations / twenty images.
The final exhaust correction refreshed the four smithies / sixteen images;
twelve configurations / forty-eight images were retained on that pass, including
their original source and camera snapshots. The verifier replayed those twelve
geometries against current source; material/studio source is unchanged. Original
rendered revisions `905e97b`, `1286d07` and `8c76e5f` remain recorded per
configuration. Matching geometry does not claim pixel identity across versions.

The lead inspected Stable/Gatehouse sheets, the representative pilots and the
revised Thornfell forge. Independent Luna High review inspected Smithy/Market
Hall sheets, identified the Thornfell visibility blocker, then checked the two
corrected Thornfell front views against the rejected view. It confirmed visible
hearth, hood, side flue and anvil; it still found the hood-to-flue connection
visually suggested rather than fully legible. This is bounded visual review,
not an accuracy study or Creative Director art approval.

## Native artifact and limits

Final archive: `dist/caelmor_architecture.zip`, 25 members, all byte-equal to local
source/bundled documents. SHA256:
`16acce0519d8c38225c18b40674658af5dad0ae59d74789f0626f76e5a6fbf5e`.
GPL-3.0-or-later and notices remain included; no third-party meshes, copied
RuneScape designs or downloaded material assets are introduced.

Purpose now changes working space, stall divisions, public circulation and
guarding structure. It does not establish universal viewer recognition or a final
production finish. Equipment is still simplified; there are no fire/smoke effects,
populated market/animal assets or complete interiors. Rear elevations remain
restrained; some stone/iron faces are austere, and stable/market bays can need
closer art review. Guard positions are partial modeled spaces, not a defense AI
or siege simulation. Wealth changes stall/vendor capacity and selected investment;
gatehouse room-layout wealth differentiation remains limited. Site/terrain,
flood levels, structural/thermal safety and target-engine traversal are untested.
Protected edits survive regeneration but can require manual reconciliation with
the four revised programs and remain outside procedural validation.

## Workflow observations for lessons-learned

Bounded Luna High implementation was useful after an explicit shared interface,
but mocked tests and semantic labels did not establish a working assembled space.
Root integration, actual meshes and early clay critique changed the architecture.
The independent reviewer found a real function-readability failure after machine
gates were green; that correction was completed rather than recorded as acceptance.
Luna Medium handled source research, composition adaptation and bookkeeping;
reference URLs and one path/function-key comparison still needed independent review.
These observations concern this workflow, not a universal model ranking.

One native build is reused for clay/materials and both angles. Partial refresh
preserves old images/provenance and invalidates retained views if geometry or
common framing changes. It retained forty-four views on the forge/access pass
and forty-eight on the final exhaust pass, but incremental
manifest support and review also consumed engineering/model effort. No measured
token, subscription-allowance, API-dollar or total wall-time saving is established.
The testable lesson is earlier semantic/art falsification plus targeted verification,
not simply fewer calls, cheaper models or larger test/gallery counts.
