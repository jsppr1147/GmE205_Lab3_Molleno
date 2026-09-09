from spatial import Point, PointSet

# --- Point checks ---
p = Point("0", 121.0, 14.0)
#print(p.id, p.lon, p.lat)
#print(p.to_tuple())
#print(p.geometry.geom_type)

q = Point("1", 121.05, 14.05)
#print(f"Distance between p and q: {p.distance_to(q):.2f} meters")
coordinate_distance = p.geometry.distance(q.geometry)
#print(f"Coordinate distance between p and q: {coordinate_distance:.6f}")

#Part C Point checks
#for valid record..
valid_record = {"id": "A", "lon": 121.0, "lat": 14.6, "name": "Gate", "tag": "POI"}
p = Point.from_dict(valid_record)
print(p.as_dict())

# testing for invalid record 
invalid_record = {"id": "B", "lon": 999, "lat": 14.6}

try:
    bad = Point.from_dict(invalid_record)
except ValueError as exc:
    print(f"Invalid record correctly rejected: {exc}")

# --- PointSet checks ---
CSV_PATH = "data/points.csv"  # relative path

ps = PointSet.from_csv(CSV_PATH)
#print(f"Loaded {ps.count()} points.")

bbox = ps.bbox()
#print(f"Bounding box: {bbox}")

poi_set = ps.filter_by_tag("poi")
#print(f"POI count: {poi_set.count()}")