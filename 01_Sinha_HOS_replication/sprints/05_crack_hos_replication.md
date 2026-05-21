# Sprint 05 — Reproduce Sinha's experimental crack HOS at 650 / 750 RPM

> **Effort:** 1 week.
> **Blocks:** Sprint 07.
> **Unblocked by:** Sprints 00, 01, 02, 03 (Sprint 04 helpful but not strictly required).
> **Artefacts produced:** `01_rotordynamic_simulation/08_crack_hos_650_750.ipynb`, PNGs in `01_rotordynamic_simulation/results/figures/sprint_05/`, `reports/sinha_crack_side_by_side.pdf`, an Execution Log appended to this file.

## Why this sprint exists

Sinha's primary diagnostic argument lives in Figs. 2, 3, 5, and 7 — four figures that show the **experimental** crack signature at 650 and 750 RPM has a specific speed-dependence:

- At 650 RPM the bi-spectrum has a strong B11 and an emerging B22 (the shaft is approaching ½ f₁ resonance of the cracked mode at 26.25 Hz).
- At 750 RPM B22 is prominent, and the tri-spectrum gains a T222 ball that was below threshold at 650 RPM.
- Simultaneously the orbit topology changes from a double loop to a "loop containing a small loop" (Sinha Fig. 3).

The claim the thesis needs to back is: **ROSS + Sinha-matched HOS can reproduce this speed-dependent behaviour numerically.** That is the core evidence for the paper abstract.

## Prerequisites

- Sprints 00–03 complete (calibrated, damped rotor).
- `results/campaign.h5` populated with `crack @ 650 rpm`, `crack @ 750 rpm`, `healthy @ 650 rpm`, `healthy @ 750 rpm`. If missing, run `python run_campaign.py --conditions crack healthy --speeds 650 750`.
- Sprint 04 recommended — it proves the HOS pipeline reproduces *Sinha's own FE* at 772.5 RPM. If Sprint 04 failed, fix it before Sprint 05.

## Work items

### 1. `01_rotordynamic_simulation/08_crack_hos_650_750.ipynb`

Outline:

```python
# Cell 1 — load everything from HDF5 (no re-simulation).
import numpy as np, h5py
from pathlib import Path
from signal_utils import bispectrum, trispectrum, amplitude_spectrum
from plot_utils   import plot_bispectrum_surface, plot_trispectrum_balls
import matplotlib.pyplot as plt

h5 = h5py.File(Path(__file__).parent / "results" / "campaign.h5", "r")
# (In a notebook: h5 = h5py.File("results/campaign.h5", "r"))

def pick(cond, rpm):
    for name, g in h5.items():
        if g.attrs["condition"] == cond and int(g.attrs["speed_rpm"]) == rpm:
            return g
    raise KeyError(f"{cond} @ {rpm} rpm not in campaign.h5")

g_c650 = pick("crack", 650);  g_c750 = pick("crack", 750)
g_h650 = pick("healthy",650); g_h750 = pick("healthy",750)
fs = float(g_c650.attrs["fs_acq"])
```

```python
# Cell 2 — Fig. 2 replication: amplitude spectra at 650 and 750 RPM.
fig, axes = plt.subplots(2, 1, figsize=(7, 8), sharex=True)
for ax, g, rpm in zip(axes, (g_c650, g_c750), (650, 750)):
    x = g["y_probe_noisy"][:]                 # vertical probe — matches Sinha
    f, A = amplitude_spectrum(x, fs)
    ax.semilogy(f, A*1e3)
    ax.set_xlim(0, 200); ax.set_ylim(1e-5, 1e0)
    ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("Vertical displ. (mm)")
    ax.set_title(f"Cracked shaft, {rpm} RPM")
    for n, lbl in [(1, "1×"), (2, "2×"), (3, "3×"), (4, "4×"), (5, "5×")]:
        ax.axvline(n*rpm/60, ls="--", lw=0.6, color="gray")
fig.savefig("results/figures/sprint_05/fig2_amplitude_spectra.png", dpi=300, bbox_inches="tight")
```

```python
# Cell 3 — Fig. 3 replication: orbits at 650 and 750 RPM.
def orbit(g, ax, title):
    # Discard first 2 s as transient
    t = np.arange(len(g["x_probe_noisy"])) / fs
    mask = t >= 2.0
    ax.plot(g["x_probe_noisy"][mask]*1e3, g["y_probe_noisy"][mask]*1e3, lw=0.5)
    ax.set_aspect("equal")
    ax.set_xlabel("Horizontal displ. (mm)")
    ax.set_ylabel("Vertical displ. (mm)")
    ax.set_title(title)

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
orbit(g_c650, axes[0], "650 RPM")
orbit(g_c750, axes[1], "750 RPM")
fig.savefig("results/figures/sprint_05/fig3_orbits.png", dpi=300, bbox_inches="tight")
```

