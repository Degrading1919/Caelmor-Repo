# Mire Side Quests — Settlements and Combat Challenges

**Status (2026-11-08):** Authored production content for Creative Director milestone review (Mire bible §12, Batch 3, part B). Four side-quest packages, ten micro-events and ten discoveries: two settlement stories (**MBO** *The Bell Roster*, **MRW** *The Returning Wage*), two combat challenges (**MNK** *Nine Stakes*, **MRH** *The Rust Hart*, a miniboss), micro-events **MME01–MME10** (bible §7.4) and discoveries **MDS01–MDS10** (bible §7.5). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[CANON]** items come from `LORE/`. **[APPROVED — id]** marks an approved architecture ruling. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. No schema, JSON or C#.

**Controlled by:** `Caelmor_Mire_Narrative_Production_Bible.md` (author truth §2, decisions §3, POIs §4.2, cast and voice §5, slate and contracts §7.2–7.5, revelation map §8, world state §9, encounter families §10, conventions §11). **Binding rulings:** `Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 to CDR-4). **Format:** `Caelmor_Thornfell_Side_Quests_Settlements_and_Combat.md` (which follows the Lowmark side-quest packages). **Dialogue** is inline in each package (§x.18), in the node format `NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`, with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>`, inspect texts `<CODE>-I<n>`. Mire voice rules (bible §5.3) bind every line.

**Read for coherence:** the Mire main packages `Caelmor_Mire_Main_Act_I.md`, `_II.md`, `_III.md` and their dialogue files (Act III reads `MDS07_READ` and *The Bell Roster* completion from this file; Act I and III present MME01, MME02, MME04, MME08 and MME10 in passing; Act II leaves MDS02 to this file); the sister file `Caelmor_Mire_Side_Quests_Work_and_Skills.md`.

**Scope guard.** The Mire is an internal production milestone of the complete game (CDR-3). Nothing here grows scope. Technical needs are listed for the Mire integration handoff (bible §12, Batch 4).

---

## 0. Slate header

### 0.1 The four quests at a glance

| Code | Quest | Type (Phase 1.5) | Unlock gate | Skill requirement | Where | Core verb (primary first) | Identity in one line | Feeds |
|---|---|---|---|---|---|---|---|---|
| **MBO** | The Bell Roster | Settlement (Griefwatch) | MR-M2 Completed | None | Griefwatch vigil hall and bell (MP03); the Dry Muster (MP24) | **audit**, cover, account | A missed bell blamed on an old man turns out to be a kindness nobody wrote down; the player rings a night, walks the muster round, and helps write a rule a stranger and a carer can both live with. | **Completion read by Act III** (`S00`, `S01`: Ide's line; the vigil book's fixed hand); `MBO_RULE` |
| **MRW** | The Returning Wage | Settlement (Rootrest) | MR-M3 Completed | None | Rootrest (MP04), its peat bank and the elder's yard | **haul**, mediate, accept | Bring in an old woman's peat beside the grandson home from Emberholt wage work, with the neighbours watching, then sit the table where his honesty makes it worse. | `MRW_TABLE` (barks only) |
| **MNK** | Nine Stakes | Combat challenge | MR-M1 Completed | None | Nine Stakes (MP21), the Field edge off the causeway | **read**, clear, re-stake | Raiders have pulled the stakes at a marked crossing to drown travellers who cross Sour; clear them and the Mud-Boss, then read the old sockets and make the crossing tell the truth again. | `MNK_NINTH` (barks; marker prop) |
| **MRH** | The Rust Hart | Combat challenge (**miniboss**) | MR-M2 Completed | **Hunting ~[GD: low-mid]** | The Rust Hollow (MP27), ironbloom ground at the Field edge | **track**, read, fight | A great tarnish stalker charges anything on two legs; its path is erratic but its stops are not, and a hunter who reads the ironbloom can be where it stops before it gets there. | `MRH_ANTLER` (barks; Rootrest bonecarver prop) |

**Recommended order of discovery** (not enforced): MNK opens with the causeway after MR-M1 and is the first combat challenge most players meet. MBO and MRH open after MR-M2; MBO is the natural first visit to Griefwatch before MR-M5. MRW opens after MR-M3, when Rootrest and the Fenward are already familiar.

### 0.2 Flags other packages read

| Flag or state | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| **MBO Completed** (quest state) | — | MBO `S07_book` | **Act III** `MBL-D1.03` (Ide: "Bell went on time. Roster's fixed. One thing in Griefwatch is."); the vigil book cover inspect variant | Flavour only. Completion is set at the moment the player and Ide write the rule into the vigil book, so the book's "fixed hand" exists whenever Act III reads it. Any `MBO_RULE` value satisfies Act III. |
| `MBO_RULE` | written / second / captain | MBO `S06_rule` | Griefwatch barks; vigil book inspect | Which substitute rule Griefwatch keeps. Act III does not need the value. |
| `MBO_RANG` | bool (always true on completion) | MBO `S04_ring` | Bell-keeper barks | The player rang a bell-night. |
| **`MDS07_READ`** | bool, persistent on the character | MDS07 reading (§6) | **Act III `S02`** (`MBL-D3.21`: "You've seen it. Then you know.") | Set when the furrow discovery's reading layer is completed. **Act III request:** the `S02` furrow inspect (`MBL-D3.20`) should also set `MDS07_SEEN` and `MDS07_READ` after its own line plays (§6, MDS07), so the post-story discovery does not repeat. |
| `MDS##_SEEN` / `MDS##_READ` | bool | Each discovery | That discovery's later presentation; MDS07_READ as above | Bible §11.2 naming. |
| `MME##_…` | per card | Each micro-event | The micro-event only, unless stated | — |
| `MRW_TABLE` | spoke / quiet / elder | MRW `S05_table` | Rootrest barks | How the player met Corwin's account at the table. |
| `MNK_NINTH` | bool (always true on completion) | MNK `S06_ninth` | Ferry household and Marshwarden barks; the ninth socket marker | The diversion socket is marked. |
| `MRH_ANTLER` | rootrest / hunter | MRH `S06_antlers` | Rootrest bonecarver prop; Annot's bark | Where the antlers went. |
| *(read)* `TH_STANDING` (Thornfell) | bool | Thornfell TF-M5 | MBO `MBO-D5.04` | One line from the visiting Ridge Warden. Never a gate. |
| *(read)* `MR_CHANNELS` | bool | MR-M1 | MNK, all stake inspects | Always true after MR-M1, which gates every quest here. |
| *(read)* `MR_BANNERS` | retired / restored | MR-M2 | MBO (one Corra bark at the vigil hall with `restored`) | Flavour. |
| *(read)* MRS Completed | — | sister file | MRH (one Annot line) | Flavour. |

No new `MR_` region flags are created. All quest-local flags use the quest code. "(request)" marks a line asked of another package that nothing depends on.

### 0.3 Shared rules for all four packages

