"""Constants for the Sinha rotor simulation."""

import numpy as np
from ross import Q_

__all__ = [
    "CRACK_RATIO",
    "BEARING_1_NODE",
    "BEARING_2_NODE",
    "DISK_NODE",
    "CRACK_NODE",
    "PROBE_NODE",
    "UNB_MAG",
    "UNB_PHASE",
    "SPEEDS",
    "DT",
    "T",
    "FREQ_RANGE",
]

# Crack parameters
CRACK_RATIO = 0.5

# Rotor nodes
BEARING_1_NODE = 1
BEARING_2_NODE = 11
DISK_NODE = 6
CRACK_NODE = DISK_NODE + 1
PROBE_NODE = BEARING_2_NODE - 1

# Unbalance parameters
UNB_MAG = Q_(2e-4, "kg*m")
UNB_PHASE = Q_(4 * np.pi / 3, "rad")

# Speed parameters
SPEED_0 = Q_(650, "rpm")
SPEED_1 = Q_(750, "rpm")
SPEEDS = [SPEED_0, SPEED_1]

# Time parameters
DT = 1e-3
T = np.arange(0.0, 2.0, DT)

# Frequency range parameters for plotting
FREQ_RANGE = Q_((0, 200), "Hz")
