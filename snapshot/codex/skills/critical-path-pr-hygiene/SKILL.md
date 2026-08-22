---
name: critical-path-pr-hygiene
description: Use when triaging, reviewing, updating, or fixing Critical Path GitHub PRs, including frontend design-system comments; isolating task comments; addressing review comments; checking merge conflicts; changing a PR base; pulling dev into a PR branch; or reporting PR status.
---

# Critical Path PR Hygiene

## Overview

Handle PR work as a reversible triage loop: identify the PR state, separate actionable comments from context, resolve only the requested scope, then report exactly what changed and what remains.

## Required sub-skill

Use `$critical-path-task-run` for implementation changes inside `critical-path-dj`. Use `$critical-path-guidelines` when available.

## Workflow

1. **Identify state**
   - Capture PR URL/number, head branch, base branch, author, mergeability, checks, and open review threads.
   - If live GitHub access fails, state that and use local git state only as a fallback.

2. **Separate work types**
   - Review comments: group by actionable code change, answered question, stale/irrelevant, and needs user/product decision.
   - Merge conflicts: list conflicted files and likely business area before editing.
   - Task isolation: map comments to the requested task; exclude unrelated conversation.

3. **Safe update rules**
   - Fetch before touching branches.
   - For open PR review fixes or conflict checks, automatically merge latest `origin/dev` into the existing PR head branch before code changes; do not ask first unless the user requested a different base/workflow.
   - Never force-push or use any Git force/discard/rewrite operation, even if requested; stop and explain the blocker instead.
   - Never retarget, close, merge, or delete branches unless explicitly asked.
   - Resolve conflicts with minimal hunks; do not import unrelated drift from `dev`.
   - Preserve user work and unrelated edits.
   - When triaging or fixing PR comments, preserve the existing frontend design system before marking comments resolved.
   - UI PR updates must reuse existing classes, colors, component patterns, helpers, and approved libraries.

4. **Verification**
   - Run focused tests or checks for touched areas.
   - Confirm the PR declares ASOS-only, TechnoSport-only, or shared scope and does not affect the non-target tenant when scoped.
   - Confirm brand and factory verification, including unchanged behavior for a deliberately non-target role.
   - Confirm every synchronized surface identified by the task still agrees on the persisted state.
   - Review diff against the intended base and confirm every hunk maps to a comment/conflict.

## Report format

- PR/state summary
- actionable items found
- actions taken
- validation run and results
- unresolved comments/questions
- files changed

## Common mistakes

| Mistake | Fix |
|---|---|
| Treating every comment as required work | Classify comments before editing. |
| Fixing unrelated code during conflict resolution | Resolve only conflict hunks and requested review issues. |
| Assuming live PR data when network fails | Say live data was unavailable and label local fallback clearly. |
