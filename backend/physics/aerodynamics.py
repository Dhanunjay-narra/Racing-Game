import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class AeroSpec:
    frontal_area_m2: float = 2.15
    drag_coefficient_cd: float = 0.32
    front_downforce_cl: float = 0.45
    rear_downforce_cl: float = 0.75
    ground_effect_factor: float = 0.20
    drafting_distance_max_m: float = 35.0


class AerodynamicsSystem:
    def __init__(self, spec: AeroSpec, air_density: float = 1.225):
        self.spec = spec
        self.air_density = air_density

    def compute_aero_forces(
        self,
        speed_mps: float,
        ride_height_m: float,
        slipstream_deficit: float = 0.0
    ) -> Tuple[float, float, float]:
        # Dynamic pressure: q = 0.5 * rho * v^2
        effective_speed = max(0.0, speed_mps * (1.0 - slipstream_deficit * 0.35))
        dynamic_pressure = 0.5 * self.air_density * (effective_speed ** 2)
        
        # Ground effect multiplier (higher downforce at lower ride height)
        height_factor = max(0.5, min(2.0, 0.10 / max(0.04, ride_height_m)))
        ground_effect_boost = 1.0 + (self.spec.ground_effect_factor * height_factor)
        
        # Drag Force
        drag_force_n = dynamic_pressure * self.spec.frontal_area_m2 * self.spec.drag_coefficient_cd
        if slipstream_deficit > 0.0:
            drag_force_n *= (1.0 - slipstream_deficit * 0.40)  # Significant drag reduction when drafting
            
        # Front and Rear Downforce
        front_downforce_n = dynamic_pressure * self.spec.frontal_area_m2 * self.spec.front_downforce_cl * ground_effect_boost
        rear_downforce_n = dynamic_pressure * self.spec.frontal_area_m2 * self.spec.rear_downforce_cl * ground_effect_boost
        
        return drag_force_n, front_downforce_n, rear_downforce_n
