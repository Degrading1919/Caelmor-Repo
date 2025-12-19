# Runtime Integration Audit

## 1) Executive Summary
- **Scope (A):** Reviewed runtime-facing code under `CODE/Systems` including transport ingress/egress (`PooledTransportRouter`, `DeterministicTransportQueues`, `OutboundSendPump`), tick loop orchestration (`WorldSimulationCore`, `RuntimeServerLoop`), ingestion (`RuntimeIntegrationZeroGcHardening`), replication (`ClientReplicationSnapshotSystem`), persistence (`PersistenceWorkerLoop`, `PersistenceCompletionQueue`), combat (`CombatIntentQueueSystem`, `CombatRuntimeSystem`), and onboarding (`SessionHandshakePipeline`). MMO guardrails cross-referenced via `00_ADMIN/Reference/MMO Runtime & Compilation Technical Brief`.
- **Tick Driver (B):** `WorldSimulationCore.RunLoop` owns the authoritative 10 Hz tick with pre/post phase hooks and participant execution; `TickThreadAssert` captures the tick thread on start. 【F:CODE/Systems/WorldSimulationCore.cs†L192-L333】
- **System Code Complete:** YES — transport ingress/egress and persistence now have running pumps; remaining gaps are P1 thread-guard coverage for replication/visibility and absent command consumers.
- **Recurring Issues Closure Scorecard:**
  1. Systems exist but aren’t pumped — **CLOSED**
  2. Islands not pipelines — **PARTIAL** (authoritative command consumer not implemented)
  3. Hot-path allocations still exist — **PARTIAL** (replication/combat allocate on growth events)
  4. Backpressure allocates when pressure happens — **CLOSED**
  5. Disconnect/shutdown leaks — **CLOSED**
  6. Thread-boundary assumed not enforced — **PARTIAL**
  7. Combat drift — **CLOSED**
  8. Replication drift — **CLOSED**

## 2) Pump Verification (the #1 recurring problem)
### 2.1 Inbound Pump Proof
- Transport enqueue (transport thread) → `PooledTransportRouter.EnqueueInbound` stages pooled payloads under per-session caps. 【F:CODE/Systems/PooledTransportRouter.cs†L45-L152】
- Tick hook `InboundPumpTickHook.OnPreTick` runs every tick (registered via `RuntimeServerLoop.Create`), drains staged frames deterministically, decodes payloads, enqueues into `AuthoritativeCommandIngestor`, then freezes per active session. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L465-L536】【F:CODE/Systems/RuntimeServerLoop.cs†L121-L139】
- Authoritative ingest ring assigns deterministic sequence and freezes batches per session. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L48-L138】
- **Gap:** No runtime consumer of `FrozenCommandBatch` was found beyond validation hooks, so authoritative commands still do not drive simulation participants. Status: **PARTIAL (P1)**.

### 2.2 Outbound Pump Proof
- Post-tick replication builds session snapshots and enqueues them to the transport queue via `SnapshotWorkItem.ExecuteSlice` → `IReplicationSnapshotQueue.Enqueue`. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L104-L133】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L372-L418】
- `BoundedReplicationSnapshotQueue` buffers snapshots with cap+trim and exposes `TryDequeueSnapshot`. 【F:CODE/Systems/DeterministicTransportQueues.cs†L629-L738】
- `OutboundSendPump.Run` (transport thread) deterministically enumerates active sessions and drains per-session outbound queues, handing ownership to the sender or disposing on failure. 【F:CODE/Systems/OutboundSendPump.cs†L57-L158】

### 2.3 Persistence Pump Proof
- Writes enqueued via `PersistenceWriteQueue.Enqueue` (per-player and global caps, drop-oldest) feed the global queue. 【F:CODE/Systems/DeterministicTransportQueues.cs†L900-L990】
- `PersistenceWorkerLoop.Run` drains writes off-thread, executes `IPersistenceWriter`, and posts completions into the bounded completion mailbox. 【F:CODE/Systems/PersistenceWorkerLoop.cs†L42-L147】
- Tick hook `PersistenceCompletionPhaseHook.OnPreTick` drains completions on the tick thread for deterministic apply. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L175-L196】
- **Config caveat:** Pump runs only when the host supplies a worker/writer and completion queue to `RuntimeServerLoop.Create`; otherwise persistence requests would stall.

