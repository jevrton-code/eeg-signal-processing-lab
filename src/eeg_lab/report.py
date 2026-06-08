"""Reproducible report assembly.

Responsibility
--------------
Assemble the committed figures, the pipeline description, and cautious
interpretation into a single self-contained HTML report (via :class:`mne.Report`)
for quality control and GitHub presentation.

Design choice
-------------
The report is built from the **already-exported PNG figures** in ``figures/``
(produced by notebooks 01 and 02) plus descriptive HTML sections, rather than by
re-running the analysis. This keeps report generation fast, deterministic, and
decoupled from data download. Regenerate the figures by executing the notebooks
first, then call :func:`build_report`.

The report makes no clinical or diagnostic claims; all interpretation is
descriptive and tied to the selected subjects (1-3) and runs (1, 2, 4, 8, 12).

Status
------
Version 1.0.
"""

from __future__ import annotations

from pathlib import Path

from . import config

DEFAULT_OUTPUT = config.REPO_ROOT / "reports" / "eeg_signal_processing_report.html"

# Curated, ordered (figure filename -> (section title, caption)). Only figures
# that exist on disk are added, so the report degrades gracefully.
_FIGURE_SECTIONS: list[tuple[str, str, str]] = [
    (
        "raw_signal_preview.png",
        "Raw EEG preview",
        "Representative raw (unfiltered, original-reference) EEG over a short "
        "window for subject 1, run 4. Descriptive only.",
    ),
    (
        "channel_layout.png",
        "Sensor montage layout",
        "EEGBCI 64-channel layout under the standard_1005 montage.",
    ),
    (
        "event_distribution.png",
        "Event distribution",
        "Annotation counts per run-aware condition across subjects 1-3, "
        "runs 1, 2, 4, 8, 12.",
    ),
    (
        "events_timeline_subject1_run4.png",
        "Events timeline (one run)",
        "Annotation timeline for subject 1, run 4, colored by run-aware "
        "condition (rest vs imagined left/right fist).",
    ),
    (
        "preprocessing_before_after.png",
        "Preprocessing: before/after PSD",
        "Mean PSD before vs after the conservative pipeline (1-40 Hz band-pass, "
        "average reference). The 40 Hz low-pass attenuates the 60 Hz line peak, "
        "so no notch is applied.",
    ),
    (
        "epochs_example.png",
        "Example epochs",
        "Condition-averaged, cue-locked epochs (-0.5 to +4.0 s) on C3/Cz/C4 for "
        "subject 1, run 4. Noisy small-sample averages, shown descriptively.",
    ),
    (
        "psd_baseline_comparison.png",
        "PSD baseline: eyes-open vs eyes-closed",
        "Grand-average occipital PSD (subjects 1-3): the expected eyes-closed "
        "alpha (8-13 Hz) increase is visible. An expected pattern, not a "
        "clinical finding.",
    ),
    (
        "band_topomap_eyes_closed.png",
        "Band-power topomaps (eyes closed)",
        "Normalized alpha/beta band-power topography for subject 1, run 2; alpha "
        "concentrates posteriorly as expected.",
    ),
]


def _intro_html() -> str:
    cfg = config.get_dataset_config()
    return f"""
    <h2>EEG Signal Processing Lab &mdash; reproducible report</h2>
    <p>A reproducible signal-processing and visualization lab over a small slice
    of the public <strong>PhysioNet EEG Motor Movement/Imagery Dataset
    (EEGMMIDB) v1.0.0</strong>, using MNE-Python. This is an educational,
    exploratory project: <strong>it is not a clinical or diagnostic tool and
    makes no medical claims</strong>, and it contains no classifier.</p>
    <h3>Analysis slice</h3>
    <ul>
      <li><strong>Subjects:</strong> {', '.join(map(str, cfg['subjects']))}</li>
      <li><strong>Runs:</strong> {', '.join(map(str, cfg['runs']))}
          (1 eyes-open, 2 eyes-closed baselines; 4, 8, 12 motor imagery L/R hand)</li>
      <li><strong>Confirmed facts:</strong> {cfg['expected_n_eeg_channels']} EEG
          channels @ {cfg['expected_sfreq_hz']:.0f} Hz, EDF+ format.</li>
    </ul>
    """


