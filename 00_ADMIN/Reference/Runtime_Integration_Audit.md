# Runtime Integration Audit

## 1) Executive Summary
- **System Code Complete:** NO — transport/handshake/command ingress are present as components but not wired into the tick lifecycle, and persistence I/O workers are absent.
- **Top 5 Risks (ordered)**
  1. **P0 — Command ingestion not integrated with tick freeze** (Authoritative input): `AuthoritativeCommandIngestor` is never drained or bound to tick boundaries, so accepted commands can accumulate or starve the simulation, violating the MMO brief’s deterministic per-tick mutation window. Evidence: the type only exists and is referenced by `RuntimeServerLoop`, but no tick participant or phase hook drains it. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L15-L93】【F:CODE/Systems/RuntimeServerLoop.cs†L17-L117】
  2. **P0 — Snapshot work contexts never released** (Replication/GC): `ClientReplicationSnapshotSystem` caches per-session `SnapshotWorkContext` entries in a `ConcurrentDictionary` with no removal on disconnect, creating unbounded memory growth over long uptimes. Violates the brief’s GC/pooling and long-uptime stability guardrails. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L25-L170】【F:CODE/Systems/RuntimeServerLoop.cs†L89-L111】
  3. **P1 — Handshake queue lacks deterministic service loop** (Session lifecycle): `SessionHandshakePipeline` provides bounded enqueue but there is no scheduler hook to process handshakes on the tick thread, so sessions may never activate. This breaks authoritative onboarding and deterministic ordering in the MMO brief. 【F:CODE/Systems/SessionHandshakePipeline.cs†L1-L132】【F:CODE/Systems/RuntimeServerLoop.cs†L17-L117】
  4. **P1 — Persistence write queue has no byte caps and drops rebuild the queue** (Persistence I/O): `PersistenceWriteQueue` enforces only count-based caps and rebuilds the global queue when trimming, allocating per drop and ignoring payload sizes; risk of GC churn and runaway memory when writes are large, violating zero-GC/backpressure guidance. 【F:CODE/Systems/DeterministicTransportQueues.cs†L620-L771】
  5. **P1 — Combat intent staging allocates per tick with no caps** (Authoritative commands): `CombatIntentQueueSystem` creates new per-tick staging lists without bounds or pooling; under load this introduces steady allocations and unbounded growth, breaching the brief’s zero/low-GC and bounded-queue requirements. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L23-L145】

## 2) Closure of Prior Missing Systems
- **Networking Transport & Message Routing**
  - **Status:** Partially implemented. Inbound/outbound routing, caps, and pooled buffers exist, but no transport thread loop is present to call `RouteQueuedInbound`/`TryDequeueOutbound`.
  - **Where:** `PooledTransportRouter`, `DeterministicTransportRouter`, `BoundedReplicationSnapshotQueue`. 【F:CODE/Systems/PooledTransportRouter.cs†L1-L203】【F:CODE/Systems/DeterministicTransportQueues.cs†L174-L365】
  - **Entry points:** `EnqueueInbound`, `RouteQueuedInbound` (tick thread), `RouteSnapshot`, `TryDequeueOutbound`.
  - **Thread:** Intended network threads enqueue/dequeue; tick thread should drain inbound/outbound via deterministic router, but the caller is absent (UNKNOWN: no loop found under `CODE/Systems`).
  - **Guardrails:** Per-session caps and pooling present; missing driver risks backlog and determinism because routing is never invoked.

- **Connection/Session Handshake Pipeline**
  - **Status:** Partially implemented; bounded ring exists but no tick-thread drain wiring.
  - **Where:** `SessionHandshakePipeline`. 【F:CODE/Systems/SessionHandshakePipeline.cs†L1-L132】
  - **Entry points:** `TryEnqueue`, `TryProcessNext`, `Drop`, `Reset`.
  - **Thread:** Intended enqueue on transport thread; processing must be tick thread but no scheduler calls were found (UNKNOWN caller).
  - **Guardrails:** Bounded ring satisfies backpressure; lack of processing path violates deterministic activation and mid-tick mutation gating.

