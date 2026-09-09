import math
import csv #for csv reading


class Point:
    def __init__(self, id, lon, lat, name=None, tag=None):
        # Validate the longitude and latitude values
        # Note that validation must happen before assigning the values to the instance variables
        if not (180.0 >= lon >= -180.0):
            raise ValueError("Longitude must be between -180 and 180 degrees.")
        if not (90.0 >= lat >= -90.0):
            raise ValueError("Latitude must be between -90 and 90 degrees.")
        
        self.id = id
        self.lon = lon
        self.lat = lat
        self.name = name
        self.tag = tag

    def to_tuple(self) -> tuple[float, float]:
        """
        Return the coordinate as a (lon, lat) tuple.
        """
        return (self.lon, self.lat)

    @staticmethod #a decorator to indicate that this method does not depend on the instance of the class
    def haversine_m(lon1:float, lat1:float, lon2:float, lat2:float)-> float:
        """
        Calculate the haversine distance between two points on the earth
        specified in decimal degrees.
        Returns the distance in meters.
        """
        # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        # Radius of earth in meters
        r = 6371000.0
        
        return c * r

    def distance_to(self, other):
        return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)

    @classmethod
    def from_row(cls,row):
        '''
        Create a Point object from a row of data.'''
        return cls(id=str(row["id"]), 
                   lon=float(row["lon"]),
                   lat=float(row["lat"]),
                   name=row.get("name"),
                   tag=row.get("tag")
                   )
    def is_poi(self):
        return (self.tag or "").lower() == "poi"

class PointSet:
    def __init__(self, points=None):
        #Store the points in a list. If no points are provided, initialize an empty list.
        self.points = list(points) if points is not None else []

    @classmethod
    def from_csv(cls, path: str):
        #Read points from a CSV file and return a Pointset object.
        points = []
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Delegate validation and object creation directly to Point.from_row
                    point = Point.from_row(row)
                    points.append(point)
                except (ValueError, KeyError, TypeError):
                    # Gracefully skip rows with invalid data/coordinates or missing keys
                    continue
        return cls(points)

    def count(self)-> int:
        #Return the number of points in the Pointset.
        return len(self.points)

    def bbox(self)-> tuple[float, float, float, float]:
        
        #Calculate the bounding box of the points in the Pointset.
        #Returns a tuple of (min_lon, min_lat, max_lon, max_lat).
        if not self.points:
            raise ValueError("Pointset is empty. Cannot calculate bounding box.")
        
        min_lon = min(point.lon for point in self.points)
        max_lon = max(point.lon for point in self.points)
        min_lat = min(point.lat for point in self.points)
        max_lat = max(point.lat for point in self.points)
        
        return (min_lon, min_lat, max_lon, max_lat)

    def filter_by_tag(self, tag: str):
     
        #Filter points by a specific tag.
        #Returns a new Pointset containing only the points with the specified tag.
        
        filtered_points = [point for point in self.points if (point.tag or "").lower() == tag.lower()]
        return PointSet(filtered_points)