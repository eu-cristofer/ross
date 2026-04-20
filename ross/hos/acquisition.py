"""Acquisition-style post-processing (filtering, decimation, noise)."""

import numpy as np
from scipy import signal


def lowpass_filter_zero_phase(x, fs, cutoff_hz, order=8):
    """Butterworth low-pass applied forward and backward (zero phase).

    Parameters
    ----------
    x : ndarray
        Uniformly sampled signal.
    fs : float
        Sample rate (Hz).
    cutoff_hz : float
        Pass-band edge (Hz).
    order : int
        Filter order (each direction uses ``order`` in ``filtfilt``).

    Returns
    -------
    ndarray
        Filtered signal same shape as ``x``.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    nyq = 0.5 * fs
    wn = min(cutoff_hz / nyq, 0.99)
    b, a = signal.butter(order, wn, btype="low")
    return signal.filtfilt(b, a, x)


def decimate_mean(x, factor):
    """Average ``factor`` consecutive samples (FIR decimation, no IIR).

    Parameters
    ----------
    x : ndarray
        Input samples.
    factor : int
        Block size; output length is ``len(x) // factor``.

    Returns
    -------
    ndarray
        Decimated sequence at ``fs / factor``.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    n = (x.size // factor) * factor
    if n == 0:
        raise ValueError("Signal too short for decimation factor.")
    return x[:n].reshape(-1, factor).mean(axis=1)


def add_gaussian_noise_snr(x, snr_db, seed=None):
    """Add zero-mean Gaussian noise to achieve approximate SNR in dB (power ratio).

    SNR here is ``10 * log10(signal_power / noise_power)`` using the
    variance of ``x`` as signal power reference.

    Parameters
    ----------
    x : ndarray
        Clean signal.
    snr_db : float
        Target SNR in decibels.
    seed : int, optional
        RNG seed for reproducibility.

    Returns
    -------
    ndarray
        Noisy signal.
    """
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=np.float64).ravel()
    sig_pow = np.mean(x**2) + 1e-30
    noise_pow = sig_pow / (10 ** (snr_db / 10.0))
    noise = rng.normal(0.0, np.sqrt(noise_pow), size=x.shape)
    return x + noise


def sinha_acquisition_chain(x, fs_in, lp_hz=1000.0, decimate_factor=10, snr_db=40.0, seed=None):
    """Low-pass, decimate by block average, then add Gaussian noise (Sinha-style chain).

    Sinha (2007) describes LP filtering near 1 kHz, decimation by 10, and noise
    injection to 40 dB SNR on synthetic traces. This function applies that chain
    in a fixed order; the caller documents physical interpretation of ``fs_in``.

    Parameters
    ----------
    x : ndarray
        Input waveform at ``fs_in``.
    fs_in : float
        Input sample rate (Hz).
    lp_hz : float
        Low-pass corner (Hz).
    decimate_factor : int
        Block averaging decimation factor.
    snr_db : float
        Target SNR after decimation.
    seed : int, optional
        Noise RNG seed.

    Returns
    -------
    y : ndarray
        Processed signal.
    fs_out : float
        ``fs_in / decimate_factor``.
    """
    y = lowpass_filter_zero_phase(x, fs_in, lp_hz)
    y = decimate_mean(y, decimate_factor)
    fs_out = fs_in / decimate_factor
    y = add_gaussian_noise_snr(y, snr_db, seed=seed)
    return y, fs_out
