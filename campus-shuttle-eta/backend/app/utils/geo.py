import math
from typing import List, Tuple, Dict, Any, Optional

EARTH_RADIUS = 6371000.0  # meters

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Compute great-circle distance between two (lat, lon) points in meters."""
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2.0)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS * c

def bearing(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Compute initial compass bearing (0..360) from coord1 to coord2."""
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    return (initial_bearing + 360.0) % 360.0

def project_point_to_segment(p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[Tuple[float, float], float, float]:
    """
    Project point p(lat, lon) onto segment [a, b].
    Returns (projected_point, orthogonal_distance_meters, fraction_t_0_to_1)
    """
    # Local flat-earth projection centered at a
    cos_lat = math.cos(math.radians(a[0]))
    k_lat = 111320.0
    k_lon = 111320.0 * cos_lat

    ax, ay = 0.0, 0.0
    bx = (b[1] - a[1]) * k_lon
    by = (b[0] - a[0]) * k_lat
    px = (p[1] - a[1]) * k_lon
    py = (p[0] - a[0]) * k_lat

    dx = bx - ax
    dy = by - ay
    l2 = dx * dx + dy * dy
    if l2 < 1e-9:
        return a, math.hypot(px, py), 0.0

    t = (px * dx + py * dy) / l2
    t_clamped = max(0.0, min(1.0, t))

    proj_x = ax + t_clamped * dx
    proj_y = ay + t_clamped * dy

    proj_lat = a[0] + proj_y / k_lat
    proj_lon = a[1] + proj_x / k_lon
    dist = math.hypot(px - proj_x, py - proj_y)

    return (proj_lat, proj_lon), dist, t_clamped

class PolylineRoute:
    """Pre-indexed route polyline with cumulative distances for rapid snapping."""
    def __init__(self, coordinates: List[Tuple[float, float]]):
        self.coords = coordinates
        self.cum_dist = [0.0]
        for i in range(1, len(coordinates)):
            d = haversine_distance(coordinates[i - 1], coordinates[i])
            self.cum_dist.append(self.cum_dist[-1] + d)
        self.total_length = self.cum_dist[-1] if self.cum_dist else 0.0

    def get_position_at_distance(self, distance: float) -> Tuple[Tuple[float, float], float]:
        """Returns (lat, lon) and heading (degrees) at distance along route."""
        d = distance % (self.total_length or 1.0)
        # binary search segment
        lo, hi = 0, len(self.cum_dist) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.cum_dist[mid] <= d:
                lo = mid
            else:
                hi = mid
        seg_len = self.cum_dist[hi] - self.cum_dist[lo]
        frac = (d - self.cum_dist[lo]) / (seg_len or 1.0)
        p1, p2 = self.coords[lo], self.coords[hi]
        lat = p1[0] + frac * (p2[0] - p1[0])
        lon = p1[1] + frac * (p2[1] - p1[1])
        hd = bearing(p1, p2)
        return (lat, lon), hd

    def project_point(self, p: Tuple[float, float], expected_dist: Optional[float] = None, search_window: float = 300.0) -> Dict[str, Any]:
        """Snap (lat, lon) to nearest segment with forward search preference."""
        best = None
        for i in range(len(self.coords) - 1):
            a, b = self.coords[i], self.coords[i + 1]
            proj_pt, dist, t = project_point_to_segment(p, a, b)
            s = self.cum_dist[i] + t * (self.cum_dist[i + 1] - self.cum_dist[i])

            if expected_dist is not None:
                # Wrap-around delta distance
                delta_s = (s - expected_dist + self.total_length / 2) % self.total_length - self.total_length / 2
                if delta_s < -50.0 or delta_s > search_window:
                    continue

            if best is None or dist < best["distance"]:
                best = {
                    "projected_point": proj_pt,
                    "distance": dist,
                    "route_distance": s,
                    "segment_index": i,
                    "heading": bearing(a, b)
                }

        # fallback if constrained search found nothing
        if best is None:
            return self.project_point(p, expected_dist=None)
        return best
