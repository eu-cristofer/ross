# Active Plan — Rotordynamic Simulation

A living document. Captures **what is being worked on right now, what is
blocking it, and what is queued next**. The detailed step-by-step is in
[`../sprints/`](../sprints/); this file is the dashboard on top of those
sprints.

> **Update cadence.** Touch this file whenever a sprint changes status,
> a blocker appears, or a decision needs the user's input. Stale entries
> > 14 days old should be re-confirmed or moved to "Done / archived".
>
> **Today:** 2026-05-19
> **Thesis defence deadline:** February 2026 (≈ 9 months from today)
> **Journal-paper submission target:** within 2 months of thesis defence

---

## 1. Current focus

**Sprint 02 — Sinha-matched acquisition + persisted long records.**
([brief](../sprints/02_acquisition_long_records.md))

The HOS core (Sprint 01) is done and unit-validated, but the existing probe
records are 2 s @ 2560 Hz (5 120 samples), which is ~10× too short for the
50-segment estimator at Δf = 1.25 Hz. Sprint 02 builds the long-record
campaign driver and the HDF5 dataset that Sprints 04–06 will read.

### This-week checklist (working set)

- [ ] Add `DT_SIM`, `FS_SIM_NEWMARK`, `FS_ACQ_FE`, `SNR_DB` to `constants.py`
      with provenance docstring (see [D-005](DECISIONS.md#d-005)).
- [ ] Decide HDF5 layout (one group per `(condition, speed_rpm)` case;
      attributes for `dt_sim`, `fs_out`, `aa_cutoff`, `snr_db`, `seed`,
      `git_sha`, `created_at`).
- [ ] Implement `run_campaign.py` with the three conditions × three speeds
      grid (`healthy`, `crack`, `misalignment` × `{650, 750, 900}` rpm) —
      see [sprint 02 §2](../sprints/02_acquisition_long_records.md).
- [ ] Append two integration-test cells to `06_hos_validation.ipynb` that
      read back the first case and assert the segment count + Δf at fs = 1000
      and fs = 2560.
- [ ] Resolve open code-review items (see §3 below) that touch the same
      files — one pass, not two.

### Definition of done for this sprint

All four exit criteria in
[`sprints/02_acquisition_long_records.md`](../sprints/02_acquisition_long_records.md)
satisfied, plus an Execution Log entry committed.

---

## 2. Sprint board

| Sprint | Status | Owner | Notes |
|---|---|---|---|
| 00 — Modal validation | **done** | Cristofer | `00a_modal_check.ipynb` asserts \|f₁ − 27.50\| ≤ 0.05 Hz. |
| 01 — HOS core | **done** | Cristofer | `signal_utils.py` + tests A/B/C pass in `06_hos_validation.ipynb`. Demos: `07_hos_demo.ipynb`, `08_hos_qpc_demo_ptbr.ipynb`. |
| 02 — Acquisition + long records | **in progress** | Cristofer | See §1 above. |
| 03 — Damping ζ₁ = 0.3 % + modal truncation | queued | Cristofer | Unblocked by 02. Audit H4 — `num_modes=12` convergence check. |
| 04 — FE-to-FE Fig. 10 replication | queued | Cristofer | Unblocked by 03. Cleanest validation target (no rig variance). |
| 05 — Crack HOS @ 650 / 750 RPM | queued | Cristofer | Unblocked by 03; parallel with 04. |
| 06 — Misalignment HOS @ 750 / 900 RPM | queued | Cristofer | Unblocked by 03; parallel with 04, 05. **Novel** ([D-008](DECISIONS.md#d-008)). |
| 07 — Validation matrix + Methods draft | queued | Cristofer | Final sprint. Needs ≥ 8/10 pass/partial to unlock DoE. |

Dependency graph: [`sprints/README.md`](../sprints/README.md#execution-order).

---

## 3. Open code-review items (blocking quality, not progress)

From [`code_review.md`](../code_review.md) (2026-04-24). P0/P1 should be
cleared **before** rerunning analysis notebooks from a clean kernel.

| Priority | Item | File(s) | Status |
|---|---|---|---|
| P0 | `constants.__all__` exported `"T"` but only `T_SHORT` / `T_LONG` defined | `constants.py` | **resolved** — `"T"` removed; notebooks `02`/`03`/`04` need a rerun to refresh stale cell outputs |
| P0 | `SInha targets.md` → `sinha_targets.md` (capitalisation + space) | filesystem | **resolved** |
| P1 | `04_sinha_fault_analysis.ipynb` overrides `CRACK_NODE`, `CRACK_RATIO`, `FREQ_RANGE`, `MIS_X/Y` inline | `04_…ipynb` | **open** |
| P1 | `04` has `from constants import *` in cell 4 instead of import cell | `04_…ipynb` | **open** |
| P1 | Extract shared helpers (`get_harmonic_amplitude`, `annotate_harmonics`, FFT-of-steady-state, colour list) | several | **partial** — `sinha_helpers.py` exists with `get_harmonic_amplitude` and `probe_dof_indices`; rest pending |
| P2 | Standardise on explicit imports | all notebooks | **open** |
| P2 | Drop unused `from ross.materials import Material` and redundant `Q_ = rs.Q_` shims | `00`, `04` | **open** |
| P3 | Docstring drift in `04` helpers (`run_healthy_baseline` documents `speed_crack_0`, takes `speed_crack`) | `04_…ipynb` | **open** |
| P3 | Unresolved TODO in `02` cell 12; empty cell in `02` cell 17 | `02_…ipynb` | **open** |

When picking these up, prefer batching by file (one notebook, one PR) rather
than by priority — fewer kernel restarts.

---

## 4. Decisions awaiting input

None at the moment. The active design decisions are recorded in
[`DECISIONS.md`](DECISIONS.md). If a new question arises that needs a
deliberate choice (e.g. "do we add Flex Breathing back into the validation
matrix?"), draft a `D-NNN` entry in `DECISIONS.md` with status `proposed`
and link it from here.

---

## 5. Risks and watch-items

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ROSS `run_misalignment` (Xia 2019) does not produce Sinha-like dense harmonic combs at 750 / 900 RPM | medium | high (kills [D-008](DECISIONS.md#d-008) novelty claim) | Spike on Sprint 06 figure 4 early — within first 2 days of starting 06. Fall back to documenting the *failure to reproduce* as a methodological finding. |
| Sprint 02 long records make integration too slow on the development laptop | medium | medium | Profile one `T_LONG` Newmark-β run before committing to the full 9-case campaign. If > 30 min per case, move the campaign to a workstation / GPU box. |
| `num_modes=12` truncation biases T222 amplitudes (audit H4) | medium | medium | Sprint 03 convergence table — sweep `num_modes ∈ {8, 12, 16, 20}` at the worst case (900 rpm misalignment) and pick the smallest value where T222 changes < 5 %. |
| Sinha-§5 noise injection (`SNR_DB = 40`) makes bispectral features at low B22 amplitudes indistinguishable from noise floor | low | medium | Test Sprint 01's positive/negative cases at `SNR_DB ∈ {20, 30, 40, 60}` to bracket the floor before Sprint 05. |
| Validation matrix scores < 8/10 → DoE deferred → thesis chapter loses its "parametric study" leg | low-medium | high | Plan B: pivot the thesis chapter from parametric DoE to depth-of-validation, using the 10-claim matrix as the headline. |

---

## 6. Done / archived

- 2026-04-23 — Decided calibration target (Sinha §3 27.50 Hz, not §5
  26.53 Hz). See [D-001](DECISIONS.md#d-001).
- 2026-04-23 — Established `constants.py` as single source of truth.
  See [D-002](DECISIONS.md#d-002).
- 2026-04-23 — Froze Mayes-only crack model for the validation programme.
  See [D-003](DECISIONS.md#d-003).
- 2026-04-25 — Sprint 00 complete (`00a_modal_check.ipynb`, `SINHA_MODAL_TARGET`).
- 2026-04-25 — Sprint 01 complete (`signal_utils.py`, `plot_utils.py`,
  validation notebook).
- 2026-04-25 — HOS demo notebooks landed (`07_hos_demo.ipynb`,
  `08_hos_qpc_demo_ptbr.ipynb`).