def _preprocessing_html() -> str:
    return f"""
    <h3>Conservative preprocessing (applied)</h3>
    <ul>
      <li><strong>Montage:</strong> standard_1005.</li>
      <li><strong>Band-pass:</strong> {config.FILTER_L_FREQ_HZ:.0f}&ndash;{config.FILTER_H_FREQ_HZ:.0f} Hz FIR (EEG).</li>
      <li><strong>Reference:</strong> {config.EEG_REFERENCE} (a documented convention, not ground truth).</li>
      <li><strong>Notch:</strong> inspected ({config.LINE_FREQ_HZ:.0f} Hz US line);
          not applied because the 40 Hz low-pass already covers it.</li>
      <li><strong>ICA:</strong> deliberately deferred (no black-box artifact removal).</li>
    </ul>
    <h3>Epochs</h3>
    <p>Cue-locked window <code>tmin={config.EPOCH_TMIN_S} s</code>,
    <code>tmax={config.EPOCH_TMAX_S} s</code>, baseline
    <code>{config.EPOCH_BASELINE}</code>, EEG picks only, run-aware condition
    labels. Rationale is summarized in the README pipeline section and this report.</p>
    """


def _limitations_html() -> str:
    return """
    <h3>Limitations</h3>
    <ul>
      <li><strong>Small sample:</strong> 3 subjects, 5 runs &mdash; not
          representative of the 109-subject dataset; nothing generalizes.</li>
      <li><strong>Exploratory preprocessing:</strong> chosen for transparency,
          not optimized performance.</li>
      <li><strong>No medical/clinical/diagnostic interpretation; no classifier;
          no real-time control.</strong></li>
      <li>Observations are descriptive and separated from conclusions.</li>
    </ul>
    <h3>References</h3>
    <ul>
      <li>PhysioNet EEGMMIDB v1.0.0:
          <a href="https://physionet.org/content/eegmmidb/1.0.0/">physionet.org/content/eegmmidb/1.0.0</a>
          (DOI: 10.13026/C28G6P).</li>
      <li>Schalk et al. (2004), BCI2000; Goldberger et al. (2000), PhysioNet.</li>
      <li>MNE-Python: <a href="https://mne.tools/">mne.tools</a>.</li>
    </ul>
    """


def build_report(
    output_path=None,
    *,
    figures_dir=None,
    open_browser: bool = False,
    overwrite: bool = True,
):
    """Assemble the reproducible HTML analysis report from exported figures.

    Parameters
    ----------
    output_path
        Destination ``.html`` path. Defaults to
        ``reports/eeg_signal_processing_report.html``.
    figures_dir
        Directory holding the exported PNG figures. Defaults to
        :data:`eeg_lab.config.FIGURES_DIR`.
    open_browser
        Forwarded to :meth:`mne.Report.save`.
    overwrite
        Whether to overwrite an existing report file.

    Returns
    -------
    pathlib.Path
        The path to the written HTML report.

    Raises
    ------
    FileNotFoundError
        If no expected figures are found (run the notebooks first).
    """
    import mne

    output_path = Path(output_path) if output_path is not None else DEFAULT_OUTPUT
    figures_dir = Path(figures_dir) if figures_dir is not None else config.FIGURES_DIR
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = mne.Report(title="EEG Signal Processing Lab — Report", verbose=False)
    report.add_html(_intro_html(), title="Overview")
    report.add_html(_preprocessing_html(), title="Pipeline & parameters")

    n_added = 0
    for filename, title, caption in _FIGURE_SECTIONS:
        path = figures_dir / filename
        if path.exists():
            report.add_image(image=path, title=title, caption=caption)
            n_added += 1

    if n_added == 0:
        raise FileNotFoundError(
            f"No expected figures found in {figures_dir}. Run the notebooks "
            "(01 and 02) to export figures before building the report."
        )

    report.add_html(_limitations_html(), title="Limitations & references")
    report.save(str(output_path), overwrite=overwrite, open_browser=open_browser)
    return output_path


def main() -> None:
    """CLI entry point: regenerate the report from the current figures."""
    path = build_report()
    size_kb = path.stat().st_size / 1024
    print(f"Wrote report to {path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
