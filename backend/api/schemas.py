from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AuthLoginRequestSchema(BaseModel):
    username: str = Field(..., example="citizen@roadvision.gov.in")
    password: str = Field(..., example="password123")

class AuthLoginResponseSchema(BaseModel):
    access_token: str = Field(..., example="jwt_token_sample_12345")
    token_type: str = Field("bearer", example="bearer")
    role: str = Field(..., example="citizen")  # 'citizen' or 'admin'
    user_email: str = Field(..., example="citizen@roadvision.gov.in")

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

class WeatherSchema(BaseModel):
    condition: str = Field(..., example="Rainy")
    temperature_c: float = Field(..., example=31.0)
    humidity_pct: int = Field(..., example=82)
    visibility_km: float = Field(..., example=4.0)
    wind_speed_kmh: int = Field(..., example=18)
    rain_probability_pct: int = Field(..., example=85)
    weather_risk: str = Field(..., example="High")
    priority_boost: int = Field(..., example=15)
    weather_risk_reason: str = Field(..., example="Continuous rainfall may worsen pothole damage.")

class FleetMetadataSchema(BaseModel):
    vehicle_id: str = Field(..., example="TN01-GOV-024")
    vehicle_type: str = Field(..., example="Government Bus")
    department: str = Field(..., example="Greater Chennai Corporation")
    camera_id: str = Field(..., example="CAM-003")
    driver_name: Optional[str] = Field("R. Sundaram", example="R. Sundaram")
    inspection_route: str = Field(..., example="Anna Salai Route")
    shift: str = Field(..., example="Morning")

class TimelineEventSchema(BaseModel):
    date_time: str = Field(..., example="2026-08-03 18:46:48")
    stage: str = Field(..., example="Reported")
    officer_name: str = Field(..., example="System Ingestion")
    comments: str = Field(..., example="Road damage report received.")

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
    weather: WeatherSchema
    fleet_info: Optional[FleetMetadataSchema] = None
    timeline: List[TimelineEventSchema]
    before_image_url: Optional[str] = Field("assets/images/before_repair_sample.jpg", example="assets/images/before_repair_sample.jpg")
    after_image_url: Optional[str] = Field(None, example="assets/images/after_repair_sample.jpg")
    complaint_id: str = Field(..., example="RV-2026-001245")
    status: str = Field(..., example="Pending Verification")
    timestamp: str
    source: str = Field(..., example="Citizen")
    road_health_score: float = Field(..., example=24.5)
    road_condition: str = Field(..., example="Poor")

class CompleteRepairPayloadSchema(BaseModel):
    after_image_url: str = Field(..., example="assets/images/after_repair_sample.jpg")
    officer_name: str = Field(..., example="Officer K. Rajan")
    comments: str = Field(..., example="Resurfacing completed with high-durability asphalt patch.")

class AdvancedAnalyticsSchema(BaseModel):
    total_roads_scanned_km: int
    total_images_processed: int
    citizen_reports_count: int
    government_fleet_count: int
    average_ai_accuracy_pct: float
    average_confidence_pct: float
    average_road_health_score: float
    average_repair_time_days: float
    critical_defects_count: int
    pending_verification: int
    assigned_repairs: int
    completed_repairs: int
    most_dangerous_zone: str
    most_reported_road: str
    most_active_vehicle: str
    repair_completion_rate_pct: float
