import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class PacejkaCoefficients:
    B: float = 10.0   # Stiffness factor
    C: float = 1.65   # Shape factor (lateral ~ 1.3-1.9)
    D: float = 1.25   # Peak friction coefficient (mu)
    E: float = -0.60  # Curvature factor
    camber_stiffness: float = 0.015


class PacejkaTireModel:
    def __init__(self, longitudinal_params: PacejkaCoefficients = None, lateral_params: PacejkaCoefficients = None):
        self.long_coeff = longitudinal_params or PacejkaCoefficients(B=11.5, C=1.65, D=1.20, E=-0.50)
        self.lat_coeff = lateral_params or PacejkaCoefficients(B=9.8, C=1.35, D=1.25, E=-0.80)

    def compute_force(self, slip: float, normal_load_n: float, coeff: PacejkaCoefficients) -> float:
        if normal_load_n <= 0.0:
            return 0.0
            
        # Magic Formula: F = D * sin(C * arctan(B*slip - E*(B*slip - arctan(B*slip))))
        b_slip = coeff.B * slip
        bx1 = b_slip - coeff.E * (b_slip - math.atan(b_slip))
        force_norm = coeff.D * math.sin(coeff.C * math.atan(bx1))
        
        return force_norm * normal_load_n

    def compute_combined_forces(
        self,
        longitudinal_slip: float,
        slip_angle_rad: float,
        camber_angle_rad: float,
        normal_load_n: float,
        surface_friction_multiplier: float = 1.0
    ) -> Tuple[float, float]:
        if normal_load_n <= 0.0:
            return 0.0, 0.0

        # Normalized slip vector (Friction Circle ellipse constraint)
        sigma_x = longitudinal_slip
        sigma_y = math.tan(slip_angle_rad)
        combined_slip = math.sqrt(sigma_x**2 + sigma_y**2) + 1e-6
        
        fx_pure = self.compute_force(combined_slip, normal_load_n, self.long_coeff)
        fy_pure = self.compute_force(combined_slip, normal_load_n, self.lat_coeff)
        
        fx = (sigma_x / combined_slip) * fx_pure * surface_friction_multiplier
        fy = (sigma_y / combined_slip) * fy_pure * surface_friction_multiplier
        
        # Camber thrust component
        camber_thrust = -self.lat_coeff.camber_stiffness * camber_angle_rad * normal_load_n
        fy += camber_thrust * surface_friction_multiplier
        
        return fx, fy
