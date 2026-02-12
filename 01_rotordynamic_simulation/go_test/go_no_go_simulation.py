#!/usr/bin/env python3
"""
GO/NO-GO Feasibility Test: HOS-Based Fault Diagnosis in Rotating Machinery
===========================================================================

This script tests whether Higher-Order Spectra (bispectrum, bicoherence) can
distinguish between shaft cracks and shaft misalignment in numerically simulated
vibration data from finite-element rotor models built with ROSS.

Two rotor models are built:
    1. Sinha rotor  -- small lab rig (OD 10 mm, L 550 mm)
    2. Laval rotor  -- textbook Jeffcott-like mid-span-disk rotor

Four simulation cases run on the Laval rotor at 1500 RPM (25 Hz):
    1. Healthy (unbalance only)
    2. Light crack  (a/D = 0.2)
    3. Severe crack  (a/D = 0.4)
    4. Parallel misalignment (offset = 0.5 mm)

Author  : Research project -- Master's thesis
Date    : 2026-02-11
"""

import sys
import warnings
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
np.random.seed(42)

# ---------------------------------------------------------------------------
# CONSTANTS  (modify these to change the simulation)
# ---------------------------------------------------------------------------
SPEED_HZ = 25.0                          # Rotational speed [Hz] (= 1500 RPM)
SPEED_RPM = 1500.0
SPEED_RAD = 2.0 * np.pi * SPEED_HZ       # ≈ 157.08 rad/s

FS = 2048                                 # Sampling frequency [Hz]
DURATION = 4.0                            # Total simulation time [s]
TRANSIENT = 1.0                           # Transient to discard [s]

UNBALANCE_MAG = 1e-4                      # Unbalance magnitude [kg·m]
UNBALANCE_PHASE = 0.0                     # Unbalance phase [rad]

# Crack parameters
CRACK_DEPTH_LIGHT = 0.2                   # a/D ratio – light crack
CRACK_DEPTH_SEVERE = 0.4                  # a/D ratio – severe crack
CRACK_BASE_AMP = 50.0                     # Base force amplitude [N]

# Misalignment parameters
MISALIGNMENT_OFFSET = 0.5                 # Parallel offset [mm]
MISALIGNMENT_BASE_AMP = 100.0             # Base force amplitude [N]

# PSD parameters
PSD_NFFT = 1024
PSD_WINDOW = "hann"
PSD_OVERLAP_RATIO = 0.5

# Bispectrum parameters
BISP_NFFT = 512
BISP_OVERLAP_RATIO = 0.5

# Plotting
PLOT_FREQ_MAX = 200.0                     # Max frequency on axes [Hz]
PLOT_DPI = 300

# Output directory  (same folder as this script)
OUTPUT_DIR = Path(__file__).resolve().parent

# ===================================================================
# DEPENDENCY CHECK
# ===================================================================
try:
    import ross as rs
    from ross.materials import Material
    print(f"[ok] ROSS {rs.__version__}")
except ImportError:
    print("[!!] ROSS not found.  Install with:  pip install ross-rotordynamics")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use("Agg")                    # non-interactive backend
    import matplotlib.pyplot as plt
    print(f"[ok] Matplotlib {matplotlib.__version__}")
except ImportError:
    print("[!!] Matplotlib not found.")
    sys.exit(1)

try:
    import scipy
    from scipy import signal as sp_signal
    from scipy.signal import detrend
    print(f"[ok] SciPy {scipy.__version__}")
except ImportError:
    print("[!!] SciPy not found.")
    sys.exit(1)


# ===================================================================
# STEP 1 — Build rotor models
# ===================================================================

