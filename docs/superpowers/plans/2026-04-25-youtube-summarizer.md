# YouTube Summarizer Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill that takes a YouTube URL and produces three artifacts in a per-video subfolder: raw VTT transcript, speaker-labeled processed transcript, and a structured summary file.

**Architecture:** Two layers. Python helpers in `scripts/` do deterministic work (yt-dlp wrapping, VTT parsing, slug derivation). `SKILL.md` is the entrypoint Claude reads — it orchestrates the helpers and embeds prompts for the LLM-driven stages (speaker inference, topic-shift paragraphing, summary writing).

**Tech Stack:** Python 3 (stdlib only), `yt-dlp` (system binary), `pytest` for unit tests, Markdown for skill/output files.

**Spec:** `docs/superpowers/specs/2026-04-25-youtube-summarizer-design.md` — read it first.

---

## File Structure

Files created by this plan:

| File | Responsibility |
|---|---|
| `.gitignore` | Ignore Python cruft (`__pycache__/`, `.pytest_cache/`) |
| `scripts/__init__.py` | Make `scripts/` a package so tests can import |
| `scripts/slug.py` | Pure function: `(title, video_id) → slug`. No side effects. |
| `scripts/parse_vtt.py` | VTT file → cues JSON on stdout. Strips styling, dedups rolling overlap. CLI + library. |
| `scripts/fetch_transcript.py` | yt-dlp wrapper. Resolves metadata, derives slug, downloads English VTT, emits metadata JSON. CLI. |
| `scripts/tests/__init__.py` | Empty marker for test package |
| `scripts/tests/test_slug.py` | Unit tests for slug derivation |
| `scripts/tests/test_parse_vtt.py` | Fixture-driven tests for VTT parser |
| `scripts/tests/test_fetch_transcript.py` | Tests for yt-dlp wrapper using `subprocess.run` mocks |
| `scripts/tests/fixtures/simple.vtt` | Clean 3-cue VTT |
| `scripts/tests/fixtures/rolling_overlap.vtt` | Sliding-window auto-caption VTT for dedup tests |
| `scripts/tests/fixtures/styled.vtt` | VTT with `<c>` styling tags and cue settings |
| `scripts/tests/fixtures/empty.vtt` | Header-only VTT |
| `SKILL.md` | Skill entrypoint Claude reads. Orchestration narrative + LLM prompts for Stages 2 and 3. |
| `README.md` | Human-facing overview, install instructions |

Each file has one focused responsibility. The Python helpers expose CLI interfaces (so `SKILL.md` can call them as shell commands) AND can be imported by tests.

---

## Task 1: Project Scaffolding

**Files:**
- Create: `.gitignore`
- Create: `conftest.py` (repo-root pytest shim — adds repo root to `sys.path` so `from scripts.X import Y` works in tests)
- Create: `scripts/__init__.py` (empty)
- Create: `scripts/tests/__init__.py` (empty)
- Create: `scripts/tests/fixtures/.gitkeep` (empty placeholder, replaced in later tasks)

- [ ] **Step 1: Create `.gitignore`**

```gitignore
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.coverage
*.tmp
.venv/
.DS_Store
```

- [ ] **Step 2: Create `conftest.py` at the repo root**

This ensures pytest adds the repo root to `sys.path` so test files can import `scripts.slug`, `scripts.parse_vtt`, etc.

```python
"""Repo-root pytest configuration: ensure the repo root is on sys.path so
test files can import the `scripts.*` package."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
```

- [ ] **Step 3: Create the empty package markers**

```bash
mkdir -p /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/scripts/tests/fixtures
touch /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/scripts/__init__.py
touch /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/scripts/tests/__init__.py
touch /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/scripts/tests/fixtures/.gitkeep
```

- [ ] **Step 4: Confirm pytest is available (or install it)**

Run: `python3 -c "import pytest; print(pytest.__version__)"`
Expected: prints a version (any 7.x or 8.x is fine). If `ModuleNotFoundError`, run `pip install --user pytest` and re-check.

