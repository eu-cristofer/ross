# Paper Notes — Thesis & Journal-Paper Drafting

Working notebook for the M.Sc. thesis (POSMEC / UFU, defence February 2026)
and the companion journal paper. Captures what *will go where*, where the
evidence already lives, and what still needs to be written or generated.

Not a draft of the paper itself — that lives in `01_article/` (when the
sprints reach Sprint 07). This is the **planning layer** on top of that
draft.

---

## 1. Outlets

| Outlet | Target venue | Length | Status | Notes |
|---|---|---|---|---|
| M.Sc. thesis | POSMEC / UFU | ~120 pp | drafting (Methods only) | Defence Feb 2026. Advisor: Prof. Dr. Aldemir Aparecido Cavallini Junior. |
| Journal paper | candidates: *MSSP*, *JSV*, *SHM*, *Eng. Failure Analysis* | 8–12 pp | not started | Submit within 2 months of thesis defence. *MSSP* preferred — Sinha's own venue is *SHM*; targeting *MSSP* signals an engineering-systems framing. |

Decision on the venue itself is deferred until Sprint 07 — the validation
matrix's score (`pass` / `partial` count out of 10) will drive the choice
between an SHM-style replication paper and a stronger MSSP-style
contribution paper.

---

## 2. Working title

> **Numerical Bispectrum / Trispectrum Diagnosis of Cracked and Misaligned
> Shafts using Finite-Element Simulations: Validation Against Sinha (2007)
> and Extension to Coupling Misalignment**

