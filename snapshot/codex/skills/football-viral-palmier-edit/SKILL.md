---
name: football-viral-palmier-edit
description: Use when creating autonomous football or soccer YouTube edits from Footbalia/Footballia or local match footage with Palmier Pro, including viral-format research, project folder setup, Palmier edit prompts, thumbnails, titles, descriptions, tags, and upload-ready deliverables.
---

# Football Viral Palmier Edit

## Goal

Create an upload-ready football edit project folder from a match/video source, using fresh YouTube research and Palmier Pro editing. Default output root:

`__HOME__/Desktop/premier-pro`

Each run creates one child folder named after the video or match.

Default business target: English-speaking Europe, the UK, and the US. Optimize source selection, titles, thumbnails, captions, and descriptions for those audiences unless the user asks for a different market.

## Required Rules

- Do not place raw credentials in skill files, prompts, reports, or deliverables. Footbalia credentials are expected in macOS Keychain services `codex-footbalia-username` and `codex-footbalia-password`, or in runtime env vars `FOOTBALIA_EMAIL` and `FOOTBALIA_PASSWORD`.
- Download only from an authenticated/authorized Footbalia session, a user-provided local file, or a direct URL the user is allowed to use. Do not bypass DRM, CAPTCHAs, paywalls, or browser security interstitials.
- Use `palmier-pro` for timeline/media work. If this thread cannot see Palmier as callable MCP tools, call its local MCP endpoint at `http://127.0.0.1:19789/mcp`.
- Palmier MCP requires Palmier Pro to be running with a `.palmier` project open. If `get_timeline` or `get_media` returns `Editor not available`, open an existing/scratch `.palmier` project first, then retry.
- Do not call paid Palmier generation tools unless the user explicitly confirms the exact model, prompt, duration, and cost-bearing action.
- Aim for autonomy. Ask the user only for missing essentials: target Footbalia URL/match, source folder, or explicit confirmation for paid generation/export blockers.
- Protect monetization potential by making reused footage meaningfully transformative: add storyline, commentary-style captions, substantive sequencing, visual rhythm, key-moment emphasis, and context. Do not produce plain copied match-clip dumps. This improves originality but does not guarantee monetization or eliminate match-footage/commentary rights risk.
- Default audio direction is commentary/crowd-only. Do not add songs or commercial music unless the user explicitly asks for music again. Prefer original match commentary/crowd for future football edits, with loudness cleanup, compression, and key-moment emphasis.
- If YouTube reports "Copyright-protected content found" or blocks viewing, do not try evasion tricks such as mirroring, pitch-shifting, heavy cropping, fake borders, or speed changes meant to hide the match. Rebuild as a more genuinely transformative analysis/story cut: remove broadcast audio, use original narration or captions, convert long live clips into annotated still-frame analysis, use short evidence moments only when needed, add original graphics/context, and clearly document that this reduces risk but cannot guarantee clearance.
- For original narration, prefer a human-sounding TTS workflow. If `OPENAI_API_KEY` is securely configured, use OpenAI speech generation such as `gpt-4o-mini-tts` with voice/style instructions for football-analysis delivery. Never paste API keys into chat, skill files, prompts, reports, or upload folders. If no secure OpenAI key is available, fall back to a local/free TTS tool such as `edge-tts`, then verify the rendered voiceover by listening/spot-checking.
- For goal-based football edits, never clip only the final shot or aftermath. Each goal sequence must start where the playmaking starts, continue through the finish, and end with the goal scorer's celebration. If this makes the edit longer than the target length, prioritize complete football moments over the nominal duration.
- Avoid repeated full-screen score cards or title cards between every goal. Use smooth transitions and compact context labels unless a single opening/end card is truly needed.
- Avoid generic "AI edit" tells: do not overuse giant captions, random effects, repeated templates, abrupt unexplained jumps, unrelated overlays, or scoreboard cards that interrupt the football. Every effect should support the play, the song, or the story.
- When music is explicitly requested, make the cut rhythm feel intentional. Put major finishes, replays, transitions, and celebration peaks on clear musical moments when possible. Prefer retiming football footage slightly over stretching commercial music; document any retime ratio.
- Use a creative commentary/music mix only when music is explicitly requested and the source commentary or crowd has value. Keep music as the main energy only for requested music-led edits; otherwise make commentary/crowd the main audio. In hybrid mixes, duck music under goal calls, emotional commentator lines, player-name moments, or big crowd roars, then bring it back to full volume. When the user asks for commentary/crowd to overshadow the music, make exact goal-impact windows where broadcast audio dominates while the song remains faintly audible underneath unless the user explicitly asks for full silence or a full mute. If a hard numerical target conflicts with audible music, prioritize the latest user preference and document the actual processed stem gap plus a music-audibility check.
- Interpret dB requests carefully. If the user says "make commentary louder by/about 12 dB," treat it as a gain request only when there is no relative reference. If they say "12 dB instead of 17-25 dB," treat it as a target commentary-over-music stem gap. Use per-window gain/ducking when the music's natural loudness changes, and verify both the measured gap and that music remains audible in every checked window.
- Before declaring the final MP4 upload-ready, visually inspect the rendered video or a dense contact sheet and confirm the audio by more than metadata. Spot-check the actual rendered audio around multiple goal/celebration windows; when a hybrid mix is promised, verify that commentary/crowd is audibly present and louder than the music in selected moments. Confirm the edit does not cut away before goals or scorer celebrations, transitions blend smoothly, repeated score-card interstitials are absent, and music/commentary choices feel deliberate. If the review fails, rerender before final delivery.
- Do not rip, record, or download commercial music from Spotify, YouTube, MP3 mirrors, or other streaming/piracy sources. If the user wants music, use a local file they are allowed to use or download from a legitimate stock/licensing service whose page clearly permits the intended use. Record the track title, artist, source URL, license URL/name, local file, and whether commentary was removed.

