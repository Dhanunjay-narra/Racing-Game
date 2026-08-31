from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class UpgradeImpact:
    top_speed_delta_kmh: float
    accel_delta_s: float
    handling_delta: float
    braking_delta: float
    nitro_capacity_delta: float


class VehicleUpgradeEngine:
    UPGRADE_CATEGORIES = [
        "engine", "transmission", "brakes", "tires",
        "suspension", "aero", "turbo", "nitro", "weight_reduction"
    ]

    @staticmethod
    def calculate_cost(category: str, current_level: int) -> Dict[str, int]:
        if current_level >= 10:
            return {"credits": 0, "tuning_alloys": 0, "maxed": True}
            
        base_credits = {
            "engine": 3500, "turbo": 4200, "transmission": 3000,
            "tires": 2500, "brakes": 2200, "suspension": 2800,
            "aero": 3200, "nitro": 4000, "weight_reduction": 4500
        }.get(category, 3000)
        
        cost_credits = int(base_credits * (1.45 ** (current_level - 1)))
        cost_alloys = int(5 * current_level * 1.5)
        
        return {
            "credits": cost_credits,
            "tuning_alloys": cost_alloys,
            "maxed": False
        }

    @staticmethod
    def calculate_upgraded_stats(base_car: Any, upgrade_levels: Dict[str, int]) -> Dict[str, float]:
        speed_bonus = (upgrade_levels.get("engine", 1) * 3.5 + 
                       upgrade_levels.get("turbo", 1) * 4.2 + 
                       upgrade_levels.get("transmission", 1) * 2.0)
        
        accel_bonus = (upgrade_levels.get("engine", 1) * 0.08 + 
                       upgrade_levels.get("turbo", 1) * 0.10 + 
                       upgrade_levels.get("weight_reduction", 1) * 0.06 + 
                       upgrade_levels.get("tires", 1) * 0.05)
        
        handling_bonus = (upgrade_levels.get("suspension", 1) * 1.5 + 
                          upgrade_levels.get("aero", 1) * 1.8 + 
                          upgrade_levels.get("tires", 1) * 1.2)
        
        braking_bonus = (upgrade_levels.get("brakes", 1) * 2.2 + 
                         upgrade_levels.get("tires", 1) * 1.0)

        return {
            "top_speed_kmh": round(base_car.top_speed_kmh + speed_bonus, 1),
            "accel_0_100_s": round(max(1.4, base_car.accel_0_100_s - accel_bonus), 2),
            "handling_score": min(99.9, round(base_car.handling_score + handling_bonus, 1)),
            "braking_score": min(99.9, round(base_car.braking_score + braking_bonus, 1)),
            "nitro_duration_s": round(3.5 + upgrade_levels.get("nitro", 1) * 0.5, 1)
        }
