Runtime at a Glance
-------------------
- Startup: host bootstrap registers eligibility gates, simulation participants, and phase hooks via `WorldBootstrapRegistration` before `RuntimeServerLoop.Start()` spins up the deterministic tick thread. Transport/mailboxes and registries are constructed upfront; backpressure budgets come from `RuntimeBackpressureConfig`.
- Handshake: session onboarding uses `SessionHandshakePipeline` (entry in `RuntimeServerLoop`) to stage session IDs and eligibility; transport handoffs are pooled/queue-based with explicit drop paths on disconnect (`RuntimeServerLoop.OnSessionDisconnected`).
- Session activation: `PlayerSessionSystem` binds sessions to players and registers tick/visibility eligibility; runtime registries (`DeterministicEntityRegistry`, `TickEligibilityRegistry`) gate tick participation before simulation starts.
- Tick loop phases (10 Hz fixed step): `WorldSimulationCore` and `TickSystem` run on dedicated threads with deterministic ordering. Phases: (1) pre-tick eligibility evaluation across registered gates, (2) simulation execution over eligible entities and ordered participants, (3) post-tick finalization including effect commit and phase hooks (replication snapshots, diagnostics). `ClientReplicationSnapshotSystem` hooks only in post-tick.
- Replication: post-tick snapshot capture reads committed state only, passes through AOI/eligibility (`IReplicationEligibilityGate`) and queues serialized snapshots (`BoundedReplicationSnapshotQueue`) for transport routing. Snapshots are time-sliced to respect budgets and use pooled buffers; outbound queue enforces caps and drops oldest when exceeded.
- Persistence: persistence write requests are enqueued (`PersistenceWriteQueue`) with per-player/global caps. I/O happens off-thread; completions return through a bounded apply-on-tick mailbox (`PersistenceCompletionQueue` + `PersistenceCompletionPhaseHook`) to keep mutations on the tick thread.
- Shutdown: `RuntimeServerLoop.ShutdownServer()` stops simulation, clears queues/registries (`ClearTransientState`), and disposes pooled resources to avoid lingering eligibility/visibility state.

Thread Boundary Map
-------------------
- Tick/Simulation thread: `WorldSimulationCore` owns authoritative mutation. Eligibility gating, participant execution, effect buffering, and post-tick hooks run here. No blocking I/O; mid-tick eligibility mutations throw.
- Transport thread(s): staged through `PooledTransportRouter` mailboxes; only interact via bounded queues (`DeterministicTransportRouter`, `BoundedReplicationSnapshotQueue`, `AuthoritativeCommandIngress`). Off-thread code must not mutate world state.
- Persistence/I/O thread(s): persistence adapters are external; tick thread enqueues `PersistenceWriteRequest` via `PersistenceWriteQueue` and later applies results during tick windows. No tick-thread I/O.
- Handoff mechanisms: concurrent/bounded queues per session for inbound commands and outbound snapshots; deterministic dequeue on tick thread. Persistence queue has per-player and global caps with drop policies. Authoritative mutation occurs only on tick thread and buffered effects commit in post-tick.

