# Mire of Fallen Banners: Integration Requirements (Technical Handoff)

**Status (2026-11-09): in review** (independent Batch 4 review 2026-11-09, §8). Requirements handoff from Creative Production, written for the Systems Engineer (Sol), the Schema & Content Engineer and the Creative Production Director. This is Batch 4 of the Mire production plan (bible §12). It records **what the authored Mire content needs the runtime, schemas and data to support**. It implements nothing. It does not design schemas, write JSON or specify C#, and it does not alter, extend or claim to alter any authoritative contract, schema or runtime architecture. Field names and ids below are requirement labels. The Schema & Content Engineer owns real names and shapes, and the Systems Engineer owns every runtime contract.

**Audience:** Systems Engineer (runtime; Roadmap Stages 24–30 and the 33.x bindings) and Schema & Content Engineer (31.x, 34.x). The Gameplay Designer, Zones/POI, Audio/UI, Encounters and item/economy passes are named where they own a decision. Nothing here is decided on Sol's behalf.

**Quest lifecycle (authoritative, cited, not restated as new):** quests have exactly three states, **Inactive → Active → Completed**. The contract is `DESIGNS/Systems Design/Stage 15.2 — Quest State & Progression Rules.md` (revision 2026-11-02: `Uninitialized` renamed `Inactive`; `Failed` and `Abandoned` removed; legal transitions `Inactive → Active` and `Active → Completed` only) and `DESIGNS/Systems Design/Stage 27 — Quest Runtime Integration Definition.md` (a quest the player leaves stays Active and resumable). `CODE/Systems/QuestRuntimeSystem.cs` implements the same model. Every Mire package was authored against it: no quest fails, none is abandoned, walking away keeps the quest Active at its persisted step with an authored resume hook, and choices are outcome flags (bible §11 rule 4).

