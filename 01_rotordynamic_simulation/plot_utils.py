"""Sinha-convention HOS visualizers (Figs. 5, 6, 7, 8, 10).

Matplotlib functions (static export)
--------------------------------------
- ``plot_bispectrum_surface`` → Sinha Figs. 5 / 6 (3-D |B|/max|B| surface)
- ``plot_trispectrum_balls``  → Sinha Figs. 7 / 8 / 10(b) (ball scatter)

Plotly functions (interactive, notebook-friendly)
--------------------------------------------------
- ``plotly_bispectrum_surface``  → interactive go.Surface, hot colormap
- ``plotly_bicoherence_surface`` → same but for b² (bounded [0, 1])
- ``plotly_trispectrum_balls``   → interactive go.Scatter3d, ball size ∝ amplitude
- ``plotly_spectrum``            → 2-D amplitude spectrum line plot
- ``plotly_time``                → 2-D time-domain signal plot

All matplotlib functions return ``matplotlib.figure.Figure``.
All plotly functions return ``plotly.graph_objects.Figure``.
Neither family calls ``show()`` or ``savefig()``; callers handle display.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3d projection
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_bispectrum_surface(B, freqs, fmax_hz=50.0, normalize=True):
    """3-D surface of |B|/max|B| over the non-redundant triangle.

    Restricted to the region f_l ≤ f_m, f_l + f_m ≤ fmax_hz.
    Hot colormap, Sinha Figs. 5/6 style.

    Parameters
    ----------
    B         : complex ndarray, shape (nf, nf)   bispectrum from :func:`signal_utils.bispectrum`
    freqs     : ndarray, shape (nf,)              Hz axis
    fmax_hz   : float                             upper frequency for both axes
    normalize : bool                              divide by max|B| when True

    Returns
    -------
    fig : matplotlib.figure.Figure
    """
    idx = freqs <= fmax_hz
    f_sub = freqs[idx]
    B_sub = B[np.ix_(idx, idx)]
    Z = np.abs(B_sub)

    # Zero out the redundant half and sum frequencies above fmax_hz
    nf_sub = len(f_sub)
    for i in range(nf_sub):
        for j in range(nf_sub):
            if j < i or (i + j) >= nf_sub:
                Z[i, j] = 0.0

    if normalize:
        peak = Z.max()
        Z = Z / peak if peak > 0.0 else Z

    X, Y = np.meshgrid(f_sub, f_sub, indexing="ij")
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(8, 6))
    ax.plot_surface(X, Y, Z, cmap="hot", vmin=0.0, vmax=1.0 if normalize else None)
    ax.set_xlabel("$f_l$ (Hz)")
    ax.set_ylabel("$f_m$ (Hz)")
    ax.set_zlabel("|B|/max|B|" if normalize else "|B|")
    ax.set_title("Bispectrum — non-redundant triangle")
    fig.tight_layout()
    return fig


def plot_trispectrum_balls(T_dict, freqs, fmax_hz=35.0, amp_min=0.10):
    """Scatter3D where each (l, m, n) with |T|/max|T| ≥ amp_min is a ball.

    Ball diameter scales with normalized amplitude.
    Matches Sinha Figs. 7, 8, 10(b).

    Parameters
    ----------
    T_dict  : dict  ``{(l, m, n): complex}`` from :func:`signal_utils.trispectrum`
    freqs   : ndarray  Hz axis
    fmax_hz : float    upper frequency for each individual index
    amp_min : float    minimum normalized amplitude to plot (Sinha threshold = 0.10)

    Returns
    -------
    fig : matplotlib.figure.Figure
    """
    if not T_dict:
        raise ValueError("T_dict is empty — nothing to plot.")

    T_abs = {k: abs(v) for k, v in T_dict.items()}
    T_max = max(T_abs.values())

    xs, ys, zs, sizes, colors = [], [], [], [], []
    for (l, m, n), a in T_abs.items():
        norm_amp = a / T_max
        if norm_amp < amp_min:
            continue
        fl, fm, fn = freqs[l], freqs[m], freqs[n]
        if fl > fmax_hz or fm > fmax_hz or fn > fmax_hz:
            continue
        xs.append(fl)
        ys.append(fm)
        zs.append(fn)
        sizes.append(norm_amp * 300.0)
        colors.append(norm_amp)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(xs, ys, zs, s=sizes, c=colors, cmap="hot", vmin=0.0, vmax=1.0, alpha=0.85)
    ax.set_xlabel("$f_l$ (Hz)")
    ax.set_ylabel("$f_m$ (Hz)")
    ax.set_zlabel("$f_n$ (Hz)")
    ax.set_title("Trispectrum — balls ∝ |T|/max|T|")
    fig.colorbar(sc, ax=ax, shrink=0.5, pad=0.1, label="|T|/max|T|")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Plotly interactive functions
# ---------------------------------------------------------------------------

def _bispectrum_z(B, freqs, fmax_hz, normalize):
    """Crop to fmax_hz, zero redundant region, optionally normalize."""
    idx = np.where(freqs <= fmax_hz)[0]
    f_sub = freqs[idx]
    Z = np.abs(B[np.ix_(idx, idx)]).copy()
    nf_sub = len(f_sub)
    rows, cols = np.triu_indices(nf_sub, k=0)
    lm = rows + cols
    valid = lm < nf_sub
    mask = np.zeros((nf_sub, nf_sub), dtype=bool)
    mask[rows[valid], cols[valid]] = True
    Z[~mask] = 0.0
    if normalize and Z.max() > 0.0:
        Z /= Z.max()
    return f_sub, Z


def plotly_bispectrum_surface(B, freqs, fmax_hz=50.0, normalize=True, title=None):
    """Interactive Plotly 3-D surface of |B|/max|B|.

    Hot colormap, non-redundant triangle only.
    Mirrors Sinha Figs. 5 / 6.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    f_sub, Z = _bispectrum_z(B, freqs, fmax_hz, normalize)
    zlabel = "|B| / max|B|" if normalize else "|B|"
    fig = go.Figure(data=go.Surface(
        x=f_sub, y=f_sub, z=Z,
        colorscale="Hot",
        cmin=0.0, cmax=1.0 if normalize else None,
        colorbar=dict(title=zlabel, thickness=15),
    ))
    fig.update_layout(
        title=title or "Bispectrum — non-redundant triangle",
        scene=dict(
            xaxis_title="f<sub>l</sub> (Hz)",
            yaxis_title="f<sub>m</sub> (Hz)",
            zaxis_title=zlabel,
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.9)),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )
    return fig


