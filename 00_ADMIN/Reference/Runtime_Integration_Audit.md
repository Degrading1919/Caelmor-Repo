1) Executive Summary
- System Code Complete: NO
- One-sentence justification: Core runtime orchestration/pipelines are present and started, but combat hot-path string IDs and per-tick HashSet allocations (plus other hot-path allocations) remain, leaving repeat-issue closure incomplete against the MMO guardrails.
- Closure Scorecard:
  1) CLOSED
  2) CLOSED
  3) CLOSED
  4) CLOSED
  5) CLOSED
  6) CLOSED
  7) PARTIAL
  8) PARTIAL
  9) PARTIAL
  10) CLOSED
  11) CLOSED
  12) PARTIAL

2) Runtime Orchestration Proof (must be explicit)
2.1 EntryPoint proof (non-validation)
- EntryPoint file/type/method: CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs — HeadlessServerEntryPoint.Main
- Call chain: HeadlessServerEntryPoint.Main -> RuntimeCompositionRoot.CreateHost -> ServerRuntimeHost.Start (CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs, RuntimeCompositionRoot.CreateHost; CODE/Systems/RuntimeHost/ServerRuntimeHost.cs, ServerRuntimeHost.Start).

2.2 CompositionRoot proof
- File/type/method: CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs — RuntimeCompositionRoot.Create
- Constructs:
  - Tick core: WorldSimulationCore (new WorldSimulationCore in Create).
  - Pumps: InboundPumpTickHook (Create), AuthoritativeCommandConsumeTickHook (Create), HandshakeProcessingPhaseHook (Create), ClientReplicationSnapshotSystem (Create), OutboundSendPump (Create).
  - Consumer/handlers: CommandHandlerRegistry (Create) plus settings.ConfigureCommandHandlers if provided; entrypoint registers SessionCommandCounterHandler (mutating) in HeadlessServerEntryPoint.RegisterRuntimeCommandHandlers.
  - Session index: DeterministicActiveSessionIndex (Create / settings.ActiveSessions), injected into replication and outbound pump.
  - Replication: ClientReplicationSnapshotSystem (Create).
  - Outbound pump: OutboundSendPump (Create).
  - Persistence posture: PersistenceSettings only if settings.Persistence and settings.Persistence.Writer are non-null; then PersistenceWriteQueue, PersistenceCompletionQueue, PersistenceWorkerLoop, PersistenceCompletionPhaseHook, PersistenceApplyState created in Create.
- Registration sites and phase order:
  - Combined hooks built in RuntimeCompositionRoot.Create: LifecycleMailboxPhaseHook (order key settings.LifecycleHookOrderKey), InboundPumpTickHook (settings.CommandFreezeHookOrderKey), AuthoritativeCommandConsumeTickHook (settings.CommandConsumeHookOrderKey), HandshakeProcessingPhaseHook (settings.HandshakeProcessingHookOrderKey), optional PersistenceCompletionPhaseHook (settings.PersistenceCompletionHookOrderKey), then ClientReplicationSnapshotSystem (settings.ReplicationHookOrderKey). Hooks are registered via WorldBootstrapRegistration.Apply -> WorldSimulationCore.RegisterPhaseHook (CODE/Systems/WorldBootstrapRegistration.cs).
- Fail-fast wiring gate call site and checks:
  - ServerRuntimeHost.Start -> ValidateRequiredHooks throws if missing inbound pump, consume hook, freeze hook, lifecycle hook, replication hook, outbound pump, or persistence hook when persistence enabled (CODE/Systems/RuntimeHost/ServerRuntimeHost.cs).
  - RuntimeServerLoop.Start -> ValidatePipelineWiring throws if hooks or persistence worker missing; DEBUG-only: handler registration counts must be > 0 and mutating handler count > 0 (CODE/Systems/RuntimeServerLoop.cs).
  - Persistence configuration fail-fast: HeadlessServerEntryPoint.TryConfigurePersistence returns false when mode is Enabled and no writer is available, blocking host start (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs).

