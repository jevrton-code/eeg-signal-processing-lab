"""Conservative preprocessing and event/epoch handling.

Responsibility
--------------
Hold the small, documented preprocessing steps applied before any analysis,
plus the run-aware event mapping used to build epochs.

Critical convention
--------------------
T0 always denotes rest. T1/T2 depend on the run:

- Left/right hand runs (e.g. 4, 8, 12): T1 = left fist, T2 = right fist.
- Hands/feet runs (e.g. 6, 10, 14): T1 = both fists, T2 = both feet.

Mapping must therefore be keyed on run number, not event code alone.

Status
------
Version 0.3. The conservative preprocessing pipeline is now implemented:
standard montage, a gentle 1-40 Hz band-pass, and an explicit average reference
(see the README pipeline section and generated report for parameters and rationale). ICA
remains deliberately deferred. This module also builds cue-locked epochs from
the run-aware event mapping and provides pure helpers for the event-count
tables. Bad-channel handling stays manual/flagged (not automated) by design.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import mne
import pandas as pd

from . import config

# The standard montage used for EEGBCI once channel names are normalized via
# ``mne.datasets.eegbci.standardize``. The 10-05 ("standard_1005") montage
# covers the 64-channel EEGBCI layout.
STANDARD_MONTAGE: str = "standard_1005"


def map_events_by_run(run: int) -> dict[str, str]:
    """Return the run-aware label mapping for the annotation codes.

    Thin re-export of :func:`eeg_lab.config.map_events_by_run` so callers can
    reach the mapping through the preprocessing module (where epoching will
    eventually live) as well as through config.
    """
    return config.map_events_by_run(run)


def apply_montage(raw: mne.io.BaseRaw, montage: str = STANDARD_MONTAGE) -> mne.io.BaseRaw:
    """Assign a standard 10-05/10-20 montage to a raw recording, in place.

    Assumes channel names have already been normalized with
    :func:`mne.datasets.eegbci.standardize` (done in :func:`eeg_lab.data.load_raw`).
    Sensor positions are required for channel-layout and topographic plots.

    Parameters
    ----------
    raw
        Raw recording with EEGBCI-standardized channel names.
    montage
        Name of a built-in MNE montage. Defaults to ``"standard_1005"``.

    Returns
    -------
    mne.io.BaseRaw
        The same object, with the montage set.
    """
    raw.set_montage(mne.channels.make_standard_montage(montage), on_missing="warn")
    return raw


def apply_basic_preprocessing(
    raw: mne.io.BaseRaw,
    *,
    l_freq: float = config.FILTER_L_FREQ_HZ,
    h_freq: float = config.FILTER_H_FREQ_HZ,
    reference: str | None = config.EEG_REFERENCE,
    montage: str = STANDARD_MONTAGE,
    notch_freqs=None,
    verbose: bool = False,
) -> mne.io.BaseRaw:
    """Apply the conservative montage / band-pass / reference pipeline, in place.

    The steps, in order, are deliberately simple and transparent (see
    the README pipeline section and generated report for the full rationale):

    1. **Montage** (``standard_1005``) so electrodes have known positions.
    2. **Band-pass filter** (default 1-40 Hz, FIR). Removes slow drifts and
       high-frequency noise while preserving alpha/beta. The 40 Hz low-pass also
       attenuates 60 Hz line noise, so a notch is not applied by default.
    3. **Notch filter** — only if ``notch_freqs`` is explicitly supplied (the
       default is ``None``: inspect the PSD first, apply only with evidence).
    4. **EEG reference** (default average reference, applied as a projector-free
       re-reference). A documented convention, not ground truth.

    ICA is intentionally *not* performed here (deferred — see the decision log).

    Parameters
    ----------
    raw
        A preloaded raw recording with EEGBCI-standardized channel names.
    l_freq, h_freq
        Band-pass edges in Hz. Pass ``None`` to skip that edge.
    reference
        EEG reference to set (e.g. ``"average"``). Pass ``None`` to leave the
        original reference untouched.
    montage
        Built-in MNE montage name.
    notch_freqs
        Frequencies (Hz) for an optional notch filter. ``None`` skips it.
    verbose
        Forwarded to MNE.

    Returns
    -------
    mne.io.BaseRaw
        The same object, preprocessed in place.
    """
    if not raw.preload:
        raw.load_data(verbose=verbose)
    apply_montage(raw, montage)
    if l_freq is not None or h_freq is not None:
        raw.filter(l_freq=l_freq, h_freq=h_freq, picks="eeg", verbose=verbose)
    if notch_freqs is not None:
        raw.notch_filter(freqs=notch_freqs, picks="eeg", verbose=verbose)
    if reference is not None:
        raw.set_eeg_reference(reference, projection=False, verbose=verbose)
    return raw


def make_epochs(
    raw: mne.io.BaseRaw,
    run: int,
    *,
    tmin: float | None = None,
    tmax: float | None = None,
    baseline=config.EPOCH_BASELINE,
    picks: str = "eeg",
    preload: bool = True,
    verbose: bool = False,
) -> mne.Epochs:
    """Build cue-locked epochs for one run using the run-aware event mapping.

    Events are read from the EDF annotations with
    :func:`mne.events_from_annotations`. The resulting ``event_id`` is relabeled
    to the run-aware condition names (``T1`` -> ``"left fist (imagined)"`` in
    L/R-hand runs, etc.) so each epoch condition is self-describing. Only codes
    actually present in the recording are kept.

    The epoch window defaults to :func:`eeg_lab.config.epoch_window` (a short
    pre-cue baseline plus the ~4 s task period) with baseline correction over
    :data:`eeg_lab.config.EPOCH_BASELINE`.

    Parameters
    ----------
    raw
        A (preferably preprocessed) raw recording.
    run
        PhysioNet run number; drives the run-aware label mapping.
    tmin, tmax
        Epoch window in seconds. Defaults to the configured window.
    baseline
        Baseline-correction window passed to :class:`mne.Epochs`.
    picks
        Channel selection (default EEG only).
    preload, verbose
        Forwarded to MNE.

    Returns
    -------
    mne.Epochs
        Epochs with run-aware, named conditions.
    """
    if tmin is None or tmax is None:
        win = config.epoch_window()
        tmin = win[0] if tmin is None else tmin
        tmax = win[1] if tmax is None else tmax

    mapping = config.map_events_by_run(run)
    events, code_to_int = mne.events_from_annotations(raw, verbose=verbose)
    # Relabel to run-aware condition names, keeping only codes that are present.
    event_id = {
        mapping[code]: code_to_int[code]
        for code in mapping
        if code in code_to_int
    }
    return mne.Epochs(
        raw,
        events,
        event_id=event_id,
        tmin=tmin,
        tmax=tmax,
        baseline=baseline,
        picks=picks,
        preload=preload,
        verbose=verbose,
    )


def count_events_by_condition(descriptions: Iterable[str], run: int) -> dict[str, int]:
    """Count annotation codes per run-aware condition (pure logic, no data access).

    Parameters
    ----------
    descriptions
        Iterable of raw annotation codes (e.g. ``"T0"``, ``"T1"``, ``"T2"``).
    run
        Run number, used to resolve the run-aware mapping.

    Returns
    -------
    dict
        Mapping from condition label to count. Every condition valid for the run
        is present (with a zero count if it never occurs). Codes not valid for
        the run are ignored (they are mapping errors, not real conditions).
    """
    mapping = config.map_events_by_run(run)
    counts = {label: 0 for label in mapping.values()}
    for desc in descriptions:
        label = mapping.get(desc)
        if label is not None:
            counts[label] += 1
    return counts


def event_count_dataframe(
    records: Sequence[dict],
) -> pd.DataFrame:
    """Build a tidy per-(subject, run, condition) event-count table (pure logic).

    Parameters
    ----------
    records
        Sequence of dicts, each with keys ``"subject"``, ``"run"`` and
        ``"descriptions"`` (an iterable of raw annotation codes for that
        recording). No MNE/data access is performed, so this is unit-testable.

    Returns
    -------
    pandas.DataFrame
        Columns: ``subject``, ``run``, ``role``, ``condition``, ``count``.
        One row per (subject, run, condition) with a non-zero-or-zero count.
    """
    rows = []
    for rec in records:
        subject = rec["subject"]
        run = rec["run"]
        counts = count_events_by_condition(rec["descriptions"], run)
        for condition, count in counts.items():
            rows.append(
                {
                    "subject": subject,
                    "run": run,
                    "role": config.run_role(run),
                    "condition": condition,
                    "count": count,
                }
            )
    return pd.DataFrame(rows, columns=["subject", "run", "role", "condition", "count"])
