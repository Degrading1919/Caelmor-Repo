# Stage 13 — Player Lifecycle & World Session Authority

---

## 1. Purpose of This Stage

Stage 13 defines **how a player exists in Caelmor** at runtime.

This stage formalizes:
- Player identity
- Session ownership
- World attachment
- Tick participation
- Save / restore boundaries

This stage exists to eliminate implicit assumptions currently spread across systems and scaffolding.

**This stage answers exactly one question:**
> When does a player become real to the server, and under what rules do they remain real?

---

## 2. Canon Scope & Authority Statement

From this stage forward:

- Player existence is **server-defined and server-owned**
- Clients must never determine:
  - spawn timing
  - tick participation
  - save boundaries
  - world attachment
- All runtime systems may assume this stage is enforced

This stage is **authoritative** for all future systems involving:
- Combat
- Gathering
- Crafting
- Quests
- Death
- Respawn
- Zone transitions
- Co-op (future)

---

## 3. Player Identity Model

### 3.1 Player Identity

Defines:
- Persistent player identifier
- Relationship between:
  - Account (conceptual)
  - PlayerSave
  - Active session

Rules:
- One active session per player
- Player identity exists independently of connection state
- Identity is never client-generated

---

## 4. Session Lifecycle

### 4.1 Session Creation

Defines:
- When a session begins
- Preconditions for activation
- World state availability requirements

### 4.2 Session Termination

Defines:
- Graceful disconnect
- Forced disconnect
- Crash scenarios

Rules:
- Session termination always triggers deterministic cleanup
- No ghost sessions
- No dangling tick participation

---

## 5. World Attachment & Residency

### 5.1 World Binding

Defines:
- How a session attaches to a world instance
- Authority boundaries between:
  - World
  - Zone
  - Player

Rules:
- World state is authoritative
- Player cannot exist outside a world context

### 5.2 Zone Residency

Defines:
- What it means to be in a zone
- When zone logic begins applying
- When zone logic ceases

Non-goals:
- No dynamic instancing
- No shard selection
- No matchmaking

---

## 6. Spawn & Respawn Contracts

### 6.1 Initial Spawn

Defines:
- When spawn occurs relative to session start
- Spawn location resolution rules
- Tick alignment guarantees

### 6.2 Death Handling (Structural Only)

Defines:
- What death means at the system level
- Removal from active participation
- Transition to respawn eligibility

Explicitly excluded:
- Death penalties
- Narrative consequences
- Difficulty tuning

### 6.3 Respawn

Defines:
- Respawn timing rules
- Authority over respawn location
- Tick-safe re-entry into the world

---

## 7. Tick Participation Rules

### 7.1 Entry Into Tick

Defines:
- The exact tick boundary at which a player becomes active
- Ordering guarantees relative to:
  - Combat resolution
  - Economy resolution

### 7.2 Exit From Tick

Defines:
- How and when a player stops participating
- Cleanup ordering guarantees

Rules:
- No partial-tick existence
- No mid-tick removal
- All transitions occur on explicit boundaries

---

## 8. Save & Restore Boundaries

### 8.1 Save Triggers

Defines:
- When PlayerSave snapshots occur
- Relationship between:
  - Session
  - Save
  - WorldSave

### 8.2 Restore Semantics

Defines:
- Rejoin after disconnect
- Rejoin after crash
- Consistency guarantees

Rules:
- No replay-based reconstruction
- No inferred state
- Restore uses persisted truth only

---

## 9. Failure & Edge Case Handling

Defines deterministic behavior for:
- Client disconnect during combat
- Client disconnect during crafting
- Client disconnect during gathering
- Server crash mid-session

Rules:
- Server truth always wins
- Incomplete actions resolve deterministically
- No rollback systems introduced

---

## 10. Validation Expectations (Stage 9 Integration)

Stage 13 must provide validation scenarios for:
- Join
- Leave
- Crash
- Rejoin
- Death
- Respawn

Validation philosophy:
- Fail loud
- Assert invariants
- Never silently recover

---

## 11. Explicit Non-Goals (Locked Out)

This stage does not include:
- UI flows
- Onboarding experience
- Matchmaking
- Lobby systems
- Party systems
- Scaling or sharding
- Balance
- Co-op logic
- Narrative logic

Any attempt to add these is a canon violation.

---

## 12. Lock Criteria

Stage 13 is considered LOCKED when:
- Player existence rules are unambiguous
- Tick participation is explicitly defined
- Save and restore boundaries are deterministic and enforceable
