"""Step 04: Run healthy, crack, and misalignment simulations."""

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ross import Probe

from sinha_common import build_healthy_rotor, ensure_output_dir


def _probe_signal(results, node):
    """Return radial probe signal at node and zero angle."""
    probe = Probe(node=node, angle=0.0)
    df = results.data_time_response(probe=[probe])
    return df["time"].to_numpy(), df["probe_resp[0]"].to_numpy()


def _save_case(out_dir, case_name, t, signal):
    """Save one case to compressed NPY."""
    np.savez_compressed(out_dir / f"step_04_{case_name}.npz", t=t, x=signal)


def main():
    """Simulate baseline and faulted responses from calibrated supports."""
    out_dir = ensure_output_dir()
    calib = json.loads((out_dir / "step_03_calibration_result.json").read_text(encoding="utf-8"))

    rotor, node_map = build_healthy_rotor(calib["kxx_n_m"], calib["cxx_n_s_m"])
    disk_node = node_map["disk_node"]
    right_node = node_map["right_bearing_node"]

    speed = 180.0  # rad/s
    dt = 2e-4
    t = np.arange(0.0, 1.0, dt)

    unb_node = [disk_node, right_node]
    unb_mag = [2.5e-4, 0.0]
    unb_phase = [-np.pi / 2, 0.0]

    healthy_force = np.zeros((len(t), rotor.ndof))
    healthy = rotor.run_time_response(speed=speed, F=healthy_force, t=t)
    t_h, x_h = _probe_signal(healthy, disk_node)
    _save_case(out_dir, "healthy", t_h, x_h)

    crack = rotor.run_crack(
        n=disk_node,
        depth_ratio=0.2,
        node=unb_node,
        unbalance_magnitude=unb_mag,
        unbalance_phase=unb_phase,
        speed=speed,
        t=t,
        crack_model="Mayes",
    )
    t_c, x_c = _probe_signal(crack, disk_node)
    _save_case(out_dir, "crack", t_c, x_c)

    mis = rotor.run_misalignment(
        coupling="flex",
        n=disk_node,
        mis_type="parallel",
        mis_distance_x=1.5e-4,
        mis_distance_y=1.5e-4,
        mis_angle=0.0,
        radial_stiffness=4e4,
        bending_stiffness=3.8e4,
        input_torque=0.0,
        load_torque=0.0,
        node=unb_node,
        unbalance_magnitude=unb_mag,
        unbalance_phase=unb_phase,
        speed=speed,
        t=t,
        method="newmark",
    )
    t_m, x_m = _probe_signal(mis, disk_node)
    _save_case(out_dir, "misalignment", t_m, x_m)

    metadata = {
        "speed_rad_s": speed,
        "dt_s": dt,
        "disk_node": disk_node,
        "cases": ["healthy", "crack", "misalignment"],
    }
    (out_dir / "step_04_run_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    print("Saved step 04 outputs in outputs/*.npz")


if __name__ == "__main__":
    main()