def build_sinha_rotor():
    """Build the Sinha rotor model.

    Physical dimensions (Sinha's paper):
        Shaft : OD = 10 mm, L = 550 mm, solid steel
        Bush bearings at L1 = 20 mm  and  L2 = 510 mm
        Balance disk  : OD = 75 mm, ID = 10 mm, thickness = 25 mm
        Disk location : L/2 = 275 mm
        Target Fn1    : 27.50 Hz (both horizontal and vertical)
    """
    steel_mat = Material(name="Steel_Sinha", rho=7810, E=211e9, G_s=81.2e9)

    shaft_od = 0.010        # 10 mm
    shaft_id = 0.0           # solid

    # Node positions [mm]: key locations → bearing, disk, bearing
    node_pos_mm = [0, 20, 70, 120, 170, 220, 275, 325, 375, 425, 475, 510, 550]
    n_elems = len(node_pos_mm) - 1
    lengths_m = [(node_pos_mm[i + 1] - node_pos_mm[i]) * 1e-3
                 for i in range(n_elems)]

    shaft_elements = [
        rs.ShaftElement(
            L=le, idl=shaft_id, odl=shaft_od,
            material=steel_mat,
            shear_effects=True, rotary_inertia=True, gyroscopic=True,
        )
        for le in lengths_m
    ]

    # Disk at node 6  (275 mm ≈ L/2)
    disk = rs.DiskElement.from_geometry(
        n=6, material=steel_mat,
        width=0.025, i_d=0.010, o_d=0.075,    # 25 mm thick, ID 10 mm, OD 75 mm
    )

    # --- iteratively tune bearing stiffness for Fn1 ≈ 27.5 Hz ----------
    target_fn1 = 27.5   # Hz
    target_wn1 = 2.0 * np.pi * target_fn1
    k_bearing = 1.0e5   # initial guess  [N/m]
    c_bearing = 10.0     # light damping  [N·s/m]

    for _ in range(15):
        brg1 = rs.BearingElement(n=1, kxx=k_bearing, kyy=k_bearing,
                                 cxx=c_bearing, cyy=c_bearing)
        brg2 = rs.BearingElement(n=11, kxx=k_bearing, kyy=k_bearing,
                                 cxx=c_bearing, cyy=c_bearing)
        rotor = rs.Rotor(shaft_elements, [disk], [brg1, brg2], tag="Sinha Rotor")
        modal = rotor.run_modal(speed=0)
        wn1 = modal.wn[0]
        fn1 = wn1 / (2.0 * np.pi)
        if abs(fn1 - target_fn1) / target_fn1 < 0.005:
            break
        k_bearing *= (target_wn1 / wn1) ** 2

    print(f"  Sinha Rotor — Fn1 = {fn1:.2f} Hz  (k_brg = {k_bearing:.0f} N/m)")
    return rotor


def build_laval_rotor():
    """Build the Laval / Jeffcott-like rotor model.

    Shaft : 1.0 m total, OD 30 mm, solid, steel
    20 equal elements × 50 mm each
    Disc at midspan (node 10)
    Bearings at node 0 and node 20
    Isotropic: kxx = kyy = 1 × 10^6 N/m,  cxx = cyy = 500 N·s/m
    """
    steel_mat = Material(name="Steel_Laval", rho=7810, E=211e9, G_s=81.2e9)

    n_elements = 20
    le = 0.050       # 50 mm
    shaft_od = 0.030  # 30 mm
    shaft_id = 0.0

    shaft_elements = [
        rs.ShaftElement(
            L=le, idl=shaft_id, odl=shaft_od,
            material=steel_mat,
            shear_effects=True, rotary_inertia=True, gyroscopic=True,
        )
        for _ in range(n_elements)
    ]

    # Disc at node 10  (midspan = 500 mm)
    disk = rs.DiskElement.from_geometry(
        n=10, material=steel_mat,
        width=0.050, i_d=0.030, o_d=0.150,    # 50 mm, ID 30 mm, OD 150 mm
    )

    bearing0 = rs.BearingElement(n=0,  kxx=1e6, kyy=1e6, cxx=500, cyy=500)
    bearing1 = rs.BearingElement(n=20, kxx=1e6, kyy=1e6, cxx=500, cyy=500)

    rotor = rs.Rotor(shaft_elements, [disk], [bearing0, bearing1],
                     tag="Laval Rotor")
    return rotor


# ===================================================================
# STEP 2 — Fault forcing functions
# ===================================================================

def compute_unbalance_force(t, omega, me):
    """Synchronous unbalance force  F = m·e·ω² in x and y.

    Returns
    -------
    fx, fy : ndarray   force in each direction [N]
    """
    fx = me * omega ** 2 * np.cos(omega * t)
    fy = me * omega ** 2 * np.sin(omega * t)
    return fx, fy


