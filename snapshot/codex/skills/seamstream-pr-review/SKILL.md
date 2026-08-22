---
name: seamstream-pr-review
description: "Use when reviewing any SeamstreamAI PR, branch, local diff, GitHub PR URL/number, or requested fresh-eye review in seamstream_ai. Produces senior-engineer findings focused on regressions, scope drift, access/scoping, API contracts, workflow state, frontend design-system drift, UI behavior, saved state, accessibility, responsive behavior, LLM/cache safety, storage/external-service safety, migrations, and verification gaps without making code changes unless explicitly asked."
---

# Seamstream PR Review

Review Seamstream changes as a senior engineer: inspect the actual diff and nearby product patterns, prioritize concrete defects over style preferences, and report findings first with file/line references. This is a review-only workflow unless the user explicitly asks for fixes.

For a copyable long-form prompt, read `references/review_prompt.md`.

## Review Contract

- Do not edit files, commit, push, retarget, merge, close, or update the PR during review unless explicitly asked.
- Treat the PR branch or user-provided diff as the review target; do not review unrelated local branches.
- If the target PR/branch is ambiguous, ask for the PR number/URL or branch before reviewing.
- Findings must be specific, reproducible, and grounded in changed code plus the closest existing Seamstream pattern.
- Act as a frontend design-system reviewer in addition to backend, database, workflow, and integration reviewer.
- Avoid speculative issues. If something is only a question or risk, label it as such instead of presenting it as a defect.
- Do not request automated tests as a default review nit; flag missing verification only when risk is real and no focused check/manual path was shown.

## Workflow

1. Resolve the review target.
   - Prefer an explicit PR URL/number, branch name, or supplied diff.
   - For "current PR," inspect local branch and `gh pr status/view` when available.
   - Record base branch, head branch, PR number/title when available, draft state, mergeability, and checks.
   - Default expected base is `main` unless the PR says otherwise.

2. Inspect the diff.
   - Fetch before comparing remote refs when using GitHub/local branches.
   - Use `git diff --stat`, `git diff --name-status`, and focused diffs against the PR base.
   - Categorize touched areas: accounts/auth/invitations, converter v1/v2 APIs, tech-pack import, operation breakdown/operation books, BOM/SMV, factory setup, flash costing, subscription/credits, messaging/email, settings/domain DB routing, storage/static files, templates/UI, JavaScript, migrations/data/resources, tests/checks.
   - Check every changed file against the stated PR/task scope. Treat unrelated styling, copy, formatting, imports, dependency/config edits, access changes, migrations, data population, or behavior changes as review risks unless the PR explicitly requires them.
   - For deleted comments or removed guard code, read the removed code as behavioral evidence. If the PR removes JSON validation, cache invalidation, in-flight guards, disabled/loading guards, transaction boundaries, factory scoping, staff checks, serializer validation, escaping, storage save-before-delete behavior, or scheduler locks, verify the replacement preserves the same safety property or flag the lost guard.

3. Read the immediate code path.
   - Inspect changed functions plus imports/exports, callers, serializers/views/viewsets, templates, JS handlers, models, business/service modules, settings, resources/schema files, and nearby comparable implementations.
   - For removals/renames, search references to ensure the old path is intentionally replaced.
   - For tech-pack import and wizard changes, trace from `apps/converter/v2/views.py` templates through static JS, `CompleteProcessViewSet`, serializers, selected images, storage, and LLM/business-layer calls.
   - For operation breakdown changes, trace `OperationCard`, `OperationBook`, `OperationBookVersion`, `OperationBreakdownVersion`, autosave, rollback, restore, lock/protect flags, `current_snapshot`, `current_version`, row-level diffing, and front-end operation-card state.
   - For factory setup changes, trace `request.user.profile.factory`, factory setup API actions, `templates/factory/`, and `static/js/factory_setup/`.
   - For subscription/credit changes, trace `SubscriptionService`, `FactoryCreditManager`, coupons, Stripe sessions, active subscription updates, credit mutations, and UI templates.
   - For LLM/cache changes, inspect OpenAI/Gemini call paths, `Settings` model fields, `cached_chat_completion`, JSON validation before caching, DB alias use, scheduler startup, and token/model performance persistence.
   - For UI/template/frontend changes, compare against existing CSS/theme files, templates, static JS, and comparable screens. Verify the PR matches Seamstream conventions: Tailwind/token utilities, local `.btn`/`.badge`/`.card` classes, Lucide/Font Awesome usage, button colors/sizes/order, table/cell styling, forms, modals, tabs, badges, cards, empty/loading/error/disabled states, labels, spacing, focus states, keyboard access, responsive behavior, and interaction feedback.
   - For JavaScript async actions, trace first click, rapid second click, sibling action click, delayed success/failure, re-render during in-flight request, and final cleanup when applicable.
   - For file/storage changes, trace save failure before delete, delete failure after save, model-field persistence, metadata updates, signed/private URL behavior, and retry behavior.

