# EEG Signal Processing Lab: LinkedIn context document

> **Language:** English · Versão em português: [`CONTEXTO_LINKEDIN.pt-BR.md`](CONTEXTO_LINKEDIN.pt-BR.md)
> **Last updated:** 2026-10-29
> **Project version covered:** v1.0.0 (commit `13d2ca2`, 2026-06-08)
> **Repository:** https://github.com/jevrton-code/eeg-signal-processing-lab

---

## 0. What this document is for

This file is the **single source of context** for everything published about
this project on LinkedIn: posts, carousels (PDF document posts), comments,
release updates and the profile's "Projects" section. Use it yourself or hand
the whole file to an AI assistant.

Everything here was checked against the repository (code, notebook outputs,
figures, tests and git history) on 2026-10-29. Where a number was derived and
is not written in the README, that is stated.

**How to use it**

- **To write a post:** read §1 (ready-made summaries), §5 (what the results
  mean) and §6 (what not to claim), then pick an angle from §12.
- **To brief an AI assistant:** give it this file and say which §12 angle you
  want, the language and the length. Tell it to use **only** the numbers in §4
  and to respect §6.
- **When the project changes:** update §4 (fact sheet), §8 (timeline) and §20
  (changelog) first.

**Non-negotiable rules for any public text**

1. Numbers come only from the fact sheet (§4), always with the context
   "subjects 1–3, runs 1, 2, 4, 8 and 12".
2. No clinical, diagnostic or cognitive interpretation. The project is
   educational and exploratory.
3. The eyes-closed alpha increase is an **expected, well-known pattern**,
   reproduced as a sanity check. It is not a discovery.
4. There is no classifier in this project. Classification lives in the sister
   project (BCI Motor Imagery Classifier, §17).
5. Credit the dataset and MNE-Python (§15).

---

## 1. Ready-made summaries (shortest to longest)

**One line (bio, image caption, carousel title)**

> A reproducible EEG signal-processing lab: loading, preprocessing, epoching
> and spectral analysis with MNE-Python on public data.

**Hook (fits before "see more")**

> Before training any model on EEG, I built a whole project just to understand
> the signal. The first trap was hiding in a label: "T1" doesn't always mean the
> same thing.

**Alternative hook (visual result)**

> Closing the eyes multiplied occipital alpha power by about 19 in my data. The
> effect has been known since 1929, and it was my sanity check.

**Short summary (for a quick post or a comment)**

> I built a reproducible EEG processing lab with MNE-Python on public PhysioNet
> data (3 subjects, 64 channels, 160 Hz). It goes from the raw signal to
> spectral analysis: inspection, conservative preprocessing (1–40 Hz, average
> reference), run-aware event mapping, epochs and PSD. The sanity check, the
> occipital alpha increase with eyes closed, showed up in all three subjects.
> No classifier, no promises: understand the signal first.

**Description for the profile's "Projects" section (about 1,400 characters;
LinkedIn limit: 2,000)**

```text
A reproducible EEG signal-processing lab, built as a foundation for brain-computer interface (BCI) and neurotechnology work.

What I did
• Loaded and inspected public data from the PhysioNet EEG Motor Movement/Imagery Dataset with MNE-Python (subjects 1–3; baseline and motor imagery runs; 64 channels, 160 Hz), checking the dataset facts instead of assuming them.
• Mapped the T0/T1/T2 events by run type, because the same code means different things in different runs; the code refuses to guess a mapping.
• Applied conservative, documented preprocessing: 10-05 montage, 1–40 Hz band-pass and average reference, with before/after evidence. Dropped the notch filter based on that evidence and deferred ICA with a written rationale.
• Built cue-locked epochs (−0.5 to +4.0 s), event-count tables and spectral analysis (PSD) with alpha and beta topographic maps.
• Kept the logic in a testable Python package (28 passing tests), with two reproducible notebooks and an auto-generated HTML report.

Sanity check result
The expected occipital alpha (8–13 Hz) increase with eyes closed showed up in all three subjects: a grand-average eyes-closed/eyes-open power ratio of 19.46.

Honest scope: an educational, exploratory project with 3 subjects. No classifier, no clinical interpretation, and no generalization to the full dataset.

Stack: Python, MNE-Python, NumPy, SciPy, pandas, Matplotlib, Jupyter, pytest.
```

**Suggested "Projects" fields**