2.3 Host lifecycle proof
- ServerRuntimeHost.Start/Stop: CODE/Systems/RuntimeHost/ServerRuntimeHost.cs — Start calls RuntimeServerLoop.Start; Stop calls RuntimeServerLoop.Stop.
- Threads started and stop paths:
  - Tick thread: WorldSimulationCore.Start creates background thread "Caelmor.WorldSimulationCore" and stops via CancellationToken + Join (CODE/Systems/WorldSimulationCore.cs).
  - Outbound pump: OutboundSendPump.Start creates background thread "Caelmor.OutboundSendPump" and stops via CancellationToken + Join (CODE/Systems/OutboundSendPump.cs).
  - Persistence worker (if enabled): PersistenceWorkerLoop.Start creates background thread "Caelmor.PersistenceWorker" and stops via CancellationToken + Join (CODE/Systems/PersistenceWorkerLoop.cs).
  - Stop path uses Stop() for persistence, outbound, simulation; no Thread.Abort (CODE/Systems/RuntimeServerLoop.cs).

3) Authoritative Tick & Phase Wiring
3.1 Identify authoritative tick driver
- File/type/method: CODE/Systems/WorldSimulationCore.cs — WorldSimulationCore.RunLoop
- Started by: RuntimeServerLoop.Start -> WorldSimulationCore.Start (CODE/Systems/RuntimeServerLoop.cs).
- Tick rate enforcement: TickRateHz = 10, TickInterval = 100ms; RunLoop uses Stopwatch and sleeps/spins to hit interval; MaxCatchUpTicksPerLoop = 3 with clamp path (WorldSimulationCore.RunLoop).
- Overrun handling: TickDiagnostics.RecordTick called with overrun and catch-up clamp flags; if behind beyond MaxCatchUpTicksPerLoop, tickCounter is advanced and clamped (WorldSimulationCore.RunLoop).

3.2 Tick hook list (phase order)
- Lifecycle mailbox hook
  - File/type/method: CODE/Systems/RuntimeServerLoop.cs — LifecycleMailboxPhaseHook.OnPreTick
  - Phase: Pre-Tick
  - Thread: tick thread (TickThreadMailbox.Drain asserts tick thread)
  - Proof-of-life counters: LifecycleMailboxCounters in RuntimeServerLoop.CaptureDiagnostics (LifecycleOpsEnqueued/Applied/DisconnectsApplied/Dropped).
- Inbound pump hook
  - File/type/method: CODE/Systems/RuntimeIntegrationZeroGcHardening.cs — InboundPumpTickHook.OnPreTick
  - Phase: Pre-Tick
  - Thread: tick thread (RuntimeGuardrailChecks.AssertTickThreadEntry)
  - Proof-of-life counters: InboundPumpDiagnostics.InboundPumpTicksExecuted, InboundFramesRouted, CommandsEnqueuedToIngestor.
- Command consume hook
  - File/type/method: CODE/Systems/RuntimeIntegrationZeroGcHardening.cs — AuthoritativeCommandConsumeTickHook.OnPreTick
  - Phase: Pre-Tick
  - Thread: tick thread (RuntimeGuardrailChecks.AssertTickThreadEntry)
  - Proof-of-life counters: CommandConsumeDiagnostics.FrozenBatchesConsumed, CommandsDispatched, MutatingHandlerInvocations.
- Handshake hook
  - File/type/method: CODE/Systems/SessionHandshakePipeline.cs — HandshakeProcessingPhaseHook.OnPreTick
  - Phase: Pre-Tick
  - Thread: tick thread (TickThreadAssert.AssertTickThread)
  - Proof-of-life counters: HandshakePipelineMetrics.Enqueued/Processed/DroppedQueueFull/DeferredTicks (SessionHandshakePipeline.SnapshotMetrics).
