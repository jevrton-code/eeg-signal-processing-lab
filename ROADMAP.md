# Roadmap

This roadmap tracks the versioned release plan. The project deliberately starts
with structure and documentation, then adds reproducible analysis stage by stage,
keeping scope tight.

## Current status

- **v0.1 — scaffolding / foundation: ✅ complete.**
  Repository structure, documentation, dependency manifest, citation, license,
  and roadmap.
- **v0.2 — first reproducible notebook: ✅ complete.**
  `notebooks/01_eeg_signal_processing_lab.ipynb` loads subjects 1–3, runs
  1, 2, 4, 8, 12 via MNE's EEGBCI helper, confirms 64 EEG channels @ 160 Hz and
  per-run durations, maps T0/T1/T2 **by run type**, and exports first inspection
  figures to `figures/`.
- **v0.3 — preprocessing & events/epochs/PSD: ✅ complete.**
  `notebooks/02_preprocessing_epochs_psd.ipynb` applies the conservative
  pipeline (standard_1005 montage, 1–40 Hz band-pass, average reference; notch
  inspected but deferred; ICA deferred), builds cue-locked epochs
  (−0.5 to +4.0 s) from the run-aware mapping with event-count tables, and
  computes the eyes-open vs eyes-closed PSD baseline (the expected occipital
  alpha increase is reproduced) plus optional band topomaps. `preprocessing` and
  a new `spectral` module are implemented and unit-tested.
- **v1.0 — polished release: ✅ complete (this release).**
  `eeg_lab.report` assembles a self-contained HTML report from the committed
  figures (regenerated locally — see `reports/README.md`). README, limitations,
  and report text are finalized; the full test suite is green and both notebooks run
  end-to-end. Classification / deep learning remain intentionally deferred.

## Versioning plan

| Version | Theme | Contents |
| --- | --- | --- |
| **v0.1** | Structure & documentation | Repo skeleton, README, dataset notes, citation, license, roadmap, stubs. |
| **v0.2** | First reproducible notebook | Load selected files via MNE EEGBCI, inspect raw signals, first figures. |
| **v0.3** | Preprocessing & events/epochs | Conservative preprocessing applied + documented, run-aware event mapping, epochs, event-count tables, PSD baseline. |
| **v1.0** | Polished release | PSD/frequency summaries, HTML report, curated figures, finalized limitations, GitHub-ready README. **(current)** |

## Milestones (from the backlog)

### M0 — Planning and scope ✅
Lock the version 1 scope (signal processing, not classification) and define the
public narrative (EEG / BCI / neurotechnology / reproducibility).

### M1 — Dataset foundation ✅ (documented in v0.1)
Document dataset facts, the version 1 subject/run subset, and the run-aware
event mapping table in the README and configuration.

### M2 — Repository setup ✅ (v0.1)
Repository skeleton, dependency plan (`pyproject.toml` / `requirements.txt`),
citation and license files. Data folders ignored; no raw data committed.

### M3 — Signal inspection ✅ (v0.2)
Load selected recordings through MNE, produce a raw signal preview, and
summarize the channel layout. Delivered in
`notebooks/01_eeg_signal_processing_lab.ipynb` with figures in `figures/`
(`raw_signal_preview.png`, `channel_layout.png`, `event_distribution.png`,
`events_timeline_subject1_run4.png`).

### M4 — Preprocessing ✅ (v0.3)
Applied conservative preprocessing (standard_1005 montage, 1–40 Hz band-pass,
average reference) with rationale and a before/after PSD figure. ICA deferred
with written rationale; notch inspected and deferred (covered by the 40 Hz
low-pass). Rationale is summarized in the README pipeline and generated report.

### M5 — Events, epochs, and frequency analysis ✅ (v0.3)
Run-aware event extraction with per-condition count tables, cue-locked epochs
(−0.5 to +4.0 s, baseline `(None, 0)`), and PSD summaries: eyes-open vs
eyes-closed baseline (expected occipital alpha increase reproduced) plus optional
alpha/beta topomaps. Delivered in `notebooks/02_preprocessing_epochs_psd.ipynb`
with figures in `figures/`.

### M6 — Documentation and GitHub polish ✅ (v1.0)
Final README, generated HTML report (`eeg_lab.report`; regenerated locally per
`reports/README.md`), curated figures, finalized limitations page, and final QA
(no raw data in Git, citations complete, reproducibility verified, tests green).

## Deferred / future work (explicitly out of scope for v1)

These are intentionally not part of the version 1 line:

- Motor-imagery **classifier** (left vs right hand, etc.).
- **Cross-subject benchmark** across the full 109-subject dataset.
- **Deep learning** baselines (e.g. Braindecode / EEGNet).
- **Real-time** biosignal dashboard / BCI control.
- **BrainFlow** and hardware integration.
- Streamlit / Next.js visual explorer.

Deferring these keeps version 1 honest: the signal is understood and documented
before any model is built on top of it.
