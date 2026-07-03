from clean_input import clean_input


def _table_md(rows):
    """Transormation par feuille en tableaux md"""
    width = max((len(r) for r in rows), default=0)
    if width == 0:
        return ""
    padded = [r + [""] * (width - len(r)) for r in rows]
    header = padded[0]
    body = padded[1:]
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join(["---"] * width) + " |"]
    for r in body:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def to_markdown(sheets, title=None):
    """Combiner [(sheet_name, rows), ...] en un seul bloc"""
    parts = []
    if title:
        parts.append(f"# {title}\n")
    for name, rows in sheets:
        table = _table_md(rows)
        if table:
            parts.append(f"## {name}\n\n{table}")
    return "\n\n".join(parts) + "\n"


def serialize(filepath):
    """Applique toute la phase de préparation de l'input"""
    sheets = clean_input(filepath)
    title = filepath.rsplit("/", 1)[-1]
    return to_markdown(sheets, title=title)
