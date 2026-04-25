"""Parse a WebVTT file into a list of deduped cues.

A cue is a dict: {"start": int_seconds, "end": int_seconds, "text": str}.

Handles:
- WEBVTT header and Kind/Language metadata lines (skipped).
- Cue settings on the timing line (align:start position:0% etc — ignored).
- Inline styling tags: <c>, <i>, <b>, etc. — stripped.
- Inline timing tags <HH:MM:SS.mmm> — stripped.
- Multiline cue text — joined with single space.
- Rolling-overlap dedup: when consecutive cues share trailing/leading words
  (auto-caption sliding window), keep only the new words from the later cue.

Used as a library (`parse_vtt_file(path)`) and as a CLI:
  python3 scripts/parse_vtt.py path/to/file.vtt   # prints JSON to stdout
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import List, Dict


_TAG_RE = re.compile(r"<[^>]+>")
_TIMING_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2})\.\d{3}\s+-->\s+(\d{2}):(\d{2}):(\d{2})\.\d{3}"
)


def _ts_to_seconds(h: str, m: str, s: str) -> int:
    return int(h) * 3600 + int(m) * 60 + int(s)


def _strip_tags(text: str) -> str:
    return _TAG_RE.sub("", text)


def _parse_raw_cues(content: str) -> List[Dict]:
    """First pass: extract cues from VTT text without dedup."""
    blocks = re.split(r"\n\s*\n", content.strip())
    cues: List[Dict] = []
    for block in blocks:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        # Skip WEBVTT header block.
        if lines[0].startswith("WEBVTT"):
            continue
        # Find the timing line (may be preceded by an optional cue identifier line).
        timing_idx = None
        match = None
        for i, line in enumerate(lines):
            m = _TIMING_RE.match(line)
            if m:
                timing_idx = i
                match = m
                break
        if timing_idx is None:
            continue
        text_lines = lines[timing_idx + 1:]
        if not text_lines:
            continue
        joined = " ".join(text_lines)
        text = _strip_tags(joined).strip()
        text = re.sub(r"\s+", " ", text)
        if not text:
            continue
        start = _ts_to_seconds(match.group(1), match.group(2), match.group(3))
        end = _ts_to_seconds(match.group(4), match.group(5), match.group(6))
        cues.append({"start": start, "end": end, "text": text})
    return cues


def _dedup_overlap(cues: List[Dict]) -> List[Dict]:
    """Remove rolling-overlap word duplication between consecutive cues."""
    if not cues:
        return []
    result = [cues[0]]
    for curr in cues[1:]:
        prev_words = result[-1]["text"].split()
        curr_words = curr["text"].split()
        max_overlap = 0
        # Find the longest word-suffix of prev that equals a word-prefix of curr.
        upper = min(len(prev_words), len(curr_words))
        for k in range(upper, 0, -1):
            if prev_words[-k:] == curr_words[:k]:
                max_overlap = k
                break
        new_words = curr_words[max_overlap:]
        if new_words:
            result.append(
                {"start": curr["start"], "end": curr["end"], "text": " ".join(new_words)}
            )
    return result


def parse_vtt_file(path: Path | str) -> List[Dict]:
    content = Path(path).read_text(encoding="utf-8")
    raw = _parse_raw_cues(content)
    return _dedup_overlap(raw)


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 parse_vtt.py <path-to-vtt>", file=sys.stderr)
        return 2
    cues = parse_vtt_file(argv[1])
    json.dump(cues, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
