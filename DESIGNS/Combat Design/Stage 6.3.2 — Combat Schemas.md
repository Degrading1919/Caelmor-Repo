# Stage 11.2 — Combat Schemas  
**Scope:** Final schema structures only (no implementation, no tuning, no timing).  
**Authority:** Server-authoritative, deterministic (10 Hz).  
**Canon Locks:** Intents, states, runtime systems, and combat architecture are immutable.

This document defines the **final combat schema set** required to implement the locked combat architecture:
- What combat schemas exist
- Structural fields (required vs optional)
- Structural validation constraints (no behavior)
- Field ownership mapping (creation/mutation/consumption) using the locked runtime system list only

---

## Canonical Enumerations (Locked)

### CombatIntentType (exhaustive)
- CombatAttackIntent
- CombatDefendIntent
- CombatAbilityIntent
- CombatMovementIntent
- CombatInteractIntent
- CombatCancelIntent

### CombatState (exhaustive — aligned to Stage 10.2)
- CombatIdle
- CombatEngaged
- CombatActing
- CombatDefending
- CombatRestricted
- CombatIncapacitated

---

# A) Combat Intent Schemas

## A.0 Common Base: `CombatIntentBase`
All intent schemas include the base fields below.

### Required fields
- `intent_id` (string, stable unique identifier)
- `intent_type` (enum: CombatIntentType)
- `actor_entity_id` (string)
- `submit_tick` (int; authoritative tick in which the intent is accepted into the server queue)

### Optional fields
- `client_nonce` (string; opaque client-provided value used only for de-duplication / correlation, not authority)

### Structural constraints
- `intent_type` MUST match the specific schema name.
- No intent may include outcome, damage, mitigation, or resolution fields.

---

## A.1 `CombatAttackIntent`
### Required fields
- Base fields (from `CombatIntentBase`)

### Optional fields
- `target_entity_id` (string; optional to allow untargeted attacks)
- `attack_profile_key` (string; opaque identifier; no mechanics implied)

### Structural constraints
- If `target_entity_id` is present, it MUST be a valid entity identifier.
- `attack_profile_key` is an opaque label only; no parameters permitted.

---

## A.2 `CombatDefendIntent`
### Required fields
- Base fields

### Optional fields
- `defend_profile_key` (string; opaque identifier; no mechanics implied)

### Structural constraints
- No directional, timing, or animation fields.
- `defend_profile_key` is an opaque label only; no parameters permitted.

---

## A.3 `CombatAbilityIntent`
### Required fields
- Base fields
- `ability_key` (string; stable identifier of the ability being invoked)

### Optional fields
- `target_entity_id` (string)
- `ability_context` (object; **restricted to identifiers only**, see constraints)

### Structural constraints
- `ability_context`, if present:
  - MUST contain identifiers only (e.g., `interactable_id`, `target_entity_id`)
  - MUST NOT include numeric tuning values, ranges, costs, durations, or probabilities.

---

## A.4 `CombatMovementIntent`
### Required fields
- Base fields
- `movement_mode` (enum: `Translate`, `Strafe`, `Backstep`; labels only)

### Optional fields
- `target_entity_id` (string)
- `movement_context` (object; identifiers only)

### Structural constraints
- No vectors, distances, velocities, or physics parameters.
- `movement_context` MUST NOT include numeric tuning.

---

## A.5 `CombatInteractIntent`
### Required fields
- Base fields
- `interactable_id` (string)

### Optional fields
- `interaction_kind` (string; opaque routing label)

### Structural constraints
- No UI or client-side interaction fields.

---

## A.6 `CombatCancelIntent`
### Required fields
- Base fields
- `cancel_target_intent_id` (string)

### Optional fields
- `cancel_reason` (string; opaque diagnostic label)

### Structural constraints
- This schema does NOT imply the referenced intent is cancelable; cancellation success is determined later by authority rules.

---

# B) Combat State Schema

## B.1 `CombatEntityState`
Represents an entity’s authoritative combat state.

