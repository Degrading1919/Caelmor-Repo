# Mire Main Questline, Act I: The Name at Sorrowmere, The Banners That Refuse to Fall

**Status:** Authored production content for Creative Director milestone review (2026-11-08). This package implements Mire main milestones MR-M1 and MR-M2 (bible §6, §6.1), which carry Act I from the player's arrival at Sorrowmere to the Act I turn. It follows the Thornfell act-package format (`Caelmor_Thornfell_Main_Act_I.md`), itself the Lowmark format. Everything marked **[NEW]** is authored and not canon until the Director promotes it (MD-16: promote nothing from this package). Everything marked **[PROPOSAL — DIRECTOR]** rests on an open bible §3 decision (MD-1 to MD-16). **[CANON]** items come from the Mire dossier, the Mire character anchors and the Part 4 ledger. **[APPROVED — id]** items rest on an architecture ruling. No schema, production JSON or C# is created here. The Mire is an internal production milestone of the complete game (CDR-3); nothing here describes release scope. Combat follows the Director rulings of 2026-11-03 (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`): every enemy is defeated at 0 HP (CDR-1), every fight accepts melee or ranged and none requires ranged (CDR-2), and standard RPG systems are preferred to bespoke simulation (CDR-4). The Mire registers no scripted-survival exception (rulings §4; bible §3 "SX proposal: none").

