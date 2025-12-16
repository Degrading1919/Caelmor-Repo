# Stage 11.1 — Combat Runtime System Breakdown
**Scope:** Runtime system decomposition only  
**Authority:** Server-authoritative, deterministic (10 Hz), schema-first  
**Dependencies:** Stage 10.0–10.4 (Combat Architecture, Intents, State Model, Resolution, Authority), Phase1_4 Technical Foundation

This document defines the **combat runtime systems** required to implement the locked combat architecture.
It establishes **clear authority boundaries**, **inputs/outputs**, and **tick participation** for each system.

This document does NOT define:
- Implementation details
- Schema fields
- Gameplay tuning, math, or balance
- Client-side behavior
- Persistence redesign

---

## 1) Combat Intent Intake & Queue System

### Primary Responsibility
Accept, validate-at-intake, order, and queue combat action intents for deterministic resolution.

### Inputs Consumed
- Client-submitted combat action intents
- Server tick boundary (10 Hz)
- Entity authority context

### Outputs Produced
- Accepted or rejected intent dispositions
- Deterministically ordered intent queue for the next resolution tick

### Authoritative State Owned
- Intent queue (ephemeral, per-tick)
- Per-entity intent sequence counters

### Tick Phase Participation
- **Pre-Tick:** Accept submissions
- **Tick Boundary:** Freeze queue for resolution at T+1

### Explicit Non-Responsibilities
- No combat state checks beyond intake legality
- No resolution, cancellation success, or outcome decisions
- No persistence writes

### Dependencies on Other Combat Systems
- Depends on **Combat State Authority** for basic referential validation
- Feeds **Combat Resolution Engine**

---

## 2) Combat State Authority System

### Primary Responsibility
Own and expose the authoritative combat state model for all entities.

### Inputs Consumed
- Resolution outputs from the Combat Resolution Engine
- Persistence hydration snapshots (on restore)

### Outputs Produced
- Authoritative combat state snapshots
- Read-only state views for resolution and validation

### Authoritative State Owned
- Entire combat state model (as locked in Stage 10.2)

### Tick Phase Participation
- **Read:** During resolution phases
- **Write:** During application phase only

### Explicit Non-Responsibilities
- No intent intake
- No damage or mitigation calculation
- No networking or broadcasting
- No persistence I/O (ownership only)

### Dependencies on Other Combat Systems
- Receives mutations from **Combat Resolution Engine**
- Serves state to **Intent Intake**, **Resolution**, and **Validation**

---

## 3) Combat Resolution Engine

### Primary Responsibility
Execute the authoritative, per-tick combat resolution pipeline.

### Inputs Consumed
- Ordered intent queue
- Read-only combat state snapshot
- Cancellation requests
- Deterministic ordering rules

### Outputs Produced
- Resolution decisions per intent (succeeded, failed, nullified, canceled)
- Proposed damage instances
- Proposed state transitions

### Authoritative State Owned
- None (pure resolution; no long-lived state)

### Tick Phase Participation
- **Full Tick:** Executes Stage 10.3 resolution phases A–H

### Explicit Non-Responsibilities
- No persistence commits
- No networking
- No client prediction
- No schema interpretation beyond contracts

### Dependencies on Other Combat Systems
- Consumes from **Intent Intake & Queue**
- Reads from **Combat State Authority**
- Produces outputs for **Damage & Mitigation Processing**

---

## 4) Damage & Mitigation Processing System

### Primary Responsibility
Transform proposed damage into finalized damage outcomes via mitigation contracts.

### Inputs Consumed
- Proposed damage instances from the Resolution Engine
- Read-only combat state (for mitigation context)

### Outputs Produced
- Finalized damage outcomes
- Mitigation result records

### Authoritative State Owned
- None (damage and mitigation are outcome records)

### Tick Phase Participation
- **Mid-Tick:** After resolution calculation, before application

### Explicit Non-Responsibilities
- No damage math specification
- No state mutation
- No intent ordering or conflict resolution

### Dependencies on Other Combat Systems
- Receives proposed damage from **Combat Resolution Engine**
- Feeds finalized outcomes back to **Combat Resolution Engine** for application

---

## 5) Combat Outcome Broadcasting System

### Primary Responsibility
Publish authoritative combat outcomes to observing clients.

### Inputs Consumed
- Resolution reports
- Damage and mitigation outcomes
- State transition summaries

### Outputs Produced
- Deterministic, ordered combat outcome notifications

### Authoritative State Owned
- None

### Tick Phase Participation
- **Post-Tick:** After authoritative application completes

### Explicit Non-Responsibilities
- No resolution
- No prediction
- No authority decisions
- No persistence

### Dependencies on Other Combat Systems
- Consumes reports from **Combat Resolution Engine**
- Reads snapshots from **Combat State Authority**

---

## 6) Combat Persistence Integration System

### Primary Responsibility
Integrate combat state with the existing persistence framework at valid checkpoints.

### Inputs Consumed
- Authoritative combat state (owned elsewhere)
- Save/load lifecycle signals

### Outputs Produced
- Persisted combat-relevant state (if defined by locked schemas)
- Hydrated combat state on restore

### Authoritative State Owned
- None (integration only)

### Tick Phase Participation
- **Checkpoint Boundary Only**
- Never mid-tick

### Explicit Non-Responsibilities
- No resolution
- No replay
- No event journaling
- No schema changes

### Dependencies on Other Combat Systems
- Reads from **Combat State Authority**
- Coordinates with global save system (non-combat)

---

## 7) Combat Validation Hooks System

### Primary Responsibility
Expose deterministic observation points for integration testing and validation.

### Inputs Consumed
- Intent queue snapshots
- Resolution reports
- Damage and mitigation outcomes
- Combat state snapshots

### Outputs Produced
- Validation snapshots
- Deterministic assertions for Stage 9-style harnesses

### Authoritative State Owned
- None

### Tick Phase Participation
- **Observation Only:** Before and after resolution phases

### Explicit Non-Responsibilities
- No mutation
- No fixes or retries
- No authority decisions
- No gameplay interpretation

### Dependencies on Other Combat Systems
- Observes **Intent Intake**, **Resolution**, **Damage/Mitigation**, and **State Authority**

---

## Authority Boundary Integrity (Justification)

Systems are intentionally **not merged** across these boundaries because:
- Intent handling must remain separate from resolution to preserve deterministic intake rules
- Combat state ownership must remain singular and mutation-controlled
- Damage and mitigation must remain outcome transforms, not state owners
- Broadcasting and persistence must not influence resolution
- Validation must observe without side effects

Any future merging must preserve these exact authority separations.

---

## Explicit Non-Goals (Reaffirmed)

This stage does NOT:
- Define combat math or tuning
- Define schemas or JSON
- Define client behavior
- Define networking protocols
- Introduce new combat concepts

---

## Exit Condition

Stage 11.1 is complete when:
- Every combat runtime responsibility is owned by exactly one system
- No system has overlapping authority
- Tick participation is explicit
- Dependencies are unidirectional and deterministic
- No system’s responsibility is ambiguous
