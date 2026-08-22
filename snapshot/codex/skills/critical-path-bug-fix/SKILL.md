---
name: critical-path-bug-fix
description: Use when fixing a bug in Critical Path / critical-path-dj, including UI/design-system regressions, especially when a bug report, screenshot, recording, log, error trace, PR comment, review thread, customer report, or reproduction path is provided, or when the prompt includes `$critical-path-bug-fix`.
---

# Critical Path Bug Fix

Use this skill to turn a Critical Path bug report into a minimal, verified fix.

## Required Sub-Skill

Use `$critical-path-guidelines` whenever available. It contains the repo-specific rules and overrides this guide if there is a conflict.

Read `AGENTS.md` first and follow it strictly.

Treat the user's pasted bug description and any attached evidence as the source of truth. If no bug description is pasted, stop and ask the user to paste the bug report before touching code.

## Inputs To Use

Primary inputs:
- The pasted bug description in the user's message.
- Any attached screenshots, mockups, recordings, logs, console errors, network errors, stack traces, spreadsheets, or images.
- Any linked ticket, PR comment, review thread, customer report, or document explicitly included by the user.

Project references:
- `$critical-path-guidelines`
- `AGENTS.md`
- Nearby existing code paths related to the bug, especially `apps/base/`, `apps/bom/`, `apps/users/`, `apps/templates/`, `apps/static/js/`, and relevant serializers, views, business helpers, selectors, models, templates, and JS modules.

## Bug Triage Before Editing

Before changing code, extract and state:
- Actual behavior: what is broken.
- Expected behavior: what should happen instead.
- Affected user/workflow: brand, factory, admin, superuser, API caller, Odoo sync, BOM/order sheet/costing/stage flow, etc.
- Tenant and role scope: whether it affects ASOS, TechnoSport, or both, and the expected brand/factory behavior.
- Synchronized surfaces: every UI/API entry point expected to share the fixed state, including whether changes must propagate in both directions.
- Reproduction path: exact page/action/API/request/data state needed to trigger the issue.
- Suspected code path: files/functions/templates/handlers likely involved, based on evidence and local inspection.
- Scope: the smallest fix that addresses the bug.
- Non-goals: anything not required to fix the bug.
- Blockers/questions: ask only when missing information changes product behavior, permissions, data model, API scope, or workflow ownership.

Do not start by guessing a fix. First inspect the relevant local code path and identify why the bug can happen.

If the report is vague, infer only safe debugging steps and inspect likely code paths. If the expected behavior is unclear after inspection, ask a targeted question before changing product behavior.

## How To Use Attached Evidence

When screenshots/images are attached:
- Inspect every image before coding.
- Treat visible broken UI, copy, layout, missing controls, error states, table shape, button placement, and status values as bug evidence.
- Compare image evidence with the live/local code path that renders the affected UI.
- If the image shows a desired fixed state, match it only where it does not conflict with existing project UI conventions.
- If image evidence conflicts with the pasted description or existing platform behavior, stop and surface the conflict before implementing the conflicting part.

When logs/errors are attached:
- Trace the failing call stack or request path before editing.
- Identify whether the error is frontend, backend, permission, data-shape, missing local data, migration, Odoo, or integration related.
- Fix the root cause, not just the visible exception, unless a safe defensive guard is the explicit bug fix.

## Scope Rules

Fix only the reported bug.

Allowed only when directly required by the bug fix:
- Small template, JavaScript, API/view, serializer, business, selector, model, or migration changes.
- Small UI adjustments that restore the intended existing behavior.
- Defensive validation/error handling when the bug is caused by invalid state or request data.
- Generated migrations only when the root cause requires a schema change.

Do not:
- Refactor unrelated code.
- Rewrite working features.
- Modify unrelated screens or workflows.
- Install libraries or introduce new UI/icon/CSS/JS frameworks.
- Change setup/config/tooling files unless the bug is explicitly in setup/config/tooling.
- Add speculative abstractions, feature flags, future-proofing, or broad fallback behavior.
- Add or update automated tests unless explicitly requested.
- Change permissions, roles, API contracts, workflow semantics, Odoo behavior, or production seed data unless the bug fix explicitly requires it and the behavior is confirmed.
- Hide missing essential business/integration data with fallback defaults unless product explicitly wants that behavior.

## Debugging Rules

- Reproduce the bug locally when possible before fixing it.
- If full reproduction is blocked, state the blocker and use the closest safe verification path.
- Find the root cause before editing.
- Check for equivalent occurrences in the same touched flow; fix equivalent cases that share the same root cause and are in scope.
- Preserve existing behavior and payload semantics outside the broken path.
- For UI bugs, fix the broken path without restyling unrelated surfaces.
- Treat new colors, mismatched buttons/cards/tabs/forms, inaccessible contrast, broken focus states, mobile overlap, and unapproved UI libraries as design-system regressions to fix or flag.
- If the bug appears after a recent change, compare against the nearest working local pattern or target branch behavior before editing.
- If a fix would remove or make unreachable an existing control, field, endpoint, handler, or workflow path, stop and confirm unless removal is explicitly required.

## Implementation Rules

General:
- Reuse the closest existing implementation as the default pattern.
- Keep the diff surgical and minimal.
- Prefer one precise root-cause fix over layered workarounds.
- Do not clean up adjacent code while fixing the bug.

