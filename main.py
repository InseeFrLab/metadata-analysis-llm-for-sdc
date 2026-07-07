import argparse
import csv

from src.data import read_file
from src.clean import _dataframe_to_rows, clean_sheet
from src.transform_input import wrap, to_markdown
from src.LLM_API_call import chat, is_auto_continued
from src.extract_JSON_array import extract_array
from src.validate_json_output import validate
from src.transform_output import _spanning_pairs, max_spanning, HEADER_BASE


def read_producer_answers():
    """Lit les reponses du producteur dans le terminal (ligne vide pour terminer)."""
    print("\n--- Vos reponses (terminez par une ligne vide) ---")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Preliminary SDC metadata pipeline driver.")
    p.add_argument("input", help="metadata workbook (.ods/.xlsx/.csv)")
    p.add_argument("-o", "--output", required=True, help="output CSV path")
    p.add_argument("--prompt", default="src/prompts/prompt_questions.md",
                   help="chemin du prompt systeme")
    args = p.parse_args()

    # ---- I. Read ---------------------------------------------------
    data = read_file(args.input)

    # ---- II. Clean ---------------------------------------------------
    cleaned_sheets = []
    for name, df in data.items():
        rows = _dataframe_to_rows(df)
        rows = clean_sheet(rows)
        if any(any(c for c in r) for r in rows):
            cleaned_sheets.append((name, rows))

    # ---- III. Transform to markdown ------------------------------------
    title = args.input.rsplit("/", 1)[-1]
    markdown = to_markdown(cleaned_sheets, title=title)

    # ---- IV. LLM call(s) ------------------------------------------------
    prompt = open(args.prompt, encoding="utf-8").read()
    history = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": wrap(markdown)},
    ]
    reply = chat(history)
    history.append({"role": "assistant", "content": reply})

    if not is_auto_continued(reply):
        print("\n--- Questions du modele ---\n")
        print(reply)
        answers = read_producer_answers()
        history.append({"role": "user", "content": answers})
        reply = chat(history)

    # ---- V. Verify -----------------------------------------------------
    records = extract_array(reply)
    errors = validate(records)
    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors))

    # ---- VI. Write CSV ---------------------------------------------------
    n_span = max_spanning(records)
    cols = list(HEADER_BASE)
    for i in range(1, n_span + 1):
        cols += [f"spanning_{i}", f"hrc_spanning_{i}"]

    rows = []
    for rec in records:
        row = [rec["table_name"], rec["field"], rec["hrc_field"],
               rec["indicator"], rec["hrc_indicator"]]
        pairs = _spanning_pairs(rec)
        for i in range(n_span):
            code, hrc = pairs[i] if i < len(pairs) else ("", "")
            row += [code, hrc]
        rows.append(row)

    with open(args.output, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        w.writerows(rows)

    print(f"\nEcrit {args.output} ({len(rows)} lignes x {len(cols)} colonnes)")
