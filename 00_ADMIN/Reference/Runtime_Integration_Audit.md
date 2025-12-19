# Runtime Integration Audit — Repeat-Issues Closure Audit

## 1) Executive Summary
- **System Code Complete: NO**
- **Justification:** The runtime now boots end-to-end via `HeadlessServerEntryPoint`, but the runtime entrypoint registers only `NoOpCommandHandler`; no concrete handler that mutates authoritative state is wired in the runtime composition (Failure Mode 5 = P0).
- **Closure Scorecard (1–12):**
  1) No runtime entrypoint starts the host (non-validation) — **CLOSED**
  2) RuntimeCompositionRoot missing or not used by entrypoint — **CLOSED**
  3) Systems exist but aren’t pumped (no callers) — **CLOSED**
  4) Islands not pipelines (missing bridges between layers) — **PARTIAL**
  5) Frozen authoritative commands have no runtime consumer — **OPEN (P0)**
  6) Client trust boundary violation (client tick/id influences authority) — **CLOSED**
  7) Thread ownership assumed not enforced — **PARTIAL**
  8) Disconnect/shutdown leaks — **CLOSED**
  9) Hot-path allocations after warm-up (lists/dicts/closures/LINQ/strings) — **PARTIAL**
  10) Backpressure allocates under pressure (rebuild queues, allocs on trim/drop) — **PARTIAL**
  11) Replication drift (no runtime session index, outbound not drained, string fingerprints) — **CLOSED**
  12) Combat drift (string IDs in hot loops, dynamic payloads, deep-freeze allocs) — **OPEN**

## 2) Runtime Orchestration Proof (NEW – must be very explicit)

### 2.1 EntryPoint proof (non-validation)
- **Entrypoint:** `CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs` → `HeadlessServerEntryPoint.Main`.
- **Call chain (explicit):**
  1) `HeadlessServerEntryPoint.Main` → `RuntimeCompositionRoot.CreateHost(settings)` (`RuntimeHost/HeadlessServerEntryPoint.cs`, `RuntimeHost/RuntimeCompositionRoot.cs`).
  2) `HeadlessServerEntryPoint.Main` → `host.Start()` (`RuntimeHost/HeadlessServerEntryPoint.cs`).
  3) `ServerRuntimeHost.Start` → `_runtimeLoop.Start()` (`RuntimeHost/ServerRuntimeHost.cs`).
  4) `RuntimeServerLoop.Start` → `_simulation.Start()` + `_outboundPump.Start()` + `_persistenceWorker?.Start()` (`RuntimeServerLoop.cs`).

### 2.2 CompositionRoot proof
- **Composition root:** `CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs` → `RuntimeCompositionRoot.Create`.
- **Constructs (explicit list):**
  - Tick core: `WorldSimulationCore` (`RuntimeCompositionRoot.Create` → `new WorldSimulationCore(...)`).
  - Inbound pipeline: `PooledTransportRouter`, `AuthoritativeCommandIngestor`, `InboundPumpTickHook`.
  - Command consumer: `AuthoritativeCommandConsumeTickHook` + `CommandHandlerRegistry`.
  - Session index: `DeterministicActiveSessionIndex` (or `settings.ActiveSessions`).
  - Replication: `ClientReplicationSnapshotSystem` + `TimeSlicedWorkScheduler` + `SnapshotEligibilityRegistry`.
  - Outbound pump: `OutboundSendPump`.
  - Persistence: `PersistenceWriteQueue`, `PersistenceCompletionQueue`, `PersistenceWorkerLoop`, `PersistenceCompletionPhaseHook`, `PersistenceApplyState` (only when `settings.Persistence.Writer` is present).
- **Registration sites (phase order & wiring):**
  - `RuntimeCompositionRoot.Create` constructs `combinedHooks` and calls `WorldBootstrapRegistration.Apply(simulation, gates, participants, combinedHooks)` (`RuntimeCompositionRoot.cs`, `WorldBootstrapRegistration.cs`).
  - Order keys are set from `RuntimeCompositionSettings`:
    - Lifecycle mailbox: `LifecycleHookOrderKey` (default `int.MinValue`)
    - Inbound pump / freeze: `CommandFreezeHookOrderKey` (default `int.MinValue`)
    - Command consume: `CommandConsumeHookOrderKey` (default `int.MinValue + 1`)
    - Handshake: `HandshakeProcessingHookOrderKey` (default `int.MinValue + 2`)
    - Persistence completion: `PersistenceCompletionHookOrderKey` (default `-1024`, optional)
    - Replication: `ReplicationHookOrderKey` (default `int.MaxValue - 512`)
- **Fail-fast wiring gate (call site + checks):**
  - `ServerRuntimeHost.Start` → `ValidateRequiredHooks()` checks inbound pump, command consume hook, freeze hook or inbound pump, lifecycle hook, replication hook, outbound pump, and persistence completion hook if persistence enabled (`RuntimeHost/ServerRuntimeHost.cs`).
  - `RuntimeServerLoop.Start` → `ValidatePipelineWiring()` checks inbound pump, command consume hook, handshake hook, lifecycle hook, replication hook, outbound pump, and persistence hook + worker when enabled (`RuntimeServerLoop.cs`).

