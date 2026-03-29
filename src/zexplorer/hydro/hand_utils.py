from __future__ import annotations

"""Lightweight hydro plausibility utilities (pure NumPy).

These helpers avoid heavy GIS deps. They operate on arrays you supply (already
reprojected to the same grid), so they remain CI-friendly and reproducible.

- `relative_hand(dem)`: toy HAND proxy (DEM - local minimum via percentile).
- `plausibility_score(delta_db, hand, hand_threshold=5.0)`:
    score in [0,1] based on fraction of pixels within the candidate mask
    that fall under a HAND-like threshold and show positive delta_db.
"""

import numpy as np
from typing import Tuple

def relative_hand(dem: np.ndarray, window: int = 51, percentile: float = 5.0) -> np.ndarray:
    """Compute a crude relative elevation (HAND-like) from a DEM array.

    Parameters
    ----------
    dem : np.ndarray
        Elevation array (float32/float64). NaNs allowed.
    window : int
        Odd window size for local percentile (default 51 ~ 1–2 km at 30–60 m px).
    percentile : float
        Local percentile to subtract (default 5th).

    Returns
    -------
    np.ndarray
        Relative elevation (>=0), NaNs preserved.
    """
    from scipy.ndimage import uniform_filter

    # Replace NaNs with local mean approximation
    dem_filled = dem.copy()
    nan_mask = np.isnan(dem_filled)
    if nan_mask.any():
        m = np.nanmean(dem_filled)
        dem_filled[nan_mask] = m

    # Approximate low-percentile by repeated uniform filters (cheap)
    k = max(3, window | 1)  # ensure odd
    base = uniform_filter(dem_filled, size=k, mode="nearest")
    rel = dem_filled - base
    rel[rel < 0] = 0.0
    rel[nan_mask] = np.nan
    return rel

def plausibility_score(delta_db: np.ndarray, hand: np.ndarray, candidate_mask: np.ndarray, hand_threshold: float = 5.0) -> float:
    """Compute a simple plausibility score for floodplain engineered features.

    Heuristic: candidate pixels with **positive ΔdB** (wet>dry) that also sit in
    **low relative elevation** (HAND <= threshold) are more plausible.

    Returns fraction in [0,1] meeting both tests over the candidate mask.
    """
    if delta_db.shape != hand.shape or hand.shape != candidate_mask.shape:
        raise ValueError("All arrays must share the same shape")
    mask = candidate_mask.astype(bool)
    if mask.sum() == 0:
        return 0.0
    ok = (delta_db > 0) & (hand <= hand_threshold) & mask
    return float(ok.sum()) / float(mask.sum())
