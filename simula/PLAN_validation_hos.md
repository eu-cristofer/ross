# FEM Model Validation and HOS Pattern Comparison

> **Author:** Cristofer Antoni Souza Costa
> **Date:** February 2026
> **Status:** In progress

---

## Overview

Build a validation workflow that:

**(a)** Replicates Sinou's (2009) experimental cracked-rotor rig in ROSS and validates
natural frequencies and harmonic amplitudes against published data.

**(b)** Implements a bispectrum/bicoherence pipeline to compare HOS patterns against
Sinha's (2014) published bispectrum plots.

---

## Context

ROSS already provides all necessary building blocks:

- Crack models: Mayes, Gasch, Flex Open, Flex Breathing in `ross/faults/crack.py`
- `run_modal()`, `run_crack()`, `run_unbalance_response()`, `run_freq_response()` in `ross/rotor_assembly.py`
- FFT-based frequency analysis via `plot_dfft()` / `_dfft()` in `ross/results.py`
- No HOS (bispectrum/bicoherence) module exists yet -- this must be built

Two primary published datasets serve as validation targets:

- **Sinou (2009)**, *ASME J. Vibration and Acoustics*, 131(4), 041008: Experimental rig
  with shaft L=480mm, d=10mm, disk at 382mm (d=75mm, t=35mm), crack at 243mm.
  Provides 1X and 2X amplitude tables for crack depths mu=0 to 1 at critical and
  1/2 subcritical speeds.
- **Sinha (2014)**, *Proc IMechE Part O: J. Risk and Reliability*, 228(4), 419-428:
  Experimental bispectrum and trispectrum plots for crack and misalignment faults
  on a test rig.

---

## Part A: FEM Model Validation Against Published Frequency Responses

### A1. Replicate Sinou's Experimental Rig in ROSS

Build a ROSS rotor model matching Sinou's (2009) test rig specifications:

- **Shaft**: L=480mm, d=10mm, steel (E~210 GPa, rho~7800 kg/m3). Discretize into
  ~24 equal elements (20mm each) to place the crack and disk at exact node positions.
- **Disk**: at node closest to 382mm from left end. Geometry: d_outer=75mm,
  thickness=35mm, d_inner=10mm (shaft bore).
- **Bearings**: Simple supports (ball bearings). Use high stiffness kxx=kyy ~ 1e7 N/m
  with light damping cxx=cyy ~ 50 N.s/m to approximate simply-supported conditions.
- **Crack**: at element closest to 243mm, using the Mayes breathing model.

### A2. Validate Natural Frequencies

- Run `rotor.run_modal(speed=0)` and extract first critical speed.
- **Target**: Sinou reports first critical speed at ~2600-2800 RPM (~272-293 rad/s).
  The model should match within ~5%.
- Tune bearing stiffness if needed to match the experimental critical speed.
- Plot a Campbell diagram using `rotor.run_campbell()`.

### A3. Validate Harmonic Responses for Cracked Shaft

For each crack depth ratio mu in {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}:

1. Run `rotor.run_crack(...)` at speeds near the 1/2 subcritical and 1st critical speeds.
2. Extract 1X and 2X amplitudes from time response using `_dfft()`.
3. Build comparison tables against Sinou's Tables 1-4.

**Quantitative validation metrics:**

- Relative error in 1X amplitudes at critical speed
- Relative error in 2X amplitudes at 1/2 subcritical speed
- Trend agreement: 2X amplitude should increase monotonically with crack depth

### A4. Validation Deliverables

Notebook `validation_sinou.ipynb` containing:

- Figure 1: ROSS rotor schematic
- Figure 2: Campbell diagram with annotated critical speed
- Figure 3: Comparison table -- computed vs. experimental natural frequencies
- Figure 4: 1X amplitude vs. crack depth
- Figure 5: 2X amplitude vs. crack depth
- Figure 6: Frequency spectra at 1/2 subcritical speed for different crack depths

---

## Part B: HOS Pattern Comparison with Sinha's Bispectrum Plots

### B1. Implement Bispectrum Estimation Module

Create `hos_analysis.py` with:

- `estimate_bispectrum(signal, fs, nfft, noverlap)` -- direct DFT-based, segment averaged
- `estimate_bicoherence(signal, fs, nfft, noverlap)` -- normalized bispectrum
- `bispectral_peak_ratio(B, freqs, f_rot)` -- BPR = |B(1X,1X)| / |B(1X,2X)|
- `bicoherence_sum(bic2, freqs, f_min, f_max)` -- sum in frequency band
- `bispectral_entropy(B, freqs)` -- Shannon entropy of normalized bispectrum

### B2. Validate Bispectrum Code

Test against synthetic signals:

1. Linearly coupled harmonics (no phase coupling) -> no bispectral peaks
2. Quadratically coupled signal -> peak at (f1, f2)
3. Gaussian noise -> bicoherence near zero

### B3. Generate HOS Patterns

Using ROSS simulations:

1. **Healthy rotor**: expect near-zero bicoherence
2. **Cracked shaft** (mu=0.2, 0.3, 0.4): expect peaks at (1X,1X) and (1X,2X)
3. **Misaligned shaft**: expect different peak pattern

### B4. Qualitative Comparison with Sinha (2014)

- Side-by-side 2D contour plots
- Check location of bispectral peaks matches qualitatively
- Check relative magnitude pattern consistency
- Document differences (rig geometry, operating speed, noise)

---

## File Organization

```
simula/
  PLAN_validation_hos.md          # This plan
  prototype.ipynb                 # Step-by-step learning prototype
  hos_analysis.py                 # HOS module (to be created)
  references/
    sinou2009.pdf                 # Sinou experimental data
  validation_sinou.ipynb          # Part A notebook (to be created)
  hos_comparison.ipynb            # Part B notebook (to be created)
```

---

## References

1. Sinou, J.-J. (2009). Experimental Study on the Nonlinear Vibrations and nX
   Amplitudes of a Rotor With a Transverse Crack. *ASME J. Vibration and Acoustics*,
   131(4), 041008. https://doi.org/10.1115/1.3086928

2. Sinha, J.K. (2014). Combined bispectrum and trispectrum for faults diagnosis
   in rotating machines. *Proc IMechE Part O: J. Risk and Reliability*, 228(4),
   419-428. https://doi.org/10.1177/1748006X14524547

3. Guo, C.-Z., Yan, J.-H., & Bergman, L.A. (2017). Experimental Dynamic Analysis
   of a Breathing Cracked Rotor. *Chinese Journal of Mechanical Engineering*, 30,
   1177-1183. https://doi.org/10.1007/s10033-017-0180-7

4. Sinou, J.-J. & Lees, A.W. (2007). A Non-Linear Study of a Cracked Rotor.
   *European Journal of Mechanics A/Solids*, 26(1), 152-170.

5. Timbo, R. et al. (2020). ROSS - Rotordynamic Open Source Software.
   *Journal of Open Source Software*. https://ross.readthedocs.io
