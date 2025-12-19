# Runtime Integration Audit — Repeat-Issues Closure Audit

## 1) Executive Summary
- **System Code Complete: NO**
- **Justification:** Authoritative command consumption is wired but no concrete runtime command handler that mutates authoritative state is present, and no non-validation entry point starts the runtime loop, leaving critical pipelines unproven in runtime composition.
- **Closure Scorecard (1–10):**
  1. Systems exist but aren’t pumped (no callers) — **PARTIAL**
  2. Islands not pipelines (missing bridges between layers) — **OPEN**
  3. Frozen authoritative commands have no runtime consumer — **PARTIAL**
  4. Client trust boundary violation (client tick/id influences authority) — **CLOSED**
  5. Thread ownership assumed not enforced (tick-only mutation called off-thread) — **PARTIAL**
  6. Disconnect/shutdown leaks (contexts/buffers/events/statics not released) — **CLOSED**
  7. Hot-path allocations after warm-up (lists/dicts/closures/LINQ/strings) — **PARTIAL**
  8. Backpressure allocates under pressure (rebuild queues, allocs on trim/drop) — **CLOSED**
  9. Replication drift (no runtime session index, outbound not drained, string fingerprints) — **PARTIAL**
  10. Combat drift (string IDs in hot loops, deep-freeze/dynamic payload allocs) — **OPEN**

## 2) Authoritative Tick & Phase Wiring (prove “pumped”)

### 2.1 Identify the authoritative tick driver
- **Tick Driver (file/type/method):** `CODE/Systems/WorldSimulationCore.cs` → `WorldSimulationCore.RunLoop`/`ExecuteOneTick`.
- **Who starts it (file/type/method):**
  - `RuntimeServerLoop.Start()` starts `_simulation.Start()` (tick thread) and `_outboundPump.Start()` (`CODE/Systems/RuntimeServerLoop.cs`, `RuntimeServerLoop.Start`).
  - `ServerRuntimeHost.Start()` starts `WorldSimulationCore.Start()` (`CODE/Systems/RuntimeIntegrationZeroGcHardening.cs`, `ServerRuntimeHost.Start`).
  - **Gap:** No runtime host or program invokes `RuntimeServerLoop.Start()` or `ServerRuntimeHost.Start()` outside validation scenarios (Appendix B search notes).
- **Tick rate enforcement (10 Hz) evidence:** `WorldSimulationCore.TickRateHz = 10` and `TickInterval = 100ms` (`WorldSimulationCore`).
- **Overrun handling evidence:** `MaxCatchUpTicksPerLoop = 3`, clamp logic with `catchUpExecuted`, and diagnostics `RecordTick(..., catchUpClamped: true)` when clamped (`WorldSimulationCore.RunLoop`).

### 2.2 Enumerate tick phases and hook order
**Phase order in `WorldSimulationCore.ExecuteOneTick`:**
1) Eligibility evaluation → 2) `ITickPhaseHook.OnPreTick` → 3) `ISimulationParticipant.Execute` per eligible entity → 4) eligibility stability check & effect commit → 5) `ITickPhaseHook.OnPostTick`.

**Registration ordering rules:** `WorldSimulationCore.RegisterPhaseHook` sorts by `OrderKey` then registration sequence (deterministic) (`WorldSimulationCore.RegisterPhaseHook`).

