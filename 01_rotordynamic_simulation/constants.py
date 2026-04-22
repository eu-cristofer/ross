"""Constants for the Sinha rotor simulation (single source of truth).

Provenance (symbol → origin → conclusion for Methods)
-----------------------------------------------------
- ``BEARING_*_NODE``, ``DISK_NODE``, ``CRACK_NODE``, ``PROBE_NODE`` — Frozen
  assembly matching ``sinha_rotor.toml`` used by notebooks ``00`` (build) /
  ``01``–``04`` (load). Conclusion: probe and crack indices are consistent with
  the published Sinha geometry table in ``00_sinha_rotor.ipynb``.

- ``UNB_MAG`` — Shared default across ``01``–``04`` crack/unbalance studies.
  Conclusion: one residual unbalance level for comparability across notebooks.
  
- ``UNB_PHASE`` = ``4π/3`` rad — Used by ``01``–``03`` via this module. Notebook
  ``04`` previously used ``3π/4`` rad inline; that local choice was superseded
  in Sprint 01 so all Sinha-replication paths share one phase. Conclusion: state
  the canonical phase explicitly in the thesis; regenerate ``04`` figures if
  old runs must be cited.
  
- ``SPEED_CRACK_*``, ``SPEEDS`` — Crack / baseline campaigns at 650 and 750 rpm
  (``02``, ``03``). ``SPEEDS`` aliases the crack pair for backward compatibility.

- ``SPEED_MIS_*`` — Misalignment cases at 750 and 900 rpm introduced in
  ``04_sinha_fault_analysis.ipynb``. Conclusion: misalignment speed pair is
  documented here for the integrated fault-comparison notebook only.

- ``MIS_X``, ``MIS_Y`` — Parallel misalignment offsets from ``04``.

- ``CRACK_RATIO`` — Default ``depth_ratio`` (0.5) for Mayes/Gasch cap; aligned
  with ``04`` narrative and ``03`` sweeps (other depths remain notebook-local).

- ``DT``, ``T``, ``FREQ_RANGE`` — Default integration and plot band shared by
  time-domain notebooks. Conclusion: ``fs_sim = 1/DT`` is the simulation sample
  rate unless subsampling is applied in post-processing (see technical note).

- ``SINHA_*`` — Acquisition and HOS metadata from Sinha (2007) §3 / §3.3 as cited
  in the sprint doc; for Sprint 02+ bispectrum code to import. Not simulation
  inputs until the analysis pipeline resamples/filters (see technical note).
"""

import numpy as np
from ross import Q_

__all__ = [
    # Keep this list alphabetically ordered for maintainability.
    "BEARING_1_NODE",
    "BEARING_2_NODE",
    "CRACK_NODE",
    "CRACK_RATIO",
    "DISK_NODE",
    "DT",
    "FREQ_RANGE",
    "FS_SIM_HZ",
    "MIS_X",
    "MIS_Y",
    "PROBE_NODE",
    "SPEED_0",
    "SPEED_1",
    "SPEED_CRACK_0",
    "SPEED_CRACK_1",
    "SPEED_MIS_0",
    "SPEED_MIS_1",
    "SPEEDS",
    "SINHA_AA_CUTOFF_HZ",
    "SINHA_FS_HZ",
    "SINHA_HOS_DF_HZ",
    "SINHA_HOS_N_SEGMENTS",
    "SINHA_HOS_OVERLAP",
    "T",
    "UNB_MAG",
    "UNB_PHASE"
]

# Crack parameters
CRACK_RATIO = 0.5

# Rotor nodes (must match sinha_rotor.toml for default Sinha path)
BEARING_1_NODE = 1
BEARING_2_NODE = 11
DISK_NODE = 6
CRACK_NODE = DISK_NODE + 1
PROBE_NODE = BEARING_2_NODE - 1

# Unbalance parameters
UNB_MAG = Q_(2e-4, "kg*m")
UNB_PHASE = Q_(4 * np.pi / 3, "rad")

# Speed parameters (rpm)
SPEED_CRACK_0 = Q_(650, "rpm")
SPEED_CRACK_1 = Q_(750, "rpm")
SPEED_MIS_0 = Q_(750, "rpm")
SPEED_MIS_1 = Q_(900, "rpm")

# Backward-compatible names used in early notebooks
SPEED_0 = SPEED_CRACK_0
SPEED_1 = SPEED_CRACK_1
SPEEDS = [SPEED_CRACK_0, SPEED_CRACK_1]

# Misalignment (parallel flexible coupling), from 04 fault analysis
MIS_X = Q_(1.0e-3, "m")
MIS_Y = Q_(0.5e-3, "m")

# Time parameters
DT = 1e-3
T = np.arange(0.0, 2.0, DT)
FS_SIM_HZ = 1.0 / DT

# Frequency range parameters for plotting
FREQ_RANGE = Q_((0, 200), "Hz")

# Sinha (2007) acquisition / HOS estimation handoff (Sprint 02+)
SINHA_FS_HZ = 2560
SINHA_AA_CUTOFF_HZ = 1000
SINHA_HOS_DF_HZ = 1.25
SINHA_HOS_N_SEGMENTS = 50
SINHA_HOS_OVERLAP = 0.5
