# Sinha acquisition vs simulation sampling

Technical note: align numerical simulation outputs with Sinha (2007) so that
higher-order spectra (HOS) estimated from ROSS probe signals are directly
comparable to the experimental bispectrum / trispectrum. Canonical numerical
defaults live in [`constants.py`](constants.py) (Sprint 01 Pattern A).

## Sinha (2007) — acquisition (experimental)

| Quantity | Value | Source |
|----------|-------|--------|
| Sampling rate \(f_s\) | 2560 samples/s | Sinha §3 (per sprint / paper) |
| Anti-aliasing low-pass | 1 kHz | Sinha §3 |
| Probe directions / axes | *Fill from Sinha §3 (paper PDF)* | — |
| Bearing 2 / measurement station layout | *Fill from Sinha §3 (paper PDF)* | — |

If your PDF is not in-repo, copy the exact sentences or figure captions into
this table when drafting the thesis Methods section.

## Simulation (ROSS / this repository)

| Quantity | Value | Notes |
|----------|-------|--------|
| Integration step `DT` | `1 / SINHA_FS_HZ ≈ 3.906e-4` s | Derived in [`constants.py`](constants.py); FEM steps at Sinha's acquisition period. |
| Simulated sampling rate `FS_SIM_HZ` | 2560 Hz | Equal to `SINHA_FS_HZ` by construction — no post-process resampling needed. |
| Steady-state window (default) `T_SHORT` | 0–2 s (5 120 samples) | Orbits, phase sweeps, and every non-HOS plot in notebooks `01`–`04`. |
| HOS window `T_LONG` | 0–25 s (64 000 samples) | Reserved for Sprint 02+ bispectrum / trispectrum estimation. |
| `FREQ_RANGE` (plots) | 0–200 Hz | DFFT display band. |
| Frozen geometry | [`sinha_rotor.toml`](sinha_rotor.toml) | Do not retune silently in Sprint 01. |

## Default HOS analysis chain (Sprints 02–03)

Because `DT = 1 / SINHA_FS_HZ`, simulated probe time series already live on
Sinha's sampling grid. The HOS pipeline therefore only needs to

1. Extract the steady-state portion of a `T_LONG` run.
2. Apply the same 1 kHz anti-aliasing low-pass (`SINHA_AA_CUTOFF_HZ`) that
   Sinha used before segmenting.
3. Segment into overlapping records and estimate bispectrum / trispectrum
   using the Sinha (2007) §3.3 parameters.

If integration stability ever forces `DT` below `1 / SINHA_FS_HZ`, decimate
probe time series to `SINHA_FS_HZ` before segmentation — and update this note.

Constants for the HOS module (import from [`constants.py`](constants.py)):

- `SINHA_FS_HZ = 2560`
- `SINHA_AA_CUTOFF_HZ = 1000`
- `SINHA_HOS_DF_HZ = 1.25`
- `SINHA_HOS_N_SEGMENTS = 50`
- `SINHA_HOS_OVERLAP = 0.5`

## Parameter provenance (thesis Methods)

| Symbol | Value (summary) | Origin | Conclusion for the paper |
|--------|-----------------|--------|---------------------------|
| `UNB_MAG` | `2e-4` kg·m | Shared across `01`–`04` | Single residual unbalance level for cross-notebook comparison. |
| `UNB_PHASE` | `4π/3` rad | `constants.py`; canonical after Sprint 01 | State the canonical phase explicitly in Methods; notebook `04` previously used `3π/4` inline. |
| `SPEEDS` / `SPEED_CRACK_*` | 650, 750 rpm | `02`, `03`, `04` crack cases | Crack and healthy baselines at two speeds. |
| `SPEED_MIS_*` | 750, 900 rpm | `04` misalignment cases | Misalignment-only speed pair for integrated comparison. |
| `MIS_X`, `MIS_Y` | 1.0 mm, 0.5 mm | `04` flexible misalignment | Parallel misalignment excitation geometry for coupling model. |
| `CRACK_RATIO` | 0.5 | `03` default cap / `04` narrative | Default Mayes/Gasch depth ratio; other depths swept locally in `03`. |
| `DT`, `T_SHORT`, `T_LONG` | `1/2560` s, 2 s, 25 s | Shared time-domain defaults | State `fs_sim = 2560 Hz` and the 2 s / 25 s windows in Methods. |
| `DISK_NODE`, `CRACK_NODE`, `PROBE_NODE` | 6, 7, 10 | `00` build → `sinha_rotor.toml` | Match published disk / crack / probe stations. |
| `SINHA_*` | see constants | Sinha §3 / §3.3 (sprint) | HOS estimator settings for literature-aligned post-processing. |

## Sprint 01 changelog

- Moved duplicate definitions from `04_sinha_fault_analysis.ipynb` into
  [`constants.py`](constants.py): `UNB_MAG`, `UNB_PHASE` (canonical `4π/3`),
  `SPEED_CRACK_*`, `SPEED_MIS_*`, `MIS_X`, `MIS_Y`, `CRACK_RATIO`, `DT`,
  `T_SHORT`, `T_LONG`, `FREQ_RANGE`, node indices.
- Added `FS_SIM_HZ`, `SINHA_FS_HZ`, `SINHA_AA_CUTOFF_HZ`, `SINHA_HOS_DF_HZ`,
  `SINHA_HOS_N_SEGMENTS`, `SINHA_HOS_OVERLAP` for Sprint 02.
- Set `DT = 1 / SINHA_FS_HZ` so the simulation rate matches Sinha's
  acquisition rate directly.
- Kept `SPEED_0` / `SPEED_1` as aliases of the crack speeds for backward
  compatibility.
- [`sinha_rotor.toml`](sinha_rotor.toml) unchanged.
- Extracted `get_harmonic_amplitude` and `probe_dof_indices` helpers from
  notebooks `02` / `03` into [`sinha_helpers.py`](sinha_helpers.py).
- Pattern **(A)** documented in
  [`sprints/sprint-01-foundation-and-sinha-acquisition.md`](sprints/sprint-01-foundation-and-sinha-acquisition.md):
  notebooks import `constants`; overrides only for sweeps (e.g. phase grid in
  `02`).
