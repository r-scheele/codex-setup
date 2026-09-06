## Review And Handoff

- At the end of implementation, inspect `git diff --stat`, `git diff --name-only`, `git diff --check`, and the focused diff.
- For UI/product-visible changes, run real-user QA through the product when feasible. Use Browser for localhost UI verification when available.
- Include screenshot evidence for visible changes whenever local setup/data permits; if blocked, state the exact blocker.
- In handoff, explain PM-facing outcome first, then the technical path through files/functions/classes/templates and validation.
- For bug fixes, technical notes should follow the app flow: user action, template/static JS, API request, backend validation/business logic, persistence/storage/external service, response, and final UI state.

Run the smallest relevant existing Django check or test. Add or update meaningful regression coverage when changed behavior or risk warrants it; do not require tests for trivial edits. For UI changes verify the real user path, desktop/mobile behavior, saved state, and before/after screenshots when available. For routed data changes verify the affected tenant database and a relevant isolation boundary. Report unverified cases accurately. Broaden checks only when a new change, failure, or shared-code risk justifies it.
