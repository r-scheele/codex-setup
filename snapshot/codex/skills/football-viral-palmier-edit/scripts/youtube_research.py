#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_QUERIES = [
    "football moments that look scripted",
    "1 in a million football moments",
    "1 in a trillion football moments",
    "moments that can't be repeated in football",
    "when football is turned into art",
    "football comeback moments",
    "champions league comeback goals commentary",
    "football goals with real commentary",
    "football goals explained tactical analysis",
    "Champions League football edits goals skills viral English",
    "Premier League football edits funny moments goals skills viral",
]


def run_json(args, timeout=60):
    cp = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    if cp.returncode != 0:
        return []
    rows = []
    for line in cp.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def normalize_url(item):
    vid = item.get("id")
    return item.get("webpage_url") or item.get("url") or (f"https://www.youtube.com/watch?v={vid}" if vid else "")


def classify(title):
    t = title.lower()
    labels = []
    for key in [
        "funny",
        "fails",
        "goals",
        "skills",
        "superhuman",
        "impossible",
        "million",
        "billion",
        "trillion",
        "scripted",
        "repeated",
        "art",
        "beauty",
        "comeback",
        "commentary",
        "explained",
        "analysis",
        "tutorial",
        "ways",
        "reels",
        "tiktok",
    ]:
        if key in t:
            labels.append(key)
    return labels or ["football"]


def reason(item):
    title = item.get("title") or ""
    labels = classify(title)
    reasons = []
    if any(x in labels for x in ["million", "trillion", "impossible", "superhuman"]):
        reasons.append("curiosity-gap spectacle promise")
    if any(x in labels for x in ["scripted", "repeated", "art", "beauty"]):
        reasons.append("shareable wonder/emotion framing")
    if any(x in labels for x in ["comeback", "commentary"]):
        reasons.append("story and broadcast-emotion hook")
    if any(x in labels for x in ["explained", "analysis"]):
        reasons.append("transformative explanation angle")
    if any(x in labels for x in ["funny", "fails"]):
        reasons.append("shareable humor/fail payoff")
    if any(x in labels for x in ["goals", "skills"]):
        reasons.append("dense football payoff keywords")
    if any(x in labels for x in ["reels", "tiktok"]):
        reasons.append("repackaged short-form format")
    if any(x in labels for x in ["tutorial", "ways"]):
        reasons.append("clear utility/listicle intent")
    if not reasons:
        reasons.append("football highlight demand")
    return reasons


def build_pattern_board(records):
    high_view = [r for r in records if (r.get("view_count") or 0) >= 1_000_000]
    labels = {}
    for record in high_view:
        for label in record.get("labels", []):
            labels[label] = labels.get(label, 0) + 1
    top_labels = sorted(labels.items(), key=lambda item: item[1], reverse=True)[:12]
    return {
        "high_view_count": len(high_view),
        "top_labels": top_labels,
        "title_formulas": [
            "1 in a Million/Trillion Football Moments",
            "Football Moments That Look Scripted",
            "Moments That Can't Be Repeated in Football",
            "When Football Turns Into Art",
            "The Comeback That Changed Everything",
            "Every Goal Explained: <Match>",
        ],
        "thumbnail_cues": [
            "2-4 words max",
            "scoreline or minute if it creates shock",
            "visible ball/player/reaction",
            "yellow/white text on dark contrast",
            "one emotional promise: CHAOS, SCRIPTED, 90+3, EXPLAINED",
        ],
        "edit_rules_to_adapt_not_copy": [
            "open with the strongest payoff or question",
            "make each moment complete enough to satisfy football viewers",
            "use original captions/analysis to explain why the moment matters",
            "avoid straight highlight dumps",
            "for copyright-risk cuts, use original narration, annotations, still-frame analysis, and short evidence clips",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--limit", type=int, default=10, help="Results per query")
    parser.add_argument("--seed-url", action="append", default=[], help="Reference YouTube URL to include")
    parser.add_argument("--query", action="append", default=[], help="Additional ytsearch query")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    seen = {}
    for url in args.seed_url:
        rows = run_json(["yt-dlp", "--skip-download", "--dump-json", "--no-warnings", url], timeout=90)
        for item in rows:
            if item.get("id"):
                seen[item["id"]] = item

    for q in (args.query or DEFAULT_QUERIES):
        rows = run_json(
            ["yt-dlp", "--skip-download", "--dump-json", "--flat-playlist", "--no-warnings", f"ytsearch{args.limit}:{q}"],
            timeout=90,
        )
        for item in rows:
            title = item.get("title") or ""
            vid = item.get("id")
            if not vid or vid in seen:
                continue
            if not re.search(r"football|soccer|goal|skill|fail|moment|edit", title, re.I):
                continue
            seen[vid] = item

    records = []
    for item in seen.values():
        record = {
            "id": item.get("id"),
            "title": item.get("title"),
            "uploader": item.get("uploader") or item.get("channel"),
            "duration": item.get("duration"),
            "view_count": item.get("view_count"),
            "like_count": item.get("like_count"),
            "comment_count": item.get("comment_count"),
            "upload_date": item.get("upload_date"),
            "url": normalize_url(item),
            "labels": classify(item.get("title") or ""),
            "viral_reasons": reason(item),
        }
        records.append(record)

    records.sort(key=lambda r: (r.get("view_count") or 0), reverse=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "summary": {
            "count": len(records),
            "common_promises": [
                "1 in a million/trillion",
                "scripted-looking moments",
                "can't be repeated",
                "football as art",
                "comeback chaos",
                "goals explained",
            ],
            "recommended_template": "commentary/analysis-led key-moment story unless source has a stronger funny or superhuman angle",
        },
        "pattern_board": build_pattern_board(records),
    }

    (out_dir / "youtube_research.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    board = payload["pattern_board"]
    lines = ["# YouTube Viral Research", "", f"Generated: {payload['generated_at']}", ""]
    lines.append("## Pattern Board")
    lines.append("")
    lines.append(f"High-view references found: {board['high_view_count']}")
    lines.append("")
    lines.append("Title formulas to adapt, not copy:")
    lines.extend(f"- {item}" for item in board["title_formulas"])
    lines.append("")
    lines.append("Thumbnail cues:")
    lines.extend(f"- {item}" for item in board["thumbnail_cues"])
    lines.append("")
    lines.append("Edit rules:")
    lines.extend(f"- {item}" for item in board["edit_rules_to_adapt_not_copy"])
    lines.append("")
    lines.append("## References")
    lines.append("")
    for i, r in enumerate(records[:25], 1):
        views = r.get("view_count")
        views_text = f"{views:,}" if isinstance(views, int) else "unknown"
        lines.append(f"{i}. [{r['title']}]({r['url']})")
        lines.append(f"   Views: {views_text}; labels: {', '.join(r['labels'])}")
        lines.append(f"   Why: {', '.join(r['viral_reasons'])}")
    (out_dir / "youtube_research.md").write_text("\n".join(lines) + "\n")
    print(out_dir / "youtube_research.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
