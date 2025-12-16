# Stage 13.1 — Player Identity Model

## 1. Purpose

This document defines the canonical, server-authoritative **Player Identity Model** for Caelmor runtime.
It establishes what a “player” is in system terms and how identity relates to saves and sessions.
All future systems must treat this document as the single source of truth for player identity semantics.

## 2. Core Identity Concepts

**Identity**  
A stable, immutable identifier representing a single player entity within the game’s authoritative model.

**Persistence**  
An identity persists across world sessions and across changes in connection state.

**Authority**  
The server is the only authority that defines, creates, validates, and enforces player identity.

**Separation of Concerns**  
- **Player Identity** answers: “Who is this player?”
- **PlayerSave** answers: “What persisted truth belongs to this player?”
- **Player Session** answers: “Is this identity currently participating in this world process, and through what live connection?”

These concepts are strictly separated and must never be conflated.

## 3. Player Identity

**Definition**  
A **Player Identity** is a server-defined, globally unique, immutable identifier representing exactly one player for the lifetime of that player’s existence in the game.

**Rules**
- A Player Identity **must** be **server-defined**.
- A Player Identity **must** be **globally unique** across all players known to the server.
- A Player Identity **must** be **persistent across sessions**.
- A Player Identity **must** be **independent of connection state**.
- A Player Identity **must never** be client-generated, client-supplied, or client-derived.
- A Player Identity **must never** be modified after creation.
- A Player Identity **must** be the sole key used by server systems to associate:
  - persisted state (PlayerSave), and
  - participation over time (Player Sessions).

**Creation Assumption (Explicit)**
- The server creates a Player Identity exactly once per new player at the moment the server decides that a new player exists.
- The mechanism by which the server makes that decision is out of scope for this document and must not be inferred as an account system, authentication flow, lobby, or matchmaking feature.

## 4. PlayerSave Relationship

**Definition**  
A **PlayerSave** is the persisted, authoritative state associated with exactly one Player Identity.

**Cardinality**
- There is **exactly one** PlayerSave for **exactly one** Player Identity.
- The relationship between Player Identity and PlayerSave is **one-to-one**.

**Rules**
- A PlayerSave **must** be keyed by Player Identity.
- A PlayerSave **must** represent **persisted truth** only.
- A PlayerSave **must not** represent history, replay logs, event streams, or reconstruction inputs.
- A PlayerSave **must** be sufficient for restore without requiring replay of gameplay logic.
- A PlayerSave **must not** be shared by multiple Player Identities.
- A Player Identity **must not** map to multiple PlayerSaves.
- A PlayerSave **must exist and be successfully loaded** before any Player Session for the associated Player Identity is considered active.
- A Player Session **must not** complete activation without a valid PlayerSave bound to its Player Identity.

## 5. Player Session Relationship

**Definition**  
A **Player Session** is a server-defined, ephemeral runtime association between a Player Identity and the current world runtime, representing active participation through a live connection context.

**Cardinality Over Time**
- A single Player Identity has a **one-to-many (over time)** relationship with Player Sessions.
- Each Player Session belongs to **exactly one** Player Identity.

**Concurrency Rule**
- At any moment in time, the server **must allow at most one** active Player Session per Player Identity.
- If multiple connection attempts occur for the same Player Identity, the server **must deterministically resolve** which single session is active.
- The client **must not** influence, participate in, or override this resolution decision in any way.

**Rules**
- A Player Session **must** be server-defined.
- A Player Session **must not** be treated as identity.
- A Player Session **must not** be treated as persistence.
- Loss of connection **must not** change Player Identity.
- Loss of connection **must** end or deactivate the Player Session according to server authority.

## 6. Identity Invariants

The following invariants are mandatory and must be enforceable by validation:

1. **Server Authority**
   - Player Identity creation and validation **must** be performed by the server.
   - Client input **must never** be accepted as the source of Player Identity.

2. **Global Uniqueness**
   - No two distinct players **can** share the same Player Identity.

3. **Immutability**
   - A Player Identity **must never** change after creation.

4. **Connection Independence**
   - Player Identity **must** remain defined regardless of connection state.

5. **Save One-to-One**
   - Each Player Identity **must** map to **exactly one** PlayerSave.
   - Each PlayerSave **must** map to **exactly one** Player Identity.

6. **Save–Session Ordering**
   - A PlayerSave **must** exist and be loaded before a Player Session is considered active.
   - A Player Session **cannot** be active without a valid PlayerSave bound to its Player Identity.

7. **Single Active Session**
   - The server **must enforce** that at most one Player Session is active per Player Identity at any time.

8. **Deterministic Session Enforcement**
   - When multiple connection attempts target the same Player Identity, the server **must deterministically resolve** the conflict.
   - The client **must never** influence which session is accepted, rejected, or terminated.

9. **Session Ownership**
   - Every Player Session **must** be associated with exactly one Player Identity.

10. **No Replay Requirement**
    - Restore of persisted player state **must not** require replay of gameplay logic.
    - PlayerSave content **must** be treated as authoritative persisted truth, not as reconstruction history.

## 7. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Account systems, authentication, entitlements, platform identity, or third-party identity providers
- Matchmaking, lobbies, party systems, friend systems, or invitation flows
- UI, onboarding, menus, character selection screens, or user-facing terminology
- Networking transport layers, optimization, packet formats, or replication efficiency
- Spawn rules, tick timing, save timing, autosave cadence, disconnect grace periods, or reconnection timing
- Any client authority, prediction, rollback, reconciliation, or client-driven identity behaviors
- Schema definitions or data formats for identity, save files, or session records
