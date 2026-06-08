"""Dataset loading and access helpers.

Responsibility
--------------
Provide a thin, reproducible layer over MNE-Python's EEGBCI dataset helper for
downloading and loading selected PhysioNet EEG Motor Movement/Imagery
recordings into MNE ``Raw`` objects.

Intended contents (to be implemented in a later stage):

- A function to fetch selected subject/run EDF files into the local,
  git-ignored ``data/raw/`` directory via ``mne.datasets.eegbci.load_data``.
- A function to read one or more runs into an MNE ``Raw`` object.
- Helpers to report channel count, sampling rate, duration, and run metadata.
- Robust, user-friendly error messages when files are missing.

Data handling rules:

- Never commit raw EDF files; downloads stay under ``data/raw/`` (gitignored).
- Document the dataset version (1.0.0) and access date in any output.

Status
------
Version 0.1 scaffolding. No loading logic is implemented yet.
"""

from __future__ import annotations


def fetch_runs(subjects, runs):
    """Download selected EEGBCI subject/run files into ``data/raw/``.

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError("eeg_lab.data.fetch_runs is a scaffolding stub.")


def load_raw(subject, runs):
    """Load selected runs for a subject into an MNE ``Raw`` object.

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError("eeg_lab.data.load_raw is a scaffolding stub.")
