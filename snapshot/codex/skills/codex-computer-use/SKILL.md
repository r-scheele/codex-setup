---
name: codex-computer-use
description: 'For custom-model sessions: operate native apps using the current computer-use tools when a connector or CLI cannot do the task.'
---

# Current Native App Tools for Custom Models

Use only in a confirmed custom-model session that needs native app interaction. Tool names, schemas, and documentation supplied by the running session are authoritative.

1. Prefer a purpose-built connector or CLI for the task. For UI interaction, discover the currently exposed computer/browser tools. If `mcp__cua_repl.js` or its normalized equivalent is present, follow its first-call and returned documentation exactly.
2. Use a legacy `mcp__node_repl__js` bootstrap only when that tool is actually exposed and its matching installed runtime documentation exists. Locate the current plugin version instead of constructing a stale path. Do not assume `@oai/sky`, `globalThis.agent`, or a particular browser ID.
3. After interaction, inspect fresh UI state and verify the requested result. Respect the current tool’s authorization and safety rules. Reuse live handles as documented.
4. If the legacy tool is absent, continue with the supported current UI tool or connector. Report a blocker only when no authorized supported path can complete the required action.

Do not start a side-channel UI driver, fabricate tool calls, or use `open_in_codex` as if it could read or click a page.
