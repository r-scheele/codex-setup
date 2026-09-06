---
name: critical-path-pr-review
description: Review a Critical Path PR or local diff for concrete defects. Findings only unless the user requests fixes.
---

# Critical Path PR Review

This is a findings-only workflow unless fixes are explicitly requested. Do not edit source, merge a base branch, change PR state, resolve threads, commit, or push merely to review.

Read `critical-path-guidelines` once for shared domain, workspace, authorization, and verification policy. Use the active checkout’s applicable AGENTS.md and only relevant domain references. If the companion skill is unavailable, continue from the checkout’s instructions and report a missing rule only if it prevents a safe decision.

Resolve the PR/head/base from the supplied URL, number, branch, or current task context. Inspect the diff, relevant caller/domain behavior, and applicable acceptance criteria. Trace ownership, validation, persistence, migration ordering, external side effects, and UI state only where affected. Report concrete defects with severity, file/line evidence, trigger, impact, and a minimal fix direction. Avoid speculative style findings.

If nothing actionable is found, say so and identify material verification limits. Do not require a clean worktree when unrelated user edits are present.

When the user requests a reusable review prompt instead of a review, use `references/review_prompt.md` if present; do not begin reviewing or modifying a repository.
