"""Plotting helpers for EEG signal inspection and frequency summaries.

Responsibility
--------------
Produce clear, well-labeled figures that explain the data and pipeline rather
than overstate findings. Every figure carries readable titles, axis labels,
units, and legends.

Status
------
Version 0.3. Adds, on top of the v0.2 inspection figures (raw preview, montage
layout, event distribution, events timeline): a before/after band-pass PSD
comparison, a condition-averaged epochs overview, a baseline PSD comparison
(eyes-open vs eyes-closed), and an optional band-power topomap.
"""

from __future__ import annotations

from collections.abc import Sequence
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


def _mean_psd_db(raw, *, fmin: float, fmax: float):
    """Return (freqs, mean-over-EEG-channels PSD in dB) for a raw recording."""
    spectrum = raw.compute_psd(method="welch", fmin=fmin, fmax=fmax, picks="eeg", verbose=False)
    psds, freqs = spectrum.get_data(return_freqs=True)
    mean_psd = psds.mean(axis=0)
    return freqs, 10.0 * np.log10(mean_psd)


def plot_filter_psd_comparison(
    raw_before: mne.io.BaseRaw,
    raw_after: mne.io.BaseRaw,
    *,
    fmin: float = 1.0,
    fmax: float = 80.0,
    title: str | None = None,
):
    """Plot the mean PSD before vs after band-pass filtering as before/after evidence.

    Power spectral density is averaged across EEG channels and shown in dB
    (10·log10 of V²/Hz). The configured low-pass edge is marked so the effect of
    the filter (and the suppression of any high-frequency / line noise) is
    visible.

    Returns
    -------
    matplotlib.figure.Figure
    """
    freqs_b, psd_b = _mean_psd_db(raw_before, fmin=fmin, fmax=fmax)
    freqs_a, psd_a = _mean_psd_db(raw_after, fmin=fmin, fmax=fmax)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(freqs_b, psd_b, color="0.5", linewidth=1.2, label="Before (raw)")
    ax.plot(freqs_a, psd_a, color="C3", linewidth=1.2, label="After (1-40 Hz band-pass, avg ref)")
    ax.axvline(config.FILTER_H_FREQ_HZ, color="C0", linestyle="--", linewidth=0.9,
               label=f"low-pass {config.FILTER_H_FREQ_HZ:.0f} Hz")
    ax.axvline(config.LINE_FREQ_HZ, color="0.7", linestyle=":", linewidth=0.9,
               label=f"line {config.LINE_FREQ_HZ:.0f} Hz")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power spectral density (dB, mean over EEG channels)")
    ax.set_title(title or "PSD before vs after conservative preprocessing")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def plot_epochs_overview(
    epochs: mne.Epochs,
    *,
    picks: Sequence[str] = ("C3", "Cz", "C4"),
    title: str | None = None,
):
    """Plot condition-averaged epoch traces for a few motor-relevant channels.

    For each requested channel, the per-condition average (evoked) is overlaid,
    with a marker at the cue onset (t = 0). This is an *example-epochs* view: a
    cue-locked average over a small sample, shown descriptively (not as an
    established effect).

    Returns
    -------
    matplotlib.figure.Figure
    """
    available = [ch for ch in picks if ch in epochs.ch_names]
    if not available:
        available = epochs.ch_names[:3]
    times = epochs.times
    fig, axes = plt.subplots(1, len(available), figsize=(4.2 * len(available), 4.2), sharey=True)
    if len(available) == 1:
        axes = [axes]
    for ax, ch in zip(axes, available):
        for i, cond in enumerate(epochs.event_id):
            if len(epochs[cond]) == 0:
                continue
            evoked = epochs[cond].average()
            data = evoked.get_data(picks=[ch])[0] * _VOLT_TO_UV
            ax.plot(times, data, color=f"C{i}", linewidth=1.0, label=cond)
        ax.axvline(0.0, color="0.6", linestyle="--", linewidth=0.8)
        ax.set_title(ch)
        ax.set_xlabel("Time (s)")
    axes[0].set_ylabel("Average amplitude (µV)")
    axes[-1].legend(loc="upper right", fontsize=7)
    fig.suptitle(title or "Condition-averaged epochs (cue-locked)")
    fig.tight_layout()
    return fig


def plot_psd_baseline_comparison(
    freqs,
    psd_eyes_open,
    psd_eyes_closed,
    *,
    picks_label: str = "occipital channels",
    shade_band: tuple[float, float] = config.ALPHA_BAND,
    title: str | None = None,
):
    """Plot eyes-open vs eyes-closed PSD curves (dB) with a shaded alpha band.

    The curves are PSDs (V²/Hz) already averaged across the channels of
    interest; they are displayed in dB (10·log10). The shaded band marks the
    alpha range where an eyes-closed power increase is *expected*.

    Returns
    -------
    matplotlib.figure.Figure
    """
    freqs = np.asarray(freqs)
    eo_db = 10.0 * np.log10(np.asarray(psd_eyes_open))
    ec_db = 10.0 * np.log10(np.asarray(psd_eyes_closed))

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axvspan(
        shade_band[0], shade_band[1], color="C2", alpha=0.12,
        label=f"alpha {shade_band[0]:.0f}-{shade_band[1]:.0f} Hz",
    )
    ax.plot(freqs, eo_db, color="C0", linewidth=1.4, label="Eyes open (run 1)")
    ax.plot(freqs, ec_db, color="C3", linewidth=1.4, label="Eyes closed (run 2)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(f"PSD (dB re V²/Hz, mean over {picks_label})")
    ax.set_title(title or "Baseline PSD: eyes-open vs eyes-closed")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    return fig


def plot_band_topomap(
    spectrum,
    *,
    bands: dict | None = None,
    title: str | None = None,
):
    """Plot frequency-band topomaps from an MNE ``Spectrum`` (optional summary).

    Requires a montage on the underlying instance. ``bands`` maps a display name
    to ``(fmin, fmax)``; defaults to alpha and beta.

    Returns
    -------
    matplotlib.figure.Figure
    """
    if bands is None:
        bands = {
            f"Alpha ({config.ALPHA_BAND[0]:.0f}-{config.ALPHA_BAND[1]:.0f} Hz)": config.ALPHA_BAND,
            f"Beta ({config.BETA_BAND[0]:.0f}-{config.BETA_BAND[1]:.0f} Hz)": config.BETA_BAND,
        }
    fig = spectrum.plot_topomap(bands=bands, normalize=True, show=False)
    if title:
        fig.suptitle(title)
    return fig
