from dataclasses import dataclass
from typing import Dict


@dataclass
class SurfaceProperty:
    name: str
    friction_coefficient: float
    rolling_resistance: float
    particle_fx: str
    skid_mark_darkness: float
    sound_type: str


class SurfaceManager:
    SURFACES: Dict[str, SurfaceProperty] = {
        "asphalt_dry": SurfaceProperty("Dry Asphalt", 1.15, 0.015, "rubber_smoke", 0.9, "tires_dry"),
        "asphalt_wet": SurfaceProperty("Wet Asphalt", 0.82, 0.020, "water_spray", 0.4, "tires_wet"),
        "concrete": SurfaceProperty("Smooth Concrete", 1.10, 0.014, "rubber_smoke", 0.8, "tires_dry"),
        "gravel": SurfaceProperty("Loose Gravel", 0.65, 0.055, "gravel_dust", 0.0, "gravel_churn"),
        "dirt": SurfaceProperty("Packed Dirt", 0.72, 0.045, "dirt_cloud", 0.2, "dirt_churn"),
        "snow": SurfaceProperty("Packed Snow", 0.40, 0.060, "snow_roost", 0.0, "snow_swish"),
        "ice": SurfaceProperty("Black Ice", 0.18, 0.010, "ice_crystals", 0.0, "ice_slick"),
        "grass": SurfaceProperty("Trackside Grass", 0.50, 0.080, "grass_clippings", 0.1, "grass_brush"),
        "curb": SurfaceProperty("Rumble Strip", 1.05, 0.025, "rubber_smoke", 0.5, "curb_vibrate"),
        "sand": SurfaceProperty("Deep Sand", 0.35, 0.120, "sand_plume", 0.0, "sand_drag"),
    }

    @classmethod
    def get_surface(cls, surface_name: str) -> SurfaceProperty:
        return cls.SURFACES.get(surface_name, cls.SURFACES["asphalt_dry"])
