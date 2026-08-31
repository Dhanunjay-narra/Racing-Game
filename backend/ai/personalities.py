from dataclasses import dataclass
from typing import Dict


@dataclass
class AIPersonality:
    name: str
    aggression: float          # 0.0 to 1.0 (propensity to ram / close-dive)
    cornering_precision: float # 0.0 to 1.0 (apex accuracy)
    overtake_urgency: float    # 0.0 to 1.0 (willingness to leave racing line)
    risk_tolerance: float      # 0.0 to 1.0 (late braking margin)
    drifting_tendency: float   # 0.0 to 1.0 (prefers oversteer vs grip)
    defensiveness: float       # 0.0 to 1.0 (blocks overtaking opponents)
    mistake_chance: float      # 0.0 to 1.0 (frequency of lockups/spins)


class AIPersonalityPresets:
    AGGRESSIVE = AIPersonality(
        name="Aggressive Brawler",
        aggression=0.90,
        cornering_precision=0.75,
        overtake_urgency=0.95,
        risk_tolerance=0.88,
        drifting_tendency=0.60,
        defensiveness=0.85,
        mistake_chance=0.08
    )
    
    TECHNICAL = AIPersonality(
        name="Technical Purist",
        aggression=0.35,
        cornering_precision=0.98,
        overtake_urgency=0.60,
        risk_tolerance=0.45,
        drifting_tendency=0.10,
        defensiveness=0.50,
        mistake_chance=0.02
    )
    
    BALANCED = AIPersonality(
        name="Balanced Racer",
        aggression=0.55,
        cornering_precision=0.80,
        overtake_urgency=0.70,
        risk_tolerance=0.60,
        drifting_tendency=0.40,
        defensiveness=0.60,
        mistake_chance=0.05
    )
    
    RISKY = AIPersonality(
        name="Daredevil Gambler",
        aggression=0.80,
        cornering_precision=0.65,
        overtake_urgency=0.90,
        risk_tolerance=0.98,
        drifting_tendency=0.85,
        defensiveness=0.40,
        mistake_chance=0.14
    )
    
    DEFENSIVE = AIPersonality(
        name="Iron Wall Tactician",
        aggression=0.40,
        cornering_precision=0.85,
        overtake_urgency=0.50,
        risk_tolerance=0.35,
        drifting_tendency=0.20,
        defensiveness=0.98,
        mistake_chance=0.03
    )

    @classmethod
    def get_by_name(cls, name: str) -> AIPersonality:
        mapping = {
            "aggressive": cls.AGGRESSIVE,
            "technical": cls.TECHNICAL,
            "balanced": cls.BALANCED,
            "risky": cls.RISKY,
            "defensive": cls.DEFENSIVE
        }
        return mapping.get(name.lower(), cls.BALANCED)