UI/templates:
- Before UI work, inspect comparable screens, nearby templates, CSS/theme files, static JS modules, and active component patterns.
- Preserve existing design principles, CSS variables/classes, color semantics, spacing, border radius, typography, tables, forms, buttons, modals, tabs, cards, badges, empty/loading/error states, accessibility, and responsive behavior.
- Reuse existing UI libraries, helpers, icon patterns, and JavaScript patterns. Do not introduce new libraries, frameworks, fonts, palettes, icon sets, animation libraries, bundlers, or one-off visual systems unless explicitly required.
- Use Tailwind utility classes and DaisyUI components/utilities.
- Use Lucide icons with `<i data-lucide="..."></i>` and refresh icons after dynamic insertion.
- Match existing button classes, colors, sizes, spacing, disabled states, empty states, hover/focus states, copy style, and toast/error feedback.
- Never hardcode internal endpoints in templates; use Django `{% url %}` tags.
- Do not rename labels, headings, columns, tooltips, or buttons unless the bug is specifically wrong copy.

JavaScript:
- Reuse existing shared helpers/modules before adding new functions.
- Avoid duplicate logic between brand/factory flows.
- Prefer targeted DOM updates over full table/page re-renders.
- Escape or sanitize user-controlled values before inserting them into HTML, attributes, tooltips, `data-*` attributes, or modal bodies.
- Preserve existing event handlers and active DOM paths.
- If the bug is a stale UI state, update only the affected state/cache/DOM path and verify adjacent actions still work.

Backend/API:
- Backend validation comes first; frontend validation mirrors it only for UX.
- Keep workflow/business side effects out of serializers.
- Put multi-step workflow logic in `business/` when the project pattern calls for it.
- Use DRF `Response` for DRF JSON responses.
- Use `serializer.is_valid(raise_exception=True)` for DRF writes.
- Convert Django `ValidationError` to DRF `serializers.ValidationError` at API boundaries.
- Keep response contracts resource-oriented and consistent with existing APIs.
- Do not silently drop request fields or change API field scope unless that is the confirmed bug fix.
- Keep defensive handling around secondary processing unless the secondary failure is intended to fail the primary request.

Permissions:
- Use existing entity mixins and permission helpers.
- Prefer one business permission per mutation endpoint.
- Protect read endpoints with correct entity scoping, not authentication alone.
- Do not widen or narrow access unless the bug is explicitly a permission bug and the correct behavior is confirmed.

Migrations/data:
- Never hand-write Django migrations. Use `uv run python manage.py makemigrations` if schema changes are required.
- Do not add production seed/default/population changes unless the bug fix explicitly requires it.
- For missing local verification data, adjust only local/test data or report the blocker.

Odoo:
- Treat Odoo as read-only during implementation and verification.
- Mirror existing Odoo sync/webhook patterns exactly unless the bug fix explicitly requires a confirmed deviation.
- Validate Odoo/source-data assumptions before changing hardcoded names, filters, model IDs, field IDs, or webhook behavior.

## Validation Requirements

Use the bug report as the validation target.

Run the smallest meaningful verification for the touched area:
- Re-run the exact reproduction path and confirm the bug no longer occurs.
- Verify the expected user-visible state or API response.
- Confirm adjacent behavior in the same workflow still works.
- Run `uv run python manage.py makemigrations --check` when models/migrations may be affected.
- Run a focused existing pytest command only when relevant or requested.
- Run lint/pre-commit only when a commit is requested or the touched files make it necessary.

For UI-visible bugs:
- Capture a before screenshot when the broken local state can be opened.
- Capture a matching after screenshot from the same affected area after the fix.
- Use full-page screenshots by default.
- If screenshots are blocked by local data, permissions, credentials, app startup, or missing state, report the exact blocker.
- Compare before/after for accidental removals, layout shifts, missing buttons, changed labels, and inconsistent spacing.
- Verify both brand and factory behavior, or confirm that an explicitly role-scoped fix leaves the non-target role unchanged.
- Verify every synchronized surface identified during triage and its persisted/two-way state where relevant.
- Verify the fix did not introduce an unapproved UI library, CSS framework, palette, font, icon set, animation library, bundler, or visual language.

For API/backend bugs:
- Verify the failing request or closest safe equivalent.
- Confirm error responses are structured and useful when applicable.
- Confirm success responses preserve the existing contract.

## Stop Conditions

Stop when:
- The reported bug is fixed for the intended user role(s), or a concrete blocker is reached.
- The reproduction path passes or the closest safe verification has been run.
- Existing affected workflows still work.
- The final diff contains only files needed for the bug fix.
- Every changed hunk maps back to the bug report, attached evidence, or root cause.

## Final Response Format

Respond in this order:

1. PM summary
   - What was broken.
   - What was fixed.
   - Why it matters to users/workflow.
   - What behavior is intentionally unchanged.

2. How to verify manually
   - Reproduction steps before the fix.
   - Expected result after the fix.
   - Include the local app URL/path when known.

3. Validation run
   - Commands/checks run and results.
   - Screenshot evidence or screenshot blocker for UI bugs.
   - Reproduction result.

4. Technical notes
   - Root cause.
   - Files changed.
   - Key functions/classes/templates touched.
   - Any migrations generated.
   - For critical-path bugs, convert the technical summary into claim-by-claim notes. Start with the plain-language claim, then list the exact code paths and line numbers that make that claim true. Example: "Centralizes costing JSON parsing" followed by clickable links to the shared parser/export and each caller that uses it.
   - Keep the claims in the same order the app runs: server/context data, template output, frontend initialization, event handler, API request, backend validation/persistence, response/UI state.

5. Risks, assumptions, and blockers
   - List anything not verified, deferred, or requiring product confirmation.
