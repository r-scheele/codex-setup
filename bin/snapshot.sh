#!/bin/zsh
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
source_home="${CODEX_SETUP_SOURCE_HOME:-$HOME}"
codex_home="${CODEX_HOME:-$source_home/.codex}"
snapshot_dir="$repo_root/snapshot"
stage="$(mktemp -d "${TMPDIR:-/tmp}/codex-setup-snapshot.XXXXXX")"

cleanup() {
  if [[ -n "${stage:-}" && "$stage" == *codex-setup-snapshot.* && -d "$stage" ]]; then
    rm -rf "$stage"
  fi
}
trap cleanup EXIT

mkdir -p "$stage/codex" "$stage/router" "$stage/agents-home" "$stage/automations" "$stage/inventory"

copy_file() {
  local source="$1"
  local destination="$2"
  [[ -f "$source" ]] || return 0
  mkdir -p "$(dirname "$destination")"
  cp -p "$source" "$destination"
}

copy_tree() {
  local source="$1"
  local destination="$2"
  shift 2
  [[ -d "$source" ]] || return 0
  mkdir -p "$destination"
  /usr/bin/rsync -a \
    --exclude '.DS_Store' \
    --exclude '.git/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude 'node_modules/' \
    "$@" "$source/" "$destination/"
}

copy_file "$codex_home/config.toml" "$stage/codex/config.toml"
copy_file "$codex_home/AGENTS.md" "$stage/codex/AGENTS.md"
for profile in "$codex_home"/*.config.toml(N); do
  copy_file "$profile" "$stage/codex/${profile:t}"
done

copy_tree "$codex_home/agents" "$stage/codex/agents"
copy_tree "$codex_home/rules" "$stage/codex/rules"
copy_tree "$codex_home/skills" "$stage/codex/skills" --exclude '.system/'
copy_tree "$source_home/.agents/skills" "$stage/agents-home/skills"

if [[ -d "$codex_home/automations" ]]; then
  while IFS= read -r -d '' automation; do
    relative="${automation#$codex_home/automations/}"
    copy_file "$automation" "$stage/automations/$relative"
  done < <(find "$codex_home/automations" -name automation.toml -type f -print0)
fi

for policy in enabled-providers.json model-picker.json discovery-mode.json user-models.json; do
  copy_file "$codex_home/codex-router/$policy" "$stage/router/$policy"
done

{
  printf 'machine=%s\n' "$(scutil --get ComputerName 2>/dev/null || hostname)"
  printf 'macos=%s\n' "$(sw_vers -productVersion 2>/dev/null || true)"
  printf 'codex=%s\n' "$(codex --version 2>/dev/null || true)"
  if [[ -d "$source_home/.local/share/codex-router/.git" ]]; then
    printf 'router_commit=%s\n' "$(git -C "$source_home/.local/share/codex-router" rev-parse HEAD 2>/dev/null || true)"
    printf 'router_remote=%s\n' "$(git -C "$source_home/.local/share/codex-router" remote get-url origin 2>/dev/null || true)"
  fi
} > "$stage/inventory/versions.txt"

if [[ -d "$codex_home/plugins/cache" ]]; then
  find "$codex_home/plugins/cache" -mindepth 3 -maxdepth 3 -type d \
    | sed "s#^$codex_home/plugins/cache/##" \
    | LC_ALL=C sort > "$stage/inventory/plugin-cache-versions.txt"
fi

python3 "$repo_root/bin/normalize_snapshot.py" "$stage" "$source_home" "$codex_home"
python3 "$repo_root/bin/check-secrets.py" "$stage" "$codex_home"

mkdir -p "$snapshot_dir"
/usr/bin/rsync -a --delete "$stage/" "$snapshot_dir/"
printf 'Snapshot updated: %s\n' "$snapshot_dir"
