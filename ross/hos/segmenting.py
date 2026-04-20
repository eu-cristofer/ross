"""Overlapped window segmentation for HOS estimators."""

import numpy as np


def _segment_signal(x, nfft, noverlap):
    """Yield window-length segments with fixed overlap (SciPy-compatible stepping).

    Parameters
    ----------
    x : ndarray
        1-D real-valued time series.
    nfft : int
        Segment length (samples).
    noverlap : int
        Samples shared between consecutive segments.

    Yields
    ------
    ndarray
        Segments of shape ``(nfft,)``.
    """
    x = np.asarray(x, dtype=np.float64).ravel()
    step = nfft - noverlap
    if step < 1:
        raise ValueError("noverlap must be smaller than nfft.")
    if x.size < nfft:
        raise ValueError("Signal shorter than one segment.")
    for start in range(0, x.size - nfft + 1, step):
        yield x[start : start + nfft]