Missing Systems Closure
-----------------------
- Networking Transport & Message Routing: implemented by `PooledTransportRouter` + `DeterministicTransportRouter` with bounded inbound mailboxes and outbound snapshot dequeue. Entry points: `EnqueueInbound`, `RouteQueuedInbound`, `RouteSnapshot`, `TryDequeueSnapshot`. Dependencies: `RuntimeBackpressureConfig`, session IDs, snapshot serializer. Invariants: bounded per-session queues, pooled buffers; tick thread must be sole state mutator. Status: transport worker loop still host-defined.
- Connection/Session Handshake Pipeline: implemented by bounded `SessionHandshakePipeline`. Entry points: enqueue handshake (`TryEnqueue`), tick-thread processing (`TryProcessNext`), reset/drop on shutdown/disconnect. Dependencies: onboarding/session systems. Invariants: handshake mutation occurs on tick thread; mailboxes bounded. Status: present.
- World Bootstrap & Zone Startup: bootstrap logic lives in `WorldBootstrapRegistration.Apply` invoked by `RuntimeServerLoop.Create`. Entry points: registration of eligibility gates, participants, phase hooks before simulation start. Dependencies: `WorldSimulationCore`, `DeterministicEntityRegistry`. Invariants: deterministic ordering, no mutation after start. Status: bootstrap helper present; actual zone loading UNKNOWN.
- Entity Registry / World State Container: implemented by `DeterministicEntityRegistry`. Entry points: `Register`, `Unregister`, `DespawnZone`, `SnapshotEntitiesDeterministic`. Dependencies: `ZoneId`, `EntityHandle`. Invariants: deterministic sorting, per-zone tracking, explicit clears on shutdown; no mid-tick mutation hooks. Pools: internal lists reused. Status: present.
- Authoritative Input Command Ingestion: implemented by `AuthoritativeCommandIngress` and exposed via `DeterministicTransportRouter.RouteInbound`. Entry points: `TryEnqueue`, `TryDequeue`. Dependencies: `RuntimeBackpressureConfig`. Invariants: per-session caps on count/bytes; pooled buffers with explicit dispose; deterministic sequencing. Status: present but transport thread integration unspecified.
- Interest Management / Visibility Culling: implemented via `ZoneSpatialIndex` and gates consumed by replication (`IReplicationEligibilityGate` usage in `ClientReplicationSnapshotSystem`). Entry points: zone residency updates/residency validation systems; visibility gates in replication. Dependencies: entity registry, zone positions. Invariants: pooled arrays, deterministic AOI sorting, no per-tick allocations. Status: present.
- Snapshot Serialization & Delta Format: implemented by `SnapshotDeltaSerializer` and `SerializedSnapshot` inside `DeterministicTransportQueues`. Entry points: `BoundedReplicationSnapshotQueue.Enqueue/TryDequeue`. Dependencies: replication snapshots, fingerprint baselines. Invariants: pooled byte buffers, deterministic order, baseline map updated post-serialization. Status: present.
- Persistence IO Hooks: persistence request DTO (`PersistenceWriteRequest`) and bounded queues (`PersistenceWriteQueue`, `PersistenceCompletionQueue`) exist. Apply-on-tick bridge is provided via `PersistenceCompletionPhaseHook`; actual I/O worker remains host-defined. Entry points: `Enqueue`, `TryDequeue`, `TryEnqueue/Drain` for completions. Dependencies: `RuntimeBackpressureConfig`, player IDs. Invariants: per-player/global caps, drop-oldest policy, no blocking; completion mailbox bounded by count/bytes with drop-oldest. Status: I/O worker UNKNOWN.
- Server Logging & Diagnostics: `TickDiagnostics` and drop counters in queues provide metrics; watchdog/logging threads mentioned in audit but not implemented. Entry points: diagnostics snapshots off tick thread. Invariants: allocation-free counters, no tick-thread formatting. Status: partial; watchdog thread UNKNOWN.
- Runtime Loop Entrypoint / Build Script: `RuntimeServerLoop` coordinates subsystems and start/stop; runnable host beyond loop not present. Entry points: `Start`, `Stop`, `ShutdownServer`. Dependencies: simulation core, transport, handshakes, commands, visibility, entity registry. Invariants: deterministic cleanup, no lingering registrations. Status: host wrapper present; external host/build scripts UNKNOWN.

File Catalog
------------
### ClientReplicationSnapshotSystem.cs
- Purpose / owns what: Post-tick replication snapshot capture with AOI gating and time-sliced serialization for sessions.
- Update cadence: Tick-gated via `ITickPhaseHook` Pre/Post tick; executes only during post-tick finalization.
- Public entry points: `OnPreTick`, `OnPostTick`, `CaptureSnapshotForSession`; invoked by world simulation phase hooks.
- Dependencies: session index/eligibility, replication eligibility gate, state reader, snapshot queue, time-sliced scheduler, backpressure budgets.
- Determinism notes: Enforces post-tick-only capture; sorts entity snapshots by handle; deterministic session iteration.
- Memory notes: Uses pooled arrays for entities and snapshots; time-sliced buffers reused; allocation-free pathways for empty slices.
- Cleanup / lifecycle notes: Returns rented buffers on snapshot disposal via callbacks; tracks allocations in DEBUG.
- Known risks / TODOs: None observed.

