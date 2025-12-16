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
