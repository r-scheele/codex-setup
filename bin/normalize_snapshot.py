#!/usr/bin/env python3
"""Normalize machine paths and remove known local secret values."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        try:
            yield path, data.decode("utf-8")
        except UnicodeDecodeError:
            continue


def strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, str) and len(value) >= 20:
        yield value


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit("usage: normalize_snapshot.py SNAPSHOT HOME CODEX_HOME")

    root = Path(sys.argv[1]).resolve()
    home = Path(sys.argv[2]).resolve()
    codex_home = Path(sys.argv[3]).resolve()
    replacements: list[tuple[str, str]] = [(str(home), "__HOME__")]

    router = codex_home / "codex-router"
    caller = router / "caller-secret"
    if caller.is_file():
        value = caller.read_text().strip()
        if value:
            replacements.append((value, "__CODEX_ROUTER_CALLER_SECRET__"))

    for path in sorted(router.glob("*.secret")):
        value = path.read_text().strip()
        if value:
            replacements.append((value, "__REAUTHENTICATE__"))

    internal = router / "internal-secret"
    if internal.is_file():
        value = internal.read_text().strip()
        if value:
            replacements.append((value, "__LOCAL_ROUTER_SECRET__"))

    auth = codex_home / "auth.json"
    if auth.is_file():
        try:
            for value in strings(json.loads(auth.read_text())):
                replacements.append((value, "__REAUTHENTICATE__"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    replacements.sort(key=lambda item: len(item[0]), reverse=True)
    for path, content in text_files(root):
        updated = content
        for value, placeholder in replacements:
            updated = updated.replace(value, placeholder)
        if updated != content:
            path.write_text(updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

