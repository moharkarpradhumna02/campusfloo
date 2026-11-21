# API Reference — ShuttleSense H4

### REST Endpoints

#### 1. Ingest GPS Ping
`POST /gps`
- **Body:**
```json
{
  "vehicle_id": "A1",
  "lat": 31.2548,
  "lon": 75.7052,
  "speed": 5.8,
  "heading": 120.0,
  "accuracy": 12.0,
  "timestamp": 1700000000.0
}
```
- **Response:**
```json
{
  "status": "accepted",
  "vehicle_id": "A1",
  "clean": true,
  "matched_lat": 31.25482,
  "matched_lon": 75.70518,
  "route_distance": 450.2,
  "confidence": 0.94,
  "rejection_reason": null
}
```

#### 2. Get Live Vehicle ETA
`GET /eta/{vehicle_id}`
- **Response:**
```json
{
  "vehicle_id": "A1",
  "lat": 31.25482,
  "lon": 75.70518,
  "heading": 120.0,
  "speed_kmh": 20.8,
  "age_seconds": 2.4,
  "in_dropout": false,
  "etas": [
    {
      "stop_id": 1,
      "stop_name": "Admin Block",
      "distance_meters": 240.5,
      "eta_seconds": 45,
      "eta_minutes": 1,
      "delay_seconds": 0,
      "is_delayed": false
    }
  ]
}
```

#### 3. Get Stops
`GET /stops`

### WebSocket
`WS /ws`
Streams real-time `{type: "VEHICLE_UPDATE", vehicle_id, matched_lat, matched_lon, etas, alert}` updates.