| Field | Suggestion |
| --- | --- |
| Project name | EEG Signal Processing Lab: reproducible EEG processing with MNE-Python |
| Date | Jun 2026 (v1.0 released 2026-06-08) |
| Skills | Python · Signal Processing · Electroencephalography (EEG) · MNE-Python · Data Analysis |
| Media | Repository link + `figures/psd_baseline_comparison.png` (see §10) |
| Associated with | [TO FILL IN: role, course or "personal project"] |

---

## 2. The problem and the motivation

### In plain words

**EEG** records the brain's electrical activity through electrodes on the
scalp. The signal is weak (tens of microvolts), noisy and full of
interference: blinks, movement, the power grid. Before any AI model, you need
to know how to load, clean, segment and analyze that signal without distorting
it.

### Why start with the foundation

BCI projects often jump straight to the classifier. This project does the
opposite: it shows maturity with neural data (loading, event mapping,
filtering, visualization, artifact awareness, reproducibility and honest
interpretation) before building any model. In the words of `ROADMAP.md`: "the
signal is understood and documented before any model is built on top of it".

### Author's personal motivation

[TO FILL IN: why you wanted to build this, where your interest in
EEG/neurotechnology comes from, what you wanted to learn. See §19.]

---

## 3. What was built

### Flow overview

```text
PhysioNet EEGMMIDB v1.0.0 (EDF+, via mne.datasets.eegbci)
  └─ v1 slice: subjects 1–3 × runs 1, 2, 4, 8, 12  (15 recordings)
      └─ Notebook 01 — loading and inspection
      │    • channel names standardized ("Fcz." → "FCz")
      │    • 64 channels @ 160 Hz and durations confirmed
      │    • T0/T1/T2 mapped BY RUN TYPE
      │    • figures: raw signal, montage, event distribution and timeline
      └─ Notebook 02 — preprocessing, epochs and PSD
           • standard_1005 montage → 1–40 Hz band-pass (FIR) → average reference
           • no notch (60 Hz removed by the 40 Hz low-pass) · ICA deferred
           • epochs from −0.5 to +4.0 s with baseline (None, 0)
           • Welch PSD: eyes open vs eyes closed over O1/Oz/O2
           • alpha and beta topographic maps
  └─ eeg_lab.report → self-contained HTML report (generated locally)
```

### Run-aware event mapping (the critical detail)

The files use the codes T0, T1 and T2, but the meaning of T1/T2 **changes with
the run**:

| Code | Run 1 (eyes open) | Run 2 (eyes closed) | Runs 4, 8, 12 (left/right imagery) |
| --- | --- | --- | --- |
| T0 | rest (eyes open) | rest (eyes closed) | rest |
| T1 | — | — | left fist (imagined) |
| T2 | — | — | right fist (imagined) |

In the dataset's fists/feet runs (such as 6, 10 and 14), T1/T2 mean "both
fists" and "both feet". That is why `map_events_by_run` takes the **run
number** and raises an error for any run outside the slice instead of guessing
a label.

### Code layout

- `src/eeg_lab/`: package with pure, testable logic: `config` (slice, filter,
  epoch and band constants), `data` (loading through MNE), `preprocessing`,
  `spectral` (PSD and band power), `visualization` and `report` (HTML report
  assembly).
- `notebooks/01_eeg_signal_processing_lab.ipynb`: loading and inspection.
- `notebooks/02_preprocessing_epochs_psd.ipynb`: preprocessing, epochs and PSD.
- `tests/`: tests for configuration, event mapping, epochs and spectral
  functions (no network or data needed).
- `figures/`: 8 versioned figures.

