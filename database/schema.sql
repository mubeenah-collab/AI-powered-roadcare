-- RoadVision PostGIS Database Schema (Human-Readable Address + Internal Coordinates)

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
    
    -- Internal Coordinates (GIS Mapping, Heatmaps, Spatial Queries, Duplicate Detection)
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)) STORED,
    
    -- Display Fields (Human-Readable Address for Users & Frontend Display)
    road_name TEXT NULL,
    area TEXT NULL,
    city TEXT NULL,
    district TEXT NULL,
    state TEXT NULL,
    country TEXT NULL,
    postal_code TEXT NULL,
    formatted_address TEXT NULL,
    
    -- 8-Stage Repair Lifecycle
    status VARCHAR(100) NOT NULL DEFAULT 'Pending Verification',
    verification_count INT NOT NULL DEFAULT 1,
    assigned_contractor TEXT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_damage_reports_geom ON damage_reports USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_damage_reports_status ON damage_reports (status);
CREATE INDEX IF NOT EXISTS idx_damage_reports_priority ON damage_reports (priority_score DESC);
