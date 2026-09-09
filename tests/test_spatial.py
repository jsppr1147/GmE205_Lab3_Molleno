import pytest
from shapely.geometry import Polygon
from spatial import Point, Parcel

## to check. In terminal: pytest tests\test_spatial.py -v
# ------------------------------------------------------------------
# Point construction and validation
# ------------------------------------------------------------------

def test_valid_point_can_be_constructed():
    #checking if point can be constructed with valid parameters
    p = Point("A", 121.0, 14.6)
    assert p.id == "A"
    assert p.lon == 121.0
    assert p.lat == 14.6


def test_invalid_longitude_raises_value_error():
    #checking if invalid longitude raises ValueError
    with pytest.raises(ValueError):
        Point("BAD", 999, 14.6)


# ------------------------------------------------------------------
# Data boundary: from_dict
# ------------------------------------------------------------------

def test_from_dict_creates_point_from_valid_record():
    #checking if point can be created from a valid dictionary record
    record = {"id": "A", "lon": 121.0, "lat": 14.6, "name": "Gate", "tag": "POI"}
    p = Point.from_dict(record)
    assert p.id == "A"
    assert p.lon == 121.0
    assert p.tag == "POI"


def test_from_dict_fails_through_constructor_validation():
    #checking if invalid dictionary record raises ValueError
    record = {"id": "BAD", "lon": 999, "lat": 14.6}
    with pytest.raises(ValueError):
        Point.from_dict(record)


# ------------------------------------------------------------------
# bbox — shared SpatialObject behavior
# ------------------------------------------------------------------

def test_point_bbox_is_correct():
    p = Point("A", 121.0, 14.6)
    assert p.bbox() == (121.0, 14.6, 121.0, 14.6)


def test_parcel_bbox_is_correct():
    geom = Polygon([(0, 0), (10, 0), (10, 5), (0, 5)])
    parcel = Parcel(101, geom, {"zone": "Residential"})
    assert parcel.bbox() == (0.0, 0.0, 10.0, 5.0)


# ------------------------------------------------------------------
# intersects — shared SpatialObject behavior
# ------------------------------------------------------------------

def test_inside_point_intersects_parcel():
    #checking if a point inside a parcel intersects with the parcel
    geom = Polygon([(0, 0), (10, 0), (10, 5), (0, 5)])
    parcel = Parcel(101, geom, {"zone": "Residential"})
    inside = Point("IN", 2, 2)
    assert inside.intersects(parcel) is True


def test_outside_point_does_not_intersect_parcel():
    #checking if a point is outside of the parcel
    geom = Polygon([(0, 0), (10, 0), (10, 5), (0, 5)])
    parcel = Parcel(101, geom, {"zone": "Residential"})
    outside = Point("OUT", 12, 2)
    assert outside.intersects(parcel) is False


# ------------------------------------------------------------------
# Output boundary: as_dict contains no live Shapely objects
# ------------------------------------------------------------------

def test_point_as_dict_contains_no_live_shapely_objects():
    p = Point("A", 121.0, 14.6, name="Gate", tag="POI")
    result = p.as_dict()
    for value in result.values():
        assert not hasattr(value, "geom_type")  # Shapely geometries all have this attribute