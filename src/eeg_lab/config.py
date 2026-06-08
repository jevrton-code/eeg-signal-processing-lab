"""Project configuration: dataset selection and analysis constants.

Responsibility
--------------
Centralize the reproducible configuration for the version 1 analysis slice so
that subjects, runs, paths, and event-mapping conventions live in one place
rather than being scattered across notebooks.

Important convention
--------------------
Event labels T1/T2 are NOT globally fixed. Their meaning depends on the run
type (see the README dataset section). Any event mapping defined here must be
keyed by run number, never by raw event code alone.

Status
------
Version 0.3. In addition to the v0.2 dataset constants and run-aware event
mapping, this module now defines the conservative preprocessing parameters
(filter band, reference), the cue-locked epoch window/baseline, the canonical
annotation-code integer codes, and the frequency-band definitions used by the
preprocessing, epoching, and spectral stages. These are kept here as small,
testable constants/pure functions so notebooks call into ``eeg_lab`` rather than
re-deriving them.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Version 1 analysis slice (see README dataset and pipeline sections).
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


# ---------------------------------------------------------------------------
# Conservative preprocessing parameters (v0.3). See
# README pipeline section and generated report for the rationale behind each value.
# ---------------------------------------------------------------------------
# Gentle band-pass for general inspection / spectral work. 1 Hz high-pass
# removes slow drifts; 40 Hz low-pass keeps alpha/beta and stays below the
# 80 Hz Nyquist (160 Hz sampling). The 40 Hz low-pass also attenuates the
# 60 Hz US line frequency, which is why a notch is not applied by default.
FILTER_L_FREQ_HZ: float = 1.0
FILTER_H_FREQ_HZ: float = 40.0

# EEG reference applied for spectral/topographic summaries. Average reference is
# a documented convention (not ground truth); the original reference is kept for
# raw inspection (notebook 01).
EEG_REFERENCE: str = "average"

# Power-line frequency for the dataset's acquisition region (PhysioNet, US).
# Inspected via PSD before deciding on a notch (see decision log); not applied
# by default because the 40 Hz low-pass already removes it.
LINE_FREQ_HZ: float = 60.0

# ---------------------------------------------------------------------------
# Cue-locked epoch window (v0.3).
# ---------------------------------------------------------------------------
# Motor-imagery cues (T1/T2) annotate ~4.1 s task periods. A conservative
# cue-locked window captures a short pre-cue baseline and the task period.
EPOCH_TMIN_S: float = -0.5
EPOCH_TMAX_S: float = 4.0
# Baseline correction window: from epoch start up to the cue onset (t = 0).
EPOCH_BASELINE: tuple[float | None, float | None] = (None, 0.0)

# Canonical integer codes for the EDF annotation codes. MNE's
# ``events_from_annotations`` assigns the same ascending order when these codes
# are present, so these constants let pure logic build epoch ``event_id`` maps
# without loading data.
EVENT_CODE_TO_INT: dict[str, int] = {"T0": 1, "T1": 2, "T2": 3}

# ---------------------------------------------------------------------------
# Frequency-band definitions (Hz), within the 1-40 Hz analysis band (v0.3).
# Contiguous, non-overlapping bands using common EEG conventions.
# ---------------------------------------------------------------------------
FREQ_BANDS: dict[str, tuple[float, float]] = {
    "delta": (1.0, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
    "gamma": (30.0, 40.0),
}
# Convenience aliases for the bands most relevant to motor imagery / arousal.
ALPHA_BAND: tuple[float, float] = FREQ_BANDS["alpha"]
BETA_BAND: tuple[float, float] = FREQ_BANDS["beta"]

# PSD computation range (Hz) for spectral summaries.
PSD_FMIN_HZ: float = 1.0
PSD_FMAX_HZ: float = 40.0


def epoch_window() -> tuple[float, float]:
    """Return the cue-locked epoch window ``(tmin, tmax)`` in seconds.

    The window starts before the cue onset (``tmin < 0``) to provide a pre-cue
    baseline and extends to cover the ~4 s motor-imagery task period.
    """
    return (EPOCH_TMIN_S, EPOCH_TMAX_S)


def build_condition_event_id(run: int) -> dict[str, int]:
    """Build the run-aware ``event_id`` mapping (condition label -> int) for epochs.

    Combines the run-aware code->label mapping (:func:`map_events_by_run`) with
    the canonical code->int codes (:data:`EVENT_CODE_TO_INT`). The result maps a
    descriptive condition label to the integer event code MNE will assign, so it
    can be passed directly as ``event_id`` to :class:`mne.Epochs`.

    Pure logic (no data access), so it is unit-testable.
    """
    mapping = map_events_by_run(run)
    return {label: EVENT_CODE_TO_INT[code] for code, label in mapping.items()}


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
