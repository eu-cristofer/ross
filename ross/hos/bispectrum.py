"""Direct bispectrum and bicoherence via segment-averaged periodograms."""

import numpy as np

from ross.hos.segmenting import _segment_signal


def _window(nfft, window):
    if window == "hann" or window == "hanning":
        w = np.hanning(nfft)
    elif window == "boxcar" or window == "rect":
        w = np.ones(nfft)
    else:
        raise ValueError(f"Unknown window type: {window!r}")
    return w


def estimate_bispectrum(signal, fs, nfft=2048, noverlap=1024, window="hann"):
    """Estimate the mean bispectrum using overlapped windowed segments.

    For each segment, compute the short-time rFFT ``X[k]`` and accumulate

    .. math::

        B[k_1, k_2] = \\mathbb{E}\\left[ X[k_1] X[k_2] X^*(k_1+k_2) \\right]

    using the direct method (Nikias & Petropulu, 1993).

    Parameters
    ----------
    signal : ndarray
        Real-valued uniformly sampled time series.
    fs : float
        Sample rate (Hz).
    nfft : int
        FFT length per segment.
    noverlap : int
        Overlap length in samples.
    window : str
        ``\"hann\"`` or ``\"boxcar\"``.

    Returns
    -------
    B : ndarray, complex
        Bispectrum grid with axes corresponding to ``freqs``.
    freqs : ndarray
        Non-negative frequency bins (Hz), length ``nfft // 2 + 1``.
    """
    signal = np.asarray(signal, dtype=np.float64).ravel()
    win = _window(nfft, window)

    n_bins = nfft // 2 + 1
    acc_b = np.zeros((n_bins, n_bins), dtype=np.complex128)
    n_seg = 0
    for seg in _segment_signal(signal, nfft, noverlap):
        xw = seg * win
        X = np.fft.rfft(xw, n=nfft)
        for i in range(n_bins):
            j = np.arange(n_bins - i)
            acc_b[i, j] += X[i] * X[j] * np.conj(X[i + j])
        n_seg += 1
    if n_seg == 0:
        raise ValueError("No segments produced; check signal length, nfft, and noverlap.")
    B = acc_b / n_seg
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    return B, freqs


def estimate_bicoherence(signal, fs, nfft=2048, noverlap=1024, window="hann", eps=1e-18):
    """Estimate squared bicoherence from the same segment ensemble.

    .. math::

        b^2(f_1, f_2) = \\frac{|B(f_1,f_2)|^2}{P(f_1) P(f_2) P(f_1+f_2)}

    where ``P`` is the one-sided power spectrum averaged across segments
    (window-normalized periodogram mean).

    Parameters
    ----------
    signal : ndarray
        Real-valued time series.
    fs : float
        Sample rate (Hz).
    nfft : int
        FFT length.
    noverlap : int
        Overlap in samples.
    window : str
        Window name passed to :func:`estimate_bispectrum`.
    eps : float
        Numerical floor in the denominator.

    Returns
    -------
    bic2 : ndarray, float
        Squared bicoherence in ``[0, 1]`` (values may slightly exceed 1 numerically).
    freqs : ndarray
        Frequency axis (Hz).
    """
    signal = np.asarray(signal, dtype=np.float64).ravel()
    win = _window(nfft, window)

    n_bins = nfft // 2 + 1
    acc_b = np.zeros((n_bins, n_bins), dtype=np.complex128)
    acc_p = np.zeros(n_bins, dtype=np.float64)
    n_seg = 0
    for seg in _segment_signal(signal, nfft, noverlap):
        xw = seg * win
        X = np.fft.rfft(xw, n=nfft)
        acc_p += np.abs(X) ** 2
        for i in range(n_bins):
            j = np.arange(n_bins - i)
            acc_b[i, j] += X[i] * X[j] * np.conj(X[i + j])
        n_seg += 1
    if n_seg == 0:
        raise ValueError("No segments produced; check signal length, nfft, and noverlap.")
    B = acc_b / n_seg
    Pmean = acc_p / n_seg
    p_floor = max(eps, float(np.percentile(Pmean, 5)))
    Pmean = np.maximum(Pmean, p_floor)
    den = np.full((n_bins, n_bins), np.inf, dtype=np.float64)
    for i in range(n_bins):
        for j in range(n_bins):
            k = i + j
            if k < n_bins:
                den[i, j] = Pmean[i] * Pmean[j] * Pmean[k] + eps
    bic2 = (np.abs(B) ** 2) / den
    bic2 = np.nan_to_num(bic2, nan=0.0, posinf=0.0, neginf=0.0)
    bic2 = np.clip(np.real(bic2), 0.0, None)
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    return bic2, freqs


def extract_bispectral_peaks(B, freqs, top_n=5, min_freq=0.0, max_freq=None, principal_domain=True):
    """Return the largest magnitude peaks as ``(f1, f2)`` pairs.

    Parameters
    ----------
    B : ndarray
        Complex bispectrum (or bicoherence; magnitude used).
    freqs : ndarray
        1-D frequency grid matching bispectrum axes.
    top_n : int
        Number of peaks to return.
    min_freq : float
        Ignore bins below this frequency (Hz).
    max_freq : float or None
        Upper frequency bound (Hz); default ``freqs.max()``.
    principal_domain : bool
        If True, only search indices with ``f2 <= f1`` and ``f1 + f2 <= freqs[-1]``.

    Returns
    -------
    list of dict
        Each dict has keys ``f1_hz``, ``f2_hz``, ``magnitude`` (|B|).
    """
    B = np.asarray(B)
    freqs = np.asarray(freqs, dtype=np.float64)
    if max_freq is None:
        max_freq = float(freqs[-1])
    mag = np.abs(B)
    candidates = []
    n = mag.shape[0]
    for i in range(n):
        f1 = freqs[i]
        if f1 < min_freq or f1 > max_freq:
            continue
        for j in range(n):
            f2 = freqs[j]
            if f2 < min_freq or f2 > max_freq:
                continue
            if principal_domain and (f2 > f1 or f1 + f2 > freqs[-1] + 1e-9):
                continue
            k = i + j
            if k >= n:
                continue
            candidates.append((mag[i, j], i, j, f1, f2))
    candidates.sort(key=lambda t: t[0], reverse=True)
    out = []
    seen = set()
    for magv, i, j, f1, f2 in candidates:
        key = (round(f1, 6), round(f2, 6))
        if key in seen:
            continue
        seen.add(key)
        out.append({"f1_hz": float(f1), "f2_hz": float(f2), "magnitude": float(magv)})
        if len(out) >= top_n:
            break
    return out