- [ ] **Step 5: Commit**

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
git add .gitignore conftest.py scripts/__init__.py scripts/tests/__init__.py scripts/tests/fixtures/.gitkeep
git commit -m "chore: scaffold scripts package layout"
```

---

## Task 2: `scripts/slug.py` (TDD)

**Files:**
- Create: `scripts/slug.py`
- Create: `scripts/tests/test_slug.py`

**Slug rule recap (from spec):**
1. Drop diacritics; replace any non-alphanumeric character with whitespace.
2. Split on whitespace into tokens.
3. For each token: if the token contains a run of 2+ consecutive uppercase letters anywhere, preserve the whole token as-is (acronym handling). Otherwise, lowercase the token and capitalize the first letter (Title-case).
4. Join tokens. Lowercase the very first character of the result.
5. Cap at 60 characters.
6. Append `-<video_id>`.

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_slug.py`:

```python
"""Tests for the slug derivation function."""
import pytest

from scripts.slug import make_slug


class TestMakeSlug:
    def test_basic_title(self):
        assert make_slug("How AI Works | Karpathy", "8rABwKRsec4") == "howAIWorksKarpathy-8rABwKRsec4"

    def test_preserves_acronyms(self):
        assert make_slug("NASA and the FBI", "abc12345678") == "nASAAndTheFBI-abc12345678"

    def test_acronym_first_word_lowercases_first_char(self):
        # Even when the first input token is an acronym, the FIRST CHARACTER
        # of the joined output is lowercased per rule 4.
        assert make_slug("NASA Foo", "xyz98765432") == "nASAFoo-xyz98765432"

    def test_strips_punctuation(self):
        # Pipes, em-dashes, exclamation marks all become whitespace and split tokens.
        assert make_slug("Hello! World — 2024", "id1234567ab") == "helloWorld2024-id1234567ab"

    def test_strips_diacritics(self):
        # "café" → "cafe", "Pokémon" → "Pokemon"
        assert make_slug("Café Pokémon", "id1234567ab") == "cafePokemon-id1234567ab"

    def test_caps_at_60_chars_before_suffix(self):
        # 80-char title; slug body should be ≤60 chars, then -<videoId> appended.
        title = "ThisIsAVeryLongTitleThatGoesOnAndOnAndShouldBeCappedSomewhereSensible Extra"
        result = make_slug(title, "id1234567ab")
        # The part before "-id1234567ab" must be ≤60 chars.
        body, _, vid = result.rpartition("-")
        assert len(body) <= 60
        assert vid == "id1234567ab"

    def test_single_word_title(self):
        assert make_slug("Welcome", "id1234567ab") == "welcome-id1234567ab"

    def test_only_punctuation_title(self):
        # All non-alphanumeric → no tokens. Body becomes empty string.
        result = make_slug("!!! --- ???", "id1234567ab")
        assert result == "-id1234567ab"

    def test_empty_title(self):
        assert make_slug("", "id1234567ab") == "-id1234567ab"

    def test_acronym_inside_token(self):
        # "macOS" contains "OS" (2+ uppercase run) → preserve whole token.
        assert make_slug("macOS Tips", "id1234567ab") == "macOSTips-id1234567ab"

    def test_mixed_case_no_acronym(self):
        # "iPhone" — only single uppercase chars, no 2+ run → title-case it.
        assert make_slug("iPhone Tips", "id1234567ab") == "iphoneTips-id1234567ab"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer && python3 -m pytest scripts/tests/test_slug.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.slug'`.

- [ ] **Step 3: Implement `scripts/slug.py`**

Create `scripts/slug.py`:

