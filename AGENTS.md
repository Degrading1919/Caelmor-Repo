# Codex Repository Instructions

## Delivery

For normal Caelmor tasks, work directly on `main`.

- Do not create task branches.
- Do not create pull requests unless the user explicitly asks for one.
- Do not inspect Git configuration, remotes, line endings, usernames, repository metadata, or individual changed files unless a publish command actually fails.
- Assume the repository is already configured correctly.
- Do not perform a Git/GitHub audit before publishing.

When the task is complete, publish using only:

`git add -A`
`git commit -m "<short task summary>"`
`git push origin main`

If `git commit` reports nothing to commit, continue with the push.

If any publish command fails, report that exact failure and stop. Do not investigate alternate GitHub integrations, APIs, authentication methods, repository configuration, or unrelated diagnostics unless explicitly asked.

If the user explicitly requests a PR, follow that request for that task only.

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

This standing authorization covers **routine execution within the user's assigned mission**, not unrelated repository edits or unrequested external actions. Preserve the Delivery rules above: direct to `main` unless a PR was explicitly requested, exact publish sequence, and STOP on publish failure.
