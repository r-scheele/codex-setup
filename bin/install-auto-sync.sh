#!/bin/zsh
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
template="$repo_root/launchd/com.rscheele.codex-setup-sync.plist"
target="$HOME/Library/LaunchAgents/com.rscheele.codex-setup-sync.plist"
log_dir="$HOME/Library/Logs"

mkdir -p "${target:h}" "$log_dir"

REPO_ROOT="$repo_root" USER_HOME="$HOME" python3 - "$template" "$target" <<'PY'
import os
import sys
from pathlib import Path

source, destination = map(Path, sys.argv[1:])
content = source.read_text()
content = content.replace('__REPO__', os.environ['REPO_ROOT'])
content = content.replace('__HOME__', os.environ['USER_HOME'])
destination.write_text(content)
PY

chmod 600 "$target"
launchctl bootout "gui/$UID" "$target" 2>/dev/null || true
launchctl bootstrap "gui/$UID" "$target"
launchctl kickstart -k "gui/$UID/com.rscheele.codex-setup-sync"
print "Automatic Codex setup sync installed: $target"

