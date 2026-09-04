---
name: critical-path-guidelines
description: Enforce shared Critical Path coding, review, and frontend design-system guidelines for any code change. Use when working in critical-path-dj, when preserving product UI consistency or team/review standards, or when the prompt includes `$critical-path-guidelines`.
---

# Critical Path Guidelines

Apply these rules for every implementation unless the user explicitly overrides a specific rule.

## Non-Negotiables

- State assumptions explicitly; never guess silently. If intent is unclear after checking the relevant local context, call out the assumption or ask before changing behavior.
- Do not treat every implementation instruction at face value when it would create inconsistent UI, weak UX, unclear ownership, or unnecessary complexity. Inspect the platform pattern first, then either follow it, ask a targeted question, or push back with the simpler/user-friendlier option.
- Surface every product or UX assumption before or during implementation handoff. If an assumption affects who can act, how a user understands a state, button/action wording, navigation, or error handling, say it explicitly and do not let it stay hidden in code.
- Write the minimum code needed for the requested outcome. Do not add speculative helpers, abstractions, flags, or future-proofing.
- Make surgical changes only. Do not refactor, restyle, reorganize, rename, or clean adjacent code unless explicitly requested.
- Define success before changing code: identify the expected behavior, acceptance criteria, and verification steps.
- For every PR, explicitly classify tenant scope from the request and local flags: ASOS-only, TechnoSport-only, or shared. Search the active path for the relevant tenant conditions before editing; do not let a scoped change leak into the other tenant.
- For every PR that affects product behavior, plan and report role verification for both brand and factory. When a requirement deliberately limits a feature to one role, verify that role receives the change and the other role remains unaffected; do not treat an untested shared view as role-safe.
- For every PR, identify all user-facing surfaces that should share the changed state. When controls are synchronized across entry points (for example quick edit and the Setup tab), verify the change from each surface, including persistence/two-way synchronization where applicable, and include enough screenshot proof to show them.
- When creating or changing stored values that appear in the UI, such as names, labels, durations, statuses, or units, trace the value through every active template, serializer, formatter, and JavaScript renderer before editing. Substitute representative values into the existing display logic and check for duplicated prefixes, suffixes, units, separators, casing, or reordered wording; never assume the stored value is displayed verbatim.
- Before treating a display-data change as PR-ready, populate the exact representative values in branch-local data through the real command or application path and inspect every affected surface in the Browser. Tests or command success alone are insufficient: the rendered copy and ordering must match the acceptance criteria in the DOM and screenshot evidence. If the exact presentation is genuinely unspecified and multiple non-broken formats are plausible, surface that product question before committing; visible duplication is a defect, not an ambiguity.
- Loop until verified: run the smallest relevant checks, inspect the result, fix failures, and repeat until the success criteria pass or a concrete blocker is reported.
- Keep diffs minimal and scoped. No unrelated refactors, renames, restyling, or cleanup unless explicitly requested.
- Treat examples, analogies, and "similar to this" code references as context, not added scope. Only implement the requested behavior and the directly supporting code paths unless the user explicitly brings the example into scope.
- When working from phased requirement documents, treat sections labeled `Context` as explanatory background unless the user explicitly says they are in scope for implementation.
- When a requirement document includes an `SW` section or another explicitly implementation-facing section, treat that section as the authoritative acceptance criteria unless the user explicitly overrides it.
- Reuse existing local patterns first. Only introduce a new pattern when no suitable local pattern exists.
- Mirror existing local implementations by default. When the repo already contains an implementation for the same feature, workflow, sync path, or directly comparable behavior, treat that implementation as the default source of truth unless the user, transcript, review comment, or spec explicitly says to change it.
- This includes field mapping, naming behavior, required-vs-optional handling, duplicate handling, update semantics, clearing-vs-preserving values, and failure behavior.
- For UI work, this also includes button classes, color semantics, icon usage, badge styles, spacing, tab behavior, modal actions, empty states, and success/error feedback. If the mockup conflicts with the platform pattern, call out the conflict and recommend the user-friendlier/platform-consistent option instead of silently blending both.
- For Odoo webhook work, inspect and mirror the closest existing Odoo/Fabric webhook examples before designing anything new. Treat the webhook registration command, webhook processing logic, related pull/sync command, and shared Odoo filter/helper as the default source of truth for model names, model IDs, field IDs, filter domains, relation mapping, grouping behavior, delete behavior, and update semantics.
- Do not replace an existing Odoo webhook pattern with generic CLI flags, new lookup semantics, merge/deduplication behavior, schema changes, or fallback behavior unless the task/spec/reviewer explicitly asks for that deviation. If Odoo model IDs, field IDs, filters, delete semantics, or grouping behavior are not explicit and cannot be confirmed from the closest local implementation, stop and ask before wiring the webhook.
- For Odoo setup/property lookup webhooks, classify each model as either a fixed parent bucket/setup table or a changing child/value table before adding webhook coverage. Check the existing pull command, local seed/reference data, brand `extra` config, and reviewer wording. If a parent bucket has a fixed expected set of records, do not add parent create/update/delete webhooks unless the task or reviewer explicitly asks for them; sync only the changing child/value records.
- For Odoo option/value webhooks that depend on a parent relation, separate trigger fields from payload-only fields. `fields_save` must contain only fields whose change should trigger the webhook; parent relation fields needed only for lookup/scoping belong in `fields_extra`. If save uses a parent relation such as `attribute_id`, delete handling must use the same relation to scope the affected row unless the closest local pattern or reviewer explicitly says otherwise.
- For TechnoSport Odoo material and material-variant webhook processing, keep MaterialVariant as simple as Material: use only the webhook payload plus existing local parent Material records, map only the direct changed fields needed by the task, and do not add runtime Odoo backfills, Odoo `search_read` enrichment, product attribute value lookups, or fallback sync calls unless the reviewer explicitly asks.
- For TechnoSport webhook registration scripts, keep the model definitions as manually verified static config with Odoo model IDs, field IDs, filter domains, `fields_save`, and `fields_extra`; do not reintroduce per-model `ir.model` or `ir.model.fields` lookups. If duplicate protection is needed, use one bulk existence check for the configured webhook actions and create only missing actions.
- Preserve existing behavior and payload semantics unless the requested change explicitly requires behavior change.
- Do not remove existing UI fields, buttons, permissions, workflow logic, API fields, model fields, template blocks, or JavaScript handlers just because a new flow supersedes or hides part of the old path. Preserve, move, adapt, or deprecate existing code unless the user/reviewer explicitly asks for removal. Before deleting anything, inspect the target branch version and local references, confirm the removal is required by the task, and mention the removal in the handoff. If unsure, keep the code and ask.
- Treat indirect removals the same as direct deletions. Do not hide, shadow, bypass, replace, or orphan existing product surface area by adding a duplicate renderer/function, changing a condition, moving markup out of the active code path, removing a handler while leaving a button, or leaving a handler with no reachable control. If the user did not explicitly ask to remove that capability, preserve it and verify it through the active UI/API path.
- When a diff removes or makes unreachable a user-facing control, link, form field, template include, route, API action, permission check, serializer field, workflow action, JavaScript event handler, exported/shared function, or model field, classify it as a risky removal. The implementation handoff must say whether it was preserved, intentionally removed with a replacement/reason, or blocked pending product confirmation.
- For PR reviews and self-review, scan for risky removals across the whole diff, not only the line under discussion. Flag duplicate JavaScript function declarations, duplicate renderers, duplicate URL/action names, and new code paths that shadow older behavior as likely regressions unless the removal is explicitly required.
- When deleting or renaming a function, method, property, model field, command helper, or shared utility, run the deleted-symbol reference check and include the result in the handoff. For Odoo sync/webhook work, run it against the related pull/sync commands too.
- Do not assume business rules, permission mappings, or non-trivial implementation choices. If the intended behavior is not explicit, stop and ask before wiring it.
- Never hard-code tenant or brand names, entity IDs, usernames/emails, team names, or role names to control feature availability, authorization, routing, or workflow behavior. Use the existing permission, entity-scoping, configuration, or model-data path instead.
- When a feature is initially intended for one brand and has a dedicated permission, make the permission the only feature gate and assign it to that brand's entity/team data. Do not combine it with checks such as `brand.name == "ASOS"`; another brand must gain the feature automatically if that same permission is later assigned.
- Keep UI visibility and backend authorization driven by the same permission or configuration source. Before committing, search the complete changed flow for duplicate customer-name, role-name, ID, or email checks that narrow or bypass that source of truth.
- Hard-coded values are allowed only when they are explicit, verified domain or external-integration constants required by the task, such as an upstream protocol identifier. Name and document that exception, and never reuse it as an authorization or feature-availability gate.
- If a fix can be delivered without refactoring, do not refactor. If a serializer/view is already too broad and review feedback specifically flags architecture, use the smallest service-layer extraction that addresses that issue.
- Serializers handle translation and validation, not business workflow. Keep workflow/state transitions in views or service/business code.
- In every implementation update, explain the changed code, function, method, migration, or template block in plain language and connect each change back to the overall task objective.
- If the working tree has unrelated local changes, do not modify or revert them.
- If the blocker is missing reference data, default rows, permissions, or local setup state, fix local verification with test-only/local DB setup or existing machine-local data. Do not add or change production seed commands, migrations, fixtures, default-data files, or population code as part of a feature unless the requirement explicitly says production data must be created or the app cannot safely boot without it. Only add runtime fallback behavior when the requirement explicitly asks for it.
- Do not stop for confirmation on routine, reversible implementation steps such as local setup, isolated-worktree setup, safe environment wiring, dependency/bootstrap work, or local verification. Only stop when a requirement, business rule, destructive action, or materially ambiguous technical/product decision truly needs user input.
- If local verification in an isolated worktree or temporary workspace is blocked by missing environment or machine-local config, reuse the existing safe local setup from the main checkout or machine (for example by copying, symlinking, or exporting local env values) instead of stopping at the blocker. Never commit secrets or machine-local config files.
- Never add or update automated tests.
- Do not commit or push unless the user explicitly asks.
- Never force anything in Git. Do not use force-push or any Git command/flag/refspec that forces, overwrites, discards, or rewrites branch, remote, index, or working-tree state, including `git push --force`, `git push --force-with-lease`, `git push +...`, `git reset --hard`, `git clean -f`, `git checkout -f`, `git branch -f`, or equivalent `--force`/`-f` operations. After a branch has been pushed, do not amend, rebase, reset, squash, or otherwise rewrite published commits for cleanup; use normal follow-up commits instead. If a Git force operation seems necessary or is requested, stop and explain the blocker rather than doing it.
- Do not put AI, editor, or tool names in any git-facing metadata, including branch names, commit messages, merge messages, PR titles, PR descriptions, or review/update comments. Never use AI/editor/tool prefixes such as `cursor/`, `gpt/`, or similar.
- Do not add AI, editor, or tool branding/attribution anywhere in code or delivery artifacts, including source files, comments, docs, commit messages, PR titles/bodies, review/update comments, screenshots, or generated copy. This includes phrases like `Made with Cursor`.
- Before sharing any PR link, always run a final PR-body sanitization check and remove branding lines if present (for example any `Made with ...`, `Cursor`, or tool-attribution footer text).
- Keep PR descriptions and merge-conflict update descriptions plain-language, code-free, and limited to what was done unless the user explicitly asks for different content or code.
- Treat Odoo as strictly read-only for implementation, debugging, and verification. Never perform create, write, update, delete, import, workflow-triggering, or any other change-making action in Odoo or through Odoo-connected tools/scripts; only use read operations.