def compute_crack_force(t, omega, a_D_ratio):
    """Approximate breathing-crack forcing with quadratic nonlinearity.

    A breathing crack opens/closes once per revolution, producing
    phase-coupled 2X and 3X harmonics.  The quadratic term ``x1²``
    is the mechanism the bispectrum can detect.

    Returns
    -------
    fx : ndarray   crack force in x direction [N]
    """
    base = CRACK_BASE_AMP * (a_D_ratio ** 2)
    x1 = np.cos(omega * t)        # 1X component
    # x1² → DC + 2X (phase-coupled to 1X)
    # x1³ → 1X + 3X
    fx = base * (x1 ** 2) + 0.2 * base * (x1 ** 3)
    return fx


def compute_misalignment_force(t, omega, offset_mm):
    """Approximate parallel-misalignment forcing.

    Misalignment generates 1X and 2X with *different* phase
    relationships compared to a crack — this is the key
    differentiator the bispectrum should reveal.

    Returns
    -------
    fx : ndarray   misalignment force in x direction [N]
    """
    base = MISALIGNMENT_BASE_AMP * (offset_mm / 0.5)
    f_1x = base * np.cos(omega * t + np.pi / 6)
    f_2x = 0.80 * base * np.cos(2 * omega * t + np.pi / 3)
    f_3x = 0.15 * base * np.cos(3 * omega * t + np.pi / 2)
    return f_1x + f_2x + f_3x


# ===================================================================
# STEP 3 — Time-domain simulation
# ===================================================================

def run_simulation(rotor, label, t, speed_rad, omega,
                   fault_type=None, fault_params=None):
    """Run one time-domain case on *rotor* and return x-displacement at disc.

    Uses the ROSS LTI method (``scipy.signal.lsim``) for speed.
    Falls back to Newmark if LTI fails.

    Returns
    -------
    x_disp : ndarray   horizontal displacement at disc node [m]
    """
    ndof = rotor.ndof
    ndof_per_node = rotor.number_dof          # 4 for a standard (4-DOF) rotor
    disc_node = 10
    dof_x = ndof_per_node * disc_node         # horizontal DOF index
    dof_y = ndof_per_node * disc_node + 1     # vertical   DOF index

    # ---- build force array  (n_time × ndof) ----
    F = np.zeros((len(t), ndof))

    # unbalance at disc
    fx_u, fy_u = compute_unbalance_force(t, omega, UNBALANCE_MAG)
    F[:, dof_x] += fx_u
    F[:, dof_y] += fy_u

    # fault-specific forces
    if fault_type == "crack":
        fx_c = compute_crack_force(t, omega, fault_params["a_D"])
        F[:, dof_x] += fx_c
        F[:, dof_y] += 0.3 * fx_c            # smaller y component

    elif fault_type == "misalignment":
        brg_node = 20                         # right bearing
        brg_dof_x = ndof_per_node * brg_node
        brg_dof_y = ndof_per_node * brg_node + 1
        fx_m = compute_misalignment_force(t, omega, fault_params["offset_mm"])
        F[:, brg_dof_x] += fx_m
        F[:, brg_dof_y] += 0.5 * fx_m

    # ---- integrate ----
    print(f"    Simulating: {label} …")
    try:
        t_out, y_out, _ = rotor.time_response(speed_rad, F, t)
    except Exception as exc:
        print(f"    [!] LTI failed ({exc}); switching to Newmark …")
        t_out, y_out, _ = rotor.time_response(
            speed_rad, F, t, method="newmark"
        )

    x_disp = y_out[:, dof_x]
    return x_disp


# ===================================================================
# STEP 4 — PSD  (Welch)
# ===================================================================

def compute_psd(sig, fs, nfft=PSD_NFFT):
    """Compute normalised Power Spectral Density via Welch's method.

    Returns  (freqs, psd_normalised)
    """
    noverlap = int(nfft * PSD_OVERLAP_RATIO)
    freqs, psd = sp_signal.welch(
        sig, fs=fs, window=PSD_WINDOW, nperseg=nfft, noverlap=noverlap,
    )
    mx = np.max(psd)
    if mx > 0:
        psd /= mx
    return freqs, psd


# ===================================================================
# STEP 5 — Bispectrum estimation  (direct DFT method)
# ===================================================================

