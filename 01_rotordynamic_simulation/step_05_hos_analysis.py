"""Step 05: Compute bispectrum and bicoherence for each condition."""

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ross.hos import estimate_bicoherence, estimate_bispectrum, extract_bispectral_peaks

from sinha_common import ensure_output_dir


def _load_case(out_dir, name):
    data = np.load(out_dir / f"step_04_{name}.npz")
    return data["t"], data["x"]


def _analyze_case(t, x, nfft=512, noverlap=256):
    dt = float(np.mean(np.diff(t)))
    fs = 1.0 / dt
    bspec, freqs = estimate_bispectrum(x, fs=fs, nfft=nfft, noverlap=noverlap)
    bic2, _ = estimate_bicoherence(x, fs=fs, nfft=nfft, noverlap=noverlap)
    peaks = extract_bispectral_peaks(bspec, freqs, top_n=3, min_freq=5.0, max_freq=120.0)
    return bspec, bic2, freqs, peaks


def main():
    """Run HOS extraction for healthy, crack, and misalignment signals."""
    out_dir = ensure_output_dir()
    summary = {}

    for case in ["healthy", "crack", "misalignment"]:
        t, x = _load_case(out_dir, case)
        bspec, bic2, freqs, peaks = _analyze_case(t, x)
        np.savez_compressed(
            out_dir / f"step_05_hos_{case}.npz",
            bspec=bspec,
            bic2=bic2,
            freqs=freqs,
        )
        summary[case] = {"top_peaks": peaks}

    # Small robustness check against segmentation choice.
    t_h, x_h = _load_case(out_dir, "healthy")
    _, _, _, peaks_512 = _analyze_case(t_h, x_h, nfft=512, noverlap=256)
    _, _, _, peaks_256 = _analyze_case(t_h, x_h, nfft=256, noverlap=128)
    summary["robustness"] = {"healthy_nfft_512": peaks_512, "healthy_nfft_256": peaks_256}

    output = out_dir / "step_05_hos_summary.json"
    output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