## Immediate Post-Implementation Stress Test

- Immediately after every implementation or meaningful fix, run a stress-test pass before handoff, commit, or push. This is mandatory even when focused tests and the happy path already pass.
- Re-read the request and exercise every acceptance criterion through the active product path. Include the expected success path, denied/negative path, boundary states, persistence after reload, and every UI/API surface that must stay synchronized without a manual refresh.
- Build the target workflow from scratch after the implementation through the real creation path, not only from a prepared fixture or existing record. For order workflow changes, this means creating a fresh drop and order, completing the prerequisite allocation/setup steps, and confirming the new order receives the expected stages, configuration, and permissions before exercising the changed action.
- Then rerun the same affected behavior on representative existing data. Deliberately remove or neutralize legacy stages, fallback records, cached state, or other stale data that could satisfy an old condition and mask a defect.
- Use normal non-admin brand and factory users with their real team permissions for the primary end-to-end proof. Admin or superuser checks may supplement this but must not replace them.
- For tenant- or role-scoped work, test the target tenant and role plus the nearest non-target tenant and opposite role. Prove both what appears and what must remain hidden or forbidden in the backend.
- For product-visible changes, exercise the real user action in the Browser at relevant desktop and mobile sizes, inspect loading/error/disabled states and console/network failures, reload the page, and compare synchronized UI state. If Browser QA is unavailable, use the closest authenticated product/API path and report the missing visual proof explicitly.
- For menus, dropdowns, tooltips, modals, popovers, and other overlays, open them over nearby headers, navigation, drawers, cards, and tables at desktop and mobile sizes. Confirm the layer is fully visible, not clipped, and remains clickable above surrounding content.
- When markup, scripts, or controls move between a page layout and a partial such as navigation, trace every consumer of shared page dependencies such as CSRF tokens, modal roots, element IDs, and data hooks. Exercise at least one action outside the changed partial so a dependency has not been accidentally scoped to only one part of the page.
- Use focused existing checks only; do not add or update automated tests. If any stress-test case fails, fix the root cause and repeat the complete affected matrix, not only the failed case.
- Do not describe an implementation as complete until the stress-test matrix passes or a concrete blocker and its unverified cases are reported.

