---
name: critical-path-pr-review
description: Use when reviewing any Critical Path PR, branch, local diff, GitHub PR URL/number, or requested "fresh eye" review in critical-path-dj. Produces senior-engineer and frontend design-system findings focused on regressions, scope drift, permissions, workflow semantics, API contracts, UI/design consistency, Odoo sync safety, migrations, and verification gaps without making code changes unless explicitly asked.
---

# Critical Path PR Review

## Overview

Review Critical Path changes as a senior engineer and frontend design-system reviewer: inspect the actual diff and nearby product patterns, prioritize concrete defects over style preferences, and report findings first with file/line references. This is a review-only workflow unless the user explicitly asks for fixes.

For a copyable long-form prompt, read `references/review_prompt.md`.

## Review Contract

- Do not edit files, commit, push, retarget, merge, close, or update the PR during review unless explicitly asked.
- Treat the PR branch or user-provided diff as the review target; do not review unrelated local branches.
- If the target PR/branch is ambiguous, ask for the PR number/URL or branch before reviewing.
- Findings must be specific, reproducible, and grounded in changed code plus the closest existing local pattern.
- Avoid speculative issues. If something is only a question or risk, label it as such instead of presenting it as a defect.
- Do not request automated tests as a default Critical Path review nit; only flag missing verification when risk is real and no focused check/manual path was shown.

## Workflow

1. Resolve the review target.
   - Prefer an explicit PR URL/number, branch name, or supplied diff.
   - For "current PR," inspect local branch and `gh pr status/view`.
   - Record base branch, head branch, PR number/title when available, draft state, mergeability, and checks.

2. Inspect the diff.
   - Fetch before comparing remote refs when using GitHub/local branches.
   - Use `git diff --stat`, `git diff --name-status`, and focused diffs against the PR base.
   - Categorize touched areas: backend/API, permissions, serializers, business logic, templates/UI, JavaScript, migrations, Odoo sync, data/defaults, tests/checks.
   - Check every changed file against the stated PR/task scope. Treat unrelated styling, copy, formatting, imports, dependency/config edits, permission changes, migrations, or behavior changes as review risks unless the PR explicitly requires them.
   - For deleted comments or removed guard code, read the removed code as behavioral evidence. If the PR removes serialization, debounce/throttle, disabled/loading guards, mutex/in-flight state, transaction boundaries, permission checks, validation, escaping, cache invalidation, or "do not run in parallel" comments, verify the replacement preserves the same safety property or flag the lost guard.

3. Read the immediate code path.
   - Inspect changed functions plus imports/exports, callers, serializers/views, templates, JS handlers, permissions, models, selectors/business modules, and nearby comparable implementations.
   - For removals/renames, search references to ensure the old path is intentionally replaced.
   - For Odoo changes, inspect the closest pull/sync command, webhook registration, processor, helper filters, and brand `extra` config.
   - For frontend changes that preserve or mutate form controls, trace at least one full user journey from initial render through event handlers, DOM value changes, in-memory state updates, recalculation/rendering, and save payload. Compare the payload before and after the PR, especially for empty/default/fallback values.
   - For frontend async actions, trace contention explicitly: first click, rapid second click, sibling action click, delayed success/failure, full-section re-render during an in-flight request, and final cleanup. Confirm live DOM state, module state, and API requests stay consistent after nodes are replaced. If one action is split into multiple buttons or multiple controls hit the same endpoint/resource, verify there is a shared in-flight guard that blocks duplicate or parallel writes and that re-rendered controls preserve disabled/loading state.
   - Act as a frontend design-system reviewer in addition to backend/database reviewer for frontend changes.
   - For frontend changes, compare against existing CSS/theme files, templates, static JS modules, and comparable screens in the same product area.
   - Verify the PR matches existing design conventions: Tailwind/DaisyUI classes, CSS variables, palette, semantic state colors, button colors/sizes/order, spacing, border radius, shadow, typography, table/cell styling, forms, modals, tabs, cards, badges, empty/loading/error/disabled states, Lucide icon usage, labels, responsive behavior, and interaction feedback.
   - Flag design-system drift: new UI libraries, CSS frameworks, icon sets, palettes, fonts, spacing/radius/shadow systems, inconsistent component styling, accessibility regressions, and responsive layout breakage.
   - Include frontend saved-state checks for form state, tabs, filters, selections, loading/error states, session/local storage, refresh behavior, and save payloads.
   - Verify the PR uses the same libraries, modules, helpers, and patterns already present in the project. Flag new dependencies, alternate UI/icon/CSS/JS libraries, duplicated helper logic, or hand-rolled behavior when an existing local helper/module should be reused.
   - Check for reusable existing code before accepting new implementation code. Search for equivalent behavior in shared JS modules, nearby templates, serializers, selectors, business services, and comparable brand/factory flows; flag duplication when it creates two sources of truth.
   - Trace existing individual behaviors that share the touched path and confirm they remain intact, including adjacent role branches, existing event handlers, disabled/locked states, save payloads, response shapes, labels, navigation, and error/toast behavior.
   - For file/storage changes, especially backfills or commands that replace existing stored files, trace storage writes in failure order: save failure before delete, delete failure after save, model-field persistence, metadata updates, and retry behavior. Flag delete-before-save replacement paths that can leave database rows pointing at missing files.
   - For serializer/view caps, limits, filtering, or deduplication, compare the write-side accepted state against the read-side returned state. Exercise all source variants and fallback fields involved in the flow, such as stored file, URL, base64, matching related record, non-matching related record, empty value, and maximum-count boundary.

