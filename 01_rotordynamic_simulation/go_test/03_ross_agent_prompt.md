# Agent Prompt: Go/No-Go Simulation for HOS Fault Diagnosis

---

You are a senior mechanical engineering researcher and Python developer specializing in rotordynamics and signal processing.

### Context

I am working on a master's thesis investigating whether **Higher-Order Spectra (HOS)** -- specifically the bispectrum and bicoherence -- can distinguish between **shaft cracks** and **shaft misalignment** in rotating machines when applied to **numerically simulated** vibration data.

Before committing to a full parametric study (months of work), I need a **quick feasibility test** to answer one critical question:

> **Do the bispectrum patterns look visually different for a healthy rotor, a cracked rotor, and a misaligned rotor when simulated via finite element models?**

If YES --> the research proceeds (GO).
If NO --> the research question must be revised (NO-GO).

### Your Task

Create a **single, self-contained Python script** (file name: `go_no_go_simulation.py`) that performs the following steps. Place it in a folder called `02_go_no_go/` at the project root.

Also create a Jupyter notebook version (`go_no_go_simulation.ipynb`) with the same logic, split into clear cells with markdown explanations, for interactive exploration.

### Environment

The project uses a conda environment named `research` with:
- Python 3.12
- numpy, scipy, matplotlib, plotly
- The `ross` library must be installed via pip: `pip install ross-rotordynamics`

Before running any simulation, check that `ross` is importable. If not, print installation instructions and exit gracefully.

### Step 1: Build a Simple Rotor-Bearing System in ROSS

Build two models: One named sinha rotor as per its paper: Physical dimensions:
Shaft: OD: 10 mm L: 550 mm
Bush bearings Mounted in a rigid massive base plate L1 (bearing 1): 20 mm L2 (bearing 2):: 510 mm
Balance disk OD: 75 mm ID: 10 mm thickness: 25 mm L3 = L / 2
Fn1: 27.50 HZ (both horizontal and vertical directions)

and an other Laval/Jeffcott-like rotor model:

- **Shaft:** 1.0 m total length, 30 mm outer diameter, solid (no inner diameter), steel (E = 211 GPa, G = 81.2 GPa, rho = 7810 kg/m3)
- **Discretization:** 20 equal shaft elements (each 50 mm long)
- **Disc:** Located at the midspan (node 10), steel, 50 mm width, 30 mm inner diameter, 150 mm outer diameter
- **Bearings:** At node 0 (left) and node 20 (right), isotropic:
  - kxx = kyy = 1e6 N/m
  - cxx = cyy = 500 N.s/m
- **Unbalance:** 1e-4 kg.m at the disc node (phase = 0)

After building, print a summary of the rotor tipical dynamics analysis.

### Step 2: Define the Simulation Cases

Simulate 4 cases at a **fixed rotational speed of 1500 RPM** (25 Hz):

| Case | Label | Fault Description |
|---|---|---|
| 1 | `healthy` | No fault -- baseline unbalance response only |
| 2 | `crack_light` | Breathing crack at midspan, crack depth ratio a/D = 0.2 |
| 3 | `crack_severe` | Breathing crack at midspan, crack depth ratio a/D = 0.4 |
| 4 | `misalignment` | Parallel misalignment at the right bearing, offset = 0.5 mm |

**How to model the faults numerically:**

Since ROSS may not natively support time-varying stiffness or misalignment forcing, implement them as **external periodic forces** applied during time integration:

#### Crack Model (approximate via periodic forcing)
A breathing crack generates harmonic forces at 2X and 3X the rotational frequency due to the periodic stiffness variation. Approximate the crack effect by adding external forces at the crack node (node 10):

```python
# Breathing crack approximate forcing
# The crack opens/closes once per revolution, creating 2X and 3X harmonics
omega = 2 * np.pi * speed_hz  # rotational frequency in rad/s

def crack_force(t, a_D_ratio):
    """Approximate crack forcing as 2X and 3X harmonics.
    Amplitude scales with crack depth ratio squared (energy argument).
    """
    base_amplitude = 50.0  # N, base force scale (adjust if needed)
    amplitude = base_amplitude * (a_D_ratio ** 2)
    f_2x = amplitude * np.cos(2 * omega * t)
    f_3x = 0.3 * amplitude * np.cos(3 * omega * t + np.pi/4)
    return f_2x + f_3x
```

The key for HOS: the crack must introduce **phase-coupled** harmonics (the 2X component is phase-locked to 1X). This is what the bispectrum detects.

To make the coupling realistic for bispectrum detection, the crack force should include a **quadratic nonlinearity** term:

```python
def crack_force_nonlinear(t, a_D_ratio):
    """Crack forcing with quadratic nonlinearity for bispectrum detection."""
    base = 50.0 * (a_D_ratio ** 2)
    x1 = np.cos(omega * t)  # 1X component
    # Quadratic coupling: x1^2 produces 2X with phase coupling
    f_crack = base * (x1 ** 2) + 0.2 * base * (x1 ** 3)
    return f_crack
```

