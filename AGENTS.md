# Codex Repository Instructions

## Delivery

GitHub `Degrading1919/Caelmor-Repo` is the sole repository authority. Use one designated local checkout at `C:/Users/CK/Documents/Caelmor-Repo` on this workstation. Treat detached recovery copies, build output and external research as non-authoritative. Preserve unique work before retiring any copy and obtain Creative Director authorization before deleting or moving it.

- Fetch from `origin`, confirm the active branch/PR and check for pending local work before switching. Start new feature work on a `codex/` branch from the applicable GitHub base. Continue work for an existing PR on its designated branch. For architecture, use `codex/architectural-generator` and PR #85 while that review is open.
- Commit only the scoped files and push the feature branch normally. Use a PR to review each feature before integration to `main`. Keep existing PRs for their assigned work. Do not merge a PR without Creative Director authorization. On a rejected push, preserve the commit, report the failure and stop unless the Director has authorized reconciliation. Never force-push or overwrite divergent work.
- Keep source, accepted evidence and decisions at the existing File Manifest destinations. Use the tracked tree to confirm exact paths. Record evidence provenance and record external datasets by source, revision or hash, and rights/access. Keep third-party assets and bulky temporary results out of Git unless their inclusion is explicitly approved.
- Before handoff, check the commit, pushed ref and working-tree status. Identify anything still held locally and record recoverable refs and artifact locations. Clean up temporary outputs only after confirming that unique work is preserved and obtaining authorization for cleanup of old project copies.

See [the repository consolidation record](00_ADMIN/Reference/Caelmor_Repository_Consolidation.md) for the checkout transition, approved placements and preservation inventory.

## Design Identity Guardrail

For gameplay, progression, economy, content, UX, or world-facing changes, treat OSRS and RS3 as references for **feel and systemic depth**, not as implementation templates.

- Preserve Caelmor’s own Phase 1 canon, grounded mythic tone, solo-dev scope, and approved technical constraints.
- Seek RuneScape-like long-term mastery, interconnected systems, self-directed goals, readable unlocks, useful resources, and knowledge-based efficiency where appropriate.
- Do not copy RuneScape skill caps, XP curves, timings, formulas, item catalogs, markets, UI, quests, naming, or content volume merely for parity.
- When RuneScape precedent conflicts with Caelmor canon, Caelmor wins.

Use the Phase 1 documents and `00_ADMIN/Reference/Caelmor_Master_Assistant_Protocol.md` as the authority for this boundary.

## Human-on-the-Loop Autonomous Delivery

The Creative Director sets objectives, approved canon/scope, and milestone acceptance—not every implementation step. Follow `00_ADMIN/Reference/Caelmor_Master_Assistant_Protocol.md` Section 5.6.

- For an authorized task, inspect actual repository sources, select the shortest dependency-ready path, execute, run available checks, independently review, fix defects, and continue to an inspectable outcome. Do not stop at a scaffold or new audit when the task requires working integration.
- Routine technical choices, exact skill/unlock tuning, reversible game-feel adjustments, bounded NPC/dialogue/quest details, and subagent allocation are delegated. Record consequential decisions and verification at milestones rather than asking for approval every time.
- Leads may direct authorized subagents and independent reviewers. Technical Director and Creative Production Director are orchestration responsibilities, not additional official roles. Only the Systems Engineer writes C#; only the Schema & Content Engineer authors schemas and production JSON.
- Preserve Phase 1 canon, approved contracts, and existing file governance. Escalate only foundational/scope changes, real same-tier contradictions, breaking schema/network/save changes, or genuinely inaccessible/irreversible blockers. Do not silently promote narrative proposals into locked canon.
- Prefer a compiling, executed, playable Lowmark slice over more scaffolding, speculative optimizations, or redundant governance reviews.
- Distinguish source presence, successful compile, tests executed, Unity runtime validation, and real player experience; claim only what evidence supports.

This standing authorization covers **routine execution within the user's assigned mission**. Follow the feature-branch, PR review and preservation workflow above.
