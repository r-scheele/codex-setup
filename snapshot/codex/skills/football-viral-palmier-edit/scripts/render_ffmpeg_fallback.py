#!/usr/bin/env python3
import argparse
import json
import math
import re
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".webm"}
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def run(cmd):
    cp = subprocess.run(cmd, text=True, capture_output=True)
    if cp.returncode != 0:
        raise SystemExit(cp.stderr or cp.stdout or f"Command failed: {cmd}")
    return cp


def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return re.sub(r"-+", "-", value).strip("-") or "football-edit"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def first_source_video(project_dir):
    source_dir = project_dir / "source"
    videos = sorted(p for p in source_dir.rglob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTS)
    if not videos:
        raise SystemExit(f"No source video found in {source_dir}")
    return videos[0]


def probe_duration(path):
    cp = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
    )
    return float(cp.stdout.strip())


def pick_segments(source_duration, target_duration, segment_duration):
    if source_duration <= target_duration + 0.25:
        return [(0, max(0.1, source_duration))]

    count = max(1, math.ceil(target_duration / segment_duration))
    usable_segment = min(segment_duration, max(0.5, source_duration / count))
    latest_start = max(0.0, source_duration - usable_segment - 0.1)
    anchors = []
    for i in range(count):
        fraction = i / max(1, count - 1)
        start = min(latest_start, fraction * latest_start)
        anchors.append((round(start, 3), round(min(source_duration, start + usable_segment), 3)))
    return anchors


def ffmpeg_text(value):
    return value.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def fit_font(text, max_width, start_size):
    size = start_size
    while size >= 24:
        font = ImageFont.truetype(FONT, size=size)
        left, top, right, bottom = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textbbox((0, 0), text, font=font, stroke_width=6)
        if right - left <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT, size=24)


def make_text_overlay(path, text, width, height, color, font_size):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = fit_font(text, width - 40, font_size)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font, stroke_width=6)
    x = (width - (right - left)) // 2
    y = (height - (bottom - top)) // 2 - top
    draw.text((x, y), text, font=font, fill=color, stroke_width=6, stroke_fill=(0, 0, 0, 220))
    image.save(path)


def make_overlays(project_dir, title):
    working = project_dir / "working"
    working.mkdir(parents=True, exist_ok=True)
    title_overlay = working / "fallback-title.png"
    lower_overlay = working / "fallback-lower.png"
    title_text = title[:38].upper()
    make_text_overlay(title_overlay, title_text, 1500, 170, (255, 255, 255, 255), 66)
    make_text_overlay(lower_overlay, "WHAT A MOMENT", 1100, 140, (255, 222, 89, 255), 64)
    return title_overlay, lower_overlay


def build_filter(segments):
    width = 1920
    height = 1080
    parts = []
    labels = []
    for i, (start, end) in enumerate(segments):
        parts.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,"
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},setsar=1[v{i}]"
        )
        parts.append(f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    concat = "".join(labels) + f"concat=n={len(segments)}:v=1:a=1[vcat][acat]"
    video = (
        "[vcat][1:v]overlay=(W-w)/2:58:enable='between(t,0,3.5)'[vtitle];"
        "[vtitle][2:v]overlay=(W-w)/2:H-h-150:enable='between(t,4,7.5)',format=yuv420p[vout]"
    )
    audio = "[acat]loudnorm=I=-16:LRA=11:TP=-1.5[aout]"
    return ";".join(parts + [concat, video, audio])


def render_video(project_dir, source, title, target_duration, segment_duration):
    output_dir = project_dir / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)
    duration = probe_duration(source)
    segments = pick_segments(duration, target_duration, segment_duration)
    output = output_dir / f"{slugify(title)}-fallback-edit.mp4"
    title_overlay, lower_overlay = make_overlays(project_dir, title)
    filter_complex = build_filter(segments)
    output_duration = sum(end - start for start, end in segments)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-loop",
        "1",
        "-i",
        str(title_overlay),
        "-loop",
        "1",
        "-i",
        str(lower_overlay),
        "-filter_complex",
        filter_complex,
        "-map",
        "[vout]",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{output_duration:.3f}",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output),
    ]
    run(cmd)
    return output, segments


def render_thumbnail(project_dir, source, title, segments):
    thumb_dir = project_dir / "thumbnail"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    thumb = thumb_dir / "thumbnail.jpg"
    raw_thumb = thumb_dir / "thumbnail_base.jpg"
    seek = segments[min(1, len(segments) - 1)][0]
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(seek),
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-vf",
            "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
            "-q:v",
            "2",
            str(raw_thumb),
        ]
    )
    image = Image.open(raw_thumb).convert("RGB")
    draw = ImageDraw.Draw(image)
    text = "UCL CHAOS" if "champions" in title.lower() else "VIRAL MOMENT"
    font = fit_font(text, 1700, 130)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font, stroke_width=10)
    draw.text(
        ((image.width - (right - left)) // 2, image.height - 230),
        text,
        font=font,
        fill=(255, 222, 89),
        stroke_width=10,
        stroke_fill=(0, 0, 0),
    )
    image.save(thumb, quality=92)
    raw_thumb.unlink(missing_ok=True)
    return thumb


def append_report(project_dir, output, thumb, segments):
    report = project_dir / "run_report.md"
    text = report.read_text() if report.exists() else "# Run Report\n"
    text += (
        "\n## FFmpeg Fallback Render\n\n"
        f"Rendered at: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"Final video: `{output}`\n\n"
        f"Thumbnail: `{thumb}`\n\n"
        f"Segments: {', '.join(f'{s:.1f}-{e:.1f}s' for s, e in segments)}\n"
    )
    report.write_text(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--target-duration", type=float, default=75)
    parser.add_argument("--segment-duration", type=float, default=3)
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser()
    manifest = load_json(project_dir / "manifest.json")
    title = manifest.get("title") or project_dir.name.replace("-", " ")
    source = first_source_video(project_dir)
    output, segments = render_video(project_dir, source, title, args.target_duration, args.segment_duration)
    thumb = render_thumbnail(project_dir, source, title, segments)
    append_report(project_dir, output, thumb, segments)
    print(output)


if __name__ == "__main__":
    main()
