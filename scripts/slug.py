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
