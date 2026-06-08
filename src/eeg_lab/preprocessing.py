"""Conservative preprocessing and event/epoch handling.

Responsibility
--------------
Hold the small, documented preprocessing steps applied before any analysis,
plus the run-aware event mapping used to build epochs.

Intended contents (to be implemented in a later stage):

- Montage assignment (standard 10-05 / 10-20 mapping for EEGBCI channels).
- Reference selection (conservative default documented in
  ``docs/preprocessing_decisions.md``).
- Band-pass and optional notch filtering with explicit parameters.
- Bad-channel inspection helpers (no aggressive automated cleaning).
- A run-aware event mapper that interprets T0/T1/T2 by run type.
- Epoch construction with a stated time window.

Critical convention
--------------------
T0 always denotes rest. T1/T2 depend on the run:

- Left/right hand runs (e.g. 4, 8, 12): T1 = left fist, T2 = right fist.
- Hands/feet runs (e.g. 6, 10, 14): T1 = both fists, T2 = both feet.

Mapping must therefore be keyed on run number, not event code alone.

Status
------
Version 0.1 scaffolding. No preprocessing logic is implemented yet.
"""

from __future__ import annotations


def map_events_by_run(run):
    """Return the label mapping for a given run number.

    Encodes the run-aware meaning of T0/T1/T2. Planned (not yet implemented
    in v0.1).
    """
    raise NotImplementedError(
        "eeg_lab.preprocessing.map_events_by_run is a scaffolding stub."
    )


def apply_basic_preprocessing(raw):
    """Apply the conservative montage/reference/filter defaults to ``raw``.

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError(
        "eeg_lab.preprocessing.apply_basic_preprocessing is a scaffolding stub."
    )