- Persistence completion hook (if enabled)
  - File/type/method: CODE/Systems/PersistenceCompletionQueue.cs — PersistenceCompletionPhaseHook.OnPreTick
  - Phase: Pre-Tick
  - Thread: tick thread (PersistenceCompletionQueue.Drain asserts tick thread)
  - Proof-of-life counters: PersistencePipelineCounters.CompletionsApplied (PersistenceCompletionApplier.Apply increments).
- Replication hook
  - File/type/method: CODE/Systems/ClientReplicationSnapshotSystem.cs — ClientReplicationSnapshotSystem.OnPostTick
  - Phase: Post-Tick
  - Thread: tick thread (RuntimeGuardrailChecks.AssertTickThreadEntry)
  - Proof-of-life counters: ReplicationSnapshotCounters.RecordSnapshotDequeuedForSend (OutboundSendPump) and ReplicationSnapshotCounters.RecordSnapshotBuilt (ClientReplicationSnapshotSystem).
- Note: Additional phase hooks can be injected via RuntimeCompositionSettings.PhaseHooks; no other hooks are proven without explicit settings (UNKNOWN).

4) End-to-End Pipeline Proofs (function-level call chains)
4.1 Inbound pipeline proof (transport -> ingest -> freeze -> consume -> mutate)
- Inbound enters server ownership:
  - InProcTransportAdapter.TryEnqueueInbound -> PooledTransportRouter.EnqueueInbound (CODE/Systems/InProcTransportAdapter.cs -> CODE/Systems/PooledTransportRouter.cs). Server stamps receive seq and receive tick at enqueue (PooledTransportRouter.EnqueueInbound).
- Inbound pump tick hook call site:
  - RuntimeCompositionRoot.Create registers InboundPumpTickHook via PhaseHookRegistration; WorldSimulationCore invokes OnPreTick each tick (CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs; CODE/Systems/WorldBootstrapRegistration.cs; CODE/Systems/WorldSimulationCore.cs).
- Ingress -> ingestor bridge call site:
  - InboundPumpTickHook.OnPreTick -> PooledTransportRouter.RouteQueuedInbound -> DeterministicTransportRouter.RouteInbound (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs; CODE/Systems/PooledTransportRouter.cs; CODE/Systems/DeterministicTransportQueues.cs).
