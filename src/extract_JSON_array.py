from __future__ import annotations
import json


def slice_array(text: str) -> str:
    """Extraction de la sous-chaine du premier '[' au dernier ']'
    (crochets inclus).
    """
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found in the text (no '[' ... ']').")
    return text[start: end + 1]


def extract_array(text: str) -> list:
    """Validité du format JSON"""
    return json.loads(slice_array(text))


def try_extract_array(text: str) -> list | None:
    """Si le modèle a posé des questions et que
    l'output n'est pas un JSON
    """
    try:
        return extract_array(text)
    except ValueError:
        return None