### 2.3 Host lifecycle proof
- **Start:** `ServerRuntimeHost.Start` (lock-gated) → `RuntimeServerLoop.Start` →
  - `_persistenceWorker?.Start()` (`PersistenceWorkerLoop.Start`, starts `Caelmor.PersistenceWorker` thread).
  - `_simulation.Start()` (`WorldSimulationCore.Start`, starts `Caelmor.WorldSimulationCore` tick thread).
  - `_outboundPump.Start()` (`OutboundSendPump.Start`, starts `Caelmor.OutboundSendPump` thread).
- **Stop:** `ServerRuntimeHost.Stop` → `RuntimeServerLoop.Stop` → `_persistenceWorker?.Stop()` + `_outboundPump.Stop()` + `_simulation.Stop()` (`RuntimeServerLoop.cs`).
- **No `Thread.Abort`:** All thread shutdowns use `CancellationTokenSource.Cancel()` + `Thread.Join()` in `WorldSimulationCore.Stop`, `OutboundSendPump.Stop`, and `PersistenceWorkerLoop.Stop`.

## 3) Authoritative Tick & Phase Wiring

### 3.1 Identify authoritative tick driver
- **Tick driver:** `CODE/Systems/WorldSimulationCore.cs` → `WorldSimulationCore.RunLoop` / `ExecuteOneTick`.
- **Start chain:** `HeadlessServerEntryPoint.Main` → `ServerRuntimeHost.Start` → `RuntimeServerLoop.Start` → `WorldSimulationCore.Start` → `RunLoop`.
- **Tick rate enforcement:** `WorldSimulationCore.TickRateHz = 10` and `TickInterval = 100ms` (`WorldSimulationCore`).
- **Overrun handling:** `MaxCatchUpTicksPerLoop = 3` with deterministic clamp when behind; recorded via `TickDiagnostics.RecordTick(..., catchUpClamped: true)` (`WorldSimulationCore.RunLoop`).
- **No tick-thread blocking I/O found:** Blocking search terms (`File.`, `Stream`, `ReadAll`, `WriteAll`) returned no hits in tick-thread code; only cadence sleeps (`Thread.Sleep`) appear in the tick loop.

### 3.2 Tick hook list (phase order)
> All hooks execute on the authoritative tick thread via `WorldSimulationCore.ExecuteOneTick`.

1) **LifecycleMailboxPhaseHook**
   - **File/type/method:** `CODE/Systems/RuntimeServerLoop.cs` → `LifecycleMailboxPhaseHook.OnPreTick`.
   - **Phase:** Pre-Tick.
   - **Thread:** Tick thread (enforced by `TickThreadMailbox.Drain` → `TickThreadAssert.AssertTickThread`).
   - **Proof-of-life counters:** `TickThreadMailbox.LifecycleOpsApplied` / `DisconnectsApplied` (`LifecycleTickMailbox.cs`).
   - **Fail condition if missing:** `RuntimeServerLoop.ValidatePipelineWiring` and `ServerRuntimeHost.ValidateRequiredHooks` throw `RUNTIME_PIPELINE_MISSING_HOOKS`.

2) **InboundPumpTickHook (freeze + drain)**
   - **File/type/method:** `CODE/Systems/RuntimeIntegrationZeroGcHardening.cs` → `InboundPumpTickHook.OnPreTick`.
   - **Phase:** Pre-Tick.
   - **Thread:** Tick thread (enforced by `RuntimeGuardrailChecks.AssertTickThreadEntry`).
   - **Proof-of-life counters:** `InboundPumpDiagnostics.InboundPumpTicksExecuted`, `CommandsEnqueuedToIngestor`.
   - **Fail condition if missing:** `RuntimeServerLoop.ValidatePipelineWiring` / `ServerRuntimeHost.ValidateRequiredHooks`.

3) **AuthoritativeCommandConsumeTickHook**
   - **File/type/method:** `CODE/Systems/RuntimeIntegrationZeroGcHardening.cs` → `AuthoritativeCommandConsumeTickHook.OnPreTick`.
   - **Phase:** Pre-Tick.
   - **Thread:** Tick thread (enforced by `RuntimeGuardrailChecks.AssertTickThreadEntry`).
   - **Proof-of-life counters:** `CommandConsumeDiagnostics.FrozenBatchesConsumed`, `CommandsDispatched`.
   - **Fail condition if missing:** `RuntimeServerLoop.ValidatePipelineWiring` / `ServerRuntimeHost.ValidateRequiredHooks`.

4) **HandshakeProcessingPhaseHook**
   - **File/type/method:** `CODE/Systems/SessionHandshakePipeline.cs` → `HandshakeProcessingPhaseHook.OnPreTick`.
   - **Phase:** Pre-Tick.
   - **Thread:** Tick thread (`TickThreadAssert.AssertTickThread`).
   - **Proof-of-life counters:** `HandshakePipelineMetrics.Processed` / `DeferredTicks`.
   - **Fail condition if missing:** `RuntimeServerLoop.ValidatePipelineWiring` when handshakes enabled.