- **World Bootstrap & Zone Startup**
  - **Status:** Partially implemented; deterministic registration helper and host start/stop exist, but no zone loading or participant list provided.
  - **Where:** `WorldBootstrapRegistration`, `ServerRuntimeHost`. 【F:CODE/Systems/WorldBootstrapRegistration.cs†L1-L61】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L510-L545】
  - **Entry points:** `WorldBootstrapRegistration.Apply`, `ServerRuntimeHost.Start/Stop`.
  - **Thread:** Tick thread created inside `WorldSimulationCore.Start`; host start is manual.
  - **Guardrails:** Deterministic ordering and no reflection (AOT-safe) satisfied; missing concrete registrations leaves simulation incomplete.

- **Entity Registry / World State Container**
  - **Status:** Implemented.
  - **Where:** `DeterministicEntityRegistry` implements `IEntityRegistry`/`ISimulationEntityIndex`. 【F:CODE/Systems/DeterministicEntityRegistry.cs†L1-L110】
  - **Entry points:** `Register`, `Unregister`, `DespawnZone`, `SnapshotEntitiesDeterministic`.
  - **Thread:** Tick thread expected (methods are lock-protected); no off-thread mutation in code.
  - **Guardrails:** Stable ordering via sort, zone cleanup, and ClearAll on shutdown; pooling not required (arrays reused). Meets determinism/duplication guardrail.

- **Authoritative Input Command Ingestion**
  - **Status:** Partially implemented; ring buffer exists but not connected to transport/tick participants and lacks metrics.
  - **Where:** `AuthoritativeCommandIngestor`. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L15-L93】
  - **Entry points:** `TryEnqueue`, `TryDrain`, `DropSession`, `Clear`.
  - **Thread:** Intended tick-thread drain; enqueue site unknown. No evidence of freeze-per-tick batching.
  - **Guardrails:** Fixed capacity (32) without configuration or drop reporting breaks backpressure and determinism under load.

- **Interest Management / Visibility Culling**
  - **Status:** Implemented.
  - **Where:** `ZoneSpatialIndex`, `VisibilityCullingService`. 【F:CODE/Systems/ZoneSpatialIndex.cs†L1-L156】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L95-L226】
  - **Entry points:** `Upsert`, `Remove`, `Query` (index); `Track`, `RefreshVisibility`, `IsEntityReplicationEligible`, `QueryNearbyTargets` (visibility).
  - **Thread:** Tick thread only; no thread-safe guards, assumes authoritative simulation thread.
  - **Guardrails:** Deterministic ordering via sorted handles, pooled buffers, bounded reuse; complies with AOI and zero-GC brief.

- **Snapshot Serialization & Delta Format**
  - **Status:** Implemented (delta + pooled serializer, queued per session).
  - **Where:** `SnapshotDeltaSerializer`, `SnapshotSerializer`, `BoundedReplicationSnapshotQueue`. 【F:CODE/Systems/DeterministicTransportQueues.cs†L808-L1033】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L228-L339】
  - **Entry points:** `BoundedReplicationSnapshotQueue.Enqueue/TryDequeue`, `SnapshotDeltaSerializer.Serialize`, `SnapshotSerializer.Serialize`.
  - **Thread:** Tick thread for enqueue/serialize; transport thread for dequeue. Pooled buffers returned via `SerializedSnapshot.Dispose`.
  - **Guardrails:** Caps enforced on count/bytes; deterministic ordering and pooling present.

- **Persistence IO Hooks**
  - **Status:** Partially implemented; completion mailbox and write queue exist but no I/O worker or apply paths beyond generic interfaces.
  - **Where:** `PersistenceCompletionQueue`, `PersistenceWriteQueue`, `PersistenceCompletionPhaseHook`. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L147】【F:CODE/Systems/DeterministicTransportQueues.cs†L620-L771】
  - **Entry points:** `TryEnqueue` (off-thread), `Drain` via phase hook, `Enqueue/TryDequeue` (write queue).
  - **Thread:** Completion drain must run on tick thread (phase hook provided); persistence worker not present (UNKNOWN).
  - **Guardrails:** Completion queue has caps/drop-oldest and pooled payload disposal; write queue lacks byte caps and allocates during drops (risk).

