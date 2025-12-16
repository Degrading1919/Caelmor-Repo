# Stage 19.5 — World & Zone Validation Scenarios

## 1. Purpose

This document defines the **validation scenarios** required to deterministically verify the legality, authority safety, persistence correctness, and restore integrity of **world** and **zone** runtime constructs.
Its sole purpose is to enable automated validation harnesses to **accept or reject runtime state unambiguously**.
This document introduces no implementation details, tooling, or content logic.

## 2. Scope

This document applies exclusively to **server-authoritative runtime validation** at 10 Hz.
It defines structural validation scenarios for worlds, zones, their composition, authority boundaries, and persistence/restore behavior.
It does not define testing frameworks, instrumentation, or performance criteria.

## 3. Canon Dependencies

This document is **subordinate to and constrained by** the following LOCKED canon:

- Stage 19.0 — World & Zone Runtime Architecture
- Stage 19.1 — Zone Runtime Definition
- Stage 19.2 — World Runtime Definition
- Stage 19.3 — World & Zone Authority Boundaries
- Stage 19.4 — World & Zone Persistence Model
- Stage 9 — Validation Philosophy & Harness

If any conflict exists, the above documents take precedence.

## 4. Validation Coverage Overview

Validation **must** cover the following structural dimensions exhaustively:

- World runtime existence and legality
- Zone runtime existence and legality
- World–zone composition correctness
- Authority boundary enforcement across all layers
- Persistence and restore correctness without replay or inference

Validation **must** fail deterministically on any violation.
No partial acceptance is permitted.

## 5. World Validation Scenarios

The validation harness **must** detect and reject the following illegal world states:

1. **Invalid World Identity**
   - A world runtime instance without a unique server-defined identity **must** be rejected.
   - A client-authored or client-influenced world identity **must** be rejected.

2. **World Existence Without Server Authority**
   - A world not created or owned by the server **must** be rejected.
   - A world existing outside server control **must** be rejected.

3. **Illegal World Lifetime**
   - A world that self-creates, self-duplicates, or self-resurrects **must** be rejected.
   - A world persisting runtime-only state across unload **must** be rejected.

4. **Illegal Tick Participation**
   - A world participating in the tick without explicit server inclusion **must** be rejected.
   - A world mutating state outside authoritative tick boundaries **must** be rejected.

## 6. Zone Validation Scenarios

The validation harness **must** detect and reject the following illegal zone states:

1. **Zone Without World**
   - A zone not belonging to exactly one world **must** be rejected.
   - A zone existing independently of a world **must** be rejected.

2. **Invalid Zone Identity**
   - A zone without a unique identity within its world **must** be rejected.
   - A client-authored or client-derived zone identity **must** be rejected.

3. **Illegal Zone Authority**
   - A zone acting independently of world authority **must** be rejected.
   - A zone mutating world-owned state **must** be rejected.

4. **Illegal Zone Tick Participation**
   - A zone participating in the tick while its world is not tick-participating **must** be rejected.
   - A zone mutating state outside tick boundaries **must** be rejected.

## 7. Authority Boundary Validation

The validation harness **must** detect and reject all authority boundary violations, including but not limited to:

1. **Downward Authority Leakage**
   - World authority delegated to zones **must** be rejected.
   - Zone authority delegated to entities **must** be rejected.

2. **Upward Authority Mutation**
   - Entities mutating zone or world authority **must** be rejected.
   - Quests mutating world, zone, or entity lifecycle **must** be rejected.

3. **Ownership Violations**
   - Zones owning players, NPCs, items, or quests **must** be rejected.
   - Worlds redefining player identity, session lifecycle, or quest ownership **must** be rejected.

4. **Client Authority Intrusion**
   - Any client-authored or client-influenced authoritative state **must** be rejected.

## 8. Persistence & Restore Validation

The validation harness **must** detect and reject the following persistence and restore violations:

1. **Partial Persistence**
   - Partial world persistence **must** be rejected.
   - Partial zone persistence **must** be rejected.

2. **Runtime State Persistence**
   - Persistence of tick, evaluation, ordering, or runtime-only state **must** be rejected.

3. **Illegal Restore Ordering**
