"""Plotting helpers for EEG signal inspection and frequency summaries.

Responsibility
--------------
Produce clear, well-labeled figures that explain the data and pipeline rather
than overstate findings.

Intended contents (to be implemented in a later stage):

- Raw signal preview plots.
- Sensor montage / channel-layout plots.
- Event distribution plots.
- Example epoch plots.
- Power spectral density (PSD) plots, including eyes-open vs eyes-closed
  baseline comparisons.
- Optional topographic frequency-band summaries when montage positions are
  reliable.

Every figure should carry readable titles, axis labels, units, and legends.

Status
------
Version 0.1 scaffolding. No plotting logic is implemented yet.
"""

from __future__ import annotations


def plot_raw_preview(raw):
    """Render a representative raw EEG preview figure.

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError(
        "eeg_lab.visualization.plot_raw_preview is a scaffolding stub."
    )


def plot_psd_comparison(spectra):
    """Render a PSD comparison figure (e.g. eyes-open vs eyes-closed).

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError(
        "eeg_lab.visualization.plot_psd_comparison is a scaffolding stub."
    )
