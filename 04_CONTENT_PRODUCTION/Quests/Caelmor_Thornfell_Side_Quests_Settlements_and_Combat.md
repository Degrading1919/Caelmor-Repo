# Thornfell Side Quests — Settlements and Combat Challenges

**Status (2026-11-02):** Authored production content for Creative Director milestone review (Thornfell bible §12, batch 3). Four side-quest packages, ten micro-events and ten discoveries: two settlement stories (**TMM** *The Mason's Margin*, **TAS** *Ash in the Snow*), two combat challenges (**TGM** *Greymantle*, **TSG** *The Salvage Ledge*), micro-events **TME01–TME10** and discoveries **TDS01–TDS10** (the bible's file map calls them TD01–TD10; the bible's own review log fixed the id to `TDS##`, which this file uses). Everything marked **[NEW]** is authored here and is not canon until the Director promotes it. **[CANON]** items come from the reconciled `LORE/` files. **[APPROVED — id]** marks an approved architecture ruling. **[PROPOSAL — DIRECTOR]** marks a consequential choice the content is built on. No schema, JSON or C# is created here. **Reconciled 2026-11-03** to the binding Creative Director rulings in `Caelmor_Director_Rulings_Combat_Ranged_Release.md` (CDR-1 defeat at 0 HP; CDR-2 Ranged included; CDR-3 internal-milestone wording); see §8.

**Controlled by:** `Caelmor_Thornfell_Narrative_Production_Bible.md` (author truth §2, director decisions §3, POIs §4, cast and voice §5, slate §7.2–7.4, revelation map §8, flags §9, encounter families §10, conventions §11). **Format:** the Lowmark side-quest packages (`Caelmor_Lowmark_Side_Quests_Settlements_and_Combat.md`, micro-events in `Caelmor_Lowmark_Side_Quests_Discovery_and_Memory.md` §8) and the act-package depth of `Caelmor_Lowmark_Main_Act_I.md` Part C. **Dialogue** for all four quests is inline in each package (§x.18), in the Lowmark node format (`NODE SPEAKER: "Line." (stage note)`, `> [condition] "Option." → NEXT {effect}`), with node ids `<CODE>-D<n>.<nn>`, barks `<CODE>-B<n>.<nn>` and inspect texts `<CODE>-I<n>`.

**Scope guard.** Thornfell is the second internal production milestone (CDR-3: there is no partial public release). Nothing here grows scope. Technical needs are documented dependencies for a later Systems Engineer (bible §12, batch 4 integration handoff), never implementations.

---

## 0. Slate header

### 0.1 The four quests at a glance

| Code | Quest | Type (Phase 1.5) | Unlock gate | Where | Core verb (primary first) | Identity in one line | Feeds |
|---|---|---|---|---|---|---|---|
| **TMM** | The Mason's Margin | Settlement (Stonewake) | TF-M2 *The Iron Winter Stores* Completed | Stonewright Quarter, Signal Terrace, Assembly Hall stair, market cistern (TP01); Hushfold (TP04) | **measure**, reconcile, decide | An audit done with a rod, a knotted cord and a lantern: the account says forty courses, the wall says twelve. | `TMM_ACCOUNT` (TF-M5 Hadrik lines, request); `TMM_BUNDLE_SEEN` (LR-M1 recognition line, request); plants the Stonewright Quarter's sealed "Lowmark work, war years" bundle (R13 seed) |
| **TAS** | Ash in the Snow | Settlement (Passwatch) | TF-M1 *The Closing of Passwatch* Completed | Passwatch gate, cold shed, horn post (TP02); the Blind Corners (TP26) | **protect**, test, repair, de-escalate | Keep four Emberholt masons safe through one cold night and set new iron in Passwatch's gate arch while a tower crew watches every spark. | `TAS_ACCOUNT` (Emberholt repair-credit callback, request; braid 9) |
| **TGM** | Greymantle | Combat challenge (miniboss) | TF-M2 Completed | Stormwake shoulder, Black Glass Hostel yard (TP05), Greymantle's Den (TP25) | **track**, fight in silence | Follow an old bear's limp through snow, then fight him where no sound carries: every tell is sight and dust. | `TGM_OUTCOME` (hostel and Yrsa barks; den prop) |
| **TSG** | The Salvage Ledge | Combat challenge | TF-M3 *The Echo of Shatterfall* Completed | The Salvage Ledge (TP12), Carrick's Cut (TP13), the Horn Seat (TP10) | **assault**, warn, hold | Take a brigand camp on a gorge ledge, then run the ledge's lip blowing Fall to three warden pairs below while cutters work at the prop stones. | `TSG_LEDGE`, `TSG_SPOIL` (Gerrit and Warden barks; *Seam Rights* cameo line, request) |

**Recommended order of discovery** (not enforced): TAS is the first offer most players meet, at Passwatch right after TF-M1. TMM and TGM open together after TF-M2, at Stonewake and on the Stormwake road, and TF-M2's first snow (`TH_SEASON` = snow) gives TGM its tracking snow. TSG opens after TF-M3, when the player knows the Horn Seat and Gerrit Carrick.

### 0.2 Flags other packages read

| Flag | Values | Set by | Read by | Effect |
|---|---|---|---|---|
| `TMM_ACCOUNT` | opened / amended / kept | TMM `S08_decide` | TF-M5 aftermath (request); Stonewake barks | One Hadrik line before the Assembly sits (TMM.11). **Does not enter the §9.3 posture count.** Nothing breaks if unread. |
| `TMM_BUNDLE_SEEN` | bool | TMM `S01_account` (always set: the pass-by inspect is guaranteed) | LR-M1 (request) | A recognition line when the Lowmark return asks for "a Thornfell work log": the player has seen where it sits. LR-M1 owns the custodian; this flag is never a gate. |
| `TAS_ACCOUNT` | named / held / unwritten | TAS `S07_book` | Emberholt content (request; braid 9, "Emberholt owns public worker credit"); Passwatch barks | Whether Passwatch's gate book names the Emberholt crew who set its cramps. A later Emberholt guild scene may read it for one line. Never required. |
| `TAS_PROOF` | proof / watch / ruled | TAS `S04_tower` | TAS lines only | Which way the tower crew was talked down. |
| `TGM_OUTCOME` | ended / sleeping | TGM `S06_choice` | Black Glass Hostel barks; *The Snow-Height Mark* (Halla, one optional line, request) | How the old bear was left: `ended` = left to the trappers (empty den), `sleeping` = den sealed as his resting place (stacked mouth and net). Yrsa's barks. |
| `TSG_LEDGE` | licensed / struck | TSG `S07_choice` | *Seam Rights* (Gerrit cameo line, request); Carrick's Cut barks | Whether Gerrit's crew works the ledge again under Warden licence. |
| `TSG_SPOIL` | held / dropped | TSG `S05_props` | TSG lines; ledge path prop | Whether the spoil terrace still stands. Both outcomes are safe for every warden. |
| *(read)* `TH_CALLS` | bool | TF-M1 | TAS, TSG, TME05, TME10, TDS03, TDS10 | Call glyphs display. TSG and TDS10 require the calls; TF-M1 is a prerequisite of their unlocks, so this always holds. |
| *(read)* `TH_SEASON` | autumn / snow | TF-M2 | TAS (sleet or snow), TGM (snow) | Presentation only. TGM unlocks after TF-M2, so it always has snow. |
| *(read)* `TH_STORES`, `TH_BRYNJAR` | enum | TF-M2 | TMM, TAS | One variant line each (TMM-D5, TAS-B6). |
| *(read)* TF-M4 Completed (`TSH_trial_record` read) | bool | TF-M4 | TGM | One extra date agreement in `S02b_dates`. |
| *(read)* `TH_SHATTERFALL_ACCOUNT` | amended / beside / kept | TF-M3 | TSG | Dorn's line at the Horn Seat rack. |
| *(read)* `TME01_TALLIED` or `TSM_PLAYER_TALLIED` | bool | TME01; TSM | TMM-D3 | Runa uses the player's name (bible §5.3 rule 4). |

No new `TH_` region flags are created. All quest-local flags use the quest code prefix. "(request)" marks a line asked of another package that nothing depends on.

### 0.3 Shared rules for all four packages

- **Quest items: none.** The bible's Thornfell budget is four, all spent by the milestones (§9.5). Every carried thing in this file (the repair account, the reconciliation slate, the cramp bundle, the plate crate) is a **carry-state object**. Reward tools are named functionally and need the item pass.
- **Three states only.** Inactive, Active, Completed. No quest can fail or be abandoned. Walking away keeps the quest Active at its persisted step; each package names its resume hook (default: the original offer node, with a "where were we" variant). Choices are outcome flags with costs. Every required proof has a guaranteed path.
- **Death** respawns at the quest's named safe point with step and flags intact. **Logout** restores the last persisted step; channels and carries are discarded, and a dropped carry-state object returns to its source. Completed channel segments persist (Lowmark convention).
- **Every enemy is defeated at 0 HP** (CDR-1; TD-7 superseded): pass bandits, Shatterfall brigands, Greymantle, ridge wolves and crows alike. No yield, no downed state, no break-off; defeated humans take the ordinary defeat presentation (no gore, no tied props, no dialogue afterwards). Every encounter can be fought in melee or at range (CDR-2); none requires ranged.
- **Evidence rule** (bible §11.3). Records (the repair account, the dray book, Hushfold's tally, Vessa's gate book, Yrsa's tally stick, the hostel weather slate), objects (cramps, treads, plates, prop timbers) and testimony carry every fact. Combat drops nothing that advances an investigation. The hall that carries voices, the arch's note, the silent roar and the ringing plates identify nobody and prove nothing.
- **Sound system** (bible §1.1). Every quest here uses it, each differently: TMM counts courses and lets a hall carry a voice; TAS tests iron by its ring; TGM takes sound away; TSG makes the player the one blowing the calls.
- **Agility triggers** are optional shortcuts; each has a walkable fallback named in its place table (click-to-move friendly; no input timing anywhere in this file).
- **Skills** (all with a crew alternative where a step uses them): Smithing (TAS), Mining (TSG, optional), Melee or Ranged (TAS, TGM, TSG), Hunting (TGM, optional butchering). Exact levels belong to the Gameplay Designer (TD-12).
- **Map.** Relative placement only. **MAP VERIFICATION REQUIRED** is marked wherever geometry matters.
- **Voice.** Bible §5.3: understated, dry, weather as grammar, nobody calls anything magic, strangers are "walker". A host who has added the player to a shelter tally (TME01) uses their name, written here as `{PLAYER}` (the Act III token).

### 0.4 Distinctness check

| Quest | What the player physically does | Not the same as |
|---|---|---|
| TMM | Measures built stone against a written account (counts fresh courses, reads tread wear, runs a knotted cord along a cistern), follows the difference to four roofs, reads a margin aloud in a hall | TIW (reads a criminal ledger in a dungeon); TSR (taps rock for voids); no combat |
| TAS | Tests iron cramps by their ring, recovers a cached bundle, holds a gate yard through one night, sets new iron at a forge between gusts | TF-M1 (bridge rebuild against a clock); TBC (triage plan for a cracked bridge) |
| TGM | Tracks one animal across snow by prints, hair, crows and frost dust; fights it in a sound-dead den by sight alone | TGY (herd management with calls); TF-M4 (null-points as a puzzle, not an arena) |
| TSG | Assaults a fortified ledge in two parts, then runs three call points blowing Fall and reads the Answers while stopping prop cutters | TF-M3 (rope-rig rescue by echo count under the Horn-Echo); TF-M5 (climbs toward other people's calls) |

---

## TMM — The Mason's Margin

### TMM.1 The quest in one paragraph

Two apprentices of Stonewake's Stonewright Quarter, Ivra and Kel, were sent to chalk this autumn's repairs into the Quarter's yard book and found that the Assembly's repair account and the stone do not agree. The account says forty new courses on the Signal Terrace parapet, twelve recut treads on the Assembly Hall stair and sixty ells of new lining in the market cistern. The player takes the account down from the Quarter's log shelf, past a sealed bundle nobody opens, and measures: by fresh tool marks on a scaffold plank in the hard wind, by the old wear hidden on the underside of turned treads, by a knotted cord run along a cistern wall in lantern light. The difference is about four roofs of slate and two lintels. The dray book sends four loads "to Ridgewall" in leaf-fall; at **Hushfold**, the clanless shelter line, four houses have new roofs, and one lintel carries Ivra's own banker mark. Runa Weatherall's tally says the Quarter's masons came, made the roofs sound and asked nothing. Back in the Quarter, the master of works admits the margin, and a slip tucked in the account's back board, in the Speaker's hand, says *"Roofs before snow. Charge it to the terrace. I'll sign."* At night, reading the three lines aloud on the speaking stone, the player hears the Assembly Hall carry their voice to the dark gallery, where Hadrik Stonewake is sitting. Hadrik hid it to keep the Assembly from tearing itself apart over whether clanless roofs deserved Assembly stone in the same season as the stores. He asks the player where they will stand: lay it before the Assembly, write it true in the book and say nothing, or keep the margin.

**Remember:** your own voice coming back from the far gallery a breath late, and a man answering it from the dark. **Want next:** to know what is in the sealed bundle on the war shelf.

### TMM.2 Selection record

| Candidate | Verdict |
|---|---|
| **A. A thief in the Quarter.** Someone is skimming the repair money; the player catches them. | Rejected. Makes the story a crime, duplicates TIW's ledger, and makes Hadrik a culprit. The bible pitch is a *useful* secret. |
| **B. An Assembly hearing.** The player argues the case on the floor. | Rejected. Talk-led resolution only in closing beats (bible §7.2 structure check); TF-M5 owns the Assembly scene. |
| **C. Measure the stone → reconcile → follow the margin to Hushfold → hear the hall carry it → choose** | **Selected.** The audit is physical (rod, cord, lantern, scaffold), the evidence is stone plus record plus testimony, and the choice puts the player where Hadrik usually puts others. |

### TMM.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Hadrik Stonewake: a buffer, not a ruler; lets arguments burn out; knows the hall amplifies some voices and never asks why; chooses where people stand | Thornfell anchors I | [CANON] |
| Stonewake's terraces, Signal Terrace, Stonewright Quarter with dwarven influence, ridge-markets | Dossier §VI.1 | [CANON] |
| Hearthguard acoustic stonework called "good old building" | Thornfell anchors II (Elira) | [CANON] |
| Hushfold: wartime shelter line, clanless households doing route labour without an agreed Assembly voice | Part 3 Thornfell proposal; bible TP04, TD-4 | [NEW, Part 3] adopted |
| *The Mason's Margin* pitch: accounts vs visible work; money diverted to shelter repairs; a useful secret and Hadrik's legitimacy | Part 3 Thornfell proposal, story 4; bible §7.2 | Proposal adopted by the bible |
| A Thornfell engineering work log as the second custodian of R13; Kaldren is not its author | Revelation Ledger R13; Arcs LR-M1; bible §8.2 | [APPROVED — FT-02a] for the revelation; the log's custody [PROPOSAL] |
| Ivra, Kel, Sefa Dunholt, the margin, Hadrik's slip, the war shelf | This package | [NEW] |

### TMM.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.masons_margin` |
| Type | Settlement story, Stonewake (bible §7.2) |
| Unlock | TF-M2 Completed. Offered by Ivra at the Stonewright Quarter's measuring yard (bark `TMM-B1` on passing; dialogue `TMM-D1`). |
| Resume hook | Ivra at the measuring yard: `TMM-D1.00` "where were we" variant pins the current step. |
| Target length | 30–40 minutes |
| Combat share | 0%. One environmental hazard (terrace gusts). |
| Skills | None required. Measuring uses lent tools (the Quarter's rod and cord; no item). |
| Choice | What becomes of the margin (3 options; each costs something) |
| Outputs | `TMM_ACCOUNT` = opened / amended / kept; `TMM_BUNDLE_SEEN` |
| **Anchor** | Stonewake's Stonewright Quarter and the Assembly (Hadrik Stonewake); Hushfold's shelter line |
| **World-truth row** | H23 (thirty years of uneven recovery: repair, disputed credit); H25 present pressure (a season of hoarding makes shelter stone contested). The bundle touches H10 as a seed only. |
| **Revelation role** | Self-contained story. **Plants R13** (the sealed "Lowmark work, war years" bundle: seen, not opened; LR-M1 owns it). Supports the §8.3 misunderstanding ladder for Hushfold ("the people who do the far-side work"). |
| **Recurring evidence** | The sealed bundle recurs in LR-M1; its independent counterpart custodian there is the Fenmere ledgers. Hushfold's tally books recur (TME04, *A Place at Smoke Week*, TF-M5); this quest reads only this autumn's page. Hadrik recurs at TF-M5. |
| **State compliance** | Inactive / Active / Completed; outcome flag `TMM_ACCOUNT`; no fail path; the bundle has no open interaction; walking away keeps the persisted step with Ivra's resume hook. |

### TMM.5 The places

#### TMM.5.1 Stonewright Quarter (TP01) [NEW detail on CANON place]

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **Q1. Measuring yard** | Hook, slate, return | A walled yard of cut blocks waiting under sacking. A long stone bench with a groove cut along it, one ell exactly, worn shiny by a hundred years of rods laid in it. A chalk wall where apprentices tally the season's work. Every doorway in the Quarter has a scuffed patch on the lintel at tapping height (TME02). |
| **Q2. Sefa's work room and the log shelf** | Account, bundle, the margin | Plans pinned under stone weights. The **log shelf**: account books by year, spines lettered in white. One end of the shelf is a separate bay with a lip, older wood: the **war shelf**. On it, one **sealed bundle** in oilcloth, cord and the Quarter's wax, with a wooden tag: *"Lowmark work, war years."* Dust on the bundle, none on the shelf around it: someone dusts the shelf and leaves the bundle alone. |
| **Q3. Dray shed** | Dray book | Two drays, harness on pegs, a lectern with the **dray book**. A chalk sum on the post: *"Ridgewall, 4."* Lime dust on the floor in a trail toward the yard gate. |

#### TMM.5.2 The three measured works (Stonewake)

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **M1. Signal Terrace parapet** | Count fresh courses (outer face) | The horn terrace on the cliff edge. From the terrace the parapet's inner face looks entirely new: it was **repointed**, and fresh mortar makes old stone look young. Only the outer face, over the drop, shows which courses carry fresh claw-chisel drag marks and which carry old weathering pits. A mason's hanging plank on ropes, left from the work. | **Agility trigger:** step down from the parapet onto the plank. **Walkable fallback:** the Quarter's hoist cage at the terrace end (crank it; it lowers to the plank level, the same crank-cage convention as the Whinstone hoist in TF-M2). |
| **M2. Assembly Hall great stair** | Read twelve treads | Broad stair up to the hall doors. Every tread looks fresh-faced. A **turned** tread was lifted, flipped and reset: its new top is the old underside, clean, but its riser edge shows an old worn hollow facing **down** into the joint. A recut tread has crisp edges on both faces. Clansfolk going up and down; a hall attendant (role) tuts at anyone kneeling. | None. |
| **M3. Market cistern** | Measure new lining | Under the ridge-market, reached by a ladder through a grate. A long vaulted tank, knee-deep at the far end. New lime lining is white and dry-looking; old lining is grey, with a tide-line. Marker pins every ten ells, set in the war or before. Water drips in the old section and nowhere in the new. | Ladder. Wading section slows movement; no hazard. |

#### TMM.5.3 Hushfold (TP04) and the Assembly Hall at night

| Area | Purpose | Environmental storytelling |
|---|---|---|
| **H1. Hushfold shelter houses** | Count new roofs; banker marks | Low stone houses along a ridge shelf, mismatched: some walls clan-built, some patched with whatever came. **Four** have new slate roofs and two have new door lintels. Banker marks (each cutter's private sign) are cut on the hidden face of each lintel, readable from inside the doorway. One mark is a small hook: Ivra's. Children have drawn the hook in charcoal on a wall, copying it. |
| **H2. Tally hut** | Runa's tally page | A one-room hut with the shelter line's tally books on a board shelf, newest at the end. A cold hearth with First Smoke kindling already laid. |
| **N1. The Assembly Hall at night** | Strange moment; Hadrik | The hall cut into the cliff, its curved ceiling carved in shallow grooves. A **speaking stone** at the floor's centre. Galleries in the dark on three sides. One lamp burning by the door. Hadrik sits in the far gallery where he can see the stone, as he does most nights after a sitting [NEW habit, within canon]. |

**MAP VERIFICATION REQUIRED:** the Signal Terrace sits on a cliff edge with an outer face over a drop; the market cistern is under the ridge-market; Hushfold is reachable from Stonewake in a few minutes' travel on Ridgewall paths. Nothing else here depends on geometry.

### TMM.6 Player-facing sequence

**Beat 0 — The book and the wall (`S00_hook`).** *Objective: Hear out the apprentices.* At the measuring yard Ivra is arguing with a chalk wall and Kel is trying to make her stop (`TMM-D1`). Their job was to chalk the autumn repairs into the yard tally from the Assembly's repair account; Ivra went to look at the terrace and says forty courses is a lie. Kel says the master will have reasons. Neither of them can take the account off the shelf without the master; the master is "at the Hall"; the player is a stranger and nobody told strangers not to. **Verbs:** listen.

**Beat 1 — The account (`S01_account`).** *Objective: Take the repair account from the Quarter's log shelf.* In Sefa's work room (Q2) the player takes this year's account (carry-state; light carry). Reaching for it sets off Kel's bark at the war shelf (`TMM-B2`), and the **sealed bundle** is inspectable (`TMM-I2`; sets `TMM_BUNDLE_SEEN` on the bark or the inspect, so it is always set). There is **no** interaction to open, cut or lift the bundle. Three account lines are read from the book (required inspects, `TMM-I3`). Ivra lends the Quarter's measuring rod and knotted cord (tools for this quest only; no item). **Verbs:** take, read.

**Beat 2 — Measure (`S02_measure`).** *Objective: Measure the three repairs against the account.* Three sites, any order (`S02a`–`S02c`). Each ends by chalking a line on the **reconciliation slate** Ivra carries (presented as a per-player slate prop at the yard; the line appears when the site is done).

| Sub-step | Site | What the player does | Result chalked |
|---|---|---|---|
| `S02a_terrace` | M1 Signal Terrace | Reach the hanging plank (agility step-down or hoist cage). On the plank, three **course inspects** along the outer face show fresh drag marks on the lower courses only; Ivra on the parapet calls out the count as the player points. **Hazard:** gusts (TMM-H1). The fluted faces below the terrace whistle up a fifth about 1.5 s before each gust; the player steps into the buttress niche at the plank's end and waits it out. | *"Terrace. Account 40. Stone 12."* |
| `S02b_stair` | M2 Hall stair | Kneel at three riser joints (lower, middle and upper flights; required inspects). Each shows recut or turned. Kel, who knows treads, counts the rest from the first three ("Same hand did all the turned ones. You can see it."). | *"Stair. Account 12 recut. Stone 4 recut, 8 turned."* |
| `S02c_cistern` | M3 Cistern | Climb down; light the hook lantern at the ladder foot (interaction). **Run the cord**: a channelled walk along the wall from the first marker pin, paying out the knotted cord; the channel stops itself where the white lining ends (enter the end-of-new-lining volume). Count the knots (inspect the cord: 22). Optional: the tide-line inspect and the drip. | *"Cistern. Account 60 ells. Stone 22."* |

**Beat 3 — The margin (`S03_slate`).** *Objective: Show Ivra the slate.* Back at the yard (`TMM-D2`). Ivra does the sum aloud in stone, not money: twenty-eight courses, eight treads, thirty-eight ells of lime. "That's four roofs of slate. Maybe two lintels." Kel: "Roofs where?" **Verbs:** reconcile.

**Beat 4 — Where the stone went (`S04_dray`).** *Objective: Find where the stone went.* The dray shed (Q3): read the dray book (required inspect `TMM-I5`): four loads, *"Ridgewall. Slate, lime. S.D."*, in leaf-fall. Optional: the chalk sum on the post. Kel says Ridgewall is a big word, and the only work the Quarter does up there is at the highsteads. Ivra: "I cut lintels in leaf-fall. For the terrace stair, he said." **Verbs:** read, track.

**Beat 5 — Hushfold (`S05_hushfold`).** *Objective: Look at Hushfold's new roofs.* At Hushfold the player:
- counts **four new roofs** (one volume each; any order; the objective counter ticks);
- reads the **banker marks** on the two new lintels from inside the doorways (required inspects; one is Ivra's hook, one is Kel's mark, a little square);
- **taps the lintel** (the TME02 habit; optional): a tight clean ring. Kel, if he came: "Sound. Good work. Mine and hers."
- asks **Runa Weatherall** at the tally hut (`TMM-D3`); she shows this autumn's tally page (required inspect `TMM-I7`): the Quarter's masons came for four days, made the roofs sound and asked nothing. She thanked "the Quarter" and believes it was the masons' own kindness.
Ivra comes up to Hushfold behind the player (she is not escorted; she arrives during the beat) and stands looking at her own mark. **Verbs:** count, read, ask.

**Beat 6 — The master (`S06_margin`).** *Objective: Ask the master of works about the margin.* Sefa Dunholt is back in her work room (`TMM-D4`). She does not deny it. She shows the account's margin: a small roof sign pencilled beside each inflated line. From the account's back board she draws a folded slip (required inspect `TMM-I8`): *"Roofs before snow. Charge it to the terrace. I'll sign. H."* She says the Speaker signed every page, as he signs every account, and knew what he was signing. She will not say more for him: "Ask him. He's in the Hall. He always is, after." **Verbs:** confront, read.

**Beat 7 — The hall (`S07_hall`).** *Objective: Find Hadrik in the Assembly Hall.* Night (keep-watch at the hall doors, one step, if the player arrives by day). The hall is empty, one lamp by the door. The objective changes on entering: *Read the slate on the speaking stone.* The player sets the slate on the stone and reads the three lines (interaction). **The strange moment** (TMM.8): the hall carries the player's voice to the dark gallery, a breath late and louder than they spoke; on the third line a man's ordinary voice answers from the far gallery and arrives as if spoken at the player's shoulder. Hadrik comes down the gallery stair (`TMM-D5`). **Verbs:** read aloud, listen.

**Beat 8 — Where it stands (`S08_decide`).** *Objective: Decide what becomes of the margin.* `TMM-D5` continues to the choice (TMM.11). Hadrik tells it plainly: the Assembly was already at each other's throats over the stores; a vote on whether clanless roofs deserved Assembly stone would have split the hall before snow, and the roofs would not have been done. He does not say he was right. He says the roofs are done. Then he does what he always does, the other way round: "You've found it. So you stand somewhere. Where?" **Verbs:** decide.

**Beat 9 — The yard (`S09_close`).** *Objective: Tell the apprentices.* `TMM-D6` at the measuring yard: Ivra and Kel, with the outcome. The chalk wall shows the result (TMM.11). Quest Completed.

### TMM.7 Encounters

No combat. The quest's danger is height and wind.

| Id | Hazard | Placement | Behaviour | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TMM-H1** | Terrace gust | Hanging plank under the Signal Terrace (M1) | Every 12–18 s a gust crosses the plank. A player standing outside the buttress niche is pushed along the plank (2 m, never off it) and their current inspect is cancelled. | The fluted faces below whistle up **a fifth, ~1.5 s** before the gust; the call-glyph area shows a small rising-wind glyph for accessibility (bible §9.5 wind-window convention). Snow or grit lifts off the plank edge in the last 0.5 s. | Teaches the wind window to a player who skipped TF-M1's set piece; keeps a measuring step physical. | Three inspects in about 60–90 s. |

**Rules.** No step needs a fight. Being pushed costs nothing but time. Falling is impossible: the plank has a rope rail and the push is clamped.

### TMM.8 The strange moment: the hall carries it (presentation spec)

Builds on Hadrik's canon (the hall amplifies certain voices; he never asks why). Player camera throughout; no cutscene; no music.

| Time | Element | Spec |
|---|---|---|
| Entry | **The empty hall** | Hall ambience low: the lamp's hiss, wind at the doors, nothing else. The galleries are dark. The speaking stone is lit by the single lamp. No figure visible. |
| 0 s | **Set the slate** | Interaction on the stone (1 s). Objective text hides. |
| 1–4 s | **First line** | The player's character reads line one in their own voice (the voiced line is the slate text, `TMM-D5.01`; subtitle). Ordinary room response. |
| 4–8 s | **Second line** | As the character reads, a delayed copy of their voice returns from the **far gallery** (~0.4 s late, louder than the original, with a dry, close character, as if spoken into an ear). Dust sifts from one ceiling groove above the gallery and nowhere else. |
| 8–12 s | **Third line** | The return is now almost as loud as the original. Halfway through the line, **a second voice** joins from the far gallery: Hadrik, speaking normally, *"Twenty-two ells."*, and his voice arrives at the player's shoulder, close and quiet, though he is thirty paces away in the dark. |
| 12–18 s | **Walk down** | A lamp is unshuttered in the far gallery: Hadrik, seated, in his coat. He stands and comes down the gallery stair at an old man's pace. Footsteps in the hall sound ordinary again. |
| After | **The line** | `TMM-D5.02` HADRIK: "It does that. I don't ask why." No one explains the hall. |
| UI | | No popup until `TMM-D5` begins. Subtitles carry a direction marker "(from the far gallery)" for the returns and for Hadrik's first line (accessibility). |

**Cannot prove:** anything. It is the hall. Hadrik already knew the numbers; he heard them because he was listening.

### TMM.9 Steps and completion events

| Step | Objective | Completes on | Req. | Notes |
|---|---|---|---|---|
| `S00_hook` | Hear out the apprentices. | `TMM-D1` end node | Yes | Inactive → Active |
| `S01_account` | Take the repair account from the Quarter's log shelf. | Pickup of account (carry-state) + 3 inspects (`TMM-I3`) | Yes | `TMM-B2` plays on pickup and sets `TMM_BUNDLE_SEEN`; inspect `TMM-I2` also sets it |
| `S02a_terrace` | Measure the terrace parapet. | 3 course inspects on the outer face | Yes (any order) | Slate line 1 |
| `S02b_stair` | Measure the hall stair. | 3 riser-joint inspects | Yes (any order) | Slate line 2 |
| `S02c_cistern` | Measure the cistern lining. | Lantern lit + cord-run channel reaches end volume + cord inspect | Yes (any order) | Slate line 3; channel progress persists |
| `S03_slate` | Show Ivra the slate. | `TMM-D2` end node | Yes | |
| `S04_dray` | Find where the stone went. | Inspect dray book `TMM-I5` | Yes | |
| `S05_hushfold` | Look at Hushfold's new roofs. | 4 roof volumes + 2 lintel inspects + `TMM-I7` (via `TMM-D3`) | Yes | Lintel tap optional (`TMM_TAPPED`) |
| `S06_margin` | Ask the master of works about the margin. | `TMM-D4` reaches `TMM-D4.20` + inspect slip `TMM-I8` | Yes | |
| `S07_hall` | Find Hadrik in the Assembly Hall. | Enter hall volume at night (keep-watch if needed) + speaking-stone interaction + presentation end | Yes | |
| `S08_decide` | Decide what becomes of the margin. | `TMM-D5` choice node resolved | Yes | Sets `TMM_ACCOUNT` |
| `S09_close` | Tell the apprentices. | `TMM-D6` end node | Yes | → Completed |

### TMM.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TMM_BUNDLE_SEEN` | `TMM-B2` or `TMM-I2` | LR-M1 (request) |
| `TMM_HOIST` / `TMM_PLANK` | M1 route taken | `TMM-D2` one line |
| `TMM_TAPPED` | Lintel tap at Hushfold | `TMM-D6` Kel line |
| `TMM_ACCOUNT` = opened / amended / kept | `TMM-D5` | `TMM-D6`; Stonewake barks; TF-M5 (request) |

### TMM.11 Choices and consequences — the margin

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **A. Lay it before the Assembly** — *"Say it from the stone. Tomorrow."* (`opened`) | Hadrik takes the slate and says he will read it himself at the next sitting. Next day (off screen; Ivra reports in `TMM-D6`) he reads the three lines from the speaking stone. The Assembly lets the roofs stand as Assembly work and puts the terrace's missing courses on next year's account. | Hadrik's standing: from now on a clan voice must countersign Quarter accounts with him; his signature alone is no longer enough. Sefa pays her season's margin out of her own purse. **Hushfold hears it was argued over**: Runa learns the roofs came from the Assembly purse and that some voices said Hushfold wasn't worth it. | Barks: Brynjar's voice in the market about "stores first" (with `TH_BRYNJAR` = disowned he adds "and roofs. Fine. Roofs."). TF-M5 (request): HADRIK: *"I've been accounted for in this hall once this winter. It didn't kill me."* |
| **B. Write it true, say nothing** — *"Write the real lines in the book. Let anyone who reads it read it."* (`amended`) | Sefa writes the true lines into the account in ink beneath the false ones: *"Hushfold shelter roofs, four, and two lintels, by the Speaker's leave."* Hadrik signs under it in full, not initials. The book goes back on the shelf. No one is told. | The record is honest only if someone reads it. The terrace parapet's twenty-eight courses are now written down as missing and unfunded. Kel is frightened of the day someone does read it. Ivra and Kel's names go into the true line as cutters. | Barks: Ivra checks the shelf "to see if anyone's read it". TF-M5 (request): HADRIK, passing the player: *"Written. Not read yet. That's most of what we do."* |
| **C. Keep the margin** — *"Leave it. Roofs matter more than lines."* (`kept`) | The slate is wiped. The account stays as written. Hadrik thanks the player once and does not mention it again. | The apprentices now know the Quarter's book lies, and Ivra must cut next year's "terrace" stone knowing where it goes. Hadrik owes a stranger a secret. Sefa's margin continues: her last line hints at another roof next leaf-fall. The terrace parapet stays under-built. | Barks: Ivra stops chalking the yard wall. TF-M5 (request): HADRIK, quietly, to the player only: *"Still mine to carry. Thank you for the weight."* |

No option is wrong. None keeps Hadrik's standing whole, the roofs uncontested and the book honest all at once. The roofs stay on in every outcome; nobody takes slate off a clanless house.

### TMM.12 Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Stonewright Quarter yard bench | Access | The Quarter's measuring yard becomes a place the player may work stone and take Quarter commissions later (Thornfell master commissions, bible §9.1 `TH_STANDING`; this only opens the yard's bench). |
| Small payment | Currency | From Sefa ("for the measuring, not the trouble"). Economy tuning. |
| Standing in dialogue | Story | Ivra and Kel's barks; Runa's line; Hadrik's TF-M5 line (request). No reputation system. |
| Knowledge | Story | The war shelf and its sealed bundle (`TMM_BUNDLE_SEEN`). |
| Skill XP | — | None (no skill actions). No lump quest XP. |

### TMM.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Walking away | Quest stays Active at the persisted step. Ivra's resume hook (`TMM-D1.00`) names the next place. |
| Death | Not expected (no combat; the plank cannot be fallen from). If it happens elsewhere, respawn at Stonewake's terrace stair with step and flags intact. |
| Logout mid-cistern | The cord-run channel keeps completed progress; the lantern relights on re-entry. |
| Logout carrying the account | The account returns to the shelf; `S01` stays complete (pages stay read). |
| Night-only hall | Keep-watch at the hall doors advances to night in one step; never world time. |
| Co-op | Independent instances. Each player measures their own slate (per-player slate prop; fallback: shared slate, every partner on the step credited). The hall moment plays per player; a partner in the hall hears only an ordinary room unless on the same step (fallback: shared presentation). The choice is per player; the yard wall and the book line are per-player props (fallback: barks only). |

### TMM.14 Integration needs

| Need | Owner | Minimum viable form | Fallback |
|---|---|---|---|
| Inspect points with chalked results on a slate prop | Systems Engineer; Schema & Content Engineer | Inspect events set quest-local counters; slate prop swaps texture per counter | Ivra speaks the result; no slate prop |
| Cord-run channel along a path | Systems Engineer | Channel interaction that stays active while the player walks inside a corridor volume and completes on entering an end volume | Two inspect points (start pin, end of new lining) |
| Crank hoist cage | Level design | Reuse TF-M2 Whinstone hoist cage | Stair down to the plank's niche |
| Gust hazard with whistle tell | Gameplay Designer; Audio | Bible §9.5 shared wind-window convention | Fixed-interval push with the glyph only |
| Hall voice return | Audio | Per-player delayed send on the player's voiced lines inside the hall volume, routed from an emitter at the far gallery; Hadrik's first line routed close to the listener | Subtitles with direction markers; ordinary reverb |
| Night window | Systems Engineer | Keep-watch interaction at the hall doors (Lowmark MQ4 convention) | Hall moment plays at any hour |
| Per-player props (slate, yard wall, book line) | Systems Engineer | Prop state keyed to quest flags | Barks carry the outcome |

### TMM.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | This autumn the Quarter overstated three Assembly repairs and sent the stone to four Hushfold roofs and two lintels. Sefa kept the margin; Hadrik countersigned knowingly to keep the question off the Assembly floor before snow. |
| Public belief | The Assembly's repairs were done as written. Hushfold believes the Quarter's masons were kind. |
| Player-observable evidence | The measured stone (three works); the dray book; banker marks on Hushfold lintels; Runa's tally page (testimony and record); the pencilled roof signs; Hadrik's slip and his own word. |
| Wrong reading | Sefa or Hadrik pocketed Assembly money. Every coin went to stone, and the stone is on Hushfold's roofs. |
| Withheld | The sealed bundle's contents (R13; LR-M1). Whether Hadrik has done this before: he says "not this way". |

### TMM.16 Open decisions

| # | Decision | Recommendation |
|---|---|---|
| TMM-OD1 | Hadrik's anchor limit says he "does not decide; he keeps the Assembly together while it decides". Countersigning a diversion is a decision. | Keep it: it is the buffer's decision (to keep a question off the floor), not a ruling on the question. He offers no defence and hands the outcome to the player. **[PROPOSAL — DIRECTOR]** |
| TMM-OD2 | Should TF-M5 read `TMM_ACCOUNT`? | One Hadrik line only (TMM.11). Never a posture weight. |
| TMM-OD3 | Who wrote the war-shelf bundle. | Unknown in Thornfell. LR-M1 owns it. Kaldren is not its author (bible §8.2; Arcs LR-M1). |

### TMM.17 Internal review log

| Check / finding | Result |
|---|---|
| Draft had Hadrik ordering the diversion himself. | Changed: Sefa proposed and kept the margin; Hadrik's slip agrees and signs. Keeps him a buffer. |
| Draft let the player cut the bundle's cord. | Removed. No open interaction exists; inspect says it is not the player's to break; `TMM_BUNDLE_SEEN` is set by a guaranteed bark. |
| Draft measured by tapping stone. | Changed to course counts, tread wear and a cord, so TMM does not repeat *Seam Rights*' tap-and-count. Sound enters through the hall and the optional lintel tap. |
| Option A first cost Hushfold its roofs. | Cut: nobody strips a roof. The cost is Hadrik's countersign and Hushfold hearing the argument. |
| Evidence rule | The hall moment proves nothing; Hadrik already knew. Facts are stone, records and testimony. |
| Ledger limits | Hadrik's scars not mentioned; no war service; no record custody beyond his ordinary signature on accounts. Kaldren does not appear and is not the bundle's author. |

### TMM.18 Dialogue

#### Cast notes

**Ivra [NEW]** — Stonewright apprentice, about seventeen, human. *Knows:* stone, and that forty courses is a lie. *Doesn't know:* where the stone went, or that she cut it. *Voice:* quick and indignant; measures with her thumb; uses stone units for everything ("That's a cart of anger"). *Change:* she finds her own mark on a clanless lintel and goes quiet.

**Kel [NEW]** — Stonewright apprentice, dwarf, a little older and much slower. *Knows:* treads, and that the master has reasons. *Doesn't know:* the reasons. *Voice:* careful; taps every lintel before going through (TME02); says "probably" about things he is sure of. *Fear:* being the one who broke the Quarter.

**Sefa Dunholt [NEW]** — the Quarter's master of works, dwarf. *Knows:* everything about the margin. *Doesn't know:* who sealed the war bundle (before her time). *Voice:* gruff, plain, "stone first, paper after". Admits what she did without apology and without a speech.

**Hadrik Stonewake [CANON ANCHOR]** — Assembly Speaker. *Knows:* he signed; why; that the hall carries some voices. *Doesn't know:* why it does, and does not ask [CANON]. *Voice:* calm, patient, few words; lets a silence finish an argument. *Guard:* no scars mentioned, no war, no date. He hands the decision to the player and does not argue for any option.

**Runa Weatherall [NEW, bible §5.2]** — Hushfold shelter host. *Knows:* the masons came and asked nothing. *Doesn't know:* where the stone came from. *Voice:* warm, tired, proud; says "we" for the whole shelter line. Uses the player's name if `TME01_TALLIED`.

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `TMM-B1` | IVRA | Measuring yard, quest available | *"Forty courses. Forty. I've been up there. I could count them on my boots."* |
| `TMM-B2` | KEL | On account pickup (S01) | *"Not that end. That's the war shelf. Nobody touches the war shelf."* (beat) *"Master dusts round it."* {set TMM_BUNDLE_SEEN} |
| `TMM-B3` | HALL ATTENDANT | Kneeling on the stair (S02b) | *"It's a stair, walker. You go up it."* |
| `TMM-B4` | IVRA | On the parapet while the player is on the plank (S02a) | *"Fresh drag marks? Count them. I'll count with you. Out loud, so I can't cheat."* / after a gust: *"Hard wind. Sit in the niche till it's done shouting."* |
| `TMM-B5` | HUSHFOLD CHILD | Near the charcoal hooks on the wall (S05) | *"That's the hook. It's on our door. It means good luck."* |
| `TMM-B6` | IVRA | Post-quest, `opened` | *"Clan voice signs with the Speaker now. Two names on every page. Twice the ink."* |
| `TMM-B7` | IVRA | Post-quest, `amended` | *"Nobody's read it yet. I check."* |
| `TMM-B8` | IVRA | Post-quest, `kept` | (not chalking the wall) *"Wall's for true things. I'll start again in spring."* |

#### Nodes

```
TMM-D1.00 [quest Active, returning] IVRA: "You. Good. Where were we." (pins the current step's objective)  → end
TMM-D1.01 IVRA: (to the chalk wall) "Forty. It says forty."
TMM-D1.02 KEL: "It says forty because the account says forty. That's how chalk works."
TMM-D1.03 IVRA: (to the player) "We chalk what the Assembly paid for. Terrace parapet, forty new courses. I went and looked. It isn't."
TMM-D1.04 KEL: "Master'll have reasons."
  > "How many is it?"                                       → TMM-D1.10
  > "Why not ask your master?"                              → TMM-D1.20
  > "Show me the account."                                  → TMM-D1.30
TMM-D1.10 IVRA: "Don't know. Can't see the outside face from the terrace. Fresh mortar makes old stone look young."  → TMM-D1 options
TMM-D1.20 KEL: "She's at the Hall."
TMM-D1.21 IVRA: "And if I ask her, I'm the apprentice who called the master a liar. If you ask, you're a stranger who can't count."   → TMM-D1 options
TMM-D1.30 IVRA: "It's on the log shelf in her room. We can't take books off the shelf."
TMM-D1.31 IVRA: "Nobody said anything about walkers."
TMM-D1.32 KEL: (unhappy) "Probably nobody thought of walkers."
TMM-D1.33 IVRA: "Rod and cord are in the yard. You'll want both."   {event: S00_hook}
```

```
TMM-D2.01 IVRA: (reads the slate twice) "Terrace short twenty-eight courses. Stair, eight turned for recut. Cistern, thirty-eight ells of lime that never went on a wall."
TMM-D2.02 [TMM_HOIST] IVRA: "And you took the cage. Sensible. Master says sensible is a kind of brave."
TMM-D2.02 [TMM_PLANK] IVRA: "And you stepped off the parapet onto a plank. Master says that's a kind of stupid."
TMM-D2.03 IVRA: "That's four roofs of slate. Maybe two lintels." (beat) "Somebody built four roofs."
TMM-D2.04 KEL: "Roofs where?"
TMM-D2.05 IVRA: "Dray book'll say. Drays don't lie. They can't write."   {event: S03_slate}
```

```
TMM-D3.01 [TME01_TALLIED or TSM_PLAYER_TALLIED] RUNA: "{PLAYER}. You're on my tally, so you're on my bench. Sit."
TMM-D3.01 [else] RUNA: "Walker. If you're lost, you're in the right place. Most of us were."
TMM-D3.02 RUNA: "You're looking at the roofs. Everyone does. We've never had four sound at once."
  > "Who built them?"                                       → TMM-D3.10
  > "Did anyone pay?"                                       → TMM-D3.20
TMM-D3.10 RUNA: "Masons from the Quarter. Leaf-fall. Four days. A dwarf woman who swore at our rafters and a lot of quiet lads."
TMM-D3.11 RUNA: "They wouldn't take bread. Took soup. You can't refuse soup, it's rude."   → TMM-D3 options
TMM-D3.20 RUNA: "Nothing asked. I wrote it down. We write everything down." (takes a book from the end of the shelf, opens it)
TMM-D3.21 RUNA: "There. So nobody can say we didn't thank them."   {inspect TMM-I7 available}
TMM-D3.22 RUNA: "Why?" (looks at the player) "Did somebody pay?"
  > "I don't know yet."                                     → TMM-D3.30
  > "Somebody did. I'm finding out who."                    → TMM-D3.30
TMM-D3.30 RUNA: "Then find out kindly. We'd like to keep the roofs either way."   → end
```

```
TMM-D4.01 SEFA: (doesn't look up from a plan) "You've been up my terrace on a plank. Everyone saw."
TMM-D4.02 SEFA: "And down my cistern with my cord. And up Hushfold with my apprentice." (looks up) "Sit or don't."
  > "Twenty-eight courses. Eight treads. Thirty-eight ells."  → TMM-D4.10
  > "Hushfold's roofs."                                      → TMM-D4.10
TMM-D4.10 SEFA: "Yes." (beat) "That's the whole answer. You want the long one?"
TMM-D4.11 SEFA: (opens the account; taps a pencil mark in the margin, a little roof) "Every line that's fat has one of those. I'm not clever. I'm tidy."
TMM-D4.12 SEFA: "Assembly money for Assembly works. Hushfold isn't an Assembly work. Hushfold isn't anything, on paper. It's people under bad slate."
TMM-D4.13 SEFA: "The terrace can wait a year. Old stone, good mortar. Roofs couldn't wait a winter."
TMM-D4.20 SEFA: (draws a folded slip out of the back board, hands it over) "He signs every account. He signed this one knowing."   {inspect TMM-I8 available; event: S06_margin on inspect}
  > "Why not ask the Assembly?"                              → TMM-D4.30
  > [TMM_BUNDLE_SEEN] "The bundle on the war shelf."         → TMM-D4.40
  > "Where is he?"                                           → TMM-D4.50
TMM-D4.30 SEFA: "Ask him. I'd have asked. He said they'd still be arguing at thaw." [TH_STORES any] "With the stores and all."   → TMM-D4 options
TMM-D4.40 SEFA: "War shelf. Sealed before I had the yard. Stays sealed till someone with a right to it asks."
TMM-D4.41 SEFA: "Whose hand? The tag doesn't say. Not Kaldren's, before you ask. Everyone asks. He laughs and says he's never worked water."   → TMM-D4 options
TMM-D4.50 SEFA: "In the Hall. He always is, after." (back to her plan) "Go at night. He likes it empty."   → end
```

```
TMM-D5.01 PLAYER: (reading the slate on the speaking stone) "Terrace: account forty, stone twelve. Stair: account twelve recut, stone four, eight turned. Cistern: account sixty ells, stone twenty-..."
          HADRIK: (from the far gallery, arriving close) "Twenty-two ells."
TMM-D5.02 HADRIK: (coming down the gallery stair) "It does that. I don't ask why."
TMM-D5.03 HADRIK: "You've been to Hushfold."
  > "You signed it."                                         → TMM-D5.10
  > "Why hide roofs?"                                        → TMM-D5.20
  > [TMM_BUNDLE_SEEN] "Sefa says you knew."                  → TMM-D5.10
TMM-D5.10 HADRIK: "I signed it." (sits on the lowest bench) "Every page. I read them, too. People think I don't."   → TMM-D5.20
TMM-D5.20 HADRIK: "In leaf-fall this hall couldn't agree on the weather." [TH_STORES any] "Then the stores."
TMM-D5.21 HADRIK: "Put 'Assembly stone for clanless roofs' on that floor and it goes on till thaw. Somebody says Hushfold has no voice here. Somebody says they're right."
TMM-D5.22 HADRIK: "The roofs don't get done. Then it snows."
TMM-D5.23 HADRIK: "I don't say it was right. It was done."
TMM-D5.24 HADRIK: (looks at the stone, not the player) "I choose where people stand. That's the job." (beat) "You found this. So you stand somewhere. Where?"
  > "Say it from the stone. Tomorrow."                       → TMM-D5.30
  > "Write the real lines in the book. Let anyone who reads it read it."  → TMM-D5.40
  > "Leave it. Roofs matter more than lines."                → TMM-D5.50
TMM-D5.30 HADRIK: "Then I'll read it myself. Here. Where some voices carry." (beat) "Mine never has. We'll see."
TMM-D5.31 HADRIK: (takes the slate) "They'll want another name on the accounts after. Fair."   {set TMM_ACCOUNT = opened}  {event: S08_decide}
TMM-D5.40 HADRIK: "In ink, under the lie. With my name, all of it, not the letter." (stands) "Sefa will grumble. She grumbles in ink too."
TMM-D5.41 HADRIK: "Then it's written. Whether it's read is the next person's business."   {set TMM_ACCOUNT = amended}  {event: S08_decide}
TMM-D5.50 HADRIK: (a long silence; the lamp hisses) "Then you've got a Speaker's secret, walker. Mind it. They get heavy."
TMM-D5.51 HADRIK: (wipes the slate with his sleeve, carefully) "Thank you." (he doesn't say it again)   {set TMM_ACCOUNT = kept}  {event: S08_decide}
```

```
TMM-D6.01 [opened] IVRA: "He read it. From the stone. Brynjar shouted. Elira shouted at Brynjar. Torvek said 'Roofs held.' That was it."
TMM-D6.02 [opened] KEL: "Clan voice signs the accounts with him now. Master's paying the margin from her own purse. She swore at the purse."
TMM-D6.03 [opened] IVRA: "Runa came down. She heard someone say Hushfold wasn't worth slate." (beat) "She said thank you anyway. To the hall. Loudly."
TMM-D6.01 [amended] IVRA: (holding the book) "Under the lie. In ink. 'Hushfold shelter roofs, four, and two lintels, by the Speaker's leave.' And his whole name."
TMM-D6.02 [amended] KEL: "And ours. As cutters." (beat) "What if somebody reads it?"
TMM-D6.03 [amended] IVRA: "Then they'll know who cut the roofs. Good."
TMM-D6.01 [kept] IVRA: (wiping the chalk wall) "Forty courses. Forty."
TMM-D6.02 [kept] KEL: "It says forty because the account says forty." (he doesn't sound sure any more)
TMM-D6.03 [kept] IVRA: "I'll cut next year's terrace stone. I'll know where it's going." (beat) "I'll put my hook on it."
TMM-D6.04 [TMM_TAPPED] KEL: "You tapped my lintel. At Hushfold. I saw." (pleased) "Rang true, didn't it."
TMM-D6.05 SEFA: (from the work-room door; pays) "For the measuring. Not the trouble. The trouble's free."   {event: S09_close → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `TMM-I1` | Rod groove (yard bench) | "One ell, cut into the bench. Worn shiny. Every rod in the Quarter is checked against it." |
| `TMM-I2` | **The sealed bundle** (war shelf) | "Work logs, by the thickness, bound in oilcloth and tied with cord. The knots are sealed with the Quarter's wax. A wooden tag: *'Lowmark work, war years.'* The seal has never been broken. It is not yours to break." / [Lowmark MQ4 Completed, optional variant] adds: "You have stood in Lowmark's wartime works. Somebody cut them." {set TMM_BUNDLE_SEEN} |
| `TMM-I3a` | Account, line 1 | *"Signal Terrace parapet, outer face: forty courses relaid in new stone."* Signed at the foot: *"Seen. H.S."* |
| `TMM-I3b` | Account, line 2 | *"Assembly Hall great stair: twelve treads recut."* |
| `TMM-I3c` | Account, line 3 | *"Ridge-market cistern: lining renewed, sixty ells."* |
| `TMM-I4a` | Outer face, fresh course | "Claw-chisel drag marks, sharp. Pale stone. New." |
| `TMM-I4b` | Outer face, old course | "Weathering pits, lichen in the pits. Fresh mortar in the joints makes it look younger from inside." |
| `TMM-I4c` | Riser joint, turned tread | "The top is clean. Under the lip, where it meets the riser, an old worn hollow faces down. This tread was turned over, not recut." |
| `TMM-I4d` | Riser joint, recut tread | "Crisp arris both faces. Recut." |
| `TMM-I4e` | Cistern cord | "Twenty-two knots paid out to where the white lime ends." |
| `TMM-I4f` | Cistern tide-line (optional) | "Grey lining with a tide-line. A drip, and the drip has worn a dimple." |
| `TMM-I5` | Dray book | *"Leaf-fall. Ridgewall. Slate, lime. One load."* Four entries, four days running. Each marked *"S.D."* |
| `TMM-I6a` | Hushfold lintel (Ivra's) | "On the hidden face, a banker mark: a small hook." |
| `TMM-I6b` | Hushfold lintel (Kel's) | "A banker mark: a little square, cut very carefully." |
| `TMM-I7` | Hushfold tally page (this autumn) | *"Quarter masons. Four days. Roofs made sound, four houses; lintels, two. Nothing asked. Soup given. Thanked."* |
| `TMM-I8` | Hadrik's slip | *"Roofs before snow. Charge it to the terrace. I'll sign. H."* The hand matches the "H.S." at the foot of every account page. |

---

## TAS — Ash in the Snow

### TAS.1 The quest in one paragraph

Four masons from Emberholt came up Windscar on the last good day before TF-M1's storm, with a guild work order and a safety notice saying three iron cramps in Passwatch's inner gate arch are failing and must be replaced before hard frost. Vessa Galt let them in under the storm and then held them: strangers whose papers are in question wait inside the gate for the Assembly clerk's word, and the word will not come before snow. They have been in the barracks' cold shed for days. Their new cramps were refused at the gate as "Emberholt iron" and sit in a mule cache below the Blind Corners. A Blood-Oath tower crew, Brynjar's people, say the papers are forged: the guild seal is a new style nobody here has seen, and the notice calls Passwatch by a name no Marcher uses. Their distrust is not stupid. In the war Emberholt pushed hard for the mountain routes, and a crew of Emberholt hands with business at the gate is exactly what a careful warden refuses. Tessaly Varn, the crew's leader, is courteous, exact and tired of being suspected. The player does not settle whether the papers are genuine. They settle whether the arch is failing: they climb to the cramps and strike them, and Dorn, who trusts his ears over anyone's paper, listens to the ring. Two of the three named cramps are sick, the third is sound, and a fourth the notice never mentioned is the worst of all. Then the player brings the iron up through bandits, talks a tower crew out of blowing Gather against their own guests, and keeps the crew safe through one cold night while new iron goes into the arch between gusts. At dawn Vessa asks what to write in the gate book.

**Remember:** forge ash drifting over a snow-dusted yard while a tower crew watches every spark, and the whole arch giving one low note as its weight comes off the bad iron. **Want next:** to know whether the guild seal was real, and who in Emberholt keeps a list of Thornfell's gates.

### TAS.2 Selection record

| Candidate | Verdict |
|---|---|
| **A. Prove the papers genuine or forged.** | Rejected. Nobody in Thornfell can authenticate an Emberholt guild seal, and the bible limits the quest to assessing the papers' immediate safety claim locally (Part 3 story 3). |
| **B. A brawl between the tower crew and the masons.** | Rejected. Thornfell's distrust is rational and Thornfell people are not enemies here; nobody fights the tower crew. |
| **C. Test the claim on the arch → bring the iron → de-escalate → protect and repair through the night → write the gate book** | **Selected.** The assessment is physical and local; combat is present but secondary (bandits at the cache, wolves on the road); the choice is about what Thornfell writes down, the bible's Thornfell theme. |

### TAS.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Thornfell distrusts Emberholt rationally; fears firecraft escalation; is wary, not preparing for total war | Dossier §XIV, §XXI.5; bible §5.3 rule 6 | [CANON] |
| Mutual respect between Emberforged and Thornfell's stoneworkers | Emberholt dossier §XVIII | [CANON] |
| Emberholt metals imported "begrudgingly" | Dossier §XIX | [CANON] |
| Brynjar's clan keeps the loudest horn towers; he believes Emberholt will betray Thornfell again | Thornfell anchors II | [CANON] |
| Ressa refuses certain calls (accountable warning) | Thornfell anchors IV; bible §5.1 | [CANON] |
| Braid 9: a Thornfell–Emberholt repair where "Thornfell owns the pass decision; Emberholt owns public worker credit" | Part 4 relationship web | Proposal |
| *Ash in the Snow* pitch; Tessaly Varn; Vessa Galt; Dorn Feldhorn | Part 3 story 3; bible §5.2, §7.2 | [NEW] adopted by the bible |
| The arch cramps, the papers' text, Geir Vellan, Bjarke, Ansa, the cache | This package | [NEW] |

### TAS.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.ash_in_the_snow` |
| Type | Settlement story, Passwatch (bible §7.2) |
| Unlock | TF-M1 Completed. Offered by Vessa Galt at the Passwatch gate (`TAS-D1`), or by passing the cold shed (bark `TAS-B1`, Tessaly). |
| Resume hook | Vessa at the gate: `TAS-D1.00` pins the current step. |
| Target length | 35–45 minutes |
| Combat share | ~20% (cache bandits required; wolves on the return optional to avoid) |
| Skills | Smithing (setting cramps; crew alternative); Melee or Ranged |
| Choice | What the gate book says (3 options) |
| Outputs | `TAS_PROOF` = proof / watch / ruled; `TAS_ACCOUNT` = named / held / unwritten |
| **Anchor** | Passwatch and the Ridge Wardens (Vessa, Ressa, Dorn); a Blood-Oath tower crew; Emberholt's Emberforged stoneworkers as people |
| **World-truth row** | H23 (recovery: repair and disputed credit); present pressure H25 (closures). Braid 9 (Thornfell–Emberholt joint repair). No history row is asserted: the arch's earlier joint repair is shown as two kinds of iron, not dated. |
| **Revelation role** | Self-contained. Plants no revelation. Optional braid-9 callback flag for Emberholt content. **No Remnant presence, phrase or implication** (FT-04 bounded reach). |
| **Recurring evidence** | Vessa's gate book (TF-M1 slate, TF-M5); Tessaly's papers stay with Tessaly or the Assembly (no Thornfell custodian claims them as proof of anything). |
| **State compliance** | Inactive / Active / Completed; `TAS_ACCOUNT` outcome flag; no fail; the crew cannot be harmed; the night cannot be lost (channel segments persist). |

### TAS.5 The places

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **P1. Passwatch gate and inner arch** (TP02) | Hook; the cramps; the repair | The inner gate arch: big dressed voussoirs and a keystone course tied with iron cramps leaded into the stone. **Two kinds of iron** show at the joints: flat Thornfell ridge-iron cramps and a few round-headed ones of a different make. Rust bloom runs down from two joints like tea stains. One voussoir has lifted a fingernail's width. | **Agility trigger:** climb the horn post's outside ladder and step across onto the arch's top course. **Walkable fallback:** the barracks' inside stair to the wall walk and along it. |
| **P2. The cold shed** | Tessaly's crew | A lean-to against the barracks wall: four bedrolls, a charcoal brazier they are only allowed to light by day, tools wrapped in oiled cloth. A guild case on a crate. A row of boots drying, toes to the brazier. One bedroll is short: the youngest sleeps curled. | — |
| **P3. Horn post** | Dorn; the tower crew; Ressa | Dorn's post above the gate. The Blood-Oath tower crew's horn hangs by the door, a big ridge horn with clan bindings. | — |
| **P4. Gate yard** | The night; the forge | Snow-dusted cobbles (`TH_SEASON` = snow) or slush and sleet (autumn; quest-local light snow begins at nightfall in either case). Tessaly's portable charcoal forge is set in the yard's lee corner for the repair. Scaffold poles against the arch. | — |
| **P5. Mule cache** (below the Blind Corners, TP26 edge) | Iron recovery | A rock overhang off the road. Two hobbled mules, pack-frames, a bundle of new cramps in sacking, lead pigs. Pass bandits have cut one frame open. | Road down from the gate; one goat-track shortcut (agility; walkable fallback is the road). |

**MAP VERIFICATION REQUIRED:** the cache sits below the Blind Corners on the Passwatch side; the gate's inner arch has a reachable top course from the horn post and from the wall walk. No compass direction toward Emberholt is asserted, and the papers do not say which way the crew came (TD-6).

### TAS.6 Player-facing sequence

**Beat 0 — Four in the cold shed (`S00_hook`).** *Objective: Find out whether Passwatch's gate is failing.* Vessa (`TAS-D1`): she is holding four Emberholt masons on the rule, a tower crew wants them in the snow, and their papers say her gate is falling down. "Nobody here reads papers that well. Everybody here reads a wall." **Verbs:** listen.

**Beat 1 — The papers (`S01_papers`).** *Objective: Talk to Tessaly Varn.* In the cold shed (`TAS-D2`). Tessaly hands over the papers to read (two required inspects: the work order and the safety notice, full text in TAS.18). She does not argue for them. "Read them. Then go and look at the arch. The arch doesn't care who sent me." Optional: give food to the crew (any cooked food: `TAS_FED`) or ask the young labourer, Ansa, about the road (`TAS-D2.30`). The tower crew's bark from the yard (`TAS-B2`). **Verbs:** read, ask.

**Beat 2 — Ask the iron (`S02_arch`).** *Objective: Test the cramps the notice names.* Climb to the arch's top course (agility from the horn post or the wall-walk stair). Dorn comes along because he will not have strangers striking iron on his gate unheard (`TAS-D3`). Four marked joints: the notice names three; the fourth is the lifted voussoir's joint, which the player finds by its rust bloom. At each joint the player **strikes** (interaction) and listens:

| Joint | Notice says | Ring (audio + glyph) | Visual | Dorn |
|---|---|---|---|---|
| J1 | Failing | A buzzing doubled ring that dies fast (glyph: a broken bar) | Rust bloom; hairline crack beside the lead | "Sick." |
| J2 | Failing | Doubled, short | Lead pushed proud of the joint | "Sick. Not as bad." |
| J3 | Failing | One clean ring that hangs (glyph: a long bar) | None | "That one's fine. Your paper's wrong." |
| J4 | Not named | Hardly rings at all: a dull clack | The lifted voussoir; rust jacking | (long pause) "That's the worst of them. Paper didn't know." |

All four strikes are required. The result is written in Dorn's words (the player's journal): *two named sick, one named sound, one unnamed worse.* The safety claim is **mostly right** and **not complete**: the papers neither prove themselves nor read like a con. **Verbs:** climb, strike, listen.

**Beat 3 — The iron (`S03_cramps`).** *Objective: Bring the new cramps up from the mule cache.* Tessaly gives the cache's place. At P5, pass bandits are picking over the pack-frames (**TAS-E1**); they fight to 0 HP. (Their talk after the fight is cut, CDR-1 pattern T-4; `TAS-D4` removed.) The player leads the two mules back (escort-carry: the mules follow; the cramp bundle rides on a frame). On the road, optional **TAS-E2** ridge wolves come at the mules; the mules shy and stop, cannot be hurt, and walk on when the wolves are defeated. **Verbs:** fight, lead.

**Beat 4 — Gather against guests (`S04_tower`).** *Objective: Get the iron through the gate.* At the gate the Blood-Oath tower crew block the mules (`TAS-D5`). Their captain, **Geir Vellan**, means to blow **Gather** from the tower horn to bring the barracks out "to see what's coming in". Before the player speaks, **Ressa Highcrag** is on the horn post stair and refuses the call (`TAS-D5.05`: "Gather's for the mountain."). Then the player picks a way through (any one works; `TAS_PROOF`):
- **proof** — take Geir up to J4 and let him strike it himself (short walk, one strike). He is a Marcher; he believes iron.
- **watch** — propose the tower crew guard the work: a tower-hand at each scaffold pole all night. It gives Geir a job he can be proud of.
- **ruled** — ask Ressa to rule. She does: the work goes ahead under Warden watch. Geir obeys and does not forgive it.
**Verbs:** de-escalate.

**Beat 5 — The night (`S05_repair`).** *Objective: Help the crew set the new cramps.* Nightfall (keep-watch at the shed if needed). The repair is a **three-segment channelled job** on the scaffold, one segment per sick joint the crew can reach tonight (J4, J1, J2; J3 is left alone, sound):

| Segment | Joint | Player does (Smithing) | Crew alternative |
|---|---|---|---|
| 1 | J4 | **Jack and cut**: set the screw-jacks under the voussoir (Tessaly holds the level), then cut out the old cramp at the forge-heated lead (channel 6 s). | Bjarke and Ansa do it: one extra watch step, and one more Geir bark from the cold. |
| 2 | J1 | **Forge and set**: heat the new cramp at Tessaly's charcoal forge (channel 4 s), carry it up (light carry), seat it (channel 3 s). | As above. |
| 3 | J2 | **Run the lead**: melt the lead pig at the forge and pour the joint (channel 5 s). | As above. |

Completed segments persist. **Wind windows** on the scaffold: the fluted faces above Passwatch whistle up a fifth ~1.5 s before a gust (bible §9.5); a gust interrupts a running channel (progress kept) unless the player waits in the lee of the arch's pier. **Protect** interruptions, one between each segment, solved without combat:
- **After segment 1:** a tower-hand kicks snow over the forge "by accident". *Relight the forge* (interaction, 3 s; Tessaly's bellows). With `TAS_PROOF` = watch, the tower-hand at the pole stops him first and the forge is not touched.
- **After segment 2:** two tower-hands come to the cold shed to "check papers" while the crew are on the scaffold, and start throwing bedrolls into the yard. *Turn them back* (`TAS-D6`; any option works). With `TAS_FED`, Ansa had already moved the bedrolls inside.
**The strange moment** (TAS.8) plays as the jacks take the voussoir's weight in segment 1. **Verbs:** smith, carry, wait out the wind, protect.

**Beat 6 — Dawn (`S06_dawn`).** *Objective: Strike the new iron.* At first light the player strikes J4, J1 and J2 again: three clean rings that hang. Dorn: "Better." Geir, if `TAS_PROOF` = proof, strikes one himself. A Passwatch child is catching forge ash on her tongue in the yard, thinking it is snow (bark `TAS-B5`). **Verbs:** strike, listen.

**Beat 7 — The gate book (`S07_book`).** *Objective: Tell Vessa what to write.* `TAS-D7`. Vessa writes the arch in her gate book either way: *"Inner arch: four cramps tested. Three made good."* She asks the player what else she writes (TAS.11). **Verbs:** decide.

**Beat 8 — The crew (`S08_close`).** *Objective: See the crew off.* `TAS-D8` with Tessaly at the gate or the shed, by outcome. Quest Completed.

### TAS.7 Encounters

Tuned for Competent identity (TD-12). Every enemy fights to 0 HP (CDR-1); melee or ranged.

| Id | Enemies (bible §10) | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TAS-E1** | 2 × pass bandit cutter, 1 × slinger | Mule cache overhang (P5) | Cutters close in pairs; slinger holds the overhang lip | **Cutter double cut:** drops the shoulder and draws the blade back low (~0.9 s), two quick cuts. **Slinger:** whirls overhead with an audible rising whirr (~1.2 s, glyph: a spiral), one stone in a straight line; side-step breaks it. | Required. First fight of the quest; the "protect" begins by recovering what was taken | 45–70 s; 60–80% HP left |
| **TAS-E2** | 1 × ridge wolf howler, 2 × runner | Road below the gate, once, on the return | Howler stands off and calls; runners go for the **mules** first, then the player | **Howl:** howler lifts its head (~1.5 s, readable howl); 4 s later the runners commit. **Runner lunge:** crouch and tail-flat (~0.8 s). | Optional (the player may lead the mules past at a walk while the howler is still howling; runners commit only if the player stops). Protect read: the mules shy and halt, never take damage. | 40–60 s |
| **TAS-H1** | Scaffold gust | Arch scaffold (P4) | Hazard | Fifth-rise whistle ~1.5 s before; snow lifts off the scaffold boards in the last 0.5 s | Wind-window convention inside a skilling job | — |

**Rules.** Nobody fights the tower crew; there is no hostile flag on Thornfell people anywhere in this quest. The masons cannot be targeted or harmed. Combat never reveals evidence. **Death:** respawn at the Passwatch barracks door; mules wait at the last point reached; segments and flags kept.

### TAS.8 The strange moment: the arch's note (presentation spec)

| Time | Element | Spec |
|---|---|---|
| 0 s | **The jacks bite** | Segment 1's channel begins; the jack screws creak. Tessaly: "Easy. Easy." |
| 2–4 s | **The weight shifts** | The lifted voussoir settles a hair onto the jacks. One **low note** comes out of the whole arch, felt in the scaffold (controller rumble where supported; visible shiver in the scaffold rope), held about 2 s. Not music. |
| 3–5 s | **The sheet** | All the snow on the arch's top course slides off at once in one sheet and falls past the scaffold into the yard with a soft thump. |
| 4–6 s | **The stables** | In the ridge stables across the yard every horse lifts its head and turns toward the gate. Then they go back to their hay. |
| After | **Lines** | TESSALY: *"Good stone. It tells you when it's comfortable."* DORN says nothing, and does not strike anything for a while. GEIR (if present): *"...Wind."* |
| UI | | Channel bar stays visible. Subtitle: "(the arch hums)". |

**Cannot prove:** anything about the papers, Emberholt or the arch's makers. Stone under load makes noise. Nobody calls it anything else.

### TAS.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Find out whether Passwatch's gate is failing. | `TAS-D1` end node, or `TAS-B1` then `TAS-D2` start | Yes |
| `S01_papers` | Talk to Tessaly Varn. | `TAS-D2` reaches `TAS-D2.20` + 2 document inspects | Yes |
| `S02_arch` | Test the cramps the notice names. | 4 strike interactions (J1–J4) | Yes |
| `S03_cramps` | Bring the new cramps up from the mule cache. | TAS-E1 defeated + escort-arrival of both mules at the gate volume | Yes |
| `S04_tower` | Get the iron through the gate. | `TAS-D5` resolved (sets `TAS_PROOF`; the proof route also needs the J4 strike by Geir) | Yes |
| `S05_repair` | Help the crew set the new cramps. | 3 channel segments complete (player or crew) + 2 protect interruptions resolved | Yes |
| `S06_dawn` | Strike the new iron. | Watch to dawn + 3 strike interactions | Yes |
| `S07_book` | Tell Vessa what to write. | `TAS-D7` choice resolved | Yes |
| `S08_close` | See the crew off. | `TAS-D8` end node | Yes (→ Completed) |

### TAS.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TAS_FED` | Food given at the shed | Protect interruption 2; `TAS-D8` line |
| `TAS_PROOF` = proof / watch / ruled | `TAS-D5` | Night interruptions; `TAS-D6`, `TAS-D7` lines |
| `TAS_CREW_HELPED` | Any segment done by crew | `TAS-D8` line |
| `TAS_ACCOUNT` = named / held / unwritten | `TAS-D7` | `TAS-D8`; Passwatch barks; Emberholt content (request) |

### TAS.11 Choices and consequences — the gate book

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **A. Name them** — *"Write who mended it. Their names."* (`named`) | Vessa writes: *"Inner arch made good by T. Varn's crew, Emberholt. Papers: not known. Arch: true."* Papers returned. The crew go out through the gate at the next clear window. | The tower crew will not blow Answer for the crew leaving (an old courtesy, refused; Tessaly notices). Geir carries a complaint to Brynjar. Emberholt hands are now written into a Passwatch book. | Barks: Geir is cold to the player at the horn post. Braid 9 (request): an Emberholt guild scene can find its crew credited in a Thornfell book. BRYNJAR at Stonewake (optional bark): *"Emberholt hands on our gate. And it held. I'll be angry about that all winter."* |
| **B. Send the papers down** — *"Send the papers to the Assembly's clerk. Let someone who's seen a seal decide."* (`held`) | Vessa writes the arch and *"Papers sent to Stonewake for the clerk."* The papers go down with the next rider. The crew must wait for an answer. | **The crew winter at Passwatch.** Tessaly loses the season's wage and her crew's way home until thaw; Ansa cries once, in the shed, where nobody is meant to hear. The tower crew settle. | Barks: the crew are a winter fixture in the cold shed, now with the brazier allowed at night (Vessa's small mercy). Whether the clerk ever answers is left open. |
| **C. Let them go quietly** — *"Give them their papers. Write the arch. Not them."* (`unwritten`) | Vessa writes: *"Inner arch made good. Wardens."* Papers returned. The crew leave before the tower crew are up. | The crew's work goes unrecorded; the book says Wardens did it. Tessaly: "Then we were never here. We're used to it." Vessa dislikes the line and writes it anyway: it is the rule ("We write what we closed. Not who."). | Barks: the tower crew believe the Wardens did the arch. Braid 9 (request): Emberholt's guild record will hold a repair Thornfell never wrote. |

No option is wrong. None both credits the crew and keeps the tower crew's peace and gets the crew home before snow.

### TAS.12 Rewards and unlocks

| Reward | Type | Notes |
|---|---|---|
| Passwatch forge access | Access | Tessaly's forge corner stays a usable forge station in the gate yard (Smithing), as long as the crew are there (`held`) and afterwards as Passwatch's own (any outcome). |
| Small payment | Currency | From Vessa's gate box ("Warden rate. It's bad."). |
| Smithing XP | Actions only | Segments done by the player. No lump quest XP. |
| Story | — | Dorn's ringing test as a learned habit: later barks at other gates ("Strike it. Listen."). |

### TAS.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Walking away | Stays Active. Vessa's resume hook. Mules left on the road walk themselves back to the cache. |
| Death | Respawn at the barracks door; mules wait; defeated bandits do not respawn until the player leaves the area. |
| Logout during the night | Completed segments persist; the night restarts at the current segment with the keep-watch hour restored. |
| Player refuses all three de-escalation routes | Not possible to soft-lock: Ressa's ruling is always available. |
| No Smithing | Crew alternative on every segment. |
| Co-op | Independent instances. Shared bandits and wolves give credit to all on the step. Strikes, segments and interruptions are per player (fallback: shared, a partner credited only when their own active step uses it; CDR-6). The gate book and the shed's state are per-player props (fallback: barks only). |

### TAS.14 Integration needs

| Need | Owner | Minimum viable form | Fallback |
|---|---|---|---|
| Strike interaction with per-joint ring result and glyph | Audio; Systems Engineer | Inspect-like interaction that plays one of three ring sounds and shows its glyph | Text result in Dorn's line only |
| Escort of non-combat pack animals that halt when threatened | Gameplay Designer; Systems Engineer | Follow-NPC that pauses inside a threat radius and is untargetable | Mules removed; cramp bundle as a heavy carry-state object |
| Three-segment channel with crew alternative | Systems Engineer | Lowmark channel convention; crew option as a dialogue choice that advances the segment and one watch step | — |
| Interruptions between segments | Systems Engineer | Scripted events gated on segment completion | Interruptions removed; Geir barks carry the tension |
| Scaffold gust hazard | Gameplay Designer | Bible §9.5 convention | — |
| Arch note presentation | Audio; VFX | One-shot sub-bass with rumble; snow-sheet slide; stable horses' head-turn animation | Sound and subtitle only |
| Quest-local snowfall at Passwatch | VFX | Particle snowfall in the yard volume from nightfall | Frost decals |
| Per-player gate book and shed state | Systems Engineer | Props keyed to `TAS_ACCOUNT` | Barks |

### TAS.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | The arch was mended long ago with iron of two makes; four cramps are now failing to different degrees. An Emberholt guild kept a maintenance list that named three of them. Whether Tessaly's seal is current guild practice is not knowable in Thornfell. |
| Public belief | Tower crew: forged papers, a pretext to get Emberholt hands on the gate. Vessa: unknown, held on the rule. |
| Player-observable evidence | Four struck joints with Dorn's ear; two kinds of iron in the arch; the papers' text. |
| Wrong reading | "The papers are proven genuine because the arch was failing." The arch proves only the arch. Or: "The papers are a trick because one named cramp was sound." An old list can be wrong and honest. |
| Withheld | Who in Emberholt keeps the list, and who first mended the arch with Emberholt iron (braid 9; Emberholt content, if ever). |

### TAS.16 Open decisions

| # | Decision | Recommendation |
|---|---|---|
| TAS-OD1 | Braid 9 is a proposal. Should TAS depict the old joint repair at all? | Only as two kinds of iron in the joints, undated and unexplained. No date, no names. |
| TAS-OD2 | Does Brynjar appear in person? | No. His people only; one optional Stonewake bark in outcome A, within his canon belief. |
| TAS-OD3 | `held` keeps four NPCs at Passwatch all winter. | Recommend yes (barks and a shed prop; low cost). If cut, `held` sends the crew down to Stonewake to wait instead. |

### TAS.17 Internal review log

| Check / finding | Result |
|---|---|
| Draft let the player authenticate the seal by matching another seal. | Cut. Local assessment only; the papers are never proven either way. |
| Draft had a fight with drunk tower-hands. | Cut. Thornfell people are never enemies here; interruptions are solved by interaction and talk. |
| Tessaly used firecraft to heat iron. | Changed: a charcoal forge and bellows, like any smith. Nobody names or shows embercraft. |
| Remnant check | No Remnant presence, phrase or hint. The broadsheet phrase (R15) is not used. |
| Emberholt caricature check | The crew are tired professionals; Bjarke complains about the wind; Ansa is young and frightened; Tessaly is exact. Thornfell's suspicion is given its reason in Geir's and Vessa's lines. |
| Ledger limits | Ressa's refusal is an accountable-warning refusal (Gather is not for neighbours). Dorn's ear judges iron, never history. Brynjar gets no Emberholt relationship. |
| **Director rulings reconciliation (2026-11-03): CDR-1.** Bandits yielded and one talked after yielding (`TAS-D4`). | TAS-E1 fights to 0 HP; `S03_cramps` completes on defeat; `TAS-D4` cut as flavour (pattern T-4; ids kept as removed); "downed" persistence wording and "driven off" wolves removed. Steps, flags and choice unchanged. |

### TAS.18 Dialogue

#### Cast notes

**Tessaly Varn [NEW, bible §5.2]** — Emberforged stonemason leading the crew. *Knows:* stone, iron, her guild's list, and how a stranger is looked at. *Doesn't know:* who wrote the list's first entry; whether Thornfell will ever say thank you. *Voice:* courteous, exact, tired. Corrects small errors. Never argues for her papers.

**Bjarke [NEW]** — the crew's old mason. Complains about the wind as if it were a colleague. "Your wind has opinions."

**Ansa [NEW]** — the crew's youngest labourer. Frightened; polite; asks how far the next village is.

**Vessa Galt [NEW, bible §5.2]** — Ridge Warden sergeant. Short sentences; follows the rule and dislikes that it is the rule.

**Dorn Feldhorn [CANON ANCHOR]** — Veteran Hornbearer. Trusts his ears. *Guard:* his ear judges iron now, never a history or a message.

**Ressa Highcrag [CANON ANCHOR]** — High Ridge Warden. One refusal, one ruling.

**Geir Vellan [NEW]** — Blood-Oath tower captain at Passwatch. *Knows:* what Emberholt wanted in the war, by the clans' account; horns. *Doesn't know:* iron. *Voice:* blunt, not cruel. He is protecting a gate.

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `TAS-B1` | TESSALY | Passing the cold shed, quest available | *"If you're the one who'll look at the arch, we've been waiting. If you're not, we've been waiting anyway."* |
| `TAS-B2` | TOWER-HAND | Gate yard, S01–S04 | *"New seal. Never seen one like it. Nor's anyone."* / *"They call it the 'Windscar Inner Gate'. Who calls it that?"* |
| `TAS-B3` | BJARKE | Shed, any time | *"Your wind has opinions. Loud ones."* |
| `TAS-B4` | GEIR | Night, if crew alternative used | *"Cold work, watching. Colder work, being right."* |
| `TAS-B5` | PASSWATCH CHILD | Dawn yard | (tongue out) *"It's warm snow."* / MOTHER: *"That's ash. Spit."* |
| `TAS-B6` | GEIR | Post-quest, any | [TH_BRYNJAR = defended] *"Brynjar says readiness. I say the arch holds. Both, then."* / [else] *"Arch rings clean. I struck it myself."* (only if `TAS_PROOF` = proof) |
| `TAS-B7` | ANSA | Post-quest, `held` | *"Is it always this cold? It's always this cold."* |

#### Nodes

```
TAS-D1.00 [quest Active, returning] VESSA: "Still four in my shed. Go on."  (pins the current step)  → end
TAS-D1.01 VESSA: "Four from Emberholt. Came up the day before the storm. I let them in under it."
TAS-D1.02 VESSA: "Then I held them. Papers in question, you wait for the clerk. Clerk won't answer before snow."
TAS-D1.03 VESSA: "Tower crew say forged. Papers say my gate's falling down."
  > "Is it?"                                                → TAS-D1.10
  > "Why do the tower crew say forged?"                     → TAS-D1.20
TAS-D1.10 VESSA: "Nobody here reads papers that well. Everybody here reads a wall." (nods at the arch) "Go and read it."   → TAS-D1.30
TAS-D1.20 VESSA: "New seal. Wrong name for us." (beat) "And the last time Emberholt wanted our gates, they wanted them for armies. That's not a story. It's why there's a gate."   → TAS-D1 options
TAS-D1.30 VESSA: "Talk to the woman in charge. Varn. She's polite. It's wearing."   {event: S00_hook}
```

```
TAS-D2.01 TESSALY: (standing, as if for an inspection) "Tessaly Varn. Stonemason. Guild-sent." (beat) "You'll want the papers."
TAS-D2.02 TESSALY: "Read them. Then go and look at the arch. The arch doesn't care who sent me."
  > "Are they forged?"                                       → TAS-D2.10
  > "Why come so late in the year?"                          → TAS-D2.15
  > (Read the papers.)                                       → TAS-D2.20
TAS-D2.10 TESSALY: "No. You can't know that. I'd say no either way. So I won't waste your time with it."   → TAS-D2 options
TAS-D2.15 TESSALY: "The list says before hard frost. Frost doesn't wait for a good season to be polite in."   → TAS-D2 options
TAS-D2.20 TESSALY: (hands them over; waits while they're read) "Three cramps named. Iron's in a cache under your corners. Your gate wouldn't let it in."   {document inspects TAS-I1, TAS-I2; event: S01_papers}
  > [carrying cooked food] "Eat something."                  → TAS-D2.40 {take food; set TAS_FED}
  > "Who's the youngest?"                                    → TAS-D2.30
  > "I'll go and look at the arch."                          → end
TAS-D2.30 ANSA: "Me. Ansa." (beat) "How far's the next village? From here? Any way?"
TAS-D2.31 TESSALY: "Far enough. Sit down, Ansa."   → TAS-D2.20 options
TAS-D2.40 BJARKE: "Food that isn't ours. That's a good day." (to the wind outside) "Hear that? A good day."
TAS-D2.41 TESSALY: "Thank you." (exact) "We'll owe you a bowl. We pay what we owe."   → TAS-D2.20 options
```

```
TAS-D3.01 DORN: (at the ladder foot) "You're striking iron on my gate? Then I'm listening to it."
TAS-D3.02 DORN: "Don't tell me what the paper says first. I want to hear it clean."
TAS-D3.10 [after J1] DORN: "Sick."
TAS-D3.11 [after J2] DORN: "Sick. Not as bad."
TAS-D3.12 [after J3] DORN: "That one's fine. Your paper's wrong."
TAS-D3.13 [after J4] DORN: (long pause) "That's the worst of them. Paper didn't know."
TAS-D3.20 [all four] DORN: "Two sick it named. One sound it named. One bad it missed." (climbing down) "Paper's not lying. Paper's old."   {event: S02_arch}
```

```
TAS-D4.01 (removed: CDR-1, T-4; the bandits fight to 0 HP and nobody talks afterwards)
TAS-D4.10 (removed: CDR-1, T-4)
TAS-D4.11 (removed: CDR-1, T-4)
```

```
TAS-D5.01 GEIR: (in the gate, arms folded; tower-hands behind) "That's Emberholt iron on those mules."
TAS-D5.02 GEIR: "And Emberholt hands waiting to put it in our gate. Our gate."
TAS-D5.03 GEIR: (to a tower-hand) "Horn. Gather. Let the barracks see what's coming in."
TAS-D5.04 TOWER-HAND: (lifts the horn)
TAS-D5.05 RESSA: (from the horn post stair, not loud) "No." (beat) "Gather's for the mountain. Not for our own guests."
TAS-D5.06 GEIR: "They're not our guests. They're Vessa's prisoners."
TAS-D5.07 RESSA: "Then they're ours twice." (to the player) "Well, walker. You've been up the arch."
  > "Come and strike the worst one yourself."                → TAS-D5.10
  > "Guard the work, then. A tower-hand at every pole, all night."   → TAS-D5.20
  > "Ressa. Rule on it."                                     → TAS-D5.30
TAS-D5.10 GEIR: (a long look; then up the ladder; strikes J4; the dull clack) "...That's not a gate. That's a guess."
TAS-D5.11 GEIR: "Let the mules in. I'm watching every spark."   {set TAS_PROOF = proof}  {event: S04_tower}
TAS-D5.20 GEIR: "Ours on the poles." (thinks) "Ours on the gate. Theirs on the iron." (to his crew) "You heard. Poles."   {set TAS_PROOF = watch}  {event: S04_tower}
TAS-D5.30 RESSA: "Work goes ahead under Warden watch. Tower crew keep the gate. That's all."
TAS-D5.31 GEIR: (obeys; doesn't look at either of them) "Warden watch."   {set TAS_PROOF = ruled}  {event: S04_tower}
```

```
TAS-D6.01 TOWER-HAND: (throwing a bedroll into the yard) "Papers check. Just checking papers."
  > "The papers are with Vessa. The bedrolls aren't."        → TAS-D6.10
  > "Your captain's watching the gate. Go and watch it with him."   → TAS-D6.20
  > [TAS_PROOF = ruled] "Ressa's watch. Go and tell her what you're doing."   → TAS-D6.30
TAS-D6.10 TOWER-HAND: (looks at the bedroll in the snow; picks it up; puts it back, badly) "...Checked."   → end
TAS-D6.20 TOWER-HAND: "He's cold." (beat) "So am I. Fine."   → end
TAS-D6.30 TOWER-HAND: (stops) "No." (puts the bedroll back) "No, I won't."   → end
      {all: event: protect interruption 2 resolved}
```

```
TAS-D7.01 VESSA: (gate book open; writes) "'Inner arch: four cramps tested. Three made good.' That's true whoever reads it."
TAS-D7.02 VESSA: "Rest is up to what I write next. Papers. Names. Or neither."
  > "Write who mended it. Their names."                       → TAS-D7.10
  > "Send the papers to the Assembly's clerk. Let someone who's seen a seal decide."  → TAS-D7.20
  > "Give them their papers. Write the arch. Not them."       → TAS-D7.30
TAS-D7.10 VESSA: (writes) "'Made good by T. Varn's crew, Emberholt. Papers: not known. Arch: true.'" (beat) "Geir will see that."
TAS-D7.11 VESSA: "Good. It's true."   {set TAS_ACCOUNT = named}  {event: S07_book}
TAS-D7.20 VESSA: (writes) "'Papers sent to Stonewake for the clerk.'" (beat) "Then they wait. All winter, likely."
TAS-D7.21 VESSA: "I'll let them have the brazier at night. That's mine to give."   {set TAS_ACCOUNT = held}  {event: S07_book}
TAS-D7.30 VESSA: (writes) "'Inner arch made good. Wardens.'" (looks at it) "We write what we closed. Not who."
TAS-D7.31 VESSA: "I've never liked that line." (closes the book) "Still the line."   {set TAS_ACCOUNT = unwritten}  {event: S07_book}
```

```
TAS-D8.01 [named] TESSALY: (at the gate at the clear window; the tower crew silent on the post) "They're not blowing Answer for us."
TAS-D8.02 [named] TESSALY: "But we're in your book. In ink." (beat) "I'll tell the guild. They'll pretend not to care."
TAS-D8.01 [held] TESSALY: (in the shed, brazier lit) "A winter at Passwatch. Bjarke's thrilled."
TAS-D8.02 [held] BJARKE: "Thrilled." (to the wind) "You hear? Thrilled."
TAS-D8.03 [held] TESSALY: "If the clerk ever answers, I'd like to know what a seal is worth up here."
TAS-D8.01 [unwritten] TESSALY: (before dawn, the mules loaded, the tower empty) "Then we were never here." (beat) "We're used to it."
TAS-D8.02 [unwritten] TESSALY: "The arch knows. That'll have to do."
TAS-D8.04 [TAS_FED] ANSA: "You fed us. I'm writing that down. In our book."
TAS-D8.05 [TAS_CREW_HELPED] TESSALY: "You let Bjarke do the hard bit. He'll be insufferable."
TAS-D8.06 TESSALY: "Strike it in spring. Listen. If it hangs, it's good." (bows, exactly)   {event: S08_close → quest Completed}
```

#### Documents and inspect texts

**`TAS-I1` — Guild work order** (Tessaly's papers, document):
> *Work order. To Passwatch, the Windscar Inner Gate. The bearer, T. Varn, mason of the guild, with three, to make good the inner arch's iron according to the guild's maintenance list. Materials carried: cramps, twelve; lead, four pigs. Payment by the guild. No charge to the holders of the gate.*
> *Seal of the guild.* (A round seal in red wax: a hammer over a flame, the flame in a newer, cleaner cut than the hammer.)

**`TAS-I2` — Safety notice** (document):
> *Notice of risk. The inner arch at the Windscar Inner Gate: cramps at the second, fourth and fifth joints of the keystone course are listed for replacement. Rust in leaded iron jacks the stone. Expect movement at hard frost. Replace before.*
> *By the guild's list. Copied.*

| Id | Object | Text |
|---|---|---|
| `TAS-I3` | Arch joints (two kinds of iron) | "Flat cramps of ridge iron, and among them a few round-headed ones of a different make. Both leaded in. No date on either." |
| `TAS-I4` | Lifted voussoir (J4) | "Raised a fingernail's width. Rust stain under it like spilled tea." |
| `TAS-I5` | Guild case | "Oiled leather, a guild mark tooled on the lid. Inside: rules, a level, a folded list. The list is Tessaly's and stays in the case." |
| `TAS-I6` | Tessaly's forge | "Charcoal, bellows, a lead pot. An ordinary forge. The tower crew watch it like a dog." |
| `TAS-I7` | Gate book (after S07) | Per outcome, the line Vessa wrote, in her square hand. |

---

## TGM — Greymantle

### TGM.1 The quest in one paragraph

Bears on the Stormwake shoulder sleep from first snow to thaw. **Greymantle**, an old grey-backed ridge bear in the trappers' stories since before most of them were born, is up in deep snow, starving, and has broken a goat fold above the Black Glass Hostel road. Yrsa Fellhand, a trapper wintering at the hostel, notched the night he woke on her tally stick: no thaw, no storm, only a hum from the high halls that the hostel's weather slate also wrote down. The player tracks him: the broken fold, a dragging forepaw in the snow, grey hair on a rubbing pine taller than Yrsa remembers, ridge crows over a cache where wolves are stealing his kill, and frost dust knocked off bare rock where prints cannot hold. The den is a cliff cave whose inner chamber is a **null-point**. Inside, there is no sound at all: not the player's steps, not their blows, not the bear. He rears and roars and nothing reaches the ear; the dust jumps off every ledge and the frost flakes off the walls in a ring. Every telegraph in the fight is sight and dust. He fights to the end and dies in the quiet of his own den, and the player and Yrsa decide how the old bear is left: the den sealed as his resting place, or his hide and fat to the trappers for the hostel's winter.

**Remember:** a roar you can see and cannot hear. **Want next:** to know what hums in the high halls on nights with no storm (TF-M4, if not yet played).

### TGM.2 Selection record

| Candidate | Verdict |
|---|---|
| **A. A bear arena fight with audio cues.** | Rejected. Ordinary; wastes the null-point. |
| **B. Prove the horn trials woke him.** | Rejected. A side effect cannot be proved by a bear; phenomena prove nothing (bible §11.3). The dates are set side by side and stay an inference. |
| **C. Track by four kinds of sign → silent fight read by sight and dust → a choice about how an animal is left** | **Selected.** Tracking first (brief); the fight inverts Thornfell's sound system and is an accessibility showcase; the end is a judgement, not a loot drop. |

### TGM.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Ridge bears hibernate in cliff caves; rare encounters | Dossier §X fauna | [CANON] |
| Null-points: sound drops out, footsteps muted, echoes vanish; Echohewn sound-dampening; clans think them solemn ground | Dossier §XVII; bible §1.1, §2.1 | [CANON] |
| Ridge crows; ridge wolves (howler) | Bible §10 | [NEW on dossier fauna] |
| Black Glass Hostel, no-colours rule | Bible TP05 (Part 3) | [NEW, Part 3] |
| The Wall-Horn trials at the Summit; Iven's and Eyvind's dated records | Bible §2.3, TF-M4 | [NEW] |
| Greymantle (miniboss), his den (TP25) | Bible §7.2, §10 | [NEW] |
| Yrsa Fellhand, the tally stick, the hostel weather slate | This package | [NEW] |

### TGM.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.greymantle` |
| Type | Combat challenge, **miniboss** (bible §7.2, §10) |
| Unlock | TF-M2 Completed (`TH_SEASON` = snow). Offered by Yrsa Fellhand in the Black Glass Hostel yard (`TGM-D1`). |
| Resume hook | Yrsa at the hostel yard (`TGM-D1.00`), or at the den mouth once reached. |
| Target length | 30–40 minutes |
| Combat share | ~45% |
| Skills | Melee or Ranged; Hunting optional (butchering in the `ended` outcome) |
| Choice | Seal the den as his resting place, or leave him to the trappers (both honoured) |
| Outputs | `TGM_OUTCOME` = ended / sleeping; `TGM_DATES` (optional read) |
| **Anchor** | Stormwake's trappers and the Black Glass Hostel; the ridge-bear family |
| **World-truth row** | None (present-day only). Touches the present splinter trials (H25) as a side effect, never as evidence. |
| **Revelation role** | Self-contained. Lightly supports R07's seeds (another dated "hum with no storm" record) without owning or proving anything. |
| **Recurring evidence** | The hostel weather slate (Halla's; recurs in *The Snow-Height Mark* as a place, not as proof). With TF-M4 Completed, Eyvind's trial record is recalled, not re-read. |
| **State compliance** | Inactive / Active / Completed; `TGM_OUTCOME`; no fail; Greymantle resets on leaving with step progress kept. |

### TGM.5 The places

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **G1. Black Glass Hostel yard** (TP05) | Hook; weather slate | A trapper's sled, snare wire coiled on pegs, Yrsa's tally stick hanging by the door. The hostel's **weather slate** by the porch: chalk lines by night. | — |
| **G2. The broken fold** | Track 1 | A drystone goat fold on a shieling shelf, its wall pushed out in one place as if leaned on. Wool on the stones; blood frozen brown; claw scores on the gatepost a head higher than a man. | — |
| **G3. The print line** | Track 2 | Prints in deep snow, wide as a shield, the left fore dragging a furrow. They wander: starving animals do. | — |
| **G4. Rubbing pine** | Track 3 | A wind-bent crag-pine; grey hairs caught in bark at shoulder height. | — |
| **G5. The kill cache** | Track 4; wolves | A goat carcass half-buried in snow under an overhang. Ridge crows circling over it in a slow column (seen from far off). Wolves have found it. | — |
| **G6. Bare rock** | Track 5 | Wind-scoured rock where prints cannot hold. Frost feathers on the rock are knocked off in a line where something heavy brushed past: a dark stripe through white. | — |
| **G7. Den approach** | Climb | A cliff path to the cave. | **Agility trigger:** shimmy a ledge (shortcut). **Walkable fallback:** a long switchback. |
| **G8. Outer cave** | Last sound | Ordinary cave sound: drip, wind at the mouth, the player's own breath. Bones. A pressed-flat bed of old bracken. | — |
| **G9. The inner chamber** (null-point) | Arena | A round chamber cut smooth in places (Echohewn work, undescribed). Dust lies thick on every ledge; frost on the walls. Three **stone pillars** stand clear of the walls; a **hollow** at the back, the quietest place, with Greymantle's bed. Dust falls straight down here. | — |

**MAP VERIFICATION REQUIRED:** the den is in Stormwake within reach of the hostel road; the kill cache sits between the fold and the den.

### TGM.6 Player-facing sequence

**Beat 0 — Up in deep snow (`S00_hook`).** *Objective: Hear Yrsa out.* `TGM-D1`. Yrsa: Greymantle is up, a starving bear is on the hostel road, and she would rather it was done by someone who can do it properly.

**Beat 1 — The night he woke (`S01_dates`, optional `S02b_dates`).** *Objective (optional): Look at the hostel's weather slate.* The tally stick's notch and the slate's chalk line agree on a night: *"Hum from the high halls. No storm."* With TF-M4 Completed, the player's journal adds that Eyvind's trial record has a test that night (no re-read; the record is with whoever `TH_HORN` gave it to). Yrsa: "Doesn't prove a thing. Bears wake for a thaw. There wasn't one." Sets `TGM_DATES`. Never required.

**Beat 2 — Track him (`S02_track`).** *Objective: Track Greymantle.* Five sign stages in order; each inspect pins the next. G2 fold (inspect the gatepost scores and the pushed wall) → G3 print line (inspect two print sets; the dragging forepaw) → G4 rubbing pine (inspect the hair: Yrsa's bark "Taller than when I last saw him. Or I've shrunk.") → G5 the kill cache, found by **crows** circling in a column visible from G4 (**TGM-E1** wolves on the cache) → G6 bare rock, where the player follows the **dark stripe through the frost** (inspect twice). Click-to-move friendly; nothing is timed. **Verbs:** track, read sign.

**Beat 3 — The den (`S03_den`).** *Objective: Find Greymantle's den.* Climb G7 (shimmy or switchback). Yrsa stops at the mouth: "I don't go in. Not because I'm scared. Because I'm sensible." In the outer cave (G8) the sound is ordinary. Stepping into G9, the sound goes: first the drip, then the wind, then the player's footsteps (TGM.8). Greymantle stands up out of the hollow.

**Beat 4 — Greymantle (`S04_fight`).** *Objective: Stop Greymantle.* Miniboss (TGM.7.1). He fights to 0 HP (CDR-1) and dies where he falls; the quest keeps his body there (no fade) until `S06_choice`.

**Beat 5 — The hollow (`S05_yrsa`).** *Objective: Fetch Yrsa.* Step out to G8 (sound returns); Yrsa comes in to the chamber edge (`TGM-D3`). In the null-point her lines are subtitles only; she speaks them in the outer cave on the way in and goes silent past the threshold (presentation rule: no voiced audio inside G9).

**Beat 6 — How he is left (`S06_choice`).** *Objective: Decide what happens to Greymantle.* TGM.11. **Leave him to the trappers:** Yrsa whistles the hostel's trappers up from the road; the player may help butcher (Hunting, optional) or leave it to them (one interaction, 2 s; no gore; the camera stays on the player's back and the dust). His hide and fat go to the hostel's winter. **Seal the den:** carry three stones from the outer cave's rockfall (light carries) and stack the inner threshold, then hang Yrsa's snare-net with stormflower stems woven in across the gap (interaction) "so the wind can't reach him". The quiet room is his resting place.

**Beat 7 — The hostel (`S07_close`).** *Objective: Return to the Black Glass Hostel.* `TGM-D4`. Quest Completed.

### TGM.7 Encounters

Tuned for late Competent to early Advanced (TD-12).

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TGM-E1** | 1 × ridge wolf howler, 2 × runner; 4 × ridge crow (flock) | Kill cache (G5) | Wolves defend the carcass; crows mob a player under 50% HP | **Howl** (~1.5 s, head lifts); runners commit 4 s later. **Runner lunge:** crouch, tail flat (~0.8 s). **Crow dive:** the flock tightens into a line (~1.0 s). | Required (wolves). A crow that dives is an ordinary enemy, defeated at 0 HP; crows that never dived stay circling as scenery | 50–80 s |
| **TGM-E2** | **Greymantle** | Inner chamber (G9) | Miniboss; spec below | Visual only | Required | 3.5–4.5 minutes |

#### TGM.7.1 Miniboss spec — Greymantle

| Field | Spec |
|---|---|
| Family | Ridge Bears, elite (bible §10). An animal; fights to 0 HP (CDR-1). |
| Read | Huge, grey across the back, ribs showing under the coat. Left forepaw lame: he favours it, and his left-side swipes are slower. Snow and frost still caked in his ruff; it sloughs off when he moves hard. His breath plumes in the cold. |
| **Audio rule** | Inside G9 **no world audio plays**: no bear sounds, no player footsteps, no hit sounds, no voiced lines. UI sounds also muted inside G9 [PROPOSAL — DIRECTOR; see TGM-OD1]. Controller rumble carries impacts where supported. Every telegraph below is visual and has a fixed duration. |
| Arena | G9: three **pillars** (block charges; a charge into a pillar stuns him 2 s), the **hollow** at the back, thick dust on all ledges. |
| **Swipe** (all phases) | He shifts his weight onto the back legs and the ruff lifts; snow sloughs off his shoulder on the swiping side (**1.0 s**; left side **1.4 s** because of the lame paw). Wide arc, moderate damage. Cadence ~6 s. |
| **Charge** (all phases) | He drops his head and paws the floor twice; each paw-strike throws a **puff of dust** (**1.6 s** total). Straight-line charge across the chamber, heavy damage. Stepping behind a pillar makes him hit it (2 s stun: free hits). Cadence ~12 s. |
| **The silent roar** (P2–P3) | He rears to full height and his breath plumes (**2.0 s**). The roar makes no sound. On release, **dust jumps off every ledge** and falls straight down in curtains, and the frost flakes off the walls in a ring expanding from him (radius 8 m, visible ring). Inside the ring: knockdown (1.5 s). Outside: nothing. After the roar, the dust curtains hang for 6 s and **hide his outline** except where he moves through them (he shows as a dark shape that disturbs the falling dust). |
| **Ceiling fall** (P2–P3) | He rears against a wall and strikes it. **Dust shadows** appear on the floor first: a patch of dust falling straight down marks where a stone will land (**1.8 s**). Then a stone falls there. Max 3 at once. |
| **From the side** (P3, below 35%) | He goes into the hollow and out of sight; 3 s later he comes out from behind one of the pillars. The tell: **dust trickles from that pillar's top** (**1.5 s**) before he steps out. Once per 20 s. |
| Phases | P1 100–60%: swipe, charge. P2 60–35%: + silent roar (~18 s), ceiling fall. P3 below 35%: + from the side; roar ~14 s. No enrage. |
| End | At 0 HP he goes down where he stands; one last plume of breath, and the dust settles on him. Combat ends. His body stays as a per-player quest prop (no fade) until `S06_choice`. |
| Reset | If the player leaves G9 or dies, he returns to the hollow at full health. Tracking steps stay complete. |
| Accessibility | Because the fight has no audio at all, it is the slate's reference case for visual-only telegraph readability. All tells are large-silhouette changes or dust/frost events, never colour alone. |

### TGM.8 The strange moment: the silent roar (presentation spec)

| Time | Element | Spec |
|---|---|---|
| Threshold | **The sound goes** | Crossing into G9, over 2 s: the drip stops, then the wind at the cave mouth, then the player's own footsteps. Breath audio stops last. A held silence with no tone or hum under it. |
| 0–3 s | **He stands** | Greymantle rises out of the hollow; snow slides off his back and makes no sound. |
| 3–5 s | **The first roar** | He rears; his breath plumes; his jaw opens wide. **Nothing is heard.** Dust jumps off every ledge in the chamber at once and falls straight down. Frost flakes off the walls in a ring travelling outward. Controller rumble only. |
| 5–8 s | **The settle** | The dust falls in straight curtains (null-point tell). The fight begins (objective appears only now). |
| After | **Outside** | Leaving to G8 brings the drip back first. Yrsa (if present): *"You were shouting. I couldn't hear you either."* |

**Cannot prove:** anything. Nobody explains the chamber. Yrsa calls it "the quiet room" and nothing more.

### TGM.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Hear Yrsa out. | `TGM-D1` end node | Yes |
| `S01_dates` | (Optional) Look at the hostel's weather slate. | Inspect slate + tally stick | No (`TGM_DATES`) |
| `S02_track` | Track Greymantle. | Five sign stages in order (G2–G6 inspects) + TGM-E1 wolves defeated | Yes |
| `S03_den` | Find Greymantle's den. | Enter G9 volume | Yes |
| `S04_fight` | Stop Greymantle. | Greymantle defeated (0 HP) | Yes |
| `S05_yrsa` | Fetch Yrsa. | `TGM-D3` reaches choice | Yes |
| `S06_choice` | Decide what happens to Greymantle. | Butcher interaction (player or trappers), **or** 3 stone carry-deposits + net interaction | Yes |
| `S07_close` | Return to the Black Glass Hostel. | `TGM-D4` end node | Yes (→ Completed) |

### TGM.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TGM_DATES` | `S01_dates` | `TGM-D4` line |
| `TGM_OUTCOME` = ended / sleeping | `S06_choice` | Den prop; hostel barks; *The Snow-Height Mark* Halla line (request) |

### TGM.11 Choices and consequences

| Option | Immediate | Cost | Honoured how |
|---|---|---|---|
| **Leave him to the trappers** — *"Leave him to the trappers. The hostel needs the winter."* (`ended`) | Yrsa kneels by him for a while, then whistles the trappers up. Hunting: the player may help butcher (the trappers do it otherwise); hide and fat go to the hostel's winter, meat to its store and to Hushfold. | Greymantle is gone from the shoulder's stories. Yrsa's grief, short and dry. The hostel's children ask where the grey bear went. | Yrsa hangs one grey hank of his coat by the hostel door. The den is empty (prop). Hostel barks: winter meat, and a toast "to the old one". |
| **Seal the den** — *"He went where it's quiet. Let him have it."* (`sleeping`) | Stack the threshold; hang the stormflower net. The quiet room is his resting place. | The hostel goes into winter without his hide and fat. Yrsa puts a cairn below the den and will not set her best snare line under it. | The stacked threshold and net stay (prop). Yrsa's bark: "Stones are still up. I walk past. I don't go in." |

No option is wrong. Neither gives the old bear his rest and the hostel its winter.

### TGM.12 Rewards and unlocks

Small payment from the hostel's box. Yrsa's snare lore in dialogue (later Hunting barks). In `ended`, a share of meat (food items from the item pass; none if the pass defines none). Melee and Hunting XP from actions. A trapper's "grey hank" is a prop, not an item. No lump XP.

### TGM.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Walking away | Stays Active; tracking stages persist; resume at Yrsa or the den mouth. |
| Death in the den | Respawn at the den mouth (G8). Greymantle resets to the hollow at full health. |
| Lost on bare rock | The frost stripe cannot vanish; Yrsa's bark from the last stage points ("Look for where the frost's been knocked off."). |
| Logout during the stacking | Stones carried and stacked persist; the net interaction remains. |
| Co-op | Greymantle is a shared world creature; all present on `S04` get credit. Silence applies to every player in G9. The choice is per player; den state is a per-player prop (fallback: the host's state). |

### TGM.14 Integration needs

| Need | Owner | Minimum viable form | Fallback |
|---|---|---|---|
| Total-silence audio zone | Audio | A volume that mutes all world and voice buses (and UI, pending OD1) with a 2 s staged fade, restoring on exit | Heavy low-pass plus 90% duck |
| Visual-only telegraphs (dust jumps, frost ring, dust shadows, pillar trickle) | VFX; Gameplay Designer | Particle events bound to ability wind-ups with fixed durations | Decal telegraphs (rings, lines) |
| Dust-curtain occlusion of the bear | VFX | Falling-dust volume with partial silhouette | Short darkening only |
| Charge-into-pillar stun | Gameplay Designer | Collision check on the charge path | Remove stun; pillars only block |
| Sign-trail pinning | Systems Engineer | Inspect events that reveal the next stage marker | All stages visible from the start |
| Crow column visible at distance | VFX | Looping flock above the cache | Waypoint after G4 |
| Per-player den prop | Systems Engineer | Keyed to `TGM_OUTCOME` | Host's state |
| Body kept after defeat | Systems Engineer | On-defeat quest hook: Greymantle's body stays as a per-player prop (no corpse fade) until `S06_choice` | Swap to an authored body prop at the point of defeat |

### TGM.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | Greymantle woke on a night the Wall-Horn was tested at the Summit. Whether the test woke him is not known to anyone, including the author's text: the dates agree, and that is all. |
| Public belief | Trappers: an old bear's bad winter. Hostel: "the hum". |
| Player-observable | Tally stick and weather slate (and, with TF-M4, a recalled trial date). |
| Wrong reading | "The Summit sent him." Nothing sends anything. |
| Withheld | Why the Echohewn cut a quiet room in a bear's cliff (TDS01's withheld layer applies). |

### TGM.16 Open decisions

| # | Decision | Recommendation |
|---|---|---|
| TGM-OD1 | Mute UI sounds in the null-point too? | Yes, for the full effect, with rumble and visual hit flashes; the Director and the accessibility review decide. **[PROPOSAL — DIRECTOR]** |
| TGM-OD2 | Should `sleeping` lead to a thaw encounter? | **Closed (CDR-1):** Greymantle dies at 0 HP in both outcomes; `sleeping` now means the den is sealed as his resting place. No thaw encounter. |

### TGM.17 Internal review log

| Check / finding | Result |
|---|---|
| Draft had Yrsa say the hum woke the bear. | Changed: she says it proves nothing. Dates sit side by side only. |
| Draft let the bear be fought in the outer cave with sound. | Cut: the identity is the silent fight. The outer cave is the safe point. |
| Accessibility | Every tell is a silhouette, dust or frost event with a fixed duration; no colour-only reads. |
| Evidence rule | Combat reveals nothing; the bear carries nothing. |
| **Director rulings reconciliation (2026-11-03): CDR-1** (rulings §4, mercy without an exception). The 10% lie-down is removed. | Greymantle fights to 0 HP; `S04_fight` completes on defeat; his body stays until `S06_choice`. `S06_choice` and `TGM_OUTCOME` (ended / sleeping) kept, reframed as how the old bear is left: left to the trappers (hide and fat for the hostel's winter) or the den sealed as his resting place (three stones, the stormflower net). TGM-D3.02/.04/.10/.20, TGM-D4.01 [sleeping] and TGM-B5 adjusted; TGM-E1 crows no longer scatter. TGM-OD2 closed. |

### TGM.18 Dialogue

#### Cast notes

**Yrsa Fellhand [NEW]** — Stormwake trapper wintering at the Black Glass Hostel. *Knows:* bears, snow, the shoulder; the night she notched. *Doesn't know:* what hums in the high halls. *Voice:* dry, practical, fond of the bear in a way she won't admit. "Sensible" is her highest word.

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `TGM-B1` | YRSA | Hostel yard, quest available | *"Old Grey's up. In this. He's never up in this."* |
| `TGM-B2` | YRSA | At the rubbing pine | *"Taller than when I last saw him. Or I've shrunk."* |
| `TGM-B3` | YRSA | Player stalls on bare rock | *"Look for where the frost's been knocked off. He's heavy. He brushes."* |
| `TGM-B4` | YRSA | Den mouth | *"I don't go in. Not because I'm scared. Because I'm sensible."* |
| `TGM-B5` | YRSA | Post-quest, `sleeping` | *"Stones are still up. I walk past. I don't go in."* |
| `TGM-B6` | HOSTEL CHILD | Post-quest, `ended` | *"Where's the grey bear gone?"* / YRSA: *"Into the stew. Eat it respectfully."* |

#### Nodes

```
TGM-D1.00 [quest Active, returning] YRSA: "Still out there. Still hungry. Go on." (pins step)  → end
TGM-D1.01 YRSA: "Greymantle. Old Grey. My mother had stories about him and she wasn't young."
TGM-D1.02 YRSA: "Bears sleep first snow to thaw. He's up. Broke the Hallin fold two nights back." (the Hallin fold: a shieling fold [NEW])
TGM-D1.03 YRSA: "A starving bear on the hostel road. I'd rather it was done properly than by somebody brave."
  > "When did he wake?"                                     → TGM-D1.10
  > "Where do I start?"                                     → TGM-D1.20
TGM-D1.10 YRSA: (taps the tally stick by the door) "That notch. No thaw. No storm. A hum from the high halls, Halla wrote it on her slate."
TGM-D1.11 YRSA: "Doesn't prove a thing. Bears wake for a thaw. There wasn't one."   → TGM-D1 options
TGM-D1.20 YRSA: "At the fold. He's lame on the left fore. You'll see it in the snow." (beat) "Don't follow it into the dark without looking up."   {event: S00_hook}
```

```
TGM-D3.01 YRSA: (in the outer cave, before the threshold) "Is he dead?"
TGM-D3.02 YRSA: (at the chamber edge; from here on, subtitles only) "He is. In the quiet bit." (looks at him a long while)
TGM-D3.03 YRSA: "He went where it's quiet. Can't blame him. Nothing reaches in there."
TGM-D3.04 YRSA: "So. Shut the door on him and leave him be. Or the trappers have him. Hide and fat'd see the hostel through." (beat) "I've done both in my time."
  > "Leave him to the trappers. The hostel needs the winter."   → TGM-D3.10
  > "He went where it's quiet. Let him have it."             → TGM-D3.20
TGM-D3.10 YRSA: (nods once) "Properly, then. He never wasted anything either."   {set TGM_OUTCOME = ended}  {butcher interaction available}
TGM-D3.20 YRSA: "Stones from the fall. Three. Then my net, with stormflower in it. So the wind can't reach him." (beat) "Stormflower keeps the wind out. My mother said. I've never checked."   {set TGM_OUTCOME = sleeping}  {stones available}
```

```
TGM-D4.01 [ended] YRSA: (hanging a grey hank of coat by the hostel door) "There. Now he's in the stories and the stew."
TGM-D4.01 [sleeping] YRSA: "Den's shut. I've put a cairn up. Won't set my line under it. Lost my best line." (beat) "Worth it. Probably."
TGM-D4.02 [TGM_DATES] YRSA: "Halla's slate and my stick still agree. Doesn't mean anything. I keep looking at it anyway."
TGM-D4.03 YRSA: (pays from the hostel box) "Hostel's money. I'm just the one who's sensible enough to hand it over."   {event: S07_close → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `TGM-I1` | Tally stick | "Notches for nights. One is cut deeper than the rest and has a little cross." |
| `TGM-I2` | Hostel weather slate | "Chalk lines by night. One reads: *'Hum from the high halls. No storm.'*" / [TF-M4 Completed] "You remember a test on that date in the hornwright's record." |
| `TGM-I3` | Fold gatepost | "Claw scores a head higher than a man. The wall pushed out as if leaned on." |
| `TGM-I4` | Print set | "Wide as a shield. The left fore drags a furrow." |
| `TGM-I5` | Rubbing pine | "Grey hairs in the bark, high up." |
| `TGM-I6` | Frost stripe | "Frost feathers knocked off the rock in a line, dark through white." |
| `TGM-I7` | Inner chamber wall | "Smooth in places, as if cut. Dust falls straight down past your hand." |

---

## TSG — The Salvage Ledge

### TSG.1 The quest in one paragraph

After TF-M3, Gerrit Carrick's miners walked away from their upper salvage camp, a ledge in the old siege works below the Horn Seat, and the Ridge Wardens put warden pairs on the lower ledges to watch the Seat's approaches. Now Shatterfall brigands have the camp. Two of them used to be Gerrit's. They are prising horn plates out of the gorge wall that the Seat's old rack should keep, and stacking them in his shed to sell to whoever pays. Gerrit asks the player to take his ledge back. The player climbs to it between wind windows and clears it in two parts: the outer works, where plate-throwers hurl plates that ring as they come, and the plate shed, where the Brigand Foreman, losing, bellows his last order down the ledge: cut the prop stones. He fights on to the end. Two cutters start on the props under the spoil terrace, which will drop a hillside of spoil onto the lower ledges where the warden pairs stand. The player runs the ledge's lip to three old horn-rests and blows **Fall** from each, listening for each pair's **Answer**, while stopping the cutters. Every pair gets under cover; whether the spoil terrace comes down depends only on how fast the cutters were stopped. The plates go back into the Seat's rack face to the rock, and the player decides whether Gerrit's crew may work the ledge again under licence.

**Remember:** a stack of stolen plates ringing faintly every time you blow the horn, and three Answers coming up out of the haze. **Want next:** to see the gorge with nobody on its ledges.

### TSG.2 Selection record

| Candidate | Verdict |
|---|---|
| **A. A straight camp clear.** | Rejected. Lacks the hold and the sound system. |
| **B. A timed escort of the warden pairs out of the gorge.** | Rejected. Duplicates TF-M3's rescue. |
| **C. Two-part assault → warn by horn while stopping cutters → plate-keeping → a choice about the ledge** | **Selected.** The player blows the calls for the first time as the one responsible for others; the hold has a split objective; no outcome harms a warden. |

### TSG.3 Canon grounding

| Element | Source | Status |
|---|---|---|
| Shatterfall Brigands: occupy unstable ledges; miners turned raiders; drawn to Echohewn scraps and war salvage | Dossier §IX | [CANON] |
| Broken siege engines embedded in cliff walls | Dossier §VII | [CANON] |
| Horn plates: tuned stone and horn, salvaged in the war | Bible §2.1 | [CANON] |
| The Ordinary Calls: Fall (short-long-short), Answer (two short) | Bible §9.4 | [NEW] |
| Gerrit Carrick; the Horn Seat; Carrick's Cut; the Salvage Ledge | Bible TP10, TP12, TP13; TF-M3 | [NEW] |
| Brigand Foreman (elite); pick-hand; plate-thrower | Bible §10 | [NEW] |

### TSG.4 Quest summary card

| Field | Value |
|---|---|
| Suggested content id | `thornfell.side.salvage_ledge` |
| Type | Combat challenge (bible §7.2) |
| Unlock | TF-M3 Completed. Offered by Gerrit Carrick at Carrick's Cut (`TSG-D1`). |
| Resume hook | Gerrit at Carrick's Cut (`TSG-D1.00`); after the ledge is taken, the warden pair leader on the ledge. |
| Target length | 30–40 minutes |
| Combat share | ~60% |
| Skills | Melee or Ranged; Mining optional (break a jammed hoist pin for a shortcut; crew alternative: Gerrit's man does it from below) |
| Choice | What becomes of the ledge (2 options) |
| Outputs | `TSG_SPOIL` = held / dropped; `TSG_LEDGE` = licensed / struck |
| **Anchor** | Shatterfall's miners (Gerrit Carrick) and the Ridge Wardens; the Horn Seat as a kept place |
| **World-truth row** | H11 (horn plates as wartime weapons) as material only; present pressure H25 (salvage for loud things). |
| **Revelation role** | Self-contained. Reinforces R06 (horn) aftermath without new evidence. |
| **Recurring evidence** | The Horn Seat's rack (TF-M3); no record is read here. |
| **State compliance** | Inactive / Active / Completed; `TSG_SPOIL`, `TSG_LEDGE`; no fail; the spoil cannot drop on a warden (TSG.6 Beat 5 rule). |

### TSG.5 The places

| Area | Purpose | Environmental storytelling | Traversal |
|---|---|---|---|
| **L1. Carrick's Cut** (TP13) | Hook | Gerrit's camp at the gorge mouth, quieter now: fewer tents, tools sold. A tally of debts chalked on a crate. | — |
| **L2. The gorge path up** | Approach | Shelves between fluted faces; the whistle tell before gusts. A jammed hoist pin on the old salvage hoist. | **Agility trigger:** a rope traverse across a gap. **Walkable fallback:** the old siege ladder route (longer). **Shortcut:** break the hoist pin (Mining) and ride the hoist; crew alternative from below. |
| **L3. Outer works** | Assault part 1 | The broken siege engine's frame built into a timber breastwork; brigand fires; plates leaning against the breastwork. | — |
| **L4. Plate shed** | Assault part 2; the stack | Gerrit's old shed, now stacked with prised plates in straw. Pry-bars. A chalk tally of plates by size. | — |
| **L5. Ledge lip and the three horn-rests** | The warning | Three old stone **horn-rests** cut along the lip, each aimed down at a different lower ledge (siege-works signal points). Below: haze, and three **warden pairs** on three lower ledges (visible as small figures from the right rest). | Walk along the lip; rope rail. |
| **L6. Spoil terrace and prop stones** | The cutters | The salvage spoil heaped on a timber-and-stone terrace above the lower ledges, held by **two prop stones** wedged under its lip. | — |
| **L7. The Horn Seat rack** (TP10) | Plate-keeping | The Seat's rack, aimed down the shelf. Empty slots. | Short path from L4. |

**MAP VERIFICATION REQUIRED:** the ledge sits above three lower ledges where warden pairs stand, with the spoil terrace above them; the Horn Seat is a short walk from the plate shed.

### TSG.6 Player-facing sequence

**Beat 0 — My old ledge (`S00_hook`).** *Objective: Hear Gerrit out.* `TSG-D1`. Brigands on his ledge, two of them his; plates going out of the gorge wall; warden pairs below who "don't know what's above them".

**Beat 1 — Up (`S01_climb`).** *Objective: Climb to the Salvage Ledge.* Wind windows (whistle tell, shelter behind marked faces); the rope traverse or ladder route; optional hoist shortcut.

**Beat 2 — The outer works (`S02_works`).** *Objective: Clear the outer works.* **TSG-E1.** Plates thrown at the player ring as they fly; plates that hit the breastwork ring the stacked plates beside them (the strange moment's foreshadow).

**Beat 3 — The plate shed (`S03_shed`).** *Objective: Take the plate shed.* **TSG-E2**, the Brigand Foreman (TSG.7.1). At his phase change (below half health) he turns his head and bellows down the ledge: "Cut them! Cut the props!" (`TSG-D2.02`), and the two cutters run for the prop stones. He fights on to 0 HP. When he is defeated, the cutters reach the props and start work: `S04` and `S05` begin, so the warning never overlaps the shed fight.

**Beat 4 — Fall (`S04_warn`).** *Objective: Warn the warden pairs below.* The player takes the **camp horn** (a work horn hanging in the shed; usable only for this quest) and runs the lip. At each **horn-rest** (L5) they **blow Fall** (interaction, 2 s; the call plays with its glyph). If the rest is aimed at a ledge with a pair, the pair's **Answer** comes back (two short) after a few beats; the echo count tells how far the ledge is, and the pair is seen moving under the overhang. Each rest serves one pair; all three are required, in any order. Objective counter: *Pairs answered 0/3*.

**Beat 5 — The props (`S05_props`).** *Objective: Stop the prop cutters.* Runs at the same time as Beat 4. **TSG-E3**: two cutters at the prop stones, each with a visible work bar (a cut takes ~90 s if left alone; a cutter attacked stops cutting to fight). A plate-thrower on a high ledge harries the lip. **No-harm rule:** the terrace can only drop after **all three pairs have answered**. If both props are cut through before that, the terrace shifts and sheds a small slide (a Fall hazard on the spoil slope, telegraphed by a ground-dust line ~1.5 s) and holds "one more breath" until the third Answer, then drops into empty ledges. Outcome: both cutters stopped before both props are cut → `TSG_SPOIL` = held; otherwise `dropped`. Either way every warden is under cover.

**Beat 6 — The pairs come up (`S06_wardens`).** *Objective: Meet the wardens.* The pair leader (role, `TSG-D3`) comes up the ledge path: dry thanks; the ledge is clear. With `dropped`: the lower path is buried; a scramble route opens over the spoil (new traversal; agility trigger with a walkable fallback round the head of it).

**Beat 7 — Face to the rock (`S07_plates` → `S07_choice`).** *Objective: Return the plates to the Horn Seat.* Carry the plate crate (heavy carry) to the Seat's rack (L7) and set them in (interaction). If Dorn is present (TF-M3 Completed; he comes up with the wardens), he turns each plate to face the rock (`TSG-D4`). Then Gerrit arrives: *Decide what becomes of the ledge* (TSG.11). Quest Completed on `TSG-D5`.

### TSG.7 Encounters

Tuned for Advanced identity (TD-12). Brigands fight to 0 HP (CDR-1): pick-hands, plate-throwers, cutters and the foreman. Melee or ranged; every thrower's perch is reachable on foot.

| Id | Enemies | Placement | AI role | Telegraph | Purpose | Solo target |
|---|---|---|---|---|---|---|
| **TSG-E1** | 3 × pick-hand, 2 × plate-thrower | Outer works (L3) | Pick-hands press; throwers hold the breastwork | **Pick overhead:** pick raised high, back arched (~1.1 s), heavy single blow. **Plate throw:** thrower draws a plate back and it **rings rising** as it is wound (~1.2 s; glyph: rising bar); a flat disc flies straight, then a second, delayed ring when it lands. Side-step. | Assault part 1 | 70–100 s |
| **TSG-E2** | **Brigand Foreman** + 1 × pick-hand | Plate shed (L4) | Elite; spec below | — | Assault part 2 | 2–3 minutes |
| **TSG-E3** | 2 × pick-hand (cutters), 1 × plate-thrower (high ledge) | Prop stones (L6); thrower above L5 | Cutters ignore the player until attacked; thrower harasses the lip | As E1; cutters show work bars | Split objective with the warning | 2–3 minutes total |

#### TSG.7.1 Elite spec — the Brigand Foreman

| Field | Spec |
|---|---|
| Read | A big ex-miner in a leather apron sewn with plate shards; a long pry-bar; a pick on his back. He talks the whole fight. |
| **Pry sweep** | Plants the pry-bar's foot and leans (~1.2 s); low sweep, knockdown on hit. Cadence ~8 s. |
| **Stack topple** (once per stack, 3 stacks) | He grabs a plate stack and heaves (~1.5 s; the stack rings as it tilts). Plates spill in a cone; damage and a 3 s ringing patch that slows. |
| **Second wind** (below 50%) | He drinks from a flask (2 s, interruptible by any hit). If not interrupted, heals 10%. Once. |
| Phase shout | Below 50% (with the second-wind phase): he turns and bellows down the ledge, `TSG-D2.02`; between swings, `TSG-D2.03`. Barks only; the fight does not pause. He fights to 0 HP. |
| Reset | Leaving the shed resets him to 100% unless defeated; spilled stacks re-stack. |

**Rules.** Combat never reveals evidence; the foreman's shouted lines are fight barks, not testimony. The plates are never loot: they are the plate crate (carry-state) only. Death respawns at the top of the gorge path (L2 head); cleared groups stay down; pairs already answered stay answered; prop-cut progress pauses while the player is dead.

### TSG.8 The strange moment: the plates answer (presentation spec)

| Time | Element | Spec |
|---|---|---|
| Blow 1 | **The stack hums** | When the player blows Fall at the first horn-rest, the plates stacked in the shed behind them ring faintly with it, a held sympathetic tone under the call, ~2 s. Water beaded on the stacked plates jumps into thin lines along their grooves. |
| Blow 2 | **Stronger** | The hum is louder; straw on the stack shivers. |
| Blow 3 | **And quiet** | The hum rises with the call and stops dead when the call stops. The beaded lines stay, and freeze where they are. |
| Then | **The fourth Answer** (optional competence beat) | After the third pair's Answer, a fourth two-short Answer comes up from an empty ledge. Counting the beats (the player's journal shows the count) matches the far face across the gorge: an echo of the third pair. The pair leader later: "Heard four. Counted. Face across." |
| Lines | | Gerrit (later, on hearing): *"They did that in the shed when the wind was right. We stopped sleeping in there."* |
| UI | | Subtitles "(the plates ring)"; glyphs for Fall and Answer. |

**Cannot prove:** anything. Tuned stone rings with a note near its own (bible §2.1). Nobody calls it anything else.

### TSG.9 Steps and completion events

| Step | Objective | Completes on | Req. |
|---|---|---|---|
| `S00_hook` | Hear Gerrit out. | `TSG-D1` end node | Yes |
| `S01_climb` | Climb to the Salvage Ledge. | Enter ledge volume | Yes |
| `S02_works` | Clear the outer works. | TSG-E1 all defeated | Yes |
| `S03_shed` | Take the plate shed. | Foreman defeated (0 HP) | Yes |
| `S04_warn` | Warn the warden pairs below. | 3 Answer events (one per horn-rest) | Yes |
| `S05_props` | Stop the prop cutters. | Both cutters defeated, **or** terrace drop event after S04 complete | Yes (sets `TSG_SPOIL`) |
| `S06_wardens` | Meet the wardens. | `TSG-D3` end node | Yes |
| `S07_plates` | Return the plates to the Horn Seat. | Carry-deposit at the rack + interaction | Yes |
| `S07_choice` | Decide what becomes of the ledge. | `TSG-D5` choice resolved | Yes (→ Completed on end node) |

### TSG.10 Flags

| Flag | Set by | Read by |
|---|---|---|
| `TSG_HOIST` | Hoist shortcut used | `TSG-D5` Gerrit line |
| `TSG_SPOIL` = held / dropped | `S05_props` | `TSG-D3`; ledge path prop |
| `TSG_LEDGE` = licensed / struck | `TSG-D5` | Carrick's Cut barks; *Seam Rights* (request) |

### TSG.11 Choices and consequences — the ledge

| Option | Immediate | Cost | Later |
|---|---|---|---|
| **License it** — *"Let Gerrit's crew work it. Iron and timber. Never plates."* (`licensed`) | The pair leader writes a Warden licence for iron and timber only, on Gerrit's word for his crew. | The ledge stays a camp; the plates in the wall stay within reach of anyone with a bar. The Wardens must keep a pair on the ledge. Gerrit stands surety on the ledge where two of his lads already went wrong. | Carrick's Cut barks: honest iron work; Gerrit's crew handle the plates in the wall like eggs. *Seam Rights* (request): Gerrit mentions the licence. |
| **Strike it** — *"Pull it down. Give the ledge back to the gorge."* (`struck`) | The shed is pulled down, the hoist rope cut. | Gerrit's men lose the last work they had in the gorge; Gerrit has nothing to show for his two lost lads but an empty ledge. | Carrick's Cut thins further; Gerrit is grateful and bleak. The ledge stays empty (prop). |

No option is wrong. Neither gives Gerrit work and keeps the plates beyond reach.

### TSG.12 Rewards and unlocks

Small payment from Gerrit ("from what's left"). A Warden standing line. The **scramble route** over the spoil if `dropped`; the **hoist** as a permanent shortcut if `licensed`. Melee (and Mining, if used) XP from actions. No lump XP.

### TSG.13 Failure, recovery, persistence, co-op

| Situation | Handling |
|---|---|
| Walking away | Stays Active; resume via Gerrit or the pair leader. |
| Leaving mid-hold | Answered pairs stay answered; cut progress pauses while the player is away and resumes on return. |
| Death | Respawn at the gorge path head; progress kept; the foreman, if not defeated, resets. |
| Player never fights the cutters | The terrace drops after the third Answer (`dropped`). Nobody is hurt. |
| Co-op | Shared brigands; each player's warning is per player (pairs and terrace presented per player; fallback: shared state, a partner credited only when their own active step uses it; CDR-6). Choice per player; ledge prop per player (fallback: host). |

### TSG.14 Integration needs

| Need | Owner | Minimum viable form | Fallback |
|---|---|---|---|
| Horn-blowing interaction with call playback and glyph | Audio; Systems Engineer | Interaction plays the Fall call; scripted Answer after N beats from the matching ledge emitter | Answer as subtitle + glyph |
| Cutter work bars that pause when engaged | Gameplay Designer | NPC channel that stops on aggro and resumes on reset | Fixed timer, paused while in combat |
| Terrace drop gated on all three Answers | Systems Engineer | Drop event requires both props cut **and** `S04` complete | Terrace never drops; `held` always |
| Sympathetic plate hum | Audio; VFX | One-shot hum layered under the call when within the shed radius; frost-line decal | Subtitle only |
| Distant warden pair figures moving to cover | Animation | Simple path-to-cover on Answer | Figures vanish behind the overhang |
| Per-player ledge state | Systems Engineer | Props keyed to `TSG_SPOIL`, `TSG_LEDGE` | Host's state |

### TSG.15 Mystery ledger

| Field | Entry |
|---|---|
| Author truth | The plates were worth something only while someone was building a horn; the brigands are selling into a market that is drying up. |
| Public belief | "Brigands are robbing the gorge for scrap." |
| Player-observable | Plate stacks, the chalk tally (prices crossed out and lowered twice), the plates' hum. |
| Wrong reading | The brigands work for the splinter. They don't; the tally shows a falling market and nothing else. |
| Withheld | Who else wants loud things (no buyer is named; no route is stated). |

### TSG.16 Open decisions

| # | Decision | Recommendation |
|---|---|---|
| TSG-OD1 | Should the re-racked plates interact with `TH_HORN` or *The Notes We Keep*? | No. They are gorge plates kept face to the rock at the Seat, never part of any horn. |
| TSG-OD2 | Dorn's presence | Only with TF-M3 Completed (always true by unlock) and only for one beat. |

### TSG.17 Internal review log

| Check / finding | Result |
|---|---|
| Draft could bury a warden pair if the player was slow. | Changed: the terrace drops only after all three Answers. Speed changes the terrain, never a life. |
| Draft let the foreman name the hornwright as his buyer. | Cut: no `[SPLINTER]` name; "anyone who wants a loud thing". |
| Distinctness from TF-M3 | No rope-rig, no Horn-Echo (clear weather only), no rescue; the player blows the calls. |
| Evidence rule | No record read; nothing proven. |
| **Director rulings reconciliation (2026-11-03): CDR-1.** Foreman yielded at 20%; brigands yielded and were taken by the wardens. | All brigands (pick-hands, throwers, cutters, foreman) fight to 0 HP. The foreman's order is a phase-change bark (`TSG-D2.02`, `D2.03`); `S04`/`S05` begin on his defeat. Foreman testimony cut (T-4: `TSG-D2.01`, `.10`, `.20` removed); the mystery ledger reads the chalk tally instead. `TSG-D3.03` and `TSG-D5.03`/`.10`/`.21` no longer depend on surviving brigands; the ledge choice, flags and steps are unchanged. Plates remain a carry-state crate, never loot. |

### TSG.18 Dialogue

#### Cast notes

**Gerrit Carrick [NEW, bible §5.2]** — Foreman of out-of-work miners. *Knows:* the ledge, the plates' price, the two men who left him. *Doesn't know:* who buys now. *Voice:* defensive, ashamed of the work, grateful; says "my lads" even about the brigands.

**Brigand Foreman [NEW, role]** — talks while fighting; a miner's humour; practical to the last.

**Pair leader [NEW, role]** — Ridge Warden; dry; counts.

**Dorn Feldhorn [CANON ANCHOR]** — one beat at the rack. *Guard:* no claim about the rear guard beyond what TF-M3 established.

#### Barks

| Id | Speaker | Condition | Line |
|---|---|---|---|
| `TSG-B1` | GERRIT | Carrick's Cut, quest available | *"Somebody's on my ledge. Two of them are mine. Were mine."* |
| `TSG-B2` | FOREMAN | Fight | *"Mind the stack! It's worth more than you!"* / *"Ringing, is it? That's money ringing."* |
| `TSG-B3` | CUTTER | Cutting | *"Two more blows. Two more."* |
| `TSG-B4` | PAIR LEADER | On each Answer, subtitle from below | *"Heard!"* |
| `TSG-B5` | GERRIT | Post-quest, `licensed` | *"Iron and timber. Never plates. I say it every morning."* |
| `TSG-B6` | GERRIT | Post-quest, `struck` | *"Nothing up there now. That's the point, I know."* |

#### Nodes

```
TSG-D1.00 [quest Active, returning] GERRIT: "Ledge is still theirs. Or it isn't. You tell me." (pins step)  → end
TSG-D1.01 GERRIT: "After the storm we came down and stayed down. Nobody pays for plates now. Good."
TSG-D1.02 GERRIT: "Brigands went up. My old ledge, my shed. Two of them were my lads."
TSG-D1.03 GERRIT: "They're prising the seat's plates out of the wall. And the Wardens have pairs on the ledges under the spoil." (beat) "They don't know what's above them."
  > "How many?"                                             → TSG-D1.10
  > "I'll take it back."                                    → TSG-D1.20
TSG-D1.10 GERRIT: "Eight, ten. A foreman with a pry-bar who thinks he's funny. He is, a bit."   → TSG-D1 options
TSG-D1.20 GERRIT: "If it goes bad, there are horn-rests on the lip. Old siege stones. They aim down." (beat) "You know Fall."   {event: S00_hook}
```

```
TSG-D2.01 (removed: CDR-1; the foreman no longer yields)
TSG-D2.02 FOREMAN: (fight bark at his phase change; turns his head and bellows down the ledge) "Cut them! Cut the props!"
TSG-D2.03 FOREMAN: (fight bark, between swings, reasonably) "Spoil comes down, path's gone, we walk off the back. Nothing personal."
TSG-D2.10 (removed: CDR-1; `S04` and `S05` now begin on the foreman's defeat)
TSG-D2.20 (removed: CDR-1, T-4; foreman testimony cut)
```

```
TSG-D3.01 PAIR LEADER: (up the path, snow on her shoulders) "Fall from the lip. Three times. Three rests." (beat) "Somebody's been taught."
TSG-D3.02 [held] PAIR LEADER: "Spoil's still up. Path's still there. Good."
TSG-D3.02 [dropped] PAIR LEADER: "Spoil came down on three empty ledges. Path's gone. We'll make another." (beat) "Heard four Answers, by the way. Counted. Face across."
TSG-D3.03 PAIR LEADER: "Ledge is clear. We'll keep a pair up here till Gerrit's had his say."   {event: S06_wardens}
```

```
TSG-D4.01 DORN: (at the rack, turning a plate) "Face to the rock."
TSG-D4.02 [TH_SHATTERFALL_ACCOUNT = amended] DORN: "They've looked down enough. Stone's honest now. So are they."
TSG-D4.02 [TH_SHATTERFALL_ACCOUNT = beside] DORN: "The roster's in the cairn. These can sit here and keep it company."
TSG-D4.02 [TH_SHATTERFALL_ACCOUNT = kept] DORN: "Roster's at the warden post. Plates are here. Nobody blows anything."
```

```
TSG-D5.01 GERRIT: (at the shed, looking at the empty plate straw) "So. My ledge."
TSG-D5.02 [TSG_HOIST] GERRIT: "You broke the hoist pin. It's been stuck since spring. Thanks, I think."
TSG-D5.03 GERRIT: "The two of mine went down with the rest. Knew them since they carried water." (beat) "I can speak for the crew I've got left. If there's work to speak for."
  > "Let Gerrit's crew work it. Iron and timber. Never plates."   → TSG-D5.10
  > "Pull it down. Give the ledge back to the gorge."             → TSG-D5.20
TSG-D5.10 PAIR LEADER: (writing) "Licence. Iron, timber. Not plates. A pair on the ledge." (to Gerrit) "Your word for your crew."
TSG-D5.11 GERRIT: "My word." (beat) "It's not worth much. It's what I've got."   {set TSG_LEDGE = licensed}
TSG-D5.20 GERRIT: (a long breath) "Fair." (takes a pry-bar to his own shed's corner post) "I built it. I'll pull it."
TSG-D5.21 GERRIT: "Nothing up here, then. For any of mine." (beat) "Those two knew. I knew."   {set TSG_LEDGE = struck}
TSG-D5.30 GERRIT: (pays) "From what's left. Don't count it in front of me."   {event: S07_choice → quest Completed}
```

#### Inspect texts

| Id | Object | Text |
|---|---|---|
| `TSG-I1` | Chalk tally in the shed | "Plates by size: hand, forearm, shield. Forty-one. A price beside each size, crossed out and lowered twice." |
| `TSG-I2` | Prised wall | "Fresh pry marks round empty sockets in the gorge wall. Grit on the ledge below." |
| `TSG-I3` | Horn-rest | "A stone cradle for a horn, cut in the lip, aimed down at a ledge in the haze." |
| `TSG-I4` | Prop stone | "Wedged under the terrace lip. Fresh cut marks across its waist." |
| `TSG-I5` | Stacked plate (after the calls) | "Frost in thin lines along the grooves. The lines weren't there before." |

---

## 5. Micro-events TME01–TME10

Each micro-event follows the Lowmark micro-event card (Discovery and Memory §8): a place, a visible invitation, one ordinary interaction, an immediate meaning, what it cannot prove. None is required for anything. Flags use the `TME0n_` prefix and are read only by the micro-event itself unless stated. No quest items; rewards are a line, a smile, a cup or a flower. Suggested content ids `thornfell.micro.<slug>`.

### TME01 — The shelter tally

| Field | Spec |
|---|---|
| Trigger | First visit to any highstead longhouse (Nettlehook, Hushfold) after TF-M2 Completed (`TH_SEASON` = snow), at dusk. Enter the hearth volume. |
| What the player sees | The host on a bench by the hearth with the winter tally open on their knee, reading aloud to the room. Children half-listening. Beds chalked on a board behind. |
| Interaction | Listen (stand within 6 m for 15 s). The host reaches the bottom of the page and looks up: two options. |
| Lines | HOST: "Beds, eleven. Wood, to the second ring. Meal for the week, if nobody's greedy. Expected: the Hallin pair, from the fold. Still out: the Brekke lad, gone for the goats." (beat; to the player) "And you, walker. Are you expected, or passing?" · > "Write me expected." → HOST: "Name?" (writes) "{PLAYER}. Expected. Now you've a bed to be late for." · > "Passing." → HOST: "Then pass warm." (writes nothing) · Later, if the Brekke lad comes in during the visit: HOST: "Brekke. In." (ticks it) |
| Persistence | `TME01_TALLIED`. If set, every highstead host addresses the player by name from then on (bible §5.3 rule 4); TMM-D3 and *A Place at Smoke Week* read it. Nothing else changes. |
| Repeatable | The reading loops at every dusk in snow; the choice once. |
| Cannot prove | Anything. A tally counts beds and people; it is not a register of who belongs. |

### TME02 — The lintel tap

| Field | Spec |
|---|---|
| Trigger | Stonewright Quarter doorways (TP01), daytime, any time after arrival in Stonewake. |
| What the player sees | A dwarf mason (role, Kaldren's neighbour) taps the lintel above a door with two knuckles before going in. A child behind him copies it, too low, tapping the door instead. |
| Interaction | **Tap** any Quarter lintel (interaction, 1 s; a short clean ring). Or talk to the neighbour. |
| Lines | NEIGHBOUR: "Safety habit." (beat) "Sound stone rings. Cracked stone clacks. You want to know before it's on your head." · CHILD: (tapping the door) "This one rings." · NEIGHBOUR: "That's wood." · *(if the player taps)* NEIGHBOUR: "There. Now you'll do it forever. Everyone does." |
| Persistence | `TME02_TAPPED`. The player character taps Quarter lintels on entering (idle animation, optional setting). TMM reads it as flavour only (Kel). |
| Repeatable | Always. |
| Cannot prove | Nothing beyond the lintel in front of you. Kaldren is not involved. |

### TME03 — Reverse cups

| Field | Spec |
|---|---|
| Trigger | A Nettlehook longhouse, a mourning meal (a fixed evening after TF-M1; a household has lost an elder to age, not the war). Enter the table volume. |
| What the player sees | A long table; cups passed hand to hand **the wrong way round**, against the usual direction. An empty place at the head with a full cup. |
| Interaction | A cup reaches the player. **Pass it** left or right. |
| Lines | *(passed the usual way)* NEIGHBOUR: (gently, turning the player's hand) "Other way. Tonight it goes back toward him." · *(passed the reverse way)* WIDOW: (a small nod) "Thank you." · Later: CHILD: "Why backwards?" · ELDER: "So it reaches the ones who went before. Drink, don't ask." |
| Persistence | `TME03_PASSED`. None visible. |
| Repeatable | Once. |
| Cannot prove | Any belief about the dead. It is manners. |

### TME04 — The Apprentice Walk

| Field | Spec |
|---|---|
| Trigger | The safe stretch between Nettlehook and Hushfold (MAP VERIFICATION REQUIRED), a fixed morning after TF-M1. Neighbours gather around a young person (role, about twelve) at the stretch's start. |
| What the player sees | Six or seven neighbours, a warden, a host with a basket. The young walker carries a coil of rope too big for them. At the stretch's end, a flat rock with **child-height marks** scratched in a row, old and lichened, and fresh ones beside them. |
| Interaction | **Walk with them** (escort-style; they wait if the player lags; ~2 minutes). At the rock the young walker scratches their own mark. **Read the old marks** (inspect). |
| Lines | WARDEN: "Rope on your shoulder, not your neck." · HOST: "Slow. It's a walk. Not a race to dinner." · YOUNG WALKER: (at the rock) "Everyone puts one?" · NEIGHBOUR: "Everyone who walks it." · Old-marks inspect (first reading): *"A row of marks at child height. Some initials, some just scratches. An old game, probably."* |
| Re-reading | After the player has visited Hushfold's tally hut (TMM S05, *A Place at Smoke Week*, or any talk with Runa there), a new option with RUNA at the hut: > "The marks on the walk rock." → RUNA: (takes down an older book from the shelf, not the first; finds a page) "Here. *'Walk put off. Gate shut all winter. Seven of ours, eight of Nettlehook's.'* The long closure, twelve winters back." (beat) "They grew into the work before the gate opened. Nobody walked them. They went and scratched the rock anyway, the year after. Grown." The rock's inspect text then reads: *"Fifteen marks in a row, all cut in one year, at a height no child reached. A cohort that never walked."* |
| Persistence | `TME04_WALKED`, `TME04_REREAD`. |
| Repeatable | The walk repeats with a different young walker each in-game season; the re-reading once. |
| Cannot prove | Anything about the war. The closure here is a recent rockfall winter (twelve years ago), not a wartime sealing; the roster belongs to TF-M5. It shows only that closures cost people things and that Hushfold wrote it down. |

### TME05 — The Horn That Never Fell

| Field | Spec |
|---|---|
| Trigger | The cliff ledge above the Old Watchfire Line (TP20), any time after TF-M1. Nearby, a small null-point niche in the rock (dust falls straight; footsteps go flat). |
| What the player sees | A shelf on an impossible face across the gap, with something like a horn-shaped shadow on it (never resolved at any zoom). Stories say its call is heard only when no one is listening. |
| Interaction | **Stand still** in the null-point niche with a hand on the rock (interaction "Rest a hand on the rock"; the player must not move for 10 s). Nothing is heard: the niche carries no sound. After 6–10 s the player **feels** a note through the rock: controller rumble in a slow two-pulse shape, the hand prop trembles faintly, and a few grains of grit run out of a crack beside the hand and fall straight down. It stops. Nothing else happens. |
| Lines | None. Rock inspect afterwards: *"Cold rock. Your hand is still tingling."* If asked about it, DORN (at Passwatch): "Felt it? Not heard it?" (beat) "That's how it goes. Leave it be." |
| Persistence | `TME05_FELT`. |
| Repeatable | Always; the feel is randomised between 6 and 10 s. |
| Cannot prove | Anything. **Never explained** (bible §7.4 list). Not a message, not a call from anyone. Accessibility: haptic plus the visible grit fall; no audio by design. (Kept distinct from *Witness at the Gate*'s moving frost.) |

### TME06 — The Stone With No Shadow

| Field | Spec |
|---|---|
| Trigger | Stormwake Plateau (TP19), the dusk window. Keep-watch on a nearby cairn if the player arrives early. |
| What the player sees | A lone boulder. As the sun goes down, every rock on the plateau throws a long shadow eastward of its base; the boulder throws **none**. |
| Interaction | **Wait for dusk; look.** Inspect the boulder's base: tool marks. |
| Lines | Inspect: *"Tool marks low on the sides, very old. It was cut to sit exactly where it sits."* · Later, *"At dusk the light runs along it, not across it."* No NPC explains it. TORVEK (if asked at Stonewake): "Leave stones where they were put." |
| Persistence | `TME06_SEEN`. |
| Repeatable | Every dusk. |
| Cannot prove | Its purpose. **Never explained.** The tool marks show it was placed, not why. |

### TME07 — The Split Ram

| Field | Spec |
|---|---|
| Trigger | A Ridgewall track by Nettlehook, daytime after TF-M1. Three children and a real ram skull on a stick. |
| What the player sees | One child is the ram (skull held in front), one is "the wind" flapping a blanket, one is the narrator. They need a new wind. |
| Interaction | **Play the wind** (take the blanket; a short scripted flap). The ram-child charges the player and "shatters" theatrically into the snow. |
| Lines | NARRATOR: "And the ram said, *I'm stronger than the wind!*" · RAM: "I'm stronger than the wind!" · NARRATOR: "And the wind said..." (looks at the player) > "Nothing. Wind doesn't talk." → NARRATOR: "Correct. And the ram charged it anyway." · > "Whoooo." → RAM: (furious) "That's not how wind *goes*." · then RAM charges; falls; lies still; NARRATOR: "And that's why you go round." RAM: (from the snow) "Can I be the wind next?" |
| Persistence | `TME07_PLAYED`. The children bark "Go round!" at the player on later passes. |
| Repeatable | The game loops; the player's part once. |
| Cannot prove | Nothing. A cautionary tale about stubbornness [CANON myth]. |

### TME08 — Stormflowers

| Field | Spec |
|---|---|
| Trigger | The Oath Cairn Fields (TP15) during a hard-wind window (the fluted-face whistle tells it; fallback: a fixed afternoon window). |
| What the player sees | A slope of closed white buds. The whistle rises a fifth; the gust hits; **the whole field opens at once**, every flower in the same second, and stays open while the wind blows. |
| Interaction | **Watch.** Optionally **pick one** (1 s) and **lay it on a cairn** (item-given to any cairn). |
| Lines | None from the wind. If MAERA is at her wall: *(if a flower is laid)* "Thank you. They only open when it's blowing. That's the point of them." |
| Persistence | `TME08_LAID`. A dry stormflower stays on that cairn (per-player prop). |
| Repeatable | Every hard-wind window; the laying once per cairn. |
| Cannot prove | Any omen. Stormflowers open in strong wind [CANON]; that is all. |

### TME09 — Echo before sound

| Field | Spec |
|---|---|
| Trigger | A Ridgewall ledge Iven names (any talk with Iven after TF-M1 adds "the stepped ledge" to the map as a marker). |
| What the player sees | A narrow ledge in steps down a face. Nothing else. |
| Interaction | **Step** down the ledge. On the third step, the player hears their own footstep **from the next step down**, a breath **before** they take it. Then they take it, and it sounds ordinary. Once per visit. |
| Lines | None during. IVEN (if asked afterward): "Heard it? Which step, what time, which way was the wind?" (writes) "That's all I do with it." |
| Persistence | `TME09_HEARD`. |
| Repeatable | Once per visit. |
| Cannot prove | Anything. **Never explained** (bible §7.4). Iven reports direction and timing only (ledger limit). |

### TME10 — The far bell drill

| Field | Spec |
|---|---|
| Trigger | Below the Red Slope Terraces (TP21), a fixed morning after TF-M1. A highstead crew practising its rockfall bell. |
| What the player sees | A bell on a frame at the terrace edge; a ringer; a warden with a slate listing hollows below. One hollow, down a side gully, is ticked "?" every year. |
| Interaction | Walk down and **stand in the hollow**; the bell rings (scripted). In the hollow, the bell is not heard at all (the gully's shape swallows it; the player sees the ringer's arm moving and hears only wind). **Call the result back**: blow **Lost** (if the player has `TH_CALLS`, as a learned call) or shout (fallback). |
| Lines | WARDEN (on the Lost call): "Lost from the hollow. So the bell's no good there." (beat) "Every year we tick it '?'. Nobody ever went down." · RINGER: "We'll put a second bell on the gully lip." |
| Persistence | `TME10_CALLED`. A second, smaller bell on a post appears at the gully lip (per-player prop); later drills ring both. |
| Repeatable | Drill loops; the call once. |
| Cannot prove | Anything beyond acoustics: it is the shape of the gully. |

---

## 6. Discoveries TDS01–TDS10 (three-layer framework)

Each discovery has a **surface** (what anyone sees), a **reading** (what a careful player learns, and the interaction that earns it) and, where marked, a **withheld** layer that no Thornfell content resolves. Discoveries are optional, set no quest steps and give no rewards beyond understanding. Flags `TDS##_SEEN` (surface seen) and `TDS##_READ` (the reading's interaction completed), e.g. `TDS01_SEEN`, `TDS10_READ`. Suggested ids `thornfell.discovery.<slug>`. Evidence rule applies: none identifies a person or proves a claim.

### TDS01 — The Silent Gorge (TP18, Ridgewall)

| Layer | Content |
|---|---|
| Surface | A ravine where sound dies. Walking in, the wind, then the player's footsteps, then their breath go silent. |
| Reading | **Drop a pebble** (interaction) or watch the dust: it falls **straight down** with no drift, though wind is visibly moving the grass at the rim. Walls show tool-straight runs under the weathering. Inspect: *"The dust falls straight. The walls are too straight in places. Somebody made this quiet."* Teaches TF-M4's null-point tell early; TGM's den uses the same tell. |
| Withheld | **Why the Echohewn needed a quiet place here.** Never explained. |
| Presentation | 2 s staged audio drop on entry (same convention as TGM.8, lighter: UI stays). |
| Links | *Witness at the Gate* uses it; TGM; TF-M4. |

### TDS02 — Spiral stairs (TP17, Echochamber Summit)

| Layer | Content |
|---|---|
| Surface | Carved stairs climbing the Summit that seem to pull air upward. |
| Reading | **Carry a lit torch** up one flight (the stair's wall sconces offer one): the flame leans and gutters in a regular pattern at each turn, strongest at the slots cut in the risers. Inspect a slot: *"A slot in the riser. Air moves through it, upward, always."* Air-channels shape the flow. |
| Withheld | — |
| Access | Lower flights any time after TF-M1; upper flights with TF-M4. |

### TDS03 — Horn-tower grooves (TP22, Old Watchfire Line)

| Layer | Content |
|---|---|
| Surface | Horn towers along the ridge with acoustic grooves cut into their faces. |
| Reading | **Blow any Ordinary Call** at a tower's mouth (requires `TH_CALLS`): the grooves carry it clearly to the next tower, where the player sees dust jump in that tower's mouth. Each tower's grooves are cut for the calls in use. **One tower's grooves are cut for a call nobody uses**: inspect shows a groove pattern of *two long, one held* (the glyph appears greyed). |
| Withheld | — (the unused call is *Witness at the Gate*'s quest; never explained in Thornfell) |
| Links | TWG (unlocks the quest's lead line if TTH Completed). |

### TDS04 — Cairn alignment (TP15, Oath Cairn Fields)

| Layer | Content |
|---|---|
| Surface | Old cairns standing on squared foundations older than the stones on top [CANON]. |
| Reading | **Stand on any two foundations and speak or call**: the voice carries cleanly along the line between them and dies off it. TORVEK, if near: "The old way. You put a stone where the old stone is. Don't ask me why it feels wrong otherwise. It does." Inspect: *"The cairns sit on lines. Sound runs along them."* |
| Withheld | **Whether the alignment ever did anything.** |
| Ledger | Torvek explains nothing and makes no wartime claim. |

### TDS05 — Ridge camp ash pits (TP23, Abandoned Ridge Camp)

| Layer | Content |
|---|---|
| Surface | An abandoned camp: shattered palisade, ash pits. |
| Reading | **Inspect three pits**: fires banked under turf for a slow burn, the way you bank them when you mean to come back by morning. Kit left by each: a pot with a lid on, boots by a fire, a whetstone on a stone. Inspect: *"Banked for a morning. Nobody came back for the boots."* |
| Withheld | **Whose camp, and why they didn't return.** *Whose Colours* uses the camp; this discovery says nothing about the banner. |

### TDS06 — The broken siege engine (TP11, Shatterfall)

| Layer | Content |
|---|---|
| Surface | A siege engine embedded in the gorge wall [CANON]. |
| Reading | **Climb to its frame** (agility trigger; walkable fallback via the ledge ramp) and inspect: the timbers carry Thornfell clan stamps, and the frame is **wedged as a prop** under a shelf, with packing stones knocked in. Inspect: *"Thornfell timber. Somebody turned it into a prop and held a shelf up with it. Before the fall."* |
| Withheld | — |
| Links | TF-M3 context; never evidence for TF-M3's roster (which owns R06). |

### TDS07 — The Ridgewalker (seen from Stormwake)

| Layer | Content |
|---|---|
| Surface | A figure on the highest ridge, in stormlight [CANON myth]. |
| Reading | Seen **only from Stormwake Plateau, only in a great storm** (a storm presentation window; fallback: the first dusk storm after TF-M3 Completed). A tall shape walking the ridge line against lightning-lit cloud. **Approach** (travel toward the ridge): when the player is within ~200 m of the sighting point, the figure is gone and there are no prints. Ridge inspect: *"Wind-scoured rock. No prints. Nothing."* |
| Withheld | **Never explained.** No NPC explains it. IVEN: "Saw it. Which ridge? What hour? Wind from where?" (writes it down; nothing more). TORVEK: "Don't point." HOSTEL GUEST: "Somebody's goat." Each voice reads it differently; none is confirmed. It is not the Horn-Echo, not a resonance figure, and not tied to anything else in this file. |

### TDS08 — The Lost Banner glimpses (Stormwake)

| Layer | Content |
|---|---|
| Surface | A flicker of red colour on a ridge where nothing could stand. |
| Reading | **Look through a gap in the Stormwake cairns** at the right time (after TF-M2, in stormlight): the colour resolves into cloth caught on a crag, shredded, moving with the wind. Inspect from the gap: *"Cloth, not a flag on a pole. Snagged. It's been there a long time."* |
| Withheld | — |
| Links | Leads to TSL (*Stormlight on the Ridge*); sets the TSL lead flag if that package reads it (request). |

### TDS09 — Burned slope regrowth (TP24, Burned Slope)

| Layer | Content |
|---|---|
| Surface | Young stormwood growing through old ash. |
| Reading | **Inspect three young trees**: the wind-side bark is ridged and dense; the lee-side smooth. Bend a sapling (interaction): it springs back hard. Inspect: *"Wind-tested. It's been bending since it was a seed."* The wood the bowyer in *Stormwood* asks for. |
| Withheld | — |
| Links | TST (Woodcutting and Fletching intro). |

### TDS10 — The Gatefall from below (TP09, before TF-M5)

| Layer | Content |
|---|---|
| Surface | The far gate: a narrow cut with stacked stone galleries above it held by timber props. |
| Reading | **Inspect the gallery marker stones from the road** (requires `TH_CALLS`): each is cut with a call-shape glyph the player recognises from the Ordinary Calls' accessibility glyphs, plus a few they don't. **Inspect the props**: most are grey, cracked and spent; **three galleries show fresh pale timber props** among the grey. Inspect: *"Fresh timber. Pale. Cut this autumn. Somebody has propped these three again."* The gatehouse door is barred; its interior is not reachable. |
| Withheld | **The roster** (TF-M5). Nothing here mentions names, the gatehouse wall or the war's sealings. |
| After TF-M5 | The discovery reads the TF-M5 state: the pale props are spent or pulled, and the inspect text changes to *"Three galleries dropped or made safe. Grey props only now."* (Act III owns the final state.) |
| Flags | `TDS10_SEEN` on entering the road view of the cut; `TDS10_READ` when the props inspect has been completed (the three pale galleries seen). **TF-M5 reads `TDS10_READ`** for its "Three pale. Same as from below." bark and marker ticks (Act III updated to read it, 2026-11-03). |
| Links | TF-M5 Beat 2 (gallery glyphs). Foreshadowing only. |

---

## 7. File-level integration summary

| Need | Used by | Owner | Notes / fallback |
|---|---|---|---|
| Keep-watch / time windows | TMM (hall night), TAS (night, dawn), TME01/03/06/08, TDS07/08 | Systems Engineer | Lowmark MQ4 convention; per-player hour, never world time. |
| Wind-window gust hazard | TMM-H1, TAS-H1, TSG climb, TME08 | Gameplay Designer; Audio | Bible §9.5 shared convention. |
| Null-point audio zones | TGM (total), TDS01, TME05 | Audio | One staged-fade volume type; TGM's variant also mutes UI pending TGM-OD1. |
| Strike / tap interactions with ring results | TAS (cramps), TME02, TMM (optional tap) | Audio; Systems Engineer | Three ring sounds plus glyphs. |
| Horn-blowing interaction with scripted Answers | TSG, TME10, TDS03 | Audio; Systems Engineer | Shared with TF-M1/TF-M5 call playback. |
| Channelled segments that persist | TMM (cord run), TAS (repair) | Systems Engineer | Lowmark convention. |
| Carry-state objects | TMM account, TAS cramp bundle (mules), TGM stones, TSG plate crate | Systems Engineer | Return to source on logout. |
| Visual-only telegraph set | TGM | VFX; Gameplay Designer | Reference case for accessibility. |
| Haptic events | TGM, TAS (arch note), TME05 | Audio | Fallback: visual shiver and subtitle. |
| Per-player props | All four quests; TME01/02/08/10 | Systems Engineer | Each package names a host-state or bark fallback. |
| Agility triggers with fallbacks | TMM plank, TAS arch, TGM ledge, TSG traverse, TDS06 | Level design | All have walkable fallbacks. |

## 8. Package review summary

| Check | Result |
|---|---|
| Brief fit (bible §7.2–7.4) | TMM, TAS, TGM, TSG match their slate rows (core verbs, places, unlocks, links). TME01–TME10 and TDS01–TDS10 match the §7.3/§7.4 tables entry for entry, including TME05 felt through rock in a null-point, TME04 re-read through Hushfold's tally, TDS07 unexplained, TDS10's three pale-propped galleries. |
| R13 seed | The sealed "Lowmark work, war years" bundle is on the Stonewright Quarter's war shelf, seen (guaranteed bark) and never opened (no interaction exists). Kaldren is stated not to be its author and does not appear. |
| Three states | No fail or abandon anywhere. Resume hooks named for each quest. TSG's terrace cannot fall on a warden; TGM resets without losing tracking; TAS's night keeps its segments. |
| Evidence rule | Facts come from stone, iron, records (account, dray book, Hushfold tally, gate book, tally stick, weather slate) and testimony. The hall, the arch's note, the silent roar, the ringing plates, the felt horn, the shadowless stone and the Ridgewalker prove and identify nothing. Combat drops nothing. |
| Character ledger | Hadrik: no scars, war or dates; signs only what Speakers sign; hands the decision to the player (TMM-OD1 flagged). Brynjar: absent in person; one optional bark within his canon belief. Ressa: one accountable-warning refusal. Dorn: judges iron and nothing historical. Torvek, Maera, Iven: one-line cameos within limits. Kaldren: mentioned once by Sefa, as not the bundle's author. |
| Splinter tagging | No node names Ingrith, Bersi or Eyvind; no `[SPLINTER]` tags needed. "The hornwright's record" is referenced in TGM-I2 without a name. |
| Emberholt and Remnant | Tessaly's crew are professionals; Thornfell's distrust is given reasons; the papers are assessed only for their immediate safety claim. No Remnant presence, phrase or hint anywhere in the file. |
| FT-03 | No grain route is stated or implied. |
| Magic | Nobody names or performs magic; Tessaly uses a charcoal forge; Kaldren does not explain anything. |
| Quest items | 0. All carried things are carry-state objects. |
| Flags | Quest-local prefixes only (`TMM_`, `TAS_`, `TGM_`, `TSG_`, `TME0n_`, `TDS0n_`); no new `TH_` flags; no posture weights added. |
| New names | Ivra, Kel, Sefa Dunholt, Geir Vellan, Bjarke, Ansa, Yrsa Fellhand, the Hallin fold [NEW]; checked against the repository for collisions. |
| Deviations from the bible | (1) Discovery ids use `TDS##` per the bible's review log, not the file map's `TD##`. (2) TME04's cancelled walk is tied to a postwar rockfall closure ("the long closure, twelve winters back"), not a wartime sealing, so it cannot pre-empt TF-M5's R06 (sealing) payoff. (3) TAS adds braid 9's "two kinds of iron" as an undated visual only (TAS-OD1). |
| **Independent review (2026-11-03)** | 6 findings (1 high, 3 medium, 2 low). High: TF-M5 could not resolve the discovery and tally flags; TDS10 now sets `TDS10_SEEN` (road view) and `TDS10_READ` (props inspected; the flag TF-M5 should read), and TME01's flag is renamed `TME01_TALLIED` to match Act III. Medium: TME05's moving frost in a null-point duplicated TWG; now a grit fall. Medium: TSG's frost lines on plates duplicated the same image; now beaded water that freezes. Medium: minor name Doran sat one letter from Dorn; renamed **Bjarke**. Low: TMM-D3 name-address now reads `TME01_TALLIED` or `TSM_PLAYER_TALLIED`; token unified to `{PLAYER}`. Low: Ranged mentions gated on S01. |
| **Director rulings reconciliation (2026-11-03)** | Applied CDR-1/2/3 (`Caelmor_Director_Rulings_Combat_Ranged_Release.md`). CDR-1: shared rule now "every enemy defeated at 0 HP" (TD-7 superseded). TAS-E1 bandits fight to 0, `TAS-D4` cut (T-4). TGM: 10% lie-down removed; Greymantle dies at 0 HP; `S06_choice`/`TGM_OUTCOME` kept as how the old bear is left (`sleeping` = den sealed as his resting place, `ended` = left to the trappers); TGM-E1 crows no longer scatter. TSG: no 20% yield; foreman's order is a phase-change (second-wind) bark; `S04`/`S05` begin on his defeat; foreman testimony cut (T-4); epilogue and ledge-choice lines no longer depend on surviving brigands. CDR-2: Melee or Ranged in TAS, TGM, TSG. CDR-3: scope guard reworded. TMM, TME01–TME10 and TDS01–TDS10 needed no change. Historical rows above describe earlier states. |
| **CDR-6 solo-completion sweep, 2026-11-14** | TAS.13 and TSG.13 "all present credited" → credit only when the partner's own active step uses it. |
