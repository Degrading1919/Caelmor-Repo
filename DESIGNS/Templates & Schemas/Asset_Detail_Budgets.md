# Caelmor — Asset Detail Budgets 

Hard, enforceable asset-detail budgets optimized for:
- Host-authoritative networking
- Fixed **10 Hz server tick**
- Low tolerance for jitter/desync
- Target scale: up to ~1000 players/world (typical visibility: 60–100 in hubs, 10–20 elsewhere)
- Unity runtime constraints
- Solo-dev production realities

This document defines **asset budgets + replication exclusions**. No gameplay logic.

---

## A. Global Non-Negotiables (All Assets)

### A1) Geometry & Runtime Features
- No runtime mesh deformation (cloth/jiggle/blendshape-driven motion)
- No per-vertex animation
- No procedural mesh generation at runtime
- No physics-driven secondary motion that affects replicated transforms
- Skinned meshes only when needed; static meshes preferred

### A2) Materials & Shaders
- Max **1 material per mesh** (2 only if absolutely unavoidable)
- URP Lit (or equivalent standard pipeline) only
- No tessellation, no parallax occlusion, no real-time reflections
- Transparency only when required (foliage/VFX-style exceptions only)

### A3) Animation
- Keyframed animation only (authored)
- No runtime IK by default (see Optional section for strict client-only exception)
- No authoritative root-motion replication
- No replication of animation time, blend weights, or bones

### A4) Networking & Replication (Hard Rules)
- Only replicate transforms for authoritative entities
- Never replicate bones
- Never replicate animation state per-frame
- Animation state changes must be event-driven (high-level state), not streamed

#### Replication Exclusions (Never Replicate)
- Bone transforms (any bones, any time)
- Animation playback time
- Blend tree weights / layer weights
- IK solver results
- Cosmetic attachment motion
- Cloth/secondary motion states
- Facial animation parameters

#### Replicate Only When Required
- World transform (position/rotation)
- Facing direction (if not derivable)
- High-level state enums (movement/combat/interaction)
- Binary/enum interaction state for props (open/closed, active/inactive)

---

## B. “Assembled Character” Budgets (Highest Leverage)

These caps apply to the **fully assembled character as rendered on screen** (base body + all equipped parts combined).

### B0) Assembled Triangle Budget Clarification (NEW)
- The LOD0 triangle budgets listed below are for the **fully assembled character on screen**, **not per equipment piece**.
- Gear modularity must not allow the assembled character to exceed the class LOD budgets.

### B1) Total Unique Materials (Assembled)
- **Player character:** total unique materials **≤ 2** (across all equipped/assembled renderers)
- **Humanoid NPC:** total unique materials **≤ 1**
- **Creatures:** total unique materials **≤ 1**
  - **Boss-tier exception:** ≤ 2 materials (rare, silhouette-critical only; see constraint below)

Notes:
- “Unique” means different material instances/shader variants at runtime.
- This is a major performance + visual cleanliness win (network impact: none).

### B2) Skinned Mesh Renderer Count (Assembled)
- **Player character:** skinned mesh renderers **≤ 2** (prefer **1**)
  - Example: Body (1) + Equipped shell/outerwear (1)
- **Humanoid NPC:** skinned mesh renderers **= 1** whenever possible
- **Creatures:** skinned mesh renderers **= 1**
  - **Boss-tier exception constraint (NEW):** Boss-tier creatures may use ≤ 2 materials **but must still use 1 skinned mesh renderer**

Implication:
- Gear authoring should support bake/merge workflows or shared atlas shells.
- This prevents draw-call and skinning CPU explosion in hubs.

---

## C. Asset Class Budgets

---

## 1) Player Characters (Highest Fidelity Allowed)

### Geometry (per character, assembled on screen)
| Metric | Budget |
|---|---|
| LOD0 | **8,000–10,000 tris** |
| LOD1 | 4,000 tris |
| LOD2 | 1,500 tris |
| LOD3 | billboard or culled |

**LOD3 clarification (NEW):**
- Player LOD3 may be **culled in hubs only** when the camera distance makes the character **unreadable anyway** (silhouette/details no longer meaningful).
- Avoid billboarded players if it looks visually wrong for multiplayer readability; culling is acceptable at extreme distances.

### Rig & Bones (REVISED — choose one policy and enforce it project-wide)

**Policy A (recommended for Alpha scale):**
- **Total bones ≤ 50**
- **No fingers by default**
- Hands may be single rigid/low-bone deform (thumb optional only if within 50)
- No facial bones

**Policy B (allowed, but must stay disciplined):**
- **Total bones ≤ 55**
- Reserve **≤ 6 bones** strictly for silhouette-critical attachments (keyframed only)
- Still no facial bones, no physics/secondary motion

