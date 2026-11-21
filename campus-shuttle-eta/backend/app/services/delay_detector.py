from typing import List, Dict, Any, Optional

class DelayDetector:
    """
    Monitors vehicle progress and triggers alerts when a shuttle slips > 3-4 minutes behind schedule.
    """
    def __init__(self, delay_threshold_seconds: float = 180.0):
        self.threshold = delay_threshold_seconds
        self.alert_history: Dict[str, Dict[str, Any]] = {}

    def check_delay(self, vehicle_id: str, vehicle_name: str, etas: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not etas:
            return None

        # Check next major stop
        next_stop = etas[0]
        delay_sec = next_stop["delay_seconds"]
        is_delayed = delay_sec > self.threshold

        prev = self.alert_history.get(vehicle_id, {"is_delayed": False})

        alert = None
        if is_delayed and not prev["is_delayed"]:
            alert = {
                "vehicle_id": vehicle_id,
                "vehicle_name": vehicle_name,
                "type": "DELAY_WARNING",
                "severity": "high" if delay_sec > 300 else "medium",
                "message": f"🚨 {vehicle_name} is running {round(delay_sec/60.0)} min behind schedule near {next_stop['stop_name']}.",
                "delay_minutes": round(delay_sec / 60.0),
                "next_stop": next_stop["stop_name"]
            }
        elif not is_delayed and prev["is_delayed"]:
            alert = {
                "vehicle_id": vehicle_id,
                "vehicle_name": vehicle_name,
                "type": "ON_TIME_RECOVERY",
                "severity": "info",
                "message": f"✅ {vehicle_name} has recovered schedule and is back on time.",
                "delay_minutes": 0,
                "next_stop": next_stop["stop_name"]
            }

        self.alert_history[vehicle_id] = {
            "is_delayed": is_delayed,
            "delay_sec": delay_sec
        }

        return alert
