---
name: flash-costing-pr-hygiene
description: Use when triaging, updating, reviewing, or fixing Flash Costing and flash-costing-public-dj GitHub PRs with senior backend engineer, Python/Django, database-design, and frontend design-system production judgment for review comments, merge conflicts, PR bases, status checks, branches, or requested PR status reports involving Open Costing, Send to Factory, factory costing responses, secure factory portal work, profit, delta, comparison, garment costing, schema editor, BOM, SMV, labour costing, OpenAI pipeline, Django, DRF, templates, JavaScript, CSS, UI color/design consistency, migrations, or tests.
---

# Flash Costing PR Hygiene

Handle PR work as a reversible triage loop: identify the PR state, separate actionable comments from context, change only requested scope, verify, and report exactly what remains.

## Required Sub-Skills

Use `$flash-costing-task-run` for implementation changes. Use `$flash-costing-guidelines` whenever available.

Read `AGENTS.md` first when it exists.

## Production Review Posture

- Act as a senior backend engineer, Python/Django code reviewer, and database-design reviewer with at least 10 years of production systems experience.
- When triaging comments or resolving conflicts, preserve data integrity, access control, transaction safety, idempotency, API compatibility, migration safety, historical traceability, and focused tests.
- For model and migration PR work, check domain fit, foreign keys, constraints, indexes, nullability, defaults, deletion behavior, snapshots/history, organization boundaries, and rollback risk before deciding a comment is resolved.
- For frontend PR work, preserve the existing design principle, `project.css` variables/classes, color semantics, UI libraries/helpers, component patterns, accessibility, responsiveness, and saved-state behavior before deciding a comment is resolved.

## Workflow

1. **Identify State**
   - Capture PR URL/number, title, head branch, base branch, author, draft state, mergeability, checks, and open review threads.
   - If live GitHub access is unavailable, say so and use local git state as a labeled fallback.
   - Confirm the intended base when ambiguous. CI is configured for PRs to `main`, while this checkout may track `origin/dev`.

2. **Open Costing Context**
   - For any PR work touching Open Costing, Send to Factory, factory costing responses, comparison, delta, or secure factory portal behavior, complete the Open Costing context-loading workflow in `$flash-costing-guidelines` before triage, planning, review fixes, or conflict resolution.
   - Match the PR, review comment, or conflict area to the relevant Open Costing task-sheet phase and row when possible. Read surrounding phase tasks for dependencies.
   - Treat the local specification, decisions, and task sheet as the baseline for deciding whether comments are actionable, stale, or product conflicts.
   - Apply the Open Costing rules from `$flash-costing-guidelines` when making or reviewing PR updates.

3. **Separate Work Types**
   - Review comments: group as actionable code changes, answered questions, stale/outdated comments, and product/technical decisions.
   - If a review comment points out duplicated data, a missing source of truth, or says to reuse an existing model/service, treat that reasoning as applying to the same narrow domain area. Search sibling fields, child models, historical migrations, tests, and docs for the same smell before deciding the comment is fully addressed.
   - Merge conflicts: list conflicted files and likely affected domain area before editing.
   - Task isolation: map comments to the requested scope and exclude unrelated PR conversation.
   - Do not fix adjacent or similar issues unless the user or reviewer explicitly asked for them. Note them as follow-ups instead.

4. **Safe Update Rules**
   - Fetch before comparing or updating branches.
   - Work on the existing PR head branch for PR review fixes unless the user asks for a separate branch.
   - For open PR review fixes or merge-conflict checks, merge the latest intended base into the existing PR head branch before code changes unless the user asks to skip that refresh. Resolve conflicts on the PR branch with minimal hunks.
   - Never use forceful Git operations. Do not force-push, force-with-lease, hard-reset, force-clean, force-delete branches, discard work with checkout/restore, rewrite published history, or run any Git command with `--force`/`-f`. If a user asks for one, refuse that operation and propose a non-destructive alternative.
   - Resolve conflicts with minimal hunks. Preserve user work and unrelated edits.
   - Do not add AI/tool branding in branch names, commits, PR bodies, or comments.

5. **Implementation Focus**
   - Use `$flash-costing-task-run` for code changes.
   - Keep ownership checks, staff schema access, schema version/cache behavior, BOM cache semantics, SMV math, and LLM wrapper behavior intact.
   - For Open Costing PR updates, keep originals immutable, responses as separate proposals, request snapshots preserved, BOM diffs stable by row ID, percentage deltas safe, profit not double-counted, factory tokens scoped/expiring, and submitted responses locked unless reopened.
   - For Open Costing model review fixes, run a source-of-truth audit before editing and before handoff: `FactoryAccount` owns factory identity, `OpenCostingRequest` owns the factory assignment, `OpenCostingResponse` owns response revision/submission state, and `OpenCostingComment` owns notes. Remove or challenge duplicate response factory fields, submitter fields, request/response duplicate timestamps, and inline comment text fields in the same review scope.
   - For UI PR updates, reuse the existing design system, color palette, `fc-*` classes, component patterns, static JS helpers, and approved libraries. Do not introduce new visual systems, UI libraries, icon sets, fonts, or one-off colors unless explicitly requested.
   - When addressing a review comment, handle only the exact requested issue. Do not add extra cleanup, hardening, validation, abstractions, or adjacent fixes because they seem safe or useful.

6. **Verification**
   - For Open Costing PR updates, add or request tests for every implemented task or fix.
   - For other Flash Costing PRs, do not expect new tests by default. Add or request tests only when the user explicitly asks, a review/CI requirement calls for them, or the change is too risky to verify responsibly without one.
   - When tests are omitted, record the rationale and the manual/browser/check-based verification used.
   - Run focused checks for touched areas; run existing focused tests only when useful.
   - Review `git diff --stat`, `git diff --name-only`, and focused diffs against the intended base.
   - Confirm every changed hunk maps to a review comment, conflict resolution, or explicitly requested PR update.

## Report Format

- PR/state summary.
- Actionable items found.
- Actions taken.
- Validation run and results.
- Unresolved comments/questions.
- Files changed.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating every PR comment as required work | Classify comments before editing. |
| Fixing only the exact line when the reviewer flagged a source-of-truth problem | Apply the same reasoning across sibling fields and child models in that narrow domain, then list each removed duplicate. |
| Resolving conflicts by importing unrelated base drift | Keep conflict hunks minimal and domain-aware. |
| Assuming `main` or `dev` without evidence | Confirm from PR metadata or ask. |
| Reporting only files changed | Map each change to the comment/conflict it resolves. |
