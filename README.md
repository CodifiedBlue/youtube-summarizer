# youtube-summarizer

A Claude Code skill that turns a YouTube URL into three Markdown artifacts:

1. **`--original.vtt`** — raw English captions from `yt-dlp`.
2. **`--processed.md`** — readable transcript with speaker labels (movie-script style) and paragraphs grouped by speaker change or topic shift, each anchored with a timestamped YouTube link.
3. **`--summary.md`** — structured summary: overview, key takeaways, action items, lists mentioned, and salient quotes.

All three are written into a per-video subfolder named `<slug>--<YYYY.MM.DD>` under your current directory.

## Install

Requirements:

- Python 3.10+
- `yt-dlp` on `$PATH`. Install with `brew install yt-dlp` (or `pip install --user yt-dlp`).
- Claude Code with the skill discovered in this repository.

## Use

In Claude Code, just paste a YouTube URL with intent to summarize, e.g.:

> Summarize this video: https://youtu.be/8rABwKRsec4

The skill auto-creates a folder like `howAIWorksKarpathy-8rABwKRsec4--2024.03.10/` in your current directory and drops the three files inside.

### Flags

- `--force` — redo all three stages even if outputs exist.
- `--output-dir <path>` — where to create the per-video folder. Defaults to current working directory.

## How it works

Two layers:

- **Python helpers** (`scripts/`) do deterministic work — fetching transcripts via `yt-dlp`, parsing VTT (with rolling-overlap dedup), deriving the folder slug.
- **Claude** drives the LLM-judgment stages: speaker inference, topic-shift paragraphing, summary writing. Prompts live in `SKILL.md`.

Smart resume: each on-disk output gates its stage. If `--processed.md` already exists, Stage 2 is skipped. Use `--force` to redo everything.

## Development

```bash
pip install --user pytest
python3 -m pytest scripts/tests/ -v
```

The Python helpers have unit-test coverage. The LLM stages are not unit-tested — verify them by running the skill end-to-end against a short real video and inspecting the outputs.

## Limitations (v1)

- English captions only.
- No retries on transient network/rate-limit errors.
- Speaker inference is best-effort; no manual speaker-name override flag.
- Live streams not specially handled; Shorts are best-effort.