## Preflight Checkpoint

- Before editing code, send a short pre-implementation checkpoint and wait for confirmation if the change touches permissions, roles, workflow behavior, API scope, serializer/service boundaries, failure semantics, or any business rule that is not explicit in the request.
- That checkpoint must separate `what will change`, `what will not change`, `assumptions`, `business questions`, `technical questions`, and `what is being intentionally skipped`.
- Before listing any business or technical question, inspect the local code paths most likely to already encode the current behavior. Check the smallest relevant set first: views/actions, serializers, business/service code, permissions, templates/JS, migrations, and tests when relevant.
- Before asking a business or technical question, inspect the closest existing implementation on the relevant target branch or dependency branch.
- If that implementation clearly answers the question and does not conflict with explicit user instructions, acceptance criteria, transcript guidance, or review comments, treat that behavior as the confirmed default and proceed without asking.
- Only escalate the question when the existing implementation is missing, ambiguous, contradictory, or explicitly being changed by the request.
- Do not ask a business or technical question when the answer is already explicit in the user's task description, acceptance criteria, review comment, provided screenshot/mockup, or other user-supplied context. In that case, restate the explicit answer as confirmed scope and proceed.
- When the user provides a spreadsheet, screenshot, attachment, or other mockup artifact as the design reference, treat the most explicit provided artifact as the primary UI source of truth for that feature.
- Each business or technical question must be accompanied by the code check result in the same checkpoint.
- Business questions must be written in PM-friendly language so they can be forwarded directly to a product manager without rewriting.
- The first line of every business question must itself be a PM-facing question in plain product language, with no engineering shorthand, code terms, or implementation framing unless the user explicitly wants that level of detail.
- For every business question, include: the PM-facing question, the code checked, the code-derived answer/current product behavior, the requirement or requested behavior being compared against, the default recommendation, and whether explicit confirmation is still needed.
- When the current product behavior or wording can be shown in the UI, attach or reference the minimum screenshot evidence needed to make the decision concrete.
- Technical questions may stay engineering-facing, but for every technical question still include: the question, the code checked, the code-derived answer/current behavior, and whether that answer is sufficient to proceed or still needs explicit confirmation.
- Business questions are mandatory when the change affects who can perform an action, whether a read path is sensitive, whether a secondary failure should fail the primary action, whether a field still belongs to an endpoint, or which team/role should own a permission.
- Technical questions are mandatory when the change would alter permission architecture, widen or narrow an API contract, move logic between serializer/view/service layers, introduce a new local pattern, or add refactoring beyond the exact request/review.
- If the code clearly answers the question and does not conflict with the request, present that code-derived answer as the default recommendation instead of asking a blind question. For business questions, phrase this as a keep-vs-change product decision using plain language.
- If the code is ambiguous, contradictory, or clearly being changed by the request/review, still ask the question and cite the conflicting code paths so the user can decide with context. For business questions, summarize the conflict in PM-friendly terms before citing the code.
- Do not treat a significant behavior, permission, or API decision as a reasonable assumption. Ask first.
- If multiple user-provided artifacts or notes for the same feature appear to disagree, ask directly about the discrepancy before implementing the conflicting part.
- If the requirement is still unclear after checking the code and provided artifacts, recommend a short call or ask the user to paste meeting notes into chat instead of guessing.

