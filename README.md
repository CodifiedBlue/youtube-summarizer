# youtube-summarizer

A Claude Code skill that turns a YouTube URL into a set of artifacts:

1. **`--original.vtt`** — raw English captions from `yt-dlp`.
2. **`--processed.md`** — readable transcript with speaker labels (movie-script style) and paragraphs grouped by speaker change or topic shift, each anchored with a timestamped YouTube link.
3. **`frames/`** — the most salient on-screen visuals (graphs, charts, tables, diagrams, data slides) pulled from the video. A deterministic `ffmpeg` pass keeps only frames that are *held static* on screen (real visuals stay put; talking heads and motion don't), then Claude vision picks the salient ones. Includes a `manifest.json` mapping each kept frame to a timestamp.
4. **`--summary.md`** — structured summary: overview, key takeaways, action items, lists mentioned, salient quotes, and a **Key Visuals** section that embeds the salient frames inline with timestamped links.

Everything is written into a per-video subfolder named `<slug>--<YYYY.MM.DD>` under your current directory.

## Install

Requirements:

- Python 3.9+
- `yt-dlp` on `$PATH`. Install with `brew install yt-dlp` (or `pip install --user yt-dlp`).
- `ffmpeg` (and `ffprobe`) on `$PATH` for visual analysis. Install with `brew install ffmpeg`. Without it, transcript + summary still work; only the Key Visuals section is skipped.
- Claude Code with the skill discovered in this repository.

## Use

In Claude Code, just paste a YouTube URL with intent to summarize, e.g.:

> Summarize this video: https://youtu.be/8rABwKRsec4

The skill auto-creates a folder like `howAIWorksKarpathy-8rABwKRsec4--2024.03.10/` in your current directory and drops the three files inside.

### Flags

- `--force` — redo all stages even if outputs exist.
- `--output-dir <path>` — where to create the per-video folder. Defaults to current working directory.
- `--no-visuals` — skip video download and frame analysis; the summary omits Key Visuals.
- `--min-hold <seconds>` — how long a frame must stay static to count as a held visual (default `3.0`; higher filters more talking-head pauses, lower catches briefly-shown slides).
- `--freeze-noise <dB|ratio>` — how much pixel motion still counts as "static" (default `-60dB`; loosen to e.g. `0.006` when slides have a moving webcam PIP or watermark).
- `--max-frames <N>` — cap on candidate frames handed to the vision layer (default `60`).

## How it works

Two layers:

- **Python helpers** (`scripts/`) do deterministic work — fetching transcripts via `yt-dlp`, parsing VTT (with rolling-overlap dedup), deriving the folder slug, and downloading a capped-resolution video to pull candidate frames via `ffmpeg` (`extract_frames.py`). Frame candidates are chosen with `ffmpeg`'s `freezedetect`: only segments that stay static for at least `--min-hold` seconds yield a frame, so motion-heavy footage (talking heads, transitions, animation) is filtered out before the LLM ever sees it. This keeps the vision step cheap — a talking-head video produces ~zero candidates.
- **Claude** drives the judgment stages: speaker inference, topic-shift paragraphing, summary writing, and **vision selection** — reviewing the small held-frame set and keeping only the genuinely salient graphs/charts/tables/diagrams. Prompts live in `SKILL.md`.

Smart resume: each on-disk output gates its stage. If `--processed.md` already exists, Stage 2 is skipped; if `frames/manifest.json` exists, Stage 3 is skipped. Use `--force` to redo everything.

## Development

```bash
pip install --user pytest
python3 -m pytest scripts/tests/ -v
```

The Python helpers have unit-test coverage. The LLM stages are not unit-tested — verify them by running the skill end-to-end against a short real video and inspecting the outputs.

## Limitations

- English captions only.
- No retries on transient network/rate-limit errors.
- Speaker inference is best-effort; no manual speaker-name override flag.
- Live streams not specially handled; Shorts are best-effort.
- Visual analysis downloads a capped-resolution copy of the video (deleted after frames are extracted unless `--keep-video` is passed to the helper). It requires `ffmpeg`. Candidate selection keys on stillness, so a visually sparse "talking head" video yields few or no Key Visuals (by design). Slides with a persistently moving element (e.g. a webcam PIP over the whole frame) may be missed unless `--freeze-noise` is loosened.
