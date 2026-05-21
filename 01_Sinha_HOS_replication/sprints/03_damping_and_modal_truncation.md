# Sprint 03 — Damping calibration + modal-truncation convergence

> **Effort:** 2 days.
> **Blocks:** Sprints 04, 05, 06 (every HOS amplitude claim depends on damping and modal truncation).
> **Unblocked by:** Sprints 00, 01, 02.
> **Artefacts produced:** a damping-tuned `01_rotordynamic_simulation/sinha_rotor.toml` (previous copy saved as `sinha_rotor_pre_damping.toml`), a short `01_rotordynamic_simulation/00b_damping_check.ipynb`, and a convergence table in Markdown at `01_rotordynamic_simulation/sprints/03_convergence_table.md`.

## Why this sprint exists

Sinha §5 specifies **stiffness-proportional damping with modal damping 0.3 % at the first mode**. Bispectral amplitudes at B22 and tri-spectral amplitudes at T222 scale sensitively with damping (lightly damped → resonant amplification → larger super-harmonics). Without calibrating to Sinha's ζ₁ = 0.3 %, the amplitude ratios that define the Sprint 05 and 06 exit criteria will be biased.

Separately, the **audit H4** flags that every downstream `run_crack` / `run_misalignment` call uses `model_reduction={"num_modes": 12}`. The Sinha rotor has 13 nodes and up to ~12 bending modes representable in the frequency band of interest, but HOS bins at (2X, 2X), (3X, 3X), and (2X, 3X) for 900 rpm reach 45–90 Hz — where residual modal response still matters. The truncation must be convergence-checked before locking the Sprint 05/06 campaign amplitudes.

## Prerequisites

- Sprints 00, 01, 02 complete.
- `sinha_rotor.toml` present with calibrated `kxx` (Sprint 00).
- `run_campaign.py` working (Sprint 02).

## Work items

### 1. Damping calibration — `tune_damping`

Add to `01_rotordynamic_simulation/00_sinha_rotor.ipynb` (or a small helper script `tune_damping.py`) a Brent-method fit, exactly mirroring the `tune_kxx` pattern:

```python
from scipy.optimize import brentq

def first_mode_zeta(rotor) -> float:
    """Return ζ of mode 1 as a scalar (between 0 and 1)."""
    modal = rotor.run_modal(speed=0)
    return float(np.real(modal.damping_ratio[0]))

def set_rayleigh_damping(rotor, alpha: float, beta: float):
    """Scatter Rayleigh damping C = α M + β K into the rotor's element matrices.

    Sinha §5 uses stiffness-proportional damping, i.e. α = 0, β chosen so
    ζ₁ ≈ 0.003. In ROSS, this is done by setting bearing damping and/or
    augmenting each shaft element's damping matrix — depends on the ROSS
    version. Implement whichever path works; document it.
    """
    ...

def tune_beta_damping(beta: float, target_zeta: float = 0.003) -> float:
    r = build_rotor(... , cxx=beta_to_bearing_cxx(beta))   # or direct shaft-C patch
    return first_mode_zeta(r) - target_zeta

beta_opt = brentq(tune_beta_damping, 1e-6, 1e-2, xtol=1e-7)
```

**Implementation reality check.** ROSS does not expose a single "stiffness-proportional damping coefficient" on the `Rotor`. The two paths that work:

1. **Scale bearing `cxx`/`cyy`** alongside `kxx`/`kyy`. Simplest. Effective ζ₁ depends on how much of the first-mode strain energy is in the bearings — verify numerically.
2. **Patch each `ShaftElement.C_element` with `β · K_element`** before building the rotor. More faithful to Sinha §5. Requires a custom rebuild helper.

Pick (1) first; if the achievable ζ₁ range doesn't span 0.3 %, fall back to (2). Record which path was chosen in the sprint notebook's markdown and in the `constants.py` docstring.

### 2. Persist the tuned rotor

```python
# Back up first
import shutil, pathlib
src = pathlib.Path("sinha_rotor.toml")
shutil.copy(src, src.with_stem(src.stem + "_pre_damping"))

# Re-save with the new damping
rotor_damped = build_rotor(... , cxx=<tuned>, kxx=<from Sprint 00>)
assert abs(first_mode_zeta(rotor_damped) - 0.003) <= 0.0005
rotor_damped.save("sinha_rotor.toml")
```

Sprint 00's modal assertion (`|f1 − 27.50| ≤ 0.05 Hz`) must still pass on the damped rotor. Damping shifts the damped frequency `wd` marginally but the *undamped* `wn[0]` is unchanged — do the Sprint 00 assertion on `wn`, not `wd`.

### 3. Modal-truncation convergence study

New cells in `00b_damping_check.ipynb`:

