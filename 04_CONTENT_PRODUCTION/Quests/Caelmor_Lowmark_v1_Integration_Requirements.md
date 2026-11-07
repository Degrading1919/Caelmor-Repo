# Lowmark v1 — Integration Requirements (Technical Handoff)

**Status:** Requirements handoff from Creative Production, written for the Creative Production Director. Bible batch 5 (`Caelmor_Lowmark_v1_Narrative_Production_Bible.md` §12). This file states **what the authored Lowmark content needs the runtime, schemas and data to support**. It does not design schemas, write JSON or specify C#. Field names below are requirement labels. The **Schema & Content Engineer** owns all real names and shapes, and the **Systems Engineer** owns all runtime contracts.

**Director rulings 2026-11-03 (binding):** `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. CDR-1: every enemy is defeated at 0 HP; the non-lethal defeat requirements (yield thresholds, downed state, tied props, hostile→neutral swap for ordinary enemies) are **removed** and replaced by one small need, a quest on-defeat hook for named creatures (SX-1, SX-2) that plays a scripted outcome and spawns the NPC non-hostile. CDR-2: ranged is a core combat skill, accepted in every encounter, never required. CDR-3: "Lowmark v1" is the label of the first internal production milestone, not a release. Technical changes for the Systems Engineer: `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`.

**Audience:** Systems Engineer (runtime, Stages 24–30, 33.x B2 bindings), Schema & Content Engineer (Stage 31, 32, 33.3/33.6/33.7 data, 34.x), with the Gameplay Designer, Zones/POI and item/economy passes named where they own a decision.

**Quest lifecycle (Creative Director ruling, reconciled 2026-11-02 by the Systems Engineer):** quests have exactly three states, **Inactive → Active → Completed**. No quest fails or is abandoned. A quest the player leaves stays Active at its persisted step and is resumed, never re-instanced (§3.7). Stage 15.2, Stage 27 and `QuestRuntimeSystem.cs` now agree on this model.

**Canonical choices applied (concurrent fix pass):** `LM_ORIEL_PROMISE` = aloud / many_hands / return; `LM_PLAN_ROUTES` and `LM_PLAN_MEMORIAL` replace `LM_PLAN_*`; MQ10's Under the Lamb chip = `UL_LEDGER` (weaker if `UL_LEDGER_CUT`; `UL_RHOSYN_WITNESS` for testimony); the player holds `SM_requisition` and `NF_bill_of_lading` until MQ10; ~~human enemies are downed or yield rather than killed~~ (superseded 2026-11-03 by CDR-1: defeat at 0 HP; SX-1/SX-2 via the on-defeat hook). §10 marks these rows canonical.

**Sources read:** the bible (all); *The True Line* §9–12; the steps, flags, choices, items, integration, co-op and failure sections of `Caelmor_Lowmark_Main_Act_I/II/III.md` and the three `Caelmor_Lowmark_Side_Quests_*.md` files; dialogue-file condition and effect notation in `04_CONTENT_PRODUCTION/Dialogue & Narrative/`; `CODE/Systems/QuestRuntimeSystem.cs`; Systems Design Stages 15.1, 15.2, 15.3, 16.3, 27; `UNITY/README.md`; Roadmap Stages 24, 30, 31, 33, 34, 35.

**Conventions in this file**

| Mark | Meaning |
|---|---|
| **MUST** | The content cannot be built as authored without it. Every MUST has a fallback named in §7 unless marked *no fallback*. |
| **SHOULD** | The authored experience degrades without it but stays playable and non-blocking. |
| **[DIRECTOR]** | A Director-level item: it would amount to a new core system, a significant unapproved mechanic, or a ruling on an open `[PROPOSAL — DIRECTOR]`. Collected in §11. |
| Quest codes | TL (MQ1) · SM MQ2 · HW MQ3 · NF MQ4 · GL MQ5 · TF MQ6 · DK MQ7 · MN MQ8 · BF MQ9 · CR MQ10 · SV MQ11 · RR MQ12 · side: WC BW FK BP HS · UL NB UR NT FW OL · SB UC TB WD CN VK FC · ME01–ME10 |

---

## 1. What exists today vs. what Lowmark needs

### 1.1 What exists

| Area | What is there today | Source |
|---|---|---|
| Quest-level state | `QuestRuntimeSystem`: register, activate, complete; server-authority and mutation-gate checks; lifecycle eligibility; a pluggable `IQuestProgressionEvaluator` returning NoChange / Complete. In-memory records only. | `CODE/Systems/QuestRuntimeSystem.cs` |
| Quest states in code | `Inactive, Active, Completed`. No failed or abandoned state (matches the Director's three-state rule). | same |
| Quest event inputs in code | `WorldEvent(name)`, `CombatEvent(outcome)`, `InventoryEvent(resource, delta)`. No player id, target id, volume id, dialogue node or step on any of them. | same |
| Quest state contracts | Three states, `Inactive`, `Active`, terminal `Completed` (15.2, revised 2026-11-02). Event observation scoped per-player / per-world / per-zone; deterministic, duplicate-safe (15.3). Stage 27 uses the same three states and forbids "implicit quest activation or completion" and quest systems mutating inventory, combat or simulation. | Stages 15.1–15.3, 27 |
| NPC interaction contract | Server-recognized interaction event; must not advance quests, grant items or alter narrative directly. | Stage 16.3 |
| Client fixture | Click-to-move on a flat baked NavMesh; host-validated interaction on a target ID with reach and LOS; `PlayableHost.InteractionCommitted(session, targetId, tick)` and `SnapshotCommitted` as narrative entry hooks; no jump, no multi-level traversal, no off-mesh links, no disk persistence, no NPCs, no quest data. | `UNITY/README.md` |
| Combat, inventory, NPC runtime | Runtime systems and validation scenarios exist in `CODE/Systems/`. | TL §12.1 |
| Old schemas | `ARCHIVE/Deprecated/QuestChain_Schema.json`, `Dialogue_Schema_Flat.json`, `NPC_Schema_Flat.json`. Deprecated; not authority. | repo |
| Roadmap | Stage 24 (Quest runtime), 25 (NPC), 30.5/30.6 (quest and interaction UI), 31 (all schemas), 33 (Lowmark slice), 34, 35 are all unchecked. | Roadmap |

### 1.2 Gap table

Owner key: **SE** Systems Engineer · **SCE** Schema & Content Engineer · **GD** Gameplay Designer · **ZN** Zones/POI package · **IT** item/economy pass · **ART** art/audio.

| # | Lowmark content needs | Exists today | Gap | Roadmap task | Owner | Priority |
|---|---|---|---|---|---|---|
| G01 | Ordered **steps** inside a quest instance, each with objective text key, completion predicate, required/optional/conditional marker | Quest-level state only; evaluator returns NoChange/Complete | Step model, step-advance outcome, step persistence | 31.3.A; 24.1.B, 24.3.B | SCE (shape), SE (runtime) | MUST |
| G02 | **Quest-local typed flags** (bool, enum, bounded int) persisted per instance and **readable after completion** by other quests and dialogue | None | Flag store, typing, cross-quest read scope | 31.3.A; 24.1.B; 24.4 | SCE, SE | MUST |
| G03 | **Character-scoped region flags** `LM_*` (16 flags, §3.6) | None | Region flag store on the character save; write-once vs overwrite rule | 31.3.A; 24.4; 21.4 | SCE, SE | MUST |
| G04 | **Walk-away and resume**: a quest the player leaves stays Active at its persisted step; an authored resume hook points them back (no abandon, no fail, no fresh instance) | Three-state model agreed across 15.2, 27 and code (2026-11-02); step persistence is G01 | Resume-hook data per quest (§3.7); quest journal keeps every Active quest listed and resumable | 30.5; 34.5.A | SCE (resume-hook data), SE (journal/query support) | MUST |
| G05 | **Auto-accept / chained activation** (quest goes Active on a volume entry or on another quest's dialogue end) | Activation is an explicit call | Stage 27 forbids "implicit activation": define these as explicit, data-declared offer/accept triggers | 24.1.A; 24.2.A | SE | MUST |
| G06 | **Rich server event vocabulary** (§2: ~25 types with player, target, volume, node, outcome payloads) | Three name/outcome/delta structs | Event types, payloads, scoping, trace ids | 24.2.A/B, 24.2.B2 | SE | MUST |
| G07 | **Dialogue content** with conditions, effects, speakers, line keys, barks, inspect texts, variants | None | Schema + runtime; effect execution path that respects Stages 16.3 and 27 (§4.5) | 31.5.A; 35.2.A; 25.3 | SCE, SE | MUST |
| G08 | **Effect executor** for dialogue/quest effects that touch inventory, NPC state, props and spawns (give/take item, loan tool, start escort, start window) | Stage 27 forbids the quest system from mutating inventory/simulation | An authorized path where quest/dialogue *request* and owning systems *apply* | 24.3.A; 26 (item) ; 25.3 | SE | MUST |
| G09 | **NPC definitions** with step-conditioned positions/schedules (~45 named, many roles; §5) | NPC runtime, no data | NPC schema + step/flag-keyed placement sets | 31.2.A; 32.4; 33.2.B2; 35.3.A | SCE, SE | MUST |
| G10 | **Inspect interactions** returning one localized line, with conditional variants | Generic host interaction on a target ID | Inspect kind, text key, variant conditions, inspect event | 30.6; 33.1.B2 | SE, SCE | MUST |
| G11 | **Channelled interactions** (fixed duration, cancel on move/damage), **segmented channels** with kept segments | None | Channel timer on server; segment persistence | 30.6.B2; 33.5.B2 | SE | MUST |
| G12 | **Carry state** (≈30 carry objects, §6.2) | None | Carry flag, deposit volumes, return-to-source rule | — (not on roadmap) | SE | MUST (fallback exists) |
| G13 | **Encounter pockets** gated by quest step, waves, re-forming creatures | Combat runtime; no spawn rules | Step-gated spawns, wave spawner, re-form timers | 33.7.B/B2; 28.2 | SCE (data), SE (rules), GD | MUST |
| G14 | **Drift-site state** per character (active / quieted / tended / closed) driving spawns | None | Site state store and spawn read | 31.4; 33.7.B2 | SE, SCE | MUST (depends on D-6 **[DIRECTOR]**) |
| G15 | **Time windows / keep-watch** (dusk, night, dawn, pulse, named scripted windows) | No world clock | Per-player server-side quest clock | 28.1; 30.x | SE | MUST |
| G16 | **Per-player presentation** of props, terrain decals, water planes, NPC positions keyed on the local player's state | Presentation interpolates host snapshots only | Per-viewer replication filter or client-side keyed presentation | 29.2; 33.1.B2 | SE | SHOULD (all packages carry fallbacks) |
| G17 | **Per-player instanced NPCs and creatures** (DK Bryn, HW Orrin, MN elk, SV evacuees, Muster visibility) | None | Owner-visible entities | 29.2; 28.2 | SE | **[DIRECTOR]** (fallbacks exist) |
| G18 | **Follower / escort / walk-with NPCs**, including MQ11 trance state machine | NPC runtime has no movement behaviours | Follow, wait-at-checkpoint, pace-match; trance FSM | 25.x, 26.x, 35.3 | SE, GD | MUST |
| G19 | **AI that targets props/NPCs** (withies, carts, lanterns, crew winch, Bryn, gate pawl) | Decision framework plans only | Prop/NPC target selection | 26.1–26.4 | SE, GD | SHOULD (fallbacks) |
| G20 | **Quest on-defeat hook (CDR-1)**: every enemy is defeated at 0 HP with the ordinary defeat; for two named creatures (SX-1 Joss, SX-2 Sallow) the quest plays a scripted outcome on defeat and spawns the NPC non-hostile | Combat runtime emits defeat; no quest hook on a named creature's defeat | A quest on-defeat hook for named creatures (SX-1, SX-2) that plays a scripted outcome and spawns the NPC non-hostile. No threshold, no downed state, no tied props | 25 (combat integration) | SE, GD | MUST (2 uses) |
| G20a | **Ranged accepted in every encounter (CDR-2)**; WC has one optional borrowed hunter's short bow (§6.3) | Combat and item runtimes | Ranged combat, ammunition and weapon catalog are owned by Gameplay/Systems/Schema; no quest step requires ranged | 25; 36.2 | GD, SE, SCE | SHOULD (optional content) |
| G21 | **Multi-level navigation** (depot, Lock, bell tower, falls path, bridge underside, culverts) and **agility triggers** | Flat NavMesh, no off-mesh links, no jump | Multi-level NavMesh; Phase 1.3 trigger boxes | 33.1.B; 30.2 | SE, ZN | MUST for multi-level; agility SHOULD (walkable fallbacks everywhere) |
| G22 | **Craft/station bindings**: Cooking (6 sites), Leatherworking (tan-yard), Smithing (forge, mill anvil, WD anvil-stone) | None | Station binding | 33.5.B2 | SE, IT | MUST for FK/BP/HS; SHOULD elsewhere |
| G23 | **Gathering and Hunting hooks** (Woodcutting gather events; Hunting approach/resolve/recover; F4 alert-and-flight) | Gathering designs exist | Runtime hooks + events | 33.4.B2; Hunting pass | SE, GD | MUST for WC/FK/MN; SHOULD elsewhere |
| G24 | **Quest items** (8 for Lowmark) with non-droppable, non-sellable, inspect text | Item runtime | Item definitions, flags | 31.1; 33.6.B | SCE, IT | MUST |
| G25 | **Server-emitted presentation events** (20 named, §2.3) for client-local effects | None | Event emission + client effect hooks | 30.1; ART | SE, ART | SHOULD (gameplay never reads them) |
| G26 | **Quest persistence** including sub-step progress (segments, gate %, wave checkpoints, follower checkpoints) | In-memory only | Save/restore wiring | 24.4.A/B, 24.4.B2 | SE | MUST |
| G27 | **Respawn anchors keyed to quest step** | Not specified | Respawn override by active quest step | 23.x/28.x (gap) | SE | MUST |
| G28 | **Minimal quest UI**: objective text, sub-counters (0/3), suppression windows (no UI during strange moments) | None | Quest log + objective binding; "UI suppressed" flag per step | 30.5 | SE | MUST |
| G29 | **Set-piece controllers** (TF gate band, DK hold/slip, SV gate progress with decay, BF flow-table, CR evidence table, UC observation) | No scripting layer; 15.3 forbids scripting in trigger evaluation | Bounded, data-configured state machines outside the quest evaluator | 24.3 / 28.x (gap) | SE | **[DIRECTOR]** (§11 D-INT-1) |
| G30 | **Content validation**: every flag read has a writer; every step predicate references known events; every required proof has a guaranteed path | None | Validation rules | 31.6.A/B; 33.8; 34.4 | SCE | MUST |

---

## 2. Server event vocabulary

### 2.1 Rules that apply to every event

| Rule | Requirement |
|---|---|
| Origin | Every event is **server-recognized** (15.3 §3). Client input remains intent only: destination, sprint, debug direction, interaction target ID (README). No event is accepted from a client. |
| Commit point | Events are emitted **after** the owning system commits its state change (README: "Interaction acknowledgment is emitted only after a legal committed state change"). Quest evaluation consumes them after simulation and before the save window (Stage 27). |
| Scope | Each event carries `player` (owning Player Identity) when per-player, plus `world`, `zone`. Shared-world events (a creature defeated) carry a `credited_players[]` list computed by the combat system: every participant whose active step consumes that event. |
| Idempotency | Each event has a server trace id (24.2.B2). Duplicates and stale events are dropped (15.3 §6). Re-delivery after restore is forbidden; progress must already be in persisted state. |
| No presentation feedback | No gameplay predicate may wait on a **client** reporting that a presentation finished. Where a step "completes when the presentation ends", the server emits the end event on its own fixed timer (§2.3). |
| Counting | "3 inspects", "4 of 5", "in order", "any one of" are **predicates over events** (§3.3), not distinct events. |

### 2.2 Event types (deduplicated)

| Id | Event (requirement label) | Payload (minimum) | Authority notes | Used by |
|---|---|---|---|---|
| EV01 | **volume.entered** | player, volume_id, zone_id, tick; optional `carrying` (carry object id) | Computed by the host from committed positions, never from a client trigger. Some volumes are **dynamic** (15 m around a moving NPC: OL Joss) and some require **carrying** (NB S05, UL S04). | Every package: step volumes, trail clues (NF), voice decoy (DK), knot/ring/threshold volumes, ME triggers |
| EV02 | **inspect.performed** | player, target_id, inspect_key; context: `window_id` if inside a time window, `carrying` if carrying | Reach and LOS validated as for the fixture interaction. Some inspects are valid only in a window (GL S02b well bucket during dusk) or only while carrying (CN wick). Inspect never consumes anything. | Every package. Heavy users: TL S02, SM S01/S07, HW, NF S07, GL S03/S05, TF S02/S06, MN S01/S05, BF S04/S06, WC, NB, OL S01 (ordered), SB, UC, CN, FC (4 of 5; 3 comparisons) |
| EV03 | **interaction.completed** | player, interaction_id, target_id, kind (`instant`/`channel`/`segment`), segment_index, outcome key (for branch interactions) | Channel timers run on the server; cancel on move or damage (TL rule) unless the interaction is marked "damage interrupts segment, keeps completed segments" (NF crank). Extends the fixture's `InteractionCommitted(session, targetId, tick)`, which today lacks interaction id and kind. | Every package (≈120 authored interactions). Segmented: NF crank. Branch outcomes: NF smash ×3 / chain ×2, GL fix branches, CR fire-line cut or smother |
| EV04 | **item.acquired** | player, item_def_id, qty, source (world pickup / NPC give / craft / gather) | Emitted by the inventory system after the grant commits. Quest reads, never writes inventory (Stage 27). | TL S03 (weathered post), S05 (marker_stem); SM S07 (`SM_requisition`); NF S07 (`NF_bill_of_lading`); TF S05 (sheets); DK S02a (bowl); CR S04 (`CR_board_minute`); WD S01b (stem) |
| EV05 | **item.given** | player, recipient (npc_id or shrine target), item_def_id **or** item_category, qty | Server validates the item is held; transfer executed by inventory. Category matching required: "any cooked food", "ordinary wood × N", "any tannin-rich bark". | TL S08b, D7 hand-overs; FK S01/S04 (×4); BW S05 Build; BP S03; TF S09; DK S03; CR S07b; SV S02b; WC feed option; MN_FED; NT S01b; UL pass route; ME02; ME09 |
| EV06 | **carry.picked_up / carry.deposited / carry.returned** | player, carry_object_id, deposit_target (volume or NPC), return_point | Carry objects never enter inventory. `returned` fires when a dropped or abandoned carry snaps back to its source (logout, leaving area, death). A carry-deposit onto an NPC counts as a give (TB gift). | TL sacks ×3, trunk; HW smoke-pot; GL stones, turf, stakes; TF beam; DK moss, stakes; CR record bundles ×2, soaked sacks, barge post, chips; SV lanterns; RR sack; WC sacks ×2; FK crates; BP armfuls ×3; UL crate, ledger; NB cloth; UR basket; NT bundles; OL lantern; UC paddle; TB fruit; CN boat; FC hurdles ×3, case, seed sack; WD hurdles ×2; ME10 lantern |
| EV07 | **creature.defeated** | creature_instance_id, creature_def_id, encounter_id, group_id, wave, outcome (`killed`/`dispersed`; `driven_off` removed, CDR-1), credited_players[] | Combat runtime authority. "Defeated" includes drift **dispersed** (may re-form); humans are ordinary defeats (CDR-1). Group and wave ids are required ("NF-E2 groups A and B", "all DK-E2"). | TL E2/E4; SM E1, Sack-King; HW E1–E4; NF E1–E3; GL E1/E4b/E4c; TF E1/E2/E3a/E3b; DK E1/E2; MN E1 (and elk killed); CR E3; SV E1–E4, `the_muster`, serpent killed; WC E1; UR E1/E2; FW E1–E3; UC E1; WD E1–E4; FC E1; NB E1/E2 |
| EV08 | **creature.scripted_defeat** (replaces `creature.yielded`, CDR-1) | creature_instance_id, creature_def_id, quest step, npc_def_id to spawn | Fired by the quest's **on-defeat hook** when a named creature reaches 0 HP: suppresses the ordinary defeat presentation, plays the scripted outcome and spawns the NPC non-hostile. No HP threshold. `cr.sallow_yield` is one instance. | CR S06 (SX-2 Sallow, on defeat); OL S04 (SX-1 Joss, on defeat). No other users |
| EV09 | **dialogue.node_reached** | player, dialogue_id, node_id, option_id chosen, flags `is_end`, `is_choice` | Emitted by the dialogue system after the node's effects commit. Satisfies Stage 16.3 (the NPC interaction itself never advances a quest). | Every quest. Specific non-end nodes: SM-D6.40, HW-D10.90, MN-D4 correct-reason, CR-D8.90, UL-D4.20, TF-D5 "tonight" |
| EV10 | **gather.completed** | player, node_id, node_type, skill, outputs[] | Woodcutting gather. Must fire even when the output is ordinary inventory (driftroot jam). | HW driftroot_jam ×3; SM driftroot_choke (opt); TL marker stem; DK stakes; UR scrub ×3; FW withies ×5; FC logs ×2; WD stem; BP stems; GL dike stakes |
| EV11 | **hunting.recovery_completed** | player, target creature_instance_id, outputs[] | Hunting recovery (field dressing) is not a combat kill (economy D02/D03). | WC S06a (sow); FK S02 (fowl ×2); optional elsewhere |
| EV12 | **craft.completed** | player, station_id, recipe or output category, output_item | Station-bound. Quest may require "required portions produced" or "weapon created". | FK S03 (fires the hush); BP S04 tan, S05 make; HS S02 blade; TF S03 strap (anvil path); SV/CR/TL optional cooking |
| EV13 | **window.entered / window.ended** | player, window_id (`dusk`, `night`, `dawn`, `first_light`, `pulse`, or a named scripted window), source (`keep_watch` / `world_clock`) | **Per-player server-side quest clock** (§7 M04). Never real time. | HW S02a (dusk tick); NF S01; GL S02 `gl.backwater_dusk`, S08 `gl.backwater_test`; TF S04 `tf.crew_scene`, S07/S08 pulse; DK S04/S05 hold window; MN S02 dawn; BF S00 dawn; CR S01/S07; SV S01; RR dusk; UL grate window; NT watches; OL S03; TB dusk/first light; WD night/dawn; CN dusk; ME02/03/04/06/09/10 |
| EV14 | **watch.step_completed** | player, watch_interaction_id, step_index | One cancellable step of keep-watch (one "lantern-fill"). Could be EV03 with kind `watch`. | NF S01 (×1 with `HW_LEAD_TALLY`, else ×2); NT S02–S05 |
| EV15 | **script.event** (start/end) | event_id, phase, owner player(s) | Server-emitted on fixed timers; client plays local presentation. Steps that "complete on presentation end" use the server's `end`. Full list §2.3. | NF S02, BF S06, TB S04, SB S07, UC S02, CN S03, TF S08, MN S07, SV S07, CR S08 |
| EV16 | **npc.arrived** | npc_instance_id, npc_def_id, volume_id, owner player | Escort, follow and walk-with arrivals. Arrival of an NPC the player is escorting, not the player. | HW S02c (Orrin ×2); CR S04 (Hesketh); MN S08; BF S01; BW S01 (Tamsin); NT S01 (×3), S03 (household); FW S02 (×3 groups); OL S06 (Joss); SV S02 (×7 cutters at tally board); ME10 |
| EV17 | **creature.entered_volume** | creature_instance_id, volume_id, owner player | Wildlife reaching a volume (herding). | MN S04 (elk reaches causeway exit) |
| EV18 | **npc.action_completed** | npc_instance_id, action_id | NPC scripted actions under player camera; hostile NPC channels. | UR S06 (Joric turns paddle); BF S06b (Oriel pulse); MN S07 (Sedge quieting); SV (Sedge spreads pressure); TF "pry the pawl" (hostile); DK hold slip/recover |
| EV19 | **prop.state_changed** | prop_id, owner player (if per-player), state, value | For set-piece props whose state is the predicate. | SV gate-board % ×3; CN boards at worn height; FW withies standing; BF gate order valid; TF band 0–3, bays filled; UC foot-pool level; CR chip deposits, bundle singed; NT/WD/CR lantern lit/out |
| EV20 | **encounter.wave_resolved / encounter.completed** | encounter_id, wave, outcome, owner player(s) | Required where a step needs "waves resolved" rather than every creature dead (FW: "resolved with ≥ 3 withies standing"; repeats on failure). | FW S03; NT S02/S04; WD S03; DK S05; SV gates; TF S08 |
| EV21 | **quest.state_changed** | player, quest_def_id, from, to | Drives prerequisites, offers, auto-start chains, and steps that "auto-pass" on another quest's completion. | SM S00 (TL Completed); NF (Active from HW-D10 end); CR S00 (MQ9 Completed); RR S00 (from SV-D9 end); VK S02 (auto-passes on MQ9 Completed); every side-quest unlock |
| EV22 | **timer.elapsed** | player, timer_id, duration | Per-player server timer started by a step or interaction. | TB S05 (60 s after wake); CN S06 (sit or 60 s); CR bundle smoulder (~90 s); HW, NT (thief rummage windows are AI) |
| EV23 | **observation.accumulated** | player, volume_id, unobserved_seconds | UC only: time the player's character spends **outside** an observation volume. No camera data. | UC S01 (≥ 30 s), S05 (≥ 90 s) |
| EV24 | **creature.split** | parent_instance_id, children[] | Drift dispersal at a flagged site spawns smaller variants downstream (depth cap 2). | MN S07 |
| EV25 | **player.died / player.respawned** | player, respawn_anchor_id | Not a progress event. Consumed by set-piece controllers to pause or reset (§8.3). | TF, DK, CR, NT, SV boss, WD, all boss resets |
| EV26 | **player.session_ended** | player | Not a progress event. Triggers carry returns, channel discards and set-piece logout rules (§8.2). | All |

### 2.3 Named script events (presentation; gameplay never reads their visuals)

| Event id | Quest / step | What the server must do | Client presentation (local) |
|---|---|---|---|
| `true_line.stone_holds` | TL S06 | Emit on `seat_post` completion | Water sheet climbs stone; audio duck; far-bank figure (frustum-gated) |
| (SM stone, A8) | SM S07 area K | Once per player on first entry to 4 m volume | Damp line at the notch (depot stone) |
| (HW dry footprints, B8) | HW S02c | Inspect-triggered | Prints that walk into water and come back dry |
| `night_flush.surge` | NF S02 | Emit at watch end; start barge path; emit end on fixed timer | Zone-wide duck, glass pool, thump, water-level rise, marker reading changes |
| `gl.backwater_dusk` / `gl.backwater_test` | GL S02 / S08 | Scripted windows | Water film, glisten line, warm-well steam; per-fix result |
| `tf.crew_scene` / `tf.pond_lag` | TF S04 / S08 | Window; then on S08 completion while in pond volume (else next entry) | Crew scene; reflection delay on the pond |
| (MN quieting, §MN.7) | MN S07 | After split; restart once on interrupt | Inward rings, mist, Sedge exhausted |
| `bf.curtain_hush`, `bf.pulse`, `bf.braids_sound` | BF S03, S06 | Threshold volume; Oriel action; valid gate order | Hush; silt thread down the Cut; Braid chord |
| `cr.sallow_yield` | CR S06 | On defeat at 0 HP (SX-2, EV08) | Hook dropped into the basin, chain grip |
| `cr.minute_read` | CR S08 | When C7 laid and read (or when Aldric reads the finding) | Water-gate duck ~6 s; ceiling ripple stops |
| `sv.fen_holds` | SV S07 | On seat-post at heart stone | Every loaded stone climbs/holds/releases; distant stones glint; fen-wide duck |
| `silent_bell.pull` | SB S07 | On SB-D4 end | Bell swings (world animation); river ring for requester only |
| `uphill_canal.seat` | UC S02 | On sit while unobserved; server end at loop point | Reflected climbing water in basin |
| `twice_burned.dream_start` / `_end` | TB S03/S04 | Start on eat; end on any of three exits (touch, boundary, ~6 min, or hostile within 15 m / damage) | Unburnt Flats dressing swap (§7 M23) |
| `whispering_door.creak` | WD S02 | On WD-D2 end, ~20 s before wave 1 | Two creaks; door moves; candle leans |
| `candle_rule.unwind` | CN S03 | Third board at worn band | Pool stops turning; offerings sink; boat crosses |
| `verse.channel` | VK S03 | Volume entry after MQ9 | Water plays the phrase near the riffles |
| `flood_carried.open` | FC S04 | Prise-lid interaction | Dry air; lid off |
| (FK hush) | FK S03 | First cooking completion | Geese stop; waterline climbs one step (kept per player) |

**Requirement:** each script event fires **once per player** unless marked repeatable (UC seat, WD creak on active nights, ME09 mist). "Once per player" is persisted (a seen-flag), so a logout cannot replay a once-only moment (TB rule: logout mid-dream marks S04 complete).

---

## 3. Quest content data requirements (Schema & Content Engineer, 31.3)

### 3.1 Quest definition record

| Field (requirement label) | Needed because | Examples |
|---|---|---|
| content id | Bible §11.2 suggests `lowmark.main.NN_slug` / `lowmark.side.slug`; SCE owns naming | `lowmark.main.01_true_line`, `lowmark.side.silent_bell` |
| code prefix | Flags and steps are prefixed by code | TL, SM, … ME01 |
| tier | main / side / micro-event; micro-events are lightweight but still persisted | ME01 persists `ME01_RULE` |
| unlock predicate | Every side quest and MQ2+ is gated on another quest's state | WC: `lowmark.main.01_true_line` Completed; UL: MQ4 Completed |
| offer trigger(s) | Volume entry, NPC bark, notice inspect, dialogue end of another quest | UC: canal foot volume **or** Bryn's bark |
| accept mode | `auto_on_offer` (TL, GL, WC, FK, TF) or `on_dialogue_end` (HW-D1) or `chained_from` (NF Active at HW-D10 end; RR at SV-D9 end) | §1.2 G05 |
| resume hook | §3.7 | — |
| can fail | **No such field.** No quest can fail and there is no failed or abandoned state (Stage 15.2; bible §11.4). | — |
| steps | §3.2 | — |
| flags | §3.5 | — |
| choice records | §3.8 | — |
| respawn anchors by step | §8.3 | NF: Cut mouth in the Lock |
| UI policy by step | objective text key, sub-counter template, `ui_suppressed` (strange moments) | NF S02 "none shown during it" |
| Director variant tags | Nodes and props tagged for swap: `[ANTAGONIST]`, `[D-7]`, `[D-8]` | bible §3.1 |

### 3.2 Steps

| Requirement | Detail | Examples |
|---|---|---|
| Ordered ids, scoped to quest | `S00_…`; the same id in two quests is distinct | SB `S00_offer` ≠ UC `S00_offer` |
| Objective text key + optional sub-counter | "(0/3)", "(1/3)" | CR S03, SV S02 "(0/7)" |
| Completion predicate | §3.3 | — |
| Kind | `required`, `optional`, `conditional` (required only after a choice), `branch` (exactly one of a set is active), `folded` (completes as part of a visible step; no own objective text) | conditional: WC S06a; branch: GL `S07_fix_circle/plot/dike`; folded: SM S06b, S07b |
| Parallel groups | Steps that may complete in any order, all required to pass the group | HW site A/B/C; NB S02–S04; UR S02/S03; TF optional preps |
| Availability window | Optional step available only from/until another step | TL S04b available from S02; TL leads available S01–S07 |
| Completion side-effects (declarative) | set flags, set region flag, write drift-site state, emit script event, start window, start encounter, change NPC placement set | HW S02a_drain → orchard pool quieted |
| Never regress | A step, once complete, stays complete (see §10 I-14 for the one package that regresses) | — |
| Persisted sub-progress | Per-step counters and per-object done-flags persist, so "completed segments are kept" survives logout | NF crank segments; SV gate %; NB faces rubbed; HW chops; UR digs |

### 3.3 Predicate vocabulary actually used

| Predicate | Meaning | Examples |
|---|---|---|
| `event(EVxx, match)` | One event matching fields | enter volume; dialogue end node |
| `count(EVxx, match) ≥ N` | N matching events (distinct targets unless stated) | TL S02 3 inspects; FK S04 4 gives; SV S02 7 arrivals |
| `n_of_m(set, N)` | N distinct of a listed set | GL S03 3 of 4; FC S02 4 of 5; UC S00 2 of 3; BF S04 3 of 5 |
| `ordered(list)` | Events in the listed order | OL S01 notched posts in order; GL circle branch (lift → open → clear → reset) |
| `all(…)` / `any(…)` | Conjunction / disjunction of predicates | TF S03 strap via anvil **or** 2 vice_lean; NF S10 smash ×3 **or** chain ×2; UL S01 four routes |
| `flag(name) op value` | Quest-local or region flag test (=, ≠, set, unset, ≥ for ints) | NF S01 count depends on `HW_LEAD_TALLY`; UR S04 dig count depends on `LM_FIELD_FIX = plot` |
| `quest_state(id) = state` | Another quest's state | VK S02 auto-pass on MQ9 Completed |
| `holds(item or category, qty)` | Inventory state, not an event | BP S02 "required amount of tannin-rich bark held" |
| `in_window(window_id)` | Inside a per-player time window | GL S02b; HW S02a |
| `while(state)` | Event counts only while a state holds | DK slip counted only during hold window; UC progress only while unobserved |
| `counter(name) op N` | Quest-local int threshold | CR S08 `CR_CHIPS_LAID ≥ 3`; FW withies ≥ 3 at wave end |
| `elapsed(timer) ≥ t` | Timer since a step or interaction | TB S05 60 s; CN S06 60 s |

**Requirement:** predicates are data, evaluated by a content-agnostic evaluator (15.2 §4, 15.3 §4). No per-quest code in the evaluator. Set-piece logic that cannot be expressed this way lives in a set-piece controller that *emits* EV19/EV20 (§11 D-INT-1).

### 3.4 Optional, conditional and guaranteed-path rules

| Rule | Requirement |
|---|---|
| Optional steps never gate | An optional step's absence must never leave a required predicate unsatisfiable. Validator check (31.6). |
| Optional steps close | Optional steps close silently when their availability window ends (TL leads close at S07). |
| Guaranteed proof | Every evidence predicate has a critical-path source (TL two proofs; MQ10 seven main-only chips; HW three core observations). Validator: for each required counter, sum the guaranteed sources ≥ threshold. |
| Conditional required | A `conditional` step becomes required only when its choice flag is set (WC S06a after `WC_SOW_TAKEN`; GL branch after `LM_FIELD_FIX`). |
| Skip-on-condition | A step may auto-pass when its condition is already met (VK S02 if MQ9 done; UR S04 one dig instead of three if `plot`). |

### 3.5 Quest-local flags

| Requirement | Detail |
|---|---|
| Types | **bool**, **enum** (closed value set), **bounded int** (counters). The packages use ints even though they are not called flags: `TF_MAX_BAND` 0–3, `DK_SLIPS`, `BF_WRONG_ORDER`, `NT_LOSSES` 0–3, `CR_CHIPS_LAID`, `CR_WEIGHT`, `SV_EVACUATED` 0–7, TL "proof +1". |
| Unset is a state | Every enum and bool distinguishes **unset** from any value. Dialogue reads "if set" (UC-D5 on `LM_SEDGE_TRUST`; TB variants). |
| Exactly-one groups | Side packages write enums as groups of mutually exclusive bools (`WC_SOW_TAKEN / _SPARED / _SPARED_FED`). Store these as **one enum per group**; keep the bool names as read-aliases so authored conditions stay searchable. Full list in §3.5.1. |
| Persist after completion | Quest-local flags of a **Completed** instance stay readable by other quests and dialogue (many cross-reads, §3.5.2). There is no abandon path, so flags are never discarded: an Active quest the player has left keeps its flags until it is resumed and completed. |
| Namespacing | Prefix = quest code. Region flags only from bible §9.1. ME flags `ME0n_`. |
| Write points | A flag is written by: a dialogue effect, a step side-effect, an interaction outcome, an inspect, or a set-piece counter. Validator: every read has at least one writer. |

#### 3.5.1 Exactly-one groups to model as enums

| Group (current bool names) | Values | Quest |
|---|---|---|
| `TL_EVIDENCE_KEEPERS / _RIVERFOLK / _PLAYER` | keepers / riverfolk / player | TL (also written to `LM_TL_EVIDENCE`) |
| `TL_STONE_PUBLIC / _KEPT` | public / kept | TL |
| `WC_SOW_TAKEN / _SPARED / _SPARED_FED` | taken / spared / spared_fed | WC |
| `BW_BANK_KEPT / _CUT / BW_LANDING_BUILT` | kept / cut / built | BW |
| `FK_POT_CREW / _FAMILY / _OWN` | crew / family / own | FK |
| `BP_HIDE_OWN / _YARD` | own / yard | BP |
| `BP_STRIPPED_BOUGHT / _REFUSED / _HIRED` | bought / refused / hired | BP |
| `HS_SALVAGE_KEEPERS / _REFUSED` | keepers / refused | HS |
| `UL_ENTRY_ERRAND / _PASS / _RIVER / _FORCE` | errand / pass / river / force | UL |
| `UL_LEDGER_GIVEN / _TAKEN` | given / taken | UL |
| `UL_RHOSYN_WITNESS / _GONE / _STAYS` | witness / gone / stays | UL |
| `NB_BOTH_CREDIT / _ALL_PAY / _WICKETT_CREDIT` | both / all_pay / wicketts | NB |
| `UR_GATE_RUN / _LINE_STAKED / _LEFT` | gate_run / line_staked / left | UR |
| `NT_BRACK_CUT / _WARNED`; `NT_FIRST_WORKERS / _HOUSEHOLD` | cut / warned; workers / household | NT |
| `FW_BED_SHARED / _ROUTE_KEPT` | shared / kept | FW |
| `OL_JOSS_IN / _LANTERN_ONLY` | joss_in / lantern_only | OL |
| `SB_KEEP_BOTH / _INTO_ROPE / _TO_FAMILIES` | both / rope / families | SB |
| `TB_GIFT_JORIC / _TREE` | joric / tree | TB |
| `WD_FLAP / _BRICKED` | flap / bricked | WD |
| `CN_FORM_WATCH / _CARRY` | watch / carry | CN |
| `VK_PERF_BOTH / _COUNT / _HUM` | both / count / hum | VK |
| `FC_OPENED / _TO_KEEPERS / _TO_HEDGE` | opened / keepers / hedge | FC |
| `SV_SERPENT_KILLED / _DRIVEN` | killed (driven is kept as an id but never set, CDR-1) | SV |
| `CR_SINGED_B1`, `CR_SINGED_B2` | (two independent bools; not a group) | CR |

Already enums in the packages: `HW_FIRST_DRIFT_SITE` (orchard/step), `MN_SAW` (water/you/mage), `CR_SALLOW_ACCOUNT` (none/lock/full), `CR_TERMS` (bare/firm/full), `CR_MARRICK_STORES` (offered/ordered), `RR_MARK` (notch/ring/hatch), `ME01_RULE`, `ME05_CUP`.

#### 3.5.2 Quest-local flags read by other packages (must survive completion)

| Writer | Flags | Readers |
|---|---|---|
| TL | `TL_STONE_*`, `TL_TOVIN_TRUSTED`, `TL_LEAD_NAN` | SM, TF, BF, ME08, VK |
| SM | `SM_LEAD_WYNN`, `SM_LEAD_STENCIL`, `SM_LEAD_CUT_NAMED`, `SM_STONE_SEEN`, `SM_CORVIN_TRUST` | NF, MN, BF, CR, RR |
| HW | `HW_LEAD_TALLY`, `HW_LEAD_SCRAP`, `HW_BRYN_MOSS`, `HW_DEN_CLEARED`, `HW_FEN_FIRST` | NF, CN, DK, GL, UR |
| NF | `NF_LEAD_CONVOY`, `NF_POSTS_SEEN`, `NF_LEAD_LAMB` | SV, CR, UL |
| GL / TF / MN | `GL_SEDGE_SPOKEN`, `GL_WELL_WARM`, `TF_KEEPERS_READ_BACKWATER`, `MN_SAW`, `MN_ELK_KILLED` | MN, DK, BF, RR, Act III |
| CR / SV / RR | `CR_TERMS`, `CR_MARRICK_STORES`, `CR_CREW_LENIENCY`, `CR_RHOSYN_LAID`, `CR_HAULED_CREWMAN`, `CR_TOVIN_STOOD`, `CR_HESKETH_SELF`, `SV_LESSA_ROUTE`, `SV_FED_EVACUEES`, `RR_MARK` | SV, RR, post-game props, commission giver |
| Side → main | `UL_LEDGER`, `UL_LEDGER_CUT`, `UL_RHOSYN_*`, `UL_OTTILIE_TOLD`, `NB_UNDERSIDE_OPEN`, `UR_*`, `NT_DAWN_SEEN`, `FW_GUIDE_ROUTE`, `FW_*`, `OL_*`, `CN_*`, `VK_*`, `UC_COMPLETE` | GL, DK, CR, SV, RR, BF |
| Side → side | `WC_BARNS_CLEARED`, `WC_SAW_ROWS`, `WC_SOW_*`, `BW_*`, `FK_NAN_TUNE`, `FK_HUSH_SEEN`, `SB_COMPLETE`, `SB_TO_FAMILIES`, `BP_KELL_PEG`, `HS_BRIGID_QUEUE` | UR, BP, SB, VK, ME01, HW, commissions |

### 3.6 Region flags `LM_*` (character-scoped)

**Scope:** stored on the character, not the quest instance (bible §9.1). Readable by any quest, dialogue, prop, NPC placement set and commission gate. **Write rule (recommended):** written at the step that sets it; no other quest writes it. Each quest has one instance per character and never restarts, so a region flag is never rewritten by a second run of its own quest. Validator: exactly one writer per flag.

| Flag | Type | Values (bible §9.1) | Values used in packages | Set by (package) | Read by | Notes / discrepancy |
|---|---|---|---|---|---|---|
| `LM_TL_EVIDENCE` | enum | keepers / riverfolk / player | same | TL D9 (bible: "from `TL_EVIDENCE_*`") | SM, NF, TF, CR (C1), RR | **TL package never writes it**; TL §9.2 has quest-local bools only. Add a TL D9 effect. §10 I-01 |
| `LM_GRAIN_ROUTE` | enum | escort / hold / split | same | SM S09 (`SM-D7`) | CR terms, RR far bank, Act II barks | Consistent |
| `LM_LOCK_STATE` | enum | smashed / chained | same | NF S10 | TF, CR (C5), RR | Consistent |
| `LM_FIELD_FIX` | enum | circle / plot / dike | same | GL S06 (`GL-D5`) | RR, UR (dig count, epilogue), field props | Consistent |
| `LM_TOVIN_CREDITED` | enum | named / unsigned | same | TF S09 (`TF-D8`) | CR (C6), RR | Consistent |
| `LM_FLUSH_CALENDAR` | bool | bool | true only | TF S09 | DK, CR | Always true after MQ6; CR authors a false fallback |
| `LM_BRYN_ROLL` | enum | commons / household | same | DK S06 (`DK-D7`) | CR roll wording, RR | Consistent |
| `LM_ORCHARD_LOSS` | enum | none / partial | same | DK S05 (from `DK_SLIPS ≥ 1`) | RR, orchard props | Consistent |
| `LM_SEDGE_TRUST` | enum | warm / cool | same; derived: cool if `MN_ELK_KILLED` or `MN_SAW = mage` | MN S08 | BF, SV, RR, UC-D5, TB | Readers test **set/unset** (UC, TB). Needs unset state |
| `LM_ORIEL_PROMISE` | enum | "3 values" → **canonical aloud / many_hands / return** | **Act II:** aloud / many_hands / return. **Act III:** promise_1/2/3 and "1/2/3" | BF (A2.5 says `S07_promise`; BF.9 says `S08_promise` / `BF-D6`) | RR | **Value names and setting step differ.** §10 I-02 |
| `LM_MARRICK_EXPOSED` | bool | bool | always true at CR completion | CR S08 | RR | "How exposed" carried by `CR_TERMS` |
| `LM_HESKETH` | enum | kept / stood-down | kept / stood-down (+ `CR_HESKETH_SELF`) | CR S09 | RR, Crestbridge Guard commission | Hyphen in a value; use `stood_down` in data. §10 I-03 |
| `LM_PLAN_ROUTES` | enum | (bible `LM_PLAN_*`, now replaced) route keeper | crews / keepers / shared | CR S10 | SV roles, RR lanterns, barks | **Canonical:** these two flags replace `LM_PLAN_*` |
| `LM_PLAN_MEMORIAL` | enum | (bible `LM_PLAN_*`, now replaced) memorial keeper | watchers / gardens / reedmere | CR S10 | SV Widow's Step station, endings | As above |
| `LM_FEN_ENDING` | enum | seal / tend / shared | same | SV S08 | Drift-site states, Stillwater presentation, NPC placements, RR, ME10, WD | Consistent |
| `LM_CIVIC_STANDING` | bool | bool | true | RR S06 | Four aspirational commission offers | Consistent |

**Not region flags but world gates the packages carry in quest-local flags (keep as is; readers must use them):** `NB_UNDERSIDE_OPEN` (route), `UC_CULVERT_OPEN` (shortcut), `FW_GUIDE_ROUTE` (MQ11 lane), Maelin's day crossing (TL completed) and night crossing (RR completed).

### 3.7 Walk-away and resume (no abandon)

The quest lifecycle is Inactive → Active → Completed (Stage 15.2). There is no Abandoned or Failed state and no transition back to Inactive, so a quest is never re-instanced. Leaving a quest is not a state change.

| Requirement | Detail |
|---|---|
| Walking away | The player can leave any Lowmark quest at any step. It stays **Active** with its persisted step, quest-local flags, region flags and quest items. Nothing is reverted. |
| No abandon action | The quest journal offers no abandon or reset. Every Active quest stays listed with its current objective. |
| Resume hook | Each quest declares where it points the player back. Default: **the original offer trigger** re-prompts with a resume line for the current step instead of the opening. Main quests MUST have one. |
| Missed moments | A time-, place- or step-bound moment the player missed must be re-offerable (repeatable watch, re-arming encounter or a later prompt), never lost permanently. Choices are recorded as outcome flags, never as a failed state. |
| Quest items | Kept while the quest is Active; acquire steps auto-pass if the item is already held (predicate `holds`). No duplicate grants. |
| Drift-site and prop state | Unchanged by walking away. |
| Resume hooks authored so far | TL: next landing approach. SM: granary-yard entry. HW: Lantern Post. NF: Lantern Post (Ansel). SB: tower square. **All other quests: not stated.** SCE defaults to "the original offer trigger" and lists exceptions. |

### 3.8 Choice records

| Requirement | Detail |
|---|---|
| Record per choice | quest id, choice id, option chosen, step, tick. Persisted with the instance; the flag write is the readable result. |
| One per player | Choices are always per player, including in co-op (two partners may route the grain differently). |
| Physical choices | Some choices are made by interactions, not dialogue (NF smash ×3 vs chain ×2; CR chip subset; GL branch steps). The record must accept an interaction outcome as the option. |
| Multi-part | Some choices set several flags at once (TF-D8: `LM_TOVIN_CREDITED`, `LM_FLUSH_CALENDAR`, `TF_KEEPERS_READ_BACKWATER`; CR-D10 two flags). |
| Refusal is not a resolution | UR-D6: an option that tells Joric what to do returns to the offers. Dialogue options can be non-resolving. |
| Gated options | Options visible only with an item or flag (`[player holds cooked food]`, `[SB_ROPE_ASKED]`, `OL_CALL_KNOWN`). |
| Derived values | `LM_SEDGE_TRUST` is computed from two inputs at S08; `CR_TERMS` from chip weight; `LM_ORCHARD_LOSS` from a counter. Schema needs derived-flag rules or an explicit effect at the step. |

### 3.9 Drift-site state (bible §9.2, D-6 **[DIRECTOR]**)

| Requirement | Detail |
|---|---|
| Store | Per character, per site id: `active` / `quieted` / `tended` / `closed`. |
| Ids | Use one id form for all: `drift.<site>` (Act II already uses `drift.drowsebank_race`). OL writes `old_lantern_bend`; WD and CN use quest flags (`WD_QUIETED`, `CN_OUTLET_QUIETED`) as the state. §10 I-12. |
| Sites (17) | orchard_pool, flats_ditch, widows_step, bramblelock_pool, drowsebank_race, orchard_dike, mantle_channel, stillwater_deep, stillwater_margins (+ remembrance channel), farmhouse_cellar, watergarden_outlet, old_lantern_bend, plus residual pockets by ending: seal_outer_a/b, tend_far_a/b, shared_boundary, shared_far (two to three exist per ending). |
| Writers | Step side-effects (HW S02a, NF S11, TF S10, MN S07, WD S07, CN S04, OL S07); MQ11 ending matrix (Act III §E.1.2) as a single bulk write keyed on `LM_FEN_ENDING`. |
| Readers | Encounter spawn rules (condition windows: dusk, after rain, flush nights before MQ4); presentation (fog, mist, softmoss state); NPC placement (Watcher patrols). |
| Condition windows | "Flush nights before MQ4" = per-player window keyed on `quest_state(NF) ≠ Completed`. |

---

## 4. Dialogue data requirements (31.5)

### 4.1 Shape the packages are written against

The cast file's format (`NODE SPEAKER: "Line." (stage note)` / `> [condition] "Player option." → NEXT {effect}`) is used by all seven dialogue sources. Node ids `<CODE>-D<n>.<nn>`; leads `<CODE>-L-<NAME>`; barks `<CODE>-B<n>`; refusals `CR-D8.R*`; household hooks `SM-H`.

| Element | Requirement |
|---|---|
| Dialogue | id, owning quest (or none for ambient), entry conditions, start trigger (NPC interaction, challenge volume, script event, step entry) |
| Node | id, speaker, line key, stage note (gesture only), conditions, effects, next |
| Option | text key, conditions, next, effects, `repeatable` marker (used options are hidden otherwise), `non_resolving` marker (UR-D6) |
| Speaker | NPC def id, role id (KEEPER, CREW, OLD WATCHER, KID A), or `NONE` for inspect/notice text |
| Line keys | Localization keys, never inline text in data |
| Tags | `[ANTAGONIST]`, `[D-7]`, `[D-8]` on nodes for search-and-swap |
| End / choice markers | Nodes flagged as end or choice for EV09 |

### 4.2 Condition types actually used

| Condition | Notation in packages | Examples |
|---|---|---|
| Flag set / unset | `[FLAG]`, `[not FLAG]` | `[TL_LEAD_ORDER]`; `[not HW_DRIFT_TAUGHT]` |
| Enum equals / in set | `[LM_GRAIN_ROUTE = hold]`, `[circle or dike]`, `[tend/shared]` | Act III endings; GL variants |
| Int comparison | `[BF_WRONG_ORDER ≥ 2]` | BF-D4 |
| Conjunction / disjunction | `[A and B]`, `[A or B]`, `[A and B and C]` | Act I |
| Item held (specific) | `[weathered_marker_post]` | TL D7 |
| Item category held | "player holds cooked food", "has a cutting tool", "has no cutting tool" | WC, FK, TL D5, CR fire-lines |
| Node seen | `[D1.10 seen]`, `[SM-D6.20 seen]`, `[NF-D9.05 seen]` | many |
| Inspect done | `[all three inspected]`, `[rotted stone inspected]` | GL, TF |
| Quest state | `[completed side quest OL]` | Act III |
| Step state | dialogue available "from S01 until S07" | TL leads |
| Set-piece state | `[wrong order]`, `[table sounding]` | BF |
| Director variant | `[D-7]`, `[D-8]` | Act II, D&M |
| Proximity | `[player within 5 m]` | Act I bark |
| Default | `[else]` | everywhere |

### 4.3 Effect types actually used

| Effect | Notation | Examples |
|---|---|---|
| Set bool / enum | `{set FLAG}`, `{set FLAG = value}` | everywhere |
| Increment counter | `{n+1}`, `{proof +1}`, `{proof +1; once only}` | TL D7, TF |
| Give item | `{give item}`, `{give smoke-pot if needed}`, loan-if-lacking | TL hatchet; SV smoke-pot; WC knife; BW axe; BP knife; HS tongs |
| Take item to NPC | `{take post, order → Hollis}` | TL D9; TF sheets → keeper; DK bowl → Bryn |
| Emit event | `{event: S0x complete}`, `{event: quest Completed}`, `{event: NF offered}` | all |
| Start set piece | `{event: hold window starts}`, `{event: walk-with starts}`, `{event: Hesketh escort begins}`, `{event: MN-E1 active}` | DK, MN, BF, CR |
| Unlock world object | `{unlock HILL GATE}`, `{watch bench active}`, `{… inspectable}` | SM, NF, HW |
| NPC behaviour toggle | `{rope assist on}` | HW-D8.02 |
| Make node available | `{Nan's N.40 becomes available}` | TL |
| Conditional effect | `{if FLAG: take item from Wynn → player}`, `{set CR_SALLOW_ACCOUNT = lock if not already full}` | TL, CR |

**Requirement (§1.2 G08):** effects that touch inventory, NPCs, props or spawns are **requests** executed by the owning system after the dialogue node commits. The dialogue system never mutates inventory directly (Stage 27, 16.3).

### 4.4 Barks, inspect texts and variant lines

| Kind | Requirement | Examples |
|---|---|---|
| Ambient barks | Keyed by place, step range and flags; repeat cooldown; positional audio | TL D0 argument loop; Lantern Post barks by `HW_SITE_*`; post-game barks by every `LM_*` |
| Combat barks | Keyed to creature ability or set-piece phase | Sallow whistles before each swing; FW Lessa calls tells ("Line!") |
| **Mimic barks** | Emitted from a creature's position using another NPC's voice lines | DK Mud Pipers in Bryn's voice; SV pipers in a cutter's voice |
| Challenge barks | Volume-triggered short dialogue that can branch | UL door-man |
| Inspect text | One line per inspect target, conditional variants, replace-default after a later quest | TL marker reading; UC inspects replaced after MQ9; GL guide-line stones |
| Knowledge-unlock inspects | A whole class of world objects becomes inspectable after a quest | TL crossing markers; MN Braid stones; WC crop damage; BW bank trees; FK flocks; BP bark; HS ring test; NB repair faces |
| Notices | Readable world text (dock notice, keepers' notice) | TF S00, DK S00 |
| Variant lines | Origin variant reserved (D-3: TL D1/D10, MQ12 farewell); flag variants everywhere | — |

---

## 5. NPC data requirements (31.2, 33.2, 35.1–35.3)

### 5.1 What every NPC definition needs

| Requirement | Detail |
|---|---|
| Identity | def id, display name key, role, voice set, canon status (CANON ANCHOR / NEW / role-based) |
| Placement sets | Positions keyed by `(quest, step range)` and by flags; plus schedule entries keyed by time window (Oriel at dawn and dusk; Tovin at ME08 "some visits") |
| Behaviours | idle, walk-to-point-and-use, follow, escort, walk-with (pace-match, wait at checkpoints), invulnerable, cannot-be-targeted, ally slow-aura |
| Interaction sets | Dialogue entries by step and flags (35.2) |
| Post-game sets | Placement and barks by `LM_FEN_ENDING`, `CR_TERMS × LM_HESKETH`, etc. (Act III §E) |
| Post-defeat NPC spawn | Only SX-1 Joss and SX-2 Sallow: the quest's on-defeat hook spawns the person as a non-hostile NPC (EV08). No hostile→neutral swap for ordinary enemies (CDR-1) |

### 5.2 Roster across all packages

Counts are distinct authored placement sets or schedule entries (estimate from packages; ±2). "Var" = flag-keyed post-game variants.

| NPC | Status | Packages | Placement sets (est.) | Special behaviour |
|---|---|---|---|---|
| Maelin Rowe | CANON | TL, NF, SV, RR, NT | 10 | Crossing interaction (day; night after RR) |
| Corvin Tath | CANON | SM, CR, HS | 5 | Spawns on HS S03 |
| Aldric Fenmere | CANON | SM (glimpse), CR, RR, NB | 5 | Glimpse actor |
| Lessa Mirepath | CANON | HW, SV, FW | 9 (+3 var) | Walk-with (FW S06); ally caller (FW boss) |
| Joric Fen | CANON | GL, RR, UR, TB, ME03 | 8 | Walk-and-use (UR paddle); TB dawn schedule |
| Annelise Reed | CANON | GL, SV, RR, CN, ME04 | 9 (+3 var) | — |
| Tovin Pell | CANON | TL, TF, CR, RR, ME08 | 9 | Witness at CR table if named |
| Hollis Avery | NEW (TL) | TL, CR, RR | 7 | — |
| Wynn Tarrow | NEW (TL) | TL, SM, RR | 5 | Drives lead cart (SM escort) |
| Nan Ferrin | NEW (TL) | TL, FK, VK, RR | 7 | Walk to dock edge (VK) |
| Dace | NEW (TL) | TL, NT, RR | 4 | Invulnerable lane holder (NT) |
| Ansel Corrie | NEW (TL) | TL, HW, NF, CR, SV, RR, OL, ME10 | 11 (+3 var) | Lectern patrol book |
| Edda Marrick `[ANTAGONIST]` | NEW | SM, CR, RR | 6 (+3 var) | Glimpse actor |
| Gideon Sallow `[ANTAGONIST]` | NEW | NF, CR, RR | 5 | Scripted escape path (NF); miniboss → defeated → scripted surrender (SX-2) → NPC |
| Bram Hesketh | NEW | SM, CR, RR | 7 (+2 var) | Escort at sprint pace, ignored by crew (CR S04) |
| Keeper-Lieutenant | NEW | CR, RR | 2 | Commission giver if `stood_down` |
| Sedge `[D-7]` | NEW | GL, MN, BF, SV, RR, UC, TB, ME09 (implied) | 11 | Walk-with (MN, BF); quieting channel; sits on UC seat as a hint |
| Oriel `[D-8]` | NEW | BF, RR, VK | 4 | Dawn/dusk schedule; operates flow-table gate |
| Bryn Ruddock | NEW | HW, DK, RR, UC (bark) | 6 | Hold state with slip (DK); per-player instance requested |
| Elspeth Quill | NEW | HW, DK, SV, RR | 6 (+3 var) | — |
| Ottilie Penner | NEW | DK, UL, RR | 3 | Vendor (economy) |
| Kell Ashby | NEW | BP, RR | 3 | Vendor with bounded intake; commission giver |
| Brigid Corliss | NEW | HS, RR | 3 | Forge vendor; commission giver |
| Aubrey Teague | NEW | NT, SB, VK | 4 | Invulnerable lane holder (NT) |
| Merrin | NEW | SB, VK | 4 | — |
| Tamsin | NEW | BW, SB, VK, ME01 | 5 | Escort-lite follow (BW); pulls bell rope |
| Rhosyn Lyle | NEW | UL, CR, RR | 6 | Follows player out (UL S04) |
| Imber Cobb | NEW | TF | 4 | — |
| Joss Garrow ("Old Lantern") | NEW | OL, SV, RR | 4 | Patrol path; miniboss → defeated → scripted surrender (SX-1) → follower |
| Rusk | NEW | NF | 0 (removed: CDR-1) | Crew boss creature only (NF-E3); fights to 0 HP; no NPC, no dialogue. Maelin names Sallow at dawn (T-1) |
| Orrin Tull | NEW | HW | 3 | Follows smoke ring; invulnerable; position checkpointed |
| Wenna Tull | NEW | HW | 1 | — |
| Mabry Gorse | NEW | HW | 1 | — |
| Wenna Hale | NEW | UR | 2 | Name clash with Wenna Tull (§10 I-15) |
| Ivo Teasel | NEW | FW | 2 | Escort group |
| Orla Wickett, Varley | NEW | NB | 2 each | — |
| Brack | NEW (named cutter) | NT | 1 | Enemy |
| Rhoda Hobb, Col Hobb | NEW | WD, ME07 | 3 each | Col follows and narrates |
| Maud Holt, Bet Holt | NEW | CN | 2 each | — |
| Amos, Hester, Jem Lark | NEW | FC, ME05 | 2 each | — |
| Carrows, Hobbs, Haskins (far-bank households) | NEW | SM, RR | 3 var each | Name clash: Hobbs (§10 I-15) |
| Role NPCs (keepers, crews, Watchers, cutters ×7, row-warden, winch-hand, charter officer, roll-keeper, road keeper, carrier, Sayer/Coombe elders, children, Pip) | role | all | — | Scheduled road keeper (FC); escort followers (NT, FW, SV) |

**Totals:** about 45 named NPCs (7 canon anchors, 5 from TL, ~33 new) and ~20 recurring roles; roughly **230 step- or flag-conditioned placement entries**, plus post-game variants from Act III §E. Each placement needs zone residency validity (Stage 19.4) at the step it applies.

---

## 6. Quest items, carry-state objects and loaned tools

### 6.1 Quest items against the Phase 1.5 budget (8–12)

| # | Item | Quest | Source → fate | Rules |
|---|---|---|---|---|
| 1 | `weathered_marker_post` | TL | Reeds (S03) → Hollis, Maelin, or player (D9) → MQ10 chip C1; MQ12 may give to keepers' hall | Non-droppable, non-sellable |
| 2 | `dispatch_order` | TL | Wynn (D7, if `TL_LEAD_ORDER`) → follows Choice 1 | As above |
| 3 | `marker_stem` | TL | Coppice gather (S05) → consumed by `seat_post` | Consumed |
| 4 | `SM_requisition` | SM | Chute floor (S07) → MQ10 chip C3 | Antagonist swap-layer seal text |
| 5 | `NF_bill_of_lading` | NF | Winding floor (S07) → MQ10 chip C4 | Swap-layer seal text |
| 6 | `tovin_floor_sheets` | TF | Tovin (`TF-D4`) → floor puzzle → keeper (S09) → record room → MQ10 C6 | **One item with seven page sub-states**, not seven items (TF.14 allows either; seven would break the budget) |
| 7 | `riverglass_bowl` | DK | Ottilie (S02a) → Bryn (S03) | Given away |
| 8 | `CR_board_minute` | CR | Hesketh (S04) → table chip C7 | Swap-layer seal text |

**Total: 8 of 8–12.** Side quests and micro-events: 0. Headroom: 4.

### 6.2 Carry-state objects (never enter inventory)

| Object | Quests | Return rule on drop / logout / leave area |
|---|---|---|
| Grain sacks, Nan's trunk | TL S08 | Back to the cart |
| Smoke-pot (set-down ring) | HW S02c | Last set-down point; Orrin to last ring |
| Circle stones (facing check), turf, dike stakes | GL S07 | Back to source; completed sections kept |
| Gate beam | TF S03 | Back to loft |
| Softmoss bundle, stake bundle | DK S02 | Back to source; rotten moss refused |
| Record bundles ×2 (smoulder timer), soaked sacks, pre-notched barge post | CR S03/S04/S08 | Logout in S04: keepers deposit unsinged; death: carried bundle back to room |
| Evacuee lantern string, heart-stone post | SV S02/S07 | Followers walk back to hut on death |
| Restitution sack | RR S01 | Back to source |
| Sacks ×2 | WC S04 | Back to heap |
| Crates | FK S01 | Discarded on logout |
| Bark armfuls ×3 | BP S01 | Back to reeds |
| Glass crate, crew ledger (light carry, survives combat) | UL | Ledger back to Rhosyn's desk |
| Rubbing cloth | NB | Winch-hand has another; faces kept |
| Seed basket | UR | Back to nest |
| Stolen bundles | NT | Back to bluff camp |
| Joss's lantern (lit, cannot go out) | OL | Back to bend |
| Gate paddle (no agility while carried) | UC | Back to hut |
| Fruit | TB | Back to fork / tree |
| Offering boat | CN | Back to pool lip |
| Hurdles ×3, tin case, seed sack | FC | Back to where it lay |
| Hurdles ×2 | WD | Back to source |
| Patrol lantern | ME10 | Back to post |

Carry rules (all packages): walk and sprint allowed; no agility while carrying (UC explicitly); carrying suspends auto-attack (HW); "light carry" flag for objects not dropped on damage (UL ledger). TL fallback applies everywhere: replace a carry with a "lift and stack" interaction chain at the source.

### 6.3 Loaned and reward tools (not quest items; item pass defines them, 36.2)

| Tool | Given by | Condition | Kept? |
|---|---|---|---|
| Crew hatchet | Maelin (TL D5), row-warden (UR) | Lacks a cutting tool | Kept |
| Hunter's field knife | WC eldest (`WC-D6`) | Lacks a recovery tool | Kept |
| Hunter's short bow and a bundle of arrows *(names are proposals for the economy pass)* | WC eldest (`WC-D6.12`, optional, CDR-2) | Player chooses to borrow it for the sow hunt (`S06a_hunt`) | Returned at `WC-D7.12`; arrows used are not returned; no stats here |
| Bank axe | BW upper household | Lacks a cutting tool | Kept |
| Yard knife | Kell (`BP-D4`) | Lacks a Leatherworking tool | Kept |
| Forge tongs | Brigid (`HS-D1`) | Lacks Smithing tools | Kept |
| Watcher smoke-pot | SV-D2 (loan), kept at SV completion | Always | Kept (tool with uses per fill) |
| Amos's hatchet | FC | Lacks a cutting tool | **Returned** |
| Spades, pry bar, maul, chain, hook-pole, pole | GL, NF, TB, VK | World props | Not items |

Requirement: a **loan-if-lacking** effect that checks an item category ("cutting tool") and grants one tool once per character, so a player who completes UR after TL never holds two loaned hatchets.

---

## 7. Mechanics catalogue

Each row: who uses it, the minimum viable implementation (MVI) and the fallback the packages authored. Rows marked **[DIRECTOR]** are collected in §11.

| # | Mechanic | Quests | Minimum viable implementation | Fallback |
|---|---|---|---|---|
| M01 | Inspect with conditional text | All | Interaction kind `inspect` → EV02 + one line key; variants by flag/step | — (required) |
| M02 | Channelled interaction | All | Server timer, fixed duration (2–6 s), cancel on move or damage | Instant interaction with a fixed animation lock |
| M03 | Segmented channel under attack (completed segments kept; waves between segments) | NF crank (3 × 5 s), CR drop_gate, SV crank add-on | Segment index persisted in step sub-progress; waves keyed on segment start | Single channel; damage pauses instead of cancels |
| M04 | **Keep-watch / time advance** (wait to dusk, night, dawn, pulse; lantern-fill steps; sleep until bell) | HW, NF, GL, TF, DK, MN, BF, CR, SV, RR, UL, NT, OL, TB, WD, CN, MEs | Per-player **quest clock**: a cancellable interaction moves the player's window state to the next named window and starts its spawns and lighting profile. Server-authoritative; presentation local; no world time change. | Single "wait until X" interaction with a lighting swap; UL grate always cranked |
| M05 | Carry state | ~30 objects (§6.2) | Toggle carried-prop state on the player; deposit volumes; return-to-source on drop/logout/area exit | TL lift-and-stack interactions |
| M06 | Smoke ring (carried set-down ring that drift will not path into) | HW S02c | Carry object; set-down creates a 4 m volume excluded from drift navigation | Three pre-placed smoke stakes lit by interaction; Orrin walks stake to stake |
| M07 | **Trance / smoke follower state machine** (warning → turning → walking → standing; smoke channel within 4 m; 3 uses per fill; refill racks) | SV S02 | Follower NPC + 4-state FSM driven by authored trigger volumes on the lanes; smoke-pot as tool with charges | Lead-out by hand from any state (3 s channel); trances only at fixed points, one at a time |
| M08 | Follow / escort / walk-with NPC | HW Orrin, CR Hesketh, MN/BF Sedge, BW Tamsin, NT, FW, OL Joss, SV ×7, ME10 | Follow-the-player with wait-at-checkpoint; invulnerable; ignored by enemies | NPC waits at checkpoints only; NPC walks to destination on dialogue end |
| M09 | Re-forming creature (drift disperse and re-form while site condition holds) | HW, NF, TF, DK, CN, WD, MN | On defeat: despawn, re-form timer, respawn at anchor while site state is `active` | Fixed extra wave |
| M10 | Drift split (dispersal spawns two smaller drifts downstream, depth cap 2) | MN S07 | Spawn rule at a flagged site linked to downstream points | Two pre-placed smaller drifts appear on dispersal |
| M11 | Drift-site state driving spawns | §3.9 | Character-scoped state store read by spawn rules | Shard-level state (first player to quiet a site quiets it for the shard) |
| M12 | Encounter pockets, waves, step-gated spawns | All combat | Step-entry spawn; wave spawner bound to a volume; despawn after step | — |
| M13 | **Herding** (alert radius ~8 m, flight away from player; reset when calm) | MN S04 elk; DK elk charge | Reuse Hunting F4 alert-and-flight; quest-spawned instance | Partner's attack counts only for that partner |
| M14 | Observation-volume puzzle (progress only while the player is *outside* a volume; time accumulates) | UC | Per-player accumulated time outside a volume → EV23; presentation state rest/climbing; level art must hide the channel from every point outside the volume (load-bearing ZN requirement) | Pre-baked reflection texture in the basin keyed to state |
| M15 | Ordered-slot puzzle with validator returning first contradiction | TF S06 | Seven slot interactions accepting one page sub-state each; validate interaction returns a text key; third wrong check unlocks Imber hint | Per-player UI list over the same floor |
| M16 | Set-piece state machine: gate band 0–3 with NPC pry channel and far crank | TF S08 | Integer band; inputs pawl seated/free, far-crank alive, wind-down channel; tick timer | — (no-fail by design) |
| M17 | NPC hold with slip trigger (hit or lunge inside 2 m → 5 s slip, flood decal) | DK S05 | NPC flag `holding`; slip event; counter `DK_SLIPS` | — |
| M18 | **Quest on-defeat hook (CDR-1)**: quest on-defeat hook for named creatures (SX-1, SX-2) that plays a scripted outcome and spawns the NPC non-hostile | OL Joss (SX-1), CR Sallow (SX-2) | Hook on the creature definition or encounter: on 0 HP, play the authored outcome and spawn the NPC (EV08) | Ordinary defeat, then the NPC is placed at the spot by the step's NPC placement set |
| M19 | Gate progress with crew channel, harass pause, decay while a flagged creature is in volume | SV S03–S05 | Per-player progress bar; NPC tick rate; player crank doubles; serpent-in-volume decays | Per-player progress, shared enemies |
| M20 | Evidence-chip table (deposit volume, per-chip validity, weight, singe, clauses, refusals) | CR S08 | Data list of chip ids with source conditions, holder, weight, singe flag, clause; deposits increment `CR_CHIPS_LAID` / `CR_WEIGHT`; non-chips draw a refusal line | Chips laid by dialogue with the holder; only the speaking holder's prop appears |
| M21 | Smoulder timer on carry objects | CR S04 | Per-object timer from volume entry; on expiry sets singe flag and moves object to yard; pauses while player dead; never on logout | — |
| M22 | Flow-table model (per-player prop state: pulse, plug, three gates in order, reset) | BF S06 | Prop state machine with three ordered gates; valid order → `bf.braids_sound`; wrong order → reset with Oriel line | Looping pulse/braids presentation for anyone; only owner's interactions advance |
| M23 | **Dream presentation layer** (bounded per-player swap of Ashen Flats dressing, inspect disabled, dreamer aggro immunity, three exits) | TB S04 | Client-side dressing swap in a bounded area for the owning player; server holds `dreaming` state for aggro immunity and exits | 60 m ring around the tree |
| M24 | Per-player time-limited water presentation (sheet climb, reflection lag, fold around NPC, inward rings, pond lag) | TL, HW, NF, GL, TF, DK, MN, BF, SV, FK, ME08 | Client effects keyed to EV15; no gameplay reads them | Audio duck only |
| M25 | View-dependent local effect (only if in frustum) | TL far-bank figure, SB river ring, ME08 | Client checks own camera; never replicated | Omit |
| M26 | Pathed vessel / moving prop with wait point | NF barge (spline, waits at sill), NB platform (rail stops), NT Brack's skiff | Prop on a spline; no player collision | NB: fixed scaffolds and ladders |
| M27 | Trail-clue volumes re-pinning objective | NF S03 | Enter-volume events that change objective text | — |
| M28 | Unreachable scripted actor | NF Sallow escape | Path to skiff, no combat definition | — |
| M29 | Traps (armed/disarmed, trigger volume, telegraph, damage/stagger/root) | SM, UR, TB | One generic farm-tool trap with four presentations; inspect reveals and offers disarm | — |
| M30 | Hazard volumes with telegraph (heat zones, fire-lines as blockers, shard lane, tower falls, timed ground hazard, ash cloud) | SM, CR, HS, SB, UR | Damage/slow volumes with a lead-in glow | — |
| M31 | AI targeting props or NPCs (withies, carts, lanterns, crew winch, gate pawl, Bryn) | FW, NT, WD, CR, SV, TF, DK | Target-a-prop behaviour in decision framework | Enemies target the player; prop state changes on enemy defeat |
| M32 | Lantern props: extinguish, relight; lit lane blocks AI | NT, WD, CR (Sallow rope cut), SV racks | Breakable light + relight interaction; lit-volume path cost | Lit posts cause hesitation only |
| M33 | Forced movement (tongue pull 3 m, knockback, drag tether, mat slide, shove into basin and wade out) | NB, FW, UL, NT, CR, SV, OL | Server-side forced move per tick; ground-zone tags (stake, mat, shallows, footing) negate | Damage pulse instead of displacement |
| M34 | Status effects: chilled (slow 4 s), rooted 2 s, knockdown 1 s, latch | SV, UR, CR, TL leech | Combat status set | Damage only |
| M35 | Boss phase checkpoints (reset to top of phase died in); full reset if no engagement | SV Muster; SM Sack-King, CR Sallow, OL Joss, FW serpent (full reset) | Per-creature checkpoint; for shared creatures, see §8.1 rule | Full reset |
| M36 | Muster drag + reading stones (3 of 8 stones near moving inflows "read true" per drag) | SV S06 | Tether toward centre; stone volumes flagged by inflow proximity; reaching one breaks drag and staggers boss | Drag becomes a damage pulse broken by any stone |
| M37 | Fen-wide simultaneous stone presentation | SV S07 | One server event; every loaded authored stone plays locally; distant stones as glints | Nearest five stones only |
| M38 | Crossing interaction (ride across water) | TL reward, NT S06, RR S05 | Interaction that moves the player along a fixed route to a far-bank volume | Fade-free teleport with bow-lantern prop |
| M39 | Mimic voice barks from creature position | DK, SV | Bark from creature emitter using another NPC's lines | Generic piper calls |
| M40 | Station-bound crafting with authored outcomes | FK, BP, HS (`quench_suspect` always cracks), TF strap, WD anvil-stone | Station binding; authored-outcome interaction independent of skill rolls | Crew-repair channel instead of Smithing |
| M41 | Hunting approach / resolve / recover; flock alert and resettle; closed ground | WC, FK | Hunting interaction pass hooks | — |
| M42 | Vendors with bounded intake; opportunity states (open / closed / closed-until) | BP, HS, WC, FK, DK | Economy pass | — |
| M43 | Agility triggers | TL, NF, GL, NB, UL, OL, SB, UC, TB, BF | Phase 1.3 trigger boxes | Walkable route always authored |
| M44 | Per-player persistent prop / terrain state | Almost all | §8.1 | Package fallbacks |
| M45 | Per-player instanced NPC/creature (owner-visible) **[DIRECTOR]** | DK Bryn, HW Orrin, MN elk, SV evacuees, BF Sedge, WC sow, Muster visibility after S06 | Owner-visible entity flag in replication filter | Shared entity; credit to all; dialogue reads each player's own state |
| M46 | Unkillable ally NPCs | NT Teague/Dace, FW cutters, SV crew | Damage-immune flag | Allies stand as blockers |
| M47 | NPC scripted walk-and-use under player camera | UR Joric, BF Oriel, MN/SV Sedge | Move to point, use animation, EV18 | Sound fade; NPC shown at end position |
| M48 | Voice-volume decoy (player entered wrong place) | DK `DK_FOLLOWED_VOICE` | Enter-volume event | — |
| M49 | Performance with player-paced pins (song waits for player) | VK S05 | Crowd vocal loop; 4 pin interactions; loop last line until pulled | World event any partner's S05 completes on |
| M50 | Restorative waypoint (meal once per visit; respawn binding) | WD Hobb hearth, HW Lantern Post | Interaction + per-visit cooldown | Omit |

**Bible §8 says "no new core system is introduced."** That holds for most rows. It does not hold cleanly for M23, M29-style set-piece controllers (M16, M17, M19, M20, M22, M36), M45 and the D-6-dependent M09/M11: see §11.

---

## 8. Per-player presentation, co-op, persistence and death

### 8.1 Per-player presentation and co-op rules (binding across packages)

| Rule | Requirement |
|---|---|
| Ownership | Each player has their own instance of every quest (15.1). There is no group quest state. |
| Shared creatures, shared credit | World creatures are shared. A defeat credits every participant whose **own** active step consumes it (EV07 `credited_players`). |
| Per-player outcomes | Choices, counters (slips, bands, losses), chips, flags and endings are per player, even when partners stand together. |
| Per-player props | Props, terrain decals, water planes and NPC placements keyed to quest state render from the **local** player's state. Partners see their own world. |
| Per-player strange moments | Script events play for the owning player only, on their own trigger (TL discovery; SB ring; TB dream; SV fen hold). Partners see only world-level motion (bell swings). |
| Set-piece timers | Set-piece state (TF band, DK hold, SV gate %, CR smoulder, NT watch) is per player. Shared creatures keep fighting; pauses apply to the owner's timer only. |
| Shared boss, per-player checkpoint | A shared boss resets to the checkpoint of the **lowest-progress** participant still engaged; a player who completed the boss step no longer sees it (SV) only if M45 exists; otherwise it remains visible but gives them no credit. SE to confirm. |
| Fallback (TL §12) | Where per-player presentation is not ready, each package names a shard-level fallback (first player's result shows for all; others' state lives in dialogue/barks). The fallback must still give each player their own flags. |
| Known conflict | NT says "a partner's lanterns light for both players (shared world props)", against the per-player prop rule. §10 I-16. |

### 8.2 Persistence and logout/resume

Baseline (all packages; Stages 13/15): restore the last persisted step and flags; discard in-progress channels and carries; carried objects return to source. Exceptions below require **persisted sub-step progress** (§3.2), which Stage 15.1 ("runtime-only state discardable") allows only if it is written as quest state at commit points.

| Quest / step | Logout rule authored | Requirement it implies |
|---|---|---|
| HW S02c | Orrin restores to his last ring; chops persist | Follower checkpoint position persisted |
| NF S03 | Restore to S03 at the weir; barge waiting at sill; clues pre-revealed | Step-entry state, not mid-path state |
| NF S08 | Crank segments persist | Segment index persisted |
| GL S05/S07 | Resume at entry shaft; completed sections stay | Per-object done flags |
| TF S06 | Sheets return to inventory; bays clear | Puzzle state discarded |
| TF S08 | Pulse restarts at phase 1 with full crew; repairs, sheets kept | Set piece restarts at step entry |
| DK S05 | Hold restarts at wave 1; `DK_SLIPS` reset to value at last completed wave | **Wave checkpoint counter** persisted |
| BF | Inside the Steps resume at curtain ledge | Respawn/resume anchor by step |
| CR S04 | Bundles not deposited are deposited by keepers, unsinged | **Logout completes part of a step** (§10 I-14) |
| SV | Delivered evacuees stay delivered; gate progress per gate persists; Muster restarts at 100% | Counters persisted; boss not checkpointed across logout |
| RR | Lanterns lit stay lit | Per-object flags |
| UL S04 | Ledger returns to desk and **step resets to S03** | Step regression (§10 I-14) |
| NB | Faces rubbed stay rubbed | Per-object flags |
| NT | Restores the last completed watch | Watch index persisted |
| OL S06 | Restart S06 with Joss at the bend, already surrendered (SX-1) | Post-defeat NPC state persisted |
| UC | Steps and latched props persist; float resets if S01 incomplete | Per-player latched prop state |
| TB S04 | Logout mid-dream: S04 complete on login, player at the tree at first light | Once-only moment marked on start |
| WD | Night restarts from S02; drain restarts at the grate | Step-entry restart |
| VK S05 | Performance restarts from verse one | Step-entry restart |

### 8.3 Death and recovery

| Requirement | Detail |
|---|---|
| No quest failure | Death never fails or regresses a quest. Steps, flags, quest items and persisted sub-progress are kept. |
| Respawn anchor by step | Each quest names a safe point, sometimes per step: TL crew fire; SM undercroft bays; HW site anchors (berm shrine, field gate, Reedmere porch); NF Cut mouth; GL top of shaft; TF mill yard; DK Sluice Shelter; MN shrine step; BF area A; CR Keepers' Yard; SV vigil fire / Reedmere / Lantern Sluice landing; WC field gate; BW bank-top; FK shelter; BP yard gate; HS forge mouth; UL Ottilie's yard; NB crew stair; UR net bench; NT ring fire; FW warning post; OL Lantern Post; SB tower square; UC listening seat; TB remembrance circle; WD hearth; CN pool bench; FC field gate. Needs a step-keyed respawn override (§1.2 G27). |
| Set piece on death | TF hold resumes at current state, pulse timer paused while dead. DK hold pauses until re-entry. CR carried bundle returns to room; smoulder pauses. NT current wave continues. WD current wave restarts, dispersed waves stay dispersed. SV followers walk back to huts. |
| Boss on death | Sack-King, Sallow, Joss, Deep-Pool Serpent reset to full (serpent only if nobody engaged 30 s). Muster resets to top of the phase the player died in; adds clear; gates stay open. |
| Lethality | No instant kills. Muster "Pulled Under" 35% max HP; HS shard cannot kill above 25%; SB falls drop one landing; BF walkable routes cannot kill. |
| Followers | Escorted NPCs cannot die, drown or be lost (Orrin, evacuees, Joss, Tamsin). |

---

## 9. Recommended build order beyond *The True Line*

Precondition: **M0 = TL slice** per TL §12.3–12.4 (steps + flags, minimal dialogue, inspect/channel, encounter pockets, carry or fallback, quest persistence). Everything below assumes M0 passes its acceptance test.

The shortest dependency path to a playable Lowmark slice is **Act I in order (MQ2 → MQ3 → MQ4)** plus side content that reuses only what Act I builds. Act I exercises every high-frequency contract (region flags, cross-quest reads, quest items, drift-site state, time windows, follower, segmented channel) while avoiding the expensive Act II–III set pieces.

| Milestone | Content | New contracts it forces (beyond M0) | Depends on |
|---|---|---|---|
| **M1 — Chain** | MQ2 *Short Measure*; FC *What the Flood Carried*; ME01, ME02, ME05, ME08 | Region flags (`LM_TL_EVIDENCE`, `LM_GRAIN_ROUTE`); quest-state predicates and unlocks; quest item with inspect; cross-quest flag reads after completion; resume hook; multi-level NavMesh (depot); traps (M29); elite reset; per-player cart props or fallback | 24.1–24.4, 31.1, 31.3, 31.5 subset, 33.1.B |
| **M2 — The water** | MQ3 *Heavy Water*; ME10; optional FK if the Cooking station and Hunting hooks exist | Drift-site state + re-form (M09, M11; **needs D-6 ruling**); dusk window via keep-watch (M04); smoke ring (M06); follower with checkpoint (M08); parallel step groups; synthesis dialogue with counters | M1; 33.7; D-6 |
| **M3 — Act I turn** | MQ4 *The Night Flush*; UL *Under the Lamb* or NT *Night Ferry* | Watch steps (EV14); zone-wide script event (`night_flush.surge`); pathed vessel (M26); trail clues (M27); segmented channel (M03); ordinary defeat (I-05 ruled, CDR-1); physical choice by interaction | M2 |
| **M4 — Act II core** | MQ5, MQ6, MQ7 (+ UR, WD, CN) | Set-piece controllers M16, M17 (**D-INT-1**); ordered-slot puzzle (M15); carry facing check; wave checkpoints persisted; mimic barks; AI targeting props/NPCs (M31) | M3; D-INT-1 |
| **M5 — Act II turn** | MQ8, MQ9 (+ UC, SB, VK) | Herding (M13); drift split (M10); walk-with (M08); flow-table (M22); observation volume (M14); per-player instanced creature or fallback (M45) | M4 |
| **M6 — Act III** | MQ10, MQ11, MQ12 (+ OL, FW, NB, TB) | Evidence table (M20); smoulder (M21); on-defeat hook (M18, SX-2; also OL SX-1); Muster (M35–M37); trance FSM (M07); gate progress (M19); ending matrix bulk writes; post-game placement sets; dream layer (M23) | M5 |

### 9.1 Acceptance tests per milestone

| Milestone | Acceptance tests (all on a fresh solo character unless stated) |
|---|---|
| M1 | 1. MQ2 is not offered before TL completes, and is offered on granary-yard entry after. 2. Each of the three `LM_TL_EVIDENCE` values produces the matching `SM-D1` opening. 3. Each `LM_GRAIN_ROUTE` value is reachable and persists across logout. 4. `SM_requisition` cannot be dropped or sold and survives death in the depot. 5. Logout mid-dungeon resumes at the hill gate with earned shortcuts. 6. Dying to the Sack-King resets him to full and keeps all steps. 7. Leave MQ2 mid-quest, travel away and re-enter the yard: MQ2 is still Active at the same step, the resume prompt plays, and the requisition is not granted twice. 8. FC and four micro-events complete using only M0 contracts; `ME01_RULE` and `ME05_CUP` persist. 9. Two-player co-op: both complete MQ2 with different grain routes and each sees their own result (or the fallback bark). |
| M2 | 1. Sites A, B, C complete in all six orders; `HW_FIRST_DRIFT_SITE` and teaching line follow. 2. Orchard pool drift re-forms until the lever, then never spawns again for that player. 3. Arriving in daylight and hauling the lever early still sets `HW_DRIFT_TAUGHT` by a fallback line. 4. Orrin cannot be lost; lapsed ring makes him stand; logout restores his last ring. 5. Synthesis reaches `HW-D10.90` with zero optional leads. 6. A partner who has not drained their pool still sees and fights their own drift (or the shard fallback completes their step on entering the drained-pool volume). |
| M3 | 1. Watch takes one step with `HW_LEAD_TALLY`, two otherwise; standing cancels and resumes. 2. No UI appears during `night_flush.surge`. 3. Falling behind the barge never fails; the barge waits at the sill. 4. Crank segments survive damage, death and logout. 5. Sallow cannot be reached or killed. 6. Rusk fights to 0 HP with the ordinary defeat; Sallow's name comes from Maelin at dawn, never from a defeated enemy. 7. Smash and chain each set `LM_LOCK_STATE` and the matching prop (or fallback). 8. Bramblelock pool is quieted at dawn. 9. All Act I acceptance tests in the Act I file pass end to end. |
| M4 | 1. MQ5 and MQ6 complete in either order with correct cross-lines. 2. TF validator returns a contradiction for every wrong order tested; three wrong checks trigger Imber. 3. TF hold reaches band 3 at worst and never fails; death mid-hold resumes at current band with paused timer. 4. DK reaches `LM_ORCHARD_LOSS = none` and `= partial`; logout mid-hold restores slips to last completed wave. 5. Every `LM_FIELD_FIX` value reachable; UR outcome changes GL's plot option without removing it. |
| M5 | 1. `LM_SEDGE_TRUST = cool` by elk killed and by "mage"; `warm` otherwise; MQ9 offered in all cases. 2. Drift split caps at depth 2; interrupting the quieting twice still finishes. 3. Flow-table wrong order resets without limit. 4. UC float moves only while unobserved; standing on the lip never advances it; culvert stays open thereafter. 5. Each `LM_ORIEL_PROMISE` value reachable and persisted under one canonical value set (I-02 resolved). |
| M6 | 1. Main-only play yields seven chips and `CR_TERMS ≥ firm` with every bundle singed. 2. Refusing Sallow's terms still exposes Marrick. 3. Logout in CR S04 never singes. 4. Every MQ11 trance resolves; no follower can drown. 5. Gate 2 progress decays only while the serpent is at the sill. 6. Muster death resets to phase top; logout restarts at 100%. 7. Each `LM_FEN_ENDING` writes the §E.1.2 drift-site table exactly. 8. `LM_CIVIC_STANDING` set at RR S06 and all four commission offer lines play. 9. Two-player co-op completes MQ10–12 independently with different endings. |

---

## 10. Inconsistencies found across packages

| # | Area | What differs | Where | Recommended canonical choice |
|---|---|---|---|---|
| I-01 | Flag write | Bible §9.1 says `LM_TL_EVIDENCE` is set by MQ1 "from `TL_EVIDENCE_*`"; Act I reads it; the TL package (§9.2) never writes it | Bible §9.1; TL §9.2; Act I header | Add `{set LM_TL_EVIDENCE = keepers/riverfolk/player}` to the TL `D9` evidence option. Keep the TL bools as aliases |
| I-02 | Flag values and step **(canonical per fix pass)** | `LM_ORIEL_PROMISE` = aloud / many_hands / return (Act II) vs promise_1/2/3 (Act III §0.2, §12.11, §E.2). Setting step `S07_promise` (Act II §A2.5) vs `S08_promise` / `BF-D6` (BF.9) | Act II, Act III | **Canonical: aloud / many_hands / return.** Setting step `S08_promise` (`BF-D6`); fix A2.5 if the fix pass has not |
| I-03 | Enum value format | `LM_HESKETH = stood-down` uses a hyphen | Bible, Act III | `stood_down` in data; prose may keep the hyphen |
| I-04 | Chip C8 and Rhosyn **(canonical per fix pass)** | UL makes the chip **the crew ledger** (`UL_LEDGER`, weakened by `UL_LEDGER_CUT`; Rhosyn attends only if `UL_RHOSYN_WITNESS`) and asks Act III to use those flags. Act III's C8 is **"Rhosyn's forged papers", held by Rhosyn in person**, gated on "completed side quest UL", and sets `CR_RHOSYN_LAID`; MQ12 says `CR_RHOSYN_LAID = false` → "she's in the cellar", which contradicts UL options *gone* (left downriver) and *witness* (with the keepers). Bible §6.1 says "Rhosyn's forged papers" | UL.11; Act III §10.5.2, §E.2; bible §6.1 | **Canonical:** C8 = crew ledger, available if `UL_LEDGER`; weight 2, −1 if `UL_LEDGER_CUT`; Rhosyn present as witness only if `UL_RHOSYN_WITNESS`. Key MQ12's Rhosyn scene on `UL_RHOSYN_*`, not on `CR_RHOSYN_LAID`. Update bible §6.1 wording |
| I-05 | Human defeat rule | Earlier packages: Smugglers **downed** at 0 HP; Joss **yields** at 0 HP; Sallow yields at **20%**; Rusk "has yielded"; "defeated humans kneel and are tied" | S&C, Act III §10.13, Act I §C12 | **Resolved 2026-11-03 by CDR-1.** Every enemy is defeated at 0 HP; no yield mechanic, downed state or tied props. SX-1 Joss and SX-2 Sallow use the quest on-defeat hook (M18, EV08). |
| I-06 | Item custody: `SM_requisition`, `NF_bill_of_lading` **(canonical per fix pass)** | Act I: both "kept by the player to MQ10", no branch hands them to keepers. Act III bundles 1/2 contain them "if Act I left it with the keepers" | Act I §Quest-item budget; Act III §10.4 Beat 3, §10.5.2 C3/C4 | **Canonical:** the player holds both until MQ10. Remove the keeper-custody branch from Act III bundles; chips C3/C4 are laid from inventory |
| I-07 | Item custody: `tovin_floor_sheets` | Act II: given to the keeper at S09 under both options and held in the record room. Act III: named → "Tovin, in person"; unsigned → bundle 2 | Act II §A2.6; Act III C6 | Sheets always in the record room (bundle 2). `named` adds Tovin as a present witness and full weight; `unsigned` lays the sheets alone |
| I-08 | Smoke-pot | MQ3: carry-state object from the Step's stake box. OL: "a bundle of banner-thistle smoke… carried Watcher tool, reusable for this quest". MQ11: loaned tool with 3 uses per fill, kept as a reward tool | Act I §B6; S&C OL.3; Act III §11.4, §11.11 | One tool, `watcher_smoke_pot`, defined by the item pass: carry-and-set-down use in MQ3 (loaned for the quest), channel-at-target use with charges in OL and MQ11, kept from MQ11. Not a quest item |
| I-09 | Joss's lantern | OL: with `OL_JOSS_IN` Joss puts the lantern out and comes home (hook stays empty); with `OL_LANTERN_ONLY` the lantern hangs at the Post. Act III reads only "completed side quest OL" and always has Ansel hang Joss's lantern at the fen edge; MQ10 refuses "Joss Garrow's lantern" laid as a chip | S&C OL.7; Act III §0.3, §10.5.3, §E.1.1 | Branch Act III on `OL_JOSS_IN` / `OL_LANTERN_ONLY`. In `joss_in`, Joss brings his unlit lantern to the edge himself (or Ansel hangs it unlit). MQ10 refusal fires only if the player holds or carries it |
| I-10 | Candle Rule boat | CN offers two forms (watch / carry). Act III reads only "completed side quest CN" and always moors the boat at the landing and launches it in Tend/Shared | D&M §5.9; Act III §0.3, §E.1.1 | Key Act III on `CN_FORM_*` as CN §5.9 requests: watch → Maud sits with her light at the channel; carry → launched boat |
| I-11 | Keep-watch semantics | MQ4: per-player **presentation** hour, no world time; HW: "dusk tick while in volume" with world-time fallback; D&M §0.4: completes "when the world clock enters the window", local fallback; UL: "server time-of-day check" | Act I, Act II §A2.10, D&M §0.4, UL.10 | One contract: **per-player server-side quest clock** set by the watch interaction (§7 M04). World clock may later drive it; content never assumes one |
| I-12 | Drift-site ids and state ownership | Act II `drift.drowsebank_race`; OL `old_lantern_bend`; WD `WD_QUIETED` and CN `CN_OUTLET_QUIETED` used as the site state | Act II §A2.7, OL.6, WD §4.8, CN §5.8 | Canonical `drift.<site>` ids in a character-scoped site store (§3.9); quest flags may mirror but are not the state |
| I-13 | Quest-state model | **Resolved 2026-11-02.** Earlier: 15.2 had Uninitialized, Active, Completed, Failed, Abandoned; Stage 27 and code had Inactive, Active, Completed, Failed; packages assumed abandon and re-offer | 15.2, 27, `QuestRuntimeSystem.cs` | Director rule applied: three states, Inactive, Active, Completed. 15.2, 27 and code reconciled; abandon/re-offer replaced by walk-away and resume (§3.7) |
| I-14 | Step regression and logout completion | UL: logout during S04 "resets to S03". CR: logout during S04 has keepers deposit bundles (partial completion by logout). Everywhere else steps never regress | UL.5; Act III §10.12 | No regression: UL keeps S04 active and returns only the carry object (objective re-pins "Take the ledger"). CR: keep the authored generosity but express it as a persisted rule "undeposited bundles count as deposited, unsinged, on restore", not a logout-time action |
| I-15 | NPC names | **Hobbs**: far-bank household on "the low smallholding" (MQ2, MQ12) vs the **Hobb farm** on the Heartlands edge (WD, ME07: Rhoda and Col). **Wenna**: Wenna Tull (Orrin's sister, MQ3) vs Wenna Hale (UR) | Act I §A9.3; D&M §4, ME07; Act I §B5; S&C UR | Rename one of each. Recommend MQ2's far-bank household becomes another name, and UR's Wenna Hale becomes another first name |
| I-16 | Co-op props | NT: "A partner's lanterns light for both players (shared world props)" against the per-player prop rule every other package uses | S&C NT.9 | Per-player lantern state; shared only as NT's fallback |
| I-17 | Missing step | `TF_FOUGHT_IN_LOFT` set by `S04b_fight`, which is not in the TF steps table | Act II §TF.9/§TF.10 | Add `S04b_fight` (optional) or set the flag from TF-E2 defeat inside S04 |
| I-18 | Braid gate names | MQ9 teaches "far → middle → near"; MQ11 says "outer, then the sill, then the centre" and names gates Reedmere Weir, Long Sill, Lantern Sluice | Act II §BF.7.4; Act III §11.4 | Declare the mapping in data: far = Reedmere Weir, middle = Long Sill, near = Lantern Sluice; keep MQ11 wording "outer / sill / centre" in dialogue only |
| I-19 | Reed Stalker first appearance | Bible §10 says first seen MQ5; NB (after MQ2) and FW (after MQ3) can be first | S&C NB.4 | Already flagged to the Encounters package; no schema impact |
| I-20 | Flag style | Act packages use enums; side packages use exactly-one bool groups for the same purpose | all | Enums in data with bool aliases (§3.5.1) |
| I-21 | Activation wording | TL "auto-accept; Stage 15.2 permits"; Stage 27 forbids "implicit quest activation" | TL §9.1; Stage 27 | Auto-accept is an explicit, data-declared offer trigger with an accept-on-offer mode; Stage 27's wording should say so (§1.2 G05) |

---

## 11. Director-level items

| # | Item | Why it is Director-level | Content affected | Recommendation |
|---|---|---|---|---|
| D-INT-1 | **Set-piece controllers** (TF gate band, DK hold/slip, SV gate progress with decay, BF flow-table, CR evidence table, UC observation, Muster drag stones) | No scripting layer exists, and 15.3 forbids scripting in trigger evaluation. Seven bespoke state machines amount to a small new system. | MQ6, 7, 9, 10, 11; UC | Approve **one** generic, data-configured "set-piece state" component (named states, counters, timers, inputs from events; emits EV19/EV20) owned by Systems, rather than seven one-off scripts. |
| D-INT-2 | **Per-player instanced NPCs and creatures** (owner-visible entities) | Effectively a phasing capability in replication and spawning. | DK Bryn, HW Orrin, MN elk, SV evacuees and Muster visibility, BF Sedge, WC sow | Do not build for the Lowmark milestone. Use the authored shared-entity fallbacks; revisit after M3. |
| D-INT-3 | **Dream presentation layer** (TB) | A bounded per-player world-dressing swap with aggro immunity; the package calls it "the most expensive presentation in this file". | TB only | Approve the 60 m-ring fallback for the Lowmark milestone. |
| D-INT-4 | ~~Non-lethal defeat / yield mechanic~~ (I-05) | **Resolved 2026-11-03 by CDR-1.** | OL, CR | Done. Only need left: the quest on-defeat hook for named creatures (SX-1, SX-2) that plays a scripted outcome and spawns the NPC non-hostile (M18). See `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`. |
| D-INT-5 | **D-6 drift-site state model** | Bible D-6 is open. Drift-site state, re-forming creatures, split (MN) and the MQ11 ending matrix all assume "disperse vs quiet". A "Wraiths can be destroyed" ruling removes M09–M11 and the MQ8 demonstration. | MQ3, 4, 6, 7, 8, 11; WD, CN, OL | Rule on D-6 before M2 starts. |
| D-INT-6 | **Keep-watch as a per-player quest clock** | Determines whether Lowmark needs a world clock at all for its milestone. Content currently relies on a local clock. | 17 packages | Approve the per-player quest clock (I-11) and defer world time. |
| D-INT-7 | **Quest-state model** (I-13) | **Ruled 2026-11-02.** The Director confirmed three states (Inactive, Active, Completed); no Failed or Abandoned. | All | Done. Stage 15.2, Stage 27 and `QuestRuntimeSystem.cs` reconciled; §3.7 rewritten. |
| D-INT-8 | **C8 / Rhosyn canon** (I-04) | Resolved in the fix pass (crew ledger, `UL_LEDGER`); Director confirms the bible §6.1 wording change. | UL, MQ10, MQ12 | Confirm. |
| D-INT-9 | **Name clashes** (I-15) | Renaming authored [NEW] households and characters. | MQ2, MQ12, WD, ME07, MQ3, UR | Approve renames before dialogue line keys are generated. |
| D-INT-10 | **Vendor and opportunity states** (BP, HS, WC, FK) | Economy surface is reopened by the Director's re-entry directive and is not in narrative scope. | Side quests | Route to the economy pass; narrative needs only the open/closed flags. |

**Open bible decisions that block data but not runtime:** D-1 (antagonist; swap layer is tagged), D-7 (Sedge; `[D-7]` tags), D-8 (Oriel; `[D-8]` tags), D-9 (subzone names), D-5 (map: every flow-table, observation-volume and zone placement is **MAP VERIFICATION REQUIRED**).

---

## Director rulings reconciliation (2026-11-03)

Applied `Quests/Caelmor_Director_Rulings_Combat_Ranged_Release.md`. Removed every non-lethal defeat need (G20 threshold/downed/swap, EV07 `downed`/`yielded` outcomes, EV08 `creature.yielded`, the NPC hostile/neutral swap row, M18 non-lethal defeat, Rusk as a tied NPC, the I-05 and D-INT-4 open rulings) and replaced them with one need: a quest on-defeat hook for named creatures (SX-1 Joss, SX-2 Sallow) that plays a scripted outcome and spawns the NPC non-hostile (G20, EV08 `creature.scripted_defeat`, M18). `cr.sallow_yield` now fires on defeat. Added G20a (ranged accepted everywhere, never required; WC optional borrowed short bow). Release wording changed to milestone language (CDR-3). Pointer added to `Quests/Caelmor_Combat_Ranged_Release_Engineering_Handoff.md`. Ids, steps and flags unchanged.
