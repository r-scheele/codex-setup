---
name: seamstream-pr-hygiene
description: "Use when triaging, reviewing, updating, or fixing SeamstreamAI GitHub PRs; isolating task comments; addressing review comments; preserving frontend design-system consistency in PR updates; checking merge conflicts; changing a PR base; pulling main into a PR branch; or reporting PR status for seamstream_ai."
---

# Seamstream PR Hygiene

Handle Seamstream PR work as a reversible triage loop: identify the PR state, separate actionable comments from context, resolve only the requested scope, then report exactly what changed and what remains.

## Required Sub-Skills

Use `$seamstream-task-run` for implementation changes inside `__HOME__/Desktop/code/seamstream_ai`.

Use `$seamstream-guidelines` whenever available.

## Workflow

1. **Identify State**
   - Capture PR URL/number, head branch, base branch, author, mergeability, checks, and open review threads.
   - Default expected base is `main` unless the PR says otherwise.
   - If live GitHub access fails, state that and use local git state only as a fallback.
   - Check local branch and dirty state before edits.

2. **Separate Work Types**
   - Review comments: group by actionable code change, answered question, stale/irrelevant, and needs user/product decision.
   - Merge conflicts: list conflicted files and likely product area before editing.
   - Task isolation: map comments to the requested task; exclude unrelated conversation.
   - Verification gaps: identify which comments need manual UI/API proof, migrations checks, focused Django tests, or screenshots.

3. **Safe Update Rules**
   - Fetch before touching branches.
   - For open PR review fixes or conflict checks, work on the existing PR head branch unless the user explicitly asks for a different workflow.
   - If updating an open PR branch, merge latest `origin/main` into that branch before code changes unless the user requested a different base/workflow.
   - Do not retarget, close, merge, delete branches, or resolve review threads unless explicitly asked.
   - Never force-push or run forceful/destructive git operations. Do not use `git push --force`, `--force-with-lease`, `git branch -D`, `git tag -f`, `git reset --hard`, `git clean -fd`, `git checkout -f`, or any git flag/command whose purpose is to force, overwrite, or discard work; if asked, refuse and offer a non-force alternative.
   - Resolve conflicts with minimal hunks; do not import unrelated drift from `main`.
   - Preserve user work and unrelated edits.
   - Use neutral branch names if a new branch is explicitly requested; never use AI/tool-branded prefixes.

4. **Implementation**
   - Use `$seamstream-task-run` and `$seamstream-guidelines`.
   - Keep fixes mapped to review comments or conflicts.
   - When triaging or fixing PR comments, preserve the existing frontend design system before marking comments resolved.
   - UI PR updates must reuse existing classes, colors, component patterns, helpers, saved-state behavior, accessibility patterns, and approved libraries.
   - For review comments touching tech-pack import, operation books/versions, factory setup, subscriptions/credits, LLM/cache, flash costing, storage, or database routing, inspect the full local flow before editing.

5. **Verification**
   - Run focused tests or checks for touched areas.
   - Run `python manage.py makemigrations --check --dry-run` when models may be affected.
   - Use manual UI/API verification and screenshots for product-visible changes when local setup permits.
   - For UI updates, verify no unapproved UI library, CSS framework, palette, font, icon set, animation library, bundler, or one-off visual language was introduced.
   - Review diff against the intended base and confirm every hunk maps to a comment/conflict.

## Report Format

- PR/state summary
- actionable items found
- actions taken
- validation run and results
- unresolved comments/questions
- files changed
- any branch, merge, or GitHub tooling blockers

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating every PR comment as required work | Classify comments before editing. |
| Updating against `dev` by habit | Use the PR base; Seamstream's inspected default branch is `main`. |
| Fixing unrelated code during conflict resolution | Resolve only conflict hunks and requested review issues. |
| Assuming live PR data when network or auth fails | Say live data was unavailable and label local fallback clearly. |
| Resolving review threads immediately after pushing | Leave them for reviewer verification unless the user explicitly asks. |
