import os

class Settings:
    PROJECT_NAME: str = "LifeLink - Emergency Resource Coordination Platform"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "lifelink_emergency_coordination_secret_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lifelink.db")
    DEFAULT_LAT: float = 20.2961  # Bhubaneswar coordinates
    DEFAULT_LNG: float = 85.8245

settings = Settings()
