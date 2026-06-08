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
Version 0.2. For this first inspection notebook only the montage assignment and
the run-aware event mapping are implemented (both are needed to display channel
layouts and event distributions correctly). Filtering, referencing, bad-channel
handling and ICA remain deferred to v0.3 — see
``docs/preprocessing_decisions.md`` — and the corresponding pipeline entry point
stays an explicit stub below.
"""

from __future__ import annotations

import mne

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


def apply_basic_preprocessing(raw):
    """Apply the conservative montage/reference/filter defaults to ``raw``.

    Deferred to v0.3. The first inspection notebook deliberately works on the
    *raw* signal (plus montage assignment) and does not filter, re-reference or
    remove artifacts; see ``docs/preprocessing_decisions.md`` for the planned,
    documented defaults.
    """
    raise NotImplementedError(
        "eeg_lab.preprocessing.apply_basic_preprocessing is deferred to v0.3 "
        "(conservative filtering/reference). v0.2 inspects the raw signal only."
    )
