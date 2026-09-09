#runner script for lab2

import os
import json
import matplotlib.pyplot as plt
from spatial import Pointset

DATA_PATH = "data/points.csv"
OUTPUT_DIR = "output"
REPORT_PATH = os.path.join(OUTPUT_DIR, "lab2_report.json")
PLOT_PATH = os.path.join(OUTPUT_DIR, "lab2_preview.png")

#A bit extra
#Filtering of which tags to plot

TARGET_TAGS = None #None means all tags will be plotted #set it to ["poi", "restaurant"] to filter only those tags
def main():
    #Making sure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    #Pointset from CSV similar to the demo kanina
    ps = Pointset.from_csv(DATA_PATH)
    #print(f"Loaded {ps.count()} points.")
    bbox = ps.bbox()

    #Updated tag counting 
    tagged_points = {}
    for point in ps.points:
        tag = point.tag or "untagged"

        #Applying the filter if TARGET_TAGS is set
        if TARGET_TAGS is not None and tag not in TARGET_TAGS:
            continue

        tagged_points.setdefault(tag, []).append(point)


    tag_counts = {tag: len(points) for tag, points in tagged_points.items()}
    total_count = sum(tag_counts.values())


    #for the json summary formatting
    summary = { 
        "total_point_counts": ps.count(),
        "bounding_box": {
            "min_lon": bbox[0],
            "min_lat": bbox[1],
            "max_lon": bbox[2],
            "max_lat": bbox[3]
        },
        "tag_counts": tag_counts
    }

    with open(REPORT_PATH, "w",encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


    #PLOTTING LIKE PREVIOUS LAB
    plt.figure(figsize=(8, 6))
    if not tagged_points:
        plt.title("No points to display")
    else:
        # Loop through each tag and plot its points with a distinct color automatically
        for tag, points in tagged_points.items():
            tag_lons = [p.lon for p in points]
            tag_lats = [p.lat for p in points]

            plt.scatter(
                tag_lons, tag_lats, label=tag, alpha=0.7, edgecolors="k"
            )

        plt.title("Pointset Preview by Tag")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        plt.legend(title="Tags", loc="best")

    plt.savefig(PLOT_PATH, dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()