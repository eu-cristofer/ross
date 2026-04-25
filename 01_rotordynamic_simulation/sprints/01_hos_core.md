# Sprint 01 — HOS core library + synthetic validation

> **Effort:** 5 days.
> **Blocks:** Sprints 02, 04, 05, 06, 07.
> **Unblocked by:** Sprint 00.
> **Artefacts produced:** `01_rotordynamic_simulation/signal_utils.py`, `01_rotordynamic_simulation/plot_utils.py`, `01_rotordynamic_simulation/06_hos_validation.ipynb`.

## Why this sprint exists

Sinha's entire diagnostic argument rests on two equations:

$$\text{Bi-spectrum:} \quad B_{xxx}(f_l, f_m) = \mathbb{E}\left[X(f_l)\, X(f_m)\, X^{*}(f_l+f_m)\right], \qquad l + m \le N$$

$$\text{Tri-spectrum:} \quad T_{xxxx}(f_l, f_m, f_n) = \mathbb{E}\left[X^{*}(f_l)\, X^{*}(f_m)\, X^{*}(f_n)\, X(f_l+f_m+f_n)\right]$$

(Sinha Eqs. 2–3; the expectation is estimated by segment averaging.) The repository contains **zero lines** of code that implements either estimator. Every downstream claim about B11 / B22 / B13 / T111 / T222 needs these operators to exist and be correct.

Equally important: without a trusted estimator, the long-record acquisition sprint (02) has no reference for "is the pipeline actually delivering Sinha-quality segments." Hence the ordering in this plan — HOS core first, then the data generator.

## Prerequisites

- Sprint 00 complete.
- `numpy`, `scipy`, `matplotlib`, `plotly` available in the `research` conda env.

## Deliverables

### 1. `01_rotordynamic_simulation/signal_utils.py`

Module-level docstring must state the normalization convention (Kim & Powers 1979) and reference Sinha Eqs. (2), (3) with the exact indexing used here. Functions:

```python
def window_and_detrend(x: np.ndarray, window: str = "hann") -> tuple[np.ndarray, np.ndarray]:
    """Detrend (scipy.signal.detrend, type='constant') then apply ``window``.

    Returns
    -------
    xw : np.ndarray    windowed signal
    w  : np.ndarray    the window itself (for amplitude correction downstream)
    """

def amplitude_spectrum(x, fs, window="hann") -> tuple[np.ndarray, np.ndarray]:
    """Single-sided Hann-corrected amplitude spectrum.

    Correction: 2 * |rfft(xw)| / sum(w).  Rectangular window (``"boxcar"``)
    collapses to the familiar 2/N.
    """

def psd_welch(x, fs, nperseg, noverlap, window="hann"):
    """Thin wrapper around ``scipy.signal.welch`` with sensible defaults."""

def bispectrum(x, fs, nfft, noverlap, window="hann") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Kim–Powers normalized bispectrum via segment averaging (direct method).

    Returns
    -------
    B         : complex ndarray, shape (nf, nf)    raw Bxxx(f_l, f_m)
    b2        : real ndarray,    shape (nf, nf)    bicoherence squared, in [0, 1]
    freqs     : ndarray,         shape (nf,)       single-sided Hz axis

    Implementation
    --------------
    * Hoist ``X_full = np.fft.fft(xw)`` outside the (f_l, f_m) double loop.
    * Accumulate ``B``, ``P12 = |X(f_l) X(f_m)|^2``, and ``P3 = |X(f_l+f_m)|^2``
      in parallel so bicoherence comes for free.
    * Normalize ``B /= K`` (K = number of segments) and
      ``b2 = |B|^2 / (⟨P12⟩ ⟨P3⟩)`` with a ``max(denom, 1e-30)`` guard.
    * Restrict to the non-redundant region ``f_l ≤ f_m`` and ``f_l + f_m ≤ Nyquist``.
    """

def bicoherence(x, fs, nfft, noverlap, window="hann") -> tuple[np.ndarray, np.ndarray]:
    """Convenience alias: returns ``(b2, freqs)`` from :func:`bispectrum`."""

def trispectrum(
    x, fs, nfft, noverlap, window="hann",
    threshold: float = 0.10,
) -> tuple[dict, np.ndarray]:
    """Sparse tri-spectrum estimator (Kim–Powers normalized).

    Returns the dict of ``{(l, m, n): Txxxx_lmn}`` where
    ``|Txxxx| / max|Txxxx| >= threshold`` and ``l + m + n <= Nyquist bin``.
    Sparse by design so the O(N^3) storage does not blow up.
    Matches Sinha's "amplitudes above 0.1 plotted" convention for Fig. 7–8.
    """

def harmonic_amplitude(x, fs, f_target, window="hann") -> float:
    """Hann-corrected peak amplitude at ``f_target`` via parabolic interpolation
    across the 3 nearest bins of the amplitude spectrum. Replaces the
    nearest-bin ``argmin`` helper currently duplicated in notebooks 02 and 03.
    """

def downsample_to(x, fs_sim: float, fs_out: float, aa_cutoff_hz: float) -> np.ndarray:
    """Butterworth low-pass at ``aa_cutoff_hz`` (order 8, zero-phase filtfilt)
    then decimate by ``int(fs_sim / fs_out)``. Lives here (not campaign.py)
    so Sprint 04 can use it on its 10 kHz Newmark-β output.
    """

def add_awgn(x, snr_db: float, rng=None) -> np.ndarray:
    """Additive white Gaussian noise to achieve the target SNR in dB
    (Sinha §5: SNR_DB = 40). ``rng`` is a ``np.random.Generator`` for
    reproducibility."""
```

