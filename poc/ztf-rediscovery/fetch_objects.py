"""Download the alert light curves of every object listed in a TSV file.

    uv run python fetch_objects.py data/ground_truth.tsv cache/objects
"""

import csv
import sys
from pathlib import Path

from fink import object_alerts


def main(tsv: str, cache: str) -> int:
    with open(tsv, newline="") as fh:
        ids = [row["ztf_id"] for row in csv.DictReader(fh, delimiter="\t")]
    missing = []
    for i, object_id in enumerate(ids, 1):
        rows = object_alerts(object_id, Path(cache))
        print(f"{i}/{len(ids)} {object_id} {len(rows)} alerts", flush=True)
        if not rows:
            missing.append(object_id)
    if missing:
        print(f"no alerts for: {' '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
