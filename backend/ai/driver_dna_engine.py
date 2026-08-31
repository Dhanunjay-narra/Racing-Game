import math
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class TelemetryFrame:
    timestamp_ms: int
    speed_kmh: float
    throttle: float
    brake: float
    steer: float
    slip_angle_deg: float
    g_lat: float
    g_long: float
    distance_to_nearest_car_m: float
    collision_occurred: bool
    apex_distance_m: float
    track_surface: str


class DriverDNAAnalyzer:
    def __init__(self):
        pass

    def analyze_race_session(self, telemetry_frames: List[TelemetryFrame]) -> Dict[str, float]:
        if not telemetry_frames:
            return {
                "aggression": 0.50, "cornering": 0.50, "overtaking": 0.50,
                "drifting": 0.50, "consistency": 0.50, "wet_racing": 0.50,
                "risk_management": 0.50, "archetype": "Balanced Prodigy"
            }

        total_frames = len(telemetry_frames)
        
        # 1. Aggression calculation
        proximity_count = sum(1 for f in telemetry_frames if f.distance_to_nearest_car_m < 3.5)
        collision_count = sum(1 for f in telemetry_frames if f.collision_occurred)
        aggression_score = min(1.0, (proximity_count / max(1, total_frames * 0.15)) * 0.6 + (collision_count * 0.08))

        # 2. Cornering precision (low apex deviation at high lat-G)
        apex_deviations = [f.apex_distance_m for f in telemetry_frames if abs(f.g_lat) > 0.8]
        avg_apex_dev = sum(apex_deviations) / max(1, len(apex_deviations)) if apex_deviations else 1.5
        cornering_score = max(0.1, min(1.0, 1.0 - (avg_apex_dev / 4.0)))

        # 3. Drifting score (slip angle sustain under power)
        drift_frames = sum(1 for f in telemetry_frames if abs(f.slip_angle_deg) > 12.0 and f.throttle > 0.5)
        drifting_score = min(1.0, drift_frames / max(1, total_frames * 0.10))

        # 4. Consistency (speed variance on similar segments)
        speeds = [f.speed_kmh for f in telemetry_frames]
        mean_speed = sum(speeds) / total_frames
        speed_variance = sum((s - mean_speed) ** 2 for s in speeds) / total_frames
        consistency_score = max(0.1, min(1.0, 1.0 - (math.sqrt(speed_variance) / 80.0)))

        # 5. Risk management (braking margin & collision avoidance)
        late_brakes = sum(1 for f in telemetry_frames if f.brake > 0.9 and f.speed_kmh > 150.0)
        risk_score = min(1.0, late_brakes / max(1, total_frames * 0.05))

        # 6. Wet racing adaptation
        wet_frames = [f for f in telemetry_frames if "wet" in f.track_surface or "snow" in f.track_surface]
        if wet_frames:
            wet_throttle_smoothness = sum(1 for f in wet_frames if 0.2 < f.throttle < 0.8) / len(wet_frames)
            wet_score = min(1.0, wet_throttle_smoothness * 1.5)
        else:
            wet_score = 0.50

        # Archetype Classification
        archetype = "Balanced Prodigy"
        if aggression_score > 0.75 and risk_score > 0.70:
            archetype = "Apex Predator"
        elif cornering_score > 0.80 and consistency_score > 0.75:
            archetype = "Precision Maestro"
        elif drifting_score > 0.70:
            archetype = "Drift Monarch"
        elif wet_score > 0.75:
            archetype = "Storm Rider"
        elif consistency_score > 0.85:
            archetype = "Metronome Master"

        return {
            "aggression": round(aggression_score, 2),
            "cornering": round(cornering_score, 2),
            "overtaking": round(min(1.0, aggression_score * 0.8 + cornering_score * 0.4), 2),
            "drifting": round(drifting_score, 2),
            "consistency": round(consistency_score, 2),
            "wet_racing": round(wet_score, 2),
            "risk_management": round(1.0 - risk_score * 0.5, 2),
            "archetype": archetype
        }
