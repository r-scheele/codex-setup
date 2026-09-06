---
name: graphify
description: Build or query a repository knowledge graph when graph traversal materially helps a broad architecture question or is explicitly requested.
---

# Repository Graphs

Use graph analysis only when explicitly requested or when it materially helps a broad architecture/dependency question. For a small code lookup or ordinary edit, use focused source search. Do not install, rebuild, scan the whole repo, export visualizations, or ask for keys merely because code is involved.

- For a question about a current existing graph, read [query guidance](references/query.md). Verify important answers and source locations against live files; stale or missing graph data does not block source inspection.
- For an explicitly requested build or rebuild, read [build workflow](references/build.md). Check installed `graphify --help` and supported modes first. Structural code extraction does not require an LLM key; semantic modes depend on the installed backend and can use authorized inline extraction. Do not request a provider key by default.
- For incremental updates, use [update guidance](references/update.md). For other requested commands, use [command notes](references/command-notes.md) and the matching reference it names.

Resolve reference-relative resources from this skill folder and repository inputs from the active checkout. Use only currently available tools. Preserve existing graphs when extraction fails, disclose incomplete/stale results, and never report estimated token savings as measured results. Do not impose a graph build before unrelated feature work.