```python
"""Derive a deterministic folder slug from a video title and ID.

Rule (from spec):
1. Drop diacritics; replace non-alphanumeric chars with whitespace.
2. Split on whitespace into tokens.
3. If a token contains any run of 2+ consecutive uppercase letters, preserve
   it as-is (acronym). Otherwise, lowercase + capitalize first letter.
4. Join tokens; lowercase the very first char of the result.
5. Cap at 60 chars.
6. Append "-<video_id>".
"""
from __future__ import annotations

import re
import unicodedata


_ACRONYM_RUN = re.compile(r"[A-Z]{2,}")
_NON_ALNUM = re.compile(r"[^A-Za-z0-9]+")


def _strip_diacritics(text: str) -> str:
    """Remove combining marks (so 'café' → 'cafe', 'Pokémon' → 'Pokemon')."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _transform_token(token: str) -> str:
    if _ACRONYM_RUN.search(token):
        return token
    return token[:1].upper() + token[1:].lower() if token else ""


def make_slug(title: str, video_id: str) -> str:
    cleaned = _strip_diacritics(title)
    tokens = _NON_ALNUM.split(cleaned)
    tokens = [t for t in tokens if t]

    transformed = [_transform_token(t) for t in tokens]
    body = "".join(transformed)

    if body:
        body = body[0].lower() + body[1:]

    if len(body) > 60:
        body = body[:60]

    return f"{body}-{video_id}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_slug.py -v`
Expected: all 11 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/slug.py scripts/tests/test_slug.py
git commit -m "feat: add slug derivation with TDD"
```

---

## Task 3: `scripts/parse_vtt.py` (TDD with fixtures)

**Files:**
- Create: `scripts/parse_vtt.py`
- Create: `scripts/tests/test_parse_vtt.py`
- Create: `scripts/tests/fixtures/simple.vtt`
- Create: `scripts/tests/fixtures/rolling_overlap.vtt`
- Create: `scripts/tests/fixtures/styled.vtt`
- Create: `scripts/tests/fixtures/empty.vtt`

- [ ] **Step 1: Create the four fixture files**

`scripts/tests/fixtures/simple.vtt`:

```
WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000
hello world

00:00:02.000 --> 00:00:04.000
this is a test

00:00:04.000 --> 00:00:06.000
of the parser
```

`scripts/tests/fixtures/rolling_overlap.vtt`:

```
WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000
welcome back to the podcast

00:00:02.000 --> 00:00:04.000
to the podcast today we're

00:00:04.000 --> 00:00:06.000
today we're talking with andrej
```

`scripts/tests/fixtures/styled.vtt`:

```
WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000 align:start position:0%
<00:00:00.000><c>hello</c><00:00:01.000><c> world</c>

00:00:02.000 --> 00:00:04.000
this is <i>italic</i> text
```

`scripts/tests/fixtures/empty.vtt`:

```
WEBVTT
Kind: captions
Language: en

```

(Note: keep the trailing newline. The file has the WEBVTT header and metadata but no cues.)

- [ ] **Step 2: Write the failing test**

Create `scripts/tests/test_parse_vtt.py`:

```python
"""Tests for the VTT parser."""
import json
from pathlib import Path

import pytest

from scripts.parse_vtt import parse_vtt_file

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseVttFile:
    def test_simple_three_cues(self):
        result = parse_vtt_file(FIXTURES / "simple.vtt")
        assert result == [
            {"start": 0, "end": 2, "text": "hello world"},
            {"start": 2, "end": 4, "text": "this is a test"},
            {"start": 4, "end": 6, "text": "of the parser"},
        ]

    def test_rolling_overlap_dedup(self):
        result = parse_vtt_file(FIXTURES / "rolling_overlap.vtt")
        # Cue 0 kept verbatim. Cue 1 overlaps cue 0 at "to the podcast" → keep "today we're".
        # Cue 2 overlaps cue 1 at "today we're" → keep "talking with andrej".
        assert result == [
            {"start": 0, "end": 2, "text": "welcome back to the podcast"},
            {"start": 2, "end": 4, "text": "today we're"},
            {"start": 4, "end": 6, "text": "talking with andrej"},
        ]

    def test_styled_tags_stripped(self):
        result = parse_vtt_file(FIXTURES / "styled.vtt")
        # Inline timing tags <00:..> and styling tags <c>, <i> all stripped.
        # Cue settings on the timing line (align:start, position:0%) ignored.
        assert result == [
            {"start": 0, "end": 2, "text": "hello world"},
            {"start": 2, "end": 4, "text": "this is italic text"},
        ]

    def test_empty_file_returns_empty_list(self):
        assert parse_vtt_file(FIXTURES / "empty.vtt") == []
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_parse_vtt.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.parse_vtt'`.

