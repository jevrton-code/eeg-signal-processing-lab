"""Spectral analysis helpers: PSD computation and frequency-band power.

Responsibility
--------------
Provide small, mostly-pure helpers for power-spectral-density (PSD) analysis and
band-power integration, used for the eyes-open vs eyes-closed baseline
comparison and the optional alpha/beta band summaries. The numeric core
(:func:`bandpower_from_psd`) is data-free and unit-tested; the MNE-facing
wrappers compute PSDs from ``Raw``/``Epochs`` objects.

Conventions
-----------
- PSD is computed with Welch's method over a stated frequency range
  (default 1-40 Hz, the analysis band).
- Band definitions live in :data:`eeg_lab.config.FREQ_BANDS`.
- Power is integrated over a band with the trapezoidal rule.

Status
------
Version 0.3 (frequency-analysis stage).
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from . import config

# np.trapz was renamed to np.trapezoid in NumPy 2.0 (np.trapz now deprecated).
_trapezoid = getattr(np, "trapezoid", None) or np.trapz


def bandpower_from_psd(freqs, psd, band: tuple[float, float]):
    """Integrate a PSD over a frequency band (trapezoidal rule). Pure numeric.

    Parameters
    ----------
    freqs
        1-D array of frequency-bin centers (Hz), ascending.
    psd
        PSD values whose **last axis** matches ``freqs``. May be 1-D (one
        spectrum) or N-D (e.g. ``(n_channels, n_freqs)``).
    band
        ``(low, high)`` band edges in Hz (inclusive).

    Returns
    -------
    float or numpy.ndarray
        Integrated power over the band. Scalar for a 1-D ``psd``, otherwise an
        array over the leading axes. Returns zeros if no bin falls in the band.
    """
    freqs = np.asarray(freqs, dtype=float)
    psd = np.asarray(psd, dtype=float)
    low, high = band
    mask = (freqs >= low) & (freqs <= high)
    if not mask.any():
        out = np.zeros(psd.shape[:-1])
        return float(out) if out.ndim == 0 else out
    power = _trapezoid(psd[..., mask], freqs[mask], axis=-1)
    return float(power) if np.ndim(power) == 0 else power


def relative_bandpower(freqs, psd, band: tuple[float, float], *, total_band=None):
    """Return band power as a fraction of the total power over ``total_band``.

    ``total_band`` defaults to the full ``(freqs[0], freqs[-1])`` range. Pure.
    """
    freqs = np.asarray(freqs, dtype=float)
    if total_band is None:
        total_band = (float(freqs[0]), float(freqs[-1]))
    band_p = bandpower_from_psd(freqs, psd, band)
    total_p = bandpower_from_psd(freqs, psd, total_band)
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.where(total_p > 0, band_p / total_p, 0.0)
    return float(rel) if np.ndim(rel) == 0 else rel


def bandpower_signal(
    signal,
    sfreq: float,
    band: tuple[float, float],
    *,
    nperseg: int | None = None,
):
    """Welch band power of a 1-D time-domain signal (uses SciPy). Mostly pure.

    Provided primarily so band-power logic can be validated on synthetic signals
    (e.g. a known sine concentrates power in its band).
    """
    from scipy.signal import welch

    signal = np.asarray(signal, dtype=float)
    if nperseg is None:
        nperseg = min(len(signal), 1024)
    freqs, psd = welch(signal, fs=sfreq, nperseg=nperseg)
    return bandpower_from_psd(freqs, psd, band)


def compute_psd(
    inst,
    *,
    fmin: float = config.PSD_FMIN_HZ,
    fmax: float = config.PSD_FMAX_HZ,
    picks="eeg",
    method: str = "welch",
    verbose: bool = False,
):
    """Compute a Welch PSD ``Spectrum`` for a ``Raw``/``Epochs`` instance.

    Thin wrapper over MNE's ``compute_psd`` with the project's default range.
    """
    return inst.compute_psd(
        method=method, fmin=fmin, fmax=fmax, picks=picks, verbose=verbose
    )


def average_psd(
    inst,
    *,
    picks="eeg",
    fmin: float = config.PSD_FMIN_HZ,
    fmax: float = config.PSD_FMAX_HZ,
    verbose: bool = False,
):
    """Return ``(freqs, mean_psd)`` averaged over the selected channels.

    ``mean_psd`` is the per-frequency mean of the PSD across the picked channels
    (absolute units, V²/Hz). Useful for grand-averaging across subjects on a
    fixed frequency grid.
    """
    spectrum = inst.compute_psd(
        method="welch", fmin=fmin, fmax=fmax, picks=picks, verbose=verbose
    )
    psds, freqs = spectrum.get_data(return_freqs=True)
    return freqs, psds.mean(axis=0)


def grand_average_psd(curves: Sequence[np.ndarray]) -> np.ndarray:
    """Average a sequence of per-subject PSD arrays sharing a frequency grid.

    All arrays must have the same length (same ``fmin``/``fmax`` and sampling
    give an identical Welch grid for these equal-length recordings). Pure.
    """
    stacked = np.vstack([np.asarray(c, dtype=float) for c in curves])
    return stacked.mean(axis=0)
