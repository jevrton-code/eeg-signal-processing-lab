# eeg-signal-processing-lab - Backlog

## Milestone M0 - Planning and Scope

### EEG-001 - Lock version 1 scope

Priority: P0

Goal:

- Keep version 1 focused on EEG signal processing and visualization.

Acceptance criteria:

- README states that classification and deep learning are future work.
- Scope includes loading, preprocessing, events, epochs, PSD, and report.
- Scope excludes clinical claims and real-time control.

### EEG-002 - Define public narrative

Priority: P0

Goal:

- Make the project useful for GitHub repositioning toward BCI and neurotechnology.

Acceptance criteria:

- README opening paragraph mentions EEG, BCI, signal processing, and reproducibility.
- The project does not read like a generic Python notebook.

## Milestone M1 - Dataset Foundation

### EEG-101 - Document dataset facts

Priority: P0

Goal:

- Write accurate notes about the PhysioNet EEG Motor Movement/Imagery Dataset.

Acceptance criteria:

- Dataset name, version, DOI, source URL, license, channel count, sampling rate, file format, and run structure are documented.
- PhysioNet and original dataset are cited.

### EEG-102 - Define subject and run subset

Priority: P0

Goal:

- Select a small version 1 subset.

Acceptance criteria:

- Subjects and runs are listed.
- Rationale for small subset is included.
- Baseline and motor imagery runs are separated.

### EEG-103 - Create event mapping table

Priority: P0

Goal:

- Prevent incorrect interpretation of T0, T1, and T2 labels.

Acceptance criteria:

- Event mapping explains that T1 and T2 depend on run type.
- Left/right hand imagery runs are clearly separated from hands/feet imagery runs.

## Milestone M2 - Repository Setup

### EEG-201 - Create repository skeleton

Priority: P0

Goal:

- Create the future project structure.

Acceptance criteria:

- README, docs, notebooks, reports, figures, and source folders exist.
- Data folders are ignored.
- No raw EEG data is committed.

### EEG-202 - Create dependency plan

Priority: P1

Goal:

- Make environment setup reproducible.

Acceptance criteria:

- Python version is stated.
- Core dependencies are listed.
- Setup instructions are clear enough for a new user.

### EEG-203 - Add citation and license files

Priority: P1

Goal:

- Make the repository professionally publishable.

Acceptance criteria:

- CITATION file includes dataset and tool references.
- LICENSE is selected for project code and docs.
- Dataset license is not confused with repository license.

## Milestone M3 - Signal Inspection

### EEG-301 - Load selected recordings

Priority: P0

Goal:

- Load selected PhysioNet EEG data through MNE.

Acceptance criteria:

- The workflow confirms subject IDs, run IDs, channels, sampling rate, and duration.
- Failures are handled with clear messages.

### EEG-302 - Produce raw signal preview

Priority: P0

Goal:

- Show representative raw EEG data.

Acceptance criteria:

- Figure is readable.
- Channels and time axis are labeled.
- Interpretation notes describe signal quality without clinical claims.

### EEG-303 - Summarize channel layout

Priority: P1

Goal:

- Show electrode/channel context.

Acceptance criteria:

- Channel names are summarized.
- Montage decision is documented.
- Any missing or unusual channels are noted.

## Milestone M4 - Preprocessing

### EEG-401 - Define preprocessing decisions

Priority: P0

Goal:

- Explain filtering, reference, montage, and artifact approach before applying them.

Acceptance criteria:

- Each preprocessing step has a rationale.
- Aggressive cleaning is avoided unless justified.

### EEG-402 - Apply conservative preprocessing

Priority: P0

Goal:

- Prepare data for basic event and frequency analysis.

Acceptance criteria:

- Before/after information is included.
- Parameters are documented.
- Data quality impact is described cautiously.

### EEG-403 - Decide whether ICA belongs in version 1

Priority: P2

Goal:

- Avoid black-box artifact removal.

Acceptance criteria:

- If ICA is included, components and rationale are documented.
- If ICA is deferred, the reason is documented.

## Milestone M5 - Events, Epochs, and Frequency Analysis

### EEG-501 - Extract and summarize events

Priority: P0

Goal:

- Build event count tables.

Acceptance criteria:

- Event counts are shown by subject, run, and condition.
- T0/T1/T2 labels are mapped correctly.

### EEG-502 - Create epochs

Priority: P0

Goal:

- Segment continuous EEG around relevant events.

Acceptance criteria:

- Epoch window is stated.
- Baseline handling is stated.
- Example epochs are visualized.

### EEG-503 - Compute PSD summaries

Priority: P0

Goal:

- Summarize spectral content.

Acceptance criteria:

- PSD plots compare at least eyes-open vs eyes-closed baseline.
- Optional motor imagery PSD comparison is included.
- Frequency ranges and units are readable.

### EEG-504 - Create optional topographic summaries

Priority: P2

Goal:

- Add spatial context if montage setup is reliable.

Acceptance criteria:

- Topomaps are readable.
- Figures are not included if channel positioning is uncertain.

## Milestone M6 - Documentation and GitHub Polish

### EEG-601 - Write final README

Priority: P0

Goal:

- Make the repository impressive and honest on first view.

Acceptance criteria:

- README includes purpose, dataset, pipeline, outputs, limitations, and roadmap.
- It clearly supports BCI/neurotech positioning.

### EEG-602 - Generate final report

Priority: P1

Goal:

- Provide a shareable analysis artifact.

Acceptance criteria:

- Report includes figures and interpretation.
- Report can be opened without rerunning code if possible.

### EEG-603 - Write limitations page

Priority: P0

Goal:

- Prevent overclaiming.

Acceptance criteria:

- Limitations mention small sample size, preprocessing choices, no clinical use, and no classifier in version 1.

### EEG-604 - Final QA

Priority: P0

Goal:

- Ensure the repo is safe to publish.

Acceptance criteria:

- No raw data in Git.
- Citations included.
- README polished.
- Figures present.
- Reproducibility instructions tested.

## Future Backlog

These are intentionally deferred:

- Motor imagery classifier.
- Cross-subject benchmark.
- Braindecode deep learning baseline.
- Real-time biosignal dashboard.
- BrainFlow integration.
- Streamlit or Next.js visual explorer.
