🗂️ ENEMY FAMILY (Updated to Match VS Whitebox)

Aligned with encounter descriptions in
Lowmark_VS_Whitebox_v1.1.md
and using the family schema ().

{
  "id": "lowmark_field_goblins",
  "region": "lowmark",
  "tier": "low",
  "base_stats": {
    "health": 20,
    "power": 5,
    "armor": 0,
    "speed": 1.1
  },
  "behavior": "skirmisher",
  "loot_table": "lt_field_goblin_basic"
}

Family Alignment Notes

Matches whitebox role as basic hostile melee enemy.

Behavior “skirmisher” suits the simple poke-attack cadence described in the Creek Crossing encounter.

Base stats are deliberately low to match the early-game readability requirement (Pillar B) .

🗂️ ENEMY VARIANT (Designed for Creek Crossing Encounter)

This variant mirrors the exact enemy described at the Bridge Path in the whitebox:

“1× Field Goblin (Tier 1) — simple poke every 2.8s, placed near the bridge.”
— Lowmark_VS_Whitebox_v1.1

Using the variant schema ():

{
  "id": "field_goblin_bridge_sentry",
  "family": "lowmark_field_goblins",
  "level": 2,
  "variant_modifiers": {
    "health": 4,
    "power": 1
  },
  "abilities": ["simple_poke"],
  "spawn_regions": ["lowmark_creek_crossing"]
}

Variant Alignment Notes

Level 2 fits the intended difficulty for an introductory combat encounter.

variant_modifiers lightly increase health/power while maintaining TTK 6–10 seconds per the whitebox.

abilities: ["simple_poke"] exactly matches the whitebox attack cadence (“poke every 2.8s”).

Spawn region references the POI path: “creek_crossing” per whitebox layout.

📘 Markdown Description (Context + Justification)
Field Goblins — Lowmark Enemy Family

Field Goblins represent the first true hostile faction encountered in Lowmark Vale.
They inhabit broken fences, abandoned farmsteads, creek crossings, and field margins — all POIs present in the VS zone.
Their role is to teach combat spacing, readable telegraphs, and simple aggro rules in a safe, isolated manner.

Family Traits

Small, quick, lightly armed skirmishers.

Fight in singles, occasionally pairs, but are intentionally spaced 8–12m apart (whitebox rule).

Telegraph a single, predictable melee poke.

Low pressure, no flanking, suitable for early-game onboarding.

Variant: Field Goblin — Bridge Sentry

This variant is placed at the Creek Crossing (Bridge Path) in the VS whitebox.
Its job is to introduce the player to:

First melee enemy

First aggro zone

First readable attack cadence

Behavior Summary

Patrols a tiny radius near the broken bridge.

Engages only when approached.

Uses a slow 2.8s poke attack with a generous wind-up.

Designed to be defeated by any starting gear/skill level.

Why this Variant Exists

The whitebox emphasizes optional combat early on — the player can choose the bridge route (encountering this goblin)
or the creekbank route (avoiding combat).
This variant supports that design intention perfectly.