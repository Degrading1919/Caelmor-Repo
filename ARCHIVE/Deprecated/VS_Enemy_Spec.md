# VS Enemy Specification — Field Goblin (Family) & Bridge Sentry (Variant)
### Role: Balance & Telemetry Analyst  
### Vertical Slice Combat Tuning

---

# 1. Overview
The Field Goblin family is the baseline Tier-1 hostile in Lowmark.  
Its VS variant — the **Bridge Sentry** — introduces the game’s first real melee encounter.

This document defines:
- Attack cadence  
- Telegraph timing  
- Hitbox dimensions  
- Early-game tuning (TTK, DPS, XP yield expectations)  
- Tick-based timing alignment for consistency

---

# 2. Combat Timing (Tick-Aligned)
Caelmor combat resolves at **10 Hz** (100 ms ticks), so all timings snap to tick multiples.

| Component | Value | Tick Count |
|----------|--------|------------|
| Attack cadence | **2.8s** | 28 ticks |
| Telegraph duration | **0.7s** | 7 ticks |
| Active hit window | **0.25s** | 3 ticks |
| Recovery | **0.4s** | 4 ticks |
| Post-hit lockout (no chain) | **0.5s** | 5 ticks |

This produces the intended slow, readable rhythm defined in Lowmark VS whitebox.

---

# 3. Telegraph Specification
The telegraph for *simple_poke* must be unmistakable from the top-down camera.

### 3.1 Sequence
1. **Wind-Up (0.7s / 7 ticks)**  
   - Torso leans forward  
   - Shoulder drops  
   - Weapon arm draws back in a clear silhouette  
   - Movement slows by 40% to emphasize commitment

2. **Strike (0.25s / 3 ticks)**  
   - Quick forward jab  
   - Small lunge (0.3m)  
   - Server resolves hit on the *second* tick inside active window to reduce edge-cases

3. **Recovery (0.4s / 4 ticks)**  
   - Returns to idle stance  
   - Movement disabled for cleanup  

### Readability Goals
- The player must be able to **consistently parry/step back** on seeing the shoulder-drop.
- Telegraph silhouette must be visible even with 45° camera offsets.

---

# 4. Hitbox Definition
Hitboxes must be sized for fairness, not realism.

### 4.1 Attack Hitbox
| Shape | Capsule |
|------|---------|
| Length | 1.5m forward |
| Radius | 0.4m |
| Height | 1.0m |

This ensures:
- Hit lands only if player is **in front and reasonably close**  
- Side-stepping even slightly will evade the hit  
- Goblin cannot “curve” attacks to track players  

### 4.2 Body Hitbox (for player attacks)
- Capsule: radius 0.45m, height 1.3m  
- Slightly generous so new players land hits reliably

---

# 5. Damage & TTK Tuning
Using family stats (base) + variant modifiers:

| Stat | Base | Variant | Final |
|------|-------|---------|--------|
| Health | 20 | +4 | **24 HP** |
| Power | 5 | +1 | **6 Power** |
| Armor | 0 | 0 | **0** |

### 5.1 Goblin DPS (Expected)
Goblin deals 6 damage every 2.8s → **~2.1 DPS** (rounded).

### 5.2 Player TTK Target
Early-game player deals ~3–4 DPS with training sword.

Expected TTK vs 24 HP:
- **6–9 seconds**, matching whitebox pacing.

### 5.3 Player Survivability
A new player starts around 40 HP.  
Goblin kills player in ~19 seconds of uninterrupted hits.

This is intentionally lenient:
- Encourages early learning  
- Prevents unfair wipes  
- Supports optional retreat

---

# 6. Movement & Spacing Tuning
| Attribute | Value |
|-----------|--------|
| Base move speed | 1.1 (family) |
| Chase speed bonus | +0.15 for 0.6s after player enters range |
| Leash radius | 12–15m |
| Re-engage delay | 1s after losing LOS |

Spacing rules prevent accidental multi-pulls in the VS zone.

---

# 7. AI Behavior Timing Notes
- Goblin pauses 0.3s after acquiring target (fairness buffer).  
- Will not attack for first 1.0s after aggro — gives player “opening moment.”  
- Will not chain attacks if player backs up beyond 2.0m; resumes normal cadence.  

---

# 8. Telemetry Hooks (Minimal VS Set)
The following events must be logged client-side and host-side for VS balancing:

### 8.1 Enemy Events
- `enemy_aggro`  
- `enemy_attack_started`  
- `enemy_attack_hit`  
- `enemy_attack_missed`  
- `enemy_damage_taken`  
- `enemy_killed`

### 8.2 Player Performance Data
- `player_time_to_kill_enemy`  
- `player_damage_taken`  
- `player_attack_accuracy`  
- `distance_player_to_enemy_on_hit`

### 8.3 Encounter Metrics
- Avg TTK  
- Avg DPS taken  
- Avg distance maintained during combat  
- Failure rate (death rate per encounter type)

These will be essential for 2.4 Combat v1 tuning and 5.2 global balance pass.

---

# 9. Summary (Tuning Targets for VS)
- Clear, readable telegraph at 0.7s  
- Simple attack every 2.8s  
- Low DPS (2.1) to ensure fairness  
- TTK 6–9s for early weapons  
- Generous hitboxes to avoid frustration  
- Telemetry-ready structure for iteration

This spec keeps Field Goblins completely aligned with Pillar B (Grounded Combat) and the VS whitebox encounter design.

---