## 3) Bridge Verification (the #2 recurring problem)
- **Ingress → ingestor bridge:** Tick hook bridges transport ingress to `AuthoritativeCommandIngestor` and freezes batches each tick. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L488-L536】
- **Snapshot queue → transport send bridge:** Replication enqueues snapshots to the transport queue; `OutboundSendPump` drains and calls the transport sender. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L372-L418】【F:CODE/Systems/OutboundSendPump.cs†L101-L139】
- **Persistence completion → apply bridge:** Worker enqueues completions; `PersistenceCompletionPhaseHook` drains/applies on tick. 【F:CODE/Systems/PersistenceWorkerLoop.cs†L93-L112】【F:CODE/Systems/PersistenceCompletionQueue.cs†L176-L196】
- **Remaining gap:** No downstream consumer for frozen authoritative commands, leaving ingress isolated from gameplay systems.

## 4) Hot-Path Allocation Audit (the #3 recurring problem)
- **Tick loop orchestration:** No steady-state allocations; participant/phase snapshots and eligibility buffers are reused each tick. 【F:CODE/Systems/WorldSimulationCore.cs†L265-L333】 Status: **NONE**.
- **Inbound routing + decode + ingestor freeze:** Ingress drains into a pooled buffer; decode uses stack-friendly primitives; ingestor rings reuse pooled arrays. **NONE** after warm-up. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L488-L536】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L48-L138】
- **Handshake service loop:** Fixed-size ring with no per-tick allocations. **NONE**. 【F:CODE/Systems/SessionHandshakePipeline.cs†L34-L102】【F:CODE/Systems/SessionHandshakePipeline.cs†L226-L258】
- **Combat intent staging + resolution:** Staging buckets and frozen snapshots are pooled; dictionary growth only when seeing new actors/ticks. **SOME (P2)** for dictionary growth on new actors. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L34-L118】【F:CODE/Systems/CombatIntentQueueSystem.cs†L226-L309】
- **Replication snapshot build/serialize/AOI:** Snapshot work slices reuse rented arrays; delta serializer reuses lists/hashset but allocates when observed entity count grows. **SOME (P2)**. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L156-L180】【F:CODE/Systems/DeterministicTransportQueues.cs†L1220-L1286】
- **Persistence trimming/drop paths:** Caps enforced with dequeue/trim only; no rebuild allocations. **NONE**. 【F:CODE/Systems/DeterministicTransportQueues.cs†L939-L986】【F:CODE/Systems/PersistenceCompletionQueue.cs†L36-L87】

## 5) Backpressure Under Pressure (the #4 recurring problem)
- **Transport inbound mailboxes:** Per-session count+byte caps; overflow rejects without reallocations. 【F:CODE/Systems/PooledTransportRouter.cs†L45-L152】
- **Authoritative ingress rings:** Fixed-size per session, drop-newest overflow. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L48-L90】
- **Handshake queue:** Fixed ring; overflow increments drop counter only. 【F:CODE/Systems/SessionHandshakePipeline.cs†L34-L63】
- **Replication snapshot queue:** Per-session count+byte caps drop oldest and dispose buffers; metrics tracked in-place. 【F:CODE/Systems/DeterministicTransportQueues.cs†L629-L738】
- **Outbound pump:** Bounded per-iteration/per-session send to avoid unbounded drain bursts. 【F:CODE/Systems/OutboundSendPump.cs†L101-L139】
- **Persistence write queue:** Per-player and global caps drop-oldest deterministically; no rebuilds. 【F:CODE/Systems/DeterministicTransportQueues.cs†L947-L986】【F:CODE/Systems/DeterministicTransportQueues.cs†L974-L986】
- **Persistence completion mailbox:** Count/byte caps drop oldest and dispose payloads. 【F:CODE/Systems/PersistenceCompletionQueue.cs†L34-L87】
- **Combat intent staging:** Per-session/actor caps with drop-newest policy. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L60-L115】【F:CODE/Systems/CombatIntentQueueSystem.cs†L246-L274】

