from typing import Tuple, Optional, Dict, Any
import math
from ..utils.geo import haversine_distance

class KalmanFilter2D:
    """Simple 2D constant-velocity Kalman filter for lat/lon smoothing."""
    def __init__(self, process_noise: float = 1e-4, measurement_noise: float = 1e-3):
        self.q = process_noise
        self.r = measurement_noise
        self.x = 0.0  # lat
        self.y = 0.0  # lon
        self.p = 1.0  # covariance
        self.initialized = False

    def update(self, lat: float, lon: float) -> Tuple[float, float]:
        if not self.initialized:
            self.x = lat
            self.y = lon
            self.p = self.r
            self.initialized = True
            return lat, lon

        # Prediction step
        self.p += self.q

        # Measurement update
        k = self.p / (self.p + self.r)
        self.x += k * (lat - self.x)
        self.y += k * (lon - self.y)
        self.p *= (1.0 - k)
        return self.x, self.y

class GPSCleaner:
    def __init__(
        self,
        max_accuracy_threshold: float = 65.0,  # meters
        max_speed_kmh: float = 80.0,           # speed gate 80 km/h = 22.2 m/s
        jump_buffer_meters: float = 55.0
    ):
        self.max_accuracy = max_accuracy_threshold
        self.max_speed_mps = max_speed_kmh / 3.6
        self.jump_buffer = jump_buffer_meters
        self.kalman_filters: Dict[str, KalmanFilter2D] = {}
        self.last_clean_pings: Dict[str, Dict[str, Any]] = {}

    def clean_ping(
        self,
        vehicle_id: str,
        lat: float,
        lon: float,
        speed_mps: float,
        timestamp: float,
        accuracy_m: float = 10.0
    ) -> Tuple[bool, Optional[Tuple[float, float]], str]:
        """
        Cleans an incoming GPS ping.
        Returns:
            (is_valid, (cleaned_lat, cleaned_lon), rejection_reason)
        """
        # 1. Accuracy gate
        if accuracy_m > self.max_accuracy:
            return False, None, f"Accuracy too poor ({accuracy_m:.1f}m > {self.max_accuracy}m)"

        # 2. Instantaneous speed gate
        if speed_mps > self.max_speed_mps:
            return False, None, f"Instantaneous speed exceeded ({speed_mps*3.6:.1f} km/h > 80 km/h)"

        # 3. Jump filter against last known clean ping
        last = self.last_clean_pings.get(vehicle_id)
        if last is not None:
            dt = max(0.5, timestamp - last["timestamp"])
            dist = haversine_distance((last["lat"], last["lon"]), (lat, lon))
            implied_speed = dist / dt
            max_allowed_dist = (self.max_speed_mps * dt) + self.jump_buffer

            if dist > max_allowed_dist or implied_speed > self.max_speed_mps:
                return False, None, f"GPS teleportation jump detected: {dist:.1f}m in {dt:.1f}s ({implied_speed*3.6:.1f} km/h)"

        # 4. Kalman smoothing
        if vehicle_id not in self.kalman_filters:
            self.kalman_filters[vehicle_id] = KalmanFilter2D()
        smooth_lat, smooth_lon = self.kalman_filters[vehicle_id].update(lat, lon)

        self.last_clean_pings[vehicle_id] = {
            "lat": smooth_lat,
            "lon": smooth_lon,
            "timestamp": timestamp,
            "speed": speed_mps
        }

        return True, (smooth_lat, smooth_lon), "OK"