### ClientReplicationSnapshotValidationScenarios.cs
- Purpose / owns what: Validation scenarios for replication snapshots and eligibility behavior.
- Update cadence: Test-driven, not part of tick loop.
- Public entry points: Scenario definitions invoked by validation harness adapters.
- Dependencies: Onboarding/session IDs, replication interfaces, tick contexts.
- Determinism notes: Exercises deterministic snapshot ordering/eligibility.
- Memory notes: Relies on test harness fixtures; no runtime pools.
- Cleanup / lifecycle notes: Scenario-scoped data only.
- Known risks / TODOs: None observed.

### CombatIntentQueueSystem.cs
- Purpose / owns what: Intent queueing surface for combat commands; no resolution logic.
- Update cadence: Event-driven enqueue/dequeue by combat runtime.
- Public entry points: Queue APIs defined within file for intent submission/consumption.
- Dependencies: Combat runtime types and command envelopes.
- Determinism notes: Designed for deterministic ordering of intents.
- Memory notes: Minimal data structures; no pooling mentioned.
- Cleanup / lifecycle notes: Queue clearing expected by caller.
- Known risks / TODOs: None observed.

### CombatOutcomeApplicationSystem.cs
- Purpose / owns what: Applies resolved combat outcomes to runtime state (hooks only, no resolution/persistence).
- Update cadence: Called by combat pipeline after resolution.
- Public entry points: Outcome application methods.
- Dependencies: Combat outcome records; state authority expected from callers.
- Determinism notes: Applies deterministic outcomes provided by resolver.
- Memory notes: No pools; relies on caller-provided data.
- Cleanup / lifecycle notes: None beyond caller control.
- Known risks / TODOs: None observed.

### CombatPresentationHookSystem.cs
- Purpose / owns what: Client-side presentation hooks for combat (animations/VFX/audio stubs).
- Update cadence: Event-driven by combat flow; not tick-authoritative.
- Public entry points: Presentation callback hooks.
- Dependencies: Presentation consumers; no state authority.
- Determinism notes: Presentation only; deterministic ordering not critical.
- Memory notes: No pooling; lightweight callbacks.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### CombatReplicationSystem.cs
- Purpose / owns what: Replication hooks for combat state (exposes combat state for replication without mutating).
- Update cadence: Invoked during replication capture or combat events.
- Public entry points: State exposure methods.
- Dependencies: Combat state sources, replication pipelines.
- Determinism notes: Should emit deterministic state snapshots.
- Memory notes: Avoids allocations; relies on external buffers.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### CombatResolutionEngine.cs
- Purpose / owns what: Computes combat outcomes deterministically without side effects.
- Update cadence: Invoked by combat runtime per resolved intent batch.
- Public entry points: Resolution methods producing outcomes.
- Dependencies: Combat intents and state reads.
- Determinism notes: Pure deterministic calculations; no mutation.
- Memory notes: Avoids allocations; pure compute.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### CombatRuntimeSystem.cs
- Purpose / owns what: Orchestrates combat flow across tick participants and state authority checks.
- Update cadence: Tick-gated via simulation participant registration.
- Public entry points: Participant registration hooks and combat tick methods.
- Dependencies: Tick/world simulation contracts, combat subsystems (intent queue, resolver, application, replication).
- Determinism notes: Uses ordered tick participation and deterministic entity handles.
- Memory notes: Uses collections for participants/intents; pooling strategy not explicit.
- Cleanup / lifecycle notes: Expected to unregister on shutdown.
- Known risks / TODOs: None observed.

### CombatRuntimeValidationScenarios.cs
- Purpose / owns what: Validation scenarios for combat runtime determinism and eligibility.
- Update cadence: Test harness driven.
- Public entry points: Scenario definitions used by validation runner.
- Dependencies: Combat runtime/system contracts.
- Determinism notes: Ensures repeatable outcomes in tests.
- Memory notes: Test-only allocations.
- Cleanup / lifecycle notes: Scenario scoped.
- Known risks / TODOs: None observed.