def plotly_bicoherence_surface(b2, freqs, fmax_hz=50.0, title=None):
    """Interactive Plotly 3-D surface of bicoherence squared b² ∈ [0, 1].

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    f_sub, Z = _bispectrum_z(b2.astype(complex), freqs, fmax_hz, normalize=False)
    Z = Z.real
    fig = go.Figure(data=go.Surface(
        x=f_sub, y=f_sub, z=Z,
        colorscale="Hot",
        cmin=0.0, cmax=1.0,
        colorbar=dict(title="b²", thickness=15),
    ))
    fig.update_layout(
        title=title or "Bicoherence² — non-redundant triangle",
        scene=dict(
            xaxis_title="f<sub>l</sub> (Hz)",
            yaxis_title="f<sub>m</sub> (Hz)",
            zaxis_title="b²",
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.9)),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )
    return fig


def plotly_trispectrum_balls(T_dict, freqs, fmax_hz=50.0, amp_min=0.10, title=None):
    """Interactive Plotly 3-D scatter where each (l, m, n) is a ball.

    Ball size and colour scale with |T|/max|T|.
    Matches Sinha Figs. 7 / 8 / 10(b).

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    if not T_dict:
        raise ValueError("T_dict is empty — nothing to plot.")
    T_abs = {k: abs(v) for k, v in T_dict.items()}
    T_max = max(T_abs.values())

    xs, ys, zs, amps, labels = [], [], [], [], []
    for (l, m, n), a in T_abs.items():
        norm = a / T_max
        if norm < amp_min:
            continue
        fl, fm, fn = freqs[l], freqs[m], freqs[n]
        if fl > fmax_hz or fm > fmax_hz or fn > fmax_hz:
            continue
        xs.append(fl); ys.append(fm); zs.append(fn); amps.append(norm)
        labels.append(f"({fl:.2f}, {fm:.2f}, {fn:.2f}) Hz<br>|T|/max = {norm:.3f}")

    fig = go.Figure(data=go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode="markers",
        marker=dict(
            size=[a * 25 + 4 for a in amps],
            color=amps,
            colorscale="Hot",
            cmin=0.0, cmax=1.0,
            opacity=0.85,
            colorbar=dict(title="|T|/max|T|", thickness=15),
        ),
        text=labels,
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(
        title=title or "Trispectrum — ball size ∝ |T|/max|T|",
        scene=dict(
            xaxis_title="f<sub>l</sub> (Hz)",
            yaxis_title="f<sub>m</sub> (Hz)",
            zaxis_title="f<sub>n</sub> (Hz)",
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.0)),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )
    return fig


def plotly_spectrum(amp, freqs, fmax_hz=100.0, title="Amplitude Spectrum", color="royalblue"):
    """2-D Plotly amplitude spectrum line plot (single-sided).

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    idx = freqs <= fmax_hz
    fig = go.Figure(data=go.Scatter(
        x=freqs[idx], y=amp[idx],
        mode="lines",
        line=dict(color=color, width=1.5),
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Frequency (Hz)",
        yaxis_title="Amplitude",
        margin=dict(l=50, r=20, t=40, b=40),
    )
    return fig


def plotly_time(x, fs, t_max=None, title="Time-domain signal", color="steelblue"):
    """2-D Plotly time-domain signal.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    t = np.arange(len(x)) / fs
    if t_max is not None:
        mask = t <= t_max
        t, x = t[mask], x[mask]
    fig = go.Figure(data=go.Scatter(
        x=t, y=x,
        mode="lines",
        line=dict(color=color, width=1.0),
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        margin=dict(l=50, r=20, t=40, b=40),
    )
    return fig