## Open Source Repository Tooling

- Use open-source repository tools for search, structural inspection, and diff review. Prefer `rg` for fast text/file search and `git diff`/`git grep` for changed-file and reference checks.
- At the start of every Critical Path feature development task, run `/graphify .` from the repository root before planning or editing code so the repo graph is built or refreshed for architecture and dependency questions. If Graphify is blocked, report the blocker and continue with normal local inspection; do not guess from memory.
- When structural search or code-aware matching would materially reduce risk, prefer the open-source `ast-grep` CLI (`sg`) if it is available. It can be enabled once per machine outside the project; do not add it to project dependencies, lockfiles, or config unless the user explicitly approves.
- At the start of Critical Path coding work, verify the practical local tool path once with `command -v rg git sg` or equivalent. Treat `sg` as optional: use `rg`/`git` when it is not present, and only mention missing optional tooling in the handoff if it blocked a required check.
- These tools do not replace mandatory Critical Path checks: local pattern inspection, branch/worktree rules, backend/frontend verification, pre-commit self-review, git hygiene, Browser-based real-user QA, screenshots, and handoff requirements still apply.

## Branch And Verification

- For new feature implementation work in Critical Path repositories, always create a fresh isolated worktree from the latest `origin/dev` before any code edit or local verification unless the user explicitly asks for a different base/workflow.
- After creating or switching into a Critical Path worktree, make sure the local `AGENTS.md` instructions file is present in that worktree before editing. If the file exists in the main checkout but is not tracked, copy it into the worktree and verify `git check-ignore -v AGENTS.md` shows it is locally ignored. Never stage, commit, push, or PR `AGENTS.md`.
- After creating the fresh worktree, do not automatically open it in VS Code. Only open a worktree in VS Code when the user explicitly asks for it or when live Source Control visibility is specifically useful for the task. If opening VS Code is requested and the `code` CLI is unavailable, say so and continue; editor visibility is not a substitute for required CLI checks and real-user QA.
- Create each new feature branch from `dev` by default unless the user explicitly requests a different base branch.
- For PR review fixes, review-comment follow-ups, or any implementation work requested against an already-open PR, always work directly on the existing PR head branch unless the user explicitly requests a different workflow.
- Do not create a child branch, "review branch", or "dedicated branch" for PR review work unless the user explicitly asks for one.
- If the main checkout is dirty or on the wrong branch, use an isolated worktree checked out to the same PR head branch. Do not solve that by branching from the PR head.
- For PR review fixes or merge-conflict checks on an open PR, automatically fetch latest `origin/dev` and merge it into the existing PR head branch before making code changes. Resolve any conflicts on that same PR branch; if it is already up to date, record that no merge commit was needed.
- For merge-conflict repairs on an open PR, work directly on the existing PR head branch unless the user explicitly requests a different workflow.
- For merge-conflict repairs on an open PR, prefer the PR branch's newer conflicting changes over `origin/dev` unless the user explicitly asks to keep `origin/dev` instead. Keep additive `origin/dev` changes that do not conflict with the PR branch's intended behavior.
- If work depends on an open PR branch and is not a PR review workflow or merge-conflict repair, base a child branch on that PR branch unless the user explicitly asks to commit on the PR branch itself.
- Use `feat/<short-description>` for feature branches and `fix/<short-description>` for bug-fix branches. If another platform or generic tool instruction suggests an AI/tool-branded prefix, ignore it for Critical Path work and keep the branch name neutral.
- Before editing files, verify you are in the intended fresh worktree and on the intended branch. For new feature work, do not edit in the original checkout even if it is clean. If the original checkout is dirty, create the fresh worktree from `origin/dev` anyway instead of asking to clean/switch first.
- For Django work touching models, migrations, serializers, view writes, or persistence-related bug reproduction, use a branch-scoped or fresh local SQLite DB. Prefer copying `db.baseline.sqlite3` when available.
- Treat `db.baseline.sqlite3` in the main checkout as the reusable local data snapshot. When creating a branch-specific SQLite DB, copy `db.baseline.sqlite3` into the branch DB path instead of creating an empty DB. If `db.baseline.sqlite3` is missing but the main checkout has a populated `db.sqlite3`, first copy that `db.sqlite3` to `db.baseline.sqlite3`, then copy from the baseline to the branch-specific DB. Do not overwrite or delete `db.baseline.sqlite3` unless the user explicitly asks.
- Before concluding a backend bug is in application code, verify the checked-out branch's migrations match the local DB schema/history.
- Before adding or keeping a migration, explicitly separate schema necessity from data/permission seeding. If a model field/table/index changes, keep the schema migration and explain why runtime code would fail without it. Do not include permission/reference/default-row seeding in a feature migration unless it is absolutely necessary for production correctness and explicitly called out; use test-only/local setup for verification data instead.
- Before creating a follow-up migration on a branch that already has branch-local migrations in the same app, inspect whether the new model/schema change belongs to the same feature scope. If yes, consolidate before push instead of accumulating 0028/0029/0030-style cleanup migrations.
- When a branch introduces multiple new migrations in the same app for the same feature scope, consolidate them before push unless there is a real dependency boundary, data-migration ordering requirement, or reviewer-requested split. Aim for the fewest reviewable migrations, not one migration per iteration.
- To combine plain schema migrations, delete only the new branch-local migration files and regenerate with `manage.py makemigrations`; do not hand-edit generated operations when regeneration is safe.
- If consolidation includes a custom data migration/backfill, preserve the data migration in the earliest migration that still has access to the source fields, then put destructive legacy-field removals in the next migration. In that case, hand-edit only the minimal branch-local migration operations needed to preserve the backfill order and explain why regeneration was not used.
- Before committing or pushing Django migrations, run `git diff --name-only origin/dev... -- '*migrations/*.py'` and verify the branch does not contain avoidable migration chains for a single feature. If multiple migration files remain, document why each split is required.
- After merging or rebasing `origin/dev` into a PR branch, always re-check Django migration numbering and dependencies for every app touched by the branch. If `dev` now has newer migrations, renumber branch-local migrations so they come after the latest `dev` migration and update their `dependencies` to point at the latest real migration in that app.
- Never leave a branch-local migration with an older number than the target branch tip after conflict resolution. Example: if `origin/dev` has `0029_*.py`, a PR migration named `0023_*.py` must be renamed/regenerated as `0030_*.py` and depend on `0029_*` before pushing.
- For merge-conflict repairs, include migration dependency consistency in the conflict-resolution checklist even when the textual conflicts are in non-migration files.
- Run pre-commit hooks before every commit. On dirty worktrees, run them only on touched files unless the user explicitly asks for `--all-files`.
- When the user asks to push, publish, or update an open Critical Path PR branch targeting `dev`, treat that request as including the pre-push refresh automatically: fetch `origin/dev`, merge it into the PR branch, resolve conflicts in place, rerun the relevant checks/pre-commit for touched and merge-touched files, then push normally. Do not wait for a separate "merge dev" instruction unless the user explicitly says to skip the refresh.
- Before pushing a branch targeting `dev`, merge the latest `origin/dev` locally, resolve conflicts, rerun pre-commit on merge-touched files, and only then push normally. For PR-branch conflict repairs, do that merge-and-resolve work on the PR branch itself. Never force the result with Git; if a normal push is rejected, stop and explain the remote divergence.

