---
name: flash-costing-guidelines
description: Apply shared Flash Costing and flash-costing-public-dj repo guidelines with senior backend engineer, Python/Django, database-design, and frontend design-system production judgment for Django, DRF, template, JavaScript, CSS, UI color/design consistency, schema editor, garment type, feature group, feature value, SMV, BOM pricing, labour costing, Open Costing, Send to Factory, factory costing responses, profit, delta, comparison, secure factory portal, OpenAI pipeline, Celery, migration, test, PR, and review work.
---

# Flash Costing Guidelines

Apply these rules for Flash Costing work unless the user explicitly overrides a specific rule.

## Repo Shape

- Treat `apps/costing/` as the product core: models, forms, views, schema editor views, API views, selectors, business logic, services, Celery tasks, management commands, and existing tests.
- Treat `apps/users/` as auth and preference support: email-only users, `costing_preferences`, user profile views, and DRF `UserViewSet`.
- Use the existing stack: Django 5.2, DRF, django-allauth, Celery, Redis, OpenAI SDK, PyMuPDF/Pillow, openpyxl, simple-history, vanilla JavaScript, Django templates, static CSS, uv, pytest, ruff, mypy, djLint, pre-commit, and Docker Compose.
- Prefer local non-Docker commands for quick checks, and use Docker/`just` when local services or CI parity are needed.
- Do not run Graphify by default until a working API key is configured. Use normal local inspection (`rg`, focused file reads, and tests) for architecture and dependency questions.

## Production Engineering Standard

- Act as a senior backend engineer, Python/Django code reviewer, and database-design reviewer with at least 10 years of experience reviewing and maintaining production systems.
- Optimize for production correctness: data integrity, ownership/access control, transactional safety, idempotency, API compatibility, migration safety, background-task reliability, numerical accuracy, and testability.
- Consider real production failure modes before coding or approving changes: concurrent requests, Celery retries, partial saves, stale data, external API failures, malformed user input, expired permissions, and rollback/retry behavior.
- Prefer small, reversible changes that fit existing architecture. Avoid clever abstractions, broad rewrites, and style churn unless the task requires them.
- Review and self-review with evidence from the actual code path, not assumptions from naming or intended behavior.
- For model, schema, and migration work, review domain fit, normalization, foreign keys, constraints, indexes, nullability, defaults, decimal precision, timestamp/audit behavior, historical snapshots, deletion behavior, and production migration safety.
- For frontend work, preserve the established product design system, color semantics, UI components, interaction patterns, accessibility, and saved-state behavior.

## Non-Negotiables