#### Misalignment Model (approximate via periodic forcing)
Misalignment generates strong 1X and 2X harmonics, but with **different phase relationships** than a crack:

```python
def misalignment_force(t, offset_mm):
    """Misalignment forcing: 1X and 2X with different phase structure than crack."""
    base_amplitude = 100.0 * (offset_mm / 0.5)  # N, scales with offset
    f_1x = base_amplitude * np.cos(omega * t + np.pi/6)
    f_2x = 0.8 * base_amplitude * np.cos(2 * omega * t + np.pi/3)
    f_3x = 0.15 * base_amplitude * np.cos(3 * omega * t + np.pi/2)
    return f_1x + f_2x + f_3x
```

The key difference for HOS: misalignment harmonics have **different phase relationships** than crack harmonics. The bispectrum phase (biphase) at frequency pairs like (f1, f1) should differ.

### Step 3: Run Time-Domain Simulations

For each case:
1. Use ROSS time integration (or scipy `solve_ivp` if ROSS time response is limited) to compute the shaft displacement at the disc node (node 10) over time.
2. **Simulation parameters:**
   - Duration: 4 seconds (100 revolutions at 25 Hz)
   - Sampling rate: 2048 Hz (gives good frequency resolution up to ~1000 Hz)
   - Discard the first 1 second as transient; use the last 3 seconds for analysis
3. Store the horizontal (x) displacement time series for each case.

If ROSS time integration is not straightforward, fall back to a simplified approach:
- Extract the system matrices (M, K, C, G) from the ROSS model
- Build the state-space representation
- Integrate using `scipy.integrate.solve_ivp` with `method='RK45'`
- Apply unbalance + fault forces as external forcing

### Step 4: Compute Power Spectral Density (PSD)

For each case, compute the PSD using `scipy.signal.welch`:
- NFFT = 1024
- Window: Hanning
- Overlap: 50%
- Normalize the PSD to highlight relative harmonic amplitudes

### Step 5: Compute the Bispectrum

Implement a bispectrum estimation function using the **direct (DFT) method** with segment averaging:

```python
def compute_bispectrum(signal, fs, nfft=512, overlap_ratio=0.5):
    """
    Estimate the bispectrum using the direct method with segment averaging.

    Parameters
    ----------
    signal : array_like
        1D time-domain signal (real-valued).
    fs : float
        Sampling frequency in Hz.
    nfft : int
        FFT length per segment.
    overlap_ratio : float
        Fractional overlap between segments (0 to 1).

    Returns
    -------
    bispectrum : 2D complex ndarray, shape (nfft//2+1, nfft//2+1)
        Estimated bispectrum B(f1, f2).
    bicoherence : 2D real ndarray, same shape
        Squared bicoherence b^2(f1, f2).
    freqs : 1D ndarray
        Frequency axis in Hz.
    """
    from scipy.signal import detrend
    signal = detrend(signal)
    noverlap = int(nfft * overlap_ratio)
    step = nfft - noverlap
    n_segments = (len(signal) - nfft) // step + 1

    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    nf = len(freqs)

    B = np.zeros((nf, nf), dtype=complex)
    P12 = np.zeros((nf, nf), dtype=float)
    P3 = np.zeros((nf, nf), dtype=float)

    window = np.hanning(nfft)

    for seg_idx in range(n_segments):
        start = seg_idx * step
        segment = signal[start:start + nfft] * window
        X_full = np.fft.fft(segment)
        X = np.fft.rfft(segment)

        for i in range(nf):
            for j in range(i, nf):
                k = i + j
                if k < nfft:
                    val = X[i] * X[j] * np.conj(X_full[k])
                    B[i, j] += val
                    P12[i, j] += np.abs(X[i] * X[j]) ** 2
                    P3[i, j] += np.abs(X_full[k]) ** 2

    B /= n_segments
    P12 /= n_segments
    P3 /= n_segments

    # Bicoherence (avoid division by zero)
    denom = np.sqrt(P12 * P3)
    denom[denom == 0] = 1e-30
    bicoherence = (np.abs(B) ** 2) / (denom ** 2)

    return B, bicoherence, freqs
```

**Important:** The bispectrum computation is O(n_segments * nf^2), which can be slow. For this go/no-go test, use nfft=512 (257 frequency bins). This is a feasibility test, not a production run.

### Step 6: Generate Plots

Create a single figure with **4 rows x 3 columns** (one row per case):

| Column 1 | Column 2 | Column 3 |
|---|---|---|
| Time signal (last 0.2 s) | PSD (log scale, 0-200 Hz) | Bispectrum magnitude (2D color map, 0-200 Hz on both axes) |

- Row 1: Healthy
- Row 2: Crack (light, a/D = 0.2)
- Row 3: Crack (severe, a/D = 0.4)
- Row 4: Misalignment

