# Sprint 01 — Foundation and Sinha acquisition parity

**Role:** You are an AI coding agent working in the repository. You implement repository hygiene and a **single source of truth** for simulation parameters, and you document how numerical signals will be made comparable to Sinha (2007) before any bispectrum code lands.

**References (read before coding):**

- [sprints/01_publication_roadmap.md](../01_publication_roadmap.md) — Phase 2 checklist gaps (parameter documentation), Phase 3–4 HOS prerequisites.
- Sinha (2007), Section 3: sampling **2560 samples/s**, anti-aliasing **1 kHz**; Section 3.3: HOS segment settings (for Sprint 02, but you must capture them in docs/constants).

**Scope — IN:**

- Consolidate duplicated configuration between [`constants.py`](../constants.py) and inline definitions in [`04_sinha_fault_analysis.ipynb`](../04_sinha_fault_analysis.ipynb) (e.g. `UNB_PHASE`, speeds, `DT`, `T`, misalignment offsets, `CRACK_RATIO`).
- **Pattern (A) — chosen:** all notebooks `from constants import *` and only override in notebooks when running sweeps. No separate `config.py`; [`constants.py`](../constants.py) is the single source of truth for the Sinha replication path (`00`, `01`, `02`, `03`, `04`).
- Add a short markdown **technical note** (single file under `01_rotordynamic_simulation/`) that lists:
  - Sinha acquisition: `fs`, AA filter, probe directions and bearing-2 location (from paper).
  - Your simulation: current `DT` and implied `fs_sim = 1/DT`; explicit statement whether you will **resample** simulated signals to 2560 Hz and/or **low-pass** at 1 kHz before HOS (recommend a default choice and justify in one paragraph).
- Ensure `sinha_rotor.toml` remains the canonical frozen geometry unless the user explicitly asked to retune; do not silently change bearing/stiffness values in this sprint.

**Scope — OUT:**

- Bispectrum/trispectrum implementation (Sprint 02+).
- Large parametric campaigns (Sprint 06).

**Deliverables:**

1. Refactored constants / config with **no contradictory** `UNB_PHASE` between [`constants.py`](../constants.py) and [`04_sinha_fault_analysis.ipynb`](../04_sinha_fault_analysis.ipynb).
2. Technical note [`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md) — Sinha vs simulation sampling tables, default HOS chain, **parameter provenance** table, Sprint 01 changelog.
3. Brief changelog (also embedded in that note): bullet list of what moved where.
4. **Research recap** markdown cell in each Sinha notebook (`00`–`04`) pointing to `constants.py` vs notebook-local parameters for thesis writing.

**Acceptance criteria:**

- [ ] `grep` or equivalent shows one canonical definition for `UNB_MAG`, `UNB_PHASE`, `SPEEDS` (or clearly named `SPEED_CRACK_*`, `SPEED_MIS_*`), `DT`, `T`, `MIS_X`/`MIS_Y`, `CRACK_RATIO` used by the Sinha notebooks.
- [ ] Running the first code cells of `00`, `01`, and `04` (user’s environment) does not require editing duplicated magic numbers in the notebook body for the default case.
- [ ] Technical note explicitly states target **HOS analysis sampling chain** for Sprints 02–03 (2560 Hz and/or filtering).

**Constraints:**

- Minimal diffs outside [`01_rotordynamic_simulation/`](../) and the one technical note path you add.
- Do not delete notebook narrative markdown; only adjust configuration cells and imports as needed.

**Verification (agent runs):**

- `python -c "import ast; ast.parse(open('01_rotordynamic_simulation/constants.py').read())"` (from repo root; or load notebooks in dry run if your environment supports it).

**Handoff to Sprint 02:** Constants module exposes `SINHA_FS_HZ = 2560`, `SINHA_AA_CUTOFF_HZ = 1000`, `SINHA_HOS_DF_HZ = 1.25`, `SINHA_HOS_N_SEGMENTS = 50`, `SINHA_HOS_OVERLAP = 0.5` (or similar names) for the HOS module to import.
