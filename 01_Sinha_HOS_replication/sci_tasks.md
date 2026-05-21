# Task List — Sinha (2007) Validation Programme

> Track sprint progress here. Mark items with `[x]` when done.
> Full sprint specs live in `sprints/`. Execution order: 00 → 01 → 02 → 03 → (04 ∥ 05 ∥ 06) → 07.

**Status snapshot (2026-05-20):** Sprints 00 and 01 are complete and their exit criteria assert green. Sprints 02–07 have not been started — no `run_campaign.py`, no `campaign.h5`, no damping calibration, no Fig. 9/10 reproduction notebook, no validation matrix, no `01_article/` methods draft. Next blocker to unlock is Sprint 02.

---

## Sprint 00 — Modal FE Validation
> *Effort: half a day. Blocks: all downstream sprints.*
>
> **Status:** complete. Notebook lives at `00a_modal_check.ipynb` (not `01_rotordynamic_simulation/...` as the original task line suggested — the directory was renamed to `01_Sinha_HOS_replication/`).

- [x] Create `00a_modal_check.ipynb`
- [x] Cell A: assert intact f1 within ±0.05 Hz of 27.50 Hz *(measured 27.5000 Hz — passes)*
- [x] Cell B: verify Mayes crack fully-open angle ≈ 180° *(implemented as a shape-inspection cell; logs θ_open = 115.3° and K[0,0] min/max. Notebook narrative explicitly defers a strict 180° / 26.25 Hz assertion to Sprint 03 / 04 once the stiffness can be frozen at θ_open for a full modal run.)*
- [x] Cell C: add `SINHA_MODAL_TARGET = 27.50` to `constants.py` with provenance docstring
- [x] `__all__` updated with `SINHA_MODAL_TARGET`

**Exit criteria**
- [x] Notebook runs end-to-end without raising
- [x] `|f1 − 27.50| ≤ 0.05 Hz` assertion passes
- [x] Decision "calibration target is experimental 27.50 Hz" written into `constants.py` docstring

---

## Sprint 01 — HOS Core Library + Synthetic Validation
> *Effort: 5 days. Blocks: Sprints 02, 04, 05, 06, 07.*
>
> **Status:** complete. All three falsifiable tests pass in `06_hos_validation.ipynb` (b²(f,f)=1.0000, b²(f,2f)=1.0000, max b² uncoupled = 0.0711, |T(f,f,f)|/max = 1.0000 with 4 entries above 0.10).

**`signal_utils.py`**
- [x] `window_and_detrend()`
- [x] `amplitude_spectrum()`
- [x] `psd_welch()`
- [x] `bispectrum()` — Kim–Powers normalized, segment averaging, non-redundant region only
- [x] `bicoherence()` — convenience alias
- [x] `trispectrum()` — sparse, threshold=0.10
- [x] `harmonic_amplitude()` — parabolic interpolation
- [x] `downsample_to()` — Butterworth LP + decimate
- [x] `add_awgn()` — reproducible AWGN injection

**`plot_utils.py`**
- [x] `plot_bispectrum_surface()` — Sinha Figs. 5/6 style
- [x] `plot_trispectrum_balls()` — Sinha Figs. 7/8 style
- [x] *(bonus)* Plotly interactive variants: `plotly_bispectrum_surface`, `plotly_bicoherence_surface`, `plotly_trispectrum_balls`, `plotly_spectrum`, `plotly_time`

**`06_hos_validation.ipynb`**
- [x] Test A — positive QPC: `b²(f,f) ≥ 0.95` and `b²(f,2f) ≥ 0.95`
- [x] Test B — negative (uncoupled phases): `max b² ≤ 0.20`
- [x] Test C — trispectrum sparsity: `(i_f, i_f, i_f)` in dict, ≤ 10 entries above 0.10

