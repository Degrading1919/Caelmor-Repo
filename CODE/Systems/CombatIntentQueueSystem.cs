// CombatIntentQueueSystem.cs
// NOTE: Save location must follow existing project structure.
// This file intentionally contains only the CombatIntentQueueSystem and minimal supporting types.
// No combat resolution, no combat state checks, no persistence, no CombatEvents emission.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Buffers;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatIntentQueueSystem
    /// - Owns authoritative combat intent queue (frozen per tick)
    /// - Accepts server-side submissions (payloads)
    /// - Performs structural schema validation only (Stage 11.2)
    /// - Orders deterministically (not based on arrival time; not influenced by client-controlled data)
    /// - Freezes at tick boundary: submissions during tick T become the frozen queue for tick T+1
    /// - Emits observable rejection results for structurally invalid intents (no success outcomes)
    /// - Exposes deterministic snapshots for Stage 9 validation harness
    /// </summary>
    // IL2CPP/AOT SAFETY: No runtime code generation or Reflection.Emit permitted; all runtime entrypoints must be
    // explicitly registered and editor-only APIs avoided. Reflection-based paths (none here) require explicit
    // preservation to survive managed code stripping.
    public sealed class CombatIntentQueueSystem
    {
        private readonly ITickSource _tickSource;
        private readonly IEntityIdValidator _entityIdValidator;
        private readonly IIntentRejectionSink _rejectionSink;

        // Staging: intents received during a tick T, to be frozen for tick T+1.
        private readonly Dictionary<int, StagingBucket> _stagedBySubmitTick = new();
        private readonly StagingBucketPool _stagingBucketPool = new StagingBucketPool(maxSize: 8);

        // Frozen queue exposed for the current authoritative tick.
        private FrozenQueueSnapshot _currentFrozen;
        private readonly Dictionary<int, FrozenQueueSnapshot> _frozenSnapshotsByTick = new();
        private readonly FrozenQueueSnapshotPool _frozenSnapshotPool = new FrozenQueueSnapshotPool(maxSize: 4);

        // Deterministic per-actor sequence assignment for a given frozen tick.
        // Derived deterministically during FreezeForTick() by sorting, not by arrival order.
        private readonly Dictionary<(int FrozenTick, string ActorId), int> _sequenceCounters = new();

        // Metrics and diagnostics (monotonic counters; deterministic updates).
        private long _structuralRejectCount;
        private long _overflowRejectCount;
        private int _peakStagingUsage;
        private int _lastFrozenCount;

        // Fixed deterministic caps to prevent unbounded growth. Overflow policy is drop-newest with rejection.
        private const int ActorIntentCapPerTick = 8;
        private const int SessionIntentCapPerTick = 64;
        private const int ActorCountCapacityHint = 8;
        private const OverflowPolicy DeterministicOverflowPolicy = OverflowPolicy.DropNewest;

        public CombatIntentQueueSystem(
            ITickSource tickSource,
            IEntityIdValidator entityIdValidator,
            IIntentRejectionSink rejectionSink)
        {
            _tickSource = tickSource ?? throw new ArgumentNullException(nameof(tickSource));
            _entityIdValidator = entityIdValidator ?? throw new ArgumentNullException(nameof(entityIdValidator));
            _rejectionSink = rejectionSink ?? throw new ArgumentNullException(nameof(rejectionSink));

            _tickSource.OnTickAdvanced += HandleTickAdvanced;

            _currentFrozen = _frozenSnapshotPool.Rent();
            _currentFrozen.Commit(_tickSource.CurrentTick, 0);
            _frozenSnapshotsByTick[_currentFrozen.AuthoritativeTick] = _currentFrozen;
        }

        /// <summary>
        /// Server-side intake entry point. Validates structure and stages for the current tick.
        /// IMPORTANT:
        /// - No combat resolution
        /// - No combat state legality checks
        /// - No success outcomes emitted
        /// - No dedupe that would break save/load determinism
        /// </summary>
        public IntakeReceipt SubmitIntent(CombatIntentSubmission submission)
        {
            if (submission == null) throw new ArgumentNullException(nameof(submission));

            int submitTick = _tickSource.CurrentTick;

            if (!CombatIntentStructuralValidator.TryValidate(submission, _entityIdValidator, out var reject))
            {
                var rejection = new IntentRejection(
                    intentId: submission.IntentId ?? string.Empty,
                    actorEntityId: submission.ActorEntityId ?? string.Empty,
                    intentType: submission.IntentType,
                    authoritativeTick: submitTick,
                    reasonCode: reject.ReasonCode);

                _structuralRejectCount++;
                _rejectionSink.OnRejected(rejection);
                return IntakeReceipt.Rejected(submission.IntentId ?? string.Empty, submitTick, reject.ReasonCode);
            }

            if (!_stagedBySubmitTick.TryGetValue(submitTick, out var bucket))
            {
                bucket = _stagingBucketPool.Rent();
                bucket.Prepare(SessionIntentCapPerTick);
                _stagedBySubmitTick.Add(submitTick, bucket);
            }

            if (bucket.SubmissionsCount >= SessionIntentCapPerTick)
            {
                return RejectOverflow(submission, submitTick, RejectReasonCodes.OverflowSessionIntentCap);
            }

            if (bucket.GetActorCount(submission.ActorEntityId!) >= ActorIntentCapPerTick)
            {
                return RejectOverflow(submission, submitTick, RejectReasonCodes.OverflowActorIntentCap);
            }

            bucket.IncrementActor(submission.ActorEntityId!);
            bucket.AddSubmission(new StagedSubmission(submission, submitTick));
            _peakStagingUsage = Math.Max(_peakStagingUsage, bucket.SubmissionsCount);

            // No success emissions here (explicit).
            return IntakeReceipt.Staged(submission.IntentId!, submitTick);
        }

        private IntakeReceipt RejectOverflow(CombatIntentSubmission submission, int submitTick, string reasonCode)
        {
            if (DeterministicOverflowPolicy != OverflowPolicy.DropNewest)
                throw new InvalidOperationException("Unsupported overflow policy.");

            _overflowRejectCount++;

            if (DeterministicOverflowPolicy == OverflowPolicy.DropNewest)
            {
                var rejection = new IntentRejection(
                    intentId: submission.IntentId ?? string.Empty,
                    actorEntityId: submission.ActorEntityId ?? string.Empty,
                    intentType: submission.IntentType,
                    authoritativeTick: submitTick,
                    reasonCode: reasonCode);

                _rejectionSink.OnRejected(rejection);
            }

            return IntakeReceipt.Rejected(submission.IntentId ?? string.Empty, submitTick, reasonCode);
        }

        /// <summary>
        /// Returns the frozen queue snapshot for the current authoritative tick.
        /// This snapshot is immutable and stable once created.
        /// </summary>
        public FrozenQueueSnapshot GetFrozenQueueForCurrentTick()
        {
            int tick = _tickSource.CurrentTick;
            if (_currentFrozen.AuthoritativeTick == tick)
                return _currentFrozen;

            if (_frozenSnapshotsByTick.TryGetValue(tick, out var existing))
            {
                _currentFrozen = existing;
                return _currentFrozen;
            }

            var emptySnapshot = _frozenSnapshotPool.Rent();
            emptySnapshot.Commit(tick, 0);
            _frozenSnapshotsByTick[tick] = emptySnapshot;
            _currentFrozen = emptySnapshot;
            return _currentFrozen;
        }

        /// <summary>
        /// Deterministic snapshot for Stage 9 harness comparisons.
        /// - Stable ordering
        /// - Minimal stable fields only
        /// </summary>
        public CombatIntentQueueValidationSnapshot GetQueueValidationSnapshot()
        {
            var frozen = GetFrozenQueueForCurrentTick();
            return CombatIntentQueueValidationSnapshot.FromFrozen(frozen);
        }

        public CombatIntentQueueDiagnosticsSnapshot GetDiagnosticsSnapshot()
        {
            return new CombatIntentQueueDiagnosticsSnapshot(
                structuralRejectCount: _structuralRejectCount,
                overflowRejectCount: _overflowRejectCount,
                peakStagingUsage: _peakStagingUsage,
                lastFrozenCount: _lastFrozenCount);
        }

        public void ResetSessionState()
        {
            foreach (var bucket in _stagedBySubmitTick.Values)
                _stagingBucketPool.Return(bucket);

            _stagedBySubmitTick.Clear();

            foreach (var snapshot in _frozenSnapshotsByTick.Values)
                _frozenSnapshotPool.Return(snapshot);

            _frozenSnapshotsByTick.Clear();
            _sequenceCounters.Clear();

            _structuralRejectCount = 0;
            _overflowRejectCount = 0;
            _peakStagingUsage = 0;
            _lastFrozenCount = 0;

            var resetSnapshot = _frozenSnapshotPool.Rent();
            resetSnapshot.Commit(_tickSource.CurrentTick, 0);
            _currentFrozen = resetSnapshot;
            _frozenSnapshotsByTick[_currentFrozen.AuthoritativeTick] = _currentFrozen;
        }

        private void HandleTickAdvanced(int newTick)
        {
            // Tick boundary semantics:
            // - Submissions received during tick (newTick - 1) become frozen queue for tick newTick.
            int sourceSubmitTick = newTick - 1;
            FreezeForTick(newTick, sourceSubmitTick);

            // Runtime hygiene only (not persistence): prune old staging buffers.
            PruneStaging(keepFromTickInclusive: newTick - 4);
        }

        private void FreezeForTick(int frozenTick, int sourceSubmitTick)
        {
            if (!_stagedBySubmitTick.TryGetValue(sourceSubmitTick, out var staged) || staged.SubmissionsCount == 0)
            {
                if (_stagedBySubmitTick.TryGetValue(sourceSubmitTick, out var emptyBucket))
                {
                    _stagedBySubmitTick.Remove(sourceSubmitTick);
                    emptyBucket.Reset();
                    _stagingBucketPool.Return(emptyBucket);
                }

                var emptySnapshot = _frozenSnapshotPool.Rent();
                emptySnapshot.Commit(frozenTick, 0);
                _currentFrozen = emptySnapshot;
                _frozenSnapshotsByTick[frozenTick] = emptySnapshot;
                _lastFrozenCount = 0;
                return;
            }

            // Deterministic ordering inputs ONLY:
            // 1) actor_entity_id (ordinal)
            // 2) intent_id (ordinal) -- used as a stable identifier for ordering; no client_nonce involvement
            //
            // NOTE: Ordering must not depend on arrival time or any client-supplied correlation fields.
            staged.Sort(StagedSubmissionComparer.Instance);

            var snapshot = _frozenSnapshotPool.Rent();
            var buffer = snapshot.AcquireBuffer(staged.SubmissionsCount);

            for (int i = 0; i < staged.SubmissionsCount; i++)
            {
                var s = staged[i];
                int seq = NextSequenceForActor(frozenTick, s.Submission.ActorEntityId!);

                // Freeze payload immutably at tick boundary:
                // - Deep-copy/clamp to immutable read-only structures
                // - After freeze, no caller can mutate payload data through references.
                var frozenPayload = PayloadFreezer.DeepFreeze(s.Submission.Payload);

                buffer[i] = new FrozenIntentRecord(
                    intentId: s.Submission.IntentId!,
                    intentType: s.Submission.IntentType,
                    actorEntityId: s.Submission.ActorEntityId!,
                    submitTick: s.SubmitTick,
                    deterministicSequence: seq,
                    payload: frozenPayload
                );
            }

            snapshot.Commit(frozenTick, staged.SubmissionsCount);
            _currentFrozen = snapshot;
            _frozenSnapshotsByTick[frozenTick] = snapshot;
            _lastFrozenCount = staged.SubmissionsCount;

            _stagedBySubmitTick.Remove(sourceSubmitTick);
            staged.Reset();
            _stagingBucketPool.Return(staged);
        }

        private int NextSequenceForActor(int frozenTick, string actorId)
        {
            var key = (frozenTick, actorId);
            if (!_sequenceCounters.TryGetValue(key, out int current))
                current = 0;

            current++;
            _sequenceCounters[key] = current;
            return current;
        }

        private void PruneStaging(int keepFromTickInclusive)
        {
            int count = _stagedBySubmitTick.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<int>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _stagedBySubmitTick)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                if (keys[i] < keepFromTickInclusive)
                {
                    if (_stagedBySubmitTick.TryGetValue(keys[i], out var bucket))
                    {
                        bucket.Reset();
                        _stagingBucketPool.Return(bucket);
                        _stagedBySubmitTick.Remove(keys[i]);
                    }
                }
            }

            ArrayPool<int>.Shared.Return(keys, clearArray: true);

            PruneFrozenSnapshots(keepFromTickInclusive);
            PruneSequenceCounters(keepFromTickInclusive);
        }

        private void PruneSequenceCounters(int keepFromTickInclusive)
        {
            int count = _sequenceCounters.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<(int FrozenTick, string ActorId)>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _sequenceCounters)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                if (keys[i].FrozenTick < keepFromTickInclusive)
                    _sequenceCounters.Remove(keys[i]);
            }

            ArrayPool<(int, string)>.Shared.Return(keys, clearArray: true);
        }

        private void PruneFrozenSnapshots(int keepFromTickInclusive)
        {
            int count = _frozenSnapshotsByTick.Count;
            if (count == 0)
                return;

            var keys = ArrayPool<int>.Shared.Rent(count);
            int index = 0;
            foreach (var kvp in _frozenSnapshotsByTick)
                keys[index++] = kvp.Key;

            for (int i = 0; i < index; i++)
            {
                int tick = keys[i];
                if (tick < keepFromTickInclusive && _frozenSnapshotsByTick.TryGetValue(tick, out var snapshot))
                {
                    _frozenSnapshotsByTick.Remove(tick);
                    _frozenSnapshotPool.Return(snapshot);
                }
            }

            ArrayPool<int>.Shared.Return(keys, clearArray: true);
        }

        private readonly struct StagedSubmission
        {
            public readonly CombatIntentSubmission Submission;
            public readonly int SubmitTick;

            public StagedSubmission(CombatIntentSubmission submission, int submitTick)
            {
                Submission = submission;
                SubmitTick = submitTick;
            }
        }

        private sealed class StagingBucket
        {
            private readonly List<StagedSubmission> _submissions;
            private readonly Dictionary<string, int> _actorCounts;

            public StagingBucket()
            {
                _submissions = new List<StagedSubmission>(SessionIntentCapPerTick);
                _actorCounts = new Dictionary<string, int>(ActorCountCapacityHint, StringComparer.Ordinal);
            }

            public int SubmissionsCount => _submissions.Count;

            public StagedSubmission this[int index] => _submissions[index];

            public void Prepare(int sessionCap)
            {
                _submissions.Clear();
                _actorCounts.Clear();
                _submissions.EnsureCapacity(sessionCap);

                if (_actorCounts.Comparer != StringComparer.Ordinal)
                    throw new InvalidOperationException("Actor count dictionary comparer changed unexpectedly.");
            }

            public int GetActorCount(string actorId)
            {
                if (_actorCounts.TryGetValue(actorId, out var count))
                    return count;

                return 0;
            }

            public void IncrementActor(string actorId)
            {
                if (_actorCounts.TryGetValue(actorId, out var count))
                    _actorCounts[actorId] = count + 1;
                else
                    _actorCounts[actorId] = 1;
            }

            public void AddSubmission(StagedSubmission submission)
            {
                _submissions.Add(submission);
            }

            public void Sort(IComparer<StagedSubmission> comparer)
            {
                _submissions.Sort(comparer);
            }

            public void Reset()
            {
                _submissions.Clear();
                _actorCounts.Clear();
            }
        }

        private sealed class StagingBucketPool
        {
            private readonly Stack<StagingBucket> _pool = new Stack<StagingBucket>();
            private readonly int _maxSize;

            public StagingBucketPool(int maxSize)
            {
                _maxSize = maxSize;
            }

            public StagingBucket Rent()
            {
                if (_pool.Count > 0)
                    return _pool.Pop();

                return new StagingBucket();
            }

            public void Return(StagingBucket bucket)
            {
                bucket.Reset();

                if (_pool.Count < _maxSize)
                    _pool.Push(bucket);
            }
        }

        private sealed class StagedSubmissionComparer : IComparer<StagedSubmission>
        {
            public static readonly StagedSubmissionComparer Instance = new StagedSubmissionComparer();

            public int Compare(StagedSubmission x, StagedSubmission y)
            {
                int actorCompare = string.CompareOrdinal(x.Submission.ActorEntityId ?? string.Empty, y.Submission.ActorEntityId ?? string.Empty);
                if (actorCompare != 0)
                    return actorCompare;

                return string.CompareOrdinal(x.Submission.IntentId ?? string.Empty, y.Submission.IntentId ?? string.Empty);
            }
        }

        private enum OverflowPolicy
        {
            DropNewest,
            DropOldest
        }
    }

    // ---------------------------
    // Intake models + snapshots
    // ---------------------------

    public sealed class CombatIntentSubmission
    {
        public string? IntentId { get; init; }
        public CombatIntentType IntentType { get; init; }
        public string? ActorEntityId { get; init; }

        // Optional per schema (correlation only; must not affect ordering)
        public string? ClientNonce { get; init; }

        // Variant fields represented inside Payload as a key/value map.
        public IReadOnlyDictionary<string, object?> Payload { get; init; } =
            new ReadOnlyDictionary<string, object?>(new Dictionary<string, object?>());
    }

    public enum CombatIntentType
    {
        CombatAttackIntent,
        CombatDefendIntent,
        CombatAbilityIntent,
        CombatMovementIntent,
        CombatInteractIntent,
        CombatCancelIntent
    }

    public sealed class FrozenQueueSnapshot
    {
        private FrozenIntentRecord[] _buffer;
        private int _count;
        private readonly FrozenIntentList _intentList;

        public int AuthoritativeTick { get; private set; }
        public IReadOnlyList<FrozenIntentRecord> Intents => _intentList;

        private FrozenQueueSnapshot()
        {
            _buffer = Array.Empty<FrozenIntentRecord>();
            _intentList = new FrozenIntentList();
        }

        internal FrozenIntentRecord[] AcquireBuffer(int requiredCapacity)
        {
            if (_buffer.Length < requiredCapacity)
            {
                if (_buffer.Length > 0)
                    ArrayPool<FrozenIntentRecord>.Shared.Return(_buffer, clearArray: true);

                _buffer = ArrayPool<FrozenIntentRecord>.Shared.Rent(requiredCapacity);
            }

            return _buffer;
        }

        internal void Commit(int authoritativeTick, int count)
        {
            AuthoritativeTick = authoritativeTick;
            _count = count;
            _intentList.Reset(_buffer, _count);
        }

        internal void Reset()
        {
            if (_buffer.Length > 0)
            {
                ArrayPool<FrozenIntentRecord>.Shared.Return(_buffer, clearArray: true);
                _buffer = Array.Empty<FrozenIntentRecord>();
            }

            _count = 0;
            AuthoritativeTick = 0;
            _intentList.Reset(Array.Empty<FrozenIntentRecord>(), 0);
        }

        public static FrozenQueueSnapshot Empty(int tick)
        {
            var snapshot = new FrozenQueueSnapshot();
            snapshot.Commit(tick, 0);
            return snapshot;
        }
    }

    internal sealed class FrozenQueueSnapshotPool
    {
        private readonly Stack<FrozenQueueSnapshot> _pool = new Stack<FrozenQueueSnapshot>();
        private readonly int _maxSize;

        public FrozenQueueSnapshotPool(int maxSize)
        {
            _maxSize = maxSize;
        }

        public FrozenQueueSnapshot Rent()
        {
            if (_pool.Count > 0)
                return _pool.Pop();

            return new FrozenQueueSnapshot();
        }

        public void Return(FrozenQueueSnapshot snapshot)
        {
            snapshot.Reset();
            if (_pool.Count < _maxSize)
                _pool.Push(snapshot);
        }
    }

    public readonly struct FrozenIntentRecord
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly string ActorEntityId;
        public readonly int SubmitTick;

        // Deterministic tie-breaker for per-actor intent ordering within the frozen tick.
        public readonly int DeterministicSequence;

        // Immutable, read-only payload as frozen at tick boundary.
        public readonly IReadOnlyDictionary<string, object?> Payload;

        public FrozenIntentRecord(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int submitTick,
            int deterministicSequence,
            IReadOnlyDictionary<string, object?> payload)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
            Payload = payload ?? throw new ArgumentNullException(nameof(payload));
        }
    }

    internal sealed class FrozenIntentList : IReadOnlyList<FrozenIntentRecord>
    {
        private FrozenIntentRecord[] _items = Array.Empty<FrozenIntentRecord>();
        private int _count;

        public FrozenIntentRecord this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));

                return _items[index];
            }
        }

        public int Count => _count;

        public void Reset(FrozenIntentRecord[] items, int count)
        {
            _items = items;
            _count = count;
        }

        public Enumerator GetEnumerator() => new Enumerator(_items, _count);

        IEnumerator<FrozenIntentRecord> IEnumerable<FrozenIntentRecord>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public struct Enumerator : IEnumerator<FrozenIntentRecord>
        {
            private readonly FrozenIntentRecord[] _items;
            private readonly int _count;
            private int _index;

            public Enumerator(FrozenIntentRecord[] items, int count)
            {
                _items = items;
                _count = count;
                _index = -1;
            }

            public FrozenIntentRecord Current => _items[_index];

            object IEnumerator.Current => Current;

            public void Dispose()
            {
            }

            public bool MoveNext()
            {
                int next = _index + 1;
                if (next >= _count)
                    return false;

                _index = next;
                return true;
            }

            public void Reset()
            {
                _index = -1;
            }
        }
    }

    // Deterministic validation snapshot for the harness.
    public sealed class CombatIntentQueueValidationSnapshot
    {
        public int AuthoritativeTick { get; }
        public IReadOnlyList<CombatIntentQueueValidationRow> Intents { get; }

        private CombatIntentQueueValidationSnapshot(int authoritativeTick, IReadOnlyList<CombatIntentQueueValidationRow> intents)
        {
            AuthoritativeTick = authoritativeTick;
            Intents = intents;
        }

        public static CombatIntentQueueValidationSnapshot FromFrozen(FrozenQueueSnapshot frozen)
        {
            var rows = new CombatIntentQueueValidationRow[frozen.Intents.Count];
            for (int i = 0; i < frozen.Intents.Count; i++)
            {
                var intent = frozen.Intents[i];
                rows[i] = new CombatIntentQueueValidationRow(
                    intentId: intent.IntentId,
                    intentType: intent.IntentType,
                    actorEntityId: intent.ActorEntityId,
                    submitTick: intent.SubmitTick,
                    deterministicSequence: intent.DeterministicSequence);
            }

            return new CombatIntentQueueValidationSnapshot(frozen.AuthoritativeTick, rows);
        }
    }

    public readonly struct CombatIntentQueueValidationRow
    {
        public readonly string IntentId;
        public readonly CombatIntentType IntentType;
        public readonly string ActorEntityId;
        public readonly int SubmitTick;
        public readonly int DeterministicSequence;

        public CombatIntentQueueValidationRow(
            string intentId,
            CombatIntentType intentType,
            string actorEntityId,
            int submitTick,
            int deterministicSequence)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntityId = actorEntityId;
            SubmitTick = submitTick;
            DeterministicSequence = deterministicSequence;
        }
    }

    // ---------------------------
    // Observable rejections
    // ---------------------------

    public sealed class IntentRejection
    {
        public string IntentId { get; }
        public string ActorEntityId { get; }
        public CombatIntentType IntentType { get; }
        public int AuthoritativeTick { get; }
        public string ReasonCode { get; }

        public IntentRejection(string intentId, string actorEntityId, CombatIntentType intentType, int authoritativeTick, string reasonCode)
        {
            IntentId = intentId;
            ActorEntityId = actorEntityId;
            IntentType = intentType;
            AuthoritativeTick = authoritativeTick;
            ReasonCode = reasonCode;
        }
    }

    public interface IIntentRejectionSink
    {
        void OnRejected(IntentRejection rejection);
    }

    public static class RejectReasonCodes
    {
        public const string MissingRequiredField = "MissingRequiredField";
        public const string InvalidIntentType = "InvalidIntentType";
        public const string InvalidEntityId = "InvalidEntityId";
        public const string ForbiddenFieldPresent = "ForbiddenFieldPresent";
        public const string InvalidContextValue = "InvalidContextValue";
        public const string InvalidMovementMode = "InvalidMovementMode";
        public const string InvalidPayloadShape = "InvalidPayloadShape";
        public const string OverflowSessionIntentCap = "OverflowSessionIntentCap";
        public const string OverflowActorIntentCap = "OverflowActorIntentCap";
    }

    public readonly struct IntakeReceipt
    {
        public readonly string IntentId;
        public readonly int SubmitTick;
        public readonly bool IsRejected;
        public readonly string ReasonCode;

        private IntakeReceipt(string intentId, int submitTick, bool isRejected, string reasonCode)
        {
            IntentId = intentId;
            SubmitTick = submitTick;
            IsRejected = isRejected;
            ReasonCode = reasonCode;
        }

        public static IntakeReceipt Staged(string intentId, int submitTick) =>
            new IntakeReceipt(intentId, submitTick, isRejected: false, reasonCode: string.Empty);

        public static IntakeReceipt Rejected(string intentId, int submitTick, string reasonCode) =>
            new IntakeReceipt(intentId, submitTick, isRejected: true, reasonCode: reasonCode);
    }

    public readonly struct CombatIntentQueueDiagnosticsSnapshot
    {
        public readonly long StructuralRejectCount;
        public readonly long OverflowRejectCount;
        public readonly int PeakStagingUsage;
        public readonly int LastFrozenCount;

        public CombatIntentQueueDiagnosticsSnapshot(long structuralRejectCount, long overflowRejectCount, int peakStagingUsage, int lastFrozenCount)
        {
            StructuralRejectCount = structuralRejectCount;
            OverflowRejectCount = overflowRejectCount;
            PeakStagingUsage = peakStagingUsage;
            LastFrozenCount = lastFrozenCount;
        }
    }

    // ---------------------------
    // Tick + entity id validation abstractions
    // ---------------------------

    public interface ITickSource
    {
        int CurrentTick { get; }
        event Action<int> OnTickAdvanced; // newTick
    }

    public interface IEntityIdValidator
    {
        bool IsValidEntityId(string entityId);
        bool IsValidInteractableId(string interactableId);
    }

    // ---------------------------
    // Payload freezing (immutable snapshot integrity)
    // ---------------------------

    internal static class PayloadFreezer
    {
        public static IReadOnlyDictionary<string, object?> DeepFreeze(IReadOnlyDictionary<string, object?> payload)
        {
            if (payload == null) throw new ArgumentNullException(nameof(payload));

            var copy = new Dictionary<string, object?>(payload.Count, StringComparer.Ordinal);
            foreach (var kv in payload)
            {
                copy[kv.Key] = DeepFreezeValue(kv.Value);
            }

            return new ReadOnlyDictionary<string, object?>(copy);
        }

        private static object? DeepFreezeValue(object? value)
        {
            if (value == null) return null;

            // Primitive/immutable types can pass through.
            if (value is string) return value;
            if (value is bool) return value;
            if (value is int) return value;
            if (value is long) return value;
            if (value is float) return value;
            if (value is double) return value;
            if (value is decimal) return value;

            // Dictionary-like: recursively freeze into ReadOnlyDictionary.
            if (value is IReadOnlyDictionary<string, object?> roDict)
            {
                var nested = new Dictionary<string, object?>(roDict.Count, StringComparer.Ordinal);
                foreach (var kv in roDict)
                    nested[kv.Key] = DeepFreezeValue(kv.Value);

                return new ReadOnlyDictionary<string, object?>(nested);
            }

            if (value is Dictionary<string, object?> dict)
            {
                var nested = new Dictionary<string, object?>(dict.Count, StringComparer.Ordinal);
                foreach (var kv in dict)
                    nested[kv.Key] = DeepFreezeValue(kv.Value);

                return new ReadOnlyDictionary<string, object?>(nested);
            }

            // Lists/arrays: freeze to read-only list by value-freezing elements.
            if (value is IReadOnlyList<object?> roList)
            {
                var list = new List<object?>(roList.Count);
                foreach (var v in roList)
                    list.Add(DeepFreezeValue(v));

                return new ReadOnlyCollection<object?>(list);
            }

            if (value is List<object?> listIn)
            {
                var list = new List<object?>(listIn.Count);
                foreach (var v in listIn)
                    list.Add(DeepFreezeValue(v));

                return new ReadOnlyCollection<object?>(list);
            }

            // Unknown reference types are not permitted for a frozen payload snapshot.
            // Treat as structural invalid shape at intake time (validator should prevent this).
            return value;
        }
    }

    // ---------------------------
    // Structural schema validation (Stage 11.2 only)
    // ---------------------------

    internal static class CombatIntentStructuralValidator
    {
        private static readonly HashSet<string> ForbiddenKeys = new(StringComparer.Ordinal)
        {
            "damage_amount",
            "damage_kind_key",
            "damage_tags",
            "mitigated_amount",
            "mitigation_kind_key",
            "mitigation_tags",
            "produced_outcome_ids",
            "result_status",
            "authoritative_tick",
            "resolved_intent_id",
            "outcome_id",
            "event_id",
            "event_type",
        };

        public static bool TryValidate(
            CombatIntentSubmission submission,
            IEntityIdValidator entityIdValidator,
            out RejectInfo reject)
        {
            reject = default;

            if (submission.Payload == null)
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "Payload is null.");
                return false;
            }

            if (string.IsNullOrWhiteSpace(submission.IntentId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "intent_id missing.");
                return false;
            }

            if (string.IsNullOrWhiteSpace(submission.ActorEntityId))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "actor_entity_id missing.");
                return false;
            }

            if (!entityIdValidator.IsValidEntityId(submission.ActorEntityId!))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "actor_entity_id invalid.");
                return false;
            }

            foreach (var k in submission.Payload.Keys)
            {
                if (ForbiddenKeys.Contains(k))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.ForbiddenFieldPresent, $"Forbidden field present: {k}");
                    return false;
                }
            }

            if (submission.Payload.TryGetValue("intent_type", out var itRaw) && itRaw is string itStr)
            {
                if (!string.Equals(itStr, submission.IntentType.ToString(), StringComparison.Ordinal))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidIntentType, "intent_type mismatch.");
                    return false;
                }
            }

            switch (submission.IntentType)
            {
                case CombatIntentType.CombatAttackIntent:
                    return ValidateAttack(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatDefendIntent:
                    return ValidateDefend(submission, out reject);

                case CombatIntentType.CombatAbilityIntent:
                    return ValidateAbility(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatMovementIntent:
                    return ValidateMovement(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatInteractIntent:
                    return ValidateInteract(submission, entityIdValidator, out reject);

                case CombatIntentType.CombatCancelIntent:
                    return ValidateCancel(submission, out reject);

                default:
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidIntentType, "Unknown intent type.");
                    return false;
            }
        }

        private static bool ValidateAttack(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (s.Payload.TryGetValue("target_entity_id", out var targetRaw) && targetRaw != null)
            {
                if (targetRaw is not string targetStr || string.IsNullOrWhiteSpace(targetStr) || !v.IsValidEntityId(targetStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (s.Payload.TryGetValue("attack_profile_key", out var profileRaw) && profileRaw != null)
            {
                if (profileRaw is not string profileStr || string.IsNullOrWhiteSpace(profileStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "attack_profile_key invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateDefend(CombatIntentSubmission s, out RejectInfo reject)
        {
            reject = default;

            if (s.Payload.TryGetValue("defend_profile_key", out var profileRaw) && profileRaw != null)
            {
                if (profileRaw is not string profileStr || string.IsNullOrWhiteSpace(profileStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "defend_profile_key invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateAbility(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("ability_key", out var abilityRaw) || abilityRaw is not string abilityKey || string.IsNullOrWhiteSpace(abilityKey))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "ability_key missing.");
                return false;
            }

            if (s.Payload.TryGetValue("target_entity_id", out var targetRaw) && targetRaw != null)
            {
                if (targetRaw is not string targetStr || string.IsNullOrWhiteSpace(targetStr) || !v.IsValidEntityId(targetStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (s.Payload.TryGetValue("ability_context", out var ctxRaw) && ctxRaw != null)
            {
                if (!IsIdentifiersOnlyObject(ctxRaw))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidContextValue, "ability_context must be identifiers-only.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateMovement(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("movement_mode", out var modeRaw) || modeRaw is not string modeStr || string.IsNullOrWhiteSpace(modeStr))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "movement_mode missing.");
                return false;
            }

            if (!string.Equals(modeStr, "Translate", StringComparison.Ordinal) &&
                !string.Equals(modeStr, "Strafe", StringComparison.Ordinal) &&
                !string.Equals(modeStr, "Backstep", StringComparison.Ordinal))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidMovementMode, "movement_mode invalid.");
                return false;
            }

            if (s.Payload.TryGetValue("target_entity_id", out var targetRaw) && targetRaw != null)
            {
                if (targetRaw is not string targetStr || string.IsNullOrWhiteSpace(targetStr) || !v.IsValidEntityId(targetStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "target_entity_id invalid.");
                    return false;
                }
            }

            if (s.Payload.TryGetValue("movement_context", out var ctxRaw) && ctxRaw != null)
            {
                if (!IsIdentifiersOnlyObject(ctxRaw))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidContextValue, "movement_context must be identifiers-only.");
                    return false;
                }
            }

            // Structural ban on vector/tuning fields.
            if (s.Payload.ContainsKey("velocity") || s.Payload.ContainsKey("distance") || s.Payload.ContainsKey("direction") ||
                s.Payload.ContainsKey("x") || s.Payload.ContainsKey("y") || s.Payload.ContainsKey("z"))
            {
                reject = RejectInfo.Of(RejectReasonCodes.ForbiddenFieldPresent, "Movement vector/tuning fields are not permitted.");
                return false;
            }

            return true;
        }

        private static bool ValidateInteract(CombatIntentSubmission s, IEntityIdValidator v, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("interactable_id", out var idRaw) || idRaw is not string iid || string.IsNullOrWhiteSpace(iid))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "interactable_id missing.");
                return false;
            }

            if (!v.IsValidInteractableId(iid))
            {
                reject = RejectInfo.Of(RejectReasonCodes.InvalidEntityId, "interactable_id invalid.");
                return false;
            }

            if (s.Payload.TryGetValue("interaction_kind", out var kindRaw) && kindRaw != null)
            {
                if (kindRaw is not string kindStr || string.IsNullOrWhiteSpace(kindStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "interaction_kind invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool ValidateCancel(CombatIntentSubmission s, out RejectInfo reject)
        {
            reject = default;

            if (!s.Payload.TryGetValue("cancel_target_intent_id", out var idRaw) || idRaw is not string tid || string.IsNullOrWhiteSpace(tid))
            {
                reject = RejectInfo.Of(RejectReasonCodes.MissingRequiredField, "cancel_target_intent_id missing.");
                return false;
            }

            if (s.Payload.TryGetValue("cancel_reason", out var reasonRaw) && reasonRaw != null)
            {
                if (reasonRaw is not string reasonStr || string.IsNullOrWhiteSpace(reasonStr))
                {
                    reject = RejectInfo.Of(RejectReasonCodes.InvalidPayloadShape, "cancel_reason invalid.");
                    return false;
                }
            }

            return true;
        }

        private static bool IsIdentifiersOnlyObject(object ctxRaw)
        {
            if (ctxRaw is IReadOnlyDictionary<string, object?> roDict)
            {
                foreach (var kv in roDict)
                {
                    if (kv.Value == null) continue;
                    if (kv.Value is string s && !string.IsNullOrWhiteSpace(s)) continue;
                    return false;
                }
                return true;
            }

            if (ctxRaw is Dictionary<string, object?> dict)
            {
                foreach (var kv in dict)
                {
                    if (kv.Value == null) continue;
                    if (kv.Value is string s && !string.IsNullOrWhiteSpace(s)) continue;
                    return false;
                }
                return true;
            }

            return false;
        }

        internal readonly struct RejectInfo
        {
            public readonly string ReasonCode;
            public readonly string Details;

            private RejectInfo(string reasonCode, string details)
            {
                ReasonCode = reasonCode;
                Details = details;
            }

            public static RejectInfo Of(string reasonCode, string details) => new RejectInfo(reasonCode, details);
        }
    }
}