- Strict task scope comes first. Implement only the behavior, review comment, or file change the user explicitly asked for. Do not add adjacent features, extra endpoints, model fields, helpers, refactors, documentation sections, cleanup, tests, validation, concurrency handling, or "safe" improvements just because they seem useful.
- If the requested task appears to need an unrequested dependency or supporting change, stop and ask before implementing that extra work. Do not decide silently that the dependency is necessary.
- Treat nearby context as background for avoiding mistakes, not as permission to implement surrounding tasks. Record out-of-scope findings as follow-ups instead of coding them.
- Inspect nearby code before changing behavior. Reuse existing model/queryset, selector, service, template, JS, and test patterns when they are already relevant.
- Before adding a new helper, template filter, calculation path, JS utility, model property, or service function, run a targeted search for equivalent existing logic. Reuse the closest local helper when it fits; if similar logic only exists in a nearby view or command, prefer the smallest sharing/calling path over duplicating it. If you intentionally do not reuse it, state why in the handoff.
- Before expanding a diff, pause for a scope pass: look for code blocks that can be reused, moved into an existing business/service module, simplified, or avoided entirely. Prefer surgical changes that preserve the requested behavior over broad new surfaces.
- Check the existing codebase pattern for the specific mechanism being added before choosing a style. For database transactions, locking, idempotency, queryset helpers, serializers, view classes, permissions, and validation, inspect nearby prior usage and follow the closest working local pattern unless there is a clear product or correctness reason not to.
- Follow Django and DRF conventions in the smallest practical way: keep transactions around the exact critical mutation, use `select_for_update()` only where concurrent writes matter, keep serializers focused on API shape, keep business rules outside large model/view blocks, and avoid abstractions that only hide one call site.
- Keep diffs focused. Do not refactor, restyle, rename, add dependencies, or change config unless the task requires it.
- Keep Django models lean. Models should hold fields, relationships, managers/querysets, `Meta`, `__str__`, simple properties, and small hooks only. Move long validation logic, JSON-shape checks, workflow rules, and private helper blocks out of `models.py` into a business or validation module, then call that module from `clean()` or the service/view that performs the action.
- Keep `clean()` methods thin. A model `clean()` may gather validation errors and call a domain validation function, but it should not become the main home for Open Costing workflow rules, BOM/SMV/profit JSON validation, snapshot locking rules, or accepted-version logic.
- Prefer Django `TextChoices` for model status, mode, and action domains. Avoid parallel string-constant sets in validation modules when the model enum can be imported or mirrored through a dedicated `TextChoices`; compare against named enum values instead of raw strings.
- Add `HistoricalRecords` only when the model needs audit history for product or compliance traceability. For Open Costing, prefer explicit immutable snapshots, submitted proposals, and accepted-version rows for quote history; do not add history tables to supporting account/reference models without a clear reason.
- For Open Costing factory data, use `FactoryAccount` as the single source for factory account details such as name, email, phone, website, country, and notes. Avoid adding parallel editable factory detail fields on requests or responses, including submitter name/email fields that duplicate the factory user/account, unless they are explicitly historical display snapshots and named/documented that way.
- When introducing or reviewing a source-of-truth model, run a same-domain duplication audit before handoff. List the authoritative model for each concept, then search nearby request, response, child, historical migration, test, and documentation files for duplicate fields. For Open Costing, `FactoryAccount` owns factory identity, `OpenCostingRequest` owns the factory assignment, `OpenCostingResponse` owns response revision state, and `OpenCostingComment` owns notes/discussion.
- Do not duplicate a relationship that is already reachable through the model graph. For Open Costing, response code should use `response.request.factory_account`; do not add `OpenCostingResponse.factory_account`, `submitted_by_user`, submitter name/email fields, or validators that only keep duplicated identity fields synchronized unless a separate product-approved historical snapshot requires them.
- Keep lifecycle timestamps on the model that owns the event. For Open Costing, request timestamps track request lifecycle events such as sent, opened, reviewed, accepted, rejected, and expired; response submission time belongs on `OpenCostingResponse.submitted_at`. Do not add matching parent/child timestamps unless the parent timestamp is explicitly denormalized for a documented query/reporting need.
- Use `OpenCostingComment` for Open Costing notes, required explanations, and discussion targets. Do not add inline `comment`, `overall_comment`, `override_comment`, row-comment, profit-comment, or similar text columns to response/proposal models when a targeted comment can represent the note. Add a focused `OpenCostingCommentTarget` value when the existing targets do not cover the section.
- Preserve user data scoping. User costings must stay scoped through `Costing.objects.for_user(user)` or `get(pk=..., user=request.user)` in UI and API paths.
- Preserve schema admin access. Schema and feature-group views use `StaffRequiredMixin`; do not widen that surface without explicit product approval.
- Preserve `CostingStatus` semantics. Use named enum values and the existing pipeline order: pending, reviewing, classifying, detecting_elements, detecting_features, generating_bom, completed, failed.
- Preserve `GarmentType.elements_schema` and denormalized `features_schema` semantics. Save edited schemas through `save_new_schema_version`, validate with `validate_elements_schema`, create a new `GarmentTypeSchemaVersion`, update `current_version`, and rebuild `features_schema`.
- Preserve feature-group history and deletion rules. Feature group/value mutations set `_change_reason`; hard-deleting a group is blocked while active garments reference it.
- Preserve SMV math. Single features multiply by element frequency; multiple-occurrence feature counts are already grand totals across the element. Cutting SMV lives in `cutting_info` and is added separately from sewing/finishing element SMV.
- Preserve BOM structure and price cache semantics. BOM sections are `fabric`, `trims`, and `packing`; `row_id` identifies rows; `prices_by_country` is per-country; `user_edited` prices must not be overwritten by LLM repricing or bleed across countries.
- Preserve lazy/idempotent BOM generation. `generate_bom_for_costing` returns an existing saved BOM; Pass 2 repricing failure should not discard a usable Pass 1 BOM unless the task explicitly changes that contract.
- Preserve materialized costs. When unit price, consumption, waste, or cached pricing changes, keep saved BOM item `cost` values and UI totals consistent.
- Preserve LLM wrapper behavior. Use `apps.costing.services.llm` helpers, `pipeline_config.json`, JSON parsing helpers, and bounded retries. Existing or explicitly requested tests must mock OpenAI calls.
- Preserve accepted upload types unless requirements change: PDF, JPG, JPEG, PNG, and WEBP.
- Keep management commands idempotent when existing commands are idempotent. Use `--dry-run` patterns for schema/BOM import changes where present.
- Treat migrations and data files as product behavior. Generate Django migrations with `uv run python manage.py makemigrations`; do not hand-write production data migrations or seed changes unless explicitly required.
- Do not commit secrets or local env files. `.env`, `.envs/`, API keys, media uploads, and local database state stay machine-local.

