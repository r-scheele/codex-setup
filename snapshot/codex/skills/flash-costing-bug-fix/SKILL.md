---
name: flash-costing-bug-fix
description: Use when fixing a Flash Costing or flash-costing-public-dj bug with senior backend engineer, Python/Django, database-design, and frontend design-system production judgment from a report, screenshot, log, traceback, failing test, PR comment, customer issue, or reproduction involving Open Costing, Send to Factory, factory costing responses, secure factory portal access, profit, delta, comparison, costings, uploads, status polling, garment schemas, feature groups, SMV, BOM, labour costs, UI color/design consistency, OpenAI pipeline, schema imports, or API ownership.
---

# Flash Costing Bug Fix

Use this skill to turn a Flash Costing bug report into a minimal, verified fix.

## Required Sub-Skill

Use `$flash-costing-guidelines` whenever available.

Read `AGENTS.md` first when it exists.

Before editing, follow the branch/workspace rules in `$flash-costing-guidelines`: bug-fix implementation work should happen in a fresh isolated worktree on a neutral branch from the intended base unless the user explicitly asks to use the current checkout.

## Engineering Posture

- Act as a senior backend engineer, Python/Django debugger, and database-design reviewer with at least 10 years of production systems experience.
- Diagnose from evidence before changing code. Trace the failing production path through validation, queryset scoping, transactions, persistence, side effects, retries, and error handling.
- Prefer the smallest reversible fix that preserves architecture and data. Avoid masking missing configuration or invalid data unless product requirements explicitly ask for that behavior.
- For data-model bugs, inspect foreign keys, constraints, indexes, nullability, defaults, deletion behavior, snapshots/history, migration assumptions, tenant boundaries, and whether mutable source records can corrupt historical behavior.
- For UI bugs, fix the broken path while preserving existing design principles, `project.css` variables/classes, color semantics, component patterns, vanilla JS helpers, accessibility, and responsive behavior.
- Before handoff, self-review for data corruption, access leaks, non-atomic saves, concurrency/retry hazards, migration risk, API contract breaks, and missing regression coverage.

## Open Costing Bug Context

For any Open Costing, Send to Factory, factory costing response, comparison, delta, or secure factory portal bug:

1. Complete the Open Costing context-loading workflow in `$flash-costing-guidelines` before triage, planning, or editing.
2. Match the bug to the relevant Open Costing task-sheet phase and row when possible.
3. State the relevant specification/decision requirements, affected code path, dependencies and risks, and regression tests to add or update before coding.
4. Apply the Open Costing rules from `$flash-costing-guidelines` as fix constraints, especially immutable originals, separate factory proposals, snapshot preservation, stable BOM row IDs, safe deltas, profit handling, token scope/expiry, response locking, and conflict handling.

## Bug Triage Before Editing

Extract and state:

- Actual behavior.
- Expected behavior.
- Affected user or role: anonymous, authenticated user, costing owner, other user, staff schema editor, API caller, or management-command operator.
- Reproduction path: URL, action, API request, uploaded file type, costing status, garment type, country, schema state, or command args.
- Suspected code path after inspection.
- Smallest fix and non-goals.
- Blockers or questions only when the missing answer changes product behavior, access, schema/data model, pricing/SMV math, or LLM failure semantics.

Do not guess a fix first. Inspect the failing path and nearby existing tests when useful.

## Evidence Handling

- For screenshots, compare visible UI with the template and static JS that render it. Treat missing controls, wrong copy, wrong totals, broken tabs, stuck status, and layout breakage as evidence.
- For visual bugs, compare against nearby existing screens and flag design-system drift: new colors, mismatched buttons/cards/tabs/forms, inconsistent spacing, inaccessible contrast, broken focus states, mobile overlap, or unapproved UI libraries.
- For logs/tracebacks, trace the call stack into views, API views, services, tasks, or management commands before editing.
- For LLM or pipeline failures, identify the step: prepare, review_document, classify_pattern_pieces, detect_elements, detect_features, generate_bom, reprice_bom, chat, redesign, or refine.
- For data issues, identify whether the source is schema JSON, schema version/cache, feature groups/values, labour config, BOM reference prices, upload/page images, or user preferences.

## Scope Rules

Fix only the reported bug.

Allowed when directly required:

- Small changes to templates, static JS, views/API views, serializers, forms, selectors, services, tasks, business helpers, management commands, models, or generated migrations.
- Defensive validation or error handling for the broken path.
- Existing focused tests or manual/browser verification that reproduce the bug or protect the risky behavior.

Do not:

- Rewrite working pipeline/schema/BOM flows.
- Change ownership/staff access unless the bug is explicitly an access bug and expected behavior is confirmed.
- Add dependencies or frontend frameworks.
- Add fallback business data that hides missing schema, labour, price, or OpenAI configuration unless product asks for it.
- Change production seed/data migrations unless the bug is in production data setup.

## Fix Rules

- Preserve `Costing.objects.for_user(user)` and `get(pk=..., user=request.user)` ownership checks.
- Preserve `StaffRequiredMixin` on schema/feature-group admin views.
- Preserve `CostingStatus` state names and pipeline order.
- Preserve schema versioning and `features_schema` cache rebuild behavior.
- Preserve BOM `row_id`, `prices_by_country`, `price_source`, `user_edited`, and cost materialization semantics.
- Preserve SMV math for single versus multiple features and separate cutting SMV.
- Preserve OpenAI wrapper retry/parsing behavior and mock external calls in any existing or explicitly requested tests.
- Preserve template URL tags, CSRF headers, `json_script`, and JS escaping around `innerHTML`.
- For Open Costing bugs, add or update regression tests for the implemented fix.
- For other bugs, do not add new regression tests to PRs by default. Add or update tests only when the user explicitly asks, a review/CI requirement calls for them, or the bug is too risky to verify responsibly without one. Otherwise, state why tests were omitted and give the manual/browser/check-based verification path.

## Validation

Run the exact reproduction path when possible. If not possible, run the closest safe focused check and state what remained unverified.

Useful focused checks:

- API/ownership: `uv run pytest apps/costing/tests/test_api.py`
- BOM bug: `uv run pytest apps/costing/tests/test_services_bom_pricing.py apps/costing/tests/test_views_bom.py apps/costing/tests/test_tasks_bom_pricing.py`
- Schema bug: `uv run pytest apps/costing/tests/test_schema_editor.py apps/costing/tests/test_views_schema_tree.py apps/costing/tests/test_views_schema_editor.py`
- Pipeline/LLM bug: `uv run pytest apps/costing/tests/test_services_llm.py apps/costing/tests/test_tasks.py`
- Import/command bug: `uv run pytest apps/costing/tests/test_management_commands.py apps/costing/tests/test_bom_reference.py apps/costing/tests/test_services_schema_xlsx_import.py`

Run `uv run python manage.py makemigrations --check` if model or migration state may be affected.

For UI-visible bugs, use Browser verification when available and capture before/after full-page screenshots when the broken state can be opened. Compare them before handoff and report screenshot blockers explicitly.

## Final Response Format

1. PM summary: what was broken, what was fixed, why it matters, and what is unchanged.
2. How to verify manually: exact page/API/command steps and expected result.
3. Validation run: commands or manual checks and results.
4. Screenshot evidence or blocker for UI bugs.
5. Technical notes: root cause, key files/functions touched, and important code paths in user-flow order.
6. Branch/worktree used.
7. Risks, assumptions, and blockers.
