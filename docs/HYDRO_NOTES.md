# Hydro plausibility notes (RAT)

This module keeps hydro checks **lightweight** and **offline**:
- Use a DEM you already have (e.g., SRTM) resampled to the same grid as your ΔdB map.
- `relative_hand(dem)` gives a toy HAND-like layer good enough for ranking.
- `plausibility_score(delta_db, hand, candidate_mask)` returns a [0,1] score.

For higher fidelity (not included here): MERIT Hydro, proper HAND, and dynamic flood modeling.
