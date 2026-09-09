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

