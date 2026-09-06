---
name: seamstream-continuous-verification
description: Verify changed SeamstreamAI behavior and applicable tenant, persistence, API, and UI boundaries before handoff.
---

# SeamstreamAI Verification

Read `seamstream-guidelines` once for shared domain, workspace, authorization, and verification policy. Use the active checkout’s applicable AGENTS.md and only relevant domain references. If the companion skill is unavailable, continue from the checkout’s instructions and report a missing rule only if it prevents a safe decision.

Before editing, map the requested behavior to the smallest affected paths and identify a meaningful way to verify it. After meaningful changes, check wiring, ownership, state/persistence, and affected callers where relevant.

Run the smallest relevant existing Django check or test. Add or update meaningful regression coverage when changed behavior or risk warrants it; do not require tests for trivial edits. For UI changes verify the real user path, desktop/mobile behavior, saved state, and before/after screenshots when available. For routed data changes verify the affected tenant database and a relevant isolation boundary. Report unverified cases accurately. Broaden checks only when a new change, failure, or shared-code risk justifies it.

Before completion, compare the actual result with the request and review the focused diff for omissions, broken references, and unrelated changes. Reuse passing evidence until a subsequent change or new risk invalidates it. Do not launch a second generic verification workflow for the same checks.
