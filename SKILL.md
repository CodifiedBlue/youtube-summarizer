---
name: youtube-summarizer
description: Use when the user shares a YouTube URL and wants a transcript, processed/readable transcript with speaker labels, or a structured summary. Triggers include "summarize this video", "transcribe this YouTube link", "give me notes on https://youtu.be/...", or any request that combines a YouTube URL with intent to extract content.
---

# YouTube Summarizer

This skill turns a YouTube URL into these artifacts in a per-video subfolder:

1. `<basename>--original.vtt` — raw English captions from `yt-dlp`.
2. `<basename>--processed.md` — readable transcript with movie-script speaker labels and topic-grouped paragraphs, each anchored with a YouTube timestamp link.
3. `frames/` — candidate on-screen-visual frames (JPEGs) extracted from the video, plus a `manifest.json` mapping each frame to a timestamp. Candidates are limited to frames that are **held static** on screen (see Stage 3), so the set is small and high-precision. Non-salient candidates are pruned during Stage 4; the kept frames are embedded in the summary.
4. `<basename>--summary.md` — structured summary: overview, key takeaways, action items, lists mentioned, salient quotes, and **key visuals** (the most salient graphs, charts, tables, and diagrams shown on screen).

The skill splits work between Python helpers (deterministic) and Claude (language- and vision-judgment). You — Claude — handle stages 2 and 4 (Stage 3 is a Python helper; you do the vision selection during Stage 4).

## Inputs

- A YouTube URL (full `https://www.youtube.com/watch?v=...` or short `https://youtu.be/...`).
- Optional flags from the user:
  - `--force` — redo all stages even if outputs exist.
  - `--output-dir <path>` — where to create the per-video folder. Default: current working directory.
  - `--no-visuals` — skip video download and frame analysis (Stage 3); the summary omits the Key Visuals section. Use this for audio-only content, or when the user only wants text.
  - `--min-hold <seconds>` — passed through to Stage 3; how long a frame must stay static to count as a held visual (default `3.0`). Raise it to filter more talking-head pauses; lower it to catch briefly-shown slides.
  - `--freeze-noise <dB|ratio>` — passed through to Stage 3; how much pixel motion still counts as "static" (default `-60dB`). Loosen it (e.g. `0.006`) when slides have a small moving element like a webcam PIP or watermark.
  - `--max-frames <N>` — cap on candidate frames handed to the vision layer in Stage 3 (default `60`).

If the user's message contains a YouTube URL but no explicit flags, default to no flags. Default behavior includes visual analysis (Stage 3). Only skip it when `--no-visuals` is passed or when the tooling is unavailable (see Errors).

## Workflow

Execute these stages sequentially. Each on-disk output gates its stage: if it already exists and `--force` was not passed, skip that stage.

### Stage 1: Fetch transcript

Run (from any cwd):

```bash
python3 ~/.claude/skills/youtube-summarizer/scripts/fetch_transcript.py <URL> [--output-dir <path>] [--force]
```

The default `--output-dir` is the user's current working directory, so the per-video folder lands where the user is, not in the skill install location.

The script handles smart-resume internally for `--original.vtt`.

It emits a single JSON line on stdout:

```json
{
  "slug": "...",
  "folder": "/abs/path",
  "video_id": "...",
  "title": "...",
  "channel": "...",
  "upload_date": "YYYY-MM-DD",
  "url": "...",
  "vtt_path": "/abs/path/<basename>--original.vtt"
}
```

Capture this JSON. Use `folder`, `vtt_path`, `video_id`, `title`, `channel`, `upload_date`, and `url` for downstream stages. The folder's basename (`<slug>--<YYYY.MM.DD>`) is the file prefix for `--processed.md` and `--summary.md`.

If the script exits non-zero, surface its stderr to the user verbatim and stop.

### Stage 2: Build `--processed.md`

Compute the target path: `<folder>/<basename>--processed.md`.

If that file already exists and `--force` was not passed, skip this stage.

Otherwise:

