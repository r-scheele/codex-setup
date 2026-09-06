## Storage And Files

- Storage behavior is controlled by `USE_S3_BACKEND`, `S3_STATIC`, and `seamstream_ai/storage_backend.py`.
- `PrivateMediaStorage`, `PublicMediaStorage`, and `LocalMediaStorage` are used by tech packs, selected images, archetypes, brand logos, and related media. Preserve private/public distinction.
- For file replacement or cleanup, save the replacement before deleting the old file and keep the model pointer valid if storage operations fail.
- For PDF/image flows, inspect PyMuPDF/Pillow usage, selected image serializers, `TechPackFile`, `TechPackSelectedImage`, and flash-costing upload/page routes before changing storage assumptions.

