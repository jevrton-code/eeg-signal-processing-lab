"""eeg_lab: reproducible EEG signal-processing toolkit (scaffolding).

This package will provide small, testable building blocks for loading,
inspecting, preprocessing, visualizing, and reporting on public EEG motor
movement/imagery data using MNE-Python.

Status
------
Version 0.2 implements the loading, montage, run-aware event mapping, and
inspection-figure helpers used by the first reproducible notebook. Preprocessing
(filtering/reference/ICA), epoching, and PSD/report generation remain deferred
to later stages; see ``ROADMAP.md``.

This project is an educational, exploratory signal-processing lab. It is not a
clinical or diagnostic tool and makes no medical claims.
"""

from . import config, data, preprocessing, visualization

__version__ = "0.2.0"

__all__ = [
    "__version__",
    "config",
    "data",
    "preprocessing",
    "visualization",
]
