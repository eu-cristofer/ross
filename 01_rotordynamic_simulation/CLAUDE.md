# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is a project-specific CLAUDE.md. The repo-root file at
[`../CLAUDE.md`](../CLAUDE.md) documents the ROSS library itself
(how to use `rs.Rotor`, analysis methods, unit conventions, element pattern,
lint/test commands). Read it first for library-level questions — do not
duplicate its content here.

## What this directory is

A numerical-simulation study replicating the Sinha (2007) rotor fault-diagnosis
experiments using ROSS, feeding an M.Sc. thesis (author: Cristofer Antoni Souza
Costa, POSMEC/UFU) and a companion paper on **higher-order spectra (HOS) for
fault diagnosis** — see `sprints/01_publication_roadmap.md`. The deliverable is
a bispectrum / trispectrum analysis pipeline that distinguishes a breathing
transverse crack from parallel coupling misalignment using only simulated
probe signals.

Notebooks are both the research artefact and the thesis figure source, so
their narrative markdown is part of the product — do not delete or
aggressively refactor it.

## The two-stage workflow

```
00_sinha_rotor.ipynb  ── builds geometry, tunes kxx to f_n1 ≈ 27.50 Hz,
                         writes  sinha_rotor.toml
                                      │
                                      ▼
01a_sinha_rotor_modal.ipynb  ┐
01b_unbalance.ipynb          │   all load sinha_rotor.toml via
02_sinha_unbalance_phase_crack.ipynb   rs.Rotor.load(...) and import
03_sinha_crack_model_comparison.ipynb  shared parameters from constants.py
04_sinha_fault_analysis.ipynb ┘
```

`sinha_rotor.toml` is the **frozen geometry contract**. Do not silently retune
bearing stiffness or node positions — downstream notebooks and the published
Methods table depend on it. If retuning is required, update
`00_sinha_rotor.ipynb`, re-save, and record the change in
`sinha_acquisition_and_simulation_sampling.md`.

## `constants.py` — single source of truth (Sprint 01, Pattern A)

All simulation parameters used across the Sinha replication path live in
[`constants.py`](constants.py). The Sprint 01 rule is: notebooks do
`from constants import *` (or explicit names) and only override values when
running a sweep. New magic numbers do **not** go inline in a notebook — add
them to `constants.py` with a provenance note in the module docstring and in
[`sinha_acquisition_and_simulation_sampling.md`](sinha_acquisition_and_simulation_sampling.md).

Key symbols (see the docstring at the top of `constants.py` for the full
provenance table):

- Geometry: `BEARING_1_NODE`, `BEARING_2_NODE`, `DISK_NODE`, `CRACK_NODE`, `PROBE_NODE`
- Unbalance: `UNB_MAG = Q_(2e-4, "kg*m")`, `UNB_PHASE = Q_(4π/3, "rad")` (canonical — `04` previously used `3π/4` inline; that is superseded)
- Speeds: `SPEED_CRACK_0/1` (650, 750 rpm), `SPEED_MIS_0/1` (750, 900 rpm), `SPEEDS` alias
- Time / sampling: `DT = 1/SINHA_FS_HZ`, `T_SHORT`, `T_LONG`, `FS_SIM_HZ`
- HOS handoff (Sprint 02+): `SINHA_FS_HZ = 2560`, `SINHA_AA_CUTOFF_HZ = 1000`, `SINHA_HOS_DF_HZ = 1.25`, `SINHA_HOS_N_SEGMENTS = 50`, `SINHA_HOS_OVERLAP = 0.5`

Sampling convention: the FEM integrates at `DT` (stability/cost-driven); for
Sinha-comparable HOS, probe time series are **resampled to `SINHA_FS_HZ` and
low-pass filtered at `SINHA_AA_CUTOFF_HZ` in post-processing** — see the
technical note. Do not change `DT` to 1/2560 without updating the note.

### Current known issue

`constants.__all__` lists `"T"` but only `T_SHORT` and `T_LONG` are defined —
`from constants import *` raises `AttributeError`. Notebooks `02`/`03`/`04`
reference bare `T`; their cell outputs are stale from a prior revision. See
`code_review.md` §1 for details and options. Fix before re-running any
analysis notebook from a clean kernel.

## Running the notebooks

Install ROSS from the repo root (editable install, per the root CLAUDE.md):

```bash
pip install -e "..[dev]"   # from this directory; or `pip install -e ".[dev]"` from the repo root
jupyter lab                # from this directory so `import constants` resolves
```

Notebooks must be launched with `01_rotordynamic_simulation/` as the working
directory so that `from constants import *` and
`rs.Rotor.load("sinha_rotor.toml")` find their files.

## Sprints and docs layout

- `sprints/01_publication_roadmap.md` — overarching thesis/paper plan; the
  source of truth for what each sprint must deliver. Read this to understand
  *why* a given change is in scope.
- `sprints/sprint-NN-*.md` — per-sprint briefs. Sprint 01 established
  `constants.py` + the sampling technical note; Sprint 02+ lands the HOS code.
- `sinha_acquisition_and_simulation_sampling.md` — how simulated signals are
  made comparable to Sinha's 2560 Hz / 1 kHz acquisition chain. Cite this in
  the thesis Methods section.
- `sinha_targets.md` — expected bispectrum/trispectrum signatures per
  fault/speed case; the acceptance criteria for the HOS code.
- `study_docs/sinha_fault_analysis/` — UML / mermaid diagrams and a narrative
  walkthrough of the fault-analysis flow.

## Conventions specific to this project

- **Pint everywhere.** Speeds, unbalance, offsets are `Q_(...)` quantities in
  `constants.py`; convert with `.to("rad/s").m` / `.to("rpm").m` at the call
  site. Do not introduce raw floats that shadow a `Q_` constant.
- **Canonical Mayes/Gasch crack depth** is `CRACK_RATIO = 0.5`. `03` sweeps
  additional depths locally; other notebooks should use the constant.
- **Probe**: always `rs.Probe(node=PROBE_NODE, angle=0.0)` unless a sweep
  requires otherwise.
- **Language**: publication-track narrative is English. `00`'s opening
  paragraph is historical Portuguese — prefer English for new text.
- **Narrative markdown is load-bearing.** Each Sinha notebook has a
  "Research recap — parameters and provenance" cell pointing at
  `constants.py` vs. notebook-local overrides; keep this in sync when editing
  parameters.