### CombatStateAuthoritySystem.cs
- Purpose / owns what: Enforces combat state authority and validation (no resolution or persistence).
- Update cadence: Event-driven authorization checks.
- Public entry points: Authority validation APIs.
- Dependencies: Combat runtime entities and authority contracts.
- Determinism notes: Authority decisions deterministic.
- Memory notes: No pools.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### DeterministicEntityRegistry.cs
- Purpose / owns what: Deterministic registry of runtime entities per zone with stable snapshots for tick/simulation.
- Update cadence: Event-driven register/unregister/despawn; snapshot read by tick thread.
- Public entry points: `Register`, `Unregister`, `DespawnZone`, `ClearAll`, `SnapshotEntitiesDeterministic`.
- Dependencies: Zone IDs, entity handles.
- Determinism notes: Sorted snapshots; idempotent registration; mid-tick safety via stable snapshots.
- Memory notes: Reuses lists and cached snapshot array; no per-tick allocations when unchanged.
- Cleanup / lifecycle notes: Clear on shutdown/dispose; despawn per-zone.
- Known risks / TODOs: None observed.

### DeterministicTransportQueues.cs
- Purpose / owns what: Queue primitives for inbound commands, outbound snapshots, and persistence writes with deterministic caps and pooled buffers.
- Update cadence: Event-driven enqueue/dequeue by tick and transport threads; snapshot serialization occurs on tick thread.
- Public entry points: `AuthoritativeCommandIngress.TryEnqueue/TryDequeue`, `DeterministicTransportRouter.RouteInbound/RouteSnapshot/TryDequeueSnapshot`, `BoundedReplicationSnapshotQueue.Enqueue/TryDequeue`, `PersistenceWriteQueue.Enqueue/TryDequeue`.
- Dependencies: Backpressure config, session/player IDs, snapshot serializer, persistence write request DTOs.
- Determinism notes: Deterministic sequence numbers, ordered per-session iteration, drop-oldest on overflow; snapshot delta serialization preserves order and updates baseline after serialize.
- Memory notes: Uses `ArrayPool` for payloads and snapshots; returns buffers on dispose; queues capped to prevent unbounded growth.
- Cleanup / lifecycle notes: Dropped items disposed to release pools; metrics tracked; no explicit dispose on queues.
- Known risks / TODOs: None observed.

### InventoryRuntimeSystem.cs
- Purpose / owns what: Server-authoritative inventory mutations with gating and diagnostics hooks.
- Update cadence: Event-driven API; not tick-driven but must align with authority windows.
- Public entry points: Inventory mutation methods (add/remove items) and validation helpers.
- Dependencies: Authority interfaces, validation asserts, resource node definitions.
- Determinism notes: Deterministic ordering of inventory slots and validation paths.
- Memory notes: Uses dictionaries/lists; no pooling; avoid per-call allocations where possible.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### InventoryRuntimeValidationScenarios.cs
- Purpose / owns what: Validation scenarios for inventory runtime behavior.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions for harness.
- Dependencies: Inventory runtime types and validation utilities.
- Determinism notes: Ensures deterministic item handling in tests.
- Memory notes: Test-only allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### MinimalClientControlHandoffHooks.cs
- Purpose / owns what: Concurrent session control handoff hooks for onboarding.
- Update cadence: Event-driven on session control transfer.
- Public entry points: Handoff registration and invocation methods using concurrent dictionaries.
- Dependencies: Onboarding/session IDs.
- Determinism notes: Uses deterministic SessionId keys; concurrency-safe.
- Memory notes: Concurrent dictionary allocations; no pooling.
- Cleanup / lifecycle notes: Supports unregister to avoid leaks.
- Known risks / TODOs: None observed.

