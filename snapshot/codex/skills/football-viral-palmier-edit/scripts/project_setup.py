#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ROOT = Path("__HOME__/Desktop/premier-pro")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:90] or "football-edit"


def unique_path(root: Path, slug: str) -> Path:
    candidate = root / slug
    if not candidate.exists():
        return candidate
    for i in range(2, 1000):
        candidate = root / f"{slug}-{i}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("Could not find a unique project folder name")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", help="Match/video title for the project folder")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Output root folder")
    parser.add_argument("--footbalia-url", default="", help="Optional Footbalia/Footballia match URL")
    parser.add_argument(
        "--footballia-selection-json",
        default="",
        help="Optional selected_footballia_match.json from footballia_discovery.py",
    )
    args = parser.parse_args()

    title = args.title
    footbalia_url = args.footbalia_url
    if args.footballia_selection_json:
        selection = json.loads(Path(args.footballia_selection_json).expanduser().read_text())
        title = title or selection.get("title")
        footbalia_url = footbalia_url or selection.get("url", "")
    if not title:
        parser.error("--title is required unless --footballia-selection-json provides a title")

    root = Path(args.root).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    project_dir = unique_path(root, slugify(title))
    for sub in ["source", "audio", "research", "exports", "thumbnail", "working"]:
        (project_dir / sub).mkdir(parents=True, exist_ok=True)

    manifest = {
        "title": title,
        "project_dir": str(project_dir),
        "footbalia_url": footbalia_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "created",
    }
    (project_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (project_dir / "run_report.md").write_text(
        f"# Run Report\n\nProject: {title}\n\nFolder: `{project_dir}`\n\nStatus: created.\n"
    )
    print(project_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
