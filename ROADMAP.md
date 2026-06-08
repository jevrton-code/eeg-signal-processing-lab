# Roadmap

This roadmap distills the milestones in `docs/03_BACKLOG.md` into a versioned
plan. The project deliberately starts with structure and documentation, then
adds reproducible analysis stage by stage, keeping scope tight.

## Current status

- **v0.1 — scaffolding / foundation: ✅ complete.**
  Repository structure, documentation, dependency manifest, citation, license,
  and roadmap.
- **v0.2 — first reproducible notebook: ✅ complete (this release).**
  `notebooks/01_eeg_signal_processing_lab.ipynb` loads subjects 1–3, runs
  1, 2, 4, 8, 12 via MNE's EEGBCI helper, confirms 64 EEG channels @ 160 Hz and
  per-run durations, maps T0/T1/T2 **by run type**, and exports first inspection
  figures to `figures/`. The `config`, `data`, `preprocessing` (montage +
  run-aware events), and `visualization` modules are now implemented for this
  stage; filtering/reference/ICA, epoching, and PSD remain stubbed/deferred.

## Versioning plan

| Version | Theme | Contents |
| --- | --- | --- |
| **v0.1** | Structure & docs | Repo skeleton, README, dataset notes, citation, license, roadmap, stubs. |
| **v0.2** | First reproducible notebook | Load selected files via MNE EEGBCI, inspect raw signals, first figures. **(current)** |
| **v0.3** | Preprocessing & events/epochs | Conservative preprocessing applied + documented, run-aware event mapping, epochs, event-count tables. |
| **v1.0** | Polished release | PSD/frequency summaries, HTML report, curated figures, finalized limitations, GitHub-ready README. |

## Milestones (from the backlog)

### M0 — Planning and scope ✅
Lock the version 1 scope (signal processing, not classification) and define the
public narrative (EEG / BCI / neurotechnology / reproducibility).

### M1 — Dataset foundation ✅ (documented in v0.1)
Document dataset facts, the version 1 subject/run subset, and the run-aware
event mapping table. See `docs/dataset_notes.md`.

### M2 — Repository setup ✅ (v0.1)
Repository skeleton, dependency plan (`pyproject.toml` / `requirements.txt`),
citation and license files. Data folders ignored; no raw data committed.

### M3 — Signal inspection ✅ (v0.2)
Load selected recordings through MNE, produce a raw signal preview, and
summarize the channel layout. Delivered in
`notebooks/01_eeg_signal_processing_lab.ipynb` with figures in `figures/`
(`raw_signal_preview.png`, `channel_layout.png`, `event_distribution.png`,
`events_timeline_subject1_run4.png`).

### M4 — Preprocessing ⏳ (v0.3)
Define and apply conservative preprocessing (montage, reference, filtering),
with rationale and before/after notes. Decide whether ICA belongs in v1 (default:
deferred).

### M5 — Events, epochs, and frequency analysis ⏳ (v0.3 → v1.0)
Extract and summarize events (T0/T1/T2 by run type), create epochs with a stated
window, and compute PSD summaries (eyes-open vs eyes-closed baseline, optional
motor-imagery comparison).

### M6 — Documentation and GitHub polish ⏳ (v1.0)
Final README, generated report, curated figures, limitations page, and final QA
(no raw data in Git, citations complete, reproducibility verified).

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
