# Saved Plan: Stepwise Sinha Replication

This file stores the implementation intent in the project workflow folder as requested.

## Objective

Validate a healthy FEM model against Sinha's reported first natural frequency
(27.50 Hz), then compare numerical crack/misalignment HOS patterns against
Sinha's experimental bispectrum trends at a semi-quantitative level.

## Rig Definition Used

- Shaft: steel, solid, OD 10 mm, total length 550 mm
- Bearings: at 20 mm and 510 mm from left end
- Disk: steel, OD 75 mm, ID 10 mm, thickness 25 mm, centered at 265 mm
- Coupler: represented by equivalent support effect in calibration
- Target: first lateral natural frequency = 27.50 Hz

## Deliverables

- Step scripts `step_01` to `step_06`
- Integrated notebook: `sinha_pipeline_step_by_step.ipynb`
- Reusable HOS helper module in `ross`
- Tests for HOS helper
- User guide index update
