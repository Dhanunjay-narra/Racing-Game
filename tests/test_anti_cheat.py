import pytest
from backend.anti_cheat.kinematics_validator import KinematicsValidator


def test_anti_cheat_speed_limit_violation():
    validator = KinematicsValidator(expected_checkpoints_count=10)
    
    # Valid normal speed: 200 km/h
    violations_normal = validator.validate_tick(pos=(0, 0, 10), speed_kmh=200.0, time_s=0.1, current_checkpoint=0)
    assert len(violations_normal) == 0
    
    # Impossible speed: 600 km/h (exceeds 486 km/h cap)
    violations_cheat = validator.validate_tick(pos=(0, 0, 100), speed_kmh=600.0, time_s=0.2, current_checkpoint=1)
    assert any(v.violation_type == "IMPOSSIBLE_SPEED" for v in violations_cheat)


def test_anti_cheat_checkpoint_bypass():
    validator = KinematicsValidator(expected_checkpoints_count=10)
    validator.validate_tick(pos=(0, 0, 0), speed_kmh=100.0, time_s=0.1, current_checkpoint=0)
    
    # Jump from checkpoint 0 directly to checkpoint 5
    violations = validator.validate_tick(pos=(0, 0, 50), speed_kmh=120.0, time_s=0.2, current_checkpoint=5)
    assert any(v.violation_type == "CHECKPOINT_BYPASS" for v in violations)
