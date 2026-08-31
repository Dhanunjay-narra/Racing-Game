from dataclasses import dataclass
from typing import Dict, List


@dataclass
class VehicleDefinition:
    id: str
    name: str
    brand: str
    category: str  # Street, Sports, Super, Hyper, Off-Road, Rally, Classic, Electric, Prototype, Special
    tier: int      # 1 to 5
    rarity: str    # Common, Rare, Epic, Legendary, Mythic
    
    # Specs
    top_speed_kmh: float
    accel_0_100_s: float
    handling_score: float
    braking_score: float
    drift_score: float
    curb_weight_kg: float
    drivetrain: str
    engine_desc: str
    max_rpm: float
    horsepower: float
    torque_nm: float
    price_credits: int
    price_gold: int
    unlocked_by_default: bool = False


class VehicleCatalogService:
    VEHICLES: Dict[str, VehicleDefinition] = {
        "apex_rs1": VehicleDefinition(
            id="apex_rs1",
            name="Apex RS-1",
            brand="Nexus Motorworks",
            category="Sports",
            tier=1,
            rarity="Common",
            top_speed_kmh=265.0,
            accel_0_100_s=4.1,
            handling_score=72.0,
            braking_score=70.0,
            drift_score=75.0,
            curb_weight_kg=1380.0,
            drivetrain="RWD",
            engine_desc="2.0L Turbocharged Inline-4",
            max_rpm=8000.0,
            horsepower=340.0,
            torque_nm=420.0,
            price_credits=0,
            price_gold=0,
            unlocked_by_default=True
        ),
        "vortex_gt": VehicleDefinition(
            id="vortex_gt",
            name="Vortex GT-R",
            brand="Kurogane Precision",
            category="Sports",
            tier=2,
            rarity="Rare",
            top_speed_kmh=305.0,
            accel_0_100_s=3.4,
            handling_score=80.0,
            braking_score=78.0,
            drift_score=82.0,
            curb_weight_kg=1490.0,
            drivetrain="AWD",
            engine_desc="3.0L Twin-Turbo Inline-6",
            max_rpm=8500.0,
            horsepower=510.0,
            torque_nm=600.0,
            price_credits=45000,
            price_gold=0
        ),
        "phantom_hyperion": VehicleDefinition(
            id="phantom_hyperion",
            name="Phantom Hyperion",
            brand="AeroDynamix",
            category="Super",
            tier=3,
            rarity="Epic",
            top_speed_kmh=348.0,
            accel_0_100_s=2.8,
            handling_score=88.0,
            braking_score=86.0,
            drift_score=78.0,
            curb_weight_kg=1320.0,
            drivetrain="RWD",
            engine_desc="4.0L Twin-Turbo V8 Mid-Engine",
            max_rpm=9200.0,
            horsepower=750.0,
            torque_nm=780.0,
            price_credits=120000,
            price_gold=300
        ),
        "nemesis_valkyrie": VehicleDefinition(
            id="nemesis_valkyrie",
            name="Nemesis Valkyrie",
            brand="Kronos Hypercars",
            category="Hyper",
            tier=4,
            rarity="Legendary",
            top_speed_kmh=395.0,
            accel_0_100_s=2.3,
            handling_score=94.0,
            braking_score=93.0,
            drift_score=84.0,
            curb_weight_kg=1250.0,
            drivetrain="AWD",
            engine_desc="6.5L Naturally Aspirated V12 + Quad Hybrid Motors",
            max_rpm=10500.0,
            horsepower=1150.0,
            torque_nm=1100.0,
            price_credits=350000,
            price_gold=1200
        ),
        "celestial_void_x": VehicleDefinition(
            id="celestial_void_x",
            name="Celestial Void-X",
            brand="Aether Quantum",
            category="Prototype",
            tier=5,
            rarity="Mythic",
            top_speed_kmh=445.0,
            accel_0_100_s=1.85,
            handling_score=99.0,
            braking_score=98.0,
            drift_score=90.0,
            curb_weight_kg=1100.0,
            drivetrain="Torque-Vectoring AWD",
            engine_desc="Solid-State Flux Quad Electric Powertrain",
            max_rpm=18000.0,
            horsepower=1600.0,
            torque_nm=1800.0,
            price_credits=1000000,
            price_gold=5000
        ),
        "gladiator_baja": VehicleDefinition(
            id="gladiator_baja",
            name="Gladiator Baja Trophy",
            brand="Ironclad Heavy",
            category="Off-Road",
            tier=2,
            rarity="Rare",
            top_speed_kmh=240.0,
            accel_0_100_s=4.5,
            handling_score=68.0,
            braking_score=72.0,
            drift_score=88.0,
            curb_weight_kg=1850.0,
            drivetrain="4WD",
            engine_desc="6.2L Supercharged V8",
            max_rpm=7500.0,
            horsepower=650.0,
            torque_nm=820.0,
            price_credits=55000,
            price_gold=0
        )
    }

    @classmethod
    def get_all(cls) -> List[VehicleDefinition]:
        return list(cls.VEHICLES.values())

    @classmethod
    def get_by_id(cls, vehicle_id: str) -> VehicleDefinition:
        return cls.VEHICLES.get(vehicle_id, cls.VEHICLES["apex_rs1"])
