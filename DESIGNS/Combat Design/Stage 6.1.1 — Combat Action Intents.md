# Stage 10.1 — Combat Action Intents
**Canon Lock: Input Contract Only**

This document defines the **minimum viable combat action intent layer** for Caelmor.
It establishes what the server accepts, validates, and queues for combat resolution.
This layer is **pure intent** — not outcome, not balance, not animation, not AI.

All intents defined here are:
- Server-authoritative
- Deterministic
- Tick-aligned (10 Hz)
- Serializable
- Validated before queuing
- Resolution-agnostic

No intent in this document:
- Applies damage
- Consumes stamina
- Applies cooldowns
- Determines hit/miss
- Advances animation state
- Resolves timing beyond queue order

---

## 1. Intent Submission & Queue Semantics (Global)

### Acceptance Window
- Intents are submitted by clients during tick **T**
- Server validates and enqueues intents for **tick T+1**
- No intent is ever accepted or resolved mid-tick

### Ordering Rules
- Intents are ordered deterministically by:
  1. Server tick number
  2. Submitting entity ID
  3. Intent sequence number (per-entity, monotonic)

No client-provided ordering is trusted.

### Conflict Handling
- Conflicts are **not resolved at intent level**
- Multiple intents from the same entity in the same tick:
  - Are accepted or rejected individually
  - Resolution system decides which succeed
- Intents never cancel, overwrite, or modify other intents directly

### Rejection Rules
- Any failed validation rejects the intent outright
- Rejected intents:
  - Are not queued
  - Produce no side effects
  - Are not persisted

---

## 2. Intent: `CombatAttackIntent`

### Purpose
Represents an entity’s intent to perform a direct combat attack against a target.

This intent exists to:
- Drive melee, ranged, and unarmed attack systems
- Trigger threat, reaction, and defensive resolution paths
- Provide a single, unified attack input for all combatants

### Required Fields
- AttackerEntityId
- TargetEntityId
- AttackProfileKey

### Optional Fields
- EquippedItemId
- DeclaredFacing
- ClientDeclaredTargetPoint

### Immediate Validation Rules
- Attacker entity exists and is alive
- Target entity exists and is attackable
- AttackProfileKey is valid and known
- Attacker has authority to submit actions
- EquippedItemId (if provided) is owned and equipped

### What This Intent Does NOT Decide
- Hit or miss
- Damage amount
- Attack speed or cadence
- Stamina or resource costs
- Cooldowns
- Animation selection
- Line-of-sight or range success

---

## 3. Intent: `CombatDefendIntent`

### Purpose
Represents an entity’s intent to actively defend against incoming attacks.

This intent exists to:
- Support blocking, parrying, bracing, and shield use
- Allow proactive defense without predicting specific attacks
- Feed defensive resolution systems

### Required Fields
- DefenderEntityId
- DefenseProfileKey

### Optional Fields
- EquippedItemId
- DeclaredFacing

### Immediate Validation Rules
- Defender entity exists and is alive
- DefenseProfileKey is valid
- EquippedItemId (if provided) is owned and equipped
- Entity is allowed to enter a defensive state

### What This Intent Does NOT Decide
- Which attacks are blocked or parried
- Damage mitigation values
- Duration of defense
- Stamina drain
- Perfect vs partial defense outcomes

---

## 4. Intent: `CombatAbilityIntent`

### Purpose
Represents the intent to use a non-basic combat ability.

This intent exists to:
- Support skills, techniques, and special combat actions
- Decouple ability execution from UI and cooldown logic
- Provide a unified entry point for complex combat actions

### Required Fields
- CasterEntityId
- AbilityKey

### Optional Fields
- TargetEntityId
- TargetPosition
- EquippedItemId

### Immediate Validation Rules
- Caster entity exists and is alive
- AbilityKey is valid and known
- Required targets (if any) exist
- EquippedItemId (if required by ability) is valid and equipped

### What This Intent Does NOT Decide
- Resource consumption
- Cooldowns
- Effect magnitude
- Area-of-effect resolution
- Success or failure
- Target eligibility beyond existence

---

## 5. Intent: `CombatMovementIntent`

### Purpose
Represents combat-context movement that must be resolved inside the combat system.

This intent exists to:
- Support dodges, steps, lunges, retreats
- Allow combat movement to interact with attack and defense resolution
- Keep movement deterministic and tick-aligned during combat

### Required Fields
- EntityId
- MovementProfileKey

### Optional Fields
- DeclaredDirection
- TargetPosition

### Immediate Validation Rules
- Entity exists and is alive
- MovementProfileKey is valid
- Movement is allowed in current combat state

### What This Intent Does NOT Decide
- Final position
- Collision outcomes
- Invulnerability frames
- Stamina cost
- Opportunity attacks

---

## 6. Intent: `CombatInteractIntent`

### Purpose
Represents intentional interaction with a combat-relevant object or entity.

This intent exists to:
- Support actions like opening gates, triggering mechanisms, mounting devices
- Allow combat systems to reason about interaction risk and interruption
- Keep interaction explicit and auditable

### Required Fields
- EntityId
- InteractionTargetId
- InteractionTypeKey

### Optional Fields
- EquippedItemId

### Immediate Validation Rules
- Entity exists and is alive
- Interaction target exists
- InteractionTypeKey is valid
- Entity has permission to interact

### What This Intent Does NOT Decide
- Interaction success
- Time to complete
- Interruptibility
- Combat consequences
- Animation or timing

---

## 7. Intent: `CombatCancelIntent`

### Purpose
Represents an entity’s intent to cancel or withdraw from a previously submitted combat action.

This intent exists to:
- Support deliberate disengagement
- Allow systems to reason about aborted actions deterministically
- Avoid implicit cancellation logic

### Required Fields
- EntityId
- TargetIntentSequenceNumber

### Optional Fields
- None

### Immediate Validation Rules
- Entity exists and is alive
- Target intent exists and belongs to entity
- Target intent has not yet been resolved

### What This Intent Does NOT Decide
- Whether the referenced action is actually cancelable
- Whether cancellation succeeds or fails
- Penalties or consequences for cancellation
- Partial execution effects
- Cooldown consequences

Whether cancellation is allowed or takes effect is determined later by
combat resolution and combat state rules.

---

## 8. Minimality Justification

Each intent exists because it serves **multiple systems**:

- **Attack** → offense, threat, defense interaction
- **Defend** → mitigation, posture, reaction systems
- **Ability** → skills, techniques, future magic
- **Movement** → positioning, avoidance, spacing
- **Interact** → environment, objectives, emergent combat
- **Cancel** → control, determinism, player agency

Any additional intent would either:
- Duplicate resolution logic
- Encode outcomes instead of intent
- Collapse multiple systems into one concern

Such intents are intentionally excluded.

---

## 9. Explicit Non-Goals (Global)

This stage does NOT:
- Define combat math
- Define balance
- Define timing or cooldowns
- Define AI behavior
- Define animation or FX
- Define hit resolution
- Define persistence changes

This document is an **input contract** only.

---

**End of Stage 10.1**
