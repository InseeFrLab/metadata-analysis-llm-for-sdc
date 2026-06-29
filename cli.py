#!/usr/bin/env python3
"""Terminal driver for the preliminary SDC pipeline (and offline test harness).

One driver, two storage backends — pick the source with `--s3`:

  python cli.py meta.ods -o out/run1            Full run on LOCAL files. Needs Qwen
                                                creds in .env (LLM_MODEL / LLM_BASE_URL /
                                                OPENAI_API_KEY or CLE_API_OPENWEBUI).
  python cli.py user/data/meta.ods --s3         Full run on ONYXIA S3 (MinIO): input and
                                                output are S3 keys; creds are injected by
                                                Onyxia (AWS_S3_ENDPOINT, …). Needs s3fs.
  python cli.py meta.ods --serialize-only       Print the serialized Markdown and exit (no
                                                model). Add --s3 to read the workbook from S3.
  python cli.py --reply saved.txt -o out        Offline: a saved JSON reply -> CSV (no model).

The two offline modes (--serialize-only, --reply) need no API key, so the deterministic
half (serialize, validate, CSV) is testable on any machine — e.g. this Mac, which has no
access to the model.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from core import pipeline, verify_json_output, transform_output  # noqa: E402


# --- S3 (Onyxia / MinIO) helpers -------------------------------------------
# s3fs is imported lazily so the local path never requires it.

def _s3_filesystem():
    """Build an s3fs filesystem from the Onyxia-injected env vars."""
    import s3fs  # lazy: only the --s3 path needs it
    return s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": "https://" + os.environ["AWS_S3_ENDPOINT"]}
    )


def _download_from_s3(key: str) -> Path:
    """Download an S3 object to a temp file (suffix preserved) and return its path."""
    fs = _s3_filesystem()
    local = Path(tempfile.mkdtemp(prefix="sdc_")) / f"input{Path(key).suffix}"
    with fs.open(key, "rb") as f_in:
        local.write_bytes(f_in.read())
    return local


def _upload_to_s3(local: Path, key: str) -> None:
    """Upload a local text file to an S3 key."""
    fs = _s3_filesystem()
    with fs.open(key, "w", encoding="utf-8") as f_out:
        f_out.write(local.read_text(encoding="utf-8"))


# --- offline helpers --------------------------------------------------------

def _records_from_reply(path: Path) -> list:
    """Slice + validate a JSON array out of a saved model reply (offline path)."""
    return verify_json_output.records_from_text(path.read_text(encoding="utf-8"))


def _read_multiline() -> str:
    """Read the producer's answers from stdin until a blank line (or EOF)."""
    lines = []
    try:
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Preliminary SDC metadata pipeline driver.")
    p.add_argument(
        "input", nargs="?",
        help="metadata workbook (.ods/.xlsx/.csv); local path or S3 key with --s3")
    p.add_argument("--reply", help="offline: a saved LLM reply (JSON array) -> CSV")
    p.add_argument("-o", "--output", help="output base path (default: alongside the input)")
    p.add_argument("--serialize-only", action="store_true", help="print the Markdown and exit")
    p.add_argument("--s3", action="store_true",
                   help="read input (and write output) on Onyxia S3 instead of the local disk")
    args = p.parse_args(argv)

    # --- offline: saved reply -> CSV (no model, no key; local files only) ---
    if args.reply:
        reply_path = Path(args.reply)
        if not reply_path.exists():
            print(f"Reply not found: {reply_path}", file=sys.stderr)
            return 2
        records = _records_from_reply(reply_path)
        base = Path(args.output) if args.output else reply_path.with_suffix("")
        base.parent.mkdir(parents=True, exist_ok=True)
        cols, rows = transform_output.write_csv(records, base.with_suffix(".csv"))
        print(f"Wrote {base.with_suffix('.csv')}  ({len(rows)} rows x {len(cols)} cols)")
        return 0

    if not args.input:
        p.error("provide a metadata workbook, or --reply for the offline path")

    # --- resolve the input to a local path (download from S3 if requested) ---
    if args.s3:
        print(f"↓ Downloading {args.input} from S3 ...")
        in_path = _download_from_s3(args.input)
    else:
        in_path = Path(args.input)
        if not in_path.exists():
            print(f"Input not found: {in_path}", file=sys.stderr)
            return 2

    md = pipeline.serialize(in_path)
    if args.serialize_only:
        sys.stdout.write(md)
        return 0

    print("Phase 1 — envoi des métadonnées au modèle...")
    try:
        r = pipeline.start(md)
    except RuntimeError as exc:  # missing key, etc.
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    if r.auto_continued:
        print("Aucune question — le modèle a produit le JSON directement.")
        records = r.records
    else:
        print("\n--- Questions du modèle ---\n")
        print(r.questions)
        print("\n--- Vos réponses (terminez par une ligne vide) ---")
        answers = _read_multiline()
        records = pipeline.answer(r.history, answers)

    expected = verify_json_output.expected_table_ids(md)
    if expected:
        missing = sorted(expected - {r["table_name"] for r in records})
        if missing:
            print(f"WARNING: {len(missing)} table(s) missing from JSON: {', '.join(missing)}")

    # --- write the CSV, locally or back to S3 ---
    if args.s3:
        out_key = args.output or str(Path(args.input).with_suffix(".csv"))
        if not out_key.endswith(".csv"):
            out_key += ".csv"
        tmp_base = Path(tempfile.mkdtemp(prefix="sdc_out_")) / "output"
        cols, rows = pipeline.to_csv(records, tmp_base)
        print(f"↑ Uploading to {out_key} ...")
        _upload_to_s3(tmp_base.with_suffix(".csv"), out_key)
        print(f"\nWrote s3://{out_key}  ({len(rows)} rows x {len(cols)} cols)")
    else:
        base = Path(args.output) if args.output else in_path.with_suffix("")
        cols, rows = pipeline.to_csv(records, base)
        print(f"\nWrote {base.with_suffix('.csv')}  ({len(rows)} rows x {len(cols)} cols)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
