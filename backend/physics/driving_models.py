from dataclasses import dataclass


@dataclass
class DrivingModelProfile:
    name: str
    steering_speed_dampening: float
    traction_control_strength: float
    abs_brake_modulation: float
    stability_control_yaw_correction: float
    counter_steer_assist: float
    drift_snap_recovery: float
    tire_grip_forgiveness: float


class DrivingModelPresets:
    ARCADE = DrivingModelProfile(
        name="Arcade",
        steering_speed_dampening=0.35,
        traction_control_strength=0.85,
        abs_brake_modulation=0.95,
        stability_control_yaw_correction=0.75,
        counter_steer_assist=0.90,
        drift_snap_recovery=0.85,
        tire_grip_forgiveness=1.40
    )
    
    SEMI_SIMULATION = DrivingModelProfile(
        name="Semi-Simulation",
        steering_speed_dampening=0.60,
        traction_control_strength=0.40,
        abs_brake_modulation=0.70,
        stability_control_yaw_correction=0.35,
        counter_steer_assist=0.40,
        drift_snap_recovery=0.45,
        tire_grip_forgiveness=1.15
    )
    
    FULL_SIMULATION = DrivingModelProfile(
        name="Full Simulation",
        steering_speed_dampening=1.00,
        traction_control_strength=0.00,
        abs_brake_modulation=0.00,
        stability_control_yaw_correction=0.00,
        counter_steer_assist=0.00,
        drift_snap_recovery=0.00,
        tire_grip_forgiveness=1.00
    )
