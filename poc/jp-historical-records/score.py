"""Relative homogeneity score for annual mean temperature.

Fixed before the JMA tables (which carry the answer marks) were downloaded.
Do not edit after looking at results; see README.md.

Where each choice comes from:

- The statistic is the standard normal homogeneity test (Alexandersson 1986)
  evaluated at one fixed split: T = n1 * mean(z1)^2 + n2 * mean(z2)^2, where z
  is the standardised difference between the candidate station and a reference.
- The window is 8 years on each side of the split. JMA's own relocation
  correction uses "8 years before and after the year of the move"
  (Ohno et al. 2011, as summarised on JMA's correction page).
- The reference is the median of the K stations whose first-difference series
  correlate best with the candidate (first differences so that a step in either
  series does not drive the choice; Peterson & Easterling 1994).
- A year's score is the larger of the split before that year and the split
  after it, because a mid-year move leaves the year itself mixed.
- Thresholds are quantiles of the same statistic on homogeneous white noise
  (the way SNHT critical values are tabulated, Khaliq & Ouarda 2007), computed
  by null_quantiles() with a fixed seed. They are not tuned on real data.
"""

from __future__ import annotations

import numpy as np

HALF = 8  # years on each side of a split
MIN_VALID_HALF = 6  # a half with fewer valid years gives no score
K_REF = 10  # reference stations per candidate
MIN_REF_IN_WINDOW = 3  # complete reference series needed inside a window
MIN_COMMON_DIFF = 30  # common first-difference years needed to rank a reference

NULL_LEVELS = (0.90, 0.95, 0.99, 0.999)
# Filled from null_quantiles(seed=20261123, n=200_000); checked by a test.
THRESHOLDS = (3.33, 4.37, 6.43, 8.73)


def split_stat(q: np.ndarray) -> float:
    """SNHT statistic of a window of length 2*HALF, split in the middle.

    NaN marks a missing year. Returns NaN when either half has fewer than
    MIN_VALID_HALF values or the window has no variance.
    """
    q = np.asarray(q, dtype=float)
    if q.shape != (2 * HALF,):
        raise ValueError(f"window must have {2 * HALF} values, got {q.shape}")
    a, b = q[:HALF], q[HALF:]
    n1, n2 = int(np.isfinite(a).sum()), int(np.isfinite(b).sum())
    if n1 < MIN_VALID_HALF or n2 < MIN_VALID_HALF:
        return float("nan")
    valid = q[np.isfinite(q)]
    sd = valid.std(ddof=1)
    if not sd > 0:
        return float("nan")
    mean = valid.mean()
    z1 = (np.nanmean(a) - mean) / sd
    z2 = (np.nanmean(b) - mean) / sd
    return float(n1 * z1**2 + n2 * z2**2)


def pick_references(temps: np.ndarray, i: int) -> list[int]:
    """Indices of up to K_REF stations best correlated with station i.

    temps is (station, year) with NaN for missing. Correlation is taken on
    first differences over the years both series have.
    """
    d = np.diff(temps, axis=1)
    ranked = []
    for j in range(temps.shape[0]):
        if j == i:
            continue
        ok = np.isfinite(d[i]) & np.isfinite(d[j])
        if ok.sum() < MIN_COMMON_DIFF:
            continue
        x, y = d[i, ok], d[j, ok]
        if x.std() == 0 or y.std() == 0:
            continue
        ranked.append((float(np.corrcoef(x, y)[0, 1]), j))
    ranked.sort(reverse=True)
    return [j for _, j in ranked[:K_REF]]


def _window_stat(temps: np.ndarray, i: int, refs: list[int], start: int) -> float:
    """Statistic for the window of 2*HALF years beginning at column start."""
    n_years = temps.shape[1]
    if start < 0 or start + 2 * HALF > n_years:
        return float("nan")
    sl = slice(start, start + 2 * HALF)
    cand = temps[i, sl]
    ref_rows = [temps[j, sl] for j in refs if np.isfinite(temps[j, sl]).all()]
    if len(ref_rows) < MIN_REF_IN_WINDOW:
        return float("nan")
    ref = np.array(ref_rows)
    ref_anom = ref - ref.mean(axis=1, keepdims=True)
    return split_stat(cand - np.median(ref_anom, axis=0))


def score_station(temps: np.ndarray, i: int) -> np.ndarray:
    """Score for every year of station i.

    The score of year index t is the larger of the split placed before t and
    the split placed after t. NaN when neither split can be evaluated.
    """
    refs = pick_references(temps, i)
    n_years = temps.shape[1]
    before = np.full(n_years + 1, np.nan)  # before[k]: split between k-1 and k
    for k in range(n_years + 1):
        before[k] = _window_stat(temps, i, refs, k - HALF)
    out = np.full(n_years, np.nan)
    for t in range(n_years):
        pair = np.array([before[t], before[t + 1]])
        if np.isfinite(pair).any():
            out[t] = np.nanmax(pair)
    return out


def score_all(temps: np.ndarray) -> np.ndarray:
    return np.array([score_station(temps, i) for i in range(temps.shape[0])])


def null_quantiles(seed: int = 20261123, n: int = 200_000) -> tuple[float, ...]:
    """Quantiles of a year's score on homogeneous white noise."""
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((n, 2 * HALF + 1))
    s = np.empty(n)
    for r in range(n):
        s[r] = max(split_stat(q[r, : 2 * HALF]), split_stat(q[r, 1:]))
    return tuple(float(x) for x in np.quantile(s, NULL_LEVELS))


def flagged(score: float, threshold: float) -> bool:
    """A missing score never counts as flagged."""
    return bool(np.isfinite(score) and score >= threshold)
