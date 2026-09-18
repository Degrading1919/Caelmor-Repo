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

If any normal direct-to-main publish command fails, report that exact failure and stop. Do not investigate unrelated repository configuration or diagnostics unless explicitly asked.

### Pull-request delivery (only when explicitly requested)

If the user explicitly requests a PR, that request overrides the normal direct-to-main delivery flow for that task.

- Start from the current `main` branch state before making task changes.
- Create a clean task branch containing only the requested work.
- Commit and push the task branch.
- Create the pull request against `main` using the available connected GitHub integration/API when one is available.
- The GitHub CLI (`gh`) is optional, not required. A missing `gh` executable is not a delivery failure when the connected GitHub integration can create the PR.
- Do not stop after pushing a branch when a PR was requested. The task is not complete until the PR exists.
- If neither the connected GitHub integration nor another authorized PR-creation mechanism is available, report that exact limitation after the branch is pushed.
- Do not open a PR from a stale branch with unrelated ancestry or unrelated commits. Recreate/rebase the task branch from current `main` first.
- Return the PR number and URL when complete.

## Design Identity Guardrail

For gameplay, progression, economy, content, UX, or world-facing changes, treat OSRS and RS3 as references for **feel and systemic depth**, not as implementation templates.

- Preserve Caelmor’s own Phase 1 canon, grounded mythic tone, solo-dev scope, and approved technical constraints.
- Seek RuneScape-like long-term mastery, interconnected systems, self-directed goals, readable unlocks, useful resources, and knowledge-based efficiency where appropriate.
- Do not copy RuneScape skill caps, XP curves, timings, formulas, item catalogs, markets, UI, quests, naming, or content volume merely for parity.
- When RuneScape precedent conflicts with Caelmor canon, Caelmor wins.

Use the Phase 1 documents and `00_ADMIN/Reference/Caelmor_Master_Assistant_Protocol.md` as the authority for this boundary.
