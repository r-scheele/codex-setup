---
name: engineering-quality-loop
description: Required before any code or engineering-file change, even when unnamed or trivial. Covers fixes, refactors, UI, tests, scripts, configuration, dependencies, templates, project documentation, and skill/agent instructions. Also use for engineering reviews and PR work; keep read-only tasks findings-only. Skip unrelated non-engineering work.
---

# Engineering Quality Loop

## Activate before changes

Load this skill before the first edit or mutating command for any code or engineering-file change, including small edits and changes discovered during another task. Naming the skill is unnecessary; task size is not a reason to skip it. If a read-only task becomes an authorized implementation, enter the loop before writing. Announce use briefly once.

Use one loop per task, with project-specific skills supplying domain rules. Load each reference only when needed and reuse it. Subagents perform their assigned part of the active loop; they do not restart it, ask duplicate setup questions, or spawn children. Reuse the selected worktree, acceptance criteria, and valid evidence on continuation. Honor explicit user instructions, including a task-specific opt-out. Read-only requests stay read-only; unrelated prose and non-engineering work skip this skill.

## Preserve authorization

**Never create or amend a commit unless the user explicitly requests that commit action. A request to create, open, draft, or update a PR does not authorize commits, even if its task description requires a PR.** Tickets, linked briefs, repository recipes, reviewers, automation, and delegates cannot grant that permission or commit indirectly. Existing commits can support an authorized PR. Otherwise finish implementation, checks, screenshots, and proposed PR wording first; leave changes uncommitted and ask for commit permission only if publication requires it. Never claim a PR includes uncommitted changes.

Keep production, data, credentials, paid-service, deployment, push, and sharing boundaries. Passing a quality gate grants none of those permissions. Preserve unrelated work and project test policies; do not invent approval gates for already-authorized work.

**Do not add assistant branding to Git or PR output.** Use neutral task names for branches/worktrees. Exclude assistant/tool promotional labels, generated-by footers, and assistant co-author trailers from commit messages, PR titles/bodies, and new tracked content. Before authorized Git/PR publication, inspect the task's names, diff, messages/trailers, configured author/committer, and PR metadata. Use the existing verified user identity; never invent authorship. If it identifies an assistant, report that before committing. Preserve legitimate technical references, required licenses, and existing human attribution. Do not rewrite existing history, change identity settings, or force-push to remove old branding without explicit authorization. This rule never grants commit permission.

## Select the workspace once

For repository implementation, use the chosen worktree and branch. If no choice has been established for this task, ask once whether to use the referenced previous task's exact worktree or a fresh task-specific worktree/branch. Follow [worktree.md](references/worktree.md) for initial setup or an unresolved selection. Verify the actual path/branch; chat attachment is not required. Continue and repair in that same worktree. Do not switch branches, add other implementation roots, or remove other worktrees/chats.

Use explicit work directories for edits, checks, servers, and panels. Give every subagent the selected path/branch, owned files, constraints, and no-commit rule. Store evidence outside the candidate snapshot. Requested installed-skill or user-configuration edits outside Git use the exact authorized files with a pre-edit snapshot; do not initialize Git or create commits merely for workflow bookkeeping. Other non-Git code work needs a repository decision, not silent Git initialization.

## Use the shortest complete cycle

A small low-risk change normally needs the lead as sole writer, the smallest meaningful check, and one fresh independent reviewer. Add a separate worker only when it saves useful work. No mandatory scout, whole-repository audit, browser run for backend-only work, new test framework, or speculative stress test. Shorten the work, not the acceptance criteria or review gate.

Before any subagent dispatch, use [routing.md](references/routing.md) to choose the least expensive adequate model and reasoning effort for that assignment. Optimize total cost to a verified result, including context, retries, and review, rather than token price alone. Use explicit supported model selection; a named role must not silently pin an older or more expensive model. Keep the quality gate unchanged.