## Workflow

1. Read `references/viral-patterns.md`.
2. Discover and select a Footballia source from 2020-present unless the user already provided a specific match/video:
   ```bash
   python3 scripts/footballia_discovery.py --out-dir "<scratch-or-project>/research" --since-year 2020
   ```
   Add user themes with repeated `--query`, such as `--query "Lamine Yamal"` or `--query "Manchester City"`. Include specific match pages with repeated `--url`. Use the top-ranked `selected_footballia_match.json` unless the user explicitly chooses another candidate. The ranking already boosts Europe/US audience fit.
3. Create the project folder:
   ```bash
   python3 scripts/project_setup.py --title "<match or video title>"
   ```
   If Footballia discovery produced a selection, create the folder directly from it:
   ```bash
   python3 scripts/project_setup.py --footballia-selection-json "<research-folder>/selected_footballia_match.json"
   ```
4. Verify Footbalia credentials when a Footbalia download is needed:
   ```bash
   python3 scripts/check_credentials.py
   ```
5. Research fresh YouTube references every run. Treat this as pattern research, not footage copying:
   ```bash
   python3 scripts/youtube_research.py --out-dir "<project-folder>/research"
   ```
   Include any user-provided reference URLs with repeated `--seed-url`.
   If discovery was run before project creation, copy `footballia_candidates.*` and `selected_footballia_match.json` into `<project-folder>/research/`.
   - Review `<project-folder>/research/youtube_research.md` before editing. Extract the title formula, thumbnail promise, first-5-seconds hook, pacing, audio approach, and transformation method from videos with million-view signals.
   - Adapt the format, not the footage. Use the selected Footballia/local match as the source and build an original angle such as `scripted-looking moments`, `7-goal chaos explained`, `comeback that changed everything`, or `every goal explained`.
   - For automation runs, write the chosen inspiration formula and the original version plan into the work notes or run report.
6. Get the source match/video:
   - Prefer a user-provided local file or folder.
   - For Footbalia/Footballia, use the Browser plugin with the Keychain credentials. Log in, open the match, play the video, inspect network requests for an authorized media URL, then save the file into `<project-folder>/source/`.
   - If only an HLS/MP4 URL is exposed, download with `yt-dlp` or `ffmpeg` using the authenticated headers/cookies from the browser session.
   - If the site exposes only DRM/encrypted playback or a CAPTCHA, stop and write the blocker in `<project-folder>/run_report.md`.