- **Server Logging & Diagnostics**
  - **Status:** Implemented.
  - **Where:** `TickDiagnostics`, stall watchdog, queue diagnostics via `TransportBackpressureDiagnostics` and completion metrics. 【F:CODE/Systems/TickDiagnostics.cs†L1-L210】【F:CODE/Systems/RuntimeServerLoop.cs†L117-L154】【F:CODE/Systems/DeterministicTransportQueues.cs†L365-L456】
  - **Entry points:** `RecordTick`, `ConfigureStallWatchdog`, `CaptureDiagnostics`.
  - **Thread:** Tick-thread safe via interlocked; watchdog uses timer thread only for detection.
  - **Guardrails:** Allocation-free hot path; meets MMO brief for stall detection and queue budgets.

- **Runtime Loop Entrypoint / Build Script**
  - **Status:** Partially implemented; loop coordinator exists but lacks per-tick orchestration of transport/handshake/commands.
  - **Where:** `RuntimeServerLoop`, `ServerRuntimeHost`. 【F:CODE/Systems/RuntimeServerLoop.cs†L1-L154】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L510-L545】
  - **Entry points:** `Start/Stop/ShutdownServer`, `OnSessionDisconnected`, `OnZoneUnloaded`, `CaptureDiagnostics`.
  - **Thread:** Starts simulation threads only; no tick-phase callbacks wiring transport/handshake.
  - **Guardrails:** Deterministic start/stop and cleanup present; missing orchestration breaks the end-to-end runtime loop.

## 3) Tick Discipline & Determinism
- **Phases:** `WorldSimulationCore` enforces Pre-Tick eligibility (gates snapshot, `EvaluateEligibility`), Simulation Execution (participants ordered by `OrderKey` then registration seq), and Post-Tick Finalization (eligibility stability check + effect commit + phase hooks). 【F:CODE/Systems/WorldSimulationCore.cs†L94-L223】【F:CODE/Systems/WorldSimulationCore.cs†L270-L343】
- **Tick rate:** 10 Hz fixed (100 ms). Catch-up capped at 3 ticks; clamping records overruns. 【F:CODE/Systems/WorldSimulationCore.cs†L24-L86】
- **Mutation windows:** Effect buffering (`SimulationEffectBuffer`) enforces commit only in Post-Tick; mid-tick eligibility mutation throws. 【F:CODE/Systems/WorldSimulationCore.cs†L271-L343】【F:CODE/Systems/WorldSimulationCore.cs†L345-L444】
- **Deterministic ordering:** Entities sorted in `DeterministicEntityRegistry`; participants/hooks sorted; snapshots sorted by entity handle and fingerprint delta; visibility sorted. 【F:CODE/Systems/DeterministicEntityRegistry.cs†L92-L110】【F:CODE/Systems/WorldSimulationCore.cs†L153-L214】【F:CODE/Systems/DeterministicTransportQueues.cs†L888-L1033】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L135-L220】
- **Nondeterminism sources:**
  - Ingress/handshake not scheduled => ordering undefined (commands/joins processed opportunistically or never). Evidence: no caller for `RouteQueuedInbound`/`TryProcessNext`.
  - `PersistenceWriteQueue` drops rebuild global queue using new `Queue`, introducing allocation and potential order changes when caps trigger. 【F:CODE/Systems/DeterministicTransportQueues.cs†L654-L711】
  - Snapshot work contexts never removed, so ordering of `_workContexts` iteration (ConcurrentDictionary) is unspecified though used only for caching; risk is growth, not ordering.

