---
name: seamstream-guidelines
description: "Use when working in __HOME__/Desktop/code/seamstream_ai, SeamstreamAI, Seamstream Django/frontend code, tech-pack import, operation breakdown, BOM, SMV, factory setup, subscriptions, flash costing, LLM/cache, domain database routing, frontend design-system consistency, or when the prompt includes `$seamstream-guidelines`."
---

# Seamstream Guidelines

Apply these rules for every Seamstream implementation unless the user explicitly overrides a specific rule.

## Repository Facts

- Repository path: `__HOME__/Desktop/code/seamstream_ai`.
- Default remote branch observed at creation time: `main` tracking `origin/main`; do not assume a `dev` branch.
- This repo currently has no `AGENTS.md`; if one appears in the checkout, read it before editing and follow it with this skill.
- Runtime stack: Django 4.2 project with Django REST Framework, Django templates, Tailwind CDN, Lucide CDN, Font Awesome in the main shell, custom CSS/token utilities, plain JavaScript modules, SQLite local DBs, optional S3 storage, OpenAI/Gemini LLM calls, Stripe, SendGrid, Slack logging, and APScheduler.
- Internal apps are `apps.converter`, `apps.subscription`, `apps.accounts`, `apps.messaging`, and `apps.factory`; `apps.flash_costing` is also present with API/templates but is not in `INTERNAL_APPS` in `seamstream_ai/app_settings/base.py`.
- Key paths: `seamstream_ai/app_settings/`, `seamstream_ai/db_logics/`, `seamstream_ai/api_router.py`, `seamstream_ai/urls.py`, `apps/accounts/`, `apps/converter/`, `apps/converter/v2/`, `apps/factory/`, `apps/flash_costing/`, `apps/subscription/`, `apps/messaging/`, `templates/`, `static/js/`, `static/css/`, `resources/`, `schema-data/`, and `tests/apps/converter/business_layer/`.

## Non-Negotiables

- State assumptions explicitly; never guess silently. If intent is unclear after inspecting the relevant Seamstream code, call out the assumption or ask before changing behavior.
- Define success before changing code: expected behavior, acceptance criteria, affected user/workflow, and verification path.
- Make surgical changes only. Do not refactor, restyle, reorganize, rename, or clean adjacent code unless the task explicitly requires it.
- Reuse existing local patterns first. Check nearby Seamstream implementations before adding new helpers, APIs, UI components, settings, or data flows.
- Treat the current UI as the design source of truth. Preserve Seamstream's existing product design principle, visual language, interaction patterns, saved state, and responsive behavior unless the user explicitly requests a visual redesign.
- Preserve existing behavior and payload semantics unless the request explicitly changes them.
- Do not remove, hide, shadow, bypass, or orphan existing UI controls, routes, API actions, serializer fields, model fields, template blocks, JavaScript handlers, scheduler behavior, cache behavior, or storage paths unless the user explicitly asks for removal and references have been checked.
- Treat indirect removals as removals: duplicate renderers, duplicate action names, unreachable buttons, replaced DOM without handlers, narrowed conditions, or new code paths that shadow old behavior are risky.
- When deleting or renaming a function, method, model field, route, URL name, template include, JavaScript export, management command, or shared helper, search references with `rg`/`git grep` and report the result.
- Do not import conventions from other repositories. Seamstream uses direct factory/profile scoping and does not have an entity permission-helper layer, DaisyUI, `uv`, or a default `dev` branch in the inspected checkout.
- Do not put AI/editor/tool branding in code, comments, generated copy, branch names, commit messages, PR titles/bodies, screenshots, or review comments.
- Do not commit, push, merge, retarget, close PRs, or delete branches unless the user explicitly asks.
- Never force-push or run forceful/destructive git operations. Do not use `git push --force`, `--force-with-lease`, `git branch -D`, `git tag -f`, `git reset --hard`, `git clean -fd`, `git checkout -f`, or any git flag/command whose purpose is to force, overwrite, or discard work; if asked, refuse and offer a non-force alternative.
- If the working tree has unrelated local changes, do not modify or revert them.

