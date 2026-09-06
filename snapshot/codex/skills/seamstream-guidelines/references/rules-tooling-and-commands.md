## Tooling And Commands

- Prefer `rg`, `git diff`, `git grep`, and `sg` when structural search reduces risk. `sg` is optional; do not add it to project dependencies.
- Use focused source searches by default. Use Graphify only for an explicit graph request or an architecture question that benefits from a current graph; do not rebuild it as a feature-start ritual. Check installed capabilities rather than assuming a provider key is required.
- Use the repo's plain Python/Django commands, not `uv`: `python manage.py ...` or `make ...`.
- Setup/run commands observed in the repo:
  - `pip install -r requirements/dev.txt`
  - `make full_setup`
  - `python manage.py runserver`
  - `make run` starts `ENABLE_SCHEDULER=true python manage.py runserver_plus`.
  - `python manage.py test tests` or focused paths such as `python manage.py test tests.apps.converter.business_layer`.
- Be careful with `make full_setup`: it runs `makemigrations`, `migrate`, `csv_to_json`, `extract_encoding_combination`, `ingest_data`, and `collectstatic`; do not run it casually when a focused command is enough.
- Use `python manage.py makemigrations --check --dry-run` to check whether model changes need migrations.
- Run pre-commit only when a commit is requested or the touched files justify it. The configured hooks are trailing whitespace, EOF fixer, YAML check, Black, isort, and flake8; `pre-commit` may not be installed locally.

