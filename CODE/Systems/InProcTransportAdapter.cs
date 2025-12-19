using System;
using System.Buffers.Binary;

namespace Caelmor.Runtime.Transport
{
    /// <summary>
    /// In-process transport adapter for proof-of-life: injects inbound payloads into the router.
    /// </summary>
    public sealed class InProcTransportAdapter
    {
        private readonly PooledTransportRouter _router;

        public InProcTransportAdapter(PooledTransportRouter router)
        {
            _router = router ?? throw new ArgumentNullException(nameof(router));
        }

        public bool TryEnqueueInbound(SessionId sessionId, int payloadA, int payloadB, string commandType, long submitTick = 0)
        {
            Span<byte> payload = stackalloc byte[8];
            BinaryPrimitives.WriteInt32LittleEndian(payload.Slice(0, sizeof(int)), payloadA);
            BinaryPrimitives.WriteInt32LittleEndian(payload.Slice(sizeof(int), sizeof(int)), payloadB);

            return _router.EnqueueInbound(sessionId, payload, commandType, submitTick);
        }
    }
}
