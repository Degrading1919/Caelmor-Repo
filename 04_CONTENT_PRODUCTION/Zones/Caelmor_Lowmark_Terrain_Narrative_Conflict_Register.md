# Lowmark — Terrain / Narrative Conflict Register

**Status:** A record for the Creative Director and Sol (Systems Engineer). It is not a ruling, a proposal for new geography, or a quest rewrite. Each row says where the provisional terrain and the authored narrative disagree, and lists the options neutrally. **No option is recommended.** Nothing here moves a landmark, invents a waterway or structure, or changes quest text, flags or steps.

**Authority, as the sources state it:**
- The Director's November 6 mission approves the supplied maps' **horizontal composition and relationships**. Elevations, gradients, contours and scale are **not** validated (`CODE/Scripts/terrain_generation/MISSION.md`; `SOURCE_NOTES.md` opening).
- All metre heights, water stages, depths, freeboards, capacity screens and access corridors in the terrain are **technical proposals** (`lowmark_controls.json` → `authority`).
- The narrative packages mark every place as **MAP VERIFICATION REQUIRED** and nothing new is canon until the Director promotes it (POI file header; bible D-5, D-11). The POI file (§7, lines 510–516 per `SOURCE_NOTES.md`) predates the approved maps. Sol's sources treat the new map as the higher placement authority and say mismatches must be surfaced, not solved by relocation (`SOURCE_NOTES.md`, Zones 510–516 row).

**Terrain baseline read:** `main` with commits `3ec4003` (regional foundation), `24d179d` (local 2 m refinement and Unity walking inspector), `d9fbc37` (architecture pipeline and scene protection) and `f5b05d6` (100 material masters). Terrain sources: `CODE/Scripts/terrain_generation/` (README, LOCAL_README, LOCAL_REVIEW, SOURCE_NOTES, MISSION, LOCAL_MISSION, `lowmark_controls.json`, `local_controls.json`) and `MEDIA/Maps/Lowmark_Terrain/` (`verification.json`, `metrics.json`, `hydrology_and_routing.png`, `Local_Refinement/`).

**Narrative sources:** `Zones/Caelmor_Lowmark_POI_and_Zone_Requirements.md` (cited as **POI**), `Quests/Caelmor_Lowmark_v1_Narrative_Production_Bible.md` (**Bible**), `Quests/Caelmor_Lowmark_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md`.

**Severity key:**
- **Blocks:** a required quest beat or step cannot be played as written on the current terrain.
- **Degrades:** the beat can run, but a stated spatial requirement, premise, sightline or pacing is lost or weakened.
- **Cosmetic / scope:** the conflict affects presentation, budget or scope. No beat depends on it.

**Measurement provenance.** Numbers marked **[Sol]** are quoted from Sol's documents or evidence files. Numbers marked **[liaison]** were computed for this register. They use the traced coordinates in `lowmark_controls.json` (normalized × 6,144 / 4,992 m) and the saved 8 m `height.npy`. They have not been verified by Sol and should be rechecked before anyone relies on them.

---

## 1. Register

### TC-01 — Crest Hall is not on the river (water-gate, Gate Landing, Granary Passage cistern, bridge north stair) — **lead item**

