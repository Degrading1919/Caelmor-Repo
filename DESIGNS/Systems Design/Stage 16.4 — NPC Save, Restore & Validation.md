# Stage 16.4 — NPC Save, Restore & Validation

## 1. Purpose

This document defines the authoritative rules governing **NPC persistence**, **NPC restore semantics**, and **NPC validation**.
It proves that the NPC runtime system defined in Stages 16.1–16.3 is deterministic, restore-safe, and authority-clean under Stage 9 validation philosophy.
This document introduces no new NPC behavior and does not modify NPC runtime, tick, perception, or interaction rules.

## 2. NPC Persistence Boundaries

**Persistence Scope**

- NPC state **must** be world-owned.
- NPC persistence **must** follow all Stage 13.5 Save & Restore Boundaries.
- NPC persistence **must** be authoritative truth for persisted NPCs.

**Legal Persistence Boundaries**

NPC state **must not** be persisted unless all of the following are true:
- The server is at an explicit, safe save boundary.
- No NPC tick participation entry or exit is mid-application.
- No NPC interaction resolution is mid-application.
- NPC runtime state is internally consistent and legal.

**Forbidden Persistence Conditions**

NPC state **must not** be persisted:
- Mid-tick.
- During NPC tick entry or exit processing.
- During NPC interaction resolution.
- While NPC state is partial, transitional, or illegal.

**Atomicity Rules**

- NPC persistence **must** be atomic within its chosen persistence model.
- Partial NPC persistence **is forbidden**.
- Mixed persistence models **are forbidden**.
- Persisted NPC state **must never** be observable in a partially applied form.

**Regeneration Model Constraint**

- NPCs using deterministic regeneration **must not** persist runtime-only state.
- Persisted data **must** be limited strictly to world-owned truth required for regeneration.

## 3. NPC Restore Semantics

**Restore Rules**

- NPC restore **must** use persisted truth only.
- NPC restore **must not** replay NPC logic, tick execution, perception, or interactions.
- NPC restore **must not** infer or reconstruct runtime-only state.

**Reconstruction Guarantees**

- Restored NPC state **must** be reconstructed using exactly one allowed persistence model.
- Restored NPC state **must** be fully legal under Stages 16.1–16.3.
- NPCs **must not** resume tick participation automatically on restore.

**Runtime Reset**

- All NPC runtime-only state **must** be discarded on restore.
- NPC tick participation and perception **must** re-enter only through normal lifecycle rules.

## 4. Disconnect Handling

The following rules apply to player or session disconnects:

**Disconnect During NPC Interaction**
- Any in-progress NPC interaction resolution **must** be discarded.
- No NPC interaction outcome **must** persist.

**Disconnect During NPC Tick Participation**
- NPC tick participation **must** continue or cease solely according to world and zone rules.
- Disconnect **must not** cause partial NPC state mutation.

**Post-Disconnect State**
- NPC persisted state **must** remain unchanged unless saved at a legal boundary.
- No NPC runtime-only state **must** survive disconnect.

## 5. Crash Handling

The following rules apply to server crashes:

**Crash During NPC Tick Participation**
- All NPC runtime-only tick and perception state **must** be discarded.
- Persisted NPC state **must** remain unchanged unless fully persisted at a legal boundary.

**Crash During NPC Interaction Resolution**
- The interaction **must** be treated as non-existent.
- No interaction outcome **must** be inferred or re-applied on restore.

**Crash During NPC Persistence**
- NPC persistence **must** be atomic.
- Restore **must** reflect either:
  - the complete previous NPC state, or
  - the complete new NPC state.
- Partial NPC state **must never** be treated as valid.

## 6. Validation Scenarios

The following validation scenarios are mandatory and must fail loudly if violated:

**Scenario: Disconnect During NPC Interaction**
- **Exercises:** Stage 16.3 Interaction Contracts, Stage 13.5 Save Boundaries
- **Expected Outcome:** No interaction outcome persists.
- **Must Never Observe:** Partial or inferred interaction state.

**Scenario: Crash During NPC Tick Participation**
- **Exercises:** Stage 16.2 Tick Participation Rules, Stage 13.5 Restore Semantics
- **Expected Outcome:** NPC runtime-only state is discarded.
- **Must Never Observe:** Automatic resumption of tick participation.

**Scenario: Crash During NPC Persistence**
- **Exercises:** Stage 13.5 Atomicity, Stage 16.4 Persistence Boundaries
- **Expected Outcome:** NPC state is fully old or fully new.
- **Must Never Observe:** Partially persisted NPC state.

**Scenario: Restore Into World With NPCs Present**
- **Exercises:** Stage 16.1 Runtime Model, Stage 16.4 Restore Semantics
- **Expected Outcome:** NPC state is legal and deterministic.
- **Must Never Observe:** Illegal NPC state or replayed execution.

## 7. NPC Invariants

The following invariants are mandatory and enforceable by validation:

1. **Authoritative Persistence**
   - Persisted NPC state **must** be the sole source of truth for persisted NPCs.

2. **Persistence Boundary Enforcement**
   - NPC persistence **must never** occur outside explicitly defined legal persistence boundaries.
   - Any persistence attempt outside those boundaries **must** be rejected deterministically.

3. **Atomicity**
   - NPC persistence **must** be atomic.
   - Partial NPC state **must never** be observable.

4. **No Replay**
   - NPC restore **must not** replay logic, perception, interactions, or tick execution.

5. **State Legality**
   - NPC state **must** always be legal under Stages 16.1–16.3.

6. **Determinism**
   - Given identical persisted world state, NPC restore outcomes **must** be identical.

7. **Server Authority**
   - NPC persistence and restore **must** be server-controlled.
   - Clients **must never** influence persisted NPC state.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- NPC AI behavior, decision-making, or reactions
- Dialogue, narrative roles, or personality
- Combat, threat, or targeting logic
- UI, presentation, or visualization
- Client authority or client-side persistence
- Replay, rollback, reconciliation, or compensation systems
- Implementation details, schemas, or storage formats
