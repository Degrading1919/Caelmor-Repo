// - Active runtime code only.
// - Fixed 10 Hz authoritative tick. No tick-thread blocking I/O.
// - Zero/low GC steady state after warm-up: no per-tick allocations in hot paths (do not introduce any).
// - Bounded growth/backpressure with deterministic overflow + metrics.
// - Deterministic ordering. No Dictionary iteration order reliance.
// - Thread ownership must be explicit and enforced: tick-thread asserts OR mailbox marshalling.
// - Deterministic cleanup on disconnect/shutdown; no leaks.
// - AOT/IL2CPP safe patterns only.
using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Sessions;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.WorldSimulation;

namespace Caelmor.Combat
{
    public sealed class CombatEventBuffer : ICombatEventSink
    {
        private readonly CombatEvent[] _buffer;
        private readonly int _maxCount;
        private int _count;
        private int _currentTick;
        private bool _hasTick;

        private long _eventsBuffered;
        private long _eventsDroppedOverflow;
        private long _eventsDroppedTickMismatch;

        public CombatEventBuffer(int maxEventsPerTick)
        {
            if (maxEventsPerTick <= 0) throw new ArgumentOutOfRangeException(nameof(maxEventsPerTick));
            _buffer = new CombatEvent[maxEventsPerTick];
            _maxCount = maxEventsPerTick;
        }

        public bool TryEmit(in CombatEvent combatEvent)
        {
            TickThreadAssert.AssertTickThread();
            if (combatEvent == null) throw new ArgumentNullException(nameof(combatEvent));

            int tick = combatEvent.AuthoritativeTick;
            if (!_hasTick)
            {
                _currentTick = tick;
                _hasTick = true;
            }
            else if (_currentTick != tick && _count > 0)
            {
                Interlocked.Increment(ref _eventsDroppedTickMismatch);
                return false;
            }
            else if (_currentTick != tick)
            {
                _currentTick = tick;
            }

            if (_count >= _maxCount)
            {
                Interlocked.Increment(ref _eventsDroppedOverflow);
                return false;
            }

            _buffer[_count++] = combatEvent;
            Interlocked.Increment(ref _eventsBuffered);
            return true;
        }

        public CombatEventBatch Drain(int authoritativeTick)
        {
            TickThreadAssert.AssertTickThread();
            int batchTick = _hasTick ? _currentTick : authoritativeTick;

            var batch = new CombatEventBatch(batchTick, _buffer, _count);

            for (int i = 0; i < _count; i++)
                _buffer[i] = null;

            _count = 0;
            _currentTick = 0;
            _hasTick = false;

            return batch;
        }

        public long CombatEventsBuffered => Interlocked.Read(ref _eventsBuffered);
        public long CombatEventsDroppedOverflow => Interlocked.Read(ref _eventsDroppedOverflow);
        public long CombatEventsDroppedTickMismatch => Interlocked.Read(ref _eventsDroppedTickMismatch);
    }

    public sealed class CombatReplicationTickHook : ITickPhaseHook
    {
        private readonly CombatEventBuffer _buffer;
        private readonly CombatReplicationSystem _replication;
        private long _combatEventsDrained;

        public CombatReplicationTickHook(CombatEventBuffer buffer, CombatReplicationSystem replication)
        {
            _buffer = buffer ?? throw new ArgumentNullException(nameof(buffer));
            _replication = replication ?? throw new ArgumentNullException(nameof(replication));
        }

        public void OnPreTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
        }

        public void OnPostTick(SimulationTickContext context, IReadOnlyList<EntityHandle> eligibleEntities)
        {
            TickThreadAssert.AssertTickThread();
            var batch = _buffer.Drain(checked((int)context.TickIndex));
            if (batch.Count > 0)
                Interlocked.Add(ref _combatEventsDrained, batch.Count);
            _replication.Replicate(in batch);
        }

        public long CombatEventsDrained => Interlocked.Read(ref _combatEventsDrained);
    }

    public sealed class ActiveSessionCombatClientRegistry : IClientRegistry
    {
        private readonly IActiveSessionIndex _sessions;

        public ActiveSessionCombatClientRegistry(IActiveSessionIndex sessions)
        {
            _sessions = sessions ?? throw new ArgumentNullException(nameof(sessions));
        }

        public IReadOnlyList<SessionId> GetSubscribers(string combatContextId)
        {
            return _sessions.SnapshotSessionsDeterministic();
        }
    }

    public sealed class AlwaysVisibleCombatVisibilityPolicy : IVisibilityPolicy
    {
        public bool IsEventVisibleToClient(CombatEvent combatEvent, SessionId clientId) => true;
    }

    public sealed class NullCombatNetworkSender : INetworkSender
    {
        public void SendReliable(SessionId clientId, CombatEventPayload payload, int authoritativeTick)
        {
        }
    }

    public sealed class NullCombatReplicationValidationSink : IReplicationValidationSink
    {
        public void RecordReplicatedPayload(SessionId clientId, int authoritativeTick, CombatEventPayload payload)
        {
        }
    }
}
