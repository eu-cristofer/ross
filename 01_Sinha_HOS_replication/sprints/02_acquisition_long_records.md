# Sprint 02 — Sinha-matched acquisition + persisted long records

> **Effort:** 3 days.
> **Blocks:** Sprints 04, 05, 06, 07.
> **Unblocked by:** Sprint 01 (`bispectrum` must be callable).
> **Artefacts produced:** extended `constants.py`, `01_rotordynamic_simulation/run_campaign.py`, `01_rotordynamic_simulation/results/campaign.h5`, two integration-test cells appended to `06_hos_validation.ipynb`.

## Why this sprint exists

The current records are 2 s at fs = 1000 Hz = **2000 samples** total; after discarding transients, ~1000 samples remain. Sinha's estimator (Sprint 01) needs **50 segments × 50 % overlap × Δf = 1.25 Hz**. At fs = 2560 Hz that means Nfft = 2048 per segment and `total_samples = Nfft · (1 + 0.5·(N_seg − 1)) ≈ 52 k samples ≈ 20.3 s`. The current data is ~50× too short and at the wrong sample rate (Nyquist 500 Hz conflicts with the declared `SINHA_AA_CUTOFF_HZ = 1000`).

Sinha §5 resolves this in a specific way that this sprint must follow verbatim: integrate the FE at a very fine step (`dt = 1/10000 s`, fs_sim = 10 kHz), then LP filter at 1 kHz, then downsample to 1 kHz, then inject noise to achieve SNR = 40 dB. That protocol is what makes Sinha's FE result (Fig. 10) comparable to his experimental data at fs = 2560 Hz with a 1 kHz AA filter — the information content above 1 kHz is matched.

In parallel, this sprint fixes **audit H1** (the mis-paired healthy baseline at 900 rpm in `04_sinha_fault_analysis.ipynb`) because the campaign driver replaces that notebook's hand-rolled simulation calls anyway.

## Prerequisites

- Sprint 01 complete — `signal_utils.bispectrum`, `downsample_to`, `add_awgn` are importable.
- `h5py` installed in the conda env. If missing: `pip install h5py` inside `conda activate research`.
- `sinha_rotor.toml` present and passing Sprint 00's modal assertion.

## Work items

### 1. Extend `01_rotordynamic_simulation/constants.py`

Add these constants, keeping `__all__` alphabetical and adding provenance paragraphs to the module docstring:

```python
# Simulation integrator step (Sinha §5: dt = 1/10000 s for Newmark-β).
DT_SIM   = 1.0 / 10_000          # s
FS_SIM   = 1.0 / DT_SIM           # Hz, = 10_000

# Long record for HOS: 25 s covers 50 segments × 50% overlap × Δf=1.25 Hz
# at the post-downsample 1 kHz rate, with a 2 s margin for transient cut-off.
T_LONG   = np.arange(0.0, 25.0, DT_SIM)    # 250_000 samples

# Acquisition / anti-aliasing chain (Sinha §3: fs=2560 Hz, AA=1 kHz;
# Sinha §5: downsampled to 1 kHz after LP filtering at 1 kHz).
FS_ACQ_EXP = 2560.0   # Hz, Sinha experimental DAQ rate
FS_ACQ_FE  = 1000.0   # Hz, Sinha's own FE post-downsample rate (used by Sprint 04)
AA_CUTOFF  = 1000.0   # Hz, matches SINHA_AA_CUTOFF_HZ

# Additive white Gaussian noise target (Sinha §5: SNR 40 dB).
SNR_DB   = 40.0

# Rename the legacy 2 s / 1 kHz grid for the existing orbit/phase-sweep notebooks.
DT_SHORT = DT
T_SHORT  = T
```

Keep the old `DT` / `T` names available (as aliases if needed) so `01_sinha_rotor_modal.ipynb`, `02_sinha_unbalance_phase_crack.ipynb`, `03_sinha_crack_model_comparison.ipynb`, `04_sinha_fault_analysis.ipynb` continue to run unmodified.