### NpcRuntimeSystem.cs
- Purpose / owns what: Runtime system for NPC behavior wiring into world simulation.
- Update cadence: Tick-gated via simulation participants.
- Public entry points: NPC tick/update methods and eligibility registration.
- Dependencies: World simulation interfaces and NPC definitions.
- Determinism notes: Depends on deterministic entity handles and tick ordering.
- Memory notes: Uses collections; no pooling noted.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### NpcRuntimeValidationScenarios.cs
- Purpose / owns what: Validation scenarios for NPC runtime behavior.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: NPC runtime and simulation contracts.
- Determinism notes: Ensures deterministic NPC progression in tests.
- Memory notes: Test-only allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### OnboardingSystem.cs
- Purpose / owns what: Session onboarding registry assigning SessionIds and coordinating initial runtime eligibility.
- Update cadence: Event-driven on handshake completion; not tick-driven.
- Public entry points: Registration of onboarding sessions, completion/handoff methods.
- Dependencies: Concurrent dictionaries, onboarding state types.
- Determinism notes: SessionId stable; no mid-process mutation hazards noted.
- Memory notes: Uses concurrent collections; no pooling.
- Cleanup / lifecycle notes: Supports reset/clear flows for disconnects.
- Known risks / TODOs: None observed.

### OnboardingValidationScenarioExecution.cs
- Purpose / owns what: Executes onboarding validation scenarios with async helpers.
- Update cadence: Test harness asynchronous execution.
- Public entry points: Scenario runner methods.
- Dependencies: Onboarding system interfaces and tasks.
- Determinism notes: Aims for deterministic outcomes via controlled threading.
- Memory notes: Uses tasks and lists; test scope only.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### PersistenceWriteRequest.cs
- Purpose / owns what: DTO describing persistence write job including payload and estimated size.
- Update cadence: Event-driven when persistence requested.
- Public entry points: Struct fields/properties for persistence queue.
- Dependencies: Player/session IDs.
- Determinism notes: Immutable after creation.
- Memory notes: Holds payload reference; size used for caps.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### PlayerIdentity+SaveBindingRuntime.cs
- Purpose / owns what: Runtime binding between player identity and save slots with authority checks.
- Update cadence: Event-driven on login/save interactions.
- Public entry points: Binding lookup/assignment methods.
- Dependencies: Dictionaries keyed by player ID, authority contracts.
- Determinism notes: Deterministic mapping; rejects conflicting bindings.
- Memory notes: Reuses dictionaries; no pooling.
- Cleanup / lifecycle notes: Supports unregister/clear.
- Known risks / TODOs: None observed.

### PlayerId↔SaveBindingValidationScenarios.cs
- Purpose / owns what: Validation scenarios for player identity/save binding behavior.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: Binding runtime.
- Determinism notes: Ensures deterministic binding resolution in tests.
- Memory notes: Test-only allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### PlayerLifecycleSystem.cs
- Purpose / owns what: Manages player lifecycle events (load/unload) and registrations with systems.
- Update cadence: Event-driven per lifecycle transitions.
- Public entry points: Lifecycle handlers for load/unload.
- Dependencies: Session management, entity registry, save/restore systems.
- Determinism notes: Uses deterministic entity/session IDs; coordinates with tick eligibility.
- Memory notes: Uses collections; no pooling noted.
- Cleanup / lifecycle notes: Explicit unload clears registrations.
- Known risks / TODOs: None observed.

### PlayerLifecycleValidationScenarios.cs
- Purpose / owns what: Validation scenarios for player lifecycle system.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: Lifecycle runtime and validation harness.
- Determinism notes: Ensures deterministic lifecycle ordering.
- Memory notes: Test allocations only.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### PlayerRuntimeInstanceManagement.cs
- Purpose / owns what: Manages runtime player instances and mappings to entities.
- Update cadence: Event-driven on player load/unload.
- Public entry points: Registration and lookup methods.
- Dependencies: Entity registry, session IDs.
- Determinism notes: Stable mappings enforced.
- Memory notes: Dictionary-based; no pooling.
- Cleanup / lifecycle notes: Clear/unregister paths provided.
- Known risks / TODOs: None observed.

