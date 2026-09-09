GmE 205 Laboratory Exercise 5: Spatial Object Systems in Python  

This laboratory exercise utilizes the previous exercise on designing a Point and Pointset. It refactors the implementation where the geometry becomes a Shapely object, common spatial behavior moves to SpatialObject class, and objects gain clean data-input and output boundaries.  

This exercise is consisted of 8 Parts (A-H): 

Part A: Setting up the environment and the reproducible workspace  
- The folder structure similar to the previous exercise was created.  
- Virtual environment was created adn the python intepreter inside it was selected.  
- The required libraries were installed. Similar to the previous exercise but with the addition of shapely library.  
- A git was initialized and the first commit for the READMe.md file was uploaded in the repository.
- The script was overhauled to fit the Lab 3 exercise.  

Part B: Refactoring Point geometry to become a shapely object  
- Point validates the coordinates in one place.  
- Changed now so that point stores a shapely object.  
- p.lon and p.lat is still working through properties.  
- to.tuple() works the same but with different input geometry values.  
- distance_to works fine but it is noted that it is different from coordinate_distance in geometry.  
- demo.py runs works properly. 

Part C: Structuring data boundaries: Dictionary -> Object -> Dictionary  
- A classmethod was created to construct Point from a dictionary data.  
- The from_dict() method passes to the class Point method which allows it to validate the point in the __init__. Thus checks it for the "single truth validation" of this class.  
- The as_dict() method returns the JSON-ready values of the point. It doesnt return a live shapely geometry object.  
- A test for invalid and valid data (lon=999) was created for checking whether it works or not.  

Part D: Creating a shared spatial abstraction: SpatialObject  
- Created a class called "SpatialObject" for storing geometries and implementing simple methods bbox() and intersect() 
- Refactored the Point class to inherit the "SpatialObject" behavior
- Point uses the super().__init__(geometry) to call the initialization of the SpatialObject on the geometry (lat,lon) attribute.  
- demo.py now have lines to checking whether bbox() work without duplicating it on Point class.  

Part E: Creating another Spatial Type (Class Parcel)  
- A starter class was created which inherits the SpatialObject class and uses a dictionary from structured parcel attributes (JSON).  
- Similar to Part C, the as_dict method is implemented to return the parcel_id, bbox() and attributes in primitive format / JSON-ready values. It doesnt return the shapely object.  
- the demo.py is updated to check for functionality of the Parcel class.  
- the import section was updated. the polygon from shapely was imported.  
- An arbitrary polygon is added to check if Parcel class is working fine.  
- Additional points were also added to check whether in the method implementation is inherited properly from the SpatialObject. This is a good practice so the responsibility is distributed and placed properly to also avoid duplication of implementation is different classes.  

Part F: Creating a specific runner script, structured outputs, and simple visualization  
- a runner for this lab was created with goal demonstrating that the runner can orchestrate output and the domain classes should remain reusable.  
- a specific json format and runner structure was followed for this exercise.  
- instead of importing to showcase runner. a similar approach to the demo.py was taken in constructing polygons and point which is used for the goals of this exercise.  
- the evaluation was done by implementing the intersection method in the SpatialObject class.  
- the JSON was created to export all the data result for the constructed data relationships.  
- the visualization was done using a function for preview of the points and polygons using matplotlib. 
    >the parcel polygon was drawn using its exterior coordinates (parcel.geometry.xy)
    >the points were labelled using scatter and annotations 
    

Part G: Testing and Debugging  
- using the test_spatial.py, a series of tests were created to check if the spatial.py works and handles its functions properly.  
- the pytest.py module was used for this exercise in debugging. Although there is a unittest available, I find it easier to used the pytest due to its syntax which is simple and direct to the test I want.  
- The labex recommended to create 10 tests for this exercise and the spatial.py successfully passed all of it while avoiding the broad suppresion.  
- a pytest.ini was created so that the pytest can also import from the src folder.  
- the outputs regenerate cleanly after using terminal: pip install -r requirements.txt  
- Focused tests PASSED  [TO RUN in terminal. pytest tests\test_spatial.py -v]  