**Controlling document:** `04_CONTENT_PRODUCTION/Quests/Caelmor_Mire_Narrative_Production_Bible.md`. Its §6 table and §6.1 briefs for MR-M1 and MR-M2 are binding and are implemented as written. Where this package adds detail, it is marked [NEW] and stays inside the bible's cast (§5), places (§4.2), flags (§9.1), encounter families (§10) and conventions (§11).

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Mire_Main_Act_I_Dialogue.md`. It holds cast notes, every dialogue node referenced here (`MNS-`, `MBR-` prefixes), barks, inspect texts and the full text of every document (the Names Below entry, the care leaf, the Hayle book page, the two written outcomes, the three unit day-books).

**Decision tags used in this package.** `[MD-1]` / `[CAUSEWAY]`: Oswin Garvey's causeway decision (bible §3.1 swap layer). `[MD-2]`: the MR-M1 fosterage case. `[MD-3]`: the night walk back in MR-M1 is part of the reason the bible moves Rowan's crossing to first light; if MD-3 changes, nothing here changes, but the beat is tagged so the Director can see what it carries. `[MD-5]`: adopted Part 3 practices (the Names Below register, Reedsward as a work rota, the Silt hearing). `[MD-7]`: Hollowfoot. Act I has **no Hollowfoot encounter**; the only Hollowfoot person in Act I is a settled, non-combatant man at Fenward (MR-M1, optional scene), valid under either MD-7 ruling. `[MD-4]` does not apply to Act I.

---

## Act I header

### What Act I does

The player arrives in the Mire as a stranger and leaves Act I knowing three things: that the Mire settles names by testimony that holds, that the ground can be read, and that the field's banners are rising because people stood them up. Act I's job is to make the player competent in the Mire's readable system (ground and water) and in its civic tool (two holds, one name), and then to turn that competence on the Field of Fallen Standards, where the evidence stops being about one family and starts being about the last day of the war.

| Quest | The player learns | By doing |
|---|---|---|
| MR-M1 **The Name at Sorrowmere** | Channel stakes (pale, ochre, black). Lantern moss (a lit line is a tended line). The two-holds rule. That the Mire writes "not found" as a record. That a woman everyone knows as Nell is very probably Linnet Hayle, and that the bones beside the causeway are very probably her mother's. That someone has been standing the field's banners up. | Sitting the stranger's seat, walking a causeway that changes under them, gathering four holds from four keepers, bringing a care cart home at night by the lit posts, and setting the holds side by side. |
| MR-M2 **The Banners That Refuse to Fall** | Banner states (laid, leaning, risen). The Reedsward crews stood the standards up. A Banner Wraith is an impression tied to a standard, and retiring the standard ends it. Records belong to Memorykeepers; relics are something else. Three columns whose clerks did not even count days the same way stopped on one day. | Lifting, re-pinning and folding three risen standards under attack, levering up an officers' chest, carrying a clay shard past a grieving man, and bringing down the Banner That Sank Twice at dusk. |

**Act I turn (Arcs §3.2; bible §8.3 misunderstanding ladder):** the player moves from "the Mire is a graveyard" and "the risen banners are ghosts with messages" to "a community doing hard work on bad ground" and "impressions woken by standing the standards up". The last thing the player sees in Act I is Calwen closing his unsorted chest on a clay shard nobody owns, with three day-books on Ysolde's table that all stop on the same day.

### Dependencies on other regions

The Mire has **no quest prerequisite** (bible §6, §11.12). Lowmark and Thornfell completion are never required. Their state is read only for optional variant lines.

| State read | Read by | Effect |
|---|---|---|
| `CN_COMPLETE` (Lowmark *The Candle Rule*) | MR-M1 `S00_offer` | Optional option: the player asks Ysolde to search the register for Ewan Holt. **Not found**; she writes that the player asked (`MNS_HOOK_ASKED`). Never a gate. Says nothing about what happened to Ewan (Lowmark keeps that deliberately unselected). |
| `thornfell.main.03_echo_of_shatterfall` Completed | MR-M1 `S00_offer` | Optional option: a name from the Rim Cairns. **Not found**; written. Never a gate. |

No other region's flag is read in Act I. `FC_SEAL_NOTED` is not read (MD-15). `TH_STANDING` is read only in Act III.

### Region flags (bible §9.1 only)

| Flag | Act I role |
|---|---|
| `MR_CHANNELS` | **Set** by MR-M1 (`S02_causeway`, at the end of the stake lesson). Turns on the stake inspect text everywhere. Read by MR-M3. |
| `MR_NAME_RECORD` = amended / qualified | **Set** by the MR-M1 choice. Read by MR-M2 (Dunstan's lines), MR-M5 (the names roll and circle placement), *Weight of the Soil*. |
| `MR_CAUSEWAY` = reset | **Set** by MR-M2 on completion (default is unset, read as "raised"). Read by causeway props and *Lifting Day*. `[CAUSEWAY]` |
| `MR_BANNERS` = retired / restored | **Set** by the MR-M2 choice. Read by MR-M5 (Corra's banner, extra wave), Griefwatch props. |

Act I invents no other `MR_` flag. Quest-local flags use `MNS_` and `MBR_`. Those read by later packages are listed in each quest's flags table under "Read by (later packages)".

### Quest-item budget (bible §9.4: four for the whole Mire)

| Item | Quest | Fate |
|---|---|---|
| `MNS_name_tape` (a child's stitched name-tape, *Linnet*) | MR-M1 | Lifted from Mara's marker in `S03`, shown at the second reading in `S05`. Removed on completion: with `amended`, Nell keeps it; with `qualified`, Mara lays it back with the remains under her stone. Not droppable, not sellable while carried. |
| `MBR_unit_logs` (three regimental day-books in oilcloth, one bundle) | MR-M2 | Taken from the officers' chest in `S04`. Kept by the player and shown to Ysolde (she keeps a copy); read again at the MR-M3 offer; in MR-M4 the vestry log's inspect matches their weather run whether or not the books are in the pack. Not droppable, not sellable. |

**Act I total: 2.** Everything else in Act I is a carry-state object (the care leaf is read at the station and carried as knowledge; the fowl and the broth crock; the shard; the folded standards), an inspectable world object (the register, the Hayle book, the stakes, the standards, the chest), or knowledge carried in flags. Nothing becomes an inventory item that the item pass has not defined.

### Structure check against the bible §6 core verbs

| Quest | Primary verb | Distinct from |
|---|---|---|
| MR-M1 | **search and match records**; walk a shifting route; sit as witness | An investigation across two settlements and a causeway, with one escort at night. Combat is small (beetles, one Wraith). The set piece is a walk, not a fight. |
| MR-M2 | **recover and retire** under attack; read banner states; repair route | Work under pressure on one narrow road. Combat is the frame for the work (Wraiths, Reedlurkers, the Risen Colour). The investigation is in objects (a chest, a shard) and in one confession. |

No two quests share a set piece. Combat changes family across the act: Griefbit beetles and a single Banner Wraith (MR-M1) → Banner Wraiths in number, Reedlurkers and the Risen Colour (MR-M2). The readable system changes job: in MR-M1 the stakes and the lantern moss are **taught** and used to move people; in MR-M2 the player reads a new layer (banner states) and works on the causeway the stakes taught them to cross.

### Unlocks across Act I (bible §7)

| After | Unlocks |
|---|---|
| MR-M1 | *The Stranger's Seat* (MSS), *The Broken Lantern Light* (MLL), *Reed Shafts* (MRS), *A Table for the Wet* (MFT), *The Ferry Harness* (MFH), *The Singing Trench* (MSG), *Nine Stakes* (MNK); MR-M2 |
| MR-M2 | *A Banner With No Side* (MBS), *Weight of the Soil* (MWS), *The Mud That Remembers* (MMR), *The Hushed Granary Key* (MHG), *The Bell Roster* (MBO), *The Rust Hart* (MRH); *Lifting Day* (MLD, also needs MLW); MR-M3 |

### Act I clocks and conventions (bible §9.2, §9.4, §11.1)

| Convention | Act I use |
|---|---|
| **Presentation hour / keep watch** (Lowmark) | Per-player hour (morning, noon, dusk, night), advanced by quest events and by the keep-watch interaction at marked benches. Never world time. MR-M1 uses it at the first stake (wait for Slack), at Hob's hide (wait for Hob, crew alternative), at the care station (dusk departure) and at the Ferrow house (wait for morning). MR-M2 uses it at the causeway works (crew pins) and at the sanctuary (wait for dusk). |
| **Channel states** (bible §9.2, N-1) | Each crossing has three states (Running, Slack, Sour) shown by its stake. **Act I pins every state it needs** (the N-1 fallback), so nothing here waits on the per-crossing schedule being built. A state swaps walkable shallows and stake water-line props. |
| **Lantern moss** | Taught in MR-M1 `S04` (a lit line is tended; a dark post has a dry foot). Used for night travel from then on. Taught properly in MR-M4. |
| **Banner states** | Taught in MR-M2 `S01`. A risen standard's Wraiths walk at dusk; lifting a risen standard wakes them at any hour; a folded or retired standard ends the condition. |
| **Earth-memory re-forming** (Lowmark drift-site model) | Wraiths are defeated at 0 HP and re-form at their standard while it stays risen. The condition, never their health, decides. |
| **Channelled segments with persistence** | Lifting a pole (MR-M2), levering the chest (MR-M2), heaving a sunk wheel (MR-M1). Completed segments are kept. |
| **Interact sequence with harmless reset** | Folding a banner by its seams (MR-M2). A wrong fold unfolds. |
| **Per-player props with fallback** | Stake water lines, standard states, the causeway's roadside standards, the register page. Co-op fallback: the host's state. |
| **Agility triggers** | Optional shortcuts only (a walkway gap at Marshfall; a ditch jump on the causeway), each with a walkable fallback. |

---
---

# Part A: MR-M1 The Name at Sorrowmere (`MNS`)

## A1. The quest in one paragraph

The player walks onto **Sorrowmere**'s raised ways on a morning nobody in the settlement wanted. **Ysolde Haverel**, the Memorykeeper who keeps the **Names Below register**, stops them: a register amendment needs someone from outside the household lines to sit the **stranger's seat**, and the player is "the only one here who isn't somebody's cousin". In the register room the case is read aloud. **Mara Fenholt**'s ground beside the **Standards Causeway** has released remains with a child's stitched name-tape: *Linnet*. **Dunstan Hayle** of Marshfall lost his mother and his small sister Linnet on the Standards road in the war's last year, and he has come to claim the bones as his sister's and have her name cut. **Nell Ferrow**, who came into **Edris Hollowmere**'s care off that road as a small child, sits at the back of the room holding her foster mother's hand, and **Agna Ferrow** wants the register to say Nell is a Ferrow and nothing else. Ysolde teaches the rule: two holds, one name. The player walks the causeway with Edris's crew, learns to read the **channel stakes**, waits for Slack, passes a Reedsward crew standing fallen banners up at the roadside, and lifts the name-tape from Mara's marker; Mara says the arm it was sewn into was a grown woman's. At Edris's old care station on the Marshfall side they defeat the Griefbit beetles swarming a sick traveller's cart, open Edris's tin box, read the care leaf (*a reed charm sewn in the hem, three knots*) and hear Edris tell what she did that night. In Marshfall the Hayle book shows the same three knots drawn beside Linnet's name. At dusk the player leads the care cart home across the causeway by the **lantern moss**, the stakes turning Sour behind them, and a **Banner Wraith** walks out of a standard the crew stood up that morning. At the Ferrow house, Nell hums a lullaby nobody taught her, and Dunstan, outside the door, finishes the line. Nobody says anything. In the morning the player sets the holds side by side. Ysolde's reading: Nell is very probably Linnet Hayle, and the bones are very probably her mother's. Nell asks the witness what they would write, and the register is **amended** or **qualified**. Ysolde blots the page and offers the player a seat at the table that night.

**What the player should remember:** the lullaby, and Agna saying "I did the raising. Write that." **What the player should want next:** why banners stood up at the roadside are moving with no wind.

## A2. Selection record

| Candidate | Verdict |
|---|---|
| **A. A courtroom: claimants argue, the player picks a winner.** | Rejected. The Mire's hearings are not contests (bible §5.3, rule 7; MD-5 Silt hearing has no appeal rules), and a winner/loser frame would make one family wrong. |
| **B. The player identifies the remains by a phenomenon (the Wraith, the lullaby).** | Rejected. Evidence rule: phenomena never identify a person (bible §11.3). Both the Wraith and the lullaby are kept, and both are explicitly refused as holds at the second reading. |
| **C. Reading → causeway walk with stakes → holds from four keepers → night walk back by lantern moss → strange moment → second reading with the holds set side by side → how the register writes her** (selected; the bible brief). | **Selected.** Every hold is earned by going to the person or the object that keeps it. The route teaches the readable system on the way to the evidence, and the night walk makes the player carry somebody before the reading decides anything. |

## A3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Sorrowmere: elevated walkways, flood-resistant longhouses, memorial gardens, banners lining streets to show community mood | Dossier §VII.1 | [CANON] |
| Marshfall: where marsh meets forest; hunters, gatherers, peat-cutters; fog rolls in | Dossier §VII.2 | [CANON] |
| Edris Hollowmere: survived by tending wounded; chose to remain; refuses to rush anything that involves the dead; "the Mire knows when it's being respected" | Mire anchors §I; Part 4 ledger (owns her own care account; cannot turn a manifestation into a witness) | [CANON] |
| Mara Fenholt: locates remains when the ground releases them; never digs too deep; marks with simple stones, never names | Mire anchors §II; Part 4 ledger | [CANON] |
| Lysa Thornettle: herbalist and peat healer at the Fenward huts; healing is making space | Mire anchors §V | [CANON] |
| Memorykeepers: civilian recorders; resist embellishment; not magical | Dossier §III, §VIII, §XVIII | [CANON] |
| Griefbit beetles: drawn to emotional disturbance; swarm when fear rises | Dossier §IX | [CANON] family |
| Banner Wraiths: impressions tied to banners; drawn to strong emotion; dissipate if the banner is honoured or retired | Dossier §IX; C15 | [CANON] |
| Lantern moss: glows faintly when damp; lights walkways at night | Dossier §X | [CANON] |
| Rootrest soil feels "lighter"; people overwhelmed by grief go there | Dossier §VII.4 | [CANON] |
| The Names Below register, the stranger's seat, two holds, the Reedsward rota | Bible §1.1, §5.2, MD-5 | [PROPOSAL — DIRECTOR] MD-5; [NEW] detail |
| The Standards Causeway and its relaying | Bible §2.1, §2.3, MD-1 | [PROPOSAL — DIRECTOR] MD-1 `[CAUSEWAY]` |
| Nell Ferrow / Linnet Hayle; Dunstan, Agna; the Hayle household | Bible §5.2, MD-2 | [PROPOSAL — DIRECTOR] MD-2 |
| Channel stakes (pale, ochre, black) | Bible §1.1 | [NEW] |
| Aldith Hayle (the mother's name in the Hayle book); the sleeve-tape custom; "a house book stays under its own roof"; Edris's old care station | This package | [NEW] |

## A4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Name at Sorrowmere** |
| Suggested content id | `mire.main.01_name_at_sorrowmere` |
| Arc position | Act I entry (Arcs §3.2, MR-M1: "teach care and testimony as civic structure") |
| Prerequisite | None (travel only). Tuned for Competent identity (MD-10). |
| Offer | Auto-offered on first entering the Sorrowmere raised-way volume from any route (`MNS-D1`). MAP VERIFICATION REQUIRED for the approach. |
| Solo / co-op | Solo-clearable. Co-op partners share the beetles and the Wraith; holds, channel states, the cart escort and the register choice are per player. |
| Target length | 40–55 minutes first time |
| Combat share | ~10% |
| Dialogue share | ~30% |
| Travel, reading the route, gathering, escort, choice | ~60% |
| Skills touched | Melee or Ranged (either; neither required); Hunting ~[GD: low] and Cooking ~[GD: low] (optional; Hob's string is the alternative) |
| Choices | How the register writes Nell and the remains (`MR_NAME_RECORD`); whether to fight or wait out the Wraith (flavour flag only); whether to visit Fenward (optional scene) |
| Unlocks | `MR_CHANNELS`; `MR_NAME_RECORD`; Sorrowmere hub (register room, raised ways, causeway head, respawn point); the Standards Causeway as a route; seven side quests (Act I header); MR-M2 |
| **Anchor** (contract) | The Memorykeepers (the Names Below register; Ysolde); Sorrowmere and Marshfall households (Ferrow, Hayle); Edris's care account |
| **World-truth row** (contract) | H23 (recovery after the war: fosterage, uncertain names) |
| **Revelation role** (contract) | Self-contained case. **Plants** R16 (the stranger's seat, never explained). **Plants** the MR-M2 cause (`[CAUSEWAY]`: a crew standing standards up; a leaning standard that is risen by night). Owns nothing. |
| **Recurring evidence** (contract) | Four independent custodians: the name-tape (Mara's marker), the care leaf (Edris's station), the Hayle book (Marshfall), Edris's testimony; Nell's reed charm as an optional fifth. The register entry written in `S05` recurs in the MR-M5 names roll (two-hold rule). |
| **State compliance** (contract) | Inactive / Active / Completed. No step can fail; every channel state can be waited out; the hold board refuses wrong holds without penalty. Choice recorded in `MR_NAME_RECORD`. Resume at the persisted step with a hook at the register room (Ysolde) or, after `S02`, at the care station (Edris). The register search hook is re-offered at the register after completion. |
| **Combat compliance** (contract) | Griefbit beetles and one Banner Wraith, each defeated at 0 HP. The Wraith re-forms at its standard while the standard stays risen (place condition, never health). Melee or ranged; ranged never required. No SX. No defeated enemy gives testimony. |

## A5. The places

### A5.1 Sorrowmere [MP01, CANON settlement; NEW detail]

Raised walkways on piles over slack water, flood-resistant longhouses along them, memorial gardens on built-up beds, and banners on poles at every junction showing the settlement's mood (MME01). **MAP VERIFICATION REQUIRED** for every placement below; relative order only: the raised way → the register room → the Ferrow house further along the same way; the causeway head at the settlement's edge facing the Field.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **S1. The raised way** | The offer (`S00_offer`). | Planks worn pale down the middle. A Bannerbearer changing a junction banner from grey to ochre ("a way is closed": the ferry way). Lantern-moss posts at every tenth pile, dark in daylight. Children playing the depth-band jumping game on a painted jetty post (MME10). |
| **S2. The register room** | The two readings (`S01`, `S05`). | A longhouse room with one long table. On the table, on a slanted reading board, the **Names Below register**: a tall book in a reed-board cover, its pages edged in soil from hands. On the wall, **index boards**: reed strips pegged in rows, one strip per name, pegs of three colours (found, held, not found). A bowl of dry soil on the table (MME02). On the visitor's side of the table, a low carved stool: **the stranger's seat**. Its seat is worn; its legs are newer than its top. Nobody comments on it. |
| **S3. The Ferrow house** | The strange moment (`S04b`). | The end house of a row, on taller piles than its neighbours. A wide door onto the way, a bench outside it. Inside: Agna's chair with a cushion on the seat and another on the floor for her bad leg; a hearth; a shelf with a child's clay cup on it, old. A small reed doll on a nail. |
| **S4. The causeway head** | Start of the walk (`S02`); end of the cart walk (`S04`). | Where the raised ways come down onto the first logs of the **Standards Causeway**. A watch bench under a lantern-moss post (keep watch). A post with painted depth marks for children (MME10). The causeway runs out into flat grey-green ground with standards leaning in it at the edges. |
| **S5. The reed-cutter's house** | Cart delivery (`S04`). | A plain longhouse near the causeway head. A woman waiting in the doorway with a lamp. |

### A5.2 The Standards Causeway [MP08, NEW] across the Field of Fallen Standards [MP07, CANON]

A wartime corduroy road of logs and fascines, laid straight across the Field to move troops and wounded, sunk after the war, and relaid this spring by Sorrowmere's Reedsward crews on the old line because it is the only ground that holds `[CAUSEWAY]`. Logs pinned with root-knee pegs; fresh pale ends among black old ones. Either side, ditches of standing water, then the flattened bog with standards leaning out of it at every angle. **MAP VERIFICATION REQUIRED:** relative order from the Sorrowmere end: causeway head → first crossing → the roadside works → Mara's marker → second crossing → the relaid section → the far end and Edris's old station on the Marshfall side.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **C1. The first crossing** | Stake lesson; wait for Slack (`S02`). | The causeway dips under a channel for twenty paces of shallows. A **channel stake** stands at the dip, painted from the top: a black cap, a pale band, an ochre band, then bare wood into the water. A crew bench beside it, with a lantern-moss post. In Running state the shallows are under and non-walkable; in Slack, the logs show through and are walkable. |
| **C2. The roadside works** `[CAUSEWAY]` | Required pass-by (`S02`). | A Reedsward crew relaying a section: logs on rollers, a stack of root-knee pins, mallets. Beside the road, three fallen standards **stood up in the peat** at the roadside, poles leaning, cloth hanging. A fourth is being lifted out from between two logs as the player passes. One of the three (the **crew's standard**, nearest the road) is the one that is risen by night (`S04`). |
| **C3. Mara's marker** | The name-tape hold (`S03`). | Off the causeway on a low peat ridge, reached by a plank. A ring of plain stones round a shallow, clean-edged hollow. A cloth over what the ground gave up. Mara's bone-basket, her short spade with a worn, rounded blade, a water jug. No name, no sign. |
| **C4. The second crossing** | Second stake (`S02`); turns Sour behind the cart (`S04`). | A shorter dip with its own stake. In Sour, the stake leans and the shallows are non-walkable. |
| **C5. The relaid section** | The lit-post fork (`S04`). | Where this spring's crews brought the road back onto firmer ground, the **old wartime line** carries straight on beside it for forty paces before it sinks. Both lines have posts. The new line's posts are wetted by the crews and glow at night; the old line's posts are dry and dark. |
| **C6. The far end** | Walk-out arrival; cart departure (`S02`, `S04`). | The causeway climbs onto a raised bank at the Marshfall side. A last stake. A path off to Edris's old station. |

### A5.3 Marshfall Edge [subzone]

**MAP VERIFICATION REQUIRED:** Edris's old station sits where the causeway meets the Marshfall side; Marshfall [MP02] is a short walk on; the Fowling Meres [MP26] are at Marshfall's edge; Rootrest and the Fenward huts lie on firmer ground beyond Marshfall (bible §4.2 route order).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **M1. Edris's old care station** [NEW site; not a numbered POI] | Beetles (`S02b`); Edris's account and the care leaf (`S03`); cart departure (`S04`). | A raised platform of grey timbers at the causeway's end, roof half gone, one wall still standing. A row of low pallet frames. A bench. Pegs where lanterns hung. In the standing wall, behind a loose board at knee height, a **tin box** with a rusted lid. The sick traveller's handcart at the platform's foot, a reed-cutter on it under a blanket. |
| **M2. Marshfall** [MP02, CANON] | The Hayle book (`S03`). | Stilt houses, peat yards, smoke sheds. Peat stacked in walls. The **Hayle house**: a peat-cutter's stilt house with a smoke shed under it. Inside, by the hearth, a shelf with one oilcloth-wrapped book on it. Peat-cutting spades in a row by the door, one short one, old, oiled and never used. An optional **agility** shortcut: a walkway gap across a peat cut (walkable fallback: round by the drying racks, 15 s). |
| **M3. Hob's hide** [at the Fowling Meres edge, MP26] | Optional skill hook: fowl for the broth (`S03`). | A reed hide on a mere's edge with a fowler's bench, a net on pegs, a string of fen fowl hanging (Hob's). Herons in the shallows. |

### A5.4 The Fenward huts [MP05, CANON anchor location] (optional)

Lysa's care huts on firmer ground beyond Marshfall. Low reed-and-root huts round a fire pit, drying herbs, a bench by each door. **MAP VERIFICATION REQUIRED.**

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **F1. Lysa's bench** | Optional scene and the charm hold (`S03`). | Nell sitting on the bench with a bowl, not eating. Lysa grinding something beside her. |
| **F2. The settled man** `[MD-7]` | Presentation only. | A quiet man by a hut door sorting reeds by length, again and again. He is one of Lysa's settled Hollowfoot. He is a non-combatant NPC and never targetable. Lysa: "He's settled. Don't be loud near him." (bark `MNS-B6.3`). He reappears in MR-M5 at the circle. |

## A6. Player-facing sequence

### Beat 0: The Raised Way (`S00_offer`)
**Objective:** *Speak to the Memorykeeper on the raised way.*
The player comes onto Sorrowmere's raised ways from any route. A Bannerbearer is changing a junction banner from grey to ochre (`MNS-B0.2`). **Ysolde Haverel** steps off a doorway into the player's path with a book under her arm (`MNS-D1`). She does not ask where they are from. She explains in four lines: a reading this morning; a name the register may have to change; an amendment needs someone from outside the household lines to sit the stranger's seat; "you're the only one here who isn't somebody's cousin".
- **Accept:** the quest becomes **Active**; Ysolde walks the player to the register room.
- **Not now:** the quest stays **Inactive**; Ysolde: "The room waits. It's good at it." She re-offers from the register room door (`MNS-D1.90`).
- **Ask about the seat:** "It's a stool. You sit on it." (beat) "Every register table in the Mire has one. Ask me why after. I won't know then, either." (R16 seed; nobody explains it, here or anywhere in the Mire.)
- **Optional option (`CN_COMPLETE`):** "Could the register hold a Lowmark name? Ewan Holt." **Optional option (`thornfell.main.03_echo_of_shatterfall` Completed):** "There's a name on the Rim Cairns at Shatterfall." For either, Ysolde runs a finger down the index boards by the door, says **"Not found."**, takes a blank reed strip, writes it, and pegs it in the not-found row: "Not found is a record too. Now somebody can find that you asked." (`MNS-D1.30`–`.36`; sets `MNS_HOOK_ASKED`). Nothing else is said about either name.
**Verbs:** arrive, talk.

### Beat 1: The Reading (`S01_reading`)
**Objective:** *Sit the stranger's seat at the reading.*
The register room (S2). Ysolde has the player sit the **stranger's seat** (interaction: sit). The room: **Agna Ferrow** in a chair at the back with her bad leg up on a cushion, **Nell Ferrow** beside her, holding her hand. **Dunstan Hayle** standing by the door in peat-cutter's boots he has tried to clean. **Edris Hollowmere** on a bench along the wall. **Lysa Thornettle** sitting with Agna (she came for Agna's leg; she stays for Nell).
The reading (`MNS-D2`) is a short set of spoken lines with player options between them. Ysolde touches the soil bowl (MME02), then reads the register entry aloud:

> *Received off the Standards road. Girl, small. Gave her name as Nell. Mother not found. Care: Hollowmere. Fostered: Ferrow.*

Dunstan reads from a reed strip: a Memorykeeper's copy of his household book's entry, carried in his shirt. *"Aldith Hayle, and Linnet, our girl, went out on the Standards road with the carts in the last wet. Not come home. Asked at the stations. Not found."* Then he says what he came for: "Mara's ground's given up our Linnet. Her tape's on it. I want her name cut." Agna: "Nell's a Ferrow. Write that and shut the book." Nell makes a joke (`MNS-D2.20`). Edris says she wrote a care leaf that night and it is in her old station's tin, on the Marshfall side.

Then Ysolde teaches the rule (`MNS-D2.30`–`.36`), which the whole quest uses:
- **Two holds, one name.** A register entry, a household book, an object or a living witness each count as one hold. A banner, a dream or a manifestation counts as none.
- **A copy isn't a hold. The book is.** Dunstan: "The book doesn't leave the house." Ysolde: "Then somebody goes to the house." (A Marshfall custom [NEW]: a house book stays under its own roof.)
- She names the holds she needs and who keeps them: Edris's account and her care leaf (at the station); the tape (on Mara's marker; Mara will not bring it, she does not leave a site open); the Hayle book (at Marshfall). "I keep the register. I can't walk the road. You can."

**Required:** hear both readings (Ysolde's entry and Dunstan's strip) and the rule. The scene ends with the room breaking up: Lysa takes Nell to the Fenward huts ("Rootrest ground's lighter. She can breathe there."); Dunstan goes home ahead of the player to open the book; Edris: "We go at the causeway head. The ferry way's sour. We'll take the logs." Those present at the reading call the player **witness** from here on (bible §5.3 rule 8).
**Verbs:** sit, listen, ask.

### Beat 2: The Causeway (`S02_causeway`)
**Objective:** *Walk the causeway to Edris's old station.*
At the causeway head (S4), Edris and two of her crew (role names: a digger and a carrier) are waiting with a handcart of empty sacks. The walk out is the lesson.
1. **The first crossing (C1): the stake lesson.** The quest pins C1 to **Running**. The crew's digger stops the player at the stake (`MNS-D3`) and teaches the three bands by pointing: "Water at the pale, she's running: boats go, the shallows are under. Down at the ochre, she's slack: we walk. Up over the black, or the stake's leaning: she's sour. Nobody crosses sour." The player **inspects the stake** (required; the inspect text names the band the water is at). **`MR_CHANNELS`** is set at the end of the lesson; from now on every stake in the Mire gives its state on inspect.
2. **Wait for Slack.** The crew sits on the bench. The player uses **Keep watch until the water turns** at the bench (one turn of the presentation hour; morning to noon). The water drops past the pale band to the ochre; the logs come up through the shallows. (If the player walks into the Running shallows, they are non-walkable: the player stops at the edge with a bark, `MNS-B2.2`: "That water won't have you. Sit down.") Crossing on Slack completes this part.
3. **The roadside works (C2): required pass-by** `[CAUSEWAY]`. A Reedsward crew is relaying logs. As the player passes, two of them lift a fallen standard out from between two logs and stand it upright in the roadside peat beside three others (`MNS-B2.4`: "Oswin's orders. Stand them up, so nobody drives over them."). Edris stops, says nothing, and walks on. Asked, she says only: "I asked him to wait for a hearing." (`MNS-D3.40`). Oswin Garvey is named, not met (bible §3.1).
   - **Optional inspect:** the standards at the roadside. Three are **leaning**, cloth hanging; the nearest (the crew's standard) has cloth that shifts once with no wind while the player looks at it. Sets `MNS_STANDARDS_SEEN` (MR-M2 reads it for one line). The inspect text says what is seen, not what it means.
4. **Mara's marker (C3).** On the route; the player can take the tape hold now or later (it is part of `S03`, any order).
5. **The second crossing (C4).** Pinned **Slack**. The digger has the player read it alone ("Go on. Tell me."); the player inspects the stake and crosses. No wait.
6. **The far end (C6).** Shouting from the old station ahead.
**Verbs:** walk, read, wait, cross.

### Beat 2b: The Old Station (`S02b_station`)
**Objective:** *Help at the care station.*
A sick reed-cutter from Sorrowmere lies on a handcart at the foot of Edris's old station platform, shaking with marsh fever, and **Griefbit beetles** are boiling up out of the platform's rotten timbers and swarming the cart (**MNS-E1**). The reed-cutter is terrified, and the more frightened he is, the more come (bible §10: more beetles when an NPC nearby is frightened). The first wave fights the player. When it is down, **Edris** goes to the cart, sits on its edge, puts a hand on the man's chest and talks to him low (`MNS-B3.4`). The second wave is visibly thinner and slower to come, and the player sees why. The step completes when every beetle is defeated. The cart and the reed-cutter cannot be harmed (beetles swarm the cart as a presentation; the man cries out; nothing is lost).
**Verbs:** fight, protect.

### Beat 3: The Holds (`S03_holds`)
**Objective:** *Gather the holds for the register.* (Sub-objectives in any order; the journal lists each with its keeper.)

| Sub-objective | Where | What the player does | Sets |
|---|---|---|---|
| **Edris's account** | The old station (M1) | Talk to Edris on the platform bench (`MNS-D4`). She tells **what she did** that night, not what it means: carts coming off the Standards road in the dark; a small girl walking alone between the carts, wet to the waist, no shoes; Edris asked her name and the child said "Nell"; asked for her mother and the child said "behind"; Edris walked back down the road with a lantern until the road went under the water; asked at the carts for two days; wrote the leaf; gave the child into Agna Ferrow's care when the station shut. "That's what I did. What it means is Ysolde's work." She also says, when asked about the tape: "Mothers on the road sewed the child's tape in their own sleeve. If you were parted, whoever found one could find the other." | `MNS_HOLD_EDRIS` |
| **The care leaf** | The old station (M1) | Edris shows where the loose board is. The player opens the **tin box** (a short channel: work a knife under the rusted lid, 2 segments). Inside, leaves tied with reed. Edris unties the one she wants and reads it with the player (document in the dialogue file). *"... smock, grey wool; under-shift; a reed charm sewn in the hem, three knots. No tape. Mother not found ..."* The leaf stays in Edris's keeping; she will bring the box to the second reading herself (she does not let her leaves travel without her). The player carries it as knowledge. | `MNS_HOLD_LEAF` |
| **The name-tape** | Mara's marker (C3) | Talk to **Mara Fenholt** (`MNS-D5`). She shows the tape on a flat stone under a cloth: a finger-wide strip of linen with *Linnet* stitched in brown thread. "It was sewn in her sleeve. Inside the cuff." Asked whose: "I mark with stones." Asked what she saw: "Seen: long bones. A grown woman's arm. Thought: I don't think about whose." She lets the player lift it for the reading ("Bring it back after. It goes where the reading says."). Quest item **`MNS_name_tape`**. Mara's account of what she saw is a hold in its own right (a living witness to what the ground gave up). | `MNS_HOLD_TAPE`; item |
| **The Hayle book** | The Hayle house, Marshfall (M2) | **Dunstan** has the book on the table, unwrapped, and food beside it he does not mention (`MNS-D6`). He reads the household page with the player (document in the dialogue file). Beside each child's name, in the same hand, a small drawn **reed charm, three knots**: beside *Dunstan* and beside *Linnet*. "That's the house mark. Mam sewed one in all our hems. Mine's in a drawer." He has not thought about it in years. He looks at it a long time. | `MNS_HOLD_BOOK` |
| **Something hot for the road** | Hob's hide (M3) and the Hayle hearth (M2), or Hob's string | Edris says the reed-cutter will not last a night walk without something hot in him (`MNS-B3.8`). **Option A (skill):** at Hob Merrit's hide, take a fen fowl from the mere (**Hunting ~[GD: low]**: a hunting interaction from the hide; any ranged weapon, or Hob's fowling net for players without one), then cook a broth at the Hayle hearth (**Cooking ~[GD: low]**, one interaction). Hob teaches one line of the craft and swears at a heron (`MNS-B5`). **Option B (crew alternative):** ask Hob for a bird off his string; he will bring one to the Hayle house when he comes in, and Dunstan's household will cook it. **Costs a turn:** keep watch at the Hayle house until dusk. The broth crock goes on the cart either way. | `MNS_BROTH` = self / hob |
| *Nell's reed charm* (optional) | Fenward huts (F1), or at the cart (`S04`), or at the Ferrow house (`S04b`) | Ask **Lysa** about Nell (`MNS-D7`). Lysa asks Nell, and Nell takes a small, worn reed charm with three knots out of her collar, on a cord. "I've always had it. Agna says I came in with it." She lets the player look, not take. Lysa: "That's a hold if Ysolde says it is. It's still hers." Visiting Fenward also gives the optional scene with Nell (jokes, fear, the settled man) and Lysa's line about making space. | `MNS_HOLD_CHARM`; `MNS_FENWARD_VISITED` |

The four required sub-objectives and the broth complete `S03`. The order is free. A player who goes to Marshfall before the station sees Dunstan waiting; a player who has not lifted the tape on the way out can go back to Mara's marker (the second crossing stays pinned Slack for this step).
**Verbs:** ask, open, read, lift, hunt or wait, cook.

### Beat 4: The Walk Back (`S04_walk_back`) `[MD-3]`
**Objective:** *Bring the cart home by the lit posts.*
At the old station at **dusk** (quest-pinned on step start), the cart is ready: the reed-cutter under his blanket with the broth crock wedged beside him, **Dunstan** in the shafts ("I'll pull. I want to."), **Lysa** and **Nell** come in from the Fenward side to walk back with them (Lysa: the reed-cutter needs a healer on the road; Nell: "I'm not sleeping at the huts. Agna'll think I've been stolen again." `MNS-D8`). Edris gives the player the station's **hand lantern** to lead with and stays behind to close up ("Somebody shuts a station. It's me."). If the player has not seen the charm, Lysa offers it here (`MNS-D7` variant).
The **escort**: the cart follows the player's lantern at walking pace and stops when the player stops (escort-follow; the cart cannot be harmed and cannot be lost). Night falls during the walk (presentation hour advances to **night** at C5).
1. **The stakes turn behind them.** As the cart passes each crossing, the stake behind it turns: the far end's shallows go **Sour** behind the cart (water rises over the black band; the stake leans), then the second crossing (C4) after the cart is across. The player sees the road close behind them and never ahead. Lysa: "That's the last slack tonight. We're on the right side of it." (`MNS-B8.3`). Nothing ever catches the cart: the turns are triggered by the cart passing, not by time.
2. **The lit posts (C5).** At the relaid section, the new line and the old wartime line run side by side. The new line's posts glow with wet lantern moss; the old line's are dark. Lysa teaches it in two lines: "Moss lights when it's wet. Crews wet the posts on the line they walk. A dark post's got a dry foot: nobody's keeping it." Leading the cart down the **lit** line is the way. Leading it down the **dark** line: after ten paces the old logs are sunk and the cart's wheel goes in to the hub (a harmless stop). Dunstan and the player heave it out (channel, 2 segments, progress kept) and back up to the fork. Bark, Dunstan: "Lit ones. I knew that. I was letting you learn it." (`MNS-B8.6`).
3. **The Wraith (C2, the crew's standard).** Back at the roadside works, the standard the crew stood up that morning is **risen**: clear of the mud, cloth moving with no wind. As the cart comes level, a **Banner Wraith** forms at its foot out of the peat (**MNS-E2**): a faint figure holding the shape of a tattered standard. It begins to walk its lane **across the road**, slowly, repeating the motion of carrying a standard forward. The cart stops by itself (Dunstan drops the shafts). Two ways through, both valid:
   - **Fight:** engage it in its lane. It fights to 0 HP and collapses into mud at its standard. The standard stays risen; at the next dusk it will re-form (condition). `MNS_WRAITH` = fought.
   - **Wait it out:** keep the cart back off its lane. The Wraith crosses the road and walks back to its standard on its repeating path, and does not engage anything outside its lane (ordinary aggro radius; it is not fleeing or disengaging, it is repeating a walk). After one full pass, the lane is clear long enough for the cart. `MNS_WRAITH` = waited.
   Nell, on the cart: "Does it want a name too? Tell it there's a queue." (`MNS-B8.9`). Nobody says what it is. Lysa: "Seen: something walked. Thought: walk faster."
4. **The causeway head.** The first crossing (C1) is at its last Slack as the cart reaches it and goes Sour after. At the head, the reed-cutter's wife takes the broth crock and her husband (`MNS-B8.12`) and presses a coin on the player (small payment).
**Verbs:** lead, read, choose a line, heave, fight or wait.

### Beat 4b: The Ferrow House (`S04b_ferrow_house`): *the strange moment*
**Objective:** *See Nell home.*
Lysa and Nell walk on to the Ferrow house (S3); the player goes with them. Dunstan walks behind and stops at the bench outside the door. He does not come in. Agna lets Nell and the player in (`MNS-D9`): "Sit. You'll eat. Then you'll tell me nothing, because I'm not asking." She sets bread and a bowl. Nell sits by the hearth with her back to the door and, while Agna fusses with the fire, **hums** a few bars of a slow tune, absently, the way people hum when their hands are busy.
Outside the open door, Dunstan, on the bench, sings the **end of the line** under his breath, in words, and stops.
Nobody comments (§A8). Agna goes on with the fire. Nell stops humming. The player is not given a dialogue option about it. Sets `MNS_LULLABY_HEARD` (always).
If the charm hold has not been taken, Agna offers it here instead: "Show the witness your knots, Nell. Ysolde'll want everything." (`MNS-D9.30`).
Agna shows the player to a bench: **Keep watch until morning** (one interaction; the presentation hour goes to morning). The step completes on waking.
**Verbs:** enter, eat, listen, rest.

### Beat 5: The Second Reading (`S05_second_reading`)
**Objective:** *Set the holds side by side.*
The register room, morning. The same people, plus **Edris** with her tin box on her knee, and **Mara** standing at the back with her spade (she has come to hear what she will mark). Ysolde lays two blank reed strips on the table: one says *The woman* and one says *The girl*. She asks the witness for holds for each (`MNS-D10`). This is the hold board: a dialogue sequence where every option is a hold the player may offer, gated by the `MNS_HOLD_*` flags, plus things that are **not** holds.

| Strip | Accepted holds (any two complete it; more are welcome) | Refused, with Ysolde's line (no penalty; the player chooses again) |
|---|---|---|
| **The woman** (the remains) | **Show the name-tape** (`MNS_name_tape`): "A child's tape. Linnet." · **Mara's account**: "A grown woman's arm. The tape was in her cuff." · **The Hayle book**: "Aldith Hayle and Linnet, on that road, in the last wet." · **Edris's account** (the sleeve custom): "Mothers sewed the child's tape in their own sleeve." | "Dunstan is sure." ("Sure isn't a hold. Grief is very sure.") · "A Wraith walked out of a standard on that road." ("Nothing on that road speaks for anyone. Not a banner. Not what walks out of one.") |
| **The girl** (Nell) | **The care leaf**: "A reed charm in the hem, three knots. Off the Standards road. Mother not found." · **The Hayle book**: "Three knots drawn by Linnet's name. The house mark." · **Edris's account**: "She came off that road that night, alone. Her mother was behind." · **Nell's charm** (if `MNS_HOLD_CHARM`): "She still has it." | "Nell and Linnet sound alike." ("In a small mouth, maybe. Maybe not. That's not a hold. That's a hope.") · "Nell hummed a song Dunstan knew." ("Songs travel. A song is not a hold.") |

When both strips have two holds, Ysolde says her reading (`MNS-D10.40`): "Two holds and more on each. Here's what I'll stand behind. Nell is very probably Linnet Hayle. The woman on Mara's ground is very probably Aldith Hayle, her mother, who carried her daughter's tape in her sleeve so somebody could find her." (beat) "Very probably. I won't round it."
Dunstan sits down on the floor. Agna says the line the quest is remembered for: **"I did the raising. Write that."** Ysolde: "I'll write it whatever we write."
Then Ysolde turns the book to Nell. Nell decides how her name is written. She asks the witness first: "You sat the seat. What would you write?" (`MNS-D10.60`). The **choice** (§A9.3):
- **Amended** (`MR_NAME_RECORD = amended`): "Write both names." Nell: "Then write both." The entry becomes *Nell Ferrow, born Linnet Hayle. Raised: Ferrow.* The remains are entered as *Hayle, Aldith, mother. Probable.* Mara cuts **no name** on her stone (she never does); the register carries it. Nell keeps the tape.
- **Qualified** (`MR_NAME_RECORD = qualified`): "Write Nell. Put the Hayle book beside it." Nell: "That's what I'd have said. I wanted somebody else to say it first." The entry stays *Nell. Fostered: Ferrow. Raised: Ferrow.* with a qualifying line naming the Hayle book as a hold. The remains are entered as *A woman. Carried a child's tape: Linnet. Marked by Mara Fenholt's stone. Unnamed. The Hayle household may mourn there.* Mara lays the tape back with the remains.
- A third option, "It's yours to say, Nell", returns her line, "I know. I'm asking you anyway," and the options again. She wants to hear it said by someone who isn't anybody's cousin.
Ysolde writes the entry (the player watches; document text in the dialogue file), reads it aloud once, and **blots the page**. She offers the player a seat at the table that night: "Sit with us tonight. Not on the stool. On the bench, with everybody." The quest **completes** on her line.
**Verbs:** show, recall, weigh, choose.

**Epilogue (no step): the table.** If the player goes to the register room longhouse at night (or keeps watch on the bench there), the table is laid. Food first (Agna makes the player sit; Dunstan brings smoked eel he does not mention). Then remembrance: Ysolde says, "Say whose story it is before you tell it" (MME08), and Edris tells the one about the night the road went under, in three lines. An empty place is set (MME04) with a child's work sign on it. Lines vary by `MR_NAME_RECORD` (`MNS-B12`). Nobody mentions the lullaby.

## A7. Encounters

Tuned for **Competent identity** (MD-10). Exact levels are Gameplay Designer calls.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MNS-E1** | Wave 1: 2 × Griefbit **swarm**, 1 × **carapace**. Wave 2 (after Edris sits with the man): 1 × swarm, 1 × carapace | Edris's old station: boiling out of the platform's rotten timbers round the cart | Swarms surge at the cart and at the player; the carapace guards the swarm's flank and butts | **Swarm:** the cloud tightens and the click-hum rises in pitch (~1.0 s), then surges along a short line (sidestep). **Carapace:** rears and clicks its wing-cases (~1.2 s), then a straight charge-butt with a small knockback. **Fear tell:** while the reed-cutter is crying out, a third swarm gathers over the cart (visible, ~3 s) in wave 1 only; it joins if wave 1 is not cleared in ~40 s. | First Mire fight; teaches that fear draws them, by showing the wave thin when Edris calms the man | 60–90 s; 60–80% HP remaining |
| **MNS-E2** | 1 × Banner **wraith** | The crew's standard at the roadside works (C2), at night during the cart walk | Repeats a walk across the road in a fixed lane; engages anything that enters its lane; re-forms at its standard while the standard is risen | **Forming:** the standard's cloth lifts with no wind and the peat at its foot darkens and swells (~3 s). **Cut:** draws its blade-shape back over its shoulder (~1.0 s), then a slow, wide cut. **Press:** leans forward behind the standard-shape (~1.5 s), then a two-step shove along its lane (one step of knockback; on the causeway that can put the player in the ditch shallows, which slow, never drown). | First sight of a Banner Wraith; teaches that it is a repeating motion tied to a place, and that it can be waited out | 30–45 s if fought; ~20 s to wait out one pass |

**Hunting fauna (not encounters):** fen fowl at Hob's hide (Hunting interaction; fauna fight only when provoked, bible §10). Herons are scenery.

**Hazards (not encounters):**
- **Running or Sour shallows:** non-walkable. The player stops at the edge; no damage. A bark tells them why.
- **Ditch shallows** along the causeway: walkable, slowed (standard slow while wading). No drowning, no deep water within reach of the road.
- **The dark line** (C5, `S04`): the cart's wheel sinks; a harmless stop and a two-segment heave.

**Rules**
- **Defeat at 0 HP** (CDR-1). Beetles and the Wraith fight until defeated. Beetles take the ordinary defeat presentation. The Wraith collapses into mud at its standard and re-forms at the next dusk while the standard is risen (place condition). Waiting out its pass is not a retreat: it is a repeating walk that never left its lane.
- **Melee or ranged** (CDR-2): both fights accept either. Swarms are small targets that reward area melee and are fine to shoot; the Wraith is slow and readable for both. Ranged is never required.
- **Combat never reveals evidence.** Every hold comes from a keeper (Mara, Edris, Dunstan, Lysa, Nell) or an object they keep. The Wraith and the beetles carry and reveal nothing. At the second reading the Wraith is explicitly refused as a hold.
- **Death:** respawn at the Sorrowmere causeway head before `S02b`; at Edris's old station from `S02b` to the start of `S04`; during `S04`, at the last stake the cart passed, with the cart waiting there. Defeated beetles stay defeated. Holds, the tape and the broth persist. Channel states never advance on death.
- **Co-op:** beetles and the Wraith shared. Each partner's holds, channel states, cart and choice are their own. Presentation follows each player's state (fallback: the host's stakes and cart; each partner still collects their own holds and makes their own choice).

### A7.1 MD-7 swap note

MR-M1 has **no Hollowfoot encounter** under either ruling. The only Hollowfoot person is the settled man at Fenward (F2), a non-combatant who is never targetable. If the Director retires Hollowfoot as an enemy family, nothing here changes. If the Director keeps them as enemies, nothing here changes either; the Fenward man remains a cared-for NPC by bible rule (MD-7 dignity rules).

## A8. The discovery moment: the lullaby at the Ferrow house

**What it is:** Nell hums a few bars of a slow tune she has never been taught, and Dunstan, outside the door, finishes the line in words. It is never explained (bible §7.5 "deliberately unexplained forever": Nell's lullaby). It is not resonance shown as power: no glow, no moss brightening, no UI. It is two people who have not met before yesterday knowing the same song. It proves nothing and is refused as a hold the next morning.

| Time | Element | Spec |
|---|---|---|
| 0 s | **The hum** | Nell, by the hearth, back to the door, hums four bars of a slow, falling tune. Her voice is quiet and not quite on pitch. Agna is kneeling at the fire with her back to Nell. |
| ~6 s | **The stop** | Nell stops humming where the tune would turn. She does not seem to know she stopped. |
| ~7.5 s | **The line** | From outside the open door, Dunstan, sitting on the bench, sings the turn of the tune under his breath, in words: *"...and the water's slack, and home."* (positional audio from the doorway; low; no music under it). |
| ~10 s | **The quiet** | Ambience ducks by about a third for ~2 s: the fire, the water under the piles. Agna's hands stop on the poker for one beat, then go on. Nell looks at her bowl. Dunstan, outside, looks at his hands. |
| After | **Nothing** | No one speaks of it. The player has no dialogue option about it in this scene. Agna's next line is about the bread (`MNS-D9.20`). |
| Never | **Explanation** | If the player raises it later with Lysa: "I heard it. I'm not going to make it mean anything for them." With Ysolde, at the hold board: "Songs travel. A song is not a hold." With Dunstan: "Mam sang that. Everybody's mam sang something." With Nell: "Did I? I do that." |
| UI | | The camera stays with the player. No cutscene. The keep-watch interaction appears on the bench only after the moment has played. |

**Why it is here:** it is MR-M1's Wonder beat (bible §1 emotional line), and it teaches the evidence rule from the inside: the most moving thing the player sees in the quest is the one thing that cannot go in the register.

## A9. Quest structure for implementation

### A9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to the Memorykeeper on the raised way. | `MNS-D1` end with accept | Yes | Quest Active on accept; Inactive on "not now" with re-offer at the register room door. `MNS_HOOK_ASKED` optional (`CN_COMPLETE` or TF-M3 Completed) |
| `S01_reading` | Sit the stranger's seat at the reading. | Sit interaction + `MNS-D2` end (both readings and the rule heard) | Yes | Address variant "witness" turns on for NPCs present (Ysolde, Dunstan, Agna, Nell, Edris, Lysa) |
| `S02_causeway` | Walk the causeway to Edris's old station. | Stake 1 inspected + keep watch to Slack + crossing + roadside pass-by volume + stake 2 inspected + enter far-end volume | Yes | Sets **`MR_CHANNELS`** at the end of the stake lesson (`MNS-D3.20`). C1 pinned Running → Slack on keep watch; C4 pinned Slack. Pass-by is on the only road. `MNS_STANDARDS_SEEN` optional |
| `S02b_station` | Help at the care station. | MNS-E1 all defeated | Yes | Edris's calming event fires on wave 1 defeated (`MNS-B3.4`) |
| `S03_holds` | Gather the holds for the register. | `MNS_HOLD_EDRIS` + `MNS_HOLD_LEAF` + `MNS_HOLD_TAPE` + `MNS_HOLD_BOOK` + `MNS_BROTH` set | Yes | Any order. Tape is quest item `MNS_name_tape`. Charm (`MNS_HOLD_CHARM`) optional, re-offered in S04 and S04b. C4 stays pinned Slack. Option B for the broth adds a keep-watch to dusk |
| `S04_walk_back` | Bring the cart home by the lit posts. | Cart reaches the causeway-head volume | Yes | Step start pins dusk; night at C5. Stake turns triggered by the cart passing (C6, C4, C1). Dark-line sink is a harmless stop with a 2-segment heave. MNS-E2 at C2: fight or wait (`MNS_WRAITH`). Small payment at the head |
| `S04b_ferrow_house` | See Nell home. | Enter the Ferrow house + lullaby event (`sorrowmere.lullaby`) + keep watch until morning | Yes | Sets `MNS_LULLABY_HEARD`. Charm re-offer (`MNS-D9.30`) |
| `S05_second_reading` | Set the holds side by side. | Both strips at two holds + choice in `MNS-D10` + `MNS-D10.90` end | Yes | Sets **`MR_NAME_RECORD`**. Item `MNS_name_tape` removed (fate by outcome). Quest → **Completed** |

### A9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `MNS_HOOK_ASKED` | `MNS-D1.30`–`.36` (optional; `CN_COMPLETE` or TF-M3 Completed) | — | *The Stranger's Seat* opening line (the player's not-found strip is still on the board); *The Book of Arrivals* (Ysolde: "You've asked after names before.") |
| `MR_CHANNELS` | `S02_causeway`, `MNS-D3.20` | Every stake inspect; `S02`–`S04` | MR-M2, MR-M3 (Rowan's knots build on it); every stake in the Mire |
| `MNS_STANDARDS_SEEN` | Roadside standards inspect (optional) | `MNS-B8.8` | MR-M2 `MBR-D2.05` (Calwen: "You looked at them. Most people don't.") |
| `MNS_HOLD_EDRIS` | `MNS-D4` end | Hold board | — |
| `MNS_HOLD_LEAF` | Tin-box channel + `MNS-D4.40` | Hold board | — |
| `MNS_HOLD_TAPE` | `MNS-D5` lift | Hold board | — |
| `MNS_HOLD_BOOK` | `MNS-D6` end | Hold board | — |
| `MNS_HOLD_CHARM` | `MNS-D7.23`, `MNS-D8.31` or `MNS-D9.32` (optional) | Hold board | — |
| `MNS_MARA_ACCOUNT` | `MNS-D5.12` or the tape lift (`MNS-D5.31`) | Hold board ("Mara's account"); `MNS-D4.20`, `MNS-D6.30` options | — |
| `MNS_EDRIS_SLEEVE` | `MNS-D4.21` (optional) | Hold board (the sleeve custom) | — |
| `MNS_FENWARD_VISITED` | Enter F1 volume during `S03` (optional) | `MNS-D8` variant | MR-M5 (Lysa's settled man nods to the player at the circle) |
| `MNS_BROTH` = self / hob | `S03` broth sub-objective | `MNS-B8.12` | *A Table for the Wet* (Lysa: "You cooked on the road once. Do it for twelve.") with `self` |
| `MNS_WRAITH` = fought / waited | `S04` at C2 | `MNS-B8.10` | MR-M2 `MBR-D1.12` (one line from Calwen) |
| `MNS_LULLABY_HEARD` | `S04b` event | Hold board refusal line | None (deliberately) |
| `MR_NAME_RECORD` = amended / qualified | `S05` choice | `MNS-D10.70`–`.86`, `MNS-B12` | MR-M2 (Dunstan's lines); MR-M5 (names roll; Nell and Dunstan's placement, §9.3); *Weight of the Soil* |

### A9.3 Choice: how the register writes her

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Amended** (`MR_NAME_RECORD = amended`): *both names* | The entry reads *Nell Ferrow, born Linnet Hayle. Raised: Ferrow.* The remains: *Hayle, Aldith, mother. Probable.* Nell keeps the tape. Dunstan cries without making a sound and then brings food. | Agna is hurt and says so once ("Ferrow's first. Good. It should be."). Mara's stone stays unnamed; some Marshfall neighbours will ask why the stone has no name when the book does (barks). | MR-M2: Dunstan speaks of "my sister" and nearly says Linny. MR-M5: Aldith Hayle is **read as a name** on the roll; Nell and Dunstan stand together at one stone. |
| **Qualified** (`= qualified`): *Nell, with the Hayle book as a hold* | The entry stays *Nell. Fostered: Ferrow. Raised: Ferrow.* with a qualifying line naming the Hayle book. The remains: *A woman. Carried a child's tape: Linnet. Unnamed.* under Mara's stone. The tape goes back with her. | Dunstan wanted a name cut and does not get one. He says "I can mourn at a stone. People do." and means it, mostly. | MR-M2: Dunstan says "Nell" carefully, like a word he is learning. MR-M5: the woman is read as *"one we hold, not yet known"*; Nell stands with Agna and Dunstan across the ring. |

**Neither is wrong.** Both keep every hold in the register; both write Agna's raising; both leave Nell's own name in her keeping. What changes is whether the register will say a name the evidence makes probable but not certain.

## A10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Channel reading (`MR_CHANNELS`) | Knowledge | Every stake in the Mire gives its state on inspect. MR-M3 builds on it. |
| Lantern-moss reading | Knowledge | No flag; taught in play. Night travel on Mire walkways uses it. |
| Sorrowmere hub | Access | Raised ways, the register room (search a name; the index boards), the causeway head (respawn point; keep-watch bench), the Ferrow house (Agna's bench) |
| The Standards Causeway | Access | A route across the Field to the Marshfall side, by the stakes |
| "Witness" | Address | NPCs who saw either reading address the player as "witness" from now on (bible §5.3). Nothing else changes. |
| Small payment | Currency | The reed-cutter's wife's coin at the causeway head. Economy tuning [GD]. |
| Skill XP | Action only [GD] | Melee or Ranged at defeat; Hunting and Cooking if done personally. No lump quest XP (bible §11.6). |
| Side-quest unlocks | Story | MSS, MLL, MRS, MFT, MFH, MSG, MNK |
| MR-M2 | Story | Offered by Calwen at his sanctuary the next morning (Corra brings word) |

## A11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player walks into Running or Sour shallows | Non-walkable edge; a bark; no damage. Keep watch is always available at the stake bench. |
| Player cannot or will not hunt | Hob's string (Option B) at the cost of one keep-watch turn. Never blocked. |
| Player offers a wrong hold | Ysolde refuses it with one line and the board stays open. No count, no penalty. |
| Player leads the cart down the dark line | The wheel sinks; a two-segment heave; back up to the fork. The cart cannot be harmed. |
| Player is beaten by the Wraith | Respawn at the last stake the cart passed; the cart waits there; the Wraith has reset in its lane. The player can wait it out instead. |
| Player leaves during the escort | The cart waits at the last stake passed (or the old station if it had not left). The night is re-pinned on return. |
| Player never visits Fenward | The charm is offered at the cart and at the Ferrow house. Fenward's scene is optional. |
| Death | Respawn by step (§A7). Holds, the tape and the broth persist. Defeated beetles stay defeated. |
| Logout | Restore to the persisted step: the register room (S00–S01), the causeway head (S02), the old station (S02b–S03 and the start of S04), the last stake passed (S04), the Ferrow house bench (S04b), the register room (S05). |
| Walking away | Quest stays Active at its step. Resume hook: Ysolde at the register room ("The room's still waiting. So's the book."), or after `S02`, Edris at the old station ("Still here. Shutting a station takes longer than you'd think."). |
| Fail state | None. |
| Co-op | Shared beetles and Wraith. Per-player holds, stake states, cart and choice. Presentation follows each player's own state; fallback: the host's stakes and cart drive the props, each partner still collects their own holds, sees their own reading and makes their own choice. A partner who has completed MR-M1 sits on the bench in the register room at the other's second reading and is addressed as "witness" too. |

## A12. Integration needs

Documented dependencies for a later Systems Engineer. Nothing here is implemented. Every item is a standard system unless marked.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Quest-pinned channel states** (bible N-1 fallback form) | Systems | Each step sets the state of the crossings it uses (C1 Running→Slack on keep watch; C4 Slack; the far end, C4 and C1 to Sour when the cart passes). A state swaps the shallows' walkable segment and the stake's water-line prop. Per player. No per-crossing schedule is needed for Act I. |
| **Keep-watch interaction** | Systems | Lowmark convention: advance the per-player presentation hour one turn at a marked bench. Used at C1, the Hayle house, the Ferrow house, the register longhouse. |
| **Escort-follow cart** | Systems / NPC | A handcart with NPCs that follows the player's position at walking pace along the causeway, stops when the player stops, cannot be harmed, and halts on enemy proximity. The "dark line" is a volume that triggers a stop-and-heave (2-segment channel). Standard escort pattern (as Lowmark *Night Ferry*, Thornfell TPW escort without calls). |
| **Lantern-moss posts** | Art / world state | Post props with a lit (wet) and dark (dry) material, swapped by presentation hour (lit at dusk and night where the line is tended). No light-gating logic in Act I. |
| **Lane-walking Wraith** | Gameplay / AI | An enemy that repeats a fixed path across the road and aggroes only within its lane (standard patrol plus aggro radius). Defeated at 0 HP; re-spawns at its standard at the next dusk while the standard prop is in its risen state (Lowmark drift-site state model). |
| **Fear-scaled spawn** (MNS-E1) | Gameplay | Wave 1 adds a third swarm if not cleared within ~40 s while the "frightened" NPC is in his frightened idle; a scripted ally action (Edris sits) swaps the NPC to calm idle before wave 2, which has a fixed smaller composition. Two authored waves; no new system. |
| **Hold board** | Dialogue | Dialogue options gated by quest flags and by item possession (`MNS_name_tape`), with two counters (one per strip) local to the conversation. Use-item-on-NPC is an acceptable alternative for the tape. Standard. |
| **Hunting from a hide; cooking at a hearth** | Skills / Gameplay | Existing Hunting and Cooking interactions. The fowl and the broth crock are carry-state quest objects until the economy pass defines fen fowl (MD-11). |
| **Scripted audio event** (`sorrowmere.lullaby`) | Audio | §A8: Nell's hum (local), Dunstan's line (positional, doorway), an ambience duck. Per player. |
| **Register page prop** | Art / world state | The open register in the register room shows the page written in `S05` (amended or qualified). Per player. |
| **Agility trigger** | Systems | Marshfall walkway gap; walkable fallback round the drying racks. |
| Creatures | Schema / Gameplay | Griefbit swarm, carapace; Banner wraith (bible §10). |

**New runtime needs: none.** Everything above is a standard system or the bible's N-1 fallback form.

## A13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Who Nell is** `[MD-2]` | Linnet Hayle, separated from her mother Aldith on the Standards road in the war's last wet. | A Ferrow, or a road child; it depends who you ask. | Care leaf, Hayle book mark, Edris's account, the charm, the tape in an adult sleeve. | The bones are Linnet's (Dunstan's reading); Nell is a Ferrow by blood (Agna's wish). | Certainty. The register says "very probably". | MR-M1 (resolved here, as probability). |
| **The stranger's seat** | Unknown in the Mire (R16, CV-M1 pays it). | "Every table has one." | A worn stool on the visitor's side; legs newer than its top. | A bit of courtesy for guests. | Why it exists. | CV-M1 (R16). Never in Mire content. |
| **The standards at the roadside** `[CAUSEWAY]` | Standing them up woke them (bible §2.3). | Oswin's crews are being careful. | Crew bark "so nobody drives over them"; cloth shifting with no wind; a Wraith at the same standard that night. | Ghosts protesting the road. | Why standing them up woke them. | MR-M2. |
| **Nell's lullaby** | Unexplained forever (bible §7.5). | — | A tune and a line. | Proof that she is a Hayle. | Everything. | None (deliberately). |

## A14. Open decisions

1. **MD-2 (the case):** the whole Hayle/Ferrow case rests on MD-2. If replaced, MR-M1's beats 1, 3, 5 and the documents change; the stakes, the cart walk, the Wraith and the roadside works survive any replacement that keeps "a fostered person whose two families each want a final answer" (Arcs §3.2).
2. **Aldith Hayle [NEW]:** the mother needs a name for MR-M5's roll (`amended`: read as a name). The name is authored here and is not canon. Changing it touches the Hayle book page, `MNS-D2`, `MNS-D10`, and MR-M5's roll.
3. **The sleeve-tape custom and "a house book stays under its own roof" [NEW]:** two small Mire customs authored for this case. Both are text only. If the Director prefers not to add customs, the tape becomes "sewn into her sleeve" without the custom (Edris's line is cut) and Dunstan simply brings the book; the hold board still works.
4. **MD-5 (Names Below register, Reedsward rota):** used as recommended. If MD-5 is not adopted, the register becomes "the Sorrowmere book" and "Reedsward crew" becomes "causeway crew" in text only.
5. **MD-3 (tag only):** the night walk is one of the reasons Rowan's crossing can move to first light without losing the Mire's night. Nothing here changes if MD-3 is ruled differently.
6. **Level framing (MD-10):** Competent identity. Hunting and Cooking levels are `[GD: low]` placeholders; both have a no-skill alternative.
7. **Edris's old care station:** a sub-site at the causeway's Marshfall end, not a numbered POI. The zone package (Batch 4) may fold it into MP08 or give it its own label. MAP VERIFICATION REQUIRED.

## A15. Internal review log

| Finding | Revision |
|---|---|
| The two-holds rule risked being a lecture. | Taught in three lines at the first reading, then used by the player at the hold board, where wrong holds (the song, the Wraith, Dunstan's certainty, the name's sound) are refused one by one. |
| Dunstan's claim (the bones are Linnet's) needed to be wrong without making him a liar. | The tape says Linnet; Mara's account says a grown woman's arm; Edris's account gives the sleeve custom. Dunstan misread the one object he had, from grief. |
| "Gave her name as Nell" against "Linnet" risked a cute solution. | Ysolde refuses the sound of the names as a hold ("That's a hope"). It is never explained. |
| Edris's ledger limit (owns her own care account; no unit, age or service). | She tells what she did that night and stops. She does not interpret the leaf or the tape; she gives the sleeve custom as something she saw mothers do. |
| Mara's limit (marks with stones, never names; never digs deeper than the ground offers). | She shows what the ground gave up, says what she saw, and cuts no name in either outcome. |
| The causeway walk risked being travel. | It is the stake lesson, a wait, a pass-by that seeds MR-M2, a hold on the way, and a second stake read alone. |
| The night walk risked a fail state (stakes turning Sour on the player). | Every turn is triggered by the cart passing. The road closes only behind. |
| The Wraith risked a non-CDR-1 "it leaves" outcome. | Waiting it out is a repeating walk in a fixed lane that never engages outside its lane; if engaged it fights to 0 HP. It re-forms only by condition (its standard is risen). |
| The lullaby risked becoming evidence. | It plays without a dialogue option and is refused as a hold the next morning. |
| Skill hook. | Hunting and Cooking for the broth, both `[GD: low]`, with Hob's string as a time-cost alternative. |
| Address. | "Traveller" until the first reading; "witness" from those present at either reading. No name, title or origin. |
| Hollowfoot (MD-7). | None fought. The settled man at Fenward is a non-combatant by bible rule. |

---
---

# Part B: MR-M2 The Banners That Refuse to Fall (`MBR`)

## B1. The quest in one paragraph

The morning after the reading, **Corra Sallis**, a young Bannerbearer, finds the player on the raised way: **Calwen Reed-Binder** is asking for them at his reed sanctuary. The causeway crews have been bringing him banners "that won't stay down", and at dusk two carters were knocked off the road by "the risen". **Edris** and **Oswin Garvey** are both at the sanctuary and not speaking. On the near causeway Calwen teaches the player to read a standard: **laid**, **leaning**, **risen**. Corra follows and is told to stay back; she does not. At the causeway works Oswin, tired and defensive, says what nobody has said aloud: his Reedsward crews lifted the fallen standards out of the logs and stood them at the roadside "so nobody'd drive over them", and he knows what that looks like now `[CAUSEWAY]`. The player cuts root-knee pins (or waits for Oswin's crew), then works three risen standards down the causeway with **Mara Fenholt**, who digs only to each pole's foot and never under it. As each cloth comes free, **Banner Wraiths** form round it and keep forming while it stays unfolded; the player fights them on a road two carts wide, pins the logs the pole was holding, and folds the cloth in Calwen's fold, strongest seam first. In the second standard's socket Mara's spade turns up a clay shard with marks pressed into it, and puts it aside: "That's not bone." Under the third, at the foot of the embankment, Reedlurkers guard a sunken **officers' chest**. Inside, three regimental day-books in oilcloth, kept by three different clerks who did not count days the same way, all stop on the same day: one with *"ground will not take a step"*, one mid-word, one with *"men sat down"*. Carrying the shard back past **Dunstan Hayle**, who has come to help stack banners, the player sees the lantern moss on the nearest post brighten and the loose silt settle flat in a ring round his boots. He does not notice. **Ysolde** takes the books as records and will not touch the shard: "That's older than anything we keep." At dusk, at the field's centre, a standard with two hoist sleeves stands up out of the bog with a colour party round it, and Corra says it is the **Banner That Sank Twice**. The player brings it down between its pulses and folds it with Corra on the far corner. That night at the sanctuary Calwen, Edris, Oswin and Corra argue whether the field's standards are **retired** or the old banner **restored** with honours at Griefwatch. Either way the causeway is cleared of standards, and Calwen puts the shard in his unsorted chest "with everything else nobody owns".

**What the player should remember:** the silt settling round Dunstan's boots, and three books that stop on one day. **What the player should want next:** what stopped three columns on one day, and who could tell them.

## B2. Selection record

| Candidate | Verdict |
|---|---|
| **A. Fight the Wraiths until they stop.** | Rejected. Combat disperses; conditions decide (bible §2.6). A fight that ends the problem would make the Wraiths ordinary spawns and the banner work pointless. |
| **B. The Wraiths show the player the battle.** | Rejected. Manifestations never testify (bible §11.3). The battle is told by three day-books and a missing explanation. |
| **C. States lesson → confession → three standards under attack (lift, pin, fold) → the chest → records and relics → the Risen Colour at dusk → retire or restore** (selected; the bible brief). | **Selected.** The player does the actual labour of retirement under pressure, finds the evidence by working the ground the way Mara allows, and meets the region's first miniboss as a standard that has to be brought down, not a creature to kill. |

## B3. Canon grounding

| Element | Source | Status |
|---|---|---|
| Field of Fallen Standards: flattened bog; banners and poles standing frozen; some shift when emotions run high | Dossier §VI.1 | [CANON] |
| Banner Wraiths dissipate if their banner is properly honoured or retired | Dossier §IX; C15 | [CANON] |
| Calwen Reed-Binder: washes, binds and stores fragments without sorting by allegiance; knows which fabrics rot slower; refuses to identify banners by faction | Mire anchors §II; Part 4 ledger (a banner needs a second channel before naming anyone) | [CANON] |
| Mara Fenholt: never forces, never digs too deep | Mire anchors §II | [CANON] |
| The Banner That Sank Twice: raised in victory, lost in retreat, raised again, drowned; if it surfaces, the regiment's honour must be restored | Dossier §XII.1 | [CANON myth] |
| Dossier questline 1: retrieving old regimental logs; Memorykeeper records vs. Memorywarden relics; retire or restore | Dossier §XV.1 | [CANON] |
| Memorywarden shards: stone or clay with faint marks; unrecognised; react near great emotional weight | Dossier §XI.5 | [CANON] legacy concept |
| Lantern moss said to brighten or dim with the tone of a gathering | Dossier §X | [CANON] |
| Reedlurkers: amphibious predators in shallows | Dossier §IX | [CANON] family |
| Bannerbearers carry ceremonial banners; colour shows communal emotion | Dossier §III, §VIII | [CANON] |
| Oswin Garvey, the standing-up, Reedsward crews | Bible §2.3, §5.2, MD-1, MD-5 | [PROPOSAL — DIRECTOR] MD-1 `[CAUSEWAY]` |
| Corra Sallis, banner states, Calwen's fold, the Risen Colour | Bible §1.1, §5.2, §10 | [NEW] |
| Day-books dated by weather run; two hoist sleeves on the Banner That Sank Twice | This package | [NEW] |

## B4. Quest summary card

| Field | Value |
|---|---|
| Working title | **The Banners That Refuse to Fall** |
| Suggested content id | `mire.main.02_banners_that_refuse_to_fall` |
| Arc position | Act I turn (Arcs §3.2, MR-M2: "separate Memorykeeper records from Memorywarden relics") |
| Prerequisite | MR-M1 Completed. Tuned for Competent identity (MD-10). |
| Offer | Next entry to Sorrowmere after MR-M1's completion (or waking from the epilogue's table): Corra Sallis on the raised way (`MBR-D1`), then Calwen at his sanctuary. |
| Solo / co-op | Solo-clearable. Co-op partners share every fight; standard states, folds, the chest, the logs item and the choice are per player. |
| Target length | 40–55 minutes first time |
| Combat share | ~35% |
| Dialogue share | ~20% |
| Work under pressure (lift, pin, fold, lever), reading, carrying, choice | ~45% |
| Skills touched | Melee or Ranged (either; neither required); Woodcutting ~[GD: low] (optional: the crew alternative costs a turn) |
| Choices | Retire or restore the field's standards (`MR_BANNERS`); cut the pins or wait for the crew (flag only) |
| Unlocks | `MR_BANNERS`; `MR_CAUSEWAY` = reset; Calwen's sanctuary (banner store, retirement pool); the Field's centre (quiet); six side quests and *Lifting Day* (Act I header); MR-M3 |
| **Anchor** (contract) | Banner and bone tenders (Calwen, Mara); Bannerbearers (Corra); the Reedsward crews `[CAUSEWAY]` |
| **World-truth row** (contract) | H12 (the war broke the Memorywardens' practice; their relics outlast it), H17 (seed: the last battle), H25 (local present pressure: the causeway decision) |
| **Revelation role** (contract) | **Plants** R08: three day-books that stop on one day; a shard that reacts near grief. Teaches the records/relics distinction. Owns nothing. |
| **Recurring evidence** (contract) | `MBR_unit_logs` (quest item) recur in MR-M3 (Ysolde's question opens it) and MR-M4 (the vestry log, a different custodian, runs the same weather and stops on the same fog). The shard recurs in Calwen's unsorted chest (MR-M4 reference; MR-M5 does not use it). |
| **State compliance** (contract) | Inactive / Active / Completed. Folds cannot fail (a wrong fold unfolds). Lift and lever progress is kept. Waiting for dusk and for the crew is always available. Choice recorded in `MR_BANNERS`; `MR_CAUSEWAY` = reset in both outcomes. Resume at the persisted step with a hook at the sanctuary (Calwen) or, during `S03`–`S04`, at the causeway works (Mara). |
| **Combat compliance** (contract) | Banner Wraiths, Reedlurkers and the Risen Colour, each defeated at 0 HP. Wraiths and the Colour re-form while their standard stays risen (place condition); bringing the standard down and folding it ends the condition, and any Wraiths still standing fight on to 0 HP. Melee or ranged; ranged never required. No SX. No defeated enemy gives testimony. |

## B5. The places

### B5.1 Calwen's Reed Sanctuary [MP14, CANON anchor location; NEW detail]

At Sorrowmere's edge, where the raised ways give out into reed beds. **MAP VERIFICATION REQUIRED.**

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **R1. The washing frames** | Offer (`S00`); the choice (`S06`). | Long reed frames with banner cloth stretched on them, drying. Buckets of grey water. Cloth of every colour washed down to earth colours. No two pieces sorted together by any mark. A bench where Edris sits at one end and Oswin stands at the other. |
| **R2. The fold table** | Calwen's fold taught (`S01`). | A long table of split reed with one laid standard on it, half folded. Calwen's fold board: a reed strip pegged with three small cloth tags (a double seam, a rolled hem, a hoist sleeve), in order. |
| **R3. The retirement pool** | `retired` outcome. | A still, square pool edged in old timbers. Folded standards lie on its bottom in rows under clear water, weighted with stones. Lantern-moss posts at its corners. |
| **R4. The unsorted chest** | Completion (`S06`). | A long chest with a reed lid, its sides worn smooth. Inside: buckles, a child's shoe, a broken horn tip, cap badges with the badges cut away, a bundle of letters nobody can read. Calwen's word for it: "everything else nobody owns". |

### B5.2 The Standards Causeway and the Field [MP08, MP07]

The same road as MR-M1, from the Sorrowmere side outward. **MAP VERIFICATION REQUIRED:** relative order: the near causeway (states lesson) → the causeway works (Oswin) → the three risen standards along the roadside → the embankment foot and the ditch (the chest) → the field's centre (the turnout platform).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **N1. The near causeway** | Banner states (`S01`). | Three standards within sight of the causeway head, one in each state: **laid** (flat in the bog, cloth under a skin of water, poles grown with moss); **leaning** (pole at a slant, cloth hanging heavy, the bog round its foot slightly raised); **risen** (pole upright and clear of the mud, its foot ringed with fresh black peat, cloth moving out from the pole with no wind). |
| **N2. The causeway works** `[CAUSEWAY]` | Oswin (`S02`); the pin pile (Woodcutting). | Logs on rollers, Oswin's crew eating on a stack. A **pile of reclaimed root-knees** (old causeway wood dug up in the relaying) with a splitting block and a wedge. Mallets. The roadside standards the crew stood up, now three risen, one leaning. |
| **N3. The three risen standards** | Recovery under attack (`S03`). | Each stands in the roadside peat against the causeway's edge, its pole wedged between two logs where the crew stood it, so the logs either side are pressed apart. **Standard 1** is the crew's standard from MR-M1 (the one a Wraith walked out of). **Standard 2** is older cloth with a broken finial. **Standard 3** stands at the bottom of the embankment on the ditch side, its foot in the ditch water. |
| **N4. The embankment foot and the ditch** | Reedlurkers; the chest (`S04`). | A wide ditch of standing water at the causeway's foot, thick with reeds. When standard 3 is out, the corner of an iron-bound box shows in the mud where its pole stood. Reeds part in lines when something moves under them. |
| **N5. The field's centre: the turnout platform** | The Risen Colour (`S05`). | A wartime passing place: a square of logs built out from the causeway, about twenty paces across, its edges sunk to the ditch line. Beside it in the open bog, a patch of black water where nothing stands. At dusk the **Banner That Sank Twice** stands up out of it. |
| **N6. The causeway head** | The shard moment (`S04b`). | Where the causeway comes up to Sorrowmere. Dunstan with a hand-sledge, stacking folded standards. A lantern-moss post beside the stack, in the stack's shade. Loose silt on the bottom logs from the crews' boots. |

### B5.3 The register room [MP01] (return)

As in MR-M1. The page from MR-M1 is open on the reading board (per player). Ysolde has cleared one end of the table for the books.

## B6. Player-facing sequence

### Beat 0: The Sanctuary (`S00_offer`)
**Objective:** *Speak to Calwen at the reed sanctuary.*
Corra Sallis finds the player on the raised way with a mood banner over her shoulder and an errand she is proud of (`MBR-D1`): "Calwen asks for you. He says you're the one who walked the causeway at night and came back." At the sanctuary, **Calwen** is at the washing frames. **Edris** sits at one end of the bench and **Oswin** stands at the other; neither speaks to the other (`MBR-B0.2`). Two carters sit on a crate with bruises and a broken cart wheel between them (`MBR-B0.3`: "The risen walked through us like we weren't there. Then it walked through us again.").
Calwen lays it out (`MBR-D1.10`): the crews keep bringing him standards that will not stay down; he folds them, they stir in the store; the road has Wraiths on it at dusk; "Somebody needs to go out and do it properly. It's hard work. I can't do it on my own and Mara won't do it without someone to lift."
- **Variant (`MNS_WRAITH`):** "You walked past one with a cart. Or through it. Either's a start."
- The quest becomes **Active** on accept. Corra asks to come. Calwen says no. She says "Yes, Calwen."
**Verbs:** talk.

### Beat 1: Banner States (`S01_states`)
**Objective:** *Learn to read the standards.*
First, at the fold table (R2), Calwen teaches **his fold** on a laid standard with no pressure (`MBR-D2`): "Strongest seam first. Then the hem. Then the hoist. Always that way. If it's wrong it comes undone. That's the cloth telling you." The player folds the practice standard (three fold handles; inspect each seam first to find the strongest: two close rows of stitching against one). A wrong fold unfolds with a soft sound; no penalty.
Then on the near causeway (N1), Calwen has the player **inspect** three standards, one in each state, and names them (`MBR-D2.20`–`.40`):
- **Laid:** "Flat. Under water or near it. That's quiet ground. Leave it."
- **Leaning:** "Stirring. If somebody grieves near it, the mud gets up. Echoes, sometimes." (He does not use the word ghost; nobody does.)
- **Risen:** "Clear of the mud, cloth going with no wind. That one walks at dusk. And if you lift it, it walks whenever it likes, until it's folded."
Corra has followed and is standing ten paces behind with her mood banner. Calwen: "Back to the frames, Corra." Corra: "I'm not here." (`MBR-B1.4`). She stays, out of the way, for the rest of the quest (non-combatant, never targetable; she never enters a fight lane).
- **Variant (`MNS_STANDARDS_SEEN`):** Calwen: "You looked at them, on the way out. Most people don't."
**Verbs:** fold, inspect, listen.

### Beat 2: Oswin (`S02_oswin`) `[CAUSEWAY]`
**Objective:** *Speak to the crew-lead at the causeway works.*
At the works (N2), **Oswin Garvey** is sitting on a log with a bowl he has not touched (`MBR-D3`). Required talk. He tells it plainly, defensively, without being asked twice: the spate soured the ferry way; Marshfall's peat and food had to come in and the sick had to go out before the long wet; the old road was the only ground that would hold; Edris asked him to wait for a Silt hearing [MD-5] and he did not, because "the hearing sits after the rain, and people eat before it". When the crews found fallen standards in the line of the logs, they lifted them out and **stood them up at the roadside so nobody'd drive over them**. "It seemed the decent thing." (beat) "I know what it looks like now. I've got eyes."
Player options let the player ask what he thinks woke them (he does not know, and says so: "Seen: we stood them up, and they stood up. Thought: I'd rather not."), ask whether he'd do it again ("People ate. Ask me after the wet."), or say nothing. None changes a flag. The bible's rule holds: a decision that was kind and wrong at once, and he is not the villain.
Then the work: the logs each risen pole was wedged between will roll once the pole is out, so the player needs **root-knee pins** (six, two per standard). Oswin points at the pile.
- **Cut them yourself (Woodcutting ~[GD: low]):** split six pins from reclaimed root-knees at the splitting block (3 interactions, 2 pins each). Oswin comments on the first ("That'll hold. Ugly, but it'll hold."). Sets `MBR_PINS` = self.
- **Leave it to the crew:** Oswin's crew will split them after they eat. **Costs a turn:** keep watch at the works (one presentation turn). Sets `MBR_PINS` = crew.
**Verbs:** listen, ask, cut (or wait).

### Beat 3: Three Standards (`S03_standards`)
**Objective:** *Bring down the three risen standards.* (Journal: *Standard 1 / Standard 2 / Standard 3*; taken in road order.)
**Mara** meets the player at standard 1 with her short spade (`MBR-D4`). Her rule, said once: "I dig to the foot. Not under it. If it won't come from the foot, it stays." Calwen stands back on the road with a carrying frame for the folded cloth.
Each standard is the same four-part job, and the job gets harder down the road:

| Part | What happens | Rules |
|---|---|---|
| **1. Lift** | A channelled lift beside Mara: **three segments** (~4 s each). Mara digs round the pole's foot between segments; the player rocks and draws the pole. | A hit interrupts the current segment; completed segments are kept. As segment 3 completes, the pole comes out and the cloth comes free. |
| **2. Wraiths form** | As the cloth comes free, Banner Wraiths form round it out of the roadside peat (**MBR-E1/E2/E3**). | They fight to 0 HP and collapse into mud. While the cloth is **unfolded**, each defeated Wraith re-forms ~25 s after its defeat at the standard's foot, after a readable ~3 s tell (the cloth lifts and cracks once with no wind; the mud at the foot swells). |
| **3. Re-pin** | The two logs the pole held apart start to roll: that section of road becomes **loose** (walkable, slowed). The player drives two pins (2 interactions, ~3 s each). | Needs the pins from `S02`. Pinning restores the road. Calwen will not lay cloth on loose logs ("It'll go in the ditch with the logs."); the fold handles become active once both pins are in. |
| **4. Fold** | Calwen's fold on the cloth where it lies: **three fold handles** in order (strongest seam, then the hem, then the hoist). Each fold is ~2.5 s. | A wrong fold unfolds (no penalty). The third correct fold **ends the condition**: no more Wraiths form from that standard. Any Wraith still standing fights on to 0 HP. Calwen lifts the folded standard onto his frame. |

**The progression down the road.**
- **Standard 1 (MBR-E1):** the crew's standard from MR-M1. Two Wraiths. Its cloth has one double seam; the fold is easy. This is the lesson under pressure.
- **Standard 2 (MBR-E2):** two Wraiths and a **bearer** (buffs nearby Wraiths while its standard stands; see §B7). Its cloth has two seams: one double, one single mended in a different thread. During the lift, at segment 2, Mara's spade stops on something at the pole's foot that is not wood. She lifts it out with two fingers and sets it on a cloth: **a clay shard**, a palm wide, broken on two sides, with marks pressed into it before firing (`MBR-D4.20`: "That's not bone. Not mine."). It goes in the lid of her basket. Optional inspect (`MBR-I` table). The lift continues.
- **Standard 3 (MBR-E3):** three Wraiths and a bearer, at the **embankment foot**, with its foot in the ditch water. The player works on the slope between road and ditch. Its cloth has three seams; the double seam is in the middle, under a crust of mud, and has to be inspected to be seen. As the cloth comes free, **Corra** runs down the bank to catch it before it goes in the water (`MBR-B3.9`), then backs off when Calwen shouts. She is never targeted and never in danger: non-combatants are never targetable (rulings §3.1.6), and the Wraiths press the player.
The road is **two carts wide**. Wraiths come along it in a lane, and their shove can put the player in the ditch shallows (slowed, never drowned). Ranged players have the length of the road; melee players have the width of it. Neither is required.
**Verbs:** lift, fight, pin, read seams, fold.

### Beat 4: The Officers' Chest (`S04_chest`)
**Objective:** *Raise what's under the third standard.*
Where standard 3's foot came out of the ditch mud, a corner of iron-bound wood shows. Mara looks at it a long time (`MBR-D4.40`): "I didn't dig that. The ground let go of it when the pole came out. I don't dig under a foot." (beat) "You're only lifting. That's allowed."
The disturbance has brought **Reedlurkers** up the ditch (**MBR-E4**). Clear them (to 0 HP). Then lever the chest up out of the mud with a stripped pole from the crew's stack: a channelled lever, **three segments** (~4 s each), progress kept. Calwen comes down to help pull it onto the bank.
Inside, wrapped in oilcloth stiff as bark: **three regimental day-books** (`MBR_unit_logs`, quest item, one bundle). Calwen turns each over without opening it. Their covers have had their marks cut away. He can tell from the bindings that they were not made in one store, and he will not say whose (`MBR-D5`): "Three bindings. Three stores. That's all I'll say, and you'll not get more out of me with a stick." The player can read the last pages there (document text in the dialogue file). Each book counts its days in its own way. Each ends on a short line:
- *"Ground will not take a step."*
- *"We are ordered forward at the turn of the li"* (ends mid-word)
- *"Men sat down."*
Calwen does not comment. Mara says, "Seen: three books. Thought: none of my business." and goes back up to the road.
**Verbs:** fight, lever, read.

### Beat 4b: Records and Relics (`S04b_records`): *the shard moment*
**Objective:** *Take the books to Ysolde.*
Back on the road Mara takes the shard out of her basket lid and holds it out (`MBR-D4.60`): "You carry it. I don't carry what isn't bone." The player carries **the shard** (carry-state object; movement normal; it cannot be dropped by a hit). The road home is quiet: every standard on it is down.
At the **causeway head** (N6), **Dunstan Hayle** is stacking folded standards on a hand-sledge (he came to help when Calwen asked for hands). The path to Sorrowmere passes him. As the player passes within a few paces, the **strange moment** plays (§B8.1): the lantern moss on the post beside the stack brightens, and the loose silt on the logs settles flat in a ring round Dunstan's boots. Dunstan goes on stacking. He does not notice. The player is given no dialogue option about it. Sets `MBR_SHARD_MOMENT`.
In the **register room**, **Ysolde** clears the table end (`MBR-D6`). She opens the three books side by side and reads them without hurrying, then tells the player what she can stand behind: three ways of counting days, three clerks; the same weather in the same order on the last days in all three (rain, rain, rain, a hard frost, a thaw, fog, fog); then all three stop. "That's one day, or I'm no keeper." She will not guess whose. "These are ours. Records. Somebody wrote them so somebody would read them. I'll keep a copy and you'll keep the books, because I think you're going to need them."
Then the player shows her the shard (dialogue option, or use-item-on-NPC). She does not take it. She does not touch it. "That's not ours. That's older than anything we keep." (`MBR-D6.40`). Asked what it is: "I don't know, and I'm not going to make a story so I feel better about not knowing. Take it to Calwen. He keeps what nobody owns." This is the dossier's records/relics distinction (Arcs §3.2 MR-M2 purpose), said once by the person whose job it is.
At the **sanctuary**, Calwen takes the shard in a cloth and sets it in a wash basket, not in the chest yet ("Not till we've decided where the rest go."). He says the field's centre has been stirring every dusk this week, and that tonight he wants it done.
- **Variant (`MR_NAME_RECORD`):** Dunstan's line at the sledge differs (`MBR-B4.2`: amended, "My sister's coming to table at the week's end. Nell. Linny. I keep doing that."; qualified, "Nell says hello. I'm practising saying it.").
**Verbs:** carry, pass, read, show.

### Beat 5: The Risen Colour (`S05_colour`)
**Objective:** *Bring down the standard at the field's centre.*
At the sanctuary, **Keep watch until dusk** (one turn) or arrive at dusk. Calwen, Mara and Corra walk out with the player to the turnout platform at the field's centre (N5). Nothing stands there. As the light goes, a standard **rises** out of the black water beside the platform: pole first, then the cloth, heavy and dark, moving out from the pole against no wind. Its hoist has **two sleeves**, one sewn inside the other. Corra says the story aloud (`MBR-D7`): raised in victory, lost in retreat, raised again, drowned. Calwen: "Seen: two sleeves. Thought: you're going to tell me it's the one in the story. You just did." He does not say it is.
A **colour party** forms round it out of the mud: the **Risen Colour** (a tall, coherent figure holding the standard's shape, never named in UI or dialogue; the encounter label is internal), two bearers and two Wraiths (**MBR-E5**). It moves as a party, not a crowd.
**How it works (§B7):**
- **The pulse.** Every ~30 s the standard **pulses**: the cloth cracks out stiff and a ripple runs out through the mud from its foot (~3 s tell). On a pulse, any bearer or Wraith that has been defeated re-forms at the standard's foot, and the Colour itself re-forms if it is down and the standard is still standing.
- **Bring the Colour down, then lift.** When the Colour is defeated it collapses into mud and slides to the standard's foot. That opens the **lift**: Mara digs to the foot while the player draws the pole, **three segments** (~4 s each), progress kept. Once opened, the lift stays open for the rest of the fight, even if a pulse re-forms the Colour. A pulse during the lift re-forms the party but never undoes completed segments. Completing the third segment brings the standard down onto the platform: **the Colour no longer re-forms**.
- **Fold it under pressure.** The cloth is down but unfolded. The pulse weakens: each pulse now forms one Wraith from the cloth. The fold is Calwen's, on a cloth twice the size: the big standard needs two people, and **Corra** takes the far corner without being asked (`MBR-B5.6`; if somehow absent, Calwen does). The cloth has two double seams; one is torn through. The strongest seam is the whole one. Three correct folds end the condition. Any Wraith still standing fights on to 0 HP.
The step completes when the standard is folded and every enemy on the platform is defeated. Corra is holding the folded standard against her chest and will not give it to Calwen.
**Verbs:** fight, lift, fold, read the pulse.

### Beat 6: Retire or Restore (`S06_choice`)
**Objective:** *Decide what happens to the field's standards.*
The sanctuary at night, the washing frames lit by moss posts. Calwen, Edris, Oswin and Corra (`MBR-D8`). The folded standards from the causeway lie on the fold table; the Banner That Sank Twice lies apart. They argue, briefly and in voice:
- **Calwen** will do either properly. "Retiring is honour. Raising is honour. Leaving it in the mud isn't."
- **Oswin** `[CAUSEWAY]`: "Put them all down. I stood them up. I'll not stand one up again." Edris, to him and not to the room: "I asked you to wait." Oswin: "I know." That is all they say to each other.
- **Edris**: "Laying them down is kind. Raising it is kind. Whatever you do, do it slow."
- **Corra**: the story says that if it ever surfaces, its honour must be restored. Griefwatch's vigil hall has a hook over the door nobody has hung anything on. "I'd carry it. I'd carry it all the way."
Then they look at the player. The **choice** (§B9.3):
- **Retired** (`MR_BANNERS = retired`): all the field's standards, the Banner That Sank Twice with them, are washed and laid in the retirement pool. The causeway sites go quiet for good.
- **Restored** (`MR_BANNERS = restored`): the Banner That Sank Twice is washed, mended at its two sleeves, and carried by Corra to **Griefwatch's vigil hall**, where it is raised with honours "for whoever", as the old story asks; the others are laid in the pool. The causeway sites go quiet. Griefwatch now flies a banner the ridge can feel (MR-M5 reads it).
Either way, Oswin says his crews will take every standard off the roadside in the morning and leave none beside the road (`MR_CAUSEWAY = reset`).
Calwen then takes the shard from the wash basket in its cloth, lifts the reed lid of his **unsorted chest**, and puts it in "with everything else nobody owns". The quest **completes** when the lid goes down.
**Verbs:** listen, choose.

**Epilogue (no step).** On the player's next pass along the causeway, the roadside is bare: pale holes in the peat where standards stood, logs pinned with new root-knee pins, crews walking it at ordinary pace. With `restored`, Griefwatch's vigil hall shows the banner over its door on the player's first visit there, and Corra standing under it in her best coat. With `retired`, the retirement pool has a new row on its bottom, the largest cloth at the end of it.

## B7. Encounters

Tuned for **Competent identity** (MD-10). Exact levels are Gameplay Designer calls. Every Wraith and the Colour are earth-memory impressions: defeated at 0 HP, they collapse into mud and re-form only while their standard stays risen (condition), never by health.

| Id | Enemies (§10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MBR-E1** | 2 × Banner **wraith** | Standard 1 (N3), on the road | Advance down the road lane; cut and shove | **Cut:** blade-shape drawn back over the shoulder (~1.0 s), then a slow wide cut. **Press:** leans behind its standard-shape (~1.5 s), then a two-step shove along the lane (one step knockback; can put the player in the ditch shallows: slowed). **Re-form tell:** the standard's cloth cracks once with no wind and the mud at its foot swells (~3 s). | The work-under-pressure lesson | 60–90 s from lift to fold; 60–80% HP |
| **MBR-E2** | 2 × wraith, 1 × **bearer** | Standard 2 | Bearer hangs back by the standard and buffs | As E1. **Bearer, Raise:** lifts its standard-shape high and holds (~2.0 s, the shape's cloth ripples); if not interrupted, nearby Wraiths' cuts come faster for ~10 s. Any hit during the raise cancels it. | Introduces the bearer and the priority target | 90–120 s; 50–70% HP |
| **MBR-E3** | 3 × wraith, 1 × bearer | Standard 3, on the embankment slope | As E2; the slope narrows the fighting ground | As E2 | The hardest standard; terrain matters | 100–140 s; 50–70% HP |
| **MBR-E4** | 2 × Reedlurker **lurker**, 1 × **snapper** | The ditch at the embankment foot | Lurkers: ambush from the reed line and spit; snapper: holds the bank | **Reed-ripple:** a line of reeds parts toward the player (~1.5 s), then a lunge-bite from the water's edge. **Lurker spit:** rears its head back (~1.2 s), then a short arcing gob of mud that slows briefly where it lands. **Snapper:** jaws open with a wet clack (~1.0 s), then a clamp that roots the player for ~1.5 s. | First Reedlurkers (bible §10 "first seen: MR-M2 ditch"); a ranged answer to a ranged enemy, and melee cover behind the bank | 45–70 s |
| **MBR-E5** | **The Risen Colour** (elite, Banner Wraith family; never named in UI), 2 × bearer, 2 × wraith; after the lift, 1 × wraith per pulse until folded | The turnout platform at the field's centre (N5), at dusk | The Colour holds the standard's ground and advances down the platform; bearers buff; Wraiths screen | **Pulse (the standard):** cloth cracks out stiff, ripple runs through the mud from its foot (~3 s); re-forms defeated members, and the Colour if the standard still stands. **Colour, Dip:** lowers its standard-shape forward (~1.5 s), then a wide sweeping arc in front (step behind or to the side). **Colour, Advance:** plants and rears its pole-shape upright (~2.0 s, the cloth cracks), then strides four paces down its lane striking anything in it (step out of the lane). **Colour, Rally** (below half health, once per life): raises the shape high (~2.5 s); if not interrupted, re-forms any defeated bearer at once. **Bearer/Wraith:** as E1–E2. | Miniboss phenomenon: bring a standard down under pressure; read the pulse | 3–4.5 min including the lift and fold; 40–60% HP |

**Hazards (not encounters):**
- **Ditch shallows:** walkable, slowed. No drowning.
- **Loose logs** where a pole has come out and the logs are not yet pinned: walkable, slowed (standard slow), until pinned.
- **The black water** beside the turnout platform: non-walkable.

**Rules**
- **Defeat at 0 HP** (CDR-1). Wraiths, bearers and the Colour fight until defeated and collapse into mud. Reedlurkers take the ordinary defeat presentation and are harvestable where the economy allows. **No enemy is "cleared" by the condition ending:** when a standard is folded it stops forming new Wraiths, and those still standing fight on to 0 HP.
- **Re-forming is a place rule** (rulings §3.1.2; bible §2.6): it depends on the standard's state (risen and unfolded), never on health or time-in-fight.
- **Melee or ranged** (CDR-2): every fight accepts both. The road gives ranged players length and the Wraiths are slow; the Colour's Advance closes distance and the pulse brings back whatever was out-ranged, so kiting is valid and bounded. Lurker spit gives ranged players something to answer and melee players the bank to close behind. Ranged is never required.
- **Combat never reveals evidence.** The shard comes from Mara's dig, the books from a chest levered out of the mud, the cause from Oswin's mouth. Nothing drops from a Wraith or a Reedlurker but ordinary loot.
- **Non-combatants:** Calwen, Mara, Corra and Dunstan are never targetable and are never engaged by Wraiths. During fights Mara stands back on the road and Corra stays behind her; neither can be harmed.
- **Death:** respawn at the causeway head (N6). Folded standards stay folded; pinned logs stay pinned; lift and lever segments are kept; defeated Reedlurkers stay defeated. A standard that was lifted but not folded keeps its Wraiths in place (they reset to full health on the player's return, as an ordinary leash reset). For MBR-E5: the step stays at dusk on return (re-pinned); lift and fold progress are kept.
- **Co-op:** every fight shared. Each partner's standards, pins, folds, chest and logs are their own (per-player props; fallback: the host's standard states, with each partner completing their own lift, pin and fold interactions on the host's props). The Colour's pulse and re-forming follow the host's state; each partner's lift and fold progress is their own.

### B7.1 MD-7 swap note

MR-M2 has **no Hollowfoot** in any role. Nothing changes under either MD-7 ruling.

## B8. The discovery moments: presentation specs

### B8.1 The shard passes Dunstan (Beat 4b)

**What it is:** the dossier's shard that "reacts subtly near great emotional weight" (§XI.5) shown once, near a grieving man who does not know he is grieving out loud. It identifies nobody and proves nothing (bible §2.4). It is the R08 seed: the Memorywardens' relics answer grief.

| Time | Element | Spec |
|---|---|---|
| 0 s | **Approach** | The player, carrying the shard, comes within ~3 paces of Dunstan at the sledge. Late afternoon, grey light; the moss post beside the stack is in the stack's shade. |
| ~0.5 s | **The moss** | The lantern moss on that post brightens from its daytime grey to a faint, clear glow, as it would at night after rain. Only that post. |
| ~1.5 s | **The silt** | The loose silt on the logs round Dunstan's boots settles: a ring about an arm's length across goes flat and smooth, as if water had stood on it and drained. A few grains slide inward. No sound beyond the ordinary. |
| ~3 s | **Dunstan** | He lifts the next folded standard onto the sledge and squares it. He does not look down. If the player stops, he looks up and says his ordinary line (`MBR-B4.2`). |
| ~6 s | **After** | As the player walks on, the moss fades back to grey over ~4 s. The ring stays flat until the player looks away. |
| Never | **Explanation** | Nobody else sees it. The player has no dialogue option about it. If the player tells Calwen: "Seen: you saw something. Thought: I'm not putting it in the chest with the shard." If the player tells Ysolde: "That's not a hold for anything. I'll write that you saw it, if you like. Under 'seen', not under 'so'." (sets nothing). |
| UI | | No glow on the shard itself, no item highlight, no UI. Camera stays with the player. |

### B8.2 The day-books (Beat 4)

| Element | Spec |
|---|---|
| **Object** | Three books, each wrapped in oilcloth gone stiff. Covers cut where marks were. Bindings of three different kinds (reed-sewn; thong-bound; stitched through boards). |
| **Reading** | The player reads the last pages in a document view (dialogue file). Each counts days differently: one by day of the march, one by week and day, one only "next day". All record the same run of weather on their last pages. |
| **The endings** | *"Ground will not take a step."* · *"We are ordered forward at the turn of the li"* · *"Men sat down."* |
| **What nobody says** | Whose units; which side; who died; how many; what stopped them. Ysolde only says: one day. |
| **Why weather and not a date** | The books do not share a calendar. Matching them by the weather run is a Memorykeeper's craft (bible §5.3 rule 7), and it lets MR-M4 date the vestry log the same way without the Mire ever stating a calendar date. |

## B9. Quest structure for implementation

### B9.1 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_offer` | Speak to Calwen at the reed sanctuary. | `MBR-D1` end with accept | Yes | Offered on next Sorrowmere entry after MR-M1 Completed (Corra, `MBR-D1.01`). `MNS_WRAITH` variant |
| `S01_states` | Learn to read the standards. | Practice fold done + three state inspects at N1 + `MBR-D2` end | Yes | `MNS_STANDARDS_SEEN` variant. Corra follows from here (presentation) |
| `S02_oswin` | Speak to the crew-lead at the causeway works. | `MBR-D3` end + six pins (self: 3 Woodcutting interactions; crew: keep watch one turn) | Yes | `[CAUSEWAY]`. Sets `MBR_PINS` |
| `S03_standards` | Bring down the three risen standards. | Standards 1–3 each: lift (3 segments) + 2 pins + fold (3 correct) | Yes | Road order. MBR-E1/E2/E3 on each lift. Shard found at standard 2 lift segment 2 (`MBR_SHARD_FOUND`). Condition ends per standard on the third fold |
| `S04_chest` | Raise what's under the third standard. | MBR-E4 all defeated + lever (3 segments) + chest opened | Yes | Grants **`MBR_unit_logs`**. Last-page read optional here (required in S04b at Ysolde's table) |
| `S04b_records` | Take the books to Ysolde. | Shard carried past Dunstan (event `causeway.shard_moss`) + `MBR-D6` end (books read; shard shown) + shard left with Calwen | Yes | Sets `MBR_SHARD_MOMENT`, `MBR_LOGS_READ`. Shard is a carry-state object, not an item |
| `S05_colour` | Bring down the standard at the field's centre. | Keep watch to dusk (or arrive at dusk) + MBR-E5: lift (3 segments) + fold (3 correct) + all enemies on the platform defeated | Yes | Pulse ~30 s. Lift and fold progress kept |
| `S06_choice` | Decide what happens to the field's standards. | Choice in `MBR-D8` + Calwen stores the shard (`MBR-D8.90`) | Yes | Sets **`MR_BANNERS`**, **`MR_CAUSEWAY = reset`**. Quest → **Completed** |

