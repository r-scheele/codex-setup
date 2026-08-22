---
name: flash-costing-pr-review
description: Use when reviewing a Flash Costing or flash-costing-public-dj PR, branch, GitHub PR URL, local diff, review request, or fresh-eye review as a senior backend engineer, Python/Django code reviewer, database-design reviewer, and frontend design-system reviewer with at least 10 years of production systems experience. Produces findings first for regressions in Open Costing, Send to Factory, factory costing responses, secure factory portal access, profit, delta, comparison, Django, DRF, templates, static JavaScript, CSS, UI color/design consistency, user ownership, staff schema access, garment schemas, feature groups, SMV, BOM pricing, labour costing, OpenAI pipeline, migrations, data commands, and verification.
---

# Flash Costing PR Review

Review Flash Costing changes as a senior backend engineer, Python/Django code reviewer, database-design reviewer, and frontend design-system reviewer with at least 10 years of experience reviewing production systems. Inspect the actual diff, read nearby product patterns, and report concrete findings first. This is review-only unless the user explicitly asks for fixes.

## Reviewer Stance

- Act like the reviewer who will be accountable if this change corrupts customer data, leaks another user's costing, breaks a Celery retry path, or makes a migration unsafe in production.
- Prioritize correctness over style: data integrity, ownership/access control, transactional safety, idempotency, API compatibility, migration safety, background-task reliability, numerical accuracy, and focused verification.
- Trace production failure modes: concurrent requests, partial saves, stale objects, retries, external API failures, malformed input, expired tokens, missing related rows, and rollback behavior.
- For database/domain changes, inspect whether the model represents the business workflow without unnecessary duplicate domain objects, preserves original versus proposed values, keeps historical revisions traceable, and enforces tenant/organization boundaries.
- For frontend changes, inspect whether the UI preserves the existing design principle, color palette, component patterns, libraries, accessibility, responsiveness, and saved-state behavior.
- Be skeptical of happy-path-only implementations. Verify persistence, permissions, state transitions, and error handling through the actual code path.
- Keep feedback actionable and minimal. Do not request broad rewrites when a smaller production-safe fix addresses the risk.

## Review Contract

- Do not edit files, commit, push, retarget, merge, close, or update the PR unless explicitly asked.
- Resolve the target PR, branch, or diff before reviewing. Ask if ambiguous.
- Findings must be specific, reproducible, and grounded in changed code plus nearby local patterns.
- Prioritize bugs, regressions, access leaks, data integrity issues, transaction/concurrency hazards, API contract breaks, migration risks, workflow/calculation mistakes, LLM/pipeline failure behavior, and missing verification.
- For Open Costing implemented tasks, treat missing or inadequate tests as reviewable because the local rules require tests for every implemented task.
- For other work, do not treat missing new tests as a review finding by default. Flag missing tests only when the user asks for that lens, a review/CI requirement calls for them, or the change is too risky to verify responsibly without one.
- Do not spend review budget on style preferences, broad refactors, or speculative future improvements.

## Open Costing Review Context

For any PR or diff that touches Open Costing, Send to Factory, factory costing responses, comparison, delta, or secure factory portal work:

1. Resolve the Git repository root and obey the active `AGENTS.md` instruction chain.
2. Before reviewing the changed code, read these local files in full when present, resolving paths from the repository root:
   - `docs/_local/open-costing/specification.md`
   - `docs/_local/open-costing/task-sheet.csv`
   - `docs/_local/open-costing/decisions.md`
   - `docs/_local/open-costing/sources.md`
3. Match the PR, branch, review request, or changed behavior to the relevant Open Costing task-sheet phase and row when possible. Read surrounding phase tasks to understand dependencies.
4. Treat `specification.md` as the product source of truth, `decisions.md` as the source of resolved decisions, and `task-sheet.csv` as the implementation breakdown.
5. Use the local Open Costing context as the review baseline. Flag changed code that violates the specification, decisions, task dependencies, or Open Costing rules.
6. Do not edit files during review-only work unless the user explicitly asks for fixes.

## Workflow

