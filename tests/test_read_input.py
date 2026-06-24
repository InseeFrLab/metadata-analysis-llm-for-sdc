"""read_input: deterministic workbook -> Markdown serialization (CSV path)."""

from core import read_input


def test_clean_escapes_pipes_and_flattens_whitespace():
    assert read_input._clean("a|b") == "a\\|b"
    assert read_input._clean("a\nb\rc") == "a b c"
    assert read_input._clean("  x   y  ") == "x y"
    assert read_input._clean(None) == ""


def test_strip_trailing_empty():
    assert read_input._strip_trailing_empty(["a", "", "b", "", ""]) == ["a", "", "b"]


def test_serialize_csv_to_markdown(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("a,b\n1,2\n", encoding="utf-8")

    md = read_input.serialize(csv_file)

    # File name as document title, sheet (stem) as a heading, GFM table body.
    assert "# sample.csv" in md
    assert "## sample" in md
    assert "| a | b |" in md
    assert "| --- | --- |" in md
    assert "| 1 | 2 |" in md


def test_serialize_is_deterministic(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("a,b\n1,2\n", encoding="utf-8")
    assert read_input.serialize(csv_file) == read_input.serialize(csv_file)


def test_serialize_escapes_embedded_pipe(tmp_path):
    csv_file = tmp_path / "piped.csv"
    csv_file.write_text('h\n"x|y"\n', encoding="utf-8")
    assert "x\\|y" in read_input.serialize(csv_file)


def test_unsupported_extension_raises(tmp_path):
    bad = tmp_path / "data.txt"
    bad.write_text("nope", encoding="utf-8")
    try:
        read_input.read_workbook(bad)
        assert False, "expected ValueError for unsupported extension"
    except ValueError:
        pass
