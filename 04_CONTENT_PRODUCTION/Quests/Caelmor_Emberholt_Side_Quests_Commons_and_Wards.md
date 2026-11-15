# Emberholt Side Quests: Commons and Wards

**Status (2026-11-15):** Authored production content for Creative Director milestone review (Emberholt bible §12, Batch 3). Five side quests from `Caelmor_Emberholt_Narrative_Production_Bible.md` §7.1 and §7.2: the **Heat Commons** questline, **EWA** *The Water That Did Not Arrive* (1/3), **ECN** *The Case That Never Reached the Court* (2/3) and **EFC** *First Cooling* (3/3); and two standalones, **EBL** *The Ward That Answers Its Own Bell* and **ESR** *The Seven Repairs*. Everything here is **[NEW]** unless marked **[CANON]** or **[APPROVED — id]**. Choices the content depends on that rest on an open bible §3 recommendation are marked **[PROPOSAL — DIRECTOR]**. Markdown only: no schema, production JSON or C#. Dialogue sits inline in each package (§x.13), as in `Caelmor_Mire_Side_Quests_Work_and_Skills.md`, in the node format `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`, with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>` and inspect texts `<CODE>-I<n>`. Voice follows bible §5.3.

**Binding rulings:** `Caelmor_Director_Rulings_Combat_Ranged_Release.md`: CDR-1 (every enemy defeated at 0 HP; no yield, retreat, break-off or scatter; Emberholt registers no SX exception), CDR-2 (ranged first-class in every fight, required in none), CDR-3 (Emberholt is an internal production milestone of the complete game), CDR-4 (standard RPG systems before bespoke simulation), CDR-6 (every step, encounter and reward completable solo; co-op is optional assistance; partner credit only when the partner's own active step consumes it; personal choices and flags independent).

**Sources used:** the Emberholt bible (binding: §1.1, §2.1, §2.3, §3 ED-1, ED-11, ED-13, §3.1, §4.2, §5, §7.1–7.3, §9, §10, §11); `Caelmor_Emberholt_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and their dialogue files (places, the warden's rules, Veska's slate, the Cooling House board, the surge bell, the Heat Commons store and `EGA-D2.30`, the Dross Scavenger kit EGA-E1); the Emberholt dossier (`LORE/Regions/Caelmor_Region4_EmberholtHeights.md`); the Part 4 character ledger (Emberholt rows; the civic-repair-credit handoff rule); `00_ADMIN/Reference/Caelmor_Part3_Emberholt_Proposal.md` (only as far as ED-13 adopts it); Thornfell *Ash in the Snow* (`TAS_ACCOUNT`); the Revelation Ledger.

**Scope guard.** Nothing here grows scope or adds a system. Every technical need is listed in each package's integration section and in the file-level summary for the Emberholt integration handoff (bible §12, Batch 4). **No Emberholt terrain exists:** every placement is relative and marked **MAP VERIFICATION REQUIRED** where geometry, distance or heat matters. No route or direction to another region is stated or implied.

**Not in this file.** The Unburnt series and the Names quests (EST, ETB, EMS, ENW, EGT) are authored in `Caelmor_Emberholt_Side_Quests_Unburnt_and_Names.md`. This file uses none of their cast as quest-givers, sets none of their flags and does not touch the Half-Name Wall, the memorial plaque's names, Maeryn's shop or Volkhari testimony.

---

## 0. Purpose and shared rules

Emberholt's main line teaches the player that the city's heat follows influence. These five quests show the other side of the same habit: what a working ward does for itself when the heat is shared out by people who live under it. The **Heat Commons** questline follows one ward's arrangement for wash water, warmth and repair (bible §1.2: social infrastructure, not a resource system) from a pipe nobody put back, through a complaint nobody heard, to the night the ward feeds itself and names its dead. **EBL** is a small Cinderwall mystery with a mechanical answer. **ESR** is a gate-side bridge that has been kept by more hands than its plaque admits.

Every quest is built on the city's readable system (bible §1.1): tells (clear, amber, red and crazed), vent breath, cooling niches, heat follows the room, and the warden's rules taught in EH-M1 ("Read the tell, not the talk"; "You don't shut hot"; "Never touch a red"). The player repairs, cuts, digs, cooks, sets iron and reads marks; talk carries the people, the work carries the quest.

### 0.1 Unlock gates and placement

| Code | Quest | Series / type (bible §7) | Core verb (primary first) | Unlock (quest state) | Skill hook (CDR-4) | Where (bible §4.2) | Length |
|---|---|---|---|---|---|---|---|
| **EWA** | The Water That Did Not Arrive | Heat Commons 1/3; Settlement | **trace**, repair, share | EH-M1 Completed (`emberholt.main.01_cold_ward`) | **Leatherworking ~[GD: low]**: cut and form a float-valve cup; alternative: keep watch until morning for the crew's spare | Cinderwall (EP02): the wash-house, the Cooling House; the Commons branch off the Cinderwall Undercroft (EP15) | 30–40 min |
| **ECN** | The Case That Never Reached the Court | Heat Commons 2/3; Combat challenge | **track**, recover, return | EWA Completed | **Mining ~[GD: low]**: break the cache out of the slag crust; alternative: Slagside diggers dig it overnight for a share | Cinderwall; the Cinderwatch post; Slagside (EP06); the Dross Scavenger Pits (EP18) | 35–45 min |
| **EFC** | First Cooling | Heat Commons 3/3; Festival | **cook**, carry, celebrate | ECN Completed **and** EH-M2 Completed (`emberholt.main.02_ember_in_every_hand`) | **Cooking ~[GD: low]**: the Commons pot; alternative: work Hennet's hatch through a turn | Cinderwall: the Cooling House, its lane, the Commons store | 25–35 min |
| **EBL** | The Ward That Answers Its Own Bell | Settlement (Cinderwall) | **listen**, read, mend | EH-M1 Completed | **Woodcutting ~[GD: low]** (reclaimed crate-wood only, ED-11): shape a new bell stay; alternative: keep watch until morning for a line hand's | Cinderwall: the bell post, Bellwright's Lane; a relief spur off the Undercroft upper line | 25–35 min |
| **ESR** | The Seven Repairs | Environmental | **read**, repair, credit | EH-M1 Completed | **Smithing ~[GD: low–mid]**: forge and set a parapet cramp; alternative: keep watch until morning and hold the level for the Hall's crew | Embergate (EP01): the Bridge of Seven Repairs (EP27), the gate yard forge, the Gate Valve House (EP26) | 30–40 min |

All five are optional, solo-clearable, cannot fail and give no lump quest XP (skill XP comes from actions; bible §11.6). Inactive, Active or Completed only. **No quest items** (bible §9.4: the Emberholt budget is spent by the milestones; side quests use carry-state objects, read-in-place records or none). No quest here is read by a milestone as a gate. Only **EFC** sets a region flag (`EH_COMMONS`, bible §9.1).

**Skill requirements.** None of these quests gates its offer on a skill level. Each skill hook sits inside a step and always has a time-cost alternative that is still play (the player reads, holds, carries or waits while someone else does the strength or the skill). The `[GD]` levels are light placeholders for the Gameplay Designer; the alternatives cost one turn of the presentation hour, a share of what is recovered, or a lower skill-XP share, never the quest.

**Level framing (ED-10).** EWA, EBL and ESR sit at EH-M1's Advanced identity; ECN and EFC at EH-M2's. Exact levels are Gameplay Designer calls.

### 0.2 Skill coverage and how the five feed one another

```text
EWA  Leatherworking (hook): soak, form and trim a cup for the cistern float valve ──► the wash cistern fills
     Heat-network repair (no skill): read the Commons branch tells, bleed the hot leg, turn the diverter
     Melee or Ranged: Cinder Rats in the dead leg
     └─ the diverter's handle is missing: stripped for brass (ECN's hook)
ECN  Tracking by objects and witnesses (no skill): scratched brackets, a cart rut, a stamped cock, a weigh-book
     Melee or Ranged: Dross Scavengers at the pits (two groups)
     Mining (hook): break the brass cache out of a cooled slag crust ──► Commons fittings back (EHC-02)
     └─ the fittings are refitted, and shown in public at First Cooling (EFC)
EFC  Cooking (hook): the Commons pot, read by the hearth tell (amber simmers, red scorches) ──► the meal before names (EHC-04)
     Carry: households' contributions, the year's mended work to the Commons table
     └─ sets EH_COMMONS: the Commons rota now opens the warming house (read by EH-M6 S01)
EBL  Woodcutting (hook, reclaimed crate-wood only): split and shave a new bell stay (EHC-05)
     Heat-network repair (no skill): set a relief valve's weight to the notch the tell approves at the night peak
ESR  Smithing (hook): draw and bend a parapet cramp at the gate yard forge, cut out the old, set the new in lead (EHC-06, EHC-07)
     Reading in place: seven crews' marks, each with a living witness or a record
```

Leatherworking uses imported offcuts; Mining breaks tip slag (the ridge seam is EFS's); Cooking is one ward pot read by the hearth tell (distinct from ESP and EH-M6 `S01`); Woodcutting is reclaimed crate-wood only (ED-11); Smithing carries ESR's hook as the bible row states. Ranged is viable in every fight here and required in none.

### 0.3 Economy-pass dependencies (ED-11)

Every material and output below is a **dependency**, not an item. **EHC-01 to EHC-07 are this file's proposal labels for the economy pass, not catalog ids or item names.** Legacy materials (ember shards, emberglass as a catalog item, ashsteel, conduction plates, Volkhari Ash) are not used.

| Id | Working name in this file | Used by | Nearest approved state | What the economy pass must decide |
|---|---|---|---|---|
| **EHC-01** | **leather offcuts** (imported, from the Commons repair box) | EWA (input, Leatherworking) | Vegetable-tanned leather (approved Lowmark state) | Whether offcuts are a lesser leather state; the cup recipe (soak, form, trim, wax). |
| **EHC-02** | **Commons brass** (stamped fittings: cocks, a diverter handle, bracket clamps) | ECN (recovered, returned; never kept by the player) | None | Nothing is created; the fittings are quest props. If the economy pass adds a scrap-brass item, the Slagside share in ECN uses it. |
| **EHC-03** | **slag crust** (cooled tip slag) | ECN (Mining node, quest-local) | Ore rock (nearest Mining node) | A breakable node with no ordinary yield in this quest; whether slag tips become a gathering source later. |
| **EHC-04** | **the Commons pot** (onion, barley, a smoked rib, root, what each lane brings) | EFC (craft output, eaten in place) | Prepared food (Cooking) | Ingredients are household contributions (carry props), not purchases. Whether a "ward stew" recipe exists outside the quest. |
| **EHC-05** | **crate-oak** (reclaimed crate beams) | EBL (input, Woodcutting) | Ordinary wood | A reclaimed-wood node at the Commons store stack (ED-11 "reclaimed crate-wood"). |
| **EHC-06** | **bar stock** (imported iron bar, from the Gatestone Masons' Hall store) | ESR (input, Smithing) | Iron bar | Cramp recipe (draw, bend, quench). |
| **EHC-07** | **lead** (for setting cramps) | ESR (input from the Hall) | None | Whether lead is a material; until defined, the pour is a channelled interaction with no item. |

### 0.4 Distinctness check

| Quest | Core verb | Physical problem | Wonder or unease | Human choice with a cost |
|---|---|---|---|---|
| EWA | trace, repair, share | Follow a branch by its tells from a cold cistern to a forgotten diverter; bleed the hot leg before turning ("you don't shut hot"); make a float cup | **Wonder:** the first steam off the cistern rolls across the wash-house floor and the queue goes quiet | The wash rota: shifts first, households first, or by the board |
| ECN | track, recover, return | Read scratches, a rut and a stamp to a scrap-weigher; fight through the pits; break a cache out of slag; take the case to the court that should have had it | **Unease:** in the pits, a slag pool shows the player's own face in a skin of cooling glass, then the skin cracks | None (contract); the court always hears it |
| EFC | cook, carry, celebrate | Gather from the lanes; cook one pot by the hearth tell; set the year's mended work on a table; light the lane plain or bright | **Wonder:** at the naming every lamp goes down a notch and the hood tells along the lane go from amber to clear, house by house, in a ripple | Plain or bright (flavour; the dimming happens in both) |
| EBL | listen, read, mend | Keep watch for a bell nobody rings; follow a second line from the rope into a grate; set a relief weight to the notch the tell approves at the night peak; replace a broken stay | **Unease:** an empty lane at night, a hiss under the grate, and the rope pulling down by itself | Keep the bell as the main's warning, or give the bell back to the shifts |
| ESR | read, repair, credit | Find seven marks in seven layers (some under the deck, beside the heat main's culvert); match each to a witness or a record; cut out a rusted cramp and set a new one in lead | **Wonder:** at dusk the culvert's heat comes up through the deck and the seven marks show dark on the warm stone, all at once, like writing | Cut the marks on the plaque stone, or write the crews in the gate's works roll |

No quest repeats a milestone's primary verb or strange moment (checked against EH-M1 to EH-M6). EWA and EBL reuse EH-M1's tell reading in a smaller space on purpose (bible §7.1). EFC's ripple is "heat follows the room" in calm, the reverse of EH-M5's crowd lift.

### 0.5 Shared rules for all five packages

- **Address.** Cinderwall NPCs, Veska, Hennet, Yorven and Odile say "warden's hand" (bible §5.3 rule 8); Embergate strangers in ESR say "traveller" until they have heard. Origin-neutral (D-3).
- **Tells and heat.** `EH_TELLS` is always true here (EH-M1 gates every quest). Each step pins the heat states it needs (bible §9.2; EI-HT-01 fallback). Waiting in a niche or at a keep-watch bench is always available.
- **The EH-M6 frost (playability audit ES-01).** The EGA hour pin (`EGA_FROST`: dusk until EGA `S01`, night from `S02` to the `S06` keep watch) governs only EGA steps and the frost-variant areas (Cinderwall W1 to W4 and the upper Undercroft). A side step placed in those areas is held while `EGA_FROST` is set and resumes at `EGA_THAW_SEEN`, as EME01 and EME05 already do. Keep watch anywhere else advances this player's hour normally. Any other quest's hour pin applies only to keep watch inside that quest's own step volume (ES-06). EDI-3 (EH-M6 auto-activation) stays open.
- **Skill steps** list their alternative in the beat; the alternative is still play and costs a turn, a share or skill XP, never the quest.
- **Combat.** Every enemy is defeated at 0 HP with the ordinary defeat presentation (CDR-1); none yields, flees, scatters or breaks off; no SX. Every fight accepts melee or ranged and requires neither (CDR-2) and is solo-tuned (CDR-6). No defeated enemy speaks after a fight or carries evidence (rulings §3.2).
- **Non-combatants.** Every named person in this file, every child, every Cinderwatch officer and every Slagside resident is never targetable.
- **Evidence and revelations.** Nothing here is evidence for a revelation; the steam, the slag mirror, the lamp ripple, the bell and the warm marks prove nothing. The tally board's "old leaks" is mentioned once as weather and is not explained or reduced (EH-M6 owns it). No Deepbrand or "below" presence. ECN's pit lot are shown only as pipe-strippers (bible §10) and are given no affiliation: the dossier calls the Dross scavengers "clandestine Remnant scavengers", and nothing here confirms or denies it (no line says what they are not). EBL's bell is a warden's knot (the Part 3 deep-works reading is not used).
- **Reserved decisions.** No node depends on D-E2, D-S1 or the initiate's name (Iven Calder, ED-3), all ruled 2026-11-15, or on D-3, C07 or the "invaders" wording. Nodes naming the EH-M1 valve order, Sarne Ardane, Ralenne's scene or the EH-M1 choice wording are tagged **`[ALLOCATION]`** (bible §3.1). No Volkhari person appears (D-C06); no precursor name, roster or casualty count (D-C03).
- **Time.** No calendar dates; the past is dated by events ("the cold-ward nights", "the winter the gate culvert froze", "the year the gate was rebuilt").
- **No failure.** Inactive / Active / Completed only. Death respawns at the quest's named safe point with step, flags and kept progress intact; logout restores the last persisted step and returns a dropped carry-state object to its source; walking away keeps the quest Active with the resume hook named in each package; missed moments re-offer on the next keep watch. **Carry-state classes (Integration EI-CA-04; playability audit ES-03):** small documents and tokens are possession flags that never limit movement or attack and are kept across death and logout; only bulky loads (walk, cannot attack) return to their source.
- **Co-op (CDR-6).** Each player's own quest state decides their own tells, valves, props, steps and choices. Shared enemies credit a partner only when the partner's own active step consumes the defeat. A partner who leaves or is ahead never blocks the other. Shared prop presentation is a fallback only (bible §9; MI-CO-06 pattern). No step needs two players.

### 0.6 Flags set and read

All flags set here are quest-local (`EWA_…`, `ECN_…`, `EFC_…`, `EBL_…`, `ESR_…`) except **`EH_COMMONS`** (bible §9.1, set by EFC). Every flag has exactly one writer.

| Flag | Values | Set by (one writer) | Read by |
|---|---|---|---|
| `EWA_SLATE_READ` | bool | EWA `S03_diverter` (slate inspect) | `EWA-D4` options |
| `EWA_CUP` | self / crew | EWA `S05_float` | `EWA-D6.20`; Dunya barks |
| `EWA_ROTA` | shifts / households / board | EWA `S06_rota` | Wash-house door prop; Commons barks; **EFC** `EFC-D3.12` (one Dunya line) |
| `ECN_COMPLAINT` | bool | ECN `S02_post` | `ECN-D5` options |
| `ECN_DIG` | self / diggers | ECN `S04_pits` | `ECN-D6.12` |
| `ECN_CASE` | bool | ECN `S05_court` | Yorven's court book prop; **EFC** `EFC-D3.20` (Grisel's mended-work line) |
| `EFC_LIGHT` | plain / bright | EFC `S04_light` | Lane props; barks |
| **`EH_COMMONS`** | bool | **EFC** `S06_first_light` (completion) | **EH-M6** `S01` (`EGA-D2.30`, the warming-house rota) per bible §9.1 and Act III |
| `EBL_STAY` | self / crew | EBL `S04_stay` | `EBL-D5.04` |
| `EBL_BELL` | kept / removed | EBL `S06_decide` | Bell post props; Cinderwall barks; EH-M6 (request only, §EBL.11) |
| `ESR_CRAMP` | self / crew | ESR `S03_cramp` | `ESR-D6.03` |
| `ESR_CREDIT` | marks / roll | ESR `S05_credit` | Plaque stone and works-roll props; gate barks |
| *(read)* `EH_TELLS` | bool | EH-M1 | Every tell inspect here |
| *(read)* `EH_COLD_WARD` | posted / settled `[ALLOCATION]` | EH-M1 `S07` | EWA `EWA-D1.10`/`.11`, `EWA-D7.10`/`.11`; EFC `EFC-D4.10`/`.11`, `EFC-D5.30` (Act I A9.2 and A9.3 name EWA and EFC as readers) |
| *(read)* `ECW_SHORTFALL_SEEN` | bool | EH-M1 `S03` | EWA `EWA-D2.30` (Act I A9.2 names EWA as a reader). The line does not explain the shortfall. |
| *(read)* `ECW_SEAT_RING` | self / crew | EH-M1 `S05` | ESR `ESR-D5.02` (one line, `self` only) |
| *(read)* `EH_CURRICULUM` | guild / evidence | EH-M2 | EFC `EFC-D6.10`/`.11` (one Jessa line) |
| *(read)* `EH_HOLLOW_TRUTH` | told / kept / unset | EH-M3 | EFC `EFC-D5.20` (optional: Hesper names her brother if EH-M3 is Completed) |
| *(read)* `TAS_ACCOUNT` | named / held / unwritten / unset (Thornfell *Ash in the Snow*) | Thornfell TAS | ESR `S02_marks` optional visit (`ESR-D4`), `named` only; any other value: no visit and no line |

---
---

## EWA — The Water That Did Not Arrive

### EWA.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.water_that_did_not_arrive` |
| Type | Settlement. Heat Commons 1/3 (bible §7.1). |
| Unlock | EH-M1 Completed. Offered by Dunya Kordel at the Commons wash-house door behind the Cooling House (`EWA-D1`); Hennet's bark sends the warden's hand there (`EWA-B0.1`). |
| Resume hook | Dunya at the wash-house door: `EWA-D1.00` "Still cold. Still a queue. Where had you got to?" pins the step. |
| Skills | Leatherworking ~[GD: low] (hook; crew alternative); Melee or Ranged (Cinder Rats) |
| Combat share | ~10% (one rat nest in the dead leg) |
| Cameo | Veska Dunmor (her slate; the key); Hennet Ulm (offer bark) |
| Choice | The wash rota (`EWA_ROTA` = shifts / households / board); text and props only |
| Unlocks | ECN; the wash-house as a public quench trough and keep-watch bench; reading the Commons branch tells |
| **Anchor** (§7.1) | Heat Commons; fire wardens |
| **World-truth row** | H23 (recovery: who the rebuilt city warms, at ward scale) |
| **Revelation role** | None (local). Feeds `[ALLOCATION]` lines only. The tally board's "old leaks" is mentioned once as weather and is not explained or reduced. |
| **Recurring evidence** | Veska's chalk slate at the Cinderwall junction (recurs from EH-M1): a second line in her hand records the diverter turned "to House" on the cold-ward nights. |
| **State compliance** | Inactive / Active / Completed. No fail path: a hot leg cannot be shut until it is bled (the diverter refuses with a scald, never a reset); the Leatherworking hook has an overnight wait; the rota choice is text only and every option fills the cistern. |
| **Combat compliance** | Cinder Rats (EWA-E1) defeated at 0 HP. Melee or ranged; ranged never required. Solo-tuned (CDR-6): one player can clear the nest, bleed, turn and fit alone; a partner's kills credit them only if their own step consumes it. No SX. |