### How to run it

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_eeg_signal_processing_lab.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_preprocessing_epochs_psd.ipynb
python -m eeg_lab.report   # -> reports/eeg_signal_processing_report.html
pytest -q
```

---

## 4. Fact sheet (verified numbers)

### Dataset and slice

| Item | Value | Source |
| --- | --- | --- |
| Dataset | PhysioNet EEG Motor Movement/Imagery Dataset v1.0.0 | `README.md` |
| DOI | 10.13026/C28G6P | `README.md` |
| Format | EDF+ with annotation channel; acquired with BCI2000 | `README.md` |
| Channels / sampling | 64 EEG @ 160 Hz (confirmed in all 15 files) | notebook 01 output |
| Runs per subject in the dataset | 14 | `README.md` |
| v1 subjects | 1, 2, 3 | `config.SUBJECTS` |
| v1 runs | 1 (eyes open), 2 (eyes closed), 4, 8, 12 (left/right imagery) | `config.RUNS` |
| Recordings analyzed | 15 (3 subjects × 5 runs) | notebook 01 |
| Baseline run duration | 60.99 s | notebook 01 |
| Imagery run duration | 122.99 to 124.99 s (mean 124.32 s) | notebook 01 |
| Annotations per imagery run | 30 | notebook 01 |
| Code license | MIT | `LICENSE` |
| Dataset license | ODC-By 1.0 (data not redistributed) | `CITATION.md` |

### Event counts (subjects 1–3, runs 1, 2, 4, 8, 12)

| Condition | Total | Per imagery run (summed over the 3 subjects) |
| --- | ---: | ---: |
| Rest (in imagery runs) | 135 | 45 |
| Left fist (imagined) | 69 | 23 |
| Right fist (imagined) | 66 | 22 |
| Rest, eyes open (run 1) | 3 | — |
| Rest, eyes closed (run 2) | 3 | — |

### Preprocessing and epochs

| Parameter | Value | Short rationale |
| --- | --- | --- |
| Montage | `standard_1005` (10-05) | Known positions for topographic maps |
| Band-pass | 1–40 Hz (FIR) | 1 Hz removes slow drift; 40 Hz keeps alpha and beta and stays below Nyquist (80 Hz) |
| Reference | Average | A documented convention, not "ground truth" |
| Notch | Not applied | The 40 Hz low-pass already attenuates the 60 Hz US line frequency; evidence in the before/after figure |
| ICA | Deferred | Written rationale; out of v1 scope |
| Bad channels | Manual/flagged handling, not automated | Design decision |
| Epoch window | −0.5 to +4.0 s, baseline (None, 0) | Covers the ~4.1 s task period |
| Epoch example (subject 1, run 4) | 29 epochs: 14 rest, 8 left, 7 right | notebook 02 |
| Bands | delta 1–4, theta 4–8, alpha 8–13, beta 13–30, gamma 30–40 Hz | `config.FREQ_BANDS` |
| PSD | Welch, 1–40 Hz | notebook 02 |

### Sanity check result: occipital alpha (O1/Oz/O2), eyes closed ÷ eyes open

| Subject | Alpha (8–13 Hz) power ratio |
| --- | ---: |
| 1 | 22.84 |
| 2 | 9.17 |
| 3 | 26.49 |
| **Grand average (mean PSD of the 3 subjects)** | **19.46** |

- The grand-average ratio is computed from the subjects' averaged PSD curves,
  not by averaging the three ratios.
- *Derived:* it is a **power** ratio. In amplitude terms it is about 4.4×
  (square root of 19.46). Always say "power" when quoting the 19.
- The topographic map (subject 1, run 2) shows alpha concentrated over the
  back of the head, as expected.

### Size and quality

- About 1,690 lines of Python (package and tests).
- 6 modules, 2 notebooks, 8 versioned figures.
- **Tests: 28 passing, 1 skipped** (an integration test that needs the data
  downloaded locally). Checked on 2026-10-29.
- An HTML report of about 2.2 MB, **not versioned** (it exceeds the project's
  ~2 MB limit for committed binaries); regenerated with
  `python -m eeg_lab.report`.
- MNE-Python version recorded in the notebook outputs: 1.12.1.

---

## 5. Results and interpretation (the stories the numbers tell)

### 5.1 The sanity check worked for all three subjects

When you close your eyes, occipital alpha power normally rises. It is one of
the oldest and most robust EEG effects, described by Hans Berger in 1929. Here
it appeared in all three subjects (ratios from 9.17 to 26.49). **This is not a
discovery:** it is proof that the loading, filtering and PSD pipeline is
correct. That is the right way to present the result.

### 5.2 Variation between people shows up even in a "guaranteed" effect

Subject 2 had a ratio of 9.17; subject 3, 26.49. Even a classic effect varies
almost threefold between people. It is the same message as the sister BCI
project: averages hide individuals.

### 5.3 An evidence-based decision: the filter that didn't make it

The plan was to evaluate a notch filter for the 60 Hz power line. The
before/after figure shows the 60 Hz peak in the raw signal and shows that the
40 Hz low-pass already removes it. Result: no unnecessary filter in the
pipeline. A concrete example of "inspect before you decide".

### 5.4 The signal is noisy, and the project says so

The averaged epochs (C3/Cz/C4, about 7–8 trials per condition in one run) are
noisy. The notebook states explicitly that this is **not** an established
evoked effect, only proof that epochs and labels work end to end.

---

## 6. What you can and cannot say

| ✅ OK to say | ❌ Do not say | Why |
| --- | --- | --- |
| "I reproduced the expected eyes-closed alpha increase as a sanity check" | "I discovered that..." / "My project shows the brain..." | The effect has been known since 1929. |
| "Grand-average alpha power ratio of 19.46 across 3 subjects" | "Alpha 19 times bigger" without saying "power" | In amplitude terms the ratio is about 4.4. |
| "An educational, exploratory project" | Any clinical, diagnostic or cognitive interpretation | The README explicitly excludes it. |
| "A foundation for BCI work" | "I built a BCI" / "an EEG classifier" | There is no classifier in this project. |
| "A reproducible, tested pipeline (28 tests)" | "100% tested" | Tests cover the pure logic; notebooks and figures are not automatically tested. |
| "Public PhysioNet data, 3 subjects" | "Analyzed the 109-subject dataset" | Only the v1 slice was analyzed. |
| "Conservative, documented preprocessing" | "Optimized preprocessing" / "removed all artifacts" | There is no ICA or artifact removal in v1. |

---

## 7. Engineering decisions (behind-the-scenes material)

1. **Map events by run number, never by code alone.** It is the most common
   failure mode with this dataset. The function raises an error for runs
   outside the slice instead of guessing.
2. **Confirm instead of assuming.** Notebook 01 checks 64 channels, 160 Hz and
   every file's duration instead of trusting the documentation.
3. **Standardize channel names** (`mne.datasets.eegbci.standardize`, which
   fixes things like "Fcz." → "FCz") so the 10-05 montage fits.
4. **Conservative preprocessing.** 1–40 Hz and average reference, each
   parameter justified; no "optimizing" filters without a criterion.
5. **Notch inspected and dropped with evidence** (before/after figure).
6. **ICA deferred on purpose**, with a written rationale. Knowing what not to
   do yet is also a decision.
7. **Notebooks orchestrate; the package holds the logic.** Pure functions in
   `eeg_lab` are testable without network or data.
8. **Repository hygiene.** Raw data never enters git (`data/raw/` and EEG file
   extensions are in `.gitignore`); the 2.2 MB HTML report is regenerated
   instead of versioned; only the source figures are versioned.
9. **Separate licenses.** MIT code; ODC-By 1.0 data, fully attributed in
   `CITATION.md`.
10. **Versioned releases.** v0.1 (structure and documentation) → v0.2 (first
    notebook) → v0.3 (preprocessing, epochs, PSD) → v1.0 (report and polish).
11. **Lean public documentation.** The `docs/` folder was removed and the
    essentials stayed in the README, the ROADMAP and the generated report.

---

## 8. Timeline

| Date | Version | Commit | What shipped |
| --- | --- | --- | --- |
| 2026-06-08 | v0.1 | `4c3c19a` | Structure, documentation, citation, roadmap |
| 2026-06-08 | v0.2 | `0333f29` | First reproducible notebook (subjects 1–3, runs 1, 2, 4, 8, 12) |
| 2026-06-08 | v0.3 | `ff241e9` | Conservative preprocessing, events and epochs |
| 2026-06-08 | v0.3 | `5760388` | Eyes-open vs eyes-closed PSD and band analysis |
| 2026-06-08 | v1.0 | `2848f46` | Reproducible report and final polish |
| 2026-06-08 | — | `1e8cc17` | GitHub URL updated in the README |
| 2026-06-08 | — | `13d2ca2` | `docs/` folder removed; lean public documentation |

No git tag or GitHub release exists yet (see §18).

---

## 9. Stack and skills

**Technologies:** Python 3.11+, MNE-Python (≥ 1.6; notebooks run with 1.12.1),
NumPy, SciPy, pandas, Matplotlib, Jupyter, pytest, ruff.

**Skills to tag on LinkedIn**

- Python
- Signal Processing
- Electroencephalography (EEG)
- MNE-Python
- Spectral Analysis / Time Series Analysis
- Jupyter
- Data Analysis
- Reproducible Research
- Neuroscience
- Neurotechnology

**Skills shown, in recruiter language**

- Working with real, noisy scientific data full of documentation traps.
- Making evidence-based technical decisions and recording them.
- Turning exploratory analysis into testable, reproducible code.
- Communicating limits clearly.

---

## 10. Available visual assets

| File | What it shows | Best use | Caveats |
| --- | --- | --- | --- |
| `figures/psd_baseline_comparison.png` (1088×591) | Occipital PSD, eyes open vs eyes closed, alpha band shaded | **Main image.** The red alpha peak reads instantly. | Explain it is the expected pattern. |
| `figures/preprocessing_before_after.png` (1088×536) | PSD before and after preprocessing, with the 60 Hz peak in the raw signal | Post about the dropped notch | Technical; needs an explanatory caption. |
| `figures/raw_signal_preview.png` (1197×646) | 10 s of raw EEG across 10 channels | Cover or opener ("this is how EEG arrives") | Unfiltered: shows drift and artifacts, on purpose. |
| `figures/events_timeline_subject1_run4.png` (1198×448) | Timeline of rest and left/right fist cues in one run | Post about T0/T1/T2 mapping | The legend covers part of two green bars. |
| `figures/band_topomap_eyes_closed.png` (531×177) | Alpha and beta topographic maps | Visual complement | **Resolution far too low** for LinkedIn; regenerate at higher DPI first. |
| `figures/channel_layout.png` (884×892) | 64-channel montage | Explaining what EEG is | Almost square; good for a carousel. |
| `figures/epochs_example.png` (1374×457) | Averaged epochs at C3/Cz/C4 | "Noise is honest" post | Noisy; never present it as an effect. |
| `figures/event_distribution.png` (978×536) | Event counts per condition | Post about the data slice | Low visual impact on its own. |

**Suggested carousel outline (8 slides, 1080×1350)**

1. Cover: "Before the model, the signal" + project name.
2. What EEG is, with `raw_signal_preview.png`.
3. The T1/T2 trap (table from §3).
4. Preprocessing in 3 steps (montage → 1–40 Hz → average reference).
5. The filter that didn't make it (`preprocessing_before_after.png`).
6. The sanity check (`psd_baseline_comparison.png` + per-subject ratios).
7. What this project does NOT do (§6).
8. Next step: the BCI benchmark + GitHub link + credits.

**Missing assets:** a GitHub *social preview* image (1280×640); a
high-resolution topomap; an online version of the HTML report (for example
through GitHub Pages) or a PDF export for a document post.

---

## 11. Audience, positioning and tone

### Who the posts speak to

| Audience | What they look for | What to highlight |
| --- | --- | --- |
| Recruiters and engineering managers | Rigor and the ability to handle real data | Documented decisions, tests, reproducibility |
| Data and engineering people | Good practices | Testable pure logic, notebooks as orchestration, repository hygiene |
| Neurotech and EEG community | Domain depth | Run-aware mapping, 10-05 montage, average reference, notch and ICA |
| Students | Learning EEG hands-on | Step-by-step pipeline, glossary |
| Curious general public | Understanding what EEG is | The eyes-closed alpha effect (an experiment anyone gets) |

### Suggested positioning

> Software engineering applied to neurotechnology: understand the signal
> before building the model, with public data, documented decisions and clear
> limits.

### Tone of voice

- First person, curious and educational.
- Honest "failures" (a noisy signal, an effect that varies) are content.
- Avoid "decoding the brain", "reading thoughts" and the like.
- Short paragraphs; few emojis, if any.

### LinkedIn format notes (check them, limits change)

- Post: up to 3,000 characters; the hook must fit in the first lines (about
  200 characters) before "see more".
- "Projects" section description: up to 2,000 characters.
- Carousel: PDF document post with portrait (1080×1350) or square slides.
- Hashtags: 3 to 5 relevant ones.

---

## 12. Bank of post angles

### A. Launch: before the model, the signal
- **Hook:** "Before training any model on EEG, I built a whole project just to
  understand the signal."
- **Points:** the flow from raw to PSD; documented decisions; the sanity
  check; no classifier, on purpose.
- **Visual:** the §10 carousel or `psd_baseline_comparison.png`.
- **CTA:** GitHub link.

### B. T1 isn't always T1
- **Hook:** "The same event code means different things in the same dataset.
  My code refuses to guess."
- **Points:** T0/T1/T2 table; runs 4/8/12 vs 6/10/14; `ValueError` for runs
  outside the slice; a general lesson about metadata.
- **Visual:** `events_timeline_subject1_run4.png`.
- **Audience:** data and engineering.

### C. Close your eyes (the Berger effect)
- **Hook:** "Closing the eyes multiplied alpha power by about 19 in my data.
  And that's not a discovery."
- **Points:** effect described since 1929; per-subject ratios; power vs
  amplitude; why a sanity check is worth more than a new result.
- **Visual:** `psd_baseline_comparison.png`.
- **Audience:** general public and neurotech.

### D. The filter I didn't use
- **Hook:** "I was going to add a filter. The evidence said I didn't need it."
- **Points:** 60 Hz peak in the raw signal; the 40 Hz low-pass already removes
  it; inspect before deciding.
- **Visual:** `preprocessing_before_after.png`.

### E. Knowing what to defer
- **Hook:** "I left ICA out. On purpose."
- **Points:** v1 scope; written rationale; the difference between "didn't do
  it" and "decided not to do it yet".

### F. Trust, but verify
- **Hook:** "The documentation said 64 channels and 160 Hz. I checked anyway."
- **Points:** all 15 files verified; channel names fixed ("Fcz." → "FCz");
  durations recorded.

### G. Notebooks are not the product
- **Hook:** "My notebooks contain no logic. It lives in a package with 28
  tests."
- **Points:** orchestration vs logic; tests without network or data; an
  integration test that only runs when the data exists.
- **Audience:** engineering and data.

### H. Noise is honest
- **Hook:** "This plot is ugly. And it's correct."
- **Points:** averaged epochs with 7–8 trials; why not to call it an effect;
  mature interpretation.
- **Visual:** `epochs_example.png`.

### I. What stays out of git
- **Hook:** "My report is 2.2 MB and it's not in the repository."
- **Points:** raw data never versioned; a regenerable report; only source
  figures in git; separate licenses.

### J. Series: from signal to classifier
- **Hook:** "First I understood the signal. Then I tried to classify it."
- **Points:** link to the BCI Motor Imagery Classifier, same dataset (§17).

---

## 13. Glossary for plain-language posts

| Term | Plain explanation |
| --- | --- |
| **EEG** | A recording of the brain's electrical activity through electrodes on the scalp. |
| **Channel / electrode** | Each measurement point on the scalp. There are 64 here. |
| **10-05 montage** | A standardized map of electrode positions on the head. |
| **Band-pass filter** | Keeps only the frequencies of interest (here, 1 to 40 Hz). |
| **Notch filter** | Removes one specific frequency, such as the 60 Hz power line. |
| **Average reference** | Measures each electrode relative to the average of all of them. |
| **ICA** | A technique that splits the signal into components, used to remove blinks and other artifacts. |
| **Artifact** | A signal that doesn't come from the brain: blinks, muscles, the power grid. |
| **Epoch** | A slice of the signal aligned to an event (here, −0.5 to +4 s around each cue). |
| **PSD (power spectral density)** | How much "energy" the signal has at each frequency. |
| **Alpha band (8–13 Hz)** | A rhythm that grows over the back of the head when we close our eyes and relax. |
| **Beta band (13–30 Hz)** | A rhythm associated, among other things, with motor activity. |
| **Topographic map** | A top-down map of the head, colored by power in each region. |
| **Motor imagery** | Imagining a movement without performing it. |
| **T0 / T1 / T2** | The dataset's event codes; what T1/T2 mean depends on the run. |

---

## 14. Hashtags and keywords

**Hashtags (pick 3 to 5 per post)**

- Core: `#EEG` `#SignalProcessing` `#Neurotechnology` `#Python` `#MNEPython`
- Reach: `#Neuroscience` `#OpenScience` `#DataScience` `#BCI`
  `#ReproducibleResearch`