```python
import numpy as np, ross as rs
from signal_utils import bispectrum, downsample_to, add_awgn
from constants import (DT_SIM, T_LONG, FS_ACQ_EXP, AA_CUTOFF, SNR_DB,
                       DISK_NODE, CRACK_NODE, PROBE_NODE, UNB_MAG, UNB_PHASE,
                       CRACK_RATIO)

rotor = rs.Rotor.load("sinha_rotor.toml")
speed = rs.Q_(750, "rpm").to("rad/s").m

rows = []
for n_modes in [12, 24, 36]:
    res = rotor.run_crack(
        n=CRACK_NODE, depth_ratio=CRACK_RATIO, crack_model="Mayes",
        node=[DISK_NODE],
        unbalance_magnitude=[UNB_MAG.to("kg*m").m],
        unbalance_phase=[UNB_PHASE.to("rad").m],
        speed=speed, t=T_LONG,
        model_reduction={"num_modes": n_modes},
    )
    px, py = rotor.number_dof * PROBE_NODE, rotor.number_dof * PROBE_NODE + 1
    x = res.yout[:, px]
    x = downsample_to(x, 1/DT_SIM, FS_ACQ_EXP, AA_CUTOFF)
    x = add_awgn(x, SNR_DB, rng=np.random.default_rng(0))
    B, b2, freqs = bispectrum(x, FS_ACQ_EXP)
    f1 = 750/60
    i1 = np.argmin(np.abs(freqs - f1))
    i2 = np.argmin(np.abs(freqs - 2*f1))
    rows.append((n_modes, abs(B[i1,i1]), abs(B[i2,i2]), abs(B[i1,i2])))

print(f"{'num_modes':>10} | {'|B11|':>10} | {'|B22|':>10} | {'|B12|':>10}")
for r in rows:
    print(f"{r[0]:>10} | {r[1]:>10.3e} | {r[2]:>10.3e} | {r[3]:>10.3e}")

# Convergence check:
ref_B22 = rows[-1][2]
for n, _, B22, _ in rows:
    rel = abs(B22 - ref_B22) / max(abs(ref_B22), 1e-30)
    print(f"num_modes={n}  Δ|B22| vs 36-mode = {rel*100:.2f}%")
```

Commit the printed table to `01_rotordynamic_simulation/sprints/03_convergence_table.md`. Decide:

- If `num_modes=12` is within 5 % of `num_modes=36` on every column, **keep** `num_modes=12` as the project default (saves ≈ 3 × runtime).
- If not, raise the default to the first `num_modes` that *is* within 5 %. Record the new default as `NUM_MODES` in `constants.py` and update `run_campaign.py`.

### 4. Re-run `run_campaign.py`

Damping calibration changes every time series. Delete the old HDF5, re-run:

```bash
rm 01_rotordynamic_simulation/results/campaign.h5
python 01_rotordynamic_simulation/run_campaign.py
```

Re-assert Sprint 02 Tests D and E on the new file.

## Exit criteria

- [ ] `sinha_rotor.toml` re-saved with `|ζ₁ − 0.003| ≤ 5e-4`.
- [ ] `sinha_rotor_pre_damping.toml` exists alongside (traceability).
- [ ] Sprint 00's Cell A assertion (`|f1 − 27.50| ≤ 0.05`) still passes.
- [ ] Convergence table at `01_rotordynamic_simulation/sprints/03_convergence_table.md` lists `(n_modes, |B11|, |B22|, |B12|)` for `n_modes ∈ {12, 24, 36}`.
- [ ] `NUM_MODES` exported from `constants.py` at the chosen default (with justification in docstring).
- [ ] `run_campaign.py` uses `NUM_MODES` (not hardcoded 12) and re-runs clean on the damping-tuned rotor.

## Implementation notes

- **ζ₁ definition:** `modal.damping_ratio[0]` is what ROSS returns; this is the critical-damping ratio, dimensionless, target 0.003. Not to be confused with loss factor (= 2ζ).
- **Brent bracket:** pick `[1e-6, 1e-2]` for `beta` (or equivalent `cxx` scale) — generous enough that the root is guaranteed interior, tight enough to converge fast.
- **xtol:** 1e-7 on beta yields ζ₁ to ~1e-5 precision; Sinha's 0.3 % is itself a nominal number, so this is plenty.
- **Sensitivity check:** compute ζ₁ across speeds `{0, 100, 300, 500 rad/s}` after calibration. If gyroscopic coupling moves ζ₁ outside `[0.002, 0.004]` anywhere in the Sprint 05/06 speed range, flag it in the sprint notes — the Methods section needs to state "nominal ζ₁ = 0.3 % at rest".

## Dependencies / hand-offs

- Directly enables Sprints 04–06: from this point on, every HOS amplitude is computed against the Sinha-damped rotor, not the lightly damped default.
- Sprint 07 cites this sprint in the Methods paragraph on "damping assumption".

## References

- Sinha (2007) §5, paragraph "The stiffness proportional damping matrix was also included in the model using experimentally measured modal damping of 0.3 % at the first mode."
- Audit: `01_rotordynamic_simulation/05_synthesis.ipynb` §3.2 H4 (modal truncation), §3.3 M5 (steady-state heuristic is downstream of damping).
- Existing pattern: `01_rotordynamic_simulation/00_sinha_rotor.ipynb` — `tune_kxx` via `brentq` (clone verbatim for `tune_damping`).
