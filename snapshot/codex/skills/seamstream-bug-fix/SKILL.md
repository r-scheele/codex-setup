---
name: seamstream-bug-fix
description: "Use when fixing a bug in SeamstreamAI / seamstream_ai, especially when a bug report, screenshot, recording, log, error trace, PR comment, review thread, customer report, reproduction path, UI/design-system regression, tech-pack issue, OB/BOM/SMV issue, factory setup issue, subscription/credit issue, flash-costing issue, or LLM/cache issue is provided, or when the prompt includes `$seamstream-bug-fix`."
---

# Seamstream Bug Fix

Use this skill to turn a Seamstream bug report into a minimal, verified fix.

## Required Sub-Skill

Use `$seamstream-guidelines` whenever available. It contains the repo-specific rules and overrides this guide if there is a conflict.

If `__HOME__/Desktop/code/seamstream_ai/AGENTS.md` exists, read it first. At creation time, Seamstream had no `AGENTS.md`.

Treat the user's pasted bug description and any attached evidence as the source of truth. If no bug description is pasted, stop and ask the user to paste the bug report before touching code.

## Inputs To Use

Primary inputs:
- The pasted bug description in the user's message.
- Any attached screenshots, mockups, recordings, logs, console errors, network errors, stack traces, spreadsheets, PDFs, JSON, or images.
- Any linked ticket, PR comment, review thread, customer report, or document explicitly included by the user.

Project references:
- `$seamstream-guidelines`
- Nearby existing code paths related to the bug, especially `apps/accounts/`, `apps/converter/`, `apps/converter/v2/`, `apps/factory/`, `apps/flash_costing/`, `apps/subscription/`, `apps/messaging/`, `templates/`, `static/js/`, `static/css/`, `resources/`, `schema-data/`, and relevant serializers, views, viewsets, business-layer helpers, models, templates, and JS modules.
- For UI bugs, inspect comparable screens, nearby templates, `static/css/` theme/token files, static JS helpers, and existing saved-state patterns before editing.

## Bug Triage Before Editing

Before changing code, extract and state:
- Actual behavior: what is broken.
- Expected behavior: what should happen instead.
- Affected user/workflow: factory admin, invited user, staff/admin, API caller, tech-pack import, minimized wizard, operation breakdown, BOM, SMV, factory setup, subscription/credits, flash costing, LLM/cache, scheduler, storage, or domain-routed tenant DB.
- Reproduction path: exact page/action/API/request/data state/domain host needed to trigger the issue.
- Suspected code path: files/functions/templates/handlers likely involved, based on evidence and local inspection.
- Scope: the smallest fix that addresses the bug.
- Non-goals: anything not required to fix the bug.
- Blockers/questions: ask only when missing information changes product behavior, access/scoping, data model, API scope, external service behavior, database routing, or workflow ownership.

Do not start by guessing a fix. First inspect the relevant local code path and identify why the bug can happen.

If the report is vague, infer only safe debugging steps and inspect likely code paths. If expected behavior is unclear after inspection, ask a targeted question before changing product behavior.

## How To Use Attached Evidence

When screenshots/images are attached:
- Inspect every image before coding.
- Treat visible broken UI, copy, layout, missing controls, error states, table shape, button placement, status values, icons, disabled/loading state, and toast/modal feedback as bug evidence.
- Compare image evidence with the live/local code path that renders the affected UI.
- If the image shows a desired fixed state, match it only where it does not conflict with existing Seamstream UI conventions.
- If image evidence conflicts with the pasted description or existing product behavior, stop and surface the conflict before implementing the conflicting part.

When logs/errors are attached:
- Trace the failing call stack or request path before editing.
- Identify whether the error is frontend, backend, serializer/data-shape, access/scoping, domain DB routing, migration/schema, missing local data, LLM/cache, scheduler, storage/S3, Stripe, SendGrid, or flash-costing related.
- Fix the root cause, not just the visible exception, unless a safe defensive guard is the explicit bug fix.

## Scope Rules

Fix only the reported bug.

Allowed only when directly required by the bug fix:
- Small template, JavaScript, API/view/viewset, serializer, business/service, model, migration, resource/schema, or settings changes.
- Small UI adjustments that restore intended existing behavior.
- Defensive validation/error handling when the bug is caused by invalid state or request data.
- Generated migrations only when the root cause requires a schema change.

Do not:
- Refactor unrelated code.
- Rewrite working features.
- Modify unrelated screens or workflows.
- Install libraries or introduce new UI/icon/CSS/JS frameworks.
- Change setup/config/tooling files unless the bug is explicitly in setup/config/tooling.
- Add speculative abstractions, feature flags, future-proofing, or broad fallback behavior.
- Add broad automated tests by default. Add focused tests only when requested or when the existing test pattern directly covers the touched bug.
- Change factory access, staff access, API contracts, database routing, workflow semantics, LLM/cache behavior, scheduler behavior, Stripe/SendGrid/S3 behavior, or production seed/data population unless the bug fix explicitly requires it and the behavior is confirmed.
- Hide missing essential business/integration data with fallback defaults unless product explicitly wants that behavior.

## Debugging Rules