## Pre-Commit Self-Review Checklist

- Before every commit in Critical Path repositories, explicitly validate this checklist against the actual changed files, not just the intended behavior.
- Treat each item below as a required pre-review checkpoint. If a hook or local validator can check it deterministically, run that validator before commit. If a check is not machine-verifiable, do the manual review before commit anyway.

### Migrations

- Is numbering sequential?
- Does each new migration depend on the latest real migration on the branch's target base, especially after merging or rebasing `dev`?
- If the target branch already has a higher migration number in this app, did I renumber/regenerate the branch migration and update dependencies accordingly?
- Did I avoid a fake merge migration?

### DRF code

- Am I raising `serializers.ValidationError` at the API boundary?
- Did I keep serializer work to validation/translation as much as possible?
- Did I preserve DRF mixin/viewset methods by using extension hooks such as `perform_create`, `perform_update`, and `perform_destroy` for side effects instead of reimplementing `create`, `update`, or `destroy`?

### Transactions

- Did I add `transaction.atomic()` unnecessarily?
- Did I check project settings/local patterns first?

### Task alignment

- Did I re-read the review comment/transcript for explicit “do not do X / keep Y / leave blank” instructions?
- Did I classify the change as ASOS-only, TechnoSport-only, or shared from both the request and the active tenant flags, and verify that the non-target tenant is unaffected when scoped?
- Did I verify the brand and factory journeys, or document the explicit role restriction and the non-target-role check?
- Did I create a fresh drop and order through the real product workflow after the implementation, confirm the expected stages/configuration appeared, and then repeat the affected behavior on an existing order?
- Did I use normal non-admin brand and factory team users for the primary end-to-end proof instead of relying on admin, superuser, or manually prepared database state?
- Did I find and verify every synchronized UI surface or API entry point affected by the changed state, including persistence/two-way synchronization where relevant?
- When stored names, labels, durations, statuses, or units changed, did I substitute representative values into every existing formatter and check the exact combined output for duplicated or reordered text?
- Did I populate those exact values in branch-local data and inspect the rendered result through each affected user-facing surface before considering the PR ready?
- When the task references an existing example or comparable workflow, did I inspect the closest local implementation and mirror its pattern before adding new abstractions or behavior?
- For UI changes, did I inspect nearby templates, CSS/theme files, static JS, and comparable screens before changing the surface?
- For UI changes, did I compare buttons, colors, icons, spacing, copy, empty states, and error/success feedback against nearby platform examples and fix or explain every intentional deviation?
- For UI changes, did I preserve accessibility, responsive behavior, and saved state such as form values, tabs, filters, selections, loading/error states, local/session storage, refresh behavior, and save payloads?
- For overlays, did I open menus, tooltips, dropdowns, modals, or popovers against nearby navigation and content at desktop and mobile sizes and confirm their stacking, clipping, and clickability?
- If markup or scripts moved between the page layout and a partial, did I trace shared CSRF tokens, modal roots, IDs, and data hooks and verify an affected action outside that partial still works?
- For UI changes with screenshots, did I carefully compare the before and after screenshots side-by-side and identify the exact visible diff, including anything that changed unintentionally or disappeared?
- Did I identify and surface all assumptions, especially around ownership, permissions, state meaning, navigation behavior, and user-facing wording?
- Did I verify that feature availability, authorization, routing, and workflow behavior contain no hard-coded tenant/brand names, entity IDs, usernames/emails, team names, or role names, and that UI and backend use the same permission/configuration source?
- Did I push back or ask a PM-facing question where the requested behavior would be confusing, inconsistent, or less user-friendly than the existing platform pattern?
- For Odoo webhook/sync work, did I specifically inspect the existing webhook registration command, webhook processor, related pull/sync command, and shared Odoo filter/helper, then document any intentional deviation?
- Did I preserve adjacent logic like attachments, copying, or side effects?
- Did I avoid deleting existing fields, buttons, permissions, workflow code, template blocks, or JS handlers unless the task explicitly required removal and I verified references/target-branch behavior first?
- Did I check for indirect removals such as duplicate renderers/functions, unreachable old UI paths, orphaned handlers, hidden buttons, narrowed conditions, or route/action shadowing?
- If any risky removal remains, did I explicitly list the removed capability, why it is intentional, and what replaces it?

