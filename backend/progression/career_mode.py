from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CareerStage:
    stage_id: str
    chapter: int
    title: str
    track_id: str
    race_mode: str
    laps: int
    required_car_tier: int
    target_time_ms: int
    reward_credits: int
    reward_gold: int
    reward_xp: int
    unlocked_vehicle_id: str = ""


class CareerModeService:
    CHAPTERS: Dict[int, Dict[str, Any]] = {
        1: {
            "name": "Rookie Ignition",
            "desc": "Master baseline vehicle handling and cornering fundamentals.",
            "stages": [
                CareerStage("c1_s1", 1, "First Contact", "pacific_coast_highway", "Sprint", 1, 1, 95000, 3000, 20, 250),
                CareerStage("c1_s2", 1, "Coastal Breeze", "pacific_coast_highway", "Circuit", 2, 1, 140000, 4500, 30, 350),
                CareerStage("c1_s3", 1, "Neon Infiltration", "neon_cyber_city", "Circuit", 2, 1, 155000, 6000, 50, 500, "vortex_gt")
            ]
        },
        2: {
            "name": "Street Dominance",
            "desc": "Push sports-grade machinery to the limits in tight urban circuits.",
            "stages": [
                CareerStage("c2_s1", 2, "Tunnel Velocity", "tokyo_underground", "Sprint", 1, 2, 85000, 7500, 40, 600),
                CareerStage("c2_s2", 2, "Desert Heat", "sahara_dunes", "Circuit", 3, 2, 180000, 10000, 60, 800),
                CareerStage("c2_s3", 2, "Baja King Showdown", "sahara_dunes", "Elimination", 3, 2, 210000, 15000, 100, 1200, "gladiator_baja")
            ]
        },
        3: {
            "name": "Professional Apex",
            "desc": "High-downforce supercars on world-class grand prix raceways.",
            "stages": [
                CareerStage("c3_s1", 3, "Monza Qualifier", "monza_grand_circuit", "TimeTrial", 1, 3, 78000, 18000, 80, 1500),
                CareerStage("c3_s2", 3, "Alpine Drift Mastery", "alpine_ridge", "Drift", 2, 3, 160000, 24000, 120, 2000),
                CareerStage("c3_s3", 3, "Hyperion Boss Duel", "monza_grand_circuit", "Circuit", 3, 3, 220000, 40000, 250, 3500, "phantom_hyperion")
            ]
        }
    }

    @classmethod
    def get_chapter(cls, chapter_id: int) -> Dict[str, Any]:
        return cls.CHAPTERS.get(chapter_id, cls.CHAPTERS[1])
