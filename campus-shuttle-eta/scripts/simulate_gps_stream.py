import time
import math
import random
import json
import os
import requests

def stream_simulation(api_url="http://localhost:8000/gps", interval_sec=2.0):
    print(f"Starting GPS simulation stream to {api_url}...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    route_file = os.path.join(base_dir, "data", "routes", "campus_route.geojson")

    with open(route_file, "r") as f:
        data = json.load(f)
    coords = [(p[1], p[0]) for p in data["features"][0]["geometry"]["coordinates"]]

    step_idx = 0
    t = time.time()
    in_blackout = False
    blackout_end = 0

    while True:
        now = time.time()
        # Random blackout simulation
        if not in_blackout and random.random() < 0.02:
            in_blackout = True
            blackout_end = now + random.uniform(30, 90)
            print(f"[SIMULATOR] 🛰️ Simulating GPS dropout for {int(blackout_end - now)}s...")

        if in_blackout:
            if now > blackout_end:
                in_blackout = False
                print("[SIMULATOR] 🛰️ GPS Signal recovered!")
            else:
                time.sleep(interval_sec)
                continue

        p = coords[step_idx % len(coords)]
        step_idx += 1

        # Add Gaussian noise
        lat = p[0] + random.gauss(0, 0.00005)
        lon = p[1] + random.gauss(0, 0.00005)
        speed = max(0.0, 5.8 + random.uniform(-1.0, 1.0))
        accuracy = random.uniform(5.0, 20.0)

        payload = {
            "vehicle_id": "A1",
            "lat": lat,
            "lon": lon,
            "speed": speed,
            "heading": 90.0,
            "accuracy": accuracy,
            "timestamp": now
        }

        try:
            resp = requests.post(api_url, json=payload, timeout=2.0)
            res_data = resp.json()
            print(f"[{time.strftime('%X')}] Ping sent -> Status: {res_data.get('status')} | Clean: {res_data.get('clean')}")
        except Exception as e:
            print(f"[{time.strftime('%X')}] Failed to send ping (backend offline?): {e}")

        time.sleep(interval_sec)

if __name__ == "__main__":
    stream_simulation()
