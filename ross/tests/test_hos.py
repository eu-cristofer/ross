import numpy as np

from ross.hos import estimate_bicoherence, estimate_bispectrum, extract_bispectral_peaks


def _quadratic_coupled_signal(fs, duration):
    t = np.arange(0.0, duration, 1.0 / fs)
    f1 = 12.0
    f2 = 20.0
    x = np.sin(2 * np.pi * f1 * t) + 0.8 * np.sin(2 * np.pi * f2 * t)
    x += 0.4 * (np.sin(2 * np.pi * f1 * t) * np.sin(2 * np.pi * f2 * t))
    return t, x


def test_bispectrum_shape_and_frequency_axis():
    fs = 256.0
    _, x = _quadratic_coupled_signal(fs, duration=8.0)
    bspec, freqs = estimate_bispectrum(x, fs=fs, nfft=256, noverlap=128)

    assert bspec.shape == (129, 129)
    assert len(freqs) == 129
    assert freqs[0] == 0.0


def test_bicoherence_bounded():
    fs = 256.0
    _, x = _quadratic_coupled_signal(fs, duration=8.0)
    bic2, _ = estimate_bicoherence(x, fs=fs, nfft=256, noverlap=128)

    assert np.nanmin(bic2) >= 0.0
    assert np.nanmax(bic2) <= 1.0


def test_extract_bispectral_peaks_returns_ranked_entries():
    fs = 256.0
    _, x = _quadratic_coupled_signal(fs, duration=8.0)
    bspec, freqs = estimate_bispectrum(x, fs=fs, nfft=256, noverlap=128)

    peaks = extract_bispectral_peaks(bspec, freqs, top_n=3, min_freq=5.0, max_freq=60.0)
    assert len(peaks) == 3
    assert peaks[0]["magnitude"] >= peaks[1]["magnitude"] >= peaks[2]["magnitude"]
