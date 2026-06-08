# Limitations

This project is intentionally scoped and cautious. The following limitations
apply and should be kept in mind when reading any current or future results.

## Sample size

- The version 1 analysis uses a **small subject subset** (subjects 1–3) and a
  small set of runs (1, 2, 4, 8, 12). This is not a representative sample of the
  full 109-subject dataset.
- Any observation is **tied to the selected subjects and runs** and must not be
  generalized to all subjects, sessions, or recording conditions.

## Preprocessing

- Preprocessing choices are **educational and exploratory**, chosen for
  transparency rather than optimized performance.
- There is no single "correct" preprocessing pipeline. Reference, filtering, and
  artifact decisions are documented in
  [`preprocessing_decisions.md`](preprocessing_decisions.md) and may change as
  the project matures.
- Cleaned EEG should not be presented as unquestionably true neural activity.

## Interpretation

- **No medical, clinical, or diagnostic interpretation is provided or implied.**
  This repository is not a medical device and makes no health claims.
- Findings are descriptive observations about a public dataset, not conclusions
  about cognition, intent, or clinical state.
- The project does not claim mind reading, robust BCI performance, or
  generalizable effects.

## Scope

- **No classifier in version 1.** Motor-imagery classification, cross-subject
  benchmarking, and deep learning are explicitly deferred (see `ROADMAP.md`).
- **No real-time control** and no hardware integration.
- Results, once produced, are tied to the selected subjects/runs and the stated
  preprocessing assumptions.

## Reproducibility caveats

- Results depend on dataset version (1.0.0), the exact runs/subjects selected,
  and the documented preprocessing parameters (band-pass 1–40 Hz, average
  reference, epoch window −0.5 to +4.0 s). Changing any of these can change the
  output.
- The analysis is reproducible from the two notebooks plus the `eeg_lab`
  package; figures are exported to `figures/` and the HTML report is regenerated
  locally (see `reports/README.md`).

## Specific to the v1.0 results

- The eyes-closed occipital alpha increase observed here (grand-average
  eyes-closed/eyes-open alpha ratio ≈ 19 over subjects 1–3) is an **expected
  physiological pattern**, reported descriptively. It is not a clinical finding
  and its magnitude should not be generalized beyond this sample.
- Condition-averaged epochs use only ~7–14 trials per condition in a single run,
  so they are noisy; they demonstrate that epoching/labeling work, not an
  established evoked effect.
- No bad channels were excluded and no ICA was performed; residual eye/movement
  artifacts remain in the data by design (transparency over aggressive cleaning).
