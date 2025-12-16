# Stage 11.3 — Combat Tick-Phase Wiring Plan
**Scope:** Per-tick wiring order for combat runtime systems only  
**Authority:** Server-authoritative, deterministic (10 Hz), schema-first  
**Alignment:** Must match Stage 10.3 resolution phases + Stage 11.1 system boundaries

This document defines the authoritative **tick-phase execution plan** for combat:
- Ordered phases per server tick
- Which systems run in each phase (and in what order)
- Which phases are read-only vs mutating
- When validation snapshots are captured
- When outcomes become observable to clients
- Where checkpoint-boundary persistence integration may run (boundary only)

This document does NOT define:
- Implementation details
- Any new persistence semantics
- Networking protocols
- Client prediction or rollback
- UI/animation/physics behaviors
- Combat tuning, math, or timing values beyond phase order

---

## A) Tick Timeline (Ordered Phases Per Server Tick)

The following phases execute in this exact order once per authoritative server tick.

### Phase 0 — Tick Boundary Freeze (Queue Cutoff)
**Allowed**
- Freeze the intent queue for resolution eligibility (T+1 semantics preserved)
- Finalize deterministic ordering inputs (entity IDs, sequence numbers)

**Disallowed**
- Any combat state mutation
- Any resolution computation
- Any event emission to clients

**Systems Executed (in order)**
1) **CombatIntentQueueSystem** (read-only finalization / freeze)

---

### Phase 1 — Validation Snapshot: Pre-Resolution
**Allowed**
- Capture deterministic snapshots of inputs:
  - Frozen intent queue
  - Combat state read-only view

**Disallowed**
- Any mutation
- Any corrective behavior
- Any event emission

**Systems Executed (in order)**
1) **CombatValidationHookLayer** (read-only capture)

---

### Phase 2 — Intake Snapshot (Stage 10.3 Phase A)
**Allowed**
- Establish the read-only resolution inputs for this tick:
  - Ordered intents
  - Combat state snapshot
  - Required authoritative references (conceptual)

**Disallowed**
- Any mutation
- Any reordering beyond deterministic rules

**Systems Executed (in order)**
1) **CombatResolutionEngine** (read-only intake snapshot step)

---

### Phase 3 — Legality Gate (Stage 10.3 Phase B)
**Allowed**
- Evaluate each queued intent for legality to attempt (nullify or proceed)
- Produce per-intent gate dispositions and reason codes

**Disallowed**
- Combat state mutation
- Damage creation or mitigation
- Auto-correction (no retarget/convert/retry)

**Systems Executed (in order)**
1) **CombatResolutionEngine** (read-only gate evaluation)

---

### Phase 4 — Cancellation Window (Stage 10.3 Phase C)
**Allowed**
- Evaluate cancellation requests as a pre-commit filter
- Mark referenced intents as ineligible for this tick’s resolution flow (if applicable)
- Produce cancellation disposition and reason codes (structural)

**Disallowed**
- Any combat state mutation
- Any guarantee that cancellation succeeds
- Any reordering of intents

**Systems Executed (in order)**
1) **CombatResolutionEngine** (read-only cancellation evaluation)

---

### Phase 5 — Commitment Set Formation (Stage 10.3 Phase D)
**Allowed**
- Deterministically form the commitment set
- Exclude intents due to deterministic conflicts (nullify with reasons)

**Disallowed**
- Combat state mutation
- Damage application
- Any “merging” or “best effort” conversion

**Systems Executed (in order)**
1) **CombatResolutionEngine** (read-only commitment planning)

---

### Phase 6 — Proposed Effects Calculation (Stage 10.3 Phase E)
**Allowed**
- Produce proposed outcomes without mutating state:
  - Proposed state transitions (conceptual)
  - Proposed damage instances (raw / opaque payload)

**Disallowed**
- Mitigation application
- State mutation
- Outcome broadcasting

**Systems Executed (in order)**
1) **CombatResolutionEngine** (read-only proposed effect generation)

---

### Phase 7 — Mitigation Evaluation (Stage 10.3 Phase F)
**Allowed**
- Transform proposed damage via mitigation contracts
- Produce mitigation result records
- Produce finalized damage outcomes (post-mitigation payload)

