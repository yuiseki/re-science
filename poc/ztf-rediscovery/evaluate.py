"""How much would a scanner have to look at to re-find the ground truth?

    uv run python evaluate.py data/ground_truth.tsv data/background.tsv cache/objects

For every score threshold, prints the share of ground-truth objects kept
(recall) next to the share of background objects that pass the same
threshold (the inspection load).
"""

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from features import light_curve_features
from intervals import newcombe_difference
from score import CRITERIA, met, tde_likeness


# Fixed in EXPERIMENT_PLAN.md before any background object was scored.
DECISION_THRESHOLD = 5
NUCLEAR_GROUPS = {"tde", "ant", "ambiguous"}


def read_tsv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def scored(rows, cache: Path, label_key):
    out, skipped = [], []
    for row in rows:
        path = cache / f"{row['ztf_id']}.json"
        if not path.exists():
            skipped.append(row["ztf_id"])
            continue
        f = light_curve_features(json.loads(path.read_text()))
        if f is None:
            # Only negative subtractions: nothing brightened, so nothing to score.
            out.append({"id": row["ztf_id"], "label": row[label_key], "score": 0, "met": {}, "f": None})
            continue
        out.append({"id": row["ztf_id"], "label": row[label_key], "score": tde_likeness(f), "met": met(f), "f": f})
    return out, skipped


def main(truth_tsv, background_tsv, cache_dir) -> int:
    cache = Path(cache_dir)
    truth, missing_truth = scored(read_tsv(truth_tsv), cache, "group")
    background, missing_bg = scored(read_tsv(background_tsv), cache, "fink_class")
    if missing_truth:
        print(f"ground truth without a light curve: {missing_truth}", file=sys.stderr)
        return 1
    if missing_bg:
        print(f"background objects not fetched yet: {len(missing_bg)}", file=sys.stderr)

    print("## Ground truth")
    print("id\tgroup\tscore\tn_det\tduration\tg_r_peak\tg_r_slope\tdist_ps1\tsgscore\tfailed")
    for t in sorted(truth, key=lambda t: -t["score"]):
        f = t["f"]
        failed = ",".join(k for k, ok in t["met"].items() if not ok)
        print(f"{t['id']}\t{t['label']}\t{t['score']}\t{f['n_det']}\t{f['duration']:.0f}\t"
              f"{f['g_r_peak']:.2f}\t{f['g_r_slope']:.4f}\t{f['dist_ps1']:.2f}\t{f['sgscore']:.2f}\t{failed}")

    print("\n## Criteria met (share of objects)")
    print("criterion\tground_truth\tbackground")
    for name in CRITERIA:
        gt = sum(t["met"].get(name, False) for t in truth) / len(truth)
        bg = sum(b["met"].get(name, False) for b in background) / max(len(background), 1)
        print(f"{name}\t{gt:.2f}\t{bg:.2f}")

    print("\n## Recall against inspection load")
    by_class = defaultdict(list)
    for b in background:
        by_class[b["label"]].append(b["score"])
    classes = sorted(by_class)
    print("score>=\ttruth_kept\ttruth_recall\tbackground_pass\t" + "\t".join(classes))
    for threshold in range(len(CRITERIA), -1, -1):
        kept = sum(t["score"] >= threshold for t in truth)
        passing = sum(b["score"] >= threshold for b in background)
        per_class = "\t".join(
            f"{sum(s >= threshold for s in by_class[c])}/{len(by_class[c])}" for c in classes)
        print(f"{threshold}\t{kept}/{len(truth)}\t{kept / len(truth):.2f}\t"
              f"{passing}/{len(background)}\t{per_class}")

    # The decision rule of EXPERIMENT_PLAN.md: nuclear transients against each stratum.
    print(f"\n## C1: share with score >= {DECISION_THRESHOLD}, nuclear transients minus background stratum")
    nuclear = [t for t in truth if t["label"] in NUCLEAR_GROUPS]
    k1 = sum(t["score"] >= DECISION_THRESHOLD for t in nuclear)
    print("stratum\tnuclear\tbackground\tdifference\tci95_low\tci95_high\tverdict")
    for c in classes:
        k2 = sum(s >= DECISION_THRESHOLD for s in by_class[c])
        d, lo, hi = newcombe_difference(k1, len(nuclear), k2, len(by_class[c]))
        verdict = "supported" if lo > 0 else "rejected" if d <= 0 else "undecided"
        print(f"{c}\t{k1}/{len(nuclear)}\t{k2}/{len(by_class[c])}\t{d:+.3f}\t{lo:+.3f}\t{hi:+.3f}\t{verdict}")

    print("\n## Ground-truth scores by group")
    groups = defaultdict(Counter)
    for t in truth:
        groups[t["label"]][t["score"]] += 1
    for g, c in sorted(groups.items()):
        print(g, dict(sorted(c.items(), reverse=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
