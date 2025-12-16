# Stage 15.4 — Quest Save, Restore & Validation

## 1. Purpose

This document defines the authoritative rules governing **quest persistence**, **quest restore semantics**, and **quest validation**.
It proves that the quest runtime system defined in Stages 15.1–15.3 is deterministic, restore-safe, and authority-clean under Stage 9 validation philosophy.
This document introduces no new quest behavior and does not modify quest progression rules.

## 2. Quest Persistence Boundaries

**Persistence Scope**

- Quest state **must** be persisted as player-owned state.
- Quest persistence **must** follow all Stage 13.5 Save & Restore Boundaries.
- Quest persistence **must** be treated as authoritative truth.

**Legal Persistence Boundaries**

Quest state **must not** be persisted unless all of the following are true:
- The server is at an explicit, safe save boundary.
- No quest state transition is mid-application.
- No quest progression evaluation is partially applied.
- Player-owned state is internally consistent.

**Forbidden Persistence Conditions**

Quest state **must not** be persisted:
- Mid-tick.
- During quest state transition execution.
- During progression evaluation.
- While quest state is in an illegal or intermediate condition.

**Atomicity Rules**

- Quest persistence **must** be atomic.
- Partial quest saves **are forbidden**.
- When required, quest persistence **must** be atomic with other player-owned persisted state.
- Mixed-version or partially applied quest state **must never** be observable.

## 3. Quest Restore Semantics

**Restore Rules**

- Quest restore **must** use persisted truth only.
- Quest restore **must not** replay quest logic, triggers, or progression evaluation.
- Quest restore **must not** infer or reconstruct runtime-only state.
- Quest restore **must** produce a quest state that is legal under Stage 15.2.

**State Validity**

- Every restored quest instance **must** be in exactly one defined quest state.
- Restored quest state **must not** violate legal state transition rules.
- Terminal quest states **must** remain terminal on restore.

**Runtime Reset**

- All quest runtime-only state **must** be discarded on restore.
- No quest progression **must** resume automatically after restore.

## 4. Disconnect Handling

The following rules apply to player disconnects:

**Disconnect During Quest Progression Evaluation**
- Any in-progress evaluation **must** be discarded.
- Quest state **must** remain at the last persisted value.
- No partial progression **must** apply.

**Disconnect During Quest State Transition**
- The transition **must** be treated as non-existent unless fully persisted.
- Quest state **must** reflect only the last valid persisted state.

**Post-Disconnect Restore**
- Quest state **must** be restored from persisted truth only.
- No quest evaluation **must** occur until normal lifecycle conditions are re-established.

## 5. Crash Handling

The following rules apply to server crashes:

**Crash During Quest Evaluation**
- All runtime evaluation state **must** be discarded.
- Quest state **must** remain unchanged unless fully persisted at a valid boundary.

**Crash During Quest State Transition**
- The transition **must** be treated as non-existent unless persistence completed atomically.
- Restore **must** reflect only the last valid persisted quest state.

**Crash During Save Operation**
- Quest persistence **must** be atomic.
- Restore **must** reflect either:
  - the complete previous quest state, or
  - the complete new quest state.
- Partially written quest state **must never** be treated as valid.

## 6. Validation Scenarios

The following validation scenarios are mandatory and must fail loudly if violated:

**Scenario: Disconnect During Quest Progression**
- **Exercises:** Stage 15.2 Progress Evaluation Rules, Stage 13.5 Save Boundaries
- **Expected Outcome:** Quest state remains unchanged.
- **Must Never Observe:** Partial quest progression.

**Scenario: Crash During Quest State Transition**
- **Exercises:** Stage 15.2 Transition Validity, Stage 13.5 Atomicity
- **Expected Outcome:** Quest state reflects last valid persisted state.
- **Must Never Observe:** Half-applied state transition.

**Scenario: Restore From Persisted Quest State**
- **Exercises:** Stage 15.2 State Legality, Stage 15.4 Restore Semantics
- **Expected Outcome:** Quest state is legal and deterministic.
- **Must Never Observe:** Inferred or replayed quest logic.

**Scenario: Illegal State Prevention**
- **Exercises:** Stage 15.2 Forbidden Transitions
- **Expected Outcome:** Illegal quest states are rejected.
- **Must Never Observe:** Undefined or multiple quest states.

## 7. Quest Invariants

The following invariants are mandatory and enforceable by validation:

1. **Authoritative Persistence**
   - Persisted quest state **must** be the sole source of truth.

2. **Persistence Boundary Enforcement**
   - Quest state persistence **must never** occur outside explicitly defined legal persistence boundaries.
   - Any persistence attempt outside those boundaries **must** be rejected deterministically.

3. **Atomicity**
   - Quest persistence **must** be atomic.
   - Partial quest state **must never** be observable.

4. **No Replay**
   - Quest restore **must not** replay logic or events.

5. **State Legality**
   - Quest state **must** always be one of the defined legal states.

6. **Determinism**
   - Given identical persisted inputs, quest restore and validation outcomes **must** be identical.

7. **Server Authority**
   - Quest state persistence and restore **must** be server-controlled.
   - Clients **must never** influence persisted quest state.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Quest rewards, outcomes, or completion effects
- Quest content, narrative, or dialogue
- UI, journals, or client-side quest representation
- Replay, rollback, reconciliation, or compensation systems
- Client authority or client-driven persistence
- Implementation details, schemas, or storage formats
