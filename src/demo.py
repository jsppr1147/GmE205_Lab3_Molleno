from spatial import Point, PointSet

# --- Point checks (Part B) ---
p = Point("0", 121.0, 14.0)
print(p.id, p.lon, p.lat)
print(p.to_tuple())

q = Point("1", 121.05, 14.05)
print(f"Distance between p and q: {p.distance_to(q):.2f} meters")

# --- Pointset checks ---
CSV_PATH = "data/points.csv"  # relative path

ps = PointSet.from_csv(CSV_PATH)
print(f"Loaded {ps.count()} points.")

bbox = ps.bbox()
print(f"Bounding box: {bbox}")

poi_set = ps.filter_by_tag("poi")
print(f"POI count: {poi_set.count()}")