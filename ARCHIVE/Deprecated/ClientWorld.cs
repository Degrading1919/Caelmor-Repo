using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    public class ClientWorld : MonoBehaviour
    {
        private readonly Dictionary<string, ClientEntity> _entities =
            new Dictionary<string, ClientEntity>();

        public void ApplyTransformSnapshot(TransformSnapshot snapshot)
        {
            foreach (var t in snapshot.Transforms)
            {
                if (!_entities.TryGetValue(t.EntityId, out ClientEntity ce)) continue;
                ce.TargetPosition = t.Position;
                ce.RotationY      = t.RotationY;
            }
        }

        // 2.3 HP Sync Strategy — periodic HP snapshot
        public void ApplyHpSnapshot(HpSnapshot snapshot)
        {
            foreach (var e in snapshot.Entries)
            {
                if (!_entities.TryGetValue(e.EntityId, out ClientEntity ce)) continue;
                ce.CurrentHp = e.CurrentHp;
                ce.MaxHp     = e.MaxHp;
                ce.MarkHpDirty();
            }
        }

        private void Update()
        {
            float dt = Time.deltaTime;

            foreach (ClientEntity ce in _entities.Values)
            {
                ce.Position = Vector3.Lerp(
                    ce.Position,
                    ce.TargetPosition,
                    10f * dt
                );
            }
        }

        public ClientEntity GetOrCreateClientEntity(string entityId)
        {
            if (!_entities.TryGetValue(entityId, out ClientEntity ce))
            {
                ce = new ClientEntity { EntityId = entityId };
                _entities.Add(entityId, ce);
            }

            return ce;
        }
    }

    public class ClientEntity
    {
        public string   EntityId;
        public Vector3  Position;
        public Vector3  TargetPosition;
        public float    RotationY;
        public int      CurrentHp;
        public int      MaxHp;

        public void MarkHpDirty()
        {
            // Hook UI refresh here (e.g., HP bars).
        }
    }
}
