"""Higher-order spectral (HOS) estimators for rotor fault diagnosis.

Normalization convention
------------------------
Bicoherence squared b²(f_l, f_m) follows Kim & Powers (1979):

    b²(f_l, f_m) = |B(f_l, f_m)|² / (⟨|X(f_l) X(f_m)|²⟩ · ⟨|X(f_l+f_m)|²⟩)

where angle brackets denote segment averaging over K records.  This normalization
bounds b² in [0, 1] by the Cauchy–Schwarz inequality (Kim & Powers, 1979,
IEEE Trans. Plasma Sci. 7(2), 120–131).

HOS definitions (Sinha, 2007, Eqs. 2–3)
-----------------------------------------
Bispectrum:
    B_xxx(f_l, f_m) = E[X(f_l) X(f_m) X*(f_l + f_m)],   l + m ≤ N

Trispectrum:
    T_xxxx(f_l, f_m, f_n) = E[X*(f_l) X*(f_m) X*(f_n) X(f_l + f_m + f_n)]

The estimator is the direct (segment-averaging) method described in
Collis, White & Hammond (1998), MSSP 12(3), 375–394.

Non-redundant region
--------------------
Only bins satisfying f_l ≤ f_m (bispectrum) or f_l ≤ f_m ≤ f_n (trispectrum)
and f_l + f_m [+ f_n] ≤ Nyquist are computed; all other entries are zero.

Sinha §3.3 defaults (imported from constants.py)
-------------------------------------------------
``bispectrum`` / ``trispectrum`` default to:
    nfft     = int(fs / SINHA_HOS_DF_HZ)   = 2048   at fs = 2560 Hz
    noverlap = int(nfft * SINHA_HOS_OVERLAP) = 1024
yielding Δf = 1.25 Hz and 50 segments for a 25 s record.

References
----------
Kim, Y. C., & Powers, E. J. (1979). Digital bispectral analysis and its
    applications to nonlinear wave interactions. *IEEE Transactions on Plasma
    Science*, 7(2), 120–131.
Sinha, J. K. (2007). Higher order spectra for crack and misalignment
    identification in the shaft of a rotating machine. *Structural Health
    Monitoring*, 6(4), 325–334.
Collis, W. B., White, P. R., & Hammond, J. K. (1998). Higher-order spectra:
    the bispectrum and trispectrum. *Mechanical Systems and Signal Processing*,
    12(3), 375–394.
"""

import numpy as np
from scipy.signal import detrend as _detrend, get_window, welch, butter, filtfilt


def _defaults(fs, nfft, noverlap):
    """Return (nfft, noverlap) filled from Sinha §3.3 constants when None."""
    from constants import SINHA_HOS_DF_HZ, SINHA_HOS_OVERLAP
    if nfft is None:
        nfft = int(round(fs / SINHA_HOS_DF_HZ))
    if noverlap is None:
        noverlap = int(round(nfft * SINHA_HOS_OVERLAP))
    return nfft, noverlap


def _segment(x, nfft, noverlap):
    """Split x into overlapping blocks of length nfft."""
    step = nfft - noverlap
    return [x[i : i + nfft] for i in range(0, len(x) - nfft + 1, step)]


def window_and_detrend(x: np.ndarray, window: str = "hann") -> tuple:
    """Detrend (constant) then apply a window.

    Returns
    -------
    xw : np.ndarray  windowed signal
    w  : np.ndarray  the window array (for amplitude correction downstream)
    """
    xd = _detrend(x, type="constant")
    w = get_window(window, len(x))
    return xd * w, w


def amplitude_spectrum(x, fs, window="hann") -> tuple:
    """Single-sided Hann-corrected amplitude spectrum.

    Correction factor: 2 * |rfft(xw)| / sum(w).
    Rectangular window (``"boxcar"``) collapses to the familiar 2/N.

    Returns
    -------
    amp   : ndarray  single-sided amplitude (peak), shape (nfft//2 + 1,)
    freqs : ndarray  frequency axis in Hz
    """
    xw, w = window_and_detrend(x, window=window)
    N = len(x)
    X = np.fft.rfft(xw)
    amp = 2.0 * np.abs(X) / w.sum()
    amp[0] /= 2.0
    if N % 2 == 0:
        amp[-1] /= 2.0
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    return amp, freqs


