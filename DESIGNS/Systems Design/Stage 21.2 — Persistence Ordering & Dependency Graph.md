# Stage 21.2 — Persistence Ordering & Dependency Graph

## 1. Purpose

This document defines the **ordering and dependency rules** governing cross-system persistence in Caelmor.
It establishes a closed, deterministic dependency graph for save and restore, the exact ordering required for each phase, and the rejection conditions that prevent partial, circular, or inference-based restores.
This document introduces no storage formats, tooling, or implementation details.

## 2. Scope

This document applies exclusively to **server-authoritative persistence ordering semantics**.
It defines save and restore ordering, dependency directionality, cycle prevention, and legality conditions.
It does not define save triggers, cadence, serialization, performance optimizations, or visualization.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 21.0 — Cross-System Persistence Architecture
- Stage 21.1 — Cross-System Persistence Architecture
- Stage 13.5 — Save & Restore Boundaries
- Stage 19 — World Simulation & Zone Runtime Architecture (all sub-stages)
- Stage 20 — Networking & Replication Architecture (all sub-stages)
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Persistence Dependency Overview

**Participating Systems (Closed Set)**

The following systems participate in cross-system persistence and define the complete dependency graph:

1. Player Identity and PlayerSave
2. World runtime (including zone structural composition)
3. NPC runtime (persisted state only)
4. Item runtime (ownership and location state)
5. Quest runtime (player-owned quest state)

No other systems are permitted to participate.

**Dependency Principle**
- Dependencies **must** be explicit, acyclic, and server-defined.
- Dependencies **must** reflect ownership and binding relationships only.
- No dependency **must** require runtime execution to resolve.

## 5. Save Ordering Rules

**Save Ordering**

Save **must** occur in the following deterministic order:

1. Player Identity and PlayerSave
2. World structural state and zone composition
3. NPC runtime persisted state
4. Item runtime persisted state
5. Quest runtime persisted state

No other ordering is permitted.

**Rules**
- Each system **must** produce persisted state only after all of its dependencies have produced persisted state.
- Save **must** be atomic across all participating systems.
- Save **must** fail if any participating system fails to produce authoritative persisted state.
- No system **must** observe or rely on partially completed save output from another system.

## 6. Restore Ordering Rules

**Restore Ordering**

Restore **must** occur in the following deterministic order:

1. Player Identity and PlayerSave
2. World structural state and zone composition
3. NPC runtime persisted state
4. Item runtime persisted state
5. Quest runtime persisted state

No other ordering is permitted.

**Rules**
- Each system **must** restore only after all of its dependencies have been restored successfully.
- Restore **must** use persisted authoritative truth only.
- Restore **must not** execute, resume, or infer runtime logic.
- Restore **must** fail deterministically if any required dependency is missing, inconsistent, or illegal.

**Activation**
- Restored systems **must** remain inactive until explicitly activated by the server.
- No tick participation **must** occur during restore.

## 7. Dependency Constraints & Cycles

**Legal Dependencies**
- NPC, item, and quest persisted state **must** depend on world structural state.
- Item and quest persisted state **must** depend on Player Identity where ownership applies.
- Quest persisted state **must** depend on PlayerSave and world context.

**Forbidden Dependencies**
- World structural state **must not** depend on NPC, item, or quest state.
- Player Identity and PlayerSave **must not** depend on world, NPC, item, or quest state.
- Any dependency on networking, snapshots, ticks, or runtime evaluation **is forbidden**.

**Cycles**
- Dependency cycles **are forbidden**.
- Any detected circular dependency **must** cause save or restore rejection.

## 8. Forbidden Ordering Patterns

The following patterns **are explicitly forbidden** and **must be validation-rejectable**:

- Save or restore ordering that differs from the defined sequence
- Partial save or partial restore across systems
- Restore against missing or unresolved dependencies
- Cross-system inference to resolve missing state
- Replay-based or event-log-based reconstruction
- Activation of runtime evaluation during restore
- Use of networking or snapshots to satisfy persistence dependencies

No exception paths are permitted.

## 9. Ordering Invariants

The following invariants **must always hold** and **must be validation-enforceable**:

1. **Closed Ordering**
   - Save and restore ordering **must** be explicit and closed.

2. **Acyclic Dependencies**
   - The persistence dependency graph **must** be acyclic.

3. **Atomicity**
   - Cross-system save and restore **must** be all-or-nothing.

4. **Deterministic Restore**
   - Given identical persisted truth, restore outcomes **must** be identical.

5. **No Runtime Execution**
   - Restore **must not** execute or resume runtime logic.

6. **Server Authority**
   - All persistence ordering decisions **must** be server-owned.

## 10. Lock Criteria

This document is considered **LOCKED** when all of the following are true:

- Persistence ordering for save and restore is explicit and deterministic.
- Dependency relationships are complete, acyclic, and closed.
- All forbidden ordering and dependency patterns are enumerated and rejectable.
- Restore legality conditions are sufficient to prevent partial or inferred state.
- No modal or speculative language remains.
- Validation harnesses can deterministically accept or reject persistence ordering correctness.
