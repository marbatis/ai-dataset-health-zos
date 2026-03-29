from __future__ import annotations

from typing import List
from math import cos, radians, isfinite

def bbox_from_center(lat: float, lon: float, half_size_m: float) -> List[float]:
    """Return [min_lon, min_lat, max_lon, max_lat] using simple spherical approximations.

    Guardrails:
    - |lat| must be < 85° (approximation degrades near poles).
    - 0 < half_size_m <= 5,000,000 (5,000 km half-size cap to avoid nonsense).
    - Inputs must be finite.

    Note: This is intended for coarse AOIs (~10–200 km). For polar/large AOIs use proper geodesy.
    """
    if not (isfinite(lat) and isfinite(lon) and isfinite(half_size_m)):
        raise ValueError("lat/lon/half_size_m must be finite floats")
    if abs(lat) >= 85.0:
        raise ValueError("Latitude too close to poles for this approximation (|lat| must be < 85°)")
    if half_size_m <= 0 or half_size_m > 5_000_000:
        raise ValueError("half_size_m must be in (0, 5,000,000] meters")

    # Approx conversions
    dlat = half_size_m / 111_320.0
    # protect against extremely small cos near the cap
    denom = 111_320.0 * max(1e-3, cos(radians(lat)))
    dlon = half_size_m / denom
    return [lon - dlon, lat - dlat, lon + dlon, lat + dlat]