- **Quest items: none.** The Mire's budget of four is spent by the milestones (bible §9.4). Everything carried is a carry-state object.
- **Three states only.** Inactive, Active, Completed. No quest fails or is abandoned. Walking away keeps the quest Active at its persisted step with a named resume hook. Choices are outcome flags with costs.
- **Death** respawns at the quest's named safe point with step and flags intact. **Logout** restores the last persisted step; completed channel segments persist; a dropped carry-state object returns to its source.
- **Every enemy is defeated at 0 HP** (CDR-1): Bog Hounds, Mud-Clad Raiders and their Mud-Boss, tarnish stalkers and the Rust Hart alike. No yield, flee, retreat, scatter or break-off. Defeated humans take the ordinary defeat presentation (no gore, no tied props, no dialogue afterwards); allies make one sober line at most. Animals can be harvested where the economy allows. Every encounter accepts melee or ranged (CDR-2); none requires ranged and none is trivialised by it. **No SX exception** is proposed (bible §3).
- **Evidence rule** (bible §11.3). Records (the vigil book, the bell roster board, the ferry book at Nine Stakes, the transferred list in Griefwatch's chest), objects (stakes, sockets, antlers, ironbloom) and living testimony carry every fact. **Combat never reveals evidence; no defeated enemy speaks.** The bell in the fog, the moss caps lighting, the hart's iron, and every discovery identify nobody and prove nothing.
- **Time and R08.** No calendar date or year appears anywhere. The past is dated by weather runs ("the night of the hail", "after the second fog") or bell-nights. No unit, side, army or casualty count is ever named or totalled (R08, FT-02).
- **Readable system** (bible §1.1). MNK is the slate's deepest use of channel stakes; MBO uses the vigil bell and lantern moss on a night round; MRH reads ironbloom; MRW reads peat.
- **Map.** Relative placement only; **MAP VERIFICATION REQUIRED** wherever geometry matters. No route or direction to another region (FT-03). Mirebone stays a ford (MDS10).
- **Voice.** Bible §5.3: plain, heavy, kind; seen then thought; nobody speaks for the dead; nobody calls anything magic; strangers are "traveller", MR-M1's witnesses say "witness".
- **MD-7 (Hollowfoot).** No Hollowfoot enemy appears anywhere in this file. No discovery or micro-event depicts Hollowfoot. Each quest carries an MD-7 swap note (all "no change").
- **`[CAUSEWAY]`.** MNK's hook and one MME line touch Oswin's causeway; tagged.

### 0.4 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| MBO | Compares a public roster board, the vigil book's bell-night lines and chalk marks on household doors; rings the bell on the watch turns; walks the muster round by lantern moss; writes a rule | MHG (weighs a store; custody of a key); MR-M5 `S01` (matches names in the vigil book: different column, different purpose) |
| MRW | Barrows and stacks peat in a herringbone rick; roofs a dry shed; sits a cold table | MFT (cooks for named people); MWS (repairs a row) |
| MNK | Reads a crossing from a rise; clears raider groups and a Mud-Boss in a reed island; carries and sets nine stakes by reading socket wear | MR-M1's stake lesson (read one stake); MR-M3 (read stakes from a boat) |
| MRH | Maps four stop sites by ironbloom colour and sign; predicts the next stop; fights a charging stag in an arena of red patches | Thornfell TGM (tracks prints in snow; silent arena); MRS (fowling) |

---

## MBO — The Bell Roster

### MBO.1 The quest in one paragraph

Griefwatch rings its vigil bell at each turn of the night, and has since the war; a bell-keeper's line goes in the vigil book for every bell-night. Three bells were missed this season, and the public roster board in the vigil hall says all three were Tibb Ormer's nights. Tibb is old, slow on the ladder, and the obvious person to blame; the hall would like him to step down. A visiting Thornfell Ridge Warden, wintering at Griefwatch, says the problem is not Tibb but that nobody can say who was meant to be at the rope. The player audits the board against the vigil book and the chalk marks the bell households keep on their own doors, and finds that neighbours have been quietly swapping nights to free Elin Copse, who cares for her bedridden father, and never fixed the board. One swap was counted twice, and on those nights everybody thought someone else had the rope. The player covers a bell-night themselves, ringing the turns and walking the round across the Dry Muster by lantern moss, where Bog Hounds hunt the old drill lines. Then Ide Larrow, the warden, Tibb and Elin sit at the vigil table to write a substitute rule, and the player helps them choose one.

**Remember:** the bell rope in your hands at the dead turn, and the whole of Griefwatch hearing it. **Want next:** to know what the gap in the Dry Muster's lines was for (MDS04).

### MBO.2 Selection record

| Candidate | Verdict |
|---|---|
| A. Catch whoever skipped the bell. | Rejected. Turns a kindness into a crime; the bible's pitch is a protective swap never written down. |
| B. A debate with the Ridge Warden. | Rejected. Talk-led resolution only in closing beats. |
| **C. Audit three records → find the double-counted swap → ring a night and walk the round → write a rule** | **Selected.** The audit is physical (boards, a book, doors), the cover is play (rope on the turns, a lantern round with a fight), and the ending is a choice about accountability with costs to someone each way. |

### MBO.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Griefwatch maintains vigil over the old battlefield; Ridge Wardens from Thornfell sometimes visit | Dossier §VII.3 | [CANON] |
| Ide Larrow, Marshwarden captain; treats a closure as a weight she carries | Bible §5.2; Act III cast | [NEW] |
| The vigil hall, vigil bell and rope; the vigil book (one line per bell-night since the war) | Act III §5.1 W2 | [NEW], consistent |
| The Dry Muster: old drill ground with a gap in the lines | Bible MP24; MDS04 | [NEW, Part 3] |
| Bog Hounds | Dossier §IX; bible §10 | [CANON] |
| Tibb Ormer, Elin and Aldous Copse, the swap chalk, the muster round | This package | [NEW] |

### MBO.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.bell_roster` |
| Type | Settlement, Griefwatch (bible §7.2) |
| Unlock | MR-M2 Completed. Offered in the vigil hall by Ide Larrow (`MBO-D1`) after the bark `MBO-B0` at the closure gate on first entering Griefwatch. |
| Resume hook | Ide at the vigil table: `MBO-D1.00` "Roster's still wrong. Where were we?" |
| Target length | 30–40 minutes |
| Combat share | ~15% (Bog Hounds on the muster round) |
| Skills | Melee or Ranged; no skill check |
| Choice | The substitute rule (3 options) |
| Outputs | MBO Completed; `MBO_RULE` = written / second / captain; `MBO_RANG` |
| **Anchor** | Griefwatch (Ide Larrow; the bell households) |
| **World-truth row** | None (present-day). |
| **Revelation role** | Self-contained. The muster round passes MDS04 (no reading required). |
| **Recurring evidence** | None. The vigil book recurs in MR-M5 as a different column (bell-night lines of the war years); MBO touches only this season's keeper column. |
| **State compliance** | Inactive / Active / Completed; `MBO_RULE`; no fail; a missed rope turn is rung late with a bark; the round always completes. |
| **Combat compliance** | Bog Hounds (MBO-E1) to 0 HP; melee or ranged; no SX. |

### MBO.5 The places [MAP VERIFICATION REQUIRED]

Griefwatch sits at the foot of Bannerline Ridge (Act III §5). The Dry Muster is an old drill ground on the flat beside Griefwatch, short of the Bannerline road's closure gate (relative only).

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **W1. The closure gate** (Act III) | Bark | Marshwardens in oilcloth; the gate open at this point in the story (MR-M5 not begun). |
| **W2. The vigil hall** (Act III) | Hook; audit; rule | Stone footings, the bell rope through the roof, the long table, the **vigil book** on a stand. On the wall, the **roster board**: pegged reed strips, one per bell household, set against bell-nights. With `MR_BANNERS = restored`, the Banner That Sank Twice over the door. |
| **W4. The bell households' row** | Door chalk | Six houses along Griefwatch's main way. Each bell household chalks a mark on its door lintel when it takes a night: a stroke for its own night, a crossed stroke for a night taken for someone. |
| **W5. The Copse house** | Elin | A low house with a bed by the hearth; Aldous Copse in it; Elin on a stool. |
| **W6. Tibb's bench** | Tibb | A bench at the foot of the bell ladder where Tibb sits most evenings. |
| **D1. The Dry Muster** (MP24) | Round; MBO-E1 | Old drill lines worn into the peat as long straight furrows, with a **gap** in them (MDS04). **Lantern-moss posts** at the corners of the round; the bell-keeper wets each with a dipper and checks it lights. A round-post at the far end with a small hand bell. |

### MBO.6 Player-facing sequence

**Beat 0 — Missed Bells (`S00_offer`).** *Objective: Hear what the vigil hall wants.* `MBO-D1`. Ide states it flat: three missed bells this season; the board says Tibb; the hall wants him to step down; the visiting Ridge Warden says that is the wrong question. Ide wants it looked at by "somebody who isn't anybody's neighbour".

**Beat 1 — Three Records (`S01_audit`).** *Objective: Compare the roster board, the vigil book and the doors.* Any order:

- **The roster board** (W2, inspect): the three missed nights are Tibb's strips.
- **The vigil book** (W2, open to this season): the keeper column has a line for every bell-night. On three nights, the line reads only *"No bell."* in Ide's hand. The book dates nights by weather: *"Hail."* *"First frost."* *"Fog, second night."* (`MBO-I2`). On the nights either side of each, the keeper's line is in **Elin's** hand or a neighbour's, not Tibb's.
- **The doors** (W4, six lintel inspects): crossed strokes on four doors around each missed night; Tibb's lintel has a crossed stroke *for* Elin before each missed night and a plain stroke missing on the missed night itself.

When all three are read, the player can lay it out to Ide (`MBO-D2`, show-evidence dialogue gated on the inspects): the neighbours took Elin's nights to free her for her father; Tibb took one of Elin's, and gave his own to the Brack household; the Bracks thought they had given theirs away too. On three nights the swap was counted twice. Nobody was at the rope, and everybody thought someone was.

**Beat 2 — Tibb and Elin (`S02_people`).** *Objective: Talk to Tibb and to Elin.* `MBO-D3` (Tibb at his bench: he knew, said nothing, "because then they'd ask Elin why, and she'd have to say it in front of the hall") and `MBO-D4` (Elin at her father's bed: she did not ask anyone; they just started doing it). Required: both.

**Beat 3 — Tonight Is Short (`S03_tonight`).** *Objective: Take tonight's bell.* Tonight is one of the unfixed nights: the board says Tibb, the doors say the Bracks, and the Bracks have the fever (a bark at their door). Ide: "Then the witness rings it." (Or "the traveller", by address rule.)

**Beat 4 — The Rope (`S04_ring`).** *Objective: Ring the bell at each turn of the night.* Keep watch at Tibb's bench; at each of the night's three turns (dusk, the dead turn, before first light), climb the ladder and pull the rope (channelled, ~3 s; three pulls). A late pull is rung late with a bark from below ("Late's still a bell."). Between the first and second turn, the round (Beat 5). Sets `MBO_RANG` after the third. Strange moment on the second turn (MBO.8).

**Beat 5 — The Muster Round (`S05_round`).** *Objective: Walk the muster round and light the posts.* After the dusk bell, take the keeper's dipper and lantern (carry-state) and walk the round across the Dry Muster: four lantern-moss posts at the corners. At each, wet the moss from the dipper (interaction ~2 s); it lights (lantern-moss rule: wet moss glows). A dark post with a dry foot is the sign it has not been kept (bible §1.1). At the far post, ring the hand bell (interaction). **MBO-E1:** Bog Hounds hunting along the drill furrows. Walking past the **gap** in the lines shows MDS04's surface (`MDS04_SEEN`); its reading is not required here.

**Beat 6 — The Rule (`S06_rule`).** *Objective: Help the vigil hall write a substitute rule.* Morning, the vigil table: Ide, Tibb, Elin, a Brack, and the Ridge Warden. `MBO-D5`. MBO.11. Sets `MBO_RULE`.

**Beat 7 — The Book (`S07_book`).** *Objective: Write the rule in the vigil book.* Ide writes the rule in the keeper column's head, and the player writes last night's line (interaction: *"Bell rung. The witness."* / *"The traveller."*). From here the keeper column is in the fixed form (the "fixed hand" Act III reads). `MBO-D6`. **Quest Completed.**

### MBO.7 Encounters

Tuned for MR-M2's Competent identity (MD-10).

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MBO-E1** | 3 × Bog Hound (runner), 1 × Bog Hound (gnawer) | The Dry Muster's drill furrows (D1), between the second and third posts | Runners run the furrows in a line and break out to flank; the gnawer holds the furrow ahead of the player | **Runner dart:** head drops, hackles lift (~0.8 s), then a short lunge. **Furrow run:** the pack's lead runner barks once (~1.0 s) and the line runs the furrow toward the player. **Gnawer bite:** stands square, lips back (~1.0 s), heavy bite with a short bleed | Required (they hold the round). Furrows are straight lanes: ranged players can shoot down a furrow; melee players step across the furrow lip and catch runners as they break out | 50–70 s |

**Rules.** Hounds to 0 HP (CDR-1). Combat drops nothing that advances the audit. **Death:** respawn at Tibb's bench; posts already lit stay lit; bell turns already rung stay rung; the hounds reset.

### MBO.8 The strange moment: the bell in the fog (presentation spec)

| Time | Element | Spec |
|---|---|---|
| The dead turn | **The pull** | The player pulls the rope at the dead turn. Fog has come down over Griefwatch. |
| 0–3 s | **The bell** | The bell rings; the sound goes out into the fog and does not come back as an echo. |
| 3–8 s | **The answers** | One by one, lights come on in windows along the row (lamps lit in answer, as households do at the dead turn; Tibb's habit, he tells the player later). Then, far off, out past the ridge's foot, one more small light comes on where there is no house the player knows of. |
| 8–12 s | **Out** | The far light goes out. The row's lamps stay. |
| After | Tibb, if asked (`MBO-D3.20`) | "That one. Bran's, maybe. He's up there. Or it's somebody's lantern on the road. I've seen it forty years. I've never gone to look." |
| Meaning | None stated. Probably Bran Hollowstep's watchpost (Act III), probably not. It proves nothing. |

### MBO.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Hear what the vigil hall wants. | `MBO-D1` accept | Yes |
| `S01_audit` | Compare the roster board, the vigil book and the doors. | Board + book + 6 lintel inspects + `MBO-D2` show-evidence end | Yes |
| `S02_people` | Talk to Tibb and to Elin. | `MBO-D3` + `MBO-D4` end nodes | Yes |
| `S03_tonight` | Take tonight's bell. | `MBO-D4b` (Ide) end | Yes |
| `S04_ring` | Ring the bell at each turn of the night. | 3 rope pulls at the three turns (keep watch between) | Yes |
| `S05_round` | Walk the muster round and light the posts. | 4 posts lit + far hand bell + MBO-E1 defeated | Yes (between turns 1 and 2) |
| `S06_rule` | Help the vigil hall write a substitute rule. | `MBO-D5` choice | Yes |
| `S07_book` | Write the rule in the vigil book. | Book interaction + `MBO-D6` end | Yes (→ **Completed**) |

### MBO.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `MBO_RANG` | `S04` | Bell-keeper barks |
| `MBO_RULE` = written / second / captain | `S06` | Barks; vigil book inspect |
| *(state)* MBO Completed | `S07` | Act III `MBL-D1.03`; vigil book cover inspect |
| *(set in passing)* `MDS04_SEEN` | `S05` gap pass-by | MDS04 |

### MBO.11 Choices and consequences — the rule

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Swaps in the book** (`written`) — *"Swap all you like. Both of you write it in the book before dusk."* (the Ridge Warden's accountable rule, adapted) | Any swap is a line in the vigil book in both hands before the night. Elin's neighbours go on covering her. | Elin's arrangement is now written where the hall can read it. She says she can live with that. Some households stop offering, because writing it makes it a favour. | Barks: households at the book at dusk. The warden approves in one line. |
| **A named second** (`second`) — *"Every night has a second. If the first doesn't ring, the second does."* (two holds for a bell) | Each bell-night has two strips on the board. | Every household rings more nights. Tibb is second most often. Nobody's swap is written; Elin's stays private. | Barks: seconds grumbling, bells always on time. |
| **The captain keeps it** (`captain`) — *"Ide sets the roster. No swaps."* | Ide assigns every night; no swaps allowed. | Elin must ask Ide out loud for nights off; Ide grants them, and Elin hates asking. The neighbours' kindness has nowhere to go. Ide: "It's a weight. I'll carry it." | Ide's strips on the board, one hand. Barks: Elin's thanks, stiff. |

**All three:** Tibb is not put off the roster; the three missed nights are written as *"No bell. Roster wrong, not the keeper."* in the book; the bells are on time afterwards. Act III's line holds for every value.

### MBO.12 Rewards and unlocks

Small payment from the vigil hall's box; the vigil bell as a world interaction (the player may ring at any turn after completion, a bark answers); Griefwatch households' greeting ("bell-ringer"). Melee or Ranged XP from actions. No lump XP.

### MBO.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Walking away | Stays Active; resume at Ide. |
| Misses a turn (walks off mid-night) | The step keeps the turns rung; the next keep watch at the bench returns to the missed turn ("Late's still a bell."). |
| Death on the round | Respawn at Tibb's bench; lit posts stay lit. |
| Logout mid-night | Resumes at the bench at the next unrung turn. |
| Co-op | Per-player audit and choice; one player rings per instance (each in their own instance); hounds shared. |

### MBO.14 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Bell rope interaction at keep-watch turns | Systems | Channelled interaction available only at the three night turns (presentation hour). |
| Lantern-moss posts wetted to light | Systems / VFX | Two-state post prop (dark / lit) toggled by the dipper interaction. Same prop as MR-M1's lit line. |
| Show-evidence gated on inspects | Systems | Standard dialogue option gate (bible §11.1). |
| Answering lamps and the far light | VFX | Scripted window lights on the dead-turn pull; one distant light event. |
| Roster board and vigil book variants | Art / Systems | Board strips by `MBO_RULE`; book page variants before and after `S07`. |

### MBO.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | The far light is not decided. It may be Bran's watchpost. |
| Public belief | "Somebody answers." |
| Observable | One far light at the dead turn, in fog. |
| Wrong reading | The dead answer the bell. (Nobody speaks for the dead.) |
| Withheld | What it is. |

### MBO.16 Open decisions

1. The Ridge Warden is a role (no name), consistent with Act III's role-named pair. If the Director wants a named Thornfell visitor, only `MBO-D` speaker labels change.
2. "Bell-nights" in the vigil book are dated by weather; the keeper column never carries a date. Act III's `S08` line ("Ysolde writes ... the date") is outside this file; flagged to the Act III author as a possible conflict with the brief's no-calendar rule.

### MBO.17 Internal review log

| Check | Result |
|---|---|
| Tibb as scapegoat | He is never punished; every outcome writes "roster wrong, not the keeper". |
| Elin's dignity | She never asked for the swaps; her care is never made a confession. |
| Ridge Warden | Never says where he came from or how; one line with `TH_STANDING`; Thornfell understatement. |
| Act III read | Completion set at `S07` alongside the book's fixed keeper column. Any `MBO_RULE` satisfies `MBL-D1.03`. |
| Evidence rule | Board, book and doors; the hounds carry nothing. |
| MD-7 swap note | No Hollowfoot content. No change under either ruling. |

### MBO.18 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Ide Larrow** [NEW, bible §5.2] | The bell, the board, the book; that the hall wants Tibb off. | About the swaps. | Clipped; counts people; a closure or a rule is a weight she carries. |
| **Tibb Ormer** [NEW], old bell volunteer | The swaps; that he gave his night away. | That the Bracks gave theirs too. | Slow, mild, stubbornly loyal; "I'll not say it in front of the hall." |
| **Elin Copse** [NEW], carer | That neighbours took her nights. | How they arranged it. | Tired, proud, embarrassed by kindness. |
| **Aldous Copse** [NEW] | — | — | Bedridden; one line, dry. |
| **Visiting Ridge Warden** (role) [CANON visits] | How Wardens keep a watch roster. | Mire households. | Thornfell understatement; calls the player "walker"; never says where they came from or how. |
| **Brack household** (role) | That they gave their night away. | That Tibb gave his to them. | Coughing; fever. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `MBO-B0` | MARSHWARDEN | Closure gate, MR-M2 done, first visit | "Ide wants somebody who isn't anybody's cousin. That's you, by the look." |
| `MBO-B1` | BRACK (through the door, coughing) | Beat 3 | "We've the fever. We gave tonight away anyway. To Tibb. Didn't we?" |
| `MBO-B2` | TIBB (from below) | Late pull | "Late's still a bell." |
| `MBO-B3` | TIBB | Post lit on the round (seen from the ladder) | "There's your corner. Three more." |
| `MBO-B4` | CORRA SALLIS | `MR_BANNERS = restored`, vigil hall | "That's the Banner That Sank Twice. Over the door. For whoever." |
| `MBO-B5` | BELL HOUSEHOLD | Post-quest, `written` | "Swapped with Wendle. Wrote it. Both of us. Like the warden said." |
| `MBO-B6` | TIBB | Post-quest, `second` | "Second again. I like being second. Nobody blames the second." |
| `MBO-B7` | ELIN | Post-quest, `captain` | "Asked Ide for the next night after the hail." (beat) "Gave it me. Still hate asking." |
| `MBO-B8` | ANY GRIEFWATCH HOUSEHOLD | Post-quest | "Bell-ringer." (a nod) |

#### Nodes

```
MBO-D1.00 [quest Active, returning] IDE: "Roster's still wrong. Where were we?" (pins step)  → end
MBO-D1.01 IDE: "Three missed bells this season. Board says Tibb's nights, all three."
MBO-D1.02 IDE: "Hall wants him off the rope. He's old. He's slow on the ladder. It's tidy."
MBO-D1.03 WARDEN: (at the hearth, not getting up) "Tidy's not the question. Can anybody say who was meant to be on the rope? Not who's on the board. Who was meant."
MBO-D1.04 IDE: "The warden thinks we don't know who keeps our own bell." (beat) "I think the warden might be right. I don't like it."
  > "What do you want me to do?"                                     → MBO-D1.05
  > "Why ask a stranger?"                                            → MBO-D1.07
MBO-D1.05 IDE: "Look at the board, the book and the doors. Bell households chalk their lintels when they take a night. Tell me what you find. Not what you think."   {event: accept → S01_audit}  → end
MBO-D1.07 IDE: "Because everyone in Griefwatch is somebody's neighbour, and neighbours have reasons." (beat) "Board, book, doors."   {event: accept}  → end
```

```
MBO-D2.01 IDE: "Well?"
  > [all three read] "The neighbours have been taking Elin Copse's nights. Tibb took one and gave his own to the Bracks. The Bracks thought they'd given theirs away too."   → MBO-D2.02
  > "I haven't finished."                                            → end
MBO-D2.02 IDE: (looks at the board a long time) "Counted twice."
MBO-D2.03 IDE: "So on those nights everybody thought somebody had the rope."
MBO-D2.04 WARDEN: "That's the question answered."
MBO-D2.05 IDE: "Talk to Tibb. And Elin. I'll not have it said I decided without them."   {event: S01 complete}  → end
```

```
MBO-D3.01 TIBB: (on his bench) "You've been at the doors. I saw you."
MBO-D3.02 TIBB: "I knew. Course I knew. I'd given my night to the Bracks so I could take Elin's."
MBO-D3.03 TIBB: "If I'd said, they'd have asked Elin why she needed it. She'd have had to say it in front of the hall." (beat) "I'll not have that."
  > "They want you off the rope."                                    → MBO-D3.04
  > "Do you want to stop?"                                           → MBO-D3.06
MBO-D3.04 TIBB: "Then they can have me off. I'm slow on the ladder. It's true."   → MBO-D3.08
MBO-D3.06 TIBB: "No. I want to ring it till I can't climb it." (beat) "That's soon. Not yet."   → MBO-D3.08
MBO-D3.08 TIBB: "Bell's the only thing in Griefwatch everyone hears. You ring it, you're talking to all of them at once."   → end
MBO-D3.20 [after S04] TIBB: "That one. Bran's, maybe. He's up there. Or it's somebody's lantern on the road." (beat) "I've seen it forty years. I've never gone to look."   → end
```

```
MBO-D4.01 ELIN: (stool by the bed) "Sit. There's tea. It's cold."
MBO-D4.02 ELIN: "I didn't ask anybody. They just started. A stroke on a door I didn't make. Then another."
MBO-D4.03 ALDOUS: (from the bed, eyes shut) "She'd have rung it and left me. She'd have run there and back. She'd have been late."
MBO-D4.04 ELIN: "Father."
  > "Do you want it written down?"                                   → MBO-D4.05
  > "They did it because they wanted to."                            → MBO-D4.07
MBO-D4.05 ELIN: "No." (beat) "Yes. If it stops Tibb being blamed. Then yes."   → end
MBO-D4.07 ELIN: "I know. That's what's hard."   → end

MBO-D4b.01 IDE: (at the bench, after both) "Tonight's one of the wrong ones. Board says Tibb. The Bracks' door says Bracks. Bracks have the fever."
MBO-D4b.02 IDE: [witness] "Then the witness rings it." / [else] "Then the traveller rings it."
MBO-D4b.03 IDE: "Three turns. Dusk, the dead turn, before first light. Round the muster after the first: light the corners, ring the far post."   {event: S03 complete}  → end
```

```
MBO-D5.01 IDE: "Rule, then. Something the board can't get wrong."
MBO-D5.02 WARDEN: "On our watches every change is written by both before the watch. Then nobody wonders."
MBO-D5.03 ELIN: "Then everyone reads my name every night I can't."
MBO-D5.04 [TH_STANDING] WARDEN: "We keep accounts of who closed what and when, back home. Better written than wondered." (beat) "Learned that the hard way."
MBO-D5.05 TIBB: "Or every night has two. Like Ysolde's names. Two holds. If one doesn't ring, the other does."
MBO-D5.06 IDE: "Or I set it and nobody swaps."
MBO-D5.07 IDE: (to the player) "You looked. Say."
  > "Swap all you like. Both of you write it in the book before dusk."   → MBO-D5.10
  > "Every night has a second. If the first doesn't ring, the second does."   → MBO-D5.20
  > "Ide sets the roster. No swaps."                                 → MBO-D5.30
MBO-D5.10 ELIN: "Written." (beat) "All right. I can live with written."
MBO-D5.11 WARDEN: "Good." (that is all)
      {set MBO_RULE = written}  → MBO-D5.40
MBO-D5.20 TIBB: "I'll be second. I'm good at second."
MBO-D5.21 IDE: "Everyone rings more." / BRACK (coughing): "Fine."
      {set MBO_RULE = second}  → MBO-D5.40
MBO-D5.30 IDE: "Then it's mine." (beat) "It's a weight. I'll carry it."
MBO-D5.31 ELIN: "And I ask you. Out loud." / IDE: "And I say yes."
      {set MBO_RULE = captain}  → MBO-D5.40
MBO-D5.40 IDE: "Book."   {event: S06 complete}  → end
```

```
MBO-D6.01 IDE: (writing at the head of the keeper column) "Rule's in."
MBO-D6.02 IDE: "And the three: 'No bell. Roster wrong, not the keeper.'" (looks at Tibb) "That's the record."
MBO-D6.03 TIBB: "...Thank you, captain."
MBO-D6.04 IDE: (turns the book to the player) "Last night's line. Yours."
      {book interaction: "Bell rung. The witness." / "Bell rung. The traveller."}
MBO-D6.05 IDE: (pays from the hall's box) "Bell went on time. Write that somewhere too."
      {event: MBO-D6 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `MBO-I1` | Roster board | "Reed strips pegged against bell-nights. Three of Tibb's strips have a black peg: missed." |
| `MBO-I2` | Vigil book, this season | "One line a bell-night. 'Hail. No bell.' 'First frost. No bell.' 'Fog, second night. No bell.' Ide's hand. Either side, Elin's hand, or a neighbour's." |
| `MBO-I3` | Lintel chalk (Tibb) | "A crossed stroke the night before each missed night. No stroke on the night itself." |
| `MBO-I4` | Lintel chalk (Brack) | "Crossed strokes: a night given away. The same nights." |
| `MBO-I5` | Lintel chalk (others) | "Crossed strokes, here and there, round Elin's nights." |
| `MBO-I6` | Lantern-moss post (dark) | "Dry at the foot. Nobody's kept it tonight." / lit: "Wet. Glowing." |
| `MBO-I7` | Vigil book (after) | "The keeper column's head carries a rule now, in Ide's hand. The lines below are in the fixed form." |

---

## MRW — The Returning Wage

### MRW.1 The quest in one paragraph

Corwin Tey left Rootrest as a young man to do wage work in Emberholt's yards, and came home this autumn because his grandmother Hessel can no longer bring in her own peat. He is strong, he works fast, and he is useful in a place that is short of hands, and Rootrest does not know what to do with him. The neighbours bring Hessel soup and do not look at him. The player helps him get Hessel's peat stack in from the cutting bank before the wet closes the plank way: barrowing turves while the neighbours watch from their doors, building a proper herringbone rick, and roofing Hessel's dry shed, where Corwin's Emberholt habit (tarred cloth) and Rootrest's (reed thatch) argue on the roof. The stack goes in. Then Hessel sets a table and asks the neighbours to it, and Corwin, asked straight out about the war, answers straight: in Emberholt they don't talk about the war, they talk about output, and he liked that, and the wage came every week on time. The table goes cold. Nothing the player says fixes it. One neighbour passes him the bread anyway.

**Remember:** the bone chimes silent all evening in a moving wind, and ringing once as the bread goes across. **Want next:** nothing resolved; that is the point.

### MRW.2 Selection record

| Candidate | Verdict |
|---|---|
| A. Prove he is a good man. | Rejected. Absolution of the war is out of bounds (bible §7.2: "no absolution"). |
| B. Expose him as a spy. | Rejected. Caricature (voice rule 10); no Remnant (bible §7.2). |
| **C. Work beside him in public → a table where honesty makes it worse → no fix** | **Selected.** Braid 11's shape (a returning worker useful and suspect); the player's tool is work and presence, not a verdict. |

### MRW.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Rootrest: root-sheltered homes, herbalists, bonecarvers; soil feels "lighter" | Dossier §VII.4 | [CANON] |
| Emberholt resented rationally (war escalation, peat and timber fears), never caricatured | Bible §5.3 rule 10 | Binding |
| Returning worker, useful and suspect (braid 11 shape) | Part 4 relationship web; bible §7.2 | Proposal adopted |
| Corwin and Hessel Tey, Gilly Ruddle, the bone chimes | This package | [NEW] |

### MRW.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.returning_wage` |
| Type | Settlement, Rootrest (bible §7.2) |
| Unlock | MR-M3 Completed. Offered by Gilly Ruddle, Hessel's neighbour, at the root arch (`MRW-D1`). |
| Resume hook | Gilly at her door: `MRW-D1.00` "Stack's still out. Where were we?" |
| Target length | 30–40 minutes |
| Combat share | 0% |
| Skills | None required (carry, stack and roof are interactions) |
| Choice | How the player meets Corwin's account at the table (flavour flag `MRW_TABLE`) |
| **Anchor** | Rootrest households |
| **World-truth row** | H23 (uneven recovery; who is owed welcome). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed; no fail; the rick can be restacked; the table always ends. |
| **Combat compliance** | None. |
| **Cross-region** | Emberholt: one person; no absolution of the war; no route stated; no Remnant; no Glassed Hollow. |

### MRW.5 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **R1. The root arch** | Hook | A path through the roots of great old trees, burned and re-grown. Bone chimes hang from the roots. |
| **R2. Hessel's yard** | Rick; shed | A small root-sheltered house, a dry shed with half a roof, an empty rick base of flat stones. |
| **R3. The plank way** | Barrow route | Planks over wet ground between the yard and the cutting bank; the neighbours' doors face it. A stake at its low point. |
| **R4. The cutting bank** | Turves | Hessel's cut peat drying in footed stacks. |
| **R5. Hessel's table** | The table | Indoors, one table, a hearth, more chairs borrowed than owned. |

### MRW.6 Player-facing sequence

**Beat 0 — Hands (`S00_offer`).** *Objective: Hear out Hessel's neighbour.* `MRW-D1`. Gilly: Hessel's peat is still on the bank; the plank way goes under when the wet comes; Corwin is doing it alone because nobody will work beside him. "I'll not. I can't say why that's fair. I'll not anyway."

**Beat 1 — Beside Him (`S01_meet`).** *Objective: Talk to Corwin.* `MRW-D2`. Corwin is polite, quick and tired of being looked at.

**Beat 2 — The Stack (`S02_haul`).** *Objective: Bring the turves in (0/4 loads).* Keep watch if the plank way's stake reads Sour (the low planks are under; Slack or Running both pass). Load a barrow at the bank (interaction), wheel it along the plank way (carry-state; slower), tip at the rick base. Four loads; Corwin does four alongside. On each run a neighbour line from a door (`MRW-B1`), one per house; they speak to the player, never to Corwin.

**Beat 3 — The Rick (`S03_rick`).** *Objective: Build the rick.* Herringbone stacking: lay turves in courses, each course angled against the last, with a ridge at the top to shed water. An interaction sequence on the rick (six courses; each course is one interaction choosing **left lean** or **right lean**; the correct answer alternates and the rick shows the pattern). A wrong lean shows the turves sliding (~1 s) and the course resets. Corwin shows the first two.

**Beat 4 — The Roof (`S04_roof`).** *Objective: Roof the dry shed.* Corwin wants to use tarred cloth (he brought a roll back from the yards); Hessel's neighbours say reed thatch, as Rootrest has always done. The player chooses which (`MRW-D3`): **tar cloth** (two interactions; quick; Gilly mutters "Emberholt pitch"), or **reed thatch** (four interactions with reed bundles from Gilly's own store, which she gives the player, not Corwin). Either roofs the shed. Flavour only; nothing changes later but one bark.

**Beat 5 — The Table (`S05_table`).** *Objective: Sit at Hessel's table.* Food first. Then Gilly asks Corwin about the war, straight out. He answers straight (`MRW-D4`). The table goes cold. The player may speak for his work, say nothing, or turn to Hessel. Sets `MRW_TABLE`. Then the bread (MRW.8).

**Beat 6 — Out (`S06_close`).** *Objective: Leave Hessel's house.* `MRW-D5` at the door with Corwin. Quest Completed.

### MRW.7 Encounters

None.

### MRW.8 The strange moment: the bone chimes (presentation spec)

| Time | Element | Spec |
|---|---|---|
| All evening | **Silent** | The bone chimes on the roots over Hessel's door hang still. The reeds beyond the door move in the wind, visibly, all evening. The chimes make no sound. (Ambient: wind in reeds, no chime.) |
| The bread | **Across** | Gilly, after a long cold quiet, takes the loaf and passes it to Corwin without looking at him. |
| At the hand-over | **Once** | The chimes ring once, a short dry clatter, then hang still again. |
| After | Hessel | "Wind." (`MRW-D4.40`) |
| Meaning | None stated. Proves nothing about Corwin, Gilly or anyone. |

### MRW.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Hear out Hessel's neighbour. | `MRW-D1` accept | Yes |
| `S01_meet` | Talk to Corwin. | `MRW-D2` end | Yes |
| `S02_haul` | Bring the turves in. | 4 barrow loads tipped | Yes |
| `S03_rick` | Build the rick. | 6 courses correct | Yes |
| `S04_roof` | Roof the dry shed. | Tar (2) or thatch (4) interactions | Yes (`MRW_ROOF` = tar / thatch) |
| `S05_table` | Sit at Hessel's table. | Sit + `MRW-D4` end | Yes (`MRW_TABLE`) |
| `S06_close` | Leave Hessel's house. | `MRW-D5` end | Yes (→ Completed) |

### MRW.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `MRW_ROOF` = tar / thatch | `S04` | Shed prop; one Gilly bark |
| `MRW_TABLE` = spoke / quiet / elder | `S05` | Rootrest barks |

### MRW.11 Choices and consequences — the table

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **Speak for his work** (`spoke`) — *"He brought the stack in. I saw it."* | Gilly: "I saw it too. That's not what I asked." | The player is now counted on his side, a little. | Corwin: "You didn't have to." |
| **Say nothing** (`quiet`) | The silence goes on until Gilly breaks it with the bread. | None visible. | Corwin: "Thanks for not." |
| **Turn to Hessel** (`elder`) — *"Hessel, it's your table."* | Hessel: "He came back. I don't need it to be more than that." | Hessel has to say it in front of them. | Hessel's bark at her door afterwards. |

In every outcome, Gilly passes the bread; nobody forgives anything; the stack is in.

### MRW.12 Rewards and unlocks

Hessel's thanks and a pot of rootcraft balm (a consumable from the item pass, or none); small payment from Corwin's wage ("Emberholt coin spends the same."). No lump XP.

### MRW.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Plank way at Sour | Keep watch; the bank waits. |
| Wrong lean | Course resets. |
| Walking away | Stays Active; resume at Gilly. |
| Logout with a barrow | The load returns to the bank. |
| Co-op | Per-player; NPC table placement follows the host. |

### MRW.14 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Barrow carry-state on a plank route | Systems | Carry-state with slowed movement. |
| Rick course sequence | Systems | Interaction sequence with harmless reset (bible §11.1). |
| Silent chimes, one ring | Audio | Chime emitter muted for the scene; one scripted ring. |

### MRW.15 Mystery ledger

None.

### MRW.16 Open decisions

1. Corwin's account is deliberately unflattering to the Mire's ears and fair to Emberholt (voice rule 10). The Emberholt bible owner should review `MRW-D4.10`–`.14` for consistency with that region's voice when it exists.

### MRW.17 Internal review log

| Check | Result |
|---|---|
| No absolution | Nobody forgives; the bread is manners. |
| Emberholt fairness | Corwin is neither villain nor apologist; Rootrest's resentment has reasons (peat and timber fears, war escalation) stated once by Gilly. |
| No Remnant, no Glassed Hollow, no route | None present; "the yards" is all that is said. |
| MD-7 swap note | No Hollowfoot content. No change under either ruling. |

### MRW.18 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Corwin Tey** [NEW] | Wage work in Emberholt's yards; peat; his grandmother. | What Rootrest wants from him. | Polite, quick, plain; tired of being looked at. |
| **Hessel Tey** [NEW], his grandmother | Her house; her grandson. | — | Old, flat, unbudgeable. |
| **Gilly Ruddle** [NEW], neighbour | Her reasons. | Whether they are fair. | Honest about her own unfairness. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `MRW-B1.1` | NEIGHBOUR (door 1) | Load 1 | "That's Hessel's peat. Good." (to the player only) |
| `MRW-B1.2` | NEIGHBOUR (door 2) | Load 2 | "He's quick. They teach them quick over there." |
| `MRW-B1.3` | NEIGHBOUR (door 3) | Load 3 | "Plank's slippy by the stake. Mind." |
| `MRW-B1.4` | GILLY | Load 4 | (watches; says nothing; goes in) |
| `MRW-B2.1` | CORWIN | Rick, first course | "Lean them. Each row the other way. Rain runs off a herringbone." |
| `MRW-B2.2` | CORWIN | Wrong lean | "Other way." |
| `MRW-B3.1` | GILLY | `MRW_ROOF = tar`, later | "Emberholt pitch on a Rootrest shed. It doesn't leak. I hate that." |
| `MRW-B3.2` | GILLY | `MRW_ROOF = thatch`, later | "My reed. On his gran's shed. Don't make anything of it." |
| `MRW-B4.1` | HESSEL | Post-quest, `elder` | "I said it. I'll not say it twice." |
| `MRW-B4.2` | CORWIN | Post-quest | "Stack's dry. Gran's warm. That's what I came for." |

#### Nodes

```
MRW-D1.00 [quest Active, returning] GILLY: "Stack's still out. Where were we?" (pins step)  → end
MRW-D1.01 GILLY: "Hessel's peat's on the bank. Wet comes, the plank way goes under, and she's cold all winter."
MRW-D1.02 GILLY: "Her grandson's back. From Emberholt. From the yards. He's doing it on his own because nobody'll go beside him."
MRW-D1.03 GILLY: "I'll not. I can't tell you why that's fair. I'll not anyway."
  > "Why not?"                                                       → MRW-D1.04
  > "I'll help him."                                                 → MRW-D1.06
MRW-D1.04 GILLY: "Emberholt made the war hotter than it had to be. Now they want our peat and our timber and send our young ones home when they're done with them." (beat) "That's not his fault. I know it's not."   → MRW-D1 options
MRW-D1.06 GILLY: "Then go on. We'll be watching. We're good at that."   {event: accept}  → end

MRW-D2.01 CORWIN: (at the bank, barrow half full) "You're not from here. Good. Everyone from here's at their doors."
MRW-D2.02 CORWIN: "Gran can't lift it now. I came back to lift it. That's all."
  > "I'll take a barrow."                                            → MRW-D2.03
  > "Why did you go?"                                                → MRW-D2.05
MRW-D2.03 CORWIN: "Four each. Mind the stake by the low plank."   {event: S01 complete}  → end
MRW-D2.05 CORWIN: "Wage. Every week. Nobody here paid anyone anything when I was young. You worked for your neighbour and your neighbour worked for you." (beat) "I wanted to be paid."   → MRW-D2 options
```

```
MRW-D3.01 CORWIN: (holding a roll of black cloth) "Tarred cloth. Two layers and it's dry for ten years."
MRW-D3.02 GILLY: (from the yard wall) "Rootrest roofs with reed."
MRW-D3.03 CORWIN: "Reed's three days and leaks in five years."
MRW-D3.04 GILLY: "It's ours."
  > "Tar cloth. It's quick and it's dry."                            → MRW-D3.10
  > "Reed. Gilly, can we have your bundles?"                         → MRW-D3.20
MRW-D3.10 CORWIN: "Thank you." / GILLY: "Emberholt pitch." (goes in)   {set MRW_ROOF = tar}  → end
MRW-D3.20 GILLY: (a long look) "...They're by my door. You carry them. Not him."   {set MRW_ROOF = thatch}  → end
```

```
MRW-D4.01 HESSEL: "Sit. Eat. Then talk, if you must."
MRW-D4.02 (Food. Bowls passed. Nobody passes to Corwin; Hessel fills his.)
MRW-D4.03 GILLY: (putting down her spoon) "Corwin. What do they say about the war, over there?"
MRW-D4.10 CORWIN: "Nothing." (beat) "They don't talk about it. They talk about output. How many, how fast, by when."
MRW-D4.11 CORWIN: "I liked that. Nobody looked at me like I was carrying something. I just carried things."
MRW-D4.12 CORWIN: "And the wage came every week. On time. Every week."
MRW-D4.13 (Nobody speaks. A neighbour sets down a cup very carefully.)
MRW-D4.14 GILLY: "On time."
  > "He brought the stack in. I saw it."                             → MRW-D4.20
  > (say nothing)                                                    → MRW-D4.30
  > "Hessel, it's your table."                                         → MRW-D4.25
MRW-D4.20 GILLY: "I saw it too. That's not what I asked."   {set MRW_TABLE = spoke}  → MRW-D4.30
MRW-D4.25 HESSEL: "He came back. I don't need it to be more than that." (beat) "I'm not asking you to either."   {set MRW_TABLE = elder}  → MRW-D4.30
MRW-D4.30 [MRW_TABLE unset] {set MRW_TABLE = quiet}
MRW-D4.31 (A long quiet. Then Gilly takes the loaf and passes it to Corwin without looking at him.)   {event: rootrest.bone_chimes (MRW.8)}
MRW-D4.32 CORWIN: (takes it) "...Thank you."
MRW-D4.40 HESSEL: (to the chimes, not to anyone) "Wind."   → end
```

```
MRW-D5.01 CORWIN: (at the door) "Stack's in. Shed's dry. That was the job."
MRW-D5.02 [spoke] CORWIN: "You didn't have to say that." / [quiet] CORWIN: "Thanks for not." / [elder] CORWIN: "She'd never have said it to me. Only to them."
MRW-D5.03 CORWIN: (coins) "Emberholt coin spends the same. Take it."
      {event: MRW-D5 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `MRW-I1` | Bone chimes | "Small carved bones strung on cord. Still." |
| `MRW-I2` | The rick (done) | "Courses leaning each way in turn. Rain will run off it." |
| `MRW-I3` | Tar cloth roll | "Black, stiff, smells of the yards." |
| `MRW-I4` | Plank-way stake | `MR_CHANNELS` reading. |

---

## MNK — Nine Stakes

### MNK.1 The quest in one paragraph

Nine Stakes is an old marked crossing at the edge of the Field of Fallen Standards: nine Reedsward depth stakes set in bog-oak sockets across a broad shallow, telling anyone on the bank whether it will take them. Since the causeway went down this spring, most traffic uses the causeway; the people who still cross at Nine Stakes are the ones who will not walk past the standards, and they are the ones being drowned. Mud-Clad Raiders have pulled the stakes and re-set them with the bands turned, so the crossing reads Slack when it is Sour, and they wait in the reeds for whoever wades out and goes in to the waist. Halsey Fenner, a Marshwarden, lost a ferry family's cart there last week and nobody in it came out of the water dry. The player reads the false stakes from the rise, clears the raider groups in their mud, fights the Mud-Boss on the reed island at the crossing's middle, and then does the real work: carries nine stakes back and sets each in its own socket by the wear ring on the bog-oak, with the right face to the bank. One socket is off the line, pointing down a side channel, worn as deep as the others. The ferry book at Halsey's post says why: in the war a stakeman moved one stake to send a fleeing group of households down the side channel where nobody could follow at Sour. The ninth stake goes back on the line; the side socket is marked. At dusk the moss caps on the stakes light one after another from the near bank to the far, as if someone were walking across with a lantern.

**Remember:** nine lights crossing the water with nobody carrying them. **Want next:** to know who the stakeman was (the ferry book does not say).

### MNK.2 Selection record

| Candidate | Verdict |
|---|---|
| A. Kill raiders, done. | Rejected. Combat-only without the Mire's system. |
| B. Re-stake without a fight. | Rejected. Bible §7.2: a combat challenge. |
| **C. Read the lie from a rise → clear the reeds → the Mud-Boss → read the sockets and re-stake → the ninth socket's history from the ferry book** | **Selected.** The fight is the middle; the stakes are the point; the history comes from a book, never from an enemy. |

### MNK.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Mud-Clad Raiders: bandits who use mud camouflage, target travellers crossing the lower bogs | Dossier §IX; bible §10 (mudcutter, reed-slinger; elite Mud-Boss) | [CANON] family; [NEW] variants |
| Nine Stakes: marked crossing, raider ground | Part 3 Mire proposal; bible MP21 | [NEW, Part 3, adopted] |
| Channel stakes, three bands | Bible §1.1 | [NEW] system |
| The Standards Causeway relaid this spring `[CAUSEWAY]` | Bible §2.3 | [NEW] |
| Halsey Fenner, the ferry book entry, the side socket | This package | [NEW] |

### MNK.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.nine_stakes` |
| Type | Combat challenge (bible §7.2) |
| Unlock | MR-M1 Completed. Offered by Halsey Fenner at the Marshwardens' post on the Nine Stakes bank (`MNK-D1`), reached off the causeway; a causeway bark points there (`MNK-B0`). |
| Resume hook | Halsey at the post: `MNK-D1.00` "Stakes are still lying. Where were we?" |
| Target length | 30–40 minutes |
| Combat share | ~45% |
| Skills | Melee or Ranged; no skill check |
| Choice | None (contract: no fail; no choice). The ninth socket's marking is fixed. |
| Outputs | `MNK_NINTH` |
| **Anchor** | Marshwardens; ferry households |
| **World-truth row** | H23 (recovery: a wartime kindness kept in a ferry book). |
| **Revelation role** | Self-contained. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed; no fail; a stake set in the wrong socket does not seat and can be lifted again. |
| **Combat compliance** | Mud-Clad Raiders and the Mud-Boss (MNK-E1–E3) defeated at 0 HP with the ordinary defeat presentation; no yield, no testimony; melee or ranged; no SX. |

### MNK.5 The places [MAP VERIFICATION REQUIRED]

Nine Stakes lies at the Field's edge off the Standards Causeway (bible §4.2 route order).

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **N1. Halsey's post** | Hook; ferry book | A Marshwarden shelter on a dry hump: a brazier, a bench, the **ferry book** in an oilcloth bag on a nail. A broken cart on its side in the shallows below. | — |
| **N2. The rise** | Read the lie | A low knoll with a view across the crossing. | — |
| **N3. The crossing** | Stakes; fights | A broad shallow a long stone's throw across, nine **bog-oak sockets** in a line (black, iron-hard old wood set in the bed), and the nine **stakes** in them, wrongly. Reed beds either side; mud mounds that are not mounds. | Wading: knee-deep at Slack, waist at Running (slow), non-walkable at Sour except on the island. |
| **N4. The reed island** | MNK-E3 | A hummock in the middle of the line, ringed with reed, the raiders' blind: a pole frame, a fire pit, stolen goods under hides. | Reachable at Slack or Running. |
| **N5. The side channel** | The ninth socket | A narrow channel leaving the crossing's line downstream. At its mouth, a **tenth socket**, off the line, worn as deep as the nine. | — |

### MNK.6 Player-facing sequence

**Beat 0 — Drowned Carts (`S00_offer`).** *Objective: Talk to the Marshwarden at Nine Stakes.* `MNK-D1`. Halsey explains the cart, the false stakes and why people still use Nine Stakes `[CAUSEWAY]`.

**Beat 1 — Read the Lie (`S01_read`).** *Objective: Read the crossing from the rise.* From the rise (N2), inspect three stakes at range (inspect from distance). With `MR_CHANNELS`, each reports its band (*"Ochre. Slack."*) and the player can compare it with the water on the near bank's own stake by Halsey's post (*"Black. Sour."*). The near stake and the crossing disagree; the crossing's stakes are lying. Also visible: three mud mounds in the reeds that breathe (a faint steam in the cold; telegraph for MNK-E1).

**Beat 2 — The Reeds (`S02_clear`).** *Objective: Clear the raiders from the reed beds.* Keep watch to Slack (Halsey pins it on the first keep watch). Two raider groups (MNK-E1 near reeds, MNK-E2 far reeds). Either order.

**Beat 3 — The Island (`S03_boss`).** *Objective: Take the reed island.* The Mud-Boss and two mudcutters on the island (MNK-E3; MNK.7.1). Stolen goods under hides (ordinary loot plus the ferry family's cart goods as a carry-state bundle for Halsey; nothing evidentiary).

**Beat 4 — Pull Them (`S04_pull`).** *Objective: Pull the false stakes.* Nine stakes, each one interaction (~2 s) to lift; carried to the island (carry-state, one at a time; or stacked on the island by lifting near it). The sockets are now bare.

**Beat 5 — Set Them True (`S05_set`).** *Objective: Set each stake in its own socket.* Each socket's bog-oak wall carries a **wear ring** where the water has stood for years at Slack, and a **notch** cut on the bank side. Each stake has a matching notch at its foot. The puzzle (no timer, harmless reset): inspect a socket (`MNK-I4`), pick up the stake whose foot matches (stakes are carved with one to nine small cuts beside the notch; the sockets' notches match by count), seat it with the notch toward the bank (interaction; a wrong stake or wrong face simply does not seat: "Won't go home."). The painted bands then sit level with the wear ring: ochre at the ring. Nine seated stakes read the true state. Halsey reads the near stake and the crossing together from the bank (`MNK-B3`).

**Beat 6 — The Ninth Socket (`S06_ninth`).** *Objective: Find out about the socket off the line.* One stake (carved nine) fits the ninth socket on the line *and* the tenth socket at the side channel's mouth (N5): both are cut for it. Inspect the side socket (`MNK-I6`). Ask Halsey (`MNK-D3`); she reads the **ferry book** (N1): an old entry, undated except by weather, in a ferryman's hand: *"Fog two days, then the hard frost. Stakeman Varne moved the ninth to the side mouth at dusk. Households off the road went down the side channel at Sour. Nobody could follow. Stake put back at first light."* (`MNK-I7`). The ninth stake goes back on the line (interaction); Halsey paints a small ring on the side socket's top so it is not forgotten (`MNK_NINTH`).

**Beat 7 — The Lights (`S07_dusk`).** *Objective: Watch the crossing at dusk.* Halsey caps each stake with wet lantern moss, as Marshwardens do on a kept crossing. Keep watch to dusk at the post. The strange moment (MNK.8). `MNK-D4`. Quest Completed.

### MNK.7 Encounters

Tuned for MR-M1's Competent identity, upper end (MD-10).

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MNK-E1** | 2 × Mud-Clad Raider (mudcutter), 1 × Mud-Clad Raider (reed-slinger) | Near reed bed (N3 west) | Mudcutters lie as mud mounds and rise when the player wades within ~6 m; the slinger stays in the reeds | **Rise:** the mound's steam thickens and it shifts (~1.2 s). **Mudcutter cleave:** weapon dragged back through the mud (~0.9 s). **Sling:** the slinger's arm whirls twice (~1.4 s), then a clod that blinds briefly on hit (standard short blind) | Required. Teaches the breathing mound | 45–60 s |
| **MNK-E2** | 1 × mudcutter, 2 × reed-slinger | Far reed bed (N3 east) | Slingers on two hummocks, crossfire; the mudcutter guards the reed path between | As E1 | Required. Ranged players can trade with slingers across the water; melee players use the reed path, which is screened from one slinger | 50–70 s |
| **MNK-E3** | **Mud-Boss** + 2 × mudcutter | Reed island (N4) | Elite; spec below | See MNK.7.1 | Required | 2.5–3.5 minutes |

#### MNK.7.1 Elite spec — the Mud-Boss

| Field | Spec |
|---|---|
| Family | Mud-Clad Raiders, elite (bible §10). Human. Fights to 0 HP (CDR-1); ordinary defeat presentation. Never speaks after defeat; nothing he carries is evidence. |
| Read | A big man in a coat of dried mud plates over oilcloth, a long hooked pole (a stake-puller) and a short blade. |
| **Hook pull** (all phases) | He sets the pole's hook low and leans back (**1.3 s**); a straight pull that drags a player within 5 m toward him and into the shallows on the island's edge (slow on landing). |
| **Mud plate** (all phases) | Below each third of health, he wades into the shallows and re-coats (**2.0 s**, kneeling, scooping mud onto his chest). A re-coat gives a damage-reduction plate on the front (readable: wet grey plates). Hitting him during the re-coat interrupts it. Ranged can interrupt from range; melee from close. |
| **Call** (P2) | At 60% he shouts once (**1.0 s**) and both remaining mudcutters rise from the island's edge mounds (if E3's mudcutters are already defeated, nothing comes). |
| **Sweep** (P3, below 30%) | He swings the pole in a full circle (**1.6 s**, pole held level and drawn back) that knocks down anyone inside 4 m. Cadence ~10 s. |
| Arena | The island: dry centre, shallow edges (slow), reed screen. Two pole-frame uprights for cover against slingers if any remain. |
| End | At 0 HP he falls; ordinary defeat. Halsey, from the bank: "That's the last of them." (one sober line). |
| Reset | Leaving the island resets him and any living mudcutters; E1/E2 stay defeated. |

**Rules.** Every raider to 0 HP; no yield; no defeated raider speaks. Combat drops nothing that advances the history (the ferry book carries it). **Death:** respawn at Halsey's post; defeated groups stay defeated; seated stakes stay seated.

### MNK.8 The strange moment: the lights cross (presentation spec)

| Time | Element | Spec |
|---|---|---|
| Dusk | **Caps** | Nine stakes, each capped with lantern moss Halsey wetted at the foot and packed on top; the water at Slack, ochre on every stake. |
| 0–2 s | **First** | The near stake's cap lights as the damp climbs into the moss (lantern-moss rule: wet moss glows). |
| 2–14 s | **Across** | One after another, from the near bank to the far, each cap lights, at a walking pace, as if someone were crossing with a lantern. The ninth lights last. Nobody is on the crossing. |
| 14–18 s | **The side** | The ringed side socket, which has no stake, stays dark. |
| After | Halsey | "Damp climbs at the same rate in each. They light in order." (beat) "My mother used to say the stakeman was walking it." (`MNK-D4.03`) |
| Meaning | The moss and the water. Halsey gives the physical reason and her mother's saying, and names it as a saying. Proves nothing. |

### MNK.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Talk to the Marshwarden at Nine Stakes. | `MNK-D1` accept | Yes |
| `S01_read` | Read the crossing from the rise. | 3 range inspects + near-stake inspect | Yes |
| `S02_clear` | Clear the raiders from the reed beds. | MNK-E1 and MNK-E2 defeated | Yes |
| `S03_boss` | Take the reed island. | MNK-E3 defeated | Yes |
| `S04_pull` | Pull the false stakes. | 9 `pull_stake` | Yes |
| `S05_set` | Set each stake in its own socket. | 9 `seat_stake` | Yes |
| `S06_ninth` | Find out about the socket off the line. | Side socket inspect + `MNK-D3` (ferry book) + ninth reseated | Yes (sets `MNK_NINTH`) |
| `S07_dusk` | Watch the crossing at dusk. | Keep watch to dusk + light event + `MNK-D4` end | Yes (→ Completed) |

### MNK.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `MNK_NINTH` | `S06` | Side socket ring prop; Halsey and ferry barks |

### MNK.11 Choices and consequences

None (contract). The crossing is made true in every playthrough.

### MNK.12 Rewards and unlocks

Nine Stakes as a true, kept crossing (a route across the Field's edge, readable by stakes); the cart family's goods returned (Halsey pays a small sum from the post); ordinary raider loot; Melee or Ranged XP. No lump XP.

### MNK.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Wades at Sour | The crossing is non-walkable beyond knee depth; the island waits. |
| Wrong stake or face | "Won't go home." Lift and try another. |
| Walking away | Stays Active; resume at Halsey. |
| Death | Respawn at the post; progress kept. |
| Co-op | Raiders and the Mud-Boss are shared; stakes are per-player props (host fallback); each player reads the ferry book. |

### MNK.14 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Range inspect on stakes | Systems | Inspect from distance with line of sight. |
| Stake/socket matching | Systems | Nine sockets with an id; stakes with an id; seat only on matching id and facing. |
| Breathing mud mounds | VFX / AI | Idle mound with steam; rise on proximity. |
| Re-coat interruptible channel | Gameplay | Standard interruptible ability with a damage-reduction buff. |
| Moss caps lighting in sequence | VFX | Nine prop state flips on a timer at dusk. |

### MNK.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | A stakeman named Varne moved the ninth stake one foggy war dusk to let fleeing households escape down the side channel. Who pursued them is withheld (R08 spirit: no side). |
| Public belief | Ferry households know "the ninth was moved once". |
| Observable | The side socket; the ferry book line. |
| Wrong reading | The stakeman drowned soldiers on purpose. (The book says only that nobody could follow.) |
| Withheld | Who followed; how many went down the channel; what happened to Varne. |

### MNK.16 Open decisions

1. "Varne" is a single surname in an old ferry book; no living Varne is placed. If the Register series wants him, it is a Director call.
2. Whether Nine Stakes should join the channel-schedule system (N-1) permanently. Recommended: yes.

### MNK.17 Internal review log

| Check | Result |
|---|---|
| CDR-1 | Raiders and the Mud-Boss to 0 HP; no yield; the Boss's "call" is a phase bark, not a surrender. |
| Evidence | History from the ferry book only. No defeated raider speaks. |
| R08 | No side, unit or number. "Households off the road." |
| CDR-2 | Slingers give ranged players a duel and melee players a screened path; the Boss's re-coat can be interrupted by either. |
| `[CAUSEWAY]` | Halsey's hook line tagged. |
| MD-7 swap note | No Hollowfoot content. No change under either ruling. |

### MNK.18 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Halsey Fenner** [NEW], Marshwarden at Nine Stakes | The crossing; the ferry book; the lost cart. | Who Varne was beyond the line. | Oilcloth, mud to the knee, wry; stake grammar in every sentence. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `MNK-B0` | REEDSWARD CREW `[CAUSEWAY]` | Causeway, MR-M1 done | "Halsey at Nine Stakes is asking for hands. People still cross there. The ones who won't walk past the standards." |
| `MNK-B1` | HALSEY | Mound breathes | "That mound's breathing. Mounds don't." |
| `MNK-B2` | HALSEY | E1 or E2 defeated | "Reeds are clear that side." |
| `MNK-B3` | HALSEY | All nine seated | "Near stake ochre. Crossing ochre. They agree. That's all a crossing has to do." |
| `MNK-B4` | FERRY HOUSEHOLD | Post-quest | "Nine Stakes is telling the truth again. Halsey says thank the traveller." |
| `MNK-B5` | HALSEY | Post-quest, dusk | "Caps are lit. Walk it if you like." |

#### Nodes

```
MNK-D1.00 [quest Active, returning] HALSEY: "Stakes are still lying. Where were we?" (pins step)  → end
MNK-D1.01 HALSEY: "Sit if you want. Don't cross."
MNK-D1.02 HALSEY: "Ferry family's cart went in last week. Stakes said slack. Water said sour. Nobody in it came out of the water dry. Nobody came out of the reeds after them either, and somebody should have."
MNK-D1.03 [CAUSEWAY] HALSEY: "Since Oswin's crews laid the causeway, most go that way. The ones who come here won't walk past the standards. Can't blame them. Raiders know it."
  > "Who pulled the stakes?"                                         → MNK-D1.04
  > "What do you need?"                                              → MNK-D1.06
MNK-D1.04 HALSEY: "Mud-Clad. They pull them and put them back wrong, bands turned. Then they lie in the reeds and wait for someone to trust a stake."   → MNK-D1 options
MNK-D1.06 HALSEY: "Go up the rise. Look at the near stake, then the crossing. Tell me if they agree." (beat) "They don't."   {event: accept}  → end
```

```
MNK-D3.01 HALSEY: (turning the ferry book's pages) "There's a tenth socket. Off the line. Everyone knows the ninth was moved once. Nobody remembers why."
MNK-D3.02 HALSEY: (finds it) "Here. Old hand. No date. They dated by weather then, same as now."
MNK-D3.03 HALSEY: (reading) "'Fog two days, then the hard frost. Stakeman Varne moved the ninth to the side mouth at dusk. Households off the road went down the side channel at Sour. Nobody could follow. Stake put back at first light.'"
  > "Who was following?"                                             → MNK-D3.04
  > "Who was Varne?"                                                  → MNK-D3.05
  > "Put it back on the line?"                                       → MNK-D3.06
MNK-D3.04 HALSEY: "Doesn't say. Book says 'nobody could follow'. That's all I'll say it says."   → MNK-D3 options
MNK-D3.05 HALSEY: "A stakeman. That's a whole life in one word, and it's all the book's got."   → MNK-D3 options
MNK-D3.06 HALSEY: "On the line. That's where it tells the truth." (beat) "I'll ring the side one. So it's not forgotten. Then it's two holds: the book and the ring."   {event: reseat enabled; MNK_NINTH on reseat}  → end
```

```
MNK-D4.01 HALSEY: (watching the last cap light) "There."
MNK-D4.02 HALSEY: "Damp climbs at the same rate in each. They light in order."
MNK-D4.03 HALSEY: (beat) "My mother used to say the stakeman was walking it." (beat) "That's her saying. Not mine."
MNK-D4.04 HALSEY: (pays from the post's box) "Cart family's goods back, crossing true. Come and walk it whenever."
      {event: MNK-D4 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `MNK-I1` | Near stake (Halsey's post) | `MR_CHANNELS` reading; the true state. |
| `MNK-I2` | Crossing stake (before) | "Ochre. Slack." (the water round it is black-dark and fast) |
| `MNK-I3` | Breathing mound | "A mound of mud. Steam rises from it in the cold." |
| `MNK-I4` | Bog-oak socket | "Black, hard as iron. A pale ring worn round the inside where the water stands at slack. A notch on the bank side, and beside it, small cuts: [one to nine]." |
| `MNK-I5` | Stake foot | "A notch at the foot, and small cuts beside it: [one to nine]." |
| `MNK-I6` | Side socket | "Off the line, at the side channel's mouth. Worn as deep as the others. Nine cuts beside its notch." / after: "A painted ring on its top." |
| `MNK-I7` | Ferry book entry | "'Fog two days, then the hard frost. Stakeman Varne moved the ninth to the side mouth at dusk. Households off the road went down the side channel at Sour. Nobody could follow. Stake put back at first light.'" |
| `MNK-I8` | Moss cap (after) | "Wet moss packed on the stake's top. It glows." |

---

## MRH — The Rust Hart

### MRH.1 The quest in one paragraph

The Rust Hollow is ironbloom ground at the edge of the Field: red soil, rust-coloured fungus, and old iron in the peat that nobody touches because battlefield metal is not salvage. A great tarnish stalker has made it its own, a stag twice the size of any in Marshfall's stories, with antlers stained iron-black, and it charges anything that walks on two legs. Annot Reeve, a Marshfall hunter, has lost a dog and nearly a nephew to it, and has worked out one thing: its path is mad, but its stops are not. It stops only on the thickest ironbloom, to lick the red soil. The player reads four stop sites by sign (scrape, licked-bare ground, antler rub, droppings red with iron) and by the ironbloom's colour (deep rust where it is thick, orange where thin), finds the one thick patch it has not yet stopped at this round, and is there first. The Rust Hart comes out of the fog, stops, licks, lifts its head, and charges. When it is down, the player finds an old arrowhead grown into the base of one antler, carried for longer than Annot has hunted.

**Remember:** a stag the colour of old iron standing quite still on a red patch, and then not. **Want next:** to read the Mire's ironbloom everywhere.

### MRH.2 Selection record

| Candidate | Verdict |
|---|---|
| A. Arena boss. | Rejected. Wastes the bible's "its stops are not". |
| B. Tracking only; it leaves. | Rejected. CDR-1; the bible lists it as a miniboss fought to 0 HP. |
| **C. Read four stops by sign and fungus → predict the fifth → ambush → a stop-and-charge fight in an arena of red patches** | **Selected.** Hunting is the quest's spine (requirement and play); the fight's pattern is the same knowledge. |

### MRH.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Tarnish Stalkers: twisted elk-like creatures, antlers stained by iron-rich soil, move erratically | Dossier §IX | [CANON] |
| Ironbloom: rust-coloured, near battle ruins, feeds on metal-rich soil; spores dangerous in high concentration | Dossier §X, §XI | [CANON] (resource legacy) |
| The Rust Hollow (MP27); the Rust Hart (side miniboss) | Bible §4.2, §10 | [NEW] |
| Battlefield metal is evidence, not feedstock | Source process; MD-11 | Proposal adopted |
| Annot Reeve, her nephew Osgar, the arrowhead | This package | [NEW] |

### MRH.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `mire.side.rust_hart` |
| Type | Combat challenge, **miniboss** (bible §7.2, §10) |
| Unlock | MR-M2 Completed. Offered by Annot Reeve at the Rust Hollow's edge (`MRH-D1`); a Marshfall hunter bark points there (`MRH-B0`). |
| Skill requirement | **Hunting ~[GD: low-mid]** to accept (CDR-4). |
| Resume hook | Annot at her blind: `MRH-D1.00` "It's still out there. Where were we?" |
| Target length | 30–40 minutes |
| Combat share | ~45% |
| Skills | Hunting (required: tracking sign, harvesting); Melee or Ranged |
| Choice | Where the antlers go (`MRH_ANTLER` = rootrest / hunter) |
| **Anchor** | Marshfall hunters |
| **World-truth row** | None. |
| **Revelation role** | Self-contained. The arrowhead proves nothing about anyone. |
| **Recurring evidence** | None. |
| **State compliance** | Inactive / Active / Completed; no fail; stop sites persist; the Hart resets on leaving. |
| **Combat compliance** | The Rust Hart and two stalkers to 0 HP; harvestable per economy; melee or ranged; no SX. |

### MRH.5 The places [MAP VERIFICATION REQUIRED]

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **H1. Annot's blind** | Hook | A turf blind on a dry lip above the Hollow; a dog's empty collar on a peg. | — |
| **H2–H5. Four stop sites** | Tracking | Patches of red ground in the Hollow, each with sign (MRH.6 Beat 2). Between them, the Hart's erratic path: prints that zigzag, double back, cross themselves. | Peat paths; fog drifts in and out. |
| **H6. The Hollow's heart** | Arena | A wide bowl of red soil with five ironbloom patches of different thickness (deep rust, rust, orange, orange, pale), old iron (a bent blade, a buckle) half in the peat (inspectable, never collectable), stumps for cover. | Agility: vault a stump line (shortcut); walkable fallback round it. |

### MRH.6 Player-facing sequence

**Beat 0 — Two Legs (`S00_offer`).** *Objective: Talk to the hunter at the Rust Hollow.* `MRH-D1`. Below the requirement: `MRH-D1.05`.

**Beat 1 — Mad Path (`S01_path`).** *Objective: Follow the hart's path.* From the blind, follow prints into the Hollow (inspect three print sets). They zigzag and double back. Annot's bark: "Don't follow the feet. Follow where it stops."

**Beat 2 — Its Stops (`S02_stops`).** *Objective: Read four of its stops (0/4).* Any order. Each stop site has two inspects: **sign** and **fungus**.

| Site | Sign | Fungus |
|---|---|---|
| H2 | Licked-bare red soil; a scrape | Deep rust, thick |
| H3 | An antler rub on a half-buried iron rim; bark of rust on the iron | Deep rust, thick |
| H4 | Droppings red with iron; a scrape | Rust, thick |
| H5 | Licked-bare soil; an old bed | Deep rust, thick |

Annot, after the fourth: every stop is on thick ironbloom; it never stops on orange. The prints show the round runs H2 → H3 → H4 → H5 and on. Hunting XP per site.

**Beat 3 — Where Next (`S03_predict`).** *Objective: Find the thick patch it has not stopped at.* In the Hollow's heart (H6), inspect the five patches: deep rust (no sign: unvisited this round), rust (old sign), orange, orange, pale. The deep-rust patch with no sign is next. Choose it (interaction: "Wait here."). Choosing an orange or pale patch gives Annot's bark ("It won't stop on orange.") and the player chooses again; no penalty.

**Beat 4 — The Wait (`S04_wait`).** *Objective: Wait downwind of the patch.* Annot marks the downwind side with a stick. Stand in the marked area and keep watch (one turn, to dusk). The Hart comes (MRH.8).

**Beat 5 — The Rust Hart (`S05_fight`).** *Objective: Bring down the Rust Hart.* Miniboss (MRH.7.1). 0 HP.

**Beat 6 — The Antlers (`S06_antlers`).** *Objective: Harvest the hart.* Hunting harvest interaction (~3 s; or Annot does it, as the alternative). Inspect the antler base: the old arrowhead (MRH.9). Annot asks where the antlers go (`MRH-D3`): Rootrest's bonecarvers (they make memorial carvings from antler) or Annot's wall. `MRH_ANTLER`. Return to the blind; `MRH-D4`. Quest Completed.

### MRH.7 Encounters

Tuned for MR-M2's Competent identity, upper end (MD-10).

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **MRH-E1** | **The Rust Hart** | Hollow's heart (H6) | Miniboss; spec below | See below | Required | 3–4 minutes |
| **MRH-E2** | 2 × Tarnish Stalker (stalker) | Called at 50% | Adds; stop-and-charge like the Hart, smaller | **Stamp:** two forefoot stamps (~1.0 s), then a charge | Phase 2 pressure | — |

#### MRH.7.1 Miniboss spec — the Rust Hart

| Field | Spec |
|---|---|
| Family | Tarnish Stalkers, elite (bible §10). An animal; fights to 0 HP (CDR-1); harvestable per economy. |
| Read | A huge iron-grey stag, flanks streaked rust-red, antlers stained black at the base and rust at the tips, wide as a cart. Moves in jerks: it starts, stops, turns its head sharply. |
| **The stop** (core pattern) | The Hart never charges from a standing start on bare ground. It always runs to the **nearest thick ironbloom patch** (deep rust or rust), **stops**, lowers its head to lick (**2.5 s**, completely still: the opening for heavy hits), then lifts its head and fixes on the nearest two-legged target. Patches thin from deep rust to orange after it has licked them twice (visible colour change), so the arena's stops move as the fight goes on. Players who read the patches are standing where it will stop. |
| **Charge** (all phases) | After a stop: head up, two forefoot stamps throwing red dust (**1.4 s**), then a straight charge across the bowl. Heavy damage and knockdown. Stepping behind a stump makes it hit the stump (2 s stagger: free hits). Cadence: after every stop. |
| **Erratic run** (all phases) | Between stops it zigzags at speed; contact deals moderate damage. Its path is random; its destination is not (the nearest thick patch). |
| **Antler rake** (P2, 70% and below) | At a stop, instead of licking, it rakes the patch with its antlers (**1.6 s**, head swinging low): a cloud of **ironbloom spores** fills the patch for 8 s. Standing in it: a standard damage-over-time (spores, dossier: "dangerous in high concentrations"). The cloud is rust-coloured and clearly bounded. |
| **Bellow** (P2, at 50%) | It raises its head and bellows (**2.0 s**, neck stretched, breath plume); two stalkers (MRH-E2) come out of the fog from the Hollow's edge. |
| **Iron run** (P3, below 25%) | It stops less: the lick shortens to **1.5 s**, and after each charge it runs straight to the next patch with no zigzag. |
| Arena | Five patches, stumps for cover, old iron in the peat (cosmetic, never collectable). |
| Ranged and melee (CDR-2) | Ranged players shoot during the lick and from behind stumps; the charge closes any distance, so range never keeps it off. Melee players stand on the patch it will stop at and hit during the lick. Neither style trivialises it: patches thin, and the charge always comes. |
| End | At 0 HP it goes down on the red ground; the dust settles. Harvestable. |
| Reset | Leaving the Hollow's heart or dying resets it to full; stop sites read earlier stay read; patches regrow. |

**Death:** respawn at Annot's blind.

### MRH.8 The strange moment: the stop (presentation spec)

| Time | Element | Spec |
|---|---|---|
| Dusk | **Fog** | Fog moves through the Hollow. The player is downwind of the deep-rust patch. |
| 0–4 s | **Out of the fog** | The Rust Hart comes out of the fog at a zigzag, fast, in jerks, and then is suddenly on the patch, completely still. |
| 4–10 s | **Still** | It lowers its head and licks the red soil. Its flanks steam. Every other sound in the Hollow (frogs, a far heron) stops. Annot, at the player's shoulder, does not breathe. |
| 10–12 s | **The look** | It lifts its head and looks straight at the player. Rust-red dust drifts off its antlers. |
| 12 s | **Begin** | Two stamps; the fight begins (objective appears only now). |
| Meaning | An animal that eats iron-rich soil. Hunters' talk only: "It knows its ground." |

### MRH.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_offer` | Talk to the hunter at the Rust Hollow. | `MRH-D1` accept (Hunting ~[GD: low-mid]) | Yes |
| `S01_path` | Follow the hart's path. | 3 print inspects | Yes |
| `S02_stops` | Read four of its stops. | 8 inspects (sign + fungus × 4) + `MRH-D2` | Yes |
| `S03_predict` | Find the thick patch it has not stopped at. | Choose the unvisited deep-rust patch | Yes |
| `S04_wait` | Wait downwind of the patch. | Keep watch to dusk in the marked area | Yes |
| `S05_fight` | Bring down the Rust Hart. | Rust Hart defeated (0 HP) | Yes |
| `S06_antlers` | Harvest the hart. | Harvest (player or Annot) + antler-base inspect + `MRH-D3` choice + `MRH-D4` end | Yes (→ Completed) |

### MRH.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `MRH_ANTLER` = rootrest / hunter | `S06` | Rootrest bonecarver prop (a carved antler memorial on the Last Root's rail); Annot's blind prop |

### MRH.11 Choices and consequences

| Option | Immediate | Cost | Honoured how |
|---|---|---|---|
| **To Rootrest's bonecarvers** (`rootrest`) | Annot carries them to Rootrest; the bonecarvers make a memorial rail-piece from them. | Annot gets no trophy, and she wanted one more than she says. | A carved antler piece on the rail by the Last Root (MDS08 area). Mourners touch it. |
| **To Annot's wall** (`hunter`) | They hang over her blind. | Rootrest's carvers lose the best antler anyone has seen. | Annot's bark; Marshfall children dare each other to touch them. |

The arrowhead stays in the antler either way. Nobody pulls it out.

### MRH.12 Rewards and unlocks

The hide and meat per the economy pass (harvest); a share to Annot; small payment; the Rust Hollow as hunting ground (ordinary tarnish stalkers return there, standard spawns); ironbloom reading as knowledge (thick or thin patches inspectable everywhere). Hunting and Melee or Ranged XP. No lump XP.

### MRH.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Below Hunting requirement | Offer visible; accept greyed with `MRH-D1.05`. |
| Chooses the wrong patch | Annot's bark; choose again. |
| Death | Respawn at the blind; stop sites stay read; the Hart resets. |
| Walking away | Stays Active; resume at Annot. |
| Co-op | The Hart is a shared world creature; all present get credit; the choice is per player (prop host fallback). |

### MRH.14 Integration needs

| Need | Owner | Minimum viable form |
|---|---|---|
| Patch-seeking AI | Gameplay / AI | "Move to nearest tagged patch, then lick" loop with a still window; patches as tagged arena volumes with a lick counter and a colour state swap. |
| Patch thinning | VFX | Two decal states (thick / thin) per patch. |
| Spore cloud | VFX / Gameplay | Bounded area DoT (standard). |
| Charge into stump stagger | Gameplay | Collision check on charge path (as Thornfell TGM pillars). |

### MRH.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | Somebody shot this stag long ago with an iron-headed arrow, and it lived and carried the head. When and who is not decided. |
| Public belief | "It's been shot at for twenty years and laughed." |
| Observable | The arrowhead grown into the antler base. |
| Wrong reading | A soldier's arrow from the war, so the Hart is as old as the war. (Nothing dates the head.) |
| Withheld | When; who. |

### MRH.16 Open decisions

1. Hunting requirement level (~[GD: low-mid]): Gameplay Designer.
2. Rust Hart drops: economy pass (hide, antler, meat). Recommended: the antler goes only as the choice says; no unique gear.

### MRH.17 Internal review log

| Check | Result |
|---|---|
| CDR-1 | The Hart and its stalkers to 0 HP; no flee; the bellow calls adds, it does not leave. |
| CDR-2 | Range never holds the charge off; melee has the lick window; both read the patches. |
| Battlefield metal | Old iron in the arena is inspect-only. The arrowhead stays in the antler. |
| Evidence | The arrowhead proves nothing; nothing dates it. |
| MD-7 swap note | No Hollowfoot content. No change under either ruling. |

### MRH.18 Dialogue

#### Cast notes

| Character | Knows | Doesn't know | Voice |
|---|---|---|---|
| **Annot Reeve** [NEW], Marshfall hunter | The Hollow, the Hart's round, ironbloom. | Why it hates two legs. | Short, grim, funny about her own fear. |

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `MRH-B0` | MARSHFALL HUNTER | Marshfall, MR-M2 done | "Annot's at the Rust Hollow, wanting a hunter who reads. Not one who runs." |
| `MRH-B1` | ANNOT | Beat 1 | "Don't follow the feet. Follow where it stops." |
| `MRH-B2` | ANNOT | Orange or pale patch chosen | "It won't stop on orange. It's fussy. It's the only thing about it that makes sense." |
| `MRH-B3` | ANNOT | Fight, first lick | "Now. While it's eating." |
| `MRH-B4` | ANNOT | Spore cloud | "Out of the red. That stuff's poison in a cloud." |
| `MRH-B5` | ANNOT | Post-quest, `hunter` | "Over my door. Osgar touches them every morning. For luck, he says. For spite, I say." |
| `MRH-B6` | ROOTREST BONECARVER | Post-quest, `rootrest` | "Best antler I've ever worked. We left the arrowhead in." |

#### Nodes

```
MRH-D1.00 [quest Active, returning] ANNOT: "It's still out there. Where were we?" (pins step)  → end
MRH-D1.01 ANNOT: "Don't go down there on two legs. That's the whole warning."
MRH-D1.02 ANNOT: "Rust Hart. Biggest stalker anyone's seen. It's had my dog. It nearly had my sister's boy."
MRH-D1.03 ANNOT: "Its path's mad. Zig, zag, back on itself. But it stops in the same kind of place every time." (beat) "I can't get there first. My knees are honest."
  > [Hunting below ~[GD: low-mid]] "I'm not much of a tracker."     → MRH-D1.05
  > [Hunting ~[GD: low-mid]] "Show me where it stops."              → MRH-D1.06
  > [MRS Completed] "Hob taught me to sit still."                    → MRH-D1.08
MRH-D1.05 ANNOT: "Then go and track something smaller first. A lot of small things. Come back when sign talks to you."   → end (offer stays open)
MRH-D1.06 ANNOT: "Follow the prints in. You'll see what I mean about mad."   {event: accept}  → end
MRH-D1.08 ANNOT: "Hob. Then you can sit. Sitting's half of it." (if Hunting met) → MRH-D1.06; (else) → MRH-D1.05
```

```
MRH-D2.01 ANNOT: "Well?"
  > "Every stop's on thick ironbloom. Deep rust. Never orange."      → MRH-D2.02
MRH-D2.02 ANNOT: "There. It's licking the iron out of the ground. It goes round the thick ones." (beat) "So where hasn't it been yet?"   {event: S02 complete}  → end
```

```
MRH-D3.01 ANNOT: (kneeling by the antler base) "Look at that."
MRH-D3.02 ANNOT: "Arrowhead. Grown right into the bone. Somebody shot it a long time ago and it carried the iron since."
MRH-D3.03 ANNOT: "Don't pull it. It's earned it." (beat) "Antlers. Rootrest's carvers would make something for the Root out of these. Or they go over my door."
  > "Rootrest. Let the carvers have them."                           → MRH-D3.10
  > "Your door. You lost a dog to it."                               → MRH-D3.20
MRH-D3.10 ANNOT: "...Good. Somebody should get some use of the thing besides me being frightened."   {set MRH_ANTLER = rootrest}  → end
MRH-D3.20 ANNOT: "I did. I'll look at them every morning and be glad." (beat) "Glad's a strong word."   {set MRH_ANTLER = hunter}  → end
```

```
MRH-D4.01 ANNOT: (at the blind, hanging the dog's collar back on its peg) "That's done."
MRH-D4.02 ANNOT: "Hollow's just a hollow now. Stalkers'll come back. Ordinary ones. They stop on the red too. You'll know where."
MRH-D4.03 ANNOT: (pays) "From me and from Osgar. He'd come and say it but he's still frightened of the place."
      {event: MRH-D4 end → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `MRH-I1` | Print set | "Huge prints. They zigzag, double back, cross themselves." |
| `MRH-I2` | Licked soil | "Red soil licked smooth and bare." |
| `MRH-I3` | Antler rub on iron | "An old iron rim in the peat, rubbed bright on one side by antlers. Not yours to take." |
| `MRH-I4` | Red droppings | "Droppings stained red. It eats the iron." |
| `MRH-I5` | Ironbloom, deep rust | "Thick rust-coloured fungus. Iron-rich ground." |
| `MRH-I6` | Ironbloom, orange | "Thin. Orange. Not much iron here." |
| `MRH-I7` | Antler base | "An old iron arrowhead grown into the bone, the bone smooth over its edges." |
| `MRH-I8` | Old iron in the arena | "A bent blade in the peat. Battlefield iron. It stays where it is." |

---

## 5. Micro-events MME01–MME10

Each micro-event follows the Thornfell/Lowmark micro-event card: a place, a visible invitation, one ordinary interaction, an immediate meaning, what it cannot prove. None is required for anything. Flags use the `MME##_` prefix and are read only by the micro-event itself unless stated. No quest items; rewards are a line, a nod, a cup. Suggested content ids `mire.micro.<slug>`. Where a main package already presents a micro-event in passing (Act I: MME01, MME02, MME04, MME08, MME10; Act III: MME01, MME08), the card here is the standing world version and the main's lines take precedence while that main step is active.

### MME01 — Mood banners

| Field | Spec |
|---|---|
| Trigger | Sorrowmere's raised ways (MP01), any time after first arrival. Junction banners on poles. |
| What the player sees | Banners at each junction in one colour. Every few presentation days a Bannerbearer on a ladder changes one. |
| Interaction | Inspect a banner; or ask the Bannerbearer on the ladder (Corra Sallis after MR-M2, otherwise a Bannerbearer role). |
| Lines | BANNERBEARER: "Grey's a burial this week. Green's a birth. Ochre's a way closed." (beat) "Nobody tells us. We ask at doors." · [ochre, MR-M1 or MR-M5 active] "Ochre. The ferry way." / "Ochre. Bannerline." · [green] "Coldwell's had a girl. Don't ask her name yet. They haven't decided." |
| States | Grey / green / ochre on a small authored rotation; main packages pin ochre (MR-M1 ferry way; MR-M5 Bannerline) and release it. |
| Persistence | `MME01_ASKED`. None visible. |
| Repeatable | Always. |
| Cannot prove | Anything about anyone; the colour is a household's news, asked at the door. |

### MME02 — Soil before testimony

| Field | Spec |
|---|---|
| Trigger | Any hearing table: the register room (MP01), the vigil hall (MP03), a Silt hearing set-up in Marshfall. When a witness is about to speak. |
| What the player sees | A clay bowl of dry soil on the table. A witness touches it with two fingers before speaking. |
| Interaction | The player may **touch the soil** (interaction, 1 s) before any dialogue at a hearing table, or not. |
| Lines | WITNESS (if asked): "Habit." (beat) "My gran did it. Keeps your hands honest, she said. I don't know what she meant." · YSOLDE (if the player touches it at the register table): (a small nod; nothing said) |
| Persistence | `MME02_TOUCHED`. Optional idle: the player's character touches the bowl before hearing-table dialogue thereafter (setting). |
| Repeatable | Always. |
| Cannot prove | Anything. A witness who touches soil is no more truthful. Soil-touch rites once grounded grief; now they are manners (dossier §XIII). |

### MME03 — Lantern walk

| Field | Spec |
|---|---|
| Trigger | A raised path in Sorrowmere or Marshfall at dusk, on a grey-banner day (MME01 grey). |
| What the player sees | A line of mourners with lanterns walking at ordinary pace, single file. Nobody overtakes. |
| Interaction | **Walk with them**: fall in at the back (enter the line volume) and walk at their pace to the memorial garden (~60 s). Running past them is possible but the player slows to walk when within 3 m (an ordinary path speed volume), never blocked. |
| Lines | MOURNER (at the garden, to the player): "You walked it. Thank you." · If the player hangs back and does not join: none. · CHILD (in the line): "Why can't we go faster?" / ELDER: "Because we're not going anywhere. We're going with her." |
| Persistence | `MME03_WALKED`. None visible. |
| Repeatable | On grey-banner dusks. |
| Cannot prove | Anything about the dead. "Going with her" is a walk, not a belief about a soul. |

### MME04 — The second place

| Field | Spec |
|---|---|
| Trigger | Any household meal the player sits at (Sorrowmere, Marshfall, Rootrest), when the table has one more place set than people. |
| What the player sees | An empty place set with bowl and spoon; a child puts a small work sign on it (a twist of reed, a peg, a scrap of net). |
| Interaction | Ask about it (dialogue option at the table). |
| Lines | CHILD: "That's for asking after." · ADULT: "It means ask after someone. Who's away. Who we haven't heard from." (beat) "It doesn't mean dead. People think it means dead." |
| Persistence | `MME04_ASKED`. |
| Repeatable | Always. *The Empty Place* (MEP, Names and Lanterns package) builds a quest on this custom; this card is the world custom only. |
| Cannot prove | That anyone is alive or dead. |

### MME05 — Mudstone faces

| Field | Spec |
|---|---|
| Trigger | Field edges after rain (a presentation turn following rain weather), near the causeway head and Nine Stakes. |
| What the player sees | Drying mud on a bank cracked into shapes that look like faces. A child naming them. An elder telling the child to stop. |
| Interaction | **Look** (inspect a face; 2 s). |
| Lines | CHILD: "That one's Old Pudding. That one's cross. That one's asleep." · ELDER: "Stop that. Come away." · CHILD: "Why?" · ELDER: "Because." (that is all) |
| Persistence | `MME05_LOOKED`. |
| Repeatable | After rain. |
| Cannot prove | Anything. **Deliberately unexplained** (bible §7.5). The faces are mud. Nobody says otherwise, and nobody says why the elder minds. |

### MME06 — The Turning Stone

| Field | Spec |
|---|---|
| Trigger | The Turning Stone (MP15) in Sorrowmere, during a mourning rite (a grey-banner day, morning; a small group at the stone). |
| What the player sees | A flat stone, waist high, polished by hands. A mourner lays a hand on it and it turns a finger's width under her palm. |
| Interaction | **Put a hand on it** during the rite (interaction, 2 s). It turns a finger's width for the player too, on the first touch only. |
| Lines | MOURNER: "It does that." (beat) "Not for everyone. Not every time." · MEMORYKEEPER (if asked): "It turns. That's Sennic's story about why. I'm not saying it's so." |
| Persistence | `MME06_TURNED`. Feeds MDS01 (the surface is seen; the reading is separate). |
| Repeatable | The rite repeats on grey days; the stone turns for the player once. |
| Cannot prove | Anything about the dead or the mourner. MDS01 holds what can be learned. |

### MME07 — The does go first

| Field | Spec |
|---|---|
| Trigger | Marshfall Edge peat paths, a fixed spot by a channel bank, first passage after MR-M1 and then on a long rotation. |
| What the player sees | A small herd of fenny does grazing. They lift their heads together and bolt, away from the bank. |
| Interaction | **Follow the does' lead**: move off the bank in their direction within ~10 s. |
| Outcome | ~60 s after the does bolt, the ground shudders and a stretch of peat bank slumps into the channel where the player was standing. A player who followed is on firm ground and watches it go. A player who stayed is caught in the edge of the slump: staggered and slowed, small damage, never into deep water. |
| Lines | MARSHFALL HUNTER (if nearby, after): "Does go first. You go after them. Every child here knows that." · [stayed] "...Most children." |
| Persistence | `MME07_FOLLOWED` (followed at least once). |
| Repeatable | On rotation at authored banks. |
| Cannot prove | What the does sense. The dossier says they flee "long before humans sense anything"; the bank slumped because peat banks slump. Nothing else is implied. |

### MME08 — Story circle

| Field | Spec |
|---|---|
| Trigger | Sorrowmere, an open space by the register room, afternoon: a Memorykeeper and five children on stools. |
| What the player sees | The Memorykeeper teaching children to say whose story it is before telling it. |
| Interaction | **Join** (sit on the spare stool). Then **tell one**: three short options. |
| Lines | MEMORYKEEPER: "Say whose story it is. Then tell it." · CHILD: "This is my gran's story. A heron stole her shoe." · > "This is my story. I crossed the causeway at night." / > "This is Hob Merrit's story. The heron always gets away." [MRS Completed] / > "This is somebody's story. I don't know whose." · MEMORYKEEPER (to the last): "Then say that. 'Somebody's.' That's honest." |
| Persistence | `MME08_TOLD`. |
| Repeatable | Daily; the telling once. |
| Cannot prove | Anything. It is a habit of honesty about sources. |

### MME09 — Banner shadows

| Field | Spec |
|---|---|
| Trigger | The Field of Fallen Standards (MP07) at dusk; any laid or retired standard's pole, or the roadside poles on the causeway after MR-M2. |
| What the player sees | Banners and poles cast shadows longer than they should for the light. |
| Interaction | **Watch** (stand still within 10 m for 10 s), or ask Calwen at his sanctuary later. |
| Lines | CALWEN: "Light bends round heavy cloth here." (beat) "That's all I'll say. It's all I know." |
| Persistence | `MME09_WATCHED`. |
| Repeatable | Every dusk. |
| Cannot prove | Anything. The light is odd; nobody says it means a Wraith will form. (Wraith presentation belongs to the mains.) |

### MME10 — Depth marks

| Field | Spec |
|---|---|
| Trigger | Sorrowmere jetty and the causeway head's painted post (Act I S1, S4), daytime. Children playing. |
| What the player sees | Children jumping on painted depth bands on a post laid flat: pale, ochre, black. Whoever lands on black is "Sour" and sits out. |
| Interaction | **Play**: jump the bands (three jump interactions; land on pale or ochre). |
| Lines | CHILD: "Pale's running! Ochre's slack! Black's sour!" · [player lands on black] CHILD: "You jumped to the black! You're sour! Sit down!" (Act I `MNS-B0.3`) · [player wins] CHILD: "You can cross. Go on, then. Cross." |
| Persistence | `MME10_PLAYED`. |
| Repeatable | Always. |
| Cannot prove | Anything. It is the stake rule as a game; it teaches it before MR-M1 if played first. |

---

## 6. Discoveries MDS01–MDS10 (three-layer framework)

Each discovery has a **surface** (what anyone sees), a **reading** (what a careful player learns, and the interaction that earns it) and, where marked, a **withheld** layer that no Mire content resolves. Discoveries are optional, set no quest steps, and give no rewards beyond understanding. **Flags:** `MDS##_SEEN` (surface seen: entering the authored view volume or first inspect) and `MDS##_READ` (the reading's interaction completed). Both are **persistent booleans on the character**. Suggested ids `mire.discovery.<slug>`. Evidence rule applies: none identifies a person, proves a claim or names the dead.

### MDS01 — The Turning Stone (MP15, Sorrowmere)

| Layer | Content |
|---|---|
| Surface | A flat stone that turns slightly under a hand (MME06). |
| Reading | **Keep watch until Sorrowmere's pool stake reads Slack** and inspect the pool beside the raised way: with the water down, a **ring of sunken stones** shows in the silt, the Turning Stone standing at one point of it. Inspect: *"A ring of stones under the water, sunk almost flat. The Turning Stone is one of them. Somebody set these in a circle."* A Memorykeeper, if asked: "Anchor circle, the old books call it. People gathered here long before anybody remembers why. We still do." |
| Withheld | **Whether the circle did anything.** Never stated. |
| Flags | `MDS01_SEEN` on first inspect of the stone; `MDS01_READ` on the pool inspect at Slack. |
| Links | R08 seed list (bible §8.1); MR-M5's circle is a different ring (no content links them in words). |

### MDS02 — Stillgrave's reflection (MP11, Stillgrave Hollow)

| Layer | Content |
|---|---|
| Surface | Water too clear; lantern light bends over it (Act II S3; dossier). |
| Reading | **At night, hold a lit lantern over the water** at the Hollow's near edge (interaction, 3 s; MR-M3's bow-lantern moss or any lantern). In the reflection, the stilt-stumps along the bank stand whole, with stilt houses on them, roofs and a ladder, where on the bank there are only stumps. Lowering the lantern ends it. Inspect: *"In the water the stumps are houses. On the bank they are stumps."* |
| Withheld | **Why. Never explained** (bible §7.5 deliberately unexplained list). Nobody in the Mire offers a reason. Mabyn, if asked: "I've seen it. I don't look long." |
| Flags | `MDS02_SEEN` entering the near-edge volume; `MDS02_READ` on the lantern interaction at night. |
| Links | Act II leaves this presentation to this file; MRC triggers nothing. Available after MR-M1 (Stillgrave is reachable on foot at the near edge; *The Broken Lantern Light* also goes there). |

### MDS03 — The Sodden Pyres (MP20, Marshfall Edge)

| Layer | Content |
|---|---|
| Surface | Burned trunks standing in wet peat. The peat is warm underfoot; steam rises on cold mornings. |
| Reading | **Kneel and put a hand on the peat** (interaction, 2 s): warm. **Inspect the ironbloom**: rust-coloured fungus runs in long lines between the trunks. Inspect: *"The fungus follows lines through the peat. Where the fire ran under the ground, the ground stayed hot for months, and the iron in it came up."* A Marshfall cutter, if asked: "Smouldered under the bog for half a year after. My grandad said you could cook an egg in it. He said a lot of things." |
| Withheld | — (what burned, and why, is war history the Mire does not state: no unit, no side). |
| Flags | `MDS03_SEEN`; `MDS03_READ` on the hand + fungus inspects. |
| Links | MRH's ironbloom reading (same fungus, same tell). |

### MDS04 — The Dry Muster (MP24, by Griefwatch)

| Layer | Content |
|---|---|
| Surface | Old drill lines worn into the peat, long straight furrows, with a **gap** in them where several lines stop and start again. (Seen on MBO's muster round.) |
| Reading | **Ask Ide Larrow for Griefwatch's chest** in the vigil hall (dialogue; Ide: "It's not locked. Nobody's asked."), and read the **transferred list** inside (inspect): a list copied from an older one, in a careful hand, headed *"Moved through the muster gap."* Lines of *"wounded, on hurdles"*, *"households, with carts"*, *"children with the bell-keeper"*, each with a mark and no names, and at the foot: *"Gap opened at dusk. Closed at first light. Lines reformed."* Inspect the gap again: *"The lines were opened here and closed again. Not broken."* Two holds: the ground and the list. |
| Withheld | **Every claimed motive**: who ordered it, whose lines they were, who was being let through and from what. The list gives no number totalled, no side and no date (weather only: *"after the second fog"*). Griefwatch households each have a story; none is confirmed. |
| Flags | `MDS04_SEEN` on the muster gap volume (MBO sets it in passing); `MDS04_READ` on the list inspect. |
| Links | MBO (the round); MR-M5 (Griefwatch). Nothing depends on it. |

### MDS05 — The Unfired Kiln (MP28, Rootrest)

| Layer | Content |
|---|---|
| Surface | A low clay kiln, never fired, that Rootrest's children use as a rain shelter. |
| Reading | **Crawl in** (interaction; crouch volume) and **inspect the inner wall** by lantern: rows of small pressed marks in the unfired clay, each row a tally, some rows crossed through and most not. Beside some rows a pressed sign: a stake, a stone, a reed. A Rootrest bonecarver, if asked: "Promise marks. Somebody promised a marker for every mark. A stake, a stone. The crossed ones got done." (beat) "Most didn't. There was a retreat." Inspect: *"Promises pressed into clay that was never fired. The uncrossed ones far outnumber the crossed."* |
| Withheld | **Whose promises**, and for whom the markers were meant. No total is stated or countable (the rows are partly broken away; the inspect never gives a number). |
| Flags | `MDS05_SEEN` on approach; `MDS05_READ` on the inner wall inspect. |
| Links | MRW (Rootrest); Mara's markers (thematic only). |

### MDS06 — Bannerline iron (MP12 foot; Griefwatch's closure gate)

| Layer | Content |
|---|---|
| Surface | Red soil at the foot of the Bannerline road and up the ridge; tarnish serpents basking on it on warm turns. |
| Reading | **Inspect the two gate posts** at Griefwatch's closure gate (Act III W1): they are old **palisade stakes**, brought down from the ridge, iron-hard, with nail holes. **Inspect the soil** at their foot: *"Red to a hand's depth. Iron-rich."* **Watch a tarnish serpent** (stand still within 6 m for 8 s): it basks on the reddest patch, its scales the same metallic red. Inspect: *"The ground's red with iron. The snakes like it. The stakes came off the ridge."* After MR-M5 the same reading is available at the Iron Bend's palisade stakes. |
| Withheld | — (the dossier's "iron from bloodshed" is a belief; no line here claims it). |
| Flags | `MDS06_SEEN` on the gate approach; `MDS06_READ` on the stake + soil + serpent. |
| Links | Act III R3 Iron Bend and its ambient serpents (same fauna, not an encounter). |

### MDS07 — The great furrow (below Bannerline; seen from Bran's watchpost, MP17)

| Layer | Content |
|---|---|
| Surface | From the edge of Bran's watchpost platform: a trench ploughed through the peat below the ridge, wide as a road, full of broken weapons and banner rags. No path leads down to it. |
| Reading | **Inspect the furrow from the platform edge**, then **ask Bran** about it (dialogue). BRAN: "Something big walks there when there's fighting." (beat) "Not tonight's trouble." Inspect: *"A trench ploughed through the peat by something huge. Broken weapons and rags of banner in it. It goes out of sight both ways."* |
| Withheld | **The Sorrowback.** Never named, never followed in the Mire arc (bible §2.4; CV-M2). Bran does not say what walks there. |
| Availability | After MR-M2, whenever Bran is at his watchpost: any time before MR-M5 starts, and after MR-M5 completes. While MR-M5 is Active, Bran is at Griefwatch and MR-M5's own `S02` furrow inspect (`MBL-D3.20`) is the presentation. |
| Flags | `MDS07_SEEN` on the platform-edge inspect. **`MDS07_READ`** (persistent bool) when Bran's line has played after the inspect. **Read by Act III** `S02` (`MBL-D3.21`: "You've seen it. Then you know."). **Request to Act III:** after `MBL-D3.20` plays (the player who never read it before), set `MDS07_SEEN` and `MDS07_READ`, so the post-story discovery shows Bran's post-story line ("Still there. Still not tonight's trouble.", Act III §E) instead of repeating the first reading. |
| Links | MR-M5 `S02`; CV-M2 seed (bible §8.2). |

### MDS08 — The Last Root of Sorrow (MP16, Rootrest)

| Layer | Content |
|---|---|
| Surface | A black-rooted tree with white flowers [CANON myth], a rail round it worn smooth by hands. |
| Reading | **Inspect the roots** where they surface across Rootrest's paths: the same black bark in the roots of every old tree in the settlement. A herbalist, if asked: "They're all its children. Grew from its roots, after the burnings." **Accept a griefroot** from a mourner at the rail and hold it there (interaction, 5 s; the root is handed back after). MOURNER: "Hold it. It takes some of the weight. That's what we say." Inspect: *"The black roots run under all of Rootrest. Mourners hold griefroot here."* |
| Withheld | — (the myth stays myth; the root "taking weight" is what mourners say). |
| Flags | `MDS08_SEEN`; `MDS08_READ` on the roots inspect + the held griefroot. |
| Links | MRH (`rootrest`: the antler piece on the rail). |

### MDS09 — The man from the fire roads (Rootrest care-book)

| Layer | Content |
|---|---|
| Surface | Rootrest's care-book on its shelf in the herbalists' room (readable). |
| Reading | **Read the marked entry** (inspect): *"A man come in burned, from the fire roads, he said. Would not give his name. Healed in the hands. Left before the thaw. Said thank you to the roots."* The herbalist: "Nobody here knows more. We wrote what he told us. He didn't tell us much." |
| Withheld | **Held back** (MD-13, braid 12). Nothing says Glassed Hollow; nothing places the fire roads. Read only. |
| Flags | `MDS09_SEEN` on the book; `MDS09_READ` on the entry. Reserved for the Emberholt bible as a possible read (R09 seed, bible §8.2); no Mire content reads it. |
| Links | None in the Mire. |

### MDS10 — Mirebone Crossing (MP10, a Blackwater edge)

| Layer | Content |
|---|---|
| Surface | A ford littered with bone: old, pale, many. Birds and does avoid it. The ground shivers underfoot at the water's edge. |
| Reading | **Inspect the near stake** the Marshwardens tried to set there: it lies flat, pulled over by the silt. **Keep watch one turn and inspect the ford again**: the shallow line across has moved; the bones lie in a different line. A Marshwarden's note on the stake: *"No stake holds here. Ford moves every turn. Don't."* Inspect: *"The ford is somewhere else since you last looked. The bones are old and many. Nothing holds a stake here."* |
| Withheld | **Its future** (convergence role provisional, MD-9). No content here builds toward it. Whose bones is withheld: no count, no side. |
| Traversal | The ford is wadeable a few steps from the near bank; beyond that the silt is non-walkable. No far-side destination is described; this is not a route (MD-9, FT-03). **MAP VERIFICATION REQUIRED.** |
| Flags | `MDS10_SEEN` on the bank volume; `MDS10_READ` on the second inspect after a turn. |
| Links | None. |

---

## 7. File-level integration summary

| Need | Used by | Owner | Notes / fallback |
|---|---|---|---|
| Keep watch / presentation hour | All four quests; MME01/03/06/07; MDS01/02/10 | Systems | Lowmark convention; per-player, never world time. |
| Channel states (N-1) | MNK, MRW, MDS01, MDS10 | Systems | Quest-pinned or authored states as fallback. |
| Lantern-moss posts and caps (dark / lit) | MBO, MNK | Systems / VFX | Same prop family as MR-M1 and MR-M4. |
| Bell rope at night turns | MBO | Systems | Channelled interaction gated by hour. |
| Stake/socket matching | MNK | Systems | Id match plus facing. |
| Patch-seeking boss AI with thinning patches | MRH | Gameplay / AI | Standard move-to-tag loop; decal swap. |
| Interruptible re-coat buff | MNK Mud-Boss | Gameplay | Standard. |
| Range inspect | MNK | Systems | Line-of-sight inspect. |
| Scripted light sequences (answering lamps; moss caps; reflection) | MBO, MNK, MDS02 | VFX | Event-driven prop states. |
| Per-player props | All | Systems | Host fallback. |
| Quest-start skill requirement | MRH | Systems / Schema | Standard requirement check on accept. |
| Persistent discovery booleans | MDS01–MDS10 | Schema | `MDS##_SEEN` / `MDS##_READ`; **`MDS07_READ` is read by Act III**. |

No runtime need beyond bible §11.1–11.2 and standard requirement checks.

## 8. Package review summary

| Check | Result |
|---|---|
| Brief fit (bible §7.2–7.5) | MBO, MRW, MNK, MRH match their slate rows and contracts (MBO Bog Hounds on the Dry Muster and a roster-rule choice; MRW no combat, no fail; MNK Raiders and the Mud-Boss to 0 HP, no fail; MRH the Rust Hart to 0 HP, harvestable). MME01–MME10 and MDS01–MDS10 match §7.4/§7.5 entry for entry; MDS02, MDS05 (MME05) and MDS07's withheld layers kept. |
| Mains' reads | **MBO Completed** at `S07_book` with the vigil book's keeper column in its fixed form (Act III `MBL-D1.03` and the vigil-book inspect). **`MDS07_READ`** set by MDS07's reading (persistent bool), listed in §0.2; request to Act III to set it after `MBL-D3.20`. *Lifting Day* and *A Table for the Wet* are not in this file (MLD: Names and Lanterns package; MFT: Work and Skills package, completion at `S06_table`). |
| CDR-1 | Every enemy to 0 HP; the Mud-Boss's call and the Hart's bellow are phase barks; no yield, flee or scatter; no SX; no defeated enemy speaks. |
| CDR-2 | Melee and ranged both viable in every fight; MNK slingers, the Boss's re-coat and the Hart's charge are designed so neither style trivialises them; nothing requires ranged. |
| CDR-3 | No release wording. |
| CDR-4 | Standard systems; MRH carries a light Hunting requirement (`[GD]`). |
| Dating and R08 | No calendar date, weekday or year anywhere; history dated by weather or bell-nights. No unit, side or casualty count; MDS04, MDS05 and MDS10 state no figure. |
| Evidence rule | Facts from the vigil book, roster, doors, ferry book, transferred list, care-book and living witnesses. Phenomena (the far light, moss caps crossing, chimes, reflection, mudstone faces) prove nothing. |
| MD-7 | No Hollowfoot content anywhere in this file; every quest carries a "no change" swap note. |
| `[CAUSEWAY]` | MNK hook and `MNK-B0` tagged. |
| Quest items | 0. |
| New names checked for collisions | Tibb Ormer, Elin and Aldous Copse, Corwin and Hessel Tey, Gilly Ruddle, Halsey Fenner, Annot Reeve, Varne (ferry book): grepped against the repository; no collisions outside this file. |
| Deviations from the bible | (1) MBO's Ridge Warden is a role (no name), matching Act III. (2) MDS07 is available before MR-M5 at Bran's watchpost (Bran is there by canon) and after; during MR-M5, Act III's own inspect presents it. (3) MRH's quest-start Hunting requirement (bible §13 recommendation). |
