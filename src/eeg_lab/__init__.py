"""eeg_lab: reproducible EEG signal-processing toolkit (scaffolding).

This package will provide small, testable building blocks for loading,
inspecting, preprocessing, visualizing, and reporting on public EEG motor
movement/imagery data using MNE-Python.

Status
------
Version 1.0 provides the full reproducible lab: v0.2 loading/inspection, the
v0.3 conservative preprocessing pipeline (montage, 1-40 Hz band-pass, average
reference), cue-locked epoching from the run-aware event mapping, spectral
helpers (PSD / band power), and a self-contained HTML report assembled in
:mod:`eeg_lab.report`. ICA and any classifier remain intentionally deferred.

This project is an educational, exploratory signal-processing lab. It is not a
clinical or diagnostic tool and makes no medical claims.
"""

from . import config, data, preprocessing, report, spectral, visualization

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "config",
    "data",
    "preprocessing",
    "report",
    "spectral",
    "visualization",
]
