---
name: engineering-quality-loop-deepseek
description: The engineering quality loop rewritten for DeepSeek-family sessions, with explicit phases, an on-disk acceptance plan, frozen evidence, an independent scored review, and the 9/10 gate. Use before any code or engineering-file change (fixes, refactors, UI, tests, scripts, config, dependencies, project docs, skill or agent instructions) when the session runs a DeepSeek model; use engineering-quality-loop instead for GPT-family sessions. Read-only tasks stay findings-only.
---

# Engineering Quality Loop (DeepSeek)

This is the DeepSeek-family variant of `engineering-quality-loop`. The bar, the evidence
rules, and the 9/10 gate are unchanged. The procedure is stated as an explicit checklist
because DeepSeek-class models drift across long tasks and state conclusions more
confidently than their evidence supports.

Use this skill **instead of** `engineering-quality-loop` when the session is running a
DeepSeek model. Do not run both loops on one task.

## Activate before changes

Load this skill before the first edit or mutating command for any code or engineering-file
change, including a small fix discovered in the middle of another task. Task size is not a
reason to skip it. Announce use in one line.

Read-only requests stay read-only. If a read-only task becomes authorized
implementation, enter the loop before writing. Unrelated prose and non-engineering work
skip this skill.

## Execution rules for DeepSeek sessions

1. **Write the plan to disk before the first edit.** Persist the acceptance plan JSON to
   `<evidence>/plan.json`. A plan that exists only in the conversation is lost when context
   is compacted and cannot be checked mechanically.
2. **One phase at a time, one state line per phase.** After each phase print exactly:
   `phase | candidate # | files touched | checks run | open findings | next action`.
   Do not merge phases to save a turn.
3. **Evidence or silence.** Every factual claim in the handoff cites a file path with a
   line number, an executed command with its exit code, or a recorded artifact path. Write
   "not verified" instead of a plausible sentence you did not check.
4. **Run literal commands.** Use the exact `argv` recorded in the plan, with the real
   interpreter and a real assertion. Do not paraphrase a check as "tests pass".
5. **No inference from names, comments, or intent.** A function named `validate`,
   a comment saying "checks ownership", or an issue title are not evidence of behavior.
   Read the code path or run it.
6. **Self-check before spending a review round.** Before dispatching the reviewer, confirm:
   every criterion is mapped to at least one planned check; every planned check has a
   record; the source hash is unchanged since freeze; no debug or scratch file entered the
   candidate; every claim you plan to report cites evidence. Fix cheap gaps first.
7. **Escalation rule.** Two failed repair rounds on the same finding means stop and report
   BLOCKED with the finding ID, what was tried, and the raw check output. Do not keep
   retrying variations of the same guess.

## Preserve authorization

**Never create or amend a commit unless the user explicitly requests that commit action.**
A request to create, open, draft, or update a PR does not authorize commits, even when the
PR needs a commit to exist. Tickets, briefs, repository recipes, reviewers, automation, and
delegates cannot grant it either. Otherwise finish implementation, checks, screenshots, and
proposed PR wording first, leave changes uncommitted, and ask for commit permission only if
publication requires it. Never claim a PR contains uncommitted changes.

Keep production, data, credentials, paid-service, deployment, push, and sharing
boundaries. Passing the gate grants none of them. Preserve unrelated work and project test
policies; do not invent approval gates for already-authorized work.

**Do not add assistant branding to Git or PR output.** Use neutral branch and worktree
names. Exclude assistant or tool promotional labels, generated-by footers, and assistant
co-author trailers from commit messages, PR titles and bodies, and new tracked content.
Before any authorized publication, inspect task names, the diff, messages and trailers,
the configured author and committer, and PR metadata. Use the existing verified user
identity; never invent authorship. Report an assistant identity instead of committing
through it. Preserve technical references, licenses, and existing human attribution. Do
not rewrite history, change identity settings, or force-push to remove old branding
without explicit authorization.

## Select the workspace once