def psd_welch(x, fs, nperseg, noverlap, window="hann"):
    """Thin wrapper around ``scipy.signal.welch`` with sensible defaults.

    Returns
    -------
    freqs : ndarray  frequency axis in Hz
    Pxx   : ndarray  one-sided power spectral density
    """
    freqs, Pxx = welch(
        x,
        fs=fs,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        return_onesided=True,
    )
    return freqs, Pxx


def bispectrum(x, fs, nfft=None, noverlap=None, window="hann") -> tuple:
    """Kim–Powers normalized bispectrum via segment averaging (direct method).

    Returns
    -------
    B     : complex ndarray, shape (nf, nf)  raw B_xxx(f_l, f_m); zero outside
            the non-redundant region f_l ≤ f_m, f_l + f_m ≤ Nyquist.
    b2    : real ndarray,    shape (nf, nf)  bicoherence squared in [0, 1]
    freqs : ndarray,         shape (nf,)     single-sided Hz axis

    Notes
    -----
    The FFT is hoisted to once per segment.  Segment averaging accumulates
    ``B``, ``⟨|X(f_l) X(f_m)|²⟩``, and ``⟨|X(f_l+f_m)|²⟩`` in a single pass
    so bicoherence is computed without a second pass.

    NaN / small-denominator guard: denominator values < 1e-30 are replaced
    with 1e-30 before division; b² cannot go negative.
    """
    nfft, noverlap = _defaults(fs, nfft, noverlap)
    segs = _segment(x, nfft, noverlap)
    K = len(segs)
    if K == 0:
        raise ValueError(
            f"Signal too short for bispectrum: need ≥{nfft} samples, got {len(x)}."
        )

    nf = nfft // 2 + 1

    # Non-redundant index pairs: l <= m and l+m < nf
    rows, cols = np.triu_indices(nf, k=0)
    lm_sum = rows + cols
    valid = lm_sum < nf
    rows, cols, lm_sum = rows[valid], cols[valid], lm_sum[valid]

    B_acc = np.zeros(len(rows), dtype=complex)
    P12_acc = np.zeros(len(rows))
    P3_acc = np.zeros(len(rows))

    for seg in segs:
        xw, _ = window_and_detrend(seg, window=window)
        X = np.fft.rfft(xw, n=nfft)
        Xl_Xm = X[rows] * X[cols]
        Xlm = X[lm_sum]
        B_acc += Xl_Xm * np.conj(Xlm)
        P12_acc += np.abs(Xl_Xm) ** 2
        P3_acc += np.abs(Xlm) ** 2

    B_flat = B_acc / K
    denom = np.maximum((P12_acc / K) * (P3_acc / K), 1e-30)
    b2_flat = np.abs(B_flat) ** 2 / denom

    B = np.zeros((nf, nf), dtype=complex)
    b2 = np.zeros((nf, nf))
    B[rows, cols] = B_flat
    b2[rows, cols] = np.clip(b2_flat, 0.0, 1.0)

    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    return B, b2, freqs


def bicoherence(x, fs, nfft=None, noverlap=None, window="hann") -> tuple:
    """Convenience alias: returns ``(b2, freqs)`` from :func:`bispectrum`."""
    _, b2, freqs = bispectrum(x, fs, nfft=nfft, noverlap=noverlap, window=window)
    return b2, freqs


