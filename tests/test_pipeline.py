"""pipeline: Phase-1 routing (questions vs. auto-continued JSON) and reply splitting.

These are pure functions over the model's reply string — no network, no key.
"""

import json

from core import pipeline

_VALID_JSON = json.dumps([{
    "table_name": "T1",
    "field": "pop",
    "hrc_field": "NA",
    "indicator": "IND",
    "hrc_indicator": "NA",
    "spanning_variables": [{"code": "c", "hrc": "NA"}],
}])


def test_split_phase1_on_separator():
    notes, after = pipeline._split_phase1("my notes\n---\nthe rest")
    assert notes == "my notes"
    assert after == "the rest"


def test_split_phase1_without_separator():
    notes, after = pipeline._split_phase1("no separator here")
    assert notes == "no separator here"
    assert after is None


def test_questions_text_returns_after_separator():
    reply = "notes\n---\n1. Question une ?\n2. Question deux ?"
    assert pipeline._questions_text(reply) == "1. Question une ?\n2. Question deux ?"


def test_records_if_valid_auto_continue():
    reply = f"work notes\n---\nAucune question.\n{_VALID_JSON}\nAucune incertitude résiduelle."
    records = pipeline._records_if_valid(reply)
    assert records is not None
    assert records[0]["table_name"] == "T1"


def test_records_if_valid_fallback_without_separator():
    # Model skipped '---' but began with the sentinel: still auto-continue.
    reply = f"Aucune question.\n{_VALID_JSON}"
    assert pipeline._records_if_valid(reply) is not None


def test_records_if_valid_returns_none_for_questions():
    reply = "notes\n---\n1. Une question ?"
    assert pipeline._records_if_valid(reply) is None


def test_records_if_valid_requires_sentinel_before_json():
    # A JSON draft inside notes (no sentinel) must NOT be mistaken for the final output.
    reply = f"draft thoughts {_VALID_JSON}\n---\n1. Une vraie question ?"
    assert pipeline._records_if_valid(reply) is None


def test_records_if_valid_rejects_schema_invalid_json():
    bad = json.dumps([{"table_name": "T1"}])  # missing required keys
    reply = f"notes\n---\nAucune question.\n{bad}"
    assert pipeline._records_if_valid(reply) is None


def test_wrap_delimits_metadata():
    wrapped = pipeline.wrap("# data")
    assert wrapped.startswith("<metadonnees>")
    assert wrapped.endswith("</metadonnees>")
    assert "# data" in wrapped
