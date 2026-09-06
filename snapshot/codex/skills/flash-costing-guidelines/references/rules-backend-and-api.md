## Backend And API

- Use selectors for query composition when a selector already exists, especially library and schema lookups.
- Use service/business modules for reusable domain behavior: schema validation/versioning, feature group mutations, SMV, labour, BOM pricing, PDF, LLM, redesign, refine, and similarity.
- Keep serializers focused on API shape and validation. Keep multi-step workflow, LLM, schema versioning, and persistence orchestration in views, services, tasks, or business modules.
- Use DRF `Response` and `serializer.is_valid(raise_exception=True)` in DRF APIs. Use `JsonResponse` in template-backed JSON views where that is the local pattern.
- Protect read endpoints with the same ownership/staff checks as writes. Authentication alone is not enough for user-owned costings.
- Keep Open Costing model documentation in a dedicated Open Costing document or section, not a broad generated model reference. Document the workflow models, ownership, snapshots, proposals, statuses, and accepted-version records together so future reviewers can reason about the domain boundary.