**Director rulings (2026-11-03, binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. CDR-1: every enemy is defeated at 0 HP. CDR-2: ranged is first-class in every fight and never required. CDR-3: the Mire is an internal production milestone of the complete game. CDR-4: standard RPG systems are preferred over bespoke simulation. The runtime consequences across regions are collected for Sol in **`Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`**. That handoff defines one small **quest on-defeat hook** (EV08 renamed `creature.scripted_defeat`) for the three named story exceptions SX-1, SX-2 and SX-3. **The Mire uses none of it.** The bible registers no SX entry (bible §3, "SX proposal: none"), and no Mire step listens for a scripted defeat. Lowmark G20 and M18 are not consumed by any Mire content.

**Open Director decisions the requirements depend on:** MD-3 (first-light crossing, "the grey"), MD-4 (staged drainage, no breath meter), MD-7 (Hollowfoot as enemies; **OPEN**, both options kept) and MD-8 (the Night Count). Rows that change with a ruling carry `[MD-3]`, `[MD-4]`, `[MD-7]` or `[MD-8]`. `[CAUSEWAY]` marks rows tied to the MD-1 cause.

**Sources read (current state, 2026-11-09):** the bible (`Quests/Caelmor_Mire_Narrative_Production_Bible.md`: §1.1, §3, §6, §7, §9, §10, §10.1, §11, §11.1, §11.2); `Caelmor_Mire_Main_Act_I.md` (§A9–A12, §B9–B12), `_Act_II.md` (§A9–A12, §B9–B12), `_Act_III.md` (inputs, §7.1.5, §7.2, §9–§12, §14, §E); the four side-quest files `Caelmor_Mire_Side_Quests_Names_and_Lanterns.md`, `_Cloth_and_Memory.md`, `_Work_and_Skills.md`, `_Settlements_and_Combat.md` (every integration table, the file-level summaries, MME01–MME10 and MDS01–MDS10), **including their independent review fixes of 2026-11-09** (commit e98147e); `Quests/Caelmor_Thornfell_Integration_Requirements.md` (format); `Quests/Caelmor_Lowmark_v1_Integration_Requirements.md` (shared capability ids); the engineering handoff above.

**Companions (Batch 4):** `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md` owns every combat value (creature kits, telegraphs, re-form timers, hazard tuning, its register C-1 to C-12 and issues I-1 to I-24). This file cites it and never restates a combat number as its own. `Zones/Caelmor_Mire_POI_and_Zone_Requirements.md` owns places, the crossing register (§6.2), the Chapel stages (§6.3), the terrain early checks (MT-01 to MT-18) and the architecture requests for Sol (§10). The three files share the canonical register in §5.1.

**Conventions in this file**

| Mark | Meaning |
|---|---|
| **MUST** | The content cannot be complete as authored without it. Each MUST names a fallback unless marked *no fallback*. |
| **SHOULD** | The authored experience degrades without it but stays playable and non-blocking (every package authors a fallback). |
| **COULD** | Polish; the package's fallback is an acceptable complete state. |
| **[DIRECTOR]** | A Director-level item. Collected in §6. |
| **Shared?** | `= LM <id>`: Lowmark already needs it; build once (ids from the Lowmark handoff: G gap rows, EV events, M mechanics). `= TH §x`: Thornfell's handoff already needs it. `ext LM <id>`: Lowmark's capability plus a Mire extension. `MR only`: the Mire needs it and earlier regions do not. |
| **New?** | Only three rows in this file are **new runtime needs**: MI-CH-01 (N-1), MI-LT-01 (N-2) and MI-WL-01 (N-3). Each has a fallback that uses only standard systems. Everything else is a standard system or an existing Lowmark or Thornfell capability. |
| Requirement ids | `MI-<group>-<nn>` (Mire Integration). They cannot collide with bible decisions `MD-n`, discoveries `MDS##`, micro-events `MME##`, POIs `MP##`, the Zones register `MC-n` or terrain checks `MT-nn`, the Enemies `C-n` / `I-n` / `R-n`, or Lowmark and Thornfell ids. |
| Quest codes | Main: **MNS** MR-M1 · **MBR** MR-M2 · **MRC** MR-M3 · **MCS** MR-M4 · **MBL** MR-M5. Side: **MSS MBA MEP** (Names Below) · **MLL MLW MLD** (Lanterns and Tenders) · **MBS MCF** (Cloth and Colour) · **MRS MFT MFH MWS MHG** (Work and Skills file) · **MFW MMR MSG** (Cloth and Memory file) · **MBO MRW MNK MRH** (Settlements and Combat file) · micro-events **MME01–MME10** · discoveries **MDS01–MDS10**. |

Owner key: **SE** Systems Engineer · **SCE** Schema & Content Engineer · **GD** Gameplay Designer · **ZN** Zones/POI package · **AU** audio · **UI** UI · **ART** art/VFX · **NPC** NPC/AI · **ENC** Encounters package · **IT** item/economy pass.

---

## 1. Baseline and how the Mire differs

### 1.1 What exists today

The Mire adds nothing to what exists. The baseline is the Lowmark handoff §1.1: `QuestRuntimeSystem` with quest-level state only, the three-state lifecycle, a thin event vocabulary, the Stage 16.3 rule that an NPC interaction never advances a quest directly, and a click-to-move client on a flat baked NavMesh with no jump and no off-mesh links. Thornfell's handoff adds the sound system, season state and posture; the Mire needs none of those.

### 1.2 What the Mire adds on top of Lowmark and Thornfell

| Theme | Lowmark / Thornfell (already in their handoffs) | Mire difference |
|---|---|---|
| Readable system | Lowmark: water against a marker (M24). Thornfell: sound | **Ground and water** (bible §1.1): stakes, crossings, knots, moss posts, standards, lit and dark ground and silt prints. Every element is a world marker the player looks at. None is a UI mode. |
| Walkable state | Lowmark crossing ride (M38), presentation water | **Channel states** (Running, Slack, Sour) swap walkable segments and stake props per crossing. Smallest form: quest-pinned states (MI-CH-02, standard). Optional upgrade: a per-crossing schedule keyed to the presentation hour (MI-CH-01, **new, N-1**). |
| Time | Per-player keep-watch clock (M04) | Same clock. It also drives channel turns, dusk Wraiths, night gathering and hour-differs gates (MRC asks, Sennic's sittings). The Mire adds four **quest-local presentation weathers**: the grey `[MD-3]`, roof rain, a dry stretch and a storm. |
| Light | Lowmark M32 lantern props; a lit lane blocks AI | **A lit post suppresses a hazard** (Chapel Shades) and **slows Echoes** (MLL). One radius effect off a lit prop (MI-LT-01, **new, N-2**). Fallback: pre-authored lit and dark zones per stage. |
| Environment stages | Lowmark drift-site state | **Chapel water stages**: three discrete nave variants swapped by quest step (MI-WL-01, **N-3**; already the fallback form). MFT reuses the pattern for one flood step. |
| Combat | Lowmark drift disperse and re-form; Thornfell lane re-form; CDR-1 | Same defeat rule. Earth-memory re-forms **by place condition** (drift-site model). The Act III **count** is one encounter metronome that several systems listen to. **No on-defeat hook, no SX.** |
| Water rules | Lowmark: no swimming in its own content | **No swimming, drowning, breath meter, tide simulation or per-tile mud** anywhere (bible §11.1; MD-4). Deep water is a non-walkable edge with a bark (MI-AG-03). |

---

## 2. Requirement register (de-duplicated, grouped by system)

Each requirement appears once. "Consumers" lists every quest and step that depends on it. Where a package only references a shared need, it is a consumer, not a second requirement.

### 2.1 Quest state and step persistence

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-QS-01 | **Ordered steps** with objective text key, sub-counters, completion predicate and kind (required / optional / parallel) | Lowmark step model unchanged; `S00_…` ids scoped to the quest | SCE, SE | All 25 quests. Optional steps: MNS charm, MBL `S01b_pot`, MRC `S04_ask`. Parallel: MCS `S04_vestry` opens at stage 2 inside `S03`; MNS `S03` holds in any order; MRC `S02` four tasks in any order | = LM G01; = TH §2.1 | MUST, *no fallback* |
| MI-QS-02 | **Three-state lifecycle only**; no fail, abandon or reset anywhere | Stage 15.2 / 27 as they stand | SE | All | = LM G04 | MUST (already contracted) |
| MI-QS-03 | **Resume hooks per step range** | Data: quest → (step range, resume NPC or volume, line key). Default: the original offer | SCE | MNS (Ysolde; Edris after `S02`); MBR (Calwen; Mara in `S03`–`S04`); MRC (Ysolde, Rowan's bench, Rowan at morning); MCS (Mabyn roof, gallery post, roof; Ysolde landing then register table after one hour turn); MBL (Ysolde, Bran, Ide, Agna); every side quest names one | = TH §2.1 (ext LM) | MUST |
| MI-QS-04 | **Data-declared activation triggers**, including zone-entry auto-start | MBL activates on entering Sorrowmere or Griefwatch after MR-M4 Completed **and** after the player has left the Blackwater Landing area (per-player event `mbl.closure_start`; Act III `S00`). MRC is Active on `MRC-D1` start. MCS is Active at MRC completion (continuous). MBR is offered on next Sorrowmere entry after MR-M1 | SE | MBL, MRC, MCS, MBR | = LM G05 | MUST |
| MI-QS-05 | **Persisted sub-progress inside a step** | Per-standard lift and fold state (MBR, MBL); per-check matches (MBL `S01`); gap hold segments and arrivals (MBL `S06`); board, post and stage state (MCS); mending tasks (MRC); stake socket state (MNK) | SE | As listed | = LM G26 | MUST |
| MI-QS-06 | **Respawn anchors by step** | Data: quest step → respawn point. MNS by step (§A11 list); MBR causeway head; MRC junction checkpoints during the ride; MCS Mabyn's loft or the gallery post; MBL wakes at Griefwatch's vigil hall with a warden walk back to the last ridge checkpoint | SE, SCE | All main quests; MNK, MRH, MCF | = LM G27 | MUST |
| MI-QS-07 | **Logout restore to a step location and presentation hour** | Restore position by step; re-apply pins (night pin in MBL; morning at the landing for MRC `S05`) | SE | MNS, MBR, MRC, MCS, MBL | = LM G26 | MUST |
| MI-QS-08 | **Quest-start skill requirement on offer** | Standard requirement check on the accept option, with a decline line | SE, SCE | MRS, MFH, MRH (per their packages) | = TH §2.11 | SHOULD. Fallback: the giver's line asks the player to come back; no gate in data |

### 2.2 Region flags and quest-local flags

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-FL-01 | **Character-scoped region flags `MR_*`** (12, bible §9.1 only) | Enum or bool per flag, one writer each (§3.1) | SCE, SE | All | = LM G03 | MUST, *no fallback* |
| MI-FL-02 | **Quest-local flags that survive completion** and are read by other packages | Persist with the character, not with the quest instance (§3.2) | SCE, SE | MNS, MBR, MRC, MCS, MBL and the side quests that read them | = LM G02 | MUST |
| MI-FL-03 | **Counters and stored values in quest-local state** | `MRC_ASKED` 0–3, `MRC_SENNIC` 0–3, `MRC_REFUSED`, `MRC_WRONG_CALLS`, `MCS_STAGE` 0–3, `MCS_WRONG_BOARDS`, `MCS_STAINS_READ`, `MRC_LAST_ASK_HOUR` (stores a presentation hour) | SCE | MRC, MCS | = LM G02 | MUST |
| MI-FL-04 | **Completion reads across packages** | Predicate "quest X Completed" readable by dialogue and placement | SCE | MBL reads MLD, MFT, MBO Completed; §E.10 reads MRS Completed; MR-M2–M5 each require the previous milestone | = LM G02 | MUST |
| MI-FL-05 | **Cross-region reads for variant lines only** | Read-only predicates; never a gate | SCE | `CN_COMPLETE` (MNS, MEP); `thornfell.main.03_echo_of_shatterfall` Completed (MNS); `thornfell.main.05_stonewake` Completed, `TWN_MIRE_HOOK`, `TWN_COMPLETE` (MBA); `TH_STANDING` (MBL, MBS) | = TH §3.2 | SHOULD. Fallback: the variant line is not shown |
| MI-FL-06 | **Discovery booleans** `MDS##_SEEN` / `MDS##_READ` | Persistent per character | SCE | MDS01–MDS10; **`MDS07_READ` is read by MBL `S02`**, and MBL `S02` sets `MDS07_SEEN` and `MDS07_READ` | = TH §3.2 | MUST for MDS07; SHOULD elsewhere |
| MI-FL-07 | **Validation**: every flag read has a writer, every region flag has exactly one writer, no Mire content reads `FC_SEAL_NOTED` (MD-15) | Build-time check | SCE | All | = LM G30 | SHOULD |

### 2.3 Dialogue conditions and effects

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-DG-01 | **Options gated by flags, completion and item possession** | Standard condition set | SCE | All | = LM G08 | MUST |
| MI-DG-02 | **Show evidence** (one need for every "show", "hold board" and "match" in the Mire) | Dialogue options gated on item possession or on an open document page; or use-item-on-NPC. Local counters inside one conversation for the hold board (two strips) | SCE, UI | MNS hold board (`MNS_name_tape`, holds); MBR logs and shard to Ysolde; MBL vigil-book show-match (3); MBO show-evidence gated on inspects; MBA show a document carry-state on a prop with a match id | = LM G08; = TH §2.3 | MUST |
| MI-DG-03 | **Document views** (one paged reader) | Read-in-place documents and item documents: MBR day-books; MCS vestry log (page spread) and four-leaf `MCS_warden_leaves`; MBL vigil book with paged entries; MBA book index by weather run; MEP ferry book; MCF ledger (in place); MMR ration board (in place) | UI | As listed | = LM G28 | MUST. Fallback for MBA's index: a dialogue list of three run headings |
| MI-DG-04 | **Swap-tagged nodes** | Nodes tagged `[CAUSEWAY]`, `[MD-3]`, `[MD-4]`, `[MD-7]`, `[MD-8]` can be swapped as a set if a ruling changes | SCE | All main acts; MLD; MCF | MR only (tag convention) | SHOULD |
| MI-DG-05 | **Address variant** "witness" | NPCs present at MR-M1's readings, and Rootrest and Griefwatch NPCs with `MR_STRANGER_SEAT`, use the variant | SCE | MNS `S01`; MSS | MR only | COULD. Fallback: plain address |
| MI-DG-06 | **Hour-differs gate** | Option available only if the presentation hour differs from a stored value | SE | MRC asks (`MRC_LAST_ASK_HOUR`); Sennic's sittings | ext LM M04 | MUST. Fallback: gate on one keep-watch since the last ask |
| MI-DG-07 | **Captioned positional fragments** | Audio with partial captions | AU, UI | MFW figure | = TH §2.15 | SHOULD |

### 2.4 Channel states and crossings (the Mire's readable system)

This is the one Mire-specific capability group. It is deliberately split so that the **standard form (MI-CH-02) is enough for every quest**, and the schedule (MI-CH-01) only improves free travel.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| **MI-CH-01** | **Per-crossing channel-state schedule** (bible N-1). **New runtime need.** | A per-crossing table of three states (Running, Slack, Sour) keyed to the existing per-player presentation hour, read by the existing world-state variant system. Rows from Zones §6.2 (X01–X15) | SE, ZN | Free travel everywhere; Rowan's Chapel route after MRC `[MD-3]`; MDS01, MDS10; MLD's wonder moment (every crew stake Slack at once) | MR only | **SHOULD.** Fallback: **MI-CH-02 alone**, with the Zones §6.2 free-travel default column as fixed data. Every quest step already pins what it needs |
| **MI-CH-02** | **Quest-pinned channel states** with free-travel defaults | A step sets the state of each crossing it uses, per player, overriding the default for that player only. Pins are step-scoped: they release to the Zones §6.2 default at step end, and quest completion releases all. A state swaps a walkable segment group, the stake's water-line prop and boat availability. Defaults per Zones §6.2 | SE, ZN | MNS `S02`–`S04` (X01–X03); MBR `S03`–`S06` (X01, X02 Slack for the pinning player); MRC `S03`, `S05` (X05); MCS buttress stake; MLD; MNK; MRS; MFH; MWS; MHG; MFW | ext LM M38 / G14 | MUST. *This is the fallback form;* no further fallback |
| MI-CH-03 | **Stake inspect gated on `MR_CHANNELS`** | Inspect text variant by flag and crossing state | SCE | Every stake | = LM G08 | MUST |
| MI-CH-04 | **State-gated interactions** | An interaction or gather node usable only at a given state: MRS reed stand and MHG hatch at Slack; MWS ditch wade (Slack) versus reach (Running); MFH bank at Slack; MCS windlass blocked at Running | SE | As listed | ext LM M02 | MUST. Fallback: quest pin to the needed state at step start |
| MI-CH-05 | **Knot clump props** | Three-state reed clump (one knot, two knots, cut through); inspect gated by `MRC_KNOTS_READ` | ART, SCE | MRC; Chapel route after MRC | MR only (authored data) | MUST |
| MI-CH-06 | **Sequential stake turns triggered by a mover** | Stakes swap to Sour as the MNS cart passes (X03, X02, X01) and to Slack in sequence in MLD | SE | MNS `S04`; MLD | ext LM M44 | MUST. Fallback: swap at step start |
| MI-CH-07 | **Stake and socket matching** | Nine sockets and nine stakes with ids; seat only on matching id and facing; range inspect with line of sight | SE | MNK | MR only (standard interact) | MUST |

### 2.5 Channelled interactions and persistent segments

One capability: the Lowmark kept-progress channel. Interrupted by a hit; segments kept.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-CS-01 | **Channelled segments with kept progress** | Standard channel. Lift 3 (MBR, MBL), lever 3 (MBR chest), heave 2 (MNS dark-line wheel), haul 3 (MRC shoal), prise 3 (MCS crypt lead), gap hold 3 (MBL), relight ~2 s (MCS), bell rope (MBO, night turns only), brazier burn (MCF), seat legs and shaping (MSS) | SE | As listed | = LM M02/M03, G11 | MUST |
| MI-CS-02 | **Interact sequence with harmless reset** | Ordered handles; wrong order resets with a sound. Fold (MBR, MBL: three handles, inactive until both pins are in); sluice windlasses (MCS: B → C → A, read from **water stains**); rick course (MRW); vent arrangements (MSG, lookup table) | SE | As listed | = LM G11; = TH §2.5 | MUST |
| MI-CS-03 | **Skill-checked channel with a crew alternative** | Woodcutting at a block or a world stake; the crew alternative costs one keep-watch turn (MBR pins, MRC mending) or two counts (MBL stakes) | SE, GD | MBR `S02`, MBL `S04`, MRC `S02`, MSS, MFH | = LM G23 | MUST. The crew path is the fallback |
| MI-CS-04 | **Authored-result test stations** (one interaction type) | Returns an authored result per object: roll board (MRS), flex test and pin gauge (MFH), weighing beam (MHG) | SE | MRS, MFH, MHG | = LM G22 (M40) | SHOULD. Fallback: inspect text gives the result |
| MI-CS-05 | **Slowed segments restored by interactions** | Loose-log section slowed until two pins are placed | SE, ZN | MBR | = LM M30 (slow volume) | MUST |
| MI-CS-06 | **Timing window on a looping prop** | Bobbing marks and the flight-net throw share one window keyed to the bob loop | GD | MRS | = LM M41 | SHOULD. Fallback: plain hit on the mark |

### 2.6 Keep-watch clock, pins and quest-local weather

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-CK-01 | **Keep watch at a marked bench** advances the per-player presentation hour (morning, noon, dusk, night); never world time | Lowmark convention | SE | Every crossing bench; MNS, MBR (dusk), MRC (crew mending, sittings, morning), MCS (Slack between boards, vigil to morning), MBL (dusk), all side quests | = LM M04, G15 | MUST |
| MI-CK-02 | **Hour pins per step** | MNS `S04` pins dusk then night; MBR `S05` dusk (re-pinned on return after death or logout) and `S06` night; MBL pins night from the end of `S02` to `S07` and releases to morning; MCS `S03` buttress-stake schedule (morning Slack; Running after Board B until the player keeps watch to dusk; dusk Slack; night Running); MCS `S07` to morning; MCF `S03`–`S05` day (noon). Pins are step-scoped and release at step end; quest completion releases all | SE | MNS, MBR, MBL, MCS, MCF | = LM M04; = TH §2.6 | MUST |
| MI-CK-03 | **Hour-keyed prop variants** | Moss posts lit at dusk and night where tended; night moss gather nodes (MRC, MLL); MEP meal-hour signs; MBO night turns; MNK moss caps at dusk | SE, ART | As listed | = LM G16 | MUST. Fallback for MLL nodes: present at any hour during `S02` |
| MI-CK-04 | **Quest-local presentation weather**, per player, paused when the player leaves the area | The grey (MRC `S05`; fog volume with four densities along the route) `[MD-3]`; roof rain (MLW); dry stretch (MLD); storm, ambience only (MSG) | SE, ART, AU | MRC, MLW, MLD, MSG | = TH §2.6 (storm windows) | MUST for the grey; SHOULD for the others. Fallback: lighting and ambience only. **No timed gust cycle** (removed from MSG in the 2026-11-09 review) |

### 2.7 Carry states

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-CA-01 | **Carry-state objects** (held prop + quest flag; not inventory; cannot be dropped by a hit) | One pattern for: the shard (MBR), the harness (MRC; weapons sheathed), the hand lantern (MCS), the reed-paper rubbing (MCS altar), pins (count), seat legs (MSS), bales (MCF; slowed), crocks with shelf slots (MFT), barrow (MRW; slowed), reed bundle (MRS), vigil pot (MBL), standard pole and folded cloth (MBL), fowl and broth crock (MNS) | SE | As listed | = LM M05, G12; = TH §2.7 | MUST. Fallback for the shard: Mara carries it and the moment triggers on proximity with Mara beside the player |
| MI-CA-02 | **Deposit targets** | Authored slots (shelves, frames, braziers, the register) that accept a carried object | SE | MFT, MCF, MBR, MBL | = LM M05 | MUST |

### 2.8 Per-player props, NPC placement and phasing

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-PP-01 | **Per-player prop state** driven by flags and steps | Lowmark per-player prop pattern; co-op fallback per §2.18 | SE | All | = LM M44, G16 | MUST |
| MI-PP-02 | **Standard prop states** | Seven states per standard: laid, leaning, risen, lifted-unfolded, folded, removed, plus pale-hole roadside variant on `MR_CAUSEWAY = reset` | SE, ART | MNS, MBR, MBL, MBS, MCF, MLD | ext LM M44 | MUST |
| MI-PP-03 | **Register page and record props** | Register page by `MR_NAME_RECORD`; arrivals wall strip by `MR_ARRIVALS`; index-board column (MEP); roster board strips by `MBO_RULE`; vigil book page variants; custody props by `MR_WARDEN_RECORD` (box with or without leaves; Tenders' chest pegged or not) | SE, ART | MNS, MBA, MEP, MBO, MCS | ext LM M44 | MUST |
| MI-PP-04 | **Placement sets from flags** (one need for every flag-driven NPC arrangement) | Per-player NPC placement and barks keyed to flags. MBL circle (up to ~20 NPCs to fixed stone or shoulder marks, bible §9.3); Sorrowmere meal; epilogue placement (§E) | SE, NPC | MBL `S06`, `S08`; epilogue | = TH §2.8 (Assembly placement) | MUST. Fallback: spawn at marks with a fade |
| MI-PP-05 | **Bannerline crown states** | Prop sets by `MR_BANNERLINE` (quieted: turfed ring, footing stone; tended: cut step, keeper on the gap), `MR_BANNERS`, `MR_ROWAN_TRUST` (landing lantern seen below) | SE, ART | MBL epilogue; Night Count | ext LM M44 | MUST |
| MI-PP-06 | **Environment variant swaps by step** (non-water) | MWS root ring (roots / cleared); MWS walkway (straight / dog-leg by `MWS_MARKER`); MSS seat (upright / upturned); MLL straight reflection; MMR print filling | SE, ART | As listed | ext LM G16, M44 (per-player presentation; walkability is a Mire extension for Sol) | SHOULD. Fallback: inspect text |
| MI-PP-07 | **Strange-moment prop sequences** | MBL: ~9–12 standards lean toward a precomputed nearest stone and lie down in order, audio cut on the 12th arrival; MBR `causeway.shard_moss`; MCS glass emissive ~5 s with Shade volumes frozen (presentation) | SE, ART, AU | MBL `S06`; MBR `S04b`; MCS stage 3 | = LM G29 | SHOULD. Fallback: standards lie down without the lean; glass inspect only |

### 2.9 Light: lantern posts and lit radius (bible N-2)

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| **MI-LT-01** | **A lit prop's radius gates a hazard and applies a slow** (bible N-2). **New runtime need.** One radius effect off a lit prop, two uses: (a) Shade spawning suppressed within ~6 m of a lit Chapel post (Enemies §9.2, MC-3); (b) a standard slow on Earthen Echoes within a lit lantern's radius (MLL) | Spawn gating by a prop's lit state; one standard slow applied in the same radius | SE | MCS `S01`–`S06` (MCS-H1, MCS-H2); MLL | **ext LM M32** (lit lane blocks AI) | **SHOULD.** Fallback (a): **pre-authored lit and dark zones flipped at each drainage stage** (Act II §B8.1). Fallback (b): no slow; waves reduced by one (MLL.11) |
| MI-LT-02 | **Lantern post states** | Dark / lit / guttering; light and relight interactions; persisted per player | SE, ART | MNS (moss posts, presentation only), MCS, MLL, MBO (dipper wets a dark post to lit), MNK (moss caps) | = LM M32 | MUST |
| MI-LT-03 | **Hand lantern looks** | Carry-state lantern whose light radius shows one dark-ground timer in three looks (bright, low, ember); a log line on change; resets in a lit radius. No stored light value, no fuel, no bar | SE, ART | MCS | Part of MI-LT-01 | MUST. Under the MI-LT-01 fallback the timer runs only in authored dark zones |
| MI-LT-04 | **Scripted push to the nearest lit post** | At ember, the next press moves the player to the nearest lit post reachable on the walkable route, never across a level change (~2 s stagger, no damage). **Content fallback for Sol (primary design unchanged):** the push may target the last lit post on the player's own level, or the stair head above it | SE | MCS | = TH push-to-safe-side (Enemies R-2) | MUST |
| MI-LT-05 | **The draught** | Scripted wave: each post goes guttering then dark in order, once each; posts relit afterward stay lit; the top post is exempt | SE | MCS `S06` (MCS-H2) | = LM G29 | MUST |

### 2.10 Water stages (bible N-3)

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| **MI-WL-01** | **Staged water level** in the Chapel nave (bible N-3). Listed as a new need; **its smallest form is already standard** | Four environment variants (flooded start, stages 1–3) swapped by `MCS_STAGE`, per player; ~15 s transition presentation over the swap; post-quest state stays at stage 3 (drained, lit) | SE, ART, ZN | MCS; post-quest Chapel | ext LM G16, M44 (per-player presentation; walkability is a Mire extension for Sol) | MUST. *This is the fallback form;* nothing more is needed |
| MI-WL-02 | **Flood variant** at the Fenward step | Two environment variants (dry / water at the step) swapped by quest step | SE, ART | MFT | Same as MI-WL-01 | SHOULD |

### 2.11 Escort, rides and group movement

The cart, the escorts and the boat are **one escort capability** with a ride variant. They are listed together to stop them being built twice.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-ES-01 | **Escort follow** that walks at the player's pace, stops when the player stops, cannot be harmed and **halts on enemy proximity** | Standard escort | SE, NPC | MNS cart (`S04`); MHG old man; MEP gate wait; MLD group follow (run disabled in the causeway volume during `S04`; no pace-matching pause, per the 2026-11-09 review) | = LM M08, G18 | MUST |
| MI-ES-02 | **Boat ride on a fixed spline** with authored stops and dialogue calls; a wrong call plays an authored detour; the ride pauses while an enemy is in reach (same halt rule as MI-ES-01) | Lowmark ferry convention (*Night Ferry*) | SE | MRC practice runs and crossing; the Chapel route after MRC; MCS `S08`; MFH rowing variant (player as rower; no physics) | = LM M26, M38 | MUST. Fallback for the halt: the boat stops at each stretch start and moves on when that stretch's Echoes have each been defeated once. Content fallback for Sol (primary design unchanged): the MRC harness haul may be presented as three channel segments at a fixed bank pad beside the grounded boat, with no walking between posts |
| MI-ES-03 | **Stop-and-heave volume** | A volume that stops the cart and offers a two-segment heave | SE | MNS dark line | = LM M02 | MUST |
| MI-ES-04 | **Non-hostile NPC on a scripted path during a boss transition** | A runner with a talk prompt and an interposition volume; timeout hands him to an ally | SE, NPC | MBL asker beat (sets `MBL_ASKER`) | = LM G29 | SHOULD. Fallback: bark-only beat; `MBL_ASKER = wardens`; the talk option moves to `S06` start |

### 2.12 The count (Bannerline)

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-CT-01 | **Encounter metronome** broadcasting beat 1/2/3 at a configurable interval (1.2 s; 0.9 s in phase 3), active per player from MBL `S02` to `S06`. The count is the encounter's timer: every player who can be struck by a count attack receives its tells (MI-AX-01), whatever their quest state (mechanism: Sol) | An ordinary boss timer exposed to several listeners (AI, decals, audio, captions, rumble). Values: MC-2 / Enemies C-7 | SE, AU | MBL `S02`–`S06`; Night Count `[MD-8]` | MR only, smallest form (Enemies R-12) | MUST. Fallback: each encounter runs its own timer at the same interval, started together |
| MI-CT-02 | **Lane movers** | Patrol-path enemies with four waypoints per lane; advance one waypoint per beat-3 event; telegraphed ground attack on arrival; respawn at the lane head on the next beat 3 (condition re-form) | SE, NPC | MBL | = TH lane re-form; = LM M09 | MUST |
| MI-CT-03 | **Gap hold with step-off** | The kept-progress channel (MI-CS-01), three segments; scripted arrivals advance only while the channel is active | SE | MBL `S06` | = LM M02 | MUST. Fallback: three separate segments with arrivals scripted between them |

### 2.13 Quest items (exactly four)

| Item | Granted | Fate | Shared? |
|---|---|---|---|
| `MNS_name_tape` | MNS `S03` (`MNS-D5` lift) | Removed at `S05`; fate by outcome (Nell keeps it, or it goes back with the woman) | = LM G24 |
| `MBR_unit_logs` | MBR `S04` (chest) | **Never removed.** Readable at any time; possession checked by MRC's offer and MCS's vestry match but **not required** by either. Note for SCE: the item stays in the pack for the rest of the game | = LM G24 |
| `MCS_warden_leaves` | MCS `S05` | Non-droppable four-page document. Leaves the pack at `S07` (altar, tenders) or `S08` (sorrowmere, `MCS-D11.40`); a location-bound readable copy stays at the register room, the crypt box or the Tenders' chest | = LM G24 |
| `MBL_names_roll` | MBL `S01` | Handed to Ysolde at the ring and back (`S06`); laid in the register at `S08` and removed | = LM G24 |

**Side content adds no item.** Everything else is a carry-state object (§2.7), a read-in-place record, or nothing. Tools named functionally (§2.14) are reward items for the item pass, not quest items.

### 2.14 Rewards and economy dependencies

No lump quest XP anywhere (bible §11 rule 6). Skill XP is by action only; weights are Gameplay Designer calls.

| Id | Dependency | Used by | Status | Fallback |
|---|---|---|---|---|
| EM-01 | **Ferryman's pole** (functional name) as a quest reward | MRC (Rowan at the roof if the player mended the boat; the boatwright if the crew did) | Item pass to define; no stats proposed | Cut the item; the line stays |
| EM-02 | **Root-wood pole** (proposal name; was "Ferryman's pole") as a master commission (Woodcutting, root-knee) | MBL §E.10 (Rowan) | Item pass; renamed to separate it from EM-01 (Q-09) | Offer shown without a named item |
| EM-03 | **Tender's hand lantern** | MCS reward (Mabyn's spare) | Item pass | If cut, the lantern is used only inside the Chapel |
| EM-04 | **Fowler's bundle** / fowler's reed bow and quiver | MRS reward; §E.10 commission (Hob) | Item pass; CDR-2 makes this a real ranged loop | Generic arrows |
| EM-05 | **Marshwarden's oilcloth coat** | §E.10 commission (Ide with a leatherworker) | Item pass | — |
| EM-06 | **Fen fowl, reed shafts, root wood, root-knee pins** as materials | MNS, MRS, MRC, MSS, MFH, MBL | Economy pass (MD-11) | Carry-state objects until defined |
| EM-07 | **Cooking recipes**: root and fowl stew, smoked eel, broth, vigil pot, peat-wax (MLW) | MNS, MFT, MBL, MLW | Economy pass | Generic cooking interaction producing a carry-state object |
| EM-08 | **Stations**: Hob's hide bench (`MRS_HOB_BENCH`), Tolley's bench (`MFH_TOLLEY_BENCH`), the Fenward hearth | MRS, MFH, MFT | = LM G22 | Ordinary station in the settlement |
| EM-09 | **Leatherworking repair** of imported leather (no local tanning) | MRC harness, MFH, MBA, MBS | Existing repair interaction (MD-11) | Crew alternative |
| EM-10 | **Small payments** | MNS, MBR, MCS (Ysolde's errand due), MBL (Ide) | Economy tuning | — |
| EM-11 | **Master commission offers** gated on `MR_STANDING` (three offers; open a commission, grant nothing) | MBL §E.10 | = TH aspirational-commission pattern | Offers shown without the variant lines |
| EM-12 | **Loot rules** | Earth-memory drops nothing ever; the General drops ordinary **non-metal** material only (Enemies I-21); the Rust Hart is harvestable per economy | Enemies §12 | — |

### 2.15 Encounters and defeat (CDR-1)

**Combat values are owned by `Enemies/Caelmor_Mire_Encounter_and_Enemy_Requirements.md`** (creature kits, telegraph lengths, re-form timers, hazard tuning, the 25% hazard clamp). This section lists only what the runtime must support.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-EN-01 | **Defeat at 0 HP** for every enemy, human or not, with the ordinary defeat presentation. **No yield, break-off, drive-off, scatter or downed state. No SX; the on-defeat hook is not used.** | Standard defeat | SE | All | = LM (post-CDR), engineering handoff | MUST |
| MI-EN-02 | **Re-form by condition** (one state model for every earth-memory site): a spawn point reads a condition and a re-form trigger (timer, pulse or beat) | Lowmark drift-site model. Sites and triggers: Enemies §10.2 | SE | MNS-E2, MBR (standards, Colour pulse), MRC-E2, MMR, MLL, MBL files and Wraiths | = LM M09, G14 | MUST |
| MI-EN-03 | **Fear-scaled add** (one pattern, two users) | One extra swarm, once per fight, after the pocket timer (MNS-E1 40 s; MWS-E1 30 s) while the frightened NPC is not yet calmed; calming cancels it. A timer and the existing calm event; no fear meter (Enemies C-12) | ENC, SE | MNS-E1, MWS-E1 | = LM G13 | MUST |
| MI-EN-04 | **Boss with phase checkpoints** (100 / 65 / 30%) and a leash: ~5 s with nobody in the arena resets to the top of the phase | Standard boss | SE | MBL-E6; Night Count `[MD-8]` | = LM M35 | MUST |
| MI-EN-04b | **Leash volumes that remove free firing spots** (CDR-2): the Mud-Boss resets if no player has been on the island for ~5 s; a Reedlurker hit from beyond its ~3 m lunge for ~5 s submerges and resets at its spot; snappers stand only in wadeable water. Values: Enemies §5.3, §7.4, C-5, C-8 | Ordinary leash/evade reset; zone placement rule (Zones §0.1, MP21) | SE, ZN | MNK-E3; every Reedlurker pocket | = LM leash/reset | MUST |
| MI-EN-05 | **Invulnerable allies; untargetable non-combatants** | Standard | SE | MBL wardens and arrivals; Fenward and Griefwatch Hollowfoot; Gethin Scarth; the MFW figure; Chapel Shades (no HP, never targetable) | = LM M46 | MUST |
| MI-EN-06 | **Statuses**: slow, root, knockdown, standard poison with antidote, conditional damage reduction, ally attack-speed buff on an interruptible wind-up, push or pull with an edge clamp | Standard statuses (Enemies R-2 to R-8) | SE | Per Enemies §9.4 | = LM / = TH | MUST. **Not needed:** bleed, blind (Enemies I-8) |
| MI-EN-07 | **Hazard clamp**: no hazard can defeat a player above 25% HP (authored tuning requirement, pending Gameplay Designer review) | One clamp parameter | SE | All hazards | = TH C-2 | MUST, value pending Gameplay Designer review |
| MI-EN-08 | **Blank earth-memory frames** (health bar, no name); the General's boss bar shows no name | UI rule | UI | Wraiths, the Colour, Echoes, files, the General | MR only (UI rule) | SHOULD [DIRECTOR item §6] |
| MI-EN-09 | **Fauna flee cue before a spawn** | Ambient does flee 4–6 s before an encounter spawn | ENC | MMR, MME07 | = LM G13 | COULD |
| MI-EN-10 | **Night Count entry** `[MD-8]` | After MR-M5 Completed only: interacting with the muster post at night (player hour) starts a separate encounter instance (MBL-E6 refight), repeatable, without story beats; its defeat never completes MBL `S05`. Whether it may run while a partner's story MBL-E6 is active at the same crown is open for Sol (Q-18) | SE | MBL §E.9 | = LM G05 | SHOULD. If MD-8 is declined, delete the interact |
| MI-EN-11 | **Hollowfoot `[MD-7]`** | Under the recommendation: optional human enemies (MBL-E3) with standard aggro and assist radius; "bright cloth" is flavour only, **no gear-visibility system**. Under the alternative: a non-hostile survivor beat with a ~3 s sit interact | ENC, SE | MBL-E3 only | Standard either way | MUST be swappable as a set |

### 2.16 Agility, multi-level navigation and water edges

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-AG-01 | **Agility triggers with walkable fallbacks** | Optional shortcuts only: Marshfall walkway gap, palisade climbs, plank gaps. Every one has a walkable fallback that is the critical path until triggers exist | SE, ZN | MNS, MBL, MWS, others per Zones | = LM M43, G21 | SHOULD. Fallback: the walkable route |
| MI-AG-02 | **Multi-level NavMesh and interaction-driven ladders** | Stairs or ramps between levels; ladders as "climb down" interactions until off-mesh links exist | SE, ZN | Chapel (roof, bell-loft, gallery, aisle, bays, nave, crypt stair), Hushed Granary, Bran's watchpost, stilt steps, archive loft | = LM G21 | MUST, *no fallback* for the Chapel's multi-level navigation itself (playability audit 2026-11-13: current Unity navigation does not yet demonstrate it). Content fallbacks Sol may accept, primary design unchanged: the Shade push targets the last lit post on the player's own level or the stair head above it (MI-LT-04); in the MCS altar outcome Mabyn waits at G6 instead of following the player down to the crypt; the MBL `S02` furrow inspect is also offered from a ground-level pad at Bran's watchpost, so the platform is presentation only |
| MI-AG-03 | **Deep-water edge stops and knockback lanes** | Deep water is non-walkable at every state; an edge volume stops the player with a bark and no damage. No push, pull or knockback ends in deep water, overboard or off a raised edge (MC-6) | SE, ZN | Everywhere | ext TH push-to-safe-side | MUST |
| MI-AG-04 | **Shallows slow** | Walkable shallows apply the standard slow | SE | Ditches, fords, island shallows | = LM M30 | MUST |

### 2.17 Hunting, gathering and skill interactions

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| MI-SK-01 | **Hunting from a hide** with a "stay still" state | Existing hide | SE | MNS (or Hob's string), MRS, MFW | = LM M41 | MUST. MNS fallback: Hob's string costs one keep-watch turn |
| MI-SK-02 | **Tracking sign** reveals the next sign volume | Hunting tracking inspect | SE | MCF, MRH | = LM M41 | MUST |
| MI-SK-03 | **Scripted fowl waves** on keep watch to dusk in the hide volume | Three spawn waves | GD | MRS | = LM G13 | SHOULD |
| MI-SK-04 | **Patch-seeking boss loop** | Move to the nearest tagged patch, lick, still window; patch decals thick / thin / rust | GD, NPC | MRH | MR only (standard move-to-tag) | MUST |

### 2.18 Co-op rules

**Solo-first (Pillar D).** All state is per player. Partners see presentation driven by their own state where the runtime allows it.

| Id | Rule |
|---|---|
| MI-CO-01 | **Shared enemies, per-player progress.** Partners share enemies, the Colour's pulse and the General. Each partner does their own lift, pin, fold, lever, hold, match and choice. A defeat credits each partner whose own active step consumes it (Lowmark §8.1). An interaction (a sluice board, a post, a gap-hold segment) counts only for the partner who performs it, against that partner's own step. |
| MI-CO-02 | **Per-player choices.** Every choice flag (`MR_*` and quest-local) is stored per partner and drives that partner's own barks, dialogue and epilogue. |
| MI-CO-03 | **Shared mending.** MRC mending and gathering credit everyone present. **Open Director item (2026-11-13 audit):** this, and the matching shared-progress rows in Cloth MMR.10 (stakes), MCF.10 (bales), MSG.10 (vents) and Names MBA.10 (spine), are unruled exceptions to MI-CO-01 (interactions count only for the partner who performs them) and to the "mended it yourself" condition on the ferryman's pole (EM-01). Sennic's sittings are per player; a partner who already heard one sits quietly. |
| MI-CO-04 | **Boss scaling.** Health scales per participant. Close up targets one player's lane at a time in rotation. |
| MI-CO-05 | **Asker beat.** Resolved by whichever partner acts first; each partner's `MBL_ASKER` is set to that result. **Open Director item (2026-11-13 audit):** an unruled exception to MI-CO-02 and MI-CO-06 (one partner's action sets another partner's flag). |
| **MI-CO-06** | **Provisional presentation fallback, pending Director review** [DIRECTOR item §6]. Where the runtime cannot show different props to partners, one shared visual state may be shown. It never decides another player's walkable ground, interaction availability, step, credit or choice: each partner's own quest state decides those, and the host's quest state is never authoritative over another partner's progression. Where a shared state would change navigation or gameplay (channel states, water stages, walkways, the closure gate, standards, the gap stone, crown props, lit-post hazard gating), the conflict and the options are recorded in §5.2 Q-18 for Sol; no networking architecture is chosen here. Each partner's own flags drive barks, dialogue and epilogue. Precedent: Thornfell recorded three fallback styles and recommended "first choice in the shard" (TH TI-CO-06, Q-06); Lowmark §8.1 describes "first player's result shows for all". No region has an approved shard-level rule. |
| MI-CO-07 | **A completed partner** sits on the register-room bench at the other's MR-M1 second reading and is addressed as "witness". |
| MI-CO-08 | **Host departure.** A host leaving is treated as a logout for every partner: each partner restores from their own persisted state by their own step's logout rule. Where a non-host partner's progress persists is a Sol question (untestable until a co-op build exists). |

### 2.19 Accessibility

Every audio-only or timing cue has a visual or haptic equivalent.

| Id | Cue | Equivalent |
|---|---|---|
| MI-AX-01 | The count (three beats) | Ground ripple decal on every beat; body poses on beat 2; optional rumble; optional caption ("one", "two", "three") |
| MI-AX-02 | Shade lean and press | The hand lantern's three looks; edges dim; a log line on each change; subtitle for Mabyn's warning |
| MI-AX-03 | The soundless bell (MRC) | Visual by design: reed-flatten rings, three, ~1 s apart; a caption "[no sound]" during the ~6 s ambience duck |
| MI-AX-04 | Silence moments (MRW chimes, MBL audio cut on the 12th arrival) | Caption "[silence]"; the visual sequence carries the moment |
| MI-AX-05 | The lullaby (`sorrowmere.lullaby`) | Captioned hum and Dunstan's line |
| MI-AX-06 | Reed-ripple and ground tells | Ground-first tells readable at night and in fog (Enemies §3) |
| MI-AX-07 | MSG per-bay singing | Inspect text per bay; dialogue-pick fallback |
| MI-AX-08 | MFW fragments | Partial captions |

---

## 3. Flag register

### 3.1 Region flags `MR_*` (character-scoped; bible §9.1 only)

Twelve flags. Each has exactly one writer. No package invents another `MR_` flag.

| Flag | Values | Set by | Read by |
|---|---|---|---|
| `MR_CHANNELS` | bool | MNS `S02` (`MNS-D3.20`) | Every stake inspect; MRC; MBL presentation |
| `MR_NAME_RECORD` | amended / qualified | MNS `S05` | MBR (Dunstan lines); MBL roll, placement and meal; MWS lines; register page |
| `MR_CAUSEWAY` | unset (raised) / reset | MBR `S06` | Causeway roadside props; MLD; MBS, MCF reads. **Not read by MBL** |
| `MR_BANNERS` | retired / restored | MBR `S06` | MBL (Corra, extra wave, placement, choice lines, epilogue); Griefwatch props; MLD; MBS |
| `MR_ROWAN_TRUST` | told / kept | MRC `S06`; upgraded kept → told by a third ask before MBL is Active (`MRC-L-ROWAN`); never told → kept | MBL placement and meal; post-story Rowan lines; §E.10 variant |
| `MR_WARDEN_RECORD` | sorrowmere / altar / tenders | MCS `S07` | MBL `S01` roll source line and `S06` opening; CV-M1 custody line; custody props |
| `MR_BANNERLINE` | quieted / tended | MBL `S07` | Crown state; Griefwatch lines; Night Count presentation; convergence |
| `MR_STANDING` | bool | MBL `S08` | §E.10 commissions; CV-M1 gate |
| `MR_STRANGER_SEAT` | bool | MSS | "Witness" variants; MBL meal line; R16 chip |
| `MR_ARRIVALS` | named / held | MBA | Arrivals wall strip; R14 chip (CV-M3) |
| `MR_LANTERN_LINE` | bool | MLL | MRC moss crew-alternative bark (`MRC-B2.6`); MCS Mabyn line; MBL placement (the Stillgrave family lights the ring) |
| `MR_CLOTH` | returned / burned | MCF | MBL placement (Calwen lays the cloth) |

### 3.2 Quest-local flags read by other packages (must survive completion)

| Flag | Set by | Read by |
|---|---|---|
| `MNS_HOOK_ASKED` | MNS `S00` (optional; `CN_COMPLETE` or TF-M3 Completed) | MSS opening line; MBA (Ysolde) |
| `MNS_STANDARDS_SEEN` | MNS roadside inspect | MBR `MBR-D2.05` |
| `MNS_FENWARD_VISITED` | MNS `S03` | MBL circle (`MBL-B7.6a`) |
| `MNS_BROTH` = self / hob | MNS `S03` | MFT (Lysa's line, with `self`) |
| `MNS_WRAITH` = fought / waited | MNS `S04` | MBR `MBR-D1.12` |
| `MBR_PINS` = self / crew | MBR `S02` | MLD pinned-post inspect `MLD-I1.02`; pinned-log post inspect |
| `MBR_SHARD_MOMENT` | MBR `S04b` | MCS (optional Mabyn line) |
| `MBR_LOGS_READ` | MBR `MBR-D6` | MRC offer |
| `MBR_CORRA_CORNER` | MBR `S05` | MBL (`MBL-B7.9`, with `restored`); MBS line |
| `MRC_HULL_DONE` / `MRC_HULL_CREW` | MRC `S02` | MCS bark `MCS-B1.4` |
| `MRC_MOSS_DONE` / `MRC_MOSS_CREW` | MRC `S02` | MCS wicks (no difference in play) |
| `MRC_SENNIC` | MRC sittings | MCS lead lines (`MCS-D4.05`, `MCS-B5.1`) |
| `MRC_KNOTS_READ` | MRC `S03` | Chapel-route knot inspects; post-story |
| `MCS_VESTRY_READ` | MCS `S04` | CV-M1 (second custodian) |
| `MCS_TOLD_MABYN_LANTERN` | MCS `MCS-D6.20` or `MCS-D9.20` | MLW opening line |
| `MCS_STAGE` | MCS boards | Post-quest Chapel variant (stays 3) |
| `MBL_ASKER` | MBL `S05` | Hewin's Marshfall epilogue bark (§E.6) |
| `MDS07_SEEN`, `MDS07_READ` | MDS07 discovery, **and** MBL `S02` furrow inspect | MBL `S02` (Bran's line); the discovery does not repeat |

**Other persisted quest-local outcome flags** (read inside their own package and by its epilogue props; listed so SCE persists them with the character): `MSS_RUBBING`, `MSS_SEAT_LEGS`, `MBA_SPINE`, `MEP_HOME`, `MLL_PLACE`, `MLW_KEEPER`, `MLD_ORDER`, `MBS_FATE`, `MCF_LEDGER_READ`, `MFW_TOLD`, `MMR_MAP`, `MSG_LISTENED`, `MRS_HERON`, `MRS_HOB_BENCH`, `MFT_CROCKS`, `MFH_TOLLEY_BENCH`, `MWS_MARKER`, `MHG_KEY`, `MBO_RULE`, `MBO_RANG`, `MRW_TABLE`, `MNK_NINTH`, `MRH_ANTLER`, and `MME##` flags where the packages set them.

### 3.3 Completion and cross-region reads (never gates)

| Read | Where | Effect |
|---|---|---|
| MLD Completed | MBL circle | Oswin at Edris's shoulder `[CAUSEWAY]`; otherwise at the closure gate |
| MFT Completed | MBL `S01` optional pot | Lysa's line |
| MBO Completed | MBL `S00`, `S01` | Ide's roster line; vigil-book column hand |
| MRS Completed | §E.10 | Hob's variant |
| `CN_COMPLETE` (Lowmark) | MNS `S00`; MEP | Optional ask and line |
| `thornfell.main.03_echo_of_shatterfall` Completed | MNS `S00` | Optional ask |
| `thornfell.main.05_stonewake` Completed, `TWN_MIRE_HOOK`, `TWN_COMPLETE` | MBA | Variant lines |
| `TH_STANDING` | MBL `S03` and road stone; MBS (Eskil) | A Ridge Warden pair; one line |
| `FC_SEAL_NOTED` | **Not read** (MD-15) | — |

---

## 4. Server events the Mire adds to the Lowmark vocabulary

Labels are requirement names; SCE owns real names.

| Event | Fired by | Listeners |
|---|---|---|
| `mbl.closure_start` | Entering Sorrowmere or Griefwatch after MR-M4 Completed **and** after leaving the Blackwater Landing area (per player; Act III `S00`) | MBL activation. It cannot fire during `MCS-D11` or the landing scene (§5.2 Q-07, resolved) |
| `sorrowmere.lullaby` | MNS `S04b` | Audio, MNS step |
| `causeway.shard_moss` | MBR `S04b` (carrying the shard past Dunstan) | VFX, MBR step (`S04b_records`) |
| `count_beat(n)` (n = 1, 2, 3) | The count metronome (MI-CT-01) | Files, the General, bearers, gap step-off, decals, captions, rumble |
| `mrc.stillgrave_bell` [label proposed here] | MRC `S05` Stillgrave trigger | VFX rings, ambience duck; sets `MRC_BELL_SEEN` |
| `mcs.glass` [label proposed here] | MCS stage 3 | Glass emissive, Shade freeze; sets `MCS_GLASS_SEEN` |
| `mcs.draught` [label proposed here] | MCS `S05` leaves read | Post gutter wave (MI-LT-05) |
| `channel.state_changed(crossing, state)` [label proposed here] | MI-CH-01 schedule or MI-CH-02 pin | Walkable segments, stake props, boat availability, state-gated interactions |
| `creature.scripted_defeat` | **Not used by the Mire** | — |

---

## 5. Canonical register, conflicts and open questions for Sol

### 5.1 Shared canonical register

**Canonical for implementation; quest packages defer to this register.** The three Batch 4 handoffs state these values in the same words. Zones and Integration number them MC-1 to MC-9; the Enemies file numbers its combat rows C-1 to C-12 and **governs every combat value**. Where a quest package gives a different number, the package value is superseded for implementation; the package text changes when its author next edits it (Enemies §13.3 lists those edits).

| # | Topic | Canonical value | Enemies |
|---|---|---|---|
| MC-1 | Channel states | Three states (Running, Slack, Sour) per crossing, keyed to the presentation hour. Quest pins override for the pinning player. Free-travel defaults per Zones §6.2 [PROPOSAL — DIRECTOR]. Rowan's Chapel route runs at Slack, **morning and noon only** `[MD-3]`. Waiting is always available. | (R-14) |
| MC-2 | The count (Bannerline) | Two soft beats, then the third. **1.2 s per beat** (3.6 s per count); General phase 3 **0.9 s per beat**. Every count attack lands on a third beat and is shown on beat 2 at the latest; in phase 3 **every** count attack is shown on **beat 1**, and the bearer's Plant ring shows from beat 1 everywhere. The count itself never damages. Audio, ground ripple, optional rumble and optional caption carry each beat. Displacement count attacks shown on beat 2 (~1.2 s) sit below C-1's 1.5 s minimum: **C-1 pending GD** (Enemies §14). | C-7, I-7, I-12 |
| MC-3 | Lantern posts and Shades | Lit post radius **~6 m**; hand lantern radius ~3 m. Shades form after **~6 s** in dark ground (draught **~3 s**); a press every **~4 s** (draught **~2 s**) after a ~2 s lean tell; at ember the next press pushes the player to the nearest lit post. **No damage.** Shades have no HP and are never targetable. | §9.2 |
| MC-4 | Banner Wraith re-form | In an encounter, a defeated Wraith re-forms at its standard **~25 s** after defeat with a **~3 s** forming tell **while** the standard is risen or lifted-unfolded; folding ends it; live Wraiths fight on to 0 HP. The Risen Colour's standard pulses every **~30 s** (~3 s tell). Bannerline Wraiths re-form on the next third beat. Outside an encounter, a standard still risen re-forms its Wraiths only when a quest next presents its condition; outside quests, standards are presentation only (Zones §7; pending Gameplay Designer confirmation). | C-3 |
| MC-5 | Earthen Echo re-form | By condition only, never by health. Default spot timer **6 s** (MLL while the ring is unfinished; MMR while `S04` is active and stakes remain); MR-M3 banks **~10 s** while the grey lasts and the boat is in the stretch (boat pacing); Bannerline files at the lane head on the next third beat while the circle is open. Echo swings have no knockback. | C-3, I-6 |
| MC-6 | Water and edges | No swimming, no drowning, no fall deaths. Deep water is non-walkable with an edge stop. Shallows walkable and slowed. No knockback ends in deep water or off a raised edge. | C-2 |
| MC-7 | Defeat | Every enemy defeated at 0 HP (CDR-1); humans (Raiders, Rootshadow, Hollowfoot `[MD-7]`) take the ordinary defeat presentation. **No SX entry; the quest on-defeat hook is not used by the Mire.** | C-3, §8 |
| MC-8 | Ranged | First-class in every fight, never required. No spot the enemy cannot reach: the General's leash excludes the ring (~5 s with nobody in the arena resets to the top of the phase). | C-8 |
| MC-9 | Hazard floor | No Mire hazard can defeat a player above **25% HP** (Enemies C-2, the Thornfell value; authored tuning requirement, pending Gameplay Designer review); the gap step-off costs ~15% max HP, knocks back toward the gap stone and never costs rite progress. | C-2, I-22 |

Telegraph minimums (C-1), the bearer (C-4), Reedlurker kits (C-5), statuses (C-6), earth-memory presentation (C-9), Hollowfoot (C-10), boss framing (C-11) and the fear add (C-12) are Enemies-only rows; this file cites them and adds nothing.

### 5.2 Conflicts between packages and open questions

| # | Issue | Packages | Recommendation / question for Sol |
|---|---|---|---|
| **Q-01** | **Sluice order "by rope bands"** in bible §11.1; the bible's own §6.1 and §13 and Act II read the order from **water stains**. | Bible §11.1; Act II §B8.2 | Water stains. MI-CS-02 is built on stains. **Fixed in bible §11.1 (2026-11-09).** (Zones Z-1) |
| **Q-02** | **Boats ground at Slack** (bible §1.1) vs **Rowan ferries at Slack** (bible §6.1). | Bible; Act II A14.2 | Act II's reconciliation: the narrow cuts go still at Slack and Rowan hauls the dry shoals (MI-ES-02 plus the haul in MI-CS-01). **Fixed in bible §1.1 and §6.1 (2026-11-09).** (Zones Z-2) |
| **Q-03** | **Chapel route schedule.** Act II A10 says Rowan ferries "morning or noon" at Slack, which needs either MI-CH-01 or a fixed default. | Act II; Zones §6.2 X05 | Use the X05 default (Slack morning and noon) as fixed data under the MI-CH-01 fallback. Question: is a fixed per-crossing default table acceptable as data in the world-state variant system, even if the schedule itself is never built? |
| **Q-04** | **MDS07 flags.** Act III §9.1 and §9.2 say MBL `S02` sets `MDS07_SEEN` and `MDS07_READ`; Act III §12's "Batch 3 dependencies" row still asks "whether the `S02` furrow inspect sets `MDS07_READ`", with the fallback "no flag set here". The Settlements file asks Act III to set them. | Act III; Settlements §6–§7 | **Set both** at the furrow inspect (as §9.1 and §9.2 say). Act III §12's row is stale text. |
| **Q-05** | **Fear-scaled add stated twice** (MNS-E1 third swarm at ~40 s; MWS extra wave at 30 s). | Act I; Work | One pattern (MI-EN-03; Enemies C-12). Pocket timers kept. |
| **Q-06** | **Lit radius used twice**: MCS Shade suppression and MLL Echo slow. | Act II; Names | One radius effect off a lit prop (MI-LT-01, ext LM M32). |
| **Q-07** | **`mbl.closure_start` fires on entering Sorrowmere** after MR-M4 Completed. MR-M4 completes at `S08` at the landing and in the register room. | Act III; Act II | **Resolved.** Act III `S00` gates activation on MR-M4 Completed + leaving the Blackwater Landing area + zone entry (ordinary predicate). MI-QS-04, §4 and AT-14 follow it. |
| **Q-08** | **Co-op fallback styles differ**: host state (most packages), "first choice in the instance" (MCS custody), "one partner holds and all present are credited" (MBL gap). | Act II; Act III | **Superseded 2026-11-13 (playability audit):** MI-CO-06 is now a provisional presentation fallback only; it never decides navigation, interaction, credit or completion (MI-CO-06, Q-18). The earlier recommendation read: one rule, MI-CO-06 (host state for shared props), pending Director review [DIRECTOR item §6]. Package wording to change if adopted (owner: act reviewer): Act II §B7 co-op bullet and §B11 co-op row (custody prop follows the host's choice, not the first choice in the instance); Act III §11 co-op row (fallback: the host's gap stone, arrivals and crown props are shown; the host's hold drives the shared arrivals; every partner present is credited per segment). **Wording applied in Act II and Act III on 2026-11-09 as the recommended fallback; revert there if the Director declines MI-CO-06.** The 2026-11-13 audit removed the crediting parts of that wording (credit only from each partner's own step). |
| **Q-09** | **"Ferryman's pole" appears twice**: an MRC reward and a §E.10 master commission. | Act II §A10; Act III §E.10 | **Resolved here:** the commission's proposal name is now **root-wood pole** (EM-02); the MRC reward keeps "ferryman's pole" (EM-01). No id changes. Act III §E.10 and its dialogue Part 8 row need the same name change (act reviewer). |
| **Q-10** | **Bannerline road access before MR-M5** is unstated (MBO uses the gate; MSS's spoon comes from the road edge; MDS06 is at the gate). | Act III; MBO; MSS; MDS06 | Per the packages: the gate is open before MR-M5 (MBO) and shut per player from MBL `S00` to `S03`; bends and crown access before MR-M5 is **open** (Zones Q-3). Recommended: no extra gate; bends and crown presentation only before MBL. Needs only the gate's per-player prop state (MI-PP-01). |
| **Q-11** | **Bran's watchpost path** must not cross the closure gate while the road is shut (MBL `S02`). | Act III §5.2 | **Requirement:** the path leaves from Griefwatch's side of the gate and never passes through it (Zones MT-14; bible §4.2; MAP VERIFICATION REQUIRED). |
| **Q-12** | **`MBR_unit_logs` is never removed** from the pack. | Act I; Act II | Fine as authored; noted so SCE does not expect a removal step. |
| **Q-13** | **Hollowfoot reacting to "bright" cloth** could imply a gear-visibility system. | Act III open decision 5 | Standard aggro and assist radius only (MI-EN-11; Enemies I-19). |
| **Q-14** | **MLD's calm path** ("the swarm stays in the ditch"). | Names MLD | Already resolved in the 2026-11-09 review: ordinary leash and aggro, no settle state. Consistent with CDR-1 (Enemies I-20). Recorded so reviewers do not flag it. |
| **Q-15** | **MR-M3 reed source**: bible says the meres; Act II uses the landing's own reed beds. | Bible §6.1; Act II A14.3 | Landing reed beds (Zones Z-3). **Fixed in bible §6.1 (2026-11-09).** |
| **Q-16** | **Earth-memory first appearances** differ from bible §10 (Reedlurkers and Echoes appear first in side quests). | Bible; side files | Enemies I-3, I-4. No runtime impact; tutorial tells use the first-appearance length. **Fixed in bible §10 (2026-11-09).** |
| **Q-17** | **Bleed and blind** appear in MBO, MFH and MNK as new statuses. | Settlements; Work | Not needed (Enemies I-8). Do not build for the Mire. |
| **Q-18** | **Shared environmental state that affects navigation or gameplay in co-op** (2026-11-13 playability audit; authored walkthrough only, untested). Partners at different steps need different channel states and pins on the causeway (MNS, MBR, MLD), Chapel water stages and lit posts (MCS), standard states (MBR, MBL), crown props and the closure gate (MBL), walkway variants (MWS, MNK stakes) and presentation hours. One player's state must not strand, block or advance the other. | Act I; Act II; Act III; Names; Work; Settlements | **Open for Sol and the Director; provisional; no architecture chosen.** Option families: F1 per-player phased set piece; F2 per-viewer props and walkability; F3 shared presentation that never gates navigation or credit (rules use each player's own state); F4 compatibility gate on entry (same step and state, or the further-ahead partner joins as a helper who makes no progress); F5 defer the stateful step to solo or a same-step partner. Fixed meanwhile in text: in co-op no partner's keep watch or pin advances another partner's hour-gated step; an escort follows its own quest owner; credit only from each partner's own step. Open Gameplay Designer question: how Shades treat a partner without the hand lantern. |

---

## 6. Director-level items

| # | Item | Recommendation |
|---|---|---|
| D-1 | **MD-3** first-light crossing | Content built on the bible's recommendation; **not approved**, pending Director. `[MD-3]` rows: MI-CK-04 (the grey), MI-CH-02 pins on X05, the Chapel route schedule. |
| D-2 | **MD-4** staged drainage, no breath meter | Content built on the bible's recommendation; **not approved**, pending Director. `[MD-4]` rows: MI-WL-01, MI-LT-01 to MI-LT-05. |
| D-3 | **MD-7** Hollowfoot as enemies (**OPEN**) | Both options are standard systems (MI-EN-11). Only MBL-E3 changes. |
| D-4 | **MD-8** the Night Count | MI-EN-10. Delete the interact if declined. |
| D-5 | **Free-travel crossing defaults** (Zones §6.2) | Approve the default column so travel works whether or not MI-CH-01 is built (Zones Q-2). |
| D-6 | **Co-op presentation rule** (MI-CO-06) | **Open.** Provisional presentation fallback only (MI-CO-06); it never decides another partner's navigation, interaction, credit or completion. Navigation-affecting conflicts and options for Sol: Q-18. |
| D-7 | **The General's boss bar shows no name** (MI-EN-08) | Yes (Enemies §14 Q4). |
| D-8 | **Canon promotion** (MD-16) | Nothing here is canon. |

---

## 7. Milestone scope and acceptance tests (CDR-3)

The Mire is **the Mire milestone**, an internal production milestone of the complete game. There is no partial public release, and the first public beta contains the complete planned game. Nothing here is a schedule or a request to build ahead of the Lowmark or Thornfell milestones. Rows marked `= LM` or `= TH` ask only to be built once. Work stays sequential by dependency and roadmap (engineering handoff: Lowmark → Thornfell → Mire → Emberholt).

### 7.1 Build order inside the milestone (dependency order, not a schedule)

1. Shared systems already asked for by Lowmark and Thornfell (steps, flags, keep watch, channels, carry, per-player props, escort and ride, drift-site re-form, boss checkpoints).
2. **MI-CH-02** quest-pinned channel states with fixed defaults. Every main quest runs on this alone.
3. MI-WL-01 Chapel stages and MI-LT-02 to MI-LT-05 with the **pre-authored lit and dark zones** fallback.
4. MI-CT-01 to MI-CT-03 (the count).
5. Upgrades if time allows: MI-CH-01 (schedule), MI-LT-01 (radius gating).

### 7.2 Acceptance tests

| # | Test | Pass condition |
|---|---|---|
| AT-01 | Lifecycle | No Mire quest can enter a fail or abandon state. Walking away from any step and returning plays the authored resume hook at the persisted step. |
| AT-02 | Channel fallback | With MI-CH-01 **not** built, MR-M1 to MR-M5 and every side quest complete; no crossing on a required route is non-walkable for longer than one keep-watch turn. |
| AT-03 | Channel schedule (if built) | A crossing's state matches Zones §6.2 at each presentation hour; a quest pin overrides it for the pinning player only; each player's walkable segments match their own state. |
| AT-04 | Water | No location in the Mire lets the player swim, drown or take fall damage; every deep-water edge stops the player with a bark; no knockback crosses an edge clamp. |
| AT-05 | Chapel stages | `MCS_STAGE` 0–3 each show the right nave variant; logout at any stage restores it; the post-quest Chapel stays at stage 3. |
| AT-06 | Light | Shades never form within a lit post's radius (or inside an authored lit zone under the fallback); the push never sends the player past the nearest lit post; Shades never deal damage. |
| AT-07 | The count | Every count attack is shown on beat 2 or earlier (beat 1 in phase 3) and lands on beat 3; the ripple, caption and rumble fire on every beat with audio muted. **C-1 pending GD:** displacement count attacks told on beat 2 (~1.2 s: file arrival knockdown, Planted Standard knockback, gap step-off) sit below C-1's 1.5 s minimum; the Gameplay Designer chooses between telling them on beat 1 in every phase and recording a C-1 exception for count-carried attacks (Enemies §14). |
| AT-08 | Defeat | Every Mire enemy, including the General, Raiders, Rootshadow and Hollowfoot `[MD-7]`, ends at 0 HP with the ordinary defeat presentation. No Mire step listens for `creature.scripted_defeat`. |
| AT-09 | Ranged parity | Each boss and miniboss can be defeated with melee only and with ranged only; no arena spot lets a ranged player avoid the General or the Mud-Boss (leash tests); no Reedlurker can be fought from beyond its reach without resetting, and every snapper is reachable on foot. |
| AT-10 | Quest items | Exactly four Mire quest items exist; each leaves the pack per §2.13 except `MBR_unit_logs`. |
| AT-11 | Flags | All 12 `MR_` flags have one writer each, except the documented `MR_ROWAN_TRUST` kept → told upgrade (`MRC-L-ROWAN`); every flag in §3.2 persists after its quest completes; `MDS07_READ` set by MBL `S02` suppresses MDS07's repeat. |
| AT-12 | Placement | The MBL circle fills twelve stones for every flag combination; nobody stands in the gap; Griefwatch households fill empty stones. |
| AT-13 | Co-op | Two partners with different `MR_BANNERS`, `MR_WARDEN_RECORD` and `MR_BANNERLINE` values each hear their own lines and see their own epilogue; no partner's walkable ground, interaction or credit depends on another partner's state. |
| AT-14 | Activation | MBL does not activate before MR-M4 is Completed and the player has left the Blackwater Landing area; it never fires during `MCS-D11`. |
| AT-15 | Accessibility | Every cue in §2.19 is readable with audio off. |

---

## 8. Internal review log

| Check | Result |
|---|---|
| Coverage | Every integration table in Act I (A12, B12), Act II (A12, B12), Act III (§12, §7.1.5, §E.9, §E.10) and the four side files (each quest's table and both file-level summaries; MME and MDS rows) is represented once in §2. Duplicates merged: show evidence, document views, channel pins, keep watch, carry, per-player props and placement, the cart, escorts and the boat ride, the fear add, the lit radius, environment variants. |
| New needs | Exactly three, each from bible §11.2 and each with a standard fallback: MI-CH-01 (N-1), MI-LT-01 (N-2), MI-WL-01 (N-3; already in fallback form). The count (MI-CT-01) is an ordinary boss timer listed because several systems read it. |
| Lifecycle | Cites Stage 15.2 (2026-11-02), Stage 27 and `QuestRuntimeSystem.cs`; three states only. |
| Combat | CDR-1 throughout; no SX; on-defeat hook unused and stated so; combat values cited from the Enemies file, not restated. CDR-2 via the leash and ranged parity test. |
| Flags and items | 12 `MR_` flags from bible §9.1, one writer each. Every quest-local flag named in §3.2 was checked to exist in the packages. Exactly four quest items. |
| Side-quest review | Built on the 2026-11-09 review fixes: MSG has no timed gust cycle; MLD uses a standard group follow and a plain leashed swarm; MLL uses a standard hold bar; MLW tending uses keep-watch turns; MMR re-forms on one condition; MFH reads "Defeat the dogs at the racks". |
| Scope and authority | No schema, JSON, C# or contract change; requirement labels only; milestone scope stated (§7). No interregional route, no compass direction, no release wording. |
| **Reconciliation check** | The Enemies file was written concurrently. §5.1 was aligned to its C-1 to C-12 on 2026-11-09, and the Zones file's MC-2, MC-4, MC-5 and MC-9 were updated to match. **If the Enemies file changes before commit, re-check §5.1, §2.15 and Zones §14 together.** |
| Batch 4 zones/integration review, 2026-11-09 | Independent review. **Fixed:** `causeway.shard_moss` listener named the wrong quest (MNS → MBR); activation text (MI-QS-04, §4, Q-07, AT-14) aligned to Act III `S00` (leave the landing area), Q-07 closed; `MR_LANTERN_LINE` readers gained MRC; MI-EN-04b added for the Enemies reach rule and Mud-Boss island leash (ordinary leash, CDR-2), AT-09 extended; MI-CO-01 states shared-prop crediting under the MI-CO-06 fallback; MI-CO-06 marked recommendation pending Director review, with the package wording changes listed at Q-08; EM-02 renamed root-wood pole (proposal name only; Q-09 resolved); Q-10 restated per the packages (crown access open); Q-11 stated as a requirement with MAP VERIFICATION REQUIRED; Q-01, Q-02, Q-15, Q-16 fixed in the bible. **Checked unchanged:** three new needs only, each MUST/SHOULD/COULD with a standard fallback; fear add and lit radius one row each (MI-EN-03, MI-LT-01); no SX or on-defeat hook; 12 `MR_` flags with one writer each against the act and side packages; four quest items; MD-3/MD-4/MD-7/MD-8 tags with the MD-7 swap (MI-EN-11); no release wording. |
| Playability audit fixes, 2026-11-13 | SM-01, SM-04 (C-1 pending GD; no option chosen), SM-05 and SM-06 (content fallbacks for Sol only), SM-08, SM-09, SM-14 (pending GD), SM-16, SM-17, SS-01, SS-04, SS-10, CO-01, CO-02, CO-03, CO-04, CO-06, CO-12, CO-17, CO-18, TD-05, TD-16, TD-19. Authored walkthrough only, nothing tested. MI-CO-06 is a provisional presentation fallback, not an approved rule; Q-18 records co-op shared-state conflicts and Sol option families without choosing one. C-1 (1.5 s) and C-2 (25%) are authored tuning requirements pending Gameplay Designer review. |
| Playability audit fixes review, 2026-11-13 | Independent review of the same-day fixes. MI-CO-03 (shared mending and the matching side-quest shared-progress rows) and MI-CO-05 (asker beat) marked as open Director items that are unruled exceptions to MI-CO-01, MI-CO-02 and MI-CO-06; no rule chosen. Authored walkthrough only; text only; no id, step, flag or geography changed; no Director recommendation promoted. |
