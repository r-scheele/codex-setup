## UI And JavaScript

- Treat the current UI as the design source of truth. Inspect nearby templates, `apps/static/css/project.css`, existing static JS, and comparable screens before changing UI.
- Preserve the existing product design principle: quiet, utilitarian, workflow-focused garment-costing screens built for repeated operational use. Do not introduce marketing-page, oversized hero, decorative card-heavy, or unrelated visual patterns into app workflows.
- Follow the existing visual system in `apps/static/css/project.css`: `fc-*` classes, `btn-primary`, `btn-secondary`, `btn-ghost`, cards, status pills, forms, tabs, modals, and dark-theme variables.
- Reuse existing color variables, palette, semantic states, spacing, border radius, typography, table/form patterns, empty/loading/error states, and responsive behavior. Do not add a new palette, one-off colors, font stack, shadow language, or radius system unless the task explicitly requires it.
- Reuse existing UI libraries, helpers, and icon patterns already present in the project. Do not introduce a new frontend framework, CSS system, UI component library, icon system, animation library, bundler, or dependency for ordinary UI work.
- Keep new Open Costing, Send to Factory, comparison, delta, and secure factory portal UI visually consistent with the existing Flash Costing app: same buttons, cards, tabs, tables, badges, forms, alerts, and dark-theme behavior.
- Preserve accessibility and interaction quality: visible focus states, labels, keyboard-reachable controls, adequate contrast, readable error messages, non-overlapping text, and stable layout on mobile and desktop.
- Use Django `{% url %}` tags and `data-*` URLs instead of hardcoded internal URLs in templates.
- Use `json_script` for server JSON injected into pages.
- Escape user-controlled strings before assigning to `innerHTML`. Existing static JS has `escapeHtml`; reuse it or write the same targeted helper.
- Preserve existing vanilla JS patterns: `fetch`, `X-CSRFToken`, `X-Requested-With` for partials, `sessionStorage` state in schema editor, and targeted DOM updates.
- For BOM UI changes, trace both DOM state and saved JSON payload: row ids, section names, `price_source`, `prices_by_country`, `view_state`, notes, country changes, and totals.
- For schema editor UI changes, trace rendered tree state, drag/drop, picker behavior, session storage, validation errors, save payload, and feature group/value refreshes.

