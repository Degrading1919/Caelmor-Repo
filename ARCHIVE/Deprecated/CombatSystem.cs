using System.Collections.Generic;
using UnityEngine;

namespace Caelmor.VerticalSlice
{
    /// <summary>
    /// Host-side combat orchestration and XP routing.
    /// </summary>
    public class CombatSystem
    {
        public WorldManager   WorldManager   { get; set; }
        public StatsSystem    StatsSystem    { get; set; }
        public SkillSystem    SkillSystem    { get; set; }
        public NetworkManager NetworkManager { get; set; }

        public void ProcessAttackTimersAndIntents(long tickIndex, List<PlayerInput_Attack> attackCommands)
        {
            // Apply new intents from players
            foreach (PlayerInput_Attack cmd in attackCommands)
            {
                Entity attacker = WorldManager.GetEntity(cmd.PlayerId);
                if (attacker == null) continue;

                if (cmd.IsStart)
                {
                    StartAutoAttackOrAbility(attacker, cmd.TargetEntityId, cmd.AbilityId, tickIndex);
                }
                else
                {
                    StopAutoAttack(attacker);
                }
            }

            // Tick-based resolution
            foreach (Entity entity in WorldManager.GetPlayerEntities())
            {
                CombatComponent combat = entity.Combat;
                if (combat == null || !combat.IsAutoAttacking) continue;
                if (tickIndex < combat.NextAttackTick) continue;

                TryResolveAttack(entity, tickIndex);
            }

            // In a full implementation, you’d also tick enemy auto-attacks here.
        }

        private void StartAutoAttackOrAbility(Entity attacker, string targetId, string abilityId, long tickIndex)
        {
            Entity target = WorldManager.GetEntity(targetId);
            if (!ValidateTarget(attacker, target)) return;

            if (string.IsNullOrEmpty(abilityId))
            {
                attacker.Combat.IsAutoAttacking = true;
                attacker.Combat.TargetId        = targetId;
                attacker.Combat.AttackSpeedTicks = GetWeaponAttackSpeedTicks(attacker);
                attacker.Combat.NextAttackTick   = tickIndex + attacker.Combat.AttackSpeedTicks;
            }
            else
            {
                // Hook for special attacks in VS+.
            }
        }

        private void StopAutoAttack(Entity attacker)
        {
            attacker.Combat.IsAutoAttacking = false;
            attacker.Combat.TargetId        = null;
        }

        private void TryResolveAttack(Entity attacker, long tickIndex)
        {
            Entity target = WorldManager.GetEntity(attacker.Combat.TargetId);
            if (!ValidateTarget(attacker, target))
            {
                attacker.Combat.IsAutoAttacking = false;
                return;
            }

            if (!InAttackRange(attacker, target)) return;

            // Simple always-hit for VS; add hit-chance later.
            int damage = ComputeDamage(attacker, target);
            ApplyDamageAndXp(attacker, target, damage, tickIndex);

            attacker.Combat.NextAttackTick += attacker.Combat.AttackSpeedTicks;
        }

        // 2.2 XP Routing Logic — melee vs ranged
        private void ApplyDamageAndXp(Entity attacker, Entity target, int damage, long tickIndex)
        {
            int newHp  = StatsSystem.ApplyDamage(target, damage);
            bool isKill = newHp <= 0;

            if (isKill)
            {
                HandleDeath(attacker, target);
            }

            // XP routing: ranged vs melee based on weapon
            string skillId = IsRangedWeapon(attacker) ? "ranged" : "melee";
            int    xpAmount = GetXpValueForTarget(target);

            SkillSystem.AwardXp(attacker, skillId, xpAmount);

            // Emit combat result (still includes HP delta)
            var evt = new Event_CombatResult
            {
                TickIndex      = tickIndex,
                SourceEntityId = attacker.EntityId,
                TargetEntityId = target.EntityId,
                Damage         = damage,
                NewHp          = newHp,
                IsKill         = isKill,
                IsCrit         = false
            };

            NetworkManager.BroadcastCombatEvent(evt);
        }

        private bool IsRangedWeapon(Entity attacker)
        {
            if (attacker.Equipment == null) return false;

            string weaponId = attacker.Combat.WeaponItemId;
            if (string.IsNullOrEmpty(weaponId)) return false;

            if (!ContentDatabase.Items.TryGetValue(weaponId, out ItemDef itemDef)) return false;
            return itemDef.IsRanged;
        }

        // --------------------------------------------------------------------
        // Helper stubs (expand as needed)
        // --------------------------------------------------------------------
        private bool ValidateTarget(Entity attacker, Entity target)
        {
            return target != null && target.Stats != null;
        }

        private bool InAttackRange(Entity attacker, Entity target)
        {
            return Vector3.Distance(attacker.Position, target.Position) <= attacker.Combat.AttackRange;
        }

        private int ComputeDamage(Entity attacker, Entity target)
        {
            return attacker.Combat.AttackDamage;
        }

        private void HandleDeath(Entity attacker, Entity target)
        {
            // Drop loot, mark dead, etc. for VS.
        }

        private int GetXpValueForTarget(Entity target)
        {
            return 10; // simple for VS.
        }

        private int GetWeaponAttackSpeedTicks(Entity attacker)
        {
            return 10; // 1s per swing at 10 Hz tick.
        }
    }
}
