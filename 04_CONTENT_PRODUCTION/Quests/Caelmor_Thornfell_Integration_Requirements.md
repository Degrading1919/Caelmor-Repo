# Thornfell — Integration Requirements (Technical Handoff)

**Status (2026-11-03): review state.** Requirements handoff from Creative Production, written for the Systems Engineer (Sol) and the Creative Production Director. This is Batch 4 of the Thornfell bible (`Caelmor_Thornfell_Narrative_Production_Bible.md` §12). It records **what the authored Thornfell content needs the runtime, schemas and data to support**. It implements nothing. It does not design schemas, write JSON or specify C#, and it does not alter, extend or claim to alter any authoritative contract, schema or runtime architecture. Field names and ids below are requirement labels; the **Schema & Content Engineer** owns real names and shapes, and the **Systems Engineer** owns every runtime contract.

**Audience:** Systems Engineer (runtime; Roadmap Stages 24–30 and the 33.x bindings), Schema & Content Engineer (31.x, 34.x), with the Gameplay Designer, Zones/POI, Audio/UI, Encounters and item/economy passes named where they own a decision. Sol is unavailable while this is written; everything here waits for him and nothing here is decided on his behalf.

**Quest lifecycle (authoritative, cited, not restated as new):** quests have exactly three states, **Inactive → Active → Completed**. The current contract is `DESIGNS/Systems Design/Stage 15.2 — Quest State & Progression Rules.md` (revision 2026-11-02: `Uninitialized` renamed `Inactive`; `Failed` and `Abandoned` removed; legal transitions `Inactive → Active` and `Active → Completed` only) and `DESIGNS/Systems Design/Stage 27 — Quest Runtime Integration Definition.md` (same three states; a quest the player leaves stays Active and resumable). `CODE/Systems/QuestRuntimeSystem.cs` implements the same model. The Lowmark handoff records this reconciliation as resolved (Lowmark I-13, D-INT-7). Every Thornfell package was authored against it: no quest fails, none is abandoned, walking away keeps the quest Active at its persisted step with an authored resume hook, and choices are outcome flags.

**Scope (see also §7).** Thornfell is **future-region authoring** (Phase 1.3 v1.5 direction; bible "Scope guard"). Only Lowmark is approved for release. This file **does not expand the initial release scope**, does not schedule Thornfell work, and does not ask for anything to be built for v1. It exists so that, when Thornfell is scheduled, its dependencies are already listed and can share what Lowmark builds.

**Sources read:** the bible (all, binding: §1.1 sound system, §2.6, §3 TD-1…TD-14, §6.1, §9 world state and calls, §10, §11 conventions, §12 file map); every "Integration needs" table, steps and flags table, rewards table and failure/co-op table in `Caelmor_Thornfell_Main_Act_I.md`, `_Act_II.md`, `_Act_III.md` and the four `Caelmor_Thornfell_Side_Quests_*.md` files (Horn and Highsteads; Banner and Memory; Settlements and Combat, including TME01–TME10 and TDS01–TDS10; Work and Skills, including EC-01…EC-14); condition notation in `Dialogue & Narrative/Caelmor_Thornfell_Main_Act_I/II/III_Dialogue.md`; the Lowmark handoff `Caelmor_Lowmark_v1_Integration_Requirements.md` (format and shared capabilities); Stage 15.2, Stage 27, `QuestRuntimeSystem.cs`; the Stage A contradiction register (S01). All packages were re-checked against their committed, reviewed state of 2026-11-03 (§8).

**Conventions in this file**

| Mark | Meaning |
|---|---|
| **MUST** | The content cannot ship as authored without it. Each MUST names a fallback unless marked *no fallback*. |
| **SHOULD** | The authored experience degrades without it but stays playable and non-blocking (every package authors a fallback). |
| **COULD** | Polish; the package's fallback is an acceptable ship state. |
| **[DIRECTOR]** | A Director-level item (a new core system, an unapproved mechanic, or an open `[PROPOSAL — DIRECTOR]`). Collected in §6. |
| **Shared?** | `= LM <id>`: Lowmark already needs the same capability; build once (ids from the Lowmark handoff: G gap rows, EV events, M mechanics). `ext LM <id>`: Lowmark's capability plus a Thornfell extension. `TH only`: Thornfell needs it and Lowmark does not. |
| Requirement ids | `TI-<group>-<nn>` (Thornfell Integration). Chosen so they cannot collide with bible decisions `TD-n`, discoveries `TDS##`, or Lowmark `G/EV/M/I/D-INT` ids. |
| Quest codes | Main: **TPW** TF-M1 · **TIW** TF-M2 · **TES** TF-M3 · **TSH** TF-M4 · **TSW** TF-M5. Side: **TTH TWG TNK** (Horn and Silence) · **TNR TSM TRR** (High Steads) · **TSL TWC** (Banner) · **TWN TSN TOS** · **TSR TST TGY TFS TBC** (Work and Skills) · **TMM TAS TGM TSG** · micro-events **TME01–TME10** · discoveries **TDS01–TDS10**. |

Owner key: **SE** Systems Engineer · **SCE** Schema & Content Engineer · **GD** Gameplay Designer · **ZN** Zones/POI package · **AU** audio · **UI** UI · **ART** art/VFX · **NPC** NPC/AI · **ENC** Encounters package · **IT** item/economy pass.

---

## 1. Baseline and how Thornfell differs from Lowmark

### 1.1 What exists today

Thornfell adds nothing to what exists. The baseline is the Lowmark handoff §1.1: `QuestRuntimeSystem` with quest-level state only (register, activate, complete; in-memory), three-state lifecycle agreed across Stage 15.2, Stage 27 and code, a thin event vocabulary (`WorldEvent`, `CombatEvent`, `InventoryEvent`), the Stage 16.3 rule that an NPC interaction never advances a quest directly, a click-to-move client on a flat baked NavMesh with no jump and no off-mesh links, no disk persistence, no dialogue, NPC or quest data. Roadmap Stages 24, 30, 31 and 33–35 are unchecked.

### 1.2 What Thornfell adds on top of Lowmark

| Theme | Lowmark (already in its handoff) | Thornfell difference |
|---|---|---|
| Readable system | Water against a marker (presentation-only water effects, M24) | **Sound** is gameplay input and output: the player **blows calls**, NPCs and crowds **obey calls**, the player **reads echoes** and **strikes rock** to learn its state, and **null-points** remove sound. This is the one large Thornfell-only capability group (§2.4). |
| Time | Per-player keep-watch quest clock (M04, D-INT-6) | Same clock, plus an **event-advanced countdown** (TPW Close count), **quest-local storm windows** that pause off-volume (TES, TSL, TOS), a **per-player blizzard** (TSW) and a **wind-window timer** exposed as lull / whistle / gust to many systems. |
| World state | Region flags `LM_*`, drift-site state | Region flags `TH_*` (16), a two-value **season** presentation state, **posture** computed from flags, no drift-site store. |
| Combat | Drift disperse/re-form; humans downed or yield (M18) | Same yield rule (TD-7), plus an **encounter-level surrender** trigger, a **threshold yield boss** (Ingrith ~20%), **re-forming resonance figures** tied to a storm window (not a site store), a **hazard that is not an entity** (Summit node pulses) and a **silent arena** (TGM). |
| Accessibility | Few audio-only cues | Many audio-only cues by design; every one needs a visual or haptic equivalent (§2.15). |

---

## 2. Requirement register (de-duplicated, grouped by system)

Each requirement appears once. "Consumers" lists every quest and step that depends on it; where a package only *references* a shared need, it is listed as a consumer, not as a second requirement.

### 2.1 Quest state and step persistence

