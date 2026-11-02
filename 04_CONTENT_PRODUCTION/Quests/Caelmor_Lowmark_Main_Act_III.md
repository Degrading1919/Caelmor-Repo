# Lowmark Main Questline — Act III (MQ10–MQ12)

**Status:** Authored production content for Creative Director milestone review. This package implements Lowmark main-arc **movements 10, 11 and 12** (`00_ADMIN/Reference/Caelmor_Part5_Lowmark_Main_Arc_Architecture.md`) as main quests 10–12 of `Caelmor_Lowmark_v1_Narrative_Production_Bible.md` (§6, §6.1). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[PROPOSAL — DIRECTOR]** marks consequential choices the content is built on. **[CANON]** marks material taken from Phase 1 or the reconciled `LORE/` files. No schema, production JSON or C# is created here.

**Companion file:** `04_CONTENT_PRODUCTION/Dialogue & Narrative/Caelmor_Lowmark_Main_Act_III_Dialogue.md` (Act III cast notes, every dialogue node, barks, MQ12 variant lines). The True Line voice rules (cast file Part 1) are binding on every line.

**Format:** each quest follows `Caelmor_Lowmark_Quest_The_True_Line.md`. Nodes naming Edda Marrick or Gideon Sallow are tagged `[ANTAGONIST]` here and in the dialogue file (bible §3.1 swap layer).

---

## 0. Act III header

### 0.1 What the act does

Act I found the scheme. Act II found what the scheme broke and who can mend it. Act III makes the mending **public, physical and shared**: the player saves the records from fire and lays them on a table (MQ10), stands in the fen on the night it lets go (MQ11), and walks the Vale to see what the work changed (MQ12). The act ends with the Vale doing what Oriel asked of it, and with the one person who never crosses at night crossing at night.

| Quest | Code | Core verbs (primary first) | Distinct from |
|---|---|---|---|
| MQ10 The Crest Hall Reckoning | CR | **defend a building** (fire, carry, gate, miniboss), then **lay evidence** | TL proof is talk at a tollpost; MQ10 proof is objects carried to a table. MQ4's assault is attacking a site; MQ10 is defending one. |
| MQ11 Stillwater's Vigil | SV | **escort, hold gates, boss**, then **seat a post** | MQ3's single rescue becomes a mass evacuation with a mechanic; MQ4's single crank becomes three sequenced gates (the arc's culminating channel set piece; MQ6 and MQ7 deliberately use other loops); TL's seat-the-post returns as the climax. |
| MQ12 The River Remains | RR | **journey, light, cross** | The only quest whose core is travel and witness. Combat-free by design. |

**Length:** MQ10 40–45 min; MQ11 45–55 min (longest main quest; it is the Act III climax); MQ12 15–20 min required, up to 40 min with every optional station.
**Level framing:** MQ10–11 assume Milestone 3 (advanced specialist equipment). MQ12 opens Milestone 4 commission legitimacy (bible §6, §8). Exact levels belong to the Gameplay Designer.

### 0.2 Inputs read (region flags set by Acts I and II)

Act III never asks how an earlier flag was set; it reads only the §9.1 values. Every value has authored content. No input value can block progress.

| Flag | Values | Read in | Effect in Act III |
|---|---|---|---|
| `LM_TL_EVIDENCE` | keepers / riverfolk / player | MQ10 chip C1; MQ12 Hollis | Where the Whisperflow proof is when the hall burns, and its weight (§10.5). |
| `LM_GRAIN_ROUTE` | escort / hold / split | MQ10 Marrick's argument and terms clause; MQ12 far-bank arrival | How strong Marrick's "the far bank would have rioted" defence is; how many far-bank lanterns meet the ferry. |
| `LM_LOCK_STATE` | smashed / chained | MQ10 chip C5; MQ10 lead-in line | Chained gives the keepers' in-place inspection (stronger chip); smashed gives only the post stock. |
| `LM_FIELD_FIX` | circle / plot / dike | MQ12 Ashenstead station | What Joric's field and Annelise's circle look like. |
| `LM_TOVIN_CREDITED` | named / unsigned | MQ10 chip C6 weight and Tovin's stand; MQ12 keepers' hall | Named: Tovin stands at the table. Unsigned: his sheets are laid without him. |
| `LM_FLUSH_CALENDAR` | bool | MQ10 chip C6 exists | Always true after MQ6; authored false fallback in §10.5. |
| `LM_BRYN_ROLL` | commons / household | MQ10 plan roll wording; MQ12 orchard | How Bryn is named on the Braid roll. |
| `LM_ORCHARD_LOSS` | none / partial | MQ12 orchard | Orchard props and Bryn's line. |
| `LM_SEDGE_TRUST` | warm / cool | MQ10 Sedge's dusk lines; MQ11 Sedge lines; MQ12 refusal | Warmth of Sedge's words; never changes mechanics. Rule (Act II §MN.8): **cool** if `MN_ELK_KILLED` or the player named him the Field-Mage aloud (`MN_SAW = mage`); otherwise **warm**. No Act III line refers to either cause. |
| `LM_ORIEL_PROMISE` | aloud / many_hands / return | MQ12 Oriel | Oriel quotes the player's exact MQ9 words back (`RR-D4.02`). |

### 0.3 Side-quest conditions read (never required)

