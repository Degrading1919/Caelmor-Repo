# Stage 9 — Integration Testing & Validation Harness
## Milestone Snapshot

Project: Caelmor  
Engine: Unity  
Architecture: Server-authoritative, deterministic (10 Hz)  
Status: PLANNED — GOVERNANCE LOCK

---

## 1. Stage Purpose

Stage 9 exists to **prove the correctness and durability** of the frozen non-combat economy and persistence systems implemented in Stage 7–8.

This stage does not introduce gameplay.  
It introduces **confidence**.

Stage 9 answers the question:

> “Can the existing economy and persistence systems be trusted as a permanent foundation for future gameplay systems?”

Specifically, Stage 9 validates that:
- Deterministic systems remain deterministic under real usage patterns
- Save / load restores exact authoritative state
- Atomic boundaries hold across ticks, sessions, and reconnects
- Multi-actor interaction does not corrupt state

Stage 9 protects Stage 7–8 from silent regression as development continues.

---

## 2. Canon Lock Statement

The following documents and systems are **final, authoritative, and immutable**:

- Stage 8.0 — Systems Snapshot & Implementation Plan
- Stage 8.0 — Systems Snapshot & Implementation Complete
- Stage7_1_ResourceNodeRuntime.md
- Stage7_2_GatheringResolution.md
- Stage7_3_InventoryAndResourceGrant.md
- Stage7_4_CraftingExecutionSystem.md
- Stage7_5_Persistence&SaveIntegration.md
- Caelmor_Phase1_4_Technical_Foundation.md

Stage 9 **wraps around** these systems.

Stage 9 does **not**:
- Redesign systems
- Modify schemas
- Adjust balance
- Change runtime behavior

Any deviation from the above documents during Stage 9 is a failure of scope.

---

## 3. In-Scope (What Stage 9 Does)

Stage 9 introduces a server-side **integration validation harness** capable of:

- Executing deterministic validation scenarios
- Driving controlled, ordered gameplay inputs
- Invoking save checkpoints and restore flows
- Capturing authoritative state snapshots
- Asserting expected vs actual outcomes
- Producing clear pass/fail signals

Validation focus areas include:
- Inventory mutation and persistence integrity
- Resource node depletion, respawn, and restore
- Atomic crafting execution across save/load
- Multi-actor contention for shared resources
- Reconnect and session boundary correctness
- Tick-boundary edge conditions

---

## 4. Explicit Non-Goals (Hard Exclusions)

Stage 9 must NOT include:

- Gameplay features or mechanics
- Combat systems or combat architecture
- AI or NPC behavior
- World simulation or ecology
- UI, debug UI, or developer tooling UI
- Client-side prediction
- Performance optimization
- Balance or tuning changes
- Content expansion
- Schema changes
- New folder structures

If work resembles “improvement” rather than “verification,” it is out of scope.

---

## 5. Execution Mode (Locked)

Stage 9 validation executes via **automatic server-startup scenarios**.

- Validation scenarios run deterministically when explicitly enabled
- No manual triggering is required for correctness
- Results are emitted via logs and structured reports

This mode minimizes human error and ensures repeatability.

---

## 6. Exit Criteria (Definition of Done)

Stage 9 is considered complete when:

- All core non-combat economy flows have at least one validation scenario
- Save/load restores exact authoritative state
- Multi-actor contention scenarios behave correctly
- Reconnect scenarios restore state without replay
- Failures are loud, localized, and diagnosable
- The economy and persistence layer can be declared **trusted**

Only after these conditions are met may the project proceed to Stage 10.

---

## 7. Re-Entry Rule (Mandatory)

If validation fails:

1. Assume an implementation bug
2. Then assume misuse of scaffolding
3. Escalate to design review only if the snapshot cannot be satisfied

Silent redesign is not permitted.

---

## 8. Anchor Statement

> “Stage 9 exists to prove that the economy is not a question mark.
> From this point forward, future systems build on certainty.”