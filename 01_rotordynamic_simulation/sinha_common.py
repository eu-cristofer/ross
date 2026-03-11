"""Shared helpers for the stepwise Sinha replication workflow."""

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ross as rs


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def ensure_output_dir():
    """Create and return the output folder path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def rig_spec():
    """Return the base rig specification in SI units."""
    shaft_length = 0.55
    shaft_od = 0.01
    shaft_id = 0.0

    bearing_left_x = 0.02
    bearing_right_x = 0.51
    disk_x = (bearing_left_x + bearing_right_x) / 2

    return {
        "shaft_length_m": shaft_length,
        "shaft_od_m": shaft_od,
        "shaft_id_m": shaft_id,
        "bearing_left_x_m": bearing_left_x,
        "bearing_right_x_m": bearing_right_x,
        "disk_x_m": disk_x,
        "disk_od_m": 0.075,
        "disk_id_m": 0.01,
        "disk_width_m": 0.025,
        "target_f1_hz": 27.50,
        "n_elems": 55,
    }


def build_healthy_rotor(kxx, cxx):
    """Assemble a healthy Sinha-like rotor with equivalent isotropic supports."""
    spec = rig_spec()
    steel = rs.Material(name="Steel", rho=7810, E=211e9, G_s=81.2e9)

    n_elems = spec["n_elems"]
    le = spec["shaft_length_m"] / n_elems
    shaft = [
        rs.ShaftElement(
            L=le,
            idl=spec["shaft_id_m"],
            odl=spec["shaft_od_m"],
            idr=spec["shaft_id_m"],
            odr=spec["shaft_od_m"],
            material=steel,
        )
        for _ in range(n_elems)
    ]

    disk_node = int(round(spec["disk_x_m"] / le))
    disk = rs.DiskElement.from_geometry(
        n=disk_node,
        material=steel,
        width=spec["disk_width_m"],
        i_d=spec["disk_id_m"],
        o_d=spec["disk_od_m"],
    )

    b_left_node = int(round(spec["bearing_left_x_m"] / le))
    b_right_node = int(round(spec["bearing_right_x_m"] / le))

    bearings = [
        rs.BearingElement(n=b_left_node, kxx=kxx, kyy=kxx, cxx=cxx, cyy=cxx),
        rs.BearingElement(n=b_right_node, kxx=kxx, kyy=kxx, cxx=cxx, cyy=cxx),
    ]

    rotor = rs.Rotor(shaft_elements=shaft, disk_elements=[disk], bearing_elements=bearings)
    return rotor, {"disk_node": disk_node, "left_bearing_node": b_left_node, "right_bearing_node": b_right_node}


def calibration_grid():
    """Return a coarse-to-fine equivalent support search grid."""
    stiffness = np.concatenate(
        [
            np.linspace(1e5, 1e6, 10),
            np.linspace(1.2e6, 1.0e7, 14),
        ]
    )
    damping = np.array([5.0, 20.0, 50.0, 100.0, 250.0, 500.0])
    return stiffness, damping