### PlayerRuntimeInstanceValidationScenarios.cs
- Purpose / owns what: Validation scenarios for player runtime instance management.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: Instance management runtime.
- Determinism notes: Validates deterministic mapping.
- Memory notes: Test scope allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### PlayerSaveRestoreSystem.cs
- Purpose / owns what: Bridges runtime state with persistence save/restore workflows.
- Update cadence: Event-driven on save/load requests; apply results on tick thread.
- Public entry points: Save/restore request methods integrating with persistence queue.
- Dependencies: Persistence DTOs, player/session IDs, authority contracts.
- Determinism notes: Must apply mutations within tick windows; follows deterministic order of requests.
- Memory notes: Minimal allocations; leverages persistence queue caps.
- Cleanup / lifecycle notes: Clears pending operations on unload.
- Known risks / TODOs: None observed.

### PlayerSaveRestoreValidationScenarios.cs
- Purpose / owns what: Validation scenarios for save/restore flows.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: Save/restore runtime and persistence stubs.
- Determinism notes: Validates deterministic apply ordering.
- Memory notes: Test allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### PlayerSessionSystem.cs
- Purpose / owns what: Manages active sessions, eligibility, and routing for runtime systems.
- Update cadence: Event-driven on session connect/disconnect.
- Public entry points: Session registration/removal and snapshot eligibility checks.
- Dependencies: Onboarding/session IDs, eligibility gates.
- Determinism notes: Deterministic session snapshots; stable ordering for replication.
- Memory notes: Uses lists/dictionaries; no pooling.
- Cleanup / lifecycle notes: Clears session caches on disconnect.
- Known risks / TODOs: None observed.

### PlayerZoneResidencySystem.cs
- Purpose / owns what: Tracks player residency per zone for eligibility/interest management.
- Update cadence: Event-driven on zone join/leave; informs tick/replication eligibility.
- Public entry points: Residency registration/update queries.
- Dependencies: Zone IDs, entity handles, residency validation helpers.
- Determinism notes: Stable zone mappings; deterministic queries.
- Memory notes: Uses dictionaries/lists; no pooling noted.
- Cleanup / lifecycle notes: Clear/unregister on zone unload.
- Known risks / TODOs: None observed.

### PlayerZoneResidencyValidationScenarios.cs
- Purpose / owns what: Validation scenarios for zone residency logic.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: Residency system and validation harness.
- Determinism notes: Validates deterministic residency updates.
- Memory notes: Test allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### QuestRuntimeSystem.cs
- Purpose / owns what: Quest progression runtime with deterministic evaluators.
- Update cadence: Event-driven; not tick-driven but must respect mutation windows.
- Public entry points: Quest state mutation/query methods.
- Dependencies: Authority contracts, player lifecycle queries.
- Determinism notes: Deterministic evaluator ordering.
- Memory notes: Uses collections; no pooling.
- Cleanup / lifecycle notes: Clears quest state on unload.
- Known risks / TODOs: None observed.

### QuestRuntimeValidationScenarios.cs
- Purpose / owns what: Validation scenarios for quest runtime behavior.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions.
- Dependencies: Quest runtime.
- Determinism notes: Ensures deterministic quest progression.
- Memory notes: Test allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### RejectClient-ProvidedIdentifiers.cs
- Purpose / owns what: Guards against client-supplied identifiers conflicting with server authority.
- Update cadence: Validation/guard checks on inbound data.
- Public entry points: Validation functions rejecting client-provided IDs.
- Dependencies: Authority contracts, onboarding/session IDs.
- Determinism notes: Deterministic rejection rules.
- Memory notes: Minimal allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### RuntimeBackpressureConfig.cs
- Purpose / owns what: Central configuration for queue caps (commands, snapshots, persistence).
- Update cadence: Static configuration used at startup.
- Public entry points: Constructor and `Default` preset.
- Dependencies: None beyond primitives.
- Determinism notes: Fixed caps ensure deterministic drop behavior.
- Memory notes: Immutable; no allocations after construction.
- Cleanup / lifecycle notes: None.
- Known risks / TODOs: None observed.

### RuntimeIntegrationZeroGcHardening.cs
- Purpose / owns what: Guidance/utilities for zero-GC runtime hardening.
- Update cadence: Doc/utility; not tick-driven.
- Public entry points: Recommendations/constants inside file.
- Dependencies: None runtime-critical.
- Determinism notes: Emphasizes allocation-free patterns.
- Memory notes: Advises pooling/reuse.
- Cleanup / lifecycle notes: None.
- Known risks / TODOs: None observed.

