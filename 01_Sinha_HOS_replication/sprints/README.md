# Sprints — Sinha (2007) validation programme

This directory contains the step-by-step plan to validate the ROSS-based simulation pipeline against Sinha (2007), *Higher Order Spectra for Crack and Misalignment Identification in the Shaft of a Rotating Machine* (Structural Health Monitoring 6(4), 325–334). The paper is at `99_references/Sinha - 2007 - ...pdf`; the rolled-up audit that motivated this plan is at `01_rotordynamic_simulation/05_synthesis.ipynb`.

Each sprint is a self-contained `.md` — purpose, prerequisites, work items, exit criteria. Hand any single file to an AI coding agent (or a student) and it should be executable without reading the others.

## Execution order

```
00 ── 01 ── 02 ── 03 ── 04
                  │     │
                  ├──> 05 ─┐
                  └──> 06 ─┴──> 07
```

- **Sprint 00 → 03** are linear. Each blocks the next.
- **Sprint 04 (FE replication of Fig. 10)** can run in parallel with Sprint 05 once Sprint 03 has landed.
- **Sprints 05 and 06** can run in parallel (they read independent HDF5 groups).
- **Sprint 07** consumes every prior sprint's Execution Log.

## The sprints

| # | File | Title | Artefact |
|---|---|---|---|
| 00 | [`00_modal_validation.md`](00_modal_validation.md) | Modal FE validation against Sinha §3 and §5 | `01_rotordynamic_simulation/00a_modal_check.ipynb`, constant `SINHA_MODAL_TARGET` |
| 01 | [`01_hos_core.md`](01_hos_core.md) | HOS core library + synthetic tests (positive + negative) | `signal_utils.py`, `plot_utils.py`, `06_hos_validation.ipynb` |
| 02 | [`02_acquisition_long_records.md`](02_acquisition_long_records.md) | Sinha-matched acquisition pipeline + HDF5 persistence | extended `constants.py`, `run_campaign.py`, `results/campaign.h5` |
| 03 | [`03_damping_and_modal_truncation.md`](03_damping_and_modal_truncation.md) | ζ₁ = 0.3 % damping calibration + `num_modes` convergence | damping-tuned `sinha_rotor.toml`, `00b_damping_check.ipynb`, `03_convergence_table.md` |
| 04 | [`04_sinha_fe_replication.md`](04_sinha_fe_replication.md) | Reproduce Sinha Figs. 9 & 10 (FE-to-FE) | `07_sinha_fig10_replication.ipynb` |
| 05 | [`05_crack_hos_replication.md`](05_crack_hos_replication.md) | Reproduce Sinha Figs. 2, 3, 5, 7 (crack at 650/750 RPM) | `08_crack_hos_650_750.ipynb`, `reports/sinha_crack_side_by_side.pdf` |
| 06 | [`06_misalignment_hos.md`](06_misalignment_hos.md) | Reproduce Sinha Figs. 4, 6, 8 (novel: Sinha could not FE-simulate misalignment) | `09_misalignment_hos_750_900.ipynb`, `reports/sinha_misalignment_side_by_side.pdf` |
| 07 | [`07_validation_report.md`](07_validation_report.md) | Scored validation matrix + Methods section draft | `results/validation_matrix.csv`, `reports/sinha_validation_figures.pdf`, `01_article/03_methods_draft.md` |

**Nominal total:** ≈ 5 calendar weeks.

## The 10 falsifiable claims this programme validates

Every sprint's exit criterion is a quantitative test of one of the 10 claims Sinha (2007) makes about bi- and tri-spectrum features. The scorecard lives in `results/validation_matrix.csv` after Sprint 07.