### Required fields
- `entity_id` (string)
- `state` (enum: CombatState)
- `combat_context_id` (string)

### Optional fields
- `committed_intent_id` (string)
- `state_change_tick` (int)

### Structural validation constraints
- `state` MUST be one of the locked CombatState values defined above.
- Any transition from `CombatIdle` to `CombatEngaged` occurs only when the server authoritatively establishes an active combat context, and a valid `combat_context_id` MUST be assigned before any combat resolution occurs.
- `committed_intent_id`:
  - MUST be present when `state` is `CombatActing` or `CombatDefending`
  - MUST be absent when `state` is `CombatIdle` or `CombatEngaged`
- `combat_context_id`:
  - MUST be present for all non-idle states
  - MAY be empty only when `state` is `CombatIdle`

**Notes**
- No durations, timers, cooldowns, or recovery lengths are represented here.
- This schema exists solely to support legality, ordering references, persistence, and validation.

---

# C) Combat Outcome Schemas

Outcomes are **results**, not actions.  
They are authoritative, server-produced, and opaque to clients.

## C.1 `DamageOutcome`
### Required fields
- `outcome_id` (string)
- `source_entity_id` (string)
- `target_entity_id` (string)
- `resolved_intent_id` (string)
- `damage_amount` (int)

### Optional fields
- `damage_kind_key` (string)
- `damage_tags` (array of string)

### Structural constraints
- Numeric fields represent **resolved outcomes only**.
- Numeric values MUST NOT be treated as tunable inputs, balance parameters, or calculation drivers.
- No formulas, probabilities, or scaling data are permitted.

---

## C.2 `MitigationOutcome`
### Required fields
- `outcome_id` (string)
- `source_entity_id` (string)
- `target_entity_id` (string)
- `resolved_intent_id` (string)
- `mitigated_amount` (int)

### Optional fields
- `mitigation_kind_key` (string)
- `mitigation_tags` (array of string)

### Structural constraints
- Numeric fields represent **resolved outcomes only**.
- Numeric values MUST NOT be treated as tunable inputs, balance parameters, or calculation drivers.
- No probabilities, durations, or mitigation formulas are encoded.

---

## C.3 `IntentResult` (ResolutionResult)
### Required fields
- `intent_id` (string)
- `intent_type` (enum: CombatIntentType)
- `actor_entity_id` (string)
- `result_status` (enum: `Accepted`, `Rejected`, `Resolved`, `Canceled`)
- `authoritative_tick` (int)

### Optional fields
- `reason_code` (string)
- `produced_outcome_ids` (array of string)

### Structural constraints
- Outcome identifiers are references only; outcomes are defined separately.

---

## C.4 `CombatEvent`
Authoritative broadcast envelope.

### Required fields
- `event_id` (string)
- `authoritative_tick` (int)
- `combat_context_id` (string)
- `event_type` (enum: `IntentResult`, `DamageOutcome`, `MitigationOutcome`, `StateChange`)

### Optional fields
- `subject_entity_id` (string)
- `intent_result` (IntentResult)
- `damage_outcome` (DamageOutcome)
- `mitigation_outcome` (MitigationOutcome)
- `state_snapshot` (CombatEntityState)

### Structural constraints
- Exactly one payload must be present, matching `event_type`.
- No client prediction or reconciliation fields.

---

# D) Combat Validation Snapshot Schemas

Snapshots are deterministic, minimal, comparable, and persistence-safe.  
They contain **no transient runtime-only fields** beyond what must be persisted/validated.

## D.1 `CombatEntityValidationSnapshot`
### Required fields
- `entity_id` (string)
- `state` (enum: CombatState)
- `combat_context_id` (string or empty when idle)

### Optional fields
- `committed_intent_id` (string)
- `last_resolved_intent_id` (string)

### Structural constraints
- No transient or runtime-only data.

---

## D.2 `CombatWorldValidationSnapshot`
### Required fields
- `authoritative_tick` (int)
- `entities` (array of CombatEntityValidationSnapshot)

