import pytest
from backend.progression.reward_engine import CentralizedRewardEngine


def test_reward_engine_first_place_multiplier():
    rewards_p1 = CentralizedRewardEngine.calculate_race_rewards(
        finish_position=1,
        total_racers=8,
        clean_race=True,
        drift_score=500,
        top_speed_kmh=280.0,
        tier=2
    )
    rewards_p5 = CentralizedRewardEngine.calculate_race_rewards(
        finish_position=5,
        total_racers=8,
        clean_race=False,
        drift_score=0,
        top_speed_kmh=220.0,
        tier=2
    )
    
    assert rewards_p1.total_credits > rewards_p5.total_credits
    assert rewards_p1.total_xp > rewards_p5.total_xp
    assert rewards_p1.tuning_alloys >= rewards_p5.tuning_alloys