4. Review against Critical Path risk categories.
    - Scope drift: unrelated refactors, styling churn, labels/copy changes, formatting/import churn, behavior changes, dependency/config additions, migrations, or files not needed for the review/task.
   - Tenant/role/synchronization scope: ASOS-only, TechnoSport-only, or shared behavior; both brand and factory paths; and every UI/API surface that should show the same persisted state.
    - Permission/entity scoping: read and write endpoints, brand/factory/superuser behavior, UI flags versus API checks.
   - API/serializer contracts: response shape, write validation, dropped fields, raw JSON responses, swallowed validation errors.
   - Read/write count consistency: if an upload/write path accepts N related records, verify list/detail serializers and UI payloads can still return N records for every supported source/fallback state, unless the product explicitly wants a smaller display cap.
   - Workflow semantics: stage done/skip behavior, role-specific locks, Activity history, side effects, status transitions.
   - Frontend safety and reuse: duplicated handlers/renderers, unreachable controls, unsafe HTML interpolation, stale DOM state, URL hardcoding, missing Lucide refresh after injected icons, duplicated helpers, or new JS patterns where an existing shared module should be used.
   - Frontend async/race safety: duplicate submissions, missing in-flight guards, parallel requests against the same order/resource, per-button disabled state that leaves sibling controls enabled, detached DOM nodes after `$container.html(...)` or `replaceWith(...)`, stale `.finally()` cleanup on replaced nodes, and loading/error states that disappear during re-render.
   - Stateful UI drift: default display values becoming persisted overrides, placeholders versus real input values, stale in-memory data after DOM-only changes, form state, tabs, filters, selections, loading/error states, session/local storage, refresh behavior, save payload changes caused by UI-only fixes, and multi-step interactions such as add row -> select parent -> select child -> change child -> save.
   - UI/design consistency: DaisyUI/Tailwind/local component patterns, CSS variables, palette, semantic state colors, button semantics, icon library choice, table/cell styling, forms, modals, tabs, cards, badges, spacing, border radius, shadow, typography, hover/focus/disabled/empty/loading/error states, accessibility, responsive layout, toast/modal feedback, and preserved labels/copy.
   - Behavior preservation: existing individual user actions, role-specific branches, event handlers, active DOM paths, API payloads, response contracts, workflow locks, and adjacent equivalent flows still behave as before unless the PR explicitly changes them.
   - Data/model/migration safety: generated migrations, numbering/dependencies, redundant workflow fields, seed/default/backfill risk.
   - File and storage data safety: save-before-delete semantics, storage exception handling, model file pointer validity, metadata consistency, cleanup of replacement files after partial failure, and idempotent retry behavior for backfills.
   - Odoo/TechnoSport safety: read-only assumptions, static config preservation, webhook field/save/extra/delete scoping, no runtime writes.
   - Performance: Python-side aggregation over large querysets, repeated full re-renders where local patterns use incremental updates.
   - Verification: focused checks or manual paths appropriate to the blast radius.

5. Validate only as needed.
   - Prefer focused static checks and targeted commands relevant to changed files.
   - For file/storage replacement changes, when feasible, run or sketch a failure-path check where replacement save fails and confirm the original file remains available and the model still points at a valid file.
   - For serializer/view count or filtering changes, when feasible, run or sketch a matrix check across the supported source variants and max-count boundary so accepted records are not silently hidden on read.
   - For JavaScript async action changes, when feasible, run or sketch a focused delayed-request check that exercises rapid repeat clicks, sibling clicks, delayed resolve/reject, and re-render while in flight. If you cannot run it locally, report the exact unverified race path instead of saying the UI was only statically inspected.
   - Do not make local data, migration, or product behavior changes just to verify.
   - If a check is blocked by local environment, report the exact blocker and what still passed.

## Finding Standards

Lead with findings. Order by severity. Each finding should include:

- Severity: `[P0]` production-critical, `[P1]` merge-blocking/high, `[P2]` important, `[P3]` minor.
- File and line reference from the PR head/diff.
- The concrete broken scenario or regression.
- Why the changed code causes it, with the closest existing pattern when useful.
- A minimal fix direction, not a full patch unless asked.

Do not list non-issues to fill space. If there are no findings, say so clearly and mention residual risk or unrun checks.

## Output Shape

Use this structure:

```markdown
Findings
- [P1] Title - path/to/file.ext:123
  Explanation of the failing scenario, changed-code cause, and minimal fix direction.

Open Questions
- Only include real decisions or ambiguities.

Review Notes
- Target reviewed, base/head, checks run, checks blocked, and any repository or GitHub tooling blockers.
```

If there are no findings:

```markdown
Findings
- No blocking or high-confidence issues found.

Review Notes
- Target reviewed, checks run, and remaining risk.
```

## Reviewer Prompt

When the user asks for a prompt rather than an actual review, provide or adapt `references/review_prompt.md`. Keep the prompt general enough to work on any Critical Path PR and specific enough to enforce project rules.
