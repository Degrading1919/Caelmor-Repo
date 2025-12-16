🧊 Stage 8.0 — Systems Snapshot & Implementation Plan

Caelmor Non-Combat Economy

1. Snapshot Purpose
This document formally freezes the non-combat economy systems at the end of Stage 7 and defines the approved execution path going forward.
From this point onward:
Changes are implementation fixes, not design changes
Schemas are immutable
Runtime behavior is canon
Balance and content scale are explicitly deferred
This snapshot exists to prevent:
Design drift
Accidental re-architecture
Scope creep during coding

2. Canon Freeze Statement
The following stages are complete, approved, and locked:
Schemas (Immutable)
ResourceCategory.schema.json
ResourceNode.schema.json
ResourceItem.schema.json
Recipe.schema.json
CraftingStation.schema.json
GatheringSkillKey.schema.json
Runtime Design References (Authoritative)
Stage7_1_ResourceNodeRuntime.md
Stage7_2_GatheringResolution.md
Stage7_3_InventoryAndResourceGrant.md
Stage7_4_CraftingExecutionSystem.md
Stage7_5_Persistence&SaveIntegration.md
These documents define what the engine must do.
They are not suggestions.

3. Proven System Guarantees
The non-combat economy now guarantees:
Server-authoritative behavior
Deterministic tick-based logic (10 Hz)
RuneScape-style node depletion & respawn
Atomic inventory mutation
Atomic crafting execution
Deterministic persistence & restore
No event replay
No duplicate grants
No partial state commits
Any future system must respect these guarantees.

4. Explicit Non-Goals (Locked Out)
The following are intentionally excluded and must not be added during implementation:
Balance tuning
Yield quantity decisions
XP curves
UI or UX flow
Animation timing
Economy inflation controls
Region-specific tuning
Market systems
These belong to future stages and are not allowed to leak backward.

5. Approved Implementation Order (Do Not Reorder)
The non-combat economy must be implemented in the following order:
Resource Node Runtime
Node instances
Tick-based respawn
Availability state
Gathering Resolution
Legality checks
Deterministic outcome resolution
Risk surfacing
Inventory Model & Resource Grant
Minimal keyed inventory
Server-authoritative mutation
Grant events
Crafting Execution
Recipe validation
Atomic input consumption
Output production
Persistence Integration
PlayerSave (inventory)
WorldSave (node state)
Tick-safe restore
Skipping or reordering these steps is not allowed.

6. Required Engine Scaffolding (Awareness Only)
Before or during implementation, the following engine-level systems must exist or be stubbed:
Server tick manager (10 Hz)
Event dispatch system (server-side)
Player session identity
World/zone loading hooks
Save/load invocation points
These are infrastructure, not gameplay systems.

7. Risk Register (Acknowledged, Accepted)
The following risks are known and accepted:
Sparse sample content may feel “thin” during early tests
Placeholder mappings will be replaced later
No balance validation occurs during implementation
No client prediction exists initially
None of these justify redesign.

8. Re-entry Rule
When returning to this system after working on other domains:
Do not ask “should this work differently?”
Ask only “did we implement this correctly?”

If a problem arises:
First assume implementation error
Only escalate to design review if implementation cannot satisfy the snapshot

9. Exit Condition
Stage 8.0 is considered successful when:
This snapshot is saved
All Stage 7 documents are treated as locked
Implementation begins against these references without modification

One-Line Anchor (Carry This Forward)
“The economy is architecturally complete. From here on, we build it — we do not rethink it.”