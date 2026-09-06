## UI And Template Rules

- Match nearby Seamstream UI. The main shell uses Tailwind CDN, Lucide CDN, Font Awesome, custom toast CSS, `static/css/tokens.css`, and local classes such as `.btn`, `.btn-primary`, `.badge`, `.card`, `bg-primary`, and `text-primary`.
- Treat the current product UI as the design system. Inspect comparable screens before changing templates, CSS, JS-rendered markup, forms, tables, cards, tabs, modals, badges, empty/loading/error states, or responsive layouts.
- Reuse existing color variables, palette, semantic states, spacing, border radius, typography, table/form/button/modal/tab/card/badge styles, toast patterns, loading and error treatments, and mobile/desktop behavior.
- Reuse existing UI libraries, helpers, icon patterns, and JavaScript patterns. Do not add a new UI library, CSS framework, icon set, font, palette, animation library, bundler, or one-off visual system unless the user explicitly requires it.
- Use Lucide icons with `<i data-lucide="..."></i>` in areas already using Lucide and refresh icons after dynamic insertion with `lucide.createIcons()` or `window.lucide?.createIcons?.()`.
- Preserve Font Awesome usage in the main navigation unless the task explicitly changes that shell.
- Prefer Django `{% url %}` tags and template-provided `data-*` URL attributes for new template-driven API paths. When editing legacy JS that already has hardcoded `/api/...` or `/factory/api/...` paths, keep changes scoped instead of broad URL rewrites.
- Escape or sanitize user-controlled values before inserting them into HTML, attributes, tooltips, `data-*`, modals, toasts, or generated downloads.
- Preserve existing event handlers, active DOM paths, onboarding markers, setup modals, import/wizard tabs, toast behavior, disabled/loading states, and copy unless the task explicitly changes them.
- Preserve accessibility: labels, focus states, keyboard access, contrast, readable validation/error messages, non-overlapping text, and stable layouts across mobile and desktop widths.
- Preserve saved state, not just display state: form values, tabs, filters, selections, loading/error state, session/local storage, and refresh behavior.
- For UI changes, verify desktop and relevant narrow/mobile widths when feasible. Capture before/after screenshots for visible changes when local state can be opened.

