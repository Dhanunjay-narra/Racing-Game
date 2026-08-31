from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class TransmissionSpec:
    gear_ratios: List[float] = field(default_factory=lambda: [-3.4, 0.0, 3.82, 2.36, 1.68, 1.31, 1.00, 0.79])
    final_drive_ratio: float = 3.73
    shift_up_rpm: float = 7800.0
    shift_down_rpm: float = 3200.0
    shift_delay_sec: float = 0.12
    differential_type: str = "LSD"  # Open, LSD, Spool, TorqueVectoring
    lsd_locking_factor: float = 0.65


class SequentialTransmission:
    def __init__(self, spec: TransmissionSpec):
        self.spec = spec
        self.current_gear: int = 2  # Index 2 = 1st gear (0 = Reverse, 1 = Neutral, 2 = 1st, ...)
        self.clutch_engagement: float = 1.0  # 0.0 (disengaged) to 1.0 (fully locked)
        self.is_shifting: bool = False
        self.shift_timer: float = 0.0
        self.target_gear: int = 2

    def get_gear_name(self) -> str:
        if self.current_gear == 0:
            return "R"
        elif self.current_gear == 1:
            return "N"
        else:
            return str(self.current_gear - 1)

    def get_current_ratio(self) -> float:
        if 0 <= self.current_gear < len(self.spec.gear_ratios):
            return self.spec.gear_ratios[self.current_gear] * self.spec.final_drive_ratio
        return 0.0

    def shift_up(self):
        if self.current_gear < len(self.spec.gear_ratios) - 1 and not self.is_shifting:
            self.target_gear = self.current_gear + 1
            self.is_shifting = True
            self.shift_timer = self.spec.shift_delay_sec
            self.clutch_engagement = 0.0

    def shift_down(self):
        if self.current_gear > 0 and not self.is_shifting:
            self.target_gear = self.current_gear - 1
            self.is_shifting = True
            self.shift_timer = self.spec.shift_delay_sec
            self.clutch_engagement = 0.0

    def update_auto(self, dt: float, current_rpm: float, throttle: float):
        if self.is_shifting:
            self.shift_timer -= dt
            if self.shift_timer <= 0.0:
                self.current_gear = self.target_gear
                self.is_shifting = False
                self.clutch_engagement = 1.0
            return

        if self.current_gear >= 2:  # Forward gears
            if current_rpm > self.spec.shift_up_rpm and throttle > 0.4 and self.current_gear < len(self.spec.gear_ratios) - 1:
                self.shift_up()
            elif current_rpm < self.spec.shift_down_rpm and self.current_gear > 2:
                self.shift_down()

    def distribute_wheel_torque(self, input_torque_nm: float, left_wheel_angular_vel: float, right_wheel_angular_vel: float) -> Tuple[float, float]:
        ratio = self.get_current_ratio()
        total_wheel_torque = input_torque_nm * ratio * self.clutch_engagement
        
        if self.spec.differential_type == "Spool":
            return total_wheel_torque * 0.5, total_wheel_torque * 0.5
            
        vel_diff = left_wheel_angular_vel - right_wheel_angular_vel
        transfer = total_wheel_torque * self.spec.lsd_locking_factor * 0.5 * (vel_diff / (abs(vel_diff) + 1.0))
        
        left_torque = (total_wheel_torque * 0.5) - transfer
        right_torque = (total_wheel_torque * 0.5) + transfer
        
        return left_torque, right_torque