**In one paragraph.** The ward is warm again, but the Heat Commons wash cistern behind the Cooling House runs cold, and the queue of ash-black forge hands and women with washing is arguing about it. **Dunya Kordel**, who keeps the wash-house, gets the warden's hand to read the cistern's coil tell (clear) against the Cooling House hood tell (amber), then go down the wash-house hatch and follow the Commons branch by its tells, past a Cinder Rat nest in the dead leg, to a tee where the three-way **diverter** is lashed toward the Cooling House and its brass handle is gone. Veska's slate at the junction holds the cause: *Commons diverter turned to House. D.K. Put back when open.* On the second cold-ward night Dunya turned it so the old ones sleeping on the benches got the Commons' last heat, and then forgot her own hand. With Veska's crew key, the player bleeds the hot leg until its tell clears ("you don't shut hot"), turns the diverter, and finds the cistern still low because the float valve's leather cup perished in the cold: they form a new one, or wait for the crew's spare. The cistern fills and steams, and Dunya asks the warden's hand to say how the rota will run.

### EWA.2 Selection record and canon grounding

Selected shape: Cold cistern → trace the branch by tells → rat nest in the dead leg → the lashed diverter and Veska's slate line → bleed before turning → the perished float cup (skill or wait) → the rota.

| Element | Source | Status |
|---|---|---|
| Cooling Houses; the Heat Commons (shared wash, warmth and repair) | Part 3 Emberholt proposal; bible §1.2, ED-13 | [PROPOSAL — DIRECTOR] ED-13; [NEW] detail |
| The Cooling House board's "rota for the wash cistern"; the Heat Commons store behind the wash-house | Act I dialogue (ECW-I2); Act III W4 | [NEW], consistent |
| Tells, cooling niches, vent breath; "You don't shut hot"; "Never touch a red" | Bible §1.1; Act I | [NEW], consistent |
| Veska's chalk slate at the junction | Act I `S02` | [NEW], recurs |
| Cinder Rats (fur glows when agitated) | Dossier §XII; bible §10 | [CANON] |
| Dunya Kordel; the diverter; the float cup | This package | [NEW] |

### EWA.3 The places [MAP VERIFICATION REQUIRED]

Relative order: the Cooling House (Act I W2) → its yard → the wash-house behind it → the wash-house hatch → the Commons branch under the lane → the tee → (a side passage) the Cinderwall junction (Act I U5), reached as in EH-M1.

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **C1. The wash-house** | Offer; cistern; float; rota | A low stone room behind the Cooling House yard. A great iron **cistern** on a plinth, a copper **coil** running into its base with a **tell** on the coil's inlet. Wash troughs along one wall, benches along the other. A **float valve** on the cistern's feed with a brass arm and a hinged lid. A **repair box** under the bench (leather offcuts, a wooden former, thread, wax). A chalk board on the door: the old rota, rubbed half out. A **queue**: forge hands in ash, two women with washing, an old man with a kettle. | — |
| **C2. The wash-house hatch** | Into the branch | An iron hatch in the floor by the cistern plinth, a ladder down. A blue-washed **cooling niche** at the ladder foot with a trough. | Ladder |
| **C3. The Commons branch** | Trace | A duct half the height of the Undercroft's, walkable stooped. Two pipe runs: the **house leg** (to the Cooling House) and the **cistern leg** (to the wash-house). Tells every twenty paces. Two floor grates that breathe (~10 s). | Walkable; one **agility** squeeze past a fallen bracket (fallback: round by the grate) |
| **C4. The dead leg** | EWA-E1 | Where the cistern leg runs cold, the duct is dry and lukewarm: a **rat nest** of fur, rag and ash packed against the pipe. | — |
| **C5. The tee** | The diverter | Where the branch splits. A three-way **diverter** with a square socket where its handle should be, lashed toward the house leg with rag and wire. A **bleed cock** on the house leg with its own tell. A cooling niche. | — |
| **C6. The Cinderwall junction** (Act I U5) | Veska's slate; the crew key | As EH-M1, now warm and Working. Veska on duty. | Through the side passage to the upper line (as Act I) |

### EWA.4 Beats

**Beat 0: The Queue (`S00_offer`).** *Objective: Talk to the wash-house keeper.* Hennet, ladling at the Cooling House hatch: "Dunya wants you. The wash-house. Take a bowl, she won't." (`EWA-B0.1`). At the wash-house door the queue is arguing (`EWA-B1`). Dunya Kordel: the ward is warm and her cistern is cold; she has asked Veska, who said the Commons branch is the Commons' own; she needs somebody who walked the junction (`EWA-D1`). With `EH_COLD_WARD` the ward's mood colours one line `[ALLOCATION]`.

**Beat 1: Read the Cistern (`S01_cistern`).** *Objective: Find out where the cistern's heat stops.* Inspect the **coil tell** (`EWA-I1`: clear, cold) and, through the yard door, the **Cooling House hood tell** (`EWA-I2`: amber, working). Dunya: "Same branch feeds both. One's cold, one's warm. You tell me." Inspect the **float valve** (`EWA-I3`): the arm hangs low; water trickles. (Noted now; it matters at `S05`.) Open the hatch (interaction).

