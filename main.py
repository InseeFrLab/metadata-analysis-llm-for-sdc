from src.data import read_file, upload_output
import argparse


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Preliminary SDC metadata pipeline driver.")
    p.add_argument("input", nargs="?", help="metadata workbook (.ods/.xlsx/.csv)")
    p.add_argument("--reply", help="offline: a saved LLM reply (JSON array) -> CSV")
    p.add_argument("-o", "--output", help="output base path (default: alongside the input)")
    p.add_argument("--serialize-only", action="store_true", help="print the Markdown and exit")
    args = p.parse_args()

    # Read
    sheets = read_file(p.input)
    df = sheets

    # Preprocess

    # Process

    # Verify

    # Upload
    upload_output(df, p.output)
