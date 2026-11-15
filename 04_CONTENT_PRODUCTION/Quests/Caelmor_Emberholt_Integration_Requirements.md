# Emberholt Heights: Integration Requirements (Technical Handoff)

**Status (2026-11-15): draft; independently reviewed 2026-11-15 (§8); awaiting Director (§6).** Requirements handoff from Creative Production, written for the Systems Engineer (Sol), the Schema & Content Engineer and the Creative Production Director. This is Batch 4 of the Emberholt production plan (bible §12). It records **what the authored Emberholt content needs the runtime, schemas and data to support**. It implements nothing. It does not design schemas, write JSON or specify C#, and it does not alter, extend or claim to alter any authoritative contract, schema or runtime architecture. Field names and ids below are requirement labels. The Schema & Content Engineer owns real names and shapes, and the Systems Engineer owns every runtime contract. Sol's environment is read-only to this file.

**Audience:** Systems Engineer (runtime) and Schema & Content Engineer (data). The Gameplay Designer, Zones/POI, Audio/UI, Encounters and item/economy passes are named where they own a decision. Nothing here is decided on Sol's behalf.

**Quest lifecycle (authoritative, cited, not restated as new):** quests have exactly three states, **Inactive → Active → Completed**. The contract is `DESIGNS/Systems Design/Stage 15.2 — Quest State & Progression Rules.md` (revision 2026-11-02: `Failed` and `Abandoned` removed) and `DESIGNS/Systems Design/Stage 27 — Quest Runtime Integration Definition.md` (a quest the player leaves stays Active and resumable). `CODE/Systems/QuestRuntimeSystem.cs` implements the same model. Every Emberholt package was authored against it: no quest fails, none is abandoned, walking away keeps the quest Active at its persisted step with an authored resume hook, and choices are outcome flags (bible §11 rule 4).