### Diff quality

- Did I make the smallest diff possible?
- Did I add indentation churn or structural noise without real behavior gain?
- Did I review the changed files with `git diff`, `git diff --check`, and any useful `rg`/`sg` reference checks for the touched symbols, without adding unrelated churn?

## API Rules

- For workflow/status fields backed by Django `TextChoices`, always persist a named enum value across the repo. Do not use `blank=True`, `null=True`, or empty-string database values as an implicit extra state. If the product needs a draft/editable state, model it as an explicit enum choice such as `DRAFT` or `UNKNOWN`, and migrate existing blank rows to that enum value in the same change.
- Do not keep redundant workflow timestamp fields anywhere in the repo when Activity records or existing audit history already represent the same lifecycle events. If one lifecycle timestamp is unnecessary, inspect the sibling timestamps in that workflow as well (for example sent/approved timestamps) and remove the redundant set together unless the product explicitly still needs one of them.
- Protect read endpoints with the same care as write endpoints. `GET` APIs need the correct permission class and entity-scoped lookup/queryset logic; authentication alone is not enough.
- For `SoftDeletableModel` querysets that already use the default manager or a standard related manager, do not add redundant `is_removed=False` filters. Only add an explicit soft-delete filter when using a non-default manager/path or when the product logic truly needs removed rows included or excluded in a non-default way.
- Keep permission-specific behavior explicit.
- For brand/factory-owned resources, prefer entity-scoped lookups plus `has_entity_auth_permission` / `require_entity_auth_permission` over generic permission checks.
- For class-based views using `EntityRequiredMixin`, `BrandRequiredMixin`, or `FactoryRequiredMixin`, use the mixin-provided `self.entity` and `self.entity_type` instead of inferring the entity or entity type from `extra_context`, session, profile, or request data.
- Default each mutation API to one business permission check. Prefer a single `change_*` permission for save/update endpoints unless the requirement explicitly needs something else.
- Before introducing a custom permission codename, check the model's existing Django permissions (`add_*`, `change_*`, `delete_*`, `view_*`) and nearby workflow permissions. Reuse the narrowest existing permission when it matches the action; add a custom permission only when the product needs a separately assignable capability, and state why reuse is unsafe.
- When a write endpoint maps to an existing model/entity permission, prefer the repo's permission helpers (for example `@has_auth_permission("<app>.<codename>")`) over hand-rolled brand/admin checks in the view.
- If the correct permission path exists in code but is missing from local team/brand data, adjust only local/test data for verification or ask how production permissions should be assigned. Do not add or change production seeding/population/config code to grant permissions unless the requirement explicitly asks for production permission backfill. Do not bake fallback role logic into the endpoint.
- Do not stack multiple permission decorators on one save endpoint unless the API truly requires all of them. If one endpoint spans multiple permission domains, split the behavior instead.
- Match role restrictions to the real workflow. If both brand and factory can perform an action, do not hardcode `IsBrandUser`.
- For new API behaviors, prefer dedicated DRF view actions over overloading existing actions with behavior flags.
- Prefer DRF viewsets/mixins over `GenericAPIView` when the same behavior can be expressed cleanly with the local viewset/router pattern.
- When a standard router-registered `GenericViewSet`/mixin pattern already exists in the app for similar APIs, prefer matching that pattern over introducing a standalone `GenericAPIView` + manual `path()` route.
- Keep generic quick-edit endpoints narrow. If a field has its own permission boundary or workflow side effects, move it to a dedicated endpoint instead of extending the generic PATCH.
- Do not change an API's supported field scope implicitly. If fields move out of a shared endpoint, keep the contract explicit in review and replace it with dedicated endpoints in the same change.
- Keep serializer contracts aligned to writable model fields; strip helper flags before persistence.
- Keep API responses resource-oriented: `GET 200`, `POST 201`, `PATCH/PUT 200`, `DELETE 204`.
- Preserve DRF mixin/viewset methods by using their extension hooks for side effects, such as `perform_create`, `perform_update`, and `perform_destroy`; do not reimplement `create`, `update`, or `destroy` just to insert secondary work.
- For JSON/API endpoints, use DRF `Response` or Django `JsonResponse`; do not introduce raw `HttpResponse` for JSON responses.
- In DRF write endpoints, prefer `serializer.is_valid(raise_exception=True)` so invalid payloads return structured 4xx responses.
- For DRF write methods, add the repo's `@has_auth_permission(...)` decorator by default. If the intended permission boundary is still "allow all authenticated/entity-authorized users", use the empty decorator form instead of omitting the permission hook entirely.
- If model validation (`full_clean()`) can raise Django `ValidationError`, convert it to DRF `serializers.ValidationError` at the serializer/view boundary.
- In DRF endpoints, do not add redundant `transaction.atomic()` wrappers when request-level atomic transactions are already enabled in local settings or existing app configuration.
- Avoid blanket `except Exception` in API write flows. Catch expected exception types; if a broad catch is unavoidable, log context and re-raise unknown exceptions.
- For attachment/file type transitions, authorize against the target operation or target type unless the requirement explicitly calls for checking both.
- Do not remove defensive error handling around secondary processing unless that secondary failure is intended to fail the primary request too.

