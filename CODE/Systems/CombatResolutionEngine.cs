// CombatResolutionEngine.cs
// NOTE: Save location must follow existing project structure.
// This file implements CombatResolutionEngine only.
// No state mutation, no damage application, no events, no persistence.

using System;
using System.Buffers;
using System.Collections;
using System.Collections.Generic;
using Caelmor.Runtime.Tick;

namespace Caelmor.Combat
{
    /// <summary>
    /// CombatResolutionEngine
    ///
    /// Responsibilities:
    /// - Consume ordered, validated intents (Stage 12.2)
    /// - Execute canonical resolution order (Stage 10.3)
    /// - Produce CombatOutcome records ONLY (Stage 11.2 schemas)
    ///
    /// Hard guarantees:
    /// - Stateless and side-effect free
    /// - Deterministic (same inputs → same outputs)
    /// - No combat state mutation
    /// - No damage application
    /// - No mitigation application
    /// - No event emission
    /// - No persistence
    /// </summary>
    public sealed class CombatResolutionEngine
    {
        public CombatResolutionResult Resolve(GatedIntentBatch gatedBatch)
        {
            if (gatedBatch == null) throw new ArgumentNullException(nameof(gatedBatch));

            int intentCount = gatedBatch.AcceptedIntentsInOrder.Count;
            var outcomesBuffer = ArrayPool<CombatOutcome>.Shared.Rent(Math.Max(intentCount, 1));
            var preIntentIds = ArrayPool<string>.Shared.Rent(Math.Max(intentCount, 1));
            var postOutcomeIds = ArrayPool<string>.Shared.Rent(Math.Max(intentCount, 1));

            for (int i = 0; i < intentCount; i++)
            {
                var intent = gatedBatch.AcceptedIntentsInOrder[i];
                preIntentIds[i] = intent.IntentId;

                // Resolution must never short-circuit.
                // Each intent is processed deterministically.
                var outcome = ResolveSingleIntent(intent, gatedBatch.AuthoritativeTick);

                outcomesBuffer[i] = outcome;
                postOutcomeIds[i] = outcome.IntentId;
            }

            var preSnapshot = CombatResolutionSnapshot.CreatePre(
                gatedBatch.AuthoritativeTick,
                new PooledStringList(preIntentIds, intentCount));

            var postSnapshot = CombatResolutionSnapshot.CreatePost(
                gatedBatch.AuthoritativeTick,
                new PooledStringList(postOutcomeIds, intentCount));

            return CombatResolutionResult.Create(
                authoritativeTick: gatedBatch.AuthoritativeTick,
                outcomesBuffer: outcomesBuffer,
                outcomeCount: intentCount,
                preIntentIds: preIntentIds,
                postOutcomeIds: postOutcomeIds,
                preSnapshot: preSnapshot,
                postSnapshot: postSnapshot);
        }

        private static CombatOutcome ResolveSingleIntent(
            FrozenIntentRecord intent,
            int authoritativeTick)
        {
            // Dispatch strictly by intent type.
            // No state inspection, no mutation, no external reads.
            switch (intent.IntentType)
            {
                case CombatIntentType.CombatAttackIntent:
                    return ResolveAttack(intent, authoritativeTick);

                case CombatIntentType.CombatDefendIntent:
                    return ResolveDefend(intent, authoritativeTick);

                case CombatIntentType.CombatAbilityIntent:
                    return ResolveAbility(intent, authoritativeTick);

                case CombatIntentType.CombatMovementIntent:
                    return ResolveMovement(intent, authoritativeTick);

                case CombatIntentType.CombatInteractIntent:
                    return ResolveInteract(intent, authoritativeTick);

                case CombatIntentType.CombatCancelIntent:
                    return ResolveCancel(intent, authoritativeTick);

                default:
                    throw new InvalidOperationException(
                        $"Unhandled CombatIntentType during resolution: {intent.IntentType}");
            }
        }

        // ------------------------------------------------------------------
        // Intent-specific resolution (OUTCOME CONSTRUCTION ONLY)
        // ------------------------------------------------------------------

        private static CombatOutcome ResolveAttack(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntity: intent.ActorEntity,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.AttackProposed
            );
        }