1. Run `python3 ~/.claude/skills/youtube-summarizer/scripts/parse_vtt.py <vtt_path>`. Capture the JSON list of cues from stdout. Each cue has `start` (seconds), `end` (seconds), `text`.
2. Use the prompt below ("Stage 2 prompt") to produce the processed Markdown content. Apply your own judgment for speakers and topic shifts; do not paraphrase the words.
3. Write the result to `<folder>/<basename>--processed.md`.

#### Stage 2 prompt

You are converting a list of caption cues into a readable transcript. Inputs you have:

- `cues`: a list of `{start, end, text}`. `start`/`end` are integer seconds. Cues are in order with no rolling overlap (already deduped).
- `video_id`, `title`, `channel`, `upload_date`, `url` from Stage 1.

Produce a Markdown document with this exact structure:

```markdown
# <title>

- **Channel:** <channel>
- **Uploaded:** <upload_date>
- **URL:** <url>

---

[<MM:SS>](https://youtu.be/<video_id>?t=<start_seconds>) **<SPEAKER NAME>**

<paragraph prose>

[<MM:SS>](https://youtu.be/<video_id>?t=<start_seconds>) **<SPEAKER NAME>**

<paragraph prose>

...
```

Rules:

1. **Speaker inference.** Read the cues end-to-end. Identify how many distinct speakers there are (typically 1–3). Look at the title, channel, and content cues for proper names. Use those as ALL-CAPS speaker labels (e.g., `LEX FRIDMAN`, `ANDREJ KARPATHY`). If a name isn't recoverable, use generic labels: `INTERVIEWER`, `GUEST`, `SPEAKER 1`, `SPEAKER 2`. Apply labels consistently — once you've decided who each speaker is, do not re-label them.

2. **Paragraph boundaries.** Start a new paragraph at:
   - A speaker change (always).
   - A clear topic shift within a long monologue from one speaker. Use judgment; don't break trivial pauses. Aim for paragraphs that are roughly 60–180 seconds when applicable, but err on the side of fewer breaks for fast back-and-forth.

3. **Paragraph header line.** Each paragraph begins with `[<TIMESTAMP>](https://youtu.be/<video_id>?t=<start_seconds>) **<SPEAKER NAME>**` as its own line, then a blank line, then the prose.
   - `<TIMESTAMP>` is `MM:SS` (zero-padded minutes) for videos under 1 hour. For 1+ hour videos, use `HH:MM:SS` (zero-padded hours and minutes). Examples: `04:22`, `38:10`, `01:02:15`.
   - `<start_seconds>` is the raw integer seconds of the first cue in the paragraph.

4. **Prose.** Concatenate the cue texts in the paragraph. Naturalize: capitalize sentences, add punctuation where missing, fix obvious caption errors that block readability. Do **not** paraphrase, summarize, or insert content. The words are the speaker's; you are only making them readable.

5. **No timestamps inside paragraphs.** Only the leading line carries a timestamp link.

Write only the Markdown document. No commentary, no surrounding explanations.

### Stage 3: Extract candidate frames

Skip this stage entirely if `--no-visuals` was passed.

This stage downloads a resolution-capped copy of the video and extracts candidate frames plus a manifest. It is a deterministic Python helper — it does **not** decide which frames are salient. That judgment happens in Stage 4.

