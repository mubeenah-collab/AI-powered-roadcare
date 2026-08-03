import os
from pydantic_settings import BaseSettings
from typing import Dict, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "RoadVision AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database Settings (PostgreSQL + PostGIS)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "roadvision_db")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis Settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    
    # Model Configuration
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "models/best.pt")
    CONFIDENCE_THRESHOLD: float = 0.35
    IOU_THRESHOLD: float = 0.45
    INPUT_IMAGE_SIZE: int = 640
    
    # Monocular Depth Estimation
    ENABLE_DEPTH_ESTIMATION: bool = True
    MIDAS_MODEL_TYPE: str = "DPT_Small"  # Choices: DPT_Large, DPT_Hybrid, DPT_Small
    
    # Spatial Deduplication
    DEDUPLICATION_RADIUS_METERS: float = 10.0  # Spatial buffer for merging duplicate reports
    
    # Class Mapping for RDD2022 + Custom Extended Classes
    CLASS_MAPPING: Dict[int, str] = {
        0: "Longitudinal Crack",  # D00
        1: "Transverse Crack",    # D10
        2: "Alligator Crack",     # D20
        3: "Pothole",             # D40
        4: "Surface Wear",        # D44 / Extended
        5: "Road Edge Failure"    # D50 / Extended
    }
    
    # Class Damage Weights for Severity Calculation
    CLASS_SEVERITY_WEIGHTS: Dict[str, float] = {
        "Pothole": 1.0,
        "Alligator Crack": 0.85,
        "Road Edge Failure": 0.75,
        "Transverse Crack": 0.60,
        "Longitudinal Crack": 0.50,
        "Surface Wear": 0.40
    }

settings = Settings()
