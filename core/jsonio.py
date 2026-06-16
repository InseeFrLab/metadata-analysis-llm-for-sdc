#!/usr/bin/env python3
"""Slice the JSON array out of an LLM reply — the one place that logic lives.

The model is told to print the JSON array first (`[` … `]`) and then a plain-text
reflection. Several stages need to recover that array from a larger text blob:

    cli.py            offline --reply path
    pipeline.py       Phase-1 routing (questions vs. auto-continued JSON)
    extract_json.py   slice + schema-validate
    json_to_table.py  JSON -> CSV/RDS transform

Previously each carried its own copy of `text.find("[") … rfind("]")`. This module
is the single source of truth. It is intentionally **dependency-free** (stdlib only)
so the deterministic CSV path can import it without pulling in `jsonschema`.
"""

from __future__ import annotations

import json


def slice_array(text: str) -> str:
    """Return the substring from the first '[' to the last ']' (inclusive).

    Raises ValueError if no bracketed region is present.
    """
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found in the text (no '[' ... ']').")
    return text[start: end + 1]


def extract_array(text: str) -> list:
    """Slice + parse the outermost array. Raises if absent, malformed, or not a list."""
    records = json.loads(slice_array(text))
    if not isinstance(records, list):
        raise ValueError(f"Expected a JSON array, got {type(records).__name__}.")
    return records


def try_extract_array(text: str) -> list | None:
    """Non-raising variant: return the parsed list, or None if there isn't a clean one.

    Used for Phase-1 classification, where "no valid array" is an expected outcome
    (it means the model asked questions rather than auto-continuing to the JSON).
    """
    try:
        return extract_array(text)
    except (ValueError, json.JSONDecodeError):
        return None
