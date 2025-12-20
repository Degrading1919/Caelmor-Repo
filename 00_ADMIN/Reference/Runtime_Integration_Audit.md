1) Executive Summary
- System Code Complete: NO
- One-sentence justification: The two combat fixes (numeric event IDs + alloc-free delivery guards) are now proven, but tick-thread enforcement for combat replication remains unproven and other hot-path allocation risks persist.
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
  12) CLOSED
- Delta since last audit:
  - Combat event IDs are now generated and propagated as numeric ulong values via CombatEvent.DeterministicEventId (no string interpolation).
  - Combat replication delivery guards now use per-client HashSet<ulong> reused across ticks; no per-tick Dictionary/HashSet allocations.

2) Combat Fix Verification (PRIMARY FOCUS)
2.1 Numeric EventId proof (no strings)
- Event/outcome types carrying ids:
  - CombatEvent.EventId (ulong) and CombatEventPayload.EventId (ulong) (CODE/Systems/CombatOutcomeApplicationSystem.cs; CODE/Systems/CombatReplicationSystem.cs).
- Creation site (numeric ulong):
  - CombatEvent.CreateIntentResultEvent/CreateDamageOutcomeEvent/CreateMitigationOutcomeEvent/CreateStateChangeEvent -> DeterministicEventId(int tick, CombatEventType type, ulong payloadId) returns ulong hash (CODE/Systems/CombatOutcomeApplicationSystem.cs, CombatEvent.*Create* + CombatEvent.DeterministicEventId).
- Storage/transport within combat systems:
  - CombatEvent stores EventId as ulong; Emit uses ICombatEventSink.Emit(CombatEvent) (CODE/Systems/CombatOutcomeApplicationSystem.cs, CombatEvent.EventId + EmitEventAfterApply).
  - CombatReplicationSystem.TryMarkDelivered receives ulong eventId and stores in DeliveryGuard.HashSet<ulong> (CODE/Systems/CombatReplicationSystem.cs, TryMarkDelivered/DeliveryGuard).
- Replication enqueue:
  - CombatReplicationSystem.ReplicateSingleEvent passes combatEvent.EventId (ulong) to TryMarkDelivered and then to CombatEventPayload.FromCombatEvent (CODE/Systems/CombatReplicationSystem.cs, ReplicateSingleEvent).
- Serialization (if applicable):
  - UNKNOWN — no concrete serializer for CombatEventPayload found; only INetworkSender.SendReliable interface is present (CODE/Systems/CombatReplicationSystem.cs, INetworkSender).
- Explicit proof of no tick-time string interpolation for event IDs:
  - DeterministicEventId uses numeric mixing (Mix/hash) only; no string interpolation in event id creation sites (CODE/Systems/CombatOutcomeApplicationSystem.cs, CombatEvent.DeterministicEventId).
  - The payload IDs are numeric ulong derived via PayloadId.HashIntentId (hash over string characters, no string construction) and PayloadId.Combine (CODE/Systems/CombatOutcomeApplicationSystem.cs, PayloadId.HashIntentId/Combine).

2.2 Delivery guard alloc-free proof
- Delivery guard mechanism:
  - CombatReplicationSystem.DeliveryGuard maintains HashSet<ulong> _deliveredThisWindow per client; held in CombatReplicationSystem._deliveryGuards dictionary keyed by ClientId (CODE/Systems/CombatReplicationSystem.cs, CombatReplicationSystem + DeliveryGuard).
- No per-tick allocation:
  - BeginTick does not allocate; guard state is cleared on tick change inside DeliveryGuard.TryMarkDelivered via _deliveredThisWindow.Clear(); HashSet is constructed only in DeliveryGuard constructor (CODE/Systems/CombatReplicationSystem.cs).
  - Dictionary<ClientId, DeliveryGuard> only grows when a new client first appears; no per-tick Dictionary/HashSet creation inside the replicate loop (CODE/Systems/CombatReplicationSystem.cs, TryMarkDelivered + DeliveryGuard constructor).
