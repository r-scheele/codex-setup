## Django And API Rules

- Use DRF `Response` for DRF endpoints and Django `JsonResponse` only for existing non-DRF view patterns.
- For v2 converter APIs that already use `APIResponseOk` / `APIResponseFail` from `apps/converter/v2/api/helper.py`, keep that envelope unless the task explicitly changes it.
- Do not force every endpoint into one response shape. `apps/factory/api/views.py`, `apps/subscription/api/views.py`, `apps/converter/api/views.py`, `apps/converter/v2/api/views.py`, and `apps/flash_costing/api/views.py` currently use different local response shapes.
- Prefer `serializer.is_valid(raise_exception=True)` for DRF writes when serializers are used; preserve existing manual validation only when matching a nearby endpoint.
- Keep workflow and multi-step business logic in business/service modules when a local module exists: `apps/converter/business_layer/`, `apps/converter/v2/business_layer/`, `apps/subscription/business_layer.py`, `apps/accounts/business_layer.py`, and `apps/flash_costing/services/`.
- Do not move code between serializers, views, and business layers without a concrete reason and a small diff.
- Preserve access scoping. Factory-owned data is commonly scoped through `request.user.profile.factory`; staff often has broader access in converter v2 paths. Do not widen or narrow this without explicit confirmation.
- Do not invent permission decorators or entity mixins that do not exist in Seamstream. The repo uses Django `LoginRequiredMixin`, `login_required`, DRF `IsAuthenticated`, per-action `permission_classes`, and direct factory/profile scoping.
- Protect read endpoints as carefully as writes when they expose factory-owned documents, tech packs, operation cards, subscriptions, credits, or setup data.
- For model changes, generate migrations with `python manage.py makemigrations`; do not hand-write routine schema migrations. Custom data migrations/backfills are allowed only when product or production correctness requires them and must use the correct DB alias when relevant.
- Do not add production data population, default rows, seed commands, or fallback behavior unless the request explicitly requires it. Use local/test data for local verification gaps.

