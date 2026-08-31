import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class ValidationViolation:
    violation_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    details: str
    timestamp_ms: int


class KinematicsValidator:
    MAX_SPEED_MPS = 135.0          # ~486 km/h
    MAX_ACCEL_MPS2 = 35.0          # ~3.5G
    MAX_TELEPORT_DISTANCE_M = 15.0 # Max distance covered in 1 tick

    def __init__(self, expected_checkpoints_count: int):
        self.expected_checkpoints_count = expected_checkpoints_count
        self.last_pos: Optional[Tuple[float, float, float]] = None
        self.last_speed_mps: float = 0.0
        self.last_time_s: float = 0.0
        self.visited_checkpoints: List[int] = []
        self.violations: List[ValidationViolation] = []

    def validate_tick(
        self,
        pos: Tuple[float, float, float],
        speed_kmh: float,
        time_s: float,
        current_checkpoint: int
    ) -> List[ValidationViolation]:
        new_violations = []
        speed_mps = speed_kmh / 3.6
        dt = max(1e-4, time_s - self.last_time_s) if self.last_time_s > 0 else 0.016

        # 1. Speed cap check
        if speed_mps > self.MAX_SPEED_MPS:
            v = ValidationViolation(
                violation_type="IMPOSSIBLE_SPEED",
                severity="CRITICAL",
                details=f"Speed {speed_kmh:.1f} km/h exceeds maximum theoretical limit",
                timestamp_ms=int(time_s * 1000)
            )
            new_violations.append(v)

        # 2. Acceleration spike check
        if self.last_time_s > 0:
            accel = (speed_mps - self.last_speed_mps) / dt
            if accel > self.MAX_ACCEL_MPS2:
                v = ValidationViolation(
                    violation_type="IMPOSSIBLE_ACCELERATION",
                    severity="HIGH",
                    details=f"Acceleration {accel:.1f} m/s^2 exceeds plausible envelope",
                    timestamp_ms=int(time_s * 1000)
                )
                new_violations.append(v)

        # 3. Teleportation / Displacement check
        if self.last_pos is not None:
            dist = math.sqrt(
                (pos[0] - self.last_pos[0])**2 +
                (pos[1] - self.last_pos[1])**2 +
                (pos[2] - self.last_pos[2])**2
            )
            max_allowed_dist = (self.last_speed_mps * dt) + 5.0
            if dist > max_allowed_dist and dist > self.MAX_TELEPORT_DISTANCE_M:
                v = ValidationViolation(
                    violation_type="TELEPORTATION_DETECTED",
                    severity="CRITICAL",
                    details=f"Displacement of {dist:.1f}m in {dt:.3f}s exceeds vehicle reach",
                    timestamp_ms=int(time_s * 1000)
                )
                new_violations.append(v)

        # 4. Checkpoint sequence integrity
        if current_checkpoint not in self.visited_checkpoints:
            expected_next = (self.visited_checkpoints[-1] + 1) % self.expected_checkpoints_count if self.visited_checkpoints else 0
            if current_checkpoint != expected_next and len(self.visited_checkpoints) > 0:
                v = ValidationViolation(
                    violation_type="CHECKPOINT_BYPASS",
                    severity="HIGH",
                    details=f"Skipped checkpoint: jumped from {self.visited_checkpoints[-1]} to {current_checkpoint}",
                    timestamp_ms=int(time_s * 1000)
                )
                new_violations.append(v)
            self.visited_checkpoints.append(current_checkpoint)

        self.last_pos = pos
        self.last_speed_mps = speed_mps
        self.last_time_s = time_s
        self.violations.extend(new_violations)
        return new_violations
