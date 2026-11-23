"""Minimal client for the Fink/ZTF REST API, with an on-disk cache.

`columns` only accepts `i:` (alert) and `d:` (Fink added-value) fields.
Asking for a `v:` field (e.g. `v:classification`) makes the server answer
500, so derived fields have to be requested by leaving `columns` out.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import requests

API = "https://api.ztf.fink-portal.org/api/v1"
COLUMNS = ",".join([
    "i:objectId", "i:candid", "i:jd", "i:fid", "i:magpsf", "i:sigmapsf", "i:isdiffpos",
    "i:ra", "i:dec", "i:distnr", "i:distpsnr1", "i:sgscore1", "i:ndethist",
    "d:cdsxmatch", "d:tns",
])
PAUSE_SECONDS = 1.0


def _post(endpoint: str, payload: dict, timeout: float = 120.0):
    r = requests.post(f"{API}/{endpoint}", json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list):
        # The API reports errors as a JSON object with a 200 status in places.
        raise RuntimeError(f"{endpoint} returned {str(data)[:200]}")
    return data


def object_alerts(object_id: str, cache_dir: Path) -> list[dict]:
    """All alerts of one object. An object unknown to Fink yields an empty list."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{object_id}.json"
    if path.exists():
        return json.loads(path.read_text())
    rows = _post("objects", {"objectId": object_id, "columns": COLUMNS})
    path.write_text(json.dumps(rows))
    time.sleep(PAUSE_SECONDS)
    return rows


def latest_alerts(fink_class: str, start: str, stop: str, n: int) -> list[dict]:
    """The last `n` alerts of a Fink class between two dates (ISO strings).

    The server walks back from `stop`, so with a small `n` everything comes
    from the last observed night of the window. A window with no observing
    night returns an empty list, not an error.
    """
    rows = _post("latests", {
        "class": fink_class, "n": n, "startdate": start, "stopdate": stop,
        "columns": "i:objectId,i:jd",
    }, timeout=300.0)
    time.sleep(PAUSE_SECONDS)
    return rows
