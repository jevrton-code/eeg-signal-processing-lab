# EEG Signal Processing Lab

Research-style EEG signal-processing project using public motor movement and motor imagery data.

This repository explores how to load, inspect, preprocess, epoch, and summarize EEG recordings with Python and MNE-Python. The goal is to build a reproducible foundation for future BCI and neurotechnology projects.

## Why This Project

EEG-based BCI work depends on careful signal handling before any machine learning model is useful. This project focuses on the foundation: understanding raw neural signals, mapping events correctly, documenting preprocessing choices, and producing interpretable visual summaries.

This is not a clinical tool and does not make medical claims.

## Dataset

Primary dataset:

- PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0
- Source: https://physionet.org/content/eegmmidb/1.0.0/
- Format: EDF+
- Channels: 64 EEG channels
- Sampling rate: 160 Hz
- Experimental context: motor execution and motor imagery tasks

The dataset is accessed locally through MNE-Python's EEGBCI helper when possible:

- https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html

Raw dataset files are not stored in this repository.

## Project Goals

- Load public EEG motor imagery data.
- Inspect raw EEG recordings.
- Document channel, event, and run structure.
- Apply conservative preprocessing.
- Segment signals into epochs.
- Analyze spectral content with PSD.
- Generate readable figures and a reproducible report.
- Build a foundation for future BCI classification work.

## What This Project Shows

- EEG signal-processing fundamentals.
- Practical use of MNE-Python.
- Scientific documentation habits.
- Reproducible analysis workflow.
- Careful interpretation of noisy biosignals.

## Planned Pipeline

1. Select subjects and runs.
2. Load EEG recordings.
3. Inspect raw signals.
4. Apply montage and reference decisions.
5. Apply conservative filtering.
6. Parse events and map labels by run type.
7. Create epochs.
8. Generate PSD and frequency-band summaries.
9. Create a report and figures.
10. Document limitations and future work.

## Initial Scope

Version 1 focuses on signal processing and visualization.

Included:

- Baseline EEG analysis.
- Motor imagery run inspection.
- Event mapping.
- Epoch examples.
- Frequency analysis.
- GitHub-ready documentation.

Not included yet:

- Deep learning.
- Real-time control.
- Clinical interpretation.
- Full dataset benchmark.
- Motor imagery classification as the main objective.

## Expected Outputs

- Raw signal preview.
- Channel layout summary.
- Event distribution table.
- Example epochs.
- Power spectral density plots.
- Optional topographic frequency summaries.
- Reproducible notebook.
- Analysis report.

## Limitations

- The first version uses a small subject subset.
- Preprocessing choices are educational and exploratory.
- Results should not be generalized to all subjects.
- No medical or diagnostic interpretation is provided.
- Classification is reserved for a separate future project.

## Roadmap

- Version 0.1: repository structure and dataset notes.
- Version 0.2: first reproducible notebook.
- Version 0.3: preprocessing and event/epoch documentation.
- Version 1.0: polished report, figures, limitations, and README.

Future related projects:

- Motor imagery classifier.
- Real-time biosignal dashboard.
- Deep learning EEG benchmark.

## References

- PhysioNet EEG Motor Movement/Imagery Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MNE-Python: https://mne.tools/
- MNE EEGBCI dataset helper: https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html
- MNE preprocessing tutorials: https://mne.tools/1.9/auto_tutorials/preprocessing/index.html
- MNE frequency analysis tutorial: https://mne.tools/stable/auto_tutorials/time-freq/20_sensors_time_frequency.html
