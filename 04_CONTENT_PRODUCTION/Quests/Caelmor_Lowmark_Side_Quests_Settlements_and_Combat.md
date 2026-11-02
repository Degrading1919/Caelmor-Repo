# Lowmark Side Quests — Settlements and Combat Challenges

**Status:** Authored production content for Creative Director milestone review (bible §12, batch 3). Six side-quest packages: three settlement stories (**UL** *Under the Lamb*, **NB** *Night Bridge*, **UR** *Unreplanted*) and three combat challenges (**NT** *Night Ferry*, **FW** *Fen Watch*, **OL** *Old Lantern*). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[CANON]** items come from Phase 1 or the reconciled `LORE/` files. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. No schema, JSON or C# is created here.

**Controlled by:** `Caelmor_Lowmark_v1_Narrative_Production_Bible.md` (author truth, cast, POIs, flags §9, encounter families §10, conventions §11). **Format and voice:** `Caelmor_Lowmark_Quest_The_True_Line.md` and Part 1 of `Dialogue & Narrative/Caelmor_Lowmark_The_True_Line_Cast_and_Dialogue.md`. Dialogue for all six quests is inline in each package (§x.12), in the True Line node format, with node ids `<CODE>-D<n>.<nn>`.

---

## 0. Slate header

### 0.1 The six quests at a glance