**Hooks registered by `RuntimeServerLoop.Create` (deterministic order):**
- `LifecycleMailboxPhaseHook` (`RuntimeServerLoop.Create`): order key `int.MinValue` unless `skipLifecycleHookRegistration`. Proof-of-life: `LifecycleMailboxCounters` incremented in `TickThreadMailbox.Drain` (`LifecycleTickMailbox.cs`).
- `InboundPumpTickHook` (`RuntimeServerLoop.Create`): order key `commandFreezeHookOrderKey` default `int.MinValue`. Proof-of-life: `InboundPumpDiagnostics` counters incremented in `InboundPumpTickHook.OnPreTick` (`RuntimeIntegrationZeroGcHardening.cs`).
- `AuthoritativeCommandConsumeTickHook` (`RuntimeServerLoop.Create`): order key `commandConsumeHookOrderKey` default `int.MinValue + 1`. Proof-of-life: `CommandConsumeDiagnostics` counters incremented in `AuthoritativeCommandConsumeTickHook.OnPreTick` (`RuntimeIntegrationZeroGcHardening.cs`).
- `HandshakeProcessingPhaseHook` (`RuntimeServerLoop.Create`): order key `int.MinValue + 2`. Proof-of-life: `SessionHandshakePipeline.RecordDeferredTick` and `HandshakePipelineMetrics` (`SessionHandshakePipeline.cs`).
- **Host-supplied `phaseHooks`**: order as provided; no runtime host found in repo to enumerate participants.
- `PersistenceCompletionPhaseHook` (optional): order key `-1024` when persistence enabled (`RuntimeServerLoop.Create`), proof-of-life via `PersistenceCompletionQueue.SnapshotMetrics` (`PersistenceCompletionQueue.cs`).
- `ClientReplicationSnapshotSystem` (`RuntimeServerLoop.Create`): order key `int.MaxValue - 512`, proof-of-life via `ReplicationSnapshotCounters` and internal debug counters (`ClientReplicationSnapshotSystem.cs`).

**Participants:** Provided via `RuntimeServerLoop.Create(... participants ...)` → `WorldBootstrapRegistration.Apply` → `WorldSimulationCore.RegisterParticipant`. No runtime host constructs this list in repo; only validation scenarios supply empty or test participants (`ClientReplicationSnapshotValidationScenarios.cs`). **If participants are required for gameplay, System Code Complete remains NO.**

### 2.3 Thread model
- **Tick/Simulation thread:** `WorldSimulationCore` background thread named `"Caelmor.WorldSimulationCore"` (`WorldSimulationCore.Start`).
- **Transport receive thread(s):** External transport threads call `PooledTransportRouter.EnqueueInbound` (thread-safe via `_inboundGate` lock; no thread creation in repo). (`PooledTransportRouter.cs`).
- **Transport send thread:** `OutboundSendPump` background thread named `"Caelmor.OutboundSendPump"` (`OutboundSendPump.Start`).
- **Persistence worker thread:** `PersistenceWorkerLoop` background thread named `"Caelmor.PersistenceWorker"` (`PersistenceWorkerLoop.Start`).
- **Other worker threads:** `TickSystem` spawns `"Caelmor.TickSystem"` when used, but no runtime host references it in this repo; `TimeSlicedWorkScheduler` runs on the tick thread (`TickSystemCore.cs`, `TimeSlicedWorkScheduler.cs`).

## 3) End-to-End Pipeline Proofs (must include call chains)

### 3.1 Inbound pipeline proof (transport → ingest → freeze → consume → mutate)
**Call chain (evidence):**
1) **Inbound enters server ownership:** `PooledTransportRouter.EnqueueInbound` rents `PooledPayloadLease`, stamps `ServerStampedInboundCommand` with server receive tick/seq, enqueues to per-session queue (`PooledTransportRouter.EnqueueInbound`).
2) **Pump that drains inbound (tick hook):** `InboundPumpTickHook.OnPreTick` (registered via `RuntimeServerLoop.Create` → `WorldBootstrapRegistration.Apply` → `WorldSimulationCore.RegisterPhaseHook`).
3) **RouteQueuedInbound call site:** `InboundPumpTickHook.OnPreTick` → `_transport.RouteQueuedInbound(context.TickIndex, ...)` (`RuntimeIntegrationZeroGcHardening.cs`).
4) **Ingress → ingestor bridge:** `PooledTransportRouter.RouteQueuedInbound` → `DeterministicTransportRouter.RouteInbound` → `AuthoritativeCommandIngress.TryEnqueue` (`DeterministicTransportQueues.cs`).
5) **Freeze call site (per tick):** `InboundPumpTickHook.OnPreTick` → `FreezeCommands` → `AuthoritativeCommandIngestor.FreezeSessions/FreezeAllSessions` (`RuntimeIntegrationZeroGcHardening.cs`).
6) **Runtime consumer tick hook:** `AuthoritativeCommandConsumeTickHook.OnPreTick` reads `IAuthoritativeCommandIngestor.GetFrozenBatch` and iterates `FrozenCommandBatch` (`RuntimeIntegrationZeroGcHardening.cs`).
7) **Handler dispatch call site:** `AuthoritativeCommandConsumeTickHook.OnPreTick` → `CommandHandlerRegistry.TryGetHandler` → `IAuthoritativeCommandHandler.Handle`.
8) **Concrete handler that mutates runtime state:** **Missing.** The only implementation present is `NoOpCommandHandler` (increments counters only). No runtime command handler mutating authoritative state exists in repo (`RuntimeIntegrationZeroGcHardening.cs`).

