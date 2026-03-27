**feat(geoutils): guardrails for `bbox_from_center` + tests**

**Why**
- Prevent pathological results near the poles or with invalid sizes.
- Make behavior explicit for coarse-AOI use cases.

**Changes**
- Guardrails: `|lat| < 85°`, `0 < half_size_m <= 5,000,000`, finite inputs.
- Protect `dlon` against tiny `cos(lat)`.
- Unit tests for invalid inputs and a near-cap sanity check.

**Notes**
- Existing behavior for typical lats (|lat| ≤ ~70°) and sizes is unchanged.