## Open Costing Context Loading

For any Open Costing, Send to Factory, factory costing response, comparison, delta, or secure factory portal task, bug fix, PR review, or PR hygiene work:

1. Resolve the Git repository root, for example with `git rev-parse --show-toplevel`.
2. Obey the active `AGENTS.md` instruction chain before planning, reviewing, or editing.
3. Before planning, reviewing, or editing code, read these local files in full when present, resolving paths from the repository root:
   - `docs/_local/open-costing/specification.md`
   - `docs/_local/open-costing/task-sheet.csv`
   - `docs/_local/open-costing/decisions.md`
   - `docs/_local/open-costing/sources.md`
4. Match the user request, bug, PR, or review comment to the relevant Open Costing task-sheet phase and row when possible. Read surrounding tasks for awareness only; implement or review only the requested scope. If an unrequested dependency appears necessary, stop and ask before changing it.
5. Treat `specification.md` as the product source of truth, `decisions.md` as the source of resolved decisions, and `task-sheet.csv` as the implementation breakdown.
6. Before coding, produce a concise implementation understanding that names the matched task and phase, relevant requirements, affected existing code, dependencies and risks, and tests that should be added or updated.
7. Before review-only work, use the same context as the review baseline and flag any changed code that conflicts with the specification, decisions, or task sheet.
8. Inspect the existing implementation and follow established project patterns before introducing new abstractions.
9. If the specification, decisions, task sheet, or existing code conflict, do not silently resolve the conflict. State the conflict and use the safest reversible implementation or review recommendation.

## Open Costing Rules

- Never overwrite or mutate the original `Costing` or `CostingResult`.
- Store factory responses as separate proposals linked to the original costing.
- Preserve a read-only snapshot of the original costing when a request is created.
- Keep Open Costing model classes small. Put request, response, BOM, labour/SMV, profit, snapshot, lock, and acceptance validation in a dedicated business/validation module instead of adding large validation helper sections to `apps/costing/models.py`.
- Treat access control as the first gate, not a fallback validation error. Brand-side Open Costing views must fetch through the owning costing/user; factory-side views must fetch through the scoped token or authenticated factory account. Validation may reject inconsistent objects, but users who cannot view or submit a request should not be able to load it in the first place.
- Before approving or handing off Open Costing model changes, perform a normalization sweep: no duplicate factory identity on responses, no duplicate submitter fields when `FactoryAccount.user` already identifies the factory user, no duplicate request/response submission timestamps, and no inline proposal comments when `OpenCostingComment` can target the response, BOM row/section, labour section/row, profit, or summary.
- Use stable row IDs for original BOM rows before comparing factory changes.
- Support added, removed, changed, and unchanged BOM rows.
- Prevent division-by-zero in percentage delta calculations.
- Do not double-count profit when profit is included in CPM.
- Accepting or rejecting a factory response must not overwrite the original result.
- Factory token access must expose only the linked request, respect expiry, and lock submitted responses unless explicitly reopened.
- Add or update tests for every implemented Open Costing task or bug fix.
- Do not silently resolve conflicts between the specification, decisions, and existing code. State the conflict and use the safest reversible implementation.

