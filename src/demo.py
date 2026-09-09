from spatial import Point
from spatial import Pointset

#p = Point("0", 121.0, 14.0)
#print(p.id, p.lon, p.lat)

#q = Point("1", -75.0, 140.0)
#print(q.id, q.lon, q.lat)

#print(p.coordinates())

#testing pointset
csv_path = "C:\\Users\\Jasper\\Documents\\1st Sem 26_27\\Programming Class\\GmE 205 Laboratory 2 - Simple Spatial Object in Python\\GmE205_Lab2_Molleno\\data\\points.csv"
ps = Pointset.from_csv(csv_path)
#print (ps.count())
#bounding box check
#a, b, c, d = ps.bbox()
#print(f"Bounding box: ({a}, {b}, {c}, {d})")
#filter by tag check
#poi_set = ps.filter_by_tag("poi")
#print(poi_set.count())

distance = ps.points[0].distance_to(ps.points[1])
print(f"Distance between point 0 and point 1: {distance} meters")