```python
# Cell 4 — Fig. 5 replication: bispectrum surfaces at 650 and 750 RPM.
def run_hos(g):
    x = g["y_probe_noisy"][:]
    t = np.arange(len(x)) / fs
    x = x[t >= 2.0]                           # kill transients
    B, b2, freqs = bispectrum(x, fs)
    return B, b2, freqs

B650, b650, f_ax = run_hos(g_c650)
B750, b750, _    = run_hos(g_c750)

fig_a = plot_bispectrum_surface(B650, f_ax, fmax_hz=50.0, normalize=True)
fig_a.suptitle("Bi-spectrum — Crack @ 650 RPM (Sinha Fig. 5a target)")
fig_a.savefig("results/figures/sprint_05/fig5a_bispectrum_650.png", dpi=300, bbox_inches="tight")

fig_b = plot_bispectrum_surface(B750, f_ax, fmax_hz=50.0, normalize=True)
fig_b.suptitle("Bi-spectrum — Crack @ 750 RPM (Sinha Fig. 5b target)")
fig_b.savefig("results/figures/sprint_05/fig5b_bispectrum_750.png", dpi=300, bbox_inches="tight")
```

```python
# Cell 5 — scalar indicator extraction for the exit criteria.
def pick_peak(B, freqs, f_row_hz, f_col_hz):
    i = np.argmin(np.abs(freqs - f_row_hz))
    j = np.argmin(np.abs(freqs - f_col_hz))
    return abs(B[i, j])

def indicators(B, freqs, rpm):
    f1 = rpm / 60.0
    B11 = pick_peak(B, freqs, f1,   f1)
    B22 = pick_peak(B, freqs, 2*f1, 2*f1)
    B12 = pick_peak(B, freqs, f1,   2*f1)
    B13 = pick_peak(B, freqs, f1,   3*f1)
    return dict(B11=B11, B22=B22, B12=B12, B13=B13,
                B22_over_B11=B22/B11, B12_over_B11=B12/B11, B13_over_B11=B13/B11)

ind_650 = indicators(B650, f_ax, 650)
ind_750 = indicators(B750, f_ax, 750)

print("650 RPM:", ind_650)
print("750 RPM:", ind_750)

# Exit criterion 1 — speed-dependent B22:
ratio_650 = ind_650["B22_over_B11"]
ratio_750 = ind_750["B22_over_B11"]
assert ratio_750 >= 2.0 * ratio_650, (
    f"B22 speed-dependence FAIL: ratio(750)={ratio_750:.3f} < 2·ratio(650)={2*ratio_650:.3f}"
)
```

```python
# Cell 6 — Fig. 7 replication: tri-spectrum balls.
T650, _ = trispectrum(g_c650["y_probe_noisy"][:], fs, threshold=0.10)
T750, _ = trispectrum(g_c750["y_probe_noisy"][:], fs, threshold=0.10)

fig_a = plot_trispectrum_balls(T650, f_ax, fmax_hz=35.0, amp_min=0.10)
fig_a.suptitle("Tri-spectrum — Crack @ 650 RPM")
fig_a.savefig("results/figures/sprint_05/fig7a_trispectrum_650.png", dpi=300, bbox_inches="tight")

fig_b = plot_trispectrum_balls(T750, f_ax, fmax_hz=35.0, amp_min=0.10)
fig_b.suptitle("Tri-spectrum — Crack @ 750 RPM")
fig_b.savefig("results/figures/sprint_05/fig7b_trispectrum_750.png", dpi=300, bbox_inches="tight")

# Exit criterion 2 — T222 appears at 750 and is absent at 650.
def has(T_dict, freqs, f_hz):
    i = np.argmin(np.abs(freqs - f_hz))
    return (i, i, i) in T_dict

f1_650, f1_750 = 650/60, 750/60
assert not has(T650, f_ax, 2*f1_650), "T222(650) should be below 0.1 threshold but isn't"
assert     has(T750, f_ax, 2*f1_750), "T222(750) should be above 0.1 threshold but isn't"
```

```python
# Cell 7 — orbit-topology check (Sinha's "loop containing small loop" at 750 RPM).
def zero_crossings_per_rev(g, rpm, fs):
    t = np.arange(len(g["x_probe_noisy"])) / fs
    mask = t >= 2.0
    y = g["y_probe_noisy"][mask]
    # Take a single revolution's worth of data
    one_rev = int(fs * 60.0 / rpm)
    seg = y[:one_rev]
    return int(np.sum(np.diff(np.sign(seg)) != 0))

cross_650 = zero_crossings_per_rev(g_c650, 650, fs)
cross_750 = zero_crossings_per_rev(g_c750, 750, fs)
print(f"Zero-crossings / revolution: 650 → {cross_650}, 750 → {cross_750}")
# Exit criterion 3 — loop-containing-small-loop at 750 RPM:
assert cross_750 >= 4, f"orbit topology at 750 RPM too simple: {cross_750} crossings"
```