## Preflight Checkpoint

- Before editing code, inspect the local code paths that likely encode the current behavior: URLs/views/viewsets, serializers, models/migrations, business/service modules, templates, static JS, settings, tests, and resources when relevant.
- Before changing UI, inspect nearby templates, `static/css/` theme/token files, static JavaScript, and comparable screens to understand the approved layout, component, color, state, and persistence patterns.
- Ask before changing permissions/access, factory scoping, staff behavior, API contract shape, serializer/service boundaries, database routing, migrations/data population, Stripe/SendGrid/S3 behavior, LLM model selection/caching, scheduler behavior, failure semantics, or business rules.
- When asking, include what code was checked, the code-derived current behavior, the requested behavior, the default recommendation, and whether confirmation is still needed.
- For PM/business questions, phrase the first line in plain product language. Avoid engineering shorthand unless the user asked for it.
- If screenshots, spreadsheets, PDFs, mockups, logs, or traces are supplied, treat them as primary evidence and inspect them before editing.

## Tooling And Commands

- Prefer `rg`, `git diff`, `git grep`, and `sg` when structural search reduces risk. `sg` is optional; do not add it to project dependencies.
- At the start of every Seamstream feature development task, run `/graphify .` from the repository root before planning or editing code so the repo graph is built or refreshed for architecture and dependency questions. If Graphify is blocked, report the blocker and continue with normal local inspection; do not guess from memory.
- Use the repo's plain Python/Django commands, not `uv`: `python manage.py ...` or `make ...`.
- Setup/run commands observed in the repo:
  - `pip install -r requirements/dev.txt`
  - `make full_setup`
  - `python manage.py runserver`
  - `make run` starts `ENABLE_SCHEDULER=true python manage.py runserver_plus`.
  - `python manage.py test tests` or focused paths such as `python manage.py test tests.apps.converter.business_layer`.
- Be careful with `make full_setup`: it runs `makemigrations`, `migrate`, `csv_to_json`, `extract_encoding_combination`, `ingest_data`, and `collectstatic`; do not run it casually when a focused command is enough.
- Use `python manage.py makemigrations --check --dry-run` to check whether model changes need migrations.
- Run pre-commit only when a commit is requested or the touched files justify it. The configured hooks are trailing whitespace, EOF fixer, YAML check, Black, isort, and flake8; `pre-commit` may not be installed locally.

## Branch, Database, And Environment

- Default new work against `main` unless the user or PR says otherwise.
- Before editing, check branch and dirty state with `git status --short --branch`.
- Use neutral branch names such as `feat/<short-description>` and `fix/<short-description>` if the user asks for a branch. Never use AI/tool-branded prefixes.
- Local settings are selected through `ENVIRONMENT`; default is `local`.
- Local settings create branch-specific SQLite DB files: `db_<branch>.sqlite3`, `db_tal_<branch>.sqlite3`, and `db_technosport_<branch>.sqlite3`.
- Domain database routing maps `app.seamstream.ai` to `default`, `tal.seamstream.ai` to `tal`, and `technosport.seamstream.ai` to `technosport`; with `ENVIRONMENT=local`, `app.local`, `tal.local`, and `technosport.local` map the same way.
- If work touches database routing, use `seamstream_ai/db_logics/domain_router_middleware.py`, `database_router.py`, `db_context.py`, and `utils.py` as source of truth.
- If local verification needs a tenant DB, explicitly set the host/domain path or DB context rather than assuming `default`.

## Django And API Rules