5) **Custom phase hooks (settings.PhaseHooks)**
   - **Registration:** `RuntimeCompositionRoot.Create` → `combinedHooks` → `WorldBootstrapRegistration.Apply`.
   - **Phase order:** As provided by `settings.PhaseHooks[i].OrderKey`.
   - **Proof-of-life:** **UNKNOWN** in runtime entrypoint; `HeadlessServerEntryPoint` provides none.
   - **Fail condition if missing:** N/A (optional hooks).

6) **PersistenceCompletionPhaseHook (optional)**
   - **File/type/method:** `CODE/Systems/PersistenceCompletionQueue.cs` → `PersistenceCompletionPhaseHook.OnPreTick`.
   - **Phase:** Pre-Tick.
   - **Thread:** Tick thread (`TickThreadAssert.AssertTickThread`).
   - **Proof-of-life counters:** `PersistencePipelineCounters.CompletionsApplied`, `CompletionQueueMetrics`.
   - **Fail condition if missing:** `RuntimeServerLoop.ValidatePipelineWiring` + `ServerRuntimeHost.ValidateRequiredHooks` when persistence enabled.

7) **ClientReplicationSnapshotSystem**
   - **File/type/method:** `CODE/Systems/ClientReplicationSnapshotSystem.cs` → `OnPreTick` / `OnPostTick`.
   - **Phase:** Pre-Tick (guard) + Post-Tick (snapshot build).
   - **Thread:** Tick thread (enforced by `RuntimeGuardrailChecks.AssertTickThreadEntry`).
   - **Proof-of-life counters:** `ReplicationSnapshotCounters.RecordSnapshotBuilt/Serialized/Enqueued` (`ReplicationSnapshotCounters.cs`).
   - **Fail condition if missing:** `RuntimeServerLoop.ValidatePipelineWiring` / `ServerRuntimeHost.ValidateRequiredHooks`.

## 4) End-to-End Pipeline Proofs (must include function-level call chains)

### 4.1 Inbound pipeline proof (transport → ingest → freeze → consume → mutate)
**Call chain:**
1) **Inbound enters server ownership:**
   - `PooledTransportRouter.EnqueueInbound` (public API) stamps `ServerStampedInboundCommand` with `serverReceiveTick` and `serverReceiveSeq` and enqueues it (`PooledTransportRouter.cs`).
2) **Inbound pump tick hook:**
   - `InboundPumpTickHook.OnPreTick` (`RuntimeIntegrationZeroGcHardening.cs`) is registered via `RuntimeCompositionRoot.Create` → `WorldBootstrapRegistration.Apply`.
3) **RouteQueuedInbound call site:**
   - `InboundPumpTickHook.OnPreTick` → `_transport.RouteQueuedInbound(context.TickIndex, ...)` (`PooledTransportRouter.RouteQueuedInbound`).
4) **Ingress → ingestor bridge:**
   - `PooledTransportRouter.RouteQueuedInbound` → `_deterministic.RouteInbound` → `AuthoritativeCommandIngress.TryEnqueue` (`DeterministicTransportQueues.cs`).
5) **Freeze call site (per tick):**
   - `InboundPumpTickHook.OnPreTick` → `FreezeCommands` → `_ingestor.FreezeSessions/FreezeAllSessions` (`RuntimeIntegrationZeroGcHardening.cs`).
6) **Consume call site:**
   - `AuthoritativeCommandConsumeTickHook.OnPreTick` → `_ingestor.GetFrozenBatch(sessionId)` (`RuntimeIntegrationZeroGcHardening.cs`).
7) **Dispatch call site:**
   - `AuthoritativeCommandConsumeTickHook.OnPreTick` → `_registry.TryGetHandler` → `handler.Handle(...)` (`RuntimeIntegrationZeroGcHardening.cs`).
8) **Concrete handler that mutates authoritative runtime state:**
   - **Missing in runtime entrypoint.** `HeadlessServerEntryPoint.RegisterNoOpCommandHandlers` registers only `NoOpCommandHandler` (no mutation). A mutating handler exists (`SessionCommandCounterHandler`), but it is wired only in the proof harness (`RuntimeHost/InProcTransportProofHarness.cs`).

**Status:** **OPEN (P0)** — runtime entrypoint lacks a mutating handler; end-to-end authoritative mutation is not proven.

### 4.2 Outbound pipeline proof (active sessions → snapshots → serialize → queue → send pump)
**Call chain:**
1) **Session index implementation + injection:**
   - `DeterministicActiveSessionIndex` implements `IActiveSessionIndex` (`DeterministicActiveSessionIndex.cs`).
   - Injected in runtime entrypoint: `HeadlessServerEntryPoint.TryBuildSettings` → `settings.ActiveSessions = activeSessions` → `RuntimeCompositionRoot.Create` uses `settings.ActiveSessions` (`RuntimeHost/HeadlessServerEntryPoint.cs`, `RuntimeHost/RuntimeCompositionRoot.cs`).