- Reproduce the bug locally when possible before fixing it.
- If full reproduction is blocked, state the blocker and use the closest safe verification path.
- Find the root cause before editing.
- Check for equivalent occurrences in the same touched flow; fix equivalent cases that share the same root cause and are in scope.
- Preserve existing behavior and payload semantics outside the broken path.
- For UI bugs, fix the broken path without restyling unrelated surfaces.
- Treat new colors, mismatched buttons/cards/tabs/forms, inaccessible contrast, broken focus states, mobile overlap, and unapproved UI libraries, CSS frameworks, icon sets, fonts, palettes, animation libraries, bundlers, or one-off visual systems as design-system regressions.
- If the bug appears after a recent change, compare against the nearest working local pattern or target branch behavior before editing.
- If a fix would remove or make unreachable an existing control, field, endpoint, handler, workflow path, scheduler path, cache path, or storage path, stop and confirm unless removal is explicitly required.

## Implementation Rules

General:
- Reuse the closest existing implementation as the default pattern.
- Keep the diff surgical and minimal.
- Prefer one precise root-cause fix over layered workarounds.
- Do not clean up adjacent code while fixing the bug.

UI/templates:
- Use Tailwind utility classes and existing Seamstream token/component classes.
- Preserve existing design principles, CSS variables/classes, color semantics, component patterns, JavaScript helpers, accessibility, and responsive behavior.
- Use Lucide icons and refresh icons after dynamic insertion only in areas already using Lucide.
- Preserve Font Awesome usage in shell/navigation areas.
- Match existing button classes, colors, sizes, spacing, disabled states, empty states, loading states, hover/focus states, copy style, modal behavior, and toast/error feedback.
- Prefer Django `{% url %}` tags and template `data-*` URL attributes for new template-driven URLs.
- Do not rename labels, headings, columns, tooltips, or buttons unless the bug is specifically wrong copy.
- Preserve saved UI state for forms, tabs, filters, selections, loading/error states, session/local storage, and refresh behavior when the broken path touches them.

JavaScript:
- Reuse existing shared helpers/modules before adding new functions.
- Avoid duplicate logic between import, minimized wizard, operation cards, factory setup, library, and flash-costing flows.
- Prefer targeted DOM/state updates over full page or full section re-renders unless the nearby module already re-renders that way.
- Escape or sanitize user-controlled values before inserting them into HTML, attributes, tooltips, `data-*`, modal bodies, toasts, or downloads.
- Preserve existing event handlers and active DOM paths.
- If the bug is stale UI state, update only the affected state/cache/DOM path and verify adjacent actions still work.

Backend/API:
- Backend validation comes first; frontend validation mirrors it only for UX.
- Keep workflow/business side effects out of serializers unless the local serializer already owns that behavior.
- Put multi-step workflow logic in existing business/service modules when the project pattern calls for it.
- Use DRF `Response` for DRF JSON responses.
- Use `APIResponseOk` / `APIResponseFail` only in v2 converter paths that already use that envelope.
- Use `serializer.is_valid(raise_exception=True)` for DRF writes when serializers are used.
- Keep response contracts consistent with existing APIs.
- Do not silently drop request fields or change API field scope unless that is the confirmed bug fix.
- Keep defensive handling around secondary processing unless the secondary failure is intended to fail the primary request.

Access/scoping:
- Use existing `LoginRequiredMixin`, `login_required`, DRF permissions, `request.user.profile.factory`, and `request.user.is_staff` patterns.
- Protect read endpoints with correct factory/user scoping, not authentication alone, when data is factory-owned or user-owned.
- Do not widen or narrow access unless the bug is explicitly an access bug and correct behavior is confirmed.

Migrations/data:
- Never hand-write routine Django schema migrations. Use `python manage.py makemigrations` if schema changes are required.
- Do not add production seed/default/population changes unless the bug fix explicitly requires it.
- For missing local verification data, adjust only local/test data or report the blocker.

External services:
- Do not live-call or mutate Stripe, SendGrid, OpenAI, Gemini, Slack, or S3 during routine verification unless explicitly requested and environment safety is confirmed.
- Preserve LLM cache, scheduler, and model-setting behavior unless the bug is in that path.

## Validation Requirements

Use the bug report as the validation target.

Run the smallest meaningful verification for the touched area:
- Re-run the exact reproduction path and confirm the bug no longer occurs.
- Verify the expected user-visible state or API response.
- Confirm adjacent behavior in the same workflow still works.
- Run `python manage.py makemigrations --check --dry-run` when models/migrations may be affected.
- Run a focused Django test command only when relevant or requested.
- Run lint/pre-commit only when a commit is requested or the touched files make it necessary.

For UI-visible bugs:
- Capture a before screenshot when the broken local state can be opened.
- Capture a matching after screenshot from the same affected area after the fix.
- Use full-page screenshots by default.
- If screenshots are blocked by local data, credentials, app startup, permissions, or missing state, report the exact blocker.
- Compare before/after for accidental removals, layout shifts, missing buttons, changed labels, broken icons, and inconsistent spacing.
- Before handoff, verify the fix did not introduce unapproved UI libraries, palettes, fonts, icon sets, frameworks, or visual language.

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
   - Convert the technical summary into claim-by-claim notes. Start with the plain-language claim, then list exact code paths and line numbers that make the claim true.
   - Keep claims in the same order the app runs: server/context data, template output, frontend initialization, event handler, API request, backend validation/business logic, persistence/storage/external service, response/UI state.

5. Risks, assumptions, and blockers
   - List anything not verified, deferred, or requiring product confirmation.
