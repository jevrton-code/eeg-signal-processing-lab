"""Placeholder tests for the dataset configuration.

These are intentionally minimal for v0.1 (scaffolding). They assert only the
documented version 1 analysis slice so that the scope stays pinned. Real tests
covering loading and metadata arrive once the pipeline is implemented.
"""

from eeg_lab import config


def test_version_one_subject_selection():
    # v1 slice: subjects 1, 2, 3 (see docs/project_brief.md).
    assert config.SUBJECTS == (1, 2, 3)


def test_version_one_run_selection():
    # v1 slice: baseline runs 1, 2 and motor-imagery L/R hand runs 4, 8, 12.
    assert config.RUNS == (1, 2, 4, 8, 12)


def test_raw_data_dir_is_gitignored_location():
    # Raw EDF downloads must live under the git-ignored data/raw/ directory.
    assert config.RAW_DATA_DIR == "data/raw"