## Documentation

- Treat product and workflow documentation as a technical writing task, not a code dump. Write for product, QA, support, and future engineers who need to understand the behavior without reverse-engineering the implementation.
- Use clear human language, active voice, and concrete examples. Avoid robotic phrasing, generated-sounding summaries, and long checklist prose when a short explanation would be clearer.
- Keep documentation accurate to the code and requirements: define statuses, ownership, state changes, access rules, validation behavior, and pending decisions. Lead with implemented behavior and avoid adding non-goals, negative capability statements, or "does not accept/support" wording unless the user asks for it or it is necessary to document a security boundary, compatibility contract, or product-critical limitation.
- Prefer source-of-truth docs for durable business rules. Link or index the document from the existing docs structure when the repo already has one.

## UI And JavaScript

- Treat the current UI as the design source of truth. Inspect nearby templates, `apps/static/css/project.css`, existing static JS, and comparable screens before changing UI.
- Preserve the existing product design principle: quiet, utilitarian, workflow-focused garment-costing screens built for repeated operational use. Do not introduce marketing-page, oversized hero, decorative card-heavy, or unrelated visual patterns into app workflows.
- Follow the existing visual system in `apps/static/css/project.css`: `fc-*` classes, `btn-primary`, `btn-secondary`, `btn-ghost`, cards, status pills, forms, tabs, modals, and dark-theme variables.
- Reuse existing color variables, palette, semantic states, spacing, border radius, typography, table/form patterns, empty/loading/error states, and responsive behavior. Do not add a new palette, one-off colors, font stack, shadow language, or radius system unless the task explicitly requires it.
- Reuse existing UI libraries, helpers, and icon patterns already present in the project. Do not introduce a new frontend framework, CSS system, UI component library, icon system, animation library, bundler, or dependency for ordinary UI work.
- Keep new Open Costing, Send to Factory, comparison, delta, and secure factory portal UI visually consistent with the existing Flash Costing app: same buttons, cards, tabs, tables, badges, forms, alerts, and dark-theme behavior.
- Preserve accessibility and interaction quality: visible focus states, labels, keyboard-reachable controls, adequate contrast, readable error messages, non-overlapping text, and stable layout on mobile and desktop.
- Use Django `{% url %}` tags and `data-*` URLs instead of hardcoded internal URLs in templates.
- Use `json_script` for server JSON injected into pages.
- Escape user-controlled strings before assigning to `innerHTML`. Existing static JS has `escapeHtml`; reuse it or write the same targeted helper.
- Preserve existing vanilla JS patterns: `fetch`, `X-CSRFToken`, `X-Requested-With` for partials, `sessionStorage` state in schema editor, and targeted DOM updates.
- For BOM UI changes, trace both DOM state and saved JSON payload: row ids, section names, `price_source`, `prices_by_country`, `view_state`, notes, country changes, and totals.
- For schema editor UI changes, trace rendered tree state, drag/drop, picker behavior, session storage, validation errors, save payload, and feature group/value refreshes.

## Backend And API

- Use selectors for query composition when a selector already exists, especially library and schema lookups.
- Use service/business modules for reusable domain behavior: schema validation/versioning, feature group mutations, SMV, labour, BOM pricing, PDF, LLM, redesign, refine, and similarity.
- Keep serializers focused on API shape and validation. Keep multi-step workflow, LLM, schema versioning, and persistence orchestration in views, services, tasks, or business modules.
- Use DRF `Response` and `serializer.is_valid(raise_exception=True)` in DRF APIs. Use `JsonResponse` in template-backed JSON views where that is the local pattern.
- Protect read endpoints with the same ownership/staff checks as writes. Authentication alone is not enough for user-owned costings.
- Keep Open Costing model documentation in a dedicated Open Costing document or section, not a broad generated model reference. Document the workflow models, ownership, snapshots, proposals, statuses, and accepted-version records together so future reviewers can reason about the domain boundary.

