from fastapi import APIRouter, HTTPException, Depends
from ..models.schemas import RawGPSPing, IngestResponse

def create_gps_router(cleaner, matcher, eta_engine, delay_detector, broadcaster):
    router = APIRouter(prefix="/gps", tags=["GPS Ingest"])

    @router.post("", response_model=IngestResponse)
    async def ingest_gps_ping(ping: RawGPSPing):
        # 1. Clean ping
        is_clean, clean_coords, reason = cleaner.clean_ping(
            vehicle_id=ping.vehicle_id,
            lat=ping.lat,
            lon=ping.lon,
            speed_mps=ping.speed,
            timestamp=ping.timestamp,
            accuracy_m=ping.accuracy or 10.0
        )

        if not is_clean:
            return IngestResponse(
                status="rejected",
                vehicle_id=ping.vehicle_id,
                clean=False,
                rejection_reason=reason
            )

        # 2. Map-match
        match_result = matcher.match(
            vehicle_id=ping.vehicle_id,
            lat=clean_coords[0],
            lon=clean_coords[1],
            timestamp=ping.timestamp,
            speed_mps=ping.speed
        )

        # 3. Update ETA engine
        eta_engine.update_vehicle_fix(
            vehicle_id=ping.vehicle_id,
            matched_s=match_result["route_distance"],
            speed_mps=ping.speed,
            timestamp=ping.timestamp
        )

        # 4. Compute ETAs & check delay
        etas = eta_engine.compute_stop_etas(ping.vehicle_id, ping.timestamp)
        alert = delay_detector.check_delay(ping.vehicle_id, f"Shuttle {ping.vehicle_id}", etas)

        # 5. Broadcast to WebSockets
        payload = {
            "type": "VEHICLE_UPDATE",
            "vehicle_id": ping.vehicle_id,
            "matched_lat": match_result["matched_lat"],
            "matched_lon": match_result["matched_lon"],
            "heading": match_result["heading"],
            "speed_kmh": round(ping.speed * 3.6, 1),
            "confidence": match_result["confidence"],
            "etas": etas,
            "alert": alert
        }
        await broadcaster.broadcast(payload)

        return IngestResponse(
            status="accepted",
            vehicle_id=ping.vehicle_id,
            clean=True,
            matched_lat=match_result["matched_lat"],
            matched_lon=match_result["matched_lon"],
            route_distance=match_result["route_distance"],
            confidence=match_result["confidence"],
            rejection_reason=None
        )

    return router