| Code | Quest | Type | Unlock gate | Where | Core verb (primary first) | Main-arc link | Feeds |
|---|---|---|---|---|---|---|---|
| **UL** | Under the Lamb | Settlement (Brookhollow) | MQ4 *The Night Flush* Completed (`LM_LOCK_STATE` set); offer window closes when MQ10 starts (UL.1) | P01, P18 | **infiltrate**, read, choose | Sallow's crew lies low after the Lock; their pay book is under the Lamb, and its pay is drawn on the Provisioner's purse under the Board seal `[ANTAGONIST]`. | **MQ10 evidence chip** (`UL_LEDGER`, weaker with `UL_LEDGER_CUT`); Rhosyn's outcome for MQ10 and MQ12 (`UL_RHOSYN_WITNESS` / `UL_RHOSYN_FLED` / `UL_RHOSYN_STAYS`); MQ7 Ottilie variant (request) |
| **NB** | Night Bridge | Settlement (Crestbridge) | MQ2 *Short Measure* Completed (`LM_GRAIN_ROUTE` set) | P02 underside | **climb**, inspect, fight | Toll enforcement after the grain shortage; Aldric's useful-but-blind authority. Reed Stalkers' first appearance for most players. | Underside route (`NB_UNDERSIDE_OPEN`); optional MQ10 approach to the water-gate (request) |
| **UR** | Unreplanted | Settlement (Ashenstead) | MQ3 *Heavy Water* Completed | Joric's plot beside P20 | **clear**, uncover, listen (drives off returning goblin raiders; MQ3's culvert den is not refought) | Seeds the ground MQ5 may cut through. | **MQ5** "cut through Joric's plot" option (`UR_GATE_RUN` / `UR_LINE_STAKED` / `UR_LEFT`); epilogue reads `LM_FIELD_FIX` |
| **NT** | Night Ferry | Combat challenge | MQ2 Completed | P19 Greyharrow Reach | **defend** a crowd through the night | Maelin's refusal of night passage, understood. | MQ12 night-crossing echo (`NT_DAWN_SEEN`, request) |
| **FW** | Fen Watch | Combat challenge | MQ5 *The Guide-Line* Completed (after MQ3, Lessa gives a soft "Not yet") | Reedmere approaches (P06) | **hold a boundary**, elite fight | Lessa's "done" paths; high-tier family preview. | **MQ11 option:** Lessa's guide route as an optional approach (`FW_GUIDE_ROUTE`) |
| **OL** | Old Lantern | Combat challenge (miniboss) | MQ3 Completed (Ansel's patrol book) | Old Lantern's bend, Stillwater edge (P21 start) | **track**, fight, recover | Ansel's arc; what long exposure does. | Drift site `old_lantern_bend` → quieted **permanently, in every fen ending**; MQ11/MQ12 Ansel and Watcher lines (`OL_JOSS_IN` / `OL_LANTERN_ONLY`) |

**Recommended order of discovery** (not enforced): NB and NT open after MQ2 and sit in Heartlands towns the player already visits; UR and OL open after MQ3, when Ansel and Ashenstead are known; UL opens after MQ4; FW opens after MQ5, when the player has Milestone 2 equipment (a player who visits the warning post after MQ3 gets Lessa's soft warning, `FW-B0`, and no offer). UR should be *offered* before MQ5 (Joric's bark appears on MQ3 completion), but it stays playable after MQ5 and reads the result.

### 0.2 Flags other packages read

| Flag | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| `UL_LEDGER` | bool | UL `S06_deposit` | MQ10 hearing | Adds the **crew ledger** chip to the long table. It shows Lock work paid to "G.S." on the wrong nights, pay **drawn on the Provisioner's purse** with the **Board seal stamped on the pay chits** `[ANTAGONIST]`, and twelve crew passes in borrowed hauler names. Full strength: it shows who paid (recommended weight 2; Act III owns weights). Holder at the table: Rhosyn if `UL_RHOSYN_WITNESS`, otherwise the keepers' locked record box from `UL-D6`. |
| `UL_LEDGER_CUT` | bool | UL choice C (always with `UL_RHOSYN_STAYS`) | MQ10 | The chit and pass pages are **torn out**. Still a valid chip but weaker (recommended weight 1): the purse line survives in the book-keeper's hand, but without the Board-sealed chits it is the crew's word only, and MQ10 cannot name the licensed haulers. |
| `UL_RHOSYN_WITNESS` | exactly one of the three `UL_RHOSYN_*` | UL choice A | MQ10, MQ12 | Rhosyn agrees to testify. She attends MQ10 under keeper protection and attests the ledger hand (bible §5.3 "MQ10 witness"); this strengthens terms but is not itself a chip. MQ12: she is clerking for the keepers. |
| `UL_RHOSYN_FLED` | (as above) | UL choice B | MQ10, MQ12 | Rhosyn fled downriver on the dawn barge. She is **absent** from MQ10 and MQ12: nobody can say who wrote the book. The chip is full strength. MQ12: her nook is empty; Ottilie's bark only. |
| `UL_RHOSYN_STAYS` | (as above) | UL choice C | MQ10, MQ12 | Rhosyn stays in Brookhollow on Ottilie's label bench; she is not a witness and does not attend MQ10. The cellar stays open. MQ12: she has a letter-writing stall. |
| `UL_OTTILIE_TOLD` | bool | UL optional step | MQ7 (request) | Ottilie has the riverglass bowl ready without a wait; one warmer line. Nothing breaks if unread. |
| `NB_UNDERSIDE_OPEN` | bool | NB completion | World; MQ10 (request) | Underside traversal route between the south abutment and the Crest Hall water-gate side. MQ10 may offer it as an optional approach to the water-gate (MAP VERIFICATION REQUIRED); nothing depends on it. |
| `UR_GATE_RUN` / `UR_LINE_STAKED` / `UR_LEFT` | exactly one | UR `D6` | MQ5 | Changes the "cut through Joric's plot" option (see UR §8.2). Never removes it. |
| `NT_DAWN_SEEN` | bool | NT completion | MQ12 (request) | One Maelin line at the night crossing. |
| `FW_GUIDE_ROUTE` | bool | FW completion | MQ11 | Lessa's kept path becomes an optional Phase 1 approach. |
| `FW_BED_SHARED` / `FW_ROUTE_KEPT` | exactly one | FW choice | MQ11 (request) | Whether cutters' skiffs use the route (variant only). |
| `OL_JOSS_IN` / `OL_LANTERN_ONLY` | exactly one | OL choice | MQ11, MQ12 | Drive Ansel and Watcher lines. `OL_JOSS_IN`: Joss is among the Reedmere evacuees in Elspeth Quill's care; his hook at the Post stays empty and no lantern is hung. `OL_LANTERN_ONLY`: Joss's lantern hangs on the Post hook **still burning** (it never goes out); Joss is never in a crowd. |
| drift site `old_lantern_bend` | quieted | OL `S07_book` | MQ11, MQ12, Act III ending matrix | **Contract:** completing OL quiets the bend **permanently, under every `LM_FEN_ENDING` value and either OL choice**. Act III must not list it as active or residual for a player who completed OL. If OL is not completed, the bend is whatever Act III authors. |
| *(read)* `HW_DEN_CLEARED` | bool | MQ3 (Act I) | UR | One callback line only. MQ3 owns the burned-culvert den; UR never refights it. |
| *(read)* `WC_BARNS_CLEARED` | bool | WC (Work and Skills) | UR | One line that the raiders came back to the P20 barns. |
| *(read)* `LM_FIELD_FIX` | enum | MQ5 | UR | Dig count and epilogue. |

"(request)" marks a line asked of another package that nothing depends on. No new region-level `LM_` flags are created. All quest-local flags use the quest code prefix.

### 0.3 Shared rules for all six packages

- **Quest items: none.** Every carried thing (Ottilie's crate, the crew ledger, the rubbing cloth, a goblin-stolen seed basket, the lantern) is a **carry-state object** (bible §11.6). Reward tools are named functionally.
- **Steps** use `S00_…` ids scoped to the quest. **Completion events** are the True Line set: enter-volume, inspect, interaction-complete, item-given/carry-deposit, creature-defeated, dialogue-node-reached, plus *watch interaction* (advance the hour, as in MQ4).
- **No quest can fail.** Losses are consequences (flags, props, lines), never a failed state. Death respawns at the quest's named safe point with step and flags intact. Logout restores the last persisted step; channels and carries are discarded and a dropped carry-state object returns to its source.
- **Co-op:** independent instances; shared world creatures give step credit to every participant on that step; quest-state props are presented per player (True Line §12 fallback applies).
- **Human enemies in settlements** (Smugglers family) are *downed* at 0 HP: they stay down and out of the fight, presented as beaten rather than killed. Joss Garrow yields. This matches MQ10, where Sallow yields `[ANTAGONIST]`. **[PROPOSAL — DIRECTOR]** presentation rule; no AI flees at low HP.
- **Evidence rule:** every fact in these quests is carried by a record, an object, a place or a person. Drift, lagging water and a lantern that burns dry never identify anyone. Combat drops nothing that advances an investigation.
- **Agility triggers** are used in NB, UL and OL. Each has a walkable fallback named in its place table.
- **Skills:** Melee, Woodcutting, Hunting, Cooking only (no Ranged, Fletching or Mining). Exact levels belong to the Gameplay Designer.

### 0.4 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| The True Line | Reads a bank, wades, cuts and seats a post, proves a lie | — |
| UL | Gets into a guarded cellar by errand, pass or river door; carries a book out | TL (no investigation of a site); MQ10 (no hearing) |
| NB | Climbs the underside of a bridge at night, reads cut marks by raking lantern light | SB (tower climb reads a wall indoors; NB is exterior traversal with predators) |
| UR | Clears scrub and a nest with their hands, drives raiders off a threshing floor; uncovers a buried gate | MQ5 (excavates a culvert); WC (tracks, does not clear) |
| NT | Holds a lantern ring around a crowd for a night; walks people back from a bad boat | TL (investigation and a single boar); MQ10 (siege of a building) |
| FW | Re-sets a boundary line, pulls people back across it, holds it against an apex predator | MQ11 (holds channel gates under Wraith pressure) |
| OL | Tracks one man's patrol, fights him without killing him, brings him or his light home | MQ10 Sallow `[ANTAGONIST]` (crew boss in a building); MQ11 Muster (Wraith Lord) |

---

## UL — Under the Lamb

### UL.1 Summary card

| Field | Value |
|---|---|
| Suggested content id | `lowmark.side.under_the_lamb` |
| Type | Settlement story, Brookhollow (bible §7) |
| Unlock | MQ4 Completed. Offered by Ottilie Penner at her glass shop, or by entering the Drowned Lamb taproom with the quest available (crew bark). **Offer window:** MQ4 Completed until MQ10 becomes Active. If UL has not been accepted by then it is withdrawn (Ottilie bark: *"Keepers emptied the Lamb's cellar. My hens' bowls are evidence now."*). If UL is Active when MQ10 starts, it continues; completed after the MQ10 hearing, the ledger goes to the keepers' archive (`UL-D6.05`) and lays no chip. **After MQ6** (the keepers bind the crew at Drowsebank, Act II `TF-D8`): the taproom holds only the remnant hands and the door-man, and Rhosyn is packing (variants in UL.2, UL.4, UL.12). |
| Length | 25–35 minutes |
| Combat share | 0–30%, chosen by the player. Every route into and out of the cellar can be taken without a fight. |
| Skills | Melee (optional), Cooking (optional: a meal for the hungry crewman) |
| Choice | What happens to Rhosyn Lyle (3 options; each costs something) |
| Outputs | `UL_LEDGER` (MQ10 chip), `UL_LEDGER_CUT`, exactly one of `UL_RHOSYN_WITNESS` / `UL_RHOSYN_FLED` / `UL_RHOSYN_STAYS`, `UL_OTTILIE_TOLD` |
| Canon used | Brookhollow's concealed smugglers' cellar under a riverside tavern, reached by a back-room trapdoor; contraband riverglass, forbidden texts and Emberholt steel traded there (dossier §V.1, [CANON]). Riverglass as very good glass for bowls (§X). Smugglers family (§VIII). |
| New | The Drowned Lamb by name (bible P01/P18), Ottilie's seconds, Rhosyn Lyle, Mott Pask the landlord, Fitch the hungry crewman, the river door, the ledger. |

**One paragraph.** Since the Hollow Lock was shut, Gideon Sallow's crew has been drinking at the Drowned Lamb and waiting for word `[ANTAGONIST]`. Ottilie Penner's seconds (bowls she sets aside as flawed) keep vanishing from her yard and turning up in the cellar under the Lamb as "contraband riverglass". She went down to buy them back, was turned away at the stair, and heard the crew argue about pay "in the book". The player gets into the cellar without a stealth system: carrying Ottilie's crate down as the expected glass delivery, showing a crew pass bought from a hungry crewman, coming up the old river door from the docks, or simply walking down and fighting. The book records the crew's pay as drawn on "the Provisioner's purse", and the pay chits tipped in at the back carry the Provision Board's seal `[ANTAGONIST]`: it shows who paid. It is kept by Rhosyn Lyle, a charming forger who writes crew passes for Sallow so that she can afford to write work papers for displaced workers. She hands it over, or the player takes it. The ledger goes to the keepers. Rhosyn cannot stay hidden once it is gone, and what happens to her costs somebody something.

**Remember:** the bowls on the rack, each holding a bead of water at exactly the same height. **Want next:** the hearing where the ledger is laid on the table.

### UL.2 The place: the Drowned Lamb and its cellar (P01, P18)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Taproom** | Hook, crew, hungry crewman | Five crew at the river-side table, palms rope-burned. An empty chair at the head of it that nobody takes; one man touches the table edge before every drink, a habit copied from someone who isn't here `[ANTAGONIST]`. The landlord, Mott Pask, polishes one tankard all evening. **After MQ6:** two remnant hands and empty chairs; the head chair has been taken away. |
| **B. Back room** | Errand and force routes | Barrels, a trapdoor with a bell-pull beside it. Chalked tallies on the doorframe: deliveries, in a carter's strokes. A sack of sawdust at the trapdoor for wet boots. |
| **C. Stair and door-man's alcove** | The challenge point | A stool, half a pie, a charcoal list on the wall of who may be let down. One line reads only "glass — market day". |
| **D. Cellar market** | The trade | Racks of riverglass; crates of steel with the stamps chiselled off; wrapped bundles of books tied shut (not readable; canon contraband, contents left to later content). A buyer's mark in red wax on every bowl. |
| **E. Rhosyn's nook** | The forger and the book | A seal press, eleven inks, references in a dozen different hands, all hers. A blanket folded on a crate: she sleeps here. Pinned list of names, each with a place: "Hand, Greyharrow ferry — placed." "Drying racks, Brookhollow — placed." The crew ledger, open, a pen across it; pay chits pinned in at the back, each with a red seal. **After MQ6:** half the inks are already in a crate. |
| **F. River door and tunnel** | Back route in and out | A brick culvert from the cellar down to an iron grate under the docks, on a winch. A small crossing marker inside the tunnel mouth (the True Line reading works here). The delivery skiff ties up at the grate at the evening bell. |
| **G. Keepers' river post** | Deposit | A keepers' hut on the Brookhollow docks with a lamp and a ledger shelf of its own. |

**Moment of unease (D):** each riverglass bowl on the tilted rack holds a bead of condensation, and every bead sits at the same height, level across the rack as if the shelf were flat. A crewman throws sacking over the rack when he sees the player looking: *"They do that when the river's up. Don't stare at them."* No interaction beyond inspect. It explains nothing.

### UL.3 Player-facing sequence

**Beat 0 — The missing seconds (`S00_hook`).** *Objective: Find out where Ottilie's glass is going.* Ottilie (`UL-D1`) names the Lamb, the cellar and "the book". If the player starts at the taproom instead, the crew bark (`UL-B1`) gives the same objective and Ottilie's dialogue becomes optional.

**Beat 1 — A way down (`S01_way_in`).** *Objective: Get into the cellar under the Lamb.* Four routes, any one completes the step; the player can try several.

| Route | What the player does | Challenge at the stair | Flag |
|---|---|---|---|
| **Errand** | Ottilie packs a crate of seconds. The player carries it (carry-state; sprint allowed) from her yard to the Lamb's back room. | Door-man `UL-D2`: "Glass?" — "Market-day glass." He waves the player down and tells them to set it on the racks. | `UL_ENTRY_ERRAND` |
| **Pass** | A hungry crewman in the taproom (`UL-D3`) will sell his crew pass for a hot meal (Cooking at the taproom hearth, any cooked food) or a small payment. | Door-man reads the pass, says it's a good one, and lets the player down. | `UL_ENTRY_PASS` |
| **River door** | From the docks, enter the culvert. **Timing:** at the evening bell the delivery skiff ties up and the grate is winched open; walking in while the skiff crew unloads is clean. Outside that window the grate is down and the player cranks it (4 s channel, loud: it wakes River Leeches in the tunnel, E3). The tunnel marker reads shut by day (flooded to the knee, slower) and open after the bell. | None. The tunnel comes up behind the door-man, beside Rhosyn's nook. | `UL_ENTRY_RIVER` |
| **Force** | Refuse the challenge, or attack. | Door-man and one crewman fight (E1); the cellar crew join (E2). | `UL_ENTRY_FORCE` |

There is no line-of-sight detection. Challenges are fixed volumes that start a short dialogue. A player with no cover can always talk their way to "force", and a player who chooses force can always win it.

**Beat 2 — The forger (`S02_find_rhosyn`).** *Objective: Find the crew's book.* In the cellar the crew (if not fought) are busy and ignore anyone the door-man let down. Errand players first set the crate on the racks (`S01a_set_crate`), which is where they can find Ottilie's maker's dot under the red wax (optional `S02b_dot`). The book is on Rhosyn's desk. `UL-D4`: she knows at once the player is not crew, because she wrote every crew pass in Brookhollow.

**Beat 3 — The book (`S03_read_ledger`).** *Objective: Read the ledger.* Three inspect pages (all required): **the Lock line** (*"Lock work, G.S., paid in full, four nights running"*; with MQ3 done, *"The nights are the wrong nights in Ansel's book"* `[ANTAGONIST]`), **the purse** (*"Drawn on the Provisioner's purse"*, with pay chits pinned in at the back, each stamped with the Provision Board's seal and signed "received" in Rhosyn's hand `[ANTAGONIST]`), and **the passes** (*"Crew passes for the Crestbridge toll, twelve, in the names of licensed haulers"*). Rhosyn gives it up (`UL-D4.30`) or the player takes it (`UL-D4.40`); either way it becomes a carry-state object.

**Beat 4 — Out (`S04_out`).** *Objective: Carry the ledger out of the cellar.* Rhosyn says the stair is counted; the river door isn't. Both exits work. The stair exit with the ledger in hand starts E2 unless the crew is already down; the river door exit has only E3 (and none if the player came in that way and the leeches are already dispersed). Rhosyn follows the player out by whichever exit they take: once the book is gone she can't be found sitting beside the empty desk.

**Beat 5 — The dock steps (`S05_rhosyn`).** *Objective: Decide what happens to Rhosyn.* At the foot of the dock steps, in the dark, `UL-D5`. The choice (UL.8) must come before the deposit because one option changes the book.

**Beat 6 — The keepers (`S06_deposit`).** *Objective: Take the ledger to the keepers' river post.* Carry-deposit at G; the keeper logs it for Crest Hall (`UL-D6`). Sets `UL_LEDGER`.

**Beat 7 — Ottilie (`S07_close`).** *Objective: Tell Ottilie what you found.* `UL-D7`. If the player found her maker's dot, she says so and sets `UL_OTTILIE_TOLD`. Quest Completed.

### UL.4 Encounters

| Id | Enemies | Where | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | Smuggler pole-man (door-man) + Smuggler cutter | Stair alcove | Aggressive once force is chosen; leashed to the stair and back room | Pole-man plants the pole and leans back (~1.2 s), then a sweep that knocks the player back 2 m. Cutter drops a shoulder, blade low (~0.9 s), then two quick cuts. | Optional. 30–45 s. Player at 60–80% HP. |
| **E2** | Smuggler pole-man + 2 cutters (after MQ6: pole-man + 1 cutter) | Cellar market | Aggressive if force was used, if the player attacks in the cellar, or if the ledger goes up the stair with the crew standing | As E1. Racks are cover: a pole sweep that hits a rack stops short. | Optional. 45–75 s. Fair for Milestone 1 dependable equipment. |
| **E3** | 2 River Leeches, 1 River Skitter swarm | River tunnel water | Aggressive in the water volume only | Leech rears (~1.2 s) before latching; latch breaks on stepping onto the brick ledge or two hits. Skitters: ripple fan (~0.8 s). | Only if the grate is cranked outside the skiff window. Low threat by design. |

Downed crew stay down until the player leaves the building. Nothing they carry advances the quest.

### UL.5 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_hook` | Find out where Ottilie's glass is going. | `UL-D1` end node, **or** enter taproom volume A with quest available (bark `UL-B1`) | Yes | Quest Inactive → Active |
| `S01_way_in` | Get into the cellar under the Lamb. | Enter cellar-market volume D **with** any `UL_ENTRY_*` flag set | Yes | Flags set by route events (dialogue node, tunnel volume, E1 defeated) |
| `S01a_set_crate` | Set the glass on the racks. | Carry-deposit at rack volume | Errand only | Ottilie's crate stays on the racks |
| `S02_find_rhosyn` | Find the crew's book. | `UL-D4` reaches node `UL-D4.20` | Yes | |
| `S02b_dot` | (Optional) Look under the red wax. | Inspect on rack bowl | No | Sets `UL_DOT_FOUND` |
| `S03_read_ledger` | Read the ledger. | 3 inspect events on ledger pages, then `UL-D4.30` or `UL-D4.40` | Yes | Ledger becomes carry-state |
| `S04_out` | Carry the ledger out of the cellar. | Enter dock-steps volume while carrying ledger | Yes | Combat does not drop the ledger; logout returns it to Rhosyn's desk and resets to `S03` |
| `S05_rhosyn` | Decide what happens to Rhosyn. | `UL-D5` choice node resolved | Yes | |
| `S06_deposit` | Take the ledger to the keepers' river post. | Carry-deposit at keepers' post G, then `UL-D6` end | Yes | Sets `UL_LEDGER` |
| `S07_close` | Tell Ottilie what you found. | `UL-D7` end node | Yes | Quest → Completed |

### UL.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `UL_ENTRY_ERRAND` / `_PASS` / `_RIVER` / `_FORCE` | Route events | `UL-D4` opener variant, `UL-D7` variant |
| `UL_DOT_FOUND` | `S02b_dot` | `UL-D7` → `UL_OTTILIE_TOLD` |
| `UL_LEDGER_GIVEN` / `UL_LEDGER_TAKEN` | `UL-D4.30` / `UL-D4.40` | `UL-D5` opener |
| `UL_RHOSYN_WITNESS` / `UL_RHOSYN_FLED` / `UL_RHOSYN_STAYS` | `UL-D5` (exactly one) | MQ10 (presence at the hearing), MQ12 (Brookhollow variant), Brookhollow barks, `UL-D7` |
| `UL_LEDGER_CUT` | `UL_RHOSYN_STAYS` (torn chit and pass pages) | MQ10 (weaker chip) |
| `UL_LEDGER` | `S06_deposit` | MQ10 chip |
| `UL_OTTILIE_TOLD` | `UL-D7` with `UL_DOT_FOUND` | MQ7 |

### UL.7 Choices and consequences — Rhosyn

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **A. Witness** — *"Come to the keepers with me. Say what you wrote."* | She gives a statement at the river post and goes to Crestbridge under keeper protection. `UL_RHOSYN_WITNESS`. | Her work papers are seized as forgeries. The people on her pinned list lose their places; two dock barks change (a worker gone from the drying racks; ME02 has one fewer mark on the beam). | MQ10: she is present and attests the ledger hand; better terms. MQ12: she is clerking for the keepers, wry about it. |
| **B. Flee** — *"Go downriver tonight. Take your press."* | A dawn barge (role-based crew) takes her. `UL_RHOSYN_FLED`. | No witness: at MQ10 the keepers ask who wrote the book and nobody can say. Brookhollow loses the only person writing papers for displaced workers. The cellar closes for a season when the crew find her nook empty. | The ledger is a full chip, held in the keepers' box. Rhosyn is absent from MQ10 and MQ12. Ottilie's glass stops vanishing (barks). |
| **C. Stays** — *"Stay. Write for the workers. Not for them."* | Rhosyn tears out the chit and pass pages, the ones carrying her own careful hand, before the ledger goes to the keepers. `UL_RHOSYN_STAYS`, `UL_LEDGER_CUT`. Ottilie offers her a bench writing labels. | The player has kept a forger's secret, and Ottilie knows it. The ledger is weaker: the Board-sealed chits are gone, so the purse line is only the crew's word, and MQ10 cannot name which licensed haulers lent their names. The cellar stays open. | MQ10 chip still valid but weaker; she does not attend. Placed workers keep their places. In MQ12 she has a stall writing letters. |

No option is wrong. None of them makes Rhosyn safe and keeps her work going and leaves the book whole.

### UL.8 Rewards

| Reward | Type | Notes |
|---|---|---|
| MQ10 evidence chip | Story | `UL_LEDGER` |
| River door route | Access | Docks ↔ Lamb cellar shortcut stays open (unless option B closes the cellar for a season). |
| Cellar market | Access | Stays a visitable space. Whether anything is sold there is an economy-pass decision (dossier calls it a recurring chain hook). |
| Small payment | Currency | From Ottilie. Amount set in economy tuning. |
| Skill XP | Actions only | Melee, Cooking. No lump quest XP. |

### UL.9 Failure, recovery, co-op

| Situation | Handling |
|---|---|
| Death in the cellar | Respawn at Ottilie's yard. Downed crew stay down; step and flags kept; a carried ledger returns to Rhosyn's desk and `S03` re-completes on pickup (pages stay read). |
| Crate dropped | Returns to Ottilie's yard. |
| No food, no coin, no will to fight | Errand and river-door routes need neither. |
| Player fights everyone | Rhosyn still talks (`UL-D4` force variant). The choice is unchanged. |
| Co-op | Each player needs their own entry flag; a partner's fight downs shared crew for both. Rhosyn's choice is per player; a partner who chose differently sees their own outcome (her nook empty or occupied, per state). |

### UL.10 Integration needs

| Need | Minimum form | Fallback |
|---|---|---|
| Challenge volumes that open dialogue | Volume → dialogue start; dialogue options check carry-state and flags | — |
| Time-of-day window for the grate | Server time-of-day check on the tunnel volume (evening bell to midnight) | If time-of-day is not ready: the grate is always cranked (4 s) and E3 always spawns once |
| Carry-state that survives combat | Carry flag "light carry: not dropped on damage" | Ledger can be dropped; returns to the desk |
| Per-player cellar state | Rhosyn's nook occupied/empty by flag | Nook always empty after completion; state carried by barks |

### UL.11 Ledger, decisions, review

**Mystery ledger.** *What the ledger proves:* that a named crew was paid for "Lock work" on the wrong nights, that the pay was **drawn on the Provisioner's purse** and chitted under the **Board seal**, and that the crew moved on borrowed hauler names `[ANTAGONIST]`. It shows who paid; it does not show what the Board knew or why, which stays MQ10's work. *Wrong reading:* Rhosyn is the crew's brain. Her nook says otherwise.
**Contract (Director ruling, independent review pass).** The MQ10 chip is **the crew ledger** (`UL_LEDGER`), not "Rhosyn's forged papers". `UL_LEDGER_CUT` (torn chit and pass pages) is the weaker chip. Rhosyn's three outcomes are `UL_RHOSYN_WITNESS` (testifies; present), `UL_RHOSYN_FLED` (absent) and `UL_RHOSYN_STAYS` (in Brookhollow, not a witness), read by MQ10 and MQ12 as listed in §0.2. Antagonist swap: the purse line and the Board-seal text on the pay chits are tagged `[ANTAGONIST]`; bible §3.1's list of Board-seal documents should add the UL pay chits (open item for the bible owner).

| Review finding | Revision |
|---|---|
| First draft used a hide-in-shadow route. | Removed: no stealth system. Replaced with fixed challenge volumes and errand/pass/timing routes. |
| Option C first let Rhosyn stay at no cost. | She cuts her chit pages; the chip weakens and the player keeps a secret. |
| Sallow was quoted in the cellar. | He is absent; every mention is tagged `[ANTAGONIST]`. |
| Ledger as a quest item. | Carry-state object, deposited; flag-only chip. 0 quest items. |
| Independent review pass: UL and Act III's chip C8 disagreed (forged papers vs ledger; impossible Rhosyn states). | Director ruling applied: the ledger is the chip and shows who paid (Provisioner's purse, Board-sealed chits). Option C tears the pages. `UL_RHOSYN_GONE` renamed `UL_RHOSYN_FLED`; all three outcomes listed in §0.2 for MQ10/MQ12. |
| Independent review pass: no state for after MQ6 or MQ10. | Post-MQ6 variants (remnant crew, Rhosyn packing, smaller E2). Offer window closes when MQ10 starts; a late completion archives the ledger with no chip. |

### UL.12 Dialogue

**UL-B1 — Crew bark (taproom, quest available):** CREWMAN: *"Book says we're paid through the month. Book says. Ask her downstairs what the book says."* / [MQ6 Completed] CREWMAN: *"Half the crew's in keeper rope since the mill. Book still says we're owed."* → objective `S00_hook`.

```
UL-D1.01 OTTILIE: (holding a bowl to the window) "Not you. I'm talking to the bowl. It's got a seed in the glass."
UL-D1.02 OTTILIE: "Seconds go on the yard shelf. Flawed. Fit for hens. They keep walking off."
UL-D1.03 OTTILIE: "I found them under the Lamb with red wax on, priced as contraband. Contraband. My hen bowls."
UL-D1.04 OTTILIE: "I went down to buy them back. Man on the stair sent me up again. Didn't even let me haggle."
  > "What else did you see?"                       → UL-D1.10
  > "I'll get down there."                         → UL-D1.20
UL-D1.10 OTTILIE: "Heard them. River crew, arguing about pay. 'It's in the book.' Said like scripture."
UL-D1.11 OTTILIE: "Those are the ones off the Lock. Everyone knows. Nobody says."      → UL-D1 options
UL-D1.20 OTTILIE: "They buy from a carter on market day. I could pack a crate. You could be the carter."
UL-D1.21 OTTILIE: "Or go round by the river. There's an old door under the docks. Ask anyone over fifty."
      {event: UL-D1 end → S00_hook; errand crate becomes available in Ottilie's yard}
```

```
UL-D2.01 DOOR-MAN: (doesn't stand) "Cellar's private."
  > [carrying Ottilie's crate] "Market-day glass."                → UL-D2.10
  > [crew pass] (Show the pass.)                                   → UL-D2.20
  > "I'm going down."                                              → UL-D2.30
  > "Wrong door."                                                  → end
UL-D2.10 DOOR-MAN: "Carter's got thinner." (beat) "Racks on the left. Don't touch the steel."   {set UL_ENTRY_ERRAND}
UL-D2.20 DOOR-MAN: (holds it to the candle) "That's one of hers. Good one, too. Go on."        {set UL_ENTRY_PASS}
UL-D2.30 DOOR-MAN: (stands, pole in hand) "No, you're not."
  > "Yes, I am."                                                   → end {start E1}
  > "Fine."                                                        → end
```

```
UL-D3.01 CREWMAN: "If you're selling, I'm not buying. If you're buying, I'm selling."
  > "What are you selling?"                     → UL-D3.10
  > "You look hungry."                          → UL-D3.20
UL-D3.10 CREWMAN: "My pass for the cellar. Can't eat a pass. Can't drink it either, I've tried."
  > [carrying cooked food] "Trade for this."     → UL-D3.30 {take cooked food}
  > "For coin, then."                            → UL-D3.30 {small payment}
  > "Keep it."                                   → end
UL-D3.20 CREWMAN: "No pay since the Lock went quiet. Book says we're owed. Book doesn't cook."  → UL-D3.10
UL-D3.30 CREWMAN: "Show it to the stair. Don't tell her where you got it. She'll know anyway."   {give crew pass (carry-state token); set UL_PASS_HELD}  → end
```

```
UL-D4.00 [MQ6 Completed] RHOSYN: (packing inks into a crate) "Half of them are in keeper rope. I'm between lives. Be quick."   → UL-D4.01
UL-D4.01 [UL_ENTRY_FORCE] RHOSYN: (pen still moving) "That was loud. I'd have let you in for a smile."
UL-D4.01 [UL_ENTRY_PASS]  RHOSYN: "That's Fitch's pass. I wrote Fitch's pass. You're not Fitch."
UL-D4.01 [UL_ENTRY_RIVER] RHOSYN: (not turning) "Nobody uses the river door but me. Come in, then. Wipe your feet."
UL-D4.01 [else]           RHOSYN: "The glass came early. And it's carrying itself. How modern."
UL-D4.02 RHOSYN: "Rhosyn. I write things. Passes, references, a love letter once. It went badly."
  > "What's that book?"                                    → UL-D4.20
  > "You wrote the crew's passes."                         → UL-D4.10
  > "Who are the names on your wall?"                      → UL-D4.15
UL-D4.10 RHOSYN: "Twelve of them. Hauler names, borrowed for the bridge toll. They pay well." (beat) "Somebody has to."   → UL-D4 options
UL-D4.15 RHOSYN: "People the flood put out. Docks want a household reference. I give them one. They're good at the work."
UL-D4.16 RHOSYN: "The crew's money pays for the ink. That's the whole of my philosophy."   → UL-D4 options
UL-D4.20 RHOSYN: "The book. I keep it because I'm the only one down here who can spell 'received'."
UL-D4.21 RHOSYN: "Read it if you like. You will anyway."   {event: S02_find_rhosyn; ledger pages inspectable}
  > [3 pages read] "I'm taking it."                        → UL-D4.40
  > [3 pages read] "Give it to me. You want out."          → UL-D4.30
UL-D4.30 RHOSYN: (closes it, holds it a moment) "I want out of the part where he comes back and asks for it." [ANTAGONIST]
UL-D4.31 RHOSYN: "Take the river door. They count heads on the stair. They don't count rats."   {give ledger (carry-state); set UL_LEDGER_GIVEN}  → end
UL-D4.40 RHOSYN: "Then I'm the woman who lost the book." (stands, takes her blanket) "Not staying to explain that."
UL-D4.41 RHOSYN: "River door. I'll be right behind you. Don't make it a race."   {give ledger (carry-state); set UL_LEDGER_TAKEN}  → end
```

```
UL-D5.01 RHOSYN: (at the dock steps; the Lamb's lamp behind her) "So. Here's the part where I'm a problem."
UL-D5.02 [UL_LEDGER_TAKEN] RHOSYN: "You took it. Fine. I'd have taken it too."
UL-D5.03 RHOSYN: "If I'm in Brookhollow when they find the shelf empty, I'm in the river by morning."
  > "Come to the keepers with me. Say what you wrote."            → UL-D5.10
  > "Go downriver tonight. Take your press."                      → UL-D5.20
  > "Stay. Write for the workers. Not for them."                  → UL-D5.30
UL-D5.10 RHOSYN: "Keepers will take my papers along with me. Every name on that wall loses their place."
UL-D5.11 RHOSYN: (long breath) "All right. I'll say it in a nice clear hand."   {set UL_RHOSYN_WITNESS}  {event: S05_rhosyn}
UL-D5.20 RHOSYN: "There's a grain barge at first light. They never ask what they're carrying. I'm very light."
UL-D5.21 RHOSYN: "Nobody will be able to say who wrote your book. I hope it's enough without me."   {set UL_RHOSYN_FLED}  {event: S05_rhosyn}
UL-D5.30 RHOSYN: "Then I'll need those pages back. The chits. They're my hand, every stroke."
UL-D5.31 RHOSYN: (tears them out along the stitching, quickly) "Your book's thinner. My neck's thicker. Don't tell anyone which."   {set UL_RHOSYN_STAYS, UL_LEDGER_CUT}  {event: S05_rhosyn}
```

```
UL-D6.01 KEEPER: (river post, lamp lit) "We're shut. Unless that's a book I've been hoping someone would bring me."
UL-D6.02 KEEPER: (reads two pages; reads them again) "Lock work. Paid in full." [ANTAGONIST]
UL-D6.03 [UL_LEDGER_CUT] KEEPER: "Pages torn out at the back. 'Drawn on the Provisioner's purse', and nothing pinned to prove it." (looks at the player) "I'll write 'as found'." [ANTAGONIST]
UL-D6.03 [else] KEEPER: (turns to the back; stops) "That's a Board seal. On a crew's pay chit." (closes the book carefully) [ANTAGONIST]
UL-D6.04 KEEPER: "This goes to Crest Hall with the morning rider. In a box. With a lock on it."   {set UL_LEDGER}  {event: S06_deposit}
UL-D6.05 [MQ10 hearing already held] KEEPER: "Hearing's been and gone. It goes in the archive, then. Late's still written down."   {set UL_LEDGER; no MQ10 chip}  {event: S06_deposit}
```

```
UL-D7.01 OTTILIE: "Well? Did you bring my hens' bowls back?"
UL-D7.02 [UL_ENTRY_ERRAND] OTTILIE: "You left a whole crate of mine down there. I'll put it on your account."
  > [UL_DOT_FOUND] "Your mark's under the wax."            → UL-D7.10
  > "The book's with the keepers."                         → UL-D7.20
UL-D7.10 OTTILIE: "My dot. Under their wax." (to the bowl in her hand) "You hear that? Smuggled. You're worth more than I thought."
UL-D7.11 OTTILIE: "When someone wants a proper bowl from me, I'll have it ready. No waiting."   {set UL_OTTILIE_TOLD}  → UL-D7.20
UL-D7.20 [UL_RHOSYN_STAYS] OTTILIE: "And the forger's on my bench writing labels. Lovely hand. Don't look at me like that."
UL-D7.20 [UL_RHOSYN_WITNESS] OTTILIE: "Half the drying racks are short a pair of hands this morning. I suppose that's justice."
UL-D7.20 [UL_RHOSYN_FLED] OTTILIE: "Cellar's dark. No wax on anything. I'll miss being outraged."
UL-D7.21 OTTILIE: (pays) "For the trouble. Not for the glass. The glass was mine."   {event: S07_close → quest Completed}
```

**Ledger inspect texts:** *The Lock line:* "'Lock work. G.S. Paid in full.' Four nights running. The same five names every time." / [MQ3 Completed] "The nights are the wrong nights in Ansel's book." `[ANTAGONIST]` *The purse:* "'Drawn on the Provisioner's purse.' Pay chits pinned behind it, each stamped with the Provision Board's seal and signed 'received'." `[ANTAGONIST]` *The passes:* "'Crew passes, Crestbridge toll: twelve.' Each beside a licensed hauler's name and a sum." *Rack bowl (under wax):* "Under the red wax, a tiny raised dot in the glass. Ottilie's mark." *Bowls on the rack:* "A bead of water in every bowl. Every bead the same height, though the shelf leans."

---

## NB — Night Bridge

### NB.1 Summary card

| Field | Value |
|---|---|
| Suggested content id | `lowmark.side.night_bridge` |
| Type | Settlement story, Crestbridge (bible §7; lattice L-S10 *Bridge Courtesy*, M01 *Repair faces*) |
| Unlock | MQ2 Completed. Offered at dusk at the south toll, where a crowd is held up (enter volume). |
| Length | 25–30 minutes |
| Combat share | ~25% (Reed Stalkers in the piers) |
| Skills | Melee; agility triggers (with fallback) |
| Choice | Whose repair is written in the toll book (3 options) |
| Outputs | `NB_UNDERSIDE_OPEN` (route), `NB_BOTH_CREDIT` / `NB_ALL_PAY` / `NB_WICKETT_CREDIT` |
| Canon used | Crestbridge: stone bridge reinforced by dwarven engineers, toll posts, Crest Hall (dossier §IV.4, §V.2); dwarven fortification of mills and bridges in the war (§II); Reed Stalkers (§VIII); Aldric Fenmere's reserved, fair manner and the House's wartime supply compacts ([CANON ANCHOR]). |
| New | Orla Wickett, Tam Varley, the south toll keeper, the bridge crew's winch-hand, the three repair faces, the hanging platform. |

**One paragraph.** For three generations the Wickett household has crossed Crestbridge's south toll free "by courtesy", because Orla Wickett's grandmother's people "paid for the bridge". Tam Varley, master of a caravan for a far-road employer, says his employer's house paid for it and his carts deserve the same. Since the grain shortages, Keeper-Captain Hesketh has ordered every toll collected, and a young toll keeper is now charging both, which has stranded the guests for the Wicketts' naming feast on the wrong side of their own bridge. Everyone says the proof is "cut under the span". At night, with a lantern held low, the player climbs down among Reed Stalker nests in the piers and reads three repair faces: a wartime dwarven face stencilled for supply, which no household paid for; a rough postwar patch with the Wickett mark; and iron cramps with Varley's employer's carter-mark. Both families mended something. Neither paid for the bridge. Aldric Fenmere comes down from the Hall to see who is blocking a naming feast and reads the cloth himself.

**Remember:** the ceiling of marks under the second arch, generations of crew hands lit sideways by one lantern. **Want next:** the underside route, which ends near Crest Hall's water-gate.

### NB.2 The place: Crestbridge underside (P02)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. South toll and waiting wall** | Hook and finale | Feast guests in their good coats on the south end; Varley's three carts behind them. The waiting wall is worn smooth at child height. The toll table has a tally book, a lamp and an inkpot nobody has knocked over yet. |
| **B. Crew stair and winch** | Way down | A maintenance stair under the south abutment. Above it, the bridge crew's winch and a hanging platform on a rail beneath the span. Crew chalk marks on the stones: arrows, "LOOSE", a drawn frog with a line through it. |
| **C. Pier 1 cutwater ledge** | First traversal | A narrow ledge on the cutwater. River loud below. Fishing line snagged on a cramp: somebody comes down here. |
| **D. Pier 2: the war face** | Face 1; E1 | A reed island has built up around the pier footing. The repair stones above it are cut deep and square, every course with the same small hammer-and-square mark. A faded stencil: SUPPLY — CRESTBRIDGE — and a number. |
| **E. Arch 2 soffit: the patch and the ceiling** | Face 2; wonder | Rough grey mortar packed into a split, hand-smoothed, with a wicket-gate mark and a season scratched beside it: *THAW AFTER PEACE*. All around it on the underside of the arch: hundreds of crew marks, initials, tally strokes, a boat, a hand traced round. In one corner, many short strokes in rows of five, the kind people make counting days. |
| **F. Pier 3: the cramps** | Face 3; E2 nest | Iron cramps let into the stone after a flood, each stamped with a carter-mark (a wheel with a bar). A tally of payments cut beside them. A Reed Stalker nest of woven reed mats wedged between pier and cramp. |
| **G. North stair** | Exit; future route | A crew stair up to the north end, close by the Crest Hall water-gate wall (MAP VERIFICATION REQUIRED). |

**Traversal.** Agility triggers: step-down B→C, gap hop C→D, cramp-ladder climb D→E, beam walk E→F, step-up F→G (Phase 1.3 §1). **Walkable fallback:** the winch-hand lowers the **hanging platform** (`NB-D2`). It rides a rail under the span and stops at D, E and F (each move is a 6-second ride, a "watch" interaction). Every face can be read from the platform. The platform gets its own danger (E3) so the fallback is not a free pass.

**Raking light.** Each face looks flat in ordinary light. Holding the lantern low across it (3 s channel, `rake_light`) brings the cuts up in shadow; a second channel (`take_rubbing`, 3 s) adds the face to the **rubbing cloth**, a carry-state object marked "light carry" (does not block traversal or combat). Without the bridge crew's lantern the player's own light works the same.

**Moment of wonder (E).** Raking the lantern across the soffit to find the patch lights the whole ceiling of marks at once, sideways, for as long as the player holds it. There is no text beyond the inspect. **Unease:** under the arch, footsteps on the deck above carry down clearly. One set walks to the waiting wall and stops, and does not walk away again while the player is there. When the player climbs up, there is nobody at the wall. (Acoustic only; no figure, no evidence.)

### NB.3 Player-facing sequence

**Beat 0 — A feast on the wrong side (`S00_hook`).** *Objective: Find out why the south toll is blocked.* `NB-D1` at the toll: Orla, Varley, the keeper. Everyone agrees on one thing: "It's cut under the span."
**Beat 1 — Down (`S01_get_down`).** *Objective: Get under the bridge.* The winch-hand (`NB-D2`) lends a crew lantern and a rubbing cloth and offers the platform. Completes on entering the underside volume by either route.
**Beat 2 — The war face (`S02_war_face`).** *Objective: Read the repair on the second pier.* E1 at the reed island, then rake and rub.
**Beat 3 — The patch (`S03_patch_face`).** *Objective: Read the repair under the second arch.* Climb or ride to the soffit. Rake and rub. The wonder moment.
**Beat 4 — The cramps (`S04_cramp_face`).** *Objective: Read the repair on the third pier.* E2: the nest keeps waking stalkers until cut (`cut_nest`, 3 s channel, any blade). Rake and rub.
**Beat 5 — Up (`S05_up`).** *Objective: Bring the rubbing to the toll.* Exit by the north stair (G) and walk the deck back, or return the way the player came.
**Beat 6 — The cloth on the table (`S06_lay_cloth`).** *Objective: Show the toll what's under it.* Carry-deposit on the toll table; `NB-D3`. Aldric arrives mid-conversation. The choice.
**Beat 7 — The steward (`S07_aldric`).** *Objective: Speak with the steward.* `NB-D4`. Quest Completed. The feast crosses. The winch-hand leaves the platform rigged and chalks the ledges: `NB_UNDERSIDE_OPEN`.

### NB.4 Encounters

| Id | Enemies | Where | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 1 Reed Stalker (stalker), 1 Reed Stalker (lurker) | Pier 2 reed island | Stalker: ambush, Aggressive within the reeds, leashed to the island. Lurker: Defensive in the water at the island's edge. | **Long first-appearance telegraphs.** Stalker: reeds part in a straight line toward the player (~1.6 s), then a leap. Throat swells with a gurgle (~1.4 s) before a tongue-lash that pulls the player 3 m toward the water; stepping onto the stone footing breaks it. Lurker: ring of bubbles at the edge (~2.0 s), then a surfacing grab. | Required. 40–55 s. Player at 60–80% HP. |
| **E2** | 1 stalker + nest | Pier 3 | The nest wakes **one** more stalker after 30 s if `cut_nest` is not complete (at most 1 extra, never more than 2 stalkers at once). | As E1. The nest pulses (mats shiver) 3 s before a stalker drops out. | Required. 45–70 s. Cutting the nest early is the readable answer. |
| **E3** | 2 stalkers, one at a time | Platform (fallback route only) | Climb onto the platform at the pier 2→3 ride; the second climbs only after the first is down | Wet hands on the platform rail (~2.0 s) before each climbs on | Only on the fallback route. 30–45 s. |

**Cap:** no NB encounter ever has more than **2 Reed Stalkers active at once**, and all NB stalker telegraphs are longer than the family's standard.

**Family note:** bible §10 lists Reed Stalkers as first seen in MQ5. NB unlocks after MQ2, so **NB is the Reed Stalkers' first appearance** for any player who takes it before MQ5; the counts and telegraphs above are tuned for that. FW now unlocks after MQ5 and is not a first appearance. Flagged to the Encounters package and to the bible §10 owner.

### NB.5 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Find out why the south toll is blocked. | `NB-D1` end node | Yes |
| `S01_get_down` | Get under the bridge. | Enter underside volume C (ledges) or platform volume (fallback) | Yes |
| `S02_war_face` | Read the repair on the second pier. | E1 defeated; `rake_light` then `take_rubbing` at D | Yes |
| `S03_patch_face` | Read the repair under the second arch. | `rake_light` then `take_rubbing` at E | Yes |
| `S04_cramp_face` | Read the repair on the third pier. | `cut_nest` complete; `rake_light` then `take_rubbing` at F | Yes |
| `S05_up` | Bring the rubbing to the toll. | Enter toll volume A carrying the rubbing cloth | Yes |
| `S06_lay_cloth` | Show the toll what's under it. | Carry-deposit on the toll table; `NB-D3` choice resolved | Yes |
| `S07_aldric` | Speak with the steward. | `NB-D4` end node | Yes (→ Completed; sets `NB_UNDERSIDE_OPEN`) |

Faces may be read in any order once the player is underneath (S02–S04 run in parallel). If the rubbing cloth is lost (logout), the winch-hand has another and the faces already rubbed stay rubbed (flags `NB_FACE_WAR`, `NB_FACE_PATCH`, `NB_FACE_CRAMP`).

### NB.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `NB_FACE_WAR` / `NB_FACE_PATCH` / `NB_FACE_CRAMP` | Rubbing channels | `NB-D3` options, cloth inspect |
| `NB_PLATFORM_USED` | Fallback route | Winch-hand bark |
| `NB_BOTH_CREDIT` / `NB_ALL_PAY` / `NB_WICKETT_CREDIT` | `NB-D3` (exactly one) | Toll barks, Orla/Varley post-quest lines |
| `NB_UNDERSIDE_OPEN` | Completion | World route; MQ10 optional approach (request) |

### NB.7 Choices and consequences

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Both credited** — *"They each mended something. Write both down, by the stone."* | The keeper writes two repair credits, not courtesies: the Wicketts for the arch, Varley's employer for the cramps. Both pass free tonight. | The toll's take is short and the keeper must explain it to Crest Hall against Hesketh's order. | Toll barks grumble about "credits". Orla and Varley share a bench at the feast, not happily. |
| **All pay** — *"Nobody here paid for the bridge. Everyone pays, and the toll pays the next repair."* | The keeper takes toll from all. A line is added: "toll toward repair". | Orla pays at her own feast, and three generations of courtesy end on her bridge. | Fairest to the bridge. Orla is civil to the player and no warmer. Varley is pleased in a way that annoys everyone. |
| **Wicketts only** — *"The Wicketts patched it when nobody else would."* | Orla's courtesy is written down for the first time. Varley's carts pay. | Varley's employer docks his wages for the toll; he takes the far road next season (barks). | The feud cools rather than ends. Orla gives the player a seat at the feast. |

All three options keep the bridge a shared duty, and none of them turns it into a political plot (lattice L-S10 boundary).

### NB.8 Rewards

| Reward | Type | Notes |
|---|---|---|
| **The underside route** | Access | Ledges chalked and the platform rigged, south abutment ↔ north stair near the water-gate. |
| Repair-face reading | Knowledge | Raked-light inspect works on other repair faces in Lowmark (M01) with one line each. Location list belongs to the Zones package. |
| Feast food (Wicketts only / both credited) | Small gift | One cooked food item from the item pass. |
| Skill XP | Actions only | Melee. |

### NB.9 Failure, recovery, co-op

Death underneath respawns the player at the crew stair (B), with faces already rubbed kept. The platform cannot strand the player: the winch-hand returns it to B if it is left at a stop for 60 s. The quest cannot fail. In co-op each player needs their own rubbings. Stalkers are shared and the nest is cut once for both. The platform carries both players.

### NB.10 Integration needs

| Need | Minimum form | Fallback |
|---|---|---|
| Agility triggers (5) | Phase 1.3 trigger boxes | Platform route (always available) |
| Moving platform on a rail | Interaction-driven position states (B, D, E, F) with a timed ride | If moving platforms are not ready, the platform becomes three fixed crew scaffolds reached by ladders from the south bank; each ladder is a walkable stair prop. |
| Rake-light presentation | Client-side decal or normal-map reveal while the channel runs | Inspect text alone carries the faces. |
| Toll-table deposit | Carry-deposit volume | — |

### NB.11 Ledger, decisions, review

**Mystery ledger.** *Who paid for the bridge:* the war effort did, through dwarven engineers (canon); the Wicketts patched war damage after the peace; Varley's employer paid for flood cramps later. *Public belief:* one family paid for all of it. *Wrong reading:* the Fenmere compacts paid, as Aldric assumes. The stencil says supply, and no house.
**Open decision:** none. Aldric's line about the compacts avoids stating what his ledgers contain (canon: he keeps them and won't destroy them).