PART H: CHALLENGES (All challenges were successfully handled)
1. Point.from_dict(d) -- this parses the id, lon, lat, & name/tag (optional) and delegates all validation to the Point class without duplicate checking.  
2. Point.as_dict() and Parcel.as_dict() -- both returns only the primitives (strings, floats, list, dicts) with no live shapely objects. NOTE: there is also a test for this on the test_spatial.py (the test_point_as_dict_contains_no_live_shapely_objects)  
3. The relationship 'Intersects' lives only on the SpatialObject class. Both the Point and Parcel class inherit it without re-defining it in their respective classes (also in test_spatial.py). I think these are the test to check if two SpatialObject intersect or not.  
4. EXPLANATION ON THE DISTANCE DECISION. 
Shapely's distance() was not used to replace the Lab 2 Haversine method because Shapely treats every geometry as existing on a flat Cartesian plane. It has no awareness that longitude and latitude represent positions on a curved Earth surface, so the number it returns is a raw coordinate-unit difference, not a real-world distance.

In this project, Shapely is responsible for pure geometric shape math: computing bounding boxes and testing intersection(topology) between geometries. These operations are correct regardless of what the coordinates represent, because they only ask geometric questions ("does this shape overlap that shape?"), not questions about real-world meaning.

Coordinate meaning — specifically, that lon/lat values represent locations on Earth's curved surface remains the responsibility of the Point class and its Haversine implementation. Unlike Shapely, Haversine explicitly accounts for Earth's radius and curvature, converting angular coordinate differences into an actual physical distance in meters.  

[REFLECTIONS ANSWERS]

1. REFACTORING: The representation of Points changed from plain floats (self.lat/self.lon) to a Shapely object (self.geometry). Because of the @property wrappers, existing methods and instances continued to work identically to the previous lab exercise. This stability is visible in that no other method in Point, nor any code in run_lab2.py or run_lab3.py, needed to change even after the internal representation changed.

2. RESPONSIBILITY: SpatialObject owns geometry storage plus bbox() and intersects(). Point owns coordinate validation, id/name/tag, and Haversine distance. Parcel owns parcel_id and its attributes. intersects() lives only in SpatialObject and is inherited by both Point and Parcel, so there is no need to duplicate the method in either subclass. They both rely on SpatialObject handling the geometry comparison generically.

3. DATA BOUNDARY: from_dict() delegates to the constructor instead of re-validating because having two places enforce the same validation rule risks them drifting out of sync if one is updated and the other isn't. It's best to have a single source of truth.

4. OUTPUT BOUNDARY: as_dict() returns only primitives because JSON cannot serialize a live Shapely object. It also means a reader of the JSON report doesn't need Shapely installed just to read the output.

5. INHERITANCE: intersects() lives in SpatialObject so that a future fix or behavior change only has to happen in one place. If it were duplicated separately inside Point and Parcel, the two copies could drift apart over time as one gets updated and the other doesn't. The same single-source-of-truth reasoning as #3.

6. COORDINATE MEANING: Similar to the explanation in Challenge 4, Shapely only computes the geometric aspect of objects. It doesn't account for the reference system or Earth's actual size, so its output has no real-world meaning on its own.

7. SCALE: Inheriting from SpatialObject gives every subclass bbox() and intersects() for free, which helps code organization and correctness as the model grows to new geometry types. However, it doesn't address performance at scale. Loading millions of points with a plain Python for-loop over a CSV is single-threaded and memory-bound, and checking intersects() against every object one-by-one doesn't scale either. Solving that would need different techniques entirely such as spatial indexing to avoid brute-force comparisons, or moving from an in-memory PointSet to a proper spatial database.