7. Build the audio plan before rendering. Default to `commentary-only`: use original source commentary/crowd, preserve sync to the edited video, loudness-normalize for YouTube, and emphasize key goal calls/crowd roars with compression or short gain rides. If prior uploads were blocked for copyright, switch to original narration/caption-led analysis and remove broadcast audio.
   - For narration-led cuts, script a short voiceover first. Use OpenAI TTS when `OPENAI_API_KEY` is securely available; suggested default: `gpt-4o-mini-tts`, a natural voice, and instructions like "energetic UK football analyst, conversational, not robotic, with controlled excitement on goal moments." Use OpenAI transcription (`gpt-4o-transcribe`) when needed to generate/verify captions from the final voiceover.
   - For OpenAI-assisted planning, use vision/image-capable models to inspect contact sheets or frames, generate thumbnail concepts, and produce concise title/description/tag variants. Do not use OpenAI video generation for match footage replacement unless the user explicitly approves cost-bearing generation and the output is not pretending to be real match footage.
   - If the project has a leftover song from a previous iteration and the user asks for commentary-only, remove/ignore the song in the final render and remove the song file from the upload folder.
   - If the user explicitly asks for music, put any user-provided or authorized music/audio in `<project-folder>/audio/` and decide the treatment before rendering: `music-only`, `commentary-only`, or `hybrid ducked mix`.
   - For requested hybrid music edits, use volume automation/keyframes: full music during most play, low match-audio bed if it helps realism, music ducked under selected goal/crowd moments, commentary/crowd boosted above the music for the best calls, then music restored on the next beat.
   - For goal-moment emphasis, use two window types: broader commentary windows around the attack/celebration, and exact impact windows where commentary/crowd clearly overshadows the music. Keep broad windows at a high music level unless the user asks otherwise; use short, tight call windows for heavier ducking so the song does not feel low for long stretches. Keep the song audible as an underlay by default; only make it functionally inaudible when the user explicitly asks to mute or remove the music at those moments.
   - Write the audio treatment, commentary status, and any sync/retime details in the run report or work notes. For music-led edits, also record the music source, license note, broad ducking windows, and exact impact windows.
8. Build the Palmier prompt and upload pack:
   ```bash
   python3 scripts/build_palmier_prompt.py --project-dir "<project-folder>"
   ```
9. Use Palmier Pro:
   - Call `get_timeline` once.
   - Call `get_media`; import local source/audio files with `import_media` if missing.
   - Call `inspect_media`/`search_media` to find goals, skills, funny moments, crowd reactions, mistakes, and emotional closeups.
   - Apply the generated `palmier_prompt.md` through Palmier editing tools.
10. Produce final deliverables in the project folder:
   - `exports/` final video if export is available.
   - `thumbnail/thumbnail_prompt.md` and thumbnail image if generated or captured.
   - `youtube_title_options.md`
   - `description.md`
   - `tags.txt`
   - `palmier_prompt.md`
   - `run_report.md`
   Remove stale failed exports, old alternate finals, unused audio files, outdated music/license notes, credential artifacts, partial raw downloads, and scratch working folders from the user-facing project folder when the user asks for a clean upload pack. If the user asks for only YouTube upload necessities, keep only: final MP4, thumbnail image, title options, description, and tags in the user-facing folder. For automations, default to this minimal upload-only folder.
11. If Palmier MCP has no export/render tool, or export is blocked, render a ready-to-upload fallback MP4 from the downloaded/local source:
   ```bash
   python3 scripts/render_ffmpeg_fallback.py --project-dir "<project-folder>"
   ```
   This requires local `ffmpeg`, `ffprobe`, and Python `Pillow`. It writes `exports/*-fallback-edit.mp4`, `thumbnail/thumbnail.jpg`, and appends the export status to `run_report.md`. Use this as the guaranteed local output path; treat Palmier as the preferred editor when its project/export path is available.

## Footbalia Browser Notes

When using Browser, retrieve credentials inside the browser-control code and do not print them. Example shell retrieval commands:

```bash
security find-generic-password -a codex -s codex-footbalia-username -w
security find-generic-password -a codex -s codex-footbalia-password -w
```

In browser automation, type the retrieved values into the login form, play the requested video, watch network traffic for `.mp4`, `.m3u8`, `.mpd`, or media API responses, then download only if the resulting media URL is accessible through the authorized session.

## Output Standard

The project folder should be useful without more chat context. Write a concise `run_report.md` unless the user asks for a minimal upload-only folder; in that case, place internal notes under the workspace `work/` folder instead of the user-facing upload folder.

- input source and project folder
- research videos used
- edit strategy
- Palmier asset IDs/timeline status
- audio treatment, including whether the edit is commentary-only or whether music was explicitly requested
- export status
- final visual/audio review result, especially whether complete goal sequences include buildup, finish, and scorer celebration
- hybrid-audio confirmation, when applicable: which goal windows were spot-checked and whether commentary/crowd was louder than music. For requested overshadow moments, confirm exact impact windows, not only broad goal windows. For numerical hard-overshadow targets, record the measured processed stem-gap range and pass threshold.
- exact remaining manual step, only if blocked