def compute_bispectrum(sig, fs, nfft=BISP_NFFT, overlap_ratio=BISP_OVERLAP_RATIO):
    """Estimate bispectrum B(f1,f2) and squared bicoherence.

    Uses the direct (DFT) method with segment averaging.

    Parameters
    ----------
    sig   : 1-D real signal
    fs    : sampling frequency [Hz]
    nfft  : FFT length per segment
    overlap_ratio : fractional overlap [0, 1)

    Returns
    -------
    B           : complex  (nf × nf)   bispectrum
    bicoherence : real     (nf × nf)   squared bicoherence
    freqs       : 1-D array            frequency axis [Hz]
    """
    sig = detrend(sig)
    step = nfft - int(nfft * overlap_ratio)
    n_segments = (len(sig) - nfft) // step + 1

    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    nf = len(freqs)

    B   = np.zeros((nf, nf), dtype=complex)
    P12 = np.zeros((nf, nf), dtype=float)
    P3  = np.zeros((nf, nf), dtype=float)
    window = np.hanning(nfft)

    for seg in range(n_segments):
        start = seg * step
        segment = sig[start : start + nfft] * window
        X_full = np.fft.fft(segment)
        X = np.fft.rfft(segment)

        # vectorised inner loop (over j for each i)
        for i in range(nf):
            j = np.arange(i, nf)
            k = i + j
            mask = k < nfft
            jv = j[mask]
            kv = k[mask]
            if jv.size == 0:
                continue
            val = X[i] * X[jv] * np.conj(X_full[kv])
            B[i, jv]   += val
            P12[i, jv] += np.abs(X[i] * X[jv]) ** 2
            P3[i, jv]  += np.abs(X_full[kv]) ** 2

    B   /= n_segments
    P12 /= n_segments
    P3  /= n_segments

    denom = np.sqrt(P12 * P3)
    denom[denom == 0] = 1e-30
    bicoherence = (np.abs(B) ** 2) / (denom ** 2)

    return B, bicoherence, freqs


# ===================================================================
# STEP 6 — Plotting
# ===================================================================

