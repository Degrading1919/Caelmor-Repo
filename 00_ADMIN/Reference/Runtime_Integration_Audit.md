# Runtime Integration Audit

## 1) Integration Summary
- **Issues Identified**
  - Duplicate runtime identifier definitions (`EntityHandle` and `SessionId`) in the Tick and Onboarding scopes risked type drift and compilation conflicts.
  - Combat runtime lacked the Tick namespace import, preventing alignment with the shared entity handle contract.
- **Fixes Applied**
  - Consolidated runtime entity handles under `Caelmor.Runtime.Tick` by removing redundant definitions from the tick eligibility registry and reusing the canonical tick contracts.
  - Centralized the onboarding `SessionId` definition by removing the duplicate struct from the handoff hooks and relying on the primary onboarding declaration.
  - Added the missing tick namespace import to the combat runtime to bind it to the authoritative entity handle and tick contracts.
- **Commits Made**
  - `fix(types): unify runtime identifiers`
  - `chore(audit): add runtime integration audit`

## 2) Dependency Map (High Level)
- **Tick & Simulation Core**: `TickSystem` and `WorldSimulationCore` own deterministic tick driving, eligibility gating, and execution phases. All simulation participants and phase hooks depend on these contexts.
- **Combat Runtime**: Depends on world simulation participation hooks, combat eligibility services, intent queues/gates, resolution engine, and outcome commit sinks. Uses tick-scoped `EntityHandle`.
- **Inventory Runtime**: Uses `IServerAuthority` and internal mutation gating; independent of simulation phases but must respect simulation mutation windows.
- **Quest Runtime**: Depends on `IServerAuthority`, quest mutation gating, player lifecycle query surfaces, and deterministic progression evaluators. Executes outside simulation ticks.
- **Replication Runtime**: Hooks into post-tick phase via `ITickPhaseHook`, depends on session indices, replication eligibility gates, committed-state readers, and snapshot queues.
- **Onboarding & Sessions**: Manage session creation, player binding, tick eligibility registration, and client-control handoff hooks; provide canonical `SessionId`.

## 3) Missing Systems / Files Needed for “System Code Complete”
- **Networking Transport & Message Routing**: Required to deliver replication snapshots and receive client intents. Needs transport-agnostic interfaces bound to session management and replication queues; must respect server authority and deterministic ordering.
- **Connection/Session Handshake Pipeline**: Necessary to validate clients, issue `SessionId`s, and negotiate onboarding start. Should integrate with onboarding system, snapshot eligibility registry, and server authority checks.
- **World Bootstrap & Zone Startup**: A server entrypoint that initializes tick/simulation cores, registers participants (combat, NPCs, replication), and loads default zones per `IWorldManager`. Ensures deterministic entity indexing before tick start.
- **Entity Registry / World State Container**: Deterministic entity index implementation that the tick/simulation core can query. Must coordinate with player/NPC runtime instance managers and residency systems.
- **Authoritative Input Command Ingestion**: A command queueing surface that freezes combat intents (and future gameplay commands) per tick, enforcing “no mid-tick mutation” and server validation.
- **Interest Management / Visibility Culling**: Eligibility layer for replication to restrict entities per session. Should plug into `IReplicationEligibilityGate` and zone residency/topology data.
- **Snapshot Serialization & Delta Format**: A serialization contract for `ClientReplicationSnapshot` suitable for transport/diffing; ideally a deterministic binary or compact JSON representation plus hashing for `ReplicatedEntityState` fingerprints.
- **Persistence IO Hooks**: Persistence adapters for player saves, inventory, and quest states to bridge runtime systems to storage, respecting mutation gates and restore contracts.
- **Server Logging & Diagnostics**: Minimal logging/error handling strategy for invariant violations (e.g., mid-tick eligibility changes) with metrics/hooks for operational visibility.
- **Runtime Loop Entrypoint / Build Script**: A runnable host (console service) that wires authority implementations, validation harness toggles, and starts/stops the tick/simulation threads deterministically.

## 3a) Thread-Boundary Mailbox Plans for Missing Systems

### Networking Transport & Message Routing
- **Threads**
  - `NetworkTransportThread`: owns socket I/O, decode/encode, and no gameplay state access. All methods in this thread must only touch transport buffers.
  - `TickThread`: authoritative simulation; only thread allowed to mutate world state or session routing tables.
