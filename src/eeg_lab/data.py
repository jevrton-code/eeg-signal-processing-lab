"""Dataset loading and access helpers.

Responsibility
--------------
Provide a thin, reproducible layer over MNE-Python's EEGBCI dataset helper for
downloading and loading selected PhysioNet EEG Motor Movement/Imagery
recordings into MNE ``Raw`` objects.

Data handling rules:

- Never commit raw EDF files; downloads stay under ``data/raw/`` (gitignored).
- Document the dataset version (1.0.0) and access date in any output.

Status
------
Version 0.2. Minimal, conservative loading helpers used by the first
reproducible inspection notebook are implemented here.
"""

from __future__ import annotations

from pathlib import Path

import mne
import pandas as pd
from mne.datasets import eegbci

from . import config


def _ensure_raw_dir() -> Path:
    """Create and return the local, git-ignored raw-data directory."""
    config.RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
    return config.RAW_DATA_PATH


def fetch_runs(subjects, runs, *, verbose=False) -> list[Path]:
    """Download selected EEGBCI subject/run files into ``data/raw/``.

    Wraps :func:`mne.datasets.eegbci.load_data`, forcing the download location
    to the repository's git-ignored ``data/raw/`` directory so raw EDF files
    can never be committed. Files already present are not re-downloaded.

    Parameters
    ----------
    subjects
        A single subject id (int) or an iterable of subject ids.
    runs
        A single run number (int) or an iterable of run numbers.
    verbose
        Forwarded to MNE.

    Returns
    -------
    list of pathlib.Path
        Absolute paths to the downloaded EDF files.
    """
    if isinstance(subjects, int):
        subjects = [subjects]
    raw_dir = _ensure_raw_dir()
    paths: list[Path] = []
    for subject in subjects:
        files = eegbci.load_data(
            subjects=subject,
            runs=list(runs),
            path=str(raw_dir),
            update_path=False,
            verbose=verbose,
        )
        paths.extend(Path(f) for f in files)
    return paths


def load_raw(subject, runs, *, preload=True, verbose=False) -> mne.io.BaseRaw:
    """Load and concatenate selected runs for one subject into an MNE ``Raw``.

    The EDF files are downloaded on demand (if missing) into ``data/raw/`` and
    read with :func:`mne.io.read_raw_edf`. Channel names are normalized with
    :func:`mne.datasets.eegbci.standardize` (this fixes the EEGBCI naming
    quirks such as trailing dots, e.g. ``"Fcz."`` -> ``"FCz"``). Runs are
    concatenated in the requested order; an ``original_run`` annotation prefix
    is *not* added here so downstream code can still rely on the raw T0/T1/T2
    codes and map them per run.

    Parameters
    ----------
    subject
        Subject id.
    runs
        A single run number or an iterable of run numbers (concatenated).
    preload
        Whether to load data into memory (required for filtering/plotting).
    verbose
        Forwarded to MNE.

    Returns
    -------
    mne.io.BaseRaw
        The concatenated raw recording with standardized channel names.
    """
    if isinstance(runs, int):
        runs = [runs]
    files = fetch_runs(subject, runs, verbose=verbose)
    raws = [
        mne.io.read_raw_edf(f, preload=preload, verbose=verbose) for f in files
    ]
    raw = mne.concatenate_raws(raws, verbose=verbose) if len(raws) > 1 else raws[0]
    # Normalize EEGBCI channel names in place (trailing dots, casing).
    eegbci.standardize(raw)
    return raw


def load_run(subject, run, *, preload=True, verbose=False) -> mne.io.BaseRaw:
    """Load a single run for a subject (convenience wrapper around ``load_raw``)."""
    return load_raw(subject, run, preload=preload, verbose=verbose)


def describe_raw(raw: mne.io.BaseRaw) -> dict:
    """Return a small dict of descriptive metadata for a raw recording.

    Includes channel count, EEG channel count, sampling rate, duration, and the
    number of annotations. Purely descriptive; no signal-quality judgement.
    """
    n_eeg = len(mne.pick_types(raw.info, eeg=True, meg=False))
    return {
        "n_channels": raw.info["nchan"],
        "n_eeg_channels": n_eeg,
        "sfreq_hz": float(raw.info["sfreq"]),
        "n_samples": raw.n_times,
        "duration_s": float(raw.times[-1]) if raw.n_times else 0.0,
        "n_annotations": len(raw.annotations),
        "highpass_hz": float(raw.info["highpass"]),
        "lowpass_hz": float(raw.info["lowpass"]),
    }


def build_metadata_table(subject_runs, *, verbose=False) -> pd.DataFrame:
    """Build a per-run metadata summary table for the given (subject, run) pairs.

    Parameters
    ----------
    subject_runs
        Iterable of ``(subject, run)`` tuples.
    verbose
        Forwarded to MNE.

    Returns
    -------
    pandas.DataFrame
        One row per (subject, run) with channel count, sampling rate, duration,
        annotation count, and the run role.
    """
    rows = []
    for subject, run in subject_runs:
        raw = load_run(subject, run, preload=False, verbose=verbose)
        meta = describe_raw(raw)
        rows.append(
            {
                "subject": subject,
                "run": run,
                "role": config.run_role(run),
                "n_channels": meta["n_channels"],
                "n_eeg_channels": meta["n_eeg_channels"],
                "sfreq_hz": meta["sfreq_hz"],
                "duration_s": round(meta["duration_s"], 2),
                "n_annotations": meta["n_annotations"],
            }
        )
    return pd.DataFrame(rows)