### Optional fields
- `context_ids` (array of string)

### Structural constraints
- Entity ordering must be deterministic for comparison purposes.

---

# E) Field Ownership Mapping (Creation / Mutation / Consumption)

Locked runtime system list (ownership reference only):
- CombatIntentQueueSystem
- CombatStateAuthoritySystem
- CombatResolutionEngine
- DamageAndMitigationProcessor
- CombatOutcomeBroadcaster
- CombatPersistenceAdapter
- CombatValidationHookLayer

## E.1 Ownership Table

### CombatIntentBase (and all intent variants)
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (queue-admission metadata only; no semantic changes)  
- **Consumption:** CombatResolutionEngine, CombatValidationHookLayer

### CombatAttackIntent
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (structural admission only)  
- **Consumption:** CombatResolutionEngine, CombatValidationHookLayer

### CombatDefendIntent
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (structural admission only)  
- **Consumption:** CombatResolutionEngine, CombatValidationHookLayer

### CombatAbilityIntent
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (structural admission only)  
- **Consumption:** CombatResolutionEngine, CombatValidationHookLayer

### CombatMovementIntent
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (structural admission only)  
- **Consumption:** CombatResolutionEngine, CombatValidationHookLayer

### CombatInteractIntent
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (structural admission only)  
- **Consumption:** CombatResolutionEngine, CombatValidationHookLayer

### CombatCancelIntent
- **Creation:** CombatIntentQueueSystem  
- **Mutation:** CombatIntentQueueSystem (structural admission only)  
- **Consumption:** CombatStateAuthoritySystem, CombatResolutionEngine, CombatValidationHookLayer

---

### CombatEntityState
- **Creation:** CombatStateAuthoritySystem  
- **Mutation:** CombatStateAuthoritySystem  
- **Consumption:** CombatResolutionEngine, CombatOutcomeBroadcaster, CombatPersistenceAdapter, CombatValidationHookLayer

---

### DamageOutcome
- **Creation:** DamageAndMitigationProcessor  
- **Mutation:** DamageAndMitigationProcessor (finalization only; no external mutation)  
- **Consumption:** CombatOutcomeBroadcaster, CombatPersistenceAdapter (if persisted), CombatValidationHookLayer

### MitigationOutcome
- **Creation:** DamageAndMitigationProcessor  
- **Mutation:** DamageAndMitigationProcessor (finalization only)  
- **Consumption:** CombatOutcomeBroadcaster, CombatPersistenceAdapter (if persisted), CombatValidationHookLayer

### IntentResult / ResolutionResult
- **Creation:** CombatResolutionEngine  
- **Mutation:** CombatResolutionEngine (finalization only)  
- **Consumption:** CombatOutcomeBroadcaster, CombatPersistenceAdapter (if persisted), CombatValidationHookLayer

### CombatEvent
- **Creation:** CombatOutcomeBroadcaster  
- **Mutation:** CombatOutcomeBroadcaster (envelope finalization only)  
- **Consumption:** CombatOutcomeBroadcaster (network emission), CombatPersistenceAdapter (if persisted as event log), CombatValidationHookLayer

---

### CombatEntityValidationSnapshot
- **Creation:** CombatValidationHookLayer  
- **Mutation:** CombatValidationHookLayer (snapshot assembly only)  
- **Consumption:** CombatValidationHookLayer, CombatPersistenceAdapter (for save/load consistency checks)

### CombatWorldValidationSnapshot
- **Creation:** CombatValidationHookLayer  
- **Mutation:** CombatValidationHookLayer  
- **Consumption:** CombatValidationHookLayer, CombatPersistenceAdapter

---

## Schema Set Completion Criteria

This stage is complete when:
- All locked intents have a structural schema definition
- CombatEntityState is fully specified with the Stage 10.2 state enumeration
- Outcome schemas exist and are separate from actions
- Validation snapshots are minimal and comparable
- Every field has a single clear owner from the locked runtime list
- No tuning, timing, RNG, or client prediction fields exist
