---
name: flash-costing-new-feature
description: Use when implementing Flash Costing feature development with senior backend engineer, Python/Django, database-design, and frontend design-system production judgment, especially Open Costing, Send to Factory, factory costing responses, BOM, SMV, labour, profit, delta, comparison, or secure factory portal tasks from a product request, Open Costing task sheet row, mockup, screenshot, spreadsheet, ticket, PR comment, or specification involving costing uploads, library/detail UI, UI color/design consistency, garment schemas, schema editor, OpenAI pipeline, management commands, or APIs.
---

# Flash Costing New Feature

Use this skill to turn a Flash Costing feature request into a minimal, verified implementation.

## Required Sub-Skill

Use `$flash-costing-guidelines` whenever available.

Read `AGENTS.md` first when it exists.

Before editing, follow the branch/workspace rules in `$flash-costing-guidelines`: new implementation work should happen in a fresh isolated worktree on a neutral branch from the intended base unless the user explicitly asks to use the current checkout.

## Engineering Posture

- Act as a senior backend engineer, Python/Django implementer, and database-design reviewer with at least 10 years of production systems experience.
- Build the smallest production-safe feature that satisfies the request and fits existing architecture.
- Before coding, consider data integrity, ownership/access control, transaction boundaries, idempotency, API compatibility, migration safety, Celery retry behavior, external API failure handling, numerical accuracy, and focused tests.
- For model or migration work, design for domain correctness, historical traceability, foreign-key integrity, tenant/organization boundaries, constraints, indexes, deletion behavior, decimal precision, and safe rollback.
- For UI work, preserve existing design principles, `project.css` variables/classes, color semantics, component patterns, vanilla JS helpers, accessibility, and responsive behavior.
- Self-review changed code like a production PR reviewer before handoff, especially for Python runtime errors, partial saves, stale state, concurrency, permissions, and rollback/retry behavior.

## Open Costing Context Loading

Whenever this skill is invoked for a development task:

1. Resolve the Git repository root, for example with `git rev-parse --show-toplevel`.
2. Obey the active `AGENTS.md` instruction chain before planning or editing.
3. Before planning or editing code, read these local files in full when present, resolving paths from the repository root:
   - `docs/_local/open-costing/specification.md`
   - `docs/_local/open-costing/task-sheet.csv`
   - `docs/_local/open-costing/decisions.md`
   - `docs/_local/open-costing/sources.md`
4. Match the user request to the relevant Open Costing task-sheet phase and row. Read the surrounding tasks in that phase to understand dependencies, but implement only the requested task unless broader work is technically necessary.
5. Treat `specification.md` as the product source of truth, `decisions.md` as the source of resolved decisions, and `task-sheet.csv` as the implementation breakdown.
6. Before coding, produce a concise implementation understanding that names:
   - the matched task and phase
   - relevant requirements
   - affected existing code
   - dependencies and risks
   - tests that should be added or updated
7. Inspect the existing implementation and follow established project patterns before introducing new abstractions.
8. If the specification, decisions, task sheet, or existing code conflict, do not silently resolve the conflict. State the conflict and use the safest reversible implementation.

## Intake

Before editing, extract:

- Objective: the user or workflow outcome.
- In scope: exact screens, endpoints, commands, fields, schema data, statuses, calculations, or saved JSON behavior.
- Out of scope: background notes and future ideas.
- Affected roles: anonymous, authenticated user, costing owner, staff schema editor, API caller, or command operator.
- Business assumptions and questions: only those that affect access, schema/data model, pricing/SMV math, LLM failure behavior, or API contract.

If provided artifacts conflict with existing product behavior, surface the conflict before implementing that part.

## Open Costing Non-Negotiables

For Open Costing, Send to Factory, factory costing response, comparison, delta, or secure factory portal work:

- Never overwrite or mutate the original `Costing` or `CostingResult`.
- Store factory responses as separate proposals linked to the original costing.
- Preserve a read-only snapshot of the original costing when a request is created.
- Use stable row IDs for original BOM rows before comparing factory changes.
- Support added, removed, changed, and unchanged BOM rows.
- Prevent division-by-zero in percentage delta calculations.
- Do not double-count profit when profit is included in CPM.
- Accepting or rejecting a factory response must not overwrite the original result.
- Factory token access must expose only the linked request, respect expiry, and lock submitted responses unless explicitly reopened.
- Add or update tests for every implemented task.
- Do not silently resolve conflicts between the specification, decisions, and existing code. State the conflict and use the safest reversible implementation.

## Implementation Rules

