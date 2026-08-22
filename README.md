# Codex setup backup

Private, automatic, secret-safe backup of Abdul's Codex configuration.

The snapshot follows Codex's documented layout: the user configuration is
`~/.codex/config.toml`, and named profile files live beside it as
`$CODEX_HOME/<profile>.config.toml`.

## What is backed up

- `config.toml` and every `*.config.toml` profile
- global `AGENTS.md`
- personal agents, rules, and skills
- shared `~/.agents/skills`
- automation definitions (`automation.toml` only)
- Codex Router provider/model selections, but never credentials
- Codex, router, and plugin version inventory

## What is never backed up

- ChatGPT/Codex authentication (`auth.json`)
- API keys, router caller/internal secrets, OAuth sessions, or Keychain data
- task transcripts, sessions, archives, attachments, browser data, or logs
- memories, SQLite databases, caches, generated media, or plugin package caches

Those exclusions are deliberate. Reproduction means restoring the setup and
then signing in again; it does not mean copying live credentials or private
task history between machines.

## Automatic sync

The macOS LaunchAgent watches the important configuration paths and also runs
every 15 minutes. It snapshots, checks for secrets, commits changes, and pushes
to this private repository. Offline commits are pushed on the next successful
run.

Run a manual sync at any time:

```sh
~/.codex-backup/bin/sync.sh
```

Check the automation:

```sh
launchctl print gui/$UID/com.rscheele.codex-setup-sync
tail -100 ~/Library/Logs/codex-setup-sync.log
```

## Restore on another Mac

1. Install Codex and GitHub CLI, then sign in to GitHub.
2. Clone this private repository:

   ```sh
   gh repo clone r-scheele/codex-setup ~/.codex-backup
   ```

3. Preview, then apply the restore:

   ```sh
   ~/.codex-backup/bin/restore.sh
   ~/.codex-backup/bin/restore.sh --apply
   ```

4. Reauthenticate the external providers using hidden local prompts:

   ```sh
   ~/.codex-backup/bin/reauthenticate.sh
   ```

5. Sign in to Codex with ChatGPT, install the auto-sync LaunchAgent, fully quit
   and reopen Codex:

   ```sh
   codex login
   ~/.codex-backup/bin/install-auto-sync.sh
   ```

The restore creates a timestamped backup under `~/Documents/Codex Backups`
before replacing any top-level configuration file.

Official reference: [Codex configuration reference](https://developers.openai.com/codex/config-reference/).