### 2. `01_rotordynamic_simulation/run_campaign.py` — the driver

A standalone script (no Jupyter needed) that builds the Sprint-05/06 dataset.

```python
"""Sinha-matched simulation campaign.

Run with:  python -m 01_rotordynamic_simulation.run_campaign

Writes 01_rotordynamic_simulation/results/campaign.h5 with one group per case.
"""
from __future__ import annotations
import argparse, datetime, hashlib, os, sys, uuid
from pathlib import Path
from typing import Iterable

import h5py, numpy as np, ross as rs

from signal_utils import downsample_to, add_awgn
from constants import (
    BEARING_1_NODE, BEARING_2_NODE, DISK_NODE, CRACK_NODE, PROBE_NODE,
    UNB_MAG, UNB_PHASE,
    DT_SIM, T_LONG, FS_ACQ_EXP, FS_ACQ_FE, AA_CUTOFF, SNR_DB,
    CRACK_RATIO, MIS_X, MIS_Y,
)

# ----- DoE grid (minimum for Sprints 05 and 06) -----------------------------
CONDITIONS = ["healthy", "crack", "misalignment"]
SPEEDS_RPM = [650, 750, 900]   # shared grid; fixes audit C4
# Crack at 650/750 for Sprint 05; misalignment at 750/900 for Sprint 06;
# healthy at all three to pair baselines correctly (fixes audit H1).

def _dof_xy(rotor, node):
    ndof = rotor.number_dof
    return ndof * node, ndof * node + 1

def _simulate_one(rotor, condition: str, speed_rpm: int, rng) -> dict:
    """Return a dict of time-series numpy arrays + a metadata dict."""
    speed = rs.Q_(speed_rpm, "rpm").to("rad/s").m
    t = T_LONG

    if condition == "healthy":
        F = np.zeros((len(t), rotor.ndof))
        dx, dy = _dof_xy(rotor, DISK_NODE)
        unb_mag = UNB_MAG.to("kg*m").m
        phase   = UNB_PHASE.to("rad").m
        f_mag   = unb_mag * speed**2
        F[:, dx] = f_mag * np.cos(speed * t + phase)
        F[:, dy] = f_mag * np.sin(speed * t + phase)
        res = rotor.run_time_response(speed=speed, F=F, t=t)

    elif condition == "crack":
        res = rotor.run_crack(
            n=CRACK_NODE,
            depth_ratio=CRACK_RATIO,
            crack_model="Mayes",  # Sinha §5's (1-cos θ)Δk/2 is exactly Mayes
            node=[DISK_NODE],
            unbalance_magnitude=[UNB_MAG.to("kg*m").m],
            unbalance_phase=[UNB_PHASE.to("rad").m],
            speed=speed,
            t=t,
            model_reduction={"num_modes": 24},   # Sprint 03 may raise this
        )

    elif condition == "misalignment":
        res = rotor.run_misalignment(
            coupling="flex",
            n=DISK_NODE,
            mis_type="parallel",
            mis_distance_x=MIS_X.to("m").m,
            mis_distance_y=MIS_Y.to("m").m,
            mis_angle=0.0,
            radial_stiffness=4e4,
            bending_stiffness=3.8e4,
            input_torque=0.0,
            load_torque=0.0,
            method="newmark",
            node=[DISK_NODE],
            unbalance_magnitude=[UNB_MAG.to("kg*m").m],
            unbalance_phase=[UNB_PHASE.to("rad").m],
            speed=speed,
            t=t,
        )
    else:
        raise ValueError(condition)

    px, py = _dof_xy(rotor, PROBE_NODE)
    dx_d, dy_d = _dof_xy(rotor, DISK_NODE)

    y_sim = res.yout  # fs = FS_SIM
    # Downsample to experimental rate with the Sinha anti-alias chain:
    x_probe = downsample_to(y_sim[:, px], fs_sim=1.0/DT_SIM, fs_out=FS_ACQ_EXP, aa_cutoff_hz=AA_CUTOFF)
    y_probe = downsample_to(y_sim[:, py], fs_sim=1.0/DT_SIM, fs_out=FS_ACQ_EXP, aa_cutoff_hz=AA_CUTOFF)
    x_disk  = downsample_to(y_sim[:, dx_d], fs_sim=1.0/DT_SIM, fs_out=FS_ACQ_EXP, aa_cutoff_hz=AA_CUTOFF)
    y_disk  = downsample_to(y_sim[:, dy_d], fs_sim=1.0/DT_SIM, fs_out=FS_ACQ_EXP, aa_cutoff_hz=AA_CUTOFF)

    # Noise injection (Sinha §5: SNR 40 dB). Apply after downsampling.
    x_probe_n = add_awgn(x_probe, SNR_DB, rng=rng)
    y_probe_n = add_awgn(y_probe, SNR_DB, rng=rng)

    arrays = dict(
        t_sim   = t,                                # full 10 kHz grid
        x_probe = x_probe, y_probe = y_probe,       # clean downsampled
        x_disk  = x_disk,  y_disk  = y_disk,        # clean downsampled (disk)
        x_probe_noisy = x_probe_n, y_probe_noisy = y_probe_n,
    )
    meta = dict(
        condition=condition, speed_rpm=speed_rpm,
        fs_sim=1.0/DT_SIM, fs_acq=FS_ACQ_EXP, aa_cutoff=AA_CUTOFF,
        snr_db=SNR_DB,
        depth_ratio=CRACK_RATIO if condition == "crack" else 0.0,
        mis_x=MIS_X.to("m").m if condition == "misalignment" else 0.0,
        mis_y=MIS_Y.to("m").m if condition == "misalignment" else 0.0,
        unb_mag_kgm=UNB_MAG.to("kg*m").m,
        unb_phase_rad=UNB_PHASE.to("rad").m,
        ross_version=rs.__version__,
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        case_id=uuid.uuid4().hex[:12],
    )
    return {"arrays": arrays, "meta": meta}

def _write_case(h5: h5py.File, case: dict) -> str:
    g = h5.create_group(f"case_{case['meta']['case_id']}")
    for k, v in case["arrays"].items():
        g.create_dataset(k, data=v, compression="gzip", compression_opts=4)
    for k, v in case["meta"].items():
        g.attrs[k] = v
    return g.name

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/campaign.h5",
                    help="HDF5 path relative to 01_rotordynamic_simulation/")
    ap.add_argument("--conditions", nargs="+", default=CONDITIONS)
    ap.add_argument("--speeds", nargs="+", type=int, default=SPEEDS_RPM)
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args(argv)

    here = Path(__file__).resolve().parent
    out = here / args.out
    out.parent.mkdir(parents=True, exist_ok=True)

    rotor = rs.Rotor.load(str(here / "sinha_rotor.toml"))
    rng = np.random.default_rng(args.seed)

    with h5py.File(out, "w") as h5:
        h5.attrs["created"] = datetime.datetime.now().isoformat()
        h5.attrs["ross_version"] = rs.__version__
        for cond in args.conditions:
            for rpm in args.speeds:
                # Skip combinations that are outside Sinha's scope:
                if cond == "crack" and rpm == 900:
                    continue
                if cond == "misalignment" and rpm == 650:
                    continue
                print(f"[campaign] {cond} @ {rpm} rpm …")
                case = _simulate_one(rotor, cond, rpm, rng)
                name = _write_case(h5, case)
                print(f"[campaign] wrote {name}")

    print(f"[campaign] done → {out}")

if __name__ == "__main__":
    main()
```

