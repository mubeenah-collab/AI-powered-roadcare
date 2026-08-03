import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Text, JSON
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="citizen") # 'citizen' or 'administrator'
    created_at = Column(DateTime, default=datetime.utcnow)

class DamageReportModel(Base):
    __tablename__ = "damage_reports"

    id = Column(String(100), primary_key=True)
    image_id = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False, default="Citizen")

    # Detection AI Attributes
    damage_type = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False, default="Low")
    priority_score = Column(Integer, nullable=False, default=0, index=True)

    # Monocular 3D Metric Estimates
    estimated_width_m = Column(Float, nullable=True)
    estimated_length_m = Column(Float, nullable=True)
    estimated_area_m2 = Column(Float, nullable=True)
    estimated_depth_cm = Column(Float, nullable=True)
    road_occupancy = Column(Float, nullable=True)
    road_health_score = Column(Float, nullable=True)
    road_condition = Column(String(50), nullable=True)

    # Weather Data
    weather_condition = Column(String(50), nullable=True)
    temperature_c = Column(Float, nullable=True)
    humidity_pct = Column(Integer, nullable=True)
    visibility_km = Column(Float, nullable=True)
    wind_speed_kmh = Column(Integer, nullable=True)
    rain_probability_pct = Column(Integer, nullable=True)
    weather_risk = Column(String(50), nullable=True)

    # Government Fleet Metadata
    vehicle_id = Column(String(100), nullable=True)
    vehicle_type = Column(String(100), nullable=True)
    department = Column(String(150), nullable=True)
    camera_id = Column(String(100), nullable=True)
    driver_name = Column(String(150), nullable=True)
    inspection_route = Column(String(255), nullable=True)
    shift = Column(String(50), nullable=True)

    # Repair Images
    before_image_url = Column(Text, nullable=True)
    after_image_url = Column(Text, nullable=True)

    # Timeline JSON
    timeline = Column(JSON, nullable=True)

    # Internal Coordinates
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Display Address Fields
    road_name = Column(Text, nullable=True)
    area = Column(Text, nullable=True)
    city = Column(Text, nullable=True)
    district = Column(Text, nullable=True)
    state = Column(Text, nullable=True)
    country = Column(Text, nullable=True)
    postal_code = Column(Text, nullable=True)
    formatted_address = Column(Text, nullable=True)

    # Status Lifecycle
    status = Column(String(100), nullable=False, default="Pending Verification", index=True)
    verification_count = Column(Integer, nullable=False, default=1)
    assigned_contractor = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FleetVehicleModel(Base):
    __tablename__ = "fleet_vehicles"

    vehicle_id = Column(String(100), primary_key=True)
    vehicle_type = Column(String(100), nullable=False)
    department = Column(String(150), nullable=False)
    camera_id = Column(String(100), nullable=False)
    driver_name = Column(String(150), nullable=True)
    inspection_route = Column(String(255), nullable=True)
    shift = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="active")
    last_latitude = Column(Float, nullable=True)
    last_longitude = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NotificationModel(Base):
    __tablename__ = "notifications"

    id = Column(String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
