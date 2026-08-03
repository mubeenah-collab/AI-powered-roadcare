from pydantic import BaseModel, Field
from typing import List, Optional

class LocationSchema(BaseModel):
    road_name: str = Field(..., example="Anna Salai")
    area: str = Field(..., example="Teynampet")
    city: str = Field(..., example="Chennai")
    district: str = Field(..., example="Chennai")
    state: str = Field(..., example="Tamil Nadu")
    country: str = Field(..., example="India")
    postal_code: str = Field(..., example="600018")
    formatted_address: Optional[str] = Field(None, example="Anna Salai, Teynampet, Chennai, Tamil Nadu")

class CoordinatesSchema(BaseModel):
    latitude: float = Field(..., example=12.926543)
    longitude: float = Field(..., example=80.143287)

class DamagePredictionSchema(BaseModel):
    damage_type: str = Field(..., example="Pothole")
    confidence: float = Field(..., example=0.964)
    severity: str = Field(..., example="High")
    priority_score: int = Field(..., example=89)
    estimated_width_m: float = Field(..., example=0.82)
    estimated_length_m: float = Field(..., example=1.05)
    estimated_area_m2: float = Field(..., example=0.86)
    estimated_depth_cm: float = Field(..., example=8.7)
    road_occupancy: float = Field(..., example=8.4)
    location: LocationSchema
    coordinates: CoordinatesSchema
    complaint_id: str = Field(..., example="RV-2026-001245")
    status: str = Field(..., example="Pending Verification")
    timestamp: str
    source: str = Field(..., example="Citizen")
    road_health_score: float = Field(..., example=24.5)
    road_condition: str = Field(..., example="Poor")

class LifecycleStatusUpdateSchema(BaseModel):
    status: str = Field(..., example="Assigned")
    contractor_name: Optional[str] = Field(None, example="Municipal Paving Corp")
    assigned_team_id: Optional[str] = Field(None, example="TEAM-WEST-02")
    notes: Optional[str] = Field(None, example="Road surface patched and verified.")

class SystemAnalyticsSchema(BaseModel):
    total_complaints: int
    critical_defects: int
    high_defects: int
    pending_repairs: int
    completed_repairs: int
    citizen_reports_count: int
    government_fleet_count: int
