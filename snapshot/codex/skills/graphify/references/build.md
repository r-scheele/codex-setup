# Requested Graph Build

Run a graph build only for the selected repository/corpus when the user requests it or it is necessary for the explicitly chosen graph analysis. Check `graphify --help` and the installed package before selecting a mode; do not install or upgrade it just to answer an ordinary source question.

The installed CLI provides `update <path>` for structural code refresh without an LLM, `extract <path>` for full AST plus semantic extraction, and `cluster-only`/`label` for clustering and optional model-generated names. `extract` supports several backends; it is not Gemini-only. Inspect whether the chosen command contacts a configured provider before running it. A configured key is not permission to send a repository to that provider. Never print credentials.

For an existing graph, use a focused `update <path>` when an update is requested. Do not pass a force-overwrite option just to suppress a graph-size warning. Preserve a usable graph when extraction is incomplete.

For a new graph, inspect the installed structural extraction API or CLI path and use code-only extraction when the requested result needs no semantic model. If full semantic extraction is requested, select an already authorized backend and the requested corpus. If no backend is available, use authorized inline extraction for a bounded corpus or report the specific semantic limitation while continuing source-based analysis. Do not request an unrelated API key or a host configuration change by default.

Only use current supported delegation tools when delegation is allowed and independent chunks help. Inline extraction is permitted when delegation is unavailable. Do not require a nonexistent Agent or close_agent tool.

Check extraction errors, missing endpoints, graph size changes, source coverage, and freshness before using the result. Label inferred edges and incomplete coverage. Generate visualizations or exports only when requested or useful to the selected outcome; do not append a sponsorship message or solicit unrelated follow-up work.

For incremental details read [update](update.md); for graph diagnostics and export variants read [exports](exports.md). Resolve repository paths from the active checkout and skill resources from this skill folder.
