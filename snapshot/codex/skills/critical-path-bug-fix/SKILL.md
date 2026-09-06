---
name: critical-path-bug-fix
description: Diagnose and fix a reported Critical Path defect from the request, linked issue, screenshot, logs, or failing behavior.
---

# Critical Path Bug Fix

Read `critical-path-guidelines` once for shared domain, workspace, authorization, and verification policy. Use the active checkout’s applicable AGENTS.md and only relevant domain references. If the companion skill is unavailable, continue from the checkout’s instructions and report a missing rule only if it prevents a safe decision.

1. Establish actual versus expected behavior from the current request, linked issue/comment, screenshot, log, or reproducible failure. Retrieve accessible sources rather than asking the user to paste them again.
2. Reproduce or trace the smallest relevant active path. Inspect callers and shared consumers before choosing the root-cause fix; do not mask missing data or configuration with a production fallback.
3. Make the smallest complete repair that preserves ownership, existing capabilities, and affected non-target behavior.
4. Verify the original failure and relevant regression boundaries using the shared project policy. Finish independent work when one check is blocked; clearly identify what remains unverified.

If evidence conflicts on a material product decision, explain the conflict and ask only about that decision while continuing independent investigation. Missing prose pasted into chat is not a blocker when the request is available elsewhere.

For UI work, inspect a comparable current screen and preserve its components, accessibility, saved state, and design system. Use actual product/browser proof for visible claims.

Handoff: state the outcome, why it changed, relevant verification, and concrete limitations. Include technical paths or screenshots when they help review the change. Do not pad the response with a fixed report template.
