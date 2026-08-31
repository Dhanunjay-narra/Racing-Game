import math
from typing import List, Tuple, Dict, Any
from backend.ai.personalities import AIPersonality, AIPersonalityPresets


class AIDriverController:
    def __init__(self, driver_id: str, name: str, personality: AIPersonality = None):
        self.driver_id = driver_id
        self.name = name
        self.personality = personality or AIPersonalityPresets.BALANCED
        
        self.current_waypoint_idx: int = 0
        self.lookahead_distance_m: float = 25.0
        self.target_steer: float = 0.0
        self.target_throttle: float = 0.0
        self.target_brake: float = 0.0
        self.use_nitro: bool = False
        self.lateral_offset: float = 0.0

    def compute_controls(
        self,
        car_pos: Tuple[float, float, float],
        car_yaw_rad: float,
        car_speed_mps: float,
        waypoints: List[Any],
        nearby_opponents: List[Dict[str, Any]],
        dt: float
    ) -> Dict[str, float]:
        if not waypoints:
            return {"steer": 0.0, "throttle": 0.8, "brake": 0.0, "nitro": False}

        # 1. Find target waypoint ahead based on speed-dependent lookahead
        self.lookahead_distance_m = max(15.0, min(50.0, car_speed_mps * 0.9))
        
        # Advance waypoint tracker
        best_dist = float('inf')
        for i in range(15):
            idx = (self.current_waypoint_idx + i) % len(waypoints)
            wp = waypoints[idx]
            d = math.hypot(wp.x - car_pos[0], wp.z - car_pos[2])
            if d < best_dist:
                best_dist = d
                self.current_waypoint_idx = idx

        # Target point lookahead
        target_idx = (self.current_waypoint_idx + max(2, int(self.lookahead_distance_m / 10.0))) % len(waypoints)
        target_wp = waypoints[target_idx]

        # 2. Steer calculation towards target
        dx = target_wp.x - car_pos[0]
        dz = target_wp.z - car_pos[2]
        desired_yaw = math.atan2(dx, dz)
        
        yaw_diff = (desired_yaw - car_yaw_rad + math.pi) % (2.0 * math.pi) - math.pi
        self.target_steer = max(-1.0, min(1.0, yaw_diff * 1.8 * self.personality.cornering_precision))

        # 3. Speed & braking control
        turn_severity = abs(yaw_diff)
        target_speed_mps = target_wp.speed_limit_mps * (1.0 - turn_severity * 0.55 * (1.0 - self.personality.risk_tolerance * 0.3))
        
        if car_speed_mps < target_speed_mps:
            self.target_throttle = 1.0
            self.target_brake = 0.0
            # Use nitro on straightaways if aggressive/risky
            self.use_nitro = (turn_severity < 0.1 and car_speed_mps > 20.0 and self.personality.aggression > 0.6)
        else:
            self.target_throttle = 0.0
            overshoot = car_speed_mps - target_speed_mps
            self.target_brake = max(0.0, min(1.0, (overshoot / 10.0) * (1.2 - self.personality.risk_tolerance * 0.4)))
            self.use_nitro = False

        # 4. Collision avoidance override
        for opp in nearby_opponents:
            opp_dx = opp["x"] - car_pos[0]
            opp_dz = opp["z"] - car_pos[2]
            opp_dist = math.hypot(opp_dx, opp_dz)
            
            if opp_dist < 8.0:
                # Close proximity!
                if opp_dz > 0:  # Opponent in front
                    if self.personality.aggression < 0.7:
                        self.target_brake = max(self.target_brake, 0.4)
                    # Steer away laterally
                    if opp_dx > 0:
                        self.target_steer = max(-1.0, self.target_steer - 0.4)
                    else:
                        self.target_steer = min(1.0, self.target_steer + 0.4)

        return {
            "steer": round(self.target_steer, 3),
            "throttle": round(self.target_throttle, 3),
            "brake": round(self.target_brake, 3),
            "nitro": self.use_nitro
        }
