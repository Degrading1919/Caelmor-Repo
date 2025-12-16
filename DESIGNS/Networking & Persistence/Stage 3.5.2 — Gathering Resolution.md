# Stage 7.2 — Gathering Resolution System  
**Design Reference Document**

---

## 1. Overview

The **Gathering Resolution System** is a server-authoritative, deterministic rules layer that resolves a player’s attempt to gather from a resource node.

This system operates:
- **After** node existence and availability validation (Stage 7.1)
- **Before** inventory, rewards, XP, or effects

Its sole purpose is to answer the question:

> “Given a valid interaction with a node, what is the authoritative outcome of this gather attempt?”

All schemas are **canonical and immutable**.  
This system consumes schema data and runtime facts but does not define or modify schemas.

---

## 2. Core Responsibilities

The Gathering Resolution System is responsible for:

### Validation
- Confirming the player possesses at least one allowed gathering skill for the node
- Re-validating node availability as a safety boundary
- Applying **logical** (non-numeric) requirements such as tool class, if present

### Resolution
- Resolving each attempt to a small, explicit outcome:
  - `success`
  - `failure_soft`
  - `failure_hard`
- Producing a single authoritative result object for downstream systems

### Risk Surfacing
- Detecting whether a node-defined risk condition was triggered
- Reporting *which* risk was triggered (descriptive only)
- Not applying damage, status effects, or mechanics

---

## 3. Resolution State Model

### Outcomes

Each gather attempt resolves to exactly one outcome:

- **success**
  - The attempt succeeds
  - Resource grant and node depletion are allowed

- **failure_soft**
  - The attempt fails without catastrophe
  - No resource grant or depletion
  - Used for poor technique or suboptimal conditions

- **failure_hard**
  - The attempt is blocked or unsafe
  - No resource grant or depletion
  - Used for missing requirements or triggered hazards

### Flags

Rather than encoding logic downstream, the result explicitly includes:

- `resource_grant_allowed`
- `node_depletion_allowed`
- `risk_triggered`

Downstream systems consume these flags without re-evaluating logic.

---

## 4. Tool Logic (Policy-Level, Optional)

Tool handling is **policy-driven and optional**.

Key design principles:
- No assumption that a finalized tool schema exists
- No hard dependency on a tool system being present
- Graceful behavior when:
  - No tool system exists
  - No tool is equipped
  - Tool requirements are undefined

### Conceptual Policy Categories
- **Not applicable** — tools irrelevant for this node
- **Recommended** — lack of tool may cause soft failure
- **Required** — lack of tool causes hard failure

Tool policies are:
- Evaluated logically, not numerically
- External to schemas
- Swappable without modifying this system

---

## 5. Risk Handling (Provisional Policy)

Nodes may define one or more **risk flags** via schema.

At this stage:
- Risk handling is **descriptive only**
- Risk triggers are deterministic
- No probability, damage, or effects are applied

### Current Provisional Mapping
- If a risk is triggered → `failure_hard`

> **Important:**  
> This coupling of risk → hard failure is provisional.  
> Future extensions may allow:
> - Risk + success
> - Risk + soft failure
> - Conditional or delayed risk effects

The system must remain flexible to support these evolutions.

---

## 6. Conceptual C# Structures (Illustrative Only)

> **Illustrative only** — these examples are not production code.

### Gathering Outcome

enum GatheringOutcome
{
    Success,
    FailureSoft,
    FailureHard
}

### Resolution Result Payload
struct GatheringResolutionResult
{
    GatheringOutcome Outcome;

    int NodeInstanceId;
    string GatheringSkillKey;

    bool ResourceGrantAllowed;
    bool NodeDepletionAllowed;
    bool RiskTriggered;

    // Descriptive only
    string TriggeredRiskKey;
}

### Attempt Context (Facts Only)
struct GatheringAttemptContext
{
    int ServerTick;
    int PlayerId;

    int NodeInstanceId;
    string NodeTypeKey;

    bool NodeIsAvailable;
    IReadOnlyList<string> AllowedGatheringSkills;
    IReadOnlyList<string> NodeRiskFlags;

    string PlayerToolClassKey; // optional / nullable
}

## 7. Resolution Flow (Deterministic)
- Step-by-Step Logic
  - Validate node availability
  - If unavailable → hard failure
  - Resolve gathering skill
  - Player must possess at least one allowed skill
  - Skill selection must be deterministic
  - Evaluate tool policy (if any)
  - Required tool missing → hard failure
  - Recommended tool missing → soft failure
  - Evaluate risk flags

- If risk deterministically triggers:
  - Mark risk_triggered = true
  - Apply provisional hard failure
  - Resolve success
  - Allow resource grant
  - Allow node depletion
  - No randomness, tuning, or time-based logic is used.

## 8. Performance & Determinism Notes
- The system is stateless

- All decisions are derived from:
  - Schema data
  - Runtime facts
  - Explicit policies
  - No per-tick overhead
  - No allocations required during resolution
  - Safe to run per interaction at scale

## 9. Extension Points (Not Implemented)
- Inventory & Resource Items
  - Replace placeholder grant permission with:
  - ResourceItem keys

- Quantities
  - Inventory ownership remains external

- Skill Progression
  - Introduce skill levels and difficulty comparisons
  - Stage 7.2 remains the resolution authority

- Risk Evolution
  - Decouple risk from outcome severity
  - Allow mixed outcomes (success + risk)

- Persistence & Auditing
  - Optional logging of resolution results
  - Useful for debugging and anti-cheat

- Networking
  - Resolution result serialized to client
  - Client uses result for feedback only
  - No prediction or authority transfer

## 10. Non-Goals
- This system explicitly does not handle:
  - XP gain
  - Yield calculation
  - Inventory modification
  - Combat effects
  - Damage or status application
  - Animation timing
  - Probability tuning
  - Client-side prediction
  - Tool schema definition