- Freeze call site (per tick):
  - InboundPumpTickHook.OnPreTick -> FreezeCommands -> AuthoritativeCommandIngestor.FreezeSessions/FreezeAllSessions (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
- Consume call site (reads FrozenCommandBatch):
  - AuthoritativeCommandConsumeTickHook.OnPreTick -> _ingestor.GetFrozenBatch (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
- Dispatch call site (handler registry):
  - AuthoritativeCommandConsumeTickHook.OnPreTick -> CommandHandlerRegistry.TryGetHandler -> handler.Handle (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
- Concrete mutating handler:
  - HeadlessServerEntryPoint.RegisterRuntimeCommandHandlers registers SessionCommandCounterHandler (IAuthoritativeStateMutatingCommandHandler) for command type validation.session_command_count; handler mutates PlayerSessionSystem.TryRecordCommandHandled (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs; CODE/Systems/SessionCommandCounterHandler.cs; CODE/Systems/PlayerSessionSystem.cs).

4.2 Outbound pipeline proof (active sessions -> snapshots -> serialize -> queue -> send pump)
- Runtime IActiveSessionIndex implementation and injection:
  - DeterministicActiveSessionIndex created in HeadlessServerEntryPoint.TryBuildSettings (ActiveSessions) and passed via RuntimeCompositionSettings.ActiveSessions to RuntimeCompositionRoot.Create; injected into ClientReplicationSnapshotSystem and OutboundSendPump (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs; CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs).
- Snapshot build tick hook call site:
  - ClientReplicationSnapshotSystem.OnPostTick enqueues time-sliced work items; SnapshotWorkItem.ExecuteSlice builds snapshot, then queues (CODE/Systems/ClientReplicationSnapshotSystem.cs).
- Serialize call site:
  - PooledTransportRouter.RouteSnapshot -> DeterministicTransportRouter.RouteSnapshot -> BoundedReplicationSnapshotQueue.Enqueue -> SnapshotDeltaSerializer.Serialize (CODE/Systems/PooledTransportRouter.cs; CODE/Systems/DeterministicTransportQueues.cs).
- Outbound queue enqueue call site + caps/metrics:
  - BoundedReplicationSnapshotQueue.Enqueue enqueues SerializedSnapshot, updates per-session metrics, and EnforceCaps drops oldest when MaxOutboundSnapshotsPerSession/MaxQueuedBytesPerSession exceeded (CODE/Systems/DeterministicTransportQueues.cs).
- Outbound send pump drain call site:
  - OutboundSendPump.Run/PumpOnce -> PooledTransportRouter.TryDequeueOutbound -> DeterministicTransportRouter.TryDequeueSnapshot -> IOutboundTransportSender.TrySend (CODE/Systems/OutboundSendPump.cs; CODE/Systems/PooledTransportRouter.cs; CODE/Systems/DeterministicTransportQueues.cs).

4.3 Persistence posture proof (must be conclusive)
- Option A (enabled):
  - Enqueue call chain: PersistenceSessionEvents.OnSessionActivated/OnSessionDeactivated -> PersistenceWriteQueue.Enqueue (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs).
  - Worker drain: PersistenceWorkerLoop.Start -> Run -> PumpOnce -> PersistenceWriteQueue.TryDequeue -> IPersistenceWriter.Execute (CODE/Systems/PersistenceWorkerLoop.cs; CODE/Systems/DeterministicTransportQueues.cs).
  - Completion bridge: PersistenceWorkerLoop.PumpOnce -> PersistenceCompletionQueue.TryEnqueue (CODE/Systems/PersistenceWorkerLoop.cs; CODE/Systems/PersistenceCompletionQueue.cs).
  - Apply-on-tick: PersistenceCompletionPhaseHook.OnPreTick -> PersistenceCompletionQueue.Drain -> PersistenceCompletionApplier.Apply -> PersistenceApplyState.Record (CODE/Systems/PersistenceCompletionQueue.cs; CODE/Systems/PersistenceWorkerLoop.cs).
- Option B (disabled + fail-fast):
  - Default auto mode: HeadlessServerEntryPoint.ResolvePersistenceMode returns Auto; TryConfigurePersistence disables persistence if writer missing (returns true with persistenceSettings null) and logs "Persistence disabled" (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs).
  - Fail-fast gate: if mode == Enabled but writer missing, TryConfigurePersistence returns false with error and host build exits with code 2 (HeadlessServerEntryPoint.Main). This is explicit fail-fast gating (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs).

5) Trust Boundary Audit
- Server stamping exists and is the only ordering source:
  - Stamping site: PooledTransportRouter.EnqueueInbound stamps ServerReceiveSeq (per-session increment) and ServerReceiveTick (Volatile read of _currentReceiveTick) into ServerStampedInboundCommand (CODE/Systems/PooledTransportRouter.cs).
  - Ordering site: AuthoritativeCommandIngress.DrainDeterministic selects by ServerReceiveTick then ServerReceiveSeq (and SessionId tie-break) (CODE/Systems/DeterministicTransportQueues.cs).
- Client tick/seq rejected or treated as metadata only:
  - Rejection site: InboundPumpTickHook.OnPreTick checks envelope.ClientSubmitTick > 0, calls RuntimeGuardrailChecks.AssertNoClientTickOrdering, increments _rejectedClientTickProvided, disposes envelope (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs; CODE/Systems/RuntimeGuardrailChecks.cs).
- Reject counters:
  - InboundPumpDiagnostics.RejectedClientTickProvided (InboundPumpTickHook.Diagnostics).

6) Thread Ownership Enforcement Audit
- Session index:
  - DeterministicActiveSessionIndex uses internal lock for TryAdd/TryRemove/SnapshotSessionsDeterministic (CODE/Systems/DeterministicActiveSessionIndex.cs). No explicit tick-thread assert; thread safety enforced by locking (PARTIAL).
- Visibility/AOI:
  - VisibilityCullingService mutation methods assert tick thread (TickThreadAssert.AssertTickThread) (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs — VisibilityCullingService).
- Replication work contexts:
  - ClientReplicationSnapshotSystem.OnPreTick/OnPostTick/OnSessionDisconnected assert tick thread (RuntimeGuardrailChecks.AssertTickThreadEntry), and session context removal calls SnapshotWorkContext.MarkForRemoval (CODE/Systems/ClientReplicationSnapshotSystem.cs).
- Ingestor/session command state:
  - InboundPumpTickHook.OnPreTick and AuthoritativeCommandConsumeTickHook.OnPreTick assert tick thread (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
  - AuthoritativeCommandIngestor uses lock for TryEnqueue/Freeze/DropSession (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
- Outbound queues:
  - PooledTransportRouter.RouteSnapshot asserts tick thread; TryDequeueOutbound is guarded by _snapshotGate lock (CODE/Systems/PooledTransportRouter.cs). OutboundSendPump runs on its own thread (CODE/Systems/OutboundSendPump.cs).
- Persistence queues/completions:
  - PersistenceWriteQueue uses lock for enqueue/dequeue; PersistenceCompletionQueue.Drain asserts tick thread (CODE/Systems/DeterministicTransportQueues.cs; CODE/Systems/PersistenceCompletionQueue.cs).
- Combat apply path:
  - CombatOutcomeApplicationSystem.Apply asserts tick thread (CODE/Systems/CombatOutcomeApplicationSystem.cs).

7) Disconnect / Shutdown Leak Audit
- Session disconnect:
  - RuntimeServerLoop.OnSessionDisconnected -> TickThreadMailbox.TryEnqueueDisconnect/Unregister/ClearVisibility/CleanupReplication (CODE/Systems/RuntimeServerLoop.cs; CODE/Systems/LifecycleTickMailbox.cs).
  - Tick-thread drain: LifecycleMailboxPhaseHook.OnPreTick -> TickThreadMailbox.Drain -> LifecycleApplier.Apply (CODE/Systems/RuntimeServerLoop.cs).
  - Cleanup actions: PooledTransportRouter.DropAllForSession (inbound/outbound queues disposed), AuthoritativeCommandIngestor.DropSession (returns pooled buffers), SessionHandshakePipeline.Drop, VisibilityCullingService.RemoveSession, ClientReplicationSnapshotSystem.OnSessionDisconnected (marks SnapshotWorkContext for pool return) (CODE/Systems/RuntimeServerLoop.cs; CODE/Systems/PooledTransportRouter.cs; CODE/Systems/RuntimeIntegrationZeroGcHardening.cs; CODE/Systems/SessionHandshakePipeline.cs; CODE/Systems/ClientReplicationSnapshotSystem.cs).
- Shutdown:
  - RuntimeServerLoop.Stop -> PersistenceWorkerLoop.Stop -> OutboundSendPump.Stop -> WorldSimulationCore.Stop -> ClearTransientState (transport.Clear, handshakes.Reset, commands.Clear, visibility.Clear, entities.ClearAll, lifecycleMailbox.Clear, persistence queues cleared) (CODE/Systems/RuntimeServerLoop.cs).
  - ServerRuntimeHost.Dispose unsubscribes TickLoopStarted, disposes runtime loop, simulation, persistence components; no Thread.Abort used (CODE/Systems/RuntimeHost/ServerRuntimeHost.cs).
- Gaps: Invocation sites for RuntimeServerLoop.OnSessionDisconnected from transport are not shown in code (UNKNOWN) and should be verified in real transport integration.

8) Hot-Path Allocation Audit (after warm-up)
- tick + hooks: SOME
  - WorldSimulationCore.ExecuteOneTick calls EnsureCapacity on participant/hook/gate snapshots and eligible arrays; if counts grow after warm-up, new arrays are allocated on the tick thread (CODE/Systems/WorldSimulationCore.cs).
- inbound decode/routing/bridge/freeze/consume: SOME
  - AuthoritativeCommandIngestor.FreezeSessionLocked rents scratch buffers via ArrayPool when null/insufficient; EnsureCapacity can allocate if session counts grow (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
- handshake: NONE
  - SessionHandshakePipeline uses fixed-size ring buffer arrays; no per-tick allocations when within capacity (CODE/Systems/SessionHandshakePipeline.cs).
- replication build/serialize/AOI: SOME
  - ClientReplicationSnapshotSystem creates ClientReplicationSnapshot objects and rents arrays from ArrayPool per snapshot; SnapshotWorkContext can rent/return arrays as entity counts grow (CODE/Systems/ClientReplicationSnapshotSystem.cs).
- persistence trim/drop + worker + apply-on-tick (if enabled): SOME
  - PersistenceApplyState.Record can grow Dictionary<SaveId, PersistenceApplyRecord> as new saves appear (CODE/Systems/PersistenceWorkerLoop.cs). Queue trims are allocation-free but dictionary growth is not explicitly bounded.
- combat staging/resolve/apply: SOME
  - CombatOutcomeApplicationSystem.DeterministicEventId uses string interpolation to allocate event IDs per outcome; PruneAppliedSets rents an int[] from ArrayPool each tick (CODE/Systems/CombatOutcomeApplicationSystem.cs).
- Strings/HashSet in tick loops:
  - CombatOutcomeApplicationSystem creates string event IDs per outcome on tick thread; CombatReplicationSystem allocates per-tick Dictionary/HashSet<string> for delivery guards (CODE/Systems/CombatOutcomeApplicationSystem.cs; CODE/Systems/CombatReplicationSystem.cs).

9) Backpressure Under Pressure Audit
- Inbound transport mailboxes:
  - PooledTransportRouter.EnqueueInbound caps MaxInboundCommandsPerSession and MaxQueuedBytesPerSession; overflow rejects and disposes payload, metrics updated (CODE/Systems/PooledTransportRouter.cs).
  - AuthoritativeCommandIngress.TryEnqueue caps MaxInboundCommandsPerSession and MaxQueuedBytesPerSession; overflow rejects and disposes payload (CODE/Systems/DeterministicTransportQueues.cs).
- Authoritative command ingestor:
  - CommandRing capacity = MaxInboundCommandsPerSession; overflow rejects newest with metrics; buffers pooled, no trim allocations (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).
- Lifecycle mailbox:
  - TickThreadMailbox caps MaxLifecycleOps/MaxLifecycleOpBytes; overflow drops oldest and does not allocate (CODE/Systems/LifecycleTickMailbox.cs).
- Handshake pipeline:
  - SessionHandshakePipeline uses fixed array capacity; queue full rejects (HandshakeRejectionReason.QueueFull) (CODE/Systems/SessionHandshakePipeline.cs).
- Replication outbound queue:
  - BoundedReplicationSnapshotQueue caps MaxOutboundSnapshotsPerSession and MaxQueuedBytesPerSession; EnforceCaps drops oldest, disposes snapshots, metrics/counters updated (CODE/Systems/DeterministicTransportQueues.cs).
- Outbound send pump:
  - OutboundSendPump caps per-session and per-iteration via _maxPerSession/_maxPerIteration (CODE/Systems/OutboundSendPump.cs).
- Persistence write queue:
  - PersistenceWriteQueue caps per-player and global counts/bytes; drop-oldest via EnforceCaps/EnforceGlobalCap; no queue rebuilds, metrics/counters updated (CODE/Systems/DeterministicTransportQueues.cs).
- Persistence completion queue:
  - PersistenceCompletionQueue caps MaxPersistenceCompletions/MaxPersistenceCompletionBytes; drop-oldest and dispose pooled payloads on overflow (CODE/Systems/PersistenceCompletionQueue.cs).
- Combat pipelines:
  - CombatIntentQueueSystem has fixed caps and drop-newest policy, but it is not wired in RuntimeCompositionRoot (UNKNOWN integration for runtime) (CODE/Systems/CombatIntentQueueSystem.cs).

10) Replication Drift Closure Audit
- Runtime session index exists and is used:
  - DeterministicActiveSessionIndex injected into ClientReplicationSnapshotSystem and OutboundSendPump by RuntimeCompositionRoot.Create (CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs; CODE/Systems/DeterministicActiveSessionIndex.cs).
