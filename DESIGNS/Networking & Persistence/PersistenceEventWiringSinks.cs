// File: Persistence/PersistenceEventWiringSinks.cs
// Stage 8.7 — event sinks that mark dirty + request checkpoint.
// This avoids modifying gameplay systems while ensuring correct save boundaries. :contentReference[oaicite:3]{index=3}

using System;
using Caelmor.Economy.Inventory;
using Caelmor.Economy.Crafting;

namespace Caelmor.Persistence
{
    public sealed class ResourceGrantPersistenceSink : IResourceGrantEventSink
    {
        private readonly ISaveRequestSink _save;
        private readonly IResourceGrantEventSink _downstream;

        public ResourceGrantPersistenceSink(ISaveRequestSink save, IResourceGrantEventSink downstream)
        {
            _save = save ?? throw new ArgumentNullException(nameof(save));
            _downstream = downstream ?? throw new ArgumentNullException(nameof(downstream));
        }

        public void Emit(ResourceGrantedEvent evt)
        {
            // Successful grant implies:
            // - Inventory mutated (PlayerSave dirty)
            // - Node depleted as part of same action (WorldSave dirty)
            // These MUST be flushed in the same checkpoint cycle. :contentReference[oaicite:4]{index=4}
            _save.MarkPlayerDirty(evt.PlayerId, "resource_granted");
            _save.MarkWorldDirty("node_depleted");
            _save.RequestCheckpoint("gather_action_mutation");

            _downstream.Emit(evt);
        }
    }

    public sealed class CraftingPersistenceSink : ICraftingExecutionEventSink
    {
        private readonly ISaveRequestSink _save;
        private readonly ICraftingExecutionEventSink _downstream;

        public CraftingPersistenceSink(ISaveRequestSink save, ICraftingExecutionEventSink downstream)
        {
            _save = save ?? throw new ArgumentNullException(nameof(save));
            _downstream = downstream ?? throw new ArgumentNullException(nameof(downstream));
        }

        public void Emit(CraftingExecutionResult evt)
        {
            // Only successful crafts mutate inventory.
            if (evt.Success)
            {
                _save.MarkPlayerDirty(evt.PlayerId, "craft_success");
                _save.RequestCheckpoint("craft_action_mutation");
            }

            _downstream.Emit(evt);
        }
    }
}
