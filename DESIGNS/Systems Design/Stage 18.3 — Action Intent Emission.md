# Stage 18.3 — Action Intent Emission

## 1. Purpose

This document defines the **structural conversion of NPC decisions into action intents**.
It establishes what an NPC action intent is, how intents are emitted from selected decisions, and the authority, ordering, and safety constraints governing that emission.
This document introduces no behavior execution, AI logic, or content semantics.

## 2. Action Intent Definition

An **NPC action intent** is a server-authored, structural instruction describing a single prospective action to be evaluated and resolved by existing intent-driven runtime systems.

**Intent Characteristics**
- An action intent **is a structural instruction only**.
- An action intent **does not execute behavior directly**.
- An action intent **does not mutate NPC, player, or world state at emission time**.
- An action intent **is consumed by downstream runtime systems** (e.g., combat, movement, interaction).
- An action intent **is compatible with existing intent-resolution systems** and does not redefine them.

An action intent represents *requested execution*, not *guaranteed outcome*.

## 3. Decision-to-Intent Mapping

**Mapping Rules**
- A selected decision **must** produce exactly one of the following outcomes:
  - An explicit no-op outcome producing zero intents, or
  - Exactly one action intent
- A decision **must not** produce more than one intent.
- A decision **must not** emit an intent implicitly or indirectly.

**Mapping Constraints**
- Intent content **must** be bounded, structural, and non-executable.
- Intent content **must not** encode AI logic, tactics, or behavior sequencing.
- Intent content **must not** bypass validation or authority checks in consuming systems.

## 4. Intent Emission Rules

**Emission Timing**
- Intent emission **must** occur only after decision selection is complete.
- Intent emission **must** occur only at server-defined tick boundaries.
- Intent emission **must not** occur mid-tick.

**Emission Authority**
- Intent emission **must** be fully server-authoritative.
- Clients **must never** emit, modify, or suppress NPC intents.

**Emission Effects**
- Emission **must not** mutate world, NPC, or player state directly.
- Emission **must** result only in intent availability for downstream systems.

## 5. Ordering & Tick Alignment

**Ordering Guarantees**
- Decision selection **must** complete before intent emission.
- Intent emission **must** complete before intent consumption.
- Intent consumption **must** occur within existing intent-resolution phases.

**Tick Alignment**
- NPC action intents **must** follow the same tick alignment rules as player action intents.
- NPC intents **must not** be emitted or consumed unless the NPC is tick-participating.
- NPC intents **must not** bypass tick participation rules defined in Stage 16.2.

## 6. Authority & Safety Invariants

The following invariants **must always hold**:

- All NPC action intents **must** be server-owned.
- Client-authored or client-modified intents **must never** exist.
- An intent **must never** be duplicated, replayed, or reordered.
- An intent **must never** persist across save or restore boundaries.
- Intent emission **must not** bypass validation, save, or restore rules.

## 7. Failure & Edge Case Handling

**No-Decision Outcomes**
- A no-decision outcome **must** result in no intent emission.
- A placeholder or implicit intent **must not** be generated.

**Emission Failure**
- If intent emission cannot complete deterministically, no intent **must** be emitted.
- Partial or malformed intents **must not** be emitted.

**Session Deactivation**
- If session deactivation occurs after decision selection but before emission:
  - The selected decision **must** be discarded.
  - No intent **must** be emitted.

**Server Crash**
- If a server crash occurs after emission but before consumption:
  - The emitted intent **must** be discarded on restore.
  - No intent **must** be replayed or inferred.

**Restore Behavior**
- On restore, no NPC action intent **must** exist.
- Decisions **must** be re-evaluated under normal tick rules.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Combat tactics, movement logic, or interactions
- AI behavior execution or sequencing
- Quest advancement or reward logic
- Intent resolution systems or queues
- Persistence formats or schemas
- Implementation details or engine internals