2) **Snapshot build hook:**
   - `WorldSimulationCore.ExecuteOneTick` → `ITickPhaseHook.OnPostTick` → `ClientReplicationSnapshotSystem.OnPostTick` (`WorldSimulationCore.cs`, `ClientReplicationSnapshotSystem.cs`).
3) **Serialize call site:**
   - `ClientReplicationSnapshotSystem.SnapshotWorkItem.BuildSnapshot` → `_queue.Enqueue` → `BoundedReplicationSnapshotQueue.Enqueue` → `SnapshotDeltaSerializer.Serialize` → `SerializedSnapshot.Rent` (`ClientReplicationSnapshotSystem.cs`, `DeterministicTransportQueues.cs`).
4) **Outbound queue enqueue + caps/metrics:**
   - `BoundedReplicationSnapshotQueue.Enqueue` → `EnforceCaps` enforces `MaxOutboundSnapshotsPerSession` + `MaxQueuedBytesPerSession` and records metrics (`DeterministicTransportQueues.cs`).
5) **Outbound send pump drain:**
   - `RuntimeServerLoop.Start` → `_outboundPump.Start()` → `OutboundSendPump.Run` → `PumpOnce` → `_transport.TryDequeueOutbound` → `DeterministicTransportRouter.TryDequeueSnapshot` → `BoundedReplicationSnapshotQueue.TryDequeue` → `_sender.TrySend` (`OutboundSendPump.cs`, `DeterministicTransportQueues.cs`).

**Status:** **CLOSED** — runtime session index is wired and outbound pump drains.

### 4.3 Persistence pipeline proof (enqueue → worker drain → completion → apply-on-tick)
**Call chain:**
1) **Enqueue write call site (tick thread):** **UNKNOWN** — no runtime call site enqueues `PersistenceWriteQueue.Enqueue(...)` found in repository (search in `CODE/Systems`).
2) **Persistence worker thread start/drain:**
   - `RuntimeServerLoop.Start` → `_persistenceWorker.Start()` → `PersistenceWorkerLoop.Run` → `PumpOnce` → `_writeQueue.TryDequeue` → `_writer.Execute` (`RuntimeServerLoop.cs`, `PersistenceWorkerLoop.cs`).
3) **Completion enqueue:**
   - `PersistenceWorkerLoop.PumpOnce` → `_completionQueue.TryEnqueue` (`PersistenceCompletionQueue.cs`).
4) **Apply-on-tick hook:**
   - `PersistenceCompletionPhaseHook.OnPreTick` → `_queue.Drain(_applier, tickIndex)` (`PersistenceCompletionQueue.cs`).

**Status:** **PARTIAL** — worker + completion apply exist, but enqueue call site is unproven in runtime composition.

## 5) Trust Boundary Audit
- **Server stamping site (receive tick + seq):** `PooledTransportRouter.EnqueueInbound` sets `ServerReceiveSeq` from `_receiveSeqBySession` and `ServerReceiveTick` from `_currentReceiveTick` (`PooledTransportRouter.cs`).
- **Ordering source (server-only):** `AuthoritativeCommandIngress.DrainDeterministic` orders by `ServerReceiveTick` then `ServerReceiveSeq` (`DeterministicTransportQueues.cs`).
- **Client tick rejection (counters):** `InboundPumpTickHook.OnPreTick` rejects any `ClientSubmitTick > 0` and increments `_rejectedClientTickProvided` (`RuntimeIntegrationZeroGcHardening.cs`).
- **Client identifier rejection:** `PlayerSessionSystem.ActivateSession` calls `ClientIdentifierRejectionGuards.RejectIfClientProvidedIdentifiersPresent` (`PlayerSessionSystem.cs`, `RejectClient-ProvidedIdentifiers.cs`).

**Conclusion:** Client-provided tick/identifiers are rejected; server-stamped tick/seq is the only ordering source.

## 6) Thread Ownership Enforcement Audit
**Legend:** Tick-thread-only = explicit `TickThreadAssert`/`RuntimeGuardrailChecks` enforcement; Locked = lock-based; Mailbox = tick-thread marshaling.

