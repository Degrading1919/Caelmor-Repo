# Runtime Integration Audit

## 1) Executive Summary
- **System Code Complete:** NO — ingress/egress drivers and persistence I/O wiring remain absent, so authoritative commands and outbound snapshots are never serviced on the tick thread and persistence writes never leave their queues.
- **Top 7 Risks (ordered)**
  1. **P0 — Transport ingress never drained on the tick thread** (Transport): `PooledTransportRouter.RouteQueuedInbound` provides deterministic draining, but no caller exists in the runtime loop or tick hooks, so inbound payloads accumulate or get dropped without ever reaching authoritative processing. 【F:CODE/Systems/PooledTransportRouter.cs†L23-L207】【F:CODE/Systems/RuntimeServerLoop.cs†L64-L202】
  2. **P0 — Command ingress is not bridged to the tick-freeze ingestor** (Authoritative input): `AuthoritativeCommandIngress.TryEnqueue/TryDequeue` buffers payloads, while `AuthoritativeCommandIngestor.FreezeSessions` freezes commands for simulation, but no code pulls envelopes from ingress into the ingestor; buffered commands will never reach the frozen batches. 【F:CODE/Systems/DeterministicTransportQueues.cs†L84-L181】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L16-L169】
  3. **P1 — Outbound snapshot dequeue driver is missing** (Transport egress): `DeterministicTransportRouter.TryDequeueSnapshot` is transport-thread only, yet no loop or tick hook calls it; outbound snapshots will accumulate in bounded queues until trimmed, causing client starvation or drops. 【F:CODE/Systems/DeterministicTransportQueues.cs†L462-L519】【F:CODE/Systems/RuntimeServerLoop.cs†L64-L202】
  4. **P1 — Persistence write queue has no worker** (Persistence): `PersistenceWriteQueue` now enforces byte+count caps, but nothing dequeues records to an I/O worker or enqueues completions; persistence requests will pile up and be trimmed instead of written. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L1010】【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】
  5. **P1 — Combat intent freezing allocates per intent** (Combat): `PayloadFreezer.DeepFreeze` creates new dictionaries/lists for every submission each tick, which violates the zero/low-GC guardrail in steady load even though staging is capped. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L848-L912】
  6. **P1 — No authoritative handoff from ingress sequencing to simulation** (Authoritative input ordering): Ingress sequencing (submit tick + deterministic sequence) is isolated inside `AuthoritativeCommandIngress` and never reconciled with the command freeze hook, so authoritative ordering across sessions remains undefined. 【F:CODE/Systems/DeterministicTransportQueues.cs†L84-L181】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L401-L443】
  7. **P2 — Visibility/replication systems assume tick thread but lack enforcement** (Replication/AOI): `VisibilityCullingService` and `ClientReplicationSnapshotSystem` assume tick-thread-only access without explicit asserts at all call sites, so off-thread misuse could corrupt caches without detection. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L581-L740】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L91-L125】