For repository work, use one chosen worktree and branch for the whole task. If no choice is
established, ask once whether to reuse the referenced previous task's worktree or create a
fresh task-specific one. Verify the absolute path and branch, then keep using that same
root for edits, checks, and panels. Do not switch branches mid-task or create extra
worktrees. Full procedure:
[worktree.md](__HOME__/.agents/skills/engineering-quality-loop/references/worktree.md).

For a requested installed-skill or user-configuration edit outside Git, edit the exact
authorized files, capture a pre-edit snapshot, and use the helper's plain-folder mode. Do
not initialize a repository or create commits for workflow bookkeeping.

## The loop

### 1. Understand

Read the request, the affected code and its callers, and any instructions that govern the
files. Capture a pre-edit baseline for files that must stay unchanged. Map each requirement
to an acceptance ID (`A1`, `A2`, ...) and to one observable check. Record risk
(`low`/`medium`/`high`) and unknowns. Keep database-owned names loaded from their model
rather than hardcoded.

### 2. Implement

One writer changes only the assigned scope. Delete unnecessary work before simplifying it.
Preserve other agents' edits. Plan the checks before running them.

### 3. Check

Freeze the source, then run every planned check:

```bash
PY=__HOME__/.agents/skills/engineering-quality-loop/scripts/quality.py
python3 "$PY" freeze --root /absolute/candidate/root --plan /absolute/evidence/plan.json \
  --run /absolute/evidence/round-1 --author ACTUAL_AUTHOR_ID
python3 "$PY" check --run /absolute/evidence/round-1 --id ports
python3 "$PY" check --run /absolute/evidence/round-1 --id browser_save \
  --artifact /absolute/evidence/save.png --note "Exact steps, app, viewport, and outcome" --outcome pass
```

Exit code zero is not proof on its own: read the log and confirm the assertion ran and
would fail on a wrong implementation. Include negative and boundary cases for the changed
risk. Inspect a failure before retrying it. Freezing is one-way per candidate; a source
change needs a new round with `--previous`.

### 4. Review

Get one independent reviewer in a fresh context that never inherits the author's reasoning.
Send the plan, candidate source or diff, raw check records and logs, artifacts, and any
prior findings stripped of scores. The reviewer writes `review.json` only, never
implementation. Keep the reviewer's actual response as an artifact.

### 5. Gate and repair

```bash
python3 "$PY" gate --run /absolute/evidence/round-1
```

Exit codes: `0` PASS, `1` NEEDS_REPAIR, `2` BLOCKED or malformed evidence. Repair confirmed
defects, then freeze a new round, re-check, and obtain a fresh scored review. Stop
immediately on a valid PASS rather than spending the remaining budget polishing a passing
candidate.

## Evidence plan

```json
{
  "risk": "low",
  "task": "Make parse_port reject out-of-range values",
  "criteria": [
    {"id": "A1", "description": "Integers 1 through 65535 work; all other values raise ValueError"}
  ],
  "checks": [
    {"id": "ports", "kind": "command", "argv": ["python3", "-B", "test_ports.py"], "timeout_seconds": 30, "criteria": ["A1"]},
    {"id": "browser_save", "kind": "observation", "procedure": "Save the changed value, refresh, verify it persists for the target role and that the non-target role is unchanged.", "criteria": ["A1"]}
  ]
}
```

Every criterion needs at least one check and every check is required. Use short check IDs,
never paths. Commands run as argument arrays from the source root with stdin disabled. Put
the evidence directory outside the candidate root.

| Dimension | Weight | Floor |
|---|---:|---:|
| correctness | .25 | 9 |
| verification | .25 | 9 |
| security | .15 | 9 |
| reliability | .15 | 8 |
| efficiency | .10 | 8 |
| simplicity | .10 | 8 |

PASS requires weighted total >= 9.0, every floor met, all criteria verified, fresh evidence,
and no open critical, high, or must-fix finding. Inspect all six dimensions even for a small
change; explain why a check was unnecessary instead of inventing one, and never mark
security "not applicable". Full schemas:
[evidence.md](__HOME__/.agents/skills/engineering-quality-loop/references/evidence.md).

