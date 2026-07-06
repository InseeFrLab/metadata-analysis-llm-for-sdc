import csv

HEADER_BASE = ["table_name", "field", "hrc_field", "indicator", "hrc_indicator"]


def _spanning_pairs(rec):
    return [(sv.get("code"), sv.get("hrc")) for sv in rec["spanning_variables"]]


def max_spanning(records):
    return max(len(_spanning_pairs(r)) for r in records)


def header(records):
    cols = list(HEADER_BASE)
    for i in range(1, max_spanning(records) + 1):
        cols += [f"spanning_{i}", f"hrc_spanning_{i}"]
    return cols


def csv_rows(records):
    n_span = max_spanning(records)
    rows = []
    for rec in records:
        row = [rec["table_name"], rec["field"], rec["hrc_field"],
               rec["indicator"], rec["hrc_indicator"]]
        pairs = _spanning_pairs(rec)
        for i in range(n_span):
            if i < len(pairs):
                code, hrc = pairs[i]
            else:
                code, hrc = "", ""
            row += [code, hrc]
        rows.append(row)
    return rows


def write_csv(records, path):
    cols = header(records)
    rows = csv_rows(records)
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        w.writerows(rows)
    return cols, rows
