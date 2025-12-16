# Stage 11.4 — Combat Validation Scenario Matrix
**Scope:** Scenario definitions only (no code)  
**Philosophy:** Stage 9 validation rules apply — deterministic, scenario-driven, fail-loud, no retries, no auto-repair, no silent correction  
**Alignment:** Must validate Stage 10.0–10.4 + Stage 11.1–11.3 (systems + tick-phase wiring)

This document defines the **combat validation scenarios** required to prove combat implementation obeys:
- Server authority
- Deterministic ordering
- State gating semantics
- Cancellation semantics
- Damage/mitigation contracts
- Tick-phase integrity
- Save/load determinism during combat
- Observability timing and authority boundaries

---

## Snapshot Capture Point Definitions (Referenced by All Scenarios)
Use these canonical capture points (from Stage 11.3 wiring plan):

- **S0 — Phase 0 (Queue Freeze):** Frozen intent queue for the resolution tick
- **S1 — Phase 1 (Pre-Resolution Snapshot):** Frozen queue + authoritative combat state (read-only)
- **S2 — Phase 9 (Post-Application Snapshot):** Updated authoritative combat state + resolution report + ordered outcome records
- **S3 — Phase 10 (Post-Emission Boundary):** Observable publication boundary (what clients may observe)
- **S4 — Phase 11 (Checkpoint Boundary):** Save integration boundary (if requested)

Scenarios below reference S0–S4 explicitly.

---

# A) Intent Intake & Deterministic Ordering

## A1 — Same-Tick Multi-Intent Deterministic Queue Order
**Scenario ID:** A1  
**Initial Setup Conditions:**
- Two entities exist: `E1`, `E2` (both valid combatants)
- Both are in a combat-eligible state (no state restrictions assumed beyond “alive and authoritative”)
- No prior intents queued for these entities

**Ordered Combat Intents (by tick):**
- **Tick T (submitted during T, queued for T+1):**
  - `E1`: CombatAttackIntent (Target = E2)
  - `E1`: CombatDefendIntent
  - `E2`: CombatMovementIntent
  - Submission order is intentionally permuted across identical runs (arrival-time shuffled)

**Snapshot Capture Points:**
- S0 (Queue Freeze for T+1)
- S1 (Pre-Resolution for T+1)

**Expected Invariants:**
- The frozen queue at S0 is **bitwise identical** across runs with the same inputs, regardless of arrival order.
- The queue ordering respects deterministic rules (tick → entity ID → per-entity intent sequence).
- No client arrival timestamp influences ordering.

**Explicit Failure Conditions:**
- Queue order differs across identical runs.
- Any ordering depends on arrival time rather than deterministic keys.
- Any intent is dropped or reordered without a deterministic rule.

---

## A2 — Cross-Entity Ordering Independence from Client Identity
**Scenario ID:** A2  
**Initial Setup Conditions:**
- Two clients control separate entities `E1` and `E2`.
- Identity-related metadata differs between clients (e.g., session IDs), but entity IDs are stable.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAbilityIntent (AbilityKey = A)
  - `E2`: CombatAbilityIntent (AbilityKey = A)
  - Client submission identity is swapped across runs (E1’s intent sent from client B in one run; from client A in another), with the same entity IDs.

**Snapshot Capture Points:**
- S0
- S1

**Expected Invariants:**
- Queue ordering and contents are identical across runs.
- Ordering keys are entity-based and deterministic; client identity does not affect order.

**Explicit Failure Conditions:**
- Ordering differs when client identity swaps.
- Any client metadata influences ordering outcome.

---

# B) State Gating & Rejection

## B1 — Illegal-for-State Intent Nullified Without State Mutation
**Scenario ID:** B1  
**Initial Setup Conditions:**
- `E1` is in a combat state where **CombatAttackIntent is not legal** (use a locked state from Stage 10.2 that disallows attacking).
- `E2` exists and is attackable in general terms.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)

**Snapshot Capture Points:**
- S1 (Pre-Resolution)
- S2 (Post-Application)
- S3 (Post-Emission boundary)

**Expected Invariants:**
- The intent is **not resolved into an outcome**; it is **nullified** during gating/commitment (per Stage 10.3 semantics).
- No authoritative combat state fields change due to the illegal intent.
- The nullification is **observable** in the resolution report emitted at/after S3 with a reason code.

**Explicit Failure Conditions:**
- Any combat state mutation occurs despite nullification.
- Nullification is silent (no observable disposition).
- The server auto-corrects (retargets, converts intent, retries).

---

## B2 — Referential Invalid Intent Rejected/Nullified and Observable
**Scenario ID:** B2  
**Initial Setup Conditions:**
- `E1` exists and is alive.
- Target entity referenced does not exist: `E999`.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E999)

**Snapshot Capture Points:**
- S0/S1 (to confirm acceptance/queue presence policy)
- S2
- S3

**Expected Invariants:**
- Intent does not produce any damage outcomes or state transitions.
- A deterministic failure disposition is observable (either rejected before queue or nullified in legality gate, consistent with intent intake contract).
- No authoritative state mutation occurs.

