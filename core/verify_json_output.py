#!/usr/bin/env python3
"""Slice the JSON array out of an LLM reply and verify it against the contract.

Pipeline position:

    LLM reply --> [THIS MODULE] --> validated JSON array --> transform_output.py

Usage:
    python3 verify_json_output.py reply.txt                 # validate, print summary
    python3 verify_json_output.py reply.txt -o clean.json   # also write the clean array
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from jsonschema import Draft202012Validator
from pathlib import Path


# --- array extraction (stdlib only) ----------------------------------------

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


# --- schema validation ------------------------------------------------------

SCHEMA_PATH = (
    Path(__file__).parent / "schema" / "sdc_output.schema.json"
    if (Path(__file__).parent / "schema").exists()
    else Path(__file__).parent.parent / "schema" / "sdc_output.schema.json"
)


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate(records, schema=None):
    """Return a list of human-readable validation error strings ([] if valid)."""

    validator = Draft202012Validator(schema or load_schema())
    errors = []
    for err in sorted(validator.iter_errors(records), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"  at {loc}: {err.message}")
    return errors


def expected_table_ids(metadata_md: str) -> set:
    """Extract T<n> table ids from the first column of the serialized markdown."""
    return set(re.findall(r'^\|\s*(T\d+)\s*\|', metadata_md, re.MULTILINE))


def records_from_text(text):
    """Slice the JSON array out of a reply string, parse it, and schema-validate it.

    Raises ValueError on any problem (no array, malformed JSON, not a list, or a
    schema violation). This is the one entry point the offline CLI path uses.
    """
    records = extract_array(text)
    errors = validate(records)
    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors))
    return records


def load_and_validate(path):
    """Parse + validate a reply file. Raises ValueError on any problem.

    Returns the list of record dicts.
    """
    return records_from_text(Path(path).read_text(encoding="utf-8"))


# --- CLI --------------------------------------------------------------------

def main(argv=None):
    p = argparse.ArgumentParser(description="Extract + validate the LLM JSON array.")
    p.add_argument("input", help="LLM reply file (JSON array + optional reflection)")
    p.add_argument("-o", "--output", help="Write the clean JSON array to this path")
    args = p.parse_args(argv)

    text = Path(args.input).read_text(encoding="utf-8")
    try:
        records = extract_array(text)  # json.JSONDecodeError is a ValueError
    except ValueError as exc:
        print(f"FAIL: could not parse a JSON array from {args.input}\n  {exc}")
        return 1

    errors = validate(records)
    if errors:
        print(f"FAIL: {len(errors)} schema violation(s) in {args.input}:")
        print("\n".join(errors))
        return 1

    print(f"OK: {len(records)} record(s) valid against {SCHEMA_PATH.name}")
    if args.output:
        Path(args.output).write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Wrote clean array to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