## UI And Template Rules

- Treat the current UI as the design source of truth for frontend work. Inspect nearby templates, CSS/theme files, static JS, and comparable screens before changing UI.
- Preserve the existing product design principle and visual language. Reuse existing color variables, palette, semantic states, spacing, border radius, typography, tables, forms, buttons, modals, tabs, cards, badges, empty/loading/error states, and responsive behavior.
- Reuse existing UI libraries, helpers, icon patterns, and JavaScript patterns before creating anything new.
- Do not add a new UI library, CSS framework, icon set, font, palette, animation library, bundler, or one-off visual system unless the task explicitly requires it and the handoff calls it out.
- Preserve accessibility: labels, focus states, keyboard access, contrast, readable errors, non-overlapping text, and stable mobile/desktop layouts.
- Preserve saved state, not just display state. Trace form values, filters, tabs, selections, loading/error state, storage-backed state, refresh behavior, and save payloads when UI changes can affect persistence.
- Never hardcode internal endpoints in templates; use Django `{% url %}` tags.
- Prefer Tailwind utility classes over ad-hoc CSS or inline styling.
- Reuse existing UI helpers and components before adding new ones.
- Use the project's established UI libraries when they apply. In Critical Path templates, prefer DaisyUI components/utilities for supported UI affordances such as tooltips, buttons, badges, modals, dropdowns, tabs, and loading states instead of native browser-only behavior, ad-hoc CSS, or custom markup. For other project-standard libraries, follow the same rule: use the local library/pattern consistently before inventing a one-off implementation.
- Before shipping UI changes, run a consistency pass against nearby platform examples: primary/secondary/destructive button styling, button sizes, colors, icon family, badges, spacing, disabled states, hover/focus states, and copy style. Fix inconsistencies or explicitly report why the new UI intentionally differs.
- Before reusing an existing UI action for a new workflow, inspect and state the action's current product meaning, side effects, and user-facing copy. If the requested workflow has a different meaning or object of action, do not overload the existing button; preserve the old action and add a separate control that matches the relevant local pattern.
- When a requested UI appears awkward, hard to understand, difficult to navigate, visually inconsistent, or likely to confuse a real user, stop and ask a PM-facing question or push back with a concrete alternative. Do not implement a poor UX silently just because it was requested.
- For user-facing actions, match color semantics already used in the platform: neutral/black for primary save/navigation actions, green/success for positive completion/approval actions, red/error for destructive or issue/error actions, and outline/white for secondary actions unless the local pattern says otherwise.
- When a task is driven by an Excel sheet, mockup, screenshot, or other visual reference, implement the visible wording, section order, table shape, and labels exactly as the mockup unless the user explicitly approves a deviation. Do not add explanatory labels, helper text, headings, placeholders, or extra UI copy that is not present in the mockup.
- When a mockup shows user metadata as `User (Brand)` or `User (Factory)`, treat `Brand`/`Factory` as an entity placeholder unless the requirement explicitly asks for the literal entity type. Display the actual entity name (for example the brand or factory name) and match the mockup separator style; do not leave generic `Brand`/`Factory` labels or add brackets if the platform/mockup uses dot or pipe separators.
- Fixes must be system-wide where relevant, not only one page/card if the same logic exists elsewhere.
- Avoid duplicate logic paths for the same behavior; keep one source of truth.
- Prefer DB-level operations (`count()`, `annotate()`, aggregates) over loading records and computing in Python.
- Prefer incremental UI recalculation over full-table/full-page recompute.
- Never interpolate unsanitized user-controlled strings into HTML.
- For floating UI positioned from `getBoundingClientRect()`, account for scroll offsets and clamp within visible bounds.
- For shared UI components used by multiple actions, keep behavior-specific constraints explicit and per-action.
- Preserve existing role-specific branches and request payload semantics; do not widen conditions or add hidden/default values unless explicitly required.
- For page-level `can_edit` or similar UI gating on brand/factory screens, keep the check aligned with the same entity permission helper used by the API so superusers and role-based permissions stay consistent.
- Do not add fallback defaults that hide missing business data unless the product explicitly wants a fallback.
- Before modifying a shared icon, template partial, or reusable component, inspect current usages and keep existing contexts working.
- If UI/UX behavior moves to a new page/flow, remove the superseded path in the same change.
- For tabbed pages with shared filters, place shared controls in the common header and apply them consistently across relevant tabs.
- Prefer the project icon system when available (Lucide in base templates) instead of introducing new inline SVG markup.

## Reviews And Handoff

