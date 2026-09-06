## Repo Shape

- Treat `apps/costing/` as the product core: models, forms, views, schema editor views, API views, selectors, business logic, services, Celery tasks, management commands, and existing tests.
- Treat `apps/users/` as auth and preference support: email-only users, `costing_preferences`, user profile views, and DRF `UserViewSet`.
- Use the existing stack: Django 5.2, DRF, django-allauth, Celery, Redis, OpenAI SDK, PyMuPDF/Pillow, openpyxl, simple-history, vanilla JavaScript, Django templates, static CSS, uv, pytest, ruff, mypy, djLint, pre-commit, and Docker Compose.
- Prefer local non-Docker commands for quick checks, and use Docker/`just` when local services or CI parity are needed.
- Use focused source searches by default. Use Graphify only for an explicit graph request or an architecture question that benefits from a current graph; do not rebuild it as a feature-start ritual. Check installed capabilities rather than assuming a provider key is required.

