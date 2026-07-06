from __future__ import annotations

import json
from jsonschema import Draft202012Validator
from pathlib import Path
from extract_JSON_array import extract_array

SCHEMA_PATH = Path(__file__).parent / "schema" / "sdc_output.schema.json"


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate(records, schema=None):
    """Retourne une liste d'erreurs comapré au schema"""

    validator = Draft202012Validator(schema or load_schema())
    errors = []
    for err in sorted(validator.iter_errors(records), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"  at {loc}: {err.message}")
    return errors


def records_from_text(text):
    """extract_array + validate. Cette fonction enchaine les deux"""
    records = extract_array(text)
    errors = validate(records)
    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors))
    return records


def load_and_validate(path):
    """Lecture de fichier + records_from_text"""
    return records_from_text(Path(path).read_text(encoding="utf-8"))
