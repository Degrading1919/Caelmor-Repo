using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Simple tick-driven AI with steering-based return behavior.
    /// </summary>
    public class AIController
    {
        public Entity   Owner;
        public Vector3  LeashCenter;
        public float    LeashRadius;
        public float    DetectionRadius;

        private enum AIState
        {
            Idle,
            Patrol,
            Chase,
            Attack,
            Return
        }

        private AIState _state = AIState.Idle;

        public void UpdateAI(long tickIndex, WorldManager world, float tickDeltaSeconds)
        {
            Entity nearestPlayer = world.FindNearestPlayerInRadius(Owner.Position, DetectionRadius);

            if (nearestPlayer == null)
            {
                HandleNoTarget(tickDeltaSeconds);
                return;
            }

            float distToPlayer = Vector3.Distance(Owner.Position, nearestPlayer.Position);
            if (distToPlayer > DetectionRadius || distToPlayer > LeashRadius)
            {
                _state = AIState.Return;
                HandleReturnToLeash(tickDeltaSeconds);
                return;
            }

            if (distToPlayer > Owner.Combat.AttackRange)
            {
                _state = AIState.Chase;
                SteerTowards(nearestPlayer.Position, GameConstants.MOVE_SPEED, tickDeltaSeconds);
            }
            else
            {
                _state = AIState.Attack;
                Owner.Combat.IsAutoAttacking = true;
                Owner.Combat.TargetId        = nearestPlayer.EntityId;
            }
        }

        private void HandleNoTarget(float tickDeltaSeconds)
        {
            if (_state == AIState.Chase || _state == AIState.Attack)
                _state = AIState.Return;

            if (_state == AIState.Return)
            {
                HandleReturnToLeash(tickDeltaSeconds);
            }
            else if (_state == AIState.Idle)
            {
                // Remain idle for VS.
            }
        }

        private void HandleReturnToLeash(float tickDeltaSeconds)
        {
            Vector3 toCenter = LeashCenter - Owner.Position;
            float distance   = toCenter.magnitude;

            if (distance < 0.05f)
            {
                Owner.Position = LeashCenter;
                Owner.MarkPositionDirty();
                Owner.Combat.IsAutoAttacking = false;
                Owner.Combat.TargetId        = null;
                _state                       = AIState.Idle;
                return;
            }

            // 2.4 AI Steering Instead of Direct Return
            Vector3 dir = toCenter / distance; // normalized
            float moveDistance = GameConstants.MAX_LEASH_SPEED * tickDeltaSeconds;
            if (moveDistance > distance) moveDistance = distance;

            Owner.Position += dir * moveDistance;
            Owner.MarkPositionDirty();
        }

        private void SteerTowards(Vector3 targetPos, float speed, float tickDeltaSeconds)
        {
            Vector3 toTarget = targetPos - Owner.Position;
            float   distance = toTarget.magnitude;
            if (distance < 0.01f) return;

            Vector3 dir = toTarget / distance;
            float moveDistance = speed * tickDeltaSeconds;

            Owner.Position += dir * moveDistance;
            Owner.MarkPositionDirty();
        }
    }
}
