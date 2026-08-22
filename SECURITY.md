# Security boundary

This repository must remain private, but privacy is not treated as the only
protection.

`bin/snapshot.sh` uses a strict allowlist, replaces the home directory and the
router caller capability with placeholders, and runs `bin/check-secrets.py`
before changing the tracked snapshot. `bin/sync.sh` repeats that check before
every commit and push.

If the checker reports a file, automatic sync stops. It prints the file path
and reason, never the suspected value.

Never add any of these manually:

- `~/.codex/auth.json`
- `~/.codex/codex-router/*.secret`
- `~/.codex/codex-router/caller-secret`
- `~/.codex/codex-router/internal-secret`
- `~/.kimi`, `~/.grok`, or provider CLI authentication stores
- session, transcript, attachment, browser, memory, log, or SQLite data

If a credential is ever committed, revoke it at the provider first, remove it
from Git history, and rotate the repository's GitHub access credentials.