## Verification

- For Open Costing tasks and bug fixes, add or update tests for every implemented task or fix.
- For other Flash Costing PRs, do not add new tests by default. Add or update tests only when the user explicitly asks, a review/CI requirement calls for them, or the change is too risky to verify responsibly without one.
- When tests are omitted, state the rationale and provide the manual/browser/check-based verification used.
- System-level tool installs are allowed when they directly unblock implementation or verification work, such as installing Playwright browser binaries for local UI testing. Keep those installs out of the project dependency files unless the task explicitly requires a repo dependency change.
- For workflow/API behavior, supplement automated tests with at least one real user-path check when feasible. Exercise the request through the same public endpoint, view, API client, or browser path a user would use; if a step must use a model save because no user-facing edit path exists, call that out plainly.
- Treat user-provided manual scenarios as task-specific acceptance checks. Verify them for that task, but do not promote the scenario itself into a standing repo rule unless the user explicitly asks.
- When existing tests are useful to run, choose focused tests first:
  - API and ownership: `uv run pytest apps/costing/tests/test_api.py`
  - BOM pricing and views: `uv run pytest apps/costing/tests/test_services_bom_pricing.py apps/costing/tests/test_views_bom.py apps/costing/tests/test_tasks_bom_pricing.py`
  - Schema editor/versioning: `uv run pytest apps/costing/tests/test_schema_editor.py apps/costing/tests/test_views_schema_tree.py apps/costing/tests/test_views_schema_editor.py`
  - LLM wrapper/pipeline: `uv run pytest apps/costing/tests/test_services_llm.py apps/costing/tests/test_tasks.py`
  - Management commands/imports: `uv run pytest apps/costing/tests/test_management_commands.py apps/costing/tests/test_bom_reference.py apps/costing/tests/test_services_schema_xlsx_import.py`
- Run `uv run python manage.py makemigrations --check` whenever models or migrations may be affected.
- Run `uv run mypy .`, existing focused `uv run pytest ...`, or `uv run pre-commit run --all-files` when the scope or requested handoff justifies broader checks.
- For UI-visible implementation work, use the Browser plugin/in-app Browser for `localhost` or `127.0.0.1` verification when available. Use credentials from the current prompt or secure local context only; do not write plaintext passwords, API keys, session cookies, or account secrets into skills, repo files, commits, or PR text.
- For UI-visible changes, capture before and after full-page screenshots when the local state can be opened. Compare them for accidental removals, layout shifts, changed labels, missing controls, and inconsistent spacing. If screenshots are blocked by local data, permissions, credentials, app startup, or missing state, report the exact blocker.
- CI runs pre-commit and Docker Compose pytest for PRs to `main`; the active local default branch may be `dev`. Confirm the intended base before branch or PR work.

## Branch, Workspace, And Git

- For new Flash Costing implementation work, create a fresh isolated worktree and neutral branch from the latest intended base before editing unless the user explicitly asks to work in the current checkout. Default ordinary feature/bug work to `origin/dev` unless the task, PR metadata, or user names another base.
- Use neutral branch names such as `feat/...`, `fix/...`, `chore/...`, `setup/...`, or `devops/...`. Do not include AI or tool branding.
- If the task is review-comment or merge-conflict work on an open PR, work directly on the existing PR head branch unless the user asks for a separate branch.
- If the main checkout is dirty, still use a fresh isolated worktree for new implementation work. Do not modify or revert unrelated local changes in the main checkout.
- After creating or switching into an isolated worktree, make sure local ignored development files are available when needed: copy `AGENTS.md` from the main checkout if present, verify it is ignored, and copy or point to the ignored local `db.sqlite3` only for local verification. Never stage, commit, push, or PR these local files.
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
