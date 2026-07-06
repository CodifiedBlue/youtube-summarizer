"""Download a YouTube video (capped resolution) and extract candidate frames
for on-screen-visual analysis (graphs, charts, tables, slides, diagrams).

Deterministic layer only: this script does NOT judge which frames are salient.
It relies on a simple, powerful heuristic to keep the candidate set tiny (and
therefore cheap for the vision layer): salient visuals are *held still* on
screen, while talking heads, transitions, animations, and b-roll are in
constant motion. So instead of sampling every scene change, it uses ffmpeg's
`freezedetect` filter to find segments where the picture stops changing for at
least `--min-hold` seconds and keeps ONE representative frame per held segment.

A pure talking-head video therefore yields ~zero candidates (nothing is held
static), and a slide/chart deck yields one frame per slide. Claude (the vision
layer) then reads only this small set and picks the genuinely salient ones.

CLI:
  python3 scripts/extract_frames.py <url> --folder <folder> [--basename <name>]
      [--force] [--freeze-noise N] [--min-hold S] [--min-gap S]
      [--max-candidates N] [--max-height PX] [--keep-video]

Output (stdout, single JSON line):
  {
    "frames_dir": "/abs/path/frames",
    "manifest_path": "/abs/path/frames/manifest.json",
    "count": 8,
    "frames": [
      {"file": "frame-00012s.jpg", "path": "/abs/.../frame-00012s.jpg",
       "seconds": 12, "timestamp": "00:12"},
      ...
    ]
  }

Errors print to stderr; exit code is non-zero on any failure. A missing
ffmpeg/ffprobe is a hard error (the caller decides whether to continue
without visuals).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

FFMPEG_INSTALL_HINT = (
    "ffmpeg/ffprobe not found. Install with: brew install ffmpeg\n"
)
YT_DLP_INSTALL_HINT = (
    "yt-dlp not found. Install with: brew install yt-dlp\n"
    "(or: pip install --user yt-dlp)\n"
)

_FREEZE_RE = re.compile(
    r"lavfi\.freezedetect\.freeze_(start|duration|end)=(-?\d+(?:\.\d+)?)"
)

# A freeze segment: (start_seconds, end_seconds|None, duration_seconds|None).
# end/duration are None when the video ends while still frozen.
FreezeSegment = Tuple[float, Optional[float], Optional[float]]


def _format_timestamp(seconds: int) -> str:
    """Seconds -> MM:SS (under 1h) or HH:MM:SS (1h+), zero-padded."""
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def parse_freeze_segments(stderr: str) -> List[FreezeSegment]:
    """Parse ffmpeg `freezedetect` metadata from stderr into freeze segments.

    freezedetect logs, in order:
      freeze_start=<t>          when the picture stops changing
      freeze_duration=<d>       ) emitted together when motion resumes
      freeze_end=<t>            )
    If the clip ends while frozen, the trailing segment has no duration/end.
    """
    segments: List[FreezeSegment] = []
    open_start: Optional[float] = None
    open_dur: Optional[float] = None
    for kind, value in _FREEZE_RE.findall(stderr):
        val = float(value)
        if kind == "start":
            if open_start is not None:
                segments.append((open_start, None, None))
            open_start = val
            open_dur = None
        elif kind == "duration":
            open_dur = val
        elif kind == "end":
            if open_start is not None:
                segments.append((open_start, val, open_dur))
                open_start = None
                open_dur = None
    if open_start is not None:
        segments.append((open_start, None, open_dur))
    return segments


def representative_times(
    segments: List[FreezeSegment], *, min_hold: float, settle: float = 1.0
) -> List[float]:
    """Pick one timestamp inside each held segment.

    Grabs a frame `settle` seconds after the freeze begins (capped at the
    segment midpoint) so the content is fully rendered and we never land on a
    transition frame.
    """
    times: List[float] = []
    for start, _end, dur in segments:
        span = dur if dur is not None else min_hold
        offset = min(settle, max(0.0, span / 2.0))
        times.append(round(start + offset, 3))
    return times


def select_candidates(
    times: List[float],
    *,
    min_gap: float,
    max_candidates: int,
) -> List[float]:
    """Thin a list of ordered candidate timestamps (seconds).

    1. Drop any timestamp within `min_gap` seconds of the previously kept one.
    2. If more than `max_candidates` remain, keep an evenly-spaced subset
       (always retaining the first and last).
    """
    if not times:
        return []

    ordered = sorted(times)
    thinned: List[float] = []
    for t in ordered:
        if not thinned or (t - thinned[-1]) >= min_gap:
            thinned.append(t)

    if max_candidates <= 0 or len(thinned) <= max_candidates:
        return thinned

    if max_candidates == 1:
        return [thinned[0]]

    n = len(thinned)
    step = (n - 1) / (max_candidates - 1)
    idxs = sorted({round(i * step) for i in range(max_candidates)})
    return [thinned[i] for i in idxs]


def _check_binaries() -> Optional[str]:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        return FFMPEG_INSTALL_HINT
    if not shutil.which("yt-dlp"):
        return YT_DLP_INSTALL_HINT
    return None


def _download_video(
    url: str, folder: Path, basename: str, max_height: int, force: bool
) -> Optional[Path]:
    """Download a capped-resolution copy of the video. Returns its path or None."""
    existing = sorted(folder.glob(f"{basename}--video.*"))
    existing = [p for p in existing if not p.name.endswith(".tmp")]
    if existing and not force:
        return existing[0]
    for p in existing:
        p.unlink()

    output_template = str(folder / f"{basename}--video.%(ext)s")
    fmt = (
        f"bestvideo[height<={max_height}]/best[height<={max_height}]/best"
    )
    cmd = [
        "yt-dlp",
        "-f", fmt,
        "--output", output_template,
        url,
    ]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        stripped = cp.stderr.strip() if cp.stderr else ""
        lines = stripped.splitlines()
        msg = lines[-1] if lines else f"exit code {cp.returncode}"
        sys.stderr.write(f"yt-dlp: {msg}\n")
        return None
    produced = sorted(folder.glob(f"{basename}--video.*"))
    produced = [p for p in produced if not p.name.endswith(".tmp")]
    return produced[0] if produced else None


def _detect_freeze_segments(
    video_path: Path, noise: str, min_hold: float
) -> List[FreezeSegment]:
    """Run ffmpeg `freezedetect` and return the held (static) segments.

    Uses the `null` muxer (no image encoding) — freeze metadata is logged to
    stderr. Frames themselves are grabbed afterward, one at a time, by
    `_grab_frame_at`.
    """
    vf = f"freezedetect=n={noise}:d={min_hold},metadata=mode=print"
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-i", str(video_path),
        "-an",
        "-vf", vf,
        "-f", "null",
        "-",
    ]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        stripped = cp.stderr.strip() if cp.stderr else ""
        lines = stripped.splitlines()
        msg = lines[-1] if lines else f"exit code {cp.returncode}"
        sys.stderr.write(f"ffmpeg: {msg}\n")
        return []
    return parse_freeze_segments(cp.stderr)


def _grab_frame_at(video_path: Path, frames_dir: Path, seconds: float) -> Optional[Path]:
    """Extract a single frame at `seconds` into frames_dir. Returns its path."""
    out = frames_dir / f"frame-{int(round(seconds)):05d}s.jpg"
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-ss", str(seconds),
        "-i", str(video_path),
        "-frames:v", "1",
        "-qscale:v", "3",
        "-y",
        str(out),
    ]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0 or not out.exists():
        return None
    return out


def run(
    url: str,
    folder: str,
    basename: Optional[str],
    force: bool,
    freeze_noise: str,
    min_hold: float,
    min_gap: float,
    max_candidates: int,
    max_height: int,
    keep_video: bool,
) -> int:
    hint = _check_binaries()
    if hint:
        sys.stderr.write(hint)
        return 1

    folder_path = Path(folder).resolve()
    if not folder_path.is_dir():
        sys.stderr.write(f"folder does not exist: {folder_path}\n")
        return 1
    if basename is None:
        basename = folder_path.name

    frames_dir = folder_path / "frames"
    manifest_path = frames_dir / "manifest.json"

    if manifest_path.exists() and not force:
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            json.dump(data, sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
            return 0
        except (json.JSONDecodeError, OSError):
            pass  # regenerate

    if frames_dir.exists() and force:
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)

    video_path = _download_video(url, folder_path, basename, max_height, force)
    if video_path is None:
        sys.stderr.write("Failed to download video for frame extraction.\n")
        return 1

    segments = _detect_freeze_segments(video_path, freeze_noise, min_hold)
    times = representative_times(segments, min_hold=min_hold)
    kept = select_candidates(times, min_gap=min_gap, max_candidates=max_candidates)

    frames: List[Dict] = []
    seen_secs = set()
    for t in kept:
        secs = int(round(t))
        if secs in seen_secs:
            continue
        seen_secs.add(secs)
        out = _grab_frame_at(video_path, frames_dir, t)
        if out is None:
            continue
        frames.append({
            "file": out.name,
            "path": str(out),
            "seconds": secs,
            "timestamp": _format_timestamp(secs),
        })

    if not keep_video:
        try:
            video_path.unlink()
        except OSError:
            pass

    result = {
        "frames_dir": str(frames_dir),
        "manifest_path": str(manifest_path),
        "count": len(frames),
        "frames": frames,
    }
    manifest_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Extract held (static) on-screen-visual frames from a YouTube video."
    )
    parser.add_argument("url", help="YouTube URL or video ID")
    parser.add_argument("--folder", required=True, help="Per-video output folder (from Stage 1)")
    parser.add_argument("--basename", default=None, help="File prefix (default: folder basename)")
    parser.add_argument("--force", action="store_true", help="Re-download/re-extract even if a manifest exists")
    parser.add_argument("--freeze-noise", default="-60dB", help="freezedetect noise tolerance: dB (e.g. -60dB) or ratio 0-1. Higher/looser tolerates slight motion over otherwise-static slides (default -60dB)")
    parser.add_argument("--min-hold", type=float, default=3.0, help="Minimum seconds a frame must stay static to count as a held visual. Higher filters more talking-head micro-pauses; lower catches briefly-shown slides (default 3.0)")
    parser.add_argument("--min-gap", type=float, default=2.0, help="Minimum seconds between kept candidate frames (default 2.0)")
    parser.add_argument("--max-candidates", type=int, default=60, help="Cap on candidate frames handed to the vision layer (default 60)")
    parser.add_argument("--max-height", type=int, default=720, help="Cap video resolution for the download (default 720)")
    parser.add_argument("--keep-video", action="store_true", help="Keep the downloaded video file (default: delete after extraction)")
    args = parser.parse_args(argv[1:])
    return run(
        url=args.url,
        folder=args.folder,
        basename=args.basename,
        force=args.force,
        freeze_noise=args.freeze_noise,
        min_hold=args.min_hold,
        min_gap=args.min_gap,
        max_candidates=args.max_candidates,
        max_height=args.max_height,
        keep_video=args.keep_video,
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv))
