# Recorded evidence

Use `python3 /absolute/path/to/engineering-quality-loop/scripts/quality.py --help`.
Python 3.9+ and Git on macOS/Linux are required. No third-party Python packages are needed.

Before implementation, capture baseline hashes or content for any protected/unchanged-file acceptance criteria. Include a preservation check or a reviewable baseline artifact in the plan; a candidate snapshot alone only proves current content.

Create a plan outside the source root before checking. Keep the same plan across repair rounds; if the user's requirements change, start a new task and explain the change rather than silently weakening the gate.

```json
{
  "risk": "low",
  "task": "Make parse_port reject out-of-range values",
  "criteria": [
    {"id": "A1", "description": "Integers 1 through 65535 work; all other values raise ValueError"}
  ],
  "checks": [
    {"id": "ports", "kind": "command", "argv": ["python3", "-B", "test_ports.py"], "timeout_seconds": 30, "criteria": ["A1"]}
  ]
}
```

Every check in the plan is required. Use check IDs like `ports` or `browser_save`, never paths. Commands are argument arrays, executed directly in the source root with stdin disabled. Use the actual environment interpreter, executable, and meaningful assertions. Shell features need an explicitly reviewed shell invocation. Do not put credentials in arguments or logs.

1. Freeze after implementation, using real task/agent author IDs, not invented labels:

```bash
python3 /path/to/quality.py freeze --root /path/to/source --plan /path/to/evidence/plan.json --run /path/to/evidence/round-1 --author ACTUAL_AUTHOR_ID
```

2. Execute each planned check:

```bash
python3 /path/to/quality.py check --run /path/to/evidence/round-1 --id ports
```

Checks record exit status, bounded output (first 1 MiB), truncation, timeout, and code fingerprints. Inspect the log: a passing command is not automatically a meaningful check. If output truncation hides needed results, plan a concise equivalent check in a documented revised task plan. Timeouts terminate the process group on macOS/Linux. The helper also cleans up background children: use separate user-authorized server tools for persistent dev servers. A daemon that deliberately escapes the process group is outside this local recorder's containment guarantee.

For manual/browser behavior, plan an observation instead:

```json
{"id":"browser_save","kind":"observation","procedure":"Save the changed value, refresh, and verify it persists for the target role; check the non-target role remains unchanged.","criteria":["A1"]}
```

Capture screenshots or browser/API transcripts through supported tools, then record the observation:

```bash
python3 /path/to/quality.py check --run /path/to/evidence/round-1 --id browser_save --artifact /path/to/evidence/browser.txt --artifact /path/to/evidence/save.png --note "Exact steps, environment, and observed outcome" --outcome pass
```

For UI tasks, include a required observation with real screenshots captured by a supported browser/app tool. Prefer saved image artifacts. When the active tool can emit a real screenshot inline but cannot save it, bind a concise manifest or browser transcript as the artifact and record the app/URL, viewport, relevant state, candidate context, and successful inline capture in the note. Include the emitted image and tool activity in the reviewer packet and show useful final screenshots to the user. A transcript without an actual captured image remains insufficient.

Choose device coverage from the changed risk: require mobile screenshots for responsive/layout changes, explicit user requirements, or project policy, not for every UI task by default. A locked native desktop does not fail the observation when another supported surface can exercise and capture the same required state. Missing evidence blocks only the criterion it is actually needed to prove; do not weaken explicit acceptance requirements because a surface is unavailable.

Observation provenance is explicitly operator-entered. The reviewer must inspect the artifacts and actual tool activity; the helper does not certify that a browser interaction happened.

3. Give the reviewer the plan, candidate, relevant diff/source, logs/artifacts, and prior findings stripped of scores. The reviewer writes `review.json` in the round directory. Keep its actual returned transcript alongside it. Required format:

```json
{
  "candidate_id": "ID_FROM_CANDIDATE_JSON",
  "reviewer": {"id": "ACTUAL_DISTINCT_AGENT_ID", "model": "OBSERVED_MODEL_OR_EXPLICITLY_UNVERIFIED_MODEL", "independent": true},
  "check_hashes": {"ports": "SHA256_OF_PORTS_JSON"},
  "criteria": [{"id":"A1","status":"met","evidence":["ports"],"rationale":"Concrete assertion and code references that establish this criterion"}],
  "findings": [],
  "specialists": [],
  "dimensions": {
    "correctness": {"score":9,"evidence":["ports"],"rationale":"..."},
    "verification": {"score":9,"evidence":["ports"],"rationale":"..."},
    "security": {"score":9,"evidence":["ports"],"rationale":"..."},
    "reliability": {"score":9,"evidence":["ports"],"rationale":"..."},
    "efficiency": {"score":9,"evidence":["ports"],"rationale":"..."},
    "simplicity": {"score":9,"evidence":["ports"],"rationale":"..."}
  }
}
```

For `risk: "high"`, `specialists` must include a second distinct non-author reviewer with `id`, `model`, `independent: true`, `focus`, `candidate_id`, `check_hashes`, `evidence`, `rationale`, and `status: "pass"`. The lead includes all specialist findings in the main findings ledger. Keep the specialist's original response as evidence. `risk` must be `low`, `medium`, or `high`.

The numbers above illustrate JSON structure only. The independent reviewer must assess its own scores and rationales from evidence. Use `shasum -a 256 /path/to/round-1/ports.json` to bind the reviewed record. Do not copy example scores as a review.

Finding example:

```json
{"id":"F1","severity":"high","must_fix":true,"status":"open","description":"Concrete trigger and incorrect behavior","evidence":["ports"],"rationale":"Evidence and required repair; after resolution, explain the confirming check"}
```

4. Run the gate:

```bash
python3 /path/to/quality.py gate --run /path/to/evidence/round-1
```

Exit codes: 0 PASS (or successful freeze/check), 1 NEEDS_REPAIR/failed check, 2 BLOCKED/malformed or stale evidence. Keep the output as a validation artifact. On repair, create `round-2` with `freeze ... --previous /path/to/evidence/round-1`, including all new authors. Never overwrite old check/review records. Before another round, check the workflow time/candidate/no-progress limits; the helper does not enforce those budgets.

## Coverage and limits

- Git: use the repository root. Hash tracked plus nonignored untracked files, including file modes. Deleted/added/renamed inputs change the fingerprint. The snapshot evaluates working files; the reviewer still needs the actual task base and full diff, including relevant commits and staged changes.
- Plain folders: hash regular files recursively, excluding `.git` and `__pycache__`. Keep generated files outside the source, or use Git ignore rules deliberately for build artifacts.
- Ignored files are excluded in Git. Include relevant ignored regular files with repeated `--extra-input relative/path` at freeze; keep the list stable. External dependencies, environment variables, databases, services, ignored directories, submodules, symlinks, and remote state need explicit independent runtime evidence. Symlinks/submodules among selected inputs block this helper instead of silently yielding a partial fingerprint. Do not remove needed files from scope to force a pass.
- Runtime evidence needs environment/version, observation time, and relevant state. A fingerprint cannot detect a transient edit restored between samples or a database/service change after a check. The lead invalidates affected evidence when these inputs change.
- Hashes detect accidental changes, not an actor rewriting all records. Reviewer independence/model identity are declarations checked against the real host's activity by the lead. This is a local assistant workflow, not protected CI, signed provenance, a sandbox, or an enforced monetary budget.
