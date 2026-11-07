# Lowmark v1 — POI and Zone Requirements

**Status:** Gameplay Designer requirement set for level design (Master Assistant Protocol §4.4), Batch 4 of the Lowmark v1 production plan (bible §12; "Lowmark v1" is the label of the first internal production milestone, not a release, CDR-3). It turns every place authored in the Lowmark narrative packages into level-design requirements: subzones, routes, POI sub-spaces, interaction objects, quest-state props, NPC presence and relative placement. All places are **[NEW]** unless canon in the region dossier, and nothing here is canon until the Director promotes it. **[PROPOSAL — DIRECTOR]** marks consequential choices. **MAP VERIFICATION REQUIRED** marks every place where geometry matters (bible D-5); no quest logic depends on distances.

**Sources:** bible §4 (POIs, subzones), §5 (cast), §6–§7, §9; The True Line §5; Act I §A5/§B5/§C5; Act II §GL.4/§GL.6/§TF.4/§DK.4/§MN.4/§BF.4/§BF.7; Act III §10.3/§11.3/§12.3/§E.1; the three side-quest files' place tables; Phase 1.5 §2–3, §10; Phase 1.3 §1, §6; `UNITY/README.md`.

**Companion:** `04_CONTENT_PRODUCTION/Enemies/Caelmor_Lowmark_Encounter_and_Enemy_Requirements.md` (encounter ids, drift-site ids, arena combat rules).

**Canonical rulings applied (review passes):** Reed Stalkers first appear in Night Bridge; Fen Watch unlocks after MQ5; the Ash Hound burned-culvert den (P14 B3) belongs to MQ3 only; The Wrong Culprit unlocks after MQ2 at the Heartlands–Ashenstead edge; Old Lantern permanently quiets Old Lantern's bend; all enemies, human included, are defeated at 0 HP with the ordinary defeat presentation (CDR-1, 2026-11-03; no downed humans, no tied props; SX-1 Joss and SX-2 Sallow are quest-scripted outcomes on defeat); every encounter space accepts melee or ranged (CDR-2); the Whispering Door's farm is referred to as **the Whispering Door farmhouse** (rename pending).

---

## 0. Level-design constraints from the current runtime

| Constraint (source) | Level-design rule |
|---|---|
| Click-to-move over a host-validated NavMesh; Shift sprint; no jump (README) | Every required route, objective and combat "safe ground" must be NavMesh-reachable by walking. Clicks on non-terrain are rejected, so every interaction point needs walkable ground within reach. |
| Agility triggers approved, **not built** (Phase 1.3 §1; README) | Every agility trigger in this file has a **walkable fallback** that is the critical path until triggers are built. Never put a required objective behind a trigger. |
| Flat fixture ground; **no multi-level traversal or off-mesh links yet** (README) | Vertical spaces (Hill Depot, culvert shaft, bell tower, bridge underside, falls path, Lock floors, Crest Hall stair, farmhouse cellar, tree fork) need multi-level NavMesh with stairs or ramps. Ladders and rungs are **interaction-driven moves** ("Use the rungs" places the player at the far end) until off-mesh links exist. Flag each to Systems. |
| Interaction needs reach and line of sight (README) | Channel points used under attack (cranks, levers, boards, withies, winches) need a clear standing pad (≥ 2 m) facing the object with nothing between. |
| Player camera only; collision-corrected; no automatic adjustment (Phase 1.3 §1) | Tight spaces (warren, culvert low run, drain, listening-seat alcove) must read at default zoom with the camera colliding cleanly. The Uphill Canal occlusion requirement (P28) is load-bearing. |
| Wading | Shallow water (ankle to knee) is NavMesh-walkable with a slow volume. Deep water is non-navigable (clicks rejected) and is never a knockback destination (kerbs, banks or wade-depth basins). |
| Ranged is a core combat skill (CDR-2) | Every arena works for melee and ranged. No arena gives a ranged player a safe perch the enemy cannot reach (raised footings, plinths and stakes stay reachable by the enemy; deep sides and far galleries are not standing spots). Ranged is never required. |
| Defeat presentation (CDR-1) | No "tied", "bound" or "downed" human props anywhere; defeated enemies fade on the standard corpse timer and nothing persists into later visits. SX-1 (Joss, M05 D) and SX-2 (Sallow, P02 Gate Landing) need only a standing spot for the NPC the quest spawns after defeat. |
| Per-player state (bible §9) | Quest-state props are client presentation keyed to the local player's state; each package's shared-world fallback applies. |

---

## 1. Hydrology and macro layout [PROPOSAL — DIRECTOR; MAP VERIFICATION REQUIRED]

The narrative fixes only four facts (bible §4.1): Whisperflow is downstream of where the Relief Cut rejoins the river; the Cut rejoins below Crestbridge; Ashenstead and the Path of Unburnt Reeds lie between the farmland and Veilwater; Stillwater Fen is where the river slows and spreads. Act I §C5.3 leaves "how the Cut bypasses Crestbridge's tolls" to this package. The chain below satisfies every package with no text change.

**River chain (upstream → downstream):**
`Veilwater Falls (uplands) → Stillwater Fen (river spreads; Reedmere on its landward shore) → river leaves the fen → Crestbridge (toll bridge; granaries; Crest Hall water-gate; Hill Depot chute backwater just below the toll line) → Drowsebank Mill leat and Drowse spur (joins the lower Cut) → Relief Cut mouth (Cut rejoins) → orchard floodplain (towpath under the dike) → Bramblelock Weir (head of the split for orchard Braids and the Flats ditches) → Whisperflow Run bend and Whisperflow Landing (Drowned Pier) → Brookhollow docks → Greyharrow side branch (Greyharrow town, bell tower, winter boom) and Greyharrow Reach (chain ferry) → region exit.`

**The Relief Cut** runs **straight** from the fen's deep pools, with the **Hollow Lock** near its fen end, past the western edge of Ashenstead Fields, to its mouth on the river below Crestbridge. It is visibly wrong against every natural line (TL-style unease, Act I T4).

