# Decision Log — Rotordynamic Simulation

Lightweight Architecture Decision Records (ADRs) for this research project.
Each entry captures **a decision that future-me (or a reviewer) might
otherwise question**: why this calibration target, why this constant, why
this scope cut.

**Format.** One entry per decision. Date in ISO-8601. Status is one of
`accepted` / `superseded` / `proposed`. Keep the *Why* short — a reviewer
should be able to read a single entry in under a minute. Link to evidence
(notebook cell, sprint file, code review §) rather than restating it.

When a decision is reversed, mark the original `superseded` (link to the new
entry) — do not delete it.

---

## D-001 — Calibrate against Sinha §3 experimental f₁ = 27.50 Hz, not §5 FE 26.53 Hz

- **Date:** 2026-04-23
- **Status:** accepted
- **Owner:** Cristofer
- **Sprints affected:** 00, 03, 04, 05, 06, 07

**Decision.** `00_sinha_rotor.ipynb` tunes the bearing stiffness `kxx` via
`brentq` so that the *intact* first bending frequency matches Sinha's
**experimental impulse-response result (§3, Ewins)**: `f₁ = 27.50 Hz` with
tolerance `± 0.05 Hz`. Sinha's own FE (§5) reports `26.53 Hz`; that is **not**
the calibration target. Cracked, fully-open vertical target is `26.25 Hz`
(Sinha §3).

**Why.** Sinha's §5 FE is a coarser 2-node Euler–Bernoulli model and is itself
a downstream approximation of the rig. Calibrating to the rig directly makes
every HOS feature comparable to Sinha's *experimental* Figs. 2–8 — the
primary validation target. Sinha's Fig. 10 (FE-to-FE) is matched qualitatively
on topology, not on Hz numbers (Sprint 04).

**Evidence.** [`sprints/00_modal_validation.md`](../sprints/00_modal_validation.md);
`constants.SINHA_MODAL_TARGET = 27.50`;
[`00a_modal_check.ipynb`](../00a_modal_check.ipynb) cell A assertion.

---

## D-002 — `constants.py` is the single source of truth (Sprint 01 Pattern A)

- **Date:** 2026-04-23
- **Status:** accepted
- **Owner:** Cristofer
- **Sprints affected:** all

**Decision.** All simulation parameters used across the Sinha replication
path live in [`constants.py`](../constants.py). Notebooks do
`from constants import …` (explicit names preferred over `import *`) and
only override a value when running a sweep. New magic numbers are added
**with a provenance paragraph** to the module docstring and the sampling
note — never inline in a notebook.

**Why.** Earlier revisions duplicated `UNB_PHASE` inline as `3π/4` in
notebook `04` while the rest of the codebase used `4π/3`. Cross-notebook
comparison silently broke. Pattern A makes parameter drift impossible to
hide.

**Evidence.** [`sprints/01_hos_core.md`](../sprints/01_hos_core.md);
[`code_review.md`](../code_review.md) §2 (single-source-of-truth leaks);
`constants.py` module docstring (provenance table).

**Known leaks still to fix.** `code_review.md` §2 lists `04_…fault_analysis`
overrides (`crack_node`, `depth_ratio`, `freq_x_range`, `mis_distance_x/y`)
that should resolve to constants. Tracked in [`PLAN.md`](PLAN.md).

---

## D-003 — Mayes breathing crack is the **only** crack model used in the validation programme

- **Date:** 2026-04-23
- **Status:** accepted
- **Owner:** Cristofer
- **Sprints affected:** 04, 05, 07

**Decision.** Sprints 04–07 use ROSS's Mayes crack model (`crack_model="Mayes"`)
exclusively. The `Flex Open` and `Flex Breathing` variants are **out of
scope** for the publication. `03_sinha_crack_model_comparison.ipynb` keeps
side-by-side model comparison as a methodological appendix only.

