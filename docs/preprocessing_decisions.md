# Preprocessing Decision Log

A decision log for the conservative preprocessing posture of this project. The
guiding principle is **transparency over aggressive cleaning**: prefer simple,
well-documented steps and readable before/after plots over black-box automated
correction.

> **Status:** every decision below is **Planned (not yet applied in v0.1)**.
> This file is a scaffold. Parameters and rationale will be confirmed against
> the real data when the pipeline is implemented (v0.3), and any change from the
> defaults stated here will be recorded with its justification.

## How to read this log

Each decision records: the question, the planned conservative default, the
rationale, and the status. When applied, we will add the actual parameters used
and before/after evidence.

---

## 1. Montage selection

- **Planned default:** Assign the standard 10-05 / 10-20 montage that matches
  the EEGBCI channel naming (via MNE's standard montages), after normalizing the
  channel names produced by the EEGBCI reader.
- **Rationale:** A correct montage is required for topographic plots and spatial
  interpretation. Using a documented standard montage avoids ad hoc electrode
  positioning.
- **Status:** Planned (not yet applied in v0.1).

## 2. EEG reference

- **Planned default:** Keep the original reference for initial inspection, then
  apply an average reference for spectral/topographic summaries — documenting
  both, and noting that the average reference is a convention, not ground truth.
- **Rationale:** The reference choice changes the apparent signal. A conservative
  approach states the choice explicitly and avoids implying a single correct
  reference.
- **Status:** Planned (not yet applied in v0.1).

## 3. Filtering range (band-pass)

- **Planned default:** A gentle band-pass of approximately **1–40 Hz** for
  general inspection and PSD work (well within the 160 Hz sampling Nyquist of
  80 Hz).
- **Rationale:** Removes slow drifts and high-frequency noise while preserving
  the alpha/beta ranges relevant to motor imagery and eyes-open/closed contrast.
  Exact cutoffs and filter design will be stated when applied.
- **Status:** Planned (not yet applied in v0.1).

## 4. Notch / line-noise filter

- **Planned default:** **Inspect first.** Decide on a notch filter only after
  examining the PSD for a line-noise peak (50 or 60 Hz depending on acquisition
  region). Do not apply a notch blindly.
- **Rationale:** Applying a notch without evidence of line noise adds processing
  without justification. Inspection keeps the decision honest.
- **Status:** Planned (not yet applied in v0.1).

## 5. Bad channel handling

- **Planned default:** Identify suspicious channels by visual inspection and
  simple descriptive checks; mark them explicitly. Prefer flagging/excluding
  with documentation over silent interpolation.
- **Rationale:** Conservative handling avoids fabricating data. Any
  interpolation, if used, will be disclosed.
- **Status:** Planned (not yet applied in v0.1).

## 6. ICA (artifact correction)

- **Planned default:** **Deferred** for version 1 unless components can be
  clearly justified and visualized.
- **Rationale:** ICA is powerful but easy to misuse as a black box. The project
  explicitly avoids opaque artifact removal in the first release; if introduced
  later, components and the removal rationale will be documented.
- **Status:** Planned / deferred (not applied in v0.1).

---

## Summary table

| # | Decision | Planned conservative default | Status |
| --- | --- | --- | --- |
| 1 | Montage | Standard 10-05/10-20 montage | Planned (v0.1) |
| 2 | Reference | Original for inspection; average for summaries | Planned (v0.1) |
| 3 | Band-pass filter | ~1–40 Hz | Planned (v0.1) |
| 4 | Notch filter | Inspect PSD first; apply only if needed | Planned (v0.1) |
| 5 | Bad channels | Flag/exclude with documentation | Planned (v0.1) |
| 6 | ICA | Deferred unless clearly justified | Planned / deferred |
