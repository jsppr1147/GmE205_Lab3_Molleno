# runner script for lab2

import os
import json
import matplotlib.pyplot as plt
from spatial import PointSet

DATA_PATH = "data/points.csv"
OUTPUT_DIR = "output"
REPORT_PATH = os.path.join(OUTPUT_DIR, "lab2_report.json")
PLOT_PATH = os.path.join(OUTPUT_DIR, "lab2_preview.png")

# Set to a list like ["poi", "restaurant"] to only report/plot those tags.
# None means every tag (including untagged points) is included.
TARGET_TAGS = None

SHOW_PLOT = False


def _group_by_tag(pointset, target_tags=None):
    """
    Runner-local helper: groups a Pointset's points by tag. This is a reporting/
    visualization concern, not a spatial responsibility, so it stays here
    rather than inside Pointset itself.
    """
    grouped = {}
    for point in pointset.points:
        tag = point.tag or "untagged"
        if target_tags is not None and tag not in target_tags:
            continue
        grouped.setdefault(tag, []).append(point)
    return grouped


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ps = PointSet.from_csv(DATA_PATH)
    bbox = ps.bbox()

    tagged_points = _group_by_tag(ps, TARGET_TAGS)
    tag_counts = {tag: len(points) for tag, points in tagged_points.items()}

    summary = {
        "total_point_count": ps.count(),
        "filtered_point_count": sum(tag_counts.values()),
        "bounding_box": {
            "min_lon": bbox[0],
            "min_lat": bbox[1],
            "max_lon": bbox[2],
            "max_lat": bbox[3],
        },
        "tag_counts": tag_counts,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    _plot_by_tag(tagged_points, PLOT_PATH, show=SHOW_PLOT)


def _plot_by_tag(tagged_points, output_path, show=False):
    plt.figure(figsize=(8, 6))

    if not tagged_points:
        plt.title("No points to display")
    else:
        for tag, points in tagged_points.items():
            lons = [p.lon for p in points]
            lats = [p.lat for p in points]
            plt.scatter(lons, lats, label=tag, alpha=0.7, edgecolors="k")

        plt.title("Pointset Preview by Tag")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        plt.legend(title="Tags", loc="best")

    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":
    main()