## 4) Allocation & GC Risk Audit (Zero/Low GC)
- **Tick loop execution:** `WorldSimulationCore` and `TickSystem` reuse buffers; `SimulationEffectBuffer` preallocates list (512). No LINQ/strings in hot path. Thread.Sleep/SpinWait used for cadence only. 【F:CODE/Systems/WorldSimulationCore.cs†L24-L214】【F:CODE/Systems/TickSystemCore.cs†L24-L214】
- **Command ingestion/drain:** `AuthoritativeCommandIngestor` uses fixed array ring per session (no pooling but no per-drain allocations). Missing drain path means retained commands can build up. Transport ingress uses pooled payload leases; dictionary allocations only at session creation. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L15-L93】【F:CODE/Systems/DeterministicTransportQueues.cs†L26-L215】
- **Snapshot building/serialization:** `ClientReplicationSnapshotSystem` rents arrays from pools; per-session scratch arrays cached; `SnapshotDeltaSerializer` uses ArrayPool<byte>. Risk: `_workContexts` never cleared → pooled buffers retained; `SnapshotSerializer.EnsureCapacity` reallocates when fingerprint strings exceed estimate. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L47-L170】【F:CODE/Systems/DeterministicTransportQueues.cs†L888-L1033】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L228-L339】
- **AOI queries/spatial index:** `ZoneSpatialIndex.Query` appends to caller-provided list; `VisibilityCullingService.RefreshVisibility` rents from `ArrayPool` and reuses buckets. Minimal steady allocations. 【F:CODE/Systems/ZoneSpatialIndex.cs†L73-L134】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L115-L180】
- **Queue operations per tick:** Transport queues reuse dictionaries/queues; completion queue reuses Queue with drop-oldest; write queue rebuilds queue when dropping (allocations). Combat intent staging allocates new `List` per submit tick and deep-freezes payload per intent. 【F:CODE/Systems/DeterministicTransportQueues.cs†L365-L520】【F:CODE/Systems/DeterministicTransportQueues.cs†L620-L711】【F:CODE/Systems/CombatIntentQueueSystem.cs†L63-L145】
- **Warm-up vs. steady-state:**
  - Warm-up: initial queue/dictionary creation per session, initial ArrayPool rents during first snapshots.
  - Steady-state allocations: combat intent staging lists; persistence write drops rebuild global queue; snapshot serializer buffer growth on underestimate; absence of work-context cleanup causing heap retention.

## 5) Pooling Ownership & Safety
- **Payload buffers:** `PooledPayloadLease` and `SerializedSnapshot` are owned by queues; dispose returns ArrayPool buffers and is idempotent. Drop paths call `Dispose` before eviction. 【F:CODE/Systems/DeterministicTransportQueues.cs†L26-L168】【F:CODE/Systems/DeterministicTransportQueues.cs†L965-L1033】
- **Visibility caches:** `VisibilityBucket.Release` returns rented arrays; `RemoveSession`/`Clear` ensure return. Risk: caller must remember to call `RemoveSession` on disconnect (handled by `RuntimeServerLoop.OnSessionDisconnected`). 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L140-L226】【F:CODE/Systems/RuntimeServerLoop.cs†L101-L113】
- **Snapshot pooling:** `ClientReplicationSnapshot` uses ArrayPool-backed buffers with disposal callback; `_workContexts` retain rented arrays indefinitely without session cleanup (ownership leak).
- **Persistence completions:** Mailbox disposes payloads on drop/drain; ownership explicit in `PersistenceCompletion.Dispose`. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L109】
- **Risks:** Double-return protection exists via idempotent disposables; main hazard is leaked ownership when sessions terminate (snapshot work contexts, command rings if `DropSession` not called via runtime loop).

## 6) Bounded Growth & Backpressure
- **Inbound commands:** `PooledTransportRouter` enforces `MaxInboundCommandsPerSession` and `MaxQueuedBytesPerSession`; rejects overflow with metrics. `AuthoritativeCommandIngestor` ring is fixed-size (implicit cap) but silent drop (TryEnqueue false) and not config-driven. 【F:CODE/Systems/PooledTransportRouter.cs†L29-L140】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L15-L93】
- **Outbound snapshots:** `BoundedReplicationSnapshotQueue` caps per session on count/bytes, drops oldest deterministically. 【F:CODE/Systems/DeterministicTransportQueues.cs†L365-L520】
- **Persistence writes/completions:** Write queue caps per player/global by count only; no byte cap; drops rebuild queue (allocations). Completion queue caps count/bytes and drops oldest with metrics. 【F:CODE/Systems/DeterministicTransportQueues.cs†L620-L711】【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L109】
- **Handshake/session state:** `SessionHandshakePipeline` bounded by fixed capacity; `PlayerSessionSystem` dictionaries guarded but unbounded session count (expected; relies on proper deactivation). 【F:CODE/Systems/SessionHandshakePipeline.cs†L19-L96】【F:CODE/Systems/PlayerSessionSystem.cs†L20-L137】
- **Metrics:** Ingress/egress and completion queues expose budget snapshots; command ingestor and handshake queues lack drop counters.
- **Unbounded structures flagged:** `_workContexts` in `ClientReplicationSnapshotSystem` (per session, never removed); combat intent staging dictionary grows with every tick key until pruned (keep last 4 ticks but allocates new lists per tick). 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L55-L170】【F:CODE/Systems/CombatIntentQueueSystem.cs†L63-L145】