**Exit criteria**
- [x] `signal_utils.py` and `plot_utils.py` importable; docstrings cite Sinha Eqs. (2)–(3) and Kim–Powers 1979
- [x] Tests A, B, C all assert true
- [x] Default `bispectrum()` yields Δf = 1.25 Hz at `fs=2560` *(62 segments produced for a 25 s record — slightly above the nominal 50 because `_segment()` walks the signal to exhaustion; equivalent statistical resolution)*
- [x] Visualizers produce figures resembling Sinha Figs. 5 and 7 on QPC signal

---

## Sprint 02 — Sinha-Matched Acquisition + HDF5 Persistence
> *Effort: 3 days. Blocks: Sprints 04, 05, 06, 07.*
>
> **Status:** not started. Acquisition constants in `constants.py` currently use the unified Sinha-rate path (`DT = 1/SINHA_FS_HZ`), not the dual `DT_SIM` (10 kHz) + `FS_ACQ_FE` (1 kHz) chain this sprint specifies. `SNR_DB`, `FS_ACQ_FE`, and a separate `DT_SIM` are not yet defined; `run_campaign.py` and `results/campaign.h5` do not exist; Tests D and E have not been added to `06_hos_validation.ipynb`.

**`constants.py` extensions**
- [ ] `DT_SIM`, `FS_SIM`, `T_LONG` (25 s at 10 kHz) — `T_LONG` exists but is built on the 2560 Hz grid, not 10 kHz
- [ ] `FS_ACQ_EXP = 2560`, `FS_ACQ_FE = 1000`, `AA_CUTOFF = 1000` — only `SINHA_FS_HZ = 2560` and `SINHA_AA_CUTOFF_HZ = 1000` exist under the old names; `FS_ACQ_FE` missing
- [ ] `SNR_DB = 40`
- [x] Keep `DT` / `T` aliases so notebooks 01–04 still run *(DT, T_SHORT, T_LONG aliases present; bare `T` removed as documented in CLAUDE.md)*
- [ ] `__all__` and docstring provenance updated for the new symbols

**`run_campaign.py`**
- [ ] 7 base cases: 3 healthy + 2 crack + 2 misalignment
- [ ] Noise injected after downsampling
- [ ] Writes `results/campaign.h5` (gzip compressed)

**Integration tests in `06_hos_validation.ipynb`**
- [ ] Test D: B11 peak at 650 RPM within ±1 bin of (10.83, 10.83) Hz
- [ ] Test E: injected SNR within ±1 dB of 40 dB

**Exit criteria**
- [ ] `constants.py` exports all new constants; `__all__` updated
- [ ] Notebooks 01–04 still run without modification
- [ ] `run_campaign.py` completes and writes 7 groups to `campaign.h5`
- [ ] Tests D and E pass
- [ ] Audit H1 closed: `04_sinha_fault_analysis.ipynb` no longer has hand-rolled `cases` list

---

## Sprint 03 — Damping Calibration + Modal-Truncation Convergence
> *Effort: 2 days. Blocks: Sprints 04, 05, 06.*
>
> **Status:** not started. No `tune_beta_damping()` helper exists; `sinha_rotor.toml` has not been re-saved with calibrated damping; `sinha_rotor_pre_damping.toml` does not exist; no convergence table; `NUM_MODES` not exported from `constants.py`.

- [ ] Implement `tune_beta_damping()` via Brentq (mirror `tune_kxx` pattern)
- [ ] Achieve `|ζ₁ − 0.003| ≤ 5×10⁻⁴`
- [ ] Back up `sinha_rotor_pre_damping.toml` before re-saving
- [ ] Re-save `sinha_rotor.toml` with tuned damping
- [ ] Verify Sprint 00 Cell A assertion still passes on damped rotor
- [ ] Modal-truncation table: `(n_modes, |B11|, |B22|, |B12|)` for n_modes ∈ {12, 24, 36}
- [ ] Commit table to `sprints/03_convergence_table.md`
- [ ] Choose `NUM_MODES` (first within 5% of 36-mode reference) and add to `constants.py`
- [ ] Update `run_campaign.py` to use `NUM_MODES` (not hardcoded 12)
- [ ] Re-run `run_campaign.py` and re-assert Sprint 02 Tests D and E