- Cap values + overflow policy:
  - Cap values: deliveryGuardInitialCapacity (default 256) and deliveryGuardMaxCount (default 512) configured in CombatReplicationSystem constructor (CODE/Systems/CombatReplicationSystem.cs).
  - Overflow policy: if _deliveredThisWindow.Count >= _maxCount, the HashSet is cleared and overflow counter increments deterministically (DeliveryGuard.TryMarkDelivered) (CODE/Systems/CombatReplicationSystem.cs).
  - Metrics counters: CombatDeliveryGuardHits/Misses/Overflow updated via Interlocked.Increment in TryMarkDelivered/DeliveryGuard.TryMarkDelivered (CODE/Systems/CombatReplicationSystem.cs).
- Deterministic reset/cleanup:
  - Per-tick reset: DeliveryGuard.TryMarkDelivered clears on tick change and sets _tick/_hasTick (CODE/Systems/CombatReplicationSystem.cs).
  - Disconnect cleanup: ReleaseClient clears guard and removes it from dictionary (CODE/Systems/CombatReplicationSystem.cs).
  - Call site for ReleaseClient is not found in runtime wiring; disconnect cleanup is therefore UNKNOWN in actual runtime integration (no call chain found in CODE/Systems).

2.3 Tick-thread enforcement in combat apply/replication
- Outcome apply entrypoint:
  - CombatOutcomeApplicationSystem.Apply asserts tick thread via TickThreadAssert.AssertTickThread (CODE/Systems/CombatOutcomeApplicationSystem.cs).
- Replication enqueue/drain entrypoints:
  - CombatReplicationSystem.Replicate/ReplicateSingleEvent/TryMarkDelivered do not assert tick thread and no enclosing tick-thread enforcement call site was found (CODE/Systems/CombatReplicationSystem.cs; rg search for usage returned none). Thread ownership for replication is therefore UNKNOWN and treated as a partial closure of failure mode 7.

3) Hot-Path Allocation Audit (combat + nearby)
- CombatOutcomeApplicationSystem
  - HOT PATH: HashSet<ulong> usage for idempotence/duplicate checks is reused (AppliedIdSet.Set and _duplicateCheckSet), no per-tick allocation; PruneAppliedSets rents int[] from ArrayPool per tick (CODE/Systems/CombatOutcomeApplicationSystem.cs, AppliedIdSet/EnsureNoDuplicateIdsInBatchOrThrow/PruneAppliedSets).
  - Remaining string usage in combat loops: IntentResult.IntentId is compared and stored for validation; no string interpolation for EventId (CODE/Systems/CombatOutcomeApplicationSystem.cs, ApplyIntentResultStateEffectsOrThrow).
- CombatReplicationSystem
  - HOT PATH: DeliveryGuard.TryMarkDelivered uses HashSet<ulong> reused per client; no per-tick new HashSet/Dictionary allocations; CombatEventPayload allocation occurs per replicated event (new CombatEventPayload in FromCombatEvent) (CODE/Systems/CombatReplicationSystem.cs).
- Combat serialization helpers
  - UNKNOWN: No concrete serialization path for CombatEventPayload located; only INetworkSender.SendReliable interface present (CODE/Systems/CombatReplicationSystem.cs).

4) Regression Check (secondary)
- EntryPoint exists and starts host: HeadlessServerEntryPoint.Main -> RuntimeCompositionRoot.CreateHost -> ServerRuntimeHost.Start (CODE/Systems/RuntimeHost/HeadlessServerEntryPoint.cs; CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs; CODE/Systems/RuntimeHost/ServerRuntimeHost.cs).
- CompositionRoot used: RuntimeCompositionRoot.Create builds simulation, hooks, and pumps (CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs).
- Inbound/outbound/persistence pumps still wired: phase hooks registered via RuntimeCompositionRoot.Create -> WorldBootstrapRegistration.Apply; outbound/persistence threads started in RuntimeServerLoop.Start (CODE/Systems/RuntimeHost/RuntimeCompositionRoot.cs; CODE/Systems/WorldBootstrapRegistration.cs; CODE/Systems/RuntimeServerLoop.cs).
- Trust boundary unchanged: client tick ordering rejected in InboundPumpTickHook (CODE/Systems/RuntimeIntegrationZeroGcHardening.cs).

5) Risk Register (recurring-issue-related only)
- P2 — Failure Mode 7 — Combat replication
  - File/type/method: CODE/Systems/CombatReplicationSystem.cs — Replicate/ReplicateSingleEvent/TryMarkDelivered
  - Why it violates MMO guardrail: Tick-thread ownership is not asserted and no tick-thread call site is proven; mutating delivery guard state could be accessed off-thread (thread ownership enforced insufficiently).
  - Minimal fix strategy (audit-only): Add TickThreadAssert/RuntimeGuardrailChecks at Replicate entry or ensure caller is tick-thread-only and document call chain.
