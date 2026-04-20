"""Sinha (2007) validation helpers: simulation orchestration, acquisition, HDF5, HOS features.

This module is notebook-facing glue around ``ross`` and ``ross.hos``. Parameters
not reported by Sinha (2007) belong in each notebook's assumptions ledger.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

import numpy as np

import ross as rs
from ross.hos.acquisition import sinha_acquisition_chain
from ross.hos.bispectrum import estimate_bispectrum
from ross.hos.trispectrum import estimate_trispectrum_point

CaseType = Literal["healthy", "crack", "misalignment", "misalignment_pedestal"]

SINHA_CRACK_NODE = 7
SINHA_CRACK_DEPTH = 0.5
SINHA_DISK_NODE = 6
SINHA_PROBE_NODE = 10
SINHA_DEFAULT_UNBALANCE_KGM = 2e-4
SINHA_DEFAULT_UNB_PHASE_RAD = 3 * np.pi / 4


def load_sinha_rotor(toml_path: str | Path = "sinha_rotor.toml") -> rs.Rotor:
    """Load the Sinha benchmark rotor from TOML (working directory relative)."""
    return rs.Rotor.load(str(toml_path))


def default_probe(rotor: rs.Rotor, node: int | None = None) -> rs.Probe:
    """Vertical displacement probe near the free overhang (Sinha-style)."""
    n = SINHA_PROBE_NODE if node is None else int(node)
    return rs.Probe(node=n, angle=0.0)


def _speed_rad_s(speed):
    if hasattr(speed, "to"):
        return float(speed.to("rad/s").m)
    return float(speed)


def simulate_healthy(
    rotor: rs.Rotor,
    unbalance_node: int,
    unbalance_mag_kgm: float,
    unbalance_phase_rad: float,
    speed,
    t: np.ndarray,
    num_modes: int = 24,
):
    """Healthy rotor with mass unbalance only (``run_time_response``)."""
    speed_r = _speed_rad_s(speed)
    n0 = int(unbalance_node)
    m0 = float(unbalance_mag_kgm)
    ph0 = float(unbalance_phase_rad)
    f_dof_t = rotor.unbalance_force_over_time([n0], [m0], [ph0], speed_r, t)
    f_rows_t = f_dof_t.T
    return rotor.run_time_response(
        speed=speed,
        F=f_rows_t,
        t=t,
        model_reduction={"num_modes": num_modes},
    )


def simulate_crack(
    rotor: rs.Rotor,
    crack_elem: int,
    depth_ratio: float,
    unbalance_node: int,
    unbalance_mag_kgm: float,
    unbalance_phase_rad: float,
    speed,
    t: np.ndarray,
    crack_model: str = "Gasch",
    num_modes: int = 24,
):
    """Cracked shaft using ``Rotor.run_crack`` (Gasch by default)."""
    speed_r = _speed_rad_s(speed)
    return rotor.run_crack(
        n=int(crack_elem),
        depth_ratio=float(depth_ratio),
        crack_model=crack_model,
        node=[int(unbalance_node)],
        unbalance_magnitude=[float(unbalance_mag_kgm)],
        unbalance_phase=[float(unbalance_phase_rad)],
        speed=speed_r,
        t=t,
        model_reduction={"num_modes": int(num_modes)},
    )


def simulate_misalignment_flex(
    rotor: rs.Rotor,
    mis_shaft_elem: int,
    disk_node: int,
    unbalance_node: int,
    unbalance_mag_kgm: float,
    unbalance_phase_rad: float,
    speed,
    t: np.ndarray,
    mis_distance_x: float = 1.0e-3,
    mis_distance_y: float = 0.5e-3,
    radial_stiffness: float = 40e3,
    bending_stiffness: float = 38e3,
    num_modes: int = 24,
):
    """Flexible-coupling parallel misalignment (``run_misalignment``)."""
    speed_r = _speed_rad_s(speed)
    return rotor.run_misalignment(
        coupling="flex",
        n=int(mis_shaft_elem),
        mis_type="parallel",
        mis_distance_x=mis_distance_x,
        mis_distance_y=mis_distance_y,
        mis_angle=0.0,
        radial_stiffness=radial_stiffness,
        bending_stiffness=bending_stiffness,
        input_torque=0.0,
        load_torque=0.0,
        node=[int(disk_node)],
        unbalance_magnitude=[float(unbalance_mag_kgm)],
        unbalance_phase=[float(unbalance_phase_rad)],
        speed=speed_r,
        t=t,
        model_reduction={"num_modes": int(num_modes)},
    )


def simulate_case(
    rotor: rs.Rotor,
    case: CaseType,
    speed,
    t: np.ndarray,
    *,
    crack_elem: int = SINHA_CRACK_NODE,
    depth_ratio: float = SINHA_CRACK_DEPTH,
    disk_node: int = SINHA_DISK_NODE,
    unbalance_node: int = SINHA_DISK_NODE,
    unbalance_mag_kgm: float = SINHA_DEFAULT_UNBALANCE_KGM,
    unbalance_phase_rad: float = SINHA_DEFAULT_UNB_PHASE_RAD,
    num_modes: int = 24,
):
    """Dispatch healthy / crack / misalignment / pedestal-proxy misalignment."""
    if case == "healthy":
        return simulate_healthy(
            rotor,
            unbalance_node,
            unbalance_mag_kgm,
            unbalance_phase_rad,
            speed,
            t,
            num_modes=num_modes,
        )
    if case == "crack":
        return simulate_crack(
            rotor,
            crack_elem,
            depth_ratio,
            unbalance_node,
            unbalance_mag_kgm,
            unbalance_phase_rad,
            speed,
            t,
            num_modes=num_modes,
        )
    if case == "misalignment":
        return simulate_misalignment_flex(
            rotor,
            mis_shaft_elem=disk_node,
            disk_node=disk_node,
            unbalance_node=unbalance_node,
            unbalance_mag_kgm=unbalance_mag_kgm,
            unbalance_phase_rad=unbalance_phase_rad,
            speed=speed,
            t=t,
            num_modes=num_modes,
        )
    if case == "misalignment_pedestal":
        brg = rotor.bearing_elements[-1].n
        mis_elem = max(0, int(brg) - 1)
        return simulate_misalignment_flex(
            rotor,
            mis_shaft_elem=mis_elem,
            disk_node=disk_node,
            unbalance_node=unbalance_node,
            unbalance_mag_kgm=unbalance_mag_kgm,
            unbalance_phase_rad=unbalance_phase_rad,
            speed=speed,
            t=t,
            num_modes=num_modes,
        )
    raise ValueError(f"Unknown case: {case!r}")


def probe_displacement_y_from_rotor(rotor: rs.Rotor, results, probe: rs.Probe) -> np.ndarray:
    n = int(probe.node)
    nd = int(rotor.number_dof)
    dof_y = nd * n + 1
    return results.yout[:, dof_y]


def acquisition_chain(
    x: np.ndarray,
    fs_in: float,
    *,
    lp_hz: float = 1000.0,
    decimate_factor: int = 10,
    snr_db: float = 40.0,
    seed: int | None = None,
):
    """LP → block decimate → AWGN at ``snr_db``; returns ``(y, fs_out)``."""
    return sinha_acquisition_chain(
        x,
        fs_in,
        lp_hz=lp_hz,
        decimate_factor=decimate_factor,
        snr_db=snr_db,
        seed=seed,
    )


def _nearest_bin(freqs: np.ndarray, f_hz: float) -> int:
    return int(np.argmin(np.abs(freqs - f_hz)))


def fault_indicators_bispectrum(
    signal: np.ndarray,
    fs: float,
    shaft_freq_hz: float,
    *,
    nfft: int = 2048,
    noverlap: int = 1024,
    window: str = "hann",
) -> dict[str, Any]:
    """Scalar bispectral magnitudes at Sinha-style harmonic pairs (nearest FFT bins)."""
    B, freqs = estimate_bispectrum(signal, fs, nfft=nfft, noverlap=noverlap, window=window)
    mag = np.abs(B)
    fr = float(shaft_freq_hz)

    def m_at(f1: float, f2: float) -> float:
        i = _nearest_bin(freqs, f1)
        j = _nearest_bin(freqs, f2)
        if i + j >= mag.shape[0]:
            return 0.0
        return float(mag[i, j])

    out = {
        "B11": m_at(fr, fr),
        "B12": m_at(fr, 2 * fr),
        "B13": m_at(fr, 3 * fr),
        "B22": m_at(2 * fr, 2 * fr),
        "freqs_hz": freqs,
        "bispectrum_mag": mag,
    }
    return out


def fault_indicators_trispectrum(
    signal: np.ndarray,
    fs: float,
    shaft_freq_hz: float,
    *,
    nfft: int = 2048,
    noverlap: int = 1024,
    window: str = "hann",
) -> dict[str, Any]:
    """Fourth-order slice magnitudes at (1X,1X,1X), (1X,1X,2X), (1X,2X,2X), (2X,2X,2X)."""
    fr = float(shaft_freq_hz)

    def Tmag(a: float, b: float, c: float) -> float:
        z, _ = estimate_trispectrum_point(
            signal, fs, a, b, c, nfft=nfft, noverlap=noverlap, window=window
        )
        return float(np.abs(z))

    return {
        "T111": Tmag(fr, fr, fr),
        "T112": Tmag(fr, fr, 2 * fr),
        "T122": Tmag(fr, 2 * fr, 2 * fr),
        "T222": Tmag(2 * fr, 2 * fr, 2 * fr),
    }


def fault_indicators(
    signal: np.ndarray,
    fs: float,
    shaft_freq_hz: float,
    *,
    nfft: int = 2048,
    noverlap: int = 1024,
) -> dict[str, Any]:
    """Combined bispectrum + trispectrum feature dict."""
    b = fault_indicators_bispectrum(
        signal, fs, shaft_freq_hz, nfft=nfft, noverlap=noverlap
    )
    t = fault_indicators_trispectrum(
        signal, fs, shaft_freq_hz, nfft=nfft, noverlap=noverlap
    )
    b_scalar = {k: b[k] for k in ("B11", "B12", "B13", "B22")}
    return {**b_scalar, **t}


def save_timeseries_hdf5(
    path: str | Path,
    *,
    fs: float,
    t: np.ndarray,
    y: np.ndarray,
    meta: dict[str, Any],
    compression: str = "gzip",
) -> None:
    """Save a single-channel trace with JSON metadata (requires ``h5py``)."""
    import h5py

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with h5py.File(path, "w") as h5:
        g = h5.create_group("signal")
        g.attrs["json_meta"] = json.dumps(meta, default=str)
        g.create_dataset("t", data=t, compression=compression)
        g.create_dataset("y", data=y, compression=compression)
        g.attrs["fs_hz"] = float(fs)


def load_timeseries_hdf5(path: str | Path) -> tuple[np.ndarray, np.ndarray, float, dict]:
    """Load ``(t, y, fs, meta_dict)`` from :func:`save_timeseries_hdf5`."""
    import h5py

    with h5py.File(path, "r") as h5:
        g = h5["signal"]
        meta = json.loads(g.attrs["json_meta"])
        fs = float(g.attrs["fs_hz"])
        t = np.array(g["t"])
        y = np.array(g["y"])
    return t, y, fs, meta


__all__ = [
    "SINHA_CRACK_DEPTH",
    "SINHA_CRACK_NODE",
    "SINHA_DEFAULT_UNB_PHASE_RAD",
    "SINHA_DEFAULT_UNBALANCE_KGM",
    "SINHA_DISK_NODE",
    "SINHA_PROBE_NODE",
    "acquisition_chain",
    "default_probe",
    "fault_indicators",
    "fault_indicators_bispectrum",
    "fault_indicators_trispectrum",
    "load_sinha_rotor",
    "load_timeseries_hdf5",
    "probe_displacement_y_from_rotor",
    "save_timeseries_hdf5",
    "simulate_case",
    "simulate_crack",
    "simulate_healthy",
    "simulate_misalignment_flex",
]
