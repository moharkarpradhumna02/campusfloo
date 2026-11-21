import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .utils.geo import PolylineRoute
from .services.gps_cleaner import GPSCleaner
from .services.map_matcher import HMMMapMatcher
from .services.eta_engine import ETAEngine
from .services.delay_detector import DelayDetector
from .api.routes_gps import create_gps_router
from .api.routes_eta import create_eta_router
from .api.routes_stops import create_stops_router
from .api.websocket import ConnectionManager
from .api.auth import auth_router

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load route geometry & stops
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(os.path.dirname(base_dir), "data", "routes")

route_file = os.path.join(data_dir, "campus_route.geojson")
stops_file = os.path.join(data_dir, "stops.geojson")

with open(route_file, "r") as f:
    route_json = json.load(f)

# Extract coordinates: GeoJSON stores [lon, lat] -> convert to (lat, lon)
pts_raw = route_json["features"][0]["geometry"]["coordinates"]
polyline_coords = [(p[1], p[0]) for p in pts_raw]
route = PolylineRoute(polyline_coords)

with open(stops_file, "r") as f:
    stops_json = json.load(f)

stops_list = []
for feat in stops_json["features"]:
    p = feat["geometry"]["coordinates"]
    proj = route.project_point((p[1], p[0]))
    stops_list.append({
        "id": feat["properties"]["id"],
        "name": feat["properties"]["name"],
        "code": feat["properties"].get("code", ""),
        "emoji": feat["properties"].get("emoji", "📍"),
        "lat": p[1],
        "lon": p[0],
        "route_distance": proj["route_distance"],
        "dwell_sec": feat["properties"].get("dwell_time_sec", 18.0)
    })

stops_list.sort(key=lambda s: s["route_distance"])

# Initialize pipeline services
cleaner = GPSCleaner(max_accuracy_threshold=settings.MAX_GPS_ACCURACY_M, max_speed_kmh=settings.MAX_SPEED_KMH)
matcher = HMMMapMatcher(route)
eta_engine = ETAEngine(route, stops_list)
delay_detector = DelayDetector(delay_threshold_seconds=180.0)
broadcaster = ConnectionManager()

# Include routers
app.include_router(auth_router)
app.include_router(create_gps_router(cleaner, matcher, eta_engine, delay_detector, broadcaster))
app.include_router(create_eta_router(eta_engine, route))
app.include_router(create_stops_router(stops_list))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await broadcaster.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        broadcaster.disconnect(websocket)

@app.get("/")
def read_root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "online",
        "accuracy_target": "±2 min for ≥ 80% predictions",
        "dropouts_survived": "120s via dead-reckoning"
    }
