---
name: engineering-quality-loop
description: Research, implement, independently review, and repair engineering work against an evidence-backed 9/10 quality gate. Use for iterative implementation and review requests, quality loops, or substantial changes needing this cycle. Use findings-only mode for read-only reviews.
---

# Engineering Quality Loop

Deliver the requested behavior with credible evidence. A score summarizes engineering judgment; it never substitutes for a working implementation or grants release permission.

**Never create or amend a Git commit unless the user explicitly asks for that commit action.** Implementing, fixing, validating, completing the task, or passing the quality gate does not authorize a commit. Otherwise leave changes uncommitted. This rule applies to the lead and every subagent; include it in delegated task instructions.

## Start with the real task

1. Read the current request, accessible brief, applicable project instructions, current diff, and affected callers. Preserve unrelated work. Before any writer starts, capture a Git baseline or hash/content snapshot for files the task requires to stay unchanged; a post-implementation fingerprint cannot prove preservation. Choose the actual task base for Git review, including relevant commits, staged/unstaged changes, and new files.
2. Map every explicit requirement to a stable acceptance ID and observable check. State risk, important invariants, and material unknowns. Research only uncertainties that affect a decision; use current primary documentation for external APIs/dependencies. Reuse verified repository patterns and database-owned names.
3. Keep the current lead/model unless the user requests a switch. Delegate bounded work using [routing.md](references/routing.md). This skill requests one independent reviewer subagent for an implementation quality loop; use another worker only when that saves useful work. A reviewer must not have authored any candidate in this task. High-risk work requires a second distinct security/reliability specialist in addition to the senior reviewer. Use a fresh context with requirements, code, and raw evidence, without author self-scores, prior numeric grades, or suggested conclusions.

For an audit/review-only request, perform research and checks and report findings; do not repair or install anything. For implementation, follow existing authorization without extra design approval. Project test policy governs test changes. Do not turn this skill into authority for production stress, paid services, deployments, commits, pushes, sharing, or data mutations outside the request.

## Implement, check, review, repair

1. **Implement:** assign one writer ownership of the relevant files. Explain the acceptance checks and what must remain true. Other agents are in the workspace: never revert their work. Challenge unnecessary code and fragile assumptions; delete before simplifying. Small tasks can be implemented by the lead and reviewed once.
2. **Freeze:** stop writes to the candidate while checking/reviewing. Record the source fingerprint and author identities with the helper below. Keep evidence outside the source tree. Include relevant ignored inputs explicitly. A changed candidate needs new evidence; do not claim old checks cover a new version.
3. **Exercise the behavior:** use meaningful existing tests, targeted commands, real browser/API/persistence checks, negative cases, and bounded failure/concurrency stress where risk warrants it. Inspect actual assertions and test discovery: exit zero with zero tests is not proof. Ask whether a plausible wrong implementation would pass. Tests, mocks, and screenshots must exercise the claimed behavior. Reuse passing evidence while its code and runtime assumptions remain valid.
4. **Review:** use a new reviewer context for each scored candidate. An earlier reviewer may verify finding closure, but must not supply the next blind grade from its existing scored context. Send the frozen code, original acceptance plan, protected-file baseline and comparison evidence, command records/observations, and prior finding identities (with numeric scores removed) to the independent reviewer. Read [review.md](references/review.md). Trace input → authorization/validation → state → side effects → output. Cover correctness, real verification, security, failure handling, resources, and simplicity. Judge UX, DX, and AX through concrete outcomes. Report defects with reproducible triggers, evidence, impact, and a verification target, not speculative redesigns.
5. **Gate:** the independent reviewer supplies the scorecard. Run the helper to validate evidence, freshness, acceptance coverage, identity declarations, finding continuity, and score arithmetic. A weighted score ≥9.0 and dimension floors are necessary; missing evidence, failed checks, stale code, open must-fix/high/critical findings, or unavailable independent review prevent PASS.
6. **Repair:** return confirmed findings to the writer with stable IDs and explicit checks. Carry every finding into the next candidate; resolved/dismissed findings need evidence and rationale. Challenge mistaken findings with evidence. Reopen regressions. Never raise scores merely because a round passed. Review the final integrated candidate after repairs.

## Bound the loop

Defaults: initial candidate plus up to three repairs, 60 minutes, at most two concurrent subagents excluding the lead, one writer, no recursive delegation. Record the host-clock start time and deadline before delegation, and announce the limits; an explicit user budget takes precedence. Check the clock before each dispatch, repair, and wait. Bound waits by the remaining time. At the deadline, interrupt outstanding agents where supported and report BLOCKED with retained evidence; do not quietly extend the budget or start another repair. Apply an explicitly authorized extension to the deadline and state it. Stop if two successive candidates resolve no material finding and add no needed evidence. Do not spend cycles escalating missing credentials or permissions through stronger models. These are workflow limits, not a monetary spending cap.

Use `PASS`, `NEEDS_REPAIR`, or `BLOCKED` accurately. At a limit, preserve the best verified candidate and report remaining work; never weaken the gate to finish. A disabled/missing reviewer blocks independent certification, but useful authorized implementation and checks can continue.

## Evidence tooling

Use Python 3.9+ with Git on macOS/Linux and the standard-library helper at `scripts/quality.py`. Read [evidence.md](references/evidence.md) when beginning recorded validation; it defines the plan, commands, observations, and reviewer JSON. The helper supports Git and plain source folders and rejects unsupported filesystem inputs rather than silently ignoring them.

The helper verifies consistency, not truth or tamper resistance. Operator-entered observations and reviewer identities are declarations. The lead must verify actual agent/tool activity, inspect supporting artifacts, and disclose unverified runtime inputs. Do not describe this as a protected CI or security enforcement system.

## Handoff

Lead with what works and the gate result. Briefly state meaningful checks, resolved findings, remaining limitations, and one next action. Link the evidence directory and changed files. For Git worktree implementation, honor the user's local Codiff review requirement when available; it supplements checks. Keep the user's output style. Do not create another report, framework, dependency, or diagram unless it improves this handoff.
