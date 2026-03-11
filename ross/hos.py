"""Higher-order spectra helpers for rotating machinery signals."""

import numpy as np
from scipy.signal import detrend


def _segment_signal(x, nfft, noverlap):
    """Split a 1D signal into overlapping segments."""
    step = nfft - noverlap
    if step <= 0:
        raise ValueError("nfft must be greater than noverlap.")
    if len(x) < nfft:
        raise ValueError("Signal length must be at least nfft.")

    segments = []
    for i in range(0, len(x) - nfft + 1, step):
        segments.append(x[i : i + nfft])
    return np.asarray(segments)


def estimate_bispectrum(signal, fs, nfft=256, noverlap=128):
    """Estimate bispectrum by direct FFT averaging.

    Parameters
    ----------
    signal : array_like
        Real-valued time series.
    fs : float
        Sampling frequency (Hz).
    nfft : int, optional
        FFT size per segment. Default is 256.
    noverlap : int, optional
        Segment overlap. Default is 128.

    Returns
    -------
    B : ndarray
        Complex bispectrum estimate in the principal domain.
    freqs : ndarray
        Frequency vector in Hz for rows/columns of `B`.
    """
    x = np.asarray(signal, dtype=float)
    x = detrend(x)
    segments = _segment_signal(x, nfft=nfft, noverlap=noverlap)

    win = np.hanning(nfft)
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    nf = len(freqs)

    bspec = np.zeros((nf, nf), dtype=complex)
    nseg = len(segments)
    for seg in segments:
        segw = seg * win
        xfft = np.fft.rfft(segw)
        for f1 in range(nf):
            for f2 in range(nf):
                f3 = f1 + f2
                if f3 < nf:
                    bspec[f1, f2] += xfft[f1] * xfft[f2] * np.conj(xfft[f3])

    bspec /= nseg
    return bspec, freqs


def estimate_bicoherence(signal, fs, nfft=256, noverlap=128):
    """Estimate squared bicoherence from segmented FFT averages.

    Parameters
    ----------
    signal : array_like
        Real-valued time series.
    fs : float
        Sampling frequency (Hz).
    nfft : int, optional
        FFT size per segment. Default is 256.
    noverlap : int, optional
        Segment overlap. Default is 128.

    Returns
    -------
    bic2 : ndarray
        Squared bicoherence map in [0, 1] where defined.
    freqs : ndarray
        Frequency vector in Hz for rows/columns of `bic2`.
    """
    x = np.asarray(signal, dtype=float)
    x = detrend(x)
    segments = _segment_signal(x, nfft=nfft, noverlap=noverlap)

    win = np.hanning(nfft)
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    nf = len(freqs)

    numerator = np.zeros((nf, nf), dtype=complex)
    p12 = np.zeros((nf, nf), dtype=float)
    p3 = np.zeros((nf, nf), dtype=float)

    for seg in segments:
        segw = seg * win
        xfft = np.fft.rfft(segw)
        for f1 in range(nf):
            for f2 in range(nf):
                f3 = f1 + f2
                if f3 < nf:
                    triple = xfft[f1] * xfft[f2] * np.conj(xfft[f3])
                    numerator[f1, f2] += triple
                    p12[f1, f2] += np.abs(xfft[f1] * xfft[f2]) ** 2
                    p3[f1, f2] += np.abs(xfft[f3]) ** 2

    num = np.abs(numerator) ** 2
    den = p12 * p3
    bic2 = np.zeros_like(num)
    mask = den > 1e-20
    bic2[mask] = num[mask] / den[mask]
    bic2 = np.clip(bic2, 0.0, 1.0)
    return bic2, freqs


def extract_bispectral_peaks(bispectrum, freqs, top_n=3, min_freq=0.0, max_freq=None):
    """Extract top bispectrum magnitude peaks and their frequency coordinates.

    Parameters
    ----------
    bispectrum : ndarray
        Complex bispectrum matrix.
    freqs : ndarray
        Frequency axis in Hz.
    top_n : int, optional
        Number of peaks to return. Default is 3.
    min_freq : float, optional
        Minimum frequency to consider. Default is 0.0.
    max_freq : float, optional
        Maximum frequency to consider. If None, uses maximum available.

    Returns
    -------
    peaks : list of dict
        List of dictionaries containing f1_hz, f2_hz, and magnitude.
    """
    max_freq = float(freqs[-1]) if max_freq is None else max_freq
    mag = np.abs(bispectrum)
    candidates = []

    for i, f1 in enumerate(freqs):
        if f1 < min_freq or f1 > max_freq:
            continue
        for j, f2 in enumerate(freqs):
            if f2 < min_freq or f2 > max_freq:
                continue
            if i + j >= len(freqs):
                continue
            candidates.append((mag[i, j], f1, f2))

    candidates.sort(key=lambda x: x[0], reverse=True)
    peaks = []
    for m, f1, f2 in candidates[:top_n]:
        peaks.append({"f1_hz": float(f1), "f2_hz": float(f2), "magnitude": float(m)})
    return peaks
