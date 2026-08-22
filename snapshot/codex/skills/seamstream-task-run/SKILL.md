---
name: seamstream-task-run
description: "Use when implementing SeamstreamAI work in __HOME__/Desktop/code/seamstream_ai, including features, bug fixes, UI/frontend changes, frontend design-system consistency, Django/DRF changes, migrations, review fixes, tech-pack import, operation breakdown, BOM, SMV, factory setup, subscriptions, flash costing, LLM/cache, or database-routing tasks."
---

# Seamstream Task Run

Run Seamstream work as a production-safe delivery loop: clarify product behavior, inspect the actual local path, make the smallest code change, verify, and report in business language before technical detail.

## Required Sub-Skill

Use `$seamstream-guidelines` whenever available. It contains the repo-specific rules and overrides this guide if there is a conflict.

If `__HOME__/Desktop/code/seamstream_ai/AGENTS.md` exists, read it before editing. At creation time, this repo did not contain `AGENTS.md`.

## Workflow

1. **Intake**
   - Translate the request into objective, user/workflow impact, exact behavior change, and what must not change.
   - If the request contains meeting notes, screenshots, review text, logs, or documents, extract only actionable requirements.
   - Ask before changing factory access/scoping, staff behavior, API contracts, serializer/service boundaries, migrations/data population, database routing, LLM/cache behavior, scheduler behavior, Stripe/SendGrid/S3 behavior, or unclear business rules.

2. **Repository Orientation**
   - Work in `__HOME__/Desktop/code/seamstream_ai` unless the user gives another Seamstream checkout.
   - Check `git status --short --branch` before edits.
   - Default base is `main` unless the PR or user says otherwise.
   - If the worktree is dirty with unrelated changes, preserve them and report any conflict with the task.

3. **Implementation Discipline**
   - Reuse existing views, viewsets, serializers, business-layer modules, templates, static JS modules, CSS tokens, tests, and data/resource patterns first.
   - For UI work, inspect comparable screens, nearby templates, `static/css/` theme/token files, static JS helpers, and existing saved-state behavior before editing.
   - Preserve existing design principles, CSS variables/classes, color semantics, component patterns, JavaScript helpers, accessibility, and responsive behavior.
   - Keep the diff minimal. Do not rename, reformat, remove, or reshape working logic unless required.
   - Use plain repo commands: `python manage.py ...` and `make ...`; do not use `uv`.
   - Never hand-write routine Django schema migrations; use `python manage.py makemigrations`.
   - Keep tenant/domain DB behavior in mind: local branch-specific DBs exist for `default`, `tal`, and `technosport`.

4. **Verification**
   - Run the smallest meaningful checks first; expand only if risk justifies it.
   - For model changes, run `python manage.py makemigrations --check --dry-run`.
   - For focused tests, use Django's test runner, for example `python manage.py test tests.apps.converter.business_layer`.
   - For UI changes, start the app when needed with `python manage.py runserver` or `make run` only when scheduler behavior is relevant, then verify the page/API path as a real user.
   - Before handoff for UI work, verify no unapproved UI library, CSS framework, palette, font, icon set, animation library, bundler, or one-off visual language was introduced.
   - Review `git diff --stat`, `git diff --name-only`, `git diff --check`, and the full focused diff for scope drift.

## Common Seamstream Risk Areas

- Tech-pack upload and selected-image handling across `TechPackFile`, `TechPackSelectedImage`, import views, and wizard templates.
- Operation Breakdown persistence across `OperationCard`, `OperationBook`, `OperationBookVersion`, autosave, restore, rollback, and locked/protected state.
- LLM calls, model settings, response parsing, JSON validation, token usage, and LLM cache behavior.
- Factory-scoped setup data for products, machines, production lines, operation preferences, finishing methods, and archetypes.
- Subscription/credit mutations that touch Stripe sessions, active subscriptions, credits, coupons, or free/pro/standard/enterprise behavior.
- Domain-routed databases and `.using(...)` paths.
- Static JS buildstamp/versioned import references in wizard/minimized flows.

## Final Response

Use this order:

- what changed
- why it changed, in PM/business language
- how to verify quickly, including the local URL/path when known
- validation run and results
- technical notes only where helpful
- risks, assumptions, or blockers

## Common Mistakes

| Mistake | Fix |
|---|---|
| Assuming another repo's conventions apply | Inspect Seamstream code and use Seamstream paths, commands, and libraries. |
| Starting from `dev` by habit | Use `main` unless the user or PR says otherwise. |
| Running `make full_setup` for a tiny check | Prefer a focused `manage.py` command. |
| Bypassing factory scoping | Preserve `request.user.profile.factory` and staff branches where they exist. |
| Treating a UI change as a blank canvas | Match the current Seamstream design system, approved libraries, accessibility behavior, and saved state. |
| Live-calling Stripe, SendGrid, OpenAI, Gemini, or S3 during routine verification | Mock, statically inspect, or verify locally unless live integration is explicitly requested and safe. |