**Status:** **OPEN (P0)** — missing runtime handler/mutation link.

### 3.2 Outbound pipeline proof (active sessions → snapshots → serialize → queue → send pump)
**Runtime session index implementation (non-validation):** `DeterministicActiveSessionIndex` implements `IActiveSessionIndex` (`DeterministicActiveSessionIndex.cs`). **Injection into runtime host is not found in repo; only validation scenarios pass instances.**

**Call chain (evidence):**
1) **Snapshot hook registration:** `ClientReplicationSnapshotSystem` is registered as a phase hook in `RuntimeServerLoop.Create` with order key `int.MaxValue - 512`.
2) **Tick hook call site:** `WorldSimulationCore.ExecuteOneTick` → `ITickPhaseHook.OnPostTick` → `ClientReplicationSnapshotSystem.OnPostTick`.
3) **Snapshot build + serialize:** `ClientReplicationSnapshotSystem.OnPostTick` → `CreateWorkItem` → `TimeSlicedWorkScheduler.Enqueue` → `SnapshotWorkItem.ExecuteSlice` → `BuildSnapshot` → `_queue.Enqueue` (`ClientReplicationSnapshotSystem.cs`).
4) **Serialization call site:** `BoundedReplicationSnapshotQueue.Enqueue` → `SnapshotDeltaSerializer.Serialize` → `SerializedSnapshot.Rent` (`DeterministicTransportQueues.cs`).
5) **Outbound queue enqueue:** `PooledTransportRouter.RouteSnapshot` → `DeterministicTransportRouter.RouteSnapshot` → `BoundedReplicationSnapshotQueue.Enqueue` (caps + metrics).
6) **Outbound send pump:** `OutboundSendPump.Run`/`PumpOnce` → `IActiveSessionIndex.SnapshotSessionsDeterministic` → `PooledTransportRouter.TryDequeueOutbound` → `DeterministicTransportRouter.TryDequeueSnapshot` → `BoundedReplicationSnapshotQueue.TryDequeue` → `IOutboundTransportSender.TrySend` (`OutboundSendPump.cs`).

**Status:** **PARTIAL (P1)** — outbound chain exists, but runtime injection of deterministic session index is unproven outside validation.

### 3.3 Persistence pipeline proof (enqueue → worker drain off-thread → completion → apply-on-tick)
**Call chain (evidence):**
1) **Enqueue write (tick thread):** `PersistenceWriteQueue.Enqueue` (tick thread caller; queue is locked) (`DeterministicTransportQueues.cs`).
2) **Worker loop start/stop:** `RuntimeServerLoop.Start` → `_persistenceWorker.Start()`; `RuntimeServerLoop.Stop` → `_persistenceWorker.Stop()` (`RuntimeServerLoop.cs`).
3) **Worker drain call site:** `PersistenceWorkerLoop.Run` → `PumpOnce` → `_writeQueue.TryDequeue` → `IPersistenceWriter.Execute` (`PersistenceWorkerLoop.cs`).
4) **Completion enqueue:** `PersistenceWorkerLoop.PumpOnce` → `_completionQueue.TryEnqueue` (`PersistenceCompletionQueue.cs`).
5) **Apply-on-tick hook:** `PersistenceCompletionPhaseHook.OnPreTick` → `_queue.Drain(_applier, tickIndex)` (`PersistenceCompletionQueue.cs`).

