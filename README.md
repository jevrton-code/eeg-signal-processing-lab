# EEG Signal Processing Lab

> A reproducible EEG signal-processing lab using public motor movement / motor
> imagery data. It focuses on responsible loading, inspection, event mapping,
> preprocessing, epoching, and spectral analysis as a foundation for future
> brain–computer interface (BCI) and neurotechnology work.

![Status](https://img.shields.io/badge/status-v0.1%20scaffolding-orange)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Stack](https://img.shields.io/badge/stack-MNE--Python-7A4FE0)
![License](https://img.shields.io/badge/code%20license-MIT-green)
![Data](https://img.shields.io/badge/data-PhysioNet%20EEGMMIDB%20(ODC--By)-lightgrey)

## Project Status

**Version 0.1 — scaffolding / foundation.** This release contains the project
structure, documentation, dependency manifest, citation, and roadmap. **The
analysis pipeline is not yet implemented.** Source modules under `src/eeg_lab/`
are documented stubs; the first reproducible notebook arrives in v0.2. See
[`ROADMAP.md`](ROADMAP.md) for the staged plan.

This is an educational, exploratory signal-processing project. **It is not a
clinical or diagnostic tool and makes no medical claims.**

## Why This Project

EEG-based BCI work depends on careful signal handling long before any machine
learning model is useful. EEG is noisy, multidimensional, and easy to misuse.
This repository deliberately starts at the foundation: understanding raw neural
signals, mapping events correctly by run type, documenting preprocessing
decisions transparently, and producing interpretable visual summaries.

The intent is to show maturity with neural data — data loading, event mapping,
filtering, visualization, artifact awareness, reproducibility, and honest
interpretation — rather than to rush a classifier.

## Dataset

Primary dataset: **PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0**.

| Property | Value |
| --- | --- |
| Source | https://physionet.org/content/eegmmidb/1.0.0/ |
| DOI | https://doi.org/10.13026/C28G6P |
| Format | EDF+ (with annotation channel) |
| Channels | 64 EEG channels |
| Sampling rate | 160 Hz |
| Acquisition context | BCI2000 |
| Runs per subject | 14 |
| License | Open Data Commons Attribution License v1.0 (ODC-By) |

The dataset is accessed locally through MNE-Python's
[EEGBCI dataset helper](https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html).
Full run/event details (including the run-aware meaning of T0/T1/T2) are in
[`docs/dataset_notes.md`](docs/dataset_notes.md).

**Raw dataset files are never committed to this repository.** Downloaded data
is written to a local, git-ignored `data/raw/` directory (see Setup).

### Version 1 analysis slice

- **Subjects:** 1, 2, 3
- **Runs:** 1 (eyes-open baseline), 2 (eyes-closed baseline), 4, 8, 12 (motor
  imagery, left vs right hand)

This is small enough to run quickly while still demonstrating baseline
comparison and motor-imagery inspection. Rationale is documented in
[`docs/project_brief.md`](docs/project_brief.md).

## Repository Structure

```text
eeg-signal-processing-lab/
  README.md                  # This file
  LICENSE                    # MIT license for repository CODE
  CITATION.md                # How to cite the dataset, MNE-Python, and this repo
  ROADMAP.md                 # Versioning plan and deferred work
  pyproject.toml             # Project metadata + planned dependencies
  requirements.txt           # Convenience mirror of runtime dependencies
  .gitignore                 # Ignores raw data, EDF files, caches, envs
  docs/
    00_*..05_*.md            # Original planning files (source of truth)
    project_brief.md         # Public-facing condensed brief
    dataset_notes.md         # Dataset facts, run table, event mapping
    preprocessing_decisions.md  # Conservative preprocessing decision log
    limitations.md           # Honest limitations
  src/eeg_lab/               # Python package (documented stubs in v0.1)
    __init__.py
    config.py                # Subjects/runs/paths + event-mapping conventions
    data.py                  # MNE EEGBCI loading helpers
    preprocessing.py         # Conservative preprocessing + run-aware events
    visualization.py         # Figure helpers
    report.py                # Reproducible report assembly
  tests/                     # Minimal placeholder tests
    test_dataset_config.py
    test_event_mapping.py
  notebooks/                 # Reproducible notebooks (added in v0.2)
  reports/                   # Generated HTML reports (added later)
  figures/                   # Exported figures (added later)
  data/raw/                  # Local downloaded EEG data (GIT-IGNORED, not created)
```

## Setup / Installation

Requires **Python 3.11+**. Dependencies are declared in
[`pyproject.toml`](pyproject.toml) (with a convenience mirror in
[`requirements.txt`](requirements.txt)). The core stack is MNE-Python, NumPy,
pandas, Matplotlib, SciPy, and Jupyter.

```bash
# 1. Clone
git clone https://github.com/eeg-signal-processing-lab/eeg-signal-processing-lab.git
cd eeg-signal-processing-lab

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies (choose one)
pip install -e ".[dev]"            # from pyproject (editable, with dev tools)
# or
pip install -r requirements.txt    # runtime deps only
```

### Where data lives

EEG recordings are **not** part of this repository. When the analysis is
implemented, MNE-Python's EEGBCI helper downloads selected subject/run files
into a local, git-ignored directory:

```text
data/raw/    # downloaded EDF files (gitignored — never committed)
```

`data/` and common EEG formats (`*.edf`, `*.fif`, ...) are excluded via
[`.gitignore`](.gitignore), so raw signals cannot be accidentally committed.

## Planned Pipeline

1. Select subjects and runs.
2. Load EEG recordings via MNE EEGBCI.
3. Inspect raw signals (channels, sampling rate, duration, quality notes).
4. Apply montage and reference decisions.
5. Apply conservative filtering.
6. Parse events and map labels **by run type**.
7. Create epochs with a stated window.
8. Generate PSD and frequency-band summaries.
9. Assemble a reproducible report and figures.
10. Document limitations and next steps.

Each stage and its acceptance criteria are tracked in
[`ROADMAP.md`](ROADMAP.md).

## What This Project Shows

- EEG signal-processing fundamentals.
- Practical use of MNE-Python.
- Scientific documentation and reproducibility habits.
- Careful, cautious interpretation of noisy biosignals.
- A bridge between software engineering and neurotechnology.

## Limitations

The first versions use a small subject subset; preprocessing choices are
educational and exploratory; results should not be generalized; no medical or
diagnostic interpretation is provided; and classification is reserved for
future work. Full details in [`docs/limitations.md`](docs/limitations.md).

## License and Citation

- **Repository code** is released under the [MIT License](LICENSE).
- **The dataset** is licensed separately under the Open Data Commons
  Attribution License v1.0 (ODC-By) by PhysioNet — see
  [`CITATION.md`](CITATION.md) for full attribution of the dataset,
  MNE-Python, and this repository.

These two licenses are independent. Using this code does not grant any rights
over the dataset, and vice versa.

## References

- PhysioNet EEG Motor Movement/Imagery Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MNE-Python: https://mne.tools/
- MNE EEGBCI dataset helper: https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html

## GitHub Topics

`eeg` · `bci` · `brain-computer-interface` · `neurotechnology` ·
`signal-processing` · `mne-python` · `python` · `neuroscience` ·
`motor-imagery` · `open-science`