- **Session index:** `DeterministicActiveSessionIndex` uses internal lock (`DeterministicActiveSessionIndex.cs`); mutations invoked via `ActiveSessionIndexedPlayerSessionSystem` (tick-thread through handshake hook).
- **Visibility/AOI:** `VisibilityCullingService.Track/Remove/RefreshVisibility/RemoveSession/Clear` assert tick thread (`RuntimeIntegrationZeroGcHardening.cs`).
- **Replication work contexts:** `ClientReplicationSnapshotSystem.OnPreTick/OnPostTick` assert tick thread; work items are executed via tick-thread `TimeSlicedWorkScheduler` (no off-thread mutation) (`ClientReplicationSnapshotSystem.cs`, `TimeSlicedWorkScheduler.cs`).
- **Ingestor/session command state:** `AuthoritativeCommandIngestor` uses `_gate` lock; tick thread enforced at drain/consume via `InboundPumpTickHook` and `AuthoritativeCommandConsumeTickHook` (`RuntimeIntegrationZeroGcHardening.cs`).
- **Outbound queues:** `PooledTransportRouter.RouteSnapshot` asserts tick thread; `TryDequeueOutbound` guarded by `_snapshotGate` lock (`PooledTransportRouter.cs`).
- **Persistence queues/completions:** `PersistenceWriteQueue.Enqueue` locked; `PersistenceCompletionQueue.Drain` asserts tick thread (`DeterministicTransportQueues.cs`, `PersistenceCompletionQueue.cs`).
- **Gaps (PARTIAL):** `CombatOutcomeApplicationSystem.Apply` mutates dictionaries and emits events without `TickThreadAssert` or locks; `CombatIntentQueueSystem.SubmitIntent` relies on `RuntimeGuardrailChecks.AssertTickThreadEntry` (DEBUG-only) (`CombatOutcomeApplicationSystem.cs`, `CombatIntentQueueSystem.cs`).

## 7) Disconnect / Shutdown Leak Audit
**Disconnect call chain:**
- `RuntimeServerLoop.OnSessionDisconnected` → `TickThreadMailbox.TryEnqueueDisconnect/Unregister/ClearVisibility/CleanupReplication` → `LifecycleMailboxPhaseHook.OnPreTick` → `TickThreadMailbox.Drain` → `LifecycleApplier.Apply` →
  - `_transport.DropAllForSession` (drops inbound/outbound mailboxes, disposes payloads) (`PooledTransportRouter.cs`).
  - `_commands.DropSession` (returns pooled command buffers) (`RuntimeIntegrationZeroGcHardening.cs`).
  - `_handshakes.Drop` (clears pending handshakes) (`SessionHandshakePipeline.cs`).
  - `_visibility.RemoveSession` (returns pooled entity buffers) (`RuntimeIntegrationZeroGcHardening.cs`).
  - `_replication.OnSessionDisconnected` (marks work contexts for removal) (`ClientReplicationSnapshotSystem.cs`).

**Shutdown call chain:**
- `RuntimeServerLoop.ShutdownServer` → `Stop()` → `_persistenceWorker.Stop()` + `_outboundPump.Stop()` + `_simulation.Stop()` → `ClearTransientState()` → `_transport.Clear` + `_handshakes.Reset` + `_commands.Clear` + `_visibility.Clear` + `_entities.ClearAll` + `_lifecycleMailbox.Clear` + `_persistenceCompletions.Clear` + `_persistenceWrites.Clear` (`RuntimeServerLoop.cs`).

**Pooled buffer ownership:**
- `PooledPayloadLease.Dispose`, `SerializedSnapshot.Dispose`, `PersistenceCompletion.Dispose` return pooled buffers deterministically (`DeterministicTransportQueues.cs`, `PersistenceCompletionQueue.cs`).

**Status:** **CLOSED** — deterministic cleanup exists for disconnect and shutdown paths.

## 8) Hot-Path Allocation Audit (after warm-up)
> Classifications reflect tick-thread and worker-thread hot paths. “UNKNOWN” means no runtime proof was found.

- **Tick + hooks:** **SOME**
  - `WorldSimulationCore.EnsureCapacity` can allocate when participant/eligibility/phase-hook/entity counts grow (`WorldSimulationCore.cs`).
- **Inbound decode/routing/bridge/freeze/consume:** **SOME**
  - New session paths allocate command rings and per-session dictionaries (`AuthoritativeCommandIngestor.TryEnqueue`, `AuthoritativeCommandIngress.TryEnqueue`) (`RuntimeIntegrationZeroGcHardening.cs`, `DeterministicTransportQueues.cs`).
  - `_sessionOrder` list can grow when session count exceeds capacity (`PooledTransportRouter.RouteQueuedInbound`).
- **Handshake:** **NONE**
  - Fixed-size ring buffers allocated at construction; no per-tick allocations (`SessionHandshakePipeline.cs`).
- **Replication build/serialize/AOI:** **SOME**
  - `SnapshotWorkContext` rents arrays per session on first use; `SnapshotDeltaSerializer` `List<>`/`HashSet<>` can grow with entity counts (`ClientReplicationSnapshotSystem.cs`, `DeterministicTransportQueues.cs`).
- **Persistence trim/drop + worker + apply-on-tick:** **SOME**
  - `PersistenceWriteQueue` per-player queue creation allocates on first use; `PersistenceApplyState` dictionary grows with new saves (`DeterministicTransportQueues.cs`, `PersistenceWorkerLoop.cs`).
- **Combat staging/resolve/apply:** **SOME**
  - `CombatOutcomeApplicationSystem` creates `HashSet<string>` per tick for idempotence and string payload IDs (`CombatOutcomeApplicationSystem.cs`).
  - `CombatIntentQueueSystem` allocates new staging buckets/snapshots when pools are exhausted and uses string identifiers in submissions (`CombatIntentQueueSystem.cs`).

