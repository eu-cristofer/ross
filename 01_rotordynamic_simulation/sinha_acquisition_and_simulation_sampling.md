# Sinha acquisition vs simulation sampling

Technical note for Sprint 01: align numerical simulation outputs with Sinha (2007) before higher-order spectra (HOS) code (Sprint 02+). Canonical numerical defaults live in [`constants.py`](constants.py) (Option A).

## Sinha (2007) — acquisition (experimental)

| Quantity | Value | Source |
|----------|-------|--------|
| Sampling rate \(f_s\) | 2560 samples/s | Sinha §3 (per sprint / paper) |
| Anti-aliasing low-pass | 1 kHz | Sinha §3 |
| Probe directions / axes | *Fill from Sinha §3 (paper PDF)* | — |
| Bearing 2 / measurement station layout | *Fill from Sinha §3 (paper PDF)* | — |

If your PDF is not in-repo, copy the exact sentences or figure captions into this table when drafting the thesis Methods section.

## Simulation (ROSS / this repository)

| Quantity | Value | Notes |
|----------|-------|--------|
| Integration step `DT` | `1e-3` s | From [`constants.py`](constants.py) |
| Implied \(f_{s,\mathrm{sim}} = 1/\mathrm{DT}\) | 1000 Hz | Coarser than Sinha’s 2560 Hz |
| `FREQ_RANGE` (plots) | 0–200 Hz | DFFT display band |
| Frozen geometry | [`sinha_rotor.toml`](sinha_rotor.toml) | Do not retune silently in Sprint 01 |

## Default HOS analysis chain (Sprints 02–03)

**Recommendation:** Keep integrating the rotor at `DT` chosen for stability and cost. For **comparison to Sinha’s bispectrum pipeline**, post-process probe time series on a steady-state window by **resampling to `SINHA_FS_HZ` (2560 Hz)** so FFT bin spacing matches the experimental record, then apply a **1 kHz** low-pass (or the same corner as Sinha’s anti-aliasing filter) before segmenting for HOS. That mimics the acquisition chain in §3 while allowing the FEM step to remain at 1000 Hz during time integration.

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
| `UNB_PHASE` | `4π/3` rad | `constants.py`; used by `01`–`03` | Canonical phase after Sprint 01. Notebook `04` previously used `3π/4` inline—cite regenerated figures or document the change. |
| `SPEEDS` / `SPEED_CRACK_*` | 650, 750 rpm | `02`, `03`, `04` crack cases | Crack and healthy baselines at two speeds. |
| `SPEED_MIS_*` | 750, 900 rpm | `04` misalignment cases | Misalignment-only speed pair for integrated comparison. |
| `MIS_X`, `MIS_Y` | 1.0 mm, 0.5 mm | `04` flexible misalignment | Parallel misalignment excitation geometry for coupling model. |
| `CRACK_RATIO` | 0.5 | `03` default cap / `04` narrative | Default Mayes/Gasch depth ratio; other depths swept locally in `03`. |
| `DT`, `T` | 1 ms, 0–2 s | Shared time-domain defaults | State `fs_sim` and steady-state extraction window in Methods. |
| `DISK_NODE`, `CRACK_NODE`, `PROBE_NODE` | 6, 7, 10 | `00` build → `sinha_rotor.toml` | Match published disk / crack / probe stations. |
| `SINHA_*` | see constants | Sinha §3 / §3.3 (sprint) | HOS estimator settings for literature-aligned post-processing. |

## Sprint 01 changelog

- Moved duplicate definitions from `04_sinha_fault_analysis.ipynb` into [`constants.py`](constants.py): `UNB_MAG`, `UNB_PHASE` (canonical `4π/3`), `SPEED_CRACK_*`, `SPEED_MIS_*`, `MIS_X`, `MIS_Y`, `CRACK_RATIO`, `DT`, `T`, `FREQ_RANGE`, node indices.
- Added `FS_SIM_HZ`, `SINHA_FS_HZ`, `SINHA_AA_CUTOFF_HZ`, `SINHA_HOS_DF_HZ`, `SINHA_HOS_N_SEGMENTS`, `SINHA_HOS_OVERLAP` for Sprint 02.
- Kept `SPEED_0` / `SPEED_1` as aliases of the crack speeds for backward compatibility.
- [`sinha_rotor.toml`](sinha_rotor.toml) unchanged.
- Pattern **(A)** documented in [`sprints/sprint-01-foundation-and-sinha-acquisition.md`](sprints/sprint-01-foundation-and-sinha-acquisition.md): notebooks import `constants`; overrides only for sweeps (e.g. phase grid in `02`).
