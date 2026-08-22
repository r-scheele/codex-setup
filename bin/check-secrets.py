#!/usr/bin/env python3
"""Fail closed when a snapshot looks like it contains credentials."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


FORBIDDEN_NAMES = {
    "auth.json",
    "caller-secret",
    "internal-secret",
    "session_index.jsonl",
}

PATTERNS = (
    ("API secret prefix", re.compile(r"\b(?:sk|sk-ant|xai)-[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("Google API key", re.compile(r"\bAIza[A-Za-z0-9_-]{20,}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("Bearer credential", re.compile(r"Bearer\s+[A-Za-z0-9._~-]{20,}", re.I)),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


def secret_strings(codex_home: Path):
    router = codex_home / "codex-router"
    candidates = list(router.glob("*.secret")) + [
        router / "caller-secret",
        router / "internal-secret",
    ]
    for path in candidates:
        if path.is_file():
            value = path.read_text(errors="ignore").strip()
            if len(value) >= 12:
                yield value

    auth = codex_home / "auth.json"
    if auth.is_file():
        try:
            payload = json.loads(auth.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return
        stack = [payload]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
            elif isinstance(value, str) and len(value) >= 20:
                yield value


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "snapshot").resolve()
    codex_home = Path(sys.argv[2] if len(sys.argv) > 2 else Path.home() / ".codex").resolve()
    known = tuple(secret_strings(codex_home))
    findings: list[tuple[Path, str]] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        lower = path.name.lower()
        if (
            lower in FORBIDDEN_NAMES
            or lower.endswith((".secret", ".sqlite", ".sqlite-shm", ".sqlite-wal", ".db", ".log"))
        ):
            findings.append((path, "forbidden filename"))
            continue
        if path.stat().st_size > 5_000_000:
            findings.append((path, "unexpected file larger than 5 MB"))
            continue
        raw = path.read_bytes()
        if b"\0" in raw:
            findings.append((path, "binary file is outside the backup allowlist"))
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            findings.append((path, "non-UTF-8 file is outside the backup allowlist"))
            continue
        if any(value in content for value in known):
            findings.append((path, "contains a known local credential"))
            continue
        for name, pattern in PATTERNS:
            if pattern.search(content):
                findings.append((path, name))
                break

    if findings:
        print("Secret check failed; nothing was committed or pushed.", file=sys.stderr)
        for path, reason in findings:
            print(f"- {path.relative_to(root)}: {reason}", file=sys.stderr)
        return 1
    print(f"Secret check passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

