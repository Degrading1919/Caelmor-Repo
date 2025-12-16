// File: Economy/Inventory/TableResourceGrantMapping.cs
// Placeholder deterministic mapping (hardcoded/table-driven).
// No tuning; counts are whatever the mapping provides.

using System;
using System.Collections.Generic;

namespace Caelmor.Economy.Inventory
{
    public sealed class TableResourceGrantMapping : IResourceGrantMapping
    {
        private readonly Dictionary<(string nodeTypeKey, string skillKey), ResourceGrant[]> _map;

        public TableResourceGrantMapping(Dictionary<(string nodeTypeKey, string skillKey), ResourceGrant[]> map)
        {
            _map = map ?? throw new ArgumentNullException(nameof(map));
        }

        public bool TryResolve(string nodeTypeKey, string gatheringSkillKey, out IReadOnlyList<ResourceGrant> grants)
        {
            if (_map.TryGetValue((nodeTypeKey, gatheringSkillKey), out var arr) && arr != null && arr.Length > 0)
            {
                grants = arr; // stable ordering by array order
                return true;
            }

            grants = Array.Empty<ResourceGrant>();
            return false;
        }
    }
}
