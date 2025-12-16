# Stage 7.3 — Inventory & Resource Grant Integration  
**Design Reference Document**

---

## 1. Overview

The **Inventory & Resource Grant Integration System** is a server-authoritative runtime layer responsible for converting a successful gathering resolution into concrete inventory state changes.

This system:
- Consumes a `GatheringResolutionResult` (Stage 7.2)
- Determines which **ResourceItem key(s)** should be granted
- Updates a minimal player inventory model
- Emits an informational `ResourceGrantedEvent`

It operates strictly:
- **After** gathering resolution (Stage 7.2)
- **Before** crafting, consumption, or persistence systems

All schemas and prior systems are canonical and immutable.  
This system does not reinterpret outcomes, risks, or tuning.

---

## 2. Core Responsibilities

### Grant Eligibility
- Process **only** results where:
  - `resource_grant_allowed == true`
- Respect all flags from `GatheringResolutionResult`
- Never reinterpret or override resolution outcomes

### Resource Determination
- Map:
  - `node_type_key`
  - `gathering_skill_key`
- To one or more **ResourceItem keys**

At this stage, mapping may be implemented using:
- Placeholder lookup tables
- Hardcoded mappings

No probability, yield tuning, rarity, or balance logic is permitted.

### Inventory Integration
- Insert granted resources into the player’s inventory state
- Inventory model is intentionally minimal:
  - Resource item key
  - Count
- Stacking rule:
  - Same key increments count

Inventory must be:
- Server-authoritative
- Deterministic
- Serializable

### Event Emission
Emit a `ResourceGrantedEvent` containing:
- `player_id`
- `source_node_instance_id`
- A list of granted items (key + count)

This event is **informational only** and does not handle UI or networking.

---

## 3. Inventory State Model

### Minimal Inventory Requirements

The inventory model required for Stage 7.3 is intentionally constrained:
- Keyed collection of resource items
- Deterministic update semantics
- Serializable representation for future persistence

No slots, weight, capacity, or stack limits exist at this stage.

### Conceptual Inventory Shape

```csharp
// Illustrative only
struct InventoryEntry
{
    string ResourceItemKey;
    int Count;
}

struct PlayerInventoryState
{
    int PlayerId;
    List<InventoryEntry> Entries;
}```

## 4. Resource Grant Mapping Approach
Mapping Inputs
The mapping must use:
node_type_key
gathering_skill_key

Mapping Outputs
The mapping produces:
One or more ResourceItem keys
A deterministic count per key (typically 1 at this stage)

Determinism Rules
Same inputs must always produce the same outputs
If multiple items are granted, ordering must be stable

Placeholder Mapping Examples
Illustrative placeholders only
These examples are not canonical keys and must not be treated as final content.

(node_type_key = "example_node", gathering_skill_key = "example_skill") → ["example_resource_item"]

(node_type_key = "example_node", gathering_skill_key = "alt_example_skill") → ["example_resource_item_alt"]

All production mappings must reference real keys from ResourceItem.schema.json.

## 5. Conceptual C# Structures (Illustrative Only)
Illustrative only — these examples are not production code.
These keys do not exist in current sample sets and must never be copied verbatim into implementation.

Resource Grant Unit
csharp
Copy code
struct ResourceGrant
{
    string ResourceItemKey;
    int Count;
}
Grant Input (from Stage 7.2)
csharp
Copy code
struct GatheringResolutionResult
{
    int NodeInstanceId;
    string NodeTypeKey;
    string GatheringSkillKey;

    bool ResourceGrantAllowed;
    bool NodeDepletionAllowed;
    bool RiskTriggered;

    GatheringOutcome Outcome;
}
Informational Event Payload
csharp
Copy code
struct ResourceGrantedEvent
{
    int PlayerId;
    int SourceNodeInstanceId;
    List<ResourceGrant> Grants;
}
## 6. Grant Flow (Deterministic)
High-Level Behavior
If resource_grant_allowed == false → no operation

Otherwise:
Resolve resource grants
Apply inventory updates
Emit informational event

Pseudocode
text
Copy code
ProcessResourceGrant(result, playerId):

  if result.ResourceGrantAllowed == false:
      return NoOp

  grants = GrantMapping.Resolve(
              result.NodeTypeKey,
              result.GatheringSkillKey)

  if grants is empty:
      Emit ServerDiagnosticEvent(
          type = "MissingResourceGrantMapping",
          nodeTypeKey = result.NodeTypeKey,
          gatheringSkillKey = result.GatheringSkillKey,
          nodeInstanceId = result.NodeInstanceId,
          playerId = playerId
      )
      return NoOp

  for each grant in grants:
      Inventory.AddOrIncrement(
          playerId,
          grant.ResourceItemKey,
          grant.Count
      )

  Emit ResourceGrantedEvent(
      playerId,
      result.NodeInstanceId,
      grants
  )

  return Applied
Inventory Add Rule
If an entry exists for ResourceItemKey → increment Count

Otherwise → create new entry with initial Count
No validation beyond this is performed.

## 7. Performance & Determinism Notes
Expected Scale
Grant operations are infrequent relative to server tick rate
Inventory updates must be O(1) or near O(1)

Recommended Internal Representation (Conceptual)
Use an internal dictionary for mutation:
Dictionary<string, int>
Serialize to a stable list representation when required

Avoided Anti-Patterns
Parallel arrays for keys/counts
Silent failure on missing mappings
Randomized or time-based logic
Full-inventory scans per grant

## 8. Extension Points (Not Implemented)
Inventory Expansion
Slot-based inventory models
Stack limits, metadata, item instances
UI-facing structures
Yield & Quantity Logic
Variable counts

Multi-item outputs
Skill- or tool-based modifiers

Persistence
Save/load of inventory state
Transactional safety guarantees

Networking
Inventory delta replication
Join-in-progress synchronization

Crafting Integration
Atomic grant/consume operations
Crafting reservation or locking

Diagnostics & Audit
Centralized logging for grant anomalies
Anti-cheat and QA instrumentation

## 9. Non-Goals
This system explicitly does not handle:
Inventory capacity or weight
UI or client sync
Persistence implementation
Crafting logic
Economy or balance tuning
Probability or RNG
XP or skill progression
Combat or risk mechanics
Node depletion logic