## 7) Thread Boundary Contract
- **Tick/Simulation thread:** `WorldSimulationCore` (captures tick thread via `TickThreadAssert`), participants, eligibility, phase hooks, and effect commits run here. `TickSystem` also owns dedicated thread (redundant loop) but not integrated. 【F:CODE/Systems/WorldSimulationCore.cs†L59-L153】【F:CODE/Systems/TickSystemCore.cs†L52-L118】
- **Transport thread(s):** Expected to enqueue inbound (`PooledTransportRouter.EnqueueInbound`) and dequeue outbound; not present in code.
- **Persistence worker:** Expected off-thread producer for `PersistenceCompletionQueue.TryEnqueue`; absent.
- **Safety checks:** `TickThreadAssert` debug-only; transport queues lock-based; completion drain asserts tick thread. No UnityEngine access off-thread.
- **Violations/Missing wiring:** No authoritative mutation observed off tick thread, but missing orchestration means handshakes/ingress may run on arbitrary threads if callers misuse. Need explicit scheduler binding.

## 8) I/O & Blocking Calls
- **Blocking waits:** Tick loops use `Thread.Sleep`/`SpinWait` for cadence; acceptable but note potential jitter if host thread preempted. 【F:CODE/Systems/WorldSimulationCore.cs†L57-L111】【F:CODE/Systems/TickSystemCore.cs†L57-L112】
- **File/Network I/O:** None in codebase; persistence/transport hooks are abstractions only. No synchronous file access found (`rg File.` returned none).
- **Locks:** Bounded usage in transport router, handshakes, registries; no evidence of long-held locks on tick thread except snapshot enqueue (short critical sections). Monitor usage absent.

## 9) AOT/IL2CPP Safety Audit
- **Dynamic codegen:** None found; files explicitly warn against Reflection.Emit and use deterministic registration helpers. Searches for `Reflection.Emit/DynamicMethod/Assembly.Load` yielded only comments. 【F:CODE/Systems/DeterministicTransportQueues.cs†L458-L480】【F:CODE/Systems/RuntimeServerLoop.cs†L11-L23】
- **Reflection-heavy discovery:** None; `WorldBootstrapRegistration` requires explicit registration (AOT-safe). 【F:CODE/Systems/WorldBootstrapRegistration.cs†L1-L61】
- **Stripping hazards:** Interfaces/classes are concrete and referenced; no reliance on reflection-based activation detected. Snapshot serializer uses `Encoding.UTF8` only.

## 10) Observability & Ops Readiness
- **Tick metrics:** Min/max/avg tick durations, overruns, catch-up clamps, stall counts tracked allocation-free. Stall watchdog present. 【F:CODE/Systems/TickDiagnostics.cs†L1-L210】
- **Queue metrics:** Ingress/snapshot budgets, persistence completion metrics exposed via diagnostics snapshots. 【F:CODE/Systems/RuntimeServerLoop.cs†L117-L154】【F:CODE/Systems/DeterministicTransportQueues.cs†L365-L456】【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L109】
- **Missing signals:** No metrics for handshake queue saturation, command ring drops, or combat intent rejects. No tick duration publishing to external monitoring; TimeSlicedWorkScheduler only increments deferral counter.
- **Allocation-free logging:** No per-tick string formatting; diagnostics snapshots avoid allocations.

## 11) Security / Trust Boundaries (Authoritative Server Hygiene)
- **Identifier issuance:** `PlayerSessionSystem` rejects client-provided IDs via `ClientIdentifierRejectionGuards` and only accepts server-issued `SessionId/PlayerId`. 【F:CODE/Systems/PlayerSessionSystem.cs†L38-L92】
- **Command validation:** Combat intent ingestion performs structural validation (`CombatIntentStructuralValidator`) before staging; other command channels (generic `AuthoritativeCommandIngestor`) accept raw ints with no schema validation. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L47-L109】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L15-L93】
- **Out-of-window commands:** Combat intents freeze per tick; generic ingress lacks submit-window enforcement (no tie to tick index).
- **Routing authority:** Transport router rejects invalid SessionId and does not mutate routing tables off-thread; snapshot routing uses authoritative SessionId tokens. 【F:CODE/Systems/PooledTransportRouter.cs†L38-L140】
- **Gaps:** Handshake queue not processed ⇒ clients may never become authoritative sessions; command ingestor lacks validation/dedupe; persistence completion queue accepts any payload length up to config without schema verification.

