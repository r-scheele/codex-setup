---
name: ticket-worker-orchestration
description: Split a large implementation into worker tickets with owned files, dependencies, acceptance criteria, and review gates.
---
# Ticket Worker Orchestration

## Overview

Convert broad product plans into isolated, reviewable work packets. Each ticket must have clear ownership, acceptance criteria, constraints, verification, and a final report format.

## Workflow

1. **Normalize the plan**
   - Extract product goal, milestones, non-goals, dependencies, and risky integration points.
   - Identify shared contracts or files that could cause collisions.

2. **Split by ownership**
   - Give each worker a disjoint file/module scope.
   - Make shared interfaces explicit before implementation begins.
   - State: the worker is not alone in the codebase and must not overwrite others' edits.

3. **Write each ticket**
   - Include workdir, branch/base if known, owned files, requirements, constraints, verification commands, and deliverable format.
   - Inherit the active project’s verification policy. Specify meaningful checks without imposing tests-first or new-test requirements that contradict it.
   - For review-only tasks, say “do not modify files.”

4. **Add review gates**
   - Create one spec-compliance review prompt per ticket.
   - Create one diff/code-quality review prompt after fixes.
   - Reviews must inspect actual diffs/files, not answer generally.

## Ticket template

```markdown
## Workdir
<absolute path>

## Ownership
You own only:
- <paths>

You are not alone in the codebase. Do not revert or overwrite others' edits.

## Requirements
- <acceptance criteria>

## Constraints
- <non-goals and forbidden files>

## Verification
- <commands/checks>

## Report format
- Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Files changed
- Tests run and results
- Risks or follow-up
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Splitting by vague theme | Split by owned files and integration boundaries. |
| Forgetting review prompts | Add spec and diff review gates for every ticket. |
| Letting workers touch shared files casually | Define shared contracts first or reserve them for integration. |
