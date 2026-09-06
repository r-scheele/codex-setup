---
name: codex-router
description: Diagnose tool relay, model routing, or usage behavior in a confirmed custom-model session using the local model router.
---
# Codex Router (custom models in the Codex app)

Apply this only after the session confirms it uses a custom provider through the local router. The presence of MCP tools alone does not establish the model or routing path.

## How your tools work

- The app's native tools appear in your tool list with flattened names:
  `codex_app__create_thread`, `codex_app__list_threads`,
  `mcp__node_repl__js`, `mcp__peekaboo__create_task`, and so on.
- Use the exact names currently exposed; the following names are examples, not an availability guarantee. The router restores the original
  namespace (for example `create_thread` in `codex_app`) before the app
  sees the call, so the app executes it natively.
- The router never executes an app tool. It only relays definitions and
  results. If a call fails, fix your arguments; do not try to run the tool
  yourself.
- Never spawn a side-channel driver. Do not start your own node_repl
  process, do not fake MCP metadata, do not write driver scripts. Use an available supported tool or report the specific missing capability.

## Companion guidance when needed

- Threads, automations, navigation: use current native tools; read `codex-app-threads` only for custom-model relay guidance.
- In-app browser: use current UI tools; read `codex-in-app-browser` only if relay guidance is needed.
- Computer use: use current UI tools; read `codex-computer-use` only if relay guidance is needed.

## When a tool rejects your arguments

The app answers `received invalid arguments.` when you missed a required
field. Stop guessing. Read the current tool schema for the exact shape, then
retry once with the correct arguments. Repeated guessing burns tokens and
turns.

## Golden rules

1. Use the tools you were given. Do not build workarounds.
2. Load a companion skill only when it adds guidance missing from the live tool documentation.
3. When a call fails, fix the arguments from the current schema, then retry.
4. A turn with no tool call ends the task. After a tool result, if more work
   still needs a tool, call it in the same turn. Do not only announce the next
   step. Text-only is for when the user's request is fully done.

## Spawned threads and model inheritance

For a new local Codex thread, omit the `model` field unless the user
explicitly requested one. Let the current task-creation tool use its documented default; do not assume parent-model inheritance. An
explicit model is never overridden. Follow-up messages retain the target
thread's settings, and cloud tasks choose their model outside this relay.

## What the token and usage numbers mean

- The router meter records provider-reported counts verbatim. When the
  provider reports `input_tokens: 0`, the router substitutes a byte-based
  estimate and stores it in a separate `estimatedInputTokens` field; the
  provider's zero is preserved in the row. Treat `estimatedInputTokens` as
  an approximation, never as a real provider count.
- A turn whose upstream stream dies mid-flight is recorded with status 502
  and a `streamAborted` marker. A client cancel records status 0. If you see
  many `streamAborted` rows, the upstream connection is flaky; do not treat
  them as model behavior.
- Verify displayed context limits and usage behavior against the running app/router version. Historical percentages are not a current guarantee. Estimated token counts are not exact provider usage.

## If the session seems to stop mid-task

Check the meter at `~/.codex/codex-router/usage-events.jsonl` for the
session's model first. Causes, in order of likelihood: a spawned thread died
on a native usage limit while the parent waited; an upstream stream dropped
mid-flight; the app compacted early on inflated estimated totals; the router
restarted. The router service restarts are normally supervised by launchd
and are not a production crash loop unless the log shows repeated exits
without an external trigger.