- **Inbound Path (client → server)**
  - `NetworkTransportThread` decodes raw packets into immutable `DecodedClientMessage` records. No UnityEngine objects are created or mutated.
  - Each decoded message is enqueued into a bounded `ConcurrentQueue<DecodedClientMessage>` named `InboundMailbox` (capacity tuned to avoid unbounded growth; drop/backpressure strategy to be configured). Enqueue performs no per-tick allocations by reusing pooled records where possible.
  - The tick boundary drains `InboundMailbox` on `TickThread` into a `FrozenCommandBatch` that plugs into Authoritative Input Command Ingestion. Draining is done once per tick, copying payloads into pooled batch buffers before processing to avoid mid-tick mutations.
- **Outbound Path (server → client)**
  - Post-tick, `TickThread` builds replication snapshots and enqueues immutable `OutboundSnapshot` records into a bounded `ConcurrentQueue<OutboundSnapshot>` named `OutboundMailbox`. This queue is the only cross-thread handoff; gameplay state reads happen before enqueuing and are never mutated off-thread.
  - `NetworkTransportThread` dequeues `OutboundSnapshot` entries and serializes/sends them over the transport. Transport code must not reference UnityEngine objects or simulation state beyond the snapshot payload.
- **Routing**
  - `TickThread` owns authoritative routing decisions (session-to-connection mapping). The network thread receives routing tokens within each record (e.g., `SessionId`, `ConnectionId`) and must not modify routing tables; it simply uses the tokens already embedded by the tick pipeline.

### Connection/Session Handshake Pipeline
- **Threads**
  - `NetworkTransportThread`: accepts new connections and runs cryptographic/identity validation off the tick thread.
  - `TickThread`: assigns authoritative `SessionId`, registers onboarding eligibility, and mutates world state.
- **Handshake Steps**
  - Transport decodes handshake requests into immutable `HandshakeRequest` records and enqueues them into a bounded `ConcurrentQueue<HandshakeRequest>` (`HandshakeMailbox`). No session/world mutation occurs here.
  - At tick boundary, `TickThread` drains `HandshakeMailbox`, validates credentials against server authority, issues `SessionId`, and registers the player with onboarding and replication eligibility services. All mutations occur solely on `TickThread`.
  - The resulting `HandshakeAccepted`/`HandshakeRejected` responses are enqueued by `TickThread` into `OutboundMailbox` (or a dedicated `HandshakeResponseMailbox`) for the transport thread to send. The network thread only serializes/sends; it never mutates session registries.
- **Backpressure & Safety**
  - Mailboxes are bounded; overflow triggers explicit logging/metrics and optional connection-level throttling on the network thread. No UnityEngine objects or world references are touched off-thread.

### Persistence IO Hooks
- **Threads**
  - `PersistenceIOThread` (or thread pool): performs disk/database operations asynchronously. Must never reference UnityEngine objects or mutate gameplay state.
  - `TickThread`: applies loaded/committed data to authoritative state during mutation windows.
- **Load/Save Flow**
  - `TickThread` requests persistence operations by enqueuing immutable `PersistenceJob` records into a bounded `ConcurrentQueue<PersistenceJob>` consumed by the persistence worker. Jobs reference serialized DTOs or snapshot payloads, not live world objects.
  - Persistence worker executes I/O and posts `PersistenceResult` records into an `ApplyOnTickQueue` (`ConcurrentQueue<PersistenceResult>`). Completion callbacks do not touch gameplay state.
  - At tick boundary (or designated post-tick phase), `TickThread` drains `ApplyOnTickQueue`, validates results, and applies state mutations within the authoritative mutation window. Any failures are handled on `TickThread` with diagnostics; off-thread code only logs transport/persistence errors.
- **Memory & Allocation Discipline**
  - Use pooled buffers for serialized payloads to avoid per-tick allocations. Queueing uses reused record instances where safe, with clear ownership to prevent cross-thread mutation after enqueue.
  - All cross-thread DTOs are immutable once enqueued; any mutation requires a new record crafted on `TickThread`.

## 4) Risks & Next Steps
- **Highest-Risk Integration Points**
  - Cross-system identifier drift (entity/session/player) could silently desync replication and combat/quest eligibility unless kept centralized.
  - Tick-phase misuse (mid-tick mutations, out-of-window snapshotting) may cause nondeterminism; requires stricter guards and diagnostics.
  - Missing bootstrap/registry layers leave simulation participants unregistered, blocking end-to-end server startup.
- **Recommended Next Stage**
  - Implement the deterministic entity registry/world bootstrap plus authoritative command ingestion, then wire replication eligibility and transport stubs.
- **Suggested Order of Execution**
  1. Deliver entity registry + world bootstrap/host entrypoint to run the simulation loop.
  2. Add authoritative input ingestion and intent freezing for combat (and future systems).
  3. Implement interest management and snapshot serialization to unlock end-to-end replication.
  4. Introduce logging/diagnostics and persistence adapters to harden runtime stability.