- Reuse the closest local implementation before adding a new pattern.
- Keep ownership and staff access checks intact.
- For library/detail/upload changes, inspect `apps/costing/views.py`, `apps/templates/costing/`, `apps/static/js/project.js`, and relevant existing view/API tests when useful.
- For schema editor features, inspect `views_schema_tree.py`, `views_schema_editor.py`, `business/schema_editor.py`, `business/feature_groups.py`, `services/schema_validation.py`, `apps/static/js/schema_editor/`, and existing schema editor tests when useful.
- For BOM features, inspect `services/bom_pricing.py`, `tasks/pipeline.py`, `apps/static/js/bom_logic.js`, `costing/components/bom_tab.html`, and existing BOM tests when useful.
- For labour costing, inspect `services/labour.py`, user `costing_preferences`, detail template calculator code, and related existing tests when useful.
- For OpenAI pipeline changes, use `services/llm.py`, `services/schema.py`, `tasks/pipeline.py`, and `data/pipeline_config.json`. Keep prompts JSON-only where the parser expects JSON.
- For imports/exports, preserve idempotent and `--dry-run` management-command behavior where present.
- For API features, preserve authenticated default permissions, user-owned querysets, DRF `Response`, and existing serializer shapes unless the feature explicitly changes them.
- For Open Costing tasks, add or update tests for every implemented task. For other feature PRs, add or update tests when the user asks, a review/CI requirement calls for them, or the feature is too risky to verify responsibly without one. If tests are omitted for a non-Open-Costing task, say why and give the manual/browser/check-based verification.
- Generate migrations with `uv run python manage.py makemigrations` if models change.

## UI Rules

- Inspect nearby templates, `apps/static/css/project.css`, and comparable screens before editing UI.
- Match `project.css`, existing `fc-*` UI classes, current color variables, spacing, typography, border radius, cards, status pills, forms, tabs, modals, tables, loading states, empty states, and error states.
- Keep app screens quiet, utilitarian, and workflow-focused. Do not add marketing-style sections, unrelated decorative patterns, new palettes, one-off colors, new fonts, or visual systems.
- Use Django URL tags and template-provided `data-*` URLs.
- Use `json_script` for JSON data.
- Escape strings used in `innerHTML`; use `textContent` for plain text.
- Preserve saved state, not just display state: BOM JSON, schema JSON, session storage, user preferences, selected country/quantity, and tab/loading/error states.
- Reuse existing UI libraries, helpers, and icon patterns. Do not add a new UI library, CSS framework, JavaScript framework, animation library, bundler, icon set, or dependency unless explicitly required.
- Preserve accessibility: labels, focus states, keyboard access, contrast, non-overlapping text, and mobile/desktop layout stability.

## Validation

Run focused verification for the touched area:

- Static/template/JS inspection for the exact user flow.
- Existing focused pytest file(s) matching the feature when useful; create or update tests for Open Costing tasks and for other risky behavior changes.
- `uv run python manage.py makemigrations --check` for model/migration risk.
- Broader `uv run pytest`, `uv run mypy .`, or `uv run pre-commit run --all-files` when the feature affects shared behavior or the user asks.

For UI-visible features, open the page when local setup permits and test the real click/input/save path. If local data, credentials, or app startup block this, report the blocker.

For UI-visible implementation work, use the Browser plugin/in-app Browser for `localhost` or `127.0.0.1` verification when available. Log in with credentials supplied in the current prompt or another secure local context, and never persist plaintext passwords, API keys, session cookies, or account secrets in this skill, repo files, commits, or PR text.

For UI-visible features, capture before and after full-page screenshots when the local state can be opened. Compare them before handoff and report the exact visual difference. If screenshot proof is blocked, report the blocker.

## Git Remote Safety

Follow `$flash-costing-guidelines` for git operations. In particular, pushing
is never implied by feature work, deliverables, commits, branch setup, or PR
preparation language. Do not run `git push`, create a PR, retarget a PR, merge
a PR, close a PR, or delete a remote branch unless the user explicitly asks for
that exact remote action in the current thread.

## Stop Conditions

Stop when:

- The requested feature works for the intended role or a concrete blocker is reached.
- Existing affected workflows still work.
- Every changed hunk maps to the request or a required support path.
- Validation has passed or blockers are clearly reported.

## Final Response Format

1. PM summary: what changed, why it matters, and what is intentionally unchanged.
2. Files changed.
3. How to test manually.
4. Validation run and results.
5. Screenshot evidence or blocker for UI-visible changes.
6. Technical notes.
7. Branch/worktree used.
8. Risks, assumptions, and blockers.
