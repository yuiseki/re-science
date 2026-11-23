"""Draw background objects: what a human scanner would have had to look through.

    uv run python sample_background.py data/background.tsv

For each of a fixed set of random weeks, and each Fink class the ground-truth
objects fall into, take the last alerts of that week and pick a few objects
at random. The sample is stratified: every class and every week contributes
the same number of objects, so it does not reproduce the real mixture of
classes in the alert stream. Read the results per class.
"""

import datetime as dt
import random
import sys

from fink import latest_alerts

SEED = 20261123
# The classes Fink assigns to the alerts of the 23 ground-truth objects, plus
# the supernova candidates that dominate any search for rising transients.
CLASSES = ["Unknown", "SN candidate", "(SIMBAD) Galaxy", "(SIMBAD) QSO", "(SIMBAD) Seyfert_1"]
# Fink's public ZTF archive starts here; the paper searched up to mid 2025.
FIRST, LAST = dt.date(2019, 11, 1), dt.date(2025, 6, 30)
WEEKS = 30
PER_CLASS_AND_WEEK = 4
ALERTS_PER_QUERY = 3000


def main(out: str) -> int:
    rng = random.Random(SEED)
    span = (LAST - FIRST).days - 7
    starts = sorted(FIRST + dt.timedelta(days=rng.randrange(span)) for _ in range(WEEKS))
    seen = set()
    with open(out, "w") as fh:
        fh.write("ztf_id\tfink_class\tweek_start\n")
        for start in starts:
            stop = start + dt.timedelta(days=7)
            for fink_class in CLASSES:
                rows = latest_alerts(fink_class, start.isoformat(), stop.isoformat(), ALERTS_PER_QUERY)
                ids = sorted({r["i:objectId"] for r in rows} - seen)
                picked = rng.sample(ids, min(PER_CLASS_AND_WEEK, len(ids)))
                seen.update(picked)
                for object_id in picked:
                    fh.write(f"{object_id}\t{fink_class}\t{start.isoformat()}\n")
                fh.flush()
                print(f"{start} {fink_class}: {len(rows)} alerts, {len(ids)} objects, picked {len(picked)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
