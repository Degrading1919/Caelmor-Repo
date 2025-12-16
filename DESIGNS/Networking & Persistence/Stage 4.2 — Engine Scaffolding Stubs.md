## 1. Server Tick Manager

### Purpose
Owns the authoritative **global simulation tick** running at 10 Hz and provides a deterministic hook for server-side systems to update.

This is the single source of truth for simulation time.

### Ownership
- Engine / Host
- Exists independently of gameplay systems
- Referenced (read-only) by Stage 7 systems

### Minimal Public Interface (Scaffolding Only)

```csharp
// Scaffolding stub — no gameplay logic
public interface IServerTickSource
{
    int CurrentTick { get; }
}

public interface IServerTickListener
{
    void OnServerTick(int tick);
}

public sealed class ServerTickManager : IServerTickSource
{
    public int CurrentTick { get; private set; }

    // Called once during engine boot
    public void StartTickLoop() { /* Not implemented */ }

    // Registration only; invocation order defined by engine
    public void RegisterListener(IServerTickListener listener) { /* Not implemented */ }
}

Must NOT Do
Must not contain gameplay logic
Must not own persistence
Must not manage zones or players
Must not expose mutable tick state

2. World / Zone Lifecycle Hooks
Purpose
Provide explicit lifecycle hooks so world-owned systems (e.g., Resource Nodes) can initialize and teardown safely around persistence boundaries.

Ownership
Engine / World layer
Independent of gameplay systems
Invoked during boot, zone load, and zone unload

Minimal Public Interface (Scaffolding Only)
csharp
Copy code
// Scaffolding stub
public interface IWorldLifecycleListener
{
    void OnWorldBoot();
    void OnWorldShutdown();
}

public interface IZoneLifecycleListener
{
    void OnZoneLoaded(string zoneId);
    void OnZoneUnloading(string zoneId);
}

public sealed class WorldManager
{
    public void RegisterWorldListener(IWorldLifecycleListener listener) { /* Not implemented */ }
    public void RegisterZoneListener(IZoneLifecycleListener listener) { /* Not implemented */ }
}

Must NOT Do
Must not stream or manage spatial logic
Must not spawn gameplay objects directly
Must not save state itself
Must not generate NodeInstanceIds

3. Player Session Manager
Purpose
Defines a server-side player session abstraction with stable identity and explicit session boundaries.

Provides the moment where player-owned state (inventory) becomes writable.

Ownership
Engine / Server authority
Independent of networking transport
Referenced by inventory, crafting, and persistence systems

Minimal Public Interface (Scaffolding Only)
csharp
Copy code
// Scaffolding stub
public interface IPlayerSession
{
    int PlayerId { get; }
}

public interface IPlayerSessionListener
{
    void OnPlayerSessionStart(IPlayerSession session);
    void OnPlayerSessionEnd(IPlayerSession session);
}

public sealed class PlayerSessionManager
{
    public void RegisterListener(IPlayerSessionListener listener) { /* Not implemented */ }

    // Resolves or creates a stable PlayerId
    public IPlayerSession GetSessionForConnection(object connectionToken)
    {
        throw new NotImplementedException();
    }
}

Must NOT Do
Must not contain inventory logic
Must not process player actions
Must not perform persistence directly
Must not assume network protocol details

4. Action Serialization Queue
Purpose
Ensures player actions are processed sequentially and safely, preventing concurrent mutation of player or world state.

Integrates with the server tick loop.

Ownership
Engine / Host
Sits between networking input and gameplay systems

Minimal Public Interface (Scaffolding Only)
csharp
Copy code
// Scaffolding stub
public interface ISerializedAction
{
    int PlayerId { get; }
    void Execute(); // Invoked by engine, not by gameplay systems
}

public sealed class ActionSerializationQueue
{
    // Enqueue action from network or input layer
    public void Enqueue(ISerializedAction action) { /* Not implemented */ }

    // Called by ServerTickManager once per tick
    public void ProcessQueuedActions() { /* Not implemented */ }
}

Must NOT Do
Must not implement gameplay logic
Must not reorder actions nondeterministically
Must not bypass the tick loop
Must not directly mutate persistence

5. Save Checkpoint Coordinator
Purpose
Coordinates logical persistence checkpoints across multiple save scopes so related mutations are committed together.

Ensures PlayerSave and WorldSave are flushed in the same checkpoint cycle.

Ownership
Engine / Persistence layer
Independent of gameplay systems
Invoked at safe boundaries (tick end, disconnect, shutdown)

Minimal Public Interface (Scaffolding Only)
csharp
Copy code
// Scaffolding stub
public interface ISaveScope
{
    void Flush(); // Atomic flush of this scope
}

public sealed class SaveCheckpointCoordinator
{
    public void RegisterScope(ISaveScope scope) { /* Not implemented */ }

    // Called by engine at checkpoint boundaries
    public void CommitCheckpoint() { /* Not implemented */ }
}

Must NOT Do
Must not define file formats or databases
Must not perform partial commits
Must not be called directly by gameplay systems
Must not schedule its own timing

6. Ordering & Ownership Summary
Required Initialization Order
ServerTickManager
WorldManager (world boot)
SaveCheckpointCoordinator
PlayerSessionManager
ActionSerializationQueue
Zone load (via WorldManager hooks)
Begin tick loop

Critical Ownership Rules
Gameplay systems observe ticks; they do not own them
Gameplay systems request checkpoints; they do not flush saves
Node identity comes from content placement, never runtime
Player identity is resolved once per session and reused

7. Explicit Non-Goals
These scaffolds must NOT:
Implement Stage 7 gameplay systems
Contain economy or crafting logic
Define persistence formats or storage
Introduce tuning, timing, or balancing
Anticipate MMO-scale infrastructure

They exist solely to unblock safe implementation of locked systems.