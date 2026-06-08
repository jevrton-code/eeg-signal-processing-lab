"""Tests for the v0.3 epoching and event-count pure logic.

These cover the testable, data-free building blocks used to construct epochs and
event-count tables: the epoch window, the run-aware ``event_id`` construction,
and the per-condition counting. An optional integration test exercises the real
epoching path but is skipped when the dataset is not present locally.
"""

from pathlib import Path

import pytest

from eeg_lab import config, preprocessing


# ---------------------------------------------------------------------------
# Epoch-window math.
# ---------------------------------------------------------------------------
def test_epoch_window_is_ordered_and_cue_locked():
    tmin, tmax = config.epoch_window()
    assert tmin < tmax  # a window must have positive length
    assert tmin <= 0.0  # includes a pre-cue baseline
    assert tmax > 0.0  # extends past the cue onset into the task period


def test_epoch_window_matches_constants():
    assert config.epoch_window() == (config.EPOCH_TMIN_S, config.EPOCH_TMAX_S)


def test_epoch_baseline_within_window():
    tmin, tmax = config.epoch_window()
    lo, hi = config.EPOCH_BASELINE
    # baseline is (None -> tmin, 0.0): must lie inside the epoch window.
    lo_val = tmin if lo is None else lo
    hi_val = tmax if hi is None else hi
    assert tmin <= lo_val <= hi_val <= tmax


# ---------------------------------------------------------------------------
# Run-aware event_id construction.
# ---------------------------------------------------------------------------
def test_event_id_lr_hand_run_has_three_named_conditions():
    event_id = config.build_condition_event_id(4)
    assert set(event_id) == {"rest", "left fist (imagined)", "right fist (imagined)"}
    # Codes follow the canonical T0=1, T1=2, T2=3 ordering MNE also assigns.
    assert event_id["rest"] == config.EVENT_CODE_TO_INT["T0"]
    assert event_id["left fist (imagined)"] == config.EVENT_CODE_TO_INT["T1"]
    assert event_id["right fist (imagined)"] == config.EVENT_CODE_TO_INT["T2"]


def test_event_id_baseline_run_has_only_rest():
    event_id = config.build_condition_event_id(1)
    assert list(event_id) == ["rest (eyes open)"]
    assert event_id["rest (eyes open)"] == config.EVENT_CODE_TO_INT["T0"]


def test_event_id_unknown_run_refuses_to_guess():
    with pytest.raises(ValueError):
        config.build_condition_event_id(6)


def test_event_id_values_are_unique():
    # Distinct conditions must map to distinct integer codes (for valid epochs).
    for run in config.MOTOR_IMAGERY_LR_HAND_RUNS:
        values = list(config.build_condition_event_id(run).values())
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# Count-table logic.
# ---------------------------------------------------------------------------
def test_count_events_by_condition_basic():
    descriptions = ["T0", "T1", "T1", "T2", "T0", "T0"]
    counts = preprocessing.count_events_by_condition(descriptions, run=4)
    assert counts["rest"] == 3
    assert counts["left fist (imagined)"] == 2
    assert counts["right fist (imagined)"] == 1


def test_count_events_includes_zero_conditions():
    # A condition valid for the run but absent in the data is reported as 0.
    counts = preprocessing.count_events_by_condition(["T0", "T0"], run=8)
    assert counts["left fist (imagined)"] == 0
    assert counts["right fist (imagined)"] == 0
    assert counts["rest"] == 2


def test_count_events_ignores_codes_not_valid_for_run():
    # Baseline runs only have T0; a stray T1 is not a real condition there.
    counts = preprocessing.count_events_by_condition(["T0", "T1", "T0"], run=2)
    assert set(counts) == {"rest (eyes closed)"}
    assert counts["rest (eyes closed)"] == 2


def test_event_count_dataframe_shape_and_columns():
    records = [
        {"subject": 1, "run": 4, "descriptions": ["T0", "T1", "T2", "T1"]},
        {"subject": 1, "run": 1, "descriptions": ["T0"]},
    ]
    df = preprocessing.event_count_dataframe(records)
    assert list(df.columns) == ["subject", "run", "role", "condition", "count"]
    # run 4 -> 3 conditions, run 1 -> 1 condition => 4 rows.
    assert len(df) == 4
    run4 = df[df["run"] == 4].set_index("condition")["count"].to_dict()
    assert run4["left fist (imagined)"] == 2
    assert run4["right fist (imagined)"] == 1
    assert run4["rest"] == 1


# ---------------------------------------------------------------------------
# Optional integration test (skipped without local data / network).
# ---------------------------------------------------------------------------
_EDF = (
    config.RAW_DATA_PATH
    / "MNE-eegbci-data/files/eegmmidb/1.0.0/S001/S001R04.edf"
)


@pytest.mark.skipif(not Path(_EDF).exists(), reason="EEGBCI data not present locally")
def test_make_epochs_integration():
    from eeg_lab import data

    raw = data.load_raw(1, [4])
    preprocessing.apply_basic_preprocessing(raw)
    epochs = preprocessing.make_epochs(raw, run=4)
    # The L/R-hand run defines three named conditions; epochs should be non-empty.
    assert set(epochs.event_id) <= {
        "rest",
        "left fist (imagined)",
        "right fist (imagined)",
    }
    assert len(epochs) > 0
    tmin, tmax = config.epoch_window()
    assert epochs.tmin == pytest.approx(tmin)
    assert epochs.tmax == pytest.approx(tmax)
