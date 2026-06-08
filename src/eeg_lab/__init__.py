"""eeg_lab: reproducible EEG signal-processing toolkit (scaffolding).

This package will provide small, testable building blocks for loading,
inspecting, preprocessing, visualizing, and reporting on public EEG motor
movement/imagery data using MNE-Python.

Status
------
Version 0.3 adds the conservative preprocessing pipeline (montage, 1-40 Hz
band-pass, average reference) and cue-locked epoching from the run-aware event
mapping on top of the v0.2 loading, montage, event-mapping, and inspection
helpers. ICA stays deferred. Spectral (PSD / band power) helpers and the HTML
report are added in the subsequent v0.3/v1.0 stages.

This project is an educational, exploratory signal-processing lab. It is not a
clinical or diagnostic tool and makes no medical claims.
"""

from . import config, data, preprocessing, visualization

__version__ = "0.3.0"

__all__ = [
    "__version__",
    "config",
    "data",
    "preprocessing",
    "visualization",
]