- Use DRF `Response` for DRF endpoints and Django `JsonResponse` only for existing non-DRF view patterns.
- For v2 converter APIs that already use `APIResponseOk` / `APIResponseFail` from `apps/converter/v2/api/helper.py`, keep that envelope unless the task explicitly changes it.
- Do not force every endpoint into one response shape. `apps/factory/api/views.py`, `apps/subscription/api/views.py`, `apps/converter/api/views.py`, `apps/converter/v2/api/views.py`, and `apps/flash_costing/api/views.py` currently use different local response shapes.
- Prefer `serializer.is_valid(raise_exception=True)` for DRF writes when serializers are used; preserve existing manual validation only when matching a nearby endpoint.
- Keep workflow and multi-step business logic in business/service modules when a local module exists: `apps/converter/business_layer/`, `apps/converter/v2/business_layer/`, `apps/subscription/business_layer.py`, `apps/accounts/business_layer.py`, and `apps/flash_costing/services/`.
- Do not move code between serializers, views, and business layers without a concrete reason and a small diff.
- Preserve access scoping. Factory-owned data is commonly scoped through `request.user.profile.factory`; staff often has broader access in converter v2 paths. Do not widen or narrow this without explicit confirmation.
- Do not invent permission decorators or entity mixins that do not exist in Seamstream. The repo uses Django `LoginRequiredMixin`, `login_required`, DRF `IsAuthenticated`, per-action `permission_classes`, and direct factory/profile scoping.
- Protect read endpoints as carefully as writes when they expose factory-owned documents, tech packs, operation cards, subscriptions, credits, or setup data.
- For model changes, generate migrations with `python manage.py makemigrations`; do not hand-write routine schema migrations. Custom data migrations/backfills are allowed only when product or production correctness requires them and must use the correct DB alias when relevant.
- Do not add production data population, default rows, seed commands, or fallback behavior unless the request explicitly requires it. Use local/test data for local verification gaps.

## Product Data And Workflows

- Treat tech-pack import and processing as a core flow. Relevant code includes `apps/converter/v2/views.py`, `apps/converter/v2/api/views.py`, `apps/converter/v2/api/serializers.py`, `apps/converter/business_layer/`, `apps/converter/v2/business_layer/`, `templates/wizard*/`, `templates/complete_poc_user_new.html`, and `static/js/complete_poc_2.js`.
- Treat Operation Breakdown state carefully. `OperationCard`, `OperationBook`, `OperationBookVersion`, `OperationBreakdownVersion`, autosave, rollback, restore, lock/protect flags, `current_snapshot`, and `current_version` must stay consistent.
- Preserve optimistic version checks, row-level diff behavior, autosave retention, lock behavior, restore provenance, and retry-on-version-collision logic unless the task explicitly changes them.
- For factory setup, inspect `apps/factory/models.py`, `apps/factory/api/views.py`, `templates/factory/`, and `static/js/factory_setup/`. Preserve `request.user.profile.factory` scoping.
- For subscriptions and credits, inspect `apps/subscription/business_layer.py`, `apps/subscription/api/views.py`, `apps/subscription/models.py`, and subscription templates. Do not create/cancel real Stripe subscriptions or sessions unless explicitly requested and the environment is confirmed safe.
- For messaging, inspect `apps/messaging/business_layer/email_backend.py` and templates before changing SendGrid/email behavior. Do not send real email during verification unless explicitly requested.
- For flash costing, inspect `apps/flash_costing/api/views.py`, `apps/flash_costing/services/`, `templates/flash_costing/`, `schema-data/`, and `resources/`; it has its own schema/config/testing/document review flow.

## LLM, Cache, Scheduler, And External Services

- Treat LLM calls as expensive external operations. Avoid live OpenAI/Gemini calls in tests or verification unless the user explicitly wants live integration verification and keys/environment are safe.
- Preserve `apps/converter/business_layer/llm_cache.py` semantics: DB-specific cache via `get_current_db()`, `Settings.disable_llm_caching`, JSON response validation before caching, OpenAI/Gemini normalization, and `process_id` / `operation_name` metadata handling.
- Preserve scheduler duplicate-start protection in `apps/converter/business_layer/scheduler.py`; scheduler startup is gated by `ENABLE_SCHEDULER=true` in `apps/converter/apps.py`.
- Do not start background scheduler work during routine verification unless scheduler behavior is the target or `make run` is intentionally used.
- Do not log secrets, API keys, signed S3 URLs, Stripe IDs beyond what is already product-visible, or full LLM payloads containing uploaded document content unless needed for a local debug trace.
- Treat Slack logging configuration and webhooks as sensitive. Do not add or expose new webhook URLs.

