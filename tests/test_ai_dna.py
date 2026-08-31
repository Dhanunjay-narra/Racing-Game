import pytest
from backend.ai.driver_dna_engine import DriverDNAAnalyzer, TelemetryFrame


def test_driver_dna_aggressive_classification():
    analyzer = DriverDNAAnalyzer()
    
    frames = [
        TelemetryFrame(
            timestamp_ms=i * 50,
            speed_kmh=220.0,
            throttle=1.0,
            brake=0.95 if i % 10 == 0 else 0.0,
            steer=0.2,
            slip_angle_deg=18.0 if i % 4 == 0 else 2.0,
            g_lat=1.2,
            g_long=0.8,
            distance_to_nearest_car_m=2.0,  # Aggressive close proximity
            collision_occurred=(i == 15),
            apex_distance_m=0.8,
            track_surface="asphalt_dry"
        )
        for i in range(50)
    ]
    
    dna = analyzer.analyze_race_session(frames)
    assert dna["aggression"] > 0.6
    assert dna["drifting"] > 0.0
    assert dna["archetype"] in ["Apex Predator", "Drift Monarch", "Balanced Prodigy"]