4. Review against Seamstream risk categories.
   - Scope drift: unrelated refactors, styling churn, labels/copy changes, formatting/import churn, behavior changes, dependency/config additions, migrations, resources, or files not needed for the task.
   - Access/scoping: read and write endpoints, factory users, factory admins, invited users, staff/admin behavior, UI flags versus API checks.
   - API/serializer contracts: response shape, write validation, dropped fields, envelope consistency, error response shape, serializer field scope.
   - Workflow state: import process creation, selected images, completion flags, operation cards, operation books, version numbers, autosaves, restore/rollback, locked/protected state, credit deductions, subscription activation/cancellation.
   - Frontend safety and reuse: duplicated handlers/renderers, unreachable controls, unsafe HTML interpolation, stale DOM state, hardcoded URLs introduced where template URL data is available, missing Lucide refresh after injected icons, duplicated helper logic, or new JS patterns where a local module should be reused.
   - UI/design consistency: new UI libraries, CSS frameworks, icon sets, palettes, fonts, spacing/radius/shadow systems, one-off component styling, Tailwind/token utilities, Lucide/Font Awesome choice, button semantics, cards/badges/modals/tabs/forms/toasts, table styling, spacing, hover/focus/disabled/loading/error states, accessibility regressions, responsive layout breakage, and preserved labels/copy.
   - Frontend saved state: form values, tabs, filters, selections, loading/error states, session/local storage, refresh behavior, and state after async success/failure.
   - Data/model/migration safety: generated migrations, numbering/dependencies, branch-local migration chains, custom data migrations, resource/schema synchronization, and seed/default/backfill risk.
   - Multi-database safety: `default`, `tal`, and `technosport` routing, `.using(...)`, `get_current_db()`, `set_current_db()`, and domain host behavior.
   - File/storage data safety: S3/local storage, private/public media, save-before-delete semantics, model file pointer validity, and local/S3 URL assumptions.
   - External services: Stripe checkout/subscription/cancel behavior, SendGrid email behavior, OpenAI/Gemini calls, Slack logging, and accidental live side effects.
   - Performance/reliability: Python-side aggregation over large querysets, repeated full re-renders where local patterns use targeted updates, unbounded LLM/image payloads, scheduler duplicate starts, cache misses, and retry behavior.
   - Verification: focused checks or manual paths appropriate to the blast radius.

5. Validate only as needed.
   - Prefer focused static checks and targeted commands relevant to changed files.
   - For model changes, use `python manage.py makemigrations --check --dry-run` when feasible.
   - For existing focused tests, use Django test runner paths such as `python manage.py test tests.apps.converter.business_layer`.
   - Do not make local data, migration, or product behavior changes just to verify.
   - If a check is blocked by local environment, report the exact blocker and what still passed.

## Finding Standards

Lead with findings. Order by severity. Each finding should include:

- Severity: `[P0]` production-critical, `[P1]` merge-blocking/high, `[P2]` important, `[P3]` minor.
- File and line reference from the PR head/diff.
- The concrete broken scenario or regression.
- Why the changed code causes it, with the closest existing Seamstream pattern when useful.
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

When the user asks for a prompt rather than an actual review, provide or adapt `references/review_prompt.md`. Keep the prompt general enough to work on any Seamstream PR and specific enough to enforce project rules.
