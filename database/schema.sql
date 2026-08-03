-- RoadVision PostGIS Database Schema
-- Enables Spatial Extensions and Tables for Citizen & Government Fleet Inspection

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enum types for data sources, severity, and repair lifecycle
CREATE TYPE data_source_enum AS ENUM ('citizen', 'government_fleet');
CREATE TYPE severity_level_enum AS ENUM ('Low', 'Medium', 'High', 'Critical');
CREATE TYPE repair_status_enum AS ENUM ('pending', 'assigned', 'in_progress', 'completed', 'archived');

-- Main Damage Detections Table
CREATE TABLE IF NOT EXISTS damage_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id VARCHAR(255) NOT NULL,
    source_type data_source_enum NOT NULL DEFAULT 'citizen',
    vehicle_id VARCHAR(100) NULL,
    citizen_id VARCHAR(100) NULL,
    
    -- Detection AI Attributes
    damage_type VARCHAR(100) NOT NULL,
    confidence FLOAT NOT NULL,
    severity severity_level_enum NOT NULL DEFAULT 'Low',
    priority_score FLOAT NOT NULL DEFAULT 0.0,
    
    -- Monocular 3D Metric Estimates
    estimated_width_m FLOAT NULL,
    estimated_length_m FLOAT NULL,
    estimated_area_m2 FLOAT NULL,
    estimated_depth_cm FLOAT NULL,
    road_occupancy_pct FLOAT NULL,
    
    -- Bounding Box (xmin, ymin, xmax, ymax) stored as JSON
    bbox JSONB NOT NULL,
    
    -- Geographic & Address Metadata
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)) STORED,
    
    road_name VARCHAR(255) NULL,
    city VARCHAR(100) NULL,
    district VARCHAR(100) NULL,
    state VARCHAR(100) NULL,
    country VARCHAR(100) NULL,
    
    -- Maintenance Workflow & Deduplication
    status repair_status_enum NOT NULL DEFAULT 'pending',
    verification_count INT NOT NULL DEFAULT 1,
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    assigned_contractor VARCHAR(255) NULL,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Spatial GIST Index for Ultra-fast Spatial Range & Deduplication Queries
CREATE INDEX IF NOT EXISTS idx_damage_reports_geom ON damage_reports USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_damage_reports_status ON damage_reports (status);
CREATE INDEX IF NOT EXISTS idx_damage_reports_priority ON damage_reports (priority_score DESC);

-- Duplicate Merges Log Table
CREATE TABLE IF NOT EXISTS report_merges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    primary_report_id UUID NOT NULL REFERENCES damage_reports(id) ON DELETE CASCADE,
    duplicate_image_id VARCHAR(255) NOT NULL,
    source_type data_source_enum NOT NULL,
    distance_meters FLOAT NOT NULL,
    merged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Government Fleet Tracking Table
CREATE TABLE IF NOT EXISTS fleet_vehicles (
    vehicle_id VARCHAR(100) PRIMARY KEY,
    vehicle_type VARCHAR(100) NOT NULL, -- 'Garbage Truck', 'Municipal Bus', 'Inspector Car'
    driver_name VARCHAR(255) NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    last_known_latitude DOUBLE PRECISION NULL,
    last_known_longitude DOUBLE PRECISION NULL,
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
