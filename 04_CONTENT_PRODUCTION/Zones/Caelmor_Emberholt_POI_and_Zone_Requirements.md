# Emberholt Heights — POI and Zone Requirements

**Status (2026-11-15):** draft; **independently reviewed 2026-11-15** (§15); awaiting Director (ZQ-1 to ZQ-5). Batch 4 of the Emberholt production plan (bible §12). This is the Gameplay Designer's set of level-design requirements for Emberholt. It turns every place in the Emberholt narrative packages into requirements: subzones, routes, POI sub-spaces, heat zones and their states, vertical access, per-player state and relative placement. It also lists what Emberholt will ask of Sol's architecture tools. Every place is **[NEW]** unless the bible marks it [CANON], and nothing here is canon until the Director promotes it (ED-19). **[PROPOSAL — DIRECTOR]** marks consequential choices. **MAP VERIFICATION REQUIRED** marks every place where geometry, distance, height or heat matters (ED-9). **No Emberholt terrain exists.** All placement is relative. No compass direction, interregional route, destination beyond Embergate or travel path to another region is stated, and no "eastern" or "invader" wording is used. This file documents dependencies only. It contains no schema, JSON, scene data or C#.

**Director rulings (binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. For places this means the following. Every enemy is defeated at 0 HP (CDR-1), so no arena needs tied-prisoner props, downed-state space or break-off lanes, and Emberholt has no SX entry. Ranged is first-class and never required (CDR-2): no arena offers the player a firing spot the enemy cannot reach, and no enemy firing spot may be unreachable by a melee player (§14 EZ-7). Emberholt is an internal milestone of the complete game (CDR-3). Ordinary RPG systems are preferred over simulation (CDR-4, ED-6): heat is ordinary hazard volumes with periodic damage, timed vents and safe niches; there is no heat or temperature meter, no stamina, no stealth or detection. Every quest completes solo (CDR-6); co-op presentation never decides another player's walkable ground, step or credit.

**Director rulings applied (2026-11-15):** D-E2 (Thalan freed, the only outcome; places carry the `freed` state only), D-S1 (the Speaker idealist and manipulator, also dream-seeded; no place changes), ED-3 (the initiate is Iven Calder; no place shows the name beyond the EH-M3 chamber roll), D-EL (Elyndra the Cinderseer a living seer met at EP20; no geography changed). **Open Director decisions the places depend on:** C14.2 (placement of the Red-Lit annex), ED-7 (EH-M3 gate), ED-15 (ECC). Places that change if a ruling changes are tagged `[C14.2]`.

**Sources:** bible §4.1–4.2 (EP01–EP28, route order), §6, §7.4–7.5 (EME01–EME10, EDS01–EDS10), §9.1–9.4, §10, §10.1, §11, §11.1–11.2; Act I (EH-M1 ECW, EH-M2 EEH, EH-M3 EGH) place tables, step tables, respawn and logout rows and integration tables; Act II (EH-M4 EAC, EH-M5 ESS) the same; Act III (EH-M6 EGA) §5, §6, §7, §9, §11, §12 and §E; the place and integration tables of the four side-quest files (`Quests/Caelmor_Emberholt_Side_Quests_*.md`); `Zones/Caelmor_Mire_POI_and_Zone_Requirements.md` (format); `Quests/Caelmor_Mire_Playability_Audit.md` (§1, §4: lessons on multi-level dependencies, pins and co-op); Sol's tool documentation: `UNITY/README.md`, `UNITY/ARCHITECTURE_PIPELINE.md`, `CODE/Scripts/architectural_generator/README.md`, `REGIONAL_GRAMMAR.md`, `FUNCTIONAL_PROGRAMS.md`, `WORLD_ARCHITECTURAL_LANGUAGES.md`, `CODE/Scripts/terrain_generation/README.md`, `MEDIA/Materials/README.md`.

**Source state.** The bible and the three acts were independently reviewed on 2026-11-14 and the four side-quest files on 2026-11-15. This file was written against that state.

**Companions:** `Enemies/Caelmor_Emberholt_Encounter_and_Enemy_Requirements.md` (written concurrently; owns encounter ids, creature values, telegraph timings, heat damage, hazard tuning, its register C-1 to C-13, issues I-1 to I-23 and world pockets EW-01 to EW-05; this file was aligned to it on 2026-11-15, §15) and `Quests/Caelmor_Emberholt_Integration_Requirements.md` (runtime needs). Zones and Integration state the shared values in §14 (EK-1 to EK-11) in the same words, each row citing the Enemies C-id it restates.

---

## 0. Level-design constraints

### 0.1 Runtime (what Sol's playable build does today, from `UNITY/README.md`)

| Constraint | Level-design rule |
|---|---|
| Click-to-move over a host NavMesh; Shift sprint; **no jump** | Every required route, objective, valve, wheel, cock, collar, niche, desk and arena safe space is NavMesh-reachable by walking. |
| **No multi-level or off-mesh traversal yet.** The README says the current flat navigation scene has none; in the Flood Kitchen the authored loft stairs are unfinished and the dry-slat crates have flat access markers | Emberholt is the most vertical region so far. Every step that assumes stairs between floors, a ladder, a hatch, a stacked room, a raised gallery or a below-grade space is listed in §5A with a ground-level or flattened fallback where one exists. Proposed (Sol's call, §10 EA-3): ladders as interaction-driven moves ("climb down") until off-mesh links exist. No required objective sits behind an agility trigger. |
| Agility triggers approved, **not built** | Every agility move (U2 ledge, G6 culvert step, ESS duct drop, EWA squeeze, EFS runnel) has a walkable fallback that is the critical path. |
| Timed work is interrupted by moving or **taking a hit** | Channels in heat zones (U5 manifold cocks, U8 relief hold, U9 splices, U10 collars, L4 damper latch, EWA, ESR) must either stand on a safe pad or niche edge, or heat ticks must not count as a hit for interruption. **Request to Sol** (Integration EI-CA-03). Standard fallback, needing nothing new: every channel pad in heat stands inside or touching a cooling-niche volume (no ticks reach it), so heat never interrupts a channel; enemy hits still do. Options for Sol, either acceptable: heat ticks excluded from interruption, or a heat tick pauses the current segment instead of cancelling it (progress kept, EI-CA-01). |
| Telegraphed environmental damage and collision-validated push exist | Vents, plates and enemy shoves use them. **No push may cross a level change** (a step, a ledge, a stair, a pit rim, the U10 plinth) or end inside a Surging zone away from a niche (EK-7). |
| Checkpoint reload starts at the road head; world position is not persisted; death restores at a fixed recovery point | Emberholt's per-step respawn points and logout restore points (§6.6) are requirements on Sol, not features of today's build (Integration EI-QS-06, EI-QS-07). Every respawn point named here is a cooling niche or a safe room, on walkable ground, at grade with the area it serves where possible. |
| Interaction needs reach and line of sight | Channel points used under attack (manifold cocks, stage cocks, relief wheels, splice collars, the draw valve, braziers, the damper latch, bleed cocks) need a standing pad of at least 2 m facing the object, on walkable ground, in every heat state in which the step can run. |
| **Edges and heat** | **No fall deaths.** Pits, slag pools, the railed pit at EP20, the shaft landings, galleries, the ring rim and the terrace edges have rails, edge blockers or a gentle slope. Slag pools and the glass vents of the Hollow are non-walkable hazard volumes with an edge stop and a bark, never a death plane. |
| Per-player state (bible §9.2) | Heat states, quest pins, the EH-M6 frost variant, pressure stages, epilogue props and NPC placement are client presentation keyed to the local player's state. Co-op: each partner's own quest state decides their walkable ground, hazards, interactions, credit and completion. A shared heat state may be shown only as a presentation fallback (Integration EI-CO-06, CDR-6) that never gates navigation, damage or credit. Navigation-affecting conflicts are listed for Sol only (Integration §5.2 EQ-12). |
| Floor visibility | `LocalFloorVisibilityPresentation` / `FloorVisibilityBuilding` is opt-in, presentation-only, not wired into the playable scene and unvalidated. **No Emberholt step depends on hiding upper floors.** Interiors seen from a click-to-move camera (Cooling House, valve house, lamp-house, academy) are authored so that the player is never hidden behind an upper floor at a required interaction; if Sol later validates floor visibility, it is an upgrade. |

### 0.2 The readable system: heat as ordinary terrain (bible §9.2, §11.1, ED-6)

| Feature | Tag | Level-design rule |
|---|---|---|
| **Heat zone** | `heat_zone` | A hazard volume with a state: **Cool** (no damage), **Working** (light periodic damage outside niches), **Surging** (heavy periodic damage outside niches). A state swaps the zone's hazard volume, its vent timings and its tells. Damage values belong to the Enemies file and the Gameplay Designer. **A Surging zone is never a wall:** every required route through one has a cooling niche within reach (EK-6). |
| **Tell** | `tell` | A small heat gauge on a hood, a duct, a kerb post or a door (bible wording: clear, amber, red and crazed). It shows the state of the zone it belongs to and is readable from outside that zone. Inspect text is gated on `EH_TELLS`. One tell per approach is the minimum; the junction (U5) and the bleed house (U8) carry one per line. |
| **Cooling niche** | `cool_niche` | A safe volume (no periodic damage) with standing room for the player and any NPC who shares the step. Every niche has: a water trough or cask to touch (presentation), a keep-watch interaction, and room for a 2 m pad outside it. Niches double as respawn points where the packages name them. |
| **Vent** | `vent` | A floor grate, wall vent or crack that exhales on a cycle. **Ash lifts about 1.5 s before each exhale** (the telegraph). Cycles in the packages: ~10 s (U2 duct grates, K2 second landing, L4 wall vent, ESH duct), ~12 s (U5 junction), ~8 s (U7 bore). The exhale is telegraphed environmental damage; any knock-back follows EK-7. |
| **Pressure plate** | `plate` | EH-M4 plate run (K4) and EH-M6 Draw Sentinel phase 3 floor lines. A plate is primed (visible), vents, is spent, then re-primes (Act II: primed ~0.6 s vent, spent ~8 s, re-priming ~2 s). Timings belong to the Enemies file (§15). |
| **Flarecap** | `flarecap` | A fungus in rock seams. Orange means a live vein behind it (EH-M3 G4, EH-M4 K2, EFS). Presentation plus inspect; at G4 the cap state pins the cut Cool or Surging. |
| **Keep watch** | `keep_watch` | Waiting in a niche or on a bench advances the player's presentation hour, and with it any zone on the schedule (EI-HT-01). Where the schedule is not built, keep watch is still the authored way to release a quest pin that says "until keep watch" (U3, EMS Working stretch). |
| **Heat follows the room** | — | An authored state change on a quest step (L3 sleep rooms when Serix enters; U8 when the relief turns). It is a pin or a variant swap, never a simulation. |
| **Valve board and tally board** | `tally_board` | Read-in-place props at the Gate Valve House (V1, V2). Their states are by flag (EME10 unbalanced before EH-M6, balanced after). |

---

## 1. Macro layout [PROPOSAL — DIRECTOR; MAP VERIFICATION REQUIRED]

Emberholt is a city on volcanic terraces with a working ward below its civic heart, a district of great forges at that ward's edge, a large system of ducts and old works beneath it, and a ridge outside the walls. The bible's relative route order (§4.2) is kept exactly:

1. **Embergate** is the city's main entrance [CANON] and leads out. No destination, direction or route beyond it is placed. The **Gate Valve House** and the **Bridge of Seven Repairs** sit just inside the gate.
2. **Cinderwall** lies below the civic heart, close enough to the gate that its heat main runs past the valve house. It is beside the Emberfall Dross (unplaced in the dossier; §13 ZQ-3). **Slagside** and the **Dross Scavenger Pits** are on the tips at its edge.
3. The **Cinderweave Quarter** sits between Cinderwall and the Emberhold District. The **Molten Stair** climbs from the quarter toward the civic terraces.
4. The **Emberhold District** holds the **Ash Terraces**, **Speaker's Hall** and the **Covenant Lamp-House**; **Ashspire** is above them.
5. The **Emberforges** lie beside Cinderwall's working edge. The **Old Lower Forge** was part of that edge; the **Half-Name Wall** is on its yard's outer side.
6. **The Underworks** run beneath: the **Cinderwall Undercroft** is entered from Cinderwall; the **Emberdeep Warrens** are reached from deeper junctions; the **Glassed Hollow** lies beneath the old lower forge; the **Ritual Chambers** are in the Warrens.
7. **The Ridge** is outside the walls, reached through a **working gate on Cinderwall's side**. The **Ridge Steadings**, the **Ridge Workings** and the **Molten Scars** lie along the **Ash Roads**; **Elyndra's Vent Shrine**, the **Cold Seam** and **Cinderreach Spire** are further out. Nothing beyond the Ridge is placed.

**Two exits from the play space**, both edge-of-region dressing only: the road out through Embergate, and the Ridge's outer edge. Neither leads anywhere in this content, and neither is a route to another region.

---

## 2. Subzones (bible §4.1)

| Subzone | Band | Ambient | Enemy families present (Enemies file owns placement) | Heat |
|---|---|---|---|---|
| **Embergate and the Gate** | Near the region edge | Gate market, carts, wardens, the hourly tally (EME10) | None in the streets; ECC is investigation only | Cool streets; ESR culvert under the bridge (pinned Working in ESR) |
| **Cinderwall and the Dross** | Hub | Shift bells (EME06), mood banners (EME02), Cooling House life (EME03, EME05, EME07) | Dross Scavengers at the tips and pits; Cinder Rats glimpsed | Hood tells everywhere (presentation); no street damage; the EH-M6 frost variant per player |
| **Cinderweave Quarter and the Molten Stair** | Hub | Dye yards, courtyards, flame-balancing on the stair (EME04), the children's game (EME09) | None in the streets | Cool streets; heat cellar under the academy (M2) |
| **Emberhold District, Ash Terraces, Ashspire** | Civic heart, high | Rehearsals at dusk, braziers, salons above | Cinder Wraiths inside the lamp-house sleep rooms only | Terrace braziers (presentation); L3/L4 heat rooms |
| **The Emberforges** | Industrial edge | Hearths, hammers, guild halls | Forge Saboteurs in EOM (kiln outside) | Hearth-line ambient heat (presentation); no damage on public floors |
| **The Underworks** | Below the ward and beyond | Ducts, junctions, wartime bores, sealed works | Cinder Rats, Slag Beetles, Dross Scavengers, Deepbrand Crews, Cinder Wraiths, Ashfall Revenants, Emberdeep Sentinels | Most heat zones are here (§6.1) |
| **The Ridge** | Outside the walls | Magma larks (EME08), ridge goats, burners' smoke | Emberback Boars, Slag Beetles, Forge Saboteurs, Cinder Wraiths at the tap | Vent stretches on the Ash Roads, the Workings, the tap cut, the shrine pit |

**World pockets** (Enemies §11, [PROPOSAL — Gameplay Designer]): EW-01 Cinder Rats in the Undercroft's upper side ducts (never the junction); EW-02 Slag Beetles in the Workings' upper galleries, on the tips by Slagside, and in the U3 vent gallery after EH-M6 (the §E.9 warden's round; Enemies I-25); EW-03 Emberback Boars in the Scars and on the Ash Roads; EW-04 Dross Scavengers at the pits outside the cache basin (never in Slagside itself); EW-05 an Ashfall revenant on the Hollow's outer glass, only if the Director picks Enemies I-13 option (b). Each pocket needs room for its pair plus a niche or safe ground at its edge.

---

## 3. Traversal route plans

All routes are relative and **MAP VERIFICATION REQUIRED**. "Fallback" is the walking critical path when a vertical or agility move is not built.

| Route | Order | Vertical or agility moves | Fallback |
|---|---|---|---|
| **R-1 Gate to ward** | Embergate → valve house and bridge → Cinderwall arrival lane (W1) | None | — |
| **R-2 Ward to Undercroft** | Cooling House (W2) → stair head and plaque (W3) → stair → stair niche (U1) | The Undercroft stair (ML-01) | A long ramp at grade change, or the Undercroft as a separate flat interior entered by a stair interaction (§5A) |
| **R-3 Undercroft line (EH-M1, EH-M6, warden's round)** | U1 → U2 duct run → U3 vent gallery (short way or long way) → U4 junction door → U5 junction → (EH-M6) warden door → U7 old conduits → U8 bleed house → U9 splice run → U10a cabin / U10 splice junction → U10b far doors | U2 agility ledge (floor fallback in the package); U7 "below the junction" (ML-14); line-hand quest travel offered from the stair head to checkpoints (EH-M6) | U2 floor route; U7 reached by a sloped bore; quest travel always has walking as its fallback |
| **R-4 Ward to the old works (EH-M3)** | Cinderwall → old works approach (G1) → sealed mouth (G2) → tool store (G3) → cut (G4) → glassed fall (G5) or drain (G6) → crew camp (G7) → Hollow outer edge (H1) → crossing (H2) → door arch (H3) → circle (H4) → bypass mouth (H5) → bypass → annex lower stacks door (A1) | G6 crawl and culvert step (sump fallback in the package); H4 one step down; the bypass "comes up" into the annex (ML-07) | Drain at grade; the circle's step as a ramp; the annex reached on a rising tunnel floor; the annex street door already readmits the player in S07 |
| **R-5 Ward to the Warrens (EH-M4)** | Maeryn's shop (C2; EAC alias C4) → Cooling House (W2) → Undercroft → U6 bypass Cinderwall end, miners' gate → K1 shaft head → K2 shaft and landings → shaft foot niche → K3 Warrens' mouth → K4 plate run (K4a, K4b) → K5 sigil gallery (three tiers) → R1 proving ring → R2 chamber; R3 vault above, seen only | **The shaft is a required descent and ascent (ML-09)**; K3 crossbow step (ML-10); K5 tiers (ML-11); R1 gallery (ML-12) | §5A ML-09: content fallback is flat landings joined by a per-flight climb interaction placing the player at the next landing's anchor (the same placement as respawn anchors). Tiers flattened into three successive chambers. Crossbow positions at grade or on ramps |
| **R-6 Quarter to the stair (EH-M2)** | Cinderweave tannery (C1), Maeryn's (C2), Selice's (C3) → Molten Stair practice court (M1) → heat cellar (M2) → ladder and hatch → annex (M3) → Theryn's study (M4) | **Cellar ladder and hatch, required in S05 (ML-03)**; the stair itself (ML-04) | Annex at grade beside the cellar with a door, or the ladder as an interaction-driven climb |
| **R-7 Civic heart (EH-M5)** | Terraces T1 → crowd floor T2 → service yard T3 → Rat's duct → Speaker's Hall letter-room cellar (H1) → Magister's chambers (H2); separately the lamp-house L1 vigil hall → L2 dormitory stair → L3 sleep rooms → L4 record gallery and record room | L2 stair (ML-15); L4 gallery above the record room and the chimney-breast ladder (ML-16, ML-17); duct crawl and optional drop (ML-18); balcony (presentation, ML-19) | §5A |
| **R-8 Ward to the Ridge** | Cinderwall working gate (EOP R1) → Ash Roads → steadings (P1), burners' clamp (P2), Scars path (P3) → Scars edge (M1), blind (M2), wallow bowl (M3); the Workings (EFS R1–R5); the kiln yard (EOM M8–M9); the tap (EAD T1–T3); further out the shrine (EFD E1–E4), the Cold Seam, the Spire | EFD steps and trapdoor (ML-25, ML-26); EOM kiln rim ledge by ramp (optional); EFS runnel (agility, fallback in package); EWQ "short climb" to the vent bath (ML-30) | §5A |
| **R-9 Gate culvert (ESR)** | Bridge deck (R1) → steps down to a ledge under the arch (R2 culvert walk) → gate yard forge (R3) → valve house (R4) | ML-27 steps down | A ramp to the ledge |

**Walk-away and resume.** Every route can be left at any point. The quest stays Active at its persisted step (three states only). Logout and death return the player to the step's named point (§6.6).

---

## 4. POI requirements (EP01–EP28)

Each table states function, relative placement, sub-areas, quest uses, state by flag, required props, traversal and map checks. Area codes are the packages' own (W, U, G, H, A, K, R, C, M, L, T, V, E, F). Area codes are scoped to their quest package where letters repeat (for example R1 is the EH-M4 proving ring, EOP's working gate and ESR's bridge deck).

### 4.0 Canonical area keys and aliases (canonical for implementation; packages keep their own labels)

**Rule.** This file is the canonical label list. The canonical key of an area is `<POI>.<defining quest code>.<label>`, where the defining quest is the first package that authors the place (for example `EP02.ECW.W2`). Zone, respawn and pin data key areas by canonical key, never by a bare label. A package's own label stays valid inside that package as an alias.

**One place, several labels (aliases):**

| Canonical key | Place | Aliases in other packages |
|---|---|---|
| `EP02.ECW.W2` | The Cooling House (warming house in EH-M6) | ECN N8; EFC F1; ESP P1 (its hearth); W2 in Acts II and III |
| `EP02.ECW.W3` | The Undercroft stair head | ESH H5 (with the first duct); W3 in Act III |
| `EP02.EGH.W4` | The Red Door clinic | EAD H2 |
| `EP02.EGA.W4` | The Heat Commons store behind the wash-house | EFC F4; EBL B4 |
| `EP02.EWA.C1` | The wash-house | ECN N1 |
| `EP02.EOP.R1` | The Cinderwall working gate | EAD R1 |
| `EP15.ECW.U1` | The Undercroft stair niche | ESP P3; U1 in Act III |
| `EP15.ECW.U5` | The Cinderwall junction | EWA C6; U5 in Act III |
| `EP26.ECW.V1`–`V3` | The Gate Valve House | ESR R4 |
| `EP03.EEH.C2` | Maeryn Vall's shop | EAC C4 |
| `EP23.ECW.T1` | The rehearsal terrace | T1 in Act II |
| `EP25.ESK.K2` | The apprentice hearth | EOM M2 |
| `EP25.EGA.F2` | The Basalt Forge Guild hall | EOM M10 |
| `EP05.EOP.P1`–`P3` | The Ridge Steadings | EOM M6 (the steadings as one stop) |

**One label, several places (homonyms; always qualify by quest code):** C1–C5 (EEH/EAC Cinderweave; EWA Commons branch); E1 (EGH Marshal's office; EFD shrine terrace); F2 (EGA guild hall; EFC lane); G1–G6 (EGH Darven's Gallery; ECC gate sites); H1–H5 (EGH Hollow; ESS Speaker's Hall H1–H2; EGA H2 Council chamber; EAD H1–H2; ESH H1–H5); K1–K4 (EAC shaft and Warrens; ESK Emberforges); M1–M4 (EEH Molten Stair; EOP Scars M1–M3; EOM M1–M10); P1–P3 (EOP steadings; ESP Cooling House route); R1–R5 (EAC ritual chambers; EOP/EAD gate and road; ESR bridge; EFS Workings); T1–T3 (ECW/ESS terraces; EAD tap); W4 (EGH clinic; EGA Commons store).

### EP01 Embergate [CANON] (Settlement)

| Row | Requirement |
|---|---|
| Function | The main gate and the region's only road out; merchant yards and gate market. |
| Placement | At the city's edge; the valve house (EP26) and the bridge (EP27) just inside. Cinderwall within a short walk. |
| Areas | Gate passage; merchant yards (ECC G2 bonded shed, G5 rope-store yard, EGT yards; crates holding EDS08 and the EDS10 notice); gate market; **E1 Marshal's office** [NEW sub-site] (EH-M3, EH-M5, §E.6); ECC G1 wardens' post, G3 farrier forge, **G4 Commission house upper office**, **G6 counting room by an outside stair**; ESR R3 gate yard forge; Ryl Danner's yard (master commission). |
| Quest uses | EH-M3 S01 (warrant), EH-M5 (intercepts), EH-M6 aftermath; ECC; EGT; ESR; EDS08, EDS10. |
| State by flag | Gate street crowd at V1 in EH-M6 S08 (per player); `EH_RIVERGLASS` barks. |
| Required props | Wardens' post, bonded shed, crates for EDS08/EDS10, Marshal's desk and ledger (inspect after `EH_HOLLOW_TRUTH = kept`). |
| Traversal | ECC G6 outside stair (ML-24, required). G4 "upper office" (ML-23). |
| Map | MAP VERIFICATION REQUIRED. The gate road leads out with no destination dressing beyond a turn out of sight (ED-9). |

### EP02 Cinderwall [CANON ward; NEW detail] (Settlement, hub)

| Row | Requirement |
|---|---|
| Function | The hub: Cooling House, Red Door clinic, terraced tenements, slag lanes, the Undercroft entrance, the working gate to the Ridge. |
| Placement | Below the civic heart; beside the Emberforges' working edge and the Emberfall Dross; its main passes the valve house. |
| Areas | **W1** arrival lane; **W2** Cooling House (board, hood tell, yard small forge, keep-watch bench, hatch to the yard; respawn for EH-M1 and all of EH-M6); **W3** Undercroft stair head (memorial plaque sightline to EP11/EDS09; thaw-lines standing point in EH-M6); **W4** Red Door clinic (EH-M3, EAD H2) and, in EH-M6, **W4 Heat Commons store** behind the wash-house (the label repeats across packages; §14 EZ-9); W5 memorial; EAD H1 Sereth's healing house; Imra's house (ENW) [NEW]; Glassmoth's stall under an arch (EGT); EWA C1 wash-house and C2 hatch; EBL B1 bell post on Bellwright's Lane; ECN N1–N8 (N5 Slagside respawn, N8 court at night); EFC F1–F4; the working gate (EOP R1, EMS). |
| Quest uses | EH-M1, EH-M3 (W4, W5), EH-M4 (W2), EH-M6 (W1–W4, frost variant); EWA, ECN, EFC, EBL, ESP, ESH, EAD, ENW, EGT, EMS; EME02, EME03, EME05, EME06, EME07; EDS03 (backlash yard, if placed here). |
| State by flag | `EGA_FROST` (frost variant W1–W4 and the upper Undercroft, per player, until `S07`); `EH_COMMONS` (cots laid in W2 in EH-M6); `EH_HEAT_MAIN` (§E.1 board lines, hood state); `EH_COLD_WARD` (barks). The hood tell reads Working after EH-M6 (§E.1). |
| Required props | Hood tell over the cook-hearth; keep-watch bench; yard small forge (Smithing); trough; Heat Commons rota slate; mood-banner lines; shift bell on its post (frozen rope in the frost variant). |
| Traversal | W3 stair (ML-01); EWA C2 hatch ladder (ML-20); EBL B2 grate-hatch ladder (ML-21; the Undercroft stair is the package's own alternative). |
| Map | MAP VERIFICATION REQUIRED: W3 thaw-lines sightline (ET-11); W3 must see the plaque or the wall of EP11 (EDS09 approach). |

### EP03 Cinderweave Quarter [CANON; NEW detail] (Settlement)

| Row | Requirement |
|---|---|
| Function | Artisans' quarter: Maeryn's shop and back room, Brisa Teglan's tannery, Selice's workshop, dye yards, courtyard. |
| Placement | Between Cinderwall and the Emberhold District; the Molten Stair rises from it. |
| Areas | C1 tannery; C2/C4 Maeryn's shop (EH-M4 respawn; keep-watch stool from S02); C5 back room (EH-M3 C5.5, EH-M4, ETB); Maeryn's yard C [NEW] with Seredh's lean-to (EST, EMS); C3 Selice's workshop (EH-M2, ETB, EGT); Sabeth's bench (EGT); Cinderweave courtyard (ETB, EME09). |
| Quest uses | EH-M2, EH-M3, EH-M4 (start and end), EST, ETB, EMS, EGT, EWQ; Brisa's commission. |
| State by flag | §E.7 by `EH_THALAN = freed` (D-E2, ruled 2026-11-15): one line (Dahrin). The aided variant (Asera in the third chair) is removed. |
| Required props | Stove, curtain, counter, tuning nails (ETB), keep-watch stool. |
| Traversal | At grade. |
| Map | MAP VERIFICATION REQUIRED. A short walk to Cinderwall's Cooling House (EH-M4 goes shop → Cooling House → Undercroft). |

### EP04 The Molten Stair [CANON] (Micro-settlement)

| Row | Requirement |
|---|---|
| Function | Theryn's academy, practice courts, student lodgings. |
| Placement | Climbing from Cinderweave toward the terraces. |
| Areas | M1 practice court (respawn; EEH Tavi test, morning-pinned; ETB court); **M2 heat cellar** (pinned Working; niche by the ladder); **M3 annex reached by a ladder up to a hatch** (S05 required; EEH-E1 inside); M4 Theryn's study; Idra's lodging [NEW sub-site] (ETB). |
| Quest uses | EH-M2, ETB, EME04. |
| State by flag | `EH_CURRICULUM` (notices, Idra's teachers; also read in EP22 dormitory). |
| Required props | Assessment ledger (`EEH_ledger`) on its shelf; lens rack; lantern row (`stair.row_lit`, `stair.lanterns_dim`). |
| Traversal | **ML-03** cellar ladder and hatch (required). The stair itself (**ML-04**) is a long incline of broad steps: build as a NavMesh slope, never as stepped colliders that block click-to-move. |
| Map | MAP VERIFICATION REQUIRED: the stair rises visibly toward the terraces. Tavi's flare is a hazard volume on a non-targetable NPC with three radius steps; the court must hold the largest radius plus a 2 m ring of walkable ground. |

### EP05 The Ridge Steadings [NEW] (Micro-settlement)

| Row | Requirement |
|---|---|
| Function | Herders and charcoal burners outside the walls. |
| Placement | On the Ash Roads beyond the working gate. |
| Areas | P1 Teodor's steading; P2 burners' clamp; P3 Scars path. |
| Quest uses | EOP (*Old Plate*), EFS; hunting staging. |
| State by flag | `EOP_TRACKED`, `EOP_PLATE` (barks). |
| Required props | Clamp (prop, smoking); pens. |
| Traversal | At grade. |
| Map | MAP VERIFICATION REQUIRED. |

### EP06 Slagside [NEW] (Micro-settlement)

| Row | Requirement |
|---|---|
| Function | Scavenger shanties on the Dross tips. |
| Placement | Cinderwall's edge, on the tips. |
| Areas | ECN N5 (respawn). |
| Quest uses | ECN. |
| Traversal | Tip slopes are walkable slopes, never steps. |
| Map | MAP VERIFICATION REQUIRED. |

### EP07 The Glassed Hollow [CANON] (Ruin/war site)

| Row | Requirement |
|---|---|
| Function | The war site under the old lower forge: outer glass, the circle. |
| Placement | Beneath the old lower forge (EP11); reached through Darven's Gallery (EP10); left by Yorven's bypass tunnel toward the Red-Lit annex. |
| Areas | H1 outer glass edge (patrol tells); H2 crossing (Embermind Echo overlay: ~1.5 s warning, ~8 s, ~25 s cycle; glass vents); H3 door arch (handprint, `hollow.handprint`); **H4 circle, sunk a step below** (frame, niche, bleed valve, pocket pulse ~30 s; Hollow Revenant); H5 bypass tunnel mouth. |
| Quest uses | EH-M3 S05–S06. |
| State by flag | `EGH_POCKET_BLED`; post-quest walkable to the camp (G7) only. No mouth barricade during S06–S07: the bypass and the annex street door serve `S07` (ML-07; playability audit CO-01). |
| Required props | Glass vents (non-walkable hazard with edge stop); the frame; the handprint; the niche ridge. |
| Traversal | **ML-06** H4 step down: build as a ramped lip; no push crosses it (EK-7). |
| Map | MAP VERIFICATION REQUIRED: the circle must sit under the old lower forge (§E.6 relies on it). |

### EP08 The Molten Scars [CANON] (Ruin/war site)

| Row | Requirement |
|---|---|
| Function | Ridges melted into glassy slopes; hunting ground. |
| Placement | On the Ash Roads beyond the steadings. |
| Areas | M1 Scars edge (EDS02); M2 blind; M3 wallow bowl (three wallows; beads cycle; walkable slope and rim). |
| Quest uses | EOP (Old Plate, side miniboss), EDS02. |
| Traversal | Bowl slope and rim walkable; no edge drop. |
| Map | MAP VERIFICATION REQUIRED: bowl size for the Old Plate fight (Enemies file). |

### EP09 The Ash Roads [CANON; placement NEW] (Ruin/war site)

| Row | Requirement |
|---|---|
| Function | Cracked old streets lined with burnt engravings, running out from the walls onto the Ridge. |
| Placement | From the working gate outward; links EP05, EP08, EP14, EP17, EP19 and on to EP20, EP21, EP24. |
| Areas | EDS01 engravings; EAD R2; EMS vent stretch and the Working stretch (pinned Surging until keep watch at the near niche). |
| Quest uses | EDS01, EAD (escort of Myr at a slow walk), EMS (carry-state walk), ECC wardens' quarrel lines. |
| Traversal | At grade; EMS carry-state blocks climb and agility (Integration EI-CA-04), so its whole route must be walkable without either. |
| Map | MAP VERIFICATION REQUIRED: walking time with the EMS carry and the EAD escort (ET-12). |

### EP10 Darven's Gallery [NEW] (Ruin/war site)

| Row | Requirement |
|---|---|
| Function | The collapsed bypass cut where Darven's crew was lost. |
| Placement | From the old works below Cinderwall toward the Hollow. |
| Areas | G1 old works approach (respawn S02–S04); G2 sealed mouth (EGH-E1; **crossbow ledge reached by a short ramp**); G3 tool store (drain grate); G4 cut (flarecap; pinned Cool or Surging by the cap); G5 glassed fall (Option A: cut the fall, 3-segment channel); **G6 drain** (Option B: crawl, two Working heat rooms with vents and niches, agility culvert step with sump fallback, "down the drain grate … then up beyond the fall"); G7 crew camp (respawn S05–S06). |
| Quest uses | EH-M3 S02–S06. |
| State by flag | Post-quest walkable to G7. |
| Traversal | G2 ramp (keep it a ramp; ML-05). G6 down-and-up (ML-05b): build as sloped crawl floors, not drops. |
| Map | MAP VERIFICATION REQUIRED: both options must end on the same side of the fall at G7. |

### EP11 The Old Lower Forge [NEW] (Ruin/war site)

| Row | Requirement |
|---|---|
| Function | Walled yard with the forge-collapse memorial plaque (EDS09). |
| Placement | Cinderwall's working edge, beside the Emberforges; above the Hollow. |
| Areas | Yard; plaque; ENW lower-forge pay list (at the pay-house in EP25). |
| Quest uses | EH-M1 pass-by (W3 plaque line), ENW, EDS09, §E.6. |
| State by flag | `EH_HOLLOW_TRUTH` (chalk over the plaque, §E.6), `EH_HALF_NAME`. |
| Map | MAP VERIFICATION REQUIRED. |

### EP12 The Half-Name Wall [NEW, Part 3] (Ruin/war site)

| Row | Requirement |
|---|---|
| Function | A wall of part-names on the forge yard's outer side. |
| Placement | The outer face of EP11's yard wall. |
| Quest uses | ENW. |
| State by flag | `EH_HALF_NAME` named/held (chalk state). |
| Required props | A decal surface for added chalk. |

### EP13 The Emberdeep Warrens [CANON] (Cave/dungeon)

| Row | Requirement |
|---|---|
| Function | The deep works below the bypass: Deepbrand's landing, the plate run, the sigil gallery. |
| Placement | Reached from deeper junctions by the old mining shaft below Yorven's bypass (U6). |
| Areas | **K1 shaft head** (winch frame, Thennek); **K2 shaft: ladders and three landings** (vents on the second landing ~10 s; flarecap); shaft foot niche (respawn S03–S04; Thalan's hand-off scene, freed, D-E2 ruled 2026-11-15); K3 Warrens' mouth (Deepbrand landing; **crossbow on a raised step reached by three stairs**); K4 plate run with K4a/K4b heat rooms pinned Surging until Asera's three breaths or a keep watch, then Working; **K5 sigil gallery: three stacked tiers with stairs between them**, three doors each, read with `EAC_sigil_stone`. |
| Quest uses | EH-M4 S03–S07; EDS08 (map seed). |
| State by flag | Post-quest: gate and shaft walkable to the mouth; a turn-back bark volume beyond, checked against each player's own EAC state (presentation; never a movement blocker; playability audit CO-01). |
| Traversal | **ML-09 shaft (required both ways); ML-10 crossbow step; ML-11 tiers.** |
| Map | MAP VERIFICATION REQUIRED: depth, heat and every relative position (Act II). |

### EP14 The Ridge Workings [NEW] (Cave/dungeon; the mine)

| Row | Requirement |
|---|---|
| Function | Shallow flarecap and ore galleries; Mining intro. |
| Areas | R1 Workings head; R2 upper gallery; R3 cap gallery (agility runnel with fallback); R4 beetle stope (orange patches pinned Surging); R5 seam face (sump out of reach). |
| Quest uses | EFS. |
| Traversal | "Upper gallery" is a sloped adit at grade; no ladder. |
| Map | MAP VERIFICATION REQUIRED. |

### EP15 The Cinderwall Undercroft [NEW] (Cave/dungeon)

| Row | Requirement |
|---|---|
| Function | Heat-main ducts and junctions below the ward, and (EH-M6) the deep main below them. |
| Placement | Entered from Cinderwall (W3 stair); also reached by the EWA hatch, the EBL relief spur and the ESP/ESH routes; connects to Yorven's bypass (U6) and the shaft (K1). |
| Areas | U1 stair niche (respawn EH-M1 S01–S02, S05–S06); U2 duct run (pinned Working; grates ~10 s; agility ledge with floor fallback); U3 vent gallery (short way pinned Surging until keep watch at the fork niche; long way with Slag Beetles); U4 junction door (broadsheet, ED-14 line; EDS04 chalk if placed here); U5 Cinderwall junction (wheel, slate, manifold of three cocks, stage cock on the down-line, vents ~12 s, two niches); **U6** Yorven's bypass, Cinderwall end, with the miners' gate (EH-M4); **U7** old conduits through a warden door below the junction (war bore; vents ~8 s; two niches; the Rat's grille high in the wall; stage cock B); **U8** bleed house (three relief wheels TERRACES/WARD/FORGES, field forge, two niches, floor vents); **U9** splice run (three splices; collars every forty paces); **U10a** fitter's cabin; **U10** splice junction (~26 m domed arena: plinth one step up, four collars, two niches with seal plates, one vent, eight plate lines, no raised firing spot, leash ~5 s; door niche outside the grille); **U10b** far doors (barred from the far side). EWA C3–C6 Commons branch, dead leg, tee, junction. |
| Quest uses | EH-M1, EH-M4 (U6), EH-M6, EWA, EBL, ESP, ESH, warden's round (§E.9). U3: EW-02 beetles after EH-M6 (world pocket). |
| State by flag | EH-M1 pins (§6.2); `EGA_STAGE` A/B/C (§6.3); `EGA_FROST` (upper Undercroft frost variant); §E.3 post-story (Sentinel inert prop, clamps stacked, far doors chained). |
| Required props | Tells per line; manifold; stage cocks A and B; relief wheels; collars with number plates; junction book; seal plates; draw valve. |
| Traversal | ML-01 stair; ML-14 U7 below the junction; ML-13 U10 plinth (presentation only for the player). Line-hand quest travel (EH-M6) to U1, U5, U7 second niche, U8, U10 door niche, walking as fallback. |
| Map | MAP VERIFICATION REQUIRED: U10 ~26 m, leash geometry, niche-to-collar distances (ET-13). |

### EP16 The Ritual Chambers [CANON] (Cave/dungeon)

| Row | Requirement |
|---|---|
| Function | The proving ring and Thalan's frame. |
| Placement | In the Warrens beyond the sigil gallery. |
| Areas | **R1 proving ring**: sunken; eight sectors; **raised gallery with stair and crossbow**; edge niche respawn S05–S07. **R2 chamber**: frame (~40 s cycle), fitter's hearth and anvil (`EAC_FRAME_WORK`). **R3 vault above, seen and never reached**; emberlight moves along its rim (`warrens.emberlight`). |
| Quest uses | EH-M4 S05–S07 (Thalan freed; D-E2, ruled 2026-11-15). |
| Traversal | ML-12 ring gallery; the ring's sunken floor is reached by ramps, never by a drop. R3 is a presentation volume only. |
| Map | MAP VERIFICATION REQUIRED: R3 visible from R2 or R1. |

### EP17 The Saboteurs' Kiln [NEW] (Camp/bandit site)

| Row | Requirement |
|---|---|
| Function | An abandoned charcoal kiln used as a hideout. |
| Areas | EOM M8 kiln yard (rim ledge on the kiln shoulder for throwers, reached by optional ramps); M9 kiln mouth (Saboteur Captain). |
| Quest uses | EOM. |
| Traversal | Rim ledge by ramp, never by stairs (ML-29); throwers on it must be reachable by melee along the ramp. |
| Map | MAP VERIFICATION REQUIRED. |

### EP18 The Dross Scavenger Pits [NEW on CANON group] (Camp/bandit site)

| Row | Requirement |
|---|---|
| Function | Scavengers' working pits on the tips. |
| Areas | ECN N6 pits with slag pools; **N7 cache basin with two slag ledges reached by ramps**. |
| Quest uses | ECN. |
| Traversal | Slag pools are non-walkable hazards with edge stops; ledges by ramp (ML-28). |

### EP19 The Embervein Tap [NEW place on CANON anchor] (Camp/bandit site)

| Row | Requirement |
|---|---|
| Function | Dalia Vret's camp at an exposed vein. |
| Areas | EAD T1 Dalia's camp; T2 tap cut (vents pinned Working, zone pinned Surging in `S04`); T3 vein lip. |
| Quest uses | EAD. |
| Traversal | T3 lip has an edge blocker. |

### EP20 Elyndra's Vent Shrine [CANON] (Shrine)

| Row | Requirement |
|---|---|
| Function | Offerings at a vent that never cools. Where **Elyndra the Cinderseer** lives in near-isolation [CANON, character file §37; D-EL, ruled 2026-11-15]; the pilgrims' story of the flame stays belief. |
| Areas | E1 shrine terrace; **E2 steps down to the lower terrace and the railed pit** (pinned Surging during the dusk vigil song); **E3 trapdoor to a cellar and a stooped crawl** (Working); E4 throat. |
| Quest uses | EFD (Elyndra's first meeting, at E1's far edge after the vigil, `EFD-D2.15`–`.18`), EDS05; EH-M5 (ESS) consult with Elyndra here (D-EL role item 2; the act file owns its staging); EH-M6 (EGA) one optional aftermath bark here after `EH_STANDING` (`EGA-B9.13`, Act III §E.12). |
| NPCs | Ivett Quarle (keeper); pilgrims; Elyndra, seldom present on E1 and non-targetable. Where she sleeps is not placed and adds no area (no geography change; MAP VERIFICATION REQUIRED). |
| Traversal | ML-25 steps; ML-26 trapdoor. Flares hover no higher than ~2 m above the pit lip (Enemies I-19). |
| Map | MAP VERIFICATION REQUIRED: from beyond the upper terrace's front edge there is **no line of sight into the pit**, so no attack point there goes unanswered (Enemies I-23). |

### EP21 The Cold Seam [NEW, Part 3] (Shrine)

| Row | Requirement |
|---|---|
| Function | A fissure where no heat rises; quiet grief. |
| Areas | Fissure edge; cold stones; EMS beat D. |
| Quest uses | EDS07, EMS. |
| Traversal | Edge blockers along the fissure. |
| Map | MAP VERIFICATION REQUIRED: far enough out that the EMS walk has weight, near enough to stay walkable with a carry (ET-12). |

### EP22 The Covenant Lamp-House [NEW place on CANON practice] (Shrine)

| Row | Requirement |
|---|---|
| Function | Vigil hall above; the Hearthveil sleep rooms below an old dormitory. |
| Placement | Emberhold District. |
| Areas | L1 vigil hall (access book on a chained lectern; custody shelf for EMS); **L2 old dormitory stair** (notice by `EH_CURRICULUM`); L3 sleep rooms a/b/c (three braziers; vigil cistern with ewer; niche; ESS-E1 Cinder Wraiths; heat follows the room); **L4 record gallery with a rail above the record room**; chimney breast with the damper latch; **iron ladder up the breast beside a wall vent (~10 s)**; record desk in the room below. |
| Quest uses | EH-M5 S04; EMS (custody shelf); EGT (vigil hall). |
| State by flag | `ESS_DAMPER` shot/climbed; L4 Surging until the damper, then Working. |
| Traversal | ML-15 stair; ML-16 gallery above the room; ML-17 ladder. |
| Map | MAP VERIFICATION REQUIRED: the latch at ~12 paces from the gallery rail (Option A). |

### EP23 The Ash Terraces [CANON] (Unique landmark)

| Row | Requirement |
|---|---|
| Function | Civic terraces where the High Kindling is rehearsed. |
| Areas | T1 (EH-M1 order trail; EH-M5); T2 crowd floor (three brazier rows; **Speaker's balcony above, out of reach**); T3 service yard with the vent grille and the Rat's duct mouth. |
| Quest uses | EH-M1, EH-M5 (dusk pins S01, S05), §E.4. |
| State by flag | `EH_HEAT_MAIN = terraces` (two brazier rows roped off), `EH_SPEAKER` crowd breath (D-S1, ruled 2026-11-15; player outcome unchanged). |
| Traversal | Terraces are broad level platforms joined by ramps or wide NavMesh-sloped steps; ML-19 balcony is presentation only. |
| Map | MAP VERIFICATION REQUIRED: visible from the W3 stair head for §E variant "terraces" (or omit, Act III). |

### EP24 Cinderreach Spire [CANON] (Unique landmark)

| Row | Requirement |
|---|---|
| Function | Landmark on the far Ridge with a weathered waymark. |
| Quest uses | EDS06 only. |
| Traversal | The sign stands on the spire path at grade; the spire is not climbed. |
| Map | MAP VERIFICATION REQUIRED: visible from the Ash Roads. |

### EP25 The Emberforges [CANON] (Unique landmark)

| Row | Requirement |
|---|---|
| Function | The great forges and guild halls. |
| Areas | ESK K1–K3; **ESK K4 hearth-line gallery, an iron walkway with gratework over the great hearths, reached by a stair from the yard (wonder beat)**; F2 Basalt Forge Guild hall [NEW sub-site] (EH-M6 `guilds` reading); **ENW forge pay-house [NEW sub-site] with high shelves and a rolling ladder**; EOM M1–M7; Durnan's anvil (master commissions). |
| Quest uses | ESK, EOM, ENW, EH-M6 S08, §E.5, §E.10. |
| State by flag | `EH_HEAT_MAIN = forges`, `EH_ACCOUNT`, `EH_GUILDS` (§E.5). |
| Traversal | ML-22 K4 gallery (presentation fallback: the wonder beat plays from the yard floor); ML-31 rolling ladder (presentation: the record is read at the pay-house table). |
| Map | MAP VERIFICATION REQUIRED: beside Cinderwall's working edge. |

### EP26 The Gate Valve House [NEW] (Unique landmark)

| Row | Requirement |
|---|---|
| Function | The city's valve book and tally board. |
| Areas | V1 public hall and tally board (EME10); V2 book room; V3 clerks' bench (Aubin Harl); ESR R4. |
| Quest uses | EH-M1 S07, EH-M6 S08 (full hall), ESR, EME10. |
| State by flag | EME10 unbalanced/balanced; §E.2 by `EH_ACCOUNT`. |
| Traversal | At grade. The hall must hold the §9.3 crowd without blocking the board's 2 m pad. |

### EP27 The Bridge of Seven Repairs [NEW, Part 3] (Unique landmark)

| Row | Requirement |
|---|---|
| Function | A bridge with seven layers of repair. |
| Areas | ESR R1 deck; **R2 culvert walk: steps down to a ledge under the arch** (pinned Working, two niches). |
| Quest uses | ESR. |
| Traversal | ML-27. |
| Map | MAP VERIFICATION REQUIRED: what the bridge crosses is not stated; the culvert implies a channel or cut (§13 ZQ-4). |

### EP28 Speaker's Hall [CANON] (Unique landmark)

| Row | Requirement |
|---|---|
| Function | The Speaker's seat; the Council's chamber. |
| Areas | H1 letter-room (cellar; duct-post tube; letter-case); H2 Magister's chambers (EH-M5); **H2 Council chamber** [NEW sub-site] (EH-M6 `council` reading; the label H2 repeats across packages); service yard. |
| Quest uses | EH-M5 S03, EH-M6 S08, §E.8. |
| Traversal | H1 is reached from the Rat's duct (ML-18); the letter-room itself is at the duct's grade. |
| Map | MAP VERIFICATION REQUIRED: the duct from T3 must reach H1 without passing a public floor. |

---

## 5. New places invented by the packages [NEW] (not counted as POIs)

| Place | Parent | Package | Note |
|---|---|---|---|
| Red Door clinic (W4) | EP02 | EH-M3, EAD | — |
| Marshal's office (E1) | EP01 | EH-M3, EH-M5, §E.6 | — |
| Maeryn's back room (C5) and yard C | EP03 | EH-M3, EH-M4, EST, ETB, EMS | Seredh's lean-to in the yard |
| **Red-Lit annex (A1–A4)** | **Unplaced `[C14.2]`** | EH-M3 S07 | Reached from below by Yorven's bypass into its lower stacks; has a street door. Must sit where both are possible (ET-03). |
| U6 bypass Cinderwall end and miners' gate | EP15 | EH-M4 | — |
| K1–K5 shaft, mouth, plate run, sigil gallery | EP13 | EH-M4 | — |
| U7 old conduits; U8–U10b deep main | EP15 | EH-M6 | — |
| W4 Heat Commons store | EP02 | EH-M6, EFC | — |
| H2 Council chamber | EP28 | EH-M6 | — |
| F2 Basalt Forge Guild hall; forge pay-house | EP25 | EH-M6; ENW | — |
| Idra's lodging | EP04 | ETB | — |
| Imra's house; Sereth's healing house | EP02 | ENW; EAD | — |
| Commission house, counting room, bonded shed, rope-store yard, wardens' post | EP01 | ECC | — |
| Wash-house and Commons branch (C1–C6) | EP02 / EP15 | EWA | — |
| Bell post, Bellwright's Lane; relief spur | EP02 / EP15 | EBL | — |
| Dalia's camp | EP19 | EAD | — |
| Hollow areas H1–H5 | EP07 | EH-M3 | — |

---

## 5A. Multi-level dependency register (every step that assumes vertical navigation)

**Why this section exists.** The Mire playability audit found that the Chapel's vertical traversal was a hard dependency with no fallback, and that NPC ladder traversal, stacked floors and off-mesh links are not demonstrated in Sol's build. Emberholt leans on vertical space far more than the Mire. Every row below is a dependency on Sol until multi-level NavMesh, stairs, ladders or off-mesh links exist. "Required" means a required step cannot complete without it. "Fallback" is a ground-level or flattened layout that keeps the authored beat; where none exists, the row says so.

| Id | Where (POI, area) | Quest and step | What it assumes | Required? | Ground-level or flattened fallback |
|---|---|---|---|---|---|
| **ML-01** | EP02 W3 → EP15 U1, Undercroft stair | EH-M1 S01 onward; EH-M3 (Cooling House respawn routes); EH-M4 S02; EH-M6 S02; EWA, EBL, ESP, ESH; §E.9 | A stair from the ward down into a space beneath it (stacked over the ward) | **Required** | (a) A long ramped descent so the Undercroft lies beside and below the ward rather than under walkable streets; or (b) the Undercroft as a separate flat interior entered by a stair interaction (a transition). Both keep every beat. |
| **ML-02** | EP15 U2 agility ledge | EH-M1 S01 | Agility | No | Floor route (package). |
| **ML-03** | EP04 M2 → M3 ladder and hatch (also EP04 "below" the annex) | **EH-M2 S05** | A ladder up through a hatch from the heat cellar into the annex above | **Required** | Annex at grade beside the cellar, reached by a door from the cellar; or the ladder as an interaction-driven climb. The cellar stays pinned Working with its niche by the door. |
| **ML-04** | EP04 Molten Stair | EH-M2; ETB; EME04 | A long climbing stair | Required route | NavMesh slope of broad shallow steps. |
| **ML-05** | EP10 G2 crossbow ledge by a short ramp | EH-M3 S02 (EGH-E1) | A raised enemy position | Enemy position | Already a ramp; keep the ramp walkable for melee players (CDR-2). |
| **ML-05b** | EP10 G6 drain, "down the drain grate … then up beyond the fall" | EH-M3 S03 Option B | A descent and climb | Optional (Option A cuts the fall) | Sloped crawl floors at grade; Option A stays available. |
| **ML-06** | EP07 H4 circle "sunk a step below" | EH-M3 S06 (Hollow Revenant) | A step change inside an arena | Required arena | Ramped lip all round; no push crosses it. |
| **ML-07** | Bypass H5 → Red-Lit annex A1 ("comes up" into the lower stacks) `[C14.2]` | EH-M3 S06–S07 | The annex stacked above the bypass | **Required** | The bypass rises on a sloped floor to the lower stacks door at grade; the annex street door (S07) already gives a second way in and out. |
| **ML-08** | EP15 U3 short way / long way | EH-M1 S01 | Two routes at one level | No | — |
| **ML-09** | EP13 K1–K2 shaft, "ladders and three landings" | **EH-M4 S03 (down) and S07 (up)**; post-quest access | Repeated ladder descents and ascents; NPCs (Thennek first down, Asera up) also on the ladders | **Required, both ways** | **Content fallback for Sol (added in review, 2026-11-15; no geography or story change):** the head, the three landings and the foot are each authored as a small flat walkable floor, and each ladder is a standard "Climb down" / "Climb up" interaction whose completion places the player at the next floor's anchor. This reuses the placement-to-a-named-anchor that respawn already needs (EI-QS-06; the shaft foot is already a respawn anchor), but current source places the player only on death, so it adds **one small action effect**: a generic "place at anchor" interaction effect reusing host-validated respawn placement (playability audit TD-04). The second-landing vent and flarecap stay on their landing floor. Other options for Sol: off-mesh ladder links; or a zone transition at the head and the foot (the landings become a short presentation). NPC ladder traversal is not demonstrated: Thennek and Asera fade and reappear at the next landing or at the foot (presentation). Thalan never climbs: freed (D-E2, ruled 2026-11-15; the only outcome), he leaves by Thennek's side cut at the shaft foot. |
| **ML-10** | EP13 K3 "crossbow on a raised step reached by three stairs" | EH-M4 S03 | A raised enemy position | Enemy position | Three-stair step becomes a ramp, or (no build needed) the crossbow stands at grade at the step's foot behind the landing brazier, which already gives cover both ways; telegraphs unchanged. A melee player must be able to reach it (§14 EZ-7). |
| **ML-11** | EP13 K5 sigil gallery, three stacked tiers with stairs between | **EH-M4 S04** | Stacked tiers | **Required** | Flatten into three successive chambers in a line, each with three doors; the stone reading is unchanged. Thalan's `freed` escort (S07) then walks back through flat chambers. |
| **ML-12** | EP16 R1 raised gallery with stair and crossbow | EH-M4 S05–S06 | A raised enemy position over a sunken ring | Enemy position | Gallery reached by a ramp, or the crossbow position at the ring rim at grade. The sunken ring is entered by ramps. |
| **ML-13** | EP15 U10 plinth one step up | EH-M6 S06 | The Sentinel's plinth | Presentation | Ramped plinth edge; no shove crosses it. |
| **ML-14** | EP15 U7 "through a warden door below the junction"; deep main U8–U10 | **EH-M6 S02–S06** | A space beneath U5 | **Required** | A sloped bore descending from the warden door at grade; or the deep main as its own flat interior entered at the warden door (quest travel already uses checkpoints). |
| **ML-15** | EP22 L2 old dormitory stair | **EH-M5 S04** | A stair down from the vigil hall to the sleep rooms | **Required** | A ramp or a stair interaction transition into a flat lower interior. |
| **ML-16** | EP22 L4 gallery with a rail above the record room | **EH-M5 S04** | Stacked gallery over a room; Option A shoots the latch from above; Option B goes down into the room | **Required** | Gallery and record room at the same grade, separated by a low rail with a gap or short ramp; the gallery side is a raised dais on a ramp. The latch remains ~12 paces from the rail and **shootable from the record-room floor as well**, so the Ranged option never depends on the gallery. |
| **ML-17** | EP22 L4 iron ladder up the chimney breast | EH-M5 S04 Option B | A climb to the latch | Optional (Option A exists; but Option B is the non-ranged path and so **required for a melee-only player**) | Ladder as an interaction-driven climb that places the player on a small landing at the latch (the ML-09 pattern; the same one small "place at anchor" action effect, TD-04), channel at the top; or a ramp-and-landing beside the breast. **Content fallback if neither is built (added in review, 2026-11-15; no geography or story change):** the latch is pulled from the floor at the ladder foot with the record room's fire hook, an ordinary flue fitting: the same 2-segment channel, run only between exhales, taking two vent cycles, with the pad at the ladder-foot niche; `ESS_DAMPER` keeps the value `climbed` (no new flag). Option A and this fallback both work from the one floor level, so neither melee nor ranged depends on the ladder (CDR-2). |
| **ML-18** | EP23 T3 → EP28 H1 Rat's duct (crawl height then walk height; optional agility drop with side-crawl fallback) | EH-M5 S03 | Crawl, then a drop into the letter-room cellar | Required route | Side crawl (package); the duct ends at the cellar's grade. |
| **ML-19** | EP23 Speaker's balcony above the crowd | EH-M5, §E.4 | An NPC on a balcony | Presentation | Out of reach by design; no player use. |
| **ML-20** | EP02 EWA C2 hatch with a ladder down (niche at its foot) | EWA S02 | A ladder into the Commons branch | **Required** | A sloped access passage from the wash-house to the branch, or an interaction-driven ladder. |
| **ML-21** | EP02 EBL B2 relief spur, ladder from a grate hatch | EBL | A ladder | No | The Undercroft stair (package's own alternative). |
| **ML-22** | EP25 ESK K4 hearth-line gallery, iron walkway over the hearths by a stair from the yard | ESK (wonder beat) | An elevated walkway | Presentation beat | The beat plays from the yard floor with the hearths in view; or a ramped walkway. |
| **ML-23** | EP01 ECC G4 Commission house "upper office" | ECC | An upper floor | Check | If a required interaction is in the upper office: move it to the ground floor or use a stair interaction. |
| **ML-24** | EP01 ECC G6 counting room by an outside stair | **ECC (required)** | An external stair to an upper room | **Required** | Counting room at grade off the yard; or the outside stair as an interaction-driven climb. |
| **ML-25** | EP20 EFD E2 steps down to the lower terrace and railed pit | EFD | Stepped terraces | Required | NavMesh-sloped steps or a ramp. |
| **ML-26** | EP20 EFD E3 trapdoor → cellar → stooped crawl | EFD | A trapdoor descent | Required | A sloped passage from the terrace; or an interaction transition into a flat cellar. |
| **ML-27** | EP27 ESR R2 steps down to a ledge under the arch | ESR | Steps | Required | A ramp to the ledge with an edge blocker. |
| **ML-28** | EP18 ECN N7 two slag ledges by ramps | ECN | Ramps | Optional | Already ramps. |
| **ML-29** | EP17 EOM M8 kiln-shoulder rim ledge by optional ramps | EOM | Ramps; throwers on the ledge | Enemy position | Already ramps; melee must reach the throwers. |
| **ML-30** | EP03/Ridge EWQ Q4 vent bath reached by a "short climb" from the range | EWQ | A climb | Check | A short ramp. |
| **ML-31** | EP25 ENW forge pay-house, high shelves and a rolling ladder | ENW | A climb | Presentation | The pay list is read at the table (an NPC brings it down). |
| **ML-32** | ESH H4 soot loft reached by a ladder | **ESH (required)**; pinned Working with a water-bucket safe volume | A ladder to a loft | **Required** | Loft at grade as a back room of the workshop, or an interaction-driven ladder. |
| **ML-33** | ESH H5 Undercroft stair and first duct with NPC follow (Lenk) | ESH S04 | NPC follow on the stair | Required | ML-01 fallback; Lenk waits at the stair foot if NPC stair traversal is not ready. |
| **ML-34** | EP02/EP18 ECN-E1 slinger on a roof reached by a ladder (Enemies §12) | ECN | A raised enemy position | Enemy position | Ramp to the roof edge, or the slinger at grade behind cover. |
| **ML-35** | EP15 U4 EGA-E1 slinger on the sack, four steps up (Enemies §12) | EH-M6 S02 | A raised enemy position | Enemy position | NavMesh slope or ramp. |
| **ML-36** | EP01 ECC-E1 slinger on a coil stack, two steps; covers the outside stair (Enemies §12) | ECC | A raised enemy position | Enemy position | Ramp; if ML-24 is flattened, the slinger covers the yard instead. |
| **ML-37** | EP02 EBL bell post: the stay is fitted at the headstock from the post's ladder | **EBL S04 (both options)** | A ladder climb to the headstock | **Required** | Fit the stay as a standing interaction at the post's foot (the same 2-segment fit and time cost); or an interaction-driven climb placing the player at a named anchor at the headstock (the ML-09 pattern). Added from playability audit ES-05. |

**Summary.** 38 rows (ML-01 to ML-37 plus ML-05b). **Fourteen required rows that assume a ladder, stair or stacked space:** ML-01, ML-03, ML-07, ML-09, ML-11, ML-14, ML-15, ML-16, ML-17 (for a melee-only player), ML-20, ML-24, ML-26, ML-32, ML-37 (added from playability audit ES-05). Every one now has a fallback: ML-09 and ML-17 gained content fallbacks in review (flat landings with a per-flight climb interaction; the damper pulled from the floor), the others a flattened layout. Required routes that need only a slope or ramp: ML-04, ML-06, ML-18, ML-25, ML-27, ML-33. Enemy positions that must stay melee-reachable: ML-05, ML-10, ML-12, ML-29, ML-34, ML-35, ML-36. **General fallback for every raised enemy position (no build needed):** if neither a ramp nor a stair is built, the raised spot stays dressing and the enemy stands at grade at its foot with the cover the package already places there, so melee and ranged are both viable from one floor level and telegraphs are unchanged. Presentation only: ML-13, ML-19, ML-22, ML-31. **Recommended fallback order (playability audit TD-03):** scene and zone transitions are not demonstrated either (the build is one scene with connected hub paths), so on every required row the slope or flattened variant is the recommended fallback, since it needs only NavMesh slopes, which exist: ML-01a, ML-03, ML-07, ML-11, ML-14 bore, ML-15 ramp, ML-16, ML-20, ML-24, ML-26 sloped passage, ML-32. Build once with Mire MI-AG-02. Sol's choice of form (§10.3 Q1) stands.

---

## 6. Zone-state tables (per player)

### 6.1 Heat-zone register

**Canonical for implementation; quest packages defer to this register** (EK-1). Each heat zone has an id, a default state used whenever no quest pins it, and the pins the packages apply. **The default column is the whole schedule if EI-HT-01 is never built**, and it is also the post-story state (§13 EZ-6). Pins are step-scoped: a pin releases at the end of its step, and quest completion releases every pin of that quest. Defaults are [PROPOSAL — DIRECTOR] for the Gameplay Designer to tune.

| Id | Zone | Default (no pin) | Quest pins (per player) | Niches | Map |
|---|---|---|---|---|---|
| HZ-01 | U2 duct run | Working | EH-M1 S01 Working; EH-M6 stage A Surging until cock A, then Working; ESH S04 Working | Stair niche U1; one mid-run | MAP VERIFICATION REQUIRED |
| HZ-02 | U3 vent gallery, short way | Working | EH-M1 S01 Surging until keep watch at the fork niche, then Working | Fork niche | — |
| HZ-03 | U3 long way | Cool | — | — | — |
| HZ-04 | U5 Cinderwall junction | Working | EH-M1 Cool until S06, Surging during S06, Working after; EH-M6 Surging until stage cock A, Working after | Two | Niche-to-cock distance short (pad rule) |
| HZ-05 | U7 old conduits | Working | EH-M6 Surging until stage cock B | Two | — |
| HZ-06 | U8 bleed house | Working | EH-M6 Surging until the relief turns, then Working | Two | — |
| HZ-07 | U9 splice run | Working | EH-M6 Surging until the relief is held, then Working | Per package | Forty-pace collar spacing |
| HZ-08 | U10 splice junction | Working | EH-M6 P1 and P3 Working, P2 Surging | Two (sealed in P2 on a cycle) | ~26 m dome |
| HZ-09 | G4 the cut | Cool | EH-M3 S02 Cool or Surging by the flarecap | — | — |
| HZ-10 | G6 drain heat rooms ×2 | Working | EH-M3 S03 Working | One each | — |
| HZ-11 | H2 Hollow crossing glass vents | Working | EH-M3 S05 Echo overlay (presentation hazard per Enemies file) | Per package | — |
| HZ-12 | K2 shaft second landing | Working (vents) | — | Shaft foot niche | — |
| HZ-13 | K4a, K4b plate run heat rooms | Working | EH-M4 S03 Surging until Asera's breaths or a keep watch; Working after and on the way out | One each | — |
| HZ-14 | R2 chamber (frame cycle) | Working | EH-M4 per package | Ring edge niche | — |
| HZ-15 | M2 academy heat cellar | Working | EH-M2 S05 Working | By the ladder (or door, ML-03) | — |
| HZ-16 | L3 sleep rooms | Cool | EH-M5 S04: heat follows the room when Serix enters; brazier-driven until all three are doused | Cistern niche | — |
| HZ-17 | L4 record room | Working | EH-M5 S04 Surging until the damper is shut | At the ladder foot | — |
| HZ-18 | Rat's duct / T3 grille | Cool | EH-M5 per package | — | — |
| HZ-19 | EWA Commons branch (house leg / cistern leg) | Working / Cool | EWA S03 house leg Working, cistern leg Cool | At C2 foot | — |
| HZ-20 | EFD E2 pit / E3 crawl | Working | EFD S02 pit Surging for the dusk vigil song; crawl Working | — | — |
| HZ-21 | ESR R2 culvert walk | Working | ESR pinned Working | Two | — |
| HZ-22 | ESH H4 soot loft | Working | ESH S03 Working (water-bucket safe volume) | Bucket | — |
| HZ-23 | Ash Roads Working stretch (EMS) | Working | EMS Surging until keep watch one turn at the near niche | Near niche | ET-12 |
| HZ-24 | EAD T2 tap cut | Working | EAD S04 zone Surging, vents Working | Per package | — |
| HZ-25 | EFS R4 beetle stope | Working | EFS S02 orange patches Surging | Per package | — |
| HZ-26 | EOP M3 wallow bowl | Cool (beads cycle presentation) | — | — | — |

Ward streets, Cinderweave, the terraces' public floors, the Emberforges' public floors and the valve house are **not heat zones**: their tells and braziers are presentation only.

### 6.2 EH-M1 junction pins (Act I)

U5 is Cool until `S06`, Surging during `S06`, Working after. U2 is pinned Working for the step. U3's short way is Surging until the player keeps watch at the fork niche. All three release at the end of their steps; after EH-M1 Completed, U2 to U5 show their §6.1 defaults.

### 6.3 EH-M6 staged pressure (EI-PR-01, environment-variant form)

| `EGA_STAGE` | Zones Surging | Zones Working | Swap trigger |
|---|---|---|---|
| (before S02) | — | §6.1 defaults; frost variant upper Undercroft | `EGA_FROST` |
| A | U5 (and U2–U4 route as pinned) | U1 | Enter U1 in S02 |
| B | U7 | U2–U5 (cock A bled) | Stage cock A bled |
| C | U8, U9 | U2–U7 (cock B bled) | Enter U8 |
| relief turned | U9 | U8 | `EH_HEAT_MAIN` set |
| relief held | — | U8, U9 | `EGA_BLEED_WORK` set |
| fight | U10 P2 | U10 P1, P3 | Sentinel phase |

A player may pass a stage without bleeding it; the zone stays Surging, and the relief cannot be turned until both cocks are bled (Act III). The frost variant ends for the player after `cinderwall.thaw_lines` in S07.

### 6.4 By region flag (post-story)

| Flag | Places | Change |
|---|---|---|
| `EH_TELLS` | All tells | Inspect text |
| `EH_HEAT_MAIN` | EP02 (§E.1), EP23 (§E.4), EP25 (§E.5), U8 slate | Props, boards, barks; the hood tell stays Working |
| `EH_ACCOUNT` | EP26 (§E.2), EP28 H2, EP25 F2 | Board copy, readings |
| `EH_HOLLOW_TRUTH` | EP11 plaque, EP01 Marshal's ledger (§E.6) | Chalk, ledger line |
| `EH_THALAN` = freed (D-E2, ruled 2026-11-15; one value) | EP03 (§E.7) | One line (Dahrin); Asera's chair variant removed |
| `EH_SPEAKER` (D-S1, ruled 2026-11-15) | EP23 crowd breath | Bark set |
| `EH_GUILDS` | EP25 Durnan | Barks |
| `EH_COMMONS` | EP02 W2 cots in EH-M6 | Props |
| `EH_HALF_NAME` | EP12, EP11 | Chalk |
| `EH_STANDING` | Master commission givers; Veska's round offer at W3 | Offers |
| `EGA` completion | EP15 §E.3 | Sentinel inert prop; clamps stacked; far doors chained |

### 6.5 Quest-local place states

EH-M3 gallery walkable to G7 after (no mouth barricade during S06–S07; CO-01); EH-M4 turn-back bark volume beyond the Warrens' mouth after, checked against each player's own EAC state (presentation; never a movement blocker; playability audit CO-01); EEH lantern row (`stair.row_lit`, `stair.lanterns_dim`); ESS braziers out (`ESS_BRAZIERS_OUT`) and damper (`ESS_DAMPER`); ECC pins on the board (`ECC_PINS`). Discoveries (EDS01–EDS10) set `EDS##_SEEN` on inspect and need no pin; their props stay in their default state for every player (Mire lesson SS-20).

### 6.6 Respawn and logout points by step (from the packages)

| Quest | Respawn (death) | Logout restore |
|---|---|---|
| EH-M1 | Cooling House W2; U1 stair niche for S01–S02 and S05–S06 | By step (Act I list) |
| EH-M2 | M1 practice court during S01, S03, S05–S07; Cooling House W2 otherwise (S00, S02, S04) (Act I §B7) | By step (Act I list) |
| EH-M3 | W2 for S00, S01, S08; G1 for S02–S04; G7 for S05–S06; A1 for S07, then W2 | By step (Act I list) |
| EH-M4 | Maeryn's shop C4; shaft foot niche S03–S04; ring edge niche S05–S07 until `EAC-D9.42`; Thalan (freed, the only outcome) rejoins at the respawn point only before `EAC-D9.42`. **After `EAC-D9.42`** (Thalan has gone by the side cut): the shaft foot niche, with no Thalan | By step; a logout during the walk out resumes at the ring edge niche before `EAC-D9.42`, and at the shaft foot niche with no Thalan after it |
| EH-M5 | By step (Act II list) | By step |
| EH-M6 | **W2 warming house for every step** | To the checkpoint (U1, U5, U7 second niche, U8, U10 door niche) |
| Side quests | Named safe points per package | Dropped carry-state returns to its source |

Each respawn point is a niche or safe room, at grade with its area, and outside any Surging zone at every stage.

---

## 7. Time, weather and phasing rules

1. **Presentation hour** (reused from Lowmark) drives heat schedules (EI-HT-01, when built), waits and hour-pinned scenes. There is no world clock.
2. **Hour pins (per player):** EH-M2 Tavi test morning; EH-M5 S01 and S05 dusk; EH-M6 dusk until S01, night S02 to the S06 keep watch, dawn S07, morning S08; EFD vigil at dusk (re-offered each dusk); ECN N8 at dusk (Commons ECN `S05_court`); ETB Asera at dusk; rehearsals at dusk (§E.4). **Scope (playability audit ES-01, ES-06):** the EGA pin governs only EGA steps and the frost-variant areas (item 3); a side step placed there is held while `EGA_FROST` is set and resumes at `EGA_THAW_SEEN`; keep watch anywhere else advances the player's hour normally. Any other quest's pin applies only to keep watch inside that quest's own step volume. EDI-3 stays open.
3. **Weather:** none, except the EH-M6 **frost variant** of Cinderwall W1–W4 and the upper Undercroft (an environment variant per player, keyed to `EGA_FROST`, ended by the thaw-lines event). "The frost does not come back this season" is presentation (§E.1).
4. **Phasing:** heat zones, stages, pins and epilogue props are per player (§0.1). Two players in the same zone may see different states. Shared presentation is a fallback only (Integration EI-CO-06).
5. **Waiting** is always available in a niche until the next state.

---

## 8. Relative placement, sightlines and exclusions

### 8.1 Must-see

| Sightline | From | To | Fallback |
|---|---|---|---|
| Plaque approach (EDS09) | W3 stair head | EP11 wall | Plaque visible on arrival at W3 |
| **Thaw lines** (EH-M6 S07) | W3 stair head at dawn | The ward's lanes and roofs | **Ground fallback (canonical for implementation):** the event plays at grade at the W3 stair head, framed down the nearest lanes, where the lines run at street level; roofs in view are a bonus, never required. Act III's "Cooling House roof" fallback is not used, because a roof is ML-class (§14 EZ-5). |
| Terraces in frost (§E variant `terraces`) | W3 | EP23 | Omit (Act III) |
| Forge roofs bare of frost (`forges`) | W3 or the ward | EP25 | Omit |
| R3 vault rim emberlight | R2 or R1 | R3 | Required presentation; keep R3 in view |
| Speaker's balcony | T2 crowd floor | Balcony | — |
| The stair rising | Cinderweave | EP04 toward EP23 | — |
| Cinderreach Spire | Ash Roads | EP24 | — |

### 8.2 Must-not

- No sightline or dressing that implies a destination beyond Embergate or the Ridge, and no road sign naming another region.
- The Red-Lit annex is never visible from the bypass before S07 (it is a reveal).
- R3 (the vault) is never reachable.
- U10b far doors never open; nothing is visible behind them.
- No Volkhari refuge, settlement or community form is located anywhere (ED-12); Thennek's side cut leads out of view and is never followed.
- No stealth cover, detection cones or hiding spots are built; none is needed (ED-6).
- No enemy in a Cooling House, warming house, clinic, shop, academy court or civic hall (Enemies §11).
- No arena has a fall, ledge drop, open shaft or deep water a player can be moved into (Enemies §1).

---

## 9. Terrain early-check register

Lowmark's provisional terrain broke beats that depended on adjacency, access to raised floors and walking times (Lowmark TC-01, TC-12, TC-18). **No Emberholt terrain exists**, and the terrain generator in `CODE/Scripts/terrain_generation/` is an offline Lowmark-only authoring prototype; it is not a runtime terrain generator and has no Emberholt mode. Emberholt can still name its geometry dependencies before any terrain pass. Each row below is a beat that depends on distance, height, heat or adjacency. The terrain pass should check these first and surface mismatches to the Director rather than relocate anything. Severity: **Blocks** / **Degrades** / **Cosmetic**.

| Id | Dependency | Beats that rely on it | If wrong | Severity |
|---|---|---|---|---|
| **ET-01** | The heat main runs from Cinderwall **past the valve house**; the EH-M1 order trail goes U5 → V1–V3 → T1 in one evening | EH-M1 S06–S07; EH-M6 S08 | The trail reads as unrelated errands | Degrades |
| **ET-02** | The Undercroft lies **under or beside and below** Cinderwall, with its stair at W3 and secondary access from the wash-house hatch (EWA), a grate hatch (EBL) and ESP/ESH routes all landing on the same duct network | EH-M1, EH-M6, EWA, EBL, ESP, ESH | Side quests contradict the main line's geography | **Blocks** |
| **ET-03** | The Hollow lies **beneath the old lower forge**; Darven's Gallery reaches it from the old works; Yorven's bypass leaves the Hollow and **rises** to the Red-Lit annex, which also has a **street door** `[C14.2]` | EH-M3 S05–S07; §E.6 | The annex cannot be placed; S07 has no exit | **Blocks** |
| **ET-04** | The miners' gate at U6 opens on the shaft head; the shaft is deep enough for three landings; the Warrens lie beyond the foot | EH-M4 S03, S07 | Descent beat lost | **Blocks** |
| **ET-05** | The Rat's duct runs from the terrace service yard (T3) to Speaker's Hall cellar (H1) without crossing a public floor | EH-M5 S03 | Letter-room approach exposed | **Blocks** |
| **ET-06** | The Molten Stair climbs from Cinderweave toward the terraces; the academy's heat cellar sits under or beside the annex (ML-03) | EH-M2 S05 | Theft beat loses its route | Degrades |
| **ET-07** | The **working gate** on Cinderwall's side opens onto the Ash Roads; steadings, workings, Scars, kiln and tap lie along them; shrine, Cold Seam and Spire further out | EOP, EFS, EOM, EAD, EMS, EFD, EDS01–EDS07 | Ridge pacing | Degrades |
| **ET-08** | The valve house and the bridge sit **just inside** Embergate; the bridge has a culvert with a ledge under its arch | ESR; EH-M1 S07; EH-M6 S08 | ESR R2 has no place | Degrades |
| **ET-09** | The Emberforges are beside Cinderwall's working edge; the old lower forge was part of it; the Half-Name Wall is the yard's outer face | ENW, ESK, EOM, EH-M6 S08 | Memorial geography wrong | Degrades |
| **ET-10** | Slagside and the scavenger pits are on the Dross tips at Cinderwall's edge | ECN | — | Degrades |
| **ET-11** | **Thaw-lines sightline**: from one standing point at W3 at dawn, the ward's lanes and roofs are visible | EH-M6 S07 | Event moves (§8.1) | Degrades |
| **ET-12** | Walking times: Thalan's slow escort from R2 to the shaft foot; Myr's slow escort on the Ash Road (EAD); the EMS carry to the Cold Seam with no sprint | EH-M4 S07; EAD; EMS | Tedium or a rushed beat | Degrades |
| **ET-13** | U10: ~26 m dome; four collars on the wall; two niches; one vent; eight plate lines; no raised firing spot; leash ~5 s | EH-M6 S06 | Boss telegraphs and leash fail | **Blocks** |
| **ET-14** | Ash Terraces crowd floor: three brazier rows; a balcony above; room for the rehearsal crowd and the player at the front | EH-M5 S01, S05 | Rehearsal beats crowded | Degrades |
| **ET-15** | K5 three doors per tier (or per chamber, ML-11); R1 ring of eight sectors with an edge niche | EH-M4 S04–S06 | Reading and fight layout fail | **Blocks** |
| **ET-16** | M3 wallow bowl: walkable slope and rim; three wallows | EOP | Old Plate fight | Degrades |
| **ET-17** | The play space ends at Embergate's road and at the Ridge's outer edge, with no implied route beyond | All | Canon breach (ED-9) | **Blocks** |
| **ET-18** | L4 latch ~12 paces from the gallery rail and visible from the record-room floor (ML-16) | EH-M5 S04 | Ranged option breaks | **Blocks** |

---

## 10. Architecture needs for Sol

**Status of the tools** (from their documentation). The **architectural generator** (v0.16.0, `CODE/Scripts/architectural_generator/`) is an offline Blender add-on that makes editable, metre-scale building **exteriors**. It has twenty building types: Farmhouse, Cottage, Townhouse, Longhouse, Barn, Grain Store, Stable, Miller, Inn, Merchant House, Shop, Warehouse, Market Hall, Smithy, Workshop, Assembly Hall, Watchtower, Gatehouse, Barracks and Boathouse. It supports orthogonal RECT, L, T and U footprints only, 6–24 m wide, 4–16 m deep and 1–3 floors. Function-first programs exist only for Smithy, Market Hall, Stable and Gatehouse. It offers four Emberholt contexts: **Emberhold, Emberforges, Cinderweave and Ashspire**. There is **no Cinderwall context**. It does not create arbitrary polygons, interiors, enterable room layouts or a settlement; a floor-separated visual preview exists for verification only. Its Emberholt world language (`WORLD_ARCHITECTURAL_LANGUAGES.md`) is a reversible art-direction interpretation, not canon. It describes terraces, towers, stacks, elevated metalwalks with visible supports and landing points, and sealed below-grade works shown as discontinuities and blocked routes. Collision proxies are approximate, and the README says traversal still needs review in the target engine. Final art acceptance belongs to the Creative Director.

The **Unity import pipeline** (`UNITY/ARCHITECTURE_PIPELINE.md`) is an offline Editor import of a generator GLB and its `.caelmor.json` sidecar for later hand placement. It creates no settlement, no occupancy areas, no navigation links and no automatic floor hiding, and it does not bake a world NavMesh. Collision proxies become static non-convex MeshColliders whose traversal limits remain. Transparent and emissive materials are rejected on import.

The **terrain generator** is an offline Lowmark-only prototype (§9). `MEDIA/Materials/README.md` describes a painting library of grayscale masters; it is art-direction interpretation and confers no resources, recipes, trade routes or canon.

**This section is a set of requests for Sol and the Director to accept, change or reject. It is not a prescription.** It names no material, texture, colour, palette or finish. Visual style belongs to the Creative Director. "The Emberholt grammar" below means whatever the generator's Emberholt grammar and named context produce, and nothing more.

### 10.1 Mapping to existing building types

| Emberholt building (POI / area) | Nearest existing type | Context | Note |
|---|---|---|---|
| Cooling House (EP02 W2) | Assembly Hall or Inn | **None fits** (EA-11) | Interior is hand-authored (hearth, benches, board, hatch to the yard). |
| Cinderwall terraced tenements; Imra's house; Sereth's healing house; Red Door clinic | Townhouse; Cottage | EA-11 | Red Door needs a usable ground-floor room. |
| Old lower forge yard (EP11) | Smithy (functional program), **ruined, walled** | Emberforges | Ruined state is a gap (EA-6). |
| Gate Valve House (EP26) | Assembly Hall | Emberhold | Public hall, book room and clerks' bench are a hand-authored interior (EA-2). |
| Embergate (EP01) | Gatehouse (functional program) | Emberhold | The gate passage is the region's exit; the generator's gate passage feature fits. |
| Merchant yards, bonded shed, rope store (EP01) | Warehouse; Market Hall | Emberhold | — |
| Marshal's office (E1); wardens' post (ECC G1) | Barracks; Watchtower | Emberhold | — |
| Commission house with upper office and an outside-stair counting room (ECC G4, G6) | Merchant House; Warehouse | Emberhold | External stair traversal is a gap (EA-3). |
| Farrier forge (ECC G3); gate yard forge (ESR R3) | Smithy | Emberhold | — |
| Maeryn's shop and back room (EP03) | Shop | Cinderweave | Back room and yard are hand-authored. |
| Brisa's tannery; Selice's workshop; Sabeth's bench | Workshop | Cinderweave | — |
| Molten Stair academy, lodgings, study (EP04) | Assembly Hall; Townhouse | Cinderweave or Emberhold (question 3) | Heat cellar and annex are interiors (EA-2, ML-03). |
| Covenant Lamp-House (EP22) | Assembly Hall | Emberhold | Below-grade sleep rooms and the record gallery are hand-authored (EA-1, EA-2). |
| Speaker's Hall (EP28) | Assembly Hall | Emberhold | Monumental civic massing likely exceeds 24 × 16 m (EA-4); cellar letter-room, chambers and Council chamber are interiors. |
| Ashspire salons | Merchant House | Ashspire | Presentation only. |
| Emberforges halls, guild hall F2, pay-house (EP25) | Smithy; Workshop; Assembly Hall; Warehouse | Emberforges | Great hearths and furnace halls exceed type limits (EA-9). |
| Ridge steadings (EP05) | Farmhouse; Cottage; Barn | Emberforges or Cinderweave (question 3) | Burners' clamp is a prop. |
| Slagside shanties (EP06) | Cottage (smallest) or none | EA-11 | Shanties may be props or a kit (EA-8). |
| Glassmoth's stall | Shop or prop | — | — |

### 10.2 Gaps, stated as requests

| Id | Gap | What the content needs | Request |
|---|---|---|---|
| **EA-1** | **The Underworks** | Ducts, junctions, the vent gallery, the war bore, the bleed house, the splice run, the ~26 m domed splice junction, the shaft, the plate run, the sigil gallery, the ring and chamber, the Hollow, Darven's Gallery, the Workings, the shrine cellar and crawl, the culvert. None is a building type. | Hand-authored kits, Sol's call. The world language's "sealed below-grade works" note fits the far doors and the gallery's sealed mouth. |
| **EA-2** | **Interiors** | Required-step interiors: Cooling House, valve house (V1–V3), lamp-house (L1–L4), academy (M2–M4), Red-Lit annex (A1–A4), Speaker's Hall (H1, H2), Maeryn's shop and back room, fitter's cabin, Commission house, pay-house, Red Door clinic. | Hand-authored interiors on generated shells, or an extension of the floor-separated preview; Sol's call. Priority: valve house, Cooling House, lamp-house, academy, annex (required steps). |
| **EA-3** | **Vertical access** | Every row in §5A. The pipeline creates no navigation links and the generator's collision proxies are untested for traversal. | Ask Sol which of three forms is cheapest per row: multi-level NavMesh with stairs and ramps; interaction-driven ladder moves; or a zone transition into a flat interior. Content accepts any of them. |
| **EA-4** | **Terraces and monumental civic platforms** | Ash Terraces (three brazier rows, crowd floor, balcony, service yard); the terraced city itself. Footprint limits are 24 × 16 m. | Terrain and hand work; the world language describes terraces as stepped platforms and retaining masses, which fits. |
| **EA-5** | **Heat-works fittings** | Tells, hoods, manifolds, cocks, relief wheels, collars with plates, seal plates, the draw valve, vents and grates, troughs and casks, tally board, valve book. | Props, not buildings; listed so nobody expects them from the generator. |
| **EA-6** | **Ruins and sealed works** | Old lower forge (walled yard, plaque), Half-Name Wall, the Hollow's glass, Darven's sealed mouth, Ash Roads engravings, the backlash yard (EDS03). | A ruined or walled state for Smithy would cover one; the rest is terrain and prop work. |
| **EA-7** | **The Bridge of Seven Repairs** | A bridge with visible layers of repair and a culvert walk under its arch. | No bridge type; hand-authored, or terrain plus kit. |
| **EA-8** | **Kilns, clamps, shanties, camps** | Saboteurs' Kiln (shoulder ledge and mouth), burners' clamp, Slagside, Dalia's camp, scavenger pits. | Kit or prop work. |
| **EA-9** | **Great forges** | The Emberforges' great hearths and the hearth-line gallery (ML-22). Process-tall halls exceed 3 floors and the footprint limits. | Ask Sol whether several generated volumes combined by hand suffice, or whether the great forges are hand-authored landmarks. The world language says Emberforges "cluster towers, stacks, furnace halls, yards, and elevated circulation"; whether any elevated circulation from the generator is walkable is a question (question 2). |
| **EA-10** | **Tells, glows and the vault rim light** | Every heat tell, the flarecap, the emberlight on R3's rim, the Hollow's glass. The import pipeline rejects transparent and emissive materials. | These must be separate presentation objects authored in Unity, not properties of imported generator surfaces. Request only; the look belongs to the Creative Director. |
| **EA-11** | **No Cinderwall context** | Cinderwall is the hub and the most-built ward, but the generator has no Cinderwall context. | Ask Sol and the Director: use Emberforges or Cinderweave for Cinderwall, or add a context. Content has no preference. |

### 10.3 Questions for Sol

1. For each §5A row marked Required: which traversal form (multi-level NavMesh, interaction ladder, zone transition) do you prefer, and can the EH-M4 shaft (ML-09) be done at all in the milestone?
2. Are the Emberholt world language's elevated metalwalks generated as walkable geometry with collision, or are they visual only? (ESK K4 depends on the answer.)
3. Which context should Cinderwall, the Molten Stair and the Ridge steadings use (EA-11)?
4. Can a hazard volume's periodic damage be excluded from channel interruption, or can a heat tick pause a channel segment instead of cancelling it? Until answered, every channel pad in heat stands in a safe volume (§0.1), which needs nothing new.
5. Can an environment variant (the EH-M6 frost and pressure stages) be applied per player without per-player walkability changes? (Emberholt's stages change damage, not walkability.)

---

## 11. Integration dependencies (documented only; nothing implemented)

Runtime needs are registered once in `Quests/Caelmor_Emberholt_Integration_Requirements.md`. The zone-owned ones:

| Need | Owner | Minimum viable form | Integration id |
|---|---|---|---|
| Heat-zone register (§6.1) as per-player state with defaults | SE + ZN | Three-state table per zone; quest pins override; the default column is the fallback schedule and the post-story state | EI-HT-01, EI-HT-02 |
| Staged pressure (§6.3) | SE + ART | Environment variants by `EGA_STAGE` | EI-PR-01 |
| Frost variant | SE + ART | Environment variant by `EGA_FROST` | EI-WV-01 |
| Vertical access (§5A) | SE | Per row, Sol's choice | EI-AG-02 |
| Edge stops and no-push-across-levels | SE + ZN | Edge volumes with a bark; push validation | EI-AG-03 |
| Channels in heat | SE | Heat ticks do not interrupt, or channel pads in safe volumes | EI-CA-03 |
| Respawn and logout points by step | SE + SCE | Data per step (§6.6) | EI-QS-06, EI-QS-07 |

---

## 12. Phase 1.5 count check

| Category (Phase 1.5 §3) | POIs | Count |
|---|---|---|
| Settlements | EP01, EP02, EP03 | 3 |
| Micro-settlements | EP04, EP05, EP06 | 3 |
| Ruins / war sites | EP07, EP08, EP09, EP10, EP11, EP12 | 6 |
| Caves / dungeons | EP13, EP14, EP15, EP16 | 4 |
| Camps / bandit sites | EP17, EP18, EP19 | 3 |
| Shrines | EP20, EP21, EP22 | 3 |
| Unique landmarks | EP23, EP24, EP25, EP26, EP27, EP28 | 6 |
| **Total** | | **28** (range 24–32) |

Hunting is staged in the Molten Scars and around the steadings (no separate hunting POI); the Ridge Workings are the mine. New places in §5 are sub-spaces and are not counted.

---

## 13. Open map questions for the Director

1. **ZQ-1 Red-Lit annex `[C14.2]`.** It must sit where Yorven's bypass can rise into its lower stacks from the Hollow side and where it has a street door. Recommend: under the edge of the Emberhold District nearest Cinderwall. MAP VERIFICATION REQUIRED.
2. **ZQ-2 Heat-zone defaults (§6.1).** Approve the default column so heat works whether or not EI-HT-01 is built, and so the post-story Undercroft (§E.3) has a state after every pin is released.
3. **ZQ-3 The Emberfall Dross.** The dossier names it without placing it. Recommend: the tips at Cinderwall's edge away from the gate, holding Slagside and the scavenger pits.
4. **ZQ-4 What the Bridge of Seven Repairs crosses.** No package says. Recommend: a dry cut or a run-off channel inside the gate (ESR R2's culvert needs one). No river is implied.
5. **ZQ-5 The EH-M4 shaft (ML-09).** If Sol cannot provide any ladder form in the milestone, including the per-flight climb interaction fallback (§5A), should the shaft become a steep spiral ramp (a layout change inside the package's intent), or should EH-M4 wait?

---

## 14. Inconsistencies found and recommended canonical values

**Shared canonical register (canonical for implementation; quest packages defer to this register).** Zones and Integration state these rows in the same words. The Enemies file governs every combat value; each row cites the Enemies C-id or issue it restates (crosswalk), and where a row adds a placement rule it says "Zones adds". Where a quest package gives a different number, the package value is superseded for implementation; the package text changes only when its author next edits it.

| Id | Value | Canonical statement |
|---|---|---|
| EK-1 | Heat states (Enemies C-3) | Three states per zone: **Cool** (no damage), **Working** (light periodic damage outside niches, about a third of Surging), **Surging** (heavy periodic damage outside niches, tuned so a ~4 s crossing costs ~10–15% max HP; walkable, never a wall). Values pending GD. Keyed to the presentation hour where EI-HT-01 is built; otherwise the Zones §6.1 default column. Quest pins override for the pinning player and are step-scoped. A cooling niche stops the damage and waiting in a niche always turns a zone. No meter, no stamina, no stealth, no cold or frost damage. |
| EK-2 | Tells (Enemies §3, §8.1) | A tell shows its zone's state and is readable from outside the zone; every red tell also crazes, so state never rests on hue alone. Inspect text gated on `EH_TELLS`. |
| EK-3 | Vent breath (Enemies §8.1) | Ash lifts **1.5 s** before every exhale; the exhale deals damage and one step of knock-back over the grate only. Cycles: ~10 s (U2, K2, L4, ESH duct), ~12 s (U5), ~8 s (U7). |
| EK-4 | Pressure plates (Enemies I-21, I-22) | Primed (visible), vent ~0.6 s after the step, spent ~8 s, re-priming ~2 s (Act II). Compliant with C-1 because the primed state is shown before the step. No displacement ends on a primed plate. |
| EK-5 | Defeat and re-form (Enemies C-4, C-13) | Every enemy defeated at 0 HP (CDR-1) with the ordinary defeat presentation. Resonance forms re-form only on their site's trigger while their condition lasts, up to their cap; constructs never re-form. **No SX entry; the quest on-defeat hook is not used by Emberholt.** The Draw Sentinel is destroyed and stays an inert prop. Combat never reveals evidence and no quest item drops. |
| EK-6 | Hazard floor (Enemies C-2; authored tuning requirement, pending GD) | No single hazard event (heat tick, exhale, plate, patch, scald, burst, seam) takes a player from above **25% max HP** to 0. Below 25%, staying in a Surging zone can defeat a player. Zones adds a placement rule: on every required route, cooling niches are spaced so that a full-health player walking between them does not fall below 25% from heat alone. |
| EK-7 | Displacement (Enemies C-1, C-2, C-6; pending GD) | Any displacement (push, pull, knock-back, knockdown, stagger) telegraphs at least **1.5 s**. No displacement ends inside a slag pool, on a primed plate or off an edge; it stops at the edge. Zones adds: **no displacement crosses a level change** (step, ledge, stair, pit rim, plinth, ring edge) or ends in a Surging zone away from a niche. No falls exist. |
| EK-8 | Ranged and reach (Enemies C-7, §12) | First-class in every fight, never required (CDR-2). Every raised enemy stands on something a player can walk to; hovering flares stay within ~2 m of their lip; every attack point is answered; out-ranging never ends a condition fight. U10 has no raised firing spot (leash ~5 s). Zones adds: where that walkable access is a stair or ladder, it depends on Zones §5A, and in today's flat build it must be a ramp or an at-grade position (ML-05, ML-10, ML-12, ML-29, ML-34 to ML-36). Every Ranged option has a non-ranged alternative (the ESS damper's Option B, subject to ML-17). |
| EK-9 | Pins | Step-scoped; released at step end; quest completion releases all of that quest's pins; unpinned zones show the Zones §6.1 default. Logout restores pins by the persisted step. |
| EK-10 | Channels in heat | A channel in a heat zone keeps progress (Lowmark channel convention). Pending Sol: heat ticks do not interrupt it, or its pad stands in a safe volume. |
| EK-11 | Set-piece cap and solo (Enemies C-10, C-12) | No more than 5 hostiles standing at once in any set piece. Every encounter is solo-clearable as authored; co-op scales health up from the solo baseline; credit only through a partner's own active step. |

**Inconsistencies (no package was edited; resolutions recorded 2026-11-15):**

| Id | Finding | Recommendation |
|---|---|---|
| EZ-1 | Bible §6.1 brief puts the EH-M5 damper in S05; Act II moved it to S04 (recorded deviation B14.2). | **Resolved 2026-11-15:** bible §6.1 aligned to Act II (damper inside S04; S05 the second rehearsal). |
| EZ-2 | The Red-Lit annex is unplaced (C14.2) yet Act I needs it reached from below by the bypass and from a street door. | ZQ-1. |
| EZ-3 | Cinderwall has no generator context. | EA-11. |
| EZ-4 | Act I place tables mark MAP VERIFICATION REQUIRED and use relative order; consistent with the bible. Note only. | — |
| EZ-5 | Act III's thaw-lines fallback ("the Cooling House roof") introduces a roof, which is itself a vertical dependency. | **Resolved for implementation (§8.1):** the ground fallback plays at grade at the W3 stair head, framed down the nearest lanes. Act III's W3 row to change at its next edit. |
| EZ-6 | Act III §E.3 says post-story heat runs on EI-HT-01 "or quest-pinned Working where the schedule is not built". After completion no pin exists (EK-9). | Use the §6.1 default column as the post-story state; same meaning, no orphan pin. Applied in Act III / Enemies §12, 2026-11-15. |
| EZ-7 | Raised enemy positions reached only by stairs or a ladder (K3, R1 gallery, the ECN-E1 roof, the EGA-E1 sack, the ECC-E1 coil stack) cannot be reached by a melee player in today's flat navigation, which breaks CDR-2's intent in reverse. The Enemies file (§12) counts a stair or ladder as walkable reach; that is true only once Zones §5A is built. | Ramps or at-grade positions (ML-10, ML-12, ML-34 to ML-36). Applied in Act III / Enemies §12, 2026-11-15 (Enemies now counts a stair or ladder as melee reach only once §5A builds it; the EAC-E3 warden-frame follows a target onto the rim or gallery). |
| EZ-8 | The ESS damper's non-ranged path (Option B) is a ladder. Without any ladder form, a melee-only player has no way to finish EH-M5 S04. | **Fallback added (ML-17):** the latch pulled from the floor with the fire hook, same channel and time cost. A ladder form or a ramp-and-landing remains the preferred build. |
| EZ-9 | Area labels repeat across packages (W4 Red Door clinic in Act I, W4 Heat Commons store in Act III; H2 Magister's chambers in Act II, H2 Council chamber in Act III; R1 in three packages). | **Resolved:** §4.0 is the canonical label list with aliases and homonyms; zone data keys areas by canonical key. |
| EZ-10 | The bible §9.4 hedges on the sigil-stone ("a carry-state object … if the budget is 4"); Act II makes it the fourth item, and Act III counts five of five. | Consistent at five; note only. |

---

## 15. Review log

| Pass | Result |
|---|---|
| **Authoring (2026-11-15)** | Written against the bible, Acts I–III and the four side-quest files as reviewed on 2026-11-14 and 2026-11-15, the Mire Zones file (format) and the Mire playability audit (lessons). Every EP id, area code, heat pin, respawn point and multi-level step was taken from the packages; no package was edited. Sol's tool status was taken from the tools' own documentation. No material, colour or finish is named. |
| **Aligned with the Enemies file (2026-11-15)** | The Enemies file landed while this file was being finished and was read the same day. Changes here: §14 EK-1 to EK-11 now restate Enemies C-2, C-3, C-4, C-6, C-7, C-10, C-12, C-13 and I-19, I-21, I-22 with a crosswalk (C-2's wording replaces this file's earlier hazard-floor recommendation; heat values from C-3 added; EK-11 added for the 5-hostile cap). §5A gained ML-34 to ML-36 (raised enemy positions from Enemies §12). EP20 gained the flare hover height (I-19) and the front-edge sightline (I-23). §2 lists the world pockets EW-01 to EW-05; §8.2 gained two exclusions. **Still to watch:** Enemies Q1 (the unplaced Ashfall revenant): option (b) would add a conditioned pocket on the Hollow's outer glass (EP07). The Enemies file treats stairs and ladders as walkable reach (§12); Zones EZ-7 records that this holds only once Zones §5A is built. |
| **Batch 4 zones/integration review, 2026-11-15** | Independent review against the bible, Acts I–III, the four side-quest files, CDR-1 to CDR-6 (§3.7), the engineering handoff and Sol's tool documentation (read-only; nothing in Sol's environment was changed). **Fixed:** the R-6 route and EP04 cited ML-04 for the cellar ladder (it is ML-03; ML-04 is the stair); §0.1 misdescribed the Flood Kitchen (the loft stairs are unfinished and the crates have flat access markers; nothing was "replaced"); §0.1 stated interaction ladders as fact (now a proposal, Sol's call); a blank line split the §5A table; the §5A summary miscounted (37 rows; 13 required rows that assume a ladder, stair or stacked space; 6 slope-only routes). **Fallbacks added for Sol (no geography or story change):** ML-09 shaft as flat landings joined by a per-flight climb interaction using the respawn-anchor placement; ML-17 damper pulled from the floor with the fire hook (same channel and time cost, `ESS_DAMPER = climbed`); a general at-grade fallback for every raised enemy position; ML-10 crossbow at the step's foot behind the brazier; the thaw lines played at grade at W3 (§8.1, EZ-5), so no roof is needed; channels in heat on niche-touching pads, with exclusion or pause-not-cancel as options for Sol (§0.1, §10.3 Q4). **Canonical labels:** new §4.0 lists canonical area keys, aliases and homonyms (EZ-9 resolved). EZ-1 resolved (bible aligned to Act II). **Verified unchanged:** relative placement and MAP VERIFICATION REQUIRED throughout; no interregional route; no material, texture or colour prescribed (colour words quote package tell and flarecap wording for readability); Sol's tools described as their READMEs state. **Left for the Director:** ZQ-1 to ZQ-5 (EDI-1, EDI-2, EDI-4) stay questions. **Encounter-review alignment (same day):** EZ-6 and EZ-7 marked applied (Act III post-story heat uses the §6.1 defaults; Enemies §12 counts stairs and ladders as reach only once §5A builds them; the EAC-E3 warden-frame follows onto the rim or gallery); EW-02 extended to U3 after EH-M6. **Needed outside this file:** Act III W3 row (thaw-lines roof fallback). |
| **Emberholt character rulings, 2026-11-15** | D-E2: every `EH_THALAN` reader now carries `freed` only (EP03 §E.7 aided chair removed; EP13 hand-off, EP16, ML-09, flag table, respawn table de-tagged). D-S1: EP23 and the flag table de-tagged; outcome unchanged. ED-3: `[INITIATE]` header entry replaced by Iven Calder. D-EL: EP20 `[CANON myth]` → `[CANON]`; Function, Quest uses and a new NPCs row record Elyndra living there and met in EFD; no area, traversal or map change. |
| Independent review of character rulings, 2026-11-15 | EP20 Quest uses: Elyndra's EH-M6 aftermath bark (`EGA-B9.13`, Act III §E.12) added; it was staged at EP20 but missing from the row. |
| Playability audit fixes, 2026-11-15 | Playability audit fixes, 2026-11-15: EM-01, EM-02 (respawn table), EM-12, ES-01, ES-03 (EMS carry note), ES-05 (ML-37 added), ES-06, ES-07, CO-01, TD-03, TD-04. |
