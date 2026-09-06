## Branch, Database, And Environment

- Default new work against `main` unless the user or PR says otherwise.
- Before editing, check branch and dirty state with `git status --short --branch`.
- Use neutral branch names such as `feat/<short-description>` and `fix/<short-description>` if the user asks for a branch. Never use AI/tool-branded prefixes.
- Local settings are selected through `ENVIRONMENT`; default is `local`.
- Local settings create branch-specific SQLite DB files: `db_<branch>.sqlite3`, `db_tal_<branch>.sqlite3`, and `db_technosport_<branch>.sqlite3`.
- Domain database routing maps `app.seamstream.ai` to `default`, `tal.seamstream.ai` to `tal`, and `technosport.seamstream.ai` to `technosport`; with `ENVIRONMENT=local`, `app.local`, `tal.local`, and `technosport.local` map the same way.
- If work touches database routing, use `seamstream_ai/db_logics/domain_router_middleware.py`, `database_router.py`, `db_context.py`, and `utils.py` as source of truth.
- If local verification needs a tenant DB, explicitly set the host/domain path or DB context rather than assuming `default`.

