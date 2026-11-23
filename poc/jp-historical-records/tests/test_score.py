import numpy as np
import pytest

import score


def test_split_stat_perfect_step_reaches_the_maximum():
    q = np.array([0.0] * 8 + [1.0] * 8)
    assert score.split_stat(q) == pytest.approx(15.0)


def test_split_stat_is_zero_when_halves_have_equal_means():
    q = np.array([0.0, 1.0] * 8)
    assert score.split_stat(q) == pytest.approx(0.0)


def test_split_stat_missing_half_gives_nan_not_a_pass():
    q = np.array([np.nan] * 3 + [0.0] * 5 + [1.0] * 8)
    assert np.isnan(score.split_stat(q))
    assert not score.flagged(score.split_stat(q), 0.0)


def test_split_stat_constant_window_gives_nan():
    assert np.isnan(score.split_stat(np.ones(16)))


def test_split_stat_rejects_wrong_length():
    with pytest.raises(ValueError):
        score.split_stat(np.zeros(10))


def _network(n_st=14, n_yr=80, seed=0):
    rng = np.random.default_rng(seed)
    common = rng.standard_normal(n_yr) * 0.6 + np.linspace(0, 1.5, n_yr)
    base = rng.uniform(5, 20, n_st)[:, None]
    return base + common[None, :] + rng.standard_normal((n_st, n_yr)) * 0.15


def test_step_in_one_station_scores_highest_at_the_step_year():
    temps = _network()
    temps[3, 40:] += 0.8
    s = score.score_station(temps, 3)
    assert np.nanargmax(s) in (39, 40)
    assert s[40] > score.THRESHOLDS[-1]


def test_common_climate_signal_is_not_flagged():
    temps = _network(seed=1)
    temps[:, 40:] += 1.0  # every station warms at once: not an inhomogeneity
    s = score.score_all(temps)
    share = np.mean(s[np.isfinite(s)] >= score.THRESHOLDS[2])
    assert share < 0.05


def test_edges_without_a_full_window_have_no_score():
    temps = _network()
    s = score.score_station(temps, 0)
    assert np.isnan(s[: score.HALF - 1]).all()
    assert np.isnan(s[-(score.HALF - 1):]).all()
    assert np.isfinite(s[score.HALF])


def test_gap_in_candidate_removes_scores_around_it():
    temps = _network()
    temps[2, 30:36] = np.nan
    s = score.score_station(temps, 2)
    assert np.isnan(s[32])


def test_too_few_references_gives_no_score():
    temps = _network(n_st=3)
    assert np.isnan(score.score_station(temps, 0)).all()


def test_thresholds_match_the_null_simulation():
    got = score.null_quantiles(n=20_000)
    assert got == pytest.approx(score.THRESHOLDS, abs=0.25)
    assert list(score.THRESHOLDS) == sorted(score.THRESHOLDS)