1. **Resolve Target**
   - Capture PR URL/number or branch, base, head, title, draft state, mergeability, checks, and local working-tree status when available.
   - Confirm base when unclear. This repo has active `dev` history and CI PRs targeting `main`.

2. **Inspect Diff**
   - Use `git diff --stat`, `git diff --name-status`, and focused file diffs against the intended base.
   - Categorize touched areas: models/migrations, views/API/serializers/forms, selectors/business/services, Celery/LLM pipeline, schema editor, BOM/labour, templates/static JS/CSS, management commands/data, tests, config/CI.
   - Treat unrelated dependency, config, migration, data, style, or formatting changes as scope risks unless justified by the PR.
   - For database or domain-model PRs, inspect relevant project documentation, existing models, new and modified migrations, tests, and repository conventions for IDs, timestamps, enums, foreign keys, indexes, validation, deletion behavior, auditing, and organization boundaries.

3. **Read The Code Path**
   - For costing UI/API changes, trace from URL/template/API view through ownership check, serializer/form, service/business logic, model persistence, response, and existing tests when useful.
   - For backend Python changes, trace validation, queryset scoping, transaction boundaries, model saves, side effects, retries/idempotency, exception paths, and database constraints.
   - For newly added helpers, filters, calculations, services, or JS utilities, search for equivalent existing logic in views, services, selectors, template tags, commands, and static JS. Flag duplication when the branch could reuse the existing path with a smaller diff.
   - For schema changes, trace `FeatureGroup`, `FeatureValue`, `GarmentType`, validation, `save_new_schema_version`, `features_schema` cache rebuild, schema editor JS, and existing version tests when useful.
   - For BOM changes, trace `generate_bom_for_costing`, `bom_pricing`, saved BOM JSON, `row_id`, `prices_by_country`, `price_source`, user edits, country repricing, materialized costs, and `bom_logic.js`.
   - For SMV/labour changes, trace feature frequency semantics, cutting versus sewing/finishing SMV, labour snapshot, user preferences, and UI totals.
   - For Open Costing changes, trace original costing/result immutability, request snapshot creation, factory response proposal persistence, BOM row comparison by stable row ID, added/removed/changed/unchanged row classification, percentage delta safety, profit-in-CPM handling, accept/reject behavior, token scope/expiry, response locking, and reopen behavior.
   - For LLM/pipeline changes, trace task status progression, page/image loading, `pipeline_config.json`, retry wrappers, JSON parsing, failure handling, and existing mocked tests when useful.
   - For frontend changes, trace the real interaction: initial render, data attributes, JSON scripts, event handler, fetch request, CSRF, loading/error state, DOM update, saved payload, and refresh/reload behavior.
   - For frontend design changes, compare against nearby templates, `apps/static/css/project.css`, existing static JS, and comparable screens. Flag unapproved new UI libraries, CSS frameworks, icon sets, palettes, fonts, spacing systems, radius systems, shadow styles, or visual patterns.
   - For removals or renames, search references and ensure the old surface is intentionally replaced.

4. **Frontend Design System Review**
   - Confirm the UI keeps the existing Flash Costing visual language: `fc-*` classes, existing button/card/tab/table/form/modal/status patterns, dark-theme variables, semantic color states, typography, spacing, and responsive behavior.
   - Check that app workflows remain quiet, utilitarian, and task-focused rather than marketing-like, decorative, or visually inconsistent with existing costing screens.
   - Verify accessibility basics: labels, focus states, keyboard-reachable controls, adequate contrast, readable error messages, non-overlapping text, and stable mobile/desktop layouts.
   - Review UI changes for saved-state integrity: BOM JSON, schema JSON, view state, country/quantity selection, form data, session storage, loading/error states, and refresh behavior.