- Outbound drained (not only trimmed):
  - OutboundSendPump.Run/PumpOnce drains via PooledTransportRouter.TryDequeueOutbound and disposes on send failure (CODE/Systems/OutboundSendPump.cs).
- Fingerprints are fixed-size or proven non-churn:
  - BoundedReplicationSnapshotQueue uses Dictionary<EntityHandle, ulong> for per-session fingerprints; no string fingerprints; map is cleared and pooled on DropSession/Clear (CODE/Systems/DeterministicTransportQueues.cs). (Potential growth with entity count remains bounded only by world size; no explicit cap.)
- Pooled buffer ownership explicit:
  - ClientReplicationSnapshot.Dispose returns pooled buffers; SerializedSnapshot.Dispose is invoked on drop paths; PooledPayloadLease.Dispose returns bytes (CODE/Systems/ClientReplicationSnapshotSystem.cs; CODE/Systems/DeterministicTransportQueues.cs).

11) Combat Drift Closure Audit (verify the micro-fix)
- No HashSet<string> created/used per tick in combat apply path: CLOSED for apply path (CombatOutcomeApplicationSystem uses HashSet<ulong> and reuses it); however combat replication uses HashSet<string> per tick (see Failure Mode 12) (CODE/Systems/CombatOutcomeApplicationSystem.cs; CODE/Systems/CombatReplicationSystem.cs).
- No string payload IDs in combat apply hot paths: PARTIAL — CombatOutcomeApplicationSystem.CreateIntentResultEvent uses DeterministicEventId with string payloadId (intentId) and string interpolation per event (CODE/Systems/CombatOutcomeApplicationSystem.cs).
- Apply enforces tick-thread ownership: CLOSED — CombatOutcomeApplicationSystem.Apply calls TickThreadAssert.AssertTickThread (CODE/Systems/CombatOutcomeApplicationSystem.cs).
- Caps/metrics exist and enforced deterministically: CLOSED — MaxTrackedPayloadIdsPerTick enforces idempotence cap and metrics track overflow/duplicates (CombatOutcomeApplicationSystem.TryRegisterPayloadId).

