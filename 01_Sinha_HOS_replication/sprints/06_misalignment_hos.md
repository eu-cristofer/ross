# Sprint 06 — Misalignment HOS extension (novel contribution vs Sinha)

> **Effort:** 1 week.
> **Blocks:** Sprint 07.
> **Unblocked by:** Sprints 00, 01, 02, 03, 05 (Sprint 05's `indicators()` helper is reused verbatim).
> **Artefacts produced:** `01_rotordynamic_simulation/09_misalignment_hos_750_900.ipynb`, PNGs in `01_rotordynamic_simulation/results/figures/sprint_06/`, `reports/sinha_misalignment_side_by_side.pdf`, an Execution Log appended to this file.

## Why this sprint matters for the thesis

**Sinha (2007) could not FE-simulate misalignment.** Section 5: "Similar simulation for the misaligned shaft could not be done, as the force function due to the shaft misalignment is not well stood." His Figs. 4, 6, and 8 are purely experimental.

ROSS's `run_misalignment` (flex coupling, parallel, from Xia et al. 2019) **can** produce a misalignment time response numerically. Reproducing Sinha's experimental misalignment HOS features with that solver is therefore a step beyond what the paper achieved — the single clearest novelty claim the thesis has against Sinha (2007). This sprint delivers that evidence.

The features to match (from Sinha §4 "Discussion"):

- Bi-spectrum has **B11, B12 = B21, and B13 = B31** present; **B22 is absent**.
- Pattern is **speed-independent** — the same topology appears at 750 and 900 RPM.
- Tri-spectrum has **only T111**, at both speeds.

## Prerequisites

- Sprints 00–03, 05 complete.
- `results/campaign.h5` contains `misalignment @ 750 rpm`, `misalignment @ 900 rpm`, `healthy @ 750 rpm`, `healthy @ 900 rpm`. If missing, run `python run_campaign.py --conditions misalignment healthy --speeds 750 900`.

## Work items

### 1. `01_rotordynamic_simulation/09_misalignment_hos_750_900.ipynb`

Reuse the Sprint 05 structure. The only material differences are the condition label (`"misalignment"`) and the exit criteria (topology, not amplitude).

```python
# Cell 1 — load from HDF5, same pick() helper as Sprint 05.
import numpy as np, h5py
from signal_utils import bispectrum, trispectrum, amplitude_spectrum
from plot_utils   import plot_bispectrum_surface, plot_trispectrum_balls
import matplotlib.pyplot as plt

h5 = h5py.File("results/campaign.h5", "r")

def pick(cond, rpm):
    for name, g in h5.items():
        if g.attrs["condition"] == cond and int(g.attrs["speed_rpm"]) == rpm:
            return g
    raise KeyError(f"{cond} @ {rpm} rpm not in campaign.h5")

g_m750 = pick("misalignment", 750)
g_m900 = pick("misalignment", 900)
g_h750 = pick("healthy",      750)
g_h900 = pick("healthy",      900)
fs = float(g_m750.attrs["fs_acq"])
```

```python
# Cell 2 — Fig. 4 replication: amplitude spectra.
fig, axes = plt.subplots(2, 1, figsize=(7, 8), sharex=True)
for ax, g, rpm in zip(axes, (g_m750, g_m900), (750, 900)):
    f, A = amplitude_spectrum(g["y_probe_noisy"][:], fs)
    ax.semilogy(f, A*1e3)
    ax.set_xlim(0, 200); ax.set_ylim(1e-6, 1e0)
    ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("Vertical displ. (mm)")
    ax.set_title(f"Misaligned shaft, {rpm} RPM")
    for n in (1, 2, 3, 4, 5, 6):
        ax.axvline(n*rpm/60, ls="--", lw=0.6, color="gray")
fig.savefig("results/figures/sprint_06/fig4_amplitude_spectra.png", dpi=300, bbox_inches="tight")
```

```python
# Cell 3 — Fig. 6 replication: bispectrum surfaces at 750 and 900.
def run_hos(g):
    x = g["y_probe_noisy"][:]
    t = np.arange(len(x)) / fs
    x = x[t >= 2.0]
    B, b2, freqs = bispectrum(x, fs)
    return B, b2, freqs

B750, _, f_ax = run_hos(g_m750)
B900, _, _    = run_hos(g_m900)

for B, rpm, tag in [(B750, 750, "a"), (B900, 900, "b")]:
    fig = plot_bispectrum_surface(B, f_ax, fmax_hz=50.0, normalize=True)
    fig.suptitle(f"Bi-spectrum — Misalignment @ {rpm} RPM (Sinha Fig. 6{tag} target)")
    fig.savefig(f"results/figures/sprint_06/fig6{tag}_bispectrum_{rpm}.png",
                dpi=300, bbox_inches="tight")
```

```python
# Cell 4 — scalar indicators and topology signature.
# Reuse indicators() from Sprint 05 (copy or import from a shared helper).
from signal_utils import pick_peak  # if Sprint 05 moved the helper there, else copy-paste.

def indicators(B, freqs, rpm):
    f1 = rpm / 60.0
    B11 = pick_peak(B, freqs, f1,   f1)
    B22 = pick_peak(B, freqs, 2*f1, 2*f1)
    B12 = pick_peak(B, freqs, f1,   2*f1)
    B13 = pick_peak(B, freqs, f1,   3*f1)
    return dict(
        B11=B11, B22=B22, B12=B12, B13=B13,
        B22_over_B11=B22/B11, B12_over_B11=B12/B11, B13_over_B11=B13/B11,
    )

ind_750 = indicators(B750, f_ax, 750)
ind_900 = indicators(B900, f_ax, 900)

print("750 RPM:", ind_750)
print("900 RPM:", ind_900)

# ---- Exit Criterion 1: B22 absent at both speeds ----
assert ind_750["B22_over_B11"] <= 0.10, f"B22 unexpectedly present at 750: {ind_750['B22_over_B11']:.3f}"
assert ind_900["B22_over_B11"] <= 0.10, f"B22 unexpectedly present at 900: {ind_900['B22_over_B11']:.3f}"

# ---- Exit Criterion 2: B13 (=B31) present at both speeds ----
assert ind_750["B13_over_B11"] >= 0.15, f"B13 missing at 750: {ind_750['B13_over_B11']:.3f}"
assert ind_900["B13_over_B11"] >= 0.15, f"B13 missing at 900: {ind_900['B13_over_B11']:.3f}"
```

```python
# Cell 5 — topology match between 750 and 900.
def topology(B, freqs, rpm, threshold=0.15):
    """Return the set {(l, m) : |B(l·f1, m·f1)| / max|B| >= threshold}."""
    f1 = rpm / 60.0
    peaks = {}
    for l in range(1, 5):
        for m in range(l, 5):
            p = pick_peak(B, freqs, l*f1, m*f1)
            peaks[(l, m)] = p
    mx = max(peaks.values())
    return {k for k, v in peaks.items() if v / mx >= threshold}

topo_750 = topology(B750, f_ax, 750)
topo_900 = topology(B900, f_ax, 900)
print("Topology 750 RPM:", topo_750)
print("Topology 900 RPM:", topo_900)

# ---- Exit Criterion 3: same topology, containing (1,1), (1,2), (1,3); NOT (2,2) ----
assert topo_750 == topo_900, (
    f"topologies differ: 750={topo_750}, 900={topo_900}  (speed-dependence violates Sinha)"
)
assert {(1, 1), (1, 2), (1, 3)} <= topo_750
assert (2, 2) not in topo_750
```

```python
# Cell 6 — Fig. 8 replication: tri-spectrum balls.
T750, _ = trispectrum(g_m750["y_probe_noisy"][:], fs, threshold=0.10)
T900, _ = trispectrum(g_m900["y_probe_noisy"][:], fs, threshold=0.10)

for Td, rpm, tag in [(T750, 750, "a"), (T900, 900, "b")]:
    fig = plot_trispectrum_balls(Td, f_ax, fmax_hz=35.0, amp_min=0.10)
    fig.suptitle(f"Tri-spectrum — Misalignment @ {rpm} RPM (Sinha Fig. 8{tag} target)")
    fig.savefig(f"results/figures/sprint_06/fig8{tag}_trispectrum_{rpm}.png",
                dpi=300, bbox_inches="tight")

# ---- Exit Criterion 4: only T111 present at either speed. ----
def only_t111(Td, freqs, rpm):
    f1 = rpm / 60.0
    i1 = np.argmin(np.abs(freqs - f1))
    # Acceptable: dict contains (i1, i1, i1) and possibly its permutations —
    # no ball at (i2, i2, i2) or (i1, i1, i2) with |T| above 0.10.
    for (a, b, c), v in Td.items():
        if (a, b, c) == (i1, i1, i1):
            continue
        if v >= 0.10 and (a, b, c) != (i1, i1, i1):
            return False, (a, b, c, v)
    return True, None

ok750, diag750 = only_t111(T750, f_ax, 750)
ok900, diag900 = only_t111(T900, f_ax, 900)
assert ok750, f"extra tri-spectrum component at 750 RPM: {diag750}"
assert ok900, f"extra tri-spectrum component at 900 RPM: {diag900}"
```

```python
# Cell 7 — side-by-side PDF, Sinha Fig. 4/6/8 vs Cristofer reproduction.
```

### 2. Append the Execution Log to this file

```
## Execution Log

- Ran on <date>, ROSS <version>, fs_acq = <> Hz.
- Misalignment offsets: δx = 1.0 mm, δy = 0.5 mm; flex coupling (radial_stiffness=4e4, bending_stiffness=3.8e4).
- Scalar indicators
  | Speed | B11 | B22 | B12 | B13 | B22/B11 | B12/B11 | B13/B11 |
  | 750   | ... | ... | ... | ... | ...     | ...     | ...     |
  | 900   | ... | ... | ... | ... | ...     | ...     | ...     |
- Topology 750 RPM: {(1,1), (1,2), (1,3), ...}
- Topology 900 RPM: {(1,1), (1,2), (1,3), ...}
- Topology match between 750 and 900: yes / no
- B22 absence (B22/B11 ≤ 0.10): 750 <>, 900 <>
- B13 presence (B13/B11 ≥ 0.15): 750 <>, 900 <>
- Tri-spectrum — only T111 above 0.10: 750 <>, 900 <>
- Exit criteria satisfied: <N>/4
- Notes: <e.g. "B21 = B12 confirmed numerically to within 2%", "B31 = B13 confirmed">
```

## Exit criteria

1. [ ] `|B22(750)| / |B11(750)| ≤ 0.10` **and** `|B22(900)| / |B11(900)| ≤ 0.10` — B22 is absent (Sinha §4 claim).
2. [ ] `|B13(750)| / |B11(750)| ≥ 0.15` **and** same at 900 — the off-diagonal B13 = B31 peak is present (Sinha Fig. 6).
3. [ ] Topology set `{(l, m) : |B(l,m)| ≥ 0.15 · max|B|}` is **identical at 750 and 900 RPM** (topology-level speed-independence, the right weakening of Sinha's "speed-independent" claim).
4. [ ] Only **T111** rises above the 0.10 normalized threshold in the tri-spectrum at either speed (Sinha Fig. 8).
5. [ ] `reports/sinha_misalignment_side_by_side.pdf` renders paired panels for Sinha Figs. 4, 6, 8 vs Cristofer's reproductions.

## Implementation notes

- **Coupling parameters.** `radial_stiffness = 4e4 N/m` and `bending_stiffness = 3.8e4 N·m/rad` are inherited from `04_sinha_fault_analysis.ipynb`. Sinha does not publish coupling stiffnesses; these are ROSS defaults. If Exit Criterion 2 (B13 presence) fails, try `radial_stiffness ∈ {1e4, 4e4, 1e5}` — the B13/B11 ratio is known from ROSS docs examples to be sensitive to coupling stiffness.
- **B22 = 0 is a physics claim.** Sinha's argument (§4) is that misalignment produces 2X via *geometric forcing*, not parametric stiffness variation, and the phase of the 2X component is locked to 1X in a way that does not create the quadratic phase coupling that B22 measures. If ROSS's flex-coupling model produces B22 > 0.10, it is because the coupling model introduces a spurious coupling nonlinearity — document this as a model-form uncertainty; it is itself a reportable result.
- **Topology threshold.** 0.15 is one-sigma above the bi-spectrum noise floor observed on healthy simulations (verify from `healthy @ 750 rpm` in `campaign.h5`). If the healthy noise floor sits higher than 0.15, raise the threshold; don't weaken the topology criterion.
- **Xia et al. 2019 reference.** ROSS's flex-coupling misalignment force follows Xia et al. The 6-bolt geometry injects 1X, 2X (small), and 3X components — B13 = B31 should emerge naturally from the 1X × 3X interaction.
- **If every exit criterion passes.** Write a single-paragraph Methods contribution note in the Execution Log: "ROSS's `run_misalignment` (flex-coupling, Xia et al. 2019) reproduces Sinha's (2007) experimental Fig. 6 and Fig. 8 topology with coupling stiffnesses within an order of magnitude of literature values — closing the FE-simulation gap Sinha acknowledged in §5." This is the one line that is worth drafting immediately because it goes into the thesis abstract.

## Dependencies / hand-offs

- Sprint 07 reads the Execution Log table and the PDF directly.
- If Exit Criteria 1 or 4 fail, flag as "partial" rather than "fail" in Sprint 07's validation matrix — a failure here has scientific content (it means ROSS's flex-coupling model behaves differently from the Sinha rig) and should be reported, not hidden.

## References

- Sinha (2007) §3.2 "Fault 2: Misaligned Shaft" (rig: 1 mm vertical, 0.5 mm horizontal bearing-pedestal misalignment); §4 "Discussion" on B13/B31 and T111; Figs. 4, 6, 8.
- Sinha §5 closing paragraph: "Similar simulation for the misaligned shaft could not be done" — the gap this sprint addresses.
- Xia, Y., Pang, J., Yang, L., Zhao, Q., & Yang, X. (2019). Study on vibration response and orbits of misaligned rigid rotors connected by hexangular flexible coupling. *Applied Acoustics* — the model behind ROSS's flex coupling.
- Existing misalignment code to inherit from: `01_rotordynamic_simulation/04_sinha_fault_analysis.ipynb` `simulate_misalignment()` helper (already computes `run_misalignment` with the correct parameters).
