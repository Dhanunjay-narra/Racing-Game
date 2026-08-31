from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Velocity Nexus"
    PROJECT_VERSION: str = "2.4.0"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WS_PORT: int = Field(default=8765, env="WS_PORT")
    ALLOWED_ORIGINS: List[str] = ["*"]
    API_V1_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = Field(default="nexus_super_secret_production_key_2026_jwt_token_auth", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./velocity_nexus.db",
        env="DATABASE_URL"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False
    
    REDIS_URL: Optional[str] = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    TICK_RATE: int = 60
    PHYSICS_SUBSTEPS: int = 2
    MAX_PLAYERS_PER_ROOM: int = 12
    MAX_SPECTATORS_PER_ROOM: int = 50
    SERVER_TIMEOUT_SECONDS: int = 30
    PING_INTERVAL_SECONDS: int = 5
    
    GRAVITY: float = 9.81
    DEFAULT_AIR_DENSITY: float = 1.225
    BASE_TIRE_FRICTION: float = 1.15
    SPEED_OF_SOUND: float = 343.0
    
    DEFAULT_MMR: int = 1200
    MMR_K_FACTOR: int = 32
    MATCHMAKING_EXPANSION_INTERVAL_SEC: int = 10
    
    STARTING_CREDITS: int = 50000
    STARTING_NEXUS_GOLD: int = 500
    STARTING_RACE_TICKETS: int = 10
    
    MAX_PLAUSIBLE_SPEED_MPS: float = 135.0
    MAX_PLAUSIBLE_ACCEL_MPS2: float = 35.0
    MAX_POSITION_DISCREPANCY_METERS: float = 8.0
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"


settings = Settings()