| Condition | Read in | Effect |
|---|---|---|
| `UL_LEDGER` (side quest UL, *Under the Lamb*) | MQ10 | Chip C8, the **crew ledger** (Rhosyn's pages included): pay drawn on "the Provisioner's purse", Board seal stamped on the pay chits. Weaker if `UL_LEDGER_CUT` (chit pages cut out). |
| `UL_RHOSYN_WITNESS` | MQ10; MQ12 | Rhosyn attends under keeper protection and attests the ledger hand (+1 weight to C8; not a chip by itself). Without it she is absent from the hearing. Nothing requires her. |
| `UL_RHOSYN_WITNESS` / `UL_RHOSYN_STAYS` / `UL_RHOSYN_FLED` | MQ12 Brookhollow | Rhosyn's MQ12 scene branches on the UL outcome, with a default for players who never did UL (`RR-D19`). |
| completed side quest FW (*Fen Watch*) | MQ11 | Lessa's guide route opens as a second, faster evacuation lane. |
| completed side quest CN (*The Candle Rule*) | MQ11 choice; ending | Annelise brings the recovered offering boat to the dawn choice; the Tend option gets its strongest argument and a launched-boat prop in the Tend/Shared ending. |
| `OL_JOSS_IN` / `OL_LANTERN_ONLY` (side quest OL, *Old Lantern*) | MQ11 arrival and choice; MQ12; Ending matrix | `OL_LANTERN_ONLY`: Ansel speaks for Shared and hangs Joss Garrow's dark lantern at the edge. `OL_JOSS_IN`: Joss is among the Reedmere evacuees in Elspeth's care; Ansel speaks with Joss sitting by the stove. Not done: Ansel speaks raw. If OL is complete, drift site `old_lantern_bend` stays **quieted** in every fen ending. His MQ12 patrol book opens differently per value. |
| `VK_COMPLETE`; `VK_PERF_BOTH` / `VK_PERF_COUNT` / `VK_PERF_HUM` (side quest VK, *A Verse Kept Back*) | MQ11 after-hold; MQ12 far bank | A cutter hums the listeners' tune after the fen exhales. Nan's MQ12 song follows the performance the player chose in VK; without VK she hums the listeners' tune with its verse missing (`RR-D7.04`). |
| completed side quest UR (*Unreplanted*) | MQ12 Ashenstead | Joric's line reflects what he decided about the ground. |
| completed side quest NT (*Night Ferry*) | MQ12 Whisperflow | Dace is in the crossing crew and says one line. |
| completed side quest BP / HS | MQ12 hand-off | Kell Ashby / Brigid Corliss deliver their commission line in person at the end. |

### 0.4 Region flags this act sets

| Flag | Values | Set by | Notes |
|---|---|---|---|
| `LM_MARRICK_EXPOSED` | bool | MQ10 `S08_table` | Always true at MQ10 completion (a guaranteed three-chip path exists, §10.5). How exposed is carried by quest-local `CR_TERMS`. |
| `LM_HESKETH` | kept / stood-down | MQ10 `S09_hesketh` | Read by MQ12 and the Crestbridge Guard commission giver. |
| `LM_PLAN_ROUTES` | crews / keepers / shared | MQ10 `S10_plan` | Member of the bible's `LM_PLAN_*` family: the route keeper. |
| `LM_PLAN_MEMORIAL` | watchers / gardens / reedmere | MQ10 `S10_plan` | Member of `LM_PLAN_*`: the memorial keeper. |
| `LM_FEN_ENDING` | seal / tend / shared | MQ11 `S08_choose` | Drives drift-site states, Stillwater presentation, MQ12 (§ Ending matrix). |
| `LM_CIVIC_STANDING` | bool | MQ12 `S06_far_bank` | Narrative legitimacy for the four aspirational commissions. |

`LM_PLAN_ROUTES` and `LM_PLAN_MEMORIAL` are the two members of the bible's `LM_PLAN_*` family ("route keeper, memorial keeper"), not new region flags.

### 0.5 Quest-local flags other packages read

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `CR_TERMS` | bare / firm / full | MQ10 | MQ11 vigil supplies line; MQ12 Marrick, Crestbridge, far bank |
| `CR_MARRICK_STORES` | offered / ordered | MQ10 | MQ11 (food at Reedmere); MQ12 households' wording |
| `CR_CREW_LENIENCY` | bool | MQ10 | MQ11 (Lock crew at gate 1); MQ12 Sallow |
| `CR_RHOSYN_LAID` | bool | MQ10 (C8 laid with `UL_RHOSYN_WITNESS`: she attested) | Side-quest package (UL epilogue). MQ12 reads the UL flags directly. |
| `RR_MARK` | notch / ring / hatch | MQ12 | Whisperflow stone prop, post-game |

### 0.6 Quest items (bible §11.6: at most 2 per act package)

| Item | Quest | Notes |
|---|---|---|
| `CR_board_minute` | MQ10 | The Provision Board's minute book. The only new quest item in Act III. Its seal text is one of the three swap-layer documents (bible §3.1). |

Everything else in Act III is carry state (record bundles, soaked sacks, a pre-notched post, evacuee lanterns, the heart-stone post, a restitution sack) or a loaned tool (Watcher smoke-pot). **Act III uses 1 of its 2 allowed quest items.**

### 0.7 Canon grounding (Act III)

| Element | Source | Status |
|---|---|---|
| Public plan with named roles, no new government; side stories alter testimony but are not required | Main Arc movement 10 | Proposal (approved structure) |
| Dangerous currents, trance-like grief responses, Wraith-like manifestations; no option kills grief or releases souls | Main Arc movement 11 | Proposal |
| Field-Mage remains a rare practitioner, not a trainer or ruler; Riverwardens do not resume control; sign of trust is non-mechanical | Main Arc movement 12 | Proposal |
| Stillwater Fen: river slows and spreads into shallow channels; wreckage of old battles | Dossier §IV.5 | [CANON] |
| Surge in Wraith activity draws locals into trances; purge vs guided remembrance | Dossier, "Stillwater's Vigil" arc note | [CANON] hook |
| Wraith Lords; Stillwater Serpents; the Hollowed Current | Dossier enemy list | [CANON] |
| Wraithwatchers' lanterns, blessed rope, banner-thistle smoke; no spellcasting | Dossier §III | [CANON] |
| Banner-thistle (wartime signal plant); softmoss | Dossier materials | [CANON] |
| Aldric: administers, does not command; keeps ledgers; "quietly ashamed" | Anchors §I | [CANON] |
| Corvin: duplicate tallies; burned one ledger and regrets it | Anchors §II | [CANON] |
| Maelin: refuses night passage through specific stretches | Anchors §II | [CANON] |
| Lessa: certain paths permanently closed; speaks to the land as if it listens | Anchors §II | [CANON] |
| Annelise: "light enough to carry"; dislikes unattended candles | Anchors §III | [CANON] |
| Tovin: never names, never seeks, never solves | Anchors §IV | [CANON] |
| Four aspirational commissions; acquisition step 1 civic legitimacy | `Caelmor_Aspirational_Equipment_Foundation.md` | Approved economy design |

---

# MQ10 — The Crest Hall Reckoning (`CR`)

## 10.1 The quest in one paragraph

Aldric Fenmere has called the Vale to Crest Hall in the morning to agree a plan for the Braids, which is what Oriel asked for. The night before, Gideon Sallow's crew pours lamp oil down the Tally Stair, sets the keepers' record room alight and cuts the evidence barge loose at the hall's water-gate. The player wakes to the bell, cuts the fire-lines, carries the keepers' records out through the smoke, drags a scorched Keeper-Captain Hesketh into the yard with the Board's minute book under his arm, runs the basin stage to make the drifting barge fast, and fights Sallow on the gate landing in the dark while he cuts the lantern ropes. Sallow yields. In the morning the hearing takes ten minutes and happens with the player's hands: every proof they earned since Whisperflow is carried to the long table and set down in front of Provisioner Edda Marrick, who answers each one kindly and reasonably until there are too many to answer. The hall decides what happens to Hesketh, and the player names who will close the routes and who will tend the fen's memorial ground. The plan passes with roles and no rulers. The player walks out with the plank crews to seal the Cut mouth, and at dusk Ansel comes up the towpath: Stillwater has gone quiet, and not the good kind.

**What the player should remember:** carrying an armful of smouldering ledgers up a stair they had to cut open, and setting a pre-notched post on a table in front of the woman who paid for it. **What the player should want next:** to be at the fen when it lets go.

## 10.2 Summary card

| Field | Value |
|---|---|
| Working title | **The Crest Hall Reckoning** |
| Suggested content id | `lowmark.main.10_crest_hall_reckoning` |
| Arc position | Act III, movement 10. |
| Prerequisite | MQ9 *Behind the Falls* completed. Offered on next entry to Crestbridge (Aldric's summons), or by Hollis at any keepers' post. |
| Solo / co-op | Solo-clearable. Co-op partners run their own instances; the siege crew and Sallow are shared world creatures for partners on the same step. |
| Target length | 40–45 min (siege ~22, hearing ~10, plan ~6, rest optional). |
| Combat share | ~35%, all in the siege. The hearing and plan have none. |
| Skills | Melee (required); Woodcutting (required as one of two fire-line methods; the other is carrying); Cooking (optional, keepers' dawn fire). |
| Choices | Which chips to lay (some carry a cost); Sallow's surrender terms; Hesketh (3 options → 2 values); route keeper (3); memorial keeper (3). |
| Unlocks | `LM_MARRICK_EXPOSED`, `LM_HESKETH`, `LM_PLAN_*`; the Relief Cut is sealed by the crews before MQ11; MQ11 lead-in. |

## 10.3 The place: Crest Hall by night [NEW interior; Crestbridge P02 is the bible POI]

Crest Hall stands on the Crestbridge bank beside the granaries, its undercroft cut down to river level where a wartime **water-gate** lets barges unload straight beneath the hall. **MAP VERIFICATION REQUIRED:** the water-gate must open onto the river above the point where the Relief Cut rejoins (bible §4.1), so that Sallow's crew could reach it by skiff.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. The Waiting Wall and hall steps** | Arrival; evening scene. | The wall is worn smooth at child height (bible P02). Tonight households from three settlements sit along it with bundles; a keeper hands out bread. A chalked line on the steps reads PLAN — MORNING BELL in Hollis's careful hand. |
| **B. The Long Hall** | The hearing. | One long table, scrubbed pale. The steward's chair is the same height as every other chair, and someone has clearly measured. The Provision Board's bench is cushioned. Iron floor-grates along one wall let you hear the water-gate below. |
| **C. The Tally Stair** | Siege route 1. | A broad wooden stair down to the undercroft with plank hoardings either side, cut with generations of tally notches. Tonight a trail of oil-soaked tow runs down both hoardings. |
| **D. The Records Undercroft** | Siege route 2; records rescue. | Shelves of keepers' crossing records, a Board press with a brass seal, and one wall of wartime brick infill still stencilled RELIEF — FENMERE — LOT. Crew have stacked records into piles against the shelf ends to burn faster. A bucket chain hook hangs empty. |
| **E. The Granary Passage** | Link to granaries; water. | A low passage to Corvin's granary undercroft. A stone cistern fed from the river; wet grain sacks hang on pegs for exactly this reason (old fire practice). |
| **F. The Water-Gate Hall** | Siege route 3. | A vaulted stone basin open to the river through a raised iron gate on chains. The evidence barge is moored at the landing stage: the post stock seized at the Hollow Lock, lashed under a keepers' tarp. Three scuttling lines run from the barge's plugs to the gate rail. |
| **G. The Gate Landing** | Miniboss arena. | A stone landing about 14 × 8 m along the basin, two bollards, three lanterns slung on ropes from the vault, a set of steps up out of the water at each end. The gate chain, thick as a wrist, runs down the far wall. |
| **H. The Keepers' Yard** | Respawn; muster; dawn. | Cobbled yard behind the hall. Rescued records end up here on a cart bed; at dawn a fire, a kettle and a lot of keepers with soot on them. |

## 10.4 Player-facing sequence

### Beat 0 — The Evening Before (`S00_convene`, `S01_evening`)
**Objective:** *Go to Crest Hall.* → *Find somewhere to sleep before the morning bell.*
Aldric meets the player on the hall steps (`CR-D1`). He has called the plan for morning because Oriel's condition was public tending, and "public means everyone hears it at once." Optional evening conversations, each short: **Corvin** at the granary door (he has brought his duplicate tallies and will not let go of them); **Hesketh** in the yard, drilling tired keepers and not sleeping; and **Edda Marrick** `[ANTAGONIST]` on the Waiting Wall, sharing bread with the households, who greets the player as though they were old friends (`CR-D2`). She knows what is coming tonight. Nothing she says proves it.
The player is given a bunk in the keepers' loft. Interacting with it ("Sleep until the bell") advances time to night.
**Verbs:** explore, listen.

### Beat 1 — The Bell (`S02_alarm`)
**Objective:** *Find the fire.*
The player wakes to the hall bell rung wrong (fast, uneven, a keeper who has never rung it in earnest). Smoke from the floor-grates. Hollis is at the top of the Tally Stair with a lantern: the stair hoardings are burning in two lines and he cannot get down (`CR-D3`, three lines). Keepers bark from every direction. Entering the stair volume completes the step.

### Beat 2 — Fire-Lines (`S03_firelines`)
**Objective:** *Cut the fire-lines on the stair and in the undercroft (0/3).*
Sallow's crew laid oil-soaked tow in lines; lit, each line is a wall of low fire across a passage. Every fire-line can be cut either of two ways, and the player chooses per line:

| Method | Interaction | Notes |
|---|---|---|
| **Cut it out** | Woodcutting interaction on the burning hoarding section (3 s channel). The section drops into the stone gutter and the line breaks. | Fast. Requires a cutting tool (the crew hatchet from MQ1 counts). Woodcutting XP from the action. |
| **Smother it** | Lift a soaked sack from the Granary Passage cistern pegs (carry), set it down on the oil trail (deposit). | Slower; needs no tool. The same carry state as MQ1's sacks. |

Fire-line 1 is on the stair. Fire-line 2 crosses the undercroft aisle; two crew cutters guard it (E1). Fire-line 3 seals the record room door. Heat zones beside burning shelves glow orange a full second before they tick damage; stepping out of the glow avoids it. Smoke reduces visibility but never damages.
**Verbs:** fight, cut, carry.

### Beat 3 — Carry It Out (`S04_records`)
**Objective:** *Carry the records out to the yard (0/2).* → *Get the Keeper-Captain out.*
Inside the record room two crew torch-bearers are lighting the piled records (E2). When they are engaged, they stop lighting. Two **record bundles** (carry state) wait on the shelves:

- **Bundle 1, the keepers' crossing record:** Hollis's Whisperflow report and the weathered post (if `LM_TL_EVIDENCE = keepers`); the keepers' Act I closure log.
- **Bundle 2, the Lock seizures box:** the keepers' Lock inspection report (if `LM_LOCK_STATE = chained`); Tovin's floor sheets (`tovin_floor_sheets`, both `LM_TOVIN_CREDITED` values: Act II left them in the record room). If `UL_LEDGER`, the keepers' locked iron box from Brookhollow (the crew ledger) sits beside it; iron does not singe.

**Custody rule.** The player has carried `SM_requisition` and `NF_bill_of_lading` since MQ2 and MQ4 (Act I item budget). They are never in the record room and the fire never threatens them. The player lays them on the table in the morning (C3, C4).

Each bundle **smoulders** from the moment the player enters the record room. A bundle not carried out within about 90 seconds of entry is pulled out by keepers, singed: it stays a valid chip but loses 1 weight (minimum 1). Nothing can burn completely. The player can sprint while carrying, the route up the stair is the one they cut open, and a keeper at the top takes the bundle if the player hands it off there.

Behind the Board press the player finds **Bram Hesketh**, hands burned, trying to drag the press cabinet away from the fire. He is not destroying anything. He is saving the book with his own signature in it (`CR-D4`). He gives the player **the Board's minute book** (`CR_board_minute`) and follows the player out (escort; he walks at sprint pace and never needs defending; crew ignore him). In the yard, Elspeth's absence is noted by a keeper ("Flow-Mender's in Ashenstead"); a keeper wraps his hands in wet sacking. **Named only:** if `LM_TOVIN_CREDITED = named`, Hollis takes Tovin's sheets off the cart and hands them to Tovin at the yard door, so that he can lay them himself in the morning.
**Verbs:** carry, fight, rescue.

### Beat 4 — The Water-Gate (`S05_water_gate`)
**Objective:** *Make the barge fast.* → *Drop the water-gate.*
A keeper runs up from below: the crew are at the barge. The player goes down through the Granary Passage into the Water-Gate Hall. The crew have pulled the barge's plugs' lines and cut it loose; three pole-men and two cutters (E3) are **poling it along the basin toward the open gate**. This is a chase on the stage, not a channel:
1. **Throw two mooring lines.** The barge drifts past two bollards on the stage. At each, a coiled line lies ready; the player runs to the bollard and **throws** (instant interaction) onto the barge's cleat as it comes level. The barge is a moving target that waits for the player: while the player is within 6 m of the next bollard, the pole-men struggle with the current and the barge slows to a crawl beside it. Crew on the stage try to shove the player off the line (pole-men's trip, E3).
2. **Drop the water-gate.** Once both lines hold, the barge is fast against the stage and keepers re-seat its plugs. The gate's chain winch is released with a **single lever pull**; the iron gate drops with a crash.

When the gate drops, the basin surges and one young pole-man is swept off the stage and pinned against the gate bars by the current, clinging to the chain. **Optional (`S05b_haul`):** the player can haul him out (3 s channel at the basin edge) before the step ends. If they don't, keepers fish him out afterwards. Nobody drowns in Crest Hall tonight.
**Verbs:** chase, throw, fight, optional rescue.

### Beat 5 — Sallow (`S06_sallow`) `[ANTAGONIST]`
**Objective:** *Stop Gideon Sallow.*
Sallow comes up the far steps from his skiff, cheerful and soaked, and touches the gate chain before he says a word (`CR-D5`). He wants the barge gone and then he wants to be gone. The miniboss fight on the Gate Landing is specified in §10.6. At 20% health he yields: he drops the boat-hook into the basin and holds the gate chain with both hands. He is not killed. Enemies in Caelmor never flee; Sallow surrenders, which is a scripted end to the encounter, not a retreat. **[PROPOSAL — DIRECTOR]** (yield at a health threshold; runtime need in §10.13). His crew in E1–E3 are **downed** at 0 HP: they yield and stay down, presented as beaten, never killed (shared rule with the side-quest packages).
The yield conversation (`CR-D6`) offers the player his account. There are two ways in, and both are always available:
- **If `CR_HAULED_CREWMAN`:** "You pulled the lad out." He gives the **full account**: the Lock, the posts, the buyer's name as written on the bill, and that "the lady said there should be nothing to read in the morning." (Chip C9, weight 2.)
- **Otherwise, or as well:** the player tells him what the flushes did to the fen. He fears the fen more than the keepers. He gives the **Lock account** only: how the flushes were run, which posts were moved. He will not speak about tonight. (Chip C9, weight 1.)
Either way he asks one thing in return: that his crew work the Cut seal instead of rotting in the lock-up. The player can give their word or refuse. The account counts as a chip **only if the player gives their word** (`CR_CREW_LENIENCY`), because without it he will not repeat it in front of the hall. Refusing is legitimate; it costs a chip, not progress.
**Verbs:** fight, judge.

### Beat 6 — Dawn in the Yard (`S07_dawn`)
**Objective:** *Go into the hall.*
The yard at first light: soot, a kettle, a cart bed of rescued records, keepers asleep sitting up. Hesketh with bandaged hands. Aldric arrives, looks at everything, says very little (`CR-D7`). Optional: cook at the keepers' fire and hand food round (`S07b_feed`; unlocks a keeper bark at the hearing and a warmer Hesketh line). There is no wait: when the player walks into the Long Hall, the morning bell rings and the hearing begins.

### Beat 7 — The Long Table (`S08_table`) `[ANTAGONIST]`
**Objective:** *Lay what you found on the table.*
The hall is full. Board members on their bench. Households in the gallery. Aldric at the table, not at its head. Marrick at the Board's end, gloves folded beside her.

The hearing is short and physical. Every chip is an object. Its **holder** stands along the hall wall with it (Corvin with his tallies, Maelin with the old post, the record cart by the door, Hollis with the barge post and, if `UL_LEDGER`, the keepers' locked box, Tovin with his sheets if named, Rhosyn between two keepers only if `UL_RHOSYN_WITNESS`, Sallow in keepers' custody by the floor-grate). The player's own items (`SM_requisition`, `NF_bill_of_lading`, and the post if `LM_TL_EVIDENCE = player`) are laid straight from inventory. A holder's hand-over and the reading play as **one line combined**; Marrick's answer follows. The player takes each chip from its holder (carry state; a one-line exchange with the holder) and **sets it on the table** (deposit volume on the table's cloth). When it lands, the holder or Hesketh says what it is in one line, and Marrick answers it, warmly and reasonably, in one or two lines (`CR-D8`). Then the player chooses the next chip.

After the **third valid chip**, Aldric stands: "That's enough to answer." The player may stop there or keep laying chips for better terms (§10.5). Rejected objects (§10.5.3) can be laid; the table refuses them in one line, they don't count and there is no penalty. When the player says "That's all of it," or lays the last chip they have, Aldric reads the finding and Marrick gives her last answer.

The **strange moment** does **not** happen during the reading of any record. It belongs to the plan's agreement (Beat 9, §10.7).
**Verbs:** carry, present, judge.

### Beat 8 — The Keeper-Captain (`S09_hesketh`)
**Objective:** *Decide whether to speak for Hesketh.*
Hesketh stands and says he signed every blanket order in the minute book without asking where the grain went, because he was told the far bank would riot (`CR-D9`). Aldric asks the hall. The hall looks at the player, who carried him out.
- **Speak for him:** → `LM_HESKETH = kept`.
- **Say nothing; let the hall decide:** Aldric stands him down → `stood-down`.
- **Let him speak for himself:** Hesketh stands himself down → `stood-down`, `CR_HESKETH_SELF`.

### Beat 9 — The Braid Plan (`S10_plan`)
**Objective:** *Name who keeps the routes and the memorial ground.*
Aldric does not propose the plan. He says Fenmere convenes and does not keep, and asks the player to speak first, since Oriel's condition was given to them (`CR-D10`). Sedge is not in the hall: he would not stand in front of the whole Vale (he speaks to the player alone at dusk, Beat 10). The plan has fixed roles and two the player names:

| Role | Who | Chosen? |
|---|---|---|
| Open and close the Braid gates | Maelin's crews | Fixed |
| Close and reopen routes and crossings during a pulse | **crews** / **keepers** / **shared** ("crews call it, keepers post it") | **Player → `LM_PLAN_ROUTES`** |
| Tend the fen's memorial ground | **Watchers** (Ansel's patrol) / **gardens** (Annelise and the watergarden keepers) / **Reedmere** (Lessa and the fen-cutters) | **Player → `LM_PLAN_MEMORIAL`** |
| Patrol heavy water, log it, carry smoke | Wraithwatchers | Fixed |
| Turn field and orchard Braid ditches | Farm workers, Bryn Ruddock named (wording by `LM_BRYN_ROLL`) | Fixed |
| Keep a trance-care station at every vigil | Flow-Menders, Elspeth Quill named | Fixed |
| Seal the Relief Cut today, at both ends, **and plank the Cut-side culverts** the backwater has been using | Crews and keepers together; Lock crew if `CR_CREW_LENIENCY` | Fixed |
| Grain for the vigil and the far bank | House Marrick's stores (`CR_MARRICK_STORES`) | Set by terms |

**No new government:** the roll is not a council and has no chair. Each role-holder says "Aye" aloud in the hall (barks), and the roll is written three times, in the keepers' record, the crews' book and the Watchers' patrol book, so that no one office holds the only copy. Crews will cut the tenders' marks into each Braid stone they tend (pays off in MQ12). Oriel's condition is met in the only form Lowmark has: everyone heard it at once. When Aldric asks *"Is it agreed?"* and the hall answers *"Aye"*, the **strange moment** plays (§10.7). Marrick, already at the door, has one parting bark.

