# Stepwise Sinha Replication Workflow

This folder contains a human-learning-oriented workflow to replicate Sinha (2007)
numerically with ROSS.

## Learning Path

1. `step_01_geometry_and_units.py`
   - Rig assumptions and unit checks.
2. `step_02_build_healthy_rotor.py`
   - Healthy rotor model assembly from geometry.
3. `step_03_modal_calibration_27_5hz.py`
   - Inverse calibration to target first natural frequency at 27.50 Hz.
4. `step_04_fault_runs_crack_misalignment.py`
   - Healthy, crack, and misalignment fault runs.
5. `step_05_hos_analysis.py`
   - Bispectrum and bicoherence analysis.
6. `step_06_compare_with_sinha.py`
   - Semi-quantitative comparison outputs.
7. `sinha_pipeline_step_by_step.ipynb`
   - Integrated notebook connecting all steps.

## How To Run

From repo root:

```bash
python "01_rotordynamic_simulation/step_01_geometry_and_units.py"
python "01_rotordynamic_simulation/step_02_build_healthy_rotor.py"
python "01_rotordynamic_simulation/step_03_modal_calibration_27_5hz.py"
python "01_rotordynamic_simulation/step_04_fault_runs_crack_misalignment.py"
python "01_rotordynamic_simulation/step_05_hos_analysis.py"
python "01_rotordynamic_simulation/step_06_compare_with_sinha.py"
```

Outputs are saved in `01_rotordynamic_simulation/outputs`.

## Scope Note

This workflow targets numerical pattern-level and key-peak-level comparison with
Sinha's experimental HOS plots. It is not a one-to-one experimental replica.
