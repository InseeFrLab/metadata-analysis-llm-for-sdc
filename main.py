from src.transform_input import serialize
from src.LLM_API_call import chat
from src.validate_json_output import records_from_text
from src.transform_output import write_csv
import argparse

SENTINEL = "Aucune question."


def wrap(markdown):
    """Delimite les metadonnees pour le prompt."""
    return f"<metadonnees>\n{markdown}\n</metadonnees>"


def is_auto_continued(reply):
    """Vrai si le modele a repondu directement en JSON (pas de questions)."""
    parts = reply.split("\n---", 1)
    after = parts[1].strip() if len(parts) == 2 else reply.strip()
    return after.startswith(SENTINEL)


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

    # Read 
     
    
    # + Preprocess (read_file + clean_sheets, chained inside serialize)
    markdown = serialize(args.input)

    # Process (Phase 1: send to LLM)
    prompt = open(args.prompt, encoding="utf-8").read()
    history = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": wrap(markdown)},
    ]
    reply = chat(history)
    history.append({"role": "assistant", "content": reply})

    if is_auto_continued(reply):
        records = records_from_text(reply)
    else:
        print("\n--- Questions du modele ---\n")
        print(reply)
        answers = read_producer_answers()
        history.append({"role": "user", "content": answers})
        reply = chat(history)

    # Verify
    records = records_from_text(reply)

    # Upload
    cols, rows = write_csv(records, args.output)
    print(f"\nEcrit {args.output} ({len(rows)} lignes x {len(cols)} colonnes)")