Minimum campaign runs: 3 healthy (650 / 750 / 900) + 2 crack (650 / 750) + 2 misalignment (750 / 900) = **7 cases**. Extensible to a full DoE later without changing the driver contract.

### 3. Integration tests in `06_hos_validation.ipynb`

Append two cells:

```python
# Test D — long-record pipeline end-to-end on a real simulation.
import h5py
from pathlib import Path
from signal_utils import bispectrum

h5_path = Path("results/campaign.h5")
assert h5_path.exists(), "run `python run_campaign.py` first"

with h5py.File(h5_path, "r") as h5:
    # Find the crack @ 650 rpm case and run HOS on it.
    for name, g in h5.items():
        if g.attrs["condition"] == "crack" and int(g.attrs["speed_rpm"]) == 650:
            x = g["x_probe_noisy"][:]
            fs = float(g.attrs["fs_acq"])
            break

B, b2, freqs = bispectrum(x, fs)
f1_hz = 650 / 60  # Hz — 1X at 650 rpm
i_f1 = np.argmin(np.abs(freqs - f1_hz))
# B11 must sit within ±1 bin of (f1, f1):
peak = np.unravel_index(np.argmax(np.abs(B[:i_f1*2, :i_f1*2])), B[:i_f1*2, :i_f1*2].shape)
assert abs(peak[0] - i_f1) <= 1 and abs(peak[1] - i_f1) <= 1
```