- [ ] **Step 4: Implement `scripts/parse_vtt.py`**

Create `scripts/parse_vtt.py`:

```python
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
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_parse_vtt.py -v`
Expected: all 4 tests PASS.

- [ ] **Step 6: Smoke-test the CLI**

Run: `python3 scripts/parse_vtt.py scripts/tests/fixtures/simple.vtt`
Expected stdout: `[{"start": 0, "end": 2, "text": "hello world"}, {"start": 2, "end": 4, "text": "this is a test"}, {"start": 4, "end": 6, "text": "of the parser"}]`

- [ ] **Step 7: Commit**

```bash
git add scripts/parse_vtt.py scripts/tests/test_parse_vtt.py scripts/tests/fixtures/
git commit -m "feat: add VTT parser with rolling-overlap dedup"
```

---

## Task 4: `scripts/fetch_transcript.py` (TDD with mocks)

**Files:**
- Create: `scripts/fetch_transcript.py`
- Create: `scripts/tests/test_fetch_transcript.py`

**Behavior:**
1. Verifies `yt-dlp` is on `$PATH`. If missing, prints install hint and exits non-zero.
2. Calls `yt-dlp --dump-json --no-download <url>` to get metadata.
3. Computes folder slug via `make_slug(title, video_id)`. Folder name: `<slug>--<YYYY.MM.DD>`. Resolves under `--output-dir` (default `$PWD`). Creates the folder.
4. Smart resume: if `<folder>/<basename>--original.vtt` exists and not `--force`, skip subs download.
5. Otherwise, calls `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs en --sub-format vtt --output <folder>/<basename> <url>`. Then locates the produced `.en.vtt` file (yt-dlp suffixes with language) and atomically moves it to `<folder>/<basename>--original.vtt`. Errors if no English subs were produced.
6. Emits metadata JSON to stdout (the structure documented in the spec).

The `<basename>` is `<slug>--<YYYY.MM.DD>` (folder name).

- [ ] **Step 1: Write the failing test**

Create `scripts/tests/test_fetch_transcript.py`:

