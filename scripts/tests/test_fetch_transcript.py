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


class TestRunSubsDownloadNetworkError:
    def test_surfaces_yt_dlp_stderr_when_subs_download_fails(self, tmp_path, capsys):
        def fake_run(cmd, *args, **kwargs):
            if "--dump-json" in cmd:
                return _completed(stdout=json.dumps(METADATA_OK))
            # Subs download fails with a non-zero exit and a network-style stderr.
            return _completed(
                returncode=1,
                stderr="ERROR: Unable to download webpage: HTTPSConnectionPool(host='youtube.com', port=443): Max retries exceeded",
            )

        with patch.object(fetch_transcript.shutil, "which", side_effect=_which_side_effect(True)), \
             patch.object(fetch_transcript.subprocess, "run", side_effect=fake_run):
            rc = fetch_transcript.run(
                url="https://youtu.be/8rABwKRsec4",
                output_dir=str(tmp_path),
                force=False,
            )

        captured = capsys.readouterr()
        assert rc != 0
        # yt-dlp stderr was surfaced (not silently swallowed).
        assert "yt-dlp:" in captured.err
        assert "Max retries exceeded" in captured.err
        # The "no captions" fallback message also fires (acceptable double-message).
        assert "No English captions available" in captured.err


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
