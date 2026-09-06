## Verification

For behavioral, calculation, access, model/migration, API/service, pipeline, or bug-fix changes, run focused tests and add or update a regression test when existing coverage does not prove the change. Open Costing behavior follows the same rule. Do not add tests that mirror trivial implementation details. Data-only exports, configuration-only, branch-sync, and setup-only changes may use appropriate non-test checks. For UI changes, verify the real user path, saved payload/state, responsive behavior, and before/after full-page screenshots when available. Report missing evidence without claiming it passed.

Run `uv run python manage.py makemigrations --check` for model/migration changes. Existing focused test commands are in the checkout AGENTS.md. Mock external LLM calls.