**Disallowed**
- Combat state mutation
- Any formula disclosure or tuning logic in this layer
- Any reordering or conflict re-selection

**Systems Executed (in order)**
1) **DamageAndMitigationProcessor** (read-only transform over proposed damage)
2) **CombatResolutionEngine** (read-only incorporation of finalized outcomes into the pending application set)

---

### Phase 8 — Authoritative Application (Stage 10.3 Phase G) **MUTATING**
**Allowed**
- Apply authoritative mutations in strict order:
  1) Apply combat state transitions
  2) Apply finalized damage outcomes to combat survivability model
  3) Record applied/not-applied dispositions as part of the resolution report

**Disallowed**
- Any re-evaluation of legality/commitment
- Any replay or “second pass”
- Any mid-phase persistence commit
- Any client-observable emission before completion

**Systems Executed (in order)**
1) **CombatStateAuthoritySystem** (mutating: apply transitions and survivability changes, driven by resolution outputs)
2) **CombatResolutionEngine** (read-only: finalize resolution report from applied results)

---

### Phase 9 — Validation Snapshot: Post-Application
**Allowed**
- Capture deterministic snapshots of results:
  - Updated combat state
  - Resolution report (ordered)
  - Damage and mitigation outcomes (ordered)

**Disallowed**
- Any mutation
- Any corrective behavior
- Any event emission

**Systems Executed (in order)**
1) **CombatValidationHookLayer** (read-only capture)

---

### Phase 10 — Outcome Emission (Observable Publication)
**Allowed**
- Emit authoritative combat outcomes (events/notifications) for client observation:
  - Intent dispositions
  - State transition summaries
  - Damage and mitigation outcomes (as published contracts)

**Disallowed**
- Any mutation
- Any persistence commit
- Any interpretation or prediction

**Systems Executed (in order)**
1) **CombatOutcomeBroadcaster** (read-only publish)

---

### Phase 11 — Checkpoint Boundary Integration (Persistence Boundary Only)
**Allowed**
- If a save checkpoint is requested, allow persistence integration to run at the boundary
- Commit must occur only at a valid checkpoint boundary (never mid-tick)
- Restore remains hydration-only (no replay)

**Disallowed**
- Any combat resolution execution here
- Any partial save of mid-tick state
- Any event replay generation

**Systems Executed (in order)**
1) **CombatPersistenceAdapter** (boundary-only integration)

---

## B) System Invocation Map (Per Locked Runtime System)

### CombatIntentQueueSystem
- **Runs In Phase(s):** Phase 0
- **Role:** Read-only finalization / freeze
- **Inputs:** Submitted intents pending acceptance, tick boundary signal
- **Outputs:** Frozen, deterministically ordered queue for this tick’s resolution eligibility
- **Must Not:** Perform combat state checks beyond intake contract, resolve outcomes, mutate combat state

---

### CombatStateAuthoritySystem
- **Runs In Phase(s):** Phase 8 (mutating), read-only participation implied wherever state snapshots are consumed
- **Role per Phase:**
  - Phase 8: **Mutating** (apply transitions + survivability model changes)
  - Other phases: **Read-only** (expose state snapshot views)
- **Inputs:**
  - Phase 8: Applied transition set + finalized damage outcomes (from resolution pipeline)
- **Outputs:**
  - Updated authoritative combat state snapshot
- **Must Not:** Order intents, compute damage/mitigation, broadcast outcomes, perform persistence I/O

---

### CombatResolutionEngine
- **Runs In Phase(s):** Phases 2–6 (read-only computation), Phase 4 (read-only cancellation evaluation), Phase 5 (read-only commitment), Phase 8 (read-only report finalization), Phase 7 (read-only incorporation)
- **Role:** Read-only resolution planning + report construction
- **Inputs:** Frozen intent queue, combat state snapshot, ordering rules, mitigation outputs
- **Outputs:** Gate dispositions, commitment set, proposed effects, pending application set, final resolution report
- **Must Not:** Mutate combat state directly, persist, broadcast, perform mitigation transforms

