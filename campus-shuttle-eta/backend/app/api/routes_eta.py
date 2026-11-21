from fastapi import APIRouter, HTTPException
import time

def create_eta_router(eta_engine, route):
    router = APIRouter(prefix="/eta", tags=["ETAs"])

    @router.get("/{vehicle_id}")
    async def get_vehicle_eta(vehicle_id: str):
        now = time.time()
        if vehicle_id not in eta_engine.vehicles:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        etas = eta_engine.compute_stop_etas(vehicle_id, now)
        dr = eta_engine.dead_reckon_to(vehicle_id, now)
        pos, hd = route.get_position_at_distance(dr["s"])
        return {
            "vehicle_id": vehicle_id,
            "lat": pos[0],
            "lon": pos[1],
            "heading": hd,
            "speed_kmh": round(dr["v"] * 3.6, 1),
            "age_seconds": round(dr["age"], 1),
            "in_dropout": dr["in_dropout"],
            "etas": etas
        }

    return router
