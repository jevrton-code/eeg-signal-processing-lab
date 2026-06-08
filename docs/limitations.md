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
  and the documented preprocessing parameters. Changing any of these can change
  the output.
- As of v0.1, no analysis has been run; this is scaffolding only.
