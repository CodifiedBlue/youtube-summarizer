"""Repo-root pytest configuration: ensure the repo root is on sys.path so
test files can import the `scripts.*` package."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
