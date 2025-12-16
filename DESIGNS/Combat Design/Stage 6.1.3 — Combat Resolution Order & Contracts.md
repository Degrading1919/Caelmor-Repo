# Stage 10.3 — Combat Resolution Order and Contracts
**Scope:** Authoritative resolution pipeline + damage/mitigation contracts only  
**Authority:** Server-authoritative, deterministic (10 Hz)  
**Dependencies:** Stage 10.1 (Intents), Stage 10.2 (State Model)

This document defines the **combat truth spine**:
- The ordered phases executed per server tick
- Deterministic ordering and conflict handling rules
- The structural contracts for damage and mitigation
- Failure semantics (reject vs nullify) and observability boundaries

This document does NOT define:
- Numbers, tuning, formulas, probabilities, or RNG
- Timing/duration, cooldowns, stamina, or resource costs
- AI behavior, animation, physics, or client prediction
- Persistence changes or save/restore semantics

---

## 1) Combat Resolution Phases (Conceptual, Per Server Tick)

All phases execute on the server once per authoritative tick.
All queued intents accepted during tick **T** are eligible for resolution in tick **T+1**.

### Phase A — Intake Snapshot (Read-Only)
**Responsibility**
- Establish the read-only inputs for the tick:
  - The ordered intent queue for tick T+1
  - The authoritative combat state snapshot for all involved entities
  - Any authoritative world references needed for legality checks

**Non-Goals**
- No mutation
- No reordering beyond deterministic rules already defined

---

### Phase B — Legality Gate (Intent-Level)
**Responsibility**
- Determine whether each queued intent is **legal to attempt** given:
  - Entity existence and authority
  - Current combat state legality rules
  - Basic referential validity (target exists, keys exist)

**Outputs**
- A per-intent gate result: **Proceed** or **Nullify**
- A reason code for any nullification

**Non-Goals**
- No outcome resolution
- No “best effort” correction (no auto-retarget, no auto-convert)

---

### Phase C — Cancellation Window (Pre-Commit)
**Responsibility**
- Process `CombatCancelIntent` requests as a **pre-commit filter** over other intents
- Cancellation is evaluated strictly as:
  - A request to withdraw a referenced, unresolved intent
  - Not a guarantee of cancelability

**Outputs**
- The referenced intent is either:
  - Marked “Canceled” for this tick’s resolution flow, or
  - Left untouched

**Non-Goals**
- No state-machine logic beyond acknowledging that cancel success is decided later
- No mutation of combat state here (only marking resolution eligibility)

---

### Phase D — Commitment Set Formation (Deterministic Plan)
**Responsibility**
- Form the deterministic **commitment set** for the tick:
  - Which non-canceled, legal intents will be passed forward as candidates for resolution
  - Which are excluded due to deterministic conflicts

**Key Rule**
- Commitment selection is deterministic and rule-driven; it never depends on wall-clock time or arrival order.

**Non-Goals**
- No outcome resolution
- No damage math

---

### Phase E — Effect Calculation (Read-Only Computation)
**Responsibility**
- Produce proposed outputs from committed intents without mutating authoritative state:
  - Proposed state transitions (conceptual)
  - Proposed damage instances (structure only)

**Non-Goals**
- No application
- No mitigation application
- No persistence writes

---

### Phase F — Mitigation Evaluation (Structural Transform)
**Responsibility**
- For each proposed damage instance, compute mitigation as a separate conceptual step:
  - Mitigation produces an adjusted damage outcome
  - Mitigation does not apply state changes directly

**Non-Goals**
- No formulas or numeric rules
- No “guaranteed defense” semantics

---

### Phase G — Application (Authoritative Mutation)
**Responsibility**
- Apply finalized outcomes in a strict order:
  1. Apply state transitions
  2. Apply damage to authoritative combatant health/condition model
  3. Apply any authoritative secondary results that are explicitly part of resolution outputs (not defined here)

**Non-Goals**
- No retroactive edits to earlier phases
- No hidden side effects

---

### Phase H — Resolution Report (Observable Record)
**Responsibility**
- Emit a deterministic, ordered report of what occurred:
  - Which intents succeeded, failed, or were nullified/canceled
  - Which damage instances were applied
  - Which state transitions were applied

**Non-Goals**
- No “retries”
- No auto-fix suggestions
- No client-authoritative interpretation

---

## 2) Deterministic Ordering Rules

### 2.1 Global Intent Order (Within a Tick)
All queued intents for the tick are processed in deterministic order:
1. Tick number (implicit: current resolution tick)
2. Submitting entity ID (stable)
3. Intent sequence number (per-entity, monotonic)

No client-provided ordering is trusted.

---

### 2.2 Per-Entity Ordering and Exclusivity
- Intents are evaluated per entity in queue order.
- If multiple intents from the same entity would require mutually exclusive commitment, a deterministic conflict rule selects which remain committed.
- Excluded intents are **nullified**, not “merged,” not “converted,” and not “corrected.”

This document defines the *existence* of deterministic conflict selection, but does not define the specific combat rules that determine exclusivity outcomes.

---