```python
# Test E — the noise injection moved the SNR to the target.
from signal_utils import add_awgn
clean = g["x_probe"][:]
noisy = g["x_probe_noisy"][:]
snr_measured = 10 * np.log10(np.var(clean) / np.var(noisy - clean))
assert abs(snr_measured - 40) < 1.0, f"SNR = {snr_measured:.2f} dB, want 40"
```

## Exit criteria

- [ ] `constants.py` exports `DT_SIM`, `T_LONG`, `FS_ACQ_EXP`, `FS_ACQ_FE`, `AA_CUTOFF`, `SNR_DB` with the values above; `__all__` updated; docstring provenance paragraph added.
- [ ] Notebooks 01–04 still run (no breakage from the `DT` / `T` rename if you keep aliases).
- [ ] `python 01_rotordynamic_simulation/run_campaign.py` completes in < 4 h and writes 7 groups to `results/campaign.h5`.
- [ ] Test D: B11 at 650 rpm lands within ±1 bin of (10.83, 10.83) Hz.
- [ ] Test E: injected noise is within ±1 dB of 40 dB SNR on the probe signal.
- [ ] Audit H1 closed — `04_sinha_fault_analysis.ipynb`'s hand-rolled `cases` list deleted (or refactored to load from `campaign.h5`).

## Implementation notes

- **Noise placement:** inject noise *after* downsampling (Sinha §5 sequence). Injecting before downsampling would be filtered out by the AA stage.
- **Anti-alias margin:** set the Butterworth cut-off to 0.4 × `FS_ACQ_EXP` (i.e. 1024 Hz at fs_acq = 2560 Hz), not exactly `AA_CUTOFF = 1000 Hz`, so the stop-band is respected. Document this choice in the docstring of `downsample_to`.
- **RNG provenance:** the seed lives in the driver; propagate into `add_awgn` so the same random stream is used across cases and re-runs are bit-identical.
- **Compression:** gzip level 4 is a good time/size tradeoff for the 40+ MB per case that this campaign will produce.
- **Memory:** `T_LONG` at 10 kHz = 250 000 samples per DOF; for a 13-node 6-DOF-per-node rotor that is ~150 MB per simulation *before* writing. Consider extracting only the probe + disk DOFs inside `_simulate_one` and discarding the full `yout` before moving on.

## Dependencies / hand-offs

- Sprints 04, 05, 06 all open `campaign.h5` as read-only and never re-simulate.
- Sprint 03's damping calibration will re-save `sinha_rotor.toml` — after which the campaign must be re-run once. Budget that time in Sprint 03.

## References

- Sinha (2007) §3 (DAQ: fs=2560 Hz, AA=1 kHz), §5 (FE: dt=1/10000 s, LP=1 kHz, downsample to 1 kHz, SNR=40 dB).
- Audit: `01_rotordynamic_simulation/05_synthesis.ipynb` §3.1 C2, C3, C4 (record length, fs, speed-grid) and §3.2 H1 (baseline pairing).
- ROSS APIs: `rs.Rotor.run_crack`, `rs.Rotor.run_misalignment`, `rs.Rotor.run_time_response` — see existing usage in notebooks 02, 03, 04.
