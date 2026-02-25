
import numpy as np
import matplotlib.pyplot as plt
from hos_analysis import estimate_bispectrum, estimate_bicoherence

def test_hos():
    fs = 1000.0
    t = np.arange(0, 10, 1.0 / fs)

    f1, f2 = 50.0, 80.0
    phi1 = np.random.uniform(0, 2 * np.pi)
    phi2 = np.random.uniform(0, 2 * np.pi)

    # Quadratically coupled: phase of (f1+f2) = phi1 + phi2 (locked)
    x_coupled = (
        np.cos(2 * np.pi * f1 * t + phi1)
        + np.cos(2 * np.pi * f2 * t + phi2)
        + 0.5 * np.cos(2 * np.pi * (f1 + f2) * t + phi1 + phi2)
        + 0.1 * np.random.randn(len(t))
    )

    B, freqs = estimate_bispectrum(x_coupled, fs, nfft=512, noverlap=384)
    bic2, freqs_bic = estimate_bicoherence(x_coupled, fs, nfft=512, noverlap=384)

    # Check peak location
    idx1 = np.argmin(np.abs(freqs - f1))
    idx2 = np.argmin(np.abs(freqs - f2))
    
    peak_val_B = np.abs(B[idx1, idx2])
    peak_val_bic = bic2[idx1, idx2]
    
    print(f"Signal: f1={f1}, f2={f2}")
    print(f"Indices: {idx1}, {idx2}")
    print(f"Bispectrum Peak: {peak_val_B:.4f}")
    print(f"Bicoherence Peak: {peak_val_bic:.4f} (Expected ~1.0)")
    
    # Check noise floor
    noise_floor_bic = np.mean(bic2[bic2 > 0])
    print(f"Mean Bicoherence Noise Floor: {noise_floor_bic:.4f}")
    
    if peak_val_bic > 0.8:
        print("PASS: Quadratic coupling detected.")
    else:
        print("FAIL: Quadratic coupling not detected strongly enough.")

if __name__ == "__main__":
    test_hos()
