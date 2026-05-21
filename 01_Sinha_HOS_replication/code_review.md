# Code review — `01_rotordynamic_simulation/`

Scope: the five Sinha notebooks (`00`–`04`), the supporting `01_unbalance.ipynb`,
`constants.py`, and the companion markdown notes. Focus as requested:
consistency, naming conventions, and architecture patterns.

Reviewed on 2026-04-24 against the current working tree (M `constants.py`, ??
`SInha targets.md`).

---

## 1. Blocking issue — `constants.py` is importable-broken

`__all__` exports `"T"` but only `T_SHORT` and `T_LONG` are defined
(`constants.py:68` vs `constants.py:111-112`). `from constants import *` raises:

```
AttributeError: module 'constants' has no attribute 'T'
```

Verified by running the import at the repo root. Notebooks `02`, `03`, and `04`
reference bare `T` in many cells (6, 5, and 3 cells respectively) — none of
them can execute cleanly from a fresh kernel. Existing cell outputs are stale
from a prior revision where `T` still existed.

Options:

1. Reintroduce `T = T_SHORT` (or whichever window was canonical) to keep the
   notebooks working and the Methods provenance table honest.
2. Remove `"T"` from `__all__` and rewrite every bare-`T` usage to pick
   `T_SHORT` / `T_LONG` explicitly (preferable — makes the sampling-window
   choice visible at each call site).

The companion note `sinha_acquisition_and_simulation_sampling.md` also
advertises `T` in its provenance table, so it needs the same fix.

Related: `constants.py:44` claims `__all__` is "alphabetically ordered for
maintainability" but it isn't (e.g., `SPEEDS` follows `SPEED_MIS_1`, which is
only correct under a non-ASCII ordering). Either enforce sort order or drop
the comment.

---

## 2. Single-source-of-truth leaks

Sprint 01 explicitly chose **Pattern (A)**: notebooks `from constants import *`
and only override for sweeps. Several call sites silently ignore that rule:

| Notebook | Offending value | What's in `constants.py` |
|---|---|---|
| `00_sinha_rotor.ipynb` | `bearing1_node = 1`, `bearing2_node = 11`, `disk_node = 6` (cell 6) | `BEARING_1_NODE`, `BEARING_2_NODE`, `DISK_NODE` |
| `04_sinha_fault_analysis.ipynb` cell 14 | `crack_node=DISK_NODE + 1` | `CRACK_NODE` (defined as `DISK_NODE + 1`) |
| `04_sinha_fault_analysis.ipynb` cell 14 | `depth_ratio=0.5` hardcoded | `CRACK_RATIO = 0.5` |
| `04_sinha_fault_analysis.ipynb` cell 10 | `freq_x_range=(0, 200)` | `FREQ_RANGE = Q_((0, 200), "Hz")` |
| `04_sinha_fault_analysis.ipynb` cell 20 | `mis_distance_x=1.0e-3`, `mis_distance_y=0.5e-3` as function defaults | `MIS_X`, `MIS_Y` |

`00` is a special case — it *defines* the geometry that lands in
`sinha_rotor.toml`, so some literal values are intrinsic. But the node indices
are the same ones exposed in `constants.py`; importing them (or at least
asserting equality, as `04` does for the disk/bearing nodes) would prevent
future drift.

---

## 3. File/notebook naming inconsistencies

- **Numbering collision.** `01_sinha_rotor_modal.ipynb` and `01_unbalance.ipynb`
  both begin with `01_`. Pick either renumbering (`01a`/`01b`) or move
  `01_unbalance.ipynb` to a different stem — the current layout makes the
  intended reading order ambiguous.
- **`SInha targets.md`.** Capitalisation bug (`SInha` → `Sinha`) and a space in
  the filename while everything else uses `snake_case.md`. Rename to
  `sinha_targets.md`.
- **Snake vs. ALL-CAPS for node indices.** `00` uses `bearing1_node`,
  `bearing2_node` (no underscore between the word and the index); `constants.py`
  uses `BEARING_1_NODE`, `BEARING_2_NODE` (underscore before the index). Pick
  one convention and migrate — `BEARING_1_NODE` is consistent with the Sinha
  paper's `B1`/`B2` notation.

---

## 4. Import-style drift across notebooks

| Notebook | Import line | Notes |
|---|---|---|
| `00_sinha_rotor.ipynb` | no `constants` import | Defines values locally. |
| `01_sinha_rotor_modal.ipynb` | `from constants import *` | |
| `01_unbalance.ipynb` | `from constants import DISK_NODE, PROBE_NODE, UNB_MAG, UNB_PHASE` | Only explicit importer — actually the best practice, but inconsistent. |
| `02_…_phase_crack.ipynb` | `from constants import *` | |
| `03_…_model_comparison.ipynb` | `from constants import *` | Also imports `from ross.faults.crack import Crack`. |
| `04_…_fault_analysis.ipynb` | `from constants import *` (in a **separate, later cell** — cell 4, after the rotor is already loaded in cell 2) | Only notebook that doesn't import constants in the first code cell. |

Two independent issues:

1. **Glob vs. explicit.** `import *` is convenient for notebooks but makes it
   impossible to tell what a notebook depends on without running it. The
   `01_unbalance.ipynb` pattern (explicit names) documents intent and should be
   the default.
