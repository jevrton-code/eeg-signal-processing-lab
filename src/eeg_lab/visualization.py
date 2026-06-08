"""Plotting helpers for EEG signal inspection and frequency summaries.

Responsibility
--------------
Produce clear, well-labeled figures that explain the data and pipeline rather
than overstate findings. Every figure carries readable titles, axis labels,
units, and legends.

Status
------
Version 0.2. The inspection figures used by the first reproducible notebook are
implemented: a raw signal preview, a sensor/channel montage layout, an
events/condition distribution summary, and a single-run events timeline. PSD
and topographic summaries remain deferred to a later stage.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd

from . import config

# Microvolt scaling for display (EEGBCI data is stored in volts).
_VOLT_TO_UV = 1e6


def save_figure(fig, path, *, dpi: int = 110) -> Path:
    """Save a figure to ``path`` as a tight, modestly-sized PNG.

    A dpi of ~110 keeps the committed PNGs readable while staying well under a
    few hundred KB each.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def plot_raw_preview(
    raw: mne.io.BaseRaw,
    *,
    n_channels: int = 10,
    duration: float = 10.0,
    start: float = 0.0,
    title: str | None = None,
):
    """Render a representative raw EEG preview as stacked, offset traces.

    A small set of channels is shown over a short time window, offset
    vertically so individual traces are legible. Amplitudes are displayed in
    microvolts. This is a descriptive preview, not a quality verdict.

    Returns
    -------
    matplotlib.figure.Figure
    """
    picks = mne.pick_types(raw.info, eeg=True, meg=False)[:n_channels]
    ch_names = [raw.ch_names[p] for p in picks]
    sfreq = raw.info["sfreq"]
    start_samp = int(start * sfreq)
    stop_samp = int((start + duration) * sfreq)
    data, times = raw[picks, start_samp:stop_samp]
    data = data * _VOLT_TO_UV  # volts -> microvolts

    # Vertical offset based on typical signal spread so traces don't overlap.
    spread = np.median(np.ptp(data, axis=1))
    offset = spread * 1.2 if spread > 0 else 1.0

    fig, ax = plt.subplots(figsize=(11, 6))
    for i, name in enumerate(ch_names):
        ax.plot(times, data[i] + i * offset, linewidth=0.6, color="C0")
        ax.text(
            times[0] - 0.02 * (times[-1] - times[0]),
            i * offset,
            name,
            va="center",
            ha="right",
            fontsize=8,
        )
    ax.set_yticks([])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"{len(ch_names)} EEG channels (offset; amplitude in µV)")
    ax.set_title(title or "Raw EEG preview")
    # Scale bar for amplitude reference.
    ax.annotate(
        f"{offset:.0f} µV",
        xy=(times[-1], 0),
        xytext=(times[-1], offset),
        arrowprops=dict(arrowstyle="<->", color="0.4"),
        fontsize=8,
        color="0.4",
        ha="left",
        va="center",
    )
    fig.tight_layout()
    return fig


def plot_channel_montage(raw: mne.io.BaseRaw, *, title: str | None = None):
    """Render the sensor/channel montage layout (2-D topographic positions).

    Requires that a montage has been set (see
    :func:`eeg_lab.preprocessing.apply_montage`).

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig = raw.plot_sensors(show_names=True, show=False)
    fig.set_size_inches(8, 8)
    ax = fig.axes[0]
    ax.set_title(
        title or "Sensor montage layout (standard_1005)", fontsize=12
    )
    return fig


def plot_event_distribution(
    count_table: pd.DataFrame,
    *,
    condition_col: str = "condition",
    count_col: str = "count",
    title: str | None = None,
):
    """Render a bar chart of event counts per (run-aware) condition.

    Parameters
    ----------
    count_table
        DataFrame with one row per condition and a count column.
    condition_col, count_col
        Column names to read.

    Returns
    -------
    matplotlib.figure.Figure
    """
    tbl = count_table.sort_values(count_col, ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(tbl[condition_col], tbl[count_col], color="C0")
    ax.bar_label(bars, padding=2, fontsize=9)
    ax.set_xlabel("Condition (run-aware mapping)")
    ax.set_ylabel("Number of annotated events")
    ax.set_title(title or "Event distribution by condition")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    return fig


def plot_events_timeline(
    raw: mne.io.BaseRaw,
    run: int,
    *,
    subject: int | None = None,
    title: str | None = None,
):
    """Render an annotation timeline for a single run, colored by condition.

    Each annotation onset is drawn as a marker on a time axis, with its
    duration shown as a horizontal span and colored by the run-aware condition
    label. Useful to see the rest/task alternation within one run.

    Returns
    -------
    matplotlib.figure.Figure
    """
    mapping = config.map_events_by_run(run)
    conditions = list(dict.fromkeys(mapping.values()))
    color_for = {c: f"C{i}" for i, c in enumerate(conditions)}
    y_for = {c: i for i, c in enumerate(conditions)}

    fig, ax = plt.subplots(figsize=(11, max(2.5, 0.9 * len(conditions) + 1.5)))
    seen = set()
    for onset, dur, desc in zip(
        raw.annotations.onset, raw.annotations.duration, raw.annotations.description
    ):
        cond = mapping.get(desc, desc)
        y = y_for.get(cond, len(conditions))
        color = color_for.get(cond, "0.5")
        label = cond if cond not in seen else None
        seen.add(cond)
        ax.barh(y, dur, left=onset, height=0.6, color=color, alpha=0.8, label=label)

    ax.set_yticks(range(len(conditions)))
    ax.set_yticklabels(conditions)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Condition")
    subj_str = f"subject {subject}, " if subject is not None else ""
    ax.set_title(title or f"Events timeline ({subj_str}run {run}: {config.run_role(run)})")
    ax.legend(loc="upper right", fontsize=8, ncol=len(conditions))
    fig.tight_layout()
    return fig
