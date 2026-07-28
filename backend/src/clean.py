import pandas as pd
from typing import List


def _clean(text: object) -> str:
    """Nettoyage par cellule pour avoir un str propre (pas d'espace,...)"""
    if text is None:
        return ""
    s = str(text).replace("\xa0", " ")
    s = s.replace("\r", " ").replace("\n", " ")
    s = s.replace("|", "\\|")
    return " ".join(s.split())


def _strip_trailing_empty(seq: List[str]) -> List[str]:
    """Retire les '' en fin de liste."""
    out = list(seq)
    while out and out[-1] == "":
        out.pop()
    return out


def _dataframe_to_rows(df: pd.DataFrame) -> List[List[str]]:
    """DataFrame -> lignes str, en-tête inclus en ligne 0."""
    df = df.fillna("")
    header = ["" if str(c).startswith("Unnamed:") else str(c) for c in df.columns]
    body = [[str(v) for v in row] for row in df.itertuples(index=False)]
    return [header] + body


def clean_sheet(rows: List[List[str]]) -> List[List[str]]:
    """Nettoie les cellules et retire les cellules/lignes vides en fin de feuille."""
    rows = [_strip_trailing_empty([_clean(cell) for cell in r]) for r in rows]
    while rows and not rows[-1]:
        rows.pop()
    return rows
