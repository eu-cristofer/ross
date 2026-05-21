# Sprint 04 — Reproduce Sinha's FE simulation (Figs. 9 & 10)

> **Effort:** 3–5 days.
> **Blocks:** Sprint 07.
> **Unblocked by:** Sprints 00, 01, 02, 03.
> **Artefacts produced:** `01_rotordynamic_simulation/07_sinha_fig10_replication.ipynb`, PNGs in `01_rotordynamic_simulation/results/figures/sprint_04/`, a one-page summary appended to `01_rotordynamic_simulation/sprints/04_sinha_fe_replication.md` (this file) after execution.

## Why this sprint exists

Sinha's own **FE simulation** (§5, Fig. 10) is the cleanest validation target available, because it is FE-to-FE comparison: no experimental rig variance, no unknown coupling, no measurement noise other than the injected 40 dB AWGN. If the ROSS pipeline *cannot* match Sinha's Fig. 10 topology at 772.5 RPM, no downstream claim about 650 / 750 / 900 RPM experimental data is defensible.

This sprint is also the first place where Sprint 01's `plot_bispectrum_surface` and `plot_trispectrum_balls` visualizers meet real simulation output.

## The Sinha §5 recipe, verbatim

| Parameter | Sinha value | How to implement in ROSS |
|---|---|---|
| Element type | 2-node Euler–Bernoulli beam, 4 DOF/node | ROSS `ShaftElement` default |
| Damping | stiffness-proportional, ζ₁ = 0.3 % at first mode | Sprint 03 |
| Unbalance | "small unbalance at the disk" (magnitude unspecified) | Use current `UNB_MAG = 2e-4 kg·m` at `DISK_NODE` |
| Crack model | `(1 − cos θ) Δk / 2` | Mayes in ROSS (exact match) |
| Crack depth | 0.5 D | `depth_ratio=0.5` |
| Speed | 772.5 RPM (≈ ½ f₁ = ½ · 27.50 Hz · 60 ≈ 825; Sinha gives 772.5 explicitly) | `rs.Q_(772.5, "rpm")` |
| Integrator | Newmark-β | ROSS `run_crack` default is Newmark-β — verify |
| Integration step | dt = 1/10000 s | `DT_SIM` from Sprint 02 |
| AA filter | LP 1 kHz | `downsample_to(..., aa_cutoff_hz=1000)` |
| Downsample | to 1 kHz | `fs_out=FS_ACQ_FE = 1000` |
| Noise | 40 dB SNR | `add_awgn(..., snr_db=40)` |
| HOS estimator | 50 segments, 50 % overlap, Δf = 1.25 Hz | `bispectrum(..., fs=1000)` with Sprint 01 defaults |
| Trispectrum threshold | amplitudes > 0.1 plotted | `trispectrum(..., threshold=0.10)` |

Note that Sinha's downsample target is **1 kHz**, not 2560 Hz. For this sprint only, override `FS_ACQ_EXP` with `FS_ACQ_FE = 1000` so the estimator settings mirror his exactly.

## Prerequisites

- Sprints 00–03 complete.
- `sinha_rotor.toml` is the damping-tuned version from Sprint 03.
- `signal_utils.bispectrum`, `trispectrum`, `downsample_to`, `add_awgn` work per Sprint 01 exit criteria.

## Work items

### 1. Create `01_rotordynamic_simulation/07_sinha_fig10_replication.ipynb`

Outline of cells:

```python
# Cell 1 — imports, rotor load, sanity modal check.
import numpy as np, ross as rs
from pathlib import Path
from signal_utils import bispectrum, trispectrum, downsample_to, add_awgn
from plot_utils   import plot_bispectrum_surface, plot_trispectrum_balls
from constants    import (
    DT_SIM, T_LONG, FS_ACQ_FE, AA_CUTOFF, SNR_DB,
    DISK_NODE, CRACK_NODE, PROBE_NODE, UNB_MAG, UNB_PHASE, NUM_MODES,
)

rotor = rs.Rotor.load("sinha_rotor.toml")
f1_hz = float(rotor.run_modal(speed=0).wn[0] / (2*np.pi))
print(f"f1 = {f1_hz:.3f} Hz  (Sinha exp: 27.50 Hz)")
speed_rpm = 772.5
speed = rs.Q_(speed_rpm, "rpm").to("rad/s").m
```