5. **Database And Domain Design Review**
   - Confirm the implementation represents the workflow with the correct original costing, brand/factory participants, proposal records, comments/reasons, submission lifecycle, revisions, and authorization relationships.
   - Check that original values, proposed values, submitted revisions, and previous revisions remain distinguishable and traceable after source records change.
   - Inspect table/model responsibilities, normalization, duplication, foreign keys, referential integrity, cascade/deletion behavior, nullability, defaults, constraints, indexes, data types, decimal precision, timestamps, auditability, and organization isolation.
   - Review migrations for reversibility, dependency ordering, safe defaults, locking risks, destructive changes, production-data assumptions, nullability transitions, missing indexes/constraints, rollback behavior, and database compatibility.
   - Flag schema designs that work on an empty test database but can fail, corrupt history, or become ambiguous against existing production data.

6. **Risk Categories**
   - User ownership or staff-only access bypass.
   - Python/Django runtime errors, swallowed exceptions, missing validation, unsafe defaults, or non-atomic multi-row writes.
   - Transaction, concurrency, retry, or idempotency bugs in requests, Celery tasks, imports, or management commands.
   - Costing status or pipeline order regressions.
   - Schema version/cache drift or invalid feature group references.
   - BOM row identity, price cache, country, `user_edited`, or total-cost regressions.
   - SMV frequency/counting errors.
   - Open Costing original-result mutation, missing request snapshot, proposal persistence errors, incomplete BOM diff classification, division-by-zero delta, profit double-counting, token access leak, expired-token bypass, or submitted response mutation.
   - OpenAI calls bypassing wrappers, unmocked tests, bad JSON parsing, or changed retry/failure semantics.
   - Unsafe `innerHTML`, hardcoded URLs, missing CSRF, lost `json_script`, stale DOM/session storage state, or broken partial update behavior.
   - Frontend design-system drift: new UI library, CSS framework, icon set, palette, font, spacing/radius/shadow system, inconsistent button/card/tab/table/form styling, inaccessible contrast/focus, or mobile/desktop layout breakage.
   - Migration/data command non-idempotency, missing `--dry-run`, or seed/data changes not required by the PR.
   - Missing focused verification for the actual blast radius.
   - New duplicate helpers or calculations when an existing local helper could be reused.

## Finding Standards

Start with a merge recommendation:

- `APPROVE`
- `APPROVE WITH NON-BLOCKING COMMENTS`
- `REQUEST CHANGES`
- `DO NOT MERGE`

Then lead with findings, ordered by severity:

- `BLOCKER` fundamentally incorrect, unsafe to merge, data loss, critical integrity/security issue, or core workflow break.
- `HIGH` significant correctness, authorization, history, migration, or production-reliability problem.
- `MEDIUM` meaningful design, validation, test, performance, or maintainability concern.
- `LOW` minor but actionable inconsistency or improvement.
- `QUESTION` requirement or design decision that cannot be verified.

Each finding must include:

- File and line reference.
- Broken scenario.
- Why the changed code causes it.
- Minimal fix direction.

If there are no findings, say that clearly and list residual risk or checks not run.

For domain-model or Open Costing reviews, include a requirements coverage matrix covering the relevant workflow, BOM feedback, SMV feedback, reasons/comments, submission, revision history, ownership, status transitions, and historical integrity.

Report commands executed, pass/fail result, relevant failure output, commands that could not run, missing tests required before approval, and a final prioritized action list.

## Output Shape

```markdown
Merge Recommendation
- REQUEST CHANGES: Concise justification.

Immediate Findings
- [HIGH] Title
  Location: path/to/file.ext:123
  Problem: Explain the issue precisely.
  Impact: Explain the failure scenario.
  Recommendation: Describe the concrete correction.

Additional Findings
- [MEDIUM] Title
  Location: path/to/file.ext:123
  Problem: ...
  Impact: ...
  Recommendation: ...

Requirements Coverage
| Requirement | Supported | Evidence | Gaps or risks |
|---|---|---|---|
| Original values remain traceable | Partial | path/to/file.ext:123 | Missing immutable snapshot |

Test And Command Results
- `uv run pytest ...`: passed/failed/not run, with relevant output.

Missing Tests
- Exact test cases needed before approval.

Final Prioritized Action List
1. Highest-priority correction.

Open Questions
- Only include real ambiguities.

Review Notes
- Target reviewed, base/head, areas inspected, checks run or blocked, and remaining risk.
```
