# Emberholt Main Questline, Act III: Embergate Accounting

**Status:** Authored production content for Creative Director milestone review (2026-11-14). This package implements Emberholt main milestone **EH-M6 *Embergate Accounting*** (`EGA`), the regional capstone, as written in the bible §6 table, the §6.1 brief, the §6.2 contract row, the §9.3 tally-board attendance rules and the §10.1 boss brief, plus the post-story states and master commissions the bible's flags and ED-11 call for (§E). It follows the Emberholt Act I and Act II packages (`Caelmor_Emberholt_Main_Act_I.md`, `Caelmor_Emberholt_Main_Act_II.md`), which follow the Mire, Thornfell and Lowmark act-package format; the capstone boss spec and ending matrix follow `Caelmor_Mire_Main_Act_III.md`. Everything marked **[NEW]** is authored and not canon until the Director promotes it (ED-19: promote nothing). **[PROPOSAL — DIRECTOR]** marks content that rests on an open bible §3 decision. **[CANON]** items come from the Emberholt dossier, the character file, Factions and the Part 4 ledger. **[APPROVED — id]** items rest on an architecture ruling (FT-02d, FT-04, FT-05 direction, D-C03, D-C06). No schema, production JSON or C# is created here. Emberholt is an internal production milestone of the complete game (CDR-3). Combat follows the Director rulings (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1), every fight accepts melee or ranged and none requires ranged (CDR-2), standard RPG systems are preferred to bespoke simulation (CDR-4), and every step, the boss and every reward are completable solo with co-op as optional assistance (CDR-6). Emberholt registers no scripted-survival exception (rulings §4; bible §3 "SX proposal: none").

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Emberholt_Narrative_Production_Bible.md`. The code **`EGA`** is confirmed against bible §6 (three letters, begins with E, no collision with `ECW`, `EEH`, `EGH`, `EAC`, `ESS` or any side code). Where this package adds detail it is marked [NEW] and stays inside the bible's cast (§5), places (§4.2), flags (§9.1), encounter families (§10) and conventions (§11). Where it reads a brief more narrowly or adds a sub-site, the reason is in §14; the bible is not edited.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Emberholt_Main_Act_III_Dialogue.md`. It holds cast notes, every `EGA-` dialogue node and bark referenced here, the inspect texts, the full text of every document (Odile's runner note, the relief tags, the junction book, the collar plates, the valve-book repair entries, the tally board at morning, Thennek's slip `[D-E2]`, the Speaker's letter `[D-S1]`), the post-story barks and the master commission offer lines.

**Reserved decisions in this package. Nothing here decides them.**
- **`[D-E2]` Thalan's fate** (bible ED-4, §3.2). EH-M6 reads `EH_THALAN` in **one place only**, the tally board (bible §9.3 item 5), plus two post-story barks. `freed`: Thennek sends word, one line, on a slip Hennet carries (`EGA-D11.50`, document `EGA-I30`). `aided`: Asera comes to the board with "the account he asked for" (`EGA-D11.55`–`.58`), reading `EAC_ACCOUNT_PROMISED`. Both variants are one short beat of the same length at the same point, add no step, set no flag and change no completion. Everything else in EH-M6, including the junction book's frame-line entry (`EGA-I22`, written so it is true in both branches), is branch-neutral. A ruling for one fate deletes the other variant's nodes; nothing else changes (§14.1).
- **`[D-S1]` the Speaker** (bible ED-5, §3.2). EH-M6 reads `EH_SPEAKER` and `ESS_LETTER_READ` in the Speaker's letter (`EGA-I32`), in one Council line (`EGA-D13.12`) and in post-story terrace barks. The letter follows the reviewed Act II working layer exactly: a man who took help for his rise and sincerely believes his vigil dreams are divine; he does not know what the deep works are for and nothing here shows he knew of the draw. He never fights, never confesses, never lies outright (he thanks, reframes and omits), and stays in office. Every dependent node is tagged; §14.2 gives the swap for a "wholly puppet" or "wholly mastermind" ruling.
- **Other tags.** `[ALLOCATION]` (ED-1): the bleed house's terraces tag (`EGA-I14`), the §9.3 item 2 attendance lines and two barks. `[ED-2]`: the Ember-Fused worker's flare in `S01` (a containment, never a fight). `[ED-12]`: Volkhari presence at the board (Maeryn and Seredh with `EH_UNBURNT = kept`; Asera `[D-E2]`), each deciding what they say. `[INITIATE]` and `[ED-3]` do not apply: EH-M6 never shows, speaks or refers to the initiate's name.

---

## Act III header

### What Act III does

Act I taught the player to read heat and ended in the Glassed Hollow. Act II found a man held below in a frame that fed a proving ring, and a Speaker who asked for his rise and dreams what he is given. Act III brings it all back to the first thing the player ever read in Emberholt: the tally board at the Gate Valve House, whose last column has never balanced. In a hard frost the civic heat main fails under Cinderwall. The ward freezes above while pressure builds below. The player goes down with Veska Dunmor's crew, bleeds the pressure into one of three places, shuts splices that were entered in the city's own book as repairs, finds the deep works' **junction book**, finds the far doors barred from the other side, destroys the construct left to keep the draw, and shuts it. In the morning the frost has melted in lines along the buried main, with dark gaps where the draw ran, and at the valve house the board balances for the first time since the main was rebuilt. The player decides who receives the account.

| Quest | Code | The player learns | By doing |
|---|---|---|---|
| EH-M6 **Embergate Accounting** | EGA | That "old leaks" were a draw: splices fitted with city collars, entered in the valve book as repairs, taking heat down to the deep works for the proving rings. That nobody set a fire: in an ordinary winter the main carried the draw, and in a hard frost it could not. That whoever kept the draw barred their doors and went deeper before the frost came. That a city can write where its heat goes on a board anyone can read. | Cooking for a warming house, steadying a frightened fused worker in a crowded room, descending a failing main in three pressure stages, deciding where the pressure goes, forging wedges or holding a relief by hand, shutting splices, reading a book that was never meant to come up, fighting a construct that drinks from the draw, reading the frost at dawn, and putting the account into hands that will keep it. |

**Act III turn (Arcs §3.3 exit; bible §8.3 misunderstanding ladder):** "the Remnant is papers kept by someone and a man in a frame" becomes "a draw on the city's heat, exposed and withdrawn deeper, not ended". "The cold ward" becomes "one small case of a main that always favoured the top". "The forge collapse" becomes "the war's end in Emberholt, now in the civic record". The player leaves with Emberholt's tool for the peace: **accountable power**, a civic account that separates useful fire from hidden harm, written where anyone can read it. The word "Remnant" enters public speech here and not before (bible §1.2), as Yorven's plain word at the board (`EGA-D11.80`).

**Length:** 60–75 minutes including the tally-board scene (bible §6). **Level framing:** Expert identity (ED-10). Exact levels belong to the Gameplay Designer.

### Inputs read (region flags set by Acts I–II and side quests)

EH-M6 never asks how an earlier flag was set; it reads only values. Every value has authored content. No value can block progress. A player who did no Emberholt side quest and no Thornfell side quest has a complete, authored path.

| Flag | Values | Read in | Effect in EH-M6 |
|---|---|---|---|
| `EH_TELLS` | bool (always set) | Every tell inspect | State words in tell inspects. |
| `EH_COLD_WARD` `[ALLOCATION]` | posted / settled | `S08` attendance (§9.3 item 2); one warming-house bark | Posted: the Cooling House regulars stand behind Veska at the board. Settled: Ralenne Kharveil's clerk brings the coal book. |
| `EH_CURRICULUM` | guild / evidence | `S08` attendance (§9.3 item 3) | Guild: Idra Callow brings two teachers. Evidence: Yorven brings the assessment ledger from his strongbox and lays it on the board's ledge; it goes back to the strongbox after (CV-M4 custody unchanged). |
| `EH_HOLLOW_TRUTH` | told / kept | `S07` one Veska line; `S08` attendance (§9.3 item 4); post-story memorial | Told: Hesper Tolk and Darven Mott stand together. Kept: Grand Marshal Kaevren Thalos comes with his second ledger. |
| `EH_THALAN` `[D-E2]` | freed / aided | `S08` attendance (§9.3 item 5) only | Freed: Thennek's slip. Aided: Asera brings the account he asked for. |
| `EH_SPEAKER` `[D-S1]` | challenged / exposed | The Speaker's letter; `EGA-D13.12`; post-story barks | One letter sentence and one Council line vary. |
| `EH_UNBURNT` (EMS) | kept / strained / unset | `S08` attendance (§9.3 item 6) | Kept: Maeryn Vall and Seredh Embercarver stand at the back. Strained or unset: no line. |
| `EH_GUILDS` (EOM) | reformed / restored / unset | `S03` forges tag and Veska's bleed line; `S08` guild reading; §E.5 | Reformed: the forges hold a relief seat open for the wardens under Durnan's new rules. Restored: the forges take it and bill the ward. Unset: neutral. |
| `EH_COMMONS` (EFC) | bool | `S01` | True: the Heat Commons rota has the warming house open and the cots laid before the player arrives; the blankets sub-objective is already done. False: the player carries blankets from the Commons store. |
| `TAS_ACCOUNT` (Thornfell TAS) | named / held / unwritten / unset | `S08` attendance (§9.3 item 7) | Named: Tessaly Varn stands with the masons and says one line. Any other value: no line. Never required, never a gate. |

| Quest-local flag from an earlier package (never required) | Read in | Effect |
|---|---|---|
| `ECW_SHORTFALL_SEEN` (EH-M1, always set) | `EGA-D10.02` | Odile: "You read this board once. Read it again." (the line Act I promised) |
| `ECW_RAT_SEEN` (EH-M1) / `ESS_RAT_PAID` (EH-M5, always set) | `S02` grille (`EGA-D4.40`) | The Rat at a grille in the old conduits: "Still the same place." (the line Act II promised). Never explained. |
| `EAC_PLATE_READ` (EH-M4, always set) | `EGA-D4.10` | Veska: "Plates? Down there? Then you know what red means under your feet." (the line Act II promised) |
| `EAC_SLATE_READ` (EH-M4, always set) | Junction book read (`EGA-I22` inspect line) | "You've read this heading before." (the line Act II promised) |
| `EAC_ACCOUNT_PROMISED` `[D-E2]` (EH-M4, aided only) | `EGA-D11.55` | Asera: "He asked for an account. You promised one." |
| `EGH_KEEP_SEEN` (EH-M3, always set) | Junction book margin (`EGA-I23`, optional) | The margin hand is the hand of *Keep. Do not copy.* Nobody is named (D-C03). Sets `EGA_HAND_MATCHED`. |
| `EEH_TAVI_STRUCK` (EH-M2) | `EGA-D11.30`/`.35` | Idra (guild) or the open ledger (evidence) mentions the struck line. |
| `ESS_LETTER_READ` `[D-S1]` (EH-M5, always set) | The Speaker's letter inspect (`EGA-I33`) | The letter is in the same hand as *To the Seat*; the player's journal sets *"I ask that the city not be frightened"* beside *"The city will learn from this night."* Presentation only, never evidence. |
| *Shift Supper* (ESP) Completed | `S01` Cooking hook | Hennet: "You know this one. Pails, lids, salt last." Flavour only. |

### Region flags this act sets

| Flag | Values | Set by | Notes |
|---|---|---|---|
| `EH_HEAT_MAIN` | terraces / ward / forges | `S03_bleed` (the relief opened) | Where the pressure went on the frost night. Read by `S07`, the board, §E and barks. |
| `EH_ACCOUNT` | guilds / council | `S08_tally` (the choice) | Who received the account. Read by §E and **CV-M1** custody. |
| `EH_STANDING` | bool | `S08_tally` (completion) | Always true at completion. Opens Emberholt master commissions (§E.10) and the CV-M1 standing gate. |

Act III invents no other `EH_` flag. Quest-local flags use `EGA_` (§9.2). Every flag has exactly one writer.

### Quest-item budget (bible §9.4: five for the whole of Emberholt)

| Item | Quest | Fate |
|---|---|---|
| `EGA_junction_book` (the deep works' junction book: a ruled book in oilcloth with Deepbrand's mark burnt into the cover) | EH-M6 | Taken from the fitter's cabin in `S04`. Read there (required). Removed at `S08`: with `guilds`, Durnan Volkryst locks it in the Basalt Forge Guild strongroom after the reading; with `council`, Magister Vael Trossen enters it in the Council's book and keeps it under his seal. Not droppable, not sellable. |

**Act III total: 1. Emberholt total: 5 of 5** (`EEH_ledger`, `EGH_roll`, `EAC_sigil_stone`, `ESS_letters`, `EGA_junction_book`). The budget is now full. Everything else is a carry-state object (the stage-cock handle, the collar plates, the bleed wedges, the shift-supper pails, the blankets), an inspectable world object (tells, relief tags, splice collars, the far doors, the valve book, the tally board, the slip, the letter), or knowledge in flags.

### Canon grounding (Act III)

| Element | Source | Status |
|---|---|---|
| The Remnant draws on the civic heat main for its deep preparations; in a hard frost the main fails under Cinderwall; no one set a fire; the Remnant withdraws deeper rather than being destroyed; a short Council scene reads what was found | Arcs §3.3 EH-M6 row | [PROPOSAL] architecture, adopted by the bible |
| Perfect Flame: advanced embercraft made reproducible through conditioning and controlled knowledge; its climax is CV-M4's | World Truth §B; bible §2.5 | [APPROVED — FT-04] |
| The Fire Titan felt only through other people's words; its binding is CV-M4's; containment, not a kill | Bible §2.4; Arcs CV-M4 | [APPROVED — FT-05 direction] |
| Deepbrand: excavation, containment, ritual infrastructure; "doesn't rescue you; retrieves what's left" | Factions §2 | [CANON] |
| Emberdeep Sentinels: Remnant constructs of embersteel and ember veins that patrol sealed chambers | Dossier §XII | [CANON] |
| Dross Scavengers ("Clandestine Remnant scavengers" on the Dross); Slag Beetles burst into sparks | Dossier §VII.5, §XII | [CANON]; scavengers as pipe-strippers [NEW, bible §10] |
| Ember-Fused Workers: laborers exposed to unstable emberstone; non-lethal containment recommended | Dossier §XII | [CANON]; never combatants (ED-2) |
| Yorven Khelt: District Overseer, a Council member; rose from miner; loyal to his district | Factions §5; character file | [CANON] |
| Durnan Volkryst, Forge-Master of the Basalt Forge Guild; the guilds resent Remnant interference | Factions §8 | [CANON] |
| The Civic Council: the Speaker, Magister Vael Trossen, Magistrix Ralenne Kharveil, Trade Commissioner Oren Falx, District Overseers; several members unknowingly act under induced dreams | Factions §5 | [CANON] |
| The Speaker: warm, measured; prefers omission to lies; sincerely believes his seeded visions divine; lacks the Ashfall endgame | Character file; Part 4 ledger | [CANON]; `[D-S1]` working layer |
| The heat main, fire wardens, tells, the valve house and tally board, Cooling Houses as warming houses, the Heat Commons | Bible §1.1, §2.1, ED-13 | [NEW, adopted from Part 3] |
| The frost night; the three pressure stages; the bleed house and its three reliefs; the splice run; the junction book's text; the far doors barred before the frost; the Draw Sentinel's arena and phases in detail; the thaw lines; the board's balanced column; the reading scenes | This package (on bible §6.1, §10.1) | [NEW] |

### Structure check against the bible §6 core verbs

| Milestone | Primary verb | Distinct from |
|---|---|---|
| EH-M1 | read tells and repair the line | — |
| EH-M2 | assist and observe | — |
| EH-M3 | descend and recover | — |
| EH-M4 | find the way by sigils | — |
| EH-M5 | watch, compare and copy | — |
| **EH-M6** | **descend the failing main**, bleed pressure, shut splices, keep a ward through the night | The only quest that starts in a crowd that needs feeding and ends at a public board. The descent reuses EH-M1's bleed channel and Veska's rules ("You don't shut hot") at a scale EH-M1 could not reach. The boss uses the readable system three ways in one fight: collars to shut (EH-M1's valve work), niches that open and close on a vent's breath (EH-M1's vent breath), and floor lines that prime like EH-M4's plates. |

No set piece repeats another milestone or another region's capstone: Lowmark's holds four Marking Stones at once, Thornfell's holds a winch while a column passes, the Mire's holds a gap stone on a three-beat count. EH-M6's ends with nobody holding anything: a construct is destroyed, a valve is shut, and the evidence is frost on the ground and chalk on a board.

### Unlocks across Act III

After EH-M6: `EH_STANDING`; Emberholt master commission offers (§E.10); the warden's round (§E.9, optional, repeatable); the post-story Emberholt states (§E); the CV-M1 standing gate (with `LR_STANDING` and `MR_STANDING`). EME10 *The hourly tally* switches to its balanced state (bible §7.4).

---
---

# EH-M6 Embergate Accounting (`EGA`)

## 1. The quest in one paragraph

The first time the warden's hand walks into **Cinderwall** after the Speaker's Smile, the ward is white. Frost lies on the brass vent hoods, on the slag lanes, on the Cooling House door. People who had taken off their second coat have put it back on. In the **Cooling House**, which is a warming house tonight, **Hennet Ulm** is feeding everyone at once, **Yorven Khelt** is shouting for blankets, and **Veska Dunmor** is standing at the hood tell with her arms folded: it reads red over a room where people can see their breath. "Hot below. Cold above. She's backing up." A runner brings **Odile Prace**'s note from the gate: intake at full, every vein open, and the draws read almost nothing; the difference has gone somewhere. Before anyone goes down, the room has to get through the first hours: the player cooks shift supper for the pails or works Hennet's hatch, fetches blankets unless the Heat Commons rota already has, and when a quarrel over whose fault it is lifts the hood tell, a fused smelter-hand at the end bench flares; the player shuts the hood damper and sits with him through the healer's count. Then Veska takes her crew down. The main is failing in three **pressure stages**: scavengers are stripping brass off it in the ducts; the stage cock at the Cinderwall junction has to be bled before anyone can pass; below it, in the **old conduits** the main was laid over, the vents breathe twice as fast and the beetles have come up out of them. At the bottom, in the wardens' **bleed house**, three relief wheels lead up three lines: to **the terraces**, to **the ward**, to **the forges**. "You don't shut hot." The pressure has to go somewhere first. The player chooses, holds the relief open with forged wedges or with the crew's hands for two cycles, and the stage comes down. Along the **splice run** beyond, the main wears three collars that are not repairs: city pattern, valve-house numbers, Deepbrand's mark on the clamp. The player shuts each splice and Veska unbolts each number plate. In a **fitter's cabin** at the end of the run lies the **junction book**: *for the proving rings*; *Perfect Flame: draw holds*; *the old circle keeps this season*; *doors to be barred from the deep side at first frost.* Through the grille, in the **splice junction**, a construct stands at the central draw valve with its seams dark. The **far doors** beyond it are barred from the other side. Whoever kept the draw went deeper before the frost and left the junction to its keeper. When the player puts a hand to the draw valve, the **Draw Sentinel** wakes. It drinks from four open collars, seals the cooling niches one at a time on the vent's breath, and at the end vents its stored heat along the floor in lines the tells show. At 0 HP it seizes and cools. The player shuts the draw. The hum changes. Veska sits down and drinks from the trough ladle. "That's her. All of her." At dawn, from the stair head, the frost has melted in lines along the buried main, every lane and roof, with dark gaps where the draw ran. At the valve house Odile chalks the hour, and the last column balances. Everyone who has stood beside the warden's hand comes to the board. Who receives the account, **the guilds** or **the Council**, is the player's choice. A runner from Speaker's Hall brings a letter: "The city will learn from this night."

**What the player should remember:** a red tell over a room where you can see your breath; "You don't shut hot"; a book that calls a draw a hold; doors barred from the other side; frost written in lines with words cut out; a board that balances. **What the player should want next:** what the proving rings were holding for, and who is still below the barred doors (CV-M1 onward).

## 2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Perfect Flame as the capstone** (dossier §XIX.5: a city-wide ignition, confront the Speaker and his allies). | Rejected. FT-04 and Arcs §3.3 move the climax to CV-M4; bible §1.2 bans city-wide ignition spectacle; ED-5 and ED-8 forbid fighting the Speaker or any named figure. |
| **B. Stage the Titan or its binding here.** | Rejected. FT-05 direction: containment, not a kill, belongs to the convergence (CV-M4); bible §2.4: the Titan is never met in Emberholt. The only trace is one line in the junction book (R19 seed). |
| **C. A Deepbrand commander or crew as the boss, fought as they retreat.** | Rejected. ED-8 (bosses are constructs or animals; Deepbrand's commander reserved) and CDR-1 (no retreat or break-off). The withdrawal happened before the frost; the far doors are found barred. Nobody retreats past the player. |
| **D. The account as a trial or exposure scene with a villain unmasked.** | Rejected. Bible §2.3: nobody set a fire; the failure is the cost of a hidden draw. The scene is a board that balances and a choice of custodian. |
| **E. Frost and warming house → descent in three stages → bleed choice → splices and the book → far doors → the Draw Sentinel → morning and the thaw lines → the tally board and the custodian choice** (selected; the bible brief). | **Selected.** The capstone is civic, physical and local: heat as terrain at its hardest, a boss that is a machine, evidence from collars and books and a public board, a choice about custody, and every earlier choice standing at the board. |

## 3. Canon grounding

Act III's canon table above applies. Additional EH-M6 points:

| Element | Source | Status |
|---|---|---|
| Ember-Fused flare as a hazard ended by a containment interaction; never a combatant; no SX needed | Bible ED-2 | [PROPOSAL — DIRECTOR] ED-2 |
| The tally board's "old leaks" are the draw | Bible §2.3; Act I §A13 | [NEW] |
| `EH_HEAT_MAIN` terraces / ward / forges; `EH_ACCOUNT` guilds / council; `EH_STANDING` | Bible §9.1; Arcs §3.3 | [PROPOSAL] |
| §9.3 attendance at the board | Bible §9.3 | [NEW] |
| "The old circle keeps this season." | Bible §2.4, §6.1, §8.2 (R19 seed) | [NEW] fixed wording |
| *Perfect Flame: draw holds* as a document heading only | Bible §1.2 | [APPROVED — FT-04] heading; text [NEW] |
| The junction book's margin hand matching *Keep. Do not copy.* | Bible §2.2; Act I `EGH_KEEP_SEEN` | [APPROVED — D-C03] limited continuity; never named |

## 4. Quest summary card

| Field | Value |
|---|---|
| Working title | **Embergate Accounting** |
| Suggested content id | `emberholt.main.06_embergate_accounting` |
| Arc position | Act III capstone (Arcs §3.3, EH-M6: "Find where the city's fire is really going, and decide who it serves") |
| Prerequisite | EH-M5 Completed. Tuned for Expert identity (ED-10). |
| Offer | **Automatic** on the player's next entry to Cinderwall after EH-M5 Completed (bible §6.1): the entry makes EH-M6 **Active** at `S00_frost` (an auto-start, like EFD's board note), and that activation sets the hard frost (`EGA_FROST`, per player). Journal: *Hard frost in Cinderwall. The Cooling House is a warming house tonight.* Yorven and Veska in the warming house (`EGA-D1`). |
| Solo / co-op | Solo-clearable. Co-op partners share the descent fights, the bleed-house fight and the Draw Sentinel; the warming-house tasks, containment, stage cocks, relief choice and hook, splices, plates, book, doors, draw valve, morning scene, board scene and custodian choice are per player. |
| Target length | 60–75 minutes first time, including the tally board (bible §6) |
| Combat share | ~25% |
| Dialogue share | ~30% |
| Cooking, containment, descent, valves, smithing or holding, reading, choice | ~45% |
| Skills touched | Cooking ~[GD: mid] (optional; working Hennet's hatch for one turn is the time-cost alternative); Smithing ~[GD: mid-high] (optional; the crew holding the relief for two vent cycles is the time-cost alternative); Melee or Ranged (either; neither required) |
| Choices | Where the pressure goes (`EH_HEAT_MAIN` = terraces / ward / forges); who receives the account (`EH_ACCOUNT` = guilds / council); cook or work the hatch (`EGA_SUPPER`, flag only); wedges or hold (`EGA_BLEED_WORK`, flag only) |
| Unlocks | `EH_HEAT_MAIN`, `EH_ACCOUNT`, `EH_STANDING`; Emberholt master commissions (§E.10); the warden's round (§E.9); EME10 balanced; CV-M1 gate (with `LR_STANDING`, `MR_STANDING`) |
| **Anchor** (contract) | Fire wardens; guilds; Council (Veska, Yorven, Odile, Hennet; Durnan Volkryst; Vael Trossen) |
| **World-truth row** (contract) | H22 (the formal Remnant's present work: the draw for Perfect Flame research), H25 (present pressure; hoarding of heat by the deep works), H18 (record: Emberholt's stop enters the civic record through the account) |
| **Revelation role** (contract) | **Owns no Revelation Ledger id.** Owns the draw (bible §2.3 present wrong) and pays off EH-M1's shortfall seed (`ECW_SHORTFALL_SEEN`); Emberholt's stop and the Remnant's existence enter the civic record through what is found in the works, with provenance (Arcs §3.3). **Seeds R18** (the junction book's *Perfect Flame: draw holds* and "next series after the Kindling"; the assessment ledger at the board with `evidence`), **seeds R19** ("the old circle keeps this season"; the Rat's "Still the same place"). R09–R12 are not re-revealed; R15 and R16 are untouched. No Titan word, shape, identity or binding; no precursor name; no roster (D-C03). |
| **Recurring evidence** (contract) | Three independent holds: the **splice collars** and their number plates (physical, in the main; Veska unbolts the plates under the player's eye), the **valve-house book** (Odile's custody: each collar number entered over years as *repair, deep-works contract*), and the **junction book** (`EGA_junction_book`; Deepbrand's own record, found in its own cabin). The **tally board** balancing after the draw is shut is the public check, not a custodian. The junction book recurs in CV-M1 (custody by `EH_ACCOUNT`) and CV-M4 (R18 heading). |
| **State compliance** (contract) | Inactive / Active / Completed. No fail. The frost night is pinned per player until `S07`; every choice completes; both hooks have time-cost alternatives; channels keep progress; a beaten player wakes at the warming house with the quest Active and **every collar already shut kept shut** (bible §10.1). Choices recorded in `EH_HEAT_MAIN` and `EH_ACCOUNT`. Resume at the persisted step with a hook at the warming house (Hennet or Yorven), the stair head (a line hand), or the splice run (Veska). |
| **Combat compliance** (contract) | Dross Scavengers (human) defeated at 0 HP with the ordinary defeat presentation; Slag Beetles (wildlife) at 0 HP, bursting into sparks; the Draw Sentinel (construct) destroyed at 0 HP. No SX; no yield, retreat or break-off. Melee or ranged in every fight; ranged viable everywhere and never required; the boss has no position it cannot reach. Solo-tuned (CDR-6). No defeated enemy gives testimony or carries a document. Veska, the line hands, Hennet, Yorven, the fused worker, the healer and every citizen are never targetable. |

## 5. The places

**MAP VERIFICATION REQUIRED** for every placement below. No Emberholt terrain exists. Relative order only. Everything below the Cinderwall junction is a [NEW] sub-site of the Cinderwall Undercroft (EP15) inside the Underworks; none of it is the Glassed Hollow (EP07), the Emberdeep Warrens (EP13) or the ritual chambers (EP16), and nothing below the far doors is placed.

### 5.1 Cinderwall [EP02] in frost (return)

As Act I §A5.1, in the **frost variant** (per player, pinned by `EGA_FROST` until `S07`): hoar on every hood, lane and sill; the Cinderweave mood banners on the lane grey and stiff with ice (EME02); breath visible; the shift bell's rope frozen to its post.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W1. The arrival lane** | Offer trigger; frost barks (`EGA-B0`). | People in two coats again. A child blowing on a doorway lantern instead of lighting it. Somebody has chalked an arrow and *COOLING HOUSE IS WARM* on a door. |
| **W2. The Cooling House, a warming house tonight** | Offer (`S00`); supper, blankets, the fused worker (`S01`); the morning scene (`S07`). Respawn point for the whole quest. | Benches pushed together; cots along the walls (laid already with `EH_COMMONS`); every bowl in use. The **hood tell** over the cook-hearth reads **red** though the room is cold: the main below is backing up (§8.1). Hennet's **hearth** and three **shift-supper pails** on hooks. The **hatch** to the yard. At the end bench, a **fused smelter-hand** in a blanket with ember-veined forearms, shivering. The yard **forge** and **keep-watch bench** as Act I. |
| **W3. The Undercroft stair head** | Descent start; the line hand's checkpoint offer; the thaw lines at dawn (`S07`). | As Act I, the plaque frosted over. At dawn the stair head looks out over the ward's lanes and roofs (sightline: **MAP VERIFICATION REQUIRED**; the thaw lines must be visible from one standing point here, or the event plays at grade at the W3 stair head, framed down the nearest lanes; the roofs are a bonus, never required). |
| **W4. The Heat Commons store** | Blankets (`S01`, unless `EH_COMMONS`). | A shared store behind the wash-house: shelves of folded blankets, a rota slate. |

### 5.2 The Cinderwall Undercroft [EP15] (return): stages A and B

| Area | Stage | Purpose | Environmental storytelling |
|---|---|---|---|
| **U1. The stair niche** | A | Checkpoint; Veska's briefing (`EGA-D4`). | Ice in the quench trough; Veska breaks it with the ladle. The three tells beyond the duct mouth all read one band up: clear spur amber, working main red. |
| **U2–U4. The duct run, the vent gallery, the junction door** | A | Dross Scavengers (**EGA-E1**) (`S02`). | Frost on the upper grates, sweat on the lower ones. Brass fittings missing from brackets in a trail. At the junction door, a **sack** of stripped brass, and the broadsheet from EH-M1 torn half away. |
| **U5. The Cinderwall junction** | A | Stage cock A (`S02`); the dawn keep-watch (`S06` end). Checkpoint. | As Act I. The manifold's three cocks; the **stage cock** on the down-line below the manifold, its brass handle missing (in the scavengers' sack). Every tell red: the line is backing up from below, not surging from the vein. |
| **U7. The old conduits** [NEW sub-site] | B | Slag Beetles (**EGA-E2**); stage cock B; the Rat's grille (`S02`). | Through a warden door below the junction: the older wartime **bore** the main was laid along, brick-lined and round, the civic pipe bracketed along one side. Vent grates every ten paces breathing fast (~8 s). Two blue-washed niches. A **grille** high in one wall where an old duct meets the bore. At the far end, **stage cock B** and a warden's chalk board: *Stage B. Bleed before passing.* Checkpoint at the second niche. |

### 5.3 The deep main [NEW sub-sites of EP15]: stage C

**MAP VERIFICATION REQUIRED.** Relative order: the old conduits → the bleed house → the splice run → the fitter's cabin (a side door off the run's end) → the splice junction (through an iron grille-door) → the far doors (across the junction).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **U8. The bleed house** | The choice and the hook (`S03`); **EGA-E3**. Checkpoint. From `S04` Veska and both line hands go on with the player (the U10 door niche in `S05`–`S06`). | A square wardens' chamber where the civic main meets three **relief lines** running up through the roof. Three great **relief wheels** in a row, each with a brass tag and a tell: **TERRACES**, **WARD**, **FORGES** (§6 Beat 3). A wardens' **field forge** (a box hearth, an anvil on a stump, a quench bucket, a rack of bar stock) and a crate of old bleed wedges, all cracked. Two niches. Floor vents. A wardens' slate with years of chalk: *Bled to ward. Bled to baths. Bled to forges.* Nobody has ever chalked *terraces*. |
| **U9. The splice run** | Three splices; the collar plates (`S04`). | A long, straight gallery where the civic main runs at waist height on stone saddles. Every forty paces a **collar**: three of them wear a second, newer clamp and a branch pipe that turns down into the floor. City-pattern collars, valve-house numbers stamped on brass plates, Deepbrand's mark on each clamp. |
| **U10a. The fitter's cabin** | The junction book (`S04`). | A side room with a cot, a brazier gone cold, a bench, a tool roll with one tool missing, a pegboard of spare number plates in city pattern (blank). On the bench, the **junction book** in its oilcloth. A shift slate wiped clean except one word: *barred*. |
| **U10. The splice junction** | The far doors (`S05`); the boss (`S06`, **EGA-E4**). | §7.1.1. Behind an iron grille-door at the run's end, a round domed chamber: four splice collars set in the wall, four floor channels running to a central **draw valve** on a plinth, two niches with raised **seal plates** above them, one floor vent. A construct stands at the valve with its seams dark. A blue-washed **door niche** outside the grille: Veska's place during the fight. |
| **U10b. The far doors** | `S05`. | A pair of iron doors in the far wall where the four draw lines, joined into one, go through the stone. Barred from the far side. Warm to the hand. Chalk on this side, wiped. |

### 5.4 Embergate [EP01]: the Gate Valve House [EP26] (return)

As Act I §A5.3 (V1 public hall and tally board, V2 book room, V3 clerks' bench). In the morning (`S08`) the public hall is full: everyone the §9.3 rules bring, plus people from the gate street who have come to see a board that balances.

### 5.5 The reading (`S08`, by `EH_ACCOUNT`)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **H2. The Council chamber, Speaker's Hall** [EP28 sub-site; NEW] (`council`) | The Council reading (`EGA-D13.10`–`.30`). | A long table under a high window, the Council's **book** on a stand. Seats by office. The Speaker's chair at the head, **empty** ("the Speaker keeps vigil this morning"; a clerk's line, no comment). |
| **F2. The Basalt Forge Guild hall, the Emberforges** [EP25 sub-site; NEW] (`guilds`) | The guild reading (`EGA-D13.40`–`.60`). | A smoke-dark hall off the great forges. Hammers racked. A **guild board** of slate by the door where commissions are chalked. Forge hands in leather aprons; the wardens' crew chiefs from other wards. |

## 6. Player-facing sequence

### Beat 0: The Frost (`S00_frost`)
**Trigger:** the player enters Cinderwall (any route) with EH-M5 Completed and EH-M6 Inactive. The quest becomes **Active** at `S00_frost`, and the activation sets `EGA_FROST`: Cinderwall and the Undercroft switch to the frost variant for this player and the presentation hour is pinned at **dusk** (§9.3). Journal: *Hard frost in Cinderwall. The Cooling House is a warming house tonight.*
**Objective:** *Go to the Cooling House.*
On the lane, frost barks (`EGA-B0`). In the warming house, **Hennet** is ladling, **Yorven** is shouting for blankets, and **Veska** stands under the hood with her arms folded (`EGA-D1`). The hood tell reads **red** over a room where people can see their breath (§8.1). Veska: "Hot below. Cold above. She's not surging. She's backing up." Yorven: "Same as the first night you walked in here. Worse. Then it was an order. Tonight nobody's ordered anything." A valve-house runner comes in stamping frost off his boots with **Odile's note** (document `EGA-I1`): *Intake at full, every vein open since noon. Draws to the wards: near nothing. Old leaks: more than the whole of Cinderwall. It has gone somewhere. O.P.* Veska reads it twice and hands it to the player. "Read the tell, not the talk. That tell says the heat's under our feet and can't get up."
- **Accept** ("I'll go down with you."): `S00_frost` completes. Veska: "Not yet. The room first. Then we go down."
- **Not now:** Hennet: "Then sit and eat. The frost'll wait for you; it's patient." `S00_frost` stays Active and the frost stays for this player (§9.3); re-offered by Yorven (`EGA-D1.90`).
**Verbs:** read, listen, accept.

### Beat 1: The Warming House (`S01_warming`) `[ED-2]` on the flare
**Objective:** *Get the warming house through the first hours.* (Sub-objectives in any order; the flare fires when the first two are done.)

| Sub-objective | What the player does | Sets |
|---|---|---|
| **Shift supper** (Cooking hook) | **Option A, Cooking ~[GD: mid]:** at Hennet's hearth, cook **three pails** of shift supper (the *Shift Supper* recipe: a stew that keeps hot under a lid). Ingredients are in Hennet's store; standard cooking interactions at the hearth. With ESP Completed: "You know this one. Pails, lids, salt last." (`EGA-D2.05`). **Option B, time-cost:** work Hennet's hatch for **one turn** of the presentation hour: stand at the hatch and hand bowls out (a held interaction the player can leave and resume; the hour advances dusk → night when it completes). Hennet cooks. | `EGA_SUPPER` = cooked / served |
| **Blankets** | Without `EH_COMMONS`: fetch the blankets from the **Heat Commons store** (W4): two carries (carry-state bundle; the player can walk but not attack while carrying). With `EH_COMMONS`: already done; the rota slate on the store door reads *Warming house: opened, cots laid, H.U.*; Yorven: "The rota beat me to it. First Cooling did that. Thank whoever cooked." (`EGA-D2.30`). | `EGA_BLANKETS` |
| **The flare** `[ED-2]` | When supper and blankets are done, a quarrel starts at the long table (`EGA-B1.1`–`.4`): whose fault the cold is, whether the wardens let it go again, whether to walk up to Ashspire and sit in a salon doorway. **Heat follows the room:** the shouting lifts the hood tell's red brighter, and at the end bench the **fused smelter-hand** (`EGA-D3`; role name; never targetable) flares: the ember-veins in his forearms brighten, the blanket smoulders, a **hazard zone** (~2 m, Working heat; it never spreads) forms round his bench. People pull back. The healer from the Red Door clinic is already there. **Containment interaction** (ED-2; the EH-M2 Tavi pattern): (1) **shut the hood damper** above his bench (one interaction at the damper chain; the zone drops a band and the smoulder stops), then (2) **sit with him** through the healer's count: a 3-segment channel (~4 s each) in which the player keeps him talking while the healer counts his breaths. Hennet bangs his ladle on the pot once and the room goes quiet (heat follows the room: the hood tell dims a little). On completion the veins settle; he asks for soup. Nothing can fail; a segment interrupted by moving away is kept. | `EGA_FUSED_STEADIED` |

The step completes on `EGA-D3.30`: Veska, at the stair door with two **line hands** and a crew lamp: "Now we go down."
**Verbs:** cook or serve, carry, shut a damper, sit with someone.

### Beat 2: The Descent (`S02_descent`)
**Objective:** *Follow the main down.*
Veska briefs at the stair niche (`EGA-D4.01`–`.08`): the main has three **stages** between here and the wardens' bleed house, each with a **stage cock**; "You bleed a stage before you pass it, or it bleeds you." With `EAC_PLATE_READ`: "Plates? Down there? Then you know what red means under your feet." (`EGA-D4.10`). The crew goes ahead and stops in each niche; they do not fight (non-combatants; never targetable; never engaged).
1. **Stage A: the duct run to the junction (U2–U5).** Frost on the upper grates, sweat on the lower. A trail of missing brass. At the junction door, **Dross Scavengers** (**EGA-E1**) are prying the last fittings off the down-line with a bar; their slinger has the stage cock's brass handle in a sack (`EGA-B3` pre-fight lines). They fight to 0 HP. After: the **sack** (world object, `EGA-I6`) holds stripped brass and the handle. One sober line from Veska (`EGA-B3.5`). The player **fits the handle** to stage cock A (one interaction) and **bleeds** it (the Act I bleed channel: 3 segments, ~3 s each; kept progress). The junction's tells drop red → amber; the U5 zone swaps to Working (pressure stage A cleared; EI-PR-01).
2. **Stage B: the old conduits (U7).** Through a warden door below the junction. Veska (`EGA-D4.30`): "This is what the main was laid on. War bore. Don't touch the brick; it's hotter than the pipe." Vents breathe on a fast cycle (~8 s; ash lift ~1.5 s); two niches. **Slag Beetles** (**EGA-E2**) have come up out of the vents. At the second niche, high in the wall, a **grille**: with `ESS_RAT_PAID` (always set), the **Cinder Rat** is behind it, glass half-mask catching the crew lamp (`EGA-D4.40`): "Warden's hand. Pipes are loud tonight." (beat; flat) "Still the same place." He is gone. Nobody explains (`EGA_RAT_GRILLE`, flavour). The player **bleeds stage cock B** (same channel); U7 swaps Surging → Working.
3. **The bleed house (U8).** The step completes on entering it. Stage C (U8 and U9) is **Surging** (heavy periodic damage outside the niches); the crew stops in the niches and Veska says why (`EGA-D4.50`): the relief has to open before anyone can work the main beyond.
**Verbs:** fight, fit, bleed, time the vents, stand in a niche.

### Beat 3: The Bleed (`S03_bleed`): *the first choice*
**Objective:** *Choose where the pressure goes.*
Veska lays it out at the three **relief wheels** (`EGA-D5`): "You don't shut hot. Everything past this room is splices and a junction, and we shut none of it till the pressure's somewhere else. One relief. Two and neither carries; the main drops and the ward freezes solid." Each wheel has a brass tag and an inspect (required to read at least the one opened; all three available):

| Relief | Tag and inspect | What happens tonight | Cost |
|---|---|---|---|
| **The ward** | `EGA-I13`: *WARD. Cinderwall risers.* | The heat goes straight up the ward's own risers. Cinderwall's hoods warm within the hour; the warming house is too hot by midnight. | The ward carries the risk. Its line runs hot all night; two lanes' hoods crack and Veska's crew stands watch at the junction till dawn. |
| **The terraces** `[ALLOCATION]` on the tag only | `EGA-I14`: *TERRACES. Emberhold line.* A brass tag beside it, newer, stamped *ceremonies office* (the line EH-M1's order used). | The heat goes up the Emberhold line to the Ash Terraces' brazier channels: open stone where nobody sleeps. The safest place to put it. | Cinderwall stays cold until the draw is shut, on Hennet's hearth and its own breath. The whole city sees the terraces glow in the frost "like the Kindling come early", above a dark ward. |
| **The forges** | `EGA-I15`: *FORGES. Great hearth line.* Variant by `EH_GUILDS`: reformed: a newer tag, *Relief seat held for wardens. D.V.*; restored: an older tag, *By order only. Billed.*; unset: no second tag. | The heat goes to the Emberforges' great hearths, which can hold it. The forges bank their work and open their halls to anyone cold. | A night's work and a set of crucibles lost; the guilds remember who sent it (by `EH_GUILDS`, `EGA-D5.24`/`.25`). |

Veska will not choose (`EGA-D5.30`): "I've had a ward blamed on me once. Tonight it's your hand on the wheel. Pick the one you can say out loud in the morning." The line hands each say one thing (`EGA-D5.31`–`.32`). An option **"What would the board say?"** returns Veska: "The board says where it went. It doesn't say if you were right." (`EGA-D5.33`).
**Opening the relief** is one interaction on the chosen wheel with a confirm line; it sets **`EH_HEAT_MAIN`** = ward / terraces / forges. The wheel turns, the line roars, and the bleed house itself drops **Surging → Working** as the relief takes the pressure (EI-PR-01), so the fight and the hook below are in Working heat; the splice run beyond stays Surging until the relief is held. The surge drives **Slag Beetles** out of the floor vents (**EGA-E3**; the same encounter in all three choices).
**Holding it open** (the hook; both options at the same field forge, after EGA-E3):

| **Option A, Smithing ~[GD: mid-high]** | **Option B, time-cost** |
|---|---|
| The old wedges in the crate are cracked (`EGA-I12`). **Forge three bleed wedges** at the field forge: for each, **heat** a bar until the hearth tell shows amber (one interaction, ~4 s), **shape** a wedge on the anvil (2-segment channel, ~3 s each), **quench** (one interaction). Then **drive** the three wedges into the relief's seat (a 3-segment channel at the wheel, one wedge per segment). The relief holds open by itself. | The crew holds the wheel open by hand. Veska and both line hands set their shoulders to it; the player keeps the **vent count** for them at the wheel's tell, calling each exhale (a held interaction per vent cycle: press when the ash lifts; a missed call simply waits for the next). **Two vent cycles** (~40 s each), then the relief seats on its own. |
| `EGA_BLEED_WORK = wedges` | `EGA_BLEED_WORK = held` |

On completion the stage comes down: U9 swaps **Surging → Working** (EI-PR-01; U8 swapped when the wheel turned). Veska: "That's somewhere else now. Let's go and see what's been taking it." (`EGA-D5.60`). Nothing in this beat can fail; the choice cannot be changed once the wheel turns (it is the night's record), and the board in `S08` shows it.
**Verbs:** read tags, choose, turn a wheel, fight, forge and drive, or hold and count.

### Beat 4: The Splices (`S04_splices`)
**Objective:** *Find what has been taking the heat.*
1. **The splice run (U9).** Every forty paces the main wears a collar. Three of them wear a second, newer **clamp** and a **branch pipe** turning down into the floor (`EGA-I16`). City-pattern collar; a brass **number plate** stamped like every plate in the valve house; **Deepbrand's mark** on the clamp. Veska, at the first one (`EGA-D6.01`–`.06`): "That's not a repair. That's ours on the outside and theirs on the inside." For each splice:
   - **Inspect** the collar (required, each; `EGA-I16`).
   - Veska **unbolts the number plate** (presentation, ~3 s) and hands it to the player (**carry-state: the collar plates**, 1 → 3; `EGA-I17`). "Odile will want these. They're her numbers."
   - **Shut the splice:** a 3-segment channel (~3 s each) at the branch valve. "Now you can shut it. She's not hot any more." (Working; the rule kept). The branch pipe's tell goes clear; the main's hum lifts a note.
2. **The fitter's cabin (U10a).** A side door at the run's end (`EGA-I18`, `EGA-I19`). On the bench, the **junction book** in oilcloth (**`EGA_junction_book`**, quest item; `EGA-I21`). **Read it** (required; document `EGA-I22`). Its headings and lines, in fitters' square hands over years: valve-house numbers against *set as repair*; draws in fitters' measure (*quarter*, *half*, *full hold*) *for the proving rings*; a page headed ***Perfect Flame: draw holds.***; *Frame line: no draw. Fitter to attend.* (true in both `[D-E2]` branches); *Lower forge undercourse: do not draw. The old circle keeps this season.*; *Hard frost: the main will not carry the holds. Hold anyway. Next series after the Kindling.*; and last: *Doors to be barred from the deep side at first frost. Leave the junction to its keeper.* With `EAC_SLATE_READ` (always set): "You've read this heading before." Sets `EGA_BOOK_READ`.
   - *Optional, with `EGH_KEEP_SEEN` (always set):* a margin note on the draw-holds page, *Keep the draw. Do not log.*, is in a hand the player has seen: the slope, the ink, the way the K is made are those of *Keep. Do not copy.* on the Red-Lit wrapper (`EGA-I23`). Nothing says whose. Sets `EGA_HAND_MATCHED` (D-C03: limited continuity, never named).
   Veska reads over the player's shoulder and stops at *Hold anyway* (`EGA-D7.04`): "They knew the main wouldn't carry it. They knew what that meant up top. And they wrote 'anyway'."
The step completes when three splices are shut, three plates are carried, and the book is taken and read.
**Verbs:** inspect, shut, carry, read, compare.

### Beat 5: The Far Doors (`S05_far_doors`)
**Objective:** *Follow the draw.*
Through the grille-door at the run's end lies the **splice junction** (U10). Veska stops at the door niche (`EGA-D8.01`): "That's not ours." In the middle of the chamber, at the **draw valve**, stands a construct: embersteel plates over dark seams, a valve-wheel set in its chest, its arms hanging. **Its seams are dark** (`EGA-I20`: "It is standing still. It is waiting on something."). It does not move while the player crosses the floor and cannot be targeted (a dormant spawn); it wakes only when someone puts a hand to the draw valve (Beat 6). Veska: "Don't touch the valve till you've seen where it goes. Then we'll know what we're shutting."
Across the chamber, the four draw lines join into one and go through the far wall at the **far doors** (U10b). The player **inspects the doors** (required; `EGA-I24`): iron, warm to the hand, **barred from the far side**; a fresh scrape where the bar dropped; on this side, chalk wiped away except a corner of a mark (`EGA-I25`). Listening at the door (optional) gives nothing: no footsteps, no voices; only the hum of the line going down. Sets `EGA_DOORS_READ`. Veska, from the door niche (`EGA-D8.10`–`.14`): "Barred from their side. Before the frost; the book says so. They didn't run from us. They went before anyone came." (beat) "Whatever's past that door, it's not tonight's. Tonight's that valve." Nobody retreats past the player; nothing can be followed (bible §6.1 beat 5).
The step completes on `EGA_DOORS_READ` and `EGA-D8.14`.
**Verbs:** look, cross, listen, read.

### Beat 6: The Draw Sentinel (`S06_sentinel`): *the boss*
**Objective:** *Shut the draw.*
The player puts a hand to the **draw valve** (interaction). The construct's seams light, one band at a time, from the four open collars inward; the valve-wheel in its chest turns once; it steps off the plinth (§7.1). Veska, from the door niche: "Keeper! Get off the valve!" The **Draw Sentinel** (**EGA-E4**) fights to **0 HP** in three phases: **Draw** (it drinks from the four open splice collars; the player shuts them), **Seal** (it plates the niches one at a time on the vent's breath), **Vent** (it vents its stored heat in lines along the floor). At 0 HP it **seizes and cools**: plates go dark from the edges in; it locks mid-step and does not move again (destroyed; construct).
Then the player **shuts the draw** at the valve (a 3-segment channel, ~4 s each; no enemies remain). The four floor channels go dark; the collars' tells go clear; the hum through the stone drops and then, faintly, rises somewhere above (heat going up the civic main to the ward). Veska comes in from the door niche and sits on the plinth's edge with the trough ladle (`EGA-D9.01`): "That's her. All of her." Sets `EGA_DRAW_SHUT`.
**Getting the ward through the night.** At the Cinderwall junction (U5) on the way up, Veska stops: "Let her come up slow. Somebody keeps this junction till light." The player **keeps watch** with the crew in the junction niche (one interaction; the presentation hour advances night → dawn; `EGA-D9.10`–`.14`). With `EH_HEAT_MAIN = ward`, the crew bleeds the manifold twice in the night (presentation) and Veska says so.
The step completes on the keep-watch's end at dawn.
**Verbs:** fight, shut collars, read niches and floor lines, shut a valve, keep watch.

### Beat 7: Morning (`S07_morning`): *the strange moment*
**Objective:** *Go up.*
At the **stair head** (W3), first light (§8.2; event `cinderwall.thaw_lines`): the frost over Cinderwall has melted in long wet lines, lane after lane and over the roofs, following the buried main the player has just walked; the whole network written on the ward in dark wet stone. Where the draw ran, the lines break off into **gaps** where the frost still lies white, like a sentence with words cut out. Veska stands beside the player and looks for a long time (`EGA-D10.01`–`.04`): "Never seen her drawn on the ground before." (beat) "Read the frost, not the talk." Sets `EGA_THAW_SEEN`. Nobody explains it; it is never evidence (the collars, the book and the board are).
With `EH_HOLLOW_TRUTH = told`: Veska looks at the chalked plaque by the stair and says nothing; she touches the chalk. With `kept`: she looks at the clean plaque. (`EGA-D10.05`/`.06`; one line each, presentation.)
**The warming house** (W2), by `EH_HEAT_MAIN` (`EGA-D10.10`–`.32`; §9.4):
- **Ward:** too warm; people asleep on benches in their shirts; two hood tells cracked; Hennet asleep on his feet. "We were warm by the second bell. Too warm. Somebody's hood popped two lanes over."
- **Terraces:** cold till the middle of the night, then warming; people talk about the terraces glowing all night above a dark ward. "Pretty, from here. Lit up like the Kindling. We watched it and ate stew."
- **Forges:** warm since the second bell; half the room went to the forge halls in the night and came back with forge hands. "Forge hands sat with us. One of them can't cook. Hennet's teaching him."
Hennet hands the player a bowl in all three. Yorven: "Odile's sent another runner. She wants you at the board, and she's never wanted anybody at the board." The step completes on `EGA-D10.40`.
**Verbs:** look, read the frost, eat, go.

### Beat 8: The Tally Board (`S08_tally`): *the second choice and the account*
**Objective:** *Take the account to the valve house.*
1. **The board** (V1). The public hall is full. Odile is chalking the hour (`EGA-D11.01`). With `ECW_SHORTFALL_SEEN` (always set): "You read this board once. Read it again." (`EGA-D11.02`). The player **inspects the tally board** (required; `EGA-I28`; §8.3): intake against draws, by vein and ward, chalked by the hour through the night; the column for whichever relief the player chose shows double for the hours before the draw was shut (`EH_HEAT_MAIN`); and at the foot of the last column, where *old leaks* has been chalked every hour since the main was rebuilt, the morning hour's figure is **nothing**. The board balances. Odile has not written *old leaks*. She has written the hour, and a line: *balanced.* Sets `EGA_BOARD_BALANCED`.
2. **The numbers.** The player gives Odile the **collar plates** (carry-state removed). She takes the valve book (V2) and finds each number (`EGA-D11.10`–`.16`; document `EGA-I29`): each was entered over the years in a day clerk's hand as *repair, deep-works contract*, with the valve-house mark. "Mine. My book. My clerks' hands. Every one a repair." The junction book's numbers match the plates and the valve book. This is the account: three holds, one civic.
3. **Who stands at the board** (bible §9.3; §9.5 here; `EGA-D11.20`–`.75`). Always: Veska, Odile, Yorven, Hennet. Then each flag adds its people and one beat, in this order, each a few seconds: `EH_COLD_WARD` `[ALLOCATION]`; `EH_CURRICULUM` (with `EEH_TAVI_STRUCK`); `EH_HOLLOW_TRUTH`; `EH_THALAN` `[D-E2]`; `EH_UNBURNT`; `TAS_ACCOUNT`. Nobody is required; a player with no side quests has Veska, Odile, Yorven, Hennet, and the people the four main-line flags bring.
4. **The word.** Yorven, looking at the junction book on the counter (`EGA-D11.80`): "Whoever wrote that is what's left of something, and they're still down there behind a door." (beat) "A remnant. Call it what it is." Odile writes at the foot of the board, under *balanced*: *Draws: the deep works, below Cinderwall. Shut.* Neither line says what the remnant is left of or mentions the Hollow, so both are true under either `EH_HOLLOW_TRUTH` value and within Yorven's limits (bible §5.1). From here the word **Remnant** is in public speech (bible §1.2; post-quest barks).
5. **The choice** (`EGA-D12`). The account (the junction book, the valve-book page, the plates in Odile's tray, the board) must go somewhere it will be kept. Two hands are offered, and Veska will not choose for the player (`EGA-D12.05`):

| Option | Who takes it | The reading |
|---|---|---|
| **The guilds** (`EH_ACCOUNT = guilds`) | **Durnan Volkryst** of the Basalt Forge Guild, with the wardens' crew chiefs. "Every collar in this city was made by somebody with a hammer. We'll know whose hands." | **F2, the Basalt Forge Guild hall** (`EGA-D13.40`–`.60`): Durnan reads each splice aloud to the forge hands; the crew chiefs copy the numbers onto the guild board; copies go to every guild hall door by noon. The guilds resolve to fit no city collar without a warden's countersign. The Council is not asked. |
| **The Council** (`EH_ACCOUNT = council`) | **Yorven**, as District Overseer and Council member, with Odile's copy. "I've a seat at that table. I've never used it for anything but Cinderwall. This is Cinderwall." | **H2, the Council chamber** (`EGA-D13.10`–`.30`): Magister **Vael Trossen** reads the account into the Council's book entry by entry before anyone speaks; councillors by office; the Speaker's chair empty ("the Speaker keeps vigil this morning"). The Council orders the valve house's board read aloud at noon each day for the season. |

Both readings are short (~2 minutes), under the player camera, and end the same way: the junction book leaves the player's hands (**item removed**: Durnan's strongroom or Vael's seal).
6. **The letter** `[D-S1]`. As the reading ends, a **runner** from Speaker's Hall finds the player and hands over a sealed letter (`EGA-D13.70`; document `EGA-I32`). The player **reads it** (required). In the Speaker's own hand, warm and short: thanks for "the night you kept", and *"The city will learn from this night."* One sentence varies by `EH_SPEAKER`. With `ESS_LETTER_READ` (always set), the inspect (`EGA-I33`) sets it beside *"I ask that the city not be frightened."* Nobody comments. Sets `EGA_LETTER_READ` and **`EH_STANDING`**. **Completes** on the letter closed (`EGA-D13.80`).
**Verbs:** read the board, hand over, match, listen, choose, read.

**Epilogue (no step):** §E.
## 7. Encounters

Tuned for **Expert identity** (ED-10). Exact levels and numbers are Gameplay Designer calls; targets are intent. Any attack that displaces the player is shown at least **~1.5 s** before it lands (the authored C-1 tuning requirement used in the Mire, pending Gameplay Designer review). Dross Scavengers take the ordinary human defeat presentation; Slag Beetles burst into sparks; the Draw Sentinel seizes, cools and stays down.

| Id | Enemies (bible §10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **EGA-E1** | 3 × Dross Scavenger **scavenger**, 1 × **slinger** | Stage A: the junction door (U4) and the end of the duct run, on frosted grates | Scavengers hold the door with pry-bars; the slinger stands on the sack by the junction door and throws | **Scavenger, Bar:** lifts the pry-bar overhead (~1.0 s), then an overhead strike. **Scavenger, Shove:** shoulder dips, feet set (~1.5 s), then a shove and one-step knock-back (onto a grate if one is there: watch the ash). **Slinger, Whirl:** sling whirls with a glowing slag pellet in the cup (~1.4 s), then a shot that leaves a burning patch ~4 s. **Slinger, Reload:** ~2.5 s visible reload (the window to close). | The first fight of the night; scavengers make the main worse, not better | 60–90 s; 60–80% HP |
| **EGA-E2** | 2 × Slag Beetle **crawler**, 2 × **sprayer** | Stage B: the old conduits (U7), on and between fast vents | Crawlers guard the vents; sprayers sit on vent lips and spit | **Crawler, Butt:** lowers its head, plates glowing (~1.5 s), then a short charge-butt with one-step knock-back. **Sprayer, Spit:** rears, abdomen swelling red (~1.0 s), then a slag gob that leaves a burning patch ~4 s. **Burst:** on defeat, ~1.5 s glow, then sparks in a 1-pace ring (light damage). **Vents:** ash lift ~1.5 s before each exhale (~8 s cycle). | Heat as terrain at its fastest: fight between exhales, use the niches | 60–90 s; 60–80% HP |
| **EGA-E3** | Wave 1: 2 × crawler, 1 × sprayer. Wave 2 (~20 s later): 1 × crawler, 1 × sprayer | The bleed house (U8), out of the floor vents when the relief opens | As EGA-E2 | As EGA-E2 | The relief's roar drives the beetles up; the same fight in all three choices | 70–100 s; 55–75% HP |
| **EGA-E4** | **The Draw Sentinel** (Emberdeep Sentinel elite; the Act III boss) | The splice junction (U10) | Boss spec §7.1 | §7.1 | Act III boss (bible §10: 1 Act III boss; §10.1 brief) | 6–8 minutes |

**Rules**
- **Defeat at 0 HP** (CDR-1). No enemy flees, yields or breaks off. Scavengers fight to the last at the door; beetles to the last at their vents; the Sentinel to 0 HP. Ordinary leash/reset applies.
- **Melee or ranged** (CDR-2): every fight accepts both. In EGA-E1 the slinger can be duelled from range or reached in four steps; in EGA-E2 and EGA-E3 sprayers give ranged players targets and the niches give melee players a place to fight from between exhales. Ranged is never required.
- **Combat never reveals evidence.** The scavengers' sack holds brass and a cock handle (fittings, not evidence; a world object, never loot). The collars, the plates, the junction book and the board are found, read and matched; nothing comes from a defeated enemy. The Sentinel drops nothing.
- **Non-combatants:** Veska, the two line hands, Hennet, Yorven, the fused smelter-hand, the healer and every citizen are never targetable and never engaged. The crew waits in niches during every fight; Veska watches the boss from the door niche outside the grille.
- **Death:** a beaten player always **wakes at the warming house** (W2) with the quest Active and the step unchanged (bible §6.1, §10.1). A **line hand at the stair head** (W3) offers to take them down to the last checkpoint reached (U1, U5, U7 second niche, U8, the U10 door niche); this is a quest travel interaction, and walking down is always the fallback (defeated enemies stay defeated; bled stages stay bled). Fitted handles, bled cocks, the relief and its wedges or hold, shut splices, carried plates, the book, the read doors and **every collar already shut** are kept.
- **Co-op:** every fight shared; a defeat credits each partner whose own active step consumes it (CDR-6). Stage cocks, the relief, splices, plates, book, doors and the draw valve are per player. Pressure-stage zones are per player (EI-PR-01 per player); any shared presentation is a fallback only (bible §9; MI-CO-06 pattern) and never decides a partner's walkable ground, step or credit.

### 7.1 Boss spec: the Draw Sentinel (EGA-E4)

**What it is (author truth):** an Emberdeep Sentinel built by Remnant engineers to keep a junction: embersteel plates over ember-vein seams, with a valve-wheel set in its chest that is coupled to the draw valve. While the splices are open it drinks from them. It is a machine. It never speaks, never carries a name (its health bar reads *Emberdeep Sentinel*, the family name; "the Draw Sentinel" is a production label), and never yields evidence (bible §10.1).

**What the player sees:** a construct about three and a half metres tall, heavier than the EH-M4 Sentinels, square-shouldered, plates scorched dark, a turning wheel in its chest. While it draws, glowing lines run along the floor channels from each open collar to its feet and its seams glow one band brighter per open collar. Its eye-slit is a single bar of light.

#### 7.1.1 Arena

| Element | Spec |
|---|---|
| Shape | A round domed chamber ~26 m across. Play space is the whole floor. **MAP VERIFICATION REQUIRED** for its place under Cinderwall; size is a zone tune. |
| The draw valve | On a round **plinth** (~4 m, one step up) at the centre. The four floor **channels** run from the collars to the plinth's foot. The Sentinel starts here. |
| Four splice collars | Set in the wall at the four quarter points, each with a **shut-wheel**, a **tell** and its floor channel. Each is a channel interaction (P1). |
| Two cooling niches | Between collars on opposite sides of the chamber (**Niche L**, **Niche R**), blue-washed, each with a quench trough, a **tell above its mouth** and a raised **seal plate** that can drop over it (P2). Each niche's safe volume extends ~2 m out from the wall onto the blue-washed floor. |
| One vent | A floor grate between the plinth and the entrance grille. Its ash lifts before each exhale. In P2 it is the clock for the seals. |
| Floor plate lines | Eight iron **plate lines** run like spokes from the plinth to the wall, each set with emberglass tells; they stop ~2 m short of the niches' blue floor. Used in P3. |
| Edges | Solid stone wall. The far doors (barred) in the far wall; the entrance **grille** behind the player. No fall, no ledge, no raised firing spot. **Leash (standard):** if no player has been inside the chamber for ~5 s, the Sentinel returns to the plinth and its health returns to the top of the current phase; **shut collars stay shut**. |
| Heat | **Working** (light periodic damage outside the niches) in P1 and P3; **Surging** (heavy periodic damage outside the niches) in P2. Tells on the walls show the state. |
| Light | Crew lamp at the grille, the collars' tells, the Sentinel's seams. Every telegraph is a body pose, a tell or a ground glow readable in this light. |

#### 7.1.2 Mechanics

| Ability | Phases | Telegraph (seconds) | Effect | Counter |
|---|---|---|---|---|
| **Draw** (the condition) | P1 | Glowing line from each **open** collar along its channel to the Sentinel's feet; one seam band per open collar | Damage reduction per open collar (suggested ~20% each; 4 open ≈ 80%; GD). While any collar is open it **cannot be brought below 65%** (its seams flare white at the floor; "drawing" on hit numbers; from the wake the objective reads *Shut the collars (n/4)*; Veska calls the floor, `EGA-B5.12`). The floor is an ordinary phase gate: it never ends the fight early and nothing yields. | **Shut collars.** A 3-segment channel (~3 s each) at a collar's shut-wheel; a hit interrupts the current segment, completed segments are kept. A shut collar's channel goes dark and its tell clears. |
| **Collar Pulse** | P1 | When a player channels at a collar, the Sentinel lifts a hand toward it and that collar's tell goes **red and crazed for ~2.0 s** | A heat burst from the collar face in a 3 m half-ring: moderate damage and one-step knock-back | Step off the wheel while the tell is red; channel progress is kept; resume. No more than once per ~10 s per collar. |
| **Sweep** | All | Draws one arm back, seams brightening down it (~1.2 s) | Wide horizontal arc in front, ~4 m: moderate damage, no displacement | Step back or out of the arc. |
| **Lock-step** | P1, P2 | Eye-slit brightens, it plants (~1.5 s) | A straight charge to the point it faced, skid stop, then a ~3 s recovery where it stopped (the solo window to work a collar segment); anyone in the path takes heavy damage (~25% max HP) and is pushed aside one step | Sidestep. It never turns during the charge. |
| **Stride** | P2 | Crouches, seams flicking toward the open niche (~1.0 s) | Walks to that niche's mouth | Meet it there, or keep range; it will reach you. |
| **Seal** | P2 | Every ~20 s the **floor vent's ash lifts (~2.0 s)**; at the same moment the tell above the **open niche** goes **red and crazed** for the full ~2.0 s and the plate above the **closed** niche shudders | The open niche's seal plate drops; the closed niche's plate lifts. Anyone still in the closing niche when it drops is pushed out (one step, light damage). Exactly one niche is open at any moment. | Watch the vent; cross to the other niche. The crossing is ~20 m (about 4 s at a run) through Surging heat. |
| **Vent Cone** | P2 | Chest plates part, glow inside (~1.5 s) | A 6 m cone of heat ahead: moderate damage and a burning patch ~3 s. **Reaches into a niche's mouth.** | Step out of the cone's line. A niche is safe from the room's heat, not from the Sentinel. |
| **Vent Lines** | P3 | A plate line's tells go **amber (~2.0 s)**, then **red and crazed (~1.0 s)** | The line vents: a sheet of heat along the whole spoke, plinth to wall; heavy damage and one-step knock-back to the side | Stand between lines. Two opposite lines vent together (P3 above 15%); three below 15%, never two adjacent, so a wedge of safe floor is always open. A new set every ~7 s. The lines stop short of the niches' blue floor. |
| **Spill** | P3 | Cocks an arm back toward the **farthest** player, glow pooling in the palm (~1.5 s) | An arcing glob of heat lands where that player stood: a 3 m burning patch ~4 s | Move after the arm cocks. It is the answer to anyone holding still far away, including in a niche. |

#### 7.1.3 Phases

| Phase | Health | Pattern | Transition |
|---|---|---|---|
| **P1, "Draw"** | 100–65% (floor at 65% while any collar is open) | Four collars open on waking. The Sentinel fights from the plinth outward: Sweep and Lock-step at whoever is nearest; Collar Pulse at whoever is channelling. The room is Working. The efficient play is to **shut collars** while it is drawn away; every shut collar makes it easier to hurt. | When the **fourth collar is shut**, at whatever health it then has (never below 65%), it climbs back onto the plinth and **re-seats** (~6 s, invulnerable): its seams go from white to deep red; both seal plates slam down, and one lifts. The room goes Surging. |
| **P2, "Seal"** | From its health at the re-seat (65% or above) down to 30% | One niche open at a time; Seal every ~20 s on the vent's breath. It Strides to the open niche's mouth and fights there: Sweep, Vent Cone, Lock-step across the room when a player crosses. Melee fights it at the niche mouth from inside the safe volume; ranged fights from inside the niche or on the crossing, and must move with every Seal. | At 30% it plants on the plinth (~4 s, invulnerable); steam hisses from every joint; **both seal plates jam open** (both niches open from here); the room drops to Working. |
| **P3, "Vent"** | 30–0% | It stays on the plinth and turns to face its target. Vent Lines every ~7 s; Sweep at anyone on the plinth's edge; Spill at the farthest player. Its seams dim with each venting. | At **0 HP** it **seizes and cools**: a last line vents short and stops; plates go dark from the edges inward; it locks mid-turn and does not move again. Destroyed (construct). The draw valve is free. |

#### 7.1.4 Tuning, death, co-op

| Item | Target |
|---|---|
| Solo duration | 6–8 minutes for an Expert player with cooked food (the warming-house supper is a fair hint). |
| Solo end state | A player who reads the collars, the vent and the lines ends at 30–60% HP. No single hit above 30% max HP (Lock-step ~25% is the heaviest). Room heat damage is tuned so a player who crosses on each Seal loses no more than ~10–15% per crossing. |
| Ranged parity | P1: the collars are on the wall and must be shut by hand, so ranged players cross the room like melee players; Collar Pulse hits a channeller of either style; Lock-step crosses the room. P2: niches close every ~20 s and Vent Cone reaches the open niche's mouth, so no niche is a perch. P3: lines run plinth to wall and Spill hits the farthest player. **There is no position it cannot reach**; ranged never ends the fight faster than reading it does (CDR-2 §3.4.1). |
| Melee parity | P1: it comes to the collars; fight it there. P2: it comes to the niche mouth; fight from inside the blue floor. P3: work it from the safe wedges at the plinth's foot, stepping off its Sweep. |
| Death | Wake at the warming house (§7 Rules; bible §10.1). The fight resets to the **top of the phase the player died in** (100 / 65 / 30%). **Every collar already shut stays shut**, so a P1 retry starts with fewer open collars and a weaker Draw. |
| Logout | `S06` persists; on re-entry the fight restarts at the top of the phase the player was in, with shut collars kept (the same checkpoint as death). |
| Co-op | Shared boss for partners on `S06`; health scales per participant (solo tuning is the baseline and is never raised for groups; CDR-6). A collar shut during a shared fight counts for the encounter and is recorded as kept for each partner whose own active step is `S06`. If partners arrive with different collars already kept from earlier solo attempts, which partner's set the shared Sentinel starts with is a **presentation question for Sol** (Act I/II pattern); solo play is unaffected and no partner's progress is reduced. The draw valve channel after the fight is per player. |
| Never | It never speaks, never shows a name, never drops anything, never retreats, never re-forms. The junction book is found before the fight (bible §10.1). Veska is outside the grille and is never in its path. |

### 7.2 Hazards (not encounters)

| Hazard | Where | Telegraph | Effect |
|---|---|---|---|
| **Working zones** | Stage A and B after their cocks; stage C after the relief; the splice junction in P1 and P3 | Amber tells | Light periodic heat damage outside niches. |
| **Surging zones** | Stage A (U5) before its cock; stage B before its cock; the bleed house (U8) before the relief is opened and the splice run (U9) until it is held; the splice junction in P2 | Red, crazed tells; heat shimmer | Heavy periodic heat damage outside niches. Never a wall; a niche always turns it. |
| **Vent grates** | U2, U3, U7 (fast), U8, U10 | Ash lift ~1.5 s (U10 vent ~2.0 s in P2) | Exhale: damage and one-step knock-back over the grate. |
| **Burning patches** | From slingers, sprayers, Vent Cone, Spill | Visible flame | ~3–4 s. |
| **The fused worker's zone** `[ED-2]` | W2, `S01` only | His veins brighten; the blanket smoulders | Working heat in ~2 m; never spreads; ends with the containment. Never an enemy. |
| **Frost** | Cinderwall and the upper Undercroft, `S00`–`S06` | — | **None.** Frost is presentation only: no cold damage, no meter (ED-6). |

## 8. The discovery moments: presentation specs

### 8.1 Hot below, cold above (Beat 0)

| Element | Spec |
|---|---|
| The room | Breath visible on every face; frost on the inside of the door; the hearth burning hard. |
| The hood tell | Over the cook-hearth, the emberglass bead reads **red with a crazed skin**, though nobody near it is warm. Inspect (`EGA-I2`): "Red, crazed. The line under this room is running hot. None of it is reaching the room." |
| Heat follows the room | During the quarrel (`S01`), the red brightens; when Hennet bangs the ladle and the room goes quiet, it dims a little. It never goes clear until the draw is shut. |
| Never | No meter, no cold status, no UI. The lesson is a warden's: read the tell, not the talk. |

### 8.2 The thaw lines (Beat 7): the strange moment

| Time | Element | Spec |
|---|---|---|
| 0 s | **Trigger** | The player steps out at the stair head (W3) after the dawn keep-watch, first time. Event `cinderwall.thaw_lines` (per player). |
| ~0.5 s | **The light** | Low first light across Cinderwall's roofs and lanes. Frost on everything. |
| ~1.5 s | **The lines** | The frost is melted in long dark-wet **lines** that follow the buried main: down every lane, over the roofs where the risers run, branching at every junction the player knows. The ward's heat main drawn on the ward itself. |
| ~3 s | **The gaps** | Where the draw lines ran (the three splices' branches and the line to the junction), the wet lines **break off**: short stretches of white frost where heat has stopped running, like words cut out of a sentence. |
| ~5 s | **Veska** | Beside the player, looking: "Never seen her drawn on the ground before." (beat) "Read the frost, not the talk." (`EGA-D10.01`–`.04`) |
| After | **Fade** | Over the following presentation hour the lines widen and the frost goes everywhere; by the next visit Cinderwall is ordinary (§E.1). |
| Never | **Evidence** | The thaw is never used as a hold: the collars, the valve book and the junction book are. No caption, no prompt, no UI. Camera stays with the player. |
| Variants | `EH_HEAT_MAIN` | Ward: the lines in the ward are widest, and two hoods have dark frost-free halos where they cracked. Terraces: from the stair head, above the city, the Ash Terraces stand wet and steaming in a ring of frost (**MAP VERIFICATION REQUIRED** for the sightline; else omit). Forges: the great forges' roofs are bare of frost and smoking. |

### 8.3 The board balances (Beat 8)

| Element | Spec |
|---|---|
| The board | As Act I: intake by vein and vent, draws by ward, forge, bath, kitchen and the terraces, a totals row by the hour. Last night's rows are chalked hour by hour in Odile's hand. |
| The night | The column for the relief the player chose (Cinderwall, the terraces or the forges) reads **double** for the hours between the relief and the draw being shut (`EH_HEAT_MAIN`). |
| The foot | Every row above the morning reads *old leaks* with a figure. The morning row reads a figure of **nothing**, and beside it, not *old leaks*: ***balanced.*** |
| Odile | Counting aloud as she chalks, stops at the foot, and does not say anything for a moment. Then: "There." |
| The crowd | People from the gate street read it over each other's shoulders. Someone says it aloud for the people at the back. |
| Never | No fanfare, no music sting, no UI. A board and chalk. |

## 9. Quest structure for implementation

### 9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_frost` | Go to the Cooling House. | `EGA-D1` end with accept | Yes | Auto-started (Active) on entering Cinderwall with EH-M5 Completed; the activation sets `EGA_FROST` (frost variant and dusk pin, per player). Re-offer `EGA-D1.90` |
| `S01_warming` | Get the warming house through the first hours. | `EGA_SUPPER` + `EGA_BLANKETS` + `EGA_FUSED_STEADIED` + `EGA-D3.30` end | Yes | Cooking hook or the hatch (one turn). `EGA_BLANKETS` set at start with `EH_COMMONS`. Containment `[ED-2]` |
| `S02_descent` | Follow the main down. | EGA-E1 defeated + stage cock A bled + EGA-E2 defeated + stage cock B bled + player in U8 (entering it, or already inside when the last cock is bled) | Yes | `EGA_STAGE` = A / B / C (EI-PR-01 swaps). `EGA_RAT_GRILLE` flavour (`ESS_RAT_PAID`) |
| `S03_bleed` | Choose where the pressure goes. | Relief opened (sets **`EH_HEAT_MAIN`**) + EGA-E3 defeated + relief held (wedges driven or two cycles) | Yes | `EGA_BLEED_WORK` = wedges / held. Stage C swaps Surging → Working |
| `S04_splices` | Find what has been taking the heat. | Three splices inspected and shut + `EGA_PLATES` = 3 + item gained + `EGA_BOOK_READ` | Yes | Item **`EGA_junction_book`**. `EGA_HAND_MATCHED` optional (`EGH_KEEP_SEEN`) |
| `S05_far_doors` | Follow the draw. | `EGA_DOORS_READ` + `EGA-D8.14` end | Yes | The Sentinel is dormant and untargetable until the valve is touched |
| `S06_sentinel` | Shut the draw. | EGA-E4 destroyed + draw valve channel (`EGA_DRAW_SHUT`) + dawn keep-watch at U5 (`EGA-D9.14`) | Yes | `EGA_COLLARS` (0–4 shut, persisted) |
| `S07_morning` | Go up. | `cinderwall.thaw_lines` event (`EGA_THAW_SEEN`) + `EGA-D10.40` end | Yes | Frost variant ends for this player after the event. Warming-house scene by `EH_HEAT_MAIN` |
| `S08_tally` | Take the account to the valve house. | `EGA_BOARD_BALANCED` + plates handed over + attendance scene end + choice (sets **`EH_ACCOUNT`**) + reading scene end + letter read (`EGA_LETTER_READ`) | Yes | Item removed at the reading. Sets **`EH_STANDING`**. Quest → **Completed** on `EGA-D13.80` |

### 9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `EGA_FROST` | Quest activation (`S00_frost`) | Frost variant, dusk pin | — |
| `EGA_SUPPER` = cooked / served | `S01` | `EGA-B1.7` (a regular) | — |
| `EGA_BLANKETS` | `S01` (or `EH_COMMONS`) | `S01` | — |
| `EGA_FUSED_STEADIED` `[ED-2]` | `EGA-D3.24` | `S01`; `EGA-D10.31` | — |
| `EGA_STAGE` = A / B / C | Stage cocks; entering U8 | EI-PR-01 zone variants; respawn checkpoint | — |
| `EGA_RAT_GRILLE` | `EGA-D4.40` | — | CV-M4 (request; the Rat's "same place") |
| `EH_HEAT_MAIN` = terraces / ward / forges | `S03` relief opened | `S03`–`S08`; `EGA-D10`; the board; §E | Post-story heat states and barks (bible §9.1) |
| `EGA_BLEED_WORK` = wedges / held | `S03` hook | `EGA-D5.62` | — |
| `EGA_PLATES` (0–3) | Each plate | `S04`, `S08` | — |
| `EGA_BOOK_READ` | `EGA-I22` read | `EGA-D7`, `EGA-D11` | **CV-M4** (request: R18 heading; "the old circle keeps this season"); **CV-M1** (custody with `EH_ACCOUNT`) |
| `EGA_HAND_MATCHED` | `EGA-I23` (optional) | `EGA-D7.05` option | CV-M1 (request; D-C03 continuity, never named) |
| `EGA_DOORS_READ` | `EGA-I24` | `S05` | Later content (the barred doors) |
| `EGA_COLLARS` (0–4) | Boss collar channels | P1 Draw strength; death/logout | — |
| `EGA_DRAW_SHUT` | Draw valve channel | `S06`; thaw-line gaps | — |
| `EGA_THAW_SEEN` | `cinderwall.thaw_lines` | `S07` | — |
| `EGA_BOARD_BALANCED` | `EGA-I28` | `S08`; EME10 balanced state | — |
| `EH_ACCOUNT` = guilds / council | `S08` choice | `EGA-D13`; §E | **CV-M1** custody (bible §9.1) |
| `EGA_LETTER_READ` `[D-S1]` | `EGA-I32` | `S08` | CV-M4 (request) |
| `EH_STANDING` | `S08` completion | §E.10 | Master commissions; **CV-M1** gate |

### 9.3 The frost night (per player)

`EGA_FROST` swaps Cinderwall (W1–W4) and the Undercroft above the junction to the **frost variant** and pins this player's presentation hour at **dusk** until `S01` (the hatch option advances it to night; otherwise `S01` completion does), at **night** from `S02` to the `S06` keep-watch, and at **dawn** for `S07`; `S08` runs in the **morning**. A player who walks away keeps their frost night: re-entering Cinderwall restores it at the persisted step. Other players' Cinderwall is their own (per-player zone variant; MI-WL-01 pattern). After `EGA_THAW_SEEN` the frost variant ends for this player. No world clock and no weather system are needed.

### 9.4 Where the pressure went (`EH_HEAT_MAIN`)

| Value | The night | The morning (`S07`) | The board (`S08`) | Who pays |
|---|---|---|---|---|
| **ward** | Cinderwall warm within the hour; too hot by midnight; Veska's crew keeps the junction; two hoods crack | Warm room; sleepers in shirts; cracked hoods | Cinderwall's column double through the night | The ward: its line ran hot all night and two lanes need new hoods |
| **terraces** | The Ash Terraces glow all night above the city; Cinderwall cold until the draw is shut | Cold until midnight, then warming; talk of the glow | The terraces' column double through the night (again) | The ward waited, and the city watched the terraces lit above a dark ward |
| **forges** | The great hearths take it; the forge halls open to anyone cold; forge hands sit in the warming house | Warm since the second bell; forge hands at the benches | The forges' column double through the night | The guilds: a night's work and a set of crucibles |

Neither is wrong. Each can be said out loud in the morning, and each is on the board.

### 9.5 Who stands at the board (bible §9.3, implemented as written)

| # | Condition | Who | Beat (dialogue) |
|---|---|---|---|
| 1 | Always | Veska, Odile, Yorven, Hennet | `EGA-D11.01`–`.20`, `.80` |
| 2 `[ALLOCATION]` | `EH_COLD_WARD = posted` | The Cooling House regulars stand behind Veska | `EGA-D11.21`: a regular: "We read it on our board once. We'll read it on this one." |
| | `= settled` | Ralenne Kharveil's clerk with the coal book | `EGA-D11.22`: "The Magistrix's compliments. The coal book, as agreed. She says she would like to read the board herself one morning." |
| 3 | `EH_CURRICULUM = guild` | Idra Callow and two teachers | `EGA-D11.30`; with `EEH_TAVI_STRUCK`: "Tavi's line is still struck out. The new test spreads the flame. She passed it laughing." |
| | `= evidence` | Yorven lays the assessment ledger on the board's ledge, open at the transfer page | `EGA-D11.35`; with `EEH_TAVI_STRUCK`, the open page shows the struck line (`EGA-I31`). The ledger returns to Yorven's strongbox after (CV-M4 custody). |
| 4 | `EH_HOLLOW_TRUTH = told` | Hesper Tolk and Darven Mott, together | `EGA-D11.40`: Hesper: "Lower forge. That's where it goes down, isn't it." Darven: "Where the walls breathe." |
| | `= kept` | Grand Marshal Kaevren Thalos with his second ledger | `EGA-D11.45`: he copies the board's last line into the ledger. "Second ledger. It's getting heavier." |
| 5 `[D-E2]` | `EH_THALAN = freed` | Thennek sends word, one line | `EGA-D11.50`: Hennet gives the player a folded slip left at the warming house's back door at midnight (`EGA-I30`). No one else reads it. |
| | `= aided` | Asera brings "the account he asked for" | `EGA-D11.55`–`.58`: Asera at the edge of the crowd. With `EAC_ACCOUNT_PROMISED`: "He asked for an account. You promised one." She decides what may be written: "Write that someone was held below on heat taken from this board. Don't write who." Odile chalks it under the deep-works line with no name and no number: *Someone was held below on this heat.* (D-C06; §14 item 13). |
| 6 `[ED-12]` | `EH_UNBURNT = kept` | Maeryn Vall and Seredh Embercarver at the back | `EGA-D11.60`: Maeryn catches the player's eye and nods; Seredh does not speak. Nothing is said about them. |
| 7 | `TAS_ACCOUNT = named` (Thornfell) | Tessaly Varn with the masons | `EGA-D11.70`: "A gate book once named my crew. I like boards that say who did the work." |

Lines 2–7 play in this order, each a few seconds, and only those whose conditions hold. Nothing waits on them; the choice follows. Every line is per player (CDR-6).

### 9.6 Choices and consequences

| Choice | Option | Immediate result | Cost | Later |
|---|---|---|---|---|
| **Where the pressure goes** (`S03`) | ward / terraces / forges | §9.4 | §9.4 | §E.1, §E.4, §E.5; barks |
| **Who receives the account** (`S08`) | **Guilds** (`EH_ACCOUNT = guilds`) | Durnan reads it to the forge hands; copies on every guild hall door by noon; the guilds will fit no city collar without a warden's countersign; the junction book in the guild strongroom. | The account is public and quick, and has no law behind it; the Council hears it from the street and some councillors resent that; the guild's countersign rule slows every repair in the city for a season. | CV-M1: the book in guild custody; the guilds' public account. §E.2, §E.5. |
| | **Council** (`EH_ACCOUNT = council`) | Vael Trossen reads it into the Council's book; the Council orders the board read aloud at noon for the season; the junction book under Vael's seal. | Slower; it is in the hands of a Council several of whose members dream what they are given (EH-M5); the guilds feel passed over. | CV-M1: the book in Council custody; the Council's record. §E.2. |

**Neither is wrong.** Both put the account somewhere it is kept, both keep the board balanced, both leave the far doors barred and the deep works unexplored, and neither punishes the player.

## 10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| `EH_STANDING` | Standing | Emberholt's regional standing (bible §9.1): the narrative-legitimacy step for Emberholt master commissions (§E.10) and one of the CV-M1 gates. |
| The balanced board | Knowledge / world state | EME10 *The hourly tally* switches to its balanced state for this player; Odile calls the last column "balanced" each hour (§E.2). |
| The warden's round | Optional activity | §E.9. |
| A warden's lamp | Tool (named functionally) | Veska gives the player the crew lamp at `EGA-D9.03` ("You carried it further than I did."). A hand lamp; heat gear family; the item pass defines it (ED-11). Never required. |
| Payment | Currency | Yorven pays from the ward's box at `EGA-D10.32`; Odile adds the valve house's fee at `EGA-D11.16` (small; [GD]). |
| Skill XP | Action only [GD] | Cooking if cooked; Smithing if forged; Melee or Ranged at defeat. No lump quest XP (bible §11.6). |
| Address | Recognition | "Warden's hand" is now used by people outside Cinderwall (guild hands, the gate street, Council clerks). Origin-neutral (D-3). |

## 11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player declines the offer | The frost night stays for this player in Cinderwall; Yorven re-offers (`EGA-D1.90`). Nothing elsewhere changes. |
| Player cannot or will not cook | Work Hennet's hatch for one turn (Option B). Never blocked. |
| Player walks away from the fused worker mid-channel | The healer keeps counting; the zone stays a band down (damper shut); completed segments kept; resume. |
| Player tries to pass a stage without bleeding it | Allowed; the zone stays Surging (heavy periodic damage). The crew will not follow (`EGA-B2.4`); the next stage's cock and the relief are reachable, but the bleed house relief cannot be turned until both stage cocks are bled (its wheel inspect: "Stage B is still holding. It'll fight you."). |
| Player cannot or will not smith | The crew holds the relief for two vent cycles (Option B). Never blocked. |
| Player tries to shut a splice before the relief | Not possible: the splice run is Surging and its branch valves refuse the hand like EH-M1's red cocks (a scald and a step of knock-back; Veska: "You don't shut hot."). Nothing resets. |
| Player strikes the dormant Sentinel | Not possible: it is untargetable until the valve is touched (`EGA-I20`). |
| Player is beaten anywhere | Wake at the warming house with the quest Active and the step unchanged; the line hand offers the last checkpoint (§7 Rules). **Collars already shut stay shut** (bible §10.1). |
| Player tries to open the far doors | Not possible: barred from the far side; inspect only. |
| Death | As above. Handles fitted, cocks bled, the relief held, splices shut, plates carried, the book, the doors read and channel progress persist. |
| Logout | Restore to the persisted step, inside the player's own frost night: the warming house (`S00`–`S01`, `S07`), the last checkpoint (`S02`–`S06`), the valve house (`S08` before the choice), the reading location (`S08` after the choice). |
| Walking away | Quest stays Active; the frost night waits. Resume hooks: Hennet ("Bowl's here. Frost's here. So's everyone."), Yorven ("She's still backing up. So am I."), a line hand at the stair head ("Veska's at the last niche. She said you'd come."), Veska in the splice run ("Book's not going anywhere. Neither am I."), Odile at the board in `S08` ("I'll keep chalking. Come when you're ready."). |
| Fail state | None. |
| Co-op | Shared fights; partner credit only from a partner's own active step (CDR-6). Per-player frost night, warming-house tasks, containment, stage cocks, relief choice and hook, splices, plates, book, doors, draw valve, thaw lines, board, attendance and both choices. A partner's relief never moves another player's `EH_HEAT_MAIN`; a partner who leaves never blocks the other. |

## 12. Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| **Staged pressure in the main** (bible **EI-PR-01**) | Systems | Per-player environment-variant swaps of zone states (U5, U7, U8–U9, U10) on quest events (stage cock bled, relief held, collars, draw shut). Reuses the Mire's MI-WL-01 variant swap; **this is the bible's listed fallback form**. |
| **Frost night** | World state / Art | A per-player zone variant for Cinderwall and the upper Undercroft (frost decals, breath VFX, stiff banners) with a quest-pinned presentation hour (§9.3). Same mechanism as EI-PR-01; no weather system. |
| **Thaw lines** (`cinderwall.thaw_lines`) | Art / World state | A dawn variant of the frost decal set with wet lines along the main's path and frost-white gaps over the draw branches, swapped on the event and faded to the ordinary ward over the next presentation hour. Per player. |
| **Heat states pinned per step** | Systems | EI-HT-01 fallback form (quest-pinned), as Acts I–II. Completion releases every pin; after it, zones show the Zones §6.1 default table. |
| **Containment interaction** `[ED-2]` | Systems | The EH-M2 pattern: a hazard volume around a non-targetable NPC, a damper interaction that drops it one band, a 3-segment channel with an NPC count. |
| **Cooking at a hearth; the hatch** | Skills / Systems | Standard cooking interactions; the hatch is a held interaction that advances the presentation hour one turn on completion. |
| **Carry-state bundles, handle, plates, wedges** | Systems | Standard carry-state (Acts I–II). |
| **Relief wheels and the choice** | Quest data | Three wheel interactions; turning one sets `EH_HEAT_MAIN` after a confirm line and locks the other two (their inspects change to "The ward has its relief. One's enough."). |
| **Smithing at a field forge** | Skills | Existing heat, shape, quench; wedges are carry-state quest objects until the item pass defines them (ED-11). |
| **Vent-count hold** (Option B) | Systems | A held interaction keyed to the vent cycle (press when the ash lifts); two completed cycles seat the relief. Same pattern as EH-M5's rehearsal windows. |
| **Boss: Draw** | Gameplay | A damage-reduction buff whose strength reads the number of open collar props, plus a phase floor (65%) while any collar prop is open. Standard prop-driven buff (EH-M4 warden-frame precedent) and standard phase gate. |
| **Boss: Seal** | Gameplay | Two timed door props (seal plates) on a ~20 s cycle with a ~2.0 s tell (vent ash, niche tell). Standard timed hazard/door. |
| **Boss: Vent Lines** | Gameplay | Eight line hazards on a sequence (EH-M4 proving-ring sectors precedent). |
| **Persisted collar state** | Quest data | `EGA_COLLARS` per player; the encounter reads it on spawn. Co-op mismatch is a Sol presentation question (§7.1.4). |
| **Dormant boss** | Gameplay | The Sentinel spawns untargetable and inert; the draw-valve interaction triggers its wake. Standard scripted spawn. |
| **Quest travel at the stair head** | Systems | A line hand's "take me down" to the last checkpoint; walking is the fallback. |
| **Document views** | UI | Odile's note, relief tags, the junction book, the valve-book entries, the board, Thennek's slip, the Speaker's letter. |
| **Board variant** | World state | The tally board prop's balanced state (per player), used by EME10 after completion. |
| **Reading scenes** | Quest data / Art | Council chamber and guild hall NPC arrangements by `EH_ACCOUNT`; scripted lines under the player camera. |
| Creatures | Schema / Gameplay | Dross Scavenger scavenger, slinger; Slag Beetle crawler, sprayer; Emberdeep Sentinel elite (the Draw Sentinel) (bible §10). |

**New runtime needs: none beyond the bible's own EI-PR-01, used in its listed fallback form.** The frost night and the thaw lines use the same per-player variant swap; everything else is a standard system or an Act I/II precedent.

## 13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **The old leaks** | Deepbrand's draw lines spliced into the civic main with city collars, entered as repairs, feeding the proving rings (bible §2.3). | Old leaks. | The splices, the plates, the valve-book entries, the junction book, the balanced board. | A failing old main; careless wardens. | Nothing about the draw itself. | **EH-M6 (resolved here).** |
| **Who kept the draw** | The Remnant's deep works (Deepbrand), in the formal order that grew from the wartime precursor (D-C03). | "Below"; rumour. | Deepbrand's mark; the book; the barred doors; the margin hand (optional). | The Speaker ordered it; the Council knew. | Who; how many; where. | Later content (CV-M1 onward). |
| **The margin hand** | A keeper of the precursor's papers is still keeping things now (D-C03, limited continuity). | — | *Keep the draw. Do not log.* in the hand of *Keep. Do not copy.* (optional). | Marenya's archive is complicit. | Whose hand. | Never named. |
| **The draw holds** | Perfect Flame research holding the proving rings' draw (FT-04). | — | The heading; "next series after the Kindling". | A forge project; a heating trial. | What the holds are for. | CV-M4 (R18). |
| **"The old circle keeps this season."** | Something below the lower forge is not still (FT-05 direction; R19). | The Ash-Clad Giant legend. | One line in a fitters' book. | A forge saying; a seal schedule. | Everything. | CV-M4 (R19). |
| **The far doors** | The deep works withdrew deeper before the frost. | — | Barred from the far side; the book's last line. | They fled the player. | What is past them. | Later content. |
| **"Same place."** | Unexplained (bible §2.4). | — | The Rat at a grille. | — | Everything. | None in Emberholt (deliberately). |
| **The Speaker's letter** `[D-S1]` | He thanks and takes the moment; he does not know what the deep works are for (working layer). | The Speaker is gracious. | The letter; its hand; the line set beside *To the Seat*. | He ordered the draw; or he knew nothing of anything. | What he suspects. | CV-M4 (the Kindling). |

## 14. Open decisions

1. **D-E2 (reserved; not decided here).** EH-M6 reads `EH_THALAN` only at the board (§9.5 item 5) and in two post-story barks (`EGA-B9.12`). **If the Director rules `freed` only:** delete `EGA-D11.55`–`.58`, the aided bark and the `EAC_ACCOUNT_PROMISED` read. **If `aided` only:** delete `EGA-D11.50`, document `EGA-I30` and the freed bark. **If a different fate:** replace only those nodes; the junction book's *Frame line: no draw. Fitter to attend.* is true in every branch in which the frame no longer works him, and should be re-read against any other ruling. Nothing else in EH-M6 changes.
2. **D-S1 (reserved; not decided here).** Working layer as reviewed in Act II: the letter thanks, reframes and omits; it shows no knowledge of the draw. **If "wholly puppet":** the letter becomes a secretary's fair copy with *Sealed by the Speaker* at the foot in another hand; its text is unchanged. **If "wholly mastermind":** the text is unchanged (it is omission under any ruling); cut the `ESS_LETTER_READ` juxtaposition inspect (`EGA-I33`) if it reads as a hint of innocence. `EGA-D13.12` and the terrace barks are `[D-S1]`-safe under any ruling. He never fights, confesses, lies outright, or leaves office.
3. **`[ALLOCATION]` (ED-1).** Tagged: the terraces relief's second tag (`EGA-I14`), §9.5 item 2 (`EGA-D11.21`/`.22`) and `EGA-B1.6`. If ED-1 changes, those lines follow the new present cause; the relief itself and the cold ward survive.
4. **Why the pressure builds [NEW].** The bible says the main fails "while pressure builds below". This package explains it in play with ordinary warden rules: in a hard frost every intake is opened to full, the draw splices (sized for an ordinary winter) choke, and heat backs up in the wartime bore below the ward instead of rising. Veska's EH-M1 rule "You don't shut hot" is why the bleed comes before the splices. Text only.
5. **The far doors barred before the frost [NEW].** Implements "the Remnant withdraws deeper; nobody retreats past the player" (bible §6.1) inside CDR-1: the withdrawal is a past event read from a book and a door, never an enemy leaving a fight.
6. **The Sentinel's phase floor in P1 (65%) [NEW].** A standard phase gate that keeps the collars central; recorded for the Gameplay Designer. If removed, P1 becomes an HP phase and Draw remains a damage reduction; nothing else changes.
7. **ED-8 kept.** The boss is a construct; no named character is fought; Deepbrand's commander, Varos Keln, Meryndis, Selvara and Durell never appear.
8. **FT-05 kept.** The Titan is not met, fought, named, shaped or explained. One fitters' line seeds R19; the binding and containment belong to CV-M4.
9. **"Remnant" enters public speech (bible §1.2) [NEW].** As Yorven's plain word at the board (`EGA-D11.80`): "A remnant. Call it what it is." If the Director prefers the word to arrive differently (a Council clerk's entry, a guild notice), only that line and the post-quest barks change. *Independent review:* the line no longer refers to "that night under the lower forge" (outside Yorven's §5.1 limit; it would have published the Hollow in the `kept` branch and asserted precursor continuity in public, D-C03). Bible §1.2 says the word enters public speech "only after EH-M6"; the board is EH-M6's last public scene and Arcs §3.3 requires the Remnant's existence to enter the civic record here, so this is read as compliant. If the Director reads §1.2 strictly, the word moves to the post-quest barks and `EGA-D11.80` ends at "what's left of something".
10. **The Council scene (Arcs §3.3: "a short Council scene afterward reads what was found").** Implemented as the `council` reading; the `guilds` reading is its mirror at the Basalt Forge Guild so both options have a scene. The Speaker's empty chair is a clerk's fact, not a comment.
11. **The junction book's margin hand (optional) [NEW, D-C03].** Pays off Act I's `EGH_KEEP_SEEN` promise without naming anyone or counting anyone. Cut freely with `EGA_HAND_MATCHED`.
12. **The frame-line entry.** Written so it is true under both `[D-E2]` branches (in `freed` the frame is empty; in `aided` its coupling is sealed), so the book needs no tag.
13. **Asera's board line (`aided`) [NEW, ED-12].** Fulfils "Asera brings the account he asked for" (bible §9.3) as her consent to one chalked line that names and counts nobody (*Someone was held below on this heat.*). An earlier draft chalked *Held below on this heat: one.*; independent review removed the number: a count of the held is a Volkhari count (D-C06) and the fate and number of the held stay unresolved after the reviewed second sheet. If the Director prefers nothing chalked, she says the line and Odile does not write it.
14. **The fused worker is a role, not Myr Adalrek** (EAD's anchor), so EH-M6 does not depend on *The Vein-Touched Man*. If EAD is Completed, a Batch 3 line may let Myr be the worker; no step changes.
15. **No post-story refight [NEW decision].** The bible names no repeatable boss for Emberholt (unlike the Mire's MD-8). The Sentinel stays destroyed. The post-story activity is the warden's round and the master commissions (§E.9, §E.10). If the Director wants a repeatable construct fight, it belongs behind the barred doors in later content, not here.
16. **`TAS_ACCOUNT` (Thornfell) read for one line only** (bible §9.3 item 7). Never required.
17. **Level framing (ED-10).** Expert identity. Cooking `[GD: mid]` with the hatch as the time-cost alternative; Smithing `[GD: mid-high]` with the crew's hold as the time-cost alternative.

### 14.1 D-E2 swap note
Nodes tagged `[D-E2]`: `EGA-D11.50`, `EGA-D11.55`–`.58`, document `EGA-I30`, bark `EGA-B9.12`. The §9.5 row 5. Nothing else.

### 14.2 D-S1 swap note
Nodes tagged `[D-S1]`: document `EGA-I32` and its inspect `EGA-I33`, `EGA-D13.12`, `EGA-D13.70`–`.80`, barks `EGA-B9.8`–`.9`. Nothing else.

## 15. Internal review log

| Finding | Revision |
|---|---|
| Bible §6.1 brief, beat by beat. | `S00` auto-start with `EGA_FROST`; `S01` warming houses, Cooking hook or Hennet's kitchen, an Ember-Fused flare as containment; `S02` three pressure stages with Veska's crew, scavengers and beetles; `S03` terraces / ward / forges with Smithing wedges or a two-cycle hold; `S04` collars with valve-house numbers and Deepbrand marks, the junction book with its three bible phrases; `S05` far doors sealed from the other side; `S06` the Draw Sentinel at the splice junction, waking at the warming house with shut collars kept; `S07` the thaw lines; `S08` the board balances, guilds / council, §9.3 attendance, `EH_STANDING`, the Speaker's letter. |
| Boss brief §10.1. | Arena (four collars, central draw valve, two niches, one vent); P1 Draw shield from open collars, shut by channel; P2 Seal on a vent-told cycle; P3 Vent in told lines; 0 HP seize and cool; failure as written; never speaks, named or yields evidence; book found before the fight. |
| CDR-1. | Every enemy to 0 HP; no SX; the withdrawal is past; the Sentinel never retreats or re-forms. |
| CDR-2. | Ranged viable in every fight; required in none; no boss position it cannot reach (collars by hand, closing niches, Vent Cone, Spill, full-length lines). |
| CDR-4. | Telegraphs in seconds; displacement ≥1.5 s; standard systems (timed hazards, prop-driven buff, phase gate, door props, channels). No meter, stealth or new UI. Frost is presentation only. |
| CDR-6. | Every step, the boss and every reward solo; per-player choices and props; partner credit only from their own active step; co-op collar-set mismatch logged for Sol as presentation. |
| Revelation Ledger. | No R-id owned; R18 and R19 seeded only; R15 and R16 untouched; R09–R12 not re-told; no Titan identification in any paper; no precursor name; no roster; nobody counted. |
| Quest items. | One (`EGA_junction_book`); Emberholt 5 of 5. |
| Promised reads. | Act I: `ECW_SHORTFALL_SEEN` ("Read it again"), `EEH_TAVI_STRUCK`, `EGH_KEEP_SEEN`. Act II: `EAC_PLATE_READ`, `EAC_SLATE_READ`, `EAC_ACCOUNT_PROMISED`, `ESS_RAT_PAID`, `ESS_LETTER_READ`. All used with the wording the earlier packages promised. |

---
---

# E. Emberholt epilogue states

This section is the single reference for how EH-M6's outcomes change Emberholt after `EH_STANDING`. Everything here is **per-player presentation** (bible §9): props, NPC positions and barks keyed on the player's own flags. Barks are in the dialogue file (`EGA-B9`, `EGA-B10`). No epilogue state removes access to any site, service or side quest. The High Kindling has not happened; it belongs to CV-M4.

## E.1 Cinderwall [EP02]

| Element | **ward** | **terraces** | **forges** |
|---|---|---|---|
| Hoods | Warm; two lanes' hoods new brass, still bright | Warm | Warm |
| Cooling House | A Cooling House again. On the board: *Hoods: two to replace. Ward pays.* | On the board, in chalk someone keeps rubbing out and someone keeps writing back: *TERRACES LIT. WARD DARK.* | Two forge hands eat at the long table most evenings. |
| Hennet | "We were too warm. I'd do it again." | "We watched them glow. Don't do that to us twice." | "One of the forge lads can nearly cook now." |
| All | The hood tell reads **amber** (Working) and stays there. Veska drinks at the trough at shift change. Yorven's box pays for coal for the old. The frost does not come back this season (presentation; no weather). |

`EH_COLD_WARD` `[ALLOCATION]` keeps its Act I barks unchanged.

## E.2 The Gate Valve House [EP26]

| Element | **guilds** | **council** |
|---|---|---|
| The board | Balanced every hour (EME10 balanced state). Beside it, a guild copy-board where crew chiefs chalk every collar fitted that week with a warden's countersign. | Balanced every hour. At noon a Council clerk reads the board aloud to whoever is in the hall; the gate street has started coming to hear it. |
| Odile | Counts aloud; at the last column: "Balanced." (every hour; she never stops saying it) | Same; at noon she hands the clerk the chalk and lets him read. |
| The valve book | Each collar number has a line through *repair* and *shut* written beside it in Odile's hand. | Same, with the Council's seal mark in the margin. |
| Aubin Harl | At his bench: "I sleep now." | Same. |

## E.3 The Undercroft and the splice junction [EP15]

All outcomes. The Undercroft stays walkable to the splice junction. The three splices stand shut with their clamps cut off (by the wardens, the next day) and stacked in the bleed house; the bleed house slate has a new line in the chalk of whichever relief was used. The **Sentinel** stands where it locked, cold and dark, a wardens' chalk mark on its chest: *DON'T* (inert prop; never re-forms; nothing drops). The **far doors** stay barred from the far side, with a warden's chain added on this side and Deepbrand's mark scraped off. The fitter's cabin is empty. EH-M6's pins are released at completion, so no pin remains: heat zones show the default state in the Zones §6.1 table (the EI-HT-01 schedule instead, where it is built).

## E.4 The Ash Terraces [EP23] (by `EH_HEAT_MAIN` and `EH_SPEAKER` `[D-S1]`)

| Element | Variants |
|---|---|
| The braziers | **terraces:** two brazier rows cracked by the night's heat, roped off, with a warden's tag. Otherwise unchanged. |
| Rehearsals | Continue every dusk toward the High Kindling (CV-M4). `challenged`: the crowd breathes raggedly on its own count (Act II `ESS-B9`). `exposed`: as written, four beats. |
| The Speaker | On his balcony at rehearsals. If the player is in the crowd, he lifts his hand to them as to anyone (`EGA-B9.8`, `[D-S1]`). |

## E.5 The Emberforges [EP25] (by `EH_HEAT_MAIN`, `EH_ACCOUNT`, `EH_GUILDS`)

| Element | Variants |
|---|---|
| The great hearths | **forges:** a stack of cracked crucibles by the Basalt Forge Guild door, chalked *the frost night*. Otherwise unchanged. |
| Durnan Volkryst | **guilds:** "Every collar with a countersign now. Slows us. Good." **council:** "The Council has our numbers. We'd rather have had them first." With `EH_GUILDS = reformed`: "My new rules held a seat for the wardens. First time a rule of mine's been used for anything but shouting." With `restored`: "We billed the ward for the forge night. I've torn the bill up. Don't tell my masters." |
| Guild board | **guilds:** the account's collar numbers in chalk, struck through. |

## E.6 The old lower forge [EP11] and the Marshal's office

`EH_HOLLOW_TRUTH = told`: the plaque's chalk *NOT A COLLAPSE* has been written over again by someone else, and under it in a warden's hand: *The board balances now.* (The junction book says the lower forge undercourse was not drawn, so nothing claims heat was taken here.) `kept`: the plaque is clean; Kaevren's second ledger now has a line with the valve-house mark beside it (inspect at his office). Nothing in either names anyone or counts anyone.

## E.7 Maeryn's shop [EP03] `[D-E2]` on one line

All outcomes: Maeryn's fitting bark is unchanged (`EAC-B9.1`). `freed`: Dahrin asks once whether the board said anything about the deep works ("Shut. Good. Shut is a word I like."). `aided`: Asera, in the third chair, opens her eyes when the player comes in: "You wrote it. He'll know." (`EGA-B9.12`). Nothing locates anyone.

## E.8 Speaker's Hall [EP28] `[D-S1]`

The Speaker's letter stays in the player's journal (document view). The Speaker's Hall service yard and the Rat's duct are unchanged. The Council (with `council`) has the board read at noon; the Speaker is not seen to attend it. Nothing here shows what he knows.

## E.9 The warden's round (post-story activity) [NEW]

An optional, repeatable activity that uses Emberholt's readable system after the story, with no new mechanics.

| Element | Spec |
|---|---|
| Offer | Veska at the Undercroft stair head, once per presentation day after `EH_STANDING`: "Walk the line with me? Same as the first night. Less shouting." (`EGA-D15`) |
| What the player does | Walk the Undercroft line from the stair niche to the bleed house with Veska; read three tells she names (inspect windows); bleed one junction that is Working in the Zones §6.1 default table, or on the EI-HT-01 schedule where it is built (the Act I bleed channel); touch water at each niche. Occasionally a duct has Cinder Rats (world pocket EW-01) or the vent gallery has Slag Beetles (EW-02 at U3) (Enemies §11; ordinary encounters to 0 HP, solo). |
| Variants | `EH_HEAT_MAIN`: the bleed house's slate gets a new line each round; Veska comments on the night's relief once. |
| Rewards | Ordinary combat and skill XP from actions; a small warden's wage from Yorven's box ([GD]). No unique item. Nothing evidentiary. |
| Cut freely | If the Director prefers no repeatable activity, the round is removed and nothing else changes. |

## E.10 Emberholt master commissions

`EH_STANDING` is Emberholt's regional standing (bible §9.1, ED-11: Smithing master commissions after `EH_STANDING`). This package authors only **who offers what, where, and the offer line** (dialogue file `EGA-D14`). The offer opens a commission; it grants nothing. Skill thresholds, materials, stats and steps belong to the economy pass (ED-11: legacy materials such as ember shards, ashsteel and conduction plates are not catalog items). Names are functional placeholders [NEW].

| Commission (functional name) | Giver | Where | Skill line | Variant |
|---|---|---|---|---|
| **Basalt Forge master piece** | Durnan Volkryst | The Emberforges | Smithing (apex) | `EH_GUILDS`: reformed: "Forge it to the new rules." restored: "Forge it the old way. I'll know." unset: neutral. |
| **Warden's valve key and bleed set** | Veska Dunmor, at Durnan's anvil | Cinderwall yard forge / the Emberforges | Smithing | `EH_HEAT_MAIN = ward`: "Make the key heavy. We'll be turning a lot of hoods." |
| **Frost-warden's lined coat** | Brisa Teglan | The Cinderweave Quarter | Leatherworking (heat-and-cold lining) | *Soot and Hide* Completed: "You know hide. Now learn cold." |
| **Border-Warden's crossbow** | Ryl Danner | Embergate yards | Fletching / Ranged (crate-wood stock, smith-yard fittings) | *Wardens' Quarrels* Completed: "Feathers first. Then we'll talk about the stock." |

Every player who completes EH-M6 receives all four offers; none depends on `EH_ACCOUNT`.

## E.11 What every ending shares

The draw is shut and the board balances. The three splices are cut out of the main, their numbers struck through in Odile's book. The junction book is in hands that will keep it. The far doors are barred from both sides now. Cinderwall is warm, and somebody paid for the night: the ward, the terraces' good name, or the forges. The word *Remnant* is in Cinderwall's mouth, plainly meant. Nobody in Emberholt says what the proving rings were holding for, what "the old circle" keeps, who wrote in the margin, or what is past the far doors. The High Kindling is still coming.

---

# Act III review log (cross-package)

| Check | Result |
|---|---|
| Brief compliance (bible §6.1 EH-M6) | Every beat implemented in order (§15). Length 60–75 minutes. Code `EGA` confirmed. |
| Contract (§6.2 row) | Anchor (fire wardens; guilds; Council), world-truth rows (H22, H25, H18 record), revelation role (EH-M1 seed paid; stop and existence into the civic record), recurring evidence (junction book + valve-house book + collars), state compliance, combat compliance: all on the card (§4). |
| Combat (CDR-1/2/4/6) | Everything to 0 HP; no SX; ranged first-class and never required; telegraphs in seconds, displacement ≥1.5 s; standard mechanics; solo-tuned boss with no co-op-only mechanic. |
| ED-2, ED-5, ED-8, ED-12 | The fused worker is a containment; the Speaker only writes; the boss is a construct and no named character is fought; Volkhari at the board decide what is said. |
| FT-04, FT-05, D-C03, D-C06 | Perfect Flame as a heading only; no Titan staged, named or identified; no precursor name; no roster; the margin hand never named; no Volkhari counted or located. |
| Revelation Ledger | Owns no R-id; seeds R18 and R19 only; R15 and R16 untouched; no reveal repeated. |
| Reserved decisions | `[D-E2]` at one board beat and two barks; `[D-S1]` on the letter, one Council line and two barks; `[ALLOCATION]` on one tag, two attendance lines and one bark; swap notes §14.1–§14.2. |
| Region flags | Reads `EH_TELLS`, `EH_COLD_WARD`, `EH_CURRICULUM`, `EH_HOLLOW_TRUTH`, `EH_THALAN`, `EH_SPEAKER`, `EH_UNBURNT`, `EH_GUILDS`, `EH_COMMONS`, `TAS_ACCOUNT`; sets `EH_HEAT_MAIN`, `EH_ACCOUNT`, `EH_STANDING`. One writer each. |
| Quest items | `EGA_junction_book` only; Emberholt 5 of 5. |
| Map | Bible POIs only (EP02, EP15, EP26, EP01, EP28, EP25, EP23, EP11, EP03) and [NEW] sub-sites inside them; relative placement; MAP VERIFICATION REQUIRED on every place table and both sightlines; nothing past the far doors or beyond the city is placed. |
| Terminology | No release wording; "craft", never "magic"; no "ghost", "undead", "curse"; "Remnant" enters public speech at the board and not before; no "invaders", no compass direction for any enemy. |
| Runtime | No new needs beyond EI-PR-01 in its bible fallback form. |
| Size | One quest and its epilogue; Acts I–II conventions referenced, not restated. |
| Independent review, 2026-11-14 | Walkthrough of all four `EH_THALAN` × `EH_SPEAKER` combinations and both custody choices: every step reachable, every read flag has one earlier writer (Act I/II and bible §9.1; side-quest and Thornfell reads optional), three states only. **Fixed:** the bleed house was Surging during EGA-E3 and the hook (now drops to Working when the wheel turns; U9 swaps on hold); Stage A added to Surging zones; the vent-count position contradiction; Veska's crew "stays in U8" contradicted `S05`–`S06`; `S02` predicate made order-safe; the Sentinel's 65% floor now has an objective counter and a Veska call and is stated as an ordinary phase gate, and Lock-step has a solo recovery window (CDR-6); Asera's chalk line counted the held ("one", D-C06) and now names and counts nobody; Yorven's "Remnant" line no longer cites the lower-forge night (his limit; `kept` branch; D-C03) and Odile's chalk says "below Cinderwall"; the `told` plaque line no longer claims heat was drawn from the lower forge (contradicted the book); §9.2 reader cells corrected. **Checked, unchanged:** Ralenne Kharveil sits on the Council (Factions §5); R18/R19 seeds only, no Titan word in any paper, no precursor name or roster; ED-8; no release wording. |
| Batch 4 encounter alignment review, 2026-11-15 | Applied Enemies file PE-8 (EGA-E2 beetle burst 1.5 s; EGA-E3 inherits). `EGA_FROST` is now set by the quest's activation: the Cinderwall entry auto-starts EH-M6 at `S00_frost` and accepting `EGA-D1` completes S00, so no flag is set while the quest is Inactive (Integration EQ-04; EDI-3 still lets the Director prefer an offer). Post-story heat (§E.3, §E.9, §12) uses the Zones §6.1 default table, since completion releases every pin (Zones EZ-6, Integration EQ-05); the warden's round's beetles and rats are world pockets EW-01 and EW-02. No id, step or line changed. |
