# Cleanup duplicate `.vtt` files in `fetch_transcript.py`

## Problem

After Stage 1 of the youtube-summarizer skill runs, the per-video folder
sometimes contains two byte-identical (or near-identical) VTT files:

- `<basename>--original.vtt` — the canonical file the script intends to keep.
- `<basename>.en.vtt` — a leftover from yt-dlp's download.

Observed in the committed sample folder
`theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/`, which has both files at
exactly 170561 bytes (`diff` returns empty).

## Root cause

`scripts/fetch_transcript.py` invokes yt-dlp with:

```
--write-subs --write-auto-subs --sub-langs en.*,en
```

For videos that have **both** manual and auto-generated English captions,
yt-dlp produces multiple files in one pass — e.g. `<basename>.en.vtt`
(manual) and `<basename>.en-orig.vtt` (auto-generated original). The
`--sub-langs en.*,en` glob matches both.

The script then runs:

```python
matches = sorted(parent.glob(f"{base}.en*.vtt"))
return matches[0] if matches else None
```

It picks `matches[0]` (alphabetically first; `-` < `.` in ASCII, so
`.en-orig.vtt` wins over `.en.vtt`), `shutil.move`s it to
`<basename>--original.vtt`, and **leaves any other matches on disk**. The
folder ends with two VTTs.

## Goal

After `fetch_transcript.py` runs, the per-video folder must contain exactly
one VTT: `<basename>--original.vtt`. No `.en*.vtt` siblings.

## Design

### Change site

`scripts/fetch_transcript.py`, inside `_download_subs`.

### Behavior change

Today `_download_subs` returns `matches[0]` and silently discards the rest
of `matches`. New behavior:

- Still pick `matches[0]` as the file to keep.
- Before returning, `unlink()` every other entry in `matches`.
- Return the kept `Path`.

The caller's existing `shutil.move(produced, tmp)` → `os.replace(tmp,
target_vtt)` rename then leaves the folder with exactly one VTT.

### Why inside `_download_subs` (not in `run()`)

The cleanup is logically part of "extract the one VTT yt-dlp produced."
Keeping it co-located with the glob means the function's contract becomes
"yt-dlp may produce N matching files; we return one Path and the rest are
gone" — which is what every caller wants. Doing it in `run()` would leak
that detail to the orchestration layer.

### "First" tie-break

Unchanged: `sorted(matches)[0]`. For the sample video that's
`.en-orig.vtt`, which is already what the committed sample contains. The
**keep** choice doesn't change — only the **cleanup** is new.

### Edge cases

| Match count | Behavior                                                    |
| ----------- | ----------------------------------------------------------- |
| 0           | Unchanged — return `None`, caller surfaces "no captions".   |
| 1           | Unchanged — cleanup loop body never runs.                   |
| 2+          | Kept = `matches[0]`; remaining entries `unlink()`'d.        |

### Sample output cleanup

The orphan
`theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt`
(currently untracked) is removed. The committed `--original.vtt` stays
as-is — it is byte-identical to the leftover.

## Testing

Add one new test class in `scripts/tests/test_fetch_transcript.py`:

- Simulate yt-dlp producing **two** `.en*.vtt` files in one pass (e.g.
  `<basename>.en.vtt` and `<basename>.en-orig.vtt`, with distinguishable
  contents so we can verify which one was kept).
- Run `fetch_transcript.run(...)`.
- Assert: folder contains exactly one VTT (`<basename>--original.vtt`).
- Assert: its contents match `matches[0]` (the alphabetically-first input
  file, i.e. the `.en-orig.vtt` content).
- Assert: no `.en*.vtt` files remain.

Existing tests all simulate the single-file case and stay green
unchanged.

## Files changed

- `scripts/fetch_transcript.py` — add cleanup loop in `_download_subs`.
- `scripts/tests/test_fetch_transcript.py` — add multi-file test.
- `theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt`
  — delete (untracked orphan from prior smoke test).

## Out of scope

- Tightening `--sub-langs` to download only one variant (rejected: would
  miss videos whose only English track is tagged `en-US`/`en-orig`).
- Splitting yt-dlp into two passes ("manual first, auto fallback")
  (rejected: more complex, two network calls on auto-only videos).
- `SKILL.md` / `README.md` updates — neither documents the leftover file;
  both already describe a single `--original.vtt` artifact.