**Explicit Failure Conditions:**
- Any state mutation or damage outcome produced.
- Failure is silent.
- Server substitutes a “closest valid target” or otherwise auto-corrects.

---

# C) Multi-Entity Conflict Resolution

## C1 — Conflicting Intents Across Entities Resolve Deterministically (Atomic Outcomes)
**Scenario ID:** C1  
**Initial Setup Conditions:**
- `E1` and `E2` are both alive and in combat-eligible states.
- Both are within a context where mutual interaction is possible (no range/LOS assumptions required in validation).

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)
  - `E2`: CombatAttackIntent (Target = E1)

**Snapshot Capture Points:**
- S1
- S2

**Expected Invariants:**
- The resolution report ordering is deterministic and repeatable across runs.
- Outcomes are atomic per tick: either both intents are resolved (as allowed by rules) or deterministic nullifications occur — never partial/mixed results that differ across runs.
- Damage outcome records (if any) reference OriginIntentRef correctly and are ordered deterministically.

**Explicit Failure Conditions:**
- Resolution order differs across identical runs.
- Mixed outcomes appear across runs (one run resolves E1 but nullifies E2, another run does the opposite) without deterministic cause.
- Any partial application occurs (e.g., state transition applied without corresponding recorded outcome/disposition).

---

## C2 — Deterministic Conflict Exclusion Within the Same Tick
**Scenario ID:** C2  
**Initial Setup Conditions:**
- `E1` is alive and eligible to submit multiple intents.
- Combat state is such that at least one exclusivity rule exists (from Stage 10.2 / 10.3 pipeline) that would prevent committing multiple incompatible actions in the same tick.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)
  - `E1`: CombatMovementIntent
  - `E1`: CombatInteractIntent (Target = X)
  - The order of submission is permuted across runs, but per-entity intent sequence numbers remain deterministic per submission.

**Snapshot Capture Points:**
- S0
- S2

**Expected Invariants:**
- Commitment selection is deterministic and repeatable across runs.
- Any excluded intents are nullified with reason codes and remain observable.
- No “merge” or “best effort” conversion occurs.

**Explicit Failure Conditions:**
- Different committed set across identical runs.
- Silent dropping of excluded intents.
- Auto-correction (converting one intent to another).

---

# D) Cancellation Semantics

## D1 — Cancellation Does Not Guarantee Success
**Scenario ID:** D1  
**Initial Setup Conditions:**
- `E1` is alive and in a state where some actions are not cancelable by rules (per Stage 10.2/10.3; the scenario asserts that such a case exists).
- A target action is queued and eligible for resolution.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAbilityIntent (AbilityKey = A)  ← referenced action
  - `E1`: CombatCancelIntent (TargetIntentSequenceNumber = sequence of the ability)

**Snapshot Capture Points:**
- S1
- S2
- S3

**Expected Invariants:**
- Cancellation is evaluated in the cancellation window phase and produces an observable disposition.
- The cancel request may fail safely; failure does not roll back or mutate unrelated state.
- Whether cancellation succeeds is not assumed; the scenario validates that “cancel always succeeds” is forbidden.

**Explicit Failure Conditions:**
- Cancellation always succeeds regardless of state rules.
- Any rollback of already-applied state occurs.
- Cancellation reorders the queue or changes deterministic ordering keys.

---

## D2 — Cancel References Nonexistent / Already-Resolved Intent Fails Safely
**Scenario ID:** D2  
**Initial Setup Conditions:**
- `E1` is alive.
- The referenced intent sequence number does not exist for `E1`, or references an intent already resolved in a prior tick.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatCancelIntent (TargetIntentSequenceNumber = nonexistent or already-resolved)

**Snapshot Capture Points:**
- S1
- S2
- S3

**Expected Invariants:**
- Cancel intent results in a deterministic failure disposition (rejected or nullified per contract).
- No authoritative state mutation occurs as a result of invalid cancellation.
- No auto-correction occurs (server does not “guess” which intent to cancel).

**Explicit Failure Conditions:**
- Any state mutation occurs.
- Cancellation silently disappears.
- Server cancels a different intent than referenced.

---

# E) Damage & Mitigation Outcomes

## E1 — Damage Outcomes Produced Only During Resolution and Applied Only in Application Phase
**Scenario ID:** E1  
**Initial Setup Conditions:**
- `E1` and `E2` exist, alive, combat-eligible.
- `E1` can submit an attack intent.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)

**Snapshot Capture Points:**
- S1 (Pre-Resolution)
- S2 (Post-Application)
- S3 (Post-Emission)

**Expected Invariants:**
- At S1, there are no new damage outcomes recorded for the tick (pre-resolution snapshot is read-only).
- Any damage outcome records appear only as part of the resolution report produced by/after application (S2/S3), never earlier.
- ApplicationDisposition is explicit (applied or not-applied with reason code).
- OriginIntentRef matches the submitted intent identity.

**Explicit Failure Conditions:**
- Damage is applied or observable before application completes.
- Damage appears in a pre-resolution snapshot.
- Damage is applied without a corresponding recorded outcome/disposition.

---

