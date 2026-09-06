## LLM, Cache, Scheduler, And External Services

- Treat LLM calls as expensive external operations. Avoid live OpenAI/Gemini calls in tests or verification unless the user explicitly wants live integration verification and keys/environment are safe.
- Preserve `apps/converter/business_layer/llm_cache.py` semantics: DB-specific cache via `get_current_db()`, `Settings.disable_llm_caching`, JSON response validation before caching, OpenAI/Gemini normalization, and `process_id` / `operation_name` metadata handling.
- Preserve scheduler duplicate-start protection in `apps/converter/business_layer/scheduler.py`; scheduler startup is gated by `ENABLE_SCHEDULER=true` in `apps/converter/apps.py`.
- Do not start background scheduler work during routine verification unless scheduler behavior is the target or `make run` is intentionally used.
- Do not log secrets, API keys, signed S3 URLs, Stripe IDs beyond what is already product-visible, or full LLM payloads containing uploaded document content unless needed for a local debug trace.
- Treat Slack logging configuration and webhooks as sensitive. Do not add or expose new webhook URLs.