**Optionality / fail-fast:** `RuntimeServerLoop.ValidatePipelineWiring` requires persistence hook + worker when persistence queues are enabled; throws `RUNTIME_PIPELINE_MISSING_HOOKS` if missing (`RuntimeServerLoop.cs`).

## 4) Trust Boundary Audit (client cannot influence authority)
- **Client tick/sequence not authoritative:** `InboundPumpTickHook.OnPreTick` rejects any `ClientSubmitTick > 0` by incrementing `_rejectedClientTickProvided` and disposing the envelope (`RuntimeIntegrationZeroGcHardening.cs`).
- **Server stamping present:** `PooledTransportRouter.EnqueueInbound` stamps `ServerStampedInboundCommand` with server receive tick (`_currentReceiveTick`) and server receive seq (`_receiveSeqBySession`) (`PooledTransportRouter.cs`).
- **Ordering uses server seq:** `AuthoritativeCommandIngress.DrainDeterministic` selects the next command by `ServerReceiveTick` then `ServerReceiveSeq` across sessions (`DeterministicTransportQueues.cs`).
- **Conclusion:** Trust boundary enforced; client tick is treated as untrusted metadata and rejected.

## 5) Thread Ownership Enforcement Audit
- **Command ingestion:** `AuthoritativeCommandIngestor` uses lock `_gate`; `InboundPumpTickHook.OnPreTick` asserts tick thread (`TickThreadAssert.AssertTickThread`) (`RuntimeIntegrationZeroGcHardening.cs`).
- **Transport queues:** `PooledTransportRouter.RouteQueuedInbound` and `RouteSnapshot` assert tick thread; enqueue paths are locked (`PooledTransportRouter.cs`).
- **Replication:** `ClientReplicationSnapshotSystem.OnPreTick/OnPostTick` asserts tick thread (`ClientReplicationSnapshotSystem.cs`).
- **Session index:** `DeterministicActiveSessionIndex` uses internal lock for add/remove/snapshot (`DeterministicActiveSessionIndex.cs`).
- **Visibility/AOI:** `VisibilityCullingService.Track/RefreshVisibility/RemoveSession/Clear` assert tick thread (`RuntimeIntegrationZeroGcHardening.cs`).
- **Entity registry:** `DeterministicEntityRegistry` uses lock for mutation and snapshot (`DeterministicEntityRegistry.cs`).
- **Lifecycle/disconnect:** `TickThreadMailbox.Drain` asserts tick thread; `LifecycleApplier.Apply` asserts tick thread (`LifecycleTickMailbox.cs`, `RuntimeServerLoop.cs`).
- **Gap (PARTIAL):** Combat systems mutate state without explicit tick-thread asserts/locks (e.g., `CombatOutcomeApplicationSystem.Apply` and `CombatIntentQueueSystem.SubmitIntent` rely on `ITickSource` but do not assert thread ownership). Thread ownership enforcement for combat path remains unproven (`CombatOutcomeApplicationSystem.cs`, `CombatIntentQueueSystem.cs`).

## 6) Disconnect / Shutdown Leak Audit
- **Disconnect call chain:** `RuntimeServerLoop.OnSessionDisconnected` → `TickThreadMailbox.TryEnqueue*` → `LifecycleMailboxPhaseHook.OnPreTick` → `TickThreadMailbox.Drain` → `LifecycleApplier.Apply` →
  - `_transport.DropAllForSession` (drops inbound/outbound queues, disposes payloads) (`PooledTransportRouter.cs`),
  - `_commands.DropSession` (returns pooled buffers) (`RuntimeIntegrationZeroGcHardening.cs`),
  - `_handshakes.Drop` (clears pending handshakes) (`SessionHandshakePipeline.cs`),
  - `_visibility.RemoveSession` (returns pooled arrays) (`RuntimeIntegrationZeroGcHardening.cs`),
  - `_replication.OnSessionDisconnected` (removes work contexts) (`ClientReplicationSnapshotSystem.cs`).