## 2) Runtime Pipeline Overview (end-to-end)
- **Startup/boot:** `RuntimeServerLoop.Create` registers eligibility gates, participants, and phase hooks, then `Start` boots `WorldSimulationCore`’s tick thread (10 Hz). 【F:CODE/Systems/RuntimeServerLoop.cs†L64-L123】【F:CODE/Systems/WorldSimulationCore.cs†L19-L131】
- **Handshake intake:** Transport thread enqueues into `SessionHandshakePipeline.TryEnqueue`; tick thread is supposed to service via `HandshakeProcessingPhaseHook` (pre-tick). 【F:CODE/Systems/SessionHandshakePipeline.cs†L43-L182】【F:CODE/Systems/SessionHandshakePipeline.cs†L226-L258】
- **Session activation:** `TryProcessNext` activates sessions through `IPlayerSessionSystem` and notifies onboarding hooks; runs only when the phase hook is invoked. 【F:CODE/Systems/SessionHandshakePipeline.cs†L66-L101】
- **Inbound transport → authoritative ingestion:** Transport threads enqueue via `PooledTransportRouter.EnqueueInbound` → `DeterministicTransportRouter.RouteInbound` → `AuthoritativeCommandIngress`. **MISSING:** no tick hook/loop calls `RouteQueuedInbound` or drains `AuthoritativeCommandIngress` into `AuthoritativeCommandIngestor`. 【F:CODE/Systems/PooledTransportRouter.cs†L52-L153】【F:CODE/Systems/DeterministicTransportQueues.cs†L84-L181】
- **Command freeze (ingestion freeze):** `AuthoritativeCommandFreezeHook.OnPreTick` freezes per-session rings each tick; ordering is deterministic by session and sequence. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L401-L443】
- **Simulation tick phases:** `WorldSimulationCore.ExecuteOneTick` runs (1) pre-tick hooks, (2) participants per eligible entity, (3) post-tick hooks, with mid-tick eligibility invariants enforced. 【F:CODE/Systems/WorldSimulationCore.cs†L261-L333】
- **Replication snapshot build:** Post-tick hook `ClientReplicationSnapshotSystem.OnPostTick` schedules time-sliced snapshot work, which enqueues snapshots to the replication queue. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L98-L125】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L340-L396】
- **AOI gate:** `VisibilityCullingService` provides `IsEntityReplicationEligible` during snapshot capture; it is updated by simulation systems off this file (tick-thread assumed). 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L581-L665】
- **Outbound queue:** Snapshots enter `BoundedReplicationSnapshotQueue` via `DeterministicTransportRouter.RouteSnapshot`. **MISSING:** no transport thread driver calls `TryDequeueSnapshot` to send to clients. 【F:CODE/Systems/DeterministicTransportQueues.cs†L462-L519】
- **Persistence queue:** `PersistenceWriteQueue.Enqueue` supports caps; **MISSING:** no worker drains via `TryDequeue`, and completions are only applied if an external worker enqueues `PersistenceCompletion` entries. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L1010】【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】
- **Apply-on-tick completion:** `PersistenceCompletionPhaseHook` would drain completions pre-tick, returning pooled payloads. Only wired when provided at construction. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】【F:CODE/Systems/RuntimeServerLoop.cs†L80-L110】
- **Shutdown:** `RuntimeServerLoop.Stop/ShutdownServer` stops the simulation thread and clears caches/registries. 【F:CODE/Systems/RuntimeServerLoop.cs†L125-L202】

## 3) Tick Discipline & Determinism
- **Authoritative tick driver:** `WorldSimulationCore.RunLoop` (10 Hz, max 3 catch-up ticks, clamped) with stall watchdog. 【F:CODE/Systems/WorldSimulationCore.cs†L192-L259】
- **Tick phases (order):** Pre-tick hooks → simulation participants per eligible entity → post-tick hooks; eligibility snapshot taken once and verified for stability. 【F:CODE/Systems/WorldSimulationCore.cs†L261-L333】
- **Command drain+freeze:** `AuthoritativeCommandFreezeHook.OnPreTick` runs once per tick (hook registered with lowest order key) to freeze per-session rings. 【F:CODE/Systems/RuntimeServerLoop.cs†L64-L110】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L401-L443】
- **Handshake servicing:** `HandshakeProcessingPhaseHook.OnPreTick` processes up to the per-tick budget deterministically; defers with a counter when backlog remains. 【F:CODE/Systems/SessionHandshakePipeline.cs†L226-L258】
- **State mutation window:** Only simulation participants run between pre/post hooks; eligibility is rechecked to detect mid-tick mutation. 【F:CODE/Systems/WorldSimulationCore.cs†L261-L392】
- **Nondeterminism hazards:**
  - Inbound commands never drained, so authoritative ordering across sessions is undefined (ingress queue ordering never applied). 【F:CODE/Systems/DeterministicTransportQueues.cs†L84-L181】
  - Outbound snapshots may be trimmed arbitrarily when queues overrun because no deterministic dequeue driver exists. 【F:CODE/Systems/DeterministicTransportQueues.cs†L462-L519】

