# Lowmark terrain input authority

The Creative Director's November 6, 2026 mission approves the supplied maps' geographical composition and relationships. Illustrated elevations, gradients, contours and scale remain unvalidated. The traced coordinates in `lowmark_controls.json` preserve the supplied topographical map's left panel; elevations, widths, flood allowances and development thresholds are adjustable **technical proposals**, not geography or population canon. The thematic map is a composition cross-check, not independent height data.

The seven settlement capacity ranges come directly from that mission. Building counts, assigned NPC rosters, visible NPC estimates and built-up spans are **proposed planning targets**. This prototype creates no buildings or NPCs. Candidate building land, circulation/public space and surrounding working landscape are distinct measurements. Candidate capacity is a feasibility estimate using an explicit average footprint and plot allowance, not a cadastral plan.

## Repository source constraints

Line references below are to the source files at the mission's verified `main` baseline. Source hashes are recorded in the controls/evidence so later edits cannot silently change what was read.

Text source fingerprints use SHA-256 over UTF-8 without a BOM and with LF line endings (`hash_mode: utf8_lf`), making Git CRLF/LF checkouts equivalent; binary maps use unchanged raw-byte hashes (`hash_mode: raw`).

| Source | Lines | Terrain significance and authority |
|---|---:|---|
| `LORE/Regions/Caelmor_Region1_LowmarkVale.md` | 137–141 | Whisperflow is a wide gentle main-river bend, with soft reed banks and old markers. Regional dossier. |
| Same | 147–151 | Floodplain orchards occupy seasonal flood routes; trees stand on raised berms; old dikes and sluices remain. Local earthworks, not a region-wide flat platform. |
| Same | 170–176 | Crestbridge crosses the central river; bridge, tolls and Crest Hall control nearby roads. |
| Same | 180–186 | Stillwater Fen is where the river slows and spreads into shallow channels. It must remain wet and connected. |
| Same | 190–200 | Veilwater's hidden enclave is behind the waterfall curtain. Regional terrain may reserve a concealed recess; it does not author the enclave or its reveal. |
| Same | 206–255 | Brookhollow is a riverside market town; Crestbridge a bridge town; Ashenstead rebuilt agricultural village; Greyharrow a more fortified side-branch town. |
| Same | 471 | Uphill Canal is an apparent gravity-defying side channel. Do not erase its topographic relationship to make every channel passive. |
| `04_CONTENT_PRODUCTION/Zones/Caelmor_Lowmark_POI_and_Zone_Requirements.md` | 29–38 | Authored spatial contract: Falls → Fen → Crestbridge → Drowsebank → Cut mouth → Bramblelock → Whisperflow → Brookhollow → Greyharrow branch → exit; straight Relief Cut bypasses the toll bridge and rejoins below it. The flush supplies barge depth, not upstream propulsion. |
| Same | 155–201 | Bramblelock lies below the Cut mouth; Hollow Lock is near the fen end; Drowsebank's tail reaches the lower Cut by a wartime spur. Local engineering must have actual head and connectivity. |
| Same | 331–351 | Uphill Canal has a low foot pool, higher cistern, stepped screened channel and hillside culvert; Falls have plunge pool, outflow and switchback access. Camera/quest spaces require later local authoring, not generated here. |
| Same | 436–472 | Adjacencies and water-contact requirements; Reedmere is at the fen's landward edge. These requirements predate the approved maps and do not authorize moving their anchors. |
| Same | 510–516 | The older zone package explicitly leaves hydrology-chain approval and several map questions open. The new map directive is the higher, current placement authority; mismatches must be surfaced rather than silently solved by relocation. |
| `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Side_Quests_Discovery_and_Memory.md` | 283, 304–311 | Authored canal scene: short uphill steps; low foot pool; head cistern spilling back when its gate is absent; a dry culvert after the pool falls. Preserve separate lift, storage, passive return and culvert functions. |
| Same | 496–500 | Mystery ledger's author truth is explicitly **proposal**, not locked canon. It describes a Braid lift and calls an ordinary pump a wrong reading; the mechanism remains withheld. Terrain work must not promote an invented mechanism to canon. |
| `04_CONTENT_PRODUCTION/Quests/Caelmor_Lowmark_Main_Act_III.md` | 239–247 | Authored state seals the Cut at both ends and its side culverts. Natural outlets must not be silently closed in a baseline terrain model to implement this quest state. |

## Hydrology interpretation boundaries

Natural rivers, tributaries, downstream exits, gravity-fed mill races and open-cut channels must have continuous, non-increasing water-surface profiles. Bed elevations and water depths are technical proposals. Locks and weirs are engineered level controls, not uphill natural river segments; their gates and transient operations are not simulated by this static prototype.

