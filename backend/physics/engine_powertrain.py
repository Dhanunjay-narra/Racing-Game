import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class EngineSpec:
    name: str
    idle_rpm: float = 900.0
    max_rpm: float = 9000.0
    rev_limiter_rpm: float = 8800.0
    peak_torque_nm: float = 650.0
    peak_torque_rpm: float = 5500.0
    peak_power_hp: float = 620.0
    peak_power_rpm: float = 7800.0
    engine_inertia: float = 0.22  # kg * m^2
    turbo_equipped: bool = True
    max_boost_bar: float = 1.4
    spool_rate: float = 2.8


class EnginePowertrain:
    def __init__(self, spec: EngineSpec):
        self.spec = spec
        self.current_rpm: float = spec.idle_rpm
        self.current_torque_nm: float = 0.0
        self.throttle_input: float = 0.0
        self.boost_pressure: float = 0.0
        self.is_rev_limiting: bool = False
        self.fuel_cut: bool = False

    def calculate_base_torque(self, rpm: float) -> float:
        norm_rpm = (rpm - self.spec.idle_rpm) / (self.spec.max_rpm - self.spec.idle_rpm)
        norm_rpm = max(0.0, min(1.0, norm_rpm))
        
        peak_norm = (self.spec.peak_torque_rpm - self.spec.idle_rpm) / (self.spec.max_rpm - self.spec.idle_rpm)
        
        if norm_rpm < peak_norm:
            factor = 0.6 + 0.4 * math.sin((norm_rpm / peak_norm) * (math.pi / 2.0))
        else:
            falloff = (norm_rpm - peak_norm) / (1.0 - peak_norm)
            factor = 1.0 - 0.35 * (falloff ** 1.5)
            
        return self.spec.peak_torque_nm * max(0.2, factor)

    def update(self, dt: float, throttle: float, clutch_engaged: bool, load_torque: float) -> Tuple[float, float]:
        self.throttle_input = max(0.0, min(1.0, throttle))
        
        # Turbo boost calculation
        if self.spec.turbo_equipped:
            target_boost = self.spec.max_boost_bar * (self.throttle_input ** 1.5) * (self.current_rpm / self.spec.max_rpm)
            self.boost_pressure += (target_boost - self.boost_pressure) * min(1.0, dt * self.spec.spool_rate)
        else:
            self.boost_pressure = 0.0
            
        boost_multiplier = 1.0 + (self.boost_pressure * 0.45)
        raw_torque = self.calculate_base_torque(self.current_rpm) * boost_multiplier * self.throttle_input
        
        # Rev limiter logic
        if self.current_rpm >= self.spec.rev_limiter_rpm:
            self.is_rev_limiting = True
            self.fuel_cut = True
            raw_torque = -50.0  # Engine braking during fuel cut
        else:
            if self.current_rpm < self.spec.rev_limiter_rpm - 200.0:
                self.is_rev_limiting = False
                self.fuel_cut = False
                
        # RPM Integration
        friction_torque = 15.0 + 0.008 * self.current_rpm
        net_engine_torque = raw_torque - friction_torque
        
        if not clutch_engaged:
            # Free revving
            angular_accel = net_engine_torque / self.spec.engine_inertia
            self.current_rpm += (angular_accel * 60.0 / (2.0 * math.pi)) * dt
        else:
            # Connected to drivetrain
            effective_torque = net_engine_torque - load_torque
            angular_accel = effective_torque / (self.spec.engine_inertia * 4.0)
            self.current_rpm += (angular_accel * 60.0 / (2.0 * math.pi)) * dt
            
        self.current_rpm = max(self.spec.idle_rpm, min(self.spec.max_rpm, self.current_rpm))
        self.current_torque_nm = max(0.0, raw_torque)
        
        power_hp = (self.current_torque_nm * self.current_rpm) / 7127.0
        return self.current_torque_nm, power_hp