## 4) Closure Checklist for Prior P0/P1 Items (MANDATORY)
| Stage | Status | Evidence | Remaining risk |
| --- | --- | --- | --- |
| Stage 1: Command ingestion drain/freeze | Partially | Freeze hook registered and runs pre-tick with deterministic ordering. 【F:CODE/Systems/RuntimeServerLoop.cs†L64-L110】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L401-L443】 | No driver pulls from `AuthoritativeCommandIngress` into the ingestor; ingress backlog persists. |
| Stage 2: Replication _workContexts cleanup | Closed | `ClientReplicationSnapshotSystem.OnSessionDisconnected` removes contexts; disposal returns pooled arrays once work items finish. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L76-L125】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L418-L544】 | None noted. |
| Stage 3: Handshake servicing on tick | Closed | `HandshakeProcessingPhaseHook` services up to the configured budget every pre-tick. 【F:CODE/Systems/SessionHandshakePipeline.cs†L226-L258】 | Backlog still possible if driver not registered, but hook exists. |
| Stage 4: Persistence byte caps + zero-allocation trim | Closed | `PersistenceWriteQueue` enforces per-player/global count+byte caps dropping oldest without rebuilding; metrics updated in-place. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L915】 | No worker drains the queue, so writes may still accumulate. |
| Stage 5: Combat intent caps + pooling/reuse | Partially | Fixed per-tick caps with pooled staging/frozen snapshot pools; overflow drops newest with metrics. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L52-L148】【F:CODE/Systems/CombatIntentQueueSystem.cs†L227-L284】 | Payload freezing still allocates new dictionaries/lists per intent. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L848-L912】 |

## 5) Allocation & GC Risk Audit (Zero/Low GC)
- **Tick loop execution:** Steady-state allocations: NONE. Pre-sized buffers and reuse in `WorldSimulationCore` snapshot/eligibility; no per-tick new collections. 【F:CODE/Systems/WorldSimulationCore.cs†L261-L333】
- **Command ingestion/drain/freeze:** Steady-state allocations: NONE once sessions are created; rings and scratch arrays are pooled. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L46-L279】
- **Handshake processing:** Steady-state allocations: NONE; uses fixed arrays and counters. 【F:CODE/Systems/SessionHandshakePipeline.cs†L34-L182】
- **Snapshot building/serialization:** SOME; `SnapshotWorkContext.EnsureEligibleCapacity/EnsureSnapshotCapacity` rent arrays, reused per session, but initial rent per session occurs on first snapshot after connect. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L418-L502】
- **AOI/spatial queries:** SOME; `VisibilityCullingService.RefreshVisibility` sorts a reusable list but allocates pooled buffers only on growth; zone pruning allocates a temporary list per call. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L581-L665】
- **Persistence queue trimming:** NONE; trims dequeue and update metrics without new collections. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L915】
- **Combat intent staging:** SOME; staging uses pooled buckets but `PayloadFreezer.DeepFreeze` allocates new dictionaries/lists per intent at freeze time. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L848-L912】

## 6) Pooling Ownership & Safety
- **Inbound payload buffers:** Transport threads rent `PooledPayloadLease` and ownership passes to ingress queues; drops/overflow dispose leases deterministically. 【F:CODE/Systems/PooledTransportRouter.cs†L52-L127】【F:CODE/Systems/DeterministicTransportQueues.cs†L99-L158】
- **Outbound snapshot buffers:** `SnapshotSerializer` rents byte arrays and ownership stays with `SerializedSnapshot`/transport until disposed; enqueue/drop paths dispose on trim and on session drop. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L746-L879】【F:CODE/Systems/DeterministicTransportQueues.cs†L580-L738】
- **Persistence payload buffers:** Completions carry `PooledPayloadLease` and are disposed on drop or after apply in `PersistenceCompletionQueue.Drain`. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】
- **Double-return/leak prevention:** Snapshot work contexts mark for removal and only return pools after in-flight work completes, avoiding double-return. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L418-L544】 Drops in transport/persistence dispose leases immediately to prevent leaks. 【F:CODE/Systems/DeterministicTransportQueues.cs†L133-L217】【F:CODE/Systems/PersistenceCompletionQueue.cs†L77-L108】
- **Disconnect/shutdown paths:** Session disconnect clears transport, command ingestor, visibility, and replication contexts; shutdown clears all transient pools. 【F:CODE/Systems/RuntimeServerLoop.cs†L138-L202】