## E2 — Mitigation Modifies Outcomes, Not Inputs (No Input Mutation)
**Scenario ID:** E2  
**Initial Setup Conditions:**
- `E1` attacks `E2`.
- `E2` also submits a defense intent in the same tick (to ensure mitigation is in scope conceptually).

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)
  - `E2`: CombatDefendIntent

**Snapshot Capture Points:**
- S1
- S2

**Expected Invariants:**
- Proposed attack intent data remains unchanged throughout the tick (intents are immutable inputs once queued).
- Mitigation results exist only as outcome records tied to damage instances.
- Any mitigation effect is reflected in finalized damage outcomes, not by mutating intent inputs.

**Explicit Failure Conditions:**
- Any intent input is mutated during mitigation evaluation.
- Mitigation is recorded as changing queued intents rather than producing separate mitigation result records.
- Mitigation changes ordering or commitment selection retroactively.

---

# F) Tick-Phase Integrity

## F1 — Mutation Occurs Only in the Authorized Application Phase
**Scenario ID:** F1  
**Initial Setup Conditions:**
- Active combat with at least one intent that would produce state changes if resolved (e.g., attack or ability).
- Validation harness can observe state snapshots at defined capture points.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAbilityIntent (AbilityKey = A, target optional)

**Snapshot Capture Points:**
- S1 (Pre-Resolution)
- S2 (Post-Application)

**Expected Invariants:**
- Between S1 and S2, authoritative combat state changes only as a result of the authorized application phase.
- No state changes are visible during read-only phases (conceptually enforced by: pre-resolution snapshot contains the “before” state; post-application snapshot contains the “after” state; intermediate read-only phases must not mutate).

**Explicit Failure Conditions:**
- Any mutation is observable prior to post-application snapshot.
- Read-only phases produce state deltas.
- A system other than the state authority/application pathway mutates combat state.

---

# G) Save / Load Determinism During Combat

## G1 — Save Requested During Active Combat; Restore Produces Identical Outcomes (No Replay)
**Scenario ID:** G1  
**Initial Setup Conditions:**
- Active combat between `E1` and `E2`.
- A save is requested while combat is active (request timing may be during a tick, but commit must occur only at checkpoint boundary per locked rules).

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)
- **Save Request:** Issued during tick T (request only; commit at checkpoint boundary)
- **Disconnect/Restore:** Occurs after checkpoint commit boundary
- **Tick T+K after restore:**
  - Repeat the same controlled intent submission sequence as baseline run (deterministic)

**Snapshot Capture Points:**
- S2 baseline (post-application state + report before save)
- S4 (checkpoint boundary commit point)
- Post-restore S1 and S2 for the comparable tick after reconnect

**Expected Invariants:**
- After restore, authoritative combat state matches the saved snapshot (hydration only).
- Identical post-restore inputs produce identical post-restore outcomes relative to baseline.
- No combat logic is replayed on restore (no duplicated outcomes, no repeated damage application).

**Explicit Failure Conditions:**
- Outcomes diverge after restore under identical input sequence.
- Any evidence of replay (duplicated damage/outcomes for already-processed intents).
- Partial state commit (save captures mid-tick transient artifacts).

---

# H) Observability & Authority

## H1 — Outcomes Observable Only After Authoritative Application and Emission Boundary
**Scenario ID:** H1  
**Initial Setup Conditions:**
- A client observer is present for `E1` and `E2`.
- Combat occurs normally under server authority.

**Ordered Combat Intents (by tick):**
- **Tick T:**
  - `E1`: CombatAttackIntent (Target = E2)

**Snapshot Capture Points:**
- S1 (Pre-Resolution)
- S2 (Post-Application)
- S3 (Post-Emission boundary)

**Expected Invariants:**
- Prior to S3, clients have no authoritative visibility into:
  - Damage outcomes
  - Mitigation results
  - Final intent dispositions
  - Post-application state transitions
- At/after S3, clients may observe only server-published outcomes (no intermediate or speculative states).

**Explicit Failure Conditions:**
- Any client-observable data implies final outcomes before the emission boundary.
- Intermediate resolution artifacts are exposed.
- Client can infer damage or mitigation as authoritative prior to S3.

---

## Matrix Completeness Checklist (Must Hold)
The scenario set above collectively proves:

- **A:** Deterministic same-tick ordering is stable across identical runs.
- **B:** Illegal intents do not mutate state and produce observable dispositions.
- **C:** Multi-entity conflicts resolve deterministically with atomic outcomes.
- **D:** Cancellation is request-only; never guaranteed; fails safely without rollback.
- **E:** Damage/mitigation are resolution products; mitigation transforms outcomes, not inputs; application is atomic.
- **F:** Tick-phase integrity is enforced: mutation only in the authorized phase.
- **G:** Save/load during combat is deterministic; restore is hydration-only; no replay.
- **H:** Observability timing is enforced; no speculative/intermediate outcomes are exposed.

---

## Explicit Non-Goals (Reaffirmed)
This document does NOT:
- Implement validation code
- Define combat math, tuning, or RNG
- Add new systems, schemas, intents, or combat states
- Introduce prediction, rollback, reconciliation, or UI/animation/physics/AI behavior
- Redefine persistence semantics
