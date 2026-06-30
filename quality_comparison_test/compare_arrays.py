import sys
import pandas as pd


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


def compare_arrays(arr1, arr2):
    """
    Compares two arrays by iterating each cell of arr1 against
    every cell of arr2, checking character-by-character correctness.

    Returns:
        matches (list): entries from arr1 that found a matching entry in arr2
        non_matches (list): entries from arr1 that found NO match in arr2
    """
    matches = []
    non_matches = []

    for i, cell1 in enumerate(arr1):
        cell1_str = str(cell1)
        match_found = False

        for j, cell2 in enumerate(arr2):
            cell2_str = str(cell2)

            # Character-by-character comparison
            if len(cell1_str) != len(cell2_str):
                continue

            is_match = True
            for k in range(len(cell1_str)):
                if cell1_str[k] != cell2_str[k]:
                    is_match = False
                    break

            if is_match:
                match_found = True
                matches.append({
                    "arr1_index": i,
                    "arr1_value": cell1,
                    "arr2_index": j,
                    "arr2_value": cell2,
                })
                break  # stop scanning arr2 once a match is found

        if not match_found:
            non_matches.append({
                "arr1_index": i,
                "arr1_value": cell1,
            })

    return matches, non_matches


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
    print(f"arr2 length: {len(arr2)}\n")

    matches, non_matches = compare_arrays(arr1, arr2)

    print("MATCHES:")
    print(f"  count: {len(matches)}")

    print("\nNON-MATCHES:")
    print(f"  count: {len(non_matches)}")