## 7) Bounded Growth & Backpressure
- **Inbound command mailboxes:** Caps per session (count + bytes) with reject-on-overflow; metrics track rejects/peaks. 【F:CODE/Systems/DeterministicTransportQueues.cs†L84-L181】
- **Authoritative ingestor rings:** Fixed per-session capacity from `RuntimeBackpressureConfig`; overflow drops newest with metrics. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L46-L90】【F:CODE/Systems/RuntimeBackpressureConfig.cs†L1-L71】
- **Handshake queue:** Fixed-size ring; overflow increments dropped counter. 【F:CODE/Systems/SessionHandshakePipeline.cs†L34-L101】
- **Replication snapshot queue:** Caps on count and bytes per session; overflow drops oldest snapshots and disposes buffers. 【F:CODE/Systems/DeterministicTransportQueues.cs†L580-L738】
- **Persistence write queue:** Per-player and global caps on count and bytes; overflow drops oldest deterministically and updates metrics. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L915】
- **Persistence completion mailbox:** Caps on count+bytes; overflow drops oldest and disposes payloads. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】
- **Combat intent staging:** Session and per-actor caps enforced with overflow rejection; staging/frozen snapshots pooled. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L52-L148】【F:CODE/Systems/CombatIntentQueueSystem.cs†L227-L284】

## 8) Thread Boundary Contract
- **Tick thread responsibilities:** World simulation tick loop, pre/post hooks (handshakes, command freeze, persistence completion drain, replication snapshot scheduling), visibility maintenance. 【F:CODE/Systems/WorldSimulationCore.cs†L261-L333】【F:CODE/Systems/RuntimeServerLoop.cs†L64-L110】
- **Transport threads:** Enqueue inbound payloads and dequeue outbound snapshots; expected to avoid world-state mutation. 【F:CODE/Systems/PooledTransportRouter.cs†L52-L153】【F:CODE/Systems/DeterministicTransportQueues.cs†L462-L519】
- **Persistence/I/O workers:** External; expected to dequeue writes via `PersistenceWriteQueue.TryDequeue` and enqueue completions for tick-thread apply. **MISSING driver.** 【F:CODE/Systems/DeterministicTransportQueues.cs†L941-L970】【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】
- **Enforcement:** Tick thread assertion present in `WorldSimulationCore` and phase hooks; transport router has no asserts but is documented as tick-only for routing. 【F:CODE/Systems/WorldSimulationCore.cs†L261-L333】【F:CODE/Systems/PooledTransportRouter.cs†L100-L153】
- **Off-thread mutation risks:** Visibility/replication caches assume tick-only without locks; misuse could corrupt state. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L581-L665】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L91-L125】

## 9) Blocking Call / Stall Risk Audit
- **Tick loop scheduling:** Uses `Thread.Sleep` with short spin to hit cadence; acceptable per brief. 【F:CODE/Systems/WorldSimulationCore.cs†L205-L259】【F:CODE/Systems/TickSystemCore.cs†L150-L200】
- **No synchronous I/O in tick paths:** No `Task.Wait`, `.Result`, file or network I/O in tick hooks/participants observed. Searches for blocking primitives were limited to scheduling sleeps/spins. 【F:CODE/Systems/WorldSimulationCore.cs†L205-L259】
- **Lock contention:** Ingress/queues use short critical sections; no locks held across tick simulation loops. Command freeze/handshake hooks lock only around snapshot/drain operations. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L92-L170】【F:CODE/Systems/SessionHandshakePipeline.cs†L50-L136】