12) Risk Register (recurring-issue related only)
- P1 — Failure Mode 12 — CODE/Systems/CombatOutcomeApplicationSystem.cs (CombatEvent.DeterministicEventId)
  - Why: String event IDs and string payload ID usage in apply path create per-event allocations and violate “no string payload IDs in hot loops.”
  - Minimal fix strategy (audit-only): Replace event ID generation with fixed-size numeric IDs (e.g., ulong) derived from hashed intent/outcome IDs and tick; avoid string interpolation on tick thread.
- P1 — Failure Mode 12 — CODE/Systems/CombatReplicationSystem.cs (BeginTick/MarkDelivered)
  - Why: Per-tick Dictionary/HashSet<string> allocations for delivery guards violate low/zero-GC steady state and “no HashSet<string> per tick” drift rule.
  - Minimal fix strategy (audit-only): Use pooled HashSet<ulong> (or fixed-size ring/bitset keyed by numeric event ID) and reuse per session across ticks with explicit Clear.
- P2 — Failure Mode 9 — CODE/Systems/WorldSimulationCore.cs (ExecuteOneTick EnsureCapacity)
  - Why: Tick thread can allocate new arrays if participant/hook/gate counts or entity counts grow after warm-up.
  - Minimal fix strategy (audit-only): Pre-register all hooks/participants before Start and pre-size snapshots to max expected counts; prevent post-start registration growth.
