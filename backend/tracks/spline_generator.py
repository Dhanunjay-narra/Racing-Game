import math
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any


@dataclass
class Waypoint:
    index: int
    x: float
    y: float  # Elevation
    z: float
    width: float = 14.0
    bank_angle_rad: float = 0.0
    surface_type: str = "asphalt_dry"
    speed_limit_mps: float = 80.0
    optimal_racing_line_offset: float = 0.0  # -1.0 (left edge) to 1.0 (right edge)


@dataclass
class TrackMetadata:
    id: str
    name: str
    location: str
    environment: str  # City, Highway, Desert, Mountain, etc.
    length_meters: float
    lap_count_default: int
    elevation_change_m: float
    turn_count: int
    difficulty: str  # Beginner, Intermediate, Expert, Master
    thumbnail_url: str


class CatmullRomSpline:
    @staticmethod
    def interpolate(p0: Tuple[float, float, float], p1: Tuple[float, float, float], 
                    p2: Tuple[float, float, float], p3: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
        t2 = t * t
        t3 = t2 * t
        
        def calc(v0, v1, v2, v3):
            return 0.5 * (
                (2.0 * v1) +
                (-v0 + v2) * t +
                (2.0 * v0 - 5.0 * v1 + 4.0 * v2 - v3) * t2 +
                (-v0 + 3.0 * v1 - 3.0 * v2 + v3) * t3
            )
            
        return (calc(p0[0], p1[0], p2[0], p3[0]),
                calc(p0[1], p1[1], p2[1], p3[1]),
                calc(p0[2], p1[2], p2[2], p3[2]))


class TrackBuilder:
    def __init__(self, metadata: TrackMetadata):
        self.metadata = metadata
        self.control_points: List[Waypoint] = []
        self.checkpoints: List[Dict[str, Any]] = []
        self.sample_points: List[Waypoint] = []

    def add_control_point(self, wp: Waypoint):
        self.control_points.append(wp)

    def generate_interpolated_track(self, samples_per_segment: int = 20) -> List[Waypoint]:
        if len(self.control_points) < 4:
            return self.control_points
            
        self.sample_points = []
        n = len(self.control_points)
        global_idx = 0
        
        for i in range(n):
            p0 = self.control_points[(i - 1 + n) % n]
            p1 = self.control_points[i]
            p2 = self.control_points[(i + 1) % n]
            p3 = self.control_points[(i + 2) % n]
            
            for s in range(samples_per_segment):
                t = s / float(samples_per_segment)
                pos = CatmullRomSpline.interpolate(
                    (p1.x, p1.y, p1.z),
                    (p2.x, p2.y, p2.z),
                    (p3.x, p3.y, p3.z),
                    (p0.x, p0.y, p0.z),
                    t
                )
                
                # Bank angle & racing line interpolation
                bank = p1.bank_angle_rad + (p2.bank_angle_rad - p1.bank_angle_rad) * t
                line_off = p1.optimal_racing_line_offset + (p2.optimal_racing_line_offset - p1.optimal_racing_line_offset) * t
                
                wp = Waypoint(
                    index=global_idx,
                    x=pos[0],
                    y=pos[1],
                    z=pos[2],
                    width=p1.width,
                    bank_angle_rad=bank,
                    surface_type=p1.surface_type,
                    optimal_racing_line_offset=line_off
                )
                self.sample_points.append(wp)
                global_idx += 1
                
        # Setup checkpoints every 150-200 meters
        self.checkpoints = []
        step = max(1, len(self.sample_points) // 10)
        for idx in range(0, len(self.sample_points), step):
            wp = self.sample_points[idx]
            self.checkpoints.append({
                "index": len(self.checkpoints),
                "waypoint_index": idx,
                "position": {"x": wp.x, "y": wp.y, "z": wp.z},
                "is_finish_line": (idx == 0)
            })
            
        return self.sample_points
