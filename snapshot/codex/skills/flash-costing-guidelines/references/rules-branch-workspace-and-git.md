## Branch, Workspace, And Git

- For new Flash Costing implementation work, create a fresh isolated worktree and neutral branch from the latest intended base before editing unless the user explicitly asks to work in the current checkout. Default ordinary feature/bug work to `origin/dev` unless the task, PR metadata, or user names another base.
- Use neutral branch names such as `feat/...`, `fix/...`, `chore/...`, `setup/...`, or `devops/...`. Do not include AI or tool branding.
- If the task is review-comment or merge-conflict work on an open PR, work directly on the existing PR head branch unless the user asks for a separate branch.
- If the main checkout is dirty, still use a fresh isolated worktree for new implementation work. Do not modify or revert unrelated local changes in the main checkout.
- After creating or switching into an isolated worktree, make sure local ignored development files are available when needed: copy `AGENTS.md` and its `.instruction-guides/` directory from the main checkout if present, verify it is ignored, and copy or point to the ignored local `db.sqlite3` only for local verification. Never stage, commit, push, or PR these local files.
- Do not commit, push, retarget, merge, or close PRs unless the user explicitly asks.
- Treat pushing as its own separate permission. Do not infer permission to run
  `git push`, create a PR, retarget a PR, merge a PR, close a PR, or delete a
  remote branch from implementation requests, ticket deliverables, branch
  creation, commit creation, or wording like "prepare a PR." Only perform the
  exact remote action after the user explicitly asks for that action in the
  current thread.
- Deleting a remote branch requires `git push origin --delete`, so it also
  requires explicit user confirmation naming the branch to delete.
- Never use forceful Git operations. Do not run `git push --force`, `git push --force-with-lease`, `git reset --hard`, `git clean -fd`, `git branch -D`, `git checkout --`, `git restore` to discard work, or any Git command with `--force`/`-f` that rewrites history, discards work, deletes refs, or overrides repository safety checks. If a user asks for one, refuse that operation and propose a non-destructive alternative.
- Do not add AI/tool branding in branch names, commits, PR bodies, comments, docs, or generated copy.
- Before final handoff, inspect `git diff --stat`, `git diff --name-only`, and the focused diff for scope drift.
- In self-review, scan the diff for newly duplicated calculations or helpers against existing services, views, template tags, selectors, commands, and static JS. Collapse duplication when the existing path can be reused without broad refactoring.
- Report what changed in product terms first, then technical details, validation, assumptions, and blockers.
