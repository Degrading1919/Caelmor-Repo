# Stage 7.1 — Resource Node Runtime System  
**Design Reference Document**

---

## 1. Overview

The **Resource Node Runtime System** governs how gatherable resource nodes exist, are interacted with, deplete, and respawn in the world at runtime.

This system implements **RuneScape-style gathering behavior**:
- Nodes are fixed in the world
- Nodes can be gathered when available
- Nodes deplete on successful interaction
- Nodes respawn after a deterministic number of server ticks

This document captures **design intent and runtime responsibilities only**.  
All schemas are **canonical and immutable**.  
This system consumes schema data but does not define or alter it.

---

## 2. Core Responsibilities

The Resource Node Runtime System is responsible for:

### Node Instance Lifecycle
- Managing runtime instances of placed resource nodes
- Tracking availability and depletion state
- Restoring nodes after respawn

### Tick-Based Depletion & Respawn
- Scheduling node respawns using **server ticks**
- Ensuring all timing is deterministic and authoritative
- Avoiding wall-clock time, coroutines, or timers

### Server-Authoritative Interaction Handling
- Validating all gather attempts on the server
- Rejecting invalid interactions
- Emitting authoritative events on success

---

## 3. Runtime Data Model

### Node Definition vs Node Instance

**Node Definition**
- Loaded from `ResourceNode.schema.json`
- Immutable, shared data
- Examples:
  - node type key
  - allowed gathering skills
  - static properties

**Node Instance**
- Runtime-only, per-placement state
- Represents a specific node in the world

### Required Runtime State Fields

Each node instance must track:
- Node instance ID
- Node type key (schema reference)
- World position
- Current state:
  - Available
  - Depleted
- Respawn tick (only when depleted)

---

## 4. Tick Model

### Server Tick Assumptions
- Server runs at **10 Hz**
- All world object updates occur during the server tick
- Tick index is the sole source of time

### Deterministic Update Loop
- No real-time clocks
- No coroutines or delayed callbacks
- All state changes occur inside tick processing

### Respawn Scheduling Approach
- When a node depletes, a respawn tick is calculated:
respawnTick = currentTick + respawnDuration

markdown
Copy code
- Respawn logic compares scheduled ticks against the current server tick
- Nodes become available when their respawn tick is reached

Respawn duration is **runtime tuning data only** and not a permanent schema responsibility.

---

## 5. Interaction Flow

All gathering interactions are server-authoritative.

### Step-by-Step Validation

1. Player submits gather request
2. Server validates:
 - Node instance exists
 - Node is currently available
 - Node definition exists
 - Player possesses **at least one allowed gathering skill**
3. On success:
 - Node transitions to `Depleted`
 - Respawn tick is scheduled
 - Resource grant event is emitted

### Event Emission

- Resource grant events **do not modify inventory**
- Events serve as authoritative signals for downstream systems

---

## 6. Conceptual C# Structures (Illustrative Only)

> **Note:** These examples are **non-compilable** and exist solely to illustrate intent.

### Resource Node Instance (Conceptual)

struct ResourceNodeInstance
{
  int NodeInstanceId;
  string NodeTypeKey;
  Vector3 WorldPosition;

  NodeState State;          // Available / Depleted
  int RespawnTick;          // Valid only when depleted
}

### Resource Node Definition (Conceptual)
struct ResourceNodeDef
{
    string NodeTypeKey;
    List<string> AllowedGatheringSkills;
}

### Resource Grant Event (Conceptual)
struct ResourceGrantedEvent
{
    int ServerTick;
    int PlayerId;
    int NodeInstanceId;
    string NodeTypeKey; // Placeholder; later emits ResourceItem keys
}

## 7. Performance & Scaling Notes
- Expected Scale
 - Hundreds of nodes per region
 - Thousands globally over time

- Data Structures
 - Dictionary for O(1) node lookup by instance ID
 - Priority queue / min-heap for respawn scheduling

- Avoided Anti-Patterns
 - No per-node polling each tick
 - No coroutines or timers
 - No per-frame logic
 - No client-side prediction

- This ensures:
 - Minimal per-tick overhead
 - Deterministic behavior
 - Predictable performance under load

## 8. Extension Points (Not Implemented)
- Inventory Integration
 - Resource grant events will later emit ResourceItem keys
 - Inventory logic remains fully separate
 - Skill Resolution

- Future systems may add:
 - Skill levels
 - Tool requirements
 - Conditional access
 - Persistence
 - Depleted nodes and respawn ticks can be serialized
 - On load, respawn scheduling is reconstructed

- Networking
 - Node state changes become reliable world-object messages
 - Clients receive authoritative availability updates only

## 9. Non-Goals
- This system explicitly does not handle:
 - Experience gain
 - Yield quantities
 - Inventory modification
 - Animations or VFX
 - Client-side prediction
 - Region loading or streaming
 - Skill leveling logic
 - Tool or equipment requirements

- All of the above are handled by separate systems.