| Field | Record |
|---|---|
| Place | P02 Crestbridge and Crest Hall (Hall areas E, F, G); NB underside north stair (G) |
| Terrain now | Crest Hall anchor is a fixed approved-map symbol at about [3257, 1830] m. It is **640.31 m from the nearest retained natural river**, 679.49 m from the regional `crest` river node, and 652.28 m from the town anchor. Ground at the Hall is about 70.0 m. Crossing stage and bed are 63.10 / 61.90 m **[Sol]** (`LOCAL_REVIEW.md` "Measured conflict"; `LOCAL_README.md` "What still requires a decision"). The Hall's nearest water of any kind is the Drowsebank mill leat, at about 616 m. The Hall is about as far from Drowsebank Mill's anchor (647.6 m) as from Crestbridge's (652.3 m) **[liaison; site screen in `verification.json` → `landmark_site_screen`]**. Sol states plainly that a better road cannot give the Hall a direct water-gate or put the bridge's north stair beside it. No canal, annex, tunnel or moved anchor has been added. |
| Narrative requires | Act III §10.3: "Crest Hall stands on the Crestbridge bank beside the granaries, its undercroft cut down to river level where a wartime water-gate lets barges unload straight beneath the hall." The water-gate must open onto the river **above** the Cut mouth so Sallow's skiff can reach it. Area F is a vaulted basin open to the river through an iron gate. Area G is a ~14 × 8 m Gate Landing with steps out of the water at each end. Area E's cistern is "fed from the river". POI P02 Map: the basin is wade-depth with end steps, and the NB north stair emerges close to the water-gate wall. POI §6.1: NB north stair near the Hall water-gate wall. POI §3 S1: Crestbridge underside → north stair near the water-gate, which is an optional MQ10 approach. §10.7 strange moment: water-gate audio carries through the Long Hall floor-grates. |
| Affected | **MQ10** `S05_water_gate` (barge chase, `throw_mooring_line`, `drop_gate_lever`), `S05b_haul` / `CR_HAULED_CREWMAN`, `S06_sallow` (Sallow arrives "up the far steps from his skiff"; `cr.sallow_yield`), `S10_plan` → `cr.plan_agreed` audio duck. **Night Bridge** (NB) north-stair exit and `NB_UNDERSIDE_OPEN`. POI §6.2 water-contact row. |
| Severity | **Blocks** (MQ10 S05/S06 need river water under the Hall; NB's exit adjacency fails). |
| Options (neutral) | (a) Keep every regional anchor and leave the civic adjacency unresolved for now. This is Sol's current implemented stance (`LOCAL_REVIEW.md` option 1). (b) The Director approves an explicit local map revision bringing the Hall's functional footprint, granaries, north stair and Depot exit into one crossing compound. Any anchor adjustment, or reading the Hall symbol as a district label, would be approved and recorded first (Sol option 2). (c) Keep the remote buildings fixed and revise the authored connection requirements, which needs explicit quest/location changes and new scope (Sol option 3). Sol notes that a new ~640 m canal or invented annex is not a routine terrain fix. (d) The Director rules on a different reading of the map symbol or the quest text that is not listed here. Narrative owners would then revise affected beats under that ruling. |

### TC-02 — Granary yard position is unfixed and over-constrained

| Field | Record |
|---|---|
| Place | P02 granary yard (A), tally room (B), undercroft (C), hill passage (D); waiting wall |
| Terrain now | **No approved granary XY exists** in the sources. The granary box in the Blender scene is labelled a "conceptual yard-location example". It is excluded from grading and capacity (`LOCAL_REVIEW.md` "No approved granary XY"; `LOCAL_README.md` §Inspect). Hall → Depot is 403.70 m straight; the candidate access is 407.31 m **[Sol]**. |
| Narrative requires | POI P02: the waiting wall faces **both** the granary yard and the south toll on the bridge. POI §6.1: the granaries have the Depot behind them, the Hall beside them, and a Granary Passage linking undercrofts. Act I A5.1 C–D: a chalk line to HILL GATE and a stone-lined hill passage from the undercroft into the depot. Act III §10.3 E: a low passage from the Hall to Corvin's granary undercroft. |
| Affected | **MQ2** (SM) `S00_arrive`, `S08_yard` (the live draw-signing glimpse), hill passage entry. **MQ10** `S04_records` / `S05` route through the Granary Passage, plus Beat 0 evening scene on the waiting wall. HS forge "under the first arch". `LM_GRAIN_ROUTE` props. |
| Severity | **Degrades**; becomes **Blocks** if no single site can satisfy both "faces the south toll" and "Hall beside / Depot behind" at the current anchor spacing. |
| Options (neutral) | (a) Leave the yard unplaced until TC-01 is ruled. Sol's review names this as "the next consequential ruling". (b) The Director fixes a granary XY on the approved map under whichever TC-01 option is chosen. (c) The Director relaxes one of the adjacency statements (toll-facing wall, Hall beside, Depot behind) as a narrative revision. |

### TC-03 — Hill Depot chute and river ledge are far from the river

| Field | Record |
|---|---|
| Place | P07 Hill Depot, areas K (Chute Gallery) and L (chute lip and river ledge) |
| Terrain now | Depot anchor is **836.62 m from the nearest retained natural water**. Gross ground-to-water head is 4.1357 m over that distance (mean fall 0.4943%). The closest water point is at the toll line, not a verified below-toll backwater **[Sol]** (`LOCAL_REVIEW.md` "Depot head/length diagnostic"). The Depot symbol is an area reference, not an approved gallery/chute footprint. **[liaison]** The nearest traced water of any kind to the Depot anchor is the Relief Cut straight, at about 303 m. This is recorded as a fact only, not as a suggested reading. |
| Narrative requires | Act I A5.2 K: a stone chute "drops through the hillside to the river", with a pulley gantry. L: a ledge "high above a slack backwater of the river", a mooring ring, and "a short walk down" to the bank and the hill road back to Crestbridge. POI P07 Map and §6.1: the chute drops to a slack river backwater **below Crestbridge's toll line**. POI §1: "Grain reaches Brookhollow from the Hill Depot chute by night skiff below the toll line." |
| Affected | **MQ2** area L (optional view) and the post-boss ledge shortcut. R2 Towpath route (POI §3: "Hill Depot river ledge"). Bible/POI §1 smuggling logic. W-03 revisit. |
| Severity | **Degrades** (L is optional in MQ2), but it undermines a stated §1 premise of the scheme. |
| Options (neutral) | (a) Hold as unresolved alongside TC-01 (Sol's stance). (b) Resolve within whatever compact-compound ruling is made for TC-01. (c) Revise the authored chute/ledge requirements, for example to a longer underground route or a detached exit. Sol notes such routes are conceivable but unapproved in geometry, scale and solo-dev cost. (d) A Director reading of which water the chute meets. Any change from "river backwater below the toll" is a narrative change to P07 / Act I A5.2. |

### TC-04 — The bridge itself: crossing position, approach and structure are unbuilt

| Field | Record |
|---|---|
| Place | P02 bridge (span, south toll, north end, underside piers 1–3, forge under the first arch) |
| Terrain now | The retained road/river intersection is at [2581.21, 1556.42] m, about 60.31 m from the `crest` node. A neutral 72 × 8 m deck proxy has a 66.115 m deck top. It is "an unapproved scale/deck example" **[Sol]** (`LOCAL_REVIEW.md` "Inspection crossing correction"). In the Unity inspector the deck's measured approach gap is **2.56 m**, which exceeds the 0.3 m controller step, so the deck is not claimed walkable from the road (`LOCAL_README.md` "Walk in the isolated Unity inspector"). No bridge or ford is generated anywhere (`verification.json` → `routes[].crossings`). The architectural generator has no bridge type (§2 below). |
| Narrative requires | POI P02: dwarven-reinforced span; south toll with tally table; forge under the first arch with a quench trough fed by a river channel; underside with crew stair, three piers, a reed island at pier 2, an arch-2 soffit, and a north stair. POI §6.3: footsteps on the deck carry down under arch 2. |
| Affected | NB (whole underside traversal), HS (forge), MQ2/MQ10 toll-facing waiting wall, R1 River Road. |
| Severity | **Degrades** (production gap). Becomes **Blocks** for NB if the north-stair adjacency in TC-01 is not resolved. |
| Options (neutral) | (a) Treat the bridge as a hand-authored structure in a later local site design at the retained crossing. (b) Defer until TC-01/TC-02 fix the civic layout around it. (c) Request a bridge capability from Sol's tools. That is a tool-scope decision for Sol and the Director, not assumed here. |

### TC-05 — "Short towpath walk" from Crest Hall's bank to the Cut mouth

| Field | Record |
|---|---|
| Place | Crest Hall → Relief Cut mouth (P10 T3) |
| Terrain now | Hall anchor → `weir_up` node (where the Cut, the mill tail and the main river converge): about **843 m straight** **[liaison]**. The Hall is not on a bank (TC-01). Sol notes that Act III line 248 also wants a short towpath walk from the Hall's bank to the Cut mouth (`LOCAL_REVIEW.md` source table, Night Bridge row). |
| Narrative requires | Act III Beat 10 `S11_dusk`: walk-with from the hall down the towpath, with dusk falling during the walk. "MAP VERIFICATION REQUIRED: the Cut mouth is a short towpath walk from Crest Hall's bank." |
| Affected | **MQ10** `S11_dusk`, optional `drop_last_plank`, `CR-D11` (Ansel and Sedge at the mouth). |
| Severity | **Degrades** (walk length and the "bank" premise; the beat still runs). |
| Options (neutral) | (a) Follow the TC-01 ruling; the walk length follows from it. (b) Keep the geography and accept a longer walk-with, which the dusk transition can absorb. (c) Revise the beat's start point. That is a narrative change. |

### TC-06 — Drowse spur: no distinct tail-race-to-lower-Cut channel

| Field | Record |
|---|---|
| Place | P11 Drowsebank Mill, area H (the Drowse spur); P10 lower Cut |
| Terrain now | `drowsebank_tailrace` returns 557.66 m to the **common outfall node `weir_up`**. The Relief Cut downstream reach and the main river also meet there. The reach is marked "Provisional tail return; Drowse spur-to-lowerCut link pending local detail" (`lowmark_controls.json` reaches; `LOCAL_REVIEW.md` "Mill race and lower Cut"). Sol: "Current common-outfall graph does not establish that distinct spur." An upstream-of-wheel bypass would be new detail, not a source-supported replacement. |
| Narrative requires | Act II TF.4 H: "Downstream, the dressed channel joins a straight wartime spur toward the Relief Cut below Crestbridge." TF.16 item 1 recommends approving the Drowse spur. POI P11 Map and §6.1: tail race reaches the **lower Cut by a wartime spur**. POI P10 "Used by MQ6 (Drowse spur joins the lower Cut)". |
| Affected | **MQ6** (TF) area D/H context, `TF_KEEPERS_READ_BACKWATER`; Bible §2.3 backwater; Act II §A2.2 "one water story after MQ4". |
| Severity | **Degrades** (area H is "Context"; the premise of the crew route rests on it). |
| Options (neutral) | (a) The Director approves the Drowse spur as a wartime work (Act II TF.16 item 1), and Sol fits a distinct spur in local design without moving anchors. (b) The Director accepts the common-outfall reading, and narrative owners check whether the TF.4 H wording still holds. (c) Hold unresolved until the Cut-mouth separation (TC-09) is designed, since both meet at `weir_up`. |

### TC-07 — Barges and crew pulses through the mill race; backwater up the spur

| Field | Record |
|---|---|
| Place | P11 race, race gate, tail race; Drowse spur |
| Terrain now | Mill working head is 0.95 m (forebay 62.5 → tail 61.55 m). It "can drain; it does not establish barge passage" **[Sol]**. The corrected leat's minimum static depth is **0.136 m**, below the 0.2 m target. It is "not proven barge draft or discharge capacity" (`LOCAL_README.md` findings). The model is static, so no reverse flow up the spur is represented (`lowmark_controls.json` → `operating_state`). |
| Narrative requires | Bible §2.3: after MQ4 "Sallow's crew still runs barges ... only through Drowsebank's mill race and a wartime spur to the Cut". Act II §A2 author truth: crew pulses go only through the race via the spur. Act II TF.15: the tail-door lines are backwater "arriving up the Drowse spur". TF.4 C: a race gate between pond and race, with stop-plank grooves. |
| Affected | **MQ6** TF.6 set piece (bracing the gate across three swells), the night scene (crew at tail door), `TF_MAX_BAND`, `LM_FLUSH_CALENDAR`. |
| Severity | **Degrades** (hydraulic premise; the set piece is staged locally and can play). |
| Options (neutral) | (a) Sol inspects a controlled passage or bypass with operating levels, width and draft before any works are approved (Sol's stated next step). No lock is silently added. (b) The Director clarifies whether "barges" through the race means laden barges or smaller craft. That is a narrative clarification, not assumed here. (c) Treat pulses and backwater as quest-state presentation outside the static terrain model, recorded as an explicit exception like the Uphill Canal's. |

### TC-08 — Drowsebank mill site: marker sits on the channel; pond works not laid out

| Field | Record |
|---|---|
| Place | P11 areas A (yard, pond bank), B (ground floor on the race wall), C (footbridge, far crank on pond bank), E (loft), G (far-bank spill weir) |
| Terrain now | The fixed mill centre samples an engineered channel: natural ground about 67.27 m, open-bed about 60.91 m. A building placed on the marker would occupy the wheel/race corridor (`LOCAL_REVIEW.md`, Drowsebank paragraph). Capacity: 4 regional / 5 local candidates against a 4–10 roof target, with "machinery, pond/wheel, spur and ancillary programme ... not laid out" (`LOCAL_README.md` table). |
| Narrative requires | POI P11; Act II TF.4: a broad still pond behind the mill, race gate with near and far cranks across a narrow footbridge, spill weir on the far bank, a pond-bank volume within 15 m of the water for the lag effect, and the loft gap view (POI §6.3). |
| Affected | **MQ6** all beats; TF.8 lagging pond; mill micro-event; ME08 echo. |
| Severity | **Degrades** (production layout outstanding; nothing contradicts in principle). |
| Options (neutral) | (a) A local mill site design beside the retained waterworks, as Sol recommends. (b) The Director confirms the 4–10 budget or a lower scope for Drowsebank. |

### TC-09 — Cut mouth, Bramblelock and the orchard towpath share one node

| Field | Record |
|---|---|
| Place | P10 T2/T3, P08 Bramblelock Weir, P16 Floodplain Orchards, P15 Sluice Shelter |
| Terrain now | `relief_cut_downstream`, `drowsebank_tailrace` and `mill_bypass_main_river` all end at node `weir_up`. Bramblelock's 1.2 m weir runs `weir_up` → `weir_down`. The Cut reach carries "Cut-mouth/weir spatial separation requires later local engineering detail; no anchor moved" (`lowmark_controls.json`). `unresolved` → `local_waterworks_detail` lists "Cutmouth/weir separation". **[liaison]** The orchard floodplain polygon lies beside the Cut's downstream reach (orchard anchor ~522 m from it), upstream of the shared node. The orchard drainage apron "follows the retained Cut-mouth/towpath works toward Bramblelock" (README "Method" §orchard). |
| Narrative requires | POI §1 chain: "Relief Cut mouth (Cut rejoins) → orchard floodplain (towpath under the dike) → Bramblelock Weir". The barge is poled upstream "over the weir crest, along the orchard towpath, over the Cut-mouth silt sill, up the Cut". POI P08: below the Cut mouth; the barge passes within ~6 m of the bench. P16 Map: floodplain below the Cut mouth along the towpath and Bramblelock. §6.1: Cut mouth near the orchard towpath, with Bramblelock downstream. Act I line 777: the barge passes Bramblelock on the pulse, and the mouth is reachable along the towpath from the weir. |
| Affected | **MQ4** chase legs (R2), NF §C8.1 bench sightline, `S11` towpath in MQ10, MQ3/MQ7 orchard beats, MQ12 stop-planks at the mouth. |
| Severity | **Degrades**; **Blocks** the MQ4 mouth → towpath → weir chase sequence if mouth and weir remain one point. |
| Options (neutral) | (a) Sol separates mouth and weir in local engineering design along existing alignments, with no anchor moved. (b) The Director reads the approved map to fix the order of mouth, towpath and weir. (c) Narrative owners revise the chase order to match the map. That is a narrative change. |

### TC-10 — The Relief Cut straight is long for its pacing beat

| Field | Record |
|---|---|
| Place | P10 T4 the straight (mouth fight → Hollow Lock) |
| Terrain now | `relief_cut_straight` is about **1,868 m**, `relief_cut_elbow` about 450 m and `relief_cut_downstream` about 1,182 m **[liaison, polyline lengths]**. At the 3 m/s technical walk (a sensitivity input, not balance), the straight alone is about 10 minutes. Sol: "Long regional journeys cannot inherit old 60–90 second quest-transition assumptions" (README "Review before production lock"). |
| Narrative requires | Act I line 817: "a short, quiet walk up the straight ... about 60–90 seconds". POI P10 Map: 60–90 s walk between the mouth fight and the Lock. |
| Affected | **MQ4** pacing beat; MQ10/MQ12 plank crews. |
| Severity | **Degrades** (pacing). |
| Options (neutral) | (a) Accept the longer walk. (b) Start the pacing beat partway up the Cut (a staging change). (c) Revise the stated duration. (d) Revisit world scale; Sol calls the 6,144 × 4,992 m extent "a working compromise for review", not approved size. |

### TC-11 — Fen "no way out" versus the open natural outlet

| Field | Record |
|---|---|
| Place | Stillwater Fen, Relief Cut, Hollow Lock, fen_to_crestbridge river |
| Terrain now | The approved natural outlet from the fen toward Crestbridge stays open. "Closing a parallel cut cannot eliminate an independently open natural river" (`SOURCE_NOTES.md` "Unresolved quest-state outlet conflict"; `lowmark_controls.json` → `unresolved.sealed_fen_outlet`). The prototype neither dams the river nor treats the sealing as validated. |
| Narrative requires | Act III Beat 10 `S11_dusk`: "The planks close the Cut-side culverts ... for the first time since MQ4 the fen has no way out at all." Act III Beat 9 roll: seal the Cut at both ends and plank the culverts. Bible §2.3: "the pressure has nowhere to go" → Hollowed Current (MQ11). |
| Affected | **MQ10** S10/S11; **MQ11** premise (fen "holding its breath"); `LM_FEN_ENDING`; D-12 backwater ruling. |
| Severity | **Degrades** (premise; the beats can play). |
| Options (neutral) | (a) The Director clarifies that the quest concerns isolated deep storage / Braid pockets rather than all river discharge. Sol notes this is the least geographically disruptive; it is a reviewed narrative/state interpretation. (b) Identify approved existing sill/gate controls on the natural outlet and model them. (c) Leave the line as in-world belief, unconfirmed by hydrology. That is a narrative decision. |

### TC-12 — Reedmere: stilt access, staging, evacuation ground

| Field | Record |
|---|---|
| Place | P06 Reedmere (stilt huts, plank walks, lantern store, staging F, kept path G, Causeway mouth); P30 gates |
| Terrain now | Regional: 43 roofs at normal stage, **0** outside the +1.5 m scenario. Implied raised floors are roughly 1.13–1.43 m. Local 2 m: **0 dry candidates; 55 conditional stilt candidates**. "Raised floors, piles, connected walks and evacuation still require design." Three neutral 10 × 8 m floor/pile tests only; no ground filled (`LOCAL_README.md` table; `LOCAL_REVIEW.md` Reedmere row). Anchor is ~173 m from the traced western braid **[liaison]**. Smaller marsh channels are not traced (README fen paragraph). |
| Narrative requires | POI P06: stilt huts on plank walks; tally board by the steps; staging F with a reed-mat floor ~20 × 14 m, four staked discs, pool kerb and landward shallows strip **at a deep pool's edge**; withy line across a channel mouth; on the fen's **landward edge**; three Braid gates in a line toward the centre. Act III §11.3 A–D; Beat 2 `S02_evacuate`: cutters led back to the hub (up to 4 followers, NavMesh walkable). POI §0: every objective walkable; deep water non-navigable. |
| Affected | **MQ3** escort walk; **FW** (staging, withies, kept path, `FW_BED_SHARED`); **MQ11** S00–S02 and gate line; MQ12 station. |
| Severity | **Degrades** (no contradiction; the walk/pile system and deep-pool staging are undesigned). |
| Options (neutral) | (a) A local Reedmere site programme fitting floors to local stage + scenario + clearance, with walks, staging kerb and evacuation access (Sol's next step), and no fen drainage or plateau fill. (b) The Director chooses which flood scenario Reedmere must be designed for. (c) The Director rules on architectural language for Reedmere's stilt huts (see §2, gap G-2). |

### TC-13 — Whisperflow Landing's distance from water; western arm; far bank

| Field | Record |
|---|---|
| Place | P04 Whisperflow Landing (marker bank E, reed walk F, old footing G, drowned pier H / P12, high landing J); Whisperflow Run bend |
| Terrain now | Landing anchor at about [3633, 459] m is **~489 m from the western arm, ~500 m from the eastern hairpin and ~517 m from the weir-to-Whisperflow reach** **[liaison]**. This is visible in `hydrology_and_routing.png`, where the landing sits south of both waters. The western arm is "INTERPRETATION_UNRESOLVED: terminal backwater vs continuous main meander", 1,436.68 m long with standing stage 60.1 m (`lowmark_controls.json`; `LOCAL_REVIEW.md` row 1). Sol: "the illustration appears to end near the landing". |
| Narrative requires | POI P04: the landing must be a short walk down from the Brookhollow road; shallows, footing, drowned pier downstream, marker bank. POI §6.3: from the road head the **whole landing at once**, including the half-sunk skiff and the pale post. POI §6.2: wadeable river margin. Far-bank settlement open (POI §7 Q3; TL §14 item 4). MQ12 night crossing. |
| Affected | **TL / MQ1** (all landing beats, `TL_EVIDENCE_PILINGS`), ME01, ME08, OL far-leg start, **MQ12** crossing and `RR_MARK`. |
| Severity | **Blocks** the TL landing beats if the landing's working edge cannot meet water. This needs Sol's confirmation, since the anchor is a symbol centre and the envelope is 100–200 m. |
| Options (neutral) | (a) Sol confirms which water the landing fronts and whether the settlement envelope reaches it, without moving the anchor. (b) The Director gives the map reading of the western arm (terminal backwater or continuous meander), which may decide which water the landing serves. (c) The Director answers POI §7 Q3 (far-bank settlement). (d) Narrative owners revise P04's water relationship. That is a narrative change. |

### TC-14 — Uphill Canal: 2.4 km regional line vs a twenty-step quest space

| Field | Record |
|---|---|
| Place | P28 Uphill Canal (A hazel cut, B foot pool, C channel, D listening seat, E cistern, H Hazel Culvert) |
| Terrain now | Envelope lifts water 61.9 → 80.0 m over 2,432.40 m (positive head 18.1 m), with energy source `UNKNOWN_AUTHORED_BRAID_MECHANISM` and no pump invented. Foot ground is about 68.76 m against a 60.7 m open-bed proposal. Cistern ground is about 77.81 m, below the proposed 80 m surface. "This is not yet a modest twenty-step site." The foot overflows downhill to the Cut elbow (`LOCAL_REVIEW.md` row; `lowmark_controls.json`). **[liaison]** The cistern node is at the east frame edge. The foot is ~1.53 km and the cistern ~1.46 km from the Ashenstead anchor. |
| Narrative requires | POI P28: twenty-odd steps sunk a body-height; listening seat; head cistern; switchback; Hazel Culvert whose far mouth opens at the **Ashenstead Fields edge**, bypassing the orchard berms ("any useful lower path works"). The **load-bearing occlusion rule** (channel visible only from inside the observation volume). POI §6.1: near the orchards. Discovery 283, 304–311 (per `SOURCE_NOTES.md`). |
| Affected | **UC** side quest; R3 shortcut; MQ12 optional inspect. |
| Severity | **Degrades** (the quest space needs its own site; the occlusion rule cannot be checked until it exists). |
| Options (neutral) | (a) A separate local site programme that fits pool, steps, cistern, return spill and culvert inside the retained alignment (Sol's stance). (b) The Director reads the map's long stepped line as schematic rather than a literal construction drawing; Sol already treats it this way. (c) The Director fixes which segment of the alignment hosts the quest space. In every option the mechanism stays withheld, per Discovery 496–500. |

### TC-15 — Ashenstead Fields height above the Cut vs "Cut backwater seepage"

| Field | Record |
|---|---|
| Place | P03 Ashenstead / Rebirth Fields (circle at low point, Joric's plot lower), P13 culvert, M06 |
| Terrain now | **[liaison, not flagged by Sol]** The Ashenstead anchor sits on the northeast upland flank. `height.npy` gives about **128 m** at the anchor, falling to about 65.6 m at the Cut corner about 1.26 km away. Cut water there is about 62 m. The anchor's `reference_ground_m` in the controls is 85 m. The extent of the Rebirth Fields is not traced in the terrain. The regional screen finds zero +1.5 m exposure for Ashenstead (`metrics.json`). Part of Crestbridge–Ashenstead exceeds the cart-grade screen (5.8% of the route; README). |
| Narrative requires | POI §1 side relationships: "Ashenstead Fields sit on the Cut's landward side (Rebirth Fields flood by Cut backwater seepage, MQ5)". The Cut runs "past the western edge of Ashenstead Fields". P03 Map: circle at the field's **low point**, Joric's plot lower than the circle, drain toward the reeds and the Path. |
| Affected | **MQ5** (GL) flooding beats and `LM_FIELD_FIX`, P13 culvert, UR, CN, MQ12. |
| Severity | **Unknown until the field extent is traced.** Potentially **Blocks** MQ5's seepage premise if the fields lie well above Cut water. |
| Options (neutral) | (a) Sol traces or confirms the Rebirth Fields' extent on the approved map and reports its ground relative to Cut water. (b) The Director confirms where the fields lie relative to the village symbol. (c) Narrative owners revisit the seepage mechanism if the fields stand well above the Cut. That is a narrative change. |

### TC-16 — Veilwater Falls approach and the end of the Path

| Field | Record |
|---|---|
| Place | P29 Veilwater Falls and the Listening Steps; Path of Unburnt Reeds |
| Terrain now | The waterfall is an explicit 83.6 m drop. "The direct Falls approach intersects the steep fall site and is not a walkable finished path; local listening-step/switchback access must be fitted" (README). The Path route's unengineered maximum grade is 4.61 (460%) against a 0.22 budget, with 3.8% of the route over budget (`verification.json` → `routes.ashenstead_path_of_unburnt_reeds`). The regional terrain "may reserve a concealed recess; it does not author the enclave" (`SOURCE_NOTES.md`, lines 190–200 row). |
| Narrative requires | POI P29: plunge pool with step-stones and a lower ford fallback; switchback falls path with listed walkable fallbacks; curtain ledge threshold; Steps; flow-table chamber walkable all round; falls **heard before seen**. |
| Affected | **MQ9** (BF), VK count channel, MQ12, UC optional inspect. |
| Severity | **Degrades** (local access design outstanding). |
| Options (neutral) | (a) A local falls tile with switchbacks inside the retained location (Sol's stated next step). (b) The Director accepts which fallback routes become the critical path. |

### TC-17 — Mantle Shrine "above a fen-edge channel"

| Field | Record |
|---|---|
| Place | P24 Mantle Shrine (E Mantle channel, west shallows loop, G lower pools) |
| Terrain now | Anchor ground is about 69.7 m with slope 5.76° (`verification.json` site screen). **[liaison]** It is ~298 m from the nearest traced channel (fen eastern braid). Smaller marsh channels "need local refinement" (README). |
| Narrative requires | POI P24: on the Path, **above a fen-edge channel**; west shallows wadeable loop ≥ 8 m from the east bank; two lower pools. |
| Affected | **MQ8** (MN), MQ9 start, ME09, MQ12. |
| Severity | **Cosmetic / scope** (a minor channel is plausibly a local detail; it needs confirmation). |
| Options (neutral) | (a) Author the Mantle channel as a local minor channel in later refinement. (b) Sol and the Director confirm whether a minor channel at the shrine is within approved composition. |

### TC-18 — Regional travel times vs "short walk" and walk-with beats

| Field | Record |
|---|---|
| Place | Region-wide |
| Terrain now | At the 3 m/s technical walk **[Sol, `verification.json` → `routes`]**: Brookhollow–Landing 1,157 m / 6.4 min; Landing–Crestbridge 2,428 m / 13.5 min; Crestbridge–Ashenstead 3,157 m / 17.5 min; Ashenstead–Path 3,727 m / 20.7 min; Reedmere–Crestbridge 2,778 m / 15.4 min. East–west crossing is 34.1 min. Speeds are sensitivity inputs, not balance. All crossings are unbuilt (`unresolved.route_crossings`). |
| Narrative requires | POI §6: "near" means a short walk with view or earshot. Walk-with beats (MQ10 S11, MQ3 escort, ME10 dusk walk P21 → M07 → P22). POI header: "no quest logic depends on distances". |
| Affected | Pacing across TL, MQ3, MQ10, ME10, MQ11 evacuation; R1–R4 route plans. |
| Severity | **Degrades** (pacing only, by the narrative's own rule). |
| Options (neutral) | (a) Accept regional distances and retune pacing text. (b) Revisit world scale (Sol's 4.1 × 3.3 km trial compressed slopes and lost Ashenstead/Greyharrow capacity; the 8.2 × 6.7 km trial costs traversal). (c) Movement balance (walk/sprint speed) is a separate Director decision. |

### TC-19 — Settlement scope: Greyharrow, Brookhollow, Crestbridge outworks

| Field | Record |
|---|---|
| Place | P05 Greyharrow, P01 Brookhollow, P02 Crestbridge |
| Terrain now | **Greyharrow:** 23 regional (18 outside +1.5 m) / 39 local candidates against the mission's 28–50. 50 is not established. It sits correctly on the side branch (~67 m). **Brookhollow:** needs the larger end of its span; a 400 m screen holds only 61. **Crestbridge:** Hall and Depot lie outside the 600 m core and are classed as outworks; whether the budget includes them "requires Director clarification" (`unresolved.crestbridge_outworks_budget_scope`). |
| Narrative requires | Bible §4.2 P05: "Micro-settlement (proposal: dossier calls it a town; it is scoped small for Lowmark)". POI P05 still lists a fortified town, militia gallery, docks, boom and tower square. POI P01: low lanes below the high street; reed margin downstream; side relative to Whisperflow MAP VERIFICATION REQUIRED. |
| Affected | SB, VK, BW, NT (Greyharrow); FK, BP, UL (Brookhollow). No beat depends on building counts. |
| Severity | **Cosmetic / scope**. |
| Options (neutral) | (a) The Director reconciles the mission's capacity targets with the bible's micro-settlement scoping for Greyharrow. (b) The Director confirms Brookhollow's span. (c) The Director rules whether Crestbridge's budget includes outworks (tied to TC-01). |

### Checked with no conflict found (for the record)

These agree with the narrative's fixed facts (Bible §4.1; POI §1). Each is still MAP VERIFICATION REQUIRED in detail.
- The Cut rejoins below Crestbridge and bypasses it (subject to TC-09).
- Whisperflow lies downstream of the rejoin.
- The Hollow Lock lies near the Cut's fen end.
- Reedmere is on the fen's western, landward side.
- The Path runs Ashenstead → Circle → Mantle → Falls in that order.
- Drowsebank lies between Crestbridge and the Cut mouth.
- Greyharrow is on the side branch.
- The fen remains wet and connected.

---

## 2. Architecture and materials: narrative-facing notes

**Status of the tools.** The architectural generator (v0.16.0) is an **offline Blender exterior generator**. Its regional grammars are "reversible visual interpretations ... not new canon" (`REGIONAL_GRAMMAR.md`; `WORLD_ARCHITECTURAL_LANGUAGES.md` "Purpose"). It does **not** create interiors or enterable room layouts, arbitrary polygons, complete settlements, or terrain fitting (README "Scope limits"). Final art acceptance is the Creative Director's (`FUNCTIONAL_PROGRAMS.md`; `ARTISTIC_REFINEMENT.md`). The Unity pipeline prepares exports **for later hand placement**. It creates no settlement or navigation, and **nothing is placed in any world scene yet** (`UNITY/ARCHITECTURE_PIPELINE.md`).

**Twenty types available:** Farmhouse, Cottage, Townhouse, Longhouse; Barn, Grain Store, Stable; Miller, Inn, Merchant House, Shop, Warehouse, Market Hall; Smithy, Workshop; Assembly Hall; Watchtower, Gatehouse, Barracks; Boathouse. Function-first programs (spaces before shell) exist only for **Smithy, Market Hall, Stable, Gatehouse** (`FUNCTIONAL_PROGRAMS.md`). Regional contexts:
- Lowmark: Brookhollow, Crestbridge, Ashenstead, Greyharrow, rural.
- Thornfell: Stonewake, Highsteads, Passwatch, ridge.
- Mire: Sorrowmere, Marshfall, Griefwatch, Rootrest.

The mapping below is a set of **requests** for the Director and Sol to accept, change or reject. It is not a prescription.

| Narrative need | Nearest existing type / language | Note |
|---|---|---|
| Crestbridge granaries, undercroft (P02 A–C) | Grain Store; Warehouse | Undercroft and hill passage are interiors and must be hand-authored. |
| Crest Hall (P02; Act III §10.3) | Assembly Hall; Gatehouse/Barracks massing | The Lowmark language treats the Hall as "exceptional infrastructure", a compact defended administrative mass. Its interior and water-gate basin are outside tool scope. |
| Brookhollow flood shelter (empty grain warehouse), docks, Drowned Lamb, shops | Warehouse; Boathouse; Inn; Shop/Merchant House | Cellar and tunnel (P18) are hand-authored. |
| Drowsebank Mill (P11) | Miller | `REGIONAL_GRAMMAR.md` says a mill wheel is a design hint **not implemented**. `WORLD_ARCHITECTURAL_LANGUAGES.md` (0.4) says "Lowmark mill wheels and raceways ... are generated". **Question for Sol:** which statement is current? |
| Forge under the bridge arch (HS) | Smithy (functional program) | "Under an arch" placement is not a generator feature. |
| Greyharrow bell tower, militia gallery (P05, P25) | Watchtower | Multi-level interior is hand-authored. |
| Watchers' Lantern Post stone shed (P21); Reedmere lantern store (P06) | Workshop / Warehouse / Watchtower | Fit is uncertain; request. |
| Hollow Lock sluice-house (P09); Bramblelock; Sluice Shelter (roofless, P15) | — | **Gap G-1:** no lock, weir, sluice, bridge, ruin/roofless or wall type. |
| Reedmere stilt huts, plank walks (P06) | Mire language (piers, braced decks, supported links) | **Gap G-2:** the Lowmark language has no stilt treatment. Using Mire construction for a Lowmark fen hamlet is an art-direction choice for the Director. Settlement-scale walkway networks are not generated (decks and links are per building). |
| **Mire:** Sorrowmere raised ways, longhouses, register room | Longhouse; Assembly Hall; Mire language | **Gap G-3:** walkway networks between buildings are not a generator output. |
| **Mire:** Marshfall stilt houses, peat yards, smoke sheds | Cottage/Longhouse (Mire piers); Workshop; Barn | — |
| **Mire:** Griefwatch vigil hall, closure gate, Bannerline palisade | Assembly Hall; Gatehouse | Palisade is not a type. |
| **Mire:** Blackwater Landing boat shed; Hushed Granary (raised emergency store) | Boathouse; Grain Store with Mire piers | — |
| **Mire:** Rootrest root-sheltered homes | — | **Gap G-4:** footprints are orthogonal RECT/L/T/U only. Root-sheltered or organic forms are outside scope. |
| **Mire:** Chapel of the Sinking Star (MP13: roof lantern line, nave, vestry, crypt, staged drainage) | — (Assembly Hall is the nearest civic mass) | **Gap G-5:** no religious type, no partially submerged or sinking state, and no interiors. The Mire language reserves sunken wartime structures "as partially submerged ruins, not as the ordinary current house foundation". This looks like a hand-authored landmark; that is a request, not a ruling. |
| **Thornfell:** Highstead longhouses, Passwatch gate/palisade, watchposts, Stonewake assembly, Black Glass Hostel, muster hut | Longhouse; Gatehouse; Watchtower; Assembly Hall; Inn; Barracks | Rope/chain bridges, cliff stairs and terraces are described in the Thornfell language. They are not standalone types. Whinstone Store (TP08) is a cave. |

**Materials.** The 100 masters in `MEDIA/Materials/` are **original grayscale starting points for hand painting**. "No baselines have been hand-painted or accepted as final production art yet." The iPad device check is pending (`MEDIA/Materials/PAINTING_CHECKLIST.md`; `README.md`). Region fit and material use are "art-direction interpretations. They confer no new resources, recipes, trade routes or canon." Masters relevant to the fen and the Mire include Reed Thatch (010), Clay Wattle and Daub (046), Wattle Lattice Infill (047), Reed Keyed Plaster (049), Reed Mat (071) and Peat Cut Face (089) (`INDEX.md`). The generator atlas and the painting library are **separate systems**. A library binding is an explicit artist step (`ARCHITECTURE_PIPELINE.md` "Material boundaries"). **Visual style, palette and final finish belong to the Creative Director.** Nothing in this register selects a material or look.

---

## 3. Questions this register hands to the Director and Sol

1. TC-01/02/03/05: the Crestbridge Hall / river / granary / Depot arrangement. Sol and this register agree it is the next consequential ruling.
2. TC-09/06: the order and separation of Cut mouth, orchard towpath, Bramblelock and the Drowse spur.
3. TC-13: which water Whisperflow Landing fronts; the western arm reading; the far-bank settlement (POI §7 Q3).
4. TC-15: the Rebirth Fields' extent and elevation relative to the Cut.
5. TC-11: the fen outlet's quest-state interpretation.
6. §2: the mill-wheel documentation discrepancy (for Sol); stilt language for Reedmere; whether the Mire chapel and walkway networks are hand-authored or tool requests.
