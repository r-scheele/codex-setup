---
name: flash-costing-continuous-verification
description: Verify changed Flash Costing behavior and applicable tenant, persistence, API, and UI boundaries before handoff.
---

# Flash Costing Verification

Read `flash-costing-guidelines` once for shared domain, workspace, authorization, and verification policy. Use the active checkout’s applicable AGENTS.md and only relevant domain references. If the companion skill is unavailable, continue from the checkout’s instructions and report a missing rule only if it prevents a safe decision.

Before editing, map the requested behavior to the smallest affected paths and identify a meaningful way to verify it. After meaningful changes, check wiring, ownership, state/persistence, and affected callers where relevant.

For behavioral, calculation, access, model/migration, API/service, pipeline, or bug-fix changes, run focused tests and add or update a regression test when existing coverage does not prove the change. Open Costing behavior follows the same rule. Do not add tests that mirror trivial implementation details. Data-only exports, configuration-only, branch-sync, and setup-only changes may use appropriate non-test checks. For UI changes, verify the real user path, saved payload/state, responsive behavior, and before/after full-page screenshots when available. Report missing evidence without claiming it passed.

Before completion, compare the actual result with the request and review the focused diff for omissions, broken references, and unrelated changes. Reuse passing evidence until a subsequent change or new risk invalidates it. Do not launch a second generic verification workflow for the same checks.
