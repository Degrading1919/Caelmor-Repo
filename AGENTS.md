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