```python
"""Tests for fetch_transcript.py — yt-dlp wrapper.

yt-dlp is mocked via subprocess.run patching. We do not hit the network.
"""
import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts import fetch_transcript


# --- helpers ---------------------------------------------------------------

METADATA_OK = {
    "id": "8rABwKRsec4",
    "title": "How AI Works | Karpathy",
    "channel": "Lex Fridman Podcast",
    "upload_date": "20240310",  # yt-dlp returns YYYYMMDD
    "duration": 7200,
    "webpage_url": "https://www.youtube.com/watch?v=8rABwKRsec4",
}


def _which_side_effect(found_yt_dlp: bool):
    """Make shutil.which return a path for yt-dlp iff found_yt_dlp is True."""
    def _which(cmd):
        if cmd == "yt-dlp":
            return "/usr/local/bin/yt-dlp" if found_yt_dlp else None
        return "/usr/bin/" + cmd
    return _which


def _completed(returncode=0, stdout="", stderr=""):
    cp = MagicMock(spec=subprocess.CompletedProcess)
    cp.returncode = returncode
    cp.stdout = stdout
    cp.stderr = stderr
    return cp


# --- tests -----------------------------------------------------------------

class TestRunMissingYtDlp:
    def test_prints_install_hint_and_exits_nonzero(self, capsys):
        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(False)):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=".",
                force=False,
            )
        captured = capsys.readouterr()
        assert rc != 0
        assert "yt-dlp not found" in captured.err
        assert "brew install yt-dlp" in captured.err


class TestRunHappyPath:
    def test_writes_original_vtt_and_emits_json(self, tmp_path, capsys):
        # Simulate yt-dlp creating "<basename>.en.vtt" inside the output folder.
        def fake_run(cmd, *args, **kwargs):
            # First call: --dump-json. Return metadata.
            if "--dump-json" in cmd:
                return _completed(stdout=json.dumps(METADATA_OK))
            # Second call: subs download. Find the --output template arg, write a fake VTT next to it.
            assert "--write-subs" in cmd or "--write-auto-subs" in cmd
            output_idx = cmd.index("--output")
            output_template = cmd[output_idx + 1]
            # yt-dlp normally appends ".en.vtt" to the template.
            produced = Path(output_template + ".en.vtt")
            produced.parent.mkdir(parents=True, exist_ok=True)
            produced.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nhello\n", encoding="utf-8")
            return _completed(returncode=0)

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=str(tmp_path),
                force=False,
            )

        captured = capsys.readouterr()
        assert rc == 0
        emitted = json.loads(captured.out)
        assert emitted["video_id"] == "8rABwKRsec4"
        assert emitted["title"] == "How AI Works | Karpathy"
        assert emitted["channel"] == "Lex Fridman Podcast"
        assert emitted["upload_date"] == "2024-03-10"
        assert emitted["url"] == "https://youtu.be/8rABwKRsec4"
        assert emitted["slug"] == "howAIWorksKarpathy-8rABwKRsec4"
        # Folder and file must exist on disk.
        folder = Path(emitted["folder"])
        vtt = Path(emitted["vtt_path"])
        assert folder.is_dir()
        assert folder.name == "howAIWorksKarpathy-8rABwKRsec4--2024.03.10"
        assert vtt.is_file()
        assert vtt.name.endswith("--original.vtt")
        assert "WEBVTT" in vtt.read_text(encoding="utf-8")


class TestRunSmartResume:
    def test_skips_subs_download_when_vtt_already_present(self, tmp_path, capsys):
        calls = []

        def fake_run(cmd, *args, **kwargs):
            calls.append(cmd)
            if "--dump-json" in cmd:
                return _completed(stdout=json.dumps(METADATA_OK))
            # Subs download should NOT be called on resume.
            raise AssertionError(f"yt-dlp subs download should be skipped, got: {cmd}")

        # Pre-create the expected --original.vtt.
        folder = tmp_path / "howAIWorksKarpathy-8rABwKRsec4--2024.03.10"
        folder.mkdir()
        (folder / "howAIWorksKarpathy-8rABwKRsec4--2024.03.10--original.vtt").write_text(
            "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\npre-existing\n", encoding="utf-8"
        )

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=str(tmp_path),
                force=False,
            )

        assert rc == 0
        # Only --dump-json was called; no subs download.
        assert len(calls) == 1
        assert "--dump-json" in calls[0]
        # JSON still emitted correctly.
        emitted = json.loads(capsys.readouterr().out)
        assert emitted["vtt_path"].endswith("--original.vtt")


class TestRunPrivateVideo:
    def test_surfaces_yt_dlp_error_and_exits_nonzero(self, tmp_path, capsys):
        def fake_run(cmd, *args, **kwargs):
            if "--dump-json" in cmd:
                return _completed(returncode=1, stderr="ERROR: Private video. Sign in if you've been granted access to this video")
            raise AssertionError("Should not reach subs download")

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/private0000",
                output_dir=str(tmp_path),
                force=False,
            )

        captured = capsys.readouterr()
        assert rc != 0
        assert "yt-dlp:" in captured.err
        assert "Private video" in captured.err


class TestRunNoEnglishCaptions:
    def test_errors_when_no_vtt_produced(self, tmp_path, capsys):
        def fake_run(cmd, *args, **kwargs):
            if "--dump-json" in cmd:
                return _completed(stdout=json.dumps(METADATA_OK))
            # Subs download "succeeds" but writes no .en.vtt file.
            return _completed(returncode=0)

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=str(tmp_path),
                force=False,
            )

        captured = capsys.readouterr()
        assert rc != 0
        assert "No English captions available" in captured.err
        assert "8rABwKRsec4" in captured.err


class TestRunForceClobbers:
    def test_force_redownloads_even_when_vtt_present(self, tmp_path, capsys):
        calls = []

        def fake_run(cmd, *args, **kwargs):
            calls.append(cmd)
            if "--dump-json" in cmd:
                return _completed(stdout=json.dumps(METADATA_OK))
            # Subs download — write a fresh fake VTT.
            output_idx = cmd.index("--output")
            output_template = cmd[output_idx + 1]
            produced = Path(output_template + ".en.vtt")
            produced.parent.mkdir(parents=True, exist_ok=True)
            produced.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nfresh\n", encoding="utf-8")
            return _completed(returncode=0)

        # Pre-create a stale --original.vtt that --force should clobber.
        folder = tmp_path / "howAIWorksKarpathy-8rABwKRsec4--2024.03.10"
        folder.mkdir()
        stale = folder / "howAIWorksKarpathy-8rABwKRsec4--2024.03.10--original.vtt"
        stale.write_text("STALE", encoding="utf-8")

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=str(tmp_path),
                force=True,
            )

        assert rc == 0
        # Both calls happened: --dump-json AND subs download.
        assert len(calls) == 2
        # File was replaced.
        assert "fresh" in stale.read_text(encoding="utf-8")
        assert "STALE" not in stale.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/tests/test_fetch_transcript.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.fetch_transcript'`.

