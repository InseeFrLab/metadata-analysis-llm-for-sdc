"""json_to_table: the deterministic JSON -> flat CSV transform (NA-vs-blank)."""

from core import json_to_table as jt


def _rec(**kw):
    base = {
        "table_name": "T1",
        "field": "pop",
        "hrc_field": "NA",
        "indicator": "IND",
        "hrc_indicator": "NA",
        "spanning_variables": [{"code": "naf_code", "hrc": "hrc_naf"}],
    }
    base.update(kw)
    return base


def test_max_spanning_counts_widest_record():
    recs = [
        _rec(),
        _rec(spanning_variables=[{"code": "a", "hrc": "NA"}, {"code": "b", "hrc": "hrc_b"}])]
    assert jt.max_spanning(recs) == 2


def test_max_spanning_defaults_to_one_when_empty():
    assert jt.max_spanning([]) == 1


def test_header_grows_with_spanning_count():
    recs = [_rec(spanning_variables=[{"code": "a", "hrc": "NA"}, {"code": "b", "hrc": "hrc_b"}])]
    assert jt.header(recs) == [
        "table_name", "field", "hrc_field", "indicator", "hrc_indicator",
        "spanning_1", "hrc_spanning_1", "spanning_2", "hrc_spanning_2",
    ]


def test_indicator_coalesces_across_variants():
    assert jt._indicator({"indicator": "X"}) == "X"
    assert jt._indicator({"indicator_label": "Y"}) == "Y"
    assert jt._indicator({"indicator_code": "Z"}) == "Z"
    # Precedence: indicator > label > code.
    assert jt._indicator({"indicator": "X", "indicator_label": "Y"}) == "X"


def test_csv_rows_na_vs_blank_convention():
    recs = [
        _rec(),  # 1 spanning; second dimension should be blank-blank
        _rec(table_name="T2", indicator="IND2", hrc_indicator="hrc_x",
             spanning_variables=[{"code": "a", "hrc": "NA"}, {"code": "b", "hrc": "hrc_b"}]),
    ]
    rows = jt.csv_rows(recs)

    # Present value with no hierarchy -> hrc cell is the literal "NA".
    # Absent 2nd dimension -> BOTH cells blank.
    assert rows[0] == ["T1", "pop", "NA", "IND", "NA", "naf_code", "hrc_naf", "", ""]
    assert rows[1] == ["T2", "pop", "NA", "IND2", "hrc_x", "a", "NA", "b", "hrc_b"]


def test_write_csv_roundtrip(tmp_path):
    out = tmp_path / "out.csv"
    cols, rows = jt.write_csv([_rec()], out)
    assert cols[0] == "table_name"
    assert out.exists()
    # utf-8-sig BOM is written for spreadsheet apps.
    assert out.read_bytes().startswith(b"\xef\xbb\xbf")
