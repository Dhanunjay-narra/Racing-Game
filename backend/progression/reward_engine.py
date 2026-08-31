from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RaceRewardCalculation:
    base_credits: int
    position_bonus_credits: int
    clean_race_bonus_credits: int
    drift_bonus_credits: int
    total_credits: int
    base_xp: int
    podium_xp: int
    total_xp: int
    tuning_alloys: int
    season_tokens: int


class CentralizedRewardEngine:
    POSITION_MULTIPLIERS = {1: 3.0, 2: 2.2, 3: 1.6, 4: 1.2, 5: 1.0, 6: 0.8}

    @classmethod
    def calculate_race_rewards(
        cls,
        finish_position: int,
        total_racers: int,
        clean_race: bool,
        drift_score: int,
        top_speed_kmh: float,
        tier: int = 1
    ) -> RaceRewardCalculation:
        base_cr = 1500 * tier
        mult = cls.POSITION_MULTIPLIERS.get(finish_position, 0.6)
        pos_cr = int(base_cr * (mult - 1.0)) if mult > 1.0 else 0
        clean_cr = int(base_cr * 0.25) if clean_race else 0
        drift_cr = int(min(1500, drift_score * 0.15))
        total_cr = base_cr + pos_cr + clean_cr + drift_cr

        base_xp = 350 * tier
        podium_xp = 250 if finish_position <= 3 else 0
        total_xp = base_xp + podium_xp + (100 if clean_race else 0)

        alloys = 3 if finish_position == 1 else (2 if finish_position <= 3 else 1)
        season_tok = 20 if finish_position == 1 else 10

        return RaceRewardCalculation(
            base_credits=base_cr,
            position_bonus_credits=pos_cr,
            clean_race_bonus_credits=clean_cr,
            drift_bonus_credits=drift_cr,
            total_credits=total_cr,
            base_xp=base_xp,
            podium_xp=podium_xp,
            total_xp=total_xp,
            tuning_alloys=alloys,
            season_tokens=season_tok
        )