**Why.** Sinha §5 specifies `(1 − cos θ) Δk / 2` — that is Mayes exactly.
Adding alternative models multiplies the validation matrix without changing
the Sinha-comparability claim, and risks pushing the 5-week sprint window.

**Evidence.** [`sprints/README.md`](../sprints/README.md) "Explicit
non-goals"; `constants.CRACK_RATIO = 0.5`.

---

## D-004 — Integrate at Sinha's acquisition rate (`DT = 1 / SINHA_FS_HZ = 1/2560 s`) for Sprints 00–01

- **Date:** 2026-04-23
- **Status:** accepted (revisit at Sprint 02 — see D-005)
- **Owner:** Cristofer
- **Sprints affected:** 00, 01

**Decision.** The FEM time step `DT = 1 / SINHA_FS_HZ ≈ 3.906 × 10⁻⁴ s`.
The simulated rate `FS_SIM_HZ = SINHA_FS_HZ = 2560 Hz`, so probe time series
already live on Sinha's experimental sampling grid — no post-process
resampling is needed for `01a` / `01b` / `02` / `03` / `04`.

**Why.** Keeps the existing short-window notebooks honest about their
sampling, removes a class of resampling bugs, and matches Sinha §3
directly.

**Evidence.** [`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md);
`constants.py:124-128`.

---

## D-005 — Sprint 02 will integrate at `dt = 1/10 000 s`, then LP @ 1 kHz, then downsample (Sinha §5 verbatim)

- **Date:** 2026-04-23
- **Status:** proposed (Sprint 02 not yet executed)
- **Owner:** Cristofer
- **Sprints affected:** 02, 04, 05, 06

**Decision.** For long records consumed by HOS (`T_LONG`-class runs), follow
Sinha §5 exactly: Newmark-β integration at `dt = 1/10 000 s`, low-pass at
1 kHz, then downsample to the target rate (`1000 Hz` for Fig. 10 replication
in Sprint 04; `2560 Hz` to match the experimental DAQ in Sprints 05/06).
Inject AWGN to achieve `SNR_DB = 40`.

**Why.** Bispectral amplitudes at B22 / T222 are sensitive to numerical
integration error. Matching Sinha's protocol verbatim removes that as a
confounder when scoring claims 5 / 7 in Sprint 07.

**How to apply.** New constants `DT_SIM = 1/10_000`, `FS_SIM_NEWMARK = 10_000`,
`FS_ACQ_FE = 1000`, `SNR_DB = 40` to be added to `constants.py` in Sprint 02.
This **supersedes D-004's `DT` definition for long records only**; the
short-record `DT = 1/2560` remains valid for `01a`–`04` orbits and phase
sweeps.

**Evidence.** [`sprints/02_acquisition_long_records.md`](../sprints/02_acquisition_long_records.md);
[`sprints/04_sinha_fe_replication.md`](../sprints/04_sinha_fe_replication.md)
"Sinha §5 recipe, verbatim" table.

---

## D-006 — Canonical residual unbalance is `UNB_MAG = 2 × 10⁻⁴ kg·m`, `UNB_PHASE = 4π/3 rad`

- **Date:** 2026-04-23
- **Status:** accepted (supersedes inline `3π/4` in `04`)
- **Owner:** Cristofer
- **Sprints affected:** 01, 02, 03, 04, 05, 06

**Decision.** All Sinha-replication notebooks use
`UNB_MAG = Q_(2e-4, "kg*m")` at `DISK_NODE` with phase
`UNB_PHASE = Q_(4π/3, "rad")`. Notebook `04` previously used `3π/4` rad
inline; that local choice is **superseded**.

**Why.** Sinha §5 specifies only "small unbalance at the disk" without a
magnitude. Picking one canonical value lets every notebook compare apples
to apples; the magnitude itself is reported in the thesis Methods section
as a chosen parameter, not a Sinha value.

**Evidence.** `constants.py:96-97`;
[`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md)
"Parameter provenance" table.

