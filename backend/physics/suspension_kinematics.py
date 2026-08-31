import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SuspensionSpec:
    spring_rate_n_per_m: float = 45000.0   # 45 N/mm
    damper_bump_n_per_m_s: float = 3800.0   # Compression damping
    damper_rebound_n_per_m_s: float = 6200.0 # Rebound damping
    anti_roll_bar_stiffness: float = 8500.0  # N/rad
    ride_height_m: float = 0.12
    max_travel_m: float = 0.16
    camber_gain_per_travel: float = 0.04   # rad/m


class SuspensionCorner:
    def __init__(self, spec: SuspensionSpec, rest_load_n: float):
        self.spec = spec
        self.rest_load_n = rest_load_n
        self.current_compression_m: float = 0.0
        self.current_velocity_m_s: float = 0.0
        self.current_load_n: float = rest_load_n
        self.dynamic_camber_rad: float = 0.0

    def update(self, ground_height_m: float, chassis_corner_height_m: float, dt: float, arb_force_n: float = 0.0) -> float:
        distance_to_ground = chassis_corner_height_m - ground_height_m
        target_compression = (self.spec.ride_height_m + self.spec.max_travel_m * 0.5) - distance_to_ground
        target_compression = max(0.0, min(self.spec.max_travel_m, target_compression))
        
        self.current_velocity_m_s = (target_compression - self.current_compression_m) / max(1e-5, dt)
        self.current_compression_m = target_compression
        
        # Spring Force (Hooke's Law)
        spring_force = self.spec.spring_rate_n_per_m * self.current_compression_m
        
        # Damper Force (Non-linear bump/rebound)
        if self.current_velocity_m_s >= 0.0:
            damper_force = self.spec.damper_bump_n_per_m_s * self.current_velocity_m_s
        else:
            damper_force = self.spec.damper_rebound_n_per_m_s * self.current_velocity_m_s
            
        total_suspension_force = max(0.0, spring_force + damper_force + arb_force_n)
        self.current_load_n = total_suspension_force
        
        # Camber change under suspension compression
        self.dynamic_camber_rad = (self.current_compression_m - (self.spec.max_travel_m * 0.5)) * self.spec.camber_gain_per_travel
        
        return total_suspension_force
