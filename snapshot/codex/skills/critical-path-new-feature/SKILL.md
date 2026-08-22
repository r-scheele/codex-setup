---
name: critical-path-new-feature
description: Use when implementing a new feature in Critical Path / critical-path-dj, including frontend/UI changes that must preserve the existing design system, especially when a feature request, screenshot, mockup, diagram, spreadsheet, linked ticket, PR comment, review thread, or product document is provided, or when the prompt includes `$critical-path-new-feature`.
---

# Critical Path New Feature

Use this skill to turn a Critical Path feature request into a minimal, verified implementation.

## Required Sub-Skill

Use `$critical-path-guidelines` whenever available. It contains the repo-specific rules and overrides this guide if there is a conflict.

Read `AGENTS.md` first and follow it strictly.

Treat the user's pasted feature description and any attached images as the feature source of truth. If no feature description is pasted, stop and ask the user to paste the feature request before touching code.

## Inputs To Use

Primary inputs:
- The pasted feature description in the user's message.
- Any attached screenshots, mockups, diagrams, spreadsheets, or images.
- Any linked ticket, PR comment, review thread, or document explicitly included by the user.

Project references:
- `$critical-path-guidelines`
- `AGENTS.md`
- Nearby existing code paths related to the feature, especially `apps/base/`, `apps/bom/`, `apps/users/`, `apps/templates/`, `apps/static/js/`, and relevant serializers, views, business helpers, selectors, models, templates, and JS modules.

## How To Interpret The Feature Description

Before editing code, extract and state:
- Objective: what user/workflow outcome this feature should create.
- In scope: exact screens, endpoints, buttons, states, fields, workflows, or data behavior requested.
- Tenant and role scope: whether it is ASOS-only, TechnoSport-only, or shared, plus the expected brand and factory behavior.
- Synchronized surfaces: every place the changed state must appear, including whether changes must propagate in both directions.
- Out of scope: anything mentioned only as background or future work.
- Assumptions: only safe assumptions that do not change permissions, API contracts, workflow semantics, or business rules.
- Blockers/questions: only ask if the missing answer would change product behavior, permissions, data model, API scope, or workflow ownership.

If the pasted description is messy, conversational, or copied from a meeting, extract only actionable product requirements. Ignore chatter.

If the feature description and images conflict, stop and surface the conflict before implementing the conflicting part.

## How To Use Attached Images

When images are attached:
- Inspect every image before coding.
- Treat visible UI details as requirements when they are clearly intentional: wording, labels, section order, table shape, button placement, empty states, and status/error states.
- Match the project's existing UI conventions even when implementing the image: Tailwind utilities, DaisyUI components, Lucide icons, existing button/color semantics, spacing, modals, badges, tabs, dropdowns, toasts, and loading states.
- Do not introduce a new visual system just because the mockup looks different.
- If the image implies a confusing UX or conflicts with existing platform behavior, pause and recommend the platform-consistent alternative.
- For screenshots of existing bugs, identify the broken state and inspect the live code path that renders it before changing anything.

## Scope Rules

Implement only the pasted feature request.

Allowed only when directly required by the feature:
- New or changed templates/components.
- New or changed JavaScript in existing project style.
- New or changed API/view/serializer/business/selector code.
- New or changed model fields and generated migrations.
- New navigation, actions, buttons, or persistence required for the feature to work.

Do not:
- Refactor unrelated code.
- Rewrite working features.
- Modify unrelated screens or workflows.
- Install libraries or introduce new UI/icon/CSS/JS frameworks.
- Change setup/config/tooling files unless the feature explicitly requires it.
- Add speculative abstractions, flags, future-proofing, or fallback behavior.
- Add or update automated tests unless explicitly requested.
- Change permissions, roles, API contracts, workflow semantics, Odoo behavior, or production seed data unless explicitly required and confirmed.

## Implementation Rules

