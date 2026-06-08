# eeg-signal-processing-lab - Research Notes

## Source Priorities

Use primary sources first:

1. PhysioNet dataset page.
2. MNE-Python official documentation.
3. Dataset DOI and cited papers.
4. Peer-reviewed sources only when needed for interpretation.

Avoid building project decisions from blog posts, forum snippets, or uncited Kaggle mirrors unless they are explicitly labeled as secondary convenience resources.

## Dataset Notes

Dataset:

- EEG Motor Movement/Imagery Dataset v1.0.0.
- Source: https://physionet.org/content/eegmmidb/1.0.0/
- DOI: https://doi.org/10.13026/C28G6P
- Access: open access under the stated dataset license.
- Format: EDF+.
- Channels: 64 EEG channels.
- Sampling rate: 160 Hz.
- Experimental context: motor execution and motor imagery.

The dataset contains 14 runs per subject:

- Run 1: baseline, eyes open.
- Run 2: baseline, eyes closed.
- Runs 3, 7, 11: motor execution, left vs right hand.
- Runs 4, 8, 12: motor imagery, left vs right hand.
- Runs 5, 9, 13: motor execution, hands vs feet.
- Runs 6, 10, 14: motor imagery, hands vs feet.

Event labels:

- T0: rest.
- T1: depends on run type.
- T2: depends on run type.

Important caution:

- In left/right hand runs, T1 and T2 refer to left/right fist conditions.
- In hands/feet runs, T1 and T2 refer to both-fists/both-feet conditions.
- Agents must map labels using run number, not just event code.

## MNE-Python Notes

MNE-Python is the recommended foundation because it supports common EEG/MEG workflows and provides public dataset helpers, data structures, preprocessing tools, visualization, epoching, PSD, and reports.

Relevant MNE concepts:

- Raw: continuous recording.
- Events: time markers extracted from annotations/stimulus channels.
- Epochs: segmented time windows around events.
- Evoked: averaged response across epochs.
- Spectrum/PSD: frequency-domain representation.
- Report: self-contained HTML summary for quality control and sharing.

Useful official pages:

- Overview of MEG/EEG analysis: https://mne.tools/stable/auto_tutorials/intro/10_overview.html
- EEGBCI dataset helper: https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html
- Preprocessing tutorials: https://mne.tools/1.9/auto_tutorials/preprocessing/index.html
- Frequency analysis: https://mne.tools/stable/auto_tutorials/time-freq/20_sensors_time_frequency.html
- MNE Report: https://mne.tools/stable/auto_tutorials/intro/70_report.html

## Interpretation Guardrails

Do:

- Describe visual and statistical patterns.
- Use cautious language.
- Tie findings to selected subjects and runs.
- Explain preprocessing assumptions.
- Separate observations from conclusions.

Do not:

- Claim diagnostic meaning.
- Claim mind reading.
- Claim robust BCI performance.
- Generalize small-subject plots to all users.
- Present cleaned EEG as unquestionably true neural activity.

## Recommended First Write-Up Angle

Suggested GitHub narrative:

> This project is an EEG signal-processing lab using public motor imagery data. It focuses on reproducible loading, preprocessing, event mapping, epoching, and spectral analysis as a foundation for future BCI systems.

This framing is strong because it connects:

- EEG fundamentals.
- BCI relevance.
- Reproducible analysis.
- Future AI readiness.
- Your software engineering ability.

## Future Reading Topics

Only add these after version 1 is stable:

- Common spatial patterns.
- Motor imagery classification.
- Cross-subject validation.
- Artifact correction with ICA.
- EEGNet and deep learning for EEG.
- BrainFlow and real-time biosignal acquisition.