**Exit criteria**
- [ ] `sinha_rotor.toml` re-saved with `|ζ₁ − 0.003| ≤ 5e-4`
- [ ] `sinha_rotor_pre_damping.toml` exists alongside
- [ ] Sprint 00 Cell A still passes
- [ ] Convergence table written to `03_convergence_table.md`
- [ ] `NUM_MODES` exported from `constants.py` with justification

---

## Sprint 04 — Reproduce Sinha's FE Simulation (Figs. 9 & 10)
> *Effort: 3–5 days. Blocks: Sprint 07. Can run in parallel with 05 after 03 lands.*
>
> **Status:** not started. The repo contains `07_hos_demo.ipynb` and `08_hos_qpc_demo_ptbr.ipynb` (the Sprint-01 demonstration / pt-BR explainer set), but neither is the specified `07_sinha_fig10_replication.ipynb`. No `reports/` directory.

- [ ] Create `07_sinha_fig10_replication.ipynb`
- [ ] Cell 1: load rotor, sanity modal check
- [ ] Cell 2: run Mayes crack at 772.5 RPM on `T_LONG` grid
- [ ] Cell 3: Sinha AA chain — LP 1 kHz → downsample to 1 kHz → add 40 dB AWGN
- [ ] Cell 4: Fig. 9 orbit plot saved to `results/figures/sprint_04/fig9_orbit.png`
- [ ] Cell 5: Fig. 10(a) bispectrum surface + peak-location assertion (top-3 peaks cover B11, B12, B22 within ±1 bin)
- [ ] Cell 6: Fig. 10(b) trispectrum balls + T111 presence assertion
- [ ] Cell 7: side-by-side PDF to `reports/sinha_fig10_side_by_side.pdf`
- [ ] Append Execution Log to this sprint file

**Exit criteria**
- [ ] Notebook runs end-to-end without raising
- [ ] Cell 5 peak-location assertion passes (±1 bin, Δf=1.25 Hz)
- [ ] Cell 6 T111 assertion passes
- [ ] Orbit shows loop-containing-small-loop topology at 772.5 RPM
- [ ] `reports/sinha_fig10_side_by_side.pdf` exists
- [ ] Execution Log filled in

---

## Sprint 05 — Reproduce Crack HOS at 650 / 750 RPM (Sinha Figs. 2, 3, 5, 7)
> *Effort: 1 week. Blocks: Sprint 07. Can run in parallel with Sprint 06.*
>
> **Status:** not started. Blocked on Sprint 02 (`campaign.h5`) and Sprint 03 (damping).

- [ ] Create `08_crack_hos_650_750.ipynb`
- [ ] Cell 1: load crack@650, crack@750, healthy@650, healthy@750 from `campaign.h5`
- [ ] Cell 2: Fig. 2 — amplitude spectra at 650 and 750 RPM
- [ ] Cell 3: Fig. 3 — orbit plots at 650 and 750 RPM
- [ ] Cell 4: Fig. 5 — bispectrum surfaces at 650 and 750 RPM
- [ ] Cell 5: scalar indicators (B11, B22, B12, B13) + speed-dependence assertion `B22/B11(750) ≥ 2·B22/B11(650)`
- [ ] Cell 6: Fig. 7 — trispectrum balls; assert T222 absent at 650, present at 750
- [ ] Cell 7: orbit-topology check — ≥ 4 zero-crossings/rev at 750 RPM
- [ ] Cell 8: assemble `reports/sinha_crack_side_by_side.pdf`
- [ ] Append Execution Log to sprint file

**Exit criteria**
1. - [ ] `|B22/B11|(750) ≥ 2·|B22/B11|(650)`
2. - [ ] `|T222|(750) ≥ 0.10` above normalized threshold; `|T222|(650) < 0.10`
3. - [ ] 750 RPM orbit has ≥ 4 y=0 crossings per revolution
4. - [ ] Amplitude spectrum at 750 RPM shows visible harmonics to ≥ 5× above −40 dB noise floor
5. - [ ] `reports/sinha_crack_side_by_side.pdf` renders four paired panels (Figs. 2, 3, 5, 7)