| Id | Requirement | Minimum viable form | Owner | Consumers (quest / step) | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-QS-01 | **Ordered steps** inside a quest instance with objective text key, sub-counter, completion predicate and kind (required / optional / conditional / parallel group) | Lowmark step model unchanged; `S00_…` ids scoped to the quest | SCE (shape), SE (runtime) | All 25 quests. Optional: TIW `S05b_cage`. Parallel/any-order: TPW S05/S06; TIW S01; TES S07; TNR, TWN | = LM G01, §3.2 | MUST, *no fallback* |
| TI-QS-02 | **Three-state lifecycle only**; no fail, abandon or reset action anywhere; journal keeps every Active quest listed | Stage 15.2 / 27 as they stand (cited above). No Thornfell-specific field | SE | All | = LM G04, §3.7 | MUST (already contracted) |
| TI-QS-03 | **Resume hooks** per quest and, where authored, **per step range** | Data: quest → list of (step range, resume NPC/volume, line key). Default: the original offer | SCE | TPW (Vessa; Aud after S04); TIW (Elira; Bersi after S09); TES (Gerrit before S07; Dorn after); TSH (Iven); TSW (Ressa S00–S01, Dorn S02–S08, Hadrik's runner S09–S12); every side quest names one | ext LM §3.7 (step-ranged hooks are new) | MUST |
| TI-QS-04 | **Explicit, data-declared activation triggers** incl. zone-entry auto-start | Offer trigger + `accept_on_offer` mode, never implicit (Stage 27). TSW activates on entering Windscar Pass or Stonewake after TF-M4 Completed (`tsw.blizzard_start`); TPW on the gate volume; TES on the Cut volume; TWC automatically at TSL's end | SE | TSW S00, TPW S00, TES S00, TWC, TIW (after TF-M1 storm broken) | = LM G05, I-21 | MUST |
| TI-QS-05 | **Unlock predicates** on other quests' states, including two-parent gates | `quest_state(id) = Completed` conjunctions | SCE | TSM (TNR + TF-M2); TRR (TSM + TF-M3); TNK (TF-M4 + TWG); TF-M2…M5 chain; all side unlocks (Act I/II unlock tables) | = LM §3.1 | MUST |
| TI-QS-06 | **Persisted sub-step progress**: segment indices, per-panel done flags, counters, checkpoints | Written as quest state at commit points (Stage 15.1 permits only this) | SE | TES irons, `TES_LOOSE_IRONS`, swell count (S06); TSH marks, plates damped, unbolt segments; TSW wipes ×3, rubs ×3, winch ×3, boss phase; TPW Close count, bridge stage; TIW cage; TWN wedges/letters; TSN dig; TOS haul; TGM stones stacked; TSG answered pairs; TAS segments | = LM G26, §8.2 | MUST |
| TI-QS-07 | **Steps never regress**; logout discards only in-progress channels and returns carries to source | Baseline rule; no Thornfell package authors a regression (checked) | SE | All | = LM §8.2, I-14 | MUST |
| TI-QS-08 | **Respawn anchor by step** | Step-keyed respawn override | SE, ZN | TPW gate / Aud's cart; TIW Three Calls / hoist foot; TES per §A7; TSH per §B7; TSW last checkpoint / warden room H1; side quests' named safe points | = LM G27, §8.3 | MUST |
| TI-QS-09 | **Restore rules on logout** that place NPCs and set pieces at a known state | Step-entry state restore with named exceptions: TPW S10 column waits at the far bridgehead; TSW mid-boss → warden room, boss 100%; mid-hold → winch floor, column in the lee; straggler on the player's rope restored inside the gate; TIW Brynjar waits at the hoist foot | SE | TPW, TIW, TSW, TES (pairs stay on stances), TSH (crew at test) | = LM §8.2 | MUST |
| TI-QS-10 | **Server-timed completion** for presentation-ending steps | Server emits the end of a script event on its own timer (no client report gates a step) | SE | TPW S12 `passwatch.rest`; TSH silence; TIW `whinstone.frame_hum` | = LM §2.1 rule | MUST |
| TI-QS-11 | **Minimal quest UI**: objective text, sub-counters, suppression during strange moments | Lowmark G28; Thornfell suppressions: TPW `passwatch.close_early`, TSH total silence, TSW roster reading | SE, UI | All | = LM G28 | MUST |
| TI-QS-12 | **Content validation**: every flag read has a writer; every required proof has a guaranteed path; every optional step closes | Lowmark validator rules applied to `TH_`/`T??_` namespaces | SCE | All; specifically TF-M5 posture inputs (§3.3) | = LM G30 | MUST |

### 2.2 Region flags and quest-local flags

The full `TH_` register with values, setters and readers is §3. This table lists the capabilities those flags need.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-FL-01 | **Character-scoped region flags** `TH_*` (16, bible §9.1 only) readable by any quest, dialogue, prop, NPC placement set and commission gate | Same store as `LM_*`; namespace `TH_`. One writer per flag (validator) | SCE, SE | §3.1 | = LM G03 | MUST |
| TI-FL-02 | **Typed quest-local flags** (bool, closed enum, bounded int) with **unset** distinct from every value; readable after Completed | Lowmark §3.5 store; `T??_` prefixes | SCE, SE | All. Ints: `TPW_CLOSE_COUNT`, `TES_LOOSE_IRONS`, `TSH_WRONG_PLATES`; enums: `TSH_MAP_TIER`, `TSW_G3/G5`, `TSW_ODDNY/HALVARD`, `TSW_READER`, `TNK_PLATES` (8 values) | = LM G02 | MUST |
| TI-FL-03 | **Exactly-one bool groups stored as one enum** with bool read-aliases | Lowmark §3.5.1 rule. Groups: `TSL_STAFF_LEFT/_TAKEN`; `TWN_CUT_BOTH/_FAMILY/_OPEN`; `TSN_RECUT/_TOLD_HOUSE/_LEFT`; `TOS_TOLD/_KEPT/_WARDEN`; `TES_JAM_MINED/_CREW` | SCE | Banner and Memory file; TES | = LM I-20 | SHOULD |
| TI-FL-04 | **Cross-quest reads of quest-local flags** (§3.2) | Read scope "any quest of the same character" | SE | §3.2 | = LM §3.5.2 | MUST |
| TI-FL-05 | **Derived flag at a step**: `TH_ASSEMBLY_POSTURE` computed from nine inputs by the §9.3 arithmetic | Explicit effect at TSW `S11_reading` evaluating a data-declared formula (open/sealed counts, thresholds ≥3 / ≤−2); weights tunable by GD | SCE (rule data), SE (effect) | TSW S11; epilogue §E; convergence | ext LM §3.8 "derived values" | MUST |
| TI-FL-06 | **Lowmark state reads for variant lines only**, never as gates | `quest_state(lowmark.main.02_short_measure / 04_night_flush / lowmark.side.night_bridge)`, `LM_CIVIC_STANDING`, NB credit outcome (Lowmark stores NB as one enum with aliases) | SCE | TPW S00 (`TPW-B0.1`, `TPW-D1.30`); TIW ledger and grain inspects, `TIW-D6.40`; TES `TES-D2.40`; TBC-D7; TSW Elira line | TH only (reads Lowmark data) | SHOULD |
| TI-FL-07 | **Discovery and micro-event flags** set without a quest instance | `TDS0n_SEEN` / `TDS0n_READ`, `TME0n_*` on the character | SCE | TSW reads `TDS10_READ` and `TME01_TALLIED`; TMM reads `TME01_TALLIED`; TME01 loop | = LM ME flags | SHOULD |
| TI-FL-08 | **Name-address substitution** in dialogue keyed on tally flags | Line variant swaps "walker" for `{name}` when `TME01_TALLIED` or `TSM_PLAYER_TALLIED` (any-of) | SCE, SE | TSW Runa; TMM-D3; all Hushfold/Nettlehook hosts; TWC (Runa, shared) | TH only | SHOULD |

### 2.3 Dialogue conditions and effects

Thornfell uses the Lowmark node format and every Lowmark condition and effect type (Lowmark §4.2–4.3). Only the additions are listed.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-DG-01 | **Condition on a call blown** inside a node's window (shape, and "anything else", and "nothing") | Dialogue waits on a `call.blown` event (TI-SN-01) with a timeout branch; notation `[player blows Answer]`, `[player blows anything else]`, `[player blows nothing within ~10 s]` | SE | TPW-D2 lessons; TSW stragglers; TTH answering stones; TIW Rest-within-window (`TIW-D6.50`) | TH only | MUST |
| TI-DG-02 | **Idle / position conditions** | `[player does not move within ~8 s]`, `[player under the eave in time]`; server-evaluated from committed position | SE | TPW-D2 Fall lesson; TSW-D1 | ext LM "proximity" | SHOULD |
| TI-DG-03 | **Item-held and tool-held conditions**, including "no horn" and "has no cutting tool" | Item / category held | SCE | TSW S00 (`[no horn]` → loan fallback); TTH-D1; TSR, TST, TGY "has no tool" | = LM §4.2 | MUST |
| TI-DG-04 | **Enum and computed-value conditions** on region flags and posture | `[TH_HORN = broken]`, `[sledge or caravan]`, `[reader = maera, TH_SHATTERFALL_ACCOUNT = kept]`, `[open]`/`[watchful]`/`[sealed_with_terms]` | SCE | TSW-D9; TSH-D11/12; TIW-D9; epilogue | = LM §4.2 | MUST |
| TI-DG-05 | **Splinter swap tags** on nodes | `[SPLINTER]` tag on every node naming Ingrith, Bersi or Eyvind, for search-and-swap if TD-1 changes (bible §3.1) | SCE | TIW, TES (pay chits), TSH, TSW, TNK | ext LM `[ANTAGONIST]` tag | MUST |
| TI-DG-06 | **Timed "deliver" input** inside a dialogue node | Input accepted during an authored hush cue. Fallback (authored): a choice "wait for the room" / "say it now" | SE, UI | TFS story (TFS.11) | TH only | COULD (fallback is the ship state; see TI-AX-05) |
| TI-DG-07 | **Document views** assembled from flags | Code-book pages from `TTH_KEEPER`, `TWG_CALL`, `TH_HORN_CODES` (fallback: fixed variants); quest-item pages (§2.10) | UI, SCE | TNK; TIW ledger; TES roster; TSH record; TSW rubbing | ext LM inspect/document | SHOULD |
| TI-DG-08 | **Side-by-side document view** | Two documents in two columns; fallback: sequential with a "set beside" log line | UI | TES S09; TSH S10 | TH only | SHOULD |
| TI-DG-09 | **Placement-reading dialogue**: lines keyed on where NPCs were placed | Reads the placement set chosen from flags (TI-PP-05) | SCE | TSW-D9 | TH only | MUST |

### 2.4 Horn-call input and audio recognition (the sound system)

This is the largest Thornfell-only group. Bible §1.1 and §9.4 define the content; nothing here may make the sound system magical (bible §5.3, §11.7). Recognition is **authored data**, never physics or microphone input: the player chooses a call from a wheel; the server knows which call was chosen.

**The calls (bible §9.4) as data the system must carry:**

| Call | Shape | Glyph | Player-blowable | Notes for implementation |
|---|---|---|---|---|
| Rest | one long | flat line | Yes (`TH_CALLS`) | TIW: Rest within ~3 s of a hornman's Gather cancels his buff/reinforcement (`TIW_GATHER_CANCELLED`) |
| Close | two long, falling | two falling bars | Yes | TPW countdown; TSW boss slab-drop cue |
| Gather | three short | three dots | Yes | Commands escort columns and child groups; summons |
| Fall | short-long-short | dot-bar-dot | Yes | Halts columns; warns pairs (TSG); bandit duck reaction (TWG); "startled by Fall" wolf interrupt (TTH) |
| Lost | one long, rising | rising line | Yes | TTH relay; TSW stragglers blow it |
| Answer | two short | two dots | Yes | Echo-count probe (TSW); reply to Lost |
| the Third Horn | Answer + one long rising | two dots and a rising line | Only with `TH_THIRD_HORN` | Restored in TTH; blown by the player in TSW S07 |
| Witness at the Gate | two long, one held | shown only in TWG | After TWG (no mechanical effect anywhere) | Needs a **held** note (TI-SN-07) |
| the Split | — | **none** | **Never** | **Must not exist as audio, glyph or data shape** (bible §9.4; TNK). Validator check |
| Gallery sealing calls [NEW] | Close plus a tag (Act III §6, open decision 7) | marker-stone glyphs | No (NPC hornmen only) | New wartime calls; need audio and glyphs; not refused calls |

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-SN-01 | **`call.blown` server event**: player, call shape id, position, volume id, hold duration | New event type (packages call it *call-blown*, TTH.14). Emitted after the call interaction commits. NPC hornmen emit the same event | SE | Every quest that uses calls: TPW, TIW, TES, TSW, TTH, TWG, TNK, TRR, TGY, TSG, TME10, TDS03/TDS04 | TH only (extends LM EV vocabulary) | MUST |
| TI-SN-02 | **Call wheel** offering the calls the player knows | Interaction with glyph buttons; **no rhythm input**; plays the call's audio from the player's position. Fallback: context prompts ("Blow Gather") where a call is needed | SE, UI | As TI-SN-01 | TH only | MUST |
| TI-SN-03 | **Horn carrier tool**: the Hornbearer's practice horn (TF-M1 reward tool) | Reward tool defined by IT; enables TI-SN-02. Every later package now relies on it (Act III open decision 4 resolved; Horn and Highsteads §0.6). Fallbacks only if the player lacks it: Dorn's lend (TTH-D1), Bera's herding horn (TGY-D1), Ressa's loan (`TSW_HORN_LOANED`) | IT, SE | TPW S01 grant; all call users | TH only | MUST |
| TI-SN-04 | **Call glyphs** on screen when a call is heard or blown and `TH_CALLS` is set | Screen-edge glyph ~2 s, **placed in the source direction**; dimmer delayed glyph for an echo; caption line. Shown with audio off | UI, AU | All call users; TSW whiteout depends on it | TH only | MUST (accessibility, TI-AX-01) |
| TI-SN-05 | **Positional NPC calls and scripted Answers** | Positional one-shots at named emitters triggered by step events, with authored delays | AU, SE | TSW warden posts and stragglers; TSG ledge pairs (Answer after N beats); TTH answering stones; TNK distant posts (5 points); TRR chord; TWG line run | TH only | MUST |
| TI-SN-06 | **Call listeners**: volumes, NPC groups and encounters that react to `call.blown` | Listener filter (shape, volume, time window) → step progress, NPC state change or encounter modifier | SE | TPW escort (Gather move / Fall halt); TRR children (advance / kneel); TGY herd (Gather → next waypoint, Fall → settle); TIW hornman cancel; TSG terrace gate; TSW posts | TH only | MUST |
| TI-SN-07 | **Held call** | Call interaction with a hold duration and breath bar; shape gains "held" at ≥ 5 s. **Toggle option** for accessibility | SE, UI | TWG | TH only | MUST for TWG |
| TI-SN-08 | **Authored echo return** from tagged faces | One component: an emitter blows (or strikes) at a tagged face; the face returns an **authored** result (beat count 1 / 2 / 3+ / none; or quality steady / short / smeared / doubled / clean) after that many beats; beat-dots pulse per beat. No raycast physics required: TSW's distance bands are authored per face tag | AU, SE, UI | TPW Narrows face state machine (holding → shedding → dropped → holding); TSW whiteout (Answer → nearest `echo_face`); TOS two call points; TGY per call-stone; TWG clean/smeared per groove; TNK clean/doubled per horn sleeve state; TDS04 | TH only | MUST |
| TI-SN-09 | **Strike-and-listen interaction** with authored result sets | Instant or short interaction on tagged objects: plays one of N authored returns, prints a log line, shows a return glyph (one tick / two spaced ticks / beat-dots). "Masked" variant during a storm swell. Results are data, not physics | AU, SE | TES anchor seams (quick-flat / slow-doubled; masked in swells); TSR faces (barren / iron tail 1–4 / hollow; hollow blocks mining); TBC fittings; TAS cramps (three rings); TWN slabs (true / flawed); TMM optional tap; TME02 lintel; post-quest "reading rock" everywhere | TH only | MUST |
| TI-SN-10 | **Wind-window timer** exposed as **lull / whistle / gust** states to interactions, hazards, NPC movers and audio | One per-player timer per site with authored period; tell **2.5 s**, gust **3 s** (TST long gust ~6 s); gust = push **2 m** toward the defined safe side (never off a ledge), light damage, no knockdown; shelter-face volumes negate; optional authored sequences (TBC long-short-long). Values per §5 C-1 | SE, AU | Every outdoor package: TPW guide line/escort; TIW ledge and shaft; TES; TSW; TSL; TWC; TOS; TMM plank; TAS scaffold; TSG; TST stem audio; TFS smoke-flap; TBC; TSM sledge; TRR; TNR car; TME08 | TH only | MUST |
| TI-SN-11 | **Null-point volume** | Staged fade (~2 s) that ducks or mutes player-generated sound, ambience and gust audio; dust and snow particles fall vertical; optional pulse-damage negation (TSH). Variants: **duck** (TDS01, TSH, TOS, TWG, TME05, TIW gully actor voice cut) and **total** (TGM: all world and voice buses; UI pending TGM-OD1) | AU, ART, SE | TIW S03 gully; TSH S06/S09 alcoves; TGM den; TWG Silent Gorge; TOS step; TDS01; TME05; Kaldren's grit-and-voice test as inspect variants everywhere | TH only | MUST |
| TI-SN-12 | **Listening points with directional mix** | Three interaction points; each plays an authored left / centre / right mix with subtitles naming direction and source | AU, UI | TSH S04 | TH only | MUST |
| TI-SN-13 | **Whisper-down-a-line** | Per-line interaction with an authored result (return / no return) | AU, SE | TSH S04 (optional, logged) | TH only | SHOULD |
| TI-SN-14 | **Positional voice override** in a hall | Play a voice line at an authored emitter with a faint second emitter at the speaker; per-player delayed send for the player's own lines | AU | TWC count scene (the stone); TMM hall voice return; TSW Assembly (some voices carry) | TH only | SHOULD (fallback: subtitles with direction markers) |
| TI-SN-15 | **Total-silence one-shot** | Mute every bus including UI for ~3 s, restore in scripted order; player keeps control | AU | TSH S09 last plate | TH only | SHOULD (see TI-AX-03) |
| TI-SN-16 | **Peg board puzzle** (compose a call) | Row of up to four slots, four peg types (short, long, rising, held), play button, compare to target; wrong composition plays back with a dry line. Fallback: dialogue options naming shapes | UI, SE | TTH, TWG, TNK | TH only | SHOULD |
| TI-SN-17 | **Gallery call sequencer** | Ordered call list with per-gallery state (spent / live / resolved); live calls repeat until resolved; haul stages advance only with the player in zone and never complete | SE | TSW S02 (`TH_STORES = seized` → G5 resolvable by cutting only) | TH only | MUST [DIRECTOR] via D-INT-1 (TDI-1, §6) |
| TI-SN-18 | **Warden post call cycles and assist re-call** | Per-post timed call loop; progress check; double call plus pinned glyph after 45 s without progress | SE | TSW S01 | TH only | MUST |
| TI-SN-19 | **Scripted audio events (strange moments)**, once per player, persisted seen-flag | Server-emitted, client-local: `passwatch.close_early` (echo before the second note; ambience duck), `whinstone.frame_hum` (+ crow lift), TTH altered echo (Answer + rising tail), TWG call running the line with a hard cut, TNR cable note + Tova hum, TSM smoke lean (visual), TRR chord, TNK unanswered call, TST stump moan, TAS arch note, TSG plate hum | AU, SE | Listed | = LM EV15 / §2.3 rule | SHOULD (fallbacks: inspect text) |
| TI-SN-20 | **Altered or haptic-only sounds** | Haptic event channel with visual fallback (shiver VFX + subtitle) | AU | TME05 (felt through rock; no audio by design); TGM impacts; TAS arch note | TH only | SHOULD |

### 2.5 Channelled interactions and persistent segments

One channel component serves every row; the rows differ only in interrupt rule.

| Id | Requirement | Minimum viable form | Owner | Consumers (segments) | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-CS-01 | **Channelled interaction**, server-timed, cancel on move or damage | Lowmark M02 | SE | TSH `take_horn` (~2 s, interrupted by a pulse); TSW pull-line cut (3 s, interrupt on damage); TES side-by-side; TME listens | = LM M02, G11 | MUST |
| TI-CS-02 | **Segmented channel, completed segments kept** across damage, death and logout | Lowmark M03 / MQ4 crank convention; segment index persisted (TI-QS-06) | SE | TPW `snub_post` ×3; TIW `wind_cage` ×3; TES `mine_jam` ×3, `rig_line` ×2 per rig, `pay_out` ×3 per rig, `climb_ladder` ×4; TSH unbolt ×2 per plate; TSW `wipe_panel` ×3, `rub_panel` ×3, `wind_slab` ×3; TSL lashings; TWN wedges and letter lines; TAS three-segment repair; TOS haul; TGY leather chain | = LM M03 | MUST |
| TI-CS-03 | **Interrupt-rule variants** per channel | Data field: `cancel` / `pause_on_gust` (TOS haul, TST stool-cut auto-pause on whistle) / `reset_current_segment_on_gust` (TSN dig slump; only the current unboarded segment) / `interrupt_and_offer` (TES loaded iron on a loose seam: scripted shift, segment interrupted, *Pull the iron* offered) / `pulse_interrupt` (TSH) | SE | Listed | ext LM M03 | MUST |
| TI-CS-04 | **Channel that stays active while walking a corridor** | Active while the player is inside a corridor volume; completes on entering an end volume. Fallback: two inspect points | SE | TMM cord run | TH only | COULD |
| TI-CS-05 | **Sustained hold that paces a scripted crowd** | Hold interaction; release pauses the crowd path; crowd waits in a lee volume | SE, NPC | TSW S06 | TH only | MUST [DIRECTOR] via D-INT-1 |
| TI-CS-06 | **Crew alternative** for every skill channel | Dialogue choice that advances the segment or step, optionally costing a Close or a watch step | SE, SCE | TPW S05/S06 (+1 Close each); TES S03 (storm one gust cycle early); TAS; TSR; TST; TGY; TBC; TWN vigil | = LM crew paths | MUST |

### 2.6 Keep-watch quest clock and time windows

All time in Thornfell is a **per-player presentation state**, never world time (bible §9.5). This is exactly the Lowmark keep-watch contract (Lowmark M04, I-11, D-INT-6) with three Thornfell extensions.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-CK-01 | **Keep-watch interaction** advancing the player's quest clock to the next named window (dusk, night, dawn, storm, drift morning) and swapping lighting/spawns | Lowmark M04 unchanged | SE | TPW epilogue (two steps); TSW S08 (×2 at H1); TSL stormwatch bench and crag-foot wait; TSN hearth wait and dusk; TWN vigil (crew path); TOS storm; TMM night at the hall doors; TAS night and dawn; TGY watch to dusk; TFS watch to dawn; TTH ~25 s seated verse watch; TME01/03/06/08; TDS07/08 storm windows | = LM M04 | MUST |
| TI-CK-02 | **Event-advanced countdown with a held final position** | Per-player counter advanced only by named events (never a timer); drives a sky/sleet step and a pip display; the final value is held until a release event, so it **cannot run out** | SE, UI | TPW Close count (`TPW_CLOSE_COUNT`: Close I on S02 exit, II at W4, crew Closes, span Close, last Close on S10) | ext LM M04 | MUST |
| TI-CK-03 | **Quest-local storm state** with an ordered window index that **pauses when the player leaves the area volume** | Per-player window index driving gust cycle, haze, snow, ambience and spawns; persisted; resumes on return. TES: five windows (fallback three: building / hard / clear); window turn gated by a persisted swells-endured counter | SE, ART, AU | TES S00–S07; TSL; TOS; TSN snowlight (`tsn.snowlight` preset, ended on S02) | TH only | MUST |
| TI-CK-04 | **Per-player blizzard / whiteout** | Quest-local weather with a visibility clamp (~3 m) and a readable character outline; other players see ordinary snow; ends for that player after S08. Fallback: heavy fog volume with the same clamp | SE, ART | TSW S00–S08 | TH only | MUST |
| TI-CK-05 | **Per-player timers** inside steps | Server timers: assist re-call 45 s; crew finish ~60 s after choice; TIW surrender ~60 s; Rest-window ~3 s | SE | TSW, TPW, TIW | = LM EV22 | MUST |
| TI-CK-06 | **Node pulse rhythm driven by quest state** | Period set by state (Eyvind playing / plates remaining / wrong-plate offset ~6 s early) | GD, SE | TSH S07–S09 | TH only | MUST [DIRECTOR] via D-INT-1 |

### 2.7 Carry states

Carry objects never enter inventory and return to their source on drop, logout, death or area exit (Lowmark M05). Thornfell adds heavy variants.

| Id | Requirement | Minimum viable form | Owner | Consumers (objects) | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-CA-01 | **Carry state** with deposit volumes and return-to-source | Lowmark M05 | SE | TPW stormwood stakes ×3, fittings, guide line, grain sack; TES rope coils, anchor irons (placed on seams); TSW wedge, charcoal and count sheet; TWN cut stone; TWG ladder; TNR sheave pins; TTH chalk copy; TNK sack of shards; TMM account and slate; TAS cramp bundle; TGM stones; TSG plate crate; TSR capstone; TRR guide line and ribbon; TSM game | = LM M05, G12 | MUST |
| TI-CA-02 | **Heavy carry** (slow walk; **drop on hit**, re-pick in place) | Carry flag `heavy` with drop-on-damage | SE | TSH damped plate (drops on pulse hit); TSM sledge | ext LM M05 | MUST |
| TI-CA-03 | **Gust-aware carry** | Gust impulse on the carrier unless a **dip** action is held (halves speed, cancels impulse); TSM sledge slides back to the last brace point on a gust (fallback: gust knocks the player down only) | SE | TWC colour on its staff (sail push); TSM sledge | TH only | SHOULD |
| TI-CA-04 | **Deposit that converts a carry into a world prop** | Deposit volume swaps the carry for a usable prop (climbable ladder) | SE | TWG ladder (per player; fallback shared once set) | TH only | SHOULD |
| TI-CA-05 | **Tow carry of an NPC** at walking pace | Rope-line carry attached to an NPC; on logout the towed straggler restores inside the gate | SE, NPC | TSW S07 (Oddny, Halvard) | TH only | MUST (fallback: patrol brings unreached stragglers at dawn) |
| TI-CA-06 | **Snatchable carry** | Creature action forcing a drop at a point. Fallback: no snatch | SE, NPC | TSM wolves | TH only | COULD |
| TI-CA-07 | **Lower an object down a face** | Channel that despawns the prop above and spawns it below with an NPC (Lowmark SB slate pattern) | SE | TSL rolled banner | = LM SB pattern | SHOULD |

### 2.8 Per-player props, NPC placement and phasing

Solo-first (bible §9): all quest state is per player. Partners see presentation from their own state. Every package authors a fallback.

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-PP-01 | **Per-player prop and terrain state** keyed on flags and steps | Lowmark G16/M44 (per-viewer replication filter or client-keyed presentation) | SE | TIW store fill (sealed / emptied / filling) and Muster Hut drill; TES cairn facing stone and niche; TSH alcove plates and hum lure; TSW epilogue props by posture / `TH_STORES` / `TH_HORN`, roster wall rubbed or railed; TSL crag staff; TWC banner in three halls; TWN Brede stone; TSN drift door and post; TOS repaired path; TGM den; TSG ledge; TMM slate and wall; TAS gate book and shed; TSR boards; TST stands; TFS tally chalk; TBC repair post; TRR ribbon rail; TNK store contents | = LM G16 | SHOULD (fallbacks everywhere) |
| TI-PP-02 | **Per-player gate state** | Passwatch gate shut for a player between TPW S11 and the storm break; fallback: a wicket wardens open for players on other steps | SE | TPW S11–epilogue | ext LM G16 | SHOULD |
| TI-PP-03 | **One per-player Narrows bridge state machine** written by several quests | States (§5 C-6; Zones §6.2): N0 down (before TPW `S08_span`) → N1 patched → N2 cracked **only while TBC is Active** (overrides other states) → N3 mended (TBC Completed) → N4 permanent span (TRR Active or Completed). Scree path walkable in every state. One prop set, one owner of the state (Zones); each package writes only its transition | SE, ZN | TPW, TBC, TRR (TBC.11, TBC open question 4) | TH only | MUST (conflict Q-05) |
| TI-PP-04 | **Per-player NPC placement sets** | Step/flag-keyed NPC position sets | SE, NPC | TIW Brynjar at the hoist foot (private) or in the hall (public), Bersi present or gone by `TH_STORES`; TWN NPCs at the wall; TWC Hadrik's stand-points | = LM G09 | MUST |
| TI-PP-05 | **Assembly placement from flags** with one movement animation set per posture | Placement read from `TH_*` (Act III §8.4); four standing-place volumes with confirm (sets `TH_STAND`). Fallback: static placements per posture without movement | SE, NPC | TSW S09–S11 | TH only | MUST |
| TI-PP-06 | **Owner-visible (phased) NPCs** | Not required. Packages use shared NPCs with per-player dialogue; e.g. TIW Brynjar appears at both places for partners on different routes | SE | TIW, TSW stragglers | = LM G17, D-INT-2 | [DIRECTOR] (do not build; fallbacks ship) |
| TI-PP-07 | **View-dependent local glimpses** | Client checks own camera; never replicated; **no step waits on it**. TSL's `tsl.ridge_seen` client report only adds an optional line (see Q-08) | SE | TSL; TDS07 Ridgewalker (vanishes within ~200 m) | = LM M25 | COULD |
| TI-PP-08 | **Lighting preset swap per player** | Preset swapped on an event; decal visibility by preset and lamp position | ART, SE | TSN snowlight; TME06 dusk shadow | TH only | SHOULD |

### 2.9 Season state

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-SE-01 | **`TH_SEASON`** per-player presentation state: autumn → snow | Set to `snow` at TIW S13 start; never world time. Drives a snowfall effect and snow cover on a **short** prop list only; no NPC wardrobe changes. Co-op fallback: the host's state | SE, ART | All Thornfell presentation; TFS, TSM, TME01 gates read it as "snow" | TH only | SHOULD |
| TI-SE-02 | **Season as an unlock condition** | `TH_SEASON = snow` readable in unlock predicates | SCE | TSL, TSN, TFS, TSM, TME01, TGM tracking snow | TH only | MUST |
| TI-SE-03 | **Quest-local weather layered over season** | TES storm, TSW blizzard, TAS yard snowfall from nightfall (fallback: frost decals), TSL stormlight on tagged sockets | SE, ART | Listed | TH only | SHOULD |
| TI-SE-04 | **Thaw presentation** | Quest-local bool `TSW_THAW`, set on first re-entry after completing TF-M5 and leaving the region once; `TH_SEASON` stays two-valued (§5 C-7) | SE, SCE | TSW §E.7 | TH only | SHOULD; [DIRECTOR] (Act III open decision 3) |

### 2.10 Quest items (exactly four)

Thornfell's budget is **four** (bible §9.5), all spent by the milestones. **Side quests, micro-events and discoveries add none** (checked in all four side files). Every other carried thing is a carry-state object (§2.7), a reward tool (§2.11) or an inspectable world object.

| Item | Acquired | Fate | Special requirement | Readers |
|---|---|---|---|---|
| `TIW_store_ledger` | TIW S09 (desk pickup; per-player desk prop in co-op) | Kept by the player through TSW | Paged document (front leaf, receipts, pay chits, allotments) with a **conditional recognition line** when `lowmark.main.04_night_flush` is Completed ("sixty-eight measures"). Never a gate | TES read-condition; TSW Assembly line and chip |
| `TES_horn_roster` | TES S07 (log tin) | **Leaves the pack at TES S10**, to one of three places by `TH_SHATTERFALL_ACCOUNT`: Maera's wall (amended), the cairn niche (beside), the Passwatch warden strongbox under Maera's cord (kept) | (1) Removal by a quest outcome (quest requests, inventory applies: Lowmark G08 effect executor; Stage 27 forbids the quest system mutating inventory directly). (2) A **location-bound readable copy** (conditional inspect prop) at whichever place matches the flag. The roster text is Act II's, unchanged (no names; margin rotted); TWN's earlier request for a new roster line was withdrawn in its review | TWN reads it in place (never carried again); TTH richer variant |
| `TSH_trial_record` | TSH S10 (bench) | Kept into TSW | Document with inspect text | TSW Assembly line ("dated against a Warden log"); TGM `S02b_dates` extra agreement |
| `TSW_closure_rubbing` | TSW S03, created by completing the third `rub_panel` | Kept after the Assembly | Document with inspect text (dialogue file D-2); seeds the CV-M3 chip | Act III `TSW-D9.51` reads TWN Completed (already authored; the "Brede on the rubbing" request was withdrawn); convergence |

All four: non-droppable, non-sellable, survive death; acquire steps auto-pass if already held; no duplicate grants (Lowmark §3.7 rule). **TI-QI-01** (SCE, IT): define the four with those properties. **TI-QI-02** (SE): quest-outcome removal of `TES_horn_roster` through the authorised request path. **TI-QI-03** (SCE): validator that the Thornfell quest-item count is exactly four. Shared: = LM G24, G08. Priority MUST.

### 2.11 Rewards and economy dependencies

**Rules (bible §11.5):** rewards are access, knowledge, tools, small payments and standing. **No lump quest XP**; skill XP comes from actions. No item exists until the item/economy pass defines it; reward tools are named functionally.

**Economy-pass dependencies EC-01…EC-14** (Work and Skills §0.3; TD-13: ridge iron, stormwood and goat leather are legacy concepts, not catalog items). Every quest is written to stand on coin, knowledge and station access if the pass derives nothing.

| Id | Working name | Consumer | Nearest approved state | Decision the economy pass owns | Blocks content? |
|---|---|---|---|---|---|
| EC-01 | seam ore | TSR output | none | Whether Thornfell has a mined ore state at all | No: ore goes to the seam rota; player share paid in coin |
| EC-02 | bar stock | TBC input | plain carbon steel stock | Steel stock or a derived ridge-iron state | No: Aud supplies stock |
| EC-03 | bridge fittings | TBC (installed at once) | none | Recipe | No: installed into the bridge (world state, TI-PP-03) |
| EC-04 | wind-tested stave billet | TST | ordinary wood (trimmings) | Bow-stave wood state; seasoning | No |
| EC-05 | first bow | TST reward | none | **S01 ranged scope** and recipe | No: the bow is a `[PROPOSAL — DIRECTOR]` layer gated on S01; the default is an unstrung stave racked at Brita's stall (TST.15). **Ranged is not a requirement here** |
| EC-06 | bowstring | TST (S01 layer) | flax linen and tow | String material | No (S01 layer only) |
| EC-07 | arrow shafts | TST (S01 layer) | ordinary wood | Shaft state or recipe | No (S01 layer only) |
| EC-08 | fletchings and arrowheads | TST (S01 layer) | none | Feather source; head metal | No (S01 layer only) |
| EC-09 | goat hide | TGY | raw hide | Raw hide or own state | No: TGY accepts either |
| EC-10 | goat-leather piece | TGY | vegetable-tanned leather | Thornfell tanning medium; smoke-finishing | No |
| EC-11 | ledge-grip wraps | TGY reward | none | Function (no stat assumed) | No |
| EC-12 | snowhare (food relationship) | TFS | pending food catalog | Food only; no pelt | No |
| EC-13 | hare stew / smoked hare | TFS | none | Eat-now and store foods; staples from the host's store (FT-03: no route) | No |
| EC-14 | fuel | TBC, TFS | wood charcoal; ordinary wood | Fuel stewardship | No: NPC stock |

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-RW-01 | **Reward and loaned tools** by functional name, none a quest item | IT defines: Hornbearer's practice horn (TPW; TI-SN-03); warden's horn (TSW fallback loan); rigger's sounding iron (TES); miner's sounding hammer (TSR, if lacking a tool); cutting saw (TST, lent then kept); Warden's spike straps (TSL); Bearer's thong, cosmetic (TWC); cairn-keeper's chisel, cosmetic (TWN); hostel lamp-hook (TSN); Warden's sheer-leg pulley (TOS); ledge-grip wraps (TGY, EC-11). Carry-state lends: Bera's herding horn (TGY fallback) | IT | Listed | = LM §6.3, I-08 pattern | SHOULD (each package has a no-item fallback) |
| TI-RW-02 | **Station bindings that persist as public workspaces** | Lowmark M40 station binding: Aud's field forge (TBC; also TPW S06 anvil cart), Nettlehook upper hearth + smoke-hood (TFS), Bera's shed chain beam/tub/stake/hood/bench (TGY), Brita's tillering bench (TST), Passwatch forge corner (TAS), Stonewright yard bench (TMM), wind butts (TST, S01 layer) | SE, IT | Listed | = LM G22, M40 | MUST for TBC/TGY/TFS; SHOULD elsewhere |
| TI-RW-03 | **Gathering and Hunting hooks** | Woodcutting gather events (TPW stakes, TST stool-cut, TSM optional); Mining (TES S03, TSR); Hunting approach / resolve / recover with wind-scent tied to the wind-window state (TGY cull, TFS snowhare, TSM, TGM optional butchering). Combat never grants Hunting recovery | SE, GD | Listed | = LM G23, M41 | MUST for TGY/TFS/TSR |
| TI-RW-04 | **Small payments** | Currency grants sized by economy tuning (Aud's day rate, Warden dues, finder's share, Brynjar's handful) | IT | Most quests | = LM | SHOULD |
| TI-RW-05 | **Commission-giver flags and the master-commission gate** | Flags `TBC_AUD_BENCH`, `TST_BRITA_BENCH`, `TGY_BERA_SHED`, `TSR_SEAM` mark givers; `TH_STANDING` opens four master commission offers (Act III §E.8). The offer only opens a commission; skills, materials and stats belong to the economy pass | SCE, IT | TSW S12; Work and Skills §0.4 | = LM `LM_CIVIC_STANDING` pattern | SHOULD |
| TI-RW-06 | **Access unlocks** | Route/state unlocks: high routes ×3 (TSH), cage shortcut (TIW), Line route (TWG), ropeway (TNR), goat steps (TGY), Splitpine fixed line (TSL), oath path (TOS), kept beds / rest points (TTH, TSM), Gatefall horn post (TSW) | SE, ZN | Listed | ext LM G21 | SHOULD |
| TI-RW-07 | **Vendors** | Gerrit's crew (rope and irons) at Carrick's Cut; Bera's shed (bounded intake) | IT | TES, TGY | = LM D-INT-10 | COULD (economy pass) |

### 2.12 Encounter behaviour and yield

| Id | Requirement | Minimum viable form | Owner | Consumers | Shared? | Priority |
|---|---|---|---|---|---|---|
| TI-EN-01 | **Defeated humans yield** (TD-7): kneel or sit and are tied (prop); never killed on screen | Lowmark M18 / EV08 yield outcome | SE, GD | TPW-E1 bandits and Corner-Boss (yields last); TIW crews; TSH-E2/E3 crews; TSW gallery crews; TWG bandit lookout; TSG brigands and foreman; TAS; TBC bandits | = LM M18, I-05, D-INT-4 | MUST; rule **[DIRECTOR]** (TD-7 open, same as Lowmark D-13) |
| TI-EN-02 | **Encounter-level surrender trigger** | First yield, or ~60 s, or fight within range of a named non-combatant → every remaining member yields | GD, SE | TIW-E5 (Bersi); TSW (crew sit when Ingrith yields) | TH only | MUST |
| TI-EN-03 | **Threshold yield boss with phase checkpoints** | Fight ends at ~20% HP (no further damage); phases at 100 / 60 / 35%; death resets to the top of the current phase; logout restarts at 100%; yielded crew stay yielded | GD, SE | TSW-E4 Ingrith | = LM M35, M18 | MUST |
| TI-EN-04 | **Non-combatant stopped by interaction** | Eyvind never attacks; `take_horn` channel stops him and he yields | GD | TSH S08 | TH only | MUST |
| TI-EN-05 | **Fleeing non-enemies** | Hires drop spears and run; not counted | GD | TIW-E1 | TH only | SHOULD |
| TI-EN-06 | **Call-driven enemy behaviours** | Hornman raise 1.5 s, then `Gather`: allies within 8 m attack faster for 8 s, or summons reinforcement; any hit in the raise interrupts; the player's Rest within 3 s cancels. Howler draw 1.5 s; a completed howl adds +1 runner once (TPW-E3 +2); any call blown at a howler makes it flinch; bandits duck once on Fall. Wolves break off at 30% and break-off counts as defeat [PROPOSAL — DIRECTOR] (§5 C-3 to C-5) | GD, ENC | TIW-E1/E4/E5, TSH-E2, TSW hornman (slab drop on Close); TPW, TST, TTH howlers; TWG | TH only | MUST |
| TI-EN-07 | **Re-forming resonance figures tied to a storm window**, not to a site store | Echo-figures spawn on a swell, charge along authored lanes (no tracking), break on hit, re-form on a timer while the window allows; **no nameplate, blank target frame**. The Held Line: seven-figure formation with a surge per swell; persisted swells-endured counter; the window turns at 4. Uphill group: non-hostile, passes through the player | GD, ENC | TES S04–S06; Shatterfall storm event revisitable after TES | ext LM M09 (no drift-site state) | MUST |
| TI-EN-08 | **Hazard that is not an entity** | Node pulse ring AoE from a fixed point (TI-CK-06); pillar-shadow and alcove volumes modify damage; **no entity, no target frame** (C11) | GD | TSH | TH only | MUST |
| TI-EN-09 | **Telegraphed hazard volumes** with HP floors | Every hazard cannot kill above 25% HP (§5 C-2). Gust push (never off a ledge); TSL iron hum then strike with 10% HP floor and lee notch; TSR slab drop; TSW shed and loose deadfalls; TSH air-channel draw (torch-lean tell, one-step push, lantern out); TMM-H1, TAS-H1 | GD | Listed | = LM M30 | MUST |
| TI-EN-10 | **Silent-arena miniboss**: visual-only telegraphs with fixed durations | Dust jumps, frost ring, dust shadows, pillar trickle; dust-curtain partial occlusion; charge-into-pillar stun; rumble on impacts | GD, ART | TGM | TH only | MUST (see TI-AX-03) |
| TI-EN-11 | **Cutter work bars that pause when engaged** | NPC channel that stops on aggro and resumes; terrace drop gated on both props cut **and** all three Answers | GD, SE | TSG | TH only | SHOULD |
| TI-EN-12 | **Animals and fauna fought as animals** | Ridge bear (Greymantle), ram (fixed charge lane, stamp telegraph), crows (flock/diver; vent draughts suspend diving on a whistle tell), wolves, vipers (TSR first-appearance tuning), fell stags | ENC | TGM, TGY, TIW, TNR, TPW, TSR | = LM fauna | MUST |
| TI-EN-13 | **Combat never reveals evidence** | Validator: no evidentiary item or flag is a combat drop | SCE | All (bible §11.3) | = LM rule | MUST |
| TI-EN-14 | **Step-gated encounter pockets** and state-scaled crew counts | Spawn rules reading `TH_STORES` (TSH-E3 crew count; TSW crew strength; `seized` leaves G5 unmanned) and `TSH_MAP_TIER` (entry route and start state) | SCE, SE | TSH, TSW | = LM G13 | MUST |

### 2.13 Agility triggers and walkable fallbacks (click-to-move)

Every agility trigger is an optional shortcut with a walkable fallback (Phase 1.3; bible §9.5). The client today has a flat NavMesh with no jump and no off-mesh links (Lowmark G21), so **multi-level navigation is a MUST** even where the agility trigger itself is optional.

| Id | Trigger | Walkable fallback | Quest |
|---|---|---|---|
| TI-AG-01 | Goat-track gap step above the Blind Corners | 15 s scramble round the back of a boulder (Act I Beat 3); the road through the Corners also stays open | TPW S03 |
| TI-AG-02 | Traveller basket on the guide line (ride) | Scree path | TPW S08 |
| TI-AG-03 | Cliff-ledge route round the Muster Hut | Through the yard (a route choice, not stealth) | TIW S04 |
| TI-AG-04 | Shaft crossbar step; wound cage as two-stop lift | The rungs (interaction-driven "climb to next ledge", rest ledges, gust "hang on"); cage optional | TIW S05, S05b |
| TI-AG-05 | Shelf gap; seat scramble | Ledge paths | TES S02, S07 |
| TI-AG-06 | Broken flight on the Summit stair | Quiet Passage / open stair by map tier | TSH |
| TI-AG-07 | **High routes**: Crown Traverse, Iven's High Path, Rim Way | Existing valley roads (longer) | Unlocked by TSH |
| TI-AG-08 | Splitpine chimney | Goat ramp to the warden ring, then clip-and-climb line stations (channelled) + one rappel channel | TSL |
| TI-AG-09 | Oath path down-climb | Walk round | TOS |
| TI-AG-10 | Goat steps | Round the shoulder | TGY reward |
| TI-AG-11 | Signal Terrace plank (via the TIW hoist-cage reuse) | Stair to the plank's niche | TMM |
| TI-AG-12 | Gate arch; den ledge; ledge traverse; siege-engine frame | Named fallbacks in each place table; TDS06 ledge ramp | TAS, TGM, TSG, TDS06 |
| TI-AG-13 | Tower ladders and ice | Ladder left at T2; ice cleared at T3 | TWG |

**TI-AG-R1** (SE, ZN): agility triggers as Phase 1.3 trigger boxes; **TI-AG-R2** (SE, ZN): multi-level NavMesh for the hoist shaft, the Summit stair, gorge ledges, towers, the Gatefall galleries and the ropeway; **TI-AG-R3** (SE): moving platforms on splines with stop points and gust events (TNR ropeway car; TPW basket; TIW cage). Shared: = LM G21, M43, M26. Priority: R1 SHOULD, R2 MUST, R3 SHOULD (TNR fallback: fixed scripted ride).

### 2.14 Co-op rules

| Id | Rule | Requirement | Consumers | Shared? |
|---|---|---|---|---|
| TI-CO-01 | Independent instances | Each player has their own instance of every quest; no group quest state | All | = LM §8.1 |
| TI-CO-02 | Shared creatures, per-step credit | A defeat credits every participant whose own active step consumes it; shared boss health scales per participant; TSW "the Count" rotates targets | All combat; TSW-E4; TGM | = LM EV07 |
| TI-CO-03 | Per-player choices, flags and items | Including `TH_STAND` and each partner's own computed posture; each partner holds their own rubbing and ledger (per-player desk prop) | All | = LM §8.1 |
| TI-CO-04 | Per-player clocks and weather | Close count, storm windows, blizzard, wind-window timer are per player; partners see their own | TPW, TES, TSW, TSL, TSN, TOS | ext LM §8.1 |
| TI-CO-05 | Shared surrender / yield scene | TIW: Bersi's surrender is shared, testimony per player. TSW: each partner sees their own yield scene; fallback shared scene with options for every partner | TIW, TSW | TH only |
| TI-CO-06 | Prop fallback when per-player props are not ready | **Three different fallbacks are authored** (host's state; first choice in the shard; first player changes the world for everyone). See Q-06 | All | = LM §8.1 fallback |

### 2.15 Accessibility

Thornfell makes sound the readable system, so it carries more audio-only cues than Lowmark. The bible already requires glyphs (§1.1, §9.4). Each row is a requirement on the listed owner.

| Id | Audio-only (or visual-only) cue | Required equivalent | Owner | Consumers |
|---|---|---|---|---|
| TI-AX-01 | Every horn call, heard or blown | Call glyph in source direction, echo glyph delayed and dimmer, caption; works with audio off | UI, AU | All call users |
| TI-AX-02 | Echo count, strike returns, ring/clack, clean/doubled, lid tick vs rattle, stem whistle | **Beat-dots or return glyphs** for every authored return (never a meter or colour code; Work and Skills §0.6); log line; subtitle cue + rumble for TST stems; TBC ring/clack and TFS lid sound need a visual tell (spark, steam, lid jump) as well as the audio | UI, AU, ART | TES, TSR, TBC, TAS, TWN, TOS, TGY, TWG, TNK, TST, TFS, TSW |
| TI-AX-03 | **TGM silent den** (no audio by design) | Visual-only telegraph set with fixed durations (the reference case); rumble; visual hit flashes; subtitles only for Yrsa past the threshold. **Do not mute UI sounds** until the Director and the accessibility review rule TGM-OD1; same question for TSH's ~3 s total silence (TI-SN-15) | GD, AU, UI | TGM; TSH |
| TI-AX-04 | Wind-window whistle tell | Small rising-wind glyph in the call-glyph area (TMM-H1 pattern) for every gust site | UI | All TI-SN-10 sites |
| TI-AX-05 | Timing inputs | Toggle or untimed alternative: TWG held call (toggle); TSL brace (timing window: needs an assist or untimed option); TFS story delivery (the authored choice fallback); call wheel already has no rhythm input | UI, GD | TWG, TSL, TFS |
| TI-AX-06 | Directional listening | Subtitles naming direction and source (TSH listening points; TMM "(from the far gallery)"; TWC voice at the stone) | UI | TSH, TMM, TWC, TSW |
| TI-AX-07 | Haptic-only moments | Visual shiver + subtitle fallback | AU, ART | TME05, TAS arch note, TGM |
| TI-AX-08 | Whiteout visibility | Readable character outline; directional glyphs; rope boundary volumes with a bark; assist pin after 45 s | UI, ART | TSW |
| TI-AX-09 | Stormlight flashes | Photosensitivity option (reduce flash intensity / frequency) for lightning sequences | ART | TSL (numbered third flash), TDS07, TDS08 |

---

## 3. Flag register

### 3.1 Region flags `TH_*` (character-scoped; bible §9.1 only)

No package creates a `TH_` flag outside this list (checked in all seven packages). Each has exactly one writer.

| Flag | Type | Values | Set by (quest / step) | Read by | Notes |
|---|---|---|---|---|---|
| `TH_CALLS` | bool | true | TPW `S01_calls` | Call glyphs everywhere; call wheel; all milestones; TTH/TWG/TNK; TGY; TAS, TSG, TME05, TME10, TDS03, TDS10 | Always true after TF-M1 (required step). TSW authors a fallback if ever false |
| `TH_PASSWATCH_ROUTE` | enum | sledge / caravan / split | TPW `S09_choose` (`TPW-D4`) | TIW (Brynjar's ledger line, Elira's closing); TNR; TBC-D1; TSW posture (sledge +1 open), Ketil placement, Nettlehook epilogue | — |
| `TH_STORES` | enum | reported / seized / leverage | TIW `S12_stores` | TSH-E3 crew count, `TSH-D10.20`; TSW gallery crews, boss phase 2, Ingrith lines, posture (leverage +1 sealed), Whinstone epilogue; TMM, TAS variant lines; Act III §E.8 Aud line | `leverage` only offered on the private route (`TIW-D7.50`) |
| `TH_BRYNJAR` | enum | disowned / defended | TIW `S11_brynjar` (private → disowned; public → defended), on the first of `TIW-D7.01` / `TIW-D8.01` | TWC; TSH post-quest barks; TSW placement, posture (±1), tribunal line; TMM, TAS | Always set by TF-M2 |
| `TH_SHATTERFALL_ACCOUNT` | enum | amended / beside / kept | TES `S10_choose` | TWN (roster location, testimony length); TSG Dorn line; TSW Maera placement, posture (amended +1 open, kept +1 sealed), reader line | Also selects the `TES_horn_roster` readable location (§2.10) |
| `TH_HORN` | enum | silenced / broken / surrendered | TSH `S11_choose` | TNK (store contents, `TNK_PLATES`); TSW lines, Kaldren's attendance, epilogue | Lines and props only; never posture |
| `TH_THIRD_HORN` | bool | true on every TTH completion path | TTH `S10_keeper` | TSW S07 (player blows the restored reply; otherwise Dorn blows Answer); TSW Assembly line; TNK; convergence | Not a posture input |
| `TH_HUSHFOLD_VOICE` | bool | true for `TSM_CLAIM` = counted / shared; false for private | TSM `S07_reading` | TSW Runa placement, posture (+1 open), reader | — |
| `TH_HIGHSTEADS_TOGETHER` | bool | true for `TRR_RIBBON` = everyone / witness; false for old_line | TRR `S06_ribbon` | TSW placement (Nettlehook beside Hushfold), posture (+1 open), Ketil/Aud/Runa lines | — |
| `TH_BANNER` | enum | blood-oath / hearthguard / shared | TWC `S07_lay` | TSW Torvek and banner placement, posture (blood-oath +1 sealed); banner prop; barks | Hyphen in a value: use `blood_oath` in data (as Lowmark I-03) |
| `TH_COLUMN` | enum | player_brought / patrol_brought | TSW `S07_stragglers` end | TSW Assembly lines, posture (player_brought +1 open), placement; epilogue; convergence | `player_brought` only if both stragglers came in on the player's line |
| `TH_STAND` | enum | hushfold / wardens / cairn / brynjar | TSW `S10_stand` (volume + confirm) | TSW posture (hushfold, cairn +1 open; brynjar +1 sealed; wardens 0); epilogue lines | — |
| `TH_SEASON` | enum | autumn / snow | TIW `S13_elira` step start (→ snow) | All presentation; unlocks of TSL, TSN, TFS, TSM, TME01; TGM | Thaw: quest-local `TSW_THAW` (TI-SE-04, §5 C-7) |
| `TH_ASSEMBLY_POSTURE` | enum (derived) | watchful / open / sealed_with_terms | TSW `S11_reading` (TI-FL-05) | TSW-D9.70–.90; epilogue §E; TNK variants after TF-M5; convergence | Start watchful; open − sealed ≥ 3 → open; ≤ −2 → sealed_with_terms |
| `TH_HORN_CODES` | enum | kept / pruned | TNK `S03_book` | Convergence alarm network (CV-M2); CV-M1 R16 custody (request) | No Thornfell gameplay reader |
| `TH_STANDING` | bool | true | TSW `S12_close` | Thornfell master commissions (§E.8); LR-M1; CV-M1 via `LR_STANDING` | Always true at TF-M5 completion |

### 3.2 Quest-local flags read by other packages (must survive completion)

| Writer | Flags | Readers |
|---|---|---|
| TPW | `TPW_NAMES_ASKED`, `TPW_WHINSTONE_ASKED`, `TPW_SACKS_SEEN`, `TPW_BOARD_SEEN`, `TPW_CREW_FITTINGS` | TSW-D8 Vessa; TTH; TIW-D2/D3; TBC Aud line |
| TIW | `TIW_LEAD_CHIT`, `TIW_GULLY_HEARD`, `TIW_SKETCHES_SEEN`, `TIW_PLATES_SEEN`, `TIW_FRAME_TOUCHED`, `TIW_GATHER_CANCELLED`, `TIW_SACKS_INSPECTED`, `TIW_BERSI_TESTIMONY`, `TIW_CAGE_WOUND`, `TIW_BROADSHEET_READ`, `TIW_LOWMARK_RECOGNISED` | TES; TSH (Kaldren, Iven, offer); TTH/TNK (Dorn); TSW; EH-M1 and convergence (optional) |
| TES | `TES_CHITS_READ`, `TES_UPHILL_SEEN`, `TES_RECORDS_SET`, `TES_THIRD_HORN_HEARD`, `TES_NAMESLIP_SEEN` | TSH-D1/D10; TTH richer variant; TWN |
| TSH | `TSH_NULL_TAUGHT`, `TSH_RECORDS_SET`, `TSH_NAMED_QM` | TNK, TME05; TSW (Ingrith's opening assumes her name) |
| TSW | `TSW_HORN_LOANED`, `TSW_ROSTER_READ`, `TSW_INGRITH_WALL`, `TSW_READER`, `TSW_ODDNY`, `TSW_HALVARD`, `TSW_THAW` | IT (horn); epilogue |
| Horn and Highsteads | `TTH_KEEPER`, `TWG_CALL`, `TNK_PLATES`, `TNK_EYVIND`, `TNR_ROTA`, `TSM_CLAIM`, `TSM_PLAYER_TALLIED`, `TRR_RIBBON` | TSW; TNK code book; TSM, TRR; CV-M1/M2 (requests) |
| Banner and Memory | `TSL_STAFF_*`, `TSL_COMPLETE`, `TWC_COMPLETE`, `TWN_COMPLETE`, `TWN_MIRE_HOOK` | TWC unlock and rite; TWN tally-stick variant; TSW `TSW-D9.51` (TWN Completed; already authored); Mire (R14, no Thornfell reader) |
| Settlements and Combat | `TMM_ACCOUNT`, `TMM_BUNDLE_SEEN`, `TAS_ACCOUNT`, `TGM_OUTCOME`, `TSG_LEDGE`, `TSG_SPOIL`, `TME01_TALLIED`, `TDS10_SEEN`, `TDS10_READ` | TSW (Hadrik line, request; `TDS10_READ` gallery bark; `TME01_TALLIED` name address); LR-M1; Emberholt (request); TSN; TSR |
| Work and Skills | `TSR_SEAM`, `TSR_VOID_MARKED`, `TST_STEM`, `TST_BRITA_BENCH`, `TGY_WAY`, `TGY_STEPS_SEEN`, `TGY_BERA_SHED`, `TFS_HARE`, `TFS_STORY`, `TFS_VERSE_ASKED`, `TBC_WAITS`, `TBC_WAIT_NAMED`, `TBC_AUD_BENCH` | Master commissions; TES coda (Gerrit); TWN; TSM; TRR; TTH; TSW Aud line (request) |

"(request)" rows are optional lines another package was asked to add; nothing depends on them. The validator (TI-QS-12) should report a request whose reader was never authored, not fail on it.

### 3.3 TF-M5 posture inputs (validator target)

Inputs: `TH_STAND`, `TH_HUSHFOLD_VOICE`, `TH_HIGHSTEADS_TOGETHER`, `TH_SHATTERFALL_ACCOUNT`, `TH_BRYNJAR`, `TH_COLUMN`, `TH_PASSWATCH_ROUTE` (toward open); `TH_STAND`, `TH_BRYNJAR`, `TH_STORES`, `TH_BANNER`, `TH_SHATTERFALL_ACCOUNT` (toward sealed). Side-quest inputs may be **unset** (quest not played): unset counts 0. Act III §9.3 lists five worked examples; they are the acceptance cases for TI-FL-05. `leverage` always arrives with `disowned` (intended balance).

---

## 4. Server events Thornfell adds to the Lowmark vocabulary

Thornfell uses Lowmark EV01–EV26 unchanged. New or extended events (requirement labels only):

| Event | Payload (minimum) | Notes | Used by |
|---|---|---|---|
| `call.blown` | player or NPC id, call shape, position, volume id, hold duration | TI-SN-01; listeners in TI-SN-06 | All call users |
| `echo.returned` | emitter, face id, authored result | Presentation and step predicate ("echo count blown twice", TPW S04) | TPW, TSW, TOS, TGY, TWG, TNK |
| `strike.result` | player, target, authored result | TI-SN-09; also a predicate (TSR lever accepted only after a doubled return; TES irons) | TES, TSR, TBC, TAS, TWN |
| `wind.state_changed` | site, state (lull / whistle / gust) | Consumed by channels (pause), NPC movers (stop on whistle), hazards | TI-SN-10 sites |
| `listen.performed` | player, listening point, mix id | TSH S04 (×3) | TSH |
| `sketch.committed` | player, marks, computed tier | Sets `TSH_MAP_TIER` from an authored answer key | TSH S07 |
| `storm.window_changed` | player, quest, window index | TI-CK-03 | TES, TSL, TOS |
| `countdown.advanced` | player, counter id, value | TPW Close count | TPW |
| Named script events (server timed, once per player unless repeatable) | — | `passwatch.close_early`, `passwatch.rest`, `whinstone.gully_quiet`, `whinstone.frame_hum`, `tsw.blizzard_start`, `tsl.stormlight`, `tsl.ridge_seen` (client-reported, never gating), `tsn.snowlight`, `twn.set`, `tos.oath`, TES storm windows, TSH silence | Listed |

---

## 5. Conflicts and open questions for Sol

**Shared canonical register (canonical for implementation; quest packages defer to this register).** Added in the independent review of 2026-11-03. The three Batch 4 handoffs (Enemies, Zones, Integration) state these values in the same words. Where a quest package gives a different number, the package value is superseded for implementation; the package text changes only when its author next edits it.

| # | Topic | Canonical value |
|---|---|---|
| C-1 | Wind window | Fluted face whistles up a fifth **2.5 s** before a **3 s** gust. The gust pushes **2 m toward the defined safe side** with light damage, no knockdown, never off an edge; a marked shelter negates it. TF-M5 whiteout adds a 3 s slow; climbing stances keep "back to the last stance / hang on". One exception: TST stand-cutting gusts last ~6 s (a labelled "long gust"; same 2.5 s tell). |
| C-2 | Hazard clamp | No hazard can kill a player above **25% HP**; TSL-H2 stormlight clamps at **10%**. |
| C-3 | Hornman | Raise **1.5 s**; Gather gives allies within 8 m faster attacks for **8 s**; any hit during the raise interrupts; the player's **Rest within 3 s** cancels it in every hornman pocket. |
| C-4 | Howler and calls | Draw **1.5 s**; a completed howl adds **+1 runner once** (TPW-E3 keeps +2 as authored escort pressure). Any call blown at a howler makes it flinch; Fall also makes bandits duck once per fight. |
| C-5 | Ridge Wolves at low health | At or below 30% HP a wolf breaks off and limps away; **break-off counts as defeat** (step credit and co-op credit as a kill). **[PROPOSAL — DIRECTOR]**; if refused, wolves fight to 0% and only text changes. |
| C-6 | Narrows bridge (TP07) | One per-player state machine, owned by the Zones package: **N0 down** (before TPW `S08_span`) → **N1 patched** → **N2 cracked only while TBC is Active** (overrides N1, N3 or N4 for that player) → **N3 mended** (TBC Completed) → **N4 permanent span** (TRR Active or Completed). Before TBC is accepted the bridge shows its ordinary state and TBC is offered by Aud's bark after a storm. The scree path is walkable in every state. |
| C-7 | Season and thaw | `TH_SEASON` has two values: autumn, then snow from TIW `S13_elira` start. Thaw is the quest-local bool `TSW_THAW` (first re-entry to Thornfell after TF-M5 Completed and leaving the region once) **[PROPOSAL — DIRECTOR; Act III open decision 3]**; no third `TH_SEASON` value. |
| C-8 | Ranged | Never required. While S01 is open every Ranged counter is optional and has a melee, brace or call alternative; TST's default is the racked unstrung stave. |

Items marked **[DIRECTOR]** need a Director ruling as well; Sol is asked only for the runtime view.

| # | Topic | What differs or is open | Where | Recommendation (for Sol to accept or replace) |
|---|---|---|---|---|
| Q-01 | Wind-window timings | Tell is "~2 breaths" (TPW A12), "~2.5 s" (TES, TSW), "~1.5 s tell, ~3 s gust" (Banner and Memory §0.3; TMM-H1 with a 12–18 s period), ~3 s (Work and Skills) | Act I, II, III; side files | **Resolved by §5 C-1:** tell 2.5 s and gust 3 s everywhere (TST long gust ~6 s); only the **period** is per site. Package tell values are superseded, not overrides |
| Q-02 | Echo-count implementation | TSW asks for a raycast to the nearest `echo_face` by distance band; every other package uses authored per-face returns | Act III §12; TPW, TOS, TGY, TWG, TNK | Authored per-face returns everywhere (TI-SN-08); TSW bands become face tags. No physics |
| Q-03 | Horn carrier | Resolved in the committed packages: TF-M1's Hornbearer's practice horn is the carrier; TTH, TGY and TSW loans are fallbacks only. Open: whether the item pass makes it droppable (which would make the fallbacks reachable) | Act III open decision 4; Horn and Highsteads §0.6; Work and Skills §0.6 | Make it non-droppable; keep the fallbacks as dead-path safety |
| Q-04 | Quest-item removal by outcome | `TES_horn_roster` leaves the pack at TES S10; Stage 27 forbids the quest system mutating inventory | Act II §A9.2, §A12 | Route through the Lowmark G08 request/apply path; no change to Stage 27 |
| Q-05 | Narrows bridge state | TPW, TBC and TRR each change the per-player Narrows prop (patched, cracked, repaired, permanent) | TBC.11, TBC open question 4; TRR rewards | **Resolved by §5 C-6:** cracked only while TBC is Active; one per-player state machine (TI-PP-03) owned by the zone package; TBC.1 and TBC.11 now agree |
| Q-06 | Co-op prop fallback rule | Three fallback styles: host's state (most packages); first choice in the shard sets the visible state (TES cairn, TSH alcoves); first player changes it for everyone, later players complete on inspect (TSL, TSN, TOS) | Act II §A11, §B11; Banner and Memory §1.12, §4.12, §5.12 | Pick one shard-level rule for v1.5 (recommend "first choice in the shard", which Lowmark §8.1 also describes) and keep every player's own flags |
| Q-07 | Set-piece controllers | Gallery call sequencer, node pulse rhythm, storm windows with swell counter, sketch tiering, column hold, crossing board (TBC), rota board (TNR), peg board, gate band–style state machines | Act I–III; side files | Same as Lowmark **D-INT-1**: one generic data-configured set-piece component; no per-quest scripts in the evaluator (Stage 15.3) **[DIRECTOR]** |
| Q-08 | Client-reported events | `tsl.ridge_seen` is reported by the client. Nothing is gated on it (one optional Iven line) | Banner and Memory §1.13 | Accept only as presentation-adjacent (Lowmark M25); confirm no predicate may read it |
| Q-09 | UI muting in silence | TGM-OD1 proposes muting UI sounds in the den; TSH silence mutes UI ~3 s | Settlements and Combat TGM-OD1; Act II §B12 | Do not mute UI until the accessibility review rules **[DIRECTOR]** |
| Q-10 | Thaw | `TSW_THAW` quest-local state vs a third `TH_SEASON` value | Act III open decision 3 | **Canonical (§5 C-7):** quest-local `TSW_THAW`; `TH_SEASON` stays two-valued **[DIRECTOR]** |
| Q-11 | Zone-entry activation | TSW goes Active on entering Windscar Pass or Stonewake after TF-M4 | Act III §9.1 | Express as an explicit offer trigger with accept-on-offer (Lowmark G05, I-21) |
| Q-12 | Crowd sizes | TSW column ~31 NPCs + goats and sledges; TRR 12 children | Act III §12; TRR.11 | Authored fallbacks (10–12 walkers; six children) are acceptable ship states; Sol to set the budget |
| Q-13 | Timed inputs | TSL brace timing window; TFS timed delivery; TWG ≥ 5 s hold | TSL.13, TFS.11, TWG.13 | Untimed alternatives (TI-AX-05); confirm the input model allows a toggle |
| Q-14 | Yield rule | TD-7 is still `[PROPOSAL — DIRECTOR]`, as Lowmark D-13 / I-05 | Bible §3 | Build one yield mechanic for both regions (Lowmark D-INT-4) **[DIRECTOR]** |
| Q-15 | Ranged | TST's bow and wind butts are a `[PROPOSAL — DIRECTOR]` layer gated on S01 (Stage A contradiction register) | Work and Skills §0.3, TST.11/15 | **No ranged requirement** in this handoff (§5 C-8); the TST default (racked stave) needs nothing from the Ranged system. Act III §E.8's "Stormwood war-bow" is an offer only; its Ranged content waits on S01 **[DIRECTOR]** |
| Q-16 | Act III review-log wording | Act III's integration table closes the flag names as `TDS10_READ` and `TME01_TALLIED`, but its 2026-11-03 review row still mentions `TDS10_SEEN` as a placeholder | Act III §12, §15 | Text only; the data reads `TDS10_READ`. Note for the Act III author, no runtime impact |
| Q-17 | Name collisions (line keys) | **Closed 2026-11-03.** The TSM household is renamed Kvist (was a clash with Lowmark's Sedge); TSR's Asa Grell was renamed Dagny Grell in the Batch 3 review | Horn and Highsteads §0.2; Work and Skills §0.4 | None |
| Q-18 | Gallery sealing calls | New wartime calls ("Close plus a tag") need audio and glyphs; the Split must never be reproduced | Act III open decision 7; bible §9.4 | Add a validator rule that no data shape or audio asset represents the Split |
| Q-19 | TNK window | TNK unlocks after TF-M4 + TWG but its practical window is after TF-M5 (reads `TH_ASSEMBLY_POSTURE`, `TH_COLUMN`) | Horn and Highsteads §0.3, TNK.16 | Unset-safe reads are enough at runtime; the window is a design decision |

---

## 6. Director-level items

| # | Item | Content affected | Recommendation |
|---|---|---|---|
| TDI-1 | Generic set-piece component (Q-07) | TPW, TES, TSH, TSW, TBC, TNR, TTH/TWG/TNK | Same component as Lowmark D-INT-1; approve once for both regions |
| TDI-2 | Yield mechanic (Q-14) | All human encounters | Same as Lowmark D-INT-4 |
| TDI-3 | Owner-visible NPCs (TI-PP-06) | TIW Brynjar, TSW stragglers | Do not build; ship shared-NPC fallbacks (Lowmark D-INT-2) |
| TDI-4 | Keep-watch as a per-player quest clock, extended with countdown and storm windows (§2.6) | 20+ packages | Approve together with Lowmark D-INT-6 |
| TDI-5 | Thaw (Q-10), UI muting (Q-09), ranged S01 (Q-15), names (Q-17) | As listed | Rule before data authoring |
| TDI-6 | Open bible decisions that block data but not runtime | TD-1 splinter (`[SPLINTER]` tags), TD-6 map (MAP VERIFICATION REQUIRED everywhere geometry matters), TD-8 Gatefall mechanism, TD-13 economy | Swap layers are tagged; runtime is unaffected |

---

## 7. Not in initial release scope

Thornfell is **future-region authoring**. Nothing in this file is a v1 requirement, a schedule or a request to build. It does **not** expand the initial release scope, which remains Lowmark only (bible "Scope guard"; Phase 1.3). Where a capability is marked `= LM`, the Lowmark handoff already asks for it; Thornfell asks only that it be built so that a later region can reuse it, not that it be built sooner or larger. `TH only` capabilities (chiefly the sound system, §2.4) are needed only when Thornfell is scheduled. This file does not alter Stage 15.2, Stage 27, `QuestRuntimeSystem.cs`, any schema or any runtime architecture; it cites them.

---

## 8. Internal review log

| Check | Result |
|---|---|
| Coverage | Every "Integration needs" table in Act I (A12, B12), Act II (A12, B12), Act III (§12) and the four side files (each quest's table plus the file-level summaries, TME01–TME10, TDS01–TDS10) is represented once in §2. Duplicates merged: call wheel, glyphs, echo returns, null-points, wind windows, keep watch, segmented channels, carry, per-player props, side-by-side view, sounding interaction. |
| Lifecycle | Cites Stage 15.2 (2026-11-02 revision), Stage 27 and `QuestRuntimeSystem.cs`; three states only; no fail, abandon or reset requirement anywhere. |
| Flags | 16 `TH_` flags, all from bible §9.1, each with one writer. Cross-package quest-local reads listed. Committed names used: `TDS10_READ`, `TME01_TALLIED`, `TST_BRITA_BENCH`. |
| Quest items | Exactly four; side content adds none. |
| Economy | EC-01…EC-14 carried from Work and Skills §0.3; none blocks content; ranged (S01) is not a requirement. |
| Accessibility | Every audio-only cue found has a named visual or haptic equivalent (§2.15); TGM silent den kept as the visual-only reference case. |
| Scope and authority | No schema, JSON, C# or contract change; requirement labels only; "not in initial release scope" stated (§7). |
| **Reconciliation check needed** | The packages were under independent review while this file was written. A first pass was reconciled on 2026-11-03 against the committed, reviewed packages (Act III flag names, the TST S01 layer, the Brita Crane rename, the horn resolution). **After any further review or fix pass lands, re-run this check**: re-read each package's integration, flags and items tables and diff them against §2, §3 and §2.10. |
| **Independent review (2026-11-03)** | 7 findings (1 high, 4 medium, 2 low). Grep checks: every flag named exists in the packages (incl. `TDS10_READ`, `TME01_TALLIED`, `TSM_PLAYER_TALLIED`, `TST_BRITA_BENCH`); 16 `TH_` flags match bible §9.1; exactly four quest items; no stale names. High: §2.10 and §3.2 still carried TWN's withdrawn requests (a "Brede, up past the Seat" roster line; a Brede on the rubbing); now read Act II's roster unchanged and Act III's authored `TSW-D9.51`. Medium: TI-EN-06 gave the howler two runners, a hornman buff without the 1.5 s raise, and Fall-startled wolves; aligned to C-3/C-4. Medium: TI-SN-10 gust "one step, small damage" and Q-01's per-site tell overrides conflicted with the Enemies register; now C-1. Medium: TI-PP-03/Q-05 bridge model made canonical (C-6; cracked only while TBC Active) and TBC edited to agree. Medium: TI-SE-04 thaw "undecided" now states the canonical proposal (C-7). Low: TI-AG-01/04/08 fallbacks corrected to the packages (15 s boulder scramble; rungs; goat ramp). Low: Q-15 notes Act III's war-bow commission is an offer only. Scope, three-state lifecycle, no contract change, no Remnant, no grain route re-checked. |
