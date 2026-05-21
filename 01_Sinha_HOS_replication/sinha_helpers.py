"""Shared post-processing helpers for the Sinha replication notebooks.

Provenance
----------
Extracted from verbatim copies previously inlined in
``02_sinha_unbalance_phase_crack.ipynb`` (Sprint 01) and
``03_sinha_crack_model_comparison.ipynb`` so they can evolve in one place.

- ``get_harmonic_amplitude`` — computed FFT amplitude at a target harmonic
  bin of a probe time series over the steady-state window.
- ``probe_dof_indices`` — the ``dof_x``/``dof_y`` index recipe for a probe
  node, accounting for ROSS's ``link_nodes`` offset.
- ``HARMONIC_COLORS`` — 1X/2X/3X colour tuple shared between the harmonic bar
  charts and polar plots in ``02``.
"""

import numpy as np

__all__ = [
    "HARMONIC_COLORS",
    "get_harmonic_amplitude",
    "probe_dof_indices",
]

HARMONIC_COLORS = ("#1f77b4", "#ff7f0e", "#2ca02c")


def get_harmonic_amplitude(yout, dof, t, target_freq_hz, steady_start):
    """Return the FFT amplitude at the frequency bin closest to ``target_freq_hz``.

    Parameters
    ----------
    yout : ndarray
        Time-response array shaped (n_samples, n_dof).
    dof : int
        Global DOF index to extract.
    t : ndarray
        Time vector matching ``yout``'s leading axis.
    target_freq_hz : float
        Target frequency (Hz) — the nearest ``rfftfreq`` bin is returned.
    steady_start : int
        Index into ``yout``/``t`` marking the start of the steady-state window.

    Returns
    -------
    amplitude : float
        Single-sided FFT amplitude at the selected bin.
    """
    signal = yout[steady_start:, dof]
    dt = t[1] - t[0]
    N = len(signal)
    freqs = np.fft.rfftfreq(N, d=dt)
    fft_vals = 2.0 / N * np.abs(np.fft.rfft(signal))
    idx = np.argmin(np.abs(freqs - target_freq_hz))
    return fft_vals[idx]


def probe_dof_indices(rotor, node):
    """Return the global ``(dof_x, dof_y)`` indices for a probe node.

    Accounts for ROSS's ``link_nodes`` bookkeeping: if the requested node is a
    link node, the translational DOFs are offset from the naive
    ``number_dof * node`` mapping.

    Parameters
    ----------
    rotor : ross.Rotor
    node : int

    Returns
    -------
    dof_x, dof_y : int
    """
    ndof = rotor.number_dof
    nodes = rotor.nodes
    link_nodes = rotor.link_nodes
    fix_dof = (node - nodes[-1] - 1) * ndof // 2 if node in link_nodes else 0
    return ndof * node - fix_dof, ndof * node + 1 - fix_dof