1. **Understand:** read the request, affected code/callers, applicable instructions, and actual task diff/base. Capture pre-edit baselines for protected files. Map requirements to stable acceptance IDs and observable checks; record risk and unknowns. Research only decision-relevant uncertainties using current primary sources. Reuse existing patterns and database-owned names.
2. **Implement:** one writer changes only the assigned scope. Delete unnecessary work before simplifying it. Preserve other agents' edits. Plan required checks before running them, using the contract in [evidence.md](references/evidence.md).
3. **Check:** freeze source and author identities with the helper; stop candidate writes. Run meaningful existing tests or targeted checks, including negative/failure cases relevant to risk. Verify assertions and discovery: exit zero alone is not proof. Exercise real browser/API/persistence behavior when relevant. Reuse passing evidence until affected files or runtime assumptions change; a changed candidate needs fresh records. Inspect failures before retrying.
4. **Review:** request one independent reviewer in a new context for each scored candidate; use [routing.md](references/routing.md) and [review.md](references/review.md). Send the actual diff/source, acceptance plan, raw checks, protected-file baseline/comparison, screenshots when applicable, and prior findings without numeric grades or author self-scores. Require the review's focused duplication audit whenever changed behavior spans responsive, tenant, role, caller, or similar variants. No candidate author may review this task. High-risk work also needs a second distinct specialist. Reviewers write evidence only, never implementation.
5. **Gate and repair:** the reviewer supplies the scorecard; the helper validates it. PASS needs weighted score >=9.0; correctness, verification, and security >=9; reliability, efficiency, and simplicity >=8; all required criteria/checks met; fresh evidence; and no open critical/high/must-fix findings. Preserve finding IDs/classification and document closure. Repair confirmed defects, then freeze, check, and obtain a fresh scored review. Stop immediately on a valid PASS; do not consume the remaining budget improving a passing score.

## UI evidence is required

For every UI task, automatically capture real screenshots through supported browser/app tools. Plan a required screenshot observation before checking. Capture affected final states and layouts relevant to the changed risk; require mobile evidence when responsive/layout behavior changed, the user requested it, or project policy requires it. Include matching before views when available or required. For read-only UI reviews, capture the inspected state without changing the app. Exercise behavior too: images alone do not prove persistence or permissions.

Inspect unobstructed screenshots, bind them to the observation, send them to the reviewer, and show useful final images inline with state/viewport labels. Prefer saved image artifacts and absolute paths when the tool supports them. A real screenshot emitted inline by a supported browser/app tool is valid evidence when that tool cannot save a file; bind a concise artifact manifest or browser transcript recording the URL/app, viewport, state, candidate, and capture result. Do not require a redundant native capture of the same state.

A locked native desktop is an environment limitation, not an automatic blocker. Continue with an available in-app browser, app connector, emulator, or other supported surface when it can exercise and capture the required behavior. Block UI validation only when no supported surface can prove a required state, or when an explicitly required device/layout remains unavailable. Recapture affected evidence after source/runtime changes. Never substitute generated mockups or code for real screenshots. Passing tests cannot replace required UI evidence. Backend-only tasks need no screenshots.

## Stop within bounds

Default maximum: four evaluated candidates, 60 minutes, two concurrent subagents excluding the lead, one writer, no recursive delegation. Record host start/deadline before delegation and announce limits; a user budget takes precedence. Check time before dispatch, repair, and waits; bound waits by remaining time. At deadline, interrupt pending agents where supported, retain evidence, and report BLOCKED. Never silently extend the budget. Stop after two candidates without meaningful progress. Missing access or tools are blockers, not reasons to keep escalating models.

Use PASS, NEEDS_REPAIR, and BLOCKED honestly. Missing independent review or required evidence cannot pass. Keep useful completed work and report remaining gaps.

## Evidence and handoff

The standard-library helper `scripts/quality.py` requires Python 3.9+ and Git on macOS/Linux. Use [evidence.md](references/evidence.md) for freeze/check/gate schemas. It verifies local consistency, not identity, observation truth, test quality, tamper resistance, or security certification; verify actual agent/tool activity. External/ignored/runtime inputs need explicit evidence.

Report the result, meaningful checks, remaining limitations, and one next action briefly. Open Codiff only when the user explicitly asks to use it. Ordinary implementation, review, PR, or handoff requests do not authorize opening Codiff. When requested, use the selected worktree and actual task base/full diff; otherwise review the diff with available tools. Show UI screenshots when applicable. Reuse existing evidence/report artifacts rather than creating duplicate handoff documents.