**If we change it.** Re-run every figure that depends on residual unbalance
amplitude (orbits, phase sweeps, every HOS amplitude). Cite the change here
with a new D-NNN entry and link from `UNB_MAG`'s docstring.

---

## D-007 — Sprint scope freeze: no DoE expansion or RK4 experimental validation until Sprint 07 passes

- **Date:** 2026-04-23
- **Status:** accepted
- **Owner:** Cristofer

**Decision.** The full Design-of-Experiments expansion
(crack depth × misalignment level × speed × damping) from
`publication_roadmap.md` §5.3 is **deferred** until Sprint 07's validation
matrix scores `≥ 8/10` `pass`/`partial`. The RK4 experimental extension
(`01_article/04_rk4_working_plan.md`) is deferred unconditionally — it is
next-paper material.

**Why.** A broader campaign on an unvalidated pipeline is wasted compute,
and stretches the 5-week sprint window into something that will not finish
before the February 2026 thesis deadline.

**Evidence.** [`sprints/README.md`](../sprints/README.md) "Explicit non-goals".

---

## D-008 — Misalignment HOS replication is the **novel contribution** vs. Sinha (2007)

- **Date:** 2026-04-23
- **Status:** accepted
- **Owner:** Cristofer
- **Sprints affected:** 06, 07

**Decision.** Sprint 06 reproduces Sinha Figs. 4, 6, 8 (misalignment HOS at
750 / 900 RPM) using ROSS's `run_misalignment` (Xia et al. 2019 flex-coupling
model). Sinha §5 *explicitly states* he could not FE-simulate misalignment
("the force function due to the shaft misalignment is not well stood").
Claims 6 and 8 in the validation matrix therefore constitute the thesis'
contribution beyond the paper, and must be highlighted as such in
[`PAPER_NOTES.md`](PAPER_NOTES.md) and the journal abstract.

**Why.** Reviewers will ask: "what's new vs. Sinha 2007?" The misalignment
HOS-via-FE result is the cleanest, defensible answer.

**Evidence.** [`sprints/README.md`](../sprints/README.md) "Novel contribution";
[`sprints/06_misalignment_hos.md`](../sprints/06_misalignment_hos.md).

---

## D-009 — `sinha_rotor.toml` is the frozen geometry contract

- **Date:** 2026-04-23
- **Status:** accepted
- **Owner:** Cristofer

**Decision.** Every analysis notebook (`01a`–`08`) loads geometry via
`rs.Rotor.load("sinha_rotor.toml")` rather than rebuilding it inline. The
TOML is regenerated *only* from `00_sinha_rotor.ipynb`; node positions and
bearing stiffness do not get silently retuned downstream. Sprint 03 will
re-save the file with damping; the previous copy is preserved as
`sinha_rotor_pre_damping.toml`.

**Why.** Cross-notebook reproducibility and the Methods-section provenance
table depend on a single canonical geometry. The four Sinha node indices
(`BEARING_1_NODE=1`, `BEARING_2_NODE=11`, `DISK_NODE=6`,
`CRACK_NODE=DISK_NODE+1=7`, `PROBE_NODE=BEARING_2_NODE-1=10`) are baked into
the TOML; constants.py mirrors them so notebook code reads symbolically.

**Evidence.** `constants.py:88-93`;
[`CLAUDE.md`](../CLAUDE.md) "The two-stage workflow".

---

## Template for new entries

```markdown
## D-NNN — <one-line decision>

- **Date:** YYYY-MM-DD
- **Status:** accepted / superseded / proposed
- **Owner:** <name>
- **Sprints affected:** <list>

**Decision.** <what>

**Why.** <reason — the one a reviewer would ask>

**Evidence.** <link to notebook cell / sprint file / code-review § / commit>

**If we change it.** <what would need to be re-run; who needs to know>
```