def generate_plots(cases, out):
    """Create and save the two summary figures.

    Figure 1 — 4 × 3 grid : time signal | PSD | bispectrum magnitude
    Figure 2 — 1 × 4       : bicoherence comparison (shared colour scale)
    """
    # ---- Figure 1 ----
    fig1, axes = plt.subplots(4, 3, figsize=(18, 16))
    fig1.suptitle(
        "GO / NO-GO Feasibility Test :  Time  ·  PSD  ·  Bispectrum\n"
        f"Speed = {SPEED_RPM:.0f} RPM  ({SPEED_HZ:.0f} Hz)",
        fontsize=14, fontweight="bold",
    )

    for row, c in enumerate(cases):
        t_a  = c["t_analysis"]
        x_a  = c["x_analysis"]
        pf   = c["psd_freqs"]
        ps   = c["psd"]
        B    = c["B"]
        bf   = c["bisp_freqs"]
        lab  = c["label"]

        # col 0 — time signal  (last 0.2 s)
        ax = axes[row, 0]
        mask = t_a >= (t_a[-1] - 0.2)
        ax.plot(t_a[mask] * 1e3, x_a[mask] * 1e6, "b-", linewidth=0.5)
        ax.set_ylabel(f"{lab}\nDisp. [µm]")
        if row == 3:
            ax.set_xlabel("Time [ms]")
        if row == 0:
            ax.set_title("Time signal (last 0.2 s)")
        ax.grid(True, alpha=0.3)

        # col 1 — PSD
        ax = axes[row, 1]
        fm = pf <= PLOT_FREQ_MAX
        ax.semilogy(pf[fm], ps[fm], "b-", linewidth=0.8)
        for nh, col, ls in [(1, "r", "--"), (2, "g", "--"), (3, "m", "--")]:
            fh = nh * SPEED_HZ
            ax.axvline(fh, color=col, ls=ls, alpha=0.5,
                       label=f"{nh}X = {fh:.0f} Hz")
        if row == 0:
            ax.set_title("PSD (Welch)")
            ax.legend(fontsize=7, loc="upper right")
        if row == 3:
            ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("Normalised PSD")
        ax.grid(True, alpha=0.3)

        # col 2 — bispectrum magnitude (log)
        ax = axes[row, 2]
        B_mag = np.log10(np.abs(B) + 1e-30)
        fi = np.searchsorted(bf, PLOT_FREQ_MAX)
        Bp = B_mag[:fi, :fi]
        fp = bf[:fi]
        im = ax.pcolormesh(fp, fp, Bp.T, cmap="inferno", shading="auto")
        plt.colorbar(im, ax=ax, label="log₁₀|B|")
        # mark key pairs
        pairs  = [(SPEED_HZ, SPEED_HZ),
                   (SPEED_HZ, 2 * SPEED_HZ),
                   (2 * SPEED_HZ, 2 * SPEED_HZ)]
        labels = ["(1X,1X)", "(1X,2X)", "(2X,2X)"]
        for (f1, f2), ml in zip(pairs, labels):
            if f1 <= PLOT_FREQ_MAX and f2 <= PLOT_FREQ_MAX:
                ax.plot(f1, f2, "w+", ms=10, mew=2)
                ax.annotate(ml, (f1 + 3, f2 + 3), color="white",
                            fontsize=7, fontweight="bold")
        if row == 0:
            ax.set_title("Bispectrum magnitude")
        if row == 3:
            ax.set_xlabel("f₁ [Hz]")
        ax.set_ylabel("f₂ [Hz]")

    fig1.tight_layout()
    path1 = out / "go_no_go_psd_bispectrum.png"
    fig1.savefig(path1, dpi=PLOT_DPI, bbox_inches="tight")
    print(f"  [saved] {path1}")
    plt.close(fig1)

    # ---- Figure 2 : bicoherence comparison ----
    fig2, axes2 = plt.subplots(1, 4, figsize=(20, 5))
    fig2.suptitle("Bicoherence comparison  (shared colour scale)",
                  fontsize=14, fontweight="bold")

    # common colour limits
    vmin_g, vmax_g = np.inf, -np.inf
    for c in cases:
        fi = np.searchsorted(c["bisp_freqs"], PLOT_FREQ_MAX)
        bp = c["bicoherence"][:fi, :fi]
        if bp.size:
            vmin_g = min(vmin_g, float(np.nanmin(bp)))
            mx = float(np.nanmax(bp[bp < 1.0])) if np.any(bp < 1.0) else 1.0
            vmax_g = max(vmax_g, mx)
    if vmax_g <= vmin_g:
        vmin_g, vmax_g = 0.0, 1.0

    for col_idx, c in enumerate(cases):
        ax = axes2[col_idx]
        fi = np.searchsorted(c["bisp_freqs"], PLOT_FREQ_MAX)
        bp = c["bicoherence"][:fi, :fi]
        fp = c["bisp_freqs"][:fi]
        im = ax.pcolormesh(fp, fp, bp.T, cmap="hot",
                           vmin=vmin_g, vmax=vmax_g, shading="auto")
        ax.set_title(c["label"], fontsize=10)
        ax.set_xlabel("f₁ [Hz]")
        if col_idx == 0:
            ax.set_ylabel("f₂ [Hz]")
        for f1, f2 in [(SPEED_HZ, SPEED_HZ), (SPEED_HZ, 2 * SPEED_HZ)]:
            ax.plot(f1, f2, "c+", ms=10, mew=2)

    fig2.colorbar(im, ax=axes2.tolist(), label="Bicoherence", shrink=0.8)
    fig2.tight_layout()
    path2 = out / "go_no_go_bicoherence.png"
    fig2.savefig(path2, dpi=PLOT_DPI, bbox_inches="tight")
    print(f"  [saved] {path2}")
    plt.close(fig2)


# ===================================================================
# STEP 7 — Quantitative summary  +  GO / NO-GO verdict
# ===================================================================

