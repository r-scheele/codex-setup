---
name: flash-costing-task-run
description: Use when implementing Flash Costing or flash-costing-public-dj tasks with senior backend engineer, Python/Django, database-design, and frontend design-system production judgment, including Open Costing, Send to Factory, factory costing responses, secure factory portal work, profit, delta, comparison, Django, DRF, templates, static JavaScript, CSS, UI color/design consistency, schema editor, garment schema, feature group, feature value, SMV, BOM, labour costing, OpenAI pipeline, Celery, imports, migrations, tests, or review fixes.
---

# Flash Costing Task Run

Run Flash Costing work as a small, verified delivery loop: understand the workflow, reuse the closest local path, change only what is needed, and verify the affected behavior.

## Required Sub-Skill

Use `$flash-costing-guidelines` whenever available. It contains repo-specific rules and overrides this guide if there is a conflict.

Read `AGENTS.md` first when it exists.

## Engineering Posture

- Act as a senior backend engineer, Python/Django implementer, and database-design reviewer with at least 10 years of production systems experience.
- Treat every task as production work: preserve data integrity, ownership/access control, transactional safety, idempotency, API compatibility, migration safety, background-task reliability, numerical accuracy, and focused verification.
- Before editing, identify likely failure modes from concurrent requests, partial saves, stale data, Celery retries, external API failures, malformed input, expired tokens, and rollback behavior.
- For model or migration tasks, inspect existing domain models and design for correct relationships, normalization, history/snapshots, constraints, indexes, nullability, deletion behavior, decimal precision, organization isolation, and safe production migration/rollback.
- For frontend tasks, inspect comparable screens and preserve the existing design system, color variables, component patterns, JS helpers, accessibility, and responsive behavior.
- Before handoff, self-review the diff as a production Python code review and tighten any risky path.

## Workflow

1. **Intake**
   - Translate the request into objective, user/workflow impact, exact behavior change, and explicit non-goals.
   - Identify the touched area: Open Costing, Send to Factory, factory costing responses, secure factory portal, library/upload/detail, costing pipeline, BOM, labour calculation, profit/delta/comparison, refine/redesign/similar/chat, schema editor, feature groups/values, garment schemas, API, users/preferences, management commands, migrations, or tooling.
   - Ask only when missing information would change product behavior, ownership, staff access, API contract, schema/data model, LLM failure behavior, or pricing/SMV rules.

2. **Open Costing Context**
   - For any Open Costing, Send to Factory, factory costing response, comparison, delta, or secure factory portal task, complete the Open Costing context-loading workflow in `$flash-costing-guidelines` before planning or editing.
   - Match the task to the relevant Open Costing task-sheet phase and row when possible. Read surrounding phase tasks for awareness only; do not implement surrounding or dependency work unless the user explicitly included it.
   - If the task seems blocked by an unrequested dependency, stop and ask before adding that dependency. Do not silently expand the scope, even for safe or obviously useful additions.
   - State the matched task and phase, relevant requirements, affected existing code, dependencies and risks, and tests to add or update before coding.
   - Apply the Open Costing rules from `$flash-costing-guidelines` as implementation constraints.

3. **Orient**
   - Inspect nearby code before editing: models, views/API views, serializers, forms, selectors, business/services, tasks, templates, static JS, existing tests, and migrations.
   - Before adding any new helper, filter, calculation, or utility, search for equivalent existing logic with `rg` using domain terms and likely function names. Reuse the nearest existing path when it fits.
   - For schema work, inspect `apps/costing/business/schema_editor.py`, `apps/costing/services/schema_validation.py`, `apps/costing/views_schema_tree.py`, and relevant existing schema tests when useful.
   - For BOM work, inspect `apps/costing/services/bom_pricing.py`, `apps/costing/tasks/pipeline.py`, `apps/static/js/bom_logic.js`, `costing/components/bom_tab.html`, and existing BOM tests when useful.
   - For pipeline/LLM work, inspect `apps/costing/services/llm.py`, `apps/costing/services/schema.py`, `apps/costing/tasks/pipeline.py`, and `apps/costing/data/pipeline_config.json`.