- Portuguese-speaking reach: `#ProcessamentoDeSinais` `#Neurotecnologia`
  `#Neurociência`

**Keywords for search and profile SEO:** EEG, signal processing, MNE-Python,
PSD, spectral analysis, alpha band, EEG preprocessing, epochs, PhysioNet,
neurotechnology, brain-computer interface.

---

## 15. Credits and citations

**Short line for the end of a post**

> Data: PhysioNet EEG Motor Movement/Imagery Dataset (Schalk et al., 2004;
> doi:10.13026/C28G6P), ODC-By 1.0. Analysis with MNE-Python (Gramfort et al.,
> 2013).

**Full references** (details and BibTeX in `CITATION.md`)

- Schalk, G. et al. (2004). BCI2000: A General-Purpose Brain-Computer
  Interface (BCI) System. *IEEE Trans. Biomed. Eng.*, 51(6), 1034–1043.
- Goldberger, A. L. et al. (2000). PhysioBank, PhysioToolkit, and PhysioNet.
  *Circulation*, 101(23), e215–e220.
- EEG Motor Movement/Imagery Dataset (v1.0.0). PhysioNet (2009).
  https://doi.org/10.13026/C28G6P
- Gramfort, A. et al. (2013). MEG and EEG Data Analysis with MNE-Python.
  *Front. Neurosci.*, 7, 267.

