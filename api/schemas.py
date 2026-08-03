from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any

# Authentication Schemas
class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., example="citizen@example.com")
    password: str = Field(..., min_length=6, example="securepassword")
    full_name: str = Field(..., example="John Doe")
    role: str = Field("citizen", example="citizen") # 'citizen' or 'admin'

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., example="citizen@example.com")
    password: str = Field(..., example="securepassword")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str

# Location & AI Schemas
class LocationSchema(BaseModel):
    latitude: Optional[float] = Field(None, example=37.7749)
    longitude: Optional[float] = Field(None, example=-122.4194)
    road_name: Optional[str] = Field(None, example="Market Street")
    city: Optional[str] = Field(None, example="San Francisco")
    district: Optional[str] = Field(None, example="Central District")
    state: Optional[str] = Field(None, example="California")

class SingleDamageDetectionSchema(BaseModel):
    damage_type: str = Field(..., example="Pothole")
    severity: str = Field(..., example="High")
    confidence: float = Field(..., example=0.94)
    priority_score: float = Field(..., example=82.5)
    bbox: List[float] = Field(..., example=[120.5, 200.0, 350.2, 410.8])
    estimated_width_m: float = Field(..., example=0.85)
    estimated_length_m: float = Field(..., example=0.92)
    estimated_area_m2: float = Field(..., example=0.78)
    estimated_depth_cm: Optional[float] = Field(..., example=7.5)
    road_occupancy_pct: float = Field(..., example=8.45)
    location: LocationSchema
    timestamp: str

class PredictionResponse(BaseModel):
    image_id: str
    source_type: str
    total_damages_found: int
    inference_time_ms: float
    detections: List[SingleDamageDetectionSchema]
    db_action: Optional[str] = Field("created", example="created")
    matched_duplicate_distance_m: Optional[float] = Field(0.0, example=2.4)

class BatchPredictionResponse(BaseModel):
    total_images_processed: int
    total_damages_detected: int
    results: List[PredictionResponse]

class AssignRepairSchema(BaseModel):
    contractor_name: str = Field(..., example="Municipal Paving Corp")
    assigned_team_id: str = Field(..., example="TEAM-WEST-02")
    notes: Optional[str] = Field(None, example="Priority urgent pothole patch")

class SystemStatsResponse(BaseModel):
    total_complaints: int
    critical: int
    high: int
    medium: int
    low: int
    pending_repairs: int
    completed_repairs: int
    citizen_reports: int
    government_reports: int
