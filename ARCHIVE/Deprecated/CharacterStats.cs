// CharacterStats.cs
namespace Caelmor.VS
{
    /// <summary>
    /// Minimal Vertical Slice stat structure.
    /// Future expansions (v1 Core Systems) will add Accuracy, Evasion,
    /// CritChance, Resistances, Masteries, etc.
    /// </summary>
    public struct CharacterStats
    {
        public int AttackPower;
        public int Defense;

        public CharacterStats(int attack, int defense)
        {
            AttackPower = attack;
            Defense = defense;
        }
    }
}
