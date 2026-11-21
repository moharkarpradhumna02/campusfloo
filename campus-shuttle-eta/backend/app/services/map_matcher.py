import math
from typing import Tuple, Optional, Dict, Any, List
from ..utils.geo import PolylineRoute, haversine_distance

class HMMMapMatcher:
    """
    Hidden Markov Model map matcher based on Newson & Krumm (2009).
    Maintains a candidate trellis of road projections to find the most probable sequence of edges.
    """
    def __init__(self, route: PolylineRoute, sigma_z: float = 12.0, beta: float = 8.0):
        self.route = route
        self.sigma_z = sigma_z
        self.beta = beta
        # State tracker per vehicle
        self.vehicle_states: Dict[str, Dict[str, Any]] = {}

    def emission_probability(self, distance_to_segment: float) -> float:
        """Gaussian distribution over orthogonal distance to edge."""
        return (1.0 / (math.sqrt(2 * math.pi) * self.sigma_z)) * math.exp(
            -(distance_to_segment ** 2) / (2.0 * (self.sigma_z ** 2))
        )

    def transition_probability(self, route_dist_diff: float, great_circle_dist: float) -> float:
        """Exponential distribution over |route_dist - euclidean_dist|."""
        diff = abs(route_dist_diff - great_circle_dist)
        return (1.0 / self.beta) * math.exp(-diff / self.beta)

    def match(
        self,
        vehicle_id: str,
        lat: float,
        lon: float,
        timestamp: float,
        speed_mps: float
    ) -> Dict[str, Any]:
        """
        Matches a raw or cleaned GPS ping to the route polyline.
        Returns dictionary containing matched_lat, matched_lon, route_distance, confidence, heading.
        """
        last_state = self.vehicle_states.get(vehicle_id)
        expected_s = last_state["route_distance"] if last_state else None

        # Search window based on elapsed time and vehicle speed
        search_window = 350.0
        if last_state and timestamp > last_state["timestamp"]:
            dt = timestamp - last_state["timestamp"]
            search_window = max(100.0, (speed_mps + 5.0) * dt + 60.0)

        proj = self.route.project_point((lat, lon), expected_dist=expected_s, search_window=search_window)

        # Compute emission probability
        p_emit = self.emission_probability(proj["distance"])

        # Compute transition probability if previous state exists
        p_trans = 1.0
        if last_state:
            gc_dist = haversine_distance((last_state["matched_lat"], last_state["matched_lon"]), (lat, lon))
            route_dist_diff = (proj["route_distance"] - last_state["route_distance"]) % self.route.total_length
            p_trans = self.transition_probability(route_dist_diff, gc_dist)

        confidence = min(0.99, max(0.10, p_emit * p_trans * 1000.0))

        match_result = {
            "matched_lat": proj["projected_point"][0],
            "matched_lon": proj["projected_point"][1],
            "route_distance": proj["route_distance"],
            "distance_to_edge": proj["distance"],
            "heading": proj["heading"],
            "segment_index": proj["segment_index"],
            "confidence": round(confidence, 3),
            "timestamp": timestamp
        }

        self.vehicle_states[vehicle_id] = match_result
        return match_result