def print_summary(cases):
    """Print the metrics table and verdict."""

    def _psd_at(pf, ps, freq):
        return ps[np.argmin(np.abs(pf - freq))]

    def _bisp_at(bf, B, f1, f2):
        i1 = np.argmin(np.abs(bf - f1))
        i2 = np.argmin(np.abs(bf - f2))
        return B[i1, i2]

    # ---- collect metrics ----
    metrics = []
    for c in cases:
        pf, ps, B, bf = c["psd_freqs"], c["psd"], c["B"], c["bisp_freqs"]
        a1 = _psd_at(pf, ps, SPEED_HZ)
        a2 = _psd_at(pf, ps, 2 * SPEED_HZ)
        a3 = _psd_at(pf, ps, 3 * SPEED_HZ)
        B11 = _bisp_at(bf, B, SPEED_HZ, SPEED_HZ)
        B12 = _bisp_at(bf, B, SPEED_HZ, 2 * SPEED_HZ)
        metrics.append({
            "label": c["label"],
            "1X": a1, "2X": a2, "3X": a3,
            "|B11|": np.abs(B11), "|B12|": np.abs(B12),
            "phi11": np.degrees(np.angle(B11)),
        })

    # ---- print table ----
    print("\n" + "=" * 70)
    print("GO / NO-GO  FEASIBILITY TEST RESULTS")
    print("=" * 70)

    hdr = (f"{'Case':<20s} | {'1X':>9s} | {'2X':>9s} | {'3X':>9s} | "
           f"{'|B(1X,1X)|':>11s} | {'|B(1X,2X)|':>11s} | {'Biphase(1X,1X)':>15s}")
    print(f"\n{hdr}")
    print("-" * len(hdr))
    for m in metrics:
        print(f"{m['label']:<20s} | {m['1X']:>9.2e} | {m['2X']:>9.2e} | "
              f"{m['3X']:>9.2e} | {m['|B11|']:>11.2e} | "
              f"{m['|B12|']:>11.2e} | {m['phi11']:>13.1f} deg")

    # ---- verdict logic ----
    def _distinguish(m1, m2, tag):
        r11 = max(m1["|B11|"], 1e-30) / max(m2["|B11|"], 1e-30)
        if r11 < 1:
            r11 = 1.0 / r11
        r12 = max(m1["|B12|"], 1e-30) / max(m2["|B12|"], 1e-30)
        if r12 < 1:
            r12 = 1.0 / r12
        dp = abs(m1["phi11"] - m2["phi11"])
        if dp > 180:
            dp = 360 - dp
        mag_ok = r11 > 3 or r12 > 3
        pha_ok = dp > 30
        mag_maybe = 2 <= r11 <= 3 or 2 <= r12 <= 3
        pha_maybe = 15 <= dp <= 30

        if mag_ok or pha_ok:
            v = "DISTINGUISHABLE"
        elif mag_maybe or pha_maybe:
            v = "INCONCLUSIVE"
        else:
            v = "NOT DISTINGUISHABLE"

        print(f"  - {tag}: [{v}]")
        print(f"    mag ratio  |B11|: {r11:.1f}   |B12|: {r12:.1f}   "
              f"phase diff: {dp:.1f} deg")
        return v

    print("\nVERDICT:")
    v1 = _distinguish(metrics[1], metrics[0], "Crack  vs  Healthy")
    v2 = _distinguish(metrics[3], metrics[0], "Misalignment  vs  Healthy")
    v3 = _distinguish(metrics[1], metrics[3], "Crack  vs  Misalignment")

    if all(v == "DISTINGUISHABLE" for v in (v1, v2, v3)):
        overall = "GO"
    elif v3 == "NOT DISTINGUISHABLE":
        overall = "NO-GO"
    else:
        overall = "INCONCLUSIVE"

    print(f"\nOVERALL:  [{overall}]")
    return metrics, overall


# ===================================================================
# STEP 8 — Interpretation guide
# ===================================================================

