# YouTube Summarizer Skill — Design

**Date:** 2026-04-25
**Skill location:** `/Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/`

## Overview

A Claude Code skill that takes a YouTube URL and produces three artifacts in a per-video subfolder:

1. `--original.vtt` — raw English captions from `yt-dlp`.
2. `--processed.md` — readable transcript with speaker labels (movie-script style) and paragraphs grouped by speaker change or topic shift, each anchored with a timestamped YouTube link.
3. `--summary.md` — a structured summary including key takeaways, action items, lists mentioned, and salient quotes (with timestamp links back to the moment).

The skill splits responsibilities: Python helpers do deterministic work (download, VTT parsing, slug derivation); Claude does language-judgment work (speaker inference, topic-shift paragraphing, summarization).

## Decisions Locked During Brainstorming

| Topic | Decision |
|---|---|
| Speaker identification | LLM inference from context (no diarization, no manual hints in v1) |
| Transcript source | `yt-dlp` only |
| Filename date | Video upload date |
| Paragraph grouping | Speaker change OR Claude-detected topic shift within a long turn |
| Summary structure | Single `--summary.md` with five fixed sections |
| Output location | Auto-create per-video subfolder under `$PWD` (overridable via `--output-dir`) |
| Implementation split | `SKILL.md` orchestration + Python helpers (no sub-agents) |
| `--original` format | Raw VTT contents, `.vtt` extension |
| Salient-quote detection | Done inside Claude during Stage 3 (no regex pre-filter) |
| Filename slug | lowerCamelCase preserving 2+ uppercase runs, suffixed with `-<videoId>` |
| Re-run behavior | Smart resume: skip stages whose output already exists; `--force` redoes everything |
| Caption language | English only (manual preferred over auto-generated; error if neither) |
| Error handling | Fail fast with clear messages; auto-install `yt-dlp` if missing |

## Architecture

### Pipeline

```
[stage 1: fetch]    yt-dlp → <slug>--<date>--original.vtt (raw VTT on disk)
                    ↓
[stage 2: process]  Claude calls parse_vtt.py → reads cues JSON from stdout
                    → infers speakers → groups by speaker+topic
                    → writes <slug>--<date>--processed.md
                    ↓
[stage 3: summarize] Claude reads processed.md → writes <slug>--<date>--summary.md
```

`parse_vtt.py` is **not** a separately gated stage — it is a stateless transformation Claude invokes on the existing `--original.vtt` whenever it needs cues for Stage 2. Smart-resume gates the three on-disk artifacts (`--original.vtt`, `--processed.md`, `--summary.md`); each stage checks if its output already exists and skips if yes (unless `--force`).

### Output Structure

```
$PWD/
└── howAIWorksKarpathy-8rABwKRsec4--2024.03.10/
    ├── howAIWorksKarpathy-8rABwKRsec4--2024.03.10--original.vtt
    ├── howAIWorksKarpathy-8rABwKRsec4--2024.03.10--processed.md
    └── howAIWorksKarpathy-8rABwKRsec4--2024.03.10--summary.md
```

## Components

### `SKILL.md`

Skill entrypoint Claude reads. Contains:

- Frontmatter: `name`, `description` (when to invoke — e.g., user mentions a YouTube URL with intent to summarize).
- Workflow narrative: parse URL → call `fetch_transcript.py` → call `parse_vtt.py` → run Stage 2 (LLM paragraphing) → run Stage 3 (LLM summary).
- Embedded prompt scaffolds for speaker inference, topic-shift paragraphing, and summary writing — so Stages 2 and 3 are consistent run-to-run.
- Documents flags: `--force`, `--output-dir <path>`.

### `scripts/fetch_transcript.py`

- **Inputs:** YouTube URL or video ID; output directory; `--force` (passed in).
- **Behavior:**
  - Verifies `yt-dlp` is on `$PATH`. If missing, prompts to `brew install yt-dlp` (falls back to `pip install --user yt-dlp` when no Homebrew).
  - Calls `yt-dlp` to fetch metadata (title, channel, upload date, video ID, duration) and English subtitles. Manual subs preferred; auto-generated as fallback. Errors fast if neither exists.
  - Computes folder slug via `slug.py`. Creates the folder.
  - Writes `<slug>--<date>--original.vtt` with raw VTT contents (atomic write: `.tmp` then `mv`).
