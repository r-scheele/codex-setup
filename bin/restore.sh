#!/bin/zsh
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
snapshot="$repo_root/snapshot"
codex_home="${CODEX_HOME:-$HOME/.codex}"
router_dir="$HOME/.local/share/codex-router"

if [[ "${1:-}" != "--apply" ]]; then
  cat <<EOF
Restore preview only. Nothing changed.

This will:
1. Back up the existing Codex configuration under ~/Documents/Codex Backups.
2. Install Codex Router in idle mode without reading or restoring credentials.
3. Restore config, profiles, AGENTS.md, agents, rules, skills, and automation definitions.
4. Restore router provider/model selections.
5. Leave ChatGPT, OAuth, and API-key authentication for you to redo locally.

Run: $repo_root/bin/restore.sh --apply
EOF
  exit 0
fi

command -v codex >/dev/null || {
  print -u2 'Codex must be installed before restore.'
  exit 1
}

python3 "$repo_root/bin/check-secrets.py" "$snapshot" "$codex_home"

timestamp="$(date +%Y%m%d-%H%M%S)"
backup="$HOME/Documents/Codex Backups/before-restore-$timestamp"
mkdir -p "$backup" "$codex_home"

for item in "$codex_home/config.toml" "$codex_home/AGENTS.md" "$codex_home"/*.config.toml(N); do
  [[ -f "$item" ]] || continue
  cp -p "$item" "$backup/"
done

if [[ ! -d "$router_dir/.git" ]]; then
  mkdir -p "${router_dir:h}"
  git clone https://github.com/duolahypercho/codex-router.git "$router_dir"
else
  git -C "$router_dir" pull --ff-only
fi

"$router_dir/install.sh" --target codex --no-provider --no-discovery --no-tray

caller_secret=""
if [[ -f "$codex_home/codex-router/caller-secret" ]]; then
  caller_secret="$(<"$codex_home/codex-router/caller-secret")"
fi

restore_text_file() {
  local source="$1"
  local destination="$2"
  [[ -f "$source" ]] || return 0
  mkdir -p "${destination:h}"
  SOURCE_HOME="$HOME" CALLER_SECRET="$caller_secret" python3 - "$source" "$destination" <<'PY'
import os
import sys
from pathlib import Path

source, destination = map(Path, sys.argv[1:])
content = source.read_text()
content = content.replace('__HOME__', os.environ['SOURCE_HOME'])
if os.environ.get('CALLER_SECRET'):
    content = content.replace('__CODEX_ROUTER_CALLER_SECRET__', os.environ['CALLER_SECRET'])
destination.write_text(content)
PY
}

restore_tree() {
  local source="$1"
  local destination="$2"
  [[ -d "$source" ]] || return 0
  mkdir -p "$destination"
  /usr/bin/rsync -a "$source/" "$destination/"
  while IFS= read -r -d '' file; do
    SOURCE_HOME="$HOME" CALLER_SECRET="$caller_secret" python3 - "$file" <<'PY'
import os
import sys
from pathlib import Path

path = Path(sys.argv[1])
raw = path.read_bytes()
if b'\0' in raw:
    raise SystemExit(0)
try:
    content = raw.decode('utf-8')
except UnicodeDecodeError:
    raise SystemExit(0)
content = content.replace('__HOME__', os.environ['SOURCE_HOME'])
if os.environ.get('CALLER_SECRET'):
    content = content.replace('__CODEX_ROUTER_CALLER_SECRET__', os.environ['CALLER_SECRET'])
path.write_text(content)
PY
  done < <(find "$destination" -type f -print0)
}

restore_text_file "$snapshot/codex/config.toml" "$codex_home/config.toml"
restore_text_file "$snapshot/codex/AGENTS.md" "$codex_home/AGENTS.md"
for profile in "$snapshot/codex"/*.config.toml(N); do
  restore_text_file "$profile" "$codex_home/${profile:t}"
done
restore_tree "$snapshot/codex/agents" "$codex_home/agents"
restore_tree "$snapshot/codex/rules" "$codex_home/rules"
restore_tree "$snapshot/codex/skills" "$codex_home/skills"
restore_tree "$snapshot/agents-home/skills" "$HOME/.agents/skills"
restore_tree "$snapshot/automations" "$codex_home/automations"

for policy in enabled-providers.json model-picker.json discovery-mode.json user-models.json; do
  [[ -f "$snapshot/router/$policy" ]] || continue
  cp -p "$snapshot/router/$policy" "$codex_home/codex-router/$policy"
done

"$router_dir/bin/refresh-catalog"
"$router_dir/bin/model-router" codex start

cat <<EOF
Restore complete.

Backup: $backup

Next:
1. Run $repo_root/bin/reauthenticate.sh
2. Run codex login
3. Run $repo_root/bin/install-auto-sync.sh
4. Fully quit and reopen Codex
EOF

