# Dataset Notes

Accurate notes on the primary dataset, distilled from `docs/00_PROJECT_BRIEF.md`
and `docs/05_RESEARCH_NOTES.md`. Primary sources only (PhysioNet dataset page,
MNE-Python documentation, dataset DOI).

## Dataset Facts

| Property | Value |
| --- | --- |
| Name | EEG Motor Movement/Imagery Dataset (EEGMMIDB) |
| Version | 1.0.0 |
| Source | https://physionet.org/content/eegmmidb/1.0.0/ |
| DOI | https://doi.org/10.13026/C28G6P |
| Published | September 9, 2009 |
| Acquisition system | BCI2000 |
| Channels | 64 EEG channels |
| Sampling rate | 160 Hz |
| File format | EDF+ (with annotation channel) |
| Runs per subject | 14 |
| License | Open Data Commons Attribution License v1.0 (ODC-By) |
| Access | Open access; via MNE-Python EEGBCI helper |

MNE EEGBCI helper:
https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html

**Raw files are not committed to this repository.** Downloads are stored locally
under the git-ignored `data/raw/` directory.

## Run Structure (14 runs per subject)

| Run(s) | Task type | Condition |
| --- | --- | --- |
| 1 | Baseline | Eyes open |
| 2 | Baseline | Eyes closed |
| 3, 7, 11 | Motor **execution** | Left vs right hand |
| 4, 8, 12 | Motor **imagery** | Left vs right hand |
| 5, 9, 13 | Motor **execution** | Both hands vs both feet |
| 6, 10, 14 | Motor **imagery** | Both hands vs both feet |

## Event Mapping (critical)

The annotation channel uses three event codes: **T0**, **T1**, **T2**. Their
meaning is **not** globally fixed — T1 and T2 depend on the run type. Agents and
code must map labels using the **run number**, not the event code alone.

| Code | Baseline runs (1, 2) | L/R hand runs (3, 4, 7, 8, 11, 12) | Hands/feet runs (5, 6, 9, 10, 13, 14) |
| --- | --- | --- | --- |
| **T0** | Rest | Rest | Rest |
| **T1** | — | Onset of motion of the **left fist** | Onset of motion of **both fists** |
| **T2** | — | Onset of motion of the **right fist** | Onset of motion of **both feet** |

Notes:

- T0 always denotes rest.
- In left/right hand runs, T1/T2 = left/right fist (executed or imagined per run).
- In hands/feet runs, T1/T2 = both fists / both feet (executed or imagined).
- Whether T1/T2 are *executed* or *imagined* depends on whether the run is a
  motor-execution or motor-imagery run (see the run table above).
- The baseline runs (1, 2) contain a continuous resting recording and are not
  mixed with task runs.

This is the single most common failure mode for this dataset: treating T1/T2 as
universally fixed. Do not.

## Version 1 Subset (chosen)

- **Subjects:** 1, 2, 3
- **Runs:** 1, 2, 4, 8, 12

| Run | Role in v1 |
| --- | --- |
| 1 | Baseline, eyes open |
| 2 | Baseline, eyes closed |
| 4 | Motor imagery, left vs right hand |
| 8 | Motor imagery, left vs right hand |
| 12 | Motor imagery, left vs right hand |

**Rationale**

- Small enough to download and run quickly.
- Includes both baseline conditions for an eyes-open vs eyes-closed comparison.
- Includes three motor-imagery (left/right hand) runs, directly relevant to BCI.
- Deliberately excludes execution runs and hands/feet runs to keep the first
  release focused. Hands/feet imagery runs (6, 10, 14) may be added later.

## Citation Requirement

The dataset and PhysioNet must both be cited (Schalk et al. 2004 for BCI2000 /
the dataset; Goldberger et al. 2000 for PhysioNet), along with the dataset DOI.
See [`../CITATION.md`](../CITATION.md).
