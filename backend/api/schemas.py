from pydantic import BaseModel, Field
from typing import List, Optional

class DamagePredictionSchema(BaseModel):
    damage_type: str = Field(..., example="Pothole")
    confidence: float = Field(..., example=0.94)
    severity: str = Field(..., example="Critical")
    priority_score: int = Field(..., example=91)
    estimated_width_m: float = Field(..., example=0.85)
    estimated_length_m: float = Field(..., example=0.96)
    estimated_area_m2: float = Field(..., example=0.81)
    estimated_depth_cm: float = Field(..., example=9.2)
    road_occupancy: float = Field(..., example=8.4)
    latitude: float = Field(..., example=37.7749)
    longitude: float = Field(..., example=-122.4194)
    road_name: str = Field(..., example="Market Street")
    city: str = Field(..., example="San Francisco")
    timestamp: str
    source: str = Field(..., example="Citizen")
    road_health_score: float = Field(..., example=22.0)
    road_condition: str = Field(..., example="Critical")

class LifecycleStatusUpdateSchema(BaseModel):
    status: str = Field(..., example="Assigned") # Reported -> AI Detection -> Pending Verification -> Verified -> Assigned -> Repair In Progress -> Completed -> Closed
    contractor_name: Optional[str] = Field(None, example="Municipal Paving Corp")
    assigned_team_id: Optional[str] = Field(None, example="TEAM-WEST-02")
    notes: Optional[str] = Field(None, example="Road surface patched and verified.")

class SystemAnalyticsSchema(BaseModel):
    total_complaints: int
    critical_defects: int
    high_defects: int
    pending_verification: int
    assigned_repairs: int
    repairs_in_progress: int
    completed_repairs: int
    citizen_reports_count: int
    government_fleet_count: int
    average_road_health: float
