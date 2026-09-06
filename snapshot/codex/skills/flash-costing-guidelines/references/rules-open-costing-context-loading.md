## Open Costing Context Loading

For any Open Costing, Send to Factory, factory costing response, comparison, delta, or secure factory portal task, bug fix, PR review, or PR hygiene work:

1. Resolve the Git repository root, for example with `git rev-parse --show-toplevel`.
2. Obey the active `AGENTS.md` instruction chain before planning, reviewing, or editing.
- Read the relevant task row and specification/decision sections from the local sources below; expand only when dependencies or conflicts require more context:
   - `docs/_local/open-costing/specification.md`
   - `docs/_local/open-costing/task-sheet.csv`
   - `docs/_local/open-costing/decisions.md`
   - `docs/_local/open-costing/sources.md`
- Complete necessary, reversible supporting changes within the requested outcome. Ask only for unresolved product/access decisions, separate scope, unauthorized external actions, or destructive operations. Reuse authorization already given in this task.
5. Treat `specification.md` as the product source of truth, `decisions.md` as the source of resolved decisions, and `task-sheet.csv` as the implementation breakdown.
6. Before coding, produce a concise implementation understanding that names the matched task and phase, relevant requirements, affected existing code, dependencies and risks, and tests that should be added or updated.
7. Before review-only work, use the same context as the review baseline and flag any changed code that conflicts with the specification, decisions, or task sheet.
8. Inspect the existing implementation and follow established project patterns before introducing new abstractions.
9. If the specification, decisions, task sheet, or existing code conflict, do not silently resolve the conflict. State the conflict and use the safest reversible implementation or review recommendation.

