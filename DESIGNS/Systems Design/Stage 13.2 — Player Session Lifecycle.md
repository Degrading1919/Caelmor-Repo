# Stage 13.2 — Player Session Lifecycle

## 1. Purpose

This document defines the canonical, server-authoritative **Player Session Lifecycle** for Caelmor.
It specifies how a Player Session is created, activated, deactivated, and terminated, and how those transitions are ordered and enforced.
All future systems must treat this document as authoritative and compatible with Stage 13.1 (Player Identity Model).

## 2. Session Definition

**Definition**  
A **Player Session** is a server-defined, ephemeral runtime construct representing the participation of exactly one Player Identity in a world runtime through a live connection context.

**Properties**
- A Player Session **must** be server-defined.
- A Player Session **must** be ephemeral.
- A Player Session **must** be bound to **exactly one** Player Identity.
- A Player Session **must not** be identity.
- A Player Session **must not** be persistence.
- A Player Session **must not** define player existence.

**Existence Rule**
- Player existence is defined solely by Player Identity and its associated PlayerSave.
- The presence or absence of a Player Session **must not** create, destroy, or redefine a player.

## 3. Session Creation

**Definition**  
**Session Creation** is the server-side act of instantiating a new Player Session record in a non-active state.

**Rules**
- Session creation **must** be initiated by the server.
- Session creation **must** be bound to a specific Player Identity at creation time.
- Session creation **must not** imply activation.
- Session creation **must not** require a loaded world state.
- Session creation **must not** modify PlayerSave.
- Session creation **must** fail deterministically if the Player Identity is invalid or unknown.

**Multiplicity**
- Multiple sessions **must not** be active concurrently for the same Player Identity.
- Creation of a new session while another session exists for the same Player Identity **must** be resolved by the server according to deterministic rules defined in later sections.

## 4. Session Activation

**Definition**  
**Session Activation** is the server-authoritative transition of a Player Session into an active, world-participating state.

**Preconditions**
A Player Session **must not** activate unless all of the following are true:
- The bound Player Identity is valid.
- The PlayerSave associated with the Player Identity **exists and is loaded**.
- The target world runtime is available to accept the session.

**Rules**
- Session activation **must** be initiated and ordered by the server.
- Session activation **must** be an explicit state transition distinct from creation.
- Session activation **must** result in exactly one active session for the Player Identity.
- Session activation **must not** occur if another session is already active for the same Player Identity.
- Clients **must not** activate sessions or influence activation ordering.

## 5. Session Deactivation

**Definition**  
**Session Deactivation** is the server-authoritative transition of an active Player Session into an inactive state without destroying the session record.

**Characteristics**
- Deactivation is temporary.
- Deactivation **must not** destroy Player Identity.
- Deactivation **must not** destroy PlayerSave.

**Rules**
- Session deactivation **must** be initiated by the server.
- Loss of client connection after activation **must** result in session deactivation.
- Deactivated sessions **must not** be treated as active participants in the world.
- Deactivation **must** preserve deterministic ownership of the Player Identity.

## 6. Session Termination

**Definition**  
**Session Termination** is the server-authoritative destruction of a Player Session and all of its ephemeral runtime state.

**Rules**
- Session termination **must** be initiated by the server.
- Session termination **must** perform deterministic cleanup of all session-scoped runtime state.
- Session termination **must not** destroy Player Identity.
- Session termination **must not** destroy or mutate PlayerSave.
- A terminated session **must not** be reactivated.

**Finality**
- After termination, the session **must** cease to exist as a runtime entity.

## 7. Session State Invariants

The following invariants are mandatory and enforceable by validation:

1. **Server Authority**
   - All session state transitions **must** be initiated and ordered by the server.
   - Clients **must never** create, activate, deactivate, extend, or terminate sessions.

2. **Identity Binding**
   - Every Player Session **must** be bound to exactly one Player Identity.
   - A Player Session **must never** change its bound Player Identity.

3. **Single Active Session**
   - The server **must enforce** that at most one Player Session is active per Player Identity at any time.

4. **Activation Ordering**
   - A PlayerSave **must** be loaded before a Player Session becomes active.
   - A Player Session **cannot** be active without a valid PlayerSave.

5. **Ephemerality**
   - Player Sessions **must not** be persisted as authoritative state.
   - Player Sessions **must** be reconstructible or discardable without replay.

6. **Determinism**
   - Given the same inputs and restore state, session lifecycle transitions **must** resolve identically.

## 8. Failure & Edge Case Handling

The following cases **must** be handled deterministically:

**Client Disconnect Before Activation Completes**
- The session **must not** activate.
- The session **must** be terminated by the server.

**Client Disconnect After Activation**
- The active session **must** be deactivated.
- Player Identity and PlayerSave **must** remain intact.

**Duplicate Connection Attempts**
- The server **must** deterministically resolve which session is eligible for activation.
- The client **must not** influence the resolution outcome.
- At most one session **must** be active.

**Server Crash During Active Session**
- All Player Sessions **must** be treated as non-existent on restore.
- Player Identity and PlayerSave **must** be restored from persisted truth.

**Session Cleanup on Crash Restore**
- No session **may** resume as active after restore.
- New session creation and activation **must** follow the same lifecycle rules as initial entry.

## 9. Explicit Non-Goals

This document does not define and must not be interpreted as defining:

- Account systems, authentication, or platform identity
- Matchmaking, lobbies, parties, or invitation flows
- Networking protocols, transports, or replication mechanics
- Tick timing, save timing, autosave cadence, or reconnect timing
- Grace periods, retries, heuristics, or timeout logic
- UI, onboarding, menus, or user-facing session concepts
- Any form of client authority, negotiation, or session ownership