### RuntimeServerLoop.cs
- Purpose / owns what: Coordinates simulation, transport, handshakes, commands, visibility, and entity registry lifecycle.
- Update cadence: Start/stop/shutdown methods; not per-tick logic.
- Public entry points: `Start`, `Stop`, `ShutdownServer`, `OnSessionDisconnected`, `OnPlayerUnloaded`, `OnZoneUnloaded`, factory `Create`.
- Dependencies: `WorldSimulationCore`, transport router, handshake pipeline, command ingestor, visibility culling, entity registry.
- Determinism notes: Idempotent start/stop; deterministic cleanup order.
- Memory notes: Holds references; no per-tick allocations.
- Cleanup / lifecycle notes: Clears queues/registries on stop/shutdown; disposes pooled components.
- Known risks / TODOs: None observed.

### ServerAuthorityContracts.cs
- Purpose / owns what: Centralized authority interfaces for server-side validation and mutation rules.
- Update cadence: Interface definitions only.
- Public entry points: Authority methods exposed to systems.
- Dependencies: None (contracts only).
- Determinism notes: Defines deterministic authority boundaries.
- Memory notes: None.
- Cleanup / lifecycle notes: None.
- Known risks / TODOs: None observed.

### TickDiagnostics.cs
- Purpose / owns what: Allocation-free tick duration/overrun diagnostics with snapshots.
- Update cadence: Updated each tick by simulation systems.
- Public entry points: `RecordTick`, `Snapshot`.
- Dependencies: None external; pure diagnostics.
- Determinism notes: Fixed-size ring buffer; deterministic ordering.
- Memory notes: Preallocated arrays; no per-tick allocations.
- Cleanup / lifecycle notes: None; struct snapshots immutable.
- Known risks / TODOs: None observed.

### TickEligibilityRegistry.cs
- Purpose / owns what: Thread-safe registry of tick-eligible entities.
- Update cadence: Event-driven grant/revoke; read each tick by tick system.
- Public entry points: `TrySetTickEligible`, `IsTickEligible`, `ClearAll`.
- Dependencies: Entity handles.
- Determinism notes: Stable membership snapshot per tick via concurrent dictionary queries.
- Memory notes: Uses concurrent dictionary; no pooling; unbounded keys but cleared on shutdown.
- Cleanup / lifecycle notes: ClearAll for teardown.
- Known risks / TODOs: None observed.

### TickSystemCore.cs
- Purpose / owns what: Fixed 10 Hz tick loop invoking ordered entity participants using deterministic snapshots.
- Update cadence: Dedicated tick thread; executes fixed-step loop with catch-up/clamp.
- Public entry points: `RegisterParticipant`, `Start`, `Stop`, `IsRunning`, `Diagnostics`.
- Dependencies: `ITickEligibilityRegistry`, `IEntityRegistry`, `TickDiagnostics`.
- Determinism notes: Sorts participants by order key/registration sequence; snapshots entities before tick; forbids mid-tick eligibility mutation via snapshot isolation.
- Memory notes: Reuses snapshots; no per-tick allocations beyond snapshots; uses lock/arrays not pooled.
- Cleanup / lifecycle notes: Stop/Dispose clear thread/CTS; idempotent start/stop.
- Known risks / TODOs: None observed.

### TimeSlicedWorkScheduler.cs
- Purpose / owns what: Executes work items in time-sliced budgets for post-tick tasks (e.g., replication).
- Update cadence: Called from tick thread with budget parameters.
- Public entry points: `Enqueue`, `ExecuteSlices`.
- Dependencies: Diagnostics for elapsed measurement.
- Determinism notes: Processes queue order deterministically; no mid-slice reordering.
- Memory notes: Uses queue/list; no pooling; avoids allocations during execution.
- Cleanup / lifecycle notes: Clears queue after execution.
- Known risks / TODOs: None observed.

