#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".webm"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def list_files(root, exts):
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts]


def load_research(project_dir):
    path = project_dir / "research" / "youtube_research.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    args = parser.parse_args()
    project_dir = Path(args.project_dir).expanduser()
    research = load_research(project_dir)
    records = research.get("records", [])[:12]
    manifest = load_json(project_dir / "manifest.json")
    selected_match = load_json(project_dir / "research" / "selected_footballia_match.json")

    videos = list_files(project_dir / "source", VIDEO_EXTS)
    audios = list_files(project_dir / "audio", AUDIO_EXTS)
    images = list_files(project_dir / "source", IMAGE_EXTS)

    research_lines = []
    for r in records[:8]:
        views = r.get("view_count")
        views_text = f"{views:,}" if isinstance(views, int) else "unknown"
        research_lines.append(f"- {r.get('title')} ({views_text} views): {', '.join(r.get('viral_reasons', []))}")

    video_lines = "\n".join(f"- `{p}`" for p in videos) or "- No source video found yet."
    audio_lines = "\n".join(f"- `{p}`" for p in audios) or "- No separate music file found; use source audio/commentary."
    research_text = "\n".join(research_lines) or "- No research file found; use the viral-patterns reference and run YouTube research first."
    source_strategy = []
    if selected_match:
        source_strategy.append(f"- Selected Footballia match: {selected_match.get('title')}")
        source_strategy.append(f"- Match URL: {selected_match.get('url')}")
        source_strategy.append(
            "- Selection signal: "
            + ", ".join(selected_match.get("rank_reasons") or ["recent Footballia source candidate"])
        )
        source_strategy.append(
            f"- Match metadata: season {selected_match.get('season') or 'unknown'}, "
            f"score {selected_match.get('score') or 'unknown'}, views {selected_match.get('views') or 0:,}"
        )
    elif manifest.get("footbalia_url"):
        source_strategy.append(f"- Footbalia/Footballia URL: {manifest['footbalia_url']}")
    source_strategy_text = "\n".join(source_strategy) or "- No Footballia selection metadata found."

    prompt = f"""# Palmier Pro Edit Prompt

Use palmier-pro to create an upload-ready football YouTube edit from the media in:

`{project_dir}`

## Source Files

Video:
{video_lines}

Audio:
{audio_lines}

Images:
{chr(10).join(f"- `{p}`" for p in images) or "- none"}

## Footballia Source Strategy

{source_strategy_text}

## Fresh Viral Research Signals

{research_text}

## Edit Objective

Create a 60-90 second football edit for English-speaking Europe and US viewers that feels like current viral YouTube football compilations: immediate payoff, fast clip variety, goals/skills/fails/reactions, strong audio rhythm, and packaging for easy upload.

Prioritize monetization-safe transformation: add a clear storyline, meaningful sequence choices, original captions/labels, audio rhythm, and visual effects so the result is not just minimally changed match footage.

## Palmier Workflow

1. Call `get_timeline` once.
2. Call `get_media`; import every local video/audio file above with `import_media` if missing.
3. Inspect source video with `inspect_media` overview first. Use `search_media` to find:
   - goals, shots, saves, celebrations
   - skills, dribbles, nutmegs, tackles
   - funny failures, misses, slips, referee chaos
   - crowd/player reactions and closeups
4. Choose the strongest viral angle from the footage:
   - "Best goals/skills/fails" if there is broad variety.
   - "Superhuman/impossible moments" if the best clips are elite or shocking.
   - "Funny football moments" if the best clips are mistakes and reactions.
   - "Champions League/Premier League chaos" if the source features elite European clubs or English-speaking audience interest.
5. Build the edit:
   - 0-3s: strongest visual payoff first.
   - 3-12s: rapid identity setup, 3-5 clips.
   - 12-45s: alternating goals, skills, fails, reactions.
   - 45-70s: densest premium moments, fastest cutting.
   - 70-90s if needed: final payoff and quick end card.
6. Use mostly hard cuts. Keep most clips 1-4 seconds; use shorter bursts for impact sequences.
7. Add sparse English text overlays only for category labels, storyline beats, or punchlines: "IMPOSSIBLE", "SKILL", "FAIL", "LAST MINUTE", "WHAT A FINISH".
8. Keep grading punchy and social-video friendly: contrast, vivid grass, clear ball/player visibility.
9. Add captions only for commentary/dialogue that improves the hook or joke.
10. Do not call paid generation tools unless the user confirms the exact generation action.

## Folder Deliverables

After editing, update:

- `{project_dir}/run_report.md`
- `{project_dir}/youtube_title_options.md`
- `{project_dir}/description.md`
- `{project_dir}/tags.txt`
- `{project_dir}/thumbnail/thumbnail_prompt.md`

If Palmier export is unavailable through MCP, say so in `run_report.md` and specify the exact manual export location:

`{project_dir}/exports/`
"""

    (project_dir / "palmier_prompt.md").write_text(prompt)

    title_options = [
        "1 in a Million Football Moments You Need To See",
        "Champions League Moments That Look Unreal",
        "Best Football Goals, Skills and Fails That Went Viral",
        "Premier League and UCL Chaos: Goals, Skills and Fails",
        "Superhuman Football Moments That Look Unreal",
    ]
    (project_dir / "youtube_title_options.md").write_text(
        "# YouTube Title Options\n\n" + "\n".join(f"- {t}" for t in title_options) + "\n"
    )
    (project_dir / "description.md").write_text(
        "Best football moments, goals, skills, fails and reactions in one fast English-language edit for football fans in Europe, the UK and the US.\n\n"
        "Like, subscribe, and comment your favorite moment.\n\n"
        "#football #soccer #championsleague #premierleague #goals #skills #fails #footballreels #footballshorts\n"
    )
    (project_dir / "tags.txt").write_text(
        "football,soccer,champions league,premier league,ucl,football edits,football goals,football skills,football fails,funny football,football compilation,football reels,tiktok football,viral football,european football,usa soccer\n"
    )
    (project_dir / "thumbnail" / "thumbnail_prompt.md").write_text(
        "# Thumbnail Prompt\n\n"
        "Create a high-contrast football thumbnail: one player mid-action, visible ball, shocked reaction face or keeper dive, bright grass, bold 2-4 word text such as IMPOSSIBLE or VIRAL MOMENTS. Avoid clutter.\n"
    )
    print(project_dir / "palmier_prompt.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
