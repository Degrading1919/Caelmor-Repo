# Thornfell — POI and Zone Requirements

**Status (2026-11-03):** review-state content. Gameplay Designer requirement set for level design, Batch 4 of the Thornfell production plan (bible §12). It turns every place authored in the Thornfell narrative packages into level-design requirements: subzones, routes, POI sub-spaces, traversal (agility triggers with walkable fallbacks), sound-system features, per-player state and phasing, and relative placement. All places are **[NEW]** unless the bible marks them [CANON], and nothing here is canon until the Director promotes it (TD-14). **[PROPOSAL — DIRECTOR]** marks consequential choices. **MAP VERIFICATION REQUIRED** marks every place where geometry matters (TD-6: relative placement only; no compass direction toward Emberholt is asserted). This file is **documented dependencies only**: no schema, JSON, scene data or C#.

**Director rulings (2026-11-03, binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. For places this means: every enemy is defeated at 0 HP, so no arena needs tied-prisoner props, downed-state space or break-off exit lanes for wolves (leash/reset only); TD-8 Gatefall deadfalls, `TSW_THAW`, TWN's open stone and TWC's banner walk (Old Torvek's local tradition) are approved; TST's wind butts are a real shooting range (CDR-2); Thornfell is an internal milestone of the complete game (CDR-3).

**Sources:** bible §1.1, §2.1, §4 (TP01–TP28, route order), §7.3–7.4, §9 (flags, season, posture, calls), §11; Act I §A5, §B5, §B10–B11; Act II §A5, §A8.1, §B5, §B8; Act III §5, §8, §11, §E; the place tables of the four side-quest files, TME01–TME10 and TDS01–TDS10; the Lowmark zone file as the format standard.

**Source state.** The three main acts were reviewed and committed before this file was written. The four side-quest files were under independent review when it was drafted; those reviews have since landed, and the independent review of this file (§13) re-checked places, flags and names against the committed text. Shared values (gust, bridge, thaw) follow the canonical register in §12 (C-1 to C-8).

**Companion:** `04_CONTENT_PRODUCTION/Enemies/Caelmor_Thornfell_Encounter_and_Enemy_Requirements.md` (encounter ids, hazard ids, arena combat rules, Horn-Echo storm sites).

---

## 0. Level-design constraints

### 0.1 Runtime (carried from Lowmark zone file §0)

| Constraint | Level-design rule |
|---|---|
| Click-to-move over a host NavMesh; Shift sprint; no jump | Every required route, objective, shelter face, niche and arena safe space is NavMesh-reachable by walking. |
| Agility triggers approved, **not built** | Every agility trigger listed here has a **walkable fallback** that is the critical path until triggers are built. No required objective sits behind a trigger. |
| No multi-level traversal or off-mesh links yet | Vertical spaces (Whinstone hoist shaft, Summit stairs, gatehouse stair and winch floor, Shatterfall ledges and ladders, horn towers, crag pitches, sheave tower, hostel ward stair) need multi-level NavMesh with stairs or ramps. Rungs, ladders and pitches are **interaction-driven moves** ("climb to next ledge") until off-mesh links exist. Flag each to Systems. |
| Interaction needs reach and line of sight | Channel points used under attack or weather (snub post, winch drum, pull-line ledges, plate frame, brake post, field anvil) need a ≥ 2 m standing pad facing the object. |
| Edges | **No fall deaths anywhere in Thornfell.** Every ledge, rim, span, crag, parapet, plank and stair that can be pushed toward has a rope rail, a rope boundary volume or an edge blocker. Every push (gust, charge, surge) goes to a defined safe side. |
| Per-player state (bible §9) | Quest-state props, weather and season are client presentation keyed to the local player's state; Lowmark's per-player prop fallback applies (host's props, each player's own barks and flags). |

### 0.2 Sound-system features (bible §1.1) — level-design definitions

Thornfell's readable system is sound. Each feature below is a **tagged volume or object** the level must supply; §4 lists every instance.

| Feature | Tag (working) | Requirement |
|---|---|---|
| **Fluted face** (wind-window source) | `fluted_face` | Vertical grooves cut in rows into a rock face. Whistles **up a fifth 2.5 s** before a gust (Enemies §13 I-1). Each has a gust lane and a **marked shelter face** beside it. |
| **Shelter face / niche** | `shelter_safe` | Always safe from gusts and sheds. Marked by environment: painted **white shoulder bar** (Windscar, TF-M1), **chalk notch** (Shatterfall), **red rag on an iron ring** (TF-M5 high track), cairn moss (goat shoulder), three-stone cairn (Splitpine Crag), buttress niche, drum hood. |
| **Echo face** | `echo_face` | A face the player can blow **Answer** at and count beats back (1 / 2 / 3+ / none by distance band). Smeared or short return means the face is moving (shedding face). Used for navigation in whiteout and for rockfall reading. |
| **Horn rest / answering stone / horn ring** | `horn_rest` | A fixed place where a call is blown with an aim: Passwatch horn post, the four TTH answering stones, the TSG ledge-lip rests, warden posts W1–W4, Gatefall parapet ring, Signal Terrace racks, Goat Ledges call-stones, Three Calls ledge. Each has a facing and, where it matters, a target sightline. |
| **Groove bank** | `groove_bank` | Horn-tower parapet stones with channels cut for specific calls (Old Watchfire Line). Carries a call to the next tower. |
| **Null-point** | `audio_null` | Echohewn sound-dead pocket: world audio mutes by layer at the threshold (drip, then wind, then footsteps, then breath); **dust and snow fall straight down**. Resonance cannot carry. Instances: TIW quiet gully, Summit Counting Room and alcoves II and V, Silent Gorge, TWG gateposts, TME05 niche, Greymantle's inner chamber. |
| **Carrying spot** | `voice_carry` | A place where any voice returns clear from every side (Assembly Hall A3; Hearthguard arch at the ridge-market; Summit whisper-hall mouths and carry lines). |
| **Pressure shadow** | `pulse_safe` | Summit great hall only: pillar lees (marked by snow wedges) and silent alcoves where node pulses do not strike. |
| **Rope boundary** | `rope_boundary` | Uncrossable rope with a creak and a bark (TF-M5 "Rope. Wrong side."). |

---

## 1. Macro layout [PROPOSAL — DIRECTOR; MAP VERIFICATION REQUIRED]

The narrative fixes these relative facts (bible §4.2, Act III §5):

**Windscar Pass route order (near → far):** `Passwatch gate → the Blind Corners → the Narrows bridge → Three Calls Shelter → the Whinstone track (leaves the pass road and climbs the cliff above the pass to the Muster Hut and the Whinstone Store) → the high track (above Three Calls, toward the far gate) → the Gatefall (far gate) → far apron → far track → far hut → Hushfold's far shielings`.

- Passwatch's **inner side** faces the Marches (Stonewake's road, Nettlehook's track); its gate faces the pass. Passwatch closes the near end for storms; the Gatefall closes the far end for a season.
- The **Whinstone track** and the TF-M5 **high track** both leave the pass beyond Three Calls Shelter. Recommendation: one track foot (K1) that forks: the Whinstone switchbacks climb to the store; the high track (C2–C6) runs along the cliff toward the Gatefall. MAP VERIFICATION REQUIRED.
- **Stonewake** is reachable from Passwatch by the ordinary road. The Summit stair foot is reachable from Stonewake's high road. Hushfold is a few minutes from Stonewake on Ridgewall paths (TMM) and sits on the Ridgewall above the pass road (TSM).
- **Shatterfall Gorge**: Carrick's Cut at the gorge mouth by the rim; ledges step down the near wall; the Horn Seat is cut into the wall above the camp shelf; the far approach is the gorge's other end; the rim cairns stand on the rim above the Seat; the Salvage Ledge is visible across the gorge from the Cut overlook.
- **Stormwake Plateau**: Black Glass Hostel on its road; Red Slope Terraces below its shoulder; the Goat Ledges on the shoulder; Greymantle's Den within reach of the hostel road; the Stone With No Shadow on the plateau; Splitpine Crag visible from the Stormwake warden shelter.
- **Oath Cairn Fields**: the Name-Stone Wall in the upper field, reached by the oath path (Oathkeeper's Step) or the long cairn path; Torvek's cairn-house at the field's edge; the stone ledge above the field.
- **Ridgewall Heights**: Nettlehook (ropeway over a ravine), Hushfold, the Old Watchfire Line along a crest (T1 nearest the Windscar track, T6 above the Silent Gorge), the Horn That Never Fell ledge above the Line, the Abandoned Ridge Camp on a route joining the Line and descending to Stonewake, the Burned Slope.

---

## 2. Subzones (bible §4.1)

Each subzone has a **near band** and a **far band**, so early side quests can play in subzones whose main content is later (the Lowmark resolution, Lowmark zone §2).

| Subzone | Contains | Band: near / far | Ambient signature | Families (Enemies file) |
|---|---|---|---|---|
| **Windscar Pass** | TP02, TP06, TP07, TP08, TP09, TP26, TP27; Whinstone track; high track; stormwood slope | Competent (TP02–TP07, TP26) / Competent → Advanced (TP08 TF-M2; TP09 and high track TF-M5) | Fluted faces whistling; snow-poles; horns from the post; wind sock and pennant | Pass Bandits, Ridge Wolves, Ridge Crows, Iron Winter crews |
| **Ridgewall Heights** | TP03, TP04, TP18, TP20, TP22, TP23, TP24; TME04 stretch; TME07 track; TME09 ledge | Competent / Competent (late) | Longhouse smoke, ropeway creak, horn towers, goats | Ridge Wolves, Ridge Crows, Pass Bandits (TWG T4) |
| **Shatterfall Gorge** | TP10, TP11, TP12, TP13, TP14 | Advanced / Advanced | Roaring gorge wind, grit, haze; plates ringing at the ledge | Rock Vipers, Horn-Echo, Shatterfall Brigands |
| **Oath Cairn Fields** | TP15, TP16; Torvek's cairn-house; the stone ledge | Competent (TOS after TF-M1) / Advanced (TWN after TF-M3) | Wind-brushed plateaus, stormflowers, cairn ribbons | Rock Vipers |
| **Stormwake Plateau** | TP05, TP19, TP21, TP25, TP28; Splitpine Crag; Stormwake warden shelter; rut ground | Competent (TP21, TP28) / Competent late (TP05, TP25, Crag) | Lightning-scarred stones, black glass, thunder after a count | Fell Stags, Ridge Bears, Rock Vipers, Ridge Wolves, storm hawks |
| **Echochamber Summit** | TP17 | Advanced / Advanced | Air-channels breathing; a hum in storms; total silence once (TF-M4) | Ridge Crows, Iron Winter crews; Summit node (hazard) |
| **Stonewake** | TP01 (Assembly Hall, Signal Terrace, Stonewright Quarter, ridge-market, cistern, Brita's stall, wind butts) | Hub / hub | Ridge-market voices carrying under arches; lintel taps; horns from the Signal Terrace | None |

---

## 3. Traversal route plans

| Route | Path | First used | Character | Agility triggers → walkable fallbacks |
|---|---|---|---|---|
| **R1 The Pass Road** | Passwatch gate → Blind Corners → Narrows → Three Calls Shelter → track foot | TF-M1 | Cart road cut into the pass wall; snow-poles; fluted faces with white-bar shelters | Blind Corners **goat-track gap** → 15 s scramble round a boulder; Narrows **guide-line traverse** → traveller basket / bosun chair; Narrows gap **scree path** down and up between S1–S3 (always walkable) |
| **R2 The Whinstone Track** | Track foot (K1) → switchbacks (K2) → quiet gully (K3, null-point) → hut shoulder (K4) or cliff ledge (K5) → store gate ledge → hoist foot (G1) | TF-M2 | Climbing switchbacks with forks read by sledge grooves; wrong forks dead-end in ~30 paces | K5 **broken rail step** → inside cleft path (+10 s); hoist shaft **crossbar step** → rungs; cage ride (after `TIW_CAGE_WOUND`) → rungs |
| **R3 The High Track** | Three Calls (C1) → Switchback Stair (C2, W1) → Fluted Run (C3, W2) → the Fork (C4; drovers' path roped shut) → Iven's Post (C5, W3) → Last Rise (C6, W4) → Gatefall near apron | TF-M5 | Rope-railed cliff track; whiteout in TF-M5; red-rag niches every 40 paces | Gallery **rock scrambles** → cut stairs; no trigger on the climb itself |
| **R4 The Gorge Descent** | Carrick's Cut (rim winch) → Gust Stair (L1) → the Jam (L2) → the Lip (L3) → scree run → Broken Engine (L4) → the Hollow (L5) → camp shelf (L6) → seat approach (L7) → Horn Seat; out by the miners' ladders (L8) to the rim | TF-M3 | Broken shelves between gusts; storm windows; Horn-Echo lanes | L1 **shelf gap** → plank detour (+~20 s); L7 **scramble** → ramp; TDS06 engine frame climb → ledge ramp; Salvage Ledge **rope traverse** → old siege ladder route; hoist shortcut (after Mining or crew) |
| **R5 The Summit Stair** | Stair foot (F1) → outer stair (S1) → inner stair (S2, air-channels) → Echo Landing (S3) → Upper Landing (S4) → whisper hall → great hall → Crown | TF-M4 | Carved stairs hugging cliff faces, then into the rock | S1 **broken flight** → full switchback |
| **R6 The Ridgewall Paths** | Passwatch inner road → Nettlehook → TME04 safe stretch → Hushfold; crest path along the Old Watchfire Line T1–T6 → gorge stair → Silent Gorge; ridge camp descent to Stonewake | TF-M1 (Nettlehook), TWG | Highstead paths, shelf paths with chalk faces, horn towers | T2 **rubble climb** → carry and set the Warden's ladder (`TWG_LADDER_SET` keeps it); T3 scramble → inner-wall steps; T5 parapet walk → interior stair; G1 **rope descent** → cut stair; sheave tower **outer lattice** → inner ladder (chip three iced rungs) |
| **R7 The Stormwake Road** | Stonewake → Stormwake warden shelter → open plateau → Black Glass Hostel → shoulder (Goat Ledges, Red Slope Terraces, Greymantle's approach) | TSL, TGY, TSR, TGM | Exposed, lightning-scarred; storm windows | Splitpine Crag **chimney** → goat ramp + warden line clip; TGM G7 **ledge shimmy** → long switchback; Red Slope **scarp scramble** → wall-steps; **goat steps** (TGY, `TGY_STEPS_SEEN`) → the ledge path; oath path **cleft down-climb** → walk round from the field and up the scree |

**Phase 1.5 check (3–4 route plans):** seven are listed because Thornfell's vertical subzones each need one; R1, R3, R4 and R5 are the four **designed** routes (set pieces); R2, R6 and R7 are connective.

---
## 4. POI requirements (TP01–TP28)

Format per POI: **placement**, **areas** (sub-space ids are the packages' own letters), **traversal** (A = agility trigger → walkable fallback), **sound features** (§0.2 tags), **state and phasing** (flags; full table in §6), **used by**, **map**. Phases: **M1–M5** (milestones), **Post** (after `TH_STANDING`), **Thaw** (`TSW_THAW`).

### TP01 Stonewake — Settlement, Stonewake [CANON]

| Field | Requirement |
|---|---|
| Placement | Terrace town on cliff tiers; reachable from Passwatch by road; Summit stair foot off its high road; Hushfold a few minutes by Ridgewall paths. |
| Areas | **Ridge-market** (M1 Hearthguard stall under a voice-carrying arch; M2 price board; M3 hauliers' stand; Brita's bow stall; market cistern under a grate, knee-deep far end, marker pins every ten ells); **Stonewright Quarter** (Q1 measuring yard with the one-ell groove bench; Q2 Sefa's work room and log shelf with the war shelf and the **sealed "Lowmark work, war years" bundle**, seen and never opened; Q3 dray shed; doorways with tap-worn lintels, TME02); **Signal Terrace** (horn racks on the parapet; the **practice face** across the gully with chalked echo marks; code-book lectern; terrace workshop; the **Wardens' store** under the terrace with an Assembly seal; Eyvind's guarded bench `[SPLINTER]`; wind butts at the terrace lip; a hanging mason's plank on the outer face, TMM M1); **Assembly Hall** (great stair of twelve treads; A1 round floor with the **speaking stone**; A2 near ring; A3 the **carrying spot**; A4 walls and door wall where the clanless stand, side door; A5 four standing places: with Hushfold, wardens' rail, cairn bench, Blood-Oath stone table; galleries on three sides; the cold room); the warden runner's post at the terrace |
| Traversal | Signal Terrace plank: A step down from the parapet → the Quarter's hoist cage (crank). Cistern ladder; wading slow, no hazard. |
| Sound features | `voice_carry`: market arch, Assembly Hall A3 (Hadrik knows it; never explained). `horn_rest`: Signal Terrace racks. `echo_face`: the practice face. `fluted_face`: below the terrace (TMM-H1 gust on the plank, buttress niche). Sightlines from the terrace to **Passwatch tower, Nettlehook ropeway head, Three Calls ledge, Hushfold's smoke and the first watchfire tower** (TNK answers come from them in turn). |
| State and phasing | `TH_SEASON` (market snow props; first snow at TF-M2 end). TF-M5 Assembly placement (per-player NPC position sets by `TH_STAND` and the §9.3 flags). Post: closure account board by posture (open: by the door wall; watchful: Wardens' room; sealed_with_terms: by the wardens' rail); Signal Terrace crier (open) or relief runs leaving on Gather and returning on Rest (sealed); market prices by posture; Ingrith held in the cold room (all postures); Brynjar by `TH_BRYNJAR`; Hushfold's chalk standing mark on the hall floor with `TH_HUSHFOLD_VOICE`. Wardens' store contents by `TH_HORN` (surrendered: three crates; broken: one sack of shards; silenced: empty). |
| Used by | TF-M2 (offer, closing), TF-M5 (Assembly, epilogue), TMM, TNK, TST, TSL (end at the hall door), TWC (offer, rite end), TME02 |
| Map | The Signal Terrace must sit on a cliff edge with an outer face over a drop and sightlines to the posts listed (MAP VERIFICATION REQUIRED). The cistern lies under the ridge-market. |

### TP02 Passwatch — Settlement, Windscar [CANON]

| Field | Requirement |
|---|---|
| Placement | Walled outpost across the throat of Windscar Pass; inner side to the Marches, gate to the pass. |
| Areas | P1 **gate** (drop-bar on chains; the warden's slate on a nail; child-height notches on the inner face; the **inner arch** with iron cramps and the lifted voussoir, TAS); P2 **horn post** on a stone shoulder above the gate (swivel horn, practice rack, the **training board**, brazier, outside ladder); P3 **store-yard** (the tarp of sacks marked *W. acct.* in M1; the empty lee and sledge-runner grooves in M2); P4 **barracks and ridge stables** (hearth bench for keep-watch; patrol board); the **cold shed** lean-to (TAS); the wall walk; the warden post strongbox (TF-M3 `kept` roster); the lock-up |
| Traversal | Arch top course: A horn-post outside ladder → barracks inside stair to the wall walk. |
| Sound features | `horn_rest`: the horn post (all six Ordinary Calls taught here; Close calls carry along the near pass). `fluted_face`: the cliffs above Passwatch (TAS-H1 scaffold gusts; lee of the arch pier). The cliffs are an `echo_face` for the Close (the **span Close returns early**, TF-M1 strange moment, heard from the Narrows). |
| State and phasing | M1: Close sky steps by `TPW_CLOSE_COUNT`; gate shut at quest end, open after the storm. M1 tarp of sacks → M2 empty lee (per player, after TF-M2 `S02_tarp`). Training board seventh row (inspect; TTH restores or not by `TTH_KEEPER = board`). Strongbox holds the roster with `TH_SHATTERFALL_ACCOUNT = kept`. TAS: arch scaffold and forge in the yard during the quest; new cramps after. Post: two slates on the gate post (open), Outside slate inside the post (watchful), full Outside slate and a postern relief line (sealed_with_terms); Dorn's dusk Lost answered by the far hut (sealed). |
| Used by | TF-M1, TF-M2, TF-M3 (`kept`), TF-M5 epilogue, TTH, TAS, TWN (`kept` reading) |
| Map | The arch top course must be reachable both from the horn post and the wall walk. |

### TP03 Nettlehook Highstead — Settlement, Ridgewall [NEW, Part 3]

| Field | Requirement |
|---|---|
| Placement | On a shelf of the Ridgewall reached by a track from Passwatch's inner side; ropeway across a ravine to a lower shelf. |
| Areas | Longhouses (upper longhouse with the smoke seat, smoke-hood, tally board; lower longhouse lessons room); shared granary; ropeway **upper station** (brake wheel, car, Ketil's field forge, the **rota board**); **sheave tower** (crow nest, pin); the **span** over the ravine; lower longhouse (Leiv's benches); the snow shelf above (snare line); the Skarde house (TSN epilogue); a table volume for TME03 |
| Traversal | Sheave tower: A outer lattice → inner ladder (chip three iced rungs, 2 s each). |
| Sound features | `fluted_face` on the far ravine wall (gusts stop the car: board *GUST — STOP — WAIT*). The cable's note (TNR strange moment). |
| State and phasing | Granary fill by `TH_PASSWATCH_ROUTE` (sledge full, caravan lean, split middling) and posture (open: topped from the common store). Ropeway running after TNR; Tova to lessons with TNR complete; rota board by `TNR_ROTA`. TRR witness ribbon on the ropeway pylon with `TH_HIGHSTEADS_TOGETHER`. Snow from TF-M2. |
| Used by | TF-M1 (sledge), TNR, TFS, TSM, TRR, TME01, TME03, TME07, TSN epilogue, TF-M5 epilogue |
| Map | MAP VERIFICATION REQUIRED: upper station on the shelf, lower longhouse below, span across a ravine; goat shoulder (TSM E) above. |

### TP04 Hushfold — Micro-settlement, Ridgewall [NEW, Part 3]

| Field | Requirement |
|---|---|
| Placement | Shelter-line houses along a Ridgewall shelf above the pass road; far shielings **beyond the Gatefall** (not visited in Hushfold quests). |
| Areas | Tally hearth (long room; the tally book on a stand; household marks on the lintel, no clan signs); tally hut (H2); Runa's house (the first tally book, kept after TF-M5); the Kvist house; the Brede house (TWN); Grima's count board by the woodshed; the shelf path to the near woodstacks (chalk faces every 60 m); four new slate roofs with banker marks (TMM) |
| Sound features | `fluted_face` on the shelf path. TSM wonder: the smokes lean together. |
| State and phasing | Snow from TF-M2. Post (Act III §E.2): shelter-line smoke and far-shieling households wintered in (open), two named outside (watchful), three wintering at the far hut by choice with "Out. Fed. Expected." chalk (sealed); a ribbon on the Weatherall page; a rubbing copy with `TSW_READER = runa`; Oddny and Halvard by `TSW_ODDNY` / `TSW_HALVARD`; the TWN slip on the same shelf with TWN Completed. |
| Used by | TF-M5 (column, epilogue), TSM, TWN, TMM, TWC (optional knot), TME01, TME04 |
| Map | MAP VERIFICATION REQUIRED: reachable from Stonewake in a few minutes; above the pass road. |

### TP05 Black Glass Hostel — Micro-settlement, Stormwake road [NEW, Part 3]

| Field | Requirement |
|---|---|
| Placement | On the Stormwake road; door faces the prevailing drift; goat pen and woodstack on the lee side; Greymantle's Den within reach. |
| Areas | A hall (colours on the pegs; hearth; safe point); B the **inward-opening door** with a black-glass panel and the **drift post** (the scraped patch beside "B.S."); C goat pen and woodstack; D the **old ward** below, by an outer stair under the drift side (locked until the drift is dug); the yard (Yrsa's sled, tally stick; the **weather slate** by the porch, TGM) |
| Sound features | Whistle through the black-glass panel (TSN-H1 tunnel slump). |
| State and phasing | Buried door on a bad night (TSN storm window, per player); dig-out tunnel segments (persist). Drift post prop by `TSN_RECUT` / `TSN_TOLD_HOUSE` / `TSN_LEFT`. Grey hank by the door with `TGM_OUTCOME = ended`. |
| Used by | TSN, TGM (hook, close) |
| Map | MAP VERIFICATION REQUIRED: door facing the drift; ward stair under the drift side. |

### TP06 Three Calls Shelter — Micro-settlement, Windscar [NEW, Part 3]

| Field | Requirement |
|---|---|
| Placement | Between the Narrows and the Whinstone track; its lower guest ledge visible from the Narrows far bridgehead. |
| Areas | C1 the **guest ledge** (roofed; brazier; lantern) with the **horn map** on its back wall; the guest room (bunks with numbered posts; Thyra Brack's chest of bed books); the Shelter Stone at the ledge lip (TTH B4); the muster point (TF-M5) |
| Sound features | `horn_rest`: Shelter Stone (mouth-hollow, soot-blackened). Ressa's horn map shows each stone's reply glyphs. |
| State and phasing | M1 split or waiting load waits here overnight (`TH_PASSWATCH_ROUTE`); TBC waiting group (`TBC_WAITS = family`). TF-M5: muster with Ressa, Kolli, wardens. Horn map: Third Horn mark chalked fresh with `TH_THIRD_HORN`. Post: Ressa's crated plates under a tarp with `TH_HORN = surrendered`; Ressa's commission bench. |
| Used by | TF-M1, TF-M5, TTH, TBC, TRR (beyond), TF-M5 epilogue |
| Map | Horn map placement: see §12 Z-3 (painted boards on a cut back wall). |

### TP07 The Windscar Narrows — Unique landmark, Windscar [NEW on CANON feature]

| Field | Requirement |
|---|---|
| Placement | A landslide gap across the pass road beyond the Blind Corners, about forty paces wide; the stormwood slope (W3) below it. |
| Areas | W4 near side (anchors, **Aud's field anvil** cart → public Smithing station after TBC; the **snub post**; the **repair post**, TBC); the **shedding face** above the gap; the **scree path** down into the gap and up the far side past shelter faces S1–S3; the **span** (footropes, handlines, deck boards, kneel marks every 10 m after TRR); W5 far bridgehead and far anchor rock; the Narrows Stone on the near-side bluff under three fluted faces (TTH B3); the meal ledge (TRR); the gap below (TBC updraft wonder) |
| Traversal | Guide-line traverse / traveller basket / bosun chair across; **scree path always walkable** (the critical-path fallback in every bridge state). |
| Sound features | `fluted_face` ×3 above the Narrows Stone; S1–S3 white-bar shelters; `echo_face`: the shedding face (Answer: three steady beats = holding; short or smeared = moving). TTH strange moment at the Narrows Stone (a rising tail nobody blew; once per player). |
| State and phasing | **Bridge state (per player, §6.2):** N0 down (TF-M1 before `S08_span`) → N1 patched (TF-M1 `S08` complete) → N2 cracked (TBC Active only; overrides any other state for that player; §12 C-6, Z-1) → N3 mended (TBC Completed) → N4 permanent span (TRR Active and after). Snow from TF-M2. Thaw: the Narrows run loud. |
| Used by | TF-M1 set piece, TF-M2 and TF-M5 travel, TBC, TTH, TRR |
| Map | MAP VERIFICATION REQUIRED: gap width; far loads visible "small and hooded" from the near side; the far bridgehead must see Three Calls' lantern. |

### TP08 The Whinstone Store — Cave/mine, Windscar [NEW]

| Field | Requirement |
|---|---|
| Placement | Wartime cliff store-house cut into the rock **above Windscar Pass**, at the top of the Whinstone track. |
| Areas | G0 barred front gate (greased hinges, swept ledge, WHINSTONE stencil); G1 hoist foot (cage chained with a rusted padlock); G2 hoist shaft (three runs of rungs, two rest ledges, two vent slits); G3 winding head (drum, crank, pawl); G4 grain gallery (nine bays; **lowland relief stencil** bay; the folded Passwatch tarp); G5 iron gallery (field forge, three crow vent shafts, hasp door, knee-high vent crawl); G6 plate gallery (crates of plates, grit, Eyvind's sketches, signal niche); G7 counting room (high desk, strongbox, **loophole window** down to the pass); G8 last bay with the **trial frame** |
| Traversal | Shaft crossbar: A → rungs. Hasp: Smithing at the field forge → vent crawl (15 s). Cage ride after `TIW_CAGE_WOUND` (also the respawn path). |
| Sound features | Vent slits and vent shafts whistle a fifth before draughts (TIW-H1, TIW-H2). Plate gallery signal niche carries sound (TIW-E4 hornman). Trial frame: touching a plate hums the rock and lifts every crow on the cliff (strange moment). |
| State and phasing | Before TF-M2 `S05`: gate barred, cage chained, interior unreachable. After TF-M2 by `TH_STORES` (Act I §B10, Act III §E.6): **reported** sealed, Warden at the hoist foot; **seized** emptied, racks bare, sledge marks; **leverage** still filling (ninth bay full, new plate crates; crew present until TF-M5, Enemies TW-03). Post by `TH_STORES` × posture (counted out / under account / relief depot; shelter on the track; storm shelter; iron racked under seal). **In every case** the relief sacks stand apart, stencils out, *"Not ours. Kept till asked."* (nothing says how they came; TD-11). |
| Used by | TF-M2 dungeon, TF-M5 epilogue |
| Map | MAP VERIFICATION REQUIRED: cliff position relative to the pass road and the Gatefall; loophole looks straight down at the pass. **Never** show or imply a route by which the relief grain arrived. |

### TP09 The Gatefall — Ruin/war site, Windscar [NEW]

| Field | Requirement |
|---|---|
| Placement | Narrow cut at the far end of Windscar Pass with seven deadfall galleries above it; near apron (G0) on the Passwatch side; far apron (F1), far track, far hut and far shielings beyond. |
| Areas | G0 near apron (Dorn's post W4 ends here; a horn post after TF-M5); **G1–G7 galleries** each with a **marker stone** cut with Close + a tag glyph, a cut stair (walkable) and a rock scramble (A); pull ledges below the live galleries' pin-beams; cut floor (war heaps, frozen wagon axle, a fallen grey prop, the slab slot); H1 **warden room** (hearth hard against the inner wall; plaster cracked off; **the closure roster** under soot in three panels; desk, empty slate shelf, drill board, six bedrolls, a child's mitten); H2 inner stair; H3 **winch floor** (~18 × 10 m, railed; drum hood ~6 × 4 m; pawl; slab slot 2 m; parapet with a horn ring and a fluted stone; outer stair); F1 far apron; F2 far track and far hut |
| Traversal | Gallery scrambles: A → cut stairs. Winch floor: inner stair (player) and outer stair (crew). Far track beyond F1 in whiteout uses the same rules as the high track (rope boundaries, niches). |
| Sound features | `horn_rest`: gatehouse roof (hornman calls the sealing order), winch-floor parapet ring, near-apron post (after TF-M5; "a true echo"). `fluted_face`: the cut walls and the parapet stone. `echo_face`: the far apron boulder (Oddny), the inner faces. **No resonance**: no echo-figures, surges or hum (TD-8). |
| State and phasing | **Gallery states (§6.3):** before TF-M5: four spent (grey props), three live (pale props: G3 Shoulder, G5 Lintel, G7 Gate gallery), gatehouse door barred, interior unreachable (TDS10). During TF-M5 per gallery: spent / live / resolved (crew defeated or line cut); G5 unmanned with `TH_STORES = seized`; G7 sheds through `S02`–`S07`. Forced shelter on the cut during `S03` until the rubbing is taken. Slab: half down → wound up (`S05`) → wedged (`S06`) → held by fresh wedges (`S07`) → up and wedged with wardens (`S08`). Post (Act III §E.5): live galleries **pinned dead** with iron straps, G7 cleared (all postures); slab up until deep snow (open), at Ressa's word (watchful), **down** with a postern (sealed_with_terms); roster wall cleaned with bench (open), warden's rail (watchful), closure account slate beside the roster (sealed); Third Horn glyph cut beside the post with `TH_THIRD_HORN`. TDS10 inspect text changes after TF-M5. Thaw event per posture (§E.7). Blizzard is quest-local weather (others see ordinary snow). |
| Used by | TF-M5, TDS10, TF-M5 epilogue and thaw |
| Map | MAP VERIFICATION REQUIRED: G7 directly above the gatehouse; visibility ~25–30 m on the near apron in the cut's lee; galleries readable from the road for TDS10; the far hut's distance is a zone call (§12 Z-6). |

### TP10 The Horn Seat — Ruin/war site, Shatterfall [NEW]

| Field | Requirement |
|---|---|
| Placement | Cut into the gorge wall above the camp shelf, facing **down the shelf**; the rim cairns stand on the rim above it; a short walk from the Salvage Ledge plate shed. |
| Areas | H1 the seat; H2 the **plate rack** (every plate angled down the shelf, three empty slots with fresh pry marks); H3 the **log niche** (lead-lidded tin, ice-wedged; `TES_horn_roster`); H4 the **strata cut** on the camp shelf (buckles, cookpots, a Thornfell-bound horn, all on the near side of the fall) |
| Sound features | The **sounding**: one plate, once; the return comes from below and slightly behind, from the camp shelf, in **two beats**; the far approach is "eight, nine beats off". Positional audio must place the return below. |
| State and phasing | Sounding disabled after `TES_SEAT_SOUNDED` ("You said once."). Rack slots refilled, plates turned to face the rock after TSG `S07`. |
| Used by | TF-M3, TSG |
| Map | MAP VERIFICATION REQUIRED: the camp shelf must be two beats away and the far approach eight to nine. Load-bearing for R06. |

### TP11 Shatterfall Ledges and the Broken Engine — Ruin/war site, Shatterfall [CANON features]

| Field | Requirement |
|---|---|
| Placement | The near wall of the gorge, stepping down from Carrick's Cut to the camp shelf; the far approach at the gorge's other end. |
| Areas | L1 Gust Stair; L2 the Jam (shale, rock-viper ground); L3 the **Lip** (five candidate seams: two solid, three loose); L4 the **Broken Engine** (TDS06; respawn); L5 the **Hollow** (six seams, two solid); L6 camp shelf (strata cut); L7 **seat approach** (~8 m wide, three marked shelter faces; the Held Line arena); L8 miners' ladders (four pitches) to the rim; brake posts at L3 and L5; Horn-Echo **lanes** along L3, L5 and L7 |
| Traversal | L1 shelf gap: A → plank detour; L7 scramble: A → ramp; TDS06 frame climb: A → ledge ramp; scree run L3 → L4 → L5 walkable. |
| Sound features | `fluted_face` along every shelf (chalk-notched shelter faces). `echo_face`: seams (strike and count: quick and flat = solid; slow and doubled = slab). The horn blast and its multiplied echoes (window 2+). |
| State and phasing | TF-M3 storm windows 1–5 (per player; leaving pauses at the current window; Act II §A8.1). Jam cleared after `S03` (`TES_JAM_MINED` / `TES_JAM_CREW`). Irons and rigs persist during the quest. Post-TF-M3: revisitable storm event `storm.shatterfall_world` (Enemies §10.2; proposal). Snow on debris. |
| Used by | TF-M3, TSG (approach from the Cut), TDS06 |
| Map | MAP VERIFICATION REQUIRED: the uphill group must be visible from the Hollow running up L7 toward the Seat. No fall: every lane push goes wallward. |

### TP12 The Salvage Ledge — Camp, Shatterfall [NEW on CANON family]

| Field | Requirement |
|---|---|
| Placement | On old siege works across the gorge from Carrick's Cut (visible from the C5 overlook), above **three lower ledges** with warden pairs, with the spoil terrace above them. |
| Areas | L2 gorge path up (jammed hoist pin; old salvage hoist); L3 outer works (engine frame breastwork); L4 plate shed (camp horn); L5 **ledge lip with three horn-rests**, each aimed at a different lower ledge; L6 spoil terrace on two prop stones; L7 the Horn Seat rack (TP10) a short path away |
| Traversal | Rope traverse: A → old siege ladder route; hoist: break the pin (Mining) or crew → ride. After `TSG_SPOIL = dropped`: a new scramble over the spoil (A → round the head of it). |
| Sound features | `horn_rest` ×3 on the lip (blow Fall; each pair's Answer returns after a few beats; a fourth Answer is the far face's echo of the third). Plates in the shed hum with the calls (tuned stone; proves nothing). `fluted_face` on the approach. |
| State and phasing | Spoil terrace held or dropped (`TSG_SPOIL`); shed standing or pulled down, hoist permanent or rope cut (`TSG_LEDGE` licensed / struck). Brigands only during TSG. |
| Used by | TF-M3 (overlook, presentation only), TSG |
| Map | MAP VERIFICATION REQUIRED: each rest must aim at exactly one lower ledge; the far face must return an echo countable from the third rest. |

### TP13 Carrick's Cut — Camp, Shatterfall [NEW]

| Field | Requirement |
|---|---|
| Placement | Miners' camp at the gorge mouth by the rim. |
| Areas | C1 tally post and chit nail; C2 plate stack; C3 rim winch and horn rail; C4 shelter; C5 overlook to the Salvage Ledge |
| Sound features | `horn_rest`: horn rail (Dorn blows Lost; two Answers return from two places below, each with its own echo count). |
| State and phasing | After TF-M3: thinner camp; after TSG fewer tents (`TSG_LEDGE = struck` thins further; `licensed` honest iron work). TSR Gerrit cameo lines elsewhere. |
| Used by | TF-M3, TSG |
| Map | MAP VERIFICATION REQUIRED: the two Answer sources (the Lip, the Hollow) must be audibly distinct in distance from the rail. |

### TP14 The Rim Cairns — Shrine, Shatterfall rim [NEW on CANON cairn lines]

| Field | Requirement |
|---|---|
| Placement | Along the gorge rim above the Horn Seat; reached from the ladders' head by the rim path; **outside the gorge's storm volume**. |
| Areas | R1 cairn row (names, LOST IN THE GORGE STORM; hollow bases; three reachable); R2 reading stone (side-by-side interaction); R3 cairn niche (slate stopper); R4 rim path |
| Sound features | Rim gusts (TWN-H1), edge blocker. |
| State and phasing | By `TH_SHATTERFALL_ACCOUNT`: **amended** "beneath our own horn" cut under the names; **beside** the tin in the niche behind the slate; **kept** stone silent, roster at Passwatch. TWN rim name inspect reads the same state. |
| Used by | TF-M3 coda, TWN |
| Map | MAP VERIFICATION REQUIRED: the row runs further along the rim than the path does. |

### TP15 The Oath Cairn Fields and Maera's Name-Stone Wall — Shrine [CANON]

| Field | Requirement |
|---|---|
| Placement | Wind-brushed plateaus; the Name-Stone Wall in the upper field; the oath path (TP16) links lower and upper fields; Torvek's cairn-house at the edge [NEW]; the stone ledge above the field, reachable from the Wall without crossing the oath path. |
| Areas | B the Name-Stone Wall (clan stones; rows of slate name-slips at hip height; unmarked stones at the foot); Maera's cairn-hut beside the wall (`amended` roster keeping); C the stone ledge (bedded stone, wedge-holes, shale under the lip, TWN-E1); cairns on squared foundations (TDS04); stormflower field (TME08) |
| Sound features | TDS04: voices carry along the line between two foundations and die off it. Gust windows for TME08 (fallback fixed afternoon). |
| State and phasing | New stone and slip-row props by `TWN_CUT_BOTH` / `TWN_CUT_FAMILY` / `TWN_CUT_OPEN` (the open stone: a newly emerging memorial custom, `[APPROVED — CDR 2026-11-03]`). Stormflowers bloom in a hard-wind window. |
| Used by | TF-M3 coda (register case), TWN, TOS (top), TME08, TDS04 |
| Map | MAP VERIFICATION REQUIRED: ledge reachable from the Wall without the oath path. |

### TP16 Oathkeeper's Step — Shrine/landmark [CANON myth]

| Field | Requirement |
|---|---|
| Placement | On the oath path across a cliff face between the lower fields and the upper field. |
| Areas | A path foot cairn (ribbons; safe point); B the oath path (three crumbling stones pre-repair); C **the step** (dressed block, wear-hollow, iron ring); D **under the arch** (the step is the keystone's top; empty haunch sockets; two dressed blocks in shale, TOS-E1); E an old cairn with matching tool marks |
| Traversal | Cleft: A down-climb from the path → walk round from the field and up the scree. |
| Sound features | Under the arch, the gust is the listening tool (TOS strange moment: the quiet step). |
| State and phasing | `TOS_COMPLETE`: path repaired (per player). Warden marks by `TOS_TOLD` / `TOS_KEPT` / `TOS_WARDEN`. |
| Used by | TOS; TWN approach |
| Map | MAP VERIFICATION REQUIRED: cleft reachable on foot from below. |

### TP17 Echochamber Summit — Unique landmark [CANON]

| Field | Requirement |
|---|---|
| Placement | Stairs climb from a foot off Stonewake's high road to the Summit; whisper hall beside the great hall; the Crown above. |
| Areas | F1–F2 stair foot; S1 outer stair (Narrow Turn crows); S2 inner stair (four air-channel mouths, sconce niches); S3 **Echo Landing**; S4 Upper Landing; W1–W3 **three listening mouths** with nine carry lines; W4 **Counting Room** (null-point); W5 Quiet Passage into alcove V; W6 open stair; G1 dais and the **Wall-Horn** frame; G2 six alcoves I–VI (**II and V null**); G3 **centre stone**; G4 four pillars (pressure shadows, snow wedges); G5 Eyvind's bench (`TSH_trial_record`); G6 great mouth; K1 the Crown (high-route marks) |
| Traversal | S1 broken flight: A → full switchback. Plates are heavy carries (walk only). |
| Sound features | `voice_carry`: mouths and carry lines (solution table, Act II §B8.1, must be physically true in the level: each alcove on exactly two lines from different mouths; null alcoves at a line's far end). `audio_null`: W4, II, V. `pulse_safe`: pillar shadows and silent alcoves. Echo Landing (a footstep from the next landing a beat early; never explained). Air-channel draws (TSH-H2). |
| State and phasing | TF-M4: crew at I, III, VI (+1 at VI with `leverage`); IV empty with a dripping bucket. Entry and start state by `TSH_MAP_TIER`. Node pulses only during `S07`–`S09`. **After TF-M4:** quiet hall; hums in storms without pulses. Plates by `TH_HORN`: **silenced** damped in the null alcoves (Kaldren visits); **broken** cracked plates swept in a roped pile; **surrendered** gone to Three Calls. |
| Used by | TF-M4, TDS02, TF-M5 epilogue |
| Map | MAP VERIFICATION REQUIRED: the whisper-hall geometry is load-bearing (§12 Z-5). |

### TP18 The Silent Gorge — Unique landmark, Ridgewall [CANON]

| Field | Requirement |
|---|---|
| Placement | Null-point ravine below Tower 6 of the Old Watchfire Line; reached by the gorge stair. |
| Areas | G1 gorge stair (iced; rope ring); G2 **the gateposts** (no gate, no hinge marks) and the long stone bench with **four cup-hollows** |
| Traversal | Rope descent: A → cut stair. |
| Sound features | `audio_null` along the ravine floor: wind, footsteps, breath go silent; dust and snow fall straight; tool-straight walls (TDS01). TWG Part 2: the call makes no sound; the frost creeps into the four hollows. |
| State and phasing | None beyond season. |
| Used by | TDS01, TWG |
| Map | MAP VERIFICATION REQUIRED: grass at the rim must visibly move in wind while dust below falls straight. |

### TP19 The Stone With No Shadow — Unique landmark, Stormwake [CANON myth]

| Field | Requirement |
|---|---|
| Placement | On the Stormwake Plateau, on the dusk light line; a nearby cairn offers keep-watch. |
| Areas | The boulder; tool marks at its base. |
| State and phasing | At the dusk window it casts **no shadow** (lighting rule on one object; never explained). |
| Used by | TME06 |
| Map | MAP VERIFICATION REQUIRED: the light line must be readable at dusk from the approach. |

### TP20 The Horn That Never Fell ledge — Unique landmark, Ridgewall cliff [CANON myth]

| Field | Requirement |
|---|---|
| Placement | Cliff ledge above the Old Watchfire Line. |
| Areas | The ledge; a small null-point niche in the rock beside it. |
| Sound features | `audio_null` niche: the player rests a hand on the rock 10 s and feels a two-pulse note (rumble, frost shiver). A call is "heard only when no one is listening" (never staged). |
| Used by | TME05 (TWG does not use it) |
| Map | MAP VERIFICATION REQUIRED: above the Line, off the TWG route. |

### TP21 Red Slope Terraces — Ruin/mine, Stormwake shoulder [NEW, Part 3]

| Field | Requirement |
|---|---|
| Placement | Below the Stormwake Plateau's shoulder; **Kettlecrag upslope and Brackenstep downslope (both off-map)**; the TME10 hollow below. |
| Areas | A lower terrace gate (two highstead camps, Gerrit's fire); B war walls (teaching stones); C plot terrace (five plank-shut cellar mouths; marker stones); D shrine niche (plot list); E the scarp (shale fans, rust bands, sounding stations, TSR-E1); F the upper face (mining site); the hollow below (TME10 bell) |
| Traversal | Scarp: A scramble → old wall-steps along the terrace ends. |
| Sound features | `echo_face`: tap and count (grave voids vs ore). TME10: the hollow swallows the bell. Chalk shelter faces on the scarp. TSR-H1 slab drop lane chalked. |
| State and phasing | Post-quest props by `TSR_SEAM` (shared / brackenstep / kettlecrag). |
| Used by | TSR, TME10 |
| Map | MAP VERIFICATION REQUIRED: the upper face must be clear of the plots' ground. |

### TP22 The Old Watchfire Line — Ruin, Ridgewall [CANON feature]

| Field | Requirement |
|---|---|
| Placement | Six horn towers along a Ridgewall crest; T1 nearest the Windscar track, T6 above the Silent Gorge. |
| Areas | T1–T6 (see TWG.4): T1 groove bank (seventh channel clean); T2 collapsed stair, Warden's ladder in snow; T3 ice-packed seventh channel, wren in the Gather channel; T4 bandit lookout hide; T5 ice-sheathed parapet; T6 lintel **WITNESS AT THE GATE**, seventh channel aimed down into the gorge; cairn lees at tower feet; fluted faces between towers (TWC rite walk) |
| Traversal | T2: A rubble → carry and set the ladder; T3: scramble → inner-wall steps; T5: parapet → interior stair. |
| Sound features | `groove_bank` per tower (TDS03: a call carries to the next tower and dust jumps in its mouth). TWG Part 1: the call runs T4 → T5 → T6 and cuts off over the gorge lip. |
| State and phasing | T2 ladder stays with `TWG_LADDER_SET`. T4 hide empty after TWG. Signal Terrace sightline to the first tower (TNK). |
| Used by | TWG, TWC (rite walk: walking the banner home, Old Torvek's own practice that others are starting to follow, not a Thornfell-wide custom; `[APPROVED — CDR 2026-11-03]`), TDS03, TNK (answers) |
| Map | MAP VERIFICATION REQUIRED: each groove bank aims along the crest at the next tower. |

### TP23 Abandoned Ridge Camp — Ruin/war site, Ridgewall [CANON feature]

| Field | Requirement |
|---|---|
| Placement | On a Ridgewall route that joins the Old Watchfire Line and descends to Stonewake. |
| Areas | Shattered palisade; ash pits in a row (TDS05); fallen bunk-house with one bunk-board; stacked cook-pots; wolf den under the collapsed gate (TWC-E1) |
| State and phasing | Wolves → world population. |
| Used by | TWC, TDS05 |
| Map | MAP VERIFICATION REQUIRED. |

### TP24 Burned Slope — Ruin/war site, Ridgewall [CANON feature]

| Field | Requirement |
|---|---|
| Placement | Ridgewall slope of crag-pine and stormwood regrowth through ash. |
| Areas | B slope foot (Brita's rock; hollow burned stumps); C three stands (chalk-faced lees); D the upper stand (last good stool) |
| Sound features | `fluted_face` above the stands; in a gust cracked stems sing and the hollow stumps moan (TST wonder). |
| State and phasing | Upper stand by `TST_STEM` (seeded: red rag and seedlings; wardens: stump with a tally notch). |
| Used by | TST, TDS09 |
| Map | MAP VERIFICATION REQUIRED. See §12 Z-2 (not the same place as TF-M1's stormwood slope). |

### TP25 Greymantle's Den — Cave, Stormwake [NEW]

| Field | Requirement |
|---|---|
| Placement | In Stormwake within reach of the hostel road; the kill cache between the fold and the den. |
| Areas | G2 broken fold; G3 print line; G4 rubbing pine; G5 kill cache under an overhang (crow column visible from G4); G6 bare rock with the frost stripe; G7 den approach; G8 outer cave (ordinary sound); G9 **inner chamber** (round, three free-standing pillars, the hollow, thick dust) |
| Traversal | G7: A ledge shimmy → long switchback. |
| Sound features | `audio_null` at the G8 → G9 threshold, layered over 2 s (drip, wind, footsteps, breath). |
| State and phasing | By `TGM_OUTCOME`: **ended** empty den; **sleeping** stacked threshold and stormflower net (his resting place), Yrsa's small cairn below the den. |
| Used by | TGM |
| Map | MAP VERIFICATION REQUIRED: pillars must be far enough from walls to stop charges and to hide him in P3. |

### TP26 The Blind Corners — Bandit site, Windscar [NEW on CANON]

| Field | Requirement |
|---|---|
| Placement | Three tight switchbacks between the Passwatch gate and the Narrows; the mule cache (TAS P5) below them on the Passwatch side. |
| Areas | Switchbacks; the overturned handcart at the second bend; slingers' ledges; the **goat track** above with a frayed hand-rope; the Corner Stone on the goat-track shoulder (TTH B2; cadet drill stakes); the mule cache overhang |
| Traversal | Goat-track gap: A → 15 s scramble round a boulder; the switchback road has its own steps up to the Corner Stone. |
| Sound features | `horn_rest`: Corner Stone. |
| State and phasing | Bandit world pocket after TF-M1 (Enemies TW-01). |
| Used by | TF-M1, TF-M2 and TF-M5 travel, TTH, TAS |
| Map | MAP VERIFICATION REQUIRED: the goat track must come down **behind and above** the slingers. |

### TP27 The Iron Winter Muster Hut — Camp, Windscar [NEW]

| Field | Requirement |
|---|---|
| Placement | On the hut shoulder (K4) of the Whinstone track below the store. |
| Areas | H1 drill yard (spear rack; straw "Emberholt" target); H2 hut wall (horn by the door; **the broadsheet**; chalk pay board); H3 the ledge rail with a broadsheet copy on the K5 route |
| Sound features | `horn_rest` by the door (hornman drill); drill noise carries down the track. |
| State and phasing | TF-M2: drill in progress. After: empty (`reported`, `seized`) or still drilling with `leverage` until TF-M5 (Enemies TW-02). After TF-M5: empty in every outcome. |
| Used by | TF-M2 |
| Map | MAP VERIFICATION REQUIRED: the broadsheet must be in view from both routes (required pass-by). |

### TP28 Goat Ledges of the Stormwake Shoulder — Hunting ground [NEW]

| Field | Requirement |
|---|---|
| Placement | On the Stormwake shoulder; Bera's shieling at their foot; the goat shoulder above Nettlehook (TSM E) is their near edge. |
| Areas | A shoulder path (moss-marked niches; heather below); B the warm stretch; C ledges with three **call-stones**, each facing a different cliff; D high ledges (drive target); E the **blank face** (goat steps); F Bera's shieling and shed |
| Traversal | Goat steps: an agility route enabled after `TGY_STEPS_SEEN` → the ledge path. |
| Sound features | `horn_rest`: call-stones (Gather and Fall drive the herd; each stone's facing determines where the call carries). |
| State and phasing | Herd by `TGY_WAY` (cull: young ram bluffs travellers; drive: herd on the high ledges). |
| Used by | TGY, TSM (edge) |
| Map | MAP VERIFICATION REQUIRED: each call-stone must face a distinct cliff that returns the call. |

---
## 5. New places invented by the packages [NEW] (not counted as POIs unless noted)

| Place | Parent / subzone | Relative placement | Traversal | Sound features | State | Used by | Source |
|---|---|---|---|---|---|---|---|
| **Splitpine Crag** [NEW] | Stormwake Plateau | Visible from the Stormwake warden shelter's slot; across open plateau; a further ridge visible **only** from its summit block | Pitch one: A chimney (three triggers) → goat ramp + clip the warden line (4 s); hawk ledge (four stances); summit block; rappel down (4 s) | Fluted face on the hawk ledge; stormlight hum (TSL-H2) near the block; lee notch with a three-stone cairn | Banner wound on the split pine (TSL); staff left or taken (`TSL_STAFF_LEFT` / `TSL_STAFF_TAKEN`); a fixed warden line after TSL (per player) | TSL; TWC (rally-mark reading) | Banner TSL 1.4 |
| **Stormwake warden shelter** [NEW] | Stormwake Plateau | Facing the crag; storm marks on the door frame | — | Keep stormwatch (storm window wait) | — | TSL; TDS08 (cairn gap nearby) | Banner TSL 1.4 |
| **Stormwake rut ground** [NEW] | Stormwake Plateau | A trampled hollow on the direct thread line between shelter and crag; skirtable along the scarred stones | Walkable | — | Fell Stags pocket; Storm Stag (proposal TW-05) | TSL | Banner TSL 1.4 |
| **Kettlecrag** [NEW] | Off-map highstead | Upslope of Red Slope Terraces | **Off-map; never visited** | — | `TSR_SEAM` reads its name | TSR | Work TSR.3 |
| **Brackenstep** [NEW] | Off-map highstead | Downslope of Red Slope Terraces | **Off-map; never visited** | — | `TSR_SEAM` | TSR | Work TSR.3 |
| **Torvek's cairn-house** [NEW] | Oath Cairn Fields edge | At the field's edge | Walkable | — | — | TWC | Banner TWC 2.4 |
| **The stone ledge** [NEW] | Oath Cairn Fields | Above the field; reachable from the Wall without the oath path | Walkable | — | New stone by `TWN_CUT_*` | TWN | Banner TWN 3.4 |
| **The Whinstone track** (K1–K5) | Windscar | Leaves the pass road beyond Three Calls and climbs the cliff above the pass; not on any patrol board | §3 R2 | `audio_null`: **K3 quiet gully** (haul crew voices stop mid-word); fluted cuts on K5 | Sledge grooves fresh in M2 | TF-M2 | Act I §B5.3 |
| **The high track** (C2–C6, warden posts W1–W4) | Windscar | Above Three Calls toward the Gatefall along a cliff face, rope-railed on the drop side; the drovers' fork roped shut | §3 R3 | `horn_rest` W1–W4; `fluted_face` on the Fluted Run; `echo_face` at the Fork (direct call, then the echo off the far face from the wrong side); red-rag niches every 40 paces | Whiteout only during TF-M5 `S01` and `S07` | TF-M5 | Act III §5.1 |
| **The stormwood slope** (W3) | Windscar | Burned-over slope **below the Narrows** | Walkable | — | — | TF-M1 | Act I §A5.2 |
| **The far apron, far track and far hut** | Beyond TP09 | Beyond the slab; the far hut "some distance out" | Whiteout rules in TF-M5 | `echo_face`: Oddny's boulder | Post: far-hut winterers (sealed_with_terms) answer Dorn's dusk Lost | TF-M5 | Act III §5.2 |
| **Hushfold's far shielings** | Beyond TP09 | Beyond the far hut | **Never visited** in Thornfell content | — | Named on the Outside slate by posture | TF-M5 (named) | Bible §4.2 |
| **TTH answering stones** B1 Gate Stone, B2 Corner Stone, B3 Narrows Stone, B4 Shelter Stone | Windscar (R1) | Outside the Passwatch gate; Blind Corners goat-track shoulder; near-side bluff above the Narrows under three fluted faces; Three Calls ledge lip | Corner Stone: goat-track trigger → road with its own steps | `horn_rest` (mouth-hollows at horn height); Narrows Stone strange return (once per player) | Restored reply glyph by `TTH_KEEPER` | TTH | Horn TTH.5 |
| **The mule cache** (TAS P5) | Windscar | Rock overhang below the Blind Corners on the Passwatch side | Road; goat-track shortcut (A → road) | — | Bandits during TAS only | TAS | Settlements TAS.5 |
| **The TGM tracking ground** (G2 fold to G6 bare rock) | Stormwake | Shieling shelf → print line → rubbing pine → kill cache → bare rock → den | Walkable; nothing timed | Crow column visible from G4 | Stages persist | TGM | Settlements TGM.5 |
| **TME04 safe stretch** | Ridgewall | Between Nettlehook and Hushfold; a rock with child-height marks | Walkable | — | Fixed morning after TF-M1 | TME04 | Settlements TME04 |
| **TME07 Ridgewall track** | Ridgewall | By Nettlehook | — | — | Daytime after TF-M1 | TME07 | Settlements TME07 |
| **TME09 stepped ledge** | Ridgewall | "A ledge Iven names"; added to the map after any talk with Iven post-TF-M1 | Walkable | Echo before sound (third step) | Once per visit | TME09 | Settlements TME09 |
| **Bera's shieling** | TP28 foot | — | — | — | Leatherworking station | TGY | Work TGY.3 |
| **Brita's stall and the wind butts** | TP01 | Ridge-market; terrace lip; the butts are the bowyer's marks for TST's shooting step (CDR-2), with a clear standing line and a safe backstop on the terrace lip | — | Ribbons show the wind | — | TST | Work TST.3 |

**Named NPC homes inside POIs** (Brede, Kvist, Skarde houses; Maera's cairn-hut) are sub-areas of their POIs, not places.

---

## 6. Zone-state table (per player)

All states are **per-player presentation** (bible §9). Co-op fallback: the host's props, as presentation only; each player's own flags drive their own barks, dialogue and epilogue, and no player's step waits on another player's prop state (Narrows bridge, Passwatch gate: scree path and wicket stay open; CDR-6).

### 6.1 Keyed by region flags (`TH_`)

| Flag = value | Where it shows | What changes |
|---|---|---|
| `TH_CALLS` = true | Everywhere | Call-shape glyphs for every heard call; echo-count ticks; marker glyph inspects at TP09 (TDS10) |
| `TH_PASSWATCH_ROUTE` = sledge / caravan / split | TP03, TP06 | Nettlehook granary full / lean / middling (watchful and sealed postures; open tops it up); split: stable smell and broken halter on the Three Calls ledge (TTH) |
| `TH_SEASON` = autumn | All | Until TIW `S13_elira` starts (TF-M2's last step; C-7): sleet, slush, bare props. TAS and TTH/TWG/TNR have autumn variants (grit in flutes instead of snow) |
| `TH_SEASON` = snow | All | From TIW `S13_elira` start: snowfall effect and a short list of snow-cover props (stair treads, rim, market, highsteads). No NPC wardrobe change |
| `TH_STORES` = reported | TP08; TP17; TP09 | Store sealed, Warden at the hoist foot; TF-M4 standard crew; G5 crew of 3; pull-line coil stamped "W." |
| `TH_STORES` = seized | TP08; TP09 | Store empty, racks bare; G5 **unmanned**; pull-line stamp absent |
| `TH_STORES` = leverage | TP08, TP27; TP17; TP09 | Store still filling and guarded, hut still drilling until TF-M5 (Enemies TW-02/03); +1 spear in alcove VI; G5 crew of 4 with new spearheads (G3 standard); Ingrith P2 +1 |
| `TH_BRYNJAR` = disowned / defended | TP01 | Post: Brynjar at the ridge-market with Elira / at the Blood-Oath towers; Assembly placement |
| `TH_SHATTERFALL_ACCOUNT` = amended / beside / kept | TP14; TP15; TP02 | Cut line under the names / tin in the cairn niche / roster in the Passwatch strongbox; TWN reads it in place |
| `TH_HORN` = silenced / broken / surrendered | TP17; TP01; TP06 | Plates damped in alcoves II and V / cracked pile roped off / crated at Three Calls; Wardens' store contents for TNK |
| `TH_THIRD_HORN` = true | TP06; TP09 | Horn map Third Horn mark chalked fresh; Third Horn glyph cut beside the Gatefall post (post-TF-M5); the player can blow it on the far apron |
| `TH_HUSHFOLD_VOICE` = true | TP01 | Hushfold standing mark on the hall floor by the stone (all postures, post) |
| `TH_HIGHSTEADS_TOGETHER` = true | TP03; TP01 | Witness ribbon on the ropeway pylon; Nettlehook beside Hushfold in the hall |
| `TH_BANNER` = blood-oath / hearthguard / shared | TP01 | Where the banner hangs and who stands near it at the Assembly (TWC owns the prop) |
| `TH_COLUMN` = player_brought / patrol_brought | TP09; TP04 | Stragglers inside the gate at once / arrive with Vessa's patrol at dawn; Hushfold barks |
| `TH_STAND` = hushfold / wardens / cairn / brynjar | TP01 A5 | The player's standing place; NPC placements around it |
| `TH_ASSEMBLY_POSTURE` = open / watchful / sealed_with_terms | TP01, TP02, TP03, TP04, TP08, TP09 | The epilogue tables (Act III §E.1–E.6): slates, boards, slab position, relief line, roster wall furniture, store use |
| `TH_HORN_CODES` = kept / pruned | TP01 Signal Terrace | Code book on the lectern; TNK's last call (unanswered Witness / Rest counted in) |
| `TH_STANDING` = true | TP02, TP06, TP04, TP07, TP01 | Four master-commission givers at their posts (Aud, the bowyer, Ressa, Runa) |

### 6.2 The Narrows bridge (TP07)

**Canonical for implementation; quest packages defer to this register** (§12 C-6). One per-player state machine; each quest writes only its own transition. N2 is shown **only while TBC is Active** and overrides N1, N3 or N4 for that player; before TBC is accepted the bridge shows its ordinary state. The scree path is walkable in every state.

| State | Condition | Presentation | Walkable route |
|---|---|---|---|
| **N0 down** | TF-M1 before `S08_span` complete (and before TF-M1 is started) | Old bridge tangled on the near anchors; far anchors under scree | Scree path through the gap (S1–S3) |
| **N1 patched** | TF-M1 `S08_span` complete | New footropes and handlines, swaying | Span; scree path |
| **N2 cracked** | **TBC Active only** (§12 Z-1) | Far anchor rock split; span hanging by its guide line; families and loads waiting | Scree path (always); guide-line traverse or bosun chair to the far rock |
| **N3 mended** | TBC Completed | Span with new fittings; repair post carved (second line with `TBC_WAIT_NAMED`) | Span; scree path |
| **N4 permanent span** | TRR Active or Completed | New span beside the stumps of the storm patch; kneel marks; meal ledge props during TRR | Span; scree path |
| Thaw | `TSW_THAW` | The Narrows run loud with meltwater | As current state |

### 6.3 The Gatefall galleries and gate (TP09)

| Phase | G1, G2, G4, G6 | G3 Shoulder | G5 Lintel | G7 Gate gallery | Slab | Gatehouse |
|---|---|---|---|---|---|---|
| Before TF-M5 (TDS10) | Spent, grey props | Live, pale props | Live, pale props | Live, pale props | Up (open gate) | Door barred; interior unreachable |
| TF-M5 `S02` | Spent (no Answer to their call) | Live → resolved (crew defeated or line cut) | Live → resolved; **unmanned** with `seized` | Ingrith draws its pins; sheds on the far apron | Half down | Crew camp; roster under soot |
| TF-M5 `S03`–`S07` | — | Resolved | Resolved | Sheds on a rhythm (Fall + grit) | Half down → wound up (`S05`) → wedged (`S06`) → fresh wedges (`S07`) | Roster wiped and rubbed (per panel, persistent) |
| TF-M5 `S08` dawn | — | — | — | Quiet | Up and wedged, wardens on it | Hushfold bedded in the warden room |
| Post (all postures) | Spent | **Pinned dead** (iron straps) | Pinned dead | Cleared, loose stone barrowed off | By posture (Act III §E.5) | Cleaned roster wall; furniture by posture; child's mitten on the drill-board peg |
| Thaw | — | — | — | — | Thaw event by posture (shared opening / wardens raise / relief line home) | Roster visited (Runa / Vessa / the winterers) |

### 6.4 Other quest-local states that change a place

| Flag | Place | Change |
|---|---|---|
| `TPW_CLOSE_COUNT` | TP02, Windscar near stretch | Sky darkens and sleet thickens per Close (TF-M1 only) |
| `TIW_CAGE_WOUND` | TP08 | Cage rides hoist foot ↔ winding head |
| `TES` storm windows 1–5 | TP11 | Gust cycle, haze, Horn-Echo activity (TF-M3 only) |
| `TSH_MAP_TIER` | TP17 | Entry route and crew start state |
| `TSW` blizzard (quest-local) | Windscar high track, TP09 | Whiteout ~3 m (`S01`, `S07`); others see ordinary snow |
| `TSW_THAW` | All Thornfell | Snow props → meltwater and wet stone; goats back on the ledges; Gatefall thaw event `[APPROVED — CDR 2026-11-03]` |
| `TSL_STAFF_LEFT` / `_TAKEN` | Splitpine Crag | Staff in the crack or gone |
| `TWG_LADDER_SET` | TP22 T2 | Ladder stays |
| `TOS_COMPLETE` | TP16 | Path repaired |
| `TSR_SEAM` | TP21 | Seam works and camp props |
| `TST_STEM` | TP24 | Seed stool with a red rag, or a tallied stump |
| `TGY_WAY`, `TGY_STEPS_SEEN` | TP28 | Herd location; goat-steps route |
| `TGM_OUTCOME` | TP25 | Empty den / stacked threshold and net with Yrsa's cairn below (sleeping) |
| `TSG_SPOIL`, `TSG_LEDGE` | TP12 | Terrace held or dropped (scramble route); shed and hoist kept or struck |
| `TSN_*` | TP05 | Drift post recut / told / left |
| `TBC_WAITS`, `TBC_WAIT_NAMED` | TP07, TP06 | Who sleeps at Three Calls; repair post lines |
| `TWN_CUT_*` | TP15 | New stone text |
| `TNR_ROTA` | TP03 | Rota board pegs |

---

## 7. Season, weather and phasing rules

| Rule | Requirement |
|---|---|
| Season | `TH_SEASON` has two values only: **autumn**, then **snow** from TIW `S13_elira` start (bible §9.2). No world clock. Thaw is **quest-local** `TSW_THAW` `[APPROVED — CDR 2026-11-03]` (C-7); no third `TH_SEASON` value. |
| Storm and blizzard | Every storm, storm window, whiteout, Close sky and stormlight is **per-player quest-local presentation** (keep-watch convention), never world weather. Leaving a zone pauses a quest storm at its current window. |
| Gust tell | One convention: fluted face whistles up a fifth **2.5 s** before a **3 s** gust; push 2 m toward the safe side (C-1; TST's ~6 s long gust is the one exception). The level supplies the face, the lane and the marked shelter. |
| Wind windows on climbs | Pushes go wallward or to the last stance; never off. |
| Null-points | Audio-null volumes must fade layers in order over ~2 s at the threshold and restore in order on exit (drip first back). |
| Lightning | TSL storm window guarantees flashes at readable intervals and a guaranteed active storm on the summit while `S07` is active. |

---

## 8. Relative placement, sightlines and exclusions

All **MAP VERIFICATION REQUIRED**.

### 8.1 Must be near or in sight

| Place | Must be near / see | Why |
|---|---|---|
| Passwatch horn post | Close calls audible across the near stretch to the Narrows; the cliffs return the span Close early | TF-M1 clock and strange moment |
| Narrows near side | The far loads across the gap; the far bridgehead sees Three Calls' lantern | TF-M1 choice; TBC |
| Track foot (K1) | Beyond Three Calls; forks to the Whinstone switchbacks and to the high track | TF-M2, TF-M5 |
| Whinstone counting room loophole | Straight down the cliff to the pass | TF-M2 G7 |
| Gatefall galleries | Readable from the pass road before TF-M5 | TDS10 |
| Carrick's Cut overlook | The Salvage Ledge across the gorge | TF-M3 seed for TSG |
| Horn rail at the Cut | Two Answer sources at audibly different depths | TF-M3 Beat 1 |
| The Hollow | The camp shelf below and the seat approach; the uphill group's path to the Seat | TF-M3 strange moment |
| Horn Seat rack | Returns from the camp shelf in two beats; far approach eight to nine beats | TF-M3 R06 |
| Rim cairns | Above the Seat; outside the storm volume | TF-M3, TWN |
| Summit stair foot | Off Stonewake's high road | TF-M4 |
| Signal Terrace | Passwatch tower, Nettlehook ropeway head, Three Calls ledge, Hushfold smoke, first watchfire tower | TNK |
| Stormwake warden shelter | Splitpine Crag summit block through the bench slot | TSL |
| Splitpine Crag summit block | The further ridge (TDS07 glimpse), visible from the block only | TSL Part 3 |
| Old Watchfire Line T6 | The Silent Gorge below its downward seventh channel | TWG |
| Salvage Ledge rests | Each aims at one lower ledge; the third rest's Answer echoes off the far face | TSG |
| TGM G4 rubbing pine | The crow column over the kill cache | TGM |
| Black Glass Hostel door | Faces the prevailing drift | TSN |
| Stone With No Shadow | On the dusk light line | TME06 |

### 8.2 Must not be seen or reached

| Constraint | Why |
|---|---|
| Any route, road or direction by which the Lowmark relief grain reached Thornfell | FT-03 / TD-11 |
| Any compass direction toward Emberholt | TD-6 |
| Whinstone Store interior before TF-M2 `S05`; Gatefall gatehouse interior before TF-M5 | Story gating |
| The Hushfold far shielings, Kettlecrag, Brackenstep | Off-map; named only |
| The drovers' path beyond the Fork rope | TF-M5 rope boundary |
| Off any ledge, rim, span, parapet, crag or plank | No fall deaths |
| Any Horn-Echo figure outside Shatterfall's storm volume; any node pulse outside the great hall | Bible §2.4; TD-8 |
| Remnant presence anywhere | FT-04 bounded reach |

---

## 9. Integration dependencies (documented only; nothing implemented)

| Need | Owner | Minimum viable form |
|---|---|---|
| Tagged sound-feature volumes (§0.2) | Systems + level design | `fluted_face` with gust lane; `shelter_safe`; `echo_face` with distance bands; `horn_rest` with facing; `audio_null`; `voice_carry`; `pulse_safe`; `rope_boundary` |
| Per-player bridge state (§6.2) | Systems (33.1-style per-player state) | Five presentation states; scree path always navigable |
| Per-player gallery and slab states (§6.3) | Systems | Gallery enum (spent / live / resolved / pinned); slab position set |
| Season swap and thaw | Systems + art | Two prop lists (autumn, snow) and one thaw list |
| Epilogue posture props | Systems + art | Prop sets per `TH_ASSEMBLY_POSTURE` × place (Act III §E) |
| Multi-level NavMesh and interaction-driven climbs | Systems | Shaft rungs, ladders, crag pitches, tower stairs, winch floor |
| Edge blockers and push clamps | Systems | Every edge in §8.2 |
| Assembly Hall placement sets | Systems + NPC | Per-player NPC positions keyed on flags (Act III §8.4) |

---

## 10. Phase 1.5 count check

| Category (Phase 1.5 §3) | POIs | Count |
|---|---|---|
| Settlements | TP01, TP02, TP03 | 3 |
| Micro-settlements | TP04, TP05, TP06 | 3 |
| Ruins / war sites | TP09, TP10, TP11, TP22, TP23, TP24 | 6 |
| Caves / mines | TP08, TP21, TP25 | 3 |
| Camps / bandit sites | TP12, TP13, TP26, TP27 | 4 |
| Shrines | TP14, TP15, TP16 | 3 |
| Unique landmarks | TP07, TP17, TP18, TP19, TP20 | 5 |
| Hunting grounds | TP28 | 1 |
| **Total** | | **28** (range 24–32) |

**New places** in §5 are quest sub-spaces or off-map names, not counted. Splitpine Crag is the only one large enough to be a candidate POI (unique landmark); adding it makes 29, still in range (§11 Q2).

---

## 11. Open map questions for the Director

1. **Track foot fork (§1):** approve one track foot beyond Three Calls forking to the Whinstone switchbacks and the high track?
2. **Splitpine Crag:** keep as a TSL sub-space or count it as TP29 (unique landmark)? The TSL package invites a dossier-style rename.
3. **Far hut distance** from the Gatefall far apron (Act III leaves it to the zone pass): recommend one whiteout leg (~the length of the Fluted Run) so both stragglers are findable in one search.
4. ~~Thaw~~ **Resolved 2026-11-03:** quest-local `TSW_THAW`; `TH_SEASON` stays two-valued.
5. **Kettlecrag and Brackenstep** stay off-map in Thornfell content?

---

## 12. Inconsistencies found and recommended canonical values

**Shared canonical register (canonical for implementation; quest packages defer to this register).** Added in the independent review of 2026-11-03. The three Batch 4 handoffs (Enemies, Zones, Integration) state these values in the same words. Where a quest package gives a different number, the package value is superseded for implementation; the package text changes only when its author next edits it.

| # | Topic | Canonical value |
|---|---|---|
| C-1 | Wind window | Fluted face whistles up a fifth **2.5 s** before a **3 s** gust. The gust pushes **2 m toward the defined safe side** with light damage, no knockdown, never off an edge; a marked shelter negates it. TF-M5 whiteout adds a 3 s slow; climbing stances keep "back to the last stance / hang on". One exception: TST stand-cutting gusts last ~6 s (a labelled "long gust"; same 2.5 s tell). |
| C-2 | Hazard clamp | No hazard can kill a player above **25% HP**; TSL-H2 stormlight clamps at **10%**. |
| C-3 | Hornman | Raise **1.5 s**; Gather gives allies within 8 m faster attacks for **8 s**; any hit during the raise interrupts; the player's **Rest within 3 s** cancels it in every hornman pocket. |
| C-4 | Howler and calls | Draw **1.5 s**; a completed howl adds **+1 runner once** (TPW-E3 keeps +2 as authored escort pressure). Any call blown at a howler makes it flinch; Fall also makes bandits duck once per fight. |
| C-5 | Ridge Wolves at low health | **Removed by CDR-1 (2026-11-03).** Wolves fight until defeated at 0 HP; no break-off, no limp-away. Step and co-op credit at defeat. |
| C-6 | Narrows bridge (TP07) | One per-player state machine, owned by the Zones package: **N0 down** (before TPW `S08_span`) → **N1 patched** → **N2 cracked only while TBC is Active** (overrides N1, N3 or N4 for that player) → **N3 mended** (TBC Completed) → **N4 permanent span** (TRR Active or Completed). Before TBC is accepted the bridge shows its ordinary state and TBC is offered by Aud's bark after a storm. The scree path is walkable in every state. |
| C-7 | Season and thaw | `TH_SEASON` has two values: autumn, then snow from TIW `S13_elira` start. Thaw is the quest-local bool `TSW_THAW` (first re-entry to Thornfell after TF-M5 Completed and leaving the region once) **[APPROVED — CDR 2026-11-03]**; no third `TH_SEASON` value. |
| C-8 | Ranged | **S01 resolved by CDR-2.** Ranged is a first-class option in every fight and is never required; every counter that names Ranged also has a melee, brace or call answer. No fight is designed so ranged trivialises it (no boss shootable from a place it cannot reach). TST teaches the bow (cut, string, fletch, shoot); the racked unstrung stave is only the bowyer's display piece. Weapon, ammunition and XP values belong to the item and systems specialists. |

| # | Inconsistency | Packages | Recommendation |
|---|---|---|---|
| **Z-1** | **Narrows cracked state scope.** TBC asks for a per-player cracked bridge "after TF-M1 until TBC completes". That would show a broken bridge during TF-M2 (`S03` says "over the Narrows (repaired)"), TF-M5 travel, TTH at the Narrows Stone and TRR, for any player who never takes TBC. TRR needs a permanent span "after TBC or regardless" (TBC open decision 4). | Work TBC.11, TBC.15; Act I §B6; Horn TRR | **Cracked (N2) only while TBC is Active** (C-6; canonical for implementation; TBC.1 and TBC.11 now agree). Before acceptance, TBC is offered by Aud's bark at the bridgehead after a storm with the bridge patched. TRR's permanent span (N4) applies regardless of TBC; if TRR completes first, TBC's storm splits the far anchor **rock** under the permanent span (text variant only). The scree path is always walkable, so no quest is ever blocked. |
| **Z-2** | **Two stormwood slopes.** TF-M1 W3 is "a burned-over slope below the Narrows where stormwood grows" (Windscar); TST uses TP24 Burned Slope (Ridgewall). | Act I §A5.2; Work TST.3; bible §4.2 | **Two places.** W3 is a Windscar minor site; TP24 is the Ridgewall POI. TST's inspect lines may nod to "the slope below the Narrows" only as a second, smaller stand. |
| **Z-3** | **Three Calls horn map** is "painted on its back wall" (Act I), "cut into the back wall" (Act III), "painted across four wall boards" (TTH). | Act I; Act III; Horn TTH.5 | **Painted on four boards fixed to the cut back wall**; Ressa chalks on the boards. Text-only edits in Act III if desired. |
| **Z-4** | **Assembly Hall seating.** TWC: "benches by clan in a horseshoe round the speaking stone; Hadrik's chair lower". Act III: "Nobody sits. People stand where Hadrik places them." TMM: galleries on three sides, Hadrik sits in the far gallery at night. | Banner TWC 2.4; Act III §5.3; Settlements TMM.5.3 | **Both are true by occasion.** Fixed stone benches in a horseshoe and galleries exist; at a closure sitting (TF-M5) custom is that everyone stands. Act III's cairn bench and Brynjar's stone table are part of the same furniture. Level design builds one hall. |
| **Z-5** | **Whisper-hall geometry** must make the Act II §B8.1 solution physically true (each alcove on two lines from different mouths; null alcoves at a line's far end; IV audible but empty). | Act II §B8.1 | Treat the table as a level-design spec, not just audio; test before art. MAP VERIFICATION REQUIRED. |
| **Z-6** | **Passwatch training board**: six painted call-shapes and a seventh row painted over in grey (Act I) vs seven rows of peg holes with painted glyphs, the seventh with a prised-out peg and a scraped label (TTH). | Act I §A5.1; Horn TTH.5 | **One board with both**: painted glyphs above peg rows; seventh row painted over in grey, two short pegs and a gouged hole, the ghost of a rising line under the paint. |
| **Z-7** | **TDS10 marker glyphs** "recognisable from the Ordinary Calls … plus a few they don't" vs Act III: every marker is Close (two falling bars) plus a tag that never uses Gather or Fall shapes. | Settlements TDS10; Act III Beat 2 | Compatible: the player recognises the **Close** bars on every marker and not the tags. One wording tweak in TDS10. |
| **Z-8** | **Wind-window lead time** differs by package (1.5 s / 2.5 s / ~3 s / "two breaths"). | All | **2.5 s**, gust 3 s (C-1; Enemies §13 I-1). Level design sizes gust lanes so a walking player reaches shelter in 2.5 s from any point on a required path (shelter spacing ~40 paces on the Fluted Run is the reference). |
| **Z-9** | **Hushfold placement** for the column: Hushfold sits above the pass road (TSM) yet the column comes from the far shielings beyond the Gatefall. | Horn TSM.4; Act III | Compatible: Hushfold's houses are on the near side; its herds and far shielings are beyond the far gate. State it once in the map note. |

---

## 13. Review log

| Check | Result |
|---|---|
| Coverage | TP01–TP28 each have placement, areas, traversal, sound features, state, use and map note; §5 lists every new place found in the packages (Splitpine Crag, Kettlecrag, Brackenstep off-map, the Whinstone track, the high track, the far hut and shielings, the TTH stones, Torvek's cairn-house, the stone ledge, the rut ground and others). |
| Traversal | Every agility trigger has a walkable fallback named; the Narrows scree path keeps every bridge state passable. |
| Sound system | Fluted faces, shelter faces, echo faces, horn rests, groove banks, null-points, carrying spots and pressure shadows tagged and located. |
| Phasing | Zone-state table keyed by every `TH_` flag in bible §9.1 that changes a place, plus the Narrows, Gatefall, season and thaw tables. |
| Binding rules | No route for the Lowmark grain; no compass direction toward Emberholt; no resonance at the Gatefall; Horn-Echo and node limited to their sites; no Remnant; no fall deaths. |
| Scope | No schema, JSON, scene data or C#; dependencies only. |
| Name changes (2026-11-03) | This file names no roster or name-slip family; the review-pass renames (the name-slip "Sig Brede", the roster's Lunde family, the Tofte carters) need no edit here. |
| **Reconciliation needed** | The four side-quest files were under independent review while this file was written. **After those reviews land, re-check §4 and §5 place rows taken from side quests, the §6.4 flag names, and Z-1, Z-2, Z-4, Z-6, Z-7 against the revised text.** Main-act rows reflect the committed packages. |
| **Independent review (2026-11-03)** | 6 findings (0 high, 4 medium, 2 low). Grep checks against the committed packages: every flag in §6 exists; POIs match bible §4.2. Medium: stale names fixed (Hild Crane → **Brita Crane** ×4: stall, bow stall, rock, §5 row; Signy Brack → **Thyra Brack**; Hallvor → **Leiv**); the Kvist, Brede and Skarde houses already matched. Medium: `leverage` gave G3 new spearheads; Act III puts them on G5 (crew of 4), G3 is standard; fixed. Medium: the shared canonical register (§12 C-1 to C-8) added, identical in all three handoffs. Medium: the Narrows model now states N2 overrides other states and appears only while TBC is Active; TBC.1 and TBC.11 edited to agree (logged in that file). Low: `TH_SEASON` turns at TIW `S13_elira` start, not "TF-M2 completion"; aligned. Low: thaw restated as quest-local `TSW_THAW` [PROPOSAL — DIRECTOR]. Agility fallbacks, no grain route, no Remnant, no Emberholt direction re-checked. The reconciliation row above is closed by this review. |
| **Director rulings reconciliation (2026-11-03)** | Applied CDR-1..3 (`Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`). Header note: no tied-prisoner props, downed space or wolf break-off exit lanes (none were authored here; leash/reset only). Gatefall gallery state "resolved (crew yielded or line cut)" → "crew defeated or line cut" (×2). C-5 removed, C-7/`TSW_THAW` approved (§6.5, §7, open question 4 resolved), C-8 ranged first-class; TST wind butts specified as a shooting range. TWN open stone and TWC banner walk (Old Torvek's local tradition) marked approved. "v1.5"/"ship" wording → Thornfell content / milestone language. Earlier rows describe past states. |
| **CDR-6 solo-completion sweep, 2026-11-14** | §6 co-op fallback (host's props) marked presentation only; no player's step waits on another player's Narrows bridge or Passwatch gate state. |
