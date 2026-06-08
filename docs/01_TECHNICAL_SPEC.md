# eeg-signal-processing-lab - Technical Spec

## Principle

This document describes the future implementation without writing source code. It is designed so an AI coding agent can create the repository with minimal ambiguity.

The first implementation should be small, reproducible, and easy to review.

## Planned Repository Structure

Recommended future repository layout:

```text
eeg-signal-processing-lab/
  README.md
  LICENSE
  CITATION.md
  pyproject.toml
  .gitignore
  docs/
    project_brief.md
    dataset_notes.md
    preprocessing_decisions.md
    limitations.md
  notebooks/
    01_eeg_signal_processing_lab.ipynb
  reports/
    eeg_signal_processing_report.html
  figures/
    raw_signal_preview.png
    channel_layout.png
    event_distribution.png
    psd_baseline_comparison.png
    epoch_examples.png
  src/
    eeg_lab/
      __init__.py
      config.py
      data.py
      preprocessing.py
      visualization.py
      report.py
  tests/
    test_dataset_config.py
    test_event_mapping.py
```

Notes:

- This planning package contains no source code.
- The future repo may use scripts/modules once implementation begins.
- Raw EEG files must not be committed.
- Generated reports and selected figures may be committed if file sizes are reasonable.

## Dataset Policy

Use PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0.

Primary access path:

- Use MNE-Python's EEGBCI dataset helper to download selected files locally.

Data handling rules:

- Do not commit raw EDF files.
- Store data in a local ignored folder such as `data/raw/`.
- Document dataset version and access date.
- Cite the dataset and PhysioNet.
- Preserve event meaning by run type.

## Initial Subject and Run Selection

Recommended version 1 selection:

- Subjects: 1, 2, and 3.
- Baseline runs: 1 and 2.
- Motor imagery left/right hand runs: 4, 8, and 12.

Reasoning:

- Small enough to run quickly.
- Includes baseline comparisons.
- Includes motor imagery, which is directly relevant to BCI.
- Avoids the complexity of a full benchmark.

## Pipeline

### Stage 1 - Environment and Project Setup

Goal:

- Create a reproducible Python project and document dependencies.

Expected deliverables:

- Dependency file.
- README setup section.
- Ignored data folders.
- Basic project layout.

Acceptance criteria:

- A new user can create the environment from documentation.
- No raw data is committed.
- The project explains where downloaded data will be stored.

### Stage 2 - Dataset Loading

Goal:

- Load selected PhysioNet EEGBCI files through MNE-Python.

Expected deliverables:

- Dataset configuration.
- Subject and run selection.
- Event/run mapping table.
- Confirmation of channels, sampling rate, and file format.

Acceptance criteria:

- The report states which subjects and runs were used.
- Event codes are interpreted according to run type.
- Baseline runs are not mixed with motor imagery task runs.

### Stage 3 - Raw EEG Inspection

Goal:

- Show that the project understands the raw signal before preprocessing.

Expected deliverables:

- Raw EEG preview.
- Channel list and channel type summary.
- Sampling rate confirmation.
- Recording duration summary.
- Basic signal quality observations.

Acceptance criteria:

- A reader can see representative raw EEG traces.
- The report identifies suspicious channels or unusual signal behavior if present.
- Observations are descriptive, not clinical.

### Stage 4 - Montage, Reference, and Preprocessing Decisions

Goal:

- Apply conservative preprocessing and document why.

Expected decisions to document:

- Electrode montage selection.
- EEG reference choice.
- Filtering range.
- Notch filter decision if line noise is inspected.
- Bad channel handling.
- Whether ICA is included or deferred.

Recommended version 1 posture:

- Keep preprocessing conservative.
- Prefer transparent plots over aggressive automated cleaning.
- Defer ICA unless the implementation can justify and visualize components clearly.

Acceptance criteria:

- Every preprocessing step has a short rationale.
- The report shows before/after evidence for meaningful steps.
- The project avoids pretending preprocessing is universally correct.

### Stage 5 - Events and Epochs

Goal:

- Convert event annotations into meaningful task labels and create epochs.

Expected deliverables:

- Event count table by subject, run, and label.
- Event mapping explanation.
- Example epochs for selected channels.
- Clear epoch timing window.

Acceptance criteria:

- T0, T1, and T2 are mapped with run context.
- Rest and task onsets are not confused.
- Epochs are visually inspected.

### Stage 6 - Frequency Analysis

Goal:

- Summarize spectral content using PSD and frequency-band views.

Expected deliverables:

- PSD plot for baseline eyes-open vs eyes-closed.
- PSD plot for selected motor imagery runs.
- Optional alpha and beta band summaries.
- Optional topographic maps if montage setup is reliable.

Acceptance criteria:

- Frequency ranges are stated.
- Plots have units and readable labels.
- Conclusions are cautious and tied to the selected sample.

### Stage 7 - Report and Documentation

Goal:

- Package the work in a GitHub-friendly and research-friendly form.

Expected deliverables:

- README.
- Notebook.
- HTML report or equivalent.
- Figures.
- Limitations page.
- References.

Acceptance criteria:

- A reviewer can skim the README and understand the project.
- A technical reviewer can inspect the notebook/report.
- The project avoids medical or overstated claims.

## Suggested Analysis Questions

Good version 1 questions:

- What does raw EEG look like before preprocessing?
- How do eyes-open and eyes-closed baseline recordings differ spectrally?
- What event labels exist in selected motor imagery runs?
- How does spectral content vary across selected conditions?
- What preprocessing decisions are necessary before any BCI classifier?

Questions to defer:

- Can we classify left vs right motor imagery accurately?
- Which model performs best?
- Can this be used for real-time control?
- Can we infer cognitive or clinical states?

## Quality Risks

Common failure modes:

- Treating event labels as globally fixed when T1 and T2 depend on run type.
- Overclaiming from a tiny subject sample.
- Building an ML model before validating signal handling.
- Committing raw data.
- Producing attractive plots without explaining preprocessing.
- Using ICA as a black box.
- Confusing educational analysis with clinical interpretation.

## Versioning Plan

Version 0.1:

- Repo structure, README, dataset notes, and one reproducible notebook.

Version 0.2:

- HTML report and figures.

Version 0.3:

- Improved preprocessing documentation and baseline comparisons.

Version 1.0:

- Stable, reproducible signal-processing lab with clear limitations and polished GitHub presentation.