2. **Split imports in `04`.** Putting `from constants import *` in cell 4
   instead of the import cell creates a silent hazard: re-running just the
   import cell leaves `DISK_NODE` undefined. Consolidate all imports into
   cell 2.

Smaller items:

- `00` and `04` both do `from ross.materials import Material` but use
  `rs.Material(...)`, so `Material` is unused.
- The `Q_ = rs.Q_` shim is re-declared in every notebook; consider exporting
  it from `constants.py` for symmetry (it already imports `Q_`).

---

## 5. Duplicated helper logic that should live in a module

`get_harmonic_amplitude(yout, dof, t, target_freq_hz)` is defined verbatim in
both `02_sinha_unbalance_phase_crack.ipynb` (cell 16) and
`03_sinha_crack_model_comparison.ipynb` (cell 12). The only difference is the
surrounding comment.

`04_sinha_fault_analysis.ipynb` defines several more helpers inline that have
the same analytical scope as the other notebooks:

- `run_healthy_baseline(...)` (cell 7)
- `annotate_harmonics(fig, speed, n_max=4)` (cell 9)
- `plot_all_conditions(...)` (cell 10)
- `run_crack_case(...)` (cell 13)
- `simulate_misalignment(...)` (cell 20)

Proposal: add a small `sinha_helpers.py` (or `analysis.py`) next to
`constants.py` containing at minimum `get_harmonic_amplitude`,
`annotate_harmonics`, and the FFT-of-steady-state boilerplate that is
copy-pasted into every notebook. This keeps the notebooks narrative-focused
and avoids stale copies drifting apart.

The plotly discrete colour list
`["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", ...]` is likewise reproduced in
`02` and `03`; move it to the helper module as `PHASE_COLORS` (or just use
`plotly.colors.qualitative.Plotly`).

---

## 6. Architecture / pattern consistency

**What works well.**

- `Rotor.save()` → `sinha_rotor.toml` → `Rotor.load()` cleanly separates the
  geometry-calibration notebook (`00`) from the analysis notebooks
  (`01`–`04`). That is the right pattern and should be preserved.
- `constants.py` docstring (lines 1–38) is unusually thorough, documenting
  each symbol's provenance. This pattern should be copied into the helper
  module when it is created.
- `04` asserting `rotor.disk_elements[0].n == DISK_NODE` (cell 4) is the right
  defensive check — propagate it to the other analysis notebooks so anyone
  editing the TOML gets a clear failure.

**What's inconsistent.**

- Function-level refactor is uneven. `04` is the only notebook that wraps
  simulations in named functions; `02` and `03` inline the same loops over
  `SPEEDS`. Pick one model (narrative-inline vs. function-per-case) and apply
  it uniformly.
- Docstrings are NumPy-style where they appear but drift from the signature.
  Example: `run_healthy_baseline` in `04` cell 7 documents a `speed_crack_0`
  parameter that the function does not take (it takes `speed_crack`). Run the
  suite through `pydocstyle` or `ruff` (pydocstyle rules) after the refactor.
- `02` cell 12 has a leading `# TODO / Check this DFFT implementation…`
  comment that was never resolved. Either answer the question in the note and
  drop the TODO, or delete the cell.
- `02` cell 17 is an empty code cell — remove.

---

## 7. Narrative / language consistency

- `00_sinha_rotor.ipynb` opens in Portuguese (cell 0 header paragraph);
  notebooks `01`–`04` are entirely in English. Pick one language for the
  publication-track narrative and translate the odd one out. The thesis
  Methods section will not want to mix.
- `sinha_acquisition_and_simulation_sampling.md` still says "Notebook `04`
  previously used `3π/4` inline" — true at the time, but now that Sprint 01
  has landed, the phrasing should be past-tense-only or the note should just
  document the canonical value and drop the historical parenthetical.

---

## 8. Prioritised fix list

1. **P0 — Fix `constants.T`.** Broken `__all__` export; blocks clean re-runs.
2. **P0 — Rename `SInha targets.md` → `sinha_targets.md`.** The typo'd name is
   annoying to tab-complete and will confuse future contributors.
3. **P1 — Reconcile `04` with `constants.py`** (`CRACK_NODE`, `CRACK_RATIO`,
   `FREQ_RANGE`, `MIS_X`/`MIS_Y`). One grep pass.
4. **P1 — Consolidate `04`'s `from constants import *`** into the first import
   cell.
5. **P1 — Extract shared helpers** (`get_harmonic_amplitude`,
   `annotate_harmonics`, FFT-of-steady-state snippet, colour list) into a
   `sinha_helpers.py` module.
6. **P2 — Standardise on explicit imports** (`from constants import NAME1,
   NAME2, …`) following `01_unbalance.ipynb`'s style.
7. **P2 — Resolve numbering collision** between the two `01_*.ipynb` files.
8. **P2 — Drop unused `Material` imports** and redundant `Q_ = rs.Q_` shims;
   expose `Q_` from `constants.py` if the shim is wanted.
9. **P3 — Fix docstring drift** in `04` helpers; add TOML-vs-constants
   assertions to `01`–`03`; resolve the `# TODO` and the empty cell in `02`;
   translate the `00` preamble.
10. **P3 — Alphabetise `__all__`** (or delete the misleading comment).

None of the P0 / P1 items require rethinking the simulation workflow — they
are tidy-up passes that restore the "single source of truth" invariant
promised by the Sprint 01 plan.