## 6) Disconnect / Shutdown Cleanup (the #5 recurring problem)
- Session disconnect drops transport queues, command ingestor state, visibility caches, and replication work contexts. 【F:CODE/Systems/RuntimeServerLoop.cs†L192-L200】【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L80-L93】
- Zone unload clears entity registry and visibility/spatial state; shutdown clears all transient queues (transport, handshakes, commands, persistence mailboxes). 【F:CODE/Systems/RuntimeServerLoop.cs†L210-L260】
- Snapshot/persistence payloads are disposed on drop paths to avoid pooled-buffer leaks. 【F:CODE/Systems/DeterministicTransportQueues.cs†L696-L738】【F:CODE/Systems/PersistenceCompletionQueue.cs†L60-L87】

## 7) Thread Boundary Enforcement (the #6 recurring problem)
- **Thread map:** Tick thread = `WorldSimulationCore.RunLoop`; transport ingress thread(s) call `PooledTransportRouter.EnqueueInbound`; transport egress thread = `OutboundSendPump`; persistence worker thread = `PersistenceWorkerLoop`. 【F:CODE/Systems/WorldSimulationCore.cs†L192-L259】【F:CODE/Systems/OutboundSendPump.cs†L57-L158】【F:CODE/Systems/PersistenceWorkerLoop.cs†L42-L147】【F:CODE/Systems/PooledTransportRouter.cs†L45-L152】
- **Tick-only guards:** Phase hooks and replication builder assert tick thread. 【F:CODE/Systems/ClientReplicationSnapshotSystem.cs†L95-L133】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L488-L536】
- **Risks:** Visibility/AOI services and spatial index lack tick-thread asserts or locks, so off-thread calls could corrupt caches. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L720-L829】 Status: **PARTIAL (P1)**.

## 8) Combat Drift Closure (the #7 recurring problem)
- Deterministic staging with fixed caps and per-actor sequencing; overflow rejects newest. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L34-L118】【F:CODE/Systems/CombatIntentQueueSystem.cs†L226-L309】
- Frozen queue uses pooled buffers; no per-intent dictionary rebuilds during freeze. 【F:CODE/Systems/CombatIntentQueueSystem.cs†L200-L274】
- Combat execution consumes only frozen intents; no dynamic payload dictionaries or string-based lookups in the hot path beyond stable identifiers. 【F:CODE/Systems/CombatRuntimeSystem.cs†L80-L124】 Status: **CLOSED**.

## 9) Replication Drift Closure (the #8 recurring problem)
- Deterministic active session index provides snapshot iteration order for both snapshot build and outbound send. 【F:CODE/Systems/DeterministicActiveSessionIndex.cs†L70-L124】【F:CODE/Systems/OutboundSendPump.cs†L101-L139】
- Outbound queue is drained continuously by transport-thread pump; trims drop/return buffers on overflow. 【F:CODE/Systems/DeterministicTransportQueues.cs†L629-L738】【F:CODE/Systems/OutboundSendPump.cs†L101-L139】
- Fingerprints cached per session; delta serializer reuses buffers and updates baselines deterministically. 【F:CODE/Systems/DeterministicTransportQueues.cs†L629-L708】【F:CODE/Systems/DeterministicTransportQueues.cs†L1220-L1286】
- Snapshot buffers pooled and returned on send/drop. 【F:CODE/Systems/DeterministicTransportQueues.cs†L1364-L1479】

