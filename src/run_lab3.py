import os
import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from spatial import Point, Parcel

OUTPUT_DIR = "output"
REPORT_PATH = os.path.join(OUTPUT_DIR, "lab3_report.json") #joins the output directory and report path to create a full path for the report file
PLOT_PATH = os.path.join(OUTPUT_DIR, "lab3_preview.png")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Construct objects (same objects used in demo.py, Part E) ---
    attributes = {"area": 42.8, "zone": "Residential", "is_active": True}
    #creating a square polygon for the parcel geometry using shapely's Polygon class
    sq_geom = Polygon([(0, 0), 
                    (10, 0), 
                    (10, 10), 
                    (0, 10)])

    parcel = Parcel(101, sq_geom, attributes)

    p1 = Point("ME", 2, 2)
    p2 = Point("YOU", 12, 2)

    # --- Evaluate relationships pertaining to SpatialObject.intersects ---
    inside_intersects = p1.intersects(parcel)
    outside_intersects = p2.intersects(parcel)

    # --- Build report dictionary from each object's own as_dict() ---
    report = {
        "p1": p1.as_dict(),
        "p2": p2.as_dict(),
        "parcel": parcel.as_dict(),
        "relationships": {
            "p1_intersects_parcel": inside_intersects,
            "p2_intersects_parcel": outside_intersects,
        },
    }

    # --- Write JSON ---
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2) #Write the report dictionary to a JSON file with indentation for readability

    # --- Create preview figure ---
    _plot_preview(parcel, p1, p2, PLOT_PATH)


def _plot_preview(parcel, inside, outside, output_path):
    """
    Visualization of runner lab3.py, Part E. Shows the parcel polygon and two points (one inside, one outside).
    """
    fig, ax = plt.subplots(figsize=(6, 5))

    # Draw the parcel polygon using its exterior coordinates
    px, py = parcel.geometry.exterior.xy
    ax.fill(px, py, alpha=0.3, edgecolor="black", label="Parcel")

    # Draw the two points, labeled
    ax.scatter(inside.lon, inside.lat, color="green", zorder=5) #scatterplot (x,y, color, order of drawing)
    ax.annotate("inside", (inside.lon, inside.lat), textcoords="offset points", xytext=(5, 5)) #annotation (text, x, y, textcoords, offset label)

    ax.scatter(outside.lon, outside.lat, color="red", zorder=5)
    ax.annotate("outside", (outside.lon, outside.lat), textcoords="offset points", xytext=(5, 5))

    ax.set_title("Parcel with Inside/Outside Points")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="best")
    ax.grid(True)

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()