| Review finding | Revision |
|---|---|
| First draft had Aldric settle the feud. | He reads, asks one question and lets the player's account stand. He convenes; he does not rule. |
| Fallback route had no danger. | E3 on the platform. |
| The arch tally strokes risked implying named dead. | Strokes only, unattributed, no names in any inspect. |
| Independent review pass: E2 could field five stalkers on a ledge at night, the hardest fight of Act I for many players. | Director ruling: max 2 stalkers at once, longer telegraphs, nest wakes at most one extra after 30 s; noted as the family's first appearance. |

### NB.12 Dialogue

```
NB-D1.01 KEEPER: "Toll is toll. Keeper-Captain's order. Every cart, every foot, since the shortages."
NB-D1.02 ORLA: "My family has crossed free since before your mother had teeth. We paid for this bridge."
NB-D1.03 VARLEY: "And I'm told by my employer, every season, that his house paid for it. So I'll cross free too."
NB-D1.04 ORLA: "Your employer couldn't pay for a bucket."
NB-D1.05 KEEPER: (to the player, quietly) "There's a naming feast on the far side and the baby's already there. Without the guests."
  > "Who paid for the bridge, then?"                       → NB-D1.10
  > "Why not just let the feast through?"                  → NB-D1.20
NB-D1.10 ORLA: "It's cut under the span. Any fool can see it."
NB-D1.11 VARLEY: "Then any fool can go and look. Not me. Things live down there."   → NB-D1.30
NB-D1.20 KEEPER: "Because then it's a courtesy, and courtesy isn't on my sheet, and I'd be the keeper who let it be."  → NB-D1.30
NB-D1.30 KEEPER: "The bridge crew's winch-hand is under the south end. If it's cut there, bring me something I can write down."
      {event: S00_hook}
```

