import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RoadVision AI Backend"
    VERSION: str = "2.0.0"
    API_PREFIX: str = "/api/v1"
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "roadvision_db")
    
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "models/best.pt")
    DEDUPLICATION_RADIUS_METERS: float = 10.0

settings = Settings()
