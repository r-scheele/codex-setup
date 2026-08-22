---
name: flash-costing-continuous-verification
description: "Use when implementing, fixing, reviewing, or declaring completion for Flash Costing / flash-costing-public-dj work that must be verified against the real codebase. Applies requirement-by-requirement verification with Flash Costing-specific gates for Django/DRF/templates/vanilla JS, ownership scoping, schema editor, garment type, BOM pricing, SMV, Open Costing, Send to Factory, factory responses, delta/comparison, secure factory portal, OpenAI pipeline, Celery, migrations, UI screenshots, and PR/review hygiene."
---

# Flash Costing Continuous Verification

Use this with `flash-costing-guidelines`. Verify each requested Flash Costing requirement against the real code path before declaring completion.

## Baseline Audit

Before editing:

1. Parse the request into atomic requirements and classify each as `COMPLETE`, `PARTIAL`, `MISSING`, or `INCORRECT`.
2. Check branch and dirty state, then identify whether this is new work, PR review follow-up, merge-conflict work, or local-only verification.
3. Search the relevant product core before assuming anything is missing: `apps/costing/`, `apps/users/`, templates, static JS/CSS, selectors, services, tasks, commands, migrations, tests, and docs.
4. Do not run Graphify by default. Use `rg`, focused file reads, local tests, and browser checks until a working Graphify/LLM key is configured.
5. Define one verification path per requirement.

Keep scope strict. Do not add adjacent features, helpers, endpoints, tests, refactors, docs, validation, concurrency handling, or "safe" improvements unless the request or review explicitly requires them.

## Open Costing Gate

For Open Costing, Send to Factory, factory response, comparison, delta, secure factory portal, or related PR work:

1. Resolve the repo root and obey `AGENTS.md`.
2. Read the local Open Costing docs when present: `docs/_local/open-costing/specification.md`, `task-sheet.csv`, `decisions.md`, and `sources.md`.
3. Match the request to the relevant task-sheet phase/row when possible.
4. Treat the specification as product source of truth, decisions as resolved decisions, and task sheet as implementation breakdown.
5. Stop and surface conflicts between docs, decisions, task sheet, and code instead of silently choosing.

## Pre-Edit Gate

Before modifying a file, answer from code evidence:

- Does this behavior already exist in a model/queryset, selector, service, view/API, template, JS file, Celery task, command, migration, or test?
- Which object owns the data: `Costing`, `CostingResult`, `FactoryAccount`, `OpenCostingRequest`, `OpenCostingResponse`, `OpenCostingComment`, schema version, BOM row, labour/SMV row, or accepted version?
- Does the change affect ownership, permissions, schema history, BOM prices/totals, SMV math, Open Costing immutability, factory token access, LLM behavior, Celery retry behavior, migrations, or external services?
- Could it duplicate identity fields, timestamps, comments, relationships, calculations, helpers, DOM renderers, or API paths?

If a dependency or product decision is not explicit, stop and ask before expanding scope.

## Flash Costing-Specific Checks

Verify these when relevant:

- Ownership: user costings stay scoped through `Costing.objects.for_user(user)` or equivalent user-owned lookups; schema admin stays staff-only.
- Statuses: use named enum values and preserve pipeline order.
- Schema editor: save through `save_new_schema_version`, validate schemas, create a schema version, update `current_version`, rebuild `features_schema`, and preserve session/drag/drop/picker state.
- BOM: preserve sections, `row_id`, `prices_by_country`, country-specific pricing, `user_edited` semantics, saved item costs, totals, and lazy/idempotent generation.
- SMV: preserve element frequency, multiple-occurrence grand totals, cutting SMV, and sewing/finishing totals.
- LLM: use existing LLM helpers, pipeline config, JSON parsing, bounded retries, and mocks for tests.
- Open Costing: never overwrite original `Costing` or `CostingResult`; preserve snapshots, proposals, response locking, expiry/token scoping, accepted-version behavior, comments, stable row IDs, delta math, and no double-counted profit.
- Migrations: use `uv run python manage.py makemigrations`; avoid hand-written production data migrations or seed changes unless explicitly required.
- UI/JS: match `apps/static/css/project.css`, `fc-*` classes, existing buttons/cards/tabs/modals/status pills/dark theme, Django `{% url %}`, `json_script`, CSRF patterns, and `escapeHtml` for user-controlled strings.

## During Implementation

After every meaningful change:

1. Re-check the current requirement in the active model/service/view/template/JS/task path.
2. Confirm imports, URLs, serializers/forms, selectors/services, Celery registration, migrations, template IDs/data URLs, JS handlers, permissions, and changed symbols are wired.
3. Search for duplicate calculations, helpers, source-of-truth fields, renderers, API paths, and orphaned code.
4. Run the smallest useful focused command. Use `uv run pytest ...`, `uv run python manage.py makemigrations --check`, `uv run mypy .`, or browser/API verification when the scope justifies it.
5. Fix verification failures before moving to the next requirement.

For Open Costing tasks and bug fixes, add or update tests for the implemented task or fix. For other Flash Costing work, do not add tests by default unless explicitly requested, required by review/CI, or too risky to verify responsibly without one.

## Product Verification

For UI or product-visible work:

1. Verify through the real user path: template, API client, browser flow, or public/factory portal as appropriate.
2. Use current prompt credentials or secure local context only; never write plaintext secrets into skills, repo files, commits, or PR text.
3. Capture before/after full-page screenshots when local state can be opened.
4. Compare for accidental removals, layout shifts, changed labels, missing controls, inconsistent spacing, and broken dark-theme behavior.
5. Report exact blockers for missing data, credentials, permissions, app startup, or unreachable state.

## Final Completion Gate

Before saying the task is done:

1. Re-read the original request and verify every atomic requirement as `YES`, `NO`, or `PARTIAL` internally.
2. Search for duplicate implementation, stale code, TODOs/placeholders/mocks, broken imports, missing routes, missing migrations, orphan JS handlers, missing edge cases, and unintended removals.
3. Inspect `git diff --stat`, `git diff --name-only`, `git diff --check`, and the focused diff.
4. Confirm no unrelated changes, secrets, or AI/tool branding were introduced.
5. Report product outcome, technical path, verification, blockers, and deliberate skips.

Completion is based on verified Flash Costing behavior, not the amount of code changed.