**Explicit hot-path allocation sites (non-exhaustive):**
- `WorldSimulationCore.EnsureCapacity` (tick-thread array growth).
- `AuthoritativeCommandIngestor.TryEnqueue` / `AuthoritativeCommandIngress.TryEnqueue` (new per-session state).
- `ClientReplicationSnapshotSystem.GetOrCreateContext` (new `SnapshotWorkContext`); `SnapshotDeltaSerializer` list/HashSet growth.
- `CombatOutcomeApplicationSystem.GetOrCreateAppliedSetForTick` / `EnsureNoDuplicateIdsInBatchOrThrow` (per-tick `HashSet<string>` allocations).
- `CombatIntentQueueSystem.SubmitIntent` (new `StagingBucket` / `FrozenQueueSnapshot` on pool exhaustion).

## 9) Backpressure Under Pressure Audit
**Queues/mailboxes and caps:**
- **Inbound transport queues:** `PooledTransportRouter` enforces `MaxInboundCommandsPerSession` + `MaxQueuedBytesPerSession`; overflow rejects newest and disposes payload (`PooledTransportRouter.EnqueueInbound`). Metrics tracked in `SessionQueueMetrics` and `TransportBackpressureDiagnostics`.
- **Deterministic ingress:** `AuthoritativeCommandIngress` enforces per-session count/bytes; overflow rejects and disposes (`DeterministicTransportQueues.cs`).
- **Command ingestion ring:** `AuthoritativeCommandIngestor` uses fixed ring with drop-newest overflow policy (`RuntimeIntegrationZeroGcHardening.cs`).
- **Handshake queue:** Fixed ring; overflow rejects with `HandshakeRejectionReason.QueueFull` (`SessionHandshakePipeline.cs`).
- **Replication snapshot queue:** `BoundedReplicationSnapshotQueue` enforces `MaxOutboundSnapshotsPerSession` + `MaxQueuedBytesPerSession`; overflow drops oldest and disposes buffers (`DeterministicTransportQueues.cs`).
- **Outbound send pump:** bounded per-iteration via `_maxPerSession` / `_maxPerIteration` (`OutboundSendPump.cs`).
- **Persistence write queue:** per-player + global caps with drop-oldest; no queue rebuild (`PersistenceWriteQueue.EnforceCaps/EnforceGlobalCap`).
- **Persistence completion queue:** caps by count + bytes, drop-oldest with payload disposal (`PersistenceCompletionQueue.cs`).
- **Lifecycle mailbox:** caps by count + bytes, drop-oldest, no allocation (`LifecycleTickMailbox.cs`).
- **Combat intent staging:** fixed caps per actor + per session; overflow uses `IntentRejection` allocations in drop path (`CombatIntentQueueSystem.cs`).

**Status:** **PARTIAL** — core runtime queues are bounded and drop deterministically without allocations, but combat overflow emits new `IntentRejection` objects on drop (alloc under pressure).

## 10) Replication Drift Closure Audit
- **Runtime session index exists and is used:** `DeterministicActiveSessionIndex` is injected in `HeadlessServerEntryPoint.TryBuildSettings` → `RuntimeCompositionRoot.Create` → `ClientReplicationSnapshotSystem` / `OutboundSendPump` (`DeterministicActiveSessionIndex.cs`, `RuntimeHost/HeadlessServerEntryPoint.cs`, `RuntimeHost/RuntimeCompositionRoot.cs`).
- **Outbound drained:** `OutboundSendPump.Run` continuously drains snapshots via `TryDequeueOutbound` (`OutboundSendPump.cs`).
- **Fingerprints:** `SnapshotDeltaSerializer` uses `Dictionary<EntityHandle, ulong>` for baselines (no string churn) (`DeterministicTransportQueues.cs`).
- **Pooled buffer ownership:** `SerializedSnapshot.Dispose` returns pooled byte[]; drop paths dispose (`DeterministicTransportQueues.cs`).

**Status:** **CLOSED**.

## 11) Combat Drift Closure Audit
- **String entity IDs in hot loops:** `CombatOutcomeApplicationSystem` builds string payload IDs (`PayloadId.*`) and uses `HashSet<string>` per tick; `CombatIntentQueueSystem` stores string intent IDs and validates string IDs in payloads (`CombatOutcomeApplicationSystem.cs`, `CombatIntentQueueSystem.cs`).
- **Dynamic payload dictionaries:** `CombatOutcomeApplicationSystem` uses `Dictionary<int, HashSet<string>>` for idempotence per tick (`CombatOutcomeApplicationSystem.cs`).
- **Deep-freeze allocations per intent:** `CombatIntentQueueSystem` allocates staging buckets and snapshots when pools are exhausted; string payloads are carried through frozen records (`CombatIntentQueueSystem.cs`).
- **Caps/metrics:** Combat intent queue has caps (`ActorIntentCapPerTick`, `SessionIntentCapPerTick`) but no explicit byte caps; idempotence map has no explicit cap beyond pruning window (`CombatOutcomeApplicationSystem.cs`).