- **Shutdown call chain:** `RuntimeServerLoop.ShutdownServer` → `Stop` → `_persistenceWorker.Stop` + `_outboundPump.Stop` + `_simulation.Stop` → `ClearTransientState` → `_transport.Clear`, `_handshakes.Reset`, `_commands.Clear`, `_visibility.Clear`, `_entities.ClearAll`, `_lifecycleMailbox.Clear`, `_persistenceCompletions.Clear`, `_persistenceWrites.Clear` (`RuntimeServerLoop.cs`).
- **Pooled buffer return evidence:** `PooledPayloadLease.Dispose`, `SerializedSnapshot.Dispose`, `PersistenceCompletion.Dispose` release pooled buffers on drop/trim (`DeterministicTransportQueues.cs`, `PersistenceCompletionQueue.cs`).

**Status:** **CLOSED** — deterministic cleanup exists for disconnect and shutdown paths.

## 7) Hot-Path Allocation Audit (after warm-up)
**Method:** Required allocation searches (Appendix B). Hot-path classification focuses on tick thread, transport send/receive, and persistence worker paths.

- **Tick driver + phase hooks:**
  - **Classification:** **SOME** — `WorldSimulationCore.EnsureCapacity` can allocate when entity/participant counts exceed prior maxima (`WorldSimulationCore.cs`).
  - **Known alloc sites:** array growth in `EnsureCapacity` for `_participantSnapshot`, `_phaseHooksSnapshot`, `_eligibilityGatesSnapshot`, `_eligibleArray`.

- **Inbound decode/routing/ingestor/freeze/consume:**
  - **Classification:** **SOME** — command rings and per-session dictionaries grow when new sessions appear (`AuthoritativeCommandIngestor.TryEnqueue`), and `AuthoritativeCommandIngress.EnsureCapacity` can grow snapshot buffers (`DeterministicTransportQueues.cs`).
  - **Known alloc sites:** dictionary growth in `_perSession/_metrics` and array growth from `EnsureCapacity`.

- **Handshake pipeline:**
  - **Classification:** **NONE** — fixed ring buffers allocated at construction (`SessionHandshakePipeline.cs`).

- **Replication snapshot build/serialize:**
  - **Classification:** **SOME** — `SnapshotWorkContext` uses `ArrayPool.Rent` for per-session buffers; `SnapshotDeltaSerializer` holds `List<>` that can grow with entity counts (`ClientReplicationSnapshotSystem.cs`, `DeterministicTransportQueues.cs`).
  - **Known alloc sites:** `ArrayPool.Rent` when pool is empty; `List<>` growth in `_changed/_removed` inside `SnapshotDeltaSerializer`.

- **Visibility/AOI:**
  - **Classification:** **SOME** — `VisibilityCullingService.RefreshVisibility` uses `_queryBuffer` list that can grow with visibility size and rents new `EntityHandle[]` when bucket grows (`RuntimeIntegrationZeroGcHardening.cs`).

- **Persistence trim/drop + worker drain + apply-on-tick:**
  - **Classification:** **SOME** — `PersistenceWriteQueue` and `PersistenceApplyState` dictionaries grow as new players/saves appear (`DeterministicTransportQueues.cs`, `PersistenceWorkerLoop.cs`).
  - **Known alloc sites:** dictionary growth; no per-drop allocations.

- **Combat staging/resolve/apply:**
  - **Classification:** **SOME** — `CombatOutcomeApplicationSystem` allocates `HashSet<string>` per tick in `_appliedPayloadIdsByTick` and stores string payload IDs; `CombatIntentQueueSystem` uses dictionaries keyed by ticks/entities and strings on submission (`CombatOutcomeApplicationSystem.cs`, `CombatIntentQueueSystem.cs`).

**Explicit remaining hot-path allocations in tick-reachable paths:**
- `new List<>` growth in `SnapshotDeltaSerializer` (`DeterministicTransportQueues.cs`).
- `ArrayPool.Rent` in replication snapshot capture (`ClientReplicationSnapshotSystem.cs`).
- `HashSet<string>` and string payload IDs in combat outcome application (`CombatOutcomeApplicationSystem.cs`).

