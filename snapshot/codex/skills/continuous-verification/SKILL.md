---
name: continuous-verification
description: Verify a code change when no project-specific verification skill applies. Scale checks to the requested behavior and risk.
---

# Verify the Requested Change

Use this fallback only when no project verification workflow applies. Follow the active repository’s test restrictions, authorization boundaries, and acceptance criteria.

Identify the affected behavior and the smallest meaningful check before editing. Reuse existing implementation and tests. Verify changed wiring, callers, ownership, persistence, and error behavior when relevant. Add a test only when permitted and it proves meaningful behavior not already covered.

Before handoff, compare the result with the request, review the focused diff, and run appropriate checks. Reuse passing evidence unless later edits or new failures invalidate it. Report exact unverified cases; do not claim completion for missing requirements, and continue independent work when one check is blocked.
