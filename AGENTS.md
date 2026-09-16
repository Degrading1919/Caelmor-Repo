# Codex Repository Instructions

## PR Delivery

When asked to push or create a PR:

- Do not inspect Git configuration, remotes, line endings, usernames, repository metadata, or individual changed files unless a publish command actually fails.
- Assume the repository is already configured correctly.
- Do not perform a Git/GitHub audit before publishing.

If currently on `main`, create a task branch:

`git switch -c codex/<short-task-name>`

Then publish using only:

`git add -A`
`git commit -m "<short task summary>"`
`git push -u origin HEAD`
`gh pr create --base main --fill`

If `git commit` reports nothing to commit, continue with push/PR creation.

If any publish command fails, report that exact failure and stop. Do not investigate alternate GitHub integrations, APIs, authentication methods, repository configuration, or unrelated diagnostics unless explicitly asked.

Do not merge the PR unless the user explicitly requests it.
