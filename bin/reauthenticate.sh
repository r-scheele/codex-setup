#!/bin/zsh
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
router_dir="$HOME/.local/share/codex-router"
providers_file="$repo_root/snapshot/router/enabled-providers.json"

[[ -x "$router_dir/bin/provider-key" ]] || {
  print -u2 "Codex Router is not installed at $router_dir"
  exit 1
}
[[ -f "$providers_file" ]] || {
  print -u2 "Missing provider snapshot: $providers_file"
  exit 1
}

providers=("${(@f)$(jq -r '.providers[]' "$providers_file")}")
for provider in $providers; do
  case "$provider" in
    opencode-free)
      print 'OpenCode Free needs no credential.'
      ;;
    kimi-oauth)
      if command -v kimi >/dev/null; then
        kimi login
      else
        print -u2 'Install the official Kimi CLI, then run: kimi login'
      fi
      ;;
    anthropic-api|deepseek|grok-api|opencode-go|zai-coding|zai-api)
      "$router_dir/bin/provider-key" "$provider" set
      ;;
    *)
      print -u2 "Provider needs manual authentication: $provider"
      ;;
  esac
  "$router_dir/bin/model-router" codex providers enable "$provider" || true
done

"$router_dir/bin/control" picker all show
"$router_dir/bin/model-router" codex doctor

