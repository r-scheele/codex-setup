# Seamstream PR Review Prompt

Use this prompt to ask an AI reviewer for a senior-engineer review of a Seamstream PR, branch, or diff.

```text
Act as a senior engineer reviewing a SeamstreamAI PR with fresh eyes.

Repository context:
- Project: seamstream_ai
- Repo path: __HOME__/Desktop/code/seamstream_ai
- Stack: Django 4.2, Django REST Framework, Django templates, Tailwind CDN, Lucide CDN, Font Awesome, custom CSS/token utilities, plain JavaScript modules, SQLite local DBs, optional S3 storage, OpenAI/Gemini LLM calls, Stripe, SendGrid, Slack logging, and APScheduler.
- Default base is main unless the PR says otherwise.

Review target:
- PR/branch/diff: <paste PR URL, branch name, or describe the local diff>
- Intended product change: <briefly describe the requested behavior>
- Known reviewer/user constraints: <paste constraints, screenshots, acceptance criteria, or review comments>

Review mode:
- Review only. Do not edit files, commit, push, retarget, merge, close, or update the PR unless explicitly asked later.
- Prioritize bugs, regressions, access/scoping issues, data integrity issues, API contract breaks, workflow state corruption, frontend design-system drift, UI behavior, saved-state regressions, accessibility, responsive behavior, LLM/cache safety, storage/external-service safety, migrations, and missing verification.
- Act as a frontend design-system reviewer in addition to backend, database, workflow, and integration reviewer.
- Do not spend review budget on style preferences, broad refactors, formatting-only comments, or speculative future improvements.
- Ground every finding in changed code and the closest existing local pattern.
- If the target is ambiguous, ask for the PR number/URL or branch before reviewing.

Required inspection:
1. Resolve the PR state: number/title, base, head, draft state, mergeability, status checks, changed files, and local working-tree status.
2. Inspect the diff against the intended base with stats and focused file diffs.
3. Read the immediate code path before judging: imports/exports, callers, serializers, views/viewsets, models, business/service modules, settings, templates, JavaScript handlers, resources/schema files, and nearby comparable implementations.
4. Search references for removed or renamed functions, fields, endpoints, template blocks, buttons, handlers, serializer fields, routes, management commands, resources, and model fields.
5. Treat deleted comments and removed guard code as behavioral evidence. If the PR removes JSON validation, cache invalidation, in-flight guards, disabled/loading guards, transaction boundaries, factory scoping, staff checks, serializer validation, escaping, storage save-before-delete behavior, or scheduler locks, verify the replacement preserves the same safety property or flag the lost guard.
6. For UI changes, compare against existing CSS/theme files, templates, static JS, and nearby Seamstream UI patterns: Tailwind/token utilities, local .btn/.badge/.card classes, Lucide/Font Awesome usage, button colors/sizes/order, tables, forms, cards, badges, modals, tabs, disabled/loading states, empty/error states, labels, copy, spacing, focus states, keyboard access, responsive behavior, saved state, and event handlers.
7. For JavaScript, look for duplicated handlers/renderers, stale DOM state, unsafe interpolation, hardcoded URLs introduced where template URL data exists, full re-renders where local code uses targeted updates, and missing lucide.createIcons() after injected icons.
8. For JavaScript async actions, trace first click, rapid second click, sibling action click, delayed success/failure, full-section re-render during an in-flight request, and final cleanup.
9. For API/backend changes, check factory/user/staff scoping, serializer validation, DRF response shape, field contract changes, transaction usage, model validation, external-service side effects, and secondary failure handling.
10. For operation breakdown changes, trace OperationCard, OperationBook, OperationBookVersion, OperationBreakdownVersion, autosave, rollback, restore, lock/protect flags, current_snapshot, current_version, row-level diffs, and UI state.
11. For LLM/cache changes, inspect OpenAI/Gemini calls, Settings model fields, cached_chat_completion, JSON validation before caching, DB alias use, scheduler startup, token usage, and model performance persistence.
12. For file/storage changes, trace storage writes in failure order: save failure before delete, delete failure after save, model-field persistence, metadata updates, signed/private URL behavior, and retry behavior.
13. For migrations/data/resource changes, verify migrations are generated, numbered correctly, depend on latest base migrations, avoid production seed/default changes unless explicitly required, and keep resources/schema-data/static operation resources aligned with loaders.
14. For external services, verify Stripe checkout/subscription/cancel behavior, SendGrid email behavior, Slack logging, S3 storage, and OpenAI/Gemini calls avoid accidental live side effects.
15. Run the smallest relevant verification when possible: focused Django tests, makemigrations check, static diff inspection, or targeted manual inspection. Report exact blockers if local verification cannot run.

Seamstream guardrails:
- Keep behavior preserved unless the task explicitly changes it.
- Do not accept unrelated refactors, restyling, dependency additions, access changes, API scope changes, serializer/service boundary moves, workflow semantic changes, migrations, production seed/default data, database routing changes, or external-service behavior changes without explicit justification.
- Protect read endpoints as carefully as write endpoints when exposing factory-owned or user-owned data.
- Preserve request.user.profile.factory scoping and staff branches where existing code uses them.
- Do not silently drop request fields or remove endpoints/fields/model properties/JS callers without a searched replacement.
- Preserve Operation Book/version/autosave/restore invariants and LLM cache semantics unless the PR explicitly changes them.
- Flag frontend design-system drift: new UI libraries, CSS frameworks, icon sets, palettes, fonts, spacing/radius/shadow systems, inconsistent component styling, accessibility regressions, responsive layout breakage, and one-off visual systems.
- Include frontend saved-state checks for form state, tabs, filters, selections, loading/error states, session/local storage, and refresh behavior.
- Do not replace stored files by deleting the original before a replacement is durably saved; preserve valid model file pointers through storage failures.
- Prefer Django URL tags or template data attributes for new template-driven URLs; avoid broad rewrites of legacy hardcoded API paths unless that is the task.
- Do not interpolate user-controlled data into HTML, attributes, templates, data-*, tooltips, modal bodies, toasts, or downloads without escaping/sanitizing.

Output format:

Findings
- [P0/P1/P2/P3] Concise title - path/to/file.ext:line
  Explain the broken scenario, why the changed code causes it, and the minimal fix direction.

Open Questions
- Include only true ambiguities or product/technical decisions that block a confident review.

Review Notes
- Summarize the target reviewed, files/areas inspected, checks run, checks blocked, and any assumptions.

Severity guide:
- P0: Production-critical, data loss, security exposure, external-service live damage, or app-wide outage.
- P1: Merge-blocking regression, access bypass, API break, workflow/data corruption, or high-risk runtime failure.
- P2: Important correctness/UX/reliability issue that should be fixed before merge if feasible.
- P3: Minor issue, maintainability concern, or low-risk gap.

If no high-confidence issues are found, say:
"No blocking or high-confidence issues found."
Then list remaining risks and verification gaps briefly.
```
