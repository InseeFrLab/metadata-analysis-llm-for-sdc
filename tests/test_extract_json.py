"""extract_json: schema validation gate (fails loud on contract violations)."""

from core import extract_json


def _valid():
    return {
        "table_name": "T1",
        "field": "entreprises_francaises",
        "hrc_field": "NA",
        "indicator": "CA",
        "hrc_indicator": "NA",
        "spanning_variables": [{"code": "naf_code", "hrc": "hrc_naf"}],
    }


def test_valid_record_passes():
    assert extract_json.validate([_valid()]) == []


def test_missing_required_key_fails():
    rec = _valid()
    del rec["spanning_variables"]
    assert extract_json.validate([rec])


def test_empty_spanning_variables_fails():
    rec = _valid()
    rec["spanning_variables"] = []  # schema requires minItems: 1
    assert extract_json.validate([rec])


def test_extra_key_fails():
    rec = _valid()
    rec["sheet_number"] = "3"  # additionalProperties: false
    assert extract_json.validate([rec])


def test_empty_string_value_fails():
    rec = _valid()
    rec["field"] = ""  # minLength: 1
    assert extract_json.validate([rec])


def test_null_value_fails():
    rec = _valid()
    rec["hrc_field"] = None  # must be the literal string "NA", never null
    assert extract_json.validate([rec])


def test_records_from_text_slices_and_validates():
    import json
    text = "notes\n[" + json.dumps(_valid()) + "]\nAucune incertitude résiduelle."
    records = extract_json.records_from_text(text)
    assert records == [_valid()]
