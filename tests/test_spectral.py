"""Tests for the v0.3 spectral helpers and frequency-band definitions.

These cover the data-free numeric core: the band definitions (contiguous,
non-overlapping, within the analysis band) and the band-power integration,
validated on a synthetic PSD and on a known sine wave.
"""

import numpy as np
import pytest

from eeg_lab import config, spectral


# ---------------------------------------------------------------------------
# Band definitions.
# ---------------------------------------------------------------------------
def test_alpha_and_beta_bands_match_conventions():
    assert config.ALPHA_BAND == (8.0, 13.0)
    assert config.BETA_BAND == (13.0, 30.0)
    assert config.FREQ_BANDS["alpha"] == config.ALPHA_BAND
    assert config.FREQ_BANDS["beta"] == config.BETA_BAND


def test_bands_are_ordered_and_within_analysis_range():
    for name, (lo, hi) in config.FREQ_BANDS.items():
        assert lo < hi, f"band {name} not ordered"
        assert lo >= config.PSD_FMIN_HZ
        assert hi <= config.PSD_FMAX_HZ


def test_bands_are_contiguous_and_non_overlapping():
    edges = list(config.FREQ_BANDS.values())
    for (lo1, hi1), (lo2, hi2) in zip(edges, edges[1:]):
        # Each band starts where the previous ended (contiguous, no overlap/gap).
        assert hi1 == lo2


# ---------------------------------------------------------------------------
# Band-power integration on a synthetic PSD.
# ---------------------------------------------------------------------------
def test_bandpower_of_flat_psd_equals_width():
    # Flat PSD == 1 over 0..40 Hz: integrated power over a band == its width.
    freqs = np.linspace(0, 40, 4001)
    psd = np.ones_like(freqs)
    power = spectral.bandpower_from_psd(freqs, psd, (8.0, 13.0))
    assert power == pytest.approx(5.0, rel=1e-3)


def test_bandpower_empty_band_is_zero():
    freqs = np.linspace(0, 40, 100)
    psd = np.ones_like(freqs)
    # A band above the available range yields zero power.
    assert spectral.bandpower_from_psd(freqs, psd, (100.0, 120.0)) == 0.0


def test_bandpower_supports_multichannel():
    freqs = np.linspace(0, 40, 401)
    psd = np.ones((3, freqs.size))  # 3 channels, flat
    power = spectral.bandpower_from_psd(freqs, psd, (8.0, 13.0))
    assert power.shape == (3,)
    np.testing.assert_allclose(power, 5.0, rtol=1e-3)


def test_relative_bandpower_fraction_of_total():
    freqs = np.linspace(1, 40, 3901)
    psd = np.ones_like(freqs)
    rel = spectral.relative_bandpower(freqs, psd, (8.0, 13.0))
    # 5 Hz alpha out of the 39 Hz total (1-40 Hz).
    assert rel == pytest.approx(5.0 / 39.0, rel=1e-2)


# ---------------------------------------------------------------------------
# Band power on a known sine wave: power concentrates in the sine's band.
# ---------------------------------------------------------------------------
def test_sine_power_concentrates_in_its_band():
    sfreq = 160.0
    t = np.arange(0, 20.0, 1.0 / sfreq)
    sine = np.sin(2 * np.pi * 10.0 * t)  # 10 Hz -> alpha band

    alpha = spectral.bandpower_signal(sine, sfreq, config.ALPHA_BAND)
    beta = spectral.bandpower_signal(sine, sfreq, config.BETA_BAND)
    delta = spectral.bandpower_signal(sine, sfreq, config.FREQ_BANDS["delta"])

    assert alpha > beta
    assert alpha > delta
    # The 10 Hz line dominates: alpha holds the vast majority of in-range power.
    assert alpha > 10 * beta


def test_grand_average_psd_mean():
    curves = [np.array([1.0, 2.0, 3.0]), np.array([3.0, 4.0, 5.0])]
    np.testing.assert_allclose(
        spectral.grand_average_psd(curves), np.array([2.0, 3.0, 4.0])
    )
