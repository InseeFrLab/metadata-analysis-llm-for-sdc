import pandas as pd


def extract_sheet(df):
    """
    Retourne (meta_text: str, table: DataFrame)
    """
    def clean_cell(v):
        if v is None:
            return ""
        s = str(v).replace("\xa0", " ").replace("\r", " ").replace("\n", " ")
        return " ".join(s.split())

    def is_real_header(row_values):
        """Une ligne est un vrai header si elle a plus de la moitié de ses cellules remplies."""
        non_empty = [v for v in row_values if v and v != "nan"]
        return len(non_empty) > len(row_values) // 2

    def is_unnamed(col):
        return str(col).startswith("Unnamed:") or str(col) == "nan"

    meta_lines = []

    # Cas 1 : le titre est déjà dans df.columns (pandas l'a pris comme header)
    real_cols = [c for c in df.columns if not is_unnamed(c)]
    if len(real_cols) == 1:
        # La première colonne non-Unnamed est le titre → c'est du meta
        meta_lines.append(clean_cell(real_cols[0]))

        # Cherche le vrai header dans les lignes
        for i, row in df.iterrows():
            values = [clean_cell(v) for v in row]
            if is_real_header(values):
                df = df.iloc[i+1:].reset_index(drop=True)
                df.columns = [v if v else f"col_{j}" for j, v in enumerate(values)]
                break
            else:
                non_empty = [v for v in values if v and v != "nan"]
                if non_empty:
                    meta_lines.append(" ".join(non_empty))

    # Cas 2 : toutes les colonnes sont Unnamed
    elif all(is_unnamed(c) for c in df.columns):
        for i, row in df.iterrows():
            values = [clean_cell(v) for v in row]
            if is_real_header(values):
                df = df.iloc[i+1:].reset_index(drop=True)
                df.columns = [v if v else f"col_{j}" for j, v in enumerate(values)]
                break
            else:
                non_empty = [v for v in values if v and v != "nan"]
                if non_empty:
                    meta_lines.append(" ".join(non_empty))

    # Nettoyage
    df = df.fillna("").astype(str).replace("nan", "")
    df = df[df.apply(lambda r: any(v.strip() for v in r), axis=1)].reset_index(drop=True)

    return "\n".join(meta_lines), df


def to_markdown(sheets, title=None):
    parts = []
    if title:
        parts.append(f"# {title}\n")

    items = sheets.items() if isinstance(sheets, dict) else sheets

    for name, data in items:
        if not isinstance(data, pd.DataFrame):
            header, *body = data
            data = pd.DataFrame(body, columns=header)

        meta_lines, df = extract_sheet(data)
        if df.empty:
            continue

        section = f"## {name}\n"
        if meta_lines:
            section += "\n" + "\n".join(meta_lines) + "\n"
        section += "\n" + df.to_markdown(index=False)
        parts.append(section)

    return "\n\n".join(parts) + "\n"