**Status:** **OPEN**.

## 12) Risk Register (recurring-issue related only)
- **P0 — Missing mutating command handler in runtime entrypoint (Failure Mode 5)**
  - **File/Method:** `RuntimeHost/HeadlessServerEntryPoint.cs` → `RegisterNoOpCommandHandlers`.
  - **Why it violates MMO guardrail:** Frozen commands are consumed but no authoritative mutation handler is wired in the runtime entrypoint; `NoOpCommandHandler` does not mutate authoritative state.
  - **Minimal fix strategy (audit-only):** Register a real `IAuthoritativeCommandHandler` (e.g., `SessionCommandCounterHandler`) in `HeadlessServerEntryPoint.TryBuildSettings` or via `RuntimeCompositionSettings.ConfigureCommandHandlers`.

- **P1 — Persistence enqueue entry not proven (Failure Mode 4)**
  - **File/Method:** **UNKNOWN** (no `PersistenceWriteQueue.Enqueue` call site found in runtime code).
  - **Why it violates MMO guardrail:** Persistence worker + completion apply exist, but there is no proven enqueue bridge; pipeline start is unverified.
  - **Minimal fix strategy (audit-only):** Wire persistence enqueue calls from authoritative systems to `PersistenceWriteQueue.Enqueue` on tick thread.

- **P1 — Thread ownership enforcement incomplete for combat (Failure Mode 7)**
  - **File/Method:** `CombatOutcomeApplicationSystem.Apply` (no `TickThreadAssert` or lock).
  - **Why it violates MMO guardrail:** Tick-thread ownership is assumed but not enforced; potential cross-thread mutation risk.
  - **Minimal fix strategy (audit-only):** Add explicit tick-thread asserts or marshal via a tick-thread mailbox.

- **P1 — Combat drift (Failure Mode 12)**
  - **File/Method:** `CombatOutcomeApplicationSystem.GetOrCreateAppliedSetForTick`, `PayloadId.*`, `CombatIntentQueueSystem`.
  - **Why it violates MMO guardrail:** String IDs and per-tick `HashSet<string>` allocations in combat hot loops; idempotence cache lacks byte caps.
  - **Minimal fix strategy (audit-only):** Replace string IDs with fixed-size numeric IDs and cap idempotence caches with pooled structures.

- **P2 — Hot-path allocations after warm-up (Failure Mode 9)**
  - **File/Method:** `WorldSimulationCore.EnsureCapacity`, `AuthoritativeCommandIngestor.TryEnqueue`, `SnapshotDeltaSerializer.Serialize`.
  - **Why it violates MMO guardrail:** Allocation spikes occur when counts exceed prior maxima.
  - **Minimal fix strategy (audit-only):** Prewarm arrays/lists to expected maxima; expand pool capacities.

---

## APPENDIX A — Evidence Table (MANDATORY)
| Severity | Failure mode # | Subsystem | File | Type/Method | Finding | Evidence summary |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | 5 | Authoritative commands | CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs | RegisterNoOpCommandHandlers | Runtime entrypoint wires only `NoOpCommandHandler` (no mutation). | `HeadlessServerEntryPoint.TryBuildSettings` sets `ConfigureCommandHandlers = RegisterNoOpCommandHandlers`; no mutating handler registered. |
| P1 | 4 | Persistence | CODE/Systems/DeterministicTransportQueues.cs | PersistenceWriteQueue.Enqueue | Persistence enqueue entry point not found in runtime wiring. | `rg` search shows no runtime call sites for `PersistenceWriteQueue.Enqueue`; only construction in composition root. |
| P1 | 7 | Combat thread ownership | CODE/Systems/CombatOutcomeApplicationSystem.cs | Apply | Tick-thread ownership not enforced in combat apply path. | `Apply` mutates dictionaries and emits events without `TickThreadAssert` or locks. |
| P1 | 10 | Combat backpressure | CODE/Systems/CombatIntentQueueSystem.cs | RejectOverflow | Drop path allocates new `IntentRejection` objects under pressure. | Overflow path allocates `IntentRejection` and string IDs before dispatching to rejection sink. |
| P1 | 12 | Combat drift | CODE/Systems/CombatOutcomeApplicationSystem.cs | GetOrCreateAppliedSetForTick / PayloadId.* | String IDs + per-tick `HashSet<string>` in hot loops. | `GetOrCreateAppliedSetForTick` allocates `HashSet<string>` per tick; `PayloadId.*` uses string interpolation. |
| P2 | 9 | Tick core | CODE/Systems/WorldSimulationCore.cs | EnsureCapacity | Tick-thread array growth when counts exceed prior maxima. | `EnsureCapacity` reallocates participant/hook/gate/eligible arrays during `ExecuteOneTick`. |
| P2 | 9 | Inbound ingestion | CODE/Systems/RuntimeIntegrationZeroGcHardening.cs | AuthoritativeCommandIngestor.TryEnqueue | New session rings allocate in tick thread. | `TryEnqueue` creates `SessionCommandState.Create(...)` and dictionary entries when session first observed. |
| P2 | 9 | Inbound transport | CODE/Systems/PooledTransportRouter.cs | RouteQueuedInbound | `_sessionOrder` list may grow on tick thread. | `RouteQueuedInbound` rebuilds and sorts `_sessionOrder`; list grows if session count exceeds capacity. |
| P2 | 9 | Replication serialize | CODE/Systems/DeterministicTransportQueues.cs | SnapshotDeltaSerializer.Serialize | List/HashSet growth allocations in tick-thread serialization. | `_changed`, `_removed`, `_presentEntities` may expand when entity counts exceed prior maxima. |
| P2 | 9 | Replication context | CODE/Systems/ClientReplicationSnapshotSystem.cs | GetOrCreateContext | New `SnapshotWorkContext` allocations on first session use. | `GetOrCreateContext` constructs a new `SnapshotWorkContext` when session is first seen. |
| P2 | 9 | Combat idempotence | CODE/Systems/CombatOutcomeApplicationSystem.cs | EnsureNoDuplicateIdsInBatchOrThrow | Per-apply `HashSet<string>` allocation. | Method allocates a new `HashSet<string>` each `Apply` call. |

