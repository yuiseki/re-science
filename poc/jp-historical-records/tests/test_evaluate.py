import numpy as np

import evaluate


def test_tabulate_counts_layers_and_never_flags_missing_scores():
    marks = ["solid", "solid", "dotted", "none", "none", "none"]
    scores = np.array([9.0, np.nan, 5.0, 7.0, 1.0, np.nan])
    low, high = evaluate.tabulate(marks, scores, thresholds=(4.0, 8.0))
    assert (low["flagged_solid"], low["flagged_dotted"], low["flagged_none"]) == (1, 1, 1)
    assert low["recall_solid"] == 0.5 and low["recall_dotted"] == 1.0
    assert low["inspection_load"] == 3 / 6
    assert (low["no_score_solid"], low["no_score_none"]) == (1, 1)
    assert high["flagged_all"] == 1 and high["recall_dotted"] == 0.0


def test_tabulate_empty_layer_gives_nan_recall():
    (row,) = evaluate.tabulate(["none", "none"], np.array([1.0, 2.0]), thresholds=(1.5,))
    assert np.isnan(row["recall_solid"]) and row["inspection_load"] == 0.5
