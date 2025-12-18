using System;
using System.Collections;
using System.Collections.Generic;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Replication;

namespace Caelmor.Runtime.Sessions
{
    /// <summary>
    /// Deterministic, allocation-free snapshot view of active sessions.
    /// Maintains a sorted in-memory index to avoid LINQ/iterator allocations on hot paths.
    /// Thread-safe via an internal gate; snapshot views reuse a pooled backing array.
    /// </summary>
    public sealed class DeterministicActiveSessionIndex : IActiveSessionIndex
    {
        private readonly object _gate;
        private SessionId[] _active = Array.Empty<SessionId>();
        private SessionId[] _snapshot = Array.Empty<SessionId>();
        private readonly SessionIdReadOnlyList _snapshotView = new SessionIdReadOnlyList();
        private int _count;

        public DeterministicActiveSessionIndex(object gate = null)
        {
            _gate = gate ?? new object();
        }

        public bool TryAdd(SessionId sessionId)
        {
            if (!sessionId.IsValid)
                return false;

            lock (_gate)
            {
                int insertAt = BinarySearch(sessionId);
                if (insertAt >= 0)
                    return false;

                insertAt = ~insertAt;
                EnsureCapacity(ref _active, _count + 1);

                if (insertAt < _count)
                    Array.Copy(_active, insertAt, _active, insertAt + 1, _count - insertAt);

                _active[insertAt] = sessionId;
                _count++;
                return true;
            }
        }

        public bool TryRemove(SessionId sessionId)
        {
            if (!sessionId.IsValid)
                return false;

            lock (_gate)
            {
                int index = BinarySearch(sessionId);
                if (index < 0)
                    return false;

                int tail = _count - index - 1;
                if (tail > 0)
                    Array.Copy(_active, index + 1, _active, index, tail);

                _active[--_count] = default;
                return true;
            }
        }

        public IReadOnlyList<SessionId> SnapshotSessionsDeterministic()
        {
            lock (_gate)
            {
                EnsureCapacity(ref _snapshot, _count);

                if (_count > 0)
                    Array.Copy(_active, 0, _snapshot, 0, _count);

                _snapshotView.Set(_snapshot, _count);
                return _snapshotView;
            }
        }

        private int BinarySearch(SessionId sessionId)
        {
            int lo = 0;
            int hi = _count - 1;

            while (lo <= hi)
            {
                int mid = lo + ((hi - lo) >> 1);
                int cmp = _active[mid].Value.CompareTo(sessionId.Value);

                if (cmp == 0)
                    return mid;

                if (cmp < 0)
                {
                    lo = mid + 1;
                }
                else
                {
                    hi = mid - 1;
                }
            }

            return ~lo;
        }

        private static void EnsureCapacity(ref SessionId[] buffer, int required)
        {
            if (buffer.Length >= required)
                return;

            int next = buffer.Length == 0 ? required : buffer.Length;
            while (next < required)
                next *= 2;

            var resized = new SessionId[next];
            if (buffer.Length > 0)
                Array.Copy(buffer, 0, resized, 0, buffer.Length);

            buffer = resized;
        }

        private sealed class SessionIdReadOnlyList : IReadOnlyList<SessionId>
        {
            private SessionId[] _buffer = Array.Empty<SessionId>();
            private int _count;

            public void Set(SessionId[] buffer, int count)
            {
                _buffer = buffer ?? Array.Empty<SessionId>();
                _count = count;
            }

            public SessionId this[int index]
            {
                get
                {
                    if ((uint)index >= (uint)_count)
                        throw new ArgumentOutOfRangeException(nameof(index));
                    return _buffer[index];
                }
            }

            public int Count => _count;

            public Enumerator GetEnumerator() => new Enumerator(_buffer, _count);

            IEnumerator<SessionId> IEnumerable<SessionId>.GetEnumerator() => GetEnumerator();

            IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

            public struct Enumerator : IEnumerator<SessionId>
            {
                private readonly SessionId[] _buffer;
                private readonly int _count;
                private int _index;

                public Enumerator(SessionId[] buffer, int count)
                {
                    _buffer = buffer ?? Array.Empty<SessionId>();
                    _count = count;
                    _index = -1;
                }

                public SessionId Current => _buffer[_index];

                object IEnumerator.Current => Current;

                public bool MoveNext()
                {
                    var next = _index + 1;
                    if (next >= _count)
                        return false;

                    _index = next;
                    return true;
                }

                public void Reset() => _index = -1;

                public void Dispose()
                {
                }
            }
        }
    }
}
