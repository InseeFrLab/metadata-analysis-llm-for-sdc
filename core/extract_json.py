#!/usr/bin/env python3
"""Slice the JSON array out of an LLM reply and validate it against the contract.

Pipeline position:

    LLM reply --> [THIS SCRIPT] --> validated JSON array --> json_to_table.py

The model is told to print the JSON array first (starting `[`, ending `]`) and
then a short plain-text note on residual uncertainty (per prompt_questions.md).
This script slices to the outermost array, parses it, and validates it against
schema/sdc_output.schema.json. It FAILS LOUD: any malformed output (missing
keys, wrong types, the token "NA" where null is required, unexpected keys) is
reported and the script exits non-zero, so a bad LLM reply never reaches the
deterministic transform.

Usage:
    python3 extract_json.py reply.txt                 # validate, print summary
    python3 extract_json.py reply.txt -o clean.json   # also write the clean array
"""

import argparse
import re
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

try:  # works whether run as a module or as `python3 core/extract_json.py`
    from core import jsonio
except ImportError:  # pragma: no cover - direct-execution fallback
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core import jsonio

# Re-exported for back-compat: callers that imported extract_json.slice_array
# keep working; the implementation now lives in core/jsonio.py.
slice_array = jsonio.slice_array

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
    records = jsonio.extract_array(text)
    errors = validate(records)
    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors))
    return records


def load_and_validate(path):
    """Parse + validate a reply file. Raises ValueError on any problem.

    Returns the list of record dicts.
    """
    return records_from_text(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    p = argparse.ArgumentParser(description="Extract + validate the LLM JSON array.")
    p.add_argument("input", help="LLM reply file (JSON array + optional reflection)")
    p.add_argument("-o", "--output", help="Write the clean JSON array to this path")
    args = p.parse_args(argv)

    text = Path(args.input).read_text(encoding="utf-8")
    try:
        records = jsonio.extract_array(text)  # json.JSONDecodeError is a ValueError
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
