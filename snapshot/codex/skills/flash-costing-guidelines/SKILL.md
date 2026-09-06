---
name: flash-costing-guidelines
description: Shared Flash Costing domain constraints and engineering policy. Load only the references relevant to the affected workflow.
---

# Flash Costing Shared Rules

Apply to the active Flash Costing checkout. Direct user instructions take precedence. These rules are the shared source for this project’s companion skills; do not reload them through every workflow.

Keep costing ownership, staff-only schema administration, stable BOM row IDs, per-country prices, user-edited values, immutable Open Costing originals/snapshots, separate factory proposals, token scoping/expiry, and SMV frequency semantics. Use the existing LLM wrapper and mock external calls during tests. Generate migrations with `uv run python manage.py makemigrations`. New implementation uses an isolated worktree from the intended base, normally `origin/dev`, unless the user chooses the current checkout. No commit, push, PR mutation, or destructive Git operation without explicit authorization. Use neutral names and keep local instructions, secrets, and databases out of commits.

Complete necessary, reversible supporting changes within the requested outcome. Ask only for unresolved product/access decisions, separate scope, unauthorized external actions, or destructive operations. Reuse authorization already given in this task.

## Verification policy

For behavioral, calculation, access, model/migration, API/service, pipeline, or bug-fix changes, run focused tests and add or update a regression test when existing coverage does not prove the change. Open Costing behavior follows the same rule. Do not add tests that mirror trivial implementation details. Data-only exports, configuration-only, branch-sync, and setup-only changes may use appropriate non-test checks. For UI changes, verify the real user path, saved payload/state, responsive behavior, and before/after full-page screenshots when available. Report missing evidence without claiming it passed.

Use focused source searches by default. Use Graphify only for an explicit graph request or an architecture question that benefits from a current graph; do not rebuild it as a feature-start ritual. Check installed capabilities rather than assuming a provider key is required.

## Conditional references

- [Repo Shape](references/rules-repo-shape.md): read the relevant section only when the task touches repo shape.
- [Production Engineering Standard](references/rules-production-engineering-standard.md): read the relevant section only when the task touches production engineering standard.
- [Non-Negotiables](references/rules-non-negotiables.md): read the relevant section only when the task touches domain ownership, workflow semantics, or scope boundaries.
- [Open Costing Context Loading](references/rules-open-costing-context-loading.md): read the relevant section only when the task touches Open Costing specification or task decisions.
- [Open Costing Rules](references/rules-open-costing-rules.md): read the relevant section only when the task touches Open Costing proposals, tokens, snapshots, or comparisons.
- [Documentation](references/rules-documentation.md): read the relevant section only when the task touches documentation.
- [UI And JavaScript](references/rules-ui-and-javascript.md): read the relevant section only when the task touches ui and javascript.
- [Backend And API](references/rules-backend-and-api.md): read the relevant section only when the task touches backend and api.
- [Verification](references/rules-verification.md): read the relevant section only when the task touches verification.
- [Branch, Workspace, And Git](references/rules-branch-workspace-and-git.md): read the relevant section only when the task touches branch setup, local database setup, or an authorized Git operation.

Reference commands and repo paths are relative to the active checkout unless explicitly marked as skill resources. Do not read every reference for each task. If a worktree has different local instructions, compare its deliberate branch-specific facts with this shared policy; do not silently overwrite its product requirements.
