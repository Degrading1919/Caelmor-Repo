using System;
using System.Collections.Generic;
using System.Threading;
using Caelmor.Runtime.Diagnostics;
using Caelmor.Runtime.Onboarding;

namespace Caelmor.Runtime.Integration
{
    /// <summary>
    /// Thread-safe lifecycle mailbox for session disconnect/unregister cleanup.
    /// Enqueued from any thread; drained and applied on the tick thread deterministically.
    /// </summary>
    public sealed class TickThreadMailbox
    {
        private readonly object _gate = new object();
        private readonly Queue<LifecycleOp> _queue;
        private readonly int _maxOps;
        private readonly int _maxBytes;
        private int _currentBytes;

        private long _opsEnqueued;
        private long _opsApplied;
        private long _disconnectsApplied;
        private long _opsDropped;

        public TickThreadMailbox(RuntimeBackpressureConfig config)
        {
            if (config is null) throw new ArgumentNullException(nameof(config));
            _maxOps = config.MaxLifecycleOps;
            _maxBytes = config.MaxLifecycleOpBytes;
            _queue = new Queue<LifecycleOp>(_maxOps);
        }

        public long LifecycleOpsEnqueued => Interlocked.Read(ref _opsEnqueued);
        public long LifecycleOpsApplied => Interlocked.Read(ref _opsApplied);
        public long DisconnectsApplied => Interlocked.Read(ref _disconnectsApplied);
        public long LifecycleOpsDropped => Interlocked.Read(ref _opsDropped);

        public bool TryEnqueueDisconnect(SessionId sessionId)
            => TryEnqueue(new LifecycleOp(LifecycleOpKind.DisconnectSession, sessionId));

        public bool TryEnqueueUnregister(SessionId sessionId)
            => TryEnqueue(new LifecycleOp(LifecycleOpKind.UnregisterSession, sessionId));

        public bool TryEnqueueClearVisibility(SessionId sessionId)
            => TryEnqueue(new LifecycleOp(LifecycleOpKind.ClearVisibility, sessionId));

        public bool TryEnqueueCleanupReplication(SessionId sessionId)
            => TryEnqueue(new LifecycleOp(LifecycleOpKind.CleanupReplication, sessionId));

        public int Drain(ILifecycleApplier applier)
        {
            if (applier is null) throw new ArgumentNullException(nameof(applier));

            TickThreadAssert.AssertTickThread();

            int applied = 0;
            lock (_gate)
            {
                while (_queue.Count > 0)
                {
                    var op = _queue.Dequeue();
                    _currentBytes = Math.Max(0, _currentBytes - op.SizeBytes);
                    applied++;
                    Interlocked.Increment(ref _opsApplied);

                    if (op.Kind == LifecycleOpKind.DisconnectSession)
                        Interlocked.Increment(ref _disconnectsApplied);

                    applier.Apply(op);
                }
            }

            return applied;
        }

        public void Clear()
        {
            lock (_gate)
            {
                _queue.Clear();
                _currentBytes = 0;
            }
        }

        private bool TryEnqueue(LifecycleOp op)
        {
            if (!op.SessionId.IsValid)
                return false;

            if (op.SizeBytes > _maxBytes)
            {
                Interlocked.Increment(ref _opsDropped);
                return false;
            }

            lock (_gate)
            {
                while (_queue.Count > 0 &&
                       (_queue.Count >= _maxOps || _currentBytes + op.SizeBytes > _maxBytes))
                {
                    var dropped = _queue.Dequeue();
                    _currentBytes = Math.Max(0, _currentBytes - dropped.SizeBytes);
                    Interlocked.Increment(ref _opsDropped);
                }

                _queue.Enqueue(op);
                _currentBytes += op.SizeBytes;
                Interlocked.Increment(ref _opsEnqueued);
                return true;
            }
        }

        public readonly struct LifecycleOp
        {
            public readonly LifecycleOpKind Kind;
            public readonly SessionId SessionId;
            public readonly int SizeBytes;

            public LifecycleOp(LifecycleOpKind kind, SessionId sessionId)
            {
                Kind = kind;
                SessionId = sessionId;
                SizeBytes = 24;
            }
        }

        public enum LifecycleOpKind : byte
        {
            DisconnectSession = 0,
            UnregisterSession = 1,
            ClearVisibility = 2,
            CleanupReplication = 3
        }
    }

    public interface ILifecycleApplier
    {
        void Apply(TickThreadMailbox.LifecycleOp op);
    }
}