- **Output (stdout JSON):**
  ```json
  {
    "slug": "howAIWorksKarpathy-8rABwKRsec4",
    "folder": "/abs/path/howAIWorksKarpathy-8rABwKRsec4--2024.03.10",
    "video_id": "8rABwKRsec4",
    "title": "How AI Works | Karpathy",
    "channel": "Lex Fridman Podcast",
    "upload_date": "2024-03-10",
    "url": "https://youtu.be/8rABwKRsec4",
    "vtt_path": ".../...--original.vtt"
  }
  ```

### `scripts/parse_vtt.py`

- **Input:** path to a VTT file.
- **Output (stdout JSON):** list of cues with rolling-overlap dedup applied.
  ```json
  [
    { "start": 0, "end": 3, "text": "welcome back to the podcast today" },
    { "start": 3, "end": 5, "text": "we're talking with andrej karpathy" }
  ]
  ```
- Strips VTT styling tags (`<c>`, `<00:00:00.000>`, etc.). `start`/`end` in integer seconds.

### `scripts/slug.py`

Pure function: `(title: str, video_id: str) -> str`.

**Rule:**

1. Drop diacritics; replace any non-alphanumeric character with whitespace.
2. Split on whitespace into tokens.
3. For each token, preserve any *input* run of 2+ consecutive uppercase letters as-is (acronyms). Otherwise, lowercase the token and capitalize the first letter (Title-case).
4. Join tokens. Lowercase the very first character of the resulting string (so even an acronym-led title like `"NASA Foo"` becomes `nASAFoo` — predictable rule, no ambiguity).
5. Cap at 60 characters.
6. Append `-<video_id>` (the YouTube 11-char ID).

**Examples:**
- `("How AI Works | Karpathy", "8rABwKRsec4")` → `howAIWorksKarpathy-8rABwKRsec4`
- `("NASA and the FBI", "abc12345678")` → `nASAAndTheFBI-abc12345678` (acronyms preserved; first char of joined string lowercased per rule 4)
- `("NASA Foo", "xyz98765432")` → `nASAFoo-xyz98765432`

**Folder name format:** `<slug>--<YYYY.MM.DD>` where the date is the video's upload date with periods as separators (matches `yt-dlp`'s `upload_date` reformatted from `YYYYMMDD`). File names inside the folder repeat this prefix and append `--original.vtt`, `--processed.md`, or `--summary.md`.

### Claude's Responsibilities (driven from `SKILL.md`)

1. **Stage 2 (processed.md):**
   - Read parsed-cues JSON.
   - Infer speakers (typically 1–3) from turn-taking patterns and content cues. Tag each cue with a speaker label (ALL-CAPS, movie-script style — e.g., `LEX FRIDMAN`, `ANDREJ KARPATHY`).
   - Walk speaker-tagged cues; emit a new paragraph on speaker change OR detected topic shift within a long turn.
   - Write `--processed.md` with header block + paragraph blocks.
2. **Stage 3 (summary.md):**
   - Read `--processed.md` (which already has speaker labels and timestamps).
   - Identify salient quotes:
     - **Reaction-anchored:** moments where an interviewer's short turn signals affirmation, surprise, or excitement (phrasing varies — use judgment, not a fixed regex).
     - **Standalone insights:** quotes Claude judges memorable even with no reaction.
   - Extract action items, lists mentioned by speakers, and key takeaways.
   - Write `--summary.md` with five fixed sections.

## File Formats

### `--original.vtt`

Raw `yt-dlp` VTT, byte-for-byte:

```
WEBVTT
Kind: captions
Language: en

00:00:00.480 --> 00:00:02.560
welcome back to the podcast today

00:00:02.560 --> 00:00:04.880
we're talking with andrej karpathy
```

Auto-captions have rolling overlap (sliding-window duplication) — this file is unmodified; dedup happens in `parse_vtt.py` for downstream consumers.

