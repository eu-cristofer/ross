"""Tests for higher-order spectral estimators (ross.hos)."""

import numpy as np

from ross.hos.acquisition import decimate_mean, sinha_acquisition_chain
from ross.hos.bispectrum import (
    estimate_bicoherence,
    estimate_bispectrum,
    extract_bispectral_peaks,
)
from ross.hos.trispectrum import estimate_trispectrum_point


def _qpc_signal(t, f1, f2, coupled=True, rng=None):
    """Two fundamentals plus sum tone; phase coupling when ``coupled`` is True."""
    w1, w2 = 2 * np.pi * f1, 2 * np.pi * f2
    if coupled:
        return (
            np.cos(w1 * t)
            + np.cos(w2 * t)
            + 0.55 * np.cos((w1 + w2) * t)
        )
    rng = rng or np.random.default_rng(0)
    p1, p2, p3 = rng.uniform(0, 2 * np.pi, size=3)
    return (
        np.cos(w1 * t + p1)
        + np.cos(w2 * t + p2)
        + 0.55 * np.cos((w1 + w2) * t + p3)
    )


def test_bispectrum_qpc_peak_coupled_vs_partial():
    """Phase-locked sum tone yields larger |B(f1,f2)| than two fundamentals alone."""
    fs = 2000.0
    f1, f2 = 30.0, 50.0
    t = np.arange(0.0, 20.0, 1.0 / fs)
    w1, w2 = 2 * np.pi * f1, 2 * np.pi * f2
    x_c = _qpc_signal(t, f1, f2, coupled=True)
    x_partial = np.cos(w1 * t) + np.cos(w2 * t)

    nfft, noverlap = 512, 256
    Bc, freqs = estimate_bispectrum(x_c, fs, nfft=nfft, noverlap=noverlap)
    Bp, _ = estimate_bispectrum(x_partial, fs, nfft=nfft, noverlap=noverlap)

    i1 = int(np.argmin(np.abs(freqs - f1)))
    i2 = int(np.argmin(np.abs(freqs - f2)))
    mc = np.abs(Bc[i1, i2])
    mp = np.abs(Bp[i1, i2])
    assert mc > 3.0 * max(mp, 1e-12), (mc, mp)


def test_bicoherence_bounded():
    fs = 1000.0
    t = np.arange(0.0, 8.0, 1.0 / fs)
    x = _qpc_signal(t, 35.0, 55.0, coupled=True)
    bic2, freqs = estimate_bicoherence(x, fs, nfft=256, noverlap=128, eps=1e-12)
    bic2 = np.nan_to_num(bic2, nan=0.0, posinf=0.0, neginf=0.0)
    assert np.nanmax(bic2) < 1.0 + 0.05
    assert np.nanmin(bic2) >= -1e-9


def test_extract_bispectral_peaks_orders_by_magnitude():
    fs = 800.0
    f1, f2 = 25.0, 40.0
    t = np.arange(0.0, 12.0, 1.0 / fs)
    x = _qpc_signal(t, f1, f2, coupled=True)
    B, freqs = estimate_bispectrum(x, fs, nfft=512, noverlap=256)
    peaks = extract_bispectral_peaks(B, freqs, top_n=12, min_freq=5.0, max_freq=200.0)
    assert len(peaks) >= 1
    df = float(freqs[1] - freqs[0])
    tol = 3.0 * df

    def near_pair(p, a, b):
        return abs(p["f1_hz"] - a) < tol and abs(p["f2_hz"] - b) < tol

    assert any(near_pair(p, f1, f2) or near_pair(p, f2, f1) for p in peaks)


def test_trispectrum_point_finite():
    fs = 1200.0
    t = np.arange(0.0, 6.0, 1.0 / fs)
    x = _qpc_signal(t, 35.0, 45.0, coupled=True)
    T, freqs = estimate_trispectrum_point(x, fs, 35.0, 35.0, 35.0, nfft=256, noverlap=128)
    assert np.isfinite(T.real) and np.isfinite(T.imag)


def test_decimate_mean_and_chain_shape():
    fs = 2000.0
    t = np.arange(0.0, 1.0, 1.0 / fs)
    x = np.sin(2 * np.pi * 50.0 * t)
    y = decimate_mean(x, 10)
    assert y.shape[0] == x.shape[0] // 10
    z, fs_out = sinha_acquisition_chain(x, fs_in=fs, lp_hz=500.0, decimate_factor=10, snr_db=30.0, seed=0)
    assert fs_out == 200.0
    assert z.shape[0] == y.shape[0]
