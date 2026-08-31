import pytest
import math
from backend.physics.engine_powertrain import EnginePowertrain, EngineSpec
from backend.physics.transmission import SequentialTransmission, TransmissionSpec
from backend.physics.pacejka_tire_model import PacejkaTireModel, PacejkaCoefficients
from backend.physics.suspension_kinematics import SuspensionCorner, SuspensionSpec
from backend.physics.aerodynamics import AerodynamicsSystem, AeroSpec


def test_engine_powertrain_torque_curve():
    spec = EngineSpec(name="Test V8", idle_rpm=1000, max_rpm=8000, peak_torque_nm=600, peak_torque_rpm=5000)
    engine = EnginePowertrain(spec)
    
    torque_idle = engine.calculate_base_torque(1000)
    torque_peak = engine.calculate_base_torque(5000)
    torque_redline = engine.calculate_base_torque(8000)
    
    assert torque_peak > torque_idle
    assert torque_peak >= torque_redline
    assert torque_peak == pytest.approx(600, rel=0.1)


def test_sequential_transmission_shifting():
    spec = TransmissionSpec()
    trans = SequentialTransmission(spec)
    assert trans.current_gear == 2  # 1st gear
    
    trans.shift_up()
    assert trans.is_shifting is True
    trans.update_auto(0.2, 7000, 1.0)
    assert trans.is_shifting is False
    assert trans.current_gear == 3  # 2nd gear


def test_pacejka_tire_model_forces():
    model = PacejkaTireModel()
    normal_load = 4000.0  # N
    
    # Pure longitudinal slip
    fx, fy = model.compute_combined_forces(
        longitudinal_slip=0.12,
        slip_angle_rad=0.0,
        camber_angle_rad=0.0,
        normal_load_n=normal_load
    )
    assert fx > 0.0
    assert fy == pytest.approx(0.0, abs=1.0)
    
    # Lateral cornering slip
    fx_lat, fy_lat = model.compute_combined_forces(
        longitudinal_slip=0.0,
        slip_angle_rad=0.10,  # ~5.7 degrees
        camber_angle_rad=0.0,
        normal_load_n=normal_load
    )
    assert fy_lat > 0.0


def test_aerodynamics_drag_and_downforce():
    aero = AerodynamicsSystem(AeroSpec())
    drag_slow, downforce_f_slow, downforce_r_slow = aero.compute_aero_forces(speed_mps=20.0, ride_height_m=0.10)
    drag_fast, downforce_f_fast, downforce_r_fast = aero.compute_aero_forces(speed_mps=80.0, ride_height_m=0.10)
    
    assert drag_fast > drag_slow * 10.0  # Speed squared relationship
    assert downforce_r_fast > downforce_r_slow * 10.0