### `--processed.md`

```markdown
# How AI Works | Karpathy

- **Channel:** Lex Fridman Podcast
- **Uploaded:** 2024-03-10
- **URL:** https://youtu.be/8rABwKRsec4

---

[00:00](https://youtu.be/8rABwKRsec4?t=0) **LEX FRIDMAN**

Welcome back to the podcast. Today we're talking with Andrej Karpathy about how AI actually works under the hood — from training to inference to where the field is heading next.

[00:24](https://youtu.be/8rABwKRsec4?t=24) **ANDREJ KARPATHY**

Thanks for having me. So when I think about how a model actually learns...

[02:15](https://youtu.be/8rABwKRsec4?t=135) **ANDREJ KARPATHY**

Now on the inference side, the picture changes...
```

**Rules:**

- H1 title; bullet metadata (channel, upload date, URL); `---` separator.
- Each paragraph: `[MM:SS](https://youtu.be/<id>?t=<seconds>) **SPEAKER NAME**` on its own line, blank line, prose.
- Speaker names ALL-CAPS.
- New paragraph on speaker change OR Claude-detected topic shift.
- Prose is naturalized (capitalization fixed, sentences joined into readable paragraphs) but no content paraphrased — words come from the captions.
- Timestamp display is `MM:SS` for videos under 1 hour; `HH:MM:SS` for longer.

### `--summary.md`

```markdown
# How AI Works | Karpathy — Summary

- **Channel:** Lex Fridman Podcast
- **Uploaded:** 2024-03-10
- **URL:** https://youtu.be/8rABwKRsec4

## Summary

[1–2 paragraphs of plain prose, no timestamps.]

## Key Takeaways

- [bullet]
- [bullet]

## Action Items

- [KARPATHY — [12:34](https://youtu.be/8rABwKRsec4?t=754)] Concrete thing the speaker recommended.
- [KARPATHY — [21:08](https://youtu.be/8rABwKRsec4?t=1268)] ...

## Lists Mentioned

### The 5 stages of model training — KARPATHY ([04:22](https://youtu.be/8rABwKRsec4?t=262))

1. ...
2. ...

### Things every ML engineer should read — KARPATHY ([38:10](https://youtu.be/8rABwKRsec4?t=2290))

- ...

## Salient Quotes

> "The thing nobody tells you about transformers is..."
> — KARPATHY, [11:42](https://youtu.be/8rABwKRsec4?t=702). Lex reacted with "oh that's a great way to put it."

> "If you only do one thing, do this..."
> — KARPATHY, [27:05](https://youtu.be/8rABwKRsec4?t=1625). Standalone insight.
```

**Rules:**

- Same header block as processed file, with `— Summary` appended to title.
- Five sections in fixed order: Summary, Key Takeaways, Action Items, Lists Mentioned, Salient Quotes.
- Empty sections render as the heading + `_None._` (consistent structure across all videos).
- Every action item, list, and quote anchored with a timestamp link back to YouTube.
- Action items prefixed with the speaker who proposed them.

## Error Handling

**Pre-flight (fail fast):**
- `yt-dlp` missing → print `yt-dlp not found. Install with: brew install yt-dlp` and offer to run it. Falls back to `pip install --user yt-dlp` if no Homebrew.
- `python3` missing or wrong version → fail fast (no auto-install).

