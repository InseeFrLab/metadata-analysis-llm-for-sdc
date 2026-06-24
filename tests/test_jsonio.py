"""jsonio: slicing/parsing the JSON array out of a larger reply blob."""

import pytest

from core import jsonio


def test_slice_array_extracts_outermost_brackets():
    assert jsonio.slice_array("notes [1, 2] trailing") == "[1, 2]"


def test_slice_array_uses_last_closing_bracket():
    # Reflection prose after the array must not truncate it.
    text = 'prose [{"a": 1}] then [not json]'
    assert jsonio.slice_array(text) == '[{"a": 1}] then [not json]'


def test_slice_array_raises_without_brackets():
    with pytest.raises(ValueError):
        jsonio.slice_array("no array here")


def test_extract_array_parses_list():
    assert jsonio.extract_array('x [{"a": 1}] y') == [{"a": 1}]


def test_extract_array_raises_on_malformed_json():
    with pytest.raises(ValueError):
        jsonio.extract_array("[not, valid, json]")


def test_try_extract_array_returns_none_when_absent():
    assert jsonio.try_extract_array("the model asked a question") is None


def test_try_extract_array_returns_none_on_malformed():
    assert jsonio.try_extract_array("[oops") is None


def test_try_extract_array_returns_list_when_present():
    assert jsonio.try_extract_array('reply: [1, 2, 3] done') == [1, 2, 3]