**How candidates are chosen (and why it's cheap):** salient visuals — charts, tables, slides, diagrams — are *held still* on screen, whereas talking heads, transitions, animations, and b-roll are in constant motion. The helper uses ffmpeg's `freezedetect` filter to find segments where the picture stops changing for at least `--min-hold` seconds, then keeps ONE representative frame per held segment. This is purely mechanical (no LLM) and drastically shrinks the set the vision layer must review: a pure talking-head video yields ~zero candidates, while a slide deck yields roughly one frame per slide.

The output gate is `<folder>/frames/manifest.json`. If it already exists and `--force` was not passed, skip this stage (the manifest is re-emitted so downstream still has it).

Run:

```bash
python3 ~/.claude/skills/youtube-summarizer/scripts/extract_frames.py <URL> --folder <folder> [--force] [--min-hold <S>] [--freeze-noise <N>] [--max-candidates <N>]
```

Pass through the user's `--min-hold` and `--freeze-noise`, and map `--max-frames` to `--max-candidates`, if they were provided. It is normal and expected for `count` to be `0` on videos with no static visuals — that is the desired outcome, not an error.

The script emits a single JSON line on stdout:

```json
{
  "frames_dir": "/abs/path/frames",
  "manifest_path": "/abs/path/frames/manifest.json",
  "count": 42,
  "frames": [
    {"file": "frame-00012s.jpg", "path": "/abs/.../frame-00012s.jpg", "seconds": 12, "timestamp": "00:12"}
  ]
}
```

Capture this JSON — Stage 4 needs the `frames` list (each entry's `path`, `seconds`, and `timestamp`).

Error handling for this stage is non-fatal: if the script exits non-zero (ffmpeg missing, video unavailable, download blocked, etc.), do **not** stop the pipeline. Note the failure, continue to Stage 4, and produce the summary with the Key Visuals section set to `_None._`. Visuals are an enhancement, not a hard requirement.

### Stage 4: Build `--summary.md`

Compute the target path: `<folder>/<basename>--summary.md`.

If that file already exists and `--force` was not passed, skip this stage.

Otherwise:

1. Read `<folder>/<basename>--processed.md` (which already has speaker labels and timestamps).
2. If Stage 3 ran and produced candidate frames, perform **visual selection** (see below) before writing the summary. Otherwise treat Key Visuals as empty.
3. Use the prompt below ("Stage 4 prompt") to produce the summary content.
4. Write the result to `<folder>/<basename>--summary.md`.

#### Visual selection (vision step)

Do this only when Stage 3 produced a non-empty `frames` list. If `count` is `0`, skip straight to writing the summary with Key Visuals as `_None._` — do not read any images.

1. Read the candidate frame images. Use the Read tool on each frame's `path` (they are JPEGs). Batch the reads. Review all of them: Stage 3 already filtered to held/static frames and capped the set, so the count is small (often a handful) and cheap to inspect.
2. Select the **most salient** frames — ones that show information a reader would want captured: graphs, charts, plots, tables, diagrams, architecture drawings, code snippets, comparison matrices, key slides with data, maps, or any dense on-screen visual. **Reject** talking-head shots that happened to hold still, plain title cards, transitions, logos, blurry/mid-animation frames, near-duplicates of an already-selected frame, and purely decorative footage.
3. Aim for roughly 3–10 kept visuals for a typical video (fewer for short or visually sparse content; it is fine to keep zero if nothing qualifies). When two candidates show the same chart, keep the single clearest one.
4. **Prune the folder.** Delete the candidate frames you are NOT keeping from `<folder>/frames/` so only the salient images remain on disk. Keep `manifest.json`. (Deleting is optional if you prefer to leave the full candidate set, but the default is to prune so the folder is clean.)
5. For each kept frame, note its `seconds`/`timestamp` from the manifest and write a one-line caption describing what the visual shows. Embed it in the summary's Key Visuals section using a relative image path (`frames/<file>`) so the Markdown renders the image inline.

#### Stage 4 prompt

You are producing a structured summary file from a speaker-labeled transcript, plus (optionally) a set of salient frames you selected in the vision step. Inputs: the contents of `--processed.md` (title, metadata header, timestamped speaker-labeled paragraphs), and the list of kept visuals (each with a `file`, `seconds`, `timestamp`, and your caption).

Produce a Markdown document with this exact structure and section order. Sections that have no content render as the heading followed by `_None._`.

```markdown
# <title> — Summary

- **Channel:** <channel>
- **Uploaded:** <upload_date>
- **URL:** <url>

## Summary

<1–2 paragraphs of plain prose, no timestamps. Capture the gist of the conversation: who, what, why it matters.>

## Key Takeaways

- <bullet — the headline insights a reader should walk away with>
- <bullet>
- ...

## Action Items

- [<SPEAKER> — [<MM:SS>](<youtube link>)] <Concrete thing the speaker recommended doing>
- ...

## Lists Mentioned

### <List title> — <SPEAKER> ([<MM:SS>](<youtube link>))

1. <item>
2. <item>

### <Another list> — <SPEAKER> ([<MM:SS>](<youtube link>))

- <item>
- <item>

## Salient Quotes

> "<exact quote from transcript>"
> — <SPEAKER>, [<MM:SS>](<youtube link>). <Optional one-line context, e.g., the interviewer's reaction phrase.>

> "<another quote>"
> — <SPEAKER>, [<MM:SS>](<youtube link>). Standalone insight.

## Key Visuals

### <Short title of the visual> — [<MM:SS>](https://youtu.be/<video_id>?t=<seconds>)

![<Short title of the visual>](frames/<file>)

<One-line caption: what the graph/chart/table/diagram shows and why it matters.>

### <Next visual> — [<MM:SS>](https://youtu.be/<video_id>?t=<seconds>)

![<Next visual>](frames/<file>)

<One-line caption.>
```

Rules:

1. **Header.** Reuse the title, channel, upload date, and URL from the processed file. Append `— Summary` to the H1 title.

2. **Summary section.** 1–2 paragraphs. Plain prose. No timestamps. Describe the conversation's substance, not its structure ("they talked about X, then Y" is bad; "X is shaped by Y for these reasons" is good).

3. **Key Takeaways.** 3–7 bullets of headline insights. Not a chronological recap — the things worth remembering. Each bullet is one sentence.

4. **Action Items.** Things a speaker recommended doing — practical, concrete advice, not philosophical statements. Prefix with the speaker who said it. Include a timestamp link to where they said it. If no action items, write `_None._`.

5. **Lists Mentioned.** Whenever a speaker enumerates something ("there are five stages", "the things every X should do are..."), capture it as a sub-section with a timestamped link. Use ordered list (`1.`) for ranked or sequential items, bullets (`-`) for unordered. If no lists, write `_None._`.

6. **Salient Quotes.** Two kinds, both go here:
   - **Reaction-anchored:** The interviewer's short turn signals affirmation, surprise, or excitement — this can be "Interesting!", "Good idea!", "Wow", "Right", "I love that", a laugh, "say more about that", and many other phrasings. Auto-captions often drop punctuation, so read tone and intent, not literal exclamation marks. The salient quote is what the *previous* speaker just said. Add a short context line: `<Reactor> reacted with "<their phrasing>".`
   - **Standalone insights:** Something a speaker said that you'd want to remember even with no reaction trigger. Annotate with `Standalone insight.` or a short context line.
   - Quote text must be from the transcript (capitalization may be normalized). Anchor each quote with a timestamp link. If no salient quotes, write `_None._`.

7. **Key Visuals.** One sub-section per frame you kept in the vision step, in chronological order by timestamp. Each has an H3 title, the embedded image (`![alt](frames/<file>)` — relative path so it renders inline next to the summary), a timestamp link into the video, and a one-line caption saying what the visual shows. Only include genuinely informative visuals (graphs, charts, tables, diagrams, data slides, code). If Stage 3 was skipped, failed, or you kept no frames, write `_None._`.

8. **Empty sections.** Always include all six section headings. Empty section body is `_None._`.

Write only the Markdown document. No commentary.

## Smart Resume Recap

- Stage 1 is gated by the existence of `<basename>--original.vtt` (the script handles this internally).
- Stage 2 is gated by `<basename>--processed.md`.
- Stage 3 is gated by `frames/manifest.json` (skipped entirely with `--no-visuals`).
- Stage 4 is gated by `<basename>--summary.md`.
- `--force` redoes all stages.

After all stages complete, report the absolute paths of the artifacts to the user as a tight bulleted list (the two Markdown files, plus the `frames/` folder and how many visuals were kept, when applicable).

## Errors

- If Stage 1 fails (no English captions, private video, network, etc.), surface the stderr message and stop. Do not attempt later stages.
- If `parse_vtt.py` produces an empty cues list, tell the user the captions were empty and stop.
- Stage 3 (frame extraction) is best-effort. If `extract_frames.py` exits non-zero — including when ffmpeg is not installed (`brew install ffmpeg`), the video can't be downloaded, or extraction yields nothing — do not fail the run. Continue to Stage 4 and set Key Visuals to `_None._`. Optionally mention to the user that visuals were skipped and why.
