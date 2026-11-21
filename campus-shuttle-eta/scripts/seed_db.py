import json
import math
import random
import csv

# Campus center (IIT / NIT style campus)
CENTER_LAT = 31.2548
CENTER_LNG = 75.7052

STOPS_DATA = [
    {"id": 0, "name": "Main Gate", "code": "MG", "emoji": "🚪", "offset": [-0.0045, -0.0030], "dwell": 20},
    {"id": 1, "name": "Admin Block", "code": "AB", "emoji": "🏛️", "offset": [-0.0020, -0.0035], "dwell": 15},
    {"id": 2, "name": "Central Library", "code": "CL", "emoji": "📚", "offset": [0.0005, -0.0030], "dwell": 20},
    {"id": 3, "name": "Hostel Quadrangle", "code": "HQ", "emoji": "🛏️", "offset": [0.0035, -0.0020], "dwell": 25},
    {"id": 4, "name": "Innovation Hub & Labs", "code": "IH", "emoji": "💡", "offset": [0.0045, 0.0015], "dwell": 20},
    {"id": 5, "name": "Sports Complex", "code": "SC", "emoji": "🏟️", "offset": [0.0020, 0.0045], "dwell": 15},
    {"id": 6, "name": "Student Activity & Food Court", "code": "FC", "emoji": "🍜", "offset": [-0.0010, 0.0040], "dwell": 25},
    {"id": 7, "name": "Medical Center", "code": "MC", "emoji": "🏥", "offset": [-0.0038, 0.0020], "dwell": 15}
]

# Generate stops GeoJSON
stops_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": s["id"],
                "name": s["name"],
                "code": s["code"],
                "emoji": s["emoji"],
                "dwell_time_sec": s["dwell"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [round(CENTER_LNG + s["offset"][1], 6), round(CENTER_LAT + s["offset"][0], 6)]
            }
        }
        for s in STOPS_DATA
    ]
}

with open("campus-shuttle-eta/data/routes/stops.geojson", "w") as f:
    json.dump(stops_geojson, f, indent=2)

# Generate route polyline with intermediate points
route_pts = []
stop_coords = [s["geometry"]["coordinates"] for s in stops_geojson["features"]]
for i in range(len(stop_coords)):
    p1 = stop_coords[i]
    p2 = stop_coords[(i + 1) % len(stop_coords)]
    steps = 15
    for k in range(steps):
        t = k / steps
        lng = p1[0] + t * (p2[0] - p1[0])
        lat = p1[1] + t * (p2[1] - p1[1])
        # subtle curved perturbation
        curve = math.sin(t * math.pi) * 0.0003
        route_pts.append([round(lng + curve, 6), round(lat + curve, 6)])

route_pts.append(route_pts[0])

route_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": "A",
                "name": "Green Loop",
                "color": "#10b981",
                "total_stops": 8,
                "loop": True
            },
            "geometry": {
                "type": "LineString",
                "coordinates": route_pts
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "B",
                "name": "Blue Express",
                "color": "#3b82f6",
                "total_stops": 4,
                "loop": True
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [stop_coords[0], stop_coords[2], stop_coords[4], stop_coords[6], stop_coords[0]]
            }
        }
    ]
}

with open("campus-shuttle-eta/data/routes/campus_route.geojson", "w") as f:
    json.dump(route_geojson, f, indent=2)

# Generate historical segment times
with open("campus-shuttle-eta/data/sample_gps/historical_segment_times.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["segment_id", "from_stop", "to_stop", "distance_meters", "median_time_sec", "p85_time_sec"])
    for i in range(len(STOPS_DATA)):
        s1 = STOPS_DATA[i]
        s2 = STOPS_DATA[(i + 1) % len(STOPS_DATA)]
        dx = (s2["offset"][1] - s1["offset"][1]) * 111320 * math.cos(math.radians(CENTER_LAT))
        dy = (s2["offset"][0] - s1["offset"][0]) * 111320
        dist = math.hypot(dx, dy)
        avg_speed = 5.8  # m/s ~ 21 km/h
        travel_sec = round(dist / avg_speed)
        writer.writerow([f"seg_{i}_{s1['code']}_{s2['code']}", s1["name"], s2["name"], round(dist), travel_sec, round(travel_sec * 1.25)])

print("Data files generated successfully.")
