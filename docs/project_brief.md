# Project Brief (Public)

A condensed, public-facing brief distilled from `docs/00_PROJECT_BRIEF.md`.

## Positioning

`eeg-signal-processing-lab` is a research-style, reproducible EEG analysis
project that demonstrates practical skill in neurodata handling, signal
processing, and scientific documentation. The signal it aims to send:

> I can work with real EEG data, understand the preprocessing pipeline, produce
> interpretable visualizations, and document limitations like a serious
> neurotechnology practitioner.

It is a foundation layer for future BCI, AI, and neurotechnology work — built to
prove that the signal is respected before any classifier is optimized.

## Research Question

How can public EEG motor movement and motor imagery data be loaded, inspected,
preprocessed, and summarized in a reproducible way using modern Python
neurodata tooling?

## Version 1 Scope

**In scope**

- Load public EEG data from the PhysioNet EEG Motor Movement/Imagery Dataset.
- Inspect raw EEG recordings from a small number of subjects.
- Map experimental runs and event labels correctly (by run type).
- Apply basic preprocessing decisions with explicit rationale.
- Create visual summaries: raw signals, channel layout, events, epochs, spectra.
- Produce a reproducible notebook / report.
- Explain limitations and next steps.

**Out of scope (deferred)**

- Deep learning.
- Real-time BCI control.
- Clinical or diagnostic interpretation; any medical claims.
- Large-scale benchmarking across all 109 subjects.
- Hardware integration.
- Classification as the main deliverable.

## Dataset Summary

- **PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0**
- Source: https://physionet.org/content/eegmmidb/1.0.0/
- DOI: https://doi.org/10.13026/C28G6P
- 64 EEG channels, 160 Hz, EDF+ format, BCI2000 acquisition context.
- License: Open Data Commons Attribution License v1.0 (ODC-By).
- Accessed via MNE-Python's EEGBCI helper; raw files are never committed.

Full facts, run table, and event mapping: [`dataset_notes.md`](dataset_notes.md).

## Chosen Version 1 Slice

- **Subjects:** 1, 2, 3
- **Runs:** 1 (eyes-open baseline), 2 (eyes-closed baseline), 4, 8, 12 (motor
  imagery, left vs right hand)

Rationale: small enough to run quickly, includes a baseline comparison, and
includes motor imagery that is directly relevant to BCI — without turning the
first release into a benchmark.

## Definition of Done (Version 1)

Version 1 is done when a reviewer can:

- Understand what dataset was used and why.
- Reproduce the analysis from the documented workflow.
- See visual evidence that EEG was loaded and processed correctly.
- Understand each preprocessing decision.
- See limitations clearly stated.
- Recognize the project as relevant to EEG, BCI, and neurotechnology.

> Note: this file reflects the v0.1 scaffolding state. The analysis described
> above is planned, not yet implemented. See `ROADMAP.md`.