def trispectrum(
    x,
    fs,
    nfft=None,
    noverlap=None,
    window="hann",
    threshold: float = 0.10,
    fmax_hz: float = None,
) -> tuple:
    """Sparse tri-spectrum estimator (Kim–Powers normalized).

    Returns the dict ``{(l, m, n): T_xxxx_lmn}`` for entries where
    ``|T| / max|T| >= threshold`` and ``l + m + n < Nyquist bin``.
    Sparse by design so O(N³) storage does not blow up.

    Matches Sinha's "amplitudes above 0.1 plotted" convention (Figs. 7–8).

    Parameters
    ----------
    fmax_hz : float or None
        Upper frequency limit for each individual index (Hz).
        Defaults to ``min(fs / 6, 200.0)`` so that l + m + n ≤ Nyquist is
        always satisfied and the index space remains tractable.

    Returns
    -------
    T_dict : dict  ``{(l, m, n): complex}``
    freqs  : ndarray  single-sided Hz axis
    """
    nfft, noverlap = _defaults(fs, nfft, noverlap)
    segs = _segment(x, nfft, noverlap)
    K = len(segs)
    if K == 0:
        raise ValueError(
            f"Signal too short for trispectrum: need ≥{nfft} samples, got {len(x)}."
        )

    nf = nfft // 2 + 1
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)

    if fmax_hz is None:
        fmax_hz = min(fs / 6.0, 200.0)
    nf_max = min(int(fmax_hz * nfft / fs) + 1, nf // 3 + 1)

    # Non-redundant: l <= m <= n and l+m+n < nf
    ls, ms, ns = np.mgrid[0:nf_max, 0:nf_max, 0:nf_max]
    ls, ms, ns = ls.ravel(), ms.ravel(), ns.ravel()
    mask = (ls <= ms) & (ms <= ns) & ((ls + ms + ns) < nf)
    ls, ms, ns = ls[mask], ms[mask], ns[mask]
    lmn_sum = ls + ms + ns

    T_acc = np.zeros(len(ls), dtype=complex)

    for seg in segs:
        xw, _ = window_and_detrend(seg, window=window)
        X = np.fft.rfft(xw, n=nfft)
        T_acc += np.conj(X[ls]) * np.conj(X[ms]) * np.conj(X[ns]) * X[lmn_sum]

    T_mean = T_acc / K
    T_abs = np.abs(T_mean)
    T_max = T_abs.max() if T_abs.max() > 0.0 else 1.0

    keep = (T_abs / T_max) >= threshold
    T_dict = {
        (int(ls[i]), int(ms[i]), int(ns[i])): T_mean[i]
        for i in np.where(keep)[0]
    }
    return T_dict, freqs


def harmonic_amplitude(x, fs, f_target, window="hann") -> float:
    """Hann-corrected peak amplitude at ``f_target`` via parabolic interpolation.

    Fits a parabola through the 3 nearest bins of the amplitude spectrum and
    returns the interpolated peak value.  Replaces the nearest-bin ``argmin``
    helper previously duplicated in notebooks 02 and 03.
    """
    amp, freqs = amplitude_spectrum(x, fs, window=window)
    i0 = int(np.argmin(np.abs(freqs - f_target)))
    if 0 < i0 < len(amp) - 1:
        alpha, beta, gamma = amp[i0 - 1], amp[i0], amp[i0 + 1]
        denom = alpha - 2.0 * beta + gamma
        if abs(denom) > 1e-30:
            delta = 0.5 * (alpha - gamma) / denom
            return beta - 0.25 * (alpha - gamma) * delta
    return float(amp[i0])


def downsample_to(x, fs_sim: float, fs_out: float, aa_cutoff_hz: float) -> np.ndarray:
    """Low-pass filter then decimate to ``fs_out``.

    Butterworth order-8 zero-phase filtfilt at ``aa_cutoff_hz``, followed by
    integer decimation.  Lives here (not campaign.py) so Sprint 04 can apply
    it to 10 kHz Newmark-β output.
    """
    b, a = butter(8, aa_cutoff_hz / (fs_sim / 2.0), btype="low")
    x_filt = filtfilt(b, a, x)
    factor = int(round(fs_sim / fs_out))
    return x_filt[::factor]


def add_awgn(x, snr_db: float, rng=None) -> np.ndarray:
    """Add white Gaussian noise to achieve target SNR in dB.

    Parameters
    ----------
    snr_db : float
        Target signal-to-noise ratio (Sinha §5: SNR_DB = 40).
    rng : np.random.Generator or None
        Pass a seeded generator for reproducibility.
    """
    if rng is None:
        rng = np.random.default_rng()
    sig_power = np.mean(x ** 2)
    noise_power = sig_power / (10.0 ** (snr_db / 10.0))
    return x + rng.standard_normal(len(x)) * np.sqrt(noise_power)