        private static CombatOutcome ResolveDefend(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntity: intent.ActorEntity,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.DefenseProposed
            );
        }

        private static CombatOutcome ResolveAbility(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntity: intent.ActorEntity,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.AbilityProposed
            );
        }

        private static CombatOutcome ResolveMovement(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntity: intent.ActorEntity,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.MovementProposed
            );
        }

        private static CombatOutcome ResolveInteract(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntity: intent.ActorEntity,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.InteractionProposed
            );
        }

        private static CombatOutcome ResolveCancel(FrozenIntentRecord intent, int tick)
        {
            return CombatOutcome.IntentResolved(
                intentId: intent.IntentId,
                intentType: intent.IntentType,
                actorEntity: intent.ActorEntity,
                authoritativeTick: tick,
                outcomeKind: CombatOutcomeKind.CancellationEvaluated
            );
        }
    }

    // ------------------------------------------------------------------
    // Resolution Outputs
    // ------------------------------------------------------------------

    public sealed class CombatResolutionResult
    {
        private CombatOutcome[] _outcomesBuffer;
        private string[] _preIntentIds;
        private string[] _postOutcomeIds;
        private bool _released;

        public int AuthoritativeTick { get; private set; }
        public OutcomeListView OutcomesInOrder { get; private set; }
        public CombatResolutionSnapshot PreResolutionSnapshot { get; private set; }
        public CombatResolutionSnapshot PostResolutionSnapshot { get; private set; }

        private CombatResolutionResult()
        {
            _outcomesBuffer = Array.Empty<CombatOutcome>();
            _preIntentIds = Array.Empty<string>();
            _postOutcomeIds = Array.Empty<string>();
            OutcomesInOrder = new OutcomeListView(Array.Empty<CombatOutcome>(), 0);
            PreResolutionSnapshot = CombatResolutionSnapshot.CreatePre(0, PooledStringList.Empty);
            PostResolutionSnapshot = CombatResolutionSnapshot.CreatePost(0, PooledStringList.Empty);
        }

        private void Reset(
            int authoritativeTick,
            CombatOutcome[] outcomesBuffer,
            int outcomeCount,
            string[] preIntentIds,
            string[] postOutcomeIds,
            CombatResolutionSnapshot preSnapshot,
            CombatResolutionSnapshot postSnapshot)
        {
            AuthoritativeTick = authoritativeTick;
            _outcomesBuffer = outcomesBuffer ?? throw new ArgumentNullException(nameof(outcomesBuffer));
            _preIntentIds = preIntentIds ?? throw new ArgumentNullException(nameof(preIntentIds));
            _postOutcomeIds = postOutcomeIds ?? throw new ArgumentNullException(nameof(postOutcomeIds));
            OutcomesInOrder = new OutcomeListView(outcomesBuffer, outcomeCount);
            PreResolutionSnapshot = preSnapshot;
            PostResolutionSnapshot = postSnapshot;
            _released = false;
        }

        public static CombatResolutionResult Create(
            int authoritativeTick,
            CombatOutcome[] outcomesBuffer,
            int outcomeCount,
            string[] preIntentIds,
            string[] postOutcomeIds,
            CombatResolutionSnapshot preSnapshot,
            CombatResolutionSnapshot postSnapshot)
        {
            var result = CombatResolutionResultPool.Rent();
            result.Reset(authoritativeTick, outcomesBuffer, outcomeCount, preIntentIds, postOutcomeIds, preSnapshot, postSnapshot);
            return result;
        }

        public void Release()
        {
            if (_released)
                return;

            _released = true;

            if (_outcomesBuffer.Length > 0)
                ArrayPool<CombatOutcome>.Shared.Return(_outcomesBuffer, clearArray: true);

            if (_preIntentIds.Length > 0)
                ArrayPool<string>.Shared.Return(_preIntentIds, clearArray: true);

            if (_postOutcomeIds.Length > 0)
                ArrayPool<string>.Shared.Return(_postOutcomeIds, clearArray: true);

            _outcomesBuffer = Array.Empty<CombatOutcome>();
            _preIntentIds = Array.Empty<string>();
            _postOutcomeIds = Array.Empty<string>();
            OutcomesInOrder = new OutcomeListView(Array.Empty<CombatOutcome>(), 0);
            PreResolutionSnapshot = CombatResolutionSnapshot.CreatePre(0, PooledStringList.Empty);
            PostResolutionSnapshot = CombatResolutionSnapshot.CreatePost(0, PooledStringList.Empty);
            AuthoritativeTick = 0;

            CombatResolutionResultPool.Return(this);
        }
    }

    public readonly struct OutcomeListView : IReadOnlyList<CombatOutcome>
    {
        private readonly CombatOutcome[] _buffer;
        private readonly int _count;

        public OutcomeListView(CombatOutcome[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<CombatOutcome>();
            _count = count;
        }

        public int Count => _count;

        public CombatOutcome this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));

                return _buffer[index];
            }
        }

        public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

        IEnumerator<CombatOutcome> IEnumerable<CombatOutcome>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public struct Enumerator : IEnumerator<CombatOutcome>
        {
            private readonly CombatOutcome[] _buffer;
            private readonly int _count;
            private int _index;

            public Enumerator(CombatOutcome[] buffer, int count)
            {
                _buffer = buffer;
                _count = count;
                _index = -1;
            }

            public CombatOutcome Current => _buffer[_index];

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

    // ------------------------------------------------------------------
    // CombatOutcome (Schema-conformant, no application)
    // ------------------------------------------------------------------

    public readonly struct CombatOutcome
    {
        public string IntentId { get; }
        public CombatIntentType IntentType { get; }
        public EntityHandle ActorEntity { get; }
        public int AuthoritativeTick { get; }
        public CombatOutcomeKind OutcomeKind { get; }

        private CombatOutcome(
            string intentId,
            CombatIntentType intentType,
            EntityHandle actorEntity,
            int authoritativeTick,
            CombatOutcomeKind outcomeKind)
        {
            IntentId = intentId;
            IntentType = intentType;
            ActorEntity = actorEntity;
            AuthoritativeTick = authoritativeTick;
            OutcomeKind = outcomeKind;
        }

        public static CombatOutcome IntentResolved(
            string intentId,
            CombatIntentType intentType,
            EntityHandle actorEntity,
            int authoritativeTick,
            CombatOutcomeKind outcomeKind)
        {
            if (string.IsNullOrWhiteSpace(intentId))
                throw new InvalidOperationException("CombatOutcome requires intent_id.");

            return new CombatOutcome(
                intentId,
                intentType,
                actorEntity,
                authoritativeTick,
                outcomeKind
            );
        }
    }

    public enum CombatOutcomeKind
    {
        AttackProposed,
        DefenseProposed,
        AbilityProposed,
        MovementProposed,
        InteractionProposed,
        CancellationEvaluated
    }

    // ------------------------------------------------------------------
    // Validation Snapshots
    // ------------------------------------------------------------------

    public readonly struct CombatResolutionSnapshot
    {
        public int AuthoritativeTick { get; }
        public PooledStringList OrderedIntentIds { get; }
        public PooledStringList OrderedOutcomeIntentIds { get; }

        private CombatResolutionSnapshot(
            int authoritativeTick,
            PooledStringList orderedIntentIds,
            PooledStringList orderedOutcomeIntentIds)
        {
            AuthoritativeTick = authoritativeTick;
            OrderedIntentIds = orderedIntentIds;
            OrderedOutcomeIntentIds = orderedOutcomeIntentIds;
        }

        public static CombatResolutionSnapshot CreatePre(int tick, PooledStringList orderedIntentIds)
        {
            return new CombatResolutionSnapshot(tick, orderedIntentIds, PooledStringList.Empty);
        }

        public static CombatResolutionSnapshot CreatePost(int tick, PooledStringList orderedOutcomeIntentIds)
        {
            return new CombatResolutionSnapshot(tick, PooledStringList.Empty, orderedOutcomeIntentIds);
        }
    }

    public readonly struct PooledStringList : IReadOnlyList<string>
    {
        private readonly string[] _buffer;
        private readonly int _count;

        public PooledStringList(string[] buffer, int count)
        {
            _buffer = buffer ?? Array.Empty<string>();
            _count = count;
        }

        public static PooledStringList Empty => new PooledStringList(Array.Empty<string>(), 0);

        public int Count => _count;

        public string this[int index]
        {
            get
            {
                if ((uint)index >= (uint)_count)
                    throw new ArgumentOutOfRangeException(nameof(index));

                return _buffer[index];
            }
        }

        public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

        IEnumerator<string> IEnumerable<string>.GetEnumerator() => GetEnumerator();

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        public struct Enumerator : IEnumerator<string>
        {
            private readonly string[] _buffer;
            private readonly int _count;
            private int _index;

            public Enumerator(string[] buffer, int count)
            {
                _buffer = buffer;
                _count = count;
                _index = -1;
            }

            public string Current => _buffer[_index];

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

    internal static class CombatResolutionResultPool
    {
        private const int MaxPoolSize = 16;
        private static readonly Stack<CombatResolutionResult> _pool = new Stack<CombatResolutionResult>(MaxPoolSize);

        public static CombatResolutionResult Rent()
        {
            if (_pool.Count > 0)
                return _pool.Pop();

            return new CombatResolutionResult();
        }

        public static void Return(CombatResolutionResult result)
        {
            if (_pool.Count < MaxPoolSize)
                _pool.Push(result);
        }
    }

}
