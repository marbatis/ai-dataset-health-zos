**feat(rat/hydro): lightweight plausibility scoring (pure NumPy) + template notebook**

**Why**
- Add the second, **physics-inspired** line of evidence without heavy deps.
- Keep CI fast; notebooks remain optional.

**Changes**
- `src/zexplorer/hydro/hand_utils.py` with:
  - `relative_hand(dem)` — toy HAND-like relative elevation
  - `plausibility_score(delta_db, hand, candidate_mask)` — score in [0,1]
- `docs/HYDRO_NOTES.md` — usage notes and upgrade path
- `notebooks/12_HAND_plausibility_template.ipynb` — minimal example with dummy arrays

**Notes**
- No new runtime deps required; uses NumPy (SciPy optional for `relative_hand`). 
- Safe for CI since notebooks aren’t executed.
