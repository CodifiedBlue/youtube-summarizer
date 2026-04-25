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
