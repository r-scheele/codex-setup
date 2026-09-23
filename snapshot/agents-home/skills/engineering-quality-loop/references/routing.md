# Model routing

Choose the least expensive adequate model for the judgment required, within the user's allowed model family. Keep this workflow's GPT defaults; a separately requested provider-specific workflow retains its own routing. Optimize the whole assignment's cost, including input/context, reasoning/output, retries, and review. These are starting defaults, not measured quality guarantees or a promise of the cheapest possible run.

Inspect the active delegation schema for callable models, efforts, role locks, and tools. Choose by risk, ambiguity, affected boundaries, and available checks, not file count or role title. Record the assignment, reason for the tier, requested model/effort, observed model (or explicitly unverified), and actual agent ID. Never invent an identifier or silently substitute a model.

| Assignment | Preferred model | Effort |
|---|---|---|
| Focused repo/doc lookup with a bounded question | gpt-6-luna | low |
| Specified implementation or repair with clear acceptance checks | gpt-6-luna | medium |
| Ordinary integration, ambiguous behavior, or several interacting modules | gpt-6-sol | medium |
| Difficult diagnosis, concurrency, or consequential cross-module design | gpt-6-sol | high |
| Independent review of a mechanical, low-risk change with decisive checks | gpt-6-luna | medium |
| Independent review requiring engineering judgment | gpt-6-sol | medium |
| Complex or high-risk independent senior review | gpt-6-sol | high |
| High-risk authorization, data integrity, payment, infrastructure review | gpt-6-astra | high |

Use the current lead; do not change its settings. Start hard tasks at the appropriate tier rather than failing through every cheaper model. For high-risk work, use a second distinct Astra specialist with an explicit security/reliability question alongside the Sol senior reviewer. Run sequentially if the two-subagent limit would otherwise be exceeded. Both must finish before PASS; record both identities and findings. The low-risk Luna review route still requires a fresh non-author context, all six dimensions, and the full gate.

Escalate only for an identified reasoning or capability gap: unresolved interacting requirements, an incorrect diagnosis, or a material missed case. Give a worker at most one evidence-guided repair before reassessing. Move Luna to Sol medium/high, or Sol to Astra high when deeper reasoning is justified; skip intermediate tiers when the risk warrants it. Increase effort only for a concrete need; do not default to max/ultra. A reviewer unable to resolve material uncertainty hands off findings to a fresh stronger reviewer without grades. Never shop for a passing grade, discard prior findings, or escalate for missing credentials, broken tools, quota, or unavailable evidence. Existing time, candidate, and no-progress limits still apply.

Installed custom roles are `quality_scout`, `quality_worker`, `quality_builder`, `quality_expert`, `quality_reviewer`, and `quality_senior`. Use one only when its actual model and effort match the selected tier. Several currently lock GPT-5.6 models and cannot accept overrides. Otherwise use a supported generic role with explicit model/effort and the same assignment constraints. For example, the current interface supports `agent_type="default", model="gpt-6-luna", reasoning_effort="medium", fork_turns="none"`. Prompt text cannot change a model. Do not change global role files or settings to implement routing. Do not fork an author's history into an independent reviewer.

If a preferred model is unavailable, choose a callable same-family alternative only when it can meet the same requirements, state the substitution and cost uncertainty, and record why. Do not downgrade a high-risk role just to continue. If no adequate model or required separate context is available, report BLOCKED for that assignment. Recheck official pricing/capabilities when the catalog changes or a new cost comparison is needed; reuse current evidence within the task.

Give workers: objective, verified selected worktree absolute path and branch, actual base/diff scope, owned files, constraints, acceptance IDs, planned checks, existing findings, and result/evidence location. State that they are not alone and must preserve others' work. Reviewers may write review artifacts only, outside the candidate. Agents must not spawn children or create additional worktrees/branches. Verify commands and edits target the assigned selected worktree; do not use the original checkout. Never create or amend commits unless the user explicitly requests that commit action; creating/updating a PR does not grant commit permission. For UI tasks, assign real screenshot capture to the appropriate worker/lead and provide those artifacts to reviewers. Return compact findings and evidence paths, not raw logs.

Efficiency: for a small low-risk change, the lead writes and one fresh reviewer reviews. Avoid separate scout/worker dispatches unless they save useful work; do not run several models on the same assignment to pick a winner. Subagents inherit the active loop and do not launch another one. Use fresh bounded context by default, with relevant source/diff paths, raw evidence, and prior findings rather than the whole conversation. Reuse a worker for a closely related repair; scored reviewers always get a fresh context. Reuse unchanged checks and stop on the first valid PASS. Close or interrupt completed agents through the supported tool.

Budget accounting: track candidate number, elapsed minutes, active agents, repairs and known usage. Unknown token/cost usage stays unknown. API list prices are comparison inputs, not the user's Codex subscription charge. Account for the actual service tier, cached input, context length, and reasoning/output when available; never claim savings without measured comparable usage. Use a lower-cost service tier only when the tool exposes it and the task permits it; the current delegation interface exposes priority only, with no tier selector. Do not fabricate one or change billing/settings. Do not poll continuously or rerun checks with unchanged inputs.

Pricing reference checked 2026-09-24: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing). Standard short-context input/output USD per 1M tokens: Luna $0.10/$0.50, Sol $2/$10, Astra $10/$50. Fast/priority rates are higher. This supports using Luna for bounded work and reserving stronger models for judgment; it does not establish task success rates. Refresh before relying on these dated rates.

Models/efforts were checked against the active delegation schema, which takes precedence over cached catalogs. No global model, permission, or concurrency setting is required for this skill; limits are applied to this workflow.
