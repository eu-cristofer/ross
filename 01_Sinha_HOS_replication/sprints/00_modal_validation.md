# Sprint 00 — Modal FE validation against Sinha (2007)

> **Effort:** half a day, **blocking** for every downstream sprint.
> **Artefact produced:** a short notebook `01_rotordynamic_simulation/00a_modal_check.ipynb` (or appended cells in `01_sinha_rotor_modal.ipynb`) plus an updated docstring in `constants.py`.

## Why this sprint exists

Sinha (2007) reports **two different first bending frequencies** for the same rotor, and the difference matters for the thesis:

| Source | f1 (Hz) | How obtained |
|---|---|---|
| Sinha §3, experimental impulse-response (Ewins) | **27.50** | rig measurement, intact |
| Sinha §5, Sinha's own FE model | 26.53 | 2-node Euler–Bernoulli beam, 4 DOF/node |
| Sinha §3, experimental, cracked fully open, vertical | 26.25 | rig measurement |
| Sinha §5, Sinha's FE, cracked fully open, vertical | 25.75 | his FE with his breathing model |
| Sinha §5, Sinha's FE, cracked fully open, horizontal | 26.10 | his FE |

Cristofer's `00_sinha_rotor.ipynb` calibrates the ROSS bearing stiffness `kxx` via `brentq` so that the *intact* f1 = 27.50 Hz (i.e. matches Sinha's experimental rig). Subsequent sprints must know which of the two targets the thesis validates against.

**Decision for this thesis (recorded here, then in `constants.py`):** the calibration target is the **experimental** 27.50 Hz. Sinha's own FE 26.53 Hz is a reference-model artefact (his beam is coarser) and is not a target. HOS features will be compared against Sinha's experimental results (Figs. 2–8); Sinha's own FE (Fig. 10) is matched *qualitatively* on peak topology, not on exact Hz numbers.

## Prerequisites

- `01_rotordynamic_simulation/sinha_rotor.toml` exists and loads. Regenerate it by running `00_sinha_rotor.ipynb` if not.
- `01_rotordynamic_simulation/constants.py` still exports `BEARING_*_NODE`, `DISK_NODE`, `CRACK_NODE`, `PROBE_NODE`.
- Sinha (2007) PDF accessible at `99_references/Sinha - 2007 - ...pdf` for reviewer cross-checks.

## Work items

1. **Create `01_rotordynamic_simulation/00a_modal_check.ipynb`** (a ~5-cell notebook).
2. **Cell A — load and assert intact frequencies.**
   ```python
   import numpy as np, ross as rs
   from constants import DISK_NODE, BEARING_1_NODE, BEARING_2_NODE, PROBE_NODE, CRACK_NODE

   rotor = rs.Rotor.load("sinha_rotor.toml")
   modal = rotor.run_modal(speed=0)
   f_hz = modal.wn / (2 * np.pi)

   SINHA_EXP_F1 = 27.50   # Hz  Sinha §3
   TOL_F1       = 0.05    # Hz  engineering tolerance

   assert abs(f_hz[0] - SINHA_EXP_F1) <= TOL_F1, (
       f"intact f1 drifted: got {f_hz[0]:.4f}, target {SINHA_EXP_F1} ± {TOL_F1}"
   )
   print(f"intact f1 = {f_hz[0]:.4f} Hz  (target 27.50 Hz)   ✓")
   print(f"intact f2 = {f_hz[2]:.4f} Hz  (Sinha's FE: 228.62 Hz, for reference only)")
   ```
   If this assertion fails, re-run `00_sinha_rotor.ipynb` to regenerate `sinha_rotor.toml`. Do not weaken the tolerance.
3. **Cell B — fully-open crack spot-check.**
   ```python
   # Dial depth_ratio to 0.5 (Sinha's crack) and force "fully open" by picking
   # the angle where K(θ) is minimum. Compare to 26.25 Hz (Sinha exp, vertical).
   from ross.faults.crack import Crack

   depth = 0.5
   crack = Crack(rotor, n=CRACK_NODE, depth_ratio=depth, crack_model="Mayes")
   # Find θ in [0, 2π] that minimises K(θ)[0,0]:
   angles = np.linspace(0, 2*np.pi, 360)
   k_over_theta = np.array([crack._crack_model(a)[0, 0] for a in angles])
   theta_open = angles[np.argmin(k_over_theta)]
   print(f"Crack fully-open angle = {np.rad2deg(theta_open):.1f}° (should be near 180°)")
   # A modal analysis with the crack held open is a bigger change; for this
   # sprint, the shape check above plus Sprint 03's damping-tuned rerun is enough.
   ```
   This cell is informational — a decisive "fully-open f1 = 26.25 Hz" assertion needs a custom ROSS run with the crack stiffness frozen at `θ_open`, which is Sprint 03 / Sprint 04 work. For Sprint 00, just verify the breathing function has the expected shape and flag it to the reviewer.
4. **Cell C — record the decision in `constants.py`'s docstring.** Add a short paragraph under the existing provenance section:
   ```python
   # - ``SINHA_MODAL_TARGET`` = 27.50 Hz — first bending frequency target for the
   #   calibrated Sinha rotor. Matches Sinha (2007) §3 impulse-response result;
   #   Sinha's own FE (§5) reports 26.53 Hz and is NOT the calibration target.
   #   Fully-open cracked f1 target: 26.25 Hz vertical (Sinha §3); Sinha §5 FE
   #   reports 25.75 / 26.10 Hz and is NOT the target.
   ```
   Also expose `SINHA_MODAL_TARGET = 27.50` as a named constant so other sprints can import it.

## Exit criteria

- [ ] `00a_modal_check.ipynb` runs end-to-end without raising.
- [ ] Cell A passes the assertion that `|f1_current − 27.50| ≤ 0.05` Hz.
- [ ] `SINHA_MODAL_TARGET` is exported from `constants.py` and listed in `__all__`.
- [ ] The decision "calibration target is the experimental 27.50 Hz" is written into the `constants.py` docstring with exactly the sentence above, so the thesis Methods section can cite it unchanged.

## Dependencies / hand-offs

- Unblocks **every** subsequent sprint.
- Sprint 03 will replace `sinha_rotor.toml` with a damping-tuned version — the assertion in Cell A must still pass afterwards (damping does not move f1 appreciably).

## References

- Sinha, J. K. (2007). *Higher Order Spectra for Crack and Misalignment Identification in the Shaft of a Rotating Machine.* Structural Health Monitoring 6(4), 325–334. §3 and §5. `99_references/`.
- Ewins, D. J. (2000). *Modal Testing: Theory, Practice and Application.* 2nd ed. — cited by Sinha [31] for the impulse-response method that produced 27.50 Hz.
- Current rotor: `01_rotordynamic_simulation/sinha_rotor.toml`, built and calibrated in `00_sinha_rotor.ipynb`.
