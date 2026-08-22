---
name: seamstream-new-feature
description: "Use when implementing a new feature in SeamstreamAI / seamstream_ai, especially when a feature request, screenshot, mockup, diagram, spreadsheet, linked ticket, PR comment, review thread, product document, UI/frontend change, or frontend design-system judgment is provided, or when the prompt includes `$seamstream-new-feature`."
---

# Seamstream New Feature

Use this skill to turn a Seamstream feature request into a minimal, verified implementation.

## Required Sub-Skill

Use `$seamstream-guidelines` whenever available. It contains the repo-specific rules and overrides this guide if there is a conflict.

If `__HOME__/Desktop/code/seamstream_ai/AGENTS.md` exists, read it first. At creation time, Seamstream had no `AGENTS.md`.

Treat the user's pasted feature description and any attached images/files as the feature source of truth. If no feature description is pasted, stop and ask the user to paste the feature request before touching code.

## Inputs To Use

Primary inputs:
- The pasted feature description in the user's message.
- Any attached screenshots, mockups, diagrams, spreadsheets, PDFs, logs, recordings, or images.
- Any linked ticket, PR comment, review thread, customer report, or document explicitly included by the user.

Project references:
- `$seamstream-guidelines`
- Nearby existing code paths related to the feature, especially `apps/accounts/`, `apps/converter/`, `apps/converter/v2/`, `apps/factory/`, `apps/flash_costing/`, `apps/subscription/`, `apps/messaging/`, `templates/`, `static/js/`, `static/css/`, `resources/`, `schema-data/`, and relevant serializers, views, viewsets, business-layer helpers, models, templates, and JS modules.
- For UI work, comparable Seamstream screens are primary references. Inspect nearby templates, `static/css/` theme/token files, static JS helpers, and existing component/state patterns before editing.

## How To Interpret The Feature Description

Before editing code, extract and state:
- Objective: what user/workflow outcome this feature should create.
- In scope: exact screens, endpoints, buttons, states, fields, workflows, resources, or data behavior requested.
- Out of scope: anything mentioned only as background or future work.
- Assumptions: only safe assumptions that do not change factory access, staff behavior, API contracts, database routing, workflow semantics, LLM/cache behavior, storage/external-service behavior, or business rules.
- Blockers/questions: only ask if the missing answer would change product behavior, permissions/access, data model, API scope, external service behavior, or workflow ownership.

If the pasted description is messy, conversational, or copied from a meeting, extract only actionable product requirements. Ignore chatter.

If the feature description and images conflict, stop and surface the conflict before implementing the conflicting part.

## How To Use Attached Images And Files

When images/screenshots/mockups are attached:
- Inspect every image before coding.
- Treat visible UI details as requirements when clearly intentional: wording, labels, section order, table shape, button placement, empty states, loading states, validation states, and error states.
- Match Seamstream's existing UI conventions: Tailwind CDN classes, `static/css/tokens.css` utilities, local button/badge/card classes, Lucide where already used, Font Awesome where already used, existing modal/toast patterns, and nearby spacing/copy.
- Do not introduce DaisyUI, React, Vue, or a new visual system just because the mockup looks different.
- If the image implies confusing UX or conflicts with existing Seamstream behavior, pause and recommend the platform-consistent alternative.

When spreadsheets, PDFs, or JSON resources are attached:
- Determine whether they are product input, expected output, schema/config, or reference data.
- Compare them with existing `resources/`, `schema-data/`, `static/operation_resources/`, model fields, and serializers before adding new files or columns.
- Do not add production data population or defaults unless the feature explicitly requires it.

## Scope Rules

Implement only the pasted feature request.

Allowed only when directly required by the feature:
- New or changed Django templates, partials, or local components.
- New or changed static JavaScript in existing Seamstream style.
- New or changed API/view/viewset/serializer/business-layer code.
- New or changed model fields and generated migrations.
- New navigation, actions, buttons, persistence, resources, or schema files required for the feature to work.

Do not:
- Refactor unrelated code.
- Rewrite working features.
- Modify unrelated screens or workflows.
- Install libraries or introduce new UI/icon/CSS/JS frameworks.
- Change setup/config/tooling files unless the feature explicitly requires it.
- Add speculative abstractions, feature flags, future-proofing, or fallback behavior.
- Add broad automated tests by default. Add focused tests only when requested or when the repo's existing test pattern clearly covers the touched behavior.
- Change factory access, staff access, API contracts, database routing, LLM/cache behavior, scheduler behavior, Stripe/SendGrid/S3 behavior, or production seed/data population unless explicitly required and confirmed.

## Implementation Rules

General:
- Reuse the closest existing implementation as the default pattern.
- Keep the diff surgical and minimal.
- Preserve existing behavior and payload semantics unless the feature explicitly changes them.
- If a change removes or makes unreachable an existing control, field, endpoint, handler, workflow path, scheduler path, cache behavior, or storage path, stop and confirm unless the feature explicitly requires removal.