```python
# Cell 8 — assemble side-by-side PDF.
# Arrange the Sprint 05 reproductions alongside paper scans (or render Sinha
# references from the PDF using poppler/ghostscript if available). Write to
# reports/sinha_crack_side_by_side.pdf.
```

### 2. Update the sprint file with the Execution Log

Once the notebook runs clean, append:

```
## Execution Log

- Ran on <date>, ROSS <version>, fs_acq = <> Hz, num_modes = <>.
- Scalar indicators
  | Speed | B11 | B22 | B12 | B13 | B22/B11 | B12/B11 | B13/B11 |
  | 650   | ... | ... | ... | ... | ...     | ...     | ...     |
  | 750   | ... | ... | ... | ... | ...     | ...     | ...     |
- Speed-dependence ratio: B22/B11(750) / B22/B11(650) = <>× (target ≥ 2)
- T222 presence: 650 → absent / 750 → present  (target: absent at 650, present at 750)
- Orbit zero-crossings per revolution: 650 → <>, 750 → <>  (target ≥ 4 at 750)
- Exit criteria satisfied: <N>/5
```

## Exit criteria

1. [ ] `|B22(750)| / |B11(750)| ≥ 2 · |B22(650)| / |B11(650)|` — speed-dependent super-harmonic (Cell 5).
2. [ ] `|T222(750)| ≥ 0.10` above normalized threshold; `|T222(650)| < 0.10` (Cell 6).
3. [ ] 750 RPM orbit has ≥ 4 y=0 crossings per revolution, indicating the loop-containing-small-loop topology Sinha describes (Cell 7).
4. [ ] Amplitude spectrum at 750 RPM shows visible harmonics out to at least 5× above the −40 dB noise floor (Cell 2 — visually, or with a programmatic peak-count assertion).
5. [ ] `reports/sinha_crack_side_by_side.pdf` renders four paired panels (Sinha Figs. 2, 3, 5, 7 alongside Cristofer's reproductions).

## Implementation notes

- **Direction matters.** Sinha measures **vertical** displacement (`y_probe_noisy` in `campaign.h5`). Use `y_probe_noisy` for the amplitude spectra and bispectrum. The orbit uses both (x, y).
- **Transient cut-off.** Fixed 2 s — matches Sprint 04. Document in Methods alongside the ζ = 0.3 % damping choice.
- **Normalization.** `plot_bispectrum_surface(normalize=True)` divides by `max(|B|)`, so the surface peaks at 1.0. Sinha's Figs. 5 and 6 use the same convention.
- **Scalloping guard.** B11 sits at a non-integer bin for 650 RPM (10.833 Hz) and 750 RPM (12.5 Hz). With Δf = 1.25 Hz, bin 9 = 11.25 Hz and bin 10 = 12.5 Hz. At 750 RPM B11 lands *exactly* on bin 10. At 650 RPM the Hann window and parabolic-interpolated `harmonic_amplitude` (Sprint 01) cancel the scallop. Verify by running `amplitude_spectrum` on a pure 10.833 Hz sinusoid and confirming amplitude error < 1 %.
- **If Exit Criterion 1 fails.** The most likely cause is under-damping or under-truncation — see Sprint 03. Secondary cause: `UNB_MAG` magnitude. Sinha writes "small unbalance" without specifics; our `2e-4 kg·m` is a guess. Try halving it; the *ratios* should be insensitive, but if they are not, document the sensitivity in Sprint 07.
- **If Exit Criterion 2 fails.** Verify that `trispectrum(..., threshold=0.10)` normalization divides by `max(|T|)` (not by `max(|T|)` per segment). The Sprint 01 synthetic test must re-pass on the current build before any claim is made.

## Dependencies / hand-offs

- Sprint 06 reuses `run_hos` and `indicators` verbatim, just for a different condition and speeds.
- Sprint 07 consumes the PNGs from `results/figures/sprint_05/` and the Execution Log table.

## References

- Sinha (2007) §3.1 "Fault 1: Cracked Shaft" (rig description, speeds), Figs. 2, 3, 5, 7.
- Sinha §4 "Discussion" paragraphs on B22 and T222 (the two scalar targets).
- Campaign driver and HDF5 contract: Sprint 02.
- Crack-model ground truth: `01_rotordynamic_simulation/03_sinha_crack_model_comparison.ipynb` (proves Mayes in ROSS matches Sinha's `(1−cosθ)Δk/2`).
