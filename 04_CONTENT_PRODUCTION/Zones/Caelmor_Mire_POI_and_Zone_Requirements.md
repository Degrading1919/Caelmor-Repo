# Mire of Fallen Banners — POI and Zone Requirements

**Status (2026-11-09):** draft, **in review** (independent Batch 4 review 2026-11-09, §15), Batch 4 of the Mire production plan (bible §12). This is the Gameplay Designer's set of level-design requirements. It turns every place in the Mire narrative packages into requirements: subzones, routes, POI sub-spaces, traversal and water, the ground-and-water readable system, per-player state and phasing, and relative placement. It also lists what the Mire will ask of the architectural generator. Every place is **[NEW]** unless the bible marks it [CANON], and nothing here is canon until the Director promotes it (MD-16). **[PROPOSAL — DIRECTOR]** marks consequential choices. **MAP VERIFICATION REQUIRED** marks every place where geometry, distance or water matters (MD-9). **No Mire terrain exists yet.** All placement is relative. No compass direction, interregional route or travel path to another region is stated. This file documents dependencies only. It contains no schema, JSON, scene data or C#.

**Director rulings (binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. For places this means the following. Every enemy is defeated at 0 HP, so no arena needs tied-prisoner props, downed-state space or break-off exit lanes. Ranged is first-class and never required, so no arena may offer a firing spot the enemy cannot reach (the General's leash, §4 MP12). The Mire is an internal milestone of the complete game (CDR-3). Ordinary RPG systems are preferred over simulation (CDR-4): no swimming, breath meter, tide simulation or per-tile mud.

**Open Director decisions the places depend on:** MD-3 (first-light crossing), MD-4 (staged drainage, no breath meter), MD-7 (Hollowfoot as enemies; **OPEN**, both options kept) and MD-8 (the Night Count). Places that change if a ruling changes are tagged `[MD-3]`, `[MD-4]`, `[MD-7]` or `[MD-8]`. `[CAUSEWAY]` marks places tied to the MD-1 cause.

**Sources:** bible §1.1, §2.1, §2.3, §4 (MP01–MP28, route order), §6.1, §7.4–7.5, §9, §10, §11; Act I §A5, §A7, §A11, §B5, §B7, §B11; Act II §A5, §A7, §A10–A11, §B5, §B7–B8, §B11; Act III §5, §7, §8.2, §9.3, §11, §E; the place tables of the four side-quest files (`Quests/Caelmor_Mire_Side_Quests_*.md`), MME01–MME10 and MDS01–MDS10; `Zones/Caelmor_Thornfell_POI_and_Zone_Requirements.md` (format); `Zones/Caelmor_Lowmark_Terrain_Narrative_Conflict_Register.md` (terrain lessons and architecture notes); `CODE/Scripts/architectural_generator/README.md`, `FUNCTIONAL_PROGRAMS.md`, `WORLD_ARCHITECTURAL_LANGUAGES.md`, `REGIONAL_GRAMMAR.md`.

**Source state.** The bible and the three main acts were independently reviewed (2026-11-07 and 2026-11-08). The four side-quest files were committed on 2026-11-08 and their independent review fixes landed on 2026-11-09 (commit e98147e); this file was re-checked against that state (§15).

**Companions:** `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` (being written concurrently; owns encounter ids, creature values, telegraph timings and hazard tuning) and `Quests/Caelmor_Mire_Integration_Requirements.md` (runtime needs). The three Batch 4 files state the shared values in §14 (MC-1 to MC-9) in the same words.

---

## 0. Level-design constraints

### 0.1 Runtime (carried from the Lowmark and Thornfell zone files)

| Constraint | Level-design rule |
|---|---|
| Click-to-move over a host NavMesh; Shift sprint; no jump | Every required route, objective, stake, post, standard, windlass and arena safe space is NavMesh-reachable by walking, or by boat where §3 says the boat is the route. |
| Agility triggers approved, **not built** | Every agility trigger listed here has a **walkable fallback** that is the critical path until triggers exist. No required objective sits behind a trigger. |
| No multi-level traversal or off-mesh links yet | Vertical spaces need multi-level NavMesh with stairs or ramps: the Chapel (roof, bell-loft ladder, gallery, aisle walk, bays, nave floor, crypt stair), the Hushed Granary ladder, Bran's watchpost platform, stilt-house steps, the archive loft ladder. Ladders are interaction-driven moves ("climb down") until off-mesh links exist. Flag each to Systems. |
| Interaction needs reach and line of sight | Channel points used under attack (standard lift poles, chest lever, windlasses, lantern posts, the gap stone, survey stakes, sluice rods) need a standing pad of at least 2 m facing the object, on walkable ground at every water state in which the step can run. |
| **Water** | **No swimming and no drowning anywhere** (bible §11.1). Deep water is non-walkable at every state; the player stops at its edge with a bark and no damage. Shallows are walkable and slowed (standard slow). No knockback, shove or push may end in deep water: every lane next to deep water has an edge blocker or pushes toward the walkable side (MC-6). **Reedlurker reach:** wherever a snapper is placed, the water it holds is wadeable (knee-deep) within a few metres of the bank or sump lip, never deep water, so melee can always reach it (Enemies §5.3, C-5). |
| Edges | **No fall deaths.** Raised ways, stilt platforms, the watchpost, the Chapel gallery and the palisade crown each have rails, edge blockers or a gentle slope. |
| Per-player state (bible §9) | Channel states, standard states, water stages, lantern posts, epilogue props and NPC placement are client presentation keyed to the local player's state. Co-op fallback: the host's props; each partner's own flags drive barks, dialogue and epilogue (see Integration MI-CO-06 for the one shard-level rule recommended). |

### 0.2 The ground-and-water system (bible §1.1): level-design definitions

The Mire's readable system is **ground and water**. Every element is a **world marker the player looks at**, never a UI mode. Each feature below is a tagged object or volume the level must supply; §4 lists the instances.

| Feature | Tag (working) | Requirement |
|---|---|---|
| **Channel stake** | `channel_stake` | A Reedsward depth stake painted in three bands (pale, ochre, black; finish is art's call). Its water-line prop shows the crossing's state: **Running**, **Slack** or **Sour** (stake leaning or water over the black band). Inspect text is gated on `MR_CHANNELS`. Every crossing that changes walkability has one at each end where a player arrives. |
| **Crossing segment** | `crossing_seg` | A walkable segment (shallows, causeway dip, bank, ford line, under-store mud) that is walkable or non-walkable by the crossing's state. One crossing id per segment group; state comes from the crossing register (§6.2). |
| **Watch bench** | `watch_bench` | A marked bench where *keep watch* advances the per-player presentation hour (Lowmark convention). Required beside every crossing a step can pin, and at every place a step waits for dusk, night or morning. Waiting is always available. |
| **Knot clump** | `knot_clump` | A clump of reed heads with Rowan's knots (one knot, two knots, cut through). Three states. Only on Rowan's route, the practice cuts and the landing stake (MR-M3). |
| **Lantern-moss post** | `moss_post` | A post whose foot carries moss. States: dark (dry foot or untended) and lit (wet, tended). Lit by presentation hour where a line is tended (MR-M1), or by interaction (MR-M4, MBO, MNK caps, MLL). Inside the Chapel a lit post also suppresses Shades in a radius (MC-3); in MLL the same radius slows Earthen Echoes (one effect, Integration MI-LT-01). |
| **Standard** | `standard` | A banner pole and cloth with states: **laid**, **leaning**, **risen**, **lifted-unfolded**, **folded**, **removed**, plus **honoured** (re-raised still, `tended` and `restored` outcomes). A risen standard is a Wraith spawn condition (MC-4). |
| **Dark ground** | `dark_ground` | Chapel only: any walkable ground outside every lit post's radius. Shades form at the edge of the hand lantern after a delay (MC-3). Shades are a hazard with no HP. |
| **Lane** | `count_lane` | Bannerline only: a drill furrow ~3 m wide in four segments, along which Echo files advance one segment per third beat. Turf strips between lanes are safe from files (not from the General's sweep). |
| **Deep water** | `deep_water` | Non-walkable volume with an edge stop and bark. |
| **Shallows / ditch** | `wade` | Walkable, slowed. Reedlurkers may use reed lines beside them. |
| **Raised way** | `raised_way` | Plank walkway on piles. Walkable at every state. The settlement network that the architectural generator does not produce (§10, request A-3). |
| **Silt apron** | `silt_print` | Smoothed silt that shows a print decal (MHG, MMR prints). |

---

## 1. Macro layout [PROPOSAL — DIRECTOR; MAP VERIFICATION REQUIRED]

The narrative fixes these relative facts and no others (bible §4.2 route order; Act I §A5; Act II §A5; Act III §5).

- **Sorrowmere** stands on raised ways over slack water. The **Standards Causeway** leaves Sorrowmere's edge and crosses the **Field of Fallen Standards** to the Marshfall side. The **old ferry way** also links Sorrowmere and Marshfall, and runs Sour this season.
- **Marshfall** lies at the causeway's far end, where marsh meets forest. **Edris's old care station** sits where the causeway meets the Marshfall side; Marshfall is a short walk on. The **Fowling Meres** lie at Marshfall's edge, toward the forest line. The **Hushed Granary** and the **Sodden Pyres** lie on Marshfall Edge.
- **Rootrest** and the **Fenward huts** lie on firmer ground beyond Marshfall. The root-timber lot (MEP) lies past Rootrest.
- **Nine Stakes** and the **Reed Hide** lie off the causeway. The **Singing Trench**, the **Rust Hollow** and Nine Stakes sit at the Field's edge.
- **Blackwater Landing** sits below Sorrowmere at the edge of the Blackwater Channels. **Sennic's Driftwood Rise** is a short walk from the landing along the peat edge. **Stillgrave's near edge**, the **Wading Ford** and the **landward side of the Drowned Encampment** are reachable on foot along the peat edge.
- The **Chapel of the Sinking Star** is reached **only by Rowan's route** by boat, past the Drowned Encampment and along Stillgrave's far side. There is no walking route to it.
- **Mirebone Crossing** lies at an edge of the Blackwater and is on no milestone route. It is not a route anywhere (MD-9).
- **Griefwatch** sits at the foot of **Bannerline Ridge**, the Mire's only high ground. The **Bannerline road** climbs from Griefwatch's closure gate to the crown by three bends. **Bran's watchpost** stands on a shoulder above Griefwatch, off the road, with a view down onto the **great furrow** in the peat below. **Requirement:** its path leaves from Griefwatch's side of the closure gate and never passes through the gate, because MR-M5 `S02` sends the player there while the road is shut (MT-14; MAP VERIFICATION REQUIRED). The **Dry Muster** lies on the flat beside Griefwatch, short of the closure gate. The gate stands open before MR-M5 (MBO); whether the bends and crown are walkable before MR-M5 is open (Q-3).
- How Griefwatch and Rootrest connect to Sorrowmere is **not stated by any package** ("the ordinary way", Act III §5). Map Q-1 (§13).

---

## 2. Subzones (bible §4.1)

Each subzone has a **near band** and a **far band**, so early side quests can play in subzones whose main content comes later.

| Subzone | Contains | Band: near / far (MD-10) | Ambient signature | Families (Enemies file) |
|---|---|---|---|---|
| **Sorrowmere and the Raised Ways** | MP01, MP14, MP15; memorial gardens; the jetty; causeway head | Hub / hub | Plank creak, water under piles, mood banners at junctions, children's depth-band game | None (hub) |
| **The Field of Fallen Standards** | MP07, MP08, MP19, MP21, MP23, MP27 | Competent (MR-M1, MR-M2, MNK, MSG) / Competent late (MCF, MRH) | Standards at every angle, flat open bog, long banner shadows at dusk (MME09) | Banner Wraiths, Reedlurkers, Griefbit Beetles, Mud-Clad Raiders, Rootshadow Cutters, Tarnish Stalkers |
| **Marshfall Edge** | MP02, MP20, MP22, MP26; Edris's old station; Peat Row | Competent / Competent | Smoke sheds, peat walls, herons, fenny does | Griefbit Beetles, Reedlurkers; fauna |
| **The Blackwater Channels** | MP06, MP09, MP10, MP11, MP13, MP18, MP25 | Advanced (MR-M3, MR-M4) / Advanced; near edge Competent (MLL, MFH) | Black water, fog banks, reed islands, distant shouting at the Encampment | Reedlurkers, Earthen Echoes, Silt Crawlers, Bog Hounds; Chapel Shades (hazard) |
| **Rootrest and the Fenward** | MP04, MP05, MP16, MP28; root-timber lot | Competent / Competent | Roots overhead, bone chimes, herb smoke | None in content (travel fauna only) |
| **Bannerline Ridge and Griefwatch** | MP03, MP12, MP17, MP24 | Competent (MBO, MSS) / Advanced (MR-M5) | Vigil bell, iron-red soil, the palisade arc on the skyline | Earthen Echoes (files), Banner Wraiths, Hollowfoot `[MD-7]`, Bog Hounds (MBO); the General |

---

## 3. Traversal route plans

| Route | Path | First used | Character | Agility trigger → walkable fallback |
|---|---|---|---|---|
| **R1 The Raised Ways** | Sorrowmere raised way → register room → Ferrow house row → memorial gardens → Calwen's sanctuary at the edge → jetty → causeway head; a stair or ramp down to Blackwater Landing | MR-M1 | Plank walkways on piles; junction banners; moss posts every tenth pile | None required |
| **R2 The Standards Causeway** | Causeway head (S4) → C1 first crossing → C2 roadside works → C3 Mara's marker (plank off) → C4 second crossing → C5 relaid section (old line beside new for ~40 paces) → turnout platform (field centre) → C6 far end → Edris's old station | MR-M1 (walk out, cart back), MR-M2, MLD | Straight log road over the bog; ditches either side; two stake-marked dips | Causeway ditch jump at standard 3 → slope steps (MR-M2) |
| **R3 Marshfall Edge** | Causeway far end → Marshfall walkways (Hayle house, Rudd house, Peat Row, jetty) → Fowling Meres → Hushed Granary → Sodden Pyres; on to Rootrest and the Fenward on firmer ground | MR-M1 | Stilt houses, peat cuts, smoke sheds | Marshfall walkway gap → round the drying racks (~15 s); feeder-channel jump at the bend → plank at the mere end (MRS) |
| **R4 The Peat Edge** | Blackwater Landing → Sennic's rise → peat path (L7) → Stillgrave near edge; separate peat-edge legs to the Wading Ford and the Drowned Encampment's landward side | MR-M3 | Laid peat and old planks along channel edges; moss posts mostly dark this season | None |
| **R5 Rowan's Route (boat)** | Landing → C1 junction one → C2 the shoal (tow path) → C3 Drowned Encampment cut (three stretches) → C4 junction two → C5 Stillgrave open water (far side) → C6 fog bank and Chapel roof landing stage | MR-M3 `S05`; after MR-M3 the Chapel route at Slack | Fixed boat spline with authored stops (ferry convention). **The only route to the Chapel.** | None (the boat is the route) |
| **R6 The Chapel Descent** | Roof landing stage (T2) → ridge (T1) → tower hatch (T4) → bell-loft (G1) → gallery (G3) → gallery post (G6) → aisle walk (N1, stage 1) → bays and vestry (N2, stage 2) → nave floor and altar (N3, stage 3) → crypt stair | MR-M4 | Indoors and vertical; lit by posts | Gallery gap G3–G5 (step across) → back round through the loft |
| **R7 Griefwatch and the Bannerline Road** | Griefwatch main way → closure gate (W1) → Low Bend (R1) → Rag Bend (R2) → Iron Bend (R3) → palisade (C1) → crown (lanes, circle); separate shoulder path from Griefwatch's side of the gate to Bran's watchpost | MR-M5 (road); MBO, MSS (Griefwatch) | Climbing road on iron-red soil; lanes cross the road at R1 and R3 | Palisade fallen-stake scramble R1 → R3 (crosses one lane) → the road |

**Phase 1.5 check (3–4 route plans):** seven are listed. R2, R5, R6 and R7 are the four **designed** routes (set pieces); R1, R3 and R4 are connective.

---

## 4. POI requirements (MP01–MP28)

Format per POI: **function**, **placement**, **areas** (sub-space ids are the packages' own letters), **quest uses** (package / step), **state by flag** (full table §6), **required props**, **traversal and water**, **map**. Phases: **M1–M5** (milestones), **Post** (after `MR_STANDING`).

### MP01 Sorrowmere — Settlement, Sorrowmere [CANON]

| Field | Requirement |
|---|---|
| Function | The hub: register, hearings, the long table, mood banners, the causeway head, respawn. |
| Placement | Raised ways over slack water. Relative order (Act I §A5.1): raised way → register room → Ferrow house further along the same way; the causeway head at the settlement's edge facing the Field; Calwen's sanctuary at the edge where the ways give out into reed; Blackwater Landing below. |
| Areas | **S1 raised way** (MR-M1 offer; MME01 junction banners; MME03 lantern walk; MME10 jetty game); **S2 register room** (Names Below register on a reading board; index boards with three peg colours and, after MEP, an *Away, not lost* column; the **stranger's seat**, worn top, newer legs; soil bowl MME02; story shelf R2; **archive loft** above by ladder, MBA; the keepers' roll, MHG; the arrivals wall, MBA); **S3 Ferrow house** (end house on taller piles; bench outside the door; Agna's chair; hearth); **S4 causeway head** (watch bench under a moss post; depth-mark post; respawn); **S5 reed-cutter's house**; **Keel house** (MEP); **memorial gardens** (griefroot beds, Prue's work shelf, MLL; lantern on a post with `MLW_KEEPER = gardens`); **long table** T1 (trestles beside the register room, MR-M5 `S08`, MLD); **jetty** (two mooring posts, MSS; channel stake); **the pool** beside the raised way with its own stake (MDS01 sunken ring at Slack). |
| Quest uses | MR-M1 `S00`, `S01`, `S04` end, `S04b`, `S05`; MR-M2 `S04b`; MR-M3 `S00`; MR-M4 `S08` (payment); MR-M5 `S00` trigger, `S08`; MSS `S00`, `S01`, `S06`; MBA all but `S04`; MEP `S00`, `S01`, `S06`; MLL `S00`; MLD `S00`–`S08`; MHG (keepers' roll); MME01, 02, 03, 04, 06, 08, 10; MDS01. |
| State by flag | Register page by `MR_NAME_RECORD`; index-board strips (MNS hook strip, MSS strip, *Away, not lost* column after MEP); arrivals wall strip by `MR_ARRIVALS`; seat-underside rubbing by `MSS_RUBBING = taken`; Warden leaves on the reading stand with `MR_WARDEN_RECORD = sorrowmere` (Post: reed slip *Closed* / *Kept*); keepers' roll note with `MHG_KEY = register`; Lenna's map with `MMR_MAP`; mood banners pinned ochre by MR-M1 and MR-M5 then released; the roll bound into the register (Post). |
| Required props | Register (paged), index boards, stranger's seat, soil bowl, watch benches, moss posts, junction banners with three states, channel stakes at the jetty and pool. |
| Traversal and water | All raised ways walkable at every state. The pool and the slack water under the piles are deep or non-walkable except the pool's edge inspect. |
| Map | The causeway head must be at the settlement's edge facing the Field. Blackwater Landing must be reachable from Sorrowmere on foot ("below"). MAP VERIFICATION REQUIRED. |

### MP02 Marshfall — Settlement, Marshfall Edge [CANON]

| Field | Requirement |
|---|---|
| Function | The far end of the causeway; household books; peat and smoke; the cloth stall; walkway repair. |
| Placement | A short walk on from Edris's old station at the causeway's Marshfall end; at the marsh/forest edge. The Fowling Meres at its edge. |
| Areas | **M2 Hayle house** (peat-cutter's stilt house, smoke shed under; the Hayle book; the short unused spade); **Rudd house** (the peg and the lighter patch; household book in a tin, MBA); **jetty** (Gethin's stall and ledger tin; eel-smoking brazier used as the MCF burn site); **Peat Row** (P1–P4: rota board, five houses, the sunk section, the root run with the buried Memorywarden marker, MWS); **smoke sheds** (MFT eel source; MRS down basket); **peat yards**. |
| Quest uses | MR-M1 `S03` (Hayle book; optional hunting line); MBA `S04`; MCF `S00`–`S02`, `S07` burn; MWS all; MRS F5; MFT (eels); Post epilogue (§E.6: Dunstan, Hewin). |
| State by flag | Hayle book page by `MR_NAME_RECORD`; Peat Row walkway straight or dog-leg by `MWS_MARKER`; stall removed after MCF (presentation); Hewin's position by `MBL_ASKER`. |
| Required props | Household books (read in place), Gethin's ledger, the brazier, pile and fascine stacks, the marker under roots, channel stake for the row's ditch. |
| Traversal and water | Walkways walkable at every state; Peat Row ditch reach (Slack) or wade (Running) by state (MWS). Agility: walkway gap → drying racks. |
| Map | Must be reachable from the causeway's far end without crossing open water. MAP VERIFICATION REQUIRED. |

### MP03 Griefwatch — Settlement, Bannerline [CANON]

| Field | Requirement |
|---|---|
| Function | Watch settlement at the ridge foot; the closure; the vigil hall; MR-M5 base and respawn. |
| Placement | At the foot of Bannerline Ridge. Dry Muster on the flat beside it. The closure gate at the foot of the Bannerline road. The shoulder path to Bran's watchpost leaves from **Griefwatch's side of the closure gate** (MT-14). |
| Areas | **W1 closure gate** (timber gate between two old palisade stakes, iron-red soil at their foot, MDS06; slate *Road shut. Ask Ide.*; wardens' brazier); **W2 vigil hall** (stone footings; bell rope through the roof to the vigil bell; long table; **vigil book** on a stand; **roster board**; cook-hearth with great pot; hearing table with its own stranger's seat, spear-shaft splint, MSS; the spoon nail; Griefwatch's chest with the transferred list, MDS04); **W3 the fold** (Lysa's yard; Jory Wick) `[MD-7]`-safe; **W4 bell households' row** (door-lintel chalk marks, MBO); **W5 Copse house**; **W6 Tibb's bench** at the bell ladder foot; **Wren and Lister houses** (household books, MSS). |
| Quest uses | MR-M2 `restored` (banner hung); MR-M5 `S00`, `S01`, `S01b`, `S03` start, death respawn; MSS `S02`; MBS (Eskil); MBO all; MDS04, MDS06; Post §E.2. |
| State by flag | Banner That Sank Twice over the hall door with `MR_BANNERS = restored`; gate shut from MR-M5 `S00` to `S03` (per player), then open; Post: gate tied back (`quieted`) or warden with a count slate (`tended`); vigil book *Gap kept by* column (`tended`); roster board strips by `MBO_RULE`; Thornfell warden pair at the brazier with `TH_STANDING`. |
| Required props | Vigil bell and rope (night-turn interaction), vigil book (paged, show-match), roster board, door chalk props, gate with shut/open/tied states, slate. |
| Traversal and water | Dry ground. No crossing. |
| Map | Bran's watchpost path must not pass the closure gate (MR-M5 `S02` runs while the road is shut). MAP VERIFICATION REQUIRED. |

### MP04 Rootrest — Micro-settlement, Rootrest [CANON]

| Field | Requirement |
|---|---|
| Function | Root-sheltered homes, herbalists, bonecarvers; hearings; peat; care book. |
| Placement | Firmer ground beyond Marshfall. The Last Root (MP16), the Unfired Kiln (MP28) and the Fenward huts (MP05) are part of or beside it. |
| Areas | **Rootrest hall** half under the roots of an old black-rooted tree (root-slab hearing table; the oldest stranger's seat on rotted legs; the hearing form board; Elric Daw's bench); **root-wood pile** (C2, Woodcutting); **Teal house** (debt tally under a lantern hook; half-cut stack); **herbalists' room** (care-book, MDS09; balm pots, MHG G5); **root arch** with bone chimes, **Hessel's yard**, **plank way** with a stake at its low point, **cutting bank**, **Hessel's table** (MRW); bonecarver's bench (antler with `MRH_ANTLER = rootrest`). |
| Quest uses | MSS `S03`–`S05`; MRW all; MHG (testimony); MRH `S06`; MDS08, MDS09; MEP route to the lot. |
| State by flag | Seat legs new after MSS (`MSS_SEAT_LEGS`); rubbing taken or left; rick and dry-shed roof after MRW; antler piece on the bonecarver's bench or the Last Root rail. |
| Required props | Seat with upright and upturned states; form board; tally post; rick base with course sequence; bone chimes (one scripted ring). |
| Traversal and water | Plank way over wet ground with a stake at its low point (MRW: walkable at every state; the stake is presentation). |
| Map | Root-sheltered forms are an architecture gap (§10, A-4). MAP VERIFICATION REQUIRED. |

### MP05 Fenward Huts — Micro-settlement, Rootrest [CANON anchor location]

| Field | Requirement |
|---|---|
| Function | Lysa's care huts; settled Hollowfoot as non-combatants; the care-cooking station. |
| Placement | By Rootrest on firmer ground beyond Marshfall. |
| Areas | **F1 Lysa's bench** (MR-M1); **F2 the settled man** (Jory Wick, sorting reeds) `[MD-7]` non-combatant, never targetable; **W1 hearth hut** (long table, iron pot, high shelves above a painted flood line, bogsedge fern on the sill); **W2 four huts**; **W3 smoke-hut** with a reed-shuttered vent; **W4 root beds**; **W5 the step** with a small three-band stake. |
| Quest uses | MR-M1 `S03` (optional; `MNS_FENWARD_VISITED`); MFT all; Post §E.7 (two more drifters, non-combatant). |
| State by flag | Flood variant (dry / water at the step) by MFT step; labelled crock shelf (`MFT_CROCKS`); public Cooking station after MFT; fern wilts and resets. |
| Required props | Two-state flood environment variant; smoke-colour loop on the vent; crock shelf slots. |
| Traversal and water | Dry by default; at the MFT flood stage water stands at the step (walkable slowed at the step, huts reachable by planks). |
| Map | MAP VERIFICATION REQUIRED. |

### MP06 Blackwater Landing — Micro-settlement, Blackwater [CANON anchor location; NEW name]

| Field | Requirement |
|---|---|
| Function | Rowan's docks; the Chapel route; ferry households; repair bench. |
| Placement | Below Sorrowmere at the Blackwater's edge. Sennic's rise a short walk along the peat edge; the peat path (L7) leads on toward Stillgrave's near edge. |
| Areas | **L1 reed docks**; **L2 boat shed and bench** (Rowan's boat on trestles; the war-years ferry list in a reed tube, MFW; the ferry passage book on a lectern, MEP); **L3 Rowan's fire and the landing stake** with a knot clump; **L4 reed beds** (six cutting spots, MR-M3 hull); **L5 practice cuts** (two short channels, each with a stake and a knot clump); **L6 ferry households' row** (three stilt houses; the Tolley house and work bench, MFH; the Lusk house with the naming board, MFW); **L7 peat path**; **H1–H4** (MFH: stranded punt, landing bank root-knees, smoke racks, home channel with a stake at each end and a tow path). |
| Quest uses | MR-M3 `S01`–`S05`; MR-M4 `S08`; MEP `S02`; MFW `S00`, Lusk house; MFH all; MR-M5 Post (Rowan lines); kept-trust lantern (MR-M5 C5). |
| State by flag | Rowan's boat on trestles before MR-M3 `S02` complete, then moored; repair bench public after MFH; Rowan's mooring presence by Chapel route schedule (MC-1). |
| Required props | Boat ride spline origin; harness prop; stakes; knot clumps (three states, inspect gated by `MRC_KNOTS_READ`); keep-watch bench by Rowan's fire. |
| Traversal and water | Docks walkable at every state. H1 mud walkable at Slack and Sour; H2 bank walkable at Slack only; H4 crossing by punt only (MFH rowing ride). |
| Map | "Below Sorrowmere" is a relative height and distance; the connection must be walkable (stair or ramp). MAP VERIFICATION REQUIRED. |

### MP07 The Field of Fallen Standards — Unique landmark, Field [CANON]

| Field | Requirement |
|---|---|
| Function | The flattened banner bog; source of the risen standards; the Risen Colour's ground. |
| Placement | Between Sorrowmere and Marshfall, crossed by the causeway. Nine Stakes, the Reed Hide, the Singing Trench and the Rust Hollow at its edges. |
| Areas | **N1 near causeway** (three standards in view of the causeway head, one in each state: laid, leaning, risen); open bog with ordinary standards in mixed states; **N5 black water** beside the turnout platform (non-walkable) where the Banner That Sank Twice rises at dusk; field edges for MME05 (mudstone faces) and MME09 (banner shadows). |
| Quest uses | MR-M2 `S01`, `S05`; MME05, MME09; Post §E.5. |
| State by flag | Field away from the road keeps its ordinary standards in mixed states in every outcome. With `MR_BANNERS = restored`, Griefwatch's banner visible far off on clear days (MAP VERIFICATION REQUIRED; else omit, MT-13). |
| Required props | Standards with all states; MME09 shadow decals at dusk. |
| Traversal and water | Open bog is non-walkable except where a package authors ground (the causeway, the turnout, plank spurs). The player meets the Field from the causeway. |
| Map | MAP VERIFICATION REQUIRED for extent and sightlines (§8). |

### MP08 The Standards Causeway — Ruin/war site, Field [NEW] `[CAUSEWAY]`

| Field | Requirement |
|---|---|
| Function | The relaid wartime log road; the Act I work route; the festival walk. **Edris's old care station** is folded in here as a sub-site (Act I open decision A14.7: decided as an area of MP08, not a POI). |
| Placement | From Sorrowmere's edge straight across the Field to the Marshfall side. Order (Act I §A5.2, §B5.2): causeway head → **C1 first crossing** (dip ~20 paces with stake) → **C2 roadside works** (crew, three stood standards, the crew's standard nearest the road) → **C3 Mara's marker** (low peat ridge reached by a plank) → standards 1–3 along the roadside (standard 3 at the embankment foot on the ditch side) → **N4 embankment foot and ditch** (the officers' chest) → **N5 turnout platform** (~20 paces square, at the field's centre) → **C4 second crossing** (shorter dip with stake) → **C5 relaid section** (old wartime line beside the new for ~40 paces; old posts dark) → **C6 far end** (raised bank, last stake) → **M1 Edris's old care station** (raised platform of old timbers, half roof, tin box behind a loose board, pallet frames). |
| Quest uses | MR-M1 `S02`, `S02b`, `S03` (marker, station), `S04` (cart walk back by lit posts; stakes turn Sour behind the cart; the dark line at C5); MR-M2 `S01`–`S05`; MLD `S04`–`S06` (children's walk to the turnout and back; stakes Slack end to end); MBS (standard 2's pale hole); MCF trail start; MNK hook. |
| State by flag | Roadside standards present (default, `MR_CAUSEWAY` unset) → removed with pale holes (`reset`); per-standard states during MR-M2; pinned logs (`MBR_PINS = self` marks one post, MLD); crew presence and barks; MLD festival props. |
| Required props | Stakes at C1, C4, C6 (and a crew stake per section for MLD's sequence); moss posts along the line (lit at dusk and night on the new line; dark on the old line); standards; loose-log segments (slowed until pinned); pin pile and splitting block; chest with lever pad; escort cart path; watch benches at C1 and the turnout. |
| Traversal and water | Logs walkable at every state except the dips, which are crossing segments (§6.2). Ditch shallows either side walkable and slowed; Wraith shoves into the ditch never reach deep water. Agility: ditch jump at standard 3 → slope steps. |
| Map | **Length and crossing count are load-bearing** (MT-01, MT-02, MT-03). MAP VERIFICATION REQUIRED. |

### MP09 The Drowned Encampment — Ruin/war site, Blackwater [CANON]

| Field | Requirement |
|---|---|
| Function | A sunk war camp: Echoes on the banks (MR-M3); the scholar's survey and the ration board (MMR). |
| Placement | On Rowan's route between junction one/the shoal and junction two. Its **landward side** is reachable on foot from the peat edge (MMR). |
| Areas | **C3 the cut** (narrow channel between two banks of wagon wheels, tent poles, rusted weapons, a field kitchen's stove on its side; faint repeating shouting) used in three stretches by MR-M3; landward: **A landward edge** (Lenna's tent, fenny does), **B string field** (grid of reed strings over printed mud), **C the loop** (prints between a sunk cookhouse and a water hole), **D the cookhouse** (ration board under silt). |
| Quest uses | MR-M3 `S05` (MRC-E2, three stretches); MMR all. |
| State by flag | Survey stakes present until MMR pulls them (Echo condition); `MMR_MAP`. |
| Required props | Bank spawn points per stretch; ride-halt volume; survey stakes; print decals (fill sequence); ration board. |
| Traversal and water | Cut by boat only. Landward string field walkable mud. |
| Map | The cut and the landward side must be the same camp but must not offer a walking route onward to the Chapel (MT-08). MAP VERIFICATION REQUIRED. |

### MP10 Mirebone Crossing — Unique landmark, Blackwater edge [CANON; convergence role provisional]

| Field | Requirement |
|---|---|
| Function | A bone-littered ford that moves; discovery only (MDS10). |
| Placement | At an edge of the Blackwater, on no milestone route. |
| Areas | Near bank; a fallen Marshwarden stake with a note; the ford line with bones. |
| Quest uses | MDS10 only. |
| State by flag | Ford line and bone line swap between two or more authored variants on each presentation-hour turn (no simulation). |
| Required props | Fallen stake; two ford-line variants. |
| Traversal and water | Wadeable a few steps from the near bank; beyond that, non-walkable silt. **No far-side destination is built or described.** It is not a route (MD-9, FT-03). |
| Map | MAP VERIFICATION REQUIRED. Nothing may lead from it to another region. |

### MP11 Stillgrave Hollow — Unique landmark, Blackwater [CANON]

| Field | Requirement |
|---|---|
| Function | Too-clear water; night moss; a family's unfinished ring; the reflection. |
| Placement | Near edge reachable on foot from the landing by the peat path. Rowan's route passes along its **far side** on open water. |
| Areas | **S1 stilt-stumps** with moss on their damp faces (five night clusters, MR-M3); **S2 shallows** (Reedlurker ground); **S3 the surface**; **MLL C the Haddow ring** (a shelf of firm bank above the water; six reed stakes in a half-circle, space for six more); **MLL D wash stones**; **C5 open water** on the far side (MR-M3 soundless bell). |
| Quest uses | MR-M3 `S02` (moss; MRC-E1), `S05` (bell); MLL `S01`, `S03`–`S08`; MDS02. |
| State by flag | Ring lanterns lit after MLL; reflection straight over the ring after MLL (`MR_LANTERN_LINE`); night-only gather nodes. |
| Required props | Moss gather nodes (night), lantern stakes (lit / out), reflection swap, reed-flatten rings on the far reed edge. |
| Traversal and water | Shallows walkable and slowed; the Hollow's body non-walkable. |
| Map | The near edge must be separable from the far side (the boat must not pass within walking reach of the near edge, or the bell reads as on foot). MAP VERIFICATION REQUIRED (MT-08). |

### MP12 Bannerline Ridge — Ruin/war site, Bannerline [CANON; circle NEW]

| Field | Requirement |
|---|---|
| Function | The MR-M5 climb, boss arena and rite; post-story vigil and the Night Count. |
| Placement | Above Griefwatch; road from the closure gate by three bends to the crown. |
| Areas | **R1 Low Bend** (two lanes cross the road); **R2 Rag Bend** (road along the lip of a rag-filled hollow; Hollowfoot drifters below the road, `[MD-7]`, optional and avoidable by keeping to the road; **MD-7 swap:** the same hollow holds three seated, non-hostile drifters, so it needs a ~3 s sit-interact spot beside them and a walkable line from the hollow back to the road for their walk down to the wardens' brazier); **R3 Iron Bend** (red iron soil, first palisade stakes, three lanes cross; checkpoint; MDS06 post-story); **C1 palisade arc** (old stakes, standards lashed, three iron-shod stakes at the lane heads); **C2 muster post** (iron-shod post with a worn crossbar); **C3 three lanes** (Stake, Post, Ring; ~3 m wide, ~25 m long, four segments each; turf strips ~4 m between); **C4 the circle** (twelve waist-high stones S1–S12, ~16 m across, one gap with a flat footing stone facing the Post Lane; five stones inspectable by place name); **C5 below the ring** (road head; view down over the Mire). |
| Quest uses | MR-M5 `S03`–`S07`; MDS06 (post); Post §E.1 vigil; Night Count `[MD-8]`. |
| State by flag | Standards risen (before `S04`) → three retired → laid in the earth (`quieted`) or re-raised honoured (`tended`); gap stone new (`quieted`) or stepped with a keeper (`tended`); muster post with keeper's rope (`tended`); Corra's banner at S1 during the rite with `MR_BANNERS = restored`; arrivals and placement per Act III §8.2. |
| Required props | Lane ripple decals; standards with lean-and-lie animation toward a precomputed nearest stone; stone marks for twelve attendees plus shoulder marks; lanterns on palisade stakes and at the road stone; gap stone with three states. |
| Traversal and water | Dry. **Boss leash:** the arena is the crown between the palisade and the ring's stones; the ring is outside the leash (no firing spot the General cannot reach). The slope beyond the ring falls gently to the road head (no fall). Agility: fallen-stake scramble R1 → R3 → the road. |
| Map | Arena dimensions and the lane/ring relation are load-bearing (MT-10). MAP VERIFICATION REQUIRED. |

### MP13 The Chapel of the Sinking Star — Cave/dungeon, Blackwater [CANON] `[MD-4]`

| Field | Requirement |
|---|---|
| Function | The R08 dungeon: roof lantern line, staged drainage, vestry, crypt. One site, three names (Chapel of the Sinking Star / Sunken Chapel / Sunken Church); the name's origin is never explained, so **no star motif anywhere**. |
| Placement | In the Blackwater, reached only by Rowan's route; the roof stands out of a fog bank just above the water. The great window's outer face is against the bank's peat (which is why the glass "lit by nothing" has nothing behind it). |
| Areas | **Roof:** T1 ridge line (six lantern posts in covered housings, half dark), T2 lower slope and landing stage (two lowest posts in knee-deep water; MCS-E1), T3 Mabyn's loft (peat stove, moss jars, the **Tenders' chest**; respawn before `S02`), T4 bell-tower hatch (Mabyn's pole lantern = top post). **Interior:** G1 bell-loft (empty bell frame; two posts; first Shade), G2 bell-loft window and **Windlass A** (view to the **buttress stake** and culvert A's outfall stain), G3 gallery on corbels round three sides (agility gap G3–G5), G4 far window and **Windlass B**, G5 corner window and **Windlass C**, G6 gallery post (respawn after `S02`; dusk wait). **Nave by stage:** N1 upper aisle walk (stage 1; P1–P4), N2 lower bays with pools and the vestry door (stage 2; P5–P9), N3 nave floor, altar and the great window (stage 3; P10–P13). **V1–V2 vestry** (field post; dispatch case high on a hook). **K1–K3 crypt** (slab with iron ring in the altar step; dry stair; lead-lined box on a shelf). |
| Quest uses | MR-M3 `S06` (arrival); MR-M4 `S00`–`S07`; MLW `S00`+ (roof, loft); Post (lit, drained, revisitable; crypt box with `altar`). |
| State by flag | `MCS_STAGE` 0–3 (three water levels plus flooded start); posts dark / lit / guttering (`S06`); outer line lit (`MCS_OUTER_LIT`); custody props: box under the altar with or without leaves, Tenders' chest pegged; Post: stage 3 kept and main paths lit, Shades still in dark corners. |
| Required props | Three windlasses with stains readable from their windows; buttress stake visible from G2; 13+ interior posts and 2 loft posts; great-window emissive state; slab, box and prise interaction. |
| Traversal and water | **No swimming, no breath meter, no air bar** `[MD-4]`. Deep water non-walkable at every stage; each stage exposes new walkable ground. Multi-level NavMesh: roof → ladder → loft → gallery → stair → aisle → bays → floor → crypt. Gallery gap: step across → back round through the loft. |
| Map | Interior is a self-contained interior zone. **Post spacing must keep every required path inside lit radii once lit** (MT-07). Architecture gap A-1 (§10). MAP VERIFICATION REQUIRED for its setting. |

### MP14 Calwen's Reed Sanctuary — Shrine, Sorrowmere edge [CANON anchor location]

| Field | Requirement |
|---|---|
| Function | Where banners are washed, folded, stored unsorted or retired. |
| Placement | At Sorrowmere's edge where the raised ways give out into reed beds. |
| Areas | **R1 washing frames** (dye-meeting VFX, MBS); **R2 fold table** with Calwen's fold board; **R3 retirement pool** (square, edged in old timbers; folded standards in rows under clear water; moss posts at its corners); **R4 unsorted chest**; **A2 store book** (MBS). |
| Quest uses | MR-M2 `S00`, `S01`, `S05` dusk wait, `S06`; MBS `S00`+; MCF `S07` return; MWS (`MWS_MARKER = lifted` marker in the chest). |
| State by flag | New row in the pool with `MR_BANNERS = retired`; shard in the chest after MR-M2; recovered cloth with `MR_CLOTH = returned`; MBS banner retired or kept. |
| Required props | Fold sequence handles; pool with row props; chest inspect. |
| Traversal and water | Pool non-walkable (inspect from the edge). |
| Map | MAP VERIFICATION REQUIRED. |

### MP15 The Turning Stone — Shrine, Sorrowmere [CANON]

| Field | Requirement |
|---|---|
| Function | A stone that turns a finger's width under a mourner's hand; one stone of an anchor circle. |
| Placement | In Sorrowmere beside the pool; at Slack a ring of sunken stones shows in the pool's silt with the Turning Stone at one point. |
| Areas | The stone (polished by hands); the pool edge (inspect); the pool stake. |
| Quest uses | MME06 (rite on grey-banner mornings); MDS01 (reading at Slack). |
| State by flag | `MME06_TURNED` (turns for the player once); pool water-line variant shows the ring at Slack. |
| Required props | Stone with a small turn animation; pool water variants by state. |
| Traversal and water | Pool non-walkable. |
| Map | **No content links this ring and the Bannerline circle in words**; do not make them visually echo each other by layout (bible §7.5 list). MAP VERIFICATION REQUIRED. |

### MP16 The Last Root of Sorrow — Shrine, Rootrest [CANON myth]

| Field | Requirement |
|---|---|
| Function | A black-rooted tree with white flowers; mourners hold griefroot. |
| Placement | In Rootrest; its roots surface across Rootrest's paths. |
| Areas | The tree and its hand-worn rail; root runs across paths. |
| Quest uses | MDS08; MRH `rootrest` antler piece on the rail. |
| State by flag | Antler piece by `MRH_ANTLER`. |
| Required props | Rail; root inspects; griefroot hold interaction (handed back). |
| Traversal and water | Dry. |
| Map | MAP VERIFICATION REQUIRED. |

### MP17 Bran's Broken Watchpost — Ruin/war site, Bannerline [CANON anchor location]

| Field | Requirement |
|---|---|
| Function | Where the count is taught; where the furrow is seen. |
| Placement | On a lower shoulder of the ridge above Griefwatch, **off the road**, reached by a path from Griefwatch's side of the closure gate that never passes through the gate (MT-14). |
| Areas | **B1 watchpost** (broken timber tower, half its platform gone, lean-to; offerings stone); **B2 practice lane** (old drill furrow downhill; weak Echo file MBL-E1); **B3 the view** (platform edge over the great furrow, MDS07; no path down). |
| Quest uses | MR-M5 `S02` (count, furrow inspect, wait for dusk); MDS07 (after MR-M2, when Bran is there); Post §E.3. |
| State by flag | Bran present except while MR-M5 is Active; new offering after MR-M5 (`quieted`). |
| Required props | Multi-level platform with rail; practice lane decals; furrow visible but unreachable. |
| Traversal and water | Dry. The furrow must not be reachable on foot from here. |
| Map | Sightline from the platform edge to the furrow is required (MT-15). MAP VERIFICATION REQUIRED. |

### MP18 Sennic's Driftwood Rise — Unique landmark, Blackwater edge [CANON anchor location]

| Field | Requirement |
|---|---|
| Function | Sennic's stories (where, never why); root-knees for the thwart. |
| Placement | A short walk from the landing along the peat edge. |
| Areas | **D1 Sennic's fire** (lean of driftwood, pot, two stools, keep-watch); **D2 driftwood piles** (three marked root-knees, Woodcutting); **D3 the view** (fog bank over the Blackwater; the Chapel is never visible from here). |
| Quest uses | MR-M3 `S02` (three sittings; thwart). |
| State by flag | Root-knees cut (per player). |
| Required props | Woodcutting nodes on reclaimed wood. |
| Traversal and water | Dry rise above the peat edge. |
| Map | **The Chapel must not be visible from D3** (MT-09). MAP VERIFICATION REQUIRED. |

### MP19 The Singing Trench — Ruin/war site, Field edge [CANON myth]

| Field | Requirement |
|---|---|
| Function | A drowned trench that hums in storms; a vent puzzle and a revetment prop. |
| Placement | Field edge. |
| Areas | **A trench mouth** (duckboard way half under water); **B bays 1–3** separated by traverses, each with a vent shaft to the surface (open / closed), bay 2's bulging revetment; **C sumps** at bays 1 and 3 (Reedlurkers); **D timber pile** at the far end. |
| Quest uses | MSG all. |
| State by flag | Revetment propped after MSG; vents by state; pinned storm. |
| Required props | Three two-state vent covers; per-bay audio emitters; storm and shaft-whistle ambience under the pinned storm (no timed gust cycle; removed in the 2026-11-09 review). |
| Traversal and water | Duckboards walkable; sumps non-walkable. |
| Map | MAP VERIFICATION REQUIRED. |

### MP20 The Sodden Pyres — Ruin/war site, Marshfall Edge [CANON feature]

| Field | Requirement |
|---|---|
| Function | Burned trunks over warm peat; ironbloom lines. |
| Placement | Marshfall Edge. |
| Areas | Trunks; warm peat (kneel interaction); ironbloom lines between trunks; steam on cold mornings. |
| Quest uses | MDS03. |
| State by flag | None. |
| Required props | Steam VFX by presentation hour; fungus line decals (same as MRH ironbloom). |
| Traversal and water | Wet peat walkable. |
| Map | MAP VERIFICATION REQUIRED. |

### MP21 Nine Stakes — Bandit site, Field edge [NEW, Part 3]

| Field | Requirement |
|---|---|
| Function | A marked crossing with nine bog-oak sockets; raiders who prey on travellers crossing Sour. |
| Placement | Field edge off the causeway. |
| Areas | **N1 Halsey's post** (shelter on a dry hump, brazier, ferry book, broken cart below); **N2 the rise** (knoll with a view across the crossing; range inspect of stakes); **N3 the crossing** (broad shallow, a long stone's throw across, nine sockets in a line, nine stakes wrongly set; mud mounds that are raiders); **N4 reed island** (raiders' blind; Mud-Boss); **N5 side channel** with a **tenth socket** downstream, off the line. |
| Quest uses | MNK all. |
| State by flag | Stakes re-set and the ninth socket marked (`MNK_NINTH`); moss caps lit in sequence at dusk after MNK. |
| Required props | Sockets and stakes with id and facing; nine moss caps; breathing mud mounds. |
| Traversal and water | Knee-deep at Slack, waist-deep at Running (slowed), non-walkable at Sour except on the island; island reachable at Slack or Running. **Mud-Boss leash:** the island is his leash volume (~5 s with no player on it resets him), so the banks are not a firing position; the island must be large enough to fight on (Enemies §7.4). |
| Map | Depth by state and the island's reachability are load-bearing (MT-11). MAP VERIFICATION REQUIRED. |

### MP22 The Hushed Granary — Unique landmark, Marshfall Edge [NEW, Part 3]

| Field | Requirement |
|---|---|
| Function | A raised emergency store; key custody. |
| Placement | Marshfall Edge; Wystan's hut near it. |
| Areas | **G1 granary** on tall stilts, ladder to a locked door, silt apron at the ladder foot, small stake, flood hatch in the floor, tally board inside (read through a gap) and a copy by the ladder; **G2 under the store** (knee-deep at Running, mud at Slack; hatch pin and rope); **G3 weighing beam** inside; **G6 Wystan's hut**. |
| Quest uses | MHG all. |
| State by flag | Key custody props by `MHG_KEY`; moving lantern inside at night (event). |
| Required props | Print decal; hatch; beam station. |
| Traversal and water | Under-store walkable at Slack (MC-1 pin). Ladder is an interaction-driven climb. |
| Map | MAP VERIFICATION REQUIRED. |

### MP23 The Reed Hide — Camp, Field [NEW on CANON group]

| Field | Requirement |
|---|---|
| Function | Rootshadow cutters' camp in a drowned trench; the cloth stack. |
| Placement | Off the causeway in reed; reached by a tracking trail and a plank way under water except at Slack (quest-pinned). |
| Areas | **B trail** (stems cut at shoulder height, threads on reed heads, boot-prints onto the plank way); **C1 hide mouth** (lookout platform with a walkable stair or ramp on the NavMesh, MCF-E1, MAP VERIFICATION REQUIRED; reed screen); **C2 stripping frames** (three standards lashed upright and stripped; poison pots; frame-cut hazard); **C3 the stack** (bales under thatch; reeds flat in a ring). |
| Quest uses | MCF `S02`–`S06`. |
| State by flag | Camp cleared and stack gone after MCF (per player). |
| Required props | Tracking sign volumes; carry-state bales; frames. |
| Traversal and water | Plank way walkable at Slack only (pinned for MCF). |
| Map | Must not be visible from the causeway's road (it is found by tracking). MAP VERIFICATION REQUIRED. |

### MP24 The Dry Muster — Ruin/war site, Bannerline [NEW, Part 3]

| Field | Requirement |
|---|---|
| Function | An old drill ground with a gap in the lines; the bell-keeper's round. |
| Placement | On the flat beside Griefwatch, short of the closure gate. |
| Areas | **D1** long straight furrows with a **gap** where several lines stop and start; moss posts at the round's corners (dipper wets each to light); round-post with a hand bell. |
| Quest uses | MBO `S05` round (MBO-E1 Bog Hounds); MDS04 surface. |
| State by flag | Posts lit during the round. |
| Required props | Two-state posts; furrow decals. |
| Traversal and water | Dry. |
| Map | Its furrows must read as drill lines distinct from Bannerline's three lanes (MBO distinctness). MAP VERIFICATION REQUIRED. |

### MP25 The Wading Ford — Unique landmark, Blackwater [NEW place on CANON myth]

| Field | Requirement |
|---|---|
| Function | Where a figure stands knee-deep at dusk calling names. |
| Placement | In the Blackwater, reached on foot along the peat edge from the landing. |
| Areas | **C** wide shallow ford with a stake (Slack at dusk, pinned); reed banks; heron roost; flat place for a hide. |
| Quest uses | MFW `S02`+ (dusk hide). |
| State by flag | Dusk impression figure per player while the quest step runs. |
| Required props | Hunting hide with a "stay still" state; figure spawn point mid-ford. |
| Traversal and water | Ford walkable at Slack; not used as a route. |
| Map | Must not be on Rowan's route (the boat does not cross at night and MFW is on foot, MD-3). MAP VERIFICATION REQUIRED. |

### MP26 The Fowling Meres — Hunting ground, Marshfall Edge [NEW]

| Field | Requirement |
|---|---|
| Function | Fowling, reed shafts, the dusk flight; public fowling station after MRS. |
| Placement | On Marshfall Edge between Marshfall's stilt houses and the forest line. |
| Areas | **F1 / M3 Hob's hide** (reed wall with a slot, bench, net, rolling board, feather and down baskets, smoke-pot, watch bench); **F2 the mere** (depth stake in the water, reed floats on tethers, herons); **F3 feeder channel** with a stake at its mouth and three reed stands (still, bend, throat; the throat is under water at Running); **F4 retrieve shallows** (Reedlurker). |
| Quest uses | MR-M1 `S03` (optional fowl); MRS all; MFT optional fowl. |
| State by flag | Public station after MRS (`MRS_HOB_BENCH`). |
| Required props | Bobbing marks; dusk flight spawn waves; heron on the stake (untargetable). |
| Traversal and water | Feeder shallows walkable at Slack only (MC-1). Agility: channel jump at the bend → plank at the mere end. |
| Map | MAP VERIFICATION REQUIRED. |

### MP27 The Rust Hollow — Hunting ground/danger, Field edge [NEW]

| Field | Requirement |
|---|---|
| Function | Ironbloom ground; the Rust Hart's range. |
| Placement | Field edge. |
| Areas | **H1 Annot's blind** (turf blind on a dry lip above the Hollow); **H2–H5 four stop sites** (red patches with sign; the Hart's zigzag prints between them; fog drifts); **H6 the Hollow's heart** (arena: a wide bowl of red soil with five ironbloom patches of different thickness, old iron half in the peat, stumps for cover). |
| Quest uses | MRH all. |
| State by flag | Patches thin as licked (per fight); antlers taken. |
| Required props | Tagged patch volumes with two decal states; stump line with charge-stagger collision. |
| Traversal and water | Peat paths; arena dry. Agility: vault a stump line → round it. |
| Map | MAP VERIFICATION REQUIRED. |

### MP28 The Unfired Kiln — Ruin/war site, Rootrest [NEW, Part 3]

| Field | Requirement |
|---|---|
| Function | A children's rain shelter; promise marks pressed in clay. |
| Placement | Rootrest. |
| Areas | Low unfired clay kiln; crouch-entry volume; inner wall with tally rows (partly broken; never countable). |
| Quest uses | MDS05. |
| State by flag | None. |
| Required props | Crouch volume; inner-wall inspect lit by lantern. |
| Traversal and water | Dry. |
| Map | MAP VERIFICATION REQUIRED. |

---

## 5. New places invented by the packages [NEW] (not counted as POIs)

| Place | Parent / subzone | Relative placement | Traversal and water | State | Used by | Source |
|---|---|---|---|---|---|---|
| **Edris's old care station** (M1) | MP08 (folded in, §4) | Causeway's Marshfall end | Raised platform; tin box behind a board | Beetles cleared; station shut after MR-M1 | MR-M1 `S02b`–`S04` | Act I §A5.3 |
| **Rowan's route junctions C1, C2 shoal, C4, C5, C6** | Blackwater | Fixed order on R5 | Boat only; the shoal tow path walkable during the haul | Knot clumps; pinned grey `[MD-3]` | MR-M3; Chapel route | Act II §A5.5 |
| **The practice cuts** (L5) | MP06 | Two short channels off the landing | Boat only | Daylight practice | MR-M3 `S03` | Act II §A5.2 |
| **The peat path** (L7) | Blackwater | Landing → Stillgrave near edge | Walkable at any hour | Moss posts mostly dark | MR-M3, MLL, MDS02 | Act II §A5.2 |
| **The Haddow ring** | MP11 | Firm bank shelf above Stillgrave's water | Walkable | Lit after MLL | MLL, MR-M5 (family at the ring) | Names and Lanterns MLL.4 |
| **Peat Row** | MP02 | A walkway row off Marshfall's main ways | Walkways; ditch by state | Straight or dog-leg by `MWS_MARKER` | MWS | Work and Skills MWS.3 |
| **The root-timber lot** | Past Rootrest | A clearing of cut roots on firm ground | Walkable | Quota board | MEP | Names and Lanterns MEP.4 |
| **Hessel's yard, plank way, cutting bank** | MP04 | Rootrest | Plank way with a stake | Rick and shed | MRW | Settlements MRW.5 |
| **Halsey's post** | MP21 | Dry hump above the crossing | Walkable | — | MNK | Settlements MNK.5 |
| **Annot's blind** | MP27 | Dry lip above the Hollow | Walkable | — | MRH | Settlements MRH.5 |
| **Wystan's hut** | MP22 | Near the granary | Walkable | Lantern by the door | MHG | Work and Skills MHG.3 |
| **The great furrow** | Below Bannerline | Seen from MP17 only | **Unreachable** | None | MR-M5 `S02`, MDS07 | Act III §5.2 |
| **The archive loft**, **Keel house**, **Rudd house**, **Lusk house**, **Tolley house**, **Wren and Lister houses**, **Copse house** | Sub-areas of MP01, MP02, MP03, MP06 | As listed in §4 | — | — | MBA, MEP, MFW, MFH, MSS, MBO | Side files |
| **Memorial gardens** | MP01 | Sorrowmere | Raised beds on built-up ground | Lantern on a post with `MLW_KEEPER = gardens` | MLL, MLW | Names and Lanterns |

**Never visited or built:** the far side of Mirebone Crossing; the old ferry way's far reaches (it runs Sour; no content walks it); the path to the great furrow; anywhere outside the Mire.

---

## 6. Zone-state table (per player)

All states are **per-player presentation** (bible §9). Co-op fallback: the host's props; each player's own flags drive their own barks, dialogue and epilogue.

### 6.1 Keyed by region flags (`MR_`)

| Flag = value | Where it shows | What changes |
|---|---|---|
| `MR_CHANNELS` = true | Every stake | Stake inspect text gives the state. Always true after MR-M1 `S02`. |
| `MR_NAME_RECORD` = amended / qualified | MP01, MP02, MP08 C3 | Register page; Hayle book (Nell's name beside Linnet's / a ribbon); Mara's stone unnamed in both; MR-M5 placement |
| `MR_CAUSEWAY` = unset / reset | MP08 | Roadside standards and crew lifting (unset) → pale holes, crews call Mara instead of lifting (reset) |
| `MR_BANNERS` = retired / restored | MP14, MP03, MP12, MP07 | New pool row (retired); banner over the vigil-hall door, Corra under it, banner at S1 during the rite, distant banner from the Field on clear days (restored) |
| `MR_ROWAN_TRUST` = told / kept | MP12 C5, MP06 | Rowan at stone S12 (told); the landing lantern lit below, seen from the gap (kept) |
| `MR_WARDEN_RECORD` = sorrowmere / altar / tenders | MP01, MP13 | Leaves on the register room stand; box under the altar with leaves; leaves pegged in the Tenders' chest |
| `MR_BANNERLINE` = quieted / tended | MP12, MP03, MP17 | §6.4 and Act III §E.1–E.3 |
| `MR_STANDING` = true | MP02, MP06, MP03 | Commission givers: Hob (Marshfall), Rowan (landing), Ide with a leatherworker (Griefwatch) |
| `MR_STRANGER_SEAT` = true | MP01, MP03, MP04 | Seats unchanged; "witness" address in Rootrest and Griefwatch; Ysolde's hand on the seat at the MR-M5 meal |
| `MR_ARRIVALS` = named / held | MP01 | Arrivals wall strip text |
| `MR_LANTERN_LINE` = true | MP11, MP12 | Haddow ring lit; the Haddows light the Bannerline ring's lanterns |
| `MR_CLOTH` = returned / burned | MP14, MP12 S4 | Recovered cloth in Calwen's store and at the foot of his stone (returned) |

### 6.2 Crossing register (bible §9.2, N-1) [PROPOSAL — DIRECTOR]

**Canonical for implementation; quest packages defer to this register** (MC-1). Every crossing below has an id, its stake, its walkable segment and the state it shows when no quest pins it. Quest pins override for the pinning player only. The **free-travel default** is used whether or not the per-crossing schedule (N-1) is built; if N-1 is never built, the default column is the whole schedule.

| Crossing | Place | Walkable when | Free-travel default (morning / noon / dusk / night) | Quest pins |
|---|---|---|---|---|
| X01 Causeway first crossing (C1) | MP08 | Slack | Slack / Slack / Running / Running | MR-M1 `S02` Running→Slack on keep watch; `S04` Sour as the cart passes; MLD Slack |
| X02 Causeway second crossing (C4) | MP08 | Slack | Slack / Slack / Slack / Running | MR-M1 `S03` Slack; `S04` Sour behind the cart; MLD Slack |
| X03 Causeway far end (C6) | MP08 | Slack | Slack / Slack / Slack / Running | MR-M1 `S04` Sour behind the cart |
| X04 Old ferry way | MP01–MP02 | Running (boats) | Sour at every hour this season | None. Never used as a route. |
| X05 Rowan's route (C1, C4, buttress) | R5, MP13 | Rowan's Slack (cuts still, shoal hauled) | Slack / Slack / Running / Running; **Rowan ferries morning and noon only** `[MD-3]` | MR-M3 `S03`, `S05` (grey); MR-M4 buttress stake per Act II §B8.2 |
| X06 Landing home channel and bank | MP06 | Bank: Slack; mud: Slack or Sour | Slack / Running / Slack / Sour | MFH pins |
| X07 Meres feeder channel | MP26 | Slack | Slack / Running / Slack / Running | MRS pins |
| X08 Nine Stakes | MP21 | Slack (knee), Running (waist) | Slack / Running / Sour / Running | MNK pins |
| X09 Granary under-store | MP22 | Slack | Running / Slack / Running / Running | MHG pins |
| X10 Peat Row ditch | MP02 | Reach at Slack, wade at Running | Slack / Running / Slack / Running | MWS pins |
| X11 Reed Hide plank way | MP23 | Slack | Running / Slack / Running / Running | MCF pins |
| X12 Wading Ford | MP25 | Slack | Running / Running / Slack / Running | MFW pins Slack at dusk |
| X13 Sorrowmere pool | MP01 | (view only) | Slack / Running / Running / Running | MDS01 reads at Slack |
| X14 Rootrest plank way | MP04 | Always walkable (presentation stake) | — | — |
| X15 Mirebone ford | MP10 | A few steps only | Ford line variant changes every turn | MDS10 |

Rules: waiting is always available at a `watch_bench`; no crossing on a required route is non-walkable at every hour; the default never blocks travel for longer than one keep-watch turn. MLD's wonder moment (every crew stake Slack at once) works because the defaults differ.

### 6.3 The Chapel by stage (MP13) `[MD-4]`

| Phase | Water | Walkable ground | Posts | Shades | Custody props |
|---|---|---|---|---|---|
| Before MR-M3 `S06` | — | Not reachable | — | — | — |
| MR-M4 `S01`–`S02` | Flooded to just below the gallery | Roof, loft, gallery | Roof T1–T2 (6), loft (2), G6 | Loft and gallery dark ground | — |
| Stage 1 (Board B) | Stage 1 | + N1 aisle walk | + P1–P4 | Dark ground until lit | — |
| Stage 2 (Board C) | Stage 2 | + N2 bays, vestry | + P5–P9 | As above | — |
| Stage 3 (Board A) | Stage 3 | + N3 floor, altar, crypt | + P10–P13 | As above; glass event freezes Shade volumes ~5 s | — |
| `S06` draught | Stage 3 | All | Each post gutters once in a wave; top post exempt; relit posts stay | Faster formation and press | — |
| Post | Stage 3 | All | Main paths lit | Dark corners only (vestry, crypt stair) | By `MR_WARDEN_RECORD` |

Wrong-order boards reset harmlessly; a board at Running will not turn. Stage never regresses.

### 6.4 Bannerline crown (MP12)

| Phase | Standards | Lanes | Gap | Road |
|---|---|---|---|---|
| Before MR-M5 | Risen along the arc (presentation; no Wraiths without the quest) | Quiet furrows | Footing stone | Gate open (MBO); no package uses the bends or crown; walkability open (Q-3, §13) |
| MR-M5 `S02`–`S06` (night pin) | Three at the lane heads retired in `S04` | Files on the count | Held in `S06` | Shut at W1 until `S03`; bends held behind the player |
| `quieted` | Laid in the earth inside the ring (mound) | Quiet | New unmarked stone | Open; gate tied back |
| `tended` | Re-raised in community cloth, hanging still (honoured) | Quiet | Stepped footing stone; nightly keeper | Open under watch; count slate |
| Night Count `[MD-8]` | As by outcome | Files on the count during the fight | Keeper steps off (`tended`) | — |

### 6.5 Other quest-local states that change a place

| Flag | Place | Change |
|---|---|---|
| `MBR_PINS` = self | MP08 | One post carries the player's pins (MLD inspect) |
| `MCS_OUTER_LIT`, `MCS_STAGE` | MP13 | §6.3 |
| `MSS_SEAT_LEGS`, `MSS_RUBBING` | MP04, MP01 | New legs; rubbing pinned in the register room |
| `MEP_HOME` | MP01 | Index-board column; Lew at the table |
| `MLL_PLACE` = ring / garden | MP11, MP01 | Where the Haddows' lantern stands |
| `MLW_KEEPER` = roof / gardens / landing | MP13, MP01, MP06 | Where the seven-night lantern stands (MLD reads it) |
| `MBS_FATE` | MP14 | Banner retired or kept unsorted |
| `MMR_MAP` | MP01 | Lenna's map corrected or annotated |
| `MWS_MARKER` | MP02 | Walkway straight or dog-leg; marker in Calwen's chest or under the walkway |
| `MHG_KEY` | MP22, MP01 | Key custody props |
| `MBO_RULE` | MP03 | Roster board strips |
| `MNK_NINTH` | MP21 | Ninth socket marker; caps |
| `MRH_ANTLER` | MP04, MP16 | Antler on the bench or the rail |
| `MRS_HOB_BENCH`, `MFH_TOLLEY_BENCH`, MFT Completed | MP26, MP06, MP05 | Public stations |
| `MDS##_SEEN/READ` | Discovery sites | Repeat presentation suppressed; MDS07 post-story line |

---

## 7. Time, weather and phasing rules

| Rule | Requirement |
|---|---|
| Presentation hour | Per player: morning, noon, dusk, night. Advanced by quest events and by keep watch. **Never world time.** No world clock, no calendar. |
| Night pins | MR-M1 `S04` (dusk to night); MR-M5 `S02` dusk to `S07` (night). Logout resumes at the pinned hour. |
| Quest-local weather | The grey (MR-M3 `S05`, fog with four densities along R5) `[MD-3]`; rain on the Chapel roof (MLW); dry stretch (MLD); storm, ambience only (MSG). All per player; leaving the area pauses them. |
| Season | **None.** The long wet continues throughout. The Mire has no season flag; its first dry stretch is MLD's quest-local weather only. |
| Dusk spawns | Banner Wraiths walk at dusk at any **risen** standard a quest uses (MR-M1 `S04`, MR-M2 `S05`); lifting a risen standard wakes them at any hour. Outside quests, standards are presentation only. |
| Missed moments | A missed dusk, turn or ask re-offers at the next turn (bible §11 rule 4). |

---

## 8. Relative placement, sightlines and exclusions

All **MAP VERIFICATION REQUIRED**.

### 8.1 Must be near or in sight

| Place | Must be near / see | Why |
|---|---|---|
| Causeway head (S4) | Three standards in three states (N1) | MR-M2 `S01` |
| C5 relaid section | The old line beside the new for ~40 paces, both with posts | MR-M1 `S04` lit-post fork |
| Turnout platform | Black water beside it; reachable at dusk; about three minutes' walk from the causeway head | MR-M2 `S05`; MLD walk |
| Bell-loft window (G2) | Buttress stake and culvert A's stain | MR-M4 `S03` |
| G4, G5 windows | Their own culvert mouths and stains | MR-M4 `S03` |
| Great window | Wholly below gallery level; outer face against peat | MR-M4 glass moment |
| Bran's platform edge | The great furrow below | MR-M5 `S02`; MDS07 |
| The gap (C4) | Down over the Mire; with `kept`, the landing lantern (or a light on the nearest channel) | MR-M5 strange moment variant |
| The Field (clear day) | Griefwatch's restored banner far off (optional; omit if no sightline) | Epilogue §E.5 |
| Nine Stakes rise (N2) | The whole crossing line and the island | MNK range inspect |
| Sorrowmere pool edge | The ring of sunken stones at Slack | MDS01 |
| Stillgrave near edge | The surface for the reflection | MDS02 |
| Hob's hide slot | The mere and its depth stake | MRS heron moment |

### 8.2 Must not be seen or reached

| Constraint | Why |
|---|---|
| Any walking route to the Chapel | Rowan's route is the only way (canon; MR-M3 premise) |
| The Chapel from Sennic's rise or the landing | "You can't see it from here. Nobody can." |
| The great furrow on foot | Sorrowback trail; seen, never followed (CV-M2) |
| Mirebone's far side; any route out of the Mire | MD-9, FT-03 |
| Any compass direction toward another region; "eastern" wording | MD-9 |
| The Reed Hide from the causeway road | Found by tracking (MCF) |
| Deep water underfoot anywhere | No swimming, no drowning |
| A star motif anywhere in the Chapel | The name's origin is never explained |
| Anything that links the Turning Stone's ring and the Bannerline circle | Bible §7.5 |
| Hollowfoot anywhere but the Rag Bend in MR-M5 (enemies) and Lysa's care (non-combatants) | MD-7 dignity rules |

---

## 9. Terrain early-check register (lessons from Lowmark TC-01 to TC-19)

Lowmark's provisional terrain broke beats that depended on adjacency to water (TC-01: Crest Hall 640 m from the river, blocking MQ10), on stilt access (TC-12) and on walking times (TC-18). No Mire terrain exists yet, so the Mire can avoid that by naming its geometry dependencies **before** the terrain pass. Each row below is a beat that **depends on distance or water geometry**. The terrain pass should check these first and surface mismatches to the Director rather than relocating anything. Severity uses the Lowmark key (**Blocks** / **Degrades** / **Cosmetic**). Distances are narrative intents, not terrain values.

| Id | Dependency | Beats that rely on it | If wrong | Severity |
|---|---|---|---|---|
| **MT-01** | The Standards Causeway is a **continuous walkable line** from Sorrowmere's edge to the Marshfall side, with exactly **two stake dips** (C1, C4) and a far-end stake (C6), and it is the only dry link this season | MR-M1 `S02`, `S04` (cart walk); MR-M2; MLD | Escort and stake lessons fail | **Blocks** |
| **MT-02** | Causeway **length**: MR-M1's night cart walk must be long enough for three stake turns, a fork and a Wraith lane; MLD wants the turnout ~3 minutes' walk from the head | MR-M1 `S04`; MLD; MR-M2 `S05` | Pacing (too long is tedious, too short loses the turns) | Degrades |
| **MT-03** | Mara's marker (C3) on a low peat ridge **off** the causeway by a plank; the ditch and embankment at standard 3 on the ditch side; the black water beside the turnout | MR-M1 `S03`; MR-M2 `S03`–`S05` | Holds and set pieces lose their place | Degrades |
| **MT-04** | Edris's old station at the causeway's Marshfall end; Marshfall a **short walk** on; Rootrest and the Fenward **beyond** Marshfall on firmer ground | MR-M1 `S02b`–`S04`; MFT; MRW; MEP | MR-M1's "holds in any order" becomes a long march | Degrades |
| **MT-05** | Blackwater Landing **below** Sorrowmere and walkable from it; Sennic's rise and Stillgrave's near edge on foot along the peat edge | MR-M3 `S02` (four tasks across three sites, several hour-turns) | MR-M3's quiet preparation pacing breaks | Degrades |
| **MT-06** | Rowan's route order: landing → junction one → shoal (tow path along a bank) → Drowned Encampment cut (room for **three stretches**, ~12 s poling each) → junction two → Stillgrave's open far side → fog bank → Chapel | MR-M3 `S05`; Chapel route | The crossing set piece cannot play as authored | **Blocks** |
| **MT-07** | Chapel interior: a nave deep enough for **three discrete water stages** below a gallery; window sightlines to the buttress stake and three outfall stains; lantern posts spaced so every required path is inside a ~6 m lit radius once lit | MR-M4 `S03`–`S06` | Puzzle unreadable; Shade press on required paths | **Blocks** |
| **MT-08** | The Chapel is reachable **only by boat**: no walkable path from the landing, the Encampment's landward side, Stillgrave's near edge or the Wading Ford | MR-M3 premise; MR-M4 | Rowan's refusal and the route reward lose meaning | **Blocks** |
| **MT-09** | No sightline to the Chapel from Sennic's rise or the landing (fog bank helps) | MR-M3 `S02` | Sennic's line contradicted | Cosmetic |
| **MT-10** | Bannerline crown: ~30 × 35 m arena; three lanes ~3 × 25 m with ~4 m turf strips; a ~16 m twelve-stone ring below the lanes with the gap facing the Post Lane; gentle slope beyond the ring | MR-M5 `S04`–`S06`; Night Count | Boss telegraphs (move on two) and ring leash fail | **Blocks** |
| **MT-11** | Nine Stakes: a shallow a long stone's throw across with depth by state (knee / waist / non-walkable) and an island reachable at Slack or Running; a downstream side channel | MNK | Crossing reading and fight layout fail | **Blocks** |
| **MT-12** | Shallows next to every lane and causeway edge stay shallow (no deep water within knockback reach) | MR-M1, MR-M2 Wraith shoves; MR-M3 boat knockback | Accidental deep-water stops mid-fight | Degrades |
| **MT-13** | Sightlines from the crown down to Blackwater Landing (`kept` lantern) and from the Field to Griefwatch (`restored` banner) | MR-M5 strange-moment variant; §E.5 | Both have authored fallbacks (a nearer light; omit) | Cosmetic |
| **MT-14** | Bran's watchpost path leaves from **Griefwatch's side** of the closure gate and never passes through it (requirement; MAP VERIFICATION REQUIRED) | MR-M5 `S02` (road shut) | Step soft-locks behind the gate | **Blocks** |
| **MT-15** | Bran's platform edge overlooks the furrow, which has no path down | MR-M5 `S02`; MDS07 | Discovery lost or the Sorrowback becomes reachable | Degrades |
| **MT-16** | Griefwatch at the foot of the Mire's **only** high ground; the road with three distinct bends | MR-M5 `S03` | Pacing and checkpoints | Degrades |
| **MT-17** | Raised settlements (Sorrowmere, Marshfall, the granary, Fenward step) have raised floors with walkable access at every water state the content uses | All hubs | Lowmark TC-12 repeat (stilt access undesigned) | Degrades |
| **MT-18** | Regional travel times between hubs (Sorrowmere, Marshfall, Rootrest, Griefwatch, the landing) | MSS (three settlements), MHG (three), MBA, MEP | Lowmark TC-18 repeat; pacing text retune | Degrades |

---

## 10. Architecture needs for Sol

**Status of the tools** (as recorded in the Lowmark register §2). The architectural generator (v0.16.0) is an **offline Blender exterior generator** with twenty building types and four regional grammars. Its Mire grammar and the Mire section of `WORLD_ARCHITECTURAL_LANGUAGES.md` are "reversible visual interpretations, not new canon". It offers four Mire local contexts: **Sorrowmere, Marshfall, Griefwatch, Rootrest**. Its Mire world language already provides raised floors on supports, slender modular upper volumes, working decks, screened private links, gate landings, boat slipways and curved roof ribs where Mire builders use bowed roofs. Function-first programs exist only for Smithy, Market Hall, Stable and Gatehouse; the Mire Market Hall reserves a rear cross-aisle and a quay connection. The tool does not make interiors or enterable layouts (except floor-separated visuals for preview), arbitrary polygons, settlement networks or terrain fitting. Footprints are RECT, L, T or U only. Final art acceptance is the Creative Director's. The other tools touch the Mire only as context: the terrain generator (`CODE/Scripts/terrain_generation/README.md`) is a Lowmark-only offline prototype, so **no Mire terrain exists**; the Unity architecture pipeline (`UNITY/ARCHITECTURE_PIPELINE.md`) prepares generator exports for later hand placement and creates no settlement, occupancy areas or navigation links; the material painting library (`MEDIA/Materials/README.md`) is art-direction material and confers no resources or canon. Nothing below asks to change any of them.

**This section is a set of requests for Sol and the Director to accept, change or reject. It is not a prescription.** It names no material, colour, palette or finish; visual style belongs to the Creative Director. The Mire regional style below means "whatever the generator's Mire grammar and context produce", and nothing more.

### 10.1 Mapping to existing building types (Mire region, named context)

| Mire building (POI / area) | Nearest existing type | Context | Note |
|---|---|---|---|
| Sorrowmere longhouses, Ferrow house, Keel house, reed-cutter's house (MP01) | Longhouse; Cottage | Sorrowmere | Ferrow house "on taller piles than its neighbours" is a support-height variation within the grammar. |
| Register room (MP01 S2) | Assembly Hall | Sorrowmere | The **interior** (long table, reading board, index boards, the seat) is hand-authored; the archive loft above needs a usable upper floor and ladder. |
| Long table shelter (MP01 T1) | Market Hall (open-sided) | Sorrowmere | Request only: an open reed-roofed shelter; Market Hall's program may be too specific. |
| Calwen's sanctuary sheds and frames (MP14) | Workshop | Sorrowmere | Retirement pool is a ground feature, not a building. |
| Marshfall stilt houses, Hayle and Rudd houses, Peat Row (MP02) | Cottage; Longhouse | Marshfall | Smoke shed **under** the Hayle house is a request (open space below the floor). |
| Marshfall smoke sheds, peat yards | Workshop; Barn | Marshfall | — |
| Marshfall jetty stall | Shop | Marshfall | Small trestle stall; may be a prop rather than a building. |
| Edris's old care station (MP08 M1) | Workshop or Stable massing, **ruined** | Marshfall | Needs a half-roofed, one-wall-standing state (gap A-6). |
| Griefwatch vigil hall (MP03 W2) | Assembly Hall | Griefwatch | Stone footings under the hall ("the only stone floor in Griefwatch") are a request; the bell rope through the roof to a vigil bell needs a bell cote or frame. |
| Griefwatch closure gate (MP03 W1) | Gatehouse (functional program) | Griefwatch | A **timber gate between two stakes** is far lighter than the Gatehouse program; may be a prop. |
| Griefwatch bell households' row, Copse, Wren, Lister houses | Cottage; Longhouse | Griefwatch | Door lintels need a chalk-mark decal surface. |
| Bran's watchpost (MP17) | Watchtower, **broken** | Griefwatch | Half the platform gone; lean-to under it (gap A-6). |
| Rootrest hall, herbalists' room, Hessel's house (MP04) | Assembly Hall; Cottage | Rootrest | Built **half under the roots of an old tree**: gap A-4. |
| Fenward huts (MP05) | Cottage (smallest) | Rootrest | "Low reed-and-root huts round a fire pit"; high interior shelves above a flood line. |
| Blackwater Landing boat shed and docks (MP06) | Boathouse | Sorrowmere | The generator's own example is a Mire Sorrowmere Boathouse. Rowan's boat on trestles inside. |
| Ferry households' row, Tolley, Lusk houses (MP06 L6) | Cottage; Longhouse | Sorrowmere | Tolley bench under an open eave. |
| Hushed Granary (MP22) | Grain Store on tall supports | Marshfall | Needs a floor hatch reachable from below and a ladder to a locked door. |
| Wystan's hut | Cottage (smallest) | Marshfall | — |
| Halsey's post (MP21 N1) | Watchtower (low) or shelter | Marshfall | A shelter on a dry hump; may be a prop. |
| Mabyn's roof loft (MP13 T3) | — | — | A shelter built **against a bell-tower on a sunken roof**: part of gap A-1. |

### 10.2 Gaps, stated as requests

| Id | Gap | What the content needs | Request |
|---|---|---|---|
| **A-1** | **The Chapel of the Sinking Star**: no religious type, no partially submerged or sinking state, no interiors | A roof ridge just above water with a squat bell-tower at one end, tower hatch, bell-loft with an empty bell frame, three-sided gallery on corbels, a nave with three water stages, vestry, great window below gallery level with its outer face against peat, crypt under the altar step, outfall culvert mouths on the outer wall with stains, a painted buttress stake. | Treat as a **hand-authored landmark**; the generator could at most supply a roof/tower shell for blockout. The Mire language already reserves sunken wartime structures "as partially submerged ruins", which fits. Ask Sol whether a "sunken civic hall" state is worth a tool extension or is cheaper by hand. |
| **A-2** | **Interiors** | Register room, archive loft, vigil hall, Rootrest hall, Hayle and Rudd houses, Keel and Ferrow houses, hearth hut, boat shed, granary interior, the whole Chapel. | Hand-authored interiors on generated shells, or the floor-separated preview extended to enterable rooms; Sol's call. List priority: Chapel, register room, vigil hall (required steps); the rest are inspect-only. |
| **A-3** | **Walkway networks** | Sorrowmere's raised ways between buildings, the jetty, Marshfall walkways and Peat Row (with a sunk section and a root-run section), plank spurs off the causeway, the Reed Hide plank way, the Rootrest plank way. The generator makes per-building decks and links only. | A settlement-scale walkway or plank-way tool, or hand placement with a kit. The Standards Causeway (a log road across bog) and its loose-log segments belong here too. |
| **A-4** | **Root homes** | Rootrest buildings half under great roots; the root arch; the Last Root's rail. Footprints are orthogonal only. | Hand-authored root forms around generated orthogonal rooms, or a terrain-art solution; request only. |
| **A-5** | **Palisades** | Bannerline palisade arc of old stakes with iron-shod lane-head stakes and standards lashed to them; Griefwatch gate posts (former palisade stakes); the Fenward/Rootrest fences. | A stake-line or palisade kit following a curve. Not a building type in the tool. |
| **A-6** | **Ruins** | Edris's old care station (half roof, one wall), Bran's broken watchpost, the Drowned Encampment (wagon wheels, tent poles, stove), the Sodden Pyres trunks, the Unfired Kiln, the Singing Trench bays and vents, the Reed Hide trench, the Dry Muster furrows. | A ruined or abandoned state for existing types (watchtower, workshop) would cover two; the rest are terrain and prop work. |
| **A-7** | **Small water structures** | Channel stakes, sluice windlasses and culvert mouths (Chapel), the retirement pool, the Hushed Granary hatch, Nine Stakes sockets, mooring posts. | Props, not buildings; listed so nobody expects them from the generator. |
| **A-8** | **Stone circles** | The twelve-stone Bannerline circle with its gap; the Turning Stone's sunken ring. | Terrain and prop work. They must not read alike (§8.2). |

### 10.3 Questions for Sol

1. Is a sunken/partially submerged state for an existing civic type (Assembly Hall) a sensible tool extension for the Chapel shell, or is the Chapel cheaper wholly by hand?
2. Can the Mire world language's per-building links be chained into a settlement walkway network (A-3), or should walkways be a separate kit?
3. Does the floor-separated visual preview help the Chapel's vertical blockout (roof / loft / gallery / nave)?
4. Which Mire context should the Hushed Granary and Blackwater Landing use (Marshfall and Sorrowmere are proposed above)?

---

## 11. Integration dependencies (documented only; nothing implemented)

Runtime needs are registered once in `Quests/Caelmor_Mire_Integration_Requirements.md`. The zone-owned ones:

| Need | Owner | Minimum viable form | Integration id |
|---|---|---|---|
| Crossing register (§6.2) as per-player state with free-travel defaults | Systems + ZN | Per-crossing three-state table keyed to the presentation hour; quest pins override; default column is the fallback schedule | MI-CH-01, MI-CH-02 |
| Standard prop states | Systems + art | Seven states, per player | MI-PP-02 |
| Chapel water stages and posts (§6.3) | Systems + art | Environment variants by `MCS_STAGE`; post states; lit-radius gating | MI-WL-01, MI-LT-01 |
| Bannerline crown states (§6.4) | Systems + art | Prop sets by outcome; placement marks | MI-PP-05 |
| Multi-level NavMesh and interaction-driven ladders | Systems | Chapel, granary, watchpost, loft | MI-AG-02 |
| Edge stops for deep water; no-deep-water knockback lanes | Systems + ZN | Edge volumes with a bark | MI-AG-03 |

---

## 12. Phase 1.5 count check

| Category (Phase 1.5 §3) | POIs | Count |
|---|---|---|
| Settlements | MP01, MP02, MP03 | 3 |
| Micro-settlements | MP04, MP05, MP06 | 3 |
| Ruins / war sites | MP08, MP09, MP12, MP17, MP19, MP20, MP24, MP28 | 8 |
| Caves / dungeons | MP13 | 1 |
| Camps / bandit sites | MP21, MP23 | 2 |
| Shrines | MP14, MP15, MP16 | 3 |
| Unique landmarks | MP07, MP10, MP11, MP18, MP22, MP25 | 6 |
| Hunting grounds | MP26, MP27 | 2 |
| **Total** | | **28** (range 24–32) |

New places in §5 are sub-spaces or never-visited names. The Mire has no mine by design (MD-11).

---

## 13. Open map questions for the Director

1. **Q-1 Hub connections.** No package states how Griefwatch and Rootrest connect to Sorrowmere and Marshfall ("the ordinary way"). Recommend: Rootrest only beyond Marshfall (bible order); Griefwatch by a firm-ground path from Sorrowmere's landward side that does not cross the Field. Both MAP VERIFICATION REQUIRED and needed before MSS/MHG pacing is checked (MT-18).
2. **Q-2 Free-travel crossing defaults (§6.2).** Approve the default column, so travel works whether or not the per-crossing schedule (N-1) is built.
3. **Q-3 Bannerline road before MR-M5 [OPEN].** What the packages state: the closure gate stands **open** before MR-M5 (MBO W1: "the gate open at this point in the story"); Mara found a spoon at the road edge (MSS); MDS06 reads the gate posts, and its Iron Bend reading is offered only after MR-M5; Ide shuts the road at MR-M5 `S00`, opens it at `S03`, and it is open after MR-M5 in both outcomes (Act III §10). No package sends the player up the bends or onto the crown before MR-M5, and none says whether they may go; bible §11 rule 6 lists the road as an access reward, which reads as if it were shut. Recommendation: no extra gate; before MR-M5 the bends and crown are walkable as presentation only (risen standards, no Wraiths, no files; muster post and circle not interactable), the reward is the road's reopening after the closure, and the only gate is MR-M5's per-player closure from `S00` to `S03`. Alternative: the road is shut beyond the gate until MR-M5 (MBO's W1 bark changes). MAP VERIFICATION REQUIRED.
4. **Q-4 Edris's old station** folded into MP08 (decided here per Act I A14.7); confirm.
5. **Q-5 Mirebone Crossing** stays a discovery with no far side; confirm.
6. **Q-6 Distant sightlines** (MT-13): keep both with fallbacks, or drop them now?

---

## 14. Inconsistencies found and recommended canonical values

**Shared canonical register (canonical for implementation; quest packages defer to this register).** The three Batch 4 handoffs (Enemies, Zones, Integration) state these values in the same words. The Enemies file numbers its rows C-1 to C-12 and governs every combat value; MC-2, MC-4, MC-5 and MC-9 below were aligned to it on 2026-11-09, and the crosswalk is in Integration §5.1. Where a quest package gives a different number, the package value is superseded for implementation; the package text changes only when its author next edits it.

| # | Topic | Canonical value |
|---|---|---|
| MC-1 | Channel states | Three states (Running, Slack, Sour) per crossing, keyed to the presentation hour. Quest pins override for the pinning player. Free-travel defaults per Zones §6.2 [PROPOSAL — DIRECTOR]. Rowan's Chapel route runs at Slack, **morning and noon only** `[MD-3]`. Waiting is always available. |
| MC-2 | The count (Bannerline) | Two soft beats, then the third. **1.2 s per beat** (3.6 s per count); General phase 3 **0.9 s per beat**. Every count attack lands on a third beat and is shown on beat 2 at the latest; in phase 3 **every** count attack is shown on **beat 1**, and the bearer's Plant ring shows from beat 1 everywhere. The count itself never damages. Audio, ground ripple, optional rumble and optional caption carry each beat. (Enemies C-7) |
| MC-3 | Lantern posts and Shades | Lit post radius **~6 m**; hand lantern radius ~3 m. Shades form after **~6 s** in dark ground (draught **~3 s**); a press every **~4 s** (draught **~2 s**) after a ~2 s lean tell; at ember the next press pushes the player to the nearest lit post. **No damage.** Shades have no HP and are never targetable. |
| MC-4 | Banner Wraith re-form | In an encounter, a defeated Wraith re-forms at its standard **~25 s** after defeat with a **~3 s** forming tell **while** the standard is risen or lifted-unfolded; folding ends it; live Wraiths fight on to 0 HP. The Risen Colour's standard pulses every **~30 s** (~3 s tell). Bannerline Wraiths re-form on the next third beat. Outside an encounter, a standard still risen repopulates at the **next dusk**. (Enemies C-3) |
| MC-5 | Earthen Echo re-form | By condition only, never by health. Default spot timer **6 s** (MLL while the ring is unfinished; MMR while survey stakes stand); MR-M3 banks **~10 s** while the grey lasts and the boat is in the stretch (boat pacing); Bannerline files at the lane head on the next third beat while the circle is open. Echo swings have no knockback. (Enemies C-3, I-6) |
| MC-6 | Water and edges | No swimming, no drowning, no fall deaths. Deep water is non-walkable with an edge stop. Shallows walkable and slowed. No knockback ends in deep water or off a raised edge. |
| MC-7 | Defeat | Every enemy defeated at 0 HP (CDR-1); humans (Raiders, Rootshadow, Hollowfoot `[MD-7]`) take the ordinary defeat presentation. **No SX entry; the quest on-defeat hook is not used by the Mire.** |
| MC-8 | Ranged | First-class in every fight, never required. No spot the enemy cannot reach: the General's leash excludes the ring (~5 s with nobody in the arena resets to the top of the phase). |
| MC-9 | Hazard floor | No Mire hazard can defeat a player above **25% HP** (Enemies C-2, the Thornfell value); the gap step-off costs ~15% max HP, knocks back toward the gap stone and never costs rite progress. |

| # | Inconsistency | Packages | Recommendation |
|---|---|---|---|
| **Z-1** | **Sluice order "by rope bands"** in bible §11.1's mechanics table; the bible's own §6.1 and §13 and Act II read the order from **water stains** on the chapel walls. | Bible §11.1; Act II §B8.2 | Water stains (Act II). **Fixed in bible §11.1 (2026-11-09).** |
| **Z-2** | **Boats ground at Slack** (bible §1.1) vs **Rowan ferries at Slack** (bible §6.1). | Bible; Act II A14.2 | Act II's reconciliation: Rowan's narrow cuts go still at Slack and he hauls the dry shoals. Route geometry must include a shoal with a tow path (MT-06). **Fixed in bible §1.1 and §6.1 (2026-11-09).** |
| **Z-3** | **MR-M3 reed** cut "at the meres" (bible) vs at the landing's own reed beds (Act II). | Bible §6.1; Act II A14.3 | Landing reed beds (L4); MP26 unaffected. **Fixed in bible §6.1 (2026-11-09).** |
| **Z-4** | **Edris's old station** unplaced as a POI. | Act I A14.7 | Area of MP08 (§4). |
| **Z-5** | **Bannerline road access before MR-M5** only partly stated (gate open per MBO; bends and crown unstated). | Act III; MBO; MSS; MDS06; bible §11 rule 6 | Stated per the packages in Q-3; crown access **open** for the Director. |
| **Z-6** | **Bran's watchpost reached while the road is shut.** Act III places it "off the road" but does not say which side of the gate. | Act III §5.2, `S02` | Requirement: path from Griefwatch's side, never through the gate (MT-14; MAP VERIFICATION REQUIRED). Bible §4.2 now states it. |
| **Z-7** | **Crossing defaults outside quests** are not authored anywhere; the Chapel route, MDS01, MDS10 and free travel need them. | Bible §9.2; all packages pin | §6.2 register. |
| **Z-8** | **MLD's turnout distance** ("about three minutes each way") is the only stated distance on the causeway; MR-M1 needs room for three stake turns. | MLD.4; Act I | MT-02; check together. |

---

## 15. Review log

| Check | Result |
|---|---|
| Coverage | MP01–MP28 each have function, placement, areas, quest uses, state, props, traversal/water and map note. §5 lists every new place found in the main acts and the four side files. |
| Water | No swimming, breath meter or drowning anywhere; every crossing has a stake and a bench; every deep-water edge stops the player; Chapel stages are environment variants `[MD-4]`. |
| Traversal | Every agility trigger has a walkable fallback; the Chapel is boat-only; the furrow and Mirebone's far side are unreachable. |
| Binding rules | No compass direction, no interregional route, no "eastern" wording, no star motif, no Hollowfoot outside MD-7's two places; no SX; ranged parity via the General's leash. |
| Architecture | Requests only; no material, colour or finish named; style left to the Director. |
| Terrain lessons | MT-01 to MT-18 name every distance or water dependency for the first terrain pass (Lowmark TC-01, TC-12, TC-18 pattern). |
| Scope | No schema, JSON, scene data or C#. |
| **Reconciliation (2026-11-09)** | Re-checked against the side-quest review fixes (e98147e): MSG's timed gust cycle removed (MP19, §7); MLD's swarm is leashed scenery with no settle state and its escort is a standard group follow; MLL's hold is a standard hold bar. §14 MC-2, MC-4, MC-5 and MC-9 aligned to the Enemies file (C-3, C-7, C-2, I-6). **Still to re-check** if the Enemies file changes before commit. |
| Batch 4 zones/integration review, 2026-11-09 | Independent review. **Fixed:** colour and finish wording removed from §2 ("grey-green") and MP08 ("grey timbers"); the Bran's-watchpost path is now stated as a requirement in §1, MP17 and MT-14 (never through the closure gate; MAP VERIFICATION REQUIRED); Q-3 restated per the packages (gate open before MR-M5 per MBO; bends and crown access left open, with a no-extra-gate recommendation and its alternative), §6.4 and Z-5 aligned; MP12 Rag Bend carries the MD-7 non-combat swap needs (sit spot, walk line); §0.2 records the MLL Echo slow as the same lit-radius effect (one need, MI-LT-01); §10 now states the terrain generator, Unity pipeline and material library accurately from their READMEs, with no request to change them. Z-1, Z-2, Z-3 and Z-6 are fixed in the bible. **Checked unchanged:** relative placement only; no interregional route or compass direction; no SX; MD-3/MD-4/MD-7/MD-8 tags; 28 POIs; crossing register X01–X15 against Act I, Act II and the side files. Coordinator additions applied the same day: Batch 3 rename Jem → Lew (§6.5; no Pim, Tam, Tamsin or Ned Rudd found here); Enemies reach rule (wadeable snapper water, §0.1), Mud-Boss island leash (MP21) and the MCF-E1 lookout stair (MP23). |