**Beat 2: Follow the Branch (`S02_trace`).** *Objective: Follow the Commons branch to where it splits.* Down the ladder (C2; touch water at the niche, Veska's rule; bark if skipped). The branch is pinned **Working** on the house leg and **Cool** on the cistern leg. Read three tells on the way (required inspects `EWA-I4` to `EWA-I6`): the riser at the foot of the ladder (cistern leg: clear), the mid-run pair (house leg amber, cistern leg clear), and the tee's bleed cock (amber). Floor grates breathe on a ~10 s cycle: ash lifts ~1.5 s before each exhale (damage and one-step knock-back). In the **dead leg** (C4) the cistern pipe is lukewarm and dry, and a Cinder Rat nest is packed against it: **EWA-E1**. The step completes on reaching the tee (C5).

**Beat 3: The Diverter (`S03_diverter`).** *Objective: Find out who turned the diverter.* Inspect the diverter (`EWA-I7`, required): turned to the house leg, lashed with rag and wire, a square socket and **no handle** ("Somebody's had the brass"). A paper tag in the lashing, pulped by damp: only "…HOUSE…" is readable. The player cannot turn a diverter without a key, and Dunya does not have one. Through the side passage to the **junction** (C6): Veska, asked (`EWA-D3`), points at her slate (`EWA-I8`; sets `EWA_SLATE_READ`): under her own *Shut on order. Protested. Overruled.* there is a second line in her hand: *Commons diverter turned to House. D.K. Put back when open.* "Second cold night. Dunya came down and said the old ones on the benches were blue. I wrote it so it'd be put back. Then it got warm and everybody forgot I can write." Veska lends the **crew key** (carry-state). Back at the wash-house, or calling down the hatch, Dunya hears it (`EWA-D4`): "D.K. That's me. I did it. I slept nine nights on a bench and I forgot my own hand."

**Beat 4: Bleed, Then Turn (`S04_turn`).** *Objective: Put the diverter back.* At the tee:

1. **Cut the lashing** (interaction).
2. **Turn with the key while the house leg is amber:** refused. The key will not seat while the diverter body is hot; the handle-end scalds (small damage, one step of knock-back) and Veska's rule comes up as a bark: "You don't shut hot." (`EWA-B4.2`). Nothing resets.
3. **Bleed the house leg** at its bleed cock: a 3-segment channel (~3 s each; a hit interrupts the current segment; completed segments are kept). Steam roars from the bleed pipe for ~2 s; the house-leg tell drops **amber → clear** over ~2 s.
4. **Turn the diverter** with the key (a 2-segment channel). The cistern-leg tells come up **clear → amber**, from the tee back toward the ladder, one by one over ~4 s. The house leg stays clear for one turn and then comes back amber on its own share (the diverter is now at its middle mark, the Commons' normal setting: both legs fed).

**Beat 5: The Float (`S05_float`).** *Objective: Get the cistern filling.* Back up the hatch. The coil tell is amber and the cistern's skin begins to steam, but the level does not rise: the float valve's **leather cup** has perished in the cold and the feed weeps past it (`EWA-I9`). Two ways, both complete the step:

- **Option A (skill): make a cup** (**Leatherworking ~[GD: low]**). From the repair box (C1): **cut** a disc from an offcut (EHC-01) against the old cup (interaction, ~2 s); **soak** it in the cistern's warm water (one interaction; the cup goes dark and soft); **form** it over the wooden former (a 2-segment channel, ~3 s each); **trim and wax** (one interaction). **Fit** it to the valve (a 2-segment channel). Dunya: "My father did those. He swore at every one." `EWA_CUP` = self.
- **Option B (time-cost): the crew's spare.** Dunya sends the old man with the kettle to the junction for one. **Keep watch** at the wash-house bench until morning (one turn); a line hand brings a cup from the crew store and the player fits it (the same 2-segment fit). `EWA_CUP` = crew.

The arm lifts, the feed hisses, the cistern fills. **The steam (EWA.5)** rolls off the surface and along the floor.

**Beat 6: The Rota (`S06_rota`).** *Objective: Tell the wash-house how the water will be shared.* The queue has come back in, and the quarrel starts again over the first hot water; the coil tell steps up to amber-bright with the voices (heat follows the room). Dunya bangs a bucket. She wants the warden's hand to say it, "so it isn't one of us saying it about the rest" (`EWA-D6`). The choice (EWA.8) sets `EWA_ROTA`. With `EH_COLD_WARD` the ward cites the EH-M1 outcome `[ALLOCATION]` (`EWA-D7.10`/`.11`). Dunya chalks the rota on the door, pays the warden's hand from the Commons box, and asks one more thing: "Grisel will want you. The handle didn't walk off by itself." (`EWA-D6.40`). Quest Completed; ECN offered.

### EWA.5 The steam (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Fill** | The float arm lifts with a clack; the feed hisses into the cistern. |
| 1–4 s | **Steam** | A sheet of steam lifts off the cistern's surface and spills over the lip, rolling across the cold stone floor at ankle height toward the door. The queue's feet disappear in it. |
| 4–8 s | **Quiet** | The queue stops talking. A child in the queue puts her hand into the steam and laughs. The coil tell holds amber. |
| After | **Dunya** | "Look at that. Forgot it did that." |
| Meaning | Hot water in a cold room. Proves nothing. |

### EWA.6 Encounters and hazards

Tuned for EH-M1's Advanced identity (ED-10).

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EWA-E1** | 3 × Cinder Rat **scurrier**, 2 × **biter** (bible §10) | The dead leg (C4), in and around the nest | Scurriers run the pipe brackets and drop; biters burst from the nest and lunge | **Scurrier drop:** fur flares orange on the bracket overhead (~1.0 s), then it drops on the spot below (sidestep). **Biter lunge:** crouches, back fur glowing (~0.8 s), then a short lunge-bite. | A small fight in a stooped duct; why the dead leg is dead | 45–60 s; 75–90% HP |
| **EWA-H1** | Floor grates (vent breath) | C3, two grates | Timed hazard | Ash lifts ~1.5 s before each exhale (~10 s cycle); damage and one-step knock-back | Reuses EH-M1's lesson | — |
| **EWA-H2** | The hot diverter | C5 | Refusal | The key will not seat; a scald and one step of knock-back | "You don't shut hot" as a rule the hand learns | — |

**Rules.** Rats defeated at 0 HP with the ordinary defeat presentation (their fur goes dark). Melee in the duct or ranged down its length both work; nothing requires ranged. The nest prop clears when the last rat is defeated (the dead leg is then just a cold pipe). Nothing in the nest advances the quest. **Death:** respawn at the wash-house niche (C2); defeated rats stay defeated; bled and turned progress is kept.

### EWA.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the wash-house keeper. | `EWA-D1` accept | Yes | Hennet's bark `EWA-B0.1` points the way |
| `S01_cistern` | Find out where the cistern's heat stops. | Coil tell + hood tell + float inspects + hatch opened | Yes | — |
| `S02_trace` | Follow the Commons branch to where it splits. | 3 tell inspects (`EWA-I4`–`I6`) + EWA-E1 defeated + enter tee volume (C5) | Yes | House leg pinned Working, cistern leg Cool |
| `S03_diverter` | Find out who turned the diverter. | Diverter inspect + slate inspect (`EWA_SLATE_READ`) + `EWA-D3` end (crew key) + `EWA-D4` end | Yes | `EWA-D4` can be heard at the hatch or the wash-house |
| `S04_turn` | Put the diverter back. | Lashing cut + bleed channel + turn channel | Yes | Turn refused while the house-leg tell is amber; cistern leg → Working on completion |
| `S05_float` | Get the cistern filling. | Cup fitted (Option A) **or** keep watch to morning + fit (Option B) | Yes | Sets `EWA_CUP`; steam moment plays |
| `S06_rota` | Tell the wash-house how the water will be shared. | `EWA-D6` choice + `EWA-D6.40` end | Yes | Sets `EWA_ROTA`; crew key returned to Veska automatically; small payment; quest Completed; ECN offered |

| Flag | Set by | Read by |
|---|---|---|
| `EWA_SLATE_READ` | `S03` | `EWA-D4` options |
| `EWA_CUP` = self / crew | `S05` | `EWA-D6.20`; Dunya barks |
| `EWA_ROTA` = shifts / households / board | `S06` | Wash-house door prop; barks; EFC `EFC-D3.12` |

### EWA.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Shifts first** (`shifts`): *"Hot shifts wash first. Ash burns if it sits."* | The bell-hour water goes to crews coming off forge and slag shifts; households wash after. | The washing waits; the women in the queue say what they think of forge hands. | Door board: *Bell: shifts. After: houses.* Forge hands nod at the warden's hand. |
| **Households first** (`households`): *"Morning water for the houses. Children, washing, the old ones."* | Mornings are for households; shifts take what is left at the bell. | Crews wash in half-warm water and say so. | Door board: *Morning: houses. Bell: what's left.* Mothers bring the warden's hand bread. |
| **By the board** (`board`): *"Lane by lane, turn by turn. Write it up and keep to it."* | Dunya chalks a turn for each lane, rotating daily. | Slow and argued every day; Dunya has to stand at the door with the chalk. | Door board: a grid of lanes. Dunya: "Fair's a lot of chalk." |

No option is wrong. The cistern fills in all three; nobody goes unwashed for long.

### EWA.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | From the Commons box ([GD] economy tuning). |
| The wash-house | Access | A public quench trough and keep-watch bench (C1). |
| Reading a branch | Knowledge | Commons diverters and bleed cocks across Cinderwall become inspectable with their state. |
| Leatherworking, Melee or Ranged XP | Action XP only [GD] | Less Leatherworking XP on the crew path. No lump quest XP. |
| ECN | Story | Grisel Tamm's offer. |

### EWA.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Tries to turn the diverter hot | Refused with a scald and the bark; nothing resets. |
| Tries to turn it before getting the key | "Square socket. No handle." (`EWA-B4.1`). |
| Will not or cannot do Leatherworking | Option B: one keep-watch turn; never blocked. |
| Death | Respawn at the wash-house niche (C2). Rats defeated stay defeated; the bleed and turn persist; the crew key stays carried. |
| Logout | Restore to the step: the wash-house (`S00`, `S01`, `S05`, `S06`), the niche at the ladder foot (`S02`–`S04`). The crew key, if dropped by logout, is back on Veska's nail at the junction. |
| Walking away | Stays Active; resume hook at Dunya (`EWA-D1.00`), or Veska at the junction (`EWA-D3.00` "Key's on the nail if you want it."). |
| Co-op | Shared rat fight (credit to each partner whose own `S02` consumes it). The diverter, bleed cock, float, tells and rota are per player; a partner's turned diverter does not turn yours. Any shared prop shown is presentation only (CDR-6). |

### EWA.11 Integration needs

All standard: quest-pinned branch states per player (house leg Working, cistern leg Cool until `S04`); a diverter interaction refused while the house-leg tell is amber (EH-M1 red-cock pattern); a cistern-leg tell cascade (~4 s) on turn; a cistern level prop and steam VFX; Leatherworking at the repair box (the cup is a quest object until EHC-01 is defined); a carry-state crew key; three door-board variants by `EWA_ROTA`; a scripted coil-tell flick during `EWA-D6` (heat follows the room, ~3 s).

### EWA.12 Mystery ledger entry

None (resolved in-quest). The tally board's "old leaks" is mentioned and not touched (EH-M6).

### EWA.13 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Dunya Kordel** [NEW], keeper of the Commons wash-house | Every lane's wash day; who argues; the cistern since her father kept it; that she turned the diverter (once reminded). | Why the board never balances. | Brisk, loud, fond of everyone she shouts at. Speaks in lists. Ashamed for exactly one line, then busy. Calls the player "warden's hand". |
| **Veska Dunmor** [NEW, bible §5.2] | Her slate; the branch; the rule. | — | As Act I: short instructions, points instead of explaining. |
| **Hennet Ulm** [NEW, bible §5.2] | Everyone's business. | — | Feeds first. |
| **QUEUE** (forge hand, woman with washing, old man with kettle, a child) | Their own turn. | — | Cooling House humour, quick and sharp. |

**Offer** (`EWA-D1`, step `S00_offer`)

```
EWA-D1.00 [quest Active, returning] DUNYA: "Still cold. Still a queue. Where had you got to?"   (pins step) → end
EWA-D1.01 DUNYA: (over the queue) "One at a time. No, not you, you've had one. Warden's hand. Good. Come here, before they eat each other."
EWA-D1.02 DUNYA: "Ward's warm. Lovely. Cistern's cold. Same branch, same pipes, same everything. The Cooling House hood's running amber and my coil's clear as a window."
EWA-D1.03 DUNYA: "I asked Dunmor. Dunmor says the Commons branch is the Commons' business. She's right, which is annoying."
EWA-D1.10 [EH_COLD_WARD = posted] [ALLOCATION] DUNYA: "The ward read that order on the board and now everybody's an expert in where heat goes. Half this queue thinks the terraces have got my water too."
EWA-D1.11 [EH_COLD_WARD = settled] [ALLOCATION] DUNYA: "Yorven says nothing moves off Cinderwall without his countersign now. Lovely. Then where's my water?"
  > "I'll look at the cistern."                                       → EWA-D1.20
  > "Why's the queue fighting?"                                      → EWA-D1.30
  > "Not now."                                                       → EWA-D1.40
EWA-D1.20 DUNYA: "Coil's at the bottom. Tell's on the inlet. Hatch is by the plinth. Don't fall in, it's the only cistern I've got."   {event: accept → S01_cistern}
EWA-D1.30 DUNYA: "Hot shifts want to wash first because ash burns. Houses want to wash first because children. They're both right. That's why it's loud."   → EWA-D1 options
EWA-D1.40 DUNYA: "Cold'll keep. So will they. Unfortunately."   → end (offer stays open)
```

**Barks: the queue and the way in**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EWA-B0.1 | Passing the Cooling House hatch after EH-M1 | HENNET | "Dunya wants you. The wash-house. Take a bowl, she won't." |
| EWA-B1.01 | Near the queue | FORGE HAND | "I've ash in places I've not got names for." |
| EWA-B1.02 | Near the queue | WOMAN WITH WASHING | "Then name them somewhere else." |
| EWA-B1.03 | Near the queue | OLD MAN | "I only want a kettle. Nobody fights over a kettle." (beat) "Usually." |

**The branch** (`EWA-D2`, Dunya down the hatch at the mid-run pair)

```
EWA-D2.30 [ECW_SHORTFALL_SEEN] DUNYA: "And don't tell me it's the old leaks. Odile's board has said old leaks since I was a girl. That's weather. This is a pipe."   → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EWA-B2.02 | EWA-E1 defeated | DUNYA (down the hatch, hearing it) | "Was that rats? Tell me it was rats. Tell me it wasn't the pipe." |

**Veska and the slate** (`EWA-D3`, at the junction)

```
EWA-D3.00 [quest Active, returning] VESKA: "Key's on the nail if you want it."   → end
EWA-D3.01 VESKA: (not looking up) "Commons diverter?"
  > "Turned to the House. Lashed. No handle."                        → EWA-D3.02
EWA-D3.02 VESKA: (points at the slate with her lamp) "Read it."   {event: slate inspect available; EWA-I8}
EWA-D3.03 [EWA_SLATE_READ] VESKA: "Second cold night. Dunya came down and said the old ones on the benches were blue. We turned it to the House. I wrote it so it'd be put back."
EWA-D3.04 VESKA: "Then it got warm, and everybody forgot I can write. Again."
  > "Can I borrow a key?"                                            → EWA-D3.05
  > "Why not put it back yourself?"                                  → EWA-D3.06
EWA-D3.05 VESKA: "Crew key. Square shank. Bring it back." (beat) "And don't turn it hot."   {give crew key (carry-state)} → end
EWA-D3.06 VESKA: "Commons branch is the Commons'. If a warden turns their diverter, next week it's my fault their water's cold. I've had that week."   → EWA-D3.05
```

**Dunya hears it** (`EWA-D4`, at the hatch or the wash-house)

```
EWA-D4.01 [EWA_SLATE_READ] DUNYA: "D.K.?" (beat) "That's me. I did it. Second night. The old ones were blue."
EWA-D4.02 DUNYA: "I slept nine nights on a bench and I forgot my own hand." (beat, busy again) "Right. Put it back. Then I'll be ashamed properly, later, when there's time."   → end
```

**At the tee** (barks)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EWA-B4.1 | Interact with the diverter, no key | (prompt) | "Square socket. No handle." |
| EWA-B4.2 | Key tried while the house leg is amber | (the player's journal line, Veska's rule) | *You don't shut hot.* |
| EWA-B4.3 | Bleed complete | DUNYA (down the hatch) | "That roar's not the cistern, is it? Tell me it's not the cistern." |
| EWA-B4.4 | Diverter turned | DUNYA | "Something's knocking in my coil. Good knocking." |

**The float and the rota** (`EWA-D6`, step `S05`–`S06`)

```
EWA-D6.01 DUNYA: (at the cistern, peering) "Coil's warm. Water isn't coming. Float's weeping past its cup. The cold had it."
  > [Option A] "I'll make a cup."                                    → EWA-D6.02
  > [Option B] "Is there a spare?"                                    → EWA-D6.03
EWA-D6.02 DUNYA: "Box under the bench. Offcuts, the former, wax. My father did those. He swore at every one."   → end
EWA-D6.03 DUNYA: "Crew store has them. Old Gav, take your kettle and ask Dunmor's lot for a cup." (OLD MAN goes) "Morning. Sit. You've earned a sit."   {event: keep watch enabled} → end
EWA-D6.10 (Steam moment, EWA.5.) DUNYA: "Look at that. Forgot it did that."
EWA-D6.11 (The queue comes back in; voices rise; the coil tell steps up.) FORGE HAND: "Hot shifts first!" WOMAN WITH WASHING: "Houses first!"
EWA-D6.12 DUNYA: (bangs a bucket; the coil tell settles) "You hear that? The coil can hear you. Warden's hand. You say it. Then it isn't one of us saying it about the rest."
EWA-D6.20 [EWA_CUP = self] DUNYA: "And your cup's holding. Don't let it go to your head."
  > "Hot shifts wash first. Ash burns if it sits."                   → EWA-D6.30 {EWA_ROTA = shifts}
  > "Morning water for the houses. Children, washing, the old ones." → EWA-D6.31 {EWA_ROTA = households}
  > "Lane by lane, turn by turn. Write it up and keep to it."        → EWA-D6.32 {EWA_ROTA = board}
EWA-D6.30 DUNYA: (chalking) "Bell: shifts. After: houses." (to the queue) "You heard."   → EWA-D7
EWA-D6.31 DUNYA: (chalking) "Morning: houses. Bell: what's left." (to the forge hands) "Wash quicker."   → EWA-D7
EWA-D6.32 DUNYA: (chalking a grid) "Fair's a lot of chalk." (beat) "I've a lot of chalk."   → EWA-D7
```

**The ward's line** (`EWA-D7`) `[ALLOCATION]` where tagged

```
EWA-D7.10 [EH_COLD_WARD = posted] [ALLOCATION] FORGE HAND: "Put it up next to the order, then. Everything that gets moved in this ward goes on that board now."
EWA-D7.11 [EH_COLD_WARD = settled] [ALLOCATION] DUNYA: "Yorven'll want it countersigned. Everything wants countersigning now. I'll countersign it myself."
EWA-D6.40 DUNYA: (pays from a tin box) "From the Commons box. Don't argue, it's rude." (beat) "Grisel will want you. Somebody had that handle, and it didn't walk off by itself."
      {crew key returned to Veska; small payment; event: EWA-D6.40 end → quest Completed; offer ECN}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| EWA-I1 | Coil tell | "Clear. Cool." / after `S04`: "Amber. Working." | `EH_TELLS` |
| EWA-I2 | Cooling House hood tell (through the yard door) | "Amber. Working." | `EH_TELLS` |
| EWA-I3 | Float valve | "The brass arm hangs low. Water trickles past the valve into the cistern and does not rise." | — |
| EWA-I4 | Riser, ladder foot | "Cistern leg: clear. The pipe is cold to the back of a hand." | — |
| EWA-I5 | Mid-run pair | "House leg: amber. Cistern leg: clear. Two pipes, a hand apart." | — |
| EWA-I6 | Tee bleed cock | "Amber. The house leg's bleed. Warden's chalk on the wall beside it: a tick." | — |
| EWA-I7 | Diverter | "A three-way diverter turned to the house leg and lashed there with rag and wire. A square socket, bright at the edges where a handle was prised off. A pulped paper tag: '…HOUSE…'." | — |
| EWA-I8 | Veska's slate | "*Shut on order. Protested. Overruled.* Under it, smaller: *Commons diverter turned to House. D.K. Put back when open.*" | Sets `EWA_SLATE_READ` |
| EWA-I9 | Float valve (after `S04`) | "The leather cup on the valve has gone hard and split. Water weeps past it however high the arm lifts." | — |
| EWA-I10 | Door board (after) | By `EWA_ROTA`: "*Bell: shifts. After: houses.*" / "*Morning: houses. Bell: what's left.*" / "A grid of lanes and days in chalk." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| DUNYA | "Water's hot. Queue's loud. Normal." | EWA Completed |
| FORGE HAND | "Washed before supper. First time this season." | `EWA_ROTA = shifts` |
| WOMAN WITH WASHING | "Morning water. You're welcome to bread." | `EWA_ROTA = households` |

### EWA.14 Open decisions

1. **`[ALLOCATION]` (ED-1):** `EWA-D1.10`/`.11` and `EWA-D7.10`/`.11` change if the EH-M1 cause changes. The reroute itself survives any cause that shut the junction.
2. **Veska's second slate line [NEW]:** uses the bible's "Veska's slate (recurs from ECW)" as the recurring evidence. If the Director prefers the slate to carry only her protest, Dunya's own tag on the lashing (fully legible) carries the line; the quest is unchanged.
3. **The missing handle** seeds ECN. If ECN changes, the crew key alone is enough.
4. **Leatherworking `[GD: low]`:** Gameplay Designer to set; the crew path is one turn.

### EWA.15 Review log

| Finding | Revision |
|---|---|
| First draft blamed the "old leaks". | Cut. The shortfall is EH-M6's; Dunya calls it weather and moves on (`EWA-D2.30`). |
| Risk of talk-and-inspect only. | The step chain is physical: tells on a branch, a rat nest, a refused key, a bleed, a turn, a float cup. |
| Choice weight. | The rota is text and props only, as the contract states; all three fill the cistern. |
| "You don't shut hot" reused. | Intended: EH-M1's rule pays off in a smaller space; the refusal is a scald, never a reset. |

---
---
## ECN — The Case That Never Reached the Court

### ECN.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.case_that_never_reached_the_court` |
| Type | Combat challenge. Heat Commons 2/3 (bible §7.1). |
| Unlock | EWA Completed. Offered by Grisel Tamm at the wash-house (`ECN-D1`), pointed there by Dunya at `EWA-D6.40`. |
| Resume hook | Grisel at the wash-house bench: `ECN-D1.00` "Brass is still gone and I'm still old. Where are we?" pins the step. |
| Skills | Mining ~[GD: low] (hook; Slagside diggers as the alternative); Melee or Ranged (Dross Scavengers) |
| Combat share | ~30% (two groups at the pits) |
| Cameo | Yorven Khelt (the ward court); a Cinderwatch clerk (role) |
| Choice | None (contract). The court always hears the case. |
| Unlocks | EFC (with EH-M2); Ilsa Cleff's weigh-shed at Slagside as a scrap buyer (economy pass); Yorven's court book as an inspect |
| **Anchor** (§7.1) | Heat Commons; Slagside |
| **World-truth row** | H23, H25 (present pressure, local: a ward's complaint that goes to the wrong door) |
| **Revelation role** | None. |
| **Recurring evidence** | The ward complaint, entered in Yorven's court book (`ECN_CASE`). |
| **State compliance** | Inactive / Active / Completed. The fittings are recovered by the player's own digging or crew-recovered next morning by Slagside diggers for a share. No fail path. |
| **Combat compliance** | Dross Scavengers (ECN-E1, ECN-E2), human, defeated at 0 HP with the ordinary defeat presentation; no yield, flight or scatter; no line after the fight. Ranged viable (slingers on ledges give ranged players targets; every slinger is reachable on foot); ranged never required. Solo-tuned (CDR-6). No SX; no elite (bible §10: no scavenger is made a boss). |

**In one paragraph.** Somebody has been taking the Heat Commons apart for its brass: the diverter's handle, wash cocks, taps and clamps, all stamped with the Commons' cup. A season ago twenty households signed a complaint and **Grisel Tamm**, the Commons fitter, handed it in at the Cinderwatch post; nothing came of it. The warden's hand reads the trail (bright pry-bar scratches, a hand-cart's rut in the ash, a dropped stamped cock), finds the complaint in the post's unlabelled tray (the Watch answers riots, accidents and surges, and nobody sent it on to the Overseer's court), and at **Slagside** gets the scrap-weigher **Ilsa Cleff** to turn her weigh-book round: a season of brass bought by weight from "the pit lot". She says where they bury it. At the **Dross Scavenger Pits** the pit lot fight and are defeated; the cache is under a skin of cooled slag, broken out with a pick or dug out by Slagside's diggers by morning for a share. Then the case goes to Yorven's court night at the Cooling House, with the complaint, the brass and Ilsa with her book, and into his court book.

### ECN.2 Selection record and canon grounding

Selected shape: Read the trail by objects → find the lost complaint → a living witness with a weigh-book → the pits (two fights) → break the cache out of slag (skill or diggers) → the ward court.

| Element | Source | Status |
|---|---|---|
| The Emberfall Dross: slag, unstable byproduct, discarded conduits, black-market opportunities | Dossier §VII.5 | [CANON] |
| Dross Scavengers as human pipe-strippers (scavenger, slinger) | Bible §10; Act III EGA-E1 kit | [NEW] on a canon group; the dossier's "clandestine Remnant scavengers" label is not used (§0.5) |
| Slagside (EP06), the Dross Scavenger Pits (EP18) | Bible §4.2 | [NEW] |
| The Cinderwatch (Emberguard; answers riots, accidents and surges) | Bible §1.2 | [CANON] |
| Yorven Khelt, District Overseer; keeps Deepbrand and Emberguard heavy-handedness out of his ward | Character file; bible §5.1 | [CANON] |
| Yorven's ward court and court book | This package (bible §7.1 "the complaint reaches Yorven's book") | [NEW] |
| Grisel Tamm, Ilsa Cleff, the Commons cup stamp | This package | [NEW] |

### ECN.3 The places [MAP VERIFICATION REQUIRED]

Relative order: the wash-house (C1) → the slag lanes along Cinderwall's Dross edge → the Cinderwatch post on the lanes → Slagside's shanties on the tips → the pits beyond them. MAP VERIFICATION REQUIRED for every placement; the Dross lies beside Cinderwall (bible §1.2).

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **N1. The wash-house** (EWA C1) | Offer; refit | As EWA, now hot. Grisel's toolbag on the bench. | — |
| **N2. The Commons runs** | Trail | Bath-house and lane brackets along Cinderwall's lower lanes: **three stripped brackets** with bright, fresh scratches. | — |
| **N3. The slag lane** | Trail | An ash-floored lane toward the Dross. A **hand-cart rut** in the ash, two wheels, one wobbling. Half-buried in the rut: a **wash cock** with the cup stamp. | — |
| **N4. The Cinderwatch post** | The complaint | A small stone post with a brazier and a desk. Three trays: *Riots*, *Accidents*, *Surges*. A fourth, unlabelled, under the desk: papers nobody sorted. | — |
| **N5. Slagside** (EP06) | Ilsa | Shanties of reclaimed plate and crate-wood on a cooled tip. **Ilsa Cleff's weigh-shed**: a beam scale, sorted bins of scrap (iron, copper, brass), a **weigh-book** on a nail. A bench by the shed (respawn point for `S03`–`S04`). Slagside's diggers sit on upturned buckets. | — |
| **N6. The pits mouth** (EP18) | ECN-E1 | A cut through slag banks into a basin. Slag **pools** (semi-cooled; glow under a crust); vent grates in the slag; a lean-to. | Walkable; the pools are hazard volumes |
| **N7. The cache basin** | ECN-E2; the dig | A lower basin with two **slag ledges** (slingers' places, each reachable by a ramp). A patch of **slag crust** with a tell bead pressed into it (the pit lot's marker), three crust nodes. A **cooling niche** cut into the basin wall by old warden crews. | Ramps to both ledges |
| **N8. The Cooling House** (Act I W2), court night | The court | Benches turned to face the end table. Yorven at the table with his **court book**. | — |

### ECN.4 Beats

**Beat 0: Twenty Marks (`S00_offer`).** *Objective: Hear the Commons fitter out.* Grisel Tamm at the wash-house bench (`ECN-D1`): the brass has been going all season; twenty households signed a complaint; he handed it in at the Cinderwatch post; nothing. He wants the brass back and the complaint heard.

**Beat 1: The Trail (`S01_trail`).** *Objective: Find where the Commons brass went.* Three required inspects along the Commons runs (N2, `ECN-I1`): bright scratches, fresh, the same pry-bar width each time. One living witness (optional, any order): a **lamp-lighter** on the lane who has seen "two with a hand-cart, nights, one wheel that clacks" (`ECN-B1.03`). On the slag lane (N3): the **rut** (inspect `ECN-I2`: a cart with one wobbling wheel, heavy going toward the Dross, light coming back) and a **wash cock** half-buried in it (pick up: carry-state; `ECN-I3`: the cup stamp). Grisel's line on the stamp sets the next lead: "That's ours. Now ask the Watch what they did with our sheet."

**Beat 2: The Wrong Door (`S02_post`).** *Objective: Find the ward's complaint.* At the Cinderwatch post (N4) the **Cinderwatch clerk** (`ECN-D2`), polite and harried: the Watch answers riots, accidents and surges; brass is none of those. Asked where the complaint went: he checks three trays and then, after a moment, the unlabelled one under the desk. It is there, under a season of other papers. He gives it up (it is the ward's) and admits nobody sent it on to the Overseer's court because "nobody said to". Carry-state: **the complaint** (twenty marks; `ECN-I4`). Sets `ECN_COMPLAINT`.

