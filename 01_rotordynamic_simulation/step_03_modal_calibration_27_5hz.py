"""Step 03: Inverse calibration to match first natural frequency at 27.50 Hz."""

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sinha_common import build_healthy_rotor, calibration_grid, ensure_output_dir, rig_spec


def first_lateral_frequency_hz(rotor):
    """Get first undamped natural frequency in Hz from a rotor model."""
    modal = rotor.run_modal(speed=0)
    return float(np.real(modal.wn[0]) / (2.0 * np.pi))


def main():
    """Search equivalent support parameters that best match Sinha target frequency."""
    out_dir = ensure_output_dir()
    target_hz = rig_spec()["target_f1_hz"]

    stiffness_grid, damping_grid = calibration_grid()
    best = {"error_hz": np.inf}

    for kxx in stiffness_grid:
        for cxx in damping_grid:
            rotor, node_map = build_healthy_rotor(kxx=float(kxx), cxx=float(cxx))
            f1_hz = first_lateral_frequency_hz(rotor)
            err = abs(f1_hz - target_hz)
            if err < best["error_hz"]:
                best = {
                    "kxx_n_m": float(kxx),
                    "cxx_n_s_m": float(cxx),
                    "f1_hz": float(f1_hz),
                    "target_f1_hz": float(target_hz),
                    "error_hz": float(err),
                    "node_map": node_map,
                }

    rotor_best, _ = build_healthy_rotor(best["kxx_n_m"], best["cxx_n_s_m"])
    rotor_file = out_dir / "step_03_healthy_rotor_calibrated.toml"
    rotor_best.save(rotor_file)

    result_file = out_dir / "step_03_calibration_result.json"
    result_file.write_text(json.dumps(best, indent=2), encoding="utf-8")

    print(f"Saved: {rotor_file}")
    print(f"Saved: {result_file}")
    print(
        f"Best equivalent support: kxx={best['kxx_n_m']:.3e} N/m, "
        f"cxx={best['cxx_n_s_m']:.2f} N.s/m, f1={best['f1_hz']:.3f} Hz, "
        f"error={best['error_hz']:.3f} Hz"
    )


if __name__ == "__main__":
    main()