- P2 — Failure Mode 9 — CODE/Systems/ClientReplicationSnapshotSystem.cs (CaptureSnapshotForSession / SnapshotWorkItem.BuildSnapshot)
  - Why: Creates new ClientReplicationSnapshot objects and rents arrays per tick; GC pressure may accumulate under load without pooling of snapshot objects.
  - Minimal fix strategy (audit-only): Pool ClientReplicationSnapshot objects or move to struct + pooled buffers; verify pool sizing against expected max sessions/entities.
- P2 — Failure Mode 7 — CODE/Systems/TimeSlicedWorkScheduler.cs (ExecuteSlices)
  - Why: Tick-thread ownership is assumed but not asserted; no explicit guard in scheduler itself.
  - Minimal fix strategy (audit-only): Add tick-thread assertion at ExecuteSlices entry or centralize time-slicer usage under a guard-railed wrapper.

APPENDIX A — Evidence Table (MANDATORY)
| Severity | Failure Mode # | Subsystem | File | Type/Method | Finding | Evidence summary |
|---|---|---|---|---|---|---|
| P1 | 12 | Combat apply | CODE/Systems/CombatOutcomeApplicationSystem.cs | CombatEvent.DeterministicEventId | String payload IDs and string interpolation in apply path | CreateIntentResultEvent -> DeterministicEventId(int, CombatEventType, string) builds "$\"ce:{tick}:{(int)type}:{payloadId}\"" per event; Apply emits events on tick thread. |
| P1 | 12 | Combat replication | CODE/Systems/CombatReplicationSystem.cs | BeginTick/MarkDelivered | HashSet<string> per tick | BeginTick clears map and creates new Dictionary<ClientId, HashSet<string>> each tick; MarkDelivered allocates new HashSet<string> for client on first event. |
| P2 | 9 | Tick core | CODE/Systems/WorldSimulationCore.cs | ExecuteOneTick/EnsureCapacity | Potential per-tick allocations on growth | ExecuteOneTick calls EnsureCapacity for participant/hook/gate snapshots and eligible arrays; new arrays allocated if counts increase after warm-up. |
| P2 | 9 | Replication | CODE/Systems/ClientReplicationSnapshotSystem.cs | CaptureSnapshotForSession / SnapshotWorkItem.BuildSnapshot | Per-tick allocations of snapshot objects/arrays | Builds new ClientReplicationSnapshot objects and rents arrays from ArrayPool per tick; object allocations are unavoidable in current implementation. |
| P2 | 7 | Threading | CODE/Systems/TimeSlicedWorkScheduler.cs | ExecuteSlices | Tick-thread ownership assumed, not enforced | No TickThreadAssert/RuntimeGuardrailChecks in scheduler; relies on call sites for correctness. |

APPENDIX B — Search Notes (MANDATORY)
- Directories searched:
  - /workspace/Caelmor-Repo/CODE/Systems
  - /workspace/Caelmor-Repo/00_ADMIN/Reference (MMO Runtime & Compilation Technical Brief)
- All grep terms used:
  - Allocation terms: "System.Linq", "new List<", "new Dictionary<", "new Queue<", "new byte[", "Action", "delegate", "=>", ".Select(", ".Where(", ".OrderBy(", ".ToArray(", "string.Format", "$\"", "ReadOnlyCollection", "IEnumerable", "HashSet<"
  - Blocking terms: "Thread.Sleep", ".Wait()", ".Result", "Task.Wait", "Monitor.Wait", "File.", "Stream", "ReadAll", "WriteAll"
  - AOT risk terms: "Reflection.Emit", "DynamicMethod", "Expression.Compile", "Activator.CreateInstance"
  - Leak risk terms: "static", "+=", "-=", "event", "IDisposable", "Dispose("
- Limitations encountered:
  - No runtime transport implementation found beyond InProcTransportAdapter; real network ingest/outbound integration call sites remain UNKNOWN.
