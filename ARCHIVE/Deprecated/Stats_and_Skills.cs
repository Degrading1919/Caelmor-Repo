using UnityEngine;

namespace Caelmor.VerticalSlice
{
    public class StatsSystem
    {
        public int ApplyDamage(Entity target, int incomingDamage)
        {
            int mitigated = Mathf.Max(0, incomingDamage - target.Stats.ArmorRating);
            target.Stats.CurrentHp = Mathf.Max(0, target.Stats.CurrentHp - mitigated);
            return target.Stats.CurrentHp;
        }
    }

    public class SkillSystem
    {
        public void AwardXp(Entity entity, string skillId, int amount)
        {
            if (entity.Skills == null) return;
            entity.Skills.AddXp(skillId, amount);
        }
    }
}
