---
name: seamstream-pr-hygiene
description: 'Inspect or update a SeamstreamAI PR when requested: isolate review comments, resolve conflicts, and preserve remote-action permissions.'
---

# SeamstreamAI PR Maintenance

Read `seamstream-guidelines` once for shared domain, workspace, authorization, and verification policy. Use the active checkout’s applicable AGENTS.md and only relevant domain references. If the companion skill is unavailable, continue from the checkout’s instructions and report a missing rule only if it prevents a safe decision.

Resolve the exact PR, head/base, task scope, and requested action. Read current review comments and distinguish unresolved task-related findings from obsolete or unrelated discussion. For review-only/status requests, inspect without editing branches, source, or PR state.

For authorized fixes, use the existing PR head branch and the project workspace rules; preserve unrelated changes. Use `seamstream-bug-fix` for diagnosis when needed, then reuse its verification. Fetch/merge the base only for the project’s authorized update workflow, not to answer a read-only review. Preserve normal merge behavior and migration dependency/order rules.

Commit, push, retarget, merge, close, resolve threads, or delete branches only when the specific action is authorized. A request for a local fix or prepared PR does not authorize publishing. Leave review threads unresolved unless asked to resolve them after verified fixes.

Report requested comments as fixed, already addressed, or blocked with concise evidence. Use a plain-language PR description limited to what changed and relevant validation, unless the user requests a different format. Verify remote state after an authorized remote change.