- [ ] **Step 3: Implement `scripts/fetch_transcript.py`**

Create `scripts/fetch_transcript.py`:

```python
"""yt-dlp wrapper. Resolves video metadata, derives folder/slug, downloads
English VTT subtitles (manual preferred, auto-generated fallback), and emits
metadata JSON to stdout.

CLI:
  python3 scripts/fetch_transcript.py <url> [--output-dir <path>] [--force]

Output (stdout, single JSON line):
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

Errors print to stderr; exit code is non-zero on any failure.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Make the script runnable directly (`python3 scripts/fetch_transcript.py …`)
# AND importable as `scripts.fetch_transcript` from tests. Add the repo root
# to sys.path so the `from scripts.slug import …` below resolves either way.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.slug import make_slug


YT_DLP_INSTALL_HINT = (
    "yt-dlp not found. Install with: brew install yt-dlp\n"
    "(or: pip install --user yt-dlp)\n"
)


def _format_date(yyyymmdd: str) -> str:
    """Convert yt-dlp's YYYYMMDD to YYYY.MM.DD."""
    if len(yyyymmdd) != 8:
        return yyyymmdd
    return f"{yyyymmdd[0:4]}.{yyyymmdd[4:6]}.{yyyymmdd[6:8]}"


def _date_iso(yyyymmdd: str) -> str:
    """Convert yt-dlp's YYYYMMDD to YYYY-MM-DD for the JSON output."""
    if len(yyyymmdd) != 8:
        return yyyymmdd
    return f"{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}"


def _fetch_metadata(url: str) -> dict | None:
    """Call yt-dlp --dump-json --no-download. Returns parsed metadata or None on error."""
    cmd = ["yt-dlp", "--dump-json", "--no-download", url]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        msg = cp.stderr.strip().splitlines()[-1] if cp.stderr else f"exit code {cp.returncode}"
        sys.stderr.write(f"yt-dlp: {msg}\n")
        return None
    try:
        return json.loads(cp.stdout)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"yt-dlp: failed to parse metadata JSON ({e})\n")
        return None


def _download_subs(url: str, output_template: str) -> bool:
    """Call yt-dlp to download English subs (manual preferred, auto fallback).

    yt-dlp writes to <output_template>.en.vtt (or similar locale variant).
    Returns True if at least one .en*.vtt file was produced.
    """
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "en.*,en",
        "--sub-format", "vtt",
        "--output", output_template,
        url,
    ]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        msg = cp.stderr.strip().splitlines()[-1] if cp.stderr else f"exit code {cp.returncode}"
        sys.stderr.write(f"yt-dlp: {msg}\n")
        return False
    # yt-dlp may produce <template>.en.vtt or <template>.en-orig.vtt etc.
    parent = Path(output_template).parent
    base = Path(output_template).name
    matches = sorted(parent.glob(f"{base}.en*.vtt"))
    return len(matches) > 0


def _locate_produced_vtt(output_template: str) -> Path | None:
    parent = Path(output_template).parent
    base = Path(output_template).name
    matches = sorted(parent.glob(f"{base}.en*.vtt"))
    return matches[0] if matches else None


def run(url: str, output_dir: str, force: bool) -> int:
    if not shutil.which("yt-dlp"):
        sys.stderr.write(YT_DLP_INSTALL_HINT)
        return 1

    metadata = _fetch_metadata(url)
    if metadata is None:
        return 1

    video_id = metadata.get("id") or ""
    title = metadata.get("title") or ""
    channel = metadata.get("channel") or metadata.get("uploader") or ""
    upload_date = metadata.get("upload_date") or ""
    webpage_url = metadata.get("webpage_url") or url

    if not video_id or not upload_date:
        sys.stderr.write(f"yt-dlp: incomplete metadata (id={video_id!r}, upload_date={upload_date!r})\n")
        return 1

    slug = make_slug(title, video_id)
    folder_name = f"{slug}--{_format_date(upload_date)}"
    folder = Path(output_dir).resolve() / folder_name
    folder.mkdir(parents=True, exist_ok=True)

    basename = folder_name  # files inside the folder share this prefix
    target_vtt = folder / f"{basename}--original.vtt"

    if force and target_vtt.exists():
        target_vtt.unlink()

    needs_download = not target_vtt.exists() or target_vtt.stat().st_size == 0

    if needs_download:
        # yt-dlp writes to <template>.en*.vtt; we pass a template without an extension.
        output_template = str(folder / basename)
        ok = _download_subs(webpage_url, output_template)
        if not ok:
            sys.stderr.write(
                f"No English captions available for {video_id}. Skill requires English subs.\n"
            )
            return 1
        produced = _locate_produced_vtt(output_template)
        if produced is None:
            sys.stderr.write(
                f"No English captions available for {video_id}. Skill requires English subs.\n"
            )
            return 1
        # Atomic-ish move to canonical name.
        tmp = target_vtt.with_suffix(target_vtt.suffix + ".tmp")
        shutil.move(str(produced), str(tmp))
        os.replace(str(tmp), str(target_vtt))

    result = {
        "slug": slug,
        "folder": str(folder),
        "video_id": video_id,
        "title": title,
        "channel": channel,
        "upload_date": _date_iso(upload_date),
        "url": webpage_url,
        "vtt_path": str(target_vtt),
    }
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript via yt-dlp.")
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--output-dir", default=".", help="Where to create the per-video folder (default: cwd)")
    parser.add_argument("--force", action="store_true", help="Re-download even if --original.vtt exists")
    args = parser.parse_args(argv[1:])
    return run(url=args.url, output_dir=args.output_dir, force=args.force)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest scripts/tests/test_fetch_transcript.py -v`