### 2.3 Cancellation Interaction with Ordering
- `CombatCancelIntent` is processed in **Phase C**, before other intents are committed.
- Cancellation requests do not reorder the queue; they only affect whether a referenced intent remains eligible.
- If multiple cancellation requests exist for the same entity in the same tick, they are evaluated in deterministic order (as above).
- Cancellation does not guarantee the referenced action is cancelable; cancelability is determined later by authoritative combat resolution/state rules.

---

### 2.4 State-Legality Interaction
- Intent legality is evaluated against the authoritative combat state snapshot during **Phase B**.
- Intents illegal in the current state are **nullified** with a reason code.
- No intent is auto-substituted for a legal one.

---

## 3) Damage Contracts

### 3.1 System Meaning of “Damage”
“Damage” is an authoritative outcome representing **a reduction or change** applied to a target’s combat survivability model (e.g., health/condition), produced by combat resolution.

Damage is:
- Produced by resolution (not by intent)
- Deterministic for a given tick input set
- Separable from mitigation and application

---

### 3.2 Damage Outcome Structure (Required Fields)
A damage outcome is represented as a **damage record** with the following required fields:

- DamageInstanceId
- ResolutionTick
- SourceEntityId
- TargetEntityId
- OriginIntentRef (entity ID + intent sequence number)
- DamageCategoryKey
- DamagePayload (opaque: the computed “raw” damage representation)
- FinalDamagePayload (opaque: post-mitigation representation)
- ApplicationDisposition (applied / not-applied, with reason code)

**Notes**
- Payload fields are intentionally opaque here to prevent formulas or tuning from entering this stage.
- “Applied / not-applied” is a structural reporting requirement, not a gameplay rule.

---

### 3.3 Separation: Calculation vs Application
- **Calculation** produces `DamagePayload` (raw proposed damage) during Phase E.
- **Mitigation** produces `FinalDamagePayload` during Phase F.
- **Application** mutates authoritative target state during Phase G.

At no point does an intent directly mutate health/condition; only Phase G may do so.

---

## 4) Mitigation Contracts

### 4.1 System Meaning of “Mitigation”
Mitigation is an authoritative transform applied to proposed damage prior to application.
It represents defenses, resistances, blocks, reductions, or nullification effects *without* specifying any math.

Mitigation is:
- Determined during resolution
- Deterministic
- Applied per damage instance (not per intent)

---

### 4.2 Mitigation Structure (Required Fields)
A mitigation result is represented as a record with the following required fields:

- MitigationInstanceId
- ResolutionTick
- TargetEntityId
- RelatedDamageInstanceId
- MitigationSourceKey (opaque identifier for the conceptual source of mitigation)
- MitigationPayload (opaque: representation of the mitigation transform)
- ResultDisposition (modified / unchanged / nullified, with reason code)

---

### 4.3 Where Mitigation Applies in the Flow
- Mitigation is evaluated after damage is proposed (Phase E) and before damage is applied (Phase G).
- Mitigation never applies “retroactively” after application.
- Mitigation does not reorder intents or alter commitment selection.

---

### 4.4 What Mitigation Does NOT Guarantee
Mitigation does NOT guarantee:
- That any damage is reduced
- That a defense intent succeeds
- That mitigation is present or applicable
- That mitigation fully prevents damage

Mitigation is a transform step, not a promise.

---

## 5) Failure Semantics

### 5.1 Reject vs Nullify
**Rejected**
- Occurs at intent intake (pre-queue) in Stage 10.1 semantics
- Intent is not queued
- Produces no combat-side effects

**Nullified**
- Occurs during Phase B (legality gate) or Phase D (conflict exclusion) or Phase C (canceled eligibility)
- Intent was accepted and queued, but produces no resolved outcome
- Must be observable in the resolution report with a reason code

---

### 5.2 Observable vs Silent Outcomes
**Must be observable**
- Nullified intents (with reason)
- Canceled intents (with disposition: succeeded/failed, and reason)
- Damage instances proposed and applied/not-applied (with reason)
- State transitions applied/not-applied (with reason)

**May be silent**
- Internal evaluation steps that do not change outcomes (no side effects, no recordable result)

---

### 5.3 What Must Never Be Auto-Corrected
The server must never:
- Retarget an intent to a “closest valid” target
- Convert an illegal intent into a different intent
- Reorder intents based on arrival time
- Retry an intent automatically
- “Fix up” invalid references by guessing
- Invent missing fields or defaults beyond the intent contract

Failure is explicit and deterministic.

---

## Explicit Non-Goals (Reaffirmed)
This stage does NOT:
- Define combat math or tuning
- Define how hit/miss works
- Define resource costs, cooldowns, or durations
- Define AI combat decision-making
- Define animation, physics, or client prediction
- Add or modify intents or combat states
- Add persistence semantics or save integration

---

## Exit Condition
Stage 10.3 is complete when:
- Combat resolution is defined as a deterministic per-tick pipeline
- Ordering, conflict handling boundaries, and cancellation interaction are explicit
- Damage and mitigation are contractually defined as structures separated from application
- Failure semantics are explicit, observable, and non-corrective
