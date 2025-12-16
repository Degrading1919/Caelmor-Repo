using System;
using System.Collections.Concurrent;

namespace Caelmor.Runtime.Tick
{
    /// <summary>
    /// Server-side registry controlling which runtime entities are eligible
    /// to participate in the fixed 10 Hz server tick.
    /// Pure execution primitive with no gameplay or scheduling logic.
    /// </summary>
    public sealed class TickEligibilityRegistry : ITickEligibilityRegistry
    {
        // Keyed by opaque runtime entity handle.
        private readonly ConcurrentDictionary<EntityHandle, byte> _eligible = new();

        /// <summary>
        /// Grants or revokes tick eligibility for a runtime entity.
        /// Idempotent and thread-safe.
        /// Returns false if the handle is invalid.
        /// </summary>
        public bool TrySetTickEligible(EntityHandle entity, bool isEligible)
        {
            if (!entity.IsValid)
                return false;

            if (isEligible)
            {
                _eligible.TryAdd(entity, 0);
            }
            else
            {
                _eligible.TryRemove(entity, out _);
            }

            return true;
        }

        /// <summary>
        /// Returns true if the entity is currently tick-eligible.
        /// Safe for concurrent access and side-effect free.
        /// </summary>
        public bool IsTickEligible(EntityHandle entity)
        {
            if (!entity.IsValid)
                return false;

            return _eligible.ContainsKey(entity);
        }

        /// <summary>
        /// Clears all eligibility state.
        /// Intended for controlled server teardown only.
        /// </summary>
        public void ClearAll()
        {
            _eligible.Clear();
        }
    }

}
