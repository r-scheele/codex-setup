# Model routing (DeepSeek only)

This loop runs on DeepSeek models for every role: the lead, each writer, and each
independent reviewer. That is the same shape as the GPT-family loop, which routes its
roles only to GPT models. Do not substitute another model family to make a role look
independent.

Choose the least expensive adequate DeepSeek model for the judgment required. These are
local workflow defaults, not a benchmark or price guarantee. Inspect the callable tools and
the model and effort values the host actually offers; never invent a role or silently
substitute a model. Record requested versus observed model and the actual agent ID. Report
when the host cannot verify model selection.

| Assignment | Model | Effort |
|---|---|---|
| Focused repo or doc lookup | deepseek-v4-flash | low |
| Specified implementation or repair | deepseek-v4-flash | high |
| Ordinary integration | deepseek-v4-pro | high |
| Difficult diagnosis or implementation | deepseek-v4-pro | max |
| Independent senior review | deepseek-v4-pro | high |
| High-risk authorization, data integrity, payment, infrastructure review | deepseek-v4-pro | max |

Use the current lead. Do not change the user's model settings just to satisfy this table.
Start a hard task at the appropriate tier rather than failing through every cheaper setting.
Allow one evidence-guided repair per worker before reconsidering the assignment or tier.
For high-risk work, use a second distinct specialist with an explicit security or
reliability question alongside the senior reviewer. Run the two sequentially if the
concurrency limit would otherwise be exceeded. Both must finish before PASS; record both
identities and findings.

## Independence inside one model family

Independent review does not require a different model family here. It requires a fresh
context that never saw the author's reasoning, plus distinct identity:

- Start the reviewer with no inherited turns and with only the raw artifacts.
- Do not fork the author's history into the reviewer.
- Give it the plan, candidate diff or source, raw check records, logs, artifacts, and prior
  findings stripped of scores. Withhold the author's conclusions and preferred outcome.
- Prefer a different tier or effort for the reviewer than the author used, and state it.
- Never let a candidate author review their own task, and never reuse one reviewer instance
  as the author of a later repair.

Give workers: objective, verified selected worktree absolute path and branch, actual base
and diff scope, owned files, constraints, acceptance IDs, planned checks, existing findings,
and the result and evidence location. State that they are not alone and must preserve others'
work. Reviewers may write review artifacts only, outside the candidate. Agents must not spawn
children or create additional worktrees or branches. Verify that commands and edits target
the assigned selected worktree, not the original checkout.

Never create or amend commits unless the user explicitly requests that commit action;
creating or updating a PR does not grant commit permission. For UI tasks, assign real
screenshot capture to the appropriate worker or the lead and provide those artifacts to
reviewers. Return compact findings and evidence paths, not raw logs.

## Budget accounting

Track candidate number, elapsed minutes, active agents, repairs, and known usage. Unknown
token or cost usage stays unknown. Do not poll continuously or rerun checks whose inputs
have not changed. Stop on the first valid PASS.

## Availability

DeepSeek-v4-flash and deepseek-v4-pro with low, high, and max effort are the expected
options. Availability can change between sessions and across hosts. The running tool schema
takes precedence: use the values it exposes, and if no DeepSeek model is callable, say so
plainly and report the affected roles as unstaffed instead of quietly routing the task to
another family.
