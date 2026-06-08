"""Reproducible report assembly.

Responsibility
--------------
Collect figures, tables, and interpretation into a single, shareable artifact
(e.g. an ``mne.Report`` HTML file) for quality control and GitHub presentation.

Intended contents (to be implemented in a later stage):

- A builder that assembles raw previews, montage, events, epochs, and PSD
  summaries into one HTML report.
- Cautious, descriptive interpretation text (no clinical or diagnostic claims).
- A consistent place to record the subjects, runs, and dataset version used.

Status
------
Version 0.1 scaffolding. No report-generation logic is implemented yet.
"""

from __future__ import annotations


def build_report(output_path):
    """Assemble the reproducible HTML analysis report.

    Planned (not yet implemented in v0.1).
    """
    raise NotImplementedError(
        "eeg_lab.report.build_report is a scaffolding stub."
    )
