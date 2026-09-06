## Open Costing Rules

- Never overwrite or mutate the original `Costing` or `CostingResult`.
- Store factory responses as separate proposals linked to the original costing.
- Preserve a read-only snapshot of the original costing when a request is created.
- Keep Open Costing model classes small. Put request, response, BOM, labour/SMV, profit, snapshot, lock, and acceptance validation in a dedicated business/validation module instead of adding large validation helper sections to `apps/costing/models.py`.
- Treat access control as the first gate, not a fallback validation error. Brand-side Open Costing views must fetch through the owning costing/user; factory-side views must fetch through the scoped token or authenticated factory account. Validation may reject inconsistent objects, but users who cannot view or submit a request should not be able to load it in the first place.
- Before approving or handing off Open Costing model changes, perform a normalization sweep: no duplicate factory identity on responses, no duplicate submitter fields when `FactoryAccount.user` already identifies the factory user, no duplicate request/response submission timestamps, and no inline proposal comments when `OpenCostingComment` can target the response, BOM row/section, labour section/row, profit, or summary.
- Use stable row IDs for original BOM rows before comparing factory changes.
- Support added, removed, changed, and unchanged BOM rows.
- Prevent division-by-zero in percentage delta calculations.
- Do not double-count profit when profit is included in CPM.
- Accepting or rejecting a factory response must not overwrite the original result.
- Factory token access must expose only the linked request, respect expiry, and lock submitted responses unless explicitly reopened.
- Add or update tests for every implemented Open Costing task or bug fix.
- Do not silently resolve conflicts between the specification, decisions, and existing code. State the conflict and use the safest reversible implementation.

