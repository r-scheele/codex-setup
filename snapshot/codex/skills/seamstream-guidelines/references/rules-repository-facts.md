## Repository Facts

- Repository path: `__HOME__/Desktop/code/seamstream_ai`.
- Default remote branch observed at creation time: `main` tracking `origin/main`; do not assume a `dev` branch.
- This repo currently has no `AGENTS.md`; if one appears in the checkout, read it before editing and follow it with this skill.
- Runtime stack: Django 4.2 project with Django REST Framework, Django templates, Tailwind CDN, Lucide CDN, Font Awesome in the main shell, custom CSS/token utilities, plain JavaScript modules, SQLite local DBs, optional S3 storage, OpenAI/Gemini LLM calls, Stripe, SendGrid, Slack logging, and APScheduler.
- Internal apps are `apps.converter`, `apps.subscription`, `apps.accounts`, `apps.messaging`, and `apps.factory`; `apps.flash_costing` is also present with API/templates but is not in `INTERNAL_APPS` in `seamstream_ai/app_settings/base.py`.
- Key paths: `seamstream_ai/app_settings/`, `seamstream_ai/db_logics/`, `seamstream_ai/api_router.py`, `seamstream_ai/urls.py`, `apps/accounts/`, `apps/converter/`, `apps/converter/v2/`, `apps/factory/`, `apps/flash_costing/`, `apps/subscription/`, `apps/messaging/`, `templates/`, `static/js/`, `static/css/`, `resources/`, `schema-data/`, and `tests/apps/converter/business_layer/`.

