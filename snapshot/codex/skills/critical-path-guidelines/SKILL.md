---
name: critical-path-guidelines
description: Shared Critical Path domain constraints and engineering policy. Load only the references relevant to the affected workflow.
---

# Critical Path Shared Rules

Apply to the active Critical Path checkout. Direct user instructions take precedence. These rules are the shared source for this project’s companion skills; do not reload them through every workflow.

Scope every change to the requested tenant and role; use existing configuration and permission helpers, never tenant-name/ID hardcoding. Preserve non-target tenant/role behavior and active UI/API capabilities. Odoo is strictly read-only. Generate normal Django schema migrations; never introduce production seed/backfill behavior without explicit scope. Use `uv run python manage.py ...`. New feature work uses an isolated worktree from `origin/dev` unless the user chooses another workflow; PR fixes stay on the existing PR head. Preserve unrelated work. No commit, push, merge, PR mutation, or destructive Git operation without the applicable explicit authorization. Use neutral names and no tool attribution.

Complete necessary, reversible supporting changes within the requested outcome. Ask only for unresolved product/access decisions, separate scope, unauthorized external actions, or destructive operations. Reuse authorization already given in this task.

## Verification policy

Do not add or update automated tests unless the user explicitly overrides that project restriction. Use relevant existing checks and real product/API verification. For visible changes, capture matching full-page before/after evidence and verify affected target/non-target tenants, brand/factory roles, responsive states, and persistence. Backend-only work uses an appropriate existing command or API check. Report unavailable proof accurately; finish independent work without repeatedly asking for an evidence waiver. Repeat broader checks only for new failures, shared-code risk, or explicit acceptance criteria.

Use focused source searches by default. Use Graphify only for an explicit graph request or an architecture question that benefits from a current graph; do not rebuild it as a feature-start ritual. Check installed capabilities rather than assuming a provider key is required.

## Conditional references

- [Non-Negotiables](references/rules-non-negotiables.md): read the relevant section only when the task touches domain ownership, workflow semantics, or scope boundaries.
- [Preflight Checkpoint](references/rules-preflight-checkpoint.md): read the relevant section only when the task touches an unresolved product, permission, or contract question.
- [Open Source Repository Tooling](references/rules-open-source-repository-tooling.md): read the relevant section only when the task touches open source repository tooling.
- [Branch And Verification](references/rules-branch-and-verification.md): read the relevant section only when the task touches branch setup, PR refresh, local database setup, or migrations.
- [Pre-Commit Self-Review Checklist](references/rules-pre-commit-self-review-checklist.md): read the relevant section only when the task touches pre-commit self-review checklist.
- [API Rules](references/rules-api-rules.md): read the relevant section only when the task touches api rules.
- [UI And Template Rules](references/rules-ui-and-template-rules.md): read the relevant section only when the task touches ui and template rules.
- [Reviews And Handoff](references/rules-reviews-and-handoff.md): read the relevant section only when the task touches reviews and handoff.

Reference commands and repo paths are relative to the active checkout unless explicitly marked as skill resources. Do not read every reference for each task. If a worktree has different local instructions, compare its deliberate branch-specific facts with this shared policy; do not silently overwrite its product requirements.
