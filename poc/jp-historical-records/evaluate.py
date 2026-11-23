"""Apply the fixed score to every station-year and tabulate by threshold.

Recall is read per layer of JMA's mark (solid, dotted). Inspection Load is the
share of all station-years at or above the threshold: what a person would
have to look at. A station-year without a score is never counted as flagged,
and the number of such rows is shown per layer.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

import score

HERE = Path(__file__).parent
DATA = HERE / "data"
LAYERS = ("solid", "dotted", "none")


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    stations = sorted({(r["prec_no"], r["block_no"]) for r in rows})
    years = [int(r["year"]) for r in rows]
    y0, y1 = min(years), max(years)
    index = {s: i for i, s in enumerate(stations)}
    temps = np.full((len(stations), y1 - y0 + 1), np.nan)
    for r in rows:
        if r["mean_temp_c"] != "":
            temps[index[(r["prec_no"], r["block_no"])], int(r["year"]) - y0] = float(r["mean_temp_c"])
    return rows, index, y0, temps


def tabulate(marks: list[str], scores: np.ndarray, thresholds=score.THRESHOLDS) -> list[dict]:
    """One row per threshold. marks and scores are aligned per station-year."""
    marks_a = np.array(marks)
    has = np.isfinite(scores)
    out = []
    for th in thresholds:
        hit = has & (scores >= th)
        row = {"threshold": th, "n_all": len(marks), "flagged_all": int(hit.sum())}
        row["inspection_load"] = row["flagged_all"] / len(marks)
        for layer in LAYERS:
            sel = marks_a == layer
            row[f"n_{layer}"] = int(sel.sum())
            row[f"no_score_{layer}"] = int((sel & ~has).sum())
            row[f"flagged_{layer}"] = int((sel & hit).sum())
        for layer in ("solid", "dotted"):
            n = row[f"n_{layer}"]
            row[f"recall_{layer}"] = row[f"flagged_{layer}"] / n if n else float("nan")
        out.append(row)
    return out


def main() -> int:
    rows, index, y0, temps = load(DATA / "station_years.tsv")
    all_scores = score.score_all(temps)
    s = np.array([all_scores[index[(r["prec_no"], r["block_no"])], int(r["year"]) - y0] for r in rows])
    marks = [r["mark"] for r in rows]

    with (DATA / "scores.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["prec_no", "block_no", "name", "year", "mark", "score"])
        for r, v in zip(rows, s):
            w.writerow([r["prec_no"], r["block_no"], r["name"], r["year"], r["mark"], "" if not np.isfinite(v) else f"{v:.3f}"])

    table = tabulate(marks, s)
    with (DATA / "results.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(table)

    t0 = table[0]
    print(f"stations {len(index)}, station-years {t0['n_all']}")
    for layer in LAYERS:
        print(f"  {layer}: {t0[f'n_{layer}']} rows, {t0[f'no_score_{layer}']} without a score")
    print()
    print("| null level | threshold | Recall solid | Recall dotted | flagged unmarked | Inspection Load |")
    print("|---|---|---|---|---|---|")
    for lv, r in zip(score.NULL_LEVELS, table):
        print(
            f"| {lv} | {r['threshold']} "
            f"| {r['flagged_solid']}/{r['n_solid']} = {r['recall_solid']:.3f} "
            f"| {r['flagged_dotted']}/{r['n_dotted']} = {r['recall_dotted']:.3f} "
            f"| {r['flagged_none']}/{r['n_none']} "
            f"| {r['flagged_all']}/{r['n_all']} = {r['inspection_load']:.3f} |"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
