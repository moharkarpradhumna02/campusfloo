import csv
import os
from typing import Dict, Any

def load_historical_segments(csv_path: str) -> Dict[str, Dict[str, Any]]:
    segments = {}
    if not os.path.exists(csv_path):
        return segments
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            segments[row["segment_id"]] = {
                "from_stop": row["from_stop"],
                "to_stop": row["to_stop"],
                "distance_meters": float(row["distance_meters"]),
                "median_time_sec": float(row["median_time_sec"]),
                "p85_time_sec": float(row["p85_time_sec"])
            }
    return segments
