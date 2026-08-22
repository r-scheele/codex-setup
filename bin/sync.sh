#!/bin/zsh
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
lock_dir="$repo_root/.sync.lock"

if ! mkdir "$lock_dir" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$lock_dir" 2>/dev/null || true' EXIT

cd "$repo_root"
git pull --rebase --autostash origin main
"$repo_root/bin/snapshot.sh"
python3 "$repo_root/bin/check-secrets.py" "$repo_root/snapshot" "${CODEX_HOME:-$HOME/.codex}"

git add --all
if ! git diff --cached --quiet; then
  machine="$(scutil --get ComputerName 2>/dev/null || hostname)"
  git commit -m "Sync Codex setup from $machine at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi

if [[ "$(git rev-list --count origin/main..HEAD 2>/dev/null || printf '0')" -gt 0 ]]; then
  git push origin main
fi