```python
# Cell 2 — run Mayes crack at 772.5 RPM on the long grid.
res = rotor.run_crack(
    n=CRACK_NODE,
    depth_ratio=0.5,
    crack_model="Mayes",     # Sinha's (1-cosθ)Δk/2 breathing
    node=[DISK_NODE],
    unbalance_magnitude=[UNB_MAG.to("kg*m").m],
    unbalance_phase=[UNB_PHASE.to("rad").m],
    speed=speed, t=T_LONG,
    model_reduction={"num_modes": NUM_MODES},
)
```

```python
# Cell 3 — Sinha anti-alias + downsample + noise.
ndof   = rotor.number_dof
px, py = ndof*PROBE_NODE, ndof*PROBE_NODE + 1

x_hi = res.yout[:, px]
y_hi = res.yout[:, py]

rng = np.random.default_rng(2026)
x_1k = add_awgn(downsample_to(x_hi, 1/DT_SIM, FS_ACQ_FE, AA_CUTOFF), SNR_DB, rng=rng)
y_1k = add_awgn(downsample_to(y_hi, 1/DT_SIM, FS_ACQ_FE, AA_CUTOFF), SNR_DB, rng=rng)
t_1k = np.arange(len(x_1k)) / FS_ACQ_FE
```

```python
# Cell 4 — Fig. 9 replication: orbit plot.
import matplotlib.pyplot as plt

# Cut the first 2 s to kill transients.
mask = t_1k >= 2.0
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x_1k[mask]*1e3, y_1k[mask]*1e3, lw=0.6)
ax.set_xlabel("Horizontal displ. (mm)"); ax.set_ylabel("Vertical displ. (mm)")
ax.set_aspect("equal"); ax.set_title(f"Cracked-shaft orbit, FE @ {speed_rpm} RPM")
fig.savefig("results/figures/sprint_04/fig9_orbit.png", dpi=300, bbox_inches="tight")
```

```python
# Cell 5 — Fig. 10(a) replication: bispectrum surface.
B, b2, freqs = bispectrum(x_1k[mask], FS_ACQ_FE)
fig_b = plot_bispectrum_surface(B, freqs, fmax_hz=35.0, normalize=True)
fig_b.savefig("results/figures/sprint_04/fig10a_bispectrum.png", dpi=300, bbox_inches="tight")

# Peak location assertion (exit criterion).
f_1x = speed_rpm / 60                 # Hz — 12.875
i_1x = np.argmin(np.abs(freqs - f_1x))
i_2x = np.argmin(np.abs(freqs - 2*f_1x))

mag = np.abs(B).copy()
# Find the top-3 peaks in the non-redundant triangle:
triu = np.triu_indices_from(mag)
top = np.argsort(mag[triu])[-3:]
peak_pairs = list(zip(triu[0][top], triu[1][top]))

ok = all(
    any(abs(p[0] - ref_i) <= 1 and abs(p[1] - ref_j) <= 1 for p in peak_pairs)
    for ref_i, ref_j in [(i_1x, i_1x), (i_1x, i_2x), (i_2x, i_2x)]
)
assert ok, f"peaks {peak_pairs} do not cover {(i_1x,i_1x),(i_1x,i_2x),(i_2x,i_2x)}"
```

```python
# Cell 6 — Fig. 10(b) replication: trispectrum balls.
T_dict, freqs_T = trispectrum(x_1k[mask], FS_ACQ_FE, threshold=0.10)
fig_t = plot_trispectrum_balls(T_dict, freqs_T, fmax_hz=35.0, amp_min=0.10)
fig_t.savefig("results/figures/sprint_04/fig10b_trispectrum.png", dpi=300, bbox_inches="tight")

# Sanity: T111 should be present.
i_1x_T = np.argmin(np.abs(freqs_T - f_1x))
assert (i_1x_T, i_1x_T, i_1x_T) in T_dict
```