Expected: all 6 tests PASS.

- [ ] **Step 5: Run the full unit-test suite**

Run: `python3 -m pytest scripts/tests/ -v`
Expected: all tests across slug + parse_vtt + fetch_transcript PASS (21 total).

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch_transcript.py scripts/tests/test_fetch_transcript.py
git commit -m "feat: add yt-dlp transcript fetcher with smart resume"
```

---

## Task 5: `SKILL.md` — Skill Entrypoint with LLM Prompts

**Files:**
- Create: `SKILL.md`

`SKILL.md` is the file Claude reads when this skill is invoked. It is NOT executable code — it's a Markdown narrative that tells Claude how to orchestrate the helpers and what prompts to use for the two LLM-driven stages.

The `description` in the frontmatter is what Claude uses to decide whether the skill applies. Make it specific.

- [ ] **Step 1: Create `SKILL.md`**

````markdown
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

Run:

```bash
python3 scripts/fetch_transcript.py <URL> [--output-dir <path>] [--force]
```

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

1. Run `python3 scripts/parse_vtt.py <vtt_path>`. Capture the JSON list of cues from stdout. Each cue has `start` (seconds), `end` (seconds), `text`.
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
````

- [ ] **Step 2: Sanity-check `SKILL.md` parses as valid Markdown with frontmatter**

Run: `python3 -c "import re,sys; t=open('SKILL.md').read(); m=re.match(r'---\n(.*?)\n---\n', t, re.S); assert m, 'no frontmatter'; assert 'name:' in m.group(1); assert 'description:' in m.group(1); print('OK')"`
Expected: prints `OK`.

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md with stage 2 and stage 3 prompts"
```

