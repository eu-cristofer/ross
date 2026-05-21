# Sprint 07 — Validation report + Methods draft

> **Effort:** 3–5 days.
> **Blocks:** nothing (final sprint).
> **Unblocked by:** Sprints 00–06.
> **Artefacts produced:** `01_rotordynamic_simulation/results/validation_matrix.csv`, `reports/sinha_validation_figures.pdf`, `01_article/03_methods_draft.md`.

## Why this sprint exists

Sprints 00–06 produce evidence; Sprint 07 **scores** it. A reviewer trained in engineering research does not want to read six notebooks — they want a single table of falsifiable claims with a pass/fail/partial decision next to each, plus one publication-ready Methods section that can be cited. This sprint delivers exactly that.

The validation matrix is the artefact a thesis advisor or a journal reviewer can read in five minutes. Making it explicit (including failures) buys more credibility than quietly dropping whichever sprint didn't converge.

## Prerequisites

- Sprints 00–06 complete, including all Execution Log tables.
- `campaign.h5`, all `results/figures/sprint_NN/*.png`, and all sprint-level side-by-side PDFs exist.

## Work items

### 1. Build `01_rotordynamic_simulation/results/validation_matrix.csv`

10 rows, one per claim. Columns:

| Column | Meaning |
|---|---|
| `claim_id` | 1–10 (matches the table in the plan's Context section) |
| `description` | one-line paraphrase of the Sinha claim |
| `sinha_source` | Sinha figure / section |
| `exit_criterion` | the numeric test, copied verbatim from the sprint it came from |
| `measured_value` | scalar or short string (e.g., `"B22/B11: 650→0.08; 750→0.41"`) |
| `status` | `pass` / `fail` / `partial` / `not_tested` |
| `sprint_id` | e.g., `05`, `06` |
| `notes` | free text — include any model-form caveats |

Script it:

```python
# 01_rotordynamic_simulation/build_validation_matrix.py
import csv
from pathlib import Path

ROWS = [
    dict(claim_id=1,
         description="Intact rotor f1 ≈ 27.50 Hz (exp); fully-open cracked f1 ≈ 26.25 Hz",
         sinha_source="§3, §5",
         exit_criterion="|f1 − 27.50| ≤ 0.05 Hz; |f1(cracked, open) − 26.25| ≤ 0.30 Hz",
         measured_value="…",                 # fill from Sprint 00 Execution Log
         status="…",
         sprint_id="00",
         notes=""),
    dict(claim_id=2,
         description="Cracked amplitude spectra at 650 & 750 RPM show 1X+2X+ higher harmonics",
         sinha_source="Fig. 2",
         exit_criterion="visible harmonics out to ≥ 5X above −40 dB noise floor",
         measured_value="…",
         status="…",
         sprint_id="05",
         notes=""),
    dict(claim_id=3,
         description="Cracked orbits: figure-eight at 650, loop-containing-small-loop at 750",
         sinha_source="Fig. 3",
         exit_criterion="zero-crossings/rev at 750 ≥ 4",
         measured_value="…",
         status="…",
         sprint_id="05",
         notes=""),
    dict(claim_id=4,
         description="Misalignment amplitude spectra at 750 & 900 RPM show dense combs",
         sinha_source="Fig. 4",
         exit_criterion="≥ 6 harmonics above noise floor at both speeds",
         measured_value="…",
         status="…",
         sprint_id="06",
         notes=""),
    dict(claim_id=5,
         description="Crack bi-spectrum: B22 appears at 650 and is prominent at 750 (speed-dependent)",
         sinha_source="Fig. 5",
         exit_criterion="|B22/B11|(750) ≥ 2·|B22/B11|(650)",
         measured_value="…",
         status="…",
         sprint_id="05",
         notes=""),
    dict(claim_id=6,
         description="Misalignment bi-spectrum: B11, B12, B13 present; B22 absent; topology speed-invariant",
         sinha_source="Fig. 6",
         exit_criterion="B22/B11 ≤ 0.10 at both; B13/B11 ≥ 0.15 at both; topology(750)==topology(900)",
         measured_value="…",
         status="…",
         sprint_id="06",
         notes=""),
    dict(claim_id=7,
         description="Crack tri-spectrum: speed-dependent, T222 emerges at 750",
         sinha_source="Fig. 7",
         exit_criterion="|T222|(750) ≥ 0.10; |T222|(650) < 0.10",
         measured_value="…",
         status="…",
         sprint_id="05",
         notes=""),
    dict(claim_id=8,
         description="Misalignment tri-spectrum: only T111 at both speeds",
         sinha_source="Fig. 8",
         exit_criterion="no non-T111 ball ≥ 0.10 at either speed",
         measured_value="…",
         status="…",
         sprint_id="06",
         notes=""),
    dict(claim_id=9,
         description="Healthy rotor: |B|, |T| < 0.3 everywhere (noise floor)",
         sinha_source="§4",
         exit_criterion="max(|B|), max(|T|) on healthy-case HDF5 records < 0.30",
         measured_value="…",
         status="…",
         sprint_id="02/05/06",
         notes=""),
    dict(claim_id=10,
         description="Sinha FE at 772.5 RPM (Fig. 10) reproduced: orbit + bispectrum + trispectrum",
         sinha_source="§5, Figs. 9, 10",
         exit_criterion="3 expected bispectrum peaks within ±1 bin at Δf=1.25 Hz; T111 in trispectrum",
         measured_value="…",
         status="…",
         sprint_id="04",
         notes=""),
]

out = Path(__file__).parent / "results" / "validation_matrix.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ROWS[0].keys())
    w.writeheader()
    for r in ROWS:
        w.writerow(r)
print(f"wrote {out}")
```

Fill the `measured_value` and `status` columns **manually** from the Execution Log sections of Sprints 00–06. Script does not scrape the logs — the human decision of pass/fail/partial is worth the five minutes it takes.

### 2. Assemble `reports/sinha_validation_figures.pdf`

A single PDF with **six paired panels** (one per Sinha figure we replicated) plus a title page and a table of contents.

Recommended layout (one sheet per paired panel):

```
┌──────────────────────────────────────────────────────────┐
│  Sinha (2007) Fig. N                     Cristofer FE     │
│  [scanned or PDF-extracted image]        [Sprint NN PNG]  │
│                                                           │
│  Verdict: PASS / FAIL / PARTIAL                           │
│  Exit criterion: ...                                      │
│  Measured: ...                                            │
│  Notes: ...                                               │
└──────────────────────────────────────────────────────────┘
```

Script it with `matplotlib.backends.backend_pdf.PdfPages`:

```python
# 01_rotordynamic_simulation/build_validation_deck.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

PAIRS = [
    ("figures/sinha_paper/fig2.png",   "results/figures/sprint_05/fig2_amplitude_spectra.png",    "Fig. 2 — Cracked amplitude spectra", "PASS"),
    ("figures/sinha_paper/fig3.png",   "results/figures/sprint_05/fig3_orbits.png",               "Fig. 3 — Cracked orbits",            "PASS"),
    ("figures/sinha_paper/fig4.png",   "results/figures/sprint_06/fig4_amplitude_spectra.png",    "Fig. 4 — Misaligned spectra",       "PASS"),
    ("figures/sinha_paper/fig5.png",   "results/figures/sprint_05/fig5b_bispectrum_750.png",      "Fig. 5 — Cracked bi-spectrum",      "PASS"),
    ("figures/sinha_paper/fig6.png",   "results/figures/sprint_06/fig6a_bispectrum_750.png",      "Fig. 6 — Misaligned bi-spectrum",   "PASS"),
    ("figures/sinha_paper/fig7.png",   "results/figures/sprint_05/fig7b_trispectrum_750.png",     "Fig. 7 — Cracked tri-spectrum",     "PASS"),
    ("figures/sinha_paper/fig8.png",   "results/figures/sprint_06/fig8a_trispectrum_750.png",     "Fig. 8 — Misaligned tri-spectrum",  "PASS"),
    ("figures/sinha_paper/fig10.png",  "results/figures/sprint_04/fig10a_bispectrum.png",         "Fig. 10 — Sinha FE replication",    "PASS"),
]

out = Path(__file__).parent.parent / "reports" / "sinha_validation_figures.pdf"
out.parent.mkdir(parents=True, exist_ok=True)

with PdfPages(out) as pdf:
    # Title page …
    fig, ax = plt.subplots(figsize=(8.5, 11)); ax.axis("off")
    ax.text(0.5, 0.7, "Sinha (2007) vs ROSS + HOS", ha="center", size=20, weight="bold")
    ax.text(0.5, 0.6, "Validation deck", ha="center", size=14)
    # … (add run timestamp, ROSS version, scoring summary)
    pdf.savefig(fig); plt.close(fig)

    for sinha_png, cristofer_png, title, verdict in PAIRS:
        fig, axes = plt.subplots(1, 2, figsize=(11, 8.5))
        for ax, img_path in zip(axes, (sinha_png, cristofer_png)):
            try:
                ax.imshow(plt.imread(img_path))
                ax.axis("off")
            except FileNotFoundError:
                ax.text(0.5, 0.5, f"missing\n{img_path}", ha="center", va="center")
                ax.axis("off")
        fig.suptitle(f"{title}   —   Verdict: {verdict}", size=13)
        pdf.savefig(fig); plt.close(fig)
```

The `figures/sinha_paper/fig*.png` paths are scans of Sinha's figures (extract from the PDF in `99_references/` with `pdftoppm` or similar). If extraction is not legally/logistically permitted for internal drafts, leave the left-hand slot as a "see Sinha (2007) Fig. N" placeholder with the figure citation.

### 3. Draft `01_article/03_methods_draft.md`

Three sections, aiming for 3–4 pages of thesis prose. Skeleton:

```markdown
# Methods — Draft (Sprint 07)

## 3.1 Finite-element rotor model

- Geometry (matches Sinha §3): 10 mm OD solid steel shaft, 550 mm long; bearings at 20 and 510 mm; balance disk (75/10/25 mm) at midspan; crack element at 315 mm; probe at 490 mm (one-element upstream of bearing-2). **Figure placeholder:** rotor schematic from `00_sinha_rotor.ipynb`.
- Material: steel with `E = 211 GPa, G_s = 81.1 GPa, ρ = 7810 kg/m³`.
- Element type: ROSS `ShaftElement`, 6-DOF-per-node beam with shear, rotary inertia, and gyroscopic terms enabled.
- Bearing calibration: isotropic `kxx = kyy = k_opt`, with `k_opt` found by Brent's method on the residual `f1(k) − 27.50 Hz`, where 27.50 Hz is Sinha's experimental first bending frequency (§3). The calibrated value is reported in Table M1.
- Damping: stiffness-proportional, tuned so `ζ₁ = 0.3 %` at the first mode, matching Sinha §5. Method `tune_damping` (see `01_rotordynamic_simulation/sprints/03_damping_and_modal_truncation.md`).
- Modal-truncation order: `NUM_MODES`, convergence-tested in Sprint 03 against a 36-mode reference.

## 3.2 Fault models

### Breathing crack (Mayes)
The cracked element's stiffness varies with shaft angle θ as `K(θ) = K_o − f(θ)·(K_o − K_c)`, with `f(θ) = ½(1 − cos θ)` — this is exactly Sinha's own FE breathing function `(1 − cos θ) Δk / 2` (§5). Implemented in ROSS as `crack_model="Mayes"`; `K_c` is built from Papadopoulos linear-fracture-mechanics compliance coefficients. Depth ratio `a/D = 0.5` matches Sinha's rig.

### Parallel misalignment (flex coupling, Xia et al. 2019)
Implemented via ROSS `run_misalignment(coupling="flex", mis_type="parallel")`. Offsets `δx = 1.0 mm`, `δy = 0.5 mm` (matches Sinha §3.2 rig). Coupling stiffnesses `radial = 4·10⁴ N/m`, `bending = 3.8·10⁴ N·m/rad`. Sinha could not FE-simulate misalignment; this is the thesis' contribution beyond the paper.

## 3.3 Time integration and acquisition pipeline

- Integrator: Newmark-β via ROSS internal solver, `dt = 1/10000 s` (Sinha §5).
- Record length: 25 s, transient cut-off at 2 s.
- Anti-aliasing: 8th-order zero-phase Butterworth LP at 1 kHz.
- Downsample: to 1 kHz (Sinha FE protocol) or 2560 Hz (Sinha experimental protocol), selected per sprint.
- Noise: additive white Gaussian noise to achieve SNR = 40 dB (Sinha §5).
- All simulations persisted to `results/campaign.h5` with per-case metadata (`ross_version`, timestamp, parameter attributes).

## 3.4 Higher-order spectra

- Bi-spectrum (Sinha Eq. 2) and tri-spectrum (Sinha Eq. 3), both by the direct DFT method with segment averaging and Hann-windowed, detrended segments.
- Estimator settings: 50 segments, 50 % overlap, `Δf = 1.25 Hz` — identical to Sinha §3.3.
- Normalization: Kim & Powers (1979). Bicoherence in [0, 1] with a `max(denom, 1e-30)` small-denominator guard.
- Plotting: bispectrum as `|B|/max|B|` 3-D surface over the non-redundant region `f_l ≤ f_m`; tri-spectrum as balls of diameter ∝ `|T|` at `(f_l, f_m, f_n)` above a 0.10 normalized threshold (Sinha Figs. 5–8, 10 convention).

## 3.5 Validation protocol

We report a scored validation matrix against Sinha (2007) Figs. 2, 3, 5, 7 (crack at 650 / 750 RPM), Figs. 4, 6, 8 (misalignment at 750 / 900 RPM), Fig. 9 (orbit), and Fig. 10 (Sinha's own FE). Ten falsifiable exit criteria; see Table M2.
```

Leave placeholders where specific numbers should land after Sprint 07's matrix is filled. The advisor can then iterate on prose rather than structure.

## Exit criteria

- [ ] `results/validation_matrix.csv` has 10 rows, every `status` field is `pass`, `fail`, `partial`, or `not_tested`.
- [ ] `reports/sinha_validation_figures.pdf` renders, opens cleanly, contains title page + one paired panel per Sinha figure + one summary scoring page.
- [ ] `01_article/03_methods_draft.md` has the five sections above filled in with measured numbers substituted for every `…` placeholder, and cites Sinha (2007), Kim & Powers (1979), Xia et al. (2019), and Mayes & Davies (1984) in the correct places.
- [ ] Advisor can read the Methods draft + scan the PDF in 15 minutes and pose concrete next-step questions (as opposed to "can you explain what you did?").

## Implementation notes

- **Honesty clause.** Any `status = "fail"` row is a scientific result, not a scaffolding bug. Write its `notes` column as if it were going straight into the paper's Discussion section ("ROSS's `run_misalignment` produced |B22|/|B11| = 0.17 at 750 RPM, above Sinha's zero-floor claim; most-likely explanation: Xia et al. flex-coupling adds a small quadratic coupling absent from Sinha's rig. Reported as a model-form limitation.").
- **Partial** is the right status when the numeric exit criterion does not strictly pass but the *topology* does — e.g. B22 at (2X − 1 bin, 2X − 1 bin) rather than exactly on-bin at 750 RPM.
- **Do not regenerate artefacts.** This sprint reads PNGs, CSVs, and Execution Logs from prior sprints; it does not re-simulate, re-HOS, or re-plot. If something needs regenerating, that is a Sprint 03/05/06 bug — fix it there, not here.
- **Side-by-side layout.** Sinha's paper figures are subject to journal copyright. For internal advisor drafts, embedding is fine; for the final thesis manuscript, replace with a "see Sinha (2007) Fig. N" citation plus the Cristofer reproduction alone.
- **After this sprint.** The next natural step is *not* another validation sprint but the DoE phase from `01_article/01_publication_roadmap.md §5.3` — crack-depth sweep × misalignment-level sweep. Flag that as a "Sprint 08 candidate" in the sprints/README.md.

## Dependencies / hand-offs

- Consumes every sprint above. Produces nothing for downstream sprints in this programme — the thesis manuscript is the only downstream consumer.

## References

- Sinha (2007), full paper. `99_references/`.
- Kim, Y. C. & Powers, E. J. (1979). Digital bispectral analysis… *IEEE T. Plasma Sci.* 7(2).
- Xia, Y. et al. (2019). Misaligned flexible coupling force model. *Applied Acoustics.*
- Mayes, I. W. & Davies, W. G. R. (1984). Transverse-crack breathing model. *ASME JVASRD* 106.
- Plan: `/Users/cristofer/.claude/plans/great-job-based-on-curious-music.md`.
- Audit: `01_rotordynamic_simulation/05_synthesis.ipynb` (the source of the 10 falsifiable claims and their numeric exit criteria).