| # | Claim | Sinha source | Tested in |
|---|---|---|---|
| 1 | Intact f1 ≈ 27.50 Hz; fully-open cracked f1 ≈ 26.25 Hz | §3, §5 | 00 |
| 2 | Cracked amplitude spectra show 1X + 2X + higher harmonics | Fig. 2 | 05 |
| 3 | Cracked orbits: figure-eight → loop-containing-small-loop | Fig. 3 | 05 |
| 4 | Misalignment amplitude spectra show dense harmonic combs | Fig. 4 | 06 |
| 5 | Crack bi-spectrum B22 emerges at 650, prominent at 750 (speed-dep.) | Fig. 5 | 05 |
| 6 | Misalignment bi-spectrum: B13 present, B22 absent, speed-independent | Fig. 6 | 06 |
| 7 | Crack tri-spectrum speed-dependent; T222 appears at 750 | Fig. 7 | 05 |
| 8 | Misalignment tri-spectrum: only T111 at both speeds | Fig. 8 | 06 |
| 9 | Healthy rotor: |B|, |T| < 0.3 everywhere (noise floor) | §4 | 02, 05, 06 |
| 10 | Sinha's own FE (Fig. 10) reproducible numerically | §5, Figs. 9, 10 | 04 |

## Novel contribution relative to Sinha (2007)

Sinha could not FE-simulate misalignment ("the force function due to the shaft misalignment is not well stood", §5). Claims 6 and 8 — reproduced in Sprint 06 via ROSS's `run_misalignment` (Xia et al. 2019 flex-coupling model) — therefore constitute the thesis' contribution beyond the paper.

## Artefact locations

```
01_rotordynamic_simulation/
├── sprints/                         ← this directory
├── constants.py                     ← extended in Sprint 02
├── sinha_rotor.toml                 ← re-saved in Sprint 03
├── sinha_rotor_pre_damping.toml     ← back-up before Sprint 03
├── signal_utils.py                  ← Sprint 01
├── plot_utils.py                    ← Sprint 01
├── run_campaign.py                  ← Sprint 02
├── build_validation_matrix.py       ← Sprint 07
├── build_validation_deck.py         ← Sprint 07
├── 00a_modal_check.ipynb            ← Sprint 00
├── 00b_damping_check.ipynb          ← Sprint 03
├── 06_hos_validation.ipynb          ← Sprint 01
├── 07_sinha_fig10_replication.ipynb ← Sprint 04
├── 08_crack_hos_650_750.ipynb       ← Sprint 05
├── 09_misalignment_hos_750_900.ipynb← Sprint 06
└── results/
    ├── campaign.h5                  ← Sprint 02 (re-written after Sprint 03)
    ├── validation_matrix.csv        ← Sprint 07
    └── figures/
        ├── sprint_04/
        ├── sprint_05/
        └── sprint_06/

reports/
├── sinha_crack_side_by_side.pdf         ← Sprint 05
├── sinha_misalignment_side_by_side.pdf  ← Sprint 06
├── sinha_fig10_side_by_side.pdf         ← Sprint 04
└── sinha_validation_figures.pdf         ← Sprint 07

01_article/
└── 03_methods_draft.md              ← Sprint 07
```

## Explicit non-goals (to protect the 5-week window)

- **No `Flex Open` / `Flex Breathing` crack models.** Mayes (matches Sinha §5 `(1 − cos θ) Δk / 2`) is the only crack model used in this programme.
- **No RK4 experimental extension** (`01_article/04_rk4_working_plan.md`) until Sprint 06 passes. That is a next-paper contribution.
- **No full DoE** (crack-depth × misalignment-level × speed × damping sweeps from `01_article/01_publication_roadmap.md §5.3`) until Sprint 07's validation matrix is scored. A broader campaign on an unvalidated pipeline is wasted compute.

## Candidate next sprint after 07

If the validation matrix scores ≥ 8/10 `pass` or `partial`, consider:

- **Sprint 08 — DoE expansion.** Crack depth ratios `{0.1, 0.2, 0.3, 0.4, 0.5}` × shared speeds `{650, 750, 900}` × misalignment levels `{small, medium, large}`. Feeds the `BPR`, `BCS`, `BE` scalar indicators from the publication roadmap §5.4.
- **Sprint 09 — RK4 experimental validation.** Activate `01_article/04_rk4_working_plan.md`.

If the validation matrix scores < 8/10, do not advance — go back and fix the failing sprints. The publishable result is a trustworthy pipeline, not a rushed DoE.
