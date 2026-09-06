## Product Data And Workflows

- Treat tech-pack import and processing as a core flow. Relevant code includes `apps/converter/v2/views.py`, `apps/converter/v2/api/views.py`, `apps/converter/v2/api/serializers.py`, `apps/converter/business_layer/`, `apps/converter/v2/business_layer/`, `templates/wizard*/`, `templates/complete_poc_user_new.html`, and `static/js/complete_poc_2.js`.
- Treat Operation Breakdown state carefully. `OperationCard`, `OperationBook`, `OperationBookVersion`, `OperationBreakdownVersion`, autosave, rollback, restore, lock/protect flags, `current_snapshot`, and `current_version` must stay consistent.
- Preserve optimistic version checks, row-level diff behavior, autosave retention, lock behavior, restore provenance, and retry-on-version-collision logic unless the task explicitly changes them.
- For factory setup, inspect `apps/factory/models.py`, `apps/factory/api/views.py`, `templates/factory/`, and `static/js/factory_setup/`. Preserve `request.user.profile.factory` scoping.
- For subscriptions and credits, inspect `apps/subscription/business_layer.py`, `apps/subscription/api/views.py`, `apps/subscription/models.py`, and subscription templates. Do not create/cancel real Stripe subscriptions or sessions unless explicitly requested and the environment is confirmed safe.
- For messaging, inspect `apps/messaging/business_layer/email_backend.py` and templates before changing SendGrid/email behavior. Do not send real email during verification unless explicitly requested.
- For flash costing, inspect `apps/flash_costing/api/views.py`, `apps/flash_costing/services/`, `templates/flash_costing/`, `schema-data/`, and `resources/`; it has its own schema/config/testing/document review flow.

