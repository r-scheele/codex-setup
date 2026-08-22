---
name: seamstream-continuous-verification
description: "Use when implementing, fixing, reviewing, or declaring completion for Seamstream / SeamstreamAI / __HOME__/Desktop/code/seamstream_ai work that must be verified against real app behavior. Applies requirement-by-requirement verification with Seamstream-specific gates for Django/DRF/templates, tenant/domain database routing, factory scoping, tech-pack import, operation breakdown, subscriptions, flash costing, LLM/cache, scheduler, storage, UI, and external-service safety."
---

# Seamstream Continuous Verification

Use this with `seamstream-guidelines`. Verify each requested Seamstream requirement against the local code and the relevant tenant/domain flow before declaring completion.

## Baseline Audit

Before editing:

1. Parse the request into atomic requirements and classify each as `COMPLETE`, `PARTIAL`, `MISSING`, or `INCORRECT`.
2. Check branch and dirty state with `git status --short --branch`.
3. Search relevant Seamstream paths before assuming anything is missing: `seamstream_ai/`, `apps/accounts/`, `apps/converter/`, `apps/converter/v2/`, `apps/factory/`, `apps/flash_costing/`, `apps/subscription/`, `apps/messaging/`, `templates/`, `static/js/`, `static/css/`, `resources/`, `schema-data/`, and tests.
4. Run `/graphify .` from the repo root for feature development. If blocked, report the blocker and continue with `rg`, `git grep`, and focused reads.
5. Define one verification path per requirement.

Do not import patterns from other repos. Seamstream uses its own direct factory/profile scoping, response shapes, database routing, and plain Python/Django command style.

## Pre-Edit Gate

Before modifying a file, answer from code evidence:

- Does this behavior already exist in a URL/view/viewset, serializer, business layer, model, template, JS file, setting, test, or resource file?
- Which tenant/domain database does the path use: default/app, `tal`, or `technosport`?
- Does the change affect factory scoping, staff behavior, API contract shape, serializer/service boundaries, DB routing, migrations/data population, Stripe/SendGrid/S3, LLM/cache, scheduler behavior, failure semantics, or product rules?
- Could the change remove, shadow, or orphan a current UI control, API action, model field, template block, JS handler, scheduler behavior, cache behavior, or storage path?

Ask only when the code and user request do not answer a material product or technical decision.

## Seamstream-Specific Checks

Verify these when relevant:

- Django/API: preserve local response envelopes. Converter v2 APIs use `APIResponseOk` / `APIResponseFail`; other apps may use different shapes.
- Scope: preserve `request.user.profile.factory` and existing staff broader-access behavior unless explicitly changed.
- Database routing: verify host/domain or DB context when code touches tenant data; do not assume `default`.
- Business logic: use existing modules in `apps/converter/business_layer/`, `apps/converter/v2/business_layer/`, `apps/subscription/business_layer.py`, `apps/accounts/business_layer.py`, or `apps/flash_costing/services/` when they already own the workflow.
- Operation Breakdown: preserve version checks, autosave, rollback/restore, locks, snapshots, and retry-on-version-collision behavior.
- LLM/cache: avoid live OpenAI/Gemini calls unless explicitly requested; preserve DB-specific cache and JSON validation semantics.
- Scheduler: do not start background scheduler work unless scheduler behavior is the target.
- Storage/files: preserve private/public storage distinctions and save replacements before deleting old files.
- External services: do not create Stripe sessions/subscriptions, send real email, or expose webhooks/secrets unless explicitly requested and safe.
- UI: match Tailwind/Lucide/Font Awesome/custom token patterns; preserve event handlers, DOM paths, onboarding markers, toasts, saved state, and accessibility.

## During Implementation

After every meaningful change:

1. Re-check the current requirement in the active URL/API/template/JS/business path.
2. Confirm imports, routes, serializers, settings, DB alias/domain behavior, migrations, template data attributes, JS handlers, and storage paths are wired.
3. Search changed symbols and removed names with `rg` or `git grep`.
4. Run the smallest useful focused command, such as `python manage.py test ...`, `python manage.py makemigrations --check --dry-run`, or a targeted browser/API path when feasible.
5. Fix verification failures before moving to the next requirement.

## Product Verification

For UI or product-visible work:

1. Verify through the product path a real user would use.
2. Use the correct domain/tenant setup for app, TAL, or Technosport flows.
3. Check desktop and relevant narrow/mobile widths when feasible.
4. Capture before/after screenshots when local state can be opened.
5. Report exact blockers for missing credentials, data, permissions, app startup, or unreachable state.

## Final Completion Gate

Before saying the task is done:

1. Re-read the original request and verify every atomic requirement as `YES`, `NO`, or `PARTIAL` internally.
2. Search for duplicate logic, stale code, TODOs/placeholders/mocks, broken imports, missing routes, missing migrations, orphan handlers, and unintended removals.
3. Inspect `git diff --stat`, `git diff --name-only`, `git diff --check`, and the focused diff.
4. Confirm no unrelated changes, secrets, or AI/tool branding were introduced.
5. Report product outcome, technical path, verification, blockers, and deliberate skips.

Completion is based on verified behavior in the real Seamstream flow.
