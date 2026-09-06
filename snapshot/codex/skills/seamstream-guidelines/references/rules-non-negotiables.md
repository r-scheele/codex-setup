## Non-Negotiables

- State assumptions explicitly; never guess silently. If intent is unclear after inspecting the relevant Seamstream code, call out the assumption or ask before changing behavior.
- Define success before changing code: expected behavior, acceptance criteria, affected user/workflow, and verification path.
- Make surgical changes only. Do not refactor, restyle, reorganize, rename, or clean adjacent code unless the task explicitly requires it.
- Reuse existing local patterns first. Check nearby Seamstream implementations before adding new helpers, APIs, UI components, settings, or data flows.
- Treat the current UI as the design source of truth. Preserve Seamstream's existing product design principle, visual language, interaction patterns, saved state, and responsive behavior unless the user explicitly requests a visual redesign.
- Preserve existing behavior and payload semantics unless the request explicitly changes them.
- Do not remove, hide, shadow, bypass, or orphan existing UI controls, routes, API actions, serializer fields, model fields, template blocks, JavaScript handlers, scheduler behavior, cache behavior, or storage paths unless the user explicitly asks for removal and references have been checked.
- Treat indirect removals as removals: duplicate renderers, duplicate action names, unreachable buttons, replaced DOM without handlers, narrowed conditions, or new code paths that shadow old behavior are risky.
- When deleting or renaming a function, method, model field, route, URL name, template include, JavaScript export, management command, or shared helper, search references with `rg`/`git grep` and report the result.
- Do not import conventions from other repositories. Seamstream uses direct factory/profile scoping and does not have an entity permission-helper layer, DaisyUI, `uv`, or a default `dev` branch in the inspected checkout.
- Do not put AI/editor/tool branding in code, comments, generated copy, branch names, commit messages, PR titles/bodies, screenshots, or review comments.
- Do not commit, push, merge, retarget, close PRs, or delete branches unless the user explicitly asks.
- Never force-push or run forceful/destructive git operations. Do not use `git push --force`, `--force-with-lease`, `git branch -D`, `git tag -f`, `git reset --hard`, `git clean -fd`, `git checkout -f`, or any git flag/command whose purpose is to force, overwrite, or discard work; if asked, refuse and offer a non-force alternative.
- If the working tree has unrelated local changes, do not modify or revert them.

