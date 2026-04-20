"""Higher-order spectral estimation for rotordynamic signals."""

from ross.hos.acquisition import (
    add_gaussian_noise_snr,
    decimate_mean,
    lowpass_filter_zero_phase,
    sinha_acquisition_chain,
)
from ross.hos.bispectrum import (
    estimate_bicoherence,
    estimate_bispectrum,
    extract_bispectral_peaks,
)
from ross.hos.segmenting import _segment_signal
from ross.hos.trispectrum import estimate_trispectrum_point

__all__ = [
    "_segment_signal",
    "add_gaussian_noise_snr",
    "decimate_mean",
    "estimate_bicoherence",
    "estimate_bispectrum",
    "estimate_trispectrum_point",
    "extract_bispectral_peaks",
    "lowpass_filter_zero_phase",
    "sinha_acquisition_chain",
]