### Beat 10 — Dusk (`S11_dusk`)
**Objective:** *Go with the plank crews to the Cut mouth.* → *Speak with Ansel.*
The crews and keepers leave with stop-planks. The fen end and the culverts along the straight are planked by early afternoon; the river-end crews carry the last planks to the Cut mouth. The player **walks with them** down the towpath (walk-with; no wait interaction). **Dusk falls during the walk.** At the mouth the player may carry and drop the last plank into its groove (optional; carry state). **The planks close the Cut-side culverts the backwater has been using; for the first time since MQ4 the fen has no way out at all.**
Ansel comes up the towpath with his lantern unlit (`CR-D11`): since the fen-end planks went in, Stillwater has gone still. No birds. Fog lying flat. "Like it's holding its breath. I've never been scared of quiet before." **Sedge** is sitting on the mouth's silt sill, beside Ansel, out of sight of any hall. He speaks to the player only (`CR-D11.10–.12`) `[D-7]`. The quest completes; MQ11 is offered.
**MAP VERIFICATION REQUIRED:** the Cut mouth is a short towpath walk from Crest Hall's bank.

## 10.5 Evidence chips

### 10.5.1 Rules

- **A chip is a physical object or a present witness** earned in play. Combat never produces a chip; nothing a crewman or Sallow drops is evidence (the account is testimony given after surrender, in words).
- **Exposure:** any **three valid chips** expose Marrick (`LM_MARRICK_EXPOSED = true`).
- **Terms:** the total **weight** of laid chips sets `CR_TERMS`: **bare** (under 8), **firm** (8–11), **full** (12 or more). Some chips also add a specific **clause** to the plan whatever the tier.
- **Singeing:** chips in record bundles lose 1 weight if the bundle was singed (minimum 1). Singeing never invalidates a chip.
- **Costs:** two chips cost something to lay (C6 named, C9). C8's cost was paid inside *Under the Lamb*. The player can always leave a costed chip on the wall.

### 10.5.2 Chip table

| # | Chip (what goes on the table) | Source quest / flag | Holder at the hearing | Weight | What it shows | Clause it adds | Cost of laying | Marrick's answer (`CR-D8`) → what beats it |
|---|---|---|---|---|---|---|---|---|
| **C1** | **The Whisperflow proof:** the weathered post (and dispatch order, if obtained). | MQ1 · `LM_TL_EVIDENCE` | keepers → record cart (bundle 1, singeable); riverfolk → Maelin, with a second pre-notched post her crews pulled from another bend; player → the player's own inventory | 1 (riverfolk: 2) | A crossing post was swapped to read open on a flush night; the order presumed it. | All crossing posts re-seated on their stones by crews within the season. | — | "Anyone can move a post on a dark bank." → beaten by C5. |
| **C2** | **Corvin's duplicate tallies:** 120 sacks drawn, 40 carried by road. | MQ2 complete | Corvin Tath | 2 | The draw and the delivery don't match. | Every sack the far bank never got is owed, by count. | — | "Grain is lost every season, to damp, to rats, to goblins under the depot." → beaten by C3 or C4. |
| **C3** | **The depot slip** (`SM_requisition`). | MQ2 complete | the player (quest item since MQ2; never in the fire) | 1 | A night draw under Board seal, lowered by rope, not carried by goblins. | — | — | "The Board's seal goes on a hundred slips a season. I can't account for every clerk." → beaten by C7. |
| **C4** | **The Hollow Lock bill of lading** (`NF_bill_of_lading`). | MQ4 complete | the player (quest item since MQ4; never in the fire) | 2 | Board-sealed grain sold to an outside buyer at priority rates. | The buyer's priority contracts are voided in the keepers' record. | — | "A buyer downriver paid what we could not refuse. The far bank ate because of it." → beaten by C2 (the far bank got 40 of 120). |
| **C5** | **The Hollow Lock posts:** one pre-notched yellow post from the barge's stock (Hollis brings it up from the barge); plus the keepers' in-place Lock inspection report if chained. | MQ4 · `LM_LOCK_STATE` | Hollis (post); record cart (report, bundle 2, singeable) | chained: 2 · smashed: 1 | The posts were cut a hand high in advance, at the Lock, by the Lock crew. | Keepers' countersign is required before any marker is replaced. | — | "Smugglers. My factor hired badly, I grant you." → beaten by C4 (her seal) or C9. |
| **C6** | **Tovin's flush calendar.** | MQ6 · `LM_FLUSH_CALENDAR`, `LM_TOVIN_CREDITED` | named → Tovin, in person (Hollis hands him the sheets at the yard door after the fire); unsigned → record cart (bundle 2) | named: 2 · unsigned: 1 (singeable either way: the sheets were in bundle 2) | Every flush night falls a day after an emergency draw. | Tovin's sheets are pinned in the keepers' hall (MQ12). | Named: Tovin must stand up in front of the hall and answer one question. He does. | "Pretty drawings. Whose?" → beaten by C7 (dates in her own book line up). |
| **C7** | **The Board's minute book** (`CR_board_minute`). | MQ10 Beat 3 (guaranteed) | the player | 2 | Every emergency was moved by the Provisioner and carried on her motion; Hesketh signed the blanket orders that followed. | Board emergency powers need a crossing keeper's countersign. | Hesketh's name is read aloud with hers. | "I moved them because the households were hungry. Read the minute: I said so every time." → beaten by any two of C2/C4/C6. |
| **C8** | **The crew ledger** from under the Lamb, Rhosyn's pages included: crew pay drawn on "the Provisioner's purse", the Board seal stamped on the pay chits. | `UL_LEDGER` (side quest UL); weaker if `UL_LEDGER_CUT`; testimony if `UL_RHOSYN_WITNESS` | Hollis, with the keepers' locked iron box (UL-D6.04); Rhosyn between two keepers only if `UL_RHOSYN_WITNESS` | 2 · `UL_LEDGER_CUT`: 1 · +1 if `UL_RHOSYN_WITNESS` attests the hand | Who paid the crew: the Provisioner's purse, under Board seal. | Full ledger only: the licensed haulers whose passes the crew used answer to the keepers before they haul again (`UL_LEDGER_CUT` cannot name them). | None at the table (UL already settled Rhosyn's fate). `UL_RHOSYN_WITNESS` + laid sets `CR_RHOSYN_LAID`. | "A cellar book. Anyone can write 'the Provisioner' in a cellar." → full: beaten by the seal stamped on the chits; cut: beaten by C4 (the same seal on the bill). |
| **C9** | **Sallow's account.** | MQ10 Beat 5 (optional; always reachable) | Sallow, in keepers' custody | full: 2 · Lock only: 1 | Full: the Lock, the posts, the buyer, and that she wanted "nothing to read in the morning." Lock only: how the flushes were run. | Lock crew work the seal under keeper watch. | Requires the player's word (`CR_CREW_LENIENCY`). Maelin's crews dislike working beside the Lock crew (MQ11 bark). | "My factor will say anything to stay dry." → beaten by C5 + C4 together. |

### 10.5.3 Not chips (the table refuses them)

Players may try to lay these. Each draws one line (`CR-D8.R*`), counts for nothing and costs nothing. This is the evidence rule taught one last time.

| Object | Refusal (speaker) |
|---|---|
| Ansel's patrol book, drift entries | ALDRIC: "It tells us when the water went wrong. It doesn't tell us who." |
| Joss Garrow's lantern (`OL_LANTERN_ONLY`; lifted from the Lantern Post hook) | ANSEL: "That's a man's lantern, not a witness. Put it down gently." |
| Any account of the stone holding a line, the flow-table, or drift | MARRICK: "The river has opinions now?" |

### 10.5.4 Guaranteed path

From main quests alone the player always has **C1, C2, C3, C4, C5, C6 and C7**: seven valid chips. C3 and C4 are always in the player's hands and can never singe. The minimum main-only weight with every bundle singed is 10 (**firm**). The maximum main-only weight is 13 (**full**), with riverfolk, chained, named and no singeing. C7 is earned inside MQ10 and cannot be missed, because Beat 3 cannot complete without Hesketh. **Fallback:** if `LM_FLUSH_CALENDAR` were somehow false, C6 is absent and six chips remain. No combination of earlier flags leaves fewer than three.

### 10.5.5 Terms

| `CR_TERMS` | Marrick's outcome | `CR_MARRICK_STORES` |
|---|---|---|
| **bare** (<8) | Marrick resigns her Board seat "for the households' peace." House Marrick keeps its standing claim, unopposed but unpressed. | **offered**: she volunteers her stores to feed the vigil, as a gift. |
| **firm** (8–11) | Marrick is put off the Board; House Marrick's stewardship claim is withdrawn from the next hearing. Her granary doors are put under keepers' seal. | **offered**: she still volunteers them first, before anyone can order it. |
| **full** (12+) | As firm, and restitution from House Marrick's own stores is **ordered**: the far-bank debt and the vigil's food. The claim is struck, not withdrawn. | **ordered**. |

`LM_GRAIN_ROUTE` adds one clause in every tier: **escort** → a far-bank householder in the gallery says they were fed by road, which is the line that breaks Marrick's riot defence (`CR-D8.40`); **hold** → Marrick's riot defence lands ("You held it, and they went hungry, as I said they would"), and the plan's first line becomes the far-bank grain; **split** → both lines are spoken, briefly.

## 10.6 Encounters

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target (Milestone 3) |
|---|---|---|---|---|---|---|
| **E1** | 2 × Smuggler cutter | Undercroft aisle, fire-line 2 | Aggressive; leashed to the aisle | Cutter: knife hand drawn back (~0.9 s) before a double cut | Fight in heat-zone terrain | Required. ~40 s. Ends at 75–90% HP. |
| **E2** | 2 × Smuggler cutter (torch-bearers) | Record room | Aggressive once engaged; otherwise light piles (each lit pile adds a heat zone, not lost records) | As E1; torch swing (~1.2 s) leaves a short-lived fire patch | Urgency without fail | Required. ~40 s. |
| **E3** | 3 × Smuggler pole-man, 2 × cutter | Water-Gate Hall, barge and stage | Aggressive; pole-men prefer to work the barge until engaged | Pole-man: pole set low (~1.2 s) before a sweeping trip that knocks the player down 1 s | The barge race; mixed reach | Required. ~70 s. Ends at 55–75% HP. |
| **E4** | **Gideon Sallow** (miniboss) + 2 × pole-man at 66% | Gate Landing | Miniboss; yields at 20% | See below | Act III's human set piece | Required. 2.5–4 min. Ends at 40–70% HP. |

### 10.6.1 Miniboss spec: Gideon Sallow `[ANTAGONIST]`

