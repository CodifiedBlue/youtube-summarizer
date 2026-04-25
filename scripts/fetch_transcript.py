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
        stripped = cp.stderr.strip() if cp.stderr else ""
        lines = stripped.splitlines()
        msg = lines[-1] if lines else f"exit code {cp.returncode}"
        sys.stderr.write(f"yt-dlp: {msg}\n")
        return None
    try:
        return json.loads(cp.stdout)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"yt-dlp: failed to parse metadata JSON ({e})\n")
        return None


def _download_subs(url: str, output_template: str) -> Path | None:
    """Call yt-dlp to download English subs (manual preferred, auto fallback).

    yt-dlp writes to <output_template>.en.vtt (or similar locale variant).
    Returns the Path of the produced .en*.vtt file, or None on failure
    (yt-dlp non-zero exit OR no .en*.vtt file found).
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
        return None
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
        produced = _download_subs(webpage_url, output_template)
        if produced is None or produced.stat().st_size == 0:
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
        "url": f"https://youtu.be/{video_id}",
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
