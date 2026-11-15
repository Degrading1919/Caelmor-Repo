# Emberholt Main Questline, Act I: Cold Ward, The Ember in Every Hand, The Hollow That Should Not Burn

**Status:** Authored production content for Creative Director milestone review (2026-11-14). This package implements Emberholt main milestones EH-M1, EH-M2 and EH-M3 (bible §6, §6.1), which carry Act I from the player's first evening in Cinderwall to the Act I turn in the Glassed Hollow. It follows the Mire act-package format (`Caelmor_Mire_Main_Act_I.md`), itself the Thornfell and Lowmark format. Everything marked **[NEW]** is authored and not canon until the Director promotes it (ED-19: promote nothing). Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 decision (ED-1 to ED-20). **[CANON]** items come from the Emberholt dossier, the Emberholt character file, Factions and the Part 4 ledger. **[APPROVED — id]** items rest on an architecture ruling (FT-02d, FT-04, D-C03, D-C06). No schema, production JSON or C# is created here. Emberholt is an internal production milestone of the complete game (CDR-3). Combat follows the Director rulings (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1), every fight accepts melee or ranged and none requires ranged (CDR-2), standard RPG systems are preferred to bespoke simulation (CDR-4), and every step, boss and reward is completable solo with co-op as optional assistance (CDR-6). Emberholt registers no scripted-survival exception (rulings §4; bible §3 "SX proposal: none").

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Emberholt_Narrative_Production_Bible.md`. Its §6 table, §6.1 briefs and §6.2 contract rows for EH-M1, EH-M2 and EH-M3 are binding and are implemented as written. Where this package adds detail it is marked [NEW] and stays inside the bible's cast (§5), places (§4.2), flags (§9.1), encounter families (§10) and conventions (§11). Where it has to read a brief more narrowly or add a sub-site, the reason is recorded in that quest's open decisions; the bible is not edited.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Emberholt_Main_Act_I_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`ECW-`, `EEH-`, `EGH-` prefixes), barks, inspect texts and the full text of every document (the valve order, the cut protest page, the tally board, the assessment ledger, the crew's day-book, the Deepbrand work order, the chamber roll, the second sheet, the inspection register and Seredh's memory-stone account).

**Decision tags used in this package.** `[ALLOCATION]` (ED-1; bible §3.1 swap layer): every node naming the ceremonies-office valve order, Sarne Ardane, Ralenne's scene or the EH-M1 choice wording. `[ED-20]`: the EH-M2 prerequisite and the "warden's hand" offer line. `[ED-7]`: the EH-M3 cross-region gate and its variant lines. (ED-3, ruled 2026-11-15): the chamber roll's one legible line names the initiate, **Iven Calder**; the name appears in the roll document and the journal entry only, is spoken nowhere in Emberholt, and its significance is not explained before CV-M4 (R19). `[ED-12]`: protected Volkhari testimony (Maeryn's heritage, Seredh's stone). `[ED-2]`: the containment interaction used for Tavi's flare (a child, never a combatant). `[ED-14]`: the reversed broadsheet phrase. D-E2 and D-S1 (both ruled 2026-11-15) do **not** apply to Act I: no Act I node depends on Thalan's fate or on what the Speaker knows. Act I never names Thalan and never shows him; the second sheet's "one elder taken in the purge after; held below" is past tense and says nothing about now (R10 belongs to EH-M4).

---

## Act I header

### What Act I does

The player arrives in Emberholt as an outsider and leaves Act I knowing three things: that the city's heat can be read and mended, that its schools are good at their work and are also measuring which children can be pushed, and that the "forge collapse" under Cinderwall was a ritual that ended the war. Act I's job is to make the player competent in Emberholt's readable system (heat: tells, vent breath, cooling niches, heat follows the room) and in its civic habit (read the tell, not the talk), and then to turn that competence on the Glassed Hollow, where the evidence stops being about a ward's allotment or a school's test and starts being about what the city did to end its war.

| Quest | The player learns | By doing |
|---|---|---|
| EH-M1 **Cold Ward** | Tells (clear, amber, red and crazed). Vent breath (ash lifts before the exhale). Cooling niches (never pass one without touching water). Heat follows the room. The valve board and its "old leaks". That the ward's heat went to a festival rehearsal because a salon asked, and that the warden who protested was blamed. | Walking the Undercroft line with a blamed warden, reading a shut junction, finding a cut page and the clerk who cut it, putting an order in front of the woman whose name is on it, forging a seat ring, and bleeding three cocks in the order the tells show while Cinder Wraiths form at every exhale. |
| EH-M2 **The Ember in Every Hand** | That every child in Emberholt learns fire well, and that the test which sorts them was changed from above: "a lens for pushing, not seeing". That some students go to "vigil guidance", some to Emberguard schools, and a few "for evaluation below". That a good teacher can be part of it and still strike a child's name off a list. | Helping a class light a row of lanterns on one breath, making heat mitts, steadying a frightened student through a flare, carrying a lens to the woman who knows glass, reading a ledger in a records room above a rat-filled cellar, and deciding where that ledger goes. |
| EH-M3 **The Hollow That Should Not Burn** | Flarecap (orange cap, live vein: do not strike). That the Embermind Echo shows fire and changes nothing; read the tells, not the vision. That the "forge collapse" was a ritual circle with people held at its rim and someone placed at its centre; that it was meant to end the war and did; that a child walked out of the fire; that the hands on the lower forge shift above it were never counted. | Carrying a recovery warrant past a Deepbrand post, following a frightened man into the gallery where his crew died, cutting or crawling round a glassed fall, crossing the Hollow while it shows a night that did not happen to you, reading a circle that was never a forge, bleeding a heat pocket under a Revenant's pressure, and setting a glassed roll beside the place it came from. |

**Act I turn (Arcs §3.3; bible §8.3 misunderstanding ladder):** the player moves from "a careless warden" and "strict, proud schools" to "an order that followed influence" and "a test changed from above", and from "a forge collapse" to "the Glassed Hollow". The last thing the player sees in Act I is the old lower forge's memorial plaque: chalked "not a collapse" by the foreman's sister, or left clean while the Grand Marshal opens a second ledger. Either way a line in the player's journal holds one name that nobody in Emberholt says aloud.

### Dependencies on other regions

EH-M1 and EH-M2 have **no** cross-region dependency (bible §6, ED-20). EH-M3 has the one consequential intersection (ED-7, Arcs §6.3).

| State read | Read by | Effect |
|---|---|---|
| `thornfell.main.03_echo_of_shatterfall` Completed (TF-M3) | EH-M3 offer gate; `EGH-D2.40` | **Alternative gate** with MR-M2 (either opens EH-M3 once EH-M2 is Completed). Optional dialogue option comparing the cut to a proud record proved partial. Darven answers only about his own crew. Changes no step. |
| `mire.main.02_banners_that_refuse_to_fall` Completed (MR-M2) | EH-M3 offer gate; `EGH-D2.43` | **Alternative gate** with TF-M3. Optional dialogue option comparing the breathing walls to an impression that was not a witness. Darven answers only about his own crew. Changes no step. |

No Lowmark flag is read. No other Thornfell or Mire flag is read in Act I. `MDS09_READ` (ENW) and `TAS_ACCOUNT` (ESR, EH-M6) are read only by side quests and EH-M6. No Emberholt package reads a Thornfell or Mire standing flag.

### Region flags (bible §9.1 only)

| Flag | Act I role |
|---|---|
| `EH_TELLS` | **Set** by EH-M1 (`S01_line`, at the end of Veska's tell lesson, `ECW-D2.20`). Turns on the state word in every tell's inspect text in Emberholt. Read by EH-M2, EH-M3 and every later package. |
| `EH_COLD_WARD` = posted / settled `[ALLOCATION]` | **Set** by the EH-M1 choice. Read by EH-M2 (`EEH-D1.03` variant), EWA, EFC, EH-M6 tally board. |
| `EH_CURRICULUM` = guild / evidence | **Set** by the EH-M2 choice. Read by EH-M3 (`EGH-D7.08` variant), ETB, EH-M6, CV-M4. |
| `EH_HOLLOW_TRUTH` = told / kept | **Set** by the EH-M3 choice. Read by memorial props (EP11), ENW, EH-M6, CV-M1. |

Act I invents no other `EH_` flag. Quest-local flags use `ECW_`, `EEH_` and `EGH_`. Those read by later packages are listed in each quest's flags table under "Read by (later packages)". Every flag has exactly one writer.

### Quest-item budget (bible §9.4: five for the whole of Emberholt)

| Item | Quest | Fate |
|---|---|---|
| `EEH_ledger` (the Molten Stair assessment ledger, one bound volume) | EH-M2 | Taken from the academy annex in `S05`. Removed at `S07`: with `guild`, given to Idra Callow for the teachers' guild; with `evidence`, locked in Yorven Khelt's strongbox at Cinderwall (in EH-M6 Yorven lays it on the tally board's ledge as a world prop, inspect only, and returns it to the strongbox; it is never granted again as an item; CV-M4 custody from there). Not droppable, not sellable. |
| `EGH_roll` (the chamber roll and the second sheet in their wrapper, one bundle) | EH-M3 | Signed out under Kaevren's warrant from the Red-Lit annex in `S07` (Marenya Silvertide writes the signing-out in the shelf book). Removed at `S08`: Kaevren returns it to the annex shelf under his seal in both outcomes. The Iven Calder line is copied into the player's journal at `S07` and stays there (ED-3, ruled 2026-11-15). Not droppable, not sellable. |

**Act I total: 2 of 5.** Everything else is a carry-state object (the cut protest page, Ralenne's reopening order, the seat ring, the test lens, the crew's tags, the Deepbrand work order), an inspectable world object (tells, the valve book, the tally board, the slate, Maeryn's mending book, the circle, the inspection register), or knowledge carried in flags.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| EH-M1 | **read tells and repair the line**; follow a paper trail | A civic repair job across one ward, one valve house and one terrace. Combat is small and in the ducts until the set piece, where it is the frame for valve work. |
| EH-M2 | **assist and observe**; make gear; read a ledger | A school story with almost no combat (one cellar). The set piece is a containment, not a fight: a frightened child is never an enemy. |
| EH-M3 | **descend and recover**: read the glass, cross the Hollow, recover the roll | A dungeon descent with a guide who will not go the whole way, a traversal under a false vision, a miniboss bound to a heat pocket, and an archive at the end. |

No two quests share a set piece. Combat changes family across the act: Cinder Rats, Slag Beetles and Cinder Wraiths (EH-M1) → Cinder Rats only (EH-M2) → Deepbrand Crews, Ashfall Revenant glasswalkers and the Hollow Revenant (EH-M3). The readable system changes job: EH-M1 **teaches** tells, vents and niches and uses them to repair; EH-M2 shows heat following the room in a person (Tavi's flare, the lanterns); EH-M3 adds flarecap and makes the player trust the tells against a vision.

### Unlocks across Act I (bible §7)

| After | Unlocks |
|---|---|
| EH-M1 | *The Water That Did Not Arrive* (EWA), *Sound Stock* (ESK), *The Flarecap Seam* (EFS), *Wardens' Quarrels* (EWQ), *Shift Supper* (ESP), *Soot and Hide* (ESH), *The Ward That Answers Its Own Bell* (EBL), *The Seven Repairs* (ESR); EH-M2 `[ED-20]` |
| EH-M2 | *Stitches in the Lining* (EST), *Old Plate* (EOP), *The Flame That Would Not Die* (EFD); *The Old Methods* (EOM, also needs ESK); *First Cooling* (EFC, also needs ECN); EH-M3 (also needs TF-M3 or MR-M2) `[ED-7]` |
| EH-M3 | *The Vein-Touched Man* (EAD), *The Half-Name Wall* (ENW); *The Memory-Stone* (EMS, also needs ETB); EH-M4 |

### Act I clocks and conventions (bible §1.1, §9.2, §9.4, §11.1)

| Convention | Act I use |
|---|---|
| **Presentation hour / keep watch** (Lowmark) | Per-player hour (morning, noon, dusk, night), advanced by quest events and by the keep-watch interaction at marked benches and cooling niches. Never world time. EH-M1 uses it in the vent gallery (wait in a niche for a Surging zone to turn), at the Cooling House bench (crew fits the seat ring overnight). EH-M2 uses it at Maeryn's shop (mitts route), before the test (the test runs in the morning). EH-M3 uses it nowhere on the required path. |
| **Heat states** (bible §9.2; EI-HT-01 fallback) | Each heat zone has three states (Cool, Working, Surging) shown by its tells. **Act I pins every state it needs** (the quest-pinned fallback), so nothing here waits on the per-zone schedule being built. A state swaps hazard volumes, vent timings and tell props. |
| **Tells** | Taught in EH-M1 `S01`. Clear = Cool (walk), amber = Working (walk, light periodic damage, touch water at the next niche), red with a crazed skin = Surging (do not pass, do not touch). |
| **Vent breath** | Taught in EH-M1 `S01`. Ash lifts off the grate ~1.5 s before each exhale; the exhale deals damage and a one-step knock-back over the grate. Walk on the rest. |
| **Cooling niches** | Taught in EH-M1 `S01`. Blue-washed alcoves with a quench trough; standing in one stops periodic heat damage. Keep watch is always available in a niche. |
| **Heat follows the room** | Shown in EH-M1 `S00` (the Cooling House hood) and EH-M2 `S03` (Tavi's flare; the lanterns). An authored state change on a quest step, answered by a quench, a closed damper or a steadied breath. Never a meter. |
| **Resonance re-forming** (Lowmark drift-site model; bible §2.7) | Cinder Wraiths and Ashfall Revenants are defeated at 0 HP and re-form on their site's trigger (a vent's exhale, a pocket's pulse) while the condition lasts. The condition, never their health, decides. |
| **Channelled interactions with kept progress** | Bleeding a cock, fitting a seat ring, shutting a damper, steadying a breath, unbolting a seal plate, cutting a fall, bleeding a pocket. A hit interrupts the current segment; completed segments are kept. |
| **Interact sequence with harmless reset** | The three cocks (EH-M1): a red cock refuses the hand with a scald and a step of knock-back; the sequence never resets. |
| **Carry-state objects** | The cut page, the reopening order, the seat ring, the lens, the crew's tags, the work order. A held prop and a quest-state flag; not inventory items; cannot be dropped by a hit. |
| **Per-player props** | Tells, the junction, the dampers, the pocket, the memorial chalk, the Cooling House board. Co-op: each player's own state decides their own heat zones, interactions, step and credit; any shared state shown is a presentation fallback only (bible §9; MI-CO-06 pattern; CDR-6) and never decides another player's progression. |
| **Agility triggers** | Optional shortcuts only (a duct ledge in the Undercroft; a step across the drain's culvert in EH-M3), each with a walkable fallback. |
| **Address** (bible §5.3 rule 8) | "Outsider" or "traveller" before EH-M1 `S06`; "warden's hand" from those who saw or heard of the ward reopened (Cinderwall NPCs, Veska's crew, Odile, Hennet, Yorven, and from EH-M2 on, Jessa). Nothing else changes. Origin-neutral (D-3). |

---
---

# Part A: EH-M1 Cold Ward (`ECW`) `[ALLOCATION]` where tagged

## A1. The quest in one paragraph

The player comes into **Cinderwall** on an evening when a ward built on volcanic heat is cold. People who have never owned a coat are wearing two. In the **Cooling House**, **Hennet Ulm** puts a bowl in the stranger's hands and says the warm air is "following the room upstairs"; the room is shouting at **Veska Dunmor**, the fire warden whose junction went dark, and the tell in the hearth hood goes amber with it until Hennet bangs a ladle and the room, and the tell, go quiet. **Yorven Khelt**, the District Overseer, needs an outsider to walk the line with Veska "so nobody can say a warden checked a warden". Down the Undercroft stair, past the old lower forge's memorial plaque, Veska teaches the player to read **tells**, to walk on a vent's rest and to touch water at every **cooling niche**, through ducts full of Cinder Rats and Slag Beetles. On a junction door someone has pasted a broadsheet: *"When the passes go dark, the forges go cold."* The junction is not broken. It is shut, chained, with a brass tag that reads *ceremonies office*, and Veska's own chalk slate says *Shut on order. Protested. Overruled.* While the player reads it, the pipes sob, once, like someone crying; Veska, without looking up, says "Pipes do that." Up at the **Gate Valve House**, **Odile Prace** shows the valve book: the order signed by **Sarne Ardane** in the Magistrix's name, moving Cinderwall's allotment to the **Ash Terraces** for nine nights of High Kindling rehearsal; the page after it numbered wrong, a stub where Veska's protest was. The night clerk cut it and could not bring himself to burn it. On the terraces, warm under banked braziers, **Ralenne Kharveil** reads the order she never read, Sarne says "It was nine nights", and Ralenne countersigns a reopening. The junction's seat ring warped when it was shut hot; the player forges a new one at the Cooling House's small forge or waits a night for the crew. Then Veska opens the wheel, the junction surges, **Cinder Wraiths** form at every exhale, and the player bleeds three cocks in the order the tells show until the ward's heat comes up the stair. At the Cooling House the ward asks what it should be told: **post** the order and the cut page on the board, or **settle** it quietly for a fixed allotment and Veska's name cleared in the book. As the player leaves, a small figure watches from a vent grille, and is gone.

**What the player should remember:** the sob in the pipes and Veska not looking up; Sarne's "It was nine nights." **What the player should want next:** why the board has never balanced, and what else in this proud city follows influence.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A sabotage mystery: someone broke the junction.** | Rejected. ED-1: the present cause is allocation by influence with no Remnant and no villain. A saboteur would make the cold ward a crime instead of a habit. |
| **B. The player repairs the junction first and learns the cause afterwards.** | Rejected. The ward needs to know why before it gets warm, or the account in `S07` has nothing to weigh. The repair would also need the order lifted, which needs Ralenne. |
| **C. Ward meeting → walk the line (teach heat) → the shut junction → the valve book and the cut page → the Magistrix → the seat ring → the surge → the account** (selected; the bible brief). | **Selected.** The readable system is taught on the way to the evidence; the paper trail goes through living witnesses (Odile, the night clerk, Sarne, Ralenne) and objects (the slate, the book, the stub, the page); the repair needs both the countersign and the player's hands; the set piece is valve work under pressure, not a damage race. |

## A3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Yorven Khelt: Cinderwall's civil governor; blunt, loyal to his district; rose from miner; keeps Deepbrand and Emberguard heavy-handedness out; has seen vein surges that contradict official safety; knows older tunnels | Character file §24; Factions; bible §5.1 | [CANON] |
| Ralenne Kharveil: overseer of civic rituals; theatrical; sincere about morale; receives script "suggestions" she believes inspired; unaware of conditioning | Character file §20; bible §5.1 | [CANON] |
| The Ash Terraces: ceremonial platforms; public demonstrations; rallies | Dossier §VI.2 | [CANON] |
| Ashspire Ward: political salons advising the Speaker | Dossier §VII.4 | [CANON] |
| Cinder Rats (glow when agitated), Slag Beetles (burst into sparks), Cinder Wraiths (resonance distortions caused by emotional surges in ember veins; not undead, not conscious) | Dossier §XII; bible §2.4, §10 | [CANON] families |
| Street colour code: yellow calm, orange productive, red volatile | Dossier §VII.2 (Cinderweave banners) | [CANON] |
| Hearthfires shift colour with emotional state; anger ignites faster | Dossier §III | [CANON] principle |
| Mourning rites where flames are dimmed, not put out | Dossier §XVI | [CANON] |
| The Cinder Rat: lives in old conduits; hears "one particular sobbing ember" | Character file §28; bible §2.4 | [CANON] |
| Fire wardens, the heat main, tells, cooling niches, the Gate Valve House and tally board, Cooling Houses | Bible §1.1, §2.1, ED-13 | [PROPOSAL — DIRECTOR] ED-13; [NEW] detail |
| The valve order, Sarne Ardane, the cut page, nine nights | Bible §2.3, ED-1 | [PROPOSAL — DIRECTOR] ED-1 `[ALLOCATION]` |
| The reversed broadsheet phrase | Bible ED-14; Revelation Ledger R15 | [PROPOSAL — DIRECTOR] ED-14 |
| The night clerk (Aubin Harl), the seat ring, "you don't shut hot", the red-cock rule, the hearth-hood tell | This package | [NEW] |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Cold Ward** |
| Suggested content id | `emberholt.main.01_cold_ward` |
| Arc position | Act I entry (Arcs §3.3, EH-M1: "show embercraft as ordinary civic infrastructure and class pressure") |
| Prerequisite | None (travel only). Tuned for Advanced identity (ED-10). |
| Offer | Auto-offered on first entering the Cinderwall Cooling House volume, which the Cinderwall arrival path leads to from any route (`ECW-D1`). MAP VERIFICATION REQUIRED for the approach. |
| Solo / co-op | Solo-clearable. Co-op partners share the duct fights and the surge; tells, the junction, the cocks, the seat ring, the paper trail and the account choice are per player. |
| Target length | 40–55 minutes first time |
| Combat share | ~20% |
| Dialogue share | ~30% |
| Walking the line, reading, carrying, forging, valve work, choice | ~50% |
| Skills touched | Melee or Ranged (either; neither required); Smithing ~[GD: low] (optional; the crew fits a ring overnight as the time-cost alternative) |
| Choices | How the ward's account is kept (`EH_COLD_WARD`); forge the ring or wait (`ECW_SEAT_RING`, flag only); the red route or the wait in the vent gallery (flavour) |
| Unlocks | `EH_TELLS`; `EH_COLD_WARD`; Cinderwall hub (Cooling House with respawn point, keep-watch bench, small forge, quench trough; Cooling House board); the upper Undercroft line as a route; the Gate Valve House (tally board, EME10); eight side quests (Act I header); EH-M2 |
| **Anchor** (contract) | Fire wardens (Veska, her crew); Cinderwall households (the Cooling House) |
| **World-truth row** (contract) | H23 (recovery after the war: who the rebuilt city warms), H25 (present pressure, local: allocation follows influence) |
| **Revelation role** (contract) | **Plants** R15 (the reversed broadsheet phrase on a junction door; unattributed, never explained; CV-M2 owns it, ED-14). **Plants** the EH-M6 shortfall seed (the tally board's "old leaks", `ECW_SHORTFALL_SEEN`). Passes the R09 seed (the memorial plaque, unremarked). Owns nothing. |
| **Recurring evidence** (contract) | Three independent custodians: the valve book (Odile's custody: the order page and the stub where page forty-two was cut), Veska's chalk slate at the junction, and the cut protest page (kept by the night clerk, recovered in `S03`). The valve book and the tally board recur in EH-M6 (the account). |
| **State compliance** (contract) | Inactive / Active / Completed. No step can fail; a Surging zone can always be waited out in a niche; a red cock refuses the hand harmlessly; the Smithing hook has an overnight wait. Choice recorded in `EH_COLD_WARD`. Resume at the persisted step with a hook at the Cooling House (Hennet), the junction (Veska) or the valve house (Odile). |
| **Combat compliance** (contract) | Cinder Rats, Slag Beetles and Cinder Wraiths, each defeated at 0 HP. The Wraiths re-form at each vent exhale while any cock is unbled (place condition, never health); bleeding the last cock ends the condition and any Wraith still standing fights on to 0 HP. Melee or ranged; ranged never required. Every fight solo-tuned. No SX. No defeated enemy gives testimony. |

## A5. The places

### A5.1 Cinderwall [EP02, CANON ward; NEW detail]

Emberholt's lowest working ward, beside the Emberfall Dross (bible §1.2; Cinderwall is unplaced in the dossier). Terraced tenements of black stone with brass vent hoods on every lintel; slag lanes; shift bells (EME06). Tonight every hood is dark. **MAP VERIFICATION REQUIRED** for every placement below; relative order only: the ward's arrival lane → the Cooling House → the Undercroft stair head beside the old lower forge's walled yard.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W1. The arrival lane** | Arrival barks. | People in two coats, one over the other. A child trying to light a doorway lantern with two fingers and getting a thin, cold flame (EME01, gone wrong). Mood banners on the lane all grey (EME02). |
| **W2. The Cooling House** | Offer (`S00_offer`); seat ring (`S05`, yard forge); account (`S07`). | A long, low hall with benches, a cook-hearth under a brass hood, a quench trough by the door, a **board** on the wall for notices (rotas, a lost cat, a shift supper list). In the hood's lip is an emberglass **tell**, a bead the size of a thumbnail. In the yard behind: a **small forge** (anvil, mandrel horn, bellows, quench tub), the crew's stock chest, a **keep-watch bench**. The respawn point. |
| **W3. The Undercroft stair head** | Start of the line (`S01`). | A stone stair going down beside a high wall. On the wall, at eye height, a bronze **memorial plaque** for the old lower forge (EP11; EDS09 surface layer). The stair has a blue-washed cooling niche at its foot. |

### A5.2 The Cinderwall Undercroft [EP15, NEW]

The heat main's ducts and junctions below the ward. Stone ducts tall enough to walk in, iron pipe runs along the walls, grates in the floor. Every hood, junction and valve has a tell. **MAP VERIFICATION REQUIRED:** relative order from the stair: the stair niche → the duct run → the vent gallery (two ways) → the junction door → the Cinderwall junction.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **U1. The stair niche** | Tell lesson; niche lesson (`S01`). Respawn point for `S01`–`S02`, `S05`–`S06`. | A blue-washed alcove with a quench trough and a ladle on a chain. Three tells on the duct mouth beyond: one clear (a cool spur), one amber (the working main), one red and crazed (a capped surge line, chalked "NO"). |
| **U2. The duct run** | Vent-breath lesson; Cinder Rats (**ECW-E1**) (`S01`). | A long duct with floor grates every twenty paces. Ash on the grates. Rat runs along the pipe brackets; their fur glows when they are frightened. An optional **agility** ledge along the pipe run (walkable fallback along the floor between grates). |
| **U3. The vent gallery** | Slag Beetles (**ECW-E2**); the red route (`S01`). | A wide gallery where the main crosses a vent field. Two ways on: the short way across a **Surging** zone (red tell, heat shimmer, slag dripping from the roof) and the long way round a side duct where the beetles nest. A cooling niche at the fork. |
| **U4. The junction door** | The broadsheet (`S01`) `[ED-14]`. | An iron door with a warden's chalk board beside it. Pasted across the door, a damp broadsheet with one line in big type. Old paste under it where other things have been pasted and torn off. |
| **U5. The Cinderwall junction** | The shut junction (`S02`); fitting the ring (`S05`); the surge (`S06`). | A round chamber where the main splits to the ward. A great **valve wheel**, chained, with a brass tag. Beside it Veska's **chalk slate** on a nail. A **manifold** along one wall with three **bleed cocks** (left, centre, right), each with its own tell. Two floor vents and two wall ducts that breathe. Two cooling niches with troughs. The pipes run up through the roof toward the ward. |

### A5.3 The Gate Valve House [EP26, NEW] at Embergate [EP01, CANON]

Inside the main gate (bible §4.2 route order: Cinderwall's main runs past it). **MAP VERIFICATION REQUIRED.**

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **V1. The public hall and the tally board** | The board (`S03`); EME10. | A high hall open to the gate street. The **tally board**: slate panels in a wooden frame, one column of intake (vents and veins, by name), one column per draw (wards, forges, baths, kitchens, the terraces), a totals row chalked every hour. The last column never balances; its foot reads *old leaks* in a hand that has written it many times. |
| **V2. The book room** | The valve book (`S03`). | Behind a counter, the **valve book** on a lectern: big, ruled, page-numbered by hand in the top corner. Order slips pinned in a rack. |
| **V3. The clerks' bench** | The night clerk (`S03`). | A bench with three tally-boxes, one per clerk, each with a name burnt in its lid. |

### A5.4 The Ash Terraces [EP23, CANON], Emberhold District

**MAP VERIFICATION REQUIRED** for the climb from Embergate.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **T1. The rehearsal terrace** | The Magistrix (`S04`) `[ALLOCATION]`. | A broad stone terrace with braziers banked high in rows. Warm, the first warm air since the gate. Lamp-bearers rehearsing a walk in pairs while a clerk reads cues. Ralenne at a lectern with her stack of scripts. Above the terrace, the glass towers of Ashspire catch the brazier light. |

## A6. Player-facing sequence

### Beat 0: The Cooling House (`S00_offer`)
**Objective:** *Speak to the Overseer in the Cooling House.*
The player comes down the arrival lane (barks `ECW-B0`) into the Cooling House. It is full. Everyone is cold. **Hennet Ulm** puts a bowl of soup in the stranger's hands before they can say anything (`ECW-D1.01`): "Sit down. You're the warmest thing in here." A regular is shouting at **Veska Dunmor**, who stands at the end of a bench with her arms folded and says nothing back. As the shouting rises, the **tell in the hearth hood** goes from clear to amber, and the hearth flame stands up tall (`ECW-D1.05`; scripted state change, **heat follows the room**). Hennet bangs his ladle on the hood: "You'll crack my hood. Sit down, all of you." The room sits. The tell goes back to clear (~3 s). Hennet, to the player: "Heat follows the room. Shout and the vent shouts back. That's why we have soup." He also says the warm air is "following the room upstairs" tonight, and does not explain.
**Yorven Khelt** comes in from the lane, loud enough to be heard over a forge (`ECW-D1.20`). He wants the junction walked tonight, and he wants a stranger to walk it with Veska "so nobody can say a warden checked a warden".
- **Accept:** the quest becomes **Active**; Veska picks up her lamp and goes to the stair.
- **Not now:** the quest stays **Inactive**; Yorven: "The ward's cold whether you help or not. I'll be here." He re-offers from the Cooling House (`ECW-D1.90`).
- **Ask why an outsider:** Yorven: "Because if a warden says it's not her fault, half this room says she would say that. If you say it, they'll argue with you instead. That's progress."
- **Optional inspect:** the hood tell (`ECW-I1`). Before `EH_TELLS` its text describes a bead; after, the state.
**Verbs:** arrive, eat, watch, talk.

### Beat 1: Walking the Line (`S01_line`)
**Objective:** *Walk the line with Veska to the ward's junction.*
At the stair head, the player passes the old lower forge's wall and its **memorial plaque**. Veska does not look at it and does not mention it. (Optional inspect: EDS09 surface text; sets `EDS09_SEEN`, the discovery's own flag, bible §7.5. Nobody in EH-M1 remarks on it.)
1. **Tells (U1).** At the stair niche Veska stops the player in front of three tells on the duct mouth (`ECW-D2.10`): "Clear is cool. Walk. Amber is working. Walk, and touch water at the next niche. Red with a skin on it like a cracked pot is surging. Don't pass it, don't touch it, don't argue with it." The player **inspects a tell** (required; any of the three). **`EH_TELLS`** is set at the end of the lesson (`ECW-D2.20`); from now on every tell in Emberholt gives its state on inspect. Her rule: **"Read the tell, not the talk."**
2. **Niches.** "Never pass a niche without touching water." The player touches the trough (interaction; required once, here; afterwards Veska barks if they pass one without, `ECW-B1.3`, no penalty). Standing in a niche stops periodic heat damage; that is all a niche does.
3. **Vent breath (U2).** The duct run is pinned **Working** (amber tells; light periodic damage outside niches). Floor grates breathe on a ~10 s cycle. Veska: "Watch the ash. It lifts before she breathes out. Walk on the rest." The exhale deals damage and a one-step knock-back over the grate. **Cinder Rats** (**ECW-E1**) come off the pipe brackets halfway down. Veska stands in the next niche with her lamp; she is never targeted.
4. **The vent gallery (U3).** The short way is pinned **Surging** (red, crazed tells; heavy periodic damage and a heat shimmer; nothing stops a player walking into it, but Veska says "Red" once and waits). Two ways on, both valid:
   - **The long way:** the side duct, where **Slag Beetles** (**ECW-E2**) nest on a vent. Fight through.
   - **Wait in the niche:** keep watch at the fork niche (one turn of the presentation hour). The short way's tells go amber; it can be walked. The beetles in the side duct stay where they are (optional fight).
   `ECW_GALLERY` = long / waited (flavour; Veska's bark varies, `ECW-B1.6`).
5. **The junction door (U4)** `[ED-14]`. A broadsheet is pasted across the door. **Optional inspect:** *"When the passes go dark, the forges go cold."* Veska: "Somebody's always pasting something." She tears nothing down. Sets `ECW_BROADSHEET_SEEN`. Nothing explains it, here or anywhere in Emberholt.
The step completes on entering the junction volume (U5).
**Verbs:** read, touch water, time, fight, choose a way, wait.

### Beat 2: The Junction (`S02_junction`)
**Objective:** *Find out why the junction is dark.*
The junction is quiet. It is not broken. The great valve wheel is **chained shut**, and a brass **tag** on the chain reads *Ceremonies office. By order.* Veska's **chalk slate** hangs on its nail: *Shut on order. Protested. Overruled.* and a date (`ECW-D3`).
- **Required inspects:** the wheel and its tag (`ECW-I6`: also notes the wheel was shut while the line was hot: scorched grease round the seat, the warden's rule "you don't shut hot"); the slate (`ECW-I7`).
- Veska, asked about the slate: "That's mine. I wrote it the night they shut it. Then I wrote it again in the book at the valve house. Then the ward got cold and everybody forgot I can write."
**The strange moment (§A8).** While the player reads the slate, **the pipes sob**: once, a long, low, broken sound through the iron, like somebody crying in another room. Veska, without looking up from her lamp, says "Pipes do that." (`ECW-D3.30`). Sets `ECW_SOB_HEARD`. Nobody explains it, here or anywhere.
Veska: "The order's in the valve book. The book's at the Gate Valve House. Odile keeps it. She'll show you. She shows anybody. Nobody asks." (`ECW-D3.40`). Veska stays at the junction ("Somebody stays with a shut junction. It's me.").
**Verbs:** inspect, read, listen.

### Beat 3: The Valve House (`S03_valve_house`) `[ALLOCATION]`
**Objective:** *Read the valve book at the Gate Valve House.* (Sub-objectives in any order.)

| Sub-objective | Where | What the player does | Sets |
|---|---|---|---|
| **The order** | Book room (V2) | **Odile Prace**, counting aloud as she chalks (`ECW-D4`), opens the valve book at the player's asking. Page forty-one: the order (document, dialogue file). *Cinderwall junction allotment to the Ash Terraces, nine nights, for the High Kindling rehearsal. By order of the ceremonies office. Signed: Sarne Ardane, for the Magistrix.* | `ECW_ORDER_READ` |
| **The stub** | Book room (V2) | **Inspect** the book's gutter (required): page forty-one, then forty-three. Between them a stub, cut close with a knife. Odile: "Somebody cut it. Not me. I'd have cut my hand off first." Asked who had the book: "Nights, it's Aubin's." | `ECW_STUB_SEEN` |
| **The night clerk** | Clerks' bench (V3) | **Aubin Harl**, the night clerk, is at his tally-box (`ECW-D5`). Shown the stub (option gated on `ECW_STUB_SEEN`), he admits it quickly and badly: the page was Veska's protest; it made the Magistrix's office look careless; pages like that get clerks moved to the slag tips. He could not burn a book page ("You don't burn a page in a valve house. It's the one thing they teach you."). It is in his box. He gives it to the player. **Carry-state object: the cut page** (document text in the dialogue file: Veska's protest, in her hand). | `ECW_PAGE_RECOVERED` |
| **The board** | Public hall (V1) | **Inspect the tally board** (required). Intake against draws, chalked by the hour. Cinderwall's column shows nothing for nine nights; the Ash Terraces' shows double. The last column never balances: its foot reads *old leaks*. Odile (`ECW-D4.30`): "The board's never balanced. That's not news, it's weather." This is the EH-M6 seed. | `ECW_SHORTFALL_SEEN` |

When the order is read Odile offers a **fair copy** of page forty-one in her hand and mark (`ECW-D4.40`: "A copy's not the book. But it's my hand on it, and my hand's good at the gate."). The copy rides with the cut page as one carry-state bundle. The step completes when all four sub-objectives are set.
**Verbs:** read, compare, ask, recover.

### Beat 4: The Magistrix (`S04_magistrix`) `[ALLOCATION]`
**Objective:** *Show the order to the Magistrix on the Ash Terraces.*
The terrace is warm. Braziers are banked high in rows; lamp-bearers rehearse a walk in pairs; a clerk reads cues. **Ralenne Kharveil** is at her lectern with a stack of scripts, delighted to have an audience (`ECW-D6.01`). **Sarne Ardane** stands at her elbow with the cue book.
The player shows the order copy and the cut page (dialogue options gated on the carry-state bundle). Ralenne reads the copy, then reads it again (`ECW-D6.10`). She did not read it before; it went out in her name. She reads the cut page and goes quiet. Then she turns to Sarne.
**Sarne Ardane** admits it at once, in a polished voice that does not quite hold (`ECW-D6.20`): an Ashspire salon asked the ceremonies office for "a warm rehearsal"; he signed the valve order for her; the warden's protest was "a formality". "It was nine nights." (He does not name the salon. Ralenne does not ask him to in front of the player.)
Ralenne is dismayed and sincere (`ECW-D6.30`): "I make ceremonies so people feel they belong to one city. I have spent nine nights warming a terrace for a walk while a ward wore two coats." She **countersigns a reopening** on the spot (carry-state: *the reopening order*, `ECW_COUNTERSIGNED`), and says she will come down to Cinderwall to hear what the ward wants said (sets up `S07`).
- **Optional, `[ALLOCATION]`:** ask Sarne why the warden's protest was not read. "It was read. It was answered. Overruled is an answer." (beat) "I didn't know it would be cold. I didn't go down to look." This is the whole of his villainy.
**Verbs:** show, listen, ask.

### Beat 5: The Seat Ring (`S05_seat_ring`)
**Objective:** *Make the junction fit to open.*
At the junction, Veska reads the reopening order, takes the chain off the wheel, and tries it. It turns a quarter and binds (`ECW-D7.01`). The **seat ring** under the wheel warped when the junction was shut while it was hot ("You don't shut hot. I wrote that too."). The player inspects the warped ring (required; `ECW-I8`) and takes it as a pattern (carry-state).
Two ways, both complete the step:
- **Option A (skill): forge a seat ring** (**Smithing ~[GD: low]**) at the Cooling House yard's small forge (W2). Take a ring blank of imported bar stock from the crew's stock chest (Veska: "Timber's dear, iron's dearer. Don't spoil it."). **Heat** it in the forge until the forge's own tell shows amber (one interaction; ~4 s); **shape** it on the mandrel horn against the old ring (a 2-segment channel, ~3 s each); **quench** it in the yard tub (one interaction). Carry it down and **fit** it at the junction (a 2-segment channel beside Veska). A shaping segment interrupted by nothing at all cannot fail; a ring left too long out of the fire before shaping simply needs reheating (one interaction). Hennet watches from the yard door: "Ring it twice. Durnan's lot always ring it twice." (seeds ESK). `ECW_SEAT_RING` = self.
- **Option B (time-cost): the crew fits one.** Veska sends to her crew; a ring is cut at the guild yard overnight. The player **keeps watch until morning** at the Cooling House bench (one interaction; the presentation hour goes to morning), then meets Veska at the junction, where her crew is fitting it (`ECW-D7.30`). `ECW_SEAT_RING` = crew.
The step completes when the ring is seated (the wheel turns freely to the stop and Veska holds it shut, ready).
**Verbs:** inspect, heat, shape, quench, fit, or wait.

### Beat 6: The Surge (`S06_surge`): *the set piece*
**Objective:** *Bleed the junction while Veska opens it.*
Veska explains the job in three lines before she touches the wheel (`ECW-D8.01`): "When I open her, she surges. Every tell on that manifold goes up. You bleed the cocks. **Never touch a red.** Bleed the amber next to it, and the red comes down to amber. Then that one. Then the last." And: "The vents will breathe. Things come out of a surge. You know what to do with things."
She opens the wheel. The junction **surges** (§A7, **ECW-E3**): a roar up the pipes; every tell on the manifold goes up a band; two of the three cocks show **red and crazed**, one shows **amber**. Which end is amber varies each time the surge starts (left or right; never the centre). The floor vents and wall ducts begin to breathe on a ~12 s cycle, and **Cinder Wraiths** form at the vents on each exhale.
- **Bleed a cock:** a 3-segment channel (~3 s each) at the cock. A hit interrupts the current segment; completed segments are kept. On completion the cock's tell goes **clear**, steam roars out of the bleed pipe for ~2 s (a harmless plume above head height), and the **neighbouring red cock drops to amber** over ~2 s (the crazed skin fades from the edge inward).
- **Touch a red cock:** refused. The handle scalds: small damage and a one-step knock-back; Veska: "Red! Read it!" (`ECW-B6.2`). Nothing resets.
- **The Wraiths:** they form at the vents on each exhale while **any** cock is unbled, up to a cap that falls as the cocks are bled (three cocks unbled: cap 3; two: cap 2; one: cap 1). A defeated Wraith re-forms on the next exhale if the cap allows. When the **third cock** is bled the condition ends: no more form. Any Wraith still standing fights on to 0 HP.
- **Veska** holds the wheel throughout and is never targeted (non-combatant; untargetable). Her barks call the vents and the tells (`ECW-B6`).
The step completes when the third cock is bled and every Wraith is defeated. Heat comes up the pipes: the tells on the manifold all go amber (Working) and stay there; the roar becomes a hum. Far above, faintly, the shift bell rings by itself once (EBL seed; never explained here). Veska sits down in a niche and drinks from the trough ladle. "That's her." (`ECW-D8.20`). From here the player is **warden's hand** to everyone who saw or heard.
**Verbs:** read tells, bleed, fight, time the vents, stand in a niche.

### Beat 7: The Account (`S07_account`) `[ALLOCATION]`
**Objective:** *Tell the ward what happened.*
The Cooling House is warm. People have taken off one coat. Hennet is serving (`ECW-B7`). **Yorven**, **Veska**, **Odile** (she has walked down from the gate, which she never does) and **Ralenne Kharveil**, with **Sarne Ardane** a step behind her, are at the end table (`ECW-D9`). The board on the wall has the shift supper list on it and an empty space.
The ward asks the warden's hand what it should be told. Veska says what she wants and does not ask for it ("I'd like my name back. I'd like it more if nobody had taken it."). Ralenne says she will stand behind either. Yorven says, "Neither of these is wrong. One of them is louder."
The **choice** (§A9.3):
- **Post it** (`EH_COLD_WARD = posted`): the player pins Odile's fair copy of the order and Veska's cut page on the Cooling House board. The room reads it. Sarne Ardane is named in Cinderwall; the room is not kind to him, and Ralenne does not stop it. Ralenne announces that her office will send coal to the ward for the rest of the season, and does.
- **Settle it** (`EH_COLD_WARD = settled`): the player gives the copy and the page to Yorven, who settles with Ralenne at the table: a **standing order** in the valve book that Cinderwall's allotment cannot be moved without the Overseer's countersign, and a line under page forty-one, in Ralenne's hand, clearing Veska Dunmor's name. The page goes back to Odile for the book. The ward is warm and quiet. Sarne keeps his post.
- **Ask Veska** returns her line ("It's not mine to say. It's my ward's. You're the one that walked it.") and the options again.
Yorven pays the warden's hand (small payment) and says the Cooling House is theirs to sit in. **Completes** on his line (`ECW-D9.80`).
**As the player leaves the Cooling House** (first exit after completion): a small figure in a soot-stained cloak and a rough glass half-mask watches from a vent grille at the end of the lane, and is gone when the player looks (event `cinderwall.rat_glimpse`; sets `ECW_RAT_SEEN`). Nobody mentions it. If asked, Hennet: "That'll be the Rat. He comes out when the pipes are talking."
**Verbs:** listen, choose, pin or hand over.

## A7. Encounters

Tuned for **Advanced identity** (ED-10). Exact levels are Gameplay Designer calls. Cinder Wraiths are resonance distortions: defeated at 0 HP, they collapse into ash and re-form only while their condition lasts (bible §2.7).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **ECW-E1** | 3 × Cinder Rat **scurrier**, 2 × **biter** | The duct run (U2), off the pipe brackets | Scurriers dart along the brackets and drop on the player; biters close and bite | **Scurrier drop:** fur flares bright orange on the bracket overhead (~1.0 s), then it drops on the spot below (sidestep). **Biter lunge:** crouches, back fur glowing (~0.8 s), then a short straight lunge-bite. | First Emberholt fight; vent-breath practice under light pressure (the fight is on the grates) | 45–70 s; 70–85% HP |
| **ECW-E2** | 2 × Slag Beetle **crawler**, 1 × **sprayer** | The side duct of the vent gallery (U3), on a vent | Crawlers butt and guard the vent; the sprayer stays on the vent lip and spits | **Crawler butt:** lowers its head and its plates glow (~1.5 s), then a short charge-butt with a small knock-back toward open floor. **Sprayer spit:** rears, abdomen swelling red (~1.0 s), then a gob of molten slag that leaves a burning patch ~4 s. **Burst:** on defeat a beetle bursts into sparks (canon) in a 1-pace ring (~1.5 s glow first; light damage). | A ranged-answer enemy for ranged players; a niche at the duct mouth for melee | 50–80 s; 60–80% HP. Optional if the player waits instead |
| **ECW-E3** | Cinder **wraith** and **flare** forms at the vents, cap 3 → 2 → 1 as cocks are bled (opening mix 2 × wraith, 1 × flare) | The Cinderwall junction (U5) during the surge | Wraiths go for whoever is at the manifold; flares hang over a vent and throw | **Vent exhale (the condition):** ash lifts off the grate (~1.5 s), then the exhale (damage and one-step knock-back over the grate); a defeated Wraith re-forms in the exhale if the cap allows. **Wraith, Grasp:** its arms flare white (~1.0 s), then a two-handed lunge (sidestep). **Wraith, Flash:** body brightens and hums (~1.5 s), then a short heat burst in a 2-pace ring. **Flare, Toss:** a ball of fire swells between its hands (~1.2 s), then an arcing throw that leaves a burning patch ~4 s. | The set piece: valve work under pressure; reading tells while time and vents press | 3–4 min from wheel to last Wraith; 50–70% HP |

**Hazards (not encounters):**
- **Working zones:** light periodic heat damage outside niches. Walkable.
- **Surging zones:** heavy periodic heat damage and heat shimmer. Walkable but deadly to linger in; Veska's bark tells the player not to. A wait in a niche always turns them.
- **Vent grates:** timed exhale (damage and one-step knock-back), telegraphed by ash lift ~1.5 s.
- **Red cocks:** a scald and a step of knock-back when touched; never a reset.
- **Burning patches** from sprayers and flares: ~4 s, visible flame.

**Rules**
- **Defeat at 0 HP** (CDR-1). Rats and beetles take the ordinary defeat presentation (beetles burst into sparks). Wraiths collapse into ash at the vent grate. **No enemy is cleared by the condition ending**: when the third cock is bled, no more Wraiths form, and those standing fight on.
- **Re-forming is a place rule** (rulings §3.1.2; bible §2.7): it depends on unbled cocks and the vent's exhale, never on health or time-in-fight.
- **Melee or ranged** (CDR-2): every fight accepts both. In the surge, ranged players can thin Wraiths from a niche but must cross to the manifold to bleed; melee players fight at the manifold and use the niches between exhales. Flares give ranged players a target. Out-ranging never ends the surge: only the cocks do. Ranged is never required.
- **Combat never reveals evidence.** The order is in a book, the protest on a slate and a page, the cause in Sarne's mouth. Nothing drops from a rat, beetle or Wraith but ordinary loot (rats and beetles, where the economy allows; Wraiths nothing).
- **Non-combatants:** Veska, Yorven, Hennet, Odile, Aubin, Ralenne, Sarne and every Cinderwall citizen are never targetable. Veska is never engaged by enemies.
- **Death:** respawn at the Cooling House (W2) during `S00`, `S03`, `S04`, `S07`; at the stair niche (U1) during `S01`, `S02`, `S05`, `S06`. Defeated rats and beetles stay defeated. In the surge: bled cocks stay bled and the cap stays lowered; live Wraiths reset (ordinary leash reset); Veska re-opens the wheel when the player returns to the manifold (`ECW-B6.8`). Heat states never advance on death.
- **Co-op:** every fight shared; a defeat credits each partner whose own active step consumes it (Lowmark §8.1; CDR-6). Each partner's tells, cocks, ring and choice are their own. The cocks are per-player props; a partner may fight Wraiths at another partner's manifold, but bleeding a cock advances only the bleeding player's own step. Any shared manifold presentation is a presentation fallback only (bible §9; MI-CO-06 pattern) and never decides a partner's step or credit.

## A8. The discovery moment: the sob in the pipes

**What it is:** a long, low, broken sound through the iron, once, like somebody crying in another room. It is the "one particular sobbing ember" the Cinder Rat has sensed for years [CANON], heard by the player once (bible §2.4). It is **never explained** in Emberholt. It is not shown as power: no glow, no tell change, no UI.

| Time | Element | Spec |
|---|---|---|
| 0 s | **Trigger** | The player completes the slate inspect (`ECW-I7`). Veska is crouched by the wheel, trimming her lamp, her back half to the player. |
| ~1.0 s | **The sob** | Positional audio from the pipes running up through the roof: a breath drawn in, then a long, low, falling sound that breaks twice and stops. ~4 s. Not loud. No music under it. |
| ~5 s | **The quiet** | Ambience ducks by about a third for ~2 s: the hum of the main, a drip. The tells do not change. |
| ~6 s | **Veska** | Without looking up from the lamp: "Pipes do that." (`ECW-D3.30`). She goes on trimming the wick. |
| After | **Nothing** | No one speaks of it. The player is given no dialogue option about it in this scene. Veska's next line is about the valve book. |
| Never | **Explanation** | Asked later, Veska: "They do. Old main, new main, laid over each other. Air gets in." Hennet: "That's the Rat's sort of question." Yorven: "I was a miner. Rock makes noises. I've never liked that one." Nobody says more. |
| UI | | The camera stays with the player. No cutscene. |

**Why it is here:** it is EH-M1's unease beat (bible §1 emotional line, §11.7) and the R19 shadow at its faintest: something below the city is in pain, and the people who live on top of it have learned not to look up.

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to the Overseer in the Cooling House. | `ECW-D1` end with accept | Yes | Hood-tell state change event (`cinderwall.hood_flare`) plays on entry. Quest Active on accept; Inactive on "not now" with re-offer at the Cooling House (`ECW-D1.90`) |
| `S01_line` | Walk the line with Veska to the ward's junction. | Tell inspected + trough touched + enter junction volume (U5) | Yes | Sets **`EH_TELLS`** at `ECW-D2.20`. U2 pinned Working; U3 short way pinned Surging until keep watch at the fork niche (then Working). ECW-E1 on the path; ECW-E2 on the long way only. `ECW_GALLERY`, `ECW_BROADSHEET_SEEN`, `EDS09_SEEN` optional |
| `S02_junction` | Find out why the junction is dark. | Wheel/tag inspect + slate inspect + `ECW-D3.40` end | Yes | Sob event (`cinderwall.pipe_sob`) on slate inspect; sets `ECW_SOB_HEARD` |
| `S03_valve_house` | Read the valve book at the Gate Valve House. | `ECW_ORDER_READ` + `ECW_STUB_SEEN` + `ECW_PAGE_RECOVERED` + `ECW_SHORTFALL_SEEN` | Yes | Any order, except the clerk's admission needs `ECW_STUB_SEEN`. The fair copy is offered at `ECW-D4.40` |
| `S04_magistrix` | Show the order to the Magistrix on the Ash Terraces. | `ECW-D6` end (copy and page shown; Sarne heard; countersign) | Yes | Sets `ECW_COUNTERSIGNED`; carry-state reopening order |
| `S05_seat_ring` | Make the junction fit to open. | Warped ring inspected + ring fitted (Option A channel) or keep watch until morning + `ECW-D7.30` (Option B) | Yes | Sets `ECW_SEAT_RING` = self / crew |
| `S06_surge` | Bleed the junction while Veska opens it. | Three cocks bled + every ECW-E3 enemy defeated | Yes | Amber end randomised per surge start. Wraith cap 3/2/1 by cocks bled. Address variant "warden's hand" turns on (Cinderwall NPCs, Veska's crew, Odile, Hennet, Yorven) |
| `S07_account` | Tell the ward what happened. | Choice in `ECW-D9` + `ECW-D9.80` end | Yes | Sets **`EH_COLD_WARD`**. Carry-state bundle removed (board or Yorven). Small payment. Quest → **Completed**. Rat glimpse on first exit (`ECW_RAT_SEEN`) |

### A9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `EH_TELLS` | `S01`, `ECW-D2.20` | Every tell inspect; `S01`–`S06` | Every Emberholt package (tell inspect text) |
| `ECW_GALLERY` = long / waited | `S01` (U3) | `ECW-B1.6` | — |
| `ECW_BROADSHEET_SEEN` | Broadsheet inspect (optional) | `ECW-D2.62` | CV-M2 (request: one line, "You've seen this before, the other way round."); never explained in Emberholt |
| `EDS09_SEEN` | Plaque inspect (optional; the discovery's own flag, bible §7.5) | — | EDS09 reading layer (Batch 3); ENW |
| `ECW_SOB_HEARD` | `S02` event | `ECW-D3.31` | None (deliberately) |
| `ECW_ORDER_READ` | `ECW-D4.12` | `S03`; `ECW-D6` options | — |
| `ECW_STUB_SEEN` | Gutter inspect (`ECW-I9`) | `ECW-D5` options | — |
| `ECW_PAGE_RECOVERED` | `ECW-D5.14` | `S03`; `ECW-D6`, `ECW-D9` options | — |
| `ECW_SHORTFALL_SEEN` | Tally board inspect (`ECW-I10`) | `ECW-D4.30` | **EH-M6** (the accounting: "You read this board once. Read it again."); EWA |
| `ECW_COUNTERSIGNED` | `ECW-D6.34` | `S05` | — |
| `ECW_SEAT_RING` = self / crew | `S05` | `ECW-D8.22` | ESK (Durnan: "You made a seat ring for Dunmor. Show me.") with `self` |
| `ECW_RAT_SEEN` | Exit event after completion | `ECW-B9.6` | EH-M5 (the Cinder Rat: "You looked back. Most don't.") |
| `EH_COLD_WARD` = posted / settled `[ALLOCATION]` | `S07` choice | `ECW-D9.40`–`.66`, `ECW-B9` | EH-M2 (`EEH-D1.03`); EWA; EFC; EH-M6 tally board (§9.3 item 2) |

### A9.3 Choice: how the ward's account is kept `[ALLOCATION]`

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Posted** (`EH_COLD_WARD = posted`) | The order copy and Veska's cut page go up on the Cooling House board. The ward reads them. Sarne Ardane is named in Cinderwall. Ralenne owns it in the room and sends coal for the season. | Sarne is shamed in a ward he will never visit again; Ralenne's office is embarrassed in public, and she lets it be. Some regulars say Veska should have shouted louder (barks). | EWA's rota argument cites the board. EFC: Hennet reads the page aloud at First Cooling. EH-M6: the Cooling House regulars stand behind Veska at the tally board. |
| **Settled** (`= settled`) | A standing order in the valve book: Cinderwall's allotment cannot move without the Overseer's countersign. Veska's name cleared under page forty-one in Ralenne's hand. | The ward never reads why it was cold; the gossip about Veska takes longer to die (barks). Sarne keeps his post. | EWA: Yorven cites the standing order. EFC: Ralenne sends a clerk with the coal book. EH-M6: Ralenne's clerk brings the coal book to the tally board. |

**Neither is wrong.** Both reopen the ward, both clear Veska in the way the ward can hear it, and both leave the tally board's shortfall untouched.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Tell reading (`EH_TELLS`) | Knowledge | Every tell in Emberholt gives its state on inspect. Vent breath and cooling niches are taught in play (no flag). |
| Cinderwall hub | Access | The Cooling House (respawn point, keep-watch bench, quench trough, the small forge in the yard for later Smithing content), the Cooling House board (shows the outcome), the Undercroft upper line as a route |
| The Gate Valve House | Access | The tally board (EME10); Odile |
| "Warden's hand" | Address | NPCs who saw or heard of the ward reopened address the player so (bible §5.3). Nothing else changes. |
| Small payment | Currency | Yorven at `S07`. Economy tuning [GD]. |
| Skill XP | Action only [GD] | Melee or Ranged at defeat; Smithing if done personally. No lump quest XP (bible §11.6). |
| Side-quest unlocks | Story | EWA, ESK, EFS, EWQ, ESP, ESH, EBL, ESR |
| EH-M2 | Story `[ED-20]` | Journal lead on completion: *A dye-worker from the Cinderweave Quarter is asking for the warden's hand at the Cooling House.* |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player walks into a Surging zone | Heavy periodic damage; Veska's bark. Death respawns at the stair niche. A wait in the fork niche always turns the zone. |
| Player cannot or will not smith | The crew fits a ring overnight (Option B) at the cost of one keep-watch turn. Never blocked. |
| Player touches a red cock | A scald and a step of knock-back. Nothing resets. Veska's bark says why. |
| Player is beaten in the surge | Respawn at the stair niche. Bled cocks stay bled; the Wraith cap stays lowered; Veska re-opens the wheel on return (`ECW-B6.8`). |
| Player shows Ralenne the order without the page (or the reverse) | Ralenne reads what she is given and asks for the rest ("Is there a second page to this? There's always a second page."). The step waits for both. |
| Death | Respawn by step (§A7). Carry-state bundle, ring, countersign and sub-objectives persist. |
| Logout | Restore to the persisted step: the Cooling House (`S00`, `S07`), the stair niche (`S01`, `S02`, `S05`, `S06`), the Gate Valve House (`S03`), the Ash Terraces (`S04`). |
| Walking away | Quest stays Active at its step. Resume hooks: Hennet at the Cooling House ("Bowl's still warm. The ward isn't."), Veska at the junction ("Still shut. Still mine."), Odile at the valve house ("Book's open. It's always open."). |
| Fail state | None. |
| Co-op | Shared duct fights and surge Wraiths. Per-player tells, gallery state, cocks, ring, paper trail and choice. Presentation follows each player's own state; any shared junction or manifold presentation is presentation only (bible §9; CDR-6) and never decides a partner's step or credit. A partner who has completed EH-M1 is addressed as "warden's hand" in the other's `S07` and stands at the end table. |

## A12. Integration needs

Documented dependencies for a later Systems Engineer. Nothing here is implemented. Every item is a standard system unless marked.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Quest-pinned heat states** (EI-HT-01 fallback form) | Systems | Each step sets the state of the zones it uses: U2 Working (`S01`); U3 short way Surging, swapped to Working by keep watch at the fork niche (`S01`); U5 Cool until `S06`, Surging during the surge, Working after. A state swaps hazard volumes, vent timings and tell props. Per player. A pin holds only for the steps that name it; completion releases all. No per-zone schedule is needed for Act I. |
| **Tell props** | Art / world state | Emberglass bead material with three states (clear, amber, red-crazed), swapped by zone state or by a cock's own state. The crazed skin fades from the edge inward over ~2 s when a red drops to amber. |
| **Timed vents** | Gameplay | Standard timed hazard: ash-lift VFX ~1.5 s, then an exhale volume (damage, one-step knock-back), on a fixed cycle per vent (~10 s ducts, ~12 s junction). |
| **Cooling niches** | Gameplay | Safe volumes that suppress the zone's periodic damage; a trough interaction (touch water); keep-watch available. |
| **Re-form at exhale with a cap** (ECW-E3) | Gameplay | Lowmark drift-site model: spawn points at the vents re-spawn defeated Wraiths on the vent's exhale while the junction's cocks are unbled, up to a cap set by the number unbled (3/2/1/0). Live Wraiths are unaffected by cap changes and fight to 0 HP. |
| **Cock sequence** | Systems | Three cock props with tell states; the amber end chosen at surge start (left or right); a 3-segment channel on an amber cock, refused with a scald (damage, knock-back) on a red cock; completion sets the cock clear and its neighbour amber. Never resets. |
| **Hood-tell state change** (`cinderwall.hood_flare`) | Art / audio | §A6 Beat 0: the hood tell and hearth flame step up one band during the shouting and back down ~3 s after Hennet's ladle. Per player. Scripted presentation. |
| **Scripted audio event** (`cinderwall.pipe_sob`) | Audio | §A8. Positional, per player, with an ambience duck. |
| **Rat glimpse** (`cinderwall.rat_glimpse`) | NPC / presentation | A non-interactive NPC model at a vent grille on the first exit after completion; despawns on look or after ~4 s. |
| **Smithing at a small forge** | Skills / Gameplay | Existing Smithing interactions (heat, shape, quench) at a forge, anvil horn and tub; the ring blank and the ring are carry-state quest objects until the item pass defines them (ED-11). |
| **Keep-watch interaction** | Systems | At the fork niche (U3) and the Cooling House bench (Option B). |
| **Carry-state bundle** | Systems | The order copy and cut page, then the reopening order; dialogue options gated on possession. |
| **Board prop** (`S07`) | Art / world state | The Cooling House board shows the pinned copy and page with `posted`; the shift supper list only with `settled`. Per player. |
| **Agility trigger** | Systems | The duct ledge in U2; walkable fallback along the floor. |
| Creatures | Schema / Gameplay | Cinder Rat scurrier, biter; Slag Beetle crawler, sprayer; Cinder Wraith wraith, flare (bible §10). |

**New runtime needs: none.** Everything above is a standard system, the bible's EI-HT-01 fallback form or the Lowmark drift-site model.

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why the ward went cold** `[ALLOCATION]` | A ceremonies-office order signed at a salon's request; the protest cut (bible §2.3). | Veska is careless. | The tag, the slate, the order, the stub, the cut page, Sarne's admission. | Sabotage; the Remnant. | Which salon. | EH-M1 (resolved here). |
| **The sob in the pipes** | Unexplained in Emberholt (bible §2.4). | "Pipes do that." | A sound, once. | Air in an old main. | Everything. | None in Emberholt (R19 shadow, CV-M4). |
| **The broadsheet** `[ED-14]` | A planted phrase (R15). | Somebody's always pasting something. | One line on a junction door. | Ward politics; a guild complaint. | Who pasted it. | CV-M2 (R15). |
| **The board's "old leaks"** | The Remnant's draw lines (bible §2.3). | Old leaks. | A shortfall at the foot of every column, every hour. | Leaks. | Everything. | EH-M6. |
| **The plaque** | Lower-forge hands above the ritual chamber (bible §2.2). | Lost in the collapse of the lower forge. | A plaque nobody looks at. | A collapse. | Everything. | EH-M3 (R09). |

## A14. Open decisions

1. **ED-1 (`[ALLOCATION]`):** `S03`, `S04`, `S07`, the Cooling House barks and `EH_COLD_WARD` depend on the cause. The cold ward, the tells lesson, the slate, the tally board's shortfall, the broadsheet, the seat ring and the surge survive any replacement that is still "a present, local, non-Remnant reason the ward's heat went elsewhere" (bible §3.1).
2. **The night clerk (Aubin Harl) [NEW]:** the bible says a clerk cut the protest page; `S07` posts "the cut page", so this package has the clerk keep it rather than burn it, which gives the paper trail a living witness. If the Director prefers the page destroyed, the player posts Odile's copy and Veska's slate instead and Aubin's scene shrinks to the admission; `EH_COLD_WARD` is unchanged.
3. **Odile's fair copy [NEW]:** the book never leaves the valve house; the copy is what the player carries and posts. Text only.
4. **"You don't shut hot" and the warped seat ring [NEW]:** a warden's rule that ties Veska's protest to the repair. Text and prop only.
5. **The red-cock rule [NEW]:** "never touch a red; bleed the amber next to it". If the Gameplay Designer wants a stricter puzzle, the randomised amber end can become a fixed order; the beat survives.
6. **The shift bell ringing by itself after the surge:** a one-sound seed for EBL (*The Ward That Answers Its Own Bell*). Cut freely if EBL changes.
7. **Level framing (ED-10):** Advanced identity. Smithing `[GD: low]` with the overnight crew alternative.

## A15. Internal review log

| Finding | Revision |
|---|---|
| The tells lesson risked a lecture. | Three tells in a row at a niche, one required inspect, one rule ("read the tell, not the talk"), then a gallery where the rule is used to choose a way or wait. |
| "Heat follows the room" risked being abstract. | Shown in the first minute: the room shouts, the hood tell goes amber, a ladle quiets both. |
| The paper trail risked a single document. | Four holds: the tag and slate (junction), the book page and stub (valve house), the clerk and the cut page (a living witness and an object), and Sarne's admission. Combat reveals none of it. |
| Ralenne and Sarne risked villainy. | Ralenne did not read it and owns it in public either way. Sarne admits at once; his worst line is "I didn't go down to look". Neither is targetable. |
| The surge risked a damage race. | The Wraiths re-form at each exhale until the cocks are bled; the cap falls as the player works. Damage alone cannot end it. |
| CDR-1 on the condition ending. | Bleeding the third cock stops new forms; Wraiths standing fight on to 0 HP. |
| The red cock risked a fail state. | It scalds and refuses; nothing resets. |
| The sob risked becoming evidence. | No option, no tell change, no explanation; Veska's "Pipes do that" is the whole of the scene. |
| R15 risked explanation. | The broadsheet is optional, unattributed, and Veska's line dismisses it. |
| Skill hook. | Smithing `[GD: low]` with the overnight crew as the time-cost alternative. |
| Address. | "Outsider/traveller" until the surge; "warden's hand" after, from those who saw or heard. |
| Remnant. | None in EH-M1 (ED-1, Arcs "No Remnant required"). The shortfall is shown, not explained. |

---
---

# Part B: EH-M2 The Ember in Every Hand (`EEH`)

## B1. The quest in one paragraph

**Jessa Ostry**, a dye-worker from the Cinderweave Quarter with blue to the elbows, finds the warden's hand at the Cooling House: her daughter **Tavi** comes home from the Molten Stair academy with her hands shaking. "They've changed something." At the academy's practice court on the **Molten Stair**, **Theryn Dalewright**, warm and unhurried, accepts a helper ("every class needs another pair of hands"), and junior teacher **Idra Callow** runs the lesson: lantern ignition, heat pulses, ember-thread, grounding breaths. On Idra's count a whole row of children lights a row of lanterns on one breath, and the craft is good. The students' mitts are scorched through. The player makes a new set at **Brisa Teglan**'s tannery and takes them to **Maeryn Vall** to be lined with ember-thread, or fetches a set she is mending; in her shop she keeps a mending book with the scorch outlines of children's hands drawn in pencil, and she goes still when a grey-cloaked Covenant visitor passes the window. At the test the next morning, **Selice Morra**'s emberglass lenses sit on the bench, and the flame they gather is too narrow. Tavi flares. The player shuts the floor vent, steadies her breath with Idra and leads her to the cooling niche, and there, when Tavi cries, every lantern in the court dims, and when she laughs, they brighten. Selice holds the test lens to her furnace light: "This is a lens for pushing, not seeing." It was reground to a Council schedule. In the annex above the academy's heat cellar, past the Cinder Rats, the assessment ledger keeps a coded second column beside every placement, a transfer sheet to "vigil guidance", to Emberguard schools and, three times, "for evaluation below", and, beside one of those, in Theryn's hand: *Not this one.* Tavi's line is there in fresh ink: *vigil guidance, pending.* Confronted gently, Theryn defends the sorting as stewardship, goes quiet at "below", does not explain her margin, and strikes Tavi's pending line herself. Then the warden's hand decides where the ledger goes: to the teachers' **guild** through Idra, so the test changes, or into **Yorven Khelt's strongbox** as evidence for a later accounting.

**What the player should remember:** the lanterns dimming when Tavi cries; Theryn's pen going through Tavi's name. **What the player should want next:** what "below" means, and who is down there.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Expose Theryn as a Remnant recruiter and have her removed.** | Rejected. The bible (§2.3, §5.1, §13 note 13) keeps her sincere, never exposed or punished in Emberholt; the Arcs ask to reveal conditioning "without condemning teachers". |
| **B. The player learns the test is wrong from Tavi's flare alone.** | Rejected. A flare is a phenomenon; heat following a frightened child proves nothing about a test (evidence rule). The cause needs the glass read by a glasswright and a ledger read in place. |
| **C. Class → mitts and Maeryn → the test and the flare → the lens read by Selice → the ledger in the annex → Theryn → where the ledger goes** (selected; the bible brief). | **Selected.** The craft is shown as good first; the evidence comes from an object (the lens), a custodian (Selice), a record (the ledger) and a person (Theryn); the set piece is care for a child, not a fight. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Every child learns lantern ignition, heat pulses, ember-thread weaving, emotional grounding; children learn embercraft before script | Dossier §III, §VIII | [CANON] |
| Academies assess emotional volatility and sort students into civic roles; fire-control exams double as compatibility assessments | Dossier §IV, §XI | [CANON] |
| The Molten Stair: apprentice groups practising flame-balancing; teachers monitoring stability; burns expected | Dossier §VII.3 | [CANON] |
| Cinderweave Quarter: weavers, glasswrights, tannery workers; embercraft softens hides | Dossier §VII.2 | [CANON] |
| Theryn Dalewright: warm, maternal; "protecting gifted children from their own power"; funnels talent toward Hearthveil and Emberguard; dossiers on youth; hid one unstable child from Deepbrand | Character file §17; Part 4 ledger (academy dossiers only as stated); bible §2.3, §5.1 | [CANON] |
| Selice Morra: master emberglass artisan; reverent toward making | Character file §22; bible §5.1 ("speaks to the glass, not to motives") | [CANON] |
| Maeryn Vall: Volkhari seamstress in disguise; ember-resistant fabrics; ember-thread weaving; safehouse; suspects the Remnant has noticed someone in the district | Character file §48; bible §5.1, ED-12 | [CANON] |
| Hearthveil Initiates identify children with high embercraft potential; "vigil guidance" | Factions §4; bible §2.3 | [CANON]; [NEW] term |
| Emberglass lenses, the reground curve, the Council schedule mark, the coded column, the transfer sheet, "Not this one." | Bible §2.3, §6.1 | [NEW] |
| Jessa and Tavi Ostry, Idra Callow, Brisa Teglan | Bible §5.2 | [NEW] |
| Tavi's pending line; the lanterns; Maeryn lining Brisa's shells; the count-bell | This package | [NEW] |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Ember in Every Hand** |
| Suggested content id | `emberholt.main.02_ember_in_every_hand` |
| Arc position | Act I (Arcs §3.3, EH-M2: "reveal curricula as conditioning without condemning teachers") |
| Prerequisite | EH-M1 Completed `[ED-20]` (the Arcs §6 graph; bible recommendation). Tuned for Advanced identity (ED-10). |
| Offer | Next entry to the Cinderwall Cooling House after EH-M1's completion: Jessa Ostry (`EEH-D1`), then Theryn at the practice court (`EEH-D2`). Journal lead on EH-M1 completion. |
| Solo / co-op | Solo-clearable. Co-op partners share the cellar fight; the class tasks, mitts, containment, lens, ledger and choice are per player. |
| Target length | 40–55 minutes first time |
| Combat share | ~5% |
| Dialogue share | ~40% |
| Class work, making, containment, carrying, reading, choice | ~55% |
| Skills touched | Leatherworking ~[GD: low] (optional; Maeryn's mended set is the time-cost alternative); Melee or Ranged in the cellar (either) |
| Choices | Where the ledger goes (`EH_CURRICULUM`); make the mitts or wait (`EEH_MITTS`, flag only); make Tavi laugh or leave it to Idra (`EEH_TAVI_LAUGHED`, flavour) |
| Unlocks | `EH_CURRICULUM`; the Molten Stair practice court (EME04 on the stair; EME09 in the Cinderweave courtyard); Maeryn's shop; Brisa's tannery; Selice's workshop; side quests (Act I header); EH-M3 (with TF-M3 or MR-M2) |
| **Anchor** (contract) | The academies (Theryn, Idra, the practice court); Cinderweave households (the Ostrys; Maeryn; Brisa) |
| **World-truth row** (contract) | H13 (aftermath: a city that weaponized craft now teaches it to every child), H22 (the hidden order shapes civic practice) |
| **Revelation role** (contract) | **Seeds** R18 (volatility tests; the curriculum ledger as a future custodian). Shown as practice, never as a plan. Owns nothing. |
| **Recurring evidence** (contract) | Three independent custodians: the assessment ledger (`EEH_ledger`, academy custody), Selice's reading of the lens (a glasswright's account of an object), and Maeryn's mending book (a seamstress's pencil outlines of scorched hands). The ledger recurs in EH-M6 and CV-M4 (`evidence`) or in the teachers' guild's revised test (`guild`). |
| **State compliance** (contract) | Inactive / Active / Completed. The class repeats each in-game day; the test re-runs each morning until the player has assisted it; containment cannot fail. Choice recorded in `EH_CURRICULUM`. Resume at the persisted step with a hook at the practice court (Idra) or Maeryn's shop (Maeryn). |
| **Combat compliance** (contract) | Cinder Rats in the heat cellar, defeated at 0 HP. Tavi's flare is a hazard around a non-targetable child, ended by a containment interaction (ED-2 pattern); no student, teacher or citizen is ever targetable. Melee or ranged; ranged never required. Solo-tuned. No SX. No defeated enemy gives testimony. |

## B5. The places

### B5.1 The Cinderweave Quarter [EP03, CANON; NEW detail]

A packed artisan district between Cinderwall and the civic heart (bible §4.2 route order). Dye yards steaming, glass studios, a tannery that smells like a tannery anywhere. Mood banners in yellow and orange. **MAP VERIFICATION REQUIRED** for every placement below.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **C1. Brisa Teglan's tannery** | Leatherworking hook (`S02`). | Hides on frames softened over a low ember bed. A cutting bench, patterns on pegs, a stitching horse. Brisa's sign: *HIDE FIRST, HEAT SECOND.* |
| **C2. Maeryn Vall's shop** | Mitts lining or mended set; the mending book (`S02`). | A narrow shop of ember-resistant cloth: smocks, long sleeves, headwraps. A counter with a **mending book** open beside a pincushion. A curtained door to a back room (closed in EH-M2). A front window on the street. A **keep-watch** stool by the counter. |
| **C3. Selice Morra's workshop** | The lens (`S04`). | A glass studio with a small furnace, a bench of finished emberglass (masks, a teardrop lamp), grinding wheels, and a rack of old school lenses she made years ago, their rims etched with her mark. |

### B5.2 The Molten Stair [EP04, CANON]

A grand stair carved into volcanic stone, heat rising from the chasms either side; apprentice groups climbing with flames held in their palms (EME04). The academy sits on a landing partway up. **MAP VERIFICATION REQUIRED.**

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **M1. The practice court** | The class (`S01`), the test (`S03`), the choice (`S07`). Respawn point for `S01`–`S07` while on the Stair. | An open court with stone benches in rows, a **lantern rack**, a **count-bell** on a post, a **test bench** with a frame for lenses, a **floor vent** with a brass **damper** under the bench, and a blue-washed **cooling niche** with a trough in the wall. Tells in the vent hood and the niche. Every student has a practice lantern. |
| **M2. The heat cellar** | Cinder Rats (**EEH-E1**) (`S05`). | A low cellar under the court where the academy's heat comes in off the main: a duct, a vent, coal-black corners, a ladder up to a hatch in the ceiling. Rats nesting in the warm by the duct. |
| **M3. The annex** | The ledger (`S05`). | A dry records room above the heat cellar: shelves of bound volumes, a sloped reading desk, a window onto the court. The **assessment ledger** on the desk. |
| **M4. Theryn's study** | Theryn (`S06`). | A small room off the court with a window on the stair. A lamp she lit by touch. Shelves of dossiers in plain covers. A child's drawing of a lantern pinned to the wall, old. |

### B5.3 Cinderwall [EP02] (return)

The Cooling House (offer) and Yorven's office at the back of it with his **strongbox** (`S07`, `evidence`).

## B6. Player-facing sequence

### Beat 0: Jessa (`S00_offer`) `[ED-20]`
**Objective:** *Speak to the dye-worker at the Cooling House.*
**Jessa Ostry** is waiting on a bench with her arms blue to the elbows (`EEH-D1`). She calls the player "warden's hand" because the ward does: "You walked the line for Dunmor. Walk up the Stair for me." She tells it plainly: Tavi is nine; she loves the class; since the new term she comes home from the volatility tests with her hands shaking, and the scorch marks on her mitts are on the inside now. "They've changed something. I can't tell you what. I dye wool."
- **Accept:** the quest becomes **Active**; journal: *Go to the academy on the Molten Stair.*
- **Not now:** Jessa: "The test's every morning. It'll still be there. So will she." Re-offered at the Cooling House (`EEH-D1.90`).
- **Variant (`EH_COLD_WARD`):** posted, "I read the board. Nine nights. I thought, somebody wrote that down, and somebody else read it." Settled: "Dunmor's name's clear in the book. I heard. I don't read books."
At the practice court, **Theryn Dalewright** meets the player at the gate (`EEH-D2`), kind and unhurried. She accepts a helper ("Every class needs another pair of hands. Idra's need two."). She asks nothing about where the player is from. The step completes on her line.
**Verbs:** listen, accept, climb.

### Beat 1: The Class (`S01_class`)
**Objective:** *Help Idra Callow with the lesson.*
**Idra Callow** runs the morning class (`EEH-D3`): twenty students on stone benches, ages about seven to twelve. **Tavi Ostry** is in the second row and waves at the player because her mother told her someone might come. The lesson is shown as good craft taught well. The player's three jobs, each a standard interaction, any order:
1. **Hand out the lanterns.** Carry the practice lanterns from the rack to the benches (one carry interaction for the tray; one place interaction per bench row, three rows).
2. **Hold the shield.** A small boy's lantern keeps flaring tall. Idra asks the player to hold the brass shield-frame round it while she coaches his breath (a 2-segment channel, ~3 s each). On the second segment his flame settles. He looks up at the player as if they did it. Idra: "He did it. You held the frame." (`EEH-D3.20`).
3. **Ring the count.** For the grounding breaths Idra raises her hand; the player strikes the **count-bell** (interaction prompted by her raised hand, three times). If the player is slow, Idra laughs: "Close enough. Breath doesn't mind." Nothing fails.
When the three jobs are done Idra calls the last exercise: **lantern ignition on one breath**. On her count, a whole row of children breathe in together, touch their lanterns, and twenty small flames come up at once and hold, steady and yellow (presentation event `stair.row_lit`; the court's vent-hood tell steadies to clear). Theryn, at the rail, smiles at it the way people smile at things they love. The step completes. Sets `EEH_CLASS_DONE`.
**Verbs:** carry, hold, ring, watch.

### Beat 2: Mitts (`S02_mitts`)
**Objective:** *Get the class a set of heat mitts for the test.*
After the class Idra shows the player the students' **mitts** (inspect, `EEH-I3`): canvas and thin hide, scorched through on the inside of the palms, in the shape of fingers. "They burn from the inside out now. They didn't, last year." She needs a set for tomorrow's test.
Two ways, both lead through Maeryn's shop and both complete the step:
- **Option A (skill): make heat mitts** (**Leatherworking ~[GD: low]**) at **Brisa Teglan**'s tannery (C1; `EEH-D4`). Brisa: "Hide first, heat second." **Cut** the palms and backs from a softened hide on her pattern (one interaction), **stitch** them on the horse (a 2-segment channel). Brisa looks at the result: "Good shells. They'll scorch through at the palm in a week. Children's hands run hotter than you'd think. Take them to Vall. She lines them." The player carries the shells to Maeryn's shop; Maeryn lines them with ember-thread while the player waits at the counter (a short wait, no keep watch: the conversation runs while she works). `EEH_MITTS` = self.
- **Option B (time-cost): fetch a mended set** from Maeryn's shop. Maeryn has a class set in for mending; it is not finished. The player **keeps watch** on the stool by her counter (one turn) while she finishes. `EEH_MITTS` = maeryn.
**At Maeryn's (either route)** `[ED-12]` (`EEH-D5`): **Maeryn Vall**, warm and quick, asks the hand sizes. She turns her **mending book** round on the counter to show the player (required: inspect, `EEH-I5`): page after page of pencil outlines of small hands, traced round scorched mitts brought in for mending, with the scorch drawn in as shading. The newest pages are darker in the palms. "I draw them so I get the size right. And then I can't stop looking at them." Mid-scene, **a grey-cloaked Covenant visitor** passes the front window slowly, looking in (presentation event `cinderweave.grey_visitor`). Maeryn's hands stop on the thread; she does not look up until the visitor has gone (~4 s); then she goes on as if nothing happened. If the player asks, she says "A customer who doesn't buy anything" and changes the subject. **Nothing about her heritage is said, shown or asked** (ED-12; bible §5.3 rule 6); the player cannot press it. Sets `EEH_MENDING_BOOK`.
The step completes when the player has the lined mitts (carry-state) and has seen the mending book.
**Verbs:** inspect, cut, stitch, carry, wait, look.

### Beat 3: The Test (`S03_test`): *the set piece*
**Objective:** *Assist at the volatility test.*
The test runs in the morning (if it is not morning, keep watch at the court bench; the test re-runs each morning until assisted). The player gives out the mitts (one interaction at the bench). **Theryn** examines; **Idra** assists; the player's job is the **floor-vent damper** under the test bench and whatever Idra asks. On the bench, in a brass frame, sit **emberglass test lenses** (inspect, `EEH-I6`: "Each lens is ground thick at the centre. The rim is etched with a small mark and a number."). One by one, students hold a small flame behind a lens while Theryn reads the light it throws on a white card: how far the flame spreads, how steady it stays. Two students pass. The light on the card is a tight, bright point, not a spread (the player can see it; Idra frowns at it).
**Tavi's turn.** She holds her flame behind the lens. The point on the card goes white. Her flame stands up past her hand. She makes a small frightened sound, and **she flares** (`EEH-D6.20`; ED-2 pattern): a hazard zone ~4 paces round her (periodic heat damage; heat shimmer; the vent-hood tell goes red and crazed; the benches near her smoke). Tavi is **never targetable**; nothing in the court is. Theryn calls the class back calmly and they go, in a line, as they have practised. **Containment** (three channelled parts, any order; progress kept; each completed part shrinks the zone by a third):
- **Cool the vent:** shut the floor-vent **damper** under the test bench, inside the zone's edge (a 2-segment channel, ~3 s each). The vent is feeding her flare. Shut, the zone's heat drops a band.
- **Steady the breath with Idra:** Idra kneels by Tavi and counts; the player kneels on her other side and strikes the hand-bell on Idra's count (a 3-segment channel, each segment ending on Idra's "three", ~4 s each). Tavi's breaths come back into the count.
- **Lead her out:** when the first two are done, take Tavi's hand (interaction) and lead her to the **cooling niche** (escort-follow, short; she walks with the player and stops when they stop).
The containment cannot fail. Standing in the zone costs health; a player who goes down respawns at the court rail with every completed part kept, and Idra holding Tavi's hands.
**The strange moment (§B8.1).** In the niche, Tavi starts to cry. **Every lantern in the court dims** at once, down to a coal (`stair.lanterns_dim`). The player has one option (`EEH-D6.40`): say something to make her laugh (a joke option), or say nothing. With the joke, Tavi laughs, hiccuping, and **every lantern brightens** back, all together. With nothing, Idra pulls a face at her and Tavi laughs at that instead (same brightening). Nobody says anything about the lanterns. Sets `EEH_LANTERNS_SEEN` (always) and `EEH_TAVI_LAUGHED` (if the player's joke). Theryn, at the bench, writes a line in the test book and does not look up.
Idra, low, to the player (`EEH-D6.50`): "That lens. Last year's lenses spread the flame so you could see it. These gather it. Take one to Selice Morra in the quarter. She made the old ones." She gives the player one of the lenses from the frame (carry-state). The step completes.
**Verbs:** hand out, watch, shut, count, lead, comfort.

### Beat 4: The Lenses (`S04_lenses`)
**Objective:** *Ask Selice Morra about the test lens.*
In her workshop (C3), **Selice Morra** takes the lens without a word and holds it up to her furnace light (`EEH-D7`). She turns it. She lays it beside one of her own old school lenses from the rack, and has the player look through each at the furnace (two inspects; the old lens throws a broad soft disc of light on the wall; the test lens throws a hard bright point). "This is a lens for pushing, not seeing." She reads the rim: the mark is a regrinding mark, the number a **Council schedule** ("Any glasswright grinds to schedule. You get a slip with a number on it. You don't get a reason."). It was one of hers once; someone ground it to a new curve. She speaks to the glass, not to motives: asked who would want that, she says "Someone who wanted to see how high a flame would go. Not how a child holds it." and nothing more. Sets `EEH_LENS_READ`.
**Verbs:** show, compare, look.

### Beat 5: The Annex (`S05_annex`)
**Objective:** *Find Tavi's placement in the assessment ledger.*
Back at the court, Idra has thought about it (`EEH-D8`). Placements go into the **assessment ledger**, kept in the annex above the heat cellar "so it stays dry". She has the right to see her own students' placements; she has never looked. "Bring me Tavi's line. Bring the book. I'd rather read it with somebody." She gives the player her cellar key.
- **The heat cellar (M2):** Cinder Rats nesting by the duct (**EEH-E1**). The cellar is pinned **Working** (amber; light periodic damage; a niche by the ladder). Clear them (to 0 HP).
- **The annex (M3):** up the ladder through the hatch. The **assessment ledger** on the desk (document, dialogue file). **Required inspects:** (1) the placements page with **Tavi's line** in fresh ink, *Student 40 (Ostry, Tavi): lens test, this day. Vigil guidance, pending.*, and beside every placement a small **mark in a second column** (a ring, a ring with a dot, a filled ring) that is not explained anywhere in the book; (2) the **transfer sheet** at the back, spanning several years: *To vigil guidance*, *To Emberguard schools*, and, three times across the years, *For evaluation below*, each by student number only. Beside one of the three, an older line struck through, and in the margin, in Theryn's hand: *Not this one.*
- The player takes the ledger (**`EEH_ledger`**, quest item) down to Idra. She reads it at the court bench with the player, slowly (`EEH-D8.20`). She knows "vigil guidance" (the Covenant's lamp-house takes students for "steadying"; she thought it was a kindness). She knows the Emberguard schools. She does not know "below". She does not know the marks. She has taught here six years. Sets `EEH_LEDGER_READ`.
**Verbs:** fight, climb, read, carry.

### Beat 6: Theryn (`S06_theryn`)
**Objective:** *Speak to Theryn Dalewright.*
In her study (M4), **Theryn** is writing (`EEH-D9`). She sees the ledger under the player's arm and puts her pen down. She is not angry. The conversation is gentle and has options, each gated on what the player has: the lens (`EEH_LENS_READ`), Tavi's line, the transfer sheet, the marks.
- On the **test**, she defends it as stewardship: "A child who doesn't know how high her flame goes will find out one day in a kitchen or a dye yard. I'd rather she found out here, with water and a teacher." On the lens: "I asked for a truer reading. I was sent a truer reading." She did not ask what the curve did.
- On **vigil guidance** and the **Emberguard schools**: "Some students need steadying. Some need a purpose. I send them where they'll get it."
- On **"below"**, she goes quiet (`EEH-D9.30`). She knows it means Deepbrand (she says the word once, low). She has never asked what happens there. "I was told it was for their safety. I was told it by people I believe." (beat) "I've never asked. You can write that down too."
- On ***Not this one.***: she does not explain it. "That's mine." The quest does not push; there is no option to press twice.
- **Tavi's line:** she takes up her pen, draws a line through *Vigil guidance, pending*, and writes *Stays. Student.* beside it (`EEH-D9.40`). "She's a student. She stays a student." Sets `EEH_TAVI_STRUCK` (always).
- She asks one question (`EEH-D9.50`): "What will you do with it?" and does not ask for it back.
Theryn is never targetable, never threatened by the player and never exposed in public here (bible §5.1). Sets `EEH_THERYN_HEARD`.
**Verbs:** show, ask, listen.

### Beat 7: The Ledger (`S07_ledger`)
**Objective:** *Decide where the ledger goes.*
At the court gate, **Jessa** is waiting with **Tavi**, who is eating something and swinging her mitts (`EEH-D10`). **Idra** is with them. Jessa hears that Tavi's line is struck and holds her daughter's head against her side for a moment. Then Idra and the player talk about the ledger. The **choice** (§B9.3):
- **The guild** (`EH_CURRICULUM = guild`): give the ledger to Idra for the **teachers' guild**. Idra: "The guild sets the test. The guild can change the lenses. It'll be loud and slow and it'll happen." The ledger leaves the player's hands at the gate. The lenses will be changed. Theryn keeps her post.
- **Evidence** (`EH_CURRICULUM = evidence`): keep it for a later accounting. Idra hesitates and agrees: "Then it goes somewhere nobody here can lose it." The player carries it down to Cinderwall and gives it to **Yorven Khelt**, who locks it in his **strongbox** without opening it (`EEH-D10.60`): "I don't read school books. I keep them." The test stays this season. The ledger is not carried again: in EH-M6 Yorven lays it on the tally board as a prop (inspect only), and CV-M4 finds it in his keeping.
- **Ask Idra** returns her line ("I'd give it to the guild. I'm a teacher. You're not, and that's why I'm asking.") and the options again.
Jessa pays the warden's hand (small payment) and says Tavi will be in the courtyard at dusk if they want to lose at "hold it steady" (EME09). **Completes** on the hand-over (Idra at the gate, or Yorven at his strongbox).
**Verbs:** listen, choose, give.

## B7. Encounters

Tuned for **Advanced identity** (ED-10).

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EEH-E1** | 3 × Cinder Rat **scurrier**, 2 × **biter** | The academy's heat cellar (M2), nesting by the duct | Scurriers run the walls and come in from the sides; biters hold the ladder | **Scurrier dash:** fur flares bright on the wall (~1.0 s), then a dash along the wall and a leap at the player (sidestep). **Biter lunge:** crouches, back fur glowing (~0.8 s), then a short lunge-bite. **Nest flare:** when the duct vent exhales (ash lift ~1.5 s), every rat's fur flares and they press for ~3 s. | The quest's only fight; a reminder of vents and niches in a low room | 45–70 s; 70–85% HP |

**Hazards (not encounters):**
- **Tavi's flare** (`S03`): a hazard zone ~4 paces round a non-targetable child; periodic heat damage; shrinks by a third with each containment part; ends when she reaches the niche. A hazard, never an enemy (ED-2 pattern).
- **The cellar** is pinned Working: light periodic damage outside the niche by the ladder.
- **The court's floor vent:** Working outside the test; feeds the flare until its damper is shut.

**Rules**
- **Defeat at 0 HP** (CDR-1). Rats take the ordinary defeat presentation.
- **Melee or ranged** (CDR-2): the cellar fight accepts both. Ranged is never required.
- **Combat never reveals evidence.** The lens's meaning comes from Selice; the ledger is read in place; the cause comes from a book and a teacher.
- **Non-combatants:** every student, teacher, artisan and citizen is never targetable. Tavi in particular is never an enemy, never a target and never in a fight.
- **Death:** respawn at the practice court rail (M1) during `S01`, `S03`, `S05` (cellar), `S06`, `S07`; at the Cooling House otherwise. Defeated rats stay defeated. Containment parts are kept. The test re-pins morning on return.
- **Co-op:** the cellar fight shared; a defeat credits each partner whose own active step consumes it (CDR-6). Each partner's class jobs, mitts, containment, lens, ledger and choice are their own. In the test, each partner's Tavi is their own per-player presentation (a partner sees their own test); any shared court presentation is presentation only (bible §9) and never decides a partner's step.

## B8. The discovery moments: presentation specs

### B8.1 The lanterns (Beat 3)

**What it is:** heat following the room (bible §1.1), shown in a child: every lantern in the court dims when Tavi cries and brightens when she laughs. It is canon that fear dims a flame and confidence brightens it (dossier §III); what is strange is that it is every lantern at once, held by nobody. It is **never explained** and never evidence.

| Time | Element | Spec |
|---|---|---|
| 0 s | **The niche** | Tavi sits on the niche bench with her mitts in her lap. Idra kneels in front of her. The court's twenty practice lanterns stand on the benches where the students left them, lit, yellow. |
| ~1.0 s | **The crying** | Tavi's face goes. She cries the way children cry when the fright is over: loudly, all at once. |
| ~1.5 s | **The dim** | Every lantern in the court dims together, over ~1 s, to a low orange coal. The vent-hood tell does not change. The court goes dusky. |
| ~3 s | **The option** | The player gets one dialogue option (a joke) or can say nothing (`EEH-D6.40`). |
| ~5 s | **The laugh** | Tavi laughs (at the player's joke, or at Idra's face). A hiccuping laugh. |
| ~5.5 s | **The brighten** | Every lantern brightens together over ~1 s, past yellow to a clear white for a breath, then settles back to yellow. |
| After | **Nothing** | Nobody remarks on it. Idra wipes Tavi's face with her sleeve. Theryn, at the bench, writes a line and does not look up. |
| Never | **Explanation** | Asked later, Idra: "Lanterns do that near children. More than they should." Maeryn (if told): "Then she's a strong one. Keep her laughing." Theryn is never asked; there is no option. |
| UI | | The camera stays with the player. No cutscene; no UI on the lanterns. |

### B8.2 Maeryn's window (Beat 2)

| Element | Spec |
|---|---|
| **Trigger** | ~10 s into `EEH-D5`, while Maeryn is threading. |
| **The visitor** | A figure in a long grey Covenant cloak passes the front window slowly, turns its head to look in, and walks on. Not targetable, not interactable; a presentation NPC. |
| **Maeryn** | Her hands stop on the thread. She does not look up. When the figure has gone (~4 s) she breathes out and goes on. |
| **Never** | The visitor is not named, followed or met in EH-M2. It is the "Covenant-grey visitor" of the bible (§5.1), seeded for EST. |

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to the dye-worker at the Cooling House. | `EEH-D1` accept + `EEH-D2` end at the court gate | Yes | Requires EH-M1 Completed `[ED-20]`. Variant `EEH-D1.03` by `EH_COLD_WARD` |
| `S01_class` | Help Idra Callow with the lesson. | Lanterns handed out + shield channel + three bell strikes + `stair.row_lit` event | Yes | Sets `EEH_CLASS_DONE`. Repeats each in-game day if left |
| `S02_mitts` | Get the class a set of heat mitts for the test. | Lined mitts held (carry-state) + `EEH_MENDING_BOOK` | Yes | Option A (Leatherworking, then Maeryn lines) or Option B (keep watch at Maeryn's). Sets `EEH_MITTS` = self / maeryn. `cinderweave.grey_visitor` event |
| `S03_test` | Assist at the volatility test. | Mitts given + three containment parts + Tavi in the niche + `stair.lanterns_dim` event + `EEH-D6.50` end | Yes | Morning pinned (keep watch if needed). Sets `EEH_LANTERNS_SEEN`; `EEH_TAVI_LAUGHED` optional. Carry-state lens given |
| `S04_lenses` | Ask Selice Morra about the test lens. | Both lens inspects at the furnace + `EEH-D7` end | Yes | Sets `EEH_LENS_READ` |
| `S05_annex` | Find Tavi's placement in the assessment ledger. | EEH-E1 defeated + placements and transfer inspects + `EEH-D8.20` end | Yes | Item **`EEH_ledger`** gained. Sets `EEH_LEDGER_READ` |
| `S06_theryn` | Speak to Theryn Dalewright. | `EEH-D9` end | Yes | Sets `EEH_THERYN_HEARD`, `EEH_TAVI_STRUCK` |
| `S07_ledger` | Decide where the ledger goes. | Choice in `EEH-D10` + hand-over (Idra at the gate, or Yorven's strongbox `EEH-D10.60`) | Yes | Sets **`EH_CURRICULUM`**. Item removed. Small payment. Quest → **Completed** |

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `EEH_CLASS_DONE` | `S01` | — | ETB (Idra: "You held the frame for Benno once.") |
| `EEH_MITTS` = self / maeryn | `S02` | `EEH-D5.05` | ESH (Brisa: "Your shells held. Vall's lining helped.") with `self` |
| `EEH_MENDING_BOOK` | `EEH-D5.22` | `S02` | EST (Maeryn's mending book recurs) |
| `EEH_LANTERNS_SEEN` | `S03` event | — | None (deliberately) |
| `EEH_TAVI_LAUGHED` | `EEH-D6.41` (optional) | `EEH-D10.05` | EME09 (Tavi asks for another joke) |
| `EEH_LENS_READ` | `EEH-D7.14` | `EEH-D9` options | ETB (Idra's old primer and the old lenses) |
| `EEH_LEDGER_READ` | `EEH-D8.20` | `EEH-D9` options | — |
| `EEH_TAVI_STRUCK` | `EEH-D9.40` | `EEH-D10.02` | EH-M6 (Idra or the ledger at the tally board) |
| `EEH_THERYN_HEARD` | `EEH-D9` end | `S06` | Later content on Theryn's choice of loyalties (request) |
| `EH_CURRICULUM` = guild / evidence | `S07` choice | `EEH-D10.30`–`.62` | EH-M3 (`EGH-D7.08`); ETB; EH-M6 (§9.3 item 3); CV-M4 |

### B9.3 Choice: where the ledger goes

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Guild** (`EH_CURRICULUM = guild`) | The ledger goes to the teachers' guild through Idra. The lenses will be changed back to a spreading curve; the transfer sheet becomes a guild matter. | The ledger is now in a guild's hands, public and argued over; the coded column and "below" will be argued about by teachers who do not know what they mean. Theryn keeps her post; some teachers will not speak to her (barks). | ETB: the guild's revised test uses Idra's older exercise. EH-M6: Idra brings two teachers to the tally board. EME09: more children play. |
| **Evidence** (`= evidence`) | The ledger is locked in Yorven's strongbox at Cinderwall for a later accounting. | The test stays this season: other children still meet the narrow lens. Idra is unhappy and says so once ("Somebody's Tavi is in that room tomorrow."). | EH-M6: the ledger is laid on the tally board. CV-M4: the ledger is a custodian for R18. |

**Neither is wrong.** Both keep Tavi a student (Theryn struck her line either way); both keep the book whole; both leave "below" unexplained.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| The Molten Stair practice court | Access | EME04 on the stair; the court's class repeats as ambient life |
| Cinderweave Quarter workshops | Access | Brisa's tannery (Leatherworking), Maeryn's shop, Selice's workshop |
| Small payment | Currency | Jessa at `S07`. Economy tuning [GD]. |
| Skill XP | Action only [GD] | Leatherworking if done personally; Melee or Ranged at defeat. No lump quest XP. |
| Side-quest unlocks | Story | EST, EOP, EFD; EOM (with ESK); EFC (with ECN) |
| EH-M3 | Story `[ED-7]` | Journal entry appears on completion. If neither TF-M3 nor MR-M2 is Completed, it appears **locked**, naming both alternatives (§C4 offer). |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player cannot or will not do Leatherworking | Maeryn's mended set (Option B) at the cost of one keep-watch turn. Never blocked. |
| Player misses the morning test | The test re-runs each morning until assisted. Keep watch at the court bench. |
| Player is beaten in Tavi's flare | Respawn at the court rail; containment parts kept; Idra holding Tavi's hands. The zone resumes at its shrunk size. |
| Player says nothing in the niche | Idra makes Tavi laugh; same brightening. |
| Player tries to press Theryn on *Not this one.* | No second option exists. Her one line ("That's mine.") is the whole answer. |
| Death | Respawn by step (§B7). Mitts, lens, ledger and sub-objectives persist. |
| Logout | Restore to the persisted step: the Cooling House (`S00`; `S07` after `evidence` is chosen and before the hand-over), the practice court (`S01`, `S03`, `S05`–`S07`), Maeryn's shop or Brisa's tannery (`S02`), Selice's workshop (`S04`). |
| Walking away | Quest stays Active. Resume hooks: Idra at the court ("Class is every morning. So's the test."), Maeryn at her shop ("Your mitts are still on my counter."), Yorven at the Cooling House once `evidence` is chosen and the ledger is still carried (`EEH-D10.59`: "Strongbox is open when you are."). The ledger stays in the player's inventory until the hand-over. |
| Fail state | None. |
| Co-op | Shared cellar fight. Per-player class jobs, mitts, test (each partner sees their own Tavi), lens, ledger and choice. Presentation follows each player's own state (CDR-6). |

## B12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Hazard volume around a non-targetable NPC** (Tavi's flare) | Gameplay | A periodic-damage hazard volume parented to an NPC and toggled by quest state, with three radius steps. Same family as the ED-2 containment pattern; standard hazard volume. Per player. |
| **Containment parts** | Systems | Three channelled interactions (damper 2 segments; breath 3 segments synced to an NPC bark cadence; take-hand) and a short escort-follow to a niche volume. Progress kept. |
| **Lantern group presentation** (`stair.row_lit`, `stair.lanterns_dim`) | Art / VFX | One material parameter on the court's practice-lantern group: lit together, dimmed together to a coal, brightened together past white and back. Per player. No logic beyond the event. |
| **Grey visitor** (`cinderweave.grey_visitor`) | NPC / presentation | A non-interactive NPC on a fixed path past Maeryn's window during `EEH-D5`. |
| **Leatherworking at a tannery** | Skills | Existing cutting and stitching interactions; the shells and mitts are carry-state quest objects until the item pass defines them (ED-11). |
| **Lens comparison at a furnace** | Art / world state | Two inspect states that project a soft disc or a hard point of light on the workshop wall. |
| **Ledger prop** | Art / world state | The annex desk ledger shows Tavi's line as pending before `S06` and struck after (per player). |
| **Keep-watch** | Systems | Maeryn's stool; the court bench. |
| Creatures | Schema / Gameplay | Cinder Rat scurrier, biter. |

**New runtime needs: none.** The flare is a standard hazard volume attached to an NPC; everything else is a standard interaction, presentation event or the Lowmark keep-watch.

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The lens** | Reground on a Council schedule to focus rather than spread (bible §2.3). | A truer reading. | The point of light; Selice's reading; the schedule mark. | A faulty batch. | Who set the schedule and why. | EH-M5/CV-M4 (R18). |
| **The coded column** | A compatibility grade kept for others (dossier §IV). | None (nobody reads it). | Rings, dotted rings, filled rings. | A clerk's shorthand. | What the marks grade. | CV-M4 (R18). |
| **"For evaluation below"** | Deepbrand (bible §2.3). | — | Three lines; Theryn's silence; her one word. | A school below the city. | What happens there; who the three were. | EH-M4 (in part); Register (bible §7.6, held open). |
| ***Not this one.*** | The child Theryn hid [CANON secret]. | — | A struck line and a margin note. | A clerical correction. | Everything. | Later content (Theryn's loyalties). |
| **The lanterns** | Heat follows the room (bible §1.1). | — | Every lantern dims and brightens. | Tavi is dangerous; Tavi is special. | Everything. | None (deliberately). |
| **The grey visitor** | A Covenant caller who has noticed Maeryn (canon: she suspects attention). | A customer. | A face at the window; Maeryn's hands. | A suitor; a debt collector. | Who and why. | EST. |

## B14. Open decisions

1. **ED-20 (prerequisite):** built on the graph (EH-M2 requires EH-M1). If the Director rules for the prose (no prerequisite), `S00_offer` moves to first entry to the Cinderweave Quarter, Jessa approaches "the outsider" instead of "the warden's hand" (`EEH-D1.01`, `.02` are tagged), and the `EH_COLD_WARD` variant line is dropped. Nothing else changes.
2. **Tavi's pending line and Theryn's strike [NEW]:** gives the confrontation a concrete act of conscience and keeps a child out of "vigil guidance" in both outcomes. If the Director prefers Theryn to do nothing in front of the player, Tavi's line is absent from the ledger and `EEH_TAVI_STRUCK` is cut.
3. **The coded marks (rings) [NEW]:** deliberately undeciphered. CV-M4 may give them meaning; Emberholt never does.
4. **"Vigil guidance" [NEW term]:** the Covenant lamp-house's "steadying" for students, the Hearthveil route (Factions §4). EH-M5 visits the lamp-house; nothing here describes it beyond the word.
5. **Brisa's shells lined by Maeryn [NEW]:** reconciles the bible's "either route gives the Maeryn conversation; the skill route reaches it after" with a reason to go.
6. **Level framing (ED-10):** Advanced identity. Leatherworking `[GD: low]` with Maeryn's mended set as the time-cost alternative.

## B15. Internal review log

| Finding | Revision |
|---|---|
| The class risked a lecture on conditioning. | The class is shown as good: a boy's flame settles, a row lights on one breath, Theryn smiles at it. Nothing in `S01` hints at harm. |
| Teachers risked condemnation. | Idra doubts and acts; Theryn defends, goes quiet at "below", and strikes Tavi's line. The other teachers appear only as a guild that will argue. Nobody is exposed or punished. |
| Theryn's ledger limits (academy dossiers only; does not know what Deepbrand does). | She knows "below" means Deepbrand and says she has never asked. She never explains *Not this one.* She never calls the player or a student "special" or "gifted" (bible §5.3 rule 7). |
| Maeryn's heritage (ED-12). | Never said, shown or asked. The window beat shows fear, not why. |
| Selice's limit (the glass, not motives). | She reads the curve and the schedule mark and stops. |
| Tavi's flare risked combat. | A hazard round a non-targetable child, ended by a damper, a count and a hand. Nothing in the court is targetable. |
| The lanterns risked becoming evidence. | No option about them; nobody remarks on them; never used again as proof. |
| Skill hook. | Leatherworking `[GD: low]` with Maeryn's mended set (keep watch) as the time-cost alternative. |
| Combat share. | One small cellar fight (bible contract: Cinder Rats only). |
| R18. | Seeded as practice (a lens, a column, a list), never as a plan. |

---
---

# Part C: EH-M3 The Hollow That Should Not Burn (`EGH`) `[ED-7]` (ED-3, ruled 2026-11-15)

## C1. The quest in one paragraph

**Hesper Tolk** has been at the Cooling House every evening since the Grand Marshal's office took her petition: her brother **Lorcan**, foreman of a contract crew, is under the rock somewhere below Cinderwall's working edge, and Deepbrand, who hired the crew, say they "retrieved what was left" and sealed the gallery. **Darven Mott**, the one man who came out, sleeps at the Red Door clinic, and the official account calls him unstable. He is frightened and precise. He will show the way if someone stands beside him. At Embergate, **Grand Marshal Kaevren Thalos** signs a recovery warrant ("I sign for bodies. That one I can sign.") and warns that Deepbrand may not like reading it. They do not: the crew at the sealed mouth of **Darven's Gallery** fight to the last. Inside, the crew's tags still hang on the board, and Darven teaches the player to read **flarecap**: orange cap, live vein close, do not strike, cut or brace. A glassed fall blocks the cut; the player cuts through it or follows Darven's drain round it through two heat rooms. At the crew's last camp the five lie under their coats, Lorcan among them, with a day-book that names a bleed valve "on the pocket, far side of the glass", and a work order with Deepbrand's mark: *Do not log with the Marshal's office.* Darven will not go onto the glass. The player crosses the **Glassed Hollow** alone while the **Embermind Echo** shows a night of fire that changes nothing underfoot, and learns to trust the old patrol tells over the vision. Under the arch of an old door there is a warm handprint, child-high, on glass that should be cold. At the centre is a **circle**: a frame broken from the inside with nothing burnt within it, iron rings set in the rim where the glass is thin, glass that flowed outward from the middle, and an empty niche with a ridge at its lip. As the player crosses the rim, the **Hollow Revenant** pulls itself up out of the glass and re-forms on every pulse of a heat pocket until the player bleeds the crew's own valve. **Yorven Khelt** comes up out of an old miners' bypass ("They've doubled the mouth behind you") and leads the player out under the city into the **Red-Lit annex**, where a shelf stands open with a note from **Marenya Silvertide**: *Shelf-marks are on the spine. The rest is yours to read.* The **chamber roll** has its heading seal cut away and every line glassed but one, a name, *placed at the centre*; its glassed edge has the same ridge as the niche. A second sheet in the same hand, written after the night, says what came out of the centre, that a child was unaccounted at the door, that the shift above was "not ours", that the circle closed the war, and that one elder was taken in the purge after. A later hand has written *Keep. Do not copy.* At Maeryn Vall's back room, **Seredh Embercarver** puts a memory-stone in the player's hands: one Volkhari account, which agrees on the child at the door. The crew is buried with dimmed flames. Then the warden's hand decides who hears it first: the Cooling House and the memorial (**told**), or Kaevren and Marenya, until the evidence is complete (**kept**).

**What the player should remember:** the tags still on the board; the handprint; one legible line on a glassed page. **What the player should want next:** who the elder was who was "held below", and whether anyone is still there.

## C2. Selection record

| Candidate | Verdict |
|---|---|
| **A. The Echo shows the player what happened.** | Rejected. Phenomena never identify, prove or name (bible §2.4, §11.3). The Echo is a hazard the player learns to read past. |
| **B. The Revenant is the initiate, or a Volkhari, and its defeat tells the story.** | Rejected. Combat never reveals evidence; the Revenant is a resonance construct, not a person (bible §2.4). |
| **C. One record proves it.** | Rejected. R09 needs site evidence plus a restricted record with provenance (Revelation Ledger R09; bible §8.1). |
| **D. Warrant and guide → the mouth → flarecap → the fall → the crew → the Hollow under the Echo → the circle site and the Revenant → the roll with provenance and one Volkhari account → who hears it** (selected; the bible brief). | **Selected.** The player earns the descent with a living witness, reads the site themselves, then sets a record with a custodian's provenance beside the place it came from, with a protected Volkhari account as a second channel. Combat frames the work and reveals nothing. |

## C3. Canon grounding

| Element | Source | Status |
|---|---|---|
| The Glassed Hollow: precursor ritual with Volkhari captives; emotional overload, ember surge; walls flash-melted to glass; a precursor initiate (not Volkhari) became the Fire Titan; Kaelith escaped; Thalan the sole current captive; covered up as a "forge collapse"; sealed, forbidden, patrolled by Emberguard; faint emberlight without a source; surges echo | Dossier §II, §VI.4 | [CANON]; [APPROVED — FT-02d] (war's end) |
| No precursor name; limited continuity; no survivor roster | D-C03 | [APPROVED — D-C03] |
| Volkhari individuals only; no count; no refuge | D-C06; bible ED-12 | [APPROVED — D-C06] |
| Darven Mott: last survivor of a crew lost near a forbidden project; "the walls were breathing"; declared unstable; guides the player to the collapse site | Character file §39; bible §5.1 | [CANON] |
| Kaevren Thalos: intercepted orders routed around him; a private disappearance ledger; suspects the danger lies below | Character file §2; Part 4 ledger | [CANON] |
| Marenya Silvertide: senior Red-Lit Scribe archivist; keeps a hidden uncensored archive; values accurate records; considering leaking select pieces | Character file §11; Factions §3; Part 4 ledger (custodian, not a pre-cleared truth source) | [CANON] |
| Seredh Embercarver: Volkhari memory-stone carver; stones hold maker-imprinted recollection, one account, needing corroboration | Character file §45; bible §5.1 | [CANON] |
| Yorven Khelt: rose from miner; knows older tunnels that bypass Ashfall security | Character file §24 | [CANON] |
| Deepbrand: excavation and containment arm; "doesn't rescue you; retrieves what's left" | Factions §2 | [CANON]; contractor framing [NEW] |
| Flarecap: glows bright orange near ember veins; miners use it to locate unstable pockets | Dossier §XIII | [CANON] |
| Ashfall Revenants (resonance constructs from trauma); the Embermind Echo (hallucinations of past fires; a hazard) | Dossier §XII; bible §2.4, §10 | [CANON] |
| The Unburnt Boy legend; children chalk him | Dossier §X, §XV.4 | [CANON] |
| The chamber roll, the second sheet, "Keep. Do not copy.", the inspection register, the lost crew as a Deepbrand contract crew, the circle site's details | Bible §2.2, §2.3, ED-3, §6.1 | ED-3 ruled 2026-11-15 (the name, Iven Calder); [NEW] detail |
| Lorcan Tolk; the crew tags and tag board; the patrol tells on the glass; the niche ridge; the crew's bleed valve; the Red-Lit annex's lower stacks; signing out under a warrant | This package | [NEW] |

## C4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Hollow That Should Not Burn** |
| Suggested content id | `emberholt.main.03_hollow_that_should_not_burn` |
| Arc position | Act I turn (Arcs §3.3, EH-M3: "establish the directed Glassed Hollow core through evidence") |
| Prerequisite | **EH-M2 Completed and (TF-M3 `thornfell.main.03_echo_of_shatterfall` or MR-M2 `mire.main.02_banners_that_refuse_to_fall`) Completed** `[ED-7]`. Two hard prerequisites, within Arcs §6.1. Tuned for Expert identity (ED-10). |
| Offer | After EH-M2's completion, Hesper Tolk at the Cinderwall Cooling House. **Locked state** (EH-M2 Completed, neither alternative Completed): the journal shows the entry as locked and names both alternatives: *Requires: The Ember in Every Hand; and either The Echo of Shatterfall (Thornfell) or The Banners That Refuse to Fall (the Mire).* Hesper is present and talkable and does not yet ask (`EGH-D1.01`–`.05`: she is waiting on the Marshal). No hidden gate. **Unlocked:** `EGH-D1.10`. |
| Solo / co-op | Solo-clearable. Co-op partners share the mouth fight, the glasswalkers and the Hollow Revenant; the warrant, route choice, tags, site reading, valve, roll, stone and choice are per player. |
| Target length | 55–70 minutes first time |
| Combat share | ~25% |
| Dialogue share | ~25% |
| Descent, traversal, reading the site, mining or the drain, archive, choice | ~50% |
| Skills touched | Melee or Ranged (either; neither required); Mining ~[GD: mid] (optional; Darven's drain route is the time-cost alternative); heat gear from *Soot and Hide* recommended, never required |
| Choices | Who hears the Hollow truth first (`EH_HOLLOW_TRUTH`); cut the fall or take the drain (`EGH_FALL`, flag only); compare with Shatterfall or the banners (optional variant line) |
| Unlocks | `EH_HOLLOW_TRUTH`; the Iven Calder journal line; Darven's Gallery to the crew camp as a revisitable site (under Kaevren's post); EAD, ENW; EMS (with ETB); EH-M4 |
| **Anchor** (contract) | Deepbrand's lost crew (Hesper, Darven, the Tolks); the Red-Lit archive (Marenya) |
| **World-truth row** (contract) | **H18** (the Glassed Hollow ended Emberholt's war; FT-02d), H09 |
| **Revelation role** (contract) | **Owns R09.** Seeds R16 (the inspection register's struck "visiting witness" column) and R19 (the roll's one legible line, Iven Calder, unexplained until CV-M4; the warm handprint). Never states Thalan lives (R10 is EH-M4's). |
| **Recurring evidence** (contract) | Three independent custodians: the **circle site** (S06; read in place: frame, rim rings, outward flow, niche ridge), the **chamber roll and second sheet** (`EGH_roll`; Marenya's shelf-marks and the signing-out in her shelf book), and **Seredh's memory-stone** (one Volkhari account; protected testimony). Darven guides; his "breathing walls" are never evidence. The roll's one line recurs in CV-M4 (the binding). |
| **State compliance** (contract) | Inactive / Active / Completed. The Mining hook has a slower route; the pocket valve's progress is kept; the Echo never harms. Choice recorded in `EH_HOLLOW_TRUTH`. Resume at the persisted step with a hook at the Cooling House (Hesper), the Red Door clinic (Darven), the crew camp (Darven) or the annex (Marenya). |
| **Combat compliance** (contract) | Deepbrand Crews (human) and Ashfall Revenant glasswalkers defeated at 0 HP. The Hollow Revenant (elite) and its glasswalkers re-form on each pulse of the heat pocket while it pulses (place condition, never health); bleeding the pocket at the crew's own valve ends the condition, and any enemy still standing fights on to 0 HP. Melee or ranged; ranged viable everywhere and never required. Solo-tuned boss. No SX. No defeated enemy gives testimony. |

## C5. The places

### C5.1 Cinderwall [EP02] and Embergate [EP01] (return)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W2. The Cooling House** | Offer (`S00`); burial and choice (`S08`). | As EH-M1, with the outcome of `EH_COLD_WARD` on the board. Hesper's bench by the door. |
| **W4. The Red Door clinic** [NEW sub-site in EP02] | Darven (`S01`). | A narrow clinic behind a red-painted door: cots, a quench trough, burn salves in jars. Darven on the end cot, awake, with his left hand (two fingers missing) in a bowl of water. |
| **W5. The old lower forge memorial** [EP11] | Chalk (`S08`, `told`). | The walled yard and its bronze plaque (EDS09). |
| **E1. The Marshal's office at the gate** [NEW sub-site in EP01] | Kaevren (`S01`); `kept` (`S08` aftermath). | A plain room over the Emberguard checkpoint, a map table, a locked ledger box on a shelf. |

### C5.2 Darven's Gallery [EP10, NEW]

A bypass gallery cut from the old works at Cinderwall's working edge toward the Hollow's outer glass. **MAP VERIFICATION REQUIRED** (depth, heat and the gallery's line to the Hollow matter here): relative order from the surface: the old works approach → the sealed mouth → the tool store (the drain's upper end) → the cut → the glassed fall (and the drain round it) → the crew camp at the outer glass.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **G1. The old works approach** | Respawn point for `S02`–`S03`. | Old pit props, a cold cooling niche, chalk crew marks decades old. |
| **G2. The sealed mouth** | Deepbrand post (**EGH-E1**); the tag board; the seal plate (`S02`). | A new iron **seal plate** bolted across the gallery mouth, Deepbrand's mark stamped in it. A chalk line on the floor ten paces out. A ledge with a crossbow rest. Beside the mouth, the crew's **tag board**: pegs, five brass tags still hanging, one empty peg. |
| **G3. The tool store** | Flarecap lesson begins; drain grate (`S02`, `S03`). | Picks, wedges, a water barrel, a broken lamp. In the floor, a **drain grate** lifted and set aside: the way Darven came out. |
| **G4. The cut** | Flarecap (`S02`). | A rough gallery with side pockets. Flarecap on the walls: pale cream where the rock is cool, bright orange where a vein runs close. The light in the dark is the cap's own glow. |
| **G5. The glassed fall** | Mining hook (`S03`). | A rockfall fused to dark glass where the heat pocket broke. Its right face is fractured rock with pale cap; its left face is glassy with orange cap at the seams. |
| **G6. The drain** | Time-cost route (`S03`). | A crawl-height culvert that becomes two low **heat rooms** (Working, vents, a niche in each) and comes up beyond the fall. An optional **agility** step across a culvert gap (walkable fallback round the sump). |
| **G7. The crew camp** | The crew; the day-book; the work order (`S04`). Respawn point for `S05`–`S06`. | A widening at the end of the cut where the outer glass begins: a cold fire ring, bedrolls, a tally board with chalked shifts, a tin box. Five crew under their coats where the pocket broke the wall. Beyond, the floor turns to glass. |

### C5.3 The Glassed Hollow [EP07, CANON]

A great cavern of warped black glass. Supports melted into frozen waves. Faint emberlight with no source. The air tastes of burnt stone. **MAP VERIFICATION REQUIRED:** relative order from the crew camp: the outer glass edge → the crossing → the old door arch → the circle → the bypass tunnel mouth on the far side.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **H1. The outer glass edge** | Darven stops (`S05`). | Where the gallery's rough rock ends and smooth glass begins. A line of old iron spikes driven into the glass with emberglass beads in their heads: **patrol tells**, Emberguard work from years of patrols (dossier: patrolled). |
| **H2. The crossing** | Echo; glasswalkers (**EGH-E2**) (`S05`). | A long glass floor with vents under it breathing heat through cracks; patrol tells on spikes every twenty paces; cooling niches cut into two glass pillars, troughs dry, a water cask left by a patrol. |
| **H3. The old door arch** | The handprint (`S05`). | The stone arch of a door, its jambs sheathed in glass that ran down and froze. On the left jamb, at the height of a child's shoulder, a clean **handprint** in the ash film. |
| **H4. The circle** | The site; the Hollow Revenant (**EGH-E3**); the pocket valve (`S06`). | A round floor sunk a step below the cavern. At its centre a **frame** of basalt posts and iron bars. Round the rim, iron **rings** set in the floor where the glass is thin. Glass in frozen waves running outward from the centre to the walls. In the rim wall, a **niche**. On the far side, a crew-fitted **bleed valve** with a red handle on a pipe the crew drove into a **heat pocket** vent. |
| **H5. The bypass tunnel mouth** | Yorven (`S06` end). | An old miners' tunnel, older than the glass, its mouth half-sheathed where the glass ran into it. |

### C5.4 The Red-Lit annex [NEW sub-site; not a numbered POI]

A restricted annex of the Red-Lit Scribes' archive, reached from below by Yorven's old bypass tunnel through its **lower stacks door**. **MAP VERIFICATION REQUIRED** (placement under the city is unset; open decision C14.2).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A1. The lower stacks door** | Arrival (`S07`). | An iron door into a long stone room of shelves. Red lamps (the Scribes' lamps) on chains. Dry, cool, quiet. |
| **A2. The lower-forge shelf** | The roll, the sheet, the wrapper; the inspection register (`S07`). | One shelf with its cage door standing open. A **note** tucked in the cage. A flat box in oilcloth. Beside it a bound **inspection register**. |
| **A3. The reading table** | Reading and comparison (`S07`). | A sloped table under a red lamp, a magnifier on an arm. |
| **A4. Marenya's desk** | Provenance; signing out (`S07`). | At the far end of the stacks: a desk, a **shelf book** open, spectacles on a chain set down on the page. |

### C5.5 Maeryn's back room [EP03] (`S07`)

The curtained room behind Maeryn's shop: a cutting table, a stove, two chairs. **Seredh Embercarver** at the table with a basalt memory-stone wrapped in wool. [ED-12] This room is shown only as a room. Nothing in it locates anyone.

## C6. Player-facing sequence

### Beat 0: Hesper (`S00_offer`) `[ED-7]`
**Objective:** *Speak to Hesper Tolk at the Cooling House.*
**Locked** (EH-M2 Completed; neither TF-M3 nor MR-M2 Completed): Hesper is on her bench by the door and talks about her brother (`EGH-D1.01`–`.05`): a contract crew, a cut below the working edge, Deepbrand's "retrieved what was left", her petition to the Marshal. "I'm waiting on him. I'm good at waiting. I'm getting worse at it." The journal entry is visible and locked, naming both alternatives. No offer is made.
**Unlocked** (`EGH-D1.10`): Hesper stands up when the warden's hand comes in. The Marshal has answered: he will sign a recovery warrant for the gallery, and he wants it carried by somebody who is "neither Deepbrand nor his". Darven Mott will show the way "if somebody stands beside him". "I want my brother. I want him somewhere I can stand. I don't want an argument." She adds that Yorven says he knows ways under his ward that nobody else does, "if it goes bad down there".
- **Accept:** the quest becomes **Active**.
- **Not now:** "I've waited. I'll wait." Re-offered from her bench (`EGH-D1.90`).
**Verbs:** listen, accept.

### Beat 1: Darven and the Warrant (`S01_darven`)
**Objective:** *Find Darven Mott and collect the warrant.* (Sub-objectives in any order.)

| Sub-objective | Where | What the player does | Sets |
|---|---|---|---|
| **Darven** | The Red Door clinic (W4) | **Darven Mott** (`EGH-D2`) is frightened and precise. He tells what he saw, not what it means: a contract crew of six, Lorcan Tolk foreman; Deepbrand paid for a cut "toward the glass" and to stop at the outer glass ("They wanted the veins round it. They didn't say why. You don't ask Deepbrand why."); the walls "breathing" for a week before (he insists; nobody else on the cut did); the pocket breaking the wall; the fall; the drain he crawled out by, round the fall to the tool store; Deepbrand at the mouth the next day, the plate going up, the word "unstable" in a clerk's mouth. He says Lorcan set **a bleed valve on the pocket** the week before, "far side, where it vents onto the glass". He will come if someone stands beside him. "I won't go on the glass. I didn't then. I'll take you to the crew." | `EGH_DARVEN_HEARD` |
| **The warrant** | The Marshal's office at the gate (E1) | **Kaevren Thalos** (`EGH-D3`), stern and dry, signs a recovery warrant at his map table: "I sign for bodies. That one I can sign." Asked about Deepbrand: "They'll read it. They may not like reading." He asks one thing: bring him anything at the camp that carries Deepbrand's mark. "I'd like to see what they sign." **Carry-state: the warrant** (and the warrant cloth for the dead). | `EGH_WARRANT` |

**Optional variant lines** `[ED-7]` (one option each, with Darven, after his account; `EGH-D2.40`–`.45`). Neither changes a step.
- **With TF-M3 Completed:** "At Shatterfall the cairns said a storm took them. The roster in the seat said otherwise." Darven: "I don't know cairns. I know my crew's tags are still on the peg. That's what the board says, and the board's not a liar, it's just a board."
- **With MR-M2 Completed:** "In the Mire, things rose that looked like they had something to say. They didn't." Darven: "The walls breathed. I'm not saying they meant anything by it. I'm saying they did it, and I'm saying I was there." (He shows no knowledge of either region; he answers only about his crew.)
Sets `EGH_COMPARED` = shatterfall / banners if used (flavour).
**Verbs:** listen, ask, carry.

### Beat 2: The Mouth and the Cap (`S02_mouth`)
**Objective:** *Get into the gallery.*
Darven walks with the player as far as the old works approach (G1) and stops at the corner. Ahead is the **sealed mouth** (G2): a Deepbrand crew post. The crossbow on the ledge calls out when the player reaches the chalk line (`EGH-B2.1`: "Sealed works. Turn round."). Shown the warrant (option): "Not ours. Turn round." (`EGH-B2.2`). When the player crosses the chalk line, the post attacks (**EGH-E1**). They fight to 0 HP.
After the fight, Darven comes up to the **tag board** beside the mouth. Five brass tags still hang; one peg is empty. He touches each tag once (`EGH-D4.01`: "You hang your tag going in. You take it coming out. Mine's in my pocket."). Inspect the tag board (required; `EGH-I2`). Then Darven lifts the five tags off their pegs into his coat (`EGH-D4.03`: "You take it coming out. They're coming out."). The player **unbolts the seal plate** under the warrant (a 2-segment channel, ~4 s each). Inside: the tool store (G3), the lifted drain grate.
**Flarecap (G4).** In the cut, Darven teaches flarecap (`EGH-D4.10`): "Cap glows near a vein. Pale cap, cool rock. Orange cap, live vein close: don't strike it, don't cut it, don't brace on it. Down here it's your lamp, too. Follow the pale. Keep the orange where you can see it." The player **inspects a cap** (required; `EGH-I3`). The cut is pinned: orange-cap stretches are **Surging** heat zones (heavy periodic damage), pale stretches **Cool**. The way to the fall follows the pale. Sets `EGH_FLARECAP`. (Variant if *The Flarecap Seam* is Completed: "You've read cap before. Breck's ridge? Good. This is the same cap with worse manners.")
The step completes on reaching the fall (G5).
**Verbs:** confront, fight, read, unbolt, follow the cap.

### Beat 3: The Fall (`S03_fall`)
**Objective:** *Get past the glassed fall.*
The fall is rock fused to glass where the pocket broke. Darven (`EGH-D5`): "That's where it came down. I was on the other side of it. Then I wasn't." Two ways, both complete the step:
- **Option A (skill): cut through** (**Mining ~[GD: mid]**, with a pick from the tool store or the player's own). Read the faces first (inspect, `EGH-I4`): the **right face** is fractured rock with pale cap; the **left face** is glassy with orange cap at the seams. Cut on the right: a 3-segment channel (~4 s each). Striking the left face: refused with a burst of heat from the seam (moderate damage, a step of knock-back; Darven: "Orange! Leave her!"). Nothing resets. `EGH_FALL` = cut.
- **Option B (time-cost): Darven's drain** (G6). Back to the tool store and down the drain grate: a crawl, then **two heat rooms** pinned Working, each with floor vents (ash lift ~1.5 s, exhale) and a cooling niche, then up beyond the fall. About four to five minutes longer. Darven goes first through the crawl ("I've done this once. I can do it twice.") and waits at each niche. Heat gear from *Soot and Hide* halves the rooms' periodic damage (recommended, never required). `EGH_FALL` = drain.
**Verbs:** read, cut, or crawl and time vents.

### Beat 4: The Crew Camp (`S04_crew_camp`)
**Objective:** *Find the crew.*
The camp (G7). Five crew lie where the pocket broke the wall, under their own coats; somebody (Darven, on his way out) pulled the coats over their faces. The presentation is plain and quiet: shapes under coats, boots, a lamp on its side. Darven sits down by the cold fire ring and does not speak for a moment (`EGH-D6.01`). Then he names them, one by one, by their first names, and stops at the foreman: "That's Lorcan. That's Hesper's."
Required, any order:
- **Lay the warrant cloth** over the five (one interaction): Kaevren's recovery detail will bring them up under the warrant once the route is clear. Darven: "That's the first thing anybody's signed for them that wasn't a contract."
- **Take the crew's tags** from Darven (one interaction, `EGH-D6.11`; the five he lifted off the mouth board in `S02`; carry-state; for Hesper and the families).
- **Read the foreman's day-book** in the tin (read in place; document in the dialogue file): the cut "toward the glass" by order; shifts; "walls breathing again, Mott says; I don't hear it"; **"Set a bleed on the pocket, far side, where it vents onto the glass. Red handle. If she goes, open it slow."** Sets `EGH_DAYBOOK_READ`.
- **The work order** in the same tin (document): Deepbrand's mark; *Bypass gallery toward the outer glass. Stop at the glass. Retrieve nothing. Do not log with the Marshal's office.* **Carry-state** (for Kaevren). Sets `EGH_WORK_ORDER`.
Darven will go no further (`EGH-D6.20`): "That's the glass. I won't go on the glass. I didn't then." He stays at the camp with the crew. The step completes.
**Verbs:** find, cover, take, read.

### Beat 5: The Hollow (`S05_hollow`): *the crossing*
**Objective:** *Cross the Hollow.*
At the outer glass edge (H1) there is a line of iron spikes with emberglass beads in their heads: **patrol tells**. On the glass, the player is alone.
**The Embermind Echo.** Every ~25 s the Echo comes (§C8.1): a ~1.5 s warning (the emberlight in the walls pulses, a low roar rises), then for ~8 s the cavern **overlays** with a night of fire: walls of flame across the floor, heat-shapes running, a roar, falling glass that never lands. **It changes nothing.** No collision, no damage, no blocked way; the vents and the tells under it are exactly as they were. Inspect any patrol tell during the Echo: it shows its true state through the overlay. The first time, a short journal line appears: *Read the tells, not the vision.* (and Darven's voice from the edge, if within earshot, `EGH-B5.2`: "It's not there! Read the beads!").
**The real hazards** are the glass vents: cracks that breathe heat on a cycle, marked by the patrol tells (amber for a breathing crack, red and crazed for a surging one: do not cross). A safe line runs from tell to tell. Two cooling niches cut into glass pillars; a patrol water cask.
**The glasswalkers** (**EGH-E2**): two Ashfall Revenant **glasswalkers** walk the crossing. They are real. The readable rule (`EGH-I6`, and the journal line on first sight): **the Echo makes no sound on the glass and leaves no mark; a glasswalker cracks the glass where it steps** (white star cracks and a crunch with every step). They fight to 0 HP and collapse into ash; they do not re-form on the crossing (no condition here).
**The strange moment (§C8.2).** At the **old door arch** (H3), the path passes under the arch. On the left jamb, at a child's shoulder height, a clean handprint stands out of the ash film, and the glass inside the print shimmers faintly with heat. The moment plays as the player passes (always; sets `EGH_HANDPRINT_SEEN`). **Optional inspect:** "Warm. Warmer than your hand. The glass round it is cold." (`EGH-I7`). Nothing explains it.
The step completes on entering the circle's rim volume (H4).
**Verbs:** read tells, ignore the vision, fight, pass under.

### Beat 6: The Circle (`S06_circle`): *R09 site evidence and the miniboss*
**Objective:** *Read the circle.*
As the player steps down into the circle, the **heat pocket** on its far side **pulses** (a ring of light running out along the cracks from the pocket vent, ~3 s), and the **Hollow Revenant** pulls itself up out of the glass at the frame (**EGH-E3**; §C7): a shape of ash and heat that is never the same height twice, with two **glasswalkers**. It re-forms on each pulse while the pocket pulses.
**The valve.** The crew's **bleed valve** (red handle) stands on the pocket's pipe on the far side of the circle. Bleeding it is a 3-segment channel (~4 s each), interrupted by hits, progress kept. Each completed segment shrinks the pulse's reach by a third (visible: the light ring runs shorter). The **third** segment ends the condition: the pocket sighs, the cracks go dark, and nothing re-forms. Any enemy still standing fights on to 0 HP. Sets `EGH_POCKET_BLED`.
**The site (required inspects; R09 site evidence; any order; available during or after the fight).** Each inspect gives what is there and nothing more (texts in the dialogue file, `EGH-I8`–`I11`):
1. **The frame** (`EGH-I8`): basalt posts and iron bars round a space the size of a standing person. The bars are bent **outward**, every one, broken from the inside. The floor inside the frame is plain grey stone, **not glazed, not scorched**. Nothing burnt inside it.
2. **The rim** (`EGH-I9`): iron **rings** set in the floor at intervals round the circle's edge, with short chains. Where the glass is thin you can see them; where it is thick you cannot. You do not count them.
3. **The flow** (`EGH-I10`): the glass did not fall in. It ran **out**, from the centre toward the walls, in waves that froze mid-run, and it climbed the walls. "A roof that falls comes down. This went out from the middle."
4. **The niche** (`EGH-I11`): a shelf cut in the rim wall. A rectangle on it the size of a folded sheet is **unglazed** where something lay and was lifted after the glass cooled; at the rectangle's front edge, a **ridge** where the glass ran up against whatever lay there and set.
When all four are read, sets `EGH_SITE_READ`. There is no forge here: no anvil, no hearth, no slag, no tools (an observation in the flow text, not a separate inspect).
**Yorven** (`EGH-D7`, after the fight and the four inspects). Footsteps from the far side: **Yorven Khelt** comes out of the bypass tunnel mouth (H5) with a miner's lamp. "Deepbrand's doubled the mouth behind you. You're not going back that way." He looks at the circle a long time. "That's not a forge. I've worked forges." He has known this tunnel since he was a miner and never followed it to the end; it comes up under the Red-Lit Scribes' stacks ("Everything that burned in the lower forge went up to the Red-Lit after. Everybody knows that. Nobody says it."). He will take the player out that way. Variant (`EH_CURRICULUM` = evidence): "Your school book's in my strongbox. This'll want a box of its own." Darven, he says, will be brought up with the crew by Kaevren's detail; Yorven sent word.
**Verbs:** fight, bleed, inspect, follow.

### Beat 7: The Roll (`S07_roll`) (ED-3, ruled 2026-11-15) `[ED-12]`
**Objective:** *Read the record of the night.* (Sub-objectives; the roll and provenance in the annex first, then the stone.)
The bypass tunnel comes up through an iron door into the **lower stacks** of the Red-Lit annex (A1). Yorven waits at the door: "I've never come up this far. I never wanted to know what was on the shelves."
| Sub-objective | Where | What the player does | Sets |
|---|---|---|---|
| **The shelf** | A2 | One shelf's cage door stands open. Tucked in it, a **note** in a neat hand: *Shelf-marks are on the spine. The rest is yours to read.* (`EGH-I12`). A copy of Kaevren's warrant is pinned under it, stamped received. In a flat oilcloth box: the roll, the second sheet, and their **wrapper**. | — |
| **The roll** | A3 | Read the **chamber roll** at the reading table (document; required). Its heading seal has been **cut away** with a knife, long ago. Under a line of script (*Admitted, the night of the circle*) every line is glassed into a milky ridge, unreadable, **except one**: *Iven Calder, placed at the centre.* The lower half of the sheet is glassed, with a hard **ridge** along one edge. | `EGH_ROLL_READ` |
| **The match** | A3 | **Compare** the roll's ridge with what the player read at the niche (dialogue-gated inspect, requires `EGH_SITE_READ`): the ridge runs where a sheet would lie against the niche's lip, the unglazed rectangle is the size of the folded roll. The roll was in the niche when the glass ran. | `EGH_NICHE_MATCH` |
| **The second sheet** | A3 | Read the **second sheet** (document; required), same hand, written after the night: what came out of the centre "went down and was not stopped"; "Volkhari held for the circle. One child unaccounted: the door"; "shift above (lower forge): not ours; not entered"; "the circle to have closed the war before the thaw: it has closed it"; "one elder taken in the purge after; held below". | `EGH_SHEET_READ` |
| **The wrapper** | A3 | Inspect the **wrapper** (required): in a different hand and later ink, *Keep. Do not copy.* Nobody signed it. | `EGH_KEEP_SEEN` |
| **Provenance** | A4 | **Marenya Silvertide** (`EGH-D8`) at her desk at the end of the stacks. She vouches for **shelf-marks, never for content**: the shelf book shows the box received "from the lower forge works" the year after the war and kept on this shelf since, under her mark and her predecessor's. "The marks are mine. What the pages say is yours." Under the warrant, once the roll, the match, the sheet and the wrapper have been read at the table (otherwise `EGH-D8.36`: "Read it at the table first. Nothing leaves this room unread."), she lets the warrant-holder **sign the box out**, writes the signing-out in the shelf book, and hands it over (**`EGH_roll`**, quest item): "Warrant goods leave under the holder's hand. They come back under it." She does not say why the cage was open. Asked: "A warrant came. I read warrants." | `EGH_PROVENANCE`; item |
| *The inspection register* (optional; R16 seed) | A2 | A bound **inspection register** on the same shelf (`EGH-I14`): *Inspection of works, lower forge and below.* A column headed **visiting witness** has a small mark in each row on the older pages, a different mark each time. For the last years before the war it is empty, and on the last page that has it, the heading is struck through with one line. Marenya, if asked: "That column was struck before my time. I keep what's struck too." | `EGH_INSPECTION_GAP_SEEN` |
| **The stone** | Maeryn's back room (C5.5) | Leaving the annex by its street door (Yorven: "Maeryn Vall sent word to the Cooling House. Somebody wants to put a stone in your hand. I didn't ask who."), the player goes to **Maeryn's shop**; she takes them through the curtain without a word. **Seredh Embercarver** (`EGH-D9`) unwraps a basalt **memory-stone** and lets the player hold it (interaction): it carries one carved account in its maker's voice (document text in the dialogue file). The maker is never named and the stone is never said to be Seredh's own memory, so no Volkhari anchor gains a wartime role or age (Part 4 ledger). It agrees with the second sheet on **a child at the door**, and says the one at the centre "was theirs, not ours". Then his terms `[ED-12]`: "You may say a Volkhari stone agrees on the child at the door. Not whose stone. Not whose hands. Not where you heard it." | `EGH_STONE_HEARD` |

On `EGH_ROLL_READ` the journal records the legible line as a **Journal entry** (`EGH_INITIATE_JOURNAL`): *On the chamber roll, one line not glassed: Iven Calder, placed at the centre.* The name is Iven Calder (ED-3, ruled 2026-11-15) and is **spoken nowhere** in Emberholt; no NPC reads it aloud, connects it to anything, or explains it, and the player has no option to say it. Its significance waits for CV-M4 (R19).
The step completes when the roll, the match, the sheet, the wrapper, provenance and the stone are all set.
**Verbs:** read, compare, sign out, hold, listen.

### Beat 8: The Truth (`S08_truth`)
**Objective:** *Decide who hears it first.*
Kaevren's recovery detail brings the crew up under the warrant while the player is in the annex (between steps; offscreen). At the **Cooling House** the five lie under grey cloth on the long tables, and the room keeps the **dimmed flame** (EME03): every lamp turned down one notch and left there for the night. **Hesper** sits by Lorcan. The player gives her the **tags** (interaction); she holds them in her fist. Darven stands at the wall with his hands in his pockets. **Kaevren** is there, in his red cloak, because he signs for bodies and comes to see them (`EGH-D10`). **Yorven** is at the end table.
- **Optional:** give Kaevren the **work order** (`EGH-D10.20`): he reads it twice. "This should have crossed my desk. It didn't." He folds it into his coat. Sets `EGH_ORDER_SHOWN`.
Then Hesper asks what happened down there. The **choice** (§C9.3):
- **Tell it** (`EH_HOLLOW_TRUTH = told`): the warden's hand tells the room (`EGH-D10.40`): not a forge, a circle; people held at its rim; someone placed at its centre; a night meant to end the war that did; a child at the door; the lower forge hands above it "not entered". The player says, if Seredh's terms allow it, that a Volkhari stone agrees on the child (never whose). The room argues (barks). Then Hesper walks out to the old lower forge's wall with half the room behind her, and **chalks** across the plaque: *NOT A COLLAPSE.* (`EGH-D10.50`; prop state per player). Kaevren takes the roll back under his seal to the annex shelf "so nobody can say it walked off".
- **Keep it** (`EH_HOLLOW_TRUTH = kept`): the warden's hand tells Hesper only that the crew died in a pocket on a Deepbrand cut, and takes the rest to **Kaevren** and, through his warrant, **Marenya** (`EGH-D10.60`): "Bring it complete. Then nobody can say a forge fell." The roll goes back to the annex under Kaevren's seal. At his office, Kaevren takes down a **second ledger**, new, and writes the first line in it while the player watches. The city is quiet.
- **Ask Hesper** returns her line ("I wanted a body. I've got him. The rest is yours. Don't make me carry it.") and the options again.
Either way the crew are buried with dimmed flames. The quest **completes** on the chalk (`told`) or Kaevren's first line (`kept`).
**Verbs:** give, choose, tell or carry.

**Epilogue (no step).** Post-quest, the gallery mouth is under an Emberguard post on Kaevren's warrant; the gallery is walkable to the crew camp and the outer glass. The circle is quiet (the pocket is bled). With `told`, the plaque keeps the chalk (per player); Cinderwall barks argue about it for a while and then about other things. With `kept`, the plaque is clean and Kaevren's office has two ledger boxes on the shelf.

## C7. Encounters

Tuned for **Expert identity** (ED-10). Exact levels are Gameplay Designer calls. Glasswalkers and the Hollow Revenant are resonance constructs (bible §2.4): defeated at 0 HP, they collapse into ash; in the circle they re-form on the pocket's pulse while it pulses.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EGH-E1** | 2 × Deepbrand Crew **guard**, 1 × **crossbow** | The sealed mouth (G2); the crossbow on the ledge | Guards hold the chalk line with shields and hooked poles; the crossbow covers the approach from the ledge (reachable by a short ramp, so melee can answer it) | **Guard, Hook:** draws the pole back to the hip (~1.5 s), then a hooking sweep that pulls the player one step toward him. **Guard, Shield bash:** sets his feet, shield up (~1.5 s), then a bash with a short stagger. **Crossbow, Aimed shot:** a red glint on the bolt-tip and a steadied stance (~1.5 s), then a heavy bolt (break line of sight or sidestep). **Crossbow, Reload:** ~3 s visible reload between shots (the window to close). | First human enemies in Emberholt; a ranged enemy that ranged players can duel and melee players can climb to | 70–100 s; 55–75% HP |
| **EGH-E2** | 2 × Ashfall Revenant **glasswalker** | The crossing (H2), walking the glass | Patrol the safe line between tells; engage on sight | **Crack step (tell that they are real):** each step stars the glass white with a crunch. **Shard throw:** pulls a shard of glass up out of the floor (~1.2 s), then throws it in a line. **Slide:** crouches, glass hissing under it (~1.0 s), then slides a short way and swipes. | Teaches the real-vs-Echo rule under pressure; ranged and melee both fine | 50–80 s for both; 60–80% HP |
| **EGH-E3** | **The Hollow Revenant** (elite, Ashfall Revenant family), 2 × glasswalker; re-form on each pocket pulse until the valve is bled | The circle (H4) | The Revenant holds the centre and advances on whoever is at the valve; glasswalkers screen the rim | **Pocket pulse (the condition):** a ring of light runs out along the cracks from the pocket vent (~3 s), then a heat wave across the circle's floor to its current reach (stand in the frame's lee or beyond the reach); on the pulse, defeated members re-form at the frame, the Revenant included. Pulse every ~30 s; reach shrinks a third per valve segment. **Revenant, Rake:** draws an arm back, ash streaming (~1.2 s), then a wide raking arc in front. **Revenant, Shatter:** raises both arms, the glass under it glowing (~2.0 s), then slams: shards burst out in a straight line (step out of the line). **Revenant, Shriek:** body contracts and brightens (~1.5 s), then a pressure shriek with a two-step knock-back ring. **Revenant, Call** (below half health, once per life): sinks its arms into the glass (~2.5 s); if not interrupted, two glasswalkers rise at the rim at once, never more than five hostiles standing (Enemies C-12). **Glasswalkers:** as EGH-E2. | Miniboss phenomenon bound to a condition: win by bleeding the pocket under pressure, not by out-damaging re-forms | 3–4.5 min including the valve; 40–60% HP |

**Hazards (not encounters):**
- **Flarecap stretches** (G4, G5): orange-cap zones are Surging (heavy periodic damage); a struck orange seam bursts (moderate damage, knock-back).
- **Heat rooms** in the drain (G6): Working zones with timed vents and a niche each.
- **Glass vents** on the crossing (H2) and in the circle: amber = breathing (timed exhale), red-crazed = surging (heavy damage; do not cross).
- **The Embermind Echo** (H2, H4): a visual and audio overlay only. No collision, no damage, no effect on any volume (§C8.1).

**Rules**
- **Defeat at 0 HP** (CDR-1). The Deepbrand crew take the ordinary defeat presentation; the line after the fight is one sober bark from Darven (`EGH-B2.4`). Glasswalkers and the Revenant collapse into ash. **No enemy is cleared by the condition ending**: when the pocket is bled, nothing re-forms, and those standing fight on.
- **Re-forming is a place rule** (rulings §3.1.2; bible §2.7): it depends on the pocket pulsing, never on health or time-in-fight. On the crossing (no condition) glasswalkers do not re-form.
- **Melee or ranged** (CDR-2): every fight accepts both. The crossbow can be duelled or climbed to. In the circle, ranged players can thin glasswalkers from the frame's lee but must cross to the valve; the pulse brings back what was out-ranged, and the Revenant's Shatter and advance close distance. Out-ranging never ends the fight: only the valve does. Ranged is never required.
- **Combat never reveals evidence.** The order is in the crew's tin; the site is read in place; the roll is on a shelf; the account is Seredh's. Deepbrand guards carry ordinary loot and nothing else; no paper is found on a body.
- **Non-combatants:** Darven, Hesper, Kaevren, Yorven, Marenya, Maeryn, Seredh and every citizen are never targetable. Darven is never engaged by enemies (he waits behind the corner at G1 and at the camp).
- **Death:** respawn at the Cooling House during `S00`, `S01`, `S08`; at the old works approach (G1) during `S02`–`S04`; at the crew camp (G7) during `S05`–`S06`; at the annex lower stacks door (A1) during `S07` until the roll is signed out, and at the Cooling House after that. Defeated Deepbrand crew and crossing glasswalkers stay defeated. In the circle: the valve's completed segments are kept and the pulse's reach stays shrunk; the Revenant and its glasswalkers reset to full (ordinary leash reset). Site inspects are kept.
- **Co-op:** every fight shared; a defeat credits each partner whose own active step consumes it (CDR-6). Each partner's warrant, route choice, tags, site reading, valve, roll, stone and choice are their own. The pocket valve is a per-player prop: a partner may fight in another's circle, but bleeding the valve advances only the bleeding player's own step; which state drives the shared pulse when partners' valves differ is a presentation question for Sol (Mire Integration Q-18 pattern) and never decides a partner's step or credit.

## C8. The discovery moments: presentation specs

### C8.1 The Embermind Echo (Beat 5, Beat 6)

**What it is:** a resonance phenomenon that shows hallucinations of past fires (dossier §XII; bible §2.4). It is a **hazard** that does nothing: it overlays the scene and never changes the ground, and it **never identifies anyone**. What it shows is not the night as it was; it is fire.

| Element | Spec |
|---|---|
| **Warning** | The faint emberlight in the walls pulses brighter once and a low roar rises (~1.5 s). |
| **Overlay** (~8 s) | Walls of flame sweep across the floor in sheets; heat-shapes, blurred and featureless, run in every direction (never faces, never figures you can count, never a shape in a frame); glass falls from the roof and never lands; a roar. |
| **Underneath** | Nothing changes. The patrol tells keep their true states and read through the overlay on inspect. Vents breathe on their own cycle. Glasswalkers keep cracking the glass. Collision and damage are untouched. |
| **First time** | Journal line: *Read the tells, not the vision.* Darven's voice from the edge if in earshot: "It's not there! Read the beads!" (`EGH-B5.2`). |
| **In the circle** | The Echo continues on its cycle during the fight. It does not sync with the pulse. |
| **Never** | It shows no person, no number, no frame, no child, no ritual. Nobody treats it as evidence. Asked later, Yorven: "I've seen it from the tunnel. It's just fire. It's always just fire." |
| **Accessibility** | A reduced-overlay option (the Echo shown at low opacity with a border shimmer) for players sensitive to flashing light. |

### C8.2 The handprint (Beat 5)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Approach** | The player passes under the old door arch. The ash film on the glass-sheathed jambs is grey and even. |
| ~0.5 s | **The print** | On the left jamb, at a child's shoulder height, a clean **handprint** stands out of the film: small, fingers spread, as if someone steadied themselves going through. |
| ~1.0 s | **The shimmer** | The glass inside the print shimmers faintly with heat, the way air does over a stove. Nothing else on the jamb does. |
| ~3 s | **After** | The shimmer fades as the player walks on. The print stays. |
| Inspect (optional) | | "Warm. Warmer than your hand. The glass round it is cold." (`EGH-I7`) |
| Never | **Explanation** | No one explains it. It is never evidence and never used as a hold for the child at the door: the second sheet and Seredh's stone carry that. If the player mentions it to Seredh: he says nothing at all, and wraps the stone. To Yorven: "I'd leave that where it is." |
| UI | | No highlight, no UI. Camera with the player. |

### C8.3 The roll beside the niche (Beat 7)

| Element | Spec |
|---|---|
| **Object** | One sheet of heavy paper, folded once. Top: a rectangle cut out with a knife, edges old and brown. Below: a line of script. Then lines that the glass ran over, each a milky raised ridge, letters visible under them and unreadable. One line clear. The lower half glassed thick, with a hard ridge along its edge. |
| **Reading** | Document view (dialogue file). The legible line shows the name **Iven Calder** (ED-3, ruled 2026-11-15) and *placed at the centre*. |
| **The match** | At the reading table, with `EGH_SITE_READ`, a comparison option: the player lays the roll's ridge against the drawing they have in memory of the niche lip (presented as an inspect line, not a minigame): "The ridge runs straight along one edge and turns at the corner, like the lip of the niche. The glass ran up against this sheet where it lay." |
| **Never** | No other line is legible under any light or magnifier. The heading cannot be recovered. Nobody reads the name aloud. |

## C9. Quest structure for implementation

### C9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to Hesper Tolk at the Cooling House. | `EGH-D1` end with accept | Yes | Available when EH-M2 Completed **and** (TF-M3 or MR-M2) Completed `[ED-7]`. Locked journal entry otherwise (names both). Re-offer `EGH-D1.90` |
| `S01_darven` | Find Darven Mott and collect the warrant. | `EGH_DARVEN_HEARD` + `EGH_WARRANT` | Yes | Any order. Variant option `EGH-D2.40`/`.43` (`EGH_COMPARED`) |
| `S02_mouth` | Get into the gallery. | EGH-E1 defeated + tag board inspect + seal plate channel + cap inspect + enter fall volume (G5) | Yes | Sets `EGH_FLARECAP`. G4 pinned Cool/Surging by cap |
| `S03_fall` | Get past the glassed fall. | Fall cut (3-segment channel on the right face) or drain exit volume beyond the fall | Yes | Sets `EGH_FALL` = cut / drain. Drain heat rooms pinned Working |
| `S04_crew_camp` | Find the crew. | Warrant cloth laid + tags taken + day-book read + work order taken + `EGH-D6.20` end | Yes | Sets `EGH_DAYBOOK_READ`, `EGH_WORK_ORDER`; carry-state tags and order |
| `S05_hollow` | Cross the Hollow. | Enter the circle rim volume (H4) | Yes | Echo cycle on (`hollow.echo`). Handprint event (`hollow.handprint`) on passing H3 sets `EGH_HANDPRINT_SEEN`. EGH-E2 on the crossing |
| `S06_circle` | Read the circle. | EGH-E3 all defeated + valve bled (3 segments) + four site inspects + `EGH-D7` end | Yes | Sets `EGH_POCKET_BLED`, **`EGH_SITE_READ`** (R09 site evidence) |
| `S07_roll` | Read the record of the night. | `EGH_ROLL_READ` + `EGH_NICHE_MATCH` + `EGH_SHEET_READ` + `EGH_KEEP_SEEN` + `EGH_PROVENANCE` + `EGH_STONE_HEARD` | Yes | Item **`EGH_roll`** gained at `EGH-D8.32`; the sign-out (`EGH-D8.30`) needs `EGH_PROVENANCE` and the four table readings (`EGH-D8.36` otherwise). Journal line (Iven Calder) on `EGH_ROLL_READ` (`EGH_INITIATE_JOURNAL`). `EGH_INSPECTION_GAP_SEEN` optional |
| `S08_truth` | Decide who hears it first. | Tags given + choice in `EGH-D10` + chalk event (`told`) or Kaevren's first line (`kept`) | Yes | Sets **`EH_HOLLOW_TRUTH`**. `EGH_ORDER_SHOWN` optional. Item `EGH_roll` removed (Kaevren returns it under seal). Quest → **Completed** |

### C9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `EGH_DARVEN_HEARD` | `EGH-D2` end | `S01` | — |
| `EGH_WARRANT` | `EGH-D3.12` | `S01`; `EGH-B2.2` option | — |
| `EGH_COMPARED` = shatterfall / banners | `EGH-D2.41` / `.44` (optional) | — | None |
| `EGH_FLARECAP` | Cap inspect (`EGH-I3`) | Cap inspect text | EFS (Breck: "You've been under the city. Cap's the same everywhere."); EH-M4 |
| `EGH_FALL` = cut / drain | `S03` | `EGH-D6.03` | — |
| `EGH_DAYBOOK_READ` | Day-book read | `S06` journal hint (the red handle) | — |
| `EGH_WORK_ORDER` | Work order taken | `EGH-D10.20` option | EH-M5 (Kaevren's intercepts: "The gallery order was the first I could hold.") |
| `EGH_ORDER_SHOWN` | `EGH-D10.22` (optional) | — | EH-M5 (Kaevren's first line) |
| `EGH_HANDPRINT_SEEN` | `hollow.handprint` event | `EGH-D9.40` option | None (R19 seed; deliberately unexplained) |
| `EGH_POCKET_BLED` | Valve channel complete | Post-quest circle state | — |
| `EGH_SITE_READ` | Four site inspects | `EGH-I13` comparison option | R09 guaranteed path (with the roll) |
| `EGH_ROLL_READ` | Roll document read | Journal | — |
| `EGH_INITIATE_JOURNAL` | `EGH_ROLL_READ` | — | **CV-M4** (the binding needs the name) (ED-3, ruled 2026-11-15) |
| `EGH_NICHE_MATCH` | `EGH-I13` | `S07` | — |
| `EGH_SHEET_READ` | Second sheet read | `EGH-D10.40` | EH-M4 (Dahrin: "You've read 'held below'. I was below.") |
| `EGH_KEEP_SEEN` | Wrapper inspect | `EGH-D8.20` option | EH-M6 (the junction book's annotation hand) |
| `EGH_PROVENANCE` | `EGH-D8.11` | `S07` | — |
| `EGH_INSPECTION_GAP_SEEN` | Register inspect (optional) | `EGH-D8.40` option | **CV-M1** (R16; request) |
| `EGH_STONE_HEARD` | `EGH-D9.32` | `EGH-D10.42` | EMS (Seredh: "You held one already."); EH-M4 |
| `EH_HOLLOW_TRUTH` = told / kept | `S08` choice | `EGH-D10.40`–`.66`, `EGH-B10` | Memorial props (EP11); ENW; EH-M6 (§9.3 item 4); CV-M1 |

### C9.3 Choice: who hears the Hollow truth first

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Told** (`EH_HOLLOW_TRUTH = told`) | The Cooling House hears it from the warden's hand; Hesper chalks *NOT A COLLAPSE* on the plaque; Cinderwall argues. The roll goes back to the annex under Kaevren's seal. | The city hears an account built on one roll, one site and one Volkhari stone the player cannot name; some say the warden's hand made it up (barks); Deepbrand knows who was below. Seredh's terms hold: nobody hears whose stone. | ENW: Imra Brask reads the chalk. EH-M6: Hesper Tolk and Darven stand together at the tally board. CV-M1: the Hollow truth is already in Cinderwall's mouth. |
| **Kept** (`= kept`) | Hesper hears that her brother died in a pocket on a Deepbrand cut. Kaevren and Marenya hold the rest until the evidence is complete. Kaevren opens a second ledger. | Hesper buries her brother without knowing what he was cutting toward; the plaque stays clean; the ward goes on saying "forge collapse". | EH-M6: Kaevren comes to the tally board with his second ledger. CV-M1: the Hollow truth enters the record through Kaevren's custody. |

**Neither is wrong.** Both bury the crew with dimmed flames, both return the roll to its shelf with a custodian's seal, both keep the Iven Calder line in the player's journal, and both keep Seredh's stone unnamed.

## C10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Flarecap reading | Knowledge | Orange cap means a live vein; follow the pale. No region flag (`EGH_FLARECAP` local). |
| Darven's Gallery | Access | Revisitable to the crew camp and the outer glass under Kaevren's post; the circle is quiet. |
| The Iven Calder journal line | Knowledge | Kept for CV-M4 (ED-3, ruled 2026-11-15). |
| Skill XP | Action only [GD] | Melee or Ranged at defeat; Mining if done personally. No lump quest XP. |
| Small payment | Currency | None from Hesper (she has nothing); Kaevren pays the warrant-holder's fee at `S08` (small). Economy tuning [GD]. |
| Side-quest unlocks | Story | EAD, ENW; EMS (with ETB) |
| EH-M4 | Story | Journal lead on completion: *Maeryn Vall has sent for you again.* |

## C11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| EH-M3 locked | The journal entry names both alternatives. Hesper is talkable and does not ask. No other gate. |
| Player cannot or will not mine | Darven's drain (Option B): longer, two heat rooms. Never blocked. |
| Player strikes the orange face | Heat burst (damage, knock-back); nothing resets. |
| Player is beaten at the mouth | Respawn at G1; defeated crew stay defeated. |
| Player loses their way in the Echo | The Echo never blocks or harms. Patrol tells mark the safe line. The overlay ends in ~8 s. |
| Player is beaten in the circle | Respawn at the crew camp. Valve segments kept; pulse reach stays shrunk; Revenant and glasswalkers reset. Site inspects kept. |
| Player tries to leave by the mouth after `S06` | Yorven's bark: "Doubled. I told you." The mouth route back is closed for `S06`–`S07` (a Deepbrand barricade prop, not an encounter); the bypass is the way out. Re-opens post-quest under Kaevren's post. |
| Death | Respawn by step (§C7). Warrant, tags, work order, roll and sub-objectives persist. |
| Logout | Restore to the persisted step: Cooling House (`S00`, `S08`), Red Door clinic or the Marshal's office (`S01`), old works approach (`S02`–`S03`), crew camp (`S04`–`S06`), annex lower stacks door or Maeryn's shop (`S07`). |
| Walking away | Quest stays Active. Resume hooks: Hesper ("Still waiting. I've got good at it."), Darven at the clinic or camp ("I'm still here. They're still there."), Marenya at the annex ("The shelf is open. It doesn't stay open forever, but it has today."). During `S07` the annex street door admits the warrant-holder, so a player who leaves before signing out returns without the bypass; the sign-out waits for the four table readings (`EGH-D8.36`), so nothing that can only be read in the annex is left owing once the player goes to Maeryn's. |
| Fail state | None. |
| Co-op | Shared fights. Per-player warrant, route, tags, site reading, valve, roll, stone and choice. Each partner signs out their own roll (presentation: one box, per-player item). Seredh's back-room scene is per player (a partner waits in the shop). Presentation follows each player's own state (CDR-6). |

## C12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Compound prerequisite** `[ED-7]` | Quest data / Systems | EH-M3 available when EH-M2 is Completed **and** either TF-M3 or MR-M2 is Completed. **Smallest form:** a derived quest-local flag `EGH_GATE_OPEN` set by a world rule on the completion of TF-M3 or MR-M2 (either), so the offer needs only an AND of `EH-M2 Completed` and `EGH_GATE_OPEN`. **Possible new need:** if the quest runtime cannot express an OR in availability, this derived flag is the fallback and needs nothing new. The locked journal entry lists both alternatives as text. |
| **Embermind Echo overlay** (`hollow.echo`) | Art / VFX / audio | A timed screen and world overlay (~1.5 s warning, ~8 s overlay, ~25 s cycle) in the Hollow volumes. Presentation only: no collision, no damage, no effect on hazard volumes or AI. Per player. A reduced-overlay accessibility option. Scripted presentation event; no new system. |
| **Glasswalker crack step** | Art / VFX | A decal and sound on each footstep of the glasswalker variant. |
| **Pocket pulse with shrinking reach** (EGH-E3) | Gameplay | A timed event on the pocket vent (~30 s, ~3 s tell) that spawns a ring hazard to a reach set by valve segments (3/2/1/0 thirds), and re-spawns defeated party members while reach > 0. Standard boss telegraph and add-spawn pattern (Mire MBR-E5 precedent). |
| **Flarecap zones** | World state | Cap props with pale and orange states (gameplay tells, not art direction); orange stretches tied to Surging hazard volumes; struck-seam burst as a refused interaction. |
| **Quest-pinned heat states** | Systems | G4 by cap; G6 Working; H2 vents per tell; circle Surging until the valve is bled, then Working. |
| **Channels with kept progress** | Systems | Seal plate (2), fall (3), valve (3). |
| **Document views and comparison inspect** | UI / dialogue | The roll, the second sheet, the wrapper, the day-book, the work order, the register; the niche comparison as a flag-gated inspect line. |
| **Journal entry with the initiate's name** | Quest data | The Iven Calder line stored as a journal entry (ED-3, ruled 2026-11-15); a standard localised string. |
| **Carry-state objects** | Systems | Warrant, tags, work order. |
| **Memorial prop** | Art / world state | The EP11 plaque with a chalk overlay per player on `told`. |
| **Barricade prop** | World state | Deepbrand barricade at the mouth during `S06`–`S07` (non-interactive). |
| **Agility trigger** | Systems | Drain culvert step; walkable fallback round the sump. |
| Creatures | Schema / Gameplay | Deepbrand Crew guard, crossbow; Ashfall Revenant glasswalker; the Hollow Revenant (elite) (bible §10). |

**New runtime needs: one possible, with a fallback that needs none.** The compound OR prerequisite (`[ED-7]`) may need runtime support; the derived flag `EGH_GATE_OPEN` is the fallback. Everything else is a standard system, a scripted presentation event, or the Mire's pulse-and-add-spawn pattern.

## C13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The forge collapse** (R09) | The precursor's amplification ritual with Volkhari captives, meant to end the war, which it did; an initiate at the centre became the Titan (bible §2.2). | A collapse of the lower forge. | The circle site; the roll with provenance; the second sheet; Seredh's stone. | It really was a collapse; the Volkhari caused it; the Titan is a Volkhari (R09 wrong readings). | The precursor's name; who survived; how many died; how many Volkhari. | **EH-M3 (resolved here).** |
| **What came out of the centre** | The initiate, become the Fire Titan (FT-05 direction). | The Ash-Clad Giant legend. | "What came out of the centre went down and was not stopped"; "theirs, not ours"; a frame broken from inside; the Ash-Clad Giant legend. | A weapon; a monster. | What it is now; whether it suffers. | R19, CV-M4. |
| **The child at the door** | Kaelith Veyr'un, who escaped. | The Unburnt Boy, a children's story. | "One child unaccounted: the door"; Seredh's stone; the handprint (not evidence). | A ghost; the child died. | Where he is; who he is. | R09 (escape); never located. |
| **The elder held below** | Thalan Veyr, taken in the purge; alive (R10). | — | "One elder taken in the purge after. Held below." (past tense). | Long dead. | That he lives. | **EH-M4 (R10).** |
| **"Keep. Do not copy."** | A later keeper of the precursor's papers, carried into the Remnant's archive (D-C03). | — | A hand and an ink. | Marenya wrote it. | Whose hand. | EH-M6 (the junction book's hand), never named. |
| **The struck column** | The Crossing Concord's witness custom (R16). | — | A column of marks that stops; a struck heading. | A clerk's habit. | Everything. | CV-M1. |
| **The handprint** | — | — | A warm print, child-high. | Proof of the child. | Everything. | None (deliberately). |
| **Why Deepbrand wanted the cut** | The deep works want the veins round the Hollow (bible §2.3). | "Contract work." | The work order; Darven's "they wanted the veins". | Salvage. | What the veins are for. | EH-M4, EH-M6. |

## C14. Open decisions

1. **ED-3, ruled 2026-11-15:** the initiate is **Iven Calder**. The name shows only in the `EGH` roll document and the journal entry. Nobody speaks it, and nothing in Emberholt explains it (R19 is CV-M4's).
2. **The Red-Lit annex [NEW sub-site]:** the bible names "the Red-Lit annex" without a POI or placement. This package makes it a restricted annex reached from below by Yorven's old miners' bypass, with a lower stacks door, Marenya's desk and a shelf book. It is not a numbered POI; the zone package (Batch 4) may fold it into a district or give it a label. MAP VERIFICATION REQUIRED.
3. **Marenya present and signing the roll out [NEW]:** the bible has the shelf left open with her note; this package also puts her at her desk to vouch for shelf-marks (custodian, never a truth source; Part 4 ledger) and to sign the box out under the warrant, which is what lets `EGH_roll` be a carried item and gives the record a chain of custody. If the Director prefers the roll read in place only, `EGH_roll` becomes a read-in-place record, the budget drops to 1 in Act I, and `S08` has the player describe it instead of carrying it; nothing else changes. Her reason for leaving the cage open is never given (canon: she is considering leaking select pieces).
4. **Seredh in Maeryn's back room [NEW placement]:** the bible lists Seredh's memory-stone in `S07` without a place. Maeryn's back room is her canon safehouse and EH-M4's meeting place. Seredh's terms ("a Volkhari stone agrees... not whose") are the ED-12 consent, fixed rather than chosen; `EH_HOLLOW_TRUTH = told` respects them.
5. **The second sheet's wording [NEW, within ED-3] (cut back by the independent review, 2026-11-14):** the sheet now says "What came out of the centre went down and was not stopped" and "Volkhari held for the circle. One child unaccounted: the door", beside the bible's §2.2 lines ("shift above: not ours", "closed the war", "one elder taken in the purge after; held below"). It gives no count, no name, no precursor name. Two phrases were cut. (a) *"Entered in the night book as: the Titan"*: a precursor record naming the Titan beside the roll's one legible name identifies a named person as the Titan from one record set, which is R19's payoff (CV-M4; custodians: the roll plus Meryndis's formulae), and bible §2.4 lets the Titan be felt only through other people's words, not the precursor's papers. (b) *"not recoverable"*: it states the fate of everyone held, which bible §2.2 withholds ("how many died in the Hollow"). "Volkhari held for the circle" stays: Volkhari captives are inside R09 as the ledger states it, and Seredh's stone corroborates. **For the Director (consequential):** with the cut, R09's "an initiate became the Fire Titan" is reached by inference (the centre "went down and was not stopped", "theirs, not ours", the frame broken from inside, the Ash-Clad Giant legend), not stated by a custodian. If the Director reads R09 as requiring the record to name the Titan, restore (a) on this one node (`EGH` second sheet document) and accept that R19's identification lands in EH-M3. Restoring (b) needs an exception to bible §2.2.
6. **Darven's drain (bible wording):** the bible says the drain "avoids Deepbrand's seals" (`S01`) and is the slower way past the fall (`S03`). This package reads both as one route: the drain is how Darven came out round the fall; the sealed mouth still has to be passed, which is where Deepbrand's crew stands. If the Director wants the drain to avoid the mouth as well, `S02`'s fight moves inside (a Deepbrand retrieval crew at the fall) and the drain becomes the only entry; the step ids hold.
7. **Glasswalkers in EH-M3 [contract extension]:** the bible contract row lists Deepbrand Crews and the Hollow Revenant; §10 says Ashfall Revenants (revenant, glasswalker) are first seen in EH-M3. Glasswalkers are added on the crossing and as the Revenant's adds; the contract field in §C4 names them.
8. **The patrol tells [NEW]:** the Hollow is patrolled by Emberguard (dossier §VI.4); their old tells on spikes give the crossing a readable line. Text and props only.
9. **Kaevren's recovery detail offscreen:** the crew are brought up between `S07` and `S08` without a scene. A Director who wants the bodies carried on screen can add an escort beat; this package avoids making a player carry the dead.
10. **Lorcan Tolk [NEW name]:** the foreman, Hesper's brother. The other four crew (Tobbe, Wendel, Marit, Yeva) are named only by first name in Darven's lines and on the tags (dialogue file); removable. Renamed by the independent review (2026-11-14) from "Haskel" (too close to Lowmark's Haskin family and Thornfell's Kol Hask) and "Brin" (a homophone of Lowmark's Bryn Ruddock). No other collision was found across `04_CONTENT_PRODUCTION`, `LORE` or `00_ADMIN` for Hesper, Tolk, Tobbe, Marit, Yeva or Aubin Harl.
11. **Level framing (ED-10):** Expert identity. Mining `[GD: mid]` with the drain as the time-cost alternative.

## C15. Internal review log

| Finding | Revision |
|---|---|
| R09 guaranteed path (Revelation Ledger: "site evidence plus a restricted record with provenance in EH-M3"; bible §8.1). | `S06` requires four site inspects (`EGH_SITE_READ`); `S07` requires the roll, the second sheet, Marenya's provenance and the niche match; Seredh's stone is a required second channel. All on the main path; nothing missable. |
| R09 wrong readings supported honestly. | "Forge collapse" is the plaque and the city's belief until `S06`; "the Volkhari caused it" is answered by "theirs, not ours" and the frame broken from inside at the centre, not the rim. |
| R10 leak. | The second sheet says "held below" in the past; no Act I line says anyone is alive now. Dahrin, Thalan and the Warrens are not named. |
| D-C03. | Heading seal cut away; every line glassed but one; "Keep. Do not copy." in an unnamed later hand; no precursor name; no roster; no count anywhere (the rim rings are not countable; Darven's crew is a present-day contract crew). |
| D-C06, ED-12. | No Volkhari number; Seredh's stone is one account and its use is on his terms; nothing locates anyone; Maeryn's room is just a room. |
| Marenya's limit (custodian, not truth source). | She vouches for shelf-marks and the signing-out; asked what the pages mean: "That's yours." |
| Seredh's limit (one account; no numbers, no refuge). | He says the stone is one stone; it gives no count and no place. |
| Darven's limit (his crew and the cut only). | His "breathing walls" are his and never used as a hold; his variant answers show no knowledge of another region. |
| Kaevren's limit (intercepts, ledger; never Remnant; never fought). | He signs, warns, reads the order, opens a second ledger. |
| The Echo risked becoming testimony. | It shows fire only, no faces, no figures that can be counted, no frame, no child; it changes nothing; the lesson is to read past it. |
| The handprint risked becoming evidence. | It is never offered as a hold; Seredh's silence and Yorven's "leave that" are the only reactions. |
| The Revenant risked being read as the initiate. | It forms at the frame but is ash and heat "never the same height twice", is a family member (Ashfall Revenant), and no line connects it to anyone. |
| CDR-1 on the condition ending. | Bleeding the pocket stops re-forming; enemies standing fight on to 0 HP. Deepbrand fight to 0 HP; one sober Darven line after. |
| CDR-2, CDR-6. | Crossbow can be duelled or climbed to; the valve forces both styles across the circle; every fight solo-tuned. |
| "Fire Titan" in dialogue. | No NPC, record or inspect in Act I names the Titan. (The independent review, 2026-11-14, cut "the Titan" from the second sheet; §C14.5.) |
| Skill hook. | Mining `[GD: mid]` with Darven's drain as the time-cost alternative; heat gear recommended. |
| Cross-region gate. | Visible locked entry naming both; variant lines change no step; nothing about another region is asserted by an Emberholt NPC. |

---

## Act I cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | Yorven: Cinderwall, old tunnels, surge suspicion; never knows the precursor's work or the draw. Ralenne: sincere, unaware, never a villain. Theryn: stewardship; knows "below" is Deepbrand; never asked; hides one child (unexplained); never exposed or targetable. Selice: the glass, not motives. Maeryn: heritage never forced. Darven: his crew and the cut only. Kaevren: warrant, intercept, ledger. Marenya: shelf-marks only. Seredh: one account, on his terms. The Cinder Rat: glimpsed. |
| Evidence rule | Every finding comes from a living witness, a record or an object read in place: the slate, the valve book, the stub, the cut page, the clerk, Sarne; the lens and Selice, the ledger, Theryn; the tags, the day-book, the work order, the circle site, the roll with provenance, the sheet, the stone. The sob, the lanterns, the Echo and the handprint are phenomena and are never used as proof. No defeated enemy speaks or carries a document. |
| Revelation limits | R09 owned and paid in EH-M3. R10 not leaked. R15 planted (broadsheet, unattributed). R16 seeded (register; optional). R18 seeded (lens, column, transfers). R19 seeded (sob, roll line, "went down and was not stopped", handprint); the Titan never met or described. R11, R12 untouched. |
| Reserved decisions | Iven Calder (ED-3, ruled 2026-11-15) shown, unspoken and unexplained; D-E2 and D-S1 (ruled 2026-11-15) not touched; origin-neutral address; no "invaders", no compass direction; C07 untouched; D-C03 kept. |
| Tagging | `[ALLOCATION]` on EH-M1 `S03`, `S04`, `S07` and their nodes; `[ED-20]` on EH-M2's offer; `[ED-7]` on EH-M3's gate and variants; ED-3 (ruled 2026-11-15) on the roll and journal; `[ED-12]` on Maeryn's window and Seredh; `[ED-14]` on the broadsheet. |
| No fail, no soft-lock | Surging zones can be waited out; red cocks scald and refuse; containment cannot fail; the test re-runs; the fall has a drain; the Echo never blocks; valve and channel progress is kept; every choice completes. |
| No cutscenes | The hood flare, the sob, the row of lanterns, the lanterns dimming, the grey visitor, the Echo, the handprint and the chalk play under the player camera. |
| Solo / co-op (CDR-6) | Every step, boss and reward solo; partner credit only from a partner's own active step; personal choices and flags per player; shared presentation never gates progress. |
| Defeat model (CDR-1) | Every enemy to 0 HP. Resonance enemies re-form only by condition (exhale with unbled cocks; pocket pulse). No SX. No child, citizen, teacher, Volkhari or official is targetable. |
| Ranged (CDR-2) | Viable in every fight; required in none; never trivialising (re-forming by condition, the valve and cocks force movement). |
| Skills (CDR-4) | Smithing `[GD: low]`, Leatherworking `[GD: low]`, Mining `[GD: mid]`, each with a time-cost alternative. |
| Quest items | 2 (`EEH_ledger`, `EGH_roll`) of Emberholt's 5. |
| Region flags | `EH_TELLS`, `EH_COLD_WARD`, `EH_CURRICULUM`, `EH_HOLLOW_TRUTH` only; one writer each. |
| Geography | Only bible POIs (EP01, EP02, EP03, EP04, EP07, EP10, EP11, EP15, EP23, EP26) and dossier places, plus four sub-sites (the Red Door clinic and the Marshal's office as parts of EP02/EP01; Maeryn's back room in EP03; the Red-Lit annex, open decision C14.2). Relative placement; MAP VERIFICATION REQUIRED on every place table. No route beyond the city; no interregional travel. |
| Terminology | No release wording. Emberholt is called a milestone only in the status line. "Craft", never "magic". No "ghost", "undead", "curse". |
| Runtime | No new runtime need except a possible compound OR prerequisite for EH-M3, with a derived-flag fallback (§C12). |
| Independent review, 2026-11-14 | Authored walkthrough of EH-M1 to EH-M3 against the brief, CDR-1 to CDR-6, the Revelation Ledger, the bible and the Part 4 ledger (nothing was played; no build exists). **High:** the second sheet named the Titan in a precursor record beside the roll's legible name (R19's identification, owned by CV-M4) and said those held were "not recoverable" (a fate bible §2.2 withholds); both phrases cut, fuller wording held as a Director question (§C14.5). **Medium:** the crew's tags existed twice (mouth board and a camp peg); Darven now lifts them at the mouth (`EGH-D4.03`) and hands them over at the camp. The annex sign-out now waits for the four table readings (`EGH-D8.36`), the street door readmits the warrant-holder, and `S07` respawn is defined outside the annex, so no annex-only reading can be left owing. Seredh's stone was described as his own wartime memory, which would give a Volkhari anchor a war role the Part 4 ledger leaves unstated; its maker is now unnamed. **Low:** `EGH_PROVENANCE` and `EGH_STONE_HEARD` set-by ids aligned with the dialogue; EH-M2 `evidence` path given a Yorven resume hook and logout point; an Echo colour-grade line and a "materials" word removed (no art prescription); release-scope phrase removed from the status line. **Renames:** Haskel to Lorcan (near Lowmark's Haskin, Thornfell's Kol Hask); Brin to Wendel (homophone of Lowmark's Bryn). Checked and holding: EH-M3 gate (EH-M2 and TF-M3 or MR-M2, visible locked entry); R09 site evidence (`EGH_SITE_READ`, four required inspects) plus roll with provenance; every enemy to 0 HP, no SX, no non-combatant targetable; ranged viable, never required; solo-completable with per-player credit and choices; D-E2, D-S1, `[INITIATE]`, origins and C07 untouched; every listed bible deviation recorded in A14 or C14. Size not cut: no redundancy found whose removal would lower contradiction risk more than it risked dropping required content. |
| Batch 4 encounter alignment review, 2026-11-15 | Applied Enemies file PE-1 to PE-5 (crawler Butt and beetle burst 1.5 s; "beaten" for "downed"; Deepbrand Hook and Shield bash 1.5 s, the bash pending GD G1) and PE-20 (EGH-E3 Call fills only up to the five-standing cap). Header: the stale `TH_STANDING` / `MR_STANDING` read removed (Integration EQ-03). `EEH_ledger`: the "reappears" wording replaced; EH-M6 shows it as a board prop and it is never re-granted, so the item budget stays at five (Integration EQ-09). PE-16 (the plain revenant on the crossing) not applied: Director Q1. No id, step, flag or line changed. |
| Emberholt character rulings, 2026-11-15 | ED-3: `[INITIATE]` replaced by **Iven Calder** in the decision-tag note, Part C heading, source table, unlocks, revelation role, Beat 7, `EGH_INITIATE_JOURNAL` entry, document reading row, flag table, outcome note, knowledge table, runtime table, C14 item 1 and compliance rows; name stays spoken nowhere in Emberholt and unexplained until CV-M4 (R19). D-E2/D-S1 tag wording updated; Act I still depends on neither. No Elyndra or Speaker seeds in Act I. |
