# Mire Side Quests — Work and Skills

**Status (2026-11-08):** Authored production content for Creative Director milestone review (Mire bible §12, Batch 3, part B). Five work and skill side quests from `Caelmor_Mire_Narrative_Production_Bible.md` §7.2: **MRS** *Reed Shafts*, **MFT** *A Table for the Wet*, **MFH** *The Ferry Harness*, **MWS** *Weight of the Soil*, **MHG** *The Hushed Granary Key*. Everything here is **[NEW]** unless marked **[CANON]** or **[APPROVED — id]**. Consequential choices the content depends on are marked **[PROPOSAL — DIRECTOR]**. Markdown only: no schema, JSON or C#. Dialogue sits inline in each package (§x.14), as in `Caelmor_Thornfell_Side_Quests_Work_and_Skills.md`, in the node format `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`, with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>` and inspect texts `<CODE>-I<n>`. Voice follows bible §5.3.

**Binding rulings:** `Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 defeat at 0 HP, no yield, retreat or break-off; CDR-2 ranged first-class and never required; CDR-3 the Mire is an internal production milestone of the complete game; CDR-4 standard RPG systems and meaningful skill requirements).

**Sources used:** the Mire bible (binding: §1.1 ground and water, §3 MD-5/MD-7/MD-10/MD-11, §4.2 POIs MP02, MP04–MP06, MP16, MP22, MP26, §5 cast and voice, §7.2–7.3 slate rows and contracts, §9 flags and conventions, §10 families, §11 conventions); `LORE/Regions/Caelmor_Region3_MireOfFallenBanners.md` (dossier: Marshfall's hunters and peat-cutters, Mire reeds, griefroot, lantern moss, bogsedge fern, Bog Hounds, Reedlurkers, Griefbit Beetles, rootcraft, bog-binding, questline 4 *Weight of the Soil*); `LORE/Characters/Caelmor_Characters_Region3_Mire_Of_Fallen_Banners_Anchors (Not Full List).txt` and the Part 4 character ledger rows (Edris, Calwen/Mara, Lysa); `00_ADMIN/Reference/Caelmor_Part3_Mire_Proposal.md` (lantern debt, the Hushed Granary, the Silt hearing, Reedsward rota; adopted by MD-5); `00_ADMIN/Reference/Caelmor_Regional_Source_Process_Mire_Proposal.md` (no local tanning; reclaimed and root wood; battlefield metal is evidence, not feedstock); the Mire main packages `Caelmor_Mire_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and their dialogue files (read for flags, cast voice, Hob's hide, Fenward, Blackwater Landing and the master commissions).

**Scope guard.** The Mire is an internal production milestone of the complete game (CDR-3). Nothing here grows scope. Technical needs are dependencies for the Mire integration handoff (bible §12, Batch 4), never implementations.

---

## 0. Purpose and shared rules

Lowmark taught skills as custody handoffs on a river. Thornfell taught them as listening work in a hard place. The Mire teaches them as **work done for other people on ground that will not hold still**. Every skill here is learned through the Mire's readable system (bible §1.1): the fowler cuts reed only when the stake says the shallows are out of the water; the cook reads smoke and seals crocks against a week of flood; the ferry household rows a fresh pin across a channel that has just turned; the walkway crew drives piles at Slack; the granary keeper weighs sacks against a tally board because the register says "two holds, one name" and a store works the same way.

Exact items, recipes, yields, stats, levels and XP belong to the item, economy and balance passes. **Reed shafts, fen fowl, griefroot and smoked eel are legacy concepts or proposals for the economy pass, not catalog items** (MD-11; dossier §XI status note). Every output is named by what it does, and every material and recipe is listed as an economy-pass dependency (§0.3).

### 0.1 Unlock gates and placement

| Code | Quest | Skills | Core verb (primary first) | Unlock (quest state) | Skill requirement (CDR-4) | Where (bible §4.2) | Length |
|---|---|---|---|---|---|---|---|
| **MRS** | Reed Shafts | Fletching, Ranged, Hunting | **cut**, fletch, shoot, pluck | MR-M1 Completed | **Hunting ~[GD: low]** to start. Fletching and Ranged are taught from any level. | Fowling Meres (MP26), Hob's hide; Marshfall (MP02) | 35–45 min |
| **MFT** | A Table for the Wet | Cooking (with entry Hunting) | **gather**, cook, serve | MR-M1 Completed | None (Cooking is taught). | Fenward Huts (MP05); Marshfall smoke sheds (MP02) | 30–40 min |
| **MFH** | The Ferry Harness | Leatherworking, Woodcutting | **strip**, mend, fit | MR-M1 Completed | **Woodcutting ~[GD: low]** to start. Leatherworking is taught from any level. | Blackwater Landing (MP06) | 30–40 min |
| **MWS** | Weight of the Soil | Woodcutting (light), Melee or Ranged | **repair**, clear, decide | MR-M2 Completed | None. | Marshfall walkways (MP02), Peat Row | 35–45 min |
| **MHG** | The Hushed Granary Key | None required | **find**, weigh, decide | MR-M2 Completed | None. | The Hushed Granary (MP22), Sorrowmere register room (MP01), Rootrest (MP04) | 30–40 min |

All five are optional, solo-clearable, cannot fail, and give no lump quest XP (skill XP comes from actions; bible §11.6). Inactive, Active or Completed only. **No quest items** (bible §9.4: the Mire budget of four is spent by the milestones). Every carried thing is a carry-state prop, a station object, an inspect point, or an ordinary output the economy pass will define.

**Skill requirements (CDR-4).** Bible §13 recommends light level requirements on a few side quests (MRS, MFH, MRH). This file applies them to **MRS** and **MFH** as RuneScape-style **quest-start requirements**: the offer is visible to everyone, and a player below the level is told plainly what to train and where it can be trained anywhere in the game (`MRS-D1.05`, `MFH-D1.06`). The requirement sits on the skill the quest **builds on**, never on the skill it teaches. Inside the quests, every step for a *taught* skill keeps its crew or alternative path (bible §7.2 skill coverage). MRH's requirement is in the Settlements and Combat file. No milestone reads any of these quests as a gate.

**Level framing (MD-10).** MRS, MFT and MFH sit at MR-M1's Competent identity; MWS and MHG at MR-M2's. Exact levels are Gameplay Designer calls.

### 0.2 Skill coverage and how the five feed one another

```text
MRS  Hunting (required): fowling from a hide at dusk flight ──► fen fowl [EM-03] (food) + flight feathers [EM-02]
     Woodcutting-free Fletching: read the stake, cut reed at Slack ──► roll-test, smoke-straighten ──► reed shafts [EM-01]
                                 nock, fit root-wood blunts [EM-04], fletch with heron or fowl feathers ──► fowler's bundle [EM-05]
     Ranged: Hob's bobbing marks, then the dusk flight (alternative: Hob's flight-net, Hunting)
     └─ feathers from the plucking go back to Fletching (CDR-2 loop: Fletching → Ranged → Hunting → Fletching)
MFT  Cooking: smoke eel by smoke colour ──► smoked eel [EM-06]; root-and-fowl stew ──► sealed crocks [EM-07]
     Hunting (entry, optional): one fen fowl at Hob's hide, or Hob's string
MFH  Leatherworking (repair): flex-test trade leather [EM-08], skive, stitch traces, dress with eel oil ──► mended tow harness
     Woodcutting (required): split root-knee [EM-09] ──► shave thole pins to the old pin's gauge
MWS  Woodcutting (light): cut choking roots ──► root wood to Marshfall's rootcrafters [EM-09]
     Bog-binding as ordinary repair: drive piles at Slack, lash fascines (no skill check; crew does the weight)
MHG  None. Weighing sacks against a tally board is an inspect-and-compare task (the register's "two holds" applied to a store).
```

- **Fletching and Ranged (MRS).** The Mire's fowlers make arrows from reed, not wood: a reed shaft is straight, light and hollow, and Marshfall has more reed than it has trees. Hob Merrit teaches the whole loop. **Ranged is never required**: Hob's flight-net (a Hunting throw from the hide) takes the dusk flight for a player who will not shoot, and the practice marks have Hob's own "call the rise" alternative (§0.6). Every encounter in this file accepts melee or ranged.
- **Hunting** is fowling from a hide (MRS) and one optional fowl for the pot (MFT). Combat never grants Hunting recovery; plucking is the recovery phase (economy convention as Lowmark).
- **Cooking** is food that keeps, for named people, through a flood (MFT). The meal comes before any question (bible §5.3 rule 6).
- **Leatherworking** is **repair of imported leather** only (MD-11; source process: no local tanning). The Mire mends what it cannot make.
- **Woodcutting** is reclaimed and root wood (MD-11): drowned root-knees for pins (MFH), choking roots off a walkway (MWS). No standing tree is felled in this file.
- **No Mining or Smithing** (MD-11). The buckles on the ferry harness are reused trade iron; nothing is forged.

### 0.3 Economy-pass dependencies (MD-11)

Every material and recipe below is a **dependency**, not an item. **EM-01 to EM-11 are this file's proposal labels for the economy pass, not catalog ids or item names**; the working name is what the quest text calls it until the economy pass derives a state. **Bows:** Hob's spare fowling bow (lent as a carry-state object in MRS, never an inventory reward) and the "proper reed bow" of his Act III commission are item-name proposals only; weapon catalog, stats and recipes stay with the economy and item passes (CDR-2; rulings §3.4).

| Id | Working name in this file | Dossier or bible concept | Used by | Nearest approved state | What the economy pass must decide |
|---|---|---|---|---|---|
| **EM-01** | **reed shafts** | Mire reeds (dossier §X); "reed-shafted fowling arrows" (MD-11) | MRS (cut, then input) | Ordinary wood is the nearest shaft state; reed is not wood | Whether reed is a shaft material in its own right, its gathering node (a reed stand gated by channel state) and processing (roll-test reject rate, smoke-straightening). |
| **EM-02** | **flight feathers** (heron moult, fen fowl) | — | MRS (input and output), loop back to Fletching | None (Lowmark's fowl is food-only; Thornfell EC-08 open) | A feather output from fowl plucking; whether moulted heron feathers are a gathered item or Hob's stock only. |
| **EM-03** | **fen fowl** | Legacy concept (MD-11) | MRS (output), MFT (input, optional) | Edible Hunting output (functional relationship pending catalog) | Food relationship; feather and down outputs from plucking. |
| **EM-04** | **root-wood blunts** (fowling heads) | Rootcraft (dossier §XVII) | MRS (input from Hob's stock) | Ordinary wood | A wooden fowling head, so no metal arrowhead is needed (the Mire has no forge; MD-11). |
| **EM-05** | **fowler's bundle** (reed fowling arrows) | — | MRS (craft output, reward) | None | Arrow item, stats and stack; the name is a functional proposal. |
| **EM-06** | **smoked eel** | Bible §7.2 (MFT systems link) | MFT (craft output); Act I table flavour | None | A preserved store food. Eels come from Marshfall's smoke sheds (trade, no new node). |
| **EM-07** | **root-and-fowl stew** (sealed crock) | Bible §7.2 | MFT (craft output); Act III `S01b_pot` uses the same recipe | None | An eat-now food and a sealed keeping form (peat-wax seal, from Fenward's stock). |
| **EM-08** | **trade leather** | Imports (dossier §XVII); source process: no local tanning | MFH (input from the Landing's store) | Vegetable-tanned leather (approved Lowmark state) | Whether imported leather is that state; repair recipes (trace, strap) that consume it. No route to its origin is stated (FT-03). |
| **EM-09** | **root wood** (root-knees, cleared roots) | Rootcraft; reclaimed wood (MD-11) | MFH (thole pins), MWS (cleared roots) | Ordinary wood | A root-wood state or ordinary wood from a reclaimed node; pin recipe. |
| **EM-10** | **fen roots** and **griefroot** | Griefroot (dossier §X; legacy, MD-11) | MFT (input) | None | Fen roots as a food; griefroot stays Lysa's medicinal addition from her own stock and is never harvested by the player here. |
| **EM-11** | **grain sacks** (the Hushed Granary store) | Imports (dossier: grain) | MHG (weighed, never taken) | Lowmark grain staple dependency | Nothing in MHG creates or consumes grain; the sacks are station props. No route is stated (FT-03). |

**Recipe dependencies** (all owned by the item and economy passes): reed shaft cutting, roll-test and smoke-straightening, nocking, blunt-fitting and fletching (MRS); eel smoking, stew, crock sealing (MFT); trace cutting, skiving, stitching and oil-dressing for repair, thole-pin shaving (MFH); root cutting (MWS).

### 0.4 Commission givers established

The Mire's master commissions are gated by `MR_STANDING` and authored in Act III §E.10 (who offers what, where, and the offer line). This file establishes the craft relationship behind one of them and two standing stations.

| Giver | Craft | Established by | Flag | What they say they will one day ask for |
|---|---|---|---|---|
| **Hob Merrit** [NEW, bible §5.2] | Fowling, Fletching, Ranged | MRS completion | `MRS_HOB_BENCH` | "A proper reed bow. Root-wood belly, horn tips, the lot. When you can sit in a hide till your feet forget you." (Act III §E.10 *Fowler's reed bow and quiver*; its variant line reads *Reed Shafts* Completed.) |
| **Gwenna Tolley** [NEW] | Ferry repair (leather, pins) | MFH completion | `MFH_TOLLEY_BENCH` | A public repair bench at Blackwater Landing (harness and pin repair station). No master commission is proposed. |
| **Lysa Thornettle** [CANON anchor] | Care cooking | MFT completion | — | The Fenward hearth becomes a public Cooking station. Lysa is not a commission giver (ledger: present care only). |

### 0.5 Distinctness check

| Quest | Core verb | Physical problem | Wonder or unease | Human choice with a cost |
|---|---|---|---|---|
| MRS | cut, fletch, shoot, pluck | Cut reed only at Slack; roll-test and smoke-straighten shafts; shoot bobbing marks on the rise; sit a hide through the dusk flight | **Wonder:** a marrow heron lands on the mere's depth stake and every bird on the water goes quiet; it lifts at the loose, every time | None (contract: no choice) |
| MFT | gather, cook, serve | Ask each person what they can eat; smoke eel by the colour of the smoke; label and seal crocks; lift them above the flood stage before dusk | **Unease:** a bogsedge fern on the sill wilts all at once while an old woman says her husband's name | None (contract: no choice) |
| MFH | strip, mend, fit | Flex-test stored leather for rot; stitch traces; split and shave pins to an old pin's gauge; row a loaded punt across a channel that has just turned | **Wonder:** mid-channel the water goes flat as glass for a boat's length and the punt runs on for three strokes with nobody rowing | None (contract: no choice) |
| MWS | repair, clear, decide | Drive piles at Slack; cut roots off a walkway; find a stone the roots grew round in a perfect ring and never touched | **Unease:** the ring of roots | Lift the marker to Calwen and run the walkway straight, or leave it and walk round it forever |
| MHG | find, weigh, decide | Read a silt apron for prints; open a flood hatch at Slack; weigh sacks against a tally board; follow a balm to a frightened old man | **Unease:** the granary at night, with the old keeper's lantern moving inside a locked store | Who keeps the key, and how many hands it needs |

None repeats a milestone verb (MR-M1 match records and walk a shifting route; MR-M2 recover and retire; MR-M3 prepare and cross; MR-M4 drain and light; MR-M5 read the count and hold the gap). MFH was checked against MR-M3: there the player mends Rowan's tow harness and **hauls** the boat in it at the shoal; here the player mends a ferry household's harness and pins and **rows** while a grandson hauls from the tow path. The wonder moments were checked against the mains: no moss brightening (MR-M2), no soundless bell (MR-M3), no glass lit by nothing (MR-M4), no standards leaning (MR-M5), no lullaby (MR-M1).

### 0.6 Shared rules for all five packages

- **Crew or alternative path (every taught-skill step).** Each taught-skill step lists its alternative in its beat text. The alternative is still play: the player does the reading, timing or choosing while someone else does the strength or the shot. Choosing it may cost a turn of the presentation hour (keep watch), a share of output or a coin share. It never costs the quest. Skill XP is lower on an alternative (balance pass).
- **Quest-start skill requirements** (MRS, MFH only) gate the offer's accept option, never a step. The offer's decline line says what to train. Requirements can be met by ordinary training anywhere.
- **Channel states and keep watch** (bible §9.2; Lowmark presentation hour). Every crossing or reed stand that matters has a stake. A step may pin a crossing's state; otherwise the player keeps watch at a marked bench until the next turn. Waiting is always available.
- **Agility triggers** are optional shortcuts, each with a walkable fallback named in its place table.
- **Every enemy is defeated at 0 HP** (CDR-1). Bog Hounds, Reedlurkers and Griefbit Beetles are wildlife or vermin; none yields, flees or breaks off. Every encounter accepts melee or ranged (CDR-2); none requires ranged. Fen fowl, herons and fenny does are Hunting fauna or scenery that fight only if provoked and are not counted as an encounter family (bible §10).
- **Evidence rule** (bible §11.3). Nothing in these quests is evidence for a revelation. The heron, the wilting fern, the slack seam, the ring of roots and the lantern in the granary prove nothing and identify nobody. The Memorywarden marker in MWS is an object with office marks and no name; it identifies nobody.
- **No failure.** Inactive / Active / Completed only. Death respawns at the quest's named safe point with step and flags intact. Logout restores the last persisted step; completed channel segments persist; a dropped carry-state object returns to its source. Walking away keeps the quest Active with the resume hook named in each package.
- **Time.** No calendar dates anywhere. Days are presentation-hour turns; the past is dated by weather ("the night of the hard frost") or by bell-nights, never by a date or a year (FT-02).
- **Co-op.** Independent instances; shared world creatures give credit to each participant on that step; quest-state props and NPC placement are per player (Lowmark per-player prop pattern; fallback: the host's state drives props, each player's own state drives dialogue).
- **Address.** NPCs who saw MR-M1's readings say "witness" (bible §5.3 rule 8); everyone else says "traveller". The register and the seat are never explained.
- **MD-7 (Hollowfoot).** No Hollowfoot enemy appears anywhere in this file. MFT includes Jory Wick (Act III cast), a settled Hollowfoot man in Lysa's care, as a **non-combatant, never targetable** NPC, tagged `[MD-7]`. Each package carries an MD-7 swap note.
- **`[CAUSEWAY]`.** Any node naming Oswin Garvey's causeway decision is tagged (bible §3.1). In this file: MWS only (one Dunstan line).

### 0.7 Flags other packages read

All flags here are quest-local (`MRS_…`, `MFT_…`, `MFH_…`, `MWS_…`, `MHG_…`). **No `MR_` region flag is set by this file.**

| Flag or state | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| **MRS Completed** (quest state) | — | MRS `S07_bench` | **Act III §E.10** Hob's commission variant ("That heron's still out there. Laughing.") | Hob remembers the heron that got away (MRS.5). Never a gate. |
| `MRS_HERON` | loosed / held | MRS `S06_heron` | Hob barks; Act III commission line (request: optional second variant) | Whether the player shot at the heron. Flavour only; not an outcome choice. |
| `MRS_HOB_BENCH` | bool | MRS completion | Act III §E.10 (Hob as commission giver) | Hob's hide opens as a public fowling station. |
| **MFT Completed** (quest state) | — | MFT `S06_table` | **Act III `S01b_pot`** (`MBL-D2b.21`: Lysa asks for "the one you made for the wet") | Flavour only. Set on the quest's completion event, nothing else. |
| `MFT_CROCKS` | bool (always true on completion) | MFT `S04_crocks` | Fenward barks | The labelled crock shelf prop at the huts. |
| `MFH_TOLLEY_BENCH` | bool | MFH completion | Blackwater Landing station; Act II L6 (request: optional ferry-row bark) | Gwenna's repair bench. |
| `MWS_MARKER` | lifted / left | MWS `S06_decide` | Calwen barks; Marshfall walkway props; Act III circle (request: none required) | Whether the marker went to Calwen's unsorted chest or stayed under a dog-legged walkway. |
| `MHG_KEY` | shared / passed / register | MHG `S06_decide` | Granary props and barks; Sorrowmere register room prop with `register` | Who keeps the Hushed Granary key. |
| *(read)* `MNS_BROTH` | self / hob | MR-M1 | MFT `MFT-D1.03` | Lysa: "You cooked on the road once. Do it for twelve." with `self` (Act I §A9.2 request honoured). |
| *(read)* `MR_NAME_RECORD` | amended / qualified | MR-M1 | MWS (Dunstan's lines) | Bible §9.1 row "Read by *Weight of the Soil*". |
| *(read)* `MR_CHANNELS` | bool | MR-M1 | All stake inspects | Always true after MR-M1, which gates every quest here. |
| *(read)* `MR_BANNERS` | retired / restored | MR-M2 | MWS (one Calwen line) | Flavour only. |
| *(read)* `MR_WARDEN_RECORD` | set or unset | MR-M4 | MWS (one optional Ysolde line about office marks) | Only if MR-M4 is Completed; MWS never requires it. |

---

## MRS — Reed Shafts

### MRS.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `mire.side.reed_shafts` |
| Type | Skill introduction (Fletching, Ranged, Hunting). Bible §7.2 row; MD-11 skills. |
| Unlock | MR-M1 Completed. Offered at Hob's hide on the Fowling Meres edge (Act I place M3) when the player passes or comes for fowl (`MRS-B0`); dialogue `MRS-D1`. |
| Skill requirement | **Hunting ~[GD: low]** to accept (CDR-4). Fletching and Ranged are taught from any level. |
| Resume hook | Hob at the hide bench: `MRS-D1.00` "Still here. Still swearing at herons. Where were we?" pins the step. |
| Skills | Fletching (required: cutting, roll-test, fletching), Ranged (taught; alternative path), Hunting (required at start; the dusk flight), Melee or Ranged (one Reedlurker) |
| Combat share | ~10% (one Reedlurker at the retrieve) |
| Cameo | None. Hob carries the quest. |
| Choice | None (contract). One flavour flag (`MRS_HERON`). |
| Unlocks | Hob's hide as a public fowling station; reed stands at the meres as a gathering opportunity (EM-01 dependent); Hob as the craft relationship behind his Act III master commission |
| **Anchor** (§7.1) | Marshfall hunters (Hob Merrit, fowler and fletcher). |
| **World-truth row** | None (present-day work). |
| **Revelation role** | Self-contained. Plants nothing. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No choice; `MRS_HERON` is flavour. No fail path: a reed cut in the wrong state cannot be cut (the stand is under water), a shaft that fails the roll goes to Hob's thatch pile, a missed mark is shot again, a missed bird lands and is shot again or netted. |
| **Combat compliance** | One Reedlurker (MRS-E1) defeated at 0 HP. Fen fowl are Hunting fauna (defeated at 0 HP when hunted; never hostile). Melee or ranged both finish MRS-E1; nothing requires ranged. No SX. |

**In one paragraph.** Hob Merrit fowls the Marshfall meres the old way: reed shafts, root-wood blunts, heron feathers he picks up off the water, and patience in a hide. His shafts are running out and his hands are slower than they were, and he would rather teach someone than buy arrows "made by people who've never sat still in their lives". The good reed grows in the feeder channel, where the water moves; at Running it stands under water and at Slack the shallows come out and a person can wade to it. The player reads the stake, waits for Slack, picks the stand by its even nodes and cuts a bundle. Back at Hob's bench every reed is rolled on a flat board: a true one rolls without a wobble, a bent one is warmed over the smoke-shed coals and pressed straight, and some go on the thatch pile. The player nocks, fits root-wood blunts, and fletches with three feathers each. Then Hob sets reed floats bobbing on the mere and teaches the rise: loose when the mark lifts, not when it drops. At dusk they sit in the hide while the flight comes in. The player takes three fen fowl, by bow or by Hob's flight-net, wades for them past a Reedlurker, and plucks them at the bench: flight feathers in one basket for the next bundle, down in another for the Fenward huts. Just before dark a marrow heron lands on the mere's own depth stake and every bird on the water goes quiet.

### MRS.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Shooting contest at Marshfall. | Rejected. Ranged-only and talk-light; CDR-2 forbids a quest that requires ranged. |
| B. Buy a bow, kill fowl, done. | Rejected. No Fletching, no reading of the Mire's system, no reason to be in the Mire. |
| **C. Read the stake → cut reed at Slack → roll-test and straighten → fletch → shoot the rise (or net) → the dusk flight from the hide → pluck, feathers back to Fletching** | **Selected.** A complete Fletching → Ranged → Hunting → Fletching loop (CDR-2) taught through the Mire's readable system, with a non-ranged path at every shot. |

| Element | Source | Status |
|---|---|---|
| Marshfall: hunters, gatherers, peat-cutters; fog rolls in unpredictably | Dossier §VII.2 | [CANON] |
| Mire reeds in shallow pools and trench remains | Dossier §X | [CANON] |
| Marrow herons: tall, pale, nest on higher ridges, feed on fish; ominous reputation near ruins | Dossier §X | [CANON] |
| Reedlurkers: amphibious ambushers in shallows | Dossier §IX; bible §10 | [CANON] |
| Fowling Meres (MP26); Hob Merrit, fowler and fletcher | Bible §4.2, §5.2 | [NEW] |
| Hob's hide, his string of fen fowl, his swearing at herons | Act I §A (M3), `MNS-B5` | [NEW], consistent |
| Reed shafts, root-wood blunts, the roll-test, smoke-straightening | This package | [NEW]; economy proposals (EM-01, EM-04) |

### MRS.3 The places [MAP VERIFICATION REQUIRED]

The Fowling Meres lie on Marshfall Edge between Marshfall's stilt houses and the forest line (relative only). Hob's hide is the one Act I uses (M3).

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **F1. Hob's hide** | Hook, bench, dusk flight | A reed hide on a mere's edge: a low reed wall with a bench behind it and a slot to look through. A net on pegs. Hob's string of fen fowl. A flat **rolling board** (a planed plank, polished by use) and a **feather basket** and a **down basket**. A smoke-pot of peat embers for the straightening. A watch bench (keep watch). | — |
| **F2. The mere** | Marks; the flight | Open water ringed by reed. Herons in the far shallows. A **depth stake** in the mere, painted in the three bands, a little crooked. Hob's **reed floats** (marks) tethered on lines. | Wading shallows at the edge; deep water is non-walkable. |
| **F3. The feeder channel** | Reed stands | A narrow channel feeding the mere, with its own **stake** at its mouth. Three reed stands along it (S1 still water, soft and bent; S2 the channel's bend, mixed; S3 the channel's throat where water moves, hard and straight). At Running the throat stand is under water to the heads; at Slack the shallows come out. | Shallows walkable at Slack only (state toggle). **Agility trigger:** jump the channel at the bend (shortcut). **Walkable fallback:** the plank at the mere end. |
| **F4. The retrieve shallows** | Retrieve; MRS-E1 | Knee-deep water where the shot fowl drift in. Reeds ripple where a Reedlurker waits. | Wading. |
| **F5. Marshfall smoke shed** | Optional | Where Hob's household smokes eel; the down basket goes here for Fenward (on the way, not a step). | — |

### MRS.4 Beats

**Beat 0 — The Marshfall Way (`S00_offer`).** *Objective: Talk to the fowler at the meres.* `MRS-D1`. Hob is in the hide swearing at a heron. His shafts are down to a handful. A player below the Hunting requirement gets `MRS-D1.05` (what to train; any Hunting counts) and the offer stays open.

**Beat 1 — Read the Channel (`S01_stake`).** *Objective: Find out when the good reed can be cut.* Hob points at the feeder channel: "The good stand's in the throat. It's under now. Read the stake." Inspect the feeder stake: with `MR_CHANNELS`, the inspect gives the state (*"Water at the pale band. Running."*). Hob: "Then it's under. Sit." Keep watch at the hide bench until the channel turns Slack (quest-pinned turn on keep watch; one turn). Teaches that the stake governs work as well as travel.

**Beat 2 — Cut the Bundle (`S02_cut`).** *Objective: Cut twelve reeds from the good stand.* Wade the channel at Slack. Inspect the three stands (`MRS-I2`–`I4`): the still-water stand is soft and bends under a thumb; the bend stand is half and half; the throat stand has **evenly spaced nodes** and stands straight in the moving water. Cutting is a gathering interaction (~2 s each). Reeds cut from the soft stand can be cut but Hob throws them on the thatch pile at Beat 3 (no penalty; the player cuts more). Twelve throat reeds complete the step. Carry-state "a reed bundle".

**Beat 3 — True or Thatch (`S03_true`).** *Objective: Test and straighten the shafts.* At the bench:

1. **Roll** each shaft on the rolling board (interaction, ~1 s): a true shaft rolls flat and quiet; a bent one wobbles and taps the board (visible bounce and a dry tick). Of twelve throat reeds, eight roll true, three wobble, one splits (authored mix).
2. **Warm and press** each wobbler over the smoke-pot (channelled, ~3 s) and roll it again: two come true, one does not and goes on the thatch pile (`MRS-B2.04`).
3. Result: ten shafts. Fletching XP per roll and per straightening.

**Beat 4 — Fletch (`S04_fletch`).** *Objective: Fletch a bundle.* Three short interactions per arrow, done as a batch of ten (one channelled interaction with three visible stages, ~6 s): **nock** (cut the nock just above a node, where the reed is strongest), **fit a blunt** (push a root-wood blunt from Hob's box onto the head end, bind with reed thread), **fletch** (three feathers from Hob's feather basket, bound and glued with eel-skin glue from the smoke shed). Output: a **fowler's bundle** (EM-05). Hob's line on feathers sets up the loop: "Heron's best. Heron drops them on the water for free. Only kind thing it ever does."

**Beat 5 — The Rise (`S05_marks`).** *Objective: Learn to loose on the rise.* Hob sets four reed floats bobbing on lines in the mere (F2). Each float lifts on the small swell and drops. The tell is visual: the float's tip tilts up as it lifts (~0.8 s) and settles. A shot loosed during the lift hits; a shot loosed on the drop lands short. Four hits complete the step (misses cost nothing but an arrow; Hob hands back shafts that land in the shallows). Ranged XP per hit.

**Alternative path (no ranged weapon, or the player chooses):** "Show me the net." Hob teaches the flight-net instead: the player watches the floats and calls **now** on each rise (four correct calls; a wrong call is just "Not yet."), which is the same timing the net throw uses at dusk. Hunting XP for the calls.

**Beat 6 — The Dusk Flight (`S06_flight`).** *Objective: Take three fen fowl from the hide.* Keep watch at the hide bench until dusk (the step pins dusk on keep watch). The flight comes in on a fixed script while the player is in the hide volume: three waves of fen fowl drop onto the mere, settle, and swim along the reed edge.

- **Shoot:** from the hide slot, with any ranged weapon and the fowler's bundle (or any arrows). A bird on the water is a Hunting target; a hit is a take. Misses lift that bird and it lands again further along within ~10 s.
- **Net:** Hob's flight-net (a Hunting throw interaction from the hide's front, ~1.5 s wind-up) at a bird that swims inside the marked throw arc. The timing is the rise from Beat 5: throw as the swell lifts the bird.
- Three takes complete the sub-objective.

**The retrieve:** the shot or netted fowl drift into the retrieve shallows (F4). Wading for them triggers **MRS-E1** (one Reedlurker). Hob, from the hide: "Reeds are moving. That's not wind."

**The heron (`S06_heron`, inside the step; MRS.5).** As the last bird is retrieved, a marrow heron lands on the mere's depth stake. Every bird on the water goes quiet. Hob: "Don't." The player may loose at it (ranged weapon equipped) or not. Either way it lifts at the moment of the loose, or, if the player holds, after a long breath, and every fowl on the mere lifts with it, turns once over the hide and comes down again. Sets `MRS_HERON = loosed / held`. No penalty either way; the heron is never a target that can be hit (it lifts before any projectile arrives; not a combat creature).

**Beat 7 — Pluck and the Bench (`S07_bench`).** *Objective: Pluck the fowl at Hob's bench.* Three plucking interactions (~3 s each; Hunting recovery). Flight feathers go in the **feather basket** (they feed the next bundle: EM-02 back to Fletching), down in the **down basket** ("Fenward. Lysa's lot sleep cold."). Hob keeps one bird, gives the player two (EM-03), and gives the player the rest of the bundle. `MRS-D5`. Quest Completed.

### MRS.5 The heron (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Landing** | A marrow heron, tall and pale, glides in low over the reeds and lands on the top of the mere's depth stake, which tilts a little under it. |
| 0–3 s | **The quiet** | Every fen fowl on the water stops calling and stops swimming. The reed hiss and a far frog continue. |
| 3–6 s | **Hob** | Hob, very quietly: "Don't." (`MRS-B4.01`). If the player has a ranged weapon drawn, an optional loose prompt is available. |
| On loose, or 10 s | **Lift** | The heron opens its wings and lifts in the same instant the string looses (or at 10 s if the player holds). The arrow passes under it and lands in the mere. Every fowl on the water lifts with it, turns once in a wide ring over the hide, and settles again where it was. |
| After | **Hob** | Loosed: "Twenty years. It's never once let me." Held: "Good. It'd only have laughed." |
| UI | No objective change until the last retrieve completes. |
| Meaning | None stated. The heron is a bird; the fowl follow a big bird. It proves nothing. Act III remembers it as "the heron that got away". |

### MRS.6 Encounters and hazards

Tuned for MR-M1's Competent identity (MD-10).

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MRS-E1** | 1 × Reedlurker (lurker) | Retrieve shallows (F4), on the first retrieve wade | Ambusher; waits submerged beside the floating fowl and lunges at a wading player | **Lunge:** reeds ripple outward from its spot (~1.2 s, the family's MR-M2 length), then a straight lunge (step aside). **Grab:** if the lunge connects, a short hold (~1.5 s) the player breaks by attacking | Required on first retrieve (contract: "one Reedlurker"). Melee in the shallows or ranged from the bank both finish it | 30–45 s; low damage |
| **MRS-H1** | Deep water | Mere beyond the retrieve marker | Non-walkable boundary | Water darkens past a line of reed floats | Keeps the retrieve on the shallows | None; the player cannot enter it |

**Rules.** Fen fowl and the heron are not encounters. Combat drops nothing that advances the quest. **Death:** respawn at Hob's hide; fowl already taken stay taken; the Reedlurker resets to its spot.

### MRS.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the fowler at the meres. | `MRS-D1` accept (Hunting ~[GD: low]) | Yes | Below the requirement: `MRS-D1.05`, offer re-available |
| `S01_stake` | Find out when the good reed can be cut. | Feeder stake inspected + keep watch to Slack | Yes | F3 shallows toggle walkable at Slack |
| `S02_cut` | Cut twelve reeds from the good stand. | 12 `cut_reed` at the throat stand (S3) | Yes | Soft-stand reeds allowed, rejected later |
| `S03_true` | Test and straighten the shafts. | All cut reeds rolled; wobblers warmed and re-rolled | Yes | Authored 8/3/1 mix for throat reeds |
| `S04_fletch` | Fletch a bundle. | `fletch_batch` channel complete | Yes | Output EM-05 |
| `S05_marks` | Learn to loose on the rise. | 4 hits **or** 4 correct `call_rise` | Yes | Sets `MRS_NET` on the call path |
| `S06_flight` | Take three fen fowl from the hide. | 3 takes (shot or netted) + 3 retrieves + MRS-E1 defeated | Yes | Dusk pinned on keep watch; heron moment sets `MRS_HERON` |
| `S07_bench` | Pluck the fowl at Hob's bench. | 3 `pluck` + `MRS-D5` end | Yes | Sets `MRS_HOB_BENCH`; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `MRS_NET` | `S05` call path | `S06` (net shown first); Hob barks |
| `MRS_HERON` = loosed / held | `S06` heron moment | `MRS-D5.03`; Hob's post-quest barks; Act III commission (request, optional) |
| `MRS_HOB_BENCH` | `S07` | Public fowling station; Act III §E.10 |

### MRS.8 Choices and consequences

None. The contract row is "No choice". `MRS_HERON` changes one Hob line and one bark.

### MRS.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| **Fowler's bundle** | Item (EM-05) | The arrows the player fletched, less those spent. Item pass defines them. |
| Two fen fowl | Food (EM-03) | Hob keeps one. |
| **Reading reed** | Knowledge | Reed stands across the Mire become inspectable: *"Even nodes. Moving water. Shaft reed."* / *"Soft. Thatch."* |
| Hob's hide | Access | Public fowling station: keep watch to dusk, shoot or net the flight, pluck at the bench. |
| Hob as craft relationship | Standing | Behind his Act III master commission (`MRS_HOB_BENCH`). |
| Fletching, Ranged, Hunting, Melee XP | Action XP only | No lump quest XP. |

### MRS.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Below the Hunting requirement | Offer visible; accept option greyed with `MRS-D1.05`. |
| Tries to cut at Running | The throat stand is under water; the cut prompt reads "Under. Wait for the turn." |
| Shafts all fail | Cannot happen (authored mix); a player who cut only soft reed cuts again (the channel stays pinned Slack for this step). |
| No ranged weapon | Net path at Beats 5 and 6. Hob also lends his spare fowling bow on request (`MRS-D3.10`), returned at `S07`. |
| Death | Respawn at the hide; takes and retrieves persist. |
| Logout | Last step restored; the reed bundle returns to the channel bank as a pile to pick up. |
| Walking away | Stays Active; resume hook at Hob. |
| Co-op | Each player cuts, fletches and takes their own. Fowl in the flight are per-player scripted spawns. The heron moment plays per player. |

### MRS.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Reed stand gated by channel state | Systems (N-1 channel schedule) | Walkable shallows and gather node enabled only at Slack; quest pin as fallback (bible §11.2 N-1). |
| Roll-test station with authored results | Systems | Interaction on the rolling board that plays one of two results per shaft from an authored list. |
| Bobbing marks with a lift tell | Gameplay / VFX | Floats on a looping bob animation; a hit volume active during the lift window only. |
| Flight-net throw | Systems | A Hunting interaction with an arc volume and a timing window keyed to the bob loop; same timing as the marks. |
| Scripted dusk flight | Systems / AI | Three spawn waves of fen fowl on keep-watch-to-dusk while in the hide volume. |
| Heron moment | Animation / Systems | Scripted bird on the stake; lift triggered by the player's loose or a 10 s timer; flock lift-and-settle. Not targetable. |
| Carry-state reed bundle | Systems | Lowmark carry-state pattern. |

### MRS.12 Economy dependencies

EM-01 reed shafts, EM-02 flight feathers, EM-03 fen fowl, EM-04 root-wood blunts, EM-05 fowler's bundle. Until the economy pass derives them, the bundle is granted as ordinary arrows of the nearest approved type and the fowl as the nearest approved food.

### MRS.13 Mystery ledger entry

None. The heron is a bird.

### MRS.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Hob Merrit** [NEW, bible §5.2], Marshfall fowler and fletcher | Reed, fowl, feathers, the meres' stakes; every heron on the meres "by face". | Anything about the war he will talk about. | Cheerful, patient, swears at herons. Calls the player "traveller" or, after MR-M1, "witness" if he was at the table (he was not; "traveller"). Pronoun: he (Act I usage). |

**Offer** (`MRS-D1`, step `S00_offer`)

```
MRS-D1.00 [quest Active, returning] HOB: "Still here. Still swearing at herons. Where were we?" (pins step)  → end
MRS-D1.01 HOB: (to the mere, not the player) "Go on. Take it. You always do." (a heron lifts away with a fish) "...Thief."
MRS-D1.02 HOB: "Traveller. You've the look of someone who came for fowl. I've four left on the string and nine arrows in the quiver."
MRS-D1.03 HOB: "Nine. I used to cut a hundred a season. Hands are slower. Eyes are fine. Eyes are the important part."
  > "I can cut reed for you."                                        → MRS-D1.04
  > "Why not buy arrows?"                                            → MRS-D1.08
  > "What's wrong with herons?"                                      → MRS-D1.10
MRS-D1.04 HOB: "Can you sit still? That's the whole trade. Cutting's the easy bit."
  > [Hunting below ~[GD: low]] "I've never hunted anything."         → MRS-D1.05
  > [Hunting ~[GD: low]] "I can sit still."                          → MRS-D1.06
MRS-D1.05 HOB: "Then go and hunt something first. Anything. Hares, fowl, a boar if you're daft. Come back when you know what waiting feels like. I'll still be here. I'm always here."   → end (offer stays open)
MRS-D1.06 HOB: "Good. I'll teach you the Marshfall way. Reed shafts, wood blunts, heron feathers. No iron in it anywhere."
MRS-D1.07 HOB: "First thing. The good reed's in the throat of that channel. Go and read the stake."   {event: accept → S01_stake}
MRS-D1.08 HOB: "Bought arrows are made by people who've never sat still in their lives. They fly like it."   → MRS-D1 options
MRS-D1.10 HOB: "Nothing. Beautiful birds. They eat my fish, scare my fowl and stand on my stake." (beat) "And they drop their feathers on the water for free. Only kind thing they ever do."   → MRS-D1 options
```

**The stake** (`MRS-D2`, at the feeder stake)

```
MRS-D2.01 [MR_CHANNELS] HOB: (calling across) "What's it say?"
  > "Pale band. Running."                                            → MRS-D2.02
  > "I don't know."                                                  → MRS-D2.03
MRS-D2.02 HOB: "Then the good stand's under. Sit. It'll turn."   → MRS-D2.04
MRS-D2.03 HOB: "You walked the causeway and you don't know? Water at the pale band. It's running. The good reed's under it." (beat) "Sit."   → MRS-D2.04
MRS-D2.04 HOB: "Reed's like people. The ones that grow where the water moves come out straight."   {event: keep watch enabled}
```

**Hob's barks while cutting and testing**

| Id | Trigger | Line |
|---|---|---|
| MRS-B1.01 | Slack reached | "There. Shallows are out. Throat stand. Look at the knots in it." |
| MRS-B1.02 | Inspect soft stand | "That's thatch. Bends if you look at it." |
| MRS-B1.03 | First throat reed cut | "Even knots. That's a shaft." |
| MRS-B1.04 | Twelfth cut | "That'll do. Don't be greedy, the stand's got to come back." |
| MRS-B2.01 | First true roll | "Hear that? Nothing. That's what true sounds like." |
| MRS-B2.02 | First wobble | "Tick, tick. Bent. Warm it." |
| MRS-B2.03 | Wobbler comes true | "There. Reed remembers straight if you remind it." |
| MRS-B2.04 | Wobbler fails | "Thatch. Somebody's roof'll thank you." |
| MRS-B2.05 | Soft-stand reed rolled | "That's from the still water. I can see it from here. Thatch." |

**Fletching** (`MRS-D3`, at the bench)

```
MRS-D3.01 HOB: "Nock above a knot. It's strongest there. Blunt on the other end, bind it with reed thread."
MRS-D3.02 HOB: "No iron heads. We're shooting birds, not doors. A blunt knocks a fowl over and doesn't spoil the meat."
MRS-D3.03 HOB: "Three feathers. Heron's best. Glue's eel skin, from the smoke shed. It smells. So will you."
  > "Where do the feathers come from?"                               → MRS-D3.04
  > [no ranged weapon] "I've nothing to shoot them from."            → MRS-D3.10
  > "Show me."                                                       → end
MRS-D3.04 HOB: "Heron drops them. And the fowl you pluck. Every bird you take gives you feathers for the next lot of arrows. That's the trade going round."   → MRS-D3 options
MRS-D3.10 HOB: "Borrow mine. The spare. Root-wood belly, horn at the tips. It's older than you and it's never once hit a heron."   {lend Hob's spare fowling bow (carry-state, returned at S07)}   → MRS-D3 options
```

**The rise** (`MRS-D4`, at the marks)

```
MRS-D4.01 HOB: "Floats. Watch one. Up, down. Up, down."
MRS-D4.02 HOB: "A bird on the water does that. Loose as it comes up, not as it drops. On the drop you'll put it under."
  > "Show me the net instead."                                       → MRS-D4.10
  > (shoot)                                                          → end
MRS-D4.10 HOB: "Net's the same timing. You watch, you call 'now' on the rise. I'll tell you when you're wrong. I enjoy that."   {set MRS_NET}   → end
```

| Id | Trigger | Line |
|---|---|---|
| MRS-B3.01 | Hit on the rise | "There." |
| MRS-B3.02 | Shot on the drop | "Under it. Up, not down." |
| MRS-B3.03 | Correct call (net path) | "Now. Yes." |
| MRS-B3.04 | Wrong call | "Not yet." |
| MRS-B3.05 | Four done | "Dusk, then. Sit in the hide. Don't fidget. Fowl can hear a fidget." |

**The flight**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MRS-B4.00 | Dusk, first wave lands | HOB (whisper) | "Let them settle. Let them think it's theirs." |
| MRS-B4.02 | First take | HOB | "Good. One." |
| MRS-B4.03 | Miss | HOB | "It'll land again. They always think it was the wind." |
| MRS-B4.04 | First retrieve wade | HOB | "Reeds are moving. That's not wind." |
| MRS-B4.05 | MRS-E1 defeated | HOB | "Lurker. They like a fowl as much as I do." |
| MRS-B4.01 | Heron lands on the stake | HOB (very quietly) | "Don't." |
| MRS-B4.06 | `MRS_HERON = loosed` | HOB | "Twenty years. It's never once let me." |
| MRS-B4.07 | `MRS_HERON = held` | HOB | "Good. It'd only have laughed." |

**The bench** (`MRS-D5`, step `S07_bench`)

```
MRS-D5.01 HOB: "Flight feathers in that basket. Down in that one. Down goes to Fenward. Lysa's lot sleep cold."
MRS-D5.02 HOB: "And there's your next bundle's feathers. See? It goes round."
MRS-D5.03 [MRS_HERON = loosed] HOB: "You'll want to say you nearly had it. Everyone does. Nobody nearly has it."
MRS-D5.03 [MRS_HERON = held] HOB: "You didn't shoot. Most people shoot. I'll remember that."
MRS-D5.04 HOB: "Two for you. One for me. The bundle's yours. Bench is yours any dusk you like."
  > "Thank you, Hob."                                                → MRS-D5.05
  > "One day I'll get that heron."                                   → MRS-D5.06
MRS-D5.05 HOB: "Come back when you can sit still for a whole flight without breathing loud. Then I'll show you how to make a proper bow."   → MRS-D5.07
MRS-D5.06 HOB: "No you won't. But come back anyway. One day I'll show you how to make a proper bow."   → MRS-D5.07
MRS-D5.07 [Hob's spare bow lent] HOB: "Bow back on its peg, please. It's sentimental. I'm not."
      {set MRS_HOB_BENCH; rewards per MRS.9; event: MRS-D5 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| MRS-I1 | Feeder stake | *"Water at the pale band. Running."* / *"Ochre. Slack. The shallows are out."* | `MR_CHANNELS` |
| MRS-I2 | Still-water stand | "Soft reed. The knots are bunched and it bends under a thumb." | — |
| MRS-I3 | Bend stand | "Some straight, some not. You'd be sorting all day." | — |
| MRS-I4 | Throat stand | "Even knots. Hard stems. They stand straight in the moving water." | — |
| MRS-I5 | Rolling board | "A planed plank, polished by a lifetime of reed rolled across it." | — |
| MRS-I6 | Feather basket | "Heron feathers, long and grey. A few fowl flights." / after `S07`: "Fuller." | — |
| MRS-I7 | Mere depth stake | "Crooked. Something heavy stands on it sometimes." | — |
| MRS-I8 | Hob's spare bow (peg) | "Root-wood belly, horn tips, a string waxed so often it shines." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| HOB | "Dusk's coming. Bench is yours." | `MRS_HOB_BENCH` |
| HOB | "It's on the stake again. Don't." | `MRS_HERON` = loosed, at dusk |
| HOB | "Lysa says thank you for the down. She didn't. I'm saying it for her." | MFT Completed |
| MARSHFALL CHILD | "Hob says you nearly hit the heron. Hob says everybody nearly hits the heron." | `MRS_HERON` = loosed |

**MD-7 swap note.** No Hollowfoot content in MRS. No change under either ruling.

### MRS.15 Open decisions

1. **EM-01/EM-04:** whether reed is a shaft material and root-wood a head. The quest stands on ordinary arrows if not.
2. **Skill requirement level** (Hunting ~[GD: low]): Gameplay Designer. Recommendation: a level reachable in Lowmark's or Thornfell's first hunting content, or about an hour of training.
3. **Hob's pronoun:** "he" throughout, matching Act I and Act III §E.10 (resolved; Act III now reads "he remembers the heron").

### MRS.16 Review log

| Finding | Revision |
|---|---|
| First draft required a hit on the heron for a bonus. | Cut. The heron is never hittable and gives nothing; the moment is wonder, not a skill test. |
| Ranged risked being required at the dusk flight. | The flight-net path uses the same rise timing; Hob also lends a bow. No step requires ranged (CDR-2). |
| Hunting requirement could gate the Fletching intro. | The requirement sits on Hunting, the skill the quest builds on; Fletching and Ranged are taught from any level (CDR-4 applied as bible §13 recommends). |
| Iron arrowheads would contradict MD-11. | Root-wood blunts; no metal anywhere in the loop. |
| Combat share. | One Reedlurker (contract). |

---

## MFT — A Table for the Wet

### MFT.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `mire.side.table_for_the_wet` |
| Type | Skill introduction (Cooking). Bible §7.2 row. |
| Unlock | MR-M1 Completed. Offered by Lysa Thornettle at the Fenward Huts (`MFT-D1`), or by her bark at the Ferrow house in Sorrowmere if the player has not been to Fenward since MR-M1 (`MFT-B0.2`). |
| Resume hook | Lysa at the Fenward hearth: `MFT-D1.00` "The water's still coming. Where were we?" |
| Skills | Cooking (required: smoke eel, stew, seal); Hunting (optional, one fowl) |
| Combat share | 0% (contract: none) |
| Cameo | Jory Wick `[MD-7]` (non-combatant, Act III cast); Hob Merrit (optional, the fowl) |
| Choice | None (contract) |
| Unlocks | The Fenward hearth as a public Cooking station; Act III `S01b_pot` variant |
| **Anchor** (§7.1) | Fenward care (Lysa Thornettle). |
| **World-truth row** | None (present-day care). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail: a crock spoiled by bad smoke is re-made; the flood stage waits for the player (it advances on keep watch, never on its own); completion sets nothing but the quest state and `MFT_CROCKS`. |
| **Combat compliance** | None. |

**In one paragraph.** The long wet is coming, and when it comes the Fenward Huts stand in water for a week. Lysa's people are the ones who cannot cook for themselves: Bettany Strand, who has no teeth left and whose husband died this spring; the Pellow brothers, one with hands that shake too much to hold a pot; a girl recovering from fever; and Jory Wick, who walked for years and will not eat anything he did not see cooked. Lysa needs a meal that will keep for the week of flood, and she needs it made for those people, not for "the sick". The player asks each of them what they can eat, gathers fen roots, a fowl and eels, smokes the eel in the Fenward smoke-hut by reading the colour of the smoke, cooks a root-and-fowl stew, and seals it in crocks with peat-wax, each crock labelled for its person. Then the water comes up to the step, and the crocks go up on the high shelves before dusk. The last thing is a meal now, at Lysa's table, everyone eating before anyone talks. Bettany lays a sprig of bogsedge on the empty place for her husband and says his name, and the fern on the windowsill wilts all at once.

### MFT.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Cook ten stews, hand them in. | Rejected. A recipe grind; nothing Mire about it. |
| B. A feast for a festival. | Rejected. *Lifting Day* owns the festival table (MLD). |
| **C. Ask what each person can eat → gather → smoke and stew → seal and label → lift above the flood → a meal now** | **Selected.** Care before explanation (bible §5.3 rule 6), record-keeping as love (rule 7, the labels), and the flood as a readable, staged pressure. |

| Element | Source | Status |
|---|---|---|
| Lysa Thornettle, healer; Fenward huts; "Healing is making space"; present care only | Mire anchors V; ledger row | [CANON] |
| Settled Hollowfoot at Fenward as non-combatant NPCs | Bible MD-7 dignity rules; Act III Jory Wick | [NEW], `[MD-7]` |
| Bogsedge fern wilts suddenly during strong grief | Dossier §X | [CANON] |
| Griefroot, medicinal tuber | Dossier §X | [CANON] (legacy resource, MD-11) |
| Bettany Strand, the Pellow brothers, the fever girl (role: Nessa) | This package | [NEW] |

### MFT.3 The places [MAP VERIFICATION REQUIRED]

The Fenward Huts lie by Rootrest on firmer ground beyond Marshfall (bible §4.2 route order). Relative only.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W1. The hearth hut** | Hook; the table | Lysa's main hut: a long table, a hearth with an iron pot (imported), herb bundles, a sill with a pot of **bogsedge fern**. **High shelves** round the walls above a painted line: the line the water reached last wet. |
| **W2. The four huts** | Asking | Bettany's hut (a chair by the door, a man's coat still on its peg); the Pellows' hut (two cots, one brother whittling, one watching his own hands); the fever hut (a girl under blankets, a cup of griefroot tea); Jory Wick's place (a pallet, a basket he sits on). |
| **W3. The smoke-hut** | Smoking eel | A low hut with a peat fire pit, eel racks and a **smoke vent** with a sliding reed shutter. |
| **W4. The root beds** | Gathering | Raised beds of fen roots on the firm ground behind the huts; a digging fork. |
| **W5. The step** | The flood | The huts' plank step and the post beside it, painted with the three bands (a small stake). When the wet comes, water stands at the step. |

### MFT.4 Beats

**Beat 0 — A Week of Water (`S00_offer`).** *Objective: Talk to Lysa at Fenward.* `MFT-D1`. With `MNS_BROTH = self`: "You cooked on the road once. Do it for twelve." Lysa asks first that the player sit and eat something (one bowl; care before explanation).

**Beat 1 — Ask Them (`S01_ask`).** *Objective: Ask each of Lysa's people what they can eat (0/4).* Four short conversations, any order (`MFT-D2`–`D5`). Each adds a line to Lysa's **slate** by the hearth (a chalk list; inspectable):

| Person | Need | What it changes |
|---|---|---|
| **Bettany Strand** | No teeth; "soft, and not fish, I can't abide fish" | Her crock is stew only, the roots mashed. |
| **Hal and Arno Pellow** | Arno's hands shake; he cannot lift a heavy pot | Their crocks are small, two each, and go on the low end of the high shelf. |
| **Nessa** (the fever girl) | Lysa says "no salt" for now | Her crock is unsalted, with griefroot from Lysa's own stock. |
| **Jory Wick** `[MD-7]` | Will not eat what he did not see cooked | He comes to the smoke-hut and watches (he sits on his basket in the doorway through `S02`–`S03`). His crock is the one he watched. |

The step teaches that the meal is for people, not for "the sick". Nothing fails: a player who asks in any order hears the same needs.

**Beat 2 — Gather (`S02_gather`).** *Objective: Gather roots, a fowl and eels.*

- **Fen roots:** dig at the root beds (W4), six roots (gathering interaction, ~2 s each).
- **A fowl** (one): **Option A (Hunting, optional):** take one at Hob's hide (the same Hunting interaction as MR-M1; any ranged weapon or Hob's flight-net). **Option B:** ask Hob for one off his string; costs a keep-watch turn at Fenward until he comes ("Hob comes by at noon with the down"). With MRS Completed, Hob gives it without the wait ("You plucked for me. Have one.").
- **Eels:** carry Lysa's lantern-moss bundle to the Marshfall smoke sheds and come back with a string of raw eels (a carry-state trade; no currency). Fallback for a player who will not walk: Lysa has two eels already; the step completes with those at the cost of a keep-watch turn while they are cleaned.

**Beat 3 — Smoke (`S03_smoke`).** *Objective: Smoke the eels.* At the smoke-hut (W3), hang the eels (interaction) and work the vent. The smoke's **colour** is the tell: thick and white means the peat is wet and the fire is choking (shutter more open); thin and blue is right; none means the fire is out (add peat). The fire drifts on a fixed loop through the three states; the player keeps it blue with the shutter (three adjustments over a ~30 s channel; a wrong adjustment just lengthens the channel). Cooking XP. Output: smoked eel (EM-06). Jory watches from his basket.

**Beat 4 — Stew and Seal (`S04_crocks`).** *Objective: Cook and seal a crock for each of them.* At Lysa's hearth: cook the root-and-fowl stew (Cooking interaction, ~4 s). Then fill and seal six crocks (one interaction each, ~2 s: ladle, peat-wax lid, tie): Bettany's (stew, mashed), two for the Pellows, Nessa's (unsalted, with Lysa's griefroot), Jory's (the one he watched), and the house crock with the smoked eel. **Label** each crock with a chalk mark from the slate (part of the seal interaction; the label reads the person's name). Sets `MFT_CROCKS`.

**Beat 5 — The Water at the Step (`S05_shelves`).** *Objective: Get the crocks above the water line before dusk.* Keep watch once (the step pins the flood stage to advance by one on keep watch): water stands at the step (W5) and the floors are wet. Carry the crocks (carry-state, two at a time) and set each on the high shelf above the painted line in the right hut (interaction). Arno Pellow's two go low, where he can reach them sitting (the slate says so; setting them high plays `MFT-B3.03` and the player moves them; no penalty). Dusk does not come until the last crock is up (the step holds the hour).

**Beat 6 — The Table (`S06_table`).** *Objective: Eat with them.* Everyone comes to the hearth hut. The player serves (interaction at the pot), then sits (sit interaction at the table). Food first: nobody speaks for a while (barks are eating sounds and one Arno line). Then the strange moment (MFT.5). Then Lysa: "Now we can talk." `MFT-D7`. Quest Completed.

### MFT.5 The fern (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The place** | At the table, Bettany lays a sprig of bogsedge fern from her apron on the empty place beside her. |
| 0–4 s | **The name** | Bettany, to the empty place: "That's yours, Ottor. Eat it or don't." (`MFT-D7.01`) |
| 4–6 s | **The sill** | On the windowsill behind her, the potted bogsedge fern wilts all at once: every frond drops flat in the same second. No sound, no music. |
| 6–10 s | **The table** | Lysa sees it. She looks at Bettany and goes on eating. Jory Wick puts his spoon down and picks it up again. |
| After | Inspect | Fern on the sill: *"Every frond lies flat. The soil is wet. It was green a minute ago."* (Next morning it is upright again; per-player prop.) |
| UI | None. |
| Meaning | None stated. Bogsedge does this "in strong grief" [CANON]; the Mire says so and no more. It proves nothing about Ottor. Lysa: "Seen: it went down. Thought: it does that. That's all I've got." (only if asked, `MFT-D7.10`). |

### MFT.6 Encounters and hazards

None. **Flood stage** (W5) is presentation only: the water at the step slows movement on the hut floors; no damage. **Death** cannot occur from the quest; ordinary death elsewhere respawns at Fenward with steps intact.

### MFT.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to Lysa at Fenward. | `MFT-D1` accept | Yes | `MNS_BROTH` variant |
| `S01_ask` | Ask each of Lysa's people what they can eat. | `MFT-D2`–`D5` end nodes (4) | Yes | Slate lines added |
| `S02_gather` | Gather roots, a fowl and eels. | 6 roots + 1 fowl (A or B) + eels (trade or Lysa's two) | Yes | `MFT_FOWL_SELF` on Option A |
| `S03_smoke` | Smoke the eels. | Smoke-vent channel complete | Yes | Jory watches |
| `S04_crocks` | Cook and seal a crock for each of them. | Stew + 6 `seal_crock` | Yes | Sets `MFT_CROCKS` |
| `S05_shelves` | Get the crocks above the water line before dusk. | 6 crocks set on authored shelf slots | Yes | Flood stage +1 on keep watch; dusk held until done |
| `S06_table` | Eat with them. | Serve + sit + `MFT-D7` end | Yes | **Quest Completed** (the state Act III reads) |

| Flag | Set by | Read by |
|---|---|---|
| `MFT_FOWL_SELF` | `S02` Option A | `MFT-D7.05` |
| `MFT_CROCKS` | `S04` | Fenward barks; crock shelf prop |
| *(state)* MFT Completed | `S06` | Act III `MBL-D2b.21` |

### MFT.8 Choices and consequences

None (contract).

### MFT.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Fenward hearth | Access | Public Cooking station with Lysa's slate (barks). |
| Smoked eel, one bowl of stew | Food (EM-06, EM-07) | Ordinary cooked food in the pack. |
| Cooking, Hunting XP | Action XP only | No lump quest XP; no payment (Lysa has none; the player does not ask). |

### MFT.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Smoke goes white or out | The channel lengthens; adjust the shutter or add peat. |
| Crock set on the wrong shelf | A bark; the crock can be moved. |
| Will not hunt | Option B or MRS-completed shortcut. |
| Will not walk to Marshfall | Lysa's two eels; one keep-watch turn. |
| Walking away | Stays Active; resume hook at Lysa. The flood stage never advances without the player's keep watch. |
| Logout | Last step restored; carried crocks return to the hearth table. |
| Co-op | Each player asks, cooks and shelves their own crocks (per-player props). The table moment plays per player; NPC placement follows the host. |

### MFT.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Smoke-colour loop | VFX / Systems | Three smoke states on a fixed loop; shutter interaction shifts state. |
| Flood stage at Fenward | Systems | Two environment variants (dry / water at the step) swapped by quest step (bible §11.2 N-3 pattern). |
| Labelled carry-state crocks with authored shelf slots | Systems | Carry-state pattern with deposit targets. |
| Wilting fern prop | Art / Systems | Two-state prop swapped by the table event; resets next presentation morning. |

### MFT.12 Economy dependencies

EM-03 fen fowl, EM-06 smoked eel, EM-07 root-and-fowl stew, EM-10 fen roots and griefroot (Lysa's stock only).

### MFT.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Observable | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| The fern | Bogsedge wilts in strong grief [CANON]; why is not known. | "It does that." | The fern goes flat as Bettany says Ottor's name. | Ottor is in the room. (Nobody speaks for the dead; bible §5.3 rule 3.) | Why. | None. Deliberately unexplained. |

### MFT.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Lysa Thornettle** [CANON anchor] | Her people, their needs, the water line, the herbs. | Anything beyond present care (ledger). | "Healing is making space." Calm; feeds first. |
| **Bettany Strand** [NEW] | Her husband Ottor, dead this spring of age and the wet; that she hates fish. | — | Tart, funny, grief worn like an apron. |
| **Hal Pellow, Arno Pellow** [NEW] | Their own hands and their own pride. | — | Hal talks for both; Arno says one thing at a time. |
| **Nessa** [NEW], fever girl | That she is bored. | — | Twelve, cross, better. |
| **Jory Wick** [NEW, Act III] `[MD-7]` | Little he says. | — | Very few words. Non-combatant, never targetable. No war history is given. |

**Offer** (`MFT-D1`)

```
MFT-D1.00 [quest Active, returning] LYSA: "The water's still coming. Where were we?" (pins step)  → end
MFT-D1.01 LYSA: "Sit. Eat. Then tell me what you came for." (puts a bowl in front of the player)
MFT-D1.02 LYSA: "Long wet's a week of water here. It comes up to the step and stays. My lot can't cook in that, and some of them can't cook in anything."
MFT-D1.03 [MNS_BROTH = self] LYSA: "You cooked on the road once. Do it for twelve."
MFT-D1.03 [else] LYSA: "I need a meal that keeps a week. Made for them, not for 'the sick'."
  > "What do they need?"                                             → MFT-D1.04
  > "I can't cook much."                                             → MFT-D1.06
MFT-D1.04 LYSA: "Ask them. Not me. Each one. Then cook what they said."   {event: accept → S01_ask}  → end
MFT-D1.06 LYSA: "Nobody can, till they do it for somebody. Ask them first. It's easier to cook for a name."   {event: accept → S01_ask}  → end
```

**Asking** (`MFT-D2`–`D5`)

```
MFT-D2.01 BETTANY: "Soft. I've no teeth to speak of. And not fish. I can't abide fish, and Lysa knows it, and she still tries."
MFT-D2.02 BETTANY: (nods at the coat on the peg) "Ottor ate the fish. Forty years I watched him eat fish."
  > "I'll make yours soft. No fish."                                 → MFT-D2.03
  > "Is that his coat?"                                              → MFT-D2.04
MFT-D2.03 BETTANY: "Good. Put my name on it, or Lysa'll give it to the Pellows."   {slate: Bettany}  → end
MFT-D2.04 BETTANY: "It's a coat. It's on a peg." (beat) "Soft. No fish. Put my name on it."   {slate: Bettany}  → end

MFT-D3.01 HAL: "Arno can't lift a pot. Not with his hands like that. He'll go hungry before he'll ask."
MFT-D3.02 ARNO: "I'll ask."
MFT-D3.03 HAL: "He won't."
MFT-D3.04 ARNO: "Small ones. Low down. Then nobody has to ask."   {slate: Pellows, small, low}  → end

MFT-D4.01 NESSA: "Lysa says no salt. Everything's horrible without salt."
MFT-D4.02 LYSA: (from the door) "Everything's horrible with fever, too. No salt. I'll put root in it."
MFT-D4.03 NESSA: "Root tastes like a cellar."   {slate: Nessa, no salt, griefroot (Lysa)}  → end

MFT-D5.01 (Jory Wick looks at the player's hands, then at the player's face.)
MFT-D5.02 LYSA: (quietly, beside the player) "Jory eats what he sees cooked. He's not being difficult. It's how he stays here."
  > "Then come and watch me cook, Jory."                             → MFT-D5.03
  > (wait)                                                           → MFT-D5.04
MFT-D5.03 JORY: (stands, picks up his basket) "...Watch."   {slate: Jory, watched}  → end
MFT-D5.04 (After a while Jory stands and picks up his basket. He looks toward the smoke-hut.) LYSA: "That's yes."   {slate: Jory, watched}  → end
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MFT-B0.2 | Ferrow house, MR-M1 done, MFT not offered | LYSA (visiting Nell) | "If you're coming out to Fenward, come hungry. I've a job that wants a cook." |
| MFT-B1.01 | Smoke white | LYSA (if near) / log | "Choking. Open the vent." |
| MFT-B1.02 | Smoke blue | log | "Thin and blue. That's right." |
| MFT-B1.03 | Fire out | log | "Nothing. Peat on." |
| MFT-B1.04 | Smoking complete | JORY | (nods once) |
| MFT-B2.01 | Fowl option B, Hob arrives | HOB | "Down for Lysa, fowl for you. Don't tell the heron." |
| MFT-B2.02 | Fowl, MRS Completed | HOB | "You plucked for me. Have one." |
| MFT-B3.01 | Water reaches the step | LYSA | "There it is. Up they go. Before dark." |
| MFT-B3.03 | Pellow crock set high | ARNO | "Can't reach that." |
| MFT-B3.04 | Last crock up | LYSA | "Good. Now it can rain all it likes." |
| MFT-B4.01 | At the table, eating | ARNO | "It's soft." (beat) "It's good soft." |

**The table** (`MFT-D7`, after the strange moment)

```
MFT-D7.01 BETTANY: (laying a sprig of bogsedge on the empty place) "That's yours, Ottor. Eat it or don't."
      {event: fenward.fen_fern (MFT.5)}
MFT-D7.02 (A long quiet. Lysa eats. Jory puts his spoon down and picks it up again.)
MFT-D7.03 LYSA: "Now we can talk."
MFT-D7.04 LYSA: "There's a week of food on those shelves with names on it. That's the best kind of record."
MFT-D7.05 [MFT_FOWL_SELF] HAL: "Fowl's good. Who shot it?" / NESSA: "The traveller. Obviously."
  > "What happened to the fern?"                                     → MFT-D7.10
  > "Thank you for having me at the table."                          → MFT-D7.20
MFT-D7.10 LYSA: "Seen: it went down. Thought: it does that." (beat) "That's all I've got. Eat."   → MFT-D7.20
MFT-D7.20 BETTANY: "You can come back when it's dry. Bring nothing with fish in it."
MFT-D7.21 LYSA: "The hearth's yours when you want it. Cook for whoever's here."
      {event: MFT-D7 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text | Condition |
|---|---|---|---|
| MFT-I1 | Lysa's slate | "Bettany: soft, no fish. Pellows: small, low. Nessa: no salt, root. Jory: watched." | After `S01` |
| MFT-I2 | Painted water line | "The line the water reached last wet. Above it, shelves." | — |
| MFT-I3 | Ottor's coat | "A man's coat on a peg. Brushed." | — |
| MFT-I4 | Crock shelf | "Six crocks, sealed with peat-wax, a name chalked on each." | After `S05` |
| MFT-I5 | Bogsedge on the sill | "A fern in a pot. Fragile fronds." / after the moment: "Every frond lies flat. The soil is wet. It was green a minute ago." | — |

**Post-quest barks**

| Speaker | Line | Condition |
|---|---|---|
| BETTANY | "Ate the lot. Soft. No fish. You'll do." | MFT Completed |
| LYSA | "Pot's on. Whoever's here eats." | MFT Completed, at the hearth |
| NESSA | "Lysa let me have salt. A bit. Don't tell her I told you." | MFT Completed, later visit |

**MD-7 swap note.** Jory Wick is already depicted as a non-combatant survivor in Lysa's care, which is the Director's alternative depiction. **No change under either ruling.** If the Director retires Hollowfoot as a word entirely, Lysa's cast note calls him "a man who walked for years", which is how every line here already reads.

### MFT.15 Open decisions

1. EM-06/EM-07: smoked eel and stew as foods. The quest gives the nearest approved food if not derived.
2. Whether the Fenward hearth's public Cooking station should read Act III's vigil-pot recipe (same stew). Recommendation: yes, one recipe.

### MFT.16 Review log

| Finding | Revision |
|---|---|
| Draft had Lysa explain the fern as grief "reaching" it. | Cut. "Seen / thought" grammar; nothing more. |
| Jory's dignity. | He is asked like everyone else, chooses to watch, is never "a case". Non-targetable. No history given. |
| Draft let the flood advance on a timer. | Changed: the flood advances only on the player's keep watch; dusk is held until the last crock is up. No time pressure that can fail. |
| Act III read. | Completion is the plain quest state at `S06`; nothing else is required for `MBL-D2b.21`. |

---

## MFH — The Ferry Harness

### MFH.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `mire.side.ferry_harness` |
| Type | Skill introduction (Leatherworking, Woodcutting). Bible §7.2 row. |
| Unlock | MR-M1 Completed. Offered at Blackwater Landing (MP06) by Gwenna Tolley when the player first reaches the reed docks (`MFH-B0`, `MFH-D1`). |
| Skill requirement | **Woodcutting ~[GD: low]** to accept (CDR-4). Leatherworking is taught from any level. |
| Resume hook | Gwenna on the Tolley punt: `MFH-D1.00` "Punt's still sat there. Where were we?" |
| Skills | Woodcutting (required: root-knee pins), Leatherworking (taught: repair), Melee or Ranged (Bog Hounds) |
| Combat share | ~15% (one Bog Hound pack at the smoke racks) |
| Cameo | Rowan Mirewake (one bark; he is not involved; MR-M3 owns him) |
| Choice | None (contract) |
| Unlocks | Gwenna's repair bench at the Landing; the Tolley punt as a short ferry across the home channel |
| **Anchor** (§7.1) | Ferry households of Blackwater Landing (the Tolleys). |
| **World-truth row** | None. |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed. No fail: leather that cracks on the flex test goes back to the store and another piece is tried; a pin that does not fit is shaved again; a wrong call on the crossing means the punt holds in an eddy for the next turn. |
| **Combat compliance** | Bog Hounds (MFH-E1) defeated at 0 HP; melee or ranged; no SX. |

**In one paragraph.** At the start of the long wet the Tolley household's tow harness parted on the home channel and their punt went onto the mud with a sick-run load in it: blankets, griefroot and a crock for Fenward. Gwenna Tolley, who has rowed the home channel for longer than the stakes have been painted, cannot get it off without a harness for her grandson Cadan on the tow path, and she cannot row it across without new thole pins: both old pins split in the same pull. The Mire does not tan; what leather it has comes in by trade and is mended until it is the Mire's. The player strips the rotten harness and keeps the buckles, flex-tests stored trade leather for the pieces that have not rotted in the damp, cuts and stitches new traces and dresses them with eel oil. Then they find a drowned root-knee at the landing bank at Slack, split it and shave two pins to the gauge of Gwenna's last good one. While they work, a pack of Bog Hounds comes for the smoke racks. At the next Running the punt goes across with the player rowing on the new pins and Cadan hauling on the new harness from the bank, and in the middle of the channel the water goes flat as glass and the punt runs on for three strokes with nobody rowing.

### MFH.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Craft a harness at a bench from nothing. | Rejected. The Mire does not tan (source process); making leather here is false. |
| B. Same task as MR-M3 (mend Rowan's harness, haul at a shoal). | Rejected. Duplicates Act II. MFH is a household, a punt, pins and **rowing**; the player never hauls. |
| **C. Strip and keep → flex-test imported leather → stitch and dress → cut pins from drowned root → hold the landing → row the crossing at Running** | **Selected.** Repair as a Mire virtue (mend what you cannot make), a Woodcutting gate the quest builds on, and the channel system as the test. |

| Element | Source | Status |
|---|---|---|
| Blackwater Landing: reed docks, boat shed, ferry households | Bible MP06; Act II §L | [CANON anchor location; NEW name] |
| No local tanning; imported leather; reclaimed and root wood | Source process proposal; MD-11 | Proposal adopted by the bible |
| Bog Hounds: thin, aggressive canines hardened by hunger | Dossier §IX; bible §10 ("first seen: *The Ferry Harness*") | [CANON] |
| Gwenna Tolley, Cadan Tolley, the home channel | This package | [NEW] |

### MFH.3 The places [MAP VERIFICATION REQUIRED]

Blackwater Landing sits below Sorrowmere (bible §4.2). The **home channel** is the short crossing from the reed docks to the ferry households' far bank, not Rowan's route.

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **L1. The reed docks** | Hook | Plank docks on stilts. Ferry households' punts in a row; Rowan's mooring (empty or not, per MR-M3 state; not used here). | — |
| **L6. The ferry households' row** (Act II name) | Tolley house; bench | Three stilt houses. The Tolley house has an open-fronted **work bench** under its eave: awls, a skiving knife, a pot of eel oil, a **leather store** (a chest of folded trade hides, damp-stained). | — |
| **H1. The stranded punt** | The problem | The Tolley punt on the mud of the home channel's near bank, listing, its load lashed under oilcloth. The **tow harness** lies in the mud, one trace parted. Two split **thole pins** in their holes. | Mud flat walkable at Slack and Sour; at Running the punt floats. |
| **H2. The landing bank** | Root-knees | Drowned stumps along the bank. At Slack the water drops and three **root-knees** stand clear. | Bank walkable at Slack only (state toggle). |
| **H3. The smoke racks** | MFH-E1 | Eel racks over a peat smoulder at the end of the row. | — |
| **H4. The home channel and tow path** | Crossing | A channel a long stone's throw wide with a **stake** at each end; a tow path of posts along the near side. | Punt only; tow path walkable. |

### MFH.4 Beats

**Beat 0 — Stranded (`S00_offer`).** *Objective: Talk to the woman on the punt.* `MFH-D1`. A player below the Woodcutting requirement gets `MFH-D1.06`.

**Beat 1 — Strip It (`S01_strip`).** *Objective: Strip the broken harness.* At the punt: cut the harness free of the punt's bow ring (interaction), carry it to the bench (carry-state), and strip it: cut away the rotten traces and breast band (two interactions), and **keep the buckles and rings** (interaction, ~2 s; "Iron's dear. Buckles outlive three harnesses."). The chest pad is sound.

**Beat 2 — Good Leather (`S02_leather`).** *Objective: Find leather that will hold.* Open the leather store. Five folded trade hides (EM-08). Each can be **flex-tested** (interaction, ~1 s): bent hard over the knee, sound leather creases dark and springs back; rotted leather cracks white along the bend (visible). Authored: two sound, three cracked. The player needs two sound pieces. Cracked pieces go back with a line, no penalty.

**Beat 3 — Stitch and Dress (`S03_mend`).** *Objective: Mend the harness.* Leatherworking (taught): **cut** two traces and a breast band against the old ones laid flat as patterns (interaction), **skive** the ends thin where they fold round the buckles (interaction), **stitch** them on (channelled, 3 segments of ~4 s; segments persist), **dress** with eel oil (interaction, ~2 s). Leatherworking XP.

**Alternative path:** "Cadan can stitch if you cut." The player cuts and skives; Cadan stitches overnight (keep watch until morning). Cost: a turn. Sets `MFH_CREW_STITCH`.

**Beat 4 — Pins from the Bank (`S04_pins`).** *Objective: Cut two thole pins from root wood.* Keep watch until Slack (if not already). On the landing bank (H2), choose a root-knee: inspect shows which is sound (the dark, heavy one) and which are punky (`MFH-I4`). Woodcutting (required by the quest's start gate): **split** the sound root-knee (channelled, 3 segments of ~4 s). At the bench, **shave** two pins (interaction, ~3 s each) and **fit** each against Gwenna's last good pin as a gauge (interaction: too fat, "Won't go." and shave again; right, "Snug."). The authored first shave is always too fat; the second fits (teaches the gauge).

**Beat 5 — The Racks (`S05_hounds`).** *Objective: Defeat the dogs at the racks.* The step triggers when both pins are fitted (or at dusk if the player is on the row): a Bog Hound pack comes for the smoke racks. **MFH-E1.** Defeat them at 0 HP. Gwenna: "They're starving. So's everybody. Doesn't mean they get the eels."

**Beat 6 — Across at Running (`S06_cross`).** *Objective: Row the punt across the home channel.* Keep watch until the home channel turns Running (the punt floats). Fit the pins in the punt (two interactions) and the harness on Cadan at the tow path (interaction). Board and take the oars. The crossing is the Lowmark ferry convention (an escorted ride on a fixed route) with the player **rowing**: three short stretches; at the start of each Gwenna calls a choice from the stakes and the water (`MFH-D4`): row on, ease, or hold for Cadan to take up the slack on the tow. A wrong call holds the punt in an eddy for a few seconds and Gwenna corrects (no failure). In the middle stretch, the strange moment (MFH.5).

**Beat 7 — The Far Bank (`S07_land`).** *Objective: Land the load.* At the far bank, carry the sick-run load (two carry-state bundles) to the households' porch. `MFH-D5`. Quest Completed.

### MFH.5 The slack seam (presentation spec: wonder)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The water** | Mid-channel, at Running. The surface ahead goes from rippled to flat as glass for a boat's length, a smooth band across the channel. The near and far stakes both still read Running. |
| 0–4 s | **The run** | The player's oars come out of the water by themselves at the end of a stroke (the rowing animation pauses). The punt runs on smoothly for three strokes' worth of distance with nobody rowing. The tow line goes slack in Cadan's harness and he stumbles a step and laughs. |
| 4–6 s | **Gwenna** | "Sit still. Let it carry." (`MFH-D4.20`) |
| 6–8 s | **Out** | The punt leaves the flat band; the ripple and the pull come back; the oars go in again. |
| After | Gwenna, if asked | "My mother called it being carried. I call it a slack seam. Two currents rub and leave a bit of nothing between. You feel it now and then." (`MFH-D4.22`) |
| Meaning | Ordinary water, unusual to a stranger. It proves nothing. Gwenna's mother's word is her mother's, and Gwenna says so. |

### MFH.6 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MFH-E1** | 2 × Bog Hound (runner), 1 × Bog Hound (gnawer) | Smoke racks (H3), along the plank row | Runners circle and dart at the player; the gnawer goes for the racks and tears an eel down each ~6 s it is left alone (cosmetic; racks refill) | **Runner dart:** drops its head and the hackles lift (~0.9 s), then a short lunge. **Gnawer bite:** stands square, lips back (~1.2 s), then a heavy bite that inflicts a short bleed | Required. First appearance of Bog Hounds (bible §10). Planks are narrow: ranged players have the row's length; melee players have the rack posts to pin a runner against | 45–60 s |
| **MFH-H1** | Mud at the punt | H1 at Slack/Sour | Slow zone | Wet mud sheen | Teaches that the punt is only free at Running | Movement slowed; no damage |

**Rules.** The hounds are wildlife defeated at 0 HP (CDR-1); no flee. Combat drops nothing that advances the quest. **Death:** respawn at the Tolley bench; stitched segments, fitted pins and the cut harness persist; the hounds reset.

### MFH.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the woman on the punt. | `MFH-D1` accept (Woodcutting ~[GD: low]) | Yes | Below requirement: `MFH-D1.06` |
| `S01_strip` | Strip the broken harness. | Cut free + carry + 2 strip + keep buckles | Yes | — |
| `S02_leather` | Find leather that will hold. | 2 sound hides chosen | Yes | Authored 2 sound / 3 cracked |
| `S03_mend` | Mend the harness. | Cut, skive, 3 stitch segments, dress **or** crew stitch (cut, skive + keep watch) | Yes | `MFH_CREW_STITCH` |
| `S04_pins` | Cut two thole pins from root wood. | Split channel + 2 shave + 2 fit | Yes | Bank walkable at Slack |
| `S05_hounds` | Defeat the dogs at the racks. | MFH-E1 defeated | Yes | — |
| `S06_cross` | Row the punt across the home channel. | Pins fitted + harness on Cadan + crossing route complete | Yes | Running pinned on keep watch; slack seam event |
| `S07_land` | Land the load. | 2 carry-deposits + `MFH-D5` end | Yes | Sets `MFH_TOLLEY_BENCH`; quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `MFH_CREW_STITCH` | `S03` alternative | `MFH-D5.03` |
| `MFH_TOLLEY_BENCH` | `S07` | Landing repair station; Act II L6 (request: optional bark) |

### MFH.8 Choices and consequences

None (contract).

### MFH.9 Rewards

| Reward | Type | Notes |
|---|---|---|
| Gwenna's bench | Access | A public repair bench (harness, strap and pin repair recipes when the item pass defines them). |
| The Tolley punt | Access | Gwenna or Cadan rows the player across the home channel at Running (a short ferry). Not Rowan's route; it reaches nowhere the player could not walk round to. |
| Small payment | Currency | Gwenna's purse; economy tuning. |
| Reading leather and root | Knowledge | Leather in Mire stores and root-knees on banks become inspectable for sound or rotten. |
| Leatherworking, Woodcutting, Melee or Ranged XP | Action XP only | No lump quest XP. |

### MFH.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Below the Woodcutting requirement | Offer visible; accept greyed with `MFH-D1.06`. |
| Picks rotten leather | It cracks on the test and goes back. |
| Picks a punky root-knee | Split channel completes but Gwenna rejects it at the gauge ("Punky. It'll crush."); the player splits the sound one. |
| Rows on a wrong call | Holds in an eddy; Gwenna corrects. |
| Death | Respawn at the bench; progress kept. |
| Walking away | Stays Active; resume hook at Gwenna. |
| Logout | Last step restored; the harness returns to the bench. |
| Co-op | Each player mends and rows their own (the punt is a per-player instance); the hounds are shared world creatures. |

### MFH.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Flex-test station with authored results | Systems | Interaction on each hide returning sound/cracked from an authored list. |
| Pin gauge fit | Systems | Two-result interaction (too fat / snug) with the first shave authored as too fat. |
| Bank and mud state by channel | Systems (N-1) | Walkable bank at Slack; punt float/ground props by state. Quest pin fallback. |
| Rowing crossing | Systems | Lowmark ferry convention with the player as the rower (rowing animation, fixed route, dialogue calls). No physics. |
| Slack-seam presentation | VFX / Animation | A flat-water band decal and a scripted glide on the route. |

### MFH.12 Economy dependencies

EM-08 trade leather (repair inputs), EM-09 root wood (pins). The buckles are kept, not crafted.

### MFH.13 Mystery ledger entry

None.

### MFH.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Gwenna Tolley** [NEW], ferry mother | The home channel, every stake on it, leather by feel, her mother's words for water. | Rowan's route (and does not ask). | Brisk, warm, bossy; talks while she works. |
| **Cadan Tolley** [NEW], her grandson | How to haul; that he is strong. | How to stitch neatly (he stitches anyway). | Seventeen, cheerful, says "Gran" a lot. |

**Offer** (`MFH-D1`)

```
MFH-D1.00 [quest Active, returning] GWENNA: "Punt's still sat there. Where were we?" (pins step)  → end
MFH-D1.01 GWENNA: (on the listing punt, up to her shins) "Don't just stand on the dock looking useful, traveller. Be useful."
MFH-D1.02 GWENNA: "Harness parted on the pull. Both pins split on the same stroke. Forty years, and they pick the first day of the wet."
MFH-D1.03 GWENNA: "There's blankets and root and a crock for Fenward under that cloth. Lysa's waiting on it."
  > "What do you need?"                                              → MFH-D1.04
  > "Can't you ask Rowan?"                                           → MFH-D1.08
MFH-D1.04 GWENNA: "A harness for Cadan, so he can haul. Two pins, so I can row. The leather's in my chest, the pins are in the bank, and my knees are in the mud."
  > [Woodcutting below ~[GD: low]] "I've never split wood."          → MFH-D1.06
  > [Woodcutting ~[GD: low]] "I'll do it."                           → MFH-D1.05
MFH-D1.05 GWENNA: "Good. Strip that harness first. Keep the buckles. Iron's dear."   {event: accept → S01_strip}  → end
MFH-D1.06 GWENNA: "Root wood's twisty. It'll have your hand off if you've never held an axe. Go and split some honest logs somewhere. Anywhere. Come back with the feel of it." (beat) "Punt's not going anywhere. Neither am I."   → end (offer stays open)
MFH-D1.08 GWENNA: "Rowan's got his own boat to worry about and his own reasons. I don't borrow a man's reasons."   → MFH-D1 options
```

**Work barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MFH-B1.01 | Buckles kept | GWENNA | "Buckles outlive three harnesses. Leather's the bit that dies." |
| MFH-B1.02 | Sound hide flexed | GWENNA | "Creases dark, comes back. That's alive." |
| MFH-B1.03 | Cracked hide | GWENNA | "White. Rotted in the damp. Back it goes." |
| MFH-B1.04 | Skive | GWENNA | "Thin where it folds. Thick where it pulls." |
| MFH-B1.05 | Dress | GWENNA | "Eel oil. You'll smell like supper." |
| MFH-B1.06 | Crew stitch chosen | CADAN | "I'll do it tonight, Gran. Neatly." / GWENNA: "You won't." |
| MFH-B2.01 | Punky knee inspected | GWENNA | "Light. Punky. Crush in a thole." |
| MFH-B2.02 | First pin too fat | log | "Won't go." |
| MFH-B2.03 | Pin fits | GWENNA | "Snug. That's a pin." |
| MFH-B3.01 | Hounds come | GWENNA | "Dogs at the racks. They're starving. So's everybody. Doesn't mean they get the eels." |
| MFH-B3.02 | Hounds defeated | CADAN | "Gran'll want those racks counted." |
| MFH-B9.01 | Passing, Rowan at the landing (any state) | ROWAN | "Tolley's got you mending. Good. She'll check it." |

**The crossing** (`MFH-D4`, step `S06_cross`, in the punt)

```
MFH-D4.01 GWENNA: "Stake says running. Punt floats. Cadan, harness."
MFH-D4.02 CADAN: (from the tow path) "On, Gran."
MFH-D4.03 GWENNA: "First stretch. Water's pushing us down. What do you do?"
  > "Row on, steady."                                                → MFH-D4.04
  > "Hold for Cadan to take the slack."                              → MFH-D4.05
MFH-D4.04 GWENNA: "Good. Steady's always right on the first bit."   → MFH-D4.10
MFH-D4.05 GWENNA: "He's got it already. Row." (the punt drifts in an eddy a moment)  → MFH-D4.10
MFH-D4.10 GWENNA: "Middle. Stake at the far end's still pale. Ease off, let the current and the line argue."
  > "Ease."                                                          → MFH-D4.11
  > "Row hard."                                                      → MFH-D4.12
MFH-D4.11 GWENNA: "There."   {event: landing.slack_seam (MFH.5)}  → MFH-D4.20
MFH-D4.12 GWENNA: "Hard and you'll pull Cadan in. Ease." (eddy)   {event: landing.slack_seam}  → MFH-D4.20
MFH-D4.20 GWENNA: "Sit still. Let it carry."
  > "What was that?"                                                 → MFH-D4.22
  > (say nothing)                                                    → MFH-D4.30
MFH-D4.22 GWENNA: "My mother called it being carried. I call it a slack seam. Two currents rub and leave a bit of nothing between." (beat) "That's her word, not mine. I just row through it."   → MFH-D4.30
MFH-D4.30 GWENNA: "Last bit. Bank's coming. Hold for the line."
  > "Hold."                                                          → MFH-D4.31
  > "Row in."                                                        → MFH-D4.32
MFH-D4.31 GWENNA: "Good. Cadan, ease her in."   → end (route completes)
MFH-D4.32 GWENNA: "We'll hit. Hold." (a soft bump)   → end (route completes)
```

**Landing** (`MFH-D5`)

```
MFH-D5.01 GWENNA: "Root and blankets up on the porch. Crock goes on to Lysa with the next boat."
MFH-D5.02 GWENNA: "Pins sat right. Harness held. Cadan's still on the right side of the water."
MFH-D5.03 [MFH_CREW_STITCH] GWENNA: "His stitching's a disgrace. It held. Don't tell him either part."
MFH-D5.04 GWENNA: (counts coins out of a purse) "That's for the mending. Bench is yours when you've something to mend. And if you want the home channel, holler."
      {set MFH_TOLLEY_BENCH; event: MFH-D5 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text |
|---|---|---|
| MFH-I1 | Broken harness | "One trace parted clean through. The rest is cracked like old bark." |
| MFH-I2 | Split thole pins | "Both split along the grain, at the same place." |
| MFH-I3 | Leather store | "Folded trade hides. Stains where the damp got in." |
| MFH-I4 | Root-knees | "One dark and heavy. Two pale and light when you knock them." |
| MFH-I5 | Gwenna's last good pin | "Black with hands. The gauge everything else is cut to." |
| MFH-I6 | Home channel stake | `MR_CHANNELS` reading, as everywhere. |

**Post-quest barks**

| Speaker | Line |
|---|---|
| CADAN | "Harness still holds. I check it every morning. Gran checks it after me." |
| GWENNA | "Want the home channel? Running's when." |
| GWENNA | "Felt the seam again yesterday. Didn't say anything to it." |

**MD-7 swap note.** No Hollowfoot content in MFH. No change under either ruling.

### MFH.15 Open decisions

1. EM-08: imported leather state and repair recipes. Recommendation: the approved vegetable-tanned leather, no route stated (FT-03).
2. Woodcutting requirement level (~[GD: low]): Gameplay Designer.
3. Bog Hounds' first appearance is here (bible §10). Telegraphs above are the long first-appearance lengths.

### MFH.16 Review log

| Finding | Revision |
|---|---|
| Draft had the player haul the punt along the tow path. | Changed to rowing; MR-M3 owns hauling in harness. |
| Draft let the player tan a hide. | Cut. Repair of imported leather only (source process). |
| The slack seam could read as magic. | Gwenna names it a water effect and attributes "being carried" to her mother. |
| Requirement on the taught skill. | Requirement moved to Woodcutting (built on); Leatherworking taught. |

---

## MWS — Weight of the Soil

### MWS.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `mire.side.weight_of_the_soil` |
| Type | Settlement (Marshfall). Dossier questline 4; bible §7.2 row. |
| Unlock | MR-M2 Completed. Offered by Hedda Fallow on Peat Row, Marshfall (`MWS-D1`); Dunstan Hayle's bark points the player there (`MWS-B0`). |
| Resume hook | Hedda at the row's head: `MWS-D1.00` "Row's still sinking. Where were we?" |
| Skills | Woodcutting (light: roots); Melee or Ranged (beetles). No skill check. |
| Combat share | ~10% (Griefbit Beetles) |
| Cameo | Dunstan Hayle; Calwen Reed-Binder and Mara Fenholt at the choice |
| Choice | Lift the marker or leave it (quest-local `MWS_MARKER`) |
| Unlocks | Peat Row's walkway (a faster path through Marshfall); Marshfall rootcrafters' trade (EM-09) |
| **Anchor** (§7.1) | Marshfall households (Peat Row). |
| **World-truth row** | H05 (Memorywarden shards and anchor circles as the earth tradition's trace: the marker); H23 (uneven recovery). |
| **Revelation role** | Self-contained. The marker is an object with office marks; it supports nothing and identifies nobody. |
| **Recurring evidence** | Marker stays in place (`left`) or goes to Calwen's unsorted chest (`lifted`), beside MR-M2's shard. Neither is read as evidence by any later package. |
| **State compliance** | Inactive / Active / Completed; `MWS_MARKER` = lifted / left; no fail. |
| **Combat compliance** | Griefbit Beetles (MWS-E1) to 0 HP; melee or ranged; no SX. |

**In one paragraph.** Peat Row is the end of Marshfall nobody visits: a line of stilt houses on a walkway that is sinking, with roots choking the paths between them, and everyone too tired to fix any of it. Hedda Fallow, who keeps the row's rota, asks the stranger for a day's work, because a stranger will not be told "we tried that". The player carries peat for an old cutter whose back has gone, closes a gap in the walkway a child keeps falling through, and sits with Maddy Brook, whose fear brings beetles out of the boards. Then the real work: re-piling a collapsed walkway section at Slack and cutting the roots that have grown across the worst stretch. Under the worst stretch, in the cleared ground, is a squat stone with a pressed ring and marks on its face, and the roots grew round it in a perfect circle and never touched it. Calwen says it is older than anything he keeps; Mara says the ground has offered it only as far as the roots opened. The row has to choose: lift it to Calwen's chest and run the walkway straight, or leave it and walk round it forever.

### MWS.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. Cleanse the site with a rite. | Rejected. No Mire NPC practises anything (bible §11.8); "cleanse" is practical (lift and relay). |
| B. Pure chores. | Rejected. Needs the marker and the choice (dossier questline 4). |
| **C. Three burdens → re-pile at Slack → clear roots → the marker in its ring → lift or leave** | **Selected.** Every dossier element is a concrete verb; the choice has a daily cost either way. |

| Element | Source | Status |
|---|---|---|
| *Weight of the Soil*: personal burdens, collapsed walkways, roots on memory-thick paths, a buried Memorywarden marker, cleanse or preserve | Dossier §XV.4 | [CANON questline] |
| Bog-binding stabilises walkways | Dossier §XVII | [CANON] |
| Griefbit Beetles swarm when fear rises | Dossier §IX; bible §10 | [CANON] |
| Memorywarden shards and markers (H05) | World Truth H05 | [CANON] |
| Calwen keeps what nobody owns; Mara never digs deeper than the ground offers | Anchors II; ledger | [CANON] |
| Dunstan Hayle; `MR_NAME_RECORD` | Bible §5.2, §9.1 | [NEW] |
| Peat Row, Hedda Fallow, Maddy Brook, old Abe Crosse | This package | [NEW] |
| The Peat Row marker's form (office-marked stone, the ring of roots, set before the war) | This package | [PROPOSAL — DIRECTOR] (dossier gives only "a buried Memorywarden marker") |

### MWS.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **P1. The row's head** | Hook | Where Peat Row's walkway leaves Marshfall's main ways. A rota board (chalk, mostly rubbed out). A stake for the row's ditch. |
| **P2. The houses** | Burdens | Five stilt houses. Abe Crosse's peat stack fallen half into the water. A child's gap in the planks with a rope across it. Maddy Brook's house with its door shut and beetle husks on the step. |
| **P3. The sunk section** | Re-piling | A run of walkway where three piles have gone and the planks dip into the water. Crew piles and fascines stacked by it. |
| **P4. The root run** | Roots; marker | The worst stretch: thick black roots across and under the planks, from an old stump at the row's end. Under them, after clearing, the **marker**. |

### MWS.4 Beats

**Beat 0 — A Stranger for a Day (`S00_offer`).** *Objective: Talk to the rota-keeper on Peat Row.* `MWS-D1`.

**Beat 1 — Three Burdens (`S01_burdens`).** *Objective: Help three households (0/3).* Any order.

- **Abe's peat:** lift six fallen turves from the ditch (Slack makes it wadeable; at Running the ditch is a reach-in from the boards, slower) and restack them on his platform (carry-state, two at a time). Abe: "Back's gone. Pride's still here."
- **The child's gap:** lash a split plank across the gap (fetch a plank from the crew pile; one channelled lash, ~3 s). The child walks it at once.
- **Maddy's door:** knock; she will talk through the door. Sit on her step (sit interaction) and listen to her for one exchange (`MWS-D2`). As she speaks of the walkway giving way under her husband's barrow last spring, her fear rises and **Griefbit Beetles** come up through the boards (**MWS-E1**). After the fight, she opens the door: "Sorry. They come when I'm frightened. I'm frightened a lot."

**Beat 2 — Piles at Slack (`S02_piles`).** *Objective: Re-pile the sunk section.* Keep watch to Slack (the ditch stake). Three piles: for each, **set** the pile in the old socket (interaction), **drive** it (channelled, 3 segments of ~3 s; the crew heave with the player; segments persist), and **lash fascines** across the gap (interaction; bog-binding as ordinary repair). Dunstan Hayle comes to help on the second pile (`MWS-B2`, `MR_NAME_RECORD` variants). No skill check; the crew does the weight.

**Beat 3 — Roots (`S03_roots`).** *Objective: Clear the roots from the worst stretch.* Lift four planks (interaction each). Cut five roots (Woodcutting interaction, ~3 s each; any axe; Hedda's crew axe if the player has none). Each cut root is carried to the rootcrafters' pile (EM-09). The fifth root comes away and shows the stone.

**Beat 4 — The Marker (`S04_marker`).** *Objective: Look at what was under the roots.* The strange moment (MWS.6) plays on inspecting the cleared ground. Inspect the marker (`MWS-I5`). Hedda sends for Calwen and Mara (keep watch one turn, or the player walks to Calwen's sanctuary and back; the step completes either way when both are on the row).

**Beat 5 — What It Is and Isn't (`S05_tenders`).** *Objective: Hear Calwen and Mara.* `MWS-D4`. Calwen: older than anything he keeps; like the shard. Mara: the roots have rocked it loose; the ground has offered it this far and no further. With `MR_WARDEN_RECORD` set (MR-M4 done), the player may say the office marks look like the chapel leaves' (`MWS-D4.20`); Calwen: "Then it's theirs, maybe. Doesn't make it anybody's."

**Beat 6 — Lift or Leave (`S06_decide`).** *Objective: Decide what happens to the marker.* `MWS-D5`. MWS.8.

**Beat 7 — The Row (`S07_relay`).** *Objective: Relay the walkway.* Lifted: relay the four planks straight over the cleared ground (four interactions). Left: build the dog-leg round the marker with two new piles (lighter: two interactions each) and four planks. `MWS-D6`. Quest Completed.

### MWS.5 Encounters and hazards

| Id | Enemies / hazard | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MWS-E1** | 2 × Griefbit Beetle (swarm), 1 × Griefbit Beetle (carapace) | Maddy's step (P2) | Swarms spread across the boards; the carapace guards the step. More spawn while Maddy is frightened: one extra swarm if the fight lasts past 30 s (bible §10: "more when an NPC nearby is frightened") | **Swarm surge:** the boards' cracks fill with moving black (~1.0 s), then the swarm rolls a few metres. **Carapace butt:** it rocks back on its legs (~1.2 s) | Required. Teaches that beetles answer fear | 40–60 s |
| **MWS-H1** | Sunk planks | P3 before `S02` | Slow zone | Planks dip into water | Shows why the row needs piles | Movement slowed |

**Rules.** Beetles to 0 HP (CDR-1). Nothing in combat advances the quest's evidence. **Death:** respawn at the row's head; burdens done stay done; driven piles stay driven.

### MWS.6 The ring of roots (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| 0 s | **Cleared** | The fifth root comes away. The player inspects the cleared ground. |
| 0–4 s | **The ring** | The camera stays with the player. Seen from the walkway's edge: every root from the old stump grew toward the stone, and every one turned aside a hand's width short of it, so the roots make a perfect ring round it. Inside the ring the peat is bare and dry. Outside it, wet and root-laced. |
| 4–7 s | **The row** | Hedda, behind the player, stops talking. Abe takes his cap off. |
| After | Inspect | *"The roots all turn aside a hand short of the stone. Inside the ring the peat is dry."* |
| Meaning | None stated. Hedda: "Seen: they went round it. Thought: I don't like it. That's all I've got." It proves nothing about who set the stone or why. |

### MWS.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Talk to the rota-keeper on Peat Row. | `MWS-D1` accept | Yes | — |
| `S01_burdens` | Help three households. | Abe's 6 turves + gap lashed + MWS-E1 defeated and `MWS-D2` end | Yes | Any order |
| `S02_piles` | Re-pile the sunk section. | 3 × (set + 3 drive segments + lash) | Yes | Slack pinned on keep watch |
| `S03_roots` | Clear the roots from the worst stretch. | 4 plank lifts + 5 root cuts | Yes | Crew axe lent if none |
| `S04_marker` | Look at what was under the roots. | Cleared-ground inspect + marker inspect + Calwen and Mara present | Yes | Strange moment |
| `S05_tenders` | Hear Calwen and Mara. | `MWS-D4` end | Yes | `MR_WARDEN_RECORD` option |
| `S06_decide` | Decide what happens to the marker. | `MWS-D5` choice | Yes | Sets `MWS_MARKER` |
| `S07_relay` | Relay the walkway. | Planks (and piles for `left`) + `MWS-D6` end | Yes | Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `MWS_MARKER` = lifted / left | `S06` | Walkway prop; Calwen and Hedda barks; Calwen's unsorted chest inspect (lifted) |

### MWS.8 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Lift it** (`lifted`) — *"Lift it as far as the roots opened. Calwen keeps it. Run the walkway straight."* | Mara rocks it out of the loosened peat by hand (no digging below the roots' depth). Calwen wraps it and takes it to his unsorted chest "with everything else nobody owns". The walkway runs straight. | The row loses the one strange thing it had. Abe: "Feels like taking a stone off a grave." Mara marks the empty ring with a plain stone of her own. | Calwen's chest inspect shows it beside the shard. The straight walkway is the faster path. |
| **Leave it** (`left`) — *"Leave it where it is. Walk round it."* | The walkway dog-legs round the ring on two new piles. The marker stays in its dry ring under the open sky. | Everyone on Peat Row walks further every day for as long as the row stands. Children will dare each other to touch it. | Hedda puts a rail on the dog-leg. Barks about the long way round. |

**Both:** the row is mended, the roots are cleared, nobody says what the marker is or did.

### MWS.9 Rewards

Small payment from the row's pot (economy tuning); Peat Row's walkway as access; rootcrafters' trade (EM-09 root wood bought at the row); Woodcutting, Melee or Ranged XP from actions. No lump XP.

### MWS.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Ditch at Running | Abe's turves reachable from the boards (slower); piles wait for Slack. |
| No axe | Hedda's crew axe (lent, returned at `S07`). |
| Walking away | Stays Active; resume at Hedda. |
| Logout | Last step restored; carried turves return to the ditch edge. |
| Co-op | Per-player row props (piles, walkway, marker state); beetles shared; each player makes their own choice (host fallback for the walkway prop). |

### MWS.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Ditch reach vs wade by state | Systems (N-1) | Two interaction points by state. |
| Fear-scaled beetle spawn | Encounters | One extra wave after 30 s while Maddy's fear flag is on. |
| Root ring reveal | Art | Two environment variants (roots / cleared ring) swapped by step. |
| Walkway variants | Systems | Straight or dog-leg prop set by `MWS_MARKER`. |

### MWS.12 Economy dependencies

EM-09 root wood. Nothing else.

### MWS.13 Mystery ledger entry

| Mystery | Author truth | Public belief | Observable | Wrong reading | Withheld | Owner |
|---|---|---|---|---|---|---|
| The Peat Row marker [PROPOSAL — DIRECTOR] | A Memorywarden marker of the old earth tradition (H05), set before the war; its purpose is not decided. | "Old stone. Leave it." | Office-mark style; roots turn aside; dry peat inside. | A grave; a curse; a Memorywarden buried there. | What it was for. | None in the Mire [PROPOSAL — DIRECTOR]. |

### MWS.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Hedda Fallow** [NEW], Peat Row's rota-keeper | Every household's trouble. | What the marker is. | Brisk, tired, funny once a day. |
| **Abe Crosse** [NEW], old cutter | Peat. | — | Proud; says "back's gone" like weather. |
| **Maddy Brook** [NEW] | That her husband's barrow went through the walkway last spring; he lived, with a bad leg. | — | Frightened, apologetic, honest about it. |
| **Dunstan Hayle** [NEW, bible §5.2] | His household; MR-M1's outcome. | — | Says less than he means; brings food. |
| **Calwen Reed-Binder**, **Mara Fenholt** [CANON] | As ledger. | Whose the marker is. | Calwen refuses to guess; Mara marks with stones, never names. |

**Offer** (`MWS-D1`)

```
MWS-D1.00 [quest Active, returning] HEDDA: "Row's still sinking. Where were we?" (pins step)  → end
MWS-D1.01 HEDDA: "Traveller. You've got hands and you're not from here. That's two things I need."
MWS-D1.02 HEDDA: "Peat Row's worn out. Walkway's going down, roots are coming up, and everyone's too tired to do the one thing that'd help."
MWS-D1.03 HEDDA: "A stranger gets a day's work out of us. Nobody tells a stranger 'we tried that'."
  > "Where do I start?"                                              → MWS-D1.04
  > "Why is everyone so tired?"                                      → MWS-D1.06
MWS-D1.04 HEDDA: "Abe's peat. The Ollen child's gap. And knock on Maddy's door. Then we'll do the hard bit."   {event: accept → S01_burdens}  → end
MWS-D1.06 HEDDA: "Wet comes early. Ground's heavy. Everything takes twice as long and nobody says so." (beat) "Start with Abe."   {event: accept}  → end
```

**Maddy** (`MWS-D2`)

```
MWS-D2.01 MADDY: (through the door) "If you're from the row, I know. I'll come out when it's dry."
  > (sit on her step)                                                → MWS-D2.02
MWS-D2.02 MADDY: "...You sat down. Nobody sits down." (beat) "Last spring Davey's barrow went through the boards by the stump. He came up. His leg didn't, not properly."
MWS-D2.03 MADDY: "Every time I hear a plank creak I see it." (the boards begin to tick)
      {event: MWS-E1 spawns}
MWS-D2.10 [after MWS-E1] MADDY: (door open) "Sorry. They come when I'm frightened. I'm frightened a lot."
  > "Then we'll fix the boards."                                     → MWS-D2.11
  > "It's all right."                                                → MWS-D2.12
MWS-D2.11 MADDY: "Fix the bit by the stump. Then I'll walk it. Once."   → end
MWS-D2.12 MADDY: "It isn't. But thank you for sitting."   → end
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MWS-B0 | Marshfall, MR-M2 done | DUNSTAN | "Hedda's asking for hands on Peat Row. I'd go. I'll bring something." |
| MWS-B1.01 | Abe's peat done | ABE | "Back's gone. Pride's still here. Thank you for not mentioning either." |
| MWS-B1.02 | Gap lashed | OLLEN CHILD | (walks it twice) "It doesn't bounce!" |
| MWS-B2.01 | Second pile, `MR_NAME_RECORD = amended` | DUNSTAN | "Nell sent bread. She said to say 'from your sister' and then laughed, so I'm not saying it." |
| MWS-B2.02 | Second pile, `= qualified` | DUNSTAN | "Brought bread. Nell's Agna's, and that's right. I go and sit at Mara's stone. It's a good stone." |
| MWS-B2.03 | Third pile, `[CAUSEWAY]` | DUNSTAN | "Oswin's crews could've done this in a morning. They've been on the causeway all spring." |
| MWS-B2.04 | Piles done | HEDDA | "Holds. Stamp on it. ...It holds." |
| MWS-B3.01 | Roots, first cut | HEDDA | "Those came off the old stump. Been reaching for the row since before I was born." |

**The tenders** (`MWS-D4`)

```
MWS-D4.01 CALWEN: (crouching at the ring's edge, not inside it) "Older than anything I keep. Like the bit of clay from the causeway."
MWS-D4.02 CALWEN: "I won't say what it is. I don't know what it is."
MWS-D4.03 MARA: "Roots have rocked it. It's loose as far down as they went." (beat) "That's as far as it's offered."
MWS-D4.04 HEDDA: "And the walkway?"
MWS-D4.05 MARA: "Walkway's your business. The stone's not mine either."
  > [MR_WARDEN_RECORD set] "The marks look like the chapel leaves."   → MWS-D4.20
  > "What happens if it's lifted?"                                   → MWS-D4.10
  > "What happens if it's left?"                                     → MWS-D4.12
MWS-D4.10 CALWEN: "It goes in my chest with everything nobody owns. Somebody might ask after it one day. Nobody has yet."   → MWS-D4 options
MWS-D4.12 HEDDA: "We walk round it. Every day. For as long as there's a row."   → MWS-D4 options
MWS-D4.20 CALWEN: "Then it's theirs, maybe. Doesn't make it anybody's." (beat) "Doesn't tell us what it's for either."   → MWS-D4 options
      {MWS-D4 ends when the player picks "Let's decide." → S06}
```

**The choice** (`MWS-D5`)

```
MWS-D5.01 HEDDA: "You did the work. Say."
  > "Lift it as far as the roots opened. Calwen keeps it. Run the walkway straight."   → MWS-D5.10
  > "Leave it where it is. Walk round it."                            → MWS-D5.20
MWS-D5.10 MARA: (kneels, rocks it free by hand, no deeper than it lies) "There. It came."
MWS-D5.11 CALWEN: "Chest, then. With everything else nobody owns."
MWS-D5.12 ABE: "Feels like taking a stone off a grave." / MARA: "Then I'll put one back." (sets a plain stone in the ring)
      {set MWS_MARKER = lifted}  → end
MWS-D5.20 HEDDA: "Long way round, then. Forever." (beat) "Fine. We're good at long ways round."
MWS-D5.21 CALWEN: "It's where it was put. That's something."
      {set MWS_MARKER = left}  → end
```

**Done** (`MWS-D6`)

```
MWS-D6.01 HEDDA: "Row's walkable. Roots are on the rootcrafters' pile. Maddy walked the stump bit. Once."
MWS-D6.02 [lifted] HEDDA: "Straight walkway. Mara's stone in the ring. Abe says hello to it."
MWS-D6.02 [left] HEDDA: "Dog-leg's got a rail. Children are already daring each other."
MWS-D6.03 HEDDA: (hands over coins from the row's pot) "That's the row's. It's not much. It's all of it."
      {event: MWS-D6 end → quest Completed}
```

**Inspect texts**

| Id | Object | Text |
|---|---|---|
| MWS-I1 | Rota board | "Names in chalk, most rubbed out. 'Walkway' written four times and crossed four times." |
| MWS-I2 | Abe's fallen stack | "Half the stack in the ditch. The rest leaning." |
| MWS-I3 | Sunk section | "Three piles gone. The planks dip into the water like a broken back." |
| MWS-I4 | Cleared ground | "The roots all turn aside a hand short of the stone. Inside the ring the peat is dry." |
| MWS-I5 | The marker | "A squat grey stone, knee high. A ring pressed into its top, and small marks round the ring, pressed, not cut. No name." |
| MWS-I6 | Calwen's unsorted chest (lifted) | "A wrapped stone beside a wrapped clay fragment. A tag on each: 'Nobody's.'" |

**MD-7 swap note.** No Hollowfoot content in MWS. No change under either ruling.

### MWS.15 Open decisions

1. The marker's purpose stays withheld [PROPOSAL — DIRECTOR]; no later content should explain it without a ruling.
2. Whether the Mire integration should reuse MR-M2's shard prop style for the marker's marks (recommended: same pressed-mark art, so a player can see the family resemblance without being told).

### MWS.16 Review log

| Finding | Revision |
|---|---|
| "Cleanse" read as a rite. | Made practical: lift to Calwen, relay straight. No Mire NPC practises anything. |
| Mara's canon limit. | She rocks it free only as far as the roots opened; she digs nothing. |
| The ring could prove the marker "works". | Hedda's seen/thought line; the ledger withholds purpose. |
| Dunstan reads `MR_NAME_RECORD` (bible §9.1). | Two variant barks, both kind. |

---

## MHG — The Hushed Granary Key

### MHG.1 Summary card

| Field | Value |
|---|---|
| Content id (suggested) | `mire.side.hushed_granary_key` |
| Type | Settlement (three settlements). Bible §7.2 row; lantern debt (MD-5). |
| Unlock | MR-M2 Completed. Offered at the Hushed Granary's ladder by Tilda Lowry (`MHG-D1`), whose family is flooded out; Ysolde's bark at the register room points there (`MHG-B0`). |
| Resume hook | Tilda at the granary ladder: `MHG-D1.00` "Still locked. Where were we?" |
| Skills | None required. |
| Combat share | 0% (contract: none) |
| Cameo | Ysolde Haverel (the keepers' roll); a Rootrest herbalist |
| Choice | Who keeps the key (`MHG_KEY` = shared / passed / register) |
| Unlocks | The granary as a visitable store; the keepers' roll as an inspect |
| **Anchor** (§7.1) | Three settlements (Marshfall's granary, Sorrowmere's register room, Rootrest's herbalists). |
| **World-truth row** | H23 (recovery: emergency stores, uneven care). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed; `MHG_KEY`; no fail; the family is fed in every outcome. |
| **Combat compliance** | None. |

**In one paragraph.** The Hushed Granary is the Mire's raised emergency store, opened once before every flood season by its keeper, Wystan Crale, who has held the key since he was young and whose hands now shake. This year the key is gone. Tilda Lowry's croft went under in the first rain of the wet and she has three children in a borrowed loft; the store's rule says nothing leaves before the Silt hearing, and the hearing sits after the rain. Some say theft; some say someone has been in through the old flood hatch; some say old Wystan has lost his wits. The player reads the silt apron round the ladder (only one set of prints, an old man's, coming and going), opens the flood hatch underneath at Slack (a new rope on the pin, a little grain spilled, and nothing missing when the sacks are weighed against the tally board), and follows a griefroot balm to Rootrest, where the herbalist says Wystan wears the key on a cord under his shirt. Wystan has not lost it. He hid it, because the three settlements mean to give it to a younger keeper before the wet and he is afraid of being "put by". Then the player sees his lantern moving inside the locked store at night. The key's custody is decided at the granary; in every outcome Tilda is fed that night, because Tilda once walked Wystan home through a dark night, and she asks for her lantern debt.

### MHG.2 Selection record and canon grounding

| Candidate | Verdict |
|---|---|
| A. A thief; catch him. | Rejected. The bible's pitch offers three readings; making it a crime flattens a care story. |
| B. A Silt hearing scene. | Rejected. Talk-led resolution only in closing beats; the hearing sits after the rain anyway. |
| **C. Test three readings with physical evidence (prints, hatch, weights) → a testimony at Rootrest → a lantern in a locked store → custody, with the family fed by lantern debt** | **Selected.** "Weigh" is literal; each theory is tested by something the player does; lantern debt does the urgent work without overriding the hearing. |

| Element | Source | Status |
|---|---|---|
| The Hushed Granary (raised emergency store) | Part 3 Mire proposal; bible MP22 | [NEW, Part 3, adopted MD-5] |
| Lantern debt (never hereditary); Silt hearing (no appeal rules stated) | Part 3 Mire proposal; bible MD-5 | [NEW, adopted]; the custom as played here (owed by the one walked home, paid on asking) is [PROPOSAL — DIRECTOR] |
| Rootrest herbalists; griefroot balms | Dossier §VII.4, §XI (griefroot resin "used in calming balms") | [CANON] (resource legacy) |
| Ysolde; "two holds" | Bible §1.1, §5.2 | [NEW] |
| Wystan Crale, Tilda Lowry, Briony Jessop | This package | [NEW] |

### MHG.3 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **G1. The granary** (MP22) | Hook; evidence | A timber store on tall stilts over Marshfall Edge's wet ground, reached by a ladder to a locked door. A **silt apron** of smoothed grey silt round the ladder foot (keepers smooth it so prints show). A small stake by the stilts. A **flood hatch** in the floor, reached from below at Slack. A **tally board** inside the door (read through a gap) and the same board's copy nailed by the ladder. |
| **G2. Under the store** | Hatch | Between the stilts, knee-deep at Running, mud at Slack. The hatch's pin and a coil of rope. |
| **G3. The weighing beam** | Weighing | Inside the store (after the hatch): a hanging balance beam, sacks in rows, chalk marks on each row. |
| **G4. The register room** (MP01) | Keepers' roll | The Names Below room; a second book on the shelf: the **keepers' roll** (who has held which store's key). |
| **G5. Rootrest herbalist's** (MP04) | Testimony | A root-sheltered home with balm pots; griefroot hanging. |
| **G6. Wystan's hut** | Wystan | A one-room hut near the granary, a lantern by the door, a chair facing the store. |

### MHG.4 Beats

**Beat 0 — Locked (`S00_offer`).** *Objective: Find out what happened to the granary key.* `MHG-D1`. Tilda explains: three children, a borrowed loft, the rule, the hearing after the rain. Three readings in the air (theft, the hatch, Wystan).

**Beat 1 — The Apron (`S01_apron`).** *Objective: Read the silt round the ladder.* Inspect the apron (`MHG-I1`): one set of prints, short and dragging, coming and going, many times over. No others. Inspect the door lock (`MHG-I2`): unforced. Theft by the door is unlikely; the prints are the keeper's (the player learns the drag when they meet Wystan).

**Beat 2 — The Hatch (`S02_hatch`).** *Objective: Look at the flood hatch.* Keep watch to Slack (the store's stake). Under the store (G2): a **new rope** on the hatch pin (`MHG-I3`), a little grain spilled in the mud. Pull the pin (interaction) and climb in (the hatch is the old flood bypass; it opens from below only).

**Beat 3 — Weigh It (`S03_weigh`).** *Objective: Weigh the sacks against the tally.* Inside, three rows of sacks. For each row, hang one sack on the beam (interaction) and read the beam against the row's chalk mark; compare with the tally board (inspect). All three rows match (authored). Nothing is missing. (A curious player who weighs a second sack per row gets the same.) The hatch has been used to **check** the store, not to take from it. Climb out and re-pin (interaction).

**Beat 4 — Two Holds for a Key (`S04_roll`).** *Objective: Ask about the keeper.* Two sources, any order:

- **Sorrowmere register room** (G4): Ysolde opens the **keepers' roll**: Wystan's name against the Hushed Granary since "the winter the ice took the ferry", and in a newer hand a pencilled line: *"To pass to Briony Jessop before the wet. Three settlements agree."* Ysolde: "That's a plan, not a record. It's in pencil for a reason."
- **Rootrest herbalist** (G5): Wystan comes every week for griefroot balm for his hands. "He wears a key on a cord under his shirt. I've seen it when I do his wrists. I didn't think it was my business." (`MHG-D3`)

**Beat 5 — The Lantern in the Store (`S05_night`).** *Objective: Find Wystan.* At Wystan's hut (G6) by day he is not there; the chair faces the store. Keep watch to night. The strange moment (MHG.6): a lantern moves inside the locked store. Wait at the ladder: Wystan comes out through the hatch below, lantern in hand, and finds the player there. `MHG-D4`: he has the key. He hid it because they mean to give it to Briony before the wet and "put him by". He has been checking the sacks every night because he is afraid of being wrong.

**Beat 6 — The Key (`S06_decide`).** *Objective: Decide who keeps the key.* At the ladder at morning: Wystan, Tilda, Briony Jessop (a young Reedsward woman), and Ysolde (who comes from Sorrowmere with the roll). `MHG-D5`. Before the custody choice, Tilda asks Wystan for her lantern debt (MHG.8); he pays it in every outcome.

**Beat 7 — Lantern Debt (`S07_debt`).** *Objective: Walk Tilda's sack home by lantern.* At dusk Wystan opens the store (with whoever now keeps the key, per the choice), weighs out one sack, chalks the tally, and walks it to Tilda's borrowed loft by lantern; the player carries the lantern (carry-state) and walks beside him (escort at his pace). `MHG-D6`. Quest Completed.

### MHG.5 Encounters and hazards

None. **Under the store** at Running is non-walkable (the hatch step pins Slack on keep watch).

### MHG.6 The lantern in the store (presentation spec: unease)

| Time | Element | Spec |
|---|---|---|
| Night | **Locked** | The granary dark on its stilts; the door's lock visible from the ladder foot. |
| 0–5 s | **Light** | A lantern light moves inside the store, seen through the board gaps: along the first row, stopping, along the second. |
| 5–10 s | **The beam** | The faint creak of the weighing beam. Then quiet. Then the light again. |
| 10–20 s | **Below** | The light goes down and out of sight; under the store, the hatch pin rattles; an old man climbs down with a lantern. |
| Meaning | An old man checking sacks. It looks like something else for twenty seconds. Proves nothing. |

### MHG.7 Steps and flags

| Step | Objective | Completes on | Required | Notes |
|---|---|---|---|---|
| `S00_offer` | Find out what happened to the granary key. | `MHG-D1` accept | Yes | — |
| `S01_apron` | Read the silt round the ladder. | Apron + lock inspects | Yes | — |
| `S02_hatch` | Look at the flood hatch. | Keep watch to Slack + rope inspect + pull pin | Yes | — |
| `S03_weigh` | Weigh the sacks against the tally. | 3 rows weighed + tally board inspect + re-pin | Yes | All match |
| `S04_roll` | Ask about the keeper. | Keepers' roll inspect with Ysolde (`MHG-D2`) + `MHG-D3` end | Yes | Any order |
| `S05_night` | Find Wystan. | Keep watch to night at G6 or G1 + lantern event + `MHG-D4` end | Yes | — |
| `S06_decide` | Decide who keeps the key. | `MHG-D5` choice | Yes | Sets `MHG_KEY` |
| `S07_debt` | Walk Tilda's sack home by lantern. | Escort complete + `MHG-D6` end | Yes | Quest Completed |

| Flag | Set by | Read by |
|---|---|---|
| `MHG_KEY` = shared / passed / register | `S06` | Granary props (a second cord, a new keeper at the ladder, or the key's peg in the register room); barks |

### MHG.8 Choices and consequences

**Lantern debt (before the choice, every outcome) [PROPOSAL — DIRECTOR].** Tilda: "Wystan. The night of the hard frost, three winters back, I walked you home from the jetty. You said if I ever asked." Wystan: "I said." Under lantern debt, the one who was walked home owes a lantern-walk when asked; it is the asker's own and is never inherited. Wystan owes Tilda, not her children; he pays by opening the store and walking a sack home by lantern. The Silt hearing is not overridden: a lantern debt is a person's own gift from a store they keep (MD-5: no hearing rules stated; this is a practice, not a ruling).

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Two on the cord** (`shared`) — *"Wystan keeps it. Briony keeps it with him. Two holds for a key."* | Wystan and Briony each wear a key (Ysolde has the smith-less Mire's answer: Wystan's key and the store's old spare, found in the roll's box). The store opens only with both present. | Slower: two people must agree to every opening. Wystan is not put by, but he is watched. | Briony at the ladder in the mornings, Wystan in his chair. They argue about chalk. |
| **Pass it** (`passed`) — *"It's time, Wystan. Give it to Briony."* | Wystan takes the cord off and gives it to Briony at the ladder. Ysolde inks the pencilled line. | Wystan is put by. He says he is glad. His chair still faces the store. | Briony keeps the store well. Wystan visits every night "to see it's still there". |
| **The register keeps it** (`register`) — *"Hang it in the register room. Anyone may ask; Ysolde writes who did."* | The key goes on a peg in Sorrowmere's register room. Each opening is written. | The store is a long walk from its key. Marshfall grumbles. Wystan is relieved and hurt at once. | Peg prop in the register room; Ysolde's line in the roll for each opening. |

No option is wrong. Tilda's family is fed in all three.

### MHG.9 Rewards

Tilda's thanks; a small payment from the three settlements' store fund (economy tuning). The keepers' roll as an inspect. No XP beyond actions (there are no skill actions; this is a talk-and-inspect quest with walking).

### MHG.10 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Comes at Running | Under the store is water; keep watch. |
| Weighs a row wrong | The beam reading is shown; nothing can be weighed "wrong". |
| Walks away | Stays Active; resume at Tilda. |
| Logout during the lantern walk | Resumes at the ladder at dusk. |
| Co-op | Per-player state; the lantern walk is per player; the key prop follows each player's `MHG_KEY` (host fallback). |

### MHG.11 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Silt apron prints | Art | Decal set (one track pattern). |
| Hatch reachable at Slack | Systems (N-1) | Walkable under-store volume at Slack. |
| Weighing beam station | Systems | Interaction showing the beam settle against a chalk mark; authored match. |
| Night lantern inside a locked store | VFX | Moving light behind board gaps on keep watch to night. |
| Escort at an old man's pace | Systems | Lowmark escort convention. |

### MHG.12 Economy dependencies

EM-11 grain sacks (station props only; nothing taken by the player).

### MHG.13 Mystery ledger entry

None (resolved in-quest).

### MHG.14 Dialogue

**Cast notes**

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Tilda Lowry** [NEW] | Her croft is under water; the rule. | Where the key is. | Practical, polite, at the end of her rope. |
| **Wystan Crale** [NEW], granary keeper | The store, every sack, his own fear. | How to say he is afraid. | Stiff, proud, shaky hands; "put by" is his worst word. |
| **Briony Jessop** [NEW], Reedsward woman named in pencil | That she was chosen; that Wystan hates it. | — | Kind, sure, slightly too quick. |
| **Ysolde Haverel** [NEW, bible §5.2] | The roll. | — | "Two holds, one name." Will not round. |
| **Rootrest herbalist** (role) | Wystan's hands and his cord. | — | Gentle, careful about what is her business. |

**Offer** (`MHG-D1`)

```
MHG-D1.00 [quest Active, returning] TILDA: "Still locked. Where were we?" (pins step)  → end
MHG-D1.01 TILDA: "Sit, if you like. There's nothing to eat, so I can't offer that." (a short laugh) "That's the problem."
MHG-D1.02 TILDA: "My croft went under in the first rain. Three children in a borrowed loft. The store's full and nothing leaves before the Silt hearing."
MHG-D1.03 TILDA: "Hearing sits after the rain. And the key's gone anyway."
  > "Gone how?"                                                      → MHG-D1.04
  > "Who keeps it?"                                                  → MHG-D1.06
MHG-D1.04 TILDA: "Depends who you ask. Stolen. Or somebody's been in through the old flood hatch. Or old Wystan's lost it, and his wits with it."   → MHG-D1.07
MHG-D1.06 TILDA: "Wystan Crale. Since before I was born. His hands shake now. They want to give it to somebody younger."   → MHG-D1.07
MHG-D1.07 TILDA: "Look at the store. I can't. I keep thinking about what's in it."   {event: accept → S01_apron}  → end
```

**Ysolde and the roll** (`MHG-D2`)

```
MHG-D2.01 YSOLDE: "The keepers' roll. Every store, every key, who held it." (opens it) "Wystan Crale. Hushed Granary. Since the winter the ice took the ferry."
MHG-D2.02 YSOLDE: (a finger on the pencil) "And this. 'To pass to Briony Jessop before the wet. Three settlements agree.'"
MHG-D2.03 YSOLDE: "That's a plan, not a record. It's in pencil for a reason."
  > "Does Wystan know?"                                              → MHG-D2.04
  > "Would you write that the key was lost?"                         → MHG-D2.06
MHG-D2.04 YSOLDE: "He was told. Being told isn't agreeing."   → end
MHG-D2.06 YSOLDE: "I'd write that somebody said it was. Not found is a record too. Lost is a story."   → end
```

**The herbalist** (`MHG-D3`)

```
MHG-D3.01 HERBALIST: "Wystan? Every week. Griefroot balm for his hands. They shake worse in the wet."
MHG-D3.02 HERBALIST: "He wears a key on a cord. Under his shirt. I've seen it when I do his wrists."
MHG-D3.03 HERBALIST: "I didn't think it was my business. I suppose it's somebody's now."   → end
```

**Wystan** (`MHG-D4`, at the ladder, night)

```
MHG-D4.01 WYSTAN: (climbing down, lantern first) "...Who's there?"
MHG-D4.02 WYSTAN: "The stranger. Of course. They'd send the stranger."
  > "You have the key."                                              → MHG-D4.03
  > "You've been checking the sacks."                                → MHG-D4.05
MHG-D4.03 WYSTAN: (a hand to his chest, on the cord) "I've had it fifty years. I haven't lost it once."   → MHG-D4.06
MHG-D4.05 WYSTAN: "Every night. Every row. In case I'd got it wrong. I never had."   → MHG-D4.06
MHG-D4.06 WYSTAN: "They wrote me out in pencil. Before the wet. 'Put by.' Like an old net."
MHG-D4.07 WYSTAN: "If I said I'd lost it, they couldn't take it. That's all. It was stupid. I knew it was stupid."
  > "Tilda's children need feeding."                                 → MHG-D4.08
  > "Nobody thinks you got it wrong."                                → MHG-D4.09
MHG-D4.08 WYSTAN: "I know. I know they do. I'd have opened for her. I'd have had to say where the key was."   → MHG-D4.10
MHG-D4.09 WYSTAN: "Then why write me out?"   → MHG-D4.10
MHG-D4.10 WYSTAN: "Morning. At the ladder. Bring whoever has to be brought."   {event: S05 complete}  → end
```

**The key** (`MHG-D5`)

```
MHG-D5.01 TILDA: "Wystan." (beat) "The night of the hard frost, three winters back, I walked you home from the jetty. You said if I ever asked."
MHG-D5.02 WYSTAN: "I said." (beat) "That's yours. Not the hearing's. I'll pay it tonight, whatever happens to this." (touches the cord)
MHG-D5.03 YSOLDE: "Lantern debt's the asker's own. It doesn't pass to anyone. That's why it's allowed."
MHG-D5.04 BRIONY: "I don't want it like this. Not taken off him."
MHG-D5.05 YSOLDE: (to the player) "You looked at everything. Say who keeps it."
  > "Wystan keeps it. Briony keeps it with him. Two holds for a key."  → MHG-D5.10
  > "It's time, Wystan. Give it to Briony."                            → MHG-D5.20
  > "Hang it in the register room. Anyone may ask; Ysolde writes who did."   → MHG-D5.30
MHG-D5.10 YSOLDE: "There's the old spare in the roll's box. Nobody's needed it." (holds it up)
MHG-D5.11 WYSTAN: "She'll chalk wrong." / BRIONY: "Then you'll tell me." / WYSTAN: "...I will."
      {set MHG_KEY = shared}  → MHG-D5.40
MHG-D5.20 WYSTAN: (a long moment; takes the cord off over his head) "Weigh the second row twice. It always looks light. It never is."
MHG-D5.21 BRIONY: "Twice. I'll remember."
MHG-D5.22 YSOLDE: (inks over the pencil) "There. A record now."
      {set MHG_KEY = passed}  → MHG-D5.40
MHG-D5.30 YSOLDE: "On a peg, by the door. Every opening written, every name."
MHG-D5.31 WYSTAN: "So nobody has it." / YSOLDE: "So everybody can see who had it."
MHG-D5.32 TILDA: "It's a long walk from the store." / YSOLDE: "Then people will only ask when they mean it."
      {set MHG_KEY = register}  → MHG-D5.40
MHG-D5.40 WYSTAN: "Dusk. I'll open for Tilda. Somebody bring a lantern. Mine's nearly out."   {event: S06 complete}  → end
```

**The walk** (`MHG-D6`, at Tilda's loft)

```
MHG-D6.01 WYSTAN: (setting the sack down) "There. Owed and paid."
MHG-D6.02 TILDA: "Paid." (to the children in the loft) "Say thank you to the keeper."
MHG-D6.03 CHILDREN: (overlapping) "Thank you, keeper."
MHG-D6.04 [MHG_KEY = passed] WYSTAN: (very quietly) "Keeper." (beat) "Well. For tonight."
MHG-D6.04 [else] WYSTAN: "Go to sleep, the lot of you."
MHG-D6.05 WYSTAN: (to the player) "You can put the lantern out. I know the way."
      {payment; event: MHG-D6 end → quest Completed}
```

**Barks**

| Id | Trigger | Speaker | Line |
|---|---|---|---|
| MHG-B0 | Register room, MR-M2 done | YSOLDE | "Tilda Lowry's at the Hushed Granary with a problem I can't write my way out of. You might be able to walk your way out of it." |
| MHG-B1.01 | Apron inspected | log | "One set of prints. Short steps, one foot dragging. Over and over." |
| MHG-B1.02 | All rows weighed | log | "Every row matches the tally." |
| MHG-B2.01 | Post-quest, `shared` | BRIONY | "He made me weigh the second row twice. It wasn't light." / WYSTAN: "It never is." |
| MHG-B2.02 | Post-quest, `passed` | WYSTAN (in his chair) | "Still there. Good." |
| MHG-B2.03 | Post-quest, `register` | YSOLDE | "Three askings this week. All written. All meant." |

**Inspect texts**

| Id | Object | Text |
|---|---|---|
| MHG-I1 | Silt apron | "Smoothed silt. One set of prints, short and dragging, coming and going, many times." |
| MHG-I2 | Door lock | "An old lock. No marks on it but a key's." |
| MHG-I3 | Hatch pin rope | "New rope, knotted by someone whose fingers don't close properly." |
| MHG-I4 | Tally board | "Three rows. A chalk weight for each. Checked off in the same shaky hand every night, back as far as the board goes." |
| MHG-I5 | Keepers' roll | "Wystan Crale, Hushed Granary. Then, in pencil: 'To pass to Briony Jessop before the wet.'" |
| MHG-I6 | Register room key peg (`register`) | "A key on a peg. Beneath it a page: who asked, when (by bell and weather), and what for." |

**MD-7 swap note.** No Hollowfoot content in MHG. No change under either ruling.

### MHG.15 Open decisions

1. Lantern debt as written here (owed by the one walked home, paid on asking, never inherited) is a [NEW] reading of the Part 3 practice. Director may adjust; only `MHG-D5.01`–`.03` and `MHG-D6` change.
2. The "old spare" key in the roll's box exists so `shared` needs no smith (MD-11). If the Director prefers one key, `shared` becomes "Wystan keeps it, Briony must be present", lines only.

### MHG.16 Review log

| Finding | Revision |
|---|---|
| Draft let the stranger open the store under emergency authority. | Cut. The stranger decides custody only because three settlements ask; the family is fed by a lantern debt that belongs to Tilda, not by overriding the hearing. |
| Wystan risked being comic or pitiful. | He is right about the sacks every night; his fear is named, not mocked. |
| Dating. | "The winter the ice took the ferry", "the night of the hard frost": weather, never a date. |

---

## Integration summary (file level)

| Need | Used by | Owner | Notes / fallback |
|---|---|---|---|
| Channel-state toggles (reed stands, banks, ditch, under-store) | MRS, MFH, MWS, MHG | Systems (bible N-1) | Quest-pinned states as fallback. |
| Keep watch / presentation hour | All five | Systems | Lowmark convention; never world time. |
| Authored-result test stations (roll, flex, gauge, beam) | MRS, MFH, MHG | Systems | One interaction type returning an authored result per object. |
| Timing window on a bob loop (marks, net) | MRS | Gameplay | Shared by shot and net. |
| Rowing crossing (player as rower) | MFH | Systems | Lowmark ferry convention variant; no physics. |
| Staged flood variant | MFT | Systems | N-3 pattern (environment variants by step). |
| Carry-state objects with deposit targets | All five | Systems | Lowmark pattern. |
| Per-player props | All five | Systems | Host fallback. |
| Quest-start skill requirement on offer | MRS, MFH | Systems / Schema | A requirement check on the accept option; decline line shown. Standard RPG requirement (CDR-4). |

No new runtime system beyond those in bible §11.1–11.2; the quest-start requirement is a standard requirement check.

## Package review summary

| Check | Result |
|---|---|
| Brief fit (bible §7.2–7.3) | MRS, MFT, MFH, MWS, MHG match their rows: core verbs, places, unlocks, contracts (MRS one Reedlurker and fowl; MFT no combat; MFH Bog Hounds; MWS beetles and lift/leave; MHG custody choice, no combat). MRS teaches the Fletching → Ranged → Hunting loop with feathers back to Fletching; item names are economy proposals (MD-11). |
| CDR-1 | Every enemy to 0 HP; no yield, flee or break-off; no SX; no defeated enemy speaks. |
| CDR-2 | Every fight accepts melee or ranged; MRS's shots all have the net/call alternative; no step requires ranged. |
| CDR-3 | No release wording. |
| CDR-4 | Standard systems only; light quest-start requirements on MRS (Hunting) and MFH (Woodcutting) as `[GD]` placeholders; MRH's is in the sister file. |
| Mains' reads | MRS Completed (Act III §E.10 variant); MFT Completed (Act III `MBL-D2b.21`); `MNS_BROTH` read in `MFT-D1.03`; `MR_NAME_RECORD` read in MWS. *Lifting Day* is not in this file (Names and Lanterns package). |
| Flags | Quest-local only; no `MR_` flag set. |
| Quest items | 0. |
| Dating and R08 | No calendar dates (weather and bell-nights only). No war history, unit, number or casualty count anywhere. |
| MD-7 | No Hollowfoot enemy; Jory Wick non-combatant `[MD-7]` in MFT; swap note per quest. |
| New names checked for collisions | Gwenna and Cadan Tolley, Hedda Fallow, Abe Crosse, Maddy Brook, Wystan Crale, Tilda Lowry, Briony Jessop, Bettany Strand, Hal and Arno Pellow, Nessa: grepped against the repository (no matches outside this file). |
| Deviations from the bible | (1) Quest-start skill requirements on MRS and MFH (bible §13 recommendation; §7.2 "crew alternative" kept for taught skills). (2) MFT names Jory Wick (Act III cast) at Fenward, consistent with Act III. (3) Hob's pronoun is "he", matching Act I and Act III. |
| Independent review (2026-11-09) | Fixed: MFH `S05` objective "Drive the dogs off the racks" (drive-off wording, CDR-1) now "Defeat the dogs at the racks" (beat and step table); EM-01 to EM-11 labelled as economy-pass proposal labels, not catalog ids, and Hob's lent bow and commission bow labelled item-name proposals (§0.3); lantern debt as played in MHG tagged [PROPOSAL — DIRECTOR] (MHG.2, MHG.8); the Peat Row marker's form tagged [PROPOSAL — DIRECTOR] (MWS.2, MWS.13); stale Hob-pronoun open item closed (Act III now reads "he"). Verified: every enemy to 0 HP; no step requires ranged (net/call path at every shot); Hunting and Woodcutting start gates are `[GD]` placeholders on the skill each quest builds on, with crew alternatives on taught-skill steps; three states, no fail paths; MFT completes at `S06_table` as Act III `MBL-D2b.21` reads; MD-7 notes; no calendar dates or casualty counts; new names grep clean. |