---

## Task 6: `README.md` — Human-Facing Overview

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create `README.md`**

````markdown
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
````

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

---

## Task 7: End-to-End Smoke Verification (Manual)

This is **manual verification**, not automated. The LLM stages can't be unit-tested deterministically. Pick a short, low-stakes real video to confirm the full pipeline works.

**Files:** None created. This task verifies the skill end-to-end.

- [ ] **Step 1: Confirm `yt-dlp` is installed**

Run: `which yt-dlp && yt-dlp --version`
Expected: prints the path and a version string. If missing, install with `brew install yt-dlp` and re-check.

- [ ] **Step 2: Pick a short test video**

Use any short (~3–10 min) public video with English captions and clear speakers. A good default is a single-speaker tech talk; a 2-speaker interview is even better for verifying speaker inference.

- [ ] **Step 3: Run Stage 1 directly via the helper**

From a scratch directory (e.g., `/tmp/yt-test`):

```bash
mkdir -p /tmp/yt-test && cd /tmp/yt-test
python3 /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/scripts/fetch_transcript.py "<URL>"
```

Expected: a JSON line on stdout, and a folder `<slug>--<YYYY.MM.DD>/` containing `<basename>--original.vtt` (non-empty, starts with `WEBVTT`).

- [ ] **Step 4: Run Stage 1's parser on the produced VTT**

```bash
python3 /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer/scripts/parse_vtt.py /tmp/yt-test/<folder>/<basename>--original.vtt | head -c 400
```

Expected: a JSON array of cue objects. No errors.

- [ ] **Step 5: Invoke the skill end-to-end through Claude Code**

In a new Claude Code session inside `/tmp/yt-test`, ask: `Summarize this video: <URL>`. Claude should pick up the skill (because of the `description` frontmatter), run all three stages, and report the three artifact paths.

Verify each output file:

- `--original.vtt`: starts with `WEBVTT`, contains cues.
- `--processed.md`:
  - Has H1 title, channel/upload-date/URL bullets, `---` separator.
  - At least one paragraph header line in the form `[MM:SS](https://youtu.be/<id>?t=N) **SPEAKER**`.
  - Paragraphs flow as readable prose, not 2-second fragments.
- `--summary.md`:
  - Has all five section headings: Summary, Key Takeaways, Action Items, Lists Mentioned, Salient Quotes.
  - Empty sections show `_None._` rather than being missing.
  - At least one timestamp link somewhere in Action Items / Lists / Quotes (when applicable).

- [ ] **Step 6: Verify smart resume**

Re-run the same prompt. Claude should detect existing files and skip all three stages, reporting that nothing was regenerated.

Then re-run with `--force` (e.g., `Summarize this video: <URL> --force`). All three files should be regenerated.

- [ ] **Step 7: Note any prompt-regression observations**

If the processed or summary file is poor quality (wrong speakers, missing action items, etc.), iterate on the Stage 2 / Stage 3 prompts in `SKILL.md`. Commit prompt changes with `chore: tune <stage> prompt — <observation>`.

- [ ] **Step 8: Final commit if any tuning happened**

```bash
git status
# If SKILL.md changed:
git add SKILL.md
git commit -m "chore: tune prompts based on smoke verification"
```

If no changes were needed, this task is complete.

---

## Done

After Task 7, the skill is functional:

- `scripts/` has three helpers with full unit-test coverage.
- `SKILL.md` is the orchestrator Claude reads when a YouTube URL is mentioned.
- `README.md` documents install + usage.
- One real video has been processed end-to-end and inspected.