General:
- Reuse the closest existing implementation as the default pattern.
- Keep the diff surgical and minimal.
- Preserve existing behavior and payload semantics unless the feature explicitly changes them.
- If a change removes or makes unreachable an existing control, field, endpoint, handler, or workflow path, stop and confirm unless the feature explicitly requires removal.

UI/templates:
- Before UI work, inspect comparable screens, nearby templates, CSS/theme files, static JS modules, and active component patterns.
- Preserve existing design principles, CSS variables/classes, color semantics, spacing, border radius, typography, tables, forms, buttons, modals, tabs, cards, badges, empty/loading/error states, accessibility, and responsive behavior.
- Reuse existing UI libraries, helpers, icon patterns, and JavaScript patterns. Do not introduce new libraries, frameworks, fonts, palettes, icon sets, animation libraries, bundlers, or one-off visual systems unless explicitly required.
- Use Tailwind utility classes and DaisyUI components/utilities.
- Use Lucide icons with `<i data-lucide="..."></i>` and refresh icons after dynamic insertion.
- Match existing button classes, colors, sizes, spacing, disabled states, empty states, hover/focus states, copy style, and toast/error feedback.
- Never hardcode internal endpoints in templates; use Django `{% url %}` tags.
- Do not rename labels, headings, columns, tooltips, or buttons unless the feature requires it.

JavaScript:
- Reuse existing shared helpers/modules before adding new functions.
- Avoid duplicate logic between brand/factory flows.
- Prefer targeted DOM updates over full table/page re-renders.
- Escape or sanitize user-controlled values before inserting them into HTML, attributes, tooltips, `data-*` attributes, or modal bodies.
- Preserve existing event handlers and active DOM paths.

Backend/API:
- Backend validation comes first; frontend validation mirrors it only for UX.
- Keep workflow/business side effects out of serializers.
- Put multi-step workflow logic in `business/` when the project pattern calls for it.
- Use DRF `Response` for DRF JSON responses.
- Use `serializer.is_valid(raise_exception=True)` for DRF writes.
- Convert Django `ValidationError` to DRF `serializers.ValidationError` at API boundaries.
- Keep response contracts resource-oriented and consistent with existing APIs.

Permissions:
- Use existing entity mixins and permission helpers.
- Prefer one business permission per mutation endpoint.
- Protect read endpoints with correct entity scoping, not authentication alone.
- Do not widen or narrow access unless explicitly required.

Migrations/data:
- Never hand-write Django migrations. Use `uv run python manage.py makemigrations` if schema changes are required.
- Do not add production seed/default/population changes unless the feature explicitly requires it.
- Do not add fallback defaults that hide missing business data unless product explicitly wants that behavior.

Odoo:
- Treat Odoo as read-only during implementation and verification.
- Mirror existing Odoo sync/webhook patterns exactly unless the feature explicitly requires a confirmed deviation.

## Validation Requirements

Run the smallest meaningful verification for the touched area.

Choose from:
- Static inspection of the exact changed path.
- Focused manual UI/API verification.
- `uv run python manage.py makemigrations --check` when models/migrations may be affected.
- Focused existing pytest command only when relevant or requested.
- Lint/pre-commit only when a commit is requested or the touched files make it necessary.

For UI-visible changes:
- Capture before and after full-page screenshots when the local state can be opened.
- If screenshots are blocked by local data, permissions, credentials, app startup, or missing state, report the exact blocker.
- Compare the before/after visually and check for accidental removals, layout shifts, missing buttons, changed labels, and inconsistent spacing.
- Verify the result as both brand and factory, or verify the explicit role restriction by confirming the non-target role is unchanged.
- Verify every identified synchronized UI surface and its persisted/two-way behavior before handoff.
- Before handoff, verify the diff did not introduce an unapproved UI library, CSS framework, palette, font, icon set, animation library, bundler, or visual language.

## Stop Conditions

Stop when:
- The pasted feature works end to end for the intended user role(s), or a concrete blocker is reached.
- Existing affected workflows still work.
- The final diff contains only files needed for the feature.
- Every changed hunk maps back to the pasted feature description or attached image.

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
