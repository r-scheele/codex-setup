## Preflight Checkpoint

- Before editing code, send a short pre-implementation checkpoint and wait for confirmation if the change touches permissions, roles, workflow behavior, API scope, serializer/service boundaries, failure semantics, or any business rule that is not explicit in the request.
- That checkpoint must separate `what will change`, `what will not change`, `assumptions`, `business questions`, `technical questions`, and `what is being intentionally skipped`.
- Before listing any business or technical question, inspect the local code paths most likely to already encode the current behavior. Check the smallest relevant set first: views/actions, serializers, business/service code, permissions, templates/JS, migrations, and tests when relevant.
- Before asking a business or technical question, inspect the closest existing implementation on the relevant target branch or dependency branch.
- If that implementation clearly answers the question and does not conflict with explicit user instructions, acceptance criteria, transcript guidance, or review comments, treat that behavior as the confirmed default and proceed without asking.
- Only escalate the question when the existing implementation is missing, ambiguous, contradictory, or explicitly being changed by the request.
- Do not ask a business or technical question when the answer is already explicit in the user's task description, acceptance criteria, review comment, provided screenshot/mockup, or other user-supplied context. In that case, restate the explicit answer as confirmed scope and proceed.
- When the user provides a spreadsheet, screenshot, attachment, or other mockup artifact as the design reference, treat the most explicit provided artifact as the primary UI source of truth for that feature.
- Each business or technical question must be accompanied by the code check result in the same checkpoint.
- Business questions must be written in PM-friendly language so they can be forwarded directly to a product manager without rewriting.
- The first line of every business question must itself be a PM-facing question in plain product language, with no engineering shorthand, code terms, or implementation framing unless the user explicitly wants that level of detail.
- For every business question, include: the PM-facing question, the code checked, the code-derived answer/current product behavior, the requirement or requested behavior being compared against, the default recommendation, and whether explicit confirmation is still needed.
- When the current product behavior or wording can be shown in the UI, attach or reference the minimum screenshot evidence needed to make the decision concrete.
- Technical questions may stay engineering-facing, but for every technical question still include: the question, the code checked, the code-derived answer/current behavior, and whether that answer is sufficient to proceed or still needs explicit confirmation.
- Business questions are mandatory when the change affects who can perform an action, whether a read path is sensitive, whether a secondary failure should fail the primary action, whether a field still belongs to an endpoint, or which team/role should own a permission.
- Technical questions are mandatory when the change would alter permission architecture, widen or narrow an API contract, move logic between serializer/view/service layers, introduce a new local pattern, or add refactoring beyond the exact request/review.
- If the code clearly answers the question and does not conflict with the request, present that code-derived answer as the default recommendation instead of asking a blind question. For business questions, phrase this as a keep-vs-change product decision using plain language.
- If the code is ambiguous, contradictory, or clearly being changed by the request/review, still ask the question and cite the conflicting code paths so the user can decide with context. For business questions, summarize the conflict in PM-friendly terms before citing the code.
- Do not treat a significant behavior, permission, or API decision as a reasonable assumption. Ask first.
- If multiple user-provided artifacts or notes for the same feature appear to disagree, ask directly about the discrepancy before implementing the conflicting part.
- If the requirement is still unclear after checking the code and provided artifacts, recommend a short call or ask the user to paste meeting notes into chat instead of guessing.

