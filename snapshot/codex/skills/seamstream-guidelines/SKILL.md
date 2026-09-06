---
name: seamstream-guidelines
description: Shared SeamstreamAI domain constraints and engineering policy. Load only the references relevant to the affected workflow.
---

# SeamstreamAI Shared Rules

Apply to the active SeamstreamAI checkout. Direct user instructions take precedence. These rules are the shared source for this project’s companion skills; do not reload them through every workflow.

Preserve factory access, staff branches, domain database routing, operation-book history/locking, cache semantics, and storage save-before-delete safety. Use plain `python manage.py ...` or relevant `make` commands, not `uv`. Default base is `main`; preserve unrelated local edits and select the actual task checkout. Use the correct domain/database context. Avoid `make full_setup` when focused commands suffice. No Stripe, SendGrid, S3, or LLM mutations during routine verification; use mocks or local inspection. No commit, push, PR mutation, or destructive Git operation without explicit authorization. Use neutral names.

Complete necessary, reversible supporting changes within the requested outcome. Ask only for unresolved product/access decisions, separate scope, unauthorized external actions, or destructive operations. Reuse authorization already given in this task.

## Verification policy

Run the smallest relevant existing Django check or test. Add or update meaningful regression coverage when changed behavior or risk warrants it; do not require tests for trivial edits. For UI changes verify the real user path, desktop/mobile behavior, saved state, and before/after screenshots when available. For routed data changes verify the affected tenant database and a relevant isolation boundary. Report unverified cases accurately. Broaden checks only when a new change, failure, or shared-code risk justifies it.

Use focused source searches by default. Use Graphify only for an explicit graph request or an architecture question that benefits from a current graph; do not rebuild it as a feature-start ritual. Check installed capabilities rather than assuming a provider key is required.

## Conditional references

- [Repository Facts](references/rules-repository-facts.md): read the relevant section only when the task touches repository facts.
- [Non-Negotiables](references/rules-non-negotiables.md): read the relevant section only when the task touches domain ownership, workflow semantics, or scope boundaries.
- [Preflight Checkpoint](references/rules-preflight-checkpoint.md): read the relevant section only when the task touches an unresolved product, permission, or contract question.
- [Tooling And Commands](references/rules-tooling-and-commands.md): read the relevant section only when the task touches tooling and commands.
- [Branch, Database, And Environment](references/rules-branch-database-and-environment.md): read the relevant section only when the task touches branch, database, and environment.
- [Django And API Rules](references/rules-django-and-api-rules.md): read the relevant section only when the task touches django and api rules.
- [Product Data And Workflows](references/rules-product-data-and-workflows.md): read the relevant section only when the task touches product data and workflows.
- [LLM, Cache, Scheduler, And External Services](references/rules-llm-cache-scheduler-and-external-services.md): read the relevant section only when the task touches llm, cache, scheduler, and external services.
- [Storage And Files](references/rules-storage-and-files.md): read the relevant section only when the task touches storage and files.
- [UI And Template Rules](references/rules-ui-and-template-rules.md): read the relevant section only when the task touches ui and template rules.
- [Review And Handoff](references/rules-review-and-handoff.md): read the relevant section only when the task touches review and handoff.

Reference commands and repo paths are relative to the active checkout unless explicitly marked as skill resources. Do not read every reference for each task. If a worktree has different local instructions, compare its deliberate branch-specific facts with this shared policy; do not silently overwrite its product requirements.