**Director rulings (binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. CDR-1: every enemy is defeated at 0 HP. CDR-2: ranged is first-class and never required. CDR-3: Emberholt is an internal milestone of the complete game. CDR-4: standard RPG systems over bespoke simulation. CDR-6: every quest is completable solo; a partner is credited only when their own active step consumes the event; shared state is a presentation fallback only. The cross-region runtime consequences are collected in **`Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`**. That handoff defines one small quest on-defeat hook (`creature.scripted_defeat`) for the named story exceptions SX-1 to SX-3. **Emberholt uses none of it.** The bible says "SX proposal: none"; no Emberholt step listens for a scripted defeat.

**Director rulings applied (2026-11-15):** D-E2 (Thalan freed, the only outcome), D-S1 (the Speaker idealist and manipulator; `EH_SPEAKER` stays a player outcome), ED-3 (the initiate is Iven Calder; a fixed string), D-EL (Elyndra a living seer met in EFD and consulted in EH-M5; standard NPC dialogue, no new requirement). **Open Director decisions the requirements depend on:** `[ALLOCATION]` (EH-M1's cause, ED-1), ED-7 (EH-M3 gate), ED-15 (ECC), ED-20 (EH-M2 prerequisite), C14.2 (Red-Lit annex placement). Rows that change with a ruling carry the tag.

**Sources read (current state, 2026-11-15):** the bible (`Quests/Caelmor_Emberholt_Narrative_Production_Bible.md`: §3, §4, §6, §7.4–7.5, §9.1–9.4, §10, §10.1, §11, §11.1, §11.2); `Caelmor_Emberholt_Main_Act_I.md` (EH-M1 to EH-M3: items, place tables, step tables, flag tables, respawn and logout rows, integration tables, §C12), `_Act_II.md` (EH-M4, EH-M5: the same), `_Act_III.md` (EH-M6: §4, §5, §6, §7, §9, §11, §12, §14, §E); the four side-quest files `Caelmor_Emberholt_Side_Quests_Unburnt_and_Names.md`, `_Commons_and_Wards.md`, `_Work_and_Skills.md`, `_Combat_and_Discovery.md` (flag tables, integration tables, file summaries); `Quests/Caelmor_Mire_Integration_Requirements.md` (format and shared ids); `Quests/Caelmor_Mire_Playability_Audit.md` (§1, §4); `UNITY/README.md` (what the playable build does today); the engineering handoff above.

**Companions (Batch 4):** `Enemies/Caelmor_Emberholt_Encounter_and_Enemy_Requirements.md` owns every combat value (creature kits, telegraphs, re-form timers, heat and hazard damage, its register C-1 to C-13, issues I-1 to I-23 and runtime rows R-1 to R-14). This file was aligned to it on 2026-11-15 (§2.18 crosswalk, §5.1, §8) and never states a combat number as its own. `Zones/Caelmor_Emberholt_POI_and_Zone_Requirements.md` owns places, the heat-zone register (Zones §6.1, HZ-01 to HZ-26), the pressure stages (Zones §6.3), the multi-level register (Zones §5A, ML-01 to ML-33), terrain early checks (ET-01 to ET-18) and the architecture requests for Sol (Zones §10). Zones and this file share the canonical register in §5.1 (EK-1 to EK-11), each row citing the Enemies C-id it restates.

**Conventions in this file**

| Mark | Meaning |
|---|---|
| **MUST** | The content cannot be complete as authored without it. Each MUST names a fallback unless marked *no fallback*. A MUST that names no fallback is met by the standard Lowmark, Thornfell or Mire capability in its Shared? column (or the standard system it names) and asks for no new build; *no fallback* is used only where that standard capability is itself the floor (EI-QS-01). |
| **SHOULD** | The authored experience degrades without it but stays playable (every package authors a fallback). |
| **COULD** | Polish; the package's fallback is an acceptable complete state. |
| **[DIRECTOR]** | A Director-level item. Collected in §6. |
| **Shared?** | `= MR <id>`: the Mire handoff already needs it; build once. `= LM <id>`: Lowmark. `ext MR <id>`: the Mire capability plus an Emberholt extension. `EH only`: Emberholt needs it and earlier regions do not. |
| **New?** | Two rows are the bible's **new runtime needs**: EI-HT-01 (heat-state schedule) and EI-PR-01 (staged pressure). Two more are **possible** new needs the packages flagged, each with a fallback that needs nothing new: EI-QS-08 (compound OR prerequisite) and EI-SG-01 (sigil-stone volume reading). Everything else is a standard system or an existing Lowmark, Thornfell or Mire capability. |
| Requirement ids | `EI-<group>-<nn>` (Emberholt Integration), keeping the bible's own EI-HT-01 and EI-PR-01. They cannot collide with bible decisions `ED-n`, POIs `EP##`, micro-events `EME##`, discoveries `EDS##`, the Zones ids (`HZ-`, `ML-`, `ET-`, `EA-`, `EK-`, `EZ-`, `ZQ-`), the economy labels `EHC-`, or Mire `MI-` ids. Conflicts and questions are `EQ-nn`; Director items `EDI-n`; acceptance tests `EAT-nn`. |
| Quest codes | Main: **ECW** EH-M1 · **EEH** EH-M2 · **EGH** EH-M3 · **EAC** EH-M4 · **ESS** EH-M5 · **EGA** EH-M6. Side: **EST ETB EMS ENW EGT** (Unburnt and Names) · **EWA ECN EFC EBL ESR** (Commons and Wards) · **ESK EOM EFS EWQ ESP ESH** (Work and Skills) · **EOP EFD EAD ECC** (Combat and Discovery) · micro-events **EME01–EME10** · discoveries **EDS01–EDS10**. |

Owner key: **SE** Systems Engineer · **SCE** Schema & Content Engineer · **GD** Gameplay Designer · **ZN** Zones/POI package · **AU** audio · **UI** UI · **ART** art/VFX · **NPC** NPC/AI · **ENC** Encounters package · **IT** item/economy pass.

---

## 1. Baseline and how Emberholt differs

### 1.1 What exists today (from `UNITY/README.md`)

Sol's playable build is a single-host composition on Unity 6000.5.5f1: click-to-move on a host NavMesh, Shift sprint, no jump; `QuestRuntimeSystem` with the three-state lifecycle; telegraphed melee, telegraphed environmental damage and collision-validated push; timed channels that moving or taking a hit interrupts; carries; an additive local checkpoint that reloads at the road head without persisting world position; death that restores at a fixed recovery point. The README states that the current flat navigation scene has no multi-level or off-mesh traversal; in the Flood Kitchen the authored loft stairs are unfinished and the dry-slat crates have flat access markers. It lists as remaining work: mobile enemy pursuit, complete NPC lifecycle, escort and inspection walks, authored water-state scheduling, walk-away resume prompts, co-op behaviour, and full PlayerSave and network binding. Floor-visibility presentation exists as an opt-in, presentation-only component that is not wired into the playable scene and is unvalidated.

### 1.2 What Emberholt adds on top of Lowmark, Thornfell and the Mire

| Area | Emberholt need | Reuses |
|---|---|---|
| Readable system | Heat zones with three states, tells, vents, niches, keep watch | The Mire's channel-state model (MI-CH-01, MI-CH-02) with heat in place of water |
| Staged set piece | EH-M6 pressure stages | The Mire's environment-variant swap (MI-WL-01) |
| Vertical space | Far more stairs, ladders, galleries and below-grade spaces than any region so far | The Mire's multi-level row (MI-AG-02), with a full register in Zones §5A |
| Hazard attached to an NPC | Tavi's flare; fused workers' flares (never combatants, ED-2) | Standard hazard volume on a non-targetable NPC |
| Sigil-stone | A held item whose inspect reads nearby doors | Possible new (EI-SG-01) |
| Compound prerequisite | EH-M3: EH-M2 AND (TF-M3 OR MR-M2) | Possible new (EI-QS-08) |

---

## 2. Requirement register (de-duplicated, grouped by system)

Each requirement appears once. "Consumers" lists every quest and step that depends on it.

### 2.1 Quest state and step persistence

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-QS-01 | **Ordered steps** with objective text key, sub-counters, completion predicate and kind (required / optional / parallel) | Lowmark step model unchanged | SCE, SE | All 26 quests | = MR MI-QS-01 | MUST, *no fallback* |
| EI-QS-02 | **Three-state lifecycle only**; no fail, abandon or reset | Stage 15.2 / 27 as they stand | SE | All | = MR MI-QS-02 | MUST (already contracted) |
| EI-QS-03 | **Resume hooks per step range** | Data: quest → (step range, resume NPC or volume, line key) | SCE | Every main quest names its hooks (EGA: Hennet or Yorven at the warming house, a line hand at the stair head); every side quest names one | = MR MI-QS-03 | MUST |
| EI-QS-04 | **Data-declared activation triggers**, including zone-entry auto-offer | ECW auto-offered on entering the Cooling House volume; EEH offered on the next Cooling House entry after ECW; **EGA auto-started (Active at `S00_frost`) on the next Cinderwall entry after ESS Completed; the activation sets `EGA_FROST`** (EQ-04); journal leads for EAC and ESS | SE | ECW, EEH, EGA; side quest unlocks | = MR MI-QS-04 | MUST. Fallback: the giver offers on first talk (Hennet for ECW and EEH; Yorven at the Cooling House door for EGA, with `EGA_FROST` set on that activation) |
| EI-QS-05 | **Persisted sub-progress inside a step** | Per-cock and per-collar state; plates count (`EGA_PLATES` 0–3); collars count (`EGA_COLLARS` 0–4, kept across death: "every collar already shut stays shut"); braziers doused (L3); K5 doors read; splice state; channel segments | SE | ECW S06; EAC S04; ESS S04; EGA S02–S06; EWA; ESR | = MR MI-QS-05 | MUST |
| EI-QS-06 | **Respawn anchors by step** | Data: quest step → respawn point (Zones §6.6). EGA always wakes at the warming house | SE, SCE | All main quests; side quests with combat | = MR MI-QS-06 | MUST. Today's build restores at one fixed point; fallback: the region's Cooling House for every step (walk-back cost only) |
| EI-QS-07 | **Logout restore to a step location, with pins re-applied** | Restore position by step (Act lists); re-apply heat pins, hour pins, `EGA_FROST`, `EGA_STAGE` | SE | All main quests; EMS (carry returns to source) | = MR MI-QS-07 | MUST. Today's build reloads at the road head without position; fallback: restore at the quest's resume hook location |
| **EI-QS-08** | **Compound prerequisite** `[ED-7]`: EH-M3 needs EH-M2 Completed **and** (TF-M3 **or** MR-M2) Completed | Native OR in availability, **or** the fallback: a derived quest-local flag `EGH_GATE_OPEN` set by a world rule when TF-M3 or MR-M2 completes (and checked on entering Emberholt for players who completed one earlier), so the offer is a plain AND | SE, SCE | EGH offer | EH only | MUST. **Possible new need**; fallback needs nothing new |
| EI-QS-09 | **Locked journal entry** naming both alternatives | Journal shows EGH as locked with the text of both alternatives (no hidden gate) | UI, SCE | EGH | ext LM | MUST |
| EI-QS-10 | **Dialogue on a Completed quest writes a region flag** | EMS `S07_mend` (post-completion, `strained` only) sets `EH_UNBURNT = kept` through a dialogue node | SE, SCE | EMS | = LM (dialogue-sets-flag) | SHOULD. Fallback: the mend becomes a final optional step before completion |
| EI-QS-11 | **Quest travel to checkpoints** | EGA line hand offers travel from the stair head to U1, U5, U7 second niche, U8, U10 door niche | SE | EGA | ext MR | COULD. Fallback: walking |
| EI-QS-12 | **Repeatable post-story activity**, once per presentation day | The warden's round (Act III §E.9) | SE, SCE | §E.9 | = MR (repeatable) | COULD. Cut freely (Act III) |

### 2.2 Region flags and quest-local flags

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-FL-01 | **Region flags `EH_*`**, character-scoped, one writer each (§3.1) | Enum and bool flags | SCE | §3.1 | = MR MI-FL-01 | MUST |
| EI-FL-02 | **Quest-local flags survive completion** where another package reads them (§3.2) | Persisted per character | SE | §3.2 | = MR | MUST |
| EI-FL-03 | **Cross-region reads** never gate except `[ED-7]` | Read-only flag access to Lowmark, Thornfell and Mire flags and quest states (§3.3) | SE | §3.3 | = MR | MUST for ED-7; SHOULD otherwise (flavour lines drop) |
| EI-FL-04 | **Derived flag by world rule** | `EGH_GATE_OPEN` (EI-QS-08 fallback); its only writer is that rule | SE | EGH | EH only | MUST if EI-QS-08 has no native OR |

### 2.3 Dialogue conditions and effects

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-DG-01 | Conditions on region, quest-local and cross-region flags | Standard | SCE | All | = LM | MUST |
| EI-DG-02 | **Show evidence**: options gated by held items, carry-states and read flags | Standard | SCE | EEH, EGH, EAC, ESS, EGA, ECC, ENW | = TH | MUST |
| EI-DG-03 | **Reserved strings** `[ALLOCATION]` lines (ED-3, D-E2 and D-S1 ruled 2026-11-15: the initiate's name is the fixed string Iven Calder, and the D-E2 / D-S1 swap lines are resolved, so they no longer need swappable keys) | Content keys that can be swapped or cut without code | SCE | EH-M1 and its readers (`[ALLOCATION]`) | EH only (data only) | MUST |
| EI-DG-04 | **Journal documents** that persist after the quest | The chamber-roll line naming Iven Calder (ED-3, ruled 2026-11-15) copied at EGH S07, with no gloss on its significance; the Speaker's letter (§E.8) | UI | EGH, EGA | = MR | SHOULD |
| EI-DG-05 | **Timed optional line on staying** | EAC `EAC-D11.35` plays if the player stays ~5 s | SE | EAC | ext LM | COULD. Fallback: a dialogue option |

### 2.4 Heat: the readable system (bible §9.2, §11.1)

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| **EI-HT-01** | **Heat-state schedule per zone** (bible §11.2): three states keyed to the presentation hour | Reuse the Mire's per-crossing state table (MI-CH-01) with Zones §6.1 as data | SE, ZN | Ambient zones; §E.3 post-story; §E.9 "the day's schedule" | ext MR MI-CH-01 | SHOULD. **New runtime need.** Fallback (bible): quest-pinned states only, **plus the Zones §6.1 default column as fixed data** for every unpinned zone (EQ-05) |
| EI-HT-02 | **Quest pins per player**, step-scoped | Pin a zone's state for a step; release at step end; completion releases all; logout re-applies by step | SE | ECW, EEH, EGH, EAC, ESS, EGA, EWA, EFD, ESR, ESH, EMS, EAD, EFS (Zones §6.1) | = MR MI-CH-02 | MUST. Fallback: a per-quest environment variant per step (the EI-PR-01 form) |
| EI-HT-03 | **Heat-zone hazard volumes** with periodic damage per state, and **cooling niches** as safe volumes | State swaps the volume's damage (Cool none, Working light, Surging heavy); values from the Enemies file | SE, ENC | Zones §6.1 | = LM (hazard volume) | MUST |
| EI-HT-04 | **Tells as state-driven props** with inspect text gated on `EH_TELLS` | A prop with three visual states bound to its zone | SE, ART | All | EH only (prop states) | MUST. Fallback: inspect text states the heat |
| EI-HT-05 | **Vents**: timed hazards with a ~1.5 s ash-lift telegraph before each exhale | Telegraphed environmental damage on a cycle per zone state (EK-3) | SE, ENC | U2, U3, U5, U7, U8, K2, L4, G6, ESH, EAD | = LM (telegraphed environmental damage) | MUST |
| EI-HT-06 | **Hazard volume attached to a non-targetable NPC** with radius steps | Tavi's flare (three radius steps; the test is morning-pinned); fused workers' flares ended by a containment channel (ED-2; never combat) | SE, NPC | EEH; EGA S01; ETB | EH only (standard volume parented to an NPC) | MUST |
| EI-HT-07 | **Heat follows the room**: an authored state change on a step event | L3 sleep rooms when Serix enters; U8 when the relief turns; G4 by the flarecap | SE | ESS S04; EGA S03; EGH S03 | = MR MI-CH-02 (pin on event) | MUST. Fallback: the pin changes at the start of the next sub-step instead of on the event |
| EI-HT-08 | **Echo overlay** in the Hollow crossing (~1.5 s warning, ~8 s, ~25 s cycle) | Timed presentation hazard per the Enemies file | SE, ENC | EGH S05 | = LM (drift-site model) | MUST. Fallback: the overlay is presentation only and the glass vents (EI-HT-05) carry the crossing's damage |

### 2.5 Staged pressure (bible EI-PR-01)

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| **EI-PR-01** | **Staged pressure in the EH-M6 main**, three stages plus relief states (Zones §6.3) | Environment-variant swap keyed to `EGA_STAGE` and step events, per player. The bible notes this is already the fallback form | SE, ART, ZN | EGA S02–S06 | ext MR MI-WL-01 | MUST. **New runtime need** in name only; the variant swap is its own fallback. If per-player variants are not possible: EI-HT-02 pins on each zone produce the same states |

### 2.6 Channelled interactions, carries and timing

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-CA-01 | **Channels with kept progress** (segments persist after interruption) | Lowmark channel convention | SE | Cocks, collars, splices, seal plate, fall cut, copy, braziers, stone setting, damper | = MR MI-CA-01 | MUST |
| EI-CA-02 | **Channel gated by a vent cycle**: segments run only between exhales | L4 damper latch (two cycles); U8 relief hold (two cycles or wedges) | SE | ESS S04 Option B; EGA S03 | EH only (channel availability by hazard phase) | MUST. Fallback: the channel runs any time and the vent simply damages |
| **EI-CA-03** | **Heat ticks do not interrupt channels** (request to Sol) | Today's build interrupts timed work on a hit. Options for Sol, either acceptable: periodic heat damage is excluded from interruption; or a heat tick pauses the current segment instead of cancelling it (progress kept, EI-CA-01). Enemy hits still interrupt | SE, ZN | U5, U8, U9, U10, L4, EWA, ESR, EGH G4 | EH only | MUST. Standard fallback, needing nothing new: every channel pad in a heat zone stands in or touching a niche volume, so no tick reaches it (Zones §0.1) |
| EI-CA-04 | **Carry-states** with movement limits; logout returns the carry to its source | Ewer, blankets, supper pails, record copy, stage-cock handle, EMS stone (blocks climb, agility and sprint) | SE | ESS, EGA, EMS, others | = MR MI-CA-02 | MUST |

### 2.7 Keep watch, presentation hour and phasing

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-KW-01 | **Keep watch** in a niche or on a bench advances the player's presentation hour and releases "until keep watch" pins | Reuse Lowmark keep watch | SE | ECW S01 (U3); EAC S03 (K4); EGA S06 (dawn); EMS; ETB | = MR MI-KW-01 | MUST. Note: not yet demonstrated in Sol's build (Mire audit TD-09). Fallback: keep watch is a timed channel at the niche or bench that releases the step's "until keep watch" pin |
| EI-KW-02 | **Hour pins per player** | EEH morning test; ESS dusk S01, S05; EGA dusk → night → dawn → morning; EFD dusk; ETB dusk | SE | As listed | = MR | MUST. Fallback: the scene plays at any hour with its hour shown by dressing and barks |
| EI-WV-01 | **Frost variant per player** | Environment variant of Cinderwall W1–W4 and the upper Undercroft keyed to `EGA_FROST`; ended by `cinderwall.thaw_lines` | SE, ART | EGA | ext MR MI-WL-01 | SHOULD. Fallback: barks and a few props only |

### 2.8 Per-player props, NPC placement and epilogue

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-PP-01 | **Props by flag** | Tally board (EME10 by `EGA_BOARD_BALANCED`), plaque chalk (`EH_HOLLOW_TRUTH`, `EH_HALF_NAME`), Half-Name Wall, braziers roped (`EH_HEAT_MAIN = terraces`), Sentinel inert prop, far-door chain, barricades | SE, ART | §E; EGH; EAC; ENW | = MR MI-PP-01 | MUST |
| EI-PP-02 | **NPC placement by flag**: the tally-board crowd (bible §9.3) | Rule list → NPC set at V1 in EGA S08 | SE, NPC | EGA S08 | = MR MI-PP-03 | MUST. The scene always completes; missing NPCs only thin the crowd |
| EI-PP-03 | **Barricades by quest state** | EGH mouth barricade S06–S07; EAC barricade beyond the mouth after | SE | EGH, EAC | = LM | MUST |

### 2.9 The sigil-stone

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| **EI-SG-01** | **Held item reads nearby door volumes** (cold / cool / warm) and its inspect text and seam glow change | Trigger volumes at each K5 door and the chamber door set a quest-local state the item reads | SE, ART | EAC S04–S05 | EH only | SHOULD. **Possible new need.** Fallback (Act II): a per-door inspect, "The stone in your hand is warm/cool/cold", needing nothing new |

### 2.10 Escort, follow and NPC movement

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-ES-01 | **Escort-follow**: NPC at walking pace, stops when the player stops, never targetable, hazard-immune; rejoins at the respawn point after death | Thalan (freed, the only outcome, D-E2 ruled 2026-11-15; R2 → shaft foot only; he never climbs the shaft); Myr (EAD, slow walk); Lenk (ESH, follow down the stair) | SE, NPC | EAC S07; EAD; ESH S04 | = MR MI-ES-01 | MUST. Escort is not yet demonstrated in Sol's build. Fallback: the NPC appears at each stop (presentation) |
| EI-ES-02 | **Non-combatant NPCs going ahead to niches** | EGA crew (Veska, line hands) stop in niches, never targeted, never engaged; Thennek leads the descent; Asera at heat rooms | SE, NPC | EGA S02–S06; EAC S03 | ext MR | SHOULD. Fallback: they are placed at each niche as the player arrives |
| EI-ES-03 | **NPC vertical movement** | Thennek down the shaft ladders, Asera up them, Lenk on the stair | SE, NPC | EAC; ESH | ext MR MI-AG-02 | SHOULD. Fallback: fade and reappear at the next landing or the foot |

### 2.11 Quest items (exactly five)

| Id | Item | Quest | Gained | Removed | Notes |
|---|---|---|---|---|---|
| EI-IT-01 | `EEH_ledger` | EH-M2 | `S05` (academy annex) | `S07`: to Idra (`guild`) or Yorven's strongbox (`evidence`) | Reappears in EH-M6 and CV-M4 from the strongbox (EQ-09) |
| EI-IT-02 | `EGH_roll` | EH-M3 | `S07` (signed out at the Red-Lit annex) | `S08`: Kaevren returns it under seal | The Iven Calder line (ED-3) copied to the journal at `S07` |
| EI-IT-03 | `EAC_sigil_stone` | EH-M4 | `S01` (Dahrin) | `S07` (`EAC-D11.30`) | Read as a held item in `S04`–`S05` (EI-SG-01) |
| EI-IT-04 | `ESS_letters` | EH-M5 | `S03` (letter-case) | `S06`: to Kaevren (`challenged`) or the sealed inquiry (`exposed`) (D-S1, ruled 2026-11-15) | — |
| EI-IT-05 | `EGA_junction_book` | EH-M6 | `S04` (fitter's cabin; read there, required) | `S08`: to the guild strongroom (`guilds`) or the Council's book (`council`) | — |

All five: not droppable, not sellable, removed by quest step (= MR MI-IT-01). Verified: five ids, the same spelling in the bible §9.4 and every act; no side quest uses a quest item. **MUST.**

### 2.12 Rewards and economy dependencies

| Id | Requirement | Minimum viable form | Owner | Consumers | Priority |
|---|---|---|---|---|---|
| EI-EM-01 | No lump quest XP; XP from actions | Standard | GD | All | MUST |
| EI-EM-02 | **Master commissions open offers only** after `EH_STANDING` | Four offers (Act III §E.10); thresholds, materials and steps belong to the economy pass | IT, SCE | §E.10 | SHOULD |
| EI-EM-03 | Small payments and wages `[GD]` | Standard currency grants | GD | EGA §E.9; side quests | SHOULD |
| EI-EM-04 | Legacy materials (ember shards, ashsteel, conduction plates) are **not** catalog items | Economy pass decides | IT | ED-11 | — |

### 2.13 Encounters and defeat (CDR-1)

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-EN-01 | **Every enemy to 0 HP**, ordinary defeat presentation | Standard | SE, ENC | All encounters | = MR MI-EN-01 | MUST |
| EI-EN-02 | **Resonance re-form by condition** | Cinder Wraiths re-form at braziers while a flare lasts (L3) or while a vein surges; the Hollow Revenant per the Enemies file | SE, ENC | ESS S04; EGH S06; EAD | = LM (drift-site model) | MUST |
| EI-EN-03 | **Boss state persists across death** | Draw Sentinel: shut collars stay shut; phases per bible §10.1 | SE, ENC | EGA S06 | = MR | MUST |
| EI-EN-04 | **Leash with reset** | U10 leash ~5 s; no raised firing spot | SE, ENC | EGA S06 | = MR MI-EN-04 | MUST |
| EI-EN-05 | **Non-targetable people in hazards** | Fused workers, Tavi, Serix, crew, Thalan: never targetable, never harmed | SE | EEH, EGA, ESS, EAC | = MR | MUST |
| EI-EN-06 | **No on-defeat hook** | Not used; no SX | — | — | — | — |
| EI-EN-07 | **Post-story: no refight** | Sentinel inert prop; nothing re-forms or drops | SE | §E.3 | — | MUST |
| EI-EN-08 | **Boss scaling from a solo baseline** | Tuned and tested solo; scales up per participant | GD, ENC | Draw Sentinel, Hollow Revenant, Old Plate, Saboteur Captain | = MR MI-CO-04 | MUST |

### 2.14 Agility, multi-level navigation and edges

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| EI-AG-01 | Agility triggers with walkable fallbacks | Fallback is the critical path | SE | U2, G6, ESS duct, EWA, EFS | = MR | COULD |
| **EI-AG-02** | **Multi-level navigation**: stairs, ladders, hatches, galleries, below-grade spaces | Per Zones §5A row, Sol's choice of multi-level NavMesh, an interaction-driven ladder, or a zone transition into a flat interior | SE | Zones §5A (37 rows, ML-01 to ML-36 plus ML-05b; 13 required rows that assume a ladder, stair or stacked space; 7 raised enemy positions) | ext MR MI-AG-02 | **MUST.** Every row now has a fallback. **ML-09** (EH-M4 shaft): flat landings joined by a per-flight climb interaction that places the player at the next landing's anchor, using only EI-QS-06 placement. **ML-17** (EH-M5 damper, melee-only path): the latch pulled from the floor at the ladder foot with the fire hook, same channel and time cost. Raised enemy positions: at grade at their foot with the package's cover |
| EI-AG-03 | **Edge stops and push validation**: no push across a level change, into a slag pool, onto a primed plate, into a glass vent or a Surging zone away from a niche | Edge volumes with a bark; push target validation with edge tags on slag pools and plates (Enemies R-2) | SE, ZN | All arenas | = MR MI-AG-03 | MUST |

### 2.15 Skills and skill hooks

| Id | Requirement | Minimum viable form | Owner | Consumers | Priority |
|---|---|---|---|---|---|
| EI-SK-01 | **Smithing at fixed forges** | Cooling House yard forge, U8 field forge, R2 fitter's hearth, gate yard forge, Emberforges | SE | ECW, EAC (frame work, flag only), EGA S03, ESK, EOM, ESR | MUST |
| EI-SK-02 | **Ranged as an optional hook with a time-cost alternative** | ESS damper (shoot ~12 paces, or climb); GD sets the level | GD | ESS S04 | MUST (CDR-2) |
| EI-SK-03 | Mining, Leatherworking, Cooking, Fletching intros | Standard gathering and crafting | SE, IT | EFS, EST, ESH, EWQ, EGA S01 | SHOULD |
| EI-SK-04 | **Quest-start skill requirements** where a side quest names one | Standard requirement check with a decline line | SE, SCE | Per side package | SHOULD. Fallback: the giver asks the player to come back |

### 2.18 Encounter runtime rows from the Enemies file (crosswalk)

The Enemies file (§15) lists fourteen runtime rows and adds no new need. Each maps to a row here or is a standard combat capability owned there.

| Enemies row | Need | Here | Status |
|---|---|---|---|
| R-1 | Re-form by condition with a cap | EI-EN-02 | Standard (Lowmark drift-site model) |
| R-2 | Push or pull one step, clamped at slag pools and primed plates | EI-AG-03 | Standard |
| R-3 | Knockdown and stagger | Enemies-owned | Standard |
| R-4 | Ground damage volumes (patches, wallow ring) | Enemies-owned | Standard |
| R-5 | Conditional damage reduction (Draw Sentinel open collars) | EI-EN-03 | Standard |
| R-6 | Phase gate (Draw Sentinel 65% while a collar is open) | EI-EN-03 | Standard |
| R-7 | Health-triggered encounter events | Enemies-owned | Standard |
| R-8 | Interruptible wind-up | Enemies-owned | Standard |
| R-9 | Heat hazard volumes, niches, timed vents | EI-HT-03, EI-HT-05 | Standard |
| R-10 | Hazard clamp (25%, pending GD) | EI-HT-03, EK-6 | Standard |
| R-11 | Step-triggered state hazards (plates) and sequenced line hazards | EI-HT-05 | Standard |
| R-12 | Non-targetable people; containment hazard round an NPC | EI-HT-06, EI-EN-05 | Standard |
| R-13 | Heat-state schedule | **EI-HT-01** | Bible new need; fallback in use |
| R-14 | Staged pressure | **EI-PR-01** | Bible need; fallback form |

Also from the Enemies file: the 5-hostile set-piece cap (C-12, EI-EN-09 below), frame names by family (C-8), and its avoided list (no meter, stamina, stealth, cold damage, burn or blind status, falls, downed state or co-op-only mechanic), which this file adopts unchanged.

| Id | Requirement | Minimum viable form | Owner | Consumers | Priority |
|---|---|---|---|---|---|
| EI-EN-09 | **Set-piece cap**: no more than 5 hostiles standing at once; re-forms and add-spawns fill only to the cap | Spawn cap per encounter | SE, ENC | Every set piece | MUST |

### 2.16 Co-op rules (CDR-6)

**Solo-first.** Every Emberholt quest is completable by one player. Co-op is optional assistance. No rule below is a prerequisite of solo completion, and none asks for a runtime capability solo play does not already need.

| Id | Rule |
|---|---|
| EI-CO-01 | **Shared enemies, per-player progress.** Partners share enemies and bosses. A defeat credits each partner whose own active step consumes it. Every cock, collar, splice, plate, door reading, brazier, damper, relief choice and custodian choice counts only for the partner who performs it. |
| EI-CO-02 | **Per-player choices.** Every `EH_*` and quest-local choice is stored per partner and drives that partner's barks, dialogue and epilogue. |
| EI-CO-03 | **Per-player heat and stages.** Heat pins, hour pins, `EGA_FROST` and `EGA_STAGE` are per player (Act III). A partner's keep watch, pin or stage never advances or changes another partner's step. |
| EI-CO-04 | **Escort follows its own quest owner** (Thalan, Myr, Lenk). |
| EI-CO-05 | **Host departure** is a logout for every partner; each restores from their own persisted step. A partner who leaves never blocks the other. |
| **EI-CO-06** | **Presentation fallback only** (the Mire's MI-CO-06 pattern, CDR-6). Where the runtime cannot show different heat states, variants or props to partners, one shared visual state may be shown. It never decides another player's walkable ground, hazard damage, interaction availability, step, credit or choice. Shared-world presentation questions are listed for Sol only in §5.2 EQ-12; no networking architecture is chosen here. |

### 2.17 Accessibility

| Id | Requirement | Owner | Priority |
|---|---|---|---|
| EI-AX-01 | Tell states are distinguishable by shape and pattern (the bible's "crazed" red), by audio and by inspect text, not by hue alone | ART, AU, UI | MUST |
| EI-AX-02 | Every vent and plate telegraph has an audio cue and an optional caption | AU, UI | MUST |
| EI-AX-03 | Flare, glow and Echo effects respect a reduced-flash setting | ART | SHOULD |
| EI-AX-04 | `ems.silence` (a 3 s full mute) has a caption ("Silence.") | AU, UI | SHOULD |

---

## 3. Flag register

### 3.1 Region flags `EH_*` (character-scoped; bible §9.1 only; verified against every package)

| Flag | Values | Sole writer (step) | Readers | Verified |
|---|---|---|---|---|
| `EH_TELLS` | bool | EH-M1 (`ECW-D2.20`, S01) | Every tell inspect; side quests | Yes |
| `EH_COLD_WARD` `[ALLOCATION]` | posted / settled | EH-M1 S07 | EWA, EFC; EH-M6 tally board | Yes |
| `EH_CURRICULUM` | guild / evidence | EH-M2 S07 | ETB; EFC; ESS L2 notice; EH-M6; CV-M4 | Yes |
| `EH_HOLLOW_TRUTH` | told / kept | EH-M3 S08 | Memorial props; ENW; EFC; EDS09; EH-M6; CV-M1 | Yes |
| `EH_THALAN` (D-E2, ruled 2026-11-15) | freed (one value) | EH-M4 S06 | ETB; EH-M6 board; §E.7; CV-M4 (none branches) | Yes |
| `EH_SPEAKER` (D-S1, ruled 2026-11-15) | challenged / exposed | EH-M5 S06 | Terrace barks; EGT barks; EH-M6 letter; CV-M4 | Yes |
| `EH_HEAT_MAIN` | terraces / ward / forges | EH-M6 S03 (relief wheel) | EH-M6 S07, S08; §E; barks | Yes |
| `EH_ACCOUNT` | guilds / council | EH-M6 S08 | §E.2, §E.5; CV-M1 | Yes |
| `EH_STANDING` | bool | EH-M6 (completion) | Master commissions; §E.9; CV-M1 gate | Yes |
| `EH_UNBURNT` | kept / strained | EMS (the stone beat, `EMS-D5.20`; and `S07_mend` after completion, strained → kept) | Volkhari lines; EH-M6 board | Yes; one writer, two nodes (EQ-07) |
| `EH_GUILDS` | reformed / restored | EOM | Forge barks; EH-M6 bleed lines; §E.5 | Yes |
| `EH_COMMONS` | bool | EFC | EH-M6 S01 (warming house) | Yes |
| `EH_HALF_NAME` | named / held | ENW | Memorial props; EDS09 variant; CV-M1 | Yes |
| `EH_RIVERGLASS` | reported / held | ECC S07 | CV-M2 (request only) | Yes |

Fourteen flags, fourteen writers, no second writer found. No package writes an `EH_*` flag outside this list.

### 3.2 Quest-local flags read by other packages (must survive completion)

| Flag | Writer | Read by |
|---|---|---|
| `ECW_SHORTFALL_SEEN` | ECW S03 | EWA; EGA S08 |
| `ECW_SEAT_RING` (self / crew) | ECW S05 | ESK; ESR |
| `EDS09_SEEN` | EDS09 inspect | ENW |
| `EEH_MENDING_BOOK` | EEH | EST |
| `EEH_CLASS_DONE` | EEH | ETB |
| `EEH_LENS_READ` | EEH | ETB |
| `EEH_MITTS` (self / maeryn) | EEH S02 | ESH |
| `EEH_TAVI_LAUGHED` | EEH (`EEH-D6.41`) | EME09 |
| `EEH_LEDGER_READ` | EEH S05 | ESS S04 (optional `ESS_STUDENTS_SEEN`) |
| `EGH_FLARECAP` | EGH S02 | EAC K2 bark; EFS |
| `EGH_STONE_HEARD` | EGH S07 | EMS |
| `EGH_SHEET_READ` | EGH S07 | ENW |
| `EAC_BREATH` (asera / waited) | EAC S03 | ETB |
| `EAC_MAERYN_SAID` | EAC S07 (optional) | EST; ETB |
| `EAC_PLATE_READ` | EAC S03 | EGA (Veska's line) |
| `ESS_SLIP_SEEN`, `ESS_ACCESS_READ`, `ESS_RECORD_READ`, `ESS_SERIX_HEARD` | ESS | EGT; EMS |
| `ESS_RAT_PAID` | ESS S03 | EGA S02 (Rat's grille) |
| `EGA_BOARD_BALANCED` | EGA S08 (`EGA-I28`) | EME10 balanced state |

Deliberately read by none: `ECW_SOB_HEARD`, `EEH_LANTERNS_SEEN`, `EAC_EMBERLIGHT_SEEN`, `EST_COLD_BREATH`, `EMS_SILENCE`, `EGT_MURMUR_HEARD` (packages say so).

**Quest-local flags by quest** (persist while Active; the packages list them in full): ECW_* (GALLERY, BROADSHEET_SEEN, SOB_HEARD, ORDER_READ, STUB_SEEN, PAGE_RECOVERED, SHORTFALL_SEEN, COUNTERSIGNED, SEAT_RING, RAT_SEEN); EEH_* (CLASS_DONE, MITTS, MENDING_BOOK, LANTERNS_SEEN, TAVI_LAUGHED, LENS_READ, LEDGER_READ, TAVI_STRUCK, THERYN_HEARD); EGH_* (nineteen, plus the derived `EGH_GATE_OPEN`); EAC_* (seventeen); ESS_* (seventeen, including `ESS_DAMPER` shot / climbed); EGA_* (FROST, SUPPER, BLANKETS, FUSED_STEADIED, STAGE, RAT_GRILLE, BLEED_WORK, PLATES, BOOK_READ, HAND_MATCHED, DOORS_READ, COLLARS, DRAW_SHUT, THAW_SEEN, BOARD_BALANCED, LETTER_READ); side quests per their files.

### 3.3 Cross-region reads (never gate, except ED-7)

| Read | Owner | Reader | Use |
|---|---|---|---|
| TF-M3 Completed **or** MR-M2 Completed | Thornfell, Mire | EGH offer | **Gate** `[ED-7]` (EI-QS-08) |
| `TAS_ACCOUNT` = named | Thornfell TAS | EGA board (bible §9.3 item 7); ESR optional visit | Flavour |
| `MDS09_READ` | Mire MDS09 | ENW `ENW-D6.30` | Optional unconfirmed echo `[ED-16]` |
| `UL_LEDGER_GIVEN` / `UL_LEDGER_TAKEN` | Lowmark UL | ECC `ECC-D4.20` | Flavour |
| `HS_SALVAGE_KEEPERS` / `HS_SALVAGE_REFUSED` | Lowmark HS | ESK `ESK-D2.20` | Flavour |
| (written) `EH_STANDING` with `LR_STANDING`, `MR_STANDING` | — | CV-M1 gate (outside Emberholt) | Not read by Emberholt |

No Lowmark content is ever required (bible §11 rule 12).

---

## 4. Events

### 4.1 Presentation events named by the packages (client-side, per player)

| Event | Quest | What it does |
|---|---|---|
| `cinderwall.hood_flare` | ECW | A hood tell flares red briefly (presentation) |
| `cinderwall.pipe_sob` | ECW | A pipe sound in the ward |
| `cinderwall.rat_glimpse` | ECW | A Cinder Rat seen at a grate |
| `stair.row_lit` | EEH | Lantern row lights on the stair |
| `stair.lanterns_dim` | EEH | Lanterns dim |
| `cinderweave.grey_visitor` | EEH | A Covenant-grey visitor seen near Maeryn's |
| `hollow.echo` | EGH | Embermind Echo overlay cycle |
| `hollow.handprint` | EGH | The handprint at the door arch |
| `warrens.emberlight` | EAC | Emberlight moves along R3's rim |
| `cinderweave.stove_flare` | EAC | Dahrin's stove flares |
| `ess.breath_carried` | ESS | The crowd's breath carries |
| `cinderwall.thaw_lines` | EGA S07 | Thaw lines across the ward at dawn; ends the frost variant for the player |
| `est.cold_breath` | EST | Breath-fog on three characters |
| `ems.silence` | EMS | 3 s full ambient mute in one volume |
| `egt.sleeper` | EGT | A one-shot bark on a sleeping ambient NPC |

### 4.2 Server events Emberholt asks for [labels proposed here]

| Event | Source | Consumers |
|---|---|---|
| `heat.state_changed(zone, state)` | EI-HT-01 schedule or EI-HT-02 pin | Hazard volumes, vent timings, tell props, channel availability (EI-CA-02) |
| `pressure.stage_changed(stage)` | EI-PR-01 | Variant swap; respawn checkpoint |
| `quest.availability_changed(EGH)` | EI-QS-08 or its derived flag | Journal locked entry |
| `sigil.door_state(door, reading)` | EI-SG-01 | Held-item inspect and glow |

No `creature.scripted_defeat` is listened for.

---

## 5. Canonical register, conflicts and open questions for Sol

### 5.1 Shared canonical register

Stated in the same words in Zones §14. The Enemies file governs every combat value; each row cites the Enemies C-id or issue it restates, and "Zones adds" marks a placement rule layered on top.

| Id | Value | Canonical statement |
|---|---|---|
| EK-1 | Heat states (Enemies C-3) | Three states per zone: **Cool** (no damage), **Working** (light periodic damage outside niches, about a third of Surging), **Surging** (heavy periodic damage outside niches, tuned so a ~4 s crossing costs ~10–15% max HP; walkable, never a wall). Values pending GD. Keyed to the presentation hour where EI-HT-01 is built; otherwise the Zones §6.1 default column. Quest pins override for the pinning player and are step-scoped. A cooling niche stops the damage and waiting in a niche always turns a zone. No meter, no stamina, no stealth, no cold or frost damage. |
| EK-2 | Tells (Enemies §3, §8.1) | A tell shows its zone's state and is readable from outside the zone; every red tell also crazes, so state never rests on hue alone. Inspect text gated on `EH_TELLS`. |
| EK-3 | Vent breath (Enemies §8.1) | Ash lifts **1.5 s** before every exhale; the exhale deals damage and one step of knock-back over the grate only. Cycles: ~10 s (U2, K2, L4, ESH duct), ~12 s (U5), ~8 s (U7). |
| EK-4 | Pressure plates (Enemies I-21, I-22) | Primed (visible), vent ~0.6 s after the step, spent ~8 s, re-priming ~2 s (Act II). Compliant with C-1 because the primed state is shown before the step. No displacement ends on a primed plate. |
| EK-5 | Defeat and re-form (Enemies C-4, C-13) | Every enemy defeated at 0 HP (CDR-1) with the ordinary defeat presentation. Resonance forms re-form only on their site's trigger while their condition lasts, up to their cap; constructs never re-form. **No SX entry; the quest on-defeat hook is not used by Emberholt.** The Draw Sentinel is destroyed and stays an inert prop. Combat never reveals evidence and no quest item drops. |
| EK-6 | Hazard floor (Enemies C-2; authored tuning requirement, pending GD) | No single hazard event (heat tick, exhale, plate, patch, scald, burst, seam) takes a player from above **25% max HP** to 0. Below 25%, staying in a Surging zone can defeat a player. Zones adds a placement rule: on every required route, cooling niches are spaced so that a full-health player walking between them does not fall below 25% from heat alone. |
| EK-7 | Displacement (Enemies C-1, C-2, C-6; pending GD) | Any displacement (push, pull, knock-back, knockdown, stagger) telegraphs at least **1.5 s**. No displacement ends inside a slag pool, on a primed plate or off an edge; it stops at the edge. Zones adds: **no displacement crosses a level change** (step, ledge, stair, pit rim, plinth, ring edge) or ends in a Surging zone away from a niche. No falls exist. |
| EK-8 | Ranged and reach (Enemies C-7, §12) | First-class in every fight, never required (CDR-2). Every raised enemy stands on something a player can walk to; hovering flares stay within ~2 m of their lip; every attack point is answered; out-ranging never ends a condition fight. U10 has no raised firing spot (leash ~5 s). Zones adds: where that walkable access is a stair or ladder, it depends on Zones §5A, and in today's flat build it must be a ramp or an at-grade position (ML-05, ML-10, ML-12, ML-29, ML-34 to ML-36). Every Ranged option has a non-ranged alternative (the ESS damper's Option B, subject to ML-17). |
| EK-9 | Pins | Step-scoped; released at step end; quest completion releases all of that quest's pins; unpinned zones show the Zones §6.1 default. Logout restores pins by the persisted step. |
| EK-10 | Channels in heat | A channel in a heat zone keeps progress (Lowmark channel convention). Pending Sol: heat ticks do not interrupt it, or its pad stands in a safe volume. |
| EK-11 | Set-piece cap and solo (Enemies C-10, C-12) | No more than 5 hostiles standing at once in any set piece. Every encounter is solo-clearable as authored; co-op scales health up from the solo baseline; credit only through a partner's own active step. |

### 5.2 Conflicts between packages and open questions

| Id | Finding | Sources | Recommendation or question |
|---|---|---|---|
| **EQ-01** | **Damper step.** The bible §6.1 brief puts the EH-M5 damper in S05; Act II moved it to S04 (recorded deviation B14.2). | Bible §6.1; Act II | Follow Act II. **Resolved 2026-11-15:** bible §6.1 aligned to Act II. |
| **EQ-02** | **Sigil-stone hedge.** The bible §9.4 calls the stone a carry-state "if the budget is 4"; Act II makes it an item and Act III counts five of five. | Bible §9.4; Acts II, III | Consistent at five. Note only. |
| **EQ-03** | **Stale cross-region note.** Act I says `TH_STANDING` and `MR_STANDING` are "read only by side quests and EH-M6". No Emberholt package reads either; `MR_STANDING` appears only in the CV-M1 gate beside `EH_STANDING`. | Act I header; all packages | Harmless; Act I's sentence should drop both at its next edit. Resolved in package 2026-11-15 (Batch 4 encounter alignment review). |
| **EQ-04** | **EH-M6 sets a flag before it is Active.** Act III sets `EGA_FROST` (the frost variant and the dusk pin) on Cinderwall entry while EH-M6 is Inactive, and S00 completes on accepting `EGA-D1`. A player who declines keeps a frost night with no Active quest. | Act III §6 trigger, §9 | Recommend: the entry trigger makes EH-M6 **Active** at `S00_frost` (as the Mire's MBL auto-start), so the pin belongs to an Active step. Question for Sol: can a quest auto-activate on zone entry (EI-QS-04)? Resolved in package 2026-11-15 (Batch 4 encounter alignment review). |
| **EQ-05** | **Post-story heat with no schedule.** Act III §E.3 says heat runs on EI-HT-01 "or quest-pinned Working where the schedule is not built", and §E.9 uses "the day's schedule". After completion no pin exists (EK-9). | Act III §E.3, §E.9 | Use the Zones §6.1 default column as fixed data whenever EI-HT-01 is not built. Question for Sol (as Mire Q-03): is a fixed per-zone default table acceptable as data in the world-state system even if the schedule is never built? Resolved in package 2026-11-15 (Batch 4 encounter alignment review): Act III post-story heat uses the Zones §6.1 default table; §E.9 now relies on world pockets EW-01 and EW-02 (Enemies I-25), not a schedule. |
| **EQ-06** | **Derived flag writer.** `EGH_GATE_OPEN` is written by a world rule, not a quest. | Act I §C12 | One writer (the rule). It must also be evaluated for a player who completed TF-M3 or MR-M2 before reaching Emberholt. |
| **EQ-07** | **Post-completion write.** EMS `S07_mend` writes `EH_UNBURNT` (strained → kept) after EMS is Completed. Still one writer. If it happens after EH-M6, the tally board has already been seen. | Unburnt file | Acceptable: the board reads the flag at S08 only. EI-QS-10. |
| **EQ-08** | **Channels interrupted by heat.** Today's build interrupts timed work on a hit; heat zones tick periodic damage on required channels. | `UNITY/README.md`; Acts I–III | EI-CA-03. Question for Sol: exclude hazard ticks from interruption, or require safe pads? |
| **EQ-09** | **The ledger "reappears".** Act I says `EEH_ledger` reappears in EH-M6 and CV-M4 from Yorven's strongbox. It is removed at EEH S07. | Act I item table | Treat the reappearance as a world prop (inspect), never a re-granted item, so the budget stays at five. Confirm with the Act I author. Resolved in package 2026-11-15 (Batch 4 encounter alignment review). |
| **EQ-10** | **Shaft.** EH-M4 needs ladder descents and ascents through three landings (ML-09). | Act II §A5 | **Content fallback added in review:** flat landings with a per-flight climb interaction using EI-QS-06 placement (Zones §5A). Question for Sol: is that, an off-mesh ladder link, or zone transitions at head and foot achievable in the milestone? [DIRECTOR item EDI-4 only if none is.] |
| **EQ-11** | **Melee-only path through the damper.** ESS S04 Option B (non-ranged) uses a ladder (ML-17). With no ladder form, a melee-only player cannot finish S04 (CDR-2 breach). | Act II §B6 | Ramp-and-landing beside the breast, or an interaction ladder, in the milestone. **Content fallback added in review:** the latch pulled from the floor with the fire hook (Zones ML-17), so no CDR-2 breach remains if neither is built. |
| **EQ-12** | **Shared environmental state in co-op** (presentation question for Sol only; CDR-6). Partners at different steps need different heat pins (U2–U5 in ECW and EGA; K4; L3–L4), different hour pins (dusk, night, dawn), different `EGA_STAGE` variants and the frost variant, and different barricades. One player's state must not strand, damage or advance the other. | All acts; side quests | **Open for Sol as a presentation question only; not a prerequisite for solo completion.** Option families (Mire Q-18): F1 per-player phased set piece; F2 per-viewer props and hazard volumes; F3 shared presentation that never gates damage, navigation or credit; F4 compatibility gate on entry; F5 defer the stateful step to solo or a same-step partner. Recommendation only, for Sol to accept or reject: hazard damage and channel availability follow each player's own state where the runtime allows it; otherwise F4 or F5. No content row and no solo step depends on any of these. |
| **EQ-13** | **Raised enemy positions on stairs or a ladder** (K3, R1 gallery, the ECN-E1 roof, the EGA-E1 sack, the ECC-E1 coil stack) are unreachable by melee in a flat build. The Enemies file (§12) counts stairs and ladders as walkable reach. | Act II; side files; Enemies §12 | Ramps or at-grade positions (Zones ML-10, ML-12, ML-34 to ML-36). Applied in Enemies §12 (2026-11-15): stairs and ladders count as reach only once Zones §5A builds them; the EAC-E3 warden-frame follows a target onto the rim or gallery. |
| **EQ-14** | **Discoveries need state without a pin** (Mire SS-20 lesson). | Bible §7.5 | `EDS##_SEEN` on inspect; props stay in their default state for all players. |

---

## 6. Director-level items

| Id | Item | Ask |
|---|---|---|
| EDI-1 | **Heat-zone defaults** (Zones §6.1, ZQ-2) | Approve the default column so heat works without EI-HT-01 and after every quest completes. |
| EDI-2 | **Red-Lit annex placement** `[C14.2]` (Zones ZQ-1) | Place it where the bypass can rise into its lower stacks and it has a street door. |
| EDI-3 | **EH-M6 auto-activation** (EQ-04) | EH-M6 now auto-starts on Cinderwall entry (Act III); Director may still prefer an offer. |
| EDI-4 | **The EH-M4 shaft** (EQ-10, Zones ZQ-5) | If Sol cannot provide any ladder form in the milestone, including the per-flight climb interaction fallback: accept a steep spiral ramp in place of the ladders (same beats), or hold EH-M4. |

Open rulings already tracked elsewhere and not repeated: ED-1, ED-7, ED-15, ED-20. (D-E2, D-S1 and ED-3 were ruled 2026-11-15 and are closed here.)

**Simplification from the 2026-11-15 rulings (for Sol and the SCE; no change to ids).** `EH_THALAN` keeps its id but now has one value, `freed`, written at EAC completion; no reader branches on it, so it need not be stored as a two-valued enum (a bool, or a derived read of `emberholt.main.04` Completed, satisfies every reader). The `aided` content keys, the aid-in-place choice node and its variant props (Asera's chair in §E.7) are dropped. The `[INITIATE]` swappable key (EI-DG-03) is dropped for a fixed string. No test needs a second Thalan outcome.

---

## 7. Milestone scope and acceptance tests (CDR-3)

### 7.1 Build order inside the milestone (dependency order, not a schedule)

1. EI-QS-01 to EI-QS-07, EI-FL-01 to EI-FL-03, EI-DG-01 to EI-DG-03, EI-IT-01 to EI-IT-05.
2. Heat in its fallback form: EI-HT-02 pins, EI-HT-03 volumes and niches, EI-HT-04 tells, EI-HT-05 vents, the Zones §6.1 defaults as data, EI-CA-03.
3. Vertical access per Zones §5A for the thirteen required rows (EI-AG-02), with ML-09 and ML-17 first.
4. EI-PR-01 variant swap and EI-WV-01 frost; EI-EN-03 boss persistence.
5. EI-QS-08 (or `EGH_GATE_OPEN`); EI-SG-01 (or per-door inspect).
6. Upgrades if time allows: EI-HT-01 schedule, EI-ES-01 escort, EI-QS-11 quest travel, EI-QS-12 warden's round.

### 7.2 Acceptance tests (authored, not run)

These are written against the packages. None has been run. Each is a pass/fail statement for a build.

| Id | Area | Test |
|---|---|---|
| EAT-01 | Lifecycle | No Emberholt quest can enter a fail or abandon state. Walking away from any step and returning plays the authored resume hook at the persisted step. |
| EAT-02 | Heat fallback | With EI-HT-01 **not** built, EH-M1 to EH-M6 and every side quest complete; every unpinned zone shows its Zones §6.1 default; no required route is impassable for longer than one keep-watch turn. |
| EAT-03 | Pins | Every pin releases at its step's end; completing a quest leaves no zone pinned for that player; logout and return re-apply the persisted step's pins. |
| EAT-04 | Hazard floor and niches | No single hazard event takes a player from above 25% max HP to 0 (Enemies C-2, pending GD); on every required route a full-health player walking between niches does not fall below 25% from heat alone. |
| EAT-05 | Channels in heat | Every required channel in a heat zone completes while the zone is at its pinned state, with no interruption from heat ticks (or from a safe pad). |
| EAT-06 | Staged pressure | In EH-M6, each stage swaps exactly the zones in Zones §6.3; passing a stage unbled leaves it Surging and the relief cannot be turned until both cocks are bled. |
| EAT-07 | Boss persistence | A player defeated by the Draw Sentinel wakes at the warming house with EH-M6 Active and every collar already shut still shut. |
| EAT-08 | Defeat | Every Emberholt enemy is defeated at 0 HP; no step listens for `creature.scripted_defeat`; no defeated enemy speaks testimony. |
| EAT-09 | Ranged parity | Every fight can be won by a melee-only player and by a ranged-only player; every enemy firing spot is melee-reachable; ESS S04 completes by Option B with no ranged attack. |
| EAT-10 | Vertical | Each of the thirteen required Zones §5A rows completes by its built form or its fallback; no required interaction is on a floor the player cannot reach. |
| EAT-11 | Gate | A player with EH-M2 Completed and only TF-M3 Completed can start EH-M3; the same with only MR-M2; with neither, the journal shows the locked entry naming both. |
| EAT-12 | Items | Exactly five quest items exist; each is gained and removed at the steps in §2.11; none can be dropped or sold. |
| EAT-13 | Region flags | Each of the fourteen `EH_*` flags is written only by its §3.1 writer. |
| EAT-14 | Solo | Every quest completes solo from a fresh character that meets its prerequisites, with no co-op feature built. |
| EAT-15 | Co-op credit | Two partners at different steps: a defeat credits only a partner whose active step consumes it; one partner's keep watch, pin, frost night or stage does not change the other's step or hazard state (or the pair is gated per EQ-12 F4/F5). Runs only with a co-op build; not a solo prerequisite (CDR-6). |
| EAT-16 | Sigil fallback | With EI-SG-01 not built, EH-M4 S04 completes using per-door inspects. |
| EAT-17 | Respawn | Death in each main-quest step returns the player to the Zones §6.6 respawn point for that step (or the region fallback in EI-QS-06), outside any Surging zone. |
| EAT-18 | Escort | With `freed` (the only outcome; D-E2, ruled 2026-11-15), Thalan follows from R2 to the shaft foot and leaves by the side cut; he never needs to climb. |
| EAT-19 | Displacement | No push, pull or knock-back ends inside a slag pool, on a primed plate, across a level change or off an edge (EK-7). |
| EAT-20 | Cap | No set piece ever has more than 5 hostiles standing at once, including re-forms and add-spawns (Enemies C-12). |

---

## 8. Internal review log

| Pass | Result |
|---|---|
| **Authoring (2026-11-15)** | Written against the bible, Acts I–III and the four side-quest files as reviewed on 2026-11-14 and 2026-11-15, with the Mire integration file as the format model and the Mire playability audit for lessons. Verified: the fourteen region flags and their single writers; the five quest items and their gain and removal steps; the fifteen named presentation events; every cross-region read; the bible's two runtime needs (EI-HT-01, EI-PR-01) and the two possible needs the acts flagged (EI-QS-08, EI-SG-01). No SX; no on-defeat hook. No package was edited. |
| **Aligned with the Enemies file (2026-11-15)** | The Enemies file landed while this file was being finished and was read the same day. Changes here: §5.1 EK-1 to EK-11 restate Enemies C-2, C-3, C-4, C-6, C-7, C-10, C-12, C-13 and I-19, I-21, I-22 with a crosswalk (the hazard floor now uses C-2's wording; heat values from C-3; EK-11 added). §2.18 maps the Enemies runtime rows R-1 to R-14 to this register and adds EI-EN-09 (cap). EI-AG-02 and EQ-13 now count the raised enemy positions from Enemies §12 (Zones ML-34 to ML-36). EAT-04 rewritten; EAT-19 and EAT-20 added. **Still to watch:** Enemies Q1 (the unplaced Ashfall revenant) changes creature data only; the 15 package edits it lists (PE-1 to PE-15) change no flag, item, step or id used here. |
| **Batch 4 zones/integration review, 2026-11-15** | Independent review against the bible, Acts I–III, the four side-quest files, CDR-1 to CDR-6 (§3.7), the engineering handoff and `UNITY/README.md` (read-only). **Verified:** fourteen `EH_*` flags, one writer each, against every package; five quest items with matching gain and removal steps; fifteen presentation events, all present in the packages and none missing; no SX and no on-defeat hook; every co-op row optional assistance, none a solo prerequisite. **Fixed:** §1.1 Flood Kitchen wording (loft stairs unfinished; crates have flat access markers); the MUST convention now states that a MUST with no named fallback is met by the standard shared capability; fallbacks added to EI-QS-04, EI-HT-02, EI-HT-07, EI-HT-08, EI-KW-01, EI-KW-02; EI-CA-03 kept as a request to Sol with a standard fallback (niche-touching pads) and two options (exclude ticks; pause the segment instead of cancelling); EI-AG-02 recounted (37 rows; 13 required; 7 raised positions) with the new Zones fallbacks for ML-09 and ML-17, EQ-10, EQ-11 and EDI-4 updated to match; EQ-12's meanwhile rule reworded as a recommendation for Sol; EAT-15 labelled co-op-build only; §7.2 headed "authored, not run". EQ-01 resolved (bible aligned to Act II). **From the encounter review, verified in the packages and applied:** EQ-03, EQ-04, EQ-05, EQ-09 resolved in package; EI-QS-04 and EDI-3 now state EH-M6's auto-start; EQ-13 notes Enemies §12 (stairs and ladders are reach only once Zones §5A builds them; EAC-E3 frame follows onto rim or gallery); §E.9 relies on world pockets EW-01 and EW-02. **Left for the Director:** EDI-1, EDI-2, EDI-3, EDI-4 stay questions. |
| **Emberholt character rulings, 2026-11-15** | D-E2: `EH_THALAN` row one value (`freed`); EI-ES-01, EAT-18 de-tagged; simplification note under §6 (enum, `aided` keys, chair variant and swap keys dropped). D-S1: EI-IT-04 and the flag row de-tagged. ED-3: `[INITIATE]` → Iven Calder in EI-DG-03/04, EI-IT-02 (journal copy carries no gloss). D-EL: noted in the header; no new requirement. No EK/EAT row tested both Thalan outcomes. |
