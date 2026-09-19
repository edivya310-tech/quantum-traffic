from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Quantum Traffic Optimization"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./traffic.db"
    
    SIMULATION_STEP_SECONDS: int = 1
    METRICS_SAMPLE_INTERVAL: int = 5
    OPTIMIZATION_INTERVAL: int = 30
    
    MIN_GREEN: int = 10
    MAX_GREEN: int = 60
    YELLOW_TIME: int = 3
    ALL_RED_TIME: int = 1
    
    QAOA_SHOTS: int = 1024
    QAOA_REPS: int = 1
    RANDOM_SEED: Optional[int] = 42
    
    TRAFFIC_ENGINE: str = "custom"
    ENABLE_QUANTUM: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
