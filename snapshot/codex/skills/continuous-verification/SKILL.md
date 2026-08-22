---
name: continuous-verification
description: "Use when Codex is implementing features, fixing bugs, addressing review feedback, or declaring code complete and must verify every requested requirement against the actual codebase. Enforces baseline audits, duplicate-implementation checks, continuous re-verification after meaningful edits, cross-file completeness checks, regression audits, and a final completion gate before saying work is done."
---

# Continuous Verification

Use this skill to prove the requested work exists in the codebase. Treat implementation as incomplete until each requirement is verified by inspection and, where applicable, runnable checks.

## Baseline Audit

Before editing code:

1. Parse the user's request into atomic requirements.
2. Create an internal checklist for every requirement.
3. Search the codebase for each item before assuming it is missing.
4. Classify each item as `COMPLETE`, `PARTIAL`, `MISSING`, or `INCORRECT`.
5. Reuse or extend existing code when it already covers the need.

Search the relevant surface area, including routes, services, models, serializers, APIs, migrations, frontend code, tests, feature flags, permissions, and utilities.

## Pre-Edit Gate

Before modifying any file, answer:

`Does this requirement already exist somewhere else?`

If yes, verify correctness, integration, and edge cases. Prefer extending the existing implementation over creating duplicate logic.

## During Implementation

After every meaningful change:

1. Stop and re-check the current requirement.
2. Confirm the changed code is wired, imported, registered, reachable, and used.
3. Check permissions, validation, error handling, state updates, response shapes, and tests relevant to the change.
4. Fix verification failures before moving to the next requirement.

Also verify new code creates no broken imports, dead code, orphan models, unused APIs, missing exports, missing dependency injection, forgotten routes, missing migrations, or inconsistent types.

## Cross-File Audit

For features spanning layers, verify all affected layers explicitly:

- Backend: route, controller/view, service, model, validation, permissions, tests.
- Frontend: API client, hooks, state, components, loading, errors, empty states.
- Database: migration, constraints, defaults, indexes.

Only check layers that exist in the project and are relevant to the request.

## Regression Audit

After completing each feature or bug fix:

1. Search for callers and neighboring code that could be affected.
2. Inspect imports, interfaces, API contracts, serializers, response shapes, state management, database queries, permissions, caching, and tests.
3. Run the smallest relevant test or command that would fail if the change is broken.

## Final Completion Gate

Before declaring the task complete:

1. Re-read the original user request.
2. Compare every requirement against the implementation.
3. Mark each item `YES`, `NO`, or `PARTIAL` internally.
4. Search again for duplicate implementations, stale code, TODOs, placeholders, mocks, temporary fixes, missing edge cases, and broken references.
5. Run applicable tests or explain exactly why they could not be run.

Do not claim completion unless every requested requirement exists, is verified, has no known partials, and passes applicable checks.

## Failure Recovery

If verification fails at any point:

1. Stop implementation.
2. Determine why verification failed.
3. Fix the issue.
4. Re-run verification.
5. Continue only after the check succeeds.
