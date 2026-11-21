from pydantic import BaseModel, Field
from typing import List, Optional

class RawGPSPing(BaseModel):
    vehicle_id: str
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    speed: float = Field(0.0, ge=0.0)
    heading: Optional[float] = 0.0
    accuracy: Optional[float] = 10.0
    timestamp: float

class IngestResponse(BaseModel):
    status: str
    vehicle_id: str
    clean: bool
    matched_lat: Optional[float] = None
    matched_lon: Optional[float] = None
    route_distance: Optional[float] = None
    confidence: Optional[float] = None
    rejection_reason: Optional[str] = None

class StopETA(BaseModel):
    stop_id: int
    stop_name: str
    stop_code: str
    distance_meters: float
    eta_seconds: int
    eta_minutes: int
    delay_seconds: int
    is_delayed: bool

class VehicleStatus(BaseModel):
    vehicle_id: str
    name: str
    route_id: str
    lat: float
    lon: float
    heading: float
    speed_kmh: float
    last_fix_age_sec: float
    is_in_dropout: bool
    is_delayed: bool
    etas: List[StopETA]

class StopItem(BaseModel):
    id: int
    name: str
    code: str
    lat: float
    lon: float
    emoji: str
