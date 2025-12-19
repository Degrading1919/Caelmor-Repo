using System;
using System.Buffers.Binary;
using System.Collections;
using System.Collections.Generic;
using Caelmor.Runtime;
using Caelmor.Runtime.Integration;
using Caelmor.Runtime.Onboarding;
using Caelmor.Runtime.Tick;
using Caelmor.Runtime.Transport;
using Caelmor.Runtime.WorldSimulation;
using Caelmor.Validation;

namespace Caelmor.Validation.Transport
{
    /// <summary>
    /// Minimal validation proving inbound transport frames reach the authoritative ingestor and freeze surfaces.
    /// </summary>
    public static class InboundTransportValidationScenarios
    {
        public static IReadOnlyList<IValidationScenario> GetScenarios()
        {
            return new IValidationScenario[] { new InboundPumpEndToEndScenario() };
        }

        private sealed class InboundPumpEndToEndScenario : IValidationScenario
        {
            public string Name => "transport_inbound_pump_end_to_end";

            public void Run(IAssert assert)
            {
                var config = RuntimeBackpressureConfig.Default;
                var transport = new PooledTransportRouter(config);
                var ingestor = new AuthoritativeCommandIngestor(config);
                var sessions = new DeterministicSessionIndex();
                var pump = new InboundPumpTickHook(transport, ingestor, sessions);
                var core = new WorldSimulationCore(new EmptyEntityIndex());

                core.RegisterPhaseHook(pump, orderKey: 0);

                var session = new SessionId(Guid.NewGuid());
                sessions.Add(session);

                Span<byte> payload = stackalloc byte[8];
                BinaryPrimitives.WriteInt32LittleEndian(payload.Slice(0, sizeof(int)), 42);
                BinaryPrimitives.WriteInt32LittleEndian(payload.Slice(sizeof(int)), 99);

                transport.EnqueueInbound(session, payload, commandType: "validation", submitTick: 0);

                core.ExecuteSingleTick();
                core.ExecuteSingleTick();

                var diagnostics = pump.Diagnostics;
                assert.True(diagnostics.InboundPumpTicksExecuted >= 2, "Inbound pump must execute each tick.");
                assert.True(diagnostics.InboundFramesRouted > 0, "Inbound frames must be routed from transport mailboxes.");
                assert.True(diagnostics.CommandsEnqueuedToIngestor > 0, "Commands must be bridged into the ingestor.");

                var frozen = pump.GetFrozenBatch(session);
                assert.True(frozen.Count > 0, "Frozen command batch must be populated after the pump runs.");

                core.Dispose();
                transport.Dispose();
            }

            private sealed class EmptyEntityIndex : ISimulationEntityIndex
            {
                private static readonly EntityHandle[] Empty = Array.Empty<EntityHandle>();

                public EntityHandle[] SnapshotEntitiesDeterministic() => Empty;
            }

            private sealed class DeterministicSessionIndex : IActiveSessionIndex
            {
                private readonly SessionId[] _buffer = new SessionId[8];
                private int _count;

                public void Add(SessionId sessionId)
                {
                    if (!sessionId.IsValid || _count >= _buffer.Length)
                        return;

                    _buffer[_count++] = sessionId;
                    Array.Sort(_buffer, 0, _count, SessionIdValueComparer.Instance);
                }

                public IReadOnlyList<SessionId> SnapshotSessionsDeterministic()
                {
                    return new SessionIdReadOnlyList(_buffer, _count);
                }
            }

            private readonly struct SessionIdReadOnlyList : IReadOnlyList<SessionId>
            {
                private readonly SessionId[] _source;
                private readonly int _count;

                public SessionIdReadOnlyList(SessionId[] source, int count)
                {
                    _source = source ?? Array.Empty<SessionId>();
                    _count = count;
                }

                public SessionId this[int index]
                {
                    get
                    {
                        if ((uint)index >= (uint)_count)
                            throw new ArgumentOutOfRangeException(nameof(index));

                        return _source[index];
                    }
                }

                public int Count => _count;

                public Enumerator GetEnumerator() => new Enumerator(_source, _count);

                IEnumerator<SessionId> IEnumerable<SessionId>.GetEnumerator() => GetEnumerator();

                IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

                public struct Enumerator : IEnumerator<SessionId>
                {
                    private readonly SessionId[] _source;
                    private readonly int _count;
                    private int _index;

                    public Enumerator(SessionId[] source, int count)
                    {
                        _source = source;
                        _count = count;
                        _index = -1;
                    }

                    public SessionId Current => _source[_index];

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
}