**Useful links**

- Dataset: https://physionet.org/content/eegmmidb/1.0.0/
- MNE-Python: https://mne.tools/

---

## 16. Roadmap and update triggers

Items deferred on purpose (`ROADMAP.md`) and the post each would enable:

| Future delivery | Post it enables |
| --- | --- |
| Motor imagery classifier | Already exists as a separate project (BCI Motor Imagery Classifier). A post linking the two. |
| Cross-subject benchmark on all 109 subjects | "Does the alpha effect hold across 109 people?" |
| Deep learning (Braindecode, EEGNet) | "After the foundation, the models" |
| Real-time biosignal dashboard / BCI control | A change of scope: offline → online |
| BrainFlow and hardware integration | "From a public dataset to my own EEG" |
| Visual explorer (Streamlit / Next.js) | An interactive demo: great visual material |
| ICA and artifact handling | "Removing blinks: before and after" |

**Rule:** every update should state the data slice used and compare against
the v1 numbers (§4) where it makes sense.

---

## 17. How it fits the portfolio

This is one of three public projects that form a coherent story:

| Project | Question it answers | Date |
| --- | --- | --- |
| **EEG Signal Processing Lab** (this one) | How do you load, inspect, preprocess and analyze EEG responsibly? | Jun 2026 |
| [BCI Motor Imagery Classifier](https://github.com/jevrton-code/bci-motor-imagery-classifier) | Can motor imagery be classified, and how do you evaluate that honestly? | Jun 2026 |
| [FlyWire Propagation Sim](https://github.com/jevrton-code/flywire-propagation-sim) | How does activity spread through a real neural circuit, mapped synapse by synapse? | Aug 2026 |

**The common thread:** real public data, reproducibility, disciplined software
engineering and honesty about limits. This project and the BCI one use the
**same dataset**: here the signal is understood, there classifiers are built
and evaluated. FlyWire moves from the signal measured on the scalp to the
brain's wiring diagram, with a full-stack app.

**Possible portfolio post:** "Three projects, one rule: write down what the
model doesn't do before showing what it does."

---

## 18. Issues to fix before promoting the project

1. **Low-resolution topomap** (531×177): regenerate at a higher DPI
   (`save_figure` defaults to 110).
2. **The HTML report is not available online.** Visitors coming from LinkedIn
   can't see it without running the project. Options: GitHub Pages, a PDF of
   the report, or a link to the notebooks rendered on GitHub.
3. **No tag or GitHub release.** Creating a `v1.0.0` release gives a stable
   link to announce.
4. **Generic author in `pyproject.toml`** ("eeg-signal-processing-lab
   contributors"). Optional: add your name.
5. **No *social preview* image** set on GitHub.
6. **Overlapping legend** in `events_timeline_subject1_run4.png` (it covers
   part of two bars).
7. `ROADMAP.md` mentions a "finalized limitations page"; since `docs/` was
   removed, the limitations live in the README and the report. Worth updating
   the wording.

---

## 19. Personal context to fill in (what the repository can't know)

- **Why this project:** [TO FILL IN]
- **Your background and path so far:** [TO FILL IN]
- **Time invested and context** (personal project, course, career change):
  [TO FILL IN]
- **What was hardest or most surprising:** [TO FILL IN]
- **Tools used along the way**, including AI assistants if you want to mention
  them: [TO FILL IN]
- **Career goal** (type of role, field, companies of interest): [TO FILL IN]
- **People or communities to thank or tag:** [TO FILL IN]
- **Your LinkedIn profile URL:** [TO FILL IN]

---

## 20. Document changelog

| Date | Change |
| --- | --- |
| 2026-10-29 | First version, covering the project at v1.0.0 (`13d2ca2`). Numbers checked against the notebook outputs; tests run locally (28 passing, 1 skipped). |
