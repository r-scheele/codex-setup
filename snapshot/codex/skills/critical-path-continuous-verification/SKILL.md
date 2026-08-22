---
name: critical-path-continuous-verification
description: "Use when implementing, fixing, reviewing, or declaring completion for Critical Path / critical-path-dj work that must be verified against the real codebase. Applies requirement-by-requirement verification with Critical Path-specific gates for permissions, workflow behavior, API contracts, Odoo read-only sync/webhooks, migrations, UI/screenshots, branch hygiene, and no duplicate or orphaned implementation."
---

# Critical Path Continuous Verification

Use this with `critical-path-guidelines`. Verify the requested Critical Path change exists in the active code path before, during, and after implementation.

## Baseline Audit

Before editing:

1. Read the request, linked review comment, spreadsheet row, screenshot, transcript, or spec.
2. Classify tenant scope as ASOS-only, TechnoSport-only, or shared from the request and active code flags. Identify the target and non-target role behavior for both brand and factory before editing.
3. Identify every synchronized user-facing surface or API entry point that should reflect the change, and define how their persisted/two-way state will be checked.
4. Break it into atomic requirements and classify each as `COMPLETE`, `PARTIAL`, `MISSING`, or `INCORRECT`.
5. Search the repo for existing routes, views/actions, serializers, services/business logic, permissions, templates, JS handlers, migrations, tests, management commands, and Odoo sync/webhook paths that already cover each item.
6. Run `/graphify .` from the repo root for feature development. If blocked, report the blocker and continue with `rg`, `git grep`, and focused file reads.
7. Define the verification path for each requirement before changing code.

Do not add or update automated tests for Critical Path. Use existing checks, reference searches, diff review, and real product/API/browser verification.

## Pre-Edit Gate

Before modifying a file, answer from code evidence:

- Does the requested behavior already exist in another active path?
- Is there a closest local implementation to mirror?
- Would this change alter permissions, roles, workflow state, API scope, serializer/service boundaries, failure semantics, or business rules?
- Would this remove, hide, shadow, bypass, or orphan existing UI/API/model/JS/workflow behavior?

If any business or permission decision is not explicit, inspect the smallest relevant code path first, then ask a targeted question if the code does not answer it.

## Critical Path-Specific Checks

Verify these when relevant:

- Permissions: use existing Django permissions and entity permission helpers; protect reads as carefully as writes.
- DRF: keep serializers focused on validation/translation, use view/service workflow code, preserve mixin hooks, and convert Django validation errors at the API boundary.
- Odoo: treat Odoo as read-only. Mirror closest webhook/sync registration and processing patterns; verify model IDs, field IDs, domains, parent relations, `fields_save`, `fields_extra`, grouping, delete semantics, and related pull/sync commands.
- Migrations: verify schema need, numbering, dependency on latest target-base migration, branch-local consolidation, and no production permission/reference/default-row seeding unless explicitly required.
- UI: inspect nearby templates, CSS/theme, JS, DaisyUI/local components, icons, copy, empty/loading/error states, saved state, and responsive behavior before changing UI.
- Risky removals: run reference checks for deleted or renamed symbols and report whether each removed surface is preserved, intentionally removed, or blocked.

## During Implementation

After every meaningful change:

1. Re-check the current requirement against the active code path.
2. Confirm imports, URLs/router registration, permissions, serializers, templates, JS event handlers, migration dependencies, and changed symbols are wired.
3. Search for duplicate renderers/functions/actions/URL names and shadowed old paths.
4. Run the smallest useful command or manual check available for the changed surface.
5. Fix verification failures before moving on.

## Product Verification

For UI or product-visible work:

1. Capture before screenshots when the state can be opened.
2. Start the app only as needed and verify through the same UI/API path a real user would use.
3. Prefer the in-app Browser for localhost UI verification when available.
4. Check role/session, copy, disabled/loading/error states, layout, console/runtime errors where accessible, and persisted/rendered final state.
5. Verify both brand and factory behavior, including that an explicitly scoped feature is absent or unchanged for the non-target role.
6. Verify matching state from every synchronized surface identified in the baseline audit.
7. Capture matching full-page after screenshots and compare for accidental removals or layout shifts.

If screenshots or real-user QA are blocked, state the exact blocker.

## Final Completion Gate

Before saying the task is done:

1. Re-read the original request and compare every atomic requirement against the implementation.
2. Search for duplicate implementation, stale code, TODOs/placeholders/mocks, broken references, orphaned handlers, missing registrations, and risky removals.
3. Inspect `git diff --stat`, `git diff --name-only`, `git diff --check`, and the focused diff.
4. Verify no unrelated changes were introduced and no AI/tool branding appears in code or git-facing text.
5. Report changed files, verification performed, blockers, and any deliberate skips.

Completion is based on verified behavior, not code volume.
