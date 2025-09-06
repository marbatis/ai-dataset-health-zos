import math
import pytest

from zexplorer.geoutils import bbox_from_center

def test_invalid_latitude_raises():
    with pytest.raises(ValueError):
        bbox_from_center(85.0, 0.0, 1000.0)
    with pytest.raises(ValueError):
        bbox_from_center(-90.0, 0.0, 1000.0)

def test_invalid_half_size_raises():
    with pytest.raises(ValueError):
        bbox_from_center(0.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        bbox_from_center(0.0, 0.0, -1.0)
    with pytest.raises(ValueError):
        bbox_from_center(0.0, 0.0, 6_000_000.0)

def test_near_cap_is_finite():
    # Just under the cap; should produce finite results
    bbox = bbox_from_center(84.999, 10.0, 100_000.0)
    assert all(map(math.isfinite, bbox)), "bbox values should be finite"