## 8) Backpressure Under Pressure Audit (alloc-free trim/drop)
- **Inbound transport mailboxes:** caps = `RuntimeBackpressureConfig.MaxInboundCommandsPerSession` + `MaxQueuedBytesPerSession`; overflow rejects newest and disposes payload (`PooledTransportRouter.EnqueueInbound`). Metrics tracked in `SessionQueueMetrics`.
- **Authoritative ingress rings:** caps = `RuntimeBackpressureConfig.MaxInboundCommandsPerSession`; overflow drop-newest via ring `TryPush` (`AuthoritativeCommandIngestor.TryEnqueue`). Metrics in `SessionCommandMetrics`.
- **Handshake queue:** fixed-size ring, overflow rejects with `HandshakeRejectionReason.QueueFull` (`SessionHandshakePipeline.TryEnqueue`). Metrics in `HandshakePipelineMetrics`.
- **Replication snapshot queue:** caps = `MaxOutboundSnapshotsPerSession` + `MaxQueuedBytesPerSession`; overflow drops oldest and disposes pooled snapshots (`BoundedReplicationSnapshotQueue.EnforceCaps`). Metrics in `SnapshotQueueMetrics` + `ReplicationSnapshotCounters`.
- **Outbound send pump:** bounded per iteration via `_maxPerSession` and `_maxPerIteration` (`OutboundSendPump.PumpOnce`).
- **Persistence write queue:** caps = per-player `MaxPersistenceWritesPerPlayer` + `MaxPersistenceWriteBytesPerPlayer`, global `MaxPersistenceWritesGlobal` + `MaxPersistenceWriteBytesGlobal`; overflow drop-oldest without rebuild (`PersistenceWriteQueue.EnforceCaps/EnforceGlobalCap`). Metrics in `PersistenceQueueMetrics` + `PersistencePipelineCounters`.
- **Persistence completion mailbox:** caps = `MaxPersistenceCompletions` + `MaxPersistenceCompletionBytes`; overflow drop-oldest and dispose payloads (`PersistenceCompletionQueue.EnforceCapsLocked`). Metrics in `CompletionQueueMetrics`.
- **Lifecycle mailbox:** caps = `MaxLifecycleOps` + `MaxLifecycleOpBytes`; overflow drop-oldest without allocation (`TickThreadMailbox.TryEnqueue`). Metrics in `LifecycleMailboxCounters`.
- **Combat intent staging:** caps = `SessionIntentCapPerTick` and `ActorIntentCapPerTick`; overflow drop-newest (`CombatIntentQueueSystem`).

**Status:** **CLOSED** — trim/drop paths dispose pooled buffers and avoid rebuild allocations.

## 9) Replication Drift Closure Audit
- **Runtime session index exists:** `DeterministicActiveSessionIndex` provides deterministic session order (`DeterministicActiveSessionIndex.cs`). **Injection into runtime host not found** (validation uses it). 
- **Outbound drained:** `OutboundSendPump.Run` continuously drains snapshots via `TryDequeueOutbound` (`OutboundSendPump.cs`).
- **Fingerprints:** Per-session fingerprints are `Dictionary<EntityHandle, ulong>` (no string churn) (`BoundedReplicationSnapshotQueue` / `SnapshotDeltaSerializer`).
- **Snapshot buffers pooled:** `SerializedSnapshot.Rent`/`Dispose` and `ClientReplicationSnapshot` use pools; drop paths dispose (`DeterministicTransportQueues.cs`, `ClientReplicationSnapshotSystem.cs`).

**Status:** **PARTIAL (P1)** — deterministic index is implemented, but runtime wiring is unproven outside validation.

## 10) Combat Drift Closure Audit
- **String IDs in hot loops:** `CombatOutcomeApplicationSystem` builds string payload IDs per result (`PayloadId.IntentResult/DamageOutcome/...`), stores `HashSet<string>` per tick, and tracks `Dictionary<EntityHandle, string>` (`CombatOutcomeApplicationSystem.cs`).
- **Dynamic payload dictionaries:** `CombatOutcomeApplicationSystem` uses `Dictionary<int, HashSet<string>>` for idempotence and `Dictionary<EntityHandle, string>` for snapshots.
- **Deep-freeze allocations per intent:** not audited to be allocation-free; string payload IDs and per-tick sets indicate drift risk.
- **Caps/metrics:** No explicit caps or backpressure metrics for combat payload ID storage.

