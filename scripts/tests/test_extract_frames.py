"""Tests for the pure logic in extract_frames (no ffmpeg/yt-dlp needed)."""
from scripts.extract_frames import (
    _format_timestamp,
    parse_freeze_segments,
    representative_times,
    select_candidates,
)


class TestFormatTimestamp:
    def test_under_an_hour(self):
        assert _format_timestamp(0) == "00:00"
        assert _format_timestamp(9) == "00:09"
        assert _format_timestamp(75) == "01:15"
        assert _format_timestamp(3599) == "59:59"

    def test_over_an_hour(self):
        assert _format_timestamp(3600) == "01:00:00"
        assert _format_timestamp(3735) == "01:02:15"


class TestParseFreezeSegments:
    def test_three_slides_last_runs_to_end(self):
        # Mirrors real freezedetect output: 3 held segments, the last one has
        # no freeze_end because the clip ended while still frozen.
        stderr = (
            "lavfi.freezedetect.freeze_start=0\n"
            "lavfi.freezedetect.freeze_duration=5\n"
            "lavfi.freezedetect.freeze_end=5\n"
            "lavfi.freezedetect.freeze_start=7\n"
            "lavfi.freezedetect.freeze_duration=5\n"
            "lavfi.freezedetect.freeze_end=12\n"
            "lavfi.freezedetect.freeze_start=14\n"
        )
        assert parse_freeze_segments(stderr) == [
            (0.0, 5.0, 5.0),
            (7.0, 12.0, 5.0),
            (14.0, None, None),
        ]

    def test_no_freezes(self):
        assert parse_freeze_segments("nothing static here") == []

    def test_back_to_back_starts_without_end(self):
        # Defensive: two starts with no intervening end -> first left open.
        stderr = (
            "lavfi.freezedetect.freeze_start=1\n"
            "lavfi.freezedetect.freeze_start=9\n"
            "lavfi.freezedetect.freeze_duration=2\n"
            "lavfi.freezedetect.freeze_end=11\n"
        )
        assert parse_freeze_segments(stderr) == [
            (1.0, None, None),
            (9.0, 11.0, 2.0),
        ]


class TestRepresentativeTimes:
    def test_settle_offset_capped_at_midpoint(self):
        segs = [(0.0, 5.0, 5.0), (7.0, 12.0, 5.0)]
        # settle=1.0 <= span/2 (2.5) -> start + 1.0
        assert representative_times(segs, min_hold=2.0) == [1.0, 8.0]

    def test_short_segment_uses_midpoint(self):
        # duration 1.0 -> midpoint offset 0.5 (below the 1.0 settle default)
        segs = [(10.0, 11.0, 1.0)]
        assert representative_times(segs, min_hold=2.0) == [10.5]

    def test_open_segment_uses_min_hold(self):
        # No duration -> span defaults to min_hold; offset = min(1.0, min_hold/2)
        segs = [(20.0, None, None)]
        assert representative_times(segs, min_hold=2.0) == [21.0]


class TestSelectCandidates:
    def test_empty(self):
        assert select_candidates([], min_gap=2.0, max_candidates=10) == []

    def test_min_gap_dedup(self):
        times = [0.0, 1.0, 2.5, 3.0, 6.0]
        assert select_candidates(times, min_gap=2.0, max_candidates=100) == [0.0, 2.5, 6.0]

    def test_sorts_input(self):
        assert select_candidates([6.0, 0.0, 2.5], min_gap=2.0, max_candidates=100) == [0.0, 2.5, 6.0]

    def test_cap_keeps_first_and_last(self):
        times = [float(i) for i in range(0, 100, 10)]
        result = select_candidates(times, min_gap=0.0, max_candidates=4)
        assert len(result) == 4
        assert result[0] == 0.0
        assert result[-1] == 90.0

    def test_cap_of_one(self):
        times = [1.0, 2.0, 3.0]
        assert select_candidates(times, min_gap=0.0, max_candidates=1) == [1.0]

    def test_under_cap_returns_all_thinned(self):
        times = [0.0, 5.0, 10.0]
        assert select_candidates(times, min_gap=2.0, max_candidates=10) == [0.0, 5.0, 10.0]
