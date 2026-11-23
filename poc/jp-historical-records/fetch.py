"""Download every staffed station's annual table and write the two TSVs.

  data/station_years.tsv  every (station, year) with an annual mean temperature
                          value or a mark: the full population, nothing sampled
  data/ground_truth.tsv   the rows JMA marks with a red line in the mean
                          temperature column

Any station that cannot be fetched or parsed stops the run.
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

import jma

HERE = Path(__file__).parent
CACHE = HERE / "cache"
DATA = HERE / "data"


def main() -> int:
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    precs = jma.parse_prec_list(jma.get(f"{jma.BASE}/select/prefecture00.php", CACHE / "select" / "prefecture00.html"))
    if not precs:
        print("no prefectures found", file=sys.stderr)
        return 1
    stations = []
    for p in precs:
        html = jma.get(f"{jma.BASE}/select/prefecture.php?prec_no={p}", CACHE / "select" / f"prec_{p}.html")
        stations += [(p, b, name) for b, name in jma.parse_stations(html)]
    print(f"{len(precs)} prefectures, {len(stations)} staffed stations", flush=True)

    rows = []
    for n, (p, b, name) in enumerate(stations, 1):
        html = jma.get(jma.annual_url(p, b), CACHE / "annual" / f"{p}_{b}.html")
        for r in jma.parse_annual(html):
            if r["temp"] is None and r["mark"] == jma.MARK_NONE:
                continue
            rows.append((p, b, name, r["year"], "" if r["temp"] is None else f"{r['temp']:.1f}", r["mark"]))
        if n % 20 == 0:
            print(f"{n}/{len(stations)}", flush=True)

    rows.sort(key=lambda r: (r[0], r[1], r[3]))
    DATA.mkdir(exist_ok=True)
    header = ["prec_no", "block_no", "name", "year", "mean_temp_c", "mark"]
    for path, keep in (
        (DATA / "station_years.tsv", rows),
        (DATA / "ground_truth.tsv", [r for r in rows if r[5] != jma.MARK_NONE]),
    ):
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(header)
            w.writerows(keep)
    (CACHE / "fetch_times.txt").write_text(
        f"started {started}\nfinished {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n"
    )
    print(f"{len(rows)} station-years, {sum(r[5] != jma.MARK_NONE for r in rows)} marked", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