## Storage And Files

- Storage behavior is controlled by `USE_S3_BACKEND`, `S3_STATIC`, and `seamstream_ai/storage_backend.py`.
- `PrivateMediaStorage`, `PublicMediaStorage`, and `LocalMediaStorage` are used by tech packs, selected images, archetypes, brand logos, and related media. Preserve private/public distinction.
- For file replacement or cleanup, save the replacement before deleting the old file and keep the model pointer valid if storage operations fail.
- For PDF/image flows, inspect PyMuPDF/Pillow usage, selected image serializers, `TechPackFile`, `TechPackSelectedImage`, and flash-costing upload/page routes before changing storage assumptions.

## UI And Template Rules

- Match nearby Seamstream UI. The main shell uses Tailwind CDN, Lucide CDN, Font Awesome, custom toast CSS, `static/css/tokens.css`, and local classes such as `.btn`, `.btn-primary`, `.badge`, `.card`, `bg-primary`, and `text-primary`.
- Treat the current product UI as the design system. Inspect comparable screens before changing templates, CSS, JS-rendered markup, forms, tables, cards, tabs, modals, badges, empty/loading/error states, or responsive layouts.
- Reuse existing color variables, palette, semantic states, spacing, border radius, typography, table/form/button/modal/tab/card/badge styles, toast patterns, loading and error treatments, and mobile/desktop behavior.
- Reuse existing UI libraries, helpers, icon patterns, and JavaScript patterns. Do not add a new UI library, CSS framework, icon set, font, palette, animation library, bundler, or one-off visual system unless the user explicitly requires it.
- Use Lucide icons with `<i data-lucide="..."></i>` in areas already using Lucide and refresh icons after dynamic insertion with `lucide.createIcons()` or `window.lucide?.createIcons?.()`.
- Preserve Font Awesome usage in the main navigation unless the task explicitly changes that shell.
- Prefer Django `{% url %}` tags and template-provided `data-*` URL attributes for new template-driven API paths. When editing legacy JS that already has hardcoded `/api/...` or `/factory/api/...` paths, keep changes scoped instead of broad URL rewrites.
- Escape or sanitize user-controlled values before inserting them into HTML, attributes, tooltips, `data-*`, modals, toasts, or generated downloads.
- Preserve existing event handlers, active DOM paths, onboarding markers, setup modals, import/wizard tabs, toast behavior, disabled/loading states, and copy unless the task explicitly changes them.
- Preserve accessibility: labels, focus states, keyboard access, contrast, readable validation/error messages, non-overlapping text, and stable layouts across mobile and desktop widths.
- Preserve saved state, not just display state: form values, tabs, filters, selections, loading/error state, session/local storage, and refresh behavior.
- For UI changes, verify desktop and relevant narrow/mobile widths when feasible. Capture before/after screenshots for visible changes when local state can be opened.

## Review And Handoff

- At the end of implementation, inspect `git diff --stat`, `git diff --name-only`, `git diff --check`, and the focused diff.
- For UI/product-visible changes, run real-user QA through the product when feasible. Use Browser for localhost UI verification when available.
- Include screenshot evidence for visible changes whenever local setup/data permits; if blocked, state the exact blocker.
- In handoff, explain PM-facing outcome first, then the technical path through files/functions/classes/templates and validation.
- For bug fixes, technical notes should follow the app flow: user action, template/static JS, API request, backend validation/business logic, persistence/storage/external service, response, and final UI state.