**URL/video errors (each prints one-line diagnostic, exits non-zero, no retry):**
- Invalid URL or unrecognized YouTube URL shape.
- Video private/removed/age-restricted (surface `yt-dlp`'s error verbatim with `yt-dlp: ` prefix).
- No English captions (manual or auto): `No English captions available for <video_id>. Skill requires English subs.`
- Network failure / DNS / timeout: surface error, exit. User re-runs.
- Rate-limited by YouTube: surface error with hint to retry later.

**Smart-resume edge cases:**
- Folder exists, `--original.vtt` exists but is empty/corrupt → treat as missing, re-fetch.
- Folder exists, `--processed.md` exists but `--original.vtt` doesn't → warn and re-fetch original (Stages 2/3 still skip if their outputs exist).
- Partial run interrupted mid-write → atomic writes (`.tmp` + `mv`) prevent half-written files.
- `--force` deletes all three output files before starting; the metadata folder itself is preserved.

**Caption-quality edge cases:**
- VTT has zero non-empty cues → `Captions returned empty. Video may have generated subs disabled.`
- Auto-captions are noisy (mangled words) → still proceed; Claude does its best.
- Single-speaker video → speaker inference falls back to one speaker. Reaction-anchored quotes may be empty (`_None._`); standalone-insight quotes still populated.

**LLM-stage edge cases:**
- Very long transcripts (3+ hours) → processed in one pass. Chunking deferred to a future enhancement if context becomes a problem in practice.
- Claude outputs malformed Markdown → not validated programmatically. We trust the model and don't want a fragile validator.
- Speaker inference unsure → Claude picks its best guess; user can `--force` to redo.

**Explicit non-goals for v1:**
- No caching of YouTube responses outside the output folder.
- No parallel/sub-agent processing.
- No language other than English.
- No retries with backoff.
- No manual speaker-name override flag.
- No special handling for live streams; Shorts handled the same as regular videos (best-effort).

## Testing Strategy

### Unit tests (`pytest`, in `scripts/tests/`)

- **`test_slug.py`** — pure function, fully deterministic:
  - basic title → camelCase
  - ALL-CAPS preservation: `"NASA and the FBI"` → `nASAAndTheFBI`
  - punctuation/diacritics stripping
  - 60-char cap then `-<videoId>` suffix
  - first-character lowercase rule even when first word is an acronym (`"NASA Foo"` → `nASAFoo`)
  - empty / single-word / only-punctuation titles
- **`test_parse_vtt.py`** — fixture-driven (`scripts/tests/fixtures/`):
  - `simple.vtt` — 3 clean cues → exact expected JSON
  - `rolling_overlap.vtt` — sliding-window auto-caption dupes → dedup non-overlapping cues
  - `styled.vtt` — VTT with `<c>` tags / position headers → tags stripped
  - `empty.vtt` — header only → returns `[]`
- **`test_fetch_transcript.py`** — `yt-dlp` mocked via `subprocess.run` patch:
  - happy path: writes `--original.vtt`, emits expected JSON
  - missing `yt-dlp`: prompts to install, exits cleanly
  - private video: surfaces `yt-dlp: <message>`
  - no English captions: documented diagnostic

**No integration tests against real YouTube** — flaky, slow, brittle.

### Manual verification of LLM stages

LLM output can't be unit-tested deterministically. Approach:

- **Smoke fixture:** one short real video URL (~5 min, 2-speaker interview) run end-to-end during development. Expected outputs committed as golden files for human review (not asserted) to detect prompt regressions when editing `SKILL.md`.
- **Optional structural guardrails (not required for v1):** simple regex assertions that processed.md has the metadata header and at least one timestamp link, and that summary.md contains all five section headings.

### Acceptable v1 testing gaps

- Speaker-inference accuracy on adversarial transcripts.
- Quote selection quality.
- Summary completeness.
- Rate-limit / network-failure paths (surfaced from `yt-dlp`, not retested).

## File Layout

```
youtube-summarizer/
├── SKILL.md
├── README.md
├── scripts/
│   ├── fetch_transcript.py
│   ├── parse_vtt.py
│   ├── slug.py
│   └── tests/
│       ├── __init__.py
│       ├── test_slug.py
│       ├── test_parse_vtt.py
│       ├── test_fetch_transcript.py
│       └── fixtures/
│           ├── simple.vtt
│           ├── rolling_overlap.vtt
│           ├── styled.vtt
│           └── empty.vtt
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-04-25-youtube-summarizer-design.md
├── .claude/
│   └── settings.json
└── .gitignore
```

- **No `requirements.txt`** — `yt-dlp` is the only runtime dep, installed system-wide. Document `pip install pytest` in README for dev setup.
- **No `pyproject.toml` / packaging** — these are scripts, not a library. Run directly: `python3 scripts/fetch_transcript.py <url>`.
