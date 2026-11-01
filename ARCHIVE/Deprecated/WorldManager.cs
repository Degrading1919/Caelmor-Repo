using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Manages entities, zones, and world state.
    /// </summary>
    public class WorldManager
    {
        private readonly Dictionary<string, Entity> _entities =
            new Dictionary<string, Entity>();

        public IEnumerable<Entity> GetPlayerEntities()
        {
            foreach (var e in _entities.Values)
                if (e.IsPlayer) yield return e;
        }

        public Entity GetEntity(string id)
        {
            _entities.TryGetValue(id, out var e);
            return e;
        }

        // --------------------------------------------------------------------
        // Movement (host-authoritative)
        // --------------------------------------------------------------------
        public void ApplyPlayerMovementInputs(List<PlayerInput_Move> moves)
        {
            foreach (var m in moves)
            {
                if (!_entities.TryGetValue(m.PlayerId, out Entity entity)) continue;
                if (!entity.IsPlayer) continue;

                Vector2 input = m.Direction;
                if (input.sqrMagnitude <= float.Epsilon) continue;

                Vector3 dir = new Vector3(input.x, 0f, input.y).normalized;
                float distance = GameConstants.MOVE_SPEED * GameConstants.TICK_INTERVAL_SECONDS;

                entity.Position += dir * distance;
                entity.MarkPositionDirty();
            }
        }

        // --------------------------------------------------------------------
        // AI
        // --------------------------------------------------------------------
        public void UpdateAIControllers(long tickIndex, float tickDeltaSeconds)
        {
            foreach (Entity entity in _entities.Values)
            {
                if (entity.AIController == null) continue;
                entity.AIController.UpdateAI(tickIndex, this, tickDeltaSeconds);
            }
        }

        public Entity FindNearestPlayerInRadius(Vector3 pos, float radius)
        {
            Entity best = null;
            float bestSqr = radius * radius;

            foreach (Entity e in _entities.Values)
            {
                if (!e.IsPlayer) continue;
                float sqr = (e.Position - pos).sqrMagnitude;
                if (sqr <= bestSqr)
                {
                    best = e;
                    bestSqr = sqr;
                }
            }

            return best;
        }

        // --------------------------------------------------------------------
        // World state + snapshots
        // --------------------------------------------------------------------
        public void UpdateWorldState(long tickIndex)
        {
            // Resource nodes, chests, simple world flags, etc.
        }

        public TransformSnapshot BuildTransformSnapshot()
        {
            var snapshot = new TransformSnapshot
            {
                Transforms = new List<TransformSnapshot.Entry>()
            };

            foreach (Entity e in _entities.Values)
            {
                // For VS, we can just always include them; later we can do LOD / range filtering.
                snapshot.Transforms.Add(new TransformSnapshot.Entry
                {
                    EntityId  = e.EntityId,
                    Position  = e.Position,
                    RotationY = e.RotationY
                });
            }

            return snapshot;
        }

        public HpSnapshot BuildHpSnapshot()
        {
            var hpSnapshot = new HpSnapshot
            {
                Entries    = new List<HpSnapshot.Entry>(),
                ServerTime = Time.time
            };

            foreach (Entity e in _entities.Values)
            {
                if (e.Stats == null) continue;

                hpSnapshot.Entries.Add(new HpSnapshot.Entry
                {
                    EntityId  = e.EntityId,
                    CurrentHp = e.Stats.CurrentHp,
                    MaxHp     = e.Stats.MaxHp
                });
            }

            return hpSnapshot;
        }

        // Stub for persistence integration
        public bool HasStateChangesSinceLastTick()
        {
            return false;
        }
    }
}