For the bispectrum color maps:
- Use `matplotlib.pyplot.pcolormesh` with a sequential colormap (e.g., `'hot'` or `'inferno'`)
- Plot only the non-redundant region (f1 <= f2)
- Use log scale for the magnitude: `np.log10(np.abs(B) + 1e-30)`
- Mark the key frequency pairs with annotations:
  - (1X, 1X) = (25, 25) Hz
  - (1X, 2X) = (25, 50) Hz
  - (2X, 2X) = (50, 50) Hz

Also create a second figure: **bicoherence comparison** (1 row x 4 columns), one bicoherence 2D map per case, all with the same color scale for direct comparison.

Save all figures as PNG files (300 DPI) in the `02_go_no_go/` folder:
- `go_no_go_psd_bispectrum.png`
- `go_no_go_bicoherence.png`

### Step 7: Quantitative Summary

Print a summary table to the console:

```
============================================================
GO/NO-GO FEASIBILITY TEST RESULTS
============================================================

Case              | 1X Amp  | 2X Amp  | 3X Amp  | |B(1X,1X)| | |B(1X,2X)| | Biphase(1X,1X)
------------------+---------+---------+---------+-----------+-----------+----------------
Healthy           | ...     | ...     | ...     | ...       | ...       | ...
Crack (a/D=0.2)  | ...     | ...     | ...     | ...       | ...       | ...
Crack (a/D=0.4)  | ...     | ...     | ...     | ...       | ...       | ...
Misalignment      | ...     | ...     | ...     | ...       | ...       | ...

VERDICT:
- Crack vs Healthy (bispectrum): [DISTINGUISHABLE / NOT DISTINGUISHABLE]
- Misalignment vs Healthy (bispectrum): [DISTINGUISHABLE / NOT DISTINGUISHABLE]
- Crack vs Misalignment (bispectrum): [DISTINGUISHABLE / NOT DISTINGUISHABLE]

OVERALL: [GO / NO-GO / INCONCLUSIVE]
```

**Discrimination criteria:**
- A pair is "DISTINGUISHABLE" if the bispectrum magnitude at (1X,1X) or (1X,2X) differs by more than a factor of 3, OR the biphase differs by more than 30 degrees.
- OVERALL is "GO" if all three pairs are distinguishable.
- OVERALL is "NO-GO" if crack vs. misalignment is NOT distinguishable.
- OVERALL is "INCONCLUSIVE" if results are borderline (factor between 2 and 3, or phase difference between 15 and 30 degrees).

### Step 8: Interpretation Guide

At the end of the script, print a brief interpretation guide:

```
============================================================
INTERPRETATION GUIDE
============================================================

What to look for in the bispectrum plots:

1. HEALTHY rotor: The bispectrum should show a single peak at (1X, 1X) = (25, 25) Hz
   from the unbalance response. Minimal energy elsewhere.

2. CRACKED rotor: The breathing crack introduces quadratic phase coupling.
   Expect strong peaks at (1X, 1X) and (1X, 2X) with specific phase relationships.
   The peak at (1X, 1X) arises because the crack couples the 1X component
   with itself to produce 2X.

3. MISALIGNED rotor: Misalignment also produces 2X, but the phase coupling
   pattern differs. Expect peaks at (1X, 1X) and (1X, 2X) with DIFFERENT
   biphase angles compared to the crack case.

4. KEY DISCRIMINATOR: The biphase (phase of the bispectrum) at (1X, 1X)
   should be different for crack vs. misalignment even if the magnitudes
   are similar. This is the core hypothesis of the research.

If the bispectrum magnitudes AND phases look identical for crack and
misalignment, the research hypothesis needs revision.
```

### Additional Requirements

1. **Error handling:** If ROSS installation fails or time integration does not converge, print a clear error message and suggest next steps. Do not let the script crash silently.
2. **Execution time:** The entire script should run in under 5 minutes on a modern laptop.
3. **Code quality:** Use clear variable names, add docstrings, and include inline comments explaining the physics (this is a research tool, not a production app).
4. **Reproducibility:** Set `np.random.seed(42)` at the start. All parameters should be defined as constants at the top of the script for easy modification.
5. **Self-contained:** The script should not depend on any other files in the repository. Everything needed is defined inside the script.

### Output Files

The script should produce:
```
02_go_no_go/
    go_no_go_simulation.py          # The main script
    go_no_go_simulation.ipynb       # Jupyter notebook version
    go_no_go_psd_bispectrum.png     # Main comparison figure (generated on run)
    go_no_go_bicoherence.png        # Bicoherence comparison (generated on run)
```

### Success Criteria

After running the script, I should be able to:
1. See clear visual differences in the bispectrum between healthy, cracked, and misaligned cases
2. Read a quantitative summary table confirming the differences
3. Get a clear GO / NO-GO / INCONCLUSIVE verdict
4. Understand what I am looking at via the interpretation guide

This is the most important early experiment of my master's thesis. Make it count.
