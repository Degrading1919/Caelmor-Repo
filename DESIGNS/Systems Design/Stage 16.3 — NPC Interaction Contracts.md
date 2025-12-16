# Stage 16.3 — NPC Interaction Contracts

## 1. Purpose

This document defines the authoritative **NPC Interaction Contracts** for Caelmor.
It specifies what constitutes an interaction at the runtime level, how interactions are initiated and recognized under server authority, and how interaction signals are structurally resolved and observed.
This document introduces no behavior, dialogue, UI, or content semantics.

## 2. Interaction Definition

**NPC Interaction**

An **NPC interaction** is a server-recognized runtime event indicating that an interaction attempt between a player-controlled entity and an NPC has been evaluated and acknowledged by the server.

**Rules**
- An NPC interaction **must** be a server-recognized event.
- An NPC interaction **must** be distinct from NPC perception.
- An NPC interaction **must not** imply dialogue, animation, AI behavior, or presentation.
- An NPC interaction **must not** directly advance quests, grant rewards, or alter narrative state.
- An NPC interaction **must** exist only as authoritative runtime recognition, not as client-authored state.

## 3. Interaction Initiation Rules

**Initiation Authority**
- All NPC interaction initiation **must** be server-authoritative.
- Client input **must** be treated as advisory intent only and **must not** be authoritative.

**Eligibility Conditions**
An NPC interaction **must not** be recognized unless all of the following are true:
- The NPC runtime instance exists and is valid.
- The NPC runtime instance is attached to a valid world.
- The NPC runtime instance has valid zone residency.
- The interacting player session is active and valid.
- The interaction attempt occurs within a valid authoritative tick context.

**Prohibitions**
- Interactions **must not** be recognized for despawned, destroyed, or invalid NPCs.
- Interactions **must not** be recognized outside a valid world or zone context.
- Interactions **must not** be initiated or forced by clients.

## 4. Interaction Scope & Limits

**Observation Scope**
- NPC interaction events **must** be observable only by server systems explicitly authorized to consume interaction signals.
- Observation **must** be limited by:
  - world attachment,
  - zone residency,
  - ownership and authority rules.

**Forbidden Observation**
- NPC interaction events **must not** be observable by:
  - client-side systems as authoritative truth,
  - systems outside the NPC’s world context,
  - systems outside the NPC’s zone when zone scoping is required.

**Isolation**
- Interaction recognition **must not** bypass perception boundaries.
- Interaction recognition **must not** bypass save, restore, or tick participation rules.

## 5. Interaction Outcomes (Structural Only)

**Allowed Outcomes**
Upon recognition, an NPC interaction **must** result in **exactly one** of the following structural outcomes:
1. Emission of a server-recognized interaction event.
2. Setting or updating of server-owned, non-content interaction flags or markers.

**Constraints**
- Interaction outcomes **must not** execute content logic.
- Interaction outcomes **must not** perform quest state transitions directly.
- Interaction outcomes **must not** grant rewards, items, or narrative progression.
- Partial or multi-outcome resolution **is forbidden**.

## 6. Authority & Ordering Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - All interaction recognition and resolution **must** be performed by the server.
   - Clients **must never** author, force, or resolve interactions.

2. **Deterministic Ordering**
   - Interaction recognition **must** follow server-defined, deterministic ordering.
   - Interactions **must not** reorder tick execution or system processing.

3. **Context Validity**
   - Interactions **must not** occur outside valid tick participation and world context.
   - Interactions **must not** occur during invalid or transitional lifecycle states.

4. **Lifecycle Isolation**
   - Interaction resolution **must not** modify:
     - player identity,
     - player session lifecycle,
     - NPC lifecycle,
     - world attachment,
     - zone residency,
     - tick participation.

## 7. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Interaction with Invalid or Despawned NPC**
- The interaction **must** be rejected.
- No interaction event **must** be emitted.

**Interaction Attempt During Tick Boundary**
- Interaction recognition **must** be deferred to the next valid tick boundary.
- No partial interaction state **must** apply.

**Session Deactivation During Interaction**
- The interaction **must** be discarded.
- No interaction outcome **must** persist.

**Server Crash During Interaction Resolution**
- Any in-progress interaction resolution **must** be discarded.
- Restore **must not** reapply or infer interaction outcomes.

## 8. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Dialogue systems, text, or writing
- NPC reactions, emotions, or behaviors
- AI decision-making or response logic
- Quest advancement, conditions, or rewards
- UI prompts, menus, or presentation
- Animation, audio, or visual feedback
- Client authority or client-side interaction handling
- Implementation details, schemas, or engine internals