**The flush and the barges (how the toll is bypassed).** A flush releases fen water from the Hollow Lock down the Cut; it leaves the Cut mouth and runs downstream over Bramblelock and on to Whisperflow ("fen side first", Act I HW synthesis; flow-table BF.7.3). A laden barge staged **below** Bramblelock (crew paid and goods staged at the Drowned Lamb's river door in Brookhollow, UL) is poled **upstream** on the raised water: over the weir crest, along the orchard towpath, over the Cut-mouth silt sill, up the Cut and through the Lock into the fen, then out by the old wartime convoy route to the outside buyer. It **never passes under Crestbridge**, so no toll or inspection. Grain reaches Brookhollow from the Hill Depot chute by night skiff below the toll line. The pulse supplies depth over the weir and sill, not current.

**Side relationships:** Ashenstead Fields sit on the Cut's landward side (Rebirth Fields flood by Cut backwater seepage, MQ5). The Whispering Door farmhouse is on the Heartlands edge nearest Ashenstead (its drain reaches the guide-line outfall). The Path of Unburnt Reeds runs from Ashenstead along the fen's edge to Veilwater. The Watchers' "far leg" runs from Whisperflow up the river side to the fen edge.

---

## 2. Subzones (bible §4.1, D-9)

Each subzone has a **near band** (reachable early) and a **far band**. This resolves the tier mismatch between bible §4.1 and early side-quest gates (Enemies §12 I-15).

| Subzone | Contains | Tier: near / far | Tone | Fauna and families | Ambient signature |
|---|---|---|---|---|---|
| **Greyharrow Heartlands** | P01 Brookhollow, P02 Crestbridge, P04 Whisperflow Landing, P05 Greyharrow, P11 Drowsebank Mill, P12 Drowned Pier, P18 Drowned Lamb cellar, P19 Ferry Camp, P25 bell tower; minor sites M01, M02, M04 | Early / early | Working river country: queues, docks, tallies, chalk; dry humour; the river as employer and threat | Shallows vermin, boar, geese; Smugglers (Lamb, Reach); drift only at the farmhouse cellar and Whisperflow-side bends | Water lap, crews calling marks, carts, gulls; Whisperflow dead-spot audio holes |
| **Brackenford Woods** | P07 Hill Depot, P08 Bramblelock Weir, P15 Sluice Shelter, P16 Floodplain Orchards, P17 renewal coppice, P28 Uphill Canal | Early / early–mid | Managed land: coppice tallies, immaculate ditches, wartime stone under growth | Field Goblins (depot), Mud Pipers (reed margin), drift (orchard pool/dike), elk (flood-driven) | Coppice birdsong, sluice drip, reed hiss that is almost words |
| **Ashenstead Fields** | P03 Ashenstead, P13 Guide-Line Culvert, P14 Furrowed Plains trench line, P20 burned barns, P23 watergarden and Ember-Well, P24 Mantle Shrine, P26 Circle of Unburnt Reeds, P27 Twice-Burned Tree; minor sites M03, M06 | Novice at the Heartlands–Ashenstead edge (P20, M03, Joric's plot, P03 village) / Competent interior (Rebirth Fields, P13, the Path) | War scars and memory; rebuilt on burned ground; grief beside work | Ash Hounds, Field Goblins (P20), Reed Stalkers (culvert), drift (watergarden outlet, Mantle channel) | Wind over scorched rye, rooks, the Ember-Well bucket rope, candle stands |
| **Riverglass Banks** | P06 Reedmere, P09 Hollow Lock, P10 Relief Cut, P21 Lantern Post, P22 Widow's Step, P29 Veilwater Falls and Listening Steps, **P30 Stillwater Fen interior (proposed)**; minor sites M05 (far leg, Old Lantern's bend), M07 (Reed-Lantern Bend) | Novice–Competent fen edge (P21, P22, P06 shore, P10, P09, M05, M07) / Advanced deep fen (P30, FW done stretch) | Mist, lanterns, the fen holding its breath; Watchers' patience; the Steps' clarity | Drift and lantern-drift, Reed Stalkers, Smugglers (Lock), Stillwater Serpents, the Muster | Frogs that stop; lantern hooks; the falls felt in the chest; after MQ11 the fen's long exhale |

---

## 3. Traversal route plans (Phase 1.5 §2.3: 3–4)

| Route | Path | First used | Character | Gates and shortcuts |
|---|---|---|---|---|
| **R1 The River Road** | Brookhollow road head → Whisperflow Landing (A) → Brookhollow → river road north to Crestbridge; south to Greyharrow and the Reach | TL | Open, social, readable: markers on every crossing (inspectable after TL) | Whisperflow crossing (TL; Maelin's crossing interaction, night variant in MQ12); Greyharrow ferry (NT) |
| **R2 The Towpath and the Cut** | Crestbridge → Hill Depot river ledge → Drowsebank → Cut mouth → orchard towpath → Bramblelock Weir; and up the Cut straight to the Hollow Lock | MQ4 (chase); SM ledge | Linear, momentum, the wrong straight line; wartime mile-stones | Hill Depot ledge shortcut (after SM boss); weir-top gap and towpath fallen tree (agility; fallbacks: footbridge 20 m downstream, dike top); Cut sealed by stop-planks at MQ12 |
| **R3 The Fields and the Reeds** | Heartlands farms → the Whispering Door farmhouse → Heartlands–Ashenstead edge (WC smallholding, P20) → Ashenstead → Rebirth Fields → Path of Unburnt Reeds → P26 → P24 Mantle Shrine → Veilwater Falls (P29) | WC, MQ5, MQ8, MQ9 | Wide fields narrowing to a reed corridor taller than the player; pilgrimage at the end | Uphill Canal Hazel Culvert shortcut (UC: Brackenford orchard side ↔ Ashenstead Fields edge); falls climb (agility; fallbacks listed at P29) |
| **R4 The Watchers' Leg** | Whisperflow → the far leg (M05) → Old Lantern's bend → Lantern Post (P21) → Reed-Lantern Bend (M07) → Widow's Step (P22) → Reedmere (P06) → fen causeways | MQ3, OL, ME10, MQ11 | Dusk route; lanterns at intervals; patrol posts with waymark notches | Lessa's kept path (FW reward; optional MQ11 lane); the Cutters' Causeway (reopened MQ11; closed again under Seal/Shared) |
| *Shortcut S1* | Crestbridge underside (NB): south abutment → piers → north stair near Crest Hall water-gate | NB | Night climb among nests | `NB_UNDERSIDE_OPEN`; optional MQ10 approach to the water-gate |

---

## 4. POI requirements

Format per POI: required areas (sub-space ids are the packages' own letters), environmental storytelling, NPCs by phase, interaction objects (**I** inspect · **C** channel · **K** carry · **W** watch/wait · **A** agility with fallback), quest-state props, uses, and map notes. Phases: **TL** · **Act I** (MQ2–4) · **Act II** (MQ5–9) · **Act III** (MQ10–11) · **Post** (MQ12 on).

### P01 Brookhollow — Settlement, Heartlands

| Field | Requirement |
|---|---|
| Areas | Docks and drying racks; high street; Ottilie's glass shop; Flow-Mender shop; the **Drowned Lamb** taproom (A) and back room (B) above P18; **flood shelter** (empty grain warehouse on the high street: shelter B, field kitchen C under the loading door); **low lanes** (A, floodable); **reed margin** below the docks (D open section, closed nesting section with rag stakes; E recovery shallows); **tan-yard** at the settlement edge (gate A, pits B, bark brake C, workroom D, backwater E with drawing-steps, lane of ring-stripped trees G); **keepers' river post** on the docks (UL G); Nan's worn dock-edge step (VK) |
| Storytelling | Chalked ring doors (empty, everyone out); a chair floating upright; shelter wall of chalked flood lines with seasons (oldest highest; tonight's lower); knife-mark lunch tally beam (ME02); NO RIVERGLASS FOR CELLARS sign; NO HIDES AFTER DARK; the crossed-scrapers strap on a nail by the tan-yard gate (after BP); the Lamb's empty head-of-table chair |
| NPCs by phase | TL: off-stage. Act I: Ottilie, Kell Ashby, Nan (FK), Mott Pask (landlord), Sallow's crew at the taproom table (after MQ4), Rhosyn in the cellar (UL), dock workers. Act II: Ottilie (MQ7 bowl). Post: Rhosyn (if UL), Kell (commission), Ottilie (MQ12 optional station) |
| Interactions | I: flood lines, beam, bowls (ring, window; DK), drying ledge of bowls; C: light the fire (3 s), break bark, charge the pit, add a mark (2 s); K: dry slats (loft ladder is a walkable stair), spoiled bark armfuls, Ottilie's crate (UL errand); W: midday window (ME02); stations: shelter Cooking (public after FK), tan-yard Leatherworking |
| Quest-state props | Shelter families present/leaving (FK); step waterline one step higher after the FK hush; pit liquor colour (BP); ring-stripped lane props by `BP_STRIPPED_*`; strap on the gate (after BP); Lamb crew presence (post-MQ4 to MQ10) |
| Used by | FK, BP, UL, DK (bowl), VK (Nan), ME02, MQ6 lead-in, MQ12 |
| Map | Low lanes must sit below the high street and flood visibly; reed margin downstream of the docks; tan-yard washing channel led off and back into the river through a settling pond. MAP VERIFICATION REQUIRED: distance and side relative to Whisperflow |

### P02 Crestbridge and Crest Hall — Settlement, Heartlands

| Field | Requirement |
|---|---|
| Areas | **Bridge** (dwarven-reinforced span, south toll with tally table, north end); **waiting wall** worn smooth at child height (faces the granary yard and the south toll); **granary yard** (A: hoists, barrel-head desk), **tally room** (B), **undercroft bays** (C: 12 swept, 3 full), **hill passage** (D, to P07); **forge** under the first arch (HS: hearth, testing horn bench, quench trough fed by a river channel, rejects rack, refurbish queue, iron tie-ends in the abutment; optional service ledge E); **underside** (NB: crew stair and winch B, pier 1 cutwater ledge C, pier 2 reed island and war face D, arch 2 soffit with the ceiling of marks E, pier 3 cramps and nest F, north stair G); **Crest Hall** (hall steps A, Long Hall B with floor-grates, Tally Stair C, Records Undercroft D, Granary Passage E with cistern and sack pegs, Water-Gate Hall F, Gate Landing G ~14 × 8 m, Keepers' Yard H); **Marrick's granary** door (MQ12); **keepers' hall** wall (MQ12) |
| Storytelling | Two matching tally racks and a bare ledger shelf; dust outlines of sacks; HILL GATE chalk line; generations of tally notches on the stair hoardings; RELIEF — FENMERE — LOT brick infill; the steward's chair the same height as every other (someone measured); Board bench cushioned; crew chalk under the span ("LOOSE", a crossed-out frog); THAW AFTER PEACE patch; day-count strokes in the soffit |
| NPCs by phase | Act I: Corvin (tally room), Hesketh and Marrick `[ANTAGONIST]` (yard glimpse, SM S08), Aldric, porters, Wynn (hill road yard), Brigid (forge), toll keeper, Orla Wickett, Tam Varley, winch-hand (NB). Act III: Hollis, Hesketh, Aldric, Marrick, keepers, households along the wall (MQ10 evening), Sallow (gate landing), Rhosyn (if UL), Tovin. Post: Wynn at Marrick's granary, keepers, Brigid and Hesketh/successor (commissions) |
| Interactions | I: racks, bays, ruts, goblin hole, stencils, ring-test bars, repair faces (with rake-light channel 3 s and rubbing 3 s), table chips; C: fire-line cut (3 s), scuttling-line re-make (2 s ×3), water-gate crank (5 s), haul the crewman (3 s), relight lantern (2 s), forge chain, `cut_nest` (3 s); K: record bundles (smoulder timer ~90 s), soaked sacks to fire-lines, rubbing cloth (light carry), evidence chips to the long table; W: hanging platform rides (6 s each); A: NB step-down, gap hop, cramp-ladder, beam walk, step-up (fallback: hanging platform on a rail, or fixed crew scaffolds with ladders) |
| Quest-state props | Grain carts by `LM_GRAIN_ROUTE`; third tally stick on the plain rack (after SM); Crest Hall night state (fire volumes, lighting) during CR; singed records; chips on the long table; water-gate up/down; Tovin's sheets on the keepers' hall wall (named/unsigned); Marrick's granary sealed, restitution sacks (MQ12); platform left rigged and chalked ledges (after NB) |
| Used by | SM, HS, NB, CR, RR, Honest Steel cameo (Corvin) |
| Map | The water-gate must open onto the river **above** the Cut mouth (Act III §10.3). NB's north stair must emerge close by the Crest Hall water-gate wall (MAP VERIFICATION REQUIRED). The Gate Landing basin must be **wade-depth with steps at each end** (Sallow's Shove). Floor-grates in the Long Hall must carry water-gate audio (CR strange moment) |

### P03 Ashenstead — Settlement, Ashenstead Fields

| Field | Requirement |
|---|---|
| Areas | Village green and **Ember-Well** (GL A); Annelise's watergarden (P23); Elspeth's station; the **Rebirth Fields** (GL C communal strips, D remembrance circle of nine unlike stones at the low point, F field hut with bench facing the circle, G boundary stones in hedge banks, H reed edge toward the Path); dig points along the guide-line; **Joric's plot** (E) at the Flats edge (shared with UR, see M06) |
| Storytelling | BEASTS ONLY TILL IT SETTLES / SETTLES WHAT on the well cap; rotted seedlings in straight bands across the furrows; a ruler-straight rush line; grey silt ring at one height on every circle stone; furrows bending round boundary stones; re-sowing tallies on the hut door; slanted reed bundles at the drain |
| NPCs by phase | Act I: households, Annelise, Elspeth (after MQ3), the Holt family (CN). Act II: Joric, Annelise, field crew and foreman, Sedge as an unmarked "Reed-cutter" at H (GL S03b), Elspeth. Post: Joric, Annelise (MQ12 station), Elspeth per `LM_FEN_ENDING` |
| Interactions | I: rush line, sunken furrow, soft ground, boundary stones (guide-line stones region-wide after MQ5), warm/cold bucket; C: dig (3 s ×2 + clear 3 s) ×3, cap, grate clears, ditch lengths, dike tamps; K: circle stones with **facing check** on set-down, turf sods, stakes; W: field-hut bench keep-watch (backwater dusk) |
| Quest-state props | Field presentation by `LM_FIELD_FIX` (circle dry / bright ditch across the plot / long mirror of water behind the dike, strips flooded a season); Ember-Well steam (dusk window only) |
| Used by | MQ5, MQ7 lead-in, CN, TB (household bark), UR, WC lead, MQ12 |
| Map | The circle must be at the field's **low point** and Joric's plot **lower than the circle**; field drain runs toward the reeds and the Path (MAP VERIFICATION REQUIRED) |

### P04 Whisperflow Landing — Micro-settlement, Heartlands (start)

| Field | Requirement |
|---|---|
| Areas | TL A road head, B tollpost and slate, C low cart-stand, D crew fire, E marker bank (five grey posts, one pale yellow), F reed walk (goose nest; root-path fallback via mud shelf and fallen driftroot), G old footing (Marking Stone; dead-spot audio), H drowned pier (P12), I renewal coppice edge (P17), J high landing terrace with old fire rings; ME01 safe-bank shallows; ME08 lagging pool upstream of G; far-bank landing (MQ12) |
| Storytelling | The pinned EMERGENCY PROVISION notice through the chalked CROSSING SHUT; Crestbridge tally marks on sacks; child's chalk game; soaked torn boot; drag marks upstream; old fire rings at the high landing ("used for this before") |
| NPCs by phase | TL: Hollis, Maelin, Dace, Wynn, Nan, Tovin, Ansel (night). Post-TL: Maelin's crossing; children (ME01); Tovin sketching at ME08 if `TL_TOVIN_TRUSTED`. Act I: crews (`riverfolk` second-post bark). Post (MQ12): Maelin, crews, lantern-bearing crowd, Dace (if NT) |
| Interactions | I: posts (marker reading enabled region-wide after TL), stone, pilings; C: clear silt, cut notch, seat post (3 s each); K: weathered post (quest item), 3 sacks, Nan's trunk; W: night camp; A: root path step-down (fallback: reed path through the nest radius) |
| Quest-state props | Yellow post / new post; notice on/off; chalk ring; five posts with unlit lantern hooks and the stone's tender-marks plus the player's mark (MQ12 `RR_MARK`) |
| Used by | TL, ME01, ME08, OL (far leg start), MQ12 |
| Map | **Road-head sightline** (see §6.3). The far bank and its settlement are **MAP VERIFICATION REQUIRED** (TL §14 item 4). The landing must be a short walk down from the Brookhollow road |

### P05 Greyharrow — Micro-settlement, Heartlands

| Field | Requirement |
|---|---|
| Areas | Fortified side-branch town; militia lookout gallery; minor docks; tower square (P25); **winter boom** across the side-branch dock mouth (pin-posts, pole rack; VK); Sayer house; Coombe ice-pole side channel and jetty; bell-tower foot; side-branch bank downstream of the docks (M04, BW) |
| Storytelling | Teague's grievance list; Rope Day trestles and bunting; the boom holding rotten ice; song-book with a sacking cover |
| NPCs by phase | Post-TL: Teague, Merrin, Tamsin, Sayer and Coombe families (VK after MQ3), BW households. Act I: Maelin's crews (second yellow post at the Reach) |
| Interactions | I: song-book, roster; C: work the floes (3 s ×3), boom pins (performance); W: VK performance event |
| Quest-state props | Ringers' slate on the Sayer mantel if `SB_TO_FAMILIES`; boom open after VK |
| Used by | SB, VK, BW, NT (militia), Night Ferry lead |
| Map | Must sit on the **side branch**, not the main river; bell louvres overlook side-branch water |

### P06 Reedmere — Micro-settlement, Riverglass Banks

| Field | Requirement |
|---|---|
| Areas | Stilt huts on plank walks; **Watchers' lantern store** (loft = Elspeth's trance-care station); tally board by the steps; cutters' huts and eel traps; **warning post** (FW A: horn, slate DONE BELOW THE WITHIES); **withy line** across the channel mouth (B); osier stools (C); **done stretch** (D, off-limits); cutters' places (E); **the staging** (F: reed-mat floor ~20 × 14 m, four staked timber discs 2 m across, pool kerb, landward shallows strip); **kept path** (G, reed-head knots); **cutting grounds** with three outlying huts **Hookreed**, **Two Posts**, **Far Racks** (MQ11 B); **Cutters' Causeway** mouth with Lessa's cloth-wound stake (MQ11 C) |
| Storytelling | Treatment cot on a porch; Wenna Tull stacking bundles; every lantern hook empty on vigil night; names crossed off the tally board; kettle still steaming at Two Posts; unlaced boots side by side at the Far Racks; snapped withies floating |
| NPCs by phase | Act I: Lessa, Elspeth, Orrin and Wenna Tull (MQ3). Act II (FW after MQ5): Lessa, Ivo Teasel and cutters, warning crew. Act III: Maelin's crews, Watchers, Elspeth, Sedge on the lantern-store steps, route keepers, evacuees, Joss (if `OL_JOSS_IN`). Post: Lessa and Elspeth per `LM_FEN_ENDING` |
| Interactions | I: slate, Marking Stones; C: set withy (2 s), smoke a trance follower (2 s), lead out (3 s), stand the vigil; K: lantern string (followers), Watcher smoke-pot (refill at 6 lantern racks); W: vigil fire |
| Quest-state props | Withy line state; Lessa's stake out/back by ending; lantern hooks filled during MQ11; Ivo's skiffs on the kept path by `FW_BED_SHARED` |
| Used by | MQ3, FW, MQ11, MQ12 station, W-02 (Old Mud) |
| Map | On the fen's **landward edge**; the three Braid gates run in a rough line from Reedmere toward the centre; the staging sits at a deep pool's edge (MAP VERIFICATION REQUIRED for the 20 × 14 m staging) |

### P07 The Hill Depot — Cave / war site, Brackenford Woods (first dungeon)

| Field | Requirement |
|---|---|
| Areas | E Sorting Hall (vaulted, rack rows, rake-bed straw; collapsed-rack agility to a gallery ledge, fallback through F); F Twine Door; G Low Tunnels with **two parallel routes** (bin route with side holes; root route through driftroot, cuttable) rejoining at I; H Larder (optional); I Harrow Run (marked shadow strip; ramp to the trapper ledge); J Heaps and Throne (sack throne, bin on a jack over it, sack nests as summon points); K Chute Gallery (door barred **from the chute side**; gantry; RELIEF CUT stencil; Marking Stone at shoulder height); L chute lip and river ledge (mooring ring; short walk down to the bank and hill road) |
| Storytelling | Two layers: orderly wartime stone (stencils RELIEF — ROTATE BY LOT, numbered bays) and goblin improvisation (twine, pans, whitewash handprints at goblin height, a smiling face drawn in grain dust on the scythe); goblin hoard of shinies (nothing evidentiary); twelve countable sacks |
| NPCs | Corvin's porters arrive behind the player after K (SM S07) |
| Interactions | I: traps (reveal + disarm), heaps ×3 (count), gallery ×3, slip pickup; C: cut twine (1.5 s), unbar (one side only, persists); A: rack ledge (fallback twine door) |
| Quest-state props | Disarmed traps per player; heap-boss replacing the Sack-King; ledge shortcut open after the boss |
| Used by | SM; revisitable dungeon (W-03) |
| Map | Hill behind the granaries; chute drops to a slack river **backwater below Crestbridge's toll line** (§1). Low ceilings rely on camera collision; no crouch. Multi-level NavMesh needed (ledges, ramps). MAP VERIFICATION REQUIRED |

### P08 Bramblelock Weir — Ruin / war site, Brackenford Woods

| Field | Requirement |
|---|---|
| Areas | W1 the weir (broken stone walkway top; weir-pool marker with notch), W2 convoy stones along the wall (thirteen, blank newer stone, fifteen), W3 watch bench with lantern hook; T1 weir walls (weir-top gap agility; footbridge fallback 20 m downstream) |
| Storytelling | The missing lot: a blank stone in plain mortar between 13 and 15 |
| NPCs | Act I: Maelin on the weir wall (MQ4). Post: none |
| Interactions | I: marker reading, convoy stones; W: keep watch (per-player presentation hour); A: weir gap (fallback footbridge) |
| Quest-state props | Pool flat and reading under the notch after MQ4 (site quieted) |
| Used by | MQ4, MQ11 evidence (convoy stones), mystery ledger |
| Map | On the river **below the Cut mouth**, at the head of the orchard/Flats split; the barge must pass within ~6 m of the bench |

### P09 The Hollow Lock — War site / bandit site, Riverglass Banks

| Field | Requirement |
|---|---|
| Areas | L1 walled yard (crew shed, lantern rack with hoods, cut chain on gate stones); L2 lock chamber (barge moored at the lower gate); L3 winding floor (gear, crank platform over the chamber; far gallery **not connected** except by the lock gates); L4 post store; L5 tally room with strongbox; L6 slack gate (silted, fresh spade marks); L7 roof walk by stair; far stair to a skiff at the lower gate |
| Storytelling | Gear greased this week over war grease; stack of yellow posts notched a hand high; chalk crossings board (Whisperflow ✓, Greyharrow Reach ✓, Drowsebank tail —); flush nights scratched into the beam; counterweight carved like a Marking Stone; warm cookpot |
| NPCs | Act I: Sallow (across the chamber, unreachable), Rusk and crew (creatures only; CDR-1), then Maelin's skiff, Ansel, keepers at dawn. Post: keepers (inspection if chained); seal crew at the Cut (MQ12) |
| Interactions | I: gear, posts, board, counterweight, slack gate, chain; C: pull the hoods (2 s), crank in 3 × 5 s persistent segments, smash (3) or chain (2) the gear; K: crew chain, a pre-notched post (flavour) |
| Quest-state props | Gear smashed/chained by `LM_LOCK_STATE`; chain later cut (chained branch, Act II); posts impounded |
| Used by | MQ4, MQ10 (chips), Act II seed (slack gate) |
| Map | Up the Cut toward the fen. **Roof-walk sightline to Stillwater's fog wall** (§6.3) |

### P10 The Relief Cut — War site (linear), Riverglass Banks

| Field | Requirement |
|---|---|
| Areas | T2 orchard towpath (fallen tree agility, dike-top fallback); T3 Cut mouth (silt sill with pole-scrapes; RELIEF CUT stencil); T4 the straight (towpath, silted culverts mouthing water, wartime mile-stones) |
| Storytelling | A straight stone-faced channel at an unnatural angle "like a ruler laid on a drawing"; mile-stone scratched TOO FAR |
| NPCs | Act I: lookouts. Act II: keepers at the Cut watch (MQ6). Post: seal crew with stop-planks (Hesketh if stood down; Sallow's men if `CR_CREW_LENIENCY`) |
| Interactions | I: stencil, mile-stones, sill; trail-clue volumes (wake slap, leaked grain, hooded light) |
| Quest-state props | Stop-planks and earth bank at the mouth (MQ12) |
| Used by | MQ4, MQ6 (Drowse spur joins the lower Cut), MQ11 (sealed), MQ12 |
| Map | 60–90 s walk on the straight between the mouth fight and the Lock (pacing beat). Must bypass Crestbridge (§1) |

### P11 Drowsebank Mill — Ruin / worked site, Heartlands

| Field | Requirement |
|---|---|
| Areas | A mill yard and pond bank (Tovin's bench facing the water); B ground floor (two millstones, hoist trap, **seven chalk-numbered sack bays** along the race wall = puzzle slots, tool rack with painted outlines, stain lines, shift board); C race and paddle gate (near crank mill side; **far crank across a narrow footbridge** on the pond bank); D tail race and tail door; E beam loft with a floorboard gap viewing B and C; F mill-smith's corner; G far bank spill weir with two extra boards; H the Drowse spur |
| Storytelling | Ducks avoid the race-gate corner; fresh pry scars on the pawl; tail-door damp patch from the wrong side; Imber's painted height bands |
| NPCs | Act II: Imber Cobb, Tovin (runs for keepers before dark), crew at night, keepers at dawn. Post: Imber; Tovin (if credited, cameo) |
| Interactions | I: gate, rack, stains; C: seat the gate, re-seat pawl (2 s), wind down (3 s/band), spill boards (2 × 3 s), hoist lower, ordered-slot sheets (7), cook at the hearth; K: salvage beam brace; W: loft keep watch |
| Quest-state props | Race-edge flood decal by `TF_MAX_BAND`; sheets laid in order; gate locked (after TF) |
| Used by | MQ6, micro-event (bible), ME08 echo |
| Map | Between Crestbridge and the Cut mouth; tail race reaches the **lower Cut by a wartime spur** (MAP VERIFICATION REQUIRED). Pond-bank volume for the lag effect within 15 m of the water |

### P12 The Drowned Pier — War site, Heartlands

Wartime ferry pier stumps just under the surface **directly on the line the false post marked**; Dace's holed skiff caught on them; TL-E3 shallows. **I** pilings (`TL_EVIDENCE_PILINGS`). Downstream of the footing, wadeable. Used by TL.

### P13 The Guide-Line Culvert — Cave / war site, Ashenstead Fields

| Field | Requirement |
|---|---|
| Areas | I1 entry shaft (iron rungs, 4 m; rungs interaction); I2 long run (knee-deep, head-high, light shafts every ~10 m, **side ledge**); I3 low run (~25 m, ceiling just over head height; water rises a hand twice, telegraphed by a 3 s gurgle; stoop-through agility optional); I4 marker chamber (two channels meet; CLEAN WATER — THIS SIDE; hooks; bandage pins; niche of unreadable scratched marks; no light shaft); I5 reed shaft (reed curtain to the water; dry stones as safe footing); I6 grate chamber under the circle (nine bars of light through gaps between the circle stones; side culvert toward the Flats) |
| Storytelling | Field crew footsteps overhead then gone; wartime treatment-boundary markers; marks that look like letters and cannot be read (nothing reads them for the player) |
| Interactions | I: grate, cap, side culvert, marks; C: grate clears (circle fix); respawn at the shaft top |
| Quest-state props | Sunlight down the shaft after the circle fix |
| Used by | MQ5; explorable after (vermin only) |
| Map | Under the Rebirth Fields from the hedge shaft to the circle; side culvert under Joric's plot. Water volume animated in I3 |

### P14 Furrowed Plains trench line — War site, Ashenstead Fields

| Field | Requirement |
|---|---|
| Areas | B1 trough field (Mabry Gorse's stock; notched gatepost); B2 ditch from the trench line down to the river (sluice board); **B3 burned culvert** (mouth with carcass and ash plug; inner Den Mother chamber); faint trench lines under crops; side gully (Hunting flank route) |
| Storytelling | Silt ridges pointing **uphill**; reed debris on the upstream face of the sluice board; crossed notches for "ran back" nights |
| NPCs | Act I: Mabry Gorse. Post: stock drinking |
| Interactions | I: gatepost, ripples ×2; C: drag out the carcass, rake out the ash plug |
| Quest-state props | Den empty after `HW_DEN_CLEARED`; ditch runs right after MQ11 (Enemies §10) |
| Used by | MQ3 only for the B3 den (**canonical ruling**); W-04 packs roam the Flats, not B3 |
| Map | The ditch must run from the trench line downhill to the river, so "uphill" ripples read |

### P15 The Sluice Shelter — Ruin, Brackenford Woods

Roofless flood-season shelter among the orchards: child-height names scratched inside in more than one hand; bench for council talk; keepers' notice on the post. NPCs: orchard households, charter officer, roll-keeper, Elspeth, Bryn (DK S06). **W** keep watch for the backwater (DK S04). Used by MQ7, micro-event. Must be within sight and short walk of the Long Bank (P16 C).

### P16 Floodplain Orchards — Worked landscape, Brackenford Woods

| Field | Requirement |
|---|---|
| Areas | A1 berm walk; A2 timber sluice jammed by driftroot (chalk ticks "rose — no rain"); A3 root pool among six old trees; A Bryn's ditch head (RUDDOCK — TURN AT FIRST FROST); B old pear rows (the slip-flood section); **C the Long Bank** (lower dike run, worn dip, Bryn's boundary stones at each end, three stake points, two moss points); E three softmoss shrine stones (nearest the reed margin blackening); F river edge (living driftroots; one storm-thrown driftroot = gather target); G reed margin; berm shrine (respawn) |
| Storytelling | Immaculate ditches with cut-stone lips; abandoned wren's nest; brown slimy softmoss near drift; cracked riverglass bowl kept on a gatepost |
| NPCs | Act I: Bryn, Ansel (dusk). Act II: Bryn, Elspeth, charter officer, households, roll-keeper. Post: Bryn (MQ12 station) |
| Interactions | I: chalk column, moss, driftroots; C: chop jam (3 Woodcutting), haul lever (4 s), stakes, moss, hold chain end (3 s ×2); K: moss and stake bundles; W: Sluice Shelter |
| Quest-state props | Pool drained (MQ3); orchard trees recover in stages; pear rows flooded by `LM_ORCHARD_LOSS`; cold mist over two far-ditch pools until MQ8 |
| Used by | MQ3, MQ7, MQ8 (quieted far ditch), W-01 (Chorus-Piper), MQ12 |
| Map | Floodplain below the Cut mouth along the towpath and Bramblelock; reed margin between orchard and river |

### P17 Renewal coppice and household woods — Worked landscape, Brackenford Woods

Cut-and-regrow stools; crew tally stick with ribbons on this year's stools (only ribboned stools interactable); bark stripped in neat bands. Two required parcels: **Whisperflow coppice** (TL I, marker stem) and **tan-yard coppice** (BP F, coppice crew hand at the far end). Also the ribboned hedge stools used in MQ5's dike fix. Used by TL, BP, BW lead. Prop: ribbons move each season (per player).

### P18 The Drowned Lamb cellar — Bandit site / cave, Heartlands

| Field | Requirement |
|---|---|
| Areas | C stair and door-man's alcove (charcoal list); D cellar market (racks of riverglass, chiselled steel, tied book bundles; racks are cover); E Rhosyn's nook (seal press, eleven inks, names-and-places list, ledger); F river door and brick tunnel to a winch grate under the docks (crossing marker inside the mouth) |
| Storytelling | Condensation beads level across a tilted rack; red-wax buyer's marks; Ottilie's maker's dot under the wax |
| NPCs | After MQ4: door-man, crew, Rhosyn. Post: nook empty or Rhosyn (by UL choice) |
| Interactions | I: ledger pages ×3, beads, maker's dot; C: crank the grate (4 s); K: crate, ledger (light carry); challenge volumes that open dialogue |
| Quest-state props | Nook occupied/empty; skiff at the grate in the evening-bell window |
| Used by | UL, MQ10 (chip), barge staging (§1) |
| Map | Directly under P01's Drowned Lamb with a tunnel to the docks |

### P19 Ferry Camp at Greyharrow Reach — Bandit site, Heartlands

| Field | Requirement |
|---|---|
| Areas | A ferry landing (chain running taut then slack; bent chain bar); Maelin's barge at the side dock; **B cart ring** (four carts, fire, **four lantern posts marking four lanes**); C dark landing (shingle spit, water two sides); D reed-edge thieves' run; E bluff camp above (tarps, lookout stool, stolen bundles); F the reach (scour-hole boil, invisible in the dark) |
| NPCs | NT (after MQ2): Teague, two militia, Dace, Maelin, Brack, stranded workers and a household with a cradle-basket. Post: opportunists' camp (W) |
| Interactions | C: light lanterns (2 s ×4), cut mooring (2 s); K: stolen bundles; W: watches; escort stragglers |
| Quest-state props | Lit/doused lanterns gate enemy lanes; bundles returned; capsized skiff at dawn |
| Used by | NT, Act I second yellow post (bark), MQ12 (Dace) |
| Map | The ring must be readable as four lanes; the bluff must overlook the ring |

### P20 Goblin camp at the burned barns — Bandit / camp site, Ashenstead Fields (near band)

Three fire-gutted barns; scrap-armour and broken-tool nests; in the end barn the **goblin field** (stolen roots replanted in three rows in the ash; plough-blade notched at marker height). Goblin path to P27 (dropped rakes, hoe-handle ladder). Fallen barn wall next door over Joric's plot burrow (UR). Used by WC (after MQ2; **canonical**), UR, TB, W-05. Props: goblin rows persist until UR changes the camp. Must be at the **Heartlands–Ashenstead edge**, a short walk from M03.

### P21 Watchers' Lantern Post — Camp, Riverglass Banks

Stone shed on a rise at the fen edge: lantern rack (one empty hook, rusted, with **J.G.** scratched under it), blessed rope coils, banner-thistle racks, cold brazier, lectern with **Ansel's patrol book chained to it**, back-wall tally WALKED WITH US. NPCs: Ansel (MQ3, MQ4 dawn report, MQ8, OL, MQ12 station), Watcher pairs (ME10). I: patrol book (updates with later quests). Props: Joss's lantern hung burning on the empty hook (`OL_LANTERN_ONLY`) or hook empty with "Came in" (`OL_JOSS_IN`); new patrol book (MQ12). Used by MQ3, MQ4, MQ8, OL, ME10, MQ12. Map: overlooks the fen edge; start of the far leg (M05) and of ME10's walk to P22.

### P22 Widow's Step — Shrine, Riverglass Banks

| Field | Requirement |
|---|---|
| Areas | C1 offering bank (unmatched scraps weighted with pebbles: mitten, ribbon, sail strip with foreign stitching); C2 drowned causeway (knee-deep; Lessa's guide stakes stop at the bank; rope from a stake to Orrin); C3 deep edge and the **last dry hump with the dry footprints**; stake box with smoke-pots; MQ11 memorial-keeper station; post-MQ11 **remembrance channel head** (Tend/Shared) |
| NPCs | Act I: Lessa, Orrin. Act III: memorial keeper with a lantern. Post: Annelise/Watchers per ending |
| Interactions | I: prints, scraps; K: smoke-pot hops (ghost marker ≤ 10 m); C: set down pot (instant) |
| Quest-state props | Remembrance channel (lantern-lined cut, stone landing for offering boats) under Tend/Shared; offering boats at the top of the embankment under Seal |
| Used by | MQ3, CN (scrap), ME10, MQ11, MQ12 |
| Map | Embankment above a slow bend; **overlooks the fen's near edge** (MQ11) |

### P23 Ashenstead Watergarden and Ember-Well — Shrine, Ashenstead Fields

| Field | Requirement |
|---|---|
| Areas | A reflection pool (candle-stands with wax; Annelise's snuffer); B memorial stone (blank band, faint scrubbed chalk); C drying ledge of reed boats with family signs (Holt space empty, hooked H); D outlet and outfall head (three boards on rope-and-peg; pale worn bands); E outfall pool (turning water, brown softmoss); the Ember-Well on the green (P03 A) |
| NPCs | After MQ3: Annelise, a caretaker, Bet and Maud Holt. Post: Annelise, offering visitors |
| Interactions | I: stand, snuffer, ledge, wet line, ropes, wick (while carrying); C: set board (3 s ×3), clear offering (2 s); K: the boat; W: sit with the light at dusk |
| Quest-state props | Lit Holt boat; outfall running; tended pool after MQ11 (if CN done, Tend/Shared) |
| Used by | CN, ME04, MQ5 (Annelise), MQ11 argument, MQ12 |
| Map | Stepped outfall from garden down to the pool; wade push-back from the centre |

### P24 The Mantle Shrine — Shrine, Ashenstead Fields

| Field | Requirement |
|---|---|
| Areas | D wayshrine furred in softmoss; stone step worn in one place; E **Mantle channel** below (heavy pool, cold mist, no birds; stone causeway of old Marking-Stone footings to dry ground east; deeper water west; old stakes in the west shallows); F stone run (three look-alike Marking Stones a stride apart); G two lower pools linked by trickles |
| NPCs | Act II: Sedge. Post: Sedge cutting reeds; ME09 mist (no NPC) |
| Interactions | I: stones ×3 each, bundles; wade west shallows; MN walk-with; ME09 leave something |
| Quest-state props | Mist mantle at dawn (after MQ8); fresh softmoss |
| Used by | MQ8, MQ9 start, MQ12, ME09 |
| Map | On the Path of Unburnt Reeds between Ashenstead and Veilwater, **above a fen-edge channel**. The elk test needs the west shallows reachable by a slow, wadeable loop around the pool (≥ 8 m from the east bank at all points of the loop) |

### P25 Greyharrow's silent bell tower — Landmark, Heartlands

| Field | Requirement |
|---|---|
| Areas | A tower square; B roster wall (ABSENT crosses; two thumb-scrubbed names); C first landing (child's chalk ladder); D joist route (agility); E militia gallery outside stair with Teague's key (**walkable fallback, the critical path**); F second landing (two rotten boards with 1.5 s tell); G bell chamber (louvres, ringers' slate, chalk tallies, drop ladder, clapper worn bright, ring in the dust) |
| Interactions | I: roster, slate, beam; A: joist route (fallback E) |
| Used by | SB, VK (Merrin, Tamsin) |
| Map | Louvres must **overlook side-branch water** (SB strange moment). Multi-level interior NavMesh |

### P26 Circle of Unburnt Reeds — Landmark, Ashenstead Fields

A maintained ring of reeds that never burned; warning stake ("KEEP OUT — THIS MEANS YOU, PIP"); child-height footprints stop at the stake; one set goes on; a small still pool inside. NPCs: Pip and two children (ME06 dusk, after MQ3). Sedge-quieted pool sign at MQ8 start (fresh softmoss, cut reed ends; presentation only, no spawn). Used by ME06, MQ8, MQ9 (Sedge touches the dare stake). On the Path of Unburnt Reeds.

### P27 The Twice-Burned Tree — Landmark, Ashenstead Fields

A trunk split to the ground in two black halves (two burnings); pale fruit in the fork; stones set in a ring; flat root wait seat; C fork (step-up agility; fallback: hook-pole from the base, 4 s). D the Ashen Flats at night (dream walk over real terrain: burn boundaries, Joric's plot, the circle, guide-line field, barns). NPCs: Sedge at dusk (TB), household bark, Joric (gift). K: fruit. Used by TB (after MQ5). Map: reachable from P20 by the goblin path; the dream route must stay on terrain that exists.

### P28 The Uphill Canal — Landmark, Brackenford Woods

| Field | Requirement |
|---|---|
| Areas | A hazel cut (sunken lane, banks taller than a person); B foot pool with half-drowned carved arch; C the channel (twenty-odd stone steps, sunk a body-height and screened by hazel); D listening seat in an alcove under a heavy brow, facing a mirror-still basin and **away** from the channel; E head cistern (empty three-ring slot); F cutter's hut (three-ring doorstep = the paddle); G switchback (step-ups agility; earth switchback fallback); H Hazel Culvert (Riverwarden carving outside, wartime brick inside) |
| Load-bearing art requirement | The channel surface is **directly visible only from inside the observation volume** (lip path, channel-side bank, cistern rim) at every reachable position and every camera orbit and zoom; the alcove keeps the camera inside its walls; the brow occludes the channel at all angles. Verify with the real camera rig |
| NPCs | Sedge cameo (after MQ3; richer after MQ9) |
| Interactions | I: moss on downhill faces, leaf, slot, lintel; K: paddle (doorstep stone) |
| Used by | UC; shortcut afterwards |
| Map | Culvert far mouth opens at the **Ashenstead Fields edge**, bypassing the orchard berms (MAP VERIFICATION REQUIRED; any useful lower path works) |

### P29 Veilwater Falls and the Listening Steps — Landmark / shrine, Riverglass Banks

| Field | Requirement |
|---|---|
| Areas | A end of the reeds (pale stone lip); B plunge pool and outflow (four cupped step-stones; lower ford fallback with Skitters); C falls path (switchbacks, iron rings; ledge-shuffle agility with cut-steps fallback; hand-line with switchback-stairs fallback); D curtain ledge (threshold volume where the roar stops in < 1 s); E the Steps (terraced carved channels, each a different note, tiny stone gates, tool niche, kneeling stone); F flow-table chamber (round basin ~8 m, waist-high, **walkable all the way round**, open to falls-light on one side); **count channel** off the Steps (strokes cut four, bar, four; VK); G the further way behind a reed screen (not interactable, never explained) |
| Flow-table | **It is the map.** Built from the approved POI map: river and branches finger-wide, Braids hair-fine with gates, settlements as flat stones with one cut, Marking-Stone pins (Whisperflow with a bright scratch), the fen carved finer and silt-clouded, **the Cut as the only ugly line**, cutting five or six Braids. Clay plug on a ledge. Three fen-edge gates (far, middle, near) |
| NPCs | Act II: Oriel, Sedge. Post: Oriel (MQ12) |
| Interactions | I: table points; C: plug (3 s), gates (3 s each); A: three climbs (fallbacks listed) |
| Quest-state props | Table Cut-scar dark and dry after MQ11; fen model by `LM_FEN_ENDING` |
| Used by | MQ9, VK, MQ12, UC (optional inspect) |
| Map | Far end of the Path of Unburnt Reeds from Ashenstead; the falls' sound must arrive before the view |

### P30 Stillwater Fen interior — [PROPOSED POI] War site / landmark, Riverglass Banks

**Proposal:** the bible's slate has no POI for the fen's interior, though MQ11 is played there. Adding it brings the slate to 30 (still within 24–32).

| Field | Requirement |
|---|---|
| Areas | MQ11 C **Cutters' Causeway** (wartime stone causeway half under water; convoy cart ruts; drift-lantern row = lane hazard at one point); D Lessa's guide route (FW only; dry reed ridges with her knots); **E Gate 1 Reedmere Weir** (low weir, gate-board winch, Marking Stone in the face, chalk "1"); **F Gate 2 Long Sill** (long stone sill across a deep channel; black still water; crushed punt; serpent breach points); **G Gate 3 Lantern Sluice** (narrow carved sluice; lantern niche in each pier; landing = Muster respawn point 20 m from the arena); **H heart pool** (Muster arena, below); author **30–40 Marking Stones** across the fen along Braids, gates, Causeway, Reedmere posts and Widow's Step, each with a lantern by `S07` |
| Heart pool arena | ~30 m circle, ankle-deep over firm bottom; **eight Marking Stones on low plinths at ~11 m radius, NavMesh-walkable (ramped, no trigger)**; three Braid inflows; centre 5 m darker water over the convoy holes; barge ribs in a curve on the north side (block lantern lines); the **heart stone** with an empty post footing; no arena point more than ~10 m (walking) from one of the three reading stones nearest the inflows |
| NPCs | MQ11: crews at gates, Watchers, Sedge (edge, then hands in the water), Maelin or a crew hand with the post. Post: keepers/Watchers per ending |
| Interactions | I: gate stones ("stuck under the notch"); C: gate crank (adds to crew rate), cut notch and seat post (3 s each) |
| Quest-state props | Hollowed Current ambience and flow direction (step-keyed); lanterns at every stone; Seal boundary of stakes, blessed rope and lantern posts (deep fen closed); Shared boundary around the heart pool only; the player's post on the heart stone (visible from the Lantern Sluice under Tend) |
| Used by | MQ11, MQ12, W-06 residual pockets |
| Map | Gates in a rough line from Reedmere to the centre; heart pool beyond Gate 3; **Reedmere's lantern line in a natural sightline from the heart stone** (§6.3) |

### Minor sites (not counted as POIs; quest sub-spaces outside a parent POI)

| Id | Site | Subzone / band | Areas and storytelling | Interactions and props | Used by | Map |
|---|---|---|---|---|---|---|
| **M01** | **The Whispering Door farmhouse** (rename pending) | Heartlands, nearest Ashenstead | A muddy yard with pump, stone-lidded yard drain nobody walks over, four lantern poles (two empty), stacked hurdles; B kitchen (tally marks by the cellar door, thicker this year; hay fork); C cellar door (oak, warped corner, latch tied with twine, light under it); D cellar (crocks, apples, floor grate under board and flour sacks, knee-height tide line); E brick drain (stooping height; TREATMENT BOUNDARY — KEEP CLEAR stencils; bandage tins; stretcher pole); F valve chamber (flap valve rusted open; bricks stacked; anvil-stone); the yard pump-well (ME07: cup on a chain) | C: hang lanterns, pen hurdles (K ×2), bar the door (optional Woodcutting stem), relight lanterns, lift the grate (3 s), clear hinge (3 s), rehang (Smithing 3 s ×2 or crew 6 s ×2) or lay bricks (×3); W: hearth wait. Props: door behaviour by `WD_FLAP`/`WD_BRICKED`; raised crock shelves (bricked); crossed-through tally | WD, ME07 | Drain section short; ends at the valve chamber; does **not** connect to P13 for traversal |
| **M02** | Lark farm and low field | Heartlands field edge | A field gate (seed sacks under tarp; plough mid-furrow); B the raft across six furrows (two driftwood logs, hurdles, reed mats, cart wheel; chest-high flood line on the hedge); C two milky standing pools; D the soldered tin case; E hedge-bank niche; the farmhouse threshold with three cups (ME05) | C: cut logs, drag hurdles (K ×3), five case inspects, mark comparisons ×3; K: case, seed sack | FC, ME05 | Low corner must hold standing water |
| **M03** | The Wrong Culprit smallholding | **Heartlands–Ashenstead edge (canonical)** | A field edge (sun-white boar skull, spear on the gate); B cut rows; C drowned low corner; D hedge-gap with stale boar slots; E carry-trail to P20; G scrub margin with sow bed | I: four field reads, three trail inspects; K: two root sacks | WC (after MQ2) | Short walk from P20; Novice band |
| **M04** | Greyharrow side-branch bank | Heartlands | A staked bank with chalk cross and knotted cord; B bank-top crack; C old repair face (crew cut-marks); D wrack line above head height; E scour pool and jam; F three driftroots (leaner, holder, old one with nesting holes); G lower landing behind the holder | C: measure (2 s ×3), cut key limb, notch + back-cut, seat the stage (×2); A: root-shelf step (fallback cut-steps); hazards H1 swing ring, H2 chalk fall line. Props: holder standing/cut, slump, landing stage | BW | Downstream of Greyharrow docks |
| **M05** | The far leg and Old Lantern's bend | Riverglass fen edge | B far leg path past old patrol posts (Joss's fresh notches; thistle stubs); C reed shelter (green coat, pages on a cord, tally pages, rope, no food); **D willow bend** (dead willow; **four knee-high stone post footings, each with a landward ramp**, a heavy-water ford across the middle, deep side behind reeds, Ansel's waypoint stone); E return path (two drift pockets) | I: notches ×3 in order, pages; W: waypoint stone watch to nightfall; K: Joss's lantern (lit). Props: man walking the leg unlit at some dusks (`OL_LANTERN_ONLY`). **Old Lantern permanently quiets the bend (canonical)**; E pockets become residual after MQ11 | OL | No arena point more than ~4 m from a footing (Joss's 3 s count) |
| **M06** | Joric's plot | Ashenstead near band, beside P20 | A net bench (back to the low corner); B burned scrub ×3 clumps; C fence line ("black teeth"); D burrow under the fallen barn wall; E **corner culvert (not the P14 burned-culvert den)**; F low corner with dead-flat standing water; G buried field gate and notched gatepost | C: scrub (Woodcutting ×3), digs ×3 (×1 if `LM_FIELD_FIX = plot`); K: Wenna's seed basket. Props: water standing/drained; self-sown rye haze | UR, MQ5 (plot fix) | Lower than the remembrance circle; side culvert from P13 runs under it |
| **M07** | Reed-Lantern Bend [names the bible §4.1 place] | Riverglass fen edge | The heavy bend halfway between P21 and P22 that the Watchers log | W: ME10 escort pause; Watchers smoke the drift | ME10 | On R4 between P21 and P22 |
| **M08** | A Heartlands field ditch (Sedge-quieted) | Heartlands | Cold mist at dusk before MQ8; at MQ8 start, softmoss thumb-pressed into the bank, cut reed ends | I: signs (MN S01) | MQ8 | Any Heartlands field ditch near R3 |

---

## 5. Phase 1.5 count check

### 5.1 POI categories (§3: 24–32)

| Category | Target | Lowmark | POIs |
|---|---|---|---|
| Settlements | 3 | 3 | P01, P02, P03 |
| Micro-settlements | 3 | 3 | P04, P05, P06 |
| Ruins and war sites | 6–8 | 8 | P08, P10, P11, P12, P14, P15, P30; P09 (dual) |
| Caves / mines | 3–4 | 3 caves, 0 mines | P07, P13, P18 (mines: none, D-10 open) |
| Camps / bandit sites | 3–5 | 4 | P09, P19, P20, P21 |
| Shrines and ritual | 2–3 | 3 (+P29 dual) | P22, P23, P24 |
| Unique landmarks | 4–6 | 5 (+P30 dual) | P25, P26, P27, P28, P29 |
| Worked landscapes (not a 1.5 category) | — | 2 | P16, P17 |
| **Total** | 24–32 | **30** (with proposed P30) | |

**Mines:** Phase 1.3 §6 expects caves and early-level mines; no authored content uses Mining (bible D-10). If Mining is confirmed, the best fit is a small quarry/ore cut in the Brackenford hillside near P07's river ledge (outside the depot, so it does not alter MQ2), not a new dungeon.

### 5.2 Environmental storytelling elements (§2.3: 15–20)

Zone-level flagship elements, each a told-by-space micro-story a player can find without a quest marker:

| # | Element | Where |
|---|---|---|
| 1 | One pale yellow post among five grey ones, notch a hand higher | P04 E |
| 2 | EMERGENCY PROVISION notice pinned through CROSSING SHUT chalk | P04 B |
| 3 | Old fire rings on the high landing ("used for this before") | P04 J |
| 4 | The waiting wall worn smooth at child height | P02 |
| 5 | Two matching tally racks and a bare ledger shelf | P02 tally room |
| 6 | RELIEF — ROTATE BY LOT stencils under goblin twine and whitewash handprints | P07 |
| 7 | The missing convoy stone between thirteen and fifteen | P08 W2 |
| 8 | Cut chain with bright metal; gear greased over war grease | P09 |
| 9 | Wartime mile-stone scratched TOO FAR on a ruler-straight channel | P10 T4 |
| 10 | Child-height names scratched in the Sluice Shelter | P15 |
| 11 | Silt ring at one height on nine unlike circle stones; ploughs bending round boundary stones | P03 |
| 12 | KEEP DRY WITHIN THE STONES under a paint band; CLEAN WATER — THIS SIDE | P03, P13 |
| 13 | Unmatched scraps weighted with pebbles for the unreturned | P22 C1 |
| 14 | One empty rusted hook over J.G.; WALKED WITH US tally | P21 |
| 15 | Chalked flood lines with seasons, oldest highest, tonight's lower | P01 shelter |
| 16 | Roster column of ABSENT crosses; bell rope newer than the dust | P25 |
| 17 | Ceiling of crew marks and day-count strokes under arch 2 | P02 underside |
| 18 | The goblin field: stolen roots in rows, a blade notched at marker height | P20 |
| 19 | Unlaced boots side by side at the water's edge | P06 Far Racks |
| 20 | Black barge ribs in a convoy curve around the heart stone | P30 H |

**20** elements (at the top of range). Each POI also carries its own micro-story (Phase 1.5 §10.3).

### 5.3 Traversal route plans (§2.3: 3–4)

**4** routes (§3: R1–R4) plus one shortcut (S1). Check: each route opens in a different act and teaches a different traversal (social road, linear chase, field-to-reed pilgrimage, dusk patrol).

---

## 6. Relative placement and adjacency

All **MAP VERIFICATION REQUIRED**. "Near" means a short walk with the other place in view or earshot; "adjacent" means sharing an edge.

### 6.1 Must be near / adjacent

| Place | Must be near | Why |
|---|---|---|
| Whisperflow Landing (P04) | Brookhollow road head; renewal coppice (P17); Drowned Pier (P12) downstream of the footing; ME08 pool upstream | TL walk lengths; road-head view |
| Crestbridge granaries (P02) | Hill Depot (P07) behind them; Crest Hall beside them with the Granary Passage linking undercrofts; forge under the first arch | MQ2, MQ10, HS |
| P07 river ledge | River backwater below the toll line; hill road back to Crestbridge | SM shortcut; barge staging (§1) |
| Drowsebank (P11) | Between Crestbridge and the Cut mouth; Drowse spur to the lower Cut | MQ6 crew route |
| Cut mouth (P10 T3) | Orchard towpath; Bramblelock (P08) downstream | MQ4 chase legs |
| Orchards (P16) | Bramblelock; Sluice Shelter (P15); reed margin; the Uphill Canal hazel cut (P28) | MQ3, MQ7, UC bark from Bryn |
| Ashenstead (P03) | Rebirth Fields, P23, Ember-Well, Joric's plot (M06), P20, P27, start of the Path | MQ5, CN, UR, TB |
| P20 burned barns | M03 smallholding, M06 Joric's plot, P27 by the goblin path | WC, UR, TB |
| Whispering Door farmhouse (M01) | Heartlands–Ashenstead edge; drain toward the guide-line outfall | WD |
| Path of Unburnt Reeds | P26 → P24 → P29 in that order from Ashenstead; along the fen edge | MQ8, MQ9 |
| Lantern Post (P21) | Fen edge; M07 then Widow's Step (P22) on a dusk walk; start of the far leg (M05) | MQ3, ME10, OL |
| Reedmere (P06) | Fen's landward edge; Widow's Step overlooking the near edge; Gate 1 | MQ3 escort walk, MQ11 |
| Hollow Lock (P09) | Up the Cut toward the fen | MQ4 |
| NB north stair | Crest Hall water-gate wall | NB → MQ10 approach |

### 6.2 Must be on or in the water

| Feature | Requirement |
|---|---|
| Whisperflow old footing, shallows, drowned pier | Wadeable river margin; deep channel non-navigable beyond |
| Bramblelock weir pool, watch bench | Bench within ~6 m of the barge path |
| Hollow Lock chamber, Crest Hall water-gate basin | Chamber with a moorable barge; basin wade-depth with end steps |
| Drowsebank race, pond, footbridge, spill weir | Footbridge narrow; far crank on the pond bank |
| Orchard root pool, Long Bank, ditch | Pool drains through the sluice; ditch carries a bog-diver V |
| Widow's Step causeway | Knee-deep, wadeable to the deep edge |
| Mantle channel | West shallows loop wadeable; west deep water non-navigable |
| Greyharrow boom, Reach landing, side-branch bank | Boom across the dock mouth; scour boil on the reach |
| Reedmere withy line, staging kerb, fen gates, heart pool | Staging pool side kerbed; heart pool ankle-deep over firm bottom |
| Culverts and drains (P13, M01 E, P18 F, P28 H) | Water volumes with dry ledges as safe ground |

### 6.3 Sightlines and sound lines the narrative relies on

| From | Must see / hear | Package |
|---|---|---|
| **Whisperflow road head (P04 A)** | The **whole landing at once**: cart queue, crew fire smoke, the half-sunk skiff downstream, and the **one pale post** on the marker bank, readable before anyone speaks | TL §5.1 |
| Whisperflow footing (G) | The far-bank treeline (view-dependent grey figure during the hold) | TL Beat 6 |
| Hollow Lock roof walk (L7) | Stillwater's **fog wall** at dawn, with the Watchers' lantern dots along the fen edge stopping at its foot | NF §C8.3 |
| Hollow Lock winding floor | Sallow on the far gallery across the chamber (visible, unreachable) | NF Beat 7 |
| Bramblelock bench | The unlit barge passing within ~6 m | NF §C8.1 |
| Rebirth Fields field-hut bench | The circle, the glisten line between boundary stones, **and steam at the Ember-Well** on the green | GL Beat 2 |
| Drowsebank loft gap | Mill floor and race gate | TF Beat 4 |
| Sluice Shelter / Long Bank | Bryn's position never moves; the reed margin is **away** from her (positional voice) | DK §DK.6 |
| Uphill Canal listening seat | The basin reflects the channel; the channel itself is **never** directly visible outside the observation volume | UC §2.3 |
| Greyharrow bell louvres | Side-branch water | SB §1.6 |
| Greyharrow Reach ring | The reach is **invisible in the dark** and plain at dawn (lighting, mist) | NT |
| NB under arch 2 | Footsteps on the deck above carry down | NB |
| Crest Hall Long Hall | Water-gate audio through floor-grates; ripple light on the ceiling | CR §10.7 |
| End of the reeds (P29 A) | The falls **heard before seen** | BF |
| Curtain ledge midpoint | The roar stops at one threshold step | BF §BF.6 |
| Lantern Sluice (Gate 3) | Heart-pool fog lifting at 50% gate progress; the Muster's lights | SV Beat 3 |
| **Heart stone (P30 H)** | **Reedmere's lantern line** and the constellation of fen-stone lanterns in a natural sightline | SV §11.7 |
| Whisperflow at night (MQ12) | The Marking Stone in view during the crossing | RR |

### 6.4 Must not be seen or reached

| Constraint | Why |
|---|---|
| The Uphill Canal channel surface from outside its observation volume | UC rule is load-bearing |
| The Listening Steps' "further way" beyond the reed screen | Not interactable; never explained (bible §2.7) |
| The deep fen inside the Seal boundary after MQ11 | Closed state |
| Hollow Lock far gallery from the winding floor | Sallow cannot be reached in MQ4; he has no combat definition there and is not targetable (by melee or ranged) |
| The deep side of Old Lantern's bend during the fight | Arena rule |
| The Whispering Door farmhouse drain → P13 | Not connected for traversal |

---

## 7. Open map questions for the Director

1. **Approve the hydrology chain and toll bypass (§1)**, including barge staging at the Drowned Lamb's river door?
2. **Add P30 Stillwater Fen interior** as a counted POI (slate becomes 30)?
3. **Which settlement lies across Whisperflow** (TL §14 item 4; MQ12 far bank and Nan's house)?
4. **Mines (D-10):** none authored; accept 3 caves and 0 mines, or reserve the Brackenford quarry cut (§5.1)?
5. **The Whispering Door farmhouse:** confirm the new name so M01 and the drift id can be finalised.

---

## Director rulings reconciliation (2026-11-03)

Applied `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. The "humans downed or yield" review ruling is replaced by CDR-1 (defeat at 0 HP, no downed humans or tied props; SX-1/SX-2 need only an NPC standing spot after defeat). §0 gains ranged (CDR-2: no safe unreachable perches; never required) and defeat-presentation rows; §6.4 notes Sallow is untargetable across the MQ4 chamber. Release wording clarified (CDR-3). No POI, area, interaction or id changed.