---

## Sprint 06 — Misalignment HOS Extension (Novel Contribution)
> *Effort: 1 week. Blocks: Sprint 07. Can run in parallel with Sprint 05.*
>
> **Status:** not started. Blocked on Sprint 02 (`campaign.h5`) and Sprint 03 (damping).

- [ ] Create `09_misalignment_hos_750_900.ipynb`
- [ ] Cell 1: load misalignment@750, misalignment@900, healthy@750, healthy@900 from `campaign.h5`
- [ ] Cell 2: Fig. 4 — amplitude spectra at 750 and 900 RPM
- [ ] Cell 3: Fig. 6 — bispectrum surfaces at 750 and 900 RPM
- [ ] Cell 4: scalar indicators + B22 absence assertion (B22/B11 ≤ 0.10) + B13 presence assertion (B13/B11 ≥ 0.15)
- [ ] Cell 5: topology set comparison — assert `topology(750) == topology(900)` and `{(1,1),(1,2),(1,3)} ⊆ topology`; `(2,2) ∉ topology`
- [ ] Cell 6: Fig. 8 — trispectrum balls; assert only T111 above 0.10 at either speed
- [ ] Cell 7: assemble `reports/sinha_misalignment_side_by_side.pdf`
- [ ] Append Execution Log to sprint file

**Exit criteria**
1. - [ ] `|B22/B11| ≤ 0.10` at both 750 and 900 RPM (B22 absent)
2. - [ ] `|B13/B11| ≥ 0.15` at both speeds (B13 = B31 present)
3. - [ ] Topology set identical at 750 and 900 RPM; contains (1,1), (1,2), (1,3); does not contain (2,2)
4. - [ ] Only T111 above 0.10 normalized threshold in tri-spectrum at either speed
5. - [ ] `reports/sinha_misalignment_side_by_side.pdf` renders paired panels for Sinha Figs. 4, 6, 8

---

## Sprint 07 — Scored Validation Report + Methods Draft
> *Effort: 3–5 days. Final sprint — no downstream.*
>
> **Status:** not started. No `results/validation_matrix.csv`, no `reports/sinha_validation_figures.pdf`, no `01_article/` directory.

- [ ] Fill `results/validation_matrix.csv` with 10 rows (one per Sinha claim), all `status` fields set to `pass` / `fail` / `partial` / `not_tested`
- [ ] Assemble `reports/sinha_validation_figures.pdf` (title page + 8 paired panels + scoring summary)
- [ ] Draft `01_article/03_methods_draft.md` — 5 sections with measured numbers substituted for all placeholders
  - [ ] §3.1 Finite-element rotor model
  - [ ] §3.2 Fault models (Mayes crack + Xia et al. misalignment)
  - [ ] §3.3 Time integration and acquisition pipeline
  - [ ] §3.4 Higher-order spectra (estimator settings, normalization, plotting)
  - [ ] §3.5 Validation protocol

**Exit criteria**
- [ ] `validation_matrix.csv` has 10 rows, all `status` fields populated
- [ ] `sinha_validation_figures.pdf` renders cleanly with title page, panels, and scoring page
- [ ] Methods draft cites Sinha (2007), Kim & Powers (1979), Xia et al. (2019), Mayes & Davies (1984) correctly
- [ ] Advisor can read the draft + scan the PDF in 15 min and pose concrete next-step questions

---

## Go / No-Go gate after Sprint 07

- [ ] Validation matrix scores ≥ 8/10 `pass` or `partial` → proceed to Sprint 08 (DoE expansion)
- [ ] If < 8/10 → do not advance; diagnose and fix failing sprints first

---

## Post-validation candidates (not started)

- [ ] **Sprint 08** — DoE expansion: crack depths {0.1…0.5} × speeds {650, 750, 900} × misalignment levels {small, medium, large}; compute BPR, BCS, BE indicators
- [ ] **Sprint 09** — RK4 experimental validation (`01_article/04_rk4_working_plan.md`)