The *and Extension* clause is the load-bearing novelty signal — it tells a
reviewer the paper does more than replicate. Tied to
[D-008](DECISIONS.md#d-008).

---

## 3. The contribution (one-sentence elevator)

> *We show that a fully open-source ROSS-based FE pipeline reproduces every
> bispectral / trispectral fault signature reported experimentally by Sinha
> (2007) for a breathing transverse crack, and we extend the result to
> parallel coupling misalignment — a case Sinha could not FE-simulate.*

If a reviewer reads only one sentence of the abstract, it must be this one.

---

## 4. Paper skeleton — current planning

Mapping each section to the sprint that produces its evidence.

| § | Section | Length (≈) | Evidence source | Status |
|---|---|---|---|---|
| 1 | Introduction & motivation | 1 pp | [`sprints/publication_roadmap.md`](../sprints/publication_roadmap.md) §1 | outline only |
| 2 | Background: HOS for rotor faults | 1 pp | Sinha (2007); Kim & Powers (1979); Collis et al. (1998) | citations gathered, prose pending |
| 3 | Rotor model + Sinha geometry | 1 pp | `00_sinha_rotor.ipynb` + [`sinha_rotor.toml`](../sinha_rotor.toml) | figures ready; Methods table pending |
| 4 | Acquisition & HOS estimator | 1.5 pp | [`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md), `signal_utils.py` docstring | technical note done; needs to be condensed |
| 5 | Validation against Sinha §3 experiments (crack) | 2 pp | Sprint 05 outputs | not started |
| 6 | Misalignment HOS (novel) | 2 pp | Sprint 06 outputs | not started |
| 7 | Discussion: speed dependence, B22 / T222 as discriminators | 1 pp | [`sinha_targets.md`](../sinha_targets.md) + Sprint 07 matrix | not started |
| 8 | Conclusion + open-source artefact pointer | 0.5 pp | this repository | not started |

Hard cap: 12 pp single-column or 8 pp double-column. Cut from §1–2 first if
needed; §5–7 are not negotiable.

---

## 5. Figures planned (camera-ready)

Each figure must have a (notebook → PNG) provenance trail recorded here so
the thesis can cite the exact cell that produced it.

| Fig | What | Source notebook | Sinha analogue |
|---|---|---|---|
| 1 | Sinha rotor diagram + node indices | `00_sinha_rotor.ipynb` (rotor.plot) | Sinha Fig. 1 |
| 2 | Campbell diagram, intact + cracked (open) | `01a_sinha_rotor_modal.ipynb` | — (our context-setting figure) |
| 3 | Probe amplitude spectra at 650 / 750 RPM, cracked vs. healthy | Sprint 05 (`08_crack_hos_650_750.ipynb`) | Sinha Fig. 2 |
| 4 | Probe orbits at 650 / 750 RPM, cracked vs. healthy | Sprint 05 | Sinha Fig. 3 |
| 5 | Probe amplitude spectra at 750 / 900 RPM, misaligned | Sprint 06 (`09_misalignment_hos_750_900.ipynb`) | Sinha Fig. 4 |
| 6 | Bispectrum surfaces — crack at 650 / 750 RPM | Sprint 05 | Sinha Fig. 5 |
| 7 | Bispectrum surfaces — misalignment at 750 / 900 RPM | Sprint 06 | Sinha Fig. 6 |
| 8 | Trispectrum ball plots — crack at 650 / 750 RPM | Sprint 05 | Sinha Fig. 7 |
| 9 | Trispectrum ball plots — misalignment at 750 / 900 RPM | Sprint 06 | Sinha Fig. 8 |
| 10 | FE-to-FE reproduction at 772.5 RPM | Sprint 04 (`07_sinha_fig10_replication.ipynb`) | Sinha Fig. 10 |
| 11 | Validation matrix heat-map (10 claims × pass/fail) | Sprint 07 (`build_validation_matrix.py`) | — (novel) |

PDF binders for side-by-side comparison: `reports/sinha_crack_side_by_side.pdf`
(Sprint 05) and `reports/sinha_misalignment_side_by_side.pdf` (Sprint 06).
These are the "open these two and the case is made" artefacts for the
defence.

---

## 6. Tables planned

| Tbl | Content | Source |
|---|---|---|
| 1 | Rotor geometry parameters (length, OD, ID, material, bearings) | `00_sinha_rotor.ipynb` + `sinha_rotor.toml` |
| 2 | Acquisition & HOS estimator settings (fs, AA, Nfft, K, Δf) | [`sinha_acquisition_and_simulation_sampling.md`](../sinha_acquisition_and_simulation_sampling.md) |
| 3 | Modal target table (Sinha §3 vs. §5 vs. ROSS) | [`sprints/00_modal_validation.md`](../sprints/00_modal_validation.md) |
| 4 | Expected B / T topology per fault × speed | [`sinha_targets.md`](../sinha_targets.md) |
| 5 | Validation matrix (10 claims, pass/fail/partial) | Sprint 07 |

---

## 7. References — collection status

Targets from `publication_roadmap.md` §4.2: 25–40 refs total.

| Category | Target | Collected | Gap |
|---|---|---|---|
| Rotordynamics fundamentals (FEM, bearings, Campbell) | 4–6 | 1 (Timbo / ROSS) | gather 3–5 |
| Crack breathing models (Mayes-Davies, harmonic balance) | 3–5 | 1 (Mayes) | gather 2–4 |
| Misalignment modelling (Xia 2019 coupling) | 2–3 | 1 (Xia 2019) | gather 1–2 |
| HOS theory (Kim-Powers, Collis, Nikias) | 3–4 | 2 (Kim-Powers, Collis) | gather Nikias textbook + one survey |
| HOS in rotating machinery | 4–6 | 1 (Sinha 2007) | gather 3–5 — search SHM / MSSP 2008–2025 |
| Fault diagnosis comparison (EMD, wavelet, ML) | 3–5 | 0 | gather 3–5 |
| Numerical fault-diagnosis FEM studies | 3–5 | 0 | gather 3–5 |
| ROSS / open-source rotordynamics | 2–3 | 1 (Timbo 2020) | gather 1–2 |
| **Total** | **25–40** | **~7** | **~20** |

**Action.** Block 2 hours after Sprint 02 lands to do the literature search
for the four most under-collected rows (HOS in rotating machinery + fault
diagnosis comparison are the highest priority — reviewers will check both).

---

## 8. Open writing questions

1. **How much of Sinha's algebra to restate?** The bispectrum / trispectrum
   definitions in `signal_utils.py` docstring already cite Eqs. 2–3 of
   Sinha. The paper should restate them briefly (1–2 lines each) so it is
   self-contained, but not re-derive Kim–Powers normalisation.
2. **Where to put the open-source pointer?** Probably a footnote on the
   first page (*"Code and data: github.com/cristofer/ross — branch
   `claude`"*) plus a Data Availability statement at the end. Confirm with
   the journal's guidelines once a venue is chosen.
3. **Portuguese ↔ English split.** Thesis Methods chapter in English (per
   project convention); thesis intro + conclusion in Portuguese per POSMEC
   norms. Confirm with advisor.
4. **Attribution of the ROSS-misalignment model.** The Xia et al. (2019)
   flex-coupling formulation is implemented inside ROSS; cite *both* the
   ROSS paper (Timbo 2020) for the implementation and the original
   formulation (Xia 2019). Do not let the citation collapse to just one.

---

## 9. Drafts and external pointers

Once Sprint 07 lands, drafts live in `01_article/` (will be created then):

- `01_article/01_publication_roadmap.md` — the original long-form roadmap
- `01_article/03_methods_draft.md` — Sprint 07 deliverable (Methods section)
- `01_article/manuscript.tex` — main draft (post-Sprint 07)

External pointers:

- Sinha (2007) PDF: `99_references/Sinha - 2007 - …pdf`
- Thesis template (POSMEC): *to be added*
- Reference manager (Zotero collection): *to be added*

---

## 10. Defence-prep notes (for later)

Empty for now. Populate from Sprint 07 onward with: 10-minute talk outline,
anticipated examiner questions, list of "what would I change if I had
another six months" reflections (always asked).
