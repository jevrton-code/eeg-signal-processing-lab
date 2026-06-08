# Preprocessing Decision Log

A decision log for the conservative preprocessing posture of this project. The
guiding principle is **transparency over aggressive cleaning**: prefer simple,
well-documented steps and readable before/after plots over black-box automated
correction.

> **Status (v0.3):** the conservative pipeline is now **applied** in
> `eeg_lab.preprocessing.apply_basic_preprocessing` and exercised in
> `notebooks/02_preprocessing_epochs_psd.ipynb`. The applied parameters and
> their rationale are recorded below; ICA remains deliberately **deferred**.
> Any future change from these defaults will be recorded with its justification.

## How to read this log

Each decision records: the question, the planned conservative default, the
rationale, and the status. When applied, we will add the actual parameters used
and before/after evidence.

---

## 1. Montage selection

- **Applied:** `standard_1005` montage (`mne.channels.make_standard_montage`),
  assigned after normalizing the EEGBCI channel names with
  `mne.datasets.eegbci.standardize`. Missing positions are handled with
  `on_missing="warn"`.
- **Rationale:** A correct montage is required for topographic plots and spatial
  interpretation. Using a documented standard montage avoids ad hoc electrode
  positioning. The standardized EEGBCI names map cleanly onto `standard_1005`.
- **Status:** **Applied (v0.3)** in `apply_montage` / `apply_basic_preprocessing`.

## 2. EEG reference

- **Applied:** Original reference is kept for raw inspection (notebook 01); an
  **average reference** (`set_eeg_reference("average", projection=False)`) is
  applied in the preprocessing pipeline used for epochs and spectral summaries
  (notebook 02). Configured via `config.EEG_REFERENCE`.
- **Rationale:** The reference choice changes the apparent signal. The average
  reference is a documented convention (not ground truth); stating it explicitly
  avoids implying a single correct reference. Inspection on the original
  reference and analysis on the average reference are kept separate and labeled.
- **Status:** **Applied (v0.3).**

## 3. Filtering range (band-pass)

- **Applied:** A gentle FIR band-pass of **1–40 Hz** (`config.FILTER_L_FREQ_HZ`
  = 1.0, `config.FILTER_H_FREQ_HZ` = 40.0), MNE default FIR design
  (`raw.filter(l_freq=1.0, h_freq=40.0, picks="eeg")`), applied to EEG channels.
  This is well within the 80 Hz Nyquist (160 Hz sampling).
- **Rationale:** The 1 Hz high-pass removes slow drifts; the 40 Hz low-pass
  removes high-frequency muscle/broadband noise while preserving the delta–beta
  ranges relevant to motor imagery and the eyes-open/closed alpha contrast.
- **Evidence:** Before/after mean-PSD comparison saved to
  `figures/preprocessing_before_after.png`.
- **Status:** **Applied (v0.3).**

## 4. Notch / line-noise filter

- **Decision: not applied (deferred), by inspection.** The PSD is inspected
  before deciding (see the before/after figure). PhysioNet EEGMMIDB was acquired
  in the US, so the relevant line frequency is **60 Hz**
  (`config.LINE_FREQ_HZ`). Because the analysis band-pass already low-passes at
  **40 Hz**, the 60 Hz line component lies in the stop-band and is attenuated —
  a separate notch would add processing without changing the analysis band.
- **Rationale:** Applying a notch without it affecting the analyzed band would
  be processing-for-its-own-sake. `apply_basic_preprocessing` exposes a
  `notch_freqs` argument so a 60 Hz notch can be enabled explicitly if a future
  analysis widens the band above 40 Hz.
- **Status:** **Inspected; not applied (v0.3)** — documented deferral.

## 5. Bad channel handling

- **Applied posture:** No automated bad-channel detection or interpolation.
  Suspicious channels are identified by visual inspection (raw preview / PSD) and
  would be marked explicitly in `raw.info["bads"]` with documentation. None were
  excluded for the v0.3 slice.
- **Rationale:** Conservative handling avoids fabricating data. Any
  interpolation, if used, will be disclosed.
- **Status:** **Applied posture (v0.3):** manual/flagged, no silent interpolation.

## 6. ICA (artifact correction)

- **Decision: deferred.** ICA is **not** performed in v0.3/v1.0.
- **Rationale:** ICA is powerful but easy to misuse as a black box. The project
  explicitly avoids opaque artifact removal in the first release. The raw preview
  shows eye/movement-type deflections that ICA *could* target, but doing so
  responsibly requires component-by-component justification and visualization,
  which is out of scope for this signal-inspection lab. If introduced later,
  every removed component and its rationale will be documented.
- **Status:** **Deferred (v0.3 / v1.0).**

---

## 7. Events and epochs (v0.3)

- **Event mapping:** Run-aware (`config.map_events_by_run`): `T0` = rest
  everywhere; in L/R-hand imagery runs (4, 8, 12) `T1` = left fist (imagined),
  `T2` = right fist (imagined). Baseline runs (1, 2) contain only `T0`.
- **Epoch window:** **`tmin = -0.5 s`, `tmax = +4.0 s`** relative to the cue
  onset (`config.epoch_window()`). The 0.5 s pre-cue segment provides a
  baseline; +4.0 s covers the ~4.1 s annotated task period for motor imagery.
- **Baseline correction:** `(None, 0.0)` — i.e. from the epoch start (−0.5 s) to
  the cue onset (`config.EPOCH_BASELINE`). Mean-subtraction baseline correction
  on the pre-cue interval.
- **Picks:** EEG channels only. No amplitude rejection threshold is applied by
  default (conservative: epochs are inspected rather than auto-dropped); a
  `reject` dict can be supplied if needed.
- **Rationale:** A short, cue-locked window with a pre-cue baseline is a standard,
  conservative choice for cue-locked motor-imagery epochs and keeps the example
  epochs interpretable without overlapping unrelated cues excessively.
- **Status:** **Applied (v0.3)** in `eeg_lab.preprocessing.make_epochs`.

---

## Summary table

| # | Decision | Applied value | Status |
| --- | --- | --- | --- |
| 1 | Montage | `standard_1005` | Applied (v0.3) |
| 2 | Reference | Original for inspection; average for analysis | Applied (v0.3) |
| 3 | Band-pass filter | 1–40 Hz FIR (EEG) | Applied (v0.3) |
| 4 | Notch filter | 60 Hz inspected; not applied (covered by 40 Hz low-pass) | Inspected, deferred (v0.3) |
| 5 | Bad channels | Manual flagging; no auto-interpolation | Applied posture (v0.3) |
| 6 | ICA | Not performed | Deferred (v0.3 / v1.0) |
| 7 | Epochs | tmin −0.5 s, tmax +4.0 s, baseline (None, 0) | Applied (v0.3) |