### Validation* (multiple files)
- Purpose / owns what: Validation harness infrastructure (`ValidationHarness_*`, `ValidationScenario*`, `ValidationSharedContracts`, `ValidationAssert`, `ValidationDiff_Utilities`, `ValidationSnapshot_*`).
- Update cadence: Test harness only; not runtime tick-driven.
- Public entry points: Scenario registration/execution utilities, snapshot capture for tests.
- Dependencies: Various runtime systems (inventory, NPC, quests, world simulation) for assertions.
- Determinism notes: Focus on deterministic comparisons and invariant checks.
- Memory notes: Test allocations acceptable.
- Cleanup / lifecycle notes: Scenario-scoped.
- Known risks / TODOs: None observed.

### WorldBootstrapRegistration.cs
- Purpose / owns what: Applies deterministic registration of eligibility gates, participants, and phase hooks to `WorldSimulationCore` before start.
- Update cadence: One-time during startup.
- Public entry points: `Apply`.
- Dependencies: World simulation core; registration arrays.
- Determinism notes: Preserves explicit ordering via provided order keys.
- Memory notes: No pooling; simple iteration.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### WorldSimulationCore.cs
- Purpose / owns what: Deterministic simulation core with pre-tick eligibility, simulation execution, and post-tick hooks at fixed 10 Hz.
- Update cadence: Dedicated simulation thread or single-tick execution for harness.
- Public entry points: `RegisterEligibilityGate`, `RegisterParticipant`, `RegisterPhaseHook`, `Start`, `Stop`, `ExecuteSingleTick`, `Diagnostics`.
- Dependencies: `ISimulationEntityIndex`, eligibility gates, participants, phase hooks, effect buffer.
- Determinism notes: Fixed ordering (order key then registration seq); eligibility snapshot enforced stable (throws on mid-tick mutation); effect buffering commits post-tick; catch-up clamped.
- Memory notes: Reuses pooled arrays/lists for eligibility snapshots; no per-tick allocations when stable; effect buffer reuses list.
- Cleanup / lifecycle notes: Stop/Dispose halt thread and dispose CTS; internal buffers cleared on reset.
- Known risks / TODOs: None observed.

### WorldSimulationCoreValidationScenarios.cs
- Purpose / owns what: Validation scenarios for simulation core tick ordering and eligibility invariants.
- Update cadence: Test-driven.
- Public entry points: Scenario definitions and harness hooks.
- Dependencies: Tick/simulation core contracts.
- Determinism notes: Asserts no mid-tick mutation and ordering.
- Memory notes: Test allocations.
- Cleanup / lifecycle notes: None observed.
- Known risks / TODOs: None observed.

### ZoneSpatialIndex.cs
- Purpose / owns what: Spatial index for zones supporting AOI/visibility queries with pooled buffers.
- Update cadence: Event-driven on entity movement/residency updates; queried during replication/AI.
- Public entry points: Registration, update, query methods (`QueryNeighbors` etc.).
- Dependencies: Zone IDs, entity handles, positions; uses deterministic ordering via comparer.
- Determinism notes: Stable sorting of results; no mid-tick mutation assumptions; deterministic AOI outputs.
- Memory notes: Uses pooled arrays/lists to avoid per-query allocation; reuse buffers; clears on removal/clear.
- Cleanup / lifecycle notes: Supports zone removal and full clear; disposes pools on clear.
- Known risks / TODOs: None observed.

Interaction Diagrams (Text)
---------------------------
- Inbound command ingestion → freeze → intent resolution → commit:
  - Transport thread decodes → `AuthoritativeCommandIngress.TryEnqueue` (bounded) → tick thread dequeues per session at tick start → intents resolved (e.g., combat resolver) → effects buffered → post-tick commit via effect buffer/application system.
- Committed state → AOI gate → snapshot build → transport send:
  - Post-tick state stable → replication gate filters entities per session → `ClientReplicationSnapshotSystem` captures/sorts snapshots → `BoundedReplicationSnapshotQueue` serializes/deltas → transport thread dequeues serialized snapshots → sends to client.
- Persistence request queue → I/O → apply-on-tick:
  - Runtime system enqueues `PersistenceWriteRequest` into `PersistenceWriteQueue` (caps/drop oldest) → persistence worker (off-thread) performs I/O → completion enqueued to apply-on-tick queue (not implemented) → tick thread drains completions during mutation window and applies state.
