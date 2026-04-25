# Cleanup Duplicate VTT Files Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `fetch_transcript.py` leave exactly one VTT (`<basename>--original.vtt`) in the per-video folder, even when yt-dlp produces multiple `.en*.vtt` files.

**Architecture:** Add a cleanup loop inside `_download_subs` that, after picking `matches[0]` to keep, `unlink()`s every other entry returned by the `glob`. The caller's existing rename to `--original.vtt` then leaves the folder with one VTT. New TDD test simulates the multi-file case; existing single-file tests stay green.

**Tech Stack:** Python 3, pytest, yt-dlp (mocked via `subprocess.run` patching).

**Spec:** `docs/superpowers/specs/2026-04-25-cleanup-duplicate-vtt-design.md`

---

## File Structure

- **Modify:** `scripts/fetch_transcript.py` — add cleanup loop in `_download_subs` (lines 77-105).
- **Modify:** `scripts/tests/test_fetch_transcript.py` — add new test class for multi-file case.
- **Delete:** `theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt` — untracked orphan from prior smoke test.

---

### Task 1: Failing test for multi-file cleanup

**Files:**
- Modify: `scripts/tests/test_fetch_transcript.py` (append a new class at end)

- [ ] **Step 1: Add the failing test class**

Append to `scripts/tests/test_fetch_transcript.py`:

```python
class TestRunCleansUpDuplicateVtts:
    """When yt-dlp produces multiple .en*.vtt files (manual + auto-generated),
    only the canonical --original.vtt should remain in the folder."""

    def test_extra_en_vtts_are_removed(self, tmp_path, capsys):
        def fake_run(cmd, *args, **kwargs):
            if "--dump-json" in cmd:
                return _completed(stdout=json.dumps(METADATA_OK))
            # Subs download — write TWO fake VTTs (e.g., manual + auto-generated original).
            output_idx = cmd.index("--output")
            output_template = cmd[output_idx + 1]
            parent = Path(output_template).parent
            parent.mkdir(parents=True, exist_ok=True)
            # Distinguishable contents so we can tell which one was kept.
            # Sorted alphabetically: ".en-orig.vtt" < ".en.vtt" (since '-' < '.' in ASCII),
            # so .en-orig.vtt is matches[0] and is what gets kept.
            Path(output_template + ".en.vtt").write_text(
                "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nMANUAL\n", encoding="utf-8"
            )
            Path(output_template + ".en-orig.vtt").write_text(
                "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nAUTO-ORIG\n", encoding="utf-8"
            )
            return _completed(returncode=0)

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=str(tmp_path),
                force=False,
            )

        assert rc == 0
        emitted = json.loads(capsys.readouterr().out)
        folder = Path(emitted["folder"])
        # Exactly one VTT remains: the canonical --original.vtt.
        vtts = sorted(folder.glob("*.vtt"))
        assert len(vtts) == 1, f"Expected 1 VTT, got {[p.name for p in vtts]}"
        assert vtts[0].name.endswith("--original.vtt")
        # The kept content is matches[0] = the .en-orig.vtt body.
        assert "AUTO-ORIG" in vtts[0].read_text(encoding="utf-8")
        # No leftover .en*.vtt siblings.
        siblings = list(folder.glob("*.en*.vtt"))
        assert siblings == [], f"Unexpected leftover VTTs: {[p.name for p in siblings]}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer && python3 -m pytest scripts/tests/test_fetch_transcript.py::TestRunCleansUpDuplicateVtts -v`

Expected: FAIL — the assertion `len(vtts) == 1` fails because the leftover `<basename>.en.vtt` is still present alongside `--original.vtt`.

- [ ] **Step 3: Commit the failing test**

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
git add scripts/tests/test_fetch_transcript.py
git commit -m "test: add failing test for duplicate VTT cleanup"
```

---

### Task 2: Implement cleanup in `_download_subs`

**Files:**
- Modify: `scripts/fetch_transcript.py:102-105`

- [ ] **Step 1: Replace the tail of `_download_subs`**

In `scripts/fetch_transcript.py`, replace the existing block:

```python
    parent = Path(output_template).parent
    base = Path(output_template).name
    matches = sorted(parent.glob(f"{base}.en*.vtt"))
    return matches[0] if matches else None
