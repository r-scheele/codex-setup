# Model routing

Choose the least expensive adequate model for the judgment required. These are local workflow defaults, not a benchmark or price guarantee. Inspect callable tools and supported model/effort values; never invent a role or silently substitute a model. Record requested versus observed model and actual agent ID. Report when the host cannot verify model selection.

| Assignment | Preferred model | Effort |
|---|---|---|
| Focused repo/doc lookup | gpt-5.6-luna | low |
| Specified implementation or repair | gpt-5.6-luna | medium |
| Ordinary integration | gpt-5.6-terra | medium |
| Difficult diagnosis or implementation | gpt-5.6-sol | high |
| Independent senior review | gpt-5.6-sol | high |
| High-risk authorization, data integrity, payment, infrastructure review | gpt-6-astra | high |

Use the current lead; Sol medium is a suggested choice for a new substantial task, not permission to change settings. Start hard tasks at the appropriate tier rather than failing through every cheaper model. One evidence-guided repair per worker before reconsidering the assignment/tier. For high-risk work, use a second distinct specialist with an explicit security/reliability question alongside the senior reviewer. Run sequentially if the two-subagent limit would otherwise be exceeded. Both must finish before PASS; record both identities and findings.

Installed custom roles are `quality_scout`, `quality_worker`, `quality_builder`, `quality_expert`, `quality_reviewer`, and `quality_senior`. If these are absent from the active tool schema, use its supported generic role with explicit model/effort. When the schema allows model overrides only on fresh/partial forks, use a fresh context (`fork_turns="none"` in the current collaboration interface). Do not pretend text inside a worker prompt changes its model. Do not fork an author's history into an independent reviewer.

Give workers: objective, verified selected worktree absolute path and branch, actual base/diff scope, owned files, constraints, acceptance IDs, planned checks, existing findings, and result/evidence location. State that they are not alone and must preserve others' work. Reviewers may write review artifacts only, outside the candidate. Agents must not spawn children or create additional worktrees/branches. Verify commands and edits target the assigned selected worktree; do not use the original checkout. Never create or amend commits unless the user explicitly requests that commit action; creating/updating a PR does not grant commit permission. For UI tasks, assign real screenshot capture to the appropriate worker/lead and provide those artifacts to reviewers. Return compact findings and evidence paths, not raw logs.

Efficiency: for a small low-risk change, the lead writes and one fresh reviewer reviews. Avoid separate scout/worker dispatches unless they save useful work. Subagents inherit the active loop and do not launch another one. Send only relevant raw evidence and prior findings, reuse unchanged checks, and stop on the first valid PASS.

Budget accounting: track candidate number, elapsed minutes, active agents, repairs and known usage. Unknown token/cost usage stays unknown. Do not poll continuously or rerun checks with unchanged inputs.

Current official references (verified 2026-09-10):
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/build-skills

Models/efforts were also checked against the local desktop model catalog. Availability may change; runtime tool schemas take precedence. No global model, permission, or concurrency setting is required for this skill; limits are applied to this workflow.
