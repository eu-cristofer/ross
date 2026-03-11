"""Step 06: Build semi-quantitative comparison report against Sinha."""

import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sinha_common import ensure_output_dir


def _peak_ratio(peaks):
    """Compute ratio between first and second strongest bispectral peaks."""
    if len(peaks) < 2 or peaks[1]["magnitude"] == 0:
        return None
    return peaks[0]["magnitude"] / peaks[1]["magnitude"]


def main():
    """Create machine-readable and human-readable comparison outputs."""
    out_dir = ensure_output_dir()
    calib = json.loads((out_dir / "step_03_calibration_result.json").read_text(encoding="utf-8"))
    hos_summary = json.loads((out_dir / "step_05_hos_summary.json").read_text(encoding="utf-8"))

    rows = []
    for case in ["healthy", "crack", "misalignment"]:
        peaks = hos_summary[case]["top_peaks"]
        ratio = _peak_ratio(peaks)
        first_peak = peaks[0] if peaks else {"f1_hz": None, "f2_hz": None, "magnitude": None}
        rows.append(
            {
                "case": case,
                "top_f1_hz": first_peak["f1_hz"],
                "top_f2_hz": first_peak["f2_hz"],
                "top_magnitude": first_peak["magnitude"],
                "peak_ratio_1_over_2": ratio,
            }
        )

    csv_file = out_dir / "step_06_peak_comparison.csv"
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md_file = out_dir / "step_06_sinha_comparison.md"
    md_content = [
        "# Semi-Quantitative Comparison Against Sinha (2007)",
        "",
        "## Modal Validation",
        f"- Target first natural frequency: 27.50 Hz",
        f"- Calibrated first natural frequency: {calib['f1_hz']:.4f} Hz",
        f"- Absolute error: {calib['error_hz']:.4f} Hz",
        "",
        "## Bispectral Key-Peak Summary",
        "",
        "| Case | Top Peak (f1, f2) [Hz] | Top Magnitude | Peak Ratio (1/2) |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        ratio_str = (
            "n/a"
            if row["peak_ratio_1_over_2"] is None
            else f"{row['peak_ratio_1_over_2']:.3f}"
        )
        md_content.append(
            f"| {row['case']} | ({row['top_f1_hz']:.2f}, {row['top_f2_hz']:.2f}) | "
            f"{row['top_magnitude']:.3e} | "
            f"{ratio_str} |"
        )

    md_content.extend(
        [
            "",
            "## Scope Note",
            "- This is a numerical, pattern-level and peak-level comparison.",
            "- Exact experimental replication is not claimed without full rig coefficients and measurement chain details.",
        ]
    )

    md_file.write_text("\n".join(md_content), encoding="utf-8")
    print(f"Saved: {csv_file}")
    print(f"Saved: {md_file}")


if __name__ == "__main__":
    main()
