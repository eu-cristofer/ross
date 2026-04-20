"""Fourth-order spectrum point estimates (selected slices only)."""

import numpy as np

from ross.hos.segmenting import _segment_signal


def _window(nfft, window):
    if window == "hann" or window == "hanning":
        return np.hanning(nfft)
    if window == "boxcar" or window == "rect":
        return np.ones(nfft)
    raise ValueError(f"Unknown window type: {window!r}")


def _freq_to_bin(f_hz, freqs):
    return int(np.argmin(np.abs(freqs - f_hz)))


def estimate_trispectrum_point(signal, fs, f1_hz, f2_hz, f3_hz, nfft=2048, noverlap=1024, window="hann"):
    """Average trispectrum slice :math:`E[X(f_1)X(f_2)X(f_3)X^*(f_1+f_2+f_3)]`.

    This is a direct fourth-order moment in the frequency domain using the same
    windowed-segment framework as the bispectrum estimator.

    Parameters
    ----------
    signal : ndarray
        Real time series.
    fs : float
        Sample rate (Hz).
    f1_hz, f2_hz, f3_hz : float
        Frequency locations (Hz).
    nfft : int
        FFT length per segment.
    noverlap : int
        Overlap (samples).
    window : str
        ``\"hann\"`` or ``\"boxcar\"``.

    Returns
    -------
    complex
        Mean complex trispectrum value at the requested triplet.
    freqs : ndarray
        FFT frequency bins (for bin lookup).
    """
    signal = np.asarray(signal, dtype=np.float64).ravel()
    win = _window(nfft, window)
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    i1 = _freq_to_bin(f1_hz, freqs)
    i2 = _freq_to_bin(f2_hz, freqs)
    i3 = _freq_to_bin(f3_hz, freqs)
    k = i1 + i2 + i3
    n_bins = nfft // 2 + 1
    if k >= n_bins:
        raise ValueError("f1+f2+f3 exceeds Nyquist for this nfft and fs.")

    acc = 0.0 + 0.0j
    n_seg = 0
    for seg in _segment_signal(signal, nfft, noverlap):
        xw = seg * win
        X = np.fft.rfft(xw, n=nfft)
        acc += X[i1] * X[i2] * X[i3] * np.conj(X[k])
        n_seg += 1
    if n_seg == 0:
        raise ValueError("No segments produced.")
    return acc / n_seg, freqs