## 12) Risk Register & Next Actions
- **P0 — Wire authoritative ingestion into tick loop:** Add a tick-phase hook or participant that drains `AuthoritativeCommandIngestor` per session each tick (freeze semantics), applies deterministic ordering, and emits drop metrics. Violates MMO brief: deterministic per-tick mutation and backpressure. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L15-L93】【F:CODE/Systems/RuntimeServerLoop.cs†L17-L117】
- **P0 — Clean up replication work contexts on disconnect:** Track session lifecycle events and remove `_workContexts` entries when sessions end; assert disposal of pooled buffers to prevent long-uptime GC growth. Violates MMO brief: pooling/long-uptime stability. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L55-L170】【F:CODE/Systems/RuntimeServerLoop.cs†L101-L113】
- **P1 — Provide scheduler for handshake pipeline:** Register a tick-phase hook that drains `SessionHandshakePipeline.TryProcessNext` deterministically each tick; add metrics for queue full drops. Addresses MMO brief: authoritative onboarding and deterministic routing. 【F:CODE/Systems/SessionHandshakePipeline.cs†L19-L96】
- **P1 — Add byte-aware caps to persistence writes:** Extend `PersistenceWriteQueue` to enforce byte budgets and avoid rebuilding queues during drops (reuse pooled structures). Addresses MMO brief: backpressure and zero/low GC. 【F:CODE/Systems/DeterministicTransportQueues.cs†L620-L711】
- **P1 — Bound combat intent staging allocations:** Introduce pooled buffers or fixed-cap ring per tick (by actor) and add drop/backpressure policy to avoid unbounded lists. Addresses MMO brief: low-GC authoritative command intake. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L63-L145】
- **P2 — Expose ops metrics for handshakes/commands:** Emit counters for handshake enqueue/drops and command ring overflows; surface via `RuntimeDiagnosticsSnapshot`. Supports MMO ops readiness.

---

## APPENDIX A — Evidence Table
| Severity | Subsystem | File | Type/Method | Finding | MMO Brief Principle Violated | Suggested Fix |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | Command ingestion | RuntimeIntegrationZeroGcHardening.cs | `AuthoritativeCommandIngestor` | Ring buffer has no tick-thread drain or metrics; commands may queue indefinitely or drop silently | Deterministic tick mutation & backpressure | Add tick-phase drain, deterministic ordering, and overflow counters tied to config |
| P0 | Replication | ClientReplicationSnapshotSystem.cs | `_workContexts` caching | Per-session work contexts never removed, causing unbounded memory over long uptime | GC/pooling, long-uptime stability | Remove contexts on disconnect; validate disposal of pooled buffers |
| P1 | Handshake | SessionHandshakePipeline.cs | `TryProcessNext` (unused) | No scheduler calls to process handshake queue deterministically | Session lifecycle determinism | Add tick-phase hook to drain queue each tick with metrics |
| P1 | Persistence | DeterministicTransportQueues.cs | `PersistenceWriteQueue.EnforceCaps` | Caps ignore bytes; dropping rebuilds queue, allocating per drop | Backpressure, zero/low GC | Track byte budgets and drop without rebuilding queues; reuse pooled buffers |
| P1 | Combat intents | CombatIntentQueueSystem.cs | `FreezeForTick`/`PruneStaging` | Per-tick staging allocates new lists without caps; no backpressure | Low-GC authoritative ingestion | Use pooled buffers/rings with caps and drop policy |

## APPENDIX B — Search/Review Notes
- Searched for `System.Linq`, `new List<`, `new Dictionary<`, `new byte[`, `Action`, `ConcurrentQueue`, `lock`, `Monitor`, `File.`, `Stream`, `Thread.Sleep`, `Task.Wait`/`.Result`, `Reflection.Emit`/`DynamicMethod` using `rg` under `CODE/Systems`.
- Manually reviewed tick/transport/handshake/replication/persistence systems for thread boundaries, pooling, and determinism.
