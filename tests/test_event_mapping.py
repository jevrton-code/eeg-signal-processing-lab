"""Tests for run-aware event mapping.

The key correctness concern for this dataset is that T1/T2 are interpreted by
run type, not by event code alone (see docs/dataset_notes.md). These tests pin
the run-aware mapping implemented in v0.2 for the version 1 slice.
"""

import pytest

from eeg_lab import config, preprocessing


def test_t0_is_always_rest():
    # T0 denotes rest in every run of the v1 slice.
    for run in config.RUNS:
        mapping = config.map_events_by_run(run)
        assert "T0" in mapping
        assert "rest" in mapping["T0"]


def test_baseline_runs_have_only_t0():
    # Baseline runs (1, 2) are continuous rest: only T0 is mapped.
    for run in config.BASELINE_RUNS:
        mapping = config.map_events_by_run(run)
        assert set(mapping) == {"T0"}
    assert "eyes open" in config.map_events_by_run(1)["T0"]
    assert "eyes closed" in config.map_events_by_run(2)["T0"]


def test_lr_hand_runs_map_t1_left_t2_right():
    # In L/R hand motor-imagery runs (4, 8, 12): T1=left fist, T2=right fist.
    for run in config.MOTOR_IMAGERY_LR_HAND_RUNS:
        mapping = config.map_events_by_run(run)
        assert "left" in mapping["T1"]
        assert "right" in mapping["T2"]
        assert "imagined" in mapping["T1"] and "imagined" in mapping["T2"]


def test_preprocessing_reexports_same_mapping():
    # The preprocessing re-export must agree with config.
    assert preprocessing.map_events_by_run(4) == config.map_events_by_run(4)


def test_unknown_run_refuses_to_guess():
    # Runs outside the v1 slice must raise rather than guess a mapping.
    with pytest.raises(ValueError):
        config.map_events_by_run(6)