def print_interpretation_guide():
    print("""
============================================================
INTERPRETATION GUIDE
============================================================

What to look for in the bispectrum plots:

1. HEALTHY rotor
   The bispectrum should show a single peak at (1X, 1X) = (25, 25) Hz
   from the unbalance response.  Minimal energy elsewhere.

2. CRACKED rotor
   The breathing crack introduces quadratic phase coupling.
   Expect strong peaks at (1X, 1X) and (1X, 2X) with specific phase
   relationships.  The peak at (1X, 1X) arises because the crack
   couples the 1X component with itself to produce 2X.

3. MISALIGNED rotor
   Misalignment also produces 2X, but the phase coupling pattern
   differs.  Expect peaks at (1X, 1X) and (1X, 2X) with DIFFERENT
   biphase angles compared to the crack case.

4. KEY DISCRIMINATOR
   The biphase (phase of the bispectrum) at (1X, 1X) should be
   different for crack vs. misalignment even if the magnitudes are
   similar.  This is the core hypothesis of the research.

If the bispectrum magnitudes AND phases look identical for crack
and misalignment, the research hypothesis needs revision.
""")


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("=" * 70)
    print("GO / NO-GO  FEASIBILITY TEST :  HOS-Based Fault Diagnosis")
    print("=" * 70)

    # ---- Step 1 : build rotors ----
    print("\n--- STEP 1 : Building rotor models ---")
    sinha_rotor = build_sinha_rotor()
    laval_rotor = build_laval_rotor()

    for name, rotor in [("Sinha", sinha_rotor), ("Laval", laval_rotor)]:
        modal = rotor.run_modal(speed=0)
        print(f"\n  {name} Rotor")
        print(f"    Nodes      : {len(rotor.nodes)}")
        print(f"    DOFs       : {rotor.ndof}")
        print(f"    Shaft elms : {len(rotor.shaft_elements)}")
        print(f"    Nat. freq. at 0 RPM (first 5):")
        for i, wn in enumerate(modal.wn[:5]):
            print(f"      fn{i + 1} = {wn / (2 * np.pi):.2f} Hz")

    # save TOML models
    sinha_rotor.save(OUTPUT_DIR / "sinha_rotor.toml")
    laval_rotor.save(OUTPUT_DIR / "laval_rotor.toml")
    print(f"\n  [saved] {OUTPUT_DIR / 'sinha_rotor.toml'}")
    print(f"  [saved] {OUTPUT_DIR / 'laval_rotor.toml'}")

    # rotor geometry plots  (plotly → PNG needs kaleido)
    for tag, rtr, fname in [
        ("Sinha", sinha_rotor, "sinha_rotor_geometry.png"),
        ("Laval", laval_rotor, "laval_rotor_geometry.png"),
    ]:
        try:
            fig = rtr.plot_rotor()
            fig.write_image(str(OUTPUT_DIR / fname))
            print(f"  [saved] {OUTPUT_DIR / fname}")
        except Exception as exc:
            print(f"  [note] {tag} geometry plot skipped ({exc})")

    # ---- Steps 2-5 : simulate, PSD, bispectrum ----
    print("\n--- STEPS 2-5 : Simulation  ·  PSD  ·  Bispectrum ---")
    print(f"  Speed     : {SPEED_RPM:.0f} RPM  ({SPEED_HZ:.0f} Hz)")
    print(f"  Duration  : {DURATION:.0f} s   fs = {FS} Hz")
    print(f"  Transient : discard first {TRANSIENT:.0f} s\n")

    t = np.arange(0, DURATION, 1.0 / FS)
    omega = SPEED_RAD

    case_defs = [
        {"label": "Healthy",
         "fault_type": None, "fault_params": None},
        {"label": "Crack (a/D=0.2)",
         "fault_type": "crack", "fault_params": {"a_D": CRACK_DEPTH_LIGHT}},
        {"label": "Crack (a/D=0.4)",
         "fault_type": "crack", "fault_params": {"a_D": CRACK_DEPTH_SEVERE}},
        {"label": "Misalignment",
         "fault_type": "misalignment",
         "fault_params": {"offset_mm": MISALIGNMENT_OFFSET}},
    ]

    cases_data = []
    trans_n = int(TRANSIENT * FS)

    for cd in case_defs:
        x = run_simulation(
            laval_rotor, cd["label"], t, SPEED_RAD, omega,
            fault_type=cd["fault_type"], fault_params=cd["fault_params"],
        )

        x_a = x[trans_n:]
        t_a = t[trans_n:]

        pf, ps = compute_psd(x_a, FS)

        print(f"    Computing bispectrum for {cd['label']} …")
        B, bic, bf = compute_bispectrum(x_a, FS)
        print(f"    [done] {cd['label']}")

        cases_data.append({
            "label": cd["label"],
            "x_analysis": x_a,
            "t_analysis": t_a,
            "psd_freqs": pf,
            "psd": ps,
            "B": B,
            "bicoherence": bic,
            "bisp_freqs": bf,
        })

    # ---- Step 6 : plots ----
    print("\n--- STEP 6 : Generating plots ---")
    generate_plots(cases_data, OUTPUT_DIR)

    # ---- Step 7 : summary ----
    metrics, overall = print_summary(cases_data)

    # ---- Step 8 : interpretation guide ----
    print_interpretation_guide()

    print("=" * 70)
    print("SIMULATION  COMPLETE")
    print("=" * 70)

    return cases_data, metrics, overall


# -------------------------------------------------------------------
if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    main()
