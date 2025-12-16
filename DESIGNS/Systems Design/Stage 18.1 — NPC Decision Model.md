# Stage 18.1 — NPC Decision Model

## 1. Purpose

This document defines the **NPC Decision Model** at a structural level.  
It establishes what a decision is at runtime, what information a decision is permitted to consume, what a decision may produce, and the authority and ordering constraints under which decisions exist.  
This document introduces no AI algorithms, behavior logic, or content semantics.

## 2. Decision Definition

An **NPC decision** is a deterministic, server-evaluated computation that derives a **structural intent** from valid inputs.

**Decision Characteristics**
- A decision **is server-defined and server-owned**.
- A decision **is evaluated deterministically**.
- A decision **does not directly perform actions**.
- A decision **does not mutate world, NPC, or player state**.
- A decision **does not guarantee execution of its output**.

A decision represents *selection*, not *execution*.

## 3. Decision Inputs

### Allowed Input Categories

An NPC decision **must consider only** the following categories of information.  
An NPC decision **must not** consider any information outside this closed set.

- NPC runtime state
- NPC perception results (as defined in Stage 16.2)
- World state visible within the NPC’s valid scope
- Zone residency context
- Deterministic, server-owned signals produced by prior systems

### Input Constraints
- All inputs **must** be server-authoritative.
- All inputs **must** be deterministic and reproducible.
- All inputs **must** be valid at the time of evaluation.

### Forbidden Inputs

A decision **must never** consider:
- Client-authored or client-suggested data
- UI state or presentation data
- Narrative or dialogue content
- Quest logic or quest state transitions
- Randomized or non-deterministic values
- Wall-clock time or external system state

## 4. Decision Outputs

### Decision Output Definition

A decision **must produce exactly one** of the following:
- A structural intent descriptor, or
- An explicit no-op outcome

### Output Constraints
- Outputs **must not** execute behavior.
- Outputs **must not** mutate state.
- Outputs **must not** bypass lifecycle, tick, or persistence rules.
- Outputs **must** be structurally valid regardless of whether they are later acted upon.

Decision outputs represent *eligibility* or *preference*, not *action*.

## 5. Decision Evaluation Constraints

### Evaluation Rules
- Decision evaluation **must** occur only under server authority.
- Decision evaluation **must** occur only while the NPC is tick-participating.
- Decision evaluation **must not** occur mid-tick.
- Decision evaluation **must not** occur during restore.

### Determinism Requirements
- Identical inputs **must** always produce identical outputs.
- No implicit state, cache, or cross-tick memory **is permitted**.

## 6. Authority & Ordering Invariants

The following invariants **must always hold**:

- Decisions **must** be evaluated only after perception is finalized.
- Decisions **must** be evaluated before any action-resolution systems.
- Decisions **must not** influence tick ordering.
- Decisions **must not** trigger persistence directly.
- Decisions **must never** bypass validation, save, or restore boundaries.
- Clients **must never** influence decision inputs, ordering, or outputs.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- AI algorithms, behavior trees, planners, or utility systems
- Combat tactics or movement logic
- Dialogue, narrative, or personality systems
- Quest logic or progression rules
- Action execution or animation
- Persistence formats or schemas
- Implementation details or engine internals