**Constants** to pull from `constants.py` inside `bispectrum` / `trispectrum`: `SINHA_HOS_DF_HZ = 1.25`, `SINHA_HOS_N_SEGMENTS = 50`, `SINHA_HOS_OVERLAP = 0.5`. These are the Sinha §3.3 settings and must be the default when no explicit `nfft`/`noverlap` is passed.

### 2. `01_rotordynamic_simulation/plot_utils.py`

Sinha-convention visualizers (mirror Figs. 5, 6, 7, 8, 10):

```python
def plot_bispectrum_surface(B, freqs, fmax_hz=50.0, normalize=True):
    """3-D surface of |B|/max|B| over the non-redundant triangle
    f_l ≤ f_m, f_l + f_m ≤ fmax_hz. Hot colormap, Sinha Figs. 5/6 style.
    Returns a matplotlib or plotly figure — pick one and stay consistent."""

def plot_trispectrum_balls(T_dict, freqs, fmax_hz=35.0, amp_min=0.10):
    """Scatter3D where each (l,m,n) with |T|≥amp_min becomes a ball whose
    diameter scales with amplitude. Matches Sinha Figs. 7, 8, 10(b)."""
```

### 3. `01_rotordynamic_simulation/06_hos_validation.ipynb`

A validation notebook with **two falsifiable unit tests** that decide whether the HOS core is trustworthy.

**Test A — positive (enforced quadratic phase coupling).**
```python
fs = 2560.0
T_len = 25.0
t = np.arange(0, T_len, 1/fs)
f = 12.5  # Hz — close to Sinha's 1X at 750 RPM
phi = 1.3  # arbitrary fixed phase
x = (
    np.cos(2*np.pi*f*t)
    + 0.5 * np.cos(2*np.pi*2*f*t + 2*phi)        # 2f with phase 2*phi — quadratically coupled
    + 0.5 * np.cos(2*np.pi*3*f*t + 3*phi)        # 3f with phase 3*phi — cubically coupled
)

from signal_utils import bispectrum, trispectrum
B, b2, freqs = bispectrum(x, fs)

i_f  = np.argmin(np.abs(freqs - f))
i_2f = np.argmin(np.abs(freqs - 2*f))

assert b2[i_f,  i_f]  >= 0.95, f"b²(f,f)  = {b2[i_f,i_f]:.3f}, want ≥ 0.95"
assert b2[i_f,  i_2f] >= 0.95, f"b²(f,2f) = {b2[i_f,i_2f]:.3f}, want ≥ 0.95"
```

