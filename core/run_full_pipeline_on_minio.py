#!/usr/bin/env python3
"""
run_full_pipeline_on_minio.py — Full SDC pipeline on MinIO files.

Takes an ODS file from MinIO, serializes it, sends to Qwen (Phase 1 + Phase 2),
and writes the CSV output back to MinIO. No manual Markdown needed.

Usage:
    python run_full_pipeline_on_minio.py <input.ods in S3> <output.csv in S3>

Example:
    python run_full_pipeline_on_minio.py \
      jawadmallat/analyse_LLM_metadata/data_tables/sujets_analyse_demande_2.ods \
      jawadmallat/analyse_LLM_metadata/output/sujets_analyse_demande_2.csv

Requires:
  - core/pipeline.py (the orchestrator)
  - core/read_input.py (ODS → Markdown)
  - API Key set in .env or env vars
"""

import os
import sys
import tempfile
from pathlib import Path

import s3fs

# Add the repo root to the path so we can import the `core` package
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import pipeline, extract_json    # noqa: E402


def main(input_s3: str, output_s3: str) -> None:
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": "https://" + os.environ["AWS_S3_ENDPOINT"]}
    )

    # Unique temp dir so concurrent runs never clobber each other's files.
    # Contains only: input.<ext> (downloaded from S3) and output.csv (before upload).
    # The intermediate Markdown and JSON records stay in memory and are never written here.
    # This directory is NOT cleaned up automatically — delete it manually if needed.
    workdir = Path(tempfile.mkdtemp(prefix="sdc_pipeline_"))
    print(f"Working directory: {workdir}")

    # Download ODS from MinIO
    print(f"↓ Downloading {input_s3} ...")
    suffix = Path(input_s3).suffix
    tmp_input = workdir / f"input{suffix}"
    with fs.open(input_s3, "rb") as f_in:
        tmp_input.write_bytes(f_in.read())

    # Serialize to Markdown
    print("📋 Serializing to Markdown ...")
    md = pipeline.serialize(tmp_input)

    # Phase 1: send to LLM (ask questions if needed)
    print("🤖 Phase 1: sending to Qwen ...")
    r = pipeline.start(md)

    if r.auto_continued:
        print("✓ No questions needed — proceeding to Phase 2 JSON")
        records = r.records
    else:
        # Questions were asked — need answers from stdin
        print("\n--- Questions from the model ---\n")
        print(r.questions)
        print("\n--- Paste your answers (blank line to finish) ---\n")
        answers = _read_multiline()
        print("\n🤖 Phase 2: sending answers to Qwen ...")
        records = pipeline.answer(r.history, answers)

    expected = extract_json.expected_table_ids(md)
    if expected:
        missing = sorted(expected - {r["table_name"] for r in records})
        if missing:
            print(f"WARNING: {len(missing)} table(s) missing from JSON: {', '.join(missing)}")

    # Write CSV to MinIO
    print(f"↑ Writing to {output_s3} ...")
    tmp_output = workdir / "output"
    pipeline.to_csv(records, tmp_output)

    with open(str(tmp_output) + ".csv", "r", encoding="utf-8") as f:
        csv_content = f.read()

    with fs.open(output_s3, "w", encoding="utf-8") as f_out:
        f_out.write(csv_content)

    print(f"✓ Done: {input_s3} → {output_s3}")


def _read_multiline() -> str:
    """Read answers from stdin until blank line."""
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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
