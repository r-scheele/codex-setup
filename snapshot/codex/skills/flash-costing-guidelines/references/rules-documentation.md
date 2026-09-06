## Documentation

- Treat product and workflow documentation as a technical writing task, not a code dump. Write for product, QA, support, and future engineers who need to understand the behavior without reverse-engineering the implementation.
- Use clear human language, active voice, and concrete examples. Avoid robotic phrasing, generated-sounding summaries, and long checklist prose when a short explanation would be clearer.
- Keep documentation accurate to the code and requirements: define statuses, ownership, state changes, access rules, validation behavior, and pending decisions. Lead with implemented behavior and avoid adding non-goals, negative capability statements, or "does not accept/support" wording unless the user asks for it or it is necessary to document a security boundary, compatibility contract, or product-critical limitation.
- Prefer source-of-truth docs for durable business rules. Link or index the document from the existing docs structure when the repo already has one.

