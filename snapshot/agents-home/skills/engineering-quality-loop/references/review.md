# Independent review and grading

Read the actual candidate and raw check results. Do not inherit author confidence. Keep scores from earlier rounds out of the review packet, but include all prior findings and dispositions. Reviewers do not modify the implementation. Report an independent review as unavailable if no separate context can be used.

Focus checks on the changed risk:
- Git/PR presentation: inspect new task names, diff, commit messages/trailers, author/committer identity, and PR metadata for assistant branding. Distinguish promotional attribution from necessary product/API references or legally required notices. Report existing history separately; never infer permission to commit, rewrite history, or falsify identity.
- Correctness: acceptance criteria, sibling callers, boundary values, persistent state, regressions, errors mistaken for success.
- Execution evidence: for UI tasks, inspect required real screenshots and observation bindings; missing/stale images leave the criterion unverified even when tests pass. Also inspect real check discovery/assertions, actual environment/version, realistic wrong implementations, mocks hiding the relevant failure, UI refresh/persistence and target/non-target roles when applicable.
- Security: trust boundaries, auth versus authorization, tenant ownership, injection, secret/PII exposure, untrusted tool or document instructions. Inspect security implications even when no runtime security test is needed.
- Reliability: concurrency, atomicity, duplicate delivery/idempotency, partial failure, cancellation, retries/timeouts, cleanup and recovery.
- Efficiency: measured bottlenecks, unbounded work or input, query/resource growth. Define local stress limits and stop conditions before running. Avoid production load or invented throughput claims.
- Simplicity: duplicated rules, hardcoded database-owned values, swallowed errors, sleeps for synchronization, unnecessary dependencies/abstractions, symptom patches. Recommend the smallest change that preserves guarantees; leave good work alone.

| Dimension key | Weight | Floor |
|---|---:|---:|
| correctness | .25 | 9 |
| verification | .25 | 9 |
| security | .15 | 9 |
| reliability | .15 | 8 |
| efficiency | .10 | 8 |
| simplicity | .10 | 8 |

Grading anchors: 0–4 has a demonstrated substantial defect; 5–7 has unresolved material behavior/evidence; 8 has bounded residual limitations; 9 meets applicable requirements with executed evidence and no material known defect; 10 requires exceptional evidence, not merely no findings. Use fractional scores only when supported by a concrete distinction. Explain each dimension with evidence IDs. These weights are engineering policy, not an OpenAI standard.

A low-risk change still gets all six dimensions inspected; explain why e.g. a new load test is unnecessary rather than inventing one. Missing required evidence stays unverified. Do not mark security "not applicable" to avoid examining it. Weighted total ≥9.0 does not override any required check, dimension floor, acceptance criterion, or must-fix finding.

Each finding: stable ID, severity (critical/high/medium/low), must_fix boolean, status (open/resolved/dismissed), concrete description, evidence IDs, and resolution rationale. Preserve descriptions/IDs across repairs; add resolution notes instead of rewriting history. Dismissal requires contrary evidence; resolution requires a check that addresses the trigger. Earlier high severity findings cannot be relabeled low to pass.

Return reviewer identity, model, fresh-context declaration, candidate ID, hashes of the check records reviewed, per-criterion status and evidence, all findings, and dimension scores. Persist the actual reviewer response as an artifact. The lead checks identity against real activity and corrects factual errors without changing the reviewer's grade. Use the gate's output; never claim an independent reviewer existed merely because a JSON field says so.
