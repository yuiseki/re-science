"""Read JMA "past weather data" pages: station list and annual tables.

Source: Japan Meteorological Agency website (https://www.data.jma.go.jp/stats/etrn/),
used under the Public Data License 1.0. Values are parsed, not altered.
"""

from __future__ import annotations

import re
import time
import urllib.request
from pathlib import Path

BASE = "https://www.data.jma.go.jp/stats/etrn"
UA = "Mozilla/5.0 (research script; annual tables only; 1 request per second)"

# Position of the annual mean temperature among the data cells of a row
# (after the year cell): 2 pressure, 4 precipitation, then mean temperature.
MEAN_TEMP_CELL = 6
N_CELLS = 27

MARK_NONE, MARK_SOLID, MARK_DOTTED = "none", "solid", "dotted"
# Cell classes are data_<top>_<bottom>, e.g. data_1t_0 or data_0_2b. In the
# site's stylesheet (stats/data/css/kako.css) level 1 is a dotted red border
# and levels 2 to 4 are solid red borders. The page legend explains only
# "solid" and "dotted"; what separates levels 2, 3 and 4 is not documented
# there, so they are all read as solid.
_CLASS = re.compile(r"^data_([0-4])t?_([0-4])b?$")
_LEVEL_TO_MARK = {"0": MARK_NONE, "1": MARK_DOTTED, "2": MARK_SOLID, "3": MARK_SOLID, "4": MARK_SOLID}
_STRENGTH = {MARK_NONE: 0, MARK_DOTTED: 1, MARK_SOLID: 2}


def stronger(a: str, b: str) -> str:
    return a if _STRENGTH[a] >= _STRENGTH[b] else b

_ROW = re.compile(r'<tr class="mtx2"[^>]*>(.*?)</tr>', re.S)
_YEAR = re.compile(r"year=(\d{4})&[^>]*>\s*(\d{4})\s*</a>")
_CELL = re.compile(r'<td class="([^"]+)"[^>]*>(.*?)</td>', re.S)
_NUMBER = re.compile(r"^(-?\d+(?:\.\d+)?)\s*(\)?)$")


def parse_value(text: str) -> float | None:
    """A plain number, or one marked ')' (near-complete), is a value.

    Everything else is missing: blank, '--', '///', 'x', '#', and numbers
    marked ']' (too little data behind the statistic).
    """
    text = re.sub(r"<[^>]+>", "", text).replace("&nbsp;", " ").strip()
    m = _NUMBER.match(text)
    return float(m.group(1)) if m else None


def parse_annual(html: str) -> list[dict]:
    """Rows of {year, temp, mark} from one station's annual table.

    mark is the red line between the previous year and this one: the line on
    top of this row, or the line under the previous row, whichever is stronger.

    Raises if a row does not have the expected number of cells, so that a
    changed layout cannot silently shift the temperature column.
    """
    out = []
    below_previous = (None, MARK_NONE)  # (year, mark under that year's row)
    for body in _ROW.findall(html):
        y = _YEAR.search(body)
        if not y:
            continue
        cells = _CELL.findall(body)
        if len(cells) != N_CELLS:
            raise ValueError(f"year {y.group(2)}: {len(cells)} cells, expected {N_CELLS}")
        cls, text = cells[MEAN_TEMP_CELL]
        m = _CLASS.match(cls)
        if not m:
            raise ValueError(f"year {y.group(2)}: unknown cell class {cls}")
        year = int(y.group(2))
        mark = _LEVEL_TO_MARK[m.group(1)]
        if below_previous[0] == year - 1:
            mark = stronger(mark, below_previous[1])
        below_previous = (year, _LEVEL_TO_MARK[m.group(2)])
        out.append({"year": year, "temp": parse_value(text), "mark": mark})
    if not out:
        raise ValueError("no annual rows found")
    return out


_PREC = re.compile(r"prefecture\.php\?prec_no=(\d+)")
_POINT = re.compile(r"viewPoint\('s','(\d+)','([^']*)'")


def parse_prec_list(html: str) -> list[str]:
    return sorted(set(_PREC.findall(html)))


def parse_stations(html: str) -> list[tuple[str, str]]:
    """(block_no, name) of the staffed-type ('s') stations on a prefecture page."""
    return sorted(set(_POINT.findall(html)))


def get(url: str, cache: Path, pause: float = 1.0) -> str:
    """Fetch with an on-disk cache. An empty or error response is not cached."""
    if cache.exists() and cache.stat().st_size > 0:
        return cache.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        if r.status != 200:
            raise RuntimeError(f"{url}: HTTP {r.status}")
        text = r.read().decode("utf-8")
    if not text.strip():
        raise RuntimeError(f"{url}: empty body")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(text, encoding="utf-8")
    time.sleep(pause)
    return text


def annual_url(prec_no: str, block_no: str) -> str:
    return f"{BASE}/view/annually_s.php?prec_no={prec_no}&block_no={block_no}&year=&month=&day=&view="
