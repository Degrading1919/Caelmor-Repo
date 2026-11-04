# Codex Repository Instructions

## Delivery

GitHub `Degrading1919/Caelmor-Repo` is the sole source of truth. `C:/Users/CK/Documents/Caelmor-Repo` is the only designated local checkout. **The Creative Director directs all ongoing project work on `main`.** No new feature branches, PRs, clones, worktrees or parallel working directories without explicit Creative Director authorization.

- Before work, fetch `origin`, confirm the designated checkout is on `main`, inspect for pending local changes, and synchronize safely with `origin/main`. Work in the existing checkout on `main` for all authorized project tasks, including architectural development. Previous feature branches and PRs are historical records, not active implementation targets.
- Commit only scoped, verified changes directly to `main` and push normally after fetching and integrating any remote changes safely. Preserve milestone reviews and Creative Director approval gates without requiring PRs. On a rejected push, preserve the commit, report the failure and stop unless the Director has authorized reconciliation. Never force-push or overwrite divergent work.
- Commit and push every project-owned deliverable, including source, tools, research, evidence and decisions, at an existing File Manifest destination. Use the tracked tree to confirm exact paths. Record external references by source, revision or hash, and rights. Third-party assets require distribution rights before they can be published.
- Keep temporary builds, research inputs and evidence inside the designated checkout. Before handoff, incorporate justified project-owned material, remove disposable outputs and verify the pushed commit and clean working tree. Persistent external research, evidence, build and staging directories are prohibited. Verify recoverability from GitHub before removing unique work, and obtain Creative Director authorization before retiring any old project copy.

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

This standing authorization covers **routine execution within the user's assigned mission**. Follow the direct-`main`, single-checkout and preservation workflow above.