## APPENDIX B — Search Notes (MANDATORY)
### A) Inventory of audited directories/files
- **Directories searched:**
  - `/workspace/Caelmor-Repo/CODE/Systems`
  - `/workspace/Caelmor-Repo/CODE/Systems/RuntimeHost`
  - `/workspace/Caelmor-Repo/00_ADMIN/Reference`
- **Key audited files (non-exhaustive):**
  - `CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs`
  - `CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs`
  - `CODE/Systems/RuntimeHost/ServerRuntimeHost.cs`
  - `CODE/Systems/RuntimeServerLoop.cs`
  - `CODE/Systems/WorldSimulationCore.cs`
  - `CODE/Systems/RuntimeIntegrationZeroGcHardening.cs`
  - `CODE/Systems/PooledTransportRouter.cs`
  - `CODE/Systems/DeterministicTransportQueues.cs`
  - `CODE/Systems/OutboundSendPump.cs`
  - `CODE/Systems/ClientReplicationSnapshotSystem.cs`
  - `CODE/Systems/PersistenceWorkerLoop.cs`
  - `CODE/Systems/PersistenceCompletionQueue.cs`
  - `CODE/Systems/SessionHandshakePipeline.cs`
  - `CODE/Systems/LifecycleTickMailbox.cs`
  - `CODE/Systems/DeterministicActiveSessionIndex.cs`
  - `CODE/Systems/CombatIntentQueueSystem.cs`
  - `CODE/Systems/CombatOutcomeApplicationSystem.cs`

### B) Authoritative tick driver identification
- `WorldSimulationCore.RunLoop` started by `RuntimeServerLoop.Start` → `WorldSimulationCore.Start` (see Sections 2–3).

### C) Tick hook enumeration
- Enumerated in Section 3.2 with order keys and registration site (`RuntimeCompositionRoot.Create` → `WorldBootstrapRegistration.Apply`).

### D) Worker threads enumeration
- `WorldSimulationCore` tick thread (`Caelmor.WorldSimulationCore`) started in `WorldSimulationCore.Start`.
- `OutboundSendPump` thread (`Caelmor.OutboundSendPump`) started in `OutboundSendPump.Start`.
- `PersistenceWorkerLoop` thread (`Caelmor.PersistenceWorker`) started in `PersistenceWorkerLoop.Start`.

### E) Searches performed (terms + classification)
- **Allocation terms:** `System.Linq`, `new List<`, `new Dictionary<`, `new Queue<`, `new byte[`, `Action`, `delegate`, `=>`, `.Select(`, `.Where(`, `.OrderBy(`, `.ToArray(`, `string.Format`, `$"`, `ReadOnlyCollection`, `IEnumerable`, `HashSet<` (rg across `CODE/Systems`).
- **Blocking terms:** `Thread.Sleep`, `.Wait()`, `.Result`, `Task.Wait`, `Monitor.Wait`, `File.`, `Stream`, `ReadAll`, `WriteAll`.
- **AOT risk terms:** `Reflection.Emit`, `DynamicMethod`, `Expression.Compile`, `Activator.CreateInstance`.
- **Leak risk terms:** `static`, `+=`, `-=`, `event`, `IDisposable`, `Dispose(`.

**Hot-path vs non-hot classification:**
- Hot-path hits were limited to tick-thread, outbound send thread, and persistence worker loops. Those hits are enumerated in Appendix A (Evidence Table). Validation-only and editor/support code were classified as **non-hot**.
- Blocking-term hits (`Thread.Sleep`) were classified as **non-hot for mutation windows** because they occur during cadence waits or worker idle delays rather than inside authoritative mutation windows.

### F) Limitations
- No runtime call site for `PersistenceWriteQueue.Enqueue` was found; persistence enqueue proof is **UNKNOWN** (Section 4.3).
