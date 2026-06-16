#!/usr/bin/env python3
"""
table_to_md.py — Workbook (ODS / XLSX / CSV / MD) → Markdown.

Thin compatibility wrapper. This used to carry its own pandas-based serializer
with a "text row vs table row" heuristic, which produced **different** Markdown
than core/read_input.py — the serializer the real pipeline (pipeline.serialize)
actually feeds to the model. That divergence meant the MinIO *preview* did not
match the pipeline *input*, defeating the point of previewing.

To keep one canonical serialization, `convert()` now delegates to
`read_input.serialize()` for .ods/.xlsx/.csv. The public `convert(path) -> str`
name and the `__main__` CLI are kept so existing imports (e.g. run_on_minio.py,
Onyxia notebooks doing `from table_to_md import convert`) keep working — they
just now get the same Markdown the model sees.

  * .ods / .xlsx / .csv  -> read_input.serialize() (stdlib for .ods/.csv; openpyxl for .xlsx)
  * .md                  -> returned verbatim (passthrough)
  * .xls (legacy binary) -> unsupported; re-save as .xlsx
"""

import sys
from pathlib import Path

try:  # works whether imported as a module or run as `python3 core/table_to_md.py`
    from core import read_input
except ImportError:  # pragma: no cover - direct-execution fallback
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core import read_input


def convert(input_path) -> str:
    """Serialize a workbook to Markdown, identically to the production pipeline."""
    path = Path(input_path)
    suffix = path.suffix.lower()

    if suffix == ".md":
        return path.read_text(encoding="utf-8")
    if suffix == ".xls":
        raise ValueError(
            "Legacy .xls is not supported; re-save as .xlsx (or .ods/.csv) first."
        )
    # .ods / .xlsx / .csv — the canonical serializer used by pipeline.serialize.
    return read_input.serialize(path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python table_to_md.py <input_file> [output.md]")

    src = Path(sys.argv[1])
    if not src.exists():
        sys.exit(f"File not found: {src}")

    dst = Path(sys.argv[2]) if len(sys.argv) >= 3 else src.with_suffix(".md")
    dst.write_text(convert(src), encoding="utf-8")
    print(f"→ {dst}")