| Element | Spec |
|---|---|
| Arena | Gate Landing (G): 14 × 8 m stone stage along the basin edge; water on the long side; steps up from the water at each end; two bollards (cover from the Shove: he stops against them); three lanterns on ropes from the vault, one over each third of the stage. |
| Weapon | Boat-hook: long reach (3 m), slow. |
| **Hook Sweep** | Telegraph: hook drawn back across his body, shoulders turn, a creak of wet leather (~1.2 s). Effect: 160° arc at 3 m in front. Counter: step out of reach or behind him. Most frequent attack. |
| **Rope Cut** | Telegraph: he looks up and flicks the hook at a lantern rope; the lantern visibly sways first (~1.5 s). Effect: the lantern drops and goes out; that third of the stage goes dim. In the dim his sweeps still telegraph by sound (he whistles before every swing; he can't help it) and the stage edge is harder to read. Counter: the fallen lantern sputters on the stone; **Relight** (2 s interaction) restores the light. Phase 2+ only; never more than two lanterns down at once. |
| **The Shove** | Telegraph: he plants the hook's butt, lowers his shoulder and scrapes a boot (~1.8 s); a wet streak marks his line on the stone. Effect: 5 m straight charge; on hit, the player is knocked back 3 m. If that carries them over the edge, they fall into the basin: no damage, but they wade to the nearest steps (6–8 s out of the fight). Sallow does not heal while they wade; he talks (barks). Counter: step off the streak, or stand with a bollard behind you. |
| **Chain Touch** | At 66% and 33% he backs to the gate chain and touches it with an open hand (2 s; one superstitious line). Not an attack. A free opening for the player, and characterisation. |
| Phases | **P1 (100–66%):** Sweep, Shove. **P2 (66–33%):** adds Rope Cut; 2 pole-men come up the far steps (E3 stats, one at a time). **P3 (33–20%):** Sweep and Shove cadence +25%; one Rope Cut on entry. |
| Yield | At 20% he drops the hook into the basin, grips the chain with both hands and says "Enough. Enough. I'm done." Combat ends; adds kneel. Event `cr.sallow_yield` → `CR-D6`. |
| Death and recovery | Player death respawns at the Keepers' Yard (H) with steps intact; the barge stays secured and the fire-lines stay cut. Sallow resets to full health on the landing. |
| Co-op | Shared world creature for partners on `S06_sallow`; health scales per participant (Gameplay Designer). Shove targets the farthest player. Each participant gets the yield and runs `CR-D6` in their own instance. |
| Evidence rule | Sallow drops nothing evidentiary. His account is given in words, after the fight, by choice. |

## 10.7 The strange moment: the water-gate stills

| Element | Spec |
|---|---|
| Trigger | Server event `cr.plan_agreed` when the hall answers **"Aye"** to Aldric's *"Is it agreed?"* (`CR-D10.33`). It never fires during the reading of any record, chip or finding. |
| Duration | ~6 s. |
| Audio | The water-gate's lap and gurgle, audible through the floor-grates all morning, ducks to silence over 1 s under the overlapping "Aye"s. The hall's own sounds stay. The water returns as a single lap. |
| Visual | The thin ripple-light that plays across the ceiling from the grates stops moving. Nothing else. |
| NPCs | A few gallery households look down at the grates. Hollis looks at the player. Marrick, already at the hall door, has one parting bark as she goes (`CR-D10.40`): *"Even the river came to the meeting. How flattering for all of us."* `[ANTAGONIST]` |
| Meaning | **Nothing is proved by it, and nobody is accused by it.** It is tied to the many hands agreeing (Oriel's condition), not to any person or record. In author truth, the water-gate sits on an old Braid outfall that the afternoon's sealing will change; no one in the hall knows that. |
| UI | None. |

## 10.8 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_convene` | Go to Crest Hall. | `CR-D1` end node | Yes | Auto-offered on MQ9 completion + entry to Crestbridge |
| `S01_evening` | Find somewhere to sleep before the morning bell. | Interaction `sleep_until_bell` at keepers' loft bunk | Yes | Evening talks (Marrick, Corvin, Hesketh) optional before this |
| `S02_alarm` | Find the fire. | Enter Tally Stair volume | Yes | Night state begins on `S01` completion |
| `S03_firelines` | Cut the fire-lines (0/3). | 3 × (interaction `cut_hoarding` complete OR soaked-sack deposit on oil trail) | Yes | E1 at line 2 |
| `S04_records` | Carry the records out (0/2). Get the Keeper-Captain out. | 2 bundle-deposit events (or keeper hand-off) + Hesketh escort enters yard volume + `CR_board_minute` acquired (`CR-D4`) | Yes | Bundle smoulder timers start on record-room entry; singe sets `CR_SINGED_B1/B2` |
| `S05_water_gate` | Make the barge fast. Drop the water-gate. | 2 × `throw_mooring_line` (instant, at the moving barge beside each bollard) + `drop_gate_lever` (single pull) + E3 downed | Yes | Barge slows beside the next bollard while the player is within 6 m |
| `S05b_haul` | (Optional) Haul the crewman out. | Interaction `haul_crewman` complete before `S05` completes | No | Sets `CR_HAULED_CREWMAN` |
| `S06_sallow` | Stop Gideon Sallow. | Event `cr.sallow_yield` + `CR-D6` end node | Yes | |
| `S07_dawn` | Go into the hall. | `CR-D7` end + enter Long Hall volume (the bell rings on entry) | Yes | No wait interaction |
| `S07b_feed` | (Optional) Feed the keepers. | Item-given: cooked food to a keeper | No | `CR_FED_KEEPERS` |
| `S08_table` | Lay what you found on the table. | ≥3 valid chip deposits + `CR-D8.90` (finding) end node | Yes | Sets `LM_MARRICK_EXPOSED`, `CR_TERMS`, `CR_MARRICK_STORES` |
| `S09_hesketh` | Decide whether to speak for Hesketh. | `CR-D9` choice resolved | Yes | Sets `LM_HESKETH` |
| `S10_plan` | Name who keeps the routes and the memorial ground. | `CR-D10` both choices resolved + `CR-D10.33` "Aye" | Yes | Sets `LM_PLAN_ROUTES`, `LM_PLAN_MEMORIAL`; fires `cr.plan_agreed` (§10.7) |
| `S11_dusk` | Go with the plank crews to the Cut mouth. Speak with Ansel. | Walk-with arrives at the Cut-mouth volume (dusk falls during the walk) + `CR-D11` end node | Yes | Optional `drop_last_plank` carry. Quest → Completed; MQ11 offered |

## 10.9 Flags (quest-local)

| Flag | Set by | Read by |
|---|---|---|
| `CR_SINGED_B1`, `CR_SINGED_B2` | Bundle timers | Chip weights; Hollis/Hesketh barks |
| `CR_HAULED_CREWMAN` | `S05b_haul` | `CR-D6` full-account branch; MQ12 Sallow line |
| `CR_SALLOW_ACCOUNT` (none / lock / full) | `CR-D6` | C9 weight |
| `CR_CREW_LENIENCY` | `CR-D6` | C9 validity; plan clause; MQ11 gate-1 crew; MQ12 |
| `CR_TOVIN_STOOD` | C6 laid with named | MQ12 Tovin line |
| `CR_RHOSYN_LAID` | C8 laid with `UL_RHOSYN_WITNESS` (she attested) | UL epilogue |
| `CR_CHIPS_LAID` (count), `CR_WEIGHT` (sum) | `S08` | `CR_TERMS` |
| `CR_TERMS`, `CR_MARRICK_STORES` | `S08` | MQ11, MQ12 |
| `CR_HESKETH_SELF` | `CR-D9` | MQ12 Hesketh line |
| `CR_FED_KEEPERS` | `S07b_feed` | `CR-D7`, hearing bark |

## 10.10 Choices and consequences

| Choice | Options | Immediate | Later |
|---|---|---|---|
| **Sallow's terms** | Give your word (crew work the seal) / Refuse | Word: C9 is valid; the Lock crew go up the Cut with the seal crews. Refuse: C9 unavailable; crew to the lock-up. | MQ11: Lock crew on gate 1 under keeper watch (word). MQ12: Sallow at the Cut mouth with a shovel (word) or behind the lock-up grille (refuse). |
| **Which chips** | Any subset ≥3 | Terms tier and clauses (§10.5). | C6 named → Tovin stood (MQ12). C8 (full) → licensed haulers answer to the keepers. Rhosyn's MQ12 fate follows the UL outcome, not the table. |
| **Hesketh** | Speak for him / Say nothing / Let him speak for himself | kept: he stays Keeper-Captain, under the new countersign rule. stood-down: Aldric stands him down, and he asks to be put on the Cut seal crew. Self: he stands himself down before anyone can. | MQ12 Crestbridge scene. The Crestbridge Guard commission is given by Hesketh (kept) or by the Keeper-Lieutenant with Hesketh's word behind it (stood-down). |
| **Route keeper** | Crews / Keepers / Shared | Who calls crossings during a pulse. | MQ11: who marshals the evacuation lanes. MQ12: who lights the Whisperflow posts with the player (crews: Maelin's hands; keepers: Hollis; shared: both). |
| **Memorial keeper** | Watchers / Gardens / Reedmere | Who tends the fen's memorial ground. | MQ11: who stands the Widow's Step station through the vigil. Ending: who keeps the Tend channel or the Seal boundary's remembrance post. |

## 10.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| The plan | Story / world | Roles active across the Vale (barks, props, MQ11 positions). |
| Keepers' waiting-wage | Currency | Small; from Hesketh (kept) or the Keeper-Lieutenant. Amount set in economy tuning. |
| Skill XP | Action XP only | Melee, Woodcutting, optional Cooking. No lump quest XP. |
| Crestbridge's thanks | Standing (narrative) | Keepers' barks change across Crestbridge. No reputation system. |

## 10.12 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death in the siege | Respawn in the Keepers' Yard; steps, flags and carried-out bundles kept; any bundle being carried returns to the room (its smoulder timer pauses while the player is dead). |
| Logout mid-siege | Restore last persisted step. If logged out during `S04`, bundles not yet deposited are deposited by keepers, unsinged (we never punish a logout with a singe). |
| Slow siege | Bundles singe (−1 weight, never invalid). No other timer exists. |
| Player has no cutting tool | Smother method on every fire-line. |
| Player refuses Sallow's terms | Six or more valid chips remain. |
| Player never did *Under the Lamb* | No C8 and no Rhosyn; nothing else changes. |
| Player lays only rejected objects | The table refuses them; the holders keep offering the real chips. |
| Fail state | None. |
| Co-op | Each partner's chips are their own (a partner cannot lay your C8). Siege creatures are shared on matching steps. The hearing runs per player; partners present see their own table state (per-player props). **Fallback** if per-player table props are not ready: chips are laid by dialogue with the holder ("Lay it on the table") and only the speaking holder's prop appears. |

## 10.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Night state for Crest Hall interior (lighting, fire volumes) | Systems + art | Step-keyed lighting profile; fire-line volumes as damaging blockers that clear on interaction. |
| Smoulder timer on carry objects | Systems | Per-object timer started by enter-volume; on expiry sets a flag and teleports the object to the yard. |
| Carry state (bundles, sacks, chips, barge post) | Systems | Same as MQ1. |
| Table deposit volume with per-chip validity and weight | Schema & Content | A list of chip ids with conditions, weight and singe flag; deposit event increments `CR_CHIPS_LAID`/`CR_WEIGHT`. |
| Miniboss yield at health threshold **[PROPOSAL — DIRECTOR]** | Systems + Gameplay | Health-threshold event (20%) that ends combat and switches the creature to a non-hostile NPC. **Runtime need:** the same mechanism serves Joss Garrow's yield in *Old Lantern*; flagged as new for the runtime. Human crew use the shared "downed at 0 HP" presentation (yield and stay down). |
| Moving barge with bollard wait points | Systems | Pathed prop (as MQ4's barge) that slows beside the next bollard while the player is near; two instant line-throw interactions. |
| Lantern-rope prop (drop + relight) | Systems + art | Breakable light with a relight interaction. Reused for MQ11 lantern racks. |
| Audio duck on `cr.plan_agreed` | Audio | Local duck of the water-gate emitter and ceiling ripple-light pause. |

## 10.14 Mystery ledger entries

| Mystery | Author truth | Public belief after MQ10 | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| Who ordered the fire | Marrick, by implication, to Sallow. | "Her factor's crew did it." | Only C9 full ("nothing to read in the morning"). | Marrick lit it herself; Hesketh tried to burn his orders. | Whether she meant fire. She never says. | MQ10 (testimony only). |
| Who the buyer was | A name on a bill; outside Lowmark. | "Someone downriver." | C4. | Emberholt; a rival Lowmark house. | Everything beyond the name. **No v1 content names a region.** | Future region (not v1). |
| Why the water-gate stilled | The gate sits on an old Braid outfall. | "The river came to the meeting." | The silence at the "Aye"; Marrick's parting joke. | The river approved the plan. | All of it. | Never. |

## 10.15 Open decisions

1. **Miniboss yield** is the only v1 creature that surrenders. *Recommendation: keep; it is the clearest way to show the antagonists are people.*
2. **Who succeeds Hesketh if stood down.** This package uses a role-based **Keeper-Lieutenant**. Hollis is the emotional choice, but he is junior and born after the armistice. *Recommendation: role-based; revisit if Hollis gets a Keeper-Captain arc later.*
3. **The outside buyer's name** on `NF_bill_of_lading` is a placeholder until the cross-region pass.

## 10.16 Internal review log

| Finding | Revision |
|---|---|
| First draft had the fire destroy any unrescued records. That allowed a soft-lock on chips. | Records singe (−1 weight) and are always pulled out. |
| Main-only chips made exposure trivial, so the hearing had no decisions. | Kept the guaranteed path (required) but added chip costs (C6, C8, C9) and a terms tier, so what the player lays is a choice. |
| Marrick's answers read as denials. | Rewrote every answer as a reasonable, partly true explanation, each beaten by a *different* chip, so the order the player lays them matters to the conversation. |
| Hesketh was a passive victim. | He is found saving his own signed orders from the fire. |
| Sallow's account was gated on an optional rescue only. | Two ways in; both always available; only the weight differs. |
| The water-gate silence risked reading as proof. | Independent review pass: it no longer coincides with any record. It fires when the hall says "Aye" to the plan, tied to many hands and no person; Marrick mocks it on her way out; the finding cites only chips. |
| Independent review pass: item custody. | `SM_requisition` and `NF_bill_of_lading` are always player-held and laid from inventory; bundles hold only keepers' records and Tovin's sheets (both values). Minimum main-only weight 10. |
| Independent review pass: C8. | C8 is now the UL crew ledger (`UL_LEDGER`, weaker if `UL_LEDGER_CUT`), with Rhosyn present only if `UL_RHOSYN_WITNESS`. |
| Independent review pass: fourth channel hold in a row. | The water-gate is a chase on the stage (two thrown lines at a moving barge, one lever). |
| Independent review pass: waits and public Sedge. | The hearing starts on entering the hall; dusk falls on the walk to the Cut mouth. Sedge speaks to the player alone at the Cut mouth, not to the hall. |
| Independent review pass: backwater. | The plan planks the Cut-side culverts too, so MQ11's fen has no way out at all. |
| The plan risked becoming a new council. | No chair, no seat; three copies; tenders' marks on stones. |

---

# MQ11 — Stillwater's Vigil (`SV`)

## 11.1 The quest in one paragraph

With the Relief Cut sealed at both ends, Stillwater Fen has nowhere to send its weight, and for a day it holds still. Then it lets go: the **Hollowed Current**, a whole fen flowing wrong. The player stands the vigil at Reedmere at dusk. First they bring the outlying fen-cutters in along a path Lessa Mirepath swore was done, while people stop mid-step, turn towards deep water and have to be brought back with banner-thistle smoke. Then they hold three Braid gates open in Oriel's order with Maelin's crews, while Reed Stalkers come out of the reeds and a Stillwater Serpent breaks through the second sill. Then, at the heart pool over the sunken Fourteenth Lot, the grief that has gathered there for a generation stands up as **the Muster**: lantern-lines of cold water, oar-knock counts, and a pull towards the deep that can be broken only by stepping onto a stone that reads true. Defeat disperses it. The player seats a post on the heart stone, Sedge puts his hands flat in the water, and **every Marking Stone in the fen holds a line at once**. The fen exhales. At dawn the people who stood the vigil ask the player to say what happens to Stillwater now: Seal it, Tend it, or both.

**What the player should remember:** a hundred lanterns across the fen, each beside a stone with water standing in its notch, all at once. **What the player should want next:** to see what the Vale looks like when it isn't afraid.

## 11.2 Summary card

| Field | Value |
|---|---|
| Working title | **Stillwater's Vigil** |
| Suggested content id | `lowmark.main.11_stillwaters_vigil` |
| Arc position | Act III, movement 11. The Act III boss. |
| Prerequisite | MQ10 completed. Offered by Ansel at `CR-D11`. |
| Solo / co-op | Solo-clearable. The Muster is a shared world creature for partners on the same step. |
| Target length | 45–55 min (evacuation ~15, gates ~15, Muster ~8, hold and choice ~7). |
| Combat share | ~45%. |
| Skills | Melee (required); Cooking (optional, Elspeth's station); marker and stone reading (required knowledge). |
| Choice | Seal / Tend / Shared → `LM_FEN_ENDING`. |
| Unlocks | Drift-site states change Vale-wide (§ Ending matrix); MQ12. |

## 11.3 The places [NEW unless noted; Stillwater Fen is CANON]

**MAP VERIFICATION REQUIRED** for all of the following. The narrative needs only: Reedmere sits on the fen's landward edge; the three Braid gates lie in a rough line from Reedmere towards the fen's centre; the heart pool lies at the centre, over the Fourteenth Lot; Widow's Step overlooks the near edge.

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Reedmere and the lantern store** (P06) | Hub; Elspeth's trance-care station in the store loft; evacuees' arrival. | Stilt houses joined by plank walks; drying racks of reed; the Watchers' lantern store with every hook empty tonight. A tally board by the steps lists the outlying huts in chalk; names get crossed off as people come in. |
| **B. The cutting grounds** | Evacuation sites: three outlying stilt huts, **Hookreed**, **Two Posts** and **the Far Racks**. | Reed bundles abandoned mid-tie. At Two Posts a kettle still steams. At the Far Racks a cutter's boots stand side by side at the water's edge, unlaced. |
| **C. The Cutters' Causeway** | The done path Lessa reopens. | A wartime stone causeway half under the water, marked at its mouth with Lessa's old warning stake: a stake wound in faded cloth. She pulls it up tonight. Convoy-era cart ruts in the stone. |
| **D. Lessa's guide route** | Second evacuation lane (completed side quest FW only). | Dry reed ridges flagged with her own knots; faster, narrower. |
| **E. Gate 1, Reedmere Weir** | First Braid gate. | A low stone weir with a wooden gate-board on a carved rack; a Marking Stone set into the weir face; the crews' chalk "1" on the gate-board. |
| **F. Gate 2, the Long Sill** | Second gate; the Serpent breach. | A long stone sill across a deep channel. The water on the deep side is black and very still. A crushed reed-cutter's punt lies on the sill. |
| **G. Gate 3, the Lantern Sluice** | Third gate; pressure peak; Muster approach. | A narrow carved sluice with a lantern niche in each pier, older than anything in Reedmere. The heart pool's fog lies just beyond it. |
| **H. The heart pool** | Muster arena. | A wide shallow sheet of water over deep holes, ringed by eight Marking Stones on low plinths. The black ribs of sunken grain barges break the surface in a curve, like the shape of a convoy laid at anchor. At the centre, a ninth stone, the **heart stone**, with an empty post-footing in it. |
| **I. Widow's Step** (P22, CANON-adjacent) | Memorial-keeper station; overlook. | The embankment of unmatched scraps (MQ3). Tonight whoever keeps the memorial ground stands here with a lantern. |

## 11.4 Player-facing sequence

### Beat 0 — Reedmere at Dusk (`S00_arrive`)
**Objective:** *Go to Reedmere.*
The fen road is silent. At Reedmere the plan is visible in people: Maelin's crews coiling rope on the plank walks; Watchers filling the lantern store's hooks; Elspeth laying out softmoss and blankets in the loft; whoever `LM_PLAN_ROUTES` named marshalling the lanes (crews in oilskins, keepers in Crestbridge blue, or both arguing politely); and food from House Marrick's stores (`CR_MARRICK_STORES`) being unloaded by keepers. Sedge sits on the steps of the lantern store, mending nothing. **`OL_JOSS_IN`:** Joss Garrow sits wrapped in a blanket by the loft stove in Elspeth's care, among the first evacuees, saying nothing; Ansel checks on him between tasks.

### Beat 1 — The Vigil (`S01_vigil`)
**Objective:** *Stand the vigil.*
The player speaks to Sedge (`SV-D1`): "It's going to let go tonight. Bring people in first. Then the gates. Then the middle." Ansel hands the player a **Watcher smoke-pot** (loaned tool, refilled at lantern racks; if Act I already gave the player a smoke tool, he refills that instead) (`SV-D2`). Interacting with the Reedmere vigil fire ("Stand the vigil") advances to full dark. The fen's sound returns all at once as a low rushing from everywhere: the Hollowed Current has begun. Lessa walks to the mouth of the Cutters' Causeway and pulls up her own stake (`SV-D3`). As she does, she says the one thing she has never explained (`SV-D3.02b`): *"Grain lot went down out there in the war. Barges, crews, all of it. Nobody wrote it. That's why this path's done."* This is Fourteenth Lot delivery 3 of 3, before the boss, and it is testimony from a living guide, never from the water.

### Beat 2 — Bring Them In (`S02_evacuate`)
**Objective:** *Bring the cutters in from the far huts (0/7).*
Seven fen-cutters remain at three huts (Hookreed 2, Two Posts 3, the Far Racks 2). The player walks out by the Causeway (and/or Lessa's route), finds them, and leads them back. Each cutter who is spoken to takes a lantern from the player's string (the player carries a lantern; followers walk to its light) and follows. Up to 4 followers at once.

**The trance mechanic.** Some followers will stop, turn towards deep water and begin to walk into it. This is a grief response to the Current, not possession: they are not hostile, do not speak for anyone, and say afterwards only that they "heard the count."

| Stage | What the player sees | Duration | What the player does |
|---|---|---|---|
| **Warning** | A distant oar-knock counts four (the Muster's stroke-call, heard first here). On "four", the follower nearest deep water stops. | 4 knocks, ~4 s | Nothing yet; this teaches the count. |
| **Turning** | The follower faces the water, lantern lowered. | ~3 s | **Smoke them** (2 s channel with the smoke-pot within 4 m): they cough, blink, and follow again. |
| **Walking** | Slow walk to the water's edge. | ~15 s | Smoke them (as above). |
| **Standing** | Knee-deep at the edge, still. Never deeper. They do not drown. After 15 s, a drift pocket rises nearby. | Until helped | Wade in, smoke them, then **lead them out** (3 s channel); clear the drift. |

Smoke-pot: 3 uses per fill; **lantern racks** along both lanes refill it (Watchers hung them; 6 racks). Trances happen at scripted points along each route (two per trip, never more than one follower at a time), so the mechanic stays readable.
**Hazards on the lanes:** drift pockets (E1) and **lantern-lines** in miniature: a row of drift-lanterns hangs over the Causeway at one point, and the water under them frosts pale a second before a cold surge runs along it. Step aside. This teaches the boss's lane telegraph. At the Far Racks, two **Mud Pipers** call in a cutter's voice from the wrong direction ("Over here — I'm stuck —"); the real cutter is silent by the boots (E1b).
Arrivals: each cutter delivered to the Reedmere tally board is crossed off by a keeper or crew hand. Elspeth treats them in the loft (barks). **Optional (`S02b_feed`):** cook at Elspeth's station for the evacuees from House Marrick's stores.
**If completed side quest FW:** Lessa's guide route is open as a second lane; it is shorter and has no lantern-line, but one extra trance point.

### Beat 3 — The Braid Gates (`S03_gate1`, `S04_gate2`, `S05_gate3`)
**Objective:** *Open the Braid gates in Oriel's order (0/3).*
Oriel's order (MQ9: **furthest from the Cut's head first, nearest last**): **Reedmere Weir** is furthest, **the Long Sill** is next, **the Lantern Sluice** beside the deep pools is nearest. The same three names and the same rule as MQ9 (Act II §BF.7.4). The order is chalked on every gate-board by the crews, so the player who forgets it is never lost. At each gate the player **reads the gate's Marking Stone** (inspect; the True Line skill): *"Water's stuck under the notch. It wants to move."* At Reedmere Weir the stone adds: *"The Cut's old head is that way. This one's furthest."* That confirms the gate is the next one. A gate opens by **holding the channel**: two crew hands work the gate-board winch (progress fills slowly while they are not attacked; the player can add a crank channel to double the rate). Enemies go for the crew; a harassed crew stops cranking. Progress never decays except at gate 2 (below). When a gate opens, a Braid channel visibly runs: water starts moving through reeds that have been still since the war, and a Watcher hangs a lantern at that gate's stone.

| Gate | Pressure | Encounter |
|---|---|---|
| **1. Reedmere Weir** | Low | E2: Reed Stalkers (2 stalkers, 1 lurker) come out of the reeds at the crew. If `CR_CREW_LENIENCY`, two of the crew on this winch are Sallow's Lock men under keeper watch, and they work hard. |
| **2. The Long Sill** | Rising | E3: one wave of drift, then a **Stillwater Serpent** breaches *through* the sill: stone cracks, the gate-board jams, and progress **falls** while the Serpent is at the sill (it is pushing the channel shut with its body). Kill or drive it off the sill (it submerges to the deep side and resurfaces) and progress resumes. |
| **3. The Lantern Sluice** | Peak | E4: drift waves and two lantern-drifts. As progress passes 50%, the heart pool's fog lifts in one movement and the player can see the lights of the Muster standing up beyond the sluice. |

### Beat 4 — The Muster (`S06_muster`)
**Objective:** *Face what stands in the heart pool.*
The player walks through the open sluice into the heart pool. Sedge is already there, standing to his knees at the edge with his hands at his sides (`SV-D6`: "Don't stand where it's stuck. Stand where it moves."). The Muster rises. Full spec §11.6. When it is dispersed, the lanterns it held go out one at a time, from the outermost in, without a sound.

### Beat 5 — The Heart Stone (`S07_heart_stone`) — *the climax*
**Objective:** *Set a post on the heart stone.*
A crew hand (or Maelin herself if `LM_PLAN_ROUTES = crews`) wades in with a marker post on their shoulder: the plan said crews tend the stones, and they brought one for the middle. The heart stone has an empty footing and one crisp notch. Two interactions, exactly as at Whisperflow: **Cut the notch** (3 s, guided by the stone's notch), **Seat the post** (3 s). Sedge puts both hands flat on the water beside the stone. Then the presentation in §11.7 plays. **This is The True Line's discovery, made by the whole fen.**

### Beat 6 — Dawn: What Happens to Stillwater (`S08_choose`)
**Objective:** *Say what happens to Stillwater.*
Grey light at Reedmere. The people who stood the vigil are on the landing. Aldric's plan left Stillwater's ending to those who stood the vigil; they could not agree and they ask the player to say it, since the player was at the heart stone (`SV-D8`). Three voices, one each, then Sedge, who refuses to choose but tells the truth about each. See §11.8.

### Beat 7 — The Morning After (`S09_close`)
**Objective:** *Speak with Maelin.*
Short. Maelin says the crews will keep whatever was chosen. The quest completes; MQ12 begins on the spot.

## 11.5 Encounters

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target (Milestone 3) |
|---|---|---|---|---|---|---|
| **E1** | Drift ×2–3 per pocket (5 pockets); lantern-line hazard ×1 per lane | Evacuation lanes; standing-trance pockets | Drift: place-bound, aggressive in radius, re-form only while condition lasts (until the step passes) | Drift: water around it rises in a ring (~1 s) before a cold grasp; lantern-line: lanterns brighten amber → white, the lane frosts (~2 s) | Escort pressure; teaches lane telegraph | Short (~20 s each). |
| **E1b** | 2 × Mud Piper | Far Racks | Lure: calls in a human voice, then bog-dives | Reed tremor + gurgle before a bog-dive (~1 s) | Unease; trust your eyes | Optional fight. |
| **E2** | 2 × Reed Stalker, 1 × lurker | Gate 1 | Ambush; target crew | Reeds part in a line (~1 s) before a lunge | Defend crew | ~60 s. |
| **E3** | Drift wave; **Stillwater Serpent** | Gate 2 | Serpent: apex, sill-bound | **Coil-rise:** body lifts out of the water (~1.5 s) → straight lunge 6 m. **Tail sweep:** water bulges on its flank (~1.2 s) → arc behind it. **Submerge:** it sinks; a swirl marks where it will rise (~2 s) | High-tier family; breach set piece | 2–3 min. Ends at 50–70% HP. |
| **E4** | Drift ×2 waves, 2 × lantern-drift | Gate 3 | As E1 | As E1 | Peak pressure | ~90 s. |
| **E5** | **The Muster** (Wraith Lord) | Heart pool | Act III boss | §11.6 | Climax | §11.6 |

Drift encounters follow D-6: they disperse and re-form only while their condition lasts. All gate and lane pockets stop spawning when their step completes.

## 11.6 Boss spec: the Muster

**What it is (author truth):** a Wraith Lord, the grief of a generation of mourners gathered over the drowned Fourteenth Lot and stirred by every flush. It repeats what the convoy did: lanterns held out in lines, oar-strokes on a count, the long pull towards the deep. **It is not the convoy's crews.** It has no face, no voice, no name, and it identifies no one (evidence rule).

**What the player sees:** a tall standing mass of fog and moving water, several times human height, carrying a dozen lantern-lights at shoulder heights in a ragged line, as if held by people standing shoulder to shoulder who are not there. When it counts, a hollow wooden knock sounds from inside it, like an oar on a gunwale.

### 11.6.1 Arena

| Element | Spec |
|---|---|
| Shape | Roughly circular, ~30 m across; shallow water (ankle depth) over firm bottom everywhere the player can walk. |
| Ring stones | **Eight Marking Stones** on low plinths around the ring at ~11 m radius, each a walkable stepping surface (click-to-move onto it; no jump). |
| Inflows | The three Braid channels the player opened enter the arena at three points. **The stones nearest moving water read true.** |
| The deep | The centre (5 m radius around the heart stone) sits over the convoy holes: darker water, bubbles. The drag pulls towards it. |
| Cover | Barge ribs break the surface in a curve on the north side (block lantern-lines). |
| Exit | The Lantern Sluice behind the player. Leaving the arena does not reset the fight for 20 s. |

### 11.6.2 Mechanics

| Ability | Telegraph (readable, non-twitch) | Effect | Counter |
|---|---|---|---|
| **Lantern-line** | 3–5 of its lanterns drift out and hang in a straight row across the arena; over **2.0 s** they brighten from amber to white and the water beneath them frosts with a pale line. | A surge of cold water runs the lane: moderate damage and **chilled** (movement slowed, 4 s). | Step out of the lane (2 m is enough), or behind a barge rib. |
| **Stroke-call** | A hollow knock counts aloud, "one… two… three… four" (P3: three), one per ~1.2 s. On each knock a ripple ring (2 m) appears under each player. On the final knock the whole **muster circle** (6 m around it, edged by its own lanterns) lights. | Each ring erupts on the *next* knock (light damage). The final knock: heavy damage inside the muster circle. | Move once per knock; be outside the lantern edge on the last count. The count was taught at the evacuation. |
| **The drag** | All its lanterns swing to face one player (**2 s**); current lines appear on the water flowing from that player towards the deep. | A tether: the player is pulled slowly towards the centre (~1.2 m/s). They can still move; moving away is slowed. | **Step onto a Marking Stone that reads true.** At each drag, the 3 stones nearest the moving inflows show water standing in their notch (a thin sheet climbing the groove, a faint lap). The other 5 are dry. Reaching a reading stone: the stone holds a line (a small echo of §11.7), the drag snaps, and the Muster **staggers** for 3 s (takes bonus damage). |
| **Pulled under** | (Failure of the drag.) | If the player reaches the centre: heavy damage (35% max HP), then the water spits them out on the ring by a random stone. Drag ends. Never an instant kill; lethal only at low HP. | — |

### 11.6.3 Phases

| Phase | Health | Pattern | Transition |
|---|---|---|---|
| **P1, the Line** | 100–70% | Lantern-line (every ~12 s) and Stroke-call (count of four, every ~20 s). No drag yet. | At 70% it sinks to its waist; every lantern in the arena gutters; the fen pulses once (screen-free: a low surge sound, water rises a hand). Two **lantern-drift** adds rise at two dry stones. |
| **P2, the Pull** | 70–35% | Adds **the drag** (every ~25 s). Lantern-lines continue. Adds must be cleared or they hold lanes open (a lantern-drift alive adds a second lane to each lantern-line). | At 35% the barge ribs creak; its lanterns double. |
| **P3, the Last Muster** | 35–0% | Stroke-call count drops to **three**; lantern-lines come in two crossing lanes, telegraphed one after the other (0.6 s apart); drag every ~18 s. No adds. | At 0% it disperses (below). |

### 11.6.4 Tuning, death, co-op

| Item | Target |
|---|---|
| Solo duration | 6–8 minutes for a Milestone 3 player with cooked food. |
| Solo end state | A player who reads the count and the stones ends at 25–60% HP. A first-timer may die once or twice; the third attempt should succeed. A player who ignores the stones loses ~35% per drag and will not survive P3. |
| Damage profile | No single hit above 30% max HP except Pulled Under (35%) and the final stroke inside the circle (~30%). |
| Defeat | **Disperses.** Lanterns go out one by one, outermost first; the fog sinks into the water; the water goes slack. No loot. Nothing evidentiary. Per D-6, it would re-form if the conditions remained; §11.7 is the change of conditions. |
| Death | Respawn at the Lantern Sluice landing, 20 m from the arena. The Muster resets to the **top of the phase the player died in** (100/70/35%); adds clear; gates stay open; evacuees stay safe. Sedge is still standing at the edge when the player returns (one line, `SV-D6.20`). |
| Logout | Step `S06` persists; the Muster restarts at 100% on re-entry. |
| Co-op | Shared world creature for partners on `S06_muster`. Health scales per participant. The drag targets each participant in rotation, never two at once; stroke rings appear under every player; lantern-lines are shared. Each participant gets credit and seats their own post in their own instance (§11.7 plays for each, per player). A partner who has already completed `S06` sees a quiet heart pool and cannot see the Muster (per-player state). |
| Evidence rule | It never forms a face, says a word, carries a name, or drops anything. Its behaviours repeat a convoy's motions; no one learns who was aboard. |

## 11.7 Presentation spec: every stone holds a line

This is the echo of The True Line's discovery (TL §8), at the scale of the whole fen. It must feel like the same quiet thing, made by many hands.

| Element | Spec |
|---|---|
| Trigger | Server event `sv.fen_holds` on completion of **Seat the post** (`S07_heart_stone`). |
| Set-up (earned in play) | During Beat 3, Watchers hang a lantern at each gate stone the player opens, and through the evening at every Braid stone in the fen. By `S07`, **every Marking Stone in the fen (author 30–40, placed along the Braids, the gates, the Causeway, Reedmere's posts and Widow's Step) has a lantern beside it.** The player has been walking past them all night without being told why. |
| Duration | ~24 s: 0–3 s quiet; 3–6 s climb; 6–14 s hold; 14–18 s release; 18–24 s return. |
| 0–3 s, quiet | All fen ambience ducks to silence over 2 s: water, reeds, insects, distant crews. The player's footsteps and Sedge's breathing remain. Every lantern flame in the fen steadies at once. |
| 3–6 s, climb | At the heart stone, a thin sheet of water climbs the groove against the slack water and stands in the notch, as at Whisperflow. **At the same instant**, at every Marking Stone in the fen, the same. The player sees near stones clearly; distant ones read as each lantern catching a sudden bright line of water beside it: a constellation across the whole fen, all together. Not a wave travelling outward. Everything at once. |
| 6–14 s, hold | The whole fen surface goes flat as glass. Reflections within ~15 m lag the player by a fraction of a second (TL echo). The fog lies down on the water. Nothing else moves. |
| 14–18 s, release | Every sheet lets go at once. The fen **exhales**: one long low sound from every direction, like wind through all the reeds at the same time, though there is no wind. Visible on every nearby stone: the water level drops by a hand and stays down. The fog rolls outward from the centre and thins. |
| 18–24 s, return | Sound comes back in order: water first, then reeds, then insects, then one human voice far off: a Watcher calling "Lantern holds!" and another answering. **If `VK_COMPLETE`:** a cutter on the Reedmere walks begins to hum the listeners' tune, badly. |
| UI | None. No objective popup until sound has returned. No music. |
| Camera | Never taken. The player may turn to look at the constellation; designers should place the heart stone so the Reedmere side's lantern line is in a natural sightline. |
| Sedge | Kneeling, both hands flat in the water. Visibly exhausted after; he sits on the heart stone's plinth. One line (`SV-D7`). |
| Repeatability | Once per player. Afterwards each fen stone's inspect text reads *"The groove is wet to the notch and no higher. The water is moving."* |
| What it means | The fen's pressure was spread through the Braids. **It does not release souls, end grief, name anyone or prove anything.** The Fourteenth Lot is still at the bottom of the heart pool. |

## 11.8 The choice: Seal, Tend, or Shared

The voices are chosen for who would really argue each, and who would pay for it.

| Option | Voice | Why this voice | What happens | Real cost |
|---|---|---|---|---|
| **Seal** — close the deep fen for a generation. | **Lessa Mirepath**, supported by the keepers (Hesketh if kept; the Keeper-Lieutenant if stood down) who would post the boundary. | Lessa's whole life is "some paths are done." Tonight she reopened one, and she knows what it cost. She is the only voice with standing to say *close it*. | Keepers post a boundary of stakes and rope around the deep fen. Inside, the heart pool is left alone. Outside, heavy water is gone (D-6 **closed**). | The harshest. Mourners lose the fen: the families who still come for the Lot have nowhere near it to come. Reedmere's best cutting grounds are inside the line, so the cutters lose work. Annelise: "You've shut the door on people who still knock." |
| **Tend** — a guided remembrance channel at the fen edge. | **Annelise Reed.** Strongest if completed side quest CN (she brings the recovered offering boat and launches it as her argument). | "Light enough to carry" is her life's rule. Tending is her work. | A channel is cut at the near edge from Widow's Step: lantern-lined, with a landing for offering boats. Watchers and the memorial keeper tend it. The deep fen stays open to guided cutters. Quiet drift remains at the channel and in the margins (**tended**). | Forever-work. Someone must walk it every night. Drift never fully goes; some households will never let their children near it. Lessa: "You'll be walking people out of the water every winter." |
| **Shared** — seal the deep pools, tend the edge. | **Ansel Corrie.** `OL_LANTERN_ONLY`: settled; he hangs Joss Garrow's dark lantern at the edge as he speaks. `OL_JOSS_IN`: settled; Joss sits by Elspeth's stove behind him and Ansel nods to him as he speaks. OL not done: raw. | He is the one who walks it. He knows the deep takes Watchers (Joss) and the edge is where people need to be. | Boundary around the heart pool and deep holes; a tended channel at the near edge. | The most labour, split two ways: keepers *and* Watchers, every season. The Lot is closed for good; the wreck is never raised and no one can go to it. The cutters lose the deep grounds *and* live beside the tended edge. Maelin: "That's two jobs. Plan's got hands for one and a half." |

**Sedge** (`SV-D8.50`) refuses to choose, every time: "Not mine." If asked, he tells one truth about each: Seal holds "as long as someone keeps the rope"; Tend "keeps it heavy, a little, where people can see it"; Shared "is the most work, and work is what holds." Warm or cool by `LM_SEDGE_TRUST`; never a recommendation.

**Elspeth** gives one line on the human cost of any choice: there will be trances again somewhere, and the station must stay.

**No option is wrong.** None "kills grief" or "frees the drowned" (Main Arc movement 11). The bible §9.2 site states follow from the choice (Ending matrix).

## 11.9 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_arrive` | Go to Reedmere. | Enter Reedmere volume | Yes | |
| `S01_vigil` | Stand the vigil. | `SV-D1` end + interaction `stand_vigil` at vigil fire | Yes | Smoke-pot loaned in `SV-D2` if needed; night + Hollowed Current state begins |
| `S02_evacuate` | Bring the cutters in (0/7). | 7 × cutter-arrival events at the tally board | Yes | Trances; lanes; `SV_LESSA_ROUTE` if FW |
| `S02b_feed` | (Optional) Cook for the evacuees. | Item-given cooked food at Elspeth's station | No | `SV_FED_EVACUEES` |
| `S03_gate1` | Open the Braid gates (1/3). | Inspect gate stone + gate-board progress 100% | Yes | E2 |
| `S04_gate2` | (2/3) | As above | Yes | E3 Serpent breach; progress decays while Serpent at sill |
| `S05_gate3` | (3/3) | As above | Yes | E4 |
| `S06_muster` | Face what stands in the heart pool. | Creature `the_muster` dispersed | Yes | |
| `S07_heart_stone` | Set a post on the heart stone. | Interactions `cut_notch_heart`, `seat_post_heart` | Yes | Fires `sv.fen_holds` (§11.7) |
| `S08_choose` | Say what happens to Stillwater. | `SV-D8` choice resolved | Yes | Sets `LM_FEN_ENDING` |
| `S09_close` | Speak with Maelin. | `SV-D9` end node | Yes | Quest → Completed; MQ12 offered |

## 11.10 Flags (quest-local)

| Flag | Set by | Read by |
|---|---|---|
| `SV_EVACUATED` (count) | `S02` | Tally board prop |
| `SV_LESSA_ROUTE` | FW lane used | `SV-D3` variant; MQ12 Lessa |
| `SV_FED_EVACUEES` | `S02b` | `SV-D8` Elspeth line; MQ12 Elspeth |
| `SV_GATE_1/2/3` | gates | Lanterns at stones; MQ12 crews' lines |
| `SV_SERPENT_KILLED` / `SV_SERPENT_DRIVEN` | E3 | MQ12 Reedmere cutter bark |
| `SV_MUSTER_DISPERSED` | `S06` | `S07` enable |

## 11.11 Rewards

| Reward | Type | Notes |
|---|---|---|
| The fen's new state | World | Drift-site states change Vale-wide (Ending matrix). |
| Watcher smoke-pot | Tool | The loan is kept ("Keep it. You'll be asked again."). Item pass defines it. |
| Skill XP | Action XP | Melee, optional Cooking. No lump quest XP. |
| Reedmere access | Access | Guided cutting grounds (Tend/Shared) or the outer grounds (Seal) open as gathering areas (economy pass). |

## 11.12 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death on the lanes | Respawn at the Reedmere vigil fire; delivered cutters stay delivered; followers at the moment of death walk back to their hut. |
| Death at a gate | Respawn at Reedmere; gate progress is kept. |
| Death in the boss | §11.6.4. |
| Trance never helped | A standing follower waits indefinitely and never drowns. |
| Out of smoke | Lantern racks refill; Ansel at Reedmere refills; a follower can also be led out by hand from Walking (3 s channel). |
| Forgets Oriel's order | Gate-boards are chalked; only the next gate's winch is interactable. |
| Logout | Last persisted step; evacuees delivered stay delivered; gate progress persists per gate. |
| Fail state | None. |
| Co-op | Each partner evacuates their own seven (their own instances' followers); drift and gate enemies are shared on matching steps; gate progress is per player (a partner's crank speeds only their own instance's bar; fallback: per-player progress, shared enemies). |

## 11.13 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Follower NPCs with a trance state machine | Systems | Follow-the-carrier + 4-state trance (warning/turning/walking/standing) driven by scripted trigger volumes. |
| Gate progress bar with crew channel, decay rule | Systems | Per-player progress with NPC tick rate, player-added channel, pause-on-harass, decay while flagged creature in volume. |
| Muster boss | Gameplay + Systems | Phase thresholds, tether (drag) with per-stone "reading" flags keyed to inflow proximity, stagger state. |
| Fen-wide simultaneous presentation | Systems + art | One server event; every authored stone in the loaded area plays the climb/hold/release locally; distant stones are lantern-glints only. Audio-duck all fen emitters. |
| Hollowed Current state | Art + audio | Step-keyed fen ambience and water flow direction. |
| Lantern placement across the fen during the step | Systems | Step-keyed props. |

## 11.14 Mystery ledger entries

| Mystery | Author truth | Public belief after MQ11 | Evidence | Wrong reading | Withheld | Reveal owner |
|---|---|---|---|---|---|---|
| What the Muster was | Coalesced grief over the Lot, stirred by the flushes. | "The convoy's dead stood up." | Lantern-lines, oar counts; the Lot's barge ribs. | The convoy's crews were in it; defeating it freed them. | Who was aboard. Who ordered the flush. | Never in v1. |
| Why every stone held at once | The Braids carried the pressure to every calibration stone together. | "The fen let go." / "The Field-Mage did it." | The constellation; Sedge exhausted. | Sedge did it alone; the player did. | The Riverwarden method. | Oriel (MQ12, briefly). |
| The Fourteenth Lot | Sank in a wartime flush; hushed. | Known now to be "a lot that went down in the fen." | Guaranteed to every player before the boss by main-quest content only: MQ4's blank convoy stone (required inspect, Maelin), MQ9's carved wreck scar on the flow-table (required inspect), and Lessa's line as she pulls her stake (`SV-D3.02b`). Then the ribs in the heart pool. Never supernatural testimony. | Marrick's house did it. | Who gave the order. | Not v1. |

## 11.15 Open decisions

1. **Muster fight length** (6–8 min) is long for v1 combat. *Recommendation: keep; it is the only boss; phases checkpoint.*
2. **Annelise at the fen** requires her to travel from Ashenstead. Travel to a nearby memorial site in a crisis is ordinary work for her role; no invented history. *Recommendation: keep.*
3. **Seal's livelihood cost** for Reedmere needs an economy note (outer grounds only).

## 11.16 Internal review log

| Finding | Revision |
|---|---|
| The trance read as possession. | Never deeper than knee-deep; no voice; "heard the count" only. |
| The boss's drag was twitch-like. | 2 s telegraph, slow pull, walkable stones; Pulled Under hurts but never one-shots. |
| "Read the stone" in the boss duplicated TL without new knowledge. | Stones read true *where water moves*: the gates the player opened decide which. Sedge says it. |
| Stone presentation travelling outward contradicted "at once." | Simultaneous; distant stones shown by pre-placed lanterns. |
| Shared looked like the obvious best ending. | It carries the most labour, closes the Lot for good, and splits the cutters' loss. |
| Sedge risked recommending. | He refuses; tells one truth about each. |
| Evacuee count risked a fetch chore. | 7 people, 3 huts, max 2 trips; trances are scripted and readable. |
| Independent review pass: most players met the boss without knowing a convoy sank. | Three guaranteed main-only deliveries (MQ4 stone, MQ9 wreck scar, Lessa `SV-D3.02b`). |
| Independent review pass: gate names and order differed from MQ9. | Reedmere Weir → the Long Sill → the Lantern Sluice, "furthest from the Cut's head first", identical in both acts; furthest-stone inspect added. |
| Independent review pass: Sedge re-taught observation vs interpretation. | `SV-D1.02`'s question cut. |
| Independent review pass: OL branches. | Joss present (`OL_JOSS_IN`) or his lantern hung (`OL_LANTERN_ONLY`) or neither, at arrival and in Ansel's Shared argument. |

---

# MQ12 — The River Remains (`RR`)

## 12.1 The quest in one paragraph

The morning after the vigil the player walks the Vale and sees what their work changed. At Crestbridge they carry one more sack, the last of the far-bank debt, to Wynn Tarrow's cart, past a Keeper-Captain who was kept or a former one who now works the Cut seal with a shovel, past Tovin's sketch pinned in the keepers' hall, and past Edda Marrick at her own granary door, who offers tea and asks how the player will tell it. At the Mantle Shrine, Sedge refuses to teach them, and says why. Behind the falls, Oriel quotes the player's promise back to them and asks what mark they cut when they cut a tally. At dusk at Whisperflow Landing, where it began, the player helps light a lantern on every marker post. The crews' new tender-marks are cut into the old stone, and beside them, though nobody saw it cut, is the player's own. Then Maelin Rowe, who never crosses at night, takes the player across by lantern, because the line reads true. On the far bank the households are waiting.

**What the player should remember:** the ferry halfway over in the dark, lanterns on both banks, and Maelin not saying anything. **What the player should want next:** the commissions, and the rest of Caelmor.

## 12.2 Summary card

| Field | Value |
|---|---|
| Working title | **The River Remains** |
| Suggested content id | `lowmark.main.12_river_remains` |
| Arc position | Act III, movement 12. Final main quest. |
| Prerequisite | MQ11 completed (starts at `SV-D9`). |
| Solo / co-op | Solo. Co-op partners see their own Vale state; the crossing is per player (fallback: partners may ride along and see their own banks). |
| Target length | 15–20 min required; up to ~40 with every optional station. |
| Combat share | 0% by design. Heavy-water sites that remain active (Ending matrix) are elsewhere. |
| Skills | None required. Optional Cooking (Nan's fire). |
| Choices | Small farewells; what mark the player cuts (`RR_MARK`, cosmetic). |
| Unlocks | `LM_CIVIC_STANDING`; aspirational commission offers (§12.8). |

## 12.3 Places

All existing POIs, changed. The Ending matrix specifies the changes; the table below is what MQ12 adds.

| Area | MQ12 addition |
|---|---|
| **Crestbridge granaries and Marrick's granary** (P02) | Wynn's cart at Marrick's granary door; restitution sacks stacked (`CR_MARRICK_STORES`); keepers' seal on the door (firm/full). |
| **The keepers' hall** (P02) | Tovin's sheets pinned on the wall (named: with his name chalked under them; unsigned: without). |
| **The Cut mouth** (P10, lower end) | Stop-planks driven and earth-banked; the seal crew at work (Hesketh if stood-down; Sallow if `CR_CREW_LENIENCY`). |
| **Mantle Shrine** (P24) | Sedge, cutting reeds. Softmoss fresh on the stone. |
| **Listening Steps flow-table** (P29) | The Cut's scar now dark and dry in the miniature; the Braids running; the fen's model changed by `LM_FEN_ENDING`. |
| **Whisperflow Landing** (P04) | Five marker posts each with an unlit lantern hook; the Marking Stone with the crews' tender-marks cut beside its notch, and the player's mark among them. |
| **The far bank** | The far-bank households' landing; Nan Ferrin's house above it. **MAP VERIFICATION REQUIRED** (TL §14 item 4: which settlement lies across the crossing). |

## 12.4 Player-facing sequence

### Beat 0 — Morning (`S00_morning`)
**Objective:** *Walk the Vale.* (Sub-objectives: *Crestbridge* · *The Mantle Shrine* · *Behind the falls* · then *Whisperflow at dusk*.)
At Reedmere, optional: Lessa at the Causeway mouth (whether she puts her stake back; by `LM_FEN_ENDING`), Elspeth packing the loft, cutters sleeping in rows.

### Beat 1 — Crestbridge (`S01_crestbridge`) `[ANTAGONIST]`
**Objective:** *See what Crestbridge made of it.*
- **The last sack.** Wynn is loading the far-bank debt from Marrick's granary (`CR_MARRICK_STORES`: ordered → keepers count each sack out; offered → Marrick's own hands open the door). The player carries one sack to the cart (carry; the same interaction as MQ1). Wynn pays Dace back for the skiff from her first wage, in front of the player (`RR-D1`).
- **Hesketh** (`LM_HESKETH`): kept → on the bridge with his keepers, bandaged hands, running the countersign log; stood-down → at the Cut mouth with the seal crew, shovel in his hands, keeping their tally.
- **Tovin's sheets** in the keepers' hall (`LM_TOVIN_CREDITED`). Tovin is there, looking at them, if spoken to.
- **Marrick** at her granary door (`RR-D2`). The step completes on the end of her conversation.
Optional here: Corvin (one line), Aldric (one line), Sallow at the Cut mouth or behind the lock-up grille (one exchange), Hollis's report variants.

### Beat 2 — The Mantle Shrine (`S02_sedge`)
**Objective:** *Find Sedge.*
Sedge is cutting reeds as if nothing happened. The player can help (a Woodcutting-style cut on two reed stands; optional). The player asks him to teach them. He refuses, and says why (`RR-D3`). He asks them one question about what they saw at the heart stone, and accepts whatever the player says without correcting it (the lesson was taught in MQ3 and MQ8).

### Beat 3 — Behind the Falls (`S03_oriel`)
**Objective:** *Go behind the falls.*
At the flow-table, the miniature Vale has changed: the Cut is a dark dry line; the Braids run; the fen model is sealed, tended or both (`LM_FEN_ENDING`). Oriel quotes the player's promise (`LM_ORIEL_PROMISE`) and says whether the Vale kept it (it did: the plan was public). She asks: *"When you cut a tally, what mark do you cut?"* The player chooses one of three plain marks, **a notch with a line under it**, **a ring** or **three crossed cuts** (origin-neutral; `RR_MARK`). Oriel does not say what it is for. She will not come to Whisperflow ("Rulers have long memories for faces"). (`RR-D4`)

### Beat 4 — Whisperflow at Dusk (`S04_lanterns`)
**Objective:** *Light the crossing.*
Unlocks when Beats 1–3 are done; if it isn't dusk, "Wait until dusk" at the high landing advances the hour. At the landing the crews have cut their tender-marks beside the stone's notch, as the plan said: a row of small marks. **The player's mark is among them.** Inspect: *"The crews' marks, cut fresh. And yours, the same depth, the same hand as theirs. Nobody here saw it cut."* Maelin: "Wasn't there this morning." Nobody explains it.
The player walks the bank and **lights a lantern on each of the five marker posts** (5 interactions, 2 s each), with whoever `LM_PLAN_ROUTES` named: Maelin's hands (crews), Hollis (keepers) or both. A lantern line, made by people, where the Muster made one of cold water.

### Beat 5 — The Night Crossing (`S05_crossing`) **[PROPOSAL — DIRECTOR]**
**Objective:** *Cross with Maelin.*
*Canon flag:* the anchor says Maelin "refuses night passage through specific stretches". This beat ends that refusal **for Whisperflow only**; every other refused stretch stays refused. It is a change to anchor behaviour and needs the Director's sign-off.
Maelin reads the post herself (inspect: "Water's under the notch. The crossing reads open."). She takes the bow lantern and the player boards (the Whisperflow crossing interaction from MQ1, in its night variant: the player stands free on deck, camera theirs). **The strange moment:** passing the stone, the water lies quiet at the notch: no wake against the stone, though the ferry's wash runs everywhere else, for as long as the stone is in view. Mid-river, Maelin speaks once (`RR-D6`). Lanterns on both banks.

### Beat 6 — The Far Bank (`S06_far_bank`)
**Objective:** *Step ashore.*
The far-bank households are on the landing with lanterns (`LM_GRAIN_ROUTE`: escort, many; split, some; hold, a few, though they came). Nan Ferrin, in her own shawl from her own house, with Duchess (`RR-D7`). Nan's song follows *A Verse Kept Back*: `VK_PERF_BOTH` → she sings the words over the hum; `VK_PERF_COUNT` → she hums it as a count and says the words after; `VK_PERF_HUM` → she hums it and keeps the words; VK not done → she hums the listeners' tune with its verse missing (`RR-D7.04`). The last conversation is Maelin's at the boat (`RR-D8`). On its end node: **`LM_CIVIC_STANDING = true`**. The quest completes. No fanfare; Maelin pushes off to cross back by lantern, alone, which is the last thing the player sees her do.

### Optional stations (any time during Beats 0–4)

| Station | Who | Physical beat | Variant by |
|---|---|---|---|
| Ashenstead | Joric, Annelise | Help Annelise clear one offering basket (ME04 echo) | `LM_FIELD_FIX`; UR; `LM_FEN_ENDING` |
| Floodplain Orchards | Bryn | Turn one ditch-gate with her | `LM_BRYN_ROLL`, `LM_ORCHARD_LOSS` |
| Watchers' Lantern Post | Ansel | He gives the player the first page of his new patrol book to write the date on | OL; `LM_FEN_ENDING` |
| Brookhollow | Rhosyn (UL), Kell (BP), Ottilie | — | `UL_RHOSYN_WITNESS` / `UL_RHOSYN_STAYS` / `UL_RHOSYN_FLED`; default if UL not done (`RR-D19`) |
| Reedmere | Lessa, Elspeth | — | `LM_FEN_ENDING`, `SV_FED_EVACUEES` |

## 12.5 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_morning` | Walk the Vale. | Quest start at `SV-D9` end | Yes |
| `S01_crestbridge` | See what Crestbridge made of it. | Sack deposited at Wynn's cart + `RR-D2` end node | Yes |
| `S02_sedge` | Find Sedge. | `RR-D3` end node | Yes |
| `S03_oriel` | Go behind the falls. | `RR-D4` mark chosen | Yes |
| `S04_lanterns` | Light the crossing. | 5 × `light_post_lantern` (requires S01–S03) | Yes |
| `S05_crossing` | Cross with Maelin. | Night crossing interaction complete (arrival volume, far bank) | Yes |
| `S06_far_bank` | Step ashore. | `RR-D8` end node | Yes → sets `LM_CIVIC_STANDING`; quest Completed |
| `S0x_*` | Optional stations | Respective dialogue end nodes | No |

## 12.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `RR_MARK` (notch / ring / hatch) | `RR-D4` | Whisperflow stone prop (permanent) |
| `RR_ASKED_SEDGE_WHY` | `RR-D3` | Post-game Sedge bark |
| `LM_CIVIC_STANDING` | `S06` | Commissions (§12.8) |

## 12.7 Rewards

| Reward | Type | Notes |
|---|---|---|
| The player's mark on the Whisperflow stone | Sign of trust | **Non-mechanical** (Main Arc movement 12). No stat, no ability, no item. |
| Night crossing at Whisperflow **[PROPOSAL — DIRECTOR]** | Access | Maelin's crossing interaction is available at night from now on (only here; her other refused stretches stay refused). |
| `LM_CIVIC_STANDING` | Legitimacy | Step 1 of the commission acquisition model. |
| Wynn's coin | Currency | Small, from her first wage ("Told you, when I'm paid."). |

## 12.8 Hand-off to the aspirational commissions

`LM_CIVIC_STANDING` satisfies **step 1 (civic and narrative legitimacy)** of the approved acquisition model in `Caelmor_Aspirational_Equipment_Foundation.md`. Steps 2–5 (demonstrated equipment use, player craft contribution, skilled fitting and custody, no supernatural shortcut) belong to the commission packages and the economy pass. This package authors only the **offer line** each giver speaks the first time the player meets them with `LM_CIVIC_STANDING` (dialogue file Part 5). The offer opens the commission; it does not grant anything.

| Commission | Giver (bible §8) | Where | Variant |
|---|---|---|---|
| Keeper's Blade | Brigid Corliss | Crestbridge forge | HS completed: she says she remembers the salvage steel. |
| Bridgewarden Harness | Brigid Corliss | Crestbridge forge | Offered in the same conversation as the Blade if both are eligible. |
| Crestbridge Guard | Hesketh (`kept`) or the Keeper-Lieutenant (`stood-down`, with Hesketh's word) | Crest Hall yard | `CR_HESKETH_SELF`: Hesketh is present when the Lieutenant makes the offer and says one line. |
| Riverpath Leathers | Kell Ashby with Maelin's crews | Brookhollow tan-yard | BP completed: Kell remembers the bark. |

None of the four depends on any other Act III choice. Every player who completes MQ12 receives all four offers.

## 12.9 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Combat | None in the quest. If the player wanders into an active heavy-water site, it is ordinary world content. |
| Logout | Last persisted step; lanterns lit stay lit. |
| Missed dusk | "Wait until dusk" at the high landing. |
| Fail state | None. |
| Co-op | Per-player Vale state. The crossing interaction carries the local player; partners on the same step cross together, each seeing their own far-bank crowd (fallback: partners ride along and see the host's crowd count but their own Nan line). |

## 12.10 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Night variant of the Whisperflow crossing interaction | Systems | Same crossing interaction, night lighting, bow lantern prop, stone-wake suppression while the stone is in view. |
| Player-mark decal on the Whisperflow stone keyed to `RR_MARK` | Art + Systems | Per-player prop (fallback: a mark appears only for the local player; partners see their own). |
| World-state presentation for the Ending matrix | Systems | Per-player props keyed on Act III flags. |

## 12.11 Open decisions

1. ~~`LM_ORIEL_PROMISE` value names.~~ Resolved: `RR-D4.02` is keyed to `aloud` / `many_hands` / `return` and quotes Act II's exact words.
4. **Maelin's Whisperflow night refusal ends** **[PROPOSAL — DIRECTOR]**: all her other refused stretches stay refused. This changes anchor behaviour and is listed for the Director.
2. **Who cut the player's mark.** Deliberately unanswered. Compatible with Oriel, with the crews, with Sedge. *Recommendation: never answer it in v1.*
3. **Far-bank settlement identity** (TL §14 item 4) affects only travel lines.

## 12.12 Internal review log

| Finding | Revision |
|---|---|
| MQ12 risked becoming an administrative "talk to everyone" chain. | Three required stations with one physical act each (carry, cut reeds, choose a mark), then lanterns and the crossing. Everything else optional. |
| Oriel cutting the mark herself would put a Riverwarden in public. | She asks for the mark; nobody sees it cut. |
| Sedge's refusal risked a lecture. | Three lines, and he asks the player a question instead (his voice rule). |
| Commission hand-off risked a reward dump. | Offer lines only; the commissions open, they don't grant. |
| Marrick's last scene risked gloating. | She is gracious and asks the player one question; the player decides how to answer. |
| Independent review pass. | Promise keys fixed (blocker). Maelin's night crossing tagged **[PROPOSAL — DIRECTOR]**. Nan's song keyed to `VK_PERF_*`. Rhosyn's station branches on `UL_RHOSYN_WITNESS` / `STAYS` / `FLED` with a default. Sedge's heart-stone question no longer corrects. Debt lines no longer say "eighty". Sallow's chained line no longer cuts the chain. |

---

# Ending matrix

This section is the single reference for how Act III's inputs and outputs change MQ12 and the post-game Vale. Everything here is per-player presentation (bible §9).

## E.1 Fen ending → Stillwater, drift sites, NPCs

### E.1.1 Stillwater presentation

| Element | **Seal** | **Tend** | **Shared** |
|---|---|---|---|
| Deep fen | Keeper boundary of stakes, blessed rope and lantern posts around the deep fen; one boundary stone carries the tenders' marks. Inside: inaccessible (closed). | Open; guided cutting only (Lessa's knots on the paths). | Boundary around the heart pool and deep holes only. |
| Near edge | Ordinary fen margin; heavy water gone; reeds regrowing green within a season (season-keyed prop). | **The remembrance channel** from Widow's Step: a short lantern-lined cut with a stone landing for offering boats. Quiet drift (tended) visible at night drifting like slow lanterns; does not engage unless attacked. | The remembrance channel as Tend, shorter, ending at the boundary rope. |
| Fog | Thin; gone by mid-morning. | Lies on the channel at dusk; thin elsewhere. | As Tend at the channel; thin at the boundary. |
| Heart pool | Unseen (inside boundary). | Visible from the Lantern Sluice: still water, barge ribs, the player's post on the heart stone. | Visible from the boundary: the post, far off. |
| Offering boats | Moved to Widow's Step's scraps (households leave them at the top of the embankment). | Launched on the channel; Annelise clears them each morning. **CN completed:** the recovered boat is moored at the landing, kept. | Launched on the channel. |
| Joss Garrow (OL) | `OL_LANTERN_ONLY`: his dark lantern hung on the boundary post nearest the Lantern Post. `OL_JOSS_IN`: no lantern; Joss sits on the Lantern Post bench at dusk, Ansel beside him. OL not done: nothing. | `OL_LANTERN_ONLY`: hung at the head of the channel. `OL_JOSS_IN`: Joss sits at Elspeth's station at the channel head at dusk. Not done: nothing. | `OL_LANTERN_ONLY`: hung where the channel meets the rope. `OL_JOSS_IN`: Joss at the channel head with Elspeth. Not done: nothing. |

### E.1.2 Drift-site states (bible §9.2) after MQ11

Sites quieted in Acts I–II stay quieted. "As left" means the state the player's own Act I–II or side-quest play left it in.

| Site | Seal | Tend | Shared |
|---|---|---|---|
| Stillwater deep pools | **closed** | **tended** | **closed** |
| Stillwater margins and remembrance channel | quieted | **tended** | **tended** |
| Widow's Step | quieted | **tended** | **tended** |
| Orchard pool (MQ3), ditch (MQ3), Bramblelock pool (MQ4), Drowsebank race (MQ6), orchard dike (MQ7), Mantle channel (MQ8) | quieted | quieted | quieted |
| Dunnock farm cellar (*The Whispering Door*) | as left | as left | as left |
| Watergarden outlet (CN) | as left | as left; if CN completed, **tended** | as left; if CN completed, **tended** |
| Old Lantern's bend (OL) | OL completed: **quieted** (stays so). Not completed: as left (active until OL is done). Not a residual site. | same | same |
| Residual pockets for progression | Two **active** pockets at the Seal boundary's outer reed-pools (where pressure frays at the rope), plus the **Stillwater far-leg pockets** | Two **active** pockets in the far margins beyond the channel, plus the **Stillwater far-leg pockets** | One **active** pocket at the boundary, one in the far margins, plus the **Stillwater far-leg pockets** |

**Why residual sites:** bible §9.2 requires a small set of heavy-water sites to stay active so Wraith combat stays available for progression. Every ending keeps the same count (three: two ending-specific pockets plus the Stillwater far-leg pockets along the old Watchers' far leg) at different places, so no ending is "easier" for progression. Old Lantern's bend is never a residual site: completing *Old Lantern* quiets it for good.

### E.1.3 NPC positions after MQ11

| NPC | Seal | Tend | Shared |
|---|---|---|---|
| **Lessa** | Back at Reedmere; her stake **goes back** at the Causeway mouth. "That one's done again." | Walks the deep paths with guided cutters; her stake stays out. | Stake back at the Causeway; she guides at the boundary. |
| **Annelise** | Ashenstead; visits Widow's Step weekly with a basket; one bitter-kind line. | At the remembrance channel at dawn and dusk (or her watergarden keepers, if `LM_PLAN_MEMORIAL = gardens` she is there daily). | At the channel at dusk. |
| **Ansel** | Patrols the boundary rope. | Patrols the channel; new patrol book. | Both, and says so. |
| **Hesketh / Keeper-Lieutenant** | Keeper post at the boundary (kept: Hesketh inspects it; stood-down: the Lieutenant's keepers, Hesketh among the hands if self). | No keeper post at the fen. | Keeper post at the boundary. |
| **Elspeth** | Ashenstead; trance-care station kept at Reedmere's loft, rarely used. | Station at the channel head, used. | Station at the channel head. |
| **Sedge** | Mantle Shrine. | Mantle Shrine; seen at the channel at dawn some days, never spoken to there. | Mantle Shrine. |
| **Reedmere cutters** | Work the outer grounds; fewer at the racks. | Work the deep grounds with guides. | Outer grounds; some at the channel. |

## E.2 Input flags → MQ12 scenes and post-game world

| Flag / condition | Value | MQ12 scene change | Post-game world |
|---|---|---|---|
| `LM_TL_EVIDENCE` | keepers | Hollis at Whisperflow: "I wrote that one down too." | Keepers' copy of the Whisperflow report in the keepers' hall (inspectable). |
| | riverfolk | Maelin: the crews pulled the second false post too. | Second false post leaning at the crew fire. |
| | player | Hollis: "You still have that post?" Option to give it to the keepers' hall now. | If given, it hangs beside Tovin's sheets. |
| `LM_GRAIN_ROUTE` | escort | Far bank: many lanterns; a householder thanks the keepers by name of office. | Far-bank households greet the player. |
| | hold | Far bank: a few lanterns; "We were hungry a while. Then we weren't." | Neutral barks. |
| | split | Far bank: some lanterns; mixed barks. | Mixed barks. |
| `LM_LOCK_STATE` | smashed / chained | Sallow's line names the broken gear or the keepers on his chain. | Hollow Lock: winding floor broken (smashed) or still chained and stop-planked (chained); sealed either way. |
| `LM_FIELD_FIX` | circle | Annelise: the circle stones were relaid "a hand to the left. Nobody minded." | Circle relaid over the cleared grate. |
| | plot | Joric: the relief ditch through his plot runs clear; he's planted the banks. | Ditch with planted banks. |
| | dike | Joric and Annelise: the fields came in a season late; both fields are whole. | Dike around both. |
| `LM_TOVIN_CREDITED` | named | Keepers' hall: sheets pinned with "T. PELL." Tovin: "They put my name on it. I keep reading it." `CR_TOVIN_STOOD`: "I said one thing in that hall. I keep hearing it." | Tovin barks at Drowsebank: steadier. |
| | unsigned | Sheets pinned without a name; Tovin looks at them: "Someone pinned one of mine. Nobody knows. That's all right." | Same sheets; quieter barks. |
| `LM_BRYN_ROLL` | commons | Bryn on the commons roll, with a teacher she argues with. | Bryn teaching two orchard hands. |
| | household | Bryn: "Still household. Still mine. Still nobody's business." | Bryn alone at the ditches, faster than anyone. |
| `LM_ORCHARD_LOSS` | none / partial | Orchard whole; or one section replanted with whips, Bryn swearing at each one. | Orchard props. |
| `LM_SEDGE_TRUST` | warm / cool | Sedge's refusal wording (dialogue file). | Sedge barks at the shrine: a nod (warm) or nothing (cool). |
| `LM_ORIEL_PROMISE` | aloud / many_hands / return | Oriel quotes the player's words (`RR-D4.02`). | — |
| `LM_MARRICK_EXPOSED` | true | Marrick's scene. | House Marrick's banner off the Board bench. |
| `CR_TERMS` | bare | Marrick at her own door, still a householder of standing, off the Board. | Marrick in Crestbridge with households, warmly received by some. |
| | firm | Granary under keepers' seal; she sits on her own step. | Seal on her door; fewer callers. |
| | full | Granary open, keepers counting restitution; she watches and offers tea anyway. | Empty granary; Marrick writing at a table in her window. |
| `CR_MARRICK_STORES` | offered / ordered | Households say "Marrick's gift" (offered) or "Marrick's debt" (ordered). | Same barks. |
| `LM_HESKETH` | kept | On the bridge with the countersign log. | Commission giver: Crestbridge Guard. |
| | stood-down | At the Cut mouth with a shovel. `CR_HESKETH_SELF`: "I did it myself. That's the only part I'm proud of." | Works the Cut seal and later the Crestbridge Braid gate. The Keeper-Lieutenant gives the commission. |
| `CR_CREW_LENIENCY` | true / false | Sallow at the Cut mouth (true) or behind the grille (false). | Lock crew on seal and Braid work (true). |
| `CR_HAULED_CREWMAN` | true | The young pole-man, now on the seal crew, nods to the player. | — |
| `UL_RHOSYN_WITNESS` / `UL_RHOSYN_STAYS` / `UL_RHOSYN_FLED` / UL not done | | Witness: clerking for the keepers, wry. Stays: a stall writing letters. Fled: absent; Ottilie's line about the dark cellar. Not done: no Rhosyn; a dock bark about the Lamb's shut back room. (`RR-D19`) | As MQ12. |
| `LM_PLAN_ROUTES` | crews / keepers / shared | Who lights the Whisperflow lanterns with the player. | Who calls crossings on flood nights (barks; crossing-closed notices signed by crews, keepers, or both). |
| `LM_PLAN_MEMORIAL` | watchers / gardens / reedmere | Who stands at the fen's memorial ground in E.1.3. | Same. |
| `OL_LANTERN_ONLY` / `OL_JOSS_IN` | | Ansel's new book, first entry: "Joss's lantern hung." / "Joss sat with me. Ate. Didn't speak." | Lantern at the fen, or Joss at the Post bench (E.1.1). `old_lantern_bend` quieted. |
| `VK_PERF_BOTH` / `VK_PERF_COUNT` / `VK_PERF_HUM` / VK not done | | Nan's far-bank song per performance; hum with a missing verse by default (`RR-D7.04`). | The thaw song sung at Greyharrow at season change (VK done). |
| completed side quest NT | | Dace in the crossing crew: "Night crossing. Don't tell my mam." | Dace at the landing. |

## E.3 Combined Crestbridge states (terms × Hesketh)

| | **kept** | **stood-down** |
|---|---|---|
| **bare** | Hesketh guards a Board that Marrick left gracefully. He looks over his shoulder. | Hesketh shovels; Marrick visits the seal crew with bread. He accepts it. That is the whole scene. |
| **firm** | Hesketh posts the seal on Marrick's granary himself, and hates it. | The Keeper-Lieutenant posts it; Hesketh watches from the Cut. |
| **full** | Hesketh counts the restitution sacks out personally. | The Lieutenant counts; Hesketh carries. |

## E.4 What every ending shares

Crossings reopen under accountable rules (crews' marks on stones, keepers' countersign). The far bank is owed and paid. The present wrong is answered in public. Stillwater is safer. Lowmark has a way to tend future water wounds: the roll in three books. Sedge stays a reed-cutter. Oriel stays behind the falls. The Fourteenth Lot stays at the bottom of the heart pool, and nobody in v1 learns who gave the order. That is the complete local ending of Main Arc movement 12.

---

# Act III review log (cross-package)

| Check | Result |
|---|---|
| Canon anchors | Maelin: no new history; her night crossing is a choice about one stretch, consistent with "refuses night passage through specific stretches." Corvin: regrets the ledger aloud once (MQ10). Aldric: convenes, does not rule; no wartime service. Lessa: reopens one done path; no Mire kinship. Annelise: no names spoken. Tovin: never names it, never solves; his one line in the hall describes ("I drew what the floor did"). Joric: decides about his field (Act II); MQ12 only reflects it. No ages, kinship, travel or record custody invented. |
| Evidence rule | Exposure rests on chips only; supernatural items refused at the table; the water-gate stilling is mocked and proves nothing; the Muster names no one; the fen-wide hold proves nothing; Sallow's account is words after surrender, not a combat drop. |
| Soft-locks | Seven main-only chips; singe never invalidates; every trance resolves; gate order chalked; boss phase checkpoints; MQ12 has no combat or timers. |
| Duplicate structures | MQ10 defence ≠ MQ4 assault; table-laying ≠ TL testimony; MQ10's water-gate is a chase, not a channel; the three-gate hold is the arc's culminating channel set piece (MQ4's crank is the other); seat-the-post deliberately echoes TL as the climax. |
| Independent review pass | Applied: promise keys; item custody; C8 = `UL_LEDGER` (+`UL_LEDGER_CUT`, `UL_RHOSYN_WITNESS`); water-gate stilling tied to the plan's "Aye"; water-gate chase; Sedge off the public floor; waits replaced by walks; culverts planked so the fen holds its breath; Fourteenth Lot delivery before the boss; Braid gate names/order; OL, VK and UL branches with defaults; residual drift sites; Sallow yield and crew "downed" tagged; Maelin's night crossing tagged. |
| Quest items | 1 new (`CR_board_minute`) of 2 allowed. |
| Flags | `LM_PLAN_ROUTES`/`LM_PLAN_MEMORIAL` documented as the `LM_PLAN_*` family. No other new `LM_` flags. Quest-local flags use CR/SV/RR. Dialogue file checked against §0.4–0.5 and each quest's flag table. |
| Player address | Origin- and address-neutral; they/them in prose; the mark choice is three plain cuts. |
| No spellcasting, cutscenes, rep, lump XP | Smoke-pot is a Watcher tool; Sedge's work is shown, never granted; camera free throughout; no reputation; XP from actions. |
| Movement | No jump; Muster stones are walkable; no agility trigger required in Act III. |
| Size | Act III quest file is above the 60–80 KB target because MQ11 carries the only boss spec and the fen presentation; MQ12 and the matrix were kept tight. |