## 10) AOT/IL2CPP Safety Audit
- **Runtime codegen:** None found; files include explicit IL2CPP/AOT cautions. 【F:CODE/Systems/RuntimeServerLoop.cs†L14-L22】【F:CODE/Systems/CombatIntentQueueSystem.cs†L24-L27】
- **Reflection-heavy discovery:** None; registration is explicit via `WorldBootstrapRegistration`. 【F:CODE/Systems/WorldBootstrapRegistration.cs†L1-L61】
- **Stripping safety:** Tick hooks/participants are explicitly constructed and registered; no dynamic type discovery that would be stripped. 【F:CODE/Systems/RuntimeServerLoop.cs†L64-L110】【F:CODE/Systems/WorldBootstrapRegistration.cs†L1-L61】

## 11) Observability & Ops Readiness
- **Tick duration metrics:** `TickDiagnostics.RecordTick` captures duration/overrun/clamp per tick without allocations; stall watchdog hooked to runtime loop. 【F:CODE/Systems/WorldSimulationCore.cs†L225-L259】【F:CODE/Systems/TickDiagnostics.cs†L1-L210】
- **Queue metrics:** Ingress, snapshot, persistence, and handshake queues expose metrics snapshots for diagnostics. 【F:CODE/Systems/DeterministicTransportQueues.cs†L241-L280】【F:CODE/Systems/DeterministicTransportQueues.cs†L972-L1010】【F:CODE/Systems/SessionHandshakePipeline.cs†L174-L182】
- **Stall watchdog:** Configured in both tick drivers (`WorldSimulationCore`, `TickSystem`) with event surfaced via `RuntimeServerLoop`. 【F:CODE/Systems/WorldSimulationCore.cs†L121-L259】【F:CODE/Systems/TickSystemCore.cs†L69-L119】
- **Gaps:** No metrics surfaced for ingress→ingestor bridging (since missing); no transport driver metrics for outbound dequeue; persistence worker absent so no I/O latency metrics.

## 12) Risk Register & Next Actions
- **P0 — Transport ingress not serviced:** (Transport) `PooledTransportRouter.RouteQueuedInbound` lacks a tick-thread caller; commands stall or drop. Guardrail: bounded queue + thread boundary. *Fix:* add a pre-tick phase hook to drain transport ingress deterministically before command freeze, disposing on rejection. 【F:CODE/Systems/PooledTransportRouter.cs†L100-L153】
- **P0 — Ingress not bridged to ingestor:** (Authoritative input) `AuthoritativeCommandIngress` never feeds `AuthoritativeCommandIngestor`; frozen batches stay empty. Guardrail: deterministic authoritative mutation window. *Fix:* add tick-phase adapter that drains ingress per session, decodes into `AuthoritativeCommand`, and stages in the ingestor before freeze. 【F:CODE/Systems/DeterministicTransportQueues.cs†L84-L181】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L401-L443】
- **P1 — Outbound snapshot dequeue missing:** (Transport egress) `DeterministicTransportRouter.TryDequeueSnapshot` unused; outbound buffers trimmed instead of sent. Guardrail: bounded queues + delivery determinism. *Fix:* supply a transport-thread loop that polls `TryDequeueSnapshot` with backpressure-aware send limits and disposes on drop. 【F:CODE/Systems/DeterministicTransportQueues.cs†L462-L519】
- **P1 — Persistence worker absent:** (Persistence) `PersistenceWriteQueue` never dequeued; completions never enqueued. Guardrail: no blocking I/O on tick thread with bounded queues. *Fix:* implement off-thread worker consuming `TryDequeue`, performing writes, and returning `PersistenceCompletion` via the mailbox. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L1010】【F:CODE/Systems/PersistenceCompletionQueue.cs†L1-L108】
- **P1 — Combat payload freeze allocations:** (Combat) `PayloadFreezer.DeepFreeze` allocates per intent each tick. Guardrail: zero/low-GC hot paths. *Fix:* introduce pooled immutable payload representations or reuse frozen payload caches across ticks. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L848-L912】
- **P1 — Thread enforcement for visibility/replication:** (Replication/AOI) Tick-thread-only assumption lacks assertions on all entry points. Guardrail: thread boundary enforcement. *Fix:* add `TickThreadAssert` to public methods or protect with locks where external calls occur. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L581-L665】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L91-L125】
- **P2 — Diagnostics gaps for ingress bridge:** (Diagnostics) No metrics exist for ingress→ingestor drops/backlog because bridge is missing. Guardrail: observability/backpressure. *Fix:* when bridging, emit counters for decoded/accepted/dropped commands and ingress drain latency. 【F:CODE/Systems/DeterministicTransportQueues.cs†L241-L280】