## 10) AOT/IL2CPP Safety Gate
- No runtime code generation or Reflection.Emit detected; entry points carry IL2CPP/AOT warnings. 【F:CODE/Systems/RuntimeServerLoop.cs†L12-L22】【F:CODE/Systems/CombatIntentQueueSystem.cs†L1-L27】【F:CODE/Systems/DeterministicTransportQueues.cs†L521-L536】
- All runtime registrations are explicit (no reflection-based discovery) via `WorldBootstrapRegistration.Apply`. 【F:CODE/Systems/RuntimeServerLoop.cs†L121-L155】【F:CODE/Systems/WorldBootstrapRegistration.cs†L15-L61】

## 11) Risk Register (recurring-issue related)
- **P1 (Issue 2 & 1)** — Authoritative commands have no runtime consumer: frozen batches are produced but no simulation system consumes `FrozenCommandBatch`, leaving authoritative input disconnected from world mutation. *Fix:* implement a tick-thread participant or hook that reads frozen batches and applies commands deterministically.
- **P1 (Issue 6)** — Visibility/AOI services lack thread asserts/locks; off-thread calls could corrupt visibility caches. *Fix:* add `TickThreadAssert` to public methods or guard with locks shared with spatial index access.
- **P1 (Issue 3)** — Replication/combat allocations on growth: delta serializer and combat staging allocate when entity/actor counts exceed prior maxima. *Fix:* pre-size buffers based on expected peaks or expose configuration knobs to prewarm pools.
- **P1 (Issue 3/4)** — Persistence pump optional: if the host omits `PersistenceWorkerLoop`/completion hook, writes will accumulate or trim without ever applying. *Fix:* enforce required persistence wiring when persistence queues are enabled.

---

## APPENDIX A — Evidence Table (MANDATORY)
| Severity | Recurring Issue (1–8) | Subsystem | File | Type/Method | Finding | Evidence summary |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | 2 | Authoritative input | RuntimeIntegrationZeroGcHardening.cs | InboundPumpTickHook.OnPreTick | Commands are bridged and frozen each tick but no consumer of `FrozenCommandBatch` exists in runtime paths. | Pump drains ingress and freezes commands, yet no simulation participant reads the frozen batches. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L488-L536】【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L48-L138】 |
| P1 | 6 | Replication/AOI | RuntimeIntegrationZeroGcHardening.cs | VisibilityCullingService.Track/RefreshVisibility | Tick-thread-only assumption lacks asserts/locks; off-thread mutation could corrupt visibility caches. | Public methods mutate shared dictionaries without thread guards. 【F:CODE/Systems/RuntimeIntegrationZeroGcHardening.cs†L720-L779】 |
| P1 | 3 | Replication | DeterministicTransportQueues.cs | SnapshotDeltaSerializer.Serialize | Delta serializer allocates on growth (lists/hashset expansions) when entity counts increase. | Lists/hashset cleared and reused but grow with observed entity set size. 【F:CODE/Systems/DeterministicTransportQueues.cs†L1220-L1286】 |
| P0 | 4 | None | — | — | — | No P0 issues identified in this audit; pumps are present for ingress, egress, and persistence. | — |

## APPENDIX B — Search Notes (MANDATORY)
- Allocation risk scans in `CODE/Systems`: `rg "System\.Linq"`, `rg "new List<"`, `rg "new Dictionary<"`, `rg "new Queue<"`, `rg "new byte["`, `rg "Action"`, `rg "delegate"`, `rg "=>"`, `rg "\.Select\("`, `rg "\.Where\("`, `rg "\.OrderBy\("`, `rg "\.ToArray\("`, `rg "string\.Format"`, `rg '\$"'`.
- Blocking risk scans in `CODE/Systems`: `rg "Thread\.Sleep|Task\.Wait|\.Result|Wait\(|Monitor\.Wait|File\.|Stream|ReadAll|WriteAll|WebRequest|HttpClient"`.
- AOT risk scans in `CODE/Systems`: `rg "Reflection\.Emit|DynamicMethod|Expression\.Compile"`.
- Leak risk scans in `CODE/Systems`: `rg "\+= "`, `rg "\bstatic\b"`, `rg "IDisposable"`, `rg "Dispose\("`, `rg "OnDestroy|OnDisable"`.
