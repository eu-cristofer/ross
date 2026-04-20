# Sinha (2007) validation table (copy-ready)

This table summarises quantities compared to Sinha (2007). Absolute and relative errors are computed as `model - Sinha`. Evidence pointers refer to artefacts in this repository; rerun notebooks to regenerate numbers (chain-of-verification).

## Modal frequencies (Hz)

| Sinha (2007) quantity | Model value (ROSS) | Absolute error | Relative error (%) | Evidence |
|----------------------|----------------------|----------------|---------------------|----------|
| Healthy 1st bending (FE) 26.53 | 27.500 | 0.970 | 3.66 | `05_sinha_modal_validation.ipynb`, `modal_comparison.csv` |
| Healthy 1st bending (exp) 27.50 | 27.500 | ~0 | ~0 | same |
| Healthy 2nd bending (FE) 228.62 | 187.606 | −41.014 | −17.94 | same; see conflicting evidence note in `05_sinha_modal_validation.ipynb` |
| Cracked 1st bending V (FE) 25.75 | 24.509 | −1.241 | −4.82 | same |
| Cracked 1st bending H (FE) 26.10 | 27.409 | 1.309 | 5.01 | same |
| Cracked 2nd bending V (FE) 226.00 | 173.772 | −52.228 | −23.11 | same |
| Cracked 2nd bending H (FE) 226.98 | 184.911 | −42.069 | −18.53 | same |
| Cracked 1st bending V/H (exp) 26.25 | 25.959 | −0.291 | −1.11 | same |
| Modal damping mode 1 (0.003) | 0.003 | 0 | 0 | Rayleigh fit `beta = 2ζ/ω₁` in `05_sinha_modal_validation.ipynb` |

## Higher-order spectra and figures

| Target | Status | Evidence |
|--------|--------|----------|
| Figs. 2, 4 amplitude spectra | Notebook `07_sinha_fig2_fig4_spectra.ipynb` | Harmonics annotated at 1X–3X |
| Fig. 3 crack orbits | Notebook `08_sinha_fig3_orbits.ipynb` | Uses acquisition chain on x/y DOFs |
| Figs. 5–6 bispectrum | Notebook `09_sinha_bispectrum.ipynb` | Uses `ross.hos.estimate_bispectrum` |
| Figs. 7–8 trispectrum slices | Notebooks `10_sinha_trispectrum.ipynb`, `12_sinha_hos_sensitivity.ipynb` | Uses `ross.hos.estimate_trispectrum_point` |
| Fault discrimination scalars | Notebook `11_sinha_fault_discrimination.ipynb` | Reads HDF5 from `06_sinha_timeseries.ipynb` when present |
| Acquisition chain (1 kHz LP, 10× decimate, 40 dB SNR) | `ross.hos.sinha_acquisition_chain`, `06_sinha_timeseries.ipynb` | Parameters documented in assumptions ledgers |

## Misalignment models

| Model | Description | Evidence |
|-------|-------------|----------|
| Flexible coupling (`run_misalignment`, `n = disk`) | Baseline ROSS misalignment | `04_sinha_fault_analysis.ipynb`, `sinha_tools.simulate_case(..., "misalignment")` |
| Pedestal proxy (`n = bearing_node − 1`) | Documented modelling proxy; not a geometric pedestal FE | `sinha_tools.simulate_case(..., "misalignment_pedestal")` |

## References

Sinha, J. K. (2007). Higher order spectra for crack and misalignment identification in the shaft of a rotating machine. *Structural Health Monitoring*, 6(4), 325–334.

Gasch, R. (1993). A survey of the dynamic behaviour of a simple rotating shaft with a transverse crack. *Journal of Sound and Vibration*, 160(2), 313–332.