```

with:

```python
    parent = Path(output_template).parent
    base = Path(output_template).name
    matches = sorted(parent.glob(f"{base}.en*.vtt"))
    if not matches:
        return None
    kept, *extras = matches
    for extra in extras:
        extra.unlink()
    return kept
```

- [ ] **Step 2: Run the new test to verify it passes**

Run: `cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer && python3 -m pytest scripts/tests/test_fetch_transcript.py::TestRunCleansUpDuplicateVtts -v`

Expected: PASS.

- [ ] **Step 3: Run the full test suite to verify no regressions**

Run: `cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer && python3 -m pytest scripts/tests/ -v`

Expected: ALL PASS (existing single-file tests `TestRunHappyPath`, `TestRunSmartResume`, `TestRunPrivateVideo`, `TestRunNoEnglishCaptions`, `TestRunForceClobbers`, `TestRunSubsDownloadNetworkError`, plus the new `TestRunCleansUpDuplicateVtts`).

- [ ] **Step 4: Commit**

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
git add scripts/fetch_transcript.py
git commit -m "fix(fetch_transcript): clean up extra .en*.vtt files after rename"
```

---

### Task 3: Remove the orphan VTT from the sample folder

**Files:**
- Delete: `theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt`

- [ ] **Step 1: Verify the orphan is byte-identical to the committed `--original.vtt` (sanity)**

Run:

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
diff theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11--original.vtt \
     theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt
```

Expected: empty output (files are byte-identical). If non-empty, STOP and surface to user — do not delete.

- [ ] **Step 2: Verify the orphan is untracked (not in git index)**

Run:

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
git ls-files --error-unmatch theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt
```

Expected: exit code 1 with "did not match any file" — confirms the file is untracked. If it IS tracked, STOP and surface to user.

- [ ] **Step 3: Delete the orphan**

Run:

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
rm theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11.en.vtt
```

- [ ] **Step 4: Verify the sample folder now has exactly the four expected artifacts**

Run:

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
ls theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11/
```

Expected output (exactly these four):

```
theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11--original.vtt
theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11--processed.md
theNewCodeSeanGroveOpenAI-8rABwKRsec4--2025.07.11--summary.md
```

(There is no fourth — the smoke-test sample is three artifacts.)

- [ ] **Step 5: Verify git status is clean**

Run:

```bash
cd /Users/galelovelace/dev/github/CodifiedBlue/skills/youtube-summarizer
git status
```

Expected: "nothing to commit, working tree clean" (the orphan was untracked, so its deletion does not produce a staged change). No commit needed for this task.

---

## Self-Review

**Spec coverage:**

| Spec section                              | Implemented in       |
| ----------------------------------------- | -------------------- |
| Cleanup logic inside `_download_subs`     | Task 2               |
| `matches[0]` kept, others `unlink()`'d    | Task 2 Step 1        |
| Edge case: 0 matches → `None`             | Task 2 Step 1 (`if not matches: return None`) |
| Edge case: 1 match → unchanged            | Task 2 Step 1 (`*extras` is `[]`, loop is no-op) — covered by existing single-file tests in Step 3 |
| Edge case: 2+ matches → cleanup           | Task 2 Step 1 + Task 1 test |
| Multi-file test                           | Task 1               |
| Sample folder orphan deletion             | Task 3               |
| No `SKILL.md` / `README.md` changes (out of scope) | not in plan, correct |

No gaps.

**Placeholder scan:** No TBDs, TODOs, "appropriate error handling," or skeleton steps. Every code block is complete.

**Type consistency:** `_download_subs` returns `Path | None` in the existing signature; new code returns `kept` (a `Path` from `parent.glob(...)`) or `None`. Consistent. The new test references `fetch_transcript.run`, `_completed`, `_which_side_effect`, `METADATA_OK` — all defined at the top of the existing test file.
