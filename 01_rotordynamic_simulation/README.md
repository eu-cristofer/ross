# Rotordynamic Simulation — Sinha (2007) HOS Replication

> **Author:** Cristofer Antoni Souza Costa — POSMEC / UFU
> **Advisor:** Prof. Dr. Aldemir Aparecido Cavallini Junior
> **Target deliverables:** M.Sc. thesis (Feb 2026) + companion journal paper
> **Library:** [ROSS](https://github.com/petrobras/ross) (rotor) + custom HOS pipeline (this directory)

A numerical study that replicates Sinha (2007), *Higher Order Spectra for Crack
and Misalignment Identification in the Shaft of a Rotating Machine*
(*Structural Health Monitoring* 6(4), 325–334), using ROSS for the FE model
and a custom bispectrum / trispectrum estimator built from `numpy` + `scipy`.
The goal is to distinguish a breathing transverse crack from parallel
coupling misalignment using only simulated probe signals — and, in the
process, deliver the misalignment HOS signatures that Sinha could not
FE-simulate (his §5 caveat).

---

## Status at a glance

| Sprint | Title | Effort | Status | Key artefact |
|---|---|---|---|---|
| 00 | Modal FE validation against Sinha §3 / §5 | ½ day | **done** | `00a_modal_check.ipynb`, `SINHA_MODAL_TARGET` |
| 01 | HOS core library + synthetic validation | 5 d | **done** | `signal_utils.py`, `plot_utils.py`, `06_hos_validation.ipynb`, `07_hos_demo.ipynb`, `08_hos_qpc_demo_ptbr.ipynb` |
| 02 | Sinha-matched acquisition + persisted long records | 3 d | **in progress** | `run_campaign.py` (pending), `results/campaign.h5` (pending) |
| 03 | ζ₁ = 0.3 % damping + modal-truncation convergence | 2 d | not started | damping-tuned `sinha_rotor.toml`, `00b_damping_check.ipynb` |
| 04 | FE-to-FE reproduction of Sinha Figs. 9 & 10 | 3–5 d | not started | `07_sinha_fig10_replication.ipynb` |
| 05 | Crack HOS at 650 / 750 RPM (Figs. 2, 3, 5, 7) | 1 w | not started | `08_crack_hos_650_750.ipynb`, side-by-side PDF |
| 06 | Misalignment HOS at 750 / 900 RPM (Figs. 4, 6, 8) — **novel** | 1 w | not started | `09_misalignment_hos_750_900.ipynb`, side-by-side PDF |
| 07 | Validation matrix + Methods draft | 3–5 d | not started | `results/validation_matrix.csv`, `01_article/03_methods_draft.md` |

Sprint dependency graph and the 10 falsifiable Sinha claims being scored
live in [`sprints/README.md`](sprints/README.md). Live tracking — what is
being worked on this week, blockers, decisions awaiting input — is in
[`docs/PLAN.md`](docs/PLAN.md).

---

## Repository layout

```
01_rotordynamic_simulation/
├── README.md                                    ← you are here
├── CLAUDE.md                                    ← agent guardrails (project conventions)
├── constants.py                                 ← single source of truth (Sprint 01 Pattern A)
├── signal_utils.py                              ← HOS estimators (bispectrum, trispectrum, …)
├── plot_utils.py                                ← Sinha-convention visualisers
├── sinha_helpers.py                             ← shared notebook helpers
├── sinha_rotor.toml                             ← frozen geometry contract (do not retune silently)
│
├── 00_sinha_rotor.ipynb                         ← geometry build + kxx calibration → TOML
├── 00a_modal_check.ipynb                        ← Sprint 00 modal assertion
├── 01a_sinha_rotor_modal.ipynb                  ← modal analysis on the frozen rotor
├── 01b_unbalance.ipynb                          ← residual unbalance baseline
├── 02_sinha_unbalance_phase_crack.ipynb         ← crack vs. unbalance phase sweeps
├── 03_sinha_crack_model_comparison.ipynb        ← Mayes / Gasch / Open comparison
├── 04_sinha_fault_analysis.ipynb                ← integrated fault overview (legacy)
├── 06_hos_validation.ipynb                      ← Sprint 01 unit tests (positive + negative)
├── 07_hos_demo.ipynb                            ← HOS demo on a coupled-harmonic signal
├── 08_hos_qpc_demo_ptbr.ipynb                   ← QPC tutorial (Portuguese)
│
├── docs/                                        ← research-management documents
│   ├── DECISIONS.md                             ← architecture / scope decision log
│   ├── PLAN.md                                  ← active plan + sprint status board
│   └── PAPER_NOTES.md                           ← thesis & journal-paper drafting notes
│
├── sprints/                                     ← per-sprint briefs (handoff-ready)
│   ├── README.md                                ← sprint index, dependency graph, claim matrix
│   ├── 00_modal_validation.md
│   ├── 01_hos_core.md
│   ├── 02_acquisition_long_records.md
│   ├── 03_damping_and_modal_truncation.md
│   ├── 04_sinha_fe_replication.md
│   ├── 05_crack_hos_replication.md
│   ├── 06_misalignment_hos.md
│   ├── 07_validation_report.md
│   └── publication_roadmap.md                   ← the overarching thesis/paper plan
│
├── study_docs/                                  ← UML / mermaid + narrative walkthroughs
├── sinha_acquisition_and_simulation_sampling.md ← acquisition-chain technical note (Methods source)
├── sinha_targets.md                             ← expected B / T signatures per fault × speed
└── code_review.md                               ← 2026-04-24 code-review findings
```

---

## How to run

```bash
# from the repo root
pip install -e ".[dev]"

# from THIS directory (so constants.py and sinha_rotor.toml resolve)
cd 01_rotordynamic_simulation
jupyter lab
```

Notebooks must be launched with `01_rotordynamic_simulation/` as the working
directory — `from constants import *` and `rs.Rotor.load("sinha_rotor.toml")`
both depend on it.

The two-stage workflow:

```
00_sinha_rotor.ipynb  ──  builds geometry, tunes kxx so f_n1 ≈ 27.50 Hz,
                          writes  sinha_rotor.toml
                                          │
                                          ▼
   01a / 01b / 02 / 03 / 04 / 06 / 07 / 08  ──  load sinha_rotor.toml and
                                                 import constants.py
```

`sinha_rotor.toml` is the **frozen geometry contract**. If retuning is
required, regenerate it from `00_sinha_rotor.ipynb` and log the change in
[`docs/DECISIONS.md`](docs/DECISIONS.md) + the sampling note.

---

## Project conventions

- **Pint everywhere.** Speeds, unbalance, offsets are `Q_(...)` quantities;
  convert at the call site with `.to("rad/s").m` / `.to("rpm").m`.
- **Constants live in `constants.py`.** Notebooks import; they do not redefine.
  New magic numbers get a provenance paragraph in the module docstring.
- **Canonical crack depth:** `CRACK_RATIO = 0.5` (Mayes).
- **Canonical probe:** `rs.Probe(node=PROBE_NODE, angle=0.0)`.
- **Modal calibration target:** `SINHA_MODAL_TARGET = 27.50` Hz
  (Sinha §3 experiment, not §5 FE). See
  [`docs/DECISIONS.md`](docs/DECISIONS.md) D-001.
- **Language:** publication-track narrative is English. `00`'s opening
  paragraph and `08_…_ptbr.ipynb` are intentional Portuguese exceptions.
- **Narrative markdown is part of the product** — each Sinha notebook has a
  "Research recap — parameters and provenance" cell; keep it in sync when you
  edit parameters.

---

## Cross-references

| Document | What it answers |
|---|---|
| [`docs/PLAN.md`](docs/PLAN.md) | What am I working on this week? What's blocking the next sprint? |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Why is this constant / model / calibration target set the way it is? |
| [`docs/PAPER_NOTES.md`](docs/PAPER_NOTES.md) | What goes in the thesis / journal paper, and where is the evidence? |
| [`sprints/README.md`](sprints/README.md) | Step-by-step execution plan + the 10 falsifiable claims being scored |
| [`sprints/publication_roadmap.md`](sprints/publication_roadmap.md) | Overarching narrative, gap analysis, risk register |
| [`sinha_acquisition_and_simulation_sampling.md`](sinha_acquisition_and_simulation_sampling.md) | Methods-section technical note (sampling, AA filter, segmentation) |
| [`sinha_targets.md`](sinha_targets.md) | Expected B / T topology per fault × speed (acceptance criteria for Sprint 05–06) |
| [`code_review.md`](code_review.md) | 2026-04-24 audit — open and resolved findings |

---

## Reference

Sinha, J. K. (2007). Higher Order Spectra for Crack and Misalignment
Identification in the Shaft of a Rotating Machine.
*Structural Health Monitoring*, 6(4), 325–334.
