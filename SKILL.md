---
name: youtube-summarizer
description: Use when the user shares a YouTube URL and wants a transcript, processed/readable transcript with speaker labels, or a structured summary. Triggers include "summarize this video", "transcribe this YouTube link", "give me notes on https://youtu.be/...", or any request that combines a YouTube URL with intent to extract content.
---

# YouTube Summarizer

This skill turns a YouTube URL into three Markdown artifacts in a per-video subfolder:

1. `<basename>--original.vtt` — raw English captions from `yt-dlp`.
2. `<basename>--processed.md` — readable transcript with movie-script speaker labels and topic-grouped paragraphs, each anchored with a YouTube timestamp link.
3. `<basename>--summary.md` — structured summary: overview, key takeaways, action items, lists mentioned, salient quotes.

The skill splits work between Python helpers (deterministic) and Claude (language-judgment). You — Claude — handle stages 2 and 3.

## Inputs

- A YouTube URL (full `https://www.youtube.com/watch?v=...` or short `https://youtu.be/...`).
- Optional flags from the user:
  - `--force` — redo all three stages even if outputs exist.
  - `--output-dir <path>` — where to create the per-video folder. Default: current working directory.

If the user's message contains a YouTube URL but no explicit flags, default to no flags.

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

### Stage 3: Build `--summary.md`

Compute the target path: `<folder>/<basename>--summary.md`.

If that file already exists and `--force` was not passed, skip this stage.

Otherwise:

1. Read `<folder>/<basename>--processed.md` (which already has speaker labels and timestamps).
2. Use the prompt below ("Stage 3 prompt") to produce the summary content.
3. Write the result to `<folder>/<basename>--summary.md`.

#### Stage 3 prompt

You are producing a structured summary file from a speaker-labeled transcript. Input: the contents of `--processed.md` (which has the title, metadata header, and timestamped speaker-labeled paragraphs).

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

7. **Empty sections.** Always include all five section headings. Empty section body is `_None._`.

Write only the Markdown document. No commentary.

## Smart Resume Recap

- Stage 1 is gated by the existence of `<basename>--original.vtt` (the script handles this internally).
- Stage 2 is gated by `<basename>--processed.md`.
- Stage 3 is gated by `<basename>--summary.md`.
- `--force` redoes all three.

After all three stages complete, report the absolute paths of the three artifacts to the user as a tight bulleted list.

## Errors

- If Stage 1 fails (no English captions, private video, network, etc.), surface the stderr message and stop. Do not attempt Stages 2 or 3.
- If `parse_vtt.py` produces an empty cues list, tell the user the captions were empty and stop.