**Beat 3: The Weigh-Shed (`S03_slagside`).** *Objective: Find who bought the brass.* At Slagside (N5): **Ilsa Cleff** (`ECN-D3`), a scrap-weigher who weighs anything. The player shows the stamped cock (option gated on carrying it). She turns her **weigh-book** round (`ECN-I5`, read in place): a season of entries, *brass, pit lot*, by weight, every week. "I buy brass. I don't buy whose." Shown the complaint's twenty marks, she is quiet, then practical: the pit lot bury what they have not sold in the pits under slag "so the Watch can't see it shine". She will bring her book to the Overseer's court herself ("Books walk better with the one who wrote them."). She will not go to the pits.

**Beat 4: The Pits (`S04_pits`).** *Objective: Recover the Commons brass from the pits.*

1. **The mouth (N6):** the pit lot hold the cut (**ECN-E1**). Slag pools are hazard volumes (heavy periodic heat damage while inside; a glow under the crust shows them). The **slag mirror** (ECN.5) plays at the first pool the player passes after the fight.
2. **The basin (N7):** the rest of the pit lot at the cache (**ECN-E2**), with slingers on the two ledges.
3. **The cache:** the slag crust over it carries the pit lot's tell bead pressed in as a marker (`ECN-I6`: amber; the crust is still warm underneath). Two ways, both complete the step:
   - **Option A (skill): break it out** (**Mining ~[GD: low]**). Three crust nodes (EHC-03), each a pick interaction (~3 s; a short shower of cooled slag; on the third, the crust lifts). Inside, wrapped in sacking: the Commons brass (`ECN-I7`), including the diverter handle. Carry-state: **a sack of Commons brass**. `ECN_DIG` = self.
   - **Option B (time-cost): Slagside's diggers.** Mark the crust (interaction: chalk the bead) and tell Ilsa's diggers at the weigh-shed bench. **Keep watch** at the bench until morning (one turn); the diggers bring the sack, less a share of the cheap clamps they keep as their wage ("Diggers' share. The handle's in. Don't look at me like that."). `ECN_DIG` = diggers.

**Beat 5: The Court (`S05_court`).** *Objective: Take the case to the Overseer's court.* Court night at the Cooling House (N8; it opens on the player's arrival in this step; the presentation hour moves to dusk if earlier). Yorven at the end table with his **court book**; Grisel with the twenty households behind him; Ilsa with her weigh-book. Hennet serves anyway (`ECN-B5`). The player lays the case on the table (`ECN-D5`; options gated on carry-states): **the complaint**, **the stamped brass**, and calls **Ilsa** as the witness to the buying. Yorven reads it all into his book, aloud (`ECN-D5.20`): the loss; the buyer; the pits cleared; and a rule for the ward: *Commons complaints to the Overseer's book, not the Watch's tray.* Ilsa undertakes to refuse cup-stamped brass and to hand any she is offered to Grisel. Sets `ECN_CASE`. Nothing from the pits is evidence beyond the brass itself; the pit lot are not named (Yorven: "Persons at the pits. The pits are clear.").

