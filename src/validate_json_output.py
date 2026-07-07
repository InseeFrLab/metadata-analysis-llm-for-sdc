from __future__ import annotations

import json
from jsonschema import Draft202012Validator
from pathlib import Path

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
