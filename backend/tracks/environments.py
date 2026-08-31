from dataclasses import dataclass
from typing import Dict, List


@dataclass
class EnvironmentPreset:
    id: str
    name: str
    description: str
    sky_gradient_top: str
    sky_gradient_bottom: str
    ambient_light_color: str
    sun_light_color: str
    fog_color: str
    fog_density: float
    road_texture: str
    road_roughness: float
    puddle_reflectivity: float
    default_weather: str


class EnvironmentCatalog:
    ENVIRONMENTS: Dict[str, EnvironmentPreset] = {
        "neon_cyber_city": EnvironmentPreset(
            id="neon_cyber_city",
            name="Neon Cyber City",
            description="High-tech futuristic metropolis with rain-slicked asphalt and neon billboards.",
            sky_gradient_top="#050515",
            sky_gradient_bottom="#150a30",
            ambient_light_color="#302060",
            sun_light_color="#00ffff",
            fog_color="#100520",
            fog_density=0.0018,
            road_texture="asphalt_slick",
            road_roughness=0.15,
            puddle_reflectivity=0.92,
            default_weather="Rain"
        ),
        "pacific_coast_highway": EnvironmentPreset(
            id="pacific_coast_highway",
            name="Pacific Coast Highway",
            description="Sun-drenched coastal highway flanked by ocean cliffs and palm trees.",
            sky_gradient_top="#0088ff",
            sky_gradient_bottom="#cce6ff",
            ambient_light_color="#ffffff",
            sun_light_color="#fffae0",
            fog_color="#c0e0ff",
            fog_density=0.0004,
            road_texture="asphalt_smooth",
            road_roughness=0.35,
            puddle_reflectivity=0.10,
            default_weather="Clear"
        ),
        "alpine_ridge": EnvironmentPreset(
            id="alpine_ridge",
            name="Alpine Ridge Pass",
            description="Winding mountainous switchbacks through snowy peaks and pine forests.",
            sky_gradient_top="#2a4565",
            sky_gradient_bottom="#9ab8d6",
            ambient_light_color="#b0c8e0",
            sun_light_color="#eef8ff",
            fog_color="#9ab0c4",
            fog_density=0.0012,
            road_texture="tarmac_mountain",
            road_roughness=0.45,
            puddle_reflectivity=0.30,
            default_weather="Snow"
        ),
        "sahara_dunes": EnvironmentPreset(
            id="sahara_dunes",
            name="Sahara Dunes Circuit",
            description="Blistering desert circuit surrounded by towering sand dunes and heat mirages.",
            sky_gradient_top="#ff9933",
            sky_gradient_bottom="#ffeecc",
            ambient_light_color="#ffe0b2",
            sun_light_color="#fff4cc",
            fog_color="#f0d0a0",
            fog_density=0.0008,
            road_texture="asphalt_dusty",
            road_roughness=0.55,
            puddle_reflectivity=0.00,
            default_weather="Sandstorm"
        ),
        "tokyo_underground": EnvironmentPreset(
            id="tokyo_underground",
            name="Tokyo Underground Expressway",
            description="Narrow expressway tunnels with sodium-vapor tunnel lights and highway overpasses.",
            sky_gradient_top="#000000",
            sky_gradient_bottom="#0f111a",
            ambient_light_color="#ffaa44",
            sun_light_color="#ffdd88",
            fog_color="#121520",
            fog_density=0.0015,
            road_texture="concrete_grooved",
            road_roughness=0.25,
            puddle_reflectivity=0.60,
            default_weather="Night"
        ),
        "nordic_glacier": EnvironmentPreset(
            id="nordic_glacier",
            name="Nordic Glacier Run",
            description="Sub-zero arctic racing over frozen fjord bridges and glacial ice caves.",
            sky_gradient_top="#082035",
            sky_gradient_bottom="#6095b5",
            ambient_light_color="#90c0e0",
            sun_light_color="#d0f0ff",
            fog_color="#70a0c0",
            fog_density=0.0020,
            road_texture="packed_snow",
            road_roughness=0.20,
            puddle_reflectivity=0.85,
            default_weather="Snow"
        ),
        "monza_grand_circuit": EnvironmentPreset(
            id="monza_grand_circuit",
            name="Monza Grand Circuit",
            description="Historic high-speed professional raceway with banked curves and chicane complexes.",
            sky_gradient_top="#1a75ff",
            sky_gradient_bottom="#e6f0ff",
            ambient_light_color="#f5f5f5",
            sun_light_color="#ffffff",
            fog_color="#e0e8f0",
            fog_density=0.0003,
            road_texture="track_racing_rubber",
            road_roughness=0.22,
            puddle_reflectivity=0.15,
            default_weather="Clear"
        ),
        "volcanic_caldera": EnvironmentPreset(
            id="volcanic_caldera",
            name="Volcanic Caldera Pass",
            description="Dangerous volcanic circuit through basalt canyons with glowing magma fissures.",
            sky_gradient_top="#200505",
            sky_gradient_bottom="#5a1005",
            ambient_light_color="#ff3300",
            sun_light_color="#ff6600",
            fog_color="#401005",
            fog_density=0.0022,
            road_texture="basalt_pavement",
            road_roughness=0.50,
            puddle_reflectivity=0.40,
            default_weather="Sunset"
        )
    }

    @classmethod
    def get_environment(cls, env_id: str) -> EnvironmentPreset:
        return cls.ENVIRONMENTS.get(env_id, cls.ENVIRONMENTS["pacific_coast_highway"])
