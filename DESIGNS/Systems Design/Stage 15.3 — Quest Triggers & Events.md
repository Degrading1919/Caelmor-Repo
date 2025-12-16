# Stage 15.3 — Quest Triggers & Events

## 1. Purpose

This document defines the structural, server-authoritative relationship between **quest instances** and **server-side events** used to drive quest progression evaluation.
It specifies how quests observe events, how events are scoped and owned, and how observation and evaluation remain deterministic and authority-safe.
This document introduces no quest content, triggers, objectives, or scripting logic.

## 2. Event Observation Model

**Definition**

Event observation is the passive, server-controlled process by which quest instances are notified of server-recognized events for the sole purpose of progression evaluation.

**Rules**
- Quest instances **must** observe events passively.
- Quest instances **must not** emit, author, mutate, or acknowledge events.
- Event observation **must** occur under exclusive server authority.
- Event observation **must not** guarantee quest progression.
- Event observation **must not** directly cause quest state transitions.
- Event observation **must** feed into progression evaluation as defined in Stage 15.2.

**Eligibility Constraint**
- A quest instance **must not** observe events unless:
  - it belongs to a valid Player Identity, and
  - it is in a non-terminal state.

## 3. Event Scope & Ownership

**Event Scope**

All observed events **must** be server-recognized and scoped to one of the following exclusive categories:

- **Per-Player Events**
  - Events scoped to a single Player Identity.

- **Per-World Events**
  - Events scoped to a specific world runtime.

- **Per-Zone Events**
  - Events scoped to a specific zone within a world.

**Scope Rules**
- A quest instance **must** observe only events that are relevant to:
  - its owning Player Identity, and
  - its associated world context.
- A quest instance **must not** observe events:
  - authored by clients,
  - outside its world scope,
  - outside its zone scope when zone-scoped relevance is required.
- Events **must not** be globally visible to quest instances without explicit scope relevance.

**Ownership**
- All events **must** be owned and recognized by the server.
- Client-authored or client-suggested events **must never** be observed by quest instances.

## 4. Trigger Evaluation Rules

**Definition**

Trigger evaluation is the structural assessment of observed events against the current quest state to determine whether progression evaluation should occur.

**Rules**
- Trigger evaluation **must** be server-authoritative.
- Trigger evaluation **must** operate only on observed, scoped, server-recognized events.
- Trigger evaluation **must** be structural and content-agnostic.
- Trigger evaluation **must not** embed:
  - quest-specific objectives,
  - narrative meaning,
  - reward logic,
  - scripting behavior.
- Trigger evaluation **must not** directly cause quest state transitions.
- Trigger evaluation **must** defer all state change decisions to Stage 15.2 progression rules.

**State Constraint**
- Trigger evaluation **must not** occur if the quest instance is in a terminal state.
- Trigger evaluation **must not** occur without a valid quest state.

## 5. Ordering & Determinism Guarantees

The following guarantees are mandatory and enforceable by validation:

- Event recognition **must** occur before any quest observation or evaluation.
- Quest observation **must** reflect the server-defined event order.
- Event ordering **must** be server-owned and deterministic.
- Clients **must never** reorder, inject, suppress, or modify events.
- Quest evaluation **must not** occur prior to authoritative event recognition.
- Given identical persisted truth and event order, quest evaluation outcomes **must** be identical.

No engine dispatch, buffering, or timing mechanisms are defined in this document.

## 6. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Event Arrival During Session Deactivation**
- The event **must** be ignored for quest observation.
- No trigger evaluation **must** occur.

**Event Arrival During Tick Transition**
- The event **must** be observed according to server ordering.
- Trigger evaluation **must** occur only when progression evaluation is legally permitted.
- No partial evaluation **must** apply.

**Event Arrival During Server Crash**
- The event **must** be treated as non-existent unless persisted as authoritative truth.
- No quest observation or evaluation **must** occur on restore for discarded events.

**Duplicate or Stale Event Signals**
- Duplicate events **must** be ignored deterministically.
- Stale events **must not** be re-applied or re-evaluated.
- No quest state **must** reflect duplicated or stale event influence.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Specific quest triggers or event types
- Quest objectives, conditions, or success criteria
- Scripting systems or rule engines
- Rewards, consequences, or completion effects
- NPCs, dialogue, narrative, or world storytelling
- Client-side event handling or authority
- Engine-level event dispatch, queues, or timing details