- Before implementing any significant technical approach, endpoint split, permission design, or business-logic mapping, restate the decision and ask for confirmation. Do not proceed on assumptions.
- For PR review workflows, treat unresolved review threads as the source of truth and separate actionable threads from informational comments.
- For PR review workflows on an open PR, make code changes on the existing PR head branch, not on a new child/review/dedicated branch, unless the user explicitly asks for a separate branch.
- For PR review workflows on an open PR, fetch and merge latest `origin/dev` into that PR branch before addressing review comments, and fix merge conflicts there before continuing.
- Treat repeated reviewer conventions as project conventions. If the same API/review rule shows up across comments or PRs, encode it here before the next implementation.
- When a review comment points to a repeated local pattern, search the touched flow and branch diff for equivalent cases before stopping at the reviewed line. Group those equivalent fixes together in the update back to the user.
- For review fixes, list every unresolved review comment and map each one to `fixed`, `already addressed/outdated`, or `blocked`, with the exact change made.
- For each review fix, include a reproducible verification note: what to trigger, expected outcome, and which command/check was run.
- For each changed file, include a line-by-line or block-by-block walkthrough of what changed, which function/class/migration it lives in, why that code exists, and how it supports the acceptance criteria or review comment being addressed.
- When explaining a change, cover both levels: PM-facing outcome first, then the technical path through the code (file, function, control flow, validation, persistence, and side effects) so the implementation can be reviewed without re-reading the full diff.
- In final `Technical notes` for bug fixes, explain the code in the same order the user/app flow runs instead of only following raw diff order. Include a clickable markdown link with the absolute file path and exact line number for each important step, for example `[apps/static/js/orders/order_bom.js](__HOME__/Desktop/code/critical-path-dj/apps/static/js/orders/order_bom.js:2245)`. Start from the user action, then follow the frontend handler, local state/cache changes, API request, backend validation/persistence, response handling, and final UI state.
- For critical-path bug explanations, map each high-level technical claim to the exact files/lines that make it true. Do not leave a sentence like "centralizes parsing" or "binds the handler reliably" unsupported. Under each claim, list the relevant clickable code paths in app-flow order and briefly state what each path contributes.
- Leave review threads unresolved by default after pushing fixes. Let the reviewer verify and resolve unless the user explicitly asks you to resolve them.
- If the user explicitly asks you to resolve review threads, do it only after the fix is committed, pushed, and the latest thread state confirms the issue is addressed.
- If multiple review threads report the same root issue, make one minimal fix and handle the equivalent threads together.
- Before declaring review complete, confirm the branch is clean and explicitly report thread status.
- At the end of implementation, include a plain-language feature summary that maps what was implemented to the original request or acceptance criteria.
- After every implementation, run a real-user QA pass before handoff whenever the changed behavior can be exercised through the product or API. Start the app locally when needed, use the same entry points a real user would use, perform the actual user action, and inspect the resulting product state. If the Browser plugin is available, read and follow `Browser:control-in-app-browser` and use the in-app Browser for localhost/UI verification, including clicks, typing, reloads, DOM/screenshot inspection, and full-page screenshots. Do not fall back to curl, server-rendered HTML checks, standalone Playwright, or a non-Browser tool for UI proof until the Browser plugin path has been tried or is concretely unavailable.
- For seed, default-data, import, synchronization, or migration changes that alter user-visible values, run the real local population path and verify the resulting UI; do not hand off based only on database rows, shell output, static inspection, or tests.
- Use Browser QA to look for bugs around the requested path, not only to prove the happy path. Check the role/session, visible copy, disabled/loading/error states, layout at relevant viewport sizes, accidental removals, console/runtime errors where accessible, and the final persisted or rendered state that a real user would rely on.
- In that PM-facing completion summary, always include how to run the app locally for manual verification and a step-by-step walkthrough a non-engineer can follow to test the implemented behavior.
- For every UI or product-visible change, capture the relevant before screenshot(s) before editing whenever the current UI can be opened locally. After implementation, capture matching after screenshot(s) from the same affected areas so reviewers can compare the exact visual/behavior change. Browser/product screenshots must be full-page captures by default, not cropped to only the changed component; add cropped detail shots only as supplemental proof or when the user explicitly asks for cropped screenshots. If before/after screenshots are blocked by local data, permissions, app startup, or an unreachable state, report the blocker explicitly instead of silently skipping them.
- After capturing before/after screenshots, compare them deliberately before handoff. State the exact visual diff in plain language: what appeared, disappeared, moved, changed copy/style/state, or stayed intentionally unchanged. Do not rely on memory or assume the implementation is correct just because the target element appears; scan the surrounding UI for accidental removals, layout shifts, hidden controls, missing buttons, changed labels, and inconsistent spacing.
- At the end of every implementation, include screenshot evidence of the implemented result whenever it can be shown in the product.
- If the acceptance criteria span a UI flow, the screenshot proof must cover the full flow, not just the end state. Include the minimum set of screenshots needed to show each required step, user action, success state, and validation or error state.
- When sharing screenshot proof with the user, embed each screenshot inline in the chat using Markdown image syntax with an absolute local file path, for example `![Setup tab](/absolute/path/setup.png)`. Do not provide screenshot paths as plain text in place of inline images unless the user explicitly asks for paths only.
- Put a brief plain-language note before or after each inline screenshot explaining what it proves. Do not include Playwright code, UI-test code, capture scripts, curl commands, or other automation/code artifacts unless the user explicitly asks for that code.
- If any required UI step cannot be shown because of local data, permissions, or setup limits, say so explicitly and describe the missing proof instead of claiming full end-to-end screenshot coverage.
- When creating a pull request, default the PR description to only what was done, in plain language, unless the user explicitly requests different content. Keep it code-free unless the user explicitly asks for code in the description.
- After `gh pr create` or `gh pr edit`, verify the live PR body with `gh pr view --json body` and immediately patch out any AI/editor/tool branding lines before handing the PR to the user.