### B9.2 Flags

| Flag | Set by | Read by (here) | Read by (later packages) |
|---|---|---|---|
| `MBR_PINS` = self / crew | `S02` (`MBR-D3.32` / `MBR-D3.36`) | `MBR-B2` | *Lifting Day* (Oswin: "You split pins for me once.") with `self` |
| `MBR_SHARD_FOUND` | `S03` standard 2 | Shard inspect | — |
| `MBR_SHARD_MOMENT` | `S04b` event | `MBR-D6.60`, `MBR-D6b.02` variants | MR-M4 (Mabyn, optional line about lantern moss and grief); none required |
| `MBR_LOGS_READ` | `MBR-D6` | — | MR-M3 offer (Ysolde's question) |
| `MBR_unit_logs` (item) | `S04` | `MBR-D6` | MR-M3 (offer); MR-M4 (vestry-log weather match; possession not required) |
| `MBR_CORRA_CORNER` | `S05` fold with Corra | `MBR-D8` | MR-M5 (Corra's line at the circle with `restored`) |
| `MR_BANNERS` = retired / restored | `S06` | `MBR-D8.70`–`.87`, epilogue | MR-M5 (Corra's banner and one extra Wraith wave with `restored`); Griefwatch props; *Lifting Day*; *A Banner With No Side* |
| `MR_CAUSEWAY` = reset | `S06` completion | Causeway roadside props | *Lifting Day* (MR-M5 does not read it; Oswin's attendance there comes from *Lifting Day*) |

### B9.3 Choice: retire or restore

| Option | Immediate result | Cost | Later |
|---|---|---|---|
| **Retired** (`MR_BANNERS = retired`): *lay them all down* | Every standard from the field, the Banner That Sank Twice last, is washed and laid in the retirement pool in a new row. Calwen says the rite's words, which are only "We put you down. Rest." Oswin carries the last one to the water. | Corra is disappointed and says so once ("The story said."). The old banner's story ends without the ending the story asked for. | MR-M5: the ridge's standards are fought and retired as written, with no extra wave; Corra comes to the circle with her mood banner and nothing else. *A Banner With No Side*: Calwen's store is quieter. |
| **Restored** (`MR_BANNERS = restored`): *raise the old banner with honours* | The Banner That Sank Twice is washed and its two sleeves mended. Corra carries it to Griefwatch, where Ide Larrow's Marshwardens hang it over the vigil hall door "for whoever". The others are laid in the pool. | Griefwatch now flies a banner from the last battle's field. Bran Hollowstep, at his watchpost, looks at it for a long time (MR-M5 line). The ridge feels it. | MR-M5: Corra brings the banner up to the circle; the ridge's standards answer it (one more Wraith wave, one more ally line). Griefwatch's hall props show it. |

**Neither is wrong.** Both bring every standard down properly, both quiet the causeway, and both reset the road. What changes is whether one banner from the field stays up, honoured, where the ridge can feel it.

## B10. Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Banner-state reading | Knowledge | No flag; taught in play (bible §1.1). Every standard in the Mire reads by its state from now on. |
| Calwen's fold | Knowledge | Used again in MR-M5 (the player does it faster) and *A Banner With No Side*. |
| `MBR_unit_logs` | Quest item / knowledge | Readable at any time; carried into Act II. |
| Calwen's sanctuary | Access | Washing frames, fold table, retirement pool, unsorted chest (inspect); side-quest giver for MBS |
| The causeway, reset | World state | Roadside standards removed; crews walk it; dusk Wraiths on the causeway end (`MR_CAUSEWAY = reset`). The field away from the road keeps its ordinary standards and states. |
| Small payment | Currency | Oswin's crew rate for "a day's lifting", paid by Oswin himself, awkwardly. Economy tuning [GD]. |
| Skill XP | Action only [GD] | Melee or Ranged at defeat; Woodcutting if the pins were split personally. No lump quest XP. |
| Side-quest unlocks | Story | MBS, MWS, MMR, MHG, MBO, MRH; MLD (with MLW) |
| MR-M3 | Story | Ysolde reads the books again and wants to know what stopped three columns on one day. |

## B11. Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Player folds wrongly | The cloth unfolds. The fold handles reset. No penalty beyond time. |
| Player has no pins | The fold handles stay inactive and Calwen says why. The pin pile and the crew alternative are always available at N2. |
| Player cannot or will not cut | The crew alternative costs one keep-watch turn. Never blocked. |
| Wraiths keep re-forming | Expected while the cloth is unfolded. The re-form tell gives a ~3 s warning; each re-form takes ~25 s. Folding ends it. |
| Player stands in the ditch | Slowed. Reedlurkers in the ditch only before `S04` is complete; afterwards the ditch is quiet. |
| Player is beaten | Respawn at the causeway head; progress kept (§B7). |
| Player arrives at the field's centre outside dusk | The objective reads *Keep watch until dusk*; the platform's bench offers it; the sanctuary's bench offers it too. |
| Logout | Restore to the persisted step: the sanctuary (S00–S01), the works (S02), the causeway head with standards in their saved states (S03–S04), the register room (S04b, shard state kept: the player still carries it, or Calwen has it), the sanctuary at dusk (S05), the sanctuary at night (S06). |
| Walking away | Quest stays Active at its step. Resume hook: Calwen at the sanctuary ("They're still up. They're patient. I'm less so."), or during `S03`–`S04`, Mara at the works ("I'll be here. The ground's not going anywhere. It's the only thing that isn't."). |
| Fail state | None. |
| Co-op | Shared enemies and shared Colour pulse. Per-player standard states, pins, folds, chest, logs, shard carry and choice. Presentation follows each player's own state (fallback: the host's props; each partner still does their own lift, pin, fold, lever and choice). The shard moment plays for the carrying player only; a partner standing near sees the moss brighten and is given no option either. |

## B12. Integration needs

Documented dependencies for a later Systems Engineer. Nothing here is implemented.

| Need | Owner | Minimum viable form |
|---|---|---|
| **Standard prop states** | Art / world state | Each standard prop has states: laid, leaning, risen, lifted-unfolded (cloth on the road), folded (on Calwen's frame), removed. Per player. The causeway roadside set swaps to "removed" on `MR_CAUSEWAY = reset`. |
| **Wraith re-form by condition** | Gameplay | Lowmark drift-site model: a spawn point at each standard re-spawns defeated Wraiths ~25 s after defeat with a ~3 s tell **while** the standard is in `risen` or `lifted-unfolded`; stops when it is `folded`. Live Wraiths are unaffected by the state change and fight to 0 HP. |
| **Pulse-driven re-form** (MBR-E5) | Gameplay | A timed event on the standard (every ~30 s, ~3 s tell) that re-spawns defeated members of the party; re-spawns the Colour only while the standard is `risen`; after the lift, spawns one Wraith per pulse until `folded`. Standard boss telegraph and add-spawn pattern. |
| **Channelled segments with persistence** | Systems | Lift (3), lever (3). Interrupt on hit; segments kept. |
| **Interact sequence with harmless reset** (fold) | Systems | Three fold handles on the cloth prop; correct order advances; wrong order resets with a sound. The seams' inspect text tells which is strongest. Handles inactive until both pins are in. |
| **Loose-log section** | World state | A walkable segment with a slow modifier while unpinned; two pin interactions restore it. |
| **Carry-state object** (the shard) | Systems | As Thornfell's grain sack, without the movement penalty: a held prop and a quest-state flag; not an inventory item; cannot be dropped by a hit. Fallback: Mara walks with the player carrying it in her basket lid and the moment triggers on the player's proximity to Dunstan with Mara beside them. |
| **Scripted presentation event** (`causeway.shard_moss`) | Art / audio / VFX | §B8.1: one moss post's material brightens and fades; a silt-ring decal smooths round an NPC's feet. Per player. No UI. |
| **Keep-watch interaction** | Systems | At the works (crew pins), at the sanctuary and at the platform (dusk). |
| **Use-item-on-NPC or gated option** | Dialogue | Showing the logs and the shard to Ysolde. |
| **Woodcutting interaction** | Skills | Splitting root-knees at a block; pins are a carry-state count, not items. |
| **Agility trigger** | Systems | A ditch jump from the embankment slope back to the road at standard 3; walkable fallback up the slope steps. |
| Creatures | Schema / Gameplay | Banner wraith, bearer, the Risen Colour (elite; internal label only); Reedlurker lurker, snapper (bible §10). |

**New runtime needs: none.** Every item is a standard system, the Lowmark drift-site model, or a standard boss add-spawn pattern.

## B13. Mystery ledger entries

| Mystery | Author truth | Public belief | Player-observable evidence | Plausible wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| **Why the banners rise** `[CAUSEWAY]` | Standing the field's standards up pulled at the imprint left by the last battle (bible §2.3). | The dead are angry about the road. | Oswin's confession; states; Wraiths stop when a standard is folded. | Ghosts protesting; the Memorywardens cursing the road. | Why standing them up woke them. | MR-M4 / MR-M5 (consequence). |
| **The three day-books** | Three columns of the last battle stopped on the day the Memorywardens grounded the field (R08). | Old army paper. | Three bindings, three reckonings, one weather run, three endings. | The armies drowned; the Mire swallowed them. | Whose; which sides; how many; what stopped them. | MR-M4 (R08). |
| **The shard** | A fragment of Memorywarden work that reacts near grief. | A bit of old pot. | Marks pressed before firing; the moss and the silt near Dunstan. | It is a weapon; it identifies Dunstan's mother; it is cursed. | What it is and what it did. | MR-M4 (record), never fully explained. |
| **The Banner That Sank Twice** | A standard from the last battle with two hoist sleeves; the story is a story. | The regiment's honour must be restored if it surfaces. | Two sleeves; Corra's telling; Calwen's refusal to confirm. | It is proof the story is true; it belongs to one side. | Whose regiment. | None (Calwen keeps it unsorted). |

## B14. Open decisions

1. **MD-1 (`[CAUSEWAY]`):** Oswin's confession (`S02`), the choice scene's Oswin and Edris lines (`S06`), the roadside props and `MR_CAUSEWAY` are the only nodes that depend on the causeway cause. The standards, the shard, the chest, the books and the Colour survive any replacement that is still "a present, local reason the field's standards were raised" (bible §3.1).
2. **Dating by weather run [NEW]:** the books share no calendar and are matched by the same run of weather on their last days. **Act II (MR-M4) must date the vestry log the same way** (the same run: rain three days, a hard frost, a thaw, fog two days) so no calendar is ever stated. If the Director prefers a stated date, only the three book texts, `MBR-D6` and the MR-M4 vestry log change.
3. **The two hoist sleeves [NEW]:** the physical sign that lets Corra name the Banner That Sank Twice without anyone confirming it. Text and prop only.
4. **The restored outcome hangs a field standard at Griefwatch:** consistent with "properly honoured" quieting a Wraith (dossier §IX). MR-M5 reads it as one more Wraith wave and one ally line, per the bible.
5. **Corra's fold corner:** Corra always follows and always takes the corner; the flag exists only so MR-M5 can thank her. If the Director would rather she not be on the field at dusk, Calwen takes the corner and the flag is unset.
6. **Level framing (MD-10):** Competent identity; Woodcutting `[GD: low]` with the crew alternative.

## B15. Internal review log

| Finding | Revision |
|---|---|
| Wraiths re-forming forever risked a grind. | Each standard ends its own condition on the third correct fold. The tell is ~3 s and the gap ~25 s, so the work fits between re-forms. |
| Ending the condition risked an un-CDR-1 "the rest vanish". | Folding stops new forms; Wraiths still standing fight on to 0 HP (§B7 rules). |
| Mara's rule (never digs too deep). | She digs to each foot and stops; the chest is levered out of mud the ground had already let go of, and she says so. |
| Calwen's limit (never identifies by faction). | He reads bindings and refuses whose; he will not confirm the Banner That Sank Twice; he keeps the shard unsorted. |
| The records/relics distinction risked a lecture. | Said once by Ysolde, with two objects on her table: she keeps the books and will not touch the shard. |
| The shard moment risked reading as proof (of Dunstan's mother, of magic). | No glow on the shard, no UI, no option; Ysolde files it under "seen", not "so". |
| R08 withholding. | No book names a unit, a side, a number of dead or what stopped them. The weather run dates nothing in a calendar. |
| Oswin risked being a villain. | He confesses without being pushed, says why, and takes the standards off the road himself. Edris's "I asked you to wait" and his "I know" are all the blame the scene carries. |
| The Colour risked a damage race. | The win is bringing the standard down and folding it, not out-damaging re-forms. The pulse is a readable clock with a ~3 s tell. |
| Ranged trivialising the Colour. | Advance closes the platform; pulses re-form out-ranged members; bearers' raise must be interrupted. Valid, bounded. |
| Skill hook. | Woodcutting `[GD: low]` for the pins, with the crew alternative costing a turn. |
| Address. | Edris, Dunstan and Ysolde say "witness" (they saw the reading); Calwen, Oswin, Mara and Corra say "traveller". |
| Hollowfoot (MD-7). | None present. |

---

## Act I cross-check (final review)

| Rule | Check |
|---|---|
| Canon anchors | Edris: her own care account only; "the Mire knows when it's respected" kept as ethics; no unit, age or service; never makes a manifestation a witness. Calwen: never names a side; refuses whose; stores without sorting. Mara: digs to the foot, never under; marks with stones, never names. Lysa: present care only; "making space". Rowan, Sennic, Bran: not in Act I. |
| Evidence rule | Every hold in MR-M1 comes from a keeper or an object they keep; the Wraith and the lullaby are refused as holds on screen. MR-M2's books come from a chest, the cause from a confession, the shard from a dig. No defeated enemy speaks. |
| R08 withholding | No Act I text names a unit, an army, a side, a number of dead, or what stopped the columns. |
| R16 | The stranger's seat is used and never explained. |
| Causeway tagging | Every node naming Oswin's decision or his crews' standing-up is `[CAUSEWAY]` in both files. Oswin is mentioned, not met, in MR-M1. |
| MD-7 | No Hollowfoot encounter in Act I. The Fenward man is a settled non-combatant. Swap notes in §A7.1 and §B7.1. |
| No fail, no soft-lock | Every channel state can be waited out; the cart cannot be lost; wrong holds and wrong folds reset harmlessly; lift, lever and heave progress persists; dusk can always be waited for. |
| No cutscenes | The lullaby, the shard moment and the Colour's rising play under the player camera. |
| Solo / co-op | Solo-clearable; per-player state with fallbacks. |
| Movement reality | Click-to-move; no swimming; deep water non-walkable; ditch shallows slow; every agility trigger has a walkable fallback. |
| Quest items | 2 (`MNS_name_tape`, `MBR_unit_logs`), within the Mire budget of 4. |
| Region flags | `MR_CHANNELS`, `MR_NAME_RECORD`, `MR_BANNERS`, `MR_CAUSEWAY` only. |
| Skills | Melee or ranged in every fight (ranged never required); Hunting and Cooking (MR-M1), Woodcutting (MR-M2), all `[GD: low]` with a time-cost alternative. |
| Defeat model | CDR-1 everywhere. Earth-memory enemies re-form only by condition. No SX. No non-combatant is targetable. |
| Geography | Only bible POIs and dossier places, plus Edris's old station as a sub-site of MP08 (open decision A14.7). Relative placement; MAP VERIFICATION REQUIRED marked. No interregional route. |
| Terminology | No release wording. The Mire is called a milestone only in the status line. |
| Independent review (2026-11-08, Acts I–II reviewer) | 9 defects fixed in place, none high. **Medium:** `MBR_CORRA_CORNER` was read (`MBR-D8.32`, MR-M5) but never set (now set on `MBR-B5.6`); Act I promised `MBR_unit_logs` would be "set beside the vestry log" in MR-M4, which Act II does not do (item, contract and flag rows now say the vestry inspect matches their weather run, possession not required); a throwaway bark named "Col", a Lowmark NPC's first name (Col Dunnock; name dropped). **Low:** §A1 said the beetles were "driven off" (CDR-1 wording; now defeated); Corra's safety was justified by a misreading of bible §2.4 (now rulings §3.1.6, non-combatants untargetable); the Risen Colour's lift could read as closing when the Colour re-forms (now stays open once opened); Dunstan's "Sunday" was a real-world weekday name (now "the week's end"); flag-table ranges cited non-existent `MNS-D10.88` / `MBR-D8.88` (now `.86` / `.87`). **Verified unchanged:** every cited dialogue id exists; flags set/read match between files; step predicates match beats; anchor limits (Edris, Calwen, Mara, Lysa); R08 (no unit, side, count; day numbers are march days, not casualties); CDR-1/2/4 (telegraphs in seconds, solo targets, `[GD]` skill placeholders with time-cost alternatives, no new runtime need); MD-7 swap notes; MAP VERIFICATION REQUIRED on every place table; no Lowmark/Thornfell name collision among the new cast; tables well-formed. |