**Status:** **OPEN (P1)** — combat path uses string identifiers and dynamic payload sets in tick-time application.

## 11) Fail-Fast Wiring Gate Audit
- **Validation gate:** `RuntimeServerLoop.ValidatePipelineWiring` checks for inbound pump hook, command consume hook, handshake hook, lifecycle mailbox hook, replication hook, outbound pump, and (if persistence enabled) persistence completion hook + worker loop. Missing components throw `InvalidOperationException` with `RUNTIME_PIPELINE_MISSING_HOOKS` (`RuntimeServerLoop.cs`).
- **Command handler gate:** `RuntimeServerLoop.Start` asserts at least one command handler in DEBUG (`_commandConsumeHook.HandlerCount <= 0` throws). (`RuntimeServerLoop.Start`).

## 12) Risk Register (recurring-issue related only)
- **P0 — Missing runtime command handler / mutation path (Failure Modes 2 & 3)**
  - **File/Method:** `RuntimeIntegrationZeroGcHardening.cs` → `AuthoritativeCommandConsumeTickHook.OnPreTick`, `NoOpCommandHandler`.
  - **Why:** Frozen commands are consumed but no concrete handler mutates authoritative state; only no-op handler exists.
  - **Minimal fix strategy:** Implement at least one `IAuthoritativeCommandHandler` that mutates authoritative runtime state (or enqueues deterministic intents), and register it in runtime composition.
- **P0 — Runtime loop not started in repo (Failure Mode 1)**
  - **File/Method:** `RuntimeServerLoop.Start`, `ServerRuntimeHost.Start`.
  - **Why:** No non-validation entry point invokes runtime start; pumps are unproven in runtime composition.
  - **Minimal fix strategy:** Add a host bootstrap that constructs `RuntimeServerLoop` (or `ServerRuntimeHost`) and calls `Start()` in the actual runtime application.
- **P1 — Deterministic session index injection unproven (Failure Mode 9)**
  - **File/Method:** `RuntimeServerLoop.Create`, `ClientReplicationSnapshotSystem` constructor.
  - **Why:** `IActiveSessionIndex` is required but runtime injection isn’t shown outside validation.
  - **Minimal fix strategy:** Wire `DeterministicActiveSessionIndex` into runtime host and document usage.
- **P1 — Combat drift (Failure Mode 10)**
  - **File/Method:** `CombatOutcomeApplicationSystem.Apply`, `PayloadId.*`.
  - **Why:** String payload IDs and per-tick `HashSet<string>` in tick path violate drift guardrails.
  - **Minimal fix strategy:** Replace string identifiers with fixed-size numeric IDs, preallocate idempotence pools, and cap per-tick storage.
- **P1 — Thread ownership enforcement incomplete in combat (Failure Mode 5)**
  - **File/Method:** `CombatOutcomeApplicationSystem.Apply`, `CombatIntentQueueSystem.SubmitIntent`.
  - **Why:** Tick-only mutation relies on `ITickSource` but lacks `TickThreadAssert` or explicit locking.
  - **Minimal fix strategy:** Enforce tick-thread asserts on combat entry points or marshal via tick-thread mailbox.

---