**Test B — negative (independent random phases per segment).**
```python
# Same f, 2f, 3f components but re-randomized phases per 1-second block.
rng = np.random.default_rng(42)
n_seg = int(T_len)
x_uncoupled = np.concatenate([
    (np.cos(2*np.pi*f*t_[:int(fs)] + rng.uniform(0, 2*np.pi))
     + 0.5*np.cos(2*np.pi*2*f*t_[:int(fs)] + rng.uniform(0, 2*np.pi))
     + 0.5*np.cos(2*np.pi*3*f*t_[:int(fs)] + rng.uniform(0, 2*np.pi)))
    for _ in range(n_seg)
])
# (sketch — replace the block-wise construction with whatever keeps the spectrum
# identical to Test A but breaks the phase relation between segments.)

_, b2_neg, _ = bispectrum(x_uncoupled, fs)
assert b2_neg.max() <= 0.20, f"max b² = {b2_neg.max():.3f}, want ≤ 0.20"
```

The negative test is the one that catches broken implementations. A common bug is to accidentally normalise by `|X(f_l+f_m)|` *per segment* rather than ⟨|X(f_l+f_m)|²⟩ — that error makes b² ≈ 1 *even for uncoupled signals*. Both tests must pass.

**Test C — trispectrum sparsity.** Re-run Test A through `trispectrum`, assert that `(i_f, i_f, i_f)` is in the returned dict with `|T| / T_max ≥ 0.95`, and that the dict has ≤ 10 entries above the 0.1 threshold (i.e. the sparsity contract is honoured).

## Exit criteria

- [ ] `signal_utils.py` and `plot_utils.py` importable; docstrings cite Sinha Eqs. (2), (3) and Kim–Powers 1979.
- [ ] `06_hos_validation.ipynb` runs end-to-end with Test A, B, C all asserting true.
- [ ] `bispectrum()` default parameters yield Δf = 1.25 Hz and 50 segments at 50% overlap (Sinha §3.3) when called with `fs=2560`.
- [ ] `plot_bispectrum_surface` and `plot_trispectrum_balls` produce figures that *visually* resemble Sinha Figs. 5 and 7 when handed an enforced-QPC signal.

## Implementation discipline

- **Do not** use the Appendix A.2 reference code from `01_article/01_publication_roadmap.md` verbatim — it recomputes the full FFT inside the `(f_l, f_m)` loop. Hoist it. The `03_ross_agent_prompt.md` version is the better starting point.
- **Hann-amplitude correction:** `|rfft(xw)| * 2 / sum(w)` for a single-sided amplitude spectrum. Rectangular window degenerates to the familiar `2/N`.
- **Kim–Powers normalization:** bispectral amplitude is divided by `sum(w**3)` implicitly via the `⟨P12⟩⟨P3⟩` denominator — do NOT additionally divide by a rectangular-window factor.
- **NaN / small-denominator:** replace any `denom < 1e-30` with `1e-30`. Never let `b2` go negative.
- **Non-redundant region only:** mask out `f_l > f_m` and `f_l + f_m > Nyquist` before returning. Makes plots cleaner and halves memory.

## Dependencies / hand-offs

- Unblocks Sprint 02 (which will load its first long record and run it through `bispectrum`).
- The `downsample_to` and `add_awgn` helpers are used by Sprint 02's `run_campaign.py` and Sprint 04's Fig. 10 replication.
- The two plotters become the default throughout Sprints 04–06.

## References

- Sinha (2007), §2.1–2.2 (HOS definitions), §3.3 (estimator settings). `99_references/`.
- Kim, Y. C., & Powers, E. J. (1979). Digital Bispectral Analysis and Its Applications to Nonlinear Wave Interactions. *IEEE Trans. Plasma Science* 7(2), 120–131. The normalization convention.
- Collis, W. B., White, P. R., & Hammond, J. K. (1998). Higher-order spectra: the bispectrum and trispectrum. *MSSP* 12(3), 375–394. Cited by Sinha as [23]; the reference implementation textbook.
- Existing audit: `01_rotordynamic_simulation/05_synthesis.ipynb` §3.2 (H2, H3), §4.1 Step 2, §4.1 Step 2 Appendix.
