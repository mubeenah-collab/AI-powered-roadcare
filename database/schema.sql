-- RoadVision Production PostgreSQL + PostGIS Schema
-- Enables PostGIS spatial extensions, Spatial Indexing, and Tables for Users, Complaints, AI Results, Fleet, Weather, and Notifications.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS & ADMINS TABLE
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'citizen', -- 'citizen' or 'administrator'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. DAMAGE REPORTS & COMPLAINTS TABLE (PostGIS GEOMETRY(Point, 4326))
CREATE TABLE IF NOT EXISTS damage_reports (
    id VARCHAR(100) PRIMARY KEY,
    image_id VARCHAR(255) NOT NULL,
    source VARCHAR(50) NOT NULL DEFAULT 'Citizen',
    
    -- Detection AI Attributes
    damage_type VARCHAR(100) NOT NULL,
    confidence FLOAT NOT NULL,
    severity VARCHAR(50) NOT NULL DEFAULT 'Low',
    priority_score INT NOT NULL DEFAULT 0,
    
    -- Monocular 3D Metric Estimates
    estimated_width_m FLOAT NULL,
    estimated_length_m FLOAT NULL,
    estimated_area_m2 FLOAT NULL,
    estimated_depth_cm FLOAT NULL,
    road_occupancy FLOAT NULL,
    road_health_score FLOAT NULL,
    road_condition VARCHAR(50) NULL,
    
    -- Weather Data
    weather_condition VARCHAR(50) NULL,
    temperature_c FLOAT NULL,
    humidity_pct INT NULL,
    visibility_km FLOAT NULL,
    wind_speed_kmh INT NULL,
    rain_probability_pct INT NULL,
    weather_risk VARCHAR(50) NULL,
    
    -- Government Fleet Metadata
    vehicle_id VARCHAR(100) NULL,
    vehicle_type VARCHAR(100) NULL,
    department VARCHAR(150) NULL,
    camera_id VARCHAR(100) NULL,
    driver_name VARCHAR(150) NULL,
    inspection_route VARCHAR(255) NULL,
    shift VARCHAR(50) NULL,
    
    -- Before & After Repair Images
    before_image_url TEXT NULL,
    after_image_url TEXT NULL,
    
    -- Complaint Timeline (JSONB Array)
    timeline JSONB NULL,
    
    -- Internal Coordinates & PostGIS Geometry (SRID 4326 WGS84)
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)) STORED,
    
    -- Human-Readable Indian Display Address
    road_name TEXT NULL,
    area TEXT NULL,
    city TEXT NULL,
    district TEXT NULL,
    state TEXT NULL,
    country TEXT NULL,
    postal_code TEXT NULL,
    formatted_address TEXT NULL,
    
    -- 8-Stage Repair Lifecycle Status
    status VARCHAR(100) NOT NULL DEFAULT 'Pending Verification',
    verification_count INT NOT NULL DEFAULT 1,
    assigned_contractor TEXT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Spatial GIST Index for Ultra-Fast ST_DWithin PostGIS Deduplication
CREATE INDEX IF NOT EXISTS idx_damage_reports_geom ON damage_reports USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_damage_reports_status ON damage_reports (status);
CREATE INDEX IF NOT EXISTS idx_damage_reports_priority ON damage_reports (priority_score DESC);

-- 3. FLEET VEHICLES TABLE
CREATE TABLE IF NOT EXISTS fleet_vehicles (
    vehicle_id VARCHAR(100) PRIMARY KEY,
    vehicle_type VARCHAR(100) NOT NULL,
    department VARCHAR(150) NOT NULL,
    camera_id VARCHAR(100) NOT NULL,
    driver_name VARCHAR(150) NULL,
    inspection_route VARCHAR(255) NULL,
    shift VARCHAR(50) NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    last_latitude DOUBLE PRECISION NULL,
    last_longitude DOUBLE PRECISION NULL,
    geom GEOMETRY(Point, 4326) GENERATED ALWAYS AS (
        CASE 
            WHEN last_longitude IS NOT NULL AND last_latitude IS NOT NULL 
            THEN ST_SetSRID(ST_MakePoint(last_longitude, last_latitude), 4326) 
            ELSE NULL 
        END
    ) STORED,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