## APPENDIX A — Evidence Table (MANDATORY)
| Severity | Failure mode # | Subsystem | File | Type/Method | Finding | Evidence summary |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | 1 | Runtime start | RuntimeServerLoop.cs / RuntimeIntegrationZeroGcHardening.cs | RuntimeServerLoop.Start / ServerRuntimeHost.Start | No non-validation caller found for runtime start. | Search for `RuntimeServerLoop` and `ServerRuntimeHost` shows only definitions; no runtime entrypoint or host bootstrap calls `Start()`. |
| P0 | 2 | Authoritative commands | RuntimeIntegrationZeroGcHardening.cs | AuthoritativeCommandConsumeTickHook.OnPreTick | Consumer exists but no concrete handler mutates runtime state. | Hook dispatches to `ICommandHandlerRegistry`; only `NoOpCommandHandler` is present and mutates no state. |
| P0 | 3 | Authoritative commands | RuntimeIntegrationZeroGcHardening.cs | NoOpCommandHandler | Frozen commands have no runtime consumer that mutates state. | `NoOpCommandHandler` increments counters only; no authoritative mutation handler exists. |
| P1 | 5 | Combat thread ownership | CombatOutcomeApplicationSystem.cs | Apply | No tick-thread assert/lock on tick-owned combat mutation. | `Apply` mutates dictionaries and emits events without `TickThreadAssert` or lock; thread contract relies only on `ITickSource`. |
| P1 | 9 | Replication session index | DeterministicActiveSessionIndex.cs / RuntimeServerLoop.cs | DeterministicActiveSessionIndex / RuntimeServerLoop.Create | Deterministic index exists but runtime injection unproven. | `IActiveSessionIndex` required in `RuntimeServerLoop.Create`; no runtime host wiring found outside validation. |
| P1 | 10 | Combat drift | CombatOutcomeApplicationSystem.cs | Apply / PayloadId.* | String payload IDs and per-tick string sets in tick path. | `HashSet<string>` per tick and string IDs created in application loops. |
| P2 | 7 | Replication serialize | DeterministicTransportQueues.cs | SnapshotDeltaSerializer.Serialize | List growth can allocate on hot path if entity counts exceed prior maxima. | `_changed`/`_removed` lists grow with observed entity count; growth allocates. |
| P2 | 7 | Tick driver | WorldSimulationCore.cs | EnsureCapacity | Tick-thread snapshots can allocate when entity/participant counts exceed prior maxima. | `EnsureCapacity` reallocates arrays when counts increase. |

## APPENDIX B — Search Notes (MANDATORY)
- **Directories searched:**
  - `/workspace/Caelmor-Repo/CODE/Systems`
  - `/workspace/Caelmor-Repo/00_ADMIN/Reference` (guardrail brief)

- **Files audited (non-exhaustive, relevant to runtime paths):**
  - `CODE/Systems/WorldSimulationCore.cs`
  - `CODE/Systems/RuntimeServerLoop.cs`
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
  - `CODE/Systems/CombatOutcomeApplicationSystem.cs`
  - `CODE/Systems/CombatIntentQueueSystem.cs`
  - `CODE/Systems/RuntimeBackpressureConfig.cs`

- **Allocation search terms used (per requirement):**
  - `rg -n "System\.Linq"`
  - `rg -n "new List<"`
  - `rg -n "new Dictionary<"`
  - `rg -n "new Queue<"`
  - `rg -n "new byte\["`
  - `rg -n "\bAction\b"`
  - `rg -n "\bdelegate\b"`
  - `rg -n "=>"`
  - `rg -n "\.Select\(|\.Where\(|\.OrderBy\(|\.ToArray\("`
  - `rg -n "string\.Format|\$\""`
  - `rg -n "ReadOnlyCollection|IEnumerable"`

- **Blocking search terms used (per requirement):**
  - `rg -n "Thread\.Sleep|\.Wait\(\)|\.Result|Task\.Wait|Monitor\.Wait|File\.|Stream|ReadAll|WriteAll"`

- **AOT risk terms used (per requirement):**
  - `rg -n "Reflection\.Emit|DynamicMethod|Expression\.Compile|Activator\.CreateInstance"`

- **Leak risk terms used (per requirement):**
  - `rg -n "\bstatic\b|\+=|-=|\bevent\b|IDisposable|Dispose\(|OnDestroy|OnDisable"`

- **Limitations encountered:**
  - No runtime host/bootstrap invoking `RuntimeServerLoop.Start` or `ServerRuntimeHost.Start` found in repo; only validation scenarios instantiate the loop. This prevents proving runtime composition beyond validation harnesses.