```
NB-D2.01 WINCH-HAND: "Going under? At night? Good. You can see the cuts at night. Daylight flattens them."
NB-D2.02 WINCH-HAND: "Lantern. Hold it low, across the stone, not at it. And a cloth for rubbings."   {give crew lantern, rubbing cloth (carry-state)}
NB-D2.03 WINCH-HAND: "Mind the reed islands round the piers. Stalkers. They've nested. We stopped going down."
  > "I'll take the ledges."                                → end {S01 via ledges}
  > "Can you lower me?"                                    → NB-D2.10
NB-D2.10 WINCH-HAND: "Platform rides the rail. Slow. Stalkers climb, mind. They like a slow thing."   {set NB_PLATFORM_USED}  → end
```

**Underside barks (player alone; inner-voice inspect lines):** pier 2: *"Deep, square cuts. Every course the same small mark: a hammer and a square."* / stencil: *"SUPPLY — CRESTBRIDGE. A number. No name of any house."* / patch: *"Rough mortar, pressed in by hand. A wicket-gate mark and 'THAW AFTER PEACE'."* / cramps: *"Iron cramps, each stamped with a wheel and a bar. Payments tallied beside them."* / ceiling: *"Marks. Hundreds of them. Initials, a boat, a hand traced round its own fingers. Rows of short strokes in fives."*

```
NB-D3.01 KEEPER: (spreads the cloth under the lamp) "Right. Show me."
  > [NB_FACE_WAR] "The second pier. Dwarven work, stencilled for supply. Nobody's family paid for that."   → NB-D3.10
  > [NB_FACE_PATCH] "Under the arch. A patch with the wicket mark. After the peace."                       → NB-D3.20
  > [NB_FACE_CRAMP] "Third pier. Iron cramps with a carter's wheel on them."                               → NB-D3.30
  > [all three seen] "So."                                                                                → NB-D3.40
NB-D3.10 VARLEY: "Supply. So it was the war's."
NB-D3.11 ORLA: "The war did a lot of things. Then it left."   → NB-D3 options
NB-D3.20 ORLA: (touches the rubbing) "My gran's mark. She did that with her hands. The crews wouldn't come."   → NB-D3 options
NB-D3.30 VARLEY: (quietly) "That's ours. The wheel." (beat) "I thought he was lying. He always says he paid for things."   → NB-D3 options
NB-D3.40 ALDRIC: (arriving down the deck, unhurried) "I'm told someone has stopped a naming feast at my bridge."
NB-D3.41 ALDRIC: (looks at the cloth for some time) "The war works will be in the House compacts, surely."
NB-D3.42 KEEPER: "It says supply, Steward. Not Fenmere."
NB-D3.43 ALDRIC: "...So it does." (to the player) "You went under. What should the keeper write?"
  > "They each mended something. Write both down, by the stone."                       → NB-D3.50
  > "Nobody here paid for the bridge. Everyone pays, and the toll pays the next repair."   → NB-D3.60
  > "The Wicketts patched it when nobody else would."                                  → NB-D3.70
NB-D3.50 KEEPER: "Repair credit, Wickett, second arch. Repair credit, the wheel, third pier." (writes) "Hesketh will hate it."
NB-D3.51 ORLA: (to Varley) "You can sit at the end. Far end."   {set NB_BOTH_CREDIT}  → NB-D4.01
NB-D3.60 ORLA: "Three generations." (pays, slowly, coin by coin) "Fine. Fine. Mend it properly next time."
NB-D3.61 VARLEY: "Fair's fair."
NB-D3.62 ORLA: "Don't."   {set NB_ALL_PAY}  → NB-D4.01
NB-D3.70 KEEPER: "Courtesy, Wickett household, for the arch. First time it's ever been written." 
NB-D3.71 VARLEY: (counting coin) "He'll take it out of my wages. He takes everything out of my wages."   {set NB_WICKETT_CREDIT}  → NB-D4.01
```

```
NB-D4.01 ALDRIC: "Thank you. I'd have assumed. That is a habit of my house."
  > "Do you know who made the marks under the arch?"        → NB-D4.10
  > "Will Hesketh overrule it?"                              → NB-D4.20
  > "Good night, Steward."                                   → NB-D4.30
NB-D4.10 ALDRIC: "Crews. Generations of them. Nobody writes down who goes under a bridge." (beat) "Perhaps someone should."   → NB-D4 options
NB-D4.20 ALDRIC: "The Keeper-Captain is very tired. I'll speak to him." (beat) "Gently."   → NB-D4 options
NB-D4.30 ALDRIC: "Go and eat something at that feast. You've earned the bread, at least."
      {event: S07_aldric → quest Completed; set NB_UNDERSIDE_OPEN}
```

**Post-quest:** WINCH-HAND: *"Left the platform rigged and chalked the ledges. Goes right under to the north stair. Mind the frogs."* / ORLA [`NB_ALL_PAY`]: *"I pay my toll. Every time. Loudly."*

---

## UR — Unreplanted

### UR.1 Summary card

| Field | Value |
|---|---|
| Suggested content id | `lowmark.side.unreplanted` |
| Type | Settlement story, Ashenstead (bible §7; lattice L-S08) |
| Unlock | MQ3 Completed. Offered on entering the plot-edge volume while Tansy Marl and the row-warden argue. Best before MQ5; playable after. |
| Length | 20–30 minutes |
| Combat share | ~30% (Field Goblins: the nest, then its returning raiders) |
| Skills | Woodcutting (scrub clearing, entry level), Melee |
| Choice | **Joric's**, not the player's. The player decides what to offer; Joric decides what the ground becomes (3 outcomes). |
| Outputs | `UR_GATE_RUN` / `UR_LINE_STAKED` / `UR_LEFT` (read by MQ5) |
| Canon used | Joric Fen: field labourer and net-mender on the Ashen Flats; his land burned in the war and was never replanted; soft-spoken, never complains, avoids standing water; lost family in a river incident that was never recorded; says the water "gives things back slowly" ([CANON ANCHOR]). Ashen Flats: scorched rye, charred fence posts "like black teeth" (dossier §IV.3). Field Goblins nesting in old pits with broken farm tools (§VIII). |
| New | Tansy Marl, the row-warden, the buried field gate, the goblin nest in the plot, the raiders' threshing floor. |

**Canon guard (binding for this package).** Joric receives no age, service, kin names, number of dead, or account of the incident. Other people may say only what canon allows: he lost people; it was a river incident; nobody wrote it down. Nothing in the plot (no object, imprint or inspect) refers to his family. The plot is grief's ground because he says so by not planting it, not because the game shows why.

**One paragraph.** Joric Fen's plot on the edge of the Flats has stood unplanted since the war. The row-warden of the Rebirth Fields wants it folded into communal work. Tansy Marl, whose house has been full since the far-bank shortages, wants ground of her own and says something is stealing her seed. Joric mends nets on the plot edge and says nothing. The player clears the scrub and finds a Field Goblin nest under a fallen barn wall (Tansy's seed basket inside it); the nest's raiders come back across the burned barns' threshing floor with a fresh haul, and the player drives them off. With the vermin gone, the ash comes off a low corner where rainwater always stands. Under it is a buried field gate: a timber-and-iron paddle at the head of a dead ditch, its post cut with the plot's old boundary. The player can offer Joric three things: the gate turns, so the standing water could run; the post shows where his line ends; or nothing at all. Joric decides.

**Remember:** Joric turning the paddle himself, or Joric not turning it. **Want next:** what happens to this ground when the fields start flooding from below (MQ5).

### UR.2 The place: Joric's plot (beside P20)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Net bench** | Joric's place | An upturned crate and a net over a charred post. He sits with his back to the plot's low corner. Mended knots in the net are neat; one row is a beginner's, re-tied over. |
| **B. Scrub** | Woodcutting | Burned scrub and driftroot suckers grown head-high. Three clumps block the plot's back. |
| **C. Fence line** | Read the plot | Charred posts like black teeth, a gap where a gate once hung. Wire rusted to lace. |
| **D. Goblin nest** | E1 | Under a fallen wall of the burned barn row next door (P20): a burrow lined with broken rakes, a cart-wheel rim, a child's tin cup, and a woven seed basket with Marl's knot on the handle. |
| **E. Threshing floor** | E2 | The open threshing floor of the burned barn row next door (P20): split seed sacks, drag marks in the ash running toward the plot, a lookout's perch on a fallen beam. Across the Flats, in sight but not entered, is the trench culvert where MQ3's Ash Hounds denned; UR does not use it. |
| **F. The low corner** | Unease | Rainwater stands here after every shower. It lies dead-flat even when the wind moves the scrub around it. Joric does not look at it. |
| **G. The field gate** | Discovery | At the low corner's lip, under a hand of ash and silt: a timber paddle in an iron frame at the head of a dry ditch. The gatepost is cut with a row of notches and a holding mark. Beyond the paddle the old ditch runs, silted, toward the communal headland. |

**Moment of unease (F):** the standing water. Inspect: *"Wind on the scrub. Not a ripple on the water."* **Moment of wonder (completion):** on the player's next return after `S07` (fallback: at completion), the cleared furrows show a thin green haze of scorched rye, self-sown from seed that sat in the ash since the burning. Joric's line about it is the quest's last.

### UR.3 Player-facing sequence

**Beat 0 — Whose ground (`S00_hook`).** *Objective: Find out what's wrong with the unplanted plot.* `UR-D1`: the row-warden and Tansy argue; Joric mends. If asked, Joric says one thing: "Ask what's eating the seed."
**Beat 1 — Clear it (`S01_clear`).** *Objective: Clear the scrub from the back of the plot.* Three Woodcutting gather interactions (scrub clumps; entry level). The row-warden lends a crew hatchet if the player has no blade (kept on completion). Clearing the third clump shows the burrow mouth.
**Beat 2 — The nest (`S02_nest`).** *Objective: Deal with whatever is in the burrow.* E1. Then inspect the nest. Optional `S02b_basket`: carry Tansy's seed basket (carry-state) to her (`UR-D2`).
**Beat 3 — The raiders (`S03_raiders`).** *Objective: Drive the raiders off the threshing floor.* After the nest is cleared, a goblin raiding party comes back across the burned barns with seed. E2 starts when the player enters the threshing-floor volume. Callback barks (`UR-B3`) read `WC_BARNS_CLEARED` and `HW_DEN_CLEARED`.
**Beat 4 — Under the ash (`S04_gate`).** *Objective: Find out why the corner floods.* With the raiders gone, the row-warden notices the low corner never drains and hands over a spade. Three dig points (3 s channel each) at the corner's lip expose the paddle; inspect the gatepost (the boundary). If `LM_FIELD_FIX = plot` (MQ5 done first), the new relief ditch has already cut the gate half-free and there is one dig point, not three.
**Beat 5 — Tell him (`S05_joric`).** *Objective: Tell Joric what's under the ash.* `UR-D5`.
**Beat 6 — His ground (`S06_decision`).** *Objective: Hear what Joric decides.* `UR-D6`. The player offers; Joric answers. If he chooses the gate, he walks to the corner and turns the paddle himself (NPC action, ~6 s, under player camera). The standing water shivers for the first time, then runs off down the old ditch.
**Beat 7 — Neighbours (`S07_close`).** *Objective: Let the neighbours know.* `UR-D7` with Tansy and the row-warden. Quest Completed.

### UR.4 Encounters

| Id | Enemies | Where | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 3 Field Goblin scrappers, 1 trapper | Burrow mouth and nest | Scrappers Aggressive within the plot; trapper Defensive, keeps two scrappers between itself and the player | Scrapper raises a broken tool overhead (~1.0 s), then an overhand blow. Trapper sets rake-tine traps in the ash: a glint and a small mound appear (~2 s to arm); stepping on one roots the player 2 s with a small hit. Traps stay visible. | Required. 45–60 s. Player at 55–75% HP. |
| **E2** | 2 Field Goblin scrappers, 1 Field Goblin hauler | Threshing floor (P20) | Scrappers Aggressive, screen the hauler. Hauler carries a seed sack along the drag marks toward the nest hole; if it reaches the hole it drops the sack in and turns to fight (no flee at low HP). | Hauler hunches and sets off (~1.0 s) along the visible drag marks; a hit makes it drop the sack. Scrappers: broken tool raised overhead (~1.0 s), then an overhand blow. No traps in this fight. | Required. 40–60 s. Fair for Novice-to-Milestone-1 equipment. |

Goblin loot is ordinary. The seed basket is a world object in the nest, not a drop.

### UR.5 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Find out what's wrong with the unplanted plot. | `UR-D1` end node | Yes |
| `S01_clear` | Clear the scrub from the back of the plot. | 3 scrub-clump gather events | Yes |
| `S02_nest` | Deal with whatever is in the burrow. | E1 defeated + inspect nest | Yes |
| `S02b_basket` | (Optional) Return the seed basket. | Carry-deposit to Tansy; `UR-D2` end | No |
| `S03_raiders` | Drive the raiders off the threshing floor. | E2 defeated | Yes |
| `S04_gate` | Find out why the corner floods. | 3 (or 1) `dig_ash` interactions + inspect gatepost | Yes |
| `S05_joric` | Tell Joric what's under the ash. | `UR-D5` end node | Yes |
| `S06_decision` | Hear what Joric decides. | `UR-D6` resolution node (sets exactly one `UR_*` outcome) | Yes |
| `S07_close` | Let the neighbours know. | `UR-D7` end node | Yes (→ Completed) |