### Animation (baseline)
- Layers: **≤ 2** (base locomotion + upper-body/state)
- Blend trees: **≤ 2 total**
- Additive layers: **0 by default** (see Optional section for 1 allowed additive)
- Animation events allowed (footsteps, weapon ready), but must not imply authority

### Networking
**Replicated**
- Transform
- Facing direction (if needed)
- High-level state enum (idle, moving, interacting, attacking)

**Not replicated**
- Bone transforms
- Animation playback time
- Layer weights / blend weights
- IK results
- Cosmetic-only motion

---

## 2) Humanoid NPCs (Guards, Villagers, Bandits)

### Geometry (per NPC, assembled on screen)
| Metric | Budget |
|---|---|
| LOD0 | **5,000–6,000 tris** |
| LOD1 | 2,500 tris |
| LOD2 | 1,000 tris |
| LOD3 | culled |

### Rig & Bones
- **Total bones ≤ 45**
- No fingers
- No facial bones

### Animation
- States: idle/walk/work/talk/combat
- Heavy reuse required; minimal layering

### Networking
**Replicated**
- Transform
- High-level AI/state enum

**Not replicated**
- Animation detail
- Head turns
- Gesture timing
- Any per-bone state

---

## 3) Creatures (Animals, Beasts)

### Geometry (per creature, assembled on screen)
| Metric | Budget |
|---|---|
| LOD0 | **3,000–5,000 tris** |
| LOD1 | 1,500 tris |
| LOD2 | 600 tris |
| LOD3 | culled |

### Materials (assembled)
- Default: **≤ 1 material**
- **Boss-tier exception:** **≤ 2 materials** (rare, silhouette-critical only)
  - **Must still use 1 skinned mesh renderer** (no exception)

### Rig & Bones
- **Total bones ≤ 35**
- Spine: 3–4
- Limbs: ~4 per limb
- Tail/wings: **≤ 5 bones total**
- No facial bones

### Animation
- States: idle/move/flee/attack
- Blend trees: **≤ 1**
- Additives: none by default

### Networking
**Replicated**
- Transform
- High-level AI/state enum

**Not replicated**
- Limb animation
- Tail/wings secondary motion
- Any per-bone state

---

## 4) Interactive Props (Doors, Levers, Crafting Stations)

### Geometry
- **500–1,500 tris**
- LOD optional (1 step)

### Animation
- No bones
- Single transform animation only (rotate/translate)
- No skinned meshes

### Networking
**Replicated**
- State enum only (open/closed, active/inactive)

**Not replicated**
- Animation progress
- Cosmetic motion

---

## 5) Environment Assets (Buildings, Terrain Props)

### Geometry
| Category | Budget |
|---|---|
| Small props | 100–300 tris |
| Medium props | 500–1,000 tris |
| Large props | 2,000–4,000 tris |
| Buildings | modular pieces **≤ 2,000 tris each** |

### Rules
- No skinned meshes
- No runtime animation
- No replication
- Static batching preferred

---

## D. LOD + Visibility Rules (Critical)

### D1) LOD Switching
- Distance-based only (deterministic)
- No screen-space or performance heuristics
- No crossfade required (hard pop acceptable)

### D2) Culling
- Server ignores LOD/culling (client-only concern)
- Culled assets must not participate in tick or replication logic

---

## E. Optional “Feel Wins” (Allowed only if strictly client-only)

These are permitted only if they remain purely visual and globally disable-able.

### E1) Client-only Foot IK (OPTIONAL)
Allowed only if:
- Never affects replicated transform
- Never affects hit detection, collision, timing, or gameplay outcomes
- Can be disabled globally (quality toggle)
- Safe to disable in hubs without breaking locomotion animation

### E2) One Additive Layer (OPTIONAL)
Allowed:
- **Exactly 1 additive layer** for subtle posture cues (breathing/weight/aim stance)
- Driven by the same high-level replicated state (event/state-driven), not per-frame network data
- Must not introduce new replicated states

---

## F. Keep These Prohibitions (Do NOT loosen)

- Do not replicate bones/anim time/blend weights
- Do not increase triangle budgets chasing “modern MMO fidelity”
- Do not add physics-based secondary motion that can leak into authority

---

## Practical Summary

Highest leverage for stability in busy areas:
1) Assembled materials cap
2) Skinned mesh renderer cap
3) Bone policy tightened (Policy A recommended for Alpha)

Optional polish is safe only if it stays client-visual and globally disable-able.

---

## Bottom Line

> **If it wiggles, it must not replicate.**  
> **If it animates, it must not tick.**  
> **If it ticks, it must be boringly deterministic.**