---

### DamageAndMitigationProcessor
- **Runs In Phase(s):** Phase 7
- **Role:** Read-only transform (proposed damage → finalized outcomes + mitigation records)
- **Inputs:** Proposed damage instances, read-only combat state context as required by contract
- **Outputs:** Finalized damage outcomes, mitigation results
- **Must Not:** Mutate combat state, reorder intents, alter commitment selection, broadcast

---

### CombatOutcomeBroadcaster
- **Runs In Phase(s):** Phase 10
- **Role:** Read-only publish of authoritative outcomes
- **Inputs:** Final resolution report, post-application combat state snapshot, ordered outcome records
- **Outputs:** Observable combat events/notifications (timing contract only)
- **Must Not:** Mutate combat state, infer outcomes, apply any logic, persist

---

### CombatPersistenceAdapter
- **Runs In Phase(s):** Phase 11 only (checkpoint boundary)
- **Role:** Boundary-only integration with persistence coordinator
- **Inputs:** Current authoritative combat state snapshot (as owned by CombatStateAuthoritySystem), save/load signals
- **Outputs:** Persisted combat-relevant state at checkpoint boundaries; hydration on restore
- **Must Not:** Commit mid-tick, replay combat logic on restore, emit outcomes, resolve combat

---

### CombatValidationHookLayer
- **Runs In Phase(s):** Phases 1 and 9
- **Role:** Read-only deterministic snapshot capture
- **Inputs:**
  - Phase 1: Frozen queue + pre-resolution combat state snapshot
  - Phase 9: Post-application combat state + resolution report + outcome records
- **Outputs:** Validation snapshots for harness/assertions
- **Must Not:** Mutate anything, retry, auto-correct, influence resolution, emit outcomes

---

## C) Mutation Guardrails

### Phases That MAY Mutate Authoritative Combat State
- **Phase 8 only** may mutate:
  - **CombatEntityState** (as defined by Stage 10.2)
  - Any combat-owned survivability model fields (health/condition) referenced by the locked state model

### Phases That Are STRICTLY Read-Only
- Phases **0–7**, **9–11** are strictly read-only with respect to:
  - CombatEntityState
  - Combat outcome records already produced for the tick
  - Any combat context/world state (if referenced as read-only inputs)

### Combat Context / World State Notes
- If any combat context or world references are consulted during legality or mitigation, they are **read-only** within this wiring plan.
- This plan does not introduce combat-owned world state.

---

## D) Checkpoint Boundary Notes (Persistence)

- A save may be **requested** at any time, but it may only be **committed** at a valid checkpoint boundary.
- In this wiring plan, the checkpoint boundary integration point is **Phase 11**.
- No partial saves:
  - No mid-tick commits
  - No persistence of “in-progress” resolution artifacts
- Restore is hydration only:
  - No event replay
  - No damage reapplication
  - No re-running missed ticks

This stage does not modify persistence semantics; it only identifies the boundary slot combat uses.

---

## E) Observability Timing (Combat Events)

- Combat outcomes become observable to clients **only after authoritative application completes**.
- In this wiring plan:
  - Client observability begins at **Phase 10**.
  - No combat outcomes are emitted earlier than Phase 10.
- Validation snapshots are captured:
  - **Phase 1** (pre-resolution inputs)
  - **Phase 9** (post-application results)
- Outcome emission does not mutate state and does not influence resolution.

This is a timing contract only. No networking implementation details are defined here.

---

## Explicit Non-Goals (Reaffirmed)

This stage does NOT:
- Define combat math, tuning, or formulas
- Define durations/cooldowns/timing beyond phase order
- Define client prediction or rollback
- Define persistence redesign or replay behavior
- Define networking protocols or message formats
- Introduce new systems, intents, or combat states

---

## Exit Condition

Stage 11.3 is complete when:
- The per-tick phase list is total-ordered and unambiguous
- Each system’s invocation phases and ordering are explicit
- Mutation is permitted only in the application phase
- Validation capture points and observability timing are locked
- Checkpoint-boundary persistence integration is clearly bounded
