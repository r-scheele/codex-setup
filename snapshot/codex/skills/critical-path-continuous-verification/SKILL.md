---
name: critical-path-continuous-verification
description: Verify changed Critical Path behavior and applicable tenant, persistence, API, and UI boundaries before handoff.
---

# Critical Path Verification

Read `critical-path-guidelines` once for shared domain, workspace, authorization, and verification policy. Use the active checkout’s applicable AGENTS.md and only relevant domain references. If the companion skill is unavailable, continue from the checkout’s instructions and report a missing rule only if it prevents a safe decision.

Before editing, map the requested behavior to the smallest affected paths and identify a meaningful way to verify it. After meaningful changes, check wiring, ownership, state/persistence, and affected callers where relevant.

Do not add or update automated tests unless the user explicitly overrides that project restriction. Use relevant existing checks and real product/API verification. For visible changes, capture matching full-page before/after evidence and verify affected target/non-target tenants, brand/factory roles, responsive states, and persistence. Backend-only work uses an appropriate existing command or API check. Report unavailable proof accurately; finish independent work without repeatedly asking for an evidence waiver. Repeat broader checks only for new failures, shared-code risk, or explicit acceptance criteria.

Before completion, compare the actual result with the request and review the focused diff for omissions, broken references, and unrelated changes. Reuse passing evidence until a subsequent change or new risk invalidates it. Do not launch a second generic verification workflow for the same checks.
