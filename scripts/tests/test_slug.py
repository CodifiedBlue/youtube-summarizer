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
