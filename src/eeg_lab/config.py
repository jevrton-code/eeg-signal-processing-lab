"""Project configuration: dataset selection and analysis constants.

Responsibility
--------------
Centralize the reproducible configuration for the version 1 analysis slice so
that subjects, runs, paths, and event-mapping conventions live in one place
rather than being scattered across notebooks.

Important convention
--------------------
Event labels T1/T2 are NOT globally fixed. Their meaning depends on the run
type (see ``docs/dataset_notes.md``). Any event mapping defined here must be
keyed by run number, never by raw event code alone.

Status
------
Version 0.2. The constants and run-aware event mapping used by the first
reproducible inspection notebook are implemented here. Heavier configuration
objects (epoch windows, band definitions) remain documented for later stages.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Version 1 analysis slice (see docs/project_brief.md and docs/dataset_notes.md).
# ---------------------------------------------------------------------------
SUBJECTS: tuple[int, ...] = (1, 2, 3)
RUNS: tuple[int, ...] = (1, 2, 4, 8, 12)

# Local directory where downloaded raw EDF files will live. This path is
# git-ignored and never committed.
RAW_DATA_DIR: str = "data/raw"

# Absolute path to the repository root (…/eeg-signal-processing-lab), derived
# from this file's location: src/eeg_lab/config.py -> repo root is two parents up.
REPO_ROOT: Path = Path(__file__).resolve().parents[2]

# Resolved absolute locations for downloaded data and exported figures.
RAW_DATA_PATH: Path = REPO_ROOT / RAW_DATA_DIR
FIGURES_DIR: Path = REPO_ROOT / "figures"

# Expected dataset facts (for confirmation against the loaded recordings).
EXPECTED_N_EEG_CHANNELS: int = 64
EXPECTED_SFREQ_HZ: float = 160.0

# ---------------------------------------------------------------------------
# Run-type classification for the v1 slice.
# ---------------------------------------------------------------------------
BASELINE_RUNS: tuple[int, ...] = (1, 2)
# Motor-imagery, left vs right hand (the v1 task runs).
MOTOR_IMAGERY_LR_HAND_RUNS: tuple[int, ...] = (4, 8, 12)

# Short human-readable role per run used in the v1 slice.
RUN_DESCRIPTIONS: dict[int, str] = {
    1: "Baseline, eyes open",
    2: "Baseline, eyes closed",
    4: "Motor imagery, left vs right hand",
    8: "Motor imagery, left vs right hand",
    12: "Motor imagery, left vs right hand",
}


def run_role(run: int) -> str:
    """Return a short human-readable role string for a run number."""
    return RUN_DESCRIPTIONS.get(run, f"Run {run} (not part of the v1 slice)")


def map_events_by_run(run: int) -> dict[str, str]:
    """Return the run-aware label mapping for the EDF annotation codes.

    The PhysioNet EEGBCI annotations use the codes ``T0``, ``T1`` and ``T2``.
    Their meaning is NOT globally fixed:

    - ``T0`` always denotes rest.
    - In left/right hand runs (4, 8, 12) ``T1`` = left fist and ``T2`` = right
      fist (imagined, since these are motor-*imagery* runs).
    - The baseline runs (1, 2) contain only ``T0`` (continuous rest), so only
      ``T0`` is mapped.

    Parameters
    ----------
    run
        The PhysioNet run number.

    Returns
    -------
    dict
        Mapping from annotation code (``"T0"``/``"T1"``/``"T2"``) to a
        descriptive, run-aware condition label.

    Raises
    ------
    ValueError
        If ``run`` is outside the version 1 slice (1, 2, 4, 8, 12). The mapping
        is intentionally limited to the runs this project actually analyzes so
        no label is silently guessed.
    """
    if run in BASELINE_RUNS:
        condition = "rest (eyes open)" if run == 1 else "rest (eyes closed)"
        return {"T0": condition}
    if run in MOTOR_IMAGERY_LR_HAND_RUNS:
        return {
            "T0": "rest",
            "T1": "left fist (imagined)",
            "T2": "right fist (imagined)",
        }
    raise ValueError(
        f"Run {run} is not part of the version 1 slice {RUNS}. "
        "Event meaning is run-dependent; refusing to guess a mapping."
    )


def get_dataset_config() -> dict:
    """Return the resolved dataset configuration for the v1 slice."""
    return {
        "subjects": SUBJECTS,
        "runs": RUNS,
        "baseline_runs": BASELINE_RUNS,
        "motor_imagery_lr_hand_runs": MOTOR_IMAGERY_LR_HAND_RUNS,
        "raw_data_dir": RAW_DATA_DIR,
        "raw_data_path": RAW_DATA_PATH,
        "figures_dir": FIGURES_DIR,
        "expected_n_eeg_channels": EXPECTED_N_EEG_CHANNELS,
        "expected_sfreq_hz": EXPECTED_SFREQ_HZ,
        "run_descriptions": dict(RUN_DESCRIPTIONS),
    }