The integrated prototype uses a common 1.2 m planning channel depth at natural/engineered junctions. This avoids a deeper cut bottom ending in an artificial submerged outfall sump; it does not certify barge draft or lock operation. A broad lowland control follows the already traced Relief Cut, preferring background ground 3.5 m above its water profile across a 180 m core with a 400 m transition. This is an explicit terrain-design proposal, not evidence of historical excavation, a newly approved geographical feature or a settlement grading platform. Coordinates and water stages remain unchanged.

**Unresolved quest-state outlet conflict:** the zone package's line 32 describes a natural outlet from Stillwater Fen toward Crestbridge, while Act III lines 239–247 say sealing the Relief Cut and its side culverts leaves the fen with no outlet. Closing a parallel cut cannot eliminate an independently open natural river. The baseline must preserve the approved main-river connection. A later quest-state hydraulic model needs an explicit, reviewed outlet-control explanation; this prototype neither silently dams the river nor treats the sealing claim as physically validated.

The Uphill Canal is an explicit exception to passive-flow verification. Preserve its approved horizontal alignment and low-foot/high-cistern relationship. A positive-head transfer requires an energy source, but the existing quest proposal withholds the mechanism and rejects an ordinary pump explanation. Represent the transfer as a declared anomalous authored boundary with its positive head measured. Do **not** call it physically explained, reinterpret it as gravity flow or add a new pump mechanism. A separate return spill can run downhill, and the culvert's invert must remain distinguishable from the pool levels.

No rainfall/runoff calibration, flood return period, sediment simulation, bank stability, geotechnical certification or medieval works design is established by a static heightfield. Flood envelopes and settlement freeboards are conservative planning scenarios, not predictions. The production step is local terrain/hydraulic refinement and Director review of any flagged composition conflicts.

## Access and outworks boundary

The final input set includes three additional **candidate technical access corridors**: Crestbridge–Mill via the fixed crossing, Crestbridge–Crest Hall and Crest Hall–Hill Depot. Their 8 m widths and 10% cart-grade screens are technical proposals. They do not assert that a road, bridge, grading scheme or runtime navigation exists.

The approved Hall and Depot anchors are outside Crestbridge's proposed 600 m built-up core envelope. They are therefore assessed as separate outworks/infrastructure in the third working-landscape area, retaining their positions. Whether the preliminary building/span budget must include them remains a Director-level scope clarification. The working-landscape radius is a measurement screen, not a claim that all infrastructure fits inside that circle. This classification does not create new building content or expand the approved settlement count.

## Orchard floodplain constraint

The orchard label alone did not establish a seasonal floodplain: the initial regional field placed the anchor about 7.7 m above the nearby weir stage, beyond the tested 1.5 m rise. The final authored orchard polygon therefore constrains low ground 0.6–0.8 m above its weir reference, with sparse 1.2 m berm ridges and a 180 m boundary transition. Its drainage apron follows the retained Cut-mouth/towpath works toward Bramblelock, with an 80 m core and 120 m transition; this is inferred local floodplain/ditch space, not an additional approved major watercourse. These numbers correct unvalidated terrain elevations within the approved composition; they neither relocate the orchard nor create town plateaus, trees, buildings, finished field parcels or a completed civil grading design. Independent tests now verify actual gravity routing and normal/raised-stage river connectivity; the static scenario does not establish flood frequency or detailed berm engineering.

## Boundary and interpolation corrections

Visual QA rejected a giant northwestern cliff caused by applying a nearest-channel water-stage floor outside its intended corridor. A second nearest-stage switch at the fen apron also produced an artificial upland discontinuity. The corrected algorithm bounds per-reach bank controls; the authored fen guard refers to the declared Veilwater Falls direction, transitions over 500 m and fades across 200 m at the polygon boundary. These are interpolation safeguards, not new cliffs or map features.

With those artifacts removed, the original unsurveyed northwestern corner lay at about 155.7 m behind a 178.9 m ridge, below the retained upland headwater, requiring 23.16 m of conditioning in this closed-boundary study. The tested minimal correction adds a smooth 25 m Gaussian at the northwestern frame corner with a 350 m radius. The core verification measured a 9.405254 m maximum conditioning raise, within the unchanged 12 m budget. The 83.6 m authored waterfall drop and all approved anchors remain unchanged. This is an explicit **technical boundary-height proposal**: the bounded single-outlet model closes the remaining frame edges, while the true divide and any drainage outside the supplied map remain unsurveyed. It is neither a named geographical/canon feature nor evidence that this fill or earthwork historically occurred.
