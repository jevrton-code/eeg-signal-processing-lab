# Reports

This folder holds the generated, self-contained HTML analysis report.

## Why the HTML is not committed

`eeg_signal_processing_report.html` is a single self-contained file that embeds
every figure as base64. With the v1.0 figure set it is **~2.2 MB**, which
exceeds this repository's ~2 MB threshold for committed binaries. To keep the
repo lean and reviewable, the HTML is **git-ignored** (`reports/*.html`) and
regenerated locally. The small source PNGs it embeds **are** committed under
[`../figures/`](../figures/), so the report can always be rebuilt deterministically.

## How to regenerate

The report is assembled by `eeg_lab.report` from the exported figures (it does
not re-download data or re-run the heavy analysis). Make sure the figures exist
first by running the notebooks, then build the report:

```bash
# from an activated environment (see ../README.md)

# 1. (Re)generate the figures by executing the notebooks end-to-end
jupyter nbconvert --to notebook --execute --inplace \
  notebooks/01_eeg_signal_processing_lab.ipynb
jupyter nbconvert --to notebook --execute --inplace \
  notebooks/02_preprocessing_epochs_psd.ipynb

# 2. Build the HTML report from the figures in figures/
python -m eeg_lab.report
# -> writes reports/eeg_signal_processing_report.html
```

Or from Python:

```python
from eeg_lab.report import build_report

build_report()  # -> reports/eeg_signal_processing_report.html
```

## Contents

The report assembles, in order: an overview (dataset/subset, confirmed facts),
the pipeline and parameters, the committed figures with captions (raw preview,
montage, events, before/after PSD, example epochs, eyes-open vs eyes-closed PSD,
band topomaps), and a limitations/references section. It makes no clinical or
diagnostic claims and contains no classifier.