- P2 — Failure Mode 9 — Tick core growth allocations
  - File/type/method: CODE/Systems/WorldSimulationCore.cs — ExecuteOneTick/EnsureCapacity
  - Why it violates MMO guardrail: arrays can grow after warm-up if participant/hook/gate counts increase, allocating on tick thread.
  - Minimal fix strategy (audit-only): Pre-register and pre-size to maximum expected counts before Start.
- P2 — Failure Mode 9 — Replication snapshot allocations
  - File/type/method: CODE/Systems/ClientReplicationSnapshotSystem.cs — CaptureSnapshotForSession/SnapshotWorkItem.BuildSnapshot
  - Why it violates MMO guardrail: new ClientReplicationSnapshot allocations and ArrayPool rents per tick; object pooling not present.
  - Minimal fix strategy (audit-only): Pool snapshot objects or shift to struct with pooled buffers.

APPENDIX A — Evidence Table (MANDATORY)
| Severity | Failure Mode # | Subsystem | File | Type/Method | Finding | Evidence summary |
|---|---|---|---|---|---|---|
| P2 | 12 | Combat apply | CODE/Systems/CombatOutcomeApplicationSystem.cs | CombatEvent.DeterministicEventId | Numeric ulong event ID generation | CreateIntentResultEvent/CreateDamageOutcomeEvent/CreateMitigationOutcomeEvent/CreateStateChangeEvent call DeterministicEventId(int, CombatEventType, ulong) which mixes tick/type/payloadId into ulong; no string interpolation. |
| P2 | 12 | Combat replication | CODE/Systems/CombatReplicationSystem.cs | TryMarkDelivered/DeliveryGuard | Per-client HashSet<ulong> reused across ticks | DeliveryGuard constructor allocates HashSet<ulong> once; TryMarkDelivered clears on tick change; no per-tick new HashSet/Dictionary. |
| P2 | 9 | Combat apply | CODE/Systems/CombatOutcomeApplicationSystem.cs | PruneAppliedSets | ArrayPool rent per tick | PruneAppliedSets rents int[] each tick to iterate applied id keys, then returns to ArrayPool. |
| P2 | 9 | Combat replication | CODE/Systems/CombatReplicationSystem.cs | CombatEventPayload.FromCombatEvent | Per-event payload allocation | FromCombatEvent constructs a new CombatEventPayload for every replicated event. |
| P2 | 7 | Combat replication | CODE/Systems/CombatReplicationSystem.cs | Replicate/ReplicateSingleEvent | Tick-thread ownership not asserted | No TickThreadAssert/RuntimeGuardrailChecks in replication entrypoints; no proven tick-thread-only call chain found. |

APPENDIX B — Search Notes (MANDATORY)
- Directories searched:
  - /workspace/Caelmor-Repo/CODE/Systems
  - /workspace/Caelmor-Repo/00_ADMIN/Reference
- All grep terms used:
  - "CombatOutcomeApplicationSystem"
  - "CombatReplicationSystem"
  - "eventId"
  - "EventId"
  - "OutcomeId"
  - "$\""
  - "string.Format"
  - "HashSet<"
  - "Dictionary<"
  - "new HashSet"
  - "new Dictionary"
  - "System.Linq"
  - "new List<"
  - "new Queue<"
  - "new byte["
  - "Action"
  - "delegate"
  - "=>"
  - ".Select("
  - ".Where("
  - ".OrderBy("
  - ".ToArray("
  - "ReadOnlyCollection"
  - "IEnumerable"
  - "static void Main"
  - "EntryPoint"
  - "ServerRuntimeHost"
  - "RuntimeCompositionRoot"
  - "CompositionRoot"
  - "CombatEventPayload"
  - "CombatEventBatch"
  - "CombatEvent"
- Any limitations encountered:
  - No concrete runtime serialization path for CombatEventPayload found; only INetworkSender interface references exist.
  - No runtime call site found for CombatReplicationSystem.Replicate or ReleaseClient, so thread ownership and disconnect cleanup are UNKNOWN.

END.