S03 opens when S02 completes (the raiders are the nest's).

### UR.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `UR_BASKET_RETURNED` | `S02b_basket` | `UR-D7` variant |
| `UR_GATE_RUN` / `UR_LINE_STAKED` / `UR_LEFT` | `UR-D6` (exactly one) | MQ5, plot props, `UR-D8` epilogue |
| reads `LM_FIELD_FIX` | — | `S04` dig count; `UR-D8` epilogue |
| reads `WC_BARNS_CLEARED` | — | `UR-B3` raider line |
| reads `HW_DEN_CLEARED` | — | `UR-B3` callback line only (MQ3 owns the culvert den) |

### UR.7 The decision (Joric's) and its consequences

The player's options in `UR-D6` are offers. Joric accepts one or none. An option that tells him what to do with his ground ("You should plant it") is answered "No." and returns to the offers; it is never a resolution.

| Player offers | Joric decides | Cost | Plot afterwards |
|---|---|---|---|
| *"The gate still turns. The water could run."* | He turns the paddle himself. `UR_GATE_RUN`. | The old ditch dumps water on the communal headland; the row-warden has to dig a soak-pit and says so. | The low corner drains. Joric's bench moves to face the plot. The ground stays unplanted. |
| *"The post shows where your line stops. I can stake it."* | He walks the line with the player and drives the last stake himself. The headland strip outside his line was never his; Tansy may plant it. `UR_LINE_STAKED`. | The row-warden's communal plan is refused in front of everyone, by a line in the ground. | A staked line, Tansy's first rows on the strip, Joric's ground unchanged. |
| *"Nothing. It's yours. The pests are gone."* | He says thank you, and means it. `UR_LEFT`. | Tansy still has no ground of her own; her seed is safe now, and that is all. | Cleared, unplanted, quiet. The water still stands in the corner. |

### UR.8 Rewards and the MQ5 link

**Rewards:** crew hatchet if loaned (tool); a small payment from Tansy if the basket came back; the self-sown rye moment; Woodcutting and Melee XP from actions. No lump XP.

**UR.8.2 What MQ5 should do with each outcome** (recommendation to the Act II package; MQ5 owns its own mechanics). The "cut through Joric's plot" option is **never removed**, and Joric's MQ5 consent remains his.

| UR state | MQ5 "cut through Joric's plot" |
|---|---|
| `UR_GATE_RUN` | The relief ditch can follow the reopened field ditch from the gate: one dig point fewer. Joric's consent line: *"It's running already. Let it run further."* |
| `UR_LINE_STAKED` | The cut must go inside Joric's line (his consent, as MQ5 writes it) or along the staked headland, which crosses Tansy's new rows and costs her a season's planting. |
| `UR_LEFT` | As MQ5 writes it, plus one Joric line: *"You cleared it and asked for nothing. Ask now, if you need to."* |
| UR not played | MQ5 default. Recommend MQ5 requires clearing scrub at the cut line (the plot is overgrown). |

**Request to Act II (independent review):** MQ5's plot-scrub fight (GL-E4b, Ash Hounds) should run only if UR is not Completed; when UR is Completed, the scrub is already cleared, and the goblins Joric warns about in `UR-D7.03` ("Mind the goblins don't come back") are the natural substitute. `GL-D5.31 [UR_LEFT]` should use UR.8.2's line (the player asked for nothing).

### UR.9 Failure, recovery, co-op

Death respawns at the net bench. Traps disarm on respawn. A dropped basket returns to the nest. No fail state. In co-op, each player's `UR-D6` outcome is their own. The paddle prop (open or shut) and the stakes are per-player presentation; fallback: the paddle stays shut and the outcome is carried by dialogue and barks.

### UR.10 Integration needs

| Need | Minimum form | Fallback |
|---|---|---|
| NPC scripted walk-and-use (Joric turns the paddle / drives a stake) | NPC moves to a point and plays a use animation, server event on finish | Joric is shown standing at the gate after a short fade of the sound only; no camera change |
| Water-plane state for the low corner | Two states (standing / drained) by flag | Always standing; Joric's line carries it |
| Self-sown rye presentation | Ground decal by flag after completion | Inspect text only |

### UR.11 Ledger, decisions, review

**Mystery ledger.** *Why the corner floods:* a buried field gate closed when the plot burned. *Public belief:* "Joric's corner is cursed" / "it's low ground." *Wrong reading:* the standing water means something about his loss. Nothing in the game says so, and neither does he.
**Open decision:** the gatepost "holding mark" style is left to the Zones/art pass and is not a Riverwarden Marking Stone.

| Review finding | Revision |
|---|---|
| Draft had a child's boot print preserved under the ash. | Cut. It implied Joric's lost family. Replaced with a goblin-scavenged tin cup with no owner. |
| Draft let the player choose the outcome directly. | Offers only; directive options are refused; Joric decides. |
| MQ5 option could be locked by `UR_LEFT`. | No outcome removes it; table rewritten as variants. |
| Independent review pass: E2 refought MQ3's burned-culvert Ash Hound den (same composition, same ground). | Director ruling: MQ3 owns the den. E2 is now a goblin raiding party on the P20 threshing floor (no traps, a hauler to intercept); `HW_DEN_CLEARED` is read for one callback line only. |
| Independent review pass: "Wenna Hale" collided with Wenna Tull (Act I) and the Watcher pair Hale & Pim. | Renamed **Tansy Marl** (no hits in any 04_CONTENT_PRODUCTION file). |

### UR.12 Dialogue

```
UR-D1.01 ROW-WARDEN: "It's good ground going to waste. The Fields could feed six houses off it."
UR-D1.02 TANSY: "I'd settle for feeding mine. And something's had my seed twice this month."
UR-D1.03 ROW-WARDEN: "He won't plant it. He won't let it be planted. That's two answers I can't use."
UR-D1.04 TANSY: (lower) "He lost people. River business. Nobody ever wrote it down." (beat) "I still need ground."
  > (Ask Joric.)                                          → UR-D1.10
  > "What's been eating the seed?"                         → UR-D1.20
UR-D1.10 JORIC: (doesn't look up from the net) "Ask what's eating the seed."   → UR-D1.20
UR-D1.20 TANSY: "Something small with hands. Comes from the back of his plot. Nobody goes back there."
UR-D1.21 ROW-WARDEN: "Clear it, then, if you're offering. There's a hatchet on my cart."   {if no blade: give crew hatchet}  {event: S00_hook}
```

```
UR-D2.01 TANSY: (takes the basket, checks the knot) "Mine. Half full. They ate the rest, or planted it."
UR-D2.02 TANSY: "So it wasn't him. I never thought it was him." (beat) "I thought it a bit."   {set UR_BASKET_RETURNED}  → end
```

**UR-B3 — Raider barks (threshing floor, on E2 start):** [`WC_BARNS_CLEARED`] TANSY: *"Somebody cleared those barns after the root raid. They came back anyway."* / [else] TANSY: *"There. That's my seed going."* / [`HW_DEN_CLEARED`, after E2] ROW-WARDEN: *"Hounds are gone from the trench culvert, at least. Somebody went in after the mother."* / [`HW_DEN_CLEARED` not set, after E2] ROW-WARDEN: *"Keep clear of the trench culvert. Hounds still use the back of it."*

**Inspect texts:** *Nest:* "Broken rakes, a wheel rim, a tin cup. A seed basket with a knotted handle." / *Low corner:* "Wind on the scrub. Not a ripple on the water." / *Paddle:* "A timber paddle in an iron frame, swollen shut. Beyond it a dry ditch runs toward the headland." / *Gatepost:* "Notches down the post and a holding mark. A boundary, cut where the ditch starts. The headland strip lies outside it." / [`LM_FIELD_FIX = plot`] *Paddle:* "The new relief ditch has cut the bank open beside it."

```
UR-D5.01 JORIC: "You found the goblins."
  > "And a gate. Under the ash, in the corner."            → UR-D5.10
UR-D5.10 JORIC: (stops mending) "...There was a gate." (beat) "I'd forgotten there was a gate."
UR-D5.11 JORIC: "Water stands there. Always has, since." (he doesn't say since what)
UR-D5.12 JORIC: "Water gives things back slowly. I don't stand and wait for it."   {event: S05_joric}  → UR-D6.01
```

```
UR-D6.01 JORIC: "They want to know what I'll do with it. You've done the work. What would you do?"
  > "The gate still turns. The water could run."           → UR-D6.10
  > "The post shows where your line stops. I can stake it." → UR-D6.20
  > "Nothing. It's yours. The pests are gone."             → UR-D6.30
  > "You should plant it."                                 → UR-D6.40
UR-D6.10 JORIC: (looks at the corner for a long time, for the first time) "Moving water's not the same."
UR-D6.11 JORIC: (walks to the gate; puts both hands on the paddle; turns it)  (the standing water shivers and runs)
UR-D6.12 JORIC: "There." (beat) "That's enough for one evening."   {set UR_GATE_RUN}  → UR-D7.01
UR-D6.20 JORIC: "The headland was never mine. Cart track, before." (takes the last stake) "Let her have it."
UR-D6.21 JORIC: (drives it in, three blows, tests it)   {set UR_LINE_STAKED}  → UR-D7.01
UR-D6.30 JORIC: (long pause) "Thank you." (beat) "Not many say nothing."   {set UR_LEFT}  → UR-D7.01
UR-D6.40 JORIC: "No."   → UR-D6.01 options (UR-D6.40 hidden afterwards)
```

```
UR-D7.01 [UR_GATE_RUN] ROW-WARDEN: "That's my headland flooding now." (beat) "I'll dig a soak. Don't thank me."
UR-D7.01 [UR_LINE_STAKED] ROW-WARDEN: "A line in the ground. Can't argue with a line in the ground." (he tries anyway, under his breath)
UR-D7.01 [UR_LEFT] ROW-WARDEN: "Well. It's cleared, anyway. That's something I can tell the Fields."
UR-D7.02 [UR_LINE_STAKED] TANSY: "A strip of my own. I'll have rows in by the thaw."
UR-D7.02 [else] TANSY: "Seed's safe, at least. That's more than last month."
UR-D7.03 JORIC: (back at the net; to nobody in particular) "Mind the goblins don't come back."   {event: S07_close → quest Completed}
```

**UR-D8 — Epilogue lines** (net bench, after completion; first matching condition):

| Condition | JORIC |
|---|---|
| Rye shoots visible | "Came up on its own. Seed sat in the ash all this while." (beat) "Gives things back slowly." |
| `LM_FIELD_FIX = plot` | "Ditch through my ground. Water goes where it's told now. I watch it, some evenings." |
| `LM_FIELD_FIX = circle` | "They lifted the circle stones and put them back after. Took care over it." |
| `LM_FIELD_FIX = dike` | "Long dike. Long season. Everyone dug." (beat) "I dug." |

---

## NT — Night Ferry

### NT.1 Summary card

| Field | Value |
|---|---|
| Suggested content id | `lowmark.side.night_ferry` |
| Type | Combat challenge: night defence with crowd management (bible §7; lattice L-S15) |
| Unlock | MQ2 Completed. Offered at dusk on reaching the Greyharrow Reach ferry landing (enter volume). |
| Length | 30–40 minutes |
| Combat share | ~50% |
| Skills | Melee; Cooking optional (feeding the ring at the fire) |
| Choice | Who crosses first at dawn (2 options) |
| Outputs | `NT_DAWN_SEEN` (MQ12), `NT_LOSSES` (0–3), `NT_FIRST_WORKERS` / `NT_FIRST_HOUSEHOLD` |
| Canon used | Maelin Rowe refuses night passage through specific stretches; calm, observant ([CANON ANCHOR]). Greyharrow: fortified side-branch town, small militia, minor docks for side routes (dossier §V.4). Bandit crews and smugglers (§VIII). |
| From the True Line | Dace, Maelin's deckhand. |
| New | Sergeant Aubrey Teague (bible §5.3), Brack the night boatman, the stranded crowd, the boil at the chain. |

**Why this is not The True Line.** There is nothing to find out. The player knows from the first minute what's wrong (a fouled chain, a dark reach, people with something to steal) and spends the night keeping a crowd together until daylight makes the safe choice obvious to everyone. The core verbs are hold, relight, intercept, walk back and fight.

**One paragraph.** At dusk Greyharrow's chain ferry fouled its chain mid-reach and was hauled back. Workers due on the far bank at first light and a household going home are stranded at the landing. Maelin Rowe's barge is moored at the side dock on a side-route run, and she will not take it across the reach in the dark. Sergeant Aubrey Teague has two militia and a list of grievances, and the opportunists in the camp on the bluff above (P19) know exactly what a stranded crowd is worth. Dace is here, and he is not taking anything across anything in the dark again. The player sets a ring of lanterns, brings stragglers in, catches thieves at the carts, walks a frightened household back from a night boatman's paid crossing, and holds the ring when the opportunists douse every light at once. At dawn the mist lifts and the reach shows what the dark hid: a smooth, humped boil of water over the scour hole where the chain fouled. The night boatman's skiff is turning upside down in it.

**Remember:** the boil at dawn, and Maelin saying nothing at all for a moment. **Want next:** the night Maelin *does* cross (MQ12).

### NT.2 The place: Greyharrow Reach ferry (P19)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Ferry landing** | Hook; dawn | The flat ferry hauled back against the landing, its chain running out taut into the dark and then slack. A chain bar bent at the grip. Maelin's barge at the side dock, lamps unlit on purpose. |
| **B. Cart ring** | The defence | Four carts and a fire. Four lantern posts mark the ring's lanes. Workers' tool rolls, a household's trunk and a cradle-basket, a goat tied to a wheel. |
| **C. Dark landing** | Brack's pitch | A shingle spit downstream, out of the lantern light, where a skiff can tie up unseen. |
| **D. Reed edge** | Thieves' run | Trampled path into the reeds toward the bluff. |
| **E. Bluff camp** (P19) | Optional raid | Opportunists' tarps on the bluff above the ferry; a lookout's stool; stolen bundles stacked under a tarp; a pot of something unappetizing. |
| **F. The reach at dawn** | The answer | Where the chain dips, the river humps into a smooth, slowly turning boil the size of a barn floor. In the dark it is invisible. |

**Unease (midnight):** for about ten breaths the reach goes silent (dead-spot audio duck), every dog in the ring turns to look at the water, and then the sound comes back. Nobody says anything except a child: *"It stopped."* **Wonder (dawn):** lanterns go out one by one along the ring as the light comes; Maelin calls marks from the bow across a river that is finally visible.

### NT.3 Player-facing sequence

**Beat 0 — Stranded (`S00_hook`).** *Objective: Find out why the ferry has stopped.* `NT-D1` with Teague and Maelin at the landing.
**Beat 1 — The ring (`S01_ring`).** *Objective: Light the lanterns and bring everyone into the ring.* Light 4 lantern posts (2 s channel each) and walk 3 stragglers in from the bank (each starts a short bark and follows the player; escort ends in the ring volume). Optional: cook at the fire and feed the ring (`S01b_feed`) for a warmer dawn line.
**Beat 2 — First watch (`S02_first_watch`).** *Objective: Keep watch at the fire.* Watch interaction advances the night. Three thieves try the carts in turn (E1). Each crouches at a cart and rummages for about 2 s (the intercept window), then runs for the reed edge with a bundle. Caught inside the ring: no loss. Reaching the reeds: `NT_LOSSES` +1, and the bundle goes to the bluff camp.
**Optional — The bluff (`S02b_bluff`).** *Objective: Get the stolen bundles back.* Available from the second watch onward. Raid the bluff camp (E4) and carry each bundle (carry-state) back to its cart; each one returned is −1 to `NT_LOSSES`.
**Beat 3 — Second watch (`S03_second_watch`).** *Objective: Keep watch at the fire.* Brack ties up at the dark landing and calls a price for a night crossing. The household with the cradle-basket starts walking toward him. The player can (a) catch them on the path and talk them back (`NT-D3`), or (b) go down to Brack (`NT-D4`), then talk the household back. At the landing the player can cut Brack's mooring (2 s; his two pole-men attack, E2; the skiff drifts off empty) or warn him off. The step completes when the household is back inside the ring.
**Beat 4 — Third watch (`S04_third_watch`).** *Objective: Hold the ring until dawn.* A shout from the bluff, then wet sacks thrown from the dark put out all four lanterns at once (2 s telegraph: shouts and a rush of feet). E3 comes through the dark lanes in two waves. Teague and Dace each hold one lane (they cannot be downed; they slow the enemies at their lane), and the player relights the lanterns and fights. A lit lane is one enemies won't enter, so each relight closes a way in. Brack comes in the second wave.
**Beat 5 — Dawn (`S05_dawn`).** *Objective: Talk to Maelin at the landing.* Watch to dawn. The mist lifts; the boil is plain; Brack's skiff (cut loose or pushed off) turns over in it. `NT-D5`: Maelin's refusal, understood, and the choice of who crosses first.
**Beat 6 — Crossing (`S06_crossing`).** *Objective: Cross with Maelin.* The player rides the first crossing (Maelin's crossing interaction). Arrival on the far bank: `NT-D6`. Quest Completed.

### NT.4 Encounters

| Id | Enemies | Where | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 3 Smuggler cutters (thieves), one at a time | Cart ring → reed edge | Target a cart, not the player; once engaged, Aggressive and fight to downed | Rummage crouch at a cart (~2 s), then a sprint path to the reeds shown by trampled ground. In combat: shoulder drop, blade low (~0.9 s), two quick cuts. | Three catches possible for a player who watches the carts. Each fight 15–25 s. |
| **E2** | 2 Smuggler pole-men | Dark landing | Aggressive once the mooring is cut | Plant the pole and lean back (~1.2 s), then a sweep with 2 m knockback; the shingle spit has water on two sides (knockback into the shallows only slows the player). | Optional. 40–60 s. |
| **E3a** | 2 cutters (dousers), 1 pole-man | Dark lanes | Dousers go for lit lanterns first; telegraph is a raised wet sack while running (~1.5 s) | As above | Required. |
| **E3b** | 2 pole-men + **Brack** (named cutter, ~2× cutter health) | Dark lanes | Aggressive | Brack: laughs and steps back (~1.0 s), then a long lunge; once per fight he grabs a fallen lantern and throws it, leaving burning oil on the ground (3 m, 3 s; ring of fire shown before it lands, ~1.2 s). | Required. 60–90 s. Player at 40–70% HP on a first attempt; Teague and Dace slow the lanes so the player is never fighting more than three at once. |
| **E4** | 2 cutters, 1 pole-man (lookout) | Bluff camp | Defensive around the tarp; do not pursue past the bluff edge | As above | Optional. 45–60 s. |

Downed opportunists are tied by Teague's militia at dawn. Nothing they carry advances the quest except the bundles, which are world objects.

### NT.5 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Find out why the ferry has stopped. | `NT-D1` end node | Yes |
| `S01_ring` | Light the lanterns and bring everyone into the ring. | 4 `light_lantern` interactions + 3 escort-arrival events in ring volume | Yes |
| `S01b_feed` | (Optional) Feed the ring. | Cooked food given to a ring NPC | No |
| `S02_first_watch` | Keep watch at the fire. | Watch interaction; then 3 thief events resolved (downed or escaped) | Yes |
| `S02b_bluff` | (Optional) Get the stolen bundles back. | Each bundle carry-deposited at its cart | No |
| `S03_second_watch` | Keep watch at the fire. | Watch interaction; household escort-arrival in ring volume | Yes |
| `S04_third_watch` | Hold the ring until dawn. | Watch interaction; E3b defeated | Yes |
| `S05_dawn` | Talk to Maelin at the landing. | Watch interaction (dawn); `NT-D5` choice resolved | Yes |
| `S06_crossing` | Cross with Maelin. | Crossing interaction; enter far-bank volume; `NT-D6` end | Yes (→ Completed) |

### NT.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `NT_LOSSES` (0–3) | E1 escapes; bundle returns | `NT-D5`, `NT-D6` variants |
| `NT_FED` | `S01b_feed` | `NT-D6` |
| `NT_BRACK_CUT` / `NT_BRACK_WARNED` | `NT-D4` | Dawn skiff presentation line |
| `NT_FIRST_WORKERS` / `NT_FIRST_HOUSEHOLD` | `NT-D5` (exactly one) | `NT-D6`, Greyharrow barks |
| `NT_DAWN_SEEN` | Completion | MQ12 Maelin line |

### NT.7 Choices and consequences

| Option | Immediate | Cost |
|---|---|---|
| **Workers first** — *"The workers. They'll lose their places."* | The workers make their shift. | The household waits another crossing in the cold; the baby cries for all of it, and the father does not thank anyone. |
| **Household first** — *"The family. The baby's been out all night."* | The household is home by breakfast. | The workers are late and docked a day's pay; one says he'll be told not to come back. |

`NT_LOSSES` is a consequence, not a choice: each lost bundle is one household or worker going home without something (tools, a coat, the goat), named in the dawn lines.

### NT.8 Rewards

Small payment from Teague's militia purse (he complains about it); a household's thanks (one cooked food item, item pass) if `NT_LOSSES` is 0; Melee and Cooking XP from actions; `NT_DAWN_SEEN`. No lump XP.

### NT.9 Failure, recovery, co-op

No fail. Death respawns at the ring fire; doused lanterns stay doused, downed enemies stay down, the current wave continues. If the player leaves the ring area during a watch, the watch pauses (no wave advances) until they return. Teague and Dace cannot be downed and never hold the ring alone for long enough to matter. Logout restores the last completed watch. In co-op, each player has their own crowd and their own losses; shared opportunists count for both players' current step. A partner's lanterns light for both players (shared world props) [integration check].

### NT.10 Integration needs

| Need | Minimum form | Fallback |
|---|---|---|
| Watch interaction advancing quest time | As MQ4: interaction → server step event → lighting state | Watches are step events with a lighting change only |
| Lantern-post state affecting enemy pathing | Lit post = lane blocked to Smugglers AI | Lit posts give enemies a short hesitation instead of blocking |
| Escort-follow for role NPCs | Follow-the-player state, ends in a volume | NPC walks to the ring on dialogue end |
| Thief target-a-prop behaviour | AI targets a cart prop, then pathing to an exit volume | Thieves target the player; losses are counted per thief defeated late |
| Unkillable ally NPCs at lanes | Ally with damage-immune flag and a slow aura | Allies stand at lanes as blockers |

### NT.11 Ledger, decisions, review

**Mystery ledger.** None needed: the danger is present and plain. The boil at the chain is river mechanics (a scour hole), not drift. **Open decision:** none.

| Review finding | Revision |
|---|---|
| Draft opened with "who fouled the chain?" | Cut. That made it an investigation. The chain fouled on the scour; nobody did it. |
| Draft's dawn showed a drowned wreck under the line. | Too close to the True Line's drowned pier. Replaced with the boil, visible only in daylight. |
| Thieves running away read as fleeing at low HP. | They run *before* combat with a bundle; once engaged they fight to downed. |

### NT.12 Dialogue

```
NT-D1.01 TEAGUE: (writing in a small book) "Ferry's fouled. Crestbridge has been told. Crestbridge will send nobody. Grievance forty-one."
NT-D1.02 MAELIN: "Chain's caught on the bottom, mid-reach. I'm not taking the barge over it in the dark."
NT-D1.03 TEAGUE: "Rowe, there are thirty people on this bank and a camp of thieves on that bluff."
NT-D1.04 MAELIN: "Better robbed on the bank than drowned in the reach."
NT-D1.05 DACE: (from the barge) "She's right. I know. I tried it the other way once."
  > "What do you need?"                                     → NT-D1.10
  > "Why won't you cross?"                                  → NT-D1.20
NT-D1.10 TEAGUE: "Lanterns lit, people inside them, and a third pair of hands until the sun comes up. Mostly the hands."   → NT-D1.30
NT-D1.20 MAELIN: "Because I can't see it. In the morning I'll see it. Then I'll cross."   → NT-D1.30
NT-D1.30 TEAGUE: "Four posts. Light them. Anybody wandering at the water, bring them in. I'll put you on my list of good things. It's short."
      {event: S00_hook}
```

**Straggler barks (escort):** WORKER: *"I'm only looking at the water. Fine. Fine, I'm coming."* / OLD CARTER: *"Lanterns. In my day we had one lantern and we were grateful."* / CHILD: *"Mam says I can't go near the edge. I'm not near it. I'm next to near it."*

```
NT-D2 — First watch barks
TEAGUE: "Watch the carts, not the dark. The dark's not going to steal anything."
[thief escapes] HOUSEHOLD: "My coat! That was my good coat!"   /   WORKER: "That's my tools gone. That's my work gone."
[thief caught] TEAGUE: (adding a line) "Good thing number two."
```

```
NT-D3.01 FATHER: (halfway to the dark landing, the cradle-basket on his arm) "He says he'll take us over for a coin each. Tonight."
NT-D3.02 MOTHER: "She's freezing. Look at her. We could be home by midnight."
  > "Maelin won't cross because she can't see the reach. Neither can he."   → NT-D3.10
  > "If his boat were safe, he'd tie it up in the light."                    → NT-D3.10
  > "I'll go and talk to him."                                              → NT-D4.01
NT-D3.10 FATHER: (looks back at the ring, then at the dark) "...He did say not to bring a lantern."
NT-D3.11 MOTHER: "Back. Come on. Back."   {household follows the player}  → end
```

```
NT-D4.01 BRACK: (in the skiff, one hand on the mooring line) "Evening. Crossing tonight. One coin a head, babies free. I'm generous."
NT-D4.02 BRACK: "The barge-mistress is careful. I'm quick. Which do you want to be?"
  > "Nobody's getting in that boat."                         → NT-D4.10
  > (Cut the mooring line.)                                  → NT-D4.20
NT-D4.10 BRACK: "Shame. I'll be about." (pushes off into the dark, empty)   {set NT_BRACK_WARNED}  → end
NT-D4.20 BRACK: "Oh, now that's rude." (whistles; two men come off the spit)   {set NT_BRACK_CUT; start E2; skiff drifts}  → end
```

```
NT-D5.01 MAELIN: (on the landing; the mist going; the boil plain where the chain dips) "There."
NT-D5.02 MAELIN: (says nothing for a moment)
NT-D5.03 [NT_BRACK_CUT or NT_BRACK_WARNED] DACE: "That's his skiff. Upside down. Turning."
NT-D5.04 TEAGUE: (quietly) "Hole in the bottom of the reach. You'd never have seen it."
NT-D5.05 MAELIN: "In the dark it looks like water. In the light it looks like that. So I wait for the light."
NT-D5.06 MAELIN: "One load first. Who goes?"
  > "The workers. They'll lose their places."               → NT-D5.10
  > "The family. The baby's been out all night."            → NT-D5.20
NT-D5.10 MAELIN: "Workers. Get on." (to the father) "Next one. I'll be quick."   {set NT_FIRST_WORKERS}  {event: S05_dawn}
NT-D5.20 MAELIN: "Family. Get on." (to the workers) "Tell your foreman a barge master said so. He won't care. Tell him anyway."   {set NT_FIRST_HOUSEHOLD}  {event: S05_dawn}
```

```
NT-D6.01 MAELIN: (far bank; she ties off, looks back at the reach) "You held them all night. That's harder than crossing."
NT-D6.02 [NT_LOSSES = 0] MAELIN: "Nobody's short a coat. Teague'll write that down twice."
NT-D6.02 [NT_LOSSES > 0] MAELIN: "Some of them are going home lighter. They're going home."
NT-D6.03 [NT_FED] DACE: "You fed them, too. I'm telling everyone. I'm not telling them you burned the edges."
  > "You were right not to cross."                          → NT-D6.10
  > "Will you ever cross at night?"                         → NT-D6.20
NT-D6.10 MAELIN: "I'm right every night I don't. That's the trouble with being right." → NT-D6.30
NT-D6.20 MAELIN: "When the water's honest enough to read in the dark." (beat) "Not yet."   → NT-D6.30
NT-D6.30 MAELIN: "Go and sleep. River keep you."   {event: S06_crossing → quest Completed; set NT_DAWN_SEEN}
```

**MQ12 hook (for the Act III package):** if `NT_DAWN_SEEN`, at the night crossing Maelin may say: *"Remember Greyharrow? The boil? Tonight I can see it in the dark."*

---

## FW — Fen Watch

### FW.1 Summary card

| Field | Value |
|---|---|
| Suggested content id | `lowmark.side.fen_watch` |
| Type | Combat challenge: hold a boundary, elite (bible §7; lattice L-S16) |
| Unlock | **MQ5 *The Guide-Line* Completed** (Milestone 2 equipment expected). Offered by Lessa Mirepath at the Reedmere warning post. Between MQ3 and MQ5, visiting the post plays Lessa's soft warning (`FW-B0`) and offers nothing. The elite is a high-tier preview and should feel like it. |
| Length | 30–40 minutes |
| Combat share | ~55% |
| Skills | Woodcutting (withies, entry level), Melee |
| Choice | Whether Ivo's cutters may use the reed bed on Lessa's kept path (2 options) |
| Outputs | `FW_GUIDE_ROUTE` (MQ11 optional approach), `FW_BED_SHARED` / `FW_ROUTE_KEPT` |
| Canon used | Lessa Mirepath: quiet, practical, speaks to the land as if it listens, treats some paths as permanently closed regardless of payment, refuses to explain why ([CANON ANCHOR]). Stillwater Serpents in the deeper fen pools, drawn to Wraith-choked water; Reed Stalkers; riverglass reed prized by glasswrights (dossier §VIII, §IX). |
| New | The withy line, Ivo Teasel and his cutters, the cutters' staging, the Deep-Pool Serpent as an individual. |

**Lessa guard.** Her "done" paths stay done. Nothing in this quest reopens one or explains why it is closed. The reward is a *different* path she keeps. She has no kin, chapel knowledge or supernatural access here.

**One paragraph.** The reed on the done stretch below Reedmere has grown tall and glossy, riverglass reed of the kind glasswrights pay for, and with prices up Ivo Teasel's cutters have started pulling up Lessa's withy line to get at it. Her warning crew has been shouted off its own boundary twice. The player cuts fresh withies and re-sets the line, goes past it to pull three cutter crews back before the Reed Stalkers find them, and holds the line at dusk when the stalkers come for it. Then the noise brings up what lives in the deep pool beside the cutters' staging. After the serpent sinks, the reeds along the done stretch lean toward the pool in still air, and straighten. Lessa says, "That's why," and nothing else. Afterwards she shows the player a path she has kept open, and asks what the cutters should get out of it.

**Remember:** standing on a staked disc of timber while a serpent the width of a barrel arches over the mat. **Want next:** the night that path will matter (MQ11).

### FW.2 The place: Reedmere approaches (P06)

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Warning post** | Hook | A pole platform with a horn and a slate: *DONE BELOW THE WITHIES*. A tally of skiffs that passed, the last three strokes scored through angrily. |
| **B. The withy line** | Boundary | Peeled willow withies in a line across the channel mouth, white in the dusk. Five are gone; the holes remain, and two withies float in the shallows, snapped. |
| **C. Osier stools** | Woodcutting | Pollarded osiers behind the post, cut in turn; a crew knot on this year's stools. |
| **D. The done stretch** | Off limits | Reed taller than a person, veins glossy in low light. No birds. The water between stems is perfectly clear and very deep. |
| **E. Cutters' places** | Three groups | Skiffs nosed into the reed, bundles stacked, a cookpot on a board. One group has a child bailing. |
| **F. The staging** | Elite arena | The cutters' loading stage at the deep pool's edge: a reed-mat floor on timber, about 20 × 14 m (MAP VERIFICATION REQUIRED). Four stakes driven deep, each with a white rag and a timber disc round it: Lessa's firm ground. The pool side has a low timber kerb. A shallow strip runs along the landward side. |
| **G. The kept path** | Reward | A narrow way through the reeds away from the done stretch, marked by knots tied in reed heads at shoulder height. |

### FW.3 Player-facing sequence

**Beat 0 — The line (`S00_hook`).** *Objective: Talk to the warning crew.* `FW-D1` with Lessa.
**Beat 1 — Re-set it (`S01_withies`).** *Objective: Cut withies and re-set the line.* Cut 5 withies from knotted osier stools (Woodcutting gather), set each in a hole (2 s channel). Lessa sets the first and says something to it.
**Beat 2 — Pull them back (`S02_cutters`).** *Objective: Bring the cutters back behind the line.* Three groups beyond the withies, any order. Group 1: a bark and they come. Group 2: Ivo Teasel (`FW-D2`) argues, then comes. Group 3: Reed Stalkers hit them as the player arrives (E1); after the fight one cutter is limping and follows the player out slowly (escort). Each group's return is an escort-arrival behind the line.
**Beat 3 — Hold (`S03_hold`).** *Objective: Hold the withy line until dark.* Two stalker waves (E2). Stalkers target withies (they pull them over and drag them into the water; telegraph: a stalker grips a withy and throat-swells, ~1.5 s). A pulled withy is re-set with a 2 s channel. The line holds if, at the end of each wave, at least three withies stand; if not, the wave repeats with one fewer stalker. It cannot be lost.
**Beat 4 — The pool (`S04_serpent`).** *Objective: Survive what's in the deep pool.* As the second wave ends the horn sounds from the post: the cutters' staging is shaking. The Deep-Pool Serpent (E3). Lessa stands at the landward edge calling the tells.
**Beat 5 — The last withy (`S05_last_withy`).** *Objective: Set the last withy.* At the staging's edge. Lessa sets it with the player. The moment of unease. `FW-D4`: the choice.
**Beat 6 — The kept path (`S06_route`).** *Objective: Follow Lessa.* She walks the kept path to its first three knots (follow-the-NPC; she waits if the player stops). `FW-D5`. Quest Completed; `FW_GUIDE_ROUTE`.

### FW.4 Encounters

| Id | Enemies | Where | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 Reed Stalker stalkers, 1 lurker | Group 3's skiff | Aggressive in the reeds; they target cutters first (cutters back off and cannot be downed) | Reeds part in a line (~1.2 s), leap; throat-swell (~1.0 s), tongue-lash pull 3 m toward water. Lurker: bubble ring (~1.5 s), surfacing grab. | Required. 45–60 s. |
| **E2** | Wave 1: 3 stalkers. Wave 2: 3 stalkers + 1 lurker | Withy line | Target withies, then the player | Withy grip + throat-swell (~1.5 s) before a pull | Required. 60–90 s per wave. |
| **E3** | **Deep-Pool Serpent** (Stillwater Serpents elite) | The staging | Elite; spec below | — | Required. 3–4 minutes. |

#### FW.4.1 Elite spec — the Deep-Pool Serpent

| Field | Spec |
|---|---|
| Family / tier | Stillwater Serpents, high tier, elite (bible §10). First appearance of the family; MQ11's breaching serpent at the second gate is a different individual. |
| Read | A body thicker than a barrel, mostly under water. Only the head and forebody are ever fully visible. Pale underside, dark back; it never makes a sound above water. Its movement is shown by the water and the reeds before the body. |
| Arena rules | **Stakes** (4 timber discs, 2 m across): firm ground. Coil-slam does no damage there, and tail-sweep and drag cannot move a player standing on one. **Soft mat:** everything hits. **Shallows** (landward strip): slows movement; no extra damage. **Kerb:** the pool edge has a timber kerb. Nothing throws the player into deep water. |
| Health target | Solo, Competent (Milestone 2) equipment, which the MQ5 unlock assumes: 3–4 minutes. Exact values belong to the Gameplay Designer. |
| **Strike** (all phases) | The water humps and a V-wake runs at the player; reeds flatten along a 6 m × 1.5 m line on the mat (**1.5 s**). Lunge along the line: heavy damage (about a quarter of a Milestone 2 player's health). Step off the line. **Punish:** the head rests on the mat for 2 s. Cadence ~8 s (P1–P2), ~6 s (P3). |
| **Tail sweep** (all phases) | The tail breaks the surface on the pool side and the reeds rustle along a 120° arc toward the landward edge (**1.5 s**). Moderate damage and a 3 m knockback into the shallows. Move inside the arc's end or onto a stake. Cadence ~12 s. |
| **Coil-slam** (P2–P3) | The body rises in an arch over the mat; a 4 m circle of shadow settles on the player's position and the mat sags (**2.0 s**). Heavy damage on soft mat; none on a stake. Leaves the circle flooded (slow) for 5 s. Cadence ~15 s. |
| **Sound and breach** (at 66% and 33%) | It submerges; 6 s with no attacks; then **one** ring of bubbles widens at one of three breach points on the staging edge, and the reeds there bend away (**2.5 s**). Breach: damage in a 3 m radius. **Punish:** it lies across the staging for 4 s and takes increased damage. |
| **Drag** (P3, below 33%) | It coils one stake: the white rag snaps taut and the stake creaks (**2.0 s**). For 4 s the mat tilts toward the pool; players on soft mat slide 1 m per tick toward the kerb (damage only on reaching it); players on any *other* stake are unaffected. The coiled stake is unusable until the drag ends. Cadence ~20 s. |
| Phases | P1 100–66%: strike, tail sweep. P2 66–33%: + coil-slam. P3 below 33%: + drag, faster strike. No enrage timer. No adds. Never flees. |
| Ally | Lessa stands at the landward edge and calls each tell once ("Line!", "Tail!", "Off the mat!", "Bubbles, left!", "Stake!"). She cannot be targeted. Her calls are a readability aid and can be muted with dialogue barks. |
| Defeat | It sinks. The pool goes glass-flat. No harvest in v1 pending the item pass. |
| Reset | If no player is engaged for 30 s it returns to full and submerges. Withies and step progress are kept. |

### FW.5 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Talk to the warning crew. | `FW-D1` end node | Yes |
| `S01_withies` | Cut withies and re-set the line. | 5 withy gather events + 5 `set_withy` interactions | Yes |
| `S02_cutters` | Bring the cutters back behind the line. | 3 escort-arrival events behind the line (group 3 after E1 defeated) | Yes |
| `S03_hold` | Hold the withy line until dark. | E2 waves 1 and 2 resolved with ≥3 withies standing | Yes |
| `S04_serpent` | Survive what's in the deep pool. | E3 defeated | Yes |
| `S05_last_withy` | Set the last withy. | `set_withy` at the staging; `FW-D4` choice resolved | Yes |
| `S06_route` | Follow Lessa. | Enter knot-3 volume; `FW-D5` end | Yes (→ Completed) |

### FW.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `FW_IVO_ANGRY` | `FW-D2` firm option | `FW-D4` Ivo line |
| `FW_BED_SHARED` / `FW_ROUTE_KEPT` | `FW-D4` (exactly one) | MQ11 variant; Reedmere barks |
| `FW_GUIDE_ROUTE` | Completion | MQ11 optional approach |

### FW.7 Choices and consequences

| Option | Immediate | Cost | MQ11 |
|---|---|---|---|
| **Share the bed** — *"Show them the reed bed on your path. If they keep to it."* | Lessa agrees; Ivo's crews get good reed on safe ground. | Lessa's kept path becomes a cutters' road: "Then it's a road. Roads get used." | The route is busy; Ivo's skiffs are there in Phase 1 and can carry two evacuees (variant). |
| **Keep the path** — *"Keep it. They cut the low beds by Reedmere."* | The cutters go to the poor low beds near the stilts: safe, thin reed. | Ivo's crews earn less this season, and Ivo says so at every chance. | The route is quiet and empty: only the player and Lessa use it. |

Either way the done stretch stays done, and the warning crew holds its boundary.

### FW.8 Rewards

**Lessa's kept path** (access; `FW_GUIDE_ROUTE`): a fen-edge route marked by reed-head knots, usable after completion and offered as an optional Phase 1 approach in MQ11. A small payment from the warning crew's box. Woodcutting and Melee XP from actions. No lump XP.

### FW.9 Failure, recovery, co-op

No fail. Death respawns at the warning post with withies, cutters and waves kept; the serpent resets only if nobody is engaged. In co-op, each player needs their own escorts; stalkers and the serpent are shared world creatures and give step credit to everyone on the step. Elite scaling for groups is a Gameplay Designer call.

### FW.10 Integration needs

| Need | Minimum form | Fallback |
|---|---|---|
| AI targeting props (withies) | Stalker targets prop, prop state "pulled" | Stalkers target the player; withies fall on stalker defeat instead |
| Ground-zone tags (stake / soft mat / shallows) on the elite's attacks | Damage and displacement multipliers per zone volume | Stakes give full immunity to slam and drag only |
| Moving-mat "drag" displacement | Server-side forced move per tick | Drag becomes a damage pulse on soft mat |
| Follow-the-NPC (Lessa) | NPC path with wait-for-player | Lessa waits at knot 3 |

### FW.11 Ledger, decisions, review

**Mystery ledger.** *Why the stretch is done:* withheld (Lessa never says). *Player-observable:* deep clear water, no birds, a serpent, reeds that lean. *Wrong reading:* the serpent is the reason. It is one reason Lessa will admit to with "That's why," and the leaning reeds suggest it isn't the only one. Nothing settles it.
**Resolved (Director ruling, independent review pass):** FW unlocks after MQ5. Before that Lessa gives the soft warning `FW-B0`. MQ11 still only needs FW done before MQ11.

| Review finding | Revision |
|---|---|
| Draft had the serpent knock players into the deep pool. | Timber kerb; no instant loss; drag only damages. |
| Draft let the boundary fail and the quest branch on it. | Waves repeat with fewer stalkers; it cannot be lost. |
| Draft had Lessa explain the done stretch after the fight. | Two words, no account. |
| An Ivo line credited "her mother" with the withies, which gave Lessa invented kin. | Changed to "Nobody ever said." |
| Independent review pass: the elite was a difficulty spike at the MQ3 gate; "calling the water" edged toward supernatural access. | Unlock moved to MQ5 with soft warning `FW-B0`; tuning restated for Milestone 2; "calling the tells". |

### FW.12 Dialogue

**FW-B0 — Soft warning (warning post, MQ3 Completed, MQ5 not Completed):** LESSA: *(looks at the player's kit, then at the deep pool)* "Not yet. Come back when the fields are seen to." No objective is given.

```
FW-D1.01 LESSA: (setting a snapped withy on the slate) "They pulled the line again. Third time."
FW-D1.02 LESSA: "Reed's good below it. Glossy. Glasswrights pay double. So the cutters go."
FW-D1.03 LESSA: "Below the withies is done. I don't take anyone there. Not for double. Not for anything."
  > "Why is it done?"                                       → FW-D1.10
  > "What do you need?"                                     → FW-D1.20
FW-D1.10 LESSA: (looks at the reeds, not the player) "It's done."   → FW-D1 options
FW-D1.20 LESSA: "New withies from the knotted stools. Five. Set them in the holes. Then bring the cutters back before something else does."
FW-D1.21 LESSA: (to the first withy as she sets it) "Stay."   {event: S00_hook}
```

```
FW-D2.01 IVO: (knee-deep, sickle in hand) "Lessa sent you. Course she did."
FW-D2.02 IVO: "That reed's worth a season. My lot haven't had a season since the shortages."
  > "Stalkers are in these reeds. Come back."                → FW-D2.10
  > "Back behind the line. Now."                            → FW-D2.20
  > "Why does she say it's done?"                           → FW-D2.30
FW-D2.10 IVO: "Stalkers are in all the reeds." (looks round anyway) "...Fine. Bundles first."   → end {group 2 follows}
FW-D2.20 IVO: "Who made you warden?" (spits) "Fine."   {set FW_IVO_ANGRY}  → end {group 2 follows}
FW-D2.30 IVO: "Never says. Nobody ever said. Just sticks in the water, as long as anyone remembers."   → FW-D2 options
```

**Group barks:** GROUP 1 CUTTER: *"All right, all right. It was getting dark anyway."* / GROUP 3 CUTTER (after E1, limping): *"Slowly. I've got one good leg and it's not this one."* / CHILD (group 3): *"I was bailing. I was doing a good job."*

**E3 serpent barks (Lessa, once per tell):** *"Line! Off the line!"* / *"Tail!"* / *"Off the mat! Stakes!"* / *"Bubbles. Left side."* / *"It's on a stake. Not that one."* / (on defeat, quietly) *"Easy. Easy now."*

```
FW-D4.01 LESSA: (setting the last withy at the staging's edge; the pool glass-flat)
      (Along the done stretch, every reed leans toward the pool in still air. Then straightens.)
FW-D4.02 LESSA: "That's why."
  > "That's why what?"                                      → FW-D4.03
  > (Say nothing.)                                          → FW-D4.04
FW-D4.03 LESSA: (doesn't answer)                            → FW-D4.04
FW-D4.04 LESSA: "Cutters still need reed. There's a bed on a path I keep. Good reed, safe ground."
FW-D4.05 [FW_IVO_ANGRY] IVO: (from behind the line) "Safe ground. That'll be the day."
FW-D4.06 LESSA: "Your say. You pulled them out."
  > "Show them the bed on your path. If they keep to it."   → FW-D4.10
  > "Keep it. They cut the low beds by Reedmere."            → FW-D4.20
FW-D4.10 LESSA: "Then it's a road. Roads get used." (beat) "All right."   {set FW_BED_SHARED}  {event: S05_last_withy}
FW-D4.20 LESSA: "Low beds are thin. They'll live." (beat) "So will the path."   {set FW_ROUTE_KEPT}  {event: S05_last_withy}
```

```
FW-D5.01 LESSA: (at the third knot) "Knots at the shoulder. Follow them, you're on firm ground. Lose them, stop."
FW-D5.02 LESSA: "It goes in a long way. Not to anywhere done."
  > "Why show me?"                                          → FW-D5.10
  > "I'll remember."                                        → FW-D5.20
FW-D5.10 LESSA: "You stood on a stake when I said stake." (beat) "Most don't."   → FW-D5.20
FW-D5.20 LESSA: (to the reeds) "This one's all right." (to the player) "Go on. River keep you."
      {event: S06_route → quest Completed; set FW_GUIDE_ROUTE}
```

---

## OL — Old Lantern

### OL.1 Summary card

| Field | Value |
|---|---|
| Suggested content id | `lowmark.side.old_lantern` |
| Type | Combat challenge, **miniboss** (bible §7, §10; dossier "Wraithwatchers Gone Wrong") |
| Unlock | MQ3 Completed (the player has seen Ansel's patrol book). Offered by Ansel Corrie at the Watchers' Lantern Post (P21). |
| Length | 30–40 minutes |
| Combat share | ~45% |
| Skills | Melee; tracking by inspection (no skill gate) |
| Choice | Bring Joss in alive to Elspeth Quill's care, or bring back only his lantern (both honoured) |
| Outputs | `OL_JOSS_IN` / `OL_LANTERN_ONLY`; drift site **Old Lantern's bend** → quieted (bible §9.2) |
| Canon used | Wraithwatchers: patrol bands with oil lanterns, blessed rope and banner-thistle smoke, no spellcasting; overwhelmed and without real understanding (dossier §III, §XVI). "Wraithwatchers Gone Wrong": former patrol members corrupted by long exposure to Wraith-haunted zones; human-scale minibosses (§VIII). Water Wraiths as place-bound manifestations, not souls. |
| New | Joss Garrow (bible §5.3), his history with Ansel, the far leg, the reed shelter, lantern-drift behaviour around his light. |

**Evidence guard (binding).** Joss's state is shown and never explained. Nothing he says, carries or wrote names, counts or describes any dead person. His calls are the ordinary patrol calls every Watcher uses. His book holds places, times and tally strokes. Being near drift for years did this to a man, and that is all the quest says. Combat reveals nothing.

**One paragraph.** Since MQ3 the player has seen one line repeat in Ansel's patrol book: *"Lantern on the far leg. Not ours."* Ansel knows whose it is. Joss Garrow walked the Whisperflow-to-fen leg with him for years. Joss wanted to know *why* the water went wrong when Ansel was content with where and when, and one winter he walked into the fen to find out and didn't come back. The Watchers wrote him "lost on patrol". His lantern still walks the far leg every second night. The player tracks Joss's patrol by his notches on the posts, his dropped thistle stubs and a reed shelter full of drying pages, then waits at his bend for the light. Joss treats the player as drift. The fight is a Watcher's whole craft turned the wrong way (lantern, rope, the count), and when he goes down to one knee he says "End of leg." Then the player brings him in, or carries his lantern home and leaves him to the patrol he won't stop walking.

**Remember:** a lantern with a dry oil well that keeps burning. **Want next:** to know what the count Joss kept is counting (MQ11, the Muster's stroke-calls).

### OL.2 The place: the far leg and Old Lantern's bend

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **A. Lantern Post** (P21) | Hook, return | The patrol book on its shelf. A row of lantern hooks with one empty, rusted rather than worn. Under it, scratched in the wood: *J.G.* |
| **B. The far leg** | Tracking | A path along the fen edge past old patrol posts. Each post has a Watcher's waymark notch, and Joss's are fresh: cut clean, cut again over old cuts. Stubs of burned banner-thistle in the mud where someone lit smoke and stamped it out. |
| **C. Reed shelter** | Joss's camp | A reed lean-to with a patrol coat gone green. Pages pinned to dry on a cord, every page the same entry in the same hand: *Far leg. Heavy at the willow. Lantern lit.* Later pages hold only tally strokes in fives, hundreds of them. A coil of rope worn smooth. No food. |
| **D. The willow bend** (Old Lantern's bend) | Miniboss arena | A slow bend under a dead willow. Four old patrol posts on raised footings (stone, knee-high). A shallow ford of heavy water across the middle; the deep side beyond a line of reeds. Ansel's waypoint stone at the landward edge. |
| **E. Return path** | Escort or carry | The far leg back to the Post, with two drift pockets that wake if a lantern passes lit (see OL.4). |

**Traversal:** one agility step-up onto each post footing (Phase 1.3). **Fallback:** each footing also has a stone ramp on its landward side.

**Unease (C, D):** inspect Joss's lantern after the fight: *"The oil well is dry. Has been for a long time. The flame doesn't care."* That is the whole explanation the game gives.

### OL.3 Player-facing sequence

**Beat 0 — Not ours (`S00_hook`).** *Objective: Ask Ansel about the lantern on the far leg.* `OL-D1`. Ansel lends a bundle of banner-thistle smoke (carried Watcher tool, as in MQ3; reusable for this quest).
**Beat 1 — His notches (`S01_track`).** *Objective: Follow the far leg.* Inspect three fresh notched posts in order (each inspect points to the next). Optional: two thistle stubs (`S01b_stubs`; one extra line from Ansel later).
**Beat 2 — The shelter (`S02_shelter`).** *Objective: Search the reed shelter.* Inspect the pages, the tally pages and the rope. The last page carries the Watchers' leg-closing call written out in full: *"Lantern in. Leg closed."* (`OL_CALL_KNOWN`).
**Beat 3 — The bend at dusk (`S03_watch`).** *Objective: Wait at the willow bend for the lantern.* Watch interaction at Ansel's waypoint stone, advancing to nightfall. The light comes along the leg; a voice calls *"Lantern coming in! Wraithwatch."*, Ansel's call, in someone else's voice. Approaching within 15 m starts the fight (`OL-D3` bark).
**Beat 4 — Old Lantern (`S04_joss`).** *Objective: Stop Joss Garrow.* Miniboss (E2, spec OL.4.1). At 0 HP he yields: down on one knee, lantern set on the ground, still burning.
**Beat 5 — End of leg (`S05_choice`).** *Objective: Decide how Joss comes home.* `OL-D5`. Lucid fragments. The choice.
**Beat 6 — Home (`S06_home`).** *Objective: Return to the Lantern Post.* **Brought in:** Joss follows the player, but only once the player has spoken the closing call (`OL_CALL_KNOWN`, always learnable at C) and he puts out his own lantern. Escort along E; the drift pockets stay asleep with no lit lantern passing. **Lantern only:** the player carries the lantern (carry-state, lit; it won't go out). The two drift pockets on E wake as it passes (E3). Joss stays on the bend and walks on into the dark.
**Beat 7 — The book (`S07_book`).** *Objective: Speak with Ansel.* `OL-D7`. Ansel writes the entry. Quest Completed; Old Lantern's bend → **quieted**.

### OL.4 Encounters

| Id | Enemies | Where | Role | Telegraph | Solo target |
|---|---|---|---|---|---|
| **E1** | 2 lantern-drift | Near the shelter, once | Water Wraith (lantern-drift): place-bound, Aggressive near water; disperse on defeat | Drift brightens and leans (~1.2 s) before a cold lash | Required on first pass. 30–45 s. |
| **E2** | **Joss Garrow, "Old Lantern"** | The willow bend | Miniboss; spec below | — | Required. 3–4 minutes. |
| **E3** | 2 drift (one per pocket) | Return path | Wake only for a lit lantern passing (lantern-only branch) | Pocket surface shivers (~1.5 s) before the drift rises | Lantern-only branch. 30–45 s each. |

#### OL.4.1 Miniboss spec — Joss Garrow, "Old Lantern"

| Field | Spec |
|---|---|
| Family | Listed under Water Wraiths as their elite (bible §10), but **Joss is a living man**. He is never "dispersed"; at 0 HP he yields. |
| Read | A Watcher's coat gone green, beard to the chest, hands blue-grey with cold. A lantern on a hooked pole, burning steadily. A coil of blessed rope at his hip. He moves at a patrol walk, never a run. He speaks only patrol calls during the fight. |
| Arena | The bend (D). **Post footings** (4, raised stone): the count's pulse and the rope's drag do not reach a player standing on one. **The ford:** heavy water, slows movement. **Deep side:** behind reeds; not reachable during the fight. |
| Health target | Solo, Milestone 1 dependable to early Competent equipment: 3–4 minutes. Values belong to the Gameplay Designer. |
| **Lantern sweep** (all phases) | He raises the lantern high; a cone of light settles on the ground in front of him (**1.5 s**). Cold sweep through the cone: moderate damage. **If the cone touches the ford**, a lantern-drift forms where the light lay, 3 s later (max 2 alive). Fight him on the bank to stop the drift spawning. Cadence ~9 s. |
| **Rope cast** (all phases) | Bark *"Hold the line!"*; the rope uncoils and a pale line is drawn on the ground from him to the player (**1.5 s**). If the player is still on the line, the rope snares and drags them 3 m toward him. Break it by stepping onto a post footing or landing two hits (the True Line leech-latch rule). Cadence ~14 s. |
| **Count the stroke** (P2–P3) | He plants the pole and counts aloud, *"One... two... three"*, one count per second (**3 s**, the count is the tell). On "three" a cold pulse rings out from the ford, radius 7 m: heavy damage unless the player is on a post footing. Cadence ~18 s. *(Foreshadows the Muster's stroke-calls; it carries no information.)* |
| **Wade** (P3, below 25%) | Bark *"End of leg."*; he turns and walks toward the deep side across the ford. A ring marks a spot ahead of him on his path (**shown for the whole wade**). If the player stands in the ring, he stops, turns and fights on. If he reaches the reeds, he stands knee-deep at the edge and fights from there: sweeps always touch water, so drift keep forming until he is beaten. Never a fail; it only makes the end harder. Once per fight. |
| **Banner-thistle smoke** (player tool) | Once per phase the player can light Ansel's smoke at any post footing (2 s channel). For 10 s inside the cloud: lantern-drift take extra damage and Joss's sweep and rope are slower (+0.5 s on each tell). While he is in the cloud he speaks one lucid fragment (`OL-D4`). |
| Phases | P1 100–60%: sweep, rope. P2 60–25%: + count. P3 below 25%: + wade, count cadence ~14 s. No enrage. Never flees. |
| Yield | At 0 HP: down on one knee, lantern set down, still lit. Combat ends; `OL-D5` opens when the player approaches. |
| Reset | If the player leaves the bend or dies, Joss returns to his patrol walk at full health; drift spawned by him disperse. Step progress kept. |

### OL.5 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Ask Ansel about the lantern on the far leg. | `OL-D1` end node | Yes |
| `S01_track` | Follow the far leg. | 3 inspect events on notched posts, in order | Yes |
| `S01b_stubs` | (Optional) Look at the burned stubs. | 2 inspect events | No |
| `S02_shelter` | Search the reed shelter. | E1 defeated + inspect pages, tally pages, rope (sets `OL_CALL_KNOWN`) | Yes |
| `S03_watch` | Wait at the willow bend for the lantern. | Watch interaction to nightfall; enter 15 m volume around Joss | Yes |
| `S04_joss` | Stop Joss Garrow. | E2 yield event | Yes |
| `S05_choice` | Decide how Joss comes home. | `OL-D5` choice resolved | Yes |
| `S06_home` | Return to the Lantern Post. | Brought in: escort-arrival of Joss at the Post. Lantern only: carry-deposit of the lantern on the empty hook. | Yes |
| `S07_book` | Speak with Ansel. | `OL-D7` end node | Yes (→ Completed; drift site quieted) |

### OL.6 Flags

| Flag | Set by | Read by |
|---|---|---|
| `OL_STUBS_SEEN` | `S01b_stubs` | `OL-D7` line |
| `OL_CALL_KNOWN` | Shelter last page | `OL-D5` bring-in option |
| `OL_JOSS_IN` / `OL_LANTERN_ONLY` | `OL-D5` (exactly one) | `OL-D7`; MQ11 (Joss among Reedmere evacuees with Elspeth and no lantern hung, or the still-burning lantern on the Post hook); MQ12 Ansel line |
| drift site `old_lantern_bend` | Completion | → quieted **permanently, in every fen ending** (§0.2 contract) |

### OL.7 Choices and consequences

| Option | Immediate | Cost | Honoured how |
|---|---|---|---|
| **Bring him in** — *"Lantern in. Leg closed."* (requires `OL_CALL_KNOWN`) | Joss puts out his lantern and follows the player. Elspeth Quill comes to the Post and takes him into her care. | Joss is frightened indoors and may never be well. Ansel has to sit with the man he wrote off, every night he isn't walking. | Ansel strikes "lost on patrol" from the book and writes *"Joss Garrow. Came in."* Joss's hook stays empty because he is home. |
| **Bring back the lantern** — *"Keep walking. I'll carry the light in."* | Joss lets the pole go and walks on along the leg, unlit. The player carries the lantern home through two waking pockets. | Joss stays out there. On some dusks the player can see a man walking the far leg without a light. He never engages and never speaks. | The lantern is hung, still burning, on the empty hook above *J.G.* Ansel writes *"Joss Garrow. On patrol."* Watchers greet it at every change. |

The bend is quieted either way: the drift was gathering to the lantern, and it is no longer there. It **stays** quieted through MQ11 and under every fen ending (§0.2 contract); the two flags change only lines and props.

### OL.8 Rewards

Watcher standing in dialogue (Ansel and Watcher barks change; no reputation system). Ansel gives the player Joss's patrol book pages to keep or burn (flavour inspect only; no item). Small payment from the Post's box. Melee XP from actions. No lump XP.

### OL.9 Failure, recovery, co-op

No fail. Death respawns at the Lantern Post with steps and flags kept; Joss resets to full and his patrol. On the bring-in escort, Joss waits if the player stops and cannot be harmed. Logout during the escort restarts `S06` with Joss back at the bend, already yielded. In co-op, Joss is a shared world creature for the fight; each player's choice is their own, and a partner who chose differently sees their own outcome at the Post (per-player prop: lantern hung or hook empty; fallback: both presented by barks).

### OL.10 Integration needs

| Need | Minimum form | Fallback |
|---|---|---|
| Non-lethal yield for a boss | Defeat event → yield animation, no despawn | Joss "sits" on defeat, same event |
| Ground telegraphs (cone, line, ring) | Decal telegraphs with fixed durations | Bark plus a simple circle |
| Drift spawned from lit water | Spawn rule: cone overlapping ford volume | Fixed drift spawns at P2 start (2) |
| Path-blocking ring during wade | Volume check stops NPC path | Wade removed; P3 just adds faster count |
| Prop-conditioned drift pockets on return | Pocket wakes on lit-lantern carry state | Pockets always wake once |

### OL.11 Ledger, decisions, review

**Mystery ledger.** *What happened to Joss:* long exposure (canon). *Public belief:* "lost on patrol"; Brookhollow says "a drift took him". *Player-observable:* the pages, the tallies, a lantern that burns dry, the count. *Wrong reading:* Joss knows what the drift is or who it was. He doesn't; he went in for the why and came back with a count. *Withheld:* what the count is counting (MQ11 owns the Muster; it identifies nobody).
**Open decision:** whether Joss can ever speak a full sentence again after `OL_JOSS_IN` is left to MQ12; recommend no recovery beyond fragments.

| Review finding | Revision |
|---|---|
| Draft's tally pages had "one for each of them". | Cut: implied counted dead. Tallies are unexplained strokes. |
| Draft let the player kill Joss. | He yields; both endings bring him or his light home. |
| Bring-in had no physical requirement. | The closing call is learned at the shelter and spoken to him. Always learnable, so there is no soft-lock. |
| Independent review pass: Act III kept the bend residual and hung a lantern regardless of choice. | Director ruling: completing OL quiets the bend permanently in all fen endings; contract and the lit/unlit lantern states made explicit in §0.2 (the old "unlit lantern" wording there was wrong). |

### OL.12 Dialogue

```
OL-D1.01 ANSEL: (open book) "You've seen it. 'Lantern on the far leg. Not ours.' Every second night."
OL-D1.02 ANSEL: "It's Joss. Joss Garrow. We walked that leg together, years. He wanted the why. I wanted my supper."
OL-D1.03 ANSEL: "One winter he went in after it. We wrote him 'lost on patrol'. It's what you write."
OL-D1.04 ANSEL: "Lantern still walks the leg. Same pace. Same stops."
  > "You never went after him?"                             → OL-D1.10
  > "I'll find him."                                         → OL-D1.20
OL-D1.10 ANSEL: "Twice. Got close enough to hear him call. My call." (beat) "Came back. I'm not proud of it."   → OL-D1 options
OL-D1.20 ANSEL: (hands over a thistle bundle) "Smoke. If he's what I think, it'll help." (beat) "If he's Joss, bring him in. If he isn't, bring the light."
      {event: S00_hook}
```

**Inspect texts:** *Notched post:* "A waymark notch, cut fresh over an old one. Same height, same angle as the Post's." / *Thistle stub:* "Banner-thistle, lit and stamped out. Recent." / *Pages:* "'Far leg. Heavy at the willow. Lantern lit.' The same words on every page." / *Tally pages:* "Strokes in fives. Pages of them. Nothing else." / *Last page:* "Written out in full, pressed hard: 'Lantern in. Leg closed.'" / *Rope:* "Blessed rope, worn smooth as a handrail." / *Lantern (after yield):* "The oil well is dry. Has been for a long time. The flame doesn't care."

```
OL-D3 — Approach bark (starts E2)
JOSS: "Lantern coming in! Wraithwatch." (raises the lantern toward the player) "Heavy at the willow. Hold the line."
```

```
OL-D4 — Lucid fragments (once each, while Joss is in the smoke)
OL-D4.01 JOSS: "...Ansel? No. Ansel's taller."
OL-D4.02 JOSS: "Don't stand in the water. I told him that. Don't stand in it."
OL-D4.03 JOSS: "Where and when. I wrote where and when."
```

```
OL-D5.01 JOSS: (on one knee, lantern on the ground) "End of leg." (beat) "End of leg?"
OL-D5.02 JOSS: "I went in for the why. There isn't one. There's a count. I kept it."
  > "Who taught you the count?"                             → OL-D5.10
  > "Ansel sent me."                                         → OL-D5.20
  > [OL_CALL_KNOWN] "Lantern in. Leg closed."               → OL-D5.30
  > "Keep walking. I'll carry the light in."                → OL-D5.40
OL-D5.10 JOSS: "Nobody. It's in the water. One, two, three." (looks at the ford) "It doesn't mean anyone. I listened."   → OL-D5 options
OL-D5.20 JOSS: "Ansel." (long pause) "He wanted his supper."   → OL-D5 options
OL-D5.30 JOSS: (repeats it, slowly, the way it's meant to be said) "Lantern in. Leg closed."
OL-D5.31 JOSS: (opens the lantern and pinches the flame; it goes out) (stands) "Which way's the Post. I forget, in the dark."
      {set OL_JOSS_IN}  {event: S05_choice; Joss follows}
OL-D5.40 JOSS: (lets the pole go into the player's hands) "Mind it. It's heavy at the willow."
OL-D5.41 JOSS: (turns and walks on along the leg, unlit) "Far leg. Lantern... out."
      {set OL_LANTERN_ONLY}  {event: S05_choice; give lantern (carry-state, lit)}
```

```
OL-D7.01 [OL_JOSS_IN] ELSPETH: (at the Post door, blanket ready) "Inside. Slowly. No, leave the coat, I'll wash it. Or burn it."
OL-D7.02 [OL_JOSS_IN] ANSEL: (looks at Joss for a long time) "...You're late."
OL-D7.03 [OL_JOSS_IN] JOSS: (sitting, not looking up) "Heavy at the willow."
OL-D7.04 [OL_JOSS_IN] ANSEL: (to the player, quietly, writing) "'Joss Garrow. Came in.'" (beat) "I've never been so glad of a line."
OL-D7.01 [OL_LANTERN_ONLY] ANSEL: (takes the pole; hangs the burning lantern on the empty hook, above J.G.) "It won't go out, will it."
OL-D7.02 [OL_LANTERN_ONLY] ANSEL: "Then it hangs here, and he walks the leg, and I'll walk it with him. From a little way off."
OL-D7.03 [OL_LANTERN_ONLY] ANSEL: (writing) "'Joss Garrow. On patrol.'" (beat) "It was always true. Now it's written right."
OL-D7.05 [OL_STUBS_SEEN] ANSEL: "Still lighting smoke out there. Still stamping it out after. Tidy man."
OL-D7.06 ANSEL: "The willow bend's quiet tonight. First time I've ever written that." (closes the book) "River keep you."
      {event: S07_book → quest Completed; drift site old_lantern_bend → quieted}
```

**Post-quest barks:** WATCHER [`OL_LANTERN_ONLY`], at the change: *"Lantern's in."* (to the hook) / ANSEL [`OL_JOSS_IN`]: *"He counts in his sleep. Elspeth says let him."* / (MQ11 hook) ANSEL during the Muster's stroke-calls: *"Joss counted like that. Don't listen to it. Watch your feet."*

---

## Package review summary

| Check | Result |
|---|---|
| Canon anchors | Maelin (NT), Aldric (NB), Lessa (FW) and Joric (UR) get no invented age, service, kin, travel or record custody. Joric's loss stays "a river incident never recorded". An Ivo line that gave Lessa a mother was cut. Tovin, Corvin and Annelise do not appear. |
| Evidence rule | Facts come only from records (ledger, toll book, Joss's pages), objects (repair faces, gatepost, bowls' maker's dot) and testimony. The drift, the level beads, the leaning reeds, the dry-burning lantern and Joss's count explain nothing and name no one. |
| Soft-locks | Every required step has a guaranteed path: four UL routes, a platform fallback in NB, a repeatable hold in FW, the closing call always learnable in OL, and no fail state anywhere. |
| Antagonist tagging | Sallow is absent and appears only in UL nodes and prose tagged `[ANTAGONIST]`. The ledger's "Provisioner's purse" line and the Board seal on its pay chits are tagged `[ANTAGONIST]`. Marrick is not named. |
| Quest items | **0.** All carried things are carry-state objects. |
| Flags | Quest-local prefixes only; no new `LM_` flags. Cross-package reads are listed in §0.2. |
| Duplicates | §0.4. NT has no investigation; NB and SB are distinct climbs. |
| Known conflict | Reed Stalkers are "first seen MQ5" in bible §10, but NB (after MQ2) is their first appearance for most players. NB caps them at 2 at once with long telegraphs; FW now unlocks after MQ5. Flagged to the Encounters package and the bible owner. |
| Independent review pass | Applied the independent side-content review and Director rulings 1, 2, 3, 4, 5 (see the entries in UL.11, NB.11, UR.11, FW.11 and OL.11). **UL:** the crew ledger is the MQ10 chip and shows who paid (the Provisioner's purse, Board-sealed pay chits `[ANTAGONIST]`); `UL_LEDGER_CUT` means torn pages; `UL_RHOSYN_GONE` is renamed **`UL_RHOSYN_FLED`**; post-MQ6 variants added; the offer window closes when MQ10 starts. **OL:** permanent quieting is now a contract in §0.2. **UR:** "Wenna Hale" is renamed **Tansy Marl**; E2 is now a goblin raiding party, not MQ3's den. **FW:** unlocks after MQ5, with a soft warning. **NB:** at most 2 stalkers at once and longer telegraphs, noted as the stalkers' first appearance. Flags with no reader in Act II or III are marked "(request)". **Rejected:** none of the review's findings for this file. Act III-side fixes (C8 re-key, the residual-pocket choice, the GL-E4b condition) belong to the main-act packages. |