---

## APPENDIX A — Evidence Table (MANDATORY)
| Severity | Subsystem | File | Type/Method | Finding | Guardrail violated | Evidence summary |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | Transport | PooledTransportRouter.cs | RouteQueuedInbound | No caller drains inbound mailboxes on tick thread. | Thread boundary & bounded queues | Method defined but runtime loop lacks invocation; ingress backlog inevitable. 【F:CODE/Systems/PooledTransportRouter.cs†L100-L153】【F:CODE/Systems/RuntimeServerLoop.cs†L64-L202】 |
| P0 | Authoritative input | DeterministicTransportQueues.cs | AuthoritativeCommandIngress.TryDequeue | Ingress queue never feeds command ingestor/freeze. | Deterministic tick mutation window | Ingress supports TryDequeue but no bridge into `AuthoritativeCommandIngestor` tick hook. 【F:CODE/Systems/DeterministicTransportQueues.cs†L160-L217】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L401-L443】 |
| P1 | Transport egress | DeterministicTransportQueues.cs | TryDequeueSnapshot | No transport-thread driver; outbound snapshots trim/drop instead of send. | Bounded growth/backpressure | Dequeue API exists but runtime loop lacks caller. 【F:CODE/Systems/DeterministicTransportQueues.cs†L462-L519】 |
| P1 | Persistence | DeterministicTransportQueues.cs | PersistenceWriteQueue.Enqueue/TryDequeue | Write queue capped but never drained by a worker. | No blocking I/O on tick thread / bounded queues | Enqueue/trim logic present; no dequeue usage. 【F:CODE/Systems/DeterministicTransportQueues.cs†L780-L1010】 |
| P1 | Combat | CombatIntentQueueSystem.cs | PayloadFreezer.DeepFreeze | Per-intent allocations each tick breach zero-GC steady state. | Zero/low GC | DeepFreeze builds new dictionaries/lists for every payload. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L848-L912】 |
| P1 | Thread safety | RuntimeIntegrationZeroGcHardening.cs | VisibilityCullingService.RefreshVisibility | Tick-thread-only assumption lacks asserts/locks, risking off-thread mutation. | Thread boundary enforcement | No synchronization or asserts guarding visibility cache updates. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L581-L665】 |
| P1 | Replication | ClientReplicationSnapshotSystem.cs | OnPostTick/CreateWorkItem | Assumes tick-thread-only invocation; off-thread misuse would corrupt pooled buffers. | Thread boundary enforcement | No asserts on entry; relies on caller discipline. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L98-L125】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L418-L502】 |
| P2 | Diagnostics | DeterministicTransportQueues.cs | SnapshotMetrics (Ingress) | No metrics for ingress→ingestor bridge (because bridge missing). | Observability/backpressure | Metrics exist only for ingress queue, not for decoded/ingested commands. 【F:CODE/Systems/DeterministicTransportQueues.cs†L241-L280】 |

## APPENDIX B — Search/Review Notes (MANDATORY)
- Reviewed runtime code under `CODE/Systems`, focusing on tick, transport, replication, persistence, combat, and integration files.
- Grep scans:
  - Allocation scan: `rg "new List<" CODE/Systems`
  - Blocking scan: `rg "Thread\.Sleep|Task\.Wait|\.Result|Wait\(|Monitor\.Wait|File\.|Stream|ReadAll|WriteAll|WebRequest|HttpClient" CODE/Systems`
  - AOT scan: `rg "Reflection\.Emit|DynamicMethod|Expression\.Compile|Activator\.CreateInstance" CODE/Systems`
- Referenced MMO guardrails from `00_ADMIN/Reference/MMO Runtime & Compilation Technical Brief` during assessment.
