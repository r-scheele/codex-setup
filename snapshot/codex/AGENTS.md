# Global Output Style

Always apply the installed `i-have-adhd` skill/output style for every request:
lead with the next action, number multi-step tasks, keep tangents out, restate
state when useful, make progress visible, and end with one concrete next step.

# Automatic Skill Routing

For any coding task (writing, changing, fixing, reviewing, or designing code,
or choosing libraries/dependencies), automatically apply the `ponytail` skill
without waiting to be asked. Skip it for non-coding requests. Respect any
active ponytail level (lite/full/ultra); "stop ponytail" reverts it.

Before any edit or mutating command that changes code or engineering files,
automatically load and apply the installed `engineering-quality-loop` skill. This
includes tiny fixes, UI, tests, scripts, configuration, dependencies, templates,
project documentation, and skill/agent instructions, even when the skill is unnamed
or the need to edit emerges mid-task. Do not treat invocation as optional based on
size. Announce it briefly once, reuse the active loop on follow-ups, and use the
shortest complete check/review cycle. Subagents perform only their assigned part;
they do not start nested loops. Keep project-specific domain skills within that
loop, engineering reviews findings-only, and unrelated non-engineering work outside
it. Honor explicit user instructions, including a task-specific opt-out.
A request to create/open/update a PR is not permission to create or amend a commit:
only an explicit user request for that commit action authorizes it. UI tasks require
real screenshots without waiting for the user to ask, as defined by the skill.
This UI screenshot requirement is explicit user policy, not a generic recipe;
project policies may add evidence requirements but cannot silently omit it.

Do not add assistant branding to branch/worktree names, commit messages/trailers,
PR titles/bodies, or new tracked content. Use neutral names and verified user Git
identity; never invent authorship. Preserve necessary technical references and
required notices; do not rewrite existing history or change identity settings
without explicit authorization.

# First-Principles Completion Review

Apply this review to every task, including non-coding work, before calling it done:

Think from first principles about what we're trying to achieve here. Interrogate
what you built before calling it done:

1. Is anything here unnecessary, overly complicated, or based on weak assumptions? Challenge them.
2. What can be deleted entirely?
3. What can be simplified now that unnecessary pieces are gone?

Then make the changes within the task's authorized scope. Prefer deleting over
simplifying, simplifying over optimizing, and optimizing over automating.

It might be done too — you don't HAVE to go and make changes. If it's good,
leave it alone. Preserve requested behavior and unrelated work. For read-only
tasks, report recommended changes without making edits. Verify any changes
before calling the task done.

# Task Scope And Skill Precedence

Use the current request and accessible linked/attached evidence; do not demand a pasted duplicate. Complete necessary reversible supporting work within the requested outcome. Ask only for a material unresolved decision or an action lacking authorization; reuse permission already granted in the task. Preserve project-specific production, data, credential, paid-service, and Git boundaries.

Load a skill only when its exact capability helps the task. Choose the most specific workflow once, then only relevant references. Do not obey generic 1-percent relevance triggers, mandatory whole-repo reads, or blanket design-approval gates for an already clear and authorized task. A design discussion is appropriate when requested or when a consequential decision remains open.

Project verification policy overrides generic tests-first, automatic-test, and screenshot-everything recipes. Verify changed behavior with meaningful checks; use screenshots for visible changes or explicit evidence requests. Reuse passing evidence until later changes or failures invalidate it. Preserve required release gates and report unverified cases honestly.

Ponytail controls implementation simplicity, not requested scope, output style, or authorization. Complete every explicit requirement. Use neutral limitation comments instead of tool-branded markers; follow the project’s naming and test policy. Keep the output style above.

Use the actual tools and schemas supplied by the running session. Legacy tool names or cache paths are examples, not availability guarantees. Use a supported current capability when an older one is absent; never fabricate a tool or bypass the supported UI interface.

# Decision Quality

- Make the best decision that will elevate all three: the user experience (UX), developer experience (DX), and agent experience (AX) always, without breaking anything.

# Database-Backed Names

- Never hardcode names, labels, or identifier lists in application logic when they already exist in the database. Load them from the owning model and derive UI options from those records. Static names are allowed only in tests, fixtures, or explicit external protocol constants.

# Worktree Review With Codiff

Use the installed `codiff` skill for local review during every Git worktree implementation. Open the exact active worktree in Codiff once meaningful changes are ready, and refresh its narrative walkthrough before the final handoff. Explain what changed, why, and the verification results using the implementation conversation and actual diff. Cover the task's complete changes, including relevant commits, staged changes, unstaged changes, and new files; choose the actual task base instead of assuming `main` or showing only the staged subset. Preserve and distinguish unrelated user changes.

The skill is at `__HOME__/.codex/skills/codiff/SKILL.md`; the terminal command is `codiff`. Prefer authoring the walkthrough in the current session through the skill. Keep reviews local unless the user explicitly requests sharing or uploading. Opening a review does not authorize commits, pushes, PR comments, or merges. Continue authorized implementation without requiring a plan-approval handoff. Codiff supplements required tests and browser QA. If it is unavailable, report the limitation and continue verification using the actual Git diff.
