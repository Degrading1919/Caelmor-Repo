# Lowmark terrain input authority

The Creative Director approved the planning and thematic maps' horizontal composition and subsequently approved a **3,456 × 3,072 m** working frame. The illustrated scale, elevations, gradients and contours are unsurveyed. Both original PNGs are retained at their original hashes. In `lowmark_controls.json`, `map_px` and `map_points_px` retain the original source traces, while `xy` and route `points` are the current technical controls. Some have a separately recorded `working_trace_px` for comparison. Water widths, engineering heads, road widths, settlement envelope diameters, footprint assumptions and local edit limits stay in physical units.

The basin edges and channel alignments retain the approved composition. The four broad landform radii are 560, 470, 490 and 230 m. The northeast crest is shifted toward the edge and its amplitude reduced to 74 m so Ashenstead can occupy a usable lower shoulder. That and the narrower western ridge prevent the compact frame from inheriting oversized upland slopes across the reclaimed fields and civic shelf. These are technical elevation controls.

Provisional site edits bring the Hall and Depot into the Crestbridge corridor, put Whisperflow Landing on the west bank of the eastern hairpin, offset the Drowsebank yard from its race, and shift the Ashenstead and Greyharrow centres to nearby working ground. Attached access traces follow the new endpoints. The composition, hydraulic levels, network identities and named features were retained. Existing map approvals do not establish engineering details, quest interfaces or final parcel positions.

The seven settlement capacity ranges come directly from that mission. Building counts, assigned NPC rosters, visible NPC estimates and built-up spans are **proposed planning targets**. This prototype creates no buildings or NPCs. Candidate building land, circulation/public space and surrounding working landscape are distinct measurements. Candidate capacity is a feasibility estimate using an explicit average footprint and plot allowance, not a cadastral plan.

## Repository source constraints

Line ranges below refer to the original mission source revision and can shift in later editions. The compact pass reviewed the current main at `d0e44fa`, including the Director rulings and Acts I–III. Current file fingerprints and revisions are recorded in the controls.

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
| Same | 436–472 | Adjacencies and water-contact requirements; Reedmere is at the fen's landward edge. These requirements help test provisional offsets under the compact mandate. |
| Same | 510–516 | The older zone package explicitly leaves hydrology-chain approval and several map questions open. The approved composition and compact working frame govern the prototype. Site offsets remain provisional, with conflicts measured against the quest requirements. |
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

The provisional Hall and Depot centres sit within the working Crestbridge core envelope. Their government, grain handling and underground service spaces have different access needs, and the original roof budget does not allocate these functions. The local render uses scale proxies to expose spatial relationships and makes no placement ruling.

## Orchard floodplain constraint

The orchard label alone did not establish a seasonal floodplain: the initial regional field placed the anchor about 7.7 m above the nearby weir stage, beyond the tested 1.5 m rise. The final authored orchard polygon therefore constrains low ground 0.6–0.8 m above its weir reference, with sparse 1.2 m berm ridges and a 180 m boundary transition. Its drainage apron follows the retained Cut-mouth/towpath works toward Bramblelock, with an 80 m core and 120 m transition; this is inferred local floodplain/ditch space, not an additional approved major watercourse. These numbers correct unvalidated terrain elevations within the approved composition; they neither relocate the orchard nor create town plateaus, trees, buildings, finished field parcels or a completed civil grading design. Independent tests now verify actual gravity routing and normal/raised-stage river connectivity; the static scenario does not establish flood frequency or detailed berm engineering.

## Boundary and interpolation corrections

Visual QA rejected a giant northwestern cliff caused by applying a nearest-channel water-stage floor outside its intended corridor. A second nearest-stage switch at the fen apron also produced an artificial upland discontinuity. The corrected algorithm bounds per-reach bank controls; the authored fen guard refers to the declared Veilwater Falls direction, transitions over 500 m and fades across 200 m at the polygon boundary. These are interpolation safeguards, not new cliffs or map features.

The current boundary rim keeps the original 25 m amplitude at a 230 m radius. Independent regional review measured a 7.343 m maximum conditioning raise against the unchanged 12 m budget. The 83.6 m waterfall drop remains. The bounded, single-outlet model closes the remaining frame edges; the terrain beyond the frame and the actual drainage divide remain unsurveyed.
