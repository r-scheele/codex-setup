## Pre-Commit Self-Review Checklist

Apply checks relevant to the actual diff before an authorized commit. Check migration dependencies/order when migrations changed; DRF validation and mixin hooks when API code changed; transaction scope when writes changed; and tenant, role, synchronized state, and responsive UI when those surfaces changed. Review every hunk for task scope. Do not require an unrelated creation flow or a full UI matrix for a backend-only edit.
