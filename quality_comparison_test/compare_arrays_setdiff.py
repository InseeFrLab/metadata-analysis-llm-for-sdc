import sys
import numpy as np
import pandas as pd

# python compare_arrays_setdiff.py ex5_comparaison_indicateurs_LLMvsCorr.ods


def load_arrays_from_ods(filepath, sheet_name=0):
    """
    Loads two arrays from the first two columns (A and B) of an .ods file.
    Assumes row 1 is a header row; values are read from row 2 onward.
    Empty cells are dropped from each column independently.
    """
    df = pd.read_excel(filepath, engine="odf", sheet_name=sheet_name)

    if df.shape[1] < 2:
        raise ValueError(f"Expected at least 2 columns in '{filepath}', found {df.shape[1]}")

    col_a = df.iloc[:, 0].dropna().tolist()
    col_b = df.iloc[:, 1].dropna().tolist()

    return col_a, col_b


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(f"Loading arrays from '{filepath}' (columns A and B)...\n")
        arr1, arr2 = load_arrays_from_ods(filepath)
    else:
        print("No file provided, running with example arrays...\n")
        arr1 = ["cat", "dog", "bird", "fish"]
        arr2 = ["dog", "fish", "cow", "cat"]

    print(f"arr1 length: {len(arr1)}")
    print(f"arr2 length: {len(arr2)}")

    non_matches = np.setdiff1d(np.array(arr1, dtype=str), np.array(arr2, dtype=str))

    print(f"non-matches count: {len(non_matches)}")
    print(non_matches)