UI/templates:
- Use Tailwind utility classes and existing Seamstream token/component classes.
- Preserve existing design principles, CSS variables/classes, color semantics, spacing, border radius, typography, component patterns, JavaScript helpers, accessibility, and responsive behavior.
- Use Lucide icons with `<i data-lucide="..."></i>` and refresh icons after dynamic insertion in areas that already use Lucide.
- Preserve Font Awesome usage in existing shell/navigation areas.
- Match existing button classes, colors, sizes, spacing, disabled states, empty states, loading states, hover/focus states, copy style, modal behavior, and toast/error feedback.
- Prefer Django `{% url %}` tags and template `data-*` URL attributes for new template-driven URLs.
- Do not rename labels, headings, columns, tooltips, buttons, or onboarding text unless the feature requires it.
- Preserve saved UI state for forms, tabs, filters, selections, loading/error states, session/local storage, and refresh behavior when the feature touches those paths.

JavaScript:
- Reuse existing shared modules/helpers before adding new functions.
- Avoid duplicating logic between import, minimized wizard, operation cards, factory setup, library, and flash-costing flows.
- Prefer targeted DOM/state updates over full page or full section re-renders unless the nearby module already re-renders that way.
- Escape or sanitize user-controlled values before inserting them into HTML, attributes, tooltips, `data-*`, modals, toasts, or downloads.
- Preserve existing event handlers, active DOM paths, loading/disabled states, and `lucide.createIcons()` refresh paths.

Backend/API:
- Backend validation comes first; frontend validation mirrors it only for UX.
- Keep multi-step workflow behavior in local business/service modules when present.
- Use DRF `Response` for DRF JSON responses.
- Use `APIResponseOk` / `APIResponseFail` only in v2 converter paths that already use that envelope.
- Use `serializer.is_valid(raise_exception=True)` for DRF writes when serializers are used.
- Keep response contracts consistent with the touched endpoint's current API shape.
- Do not silently drop request fields or change field scope unless that is the confirmed feature behavior.

Access/scoping:
- Use existing `LoginRequiredMixin`, `login_required`, DRF permissions, `request.user.profile.factory`, and `request.user.is_staff` patterns.
- Protect read endpoints with correct factory/user scoping, not authentication alone, when data is factory-owned or user-owned.
- Do not add non-existent permission helpers or new access architecture unless explicitly required.

Migrations/data/resources:
- Never hand-write routine Django schema migrations. Use `python manage.py makemigrations`.
- Run `python manage.py makemigrations --check --dry-run` when models may be affected.
- Do not add production seed/default/population changes unless the feature explicitly requires it.
- Keep `resources/`, `schema-data/`, `static/operation_resources/`, and model-backed prompt/settings data aligned with the existing loader/management-command paths.

External services:
- Do not trigger live Stripe, SendGrid, OpenAI, Gemini, Slack, or S3 write behavior during routine implementation/verification unless explicitly requested and environment safety is confirmed.
- Preserve LLM cache, scheduler, and model-setting behavior unless the feature explicitly changes them.

## Validation Requirements

Run the smallest meaningful verification for the touched area.

Choose from:
- Static inspection of the exact changed path.
- Focused manual UI/API verification.
- `python manage.py makemigrations --check --dry-run` when models/migrations may be affected.
- Focused Django tests such as `python manage.py test tests.apps.converter.business_layer` only when relevant or requested.
- Pre-commit only when a commit is requested or the touched files make it necessary.

For UI-visible changes:
- Capture before and after full-page screenshots when the local state can be opened.
- If screenshots are blocked by local data, credentials, app startup, permissions, or missing state, report the exact blocker.
- Compare before/after for accidental removals, layout shifts, missing buttons, changed labels, broken icons, and inconsistent spacing.
- Before handoff, verify no unapproved UI library, CSS framework, palette, font, icon set, animation library, bundler, or one-off visual language was introduced.

## Stop Conditions

Stop when:
- The pasted feature works end to end for the intended user role(s), or a concrete blocker is reached.
- Existing affected workflows still work.
- The final diff contains only files needed for the feature.
- Every changed hunk maps back to the pasted feature description or attached artifact.

## Final Response Format

Respond in this order:

1. PM summary
   - What changed.
   - Why it matters to users/workflow.
   - What behavior is intentionally unchanged.

2. How to test manually
   - Step-by-step instructions a non-engineer can follow.
   - Include the local app URL/path when known.

3. Validation run
   - Commands/checks run and results.
   - Screenshot evidence or screenshot blocker for UI changes.

4. Technical notes
   - Files changed.
   - Key functions/classes/templates touched.
   - Any migrations generated.

5. Risks, assumptions, and blockers
   - List anything not verified, deferred, or requiring product confirmation.