4. **Branch and Workspace Safety**
   - For new implementation work, create a fresh isolated worktree and neutral branch from the latest intended base before editing unless the user explicitly asks to work in the current checkout.
   - Default ordinary feature/bug work to `origin/dev` unless the task, PR metadata, or user names another base. CI may target `main`, so confirm the base when the request or PR context is ambiguous.
   - Fetch before creating/updating the worktree and branch when network/local remote state is available.
   - If `AGENTS.md` exists in the main checkout but is ignored, copy it into the isolated worktree and verify it remains ignored. Copy or point to the ignored local `db.sqlite3` only for local verification, and never stage local instructions or local DB files.
   - Preserve unrelated local changes. Do not stage or commit unless explicitly asked.
   - Use neutral branch names only, such as `feat/...` or `fix/...`. Never use AI/tool-branded prefixes.

5. **Implementation**
   - Implement only the requested behavior. Do not add adjacent features, cleanup, refactors, extra validations, extra APIs, defensive concurrency handling, docs, or tests outside the task just because they seem helpful.
   - Reuse existing selectors, services, business helpers, template classes, static JS helpers, and test patterns when tests are already in scope.
   - Keep ownership checks and staff-only schema access intact.
   - Keep schema changes versioned through the existing schema editor business path unless the task is explicitly a migration/import path.
   - Keep BOM row ids, per-country price cache, `user_edited` source, and materialized cost behavior intact.
   - Keep OpenAI calls behind the project LLM wrapper; mock them in any existing or explicitly requested tests.
   - For Open Costing work, keep original costings/results immutable, store factory responses as separate proposals, preserve request snapshots, compare BOM rows by stable row ID, handle added/removed/changed/unchanged rows, avoid division-by-zero deltas, avoid double-counting profit included in CPM, and keep factory tokens scoped, expiring, and locked after submission unless reopened.
   - Generate migrations with `uv run python manage.py makemigrations` when schema changes are required.

6. **Verification**
   - For Open Costing tasks, add or update tests for every implemented task.
   - For other tasks, do not add new tests to PRs by default. Add or update tests only when the user explicitly asks, a review/CI requirement calls for them, or the change is too risky to verify responsibly without one.
   - When tests are omitted, state the rationale and the manual/browser/check-based verification used.
   - Run the smallest meaningful command first, usually ruff/migration checks or an existing focused `uv run pytest ...` file or class when useful.
   - Run `uv run python manage.py makemigrations --check` for model/migration risk.
   - Run broader checks only when scope justifies them or the user asks: `uv run pytest`, `uv run mypy .`, or `uv run pre-commit run --all-files`.
   - For UI work, inspect or exercise the actual template/static JS path and check saved payload/state, not only the rendered element.
   - For UI work, compare against existing design-system patterns and verify no new palette, UI library, framework, icon set, font, or visual language was introduced without explicit approval.
   - For UI-visible work, use Browser verification when available and capture before/after full-page screenshots when local state permits. If screenshot capture is blocked, report the blocker.

## Final Response

Use this order:

- PM summary of the behavior delivered.
- Files changed.
- Validation run and results.
- Manual verification path when relevant.
- Technical notes only where useful.
- Screenshot evidence or blocker for UI-visible changes.
- Assumptions, risks, or blockers.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Changing schema JSON directly while bypassing version/cache logic | Use `save_new_schema_version` or explain why the task is specifically an import/migration path. |
| Treating a UI-only BOM edit as harmless | Trace saved BOM JSON, row ids, price cache, country, and totals. |
| Creating a new helper when equivalent logic already exists in a view, service, selector, template tag, command, or JS module | Reuse the existing path, or explain why it cannot be reused without changing scope. |
| Calling OpenAI directly in new code/tests | Use `apps.costing.services.llm` wrappers and patch them in any tests. |
| Assuming `main` or `dev` silently | Confirm the target base from the task, PR, or user. |
