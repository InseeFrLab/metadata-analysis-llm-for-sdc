
HEADER_BASE = ["table_name", "field", "hrc_field", "indicator", "hrc_indicator"]


def _spanning_pairs(rec):
    """Extrait la liste (code, hrc) des variables de croisement d'un enregistrement."""
    return [(sv.get("code"), sv.get("hrc")) for sv in rec["spanning_variables"]]


def max_spanning(records):
    """Nombre maximal de variables de croisement parmi tous les enregistrements."""
    return max(len(_spanning_pairs(r)) for r in records)
