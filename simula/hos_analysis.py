import numpy as np
from scipy.signal import detrend, periodogram

def estimate_bispectrum(signal, fs, nfft=256, noverlap=128):
    """
    Estimate bispectrum using direct (DFT-based) method with segment averaging.

    Parameters
    ----------
    signal : array_like
        Time-domain signal.
    fs : float
        Sampling frequency (Hz).
    nfft : int
        FFT length per segment.
    noverlap : int
        Overlap between segments.

    Returns
    -------
    B : ndarray, complex
        Bispectrum estimate (nf x nf).
    freqs : ndarray
        Frequency axis (Hz).
    """
    signal = detrend(signal)
    step = nfft - noverlap
    n_segments = (len(signal) - nfft) // step + 1

    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    nf = len(freqs)
    
    B = np.zeros((nf, nf), dtype=complex)
    window = np.hanning(nfft)

    for i in range(n_segments):
        segment = signal[i * step : i * step + nfft]
        
        # Full FFT for f3 terms (need negative frequencies implicitly via periodicity or explicit full FFT)
        # B(f1, f2) = X(f1) * X(f2) * X*(f1 + f2)
        # For real signals, X(-f) = X*(f). 
        # But using full FFT is easier for indexing f1+f2.
        X_full = np.fft.fft(segment * window)
        X = np.fft.rfft(segment * window) # Positive frequencies 0 to Nyquist

        # Vectorized outer product for X(f1) * X(f2)
        # X is shape (nf,)
        # X_outer is shape (nf, nf) where X_outer[i, j] = X[i] * X[j]
        X_outer = np.outer(X, X)
        
        # We need X*(f1 + f2). 
        # f1 + f2 can range from 0 to 2*(nf-1).
        # We need to map this to indices in X_full.
        # X_full has length nfft.
        # Indices 0 to nf-1 correspond to positive frequencies.
        # Indices nfft/2 to nfft-1 correspond to negative frequencies (aliased).
        # But here we are looking for f3 = f1 + f2.
        # If f1+f2 < nf, it's in the positive spectrum range.
        # If f1+f2 >= nf, it technically exceeds Nyquist if we consider strictly bandlimited,
        # but in discrete DFT, indices wrap. However, physically f1+f2 > Nyquist aliases.
        # We typically only care about the principal domain where f1+f2 <= Nyquist.
        # Or we might want to see aliasing. 
        # Standard definition restricts f1+f2 <= Nyquist (f3 < nf).
        
        # Let's compute for all valid f1, f2 where f1+f2 < nf.
        
        # Create a grid of f1+f2 indices
        f1_grid, f2_grid = np.meshgrid(np.arange(nf), np.arange(nf), indexing='ij')
        f3_grid = f1_grid + f2_grid
        
        # Mask for valid region (f1 + f2 < nf)
        # Or maybe f1 + f2 <= nfft/2? 
        # rfft returns nfft//2 + 1 points.
        mask = f3_grid < nf 
        
        # X_conj_sum = X_full[f3_grid].conj() 
        # Wait, X_full indices match rfft indices for 0..nfft/2.
        # So X_full[k] == X[k] for k < nf.
        # We want X*(f1+f2).
        
        # Let's extract X_conj for the sum frequencies
        # We can just use X.conj() but we need it extended to 2*nf to handle sums?
        # No, if f1+f2 goes beyond Nyquist, it's not in X (rfft output).
        # We usually only compute bispectrum in the non-aliased region.
        
        # Term: X[f1] * X[f2] * conj(X[f1+f2])
        # Only possible if f1+f2 is a valid frequency bin in X.
        
        X_conj = np.zeros((nf, nf), dtype=complex)
        
        # We can use fancy indexing if we are careful
        valid_f3 = f3_grid[mask]
        X_conj[mask] = np.conj(X[valid_f3])
        
        B += X_outer * X_conj

    B /= n_segments
    return B, freqs

def estimate_bicoherence(signal, fs, nfft=256, noverlap=128):
    """
    Estimate squared bicoherence (normalized bispectrum).

    Returns
    -------
    bic2 : ndarray, real
        Squared bicoherence in [0, 1].
    freqs : ndarray
        Frequency axis (Hz).
    """
    signal = detrend(signal)
    step = nfft - noverlap
    n_segments = (len(signal) - nfft) // step + 1

    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    nf = len(freqs)
    
    B = np.zeros((nf, nf), dtype=complex)
    P12 = np.zeros((nf, nf))  # E[|X(f1)X(f2)|^2]
    P3 = np.zeros((nf, nf))   # E[|X(f1+f2)|^2]
    
    window = np.hanning(nfft)
    # Correction for window power? 
    # Bicoherence is a ratio, so window scaling might cancel out, 
    # but strictly P should be power. 
    # Let's stick to raw FFT products for now as they cancel in the ratio.

    for i in range(n_segments):
        segment = signal[i * step : i * step + nfft]
        X = np.fft.rfft(segment * window)
        
        X_outer = np.outer(X, X) # X(f1)X(f2)
        
        f1_grid, f2_grid = np.meshgrid(np.arange(nf), np.arange(nf), indexing='ij')
        f3_grid = f1_grid + f2_grid
        mask = f3_grid < nf
        
        # B numerator accumulation
        X_conj = np.zeros((nf, nf), dtype=complex)
        valid_f3 = f3_grid[mask]
        X_conj[mask] = np.conj(X[valid_f3])
        B += X_outer * X_conj
        
        # Denominator terms accumulation
        # Term 1: |X(f1)X(f2)|^2
        P12 += np.abs(X_outer)**2
        
        # Term 2: |X(f1+f2)|^2
        X3_sq = np.zeros((nf, nf))
        X3_sq[mask] = np.abs(X[valid_f3])**2
        P3 += X3_sq

    B /= n_segments
    P12 /= n_segments
    P3 /= n_segments

    # Avoid division by zero
    denom = P12 * P3
    bic2 = np.zeros_like(denom)
    
    valid_denom = denom > 1e-10 # small epsilon
    bic2[valid_denom] = (np.abs(B[valid_denom])**2) / denom[valid_denom]
    
    return bic2, freqs

def bispectral_peak_ratio(B, freqs, f_rot):
    """Ratio of bispectrum magnitude at (1X,1X) to (1X,2X)."""
    idx_1x = np.argmin(np.abs(freqs - f_rot))
    idx_2x = np.argmin(np.abs(freqs - 2 * f_rot))

    b_1x1x = np.abs(B[idx_1x, idx_1x])
    b_1x2x = np.abs(B[idx_1x, idx_2x])

    return b_1x1x / b_1x2x if b_1x2x > 0 else np.inf

def bicoherence_sum(bic2, freqs, f_min, f_max):
    """Sum of squared bicoherence in a frequency band."""
    mask = (freqs >= f_min) & (freqs <= f_max)
    return np.sum(bic2[np.ix_(mask, mask)])

def bispectral_entropy(B, freqs, f_max=None):
    """Shannon entropy of normalized bispectrum magnitude."""
    if f_max is not None:
        mask = freqs <= f_max
        B_sub = np.abs(B[np.ix_(mask, mask)])
    else:
        B_sub = np.abs(B)

    B_norm = B_sub / np.sum(B_sub) if np.sum(B_sub) > 0 else B_sub
    B_norm = B_norm[B_norm > 0]
    return -np.sum(B_norm * np.log(B_norm))