**Beat 6: The Handle (`S06_refit`).** *Objective: Refit the Commons brass.* With Grisel at the tee (EWA C5), fit the **diverter handle** (a 2-segment channel); then two wash cocks at the wash-house (one interaction each). Grisel (`ECN-D6`) keeps the rest for the lanes "and the table at First Cooling, if this ward ever has one again". Quest Completed; EFC offered when EH-M2 is also Completed (otherwise Hennet's bark waits for it, `ECN-B6.3`).

### ECN.5 The slag mirror (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Trigger** | First slag pool the player passes after ECN-E1. The pool's crust is thin and glassy. |
| 0–3 s | **Reflection** | The player's own face and shoulders show in the crust, dark and wavering, lit orange from below. |
| 3–5 s | **Crack** | A line runs across the reflection; the crust crazes like a red tell's skin and sinks with a soft sound. Heat rolls up (no damage outside the pool). |
| After | **Nothing** | No line from anyone. If asked later, Grisel: "Slag does that. Don't look in it. That's all the Dross knows." |
| Meaning | Cooling glass on slag. Proves nothing; is not the Embermind Echo and shows nothing but the player. |

### ECN.6 Encounters and hazards

Tuned for EH-M2's Advanced identity (ED-10). Dross Scavengers use the bible §10 kit as Act III EGA-E1 (same telegraphs), at a lower tier.

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **ECN-E1** | 3 × Dross Scavenger **scavenger**, 1 × **slinger** | The pits mouth (N6) | Scavengers hold the cut with pry-bars; the slinger on the lean-to roof (a ladder reaches it) | **Scavenger, Bar:** pry-bar lifted overhead (~1.0 s), then an overhead strike. **Scavenger, Shove:** shoulder dips, feet set (~1.5 s), then a shove and one-step knock-back (it stops at a pool's crust edge, never inside: watch the glow). **Slinger, Whirl:** sling whirls with a glowing slag pellet in the cup (~1.4 s), then a shot that leaves a burning patch ~4 s. **Slinger, Reload:** ~2.5 s visible reload (the window to close). | The pit lot at their door; pools as terrain | 60–90 s; 65–85% HP |
| **ECN-E2** | 2 × scavenger, 2 × slinger | The cache basin (N7): scavengers on the floor, a slinger on each ledge | Floor scavengers press; slingers alternate from the ledges | As ECN-E1. The ledges are reached by ramps in ~4 steps; the basin's cooling niche gives melee players a place between volleys. | The challenge: crossfire on open slag | 90–120 s; 55–75% HP |
| **ECN-H1** | Slag pools | N6, N7 | Hazard volumes | A dull glow under the crust; inside: heavy periodic damage | Terrain; no knock-back ends inside one | — |
| **ECN-H2** | Vent grates in the slag | N6 | Timed hazard | Ash lifts ~1.5 s before each exhale (~12 s) | Vent breath reused | — |

**Rules.** Every scavenger fights to 0 HP and takes the ordinary defeat presentation; none flees, yields or drops a document. No scavenger speaks after a fight (pre-fight barks only, `ECN-B4`). Ranged players duel slingers from the basin floor; melee players climb the ramps; no ledge is unreachable on foot (CDR-2: ranged never trivialises or is required). The cache is found by Ilsa's directions and the bead in the crust, never as loot. **Death:** respawn at the Slagside bench (N5); defeated scavengers stay defeated; a broken crust node stays broken.

### ECN.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Hear the Commons fitter out. | `ECN-D1` accept | Yes | — |
| `S01_trail` | Find where the Commons brass went. | 3 bracket inspects + rut inspect + wash cock picked up | Yes | Lamp-lighter optional |
| `S02_post` | Find the ward's complaint. | `ECN-D2` end (complaint given) | Yes | Sets `ECN_COMPLAINT` |
| `S03_slagside` | Find who bought the brass. | Weigh-book inspect + `ECN-D3` end | Yes | Needs the stamped cock carried |
| `S04_pits` | Recover the Commons brass from the pits. | ECN-E1 and ECN-E2 defeated + cache opened (Option A) **or** crust marked + keep watch to morning (Option B) | Yes | Sets `ECN_DIG`; slag mirror plays once |
| `S05_court` | Take the case to the Overseer's court. | `ECN-D5` end | Yes | Sets `ECN_CASE`; court book prop updates |
| `S06_refit` | Refit the Commons brass. | Handle fitted + 2 cocks fitted + `ECN-D6` end | Yes | Small payment; quest Completed; EFC offer if EH-M2 Completed |

| Flag | Set by | Read by |
|---|---|---|
| `ECN_COMPLAINT` | `S02` | `ECN-D5` options |
| `ECN_DIG` = self / diggers | `S04` | `ECN-D6.12` |
| `ECN_CASE` | `S05` | Court book prop; EFC `EFC-D3.20` |

### ECN.8 Choices and consequences

None (contract). The court always hears the case and the brass always comes home. `ECN_DIG` changes one Grisel line (whether the diggers' share is missing from the sack).

### ECN.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Small payment | Currency | From Yorven's court purse ([GD]). |
| Ilsa's weigh-shed | Access | A scrap buyer at Slagside (economy pass decides what she buys). She refuses cup-stamped brass. |
| Yorven's court book | Inspect | Shows the Commons case, and later cases if other packages add them. |
| Mining, Melee or Ranged XP | Action XP only [GD] | Less Mining XP on the diggers' path. |
| EFC | Story | With EH-M2 Completed. |

### ECN.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Goes to Slagside before the trail | Ilsa will weigh the player's scrap and talks about prices; no step advances until the stamped cock is carried. |
| Goes to the pits before Ilsa | The pits are open and the fights happen; the crust bead reads as "a bead in slag" and cannot be broken until `S03` is done (prompt: "You don't know what's under it."). Defeats are kept. |
| No Mining | Option B: one keep-watch turn and a share. Never blocked. |
| Death | Respawn at the Slagside bench (N5). Defeats, crust nodes and carry-states kept. |
| Logout | Restore to the step: the wash-house (`S00`, `S06`), the lanes (`S01`), the post (`S02`), Slagside (`S03`, `S04`), the Cooling House (`S05`). A dropped carry-state returns to its source (the cock to the rut, the complaint to the post's desk, the sack to the cache). |
| Walking away | Stays Active; resume at Grisel (`ECN-D1.00`). |
| Co-op | Shared fights; each partner gets defeat credit only if their own `S04` consumes it. The trail, complaint, weigh-book, cache and court are per player. A partner's court night does not complete another's `S05`. |

### ECN.11 Integration needs

All standard: slag pools as hazard volumes with a glow under a crust; a per-player slag-mirror material with a craze-and-sink animation; quest-local Mining crust nodes gated on `S03` (EHC-03); a keep-watch bench at Slagside that places the diggers' sack at morning; a court-night NPC placement variant in the Cooling House (per player); a court-book prop updated by `ECN_CASE`; Dross Scavenger scavenger and slinger (bible §10).

### ECN.12 Mystery ledger entry

None (resolved in-quest). The pit lot are shown only as pipe-strippers; this quest gives them no affiliation and neither uses nor contradicts the dossier's "clandestine Remnant scavengers" label.

### ECN.13 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Grisel Tamm** [NEW], Commons fitter | Every Commons fitting in Cinderwall by its stamp; who signed the complaint; how long it has been. | Where it went. | Old, dry, patient until he isn't. Talks to pipes. "Warden's hand." |
| **Ilsa Cleff** [NEW], Slagside scrap-weigher | Weights; prices; the pit lot by sight; where they bury. | Who the brass belonged to (until shown). | Flat, quick, honest about being dishonest. Never sentimental; once, nearly. |
| **CINDERWATCH CLERK** (role) | The three trays. | Where a ward complaint should go. | Polite, harried, not unkind. |
| **Yorven Khelt** [CANON ANCHOR] | His ward; his book. | — | Loud, plain, fair; jokes that are orders. Limits: no knowledge of the precursor or the draw. |
| **LAMP-LIGHTER**, **DIGGER**, **SCAVENGER**, **SLINGER** (roles) | — | — | Short. |

**Offer** (`ECN-D1`)

```
ECN-D1.00 [quest Active, returning] GRISEL: "Brass is still gone and I'm still old. Where are we?"   (pins step) → end
ECN-D1.01 GRISEL: (to the diverter's empty socket, through the hatch) "Somebody had your handle off with a bar. Two goes. First go slipped." (to the player) "Warden's hand."
ECN-D1.02 GRISEL: "It's not just the handle. Wash cocks. Bath taps. Bracket clamps off half the lanes. All brass. All ours. Every one's got the cup on it."
ECN-D1.03 GRISEL: "A season back, twenty houses put their marks on a sheet. I took it to the Watch post on the slag lanes myself. In my good coat."
ECN-D1.04 GRISEL: "Nothing. Not a word. Not a no."
  > "I'll find the brass."                                           → ECN-D1.10
  > "Why the Watch?"                                                 → ECN-D1.20
  > "Not now."                                                       → ECN-D1.30
ECN-D1.10 GRISEL: "Find the brass and find the sheet. I want both on a table in front of somebody who has to write it down."   {event: accept → S01_trail} → end
ECN-D1.20 GRISEL: "Because they've a post and a desk and a brazier. Looked official. Turns out looking official's a skill too."   → ECN-D1 options
ECN-D1.30 GRISEL: "It's been a season. It'll be a season and a day."   → end (offer stays open)
```

**The trail**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ECN-B1.03 | Lamp-lighter, if asked | LAMP-LIGHTER | "Two with a hand-cart, nights. One wheel clacks. I thought they were your lot, fixing." |
| ECN-B1.04 | Wash cock picked up | GRISEL (when next spoken to) | "That's ours. Now ask the Watch what they did with our sheet." |

**The Cinderwatch post** (`ECN-D2`)

```
ECN-D2.01 CLERK: "Cinderwatch. Riots, accidents, surges. Which?"
  > "A complaint. Twenty marks. A season ago."                       → ECN-D2.02
ECN-D2.02 CLERK: "Brass?" (beat) "We don't do brass. Brass isn't a riot." (checks Riots, Accidents, Surges) "No."
  > "What's under the desk?"                                         → ECN-D2.03
ECN-D2.03 CLERK: (pulls out the unlabelled tray; a season of paper; he goes through it slowly) "...Cinderwall Commons. Twenty marks." (beat) "It's here."
ECN-D2.04 CLERK: "It should've gone to the Overseer's court. Nobody said to send it. Nobody said not to." (holds it out) "It's the ward's. Take it."   {give complaint (carry-state); set ECN_COMPLAINT} → end
```

**The weigh-shed** (`ECN-D3`)

```
ECN-D3.01 ILSA: "Scrap? On the scale. I pay by weight, not by story."
  > [carrying the stamped cock] "Recognise this?"                    → ECN-D3.02
ECN-D3.02 ILSA: (weighs it in her hand without the scale) "Brass. Good brass." (turns it) "...That's the cup."
ECN-D3.03 ILSA: (turns the weigh-book round on its nail) "Brass, pit lot. Every week this season. By weight." (beat) "I buy brass. I don't buy whose."
  > [ECN_COMPLAINT] (show the complaint)                             → ECN-D3.04
  > "Where do they keep what they haven't sold?"                     → ECN-D3.05
ECN-D3.04 ILSA: (reads the marks; a long breath) "Twenty houses." (beat) "Some of those marks buy their kettles off me."   → ECN-D3.05
ECN-D3.05 ILSA: "Pits. They bury it under slag so the Watch can't see it shine. Not that the Watch looks. There's a bead in the crust where it is."
ECN-D3.06 ILSA: "I'm not going down there. My diggers will, for a share, if you want it done for you."
ECN-D3.07 ILSA: "And if your Overseer wants to read this book, I'll bring it myself. Books walk better with the one who wrote them."   → end
```

**The pits** (pre-fight barks only)

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ECN-B4.01 | Player seen at the mouth | SCAVENGER | "Warden's lot. Brass is ours. Pipe's ours too, if you're slow." |
| ECN-B4.02 | Player seen | SLINGER | (whirling) "Off the crust!" |
| ECN-B4.03 | Player enters the basin | SCAVENGER | "That's the dig. Nobody digs but us." |
| ECN-B4.04 | Last scavenger defeated | (none; the basin goes quiet except the pools' hiss) | — |
| ECN-B4.10 | Option B, morning, at the bench | DIGGER | "Diggers' share. The handle's in. Don't look at me like that." |

Production rule: no scavenger speaks after any fight; nothing in the basin but the cache under the crust (CDR-1 §3.1.3; combat never reveals evidence).

**The court** (`ECN-D5`, step `S05_court`)

```
ECN-D5.01 YORVEN: (court book open; loud enough for the back benches) "Court night. Commons first, Grisel says, and Grisel's older than me. Warden's hand. What've you got?"
  > [ECN_COMPLAINT] (lay the complaint on the table)                 → ECN-D5.02
ECN-D5.02 YORVEN: (reads; counts the marks under his breath) "Twenty. A season ago." (to the room) "Who had this?" GRISEL: "The Watch's tray." YORVEN: "The Watch's tray." (beat) "We'll come back to that."
  > [carrying the brass] (lay the brass on the table)                → ECN-D5.03
ECN-D5.03 YORVEN: (holds up the diverter handle; the cup stamp to the room) "Commons." (sets it down) "Where?"
  > "Bought by weight at Slagside. Ilsa Cleff will say so."          → ECN-D5.04
ECN-D5.04 ILSA: (steps up; opens the weigh-book on the table) "Brass, pit lot, every week. I bought it. I didn't ask whose." (beat) "I'm asking now."
ECN-D5.10 YORVEN: "Right." (writes, aloud) "Commons of Cinderwall: brass taken off the lanes this season. Bought by weight at Slagside, the buyer here and honest about it. The brass recovered from the pits. Persons at the pits. The pits are clear."
ECN-D5.20 YORVEN: (still writing) "And this: Commons complaints come to the Overseer's book. Not the Watch's tray. Not any tray." (looks up) "If a sheet sits a season again, I want to know whose desk it sat under."
ECN-D5.21 ILSA: "I'll not take cup-stamped brass. Anyone brings it, Grisel gets it."
ECN-D5.22 YORVEN: (closes the book) "Done. That's a case. It took a season and a stranger, and it's done." {set ECN_CASE} → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ECN-B5.01 | Court night begins | HENNET | "Court or no court, it's soup first." |

**The refit** (`ECN-D6`)

```
ECN-D6.01 GRISEL: (at the tee, handing the handle over) "Square shank. Push, don't hammer. It's been hammered enough."
ECN-D6.10 (Handle fitted.) GRISEL: (pats the pipe) "There you are."
ECN-D6.12 [ECN_DIG = diggers] GRISEL: "Short three clamps. Diggers' share. Fair's fair. I've got clamps." / [ECN_DIG = self] GRISEL: "All of it. You dig like a miner. Yorven'll be jealous."
ECN-D6.20 GRISEL: "Rest goes back on the lanes. And some on the table at First Cooling, if this ward ever has one again." (beat) "Hennet thinks we should."   {small payment; event: ECN-D6 end → quest Completed}
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ECN-B6.3 | ECN Completed, EH-M2 not Completed | HENNET | "First Cooling wants you. When you've done your business up the Stair." |

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| ECN-I1 | Stripped bracket | "Bright scratches in old soot. A bar's width. The clamp is gone; two bolt holes stare." | — |
| ECN-I2 | The rut | "Two wheels in the ash. One wobbles. Deep going toward the Dross, shallow coming back." | — |
| ECN-I3 | Wash cock | "A brass wash cock, a cup struck into its body. Ash in its mouth." | — |
| ECN-I4 | The complaint | "*Commons of Cinderwall. Brass taken off our lanes: cocks, taps, clamps, the diverter. Twenty houses.* Twenty marks: names, initials, a drawn cup, a thumb." | — |
| ECN-I5 | Weigh-book | "Weekly lines in a cramped hand: *brass, pit lot*, and a weight, all season. Other lines: *iron, Dross crew*; *copper, kettle (old)*." | — |
| ECN-I6 | Crust bead | "A tell bead pressed into the slag. Amber. Warm underneath." | `EH_TELLS` |
| ECN-I7 | The cache | "Sacking round brass: cocks, clamps, taps, a square-shanked handle. Every one with the cup." | — |
| ECN-I8 | Yorven's court book (after) | "*Commons of Cinderwall...* in Yorven's big hand, and under it, ruled off: *Commons complaints to the Overseer's book.*" | `ECN_CASE` |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| GRISEL | "Handle's still on. I check." | ECN Completed |
| ILSA | "Got offered a cup tap yesterday. Sent him to Grisel. He didn't go." | ECN Completed |

### ECN.14 Open decisions

1. **Yorven's ward court [NEW]:** the bible says the complaint "reaches Yorven's book". This package makes the book a court book read aloud on a court night. If the Director prefers no court, Yorven enters it at his strongbox in a short scene; `ECN_CASE` is unchanged.
2. **Dross Scavengers and the dossier label:** the dossier calls some Dross scavengers "clandestine Remnant scavengers". This file follows the bible's plain pipe-strippers and gives them no affiliation. If a later package wants the label, it must bring its own evidence; nothing here supports or denies it.
3. **Mining `[GD: low]`** on a quest-local slag node: Gameplay Designer.

### ECN.15 Review log

| Finding | Revision |
|---|---|
| First draft had the pit lot's leader confess where the brass went. | Cut (rulings §3.2): Ilsa, a living witness with her book, says where; the bead in the crust confirms. No scavenger speaks after a fight. |
| The Cinderwatch clerk risked being a villain. | He is harried and sorting by tray; the fault is the door, and Yorven fixes the door. |
| Ranged could trivialise the ledges. | Each ledge has a ramp in ~4 steps; slingers are duelable from the floor; melee has the niche. |
| Contract "crew-recovered next morning". | Option B: Slagside diggers, one turn, a share. |

---
---

## EFC — First Cooling

### EFC.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.first_cooling` |
| Type | Festival. Heat Commons 3/3 (bible §7.1). |
| Unlock | ECN Completed **and** EH-M2 Completed. Offered by Hennet Ulm at the Cooling House hatch (`EFC-D1`). |
| Resume hook | Hennet at the hatch: `EFC-D1.00` "Pot's on. Ward's arguing. Where were we?" pins the step. |
| Skills | Cooking ~[GD: low] (hook; Hennet's hatch as the alternative) |
| Combat share | 0% (contract: none) |
| Cameo | Veska, Yorven, Dunya, Grisel; Jessa and Tavi Ostry; Hesper Tolk (only if EH-M3 Completed); Ralenne's clerk (`[ALLOCATION]`, settled only) |
| Choice | Plain or bright (`EFC_LIGHT`); flavour. The dimming happens in both. |
| Unlocks | **Sets `EH_COMMONS`** (bible §9.1): the Commons rota takes on the warming house (read by EH-M6 `S01`); Hennet's pot nights (barks) |
| **Anchor** (§7.1) | Cinderwall households |
| **World-truth row** | H23 |
| **Revelation role** | None. |
| **Recurring evidence** | None (contract). |
| **State compliance** | Inactive / Active / Completed. `EH_COMMONS` set on completion in every outcome; the festival always completes. |
| **Combat compliance** | None. No enemy appears. Every person present is a non-combatant and never targetable. CDR-6 solo test: every step is one player's; no step needs a partner. |

**In one paragraph.** Cinderwall keeps **First Cooling** the first night its Commons runs full after the year's mending: lowered flames, repaired work shown in public, a meal before names. **Hennet Ulm** wants it plain; **Sorrel Vamm** and the young want it bright, with flame-weaving on the lane. The warden's hand gathers what each house can put in the pot, cooks it on the Cooling House hearth by its tell (amber simmers, red scorches) or works Hennet's hatch, and carries the year's mended work to the Commons table. The ward lights the lane plain or bright and eats. Before the names every lamp goes down a notch and the hood tells down the lane go from amber to clear, house by house. Hennet reads the year's names; a child relights the first lamp; and Yorven chalks the Commons rota on the store door: the warming house is the Commons' job now.

### EFC.2 Selection record and canon grounding

Selected shape: Gather from the lanes → cook the pot by the hearth tell (or the hatch) → carry the mended work → plain or bright → the meal before names, dimmed flames, a ripple of tells → a child's first light.

| Element | Source | Status |
|---|---|---|
| First Cooling: lowered household flames, repaired work shown in public, a meal before names; street meals, supervised flame weaving, a child's first safe ignition | Part 3 Emberholt proposal; bible §1.2, §7.1, ED-13 | [PROPOSAL — DIRECTOR] ED-13; [NEW] detail |
| Mourning rites where flames are dimmed instead of extinguished | Dossier §XVI | [CANON] |
| The dimmed flame (EME03); warm stones (EME07) | Bible §7.4 | [NEW] |
| Children light lanterns by touch; the Cinderweave Quarter hosts the largest festivals | Dossier §III, §VII.2 | [CANON] |
| Heat follows the room | Bible §1.1 | [NEW], consistent |
| "Kept the first night the Commons runs full after the year's mending" | This package (bible: "the first night the heat is shared fairly") | [NEW] |
| Sorrel Vamm | This package | [NEW] |

### EFC.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **F1. The Cooling House** (Act I W2) | Offer; the pot; the names | Benches pushed into two long rows. The **hearth** under the brass hood with its **tell**. Hennet's **hatch**. The board (EH-M1 outcome on it). A box of lamp-wicks. |
| **F2. The lane** | Gathering; plain or bright; the ripple | Cinderwall's Cooling House lane: a dozen doors, each with a brass **vent hood** and a **hood tell** over the lintel, and a doorway lamp. Mood banners (EME02). At the lane's end, the Commons store and the wash-house (EWA). |
| **F3. The Commons table** | Mended work | A trestle in the lane outside the Cooling House door, under a strung line of lamps. |
| **F4. The Commons store** (Act III W4) | Carry | Shelves of blankets and a **rota slate** on the door; the year's mended things in a crate. |

### EFC.4 Beats

**Beat 0: Plain (`S00_offer`).** *Objective: Talk to Hennet about First Cooling.* `EFC-D1`. Hennet wants it kept, and plain: "Lamps down, food out, names read. That's First Cooling." Sorrel Vamm, at the next bench, wants it bright. Hennet: "Help me get a pot on and we'll argue after."

**Beat 1: The Lanes (`S01_lanes`).** *Objective: Gather what the lanes can give.* Four doors on the lane (F2), any order; each is a short exchange and a carry (bark-sized dialogue, `EFC-B1`): an onion string from the lamp-lighter's house; a **smoked rib** from a forge hand's door; a **twist of salt** from Grisel (who also hands over the crate key: "Mended things are in the store"); **barley** in a kettle from the old man with the kettle (EWA). Each household says one thing about its year (a line, not a list). The four contributions are one carry-state basket.

**Beat 2: The Pot (`S02_pot`).** *Objective: Get the Commons pot cooking.* At the Cooling House hearth (F1). Two ways, both complete the step:

- **Option A (skill): cook it** (**Cooking ~[GD: low]**; EHC-04). **Brown** the rib in the pot (one interaction, ~3 s); **add** onion and barley (one interaction); **water** from the hearth kettle (one interaction); **simmer** by the hearth tell: the pot must sit at **amber** for three short holds (a 3-segment channel at the hearth damper, ~4 s each). The tell drifts toward **red** if the damper is left open; a red hold is **refused** ("Never cook on a red. Hennet's rule, not Dunmor's.") and the player closes the damper a notch to bring it back to amber (one interaction). Nothing burns past saving. **Season** with Grisel's salt (one interaction). Hennet tastes it: `EFC-D2.10`.
- **Option B (time-cost): Hennet's hatch.** Hennet cooks; the player stands at the hatch and hands out the first bowls through one turn of the presentation hour (dusk; one keep-watch-style interaction at the hatch with three bowl hand-outs prompted by REGULARS).

**Beat 3: The Year's Work (`S03_work`).** *Objective: Set the mended work on the Commons table.* With Grisel's crate key, carry the **crate** from the Commons store (F4) to the Commons table (F3) (carry-state; walk, cannot attack), then set out **three** things from it (one interaction each), with a line from whoever mended it (`EFC-D3`): the **diverter handle** (Grisel; `ECN_CASE` line), the **float cup** (Dunya; `EWA_ROTA` line), and a **patched mitt** (a lane child's, mended by her grandmother). With `EH_COLD_WARD` `[ALLOCATION]`, one more thing comes to the table (`EFC-D4.10`/`.11`): posted, Hennet takes Veska's cut page down from the board and lays it on the table to read later; settled, a clerk from the Magistrix's office arrives with the coal book and lays it open at the season's coal.

**Beat 4: Plain or Bright (`S04_light`).** *Objective: Decide how the lane is lit.* Hennet and Sorrel put it to the warden's hand (`EFC-D4`). The choice (EFC.8) sets `EFC_LIGHT`. **Plain:** doorway lamps only, lit by each house; the lane is warm and low. **Bright:** Sorrel and four of the young weave a ribbon of flame along the lane under Veska's eye (supervised; NPC craft, never the player's: bible §11.8), then let it go to the doorway lamps. Either way the lane fills and the pot is served.

**Beat 5: The Meal Before Names (`S05_names`).** *Objective: Sit for the names.* Take a bowl and **sit** (interaction at a bench). The **dimming (EFC.5)** plays: every lamp in the room is turned down one notch (EME03; the player may turn the nearest one down or not), and the ripple runs down the lane. Hennet reads the year's names of Cinderwall's dead (`EFC-D5`): four ordinary names (a slag hand, a grandmother, a baby who did not see the spring, a man who fell on the lanes in the frost of the cold-ward nights). **If EH-M3 is Completed** (`EH_HOLLOW_TRUTH` set): Hesper Tolk stands and names her brother, Lorcan, and his crew by their first names (`EFC-D5.20`), and says nothing about where or why; the room turns its lamps down one more notch and back. Warm stones (EME07) pass along the bench.

**Beat 6: First Light (`S06_first_light`).** *Objective: Bring the lamps back up.* A child relights the first lamp (by custom, a child who has learned the touch this year). Jessa has brought **Tavi** (EH-M2 is a prerequisite): Hennet asks her. The player holds the **draught shield** round the lamp while she lights it (a 2-segment channel, ~3 s each, the EH-M2 shield action). Tavi lights it with two fingers on the second try, and laughs; the lamp steadies (`EFC-D6`). Every house brings its lamp up a notch after it, door by door. Jessa's line reads `EH_CURRICULUM` (`EFC-D6.10`/`.11`). Yorven: "Commons rota." He chalks the store door's slate: *Warming house: Commons*. Sets **`EH_COMMONS`**. Quest Completed.

### EFC.5 The dimming (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Hennet's ladle** | One tap on the hood. The room goes quiet. |
| 0–4 s | **The notch** | Every lamp in the Cooling House goes down one notch, hand by hand, from the hatch end to the door. The player's nearest lamp offers a prompt (turn it down or leave it). |
| 4–10 s | **The ripple** | Through the open door and down the lane: each house's **hood tell** goes **amber → clear** in turn, door by door, as the houses go quiet (heat follows the room). The last, at the lane's end, is the wash-house cistern's coil tell. |
| 10–14 s | **The hum** | With every hearth banked, the ward is quiet enough to hear the main hum under the street. Nobody speaks. |
| After | **Hennet** | Begins the names (`EFC-D5`). |
| UI | None. Camera stays with the player. |
| Meaning | A calm room lowers its heat (bible §1.1). Proves nothing. |

### EFC.6 Encounters and hazards

None. The hearth's red state (Option A) is a refusal, never damage.

### EFC.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to Hennet about First Cooling. | `EFC-D1` accept | Yes | Gate: ECN Completed and EH-M2 Completed |
| `S01_lanes` | Gather what the lanes can give. | 4 contributions collected | Yes | Any order; one basket carry-state |
| `S02_pot` | Get the Commons pot cooking. | Pot cooked and seasoned (Option A) **or** hatch turn (Option B) | Yes | Hearth tell amber for the simmer; red refused |
| `S03_work` | Set the mended work on the Commons table. | Crate carried + 3 items set + `EFC-D3` end | Yes | `[ALLOCATION]` addition by `EH_COLD_WARD` (`EFC-D4.10`/`.11`) |
| `S04_light` | Decide how the lane is lit. | `EFC-D4` choice | Yes | Sets `EFC_LIGHT` |
| `S05_names` | Sit for the names. | Sit interaction + dimming event + `EFC-D5` end | Yes | Hesper's line only if `EH_HOLLOW_TRUTH` is set |
| `S06_first_light` | Bring the lamps back up. | Shield channel + `EFC-D6` end | Yes | Sets **`EH_COMMONS`**; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `EFC_LIGHT` = plain / bright | `S04` | Lane props on later First Cooling barks; barks |
| **`EH_COMMONS`** (true) | `S06` (completion) | EH-M6 `S01` (`EGA-D2.30`): the warming house opened and cots laid by the Commons rota |

### EFC.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Plain** (`plain`): *"Lamps down, food out, names read. Hennet's way."* | Doorway lamps only. A low, warm lane. | Sorrel and the young are disappointed and say so; two of them weave a small flame at the lane's end anyway, and Veska lets them. | Barks: Hennet content; Sorrel "next year". |
| **Bright** (`bright`): *"Let them weave it. Then bring it down for the names."* | Sorrel's ribbon of flame runs the lane under Veska's eye, then settles into the doorway lamps. | Hennet grumbles that grief should not have a show; the old ones like it more than he thought. | Barks: the young ask the warden's hand to come next year; Hennet admits it "looked like the ward". |

No option is wrong. The dimming, the names and the first light happen in both; `EH_COMMONS` is set in both.

### EFC.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| A seat and a bowl | Food | A bowl of the Commons pot (EHC-04), eaten in place; a second to carry ([GD]). |
| `EH_COMMONS` | World state | The Commons rota opens the warming house in EH-M6 (`EGA-D2.30`). |
| Cooking XP | Action XP only [GD] | Option A only. |
| Hennet's pot nights | Barks | The Cooling House hearth gains "pot night" ambience on later evenings. |

### EFC.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Pot drifts red | Refused hold; close the damper a notch; nothing burns. |
| No Cooking | Option B at the hatch; one turn. |
| Leaves mid-festival | Stays Active; the festival waits at the step (NPC placements persist per player). Resume at Hennet. |
| Death | No combat; heat hazards none. If the player dies elsewhere, they respawn at the Cooling House with the step intact. |
| Logout | Restore to the step at the Cooling House or the lane; the basket or crate returns to its source. |
| Co-op | Each player gathers, cooks, sets and chooses their own; a partner may sit at the same bench. The dimming, the ripple and the first light play per player. A partner's `EFC_LIGHT` never sets yours; `EH_COMMONS` is set per player on their own completion. |

### EFC.11 Integration needs

All standard: a Cooking interaction whose damper steps the hearth tell amber/red (red refuses the hold); a per-player lamp-notch event across the room and lane with an optional prompt on the nearest lamp; a lane hood-tell ripple (amber to clear in sequence, ~6 s); festival NPC placements for `S03`–`S06`; an NPC-performed flame ribbon for `bright` (no hazard); EH-M2's draught-shield channel; the store-door slate prop after `EH_COMMONS`.

### EFC.12 Mystery ledger entry

None.

### EFC.13 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Hennet Ulm** [NEW, bible §5.2] | Every soup order; every name to be read. | — | Feeds first; bangs a ladle. Wants it plain because plain is what his mother did. |
| **Sorrel Vamm** [NEW], a young lane weaver (about eighteen) | Flame-weaving from Cinderweave festivals; the young's mood. | Why Hennet minds. | Quick, eager, half laughing, serious about the dead in a way that surprises Hennet. |
| **Jessa Ostry** [NEW, bible §5.2]; **Tavi Ostry** [NEW; a child, never targetable] | As EH-M2. | — | As Act I. Tavi asks questions back. |
| **Hesper Tolk** [NEW, bible §5.2] | Her brother. | — | Wants somewhere to stand. Says names only. |
| **Yorven**, **Veska**, **Dunya**, **Grisel** | As above. | — | As above. |
| **CLERK** (Magistrix's office) `[ALLOCATION]` | The coal book. | — | Embarrassed in Cinderwall. |

**Offer** (`EFC-D1`)

```
EFC-D1.00 [quest Active, returning] HENNET: "Pot's on. Ward's arguing. Where were we?"   (pins step) → end
EFC-D1.01 HENNET: "Water's hot. Brass is back. Court's sat." (bangs the ladle on the hood, gently) "That's a year mended. That's First Cooling."
EFC-D1.02 HENNET: "Lamps down, food out, names read. That's all it is. That's all it ever was."
EFC-D1.03 SORREL: (from the next bench) "That's all it ever was because nobody's let us do it properly."
EFC-D1.04 HENNET: "Properly." (to the player) "She wants flames on the lane. Weaving. Like Cinderweave."
  > "I'll help."                                                     → EFC-D1.10
  > "What's First Cooling for?"                                      → EFC-D1.20
  > "Not now."                                                       → EFC-D1.30
EFC-D1.10 HENNET: "Then go round the lanes. Every house puts something in the pot. Then we'll argue."   {event: accept → S01_lanes} → end
EFC-D1.20 HENNET: "You turn your flame down for the ones who went this year. You show what you mended. You eat before the names, because names on an empty belly are cruel."   → EFC-D1 options
EFC-D1.30 HENNET: "It's been a cold year. It can wait a night."   → end (offer stays open)
```

**The lanes** (barks, step `S01`)

| Id | Door | Speaker | Line (on giving) |
|---|---|---|---|
| EFC-B1.01 | Lamp-lighter's house | LAMP-LIGHTER | "Onions. I lit every lamp on this lane through the cold and none of them took." |
| EFC-B1.02 | Forge hand's door | FORGE HAND | "Smoked rib. Washed before I cut it. Tell Dunya." |
| EFC-B1.03 | Grisel's door | GRISEL | "Salt. And the store key. Mended things are in the crate. Don't drop the handle; I've had enough of that handle." |
| EFC-B1.04 | The old man's door | OLD MAN | "Barley. In the kettle. The kettle comes back." |

**The pot** (`EFC-D2`)

```
EFC-D2.01 [Option A] HENNET: "Brown the rib. Then the rest. Then keep her at amber. Never cook on a red. That's my rule, not Dunmor's."
EFC-D2.02 [hearth tell red] HENNET: "Red. Damper. One notch. There."
EFC-D2.10 HENNET: (tastes) "...That's a ward pot." (beat) "Too much salt. Grisel always gives too much salt. It's right."
EFC-D2.20 [Option B] HENNET: "Hatch, then. Bowls out, smiles optional. I'll stir."
```

**The year's work** (`EFC-D3`, step `S03`)

```
EFC-D3.01 (The crate on the table.) HENNET: "Three things. Somebody mended each. They'll tell you."
EFC-D3.10 (The float cup.) DUNYA: "Cup off the cistern float. Cold killed the old one."
EFC-D3.12 [EWA_ROTA = shifts] DUNYA: "Shifts wash first now. Forge hands smell of soap. It's unsettling." / [EWA_ROTA = households] DUNYA: "Houses wash in the mornings. My mornings are very loud." / [EWA_ROTA = board] DUNYA: "Lane by lane. I've worn out two chalks."
EFC-D3.20 [ECN_CASE] (The diverter handle.) GRISEL: "Off our diverter, into a pit, out of a pit, into Yorven's book, back on the diverter." (beat) "Most travelled handle in Cinderwall."
EFC-D3.30 (The patched mitt.) LANE CHILD: "Gran did it. It's ugly." GRAN: "It's warm."
```

**`[ALLOCATION]` addition** (`EFC-D4.10`/`.11`, during `S03`)

```
EFC-D4.10 [EH_COLD_WARD = posted] [ALLOCATION] HENNET: (takes Veska's cut page down from the board and lays it on the table) "That's mended work too. Her name. I'll read it later, after the others." VESKA: (from the door) "Don't."  HENNET: "I will."
EFC-D4.11 [EH_COLD_WARD = settled] [ALLOCATION] CLERK: (at the table, the coal book under his arm, opening it) "From the Magistrix's office. The season's coal for Cinderwall. She said to bring it and let it be read." YORVEN: "Then sit down and eat, and we'll read it."
```

**Plain or bright** (`EFC-D4`, step `S04`)

```
EFC-D4.01 HENNET: "Now we argue." SORREL: "Now we argue."
EFC-D4.02 SORREL: "Cinderweave weaves for its dead. A ribbon down the street, and then you let it go into the lamps. It's not a show. It's a way of saying it."
EFC-D4.03 HENNET: "My mother turned her lamp down and read the names. That's a way of saying it too."
EFC-D4.04 VESKA: (from the door) "If they weave, I'm watching the hoods. One red and it's lamps."
  > "Lamps down, food out, names read. Hennet's way."                → EFC-D4.20 {EFC_LIGHT = plain}
  > "Let them weave it. Then bring it down for the names."           → EFC-D4.21 {EFC_LIGHT = bright}
EFC-D4.20 SORREL: (a breath) "...Next year." HENNET: "Next year, you can ask me nicely."   → end
EFC-D4.21 HENNET: (a long look at the lane) "...Under Dunmor's eye." SORREL: (already running) "Under Dunmor's eye!"   → end
```

**The names** (`EFC-D5`, step `S05`)

```
EFC-D5.01 (The dimming, EFC.5.) HENNET: (ladle down; quiet) "Eaten? Good. Then the year."
EFC-D5.02 HENNET: "Adda Halloran, slag hand. Old Mother Mossa, who taught half this lane its letters. Little Bett, who didn't see the spring. Haldo Brune, on the lanes, in the cold nights."
EFC-D5.03 HENNET: (beat) "That's Cinderwall's year."
EFC-D5.20 [EH_HOLLOW_TRUTH is set] HESPER: (standing at the back) "Lorcan Tolk. Tobbe. Wendel. Marit. Yeva." (she sits)   {event: room lamps down one more notch, then back}
EFC-D5.30 [EH_COLD_WARD = posted] [ALLOCATION] HENNET: "And one that isn't dead." (reads from the cut page) "Veska Dunmor, who said so in writing." VESKA: (from the door, very quietly) "Hennet." HENNET: "Year's done."
```

**First light** (`EFC-D6`, step `S06`)

```
EFC-D6.01 HENNET: "First light. A child who learned the touch this year." (looks along the benches) "Tavi Ostry. Come up."
EFC-D6.02 TAVI: (to the player) "Will you hold the shield? Idra says I'm too fast."
EFC-D6.03 (Shield channel; first try: a spark; second: the lamp takes.) TAVI: (laughs) "It took! Mum, it took!"
EFC-D6.10 [EH_CURRICULUM = guild] JESSA: "New lenses on the Stair this term. Her hands don't shake." 
EFC-D6.11 [EH_CURRICULUM = evidence] JESSA: "Same old lenses this season. She does it anyway. She's stubborn. She gets it from me."
EFC-D6.20 (Doors bring their lamps up, one by one.) YORVEN: (at the store door with chalk) "Commons rota." (writes) "Warming house: Commons. If it freezes, the rota opens it. Not me. Not the Watch. The rota."
EFC-D6.21 HENNET: "Sit down, warden's hand. You're running hot."   {set EH_COMMONS; event: EFC-D6 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| EFC-I1 | Hearth tell | "Amber. Working." / "Red. Crazed. Close the damper." | `EH_TELLS` |
| EFC-I2 | Commons table | "A trestle under strung lamps: a handle, a cup, a mitt" (+ "a cut page" with posted; + "an open coal book" with settled). | — |
| EFC-I3 | Store-door rota slate (after) | "*Warming house: Commons.* Yorven's chalk." | `EH_COMMONS` |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| HENNET | "Pot night. Sit." | EFC Completed, evening |
| SORREL | "Next year I'm asking nicely. And early." | `EFC_LIGHT = plain` |
| SORREL | "Old Mother Mossa's granddaughter cried at the ribbon. Good crying." | `EFC_LIGHT = bright` |

### EFC.14 Open decisions

1. **First Cooling's custom (ED-13):** "the first night the Commons runs full after the year's mending" is this package's reading of the bible's "first night the heat is shared fairly". The Part 3 "unapproved verse" is **not used**; no verse is sung.
2. **The year's names [NEW]:** four ordinary Cinderwall names with no war reference. Hesper's names reuse Act I's crew (Lorcan and four first names) and appear only if EH-M3 is Completed; they say nothing of where or why.
3. **`[ALLOCATION]`:** `EFC-D4.10`/`.11` and `EFC-D5.30` change with ED-1.
4. **Tavi as first light:** EH-M2 is a prerequisite, so Tavi is always present. If the Director prefers a Cinderwall child, any lane child takes the lines; Jessa's `EH_CURRICULUM` line is cut.

### EFC.15 Review log

| Finding | Revision |
|---|---|
| "Bright" risked player spellcasting. | The weaving is Sorrel's and the young's (NPC craft); the player holds a shield and chooses (bible §11.8). |
| Hesper's line risked R09 content. | Names only; no "collapse", no "Hollow", no cause. Only shown if EH-M3 is done. |
| `EH_COMMONS` reader. | Matches Act III `EGA-D2.30` text ("First Cooling did that"); the rota slate line uses the warming house. |
| Children are children. | Tavi laughs and asks; nobody calls her gifted. |

---
---
## EBL — The Ward That Answers Its Own Bell

### EBL.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.ward_that_answers_its_own_bell` |
| Type | Settlement (Cinderwall). Standalone (bible §7.2). |
| Unlock | EH-M1 Completed. Offered by Agathe Mund at the bell post on Bellwright's Lane (`EBL-D1`); Hennet's bark points there (`EBL-B0.1`). |
| Resume hook | Agathe on her stool at the post: `EBL-D1.00` "It rang again. I didn't. Where were we?" |
| Skills | Woodcutting ~[GD: low] (reclaimed crate-wood; hook); crew alternative |
| Combat share | 0% (contract: none) |
| Cameo | Veska Dunmor (the knot, the rule, her slate) |
| Choice | Keep the bell as the main's warning, or give it back to the shifts (`EBL_BELL`) |
| Unlocks | The bell post bench (keep watch); Agathe's and Wim's names cleared |
| **Anchor** (§7.1) | Cinderwall; fire wardens |
| **World-truth row** | H23 |
| **Revelation role** | None. The bell is a warden's knot from the cold-ward nights; nothing below is implied. |
| **Recurring evidence** | The bell valve (inspect in place) |
| **State compliance** | Inactive / Active / Completed. Keep or remove; no fail. The relief weight cannot be left at a red setting (refused); the stay has an overnight wait. |
| **Combat compliance** | None. No enemy appears; the relief spur is a light heat zone with a niche. CDR-6: every step is one player's. |

**In one paragraph.** Since the ward came back, Cinderwall's shift bell has been ringing by itself at night. The lane blames **Agathe Mund**, its bell-keeper; **Wim Kettering**, a carter, went out at a false bell and was docked a day. The warden's hand sits up and hears it: a hiss under the grate, then the rope pulls down with nobody there. A second line spliced into the rope runs down to a **relief valve** on the ward branch, tied to its lever with a warden's hitch. Veska knows it: on the third cold-ward night her line hand tied the relief to the bell so a lift would wake the crew, and nobody untied it. Now the ward banks its hearths at night, the branch peaks, the relief lifts, and Cinderwall answers its own bell (the player heard it once already, the night of the surge). The player replaces the cracked bell stay from reclaimed crate-oak or waits for one, sets the relief weight to the notch the tell approves at the night peak, and decides with Agathe whether the bell keeps the main's line as a warning.

### EBL.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. A hidden schedule from below (Part 3's later reading). | Rejected for this quest (bible §7.2 sets a forgotten valve; revelation role none). |
| **B. Night watch → the second line → the spur and the knot → Veska's witness → the stay (skill or wait) → the weight by the tell → keep or remove** | **Selected.** Listen, read, mend; a mechanical answer with a person behind it; two blamed people cleared. |

| Element | Source | Status |
|---|---|---|
| The ward that answers its own bell; a worker unfairly blamed | Part 3 Emberholt proposal, story 4 (first outcome only) | [NEW, adopted by bible §7.2] |
| Shift bells (EME06); the bell rings by itself after the surge | Bible §7.4; Act I `S06`, A14 item 6 | [NEW], consistent |
| Tells; "You don't shut hot"; "Never touch a red" | Bible §1.1; Act I | [NEW], consistent |
| Agathe Mund, Wim Kettering, Bellwright's Lane, the relief spur | This package | [NEW] |

### EBL.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **B1. The bell post** (Bellwright's Lane, Cinderwall) | Offer; night watch; the stay | A stone post with a small bell-cote; the **bell** on a headstock with a wooden **stay**; a long rope to a cleat. A **vent grate** at the post's foot. Agathe's **stool** and a bench (keep watch). Chalked on the post, new: *DRUNK*, half rubbed out. | — |
| **B2. The relief spur** | The knot; the weight | Off the Undercroft upper line by the stair head (Act I W3/U1). A short duct pinned **Working**; at its end, a **relief valve** on the ward branch with a **weighted lever** (three notches cut in it, a **tell** on the valve body), and a **line** running up a pipe to the grate. A cooling niche. | Ladder from the grate's access hatch; or the Undercroft stair |
| **B3. The forge gate** | Wim | The Emberforges' Cinderwall gate (EP25 edge): a gatekeeper's hut with a **docking slate**. | — |
| **B4. The Commons store** (Act III W4) | Crate-oak | A stack of reclaimed crate beams by the store wall. | — |

### EBL.4 Beats

**Beat 0: Drunk (`S00_offer`).** *Objective: Talk to the bell-keeper.* `EBL-D1`. Agathe: she has rung Cinderwall's shifts since the gate was rebuilt; she does not drink; the bell rings itself at night and the lane chalks *DRUNK* on her post.

**Beat 1: Night (`S01_listen`).** *Objective: Keep watch at the bell post at night.* Keep watch at the post bench to night (the step pins the night state). **The bell (EBL.5)** plays: a hiss under the grate, the rope pulls down, the bell swings. Then three short inspects (required): the **rope** (`EBL-I1`: a second line spliced in, running down through the grate), the **grate** (`EBL-I2`: warm air, a hiss before each ring), the **stay** (`EBL-I3`: cracked through). Two of three witnesses (optional for flavour, one required): **Wim Kettering** at the forge gate (`EBL-D2`; his docking slate: *Kettering: out early, gate blocked, a day*), the night baker (`EBL-B1.02`), or Hennet (`EBL-B1.03`).

**Beat 2: The Line (`S02_spur`).** *Objective: Follow the line down.* Through the grate's access hatch (or by the Undercroft stair). The spur is pinned **Working** (light periodic damage outside the niche; touch water). At its end, the **relief valve** (`EBL-I4`): the line is tied to its lever with a **warden's hitch**; the weight sits on the **inner notch**; the tell is amber now. Leave the knot as it is (cutting it now is refused: "Ask the warden whose hitch it is." `EBL-B2.2`).

**Beat 3: The Hitch (`S03_veska`).** *Objective: Ask the warden about the hitch.* At the junction (Act I U5) Veska (`EBL-D3`) recognises it before the player finishes: third cold night, the branch backing up with the junction shut, her line hand tied the relief to the bell "so the lift would wake us". "Then the ward came back. Nobody untied it. I didn't." She writes it on her slate under the rest (`EBL-I5`) and walks down to the spur with the player. At night now, she explains, the ward banks its hearths, draws least, and the branch peaks: the relief lifts and rings. "That's your bell. That's your drunk."

**Beat 4: The Stay (`S04_stay`).** *Objective: Make the bell safe to ring.* Two ways, both complete the step:

- **Option A (skill): shape a stay** (**Woodcutting ~[GD: low]**; EHC-05, reclaimed crate-wood only). At the Commons store stack (B4): **split** a crate-oak beam (interaction, ~3 s), **shave** the bar to the old stay's length against it (a 2-segment channel), **fit** it at the headstock from the post's ladder (a 2-segment channel). `EBL_STAY` = self.
- **Option B (time-cost): the crew's.** Veska sends a line hand; keep watch at the post bench until morning; fit the stay he brings (the same 2-segment fit). `EBL_STAY` = crew.

**Beat 5: The Notch (`S05_notch`).** *Objective: Set the relief weight at the night peak.* At the spur at night (keep watch in the niche if it is not night; the step pins the peak). Move the weight along its lever (one interaction per notch) and watch the valve tell at the peak:

| Notch | Valve tell at the night peak | Result |
|---|---|---|
| Inner (as found) | Amber → **lifts**: hiss, the line jerks | Too light: it rings. |
| Middle | **Amber, steady** | Right: holds at the night peak and still lifts on a real back-up. |
| Outer | **Red, crazed** | Refused before the weight seats (Veska's line if she is at the spur; otherwise the same line as a remembered bark, `EBL-B5.x`): "You've stopped her breathing. Back a notch." Never touch a red; nothing resets. |

The step completes on the middle notch held through one peak (~10 s).

**Beat 6: Keep or Give Back (`S06_decide`).** *Objective: Decide what the bell is for.* At the post straight after `S05`, with no wait for morning (playability audit ES-11): Agathe, Veska, Wim, a few of the lane (`EBL-D5`). The choice (EBL.8) sets `EBL_BELL`. In both outcomes Veska writes on Wim's docking slate at the forge gate (*Bell was the main's. Not his.*) and the gatekeeper wipes the docking; Agathe rubs *DRUNK* off her post herself. Quest Completed.

### EBL.5 The bell (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| Night | **The lane** | Empty; doorway lamps banked low; hood tells clear. Agathe asleep on her stool. |
| 0–2 s | **Hiss** | A long hiss from the grate at the post's foot; warm air lifts the ash. |
| 2–4 s | **Rope** | The rope pulls down through the cleat by itself, slowly, then hard. |
| 4–7 s | **Bell** | The bell swings and rings once, twice, three times; the stay creaks. Agathe wakes and looks at her hands. |
| After | **Agathe** | "Not me. You saw. Not me." |
| Meaning | A relief valve tied to a rope. Proves nothing; not the sob in the pipes; nothing below is suggested. |

### EBL.6 Encounters and hazards

No encounters. **EBL-H1:** the relief spur is a Working zone (light periodic damage outside the niche). **EBL-H2:** the valve's outer notch shows red and is refused (no damage beyond a scald if the player forces the weight; one step of knock-back). **Death** (only possible by lingering in the spur): respawn at the Cooling House; step and notch progress kept.

### EBL.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the bell-keeper. | `EBL-D1` accept | Yes | — |
| `S01_listen` | Keep watch at the bell post at night. | Keep watch to night + bell event + 3 inspects + one witness (`EBL-D2` or `EBL-B1.02`/`.03`) | Yes | Night pinned |
| `S02_spur` | Follow the line down. | Enter spur + relief valve inspect | Yes | Knot cannot be cut yet |
| `S03_veska` | Ask the warden about the hitch. | `EBL-D3` end | Yes | Veska's slate line |
| `S04_stay` | Make the bell safe to ring. | Stay fitted (Option A) or keep watch to morning + fit (Option B) | Yes | Sets `EBL_STAY` |
| `S05_notch` | Set the relief weight at the night peak. | Middle notch held through one peak | Yes | Outer notch refused |
| `S06_decide` | Decide what the bell is for. | `EBL-D5` choice + end | Yes | Sets `EBL_BELL`; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `EBL_STAY` = self / crew | `S04` | `EBL-D5.04` |
| `EBL_BELL` = kept / removed | `S06` | Bell post props (marked rope with `kept`); barks; EH-M6 (request only, EBL.11) |

### EBL.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Keep it** (`kept`): *"Keep the line on. If the bell rings by itself, it's the main. Get the wardens."* | The line stays tied to the relief at its proper notch; Agathe marks the rope where the line joins. The bell now rings by itself only on a real back-up. | A bell that can ring at night is a bell people sleep badly under; the lane grumbles. | Barks: Agathe "If it rings and I'm asleep, it's the main." Children dare each other to touch the marked rope. |
| **Give it back** (`removed`): *"Untie it. The bell's for shifts. The relief vents to the duct, like it should."* | Veska unties the hitch; the relief vents into the spur; the bell is Agathe's again. | If the branch backs up at night, nobody hears it until the hoods go cold. | Barks: Agathe rings the shifts "on the dot, thank you". Veska checks the spur on her rounds. |

No option is wrong. Wim's day is restored and Agathe's post is wiped in both.

### EBL.9 Rewards

Agathe's thanks and a small payment from the lane's bell box ([GD]); Wim's thanks (a ride on his cart from Cinderwall to the forge gate: a short quest-travel interaction, flavour); the bell post bench as a keep-watch bench; Woodcutting XP on Option A only. No lump quest XP.

### EBL.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Comes by day | The bell is quiet; keep watch to night at the bench. |
| Cuts the line early | Refused until `S03` (`EBL-B2.2`). |
| No Woodcutting | Option B; one turn. |
| Logout / walking away | Stays Active at the step; resume at Agathe (`EBL-D1.00`) or Veska. |
| Co-op | Per-player bell event, valve, weight and choice; a partner's notch never sets yours. Any shared bell sound is presentation only. |

### EBL.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Night bell event | Audio / Systems | Per-player scripted hiss, rope pull and ring on keep watch to night during `S01`. |
| Weighted lever with three notches | Systems | Interaction moves the weight; the valve tell plays an authored result per notch at the pinned peak; outer notch refused. |
| Woodcutting on reclaimed crate-oak | Skills | Reclaimed-wood node (EHC-05) at the Commons store stack. |
| Rope prop variants | Art | A marked rope with `EBL_BELL = kept` (Art chooses the marking). |
| EH-M6 (request only) | Narrative | Optional Agathe bark in the EH-M6 frost if `EBL_BELL = kept`: "Rope's frozen to the post. My warning's no use if it can't swing." No change to EH-M6 steps; Act III already freezes the rope. |

### EBL.12 Mystery ledger entry

None (resolved). The bell after the EH-M1 surge is explained here: the opening surge lifted the relief.

### EBL.13 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Agathe Mund** [NEW], Cinderwall bell-keeper | Every shift's hour; the lane's sleep. | Pipes. | Old, sharp, proud of being exact; hurt and hiding it. |
| **Wim Kettering** [NEW], carter | His cart, his docked day. | Why the bell rang. | Slow, fair, a little shy. |
| **Veska Dunmor** | Her crew's hitch; the branch. | — | As Act I. Owns it in one line. |

```
EBL-D1.00 [quest Active, returning] AGATHE: "It rang again. I didn't. Where were we?"   (pins step) → end
EBL-D1.01 AGATHE: (rubbing at the chalk on her post with a sleeve) "Drunk. On my post. I've rung this ward's shifts since they rebuilt the gate."
EBL-D1.02 AGATHE: "Since the ward came back, it rings at night. By itself. And who's sat under it? Me."
  > "I'll sit up and listen."                                        → EBL-D1.10
  > "Who else has it hurt?"                                          → EBL-D1.20
EBL-D1.10 AGATHE: "Bench is there. Bring a coat. Bring two; it's still Cinderwall."   {event: accept → S01_listen} → end
EBL-D1.20 AGATHE: "Wim Kettering took his cart out at it and blocked the forge gate an hour early. They docked him a day. He's not even cross with me. That's worse."   → EBL-D1 options
EBL-D2.01 WIM: (at the forge gate, beside the docking slate) "Bell went, I went. That's what a bell's for." (beat) "Gate was shut. They docked me a day. It's on the slate."
EBL-D2.02 WIM: "Don't blame Agathe. She was asleep on her stool. I saw her."   → end
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| EBL-B0.1 | Cooling House, after EH-M1 | HENNET | "Agathe's bell's been daft since the ward came back. She's taking it personally. Go and sit with her." |
| EBL-B1.02 | Night baker, if asked | NIGHT BAKER | "Hiss, then the bell. Every night about the time I knock back the dough." |
| EBL-B1.03 | Hennet, if asked | HENNET | "Rang the night you opened the junction, too. Didn't you hear it?" |
| EBL-B2.2 | Cut the line before `S03` | (prompt) | "A warden's hitch. Ask the warden whose it is." |
| EBL-B5.x | Weight pushed to the outer notch in `S05` with Veska elsewhere | VESKA (remembered, as at `EBL-D3.04`) | "You've stopped her breathing. Back a notch." |

```
EBL-D3.01 VESKA: (the player describes the knot; she is already nodding) "Warden's hitch. Ours. Third cold night."
EBL-D3.02 VESKA: "Junction shut, the branch backing up behind it, nobody awake. We tied the relief to the bell so a lift would wake us." (beat) "Then the ward came back. Nobody untied it. I didn't."
EBL-D3.03 VESKA: "Nights now, the ward banks its hearths and draws least. Branch peaks. Relief lifts. Bell rings." (beat) "That's your bell. That's your drunk."
EBL-D3.04 VESKA: (chalks her slate) "Come on. I'll show you where the weight goes. You'll read it, not me."   → end
EBL-D5.01 AGATHE: (at the post) "Stay's in. Weight's right. Now what? Is it my bell or the pipe's?"
EBL-D5.02 VESKA: "Keep the line on and it'll only ring if she really backs up. Or untie it and she vents to the duct, like she should, and nobody hears."
EBL-D5.04 [EBL_STAY = self] AGATHE: "And that stay's crate-oak. It'll outlast me. Don't say anything."
  > "Keep the line on. If the bell rings by itself, it's the main."  → EBL-D5.10 {EBL_BELL = kept}
  > "Untie it. The bell's for shifts."                               → EBL-D5.11 {EBL_BELL = removed}
EBL-D5.10 AGATHE: (fetches a pot of paint) "Then the rope's marked where the line joins. If it rings and I'm asleep, it's the main. Get the wardens."   → EBL-D5.20
EBL-D5.11 VESKA: (unties the hitch on the next descent; up the grate) "Off." AGATHE: "Then it's mine. On the dot, thank you."   → EBL-D5.20
EBL-D5.20 VESKA: (to the forge gate, chalking Wim's docking slate) "Bell was the main's. Not his." WIM: (to the player, shy) "A day's a day." AGATHE: (wiping DRUNK off the post herself) "And that's that."   {small payment; quest Completed}
```

| Id | Object | Text | Condition |
|---|---|---|---|
| EBL-I1 | Rope | "Hemp, worn pale. A second line spliced into it a hand above the cleat, running down through the grate." | — |
| EBL-I2 | Grate | "Warm air. Ash on the bars lifts before each hiss." | — |
| EBL-I3 | Stay | "The wooden stay on the headstock is cracked through. A bell yanked too often goes over." | — |
| EBL-I4 | Relief valve | "A weighted lever with three notches; the weight on the inner. A warden's hitch round the lever's end. The tell: amber." | `EH_TELLS` |
| EBL-I5 | Veska's slate | Adds: "*Relief tied to bell, third night. Untie when open.* Then, today: *Didn't.*" | After `S03` |

| Speaker | Line | Condition |
|---|---|---|
| AGATHE | "If it rings and I'm asleep, it's the main." | `EBL_BELL = kept` |
| AGATHE | "Shifts on the dot. Thank you." | `EBL_BELL = removed` |
| CHILD | "Touch the marked rope. Go on. I dare you." | `EBL_BELL = kept` |

### EBL.14 Open decisions

1. **The Part 3 "much later" reading** (the bell sequence matching deep-works movement) is not used anywhere; if a later package wants it, it needs its own evidence.
2. **Woodcutting on crate-oak:** follows ED-11; Gameplay Designer sets the level.

### EBL.15 Review log

| Finding | Revision |
|---|---|
| Talk-and-inspect risk. | Night watch, a descent, a stay to shape, and a weight set by reading a tell at a peak. |
| Veska as a villain. | She owns it in one line and writes it on her slate; the ward's cold nights are the cause. |
| Remnant creep. | None; the relief is a warden's job and stays one. |

---
---
## ESR — The Seven Repairs

### ESR.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `emberholt.side.seven_repairs` |
| Type | Environmental. Standalone (bible §7.2). |
| Unlock | EH-M1 Completed. Offered by Hallam Drost on the Bridge of Seven Repairs inside Embergate (`ESR-D1`). |
| Resume hook | Hallam on the parapet: `ESR-D1.00` "Still seven. Still one name on the plate. Where were we?" |
| Skills | Smithing ~[GD: low–mid] (hook); the Hall's crew as the alternative |
| Combat share | 0% (contract: none) |
| Cameo | Odile Prace (the valve book); Tessaly Varn (`TAS_ACCOUNT = named` only) |
| Choice | Credit: cut the marks on the plaque stone, or write the crews in the gate's works roll (`ESR_CREDIT`); text and props only |
| Unlocks | The gate yard forge as a public Smithing station |
| **Anchor** (§7.1) | Masons and crews |
| **World-truth row** | H23 |
| **Revelation role** | None. Optional Thornfell echo (`TAS_ACCOUNT = named`) is flavour; it proves nothing across regions. |
| **Recurring evidence** | The seven marks (inspect in place) |
| **State compliance** | Inactive / Active / Completed. No fail; the Smithing hook has a crew wait; the credit choice is text only. |
| **Combat compliance** | None. The culvert walk is a light heat zone with niches. CDR-6: every step is one player's. |

**In one paragraph.** Inside Embergate a short stone bridge carries the gate street over a hot cut where the heat main runs in a culvert. Its plate says *Raised and kept by the Gatestone Masons*. **Hallam Drost**, an old bridgeworker, says seven crews kept it and every one left a mark, and wants them read before **Ludo Ferrant** of the Masons' Hall re-gilds the plate for the High Kindling. The player finds the marks in seven layers of work, above the deck and beside the culvert below, and matches six of them to a person or a record; the seventh, an X on a rail of old pipe, belongs to nobody anyone can name. The eighth repair is a parapet stone burst by a rusted cramp: the player forges and sets a new cramp in lead, or holds the level for the Hall's crew in the morning. At dusk the culvert's heat rises through the deck and all the marks show dark on the warm stone at once. Then Hallam and Ludo ask the warden's hand how the bridge should credit its keepers.

### ESR.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Part 3's four-region reading (a Thornfell method and a Mire transfer list). | Rejected: the bible adopts only the optional `TAS_ACCOUNT` echo; the Part 4 ledger requires shared people, dates and task across two records before any cross-region repair claim. |
| **B. Read seven marks in their layers with a witness or record each → the eighth repair (skill or crew) → the dusk marks → credit** | **Selected.** Read, repair, credit; physical reading, one forged repair, a credit choice. |

| Element | Source | Status |
|---|---|---|
| The Bridge of Seven Repairs (EP27), inside Embergate | Part 3; bible §4.2, ED-13 | [PROPOSAL — DIRECTOR] ED-13; [NEW] detail |
| Embergate; lanterns lit by apprentice embercrafters | Dossier §VII.1 | [CANON] |
| Emberforged artisans; emberglass; Cinderweave glasswrights | Dossier §V, §VII.2 | [CANON] |
| Tessaly Varn, Emberforged stonemason; *Ash in the Snow*; `TAS_ACCOUNT` | Thornfell bible §5.2; Thornfell TAS | [NEW, Thornfell] |
| "Civic repair credit omits collaborators": needs two matching records; never blame the Remnant | Part 4 ledger, controlled handoffs | Binding limit |
| Hallam Drost, Ludo Ferrant, the Gatestone Masons' Hall, the works roll | This package | [NEW] |

### ESR.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **R1. The deck and parapet** | Offer; plate; marks 3, 4, 6, 7; the cramp | A short arched bridge on the gate street. The **bronze plate** on the parapet's end stone. Setts worn in two ruts. Emberglass **lamp-cups** on the parapet. One **split parapet stone** with a rust-burst cramp. An iron **rail** on one side made of old pipe. | — |
| **R2. The culvert walk** | Marks 1, 2, 5 | Steps down to a ledge along the hot cut under the arch. The heat main's **culvert** in the cut's floor; warm air rising. The **arch ring** overhead; the **downstream face**. Pinned **Working**; two cooling niches. | Steps; ledge |
| **R3. The gate yard forge** | Smithing | A mason's forge in the merchant yards by the gate (Hall property): anvil with a swage, bellows, quench tub, a bar rack. | — |
| **R4. The Gate Valve House** (Act I V1–V2) | Odile; the works roll | As Act I. A second, thinner book beside the valve book: the gate's **works roll**. | — |

### ESR.4 Beats

**Beat 0: The Plate (`S00_offer`).** *Objective: Talk to the old bridgeworker.* `ESR-D1`. Hallam: seven crews, one name; Ludo is coming with gold leaf; read the marks first.

**Beat 1: The Plate Read (`S01_plate`).** *Objective: Read the bridge's plate.* Inspect the plate (`ESR-I1`). Ludo Ferrant arrives (`ESR-D2`): the Hall rebuilt the bridge after the war and has its name on it "rightly"; he does not mind marks being read.

**Beat 2: Seven Marks (`S02_marks`).** *Objective: Find the seven marks and who left them.* Any order. Each mark is an inspect; each needs its **match** (a witness line or a record inspect). The step completes when all seven are found and six matched (the X has no match by design). The carters' elder (match 3) and the glasswright (match 4) both stand at the gate yard at every hour while `S02` is Active (playability audit ES-12).

| # | Mark (where) | Layer it marks | Match |
|---|---|---|---|
| 1 | Hammer in a ring (arch ring, R2) | The rebuild of the arch | Ludo and the plate (`ESR-D2.10`) |
| 2 | A tell bead set in mortar (culvert lining, R2) | Wardens relined the culvert | Odile's valve book: *Gate culvert relined, wardens' crew* (`ESR-I9`) |
| 3 | A wheel scratched in a sett (deck, R1) | The deck relaid | A carters' elder at the gate yard (`ESR-B2.03`) |
| 4 | A flower in the glass (lamp-cups, R1) | The lamp-cups reset | A Cinderweave glasswright buying at the gate market (`ESR-B2.04`): "Our apprentices' flower." |
| 5 | Three notches (downstream face, R2) | The face repointed, unpaid, at night, the winter the gate culvert froze | Hallam's own trowel handle has the same three notches (`ESR-I7`; `ESR-D3`) |
| 6 | A square with a notch (beside a parapet cramp, R1) | Parapet cramps renewed | The Hall's work roll, which Ludo opens: *Parapet cramps renewed. Guild crew.* (`ESR-I10`) |
| 7 | A deep X (the pipe rail, R1) | The rail replaced with old pipe after somebody fell | **None.** Hallam: "A Dross crew, the year after the gate was rebuilt. Wanted nothing. Never said a name." |

**Optional, `TAS_ACCOUNT = named` only:** when mark 6 is matched, **Tessaly Varn** is at the parapet with her guild case (`ESR-D4`): the square with a notch is her crew's. She says one thing about Passwatch's arch and one about cramps. No other value of `TAS_ACCOUNT` places her here or gives any line.

**Beat 3: The Eighth (`S03_cramp`).** *Objective: Make the split parapet stone good.* Inspect the split stone (`ESR-I11`): an old cramp rusted, swelled and burst the stone. Two ways, both complete the step:

- **Option A (skill): forge and set a cramp** (**Smithing ~[GD: low–mid]**). At the gate yard forge (R3), take bar stock (EHC-06); **heat** until the forge's tell shows amber (one interaction); **draw** the bar on the anvil (a 2-segment channel); **bend** the ends at the swage (a 2-segment channel); **quench** (one interaction). At the parapet: **cut out** the old cramp (a 3-segment channel), **seat** the new one (one interaction), **pour** lead (EHC-07; a 2-segment channel). `ESR_CRAMP` = self.
- **Option B (time-cost): the Hall's crew.** Keep watch on the parapet until morning; the crew set the cramp while the player **holds the level** on the stone (a 2-segment channel: keep the bubble centred by small corrections on the crew's call). `ESR_CRAMP` = crew.

Hallam: "That's eight. Mark it." The player cuts a mark of their choosing in the lead (flavour; no flag).

**Beat 4: Dusk (`S04_dusk`).** *Objective: Watch the bridge at dusk.* Keep watch on the parapet to dusk (pinned). **The marks (ESR.5)** play.

**Beat 5: Credit (`S05_credit`).** *Objective: Decide how the bridge credits its keepers.* Hallam and Ludo (`ESR-D6`). The choice (ESR.8) sets `ESR_CREDIT`. Ludo pays from the Hall and lends the gate yard forge. Quest Completed.

### ESR.5 The marks at dusk (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| Dusk | **Lamps** | An apprentice lights the parapet lamp-cups with a gesture (EME01 at the gate). |
| 0–4 s | **Heat** | Warm air from the culvert rises through the deck joints; the stone warms unevenly. |
| 4–8 s | **Marks** | All seven marks, and the eighth in the new lead, show dark on the warm stone at once, cut deeper than the face around them and holding the cool a moment longer. |
| 8–12 s | **Fade** | They fade as the stone warms through. Hallam: "There they are. Every evening. Nobody looks." |
| Meaning | Cut stone cooling slower. Proves nothing. |

### ESR.6 Encounters and hazards

No encounters. **ESR-H1:** the culvert walk is Working (light periodic damage outside niches; touch water). **Death** there respawns at the Gate Valve House; marks found are kept.

### ESR.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the old bridgeworker. | `ESR-D1` accept | Yes | — |
| `S01_plate` | Read the bridge's plate. | Plate inspect + `ESR-D2` end | Yes | — |
| `S02_marks` | Find the seven marks and who left them. | 7 mark inspects + 6 matches | Yes | Tessaly optional, `TAS_ACCOUNT = named` |
| `S03_cramp` | Make the split parapet stone good. | Cramp set (Option A) or keep watch + level held (Option B) | Yes | Sets `ESR_CRAMP` |
| `S04_dusk` | Watch the bridge at dusk. | Keep watch to dusk + marks event | Yes | — |
| `S05_credit` | Decide how the bridge credits its keepers. | `ESR-D6` choice + end | Yes | Sets `ESR_CREDIT`; payment; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `ESR_CRAMP` = self / crew | `S03` | `ESR-D6.03` |
| `ESR_CREDIT` = marks / roll | `S05` | Plaque stone prop; works roll prop; gate barks |

### ESR.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Cut the marks** (`marks`): *"Cut all eight marks on the plate stone, under the Hall's line."* | The Hall's mason cuts the seven marks and the eighth in a row under the gilded line; no names, so the X stands equal with the rest. | Ludo's Hall is one mark among eight on its own plate; he says so. | Prop: eight marks under the plate. Children trace them. |
| **Write the roll** (`roll`): *"Leave the plate. Write every crew in the gate's works roll, names where known."* | Odile writes the seven repairs and the eighth into the works roll beside the valve book, names where known, *not known* for the X. | The plate still says one name to everyone who crosses; the roll is read by those who ask. | Prop: the roll open at the bridge page. Odile: "Anyone can read it. Nobody asks. Somebody will." |

No option is wrong. Both credit the crews; one where everyone walks, one where anyone may read.

### ESR.9 Rewards

Ludo's payment from the Hall ([GD]); the gate yard forge as a public Smithing station; Smithing XP on Option A; no lump quest XP.

### ESR.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| The X has no match | By design; the step needs six matches. |
| No Smithing | Option B; one turn and the level. |
| Logout / walking away | Stays Active; resume at Hallam (`ESR-D1.00`). Found marks and matches persist. |
| Co-op | Marks, matches, the cramp, the dusk moment and the choice are per player. Tessaly's visit follows each player's own `TAS_ACCOUNT`. |

### ESR.11 Integration needs

Mark decals and inspects (per layer); a culvert walk heat zone pinned Working with two niches; Smithing at the gate yard forge (existing heat, draw, bend, quench) and a lead-pour channel; a level-holding channel (Option B); a warm-stone decal reveal on keep watch to dusk; plate-stone and works-roll prop variants by `ESR_CREDIT`; an optional NPC placement for Tessaly read from `TAS_ACCOUNT = named`.

### ESR.12 Mystery ledger entry

| Mystery | Author truth | Public belief | Evidence | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| **The X on the rail** | A Dross crew who put a rail back after a fall and wanted nothing. | The Hall did it all. | The mark; Hallam's memory. | It was someone hiding. | Their names. **Never resolved.** | None. |

### ESR.13 Dialogue

**Cast notes.** **Hallam Drost** [NEW], old gate labourer and bridgeworker: knows every stone; doesn't know who the X crew were; voice slow, exact, fond of the bridge as of a dog, never bitter. **Ludo Ferrant** [NEW], steward of the Gatestone Masons' Hall: knows the roll; voice proud, decent, a little pompous, honest when shown. **Odile Prace**: counts aloud. **Tessaly Varn** (Thornfell bible; `TAS_ACCOUNT = named` only): courteous, exact, tired; corrects small errors.

```
ESR-D1.00 [quest Active, returning] HALLAM: "Still seven. Still one name on the plate. Where were we?"   (pins step) → end
ESR-D1.01 HALLAM: (polishing a mark with a thumb) "Traveller. Or warden's hand, Odile says. Seven crews kept this bridge. Every one cut a mark. Plate's got one name."
ESR-D1.02 HALLAM: "Hall's sending a man with gold leaf for the High Kindling. Read the marks before he shines the plate. Then tell me I'm wrong."
  > "Show me."                                                       → ESR-D1.10
  > "Not now."                                                       → end (offer stays open)
ESR-D1.10 HALLAM: "Some are on top. Some are under, by the culvert. Touch water on the way down; it's warm under there."   {accept → S01_plate}
ESR-D2.01 LUDO: (gold leaf in a book under his arm) "Ludo Ferrant, for the Gatestone Masons. We raised this bridge when the gate was rebuilt. The plate says so, rightly."
ESR-D2.10 LUDO: (at the arch ring, on mark 1) "Our hammer. Our ring." (beat, seeing the others) "...I didn't say we were the only hands. I said the plate was right."
ESR-D3.01 HALLAM: (on mark 5; turns his trowel over: three notches in the handle) "Winter the gate culvert froze. The face cracked. Hall had no crew for it. Five of us did it nights. Nobody paid. Nobody wrote it."
ESR-D3.02 HALLAM: "And the X. A Dross crew, the year after the gate was rebuilt. Somebody fell. They put a rail back out of old pipe. Wanted nothing. Never said a name."
ESR-D4.01 [TAS_ACCOUNT = named] TESSALY: (at the parapet, guild case at her feet) "That square with a notch is my crew's. Parapet cramps."
ESR-D4.02 [TAS_ACCOUNT = named] TESSALY: "A gate book on a cold pass once wrote my crew's name for an arch. I came to see if my own city's bridge ever did." (beat, looking at the burst stone) "Cramps rust. Somebody always forgets cramps rust."   → end
ESR-D5.02 [ECW_SEAT_RING = self] HALLAM: (at the forge) "You made Dunmor's seat ring, I heard. A cramp's a seat ring that holds stone. Same hands."
ESR-D6.01 HALLAM: (the eight marks fading on the warm stone) "There they are. Every evening. Nobody looks."
ESR-D6.02 LUDO: (gold leaf book closed) "The Hall raised it. I won't pretend otherwise. But I'll not pretend it was only us, either. How should it say so?"
ESR-D6.03 [ESR_CRAMP = self] HALLAM: "And the eighth's yours. In lead, with your mark." / [ESR_CRAMP = crew] HALLAM: "And the eighth's the Hall's crew, with you on the level. That counts. Ask any mason."
  > "Cut all eight marks on the plate stone, under the Hall's line." → ESR-D6.10 {ESR_CREDIT = marks}
  > "Leave the plate. Write every crew in the gate's works roll."    → ESR-D6.11 {ESR_CREDIT = roll}
ESR-D6.10 LUDO: (a long breath) "Eight marks under our line. The X as big as our hammer." (beat) "Fair. I'll send the mason." HALLAM: "Send a good one."   → ESR-D6.20
ESR-D6.11 ODILE: (fetched from the valve house, the works roll open) "Seven. Eight. Names where known. One: not known." (writes) "Anyone can read it. Nobody asks. Somebody will."   → ESR-D6.20
ESR-D6.20 LUDO: (pays) "From the Hall. And the yard forge is yours when you want it." HALLAM: "Seven was a good number. Eight's better."   {quest Completed}
```

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| ESR-B2.03 | Carters' elder, shown mark 3 | CARTERS' ELDER | "Our wheel. We relaid the setts the year the ruts took a cart's axle. Hall sent a bill." |
| ESR-B2.04 | Glasswright, shown mark 4 | GLASSWRIGHT | "Our apprentices' flower. They reset the cups. Badly, the first time." |

| Id | Object | Text | Condition |
|---|---|---|---|
| ESR-I1 | Plate | "Bronze: *Raised and kept by the Gatestone Masons.* The gilt is worn off the 'kept'." | — |
| ESR-I2 | Mark 1 | "A hammer in a ring, crisp, on the arch's keystone." | — |
| ESR-I3 | Mark 2 | "A tell bead set flush in the culvert mortar. Amber." | `EH_TELLS` |
| ESR-I4 | Mark 3 | "A wheel scratched into one sett, worn nearly smooth." | — |
| ESR-I5 | Mark 4 | "In the base of one lamp-cup's glass, a five-petalled flower." | — |
| ESR-I6 | Mark 5 | "Three notches on a pointing stone of the downstream face. The pointing is a different grey." | — |
| ESR-I7 | Hallam's trowel | "Worn handle. Three notches near the ferrule." | — |
| ESR-I8 | Mark 7 | "An X cut deep into the pipe rail's foot plate. No other mark." | — |
| ESR-I9 | Valve book (Odile) | "Under the culvert's number: *Gate culvert relined. Wardens' crew.* A tick in a warden's hand." | — |
| ESR-I10 | Hall work roll | "*Parapet cramps renewed. Guild crew.* No crew name." | — |
| ESR-I11 | Split stone | "A parapet stone split along an old cramp; rust has burst out of the lead." | — |

### ESR.14 Open decisions

1. **Tessaly Varn (bible §5.2):** appears only with `TAS_ACCOUNT = named`. The Hall's roll does not name her crew in any case, so no Thornfell outcome leaks into the record. No cross-region repair claim is made (Part 4 ledger).
2. **The X** is never resolved; nothing implies it was Volkhari, Remnant or anyone else, and nothing rules any of them out.

### ESR.15 Review log

| Finding | Revision |
|---|---|
| Part 3's Thornfell method and Mire transfer list. | Not used (bible §7.2; Part 4 ledger handoff rule). |
| Credit choice risked blaming the Hall. | Ludo is decent; the plate was "right" and incomplete. |
| Reading only. | Two layers need the culvert walk; the eighth repair is forged and set. |

---
---

## Integration summary (file level)

Every need above is a standard system already used by the Emberholt act packages: quest-pinned heat states (EI-HT-01 fallback), tell-gated refusals (the EH-M1 red-cock pattern; never a reset), keep watch on the presentation hour, channelled interactions with kept progress, carry-state objects, existing skill verbs (Leatherworking, Mining, Cooking, Woodcutting, Smithing) with outputs as quest objects until the economy pass defines EHC-01 to EHC-07, per-player props and NPC placement variants (presentation fallback only, CDR-6), and short scripted per-player presentations (steam, slag mirror, lamp ripple, bell, warm marks; no cutscene). **New runtime needs: none.**

## Package review summary

| Check | Result |
|---|---|
| Brief fit (bible §7.1–7.3) | EWA, ECN, EFC, EBL, ESR match their rows: unlocks (EH-M1; EWA; ECN + EH-M2; EH-M1; EH-M1), verbs, places and contracts (EWA Cinder Rats; ECN Dross Scavengers, crew-recovered next morning; EFC no combat, sets `EH_COMMONS`; EBL keep/remove; ESR credit text only). |
| Rulings | CDR-1: every enemy to 0 HP, no SX, no post-fight speech. CDR-2: melee or ranged everywhere, ranged required nowhere. CDR-3: no release wording. CDR-4: standard systems; one skill hook per quest with a time-cost alternative. CDR-6: every step solo; partner credit only from the partner's own step; choices per player. |
| Flags | One writer each; `EH_COMMONS` set only by EFC. Every main-line flag read exists exactly as Act I/III define it (`EH_TELLS`, `EH_COLD_WARD`, `ECW_SHORTFALL_SEEN`, `ECW_SEAT_RING`, `EH_CURRICULUM`, `EH_HOLLOW_TRUTH`); Thornfell `TAS_ACCOUNT` read for `named` only. |
| Revelations and reserved decisions | Nothing owned or seeded; the shortfall untouched. No D-E2, D-S1 or ED-3 (Iven Calder) dependency (all ruled 2026-11-15); `[ALLOCATION]` on every EH-M1-cause line; D-C03 and D-C06 kept. No overlap with EST, ETB, EMS, ENW, EGT (the memorial plaque and the Half-Name Wall are not used). Quest items: 0. |
| New names (grepped across `04_CONTENT_PRODUCTION`, `LORE`, `00_ADMIN`) | Dunya Kordel, Grisel Tamm, Ilsa Cleff, Sorrel Vamm, Agathe Mund, Wim Kettering, Hallam Drost, Ludo Ferrant, the Gatestone Masons' Hall, Bellwright's Lane, Adda Halloran, Old Mother Mossa, little Bett, Haldo Brune, Old Gav: no other use. Rejected for collisions: Sefa, Tarrow, Ebbe, Orsa, Ruddle, Tibb (Mire), Wenn (Wenna), Lorcan (Act I), Orrin. |
| Deviations from the bible | (1) ECN's ward court and court book realise "the complaint reaches Yorven's book". (2) EFC dates First Cooling as "the first night the Commons runs full after the year's mending". (3) EBL explains the EH-M1 surge bell (Act I A14 item 6). (4) EFC reads `EH_HOLLOW_TRUTH` for Hesper's optional names, a reader the bible §9.1 row does not list. (5) Rejected candidates are not listed in the selection records (size). |
| Independent review, 2026-11-15 | Authored walkthrough against the brief, CDR-1 to CDR-6 (§3.7), the bible, dossier, Factions, Part 4 ledger and the reviewed Act I–III packages and dialogue (nothing was played; no build exists). **Flags:** `EH_TELLS`, `EH_COLD_WARD` (posted / settled), `ECW_SHORTFALL_SEEN`, `ECW_SEAT_RING` (self / crew), `EH_CURRICULUM`, `EH_HOLLOW_TRUTH` and Thornfell `TAS_ACCOUNT` (named / held / unwritten) exist as read; `EH_COMMONS` has one writer (EFC `S06`) and matches Act III `S01`, `EGA-D2.30`–`.32` and the store slate. Unlocks match Act I's unlock row (EWA, EBL, ESR after EH-M1). **Canon (Medium):** §0.5 and ECN.12 said the pit lot were "plain" / "ordinary" pipe-strippers under a "No Remnant presence" rule, which reads as denying the dossier's "clandestine Remnant scavengers"; reworded to give them no affiliation and neither use nor contradict the label. ESR open decision 2 reworded the same way for the X. **Rulings:** CDR-1 holds (ECN and EWA enemies to 0 HP; no post-fight speech; every named person, child, Watch officer and Slagside resident non-targetable); CDR-2 (slinger ledges reachable on foot); CDR-6 (partner credit only through the partner's own step). Combat reveals nothing; the cache is found by Ilsa's directions. **Playability (Low):** EBL's outer-notch refusal was voiced by Veska, who need not be at the spur at night; now a remembered bark (`EBL-B5.x`) when she is elsewhere. No softlock found; every skill hook has a time-cost alternative; every quest has physical steps. **Renames (near-duplicates):** Wim Ostrander → **Wim Kettering** (Ostry, Act I); Adda Corr → **Adda Halloran** (Corra, Mire; Corm Brask); Haldo Price → **Haldo Brune** (Odile Prace). **Art direction:** EBL's "red-painted rope" is now a marked rope (Art chooses the marking). D-C03, D-C06 kept; Hesper's names are Act I's crew, names only. No release wording. |
| Batch 4 encounter alignment review, 2026-11-15 | Applied Enemies file PE-15: ECN-E1's Shove and ECN-H1 now say no knock-back ends inside a slag pool (Enemies C-2, authored tuning pending the Gameplay Designer). The ECN-E1 lean-to roof's ladder access depends on Zones ML-34 (ramp or at-grade slinger in a flat build). No id, step, flag or line changed. |
| Emberholt character rulings, 2026-11-15 | Reserved-decision notes (§0, review summary) updated: D-E2, D-S1 and ED-3 ruled; `[INITIATE]` placeholder replaced by Iven Calder (not used in any node). No node, flag or line changed; no Thalan, Speaker-knowledge or Elyndra content here. |
| Director review pass, 2026-11-15 | ESR bridgework elder Hallam Calder renamed **Hallam Drost** so no Emberholt NPC shares a surname with Iven Calder (ED-3); "Drost" grepped clean across 04_CONTENT_PRODUCTION, LORE and 00_ADMIN. |
| Playability audit fixes, 2026-11-15 | Playability audit fixes, 2026-11-15: ES-01, ES-03, ES-11, ES-12. |
