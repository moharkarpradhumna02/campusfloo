import math
from typing import List, Dict, Any, Optional
from ..utils.geo import PolylineRoute

class ETAEngine:
    def __init__(
        self,
        route: PolylineRoute,
        stops: List[Dict[str, Any]],
        historical_speed_mps: float = 5.8,  # ~21 km/h campus cruising speed
        default_dwell_sec: float = 18.0
    ):
        self.route = route
        self.stops = stops  # [{id, name, code, route_distance, dwell_sec}]
        self.hist_speed = historical_speed_mps
        self.default_dwell = default_dwell_sec
        self.vehicles: Dict[str, Dict[str, Any]] = {}

    def update_vehicle_fix(self, vehicle_id: str, matched_s: float, speed_mps: float, timestamp: float):
        v_current = max(1.5, speed_mps) if speed_mps > 0.5 else 0.0
        if vehicle_id not in self.vehicles:
            self.vehicles[vehicle_id] = {
                "s": matched_s,
                "v": v_current or self.hist_speed,
                "v_ema": v_current or self.hist_speed,
                "last_fix_ts": timestamp,
                "last_step_ts": timestamp,
                "in_dropout": False
            }
        else:
            state = self.vehicles[vehicle_id]
            if v_current > 1.0:
                state["v_ema"] = 0.85 * state["v_ema"] + 0.15 * v_current
                state["v"] = 0.7 * state["v"] + 0.3 * v_current
            state["s"] = matched_s
            state["last_fix_ts"] = timestamp
            state["last_step_ts"] = timestamp
            state["in_dropout"] = False

    def dead_reckon_to(self, vehicle_id: str, current_time: float) -> Dict[str, Any]:
        if vehicle_id not in self.vehicles:
            return {"s": 0.0, "v": self.hist_speed, "age": 0.0, "in_dropout": False}

        state = self.vehicles[vehicle_id]
        dt = max(0.0, current_time - state["last_step_ts"])
        age = current_time - state["last_fix_ts"]
        state["in_dropout"] = (age >= 10.0)

        # Smooth dead-reckoning speed: blend towards historical speed during blackout
        w = math.exp(-age / 90.0)
        blended_speed = max(2.5, w * (0.6 * state["v_ema"] + 0.4 * self.hist_speed) + (1.0 - w) * self.hist_speed)

        state["s"] = (state["s"] + blended_speed * dt) % self.route.total_length
        state["v"] = blended_speed
        state["last_step_ts"] = current_time

        return {
            "s": state["s"],
            "v": blended_speed,
            "age": age,
            "in_dropout": state["in_dropout"]
        }

    def compute_stop_etas(self, vehicle_id: str, current_time: float) -> List[Dict[str, Any]]:
        dr = self.dead_reckon_to(vehicle_id, current_time)
        curr_s = dr["s"]
        L = self.route.total_length
        v_eff = max(2.5, dr["v"])

        etas = []
        for stop in self.stops:
            stop_s = stop["route_distance"]
            raw_d = (stop_s - curr_s) % L
            dist = raw_d if raw_d > 10.0 else L + raw_d

            # Count stops between current position and target stop
            intermediate = 0
            for other in self.stops:
                if other["id"] == stop["id"]:
                    continue
                other_d = (other["route_distance"] - curr_s) % L
                if 20.0 < other_d < raw_d - 20.0:
                    intermediate += 1

            dwell_sec = intermediate * stop.get("dwell_sec", self.default_dwell)
            eta_seconds = (dist / v_eff) + dwell_sec
            nominal_seconds = (dist / self.hist_speed) + dwell_sec
            delay_seconds = eta_seconds - nominal_seconds

            etas.append({
                "stop_id": stop["id"],
                "stop_name": stop["name"],
                "stop_code": stop.get("code", ""),
                "distance_meters": round(dist, 1),
                "eta_seconds": round(eta_seconds),
                "eta_minutes": max(1, round(eta_seconds / 60.0)),
                "delay_seconds": round(delay_seconds),
                "is_delayed": (delay_seconds > 180.0)
            })

        etas.sort(key=lambda x: x["distance_meters"])
        return etas