```python
# Cell 7 — side-by-side figure sheet.
# Open Sinha's Fig. 9 and Fig. 10 as image exports (if available) OR as a link,
# and place the reproductions next to them. Export a single PDF to
# reports/sinha_fig10_side_by_side.pdf.
```

### 2. Append a summary to this sprint file

Once the notebook runs clean, add a short "Execution Log" section to the bottom of this `.md`:

```
## Execution Log

- Ran on <date>, ROSS <version>, f1_current = <xx.xx> Hz.
- Peak locations: B11 at (<i_1x>, <i_1x>) bin = (<Hz>, <Hz>); B12 at (<>,<>); B22 at (<>,<>).
- Max peak-location error: ±<k> bins at Δf = <df> Hz.
- Trispectrum balls above 0.1: T111, T112, T122, T222 present (or flag any surprises).
- Figures: results/figures/sprint_04/*.png committed? yes / no.
- Deviations from Sinha Fig. 10: <describe>.
```

## Exit criteria

- [ ] Notebook `07_sinha_fig10_replication.ipynb` runs end-to-end without raising.
- [ ] Cell 5 assertion passes: the three bispectrum peaks expected at (f1, f1), (f1, 2f1), (2f1, 2f1) are found in the top-3 of the surface within ±1 bin at Δf = 1.25 Hz.
- [ ] Cell 6 assertion passes: T111 is in the trispectrum dict above the 0.10 threshold.
- [ ] Orbit plot (Cell 4) shows the expected loop-containing-small-loop topology at 772.5 RPM ≈ ½ f1.
- [ ] Side-by-side PDF with Sinha Figs. 9 and 10 exists at `reports/sinha_fig10_side_by_side.pdf`.
- [ ] Execution Log filled in at the bottom of this file.

## Implementation notes

- **Transient discard.** Sinha does not state his transient cut-off. 2 s at 1 kHz = 2000 samples ≫ settling time of a ζ=0.3 % mode at 27.5 Hz (τ ≈ 1/(ζωn) = 1/(0.003 · 2π · 27.5) ≈ 1.9 s). Use 2 s as the fixed cut-off; document it.
- **Normalization.** Sinha plots |B| normalized to 1 (`max(|B|) = 1`). Our `plot_bispectrum_surface(normalize=True)` matches this exactly.
- **Axes.** Sinha's Fig. 10(a) axes run 5–35 Hz. Restrict plotting to `fmax_hz = 35.0` to make side-by-side comparison immediate.
- **Speed exactness.** Sinha writes "half the first natural frequency i.e., 772.5 RPM" — but 27.50 Hz × 60 / 2 = 825 RPM, not 772.5. Sinha's own FE has f1 = 26.53 Hz, which gives 795.9 RPM. Neither reconciles exactly with 772.5; this is a paper inconsistency. Follow Sinha's stated 772.5 RPM and note the discrepancy in the Execution Log.
- **Do not over-fit amplitudes.** Exit criteria are on *topology* (peak locations) and *presence* (T111 above threshold). Amplitude matching is not required — Sinha's FE beam and ROSS's beam have different higher modes, so absolute amplitudes will diverge.

## Dependencies / hand-offs

- Sprint 05 and 06 reuse the same `downsample_to → add_awgn → bispectrum → plot_bispectrum_surface` chain with their own speeds.
- Sprint 07 reuses the side-by-side PDF layout established here.

## References

- Sinha (2007), §5 "Finite Element Simulation"; Figs. 9, 10. `99_references/`.
- Kim & Powers (1979) — normalization; already cited in Sprint 01.
- Cristofer's prior art: `01_rotordynamic_simulation/03_sinha_crack_model_comparison.ipynb` §"Stiffness Variation Over One Revolution" shows that Mayes' `(1 − cos θ) / 2` stiffness profile is implemented correctly in ROSS and matches Sinha's formula. Reuse its sanity-plot logic if useful.
