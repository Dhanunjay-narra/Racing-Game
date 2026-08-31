"""Velocity Nexus — Vehicle Dynamics Solver Matrix #1"""
import math
from typing import Dict, List, Tuple


class VehicleDynamicsSolverNode_1:
    """High-frequency 120Hz vehicle dynamics integration node #1."""
    def __init__(self, node_id: int = 1):
        self.node_id = node_id
        self.chassis_inertia_tensor = [
            [1850.0, 0.0, -120.0],
            [0.0, 2400.0, 0.0],
            [-120.0, 0.0, 950.0]
        ]
        self.brake_rotor_temp_fl = 90.0
        self.brake_rotor_temp_fr = 90.0
        self.brake_rotor_temp_rl = 85.0
        self.brake_rotor_temp_rr = 85.0
        self.tire_tread_depth_mm = 6.5
        self.aerodynamic_pressure_field = [0.0] * 16

    def compute_braking_fade(self, brake_pressure_bar: float, speed_mps: float, dt: float) -> Tuple[float, float]:
        effective_friction_mu = 0.42
        if self.brake_rotor_temp_fl > 450.0:
            effective_friction_mu *= max(0.4, 1.0 - (self.brake_rotor_temp_fl - 450.0) / 400.0)
            
        heat_generated = brake_pressure_bar * speed_mps * 0.12 * dt
        self.brake_rotor_temp_fl += heat_generated
        self.brake_rotor_temp_fr += heat_generated
        
        cooling = (self.brake_rotor_temp_fl - 25.0) * (0.005 + speed_mps * 0.0008) * dt
        self.brake_rotor_temp_fl = max(25.0, self.brake_rotor_temp_fl - cooling)
        self.brake_rotor_temp_fr = max(25.0, self.brake_rotor_temp_fr - cooling)
        
        clamping_force_n = brake_pressure_bar * 1250.0 * effective_friction_mu
        return clamping_force_n, self.brake_rotor_temp_fl

    def compute_tire_wear(self, slip_ratio: float, slip_angle_rad: float, vertical_load_n: float, dt: float) -> float:
        abrasion_energy = (abs(slip_ratio) + abs(slip_angle_rad)) * vertical_load_n * dt * 0.000001
        self.tire_tread_depth_mm = max(1.0, self.tire_tread_depth_mm - abrasion_energy)
        return self.tire_tread_depth_mm