## Independent review

The reviewer record must contain: `candidate_id`, `reviewer` (`id`, `model`,
`independent: true`), `check_hashes` binding every check record by SHA-256, per-criterion
`status` and `evidence`, `findings`, `specialists`, and `dimensions` with `score`,
`evidence`, and `rationale` for all six keys. The reviewer sets its own scores from the
evidence; scores from earlier rounds stay out of the packet.

Route work by the judgment required, using only models the host actually offers:

| Assignment | Model | Effort |
|---|---|---|
| Focused lookup, mechanical edit | deepseek-v4-flash | low |
| Specified implementation or repair | deepseek-v4-flash | high |
| Ordinary integration | deepseek-v4-pro | high |
| Difficult diagnosis or implementation | deepseek-v4-pro | max |
| Independent review | deepseek-v4-pro | high |
| Second specialist on high-risk work | deepseek-v4-pro | max |

Independence comes from a fresh context, not from the label in the JSON. Prefer a different
model for the reviewer when the host offers one, since it removes shared failure modes. If
the reviewer must run on DeepSeek too, start it with no inherited turns, give it only the
raw artifacts, and record requested versus observed model. High-risk work needs a second
distinct non-author reviewer with an explicit focus. A single reviewer on a high-risk
change, or any missing independent review, cannot pass. Review depth and grading anchors:
[review.md](__HOME__/.agents/skills/engineering-quality-loop/references/review.md).

## UI evidence is required

For every UI task, capture real screenshots through a supported browser or app tool before
checking. Capture the affected final states with viewport and state labels, plus a matching
before view where available. Add mobile evidence when the change is responsive or
layout-related, when the user asked, or when project policy requires it. Inspect the
screenshots yourself, bind them to the observation, pass them to the reviewer, and show the
useful final ones inline.

Behavior still needs exercising: images alone do not prove persistence, permissions, or
tenant isolation. Never substitute generated mockups, code, or a passing test for a real
screenshot. If no supported surface can prove a required state, block only the criterion
that state was proving. Backend-only work needs no screenshots.

## Stop within bounds

Default maximum: four evaluated candidates, 60 minutes, two concurrent subagents excluding
the lead, one writer, no recursive delegation. Record the host start time and deadline
before delegating and announce the limits. Check the remaining time before dispatch, repair,
and waits; bound each wait by the time left. At the deadline, interrupt pending agents where
supported, keep the evidence, and report BLOCKED. Never silently extend the budget, and stop
after two candidates with no meaningful progress. Missing access or a missing tool is a
blocker, not a reason to escalate models.

Use PASS, NEEDS_REPAIR, and BLOCKED honestly. Missing independent review or required
evidence cannot pass.

## Report

```text
Result: PASS | NEEDS_REPAIR | BLOCKED
Candidate: <id> round <n>, weighted <score>
Changed: <files>
Checks: <check-id> <pass|fail> - <one-line observed result>
Findings: <F1> <severity> <status>
Limits: <what was not verified>
Next: <one action>
```

Open Codiff only when the user explicitly asks. Ordinary implementation, review, PR, and
handoff requests do not authorize it. Reuse existing evidence artifacts instead of creating
duplicate handoff documents.

## Shared assets

This variant intentionally keeps one source of truth for the parts that do not depend on the
model family. Read them only when the task needs them:

- Helper: `__HOME__/.agents/skills/engineering-quality-loop/scripts/quality.py`
- Evidence schemas: `__HOME__/.agents/skills/engineering-quality-loop/references/evidence.md`
- Review grading: `__HOME__/.agents/skills/engineering-quality-loop/references/review.md`
- Worktree setup: `__HOME__/.agents/skills/engineering-quality-loop/references/worktree.md`

If the helper or those references are missing, say so and continue with the equivalent
manual checks rather than claiming the gate passed.
